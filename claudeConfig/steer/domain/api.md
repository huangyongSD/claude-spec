---
inclusion: fileMatch
fileMatchPattern: ["**/controller/**/*.java", "**/vo/**/*.java"]
---

# API 开发规范

> 本文件在编辑后端 API 文件时加载。

## RESTful 规范

- URL 使用名词复数：`/users` 而非 `/getUser`
- 使用正确的 HTTP 方法：GET（查询）、POST（新增）、PUT（更新）、DELETE（删除）
- 嵌套资源限制一层：`/users/123/orders` 而非 `/users/123/orders/456/items`

## 响应格式

```json
{
  "code": 0,
  "data": {},
  "message": "success"
}
```

| code | 含义 |
|------|------|
| 0 | 成功 |
| 400 | 参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 500 | 服务器错误 |

## 错误处理

- 所有异常必须捕获，统一返回上述响应格式
- 不在响应中暴露堆栈信息
- 记录错误日志，包含请求 ID 用于追踪

## 参数校验

- 必填参数必须校验，不允许 null/undefined
- 字符串类型校验长度范围
- 数字类型校验最大值最小值
- 日期类型校验格式和范围

## 分页规范

```json
{
  "code": 0,
  "data": {
    "list": [],
    "total": 100,
    "page": 1,
    "pageSize": 20
  },
  "message": "success"
}
```

## VO 包规范

| 类型 | 包路径 | 说明 |
|------|--------|------|
| ReqVO | vo/xxx/XxxSaveReqVO.java | 保存请求参数 |
| PageReqVO | vo/xxx/XxxPageReqVO.java | 分页请求参数 |
| RespVO | vo/xxx/XxxRespVO.java | 响应数据 |

## 权限注解规范

| 操作 | 权限标识 |
|------|---------|
| 新增 | xxx:create |
| 更新 | xxx:update |
| 删除 | xxx:delete |
| 查询 | xxx:query |
| 导出 | xxx:export |
