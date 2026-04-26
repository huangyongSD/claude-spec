---
inclusion: fileMatch
fileMatchPattern: ["**/*Test.java", "**/test/**/*.java"]
---

# 测试规范

> 本文件在编辑测试文件时加载。

## 测试文件命名

- 单元测试：`*Test.java` 或 `*ServiceTest.java`
- 集成测试：`*IntegrationTest.java`
- E2E 测试：`e2e/**/*.spec.ts`

## 测试文件位置

- 单元测试：与被测文件同目录（如 `service/impl/XxxServiceImplTest.java`）
- 集成测试：`test/` 目录
- E2E 测试：`tests/e2e/` 目录

## 测试结构

```java
@SpringBootTest
class XxxServiceTest {
    @Test
    void shouldCreateXxx() {
        // given
        // when
        // then
    }
}
```

## Mock 规范

- 使用 Mockito 创建 mock 对象
- Mock 文件放在测试目录
- 只 mock 外部依赖，不 mock 被测单元本身

## 覆盖率要求

- 核心业务逻辑：目标 80%（当前无配置）
- 新增代码必须附带测试
- 不允许提交跳过测试的代码（`@Disabled`、`@Ignore`）

## 常见错误

1. 异步测试忘记 `async/await` 或 `.resolves()`
2. Mock 路径不正确导致 mock 不生效
3. 测试之间没有隔离，依赖执行顺序
