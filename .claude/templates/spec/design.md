# 设计文档：{功能名称}

> 创建时间：{日期}
> 状态：{草稿 / 已评审 / 已确认}

## 1. 技术方案概述

**一句话描述**：{采用什么技术方案实现}

**方案选择原因**：{为什么选择这个方案}

## 1.1 需求追溯矩阵

> **必填项**。确保 design.md 每个章节都覆盖了 requirements.md 中的所有 AC。
> 评审时逐行检查：每个 AC 必须至少有一个设计章节覆盖，否则设计不完整。

| AC 编号 | 条件描述 | 覆盖章节 | 覆盖方式 | 对应 BR |
|---------|---------|---------|---------|---------|
| AC-001 | {条件1} | §3 API / §5 前端 | {哪个接口+哪个页面实现} | BR-001 |
| AC-002 | {条件2} | §3 API / §4 安全 | {哪个接口+哪个安全约束} | BR-002 |
| AC-003 | {条件3} | §2 数据库 / §3 API | {哪个表+哪个接口} | BR-003 |

**示例**：
| AC-001 | 用户可以创建会议室预约 | §3.2 创建接口 + §5.1 列表页 | POST /create + 新增按钮 | BR-002 |
| AC-002 | 预约时间冲突时提示错误 | §3.2 异常场景 + §4.2 IDOR | 业务逻辑校验 + 错误提示 | BR-001 |
| AC-003 | 只有管理员可以删除预约 | §4.1 权限模型 | @PreAuthorize + 前端按钮 v-if | BR-003 |

> **检查规则**：
> - 每个 AC 必须至少出现一次，否则设计遗漏
> - 一个 AC 可以被多个章节覆盖（如 AC-001 同时需要 API + 前端）
> - 如果某个 AC 无法在本设计中覆盖（如纯运维需求），在"覆盖方式"列标注"非本功能范围"并说明原因

## 2. 数据库设计

> 必填项。新表或修改现有表的设计。
>
> **字符集规范**：SQL 脚本字符集声明和 Docker MySQL 执行规范详见 CLAUDE.md 数据库规范节。

### 2.1 新增表

#### 表：{table_name}

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 主键 |
| {字段名} | {类型} | {约束} | {说明} |
| creator | VARCHAR(64) | | 创建者 |
| create_time | DATETIME | NOT NULL | 创建时间 |
| updater | VARCHAR(64) | | 更新者 |
| update_time | DATETIME | NOT NULL | 更新时间 |
| deleted | BIT(1) | NOT NULL DEFAULT 0 | 逻辑删除标识 |

**索引设计**：

| 索引名 | 字段 | 类型 | 说明 |
|--------|------|------|------|
| idx_{字段} | {字段} | 普通/唯一 | {用途} |

**示例**：
```sql
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
-- DB_TYPE: MySQL 8.0

CREATE TABLE `business_meeting_room` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '会议室ID',
  `name` varchar(100) NOT NULL COMMENT '会议室名称',
  `capacity` int NOT NULL DEFAULT 0 COMMENT '容纳人数',
  `location` varchar(200) DEFAULT NULL COMMENT '位置',
  `equipment` varchar(500) DEFAULT NULL COMMENT '设备信息（JSON）',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '状态（0禁用 1启用）',
  `creator` varchar(64) DEFAULT '' COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updater` varchar(64) DEFAULT '' COMMENT '更新者',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted` bit(1) NOT NULL DEFAULT b'0' COMMENT '是否删除',
  `tenant_id` bigint NOT NULL DEFAULT 0 COMMENT '租户编号',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name` (`name`, `tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会议室信息表';
```

### 2.2 修改表

| 表名 | 修改内容 | 说明 |
|------|----------|------|
| {表名} | 新增字段 {字段名} | {用途} |
| {表名} | 修改字段 {字段名} | {原因} |

### 2.3 回滚脚本

> 必填项。数据库变更必须提供回滚方案。

```sql
-- 回滚脚本（幂等执行）
DROP TABLE IF EXISTS `business_meeting_room`;
-- 或修改表的回滚
-- ALTER TABLE `xxx` DROP COLUMN `new_field`;
```

## 3. API 设计

> 必填项。接口定义。

### 3.1 接口列表

| 方法 | 路径 | 说明 | 权限标识 | 返回集合需 nil 兜底 | 对应 AC | 对应 BR |
|------|------|------|----------|---------------------|---------|---------|
| POST | /business/meeting-room/create | 创建会议室 | business:meeting-room:create | — | AC-001 | BR-002 |
| PUT | /business/meeting-room/update | 更新会议室 | business:meeting-room:update | — | AC-001 | — |
| DELETE | /business/meeting-room/delete | 删除会议室 | business:meeting-room:delete | — | AC-003 | BR-003 |
| GET | /business/meeting-room/get | 获取会议室详情 | business:meeting-room:query | — | AC-001 | — |
| GET | /business/meeting-room/page | 获取会议室分页列表 | business:meeting-room:query | ✅ list 字段 | AC-001 | — |

> **nil 兜底**：标记 ✅ 的接口，后端响应层必须将 null 集合兜底为空数组 `[]`，前端消费时加 `?? []`。

### 3.2 接口详情

#### 创建会议室

**请求 VO**：`MeetingRoomSaveReqVO`（禁止直接绑定 DO）

```json
{
  "name": "会议室A",
  "capacity": 10,
  "location": "3楼-301",
  "equipment": "[\"投影仪\", \"白板\"]"
}
```

**响应**：
```json
{
  "code": 0,
  "data": 1,
  "message": "success"
}
```

**业务逻辑**：
1. 校验会议室名称唯一性
2. 创建会议室记录
3. 返回会议室ID

**异常场景**：

| 场景 | 错误码 | 处理方式 |
|------|--------|----------|
| 名称重复 | 重复数据 | 返回"会议室名称已存在" |
| 参数校验失败 | 参数错误 | 返回具体校验失败字段 |

#### 获取会议室分页列表

**请求 VO**：`MeetingRoomPageReqVO`（extends PageParam）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | String | 否 | 会议室名称（模糊匹配） |
| status | Integer | 否 | 状态 |
| pageNo | Integer | 是 | 页码 |
| pageSize | Integer | 是 | 每页数量（上限 100） |

**响应 VO**：`MeetingRoomRespVO`

```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "id": 1,
        "name": "会议室A",
        "capacity": 10,
        "location": "3楼-301",
        "status": 1
      }
    ],
    "total": 100
  },
  "message": "success"
}
```

> **nil 兜底**：`list` 字段后端兜底 `[]`，前端消费 `response.data.list ?? []`。

## 4. 安全设计

> 必填项。安全约束必须在设计阶段明确，开发 agent 不可省略。

### 4.1 权限模型

| 权限标识 | 对应角色 | 对应 AC | 说明 |
|----------|---------|---------|------|
| business:meeting-room:create | {角色列表} | AC-001 | 创建权限 |
| business:meeting-room:update | {角色列表} | AC-001 | 更新权限 |
| business:meeting-room:delete | {角色列表} | AC-003 | 删除权限 |
| business:meeting-room:query | {角色列表} | AC-001 | 查询权限 |

**前后端权限同步**：

| 前端路由守卫 | 后端 @PreAuthorize | 同步状态 |
|-------------|-------------------|---------|
| {路由权限} | {权限标识} | ✅ 已同步 |

> **注意**：角色检查 ≠ 权限检查。`@PreAuthorize("hasRole('MANAGER')")` 只验证角色，不验证功能权限。写操作必须用 `@ss.hasPermission('xxx:action')`。

### 4.2 IDOR 防护（横向越权）

| 写操作 | 校验逻辑 | 说明 |
|--------|---------|------|
| 更新会议室 | 校验操作者是否有 `business:meeting-room:update` 权限 | 权限校验 |
| 删除会议室 | 校验操作者是否有 `business:meeting-room:delete` 权限 | 权限校验 |

> 如果业务涉及"只能操作自己创建的资源"，必须额外校验 `creator == 当前用户`。

### 4.3 输入安全

| 风险点 | 防护措施 | 说明 |
|--------|---------|------|
| SQL 注入 | MyBatis 使用 `#{}` 禁止 `${}` | 参数化查询 |
| XSS | 用户输入转义处理 | 前端 v-text 优先于 v-html |
| 字段注入 | 用 VO 接收参数，禁止绑定 DO | DTO 隔离 |
| 敏感数据 | 禁止明文传输，HTTPS 强制 | 传输安全 |

### 4.4 nil 集合兜底

| API | 集合字段 | 兜底策略 |
|-----|---------|---------|
| GET /page | list | 后端响应层兜底 `[]`，前端 `?? []` |
| {其他返回集合的 API} | {字段名} | 后端响应层兜底 `[]`，前端 `?? []` |

> **原则**：后端 API 响应层统一拦截 nil 集合，前端防御性消费 `?? []`。双保险优于单保险。

## 5. 前端设计

> 必填项。前端页面、组件、路由、菜单的设计。

### 5.1 页面设计

| 页面 | 路由 | 组件 | 对应 AC | 说明 |
|------|------|------|---------|------|
| 会议室列表 | /business/meeting-room | views/business/meeting-room/index.vue | AC-001 | 搜索 + 表格 + 分页 |
| 会议室表单 | — | views/business/meeting-room/MeetingRoomForm.vue | AC-001 | 新增/编辑弹窗 |

### 5.2 菜单配置

> 必填项。新增菜单必须配置 sys_menu 记录，否则前端看不到入口。

| 菜单层级 | 菜单名称 | path | component | perms | 说明 |
|----------|---------|------|-----------|-------|------|
| 一级菜单 | {名称} | /{path} | — | — | 目录（path 必须以 `/` 开头） |
| 二级菜单 | 会议室管理 | meeting-room | business/meeting-room/index | — | 页面 |
| 按钮 | 新增 | — | — | business:meeting-room:create | 按钮权限 |
| 按钮 | 修改 | — | — | business:meeting-room:update | 按钮权限 |
| 按钮 | 删除 | — | — | business:meeting-room:delete | 按钮权限 |
| 按钮 | 查询 | — | — | business:meeting-room:query | 按钮权限 |

> **关键**：一级菜单 path 必须以 `/` 开头，否则 Vue Router 无法识别为根路由，页面会 404。

### 5.3 防御性数据消费

| 场景 | 代码模式 | 说明 |
|------|---------|------|
| 列表数据赋值 | `this.list = response.data.list ?? []` | 禁止裸赋值 |
| 嵌套字段访问 | `row.equipment?.split(',') ?? []` | 可选链 + 默认值 |
| 数值显示 | `(row.capacity ?? 0).toString()` | 数值守卫 |
| API 调用错误 | `catch` 中显示错误提示 | 禁止静默失败 |

### 5.4 组件设计

| 组件 | 类型 | 关键交互 | 说明 |
|------|------|---------|------|
| {XxxForm} | 弹窗表单 | 新增/编辑复用，通过 `dialogStatus` 区分 | el-dialog + el-form |
| {XxxTable} | 表格 | 搜索 + 分页 + 操作按钮 | el-table + el-pagination |

## 6. 性能约束

> 必填项。性能相关的设计决策。

### 6.1 数据量预估

| 表 | 预估数据量 | 增长速度 | 对应 AC | 说明 |
|----|-----------|---------|---------|------|
| {table_name} | {N} 条/年 | {增长速度} | AC-xxx | {是否需要分表} |

### 6.2 索引策略

| 查询场景 | 使用索引 | 预期扫描行数 | 说明 |
|----------|---------|-------------|------|
| 按名称模糊搜索 | idx_name | {N} | LIKE 'xxx%' 走索引 |
| 按状态筛选 | idx_status | {N} | 枚举值，区分度低，考虑组合索引 |

### 6.3 缓存策略

| 缓存对象 | 缓存方式 | 过期时间 | 失效策略 | 说明 |
|----------|---------|---------|---------|------|
| {对象} | Redis / 无 | {TTL} | {失效方式} | {是否需要缓存} |

### 6.4 分页限制

| 接口 | pageSize 上限 | 对应 AC | 说明 |
|------|-------------|---------|------|
| {分页接口} | 100 | AC-xxx | 超过上限截断 |

## 7. 关键决策

> 必填项。技术选型、架构决策及其原因。

| 决策项 | 选择 | 原因 | 替代方案 |
|--------|------|------|----------|
| 时间冲突检测 | 数据库唯一索引 + 应用层校验 | 双重保障，防止并发超卖 | 仅应用层校验 |
| 统计查询 | 实时查询 + 缓存 | 数据量可控，缓存提升性能 | 定时任务聚合 |

## 8. 数据流程图

> 可选项。关键业务流程的时序图或流程图。

```
用户 -> Controller: 创建预约请求
Controller -> Service: 校验参数
Service -> Mapper: 查询时间段内是否有冲突
alt 有冲突
    Service --> Controller: 返回错误提示
else 无冲突
    Service -> Mapper: 插入预约记录
    Service --> Controller: 返回预约ID
end
```

## 9. 风险评估

> 可选项。已知风险及应对措施。

| 风险 | 级别 | 应对措施 |
|------|------|----------|
| 并发预约冲突 | 高 | 数据库唯一索引 + 乐观锁 |
| 统计查询性能 | 中 | 添加索引 + 缓存 |

## 10. 测试要点

> 可选项。重点测试场景。详细测试用例见 test-cases.md。

| 场景 | 测试要点 | 对应测试用例 |
|------|----------|------------|
| 正常预约 | 预约成功，数据正确 | UT-001, E2E-003 |
| 时间冲突 | 提示错误，不创建记录 | UT-002, E2E-005 |
| 并发预约 | 只有一个成功 | UT-002 |
| 边界值 | 预约时间刚好相邻 | UT-003 |

## 11. 文件产出清单

> **必填项**。每个 SDA 将创建或修改的文件及关键签名，确保 SDA 之间文件路径对齐，减少上下文传递偏差。
>
> **约束**：第 11 节的文件路径必须是具体路径（非占位符），由 sda-doc-reviewer 在 Spec 评审时验证。后续 SDA 以此节为契约自行发现前序产出文件。

### 数据库层（sda-db-implementer 产出）

| 文件类型 | 文件路径 | 关键内容 |
|----------|---------|---------|
| SQL（建表） | sql/{TABLE_NAME}.sql | 建表脚本（含 `SET NAMES utf8mb4` + `-- DB_TYPE: MySQL 8.0`） |
| SQL（回滚） | sql/{TABLE_NAME}_rollback.sql | 回滚脚本（幂等执行） |
| DO | {entity_package}/{ClassName}DO.java | 实体类（字段清单） |
| Mapper | {mapper_package}/{ClassName}Mapper.java | `extends BaseMapper<{ClassName}DO>` |

### 后端层（sda-backend 产出）

| 文件类型 | 文件路径 | 关键签名 |
|----------|---------|---------|
| SaveReqVO | {vo_package}/{ClassName}SaveReqVO.java | 字段：{列出必填字段}。校验注解：@NotBlank 等 |
| PageReqVO | {vo_package}/{ClassName}PageReqVO.java | `extends PageParam` |
| RespVO | {vo_package}/{ClassName}RespVO.java | 字段：{列出响应字段}。集合字段兜底 `[]` |
| Service | {service_package}/{ClassName}Service.java | `Long createXxx(SaveReqVO)`, `void updateXxx(SaveReqVO)`, `void deleteXxx(Long)`, `RespVO getXxx(Long)`, `PageResult<RespVO> getXxxPage(PageReqVO)` |
| ServiceImpl | {service_package}/{ClassName}ServiceImpl.java | 实现 {ClassName}Service。写操作校验直属关系 |
| Controller | {controller_package}/{ClassName}Controller.java | `@RequestMapping("/xxx")`, `@PreAuthorize("@ss.hasPermission('xxx:create')")` 等。用 VO 接收参数，禁止绑定 DO |

### 前端层（sda-frontend 产出）

| 文件类型 | 文件路径 | 关键内容 |
|----------|---------|---------|
| API | api/xxx/index.js | `getXxxPage`, `getXxx`, `createXxx`, `updateXxx`, `deleteXxx` |
| 列表页 | views/xxx/index.vue | 表格 + 搜索 + 分页。列表赋值 `this.list = res.data.list ?? []` |
| 表单弹窗 | views/xxx/XxxForm.vue | 新增/编辑表单 |
| 菜单 SQL | sql/{MODULE}_menu.sql | sys_menu 插入语句（一级菜单 path 以 `/` 开头） |

**示例**：
| SQL | sql/business_meeting_room.sql | 建表脚本（含 SET NAMES utf8mb4 + DB_TYPE） |
| SQL（回滚） | sql/business_meeting_room_rollback.sql | DROP TABLE IF EXISTS |
| DO | entity/business/MeetingRoomDO.java | 字段：id, name, capacity, location, status |
| Mapper | mapper/business/MeetingRoomMapper.java | `extends BaseMapper<MeetingRoomDO>` |
| SaveReqVO | vo/business/MeetingRoomSaveReqVO.java | name(必填), capacity(必填), location, equipment |
| RespVO | vo/business/MeetingRoomRespVO.java | id, name, capacity, location, status, createTime |
| Service | service/business/MeetingRoomService.java | `createMeetingRoom`, `updateMeetingRoom`, `deleteMeetingRoom`, `getMeetingRoomPage` |
| Controller | controller/admin/business/MeetingRoomController.java | `@RequestMapping("/business/meeting-room")` |
| API | api/business/meeting-room/index.ts | `getMeetingRoomPage`, `createMeetingRoom`, `updateMeetingRoom`, `deleteMeetingRoom` |
| 列表页 | views/business/meeting-room/index.vue | 搜索 + 表格 + 分页 |
| 表单弹窗 | views/business/meeting-room/MeetingRoomForm.vue | 新增/编辑表单 |
| 菜单 SQL | sql/business_meeting_room_menu.sql | 一级菜单 path: /business-meeting-room |
