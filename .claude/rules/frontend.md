---
description: 前端编码底线规则
globs: ["**/*.vue", "**/*.js", "**/*.css", "**/*.scss"]
---

# 前端编码底线规则

> 本文件定义前端编码的不可违反红线。与 security.md（安全规则）互补：
> - frontend.md = 前端编码规范（写 Vue/JS 时遵守）
> - security.md = 安全编码规则（写任何代码时遵守）
>
> 本项目技术栈：Vue2 2.6.12 + Element-UI 2.15.14 + Vuex 3.6.0 + Vue Router 3.4.9 + Webpack

## 🔴 立即执行（违反即阻断）

### 防御性数据消费

1. **API 返回值一律加空值守卫** — `data ?? []`
2. **链式访问加可选链** — `row.nested?.field ?? defaultValue`
3. **禁止裸赋值** — `this.list = response.data` → `this.list = response.data ?? []`
4. **数值方法调用加守卫** — `(value ?? 0).toFixed(1)`
5. **API 调用必须处理错误态** — 禁止静默失败，必须显示错误提示

### 代码质量

6. **禁止提交 placeholder/硬编码假数据** — 质量门禁 `grep -rE "placeholder" src/` 检查
7. **禁止提交 TODO/FIXME 残留** — 见 governance.md P0-5
8. **调试代码输出 JSON 对象必须转字符串** — `console.log(JSON.stringify(obj))` 禁止直接 `console.log(obj)`，避免对象引用或循环引用导致输出异常或性能问题

### 路由与菜单

8. **一级菜单 path 必须以 `/` 开头** — 否则 Vue Router 无法识别为根路由，页面 404
9. **菜单 component 路径与 src/views/ 文件对应** — `component: 'business/meeting-room/index'` 对应 `src/views/business/meeting-room/index.vue`
10. **操作按钮根据权限显隐** — 使用 `v-hasPermi="['xxx:add']"` 指令（若依项目自定义指令，位于 `src/directive/permission/hasPermi.js`）

## 🟡 新代码执行

### 组件设计

1. **列表页标准结构** — 搜索栏 + 操作按钮 + el-table + el-pagination
2. **表单弹窗复用新增/编辑** — 通过 `dialogStatus` 变量区分，`create` / `update` 复用同一表单
3. **组件拆分** — 单文件不超过 300 行，超过则拆分子组件
4. **全局共享状态使用 Vuex** — 用户信息、权限等全局状态使用 Vuex（本项目为 Vue2）；页面内跨组件状态优先使用 props/emits

### API 调用规范

5. **API 定义文件与后端 Controller 对齐** — `api/xxx/index.js` 的方法名与后端 API 路径一致
6. **列表赋值模式**：
   ```javascript
   this.list = response.data.list ?? []
   this.total = response.data.total ?? 0
   ```
7. **表单提交模式** — 成功后 `this.$modal.msgSuccess` + `this.getList()` 刷新列表 + `this.dialogVisible = false` 关闭弹窗

### Element-UI 规范

8. **表格列使用 `show-overflow-tooltip`** — 长文本不撑开布局
9. **表单校验使用 `el-form` 的 `rules`** — 不手动写 if-else 校验
10. **删除操作使用 `this.$modal.confirm`** — 不使用原生 `confirm()`
11. **日期选择器使用 `value-format`** — 统一格式为 `YYYY-MM-DD HH:mm:ss`

### 代码规范

12. 用户输入必须做校验和转义处理（XSS 防护见 security.md 🔴6）
13. 复杂逻辑必须拆分为可测试的函数

## 🟢 逐步达标

### 最佳实践

1. 组件必须有明确的 JSDoc 类型注释
2. 禁止隐式全局变量（未声明直接赋值的变量）
3. 样式规范：遵循项目 UI 设计规范，以原型为最终权威
4. 分页组件默认 `pageSize: 10`，上限 100

## 执行方式

🔴 级别违反，代码审查时阻断。
🟡 级别在代码审查时检查，新代码不合规不合并。
🟢 级别作为团队习惯逐步养成，不强制。

## 关键洞察

- **原型 HTML 为最终权威**：当设计规范文档与原型不一致时，以原型为准
- **一级菜单 path 以 `/` 开头是 Vue Router 的硬性要求**：不写 `/` 会被当作相对路径，页面 404 但不报错，极难排查
- **裸赋值是定时炸弹**：后端某天返回 `null`，前端 `.map()` 直接崩。`?? []` 是零成本的保险
- **Element-UI 组件内部结构复杂**：测试时不要用 `.el-table` 选择器，优先选择业务关键元素（如按钮文本）

## 变更记录

| 日期 | 变更内容 | 原因 |
|------|----------|------|
| 2026-04-28 | 🔴10 补充 v-hasPermi 指令来源说明 | 新成员/AI 不知道指令出处 |
| 2026-04-28 | 🟡4 从"跨组件状态使用VuX"改为"全局共享状态使用VuX，页面内优先props/emits" | 原规则过于绝对，导致 store 膨胀 |
| 2026-04-28 | 🟢2 从"禁止any类型"改为"禁止隐式全局变量" | 项目为 Vue2+JS，不存在 any 类型 |
