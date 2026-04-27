---
name: sdc-dev
description: 全栈开发编排，按 sda-db+sda-backend→sda-frontend→sda-tester→reviewer 串行调度，每个阶段含多轮评审
---

# /sdc-dev 命令规范

## 触发场景

- 新项目全栈开发
- 大规模功能实现（多模块协同）
- 需要完整开发流程编排

## 概念说明

> **调度粒度 vs 任务粒度**：
> - **本文档（sdc-dev.md）** 定义的是 **调度阶段（Phase）**，每个阶段对应一个 SDA 执行单元
> - **tasks.md** 定义的是 **具体任务（Task）**，是调度阶段的细粒度拆分
> - 一个 Phase 可能包含多个 Task，例如"数据库阶段"包含 T-001~T-003

## 编排流程

### 第一阶段：准备

> **前置条件**：需求确认后，必须先按 CLAUDE.md 的 Spec 工作流创建 `.claude/specs/<feature>/` 下的四个文件（requirements / design / test-cases / tasks），/sdc-dev 命令读取这些 Spec 作为输入。

**E2E 测试框架检查（必须）**：

在开始编排前，检查项目是否已配置 E2E 测试框架：
1. 检查 `package.json` 中是否安装了 Playwright / Cypress / Nightwatch 等依赖
2. 检查是否存在 E2E 测试配置文件（如 `playwright.config.ts`、`cypress.config.ts`）
3. 如**未配置**：
   - **提醒用户**：当前项目未配置 E2E 测试框架，sda-tester 阶段将跳过 E2E 测试代码编写
   - **建议排期**：建议在 Day 30 回顾时评估 E2E 测试框架引入计划
   - **降级方案**：E2E 测试相关的任务（T-E2E-xxx）降级为人工验收，质量门禁第 3-5 项降级处理
   - **继续执行**：用户确认后，跳过 sda-tester 阶段的 E2E 测试部分，仅保留单元测试

1. 读取需求文档（.claude/specs/*/requirements.md）
2. 读取设计文档（.claude/specs/*/design.md）
3. 读取测试用例文档（.claude/specs/*/test-cases.md）
4. 读取任务清单（.claude/specs/*/tasks.md）

### 第二阶段：串行调度（含阶段内评审）

> **注意**：架构设计已在 Spec 阶段由 sda-architect agent 完成（design.md），本阶段直接进入实现。

> **阶段内评审机制**：每个 SDA 阶段完成后，必须调用 sda-code-reviewer 对该阶段的产出进行评审。评审不通过则修复后重新评审，最多 3 轮。3 轮后仍有问题则暂停等待人工决策。通过后才进入下一阶段。

按顺序调度以下阶段：

| 序号 | 阶段 | SDA | 阶段内评审 | 输入 | 对应 tasks.md 阶段 |
|------|------|-------|-----------|------|-------------------|
| 1 | 数据库实现 | sda-db-implementer | sda-code-reviewer 评审 DB 产出 | design.md（Schema + 文件产出清单） | 阶段二：数据库 |
| 1a | DB 评审修复 | sda-db-implementer | 重新评审（最多 3 轮） | 审查报告 | — |
| 2 | 后端实现 | sda-backend | sda-code-reviewer 评审后端产出 | design.md（API + 文件产出清单）、DB 产出文件 | 阶段二：后端 |
| 2a | 后端评审修复 | sda-backend | 重新评审（最多 3 轮） | 审查报告 | — |
| **2b** | **后端编译验证** | **sda-backend** | **运行 `mvn clean compile`，失败则调用 sda-build-error-resolver 修复** | **后端代码** | **—** |
| 3 | 前端实现 | sda-frontend | sda-code-reviewer 评审前端产出 | design.md（API + 文件产出清单）、后端 API 端点、原型 HTML | 阶段三：前端 |
| 3a | 前端评审修复 | sda-frontend | 重新评审（最多 3 轮） | 审查报告 | — |
| **3b** | **前端编译验证** | **sda-frontend** | **运行 `yarn build`，失败则调用 sda-build-error-resolver 修复** | **前端代码** | **—** |
| 4 | 测试执行 | sda-tester | sda-code-reviewer 评审测试代码 | test-cases.md、前端页面 | 阶段四：测试执行 |
| 4a | 测试评审修复 | sda-tester | 重新评审（最多 3 轮） | 审查报告 | — |
| 5 | 全量代码审查 | sda-code-reviewer | — | 所有代码文件 | 阶段五：审查 |
| 6 | 提交 Git | 主 CC | — | 审查通过 | 阶段六：提交 Git |

> **SDA 说明**：
> - **独立配置 SDA**：sda-db-implementer / sda-backend / sda-frontend / sda-tester / sda-code-reviewer 有独立配置文件（见 `.claude/agents/` 目录）
> - **修复机制**：评审不通过时，重新调度产出该代码的 SDA（附加审查报告上下文）进行修复，无需单独的 fixer 角色

### 第三阶段：全量审查问题修复

1. 汇总阶段 5 全量审查报告，按 P0/P1/P2 分类
2. 按问题归属重新调度对应 SDA 修复（DB 问题→sda-db-implementer，后端问题→sda-backend，前端问题→sda-frontend，测试问题→sda-tester）
3. 修复后重新运行测试
4. 重新提交 sda-code-reviewer 审查（最多 3 轮）

### 第四阶段：质量门禁验证

运行质量门禁清单（见 `.claude/steer/domain/quality-gate.md`），全部通过才交付。

## SDA 配置索引

### 独立配置 SDA

| SDA | 配置文件 | 职责 |
|-------|---------|------|
| sda-architect | .claude/agents/sda-architect.md | 输出 Schema + API 文档 + 设计决策（Spec 阶段使用） |
| sda-reviewer | .claude/agents/sda-reviewer.md | Spec 文档评审（Spec 阶段使用） |
| sda-db-implementer | .claude/agents/sda-db-implementer.md | 创建数据库表、DO 实体类、Mapper 接口 |
| sda-backend | .claude/agents/sda-backend.md | 创建 VO、Service、Controller |
| sda-frontend | .claude/agents/sda-frontend.md | 创建 API 定义、页面、组件 |
| sda-tester | .claude/agents/sda-tester.md | 编写/修复 E2E 测试 |
| sda-code-reviewer | .claude/agents/sda-code-reviewer.md | 审查质量/安全/可维护性 |
| sda-build-error-resolver | .claude/agents/sda-build-error-resolver.md | 修复构建/测试错误 |

### 修复机制（无独立配置文件，复用实现 SDA）

| 问题归属 | 修复 SDA | 调度方式 |
|----------|---------|---------|
| 数据库层 | sda-db-implementer | 重新调度，附加审查报告 |
| 后端层 | sda-backend | 重新调度，附加审查报告 |
| 前端层 | sda-frontend | 重新调度，附加审查报告 |
| 测试代码 | sda-tester | 重新调度，附加审查报告 |

## Prompt 模板

> **注意**：以下 agent 有独立配置文件，调用时会自动加载配置中的规范约束。主 CC 只需提供任务上下文，无需重复说明规范。

### 自动编排调度流程

`/sdc-dev` 命令执行时，主 CC 按以下流程自动调度 SDA，每个阶段完成后自动进入下一阶段，无需人工干预：

```
读取 Spec → 检查 E2E 框架 → 调度 sda-db-implementer → 评审 → [sda-db-implementer 修复→重审]×3 → 调度 sda-backend → 评审 → [sda-backend 修复→重审]×3 → **后端编译验证（mvn compile，失败调用 sda-build-error-resolver）** → 调度 sda-frontend → 评审 → [sda-frontend 修复→重审]×3 → **前端编译验证（yarn build，失败调用 sda-build-error-resolver）** → 调度 sda-tester → 评审 → [sda-tester 修复→重审]×3 → 全量审查 → 按归属调度 SDA 修复 → [重审]×3 → 质量门禁
```

每个 SDA 阶段完成后，立即调用 sda-code-reviewer 对该阶段产出进行评审。评审不通过则修复后重新评审（最多 3 轮），3 轮后仍有问题暂停等待人工决策。通过后才进入下一阶段。

### 完整调度 Prompt 模板

以下为每个阶段的完整调度 prompt，主 CC 按顺序逐个执行：

#### 阶段 1：sda-db-implementer 调度

```
你现在是 sda-db-implementer（配置文件：.claude/agents/sda-db-implementer.md）。

任务：根据设计文档创建数据库结构

输入：
- 设计文档：{SPEC_DIR}/design.md
- 数据库设计章节：第 2 节
- 文件产出清单：design.md 第 8 节

输出：
- SQL 脚本：创建数据库表
- DO 实体类：对应数据库表的实体
- Mapper 接口：MyBatis Mapper

约束：
- 每次写入 ≤ 200 行，大文件分模块写入
- SQL 脚本开头添加 SET NAMES utf8mb4;
- 参考 .claude/agents/sda-db-implementer.md 中的规范约束执行

完成后：列出所有已创建的文件路径，供后续 agent 参考。
```

**阶段内评审**：调用 sda-code-reviewer 评审 sda-db-implementer 产出
- 审查范围：SQL 脚本、DO 实体类、Mapper 接口
- 审查维度：表结构完整性（对照 design.md）、字段类型正确性、索引合理性、命名规范
- 如有问题：重新调度 sda-db-implementer 修复（附加审查报告） → 重新评审（最多 3 轮）
- 通过后继续

#### 阶段 2：sda-backend 调度

```
你现在是 sda-backend（配置文件：.claude/agents/sda-backend.md）。

前置：sda-db-implementer 已完成数据库结构创建，产出文件：{sda-db-implementer 输出的文件列表}

任务：根据设计文档实现后端 API

输入：
- 设计文档：{SPEC_DIR}/design.md
- API 设计章节：第 3 节
- 文件产出清单：design.md 第 8 节
- 测试用例文档：{SPEC_DIR}/test-cases.md
- sda-db-implementer 产出文件：参考文件产出清单中的 DO/Mapper 路径

输出：
- VO 类（Req/Resp/Page）
- Service 接口和实现
- Controller

约束：
- 每次写入 ≤ 200 行，大文件分模块写入
- Service 层返回空集合而非 null
- 使用 @Valid 校验参数
- 权限注解必须与前端路由守卫同步
- 参考 .claude/agents/sda-backend.md 中的规范约束执行

完成后：列出所有已创建的文件路径和 API 端点路径，供后续 SDA 参考。
```

**阶段内评审**：调用 sda-code-reviewer 评审 sda-backend 产出
- 审查范围：VO 类、Service 接口和实现、Controller
- 审查维度：API 完整性（对照 design.md）、参数校验、权限注解、null 返回路径、错误处理
- 如有问题：重新调度 sda-backend 修复（附加审查报告） → 重新评审（最多 3 轮）

**后端编译验证**（评审通过后执行）：
- 运行 `mvn clean compile` 验证 Java 代码可编译
- 如编译失败：调用 sda-build-error-resolver 诊断并修复错误
- 修复后重新编译验证，通过后才进入下一阶段

#### 阶段 3：sda-frontend 调度

```
你现在是 sda-frontend（配置文件：.claude/agents/sda-frontend.md）。

前置：sda-backend 已完成后端 API 实现，产出文件：{sda-backend 输出的文件列表}，API 端点：{sda-backend 输出的端点列表}

任务：根据设计文档实现前端页面

输入：
- 设计文档：{SPEC_DIR}/design.md
- API 设计章节：第 3 节
- 文件产出清单：design.md 第 8 节（含后端 API 路径和方法签名）
- 后端 API 端点：{sda-backend 输出的端点列表}
- 原型 HTML：（如有提供）

输出：
- API 定义文件（api/xxx.js）
- 列表页面
- 表单弹窗

约束：
- 每次写入 ≤ 200 行，大文件分模块写入
- API 返回值一律加空值守卫（?? []）
- 权限指令 v-hasPermi 与后端 @PreAuthorize 必须同步
- 参考 .claude/agents/sda-frontend.md 中的规范约束执行

完成后：列出所有已创建的文件路径，供后续 agent 参考。
```

**阶段内评审**：调用 sda-code-reviewer 评审 sda-frontend 产出
- 审查范围：API 定义文件、列表页面、表单弹窗
- 审查维度：空值守卫（?? []）、权限指令与后端同步、placeholder 残留、UI 交互完整性
- 如有问题：重新调度 sda-frontend 修复（附加审查报告） → 重新评审（最多 3 轮）

**前端编译验证**（评审通过后执行）：
- 运行 `yarn build` 验证前端代码可编译
- 如编译失败：调用 sda-build-error-resolver 诊断并修复错误
- 修复后重新编译验证，通过后才进入下一阶段

#### 阶段 4：sda-tester 调度

```
你现在是 sda-tester（配置文件：.claude/agents/sda-tester.md）。

前置：sda-frontend 已完成前端页面实现，所有功能页面已可访问。

任务：基于测试用例文档编写和执行测试

输入：
- 测试用例文档：{SPEC_DIR}/test-cases.md
- 任务清单：{SPEC_DIR}/tasks.md（阶段四的测试任务）
- 前端页面路径：{sda-frontend 输出的文件列表}

输出：
- 单元测试代码（基于 test-cases.md 中的 UT 用例）
- E2E 测试代码（基于 test-cases.md 中的 E2E 用例，如 E2E 框架已配置）
- 测试执行结果

约束：
- 每次写入 ≤ 200 行，大文件分模块写入
- E2E 测试必须包含三层验证：页面可达、数据加载、数据渲染非空
- 全局错误监听：pageerror + console.error + 微任务等待
- 测试数据覆盖关键角色组合（超级管理员、普通用户、无权限用户）
- 如项目未配置 E2E 测试框架，跳过 E2E 测试代码编写，仅编写单元测试
- 参考 .claude/agents/sda-tester.md 中的规范约束执行

完成后：输出测试报告（通过/失败数量），如有失败列出失败用例。
```

**阶段内评审**：调用 sda-code-reviewer 评审 sda-tester 产出
- 审查范围：单元测试代码、E2E 测试代码
- 审查维度：测试覆盖率（对照 test-cases.md）、断言有效性、测试数据合理性、三层验证完整性
- 如有问题：重新调度 sda-tester 修复（附加审查报告） → 重新评审（最多 3 轮）
- 通过后继续

#### 阶段 5：sda-code-reviewer 全量审查调度

```
你现在是 sda-code-reviewer（配置文件：.claude/agents/sda-code-reviewer.md）。

前置：所有 SDA 阶段已完成，且各阶段内评审已通过。

任务：对本次功能开发的所有代码变更进行全量审查（跨阶段交叉检查）

输入：
- 需求文档：{SPEC_DIR}/requirements.md
- 设计文档：{SPEC_DIR}/design.md
- 所有新增/修改的文件：{汇总所有 agent 输出的文件列表}

审查维度（5 项 + 交叉检查）：
1. 质量：逻辑正确性、边界情况、错误处理
2. 安全：SQL 注入/XSS/敏感信息/权限（对照 rules/security.md 🔴 级别规则）
3. 可维护性：命名、函数长度、重复代码
4. 性能：不必要的循环/N+1/缓存
5. 测试覆盖：新增代码是否有测试、覆盖率
6. 交叉一致性：前后端 API 参数/路径是否对齐、数据库字段与 DO 实体是否一致、前后端权限是否同步

额外检查项（智能体质量门禁）：
- nil 返回路径检查：后端 API 是否可能返回 null 集合
- 裸赋值检查：前端是否直接赋值 API 返回值
- 前后端权限一致性：前端路由守卫与后端 API 权限是否同步
- placeholder 残留：TODO、FIXME、硬编码假数据

输出：按 P0/P1/P2 分类的问题清单

参考 .claude/agents/sda-code-reviewer.md 中的规范约束执行。
```

#### 阶段 6：问题修复（如全量审查有问题）

按问题归属重新调度对应 SDA 修复（与阶段内评审修复机制一致，附加审查报告上下文）：

```
你现在是 {sda-db-implementer / sda-backend / sda-frontend / sda-tester}（配置文件：.claude/agents/{对应配置文件}）。

前置：sda-code-reviewer 全量审查发现以下问题：{P0/P1 问题清单}

任务：修复审查发现的问题

输入：
- 审查报告：{sda-code-reviewer 输出}
- 需要修复的文件：{根据问题清单确定}

约束：
- 一次只修一个问题，修完验证
- 修复后不影响其他功能
- 每次写入 ≤ 200 行
- 参考 .claude/agents/{对应配置文件} 中的规范约束执行

修复完成后：重新运行测试确认通过，再重新提交 sda-code-reviewer 审查（最多 3 轮）。
3 轮后仍有 P0/P1 问题，暂停等待人工决策。
```

#### 阶段 7：质量门禁 + Git 提交

```
所有代码已通过审查，执行质量门禁检查：

1. 运行编译/类型检查：{BUILD_CMD}
2. 运行测试：{TEST_CMD}
3. 检查 TODO/FIXME/占位符残留
4. 确认无占位符残留后提交 Git

提交信息遵循 .claude/rules/git.md 的 Commit 规范：
type(scope): subject

Body 包含本次变更的文件说明和 review 重点。
```

## 注意事项

1. **每个 SDA 的 prompt 必须自包含**：看不到对话历史，需要完整上下文
2. **写文件规则在 prompt 开头强调**：≤200 行/次，大文件分模块写入
3. **全新代码也要审查**：AI 生成的代码存在权限缺失、校验遗漏等问题
4. **测试用例文档先行**：test-cases.md 在 Spec 阶段已创建，实现阶段参考测试用例文档编写代码
5. **阶段内评审必须执行**：每个 SDA 阶段完成后立即评审，不可跳过，不可延迟到全量审查
6. **多轮评审上限**：每个评审点最多 3 轮，3 轮后由主 CC 决策是否继续修复或标记为已知问题
7. **评审修复分工**：评审发现问题后，重新调度产出该代码的 SDA 修复——数据库问题→sda-db-implementer，后端问题→sda-backend，前端问题→sda-frontend，测试问题→sda-tester。修复 prompt 必须附加审查报告上下文
