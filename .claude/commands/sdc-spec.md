---
name: sdc-spec
description: 需求确认后创建 Spec 目录及四个核心文件
---

# /sdc-spec 命令规范

## 用途

用户确认需求后，开始实现前，按此流程创建 Spec 文件。Spec 是开发的唯一依据，所有 SDA 的实现必须以 Spec 为准。

## 触发场景

- `/sdc-plan` 确认后自动触发
- 用户手动调用 `/sdc-spec` 直接创建 Spec

## 前置条件

- 用户已确认 Plan，AI 已分析需求并得到用户认可
- 或用户直接提供需求描述

## Spec 命名规范

| 规则 | 说明 | 示例 |
|------|------|------|
| 使用英文短横线命名 | 功能名用 kebab-case | `order-management` |
| 与功能模块对应 | 名称反映业务含义 | `user-notification` |
| 避免过长的名称 | 控制在 3-5 个单词 | `product-category` |

## 工作流程

```
整理需求概要 → 创建 Spec 目录 → 生成 requirements.md → 评审 → 生成 design.md → 评审 → 生成 test-cases.md → 评审 → 生成 tasks.md → 评审 → Spec 完成
```

### 第一步：整理需求概要

AI 根据对话历史整理需求概要，向用户确认理解是否正确：

```markdown
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

每个文件生成后必须调用 sda-doc-reviewer agent 进行评审，通过后才进入下一步。

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
- 写文件规则：见 rules/sda-collaboration.md 和对应 SDA 配置文件
```

**评审**：调用 sda-doc-reviewer agent 评审 requirements.md
- 如有问题：修复 → 重新评审（最多 5 轮）
- 通过后继续

#### 3.2 生成 design.md

参考 `.claude/templates/spec/design.md` 模板，输出到 `.claude/specs/{feature}/design.md`：

```
你现在是 sda-architect agent。

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
7. 文件产出清单（每个 SDA 将创建的文件路径、方法签名、关键字段，确保 SDA 间路径对齐）

约束：
- 写文件规则：见 rules/sda-collaboration.md 和对应 SDA 配置文件
- 字符集规范：见 steer/foundation/tech.md「数据库字符集规范」节
- 字段命名参考项目现有风格
```

**评审**：调用 sda-doc-reviewer agent 评审 design.md
- 如有问题：修复 → 重新评审（最多 5 轮）
- 通过后继续

#### 3.3 生成 test-cases.md

参考 `.claude/templates/spec/test-cases.md` 模板，输出到 `.claude/specs/{feature}/test-cases.md`：

```
你现在是 sda-architect agent。

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

约束：
- 写文件规则：见 rules/sda-collaboration.md 和对应 SDA 配置文件
- 每个 AC 必须有对应测试用例
- E2E 必须包含三层验证：页面可达、数据加载、数据渲染
```

**评审**：调用 sda-doc-reviewer agent 评审 test-cases.md
- 如有问题：修复 → 重新评审（最多 5 轮）
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
4. 测试用例文档先行开发原则
5. 总计（预计工时、任务总数、进度）

约束：
- 写文件规则：见 rules/sda-collaboration.md 和对应 SDA 配置文件
- 任务 ID 格式：T-xxx（测试文档 T-DOC-xxx，单元测试 T-UT-xxx，E2E 测试 T-E2E-xxx）
- 任务粒度规范：见下方「任务粒度规范」
```

### 任务粒度规范

任务粒度直接影响开发效率和进度跟踪，遵循以下原则：

#### 粒度标准

| 维度 | 要求 | 说明 |
|------|------|------|
| **一个任务 = 一个 SDA 的一次产出** | 一个任务对应一个文件或一组强关联文件 | 如一个 DO 类 + 对应 Mapper 为一个任务 |
| **可独立验证** | 每个任务完成后可独立验证结果 | 如创建表后可 DESC 验证，创建 API 后可编译验证 |
| **可独立回滚** | 每个任务失败不影响其他任务 | 如一个 Service 创建失败不影响另一个 |
| **描述具体** | 任务描述包含具体文件路径和操作 | 而非"实现后端"这种模糊描述 |

#### 各阶段任务粒度参考

| 阶段 | 一个任务的粒度 | 示例 |
|------|---------------|------|
| 数据库 | 一张表的完整创建（SQL + DO + Mapper） | T-001: 创建 t_order 表及 OrderDO、OrderMapper |
| 后端 | 一组强关联的 VO + Service + Controller | T-010: 实现订单管理 API（OrderSaveReqVO + OrderService + OrderController） |
| 前端 | 一个页面的完整实现（API + 页面 + 组件） | T-020: 实现订单管理页面（api/order/index.js + views/order/index.vue + OrderForm.vue） |
| 测试 | 一个模块的测试套件 | T-030: 订单管理单元测试 / T-E2E-001: 订单管理 E2E 测试 |

#### 过细 vs 过粗的判断

| 问题 | 过细的表现 | 过粗的表现 | 合适的粒度 |
|------|-----------|-----------|-----------|
| 任务数量 | 一个功能拆出 20+ 个任务 | 一个功能只有 2-3 个任务 | 一个功能 5-10 个任务 |
| 依赖关系 | 大量串行依赖，无法并行 | 无法跟踪具体进度 | 依赖清晰，可部分并行 |
| 验证方式 | 每个任务验证成本高 | 无法独立验证 | 每个任务可独立验证 |
| 回滚影响 | 回滚影响极小 | 回滚影响极大 | 回滚范围可控 |

#### 任务拆分示例

**过细**（不推荐）：
```
T-001: 创建 t_order 表 SQL
T-002: 创建 OrderDO 实体类
T-003: 创建 OrderMapper 接口
T-004: 创建 OrderSaveReqVO
T-005: 创建 OrderPageReqVO
T-006: 创建 OrderRespVO
T-007: 创建 OrderService 接口
T-008: 创建 OrderServiceImpl
T-009: 创建 OrderController
```

**过粗**（不推荐）：
```
T-001: 实现订单管理功能
```

**合适**（推荐）：
```
T-001: 创建订单表及 DO/Mapper（SQL + OrderDO + OrderMapper）
T-010: 实现订单管理 API（OrderVO + OrderService + OrderController）
T-020: 实现订单管理页面（API 定义 + 列表页 + 表单弹窗）
T-030: 订单管理单元测试
T-E2E-001: 订单管理 E2E 测试
```

**评审**：调用 sda-doc-reviewer agent 评审 tasks.md
- 如有问题：修复 → 重新评审（最多 5 轮）
- 通过后 Spec 完成

## 文件模板索引

| 文件 | 模板位置 |
|------|----------|
| requirements.md | .claude/templates/spec/requirements.md |
| design.md | .claude/templates/spec/design.md |
| test-cases.md | .claude/templates/spec/test-cases.md |
| tasks.md | .claude/templates/spec/tasks.md |

## Spec 完成检查清单

四个文件全部通过评审后，主 CC 应自检以下要点：

- [ ] requirements.md：所有 AC 编号化，优先级明确，可验证
- [ ] design.md：表结构与 API 一致，字段完整，索引合理
- [ ] test-cases.md：每个 AC 有对应测试用例，覆盖异常流程
- [ ] tasks.md：任务无遗漏，依赖正确，无循环依赖
- [ ] 四个文件之间内容一致（AC 编号、字段名、API 路径对齐）
- [ ] 文件产出清单与 tasks.md 任务对应

## Spec 变更流程

### 变更触发方式

| 触发来源 | 场景 | 处理方式 |
|----------|------|----------|
| 用户主动提出 | 用户说"需求变了"、"加个字段"、"改一下逻辑" | 主 CC 识别变更范围，调用 `/sdc-spec` 更新 |
| 开发中发现 | SDA 实现时发现设计不合理或遗漏 | SDA 反馈问题，主 CC 评估后调用 `/sdc-spec` 更新 |
| 评审中发现 | sda-doc-reviewer 或 sda-code-reviewer 发现问题 | 评审报告驱动，主 CC 调用 `/sdc-spec` 更新 |
| 测试中发现 | sda-tester 发现功能与需求不符 | Bug 报告驱动，主 CC 评估后调用 `/sdc-spec` 更新 |

### 变更影响评估

收到变更请求后，主 CC 必须先评估影响范围：

```markdown
## 变更影响评估

### 变更内容
[一句话描述变更]

### 影响范围
| 文件 | 是否受影响 | 具体影响 |
|------|-----------|----------|
| requirements.md | 是/否 | [具体变更] |
| design.md | 是/否 | [具体变更] |
| test-cases.md | 是/否 | [具体变更] |
| tasks.md | 是/否 | [具体变更] |

### 已实现代码影响
| 模块 | 是否受影响 | 具体影响 |
|------|-----------|----------|
| 后端 | 是/否 | [具体文件] |
| 前端 | 是/否 | [具体文件] |
| 数据库 | 是/否 | [具体表] |

### 处理建议
- [更新 Spec 后继续实现 / 回滚已实现代码 / 暂缓变更]
```

### 变更处理流程

代码实现开始后，如需修改 Spec：

| 变更类型 | 处理方式 |
|----------|----------|
| 新增字段/接口 | 更新 design.md → 更新 test-cases.md → 更新 tasks.md → 重新评审 |
| 修改字段/接口 | 更新 design.md → 通知受影响的 SDA → 更新 test-cases.md |
| 删除字段/接口 | 更新 design.md → 确认无代码依赖 → 更新 test-cases.md |
| 需求变更 | 从 requirements.md 开始，全链路更新 |

### 变更执行步骤

```
1. 主 CC 评估变更影响范围
2. 向用户确认变更方案
3. 按影响范围更新 Spec 文件（从受影响的最早文件开始）
4. 对更新的文件重新调用 sda-doc-reviewer 评审
5. 通知受影响的 SDA 更新代码
6. 标注变更记录
```

### 变更标注格式

在修改的文件顶部标注变更记录：

```markdown
## 变更记录

| 日期 | 变更内容 | 影响范围 | 原因 |
|------|----------|----------|------|
| 2026-04-27 | 新增字段 `status` | design.md, test-cases.md | 业务需求变更 |
```

## 完成后

Spec 创建完成后，用户输入"继续"、"开始实现"等确认词，AI 使用 `/sdc-dev` 命令启动 SDA 协作实现。

## 注意事项

1. **必须先 Spec 再实现** — 禁止跳过 Spec 直接写代码
2. **四个文件缺一不可** — requirements / design / test-cases / tasks
3. **写文件规则** — 见 rules/sda-collaboration.md 和对应 SDA 配置文件
4. **模板是唯一权威** — 内容格式必须参考 `.claude/templates/spec/` 下的四个模板文件
5. **评审机制** — 每个文件生成后必须经过 sda-doc-reviewer agent 评审，通过后才能进入下一步
6. **多轮评审** — 最多 5 轮，5 轮后由用户决定是否继续
7. **文件间一致性** — 四个文件的 AC 编号、字段名、API 路径必须对齐
8. **Spec 变更需全链路更新** — 修改一个文件需检查其他文件是否受影响
