# 目录结构与修改导航

> 本文件是 AI 修改代码时的"导航图"——改 X 去哪里改。
> 这是 ROI 最高的内容：减少 AI 盲目搜索，快速定位正确文件。

## 目录结构

```
yudao-boot-mini/
├─ yudao-server/          主服务器（聚合模块）
│  └─ src/main/resources/  全局配置 (application.yaml)
├─ yudao-framework/        框架层（各 starter）
│  ├─ yudao-common/               公共工具
│  ├─ yudao-spring-boot-starter-security/  安全认证
│  ├─ yudao-spring-boot-starter-mybatis/   ORM
│  ├─ yudao-spring-boot-starter-redis/     缓存
│  ├─ yudao-spring-boot-starter-web/       Web
│  ├─ yudao-spring-boot-starter-mq/        消息队列
│  ├─ yudao-spring-boot-starter-job/       定时任务
│  ├─ yudao-spring-boot-starter-excel/     Excel
│  ├─ yudao-spring-boot-starter-monitor/   监控
│  ├─ yudao-spring-boot-starter-protection/ 保护
│  ├─ yudao-spring-boot-starter-biz-tenant/    多租户
│  ├─ yudao-spring-boot-starter-biz-data-permission/ 数据权限
│  ├─ yudao-spring-boot-starter-biz-ip/    IP 地域
│  └─ yudao-spring-boot-starter-websocket/ WebSocket
├─ yudao-module-system/   系统功能模块
│  └─ src/main/java/cn/iocoder/yudao/module/system/
│     ├─ controller/  控制器（admin + app）
│     ├─ service/     业务逻辑
│     ├─ dal/         数据访问层
│     └─ convert/     对象转换
├─ yudao-module-infra/    基础设施模块
│  └─ src/main/java/cn/iocoder/yudao/module/infra/
│     ├─ controller/  控制器
│     ├─ service/     业务逻辑
│     ├─ dal/         数据访问层
│     └─ convert/     对象转换
├─ yudao-dependencies/    BOM 依赖版本管理
├─ yudao-ui-admin/        前端管理后台
│  ├─ src/api/       API 调用层
│  ├─ src/views/     页面视图
│  ├─ src/components/ 公共组件
│  ├─ src/router/    路由配置
│  ├─ src/store/     Vuex 状态管理
│  └─ src/utils/     工具函数
├─ sql/                  数据库脚本
│  ├─ mysql/        MySQL
│  ├─ postgresql/   PostgreSQL
│  ├─ oracle/       Oracle
│  ├─ dm/           达梦
│  ├─ kingbase/     人大金仓
│  ├─ opengauss/    OpenGauss
│  └─ tools/        工具脚本
└─ script/               部署脚本
```

## 修改导航（改 X 去哪里改）

| 场景 | 目标文件/目录 | 注意事项 |
|------|-------------|---------|
| 新增 API endpoint | controller/**/*.java（admin/app 子包） + @RequestMapping | 需同步更新测试 |
| 修改业务逻辑 | service/**/*.java | 避免直接操作数据库 |
| 新增数据库表 | sql/mysql/ 目录 | 所有 SQL 脚本必须保存在 yudao-boot-mini/sql/ 目录 |
| 修改配置 | yudao-server/src/main/resources/application*.yaml | 注意环境差异 |
| 新增前端页面 | yudao-ui-admin/src/views/ + src/router/ | 需同步更新菜单 |

## 关键文件说明

| 文件 | 用途 | 修改频率 |
|------|------|---------|
| pom.xml | Maven 项目配置与依赖管理 | 高 |
| application.yaml | Spring Boot 全局配置 | 低 |

## 架构决策记录

> 这些决策不能从代码中推断出来，必须显式记录。

- **ADR-001**：选择 SpringBoot 而非 Quarkus，因为企业级稳定性与社区成熟度（日期：2026-04-27）
- **ADR-002**：选择 Vue2 而非 Vue3，因为 Element-UI 配套完善、团队熟悉度高、迁移成本大
- **ADR-003**：选择 MyBatis-Plus 而非 JPA，因为 SQL 控制更精细、团队经验丰富、动态 SQL 灵活
