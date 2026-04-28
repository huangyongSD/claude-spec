---
inclusion: auto
name: workflow
description: 开发工作流规范，兼容 CC（并行）和 Trea（串行）模式
updated: 2026-04-27
---

# 开发工作流规范

## 工作流步骤（7 步）

### Step 1：沟通先行 — 与用户讨论任务

- 用户提出需求（新功能、Bug 修复、功能优化）
- AI 基于项目信息与用户沟通、细化方案
- 澄清需求细节：影响范围、验收标准、技术约束
- 输出：需求理解文档（口头确认或简短文档）

**CC 模式**：单一对话线程
**Trea 模式**：逐步 prompt-response，每步包含项目上下文

### Step 2：文档生成 — 输出 Plan 和 Spec

- 基于沟通结果生成 Plan
- 用户确认 Plan 后，自动调用 `/sdc-spec` 创建 Spec 四文件
- Spec 文件：requirements.md / design.md / test-cases.md / tasks.md

**两种模式相同**，Spec 文件是持久化的跨 agent 通信载体

### Step 3：文档评审 — 多轮评审直到通过

- 调用 sda-doc-reviewer 对 Spec 文件进行评审
- 最多 5 轮评审，每轮评审后修复问题并重新提交
- 5 轮后由用户决定：接受当前状态 / 继续额外轮次 / 拒绝重设计

**CC 模式**：在当前上下文中调用 sda-doc-reviewer
**Trea 模式**：每次评审为独立自包含 prompt

### Step 4：触发开发 — 自动或手动

- 评审通过后：自动拉起 `/sdc-dev` 开发流程
- 用户也可自主触发 `/sdc-dev`

### Step 5：多 Agent 开发

**CC 模式**（并行）：
- Phase A（并行）：sda-db-implementer + sda-backend 合并为一个调度单元
- Phase B（依赖 A 完成）：sda-frontend
- Phase C（依赖 B 完成）：sda-tester

**Trea 模式**（串行）：
- 同样的调度顺序，但严格串行执行
- 每个 agent 独立 prompt，prompt 必须自包含（包含需求路径、设计路径、文件清单）

### Step 6：Per-Agent 独立评审

- 每个 agent 完成后由 sda-code-reviewer 进行评审
- 最多 5 轮评审，5 轮后由用户决定
- 评审不通过：重新调度该 agent 修复（附加审查报告上下文）

### Step 7：编译验证

所有 agent 完成后：
1. 后端编译：`mvn clean compile`（或 `mvn clean package -Dmaven.test.skip=true`）
2. 前端编译：`yarn install && yarn build:prod`（或 `yarn local` 验证开发模式）
3. 启动验证：后端端口 48080、前端端口 80 可达
4. 数据库状态验证：`python .claude/tools/db-query.py --query "SHOW TABLES" --format table`
5. 全量代码审查：sda-code-reviewer 跨阶段交叉检查
6. 质量门禁：见 steer/domain/quality-gate.md

## CC vs Trea 执行矩阵

| 步骤 | CC 模式 | Trea 模式 |
|------|---------|-----------|
| 1. 沟通 | 单线程对话 | 逐步 prompt-response |
| 2. 文档生成 | 相同流程 | 相同流程 |
| 3. 评审 | 上下文中评审，最多 5 轮 | 自包含 prompt 评审，最多 5 轮 |
| 4. 触发 | 评审通过后自动拉起 /sdc-dev | 用户手动确认触发 |
| 5. Agent 执行 | 可并行（DB+Backend 同时） | 严格串行 |
| 6. Per-agent 评审 | 上下文中评审 | 自包含 prompt 评审 |
| 7. 编译验证 | 后端+前端编译可并行 | 后端先，前端后 |

## 评审轮次上限：5 轮

所有评审点最多 5 轮。5 轮后用户决定：
- 接受当前状态（已知问题记录在 tasks.md）
- 继续额外轮次（用户手动触发）
- 拒绝并重新设计

## 敏感信息保护

- .claude/ 配置文件中使用占位符（{{DB_MASTER_PASSWORD}} 等），不使用真实密码/IP
- 真实值存储在 .claude/tools/secrets.json（本地，不提交 Git）
- 数据库操作通过 db-query.py 本地执行，不将密码传递给 AI 模型
- Hook 层在运行时检测和提醒敏感信息泄露