#!/usr/bin/env python3
"""Recursively mirror OpenAI Codex developer docs into a local directory.

Default behavior:
  - Start at https://developers.openai.com/codex
  - Crawl only pages under /codex on developers.openai.com
  - Download same-origin assets referenced by those pages
  - Do not scan the full site sitemap unless --use-sitemap is passed
  - Save files under ./codex_docs

The script uses only Python's standard library.
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import dataclasses
import hashlib
import html.parser
import mimetypes
import posixpath
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable


DEFAULT_START_URL = "https://developers.openai.com/codex"
DEFAULT_OUTPUT_DIR = "codex_docs"
DEFAULT_USER_AGENT = "codex-docs-mirror/1.0 (+https://developers.openai.com/codex)"

ASSET_EXTENSIONS = {
    ".avif",
    ".bmp",
    ".css",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".mjs",
    ".mp3",
    ".mp4",
    ".ogg",
    ".otf",
    ".pdf",
    ".png",
    ".svg",
    ".ttf",
    ".txt",
    ".webm",
    ".webp",
    ".woff",
    ".woff2",
    ".xml",
}

MARKDOWN_EXTENSIONS = {".md", ".mdx", ".markdown"}
PAGE_LIKE_EXTENSIONS = {"", ".html", ".htm", *MARKDOWN_EXTENSIONS}

CSS_URL_RE = re.compile(
    r"""url\(\s*(?P<quote>['"]?)(?P<url>.*?)(?P=quote)\s*\)""",
    re.IGNORECASE | re.DOTALL,
)
CSS_IMPORT_RE = re.compile(
    r"""@import\s+(?:url\(\s*)?(?P<quote>['"])(?P<url>.*?)(?P=quote)""",
    re.IGNORECASE | re.DOTALL,
)
MARKDOWN_LINK_RE = re.compile(r"""!?\[[^\]]*]\((?P<url>[^)\s]+)(?:\s+"[^"]*")?\)""")
RAW_URL_RE = re.compile(r"""https?://[^\s<>"')]+""", re.IGNORECASE)


@dataclasses.dataclass(frozen=True)
class WorkItem:
    url: str
    kind: str  # "page", "asset", "sitemap"


class LinkExtractor(html.parser.HTMLParser):
    """Extract page and asset candidates from HTML."""

    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.page_candidates: list[str] = []
        self.asset_candidates: list[str] = []
        self._in_style = False
        self._style_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_dict = {name.lower(): value for name, value in attrs if value}

        if tag == "style":
            self._in_style = True

        if tag == "a" and attrs_dict.get("href"):
            self.page_candidates.append(attrs_dict["href"])

        for attr_name in ("src", "poster"):
            value = attrs_dict.get(attr_name)
            if value:
                self.asset_candidates.append(value)

        if tag in {"link", "iframe", "embed", "object", "track"}:
            value = attrs_dict.get("href") or attrs_dict.get("src") or attrs_dict.get("data")
            if value:
                self.asset_candidates.append(value)

        if tag == "meta":
            content = attrs_dict.get("content")
            if content and looks_like_url(content):
                self.asset_candidates.append(content)

        for attr_name in ("srcset", "imagesrcset"):
            value = attrs_dict.get(attr_name)
            if value:
                self.asset_candidates.extend(parse_srcset(value))

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style":
            self._in_style = False

    def handle_data(self, data: str) -> None:
        if self._in_style:
            self._style_chunks.append(data)

    def extracted_style_urls(self) -> list[str]:
        return extract_css_urls("\n".join(self._style_chunks))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively mirror https://developers.openai.com/codex into codex_docs.",
    )
    parser.add_argument("--start-url", default=DEFAULT_START_URL, help="URL to start crawling.")
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to write downloaded files into.",
    )
    parser.add_argument(
        "--page-prefix",
        default="/codex",
        help="Only crawl pages at this URL path prefix.",
    )
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent header.")
    parser.add_argument("--delay", type=float, default=0.2, help="Delay between requests in seconds.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds.")
    parser.add_argument("--max-pages", type=int, default=0, help="Limit crawled pages; 0 means unlimited.")
    parser.add_argument("--max-files", type=int, default=0, help="Limit total fetched files; 0 means unlimited.")
    parser.add_argument("--no-assets", action="store_true", help="Do not download page assets.")
    parser.add_argument("--include-query-pages", action="store_true", help="Also crawl page URLs with query strings.")
    parser.add_argument("--use-sitemap", action="store_true", help="Also seed /codex pages from sitemap XML.")
    parser.add_argument("--sitemap-only", action="store_true", help="Download only pages listed in sitemap XML.")
    parser.add_argument("--ignore-robots", action="store_true", help="Skip robots.txt checks.")
    parser.add_argument("--resume", action="store_true", help="Reuse existing files and continue missing downloads.")
    parser.add_argument(
        "--assets-from-local",
        action="store_true",
        help="Scan downloaded HTML/CSS and download missing same-origin assets.",
    )
    parser.add_argument("--asset-workers", type=int, default=1, help="Parallel workers for --assets-from-local.")
    parser.add_argument("--dry-run", action="store_true", help="Discover URLs without writing files.")
    parser.add_argument("--verbose", action="store_true", help="Print skipped URLs and details.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    start_url = normalize_url(args.start_url)
    start_parts = urllib.parse.urlparse(start_url)
    if start_parts.scheme not in {"http", "https"} or not start_parts.netloc:
        print(f"Invalid start URL: {args.start_url}", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir)
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    robot = None if args.ignore_robots else build_robot_parser(start_url, args)
    if args.assets_from_local:
        downloader = LocalAssetDownloader(args, start_url, output_dir, robot)
        downloader.run()
        downloader.print_summary()
        return 0 if not downloader.failures else 1

    crawler = Crawler(args, start_url, output_dir, robot)
    crawler.run()
    crawler.print_summary()
    return 0 if not crawler.failures else 1


class LocalAssetDownloader:
    def __init__(
        self,
        args: argparse.Namespace,
        start_url: str,
        output_dir: Path,
        robot: urllib.robotparser.RobotFileParser | None,
    ) -> None:
        self.args = args
        self.start_url = start_url
        self.output_dir = output_dir
        self.robot = robot
        self.start_parts = urllib.parse.urlparse(start_url)
        self.allowed_netloc = self.start_parts.netloc.lower()
        self.queue: collections.deque[str] = collections.deque()
        self.seen: set[str] = set()
        self.downloaded = 0
        self.skipped_existing = 0
        self.failures: list[tuple[str, str]] = []

    def run(self) -> None:
        self.seed_from_local_files()

        if self.args.asset_workers > 1:
            self.run_parallel()
            return

        while self.queue:
            if self.args.max_files and self.downloaded >= self.args.max_files:
                print(f"Reached --max-files={self.args.max_files}; stopping.", flush=True)
                break

            url = self.queue.popleft()
            local_path = local_path_for_url(self.output_dir, url, "")
            if local_path.exists() and local_path.is_file() and local_path.stat().st_size > 0:
                self.skipped_existing += 1
                if local_path.suffix.lower() == ".css":
                    self.seed_css_file(local_path, url)
                continue

            if not self.can_fetch(url):
                self.debug(f"robots.txt disallows: {url}")
                continue

            try:
                response = fetch_url(url, self.args)
            except Exception as exc:  # noqa: BLE001
                self.failures.append((url, str(exc)))
                print(f"[ERR] {url}: {exc}", flush=True)
                continue

            final_url = normalize_url(response.url)
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            save_path = local_path_for_url(self.output_dir, final_url, content_type)
            if not self.args.dry_run:
                save_path.parent.mkdir(parents=True, exist_ok=True)
                save_path.write_bytes(response.body)
            self.downloaded += 1
            print(f"[OK] {url} -> {save_path}", flush=True)

            if content_type == "text/css" or save_path.suffix.lower() == ".css":
                self.seed_css_text(response.body, final_url, content_type)

            if self.args.delay > 0:
                time.sleep(self.args.delay)

    def run_parallel(self) -> None:
        candidates: list[str] = []
        while self.queue:
            url = self.queue.popleft()
            local_path = local_path_for_url(self.output_dir, url, "")
            if local_path.exists() and local_path.is_file() and local_path.stat().st_size > 0:
                self.skipped_existing += 1
                continue
            if not self.can_fetch(url):
                self.debug(f"robots.txt disallows: {url}")
                continue
            candidates.append(url)
            if self.args.max_files and len(candidates) >= self.args.max_files:
                break

        if self.args.dry_run:
            for url in candidates:
                print(f"[DRY] {url} -> {local_path_for_url(self.output_dir, url, '')}", flush=True)
            self.downloaded = len(candidates)
            return

        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, self.args.asset_workers)) as executor:
            future_to_url = {executor.submit(self.download_one, url): url for url in candidates}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    ok, path_or_error = future.result()
                except Exception as exc:  # noqa: BLE001
                    ok, path_or_error = False, str(exc)

                if ok:
                    self.downloaded += 1
                    print(f"[OK] {url} -> {path_or_error}", flush=True)
                else:
                    self.failures.append((url, path_or_error))
                    print(f"[ERR] {url}: {path_or_error}", flush=True)

    def download_one(self, url: str) -> tuple[bool, str]:
        try:
            response = fetch_url(url, self.args)
            final_url = normalize_url(response.url)
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            save_path = local_path_for_url(self.output_dir, final_url, content_type)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(response.body)
            return True, str(save_path)
        except Exception as exc:  # noqa: BLE001
            return False, str(exc)

    def seed_from_local_files(self) -> None:
        if not self.output_dir.exists():
            return
        for path in self.output_dir.rglob("*"):
            if not path.is_file():
                continue
            suffix = path.suffix.lower()
            if suffix in {".html", ".htm"}:
                self.seed_html_file(path)
            elif suffix == ".css":
                self.seed_css_file(path, local_url_for_path(self.output_dir, path, self.start_parts))

    def seed_html_file(self, path: Path) -> None:
        base_url = local_url_for_path(self.output_dir, path, self.start_parts)
        text = path.read_text(encoding="utf-8", errors="replace")
        extractor = LinkExtractor(base_url)
        extractor.feed(text)
        for href in [*extractor.asset_candidates, *extractor.extracted_style_urls()]:
            self.enqueue_asset(base_url, href)

    def seed_css_file(self, path: Path, base_url: str) -> None:
        text = path.read_text(encoding="utf-8", errors="replace")
        for href in extract_css_urls(text):
            self.enqueue_asset(base_url, href)

    def seed_css_text(self, body: bytes, base_url: str, content_type: str) -> None:
        text = decode_text(body, content_type)
        for href in extract_css_urls(text):
            self.enqueue_asset(base_url, href)

    def enqueue_asset(self, base_url: str, href: str) -> None:
        target = absolutize_url(base_url, href)
        if not target:
            return
        if not self.is_same_origin(target):
            self.debug(f"skip external asset: {target}")
            return
        if self.is_page_url(target):
            return
        if target in self.seen:
            return
        self.seen.add(target)
        self.queue.append(target)

    def is_same_origin(self, url: str) -> bool:
        parts = urllib.parse.urlparse(url)
        return parts.scheme in {"http", "https"} and parts.netloc.lower() == self.allowed_netloc

    def is_page_url(self, url: str) -> bool:
        parts = urllib.parse.urlparse(url)
        if parts.query:
            return False
        path = parts.path.rstrip("/") or "/"
        suffix = Path(path).suffix.lower()
        return (
            path == normalize_prefix(self.args.page_prefix)
            or path.startswith(normalize_prefix(self.args.page_prefix) + "/")
        ) and (suffix in PAGE_LIKE_EXTENSIONS or suffix not in ASSET_EXTENSIONS)

    def can_fetch(self, url: str) -> bool:
        if self.robot is None:
            return True
        return self.robot.can_fetch(self.args.user_agent, url)

    def print_summary(self) -> None:
        print()
        print("Summary")
        print(f"  Asset refs seen:  {len(self.seen)}")
        print(f"  Existing assets:  {self.skipped_existing}")
        print(f"  Assets fetched:   {self.downloaded}")
        print(f"  Failures:         {len(self.failures)}")
        if self.failures:
            print()
            print("Failures")
            for url, error in self.failures[:20]:
                print(f"  - {url}: {error}")
            if len(self.failures) > 20:
                print(f"  ... {len(self.failures) - 20} more")

    def debug(self, message: str) -> None:
        if self.args.verbose:
            print(f"[SKIP] {message}", flush=True)


class Crawler:
    def __init__(
        self,
        args: argparse.Namespace,
        start_url: str,
        output_dir: Path,
        robot: urllib.robotparser.RobotFileParser | None,
    ) -> None:
        self.args = args
        self.start_url = start_url
        self.output_dir = output_dir
        self.robot = robot
        self.start_parts = urllib.parse.urlparse(start_url)
        self.allowed_netloc = self.start_parts.netloc.lower()
        self.page_prefix = normalize_prefix(args.page_prefix)
        self.queue: collections.deque[WorkItem] = collections.deque()
        self.seen: set[str] = set()
        self.fetched: set[str] = set()
        self.pages_fetched = 0
        self.assets_fetched = 0
        self.sitemaps_fetched = 0
        self.failures: list[tuple[str, str]] = []

    def run(self) -> None:
        if not self.args.sitemap_only:
            self.enqueue(WorkItem(self.start_url, "page"))

        if self.args.use_sitemap or self.args.sitemap_only:
            for sitemap_url in self.initial_sitemap_urls():
                self.enqueue(WorkItem(sitemap_url, "sitemap"))

        while self.queue:
            if self.args.max_files and len(self.fetched) >= self.args.max_files:
                print(f"Reached --max-files={self.args.max_files}; stopping.", flush=True)
                break

            item = self.queue.popleft()
            if item.url in self.fetched:
                continue

            if item.kind == "page" and self.args.max_pages and self.pages_fetched >= self.args.max_pages:
                continue

            if self.resume_existing(item):
                continue

            if not self.can_fetch(item.url):
                self.debug(f"robots.txt disallows: {item.url}")
                continue

            try:
                response = fetch_url(item.url, self.args)
            except Exception as exc:  # noqa: BLE001
                self.failures.append((item.url, str(exc)))
                print(f"[ERR] {item.url}: {exc}", flush=True)
                continue

            self.fetched.add(item.url)
            final_url = normalize_url(response.url)
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()

            if item.kind == "sitemap":
                self.sitemaps_fetched += 1
                self.handle_sitemap(final_url, response.body)
            else:
                if item.kind == "page":
                    self.pages_fetched += 1
                else:
                    self.assets_fetched += 1
                self.save_response(final_url, response.body, content_type)
                self.discover(final_url, response.body, content_type, item.kind)

            if self.args.delay > 0:
                time.sleep(self.args.delay)

    def resume_existing(self, item: WorkItem) -> bool:
        if not self.args.resume or self.args.dry_run or item.kind == "sitemap":
            return False

        assumed_content_type = assumed_content_type_for_item(item)
        local_path = local_path_for_url(self.output_dir, item.url, assumed_content_type)
        if not local_path.exists():
            return False

        body = local_path.read_bytes()
        self.fetched.add(item.url)
        if item.kind == "page":
            self.pages_fetched += 1
        else:
            self.assets_fetched += 1

        print(f"[SKIP] existing {item.url} -> {local_path}", flush=True)
        if not self.args.no_assets and not self.args.sitemap_only:
            self.discover(item.url, body, content_type_for_path(local_path), item.kind)
        return True

    def enqueue(self, item: WorkItem) -> None:
        normalized = normalize_url(item.url)
        if normalized in self.seen:
            return

        if item.kind == "page" and not self.is_allowed_page(normalized):
            self.debug(f"skip page outside prefix: {normalized}")
            return

        if item.kind in {"asset", "sitemap"} and not self.is_same_origin(normalized):
            self.debug(f"skip external {item.kind}: {normalized}")
            return

        self.seen.add(normalized)
        self.queue.append(WorkItem(normalized, item.kind))

    def discover(self, base_url: str, body: bytes, content_type: str, item_kind: str) -> None:
        if content_type in {"text/html", "application/xhtml+xml"}:
            text = decode_text(body, content_type)
            extractor = LinkExtractor(base_url)
            extractor.feed(text)

            if not self.args.sitemap_only:
                for href in extractor.page_candidates:
                    target = absolutize_url(base_url, href)
                    if target and self.is_allowed_page(target):
                        self.enqueue(WorkItem(target, "page"))

            if not self.args.no_assets:
                for href in [*extractor.asset_candidates, *extractor.extracted_style_urls()]:
                    self.enqueue_asset_candidate(base_url, href)

        elif content_type in {"text/css"} or url_path_suffix(base_url) == ".css":
            if not self.args.no_assets:
                text = decode_text(body, content_type)
                for href in extract_css_urls(text):
                    self.enqueue_asset_candidate(base_url, href)

        elif content_type in {"text/markdown", "text/plain"} or url_path_suffix(base_url) in MARKDOWN_EXTENSIONS:
            text = decode_text(body, content_type)
            for href in extract_markdown_urls(text):
                target = absolutize_url(base_url, href)
                if not target:
                    continue
                if self.is_allowed_page(target):
                    self.enqueue(WorkItem(target, "page"))
                elif not self.args.no_assets:
                    self.enqueue_asset_candidate(base_url, href)

    def enqueue_asset_candidate(self, base_url: str, href: str) -> None:
        target = absolutize_url(base_url, href)
        if not target:
            return
        if self.is_allowed_page(target):
            return
        if self.is_same_origin(target):
            self.enqueue(WorkItem(target, "asset"))
        else:
            self.debug(f"skip external asset: {target}")

    def handle_sitemap(self, sitemap_url: str, body: bytes) -> None:
        try:
            root = ET.fromstring(body)
        except ET.ParseError as exc:
            self.failures.append((sitemap_url, f"invalid sitemap XML: {exc}"))
            print(f"[ERR] {sitemap_url}: invalid sitemap XML: {exc}", flush=True)
            return

        for loc in root.findall(".//{*}loc"):
            if not loc.text:
                continue
            target = normalize_url(loc.text.strip())
            path_suffix = url_path_suffix(target)
            if target.endswith(".xml") or path_suffix == ".xml":
                self.enqueue(WorkItem(target, "sitemap"))
            elif self.is_allowed_page(target):
                self.enqueue(WorkItem(target, "page"))

    def initial_sitemap_urls(self) -> Iterable[str]:
        robots_url = urllib.parse.urlunparse(
            (self.start_parts.scheme, self.start_parts.netloc, "/robots.txt", "", "", "")
        )
        try:
            response = fetch_url(robots_url, self.args)
        except Exception:
            yield urllib.parse.urljoin(self.start_url, "/sitemap-index.xml")
            return

        text = decode_text(response.body, "text/plain")
        found = False
        for line in text.splitlines():
            if line.lower().startswith("sitemap:"):
                found = True
                yield normalize_url(urllib.parse.urljoin(robots_url, line.split(":", 1)[1].strip()))
        if not found:
            yield urllib.parse.urljoin(self.start_url, "/sitemap-index.xml")

    def save_response(self, url: str, body: bytes, content_type: str) -> None:
        local_path = local_path_for_url(self.output_dir, url, content_type)
        if self.args.dry_run:
            print(f"[DRY] {url} -> {local_path}", flush=True)
            return

        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(body)
        print(f"[OK] {url} -> {local_path}", flush=True)

    def is_same_origin(self, url: str) -> bool:
        parts = urllib.parse.urlparse(url)
        return parts.scheme in {"http", "https"} and parts.netloc.lower() == self.allowed_netloc

    def is_allowed_page(self, url: str) -> bool:
        if not self.is_same_origin(url):
            return False
        if urllib.parse.urlparse(url).query and not self.args.include_query_pages:
            return False
        path = urllib.parse.urlparse(url).path.rstrip("/") or "/"
        if path != self.page_prefix and not path.startswith(self.page_prefix + "/"):
            return False
        suffix = url_path_suffix(url)
        return suffix in PAGE_LIKE_EXTENSIONS or suffix not in ASSET_EXTENSIONS

    def can_fetch(self, url: str) -> bool:
        if self.robot is None:
            return True
        return self.robot.can_fetch(self.args.user_agent, url)

    def print_summary(self) -> None:
        print()
        print("Summary")
        print(f"  Pages fetched:   {self.pages_fetched}")
        print(f"  Assets fetched:  {self.assets_fetched}")
        print(f"  Sitemaps read:   {self.sitemaps_fetched}")
        print(f"  Unique queued:   {len(self.seen)}")
        print(f"  Failures:        {len(self.failures)}")
        if self.failures:
            print()
            print("Failures")
            for url, error in self.failures[:20]:
                print(f"  - {url}: {error}")
            if len(self.failures) > 20:
                print(f"  ... {len(self.failures) - 20} more")

    def debug(self, message: str) -> None:
        if self.args.verbose:
            print(f"[SKIP] {message}", flush=True)


@dataclasses.dataclass(frozen=True)
class FetchResponse:
    url: str
    headers: urllib.request.addinfourl.headers
    body: bytes


def fetch_url(url: str, args: argparse.Namespace) -> FetchResponse:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": args.user_agent,
            "Accept": "*/*",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(request, timeout=args.timeout) as response:
        return FetchResponse(
            url=response.geturl(),
            headers=response.headers,
            body=response.read(),
        )


def build_robot_parser(
    start_url: str,
    args: argparse.Namespace,
) -> urllib.robotparser.RobotFileParser | None:
    parts = urllib.parse.urlparse(start_url)
    robots_url = urllib.parse.urlunparse((parts.scheme, parts.netloc, "/robots.txt", "", "", ""))
    parser = urllib.robotparser.RobotFileParser(robots_url)
    parser.set_url(robots_url)
    try:
        parser.read()
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: could not read robots.txt ({exc}); continuing.", file=sys.stderr)
        return None
    return parser


def normalize_prefix(prefix: str) -> str:
    if not prefix.startswith("/"):
        prefix = "/" + prefix
    return prefix.rstrip("/") or "/"


def normalize_url(url: str) -> str:
    parts = urllib.parse.urlparse(url.strip())
    path = parts.path or "/"
    path = posixpath.normpath(path)
    if not path.startswith("/"):
        path = "/" + path
    if parts.path.endswith("/") and not path.endswith("/"):
        path += "/"
    return urllib.parse.urlunparse(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            path,
            "",
            parts.query,
            "",
        )
    )


def absolutize_url(base_url: str, href: str) -> str | None:
    href = href.strip()
    if not href or href.startswith("#"):
        return None
    scheme = urllib.parse.urlparse(href).scheme.lower()
    if scheme in {"mailto", "tel", "javascript", "data", "blob"}:
        return None
    return normalize_url(urllib.parse.urljoin(base_url, href))


def local_path_for_url(output_dir: Path, url: str, content_type: str) -> Path:
    parts = urllib.parse.urlparse(url)
    raw_path = urllib.parse.unquote(parts.path or "/")
    normalized = posixpath.normpath(raw_path)
    if normalized in {"", "."}:
        normalized = "/"
    if normalized.startswith("../") or "/../" in normalized:
        raise ValueError(f"unsafe URL path: {url}")

    relative = normalized.lstrip("/")
    if not relative:
        relative = "index.html"

    path = Path(*[sanitize_path_segment(segment) for segment in relative.split("/") if segment])
    suffix = path.suffix.lower()

    if raw_path.endswith("/"):
        path = path / "index.html"
    elif content_type in {"text/html", "application/xhtml+xml"} and suffix not in {".html", ".htm"}:
        path = path / "index.html"
    elif not suffix:
        guessed = extension_for_content_type(content_type)
        if guessed:
            path = path.with_name(path.name + guessed)

    if parts.query:
        digest = hashlib.sha1(parts.query.encode("utf-8")).hexdigest()[:10]
        path = path.with_name(f"{path.stem}__q_{digest}{path.suffix}")

    full_path = (output_dir / path).resolve()
    output_root = output_dir.resolve()
    if output_root != full_path and output_root not in full_path.parents:
        raise ValueError(f"resolved path escaped output directory: {url}")
    return full_path


def local_url_for_path(output_dir: Path, path: Path, start_parts: urllib.parse.ParseResult) -> str:
    relative = path.relative_to(output_dir).as_posix()
    if relative.endswith("/index.html"):
        url_path = "/" + relative[: -len("/index.html")]
    else:
        url_path = "/" + relative
    if url_path == "/":
        url_path = "/index.html"
    return urllib.parse.urlunparse((start_parts.scheme, start_parts.netloc, url_path, "", "", ""))


def sanitize_path_segment(segment: str) -> str:
    cleaned = re.sub(r"""[<>:"\\|?*\x00-\x1f]""", "_", segment)
    cleaned = cleaned.rstrip(" .")
    return cleaned or "_"


def extension_for_content_type(content_type: str) -> str:
    if content_type == "text/html":
        return ".html"
    if content_type == "text/css":
        return ".css"
    if content_type in {"application/javascript", "text/javascript"}:
        return ".js"
    guessed = mimetypes.guess_extension(content_type or "")
    return guessed or ""


def assumed_content_type_for_item(item: WorkItem) -> str:
    suffix = url_path_suffix(item.url)
    if item.kind == "page":
        if suffix in MARKDOWN_EXTENSIONS:
            return "text/markdown"
        return "text/html"
    return mimetypes.types_map.get(suffix, "")


def content_type_for_path(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".html", ".htm"}:
        return "text/html"
    if suffix == ".css":
        return "text/css"
    if suffix in MARKDOWN_EXTENSIONS:
        return "text/markdown"
    return mimetypes.types_map.get(suffix, "")


def decode_text(body: bytes, content_type: str) -> str:
    match = re.search(r"charset=([-\w.]+)", content_type, re.IGNORECASE)
    encoding = match.group(1) if match else "utf-8"
    try:
        return body.decode(encoding, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def parse_srcset(value: str) -> list[str]:
    urls = []
    for candidate in value.split(","):
        candidate = candidate.strip()
        if not candidate:
            continue
        urls.append(candidate.split()[0])
    return urls


def extract_css_urls(text: str) -> list[str]:
    urls = [match.group("url").strip() for match in CSS_URL_RE.finditer(text)]
    urls.extend(match.group("url").strip() for match in CSS_IMPORT_RE.finditer(text))
    return [url for url in urls if url and not url.startswith("#")]


def extract_markdown_urls(text: str) -> list[str]:
    urls = [match.group("url").strip("<>") for match in MARKDOWN_LINK_RE.finditer(text)]
    urls.extend(match.group(0) for match in RAW_URL_RE.finditer(text))
    return urls


def looks_like_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return bool(parsed.scheme in {"http", "https"} and parsed.netloc) or value.startswith("/")


def url_path_suffix(url: str) -> str:
    return Path(urllib.parse.urlparse(url).path).suffix.lower()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
