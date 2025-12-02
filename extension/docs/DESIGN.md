# TRQuant Cursor Extension 设计文档

## 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 0.1.0 | 2025-12-02 | TRQuant | 初始设计 |

---

## 一、系统概述

### 1.1 项目背景

TRQuant Cursor Extension 是一个为 Cursor IDE 开发的量化投资助手插件，旨在：

1. **提供A股量化分析能力**：市场状态、投资主线、因子推荐
2. **自动生成策略代码**：支持 PTrade 和 QMT 两大平台
3. **与AI深度集成**：通过 MCP 协议让 Cursor AI 调用量化工具
4. **跨平台支持**：Linux 和 Windows 双平台

### 1.2 目标用户

- 量化策略研究员
- 程序化交易开发者
- 使用 PTrade/QMT 的券商用户

### 1.3 参考项目

- QuantConnect MCP Server
- 金融数据 MCP Server
- VS Code Extension API

---

## 二、系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        Cursor IDE                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │ TRQuant Extension│  │ Cursor Composer  │  │ .cursor/rules │ │
│  │                  │  │ (AI Agent)       │  │               │ │
│  │ • Commands       │  │                  │  │ • architecture│ │
│  │ • WebView        │  │ 自动调用MCP工具   │  │ • prompts     │ │
│  │ • StatusBar      │  │                  │  │ • style       │ │
│  └────────┬─────────┘  └────────┬─────────┘  └───────────────┘ │
│           │                     │                               │
│           │    ┌────────────────┴────────────────┐              │
│           │    │         MCP Protocol            │              │
│           │    └────────────────┬────────────────┘              │
└───────────┼─────────────────────┼───────────────────────────────┘
            │                     │
            ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TRQuant Python Backend                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐│
│  │ bridge.py    │  │ mcp_server.py│  │ TRQuant Core           ││
│  │              │  │              │  │                        ││
│  │ JSON/stdio   │  │ MCP Protocol │  │ ├── TrendAnalyzer      ││
│  │ 与Extension  │  │ 与Cursor AI  │  │ ├── CandidatePool      ││
│  │ 通信         │  │ 通信         │  │ ├── FactorManager      ││
│  └──────────────┘  └──────────────┘  │ ├── StrategyGenerator  ││
│                                      │ │   ├── PTrade         ││
│                                      │ │   └── QMT            ││
│                                      │ └── BacktestEngine     ││
│                                      └────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      数据层                                      │
├─────────────────────────────────────────────────────────────────┤
│  • JQData (行情/财务)  • AKShare (宏观)  • MongoDB (本地存储)    │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 模块职责

| 模块 | 职责 | 技术 |
|------|------|------|
| Extension | 命令注册、UI渲染、与后端通信 | TypeScript |
| bridge.py | Extension与TRQuant Core的桥接 | Python |
| mcp_server.py | MCP协议实现，供Cursor AI调用 | Python |
| TRQuant Core | 核心业务逻辑 | Python |
| Rules | AI行为指导 | MDC格式 |

### 2.3 通信协议

#### 2.3.1 Extension ↔ Bridge (JSON over stdio)

**请求格式：**
```json
{
  "action": "get_market_status",
  "params": {
    "universe": "CN_EQ",
    "as_of": "2025-12-02"
  }
}
```

**响应格式：**
```json
{
  "ok": true,
  "data": {
    "regime": "risk_on",
    "summary": "..."
  },
  "error": null
}
```

#### 2.3.2 MCP Protocol (JSON-RPC 2.0)

**工具调用：**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "trquant_get_market_status",
    "arguments": {}
  }
}
```

---

## 三、功能设计

### 3.1 命令列表

| 命令 | 功能 | 快捷键 |
|------|------|--------|
| TRQuant: 获取市场状态 | 分析当前市场Regime | - |
| TRQuant: 获取投资主线 | 返回TOP20投资主线 | - |
| TRQuant: 推荐因子 | 基于市场状态推荐因子 | - |
| TRQuant: 生成策略代码 | 生成PTrade/QMT策略 | - |
| TRQuant: 分析回测结果 | 分析回测，给出优化建议 | - |
| TRQuant: 启用MCP Server | 注册MCP到Cursor | - |
| TRQuant: 打开控制面板 | 显示综合面板 | - |

### 3.2 策略生成器设计

#### 3.2.1 支持平台

| 平台 | 说明 | 函数规范 |
|------|------|----------|
| **PTrade** | 恒生PTrade | initialize(), handle_data() |
| **QMT** | 迅投QMT | init(), handlebar() |

#### 3.2.2 策略风格

| 风格 | 代码 | 说明 |
|------|------|------|
| 多因子选股 | multi_factor | 综合因子评分选股 |
| 动量成长 | momentum_growth | 追逐强势成长股 |
| 价值投资 | value | 低估值高分红 |
| 市场中性 | market_neutral | 多空对冲 |

#### 3.2.3 风控参数

```python
risk_params = {
    "max_position": 0.1,      # 单票最大仓位
    "stop_loss": 0.08,        # 止损线
    "take_profit": 0.2,       # 止盈线
    "max_drawdown": 0.15,     # 最大回撤限制
    "rebalance_freq": "daily" # 调仓频率
}
```

### 3.3 MCP工具设计

| 工具名 | 功能 | 参数 |
|--------|------|------|
| trquant_get_market_status | 市场状态 | universe, as_of |
| trquant_get_mainlines | 投资主线 | top_n, time_horizon |
| trquant_recommend_factors | 因子推荐 | market_regime |
| trquant_generate_strategy | 策略生成 | factors, style, platform |
| trquant_analyze_backtest | 回测分析 | backtest_file |
| trquant_risk_assessment | 风险评估 | portfolio |

---

## 四、跨平台设计

### 4.1 平台差异

| 特性 | Linux | Windows |
|------|-------|---------|
| Python路径 | python3 | python |
| 路径分隔符 | / | \\ |
| 换行符 | LF | CRLF |
| Shell | bash/zsh | cmd/powershell |

### 4.2 解决方案

1. **Python路径**：配置项 `trquant.pythonPath`
2. **路径处理**：使用 `path.join()` 和 `Path`
3. **脚本**：提供 `.sh` 和 `.bat` 双版本
4. **环境变量**：统一使用 `os.environ`

---

## 五、数据流设计

### 5.1 获取市场状态

```
User → Command Palette
        ↓
Extension.getMarketStatus()
        ↓
TRQuantClient.callBridge("get_market_status")
        ↓
bridge.py → TrendAnalyzer.analyze_market()
        ↓
Response → WebView显示 + StatusBar更新
```

### 5.2 生成策略代码

```
User → 选择策略风格/平台
        ↓
Extension.generateStrategy()
        ↓
TRQuantClient.getMarketStatus()
TRQuantClient.getMainlines()
TRQuantClient.recommendFactors()
        ↓
TRQuantClient.generateStrategy({factors, style, platform})
        ↓
bridge.py → StrategyGenerator.generate(platform="ptrade|qmt")
        ↓
Response → 新建文件显示代码 → 可保存
```

---

## 六、错误处理

### 6.1 错误类型

| 错误 | 处理 |
|------|------|
| Python未安装 | 提示安装Python |
| TRQuant Core不可用 | 使用Mock数据 |
| 网络超时 | 显示错误，提供重试 |
| 数据源异常 | 降级到本地缓存 |

### 6.2 日志级别

- **DEBUG**: 详细调试信息
- **INFO**: 正常操作日志
- **WARN**: 警告但不影响功能
- **ERROR**: 错误需要处理

---

## 七、安全考虑

1. **不存储敏感信息**：API密钥等通过环境变量
2. **本地通信**：Extension与Bridge仅本地通信
3. **输入验证**：所有参数进行类型检查
4. **权限最小化**：Extension只请求必要权限

---

## 八、测试策略

### 8.1 单元测试

- bridge.py 各action函数
- TypeScript 服务类方法

### 8.2 集成测试

- Extension ↔ Bridge 通信
- MCP Server 协议兼容

### 8.3 E2E测试

- 完整工作流测试
- 跨平台验证

---

## 九、版本规划

| 版本 | 功能 | 时间 |
|------|------|------|
| 0.1.0 | MVP（4个基础命令） | Week 1-3 |
| 0.2.0 | MCP集成 | Week 4-6 |
| 0.3.0 | 进阶功能（回测、风控） | Week 7-10 |
| 1.0.0 | 正式发布 | Week 11-12 |

