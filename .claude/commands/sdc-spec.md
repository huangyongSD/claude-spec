---
name: sdc-spec
description: 需求确认后创建 Spec 目录及四个核心文件
---

# /sdc-spec 命令规范

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

每个文件生成后必须调用 sda-reviewer agent 进行评审，通过后才进入下一步。

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
- 每次写入 ≤ 200 行，大文件分模块写入
```

**评审**：调用 sda-reviewer agent 评审 requirements.md
- 如有问题：修复 → 重新评审（最多 3 轮）
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
- 每次写入 ≤ 200 行，大文件分模块写入
- 字符集规范：SQL 脚本开头添加 SET NAMES utf8mb4;
- 字段命名参考项目现有风格
```

**评审**：调用 sda-reviewer agent 评审 design.md
- 如有问题：修复 → 重新评审（最多 3 轮）
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
- 每次写入 ≤ 200 行，大文件分模块写入
- 每个 AC 必须有对应测试用例
- E2E 必须包含三层验证：页面可达、数据加载、数据渲染
```

**评审**：调用 sda-reviewer agent 评审 test-cases.md
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
4. 测试用例文档先行开发原则
5. 总计（预计工时、任务总数、进度）

约束：
- 每次写入 ≤ 200 行，大文件分模块写入
- 任务 ID 格式：T-xxx（测试文档 T-DOC-xxx，单元测试 T-UT-xxx，E2E 测试 T-E2E-xxx）
```

**评审**：调用 sda-reviewer agent 评审 tasks.md
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

Spec 创建完成后，用户输入"继续"、"开始实现"等确认词，AI 使用 `/sdc-dev` 命令启动 SDA 协作实现。

## 注意事项

1. **必须先 Spec 再实现** — 禁止跳过 Spec 直接写代码
2. **四个文件缺一不可** — requirements / design / test-cases / tasks
3. **写文件规则** — 每次 ≤ 200 行，大文件分模块写入
4. **模板是唯一权威** — 内容格式必须参考 `.claude/templates/spec/` 下的四个模板文件
5. **评审机制** — 每个文件生成后必须经过 sda-reviewer agent 评审，通过后才能进入下一步
6. **多轮评审** — 最多 3 轮，3 轮后由主 CC 决策是否继续
