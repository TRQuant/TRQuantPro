# Claude Commands 配置说明

> **创建时间**: 2026-01-06  
> **目的**: 为TRQuant项目配置Claude Commands，提高开发效率

---

## 📁 目录结构

```
.claude/
└── commands/
    ├── market-trend-analysis.md      # 市场趋势分析
    ├── run-backtest.md                # 运行回测
    ├── generate-report.md             # 生成报告
    ├── screen-investment-targets.md   # 筛选投资标的
    ├── validate-code.md               # 验证代码
    └── setup-notebook.md              # 初始化Notebook环境
```

---

## 🚀 使用方法

### 在Cursor Chat中

使用 `@` 符号调用命令：

```
@market-trend-analysis
```

### 在Agent模式中

Agent会自动识别和使用这些命令。

---

## 📋 可用命令列表

### 1. market-trend-analysis
**功能**: 运行市场趋势分析

**使用**: `@market-trend-analysis`

**输出**: 趋势得分、趋势方向、市场状态

### 2. run-backtest
**功能**: 运行Phase 1和Phase 2回测

**使用**: `@run-backtest`

**说明**: 执行完整的回测流程，结果保存到MongoDB

### 3. generate-report
**功能**: 生成市场趋势分析报告

**使用**: `@generate-report`

**输出**: JSON格式报告，保存到 `output/reports/`

### 4. screen-investment-targets
**功能**: 筛选投资标的股票

**使用**: `@screen-investment-targets`

**说明**: 基于投资主线筛选，可修改mainline_name参数

### 5. validate-code
**功能**: 运行单元测试验证代码

**使用**: `@validate-code`

**说明**: 运行Core模块的测试，验证代码质量

### 6. setup-notebook
**功能**: 生成Notebook初始化代码

**使用**: `@setup-notebook`

**输出**: 标准初始化代码，可直接复制到Notebook

---

## 🔧 自定义命令

### 创建新命令

1. 在 `.claude/commands/` 目录创建 `.md` 文件
2. 使用MDC格式（Markdown with front matter）
3. 定义 `name`、`description` 和 `command`

### 命令格式

```markdown
---
name: "命令名称"
description: "命令描述"
command: |
  命令内容（可以是多行）
---

# 命令说明文档
```

---

## 💡 最佳实践

1. **命令应该简洁**: 每个命令聚焦一个任务
2. **提供清晰描述**: description字段要准确
3. **使用绝对路径**: 确保命令在任何目录都能运行
4. **错误处理**: 命令应该处理常见错误情况

---

**最后更新**: 2026-01-06
