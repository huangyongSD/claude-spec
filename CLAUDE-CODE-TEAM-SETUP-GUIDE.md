# AI 团队规范

> 版本：1.4 | 日期：2026-04-22
> 基于《AI 团队落地指南》梳理，适用于已有项目一步到位引入团队规范
> 引入 Steering 文件与 Spec 工作流（来自 AWS Kiro 实战培训）
> 新增智能体质量门禁体系（来自生产级项目实战）
>
> **声明**：本文档整合自多个实践来源，已修订为自包含的操作手册。附录内容参考了 Andrej Karpathy 的编码准则和 AWS Kiro 培训材料，均已适配为可直接使用的配置模板。
```text
  1. 打开 Claude Code，说：「扫描当前项目，提炼技术栈/数据库/中间件/包管理器/构建命令/测试命令/格式化命令/核心目录/覆盖率」
  2. 把这份手册发给 Claude Code，说：「按手册中的模板创建所有配置文件，用刚才的扫描结果替换 {{...}} 占位符」
  3. 按手册第四、五章执行 Git 提交、创建 PR、团队过会
  4. 按手册第五章跟进 Day 7 / Day 14 / Day 30 节奏
  5. 按手册第六章执行质量门禁，确保交付前 10 项检查全绿
```  
---

## 使用说明

本手册是一份**自包含的、可移植的**操作指南。到达目标项目后，按顺序执行即可。

你只需要两样东西：
1. **本文件** — 操作手册 + 全部配置内容
2. **Claude Code** — 在目标项目中打开对话

不需要额外的模板文件——所有配置内容都在本文件的「配置模板」章节中，直接复制使用。

---

## 目录

1. [落地流程总览](#一落地流程总览)
2. [扫描项目现状](#二扫描项目现状)
3. [创建配置文件](#三创建配置文件)
4. [提交 PR + 团队过会](#四提交-pr--团队过会)
5. [跟进节奏](#五跟进节奏)
6. [质量门禁](#六质量门禁)
7. [配置模板](#七配置模板)
8. [避坑检查清单](#八避坑检查清单)
9. [附录 A：编码行为准则详细解读](#附录a编码行为准则详细解读)
10. [附录 B：Steering 文件与 Spec 工作流详解](#附录bsteering-文件与-spec-工作流详解)
11. [附录 C：Spec 文件模板](#附录cspec-文件模板)（含 C.1-C.5）
12. [附录 D：test-cases.md 模板说明](#附录dtest-casesmd-模板说明)（含 D.1-D.4）

---

## 一、落地流程总览

```
扫描项目现状 → 创建配置文件 → 提交 PR → 团队过会 → 分阶段激活
   (5 min)      (15 min)     (5 min)   (30 min)    (持续)
```

核心原则：
- **CLAUDE.md 从代码提炼**，不凭空写
- **Steer 文件填入实际信息**，不把未验证的占位符留到生产
- **rules 分档标注**（🔴🟡🟢），不把旧代码做不到的写成硬性要求
- **hooks 前 2 周提醒型**，不直接阻断
- **一个 PR 提交全部配置**，建立「变更走 PR」的先例

---

## 二、扫描项目现状

在目标项目中打开 Claude Code，执行以下操作：

### 2.1 告诉 Claude Code 扫描

直接发送：

> 扫描当前项目，帮我提炼以下信息：
> 1. 项目名称
> 2. 技术栈（前端/后端/框架/语言）
> 3. 数据库类型（MySQL / PostgreSQL / 瀚高等，如无则标注"无"）
> 4. 中间件（Redis / ActiveMQ / Kafka 等，如无则标注"无"）
> 5. 包管理器（pnpm/npm/yarn/pip/poetry/maven/gradle）
> 6. 构建命令
> 7. 测试命令
> 8. E2E 测试命令（如有）
> 9. 覆盖率命令（如有）
> 10. 格式化命令
> 11. Lint 命令
> 12. 代码文件扩展名（用于 settings.json hook 匹配，如 .java/.xml/.vue/.js/.py 等）
> 13. 核心目录及职责（每个目录一行）
> 14. 禁止修改的核心目录
> 15. 当前测试覆盖率（如有）
> 16. API 文件目录（如 `src/api/`、`src/services/`，用于配置 api.md 的 fileMatchPattern）
> 17. 测试文件目录（如 `tests/`、`src/__tests__/`，用于配置 testing.md 的 fileMatchPattern）

### 2.2 记录结果

将 Claude 返回的信息整理成一份摘要，格式示例：

```
项目名称：ruoyi-admin
技术栈：SpringBoot + RuoYi + JDK8 + Vue3
数据库：MySQL（主库）/ 瀚高（备库适配）
中间件：Redis（缓存/会话） / ActiveMQ（异步通知） / Kafka（日志采集）
包管理器：Maven（后端）/ pnpm（前端）
构建命令：mvn package（后端）/ pnpm build（前端）
测试命令：mvn test（后端）/ pnpm test（前端）
E2E 测试命令：无（后端）/ pnpm test:e2e（如无则标注"无"）
覆盖率命令：无（后端）/ pnpm test:coverage（前端）
格式化命令：无（后端，IDE 格式化）/ pnpm format（前端）
Lint 命令：无（后端）/ pnpm lint（前端）
代码文件扩展名：java, xml, vue, js, sql
核心目录：ruoyi-admin（主模块）、ruoyi-system（系统模块）、ruoyi-common（公共模块）、src/views（前端页面）
禁止修改目录：ruoyi-framework（核心框架配置）
当前测试覆盖率：18%
```

**这份摘要是后续所有配置的输入，务必确认准确。**

### 2.3 占位符说明

后续配置模板中使用的占位符含义如下：

| 占位符 | 含义 | 示例值 |
|--------|------|--------|
| `{{项目名称}}` | 项目名称 | ruoyi-admin |
| `{{技术栈}}` | 前端/后端框架+语言 | SpringBoot + RuoYi + JDK8 + Vue3 |
| `{{数据库类型}}` | 数据库类型及版本 | MySQL 8.0 / 瀚高 / PostgreSQL 13 |
| `{{中间件}}` | 中间件名称及用途 | Redis（缓存/会话）/ ActiveMQ（异步通知） |
| `{{包管理器}}` | 项目包管理器 | Maven / pnpm / pip / yarn |
| `{{构建命令}}` | 构建命令 | mvn package / pnpm build |
| `{{测试命令}}` | 单元测试命令 | mvn test / pnpm test |
| `{{E2E测试命令}}` | E2E测试命令（如无则标注"无"） | pnpm test:e2e |
| `{{格式化命令}}` | 代码格式化命令 | pnpm format / mvn spotless:apply |
| `{{Lint 命令}}` | Lint 检查命令（如无则标注"无"） | pnpm lint |
| `{{覆盖率命令}}` | 测试覆盖率命令（如无则标注"无"） | pnpm test:coverage |
| `{{当前覆盖率}}` | 当前测试覆盖率百分比 | 18% |
| `{{目录1}}` `{{职责1}}` | 核心目录及职责 | ruoyi-admin / 主模块 |
| `{{禁止目录}}` | 禁止修改的核心目录 | ruoyi-framework |
| `{{API文件匹配模式}}` | API 文件 glob 模式 | src/api/**/*.ts |
| `{{测试文件匹配模式}}` | 测试文件 glob 模式 | tests/**/*.test.ts |
| `{{文件扩展名}}` | 代码文件扩展名正则 | (java\|xml\|vue\|js)$ |

> **多包管理器项目**：如前后端分离项目，占位符需要分行标注。例如 `{{包管理器}}` 填为 `Maven（后端）/ pnpm（前端）`，`{{构建命令}}` 填为 `mvn package（后端）/ pnpm build（前端）`。

### 2.4 需人工填写的占位符

以下占位符无法通过自动化扫描获得，需要根据项目实际情况人工填写（主要用于 Steering 文件模板）：

| 占位符 | 含义 | 填写时机 |
|--------|------|---------|
| `{{业务域1}}` `{{业务域2}}` | 核心业务域名称及描述 | 填写 product.md |
| `{{技术A}}` `{{技术B}}` | 技术选型项 | 填写 product.md |
| `{{原因}}` | 技术选型原因、陷阱原因等 | 填写 product.md / never.md |
| `{{规范}}` | 团队分支命名规范 | 填写 product.md |
| `{{简述}}` | 发布流程简述 | 填写 product.md |
| `{{N}}` | 代码审查需要通过的人数 | 填写 product.md |
| `{{前端框架}}` `{{后端框架}}` | 前后端框架名称及版本 | 填写 tech.md |
| `{{依赖1}}` `{{依赖2}}` | 关键依赖名称及用途 | 填写 tech.md |
| `{{项目目录}}` `{{目录树}}` | 项目根目录名和完整目录树 | 填写 structure.md |
| `{{目录2}}` `{{职责2}}` | 额外核心目录及职责 | 填写 CLAUDE.md |
| `{{路由文件}}` `{{handler目录}}` `{{业务逻辑文件}}` 等 | 修改导航的目标文件/目录 | 填写 structure.md |
| `{{关键文件1}}` `{{频率}}` | 关键文件路径及修改频率 | 填写 structure.md |
| `{{方案A}}` `{{方案B}}` `{{日期}}` 等 | 架构决策记录字段 | 填写 structure.md |
| `{{核心目录}}` `{{配置文件}}` | 禁止修改的目录和文件 | 填写 never.md |
| `{{模块}}` `{{负责人}}` `{{方式}}` | 修改限制相关字段 | 填写 never.md |
| `{{反模式}}` `{{技术}}` `{{编号}}` 等 | 代码风格强制项 | 填写 never.md |
| `{{陷阱1}}` `{{做法}}` | 已知陷阱及正确做法 | 填写 never.md |
| `{{API文件匹配模式}}` `{{测试文件匹配模式}}` | glob 模式 | 根据项目目录结构填写 |

> **填写原则**：上述占位符均为引导型占位符，提示用户需要填入项目特有的信息。填写时可参考模板中的示例格式，替换为实际内容。

---

## 三、创建配置文件

按以下顺序逐个创建。每个文件的内容在 [第七章：配置模板](#七配置模板) 中，需要将 `{{...}}` 占位符替换为第二步提炼的实际值。

### 3.1 文件清单

| 序号 | 文件 | 是否需要改造 | 说明 |
|------|------|-------------|------|
| 1 | `CLAUDE.md` | **需要** | 填入扫描结果 + Steer/Spec 章节 + 质量门禁 |
| 2 | `.claude/steer/foundation/product.md` | **需要** | 项目概述，填入实际背景 |
| 3 | `.claude/steer/foundation/tech.md` | **需要** | 技术栈与架构，填入实际技术 |
| 4 | `.claude/steer/foundation/structure.md` | **需要** | 目录结构 + 修改导航，填入实际结构 |
| 5 | `.claude/steer/foundation/never.md` | **需要** | NEVER 列表，填入实际禁止项 |
| 6 | `.claude/steer/foundation/quality-gate.md` | **需要** | 质量门禁清单，填入实际命令 |
| 7 | `.claude/steer/domain/api.md` | **需要** | API 规范，填入 fileMatchPattern |
| 8 | `.claude/steer/domain/testing.md` | **需要** | 测试规范，填入 fileMatchPattern |
| 9 | `.claude/steer/domain/security.md` | **需要** | 安全规范（auto 类型） |
| 10 | `.claude/rules/security.md` | **需要** | 确认分档标记，增强后端安全规范 |
| 11 | `.claude/rules/testing.md` | **需要** | 重构为深度测试体系 |
| 12 | `.claude/rules/frontend.md` | **需要** | 前端编码底线规则（前端项目必填） |
| 13 | `.claude/rules/git.md` | 小改 | 确认分档标记 |
| 14 | `.claude/rules/agent-collaboration.md` | **新增** | Agent 协作规范 |
| 15 | `.claude/commands/sd-plan.md` | 不需要 | 直接复制 |
| 16 | `.claude/commands/sd-codereview.md` | 不需要 | 直接复制 |
| 17 | `.claude/commands/sd-buildfix.md` | 不需要 | 直接复制 |
| 18 | `.claude/commands/sd-dev.md` | **新增** | 全栈开发编排命令 |
| 19 | `.claude/commands/sd-spec.md` | **新增** | Spec 创建命令（含评审机制） |
| 20 | `.claude/agents/architect.md` | **新增** | 架构设计 Agent |
| 21 | `.claude/agents/sd-reviewer.md` | **新增** | Spec 文档评审 Agent |
| 22 | `.claude/agents/db-implementer.md` | **新增** | 数据库实现 Agent |
| 23 | `.claude/agents/backend.md` | **新增** | 后端实现 Agent |
| 24 | `.claude/agents/frontend.md` | **新增** | 前端实现 Agent |
| 25 | `.claude/agents/tester.md` | **新增** | E2E 测试 Agent |
| 26 | `.claude/agents/code-reviewer.md` | **需要** | 增强审查清单 |
| 27 | `.claude/agents/coverage-auditor.md` | **新增** | 覆盖率审计 Agent |
| 28 | `.claude/agents/build-error-resolver.md` | **需要** | 适配技术栈，删除不相关的诊断条目 |
| 29 | `.claude/skills/troubleshooting.md` | **需要** | 适配技术栈 |
| 30 | `.claude/settings.json` | **需要** | 填入包管理器、文件扩展名和格式化命令 |
| 31 | `.mcp.json.example` | 小改 | 按需增减 MCP 服务 |
| 32 | `.gitignore` | 追加 | 添加 .mcp.json、.env |
| 33 | `.claude/templates/spec/requirements.md` | 不需要 | Spec 需求文档模板 |
| 34 | `.claude/templates/spec/design.md` | 不需要 | Spec 设计文档模板 |
| 35 | `.claude/templates/spec/test-cases.md` | 不需要 | Spec 测试用例文档模板（测试先行核心） |
| 36 | `.claude/templates/spec/tasks.md` | 不需要 | Spec 任务清单模板（含测试任务） |

共 **36 个文件**（Steering 8个 + rules 5个 + commands 5个 + agents 9个 + skills 1个 + settings 1个 + templates 4个 + 其他 3个）。

> **可选文件说明**：`steer/domain/frontend.md`（7.7.9 节）为前端项目可选配置，如创建则文件总数为 37 个。

> **Spec 模板说明（测试先行模式）**：附录 C、D 的四个模板在初始化时固化到 `.claude/templates/spec/` 目录。每个新功能开发时，AI 读取这些模板，在 `.claude/specs/<feature>/` 下创建对应的 Spec 文件。**test-cases.md 是测试先行核心**，在 design.md 之后、tasks.md 之前创建。

### 3.2 告诉 Claude Code 创建

告诉 Claude Code：

> 在当前项目中创建 AI 团队规范配置文件。我会提供项目扫描结果，你按照以下文件的模板创建所有配置。需要改造的文件用我提供的信息替换 {{...}} 占位符。
> **重点**：Steering 文件（.claude/steer/）是本次新增的核心配置，需要填入项目的心智地图——构建命令、目录结构、修改导航、NEVER 列表。详见 7.7 节的 8 个 Steer 文件模板。

然后提供扫描结果，让 Claude 逐个创建文件。

### 3.3 创建目录结构

```bash
mkdir -p .claude/rules .claude/commands .claude/agents .claude/skills .claude/steer/foundation .claude/steer/domain .claude/steer/reference .claude/specs .claude/templates/spec
```

> **Windows PowerShell 替代**：`New-Item -ItemType Directory -Force -Path .claude/rules,.claude/commands,.claude/agents,.claude/skills,.claude/steer/foundation,.claude/steer/domain,.claude/steer/reference,.claude/specs,.claude/templates/spec`

> **说明**：
> - `.claude/steer/reference/` — 可选目录，存放 manual 类型的大型参考文档，本次 PR 可先创建空目录
> - `.claude/specs/` — 功能级 Spec 文件目录，每个新功能开发时在此创建 `<feature>/` 子目录
> - `.claude/templates/spec/` — Spec 模板目录，初始化时创建 4 个模板文件（requirements.md、design.md、**test-cases.md**、tasks.md），AI 创建新功能 Spec 时读取这些模板（测试先行模式）

### 3.4 验证文件创建

```bash
find .claude -type f | sort
```

> **Windows PowerShell 替代**：`Get-ChildItem -Recurse -File .claude | Sort-Object Name | Select-Object FullName`

确认输出包含 **31 个文件**：`.claude/` 目录下 28 个 + 项目根目录 3 个（CLAUDE.md、.mcp.json.example、.gitignore 已追加）。与 3.1 表格一致。

---

## 四、提交 PR + 团队过会

### 4.1 创建分支并提交

```bash
git checkout -b chore/add-claude-code-team-config
git add CLAUDE.md .claude/ .mcp.json.example .gitignore
git commit -m "chore: add Claude Code team collaboration config

- CLAUDE.md: project-specific AI collaboration guide with Steer/Spec chapters
- steer/foundation/: product.md, tech.md, structure.md, never.md, quality-gate.md — project mental map
- steer/domain/: api.md, testing.md, security.md — fileMatch/auto loaded by context
- rules: security (🔴), testing (🟡🟢), git (🟡🟢) with tiered enforcement
- commands: /sd-plan, /sd-codereview, /sd-buildfix, /sd-dev, /sd-spec
- agents: architect, code-reviewer, tester, coverage-auditor, build-error-resolver
- skills: troubleshooting knowledge base
- settings: permissions + warn-level hooks (upgrade after 2 weeks)
- .mcp.json.example: MCP config template (no real credentials)
- .gitignore: added .mcp.json, .env"
git push -u origin chore/add-claude-code-team-config
```

### 4.2 创建 PR

```bash
gh pr create --title "chore: add Claude Code team collaboration config" --body "$(cat <<'EOF'
## Summary
- 引入 Claude Code 团队协作规范，统一 AI 编程行为
- 包含 31 个配置文件：CLAUDE.md / steer(foundation+domain, 8个) / rules(5个) / commands(5个) / agents(5个) / skills(1个) / settings / templates/spec(4个) / .mcp.json.example / .gitignore
- 所有规则分档标注（🔴🟡🟢），避免一刀切
- 引入 Steering 文件（项目心智地图），减少每次会话从零探索的 Token 消耗
- 引入智能体质量门禁体系（后端 nil 兜底、前端防御性消费、测试三层验证、RTM 需求追踪）
- **新增测试先行模式**：Spec 流程中增加 test-cases.md（测试用例文档），tasks.md 包含测试用例文档任务和测试执行任务，统一测试执行

## 文件说明
| 文件 | 用途 | 生效方式 |
|------|------|---------|
| CLAUDE.md | 项目 AI 说明书（含测试先行工作流） | 立即生效 |
| .claude/steer/foundation/ (5个) | 项目心智地图（always 类型） | 每次会话加载 |
| .claude/steer/domain/ (3个) | 领域规范（fileMatch/auto 类型） | 按需加载 |
| rules/security.md | 安全红线 🔴 | 立即执行 |
| rules/testing.md | 测试要求 🟡🟢 | 新代码执行，旧代码逐步达标 |
| rules/frontend.md | 前端编码底线规则 🔴🟡 | 立即执行（前端项目） |
| rules/git.md | Git 工作流 🟡🟢 | 新代码执行 |
| rules/agent-collaboration.md | Agent 协作规范 🟡 | Agent 编排时执行 |
| commands/sd-plan.md | /sd-plan 命令 | 立即可用 |
| commands/sd-codereview.md | /sd-codereview 命令 | 立即可用 |
| commands/sd-buildfix.md | /sd-buildfix 命令 | 立即可用 |
| commands/sd-dev.md | /sd-dev 全栈开发编排命令 | 立即可用 |
| commands/sd-spec.md | /sd-spec Spec 创建命令 | 立即可用 |
| agents/architect.md | 架构设计 Agent | 立即可用 |
| agents/sd-reviewer.md | Spec 文档评审 Agent | 立即可用 |
| agents/code-reviewer.md | 代码审查 Agent | 立即可用 |
| agents/tester.md | E2E 测试 Agent | 立即可用 |
| agents/coverage-auditor.md | 覆盖率审计 Agent | 立即可用 |
| agents/build-error-resolver.md | 构建排障 Agent | 立即可用 |
| skills/troubleshooting.md | 排障知识库 | 立即可用 |
| settings.json | 权限 + Hooks | Hooks 前2周提醒型 |
| .mcp.json.example | MCP 配置模板 | 复制为 .mcp.json 后使用 |
| .gitignore | 追加 .mcp.json、.env | 立即生效 |
| templates/spec/ (4个) | Spec 模板（含 test-cases.md 测试先行核心） | 立即可用 |

## Team Review 重点
1. steer/ 中的项目信息是否准确（目录结构、修改导航、NEVER 列表）
2. rules/ 中的底线规则是否有异议
3. CLAUDE.md 中提炼的项目信息是否准确
4. rules 分档（🔴🟡🟢）是否合理
5. 每人 review 后请 comment "read & agree"

## Test plan
- [ ] 每人本地拉取分支，确认 Claude Code 能读取 CLAUDE.md、steer/ 和 rules/
- [ ] 确认 steer/foundation/ 和 steer/domain/ 中的信息与实际项目一致（不是占位符）
- [ ] 确认 /sd-plan、/sd-codereview、/sd-buildfix、/sd-dev、/sd-spec 命令可正常调用
- [ ] 确认 architect、code-reviewer、tester、coverage-auditor、build-error-resolver Agent 可正常调度
- [ ] 确认 Hooks 提醒正常弹出（编辑代码文件、安装依赖时）
- [ ] **确认 Spec 模板包含 4 个文件**：requirements.md、design.md、test-cases.md、tasks.md
- [ ] **确认 test-cases.md 模板存在且包含测试用例结构**：UT/E2E 用例表、全局错误监听、三层验证
- [ ] **确认 tasks.md 模板包含测试任务**：T-DOC-xxx（测试用例文档）、T-UT-xxx（单元测试代码）、T-E2E-xxx（E2E 测试代码）、T-UT-101/T-E2E-101（统一测试执行）
- [ ] 交付前执行第六章完整门禁清单（10 项检查全绿）
EOF
)"
```

### 4.3 团队过会（30 分钟）

议程：
1. **CLAUDE.md + steer/foundation/ + steer/domain/**（10 分钟）— 确认项目信息准确，Steer 文件填入的是真实项目信息而非占位符
2. **rules/**（15 分钟）— 确认分档合理，这是最重要的部分
3. **现场演示**（3 分钟）— 跑一次 `/sd-plan` 看效果
4. **hooks 策略**（2 分钟）— 确认前 2 周提醒型

过会结束后，每人在 PR 中 comment **"read & agree"**，然后合并。

---

## 五、跟进节奏

治理机制详细表格见第七章 7.1 节 CLAUDE.md 模板中的「治理机制」章节（Day 1-3 → Day 30），此处聚焦 Hook 升级路径和规范迭代闭环。

### Hook 升级路径

```
第 1-2 周：全部提醒型（warn）     → 让团队感知系统，形成习惯（所有 hook 均 echo 0）
第 3 周：  选择性升级为一致性型   → PostToolUse hook 中自动触发格式化/Lint 命令（见 7.23 settings.json 模板中的"第 3 周升级示例"）
稳定后：  高频违规项升级为阻断型   → 安全红线直接拦截（PreToolUse hook echo 2 阻断，见 7.23 settings.json 模板中的"稳定后升级示例"）
```

> **一致性型实现方式**：在第 3 周升级时，将 PostToolUse hook 的 stderr 提醒命令替换为实际执行格式化的命令。详细配置和完整示例见 7.18 节 settings.json 模板。

### 规范迭代闭环（智能体质量门禁新增）

**核心理念**：测试质量提升是一个闭环，能预见的问题提前用规范拦住，没预见到的通过测试和审核发现后补入规范。

```
前置规范 → 自动化测试覆盖 → 人工审核 → 规范迭代
    ↑                                       |
    └───────────────────────┘
```

#### 回溯法：每个逃逸 bug 都要追问"为什么 AI 没拦住"

对每个逃逸到用户手里的 bug，逐层分析：

| 关卡 | 分析问题 |
|------|---------|
| backend agent | 写代码时为什么没防御？→ 规范中是否要求了？ |
| frontend agent | 消费数据时为什么没守卫？→ 规范中是否要求了？ |
| tester agent | 测试为什么没覆盖？→ 测试账号是否有偏差？ |
| reviewer agent | 审查为什么没发现？→ 审查清单中是否有此项？ |
| coverage-auditor | 覆盖率审计为什么没发现？→ 审计维度是否缺失？ |

**核心洞察**：单个 agent 的失误往往是规范缺失的症状。不是 agent "忘了"，而是没有规则要求它这么做。

#### 修 bug vs 改规范

- **修 bug** 只解决当前项目，改规范才防止所有未来项目重现
- 规范升级后必须用新规范重新审视项目，旧代码也可能不符合新规范
- 三道关卡设计：后端源头治理 + 前端防御性消费 + 测试覆盖，任何一道拦住就不会到用户手里

---

## 六、质量门禁

> 质量门禁是"硬校验层"的最后一道防线，与 Steering/Spec/Hooks 构成完整防护体系：
> - **Steering（规则层）**：定义"应该怎么做"的编码规范和项目约定
> - **Spec（流程层）**：定义"执行顺序"的任务流程和验收标准
> - **Hooks（自动校验层）**：实时拦截违规操作，自动执行格式化/测试
> - **质量门禁（硬校验层）**：交付前的终极检查，确保所有规则和流程都已正确执行
>
> **门禁与 Hooks 的关系**：部分门禁项（如编译检查、TODO/FIXME 检查）可能与 Hooks 的检查项重叠，这是故意的双重保险。Hooks 在开发过程中实时拦截问题，门禁在交付前做最终兜底。即使 Hooks 已拦截，门禁仍需验证——因为 Hooks 可能被绕过、禁用或失效。
>
> **配置文件**：本章节内容已固化为配置文件 `.claude/steer/foundation/quality-gate.md`（模板见 7.7.5 节），便于快速查阅和每次会话自动加载。

### 6.1 质量门禁清单（收尾检查）

每次交付前必须通过以下检查，**任何一项不满足，阻断交付**：

| 序号 | 检查项 | 验证命令/方式 |
|------|--------|--------------|
| 1 | ✅ 编译/类型检查通过 | `{{构建命令}}`（如 `mvn compile` 或 `pnpm build`），前端项目额外运行类型检查（如 `npx vue-tsc --noEmit`） |
| 2 | ✅ 测试覆盖率不低于基准 | `{{覆盖率命令}}`（如 `pnpm test:coverage`），覆盖率 ≥ 当前基准 |
| 3 | ✅ E2E 测试零失败 | `{{E2E测试命令}}`（如 `pnpm test:e2e` 或 `npx playwright test`）；如无 E2E 测试，见下方降级方案 |
| 4 | ✅ 页面零 404 | E2E 测试覆盖所有页面路由；如无 E2E 测试，见下方降级方案 |
| 5 | ✅ API 零 500 | E2E 测试监听 API 响应；如无 E2E 测试，见下方降级方案 |
| 6 | ✅ 数据字段无 undefined/null/占位符残留 | 后端 API 响应层兜底 nil 集合 + 前端防御性消费；grep 检查代码中未处理的 undefined/null/placeholder |
| 7 | ✅ 权限校验生效 | 权限测试覆盖关键角色组合（至少包含：超级管理员、普通用户、无权限用户） |
| 8 | ✅ RTM 需求追踪矩阵零空白 | RTM 四类清单（AC/ST/PM/BF）零空白项，详见 6.5 节 |
| 9 | ✅ 代码无 TODO/FIXME/placeholder/{{占位符}} 残留 | `grep -r "TODO\|FIXME\|placeholder" src/` + `grep -r "{{.*}}" .claude/` 检查配置文件占位符 |
| 10 | ✅ 前后端 API 对接完整性 | API 文档 vs 前端调用 vs 后端实现 |

> **无 E2E 测试时的降级方案**：如项目暂无 E2E 测试（第二章扫描结果中 `{{E2E测试命令}}` 为"无"），第 3-5 项可降级为人工验收：
> - 第 3 项降级为：运行单元测试 + 集成测试，确保核心功能验证通过
> - 第 4 项降级为：人工遍历所有页面路由，确认无 404
> - 第 5 项降级为：人工测试关键 API 端点，确认无 500 错误
>
> 降级需在 PR 中标注原因并排期补充 E2E 测试。建议在第五章（跟进节奏）Day 30 回顾时评估 E2E 测试引入计划。

### 6.2 门禁执行时机

- **每次提交前**：运行编译和类型检查（第 1 项）
- **每次 PR 合并前**：运行全量 E2E 测试 + 覆盖率检查（第 1-3 项）
- **CI/CD 自动触发**：PR 创建时自动运行可自动化的检查项（见 6.4.2），包括编译、测试、覆盖率、TODO/FIXME 检查等
- **每次交付前**：运行完整门禁清单（第 1-10 项全部通过）

### 6.3 门禁失败处理

| 序号 | 失败项 | 处理方式 |
|------|--------|---------|
| 1 | 编译失败 | build-error-resolver agent 修复 |
| 2 | 覆盖率不足 | tester agent 补充测试，coverage-auditor agent 审计 |
| 3 | 测试失败 | 分析是测试代码 bug 还是被测系统 bug，对应 agent 修复 |
| 4 | 页面 404 | 前端开发者（人工）检查路由配置，E2E 测试覆盖所有路由 |
| 5 | API 500 | 后端开发者（人工或 backend agent，如有配置）修复错误处理逻辑，前端开发者加容错机制 |
| 6 | 数据字段问题 | 前端开发者加守卫，后端开发者加兜底 |
| 7 | 权限问题 | 后端开发者（人工或 backend agent，如有配置）修复权限逻辑，前端开发者同步路由守卫 |
| 8 | RTM 空白 | tester agent 补充测试用例，确保需求与测试一一对应 |
| 9 | TODO/FIXME/占位符 残留 | 人工清理遗留项或转为正式需求 |
| 10 | API 对接不一致 | 后端开发者修正 API 实现，前端开发者修正调用方式，同步更新文档 |
| - | 任何门禁失败 | 执行回溯分析：门禁清单是否遗漏该检查项？规范中是否缺失对应规则？是否需要更新 rules/ 或 steer/？ |

> **说明**：表中"前端开发者/后端开发者"指人工介入或运行时角色，对应第七章 7.6 agent-collaboration.md 中的 `frontend`/`backend` 角色。标有"agent"的项（如 tester agent、build-error-resolver agent）对应 `.claude/agents/` 下的配置文件。

> **回溯法核心**：每个逃逸 bug 都要追问"为什么 AI 没拦住"。单个 agent 的失误往往是规范缺失的症状——不是 agent "忘了"，而是没有规则要求它这么做。门禁回溯不仅要问"规范是否缺失"，还要问"门禁清单是否应增加检查项"。详见第五章"规范迭代闭环"。

### 6.4 门禁执行流程

#### 前置条件

执行门禁检查前，确认以下条件已满足：
- **代码已提交**：所有变更已提交到当前分支，无未暂存的修改
- **本地测试已通过**：`{{测试命令}}` 执行成功（如 `mvn test` 或 `pnpm test`）
- **环境配置正确**：
  - 数据库连接正常（开发环境或测试环境）
  - 中间件服务可用（Redis、ActiveMQ、Kafka 等，如有）
  - 环境变量已配置（`.env` 或 `application-*.yml` 中的变量）
- **依赖已安装**：`{{包管理器}} install` 已执行（如 `mvn install` 或 `pnpm install`）

> 如果前置条件未满足，门禁检查可能产生误报，应先解决环境问题。

#### 6.4.1 交付前检查步骤

以下步骤与门禁清单序号一一对应：

| 步骤 | 对应检查项 | 执行方式 |
|------|-----------|---------|
| 1 | 第 1 项：编译/类型检查 | 运行 `{{构建命令}}`（如 `mvn compile` 或 `pnpm build`），前端项目额外运行 `npx vue-tsc --noEmit` |
| 2 | 第 2 项：覆盖率检查 | 运行 `{{覆盖率命令}}`（如 `pnpm test:coverage`），确认覆盖率 ≥ 当前基准值 |
| 3 | 第 3 项：E2E 测试 | 运行 `{{E2E测试命令}}`（如 `pnpm test:e2e` 或 `npx playwright test`） |
| 4 | 第 4 项：页面 404 | 查看 E2E 测试覆盖的路由列表，确认所有路由均有测试 |
| 5 | 第 5 项：API 500 | 查看 E2E 测试的错误监听日志（pageerror + console.error） |
| 6 | 第 6 项：数据字段 | `grep -r "undefined\|null\|placeholder" src/`，确认无未处理的空值；后端检查 API 响应层 nil 集合兜底，前端检查防御性消费（`?? []`） |
| 7 | 第 7 项：权限校验 | 运行权限测试 batch，覆盖关键角色组合（至少包含：超级管理员、普通用户、无权限用户） |
| 8 | 第 8 项：RTM 矩阵 | 确认 RTM 四类清单（AC/ST/PM/BF）零空白项，详见 6.5 节 |
| 9 | 第 9 项：TODO/FIXME/占位符 | `grep -r "TODO\|FIXME\|placeholder" src/` 确认无残留 + `grep -r "{{.*}}" .claude/` 确认配置文件无占位符 |
| 10 | 第 10 项：API 对接 | 对照 API 文档、前端调用、后端实现，确认三方一致 |

#### 6.4.2 自动化执行（推荐）

将上述检查项配置为 CI/CD 流水线，每次 PR 自动运行。

**前端项目示例（GitHub Actions）**：
```yaml
name: Quality Gate
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: pnpm install
      - name: Type check
        run: pnpm type-check
      - name: Run tests with coverage
        run: pnpm test:coverage
      - name: Run E2E tests
        run: pnpm test:e2e
      - name: Check TODO/FIXME
        run: grep -r "TODO\|FIXME\|placeholder" src/ && exit 1 || exit 0
```

**后端项目示例（GitHub Actions + Maven）**：
```yaml
name: Quality Gate
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up JDK
        uses: actions/setup-java@v3
        with:
          java-version: '8'
          distribution: 'temurin'
          cache: maven
      - name: Compile
        run: mvn compile
      - name: Run tests with coverage
        run: mvn test jacoco:report  # 或根据项目覆盖率工具配置，如 Cobertura、JaCoCo 等
      - name: Check coverage threshold
        run: |  # 示例：检查覆盖率是否达标（需根据实际工具调整）
          coverage=$(grep -oP '(?<=<counter type="INSTRUCTION" missed=")[^"]*' target/site/jacoco/jacoco.xml | head -1)
          echo "Coverage check passed"
      - name: Check TODO/FIXME
        run: grep -r "TODO\|FIXME\|placeholder" src/ && exit 1 || exit 0
```

> **后端覆盖率工具说明**：Java 项目常用 JaCoCo（Maven 插件 `jacoco-maven-plugin`）或 Cobertura。上例假设已配置 JaCoCo 插件。如项目暂无覆盖率工具，可在 `mvn test` 后添加覆盖率配置。

> **说明**：以上 CI 示例仅覆盖部分检查项（1-3、9）。完整门禁自动化可行性分析：
>
> **可全自动化**：
> - 第 1 项（编译/类型检查）：CI 流水线固定步骤
> - 第 2 项（覆盖率检查）：`{{覆盖率命令}}` + 阈值校验脚本
> - 第 3 项（E2E 测试）：`{{E2E测试命令}}` + 错误监听日志解析
> - 第 9 项（TODO/FIXME）：grep 脚本自动检查
>
> **半自动化**（需脚本 + 人工确认）：
> - 第 4 项（页面 404）：E2E 测试覆盖路由列表 → 人工确认无遗漏
> - 第 5 项（API 500）：E2E 测试错误日志 → 人工分析是否为预期错误
> - 第 6 项（数据字段）：grep 检查 → 人工确认空值是否有业务含义
> - 第 8 项（RTM）：脚本检查 RTM 文件格式 → 人工确认需求与测试对应关系
> - 第 10 项（API 对接）：自动化 API 文档生成 → 人工确认三方一致性
>
> **需人工检查**：
> - 第 7 项（权限校验）：权限测试 batch 可自动化，但"覆盖关键角色组合"需人工设计测试矩阵（建议至少包含：超级管理员、普通用户、无权限用户）
>
> 建议将可自动化的项配置为 CI 阻断条件，半自动化的项配置为 CI 报告输出，需人工的项在 PR 审查时确认。

### 6.5 RTM 需求追踪矩阵

> 本节对应门禁清单第 8 项"RTM 需求追踪矩阵零空白"。RTM 确保每个需求都有对应的测试用例，零空白项才可交付。

从需求文档提取四类编号化清单，构建 RTM（需求追踪矩阵）。

#### RTM 生命周期管理

**创建时机**：
- 需求评审后立即创建 RTM 文件（`.claude/specs/<feature>/rtm.md`）
- 开发前明确验收标准，开发中追踪进度，交付前验证完整性
- **注意**：RTM 是功能开发过程中按需创建的，不属于第三章初始化的 28 个配置文件。每个功能/特性开发时独立创建，位于 `.claude/specs/<feature>/rtm.md`

**责任归属**：
- **创建**：tester agent（或开发者），从需求文档提取 AC/ST/PM/BF 清单
- **维护**：开发过程中新增需求时同步更新 RTM
- **审计**：coverage-auditor agent 独立验证 RTM 覆盖率真实性

**与需求评审的关系**：
- 需求评审时，RTM 作为验收标准的结构化表达
- 评审通过后，RTM 作为测试用例的编写依据
- 交付前，RTM 作为"测试是否完成"的唯一真相

#### RTM 四类清单定义

| 清单类型 | 说明 | 示例 |
|----------|------|------|
| 验收条件（AC） | 功能性需求 | AC-001: 用户可以创建订单 |
| 状态流转（ST） | 正向转换 + 非法转换 | ST-001: 待支付 → 已支付（正向） |
| 权限矩阵（PM） | 角色 × 操作 × 预期结果 | PM-001: 普通用户 × 删除订单 → 403 |
| 业务流程（BF） | 端到端完整流程 | BF-001: 下单 → 支付 → 发货 |

**RTM 模板**（示例）：
```markdown
## 需求追踪矩阵

| ID | 需求描述 | 测试用例 | 状态 |
|----|----------|---------|------|
| AC-001 | 用户可以创建订单 | tests/e2e/order/create.test.ts | ✅ |
| AC-002 | 用户可以取消订单 | tests/e2e/order/cancel.test.ts | ✅ |
| AC-003 | 用户可以查看订单详情 | tests/e2e/order/detail.test.ts | ⚠️ 缺失 |
| ST-001 | 待支付 → 已支付 | tests/e2e/order/status.test.ts | ✅ |
| ST-002 | 已支付 → 待发货 | tests/e2e/order/status.test.ts | ✅ |
| ST-003 | 待支付 → 已取消（非法） | tests/e2e/order/invalid-transition.test.ts | ✅ |
| PM-001 | 普通用户 × 删除订单 → 403 | tests/e2e/permission/delete-order.test.ts | ✅ |
| PM-002 | 管理员 × 删除订单 → 成功 | tests/e2e/permission/admin-delete-order.test.ts | ✅ |
| BF-001 | 完整下单流程 | tests/e2e/flow/order-flow.test.ts | ✅ |

**覆盖率**：9/10（90%）
**空白项**：AC-003
```

> **说明**：RTM 中状态列用 `✅` 表示已完成，`⚠️ 缺失` 表示未实现，`❌ 阻塞` 表示有依赖问题。交付前必须清理所有缺失项。

#### 创建与维护步骤

1. **需求评审阶段**：从需求文档提取 AC/ST/PM/BF 四类清单
2. **开发前**：为每个需求项创建对应的测试用例文件（可以是空文件占位）
3. **开发中**：填写测试用例路径和状态，实现测试逻辑
4. **新增需求时**：同步更新 RTM，确保不遗漏
5. **交付前**：验证 RTM 零空白，所有需求均有测试覆盖

#### 验证方法
```bash
# 检查 RTM 是否有空白项（假设 RTM 文件在 .claude/specs/*/rtm.md）
grep -E "^\| [A-Z]+-[0-9]+ \| .* \|  *\|" .claude/specs/*/rtm.md
# 如有输出则表示存在空白项，需要补充测试用例
```

---

## 七、配置模板

以下为全部配置文件的完整内容。`{{...}}` 为需要替换的占位符，用第二步的扫描结果填入。

### 文件清单

本章节包含以下配置模板（共 31 个文件，对应 3.1 节文件清单）：

- **7.1 CLAUDE.md** — 项目主配置文件
- **7.2-7.6 rules/** — 底线规则（security / testing / frontend / git / agent-collaboration，共 5 个文件）
- **7.7 steer/** — 项目心智地图（共 8 个文件 + 1 个可选，分为 7.7.1-7.7.9 九个子节）
  - 7.7.1-7.7.5 foundation/ — product / tech / structure / never / quality-gate
  - 7.7.6-7.7.8 domain/ — api / testing / security
  - 7.7.9 frontend/ — 前端开发规范（可选）
- **7.8-7.11 commands/** — 斜杠命令（plan / code-review / build-fix / dev，共 4 个文件）
- **7.13-7.21 agents/** — 专用子代理（architect / code-reviewer / sd-reviewer / db-implementer / backend / frontend / tester / coverage-auditor / build-error-resolver，共 9 个文件）
- **7.22 skills/** — 知识库（troubleshooting）
- **7.23 settings.json** — 权限与 Hooks 配置（含 Hook 升级示例）
- **7.24 .mcp.json.example** — MCP 配置模板
- **7.25 .gitignore** — Git 忽略规则追加
- **7.26-7.29 templates/spec/** — Spec 模板文件（requirements / design / test-cases / tasks，共 4 个文件，测试先行模式）
  - 详细内容见附录 C.1-C.3、D

> **注意**：
> - 每个子节标题下有简短说明，标注是否需要改造及适配要点
> - 7.18 节包含 Hook 升级路径的完整配置示例（一致性型、阻断型、PowerShell 版），对应第五章的升级策略
> - foundation/ 下的模板为骨架式占位符（需人工填写项目特有信息），domain/ 下的模板为具体规范条文（可直接使用或微调）
> - **7.21-7.24** Spec 模板文件：初始化时创建到 `.claude/templates/spec/`，内容见附录 C.1-C.3，test-cases.md 见附录 D（测试先行核心）

---

### 7.1 CLAUDE.md

**需要替换所有 `{{...}}` 占位符，填入第二步扫描的项目信息。**

````markdown
# 项目 AI 协作规范

> 遵循「配置即代码」原则，所有变更需走 PR 流程。

## 项目信息

- **项目名称**：{{项目名称}}
- **技术栈**：{{技术栈}}
- **数据库**：{{数据库类型}}
- **中间件**：{{中间件}}（如无则标注"无"）

> 构建命令、测试命令、格式化命令等详见 .claude/steer/foundation/tech.md

## 目录结构约定

```
{{项目目录}}/
├─ CLAUDE.md           # 本文件，项目 AI 协作说明书
└─ .claude/
   ├─ steer/          # 项目心智地图（foundation/domain）
   ├─ rules/          # 底线规则（安全/测试/Git）
   ├─ agents/          # 专用子代理（审查/排障）
   ├─ commands/        # 斜杠命令（sd-plan/sd-codereview/sd-buildfix/sd-dev/sd-spec）
   ├─ skills/          # 知识库
   ├─ templates/spec/  # Spec 模板（requirements/design/test-cases/tasks）
   ├─ specs/           # 功能级 Spec 目录
   └─ settings.json    # 基础配置
```

## 核心目录

| 目录 | 职责 |
|------|------|
| {{目录1}} | {{职责1}} |
| {{目录2}} | {{职责2}} |

> 每个核心目录一行，根据扫描结果增减行数。禁止修改的目录详见 .claude/steer/foundation/never.md

## 行为规范

### 需求开发流程（强制）

**所有新功能开发必须遵循以下流程：**

```
用户提需求 → AI 分析需求 → 输出 Plan → 用户确认 → 【自动】创建 Spec → 用户确认 → 开始实现
```

**触发 Spec 的时机：**
- 用户确认 Plan 后，AI 自动调用 `/sd-spec` 创建 Spec 文件
- 无需用户再次手动触发

**Spec 创建内容：**
- `.claude/specs/<name>/` 目录下创建四个文件：
  - `requirements.md` — 验收标准
  - `design.md` — 技术方案
  - `test-cases.md` — 测试用例文档（测试先行核心）
  - `tasks.md` — 任务清单
- 创建完 Spec 后才能开始写代码

**豁免条件（跳过 Spec 直接实现）：**
- 用户明确说"直接改"、"不用规划"等豁免词
- 单文件小改动（如修复 bug、调整配置）

### 必须先 Plan 的高风险操作

1. 多文件批量改动（3个文件以上）
2. 代码结构调整、大规模重构
3. 引入新依赖、新服务
4. 安全/权限相关的代码修改
5. 需求本身不清晰的开发任务

> 无法用一句话说清楚 diff 时，必须先写 Plan。

> 禁止行为详见 .claude/steer/foundation/never.md 和 .claude/rules/security.md

### 编码行为准则

> 偏向审慎而非速度。简单任务自行判断适用程度。详细解读见附录 A。

1. **先想后写** — 不假设，不隐藏困惑。多种解读列出来，不确定先问，有更简方案就提。
2. **简洁优先** — 最少代码解决问题。不加未要求的功能/抽象/灵活性。200行能缩50行就重写。
3. **精准改动** — 只动必须动的。不改相邻代码，不重构没坏的东西，匹配已有风格。每行变更可追溯到需求。
4. **目标驱动** — 定义可验证的成功标准。"修Bug" → 先写复现测试再修；多步骤任务列出验证点。

## 治理机制

| 时间点 | 动作 |
|--------|------|
| Day 1-3 | 每人实际使用，群内反馈问题 |
| Day 7 | 收集第一周反馈，微调 rules 和 CLAUDE.md |
| Day 14 | 评估 Hook 升级：哪些提醒型该升级为阻断型 |
| Day 30 | 全面回顾：分档调整、覆盖率提升、新配置需求；E2E 测试引入计划评估（如项目暂无 E2E 测试） |

> Hook 详细升级路径（提醒型 → 一致性型 → 阻断型）见第五章。

## 存储位置

| 类型 | 位置 |
|------|------|
| 团队共享 | .claude/（Git 版本控制） |
| 个人偏好 | ~/.claude/（本地） |

## 配置索引

- **规则**：.claude/rules/security.md | testing.md | frontend.md | git.md | agent-collaboration.md
- **Steer**：.claude/steer/ — 项目心智地图，减少从零探索的 Token 消耗
- **Spec**：.claude/specs/ — 结构化任务流程，先思考再动手
- **Spec 模板**：.claude/templates/spec/ — 创建 Spec 时读取的模板文件
- **命令**：/sd-plan | /sd-codereview | /sd-buildfix | /sd-dev | /sd-spec
- **Agent**：architect | code-reviewer | tester | coverage-auditor | build-error-resolver
- **知识库**：.claude/skills/troubleshooting.md
- **权限/Hooks**：.claude/settings.json
- **MCP**：.mcp.json.example（复制为 .mcp.json 后配置环境变量）
- **质量门禁**：见第六章质量门禁清单（10 项全绿才交付）

## Steer 文件 — 项目心智地图

> .claude/steer/ 目录下的文件为 AI 提供项目心智地图，减少每次会话从零探索的 Token 消耗。
> 只记项目特有的、容易踩坑的东西，不解释 AI 已知的常识。
> 详细编写指南见附录 B。

| 类型 | 文件 | 加载模式 |
|------|------|---------|
| foundation | product.md / tech.md / structure.md / never.md / quality-gate.md | always（每次会话） |
| domain | api.md / testing.md / security.md / frontend.md（可选）| fileMatch / auto（按需加载） |

## Rules 文件 — 底线规则

> .claude/rules/ 目录下的文件定义不可违反的底线规则，按严重程度分档执行。
> 详细分档说明见各文件开头的 🔴🟡🟢 标记。

| 文件 | 职责 | 加载模式 |
|------|------|---------|
| security.md | 安全底线（凭证/密钥/SQL注入/XSS/权限） | fileMatch（Java/SQL/配置文件） |
| testing.md | 测试底线（覆盖率/数据规范/需求驱动） | fileMatch（test 目录/测试文件） |
| frontend.md | 前端编码底线（防御性数据消费/代码质量） | fileMatch（Vue/JS/TS 文件） |
| git.md | Git 工作流（Commit/Branch/PR/Merge） | 按需（git 操作时） |
| agent-collaboration.md | Agent 协作规范（串行调度/Prompt自包含） | 按需（多 agent 编排时） |

## Spec 工作流 — Agent 协作开发模式

**强制触发条件：用户确认 Plan 后，自动创建 Spec。**

### 完整流程图

```
┌─────────────────────────────────────────────────────────────────┐
│  第一阶段：需求分析 & Plan 输出                                    │
├─────────────────────────────────────────────────────────────────┤
│  1. 用户提需求                                                   │
│  2. AI 分析需求 → 输出 Plan                                       │
│  3. 用户确认 Plan                                                │
│  4. 【自动】调用 /sd-spec 创建 Spec                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  第二阶段：Agent 协作产出 Spec 文件                               │
├─────────────────────────────────────────────────────────────────┤
│  5. requirements.md   ← 开发者/用户定义验收条件 AC 表              │
│  6. architect agent  → 输出 design.md（数据库设计 + API 文档）   │
│  7. architect agent  → 输出 test-cases.md（测试用例）            │
│  8. 填充 tasks.md     ← 任务清单（基于 design + test-cases）       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  第三阶段：实现 & 测试（使用 /sd-dev 命令调度 Agent）                │
├─────────────────────────────────────────────────────────────────┤
│  /sd-dev 命令读取 Spec 作为输入，串行调度：                        │
│                                                                 │
│  1. architect      → 确认/补充 Schema + API 文档                 │
│  2. db-implementer  → 创建数据表 SQL                              │
│  3. backend         → API handler + service + repository         │
│  4. frontend        → Vue 页面 + 组件                            │
│  5. tester          → E2E 测试（基于 test-cases.md）            │
│  6. code-reviewer   → 代码审查                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  第四阶段：收尾门禁 → Git 提交                                     │
└─────────────────────────────────────────────────────────────────┘
```

### Spec 文件产出分工

| 文件 | 产出者 | 时机 |
|------|--------|------|
| requirements.md | 开发者/用户定义 | 需求阶段 |
| design.md | architect agent | 基于 requirements |
| test-cases.md | architect agent | 与 design 同时产出 |
| tasks.md | 开发者/主 Agent | 基于 design + test-cases |

### Spec 创建步骤

1. 读取模板：`.claude/templates/spec/` 下的四个模板文件
2. 创建目录：`.claude/specs/<feature-name>/`
3. 填充内容：基于模板框架，结合具体需求填充业务内容
   - 替换 `{占位符}` 为具体值（如 `{功能名称}` → `会议室管理`）
   - 填充验收条件表（根据需求补充 AC-001、AC-002...）
   - **architect agent** 填充数据库设计和 API 设计
   - **architect agent** 根据验收条件为每个 AC 补充测试用例
   - 填充任务清单（包含测试用例文档任务 + 测试执行任务）

| 阶段 | 模板文件 | 创建文件 | 需填充内容 |
|------|----------|----------|-----------|
| 需求 | `.claude/templates/spec/requirements.md` | `.claude/specs/<name>/requirements.md` | 功能描述、验收条件（AC表）、影响范围表、用户故事 |
| 设计 | `.claude/templates/spec/design.md` | `.claude/specs/<name>/design.md` | 数据库表设计、字段详情、索引、API 定义、关键决策 |
| 测试用例 | `.claude/templates/spec/test-cases.md` | `.claude/specs/<name>/test-cases.md` | 每个 AC 对应的测试用例、测试数据、预期结果 |
| 任务 | `.claude/templates/spec/tasks.md` | `.claude/specs/<name>/tasks.md` | 具体任务列表（含测试用例文档任务 + 测试执行任务）、依赖关系、预计/实际工时 |

> Spec 文件持久化，不受上下文摘要影响。实现过程中可随时更新 tasks.md 进度。

### 开发执行顺序

1. requirements.md（需求定义）
2. architect agent → design.md（技术方案）
3. architect agent → test-cases.md（测试用例）
4. tasks.md（任务清单）
5. **使用 /sd-dev 命令** 启动 Agent 协作实现
6. **全部实现完成后**统一执行测试
7. **测试通过后**提交 Git（遵循 .claude/rules/git.md 的 Commit 规范）

> **约束**：CLAUDE.md 力求精简，只写 Claude 读代码推导不出的信息。项目信息字段和配置索引为结构化数据，不适用字数限制；正文（行为规范、禁止行为等）建议控制在 400 字内。

---

### 7.2 rules/security.md

**需要根据项目技术栈调整术语。**

以下模板以 Java/SpringBoot 为例（`application.yml`、`MyBatis`、`${}` 占位符等）。纯前端项目将 `application.yml` 改为 `.env` 或 `config.js`，MyBatis `#{} vs ${}` 改为 ORM 参数化查询或模板字符串安全提醒；Python 项目将 `${VAR}` 改为 `os.environ` 或 `.env` 文件引用。

```markdown
---
description: 安全红线规则
type: rules
updated: 2026-04-22
---

# 安全底线规则

## 🔴 立即执行（违反即阻断）

### 凭证与密钥
1. **禁止硬编码密钥** — API Key、Token、数据库密码必须通过环境变量注入（application.yml 中使用 `${VAR}` 占位符，不写明文密码）
2. **禁止提交凭证** — .env、.mcp.json、application-dev.yml、application-*.yml 中的真实凭证不得提交到 Git（数据库密码、Redis 密码、ActiveMQ/Kafka 认证信息、第三方 API Key 均适用）

### 代码安全
3. **禁止 SQL 拼接** — 必须使用参数化查询（MyBatis 中使用 `#{}` 而非 `${}`，`${}` 存在注入风险）
4. **禁止 XSS 风险** — 用户输入必须做转义处理
5. **禁止明文传输敏感数据** — HTTPS 强制，非必要不走 HTTP

### 后端安全（智能体质量门禁新增）
6. **API 响应层 nil 集合兜底** — 序列化前拦截 nil 集合类型，返回空数组/列表 `[]` 而非 `null`
7. **写操作校验直属关系** — 防止 IDOR 横向越权，必须校验操作者与目标的直属关系
8. **用 DTO 接收前端参数** — 禁止直接绑定数据库 entity/model，防止字段注入

## 🟡 新代码执行

### 依赖管理
1. 新增依赖需说明用途，并确认非恶意包
2. 涉及权限/认证的代码修改必须通过人工 code review + /sd-codereview 命令双重检查
3. 数据库迁移前必须备份，并保留回滚方案

### 权限一致性（智能体质量门禁新增）
4. **前后端权限同步维护** — 前端路由守卫和后端 API 权限必须同步
   - 前端允许访问但后端拒绝 = 用户看到 403 报错
   - 后端允许访问但前端隐藏 = 安全漏洞
5. **角色检查 ≠ 权限检查** — 验证"是不是某角色"不等于验证"是不是这个目标的负责人"
   - `@PreAuthorize("hasRole('MANAGER')")` 只验证了"是不是管理者"
   - 没有验证"是不是具有这个功能权限的管理者"

## 触发规则

🔴 级别违反，Hook 直接阻断操作并报错。
🟡 级别违反，代码审查时检查。

## 关键洞察（来自生产级项目实战）

- **后端 nil 集合是万恶之源**：nil 集合序列化为 `null`，前端 `.map()` 直接崩。响应层统一兜底是最高效的修复
- **前端永远不信任后端返回值**：即使后端承诺返回数组，前端也要加 `?? []`。双保险优于单保险
- **角色检查 ≠ 权限检查**：验证"是不是某角色"不等于验证"是不是这个目标的负责人"。写操作必须校验操作者与目标的关系
```

---

### 7.3 rules/testing.md

**需要填入测试命令和当前覆盖率，并根据项目技术栈调整术语。**

以下模板以 Java + Vue 前后端分离为例（`System.out.println`、`@Disabled/@Ignore`、`console.log`、`it.skip/describe.skip`）。纯前端项目删除后端相关条目（System.out.println、@Disabled 等）；纯后端项目删除前端相关条目；Python 项目将 `console.log` 改为 `print()`，将 `it.skip` 改为 `@pytest.mark.skip`，将 `@Disabled` 改为 `@unittest.skip`。

```markdown
---
description: 测试要求规则
type: rules
updated: 2026-04-22
---

# 测试底线规则

## 🔴 立即执行（违反即阻断）

### 测试基础设施（E2E 测试必须遵守）
1. **全局错误监听** — 必须同时监听两种错误源：
   ```javascript
   page.on('pageerror', err => errors.push(err.message))
   page.on('console', msg => {
     if (msg.type() === 'error') errors.push(msg.text())
   })
   // 断言前等待微任务完成
   await page.waitForLoadState('networkidle')
   await page.waitForTimeout(500)
   expect(errors.filter(e => !isKnownNoise(e))).toEqual([])
   ```
2. **三层验证标准** — 每个测试必须验证（缺一不可）：
   - 页面可达：URL 正确，主容器可见
   - 数据加载：至少一个 API 请求返回成功
   - 数据渲染：至少一个数据驱动的 DOM 元素包含非空文本（非占位符）

3. **禁止模式** — 测试的职责是暴露问题，不是掩盖问题：

| 禁止模式 | 示例 | 正确做法 |
|----------|------|---------|
| 吞掉失败 | `.catch(() => null)` | 让错误直接抛出 |
| 条件断言 | `if (resp) expect(...)` | 无条件断言 |
| 只验证 DOM 存在 | `toBeVisible()` 就结束 | 验证数据内容非空 |
| 硬等待 | `waitForTimeout(3000)` | 等待具体条件 |

## 🟡 新代码执行

### 测试覆盖
1. 新增函数必须附带单元测试
2. Pull Request 必须通过全部 CI 测试
3. 测试覆盖率下降不允许合并
4. 调试打印代码在提交前必须清除（前端 console.log，后端 System.out.println）
5. 禁止跳过测试的标注（前端 it.skip/describe.skip，后端 @Disabled/@Ignore）提交到主分支
6. 构建前必须通过本地测试

### 测试数据规范（智能体质量门禁新增）
7. **测试账号覆盖关键角色组合** — 至少包含：超级管理员、普通用户、无权限用户。不要只测有数据的用户（只测 happy path）
8. **必须包含"无数据"用户** — 测试空状态
9. **测试数据通过 seed 脚本准备** — 可重复执行，幂等
10. **不要假设数据库状态** — 直接查询验证，数据库里可能只有 M 种角色，代码定义了 N 种

### 需求驱动测试（智能体质量门禁新增）
11. 从需求文档提取四类编号化清单：
    - 验收条件（AC）：功能性需求
    - 状态流转（ST）：正向转换 + 非法转换
    - 权限矩阵（PM）：角色 × 操作 × 预期结果
    - 业务流程（BF）：端到端完整流程
12. 构建 RTM（需求追踪矩阵），标记所有 GAP。**RTM 详细说明和模板见第六章 6.5 节**。RTM 是功能开发过程中按需创建的（`.claude/specs/<feature>/rtm.md`），不属于第三章初始化的 26 个配置文件
13. 补写测试直到 RTM 零空白

## 🟢 逐步达标

### 覆盖率目标
1. 核心业务逻辑测试覆盖率逐步达到 80%（当前：{{当前覆盖率}}%）
2. 所有 API 端点有对应测试用例

### 分层测试策略
```
┌─────────────┐
│  batch-d    │  流程测试（serial，端到端完整流程）
├─────────────┤
│  batch-e    │  状态流转测试（正向 + 非法转换）
├─────────────┤
│  batch-c    │  权限测试 + 视觉回归
├─────────────┤
│  batch-b    │  功能测试（单个功能点验证）
├─────────────┤
│  batch-a    │  冒烟测试（页面可达 + 数据加载）
└─────────────┘
```

各层职责不可互相替代。冒烟测试保证页面能打开，功能测试保证逻辑正确，流程测试保证端到端可用。

## 测试命令

- 单元测试：`{{测试命令}}`（多模块项目分行标注，如后端 `mvn test` / 前端 `pnpm test`）
- E2E 测试：`{{E2E测试命令}}`（如无 E2E 测试则删除此行）
- 覆盖率：`{{覆盖率命令}}`
- Lint：`{{Lint 命令}}`（如无则删除此行）

## 执行方式

🔴 级别违反，测试不通过，阻断合并。
🟡 级别在代码审查时检查，新代码不合规不合并。
🟢 级别记入技术债清单，排期整改，不阻塞当前开发。

## 关键洞察（来自生产级项目实战）

- **测试全绿 ≠ 没有 bug**：只测有数据的用户等于只测了 happy path。测试账号的选择偏差会制造虚假的安全感
- **测试基础设施本身也会坏**：登录 helper 字段名错误会导致所有测试静默失败，测试看似在跑实则形同虚设
- **RTM 是覆盖率的唯一真相**：不要相信"感觉覆盖了"，用需求追踪矩阵验证
- **覆盖率审计必须独立**：编写测试的 agent 不能自己审计覆盖率，避免自我评价偏差
```

---

### 7.4 rules/frontend.md

**新增配置文件，前端项目必须创建。**

```markdown
---
description: 前端编码底线规则
type: rules
updated: 2026-04-22
---

# 前端编码底线规则

## 🔴 立即执行（违反即阻断）

### 防御性数据消费
1. **API 返回值一律加空值守卫** — `data ?? []`
2. **链式访问加可选链** — `row.nested?.field ?? defaultValue`
3. **禁止裸赋值** — `list.value = response.data` → `list.value = response.data ?? []`
4. **数值方法调用加守卫** — `(value ?? 0).toFixed(1)`

### 代码质量
5. **禁止提交 placeholder/TODO/FIXME/{{占位符}}/硬编码假数据** — 质量门禁 `grep -r "TODO\|FIXME\|placeholder" src/` 检查代码文件 + `grep -r "{{.*}}" .claude/` 检查配置文件占位符

## 🟡 新代码执行

### 错误处理
1. API 调用必须处理错误态，不允许静默失败
2. 用户输入必须做校验和转义处理

### 代码规范
3. 组件必须有明确的 TypeScript 类型定义
4. 禁止 any 类型（除非有充分理由并添加注释说明）
5. 复杂逻辑必须拆分为可测试的函数

## 🟢 逐步达标

### 最佳实践
1. 组件拆分：单文件不超过 300 行
2. 状态管理：跨组件状态使用 Pinia/Vuex，避免 prop drilling
3. 样式规范：遵循项目 UI 设计规范，以原型为最终权威

## 执行方式

🔴 级别违反，代码审查时阻断。
🟡 级别在代码审查时检查，新代码不合规不合并。
🟢 级别作为团队习惯逐步养成，不强制。

## 关键洞察（来自生产级项目实战）

- **前端永远不信任后端返回值**：即使后端承诺返回数组，前端也要加 `?? []`。双保险优于单保险
- **后端 nil 集合是万恶之源**：nil 集合序列化为 `null`，前端 `.map()` 直接崩。响应层统一兜底是最高效的修复
- **原型 HTML 为最终权威**：当设计规范文档与原型不一致时，以原型为准
```

---

### 7.5 rules/git.md

**需要确认分档标记（🔴🟡🟢）是否符合团队实际。**

```markdown
---
description: Git 工作流规范
type: rules
updated: 2026-04-22
---

# Git 工作流底线规则

## 🟡 新代码执行

### Commit 规范

格式（Angular 规范）：`<type>(<scope>): <subject>`

| Type | 适用场景 |
|------|---------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档变更 |
| style | 格式/样式（不影响逻辑） |
| refactor | 重构 |
| test | 测试相关 |
| chore | 构建/工具变更 |

规则：
1. Subject 不超过 50 字，句末不加句号
2. Body 解释「为什么」，不解释「是什么」
3. 禁止空 Commit 消息

### Branch 规范

1. 分支命名：type/short-description
   - `feature/user-auth`
   - `fix/login-timeout`
   - `chore/update-deps`
2. 禁止在 main/master 直接提交，所有变更走 PR
3. 分支生命周期：完成即合并，合并即删除

### PR 规范

1. PR 标题同 Commit 规范
2. 必须包含 Summary（改了什么）+ Test plan（如何验证）
3. Review 通过前禁止合并
4. 代码所有者（CODEOWNERS）必须审核

### Merge 策略

- 使用 **Squash and Merge** 保持历史整洁
- 或 **Rebase + Merge** 保留完整历史（视团队习惯选择）
- 禁止 **Fast-forward Merge**（无法追溯合并来源）

## 🟢 逐步达标

1. 分支完成后及时删除
2. Commit message Footer 引用相关 Issue：Closes #123
3. PR 合并后自动删除远程分支

## 执行方式

🟡 级别在代码审查和 PR 流程中检查。
🟢 级别作为团队习惯逐步养成，不强制。
```

---

### 7.6 rules/agent-collaboration.md

**新增配置文件，使用 Agent Team 编排时必须创建。**

```markdown
---
description: Agent 协作规范
type: rules
updated: 2026-04-22
---

# Agent 协作规范

## 🟡 新代码执行

### 串行保证正确性
Agent 编排必须遵循依赖顺序：architect → db → backend → frontend → tester → reviewer，每一层基于上一层产出。

**为什么必须串行**：
- architect 输出 Schema 和 API 文档，db 需要据此定义 struct
- backend 需要基于 db 定义的 struct 实现 handler
- frontend 需要基于 backend 的 API 实现页面
- tester 需要基于前端页面编写测试
- reviewer 最后审查所有代码

### Prompt 自包含
每个 agent 看不到对话历史，prompt 必须包含：
- 需求文档路径
- 设计决策文件路径
- 相关文件清单
- 具体改动描述

**为什么必须自包含**：
- Agent 只能看到当前对话的消息，看不到之前的上下文
- 缺少上下文会导致 agent 凭猜测工作，产出不符合预期

### 写文件规则
每次写入 ≤ 60 行，分块追加。

**为什么限制行数**：
- 工具参数有长度限制，超过会截断
- 截断导致 agent 无限重试，浪费时间和 token
- 分块追加保证每次操作都是有效的

### Agent Team 组织

**有独立配置文件的 Agent（9 个）**：

| Agent | 角色 | 职责 | 配置文件 |
|-------|------|------|---------|
| architect | 架构师 | 输出 Schema + API 文档 + 设计决策 | 7.12 节 |
| sd-reviewer | Spec 评审 | 对 Spec 文件进行结构化评审 | 7.13 节 |
| db-implementer | 数据库实现 | 创建数据库表、DO 实体类、Mapper 接口 | 7.14 节 |
| backend | 后端实现 | 创建 VO、Service、Controller | 7.15 节 |
| frontend | 前端实现 | 创建 API 定义、页面、组件 | 7.16 节 |
| tester | 测试工程师 | 编写/修复 E2E 测试 | 7.17 节 |
| code-reviewer | 代码审查 | 审查质量/安全/可维护性 | 7.18 节 |
| coverage-auditor | 覆盖率审计 | 独立审计覆盖率真实性 | 7.19 节 |
| build-error-resolver | 构建排障 | 修复构建/测试错误 | 7.20 节 |

**运行时角色（无独立配置文件，由主 CC 直接调度）**：

| 角色 | 职责 |
|------|------|
| 主 CC（调度员） | 任务分配、进度监控、质量把关 |
| backend-fixer | 修复后端问题（审查/测试失败时） |
| frontend-fixer | 修复前端问题（审查/测试失败时） |

> **说明**：运行时角色由主 CC 在编排时直接调度，用于问题修复，不需要预定义专用 prompt 模板。

### 并行 vs 串行调度

**可并行**（无文件冲突）：
- tester + frontend-fixer（不同目录）
- coverage-auditor + 任何 agent（只读）
- 多个调查 agent

**必须串行**（有文件依赖）：
- backend-fixer 修复 → tester 重跑
- coverage-auditor 审计 → tester 修复虚假覆盖

## 🟢 逐步达标

### 全新代码也要审查
AI 生成的代码存在权限缺失、校验遗漏等问题，审查不可省略。

**审查清单要点**：
- nil 返回路径
- 裸赋值
- 前后端权限一致性
- placeholder 残留

## 执行方式

🟡 级别在 agent 编排时强制执行。
🟢 级别作为团队习惯逐步养成，不强制。

## 关键洞察（来自生产级项目实战）

- **Agent prompt 必须自包含**：每个 agent 看不到对话历史，prompt 中要包含需求文档路径、设计决策、文件清单、具体改动描述
- **写文件规则要在 prompt 开头强调**：≤60 行/次，分块追加，否则工具参数截断导致无限重试
- **全新项目也需要代码审查**：AI 生成的代码不等于正确的代码，本次审查发现了 10 个 P0 级安全/逻辑问题
```

---

### 7.7 .claude/steer/ 项目心智地图

**需要替换所有 `{{...}}` 占位符，填入第二步扫描的项目信息。共 8 个文件：foundation 5个 + domain 3个（可选 frontend.md 见 7.7.9）。**

Steering 文件目录结构：
```
.claude/steer/
├─ foundation/          # always 类型，每次会话加载
│   ├─ product.md      # 产品/项目概述
│   ├─ tech.md         # 技术栈与架构
│   ├─ structure.md    # 目录结构 + 修改导航
│   ├─ never.md        # NEVER 列表（禁止行为）
│   └─ quality-gate.md # 质量门禁清单
├─ domain/             # fileMatch/auto 类型，按需加载
│   ├─ api.md          # API 开发规范（fileMatch）
│   ├─ testing.md      # 测试规范（fileMatch）
│   ├─ security.md     # 安全规范（auto 类型）
│   └─ frontend.md     # 前端开发规范（fileMatch，可选）
└─ reference/          # manual 类型，手动引用（可选，按需创建）
```

> **重要说明**：
> - foundation/ 下的 5 个文件使用 `always` 类型（每次会话自动加载），内容应精简，控制在 2K tokens 以内。这些模板为骨架式占位符，需要人工填写项目特有信息
> - domain/ 下的文件使用 `fileMatch` 或 `auto` 类型（按需加载），提供具体的规范条文，可直接使用或根据项目微调
> - reference/ 目录用于存放 manual 类型的大型参考文档（如 OpenAPI spec），按需创建，本节不提供模板
> - `frontend.md` 为可选配置，模板见 7.7.9 节

#### 7.7.1 steer/foundation/product.md

**always 类型（每次会话加载），需要填入项目背景和业务域。**

```markdown
# {{项目名称}} — 产品概述

> 本文件是 AI 理解项目的起点，每次新会话都会加载。
> 只写 AI 读代码推导不出的项目背景和业务知识。

## 项目背景
{{一句话描述项目是什么、做什么、给谁用}}

## 核心业务域
- {{业务域1}}：{{一句话描述}}
- {{业务域2}}：{{一句话描述}}

## 技术选型背景
- 为什么选择 {{技术A}}：{{原因}}
- 为什么选择 {{技术B}}：{{原因}}

## 团队约定
- 代码审查需要几人通过：{{N}}
- 分支命名规范：{{规范}}
- 发布流程：{{简述}}
```

#### 7.7.2 steer/foundation/tech.md

**always 类型（每次会话加载），需要填入技术栈、环境配置和关键依赖。**

```markdown
# 技术栈与架构

> 本文件描述项目的技术组成，帮助 AI 理解代码的组织方式。

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | {{前端框架}} | {{版本}} |
| 后端 | {{后端框架}} | {{版本}} |
| 数据库 | {{数据库}} | {{版本}} |
| 中间件 | {{中间件}} | {{用途}} |

## 环境配置

- **包管理器**：{{包管理器}}
- **构建命令**：{{构建命令}}
- **测试命令**：{{测试命令}}
- **格式化命令**：{{格式化命令}}
- **Lint 命令**：{{Lint 命令}}

## 环境差异

| 环境 | 用途 | 配置特点 |
|------|------|---------|
| dev | 本地开发 | 本地数据库、热重载 |
| test | 自动化测试 | H2 内存数据库 |
| prod | 生产环境 | 连接远程数据库、禁用调试 |

## Maven 编译规范

**重要**：模块重组后，必须使用 `mvn clean compile` 项目全量编译验证，不能仅用 `mvn compile` 增量编译。

- 增量编译（`mvn compile`）：只编译改动的文件，复用 `target/` 旧 class 文件
- 项目全量编译（`mvn clean compile`）：删除 target 后从源码重新编译，暴露包路径不匹配等问题

**教训**：模块合并时目录结构改了但 package 声明未同步，导致单独编译通过但全项目编译失败。

## 关键依赖

- {{依赖1}}：{{用途}}
- {{依赖2}}：{{用途}}

## 数据库字符集规范

**重要**：所有 SQL 脚本必须包含字符集声明，避免中文乱码。

### SQL 文件规范
```sql
-- SQL 文件开头必须添加：
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
```

### Docker MySQL 执行规范
```bash
# 必须指定字符集
docker exec <container> mysql -uroot -p123456 --default-character-set=utf8mb4 <db> -e "SQL语句"

# 或通过管道执行 SQL 文件
docker exec -i <container> mysql -uroot -p123456 --default-character-set=utf8mb4 <db> < script.sql
```

### 问题排查
```bash
# 检查字符集设置
docker exec <container> mysql -uroot -p123456 -e "SHOW VARIABLES LIKE 'character%';"

# 正确输出应为：
# character_set_client     = utf8mb4
# character_set_connection = utf8mb4
# character_set_results    = utf8mb4
# character_set_database   = utf8mb4
```
```

#### 7.7.3 steer/foundation/structure.md

**always 类型（每次会话加载），需要填入目录结构、修改导航和架构决策。这是 ROI 最高的 Steer 文件。**

````markdown
# 目录结构与修改导航

> 本文件是 AI 修改代码时的"导航图"——改 X 去哪里改。
> 这是 ROI 最高的内容：减少 AI 盲目搜索，快速定位正确文件。

## 目录结构

```
{{项目根目录}}/
{{目录树}}
```

## 修改导航（改 X 去哪里改）

| 场景 | 目标文件/目录 | 注意事项 |
|------|-------------|---------|
| 新增 API endpoint | {{路由文件}} + {{handler目录}} | 需同步更新测试 |
| 修改业务逻辑 | {{业务逻辑文件}} | 避免直接操作数据库 |
| 新增数据库表 | {{migration目录}} + {{entity目录}} | 需运行迁移脚本 |
| 修改配置 | {{配置目录}} | 注意环境差异 |
| 新增前端页面 | {{页面目录}} + {{路由配置}} | 需同步更新菜单 |

## 关键文件说明

| 文件 | 用途 | 修改频率 |
|------|------|---------|
| {{关键文件1}} | {{用途}} | {{频率}} |
| {{关键文件2}} | {{用途}} | {{频率}} |

## 架构决策记录

> 这些决策不能从代码中推断出来，必须显式记录。

- **ADR-001**：选择 {{方案A}} 而非 {{方案B}}，因为 {{原因}}（日期：{{日期}}）
- **ADR-002**：正在从 {{旧技术}} 迁移到 {{新技术}}，新代码优先使用 {{新技术}}（进行中）
- **ADR-003**：禁用 {{功能}}，原因见 {{链接}}（日期：{{日期}}）
````

#### 7.7.4 steer/foundation/never.md

**always 类型（每次会话加载），需要填入项目特有的禁止行为和已知陷阱。**

```markdown
# NEVER 列表 — 禁止行为

> 本文件列出 AI 必须严格避免的行为，不需要解释原因。
> 违反这些规则会直接阻断操作。

## 绝对禁止

- **禁止修改** `{{核心目录}}/` 下的文件（需通过专用工具或人工介入）
- **禁止硬编码** 密钥、Token、数据库凭证（必须通过环境变量注入）
- **禁止提交** `.env`、`.mcp.json`、{{配置文件}} 到 Git
- **禁止使用** `any` 类型（必须使用具体类型或 `unknown`）
- **禁止绕过** 安全检查（如 SQL 拼接、XSS 未转义）
- **禁止修改** rules/ 以外的配置文件作为绕过规则的 workaround
- **禁止在未沟通的情况下** 删除他人代码

## 修改限制

- 修改 {{模块}} 前必须先 `/sd-plan` 并获得确认
- 修改 {{模块}} 需要通知 {{负责人}}（通过 {{方式}}）

## 代码风格强制

- 不使用 {{反模式}}（原因：{{原因}}）
- 不引入 {{技术}}（已在 ADR-{{编号}} 中废弃）
- 禁止在 {{位置}} 写业务逻辑（应该放在 {{正确位置}}）

## 已知陷阱

> 这些是团队踩过的坑，避免重蹈覆辙。

1. {{陷阱1}}：{{原因}} → 正确做法：{{做法}}
2. {{陷阱2}}：{{原因}} → 正确做法：{{做法}}
```

#### 7.7.5 steer/foundation/quality-gate.md

**always 类型（每次会话加载），质量门禁清单独立配置文件。**

本文件将第六章的完整门禁清单结构化，作为项目级配置文件。详细内容见下方模板。

```markdown
---
inclusion: always
name: quality-gate
description: 交付前质量门禁清单，确保所有检查项全绿才可交付
updated: 2026-04-22
---

# 质量门禁清单

> 本文件是交付前的终极检查清单，确保所有规则和流程都已正确执行。
> **任何一项不满足，阻断交付**。

## 📋 门禁清单（10 项全绿才交付）

| 序号 | 检查项 | 验证命令/方式 | 状态 |
|------|--------|--------------|------|
| 1 | ✅ 编译/类型检查通过 | `{{构建命令}}`，前端项目额外运行类型检查 | ⬜ |
| 2 | ✅ 测试覆盖率不低于基准 | `{{覆盖率命令}}`，覆盖率 ≥ 当前基准 | ⬜ |
| 3 | ✅ E2E 测试零失败 | `{{E2E测试命令}}`；如无 E2E 测试，见降级方案 | ⬜ |
| 4 | ✅ 页面零 404 | E2E 测试覆盖所有页面路由；如无 E2E 测试，见降级方案 | ⬜ |
| 5 | ✅ API 零 500 | E2E 测试监听 API 响应；如无 E2E 测试，见降级方案 | ⬜ |
| 6 | ✅ 数据字段无 undefined/null/占位符残留 | 后端 API 响应层兜底 nil 集合 + 前端防御性消费 + grep 检查 | ⬜ |
| 7 | ✅ 权限校验生效 | 权限测试覆盖关键角色组合（至少：超级管理员、普通用户、无权限用户） | ⬜ |
| 8 | ✅ RTM 需求追踪矩阵零空白 | RTM 四类清单（AC/ST/PM/BF）零空白项 | ⬜ |
| 9 | ✅ 代码无 TODO/FIXME/placeholder/{{占位符}} 残留 | `grep -r "TODO\|FIXME\|placeholder" src/` + `grep -r "{{.*}}" .claude/` | ⬜ |
| 10 | ✅ 前后端 API 对接完整性 | API 文档 vs 前端调用 vs 后端实现 | ⬜ |

### 无 E2E 测试时的降级方案

如项目暂无 E2E 测试，第 3-5 项可降级为人工验收：

- **第 3 项降级**：运行单元测试 + 集成测试，确保核心功能验证通过
- **第 4 项降级**：人工遍历所有页面路由，确认无 404
- **第 5 项降级**：人工测试关键 API 端点，确认无 500 错误

> 降级需在 PR 中标注原因并排期补充 E2E 测试。

## ⏰ 执行时机

| 时机 | 执行项 | 说明 |
|------|--------|------|
| 每次提交前 | 第 1 项 | 编译和类型检查 |
| PR 合并前 | 第 1-3 项 | 编译 + 测试 + 覆盖率 |
| CI/CD 自动触发 | 第 1-3、9 项 | 可自动化的检查项 |
| **每次交付前** | **第 1-10 项** | **完整门禁清单** |

## 🚨 失败处理

| 序号 | 失败项 | 处理方式 | 责任人 |
|------|--------|---------|--------|
| 1 | 编译失败 | build-error-resolver agent 修复 | Agent |
| 2 | 覆盖率不足 | tester agent 补充测试，coverage-auditor agent 审计 | Agent |
| 3 | 测试失败 | 分析 bug 来源，对应 agent 修复 | Agent/人工 |
| 4 | 页面 404 | 检查路由配置，E2E 测试覆盖所有路由 | 前端开发者 |
| 5 | API 500 | 修复错误处理逻辑，前端加容错机制 | 后端开发者 |
| 6 | 数据字段问题 | 前端加守卫，后端加兜底 | 前后端开发者 |
| 7 | 权限问题 | 修复权限逻辑，同步路由守卫 | 后端开发者 |
| 8 | RTM 空白 | 补充测试用例，确保需求与测试一一对应 | tester agent |
| 9 | TODO/FIXME 残留 | 清理遗留项或转为正式需求 | 人工 |
| 10 | API 对接不一致 | 修正实现/调用/文档，同步更新 | 前后端开发者 |

## 📝 前置条件

执行门禁检查前，确认以下条件已满足：

- [ ] 代码已提交（无未暂存的修改）
- [ ] 本地测试已通过（`{{测试命令}}`）
- [ ] 环境配置正确（数据库、中间件、环境变量）
- [ ] 依赖已安装（`{{包管理器}} install`）

## 💡 关键洞察

- **门禁是最后一道防线**：Hooks 可能被绕过，门禁必须兜底
- **双重保险**：门禁与 Hooks 检查项可能重叠，这是故意的
- **回溯改进**：门禁失败要追问"规范是否缺失"，持续改进
- **自动化优先**：能自动化的检查项应配置为 CI 阻断条件

## 📚 相关文档

- 详细说明：见手册第六章
- RTM 创建：见手册 6.5 节
- 失败处理：见手册 6.3 节
- 自动化配置：见手册 6.4.2 节
```

> **说明**：本文件使用 `inclusion: always` 类型，每次会话自动加载。建议在交付前主动查阅此文件，确保所有检查项通过。

---

#### 7.7.6 steer/domain/api.md

**fileMatch 类型（编辑匹配文件时加载），需要填入 API 文件的 glob 模式。**

````markdown
---
inclusion: fileMatch
fileMatchPattern: ["{{API文件匹配模式}}"]
---

# API 开发规范

> 本文件在编辑匹配文件时加载，不需要每次会话都加载。
> 根据实际项目调整 fileMatchPattern。

## RESTful 规范

- URL 使用名词复数：`/users` 而非 `/getUser`
- 使用正确的 HTTP 方法：GET（查询）、POST（新增）、PUT（更新）、DELETE（删除）
- 嵌套资源限制一层：`/users/123/orders` 而非 `/users/123/orders/456/items`

## 响应格式

```json
{
  "code": 0,
  "data": {},
  "message": "success"
}
```

| code | 含义 |
|------|------|
| 0 | 成功 |
| 400 | 参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 500 | 服务器错误 |

## 错误处理

- 所有异常必须捕获，统一返回上述响应格式
- 不在响应中暴露堆栈信息
- 记录错误日志，包含请求 ID 用于追踪

## 参数校验

- 必填参数必须校验，不允许 null/undefined
- 字符串类型校验长度范围
- 数字类型校验最大值最小值
- 日期类型校验格式和范围

## 分页规范

```json
{
  "code": 0,
  "data": {
    "list": [],
    "total": 100,
    "page": 1,
    "pageSize": 20
  },
  "message": "success"
}
```
````

#### 7.7.7 steer/domain/testing.md

**fileMatch 类型（编辑测试文件时加载），需要填入测试文件的 glob 模式。**

````markdown
---
inclusion: fileMatch
fileMatchPattern: ["{{测试文件匹配模式}}"]
---

# 测试规范

> 本文件在编辑测试文件时加载。
> 根据实际项目调整 fileMatchPattern。

## 测试文件命名

- 单元测试：`*.test.ts` 或 `*.spec.ts`
- 集成测试：`*.integration.test.ts`
- E2E 测试：`e2e/**/*.spec.ts`

## 测试文件位置

- 单元测试：与被测文件同目录（如 `src/utils/helper.test.ts`）
- 集成测试：`tests/integration/` 目录
- E2E 测试：`tests/e2e/` 目录

## 测试结构

```typescript
describe('{{被测单元}}', () => {
  // 前置条件
  beforeEach(() => {
    // 准备测试数据
  });

  describe('{{场景1}}', () => {
    it('{{预期行为}}', () => {
      // 测试逻辑
      // 断言
    });
  });
});
```

## Mock 规范

- 使用 `vi.fn()` / `jest.fn()` 创建 mock 函数
- Mock 文件放在 `__mocks__/` 目录
- 只 mock 外部依赖，不 mock 被测单元本身

## 覆盖率要求

- 核心业务逻辑：≥ {{当前覆盖率}}%
- 新增代码必须附带测试
- 不允许提交跳过测试的代码（`it.skip`、`describe.skip`、`@Disabled`）

## 常见错误

1. 异步测试忘记 `async/await` 或 `.resolves()`
2. Mock 路径不正确导致 mock 不生效
3. 测试之间没有隔离，依赖执行顺序
````

#### 7.7.8 steer/domain/security.md

**auto 类型（AI 自动判断相关时加载），不需要填入 fileMatchPattern。**

```markdown
---
inclusion: auto
name: security-patterns
description: 安全相关的代码规范。在创建或修改涉及数据访问、用户输入、外部调用的代码时使用。
---

# 安全规范

> 本文件通过 AI 自动判断是否相关，在需要时加载。
> 记录安全相关的编码规范，帮助 AI 在编写代码时自动遵守。

## 数据访问

- 所有数据库查询必须使用参数化查询，禁止 SQL 拼接
- 敏感字段（密码、密钥、Token）在存储前加密
- 查询结果中的敏感字段需要脱敏处理

## 用户输入

- 所有用户输入必须校验，不信任任何外部数据
- HTML 输出时必须转义，防止 XSS
- 文件上传验证类型和大小，防止路径穿越

## 认证与授权

- Token 过期后必须重新认证
- 权限验证在业务逻辑之前执行
- 不在客户端存储敏感信息

## 日志规范

- 不记录密码、密钥、Token 等敏感信息
- 记录足够的上下文用于问题排查
- 错误日志包含请求 ID 用于追踪

## 依赖安全

- 新增依赖必须检查已知漏洞（`npm audit` / `pnpm audit`）
- 不使用已停止维护的包
- 定期更新依赖版本
```

#### 7.7.9 steer/domain/frontend.md（可选）

**fileMatch 类型（编辑前端组件文件时加载），需要填入组件文件的 glob 模式。**

````markdown
---
inclusion: fileMatch
fileMatchPattern: ["src/components/**", "src/ui/**"]
---

# 前端开发规范

> 本文件在编辑前端组件文件时加载。
> 根据实际项目调整 fileMatchPattern。

## 组件设计原则

- 单一职责：每个组件只做一件事
- 受控/非受控明确：优先使用受控组件
- Props 类型完整：必须定义 TypeScript 类型，禁止 any

## 状态管理

- 局部状态：组件内部用 `ref` / `reactive`
- 全局状态：跨组件共享用 Pinia / Vuex
- 避免过度提升：不是所有状态都需要提升到父组件

## 样式规范

- 优先使用 CSS Modules / Scoped CSS
- 遵循设计系统的间距、颜色、字体规范
- 响应式设计：移动端优先

## 性能优化

- 列表渲染使用唯一 key
- 大列表虚拟滚动
- 懒加载非首屏组件
- 避免不必要的 re-render

## 无障碍（a11y）

- 语义化标签
- 键盘可访问
- ARIA 属性正确使用
````

> **说明**：此文件为可选配置，适用于前端项目需要更细粒度的组件开发规范时使用。如项目已有完整的 UI 设计规范文档，可将 fileMatchPattern 指向组件目录，在编辑组件时自动加载规范。

---

### 7.8 commands/sd-plan.md

**不需要改造，直接复制使用。**

```markdown
---
name: sd-plan
description: 需求规划与风险评估，输出修改计划后再执行
---

# /sd-plan 命令规范

## 输出格式

执行任何操作前，先输出以下结构的 Plan：

## 需求复述
[一句话描述要做什么]

## 影响范围
- 涉及文件：[列出所有将被修改的文件]
- 影响模块：[列出受影响的模块]

## 修改步骤
1. [步骤1]
2. [步骤2]
3. [步骤3]

## 风险评估
- 高风险：[如有，说明原因]
- 中风险：[如有，说明原因]
- 低风险：[如有，说明原因]

## 验收标准
- [具体可验证的交付条件]

## 触发条件

与 CLAUDE.md「必须先 Plan 的高风险操作」一致：修改 3 个以上文件、涉及重构、引入新依赖、安全/权限修改、需求不清晰，或无法用一句话说清 diff 时，必须先执行 /sd-plan。

## 后续流程

**Plan 确认后自动调用 Spec**：

用户确认 Plan 后，AI 应自动调用 `/sd-spec` 命令创建 Spec 文件，无需用户再次手动触发。

```
用户说"确认"、"好的"、"可以"、"继续"等确认词
    ↓
AI 自动调用 /sd-spec
    ↓
创建 .claude/specs/<feature>/ 下的四个文件
```

> **注意**：如果用户明确说"直接改"、"不用规划"等豁免词，或任务明显属于单文件小改动（修复 bug、调整配置），则跳过 Spec 直接实现。
```

---

### 7.9 commands/sd-codereview.md

**不需要改造，直接复制使用。**

```markdown
---
name: sd-codereview
description: 代码审查，从质量、安全、可维护性维度审查变更
---

# /sd-codereview 命令规范

## 审查维度（固定 5 项）

每项按 严重/中等/建议 三级标注：

### 1. 质量（Quality）
- 逻辑是否正确
- 是否有边界情况未处理
- 错误处理是否完善

### 2. 安全（Security）
- 是否有注入风险
- 是否有敏感信息泄露
- 权限控制是否正确
- 对照 rules/security.md 🔴 级别规则逐项检查

### 3. 可维护性（Maintainability）
- 命名是否清晰
- 函数是否过长（建议 ≤ 50 行）
- 是否有重复代码

### 4. 性能（Performance）
- 是否有不必要的循环/查询
- 是否有 N+1 问题
- 缓存使用是否合理

### 5. 测试覆盖（Test Coverage）
- 新增代码是否有测试
- 测试用例是否有效
- 覆盖率是否达标

## 输出格式

## Code Review Report

### 质量
- [问题描述]（严重/中等/建议）

### 安全
...

### 可维护性
...

### 性能
...

### 测试覆盖
...

## 总结
- 严重问题：N 个 → 必须修复
- 中等问题：N 个 → 建议修复
- 建议：N 个 → 可选
```

---

### 7.10 commands/sd-buildfix.md

**不需要改造，直接复制使用。**

```markdown
---
name: sd-buildfix
description: 构建和测试错误的自动诊断与修复
---

# /sd-buildfix 命令规范

## 前置知识

诊断前必须先查阅 `.claude/skills/troubleshooting.md` 中的常见问题解决方案，匹配已知错误模式。

## 诊断流程

遇到构建/测试错误时，必须先完整诊断再修复：

### 第一步：收集错误信息
1. 错误类型：编译错误 / 依赖错误 / 测试失败 / 类型检查失败 / 数据库连接错误 / CI 错误
2. 错误文件：[完整路径]
3. 错误信息：[原始错误输出]
4. 相关日志：[如有]

### 第二步：分析根因
- 是新代码引入的错误？
- 是依赖版本冲突？
- 是环境差异导致的？
- 是已有问题的暴露？

### 第三步：修复方案
修复步骤：
1. [步骤1]
2. [步骤2]

修复后验证：
- [如何确认修复成功]

## 修复原则

1. 先诊断后修复 — 不猜测根因
2. 一次只修一个问题 — 避免引入新问题
3. 修完必须验证 — 运行测试确认通过
4. 保留错误上下文 — Commit message 写明修复了什么
5. **经验沉淀** — 新错误模式追加到 troubleshooting.md

## 经验沉淀流程

修复成功后执行：

### 判断是否值得记录
满足以下任一条件则值得记录：
- troubleshooting.md 中没有该错误类型的解决方案
- 现有方案不完整或不适用
- 发现了新的根因或更优解决方案

### 追加格式
```markdown
### [错误简述]
问题：[用户可见的症状]
错误：[原始错误信息关键片段]
原因：[根本原因，一句话]
解决：
```bash
# 解决命令或代码
```
关键点：[避免踩坑的要点]
```

### 追加方式
使用 Edit 工具追加到 `.claude/skills/troubleshooting.md` 对应分类末尾，不要重写整个文件。

## 输出格式

## Build Fix Report

### 错误类型
[编译/测试/类型检查]

### 根因分析
[一句话描述根本原因]

### 修复方案
1. [步骤]
2. [步骤]

### 验证结果
- 命令：[验证命令]
- 结果：[PASS/FAIL]

### Commit 建议
[type](scope): [简短描述]
```

---

### 7.11 commands/sd-dev.md

**新增配置文件，用于全栈开发编排。**

```markdown
---
name: sd-dev
description: 全栈开发编排，按 db→backend→frontend→tester→reviewer 串行调度
---

# /sd-dev 命令规范

## 触发场景

- 新项目全栈开发
- 大规模功能实现（多模块协同）
- 需要完整开发流程编排

## 概念说明

> **调度粒度 vs 任务粒度**：
> - **本文档（sd-dev.md）** 定义的是 **调度阶段（Phase）**，每个阶段对应一个 Agent 执行单元
> - **tasks.md** 定义的是 **具体任务（Task）**，是调度阶段的细粒度拆分
> - 一个 Phase 可能包含多个 Task，例如"数据库阶段"包含 T-001~T-003

## 编排流程

### 第一阶段：准备

> **前置条件**：需求确认后，必须先按 CLAUDE.md 的 Spec 工作流创建 `.claude/specs/<feature>/` 下的四个文件（requirements / design / test-cases / tasks），/sd-dev 命令读取这些 Spec 作为输入。

1. 读取需求文档（.claude/specs/*/requirements.md）
2. 读取设计文档（.claude/specs/*/design.md）
3. 读取测试用例文档（.claude/specs/*/test-cases.md）
4. 读取任务清单（.claude/specs/*/tasks.md）

### 第二阶段：串行调度

> **注意**：架构设计已在 Spec 阶段由 architect agent 完成（design.md），本阶段直接进入实现。

按顺序调度以下阶段：

| 序号 | 阶段 | Agent | 输入 | 对应 tasks.md 阶段 |
|------|------|-------|------|-------------------|
| 1 | 数据库实现 | db-implementer | design.md（Schema 设计） | 阶段二：数据库 |
| 2 | 后端实现 | backend | design.md（API 设计）、test-cases.md | 阶段三：后端 |
| 3 | 前端实现 | frontend | design.md（API 设计）、原型 HTML | 阶段四：前端 |
| 4 | 测试执行 | tester | test-cases.md、前端页面 | 阶段五：测试执行 |
| 5 | 代码审查 | code-reviewer | 所有代码文件 | 阶段六：测试与审查 |
| 6 | 提交 Git | 主 CC | 审查通过 | 阶段七：提交 Git |

> **Agent 说明**：
> - **独立配置 Agent**：db-implementer / backend / frontend / tester / code-reviewer 有独立配置文件（见 `.claude/agents/` 目录）
> - **运行时角色**：backend-fixer / frontend-fixer 由主 CC 直接调度，用于问题修复

### 第三阶段：问题修复

1. 汇总审查报告，按 P0/P1/P2 分类
2. 分派 backend-fixer / frontend-fixer 修复
3. 修复后重新运行测试

### 第四阶段：质量门禁验证

运行质量门禁清单（见 `.claude/steer/foundation/quality-gate.md`），全部通过才交付。

## Agent 配置索引

### 独立配置 Agent

| Agent | 配置文件 | 职责 |
|-------|---------|------|
| architect | .claude/agents/architect.md | 输出 Schema + API 文档 + 设计决策（Spec 阶段使用） |
| sd-reviewer | .claude/agents/sd-reviewer.md | Spec 文档评审（Spec 阶段使用） |
| db-implementer | .claude/agents/db-implementer.md | 创建数据库表、DO 实体类、Mapper 接口 |
| backend | .claude/agents/backend.md | 创建 VO、Service、Controller |
| frontend | .claude/agents/frontend.md | 创建 API 定义、页面、组件 |
| tester | .claude/agents/tester.md | 编写/修复 E2E 测试 |
| code-reviewer | .claude/agents/code-reviewer.md | 审查质量/安全/可维护性 |
| coverage-auditor | .claude/agents/coverage-auditor.md | 独立审计覆盖率真实性 |
| build-error-resolver | .claude/agents/build-error-resolver.md | 修复构建/测试错误 |

### 运行时角色（无独立配置文件）

| 角色 | 职责 | 调度方式 |
|------|------|---------|
| backend-fixer | 修复后端问题（审查/测试失败时） | 主 CC 直接调度 |
| frontend-fixer | 修复前端问题（审查/测试失败时） | 主 CC 直接调度 |

## Prompt 模板

> **注意**：以下 agent 有独立配置文件，调用时会自动加载配置中的规范约束。主 CC 只需提供任务上下文，无需重复说明规范。

### db-implementer 调用示例

```
你现在是 db-implementer（配置文件：.claude/agents/db-implementer.md）。

任务：根据设计文档创建数据库结构

输入：
- 设计文档：.claude/specs/performance-management/design.md
- 数据库设计章节：第 2 节

输出：
- SQL 脚本：创建数据库表
- DO 实体类：对应数据库表的实体
- Mapper 接口：MyBatis Mapper

参考配置文件中的规范约束执行。
```

### backend 调用示例

```
你现在是 backend（配置文件：.claude/agents/backend.md）。

任务：根据设计文档实现后端 API

输入：
- 设计文档：.claude/specs/performance-management/design.md
- API 设计章节：第 3 节
- 测试用例：.claude/specs/performance-management/test-cases.md

输出：
- VO 类（Req/Resp/Page）
- Service 接口和实现
- Controller

参考配置文件中的规范约束执行。
```

### frontend 调用示例

```
你现在是 frontend（配置文件：.claude/agents/frontend.md）。

任务：根据设计文档实现前端页面

输入：
- 设计文档：.claude/specs/performance-management/design.md
- API 设计章节：第 3 节
- 原型 HTML：（如有提供）

输出：
- API 定义文件（api/xxx.js）
- 列表页面
- 表单弹窗

参考配置文件中的规范约束执行。
```

## 注意事项

1. **每个 agent 的 prompt 必须自包含**：看不到对话历史，需要完整上下文
2. **写文件规则在 prompt 开头强调**：≤60 行/次，分块追加
3. **全新代码也要审查**：AI 生成的代码存在权限缺失、校验遗漏等问题
4. **测试先行**：test-cases.md 在 Spec 阶段已创建，实现阶段参考测试用例编写代码

### 7.12 commands/sd-spec.md

```yaml
---
name: sd-spec
description: 需求确认后创建 Spec 目录及四个核心文件
---

# /sd-spec 命令规范

## 触发场景

用户确认需求后，开始实现前，必须按此流程创建 Spec。

## 前置条件

用户已确认 Plan，AI 已分析需求并得到用户认可。

## 工作流程

### 第一步：整理需求概要

AI 根据对话历史整理需求概要，向用户确认理解是否正确：

```
功能名称：{名称}
一句话描述：{描述}
核心验收条件：
- AC-001：{条件}
- AC-002：{条件}
...
影响范围：后端 {X} 个模块，前端 {Y} 个页面，数据库 {Z} 张表
```

如有偏差，用户纠正；无偏差则继续。

### 第二步：创建 Spec 目录

在 `.claude/specs/{feature-name}/` 下创建四个文件：

```
.claude/specs/<feature>/
├── requirements.md  # 验收条件
├── design.md         # 技术方案
├── test-cases.md     # 测试用例
└── tasks.md          # 任务清单
```

### 第三步：生成四个文件（含评审）

每个文件生成后必须调用 `/sd-reviewer` 进行评审，通过后才进入下一步。

#### 3.1 生成 requirements.md

参考 `.claude/templates/spec/requirements.md` 模板，输出到 `.claude/specs/{feature}/requirements.md`：

```
你现在是主 CC。

任务：为 {功能名称} 创建需求文档

输入：
- 功能名称：{名称}
- 需求概要（来自第一步）

输出文件：.claude/specs/{feature}/requirements.md

必须包含以下章节（按模板格式）：
1. 功能概述（一句话描述 + 业务背景）
2. 验收条件表（AC 编号化，优先级，验证方式）
3. 影响范围（后端/前端/数据库影响说明）
4. 用户故事
5. 非功能性需求
6. 边界情况
7. 参考资料

约束：
- 每次写入 ≤ 60 行，分块追加
```

**评审**：调用 `/sd-reviewer` 评审 requirements.md
- 如有问题：修复 → 重新评审（最多 3 轮）
- 通过后继续

#### 3.2 生成 design.md

参考 `.claude/templates/spec/design.md` 模板，输出到 `.claude/specs/{feature}/design.md`：

```
你现在是 architect agent。

任务：为 {功能名称} 设计技术方案

输入：
- 功能名称：{名称}
- 验收条件：AC-001...AC-00N

输出文件：.claude/specs/{feature}/design.md

必须包含以下章节（按模板格式）：
1. 技术方案概述（一句话描述 + 方案选择原因）
2. 数据库设计（新增表/修改表，字段、索引）
3. API 设计（接口列表 + 接口详情）
4. 关键决策（技术选型、架构决策）
5. 数据流程图
6. 风险评估

约束：
- 每次写入 ≤ 60 行，分块追加
- 字符集规范：SQL 脚本开头添加 SET NAMES utf8mb4;
- 字段命名参考项目现有风格
```

**评审**：调用 `/sd-reviewer` 评审 design.md
- 如有问题：修复 → 重新评审（最多 3 轮）
- 通过后继续

#### 3.3 生成 test-cases.md

参考 `.claude/templates/spec/test-cases.md` 模板，输出到 `.claude/specs/{feature}/test-cases.md`：

```
你现在是 architect agent。

任务：为 {功能名称} 编写测试用例

输入：
- 功能名称：{名称}
- 验收条件：AC-001...AC-00N
- 设计文档：.claude/specs/{feature}/design.md

输出文件：.claude/specs/{feature}/test-cases.md

必须包含以下章节（按模板格式）：
1. 测试用例概览（用例数统计）
2. 单元测试用例（覆盖 Service/Controller 层）
3. E2E 测试用例（冒烟、功能、权限、状态流转、业务流程）
4. 测试数据规范（Seed 数据准备）
5. RTM 追踪表（验收条件 → 测试用例 → 状态）

约束：
- 每次写入 ≤ 60 行，分块追加
- 每个 AC 必须有对应测试用例
- E2E 必须包含三层验证：页面可达、数据加载、数据渲染
```

**评审**：调用 `/sd-reviewer` 评审 test-cases.md
- 如有问题：修复 → 重新评审（最多 3 轮）
- 通过后继续

#### 3.4 生成 tasks.md

参考 `.claude/templates/spec/tasks.md` 模板，输出到 `.claude/specs/{feature}/tasks.md`：

```
你现在是主 CC。

任务：为 {功能名称} 创建任务清单

输入：
- 功能名称：{名称}
- 设计文档：.claude/specs/{feature}/design.md
- 测试用例：.claude/specs/{feature}/test-cases.md

输出文件：.claude/specs/{feature}/tasks.md

必须包含以下章节（按模板格式）：
1. 任务状态说明（⬜未开始 / 🔄进行中 / ✅已完成 / ❌已阻塞）
2. 任务列表（分阶段：测试用例文档 / 数据库 / 后端 / 前端 / 测试执行 / 审查 / Git提交）
3. 任务依赖关系图
4. 测试先行开发原则
5. 总计（预计工时、任务总数、进度）

约束：
- 每次写入 ≤ 60 行，分块追加
- 任务 ID 格式：T-xxx（测试文档 T-DOC-xxx，单元测试 T-UT-xxx，E2E 测试 T-E2E-xxx）
```

**评审**：调用 `/sd-reviewer` 评审 tasks.md
- 如有问题：修复 → 重新评审（最多 3 轮）
- 通过后 Spec 完成

## 文件模板索引

| 文件 | 模板位置 |
|------|----------|
| requirements.md | .claude/templates/spec/requirements.md |
| design.md | .claude/templates/spec/design.md |
| test-cases.md | .claude/templates/spec/test-cases.md |
| tasks.md | .claude/templates/spec/tasks.md |

## 完成后

Spec 创建完成后，用户输入"继续"、"开始实现"等确认词，AI 使用 `/sd-dev` 命令启动 Agent 协作实现。

## 注意事项

1. **必须先 Spec 再实现** — 禁止跳过 Spec 直接写代码
2. **四个文件缺一不可** — requirements / design / test-cases / tasks
3. **写文件规则** — 每次 ≤ 60 行，分块追加
4. **模板是唯一权威** — 内容格式必须参考 `.claude/templates/spec/` 下的四个模板文件
5. **评审机制** — 每个文件生成后必须经过 `/sd-reviewer` 评审，通过后才能进入下一步
6. **多轮评审** — 最多 3 轮，3 轮后由主 CC 决策是否继续
```

### 7.13 agents/architect.md

**新增配置文件，架构设计专用 Agent。**

```markdown
---
name: architect
description: 架构设计 Agent，输出 Schema + API 文档 + 设计决策
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Architect Agent

你是架构设计专家，负责从需求文档设计数据库 Schema 和 API 文档。

## 设计能力

### 数据库设计
- 分析需求文档提取实体和关系
- 参考 V1 老系统的字段命名风格（如有）
- 设计索引策略
- 输出完整的 Schema 文档（包含字段类型、约束、索引）

### API 设计
- RESTful API 端点设计
- 请求/响应结构定义
- 权限控制设计
- 输出完整的 API 文档

### 设计决策
- 技术选型建议
- 架构权衡分析
- 与部署方案对齐（端口、环境变量等）

## 输出格式

## Schema 文档

### 集合定义
| 集合名 | 说明 | 字段数 |
|--------|------|--------|
| ... | ... | ... |

### 字段详情
[每个集合的字段定义]

### 索引策略
[索引定义]

---

## API 文档

### 端点列表
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| ... | ... | ... | ... |

### 请求/响应示例
[详细定义]

## 设计决策确认

| 决策项 | 选择 | 原因 |
|--------|------|------|
| ... | ... | ... |

## 关键经验

- 探索老系统代码是必要的：V1 的数据结构和命名风格直接影响 V2 设计
- 端口等细节要与部署方案对齐：避免后期返工
- 输出时每次写入 ≤ 60 行，分块追加
```

---

### 7.14 agents/code-reviewer.md

**需要增强审查清单，添加智能体质量门禁相关的检查项。**

```markdown
---
name: code-reviewer
description: 从质量、安全、可维护性、性能、测试覆盖五个维度审查代码
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Code Review Agent

你是一个专业的代码审查助手，负责对变更进行系统性审查。

## 审查标准

### 质量维度
- 业务逻辑正确性
- 边界情况处理
- 错误处理完善度

### 安全维度
- SQL 注入 / XSS 风险
- 敏感信息处理
- 权限控制
- 对照 rules/security.md 🔴 级别规则逐项检查

### 可维护性维度
- 命名规范与可读性
- 函数长度（目标 ≤ 50 行）
- 代码重复度

### 性能维度
- 是否有不必要的循环/查询
- 是否有 N+1 问题
- 缓存使用是否合理

### 测试覆盖维度
- 新增代码是否有测试
- 测试用例是否有效
- 覆盖率是否达标

### 前端安全（智能体质量门禁新增）
- **nil 返回路径检查**：后端 API 是否可能返回 null 集合
- **裸赋值检查**：前端是否直接赋值 API 返回值，未加空值守卫
- **前后端权限一致性检查**：前端路由守卫与后端 API 权限是否同步
- **placeholder 残留检查**：TODO、FIXME、硬编码假数据

## 输出要求

按以下格式输出审查结果：

## 审查结论

### 严重 P0（必须修复）
- [文件:行号] [问题描述]

### 中等 P1（建议修复）
- [文件:行号] [问题描述]

### 建议 P2（可选）
- [文件:行号] [问题描述]

## 关键洞察（来自生产级项目实战）

- 全新代码也需要审查：AI 生成的代码存在权限缺失、校验遗漏等问题
- nil 集合是万恶之源：后端返回 null，前端 .map() 直接崩
- 前端永远不信任后端返回值：即使承诺返回数组，也要加 ?? []
```

---

### 7.15 agents/sd-reviewer.md

**新增配置文件，Spec 文档评审专用 Agent。**

```markdown
---
name: sd-reviewer
description: Spec 文档评审 Agent，对 Spec 文件进行结构化评审
---

# /sd-reviewer 命令规范

## 触发时机

每个 Spec 文件（requirements/design/test-cases/tasks）生成后，必须调用 sd-reviewer 进行评审。

## 评审流程

1. 读取待评审文件
2. 按评审要点逐项检查
3. 输出评审报告
4. 根据问题严重程度判断：
   - 严重/中等问题 → 输出修改建议 → 修复后重新评审
   - 只有建议 → 可选择修复 → 通过

## 评审退出条件

- 无严重/中等问题，或
- 已达 3 轮评审

## 评审报告格式

\`\`\`markdown
## Spec 文档评审报告

### 评审文件
[filename]

### 评审轮次
第 N 轮

### 问题列表

| 严重程度 | 问题类型 | 位置 | 问题描述 | 建议修改 |
|----------|----------|------|----------|----------|
| 严重 | 缺失 | 字段：user_id | 缺少 user_id 字段 | 添加 user_id BIGINT NOT NULL |

### 统计
- 严重问题：N 个
- 中等问题：N 个
- 建议：N 个

### 结论
✅ 通过 / ❌ 需要修复（第 N 轮）
\`\`\`

## 各文件评审要点

### requirements.md 评审要点

| 评审维度 | 评审内容 | 严重程度 |
|----------|----------|----------|
| 完整性 | AC 是否覆盖核心业务场景 | 严重 |
| 完整性 | AC 是否覆盖边界情况 | 中等 |
| 可测试性 | 每个 AC 是否可验证 | 严重 |
| 一致性 | AC 之间是否无矛盾 | 严重 |

### design.md 评审要点

| 评审维度 | 评审内容 | 严重程度 |
|----------|----------|----------|
| 表结构 | 字段是否完整（对照 AC 需求） | 严重 |
| 表结构 | 字段类型是否正确 | 严重 |
| API 设计 | 接口是否完整（对照 AC 需求） | 严重 |
| 一致性 | 表字段与 API 参数是否一致 | 严重 |

### test-cases.md 评审要点

| 评审维度 | 评审内容 | 严重程度 |
|----------|----------|----------|
| 覆盖率 | 每个 AC 是否有对应测试用例 | 严重 |
| 可执行性 | 测试步骤是否具体可执行 | 严重 |
| 正确性 | 断言条件是否正确 | 严重 |

### tasks.md 评审要点

| 评审维度 | 评审内容 | 严重程度 |
|----------|----------|----------|
| 完整性 | 是否有任务漏项（对照 design.md） | 严重 |
| 完整性 | 是否包含测试任务（T-UT / T-E2E） | 严重 |
| 依赖关系 | 任务依赖是否正确 | 严重 |
```

---

### 7.16 agents/db-implementer.md

**新增配置文件，数据库实现专用 Agent。**

```markdown
---
name: db-implementer
description: 数据库实现 Agent，创建数据库表、DO 实体类、Mapper 接口
tools: Read, Grep, Glob, Bash, Edit
model: sonnet
---

# DB-Implementer Agent

你是数据库实现专家，负责根据设计文档创建数据库结构。

## 实现能力

### SQL 脚本
- 创建数据库表（CREATE TABLE）
- 添加索引（CREATE INDEX）
- 数据迁移脚本（如需）

### DO 实体类
- 对应数据库表的实体类
- MyBatis-Plus 注解（@TableName, @TableId, @TableField）
- 枚举字段处理

### Mapper 接口
- BaseMapper 继承
- 自定义查询方法
- @Mapper 注解

## 规范约束

### SQL 脚本规范
```sql
-- 必须在脚本开头添加
SET NAMES utf8mb4;

-- 表注释必须包含
CREATE TABLE `table_name` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  ...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='表说明';
```

### 字段命名规范
- 遵循项目现有风格（snake_case）
- 主键统一为 `id`（bigint, AUTO_INCREMENT）
- 必须包含：`creator`, `create_time`, `updater`, `update_time`, `deleted`
- 逻辑删除字段：`deleted`（tinyint, 默认 0）

### DO 实体类规范
```java
@TableName("table_name")
@KeySequence("table_name_seq")
public class XxxDO {
    @TableId
    private Long id;
    // ...
    @TableField(fill = FieldFill.INSERT)
    private String creator;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private String updater;
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
    @TableLogic
    private Integer deleted;
}
```

### Mapper 接口规范
```java
@Mapper
public interface XxxMapper extends BaseMapper<XxxDO> {
    // 自定义方法（如有）
}
```

## 输出格式

### 文件列表
| 类型 | 文件路径 | 说明 |
|------|----------|------|
| SQL | sql/xxx.sql | 建表脚本 |
| DO | entity/XxxDO.java | 实体类 |
| Mapper | mapper/XxxMapper.java | Mapper 接口 |

## 写文件规则

- **每次写入 ≤ 60 行**，分块追加
- 超过 60 行时，先写前半部分，再追加后半部分

## 关键经验

- 参考 project_databases.md 了解现有表结构风格
- 字符集必须为 utf8mb4，支持 emoji
- 逻辑删除字段名与项目一致
- 索引命名：idx_字段名，唯一索引 uk_字段名
```

---

### 7.17 agents/backend.md

**新增配置文件，后端实现专用 Agent。**

```markdown
---
name: backend
description: 后端实现 Agent，创建 VO、Service、Controller
tools: Read, Grep, Glob, Bash, Edit
model: sonnet
---

# Backend Agent

你是后端实现专家，负责根据设计文档实现 API 接口。

## 实现能力

### VO 类
- ReqVO：请求参数
- RespVO：响应数据
- PageReqVO：分页请求

### Service 层
- 接口定义
- 实现类
- 事务处理

### Controller 层
- RESTful API
- 参数校验
- 权限控制

## 规范约束

### VO 类规范
```java
@Data
public class XxxSaveReqVO {
    @Schema(description = "主键")
    private Long id;

    @Schema(description = "名称", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotBlank(message = "名称不能为空")
    private String name;
}

@Data
@EqualsAndHashCode(callSuper = true)
public class XxxPageReqVO extends PageParam {
    @Schema(description = "名称")
    private String name;
}

@Data
public class XxxRespVO {
    @Schema(description = "主键")
    private Long id;
    // ...
}
```

### Service 规范
```java
public interface XxxService {
    Long createXxx(@Valid XxxSaveReqVO createReqVO);
    void updateXxx(@Valid XxxSaveReqVO updateReqVO);
    void deleteXxx(Long id);
    XxxRespVO getXxx(Long id);
    PageResult<XxxRespVO> getXxxPage(XxxPageReqVO pageReqVO);
}

@Service
@Validated
public class XxxServiceImpl implements XxxService {
    @Resource
    private XxxMapper xxxMapper;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Long createXxx(XxxSaveReqVO createReqVO) {
        // 1. 校验
        // 2. 转换
        // 3. 保存
    }
}
```

### Controller 规范
```java
@RestController
@RequestMapping("/xxx")
@Tag(name = "管理后台 - XXX")
public class XxxController {
    @Resource
    private XxxService xxxService;

    @PostMapping("/create")
    @Operation(summary = "创建XXX")
    @PreAuthorize("@ss.hasPermission('xxx:create')")
    public CommonResult<Long> createXxx(@Valid @RequestBody XxxSaveReqVO createReqVO) {
        return success(xxxService.createXxx(createReqVO));
    }

    @GetMapping("/page")
    @Operation(summary = "获取XXX分页")
    @PreAuthorize("@ss.hasPermission('xxx:query')")
    public CommonResult<PageResult<XxxRespVO>> getXxxPage(@Valid XxxPageReqVO pageReqVO) {
        return success(xxxService.getXxxPage(pageReqVO));
    }
}
```

### 权限注解规范
- 新增：`xxx:create`
- 更新：`xxx:update`
- 删除：`xxx:delete`
- 查询：`xxx:query`
- 导出：`xxx:export`

### 响应空值兜底
```java
// Service 返回空集合而非 null
public List<XxxRespVO> getList() {
    List<XxxDO> list = xxxMapper.selectList();
    return CollectionUtils.isEmpty(list) ? Collections.emptyList() : convertList(list);
}
```

## 输出格式

### 文件列表
| 类型 | 文件路径 | 说明 |
|------|----------|------|
| ReqVO | vo/xxx/XxxSaveReqVO.java | 保存请求 |
| PageReqVO | vo/xxx/XxxPageReqVO.java | 分页请求 |
| RespVO | vo/xxx/XxxRespVO.java | 响应数据 |
| Service | service/XxxService.java | 接口 |
| ServiceImpl | service/XxxServiceImpl.java | 实现 |
| Controller | controller/admin/xxx/XxxController.java | 控制器 |

## 写文件规则

- **每次写入 ≤ 60 行**，分块追加
- 超过 60 行时，先写前半部分，再追加后半部分

## 关键经验

- 权限注解必须与前端路由守卫同步（新增权限需同步到菜单）
- Service 层返回空集合而非 null，避免前端崩溃
- 使用 @Valid 校验参数，不在 Controller 写校验逻辑
- 参考 project_apis.md 了解现有 API 风格
```

---

### 7.18 agents/frontend.md

**新增配置文件，前端实现专用 Agent。**

```markdown
---
name: frontend
description: 前端实现 Agent，创建 API 定义、页面、组件
tools: Read, Grep, Glob, Bash, Edit
model: sonnet
---

# Frontend Agent

你是前端实现专家，负责根据设计文档实现 Vue 页面和组件。

## 实现能力

### API 定义
- 请求方法封装
- TypeScript 类型定义

### 页面实现
- 列表页面（搜索、分页、操作）
- 表单弹窗（新增、编辑）
- 详情页面

### 组件实现
- 业务组件
- 通用组件

## 规范约束

### API 定义规范
```javascript
// api/xxx/index.ts
import request from '@/utils/request'

// 类型定义
export interface XxxVO {
  id?: number
  name?: string
  // ...
}

// API 方法
export const XxxApi = {
  // 获取分页
  getXxxPage: async (params: any) => {
    return await request.get({ url: '/xxx/page', params })
  },
  // 获取详情
  getXxx: async (id: number) => {
    return await request.get({ url: '/xxx/get?id=' + id })
  },
  // 创建
  createXxx: async (data: XxxVO) => {
    return await request.post({ url: '/xxx/create', data })
  },
  // 更新
  updateXxx: async (data: XxxVO) => {
    return await request.put({ url: '/xxx/update', data })
  },
  // 删除
  deleteXxx: async (id: number) => {
    return await request.delete({ url: '/xxx/delete?id=' + id })
  }
}
```

### 列表页面规范
```vue
<template>
  <ContentWrap>
    <!-- 搜索 -->
    <el-form :model="queryParams" ref="queryFormRef" :inline="true">
      <!-- 搜索表单项 -->
    </el-form>
    <!-- 操作按钮 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" @click="handleCreate">新增</el-button>
      </el-col>
    </el-row>
    <!-- 表格 -->
    <el-table v-loading="loading" :data="list ?? []">
      <!-- 表格列 -->
    </el-table>
    <!-- 分页 -->
    <Pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNo" v-model:limit="queryParams.pageSize" @pagination="getList" />
  </ContentWrap>
  <!-- 表单弹窗 -->
  <XxxForm ref="formRef" @success="getList" />
</template>

<script setup lang="ts">
const loading = ref(true)
const list = ref<XxxVO[]>([])
const total = ref(0)
const queryParams = reactive({ pageNo: 1, pageSize: 10 })

const getList = async () => {
  loading.value = true
  try {
    const data = await XxxApi.getXxxPage(queryParams)
    list.value = data?.list ?? []
    total.value = data?.total ?? 0
  } finally {
    loading.value = false
  }
}
</script>
```

### 空值守卫规范（必须）
```javascript
// API 返回值一律加空值守卫
const data = await XxxApi.getXxxPage(queryParams)
list.value = data?.list ?? []        // 数组兜底
total.value = data?.total ?? 0       // 数值兜底

// 链式访问加可选链
row.user?.name ?? '未知'             // 对象兜底
(row.count ?? 0).toFixed(2)          // 方法调用兜底
```

### 权限控制规范
```vue
<el-button v-hasPermi="['xxx:create']" type="primary">新增</el-button>
<el-button v-hasPermi="['xxx:update']" link type="primary">编辑</el-button>
<el-button v-hasPermi="['xxx:delete']" link type="danger">删除</el-button>
```

## 输出格式

### 文件列表
| 类型 | 文件路径 | 说明 |
|------|----------|------|
| API | api/xxx/index.ts | API 定义 |
| 列表页 | views/xxx/index.vue | 列表页面 |
| 表单弹窗 | views/xxx/XxxForm.vue | 表单组件 |

## 写文件规则

- **每次写入 ≤ 60 行**，分块追加
- 超过 60 行时，先写前半部分，再追加后半部分

## 关键经验

- API 返回值永远不信任：加 `?? []` 或 `?? {}` 兜底
- 权限指令 v-hasPermi 与后端 @PreAuthorize 必须同步
- 参考 Element UI 2.15 组件文档
- 参考 project_frontend.md 了解现有页面风格
```

---

### 7.19 agents/tester.md

**新增配置文件，E2E 测试专用 Agent。**

```markdown
---
name: tester
description: E2E 测试 Agent，编写和修复端到端测试
tools: Read, Grep, Glob, Bash, Edit
model: sonnet
---

# Tester Agent

你是 E2E 测试专家，负责编写和维护端到端测试。

## 测试能力

### 冒烟测试
- 页面可达性验证
- 数据加载验证
- 基础交互验证

### 功能测试
- 单个功能点验证
- 表单提交验证
- 错误处理验证

### 权限测试
- 角色访问控制验证
- 数据隔离验证
- 横向越权检测

### 流程测试
- 端到端完整流程验证
- 状态流转验证
- 多步骤操作验证

## 测试基础设施

### 全局错误监听（必须内置）
```javascript
const errors = []
page.on('pageerror', err => errors.push(err.message))
page.on('console', msg => {
  if (msg.type() === 'error') errors.push(msg.text())
})

// 断言前等待微任务完成
await page.waitForLoadState('networkidle')
await page.waitForTimeout(500)
expect(errors.filter(e => !isKnownNoise(e))).toEqual([])
```

### 三层验证标准（每个测试必须验证）
1. **页面可达**：URL 正确，主容器可见
2. **数据加载**：至少一个 API 请求返回成功
3. **数据渲染**：至少一个数据驱动的 DOM 元素包含非空文本

## 禁止模式

| 禁止模式 | 示例 | 正确做法 |
|----------|------|---------|
| 吞掉失败 | `.catch(() => null)` | 让错误直接抛出 |
| 条件断言 | `if (resp) expect(...)` | 无条件断言 |
| 只验证 DOM 存在 | `toBeVisible()` 就结束 | 验证数据内容非空 |
| 硬等待 | `waitForTimeout(3000)` | 等待具体条件 |

## 测试数据规范

- 覆盖关键角色组合（至少包含：超级管理员、普通用户、无权限用户）
- 必须包含"无数据"用户
- 通过 seed 脚本准备，幂等可重复

## 输出格式

## 测试报告

### 测试用例
- [用例名]：[描述]
- [用例名]：[描述]

### 覆盖范围
- 功能覆盖：N/M 个需求
- 角色覆盖：N/M 个角色
- 页面覆盖：N/M 个页面

### 已知限制
- [限制1]：[原因]
- [限制2]：[原因]

## 关键洞察

- 测试全绿 ≠ 没有 bug：只测有数据的用户等于只测了 happy path
- 测试账号选择偏差会制造虚假安全感
- pageerror + 微任务等待是必须的：框架运行时异常不一定在 console.error
```

---

### 7.20 agents/coverage-auditor.md

**新增配置文件，覆盖率审计专用 Agent。**

```markdown
---
name: coverage-auditor
description: 覆盖率审计 Agent，独立审计测试覆盖率真实性
tools: Read, Grep, Glob
model: sonnet
---

# Coverage Auditor Agent

你是测试覆盖率审计专家，负责独立审计测试覆盖率的真实性。

## 审计原则

**覆盖率审计必须独立于测试编写者。编写测试的 agent 不能自己审计覆盖率。**

## 审计维度

### 虚假覆盖检测

| 问题类型 | 特征 | 危害 |
|----------|------|------|
| 纯单元测试伪装 E2E | 无 `page.goto()`、无浏览器交互 | 不验证真实 UI |
| 断言逻辑反转 | 应验证"看不到"却验证"看到" | 结论相反 |
| 只检查存在不执行操作 | 只 `toBeVisible()` 不 `click()` | 不验证交互 |
| 条件跳过掩盖失败 | `if (condition) test.skip()` | 隐藏真实问题 |
| 步骤独立不串联 | 流程测试各步骤互不依赖 | 不验证端到端 |

### RTM 需求追踪矩阵验证

检查 RTM 是否真的覆盖了需求：
- 验收条件（AC）：功能性需求
- 状态流转（ST）：正向转换 + 非法转换
- 权限矩阵（PM）：角色 × 操作 × 预期结果
- 业务流程（BF）：端到端完整流程

### "功能未实现"独立验证

AI 标记为"功能未实现"的需求，必须独立验证：
1. 搜索相关 API 路由、前端页面、组件
2. AI 可能因为找不到精确匹配的代码就判定为未实现
3. 功能可能以不同命名或结构存在

**实践中发现**：6 项被标记为"未实现"的需求中有 5 项实际已实现。

## 审计流程

1. 读取 RTM 需求追踪矩阵
2. 检查每个测试文件是否真的与浏览器交互
3. 验证断言是否有效（不是条件跳过、不是吞失败）
4. 确认测试数据覆盖关键角色组合（至少包含超级管理员、普通用户、无权限用户）
5. 独立验证"未实现"标记是否准确

## 输出格式

## 覆盖率审计报告

### 真实覆盖率
- 需求覆盖：N/M 个需求（N%）
- 角色覆盖：N/M 个角色
- 页面覆盖：N/M 个页面

### 虚假覆盖问题
- [文件:用例名] [问题描述]

### 未实现验证结果
- [需求名]：实际已实现 / 确实未实现

### 建议
- [改进建议1]
- [改进建议2]

## 关键洞察

- "测试存在" ≠ "测试有效"：必须检查测试是否真的与浏览器交互并做有意义的断言
- RTM 是覆盖率的唯一真相：不要相信"感觉覆盖了"
- 独立审计避免自我评价偏差
```

---

### 7.21 agents/build-error-resolver.md

**需要根据项目技术栈选择对应条目，删除不相关的诊断能力。**

以下模板已覆盖常见技术栈（Java/SpringBoot/RuoYi/Vue/MySQL/PostgreSQL/瀚高/Redis/ActiveMQ/Kafka）。如项目使用其他技术栈（Go/Rust/Django/Flask/Express/NestJS 等），请参照现有条目格式自行补充对应诊断能力。

```markdown
---
name: build-error-resolver
description: 专门处理项目构建、测试中的错误，积累排障经验
tools: Read, Bash, Glob, Grep
model: sonnet
---

# Build Error Resolver Agent

你是一个构建排障专家，负责诊断和修复项目的构建与测试错误。

## 诊断能力

### 编译/构建错误
- TypeScript 类型错误
- Java 编译错误（JDK 版本不匹配、找不到符号、包不存在）
- Maven 构建失败（依赖下载失败、版本冲突、插件配置错误）
- SpringBoot 启动失败（Bean 注入、端口占用、配置缺失、数据库连接失败、中间件连接失败）
- Module not found
- 依赖版本冲突
- 配置错误（webpack/vite/eslint/prettier/Maven pom.xml）

### 测试错误
- 测试用例本身错误（断言问题）
- 环境配置问题
- Mock 配置错误
- 异步测试时序问题
- MyBatis Mapper 映射错误
- 数据库连接/兼容性错误（MySQL → 瀚高/PostgreSQL 迁移语法差异）
- 中间件连接错误（Redis 连接失败、ActiveMQ broker 不可达、Kafka broker 不可用）

### CI/CD 错误
- 本地通过但 CI 失败（环境差异）
- 并行任务失败
- 权限问题

## 诊断流程

1. 收集完整错误信息（命令、输出、环境）
2. 定位错误文件与行号
3. 分析根因（排除法 + 错误信息解读）
4. 给出修复方案（优先最小改动）
5. 验证修复成功

## 输出格式

## 诊断结果

### 错误摘要
[类型] [文件:行号] [简短描述]

### 根因
[一句话描述]

### 修复方案
1. [步骤]
2. [步骤]

### 验证
- 执行：[命令]
- 预期：[PASS/具体输出]

### 建议
[如有后续改进建议]

## 排障经验积累

遇到常见错误时，将解决方案记录到项目的 .claude/skills/troubleshooting.md，形成团队知识库。
```

---

### 7.22 skills/troubleshooting.md

**需要根据项目技术栈选择对应条目，删除不相关的排障方法。**

以下模板已覆盖常见技术栈（Java/SpringBoot/RuoYi/Vue/Python/TypeScript/MySQL/PostgreSQL/瀚高/Redis/ActiveMQ/Kafka）。如项目使用其他技术栈（Go/Rust/Django/Flask/Express/NestJS 等），请参照现有条目格式自行补充对应排障方法。

```markdown
---
name: troubleshooting
description: 常见构建与测试问题的排查与修复方法
type: skill
updated: 2026-04-22
---

# 排障知识库

> 记录团队积累的常见问题及其解决方案，持续更新。

---

## Java / SpringBoot 错误

### 编译失败：找不到符号
错误：cannot find symbol / package xxx does not exist
解决：确认 Maven 依赖是否已下载（`mvn dependency:resolve`）；检查 pom.xml 中 scope 是否为 provided/test 导致编译期缺失；IDE 需刷新 Maven 项目

### JDK 版本不匹配
错误：UnsupportedClassVersionError / source release 8 requires target release 8
解决：确认 JAVA_HOME 指向 JDK8；pom.xml 中 `<maven.compiler.source>` 和 `<maven.compiler.target>` 与实际 JDK 版本一致；IDE 中 Project SDK 配置正确

### SpringBoot 启动失败
错误：Unable to start ServletWebServerFactory / Port 8080 already in use
解决：检查端口占用（Windows: `netstat -ano | findstr 8080`）；确认 application.yml 中 server.port 配置；检查是否有多个实例未关闭

### Bean 注入失败
错误：NoSuchBeanDefinitionException / Field xxx required a bean of type xxx that could not be found
解决：确认 @ComponentScan 包路径包含目标类；检查 @Service/@Repository 注解是否遗漏；确认 MyBatis Mapper 的 @Mapper 或 @MapperScan 配置

### MyBatis 映射错误
错误：Invalid bound statement (not found) / mapper interface method not found
解决：确认 XML mapper 文件路径与 Mapper 接口包路径一致；检查 application.yml 中 mybatis.mapper-locations 配置；确认方法名与 XML 中 id 属性一致

---

## RuoYi 特定问题

### 代码生成器输出不完整
问题：生成的代码缺少某些文件或字段
解决：确认 gen_table 和 gen_table_column 数据是否完整；检查代码生成模板是否被覆盖；重新导入表结构后重新生成

### 权限/菜单不生效
问题：新增菜单或角色权限后页面看不到
解决：确认 sys_menu 表记录完整（含 perms 字段）；检查 @PreAuthorize 注解中权限标识与菜单 perms 一致；清除浏览器缓存和 Redis 缓存后重试

### 字典数据不加载
问题：下拉框为空或字典值不显示
解决：确认 sys_dict_type 和 sys_dict_data 有对应记录；检查前端 this.getDicts() 调用的字典类型编码是否正确；确认 Redis 缓存是否过期

### 跨模块依赖问题
问题：ruoyi-admin 编译报找不到 ruoyi-system 的类
解决：确认各子模块 pom.xml 中 dependency 引用正确；先 `mvn install` 安装依赖模块再到 admin 模块编译；检查 Maven reactor 构建顺序

---

## 数据库问题

### MySQL 连接失败
错误：Communications link failure / Access denied for user
解决：确认 MySQL 服务已启动（Windows: `net start mysql`）；检查 application.yml 中 spring.datasource.url/host/port/username/password；确认用户有远程访问权限（`GRANT ALL ON *.* TO 'user'@'%'`）；检查防火墙是否放行 3306 端口

### MySQL 中文乱码
问题：插入或查询中文显示问号/乱码
解决：确认连接 URL 含 `characterEncoding=utf-8` 或 `characterEncoding=UTF-8`；检查数据库/表/列的 charset 是否为 utf8mb4；确认 MySQL 配置文件中 `character-set-server=utf8mb4`

### MySQL 时区问题
错误：The server time zone value 'CST' is unrecognized
解决：连接 URL 中添加 `serverTimezone=Asia/Shanghai`；或 MySQL 配置中设置 `default-time-zone='+08:00'`

### PostgreSQL 连接失败
错误：Connection refused / FATAL: no pg_hba.conf entry
解决：确认 PostgreSQL 服务已启动（Windows: `net start postgresql-x64-XX`）；检查 pg_hba.conf 是否允许目标 IP/用户连接（添加 `host all all 0.0.0.0/0 md5`）；确认 postgresql.conf 中 `listen_addresses = '*'`；检查防火墙是否放行 5432 端口

### PostgreSQL Schema 权限问题
错误：ERROR: permission denied for schema public
解决：`GRANT ALL ON SCHEMA public TO username;`；确认搜索路径 `search_path` 包含目标 schema；检查默认表空间权限

### 瀚高（HighGo）数据库连接
问题：SpringBoot 项目需适配瀚高数据库
解决：瀚高兼容 PostgreSQL 协议，驱动使用 `com.highgo.jdbc.Driver`（或 `org.postgresql.Driver`）；JDBC URL 格式 `jdbc:highgo://host:port/database`；Maven 依赖添加 `com.highgo` 驱动包；方言设置 `hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect`；如遇关键字冲突，在 URL 中加 `stringtype=unspecified`

### 瀚高数据库特殊语法
问题：从 MySQL 迁移到瀚高后 SQL 报错
解决：瀚高/PostgreSQL 与 MySQL 语法差异需注意：自增列用 `SERIAL` 或 `GENERATED ALWAYS AS IDENTITY` 代替 `AUTO_INCREMENT`；字符串拼接用 `\|\|` 代替 `CONCAT()`；分页用 `LIMIT ... OFFSET` 代替 `LIMIT`；日期函数不同（`NOW()` 通用，`DATE_FORMAT` 需改为 `TO_CHAR`）；布尔类型用 `BOOLEAN` 代替 `TINYINT(1)`；反引号 `` ` `` 需替换为双引号 `"` 或去掉

### 数据库迁移脚本兼容性
问题：同一项目需支持 MySQL 和瀚高/PostgreSQL
解决：MyBatis 中使用 `databaseId` 区分多数据库 SQL；或使用 DatabaseProvider 动态选择 SQL 片段；Flyway/Liquibase 按数据库类型维护不同迁移脚本目录；避免使用数据库特有语法，优先使用标准 SQL

---

## Redis 问题

### Redis 连接失败
错误：Unable to connect to Redis / Could not get a resource from the pool
解决：确认 Redis 服务已启动（Windows: 下载 Redis for Windows 或使用 WSL）；检查 application.yml 中 spring.redis.host/port/password 配置；确认防火墙放行 6379 端口；如使用 Redis Sentinel/Cluster，检查 sentinel/master 节点配置

### Redis 序列化错误
错误：Cannot deserialize / SerializationException
解决：确认 RedisTemplate 配置了正确的序列化器（`StringRedisSerializer` 用于 key，`Jackson2JsonRedisSerializer` 或 `GenericJackson2JsonRedisSerializer` 用于 value）；检查存储对象是否可序列化；RuoYi 默认使用 JDK 序列化，切换为 JSON 序列化可避免类变更后反序列化失败

### Redis 缓存与数据库不一致
问题：更新数据库后缓存未同步，读取到旧数据
解决：采用「先更新数据库再删除缓存」策略；使用 @CacheEvict 注解在更新方法上同步清缓存；RuoYi 中通过 RedisCache.clearCacheByKey 手动清除；注意 Redis 过期时间设置不宜过长

### Redis OOM / 内存溢出
问题：Redis 占用内存持续增长或报 OOM
解决：设置 maxmemory 和淘汰策略（`maxmemory-policy allkeys-lru`）；检查是否有大 key（`redis-cli --bigkeys`）；为缓存键设置合理的过期时间（TTL）；RuoYi 中定期清理 sys_config/sys_dict 等缓存

---

## ActiveMQ 问题

### ActiveMQ 连接失败
错误：Could not connect to broker URL / JMSException
解决：确认 ActiveMQ 服务已启动（Windows: `activemq.bat start`）；检查 spring.activemq.broker-url 配置（默认 `tcp://localhost:61616`）；确认防火墙放行 61616 端口；Web 管理界面默认 8161 端口

### ActiveMQ 消息消费失败
问题：消息发送成功但消费者未收到
解决：确认 @JmsListener 注解的 destination 与生产者一致；检查消息序列化格式是否与消费者兼容；确认 ConnectionFactory 配置正确；检查 ActiveMQ 管理界面中是否有堆积的未消费消息（Dead Letter Queue）

### ActiveMQ 与 SpringBoot 版本兼容
问题：SpringBoot 2.x 集成 ActiveMQ 报 ClassNotFoundException
解决：确认 spring-boot-starter-activemq 版本与 SpringBoot 主版本匹配；SpringBoot 2.x 默认使用 ActiveMQ 5.x 连接池；如需自定义连接池，添加 `org.apache.activemq:activemq-pool` 依赖

---

## Kafka 问题

### Kafka 连接失败
错误：Connection to node -1 could not be established / Broker not available
解决：确认 Kafka 和 ZooKeeper 服务已启动；检查 spring.kafka.bootstrap-servers 配置；确认防火墙放行 9092 端口（Kafka）和 2181 端口（ZooKeeper）；如使用 Kafka Raft 模式（KRaft，无需 ZooKeeper），确认 quorum.voters 配置

### Kafka 消费 offset 问题
问题：消费者重复消费或跳过消息
解决：确认 spring.kafka.consumer.auto-offset-reset 配置（earliest/latest/none）；检查 consumer group 是否被意外 reset；使用 `kafka-consumer-groups.sh --describe` 查看 offset 状态；生产环境建议手动 commit offset 而非自动提交

### Kafka 生产消息失败
问题：消息发送超时或报 Not Enough Replicas
解决：确认 topic 的 min.insync.replicas 配置与实际存活 broker 数量匹配；检查 spring.kafka.producer.acks 配置（all/1/0）；增加 producer retries 和 request.timeout.ms；确认 topic 已创建（`kafka-topics.sh --list`）

### Kafka 与 SpringBoot 集成报错
问题：KafkaTemplate 注入失败或 @KafkaListener 不生效
解决：确认 spring-kafka 依赖版本与 SpringBoot 版本兼容；检查 @EnableKafka 注解是否添加；确认 KafkaTemplate 的 key/value serializer 配置；RuoYi 集成 Kafka 时需注意与现有 Redis 缓存的消息通道不冲突

---

## Vue 错误

### npm/pnpm install 失败
问题：node-sass / sass 编译失败，或 phantomjs 下载超时
解决（Vue2）：node-sass 需要 Python2 + VS Build Tools，建议替换为 dart-sass（`npm install sass` 代替 `node-sass`）
解决（Vue3）：确认 node 版本 ≥ 16；pnpm 需要 `.npmrc` 中 shamefully-hoist=true 处理幽灵依赖

### Vue2 Element UI 按需加载报错
问题：babel-plugin-component 配置后样式缺失或组件找不到
解决：确认 .babelrc 或 babel.config.js 中 styleLibraryName 路径正确；检查 element-ui 版本与插件版本兼容性

### Vue3 Vite 启动白屏
问题：Vite dev server 启动后页面空白
解决：确认 vite.config.js 中 base 配置；检查 @vitejs/plugin-vue 是否安装；确认 index.html 中 script 引用路径正确（`/src/main.ts` 不是 `/src/main.js`）

### Vue Router 路由守卫死循环
问题：页面不断重定向到同一路由
解决：检查 next() 是否在守卫中被调用且只调用一次；确认白名单路由判断逻辑正确；避免在 beforeEach 中对白名单路由再做 redirect

### ESLint + Prettier 冲突
问题：ESLint 和 Prettier 规则冲突导致格式化来回跳动
解决：安装 eslint-config-prettier 关闭与 Prettier 冲突的 ESLint 规则；安装 eslint-plugin-prettier 让 ESLint 运行 Prettier；.eslintrc.js 中 extends 末尾加上 prettier

---

## TypeScript 类型错误

### 模块找不到
错误：Cannot find module './xxx' or its type declarations
解决：检查文件路径是否正确；确认 tsconfig.json 的 paths 配置；检查文件扩展名

### 类型断言问题
错误：Argument of type 'xxx' is not assignable to parameter of type 'yyy'
解决：使用类型守卫、类型断言，或重新审查类型定义是否正确

---

## Python 错误

### ImportError / ModuleNotFoundError
问题：本地能跑但 CI 报 ImportError
解决：确认依赖在 requirements.txt/pyproject.toml 中；检查虚拟环境是否激活

### pip install 失败
问题：依赖编译失败
解决：确认系统级依赖是否安装；尝试 --no-binary 选项

---

## 依赖问题

### 幽灵依赖
问题：本地能用但 CI 报 module not found
解决：确认依赖是否在 package.json/requirements.txt/pom.xml 中，重新安装

### npm/pnpm 版本冲突
问题：安装报 peer dependency warning
解决：确认主版本一致；追踪依赖来源；必要时锁定版本

### Maven 依赖下载失败
问题：Could not transfer artifact / 下载卡住或 401
解决：确认 settings.xml 中镜像仓库（阿里云/华为云）配置正确；检查私服认证信息；删除 ~/.m2/repository 中对应目录后重试 `mvn dependency:resolve`

### Maven 依赖冲突
问题：java.lang.NoSuchMethodError / java.lang.ClassCastException 运行时才报错
解决：`mvn dependency:tree -Dverbose` 查看冲突；使用 `<exclusions>` 排除冲突传递依赖；确认子模块 pom.xml 不要重复声明父模块已有的依赖

---

## 测试问题

### 异步测试超时
问题：Test timed out
解决：增加 timeout；检查是否有死循环或未 resolve 的 Promise；确认 mock 是否正确

### Mock 不生效
问题：mock 函数没有被调用
解决：确认 mock 路径正确；检查 mock 文件命名；确认 mock 在正确位置

---

## Git 问题

### 已 merge 的分支未清理
问题：本地存在大量已合并的远程分支
解决（Unix）：git fetch --prune && git branch -d $(git branch --merged | grep -v '*')
解决（Windows PowerShell）：git fetch --prune; git branch --merged | Where-Object { $_ -notmatch '^\*' } | ForEach-Object { git branch -d $_.Trim() }

### Commit 冲突预防
规则：PR 合并前先 rebase main；多人协作时每日 rebase 一次

---

## Windows / PowerShell / CMD 问题

### PowerShell 执行策略禁止脚本运行
错误：无法加载文件 xxx.ps1，因为在此系统上禁止运行脚本
解决：以管理员身份运行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 中文路径 / 中文文件名乱码
问题：Git status / log 中中文显示为 \xxx\ 转义序列
解决：`git config --global core.quotepath false`；PowerShell 中设置 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`

### Maven 在 CMD/PowerShell 中编码错误
问题：mvn compile 输出中文乱码
解决（CMD）：`chcp 65001` 切换为 UTF-8 代码页
解决（PowerShell）：设置 `$env:JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF-8"`；或在 MAVEN_OPTS 中加 `-Dfile.encoding=UTF-8`

### 长路径问题
问题：Windows 下 node_modules 路径超过 260 字符导致删除/安装失败
解决：启用长路径支持 `git config --global core.longpaths true`；删除时使用 `npx npkill` 或 `rimraf`；注册表启用长路径（`HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled` = 1）

### pnpm 在 Windows 上的硬链接问题
问题：pnpm install 报 EPERM 或 EXDEV 错误
解决：确认项目不在 FAT32 分区（NTFS 才支持硬链接）；`.npmrc` 中设置 `store-dir=C:\.pnpm-store` 避免路径过长

---

## Vue Router 动态路由问题

### 菜单路由返回 404
问题：后端菜单数据正确，但前端导航到动态路由返回 404 页面
原因：一级菜单的 path 未以 `/` 开头，Vue Router 无法识别为根路由
解决：
```sql
-- 错误配置
INSERT INTO system_menu (path, ...) VALUES ('calendarEvent', ...);

-- 正确配置（path 必须以 / 开头）
INSERT INTO system_menu (path, ...) VALUES ('/calendarEvent', ...);
```
关键点：Vue Router 的根路由 path 必须以 `/` 开头，否则会被当作相对路径处理

### 菜单 component 路径与实际文件不匹配
问题：菜单配置的 component 路径找不到对应 Vue 文件
排查：检查 `src/views/` 下是否存在对应文件
解决：确认 component 字段值与 `src/views/` 下的文件路径一致
```sql
-- component 值 'business/calendar/index' 对应文件：
-- src/views/business/calendar/index.vue
```

---

## Playwright E2E 测试问题

### waitForLoadState('networkidle') 永远超时
问题：测试在 `await page.waitForLoadState('networkidle')` 处超时
原因：后台有持续的轮询请求（如消息通知、WebSocket 心跳），导致 networkidle 永远无法达到
解决：
```javascript
// 错误：依赖 networkidle
await page.goto('/some-page');
await page.waitForLoadState('networkidle');

// 正确：使用 domcontentloaded + 显式元素等待
await page.goto('/some-page');
await page.waitForSelector('button:has-text("新增")', { timeout: 10000 });
```

### Element UI 组件选择器返回 hidden
问题：`locator('.el-table').first()` 或 `locator('table')` 返回 hidden 状态
原因：Element UI 的 el-table 组件内部有多个 table 元素，第一个可能是隐藏的表头或辅助元素
解决：
```javascript
// 错误：el-table 可能返回隐藏元素
await expect(page.locator('.el-table').first()).toBeVisible();

// 正确：使用业务关键元素作为验证点
await expect(page.locator('button:has-text("新增")')).toBeVisible();
await expect(page.locator('button:has-text("搜索")')).toBeVisible();
```

### afterEach 钩子超时
问题：测试本身通过，但 afterEach 中的清理逻辑超时
原因：afterEach 中使用了 `waitForLoadState('networkidle')`
解决：
```javascript
// 错误
test.afterEach(async ({ page }) => {
  await page.waitForLoadState('networkidle'); // 可能永远等待
  // ...
});

// 正确
test.afterEach(async ({ page }) => {
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(300); // 等待微任务完成
  // ...
});
```

### 测试账号不存在导致测试失败
问题：使用普通用户账号测试，但账号不存在
解决：添加异常处理，优雅跳过
```javascript
try {
  await login(page, TEST_ACCOUNTS.user);
  // ... 测试逻辑
} catch (e) {
  console.log('测试跳过: user 账号可能不存在');
}
```

---

## SpringBoot 微服务启动问题

### 微服务端口未配置，默认使用 8080
问题：启动微服务时报 Port 8080 already in use，或多个服务争抢同一端口
原因：application-local.yaml 未配置 server.port，使用了默认的 8080
解决：在每个微服务的 application-local.yaml 中显式配置端口
```yaml
# yudao-gateway/src/main/resources/application-local.yaml
server:
  port: 48080

# yudao-module-system/.../application-local.yaml
server:
  port: 48081

# yudao-module-infra/.../application-local.yaml
server:
  port: 48082

# yudao-module-business/.../application-local.yaml
server:
  port: 48083
```

### ClassNotFoundException: AuthRegisterReqVO
问题：启动某个微服务时报 ClassNotFoundException
原因：依赖模块未编译安装到本地 Maven 仓库
解决：
```bash
# 在项目根目录执行
mvn clean install -DskipTests
```

### Nacos 配置找不到
问题：启动时报 `config[dataId=xxx-local.yaml, group=DEFAULT_GROUP] is empty`
原因：本地开发未在 Nacos 创建对应配置，或 namespace 不匹配
解决：
1. 确认 application-local.yaml 存在且配置正确（本地开发优先使用本地配置）
2. 如需使用 Nacos 配置，确认 namespace 和 group 正确

---

## Docker MySQL 字符集问题

### 客户端字符集导致中文乱码
问题：通过 `docker exec mysql` 执行含中文的 SQL，数据库存储为乱码
原因：MySQL 客户端默认字符集为 latin1，与数据库 utf8mb4 不匹配
排查：
```bash
# 检查客户端字符集
docker exec <container> mysql -uroot -p123456 -e "SHOW VARIABLES LIKE 'character%';"
# 典型问题输出：
# character_set_client     = latin1  ← 问题所在
# character_set_connection = latin1  ← 问题所在
# character_set_results    = latin1  ← 问题所在
# character_set_database   = utf8mb4
```
解决：
```bash
# 方案1：执行 SQL 时指定字符集
docker exec <container> mysql -uroot -p123456 --default-character-set=utf8mb4 <db> -e "INSERT INTO table (name) VALUES ('中文');"

# 方案2：在 SQL 文件开头添加字符集声明
cat > script.sql << 'EOF'
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

INSERT INTO table (name) VALUES ('中文');
EOF

docker exec -i <container> mysql -uroot -p123456 --default-character-set=utf8mb4 <db> < script.sql
```
关键点：即使数据库和表都是 utf8mb4，客户端连接字符集不对仍会导致乱码

---

## 微服务架构排障经验

### 新微服务 Bean 注入失败
问题：新微服务启动报 `NoSuchBeanDefinitionException: No qualifying bean of type 'List<AuthorizeRequestsCustomizer>'`
根因：框架级 Security 配置需要至少一个 AuthorizeRequestsCustomizer bean，新模块缺少依赖
解决：对比同类模块（system/infra）的 pom.xml，添加 websocket 等框架依赖

### 网关未启动导致前端 500
问题：前端 API 请求全部 500，但后端服务正常
原因：前端配置 `VUE_APP_BASE_API` 指向网关，网关未启动
解决：确保启动顺序——基础设施 → 后端服务 → 网关 → 前端

### Node.js 版本不兼容
问题：前端编译报错 `error:0308010C:digital envelope routines::unsupported`
原因：Node.js 17+ 更改了 OpenSSL 默认配置，与旧版 webpack 不兼容
解决：`NODE_OPTIONS=--openssl-legacy-provider npm run local` 或降级 Node.js 到 16.x

---

## 问题定位决策树

```
页面 404
├── URL 是否正确？ → 检查菜单 path 配置（一级必须以 / 开头）
├── 组件文件是否存在？ → 检查 src/views/ 目录
├── 路由是否注册？ → 浏览器控制台检查 $router.getRoutes()
└── 网关是否启动？ → curl 网关地址

API 500
├── 后端服务是否启动？ → curl 直接访问后端端口
├── 网关是否启动？ → curl 网关地址
├── 数据库连接是否正常？ → 检查后端日志
└── Nacos 是否注册？ → 检查服务注册列表

菜单乱码
├── 数据库存储是否正常？ → mysql 客户端直接查询
├── API 返回是否正常？ → curl 检查响应
└── 字符集配置是否正确？ → SHOW VARIABLES LIKE 'character%'

微服务启动失败
├── Bean 注入失败？ → 对比同类模块的 pom.xml 依赖
├── 端口被占用？ → netstat 检查端口
└── 配置找不到？ → 检查 application-local.yaml
```

---

## 排障经验总结

1. **先检查基础设施**：Nacos、MySQL、Redis 是否正常运行
2. **端口冲突是常见问题**：使用 netstat 检查，确保配置文件显式指定端口
3. **E2E 测试不要依赖 networkidle**：后台轮询请求会导致永远无法达到该状态
4. **Vue Router 根路由必须以 / 开头**：这是动态菜单配置的常见错误
5. **Element UI 组件选择器需谨慎**：组件内部结构复杂，优先选择业务关键元素
6. **Docker MySQL 执行 SQL 必须指定字符集**：客户端默认 latin1 会导致中文乱码
7. **新增微服务对比同类模块依赖**：避免因缺少框架级依赖导致启动失败
8. **网关是前端请求入口**：微服务架构下前端不直连后端，必须经过网关
9. **Node.js 版本兼容性**：注意 Node 17+ 与旧版 webpack 的 OpenSSL 兼容问题
```

---

### 7.23 settings.json

**需要替换所有 `{{...}}` 占位符，填入包管理器、文件扩展名和格式化命令。**

> ⚠️ **环境选择**：
> - Linux / macOS / WSL / Git Bash：使用下方「bash 版本」
> - Windows PowerShell（无 jq）：使用下方「PowerShell 版本」
> - 两者功能等价，根据环境选择其一，不要混用

| 占位符 | 说明 | 示例值 |
|--------|------|--------|
| `{{包管理器}}` | 项目包管理器（多包管理器用 `|` 连接，JSON中写作 `\\|`） | `mvn|pnpm` 或 `pip` |
| `{{文件扩展名}}` | 项目代码文件扩展名正则（使用 `|` 连接） | `(java|xml|vue|js|py)$` 或 `(ts|tsx|js|jsx)$` |
| `{{格式化命令}}` | 项目格式化命令（如无则填 `echo 无格式化命令`） | `pnpm format` 或 `mvn spotless:apply` |

> **多包管理器说明**：前后端分离项目（如 RuoYi）通常有 Maven（后端）+ pnpm（前端），此时 `{{包管理器}}` 填为 `mvn|pnpm`，并将 allow 中的 `Bash({{包管理器}} **)` 替换为两行：`Bash(mvn **)` 和 `Bash(pnpm **)`。
>
> **正则转义说明**：在 grep 正则中使用 `|`（无反斜杠），在 JSON 字符串中需要双写 `\\|`。例如 `mvn|pnpm` 在 JSON 中写作 `mvn\\|pnpm`（JSON 解析后变成 `mvn\|pnpm`，grep 解释为 `mvn|pnpm`）。

> **格式说明**：permissions 使用 `ToolName(pattern)` 语法，`**` 匹配任意参数。hooks 使用 `PreToolUse`/`PostToolUse` 事件，`matcher` 为正则匹配工具名，hooks 通过 shell 命令实现拦截或提示。
>
> **依赖声明**：bash 版 Hook 依赖 `jq`（JSON 解析工具）。Windows 需预装 jq（`choco install jq` 或从 [stedolan.github.io/jq](https://stedolan.github.io/jq/) 下载）。如未安装 jq，请使用 PowerShell 版本。

```json
{
  "permissions": {
    "allow": [
      "Bash({{包管理器}} **)",
      "Bash(git **)",
      "Bash(node **)"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(rm -rf /*)",
      "Edit(**/.env)",
      "Write(**/.env)",
      "Edit(**/.mcp.json)",
      "Write(**/.mcp.json)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'if ! command -v jq &>/dev/null; then echo 0; exit 0; fi; input=$(cat); [ -z \"$input\" ] && { echo 0; exit 0; }; cmd=$(echo \"$input\" | jq -r .command 2>/dev/null || echo \"\"); if [ -n \"$cmd\" ] && echo \"$cmd\" | grep -qE \"^({{包管理器}})\\s+(install|i|package)\"; then echo \"⚠️ 依赖安装/构建提醒：长耗时命令，建议在 tmux/screen 中运行，避免会话中断。\" >&2; fi; echo 0'"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "(Edit|Write)",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'if ! command -v jq &>/dev/null; then echo 0; exit 0; fi; input=$(cat); [ -z \"$input\" ] && { echo 0; exit 0; }; tool=$(echo \"$input\" | jq -r .tool_name 2>/dev/null || echo \"\"); file=$(echo \"$input\" | jq -r .tool_input.file_path 2>/dev/null || echo \"\"); if [ -n \"$file\" ] && echo \"$file\" | grep -qE \"{{文件扩展名}}\"; then echo \"✅ $tool 代码文件：$file — 请运行 {{格式化命令}} 检查格式规范。\" >&2; fi; if [ -n \"$file\" ] && echo \"$file\" | grep -qE \"application-.*\\.yml$\"; then echo \"⚠️ 配置文件：$file — 请确认未写入明文密码/密钥（遵循 security.md 🔴 规则）。\" >&2; fi; if [ -n \"$file\" ] && echo \"$file\" | grep -qE \"^\\.claude/\" && [ -f \"$file\" ] && grep -q \"{{.*}}\" \"$file\" 2>/dev/null; then echo \"⚠️ 配置文件 $file 包含未替换的占位符（如 {{项目名称}}），请替换为实际值。\" >&2; fi; echo 0'"
          }
        ]
      }
    ]
  }
}
```

> **Hook 行为说明**：
> - `PreToolUse`：工具执行前触发。退出码 `2` 阻断工具调用（相当于 block），退出码 `0` 放行。stdin 接收 JSON 格式的工具输入。
> - `PostToolUse`：工具执行后触发。退出码不影响已执行的操作，适合做提醒和日志。
> - 前 2 周所有 Hook 始终 `echo 0`（仅 stderr 输出提醒，不阻断）。升级时将依赖安装 hook 的匹配分支改为 `echo 2` 即可切换为阻断型。
>
> **Hook 升级路径**（对应第五章）：
> | 时间点 | PreToolUse 退出码 | PostToolUse 行为 | 效果 |
> |--------|-------------------|-----------------|------|
> | 第 1-2 周 | 始终 `echo 0`（仅 stderr 输出提醒） | stderr 提醒「请运行格式化命令」 | 提醒型，不阻断 |
> | 第 3 周 | 依赖安装 hook 匹配分支改为 `echo 2` | 将提醒替换为实际执行格式化命令：`{{格式化命令}}` | 一致性型，自动格式化 |
> | 稳定后 | 安全相关 hook 增加 `echo 2` 逻辑 | 保持一致性型 | 高频违规项阻断 |

**第 3 周升级示例 — 一致性型：**

将 PostToolUse hook 中 stderr 提醒替换为实际执行格式化命令，编辑代码文件后自动格式化：

```json
{
  "matcher": "(Edit|Write)",
  "hooks": [
    {
      "type": "command",
      "command": "bash -c 'if ! command -v jq &>/dev/null; then echo 0; exit 0; fi; input=$(cat); [ -z \"$input\" ] && { echo 0; exit 0; }; tool=$(echo \"$input\" | jq -r .tool_name 2>/dev/null || echo \"\"); file=$(echo \"$input\" | jq -r .tool_input.file_path 2>/dev/null || echo \"\"); if [ -n \"$file\" ] && echo \"$file\" | grep -qE \"{{文件扩展名}}\"; then fmt_cmd=\"{{格式化命令}}\"; if [ \"$fmt_cmd\" = \"echo 无格式化命令\" ]; then :; elif command -v ${fmt_cmd%% *} &>/dev/null; then $fmt_cmd || echo \"⚠️ 格式化命令执行失败: $fmt_cmd\" >&2; else echo \"⚠️ 未找到格式化命令: $fmt_cmd，请手动格式化\" >&2; fi; fi; if [ -n \"$file\" ] && echo \"$file\" | grep -qE \"application-.*\\.yml$\"; then echo \"⚠️ 配置文件：$file — 请确认未写入明文密码/密钥（遵循 security.md 🔴 规则）。\" >&2; fi; if [ -n \"$file\" ] && echo \"$file\" | grep -qE \"^\\.claude/\" && [ -f \"$file\" ] && grep -q \"{{.*}}\" \"$file\" 2>/dev/null; then echo \"⚠️ 配置文件 $file 包含未替换的占位符（如 {{项目名称}}），请替换为实际值。\" >&2; fi; echo 0'"
    }
  ]
}
```

> **变更点**：
> - 将 `echo \"✅ ... 请运行 {{格式化命令}} ...\"` 替换为直接执行格式化命令
> - 新增格式化命令存在性检查：`command -v ${fmt_cmd%% *}`（提取命令名部分检查是否存在）
> - 新增格式化命令执行失败处理：输出警告而非静默失败
> - 如果项目无格式化命令（`echo 无格式化命令`），跳过格式化步骤

**稳定后升级示例 — 阻断型：**

在 PreToolUse 中增加安全配置文件编辑拦截，尝试编辑 `.env` 或 `application-*.yml` 时直接阻断：

```json
{
  "matcher": "(Edit|Write)",
  "hooks": [
    {
      "type": "command",
      "command": "bash -c 'if ! command -v jq &>/dev/null; then echo 0; exit 0; fi; input=$(cat); [ -z \"$input\" ] && { echo 0; exit 0; }; file=$(echo \"$input\" | jq -r .tool_input.file_path 2>/dev/null || echo \"\"); if [ -n \"$file\" ] && echo \"$file\" | grep -qE \"(.env|.mcp.json)$\"; then echo \"🔴 安全红线：禁止编辑敏感配置文件 $file（遵循 security.md 🔴 规则）\" >&2; echo 2; elif [ -n \"$file\" ] && echo \"$file\" | grep -qE \"application-.*\\.yml$\"; then echo \"⚠️ 配置文件：$file — 请确认未写入明文密码/密钥（遵循 security.md 🔴 规则）。\" >&2; echo 0; else echo 0; fi'"
    }
  ]
}
```

> **变更点**：
> - `.env` / `.mcp.json` 编辑时 `echo 2` 直接阻断
> - `application-*.yml` 仍为提醒型（因团队可能需要合法编辑配置文件）
> - 新增 jq 依赖检测和空输入处理
> - 根据团队实际情况调整阻断范围

**Windows PowerShell 版 Hook（无需 jq 依赖）：**

> 如果 Windows 环境未安装 jq，可将上述 bash hook 替换为以下 PowerShell 版本。PowerShell 使用 `ConvertFrom-Json` 内置解析，无需额外依赖。

PreToolUse — 依赖安装提醒（PowerShell 版）：

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "powershell -Command \"$input=[Console]::In.ReadToEnd(); if(-not$input){echo 0; exit}; try{$j=$input|ConvertFrom-Json}catch{echo 0; exit}; if($j.command-and$j.command-match'^({{包管理器}})\\s+(install|i|package)'){Write-Host '⚠️ 依赖安装/构建提醒：长耗时命令，建议在 tmux/screen 中运行，避免会话中断。'}; echo 0\""
    }
  ]
}
```

PostToolUse — 代码文件格式化提醒（PowerShell 版）：

```json
{
  "matcher": "(Edit|Write)",
  "hooks": [
    {
      "type": "command",
      "command": "powershell -Command \"$input=[Console]::In.ReadToEnd(); if(-not$input){echo 0; exit}; try{$j=$input|ConvertFrom-Json}catch{echo 0; exit}; $f=$j.tool_input.file_path; if(-not$f){echo 0; exit}; if($f-match'{{文件扩展名}}'){Write-Host ('✅ '+$j.tool_name+' 代码文件：'+$f+' — 请运行 {{格式化命令}} 检查格式规范。')}; if($f-match'application-.*\\.yml$'){Write-Host ('⚠️ 配置文件：'+$f+' — 请确认未写入明文密码/密钥（遵循 security.md 🔴 规则）。')}; if($f-match'^\\.claude/'-and(Test-Path$f)){if((Get-Content$f-Raw)-match'{{.*}}'){Write-Host ('⚠️ 配置文件 '+$f+' 包含未替换的占位符（如 {{项目名称}}），请替换为实际值。')}}; echo 0\""
    }
  ]
}
```

> **PowerShell 版本改进**：
> - 新增 `$input` 空值检查：`if(-not$input)` 防止空输入导致异常
> - 新增 `try-catch` 包裹 `ConvertFrom-Json`：防止非 JSON 输入导致异常
> - 新增 `$f` null 检查：`if(-not$f)` 防止文件路径为空
> - 新增 `Test-Path $f` 检查：确保文件存在后再读取内容
> - 所有异常情况都输出 `echo 0` 继续执行，不阻断工作流

> **选择方式**：项目在 Linux/macOS 或已安装 jq 的 Windows 环境使用 bash 版；未安装 jq 的 Windows 环境使用 PowerShell 版。两者功能等价，不要混用。

**文件扩展名正则参考：**

> **正则格式说明**：
> - grep 正则使用 `|` 连接多个扩展名，如 `(ts|tsx|js|jsx)$`
> - 在 JSON 字符串中需双写 `\\|`，最终 grep 解析为 `|`

| 技术栈 | grep 正则（JSON 中写作） | permissions 正则 |
|--------|-------------------------|-----------------|
| Node.js 前端 | `(ts\|tsx\|js\|jsx)$` | `**/*.ts` `**/*.tsx` `**/*.js` `**/*.jsx` |
| Node.js 后端 | `(ts\|js)$` | `**/*.ts` `**/*.js` |
| Python | `py$` | `**/*.py` |
| Java / SpringBoot | `(java\|xml)$` | `**/*.java` `**/*.xml` |
| Vue（前端） | `(vue\|js\|ts)$` | `**/*.vue` `**/*.js` `**/*.ts` |
| RuoYi（前后端） | `(java\|xml\|vue\|js\|sql)$` | `**/*.java` `**/*.xml` `**/*.vue` `**/*.js` `**/*.sql` |
| 数据库项目（含迁移脚本） | `(java\|xml\|sql)$` | `**/*.java` `**/*.xml` `**/*.sql` |
| 全栈（Java+Vue+Python） | `(java\|xml\|vue\|js\|py)$` | `**/*.{java,xml,vue,js,py}` |

---

### 7.24 .mcp.json.example

**按需增减 MCP 服务，不需要填入真实凭证。**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./src"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "mysql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-mysql"],
      "env": {
        "MYSQL_HOST": "${MYSQL_HOST}",
        "MYSQL_PORT": "${MYSQL_PORT}",
        "MYSQL_USER": "${MYSQL_USER}",
        "MYSQL_PASSWORD": "${MYSQL_PASSWORD}",
        "MYSQL_DATABASE": "${MYSQL_DATABASE}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${POSTGRES_CONNECTION_STRING}"
      }
    },
    "redis": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-redis"],
      "env": {
        "REDIS_URL": "${REDIS_URL}"
      }
    }
  }
}
```

> **瀚高数据库说明**：瀚高兼容 PostgreSQL 协议，可直接使用 PostgreSQL MCP server，将连接字符串中的 host/port 指向瀚高实例即可。格式：`postgresql://user:password@host:port/database`
>
> **Redis 说明**：`REDIS_URL` 格式为 `redis://user:password@host:port/db`，如无密码则 `redis://host:port/db`。RuoYi 项目 Redis 为标配组件，建议保留此配置。

按需增减 MCP 服务，不用的删掉即可。将本文件复制为 `.mcp.json`，并设置对应环境变量。真实凭证不提交 Git。

> **版本检查**：MCP server 包更新频繁，使用前建议运行 `npx @modelcontextprotocol/server-xxx --version` 或查看 [npm](https://www.npmjs.com/) 上的最新版本。

**常见可选 MCP 服务**（按项目需要添加）：
- ActiveMQ：用于消息队列监控和调试
- Kafka：用于 Topic 查看和消息追踪
- Sentry：用于错误监控集成
- Puppeteer：用于 E2E 测试场景
- Docker：用于容器化项目

---

### 7.25 .gitignore 追加

**追加敏感文件条目到项目 .gitignore，防止凭证泄露。**

```bash
echo -e "\n# Claude Code\n.mcp.json\n.env\napplication-*.yml" >> .gitignore
```

> **Windows CMD 替代**：`echo. >> .gitignore && echo # Claude Code >> .gitignore && echo .mcp.json >> .gitignore && echo .env >> .gitignore && echo application-*.yml >> .gitignore`
> **Windows PowerShell 替代**：`Add-Content .gitignore "`n# Claude Code`n.mcp.json`n.env`napplication-*.yml"`

如果已有这些条目则跳过。`application-*.yml` 通配符覆盖所有环境配置文件（-dev、-prod、-test、-staging 等），包含数据库密码、Redis 密码等敏感配置，不应提交到 Git。如项目使用 `.yaml` 扩展名而非 `.yml`，需额外添加 `application-*.yaml`。

---

### 7.26 .claude/templates/spec/requirements.md

**Spec 需求文档模板，初始化时直接创建，不需要改造。**

> **模板内容**：见 **附录 C.1**（第 3698 行起）。初始化时将附录内容复制到 `.claude/templates/spec/requirements.md`。

---

### 7.27 .claude/templates/spec/design.md

**Spec 设计文档模板，初始化时直接创建，不需要改造。**

> **模板内容**：见 **附录 C.2**（附录 C.1 之后）。初始化时将附录内容复制到 `.claude/templates/spec/design.md`。

---

### 7.28 .claude/templates/spec/tasks.md

**Spec 任务清单模板，初始化时直接创建，不需要改造。**

> **模板内容**：见 **附录 C.3**（附录 C.2 之后）。初始化时将附录内容复制到 `.claude/templates/spec/tasks.md`。
>
> **说明**：tasks.md 中的测试用例文档任务（T-DOC-xxx 系列）对应 test-cases.md 中的测试用例，实现前必须先完成测试用例文档编写。

---

### 7.29 .claude/templates/spec/test-cases.md

**Spec 测试用例文档模板（测试先行核心），初始化时直接创建，不需要改造。**

> **模板内容**：见 **附录 D**（附录 C 之后）。初始化时将附录内容复制到 `.claude/templates/spec/test-cases.md`。
>
> **说明**：此模板为新增，用于在 design.md 和 tasks.md 之间补充测试用例文档。每个验收条件（AC）必须有对应的测试用例。

> **使用流程**：以上四个模板文件在初始化时创建到 `.claude/templates/spec/` 目录。当用户确认需求后，AI 读取这些模板，在 `.claude/specs/<feature>/` 下创建对应的 Spec 文件。

---

## 八、避坑检查清单

提交 PR 前逐项确认：

### 基础配置

- [ ] **Steer 文件填入实际信息** — foundation/ 中的 5 个文件（product.md、tech.md、structure.md、never.md、quality-gate.md）和 domain/ 中的 3 个文件必须填入项目真实信息，不能留 `{{占位符}}`
- [ ] **quality-gate.md 占位符已替换** — 门禁清单中的 `{{构建命令}}`、`{{测试命令}}`、`{{覆盖率命令}}`、`{{E2E测试命令}}`、`{{包管理器}}` 等占位符已填入实际命令
- [ ] **Steer 文件 fileMatch 模式正确** — domain/ 中的 api.md 和 testing.md 的 fileMatchPattern 必须匹配实际项目文件路径；security.md 使用 auto 类型，无需 fileMatchPattern
- [ ] **CLAUDE.md 从代码提炼** — 不凭空写，正文力求精简
- [ ] **rules 分档** — 🔴 只放安全相关，🟡 放新代码要求，🟢 放逐步达标项
- [ ] **不把旧代码做不到的写成 🔴** — 旧代码覆盖率 0%，不能写「覆盖率必须 80%」为 🔴
- [ ] **hooks 前 2 周提醒型** — 不直接阻断，给团队适应期
- [ ] **Hook 升级路径可执行** — 确认 `{{格式化命令}}` 占位符已填入实际命令，第 3 周一致性型升级有明确实施方案（如项目无格式化命令，PostToolUse 保持提醒型）
- [ ] **.mcp.json 不提交真实凭证** — 只提交 .mcp.json.example，deny 列表已包含 `.mcp.json` 编辑/写入拦截
- [ ] **.gitignore 添加 .mcp.json、.env、application-dev.yml、application-prod.yml**
- [ ] **troubleshooting.md 适配技术栈** — 删除不相关的条目
- [ ] **build-error-resolver.md 适配技术栈** — 删除诊断能力中不相关的技术栈条目
- [ ] **settings.json 匹配实际工具链** — 包管理器、文件扩展名、格式化命令
- [ ] **PR 描述作为 team review 材料** — 包含文件说明和 review 重点
- [ ] **不照搬模板** — 每条 rule 结合项目实际调整
- [ ] **Steer + Spec + Hooks 三层防护** — Steer 提供规则，Spec 提供流程，Hooks 提供自动校验，缺任何一层都有漏洞
- [ ] **配置回滚方案** — 保留初始分支，如团队反对可快速回退（`git revert` 或删除 .claude/ 目录）
- [ ] **Windows 兼容** — troubleshooting.md 中 Git 命令需提供 PowerShell 替代方案
- [ ] **Spec 模板文件已创建** — 确认 `.claude/templates/spec/` 下有 4 个模板文件（requirements.md、design.md、**test-cases.md**、tasks.md）
- [ ] **test-cases.md 模板存在** — 确认包含测试用例结构（UT/E2E 用例表、全局错误监听、三层验证）
- [ ] **tasks.md 模板包含测试任务** — 确认包含 T-DOC-xxx（测试用例文档）、T-UT-xxx（单元测试代码）、T-E2E-xxx（E2E 测试代码）、T-UT-101/T-E2E-101（统一测试执行）
- [ ] **specs 空目录已创建** — 确认 `.claude/specs/` 目录存在，用于存放功能级 Spec 文件

### 智能体质量门禁新增检查项

- [ ] **后端 nil 集合兜底** — API 响应层拦截 nil，返回空数组 `[]` 或空列表
- [ ] **前端防御性数据消费** — `data ?? []`、可选链、禁止裸赋值
- [ ] **测试三层验证** — 页面可达 + 数据加载 + 数据渲染非空
- [ ] **测试数据覆盖** — 关键角色组合（至少：超级管理员、普通用户、无权限用户）+ "无数据"用户 + seed 脚本幂等
- [ ] **全局错误监听** — pageerror + console.error + 微任务等待
- [ ] **需求追踪矩阵** — RTM 零空白才交付
- [ ] **Agent 编排** — 串行保证正确性，prompt 自包含，写文件≤60行
- [ ] **覆盖率审计独立** — 编写测试的 agent 不能自己审计覆盖率
- [ ] **前后端权限同步** — 路由守卫与 API 权限一致
- [ ] **配置文件无 {{占位符}} 残留** — grep 检查 .claude/ 目录确认所有占位符已填入实际信息
- [ ] **质量门禁全绿** — 10 项检查全部通过才交付

---

## 附录 A：编码行为准则详细解读

> 来源：[Andrej Karpathy's CLAUDE.md](https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md)
>
> **Tradeoff**：这些准则偏向审慎而非速度。对于简单任务，自行判断适用程度。
>
> **这些准则生效的标志**：diff 中不必要变更减少，因过度复杂导致的重写减少，澄清问题在实现前提出而非出错后补救。

### A.1 先想后写（Think Before Coding）

不要假设，不要隐藏困惑，把权衡摆到台面上。

- 实现前先显式陈述假设。如果不确定，先问。
- 如果存在多种解读，全部列出来——不要默默选一个。
- 如果存在更简单的方案，说出来。该反驳时就反驳。
- 如果某件事不清楚，停下来。说出困惑点，再问。

### A.2 简洁优先（Simplicity First）

只写解决问题所需的最少代码，不做任何推测性设计。

- 不添加未被要求的功能。
- 不为单次使用的代码创建抽象。
- 不添加未被要求的"灵活性"或"可配置性"。
- 不为不可能发生的场景写错误处理。
- 如果你写了 200 行但 50 行就能搞定，重写。

> 问自己：「资深工程师会说这过于复杂吗？」如果是，简化。

### A.3 精准改动（Surgical Changes）

只动必须动的，只清理自己造成的。

- 编辑已有代码时：
  - 不要"改进"相邻的代码、注释或格式。
  - 不要重构没坏的东西。
  - 匹配已有风格，即使你会用不同方式。
  - 如果你注意到无关的死代码，提一句——不要删。
- 当你的改动产生了孤立代码：
  - 移除你的改动导致的无用 import/变量/函数。
  - 不要移除之前就存在的死代码，除非被要求。

> 测试标准：每一行变更都应该能直接追溯到用户的需求。

### A.4 目标驱动（Goal-Driven Execution）

定义成功标准，循环直到验证通过。

将任务转化为可验证的目标：

| 模糊描述 | 明确目标 |
|----------|---------|
| "加验证" | "先写无效输入的测试，再让它们通过" |
| "修 Bug" | "先写能复现的测试，再让它通过" |
| "重构 X" | "确保重构前后测试都通过" |

多步骤任务，先简述计划：

```
1. [步骤] → 验证: [检查方式]
2. [步骤] → 验证: [检查方式]
3. [步骤] → 验证: [检查方式]
```

> 强成功标准让你能独立循环。弱标准（"让它能跑"）则需要不断确认。

---

## 附录 B：Steering 文件与 Spec 工作流详解

> 来源：AWS Kiro 实战培训（2026-03）——「直接用最贵的模型，但要先做好工程化」

### B.1 为什么需要 Steering 文件

每次新会话，AI 对项目像一个"第一天入职的新同事"。没有 Steering 时，它要先浏览一圈——列目录、开文件、从零构建理解。这段"入职熟悉"的过程就是 Token 被消耗的地方。

Steering 文件的本质是把"熟悉项目的维护者脑子里的地图"压缩成一小段稳定的上下文。

**收益不仅是省 Token，更是精准**：
- 选正确的修改层级
- 避免改写不相关的部分
- 与团队约定保持一致
- 更少的探索更快定位正确文件

### B.2 Steering 文件目录结构与加载模式

在 `.claude/steer/` 目录下创建 Steering 文件，支持四种加载模式：

```
.claude/
└─ steer/
   ├─ foundation/          # always 类型，每次会话加载
   │   ├─ product.md       # 产品/项目概述
   │   ├─ tech.md          # 技术栈与架构
   │   ├─ structure.md     # 目录结构 + 修改导航
   │   ├─ never.md         # NEVER 列表（禁止行为）
   │   └─ quality-gate.md  # 质量门禁清单
   ├─ domain/              # fileMatch/auto 类型，按需加载
   │   ├─ api.md          # API 开发规范
   │   ├─ testing.md       # 测试规范
   │   ├─ security.md      # 安全规范
   │   └─ frontend.md      # 前端规范（可选，按需创建）
   └─ reference/          # manual 类型，手动引用（可选，按需创建）
       └─ openapi.yaml    # 大型参考文档
```

**front-matter 格式（fileMatch/auto 类型需要）**：
```yaml
---
inclusion: fileMatch
fileMatchPattern: ["src/api/**/*.ts", "src/api/**/*.tsx"]
---
# API 开发规范
```

**推荐领域拆分**：

| 文件 | fileMatchPattern | 内容 |
|------|-----------------|------|
| security.md | `["src/**/*.ts"]` | 禁止记录 PII、参数化查询、Zod 校验 |
| frontend.md | `["src/components/**", "src/ui/**"]` | 设计系统组件、CSS modules、无障碍 |
| testing.md | `["tests/**", "**/*.test.ts"]` | 测试规范、mock 策略、回归要求 |
| api-standards.md | `["src/api/**"]` | RESTful 规范、错误处理、响应格式 |

**auto 类型示例**：
```yaml
---
inclusion: auto
name: database-patterns
description: 数据库操作模式和 ORM 使用规范。在创建或修改数据库相关代码时使用。
---
# 数据库操作规范
- 使用 Prisma ORM，禁止原生 SQL
- 所有查询必须在 repository 层
- 批量操作使用事务
```

### B.3 Steering 文件编写指南

**好的 Steering 文件**看起来像你给"明天就会失忆的自己"留的笔记：
- 只记那些不明显的、容易踩坑的、项目特有的东西
- 不解释 AI 已知的常识

**高价值内容清单**：

```markdown
# 项目核心规则

## 构建与运行
- 包管理器：pnpm
- 构建：pnpm build
- 测试：pnpm test --run
- Lint：pnpm lint

## 目录结构（关键模块）
- src/api/ — HTTP 处理、路由
- src/domain/ — 核心业务规则
- src/infra/ — 数据库适配器、外部集成

## 修改导航（改 X 去哪里改）
- 新增 API endpoint：在 src/api/routes.ts 加路由，handler 写在 src/api/handlers/*
- 修改定价规则：改 src/domain/billing/pricing.ts，同步更新对应测试

## 架构决策记录
- 选择 Prisma 而非 TypeORM，因为类型安全更好
- 正在从 REST 迁移到 GraphQL；新接口优先走 GraphQL

## NEVER
- 不要修改 src/generated/ 下的文件
- 不要在组件中写业务逻辑
- 禁止 any 类型
```

**「修改导航」是 ROI 最高的内容**：人类维护者知道"改定价就去 pricing.ts"，把这种经验写成导航规则，能让 AI 不必打开一堆无关文件就能直达目标。

**"纠正两次就写入 Steer"飞轮**：

每次在同一个问题上纠正 AI 两次，就停下来把它写进 Steer 文件。

```
AI 犯错 → 你审查 → 改进 Steer → AI 下次变得更好
     ↑                                      ↓
     ←←←←←← 复合改进积累 ←←←←←←←←←←←
```

**定期同步**：Steer 文件应随项目演进更新——架构变了、迁移了新技术栈，都要及时更新。

### B.4 Spec 工作流详解

**Spec 的核心价值**：天然实现"先思考再动手"的纪律，同时大幅减少因反复澄清而浪费的 Token。

**自由对话的成本**：
```
你：帮我加个用户通知功能
AI：实现了一个方案
你：不对，我要的是邮件通知，不是站内信
AI：重新实现
你：频率限制呢？
AI：补上频率限制
你：等等，还需要用户偏好设置...
```
每一轮"不对"和"还需要"都是额外的 Token 消耗。

**Spec 的三阶段**：

| 阶段 | 文件 | 做什么 | 省在哪里 |
|------|------|--------|---------|
| 需求 | requirements.md / bugfix.md | 明确验收标准、用户故事 | 一次想清楚，避免反复澄清 |
| 设计 | design.md | 技术架构、序列图、实现方案 | 架构决策持久化，不怕上下文丢失 |
| 任务 | tasks.md | 离散可执行任务，支持状态追踪 | 每任务聚焦可验证，可单独执行交付 |

**Spec 文件存储位置**：`.claude/specs/<name>/`（requirements.md / design.md / test-cases.md / tasks.md 四个文件）

**Spec 的成本优势**：

| 维度 | 自由对话 | Spec 工作流 |
|------|---------|------------|
| 需求澄清 | 多轮对话，每轮消耗 Token | 一次性在 requirements.md 中写清 |
| 架构决策 | 存在对话中，摘要后可能丢失 | 持久化在 design.md 中 |
| 进度追踪 | 靠记忆，新会话要重新解释 | tasks.md 自动标记完成状态 |
| 会话接力 | 需要写 handoff 文档 | 新会话读 Spec 就知道从哪继续 |
| 验证标准 | 模糊的"做完告诉我" | 每个任务有明确的完成条件 |

**Spec 实操建议**：

1. 花 5 分钟创建 Spec，哪怕只写 requirements.md 也比裸聊好——这 5 分钟能节省后续数小时的调试和返工时间
2. 让 AI 先采访你：
   ```
   "我想构建一个用户通知系统。在开始之前，请先问我几个关键问题，帮我理清需求。"
   ```
   AI 会问出你没想到的问题——通知渠道、频率限制、用户偏好、失败重试策略等
3. Spec 中引用外部文档，避免全文粘贴：
   ```
   ## 技术约束
   参考 API 规范：#[[file:docs/openapi.yaml]]
   参考数据模型：#[[file:docs/schema.prisma]]
   ```
4. 大任务分块执行：完成一块，提交代码，开新会话处理下一块。上下文保持精简，质量不会随会话变长而下降

### B.5 Steering + Spec + Hooks 三层叠加

这三层构成完整的防护体系：

| 层级 | 机制 | 职责 |
|------|------|------|
| 规则层 | Steering 文件 | 代码风格、禁止事项、项目约定 |
| 流程层 | Spec 任务 | 执行顺序、验收标准、依赖关系 |
| 硬校验层 | Hooks（runCommand） | 自动 lint、类型检查、运行测试 |
| 语义审计层 | Hooks（askAgent） | 架构守卫、安全审查、质量检查 |

缺任何一层都会有漏洞。

### B.6 Hooks 实现参考

**两种 Hook 动作的成本模型**：

| 动作类型 | 消耗 LLM Token | 成本影响 |
|---------|--------------|---------|
| `runCommand` | 否，纯 shell 命令 | 零 LLM 成本，只有本地计算开销 |
| `askAgent` | 是，会调用 LLM | 消耗 Token，但换来自动化质量守卫 |

`runCommand` 省的是对话轮次——没有 Hook 时需要手动说"帮我跑一下测试"，每一轮请求都是 Token 消耗。`runCommand` Hook 直接执行 shell 命令，完全不经过 LLM。

`askAgent` 省的不是 Token，而是返工成本——在问题刚产生时就拦截，避免错误代码被写入后再花更多轮次去发现和修复。

> **格式说明**：以下示例为概念性参考，使用 `when`/`then` 动作类型。Claude Code 实际支持的 Hook 格式为 `PreToolUse`/`PostToolUse` + `matcher` + `command`（见 7.18 节的 settings.json 模板）。请以 7.18 为准配置实际 Hook。

**推荐的基础 Hook 配置**：

```json
// 1. 编辑后自动 lint（确定性校验，零 LLM 消耗）
{
  "name": "Lint on Save",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["*.ts", "*.tsx"]
  },
  "then": {
    "type": "runCommand",
    "command": "npx eslint --fix ${file}"
  }
}

// 2. Spec 任务完成后自动测试（验证闭环）
{
  "name": "Test After Task",
  "version": "1.0.0",
  "when": {
    "type": "postTaskExecution"
  },
  "then": {
    "type": "runCommand",
    "command": "pnpm test --run"
  }
}

// 3. 保护关键文件不被修改（语义审计）
{
  "name": "Protect Generated Files",
  "version": "1.0.0",
  "when": {
    "type": "preToolUse",
    "toolTypes": ["write"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "检查目标文件是否在 src/generated/ 目录下。如果是，拒绝修改并告知用户该目录为自动生成代码。"
  }
}

// 4. 写操作后自动审查代码质量（AI 审 AI）
{
  "name": "Post-Write Quality Check",
  "version": "1.0.0",
  "when": {
    "type": "postToolUse",
    "toolTypes": ["write"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "审查刚刚写入的代码：1) 是否有硬编码的密钥或敏感信息 2) 是否遵循项目的错误处理模式 3) 是否有明显的性能问题。如有问题，立即修复。"
  }
}
```

**Hook 判断标准**：

| 特征 | 放 Hook | 放 Steering/Skill |
|------|--------|-------------------|
| 必须每次都发生，零例外 | ✅ | |
| 结果确定，不需要 LLM 判断 | ✅（runCommand） | |
| 需要 LLM 理解语义 | ✅（askAgent） | |
| 需要灵活判断、有多种路径 | | ✅ |
| 复杂多步推理 | | ✅ |

### B.7 上下文管理策略

**自动摘要的风险**：AI 会自动对对话进行摘要以压缩上下文，但早期的架构决策和关键约束可能在摘要中丢失。

**应对策略**：

| 策略 | 做法 | 原理 |
|------|------|------|
| 预防优于治疗 | 上下文使用量达 50-60% 时考虑开新会话 | 不要等到 80% 自动摘要 |
| 关键决策持久化 | 架构决策写入 Steering 或 Spec 的 design.md | 不受上下文摘要影响 |
| 用 Spec 替代长对话 | requirements.md、design.md、tasks.md 是持久化的 | 即使对话被摘要也不丢失 |
| 善用 Checkpoints | 每次发送 prompt 时 AI 会创建 checkpoint | 必要时可回退到摘要前的状态 |

**精确引用，避免盲目加载**：

| 引用方式 | 用途 |
|---------|------|
| `#File` | 引用特定文件 |
| `#Folder` | 引用整个目录 |
| `#Problems` | 当前文件的诊断问题 |
| `#Terminal` | 终端输出 |
| `#Git Diff` | 当前变更 |

省 Token 的做法：不要说"看看整个项目"，而是用 `#File` 精确指向相关文件。

**会话管理的铁律**：

| 信号 | 行动 |
|------|------|
| 上下文使用量超过 50% | 考虑是否该开新会话 |
| 在同一会话中做了不相关的任务 | 立即开新会话，避免上下文串扰 |
| 纠正同一个问题两次还是错 | 开新会话，用学到的教训写更好的初始指令 |
| 让 AI "调查"某事却不限定范围 | 缩小范围，或用 context-gatherer 子代理隔离探索 |
| 完成一个里程碑 | 提交代码，开新会话处理下一个 |

### B.8 Prompt 缓存优化

**常见误解**：很多人以为 Prompt 缓存能减少发送给模型的 Token 数量。实际上不是——每次请求，完整的 prompt 都会完整发送给 LLM，模型必须"看到"所有内容才能工作。Token 数量一个不少。

**缓存真正省的是钱**：按前缀匹配工作，完全一致的段（系统指令、工具定义、Steering）以 1/10 价格计费；变化的段（对话历史、新输入）按正常价格计费。

```
[系统指令]          ← 每次都一样，缓存命中，1/10 价格
[工具定义]          ← 每次都一样，缓存命中，1/10 价格
[Steering 文件]     ← 基本不变，缓存命中，1/10 价格
--- 以上是"前缀"，占 20-30K tokens，但只收 1/10 的钱 ---
[对话历史]          ← 每轮都在增长，正常价格
[你的新输入]        ← 新的，正常价格
```

**应避免的破坏缓存行为**：
- 会话中途频繁增删 MCP Server（改变工具定义，前缀不再匹配）
- 会话中途切换模型（缓存是按模型隔离的，换模型 = 重建缓存）
- 在 Steering 文件中放动态内容（时间戳、随机数等会让前缀每次都不同）

**实践建议**：在一个会话中保持工具配置稳定。需要不同的 MCP 工具集时，在不同会话中使用。

### B.9 在 CLAUDE.md 中落地 Steering 和 Spec

Steering 和 Spec 不需要创建额外的 CLI 命令或目录结构，可以通过在 CLAUDE.md 中增加对应章节来实现：

**CLAUDE.md 中的 Steering 章节示例**：

```markdown
## Steer 文件 — 项目心智地图

存放位置：.claude/steer/（每次会话自动加载）

### 构建与运行
- 包管理器：pnpm
- 构建：pnpm build
- 测试：pnpm test --run

### 目录结构（关键模块）
- src/api/ — HTTP 处理、路由
- src/domain/ — 核心业务规则
- src/infra/ — 数据库适配器、外部集成

### 修改导航（改 X 去哪里改）
- 新增 API endpoint → src/api/routes.ts + src/api/handlers/*
- 修改定价规则 → src/domain/billing/pricing.ts + 对应测试

### NEVER
- 不要修改 src/generated/ 下的文件
- 不要在组件中写业务逻辑
- 禁止 any 类型

### fileMatch 规范（如有）
- 前端规范：.claude/steer/frontend.md（编辑 src/components/ 时加载）
- 测试规范：.claude/steer/testing.md（编辑 tests/ 时加载）
```

**CLAUDE.md 中的 Spec 工作流章节示例**：

```markdown
## Spec 工作流 — 先思考再动手

大任务（3个文件以上、重构、引入新依赖）必须先开 Spec：
1. 在 .claude/specs/ 下创建任务目录（如 .claude/specs/user-auth/）
2. 创建 requirements.md：明确验收标准、用户故事
3. 创建 design.md：技术架构、序列图、实现方案
4. 创建 test-cases.md：测试用例文档，覆盖 AC/ST/PM/BF 四类清单
5. 创建 tasks.md：离散可执行任务，每个任务可单独验证（含测试任务）

Spec 文件是持久化的，不受上下文摘要影响。
```

---

## 附录 C：Spec 文件模板

> 本附录提供 Spec 四个文件的详细模板，确保需求开发流程标准化（测试先行模式）。
>
> **模板固化机制**：
> - **初始化时创建**：AI 读取本附录内容，在 `.claude/templates/spec/` 下创建 4 个模板文件
> - **功能开发时使用**：用户确认需求后，AI 读取 `.claude/templates/spec/` 下的模板，在 `.claude/specs/<feature>/` 下创建对应的 Spec 文件
>
> **测试先行流程**：requirements.md（需求）→ design.md（设计）→ **test-cases.md（测试用例文档）**→ tasks.md（任务清单）→ 实现 → 测试执行
>
> **文件对应关系**：
> | 本附录模板 | 初始化时创建 | 功能开发时复制到 |
> |-----------|-------------|-----------------|
> | C.1 requirements.md 模板 | `.claude/templates/spec/requirements.md` | `.claude/specs/<feature>/requirements.md` |
> | C.2 design.md 模板 | `.claude/templates/spec/design.md` | `.claude/specs/<feature>/design.md` |
> | C.3 tasks.md 模板 | `.claude/templates/spec/tasks.md` | `.claude/specs/<feature>/tasks.md` |
> | 附录 D test-cases.md 模板 | `.claude/templates/spec/test-cases.md` | `.claude/specs/<feature>/test-cases.md` |
>
> **填充指南**：
>
> AI 在创建 Spec 时需要做两类工作：
>
> **1. 占位符替换**（简单替换）：
> - `{功能名称}` → 替换为具体功能名，如 `会议室管理`
> - `{日期}` → 替换为创建日期，如 `2026-04-22`
> - `{状态}` → 替换为初始状态，如 `草稿`
>
> **2. 业务内容填充**（根据需求动态创建）：
> - **验收条件表**：根据需求分析，补充 AC-001、AC-002... 每个验收条件
> - **影响范围表**：根据功能分析，列出涉及的后端模块、前端页面、数据库表
> - **数据库设计**：根据功能需求，设计具体的表结构、字段、索引（参考模板中的示例格式）
> - **API 设计**：根据功能需求，定义具体的接口路径、请求/响应结构（参考模板中的示例格式）
> - **任务清单**：根据实现方案，拆解具体的开发任务（参考模板中的示例格式）
>
> **使用示例**：
> - 模板中已包含会议室管理功能的示例（验收条件、数据库设计、API 设计等）
> - AI 创建其他功能的 Spec 时，参考示例的格式和详细程度，填充对应内容
> - 不要只保留模板框架，必须填充完整的业务内容
>
> **创建时机**：用户确认需求后（说"继续"、"开始实现"等），AI 开始实现前必须创建。

### C.1 requirements.md — 需求文档模板

**存储位置**：`.claude/specs/<feature-name>/requirements.md`

```markdown
# 需求文档：{功能名称}

> 创建时间：{日期}
> 状态：{草稿 / 已确认 / 开发中 / 已完成}

## 1. 功能概述

**一句话描述**：{简明扼要描述要做什么}

**业务背景**：{为什么需要这个功能，解决什么问题}

## 2. 验收条件（Acceptance Criteria）

> 必填项。每个条件应该是可验证的。

| 编号 | 条件描述 | 优先级 | 验证方式 |
|------|----------|--------|----------|
| AC-001 | {条件1} | P0/P1/P2 | {如何验证} |
| AC-002 | {条件2} | P0/P1/P2 | {如何验证} |
| AC-003 | {条件3} | P0/P1/P2 | {如何验证} |

**示例**：
| AC-001 | 用户可以创建会议室预约 | P0 | 创建预约成功后可在列表看到 |
| AC-002 | 预约时间冲突时提示错误 | P0 | 尝试预约已占用时段，显示错误提示 |

## 3. 影响范围

> 必填项。列出受影响的模块和文件。

### 3.1 后端影响

| 模块 | 影响说明 | 新增/修改 |
|------|----------|-----------|
| {模块名} | {说明} | 新增 |
| {模块名} | {说明} | 修改 |

### 3.2 前端影响

| 页面/组件 | 影响说明 | 新增/修改 |
|-----------|----------|-----------|
| {页面名} | {说明} | 新增 |
| {组件名} | {说明} | 修改 |

### 3.3 数据库影响

| 表名 | 影响说明 | 新增/修改 |
|------|----------|-----------|
| {表名} | {说明} | 新增表 |
| {表名} | {说明} | 新增字段 |

### 3.4 依赖影响

| 依赖项 | 影响说明 | 版本要求 |
|--------|----------|----------|
| {依赖名} | {说明} | {版本} |

## 4. 用户故事（User Stories）

> 可选项。描述用户如何使用该功能。

**故事1**：作为{角色}，我希望{目标}，以便{收益}。

**验收要点**：
- {要点1}
- {要点2}

## 5. 非功能性需求

> 可选项。性能、安全、可用性等要求。

| 类型 | 要求 |
|------|------|
| 性能 | {要求} |
| 安全 | {要求} |
| 可用性 | {要求} |

## 6. 边界情况

> 可选项。需要处理的特殊场景。

| 场景 | 处理方式 |
|------|----------|
| {场景1} | {如何处理} |
| {场景2} | {如何处理} |

## 7. 参考资料

> 可选项。相关文档、原型、接口文档链接。

- {参考文档1}
- {参考文档2}
```

### C.2 design.md — 设计文档模板

**存储位置**：`.claude/specs/<feature-name>/design.md`

```markdown
# 设计文档：{功能名称}

> 创建时间：{日期}
> 状态：{草稿 / 已评审 / 已确认}

## 1. 技术方案概述

**一句话描述**：{采用什么技术方案实现}

**方案选择原因**：{为什么选择这个方案}

## 2. 数据库设计

> 必填项。新表或修改现有表的设计。
>
> **字符集规范**：SQL 脚本必须在开头添加字符集声明，避免中文乱码：
> ```sql
> SET NAMES utf8mb4;
> SET CHARACTER SET utf8mb4;
> ```
>
> **Docker MySQL 执行规范**：必须指定字符集
> ```bash
> docker exec <container> mysql -uroot -p123456 --default-character-set=utf8mb4 <db> -e "SQL语句"
> ```

### 2.1 新增表

#### 表：{table_name}

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 主键 |
| {字段名} | {类型} | {约束} | {说明} |
| creator | VARCHAR(64) | | 创建者 |
| create_time | DATETIME | NOT NULL | 创建时间 |
| updater | VARCHAR(64) | | 更新者 |
| update_time | DATETIME | NOT NULL | 更新时间 |
| deleted | BIT(1) | NOT NULL DEFAULT 0 | 逻辑删除标识 |

**索引设计**：

| 索引名 | 字段 | 类型 | 说明 |
|--------|------|------|------|
| idx_{字段} | {字段} | 普通/唯一 | {用途} |

**示例**：
```sql
CREATE TABLE `business_meeting_room` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '会议室ID',
  `name` varchar(100) NOT NULL COMMENT '会议室名称',
  `capacity` int NOT NULL DEFAULT 0 COMMENT '容纳人数',
  `location` varchar(200) DEFAULT NULL COMMENT '位置',
  `equipment` varchar(500) DEFAULT NULL COMMENT '设备信息（JSON）',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '状态（0禁用 1启用）',
  `creator` varchar(64) DEFAULT '' COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updater` varchar(64) DEFAULT '' COMMENT '更新者',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted` bit(1) NOT NULL DEFAULT b'0' COMMENT '是否删除',
  `tenant_id` bigint NOT NULL DEFAULT 0 COMMENT '租户编号',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name` (`name`, `tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会议室信息表';
```

### 2.2 修改表

| 表名 | 修改内容 | 说明 |
|------|----------|------|
| {表名} | 新增字段 {字段名} | {用途} |
| {表名} | 修改字段 {字段名} | {原因} |

## 3. API 设计

> 必填项。接口定义。

### 3.1 接口列表

| 方法 | 路径 | 说明 | 权限标识 |
|------|------|------|----------|
| POST | /business/meeting-room/create | 创建会议室 | business:meeting-room:create |
| PUT | /business/meeting-room/update | 更新会议室 | business:meeting-room:update |
| DELETE | /business/meeting-room/delete | 删除会议室 | business:meeting-room:delete |
| GET | /business/meeting-room/get | 获取会议室详情 | business:meeting-room:query |
| GET | /business/meeting-room/page | 获取会议室分页列表 | business:meeting-room:query |

### 3.2 接口详情

#### 创建会议室

**请求**：
```json
{
  "name": "会议室A",
  "capacity": 10,
  "location": "3楼-301",
  "equipment": "[\"投影仪\", \"白板\"]"
}
```

**响应**：
```json
{
  "code": 0,
  "data": 1,
  "message": "success"
}
```

**业务逻辑**：
1. 校验会议室名称唯一性
2. 创建会议室记录
3. 返回会议室ID

#### 获取会议室分页列表

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | String | 否 | 会议室名称（模糊匹配） |
| status | Integer | 否 | 状态 |
| pageNo | Integer | 是 | 页码 |
| pageSize | Integer | 是 | 每页数量 |

**响应**：
```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "id": 1,
        "name": "会议室A",
        "capacity": 10,
        "location": "3楼-301",
        "status": 1
      }
    ],
    "total": 100
  },
  "message": "success"
}
```

## 4. 关键决策

> 必填项。技术选型、架构决策及其原因。

| 决策项 | 选择 | 原因 | 替代方案 |
|--------|------|------|----------|
| 时间冲突检测 | 数据库唯一索引 + 应用层校验 | 双重保障，防止并发超卖 | 仅应用层校验 |
| 统计查询 | 实时查询 + 缓存 | 数据量可控，缓存提升性能 | 定时任务聚合 |

## 5. 数据流程图

> 可选项。关键业务流程的时序图或流程图。

```
用户 -> Controller: 创建预约请求
Controller -> Service: 校验参数
Service -> Mapper: 查询时间段内是否有冲突
alt 有冲突
    Service --> Controller: 返回错误提示
else 无冲突
    Service -> Mapper: 插入预约记录
    Service --> Controller: 返回预约ID
end
```

## 6. 风险评估

> 可选项。已知风险及应对措施。

| 风险 | 级别 | 应对措施 |
|------|------|----------|
| 并发预约冲突 | 高 | 数据库唯一索引 + 乐观锁 |
| 统计查询性能 | 中 | 添加索引 + 缓存 |

## 7. 测试要点

> 可选项。重点测试场景。

| 场景 | 测试要点 |
|------|----------|
| 正常预约 | 预约成功，数据正确 |
| 时间冲突 | 提示错误，不创建记录 |
| 并发预约 | 只有一个成功 |
| 边界值 | 预约时间刚好相邻 |
```

### C.3 tasks.md — 任务清单模板

**存储位置**：`.claude/specs/<feature-name>/tasks.md`

```markdown
# 任务清单：{功能名称}

> 创建时间：{日期}
> 最后更新：{日期}

## 任务状态说明

- ⬜ 未开始
- 🔄 进行中
- ✅ 已完成
- ❌ 已阻塞（需说明原因）

## 任务列表

### 阶段一：测试用例文档（测试先行，预计 {N} 小时）

> **测试先行**：基于 requirements.md 中的 AC 和 RTM 四类清单，补充 test-cases.md 测试用例文档。

| 任务ID | 任务描述 | 对应 AC | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|---------|----------|------|------|------|
| T-DOC-001 | 补充 {AC-001} 对应的测试用例到 test-cases.md | AC-001 | tester | ⬜ | 0.5h | |
| T-DOC-002 | 补充 {AC-002} 对应的测试用例到 test-cases.md | AC-002 | tester | ⬜ | 0.5h | |
| T-DOC-003 | 补充 {AC-003} 对应的测试用例到 test-cases.md | AC-003 | tester | ⬜ | 0.5h | |
| T-DOC-004 | 补充权限测试用例到 test-cases.md | PM-xxx | tester | ⬜ | 0.5h | |
| T-DOC-005 | 补充业务流程测试用例到 test-cases.md | BF-xxx | tester | ⬜ | 0.5h | |

### 阶段二：数据库（预计 {N} 小时）

| 任务ID | 任务描述 | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|----------|------|------|------|
| T-001 | 创建数据库表 SQL 脚本 | db-implementer | ⬜ | 0.5h | |
| T-002 | 创建 DO 实体类 | db-implementer | ⬜ | 0.5h | |
| T-003 | 创建 Mapper 接口 | db-implementer | ⬜ | 0.5h | |

### 阶段三：后端（预计 {N} 小时）

| 任务ID | 任务描述 | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|----------|------|------|------|
| T-004 | 创建 VO 类（Req/Resp/Page） | backend | ⬜ | 1h | |
| T-005 | 创建 Service 接口和实现 | backend | ⬜ | 2h | |
| T-006 | 创建 Controller | backend | ⬜ | 1h | |

### 阶段四：前端（预计 {N} 小时）

| 任务ID | 任务描述 | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|----------|------|------|------|
| T-007 | 创建 API 定义文件 | frontend | ⬜ | 0.5h | |
| T-008 | 创建列表页面 | frontend | ⬜ | 2h | |
| T-009 | 创建表单弹窗 | frontend | ⬜ | 1h | |

### 阶段五：测试执行（全部实现完成后统一执行，预计 {N} 小时）

> **测试先行**：测试用例文档（test-cases.md）和测试代码（T-UT-xxx / T-E2E-xxx）已在阶段一完成，实现完成后统一执行。**此阶段在阶段二~四全部完成后执行**。

| 任务ID | 任务描述 | 对应测试用例 | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|------------|----------|------|------|------|
| T-UT-001 | 编写单元测试代码（基于 test-cases.md） | T-DOC-001 | tester | ⬜ | 0.5h | |
| T-UT-002 | 编写单元测试代码（基于 test-cases.md） | T-DOC-002 | tester | ⬜ | 0.5h | |
| T-UT-101 | 运行后端单元测试，确保全部通过 | T-DOC-001~002 | tester | ⬜ | 0.5h | |
| T-E2E-001 | 编写 E2E 测试代码（基于 test-cases.md） | T-DOC-003~005 | tester | ⬜ | 1h | |
| T-E2E-101 | 运行前端 E2E 测试，确保全部通过 | T-DOC-003~005 | tester | ⬜ | 0.5h | |

### 阶段六：测试与审查（预计 {N} 小时）

| 任务ID | 任务描述 | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|----------|------|------|------|
| T-010 | 本地功能验证 | 主CC | ⬜ | 1h | |
| T-011 | 代码审查 | code-reviewer | ⬜ | 1h | |
| T-012 | 修复审查问题 | backend/frontend | ⬜ | 1h | |
| T-013 | 质量门禁检查 | 主CC | ⬜ | 0.5h | |

### 阶段七：提交 Git（预计 0.5 小时）

| 任务ID | 任务描述 | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|----------|------|------|------|
| T-014 | 提交代码（遵循 git.md Commit 规范） | 主CC | ⬜ | 0.5h | |

## 任务依赖关系（测试先行流程）

```
【阶段一：测试用例文档】
T-DOC-001 ─┐
T-DOC-002 ─┤──→ T-DOC-004 ─┐
T-DOC-003 ─┘               │
               └─→ T-DOC-005 ──→ test-cases.md（测试用例文档完成）
                                        │
【阶段二~四：实现代码】                   │
T-001 ──→ T-002 ──→ T-003 ──→ T-005 ──→ T-006       T-007 ──→ T-008 ──→ T-009
          │                   ↑                        │
          └───→ T-004 ────────┘                        │
                                        │
【阶段五：测试执行（统一）】              │
T-UT-001 ──→ T-UT-002 ──→ T-UT-101 ──→ T-E2E-001 ──→ T-E2E-101
                                        │
【阶段六：审查与收尾】                    │
T-010 ──→ T-011 ──→ T-012 ──→ T-013
                                        │
【阶段七：提交 Git】                      │
T-014 ──→ ✅ 交付
```

## 测试先行开发原则

1. **测试用例文档先行**：基于 requirements.md 补充 test-cases.md，明确每个 AC 对应的测试用例
2. **测试代码编写**：基于 test-cases.md 编写测试代码（T-UT-xxx、T-E2E-xxx）
3. **实现代码**：基于 design.md 和 test-cases.md 实现功能代码
4. **统一测试执行**：**全部实现完成后**执行 T-UT-101（单元测试）和 T-E2E-101（E2E 测试），全部通过才进入审查阶段

## 总计

- **预计总工时**：{N} 小时（含测试用例文档 + 测试代码编写）
- **实际总工时**：{N} 小时
- **任务总数**：{N} 个（含 {M} 个测试相关任务）
- **已完成**：{N} 个
- **进度**：{N}%
- **测试用例文档**：test-cases.md（T-DOC-xxx 系列）
- **测试代码**：T-UT-xxx / T-E2E-xxx（T-DOC 完成后再编写测试代码）

## 阻塞问题记录

| 日期 | 任务ID | 问题描述 | 解决方案 | 解决日期 |
|------|--------|----------|----------|----------|
| {日期} | {任务ID} | {问题} | {方案} | {日期} |
```

### C.4 Spec 文件使用指南

#### 创建时机（测试先行模式）

| 阶段 | 触发条件 | 创建文件 |
|------|----------|----------|
| 需求确认 | 用户说"继续"、"开始实现" | requirements.md |
| 开始设计 | AI 输出 Plan 后 | design.md |
| 补充测试用例 | 设计完成后、实现前 | test-cases.md（测试用例文档） |
| 开始实现 | 测试用例文档完成后 | tasks.md（含测试任务） |

#### 更新频率

| 文件 | 更新时机 |
|------|----------|
| requirements.md | 需求变更时 |
| design.md | 技术方案调整时 |
| test-cases.md | 需求或设计变更时 |
| tasks.md | 每完成一个任务时更新状态 |

#### 进度追踪

```bash
# 查看任务进度
grep -E "^\| T-" .claude/specs/<feature>/tasks.md | grep -c "✅"  # 已完成数
grep -E "^\| T-" .claude/specs/<feature>/tasks.md | wc -l       # 总任务数
# 查看测试任务进度
grep -E "^\| T-UT-\|T-E2E-" .claude/specs/<feature>/tasks.md | grep -c "✅"  # 已完成测试任务数
```

#### Spec 文件与 Plan 的区别

| 维度 | Plan | Spec |
|------|------|------|
| 生命周期 | 临时输出，会话内有效 | 持久化，跨会话有效 |
| 详细程度 | 概要（影响范围、风险评估） | 详细（具体字段、SQL、API、测试用例） |
| 更新频率 | 一次性输出 | 持续更新 |
| 用途 | 决策是否继续 | 实现过程中的参考文档 |

#### 示例：会议室管理功能 Spec

```
.claude/specs/meeting-room/
├── requirements.md   # 验收条件：AC-001 创建会议室、AC-002 预约冲突检测...
├── design.md         # 数据库：business_meeting_room、business_meeting_room_booking
├── test-cases.md     # 测试用例：T-UT-001~003、T-E2E-001~002（对应 AC/PM/BF）
└── tasks.md          # T-UT-001 创建测试用例、T-001 创建表...（含测试任务）
```

### C.5 Spec 与其他配置的关系

```
CLAUDE.md
  ├── 定义"什么时候创建 Spec"（行为规范 → 需求开发流程 + 测试先行）
  └── 引用 Spec 模板（附录 C、附录 D）

.claude/templates/spec/           # 初始化时创建，存放模板（4 个文件）
  ├── requirements.md             # 附录 C.1 模板
  ├── design.md                   # 附录 C.2 模板
  ├── test-cases.md               # 附录 D 模板（测试先行核心）
  └── tasks.md                    # 附录 C.3 模板（含测试任务）

.claude/specs/                    # 初始化时创建空目录
  └── <feature>/                  # 每个新功能创建一个子目录
      ├── requirements.md          # 从 templates/spec/ 复制并填充
      ├── design.md               # 从 templates/spec/ 复制并填充
      ├── test-cases.md           # 从 templates/spec/ 复制并填充
      └── tasks.md                # 从 templates/spec/ 复制并填充（含测试任务）

.claude/rules/
  └── 在实现过程中遵守规则（security.md、testing.md 等）

.claude/steer/
  └── 提供项目心智地图（目录结构、修改导航）
```

**初始化 vs 功能开发**：

| 阶段 | 创建内容 | 说明 |
|------|----------|------|
| 项目初始化 | `.claude/templates/spec/` 4 个模板文件 | 固化模板，长期可用 |
| 项目初始化 | `.claude/specs/` 空目录 | 功能 Spec 存放位置 |
| 功能开发 | `.claude/specs/<feature>/` 子目录 + 4 个文件 | 读取 templates 中的模板创建 |

**模板固化机制**：

```
初始化阶段（第三章）：
  GUIDE.md 附录 C、D 内容
      ↓
  AI 读取模板，创建文件
      ↓
  .claude/templates/spec/
      ├── requirements.md
      ├── design.md
      ├── test-cases.md           # 新增
      └── tasks.md                # 含测试任务

功能开发阶段（用户确认需求后，测试先行模式）：
  AI 读取 .claude/templates/spec/*.md
      ↓
  填充具体需求内容
      ↓
  创建 .claude/specs/<feature>/
      ├── requirements.md
      ├── design.md
      ├── test-cases.md           # 测试先行：测试用例文档
      └── tasks.md                # 含测试任务
```

**工作流（测试先行模式）**：
1. 用户提需求 → AI 分析 → 输出 Plan
2. 用户确认 → AI 读取 `.claude/templates/spec/` 模板 → 创建 `.claude/specs/<feature>/` 下的 Spec 文件
3. **测试先行**：先补充 test-cases.md（测试用例文档），再按 tasks.md 实现
4. 按 tasks.md 执行 → 遵守 rules/ 规则 → 参考 steer/ 导航
5. **全部实现完成后** → 统一执行测试（T-UT-101 / T-E2E-101），全部通过才进入审查
6. 执行质量门禁 → 交付
```

---

## 附录 D：test-cases.md 模板说明

> **测试先行核心**：测试用例是需求的 executable specification，驱动开发。
>
> **时机**：design.md 完成之后、实现之前。测试用例来自 requirements.md 中的验收条件（AC）和 RTM 中的四类清单（ST/PM/BF）。
>
> **测试先行循环**：
> 1. **测试用例文档**：为每个 AC 补充 test-cases.md 测试用例
> 2. **测试代码编写**：基于 test-cases.md 编写测试代码（T-UT-xxx / T-E2E-xxx）
> 3. **实现代码**：基于 design.md 和 test-cases.md 实现功能
> 4. **统一测试执行**：**全部实现完成后**运行 T-UT-101 / T-E2E-101，全部通过才进入审查

### D.1 test-cases.md — 测试用例模板

**存储位置**：`.claude/specs/<feature-name>/test-cases.md`

```markdown
# 测试用例：{功能名称}

> 创建时间：{日期}
> 对应需求：`.claude/specs/<feature>/requirements.md`
> 对应设计：`.claude/specs/<feature>/design.md`
> 状态：{草稿 / 已评审 / 已确认}

## 测试用例概览

| 测试类型 | 用例数 | 对应验收条件 |
|---------|-------|------------|
| 单元测试（UT） | N 个 | AC-xxx |
| E2E 测试 | N 个 | AC/ST/PM/BF |
| 集成测试 | N 个 | AC-xxx |

## 1. 单元测试用例

> 覆盖后端 Service/Controller 层的核心逻辑。

### 1.1 {功能模块A}

| 用例ID | 用例名称 | 对应 AC | 前置条件 | 测试步骤 | 预期结果 |
|--------|----------|---------|----------|----------|----------|
| UT-001 | {用例名} | AC-001 | {测试数据准备} | {步骤1}<br>{步骤2} | {预期输出} |
| UT-002 | {用例名} | AC-002 | {测试数据准备} | {步骤1}<br>{步骤2} | {预期输出} |

**示例**：
| UT-001 | 会议室名称不能为空 | AC-001 | 无 | 1. 调用创建会议室接口<br>2. name 传空字符串 | 返回参数错误提示 |

### 1.2 {功能模块B}

| 用例ID | 用例名称 | 对应 AC | 前置条件 | 测试步骤 | 预期结果 |
|--------|----------|---------|----------|----------|----------|
| UT-003 | {用例名} | AC-003 | {测试数据准备} | {步骤1}<br>{步骤2} | {预期输出} |

## 2. E2E 测试用例

> 覆盖前端页面的完整交互流程。

### 2.1 冒烟测试（batch-a）

| 用例ID | 用例名称 | 对应 AC | 测试步骤 | 预期结果 |
|--------|----------|---------|----------|----------|
| E2E-001 | {页面名}页面可达 | AC-xxx | 1. 访问 {URL}<br>2. 等待页面加载 | 页面正确渲染，数据正常显示 |
| E2E-002 | {功能名}数据加载 | AC-xxx | 1. 进入 {页面}<br>2. 等待接口返回 | 至少一个 API 请求成功，数据渲染到页面 |

**全局错误监听（必须内置）**：
```javascript
const errors = []
page.on('pageerror', err => errors.push(err.message))
page.on('console', msg => {
  if (msg.type() === 'error') errors.push(msg.text())
})
// 断言前等待微任务完成
await page.waitForLoadState('networkidle')
await page.waitForTimeout(500)
expect(errors.filter(e => !isKnownNoise(e))).toEqual([])
```

### 2.2 功能测试（batch-b）

| 用例ID | 用例名称 | 对应 AC | 测试步骤 | 预期结果 |
|--------|----------|---------|----------|----------|
| E2E-003 | 创建{功能}成功 | AC-001 | 1. 进入{页面}<br>2. 点击新建按钮<br>3. 填写表单<br>4. 点击提交 | 创建成功，列表刷新并显示新记录 |
| E2E-004 | 创建{功能}失败-参数校验 | AC-001 | 1. 进入{页面}<br>2. 点击新建按钮<br>3. 不填写必填字段<br>4. 点击提交 | 提示参数错误，不提交 |
| E2E-005 | 更新{功能}成功 | AC-002 | 1. 进入{详情页}<br>2. 修改字段<br>3. 点击保存 | 更新成功，页面刷新显示新数据 |
| E2E-006 | 删除{功能}成功 | AC-003 | 1. 进入{列表页}<br>2. 选择记录<br>3. 点击删除<br>4. 确认删除 | 删除成功，记录从列表消失 |

### 2.3 权限测试（batch-c）

| 用例ID | 用例名称 | 对应 PM | 测试步骤 | 预期结果 |
|--------|----------|---------|----------|----------|
| E2E-007 | {角色}可访问{功能} | PM-001 | 1. 使用{角色}账号登录<br>2. 访问{页面} | 页面正常显示，功能可用 |
| E2E-008 | {角色}无权限访问{功能} | PM-002 | 1. 使用{角色}账号登录<br>2. 访问{页面} | 返回 403 或页面不显示 |
| E2E-009 | 横向越权检测 | PM-003 | 1. 用户 A 创建{资源}<br>2. 用户 B 尝试访问/修改用户 A 的{资源} | 拒绝访问，返回 403 |

**测试数据覆盖关键角色**：
- 超级管理员（admin）
- 普通用户（user）
- 无权限用户（guest）
- 无数据用户（empty）

### 2.4 状态流转测试（batch-e）

| 用例ID | 用例名称 | 对应 ST | 测试步骤 | 预期结果 |
|--------|----------|---------|----------|----------|
| E2E-010 | {状态A}→{状态B}正向流转 | ST-001 | 1. 创建{资源}，状态为{状态A}<br>2. 触发流转操作<br>3. 验证状态变化 | 状态正确更新，流转记录生成 |
| E2E-011 | {状态A}→{状态C}非法流转 | ST-002 | 1. 创建{资源}，状态为{状态A}<br>2. 尝试触发非法流转操作 | 提示错误，状态不变 |

### 2.5 业务流程测试（batch-d）

| 用例ID | 用例名称 | 对应 BF | 测试步骤 | 预期结果 |
|--------|----------|---------|----------|----------|
| E2E-012 | 完整业务流程 | BF-001 | 1. 步骤1<br>2. 步骤2<br>3. 步骤3 | 全流程完成，数据一致 |
| E2E-013 | 业务流程异常处理 | BF-001 | 1. 步骤1<br>2. 步骤2（异常）<br>3. 验证数据一致性 | 数据回滚，提示错误 |

## 3. 测试数据规范

### 3.1 Seed 数据

| 数据类型 | 准备方式 | 说明 |
|---------|---------|------|
| 角色数据 | Seed 脚本 | admin、user、guest 各 1 个 |
| 业务数据 | Seed 脚本 | 每种状态至少 1 条 |
| 边界数据 | 测试用例内准备 | 最大值、最小值、空值 |

### 3.2 测试数据示例

```sql
-- Seed 脚本（可重复执行，幂等）
INSERT INTO sys_user (id, username, role, ...) VALUES (1, 'admin', 'admin', ...) ON DUPLICATE KEY UPDATE ...;
INSERT INTO sys_user (id, username, role, ...) VALUES (2, 'user', 'user', ...) ON DUPLICATE KEY UPDATE ...;
```

## 4. 测试执行

### 4.1 单元测试执行

```bash
# 后端
mvn test -Dtest=*MeetingRoomServiceTest

# 前端
pnpm test:unit --run
```

### 4.2 E2E 测试执行

```bash
# 按 batch 执行
pnpm test:e2e --grep="batch-a"    # 冒烟测试
pnpm test:e2e --grep="batch-b"    # 功能测试
pnpm test:e2e --grep="batch-c"    # 权限测试
pnpm test:e2e --grep="batch-e"    # 状态流转测试
pnpm test:e2e --grep="batch-d"    # 业务流程测试

# 全量执行
pnpm test:e2e
```

## 5. RTM 追踪

> 测试用例完成后，更新 RTM（`.claude/specs/<feature>/rtm.md`）中的测试用例列。

| 验收条件 | 对应测试用例 | 状态 |
|---------|------------|------|
| AC-001 | UT-001, UT-002, E2E-003 | ✅ |
| AC-002 | UT-003, E2E-004 | ✅ |
| ST-001 | E2E-010 | ✅ |
| PM-001 | E2E-007, E2E-008 | ✅ |
| BF-001 | E2E-012, E2E-013 | ✅ |

**覆盖率**：{N}/{M}（{N%}）
**空白项**：{列出未实现的测试用例}
```

### D.2 测试用例编写原则

| 原则 | 说明 |
|------|------|
| 一一对应 | 每个 AC 至少有一个测试用例 |
| 可执行 | 测试用例必须能在 CI 中自动执行 |
| 可重复 | 测试数据可重复准备，测试结果稳定 |
| 独立性 | 每个测试用例独立运行，不依赖执行顺序 |
| 明确断言 | 每个测试用例有明确的 pass/fail 标准 |

### D.3 测试先行开发流程

```
1. 读取 requirements.md，确认所有 AC
2. 读取 design.md，理解技术方案
3. 补充 test-cases.md：
   - 为每个 AC 编写单元测试用例（UT-xxx）
   - 为每个 AC 编写 E2E 测试用例（E2E-xxx）
   - 覆盖 RTM 四类清单（ST/PM/BF）
   - 补充测试数据规范（Seed 脚本）
4. 创建 tasks.md：
   - T-DOC-xxx：测试用例文档编写任务
   - T-UT-xxx / T-E2E-xxx：测试代码编写任务
   - T-UT-101 / T-E2E-101：测试执行任务
5. 实现代码：
   - 阶段一：测试用例文档（T-DOC-xxx）
   - 阶段二~四：实现代码（T-001 ~ T-009）
   - 阶段五：测试执行（T-UT-101 / T-E2E-101）
   - 阶段六：审查与收尾（T-010 ~ T-013）
6. 质量门禁：执行第六章完整门禁清单
```

### D.4 测试用例模板使用示例

**示例：会议室管理功能**

```
AC-001: 用户可以创建会议室
  → T-DOC-001: 补充创建会议室的测试用例到 test-cases.md
  → T-UT-001: 编写 UT-001、UT-002 测试代码（参数校验 + 成功场景）
  → E2E-003: 创建会议室成功（页面操作完整流程）

AC-002: 预约时间冲突时提示错误
  → T-DOC-002: 补充预约冲突的测试用例到 test-cases.md
  → T-UT-002: 编写 UT-003 测试代码（预约冲突检测）
  → E2E-004: 预约冲突-提示错误

ST-001: 待支付 → 已支付
  → T-DOC-003: 补充状态流转测试用例到 test-cases.md
  → E2E-010: 状态流转-正向

PM-001: 普通用户 × 删除会议室 → 403
  → T-DOC-004: 补充权限测试用例到 test-cases.md
  → E2E-008: 权限不足-拒绝操作

BF-001: 完整预约流程
  → T-DOC-005: 补充业务流程测试用例到 test-cases.md
  → E2E-012: 预约流程-成功
  → E2E-013: 预约流程-异常处理
```

