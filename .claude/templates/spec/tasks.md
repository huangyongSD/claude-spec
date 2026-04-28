# 任务清单：{功能名称}

> 创建时间：{日期}
> 最后更新：{日期}
> 对应需求：`.claude/specs/<feature>/requirements.md`
> 对应设计：`.claude/specs/<feature>/design.md`
> 对应测试：`.claude/specs/<feature>/test-cases.md`

## 任务状态说明

- ⬜ 未开始
- 🔄 进行中
- ✅ 已完成
- ❌ 已阻塞（需说明原因）

## AC→任务 追溯矩阵

> **必填项**。确保 requirements.md 中的每个 AC 都有实现任务覆盖。
> 评审时逐行检查：每个 AC 必须至少有一个实现任务 + 一个测试任务。

| AC 编号 | AC 描述 | 实现任务 | 测试任务 | design.md 章节 | 覆盖状态 |
|---------|---------|---------|---------|---------------|---------|
| AC-001 | {条件1} | T-001~T-006, T-007~T-009 | T-UT-001, T-E2E-003 | §3.2 + §5.1 | ⬜ |
| AC-002 | {条件2} | T-005 | T-UT-002, T-E2E-005 | §3.2 异常场景 | ⬜ |
| AC-003 | {条件3} | T-005, T-006 | T-E2E-009~T-E2E-012 | §4.1 + §4.2 | ⬜ |
| AC-004 | {条件4} | T-008 | T-E2E-008 | §5.1 | ⬜ |
| AC-005 | {条件5} | — | 人工验证 | §6 | ⬜ |

> **覆盖规则**：
> - 每个 AC 必须有实现任务（标注"人工验证"的性能类 AC 除外）
> - 每个 AC 必须有测试任务（与 test-cases.md 追溯矩阵一致）
> - 实现任务和测试任务的 AC 引用必须与 design.md 追溯矩阵对齐

## 任务列表

### 阶段一：测试用例文档（测试用例文档先行，预计 {N} 小时）

> **测试用例文档先行**：基于 requirements.md 中的 AC，补充 test-cases.md 测试用例文档。注意：这是编写测试用例文档（描述预期行为），而非编写测试代码。

| 任务ID | 任务描述 | 对应 AC | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|---------|----------|------|------|------|
| T-DOC-001 | 补充功能类 AC 对应的测试用例到 test-cases.md | AC-001 | sda-tester | ⬜ | 0.5h | |
| T-DOC-002 | 补充数据类 AC 对应的测试用例到 test-cases.md | AC-002 | sda-tester | ⬜ | 0.5h | |
| T-DOC-003 | 补充权限类 AC 对应的测试用例到 test-cases.md | AC-003 | sda-tester | ⬜ | 0.5h | |
| T-DOC-004 | 补充交互类 AC 对应的测试用例到 test-cases.md | AC-004 | sda-tester | ⬜ | 0.5h | |
| T-DOC-005 | 补充边界情况和防御性测试用例到 test-cases.md | AC-001~004 | sda-tester | ⬜ | 0.5h | |
| T-DOC-006 | 完善 AC 覆盖追溯矩阵，确保每个 AC 有测试覆盖 | ALL | sda-tester | ⬜ | 0.5h | |

### 阶段二：数据库 + 后端（合并调度，预计 {N} 小时）

> sda-db-implementer 和 sda-backend 共用 design.md 作为输入，合并为一个阶段减少上下文传递断裂。sda-backend 在 sda-db-implementer 产出（DO/Mapper）之上直接构建。

| 任务ID | 任务描述 | 对应 AC | 产出文件（来自 design.md 文件产出清单） | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|---------|--------------------------------------|----------|------|------|------|
| T-001 | 创建数据库表 SQL 脚本（含字符集声明 + 回滚脚本） | AC-001 | sql/{TABLE}.sql + sql/{TABLE}_rollback.sql | sda-db-implementer | ⬜ | 0.5h | |
| T-002 | 创建 DO 实体类 | AC-001 | {entity_package}/{ClassName}DO.java | sda-db-implementer | ⬜ | 0.5h | |
| T-003 | 创建 Mapper 接口 | AC-001 | {mapper_package}/{ClassName}Mapper.java | sda-db-implementer | ⬜ | 0.5h | |
| T-004 | 创建 VO 类（SaveReqVO / PageReqVO / RespVO） | AC-001 | {vo_package}/{ClassName}*.java | sda-backend | ⬜ | 1h | |
| T-005 | 创建 Service 接口和实现（含业务规则校验 + nil 集合兜底） | AC-001~003 | {service_package}/{ClassName}Service*.java | sda-backend | ⬜ | 2h | |
| T-006 | 创建 Controller（含权限注解 + VO 接收参数） | AC-001, AC-003 | {controller_package}/{ClassName}Controller.java | sda-backend | ⬜ | 1h | |

> **安全检查点**（sda-backend 完成后自检）：
> - Controller 是否使用 `@PreAuthorize("@ss.hasPermission('xxx')")` 而非 `hasRole()`
> - Controller 是否使用 VO 接收参数，而非直接绑定 DO
> - Service 写操作是否校验直属关系（IDOR 防护）
> - 返回集合的 API 是否兜底 `[]`（nil 集合兜底）

### 阶段三：前端（预计 {N} 小时）

| 任务ID | 任务描述 | 对应 AC | 产出文件（来自 design.md 文件产出清单） | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|---------|--------------------------------------|----------|------|------|------|
| T-007 | 创建 API 定义文件 | AC-001 | api/xxx/index.js | sda-frontend | ⬜ | 0.5h | |
| T-008 | 创建列表页面（含防御性数据消费 + 筛选交互） | AC-001, AC-004 | views/xxx/index.vue | sda-frontend | ⬜ | 2h | |
| T-009 | 创建表单弹窗 | AC-001 | views/xxx/XxxForm.vue | sda-frontend | ⬜ | 1h | |
| T-010 | 创建菜单配置 SQL（一级 path 以 `/` 开头） | AC-001 | sql/{MODULE}_menu.sql | sda-frontend | ⬜ | 0.5h | |

> **前端检查点**（sda-frontend 完成后自检）：
> - 列表赋值是否使用 `this.list = response.data.list ?? []`（禁止裸赋值）
> - 嵌套字段是否使用 `row.field?.subField ?? defaultValue`（可选链 + 默认值）
> - API 调用是否处理错误态（禁止静默失败）
> - 操作按钮是否根据权限显隐（`v-hasPermi`）
> - 菜单 SQL 一级菜单 path 是否以 `/` 开头

### 阶段四：测试执行（全部实现完成后统一执行，预计 {N} 小时）

> **测试用例文档先行**：测试用例文档（test-cases.md）在阶段一完成，测试代码（T-UT-xxx / T-E2E-xxx）在本阶段编写并执行。**此阶段在阶段二~三全部完成后执行**。

| 任务ID | 任务描述 | 对应 AC | 对应测试用例 | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|---------|------------|----------|------|------|------|
| T-UT-001 | 编写单元测试代码-功能类 | AC-001 | UT-001~UT-003 | sda-tester | ⬜ | 0.5h | |
| T-UT-002 | 编写单元测试代码-数据校验 | AC-002 | UT-002 | sda-tester | ⬜ | 0.5h | |
| T-UT-003 | 编写单元测试代码-权限校验 | AC-003 | UT-004 | sda-tester | ⬜ | 0.5h | |
| T-UT-101 | 运行后端单元测试，确保全部通过 | ALL | ALL UT | sda-tester | ⬜ | 0.5h | |
| T-E2E-001 | 编写 E2E 测试代码-冒烟+功能 | AC-001, AC-004 | E2E-001~E2E-008 | sda-tester | ⬜ | 1h | |
| T-E2E-002 | 编写 E2E 测试代码-权限+IDOR | AC-003 | E2E-009~E2E-012 | sda-tester | ⬜ | 1h | |
| T-E2E-101 | 运行 E2E 测试，确保全部通过 | ALL | ALL E2E | sda-tester | ⬜ | 0.5h | |

> **E2E 降级方案**：如项目未配置 Playwright，T-E2E-001/002/101 降级为人工验收，在"覆盖方式"列标注"人工验证"。

### 阶段五：编译验证（预计 {N} 小时）

> 对应 workflow.md Step 7。编译验证是质量门禁的前置条件。

| 任务ID | 任务描述 | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|----------|------|------|------|
| T-BUILD-001 | 后端全量编译 `mvn clean compile` | 主CC | ⬜ | 0.5h | |
| T-BUILD-002 | 前端生产构建 `yarn install && yarn build:prod` | 主CC | ⬜ | 0.5h | |
| T-BUILD-003 | 修复编译/构建错误（如有） | sda-build-error-resolver | ⬜ | 1h | |

### 阶段六：审查与质量门禁（预计 {N} 小时）

| 任务ID | 任务描述 | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|----------|------|------|------|
| T-011 | 代码审查（安全/权限/防御性消费/nil 兜底） | sda-code-reviewer | ⬜ | 1h | |
| T-012 | 修复审查问题 | 对应 SDA | ⬜ | 1h | |
| T-013 | 质量门禁检查（见 governance.md） | 主CC | ⬜ | 0.5h | |
| T-014 | 敏感信息扫描 `secrets-sync.py --scan-configs` | 主CC | ⬜ | 0.5h | |
| T-015 | 代码残留检查 `grep -rE "TODO|FIXME|placeholder" src/` | 主CC | ⬜ | 0.5h | |

### 阶段七：提交 Git（预计 0.5 小时）

| 任务ID | 任务描述 | 负责角色 | 状态 | 预计 | 实际 |
|--------|----------|----------|------|------|------|
| T-016 | 提交代码（遵循 git.md Commit 规范） | 主CC | ⬜ | 0.5h | |

## 任务依赖关系

```
【阶段一：测试用例文档】
T-DOC-001 ─┐
T-DOC-002 ─┤──→ T-DOC-005 ──→ T-DOC-006 ──→ test-cases.md 完成
T-DOC-003 ─┘
T-DOC-004 ─┘

【阶段二：数据库 + 后端（合并）】
T-001 ──→ T-002 ──→ T-003 ──→ T-005 ──→ T-006
          │                   ↑
          └───→ T-004 ────────┘

【阶段三：前端】
T-007 ──→ T-008 ──→ T-009
                      │
          T-010 ──────┘（菜单 SQL 可并行）

【阶段四：测试执行（阶段二~三完成后）】
T-UT-001 ─┐
T-UT-002 ─┤──→ T-UT-101 ─┐
T-UT-003 ─┘               │
                           ├──→ T-E2E-101
T-E2E-001 ─┐              │
T-E2E-002 ─┘──→ T-E2E-101─┘

【阶段五：编译验证（阶段四完成后）】
T-BUILD-001 ─┐──→ T-BUILD-003（如有错误）──→ 重新编译
T-BUILD-002 ─┘

【阶段六：审查与质量门禁（编译通过后）】
T-011 ──→ T-012 ──→ T-013 ──→ T-014 ──→ T-015

【阶段七：提交 Git（门禁通过后）】
T-016 ──→ ✅ 交付
```

## 测试用例文档先行开发原则

1. **测试用例文档先行**：基于 requirements.md 补充 test-cases.md，明确每个 AC 对应的测试用例（注意：这是编写测试用例文档，不是编写测试代码）
2. **实现代码**：基于 design.md 和 test-cases.md 实现功能代码
3. **测试代码编写**：基于 test-cases.md 编写测试代码（T-UT-xxx、T-E2E-xxx）
4. **统一测试执行**：**全部实现完成后**执行 T-UT-101（单元测试）和 T-E2E-101（E2E 测试），全部通过才进入编译验证阶段

## 总计

- **预计总工时**：{N} 小时（含测试用例文档 + 测试代码编写）
- **实际总工时**：{N} 小时
- **任务总数**：{N} 个（含 {M} 个测试相关任务）
- **已完成**：{N} 个
- **进度**：{N}%
- **AC 覆盖**：{N}/{M} 个 AC 有实现任务覆盖

## 阻塞问题记录

| 日期 | 任务ID | 问题描述 | 解决方案 | 解决日期 |
|------|--------|----------|----------|----------|
| {日期} | {任务ID} | {问题} | {方案} | {日期} |

## 变更记录

| 日期 | 变更内容 | 影响范围 | 原因 |
|------|----------|----------|------|
| {日期} | {变更描述} | {受影响的任务ID} | {原因} |
