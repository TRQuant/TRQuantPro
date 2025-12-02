# TRQuant Cursor Extension

<div align="center">

![TRQuant Logo](resources/icon.svg)

**A股量化投资助手 - Cursor IDE 插件**

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](CHANGELOG.md)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey.svg)](docs/INSTALLATION.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## ✨ 功能特性

- 📊 **市场状态分析** - 实时获取A股市场Regime、指数趋势、风格轮动
- 🎯 **投资主线识别** - TOP20热门主线、行业轮动、投资逻辑
- 📈 **因子推荐** - 基于市场状态智能推荐量化因子
- 🚀 **策略生成** - 一键生成PTrade/QMT策略代码
- 🤖 **AI深度集成** - 通过MCP协议让Cursor AI调用量化工具
- 🖥️ **跨平台支持** - Linux和Windows双平台

---

## 🚀 快速开始

### 安装

**Linux/macOS:**
```bash
cd extension
./scripts/setup.sh
```

**Windows:**
```powershell
cd extension
.\scripts\setup.bat
```

### 使用

1. 按 `Ctrl+Shift+P` (Windows) 或 `Cmd+Shift+P` (Mac)
2. 输入 "TRQuant" 查看可用命令
3. 选择所需功能

---

## 📋 命令列表

| 命令 | 功能 |
|------|------|
| `TRQuant: 获取市场状态` | 分析当前市场Regime |
| `TRQuant: 获取投资主线` | 返回TOP20投资主线 |
| `TRQuant: 推荐因子` | 智能推荐量化因子 |
| `TRQuant: 生成策略代码` | 生成PTrade/QMT策略 |
| `TRQuant: 分析回测结果` | 分析回测结果 |
| `TRQuant: 打开控制面板` | 显示综合控制台 |

---

## 🔧 策略平台支持

### PTrade (恒生)

```python
def initialize(context):
    context.max_position = 0.1
    run_daily(rebalance, time='9:35')

def handle_data(context, data):
    pass
```

### QMT (迅投)

```python
def init(ContextInfo):
    ContextInfo.max_position = 0.1

def handlebar(ContextInfo):
    pass
```

---

## 🤖 AI集成

通过MCP协议，Cursor AI可以直接调用TRQuant工具：

```
用户: 帮我生成一个适合当前市场的多因子策略

AI: 让我先调用TRQuant工具获取市场信息...
    [调用 trquant_get_market_status]
    [调用 trquant_get_mainlines]
    [调用 trquant_recommend_factors]
    [调用 trquant_generate_strategy]
    
    根据当前市场状态，我为您生成了以下策略...
```

---

## 📁 项目结构

```
extension/
├── src/
│   ├── extension.ts       # 入口
│   ├── commands/          # 命令实现
│   ├── services/          # 后端通信
│   └── views/             # WebView面板
├── python/
│   ├── bridge.py          # Python桥接
│   └── mcp_server.py      # MCP Server
├── rules/                 # Cursor规则文件
├── docs/                  # 文档
└── scripts/               # 安装脚本
```

---

## 📖 文档

- [安装指南](docs/INSTALLATION.md)
- [设计文档](docs/DESIGN.md)
- [使用教程](docs/TUTORIAL.md)
- [API参考](docs/API.md)

---

## 🔗 相关项目

- [TRQuant Core](../) - 量化投资核心库
- [QuantConnect MCP](https://github.com/quantconnect/mcp-server) - 参考实现

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

