# Cursor Rules 配置说明

> **创建时间**: 2026-01-06  
> **目的**: 为TRQuant项目配置Cursor Rules，指导AI行为

---

## 📁 目录结构

```
.cursor/
├── rules/                          # Rules规则文件
│   ├── coding-standards.md        # 编码规范（always）
│   ├── architecture.md            # 架构规范（always）
│   ├── notebook-development.md    # Notebook开发规范（auto-attached）
│   └── market-trend-analysis.md   # 市场趋势分析规范（agent-requested）
└── commands/                       # Commands命令文件（待创建）
```

---

## 📋 Rules说明

### 1. coding-standards.md
- **类型**: `always` - 始终应用
- **用途**: Python编码规范、命名规范、导入规范
- **适用**: 所有代码文件

### 2. architecture.md
- **类型**: `always` - 始终应用
- **用途**: 三层架构规范、模块组织原则
- **适用**: 所有代码文件

### 3. notebook-development.md
- **类型**: `auto-attached` - 自动附加到`.ipynb`文件
- **用途**: Notebook开发规范、初始化模式、可视化规范
- **适用**: 所有`.ipynb`文件

### 4. market-trend-analysis.md
- **类型**: `agent-requested` - 代理请求时应用
- **用途**: 市场趋势分析开发规范、工作流程
- **适用**: 市场趋势分析相关任务

---

## 🚀 使用方法

### 在Cursor Chat中

Rules会自动应用，AI会遵循这些规范：

```
"请创建一个新的市场趋势分析模块"
```

AI会：
- ✅ 遵循编码规范
- ✅ 遵循架构规范
- ✅ 使用正确的模块组织
- ✅ 遵循工作流程术语

### 手动引用Rules

```
"请按照market-trend-analysis规则创建分析模块"
```

---

## 📝 更新Rules

1. 编辑对应的`.md`文件
2. 保存文件
3. Cursor会自动重新加载Rules

---

## 🔍 验证Rules是否生效

在Cursor Chat中测试：

```
"请按照TRQuant编码规范创建一个Python模块"
```

如果AI引用了Rules中的规范，说明Rules已生效。

---

**最后更新**: 2026-01-06
