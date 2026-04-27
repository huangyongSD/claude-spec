# NEVER 列表 — 禁止行为

> 本文件列出 AI 必须严格避免的行为，不需要解释原因。
> 违反这些规则会直接阻断操作。

## 绝对禁止

- **禁止修改** `{{CORE_DIR}}/` 下的文件（需通过专用工具或人工介入）
- **禁止硬编码** 密钥、Token、数据库凭证（必须通过环境变量注入）
- **禁止提交** `.env`、`{{CONFIG_FILE}}` 到 Git
- **禁止使用** `any` 类型（必须使用具体类型或 `unknown`）
- **禁止绕过** 安全检查（如 SQL 拼接、XSS 未转义）
- **禁止修改** rules/ 以外的配置文件作为绕过规则的 workaround
- **禁止在未沟通的情况下** 删除他人代码

## 修改限制

- 修改 {{MODULE}} 前必须先 `/sdc-plan` 并获得确认
- 修改 {{MODULE}} 需要通知 {{OWNER}}（通过 {{METHOD}}）

## 代码风格强制

- 不使用 {{ANTI_PATTERN}}（原因：{{REASON}}）
- 不引入 {{TECH}}（已在 ADR-{{ID}} 中废弃）
- 禁止在 {{LOCATION}} 写业务逻辑（应该放在 {{CORRECT_LOCATION}}）

## 已知陷阱

> 这些是团队踩过的坑，避免重蹈覆辙。

1. {{PITFALL_1}}：{{REASON}} → 正确做法：{{CORRECT_PRACTICE}}
2. {{PITFALL_2}}：{{REASON}} → 正确做法：{{CORRECT_PRACTICE}}
