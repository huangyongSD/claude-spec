# AI 项目初始化文档

> 版本：1.0 | 日期：2026-04-27
> 本文档供 AI（Claude Code）使用，在目标项目中执行初始化配置
> 参考：CLAUDE-CODE-TEAM-SETUP-GUIDE.md

---

## 执行流程

```
复制配置文件 → 扫描项目 → 用户选择范围 → 提炼信息替换占位符 → 验证文件完整性
```

---

## 第一步：复制 claudeConfig 到 .claude

### 1.1 检查现有文件

先检查 `.claude/` 目录是否已存在以及其中有哪些文件：

```bash
ls -la .claude/ 2>/dev/null || echo "No .claude directory"
git ls-files .claude/ 2>/dev/null
```

### 1.2 复制策略

**需要复制的文件清单（35 个）**：

| 序号 | 源文件（claudeConfig/） | 目标文件（.claude/） |
|------|------------------------|---------------------|
| 1 | rules/security.md | .claude/rules/security.md |
| 2 | rules/testing.md | .claude/rules/testing.md |
| 3 | rules/frontend.md | .claude/rules/frontend.md |
| 4 | rules/git.md | .claude/rules/git.md |
| 5 | rules/sda-collaboration.md | .claude/rules/sda-collaboration.md |
| 6 | steer/foundation/product.md | .claude/steer/foundation/product.md |
| 7 | steer/foundation/tech.md | .claude/steer/foundation/tech.md |
| 8 | steer/foundation/structure.md | .claude/steer/foundation/structure.md |
| 9 | steer/foundation/never.md | .claude/steer/foundation/never.md |
| 10 | steer/domain/quality-gate.md | .claude/steer/domain/quality-gate.md |
| 11 | steer/domain/api.md | .claude/steer/domain/api.md |
| 12 | steer/domain/testing.md | .claude/steer/domain/testing.md |
| 13 | steer/domain/security.md | .claude/steer/domain/security.md |
| 14 | steer/domain/frontend.md | .claude/steer/domain/frontend.md |
| 15 | commands/sdc-plan.md | .claude/commands/sdc-plan.md |
| 16 | commands/sdc-codereview.md | .claude/commands/sdc-codereview.md |
| 17 | commands/sdc-buildfix.md | .claude/commands/sdc-buildfix.md |
| 18 | commands/sdc-spec.md | .claude/commands/sdc-spec.md |
| 19 | commands/sdc-dev.md | .claude/commands/sdc-dev.md |
| 20 | agents/sda-architect.md | .claude/agents/sda-architect.md |
| 21 | agents/sda-reviewer.md | .claude/agents/sda-reviewer.md |
| 22 | agents/sda-db-implementer.md | .claude/agents/sda-db-implementer.md |
| 23 | agents/sda-backend.md | .claude/agents/sda-backend.md |
| 24 | agents/sda-frontend.md | .claude/agents/sda-frontend.md |
| 25 | agents/sda-tester.md | .claude/agents/sda-tester.md |
| 26 | agents/sda-code-reviewer.md | .claude/agents/sda-code-reviewer.md |
| 27 | agents/sda-build-error-resolver.md | .claude/agents/sda-build-error-resolver.md |
| 28 | skills/troubleshooting.md | .claude/skills/troubleshooting.md |
| 29 | settings.json | .claude/settings.json |
| 30 | hooks/pre-bash-check.ps1 | .claude/hooks/pre-bash-check.ps1 |
| 31 | hooks/post-edit-check.ps1 | .claude/hooks/post-edit-check.ps1 |
| 32 | templates/spec/requirements.md | .claude/templates/spec/requirements.md |
| 33 | templates/spec/design.md | .claude/templates/spec/design.md |
| 34 | templates/spec/test-cases.md | .claude/templates/spec/test-cases.md |
| 35 | templates/spec/tasks.md | .claude/templates/spec/tasks.md |

另有 CLAUDE.md 需根据模板生成（见说明），`.gitignore` 需追加 `.env` 条目。

> **CLAUDE.md 生成说明**：claudeConfig/ 目录中没有独立的 CLAUDE.md 文件，需要根据参考文档中的模板内容生成。参考文档中包含完整的 CLAUDE.md 模板（含所有 `{{...}}` 占位符），AI 读取模板后替换占位符写入项目根目录。

> **CLAUDE.md 已存在时的处理**：如果项目根目录已有 CLAUDE.md，询问用户「CLAUDE.md 已存在，是否替换？」用户确认替换 → 用模板重新生成并替换占位符；用户拒绝替换 → 保留原 CLAUDE.md，跳过生成步骤，但后续占位符替换步骤仍需检查原 CLAUDE.md 中是否有 `{{...}}` 占位符并处理。

### 1.3 复制执行规则

**如果目标文件不存在**：直接复制，无需询问。

**如果目标文件已存在**：
- 逐个询问用户：「文件 `{目标路径}` 已存在，是否替换？」
- 用户确认替换 → 覆盖复制
- 用户拒绝替换 → 保留原文件，跳过该文件
- 记录哪些文件被跳过，在最终验证报告中标注

### 1.4 复制命令

```bash
# 先创建目录结构
mkdir -p .claude/rules .claude/commands .claude/agents .claude/skills \
  .claude/steer/foundation .claude/steer/domain \
  .claude/specs .claude/templates/spec .claude/hooks

# 逐个复制文件（对已存在文件需先询问）
cp claudeConfig/rules/security.md .claude/rules/security.md
cp claudeConfig/rules/testing.md .claude/rules/testing.md
cp claudeConfig/rules/frontend.md .claude/rules/frontend.md
cp claudeConfig/rules/git.md .claude/rules/git.md
cp claudeConfig/rules/sda-collaboration.md .claude/rules/sda-collaboration.md
cp claudeConfig/steer/foundation/product.md .claude/steer/foundation/product.md
cp claudeConfig/steer/foundation/tech.md .claude/steer/foundation/tech.md
cp claudeConfig/steer/foundation/structure.md .claude/steer/foundation/structure.md
cp claudeConfig/steer/foundation/never.md .claude/steer/foundation/never.md
cp claudeConfig/steer/domain/quality-gate.md .claude/steer/domain/quality-gate.md
cp claudeConfig/steer/domain/api.md .claude/steer/domain/api.md
cp claudeConfig/steer/domain/testing.md .claude/steer/domain/testing.md
cp claudeConfig/steer/domain/security.md .claude/steer/domain/security.md
cp claudeConfig/steer/domain/frontend.md .claude/steer/domain/frontend.md
cp claudeConfig/commands/sdc-plan.md .claude/commands/sdc-plan.md
cp claudeConfig/commands/sdc-codereview.md .claude/commands/sdc-codereview.md
cp claudeConfig/commands/sdc-buildfix.md .claude/commands/sdc-buildfix.md
cp claudeConfig/commands/sdc-spec.md .claude/commands/sdc-spec.md
cp claudeConfig/commands/sdc-dev.md .claude/commands/sdc-dev.md
cp claudeConfig/agents/sda-architect.md .claude/agents/sda-architect.md
cp claudeConfig/agents/sda-reviewer.md .claude/agents/sda-reviewer.md
cp claudeConfig/agents/sda-db-implementer.md .claude/agents/sda-db-implementer.md
cp claudeConfig/agents/sda-backend.md .claude/agents/sda-backend.md
cp claudeConfig/agents/sda-frontend.md .claude/agents/sda-frontend.md
cp claudeConfig/agents/sda-tester.md .claude/agents/sda-tester.md
cp claudeConfig/agents/sda-code-reviewer.md .claude/agents/sda-code-reviewer.md
cp claudeConfig/agents/sda-build-error-resolver.md .claude/agents/sda-build-error-resolver.md
cp claudeConfig/skills/troubleshooting.md .claude/skills/troubleshooting.md
cp claudeConfig/settings.json .claude/settings.json
cp claudeConfig/hooks/pre-bash-check.ps1 .claude/hooks/pre-bash-check.ps1
cp claudeConfig/hooks/post-edit-check.ps1 .claude/hooks/post-edit-check.ps1
cp claudeConfig/templates/spec/requirements.md .claude/templates/spec/requirements.md
cp claudeConfig/templates/spec/design.md .claude/templates/spec/design.md
cp claudeConfig/templates/spec/test-cases.md .claude/templates/spec/test-cases.md
cp claudeConfig/templates/spec/tasks.md .claude/templates/spec/tasks.md
# CLAUDE.md 不在 claudeConfig/ 中，需根据参考文档模板生成
```

> **注意**：如果项目使用 git 且 `.claude/` 文件已在 git 中跟踪但工作树中缺失（如之前误删），优先使用 `git restore .claude/` 恢复，而非从 claudeConfig 复制。

### 1.5 .gitignore 追加

检查 `.gitignore` 是否已包含 `.env`，如未包含则追加：

```bash
grep -q "^\.env$" .gitignore 2>/dev/null || echo ".env" >> .gitignore
```

---

## 第二步：全量扫描项目信息

### 2.1 扫描指令

AI 需执行以下扫描任务，逐项检查项目实际状态：

**扫描清单**：

1. **项目名称**
   - 查找：pom.xml 中的 `<artifactId>`、package.json 中的 `name`、README.md 标题
   - 取最先找到的有意义名称

2. **技术栈（前端/后端/框架/语言）**
   - 后端：检查 pom.xml / build.gradle 的依赖（SpringBoot、MyBatis-Plus 等）
   - 前端：检查 package.json 的 dependencies（Vue、React 等）
   - 语言版本：pom.xml 的 `<java.version>`、package.json 的 engines

3. **数据库类型**
   - 检查：application.yml / application.properties 中的 `spring.datasource.url`
   - 提取：MySQL / PostgreSQL / 瀚高 / Oracle / 无

4. **中间件**
   - 检查：application.yml 中的 Redis / ActiveMQ / Kafka / RabbitMQ 配置
   - 如无则标注"无"

5. **包管理器**
   - 检查：pom.xml → Maven / build.gradle → Gradle / package.json → pnpm/npm/yarn
   - 多模块项目分行标注（如 Maven（后端）/ pnpm（前端））

6. **构建命令**
   - 后端：`mvn package` / `mvn clean compile` / `gradle build`
   - 前端：`pnpm build` / `npm run build` / `yarn build`
   - 多模块项目分行标注

7. **测试命令**
   - 后端：`mvn test` / `gradle test`
   - 前端：`pnpm test` / `npm test` / `yarn test`

8. **E2E 测试命令**
   - 检查：package.json 的 scripts 中是否有 `test:e2e` / `playwright` / `cypress`
   - 如无则标注"无"

9. **格式化命令**
   - 后端：`mvn spotless:apply`（检查 pom.xml 是否有 spotless 插件）
   - 前端：`pnpm format` / `npm run format`
   - 如无则标注"无（IDE 格式化）"

10. **Lint 命令**
    - 前端：`pnpm lint` / `npm run lint` / `yarn lint`
    - 后端：如无则标注"无"
    - 检查 package.json scripts 和 eslint 配置

11. **代码文件扩展名**
    - 检查项目中的实际文件类型：.java / .xml / .vue / .js / .ts / .py / .sql 等
    - 用于 settings.json hook 匹配

12. **核心目录及职责**
    - 识别项目的核心源码目录（如 ruoyi-admin、src/views、src/main/java 等）
    - 每个目录一行，标注职责

13. **禁止修改的核心目录**
    - 识别框架核心配置目录（如 ruoyi-framework、src/config 等）
    - 标注哪些目录 AI 不应擅自修改

14. **API 文件目录**
    - 前端：src/api/ / src/services/ / api/ 等
    - 后端：src/controller/ / src/handler/ 等
    - 用于配置 api.md 的 fileMatchPattern

15. **测试文件目录**
    - 前端：tests/ / src/__tests__/ / test/ 等
    - 后端：src/test/ / test/ 等
    - 用于配置 testing.md 的 fileMatchPattern

16. **E2E 测试框架是否已配置**
    - 检查：package.json 中是否有 playwright / cypress / nightwatch 依赖
    - 检查：是否存在 playwright.config.ts / cypress.config.ts 等配置文件
    - 已配置 → 标注框架名称 + "已配置"
    - 未配置 → 标注"未配置"

### 2.2 扫描方法

AI 按以下顺序执行扫描：

```
1. 读取项目根目录文件列表 → 识别项目结构
2. 读取 pom.xml / build.gradle / package.json → 提取技术栈和依赖
3. 读取 application.yml / application.properties → 提取数据库和中间件配置
4. 搜索测试配置文件 → 提取测试命令
5. 搜索 E2E 测试相关文件 → 判断 E2E 框架状态
6. 读取 README.md → 补充项目背景信息
7. 执行 find/glob 命令 → 识别核心目录和文件扩展名
```

### 2.3 扫描结果格式

将扫描结果整理为以下结构化摘要：

```
项目名称：{PROJECT_NAME}
技术栈：{TECH_STACK}
数据库：{DB_TYPE}
中间件：{MIDDLEWARE}
包管理器：{PACKAGE_MANAGER}
构建命令：{BUILD_CMD}
测试命令：{TEST_CMD}
E2E 测试命令：{E2E_TEST_CMD}
格式化命令：{FORMAT_CMD}
Lint 命令：{LINT_CMD}
代码文件扩展名：{FILE_EXTENSIONS}
核心目录：{DIR_1}（{DIR_1_ROLE}）、{DIR_2}（{DIR_2_ROLE}）...
禁止修改目录：{FORBIDDEN_DIR}（→ 填入 {{CORE_DIR}}）
API 文件目录：{API_FILE_DIR}
测试文件目录：{TEST_FILE_DIR}
E2E 测试框架：{E2E_FRAMEWORK}

--- 以下为占位符映射 ---
{{PROJECT_NAME}} → {PROJECT_NAME}
{{TECH_STACK}} → {TECH_STACK}
{{DB_TYPE}} → {DB_TYPE}
{{MIDDLEWARE}} → {MIDDLEWARE}
{{PACKAGE_MANAGER}} → {PACKAGE_MANAGER}
{{BUILD_CMD}} → {BUILD_CMD}
{{TEST_CMD}} → {TEST_CMD}
{{E2E_TEST_CMD}} → {E2E_TEST_CMD}
{{FORMAT_CMD}} → {FORMAT_CMD}
{{LINT_CMD}} → {LINT_CMD}
{{DIR_1}} → {DIR_1}
{{DIR_1_ROLE}} → {DIR_1_ROLE}
{{DIR_2}} → {DIR_2}
{{DIR_2_ROLE}} → {DIR_2_ROLE}
{{CORE_DIR}} → {CORE_DIR}（禁止修改的目录，填入 never.md）
{{API_FILE_PATTERN}} → {API 文件目录的 glob 模式，如 src/api/**/*.ts}
{{TEST_FILE_PATTERN}} → {测试文件目录的 glob 模式，如 tests/**/*.test.ts}
{{FILE_EXTENSIONS}} → {代码文件扩展名正则，如 (java|xml|vue|js)$}
{{E2E_FRAMEWORK}} → {E2E 测试框架及状态}
{{PROJECT_DIR}} → {项目根目录名}
```

> **多模块项目标注规则**：前后端分离项目，占位符需分行标注。例如 `{{PACKAGE_MANAGER}}` → `Maven（后端）/ pnpm（前端）`，`{{BUILD_CMD}}` → `mvn package（后端）/ pnpm build（前端）`。

---

## 第三步：用户选择工作范围

### 3.1 展示扫描结果

将第二步的扫描结果展示给用户，格式如下：

```
扫描完成，发现以下项目信息：

项目名称：xxx
技术栈：xxx
数据库：xxx
...
```

### 3.2 展示可选范围

列出所有可以包含到工作范围内的项目/模块/功能领域：

```
请选择需要包含到 AI 协作工作范围内的项目/模块：

[1] ✅ {模块名} — {简要描述}
[2] ✅ {模块名} — {简要描述}
[3] ⬜ {模块名} — {简要描述}（可选）
...

输入编号来选择/取消选择，或输入 'all' 全选，'none' 全不选。
```

### 3.3 用户确认

用户确认后，AI 根据选定范围调整扫描结果摘要：
- 仅保留选定模块的核心目录
- 仅保留选定模块的 API 文件目录和测试文件目录
- 核心目录表根据选定模块增减行数

---

## 第四步：替换占位符

### 4.1 需要替换的文件

**以下文件包含 `{{...}}` 占位符，需要用扫描结果替换**：

| 序号 | 文件 | 替换方式 |
|------|------|---------|
| 1 | CLAUDE.md | 用扫描结果替换所有 `{{...}}` 占位符 |
| 2 | .claude/steer/foundation/product.md | 用扫描结果替换 `{{PROJECT_NAME}}` 等 |
| 3 | .claude/steer/foundation/tech.md | 用扫描结果替换 `{{FRONTEND_FRAMEWORK}}`、`{{BUILD_CMD}}`、`{{E2E_TEST_CMD}}`、`{{E2E_FRAMEWORK}}` 等 |
| 4 | .claude/steer/foundation/structure.md | 用扫描结果替换 `{{PROJECT_ROOT_DIR}}`、`{{DIR_TREE}}` 等 |
| 5 | .claude/steer/foundation/never.md | 用扫描结果替换 `{{CORE_DIR}}` 等 |
| 6 | .claude/steer/domain/api.md | 无 `{{...}}` 占位符，需手动编辑 fileMatchPattern |
| 7 | .claude/steer/domain/testing.md | 无 `{{...}}` 占位符，直接复制使用 |
| 8 | .claude/steer/domain/quality-gate.md | 无 `{{...}}` 占位符，直接复制使用 |
| 9 | .claude/steer/domain/security.md | 无 `{{...}}` 占位符，直接复制使用 |
| 10 | .claude/steer/domain/frontend.md | 无 `{{...}}` 占位符，直接复制使用 |
| 11 | .claude/rules/testing.md | 含 `{{TEST_CMD}}`、`{{CURRENT_COVERAGE}}`、`{{COVERAGE_CMD}}`、`{{LINT_CMD}}` 占位符，需替换 |
| 12 | .claude/rules/frontend.md | 含 `{{PLACEHOLDER}}` 占位符（文档性引用，非需替换），但会导致占位符检测误报（见 5.2 说明） |
| 13 | .claude/settings.json | 用扫描结果替换 `{{PACKAGE_MANAGER}}` |
| 14 | .claude/hooks/pre-bash-check.ps1 | 无 `{{...}}` 占位符，需手动编辑 PowerShell 变量（`$PACKAGE_MANAGER`） |
| 15 | .claude/hooks/post-edit-check.ps1 | 无 `{{...}}` 占位符，需手动编辑 PowerShell 变量（`$FILE_EXTENSIONS`、格式化提醒文本） |

> **注意**：rules/security.md、rules/git.md、rules/sda-collaboration.md 已包含实际规范内容，仅需确认分档标记，不包含 `{{...}}` 占位符。rules/testing.md 和 rules/frontend.md 含有少量占位符，需在替换步骤中处理。commands/ 和 agents/ 目录下的文件也不包含占位符，直接复制使用。

### 4.2 占位符完整清单

以下为所有需要替换的占位符及其含义：

> **占位符来源说明**：以下占位符分为两类：
> - **模板文件中的 `{{...}}` 占位符**：存在于 `claudeConfig/` 目录下的模板文件中，AI 可通过 `grep` 检测到。这些是严格意义上的占位符，必须在替换步骤中处理。
> - **参考文档中的占位符**：存在于 CLAUDE-CODE-TEAM-SETUP-GUIDE.md 中的 CLAUDE.md 模板（6.1 节），但 `claudeConfig/` 目录中没有独立的 CLAUDE.md 文件。AI 生成 CLAUDE.md 时需要从参考文档中读取模板并替换这些占位符。
>
> **命名约定说明**：以下占位符中存在三套技术栈命名体系，用途不同，不可混淆：
> - `{{TECH_STACK}}`（CLAUDE.md）→ 综合描述，如"SpringBoot + Vue3"
> - `{{TECH_A}}` / `{{TECH_B}}`（product.md）→ 技术选型决策 + 选型原因，如"选择 SpringBoot" + "企业级稳定性"
> - `{{FRONTEND_FRAMEWORK}}` / `{{BACKEND_FRAMEWORK}}`（tech.md）→ 具体框架 + 版本，如"Vue3 + Element Plus" / "SpringBoot 2.7"
> 同理，`{{DB_TYPE}}`（CLAUDE.md）是综合描述，`{{DATABASE}}`（tech.md）是具体名称+版本。

| 占位符 | 含义 | 示例值 | 主要使用文件 |
|--------|------|--------|-------------|
| `{{PROJECT_NAME}}` | 项目名称 | ruoyi-admin | CLAUDE.md、product.md |
| `{{TECH_STACK}}` | 前端/后端框架+语言 | SpringBoot + RuoYi + JDK8 + Vue3 | CLAUDE.md |
| `{{DB_TYPE}}` | 数据库类型及版本（综合描述） | MySQL 8.0 / 瀚高 / PostgreSQL 13 | CLAUDE.md |
| `{{MIDDLEWARE}}` | 中间件名称及用途 | Redis（缓存/会话）/ ActiveMQ（异步通知） | CLAUDE.md、tech.md |
| `{{PACKAGE_MANAGER}}` | 项目包管理器 | Maven / pnpm / pip / yarn | tech.md、settings.json、hooks |
| `{{BUILD_CMD}}` | 构建命令 | mvn package / pnpm build | tech.md |
| `{{TEST_CMD}}` | 单元测试命令 | mvn test / pnpm test | tech.md、rules/testing.md |
| `{{E2E_TEST_CMD}}` | E2E测试命令（如无则标注"无"） | pnpm test:e2e | tech.md |
| `{{FORMAT_CMD}}` | 代码格式化命令（如无则标注"无（IDE 格式化）"） | pnpm format / mvn spotless:apply | tech.md |
| `{{LINT_CMD}}` | Lint 检查命令（如无则标注"无"） | pnpm lint | tech.md、rules/testing.md |
| `{{DIR_1}}` `{{DIR_1_ROLE}}` | 核心目录及职责 | ruoyi-admin / 主模块 | CLAUDE.md |
| `{{DIR_2}}` `{{DIR_2_ROLE}}` | 额外核心目录及职责 | ruoyi-system / 系统模块 | CLAUDE.md |
| `{{API_FILE_PATTERN}}` | API 文件 glob 模式（需手动编辑 api.md 的 fileMatchPattern） | src/api/**/*.ts | steer/domain/api.md |
| `{{TEST_FILE_PATTERN}}` | 测试文件 glob 模式（需手动编辑 testing.md 的 fileMatchPattern） | tests/**/*.test.ts | steer/domain/testing.md |
| `{{FILE_EXTENSIONS}}` | 代码文件扩展名正则 | (java|xml|vue|js)$ | hooks/post-edit-check.ps1 |
| `{{E2E_FRAMEWORK}}` | E2E 测试框架及状态 | Playwright（已配置）/ 未配置 | tech.md |
| `{{PROJECT_DIR}}` | 项目根目录名 | ruoyi-admin | CLAUDE.md |
| `{{PROJECT_DESC}}` | 项目描述 | 企业级后台管理系统 | product.md |
| `{{BUSINESS_DOMAIN_1}}` | 核心业务域1 | 用户管理 | product.md |
| `{{BUSINESS_DOMAIN_2}}` | 核心业务域2 | 系统监控 | product.md |
| `{{BRIEF_DESC}}` | 业务域简述 | 用户权限和角色管理 | product.md |
| `{{TECH_A}}` | 技术选型A（选型决策） | SpringBoot | product.md |
| `{{TECH_B}}` | 技术选型B（选型决策） | Vue3 | product.md |
| `{{REASON}}` | 选型原因 | 企业级稳定性、社区活跃 | product.md、never.md、structure.md |
| `{{N}}` | 代码审查通过人数 | 2 | product.md |
| `{{CONVENTION}}` | 分支命名规范 | type/short-description | product.md |
| `{{BRIEF}}` | 发布流程简述 | CI 自动构建 → 人工测试 → 合并发布 | product.md |
| `{{FRONTEND_FRAMEWORK}}` | 前端框架名称+版本（具体技术） | Vue3 + Element Plus | tech.md |
| `{{BACKEND_FRAMEWORK}}` | 后端框架名称+版本（具体技术） | SpringBoot 2.7 | tech.md |
| `{{DATABASE}}` | 数据库名称+版本（具体技术） | MySQL 8.0 | tech.md |
| `{{VERSION}}` | 版本号 | 2.7 / 3.x | tech.md |
| `{{DEPENDENCY_1}}` | 关键依赖1 | MyBatis-Plus | tech.md |
| `{{DEPENDENCY_2}}` | 关键依赖2 | Sa-Token | tech.md |
| `{{PURPOSE}}` | 依赖用途 | ORM 框架 / 权限认证 | tech.md、never.md |
| `{{PROJECT_ROOT_DIR}}` | 项目根目录名 | ruoyi-admin | structure.md |
| `{{DIR_TREE}}` | 目录树 | 实际目录结构文本 | structure.md |
| `{{ROUTE_FILE}}` | 路由文件 | src/router/index.js | structure.md |
| `{{HANDLER_DIR}}` | Handler目录 | src/controller/ | structure.md |
| `{{BIZ_LOGIC_FILE}}` | 业务逻辑文件 | src/service/ | structure.md |
| `{{CONFIG_DIR}}` | 配置目录 | src/main/resources/ | structure.md |
| `{{PAGE_DIR}}` | 页面目录 | src/views/ | structure.md |
| `{{ROUTE_CONFIG}}` | 路由配置 | src/router/ | structure.md |
| `{{KEY_FILE_1}}` | 关键文件1 | pom.xml | structure.md |
| `{{KEY_FILE_2}}` | 关键文件2 | application.yml | structure.md |
| `{{FREQUENCY}}` | 修改频率 | 低 / 中 / 高 | structure.md |
| `{{OPTION_A}}` | ADR选项A | SpringBoot | structure.md |
| `{{OPTION_B}}` | ADR选项B | Quarkus | structure.md |
| `{{DATE}}` | ADR日期 | 2026-04-27 | structure.md |
| `{{OLD_TECH}}` | 迁移旧技术 | Vue2 | structure.md |
| `{{NEW_TECH}}` | 迁移新技术 | Vue3 | structure.md |
| `{{FEATURE}}` | 禁用特性 | 某功能 | structure.md |
| `{{LINK}}` | 参考链接 | issue#123 | structure.md |
| `{{CORE_DIR}}` | 禁止修改的目录 | ruoyi-framework | CLAUDE.md、never.md |
| `{{CONFIG_FILE}}` | 禁止提交的配置 | application-prod.yml | never.md |
| `{{MODULE}}` | 修改限制模块 | ruoyi-framework | never.md |
| `{{OWNER}}` | 模块负责人 | 张三 | never.md |
| `{{METHOD}}` | 通知方式 | Slack #dev频道 | never.md |
| `{{ANTI_PATTERN}}` | 代码反模式 | var 声明 | never.md |
| `{{TECH}}` | 废弃技术 | jQuery | never.md |
| `{{ID}}` | ADR编号 | 001 | never.md |
| `{{LOCATION}}` | 禁止写逻辑的位置 | Controller | never.md |
| `{{CORRECT_LOCATION}}` | 正确位置 | Service | never.md |
| `{{PITFALL_1}}` | 已知陷阱1 | 数据库字段类型不匹配 | never.md |
| `{{PITFALL_2}}` | 已知陷阱2 | 前端路由与后端权限不同步 | never.md |
| `{{CORRECT_PRACTICE}}` | 正确做法 | 使用统一的类型映射 | never.md |
| `{{TEST_UNIT}}` | 测试单元名 | UserService | rules/testing.md |
| `{{SCENARIO_1}}` | 测试场景 | 正常登录 | rules/testing.md |
| `{{CURRENT_COVERAGE}}` | 当前测试覆盖率百分比 | 0% / 45% | rules/testing.md |
| `{{COVERAGE_CMD}}` | 覆盖率检查命令 | mvn jacoco:report / npx coverage | rules/testing.md |

### 4.3 需人工填写的占位符

以下占位符无法通过自动化扫描获得，需要根据项目实际情况人工填写（主要用于 Steering 文件）：

| 占位符 | 含义 | 填写指引 |
|--------|------|---------|
| `{{BUSINESS_DOMAIN_1}}` `{{BUSINESS_DOMAIN_2}}` | 核心业务域名称及描述 | 根据项目实际业务填写 |
| `{{TECH_A}}` `{{TECH_B}}` | 技术选型项 | 从扫描结果的技术栈中选取关键框架 |
| `{{REASON}}` | 技术选型原因、陷阱原因等 | 人工填写团队决策背景 |
| `{{CONVENTION}}` | 团队分支命名规范 | 填写团队实际使用的命名规范 |
| `{{BRIEF}}` | 发布流程简述 | 填写团队实际发布流程 |
| `{{N}}` | 代码审查需要通过的人数 | 填写团队实际规定 |
| `{{DIR_TREE}}` | 完整目录树 | AI 执行 tree/find 命令生成 |
| `{{ROUTE_FILE}}` `{{HANDLER_DIR}}` `{{BIZ_LOGIC_FILE}}` 等 | 修改导航的目标文件/目录 | 根据项目目录结构填写 |
| `{{KEY_FILE_1}}` `{{FREQUENCY}}` | 关键文件路径及修改频率 | 根据项目实际填写 |
| `{{CORE_DIR}}` `{{CONFIG_FILE}}` | 禁止修改的目录和文件 | 根据项目实际情况填写 |
| `{{MODULE}}` `{{OWNER}}` `{{METHOD}}` | 修改限制相关字段 | 根据团队实际情况填写 |
| `{{ANTI_PATTERN}}` `{{TECH}}` `{{ID}}` 等 | 代码风格强制项 | 根据项目实际填写 |
| `{{PITFALL_1}}` `{{CORRECT_PRACTICE}}` | 已知陷阱及正确做法 | 根据团队踩坑经验填写 |

**AI 处理策略**：
- 可通过扫描获得的占位符 → 自动替换
- 需人工填写的占位符 → AI 向用户逐一询问，或标注为"待填写"并在最终验证中检查
- 用户可选择"全部跳过人工填写"，后续手动补充

### 4.4 替换执行方式

**逐个文件替换，每个文件替换后立即验证**：

1. 读取文件内容
2. 执行所有 `{{...}}` 占位符替换（用扫描结果或人工填写值）
3. 写入替换后的内容
4. 检查替换后文件是否还有未替换的占位符

**替换优先级**：
- 有扫描结果值的 → 直接替换
- 需人工填写但用户已提供的 → 替换
- 需人工填写但用户跳过的 → 保留原占位符，在验证步骤中标注

### 4.5 各文件替换详情

#### CLAUDE.md

替换以下核心占位符（CLAUDE.md 优先替换这 7 个，其余占位符在其他文件中替换；5.2 节验证全部占位符残留）：
- `{{PROJECT_NAME}}` → 项目名称
- `{{TECH_STACK}}` → 技术栈
- `{{DB_TYPE}}` → 数据库
- `{{MIDDLEWARE}}` → 中间件
- `{{DIR_1}}`、`{{DIR_1_ROLE}}` → 核心目录及职责（根据选定模块增减行数）
- `{{DIR_2}}`、`{{DIR_2_ROLE}}` → 额外核心目录及职责
- `{{PROJECT_DIR}}` → 项目根目录名

#### .claude/steer/foundation/product.md

替换以下占位符：
- `{{PROJECT_NAME}}` → 项目名称
- `{{PROJECT_DESC}}` → 项目描述（人工填写）
- `{{BUSINESS_DOMAIN_1}}`、`{{BRIEF_DESC}}` → 核心业务域（人工填写）
- `{{BUSINESS_DOMAIN_2}}`、`{{BRIEF_DESC}}` → 核心业务域（人工填写）
- `{{TECH_A}}`、`{{REASON}}` → 技术选型（人工填写）
- `{{TECH_B}}`、`{{REASON}}` → 技术选型（人工填写）
- `{{N}}` → 审查人数（人工填写）
- `{{CONVENTION}}` → 分支规范（人工填写）
- `{{BRIEF}}` → 发布流程（人工填写）

#### .claude/steer/foundation/tech.md

替换以下占位符：
- `{{FRONTEND_FRAMEWORK}}`、`{{VERSION}}` → 前端框架+版本
- `{{BACKEND_FRAMEWORK}}`、`{{VERSION}}` → 后端框架+版本
- `{{DATABASE}}`、`{{VERSION}}` → 数据库+版本
- `{{MIDDLEWARE}}`、`{{PURPOSE}}` → 中间件+用途
- `{{PACKAGE_MANAGER}}` → 包管理器
- `{{BUILD_CMD}}` → 构建命令
- `{{TEST_CMD}}` → 测试命令
- `{{E2E_TEST_CMD}}` → E2E 测试命令（扫描结果，如无则填"无"）
- `{{E2E_FRAMEWORK}}` → E2E 测试框架及状态（扫描结果）
- `{{FORMAT_CMD}}` → 根据项目实际情况填写（如无格式化命令则填"无（IDE 格式化）"，但保留占位符以匹配模板）
- `{{LINT_CMD}}` → Lint命令
- `{{DEPENDENCY_1}}`、`{{PURPOSE}}` → 关键依赖1（人工填写）
- `{{DEPENDENCY_2}}`、`{{PURPOSE}}` → 关键依赖2（人工填写）

**特别处理**：
- 如项目无 Maven（非 Java 项目），删除"Maven 编译规范"章节
- 如项目无 MySQL，删除"数据库字符集规范"和"Docker MySQL 执行规范"章节，保留"数据库方言规范"并根据实际数据库调整
- 如项目为纯前端项目，删除后端相关内容

#### .claude/steer/foundation/structure.md

替换以下占位符：
- `{{PROJECT_ROOT_DIR}}` → 项目根目录名
- `{{DIR_TREE}}` → 实际目录树（AI 执行 `tree -L 3 -d` 或等效命令生成）
- `{{ROUTE_FILE}}`、`{{HANDLER_DIR}}` → 路由/Handler文件（根据项目结构填写）
- `{{BIZ_LOGIC_FILE}}` → 业务逻辑文件
- `{{CONFIG_DIR}}` → 配置目录
- `{{PAGE_DIR}}`、`{{ROUTE_CONFIG}}` → 页面/路由目录
- `{{KEY_FILE_1}}`、`{{PURPOSE}}`、`{{FREQUENCY}}` → 关键文件（人工填写）
- `{{KEY_FILE_2}}`、`{{PURPOSE}}`、`{{FREQUENCY}}` → 关键文件（人工填写）
- `{{OPTION_A}}`、`{{OPTION_B}}`、`{{REASON}}`、`{{DATE}}` → ADR（人工填写）

#### .claude/steer/foundation/never.md

替换以下占位符：
- `{{CORE_DIR}}` → 禁止修改的目录
- `{{CONFIG_FILE}}` → 禁止提交的配置文件
- `{{MODULE}}` → 修改限制模块（人工填写）
- `{{OWNER}}` → 负责人（人工填写）
- `{{METHOD}}` → 通知方式（人工填写）
- `{{ANTI_PATTERN}}`、`{{REASON}}` → 反模式（人工填写）
- `{{TECH}}`、`{{ID}}` → 废弃技术（人工填写）
- `{{LOCATION}}`、`{{CORRECT_LOCATION}}` → 禁止位置（人工填写）
- `{{PITFALL_1}}`、`{{REASON}}`、`{{CORRECT_PRACTICE}}` → 已知陷阱（人工填写）

#### .claude/steer/domain/api.md

无 `{{...}}` 占位符，需手动编辑 `fileMatchPattern`：
- 将 frontmatter 中的 `fileMatchPattern` 从硬编码值改为项目实际的 API 文件 glob 模式
- 示例：`["src/api/**/*.ts", "src/controller/**/*.java"]`

#### .claude/steer/domain/testing.md

无 `{{...}}` 占位符，直接复制使用。

#### .claude/steer/domain/quality-gate.md

无 `{{...}}` 占位符，直接复制使用。

#### .claude/steer/domain/security.md

无 `{{...}}` 占位符，直接复制使用。

#### .claude/steer/domain/frontend.md

无 `{{...}}` 占位符，直接复制使用。

#### .claude/rules/testing.md

替换以下占位符：
- `{{CURRENT_COVERAGE}}` → 当前测试覆盖率百分比（扫描结果或人工填写，如无则填 `0`）
- `{{TEST_CMD}}` → 单元测试命令（扫描结果）
- `{{COVERAGE_CMD}}` → 覆盖率检查命令（扫描结果或人工填写，如无则填 `无`）
- `{{LINT_CMD}}` → Lint 命令（扫描结果，如无则删除该行）

#### .claude/rules/frontend.md

含 `{{PLACEHOLDER}}` 占位符，但此为文档性引用（用于说明禁止提交未替换占位符的规则），**不需要替换**。但 `grep -rE "{{[A-Z][A-Z_]+}}" .claude/` 会匹配到它，产生误报。5.2 占位符残留检查需排除此文件。

#### .claude/settings.json

替换以下占位符：
- `{{PACKAGE_MANAGER}}` → 包管理器命令（如 `mvn|yarn`）

> allow 权限列表需根据项目实际包管理器调整（增删条目），多模块项目参考附录 D。

#### .claude/hooks/pre-bash-check.ps1

无 `{{...}}` 占位符，需手动编辑 PowerShell 硬编码变量：
- `$PACKAGE_MANAGER = "mvn|yarn"` → 根据项目实际包管理器调整
  - Java+Maven → `mvn`
  - Java+Gradle → `gradle`
  - 前端+pnpm → `pnpm`
  - 前端+yarn → `yarn`
  - 多模块 → `mvn|pnpm`（用 `|` 分隔）

#### .claude/hooks/post-edit-check.ps1

无 `{{...}}` 占位符，需手动编辑 PowerShell 硬编码变量：
- `$FILE_EXTENSIONS = "(java|xml|vue|js|sql)$"` → 根据项目实际文件扩展名调整
- 格式化提醒文本 → 根据项目实际情况调整

---

## 第五步：验证文件完整性

### 5.1 文件存在性检查

检查所有 35 个文件是否已创建/恢复：

```bash
# Windows PowerShell
Get-ChildItem -Recurse -File .claude | Sort-Object Name | Select-Object FullName

# 或 bash
find .claude -type f | sort
```

**预期文件列表（35 个 .claude 文件，按路径排序）**：

```
.claude/agents/sda-architect.md
.claude/agents/sda-backend.md
.claude/agents/sda-build-error-resolver.md
.claude/agents/sda-code-reviewer.md
.claude/agents/sda-db-implementer.md
.claude/agents/sda-frontend.md
.claude/agents/sda-reviewer.md
.claude/agents/sda-tester.md
.claude/commands/sdc-buildfix.md
.claude/commands/sdc-codereview.md
.claude/commands/sdc-dev.md
.claude/commands/sdc-plan.md
.claude/commands/sdc-spec.md
.claude/hooks/post-edit-check.ps1
.claude/hooks/pre-bash-check.ps1
.claude/rules/frontend.md
.claude/rules/git.md
.claude/rules/sda-collaboration.md
.claude/rules/security.md
.claude/rules/testing.md
.claude/settings.json
.claude/skills/troubleshooting.md
.claude/steer/domain/api.md
.claude/steer/domain/frontend.md
.claude/steer/domain/quality-gate.md
.claude/steer/domain/security.md
.claude/steer/domain/testing.md
.claude/steer/foundation/never.md
.claude/steer/foundation/product.md
.claude/steer/foundation/structure.md
.claude/steer/foundation/tech.md
.claude/templates/spec/design.md
.claude/templates/spec/requirements.md
.claude/templates/spec/tasks.md
.claude/templates/spec/test-cases.md
```

加上根目录的 `CLAUDE.md`（根据参考文档模板生成，不在 `find .claude` 输出中），共 36 个文件（35 个 .claude 文件 + 1 个 CLAUDE.md）。

### 5.2 占位符残留检查

检查替换后的文件是否仍有未替换的 `{{...}}` 占位符：

```bash
# 检查配置文件中的占位符（不含规范手册本身，排除 frontend.md 的 {{PLACEHOLDER}} 文档性引用）
grep -rE "{{[A-Z][A-Z_]+}}" .claude/ --include="*.md" --include="*.json" --include="*.ps1" | grep -v "frontend.md"

# 检查 CLAUDE.md
grep -E "{{[A-Z][A-Z_]+}}" CLAUDE.md
```

> **排除说明**：frontend.md 中的 `{{PLACEHOLDER}}` 是禁止提交占位符规则的示例引用，非需替换的变量，grep 检查时需排除该文件。

**判断标准**：
- 有未替换的占位符 → 标注为"待填写"，提示用户后续手动补充
- 无未替换的占位符 → 该文件通过验证

### 5.3 关键内容验证

逐个检查以下文件的关键内容是否正确：

| 检查项 | 文件 | 验证方法 |
|--------|------|---------|
| 项目名称正确 | CLAUDE.md | `{{PROJECT_NAME}}` 已替换 |
| 技术栈正确 | tech.md | `{{FRONTEND_FRAMEWORK}}`、`{{BACKEND_FRAMEWORK}}` 已替换 |
| 目录结构正确 | structure.md | `{{DIR_TREE}}` 已替换为实际目录树 |
| 禁止目录正确 | never.md | `{{CORE_DIR}}` 已替换 |
| API glob 正确 | api.md | `fileMatchPattern` 已手动编辑为项目实际路径 |
| 构建命令正确 | tech.md / quality-gate.md | `{{BUILD_CMD}}` 已替换 |
| 包管理器正确 | settings.json / hooks | `{{PACKAGE_MANAGER}}` 已替换、`$PACKAGE_MANAGER` 已手动编辑 |
| 文件扩展名正确 | hooks | `$FILE_EXTENSIONS` 已手动编辑 |
| 测试命令正确 | rules/testing.md | `{{TEST_CMD}}`、`{{CURRENT_COVERAGE}}`、`{{COVERAGE_CMD}}` 已替换 |
| .gitignore 包含 .env | .gitignore | `grep .env .gitignore` |

### 5.4 最终验证报告

生成验证报告，格式如下：

```
=== 项目初始化验证报告 ===

文件完整性：
  ✅ 已创建：35/35 个 .claude 文件
  ✅ CLAUDE.md 已生成
  ✅ .gitignore 已追加 .env
  ⬜ 被用户跳过：0 个文件（如有则列出）

占位符替换：
  ✅ 已替换：{N} 个占位符
  ⬜ 待填写：{M} 个占位符（列出具体文件和占位符名称）
  ✅ 无残留的文件：{K} 个

关键内容验证：
  ✅ 项目名称：{PROJECT_NAME}
  ✅ 技术栈：{TECH_STACK}
  ✅ 数据库：{DB_TYPE}
  ✅ 目录结构：已填入实际目录树
  ⬜ 人工填写项：{列出未填写的占位符}

下一步：
  1. 手动填写标记为"待填写"的占位符
  2. 确认 rules/ 下的分档标记（🔴🟡🟢）是否符合团队实际
  3. 提交 Git（参考 CLAUDE-CODE-TEAM-SETUP-GUIDE.md 第四章）
  4. 执行质量门禁（参考第五章）
```

---

## 附录：特殊场景处理

### A. 项目无后端（纯前端）

- 删除 tech.md 中的"后端"行、"Maven 编译规范"章节、"数据库字符集规范"中 MySQL 相关内容
- 删除 security.md 中的 `application.yml`、MyBatis `#{}` vs `${}` 引用，改为 `.env` / config.js
- 删除 testing.md 中的 `@Disabled/@Ignore`、`System.out.println` 引用
- structure.md 的修改导航中删除"新增数据库表"、"修改业务逻辑"行（如无后端）
- settings.json 中删除 `Bash(mvn **)` 权限
- hooks 中删除 Maven 相关匹配

### B. 项目无前端（纯后端）

- 删除 frontend.md（或标记为"不适用"）
- 删除 testing.md 中的 E2E 测试基础设施章节、`it.skip/describe.skip`、`console.log` 引用
- 删除 structure.md 的修改导航中"新增前端页面"行
- CLAUDE.md 的核心目录表中删除前端目录行

### C. .claude 文件已在 git 中但工作树缺失

优先使用 `git restore .claude/` 恢复，而非从 claudeConfig 复制。恢复后再执行占位符替换步骤。

### D. 多模块前后端分离项目

占位符值需分行标注后端和前端，如：
- `{{PACKAGE_MANAGER}}` → `Maven（后端）/ pnpm（前端）`
- `{{BUILD_CMD}}` → `mvn package（后端）/ pnpm build（前端）`
- `{{TEST_CMD}}` → `mvn test（后端）/ pnpm test（前端）`

settings.json 的 allow 权限需包含两个包管理器：
```json
"allow": [
  "Bash(mvn **)",
  "Bash(pnpm **)",
  "Bash(git **)",
  "Bash(node **)"
]
```

hooks 的 PACKAGE_MANAGER 匹配需包含两个：
```powershell
$PACKAGE_MANAGER = "mvn|pnpm"
```