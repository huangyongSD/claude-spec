# 项目 AI 协作规范

> 遵循「配置即代码」原则，所有变更需提交到版本控制。

## 项目信息

- **项目名称**：`yudao（芋道）`
- **技术栈**：`SpringBoot 2.7.18 + MyBatis-Plus 3.5.15 + JDK8 / Vue2 2.7.14 + Element-UI 2.15.14`
- **数据库**：`MySQL 8.0`
- **中间件**：`Redis + Redisson（缓存/分布式锁）`

| 命令 | 用途 |
|------|------|
| `mvn clean compile` | 后端全量编译 |
| `mvn test` | 后端单元测试 |
| `yarn build:prod` | 前端生产构建 |
| `yarn lint` | 前端 Lint |

## 目录结构

> 详细结构见 [.claude/knowledge/structure.md](.claude/knowledge/structure.md)

```
yudao-boot-mini/
├─ yudao-server/          主服务器（聚合模块）
├─ yudao-framework/       框架层（禁止修改）
├─ yudao-module-system/   系统功能模块
├─ yudao-module-infra/    基础设施模块
├─ yudao-dependencies/    BOM 依赖管理（禁止修改）
├─ yudao-ui-admin/        前端管理后台
├─ sql/                   数据库脚本
└─ script/                部署脚本
```

## 修改导航

| 场景 | 目标位置 |
|------|----------|
| 新增 API | `controller/**/*.java`（admin/app 子包） |
| 修改业务逻辑 | `service/**/*.java` |
| 新增数据库表 | `sql/mysql/` 目录 |
| 修改配置 | `yudao-server/.../application*.yaml` |
| 新增前端页面 | `yudao-ui-admin/src/views/` + `src/router/` |

## 红线规则（5 条）

1. **禁止修改 `yudao-framework/` 和 `yudao-dependencies/`** — 需通过 `/sds-plan` 并获确认
2. **禁止硬编码密钥/SQL 拼接** — 见 [security.md](.claude/rules/security.md)
3. **禁止 Controller 写业务逻辑** — 应放在 Service
4. **禁止提交真实密码/IP** — 使用占位符，见 [敏感信息保护](#敏感信息保护)
5. **新功能必须先 Spec 再开发** — 见 [工作流](#工作流)

> 详细规则按文件类型自动加载：security.md / frontend.md / testing.md / governance.md

## 工作流

### 新功能开发（强制）

```
沟通任务 → /sds-spec → Spec 评审 → /sds-dev → 编译验证 → Git 提交
```

**豁免条件**：用户说"直接改"/"不用规划"，或单文件小改动（bug 修复、配置调整）

### 高风险操作（必须先 Plan）

- 多文件批量改动（≥3 个文件）
- 代码重构、引入新依赖
- 安全/权限相关修改

## 敏感信息保护

- 配置文件使用占位符（如 `{{DB_MASTER_PASSWORD}}`）
- 真实值存储在 `.claude/tools/secrets.json`（不提交 Git）
- 数据库查询用 `db-query.py`，不将密码传给 AI

## 配置索引

| 类型 | 位置 |
|------|------|
| 规则 | `.claude/rules/{security,frontend,testing,governance}.md`（globs 条件加载） |
| 知识库 | `.claude/knowledge/`（按需 Read，不自动加载） |
| Spec 模板 | `.claude/templates/spec/` |
| Skills | `/sds-plan` `/sds-spec` `/sds-dev` `/sds-codereview` `/sds-buildfix` `/sds-dbquery` |
| 工具 | `.claude/tools/db-query.py` `secrets-sync.py` |

## Rules 条件加载

> Rules 文件通过 `globs` frontmatter 实现条件加载，只有操作匹配文件时才加载。

| 文件 | 触发条件 |
|------|----------|
| security.md | `*.java` `*.sql` `*.vue` `*.js` `*.yaml` `*.xml` |
| frontend.md | `*.vue` `*.js` `*.css` `*.scss` |
| testing.md | `*Test*.java` `*.spec.js` `*.test.js` `test-cases.md` |
| governance.md | `*.java` `*.vue` `*.js` `*.sql` `.claude/**/*.md` |

## 知识库按需读取

> 知识库文件不在 rules 自动加载范围内，AI 在对应场景必须主动 Read。

| 文件 | 读取时机 |
|------|----------|
| structure.md | 定位文件、理解项目结构时 |
| dbinfo.md | 编写 SQL、处理数据库相关任务时 |
| troubleshooting.md | 遇到编译/运行/部署报错、调用 `/sds-buildfix` 时 |

