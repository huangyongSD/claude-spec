---
description: Git 工作流规范
type: rules
updated: 2026-04-22
---

# Git 工作流底线规则

## 🟡 新代码执行

### Commit 规范

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

### Branch 规范

1. 分支命名：type/short-description
   - `feature/user-auth`
   - `fix/login-timeout`
   - `chore/update-deps`
2. 禁止在 main/master 直接提交，所有变更走分支
3. 分支生命周期：完成即合并，合并即删除

### Merge 策略

- 使用 **Squash and Merge** 保持历史整洁
- 或 **Rebase + Merge** 保留完整历史（视团队习惯选择）
- 禁止 **Fast-forward Merge**（无法追溯合并来源）

## 🟢 逐步达标

1. 分支完成后及时删除
2. Commit message Footer 引用相关 Issue：Closes #123
3. 分支合并后自动删除远程分支

## 执行方式

🟡 级别在代码审查中检查。
🟢 级别作为团队习惯逐步养成，不强制。
