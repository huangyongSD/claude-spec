---
description: 流程治理规则（SDA 协作 + Git 工作流 + 质量门禁）
type: rules
updated: 2026-04-28
---

# 流程治理规则

> 本文件整合 SDA 协作规范、Git 工作流和质量门禁，供主 CC 和编排流程使用。
> SDA 不直接引用此文件——SDA 的安全/前端/测试规则分别在 security.md、frontend.md、testing.md 中定义。

## 🔴 立即执行（违反即阻断交付）

### 质量门禁 P0 清单（8 项，必须全绿）

| 序号 | 检查项 | 验证命令/方式 | 自动化 |
|------|--------|--------------|--------|
| 1 | 后端编译通过 | `mvn clean compile`（必须全量，非增量） | ✅ |
| 2 | 前端构建通过 | `yarn install && yarn build:prod` | ✅ |
| 3 | 后端单元测试零失败 | `mvn test` | ✅ |
| 4 | 无敏感信息泄露 | `python .claude/tools/secrets-sync.py --scan-configs` + Hook 层兜底 | ✅ |
| 5 | 代码无 TODO/FIXME/placeholder 残留 | `grep -rE "TODO\|FIXME\|placeholder" src/`（排除规范文件自身） | ✅ |
| 6 | 数据字段无 null/undefined/占位符残留 | 后端 nil 集合兜底 + 前端 `?? []` 防御性消费 + grep 抽查 | 半自动 |
| 7 | 前后端 API 对接完整性 | API 文档 vs 前端调用 vs 后端 Controller，三者一致 | 人工 |
| 8 | 权限校验生效 | 后端 @PreAuthorize 与前端路由守卫同步 + 关键角色组合测试 | 人工 |

### P0 失败处理

| 失败项 | 处理方式 | 责任人 |
|--------|---------|--------|
| 后端编译失败 | sda-build-error-resolver 修复（必须全量编译） | SDA |
| 前端构建失败 | 检查 Node 版本兼容性、依赖完整性 | 前端开发者 |
| 单元测试失败 | 对应 SDA 修复；禁止跳过测试提交 | SDA/人工 |
| 敏感信息泄露 | 立即替换为占位符，运行 secrets-sync.py 全量扫描 | SDA/人工 |
| TODO/FIXME 残留 | 清理或转为正式需求/Issue | 人工 |
| 数据字段问题 | 后端加 nil 集合兜底，前端加 `?? []` 守卫（见 security.md + frontend.md） | 前后端开发者 |
| API 对接不一致 | 三者同步更新 | 前后端开发者 |
| 权限问题 | 修复权限逻辑（见 security.md 🟡4-5） | 后端开发者 |

## 🟡 新代码执行

### SDA 协作规范

#### 串行保证正确性

SDA 编排分两个阶段，必须按依赖顺序串行执行：

**Spec 阶段**（由 `/sds-spec` 命令触发）：
```
主CC（输出 requirements.md）→ sda-doc-reviewer（评审）→ sda-architect（输出 design.md）→ sda-doc-reviewer（评审）→ sda-architect（输出 test-cases.md）→ sda-doc-reviewer（评审）→ 主CC（输出 tasks.md）→ sda-doc-reviewer（评审）
```

**实现阶段**（由 `/sds-dev` 命令触发）：
```
sda-db+sda-backend → sda-frontend → sda-tester → sda-code-reviewer
```

每一层基于上一层产出，不能跳步。

- sda-db-implementer 和 sda-backend 共用 design.md 作为唯一输入，合并为一个阶段减少上下文传递断裂点
- design.md 中的「文件产出清单」确保 agent 之间文件路径对齐
- sda-frontend 需要基于 sda-backend 的 API 和文件产出清单实现页面
- sda-tester 需要基于前端页面编写测试
- reviewer 最后审查所有代码

#### Prompt 自包含

每个 SDA 看不到对话历史，prompt 必须包含：
- 需求文档路径
- 设计决策文件路径
- 相关文件清单
- 具体改动描述

#### 写文件规则

每次写入 ≤ 200 行，大文件分模块写入。

#### SDA Team 组织

| SDA | 阶段 | 角色 | 职责 | 配置文件 |
|-------|------|------|------|---------|
| sda-architect | Spec | 架构师 | 输出 Schema + API 文档 + 设计决策 + 测试用例文档 | `.claude/agents/sda-architect.md` |
| sda-doc-reviewer | Spec | Spec 评审 | 对 Spec 文件进行结构化评审 | `.claude/agents/sda-doc-reviewer.md` |
| sda-db-implementer | 实现 | 数据库实现 | 创建数据库表、DO 实体类、Mapper 接口 | `.claude/agents/sda-db-implementer.md` |
| sda-backend | 实现 | 后端实现 | 创建 VO、Service、Controller | `.claude/agents/sda-backend.md` |
| sda-frontend | 实现 | 前端实现 | 创建 API 定义、页面、组件 | `.claude/agents/sda-frontend.md` |
| sda-tester | 实现 | 测试工程师 | 编写/修复 E2E 测试 | `.claude/agents/sda-tester.md` |
| sda-code-reviewer | 实现 | 代码审查 | 审查质量/安全/可维护性（含覆盖率审计） | `.claude/agents/sda-code-reviewer.md` |
| sda-build-error-resolver | 实现 | 构建排障 | 修复构建/测试错误 | `.claude/agents/sda-build-error-resolver.md` |

> Spec 阶段由 `/sds-spec` 调度，实现阶段由 `/sds-dev` 调度。两阶段不可交叉。

#### 修复机制

评审发现问题后，重新调度产出该代码的 SDA 进行修复：

| 问题归属 | 修复 SDA |
|----------|---------|
| 数据库层（SQL、DO、Mapper） | sda-db-implementer |
| 后端层（VO、Service、Controller） | sda-backend |
| 前端层（Vue、JS、组件） | sda-frontend |
| 测试代码 | sda-tester |

> 重新调度时在 prompt 中附加审查报告和具体问题清单。

#### 并行 vs 串行调度

**可并行**（无文件冲突）：sda-tester + sda-frontend（不同目录）、多个调查 SDA
**必须串行**（有文件依赖）：sda-backend 修复 → sda-tester 重跑

### Git 工作流规范

#### Commit 规范

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

#### Branch 规范

1. 分支命名：type/short-description（如 `feature/user-auth`、`fix/login-timeout`）
2. 🔴 **禁止在 main/master 直接提交**，所有变更走分支
3. 分支生命周期：完成即合并，合并即删除

#### Merge 策略

- 使用 **Squash and Merge** 保持历史整洁
- 或 **Rebase + Merge** 保留完整历史
- 煎制 **Fast-forward Merge**（无法追溯合并来源）

### P1 门禁清单（5 项，记录排期）

| 序号 | 检查项 | 验证命令/方式 | 自动化 |
|------|--------|--------------|--------|
| 9 | 测试覆盖率不低于基准 | 目标：核心业务逻辑 80%（当前无配置） | ❌ |
| 10 | E2E 测试零失败 | `npx playwright test`（当前未配置，见降级方案） | ✅ |
| 11 | 页面零 404 | E2E 覆盖所有页面路由（当前未配置，见降级方案） | ✅ |
| 12 | API 零 500 | E2E 监听 API 响应（当前未配置，见降级方案） | ✅ |
| 13 | 测试用例与需求对应完整 | 每个 AC 均有对应测试用例覆盖 | 人工 |

### 降级方案

**E2E 测试未配置时**（第 10-12 项降级）：
- 第 10 项降级：运行 `mvn test` 确保核心功能验证通过
- 第 11 项降级：人工遍历所有页面路由，确认无 404
- 第 12 项降级：人工测试关键 API 端点（CRUD 全覆盖），确认无 500

> 降级需在交付记录中标注原因并排期补充 E2E 测试。降级 ≠ 跳过。

**覆盖率工具未配置时**（第 9 项降级）：人工审查核心 Service 类覆盖情况，记录未覆盖路径到技术债清单。

### 执行时机

| 时机 | 执行项 |
|------|--------|
| 每次提交前 | 第 1-2、5 项 |
| 合并前 | 第 1-5 项 |
| CI/CD 自动触发 | 第 1-5、9-10 项 |
| **每次交付前** | **第 1-15 项** |

## 🟢 逐步达标

### P2 门禁清单（2 项）

| 序号 | 检查项 | 验证方式 |
|------|--------|---------|
| 14 | 数据库迁移脚本可重复执行 | SQL 幂等性验证 + db-query.py 抽查 |
| 15 | 服务可达性验证 | 后端 48080 + 前端 80 可达 |

### Git 逐步达标

1. 分支完成后及时删除
2. Commit Footer 引用 Issue：Closes #123
3. 分支合并后自动删除远程分支

### 全新代码也要审查

AI 生成的代码存在权限缺失、校验遗漏等问题，审查不可省略。

**审查清单要点**（详细维度见 sda-code-reviewer 配置）：
- nil 返回路径（见 security.md 🔴6 + frontend.md 🔴1-4）
- 裸赋值（见 frontend.md 🔴3）
- 前后端权限一致性（见 security.md 🟡4-5）
- placeholder 残留（见本文件 P0-5）

## 执行方式

🔴 级别违反，阻断交付。P0 任何一项不满足即不可交付。
🟡 级别违反，记录并排期修复，不阻断但不可忽略。
🟢 级别建议修复，记入技术债清单，不阻断交付。

## 关键洞察

- **SDA prompt 必须自包含**：看不到对话历史，prompt 中要包含需求文档路径、设计决策、文件清单、具体改动描述
- **门禁是最后一道防线**：Hooks 可能被绕过，门禁必须兜底
- **降级 ≠ 跳过**：降级必须记录原因和排期
- **全量编译不可省**：增量编译可能隐藏包路径不匹配问题

## 相关文档

- 安全规则：.claude/rules/security.md
- 前端规则：.claude/rules/frontend.md
- 测试规则：.claude/rules/testing.md