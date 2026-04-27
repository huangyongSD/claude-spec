---
inclusion: fileMatch
fileMatchPattern: ["src/components/**", "src/ui/**"]
---

# 前端开发规范

> 本文件在编辑前端组件文件时加载。
> 根据实际项目调整 fileMatchPattern。

## 组件设计原则

- 单一职责：每个组件只做一件事
- 受控/非受控明确：优先使用受控组件
- Props 类型完整：必须定义 TypeScript 类型，禁止 any

## 状态管理

- 局部状态：组件内部用 `ref` / `reactive`
- 全局状态：跨组件共享用 Pinia / Vuex
- 避免过度提升：不是所有状态都需要提升到父组件

## 样式规范

- 优先使用 CSS Modules / Scoped CSS
- 遵循设计系统的间距、颜色、字体规范
- 响应式设计：移动端优先

## 性能优化

- 列表渲染使用唯一 key
- 大列表虚拟滚动
- 懒加载非首屏组件
- 避免不必要的 re-render

## 无障碍（a11y）

- 语义化标签
- 键盘可访问
- ARIA 属性正确使用
