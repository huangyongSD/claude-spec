---
name: sds-dev
description: 全栈开发编排，按 sda-db+sda-backend→sda-frontend→sda-tester→reviewer 串行调度，每个阶段含多轮评审
---

# /sds-dev Skill 规范

## 用途

根据 Spec 文件编排全栈开发流程，按阶段调度 SDA 执行实现，每阶段含评审和编译验证，确保代码质量。

## 触发场景

- `/sds-spec` 完成后，用户确认"开始实现"
- 用户手动调用 `/sds-dev` 直接启动开发（需已有 Spec 文件）

## 前置条件

- Spec 文件已创建并通过评审（`.claude/specs/<feature>/` 下四个文件）
- 项目环境可编译（后端 `mvn compile`、前端 `yarn build:prod`）

## 执行模式

> 工作流编排规范见本文件后续章节

**CC 模式（Claude Code）**：所有阶段严格串行。每个 SDA 需要前序 SDA 的产出文件存在于磁盘才能进行前置发现，不可并行。
**Trea 模式（类似 Cursor/Trae）**：严格串行。每步一个 prompt，prompt 必须自包含（包含需求路径、设计路径）。不可跳步。

## 概念说明

> **调度粒度 vs 任务粒度**：
> - **本文档（sds-dev.md）** 定义的是 **调度阶段（Phase）**，每个阶段对应一个 SDA 执行单元
> - **tasks.md** 定义的是 **具体任务（Task）**，是调度阶段的细粒度拆分
> - 一个 Phase 可能包含多个 Task，例如"数据库阶段"包含 T-001~T-003

## 编排总览

```
准备 → DB实现→评审→修复 → 后端实现→评审→编译验证 → 前端实现→评审→编译验证 → 测试→评审 → 全量审查→修复 → 质量门禁→Git提交
```

| 阶段 | SDA | 评审 | 编译验证 | 最多轮次 |
|------|-----|------|----------|----------|
| 1. 数据库 | sda-db-implementer | sda-code-reviewer | — | 5 |
| 2. 后端 | sda-backend | sda-code-reviewer | mvn compile | 5 |
| 3. 前端 | sda-frontend | sda-code-reviewer | yarn build:prod | 5 |
| 4. 测试 | sda-tester | sda-code-reviewer | — | 5 |
| 5. 全量审查 | sda-code-reviewer | — | — | 5 |
| 6. 质量门禁 | 主 CC | — | 全量 | — |

## 编排流程

### 第一阶段：准备

> **前置条件**：需求确认后，必须先按 CLAUDE.md 的 Spec 工作流创建 `.claude/specs/<feature>/` 下的四个文件（requirements / design / test-cases / tasks），/sds-dev Skill 读取这些 Spec 作为输入。

**E2E 测试框架检查（强制）**：

> **前置保证**：项目初始化时（`/sds-init`）已处理 E2E 框架配置，此处仅做验证。

在开始编排前，检查项目 E2E 状态：
1. 检查 `package.json` 中是否安装了 Playwright / Cypress / Nightwatch 等依赖
2. 检查是否存在 E2E 测试配置文件（如 `playwright.config.js`、`cypress.config.ts`）
3. **Web 端项目**（Vue/React/Angular 等）：
   - 如已配置 Playwright：继续执行
   - 如未配置：**阻断执行**，提示用户先调用 `/sds-init` 配置 E2E 框架
4. **移动端项目**（uni-app/React Native/Flutter/Taro 等）：
   - **E2E 降级为人工验收**，不阻断执行
   - 在 tasks.md 中标注 T-E2E 任务为"人工验收"
5. **纯后端项目**：
   - 跳过 E2E 相关任务，不阻断执行

1. 读取需求文档（.claude/specs/*/requirements.md）
2. 读取设计文档（.claude/specs/*/design.md）
3. 读取测试用例文档（.claude/specs/*/test-cases.md）
4. 读取任务清单（.claude/specs/*/tasks.md）

### 第二阶段：串行调度（含阶段内评审）

> **注意**：架构设计已在 Spec 阶段由 sda-architect agent 完成（design.md），本阶段直接进入实现。

> **阶段内评审机制**：每个 SDA 阶段完成后，必须调用 sda-code-reviewer 对该阶段的产出进行评审。评审不通过则修复后重新评审，最多 5 轮。5 轮后仍有问题则暂停等待人工决策。通过后才进入下一阶段。

按顺序调度以下阶段：

| 序号 | 阶段 | SDA | 阶段内评审 | 输入 | 对应 tasks.md 阶段 |
|------|------|-------|-----------|------|-------------------|
| 1 | 数据库实现 | sda-db-implementer | sda-code-reviewer 评审 DB 产出 | design.md（Schema + 文件产出清单） | 阶段二：数据库 |
| 1a | DB 评审修复 | sda-db-implementer | 重新评审（最多 5 轮） | 审查报告 | — |
| 2 | 后端实现 | sda-backend | sda-code-reviewer 评审后端产出 | design.md（API + 文件产出清单） | 阶段二：后端 |
| 2a | 后端评审修复 | sda-backend | 重新评审（最多 5 轮） | 审查报告 | — |
| **2b** | **后端编译验证** | **sda-backend** | **运行 `mvn clean compile`，失败则调用 sda-build-error-resolver 修复** | **后端代码** | **—** |
| 3 | 前端实现 | sda-frontend | sda-code-reviewer 评审前端产出 | design.md（API + 文件产出清单） | 阶段三：前端 |
| 3a | 前端评审修复 | sda-frontend | 重新评审（最多 5 轮） | 审查报告 | — |
| **3b** | **前端编译验证** | **sda-frontend** | **运行 `yarn build:prod`，失败则调用 sda-build-error-resolver 修复** | **前端代码** | **—** |
| 4 | 测试执行 | sda-tester | sda-code-reviewer 评审测试代码 | test-cases.md、design.md（文件产出清单） | 阶段四：测试执行 |
| 4a | 测试评审修复 | sda-tester | 重新评审（最多 5 轮） | 审查报告 | — |
| 5 | 全量代码审查 | sda-code-reviewer | — | design.md（通过第 11 节自发现所有代码文件） | 阶段五：审查 |
| 6 | 提交 Git | 主 CC | — | 审查通过 | 阶段六：提交 Git |

> **SDA 说明**：
> - **独立配置 SDA**：sda-db-implementer / sda-backend / sda-frontend / sda-tester / sda-code-reviewer 有独立配置文件（见 `.claude/agents/` 目录）
> - **修复机制**：评审不通过时，重新调度产出该代码的 SDA（附加审查报告上下文）进行修复，无需单独的 fixer 角色

### 第三阶段：全量审查问题修复

1. 汇总阶段 5 全量审查报告，按 P0/P1/P2 分类
2. 按问题归属重新调度对应 SDA 修复（DB 问题→sda-db-implementer，后端问题→sda-backend，前端问题→sda-frontend，测试问题→sda-tester）
3. 修复后重新运行测试
4. 重新提交 sda-code-reviewer 审查（最多 5 轮）

### 第四阶段：质量门禁验证

运行质量门禁清单（见 `.claude/rules/governance.md`），全部通过才交付。

## 数据库查询工具

> sda-db-implementer 和 sda-code-reviewer 可使用 `python .claude/tools/db-query.py --query "SQL" --format table` 验证数据库状态（连接信息自动从 secrets.json 读取）。详见 `.claude/skills/sds-dbquery/SKILL.md`。

## SDA 配置索引

### 独立配置 SDA

| SDA | 配置文件 | 职责 |
|-------|---------|------|
| sda-architect | .claude/agents/sda-architect.md | 输出 Schema + API 文档 + 设计决策（Spec 阶段使用） |
| sda-doc-reviewer | .claude/agents/sda-doc-reviewer.md | Spec 文档评审（Spec 阶段使用） |
| sda-db-implementer | .claude/agents/sda-db-implementer.md | 创建数据库表、DO 实体类、Mapper 接口 |
| sda-backend | .claude/agents/sda-backend.md | 创建 VO、Service、Controller |
| sda-frontend | .claude/agents/sda-frontend.md | 创建 API 定义、页面、组件 |
| sda-tester | .claude/agents/sda-tester.md | 编写/修复 E2E 测试 |
| sda-code-reviewer | .claude/agents/sda-code-reviewer.md | 审查质量/安全/可维护性（含覆盖率审计） |
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

`/sds-dev` Skill 执行时，主 CC 按以下流程自动调度 SDA，每个阶段完成后自动进入下一阶段，无需人工干预：

```
读取 Spec → 检查 E2E 框架 → 调度 sda-db-implementer → 评审 → [sda-db-implementer 修复→重审]×5 → 调度 sda-backend → 评审 → [sda-backend 修复→重审]×5 → **后端编译验证（mvn clean compile，失败调用 sda-build-error-resolver）** → 调度 sda-frontend → 评审 → [sda-frontend 修复→重审]×5 → **前端编译验证（yarn build:prod，失败调用 sda-build-error-resolver）** → 调度 sda-tester → 评审 → [sda-tester 修复→重审]×5 → 全量审查 → 按归属调度 SDA 修复 → [重审]×5 → 质量门禁
```

### 完整调度 Prompt 模板

以下为每个阶段的完整调度 prompt，主 CC 按顺序逐个执行：

#### 阶段 1：sda-db-implementer 调度

```
你现在是 sda-db-implementer（配置文件：.claude/agents/sda-db-implementer.md）。

任务：根据设计文档创建数据库结构

输入：
- 设计文档：{SPEC_DIR}/design.md
- 数据库设计章节：第 2 节
- 文件产出清单：design.md 第 11 节

输出：
- SQL 脚本：创建数据库表（含 SET NAMES utf8mb4 + -- DB_TYPE: MySQL 8.0）
- 回滚脚本：幂等回滚 SQL
- DO 实体类：对应数据库表的实体
- Mapper 接口：MyBatis Mapper

约束：
- 写文件规则：见 rules/governance.md 和对应 SDA 配置文件
- SQL 脚本开头添加 SET NAMES utf8mb4;（规范见 CLAUDE.md 数据库规范节）
- 参考 .claude/agents/sda-db-implementer.md 中的规范约束执行

完成后：列出所有已创建的文件路径。对照 design.md 第 11 节"数据库层"产出清单，确认路径一致。如有偏差在报告中说明。
```

**阶段内评审**：调用 sda-code-reviewer 评审 sda-db-implementer 产出
- 审查范围：SQL 脚本、DO 实体类、Mapper 接口
- 审查维度：表结构完整性（对照 design.md）、字段类型正确性、索引合理性、命名规范
- 评审通过条件：P0 问题数量 = 0
- 如有问题：重新调度 sda-db-implementer 修复（**评审结果必须按 governance.md 评审结果传递机制完整传递，不得省略问题清单**） → 重新评审（最多 5 轮）
- 每轮记录：当前第 X 轮评审，已解决 Y 个问题，遗留 Z 个问题
- 通过后继续

#### 阶段 2：sda-backend 调度

```
你现在是 sda-backend（配置文件：.claude/agents/sda-backend.md）。

任务：根据设计文档实现后端 API

输入：
- 设计文档：{SPEC_DIR}/design.md
- API 设计章节：第 3 节
- 文件产出清单：design.md 第 11 节
- 测试用例文档：{SPEC_DIR}/test-cases.md

前置发现（必须执行）：
1. 读取 design.md 第 11 节，提取"数据库层"产出清单中的 DO/Mapper 文件路径
2. 对清单中的每个路径，使用 Glob 验证文件是否存在于磁盘
3. 读取已存在的 DO/Mapper 文件，了解字段定义和方法签名
4. 如有文件缺失：在产出报告中标注，但仍基于 design.md 定义实现
   如 Glob 在预期路径未找到文件，使用更宽泛模式（如 **/*XxxDO.java）搜索实际位置

输出：
- VO 类（Req/Resp/Page）
- Service 接口和实现
- Controller

约束：
- 写文件规则：见 rules/governance.md 和对应 SDA 配置文件
- Service 层返回空集合而非 null（nil 集合兜底）
- 使用 @Valid 校验参数
- 权限注解必须与前端路由守卫同步
- 使用 @PreAuthorize("@ss.hasPermission('xxx')") 而非 hasRole()
- 使用 VO 接收参数，禁止直接绑定 DO
- 写操作校验直属关系（IDOR 防护）
- 参考 .claude/agents/sda-backend.md 中的规范约束执行

完成后：列出所有已创建的文件路径和 API 端点路径。对照 design.md 第 11 节"后端层"产出清单，确认路径一致。如有偏差在报告中说明。
```

**阶段内评审**：调用 sda-code-reviewer 评审 sda-backend 产出
- 审查范围：VO 类、Service 接口和实现、Controller
- 审查维度：API 完整性（对照 design.md）、参数校验、权限注解、null 返回路径、错误处理
- 评审通过条件：P0 问题数量 = 0
- 如有问题：重新调度 sda-backend 修复（**评审结果必须按 governance.md 评审结果传递机制完整传递，不得省略问题清单**） → 重新评审（最多 5 轮）
- 每轮记录：当前第 X 轮评审，已解决 Y 个问题，遗留 Z 个问题
- 通过后继续

**后端编译验证**（评审通过后执行）：
- 运行 `mvn clean compile` 验证 Java 代码可编译
- 如编译失败：调用 sda-build-error-resolver 诊断并修复错误
- 修复后重新编译验证，通过后才进入下一阶段

#### 阶段 3：sda-frontend 调度

```
你现在是 sda-frontend（配置文件：.claude/agents/sda-frontend.md）。

任务：根据设计文档实现前端页面

输入：
- 设计文档：{SPEC_DIR}/design.md
- API 设计章节：第 3 节
- 文件产出清单：design.md 第 11 节
- 原型 HTML：（如有提供）

前置发现（必须执行）：
1. 读取 design.md 第 11 节，提取"后端层"产出清单中的 Controller 文件路径
2. 对清单中的每个 Controller 路径，使用 Glob 验证文件是否存在于磁盘
3. 读取已存在的 Controller 文件，提取实际 API 端点路径和方法签名
4. 如有 Controller 文件缺失：以 design.md 第 3 节 API 定义为准，在报告中标注
   如 Glob 在预期路径未找到文件，使用更宽泛模式（如 **/*XxxController.java）搜索
5. 读取 design.md 第 11 节"数据库层"的 DO 文件路径（如需了解字段名用于表单字段映射）

输出：
- API 定义文件（api/xxx.js）
- 列表页面
- 表单弹窗
- 菜单配置 SQL（一级 path 以 `/` 开头）

约束：
- 写文件规则：见 rules/governance.md 和对应 SDA 配置文件
- API 返回值一律加空值守卫（?? []）
- 权限指令 v-hasPermi 与后端 @PreAuthorize 必须同步
- 参考 .claude/agents/sda-frontend.md 中的规范约束执行

完成后：列出所有已创建的文件路径。对照 design.md 第 11 节"前端层"产出清单，确认路径一致。如有偏差在报告中说明。
```

**阶段内评审**：调用 sda-code-reviewer 评审 sda-frontend 产出
- 审查范围：API 定义文件、列表页面、表单弹窗
- 审查维度：空值守卫（?? []）、权限指令与后端同步、placeholder 残留、UI 交互完整性
- 评审通过条件：P0 问题数量 = 0
- 如有问题：重新调度 sda-frontend 修复（**评审结果必须按 governance.md 评审结果传递机制完整传递，不得省略问题清单**） → 重新评审（最多 5 轮）
- 每轮记录：当前第 X 轮评审，已解决 Y 个问题，遗留 Z 个问题
- 通过后继续

**前端编译验证**（评审通过后执行）：
- 运行 `yarn build:prod` 验证前端代码可编译
- 如编译失败：调用 sda-build-error-resolver 诊断并修复错误
- 修复后重新编译验证，通过后才进入下一阶段

#### 阶段 4：sda-tester 调度

```
你现在是 sda-tester（配置文件：.claude/agents/sda-tester.md）。

任务：基于测试用例文档编写和执行测试

输入：
- 测试用例文档：{SPEC_DIR}/test-cases.md
- 任务清单：{SPEC_DIR}/tasks.md（阶段四的测试任务）
- 设计文档：{SPEC_DIR}/design.md（用于发现被测代码路径）

前置发现（必须执行）：
1. 读取 design.md 第 11 节，提取所有层（数据库/后端/前端）的产出文件路径
2. 对前端层产出清单中的每个页面路径，使用 Glob 验证文件是否存在于磁盘
3. 对后端层产出清单中的每个 Controller 路径，使用 Glob 验证，提取实际 API 端点
4. 如有文件缺失：跳过依赖该文件的测试用例，标记为"前置文件缺失，待补充"

输出：
- 单元测试代码（基于 test-cases.md 中的 UT 用例）
- E2E 测试代码（基于 test-cases.md 中的 E2E 用例，如 E2E 框架已配置）
- 测试执行结果

约束：
- 写文件规则：见 rules/governance.md 和对应 SDA 配置文件
- E2E 测试必须包含三层验证：页面可达、数据加载、数据渲染非空
- 全局错误监听：pageerror + console.error + 微任务等待
- 测试数据覆盖关键角色组合（超级管理员、普通用户、无权限用户）
- 如项目未配置 E2E 测试框架，跳过 E2E 测试代码编写，仅编写单元测试
- 参考 .claude/agents/sda-tester.md 中的规范约束执行

完成后：输出测试报告（通过/失败数量），如有失败列出失败用例。在报告中包含前置发现结果：哪些预期文件存在、哪些缺失。
```

**阶段内评审**：调用 sda-code-reviewer 评审 sda-tester 产出
- 审查范围：单元测试代码、E2E 测试代码
- 审查维度：测试覆盖率（对照 test-cases.md）、断言有效性、测试数据合理性、三层验证完整性
- 评审通过条件：P0 问题数量 = 0
- 如有问题：重新调度 sda-tester 修复（**评审结果必须按 governance.md 评审结果传递机制完整传递，不得省略问题清单**） → 重新评审（最多 5 轮）
- 每轮记录：当前第 X 轮评审，已解决 Y 个问题，遗留 Z 个问题
- 通过后继续

#### 阶段 5：sda-code-reviewer 全量审查调度

```
你现在是 sda-code-reviewer（配置文件：.claude/agents/sda-code-reviewer.md）。

前置：所有 SDA 阶段已完成，且各阶段内评审已通过。

任务：对本次功能开发的所有代码变更进行全量审查（跨阶段交叉检查）

输入：
- 需求文档：{SPEC_DIR}/requirements.md
- 设计文档：{SPEC_DIR}/design.md

前置发现（必须执行）：
1. 读取 design.md 第 11 节，提取所有层的预期产出文件路径
2. 对每个预期路径，使用 Glob 验证文件是否存在于磁盘
3. 汇总实际存在的文件列表作为审查范围
4. 如有预期文件缺失：在审查报告中标注，评估对交叉一致性检查的影响

审查维度（5 项 + 交叉检查）：
1. 质量：逻辑正确性、边界情况、错误处理
2. 安全：SQL 注入/XSS/敏感信息/权限（对照 rules/security.md 🔴 级别规则）
3. 可维护性：命名、函数长度、重复代码
4. 性能：不必要的循环/N+1/缓存
5. 测试覆盖：新增代码是否有测试、覆盖率
6. 交叉一致性：前后端 API 参数/路径是否对齐、数据库字段与 DO 实体是否一致、前后端权限是否同步

额外检查项（对照 rules/security.md + rules/frontend.md）：
- nil 返回路径检查：后端 API 是否可能返回 null 集合（security.md 🔴8）
- 裸赋值检查：前端是否直接赋值 API 返回值（frontend.md 🔴3）
- 前后端权限一致性：前端路由守卫与后端 API 权限是否同步（security.md 🟡1-3）
- placeholder 残留：TODO、FIXME、硬编码假数据（frontend.md 🔴6-7）
- 一级菜单 path 以 `/` 开头（frontend.md 🔴8）

输出：按 P0/P1/P2 分类的问题清单

参考 .claude/agents/sda-code-reviewer.md 中的规范约束执行。
```

#### 阶段 6：问题修复（如全量审查有问题）

按问题归属重新调度对应 SDA 修复（与阶段内评审修复机制一致，**评审结果必须按 governance.md 评审结果传递机制完整传递，不得省略问题清单**）：

```
你是 {sda-db-implementer / sda-backend / sda-frontend / sda-tester}（配置文件：.claude/agents/{对应配置文件}）。

前置：sda-code-reviewer 第 {N} 轮全量审查发现以下问题需要修复。

【评审问题清单】
| 文件 | 行号 | 级别 | 问题描述 | 修复建议 |
|------|------|------|----------|----------|
| src/xxx.java | 45 | P0 | 缺少权限注解 | 添加 @PreAuthorize("@ss.hasPermi('xxx:list')") |

前置发现（必须执行）：
1. 读取上述问题文件，定位问题位置
2. 读取 design.md 第 11 节，确认该文件属于哪一层产出
3. 如文件路径与 design.md 不一致，在修复报告中标注

任务：修复评审发现的问题

约束：
- 一次只修一个问题，修完验证
- 修复后不影响其他功能
- 参考 .claude/agents/{对应配置文件} 中的规范约束执行
- 禁止引入新问题

完成后：列出修复的具体内容和文件变更。

当前进度：第 {N} 轮全量审查修复，已解决 Y 个问题，遗留 Z 个问题。
达到 5 轮上限后仍有 P0/P1 问题，暂停等待人工决策。
```

#### 阶段 7：质量门禁 + Git 提交

```
所有代码已通过审查，执行质量门禁检查（见 .claude/rules/governance.md）：

P0 检查（阻断交付）：
1. 后端编译：mvn clean compile
2. 前端构建：yarn install && yarn build:prod
3. 后端单元测试：mvn test
4. 敏感信息扫描：python .claude/tools/secrets-sync.py --scan-configs
5. 代码残留检查：grep -rE "TODO|FIXME|placeholder" src/
6. 数据字段 nil 兜底：后端 + 前端防御性消费
7. 前后端 API 对接完整性
8. 权限校验生效

P1 检查（记录排期）：
9. 测试覆盖率
10. E2E 测试（如已配置）
11. 页面零 404
12. API 零 500
13. 测试用例与需求对应

P2 检查（建议修复）：
14. 数据库迁移脚本可重复执行
15. 服务可达性验证

全部通过后提交 Git，提交信息遵循 .claude/rules/governance.md 的 Git Commit 规范：
type(scope): subject

Body 包含本次变更的文件说明和 review 重点。
```

## 注意事项

1. **每个 SDA 的 prompt 必须自包含且去依赖**：看不到对话历史，需要完整上下文。所有 SDA 仅接收 Spec 文档路径作为输入，不接收前序 SDA 的运行时输出。每个 SDA 通过读取 design.md 第 11 节自行发现前序产出文件路径，再用 Glob/Read 验证和读取实际文件。design.md 第 11 节是 SDA 间文件路径对齐的唯一契约。
2. **写文件规则**：参考对应 SDA 配置文件中的规范约束（见 rules/governance.md）
3. **全新代码也要审查**：AI 生成的代码存在权限缺失、校验遗漏等问题
4. **测试用例文档先行**：test-cases.md 在 Spec 阶段已创建，实现阶段参考测试用例文档编写代码
5. **阶段内评审必须执行**：每个 SDA 阶段完成后立即评审，不可跳过，不可延迟到全量审查
6. **多轮评审上限**：每个评审点最多 5 轮，5 轮后由用户决定是否继续修复或标记为已知问题
7. **评审修复分工**：评审发现问题后，重新调度产出该代码的 SDA 修复——数据库问题→sda-db-implementer，后端问题→sda-backend，前端问题→sda-frontend，测试问题→sda-tester。修复 prompt 必须附加审查报告上下文

## 进度跟踪

每个阶段完成后，主 CC 应更新 tasks.md 中的任务状态，并向用户汇报进度：

```markdown
## 开发进度

| 阶段 | 状态 | 评审结果 | 备注 |
|------|------|----------|------|
| 1. 数据库 | ✅ 已完成 | P0:0 P1:1 P2:0 | P1 已修复 |
| 2. 后端 | 🔄 进行中 | — | — |
| 3. 前端 | ⬜ 未开始 | — | — |
| 4. 测试 | ⬜ 未开始 | — | — |
| 5. 全量审查 | ⬜ 未开始 | — | — |
| 6. 质量门禁 | ⬜ 未开始 | — | — |
```

## 开发中需求变更

开发过程中如遇需求变更，按以下流程处理：

| 变更时机 | 处理方式 |
|----------|----------|
| 当前阶段内 | 完成当前阶段 → 调用 `/sds-spec` 更新 Spec → 继续后续阶段 |
| 阶段切换时 | 暂停 → 调用 `/sds-spec` 更新 Spec → 评估已实现代码影响 → 继续或回滚 |
| 全量审查后 | 评估变更范围 → 小变更直接修复 → 大变更调用 `/sds-spec` 更新 Spec |

### 变更处理原则

- **不中断当前阶段**：当前 SDA 正在执行时不暂停，完成后再处理变更
- **先更新 Spec 再改代码**：确保变更可追溯
- **评估已实现代码影响**：变更可能影响已完成的阶段，需评估是否回滚
- **通知用户确认**：变更影响超过当前阶段时，需用户确认处理方案