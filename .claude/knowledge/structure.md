---
description: 项目目录结构详解（按需读取，定位文件时查阅）
---

# 目录结构详解

> 本文件从 CLAUDE.md 按需加载，AI 在需要定位文件时应主动查阅。

## 完整目录树

```
yudao-boot-mini/
├─ yudao-server/                    # 主服务器（聚合模块）
│  └─ src/main/resources/
│     └─ application.yaml           # 全局配置
│
├─ yudao-framework/                 # 框架层（禁止修改）
│  ├─ yudao-spring-boot-starter-web/
│  ├─ yudao-spring-boot-starter-security/
│  ├─ yudao-spring-boot-starter-mybatis/
│  └─ ...（各 starter）
│
├─ yudao-module-system/             # 系统功能模块
│  └─ src/main/java/.../system/
│     ├─ controller/
│     │  ├─ admin/                  # 管理后台 API
│     │  └─ app/                    # 移动端 API
│     ├─ service/                   # 业务逻辑
│     ├─ dal/
│     │  ├─ dataobject/             # DO（数据库实体）
│     │  └─ mysql/                  # Mapper
│     └─ convert/                   # 对象转换
│
├─ yudao-module-infra/              # 基础设施模块（结构同 system）
│
├─ yudao-dependencies/              # BOM 依赖版本管理（禁止修改）
│
├─ yudao-ui-admin/                  # 前端管理后台
│  ├─ src/api/                      # API 调用层
│  ├─ src/views/                    # 页面视图
│  ├─ src/components/               # 公共组件
│  ├─ src/router/                   # 路由配置
│  ├─ src/store/                    # Vuex 状态管理
│  ├─ src/utils/                    # 工具函数
│  └─ src/directive/                # 自定义指令（如 v-hasPermi）
│
├─ sql/                             # 数据库脚本
│  ├─ mysql/                        # MySQL 脚本
│  ├─ postgresql/                   # PostgreSQL 脚本
│  ├─ oracle/                       # Oracle 脚本
│  ├─ dm/                           # 达梦脚本
│  ├─ kingbase/                     # 瀚高脚本
│  └─ tools/                        # 工具脚本
│
└─ script/                          # 部署脚本
```

## 修改导航详解

| 场景 | 目标文件/目录 | 注意事项 |
|------|-------------|---------|
| 新增 API endpoint | `controller/**/*.java`（admin/app 子包） | 需同步更新测试 |
| 修改业务逻辑 | `service/**/*.java` | 避免直接操作数据库 |
| 新增数据库表 | `sql/mysql/` 目录 | 所有 SQL 必须保存在 sql/ 目录 |
| 修改配置 | `yudao-server/src/main/resources/application*.yaml` | 注意环境差异 |
| 新增前端页面 | `yudao-ui-admin/src/views/` + `src/router/` | 需同步更新菜单 |
| 新增前端组件 | `yudao-ui-admin/src/components/` | 优先复用现有组件 |
| 权限配置 | `sys_menu` 表 + 后端 `@PreAuthorize` | 前后端同步 |

## 架构决策记录

| 编号 | 决策 | 原因 |
|------|------|------|
| ADR-001 | 选择 SpringBoot 而非 Quarkus | 企业级稳定性与社区成熟度 |
| ADR-002 | 选择 Vue2 而非 Vue3 | Element-UI 配套完善、团队熟悉度高、迁移成本大 |
| ADR-003 | 选择 MyBatis-Plus 而非 JPA | SQL 控制更精细、团队经验丰富、动态 SQL 灵活 |