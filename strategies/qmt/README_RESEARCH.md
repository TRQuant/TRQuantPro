# QMT研究环境策略代码使用说明

## 📋 策略概述

**TRQuant Advisor V4.0 - QMT研究环境策略**

基于7个已验证因子的多因子选股策略，适用于QMT桌面app研究环境，无需连接交易账户，可直接运行回测。

### 与连接版本的区别

| 特性 | 连接版本 | 研究环境版本 |
|------|---------|-------------|
| 交易对象 | XtQuantTrader + StockAccount | ContextInfo |
| 数据获取 | xtdata.get_market_data_ex() | ContextInfo.get_market_data() |
| 订单执行 | xt_trader.order_stock() | ContextInfo.order() |
| 持仓查询 | xt_trader.query_stock_positions() | ContextInfo.get_trade_detail_data() |
| 账户连接 | 需要连接交易账户 | 无需连接，直接运行 |
| 使用场景 | 实盘交易 | 策略研究和回测 |

### 7个已验证因子

1. **20日动量** (momentum_20d) - 核心因子，权重1.0
2. **相对位置** (rel_position) - 核心因子，权重0.9
3. **市值** (market_cap) - 核心因子，权重0.85
4. **5日动量** (momentum_5d) - 确认因子，权重0.75
5. **换手率** (turnover_rate) - 流动性因子，权重0.7
6. **ROE** (roe) - 基本面因子，权重0.5
7. **净利润增长率** (growth) - 成长性因子，权重0.4

## 🚀 快速开始

### 1. 环境准备

```bash
# QMT研究环境通常已内置pandas和numpy
# 无需额外安装依赖
```

### 2. 在QMT研究环境中加载策略

1. 打开QMT桌面app
2. 进入"研究"或"策略研究"模块
3. 加载策略文件：`TRQuant_V4_QMT_Research_*.py`
4. 设置回测参数（起始日期、结束日期、初始资金等）
5. 点击"运行"或"回测"

### 3. 策略参数调整（可选）

在策略文件中修改以下参数：

```python
# 选股参数
MAX_STOCKS = 10              # 最大持股数量
MIN_TOTAL_SCORE = 30.0       # 最小综合得分

# 仓位参数
SINGLE_POSITION_MAX = 0.2    # 单票最大仓位（20%）

# 止损止盈
STOP_LOSS = -0.08            # 止损（-8%）
TAKE_PROFIT = 0.30           # 止盈（+30%）
```

## 📊 策略逻辑

### 选股流程

1. **获取股票池**: 沪深300成分股
2. **计算因子**: 计算7个已验证因子
3. **因子得分**: 基于理论最优区间计算得分
4. **综合评分**: 加权求和得到综合得分
5. **筛选排序**: 按得分排序，取前N只

### 调仓机制

- **调仓频率**: 每周一次（默认周一09:35）
- **仓位分配**: 等权分配，单票最大20%
- **调仓逻辑**: 卖出不在目标持仓中的股票，买入目标持仓中的股票

### 风控机制

- **止损**: 亏损达到-8%时卖出
- **止盈**: 盈利达到+30%时卖出
- **移动止损**: 盈利超过15%后，从最高价回撤8%时卖出
- **分批止盈**: 盈利达到+20%时卖出50%
- **时间止损**: 持仓超过20个交易日时卖出

## 🔧 QMT研究环境API说明

### ContextInfo对象

QMT研究环境通过`ContextInfo`对象提供所有功能：

```python
# 初始化函数
def init(ContextInfo):
    # 设置股票池
    ContextInfo.set_universe(stock_list)
    
    # 设置定时任务
    ContextInfo.run_time('function_name', '09:35:00', 'SH', weekday='monday')

# 主回调函数
def handlebar(ContextInfo):
    # 获取当前日期
    current_date = ContextInfo.current_dt
    
    # 获取数据
    data = ContextInfo.get_market_data(stock, period='1d', count=20)
    
    # 执行交易
    ContextInfo.order(stock, amount, ContextInfo.MARKET_SH_SZ)
    
    # 获取持仓
    positions = ContextInfo.get_trade_detail_data(ContextInfo.accout_id, 'stock', 'position')
    
    # 获取账户信息
    account = ContextInfo.get_account_info(ContextInfo.accout_id)
```

### 常用API

1. **数据获取**:
   - `ContextInfo.get_market_data(stock, period='1d', count=20)`
   - `ContextInfo.get_stock_list_in_sector(index_code)`
   - `ContextInfo.get_financial_data(stock, fields, date)`

2. **交易执行**:
   - `ContextInfo.order(stock, amount, market_type)`
   - `ContextInfo.get_last_price(stock)`

3. **持仓查询**:
   - `ContextInfo.get_trade_detail_data(account_id, 'stock', 'position')`
   - `ContextInfo.get_account_info(account_id)`

4. **定时任务**:
   - `ContextInfo.run_time('function_name', 'HH:MM:SS', 'SH', weekday='monday')`

## ⚠️ 注意事项

### API差异

1. **数据获取**:
   - 研究环境使用 `ContextInfo.get_market_data()` 而不是 `xtdata.get_market_data_ex()`
   - 参数格式可能不同，需要根据实际QMT API调整

2. **订单执行**:
   - 使用 `ContextInfo.order()` 而不是 `xt_trader.order_stock()`
   - 参数格式：`ContextInfo.order(stock, amount, ContextInfo.MARKET_SH_SZ)`

3. **持仓查询**:
   - 使用 `ContextInfo.get_trade_detail_data()` 获取持仓
   - 属性名可能不同（如 `pos.m_strInstrumentID`, `pos.m_dPrice`）

4. **定时任务**:
   - 使用 `ContextInfo.run_time()` 设置定时任务
   - 语法：`ContextInfo.run_time('function_name', '09:35:00', 'SH', weekday='monday')`

### 数据源说明

- **价格数据**: 从QMT研究环境获取
- **基本面数据**: 需要QMT支持财务数据API，否则相关因子可能无法计算

### 测试建议

1. **研究环境测试**: 在QMT研究环境中直接运行回测
2. **参数调整**: 根据回测结果调整策略参数
3. **API验证**: 确保所有API调用符合QMT研究环境规范
4. **监控日志**: 关注策略运行日志，及时发现问题

## 📁 文件结构

```
strategies/qmt/
├── TRQuant_V4_QMT_Research_*.py    # 研究环境策略代码
├── TRQuant_V4_QMT_*.py             # 连接版本策略代码
├── README.md                        # 连接版本说明
└── README_RESEARCH.md               # 本说明文档（研究环境）
```

## 🔧 故障排查

### 问题1: ContextInfo API调用失败
```
检查项:
1. API函数名是否正确
2. 参数格式是否符合QMT研究环境规范
3. 是否在正确的回调函数中使用
```

### 问题2: 数据获取失败
```
检查项:
1. get_market_data参数是否正确
2. 股票代码格式是否正确（.SH/.SZ）
3. 数据权限是否足够
```

### 问题3: 定时任务不执行
```
检查项:
1. run_time语法是否正确
2. 时间格式是否正确（'HH:MM:SS'）
3. weekday参数是否正确
4. 函数名是否与定义一致
```

### 问题4: 基本面数据无法获取
```
说明: QMT研究环境可能不支持某些基本面数据API
解决方案: 
1. 检查QMT版本是否支持财务数据API
2. 考虑从其他数据源获取基本面数据
3. 调整策略，减少对基本面因子的依赖
```

## 📚 相关文档

- QMT官方文档: https://dict.thinktrader.net/
- QMT研究环境API文档: 请参考QMT桌面app内置文档
- TRQuant策略文档: `docs/advisor_v4/`

## 📝 更新日志

- 2026-01-09: 初始版本，基于7个已验证因子，适用于QMT研究环境

## 💡 使用技巧

### 1. 快速回测

在QMT研究环境中：
1. 加载策略文件
2. 设置回测时间段（如：2024-01-01 至 2024-12-31）
3. 设置初始资金（如：1000000）
4. 点击"运行回测"
5. 查看回测报告和图表

### 2. 参数优化

1. 修改策略参数（如MAX_STOCKS、STOP_LOSS等）
2. 重新运行回测
3. 对比不同参数的回测结果
4. 选择最优参数组合

### 3. 因子分析

1. 在策略代码中添加因子值输出
2. 分析因子分布和相关性
3. 调整因子权重和阈值

## 🔄 版本对比

### 研究环境版本 vs 连接版本

**研究环境版本优势**:
- ✅ 无需连接交易账户
- ✅ 可直接运行回测
- ✅ 适合策略研究和开发
- ✅ 更简单的API调用

**连接版本优势**:
- ✅ 支持实盘交易
- ✅ 实时数据获取
- ✅ 完整的交易功能

**建议**:
- 策略开发阶段：使用研究环境版本
- 策略验证阶段：使用研究环境版本进行回测
- 实盘交易阶段：使用连接版本
