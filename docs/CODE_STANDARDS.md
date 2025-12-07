# TRQuant 代码规范化指南

## 📚 概述

本文档基于 **Compound Engineering** 理念，旨在让每次代码生成都更规范、更易维护。参考了 [compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) 的设计思想。

## 🎯 核心理念

> **每次代码生成都应该让后续代码更容易写**

### Compound Engineering 原则

1. **文档化模式**：每次代码生成都记录模式，供后续参考
2. **创建可复用组件**：提取通用逻辑为可复用组件
3. **建立约定**：减少决策疲劳，提高一致性
4. **编码知识**：将知识转化为代码和文档

## 🛠️ 工具链

### Python 工具

| 工具 | 用途 | 安装 |
|------|------|------|
| **Black** | 代码格式化 | `pip install black` |
| **Ruff** | 快速 Linting | `pip install ruff` |
| **mypy** | 类型检查 | `pip install mypy` |
| **pytest** | 测试框架 | `pip install pytest` |

### TypeScript/JavaScript 工具

| 工具 | 用途 | 安装 |
|------|------|------|
| **Prettier** | 代码格式化 | `npm install -D prettier` |
| **ESLint** | 代码检查 | `npm install -D eslint` |
| **TypeScript** | 类型检查 | 已包含在项目中 |

### 快速安装

```bash
# 运行安装脚本
./scripts/setup_code_quality.sh
```

## 📋 代码规范

### Python 规范

详见 `.cursorrules` 文件中的详细规范。

**关键要点**：
- PEP 8 严格遵循
- 类型提示必须
- 文档字符串（Google 风格）
- 行长度 100 字符

### TypeScript 规范

详见 `.cursorrules` 文件中的详细规范。

**关键要点**：
- TypeScript 严格模式
- 避免 `any` 类型
- 2 空格缩进
- 单引号优先

## 🔄 工作流程

### 1. 代码生成前

1. **分析现有模式**
   ```bash
   # 查找类似实现
   grep -r "similar_pattern" .
   ```

2. **检查架构约束**
   - 查看 `.cursorrules` 中的架构规范
   - 确认文件保护级别
   - 检查依赖关系

### 2. 代码生成时

遵循 `.cursorrules` 中的规范：
- 使用正确的命名规范
- 添加类型注解
- 编写文档字符串
- 处理错误情况

### 3. 代码生成后

1. **格式化代码**
   ```bash
   # Python
   black .
   ruff check .
   
   # TypeScript
   cd extension
   npx prettier --write .
   npx eslint .
   ```

2. **运行测试**
   ```bash
   # Python
   pytest
   
   # TypeScript
   npm run test
   ```

3. **类型检查**
   ```bash
   # Python
   mypy .
   
   # TypeScript
   npm run type-check
   ```

## 📝 Cursor AI 使用指南

### 在 Cursor 中使用

1. **确保 `.cursorrules` 文件存在**
   - 项目根目录应有 `.cursorrules` 文件
   - Cursor 会自动读取并应用规则

2. **使用 AI 生成代码时**
   - Cursor 会根据 `.cursorrules` 自动应用规范
   - 生成的代码应该符合项目规范

3. **代码审查**
   - 使用 `/compound-engineering:review` 理念
   - 检查代码是否符合规范
   - 运行格式化工具验证

### 示例：生成新功能

```
用户: 添加一个新的动量因子计算函数

AI 应该：
1. 查看 core/factors/momentum_factors.py 的现有模式
2. 遵循命名规范（snake_case）
3. 添加类型提示和文档字符串
4. 处理错误情况
5. 生成符合 Black 格式的代码
```

## 🔍 代码审查清单

### Python 代码审查

- [ ] 遵循 PEP 8 规范
- [ ] 有类型提示
- [ ] 有文档字符串
- [ ] 错误处理完善
- [ ] 通过 Black 格式化
- [ ] 通过 Ruff 检查
- [ ] 通过 mypy 类型检查
- [ ] 有单元测试

### TypeScript 代码审查

- [ ] 遵循 ESLint 规则
- [ ] 无 `any` 类型
- [ ] 有 JSDoc 注释
- [ ] 错误处理完善
- [ ] 通过 Prettier 格式化
- [ ] 通过 TypeScript 编译
- [ ] 有单元测试

## 🚀 与 Compound Engineering Plugin 的对比

| 功能 | Compound Engineering Plugin | TRQuant 方案 |
|------|---------------------------|--------------|
| **代码规划** | `/compound-engineering:plan` | `.cursorrules` + AI 提示 |
| **代码执行** | `/compound-engineering:work` | Cursor AI + 工作流 |
| **代码审查** | `/compound-engineering:review` | 工具链 + 检查清单 |
| **代码规范化** | 内置规则 | `.cursorrules` + 格式化工具 |

### 优势

1. **无需额外安装**：使用 Cursor 内置功能
2. **完全定制**：根据项目需求定制规则
3. **工具链集成**：与现有开发工具无缝集成
4. **跨语言支持**：同时支持 Python 和 TypeScript

## 📚 参考资源

- [Compound Engineering Plugin](https://github.com/EveryInc/compound-engineering-plugin)
- [PEP 8 Style Guide](https://pep8.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [ESLint Rules](https://eslint.org/docs/rules/)

## 🔄 持续改进

### 如何更新规范

1. **收集问题**：记录代码审查中发现的问题
2. **更新规则**：修改 `.cursorrules` 文件
3. **更新工具**：调整格式化工具配置
4. **团队同步**：确保团队成员了解更新

### 反馈机制

- 在代码审查中记录规范问题
- 定期回顾和更新规范
- 分享最佳实践

---

**最后更新**: 2025-12-06  
**维护者**: TRQuant 开发团队







