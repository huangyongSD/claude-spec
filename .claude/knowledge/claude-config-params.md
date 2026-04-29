---
description: Claude 配置参数映射表（项目特定内容参数化参考）
---

# Claude 配置参数映射表

> 本文件定义所有 Claude 配置文件中项目特定内容的参数化方案。
> 配置文件中使用 `{{PARAM}}` 占位符，新项目初始化时替换为实际值。

## A. 技术栈参数

| 参数名 | 当前值（芋道） | 说明 |
|--------|--------------|------|
| `{{PROJECT_NAME}}` | yudao（芋道） | 项目名称 |
| `{{BACKEND_TECH}}` | SpringBoot 2.7.18 + MyBatis-Plus 3.5.15 + JDK8 | 后端技术栈描述 |
| `{{FRONTEND_TECH}}` | Vue2 2.7.14 + Element-UI 2.15.14 | 前端技术栈描述 |
| `{{DATABASE}}` | MySQL 8.0 | 目标数据库 |
| `{{MIDDLEWARE}}` | Redis + Redisson（缓存/分布式锁） | 中间件 |
| `{{BACKEND_BUILD_CMD}}` | `mvn clean compile` | 后端编译命令 |
| `{{BACKEND_TEST_CMD}}` | `mvn test` | 后端测试命令 |
| `{{FRONTEND_BUILD_CMD}}` | `yarn build:prod` | 前端构建命令 |
| `{{FRONTEND_LINT_CMD}}` | `yarn lint` | 前端 Lint 命令 |
| `{{FRONTEND_PKG_MANAGER}}` | yarn | 前端包管理器 |
| `{{BACKEND_PKG_MANAGER}}` | mvn | 后端包管理器 |

## B. 框架特定类名/注解

| 参数名 | 当前值（芋道） | 说明 |
|--------|--------------|------|
| `{{RESPONSE_WRAPPER}}` | `CommonResult<T>` | 统一响应包装类 |
| `{{PAGE_RESULT_WRAPPER}}` | `PageResult<T>` | 分页结果包装类 |
| `{{PAGE_PARAM_BASE}}` | `PageParam` | 分页参数基类 |
| `{{DO_BASE_CLASS}}` | `BaseDO` | DO 基类（含审计字段） |
| `{{MAPPER_BASE_CLASS}}` | `BaseMapper<XxxDO>` | Mapper 基类 |
| `{{QUERY_WRAPPER_CLASS}}` | `LambdaQueryWrapperX<XxxDO>` | 扩展查询包装类 |
| `{{ENCRYPT_HANDLER_CLASS}}` | `EncryptTypeHandler.class` | 加密字段处理器 |
| `{{BIZ_EXCEPTION_CLASS}}` | `BizException` | 业务异常类 |
| `{{TEST_EXCEPTION_CLASS}}` | `ServiceException.class` | 测试断言异常类 |
| `{{PERMISSION_EXPRESSION}}` | `@ss.hasPermission('xxx:action')` | 权限 EL 表达式格式 |
| `{{PERMISSION_ANNOTATION}}` | `@PreAuthorize` | 权限注解 |
| `{{VO_SAVE_REQ_NAMING}}` | `XxxSaveReqVO` | 新增/更新请求 VO 命名 |
| `{{VO_PAGE_REQ_NAMING}}` | `XxxPageReqVO` | 分页请求 VO 命名 |
| `{{VO_RESP_NAMING}}` | `XxxRespVO` | 响应 VO 命名 |
| `{{SERVICE_INTERFACE_NAMING}}` | `XxxService` | Service 接口命名 |
| `{{SERVICE_IMPL_NAMING}}` | `XxxServiceImpl` | Service 实现命名 |
| `{{TRANSACTION_ANNOTATION}}` | `@Transactional(rollbackFor = Exception.class)` | 事务注解 |
| `{{DO_TABLE_ANNOTATION}}` | `@TableName` | 表名注解 |
| `{{DO_KEY_ANNOTATION}}` | `@TableId` | 主键注解 |
| `{{DO_KEYSEQ_ANNOTATION}}` | `@KeySequence` | 主键序列注解 |
| `{{NULL_SAFE_COLLECTIONS}}` | `CollectionUtils.isEmpty()` / `Collections.emptyList()` | 空安全集合工具 |
| `{{SWAGGER_ANNOTATIONS}}` | `@Schema` / `@Operation` | Swagger 注解 |

## C. 前端框架特定

| 参数名 | 当前值（芋道） | 说明 |
|--------|--------------|------|
| `{{FE_PERMISSION_DIRECTIVE}}` | `v-hasPermi` | 权限指令名 |
| `{{FE_LAYOUT_WRAPPER}}` | `ContentWrap` | 布局包装组件 |
| `{{FE_PAGINATION_COMPONENT}}` | `Pagination` | 分页组件 |
| `{{FE_REQUEST_UTIL}}` | `@/utils/request` | HTTP 请求工具路径 |
| `{{FE_MODAL_SUCCESS}}` | `this.$modal.msgSuccess` | 成功提示方法 |
| `{{FE_MODAL_CONFIRM}}` | `this.$modal.confirm` | 确认弹窗方法 |
| `{{FE_PAGE_NO_PARAM}}` | `pageNo` | 分页页码参数名 |
| `{{FE_PAGE_SIZE_PARAM}}` | `pageSize` | 分页大小参数名 |
| `{{FE_FORM_DIALOG_STATUS}}` | `dialogStatus` | 表单弹窗状态变量名 |
| `{{FE_XSS_FILTER}}` | `DOMPurify` | XSS 过滤工具 |
| `{{FE_VUE_VERSION}}` | Vue2 | Vue 版本 |
| `{{FE_UI_LIBRARY}}` | Element-UI | UI 组件库 |
| `{{FE_STATE_MANAGEMENT}}` | Vuex | 状态管理方案 |
| `{{FE_SCRIPT_TYPE}}` | JavaScript | 前端语言（非 TypeScript） |

## D. 项目目录结构

| 参数名 | 当前值（芋道） | 说明 |
|--------|--------------|------|
| `{{SERVER_MODULE}}` | `yudao-server/` | 主服务器模块目录 |
| `{{FRAMEWORK_MODULE}}` | `yudao-framework/` | 框架层目录（禁止修改） |
| `{{DEPENDENCIES_MODULE}}` | `yudao-dependencies/` | BOM 依赖管理目录（禁止修改） |
| `{{SYSTEM_MODULE}}` | `yudao-module-system/` | 系统功能模块目录 |
| `{{INFRA_MODULE}}` | `yudao-module-infra/` | 基础设施模块目录 |
| `{{UI_ADMIN_MODULE}}` | `yudao-ui-admin/` | 前端管理后台目录 |
| `{{CONTROLLER_ADMIN_PATH}}` | `controller/admin/` | 管理后台 API 子包 |
| `{{CONTROLLER_APP_PATH}}` | `controller/app/` | 移动端 API 子包 |
| `{{SERVICE_PATH}}` | `service/` | 业务逻辑包 |
| `{{DO_PATH}}` | `dal/dataobject/` | DO 实体包 |
| `{{MAPPER_PATH}}` | `dal/mysql/` | Mapper 包 |
| `{{CONVERT_PATH}}` | `convert/` | 对象转换包 |
| `{{VO_PATH}}` | `vo/` | VO 包 |
| `{{FE_API_PATH}}` | `src/api/xxx/index.js` | 前端 API 定义路径模式 |
| `{{FE_VIEW_PATH}}` | `src/views/xxx/` | 前端页面路径模式 |
| `{{FE_ROUTER_PATH}}` | `src/router/modules/xxx.js` | 前端路由路径模式 |
| `{{FE_STORE_PATH}}` | `src/store/` | 前端状态管理路径 |
| `{{FE_DIRECTIVE_PATH}}` | `src/directive/` | 前端自定义指令路径 |
| `{{SQL_PATH}}` | `sql/mysql/` | SQL 脚本目录 |
| `{{CONFIG_PATH}}` | `application*.yaml` | 配置文件路径模式 |

## E. 安全/占位符体系

| 参数名 | 当前值（芋道） | 说明 |
|--------|--------------|------|
| `{{SQL_CHARSET_DECLARATION}}` | `SET NAMES utf8mb4; SET CHARACTER SET utf8mb4;` | SQL 字符集声明 |
| `{{SQL_DB_TYPE_TAG}}` | `-- DB_TYPE: MySQL 8.0` | SQL 数据库类型标注 |
| `{{DO_AUDIT_FIELDS}}` | `creator, create_time, updater, update_time, deleted` | DO 审计字段列表 |
| `{{DO_LOGICAL_DELETE_FIELD}}` | `deleted` | 逻辑删除字段名 |
| `{{DO_LOGICAL_DELETE_TYPE}}` | `BIT(1)` / `tinyint` | 逻辑删除字段类型 |
| `{{MYBATIS_PARAM_BINDING}}` | `#{}` | MyBatis 参数化绑定符号 |
| `{{MYBATIS_LITERAL_BINDING}}` | `${}` | MyBatis 字面量绑定符号（禁止使用） |

## F. 项目特定业务知识

| 参数名 | 当前值（芋道） | 说明 |
|--------|--------------|------|
| `{{MENU_TABLE}}` | `sys_menu` | 菜单配置表名 |
| `{{DICT_TYPE_TABLE}}` | `sys_dict_type` | 字典类型表名 |
| `{{DICT_DATA_TABLE}}` | `sys_dict_data` | 字典数据表名 |
| `{{REDIS_CACHE_CLEAR_METHOD}}` | `RedisCache.clearCacheByKey` | Redis 缓存清除方法 |
| `{{SERVER_PORT}}` | 48080 | 主服务端口 |
| `{{CONFIG_CENTER}}` | Nacos | 配置中心类型 |

## G. SDA 工作流体系（大部分可通用化）

> 以下参数是工作流框架的核心概念，多数项目可复用。

| 参数名 | 当前值 | 说明 |
|--------|--------|------|
| `{{SDA_SERIAL_ORDER}}` | db→backend→frontend→tester→reviewer | SDA 串行编排顺序 |
| `{{SPEC_FILE_COUNT}}` | 4（requirements/design/test-cases/tasks） | Spec 文件数量和类型 |
| `{{AC_TYPES}}` | 功能/权限/数据/交互/性能 | AC 类型分类 |
| `{{DESIGN_OUTPUT_MANIFEST_SECTION}}` | §11 | design.md 文件产出清单章节号 |
| `{{MAX_REVIEW_ROUNDS}}` | 5 | 评审最大轮次 |
| `{{TASK_ID_FORMATS}}` | T-xxx / T-DOC-xxx / T-UT-xxx / T-E2E-xxx | 任务 ID 格式 |

## 使用方法

1. 新项目初始化时，创建 `.claude/knowledge/project-params.json`，填入实际值
2. 运行 `python .claude/tools/params-replace.py --init`，将所有配置文件中的 `{{PARAM}}` 替换为实际值
3. 项目特定知识（troubleshooting.md 中的业务问题）需手动更新

## 当前状态

> 本参数映射表已定义但尚未替换。配置文件仍使用芋道项目的实际值。
> 替换后，配置体系可复用到任何 SpringBoot + Vue 技术栈项目。