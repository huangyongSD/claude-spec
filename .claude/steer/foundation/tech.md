# 技术栈与架构

> 本文件描述项目的技术组成，帮助 AI 理解代码的组织方式。

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | {{FRONTEND_FRAMEWORK}} | {{VERSION}} |
| 后端 | {{BACKEND_FRAMEWORK}} | {{VERSION}} |
| 数据库 | {{DATABASE}} | {{VERSION}} |
| 中间件 | {{MIDDLEWARE}} | {{PURPOSE}} |

## 环境配置

- **包管理器**：{{PACKAGE_MANAGER}}
- **构建命令**：{{BUILD_CMD}}
- **测试命令**：{{TEST_CMD}}
- **格式化命令**：{{FORMAT_CMD}}
- **Lint 命令**：{{LINT_CMD}}

## 环境差异

| 环境 | 用途 | 配置特点 |
|------|------|---------|
| dev | 本地开发 | 本地数据库、热重载 |
| test | 自动化测试 | H2 内存数据库 |
| prod | 生产环境 | 连接远程数据库、禁用调试 |

## Maven 编译规范

**重要**：模块重组后，必须使用 `mvn clean compile` 项目全量编译验证，不能仅用 `mvn compile` 增量编译。

- 增量编译（`mvn compile`）：只编译改动的文件，复用 `target/` 旧 class 文件
- 项目全量编译（`mvn clean compile`）：删除 target 后从源码重新编译，暴露包路径不匹配等问题

**教训**：模块合并时目录结构改了但 package 声明未同步，导致单独编译通过但全项目编译失败。

## 关键依赖

- {{DEPENDENCY_1}}：{{PURPOSE}}
- {{DEPENDENCY_2}}：{{PURPOSE}}

## 数据库字符集规范

**重要**：所有 SQL 脚本必须包含字符集声明，避免中文乱码。

### SQL 文件规范
```sql
-- SQL 文件开头必须添加：
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
```

### Docker MySQL 执行规范
```bash
# 必须指定字符集
docker exec <container> mysql -uroot -p123456 --default-character-set=utf8mb4 <db> -e "SQL语句"

# 或通过管道执行 SQL 文件
docker exec -i <container> mysql -uroot -p123456 --default-character-set=utf8mb4 <db> < script.sql
```

### 问题排查
```bash
# 检查字符集设置
docker exec <container> mysql -uroot -p123456 -e "SHOW VARIABLES LIKE 'character%';"

# 正确输出应为：
# character_set_client     = utf8mb4
# character_set_connection = utf8mb4
# character_set_results    = utf8mb4
# character_set_database   = utf8mb4
```

## 数据库方言规范

**重要**：生成 SQL 脚本时必须与项目数据库类型一致，避免语法差异导致执行失败。

| 数据库类型 | 语法特点 |
|-----------|---------|
| MySQL | 使用 `AUTO_INCREMENT`、反引号、LIMIT OFFSET |
| PostgreSQL/瀚高 | 使用 `SERIAL`/`GENERATED ALWAYS AS IDENTITY`、双引号、LIMIT OFFSET |
| 瀚高 | 兼容 PostgreSQL 协议，字符串拼接用 `\|\|` |

### 常见语法差异

| 场景 | MySQL | PostgreSQL/瀚高 |
|------|-------|----------------|
| 自增主键 | `id INT AUTO_INCREMENT` | `id SERIAL` 或 `id GENERATED ALWAYS AS IDENTITY` |
| 字符串拼接 | `CONCAT(a, b)` | `a \|\| b` |
| 分页 | `LIMIT 10 OFFSET 20` | `LIMIT 10 OFFSET 20`（相同） |
| 日期函数 | `NOW()`、`DATE_FORMAT()` | `NOW()`、`TO_CHAR()` |
| 标识符引号 | 反引号 `` ` `` | 双引号 `"` 或不加 |

### 使用约束

- **禁止**使用数据库特有函数（除非明确标注）
- **必须**在 SQL 头部注释标注目标数据库类型：`-- DB_TYPE: MySQL 8.0`
- 多数据库项目使用 `databaseId` 区分 SQL（MyBatis）或分开目录管理
