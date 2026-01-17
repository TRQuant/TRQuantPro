# Cursor 2.3 功能快速参考

> **快速参考**: Cursor 2.3新功能的使用方法

---

## 🚀 快速开始

### 1. Rules已配置 ✅

Rules文件已创建在 `.cursor/rules/` 目录：
- ✅ `coding-standards.md` - 编码规范
- ✅ `architecture.md` - 架构规范
- ✅ `notebook-development.md` - Notebook开发规范
- ✅ `market-trend-analysis.md` - 市场趋势分析规范

**验证**: 在Cursor Chat中询问编码规范，AI应引用Rules。

### 2. Commands（待配置）

Commands目录已创建：`.cursor/commands/`

**使用方式**:
```
@command 命令名
"执行操作"
```

### 3. Import Settings

**位置**: Cursor设置 → General > Account → VS Code Import

**用途**: 从VS Code导入扩展、主题、设置

### 4. Claude Skills

**状态**: ⚠️ 需要Nightly版本

**启用步骤**:
1. 设置 → Beta → 更新渠道 → Nightly
2. 设置 → Rules → Import Settings → Agent Skills → 开启

**替代方案**: 使用现有的MCP Server架构（推荐）

---

## 📝 Rules使用示例

### 在Chat中测试Rules

```
"请按照TRQuant编码规范创建一个新的Python模块"
```

AI应该：
- ✅ 使用snake_case命名
- ✅ 遵循导入规范
- ✅ 包含docstring
- ✅ 遵循架构规范

### 引用特定Rule

```
"请按照market-trend-analysis规则创建市场趋势分析模块"
```

---

## 🎯 针对市场趋势分析Notebook的建议

### 使用Rules指导开发

1. **编码规范**: 确保代码符合项目标准
2. **架构规范**: 确保模块组织正确
3. **Notebook规范**: 确保Notebook初始化正确
4. **市场趋势规范**: 确保遵循工作流程

### 使用Agent模式

切换到Agent模式（`Ctrl + Alt + Tab`），让AI自动执行多步骤任务。

### 使用MCP工具

```
"请使用market.trend工具分析当前市场趋势"
```

---

## 📚 详细文档

- 完整研究文档: `docs/02_development_guides/CURSOR_2.3_FEATURES_RESEARCH.md`
- Rules说明: `.cursor/README.md`

---

**最后更新**: 2026-01-06
