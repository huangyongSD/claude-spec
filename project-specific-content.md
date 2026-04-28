# 项目特定内容清单（排除通用项后）

> 分析范围：所有 Claude 配置文件（CLAUDE.md + .claude/ 目录下的 43 个文件）
> 排除规则：构建命令、权限指令/注解、Claude 配置文件名、密钥管理方式、通用规则、通用配置、通用 hooks、通用 skills、通用模板均为通用项，不列入

---

## 排除清单（通用项，不计入项目特定）

| 类别 | 排除原因 |
|------|---------|
| 构建命令（`mvn` / `yarn` / `npm` 等） | 通用构建工具命令 |
| 前端权限指令（`v-hasPermi`） | 芋道框架内置指令，属于框架通用 |
| 后端注解（`@PreAuthorize` / `@ss.hasPermission`） | 芋道框架内置注解，属于框架通用 |
| Claude 配置文件名（`sds-*` / `sda-*` / `db-query.py` / `secrets-sync.py`） | 配置层命名，与业务无关 |
| 密钥管理方式（`{{DB_MASTER_PASSWORD}}` 占位符 / `secrets.json` 结构） | 通用密钥管理模式 |
| troubleshooting.md 全部 | 通用排障知识库 |
| rules/security.md / frontend.md / governance.md / testing.md | 通用编码规则 |
| settings.json | 通用 Claude 配置 |
| hooks/（除 MySQL 相关外） | 通用安全 hook（危险命令检测、敏感信息检测等） |
| skills/（除 SQL 相关外） | 通用工作流编排 Skill |
| templates/spec/（4 个模板） | 通用 Spec 模板 |

---

## 1. CLAUDE.md（项目根）

| 项目特定内容 | 说明 |
|---|---|
| `yudao（芋道）` 项目名称 | 绑定芋道项目 |
| `SpringBoot 2.7.18 + MyBatis-Plus 3.5.15 + JDK8` | 芋道后端技术栈版本号 |
| `Vue2 2.7.14 + Element-UI 2.15.14` | 芋道前端技术栈版本号 |
| `MySQL 8.0` 数据库 | 芋道数据库类型及版本 |
| `Redis + Redisson` 中间件 | 芋道中间件选型 |
| `yudao-boot-mini/` 目录结构 | 芋道项目目录名 |
| `yudao-server` / `yudao-framework` / `yudao-module-system` 等 | 芋道模块名 |
| `controller/admin/app` 子包结构 | 芋道 Controller 分层规范 |
| `sql/mysql/` 目录 | 芋道 SQL 脚本存放路径 |
| `yudao-server/.../application*.yaml` 配置路径 | 芋道配置文件路径 |
| `yudao-ui-admin/src/views/` / `src/router/` | 芋道前端项目名及目录路径 |

## 2. .claude/knowledge/structure.md

| 项目特定内容 | 说明 |
|---|---|
| `yudao-boot-mini/` 完整目录树 | 芋道项目目录名 |
| `yudao-spring-boot-starter-web/security/mybatis` | 芋道框架 starter 名 |
| `yudao-module-system/` / `yudao-module-infra/` | 芋道模块名 |
| `controller/admin/` / `controller/app/` | 芋道 API 分层规范 |
| `dal/dataobject/` / `dal/mysql/` / `convert/` | 芋道包结构 |
| `yudao-ui-admin/` 前端目录 | 芋道前端项目名 |
| `src/api/` / `src/views/` / `src/components/` 等 | 芋道前端子目录 |
| `sql/mysql/postgresql/oracle/dm/kingbase/` | 芋道多数据库脚本目录 |
| 修改导航表（每个路径都绑定芋道） | 芋道文件定位映射 |
| `sys_menu` 表 | 芋道菜单系统表名 |
| ADR-001/002/003 架构决策 | 芋道技术选型决策（选 SpringBoot/Vue2/MyBatis-Plus 的具体原因） |

## 3. .claude/knowledge/dbinfo.md

| 项目特定内容 | 说明 |
|---|---|
| `-- DB_TYPE: MySQL 8.0` 标注要求 | 芋道目标数据库 |
| MySQL vs PostgreSQL/瀚高 方言对照 | 芋道多数据库适配需求 |
| 反引号 `` ` `` vs 双引号 `"` 标识符 | 芋道 SQL 标识符规范 |
| `databaseId` 多数据库区分 | 芋道 MyBatis 多库方案 |

## 4. .claude/knowledge/troubleshooting.md

| 项目特定内容 | 说明 |
|---|---|
| "yudao（芋道）特定问题" 整节 | 芋道项目特有的排障经验 |
| `gen_table` / `gen_table_column` 代码生成器 | 芋道代码生成器表名 |
| `sys_menu` / `sys_dict_type` / `sys_dict_data` | 芋道系统表名 |
| `RedisCache.clearCacheByKey` | 芋道缓存清除方法名 |
| `yudao-server` 编译问题 / 跨模块依赖 | 芋道模块依赖排障 |
| `AuthorizeRequestsCustomizer` bean 问题 | 芋道框架 Security 配置类名 |
| `VUE_APP_BASE_API` 网关配置 | 芋道前端环境变量名 |
| `server.port: 48080~48083` | 芋道微服务端口分配方案 |
| 菜单 SQL `INSERT INTO system_menu` 示例 | 芋道菜单表结构及字段 |

## 5. .claude/hooks/（MySQL 相关部分）

| 项目特定内容 | 说明 |
|---|---|
| `mysql|psql|sqlplus` 写操作阻断规则 | 芋道数据库防护策略（仅 MySQL 部分项目特定） |

> 注：hooks 中其余内容（危险命令检测、敏感信息检测、IP/密码 pattern 等）均为通用安全 hook，已排除。

## 6. .claude/tools/db-query.py

| 项目特定内容 | 说明 |
|---|---|
| `pymysql` 连接 | 芋道使用 MySQL + pymysql |
| `db_master_*` / `db_slave_*` 字段名 | 芋道数据库配置字段名（master/slave 双数据源） |
| `charset: utf8mb4` | 芋道字符集设定 |

## 7. .claude/tools/secrets-sync.py

| 项目特定内容 | 说明 |
|---|---|
| `yudao-boot-mini/yudao-server/...application-*.yaml` 搜索路径 | 芋道配置文件路径 |
| `spring.datasource.dynamic.datasource.master/slave` YAML 结构 | 芋道（芋道多数据源配置路径） |
| `spring.redis` / `spring.data.redis` | 芋道 Redis 配置路径 |
| `spring.rabbitmq` | 芋道 RabbitMQ 配置 |
| `JDBC_PATTERN = jdbc:mysql://` | 芋道 JDBC URL 格式 |

> 注：`{{DB_MASTER_URL}}` 等 16 个占位符映射属于通用密钥管理方式，已排除。

## 8. .claude/skills/（SQL 相关部分）

| 项目特定内容 | 说明 |
|---|---|
| `SET NAMES utf8mb4` / `-- DB_TYPE: MySQL 8.0` | 芋道 SQL 规范要求 |

> 注：skills 中其余内容（SDA 编排流程、评审机制、质量门禁、编译验证等）均为通用工作流，已排除。

---

## 绑定维度汇总（排除通用项后）

| 维度 | 具体内容 | 涉及文件数 |
|------|---------|-----------|
| **项目名称与模块名** | `yudao` / `yudao-boot-mini` / `yudao-ui-admin` / `yudao-server` / `yudao-framework` / `yudao-module-system` 等 | 6 |
| **技术栈版本号** | `SpringBoot 2.7.18` / `MyBatis-Plus 3.5.15` / `JDK8` / `Vue2 2.7.14` / `Element-UI 2.15.14` / `MySQL 8.0` | 3 |
| **数据库相关** | `pymysql` / `master/slave 双数据源` / `utf8mb4` / `jdbc:mysql://` / `sys_menu` / `sys_dict_*` / `gen_table` / `databaseId` / `-- DB_TYPE: MySQL 8.0` / `SET NAMES utf8mb4` | 5 |
| **目录结构与路径** | `controller/admin/app` / `dal/dataobject/mysql` / `convert` / `sql/mysql/` / `yudao-server/...application*.yaml` / `spring.datasource.dynamic.datasource.*` | 4 |
| **芋道特有类/方法** | `RedisCache.clearCacheByKey` / `AuthorizeRequestsCustomizer` / `VUE_APP_BASE_API` / `gen_table` / `gen_table_column` / `server.port: 48080~48083` | 2 |
| **架构决策** | ADR-001（选 SpringBoot）/ ADR-002（选 Vue2）/ ADR-003（选 MyBatis-Plus） | 1 |