# 设计文档：{功能名称}

> 创建时间：{日期}
> 状态：{草稿 / 已评审 / 已确认}

## 1. 技术方案概述

**一句话描述**：{采用什么技术方案实现}

**方案选择原因**：{为什么选择这个方案}

## 2. 数据库设计

> 必填项。新表或修改现有表的设计。
>
> **字符集规范**：SQL 脚本字符集声明和 Docker MySQL 执行规范详见 `steer/foundation/tech.md`「数据库字符集规范」节。

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

## 3. API 设计

> 必填项。接口定义。

### 3.1 接口列表

| 方法 | 路径 | 说明 | 权限标识 |
|------|------|------|----------|
| POST | /business/meeting-room/create | 创建会议室 | business:meeting-room:create |
| PUT | /business/meeting-room/update | 更新会议室 | business:meeting-room:update |
| DELETE | /business/meeting-room/delete | 删除会议室 | business:meeting-room:delete |
| GET | /business/meeting-room/get | 获取会议室详情 | business:meeting-room:query |
| GET | /business/meeting-room/page | 获取会议室分页列表 | business:meeting-room:query |

### 3.2 接口详情

#### 创建会议室

**请求**：
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

#### 获取会议室分页列表

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | String | 否 | 会议室名称（模糊匹配） |
| status | Integer | 否 | 状态 |
| pageNo | Integer | 是 | 页码 |
| pageSize | Integer | 是 | 每页数量 |

**响应**：
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

## 4. 关键决策

> 必填项。技术选型、架构决策及其原因。

| 决策项 | 选择 | 原因 | 替代方案 |
|--------|------|------|----------|
| 时间冲突检测 | 数据库唯一索引 + 应用层校验 | 双重保障，防止并发超卖 | 仅应用层校验 |
| 统计查询 | 实时查询 + 缓存 | 数据量可控，缓存提升性能 | 定时任务聚合 |

## 5. 数据流程图

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

## 6. 风险评估

> 可选项。已知风险及应对措施。

| 风险 | 级别 | 应对措施 |
|------|------|----------|
| 并发预约冲突 | 高 | 数据库唯一索引 + 乐观锁 |
| 统计查询性能 | 中 | 添加索引 + 缓存 |

## 7. 测试要点

> 可选项。重点测试场景。

| 场景 | 测试要点 |
|------|----------|
| 正常预约 | 预约成功，数据正确 |
| 时间冲突 | 提示错误，不创建记录 |
| 并发预约 | 只有一个成功 |
| 边界值 | 预约时间刚好相邻 |

## 8. 文件产出清单

> **必填项**。每个 SDA 将创建或修改的文件及关键签名，确保 SDA 之间文件路径对齐，减少上下文传递偏差。

### 数据库层（sda-db-implementer 产出）

| 文件类型 | 文件路径 | 关键内容 |
|----------|---------|---------|
| SQL | sql/{TABLE_NAME}.sql | 建表脚本 |
| DO | {entity_package}/{ClassName}DO.java | 实体类（字段清单） |
| Mapper | {mapper_package}/{ClassName}Mapper.java | `extends BaseMapper<{ClassName}DO>` |

### 后端层（sda-backend 产出）

| 文件类型 | 文件路径 | 关键签名 |
|----------|---------|---------|
| SaveReqVO | {vo_package}/{ClassName}SaveReqVO.java | 字段：{列出必填字段} |
| PageReqVO | {vo_package}/{ClassName}PageReqVO.java | `extends PageParam` |
| RespVO | {vo_package}/{ClassName}RespVO.java | 字段：{列出响应字段} |
| Service | {service_package}/{ClassName}Service.java | `Long createXxx(SaveReqVO)`, `void updateXxx(SaveReqVO)`, `void deleteXxx(Long)`, `RespVO getXxx(Long)`, `PageResult<RespVO> getXxxPage(PageReqVO)` |
| ServiceImpl | {service_package}/{ClassName}ServiceImpl.java | 实现 {ClassName}Service |
| Controller | {controller_package}/{ClassName}Controller.java | `@RequestMapping("/xxx")`, `@PreAuthorize("@ss.hasPermission('xxx:create')")` 等 |

### 前端层（sda-frontend 产出）

| 文件类型 | 文件路径 | 关键内容 |
|----------|---------|---------|
| API | api/xxx/index.js | `getXxxPage`, `getXxx`, `createXxx`, `updateXxx`, `deleteXxx` |
| 列表页 | views/xxx/index.vue | 表格 + 搜索 + 分页 |
| 表单弹窗 | views/xxx/XxxForm.vue | 新增/编辑表单 |

**示例**：
| SQL | sql/business_meeting_room.sql | 建表脚本（含 SET NAMES utf8mb4） |
| DO | entity/business/MeetingRoomDO.java | 字段：id, name, capacity, location, status |
| Mapper | mapper/business/MeetingRoomMapper.java | `extends BaseMapper<MeetingRoomDO>` |
| SaveReqVO | vo/business/MeetingRoomSaveReqVO.java | name(必填), capacity(必填), location, equipment |
| RespVO | vo/business/MeetingRoomRespVO.java | id, name, capacity, location, status, createTime |
| Service | service/business/MeetingRoomService.java | `createMeetingRoom`, `updateMeetingRoom`, `deleteMeetingRoom`, `getMeetingRoomPage` |
| Controller | controller/admin/business/MeetingRoomController.java | `@RequestMapping("/business/meeting-room")` |
| API | api/business/meeting-room/index.ts | `getMeetingRoomPage`, `createMeetingRoom`, `updateMeetingRoom`, `deleteMeetingRoom` |
| 列表页 | views/business/meeting-room/index.vue | 搜索 + 表格 + 分页 |
| 表单弹窗 | views/business/meeting-room/MeetingRoomForm.vue | 新增/编辑表单 |
