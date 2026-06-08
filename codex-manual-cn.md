---
title: "Codex 手册"
hidden: true
---

## 按主题查找

- `pricing`, `plans`, `ChatGPT`, `API key`, `Plus`, `Pro`, `Business`, `Enterprise`, `Edu`, `feature maturity`: [界面与模式](#surfaces-and-modes)
- `prompting`, `threads`, `context window`, `multi_agent`, `spawn_agents_on_csv`, `/plan`, `workflow`: [执行模型与工作流](#execution-model-and-workflows)
- `approval_policy`, `sandbox_mode`, `read-only`, `workspace-write`, `danger-full-access`, `security`, `cyber`: [审批、沙箱和安全](#approvals-sandboxing-and-security)
- `config.toml`, `.codex/config.toml`, `auth.json`, `ChatGPT sign-in`, `API key login`, `models`, `providers`, `model_reasoning_effort`: [配置、身份验证与模型](#configuration-auth-and-models)
- `codex exec`, `codex cloud`, `codex mcp`, `worktrees`, `automations`, `cloud environments`, `internet access`: [CLI、IDE、应用与云行为](#surface-behavior)
- `AGENTS.md`, `skills`, `rules`, `custom prompts`, `MCP`, `GitHub integration`, `Slack integration`: [定制、技能、规则、MCP 与集成](#customization-and-tooling)
- `sdk`, `noninteractive`, `app-server`, `github-action`, `CI`, `auth in CI`: [无交互和程序化接口](#automation-and-programmatic-interfaces)
- `Windows`, `WSL`, `enterprise`, `RBAC`, `data residency`, `OSS`: [平台、企业与注意事项](#platform-enterprise-and-caveats)

## 界面与模式

<a id="surfaces-and-modes"></a>

入口点、计划、支持的界面、成熟度，以及高层产品定位。

### Codex

来源：[Codex](/codex/overview.md)

Codex 是 OpenAI 面向软件开发的编码代理。ChatGPT Plus、Pro、Business、Edu 和 Enterprise 计划都包含 Codex。它可以帮助你：

- **编写代码**：描述你想要构建的内容，Codex 会生成与意图匹配的代码，并适应现有项目结构和约定。
- **理解不熟悉的代码库**：Codex 可以阅读并解释复杂或遗留代码，帮助你掌握团队如何组织系统。
- **审查代码**：Codex 分析代码以识别潜在错误、逻辑缺陷和未处理的边界情况。
- **调试和修复问题**：出现故障时，Codex 帮助追踪失败、诊断根因并建议有针对性的修复。
- **自动化开发任务**：Codex 可以运行重复性工作流，如重构、测试、迁移和设置任务，让你专注于更高层次的工程工作。

### Codex 定价

来源：[Codex Pricing](/codex/pricing.md)

定价选项

**免费**（$0 /月）：

探索 Codex 在快速编码任务中的能力。

[获取免费版](https://chatgpt.com/plans/free/)

**Go**（$8 /月）：

将 Codex 用于轻量编码任务。

[获取 Go](https://chatgpt.com/plans/go)

**Plus**（$20 /月）：

支持每周几次的重点编码会话。

- 在网页、CLI、IDE 扩展和 iOS 上使用 Codex
- 云端集成，如自动代码审查和 Slack 集成
- 最新模型，包括 GPT-5.5、GPT-5.4 和 GPT-5.3-Codex
- 使用 GPT-5.4-mini 在常规本地消息上获得更高使用限额
- 使用 [ChatGPT 积分](#credits-overview) 灵活扩展使用
- 作为 Plus 计划的一部分，享受其他 [ChatGPT 功能](https://chatgpt.com/pricing)

[获取 Plus](https://chatgpt.com/explore/plus?utm_internal_source=openai_developers_codex)

**Pro**（从 $100 /月起）：

选择比 Plus 高 5 倍或 20 倍的速率限制。

Plus 中的全部内容，以及：

- 访问 GPT-5.3-Codex-Spark（研究预览），这是一个适合日常编码任务的快速 Codex 模型
- 比 Plus 多 5 倍或 20 倍的 Codex 使用量\*
- 作为 Pro 计划的一部分，享受其他 [ChatGPT 功能](https://chatgpt.com/pricing)

[获取 Pro](https://chatgpt.com/explore/pro?utm_internal_source=openai_developers_codex)

[\*了解两个层级的限制。](https://help.openai.com/en/articles/9793128-about-chatgpt-pro-plans)

**API Key**：

非常适合在 CI 等共享环境中自动化。

- 在 CLI、SDK 或 IDE 扩展中使用 Codex
- 无云端功能（GitHub 代码审查、Slack 等）
- 新模型如 GPT-5.3-Codex 和 GPT-5.3-Codex-Spark 的访问可能延迟
- 仅按 Codex 使用的令牌付费，基于 [API 定价](https://platform.openai.com/docs/pricing)

[了解更多](/codex/auth)

**Business**（按用量付费）：

将 Codex 引入你的初创公司或成长型企业。

Plus 中的全部内容，以及：

- 根据团队需求分配标准或基于使用的 Codex 座位。[了解更多](https://help.openai.com/en/articles/8792828-what-is-chatgpt-business)
- 更大的虚拟机以更快运行云任务
- 使用 [ChatGPT 积分](#credits-overview) 灵活扩展使用
- 提供一个安全、独立的工作区，具备基本管理员控制、SAML SSO 和 MFA
- 默认不对你的业务数据进行训练。[了解更多](https://openai.com/business-data/)
- 作为 Business 计划的一部分，享受其他 [ChatGPT 功能](https://chatgpt.com/pricing)

[获取 Business](https://chatgpt.com/codex/team/start)

**Enterprise 与 Edu**：

为整个组织解锁 Codex 的企业级功能。

Business 中的全部内容，以及：

- 优先请求处理
- 企业级安全与控制，包括 SCIM、EKM、用户分析、域验证和基于角色的访问控制（[RBAC](https://help.openai.com/en/articles/11750701-rbac)）
- 通过 [合规 API](https://chatgpt.com/admin/api-reference#tag/Codex-Tasks) 的审计日志和使用监控
- 数据保留和数据驻留控制
- 作为 Enterprise 计划一部分享受其他 [ChatGPT 功能](https://chatgpt.com/pricing)

[联系销售](https://chatgpt.com/contact-sales?utm_internal_source=openai_developers_codex)

### 功能成熟度

来源：[Feature Maturity](/codex/feature-maturity.md)

某些 Codex 功能会带有成熟度标签，以便你了解每项功能的可靠性、可能发生的变更以及可期望的支持级别。

| 成熟度 | 含义 | 建议 |
| ----------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 开发中 | 尚未准备好使用。 | 不要使用。 |
| 实验性 | 不稳定，OpenAI 可能会移除或更改。 | 自行承担风险使用。 |
| 测试版 | 适合广泛测试；大多数方面已完整，但可能会根据用户反馈发生变化。 | 适合大多数评估和试点；预期会有小变更。 |
| 稳定 | 完全支持、文档完善、适合广泛使用；行为和配置在一段时间内保持一致。 | 可安全用于生产；移除通常会经过弃用流程。 |

### 快速入门

来源：[Quickstart](/codex/quickstart.md)

每个 ChatGPT 计划都包含 Codex。

你也可以通过使用 OpenAI API 密钥登录，使用 API 积分来访问 Codex。

## 执行模型与工作流

<a id="execution-model-and-workflows"></a>

Codex 如何推理工作、线程、提示、速度和多代理协调。

### 最佳实践

来源：[Best practices](/codex/learn/best-practices.md)

如果你是 Codex 或编码代理的新手，本指南会帮助你更快获得更好结果。它涵盖了 Codex 在 [CLI](/codex/cli)、[IDE 扩展](/codex/ide) 和 [Codex 应用](/codex/app) 中从提示和计划到验证、MCP、技能和自动化的核心习惯。

当你把 Codex 当作一个你可以配置并随着时间改进的队友，而不是一次性助手时，它表现最佳。

一种有用的思考方式是：从正确的任务上下文开始，使用 `AGENTS.md` 编写持久性指导，配置 Codex 以匹配你的工作流，使用 MCP 连接外部系统，将重复工作转成技能，并自动化稳定工作流。

#### 首次使用要重视：上下文和提示

即使你的提示不完美，Codex 也已经足够强大，可以有所帮助。你通常可以在最少设置下给它一个困难问题，仍然得到不错的结果。清晰的 [提示](/codex/prompting) 并非获取价值的必要条件，但它确实让结果更可靠，尤其在大型代码库或高风险任务中。

如果你在大型或复杂仓库工作，最重要的突破是提供正确的任务上下文以及一个清晰的结构说明你希望完成什么。

一个好的默认提示应包含四件事：

- **目标**：你想改变或构建什么？
- **上下文**：哪些文件、文件夹、文档、示例或错误与此任务相关？你可以使用 @ 提及特定文件作为上下文。
- **约束**：Codex 应遵循哪些标准、架构、安全要求或约定？
- **完成条件**：任务完成前应满足什么条件，例如测试通过、行为改变或错误不再复现？

这有助于 Codex 保持范围、减少假设，并生成更易于审查的工作。

根据任务难度选择推理级别，并测试哪种设置最适合你的工作流。不同用户和任务可能适合不同设置。

- 低：适用于更快、范围明确的任务
- 中：适用于更复杂的更改或调试
- 高：用于较长、需要代理式推理的任务

为了更快提供上下文，可以尝试在 Codex 应用中使用语音输入来口述你希望 Codex 做什么，而不是手动输入。

#### 对复杂任务先制定计划

如果任务复杂、模糊或难以描述清楚，让 Codex 在开始编码前先制定计划。

有几种方法效果很好：

**使用计划模式**：对于大多数用户，这是最简单最有效的选项。计划模式让 Codex 在实施前收集上下文、提出澄清问题并构建更稳健的计划。使用 `/plan` 或 Shift+Tab 切换。

**让 Codex 先采访你**：如果你有一个大致想法，但不确定如何描述得好，让 Codex 先向你提问。告诉它挑战你的假设，并将模糊想法变成具体内容后再编写代码。

**使用 PLANS.md 模板**：对于更高级工作流，你可以配置 Codex 按照 `PLANS.md` 或执行计划模板来处理较长的多步骤工作。更多细节请参见[执行计划指南](/cookbook/articles/codex_exec_plans)。

#### 使用 `AGENTS.md` 让指导可复用

一旦某种提示模式有效，下一步就是停止手动重复它。这就是 [AGENTS.md](/codex/guides/agents-md) 的作用。

把 `AGENTS.md` 想象成代理的开放格式 README。它会自动加载到上下文中，是在仓库中编码你和团队希望 Codex 如何工作的最佳位置。

一个好的 `AGENTS.md` 应包括：

- 仓库布局和重要目录
- 如何运行项目
- 构建、测试和 lint 命令
- 工程约定和 PR 期望
- 约束和禁忌规则
- 完成标准以及如何验证工作

CLI 中的 `/init` 斜线命令是快速启动命令，用于在当前目录搭建一个入门 `AGENTS.md`。这是一个很好的起点，但你应该根据团队实际构建、测试、审查和发布代码的方式编辑结果。

你可以在不同层级创建 `AGENTS.md` 文件：位于 `~/.codex` 的全局 `AGENTS.md` 作为个人默认设置，仓库级文件用于共享标准，以及更具体目录中的文件用于本地规则。如果当前目录附近有更具体的文件，则该指导优先。

保持实用。一个简短、准确的 `AGENTS.md` 比一份冗长但模糊的规则更有用。先从基础开始，然后只有在发现重复错误后再添加新规则。

如果 `AGENTS.md` 变得过大，请保持主文件简洁，并引用任务特定的 Markdown 文件，例如规划、代码审查或架构。

当 Codex 连续两次犯同样错误时，要求它做一次回顾并更新 `AGENTS.md`。这样指导就会保持务实，并基于真实摩擦。

#### 配置 Codex 以保持一致性

配置是让 Codex 在不同会话和界面中表现更一致的主要方式。例如，你可以设置模型选择、推理努力、沙箱模式、审批策略、配置文件和 MCP 设置的默认值。

一个好的起始模式是：

- 将个人默认保存在 `~/.codex/config.toml`（Codex 应用 → 设置 → 打开 config.toml）
- 将仓库特定行为保存在 `.codex/config.toml`
- 仅将命令行覆盖用于一次性情况（如果你使用 CLI）

[`config.toml`](/codex/config-basic) 是定义持久偏好（如 MCP 服务器、多代理设置和功能标志）的地方。配置文件特定的覆盖存放在单独的 `$CODEX_HOME/profile-name.config.toml` 文件中。

Codex 附带操作级别的沙箱功能，并且有两个关键控制项：审批模式决定 Codex 在何时请求你许可运行命令；沙箱模式决定 Codex 是否可以读取或写入目录以及代理可以访问哪些文件。

如果你是编码代理新手，请从默认权限开始。默认保持审批和沙箱严格，仅在信任的仓库或特定工作流中，且明确需求时才放宽权限。

注意 CLI、IDE 和 Codex 应用都共享相同的配置层。更多内容请参见 [示例配置](/codex/config-sample) 页面。

尽早为你的真实环境配置 Codex。许多质量问题实际上是设置问题，例如工作目录错误、缺少写权限、模型默认设置错误或缺少工具和连接器。

#### 通过测试和审查提高可靠性

不要仅仅让 Codex 做更改。让它在需要时创建测试、运行相关检查、确认结果，并在你接受之前审查工作。

Codex 可以为你执行这个循环，但前提是它知道“好”的定义。这种指导可以来自提示，也可以来自 `AGENTS.md`。

这可以包括：

- 为更改编写或更新测试
- 运行正确的测试套件
- 检查 lint、格式化或类型检查
- 确认最终行为符合请求
- 审查 diff 以寻找缺陷、回归或风险模式

切换 Codex 应用中的 diff 面板，可直接本地[审查更改](/codex/app/review)。单击特定行以提供反馈，该反馈作为上下文传递给下一次 Codex 运行。

这里一个有用选项是斜线命令 `/review`，它提供几种审查代码的方式：

- 与基线分支进行 PR 风格审查
- 审查未提交更改
- 审查提交
- 使用自定义审查说明

如果你和团队有 `code_review.md` 文件，并在 `AGENTS.md` 中引用它，Codex 也可以在审查过程中遵循该指导。这是让团队审查行为在不同仓库和贡献者间保持一致的强模式。

Codex 不应只是生成代码。在正确指令下，它还可以帮助**测试、检查和审查**代码。

如果你使用 GitHub Cloud，可以设置 Codex 为你的 PR 运行[代码审查](/codex/integrations/github)。在 OpenAI，Codex 会审查 100% 的 PR。你可以启用自动审查，或在你 @Codex 时让它进行被动审查。

### 示例工作流

来源：[Workflows](/codex/workflows.md)

当你把 Codex 当作一个有明确上下文和清晰“完成”定义的队友时，它表现最佳。
此页面提供 Codex IDE 扩展、Codex CLI 和 Codex 云的端到端工作流示例。

如果你是 Codex 新手，先阅读 [提示](/codex/prompting) ，然后再回来查看具体流程。

#### 如何阅读这些示例

每个工作流包括：

- **何时使用** 以及哪个 Codex 界面最适合（IDE、CLI 或云）
- 带示例用户提示的 **步骤**
- **上下文说明**：Codex 自动看到什么，以及你应附加什么
- **验证**：如何检查输出

> **注意：** IDE 扩展会自动将你的打开文件作为上下文包含进来。在 CLI 中，你通常需要显式提及路径（或使用 `/mention` 和 `@` 路径自动完成附加文件）。

---

#### 解释代码库

当你正在入职、继承服务，或尝试推理协议、数据模型或请求流程时使用此方法。

#### 方案：在 IDE 中解释代码库

1. 打开最相关的文件。
2. 选择你关心的代码（可选但推荐）。
3. 提示 Codex：

   ```text
   Explain how the request flows through the selected code.

   Include:
   - a short summary of the responsibilities of each module involved
   - what data is validated and where
   - one or two "gotchas" to watch for when changing this
   ```

验证：

- 让它提供一个你可以快速验证的图表或检查清单：

```text
Summarize the request flow as a numbered list of steps. Then list the files involved.
```

#### 方案：在 CLI 中解释代码库

1. 启动交互会话：

   ```bash
   codex
   ```

2. 附加文件（可选），并提示：

   ```text
   I need to understand the protocol used by this service. Read @foo.ts @schema.ts and explain the schema and request/response flow. Focus on required vs optional fields and backward compatibility rules.
   ```

上下文说明：

- 你可以在撰写器中使用 `@` 插入工作区文件路径，或使用 `/mention` 附加特定文件。

---

#### 修复 bug

当你有可在本地复现的失败行为时使用此方法。

#### 方案：在 CLI 中修复 bug

1. 在仓库根目录启动 Codex：

   ```bash
   codex
   ```

2. 给 Codex 一个复现方案，以及你怀疑的文件：

   ```text
   Bug: Clicking "Save" on the settings screen sometimes shows "Saved" but doesn't persist the change.

   Repro:
   1) Start the app: npm run dev
   2) Go to /settings
   3) Toggle "Enable alerts"
   4) Click Save
   5) Refresh the page: the toggle resets

   Constraints:
   - Do not change the API shape.
   - Keep the fix minimal and add a regression test if feasible.

   Start by reproducing the bug locally, then propose a patch and run checks.
   ```

上下文说明：

- 由你提供：复现步骤和约束（这些比高层描述更重要）。
- 由 Codex 提供：命令输出、发现的调用点以及它触发的任何堆栈跟踪。

验证：

- 修复后，运行 lint 和最小相关测试套件。报告命令和结果。

#### 方案：在 IDE 中修复 bug

1. 打开你认为 bug 所在的文件，以及最近的调用方文件。
2. 提示 Codex：

   ```text
   Find the bug causing "Saved" to show without persisting changes. After proposing the fix, tell me how to verify it in the UI.
   ```

---

#### 编写测试

当你想非常明确地指定测试范围时使用此方法。

#### 方案：在 IDE 中编写测试

1. 打开包含函数的文件。
2. 选择定义该函数的行。使用命令面板中的“Add to Codex Thread”将这些行添加到上下文。
3. 提示 Codex：

   ```text
   Write a unit test for this function. Follow conventions used in other tests.
   ```

上下文说明：

- 由“Add to Codex Thread”命令提供：所选代码行（这是“行号”范围），以及打开的文件。

#### 方案：在 CLI 中编写测试

1. 启动 Codex：

   ```bash
   codex
   ```

2. 通过函数名提示：

   ```text
   Add a test for the invert_list function in @transform.ts. Cover the happy path plus edge cases.
   ```

---

#### 从截图原型化

当你有设计稿、截图或 UI 参考，并想快速生成可工作的原型时使用此方法。

### 提示

来源：[Prompting](/codex/prompting.md)

#### 提示语

你通过发送描述你希望它做什么的提示（用户消息）与 Codex 交互。

示例提示：

```text
Explain how the transform module works and how other modules use it.
```

```text
Add a new command-line option `--json` that outputs JSON.
```

提交提示后，Codex 以循环方式工作：它调用模型，然后执行模型输出中指示的操作，例如读取文件、编辑文件和调用工具。当任务完成或你取消时，此过程结束。

与 ChatGPT 一样，Codex 的效果取决于你给出的指令。以下是我们发现对提示 Codex 有帮助的一些建议：

- 如果 Codex 能验证自己的工作，它会产生更高质量的输出。包括重现问题、验证功能以及运行 lint 和 pre-commit 检查的步骤。
- 当你把复杂工作拆分成更小、更集中的步骤时，Codex 的处理效果更好。较小的任务更易于 Codex 测试，也更易于你审查。如果你不确定如何拆分任务，让 Codex 提出计划。

有关提示 Codex 的更多想法，请参考 [工作流](/codex/workflows)。

#### 线程模型

线程是一个会话：你的提示以及随后的模型输出和工具调用。线程可以包含多个提示。例如，你的第一个提示可能要求 Codex 实现一个功能，后续提示可能要求它添加测试。

当 Codex 正在积极处理线程时，该线程称为“运行中”。你可以同时运行多个线程，但应避免让两个线程修改相同文件。你也可以稍后通过继续发送提示来恢复线程。

线程可以在本地或云端运行：

- **本地线程** 在你的机器上运行。Codex 可以读取和编辑你的文件并运行命令，因此你可以看到更改并使用现有工具。为了减少对工作区外部不想要更改的风险，本地线程在[沙箱](/codex/agent-approvals-security)中运行。
- **云线程** 在隔离的[环境](/codex/cloud/environments)中运行。Codex 克隆你的仓库并检出它正在处理的分支。当你希望并行运行工作或从另一台设备委派任务时，云线程很有用。要在你的仓库上使用云线程，请先将代码推送到 GitHub。你也可以[从本地机器委派任务](/codex/ide/cloud-tasks)，这包括你当前的工作状态。

在 Codex 应用中，你还可以启动一个不选择项目的聊天。聊天不与已保存的仓库或项目文件夹绑定。将其用于研究、规划、连接工具工作流或其他不希望 Codex 从代码库开始的工作。聊天使用 Codex 管理的 `threads` 目录作为其工作位置。默认情况下，该位置为 `~/.codex/threads`。要更改此状态的基本位置，请设置 `CODEX_HOME`；参见 [配置和状态位置](/codex/config-advanced#config-and-state-locations)。

#### 上下文

提交提示时，请包括 Codex 可以使用的上下文，例如相关文件和图像的引用。Codex IDE 扩展会自动将打开文件列表和所选文本范围作为上下文包含进来。

随着代理工作的进行，它还会从文件内容、工具输出以及它已完成和仍需完成的事项的持续记录中收集上下文。

线程中的所有信息必须适应模型的**上下文窗口**，该窗口因模型而异。Codex 会监视并报告剩余空间。对于较长任务，Codex 可能会自动通过总结相关信息并丢弃不太相关的细节来**压缩**上下文。通过反复压缩，Codex 可以在多个步骤中继续处理复杂任务。

#### 目标模式

目标模式为 Codex 提供一个持久目标，以便在较长任务中持续推进。若工作可能需要多步，或 Codex 需要一个它可以不断检查的清晰完成标准时，请使用它。

设置目标后，目标文本既作为起始提示，也作为完成标准。Codex 使用它来决定下一步做什么以及任务是否完成。在 [Codex 应用](/codex/app/commands#set-or-manage-a-goal-with-goal)、[IDE 扩展](/codex/ide/slash-commands) 或 [CLI](/codex/cli/slash-commands#set-or-view-a-task-goal-with-goal) 中使用 `/goal` 启动目标模式。

如果斜线命令列表中没有 `/goal`，请在 `config.toml` 中启用 `features.goals`：

```toml
[features]
goals = true
```

你也可以从 CLI 运行 `codex features enable goals` 或让 Codex 运行该命令。
在 Codex 应用中，进度显示在撰写器上方，并带有暂停、恢复、编辑或清除目标的控件。

编写目标时要让 Codex 能判断它是否成功。好的目标应包含具体结果、可衡量目标或测试标准。例如：

```text
Migrate this codebase from JavaScript to TypeScript. The app should compile in
strict mode without explicit `any` type definitions.
```

```text
Reduce the time to interactive of the home page to below 1 second.
```

如果目标难以事先定义，请从 `/plan` 开始，要求 Codex 在实施前塑造它。你也可以让 Codex 采访你并起草一个具有明确成功标准的目标。

目标启动后，你可以继续引导 Codex。发送后续消息以调整约束，例如要求 Codex 使用特定库或避免某种方式。当你想要状态摘要或解释而不打断主要任务时，使用侧边聊天。对于长期工作，在失去连接前暂停目标，然后在准备好继续时恢复或编辑它。

### 速度

来源：[Speed](/codex/speed.md)

#### 快速模式

Codex 提供提高模型速度的能力，但会消耗更多积分。

快速模式使支持的模型速度提升 1.5 倍，并且比标准模式消耗更高的积分。目前支持 GPT-5.5 和 GPT-5.4，GPT-5.5 的积分消耗为标准速率的 2.5 倍，GPT-5.4 为标准速率的 2 倍。

在 CLI 中使用 `/fast on`、`/fast off` 或 `/fast status` 更改或查看当前设置。你也可以通过在 `config.toml` 中设置 `service_tier = "fast"` 和 `[features].fast_mode = true` 来持久保存默认值。Codex IDE 扩展、Codex CLI 和使用 ChatGPT 登录的 Codex 应用都可使用快速模式。对于 API 密钥，Codex 使用标准 API 定价，无法使用快速模式积分。

#### Codex-Spark

GPT-5.3-Codex-Spark 是一个单独的快速、更低能力的 Codex 模型，优化用于近乎即时的实时编码迭代。与快速模式在更高积分率下加速支持模型不同，Codex-Spark 是其自身的模型选择，且具有自己的使用限制。

在研究预览期间，Codex-Spark 仅对 ChatGPT Pro 订阅者可用。

## 审批、沙箱和安全

<a id="approvals-sandboxing-and-security"></a>

沙箱行为、审批、网络安全和安全专项指导。

### Codex 安全常见问题

来源：[FAQ](/codex/security/faq.md)

#### 安全常见问题：入门

#### 什么是 Codex Security？

软件安全仍然是工程中最难且最重要的问题之一。Codex Security 是一个由大型语言模型驱动的安全分析工具包，它检查源代码并返回结构化、排序的漏洞发现以及建议修复。它帮助开发人员和安全团队规模化地发现并修复安全问题。

#### 为什么它很重要？

软件是现代工业和社会的基础，漏洞会带来系统性风险。Codex Security 支持先防守的工作流，持续识别可能问题、在可能情况下进行验证，并建议修复方案。这有助于团队在不减慢开发速度的情况下提高安全性。

#### Codex Security 解决了什么业务问题？

Codex Security 缩短了从怀疑问题到确认、可复现发现并带证据和建议补丁的路径。与传统扫描器单独使用相比，它减少了分拣负担并降低了误报。

#### Codex Security 如何工作？

Codex Security 在一个临时的隔离容器中运行分析，并暂时克隆目标仓库。它执行代码级分析，并返回包含描述、文件和位置、严重性、根因和建议修复的结构化发现。

对于包含验证步骤的发现，系统会在相同沙箱中执行建议的命令或测试，记录成功或失败、退出代码、stdout、stderr、测试结果，以及任何生成的 diff 或工件，并将这些输出作为审查证据附加。

#### 它会取代 SAST 吗？

不。Codex Security 是对 SAST 的补充。它增加了语义化、大型模型驱动的推理和自动验证，而现有 SAST 工具仍提供广泛的确定性覆盖。

#### 功能

#### 分析管道是什么？

Codex Security 遵循分阶段管道：

1. **分析** 为仓库构建威胁模型。
2. **提交扫描** 审查已合并提交和仓库历史以查找可能问题。
3. **验证** 尝试在沙箱中复现可能漏洞以减少误报。
4. **修补** 与 Codex 集成，提出建议补丁，审查者可以在打开 PR 之前检查。

它与 GitHub、Codex 以及标准审查工作流中的工程师协同工作。

#### 支持哪些语言？

Codex Security 是语言无关的。实际上，性能取决于模型对仓库使用的语言和框架的推理能力。

#### 扫描完成后我会得到什么输出？

你会获得带有严重性、验证状态以及可用时建议补丁的排序发现。发现还可以包含崩溃输出、复现证据、调用路径上下文和相关注释。

#### 客户代码如何隔离？

每个分析和验证作业都在一个临时的 Codex 容器中运行，并具有会话作用域工具。工件会被提取以供审查，作业完成后容器会被销毁。

#### Codex Security 会自动应用补丁吗？

不会。建议补丁是推荐修复。用户可以审查它，并从发现界面将其作为 PR 推送到 GitHub，但 Codex Security 不会自动向仓库应用更改。

#### 项目需要构建才能扫描吗？

不。Codex Security 可以仅从仓库和提交上下文生成发现，而无需编译步骤。在自动验证期间，如果有助于复现问题，它可能会尝试在容器内构建项目。有关环境设置详情，请参见 [Codex 云环境](/codex/cloud/environments)。

#### Codex Security 如何减少误报并避免破坏性补丁？

Codex Security 使用两个阶段。首先，模型对可能问题进行排序。然后自动验证尝试在干净容器中复现每个问题。成功复现的发现会被标记为已验证，这有助于在人工审查前减少误报。

#### 初次扫描需要多长时间？之后会怎样？

初次扫描时间取决于仓库大小、构建时间以及进入验证的发现数量。对于某些仓库，扫描可能需要几小时。对于较大仓库，可能需要多天。后续扫描通常更快，因为它们聚焦于新提交和增量更改。

#### 什么是威胁模型？

威胁模型是仓库扫描期间的安全上下文。它将项目概述与攻击面细节（如入口点、信任边界、认证假设和风险组件）结合在一起。详情请参见 [改进威胁模型](/codex/security/threat-model)。

#### 威胁模型如何生成？

Codex Security 会提示模型总结仓库架构和安全入口点，分类仓库类型，运行专用提取器，并将结果合并为项目概述或威胁模型工件，用于整个扫描过程。

#### 它会取代手动安全审查吗？

不会。Codex Security 加速审查并有助于排序发现，但它不会取代代码级验证、可利用性检查或人工威胁评估。

#### 我可以编辑威胁模型吗？

可以。Codex Security 会创建初始威胁模型，你可以在架构、风险和业务上下文发生变化时更新它。有关编辑工作流，请参见 [改进威胁模型](/codex/security/threat-model)。

### Codex Security 插件

来源：[Codex Security plugin](/codex/security/plugin.md)

Codex Security 插件为你有权限评估的代码添加安全审查工作流。在打开的仓库中使用它来调查代码库、审查变更集安全回归、确认可行发现，并准备可审查的最小修复。

本页面介绍在 Codex 线程中运行的可安装插件。对于通过 Codex Web 扫描连接 GitHub 仓库的研究预览产品，请参见 [Codex Security](/codex/security)。

#### 安装插件

安装 Codex Security 插件

    安装后，在你要评估的仓库中启动一个新线程。

1. 打开 Codex

   从你的仓库启动 Codex：

   ```bash
   codex
   ```

2. 打开插件浏览器

   输入：

   ```text
   /plugins
   ```

3. 安装 Codex Security

   搜索 **Codex Security**，打开它，然后选择 `Install plugin`。

4. 启动新线程

   在你有权限审查的仓库中启动一个新线程。

#### 选择安全工作流

选择最窄的工作流来回答你的问题。一个以 diff 为中心的扫描比仓库范围扫描更易于审查；深度扫描故意使用更多时间和令牌去搜索更多候选发现。

| 目标 | 技能 | 范围与输出 |
| -------------------------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 审查仓库或一个有范围的路径 | `$codex-security:security-scan` | 运行威胁建模、发现发现、验证、攻击路径分析，并生成 Markdown 和 HTML 报告。 |
| 运行高召回审计 | `$codex-security:deep-security-scan` | 在验证和报告前重复仓库范围发现并委派工作者。仅对整个仓库使用。 |
| 在合并前审查更改 | `$codex-security:security-diff-scan` | 审查拉取请求、提交、分支差异或工作树补丁，并生成以更改代码为基础的 Markdown 报告。 |
| 修复一个发现 | `$codex-security:fix-finding` | 复现或验证一个可行发现，必要时进行最小修复，并检查漏洞行为不再复现。 |

例如，要扫描仓库：

```text
Use $codex-security:security-scan to scan this repository for security
vulnerabilities. Keep the scan grounded in code evidence, validate plausible
findings where feasible, and return the final report paths. Do not modify code.
```

要审查当前更改：

```text
Use $codex-security:security-diff-scan to review the current branch diff for
security regressions. Keep the review scoped to changed code and directly
supporting files. Do not modify code.
```

#### 审查结果并修复发现

仓库扫描使用分阶段工作流：

1. **威胁建模** 识别入口点、信任边界、敏感操作和风险组件。
2. **发现发现** 搜索请求范围内的具体源到汇路径或破坏控制。
3. **验证** 测试或以其他方式验证可行发现，并记录证据或缺口。
4. **攻击路径分析** 跟踪可利用路径，并对验证后存活的发现评估严重性。
5. **报告** 将发现、受影响位置、验证证据、修复指导和审查指令写入工件。

普通仓库扫描或深度扫描会在其扫描目录中写入 `report.md` 和可读的 `report.html`。差异扫描会写入一个聚焦的 Markdown 报告。开始修复前，请审查受影响文件、证据、假设和严重性。

当发现可操作时，请请求有界修复：

```text
Use $codex-security:fix-finding to fix finding [finding ID or report
reference]. Add focused regression coverage, verify legitimate behavior still
works, and show that the original issue no longer reproduces. Do not broaden
the change beyond this finding.
```

#### 保持安全工作获得授权且可审查

仅对你拥有或组织授权你评估的仓库、差异和系统运行扫描。发现是审查的输入，不是合并代码或测试无关目标的指令。

- 仅在你明确要求 Codex 准备修复时，才让首次扫描变为可写。
- 在不熟悉仓库时，批准构建、运行或复现行为的命令之前，请先审查它们。
- 在合并前，审查每个建议补丁和验证结果。
- 使用插件时，保持仓库指令和审批策略到位。详情请参见 [代理审批与安全](/codex/agent-approvals-security)。

#### 探索安全用例

- [运行深度安全扫描](/codex/use-cases/deep-security-scan)
- [扫描代码更改以确保安全](/codex/use-cases/scan-code-changes-for-security)
- [修复漏洞积压](/codex/use-cases/remediate-vulnerability-backlog)

### Codex Security 设置

来源：[Codex Security setup](/codex/security/setup.md)

本页面将引导你从初次访问到 Codex Security 的审查发现和修复拉取请求。

首先确认已设置 Codex Cloud。如果没有，请参见 [Codex Cloud](/codex/cloud) 获取入门指导。

#### 1. 访问和环境

Codex Security 扫描通过 [Codex Cloud](/codex/cloud) 连接的 GitHub 仓库。

- 确认你的工作区有权访问 Codex Security。
- 确认你要扫描的仓库可在 Codex Cloud 中使用。

转到 [Codex environments](https://chatgpt.com/codex/settings/environments) 并检查该仓库是否已有环境。如果没有，请在继续之前先在那里创建一个。

[打开环境](https://chatgpt.com/codex/settings/environments)

#### 2. 新建安全扫描

环境存在后，转到 [Create a security scan](https://chatgpt.com/codex/security/scans/new) 并选择你刚连接的仓库。

[创建安全扫描](https://chatgpt.com/codex/security/scans/new)

Codex Security 会先从最新提交向后扫描仓库。它利用这一点在新提交到来时构建并刷新扫描上下文。

配置仓库时：

1. 选择 GitHub 组织。
2. 选择仓库。
3. 选择要扫描的分支。
4. 选择环境。
5. 选择一个**历史窗口**。窗口越长提供的上下文越多，但回填时间越长。
6. 点击**创建**。

#### 3. 初始扫描可能需要一段时间

创建扫描后，Codex Security 首先对所选历史窗口运行提交级安全检查。
初始回填可能需要几小时，尤其对于较大仓库或较长窗口。
如果发现尚未立即可见，这是正常的。在初始扫描完成前，请等待，不要立即打开工单或故障排除。

初始扫描设置是自动且彻底的。若第一批发现延迟出现，不要惊慌。

#### 4. 审查扫描并改进威胁模型

[审查扫描](https://chatgpt.com/codex/security/scans)

初始扫描完成后，打开扫描并审查生成的威胁模型。
初始发现出现后，更新威胁模型，使其匹配你的架构、信任边界和业务上下文。
这有助于 Codex Security 为你的团队排序问题。

如果你希望扫描结果发生变化，可以使用更新的范围、优先级和假设编辑威胁模型。

初始发现出现后，重新审视模型，以便扫描指导与当前优先级保持一致。
保持其当前状态有助于 Codex Security 生成更好的建议。

有关威胁模型及其如何影响严重性和分流的更深入解释，请参见 [改进威胁模型](/codex/security/threat-model)。

#### 5. 审查发现并修补

初始回填完成后，从 **发现** 视图审查发现。

[打开发现](https://chatgpt.com/codex/security/findings)

你可以使用两种视图：

- **推荐发现**：仓库最关键问题的动态前十列表
- **全部发现**：仓库中发现的可排序、可筛选表格

点击某一发现可打开其详细页面，其中包括：

- 问题的简洁描述
- 提交详情和文件路径等关键元数据
- 有关影响的上下文推理
- 相关代码摘录
- 可用时的调用路径或数据流上下文
- 验证步骤和验证输出

你可以审查每个发现，并直接从发现详细页创建 PR。

[审查发现并创建 PR](https://chatgpt.com/codex/security/findings)

#### 安全设置参考

- [Codex Security](/codex/security) 提供产品概述。
- [FAQ](/codex/security/faq) 涵盖常见问题。
- [改进威胁模型](/codex/security/threat-model) 解释如何改进扫描上下文和发现优先级。

### 改进威胁模型

来源：[Improving the threat model](/codex/security/threat-model.md)

了解什么是威胁模型，以及编辑它如何改进 Codex Security 的建议。

#### 什么是威胁模型

威胁模型是你仓库工作方式的简短安全摘要。在 Codex Security 中，你将其作为“项目概述”进行编辑，系统将其用作后续扫描、优先级和审查的上下文。

Codex Security 会从代码中创建第一稿。如果发现结果感觉不对，这是首先要编辑的内容。

一个有用的威胁模型会指出：

- 入口点和不受信任输入
- 信任边界和认证假设
- 敏感数据路径或特权操作
- 团队希望优先审查的区域

例如：

> 公共帐户变更 API。接受 JSON 请求和文件上传。使用内部认证服务进行身份检查，并通过内部服务写入计费变更。重点审查认证检查、上传解析和服务间信任边界。

这使 Codex Security 为未来扫描和发现优先级提供更好的起点。

#### 改进和重新审视威胁模型

如果你想改进结果，请先编辑威胁模型。当发现缺少你关心的区域或出现在你不期望的地方时，使用它。威胁模型会改变未来的扫描上下文。

一些用户会将当前威胁模型复制到 Codex，与其对话以根据他们希望更密切审查的区域改进它，然后将更新后的版本粘贴回 Web UI。

#### 在哪里编辑

要审查或更新威胁模型，请转到 [Codex Security scans](https://chatgpt.com/codex/security/scans)，打开仓库，然后单击 **Edit**。

#### 威胁模型参考

- [Codex Security setup](/codex/security/setup) 涵盖仓库设置和发现审查。
- [Codex Security](/codex/security) 提供产品概述。
- [FAQ](/codex/security/faq) 涵盖常见问题。

### 代理审批与安全

来源：[Agent approvals & security](/codex/agent-approvals-security.md)

Codex 帮助保护你的代码和数据，并降低误用风险。

本页面介绍如何安全操作 Codex，包括沙箱、审批和网络访问。如果你在寻找 Codex Security（用于扫描连接 GitHub 仓库的产品），请参见 [Codex Security](/codex/security)。

默认情况下，代理运行时网络访问关闭。本地环境中，Codex 使用操作系统强制的沙箱机制限制其可接触范围（通常限于当前工作区），并使用审批策略控制其何时必须停止并在行动前询问你。

有关 Codex 应用、IDE 扩展和 CLI 中沙箱如何工作的高级解释，请参见 [沙箱](/codex/concepts/sandboxing)。
有关更广泛的企业安全概述，请参见 [Codex 安全白皮书](https://trust.openai.com/?itemUid=382f924d-54f3-43a8-a9df-c39e6c959958&source=click)。

#### 沙箱与审批

Codex 安全控制来自两个协同工作的层级：

- **沙箱模式**：当执行模型生成的命令时，Codex 在技术上可以做什么（例如，它可以写入哪里、是否可以访问网络）。
- **审批策略**：Codex 在执行某个动作前何时必须先征求你许可（例如，离开沙箱、使用网络或运行工作区外的命令）。

Codex 根据运行位置使用不同的沙箱模式：

- **Codex 云**：在 OpenAI 管理的隔离容器中运行，防止访问你的主机系统或无关数据。使用两阶段运行时模型：设置阶段在代理阶段前运行，并可以访问网络以安装指定依赖；然后代理阶段默认离线运行，除非你为该环境启用互联网访问。配置给云环境的秘密仅在设置阶段可用，并在代理阶段开始前移除。
- **Codex CLI / IDE 扩展**：OS 级机制强制执行沙箱策略。默认包括禁止网络访问和将写权限限制在活动工作区内。你可以根据风险承受能力配置沙箱、审批策略和网络设置。

在 `Auto` 预设中（例如 `--sandbox workspace-write --ask-for-approval on-request`），Codex 可以自动读取文件、进行编辑并运行工作目录中的命令。

Codex 会在编辑工作区外的文件或运行需要网络访问的命令时请求审批。如果你想聊天或规划而不做更改，请使用 `/permissions` 命令切换到 `read-only` 模式。

Codex 还可以针对宣传副作用的应用（连接器）工具调用引发审批，即使该操作不是 shell 命令或文件更改。破坏性应用/MCP 工具调用总是需要审批，只要工具宣称具有破坏性注释，即便它也提供其他提示（例如只读提示）。

#### 网络访问

对于 Codex 应用、CLI 或 IDE 扩展，默认 `workspace-write` 沙箱模式在你未在配置中启用时关闭网络访问：

```toml
[sandbox_workspace_write]
network_access = true
```

#### 网络隔离

网络访问通过目标规则控制，适用于脚本、程序和命令生成的子进程。当命令网络访问已启用时，开启 `network_proxy` 可将该流量约束到你配置的网络策略。

```toml
[features.network_proxy]
enabled = true
domains = { "api.openai.com" = "allow", "example.com" = "deny" }
```

对于一次性 CLI 会话，当你只需要切换时使用布尔简写；当你还要设置策略选项时使用表格形式：

```bash
codex \
  -c 'features.network_proxy=true' \
  -c 'sandbox_workspace_write.network_access=true'

codex \
  -c 'features.network_proxy.enabled=true' \
  -c 'features.network_proxy.domains={ "api.openai.com" = "allow", "example.com" = "deny" }' \
  -c 'sandbox_workspace_write.network_access=true'
```

此功能更改已启用网络访问时的强制方式；它本身不授予网络访问。请将 `sandbox_workspace_write.network_access` 与 `workspace-write` 配置结合使用，以决定命令是否具有网络访问：

- 网络关闭 + `network_proxy` 开启：网络保持关闭，特性无效。
- 网络开启 + `network_proxy` 关闭：网络保持开启，直接外发访问不受限。
- 网络开启 + `network_proxy` 开启：网络开启，外发流量受配置的网络策略约束。

管理员管理的 `experimental_network` 要求与用户功能开关分开。它们可以在没有 `features.network_proxy` 的情况下配置并启动沙箱网络，但当活动沙箱将其关闭时，它们不会打开网络访问。有关管理员端 `requirements.toml` 形式，请参见 [托管配置](/codex/enterprise/managed-configuration#configure-network-access-requirements)。

#### 网络策略

域规则采用先允许列表方式：

- 精确主机仅匹配自身。
- `*.example.com` 匹配子域，如 `api.example.com`，但不匹配 `example.com`。
- `**.example.com` 同时匹配 apex 和子域。
- 全局 `*` 允许规则匹配任何未被拒绝的公共主机。将 `*` 视为广泛网络访问，若可能请优先使用作用域规则。
- `deny` 总是优先于 `allow`，且全局 `*` 仅对允许规则有效。

#### 本地和私有目标

默认情况下，`allow_local_binding = false` 阻止环回、链路本地和私有目标：

- 具体例外：当命令需要一个本地目标时，添加精确本地 IP 文字或 `localhost` 允许规则。
- 更广泛访问：仅在你有意希望更广泛本地/私有访问时，将 `allow_local_binding = true`。
- 通配符：通配符规则不计入显式本地例外。
- 解析地址：解析为本地/私有 IP 的主机名即使匹配允许列表也仍然被阻止。

#### DNS 重新绑定保护

在允许主机名之前，Codex 会进行尽力而为的 DNS 和 IP 分类检查：

- 查找失败或超时的情况下会阻止该主机名。
- 解析为非公共地址的主机名会被阻止。
- 该检查降低了 DNS 重新绑定风险，但不能完全消除它。要完全防止重新绑定，需要通过传输层锁定解析后的 IP。

如果敌对 DNS 在范围内，也应在更低层实施出站控制。

#### 危险设置

有两个设置会有意扩大信任边界：

- `dangerously_allow_non_loopback_proxy = true` 可能将代理监听器暴露到环回之外。
- `dangerously_allow_all_unix_sockets = true` 绕过 Unix socket 允许列表。

仅在严格控制的环境中使用它们。启用 Unix socket 代理时，即使请求了非环回绑定，监听器仍保持环回范围，因此沙箱网络不会变成访问本地守护进程的远程桥。

`network_proxy` 默认关闭。启用时：

| 设置 | 默认 | 行为 |
| -------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------ |
| `enabled` | `false` | 仅当命令网络访问已开启时才启动沙箱网络。 |
| `domains` | unset | 使用允许列表行为，因此在添加 `allow` 规则之前不允许任何外部目标。支持精确主机、作用域通配符和全局 `*` 允许规则；`deny` 总是优先。 |
| `unix_sockets` | unset | 在你添加显式 `allow` 规则之前，不允许任何 Unix socket 目标。 |
| `allow_local_binding` | `false` | 阻止本地和私有网络目标，除非你添加精确本地 IP 文字或 `localhost` 允许规则，或显式选择更广泛本地/私有访问。 |
| `enable_socks5` | `true` | 在策略允许时启用 SOCKS5 支持。 |
| `enable_socks5_udp` | `true` | 在 SOCKS5 可用时允许 UDP over SOCKS5。 |
| `allow_upstream_proxy` | `true` | 允许沙箱网络遵循来自环境的上游代理。 |
| `dangerously_allow_non_loopback_proxy` | `false` | 除非你刻意将其暴露到 localhost 之外，否则将监听端点限制在环回。 |
| `dangerously_allow_all_unix_sockets` | `false` | 将 Unix socket 访问保留为基于允许列表，除非你刻意绕过该保护。 |

你还可以在不授予对生成命令的完整网络访问的情况下控制[网络搜索工具](https://platform.openai.com/docs/guides/tools-web-search)。Codex 默认使用网络搜索缓存访问结果。缓存模式是一个由 OpenAI 维护的网页结果索引，因此缓存模式返回预索引结果，而不是获取实时页面。这减少了来自任意实时内容的提示注入风险，但你仍应将网页结果视为不受信任内容。如果你正在使用 `--yolo` 或其他 [完全访问沙箱设置](#common-sandbox-and-approval-combinations)，网络搜索默认使用实时结果。使用 `--search` 或将 `web_search = "live"` 以允许实时浏览；或将其设置为 `"disabled"` 以关闭工具：

```toml
web_search = "cached"  # 默认
# web_search = "disabled"
# web_search = "live"  # 等同于 --search
```

在 Codex 中启用网络访问或网络搜索时请谨慎。提示注入可能导致代理获取并遵循不受信任的指令。

#### 默认值和建议

- 启动时，Codex 会检测文件夹是否受版本控制，并推荐：
  - 版本控制文件夹：`Auto`（工作区写入 + 按需审批）
  - 非版本控制文件夹：`read-only`
- 根据你的设置，Codex 也可能在你明确信任工作目录之前启动为 `read-only`（例如通过入职提示或 `/permissions`）。
- 工作区包括当前目录和临时目录，如 `/tmp`。使用 `/status` 命令查看哪些目录包含在工作区中。
- 若要接受默认设置，请运行 `codex`。
