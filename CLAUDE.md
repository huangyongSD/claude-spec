# 项目 AI 协作规范

> 遵循「配置即代码」原则，所有变更需提交到版本控制。

## 项目信息

- **项目名称**：`{{PROJECT_NAME}}`
- **技术栈**：`{{TECH_STACK}}`
- **数据库**：`{{DB_TYPE}}`
- **中间件**：`{{MIDDLEWARE}}`（如无则标注"无"）

> 构建命令、测试命令、格式化命令等详见 .claude/steer/foundation/tech.md

## 目录结构约定

```
{{PROJECT_DIR}}/
├─ CLAUDE.md           # 本文件，项目 AI 协作说明书
└─ .claude/
   ├─ steer/          # 项目心智地图（foundation/domain）
   ├─ rules/          # 底线规则（安全/测试/Git）
   ├─ agents/          # 专用子代理（审查/排障）
   ├─ commands/        # 斜杠命令（sdc-plan/sdc-codereview/sdc-buildfix/sdc-dev/sdc-spec）
   ├─ skills/          # 知识库
   ├─ templates/spec/  # Spec 模板（requirements/design/test-cases/tasks）
   ├─ specs/           # 功能级 Spec 目录
   └─ settings.json    # 基础配置
```

## 核心目录

| 目录 | 职责 |
|------|------|
| {{DIR_1}} | {{DIR_1_ROLE}} |
| {{DIR_2}} | {{DIR_2_ROLE}} |

> 每个核心目录一行，根据扫描结果增减行数。禁止修改的目录详见 .claude/steer/foundation/never.md

## 行为规范

### 需求开发流程（强制）

**所有新功能开发必须遵循以下流程：**

```
用户提需求 → AI 分析需求 → 输出 Plan → 用户确认 → 【自动】创建 Spec → 用户确认 → 开始实现
```

**触发 Spec 的时机：**
- 用户确认 Plan 后，AI 自动调用 `/sdc-spec` 创建 Spec 文件
- 无需用户再次手动触发

**Spec 创建内容：**
- `.claude/specs/<name>/` 目录下创建四个文件：
  - `requirements.md` — 验收标准
  - `design.md` — 技术方案（含文件产出清单）
  - `test-cases.md` — 测试用例文档（测试用例文档先行核心）
  - `tasks.md` — 任务清单
- 创建完 Spec 后才能开始写代码

**豁免条件（跳过 Spec 直接实现）：**
- 用户明确说"直接改"、"不用规划"等豁免词
- 单文件小改动（如修复 bug、调整配置）

### 必须先 Plan 的高风险操作

1. 多文件批量改动（3个及以上文件）
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
| Day 14 | 评估 Hook 配置，调整检查规则 |
| Day 30 | 全面回顾：分档调整、覆盖率提升、新配置需求；E2E 测试引入计划评估（如项目暂无 E2E 测试） |

## 存储位置

| 类型 | 位置 |
|------|------|
| 团队共享 | .claude/（Git 版本控制） |
| 个人偏好 | ~/.claude/（本地） |

## 配置索引

- **规则**：.claude/rules/security.md | testing.md | frontend.md | git.md | sda-collaboration.md
- **Steer**：.claude/steer/ — 项目心智地图，减少从零探索的 Token 消耗
- **Spec**：.claude/specs/ — 结构化任务流程，先思考再动手
- **Spec 模板**：.claude/templates/spec/ — 创建 Spec 时读取的模板文件
- **命令**：/sdc-plan | /sdc-codereview | /sdc-buildfix | /sdc-dev | /sdc-spec
- **SDA**：sda-architect | sda-code-reviewer | sda-tester | sda-coverage-auditor | sda-build-error-resolver
- **知识库**：.claude/skills/troubleshooting.md
- **权限/Hooks**：.claude/settings.json + .claude/hooks/
- **质量门禁**：见第五章质量门禁清单（10 项全绿才交付）

## Steer 文件 — 项目心智地图

> .claude/steer/ 目录下的文件为 AI 提供项目心智地图，减少每次会话从零探索的 Token 消耗。
> 只记项目特有的、容易踩坑的东西，不解释 AI 已知的常识。
> 详细编写指南见附录 B。

| 类型 | 文件 | 加载模式 |
|------|------|---------|
| foundation | product.md / tech.md / structure.md / never.md | always（每次会话） |
| domain | quality-gate.md / api.md / testing.md / security.md / frontend.md（可选）| fileMatch / auto（按需加载，由本配置索引引导 AI 主动读取） |

## Rules 文件 — 底线规则

> .claude/rules/ 目录下的文件定义不可违反的底线规则，按严重程度分档执行。
> 详细分档说明见各文件开头的 🔴🟡🟢 标记。

| 文件 | 职责 | 加载模式 |
|------|------|---------|
| security.md | 安全底线（凭证/密钥/SQL注入/XSS/权限） | fileMatch（Java/SQL/配置文件） |
| testing.md | 测试底线（覆盖率/数据规范/需求驱动） | fileMatch（test 目录/测试文件） |
| frontend.md | 前端编码底线（防御性数据消费/代码质量） | fileMatch（Vue/JS/TS 文件） |
| git.md | Git 工作流（Commit/Branch/Merge） | 按需（git 操作时） |
| sda-collaboration.md | SDA 协作规范（串行调度/Prompt自包含） | 按需（多 SDA 编排时） |

## Spec 工作流 — SDA 协作开发模式

**强制触发条件：用户确认 Plan 后，自动创建 Spec。**

### 完整流程图

```
┌─────────────────────────────────────────────────────────────────┐
│  第一阶段：需求分析 & Plan 输出                                    │
├─────────────────────────────────────────────────────────────────┤
│  1. 用户提需求                                                   │
│  2. AI 分析需求 → 输出 Plan                                       │
│  3. 用户确认 Plan                                                │
│  4. 【自动】调用 /sdc-spec 创建 Spec                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  第二阶段：SDA 协作产出 Spec 文件                               │
├─────────────────────────────────────────────────────────────────┤
│  5. requirements.md   ← 开发者/用户定义验收条件 AC 表              │
│  6. sda-architect agent  → 输出 design.md（数据库设计 + API 文档）   │
│  7. sda-architect agent  → 输出 test-cases.md（测试用例）            │
│  8. 填充 tasks.md     ← 任务清单（基于 design + test-cases）       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  第三阶段：实现 & 测试（使用 /sdc-dev 命令调度 SDA）                │
├─────────────────────────────────────────────────────────────────┤
│  /sdc-dev 命令读取 Spec 作为输入，串行调度：                        │
│                                                                 │
│  1. sda-db+sda-backend     → 创建数据表 SQL + API handler + service       │
│  2. sda-frontend        → Vue 页面 + 组件                            │
│  3. sda-tester          → E2E 测试（基于 test-cases.md）            │
│  4. sda-code-reviewer   → 代码审查                                   │
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
| design.md | sda-architect agent | 基于 requirements |
| test-cases.md | sda-architect agent | 与 design 同时产出 |
| tasks.md | 开发者/主 SDA | 基于 design + test-cases |

### Spec 创建步骤

1. 读取模板：`.claude/templates/spec/` 下的四个模板文件
2. 创建目录：`.claude/specs/<feature-name>/`
3. 填充内容：基于模板框架，结合具体需求填充业务内容
   - 替换 `{占位符}` 为具体值（如 `{功能名称}` → `会议室管理`）
   - 填充验收条件表（根据需求补充 AC-001、AC-002...）
   - **sda-architect agent** 填充数据库设计和 API 设计
   - **sda-architect agent** 根据验收条件为每个 AC 补充测试用例
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
2. sda-architect agent → design.md（技术方案 + 文件产出清单）
3. sda-architect agent → test-cases.md（测试用例）
4. tasks.md（任务清单）
5. **使用 /sdc-dev 命令** 启动 SDA 协作实现
6. **全部实现完成后**统一执行测试
7. **测试通过后**提交 Git（遵循 .claude/rules/git.md 的 Commit 规范）

> **约束**：CLAUDE.md 力求精简，只写 Claude 读代码推导不出的信息。项目信息字段和配置索引为结构化数据，不适用字数限制；正文（行为规范、禁止行为等）建议控制在 400 字内。
