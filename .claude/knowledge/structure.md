---
description: 项目目录结构详解（按需读取，定位文件时查阅）
---

# 目录结构详解

> 本文件从 CLAUDE.md 按需加载，AI 在需要定位文件时应主动查阅。

## 完整目录树

```
RuoYi-Vue-Postgresql/
├─ ruoyi-admin/                     # 聚合模块（启动入口+Controller）
│  └─ src/main/java/com/ruoyi/web/
│     ├─ controller/
│     │  ├─ common/                  # 公共 API
│     │  ├─ monitor/                 # 监控 API
│     │  ├─ system/                  # 系统 API
│     │  └─ tool/                    # 工具 API
│     └─ RuoYiApplication.java       # 启动类
│  └─ src/main/resources/
│     ├─ application.yml             # 全局配置
│     └─ application-druid.yml       # 数据源配置
│
├─ ruoyi-framework/                 # 框架层（禁止修改）
│  └─ src/main/java/com/ruoyi/framework/
│     ├─ config/                     # 各类配置类
│     ├─ security/                   # 安全相关
│     └─ interceptor/                # 拦截器
│
├─ ruoyi-system/                    # 系统功能模块
│  └─ src/main/java/com/ruoyi/system/
│     ├─ domain/                     # Domain 实体类（对应数据库表）
│     ├─ domain/vo/                  # VO（仅 MetaVo/RouterVo）
│     ├─ mapper/                     # Mapper 接口（纯 MyBatis）
│     └─ service/                    # ISysXxxService 接口
│        └─ impl/                    # SysXxxServiceImpl 实现
│
├─ ruoyi-quartz/                    # 定时任务模块
│  └─ src/main/java/com/ruoyi/quartz/
│     ├─ controller/
│     ├─ domain/
│     ├─ mapper/
│     └─ service/
│
├─ ruoyi-generator/                 # 代码生成模块
│  └─ src/main/java/com/ruoyi/generator/
│     ├─ controller/
│     ├─ domain/
│     ├─ mapper/
│     └─ service/
│
├─ ruoyi-common/                    # 通用工具模块
│  └─ src/main/java/com/ruoyi/common/
│     ├─ core/domain/               # BaseEntity/AjaxResult/TableDataInfo
│     ├─ core/controller/           # BaseController
│     ├─ core/page/                 # 分页相关
│     ├─ annotation/                # @Log 等注解
│     ├─ enums/                     # BusinessType 等枚举
│     ├─ exception/                 # ServiceException
│     ├─ utils/                     # 工具类
│     └─ constant/                  # 常量
│
├─ ruoyi-ui/                        # 前端管理后台
│  ├─ src/api/                      # API 调用层
│  ├─ src/views/                    # 页面视图
│  ├─ src/components/               # 公共组件（Pagination 等）
│  ├─ src/router/                   # 路由配置
│  ├─ src/store/                    # Vuex 状态管理
│  ├─ src/utils/                    # 工具函数
│  ├─ src/directive/                # 自定义指令（v-hasPermi/v-hasRole）
│  ├─ src/plugins/                  # 插件
│  └─ src/layout/                   # 布局组件
│
├─ sql/                             # 数据库脚本
│  ├─ postgresql.sql                # PostgreSQL 主脚本
│  ├─ postgresql_view.sql           # PostgreSQL 视图
│  ├─ quartz.sql                    # 定时任务表
│  └─ ry_20250522.sql               # 其他 SQL
│
└─ doc/                             # 文档
```

## 修改导航详解

| 场景 | 目标文件/目录 | 注意事项 |
|------|-------------|---------|
| 新增 API endpoint | `controller/**/*.java`（system/monitor/tool/common 子包） | 需同步更新测试 |
| 修改业务逻辑 | `service/impl/**/*.java` | 避免直接操作数据库 |
| 新增数据库表 | `sql/` 目录 | 所有 SQL 必须保存在 sql/ 目录 |
| 修改配置 | `ruoyi-admin/src/main/resources/application*.yml` | 注意环境差异 |
| 新增前端页面 | `ruoyi-ui/src/views/` + `src/router/` | 需同步更新菜单 |
| 新增前端组件 | `ruoyi-ui/src/components/` | 优先复用现有组件 |
| 权限配置 | `sys_menu` 表 + 后端 `@PreAuthorize("@ss.hasPermi")` | 前后端同步 |

## 架构决策记录

| 编号 | 决策 | 原因 |
|------|------|------|
| ADR-001 | 选择 SpringBoot 而非 Quarkus | 企业级稳定性与社区成熟度 |
| ADR-002 | 选择 Vue2 而非 Vue3 | Element-UI 配套完善、团队熟悉度高、迁移成本大 |
| ADR-003 | 选择 MyBatis 而非 MyBatis-Plus 或 JPA | SQL 控制更精细、团队经验丰富、动态 SQL 灵活 |
| ADR-004 | 选择 PostgreSQL 而非 MySQL | 业务需求或合规要求（需人工填写原因） |