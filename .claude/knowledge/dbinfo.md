---
description: 数据库规范与方言差异（按需读取，处理 SQL/数据库时查阅）
---

# 数据库规范

> 本文件从 CLAUDE.md 按需加载，AI 在处理 SQL/数据库相关任务时应主动查阅。

## 字符集规范

所有 SQL 脚本必须声明字符集：

```sql
-- PostgreSQL 使用 UTF-8（服务端默认配置，无需 SET NAMES）
-- 确认数据库编码：
SHOW server_encoding;  -- 应为 UTF8
```

Docker 执行必须指定字符集：

```bash
docker exec <container> psql -U postgres -d ruoyi -c "SQL语句"
```

## 方言差异对照

本项目目标数据库为 **PostgreSQL**，SQL 脚本头部必须标注：`-- DB_TYPE: PostgreSQL`

| 场景 | PostgreSQL（本项目） | MySQL（对照） |
|------|---------------------|--------------|
| 自增主键 | `BIGSERIAL` / `SERIAL` | `INT AUTO_INCREMENT` |
| 字符串拼接 | `a || b` | `CONCAT(a, b)` |
| 标识符引号 | 双引号 `"` | 反引号 `` ` `` |
| 分页 | `LIMIT count OFFSET offset` | `LIMIT offset, count` |
| 布尔类型 | `BOOLEAN` | `TINYINT(1)` |
| 日期格式化 | `TO_CHAR(date, 'YYYY-MM-DD')` | `DATE_FORMAT(date, '%Y-%m-%d')` |
| 逻辑删除 | `del_flag char(1) DEFAULT '0'` | `deleted tinyint DEFAULT 0` |
| 注释 | `COMMENT ON COLUMN/TABLE` | `COMMENT '注释'` 内联 |
| 空值判断 | `IS NULL` / `COALESCE` | `IS NULL` / `IFNULL` |
| 时间戳 | `timestamp(6)` | `datetime` |

## 禁止事项

- 禁止使用数据库特有函数（除非明确标注 `-- DB_TYPE: PostgreSQL`）
- 禁止 SQL 拼接（见 [security.md](../rules/security.md) 🔴4）
- 禁止使用 MySQL 语法（如 `AUTO_INCREMENT`、`ENGINE=InnoDB`、反引号等）

## 常见问题

详见 [troubleshooting.md](troubleshooting.md) 数据库章节：
- MySQL 连接失败
- 中文乱码
- 时区问题
- PostgreSQL/瀚高适配