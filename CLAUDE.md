# 项目 AI 协作规范

> 遵循「配置即代码」原则，所有变更需提交到版本控制。

## 项目信息

- **项目名称**：`yudao（芋道）`
- **技术栈**：`SpringBoot 2.7 + MyBatis-Plus + JDK8 / Vue2 + Element-UI`
- **数据库**：`MySQL`
- **中间件**：`Redis + Redisson（缓存/分布式锁）`

> 构建命令、测试命令、格式化命令等详见 .claude/steer/foundation/tech.md

## 目录结构约定

```
yudao-boot-mini/
├─ CLAUDE.md           # 本文件，项目 AI 协作说明书
└─ .claude/
   ├─ steer/          # 项目心智地图（foundation/domain）
   ├─ rules/          # 底线规则（安全/测试/Git）
   ├─ agents/          # 专用子代理（审查/排障）
   ├─ commands/        # 斜杠命令（sdc-plan/sdc-codereview/sdc-buildfix/sdc-dev/sdc-spec/sdc-dbquery）
   ├─ skills/          # 知识库
   ├─ templates/spec/  # Spec 模板（requirements/design/test-cases/tasks）
   ├─ specs/           # 功能级 Spec 目录
   ├─ tools/           # 工具（db-query.py/secrets-sync.py/secrets.json）
   ├─ hooks/           # 运行时校验 Hook
   └─ settings.json    # 基础配置
```

## 核心目录

| 目录 | 职责 |
|------|------|
| yudao-server | 主服务器聚合模块 |
| yudao-framework | 框架层（starter 组件） |
| yudao-module-system | 系统功能（用户、角色、权限、字典） |
| yudao-module-infra | 基础设施（代码生成、文件、定时任务） |
| yudao-dependencies | BOM 依赖版本管理 |
| yudao-ui-admin | 前端管理后台（Vue2 + Element-UI） |
| sql | 数据库初始化脚本 |

> 每个核心目录一行，根据扫描结果增减行数。禁止修改的目录详见 .claude/steer/foundation/never.md

## 行为规范

### 需求开发流程（强制）

**所有新功能开发必须遵循以下流程（详见 .claude/steer/domain/workflow.md）：**

```
沟通任务 → 文档生成 → 文档评审（最多5轮） → 触发开发 → 多Agent开发 → Per-Agent评审（最多5轮） → 编译验证 → Git提交
```

**触发 Spec 的时机：**
- 用户确认 Plan 后，AI 自动调用 `/sdc-spec` 创建 Spec 文件

**Spec 创建内容：**
- `.claude/specs/<name>/` 目录下创建四个文件：
  - `requirements.md` — 验收标准
  - `design.md` — 技术方案（含文件产出清单）
  - `test-cases.md` — 测试用例文档
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

1. **先想后写** — 不假设，不隐藏困惑。不确定先问，有更简方案就提。
2. **简洁优先** — 最少代码解决问题。不加未要求的功能/抽象/灵活性。
3. **精准改动** — 只动必须动的。不改相邻代码，不重构没坏的东西，匹配已有风格。
4. **目标驱动** — 定义可验证的成功标准。

### 敏感信息保护

- .claude/ 配置文件中禁止使用真实密码/IP，使用占位符替代（如 {{DB_MASTER_PASSWORD}}）
- 真实值存储在本地 .claude/tools/secrets.json（不提交 Git）
- 数据库操作通过 db-query.py 本地执行，不将密码传递给 AI 模型
- Hook 层在运行时检测和提醒敏感信息泄露

## 治理机制

| 时间点 | 动作 |
|--------|------|
| Day 1-3 | 每人实际使用，群内反馈问题 |
| Day 7 | 收集第一周反馈，微调 rules 和 CLAUDE.md |
| Day 14 | 评估 Hook 配置，调整检查规则 |
| Day 30 | 全面回顾：分档调整、覆盖率提升、新配置需求 |

## 存储位置

| 类型 | 位置 |
|------|------|
| 团队共享 | .claude/（Git 版本控制） |
| 个人偏好 | ~/.claude/（本地） |

## 配置索引

- **规则**：.claude/rules/security.md | testing.md | frontend.md | git.md | sda-collaboration.md
- **Steer**：.claude/steer/ — 项目心智地图，减少从零探索的 Token 消耗
- **Spec**：.claude/specs/ — 结构化任务流程
- **Spec 模板**：.claude/templates/spec/ — 创建 Spec 时读取的模板文件
- **命令**：/sdc-plan | /sdc-codereview | /sdc-buildfix | /sdc-dev | /sdc-spec | /sdc-dbquery
- **SDA**：sda-architect | sda-doc-reviewer | sda-db-implementer | sda-backend | sda-frontend | sda-code-reviewer（含覆盖率审计） | sda-tester | sda-build-error-resolver
- **工具**：db-query.py（只读数据库查询） | secrets-sync.py（敏感信息同步）
- **知识库**：.claude/skills/troubleshooting.md
- **权限/Hooks**：.claude/settings.json + .claude/hooks/
- **质量门禁**：见 .claude/steer/domain/quality-gate.md（10 项全绿才交付）

## Steer 文件 — 项目心智地图

| 类型 | 文件 | 加载模式 |
|------|------|---------|
| foundation | product.md / tech.md / structure.md / never.md | always（每次会话） |
| domain | workflow.md（CC/Trea 双模式工作流）/ quality-gate.md | fileMatch / auto（按需加载） |

## Rules 文件 — 底线规则

| 文件 | 职责 | 加载模式 |
|------|------|---------|
| security.md | 安全底线（凭证/密钥/SQL注入/XSS/权限/敏感信息保护） | fileMatch（Java/SQL/配置文件） |
| testing.md | 测试底线（覆盖率/数据规范/需求驱动） | fileMatch（test 目录/测试文件） |
| frontend.md | 前端编码底线（防御性数据消费/代码质量） | fileMatch（Vue/JS 文件） |
| git.md | Git 工作流（Commit/Branch/Merge） | 按需（git 操作时） |
| sda-collaboration.md | SDA 协作规范（串行调度/Prompt自包含） | 按需（多 SDA 编排时） |

## CC vs Trea 双模式

| 步骤 | CC 模式 | Trea 模式 |
|------|---------|-----------|
| 沟通 | 单线程对话 | 逐步 prompt-response |
| 文档/评审 | 上下文中评审，最多5轮 | 自包含 prompt，最多5轮 |
| Agent 执行 | 可并行（DB+Backend同时） | 严格串行 |
| 编译验证 | 后端+前端可并行 | 后端先，前端后 |

> 详细工作流见 .claude/steer/domain/workflow.md