---
name: sds-init
description: 项目初始化——扫描项目源码信息并自动填充 .claude/ 配置文件中的项目信息段落
---

# /sds-init Skill 规范

## 用途

扫描目标项目的源码，提取技术栈版本、数据库信息、中间件、目录结构、代码模式等项目信息，然后直接 Edit 替换 `.claude/` 配置文件中对应的项目信息段落。替换完成后自动进行一轮评审验证。

## 触发场景

- 用户在新项目上初始化 `.claude/` 配置时调用 `/sds-init`
- 项目技术栈/数据库/目录结构发生重大变更时重新调用

## 前置条件

- `.claude/` 目录已存在并包含配置文件（如不存在，先提示用户复制 claudeConfig）
- 项目目录中至少有 pom.xml 或 package.json（否则无法检测项目类型）

## 约定

- **后端固定 Maven**，前端固定 npm — 不需要检测包管理器
- **不替换 .ps1 和 .py 脚本** — 这些是通用工具，已覆盖 mvn/npm/pip/gradle
- **不替换 settings.json** — allow 列表固定为 Bash(mvn/npm/git/node/python工具)
- **表达差异可接受** — 版本号/关键信息正确即可，空格/格式/措辞差异不阻断
- **规则/治理/流程内容不替换** — 只替换项目信息段落

## 工作流程

```
扫描项目源码 → 展示扫描结果供用户确认 → Edit 替换 14 个配置文件 → 评审验证 → 最终报告
```

---

## 第一步：扫描项目信息

使用 Read/Glob/Grep/Bash 扫描项目源码，按以下子步骤执行：

### 1.1 项目基础

- Bash: 获取项目根目录名（`basename` 或 `ls`）
- Read: 根 pom.xml → 提取 `<artifactId>/<name>/<version>/<modules>/<java.version>` 和关键依赖（spring-boot、mybatis-plus、redisson、sa-token/spring-security、druid/hikari）
- Read: package.json → 提取 `name/version/dependencies`（vue、element-ui/element-plus、vuex/pinia、typescript）和 `scripts`（build/test/lint/e2e）
- Read: README.md（如有）→ 补充项目描述
- 如无 pom.xml → 纯前端项目，跳过后端扫描
- 如无 package.json → 纯后端项目，跳过前端扫描

### 1.2 数据库

- Glob: 定位 `application*.yaml` / `application*.yml` / `application*.properties`
- Read: YAML → 提取 `spring.datasource.url`（或 `spring.datasource.dynamic.datasource.master.url`）
- AI 从 JDBC URL 解析：数据库类型（mysql/postgresql/oracle/highgo/dm/kingbase）+ 版本 + host + port + dbname
- 从 JDBC URL 参数提取 `characterEncoding` → charset
- Glob: 检测 `sql/` 下各数据库子目录（sql/mysql/、sql/postgresql/ 等）
- Read: 采样 1-2 个 DDL SQL 文件 → 提取 `ENGINE=xxx DEFAULT CHARSET=xxx COLLATE=xxx`

### 1.3 中间件

- Read: YAML → 提取 `spring.redis.*` / `spring.data.redis.*` / `spring.rabbitmq.*` / `spring.activemq.*` / `spring.kafka.*`
- Grep: pom.xml 中搜索 redisson / spring-kafka / spring-amqp 依赖
- AI 合成描述字符串（如 "Redis + Redisson（缓存/分布式锁）"）
- 如无中间件 → 描述为"无"

### 1.4 项目结构

- Read: pom.xml `<modules>` → 模块列表
- Bash: 生成 3 层目录树（排除 node_modules/.git/target/build/dist/.idea）
- Glob: 检测关键目录（controller/、service/、dal/dataobject/、dal/mysql/、convert/、src/api/、src/views/、src/router/、src/store/、src/utils/、src/directive/、src/components/）
- AI 分类模块角色：server（聚合模块）、framework（框架层，禁止修改）、business（业务模块）、bom（依赖管理，禁止修改）、frontend（前端）、support（sql/script）
- AI 标记禁止修改目录：`*-framework/` 和 `*-dependencies/`

### 1.5 命令

- 后端固定 Maven：`mvn clean compile`（编译）、`mvn test`（测试）
- 检测 pom.xml 是否有 spotless 插件 → `mvn spotless:apply`（格式化）
- 前端固定 npm：从 package.json scripts 读取 `npm run build:prod`、`npm run lint`
- 检测 Playwright/Cypress → E2E 状态（"已配置"或"未配置"）

### 1.6 文件扩展名

- Bash: 收集项目中代码文件扩展名（排除 node_modules/.git/target）
- AI 过滤合成正则（如 `(java|xml|vue|js|sql|yaml|yml)$`）

### 1.7 代码模式采样

这是 SDA agents 配置依赖的关键信息。用 Grep + Read 采样检测：

**后端模式：**
- `@TableName` → ORM 表注解
- `BaseDO` → DO 基类名
- `BaseMapper` → Mapper 基类
- `LambdaQueryWrapperX` → 查询构建器类
- `*SaveReqVO` / `*PageReqVO` / `*RespVO` → VO 命名后缀
- `@PreAuthorize("@ss.hasPermission")` → 权限 SpEL bean 名（如 `ss`）
- 权限后缀模式：`xxx:create/update/delete/query/export`
- `CommonResult` / `PageResult` → 响应包装类
- `ServiceException` / `BizException` → 业务异常类
- `#{}` vs `${}` → SQL 参数绑定风格（mapper XML）
- `EncryptTypeHandler` → 加密字段处理器
- `@TableLogic` → 逻辑删除注解
- Read 1 个 BaseDO 类 → 审计字段名列表（creator/create_time/updater/update_time/deleted + tenant_id?）
- Read 1 个 Controller → @Tag 前缀、@PreAuthorize 表达式、返回类型 CommonResult/PageResult
- Read 1 个 Service → DI 注解（@Resource/@Autowired）、事务注解、方法签名
- Read 1 个 Mapper → extends 基类、查询构建器
- `@MapperScan` → Mapper 扫描注解包路径

**前端模式：**
- `v-hasPermi` / 其他权限指令 → 权限指令名
- `this.$modal.msgSuccess` / `this.$modal.confirm` → modal 方法
- `<ContentWrap>` / `<Pagination>` → 自定义组件
- `import request from '@/utils/request'` → API 请求工具路径
- API 导出风格：function-style 还是 object-style
- Vuex vs Pinia import → 状态管理库
- tsconfig.json 存在性 → TypeScript 使用
- Read 1 个 API file → URL 模式（/xxx/page、/xxx/get?id=、/xxx/create 等）

---

## 第二步：展示扫描结果，确认范围

用 AskUserQuestion 展示扫描摘要，包括：

- 项目名称
- 技术栈描述（后端框架+版本 / 前端框架+版本）
- 数据库（类型+版本+charset）
- 中间件描述
- 模块列表及角色分类
- 禁止修改目录
- 命令列表（构建/测试/格式化/lint）
- 代码模式摘要（权限方式/VO命名/组件模式等）

用户确认 → 继续替换；用户调整 → 修正后继续。

---

## 第三步：Edit 替换 14 个配置文件

逐文件逐段落 Edit，只替换项目信息段落，不触碰规则/治理/流程内容。

### 替换文件清单及段落

#### 1. CLAUDE.md（根目录）

替换段落：
- 项目信息区：项目名称、技术栈行、数据库行、中间件行
- 命令表：4 行命令（编译/测试/前端构建/前端lint），npm 替代 yarn
- 目录结构图：整个目录树段落
- 修改导航表：各行路径
- 红线规则：禁止修改目录名
- 配置索引：globs 条件加载表中的文件扩展名

#### 2. .claude/knowledge/structure.md

替换段落：
- 完整目录树
- 修改导航详解
- 架构决策记录（ADR）：技术选型从扫描推断，原因需 AskUserQuestion

#### 3. .claude/knowledge/dbinfo.md

替换段落：
- 字符集规范（SET NAMES xxx）
- 方言差异对照表（根据实际 DB 类型生成）
- 目标数据库标注（DB_TYPE）
- 禁止事项中的 DB_TYPE 引用

#### 4. .claude/rules/testing.md

替换段落：
- 测试命令行（mvn test → 固定 Maven 不改）
- E2E 测试命令和状态标注
- 覆盖率命令（如有 JaCoCo → `mvn jacoco:report`；否则"无"）

#### 5. .claude/rules/frontend.md

替换段落：
- 技术栈声明（Vue2 + Element-UI + Vuex + Webpack → 换为扫描结果）

#### 6. .claude/rules/security.md

替换段落：
- MyBatis 安全语法（`#{}` not `${}`）→ 如项目用 JPA 则删除此条，改为 JPA 参数绑定安全规则
- 权限注解（`@PreAuthorize("@ss.hasPermission")`）→ 换为扫描结果

#### 7. .claude/rules/governance.md

替换段落：
- P0-2 前端构建命令（`yarn install && yarn build:prod` → `npm install && npm run build:prod`）
- P0-4 密钥扫描命令（如有 secrets-sync.py 则保留；否则标注"无"）
- P2-15 端口（后端端口从 YAML server.port 提取）

#### 8. .claude/agents/sda-db-implementer.md

替换段落：
- SQL charset 规范（`SET NAMES utf8mb4` → 实际 charset）
- SQL template 中的 ENGINE/CHARSET/COLLATE → 实际值
- 审计字段列表 → 从 BaseDO 类提取的实际字段
- 逻辑删除字段 → 从 @TableLogic 提取
- 主键规范 → 从 @TableId 提取
- 索引命名规范 → 从 CREATE INDEX 提取
- DO 类模式（@TableName/@KeySequence/BaseDO/Lombok）→ 实际注解集
- Mapper 模式（extends BaseMapper/LambdaQueryWrapperX）→ 实际模式
- EncryptTypeHandler → 实际 TypeHandler（如有）
- SQL 脚本路径（sql/mysql/）→ 实际 SQL 目录
- DO/Mapper 输出路径 → 实际包路径
- 租户字段 → 如有 TenantLineHandler 则添加

#### 9. .claude/agents/sda-backend.md

替换段落：
- VO 命名模式 → 实际 VO 后缀（如 SaveReqVO/PageReqVO/RespVO）
- Service 模式 → 实际命名和注解
- Controller 模式 → 实际注解集和 @Tag 前缀
- 权限后缀 → 实际权限命名（如 xxx:create/update/delete/query/export）
- 权限 SpEL bean → 实际 bean 名（如 `ss`）
- DI 注解 → 实际注入方式（@Resource/@Autowired）
- 事务注解 → 实际事务注解
- 响应包装 → 实际包装类（CommonResult/PageResult）
- 业务异常类 → 实际异常类名
- Controller 子包 → 实际路径（admin/app 或其他）
- PageParam 基类 → 实际分页基类名

#### 10. .claude/agents/sda-frontend.md

替换段落：
- 技术栈声明 → 实际框架+UI库+语言
- 状态管理 → 实际库和版本
- 技术栈排除 → 根据实际检测（如"不使用 TypeScript 或 Pinia"）
- 权限指令 → 实际指令名
- Modal 方法 → 实际方法名
- 组件模式 → 实际组件名
- API 导入 → 实际请求工具路径
- API 导出风格 → 实际风格
- API URL 模式 → 实际 URL 格式
- 文件路径模式 → 实际路径（api/views/router）
- UI 库版本引用 → 实际版本

#### 11. .claude/agents/sda-tester.md

替换段落：
- 后端测试注解 → 实际注解集
- 异常断言 → 实际异常类
- 前端 stubs → 实际需 stub 的组件列表
- 测试命令 → 实际命令
- 测试角色 → 实际角色配置（如从系统菜单表提取）
- E2E 框架 → 实际框架和 API
- 文件路径 → 实际测试目录路径

#### 12. .claude/agents/sda-architect.md

替换段落：
- 权限注解 → 实际注解
- 菜单表名 → 实际表名（从 SQL 或 @TableName 提取）
- 状态管理选项 → 实际库

#### 13. .claude/agents/sda-code-reviewer.md

替换段落：
- MyBatis SQL 注入检查 → 如项目用 JPA 则删除此检查项
- 权限注解检查 → 实际注解
- DB 查询工具命令 → 如有 db-query.py 则保留
- 文件类型分类 → 实际文件类型

#### 14. .claude/agents/sda-build-error-resolver.md

替换段落：
- 框架错误类别 → 实际框架名
- 依赖树命令 → Maven 固定不改

### 不替换文件

- `.claude/settings.json` — allow 列表固定
- `.claude/hooks/*.ps1` — 通用脚本
- `.claude/tools/*.py` — 通用工具
- 各文件中的规则/治理/流程内容 — 只替换项目信息

---

## 第四步：评审验证

替换完成后，自动触发评审：

### 4.1 逐文件 Read 检查

Read 所有 14 个被修改的文件，逐文件验证替换内容。

### 4.2 交叉验证

- 技术栈描述 ↔ pom.xml/package.json 版本号一致？
- 数据库类型 ↔ JDBC URL 一致？
- 中间件描述 ↔ pom.xml 依赖 + YAML 配置一致？
- 目录结构 ↔ 实际文件系统一致？
- 命令 ↔ package.json scripts 一致？
- SDA 代码模式 ↔ 实际代码采样一致？

### 4.3 SDA 特殊验证

- sda-db-implementer 的 SQL template charset/engine/collation ↔ 实际 DDL 一致？
- sda-backend 的 VO 命名 ↔ 实际 VO 类名一致？
- sda-frontend 的组件模式 ↔ 实际 Vue 代码一致？
- sda-tester 的 stubs ↔ 实际组件一致？
- security.md 的 ORM 检查 ↔ 项目实际 ORM 一致？

### 4.4 修正

发现不一致 → Edit 修正。修正后重新验证该文件。

### 4.5 通过

全部验证通过 → 进入第五步。

---

## 第五步：最终报告

展示完整验证报告：

```
=== 项目初始化报告 ===

扫描信息：
  项目名称: xxx
  技术栈: xxx
  数据库: xxx
  中间件: xxx

修改文件（14 个）：
  ✅ CLAUDE.md — 项目信息区/命令/目录/红线
  ✅ structure.md — 目录树/导航/ADR
  ✅ dbinfo.md — charset/方言/DB类型
  ✅ testing.md — 命令/E2E
  ✅ frontend.md — 技术栈
  ✅ security.md — ORM/权限
  ✅ governance.md — 构建命令/端口
  ✅ sda-db-implementer.md — SQL规范/字段/DO/Mapper
  ✅ sda-backend.md — VO/Service/Controller/权限
  ✅ sda-frontend.md — 技术栈/组件/API
  ✅ sda-tester.md — 注解/stubs/命令/E2E
  ✅ sda-architect.md — 权限/菜单表
  ✅ sda-code-reviewer.md — ORM检查/权限
  ✅ sda-build-error-resolver.md — 框架/命令

不修改文件（4 个）：
  ⬜ settings.json — 固定配置
  ⬜ *.ps1 hooks — 通用脚本
  ⬜ *.py tools — 通用工具

评审验证：
  ✅ 全部交叉验证通过

需用户手动确认的信息：
  - ADR 技术选型原因（AI 推断技术，原因需人工填写）
  - 已知陷阱（团队踩坑经验）
  - 其他团队约定

下一步：
  1. 手动填写 ADR 原因和已知陷阱
  2. 提交 Git
```

用 AskUserQuestion 询问用户是否需要填写 ADR 原因等手动信息。用户选择填写 → 逐项询问；用户选择跳过 → 结束初始化。