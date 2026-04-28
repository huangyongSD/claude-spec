---
name: sds-spec
description: 需求确认后创建 Spec 目录及四个核心文件
---

# /sds-spec Skill 规范

## 用途

用户确认需求后，开始实现前，按此流程创建 Spec 文件。Spec 是开发的唯一依据，所有 SDA 的实现必须以 Spec 为准。

## 触发场景

- `/sds-plan` 确认后自动触发
- 用户手动调用 `/sds-spec` 直接创建 Spec

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
1. 功能概述（一句话描述 + 业务背景 + 目标用户 + 当前痛点）
2. 验收条件表（AC 编号化，AC 类型分类，优先级，验证方式）
3. 影响范围（后端/前端/数据库/依赖/菜单权限影响）
4. 用户故事（验收要点关联 AC 编号）
5. 非功能性需求（安全需求 + 性能需求 + 兼容性需求，每项关联 AC）
6. 业务规则（BR 编号化，关联 AC，与 AC 区别说明）
7. 边界情况（关联 AC，含常见边界场景清单）
8. 数据实体（核心实体 + 实体关系图）
9. 参考资料（结构化表格）
10. 需求完整性自检

约束：
- 写文件规则：见 rules/governance.md 和对应 SDA 配置文件
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
1. 技术方案概述（一句话描述 + 方案选择原因 + 需求追溯矩阵）
2. 数据库设计（新增表/修改表/回滚脚本，字段、索引、字符集声明）
3. API 设计（接口列表含 AC+BR 关联 + 接口详情含异常场景 + nil 兜底标注）
4. 安全设计（权限模型 + IDOR 防护 + 输入安全 + nil 集合兜底）
5. 前端设计（页面设计 + 菜单配置 + 防御性数据消费 + 组件设计）
6. 性能约束（数据量预估 + 索引策略 + 缓存策略 + 分页限制）
7. 关键决策
8. 数据流程图
9. 风险评估
10. 测试要点（关联 test-cases.md 用例 ID）
11. 文件产出清单（含回滚脚本 + 菜单 SQL）

约束：
- 写文件规则：见 rules/governance.md 和对应 SDA 配置文件
- 字符集规范：见 CLAUDE.md 数据库规范节
- 字段命名参考项目现有风格
```

**评审**：调用 sda-doc-reviewer agent 评审 design.md
- 如有问题：修复 → 重新评审（最多 5 轮）
- 通过后继续

#### 3.3 生成 test-cases.md

参考 `.claude/templates/spec/test-cases.md` 模板，输出到 `.claude/specs/{feature}/test-cases.md`：

```
你现在是主 CC（参考 sda-tester 的测试设计规范）。

任务：为 {功能名称} 编写测试用例

输入：
- 功能名称：{名称}
- 验收条件：AC-001...AC-00N
- 设计文档：.claude/specs/{feature}/design.md

输出文件：.claude/specs/{feature}/test-cases.md

必须包含以下章节（按模板格式）：
1. AC 覆盖追溯矩阵（每个 AC 关联覆盖用例 + design.md 章节）
2. 测试用例概览
3. 单元测试用例（对应 AC + BR，含覆盖检查）
4. E2E 测试用例（冒烟/功能/权限/状态流转/业务流程/前端防御性，含覆盖检查）
5. 测试数据规范（Seed 数据 + 测试账号覆盖 4 种角色）
6. 降级方案（E2E 未配置时）
7. 测试执行命令
8. 测试完整性自检

约束：
- 写文件规则：见 rules/governance.md 和对应 SDA 配置文件
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
1. 任务状态说明
2. AC→任务 追溯矩阵（每个 AC 关联实现任务 + 测试任务 + design.md 章节）
3. 任务列表（分阶段：测试用例文档 / 数据库+后端 / 前端 / 测试执行 / 编译验证 / 审查与质量门禁 / Git 提交）
4. 任务依赖关系图
5. 测试用例文档先行开发原则
6. 总计（含 AC 覆盖统计）
7. 阻塞问题记录
8. 变更记录

约束：
- 写文件规则：见 rules/governance.md 和对应 SDA 配置文件
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

#### 任务拆分示例

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

- [ ] requirements.md：所有 AC 编号化，AC 类型分类，优先级明确，可验证
- [ ] requirements.md：业务规则（BR）编号化，与 AC 关联
- [ ] requirements.md：非功能性需求明确（安全+性能+兼容性）
- [ ] requirements.md：数据实体和关系已定义
- [ ] design.md：需求追溯矩阵完整（每个 AC+BR 有覆盖章节）
- [ ] design.md：安全设计章节完整（权限模型+IDOR+输入安全+nil兜底）
- [ ] design.md：前端设计章节完整（页面+菜单+防御性消费+组件）
- [ ] design.md：性能约束章节完整（数据量+索引+缓存+分页）
- [ ] design.md：回滚脚本和菜单 SQL 在文件产出清单中
- [ ] test-cases.md：AC 覆盖追溯矩阵完整（每个 AC 有覆盖用例+design 章节）
- [ ] test-cases.md：权限类 AC 有 IDOR 测试，数据类 AC 有 UT
- [ ] test-cases.md：测试数据覆盖 4 种角色（admin/user/guest/empty）
- [ ] tasks.md：AC→任务追溯矩阵完整（每个 AC 有实现任务+测试任务+design 章节）
- [ ] tasks.md：包含编译验证阶段和质量门禁阶段
- [ ] 四个文件之间内容一致（AC 编号、BR 编号、字段名、API 路径对齐）
- [ ] 文件产出清单与 tasks.md 任务对应

## Spec 变更流程

### 变更触发方式

| 触发来源 | 场景 | 处理方式 |
|----------|------|----------|
| 用户主动提出 | 用户说"需求变了"、"加个字段"、"改一下逻辑" | 主 CC 识别变更范围，调用 `/sds-spec` 更新 |
| 开发中发现 | SDA 实现时发现设计不合理或遗漏 | SDA 反馈问题，主 CC 评估后调用 `/sds-spec` 更新 |
| 评审中发现 | sda-doc-reviewer 或 sda-code-reviewer 发现问题 | 评审报告驱动，主 CC 调用 `/sds-spec` 更新 |
| 测试中发现 | sda-tester 发现功能与需求不符 | Bug 报告驱动，主 CC 评估后调用 `/sds-spec` 更新 |

### 变更处理流程

代码实现开始后，如需修改 Spec：

| 变更类型 | 处理方式 |
|----------|----------|
| 新增字段/接口 | 更新 design.md → 更新 test-cases.md → 更新 tasks.md → 重新评审 |
| 修改字段/接口 | 更新 design.md → 通知受影响的 SDA → 更新 test-cases.md |
| 删除字段/接口 | 更新 design.md → 确认无代码依赖 → 更新 test-cases.md |
| 需求变更 | 从 requirements.md 开始，全链路更新 |

### 变更标注格式

在修改的文件顶部标注变更记录：

```markdown
## 变更记录

| 日期 | 变更内容 | 影响范围 | 原因 |
|------|----------|----------|------|
| 2026-04-27 | 新增字段 `status` | design.md, test-cases.md | 业务需求变更 |
```

## 完成后

Spec 创建完成后，用户输入"继续"、"开始实现"等确认词，AI 使用 `/sds-dev` Skill 启动 SDA 协作实现。

## 注意事项

1. **必须先 Spec 再实现** — 禁止跳过 Spec 直接写代码
2. **四个文件缺一不可** — requirements / design / test-cases / tasks
3. **写文件规则** — 见 rules/governance.md 和对应 SDA 配置文件
4. **模板是唯一权威** — 内容格式必须参考 `.claude/templates/spec/` 下的四个模板文件
5. **评审机制** — 每个文件生成后必须经过 sda-doc-reviewer agent 评审，通过后才能进入下一步
6. **多轮评审** — 最多 5 轮，5 轮后由用户决定是否继续
7. **文件间一致性** — 四个文件的 AC 编号、字段名、API 路径必须对齐
8. **Spec 变更需全链路更新** — 修改一个文件需检查其他文件是否受影响