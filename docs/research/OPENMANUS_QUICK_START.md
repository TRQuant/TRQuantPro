# OpenManus 快速开始指南

> **创建时间**: 2026-01-11  
> **目的**: 快速了解OpenManus能做什么，如何开始使用

---

## 🎯 OpenManus能做什么？

OpenManus提供了4个核心工具，可以与TRQuant系统集成：

### 1. 🌐 浏览器自动化 (BrowserUseTool)

**能做什么**:
- ✅ 访问网页（如东方财富、同花顺等财经网站）
- ✅ 点击按钮、填写表单、选择下拉菜单
- ✅ 提取网页内容（价格、新闻、数据等）
- ✅ 截图和录制
- ✅ 网页搜索

**在TRQuant中的应用**:
- 📊 抓取实时行情数据
- 📰 收集财经新闻和公告
- 📈 获取财务报表和宏观数据
- 🔍 数据源检测和验证

**示例**:
```
在Cursor Chat中: "使用openmanus的browser工具访问东方财富，搜索000001，获取当前价格"
```

---

### 2. 💻 命令行工具 (Bash)

**能做什么**:
- ✅ 执行Shell命令
- ✅ 文件操作（创建、删除、移动）
- ✅ 运行数据处理脚本
- ✅ 系统维护任务

**在TRQuant中的应用**:
- 🔄 数据处理和转换
- 📁 文件批量操作
- 🛠️ 系统维护
- 🚀 自动化脚本执行

**示例**:
```
在Cursor Chat中: "使用openmanus的bash工具运行数据处理脚本 process_data.py"
```

---

### 3. 📝 代码编辑器工具 (StrReplaceEditor)

**能做什么**:
- ✅ 读取文件
- ✅ 修改代码（基于字符串替换）
- ✅ 生成代码（基于模板）
- ✅ 保存文件

**在TRQuant中的应用**:
- 💡 策略代码自动生成
- ⚙️ 配置文件修改
- 🔧 代码重构
- 📋 模板填充

**示例**:
```
在Cursor Chat中: "使用openmanus的editor工具，基于MA交叉策略模板，生成一个策略代码"
```

---

### 4. 🔌 MCP服务器

**能做什么**:
- ✅ 提供MCP协议接口
- ✅ 供Cursor Chat调用
- ✅ 工具统一管理

**在TRQuant中的应用**:
- 🔗 通过Cursor Chat使用OpenManus工具
- 🔄 与其他MCP服务器集成
- 🎯 工作流自动化

---

## 🚀 快速开始

### 步骤1: 安装OpenManus（已完成）✅

- ✅ 已安装到: `third_party/OpenManus/`
- ✅ 虚拟环境: `.venv/`
- ✅ 依赖已安装

### 步骤2: 配置MCP服务器（下一步）

在 `.cursor/mcp.json` 中添加配置:

```json
{
  "mcpServers": {
    "openmanus": {
      "command": "/home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus/.venv/bin/python",
      "args": ["-m", "app.mcp.server"],
      "env": {
        "PYTHONPATH": "/home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus"
      }
    }
  }
}
```

### 步骤3: 测试使用

在Cursor Chat中:
```
"使用openmanus的browser工具访问 https://www.eastmoney.com"
```

---

## 📊 实际应用场景

### 场景1: 财经数据抓取 📈

**需求**: 从东方财富网站获取实时股票价格

**使用工具**: BrowserUseTool

**在Cursor Chat中**:
```
"使用openmanus的browser工具访问东方财富网站，搜索000001，获取当前价格"
```

**结果**: 自动访问网站，提取价格信息

---

### 场景2: 策略代码生成 💡

**需求**: 基于模板生成策略代码

**使用工具**: StrReplaceEditor

**在Cursor Chat中**:
```
"使用openmanus的editor工具，基于MA交叉策略模板，生成一个策略，参数为10日和30日均线"
```

**结果**: 自动生成策略代码文件

---

### 场景3: 数据处理自动化 🔄

**需求**: 自动化数据处理流程

**使用工具**: Bash + BrowserUseTool

**在Cursor Chat中**:
```
"使用openmanus工具自动化执行：
1. 使用browser工具从网站下载CSV数据
2. 使用bash工具运行数据处理脚本
3. 保存处理后的数据"
```

**结果**: 自动完成整个数据处理流程

---

## 🎨 与TRQuant工作流集成

### R0: 数据源检测
- 使用BrowserUseTool检测数据源可用性
- 验证财经网站连接

### R1: 市场趋势分析
- 使用BrowserUseTool收集市场新闻
- 提取关键信息

### R3: 因子组合开发
- 使用StrReplaceEditor生成因子计算代码
- 批量创建因子

### R6: 策略开发与回测
- 使用StrReplaceEditor生成策略代码
- 自动化策略创建

---

## ✅ 总结

### OpenManus能做什么？

1. **浏览器自动化** - 抓取网页数据、自动化网页操作
2. **命令行执行** - 运行脚本、文件操作
3. **代码编辑** - 代码生成、文件修改
4. **MCP服务器** - 通过Cursor Chat调用

### 在TRQuant中的价值

- ✅ 增强数据收集能力
- ✅ 自动化工作流
- ✅ 代码自动生成
- ✅ 与Cursor深度集成

### 下一步

1. 配置MCP服务器到Cursor
2. 测试工具功能
3. 开发实际应用
4. 集成到工作流

---

**更多信息**: 查看 `docs/research/OPENMANUS_CAPABILITIES_GUIDE.md`
