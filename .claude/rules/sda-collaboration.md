---
description: SDA 协作规范
type: rules
updated: 2026-04-22
---

# SDA 协作规范

## 🟡 新代码执行

### 串行保证正确性
SDA 编排分两个阶段，必须按依赖顺序串行执行：

**Spec 阶段**（由 `/sdc-spec` 命令触发）：
```
主CC（输出 requirements.md）→ sda-reviewer（评审）→ sda-architect（输出 design.md）→ sda-reviewer（评审）→ sda-architect（输出 test-cases.md）→ sda-reviewer（评审）→ 主CC（输出 tasks.md）→ sda-reviewer（评审）
```

**实现阶段**（由 `/sdc-dev` 命令触发）：
```
sda-db+sda-backend → sda-frontend → sda-tester → sda-code-reviewer
```

每一层基于上一层产出，不能跳步。

- sda-db-implementer 和 sda-backend 共用 design.md 作为唯一输入，合并为一个阶段减少上下文传递断裂点
- sda-backend 直接在 sda-db-implementer 产出（DO 实体类、Mapper）之上构建 Service/Controller，紧耦合无需跨阶段
- design.md 中的「文件产出清单」确保 agent 之间文件路径对齐
- sda-frontend 需要基于 sda-backend 的 API 和文件产出清单实现页面
- sda-tester 需要基于前端页面编写测试
- reviewer 最后审查所有代码

### Prompt 自包含
每个 SDA 看不到对话历史，prompt 必须包含：
- 需求文档路径
- 设计决策文件路径
- 相关文件清单
- 具体改动描述

**为什么必须自包含**：
- SDA 只能看到当前对话的消息，看不到之前的上下文
- 缺少上下文会导致 agent 凭猜测工作，产出不符合预期

### 写文件规则
每次写入 ≤ 200 行，大文件分模块写入。

**为什么限制行数**：
- 工具参数有长度限制，超过会截断
- 截断导致 agent 无限重试，浪费时间和 token
- 分块追加保证每次操作都是有效的

### SDA Team 组织

**有独立配置文件的 SDA（9 个）**：

| SDA | 阶段 | 角色 | 职责 | 配置文件 |
|-------|------|------|------|---------|
| sda-architect | Spec | 架构师 | 输出 Schema + API 文档 + 设计决策 + 测试用例文档 | 6.13 节 |
| sda-reviewer | Spec | Spec 评审 | 对 Spec 文件（requirements/design/test-cases/tasks）进行结构化评审 | 6.15 节 |
| sda-db-implementer | 实现 | 数据库实现 | 创建数据库表、DO 实体类、Mapper 接口 | 6.16 节（与 sda-backend 合并调度） |
| sda-backend | 实现 | 后端实现 | 创建 VO、Service、Controller | 6.17 节（与 sda-db-implementer 合并调度） |
| sda-frontend | 实现 | 前端实现 | 创建 API 定义、页面、组件 | 6.18 节 |
| sda-tester | 实现 | 测试工程师 | 编写/修复 E2E 测试 | 6.19 节 |
| sda-code-reviewer | 实现 | 代码审查 | 审查质量/安全/可维护性 | 6.14 节 |
| sda-coverage-auditor | 实现 | 覆盖率审计 | 独立审计覆盖率真实性 | 6.20 节 |
| sda-build-error-resolver | 实现 | 构建排障 | 修复构建/测试错误 | 6.21 节 |

> **阶段说明**：Spec 阶段的 SDA（sda-architect、sda-reviewer）由 `/sdc-spec` 命令调度，产出设计文档和测试用例文档；实现阶段的 SDA（sda-db-implementer 至 sda-build-error-resolver）由 `/sdc-dev` 命令调度，产出代码和测试。两个阶段不可交叉——实现阶段必须等 Spec 阶段全部完成（四个 Spec 文件均通过评审）后才开始。

**修复机制**：评审发现问题后，重新调度产出该代码的 SDA 进行修复（而非单独的 fixer 角色）：

| 问题归属 | 修复 SDA | 说明 |
|----------|---------|------|
| 数据库层（SQL、DO、Mapper） | sda-db-implementer | 重新调度，附加审查报告上下文 |
| 后端层（VO、Service、Controller） | sda-backend | 重新调度，附加审查报告上下文 |
| 前端层（Vue、TS、组件） | sda-frontend | 重新调度，附加审查报告上下文 |
| 测试代码 | sda-tester | 重新调度，附加审查报告上下文 |

> **设计原则**：产出代码的 SDA 最了解自身上下文，适合修复自己的问题。修复时重新调度该 SDA，在 prompt 中附加审查报告和具体问题清单，SDA 基于自身配置规范执行修复。无需单独的 fixer 角色和配置文件。

### 并行 vs 串行调度

**可并行**（无文件冲突）：
- sda-tester + sda-frontend（不同目录）
- sda-coverage-auditor + 任何 SDA（只读）
- 多个调查 SDA

**必须串行**（有文件依赖）：
- sda-backend 修复 → sda-tester 重跑
- sda-coverage-auditor 审计 → sda-tester 修复虚假覆盖

## 🟢 逐步达标

### 全新代码也要审查
AI 生成的代码存在权限缺失、校验遗漏等问题，审查不可省略。

**审查清单要点**：
- nil 返回路径
- 裸赋值
- 前后端权限一致性
- placeholder 残留

## 执行方式

🟡 级别在 SDA 编排时强制执行。
🟢 级别作为团队习惯逐步养成，不强制。

## 关键洞察（来自生产级项目实战）

- **SDA prompt 必须自包含**：每个 SDA 看不到对话历史，prompt 中要包含需求文档路径、设计决策、文件清单、具体改动描述
- **写文件规则在 prompt 开头强调**：≤200 行/次，大文件分模块写入
- **全新项目也需要代码审查**：AI 生成的代码不等于正确的代码，本次审查发现了 10 个 P0 级安全/逻辑问题
