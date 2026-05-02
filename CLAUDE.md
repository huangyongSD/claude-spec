# 项目 AI 协作规范

> 遵循「配置即代码」原则，所有变更需提交到版本控制。

## 项目信息

- **项目名称**：`ruoyi（若依）`
- **技术栈**：`SpringBoot 4.0.3 + MyBatis 4.0.1 + JDK17 / Vue2 2.6.12 + Element-UI 2.15.14`
- **数据库**：`PostgreSQL`
- **中间件**：`Redis + Lettuce（缓存）`

| 命令 | 用途 |
|------|------|
| `mvn clean compile` | 后端全量编译 |
| `mvn test` | 后端单元测试 |
| `npm run build:prod` | 前端生产构建 |
| `npm run dev` | 前端开发服务 |

## 目录结构

> 详细结构见 [.claude/knowledge/structure.md](.claude/knowledge/structure.md)

```
RuoYi-Vue-Postgresql/
├─ ruoyi-admin/          聚合模块（启动入口+Controller）
├─ ruoyi-framework/      框架层（禁止修改）
├─ ruoyi-system/         系统功能模块（domain/mapper/service）
├─ ruoyi-quartz/         定时任务
├─ ruoyi-generator/      代码生成
├─ ruoyi-common/         通用工具（BaseEntity/AjaxResult等）
├─ ruoyi-ui/             前端管理后台
├─ sql/                  数据库脚本（PostgreSQL）
└─ doc/                  文档
```

## 修改导航

| 场景 | 目标位置 |
|------|----------|
| 新增 API | `controller/**/*.java`（system/monitor/tool/common 子包） |
| 修改业务逻辑 | `service/**/*.java` |
| 新增数据库表 | `sql/` 目录 |
| 修改配置 | `ruoyi-admin/.../application*.yml` |
| 新增前端页面 | `ruoyi-ui/src/views/` + `src/router/` |

## 红线规则（5 条）

1. **禁止修改 `ruoyi-framework/`** — 需通过 `/sds-plan` 并获确认
2. **禁止硬编码密钥/SQL 拼接** — 见 [security.md](.claude/rules/security.md)
3. **禁止 Controller 写业务逻辑** — 应放在 Service
4. **禁止提交真实密码/IP** — 使用占位符，见 [敏感信息保护](#敏感信息保护)
5. **新功能必须先 Spec 再开发** — 见 [工作流](#工作流)

> 详细规则按文件类型自动加载：security.md / frontend.md / testing.md / governance.md

## 工作流

### 新功能开发（强制）

```
沟通任务(确认需求+页面布局) → /sds-spec(plan→design迁移) → Spec 评审 → /sds-dev → 编译验证 → Git 提交
```

**豁免条件**：用户说"直接改"/"不用规划"，或单文件小改动（bug 修复、配置调整）

### plan→design 迁移约束（强制）

> plan.md 中与用户确认的页面布局、入口说明是设计决策，`/sds-spec` 生成 design.md 时必须完整继承。

1. **design.md §5.1 必须包含 plan.md 中所有页面的入口说明和 ASCII 布局图**
2. **禁止信息降级**：不得将 plan.md 的 ASCII 布局图压缩为一行文字描述（如"搜索+表格+分页"）
3. **覆盖度校验**：生成 design.md 后，逐项检查 plan.md 中每个页面布局是否在 design.md §5.1 中有对应描述，输出缺失项清单
4. **plan.md 原文保留**：迁移后 plan.md 中的布局内容仍保留（作为需求讨论记录），design.md 是开发者的唯一参考文档

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
| security.md | `*.java` `*.sql` `*.vue` `*.js` `*.yml` `*.xml` |
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

