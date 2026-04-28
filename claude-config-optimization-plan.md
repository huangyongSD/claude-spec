# Claude 配置文件全面优化计划

> 生成日期：2026-04-27
> 工作空间：C:\Users\andy\Documents\wordDoc\discover\claude-spec

## Context

当前项目 `.claude/` 目录下有 37 个配置文件，存在以下问题：
- 大量内容重复（安全规则三重定义、200行规则出现 20+ 次、关键洞察 3 处完全相同）
- Vue2/Vue3 不匹配（项目是 Vue2+Element-UI，但配置文件大量使用 Vue3/TS 模式）
- SDA 数量不一致（CLAUDE.md 说 8 个，sda-collaboration.md 说 9 个）
- 审评轮次为 3 轮，用户要求改为 5 轮
- steer/domain/ 4 个文件与 rules/ 高度重叠且包含错误
- 项目缺少数据库查询工具和 CC/Trea 双模式工作流
- 多处占位符未填写、E2E 测试规则与实际基础设施矛盾

用户期望：构建完整的、有监管和评审的开发流程，兼容 CC（可并行 agent）和 Trea（串行执行），支持 5 轮评审、自动触发开发、编译验证、数据库查询工具。

**新增需求**：敏感信息保护 — 不将真实密码/主机IP传递给 AI 模型，配置文件中只使用占位符，真实值只在本地 secrets.json 中保存（不提交 Git），通过 Hook 机制在运行时拦截和提醒。

---

## Phase A：删除冗余文件（5 个文件）

| 删除文件 | 原因 |
|----------|------|
| `.claude/steer/domain/security.md` | 与 `rules/security.md` 100% 重叠，且为泛化规则而非项目特有 |
| `.claude/steer/domain/frontend.md` | 与 `rules/frontend.md` 重叠 + Vue3 错误内容（Pinia/ref/reactive/CSS Modules） |
| `.claude/steer/domain/testing.md` | 与 `rules/testing.md` 重叠，fileMatchPattern 只匹配 Java 测试 |
| `.claude/steer/domain/api.md` | 与 `rules/security.md` 和 `sda-backend.md` 重叠，RESTful 规范为 AI 常识 |
| `.claude/agents/sda-coverage-auditor.md` | 从未在 sdc-dev 工作流中被调度，功能合并到 sda-code-reviewer |

---

## Phase B：修复错误内容

1. **`agents/sda-frontend.md`** — 将所有 Vue3/TypeScript 示例改为 Vue2+Element-UI+JS：
   - `api/xxx/index.ts` → `api/xxx/index.js`（函数式 export，非 XxxApi 对象模式）
   - `<script setup lang="ts">` → `<script>` with Options API 或 Vue 2.7 `<script setup>`（无 TS）
   - `interface XxxVO` → JSDoc `@typedef` 或直接删除类型定义
   - `ref<XxxVO[]>()` → `data() { return { list: [] } }` 或 Vue 2.7 `ref([])`
   - `XxxApi` 对象模式 → `import { getXxxPage } from '@/api/xxx'` 函数模式（匹配项目实际风格）
   - Pinia → Vuex

2. **`skills/troubleshooting.md`** — 修正 RuoYi → yudao 命名（7 处）

3. **`steer/foundation/product.md`** — 填充 3 处"待填写"

4. **`steer/foundation/never.md`** — 填充 1 处"待填写"

5. **`steer/foundation/structure.md`** — 填充 3 处 ADR 占位符

6. **`rules/testing.md`** — 在 E2E 规则区域顶部添加项目现状说明：当前无 E2E 框架，E2E 规则降级为人工验收

7. **`rules/frontend.md`** — 将 Pinia/Vuex 改为 `Vuex（本项目为 Vue2）`

---

## Phase C：内容去重合并

1. **关键洞察去重** — `rules/security.md` 为权威源，删除 `rules/frontend.md` 和 `sda-code-reviewer.md` 中的重复洞察块，改为引用行

2. **覆盖率审计合并到 sda-code-reviewer** — 在 `sda-code-reviewer.md` 中新增"Coverage Audit Dimension"段落，包含虚假覆盖率检测表和审计流程（来自已删除的 sda-coverage-auditor.md）

3. **charset 规范去重** — 权威源为 `steer/foundation/tech.md`，其他文件改为引用

4. **200行规则去重** — 权威源为 `rules/sda-collaboration.md` + 各 SDA 自身配置。从 `sdc-dev.md` prompt 和 `sdc-spec.md` prompt 中删除重复说明，改为"参考对应 SDA 配置文件中的规范约束"

5. **Playwright 代码片段去重** — 权威源为 `rules/testing.md` + `sda-tester.md`，`templates/spec/test-cases.md` 改为引用

---

## Phase D：评审轮次 3→5（17 处）

全局替换所有"最多 3 轮"为"最多 5 轮"，涉及：
- `sdc-spec.md`（5 处）
- `sdc-dev.md`（12 处）
- `sda-doc-reviewer.md`（1 处）

同时更新 `sda-doc-reviewer.md` 退出条件：5 轮后由用户决定（接受/继续/拒绝）

---

## Phase E：新增文件（6 个）

1. **`.claude/tools/db-query.py`** — 数据库只读查询工具
   - 从 `.claude/tools/secrets.json`（本地存储，不提交 Git）自动读取连接信息
   - 首次运行需用户确认连接信息（`--confirm` 或交互确认）
   - 只允许 SELECT/SHOW/DESC/DESCRIBE，正则拦截所有写操作关键字
   - 单条语句限制、默认 100 行上限、30 秒超时
   - 输出格式：JSON（默认，供 AI 解析）或 table（`--format table`）
   - 强制 charset=utf8mb4
   - CLI：`python db-query.py --query "SQL" [--source master|slave] [--format json|table] [--limit N] [--timeout S] [--confirm] [--show-config]`

2. **`.claude/tools/requirements.txt`** — `pymysql>=1.1.0` + `pyyaml>=6.0`

3. **`.claude/tools/secrets.json`** — 本地敏感信息存储（**不提交 Git**）
   - 存储数据库密码、主机 IP、Redis 密码等真实值
   - 由 `secrets-sync.py` 从 application YAML 自动提取并生成
   - 包含字段：db_master_host, db_master_port, db_master_name, db_master_user, db_master_password, db_slave_*, redis_host, redis_port, redis_password 等
   - `.gitignore` 中添加 `.claude/tools/secrets.json`

4. **`.claude/tools/secrets-sync.py`** — 敏感信息同步脚本
   - 从 `application-*.yml` 自动提取连接信息，写入 `secrets.json`
   - 同时扫描 `.claude/` 下所有配置文件，将其中出现的真实敏感值替换为占位符（如 `{{DB_MASTER_PASSWORD}}`）
   - 占位符映射表存储在 `secrets.json` 的 `placeholders` 字段
   - 仅在本地运行，不提交到 Git
   - 运行时机：每次修改 application YAML 后执行一次同步
   - CLI：`python secrets-sync.py [--profile local|dev] [--scan-configs]`

5. **`.claude/commands/sdc-dbquery.md`** — 斜杠命令包装 db-query.py

6. **`.claude/steer/domain/workflow.md`** — CC/Trea 双模式工作流规范（替代已删除的 4 个 domain 文件）
   - 定义 7 步工作流：沟通→文档→评审→触发→多agent开发→per-agent评审→编译验证
   - CC 模式：可并行的阶段使用并行（DB+Backend 合并调度、前后端编译可并行）
   - Trea 模式：严格串行，每步一个 prompt，prompt 必须自包含
   - 5 轮评审上限，5 轮后用户决定
   - 编译验证作为显式步骤（后端 mvn clean package + 前端 yarn build:prod + 启动验证）

---

## Phase E2：敏感信息保护 Hook（新增 3 个文件 + 更新 3 个文件）

### 泄露路径分析

敏感信息可能通过以下路径传递给 AI 模型（Claude/Trea）：
1. **AI 读取项目源代码** — application-*.yaml 包含真实密码（123456/rabbit/guest/admin）和主机 IP
2. **AI 读取 .claude/ 配置文件** — 如果配置中引用了真实密码/IP
3. **AI 写入代码** — 生成的代码中可能包含从上下文中复制的真实密码/IP

**保护策略**：
- **源代码中的 application YAML** 不修改（它们是项目运行必需的，且已在 Git 中）
- **新增 PostToolUse Hook**：当 AI 读取 application YAML 时提醒忽略真实敏感值
- **新增 PostToolUse Hook**：当 AI 写入任何文件时，检测内容是否包含真实敏感值并警告

### 新增 Hook/脚本文件

1. **`.claude/hooks/sensitive-filter.py`** — 核心敏感信息过滤脚本（Python，跨平台）
   - 功能：接收文件内容，扫描并替换所有已知敏感值为占位符
   - 真实值来源：`.claude/tools/secrets.json` 的 `real_values` 字段
   - 占位符格式：`{{DB_MASTER_PASSWORD}}`、`{{DB_MASTER_HOST}}`、`{{REDIS_PASSWORD}}` 等
   - 支持多种匹配模式：精确字符串匹配、正则模式（IP 地址、常见密码格式）
   - 输出：脱敏后的内容 + 检测到的敏感项列表

2. **`.claude/hooks/post-sensitive-read.ps1`** — PostToolUse Hook（Read 工具读取后提醒）
   - 当 AI 读取 `application-*.yaml` 或其他可能包含敏感信息的文件后：
   - 检测读取的文件路径是否匹配敏感文件模式
   - 如果匹配：发出提醒 "[Hook] 此文件包含敏感信息（密码/IP），请勿在后续操作中使用真实值，使用占位符替代"
   - 不阻断操作，只发出警告提醒

3. **`.claude/hooks/post-sensitive-scan.ps1`** — PostToolUse Hook（扫描 Edit/Write 操作）
   - 在写入任何文件时，检查写入内容是否包含真实密码/IP
   - 检测范围：所有 `.claude/` 配置文件 + 所有 `.java/.vue/.js/.yaml` 代码文件
   - 如果发现真实敏感值：发出警告 "[Hook] 检测到敏感信息（密码/IP）正在写入文件，建议使用占位符替代"
   - 检测值来自 `secrets.json` 的 `real_values` 字段（精确匹配）
   - 不会阻断操作，只发出警告提醒

### 更新现有文件

4. **`.claude/hooks/post-edit-check.ps1`** — 扩展：
   - 保留现有格式化提醒和 `{{PLACEHOLDER}}` 检测功能
   - 新增：如果编辑的是 `.claude/` 下的配置文件，检测写入内容是否包含真实密码/IP（来自 secrets.json）

5. **`.claude/settings.json`** — 新增 Hook 配置：
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             {
               "type": "command",
               "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/pre-bash-check.ps1"
             }
           ]
         }
       ],
       "PostToolUse": [
         {
           "matcher": "(Read)",
           "hooks": [
             {
               "type": "command",
               "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/post-sensitive-read.ps1"
             }
           ]
         },
         {
           "matcher": "(Edit|Write)",
           "hooks": [
             {
               "type": "command",
               "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/post-sensitive-scan.ps1"
             },
             {
               "type": "command",
               "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/post-edit-check.ps1"
             }
           ]
         }
       ]
     }
   }
   ```

6. **`.gitignore`** — 新增 `.claude/tools/secrets.json` 行

### 在 CLAUDE.md 和 rules/security.md 中新增敏感信息保护规则

7. **`rules/security.md`** — 新增 🔴 级规则：
   > 9. **禁止在 .claude/ 配置文件中使用真实密码/IP** — 必须使用占位符（如 {{DB_MASTER_PASSWORD}}），真实值存储在 .claude/tools/secrets.json（本地，不提交 Git）。AI 生成代码时也必须使用占位符，不得复制上下文中看到的真实敏感值。

8. **`CLAUDE.md`** — 在行为规范中新增：
   > - **敏感信息保护**：.claude/ 配置文件中禁止使用真实密码/IP，使用占位符替代。真实值存储在本地 secrets.json，通过 db-query.py 本地执行数据库操作，不将密码传递给 AI 模型。

### 敏感信息保护机制总览

```
┌──────────────────────────────────────────────┐
│  secrets.json（本地，不提交 Git）                │
│  ├─ real_values: 真实密码/IP/端口               │
│  └─ placeholders: 占位符映射表                   │
│    {{DB_MASTER_PASSWORD}} → 123456             │
│    {{DB_MASTER_HOST}} → 127.0.0.1              │
│    {{REDIS_PASSWORD}} → (empty)                │
├──────────────────────────────────────────────┤
│  secrets-sync.py（同步脚本）                     │
│  ├─ 从 application YAML 提取真实值              │
│  ├─ 写入 secrets.json                          │
│  └─ 扫描 .claude/ 配置文件，替换真实值→占位符    │
├──────────────────────────────────────────────┤
│  Hook 层（运行时防护）                           │
│  ├─ post-sensitive-read.ps1：Read application  │
│  │   YAML 时提醒 AI 忽略真实敏感值              │
│  ├─ post-sensitive-scan.ps1：写入文件时检测      │
│  │   真实敏感值并警告                            │
│  └─ post-edit-check.ps1：配置文件编辑时检测      │
│    敏感值 + placeholder 残留                    │
├──────────────────────────────────────────────┤
│  db-query.py（查询工具）                         │
│  ├─ 从 secrets.json 读取真实连接信息             │
│  ├─ 本地执行查询，不将密码传入 AI prompt          │
│  └─ 输出不包含密码字段                            │
├──────────────────────────────────────────────┤
│  application YAML（源代码，不修改）               │
│  ├─ 包含真实密码/IP（项目运行必需）               │
│  ├─ AI Read 时 Hook 提醒：忽略真实敏感值          │
│  └─ secrets-sync.py 从此文件提取真实值           │
└──────────────────────────────────────────────┘
```

**关键设计原则**：
- **项目源代码中的 application YAML 不修改** — 它们包含真实密码是项目运行必需的
- **.claude/ 配置文件中只存在占位符**，不存在真实密码/IP
- **AI agent 只能看到占位符**，不应在后续操作中使用从 application YAML 中读取的真实密码/IP
- **db-query.py 从 secrets.json 读取真实连接信息**，在本地终端执行，不将密码传入 AI 可见的上下文
- **Hook 层提供运行时提醒**：当 AI 读取包含敏感信息的文件时发出警告，当 AI 写入包含真实敏感值的文件时发出警告
- **secrets.json 不提交 Git**，`.gitignore` 中排除

---

## Phase F：更新交叉引用

1. **`CLAUDE.md`** — 精简重构：
   - SDA 列表改为 8 个（sda-coverage-auditor 已合并到 sda-code-reviewer，标注"含覆盖率审计"）
   - 流程图简化为引用 `steer/domain/workflow.md`，删除内联大段流程图
   - domain 表更新：删除已删的 4 个文件，新增 workflow.md
   - 新增 tools/ 和 db-query 引用
   - 新增 CC/Trea 双模式说明
   - 新增敏感信息保护说明

2. **`sdc-dev.md`** — 更新：
   - 评审轮次 3→5
   - 新增 CC/Trea 执行模式说明段落
   - 新增编译验证作为显式最终阶段（mvn clean package + yarn build:prod + 启动验证）
   - 新增 db-query 工具引用
   - 去重 200 行规则和 charset 规范
   - SDA 表删除 sda-coverage-auditor 行

3. **`sda-db-implementer.md`** — 新增 db-query 工具引用（验证数据库状态时使用）

4. **`sda-code-reviewer.md`** — 新增覆盖率审计段落 + db-query 工具引用 + 去重关键洞察

5. **`steer/domain/quality-gate.md`** — sda-coverage-auditor 引用改为 sda-code-reviewer

6. **`settings.json`** — 新增 `Bash(python .claude/tools/db-query.py *)` 到 allow 列表 + 新增敏感信息扫描 Hook 配置

7. **`.gitignore`** — 新增 `.claude/tools/secrets.json` 条目

---

## Phase G：验证

1. 读取所有修改后的文件确认内容正确
2. 运行 `python .claude/tools/secrets-sync.py --profile local --scan-configs` 验证同步脚本可提取敏感信息并生成 secrets.json
3. 运行 `python .claude/tools/db-query.py --show-config` 验证工具可从 secrets.json 读取连接信息
4. 检查 `.claude/` 所有配置文件中不存在真实密码/IP（只存在占位符）
5. 检查所有文件中不再有"最多 3 轮"残留
6. 检查所有文件中不再有 Vue3/TS 错误模式残留
7. 检查 steer/domain/ 目录只剩 workflow.md 和 quality-gate.md
8. 运行 `mvn clean compile` + `yarn build` 确认项目仍可编译

---

## 最终文件统计

| 类别 | 优化前 | 优化后 | 变化 |
|------|--------|--------|------|
| rules/ | 5 | 5 | 0 |
| steer/foundation/ | 4 | 4 | 0 |
| steer/domain/ | 5 | 2（workflow+quality-gate） | -3 |
| agents/ | 9 | 8 | -1 |
| commands/ | 5 | 6 | +1 |
| skills/ | 1 | 1 | 0 |
| templates/ | 4 | 4 | 0 |
| hooks/ | 2 | 4（+sensitive-filter.py +post-sensitive-read.ps1 +post-sensitive-scan.ps1） | +2 |
| tools/ | 0 | 4（db-query+secrets-sync+secrets.json+requirements.txt） | +4 |
| settings.json | 1 | 1 | 0 |
| **总计** | **37** | **37** | **0** |

净文件数不变（删除 5 + 新增 6 + hooks +2 = 37），但实际改善远大于数字：
- 消除 ~15 处重复内容
- 修正 Vue2/Vue3 不匹配
- 修复命名错误（RuoYi→yudao）
- 填充占位符
- 新增数据库查询工具和双模式工作流
- **新增敏感信息保护机制防止密码/IP 泄露给 AI 模型**
- 审评轮次从 3 轴提升到 5 轮