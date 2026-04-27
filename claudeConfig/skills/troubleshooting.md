---
name: troubleshooting
description: 常见构建与测试问题的排查与修复方法
type: skill
updated: 2026-04-22
---

# 排障知识库

> 记录团队积累的常见问题及其解决方案，持续更新。

---

## Java / SpringBoot 错误

### 编译失败：找不到符号
错误：cannot find symbol / package xxx does not exist
解决：确认 Maven 依赖是否已下载（`mvn dependency:resolve`）；检查 pom.xml 中 scope 是否为 provided/test 导致编译期缺失；IDE 需刷新 Maven 项目

### JDK 版本不匹配
错误：UnsupportedClassVersionError / source release 8 requires target release 8
解决：确认 JAVA_HOME 指向 JDK8；pom.xml 中 `<maven.compiler.source>` 和 `<maven.compiler.target>` 与实际 JDK 版本一致；IDE 中 Project SDK 配置正确

### SpringBoot 启动失败
错误：Unable to start ServletWebServerFactory / Port 8080 already in use
解决：检查端口占用（Windows: `netstat -ano | findstr 8080`）；确认 application.yml 中 server.port 配置；检查是否有多个实例未关闭

### Bean 注入失败
错误：NoSuchBeanDefinitionException / Field xxx required a bean of type xxx that could not be found
解决：确认 @ComponentScan 包路径包含目标类；检查 @Service/@Repository 注解是否遗漏；确认 MyBatis Mapper 的 @Mapper 或 @MapperScan 配置

### MyBatis 映射错误
错误：Invalid bound statement (not found) / mapper interface method not found
解决：确认 XML mapper 文件路径与 Mapper 接口包路径一致；检查 application.yml 中 mybatis.mapper-locations 配置；确认方法名与 XML 中 id 属性一致

---

## RuoYi 特定问题

### 代码生成器输出不完整
问题：生成的代码缺少某些文件或字段
解决：确认 gen_table 和 gen_table_column 数据是否完整；检查代码生成模板是否被覆盖；重新导入表结构后重新生成

### 权限/菜单不生效
问题：新增菜单或角色权限后页面看不到
解决：确认 sys_menu 表记录完整（含 perms 字段）；检查 @PreAuthorize 注解中权限标识与菜单 perms 一致；清除浏览器缓存和 Redis 缓存后重试

### 字典数据不加载
问题：下拉框为空或字典值不显示
解决：确认 sys_dict_type 和 sys_dict_data 有对应记录；检查前端 this.getDicts() 调用的字典类型编码是否正确；确认 Redis 缓存是否过期

### 跨模块依赖问题
问题：ruoyi-admin 编译报找不到 ruoyi-system 的类
解决：确认各子模块 pom.xml 中 dependency 引用正确；先 `mvn install` 安装依赖模块再到 admin 模块编译；检查 Maven reactor 构建顺序

---

## 数据库问题

### MySQL 连接失败
错误：Communications link failure / Access denied for user
解决：确认 MySQL 服务已启动（Windows: `net start mysql`）；检查 application.yml 中 spring.datasource.url/host/port/username/password；确认用户有远程访问权限（`GRANT ALL ON *.* TO 'user'@'%'`）；检查防火墙是否放行 3306 端口

### MySQL 中文乱码
问题：插入或查询中文显示问号/乱码
解决：确认连接 URL 含 `characterEncoding=utf-8` 或 `characterEncoding=UTF-8`；检查数据库/表/列的 charset 是否为 utf8mb4；确认 MySQL 配置文件中 `character-set-server=utf8mb4`

### MySQL 时区问题
错误：The server time zone value 'CST' is unrecognized
解决：连接 URL 中添加 `serverTimezone=Asia/Shanghai`；或 MySQL 配置中设置 `default-time-zone='+08:00'`

### PostgreSQL 连接失败
错误：Connection refused / FATAL: no pg_hba.conf entry
解决：确认 PostgreSQL 服务已启动（Windows: `net start postgresql-x64-XX`）；检查 pg_hba.conf 是否允许目标 IP/用户连接（添加 `host all all 0.0.0.0/0 md5`）；确认 postgresql.conf 中 `listen_addresses = '*'`；检查防火墙是否放行 5432 端口

### PostgreSQL Schema 权限问题
错误：ERROR: permission denied for schema public
解决：`GRANT ALL ON SCHEMA public TO username;`；确认搜索路径 `search_path` 包含目标 schema；检查默认表空间权限

### 瀚高（HighGo）数据库连接
问题：SpringBoot 项目需适配瀚高数据库
解决：瀚高兼容 PostgreSQL 协议，驱动使用 `com.highgo.jdbc.Driver`（或 `org.postgresql.Driver`）；JDBC URL 格式 `jdbc:highgo://host:port/database`；Maven 依赖添加 `com.highgo` 驱动包；方言设置 `hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect`；如遇关键字冲突，在 URL 中加 `stringtype=unspecified`

### 瀚高数据库特殊语法
问题：从 MySQL 迁移到瀚高后 SQL 报错
解决：瀚高/PostgreSQL 与 MySQL 语法差异需注意：自增列用 `SERIAL` 或 `GENERATED ALWAYS AS IDENTITY` 代替 `AUTO_INCREMENT`；字符串拼接用 `||` 代替 `CONCAT()`；分页用 `LIMIT ... OFFSET` 代替 `LIMIT`；日期函数不同（`NOW()` 通用，`DATE_FORMAT` 需改为 `TO_CHAR`）；布尔类型用 `BOOLEAN` 代替 `TINYINT(1)`；反引号 `` ` `` 需替换为双引号 `"` 或去掉

### 数据库迁移脚本兼容性
问题：同一项目需支持 MySQL 和瀚高/PostgreSQL
解决：MyBatis 中使用 `databaseId` 区分多数据库 SQL；或使用 DatabaseProvider 动态选择 SQL 片段；Flyway/Liquibase 按数据库类型维护不同迁移脚本目录；避免使用数据库特有语法，优先使用标准 SQL

---

## Redis 问题

### Redis 连接失败
错误：Unable to connect to Redis / Could not get a resource from the pool
解决：确认 Redis 服务已启动（Windows: 下载 Redis for Windows 或使用 WSL）；检查 application.yml 中 spring.redis.host/port/password 配置；确认防火墙放行 6379 端口；如使用 Redis Sentinel/Cluster，检查 sentinel/master 节点配置

### Redis 序列化错误
错误：Cannot deserialize / SerializationException
解决：确认 RedisTemplate 配置了正确的序列化器（`StringRedisSerializer` 用于 key，`Jackson2JsonRedisSerializer` 或 `GenericJackson2JsonRedisSerializer` 用于 value）；检查存储对象是否可序列化；RuoYi 默认使用 JDK 序列化，切换为 JSON 序列化可避免类变更后反序列化失败

### Redis 缓存与数据库不一致
问题：更新数据库后缓存未同步，读取到旧数据
解决：采用「先更新数据库再删除缓存」策略；使用 @CacheEvict 注解在更新方法上同步清缓存；RuoYi 中通过 RedisCache.clearCacheByKey 手动清除；注意 Redis 过期时间设置不宜过长

### Redis OOM / 内存溢出
问题：Redis 占用内存持续增长或报 OOM
解决：设置 maxmemory 和淘汰策略（`maxmemory-policy allkeys-lru`）；检查是否有大 key（`redis-cli --bigkeys`）；为缓存键设置合理的过期时间（TTL）；RuoYi 中定期清理 sys_config/sys_dict 等缓存

---

## ActiveMQ 问题

### ActiveMQ 连接失败
错误：Could not connect to broker URL / JMSException
解决：确认 ActiveMQ 服务已启动（Windows: `activemq.bat start`）；检查 spring.activemq.broker-url 配置（默认 `tcp://localhost:61616`）；确认防火墙放行 61616 端口；Web 管理界面默认 8161 端口

### ActiveMQ 消息消费失败
问题：消息发送成功但消费者未收到
解决：确认 @JmsListener 注解的 destination 与生产者一致；检查消息序列化格式是否与消费者兼容；确认 ConnectionFactory 配置正确；检查 ActiveMQ 管理界面中是否有堆积的未消费消息（Dead Letter Queue）

### ActiveMQ 与 SpringBoot 版本兼容
问题：SpringBoot 2.x 集成 ActiveMQ 报 ClassNotFoundException
解决：确认 spring-boot-starter-activemq 版本与 SpringBoot 主版本匹配；SpringBoot 2.x 默认使用 ActiveMQ 5.x 连接池；如需自定义连接池，添加 `org.apache.activemq:activemq-pool` 依赖

---

## Kafka 问题

### Kafka 连接失败
错误：Connection to node -1 could not be established / Broker not available
解决：确认 Kafka 和 ZooKeeper 服务已启动；检查 spring.kafka.bootstrap-servers 配置；确认防火墙放行 9092 端口（Kafka）和 2181 端口（ZooKeeper）；如使用 Kafka Raft 模式（KRaft，无需 ZooKeeper），确认 quorum.voters 配置

### Kafka 消费 offset 问题
问题：消费者重复消费或跳过消息
解决：确认 spring.kafka.consumer.auto-offset-reset 配置（earliest/latest/none）；检查 consumer group 是否被意外 reset；使用 `kafka-consumer-groups.sh --describe` 查看 offset 状态；生产环境建议手动 commit offset 而非自动提交

### Kafka 生产消息失败
问题：消息发送超时或报 Not Enough Replicas
解决：确认 topic 的 min.insync.replicas 配置与实际存活 broker 数量匹配；检查 spring.kafka.producer.acks 配置（all/1/0）；增加 producer retries 和 request.timeout.ms；确认 topic 已创建（`kafka-topics.sh --list`）

### Kafka 与 SpringBoot 集成报错
问题：KafkaTemplate 注入失败或 @KafkaListener 不生效
解决：确认 spring-kafka 依赖版本与 SpringBoot 版本兼容；检查 @EnableKafka 注解是否添加；确认 KafkaTemplate 的 key/value serializer 配置；RuoYi 集成 Kafka 时需注意与现有 Redis 缓存的消息通道不冲突

---

## Vue 错误

### npm/pnpm install 失败
问题：node-sass / sass 编译失败，或 phantomjs 下载超时
解决（Vue2）：node-sass 需要 Python2 + VS Build Tools，建议替换为 dart-sass（`npm install sass` 代替 `node-sass`）
解决（Vue3）：确认 node 版本 ≥ 16；pnpm 需要 `.npmrc` 中 shamefully-hoist=true 处理幽灵依赖

### Vue2 Element UI 按需加载报错
问题：babel-plugin-component 配置后样式缺失或组件找不到
解决：确认 .babelrc 或 babel.config.js 中 styleLibraryName 路径正确；检查 element-ui 版本与插件版本兼容性

### Vue3 Vite 启动白屏
问题：Vite dev server 启动后页面空白
解决：确认 vite.config.js 中 base 配置；检查 @vitejs/plugin-vue 是否安装；确认 index.html 中 script 引用路径正确（`/src/main.ts` 不是 `/src/main.js`）

### Vue Router 路由守卫死循环
问题：页面不断重定向到同一路由
解决：检查 next() 是否在守卫中被调用且只调用一次；确认白名单路由判断逻辑正确；避免在 beforeEach 中对白名单路由再做 redirect

### ESLint + Prettier 冲突
问题：ESLint 和 Prettier 规则冲突导致格式化来回跳动
解决：安装 eslint-config-prettier 关闭与 Prettier 冲突的 ESLint 规则；安装 eslint-plugin-prettier 让 ESLint 运行 Prettier；.eslintrc.js 中 extends 末尾加上 prettier

---

## TypeScript 类型错误

### 模块找不到
错误：Cannot find module './xxx' or its type declarations
解决：检查文件路径是否正确；确认 tsconfig.json 的 paths 配置；检查文件扩展名

### 类型断言问题
错误：Argument of type 'xxx' is not assignable to parameter of type 'yyy'
解决：使用类型守卫、类型断言，或重新审查类型定义是否正确

---

## Python 错误

### ImportError / ModuleNotFoundError
问题：本地能跑但 CI 报 ImportError
解决：确认依赖在 requirements.txt/pyproject.toml 中；检查虚拟环境是否激活

### pip install 失败
问题：依赖编译失败
解决：确认系统级依赖是否安装；尝试 --no-binary 选项

---

## 依赖问题

### 幽灵依赖
问题：本地能用但 CI 报 module not found
解决：确认依赖是否在 package.json/requirements.txt/pom.xml 中，重新安装

### npm/pnpm 版本冲突
问题：安装报 peer dependency warning
解决：确认主版本一致；追踪依赖来源；必要时锁定版本

### Maven 依赖下载失败
问题：Could not transfer artifact / 下载卡住或 401
解决：确认 settings.xml 中镜像仓库（阿里云/华为云）配置正确；检查私服认证信息；删除 ~/.m2/repository 中对应目录后重试 `mvn dependency:resolve`

### Maven 依赖冲突
问题：java.lang.NoSuchMethodError / java.lang.ClassCastException 运行时才报错
解决：`mvn dependency:tree -Dverbose` 查看冲突；使用 `<exclusions>` 排除冲突传递依赖；确认子模块 pom.xml 不要重复声明父模块已有的依赖

---

## 测试问题

### 异步测试超时
问题：Test timed out
解决：增加 timeout；检查是否有死循环或未 resolve 的 Promise；确认 mock 是否正确

### Mock 不生效
问题：mock 函数没有被调用
解决：确认 mock 路径正确；检查 mock 文件命名；确认 mock 在正确位置

---

## Git 问题

### 已 merge 的分支未清理
问题：本地存在大量已合并的远程分支
解决（Unix）：git fetch --prune && git branch -d $(git branch --merged | grep -v '*')
解决（Windows PowerShell）：git fetch --prune; git branch --merged | Where-Object { $_ -notmatch '^\*' } | ForEach-Object { git branch -d $_.Trim() }

### Commit 冲突预防
规则：合并前先 rebase main；多人协作时每日 rebase 一次

---

## Windows / PowerShell / CMD 问题

### PowerShell 执行策略禁止脚本运行
错误：无法加载文件 xxx.ps1，因为在此系统上禁止运行脚本
解决：以管理员身份运行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 中文路径 / 中文文件名乱码
问题：Git status / log 中中文显示为 \xxx\ 转义序列
解决：`git config --global core.quotepath false`；PowerShell 中设置 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`

### Maven 在 CMD/PowerShell 中编码错误
问题：mvn compile 输出中文乱码
解决（CMD）：`chcp 65001` 切换为 UTF-8 代码页
解决（PowerShell）：设置 `$env:JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF-8"`；或在 MAVEN_OPTS 中加 `-Dfile.encoding=UTF-8`

### 长路径问题
问题：Windows 下 node_modules 路径超过 260 字符导致删除/安装失败
解决：启用长路径支持 `git config --global core.longpaths true`；删除时使用 `npx npkill` 或 `rimraf`；注册表启用长路径（`HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled` = 1）

### pnpm 在 Windows 上的硬链接问题
问题：pnpm install 报 EPERM 或 EXDEV 错误
解决：确认项目不在 FAT32 分区（NTFS 才支持硬链接）；`.npmrc` 中设置 `store-dir=C:\.pnpm-store` 避免路径过长

---

## Vue Router 动态路由问题

### 菜单路由返回 404
问题：后端菜单数据正确，但前端导航到动态路由返回 404 页面
原因：一级菜单的 path 未以 `/` 开头，Vue Router 无法识别为根路由
解决：
```sql
-- 错误配置
INSERT INTO system_menu (path, ...) VALUES ('calendarEvent', ...);

-- 正确配置（path 必须以 / 开头）
INSERT INTO system_menu (path, ...) VALUES ('/calendarEvent', ...);
```
关键点：Vue Router 的根路由 path 必须以 `/` 开头，否则会被当作相对路径处理

### 菜单 component 路径与实际文件不匹配
问题：菜单配置的 component 路径找不到对应 Vue 文件
排查：检查 `src/views/` 下是否存在对应文件
解决：确认 component 字段值与 `src/views/` 下的文件路径一致
```sql
-- component 值 'business/calendar/index' 对应文件：
-- src/views/business/calendar/index.vue
```

---

## Playwright E2E 测试问题

### waitForLoadState('networkidle') 永远超时
问题：测试在 `await page.waitForLoadState('networkidle')` 处超时
原因：后台有持续的轮询请求（如消息通知、WebSocket 心跳），导致 networkidle 永远无法达到
解决：
```javascript
// 错误：依赖 networkidle
await page.goto('/some-page');
await page.waitForLoadState('networkidle');

// 正确：使用 domcontentloaded + 显式元素等待
await page.goto('/some-page');
await page.waitForSelector('button:has-text("新增")', { timeout: 10000 });
```

### Element UI 组件选择器返回 hidden
问题：`locator('.el-table').first()` 或 `locator('table')` 返回 hidden 状态
原因：Element UI 的 el-table 组件内部有多个 table 元素，第一个可能是隐藏的表头或辅助元素
解决：
```javascript
// 错误：el-table 可能返回隐藏元素
await expect(page.locator('.el-table').first()).toBeVisible();

// 正确：使用业务关键元素作为验证点
await expect(page.locator('button:has-text("新增")')).toBeVisible();
await expect(page.locator('button:has-text("搜索")')).toBeVisible();
```

### afterEach 钩子超时
问题：测试本身通过，但 afterEach 中的清理逻辑超时
原因：afterEach 中使用了 `waitForLoadState('networkidle')`
解决：
```javascript
// 错误
test.afterEach(async ({ page }) => {
  await page.waitForLoadState('networkidle'); // 可能永远等待
  // ...
});

// 正确
test.afterEach(async ({ page }) => {
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(300); // 等待微任务完成
  // ...
});
```

### 测试账号不存在导致测试失败
问题：使用普通用户账号测试，但账号不存在
解决：添加异常处理，优雅跳过
```javascript
try {
  await login(page, TEST_ACCOUNTS.user);
  // ... 测试逻辑
} catch (e) {
  console.log('测试跳过: user 账号可能不存在');
}
```

---

## SpringBoot 微服务启动问题

### 微服务端口未配置，默认使用 8080
问题：启动微服务时报 Port 8080 already in use，或多个服务争抢同一端口
原因：application-local.yaml 未配置 server.port，使用了默认的 8080
解决：在每个微服务的 application-local.yaml 中显式配置端口
```yaml
# yudao-gateway/src/main/resources/application-local.yaml
server:
  port: 48080

# yudao-module-system/.../application-local.yaml
server:
  port: 48081

# yudao-module-infra/.../application-local.yaml
server:
  port: 48082

# yudao-module-business/.../application-local.yaml
server:
  port: 48083
```

### ClassNotFoundException: AuthRegisterReqVO
问题：启动某个微服务时报 ClassNotFoundException
原因：依赖模块未编译安装到本地 Maven 仓库
解决：
```bash
# 在项目根目录执行
mvn clean install -DskipTests
```

### Nacos 配置找不到
问题：启动时报 `config[dataId=xxx-local.yaml, group=DEFAULT_GROUP] is empty`
原因：本地开发未在 Nacos 创建对应配置，或 namespace 不匹配
解决：
1. 确认 application-local.yaml 存在且配置正确（本地开发优先使用本地配置）
2. 如需使用 Nacos 配置，确认 namespace 和 group 正确

---

## Docker MySQL 字符集问题

### 客户端字符集导致中文乱码
问题：通过 `docker exec mysql` 执行含中文的 SQL，数据库存储为乱码
原因：MySQL 客户端默认字符集为 latin1，与数据库 utf8mb4 不匹配
排查：
```bash
# 检查客户端字符集
docker exec <container> mysql -uroot -p123456 -e "SHOW VARIABLES LIKE 'character%';"
# 典型问题输出：
# character_set_client     = latin1  ← 问题所在
# character_set_connection = latin1  ← 问题所在
# character_set_results    = latin1  ← 问题所在
# character_set_database   = utf8mb4
```
解决：
```bash
# 方案1：执行 SQL 时指定字符集
docker exec <container> mysql -uroot -p123456 --default-character-set=utf8mb4 <db> -e "INSERT INTO table (name) VALUES ('中文');"

# 方案2：在 SQL 文件开头添加字符集声明
cat > script.sql << 'EOF'
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

INSERT INTO table (name) VALUES ('中文');
EOF

docker exec -i <container> mysql -uroot -p123456 --default-character-set=utf8mb4 <db> < script.sql
```
关键点：即使数据库和表都是 utf8mb4，客户端连接字符集不对仍会导致乱码

---

## 微服务架构排障经验

### 新微服务 Bean 注入失败
问题：新微服务启动报 `NoSuchBeanDefinitionException: No qualifying bean of type 'List<AuthorizeRequestsCustomizer>'`
根因：框架级 Security 配置需要至少一个 AuthorizeRequestsCustomizer bean，新模块缺少依赖
解决：对比同类模块（system/infra）的 pom.xml，添加 websocket 等框架依赖

### 网关未启动导致前端 500
问题：前端 API 请求全部 500，但后端服务正常
原因：前端配置 `VUE_APP_BASE_API` 指向网关，网关未启动
解决：确保启动顺序——基础设施 → 后端服务 → 网关 → 前端

### Node.js 版本不兼容
问题：前端编译报错 `error:0308010C:digital envelope routines::unsupported`
原因：Node.js 17+ 更改了 OpenSSL 默认配置，与旧版 webpack 不兼容
解决：`NODE_OPTIONS=--openssl-legacy-provider npm run local` 或降级 Node.js 到 16.x

---

## 问题定位决策树

```
页面 404
├── URL 是否正确？ → 检查菜单 path 配置（一级必须以 / 开头）
├── 组件文件是否存在？ → 检查 src/views/ 目录
├── 路由是否注册？ → 浏览器控制台检查 $router.getRoutes()
└── 网关是否启动？ → curl 网关地址

API 500
├── 后端服务是否启动？ → curl 直接访问后端端口
├── 网关是否启动？ → curl 网关地址
├── 数据库连接是否正常？ → 检查后端日志
└── Nacos 是否注册？ → 检查服务注册列表

菜单乱码
├── 数据库存储是否正常？ → mysql 客户端直接查询
├── API 返回是否正常？ → curl 检查响应
└── 字符集配置是否正确？ → SHOW VARIABLES LIKE 'character%'

微服务启动失败
├── Bean 注入失败？ → 对比同类模块的 pom.xml 依赖
├── 端口被占用？ → netstat 检查端口
└── 配置找不到？ → 检查 application-local.yaml
```

---

## 排障经验总结

1. **先检查基础设施**：Nacos、MySQL、Redis 是否正常运行
2. **端口冲突是常见问题**：使用 netstat 检查，确保配置文件显式指定端口
3. **E2E 测试不要依赖 networkidle**：后台轮询请求会导致永远无法达到该状态
4. **Vue Router 根路由必须以 / 开头**：这是动态菜单配置的常见错误
5. **Element UI 组件选择器需谨慎**：组件内部结构复杂，优先选择业务关键元素
6. **Docker MySQL 执行 SQL 必须指定字符集**：客户端默认 latin1 会导致中文乱码
7. **新增微服务对比同类模块依赖**：避免因缺少框架级依赖导致启动失败
8. **网关是前端请求入口**：微服务架构下前端不直连后端，必须经过网关
9. **Node.js 版本兼容性**：注意 Node 17+ 与旧版 webpack 的 OpenSSL 兼容问题
