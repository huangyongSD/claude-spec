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
- **表达差异可接受** — 版本号/关键信息正确即可，空格/格式/措辞差异不阻断
- **规则/治理/流程内容不替换** — 只替换项目信息段落

## 工作流程

```
第一步：扫描项目信息（含登录接口与鉴权检测）→ 第二步：E2E 框架自动配置 → 第三步：展示扫描结果供用户确认 → 第四步：Edit 替换 16 个配置文件（含 secrets.json）→ 第五步：审批通用配置文件 → 第六步：评审验证 → 第七步：最终报告
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

### 1.8 登录接口与鉴权检测

> **核心目标**：找出系统登录接口和鉴权方式，配置测试和调试时的认证流程。所有后端接口测试都必须先调用登录接口获取 token，然后按照系统鉴权方式携带 token 请求。

#### 1.8.1 检测鉴权框架

- Grep: pom.xml 中搜索 `spring-boot-starter-security` / `sa-token` / `jwt` / `jjwt` 等依赖
- Grep: 源码中搜索 `@EnableWebSecurity` / `@Configuration` + `SecurityConfig` / `SaTokenConfig` 等配置类
- Read: 鉴权配置类 → 提取鉴权框架类型（Spring Security / Sa-Token / 自定义）

#### 1.8.2 检测登录接口

- Grep: 搜索 `@PostMapping` / `@GetMapping` + `login` / `signin` / `auth` 关键字
- Grep: 搜索 `login` 相关 Controller 方法名
- Read: 登录 Controller → 提取：
  - 接口路径（如 `/login`、`/auth/login`）
  - 请求方式（POST / GET）
  - 请求参数结构（username、password、captcha、uuid 等）
  - 返回结构（token 字段名、用户信息等）

#### 1.8.3 检测 Token 类型与携带方式

**Token 类型检测：**
- Grep: 搜索 `JwtUtil` / `JwtHelper` / `Jwts` → JWT 类型
- Grep: 搜索 `session.getId()` / `session.setAttribute()` → Session 类型
- Grep: 搜索 `StpUtil` / `SaManager` → Sa-Token 类型
- Read: Token 工具类 → 提取 token 生成逻辑和有效期

**Token 携带方式检测：**
- Grep: 搜索 `Authorization` / `Bearer` → Header 携带方式
- Grep: 搜索 `Cookie` / `addCookie` → Cookie 携带方式
- Grep: 搜索 `request.getHeader` → 自定义 Header 名称
- Read: 鉴权拦截器 / 过滤器 → 提取 token 提取逻辑

**Token 前缀检测：**
- Grep: 搜索 `Bearer` / `Bearer ` → Bearer 前缀
- 如无前缀 → 标注为"无前缀"

#### 1.8.4 检测 Token 刷新机制

- Grep: 搜索 `refresh` / `refreshToken` / `renew`
- Read: Token 刷新接口 → 提取刷新路径和参数

#### 1.8.5 检测测试账号

- Grep: SQL 初始化脚本中搜索 `INSERT INTO sys_user` / `INSERT INTO user`
- Read: 测试配置文件 → 提取测试账号和密码
- **如检测到测试账号 → 展示给用户确认**
- **如未检测到 → 使用 AskUserQuestion 要求用户输入测试账号信息**：
  - 用户名（必填）
  - 密码（必填）
  - 角色说明（可选，如"超级管理员"、"普通用户"）

> **强制要求**：测试账号必须配置，否则后续测试无法执行。如果用户拒绝输入，在报告中标注"未配置测试账号，测试功能将受限"。

#### 1.8.6 生成认证配置摘要

AI 合成以下信息：

```yaml
登录接口:
  路径: /login
  方法: POST
  参数: { username: string, password: string, captcha: string, uuid: string }
  返回: { token: string, user: object }

鉴权方式:
  框架: Spring Security / Sa-Token / 自定义
  Token类型: JWT / Session / 其他
  Token携带: Header#Authorization
  Token前缀: Bearer
  Token有效期: 24h

刷新接口:
  路径: /refresh
  方法: POST

测试账号:
  - 用户名: admin, 密码: admin123, 角色: 超级管理员
  - 用户名: test, 密码: test123, 角色: 普通用户
```

---

## 第二步：E2E 框架自动配置（强制）

> **强制要求**：所有项目必须配置 E2E 测试框架，不允许跳过或降级。

### 2.1 检测当前 E2E 状态

检查项目中是否已存在 E2E 测试框架：

1. 检查 `package.json` 中是否已安装 Playwright / Cypress / Nightwatch 等
2. 检查是否存在 E2E 配置文件（如 `playwright.config.js`、`cypress.config.ts`）
3. 检查是否存在 E2E 测试目录（如 `tests/e2e/`、`cypress/`）

### 2.2 如未配置，自动安装 Playwright

> **选择理由**：Playwright 是现代 Web 应用的首选 E2E 框架，支持 Vue/React 等主流框架，API 简洁，文档完善。

**前置条件**：项目必须有 `package.json`（纯后端项目跳过此步骤）

**安装步骤**：

1. **安装 Playwright 依赖**
   ```bash
   cd <前端项目目录>
   npm install -D @playwright/test
   ```

2. **创建 Playwright 配置文件**
   创建 `playwright.config.js`（内容见下方模板）

3. **创建测试目录结构**
   ```
   <前端项目>/
   └── tests/
       └── e2e/
           ├── pages/           # 页面对象
           ├── specs/           # 测试用例
           ├── fixtures/         # 测试数据
           └── utils/           # 测试工具
   ```

4. **添加 E2E 测试脚本到 package.json**
   在 `scripts` 中添加：
   ```json
   {
     "test:e2e": "playwright test",
     "test:e2e:ui": "playwright test --ui",
     "test:e2e:headed": "playwright test --headed"
   }
   ```

5. **安装浏览器**
   ```bash
   npx playwright install chromium
   ```

### 2.3 Playwright 配置模板

创建 `playwright.config.js`：

```javascript
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e/specs',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:80',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:80',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

### 2.4 验证 E2E 框架安装成功

```bash
cd <前端项目目录>
npx playwright test --version
```

验证输出包含 Playwright 版本号，表示安装成功。

### 2.5 纯后端项目处理

如项目无 `package.json`（纯后端项目）：

1. **跳过前端 E2E 配置**，不阻断初始化流程
2. **在初始化报告中标注**：纯后端项目，前端 E2E 测试待配置
3. **后续处理**：如后续添加前端模块，再调用 `/sds-init` 重新初始化

### 2.6 移动端项目处理

> 移动端项目（uni-app、React Native、Flutter 等）不适用 Web E2E 测试框架。

如检测到移动端项目（如 package.json 中包含 uni-app、react-native、flutter、taro、mpvue 等）：

1. **跳过 Playwright 配置**，不阻断初始化流程
2. **在初始化报告中标注**：移动端项目，E2E 测试降级为人工验收
3. **说明**：移动端 E2E 需要 Appium/Detox 等原生测试框架，建议在专项测试方案中处理

---

## 第三步：展示扫描结果，确认范围

用 AskUserQuestion 展示扫描摘要，包括：

- 项目名称
- 技术栈描述（后端框架+版本 / 前端框架+版本）
- 数据库（类型+版本+charset）
- 中间件描述
- 模块列表及角色分类
- 禁止修改目录
- 命令列表（构建/测试/格式化/lint）
- 代码模式摘要（权限方式/VO命名/组件模式等）
- **登录接口信息**（路径/方法/参数/返回）
- **鉴权方式**（框架/Token类型/携带方式/前缀）

**测试账号处理流程**：

1. **如已检测到测试账号**：
   - 展示检测到的账号列表
   - 用户确认或调整

2. **如未检测到测试账号**：
   - 提示："未检测到测试账号，请输入测试账号信息"
   - 使用 AskUserQuestion 要求用户输入：
     - 管理员账号：用户名 / 密码
     - 普通用户账号：用户名 / 密码（可选）
   - 用户选择跳过 → 在报告中标注"未配置测试账号"

用户确认 → 继续替换；用户调整 → 修正后继续。

---

## 第四步：Edit 替换 16 个配置文件（含 secrets.json）

> **强制要求**：secrets.json 必须与项目数据库、中间件配置保持一致，这是 sds-dbquery 等工具正常运行的前提。

逐文件逐段落 Edit，只替换项目信息段落，不触碰规则/治理/流程内容。

### 替换文件清单及段落

#### 0. .claude/tools/secrets.json（强制更新）

> **此文件关系到 db-query.py 等工具能否正常运行，必须与项目配置一致。**

替换字段（从 application*.yml 扫描获取）：
- `db_master_url` → 从 `spring.datasource.druid.master.url` 提取完整 JDBC URL（必须保留 `currentSchema`、`characterEncoding` 等参数）
- `db_master_host` → 从 JDBC URL 解析 host
- `db_master_port` → 从 JDBC URL 解析 port
- `db_master_name` → 从 JDBC URL 解析 dbname（如 `digital_housing`）
- `db_master_schema` → 从 JDBC URL 的 `currentSchema=` 参数提取（如未指定则为 public）
- `db_master_user` → 从 `spring.datasource.druid.master.username` 提取
- `db_master_password` → 从 `spring.datasource.druid.master.password` 提取
- `db_slave_*` → 从 `spring.datasource.druid.slave` 提取（如未启用则留空）
- `redis_host` → 从 `spring.redis.cluster.nodes` 或 `spring.redis.host` 提取
- `redis_port` → 从 `spring.redis.cluster.nodes` 提取（如为集群，取第一个节点的 port）
- `redis_password` → 从 `spring.redis.password` 提取（如无密码则留空）
- `rabbit_host` → 从 `rocketmq.name-server` 或 `spring.rabbitmq.*` 提取
- `rabbit_port` → 从 `rocketmq.name-server` 或 `spring.rabbitmq.*` 提取

> **注意**：
> - secrets.json 中 `real_values` 和 `placeholders` 的对应字段必须同步更新
> - `db_master_url` 必须完整保留原始参数（currentSchema、characterEncoding、serverTimezone 等），不得截断

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
- **登录接口配置** → 实际登录接口路径/方法/参数/返回
- **鉴权方式配置** → 实际鉴权框架/Token类型/携带方式/前缀

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
- **登录认证配置** → 实际登录接口信息（路径/方法/参数/返回）
- **Token 携带方式** → 实际携带方式（Header#Authorization / Cookie）
- **Token 前缀** → 实际前缀（Bearer / 无前缀）
- **测试账号配置** → 实际测试账号列表（用户名/密码/角色）
- **认证流程说明** → 测试前先登录获取 token，后续请求携带 token

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

#### 15. .claude/knowledge/auth.md（新建）

> **新建文件**：存储系统登录接口和鉴权配置信息，供所有 SDA 和测试工具使用。

创建文件并写入以下内容：
```markdown
# 系统认证配置

> 本文件由 /sds-init 自动生成，存储登录接口和鉴权方式信息。

## 登录接口

- **路径**：{实际路径，如 /login}
- **方法**：{实际方法，如 POST}
- **参数**：
  - username: {类型，如 string}
  - password: {类型，如 string}
  - captcha: {类型，如 string（可选）}
  - uuid: {类型，如 string（可选）}
- **返回**：
  - token: {字段名，如 token}
  - user: {用户信息对象}

## 鉴权方式

- **框架**：{实际框架，如 Spring Security / Sa-Token / 自定义}
- **Token 类型**：{实际类型，如 JWT / Session / 其他}
- **Token 携带方式**：{实际方式，如 Header#Authorization}
- **Token 前缀**：{实际前缀，如 Bearer}
- **Token 有效期**：{实际有效期，如 24h}

## Token 刷新

- **刷新接口**：{实际路径，如 /refresh}
- **刷新方法**：{实际方法，如 POST}
- **刷新参数**：{实际参数}

## 测试账号

> **重要提示**：测试账号由用户在初始化时手动输入，用于测试和调试。

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| {用户输入的用户名} | {用户输入的密码} | {用户输入的角色} | {用户输入的说明} |
| {如未配置} | - | - | 未配置测试账号，测试功能将受限 |

> **安全提醒**：测试账号信息存储在本地配置文件中，不会提交到 Git。请勿使用生产环境账号密码。

## 测试认证流程

> **所有后端接口测试必须遵循此流程**

1. **登录获取 Token**
   ```bash
   # 示例请求（使用配置的测试账号）
   # 用户名密码从 .claude/knowledge/auth.md 读取
   curl -X POST http://localhost:8080/login \
     -H "Content-Type: application/json" \
     -d "{\"username\":\"$TEST_USERNAME\",\"password\":\"$TEST_PASSWORD\"}"
   
   # 响应示例
   {"token":"eyJhbGciOiJIUzUxMiJ9...","user":{...}}
   ```

> **重要**：命令行测试时，用户名密码应从环境变量或配置文件读取，禁止硬编码。

2. **携带 Token 请求业务接口**
   ```bash
   # 示例请求（Header 方式）
   curl -X GET http://localhost:8080/api/xxx \
     -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
   
   # 示例请求（Cookie 方式）
   curl -X GET http://localhost:8080/api/xxx \
     -H "Cookie: JSESSIONID=xxx"
   ```

3. **测试代码示例**
   ```java
   // 单元测试认证示例
   @BeforeEach
   void setUp() {
       // 1. 登录获取 token（使用配置的测试账号）
       // 测试账号从 .claude/knowledge/auth.md 读取
       String username = getConfiguredTestUsername(); // 从配置读取
       String password = getConfiguredTestPassword(); // 从配置读取
       
       LoginRequest loginRequest = new LoginRequest(username, password);
       LoginResponse loginResponse = authService.login(loginRequest);
       this.token = loginResponse.getToken();
       
       // 2. 设置到请求头
       mockMvc = MockMvcBuilders.webAppContextSetup(context)
           .defaultRequest(post("/api/xxx")
               .header("Authorization", "Bearer " + token))
           .build();
   }
   ```

> **重要**：测试代码中禁止硬编码用户名密码，必须从配置文件读取。

## 变更记录

| 日期 | 变更内容 | 原因 |
|------|----------|------|
| {日期} | 初始化认证配置 | /sds-init 自动生成 |
```

---

## 第五步：审批通用配置文件

审批 settings.json、hooks/*.ps1、tools/*.py、secrets.json 是否符合当前项目技术栈和项目结构，不符合则修改。

- Read: `.claude/settings.json` → 检查 allow 列表是否覆盖当前项目的命令（Bash 允许 mvn/npm/git/node/python 等）
- Glob: `.claude/hooks/*.ps1` → 读取每个 ps1 脚本，检查是否涉及项目特有的路径/命令
- Glob: `.claude/tools/*.py` → 读取每个 py 工具，检查是否涉及项目特有的路径/框架
- **Read: `.claude/tools/secrets.json` → 验证数据库类型是否与项目一致**
  - 检查 `db_master_url` 的 JDBC 前缀：`jdbc:mysql://` / `jdbc:postgresql://` / `jdbc:highgo://`
  - 如 db-query.py 使用 psycopg2，则 `db_master_url` 必须为 PostgreSQL 兼容格式
  - 如 db-query.py 使用 pymysql，则 `db_master_url` 必须为 MySQL 格式
  - 如不匹配，Edit 修正 secrets.json 并更新 db-query.py 的连接参数

发现不符合 → Edit 修正。

### 5.1 JDBC URL 参数同步（强制）

> **问题背景**：JDBC URL 中的 `currentSchema`、`characterEncoding`、`serverTimezone` 等参数直接影响数据库连接和字符编码。db-query.py 必须完整保留这些参数，否则可能导致连接失败或中文乱码。

**强制要求**：所有项目的 db-query.py 必须支持从 JDBC URL 解析完整参数。

**处理流程**：

1. **从 JDBC URL 解析完整参数**
   - 提取数据库类型（mysql/postgresql/highgo/kingbase/dm）
   - 提取 `currentSchema` → schema 名称
   - 提取 `characterEncoding` → 字符编码
   - 提取 `serverTimezone` → 时区
   - 提取其他关键参数（如 `useUnicode`、`allowMultiQueries`）

2. **修改 db-query.py 支持 schema 和编码参数**

   在 `get_secrets_url_config()` 函数中解析参数：

   ```python
   def get_secrets_url_config(secrets):
       real = secrets["real_values"]
       full_url = real.get("db_master_url", "")

       # 通用匹配：jdbc:数据库类型://host:port/database?params
       match = re.match(r'jdbc:([^:]+)://([^/:]+):(\d+)/([^?]+)\??(.*)', full_url)
       if not match:
           return None

       db_type = match.group(1)      # mysql / postgresql / highgo / kingbase / dm
       host = match.group(2)
       port = int(match.group(3))
       database = match.group(4)
       params = match.group(5)

       # 解析 schema 从 currentSchema 参数
       schema = None
       for param in params.split('&'):
           if param.startswith('currentSchema='):
               schema = param.split('=')[1]
               break

       return {
           "db_type": db_type,
           "host": host,
           "port": port,
           "database": database,
           "schema": schema,
           "user": real["db_master_user"],
           "password": real["db_master_password"],
           "full_url": full_url  # 保留完整 URL
       }
   ```

   在 `build_jdbc_url()` 中优先使用完整 URL：

   ```python
   def build_jdbc_url(config):
       # 使用完整 URL（保留所有参数）
       if "full_url" in config:
           return config["full_url"]

       # 回退：手动拼接
       host = config["host"]
       port = config["port"]
       database = config["database"]
       schema = config.get("schema")

       url = f"jdbc:{config.get('db_type', 'postgresql')}://{host}:{port}/{database}"
       if schema:
           url += f"?currentSchema={schema}"
       return url
   ```

   根据数据库类型选择 JDBC driver：

   ```python
   # 根据数据库类型选择 JDBC driver
   DRIVER_MAP = {
       "mysql": "com.mysql.cj.jdbc.Driver",
       "postgresql": "org.postgresql.Driver",
       "highgo": "com.highgo.jdbc.Driver",
       "kingbase": "com.kingbase.Driver",
       "dm": "dm.jdbc.driver.DmDriver",
   }

   def get_driver_class(db_type):
       return DRIVER_MAP.get(db_type, "org.postgresql.Driver")  # 默认 PostgreSQL
   ```

3. **更新 secrets.json 中的配置**
   - 确保 `db_master_url` 完整保留原始参数
   - `db_master_schema` → 从 JDBC URL 的 `currentSchema=` 参数提取（如未指定则为 public）

4. **验证连接**

   执行测试查询验证连接正常且无乱码：
   ```bash
   python .claude/tools/db-query.py --query "SELECT xmdm FROM prjsys.project_info LIMIT 1"
   ```

---

### 5.2 Windows 中文路径下 hooks 脚本处理（Windows 专用）

> **问题背景**：PowerShell 在解析含中文字符的路径时存在编码问题，导致 hooks 脚本执行失败（报错：无法识别文件格式或路径不存在）。项目路径含中文（如 `C:/Users/xxx/Desktop/住建厅/数据治理/`）时，`.claude/hooks/*.ps1` 的相对路径会触发此问题。

**检测条件**：当前系统为 Windows（`platform: win32`）且项目路径包含非 ASCII 字符。

**处理流程**：

1. **检测项目路径是否含中文**
   - 检查项目根目录路径是否包含非 ASCII 字符（如中文、日文、特殊符号）
   - Windows 可用 `echo $PWD | grep -P '[^\x00-\x7F]'` 检测

2. **如项目路径含中文，执行以下步骤**

   #### 5.2.1 创建 ASCII 路径目录

   询问用户输入一个纯 ASCII 路径（如 `C:/Users/andyh/.claude/hooks-scripts`），用于存放 hooks 脚本。

   > **提示**：推荐使用 `~/.claude/hooks-scripts`（即 `C:/Users/<用户名>/.claude/hooks-scripts`），这是 Claude Code 全局配置目录，不随项目路径变化。

   使用 `mkdir -p "<用户输入的路径>"` 创建目录。

   #### 5.2.2 复制 hooks 脚本到新位置

   从 `.claude/hooks/*.ps1` 读取所有 ps1 脚本内容，复制到新目录。

   **关键修改**：每个脚本中 `$secretsPath` 的相对路径引用改为绝对路径：
   ```powershell
   # 原（相对路径，会受工作目录中文影响）：
   $secretsPath = Join-Path $PSScriptRoot "..\tools\secrets.json"

   # 改为（绝对路径，绕过中文路径问题）：
   $secretsPath = "C:/Users/<用户名>/.claude/tools/secrets.json"
   ```

   > **注意**：脚本中如有 `param()` 声明，保留不动；仅修改路径相关变量。

   #### 5.2.3 更新 settings.json 中的 hooks 引用

   将 `.claude/settings.json` 中所有 hooks 的 `command` 路径从相对路径改为绝对路径：
   ```json
   // 改前（相对路径，含 .claude/hooks/）
   "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/post-sensitive-read.ps1"

   // 改后（绝对路径，指向 ASCII 目录）
   "command": "powershell -ExecutionPolicy Bypass -File \"C:/Users/xxx/.claude/hooks-scripts/post-sensitive-read.ps1\""
   ```

   涉及的文件：
   - `pre-bash-check.ps1`
   - `post-sensitive-read.ps1`
   - `post-sensitive-scan.ps1`
   - `post-edit-check.ps1`

   #### 5.2.4 验证 hooks 可执行

   运行测试命令验证：
   ```bash
   powershell -ExecutionPolicy Bypass -File "<新路径>/pre-bash-check.ps1" < /dev/null; echo "Exit: $?"
   ```
   预期输出：`Exit: 0`（无错误）

3. **如项目路径为纯 ASCII，跳过上述步骤**，hooks 脚本保持在 `.claude/hooks/` 原位不动。

---

## 第六步：评审验证

替换完成后，自动触发评审：

### 6.1 逐文件 Read 检查

Read 所有 15 个被修改的文件，逐文件验证替换内容。

### 6.2 交叉验证

- 技术栈描述 ↔ pom.xml/package.json 版本号一致？
- 数据库类型 ↔ JDBC URL 一致？
- **secrets.json 数据库配置 ↔ application*.yml 中的实际配置一致？**
- 中间件描述 ↔ pom.xml 依赖 + YAML 配置一致？
- 目录结构 ↔ 实际文件系统一致？
- 命令 ↔ package.json scripts 一致？
- SDA 代码模式 ↔ 实际代码采样一致？
- **登录接口配置 ↔ 实际 Controller 代码一致？**
- **鉴权方式配置 ↔ 实际鉴权框架配置一致？**
- **测试账号 ↔ 数据库/配置文件一致？**

### 6.3 SDA 特殊验证

- sda-db-implementer 的 SQL template charset/engine/collation ↔ 实际 DDL 一致？
- sda-backend 的 VO 命名 ↔ 实际 VO 类名一致？
- sda-frontend 的组件模式 ↔ 实际 Vue 代码一致？
- sda-tester 的 stubs ↔ 实际组件一致？
- security.md 的 ORM 检查 ↔ 项目实际 ORM 一致？
- **db-query.py 的 JDBC driver ↔ secrets.json 的数据库类型一致？**
  - com.mysql.cj.jdbc.Driver → MySQL
  - org.postgresql.Driver → PostgreSQL
  - com.highgo.jdbc.Driver → HighGo
  - com.kingbase.Driver → Kingbase
  - dm.jdbc.driver.DmDriver → DM（达梦）
  - 不一致则标记为 P0 问题，必须修复

### 6.4 修正

发现不一致 → Edit 修正。修正后重新验证该文件。

### 6.5 通过

全部验证通过 → 进入第七步。

---

## 第七步：最终报告

展示完整验证报告：

```
=== 项目初始化报告 ===

扫描信息：
  项目名称: xxx
  技术栈: xxx
  数据库: xxx
  中间件: xxx

登录接口与鉴权：
  ✅ 登录接口: /login (POST)
    - 参数: username, password
    - 返回: token, user
  ✅ 鉴权方式: Spring Security + JWT
    - Token携带: Header#Authorization
    - Token前缀: Bearer
    - 有效期: 24h
  ✅ 测试账号: admin/admin123 (超级管理员), test/test123 (普通用户)
  ⚠️  未检测到登录接口 — 需手动配置
  ⚠️  未配置测试账号 — 测试功能将受限

E2E 测试框架：
  ✅ Playwright — 已安装并配置完成
    - 配置文件: playwright.config.js
    - 测试目录: tests/e2e/
    - 测试命令: npm run test:e2e
  ℹ️ 纯后端项目 — 跳过 E2E 配置
  ℹ️ 移动端项目 — E2E 降级为人工验收

修改文件（16 个）：
  ✅ secrets.json — 数据库/中间件连接配置（强制）
  ✅ CLAUDE.md — 项目信息区/命令/目录/红线
  ✅ structure.md — 目录树/导航/ADR
  ✅ dbinfo.md — charset/方言/DB类型
  ✅ testing.md — 命令/E2E
  ✅ frontend.md — 技术栈
  ✅ security.md — ORM/权限
  ✅ governance.md — 构建命令/端口
  ✅ sda-db-implementer.md — SQL规范/字段/DO/Mapper
  ✅ sda-backend.md — VO/Service/Controller/权限/登录接口/鉴权方式
  ✅ sda-frontend.md — 技术栈/组件/API
  ✅ sda-tester.md — 注解/stubs/命令/E2E/登录认证/测试账号
  ✅ sda-architect.md — 权限/菜单表
  ✅ sda-code-reviewer.md — ORM检查/权限
  ✅ sda-build-error-resolver.md — 框架/命令
  ✅ auth.md — 登录接口/鉴权方式/测试账号/认证流程

已审批通用配置文件（4 类）：
  ✅ settings.json — allow 列表
  ✅ *.ps1 hooks — 路径/命令适配（Windows 中文路径已迁移至 ASCII 目录）
  ✅ *.py tools — 路径/框架适配
  ✅ secrets.json — 数据库/中间件配置一致性

评审验证：
  ✅ secrets.json ↔ application*.yml 数据库配置一致
  ✅ db-query.py 连接库 ↔ secrets.json 数据库类型一致
  ✅ 全部交叉验证通过

需用户手动确认的信息：
  - ADR 技术选型原因（AI 推断技术，原因需人工填写）
  - 已知陷阱（团队踩坑经验）
  - 其他团队约定
  - 测试账号（如未配置）

下一步：
  1. 手动填写 ADR 原因和已知陷阱
  2. 如未配置测试账号，需用户手动输入
  3. 提交 Git
```

用 AskUserQuestion 询问用户是否需要填写 ADR 原因等手动信息。用户选择填写 → 逐项询问；用户选择跳过 → 结束初始化。

**注意**：测试账号是测试功能的必要条件。如果用户拒绝配置测试账号，在 auth.md 中标注"未配置测试账号"，并提示后续测试功能将受限。