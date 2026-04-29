# claude-spec

基于 Claude Code 的 AI 协作开发脚手架，适用于任何 **Java 后端 + 前端** 技术栈项目。通过结构化的 Spec 驱动流程，实现规范化的全栈开发。

技术栈信息由 `/sds-init` 自动扫描并填充，适配 Spring Boot / DJL / JHipster 等任意 Java 框架。

## 环境依赖

| 依赖 | 说明 |
|------|------|
| Python 3 | 工具脚本执行（db-query / secrets-sync） |
| Maven | 后端构建（由 sds-init 自动检测） |
| npm | 前端构建（由 sds-init 自动检测） |

## 核心 Skills

### `/sds-init` — 项目初始化

扫描项目源码，自动提取技术栈、数据库、中间件、目录结构、代码模式等信息，填充 `.claude/` 配置文件中所有项目信息段落。

```
扫描项目源码 → 展示结果确认 → 替换 14 个配置文件 → 评审验证 → 最终报告
```

**替换范围**：CLAUDE.md、structure.md、dbinfo.md、各 SDA Agent 配置（sda-db-implementer / sda-backend / sda-frontend / sda-tester 等）、rules 文件（security / frontend / testing / governance）

**不替换**：settings.json、hooks、tools、规则/治理/流程内容

---

### `/sds-spec` — 需求规格化

将需求转化为结构化 Spec 文档，作为开发的唯一依据。**必须先 Spec 再开发**。

```
整理需求概要 → 创建 Spec 目录 → requirements.md → 评审 → design.md → 评审 → test-cases.md → 评审 → tasks.md → 评审
```

**四个核心文件**：

| 文件 | 内容 |
|------|------|
| `requirements.md` | 验收条件（AC）+ 业务规则（BR）+ 影响范围 |
| `design.md` | 数据库设计 + API 设计 + 安全设计 + 前端设计 + 性能约束 |
| `test-cases.md` | 单元测试 + E2E 测试用例，覆盖所有 AC |
| `tasks.md` | 任务清单 + AC→任务追溯矩阵 |

每个文件生成后必须经过 `sda-doc-reviewer` 评审，最多 5 轮，5 轮后由用户决策。

---

### `/sds-dev` — 全栈开发编排

根据 Spec 文件串行调度 SDA 执行实现，每阶段含评审和编译验证。

```
DB实现 → 评审 → 后端实现 → 评审 → 编译验证
→ 前端实现 → 评审 → 编译验证
→ 测试执行 → 评审
→ 全量审查 → 修复 → 质量门禁 → Git提交
```

**六阶段流程**：

| 阶段 | SDA | 关键产出 |
|------|-----|---------|
| 1. 数据库 | sda-db-implementer | SQL + DO + Mapper |
| 2. 后端 | sda-backend | VO + Service + Controller |
| 3. 前端 | sda-frontend | API + 页面 + 组件 |
| 4. 测试 | sda-tester | UT + E2E |
| 5. 全量审查 | sda-code-reviewer | P0/P1/P2 问题清单 |
| 6. 质量门禁 | 主 CC | 全量编译验证 |

**质量门禁（P0 阻断交付）**：
- `mvn clean compile` 后端编译通过
- `npm run build:prod` 前端构建通过
- `mvn test` 单元测试零失败
- 无敏感信息泄露
- 无 TODO/FIXME/placeholder 残留

**SDA 配置索引**：sda-db-implementer / sda-backend / sda-frontend / sda-tester / sda-doc-reviewer / sda-code-reviewer / sda-build-error-resolver 均使用 `.claude/agents/` 下的独立配置文件。

## 工作流总览

```
沟通任务 → /sds-plan（高风险操作）→ /sds-spec → Spec 评审 → /sds-dev → 编译验证 → Git 提交
```

**豁免条件**：用户说"直接改"/"不用规划"，或单文件小改动（bug 修复、配置调整）。

## 快速开始

```bash
# 1. 初始化项目（首次使用时调用）
/sds-init

# 2. 描述需求
# 向 AI 描述要开发的功能，如"实现用户管理模块的增删改查"

# 3. 生成 Spec 文档
/sds-spec

# 4. 开始开发
/sds-dev
```

## 目录结构

```
.claude/
├─ agents/          # SDA Agent 配置（db/backend/frontend/tester 等）
├─ knowledge/       # 知识库（structure/dbinfo/troubleshooting）
├─ rules/           # 编码规则（security/frontend/testing/governance）
├─ skills/          # Skills（sds-init/sds-spec/sds-dev 等）
├─ specs/           # Spec 文档输出目录（按功能模块组织）
├─ templates/spec/  # Spec 文件模板
├─ tools/           # 工具脚本（db-query/secrets-sync）
└─ hooks/           # Git Hooks
```

## 红线规则

1. **禁止硬编码密钥/SQL 拼接** — 参数化查询，`${}` 存在注入风险
2. **禁止提交真实密码/IP** — 使用占位符 `{{VAR}}`
3. **新功能必须先 Spec 再开发** — 跳过 Spec 直接写代码属违规
4. **框架层修改需通过 `/sds-plan`** — 涉及重构或引入新依赖时必须先规划
5. **业务逻辑放在 Service 层** — Controller 仅负责路由和参数组装

## 相关文档

- [CLAUDE.md](CLAUDE.md) — 项目信息和导航
- [.claude/rules/security.md](.claude/rules/security.md) — 安全底线规则
- [.claude/rules/governance.md](.claude/rules/governance.md) — 流程治理规则
- [.claude/skills/sds-spec/SKILL.md](.claude/skills/sds-spec/SKILL.md) — Spec 详细规范
- [.claude/skills/sds-dev/SKILL.md](.claude/skills/sds-dev/SKILL.md) — 开发编排详细规范
