---
name: sdc-buildfix
description: 构建和测试错误的自动诊断与修复（调用 sda-build-error-resolver）
---

# /sdc-buildfix 命令规范

## 触发场景

- 项目编译失败（`mvn compile` / `yarn build`）
- 测试失败（`mvn test` / `yarn test`）
- CI/CD 构建错误
- 本地启动异常（SpringBoot / Node 服务启动失败）
- 依赖下载失败或版本冲突

## 执行方式

`/sdc-buildfix` 是对 `sda-build-error-resolver` agent 的包装命令。

执行时，主 CC 直接调用 `sda-build-error-resolver` agent 进行诊断和修复。

## 前置条件

调用前，主 CC 应先收集以下信息：

| 信息 | 获取方式 | 必需 |
|------|----------|------|
| 失败的命令 | 询问用户或从上下文获取 | 是 |
| 完整错误输出 | 执行相同命令获取 | 是 |
| 环境信息 | JDK 版本、Node 版本、操作系统 | 否 |
| 最近代码变更 | `git diff --name-only` | 否 |

## 工作流程

```
收集错误上下文 → 调用 sda-build-error-resolver → 诊断根因 → 修复 → 验证 → 经验沉淀
```

### 详细步骤

1. **主 CC 接收 `/sdc-buildfix` 命令**
2. **收集错误上下文**
   - 失败的命令（如 `mvn clean compile`）
   - 完整错误输出（重新执行命令获取）
   - 相关文件路径（从错误信息中提取）
3. **调用 `sda-build-error-resolver` agent**
   - 传递错误上下文
   - agent 执行诊断和修复
4. **验证修复结果**
   - 执行相同命令确认修复成功
   - 如失败，重复步骤 3（最多 3 轮）
5. **经验沉淀**
   - 由 `sda-build-error-resolver` 自动追加到 `.claude/skills/troubleshooting.md`

## 多错误处理

当同时存在多个错误时：

1. 按优先级排序：P0（阻塞构建）> P1（测试失败）> P2（警告）
2. 按依赖关系排序：先修复被依赖的模块
3. 每修复一个错误后验证，避免引入新问题
4. 最多 3 轮修复，超过则交由用户决定

## 修复后验证

修复完成后，主 CC 必须执行以下验证：

| 验证项 | 命令 | 说明 |
|--------|------|------|
| 后端编译 | `mvn clean compile` | 确认 Java 代码可编译 |
| 前端编译 | `yarn build` | 确认前端代码可构建 |
| 测试执行 | `mvn test` / `yarn test` | 确认测试通过 |

## 输出

直接输出 `sda-build-error-resolver` 的 `## Build Fix Report` 格式：

```markdown
## Build Fix Report

### 错误类型
[编译/测试/类型检查/CI]

### 错误优先级
[P0/P1/P2/P3]

### 根因分析
[一句话描述根本原因]

### 错误位置
- 文件：[文件路径]
- 行号：[行号]

### 修复方案
1. [步骤]
2. [步骤]

### 验证结果
- 命令：[验证命令]
- 结果：[PASS/FAIL]

### Commit 建议
fix(module): [简短描述]

### 经验沉淀
[是否已追加到 troubleshooting.md]
```

## 注意事项

- 修复时遵循最小改动原则，避免引入新问题
- 一次只修一个问题，修完验证后再修下一个
- 安全问题不在此命令范围内，需人工确认
- 如 3 轮修复仍失败，输出当前状态交由用户决定
