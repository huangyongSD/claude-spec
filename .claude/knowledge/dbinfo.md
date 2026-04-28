---
description: 数据库规范与方言差异（按需读取，处理 SQL/数据库时查阅）
---

# 数据库规范

> 本文件从 CLAUDE.md 按需加载，AI 在处理 SQL/数据库相关任务时应主动查阅。

## 字符集规范

所有 SQL 脚本必须声明字符集：

```sql
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
```

Docker 执行必须指定字符集：

```bash
docker exec <container> mysql -uroot -p123456 --default-character-set=utf8mb4 <db> -e "SQL语句"
```

## 方言差异对照

本项目目标数据库为 **MySQL 8.0**，SQL 脚本头部必须标注：`-- DB_TYPE: MySQL 8.0`

| 场景 | MySQL | PostgreSQL/瀚高 |
|------|-------|----------------|
| 自增主键 | `INT AUTO_INCREMENT` | `SERIAL` |
| 字符串拼接 | `CONCAT(a, b)` | `a || b` |
| 标识符引号 | 反引号 `` ` `` | 双引号 `"` |
| 分页 | `LIMIT offset, count` | `LIMIT count OFFSET offset` |
| 布尔类型 | `TINYINT(1)` | `BOOLEAN` |
| 日期格式化 | `DATE_FORMAT(date, '%Y-%m-%d')` | `TO_CHAR(date, 'YYYY-MM-DD')` |

## 禁止事项

- 禁止使用数据库特有函数（除非明确标注 `-- DB_TYPE: MySQL 8.0`）
- 多数据库项目使用 `databaseId` 区分 SQL
- 禁止 SQL 拼接（见 [security.md](../rules/security.md) 🔴4）

## 常见问题

详见 [troubleshooting.md](troubleshooting.md) 数据库章节：
- MySQL 连接失败
- 中文乱码
- 时区问题
- PostgreSQL/瀚高适配