---
name: sdc-dbquery
description: 数据库只读查询工具，自动读取连接信息，支持 SELECT/SHOW/DESC 仅
---

# /sdc-dbquery 命令

## 用途

对项目数据库执行只读查询（SELECT/SHOW/DESC/DESCRIBE），连接信息从 secrets.json 自动读取。

## 触发场景

- 审查代码时需要验证数据库状态（表是否存在、字段类型、索引配置）
- 开发时需要查看现有表结构作为参考
- 排查问题时需要查询数据验证业务逻辑
- 数据迁移前后需要验证数据完整性

## 安全约束

| 约束 | 说明 |
|------|------|
| 只允许 SELECT/SHOW/DESC/DESCRIBE | 禁止 INSERT/UPDATE/DELETE/DROP/ALTER/CREATE 等写操作 |
| 默认最多返回 100 行 | 防止大查询影响性能，可通过 `--limit` 调整 |
| 查询超时 30 秒 | 防止慢查询阻塞 |
| 密码不传递给 AI 模型 | 连接信息从 secrets.json 本地读取 |

## 使用方法

### 基本查询

```bash
python .claude/tools/db-query.py --query "{args}" --format table
```

### 查看连接配置（密码不显示）

```bash
python .claude/tools/db-query.py --show-config
```

### 首次使用需确认连接信息

```bash
python .claude/tools/db-query.py --confirm --query "SHOW TABLES"
```

### 限制返回行数

```bash
python .claude/tools/db-query.py --query "{args}" --format table --limit 50
```

## 常用查询示例

### 查看所有表

```bash
python .claude/tools/db-query.py --query "SHOW TABLES" --format table
```

### 查看表结构

```bash
python .claude/tools/db-query.py --query "DESC t_user" --format table
```

### 查看索引

```bash
python .claude/tools/db-query.py --query "SHOW INDEX FROM t_user" --format table
```

### 查看表字符集

```bash
python .claude/tools/db-query.py --query "SHOW CREATE TABLE t_user" --format table
```

### 查询数据量

```bash
python .claude/tools/db-query.py --query "SELECT COUNT(*) FROM t_user" --format table
```

### 按条件查询

```bash
python .claude/tools/db-query.py --query "SELECT id, name, status FROM t_user WHERE deleted = 0 LIMIT 10" --format table
```

## 输出格式

支持两种输出格式：

| 格式 | 说明 | 适用场景 |
|------|------|----------|
| `table` | 表格格式（默认） | 人工查看 |
| `json` | JSON 格式 | 程序处理 |

## 注意事项

- 查询结果仅用于参考和验证，不作为代码依据
- 表结构设计以 design.md 和 DO 类为准
- 查询生产数据库时需格外谨慎，避免大查询
- 敏感数据（密码、手机号等）查询结果不要在日志中展示
- 如查询超时，尝试添加 LIMIT 或缩小查询范围
