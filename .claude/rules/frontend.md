---
description: 前端编码底线规则
type: rules
updated: 2026-04-22
---

# 前端编码底线规则

## 🔴 立即执行（违反即阻断）

### 防御性数据消费
1. **API 返回值一律加空值守卫** — `data ?? []`
2. **链式访问加可选链** — `row.nested?.field ?? defaultValue`
3. **禁止裸赋值** — `this.list = response.data` → `this.list = response.data ?? []`
4. **数值方法调用加守卫** — `(value ?? 0).toFixed(1)`

### 代码质量
5. **禁止提交 placeholder/TODO/FIXME/{{PLACEHOLDER}}/硬编码假数据** — 质量门禁 `grep -r "TODO\|FIXME\|placeholder" src/` 检查代码文件 + `grep -rE "{{[A-Z][A-Z_]+}}" .claude/` 检查配置文件占位符（注意：grep 范围不含规范手册文件本身）

## 🟡 新代码执行

### 错误处理
1. API 调用必须处理错误态，不允许静默失败
2. 用户输入必须做校验和转义处理

### 代码规范
3. 组件必须有明确的 JSDoc 类型注释
4. 禁止 any 类型（除非有充分理由并添加注释说明）
5. 复杂逻辑必须拆分为可测试的函数

## 🟢 逐步达标

### 最佳实践
1. 组件拆分：单文件不超过 300 行
2. 状态管理：跨组件状态使用 Vuex（本项目为 Vue2），避免 prop drilling
3. 样式规范：遵循项目 UI 设计规范，以原型为最终权威

## 执行方式

🔴 级别违反，代码审查时阻断。
🟡 级别在代码审查时检查，新代码不合规不合并。
🟢 级别作为团队习惯逐步养成，不强制。

## 关键洞察

> See rules/security.md "关键洞察" for nil collection and trust boundary principles.

- **原型 HTML 为最终权威**：当设计规范文档与原型不一致时，以原型为准
