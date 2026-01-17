# PTrade策略代码使用说明

## 📋 策略概述

**TRQuant Advisor V4.0 - PTrade策略**

基于7个已验证因子的多因子选股策略，100%使用已验证因子，不使用聚宽因子。

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
# PTrade平台要求Python 3.11
# 确保已安装pandas和numpy
pip install pandas numpy
```

### 2. 配置参数

打开策略文件，根据PTrade实际API调整以下函数：

```python
# 数据获取函数（需要根据PTrade实际API调整）
def get_price_ptrade(stocks, count=None, fields=None):
    # PTrade使用get_klines API
    # 需要根据实际PTrade API文档调整
    pass

def get_fundamentals_ptrade(stocks, date_str, fields=None):
    # PTrade基本面数据API
    # 需要根据实际PTrade API文档调整
    pass
```

### 3. 策略参数调整（可选）

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

### 4. 运行策略

在PTrade平台中加载策略文件并运行。

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

## ⚠️ 注意事项

### PTrade API差异

1. **股票代码格式**:
   - PTrade使用 `.SH` / `.SZ` 格式（不是 `.XSHG` / `.XSHE`）
   - 策略代码中已处理格式转换

2. **数据获取API**:
   - 使用 `get_klines()` 而不是 `get_price()`
   - 参数格式可能不同：`get_klines(security, count, frequency='1d')`
   - 需要根据实际PTrade API文档调整

3. **定时任务**:
   - 使用 `schedule()` 函数而不是 `run_daily()` / `run_weekly()`
   - 语法：`schedule(time='09:35', func=rebalance, weekday='monday')`

4. **订单API**:
   - PTrade可能使用 `order()` 或 `order_to()` 函数
   - 需要根据实际PTrade API文档调整

5. **持仓查询**:
   - 使用 `get_positions()` 获取持仓
   - 属性名可能不同（如 `total_qty` 而不是 `total_amount`）

### 数据源说明

- **价格数据**: 从PTrade平台获取
- **基本面数据**: 需要PTrade支持财务数据API，否则相关因子可能无法计算

### 测试建议

1. **模拟环境测试**: 先在PTrade模拟环境测试策略
2. **小资金测试**: 实盘前使用小资金测试
3. **API验证**: 确保所有API调用符合PTrade实际规范
4. **监控日志**: 关注策略运行日志，及时发现问题

## 📁 文件结构

```
strategies/ptrade/
├── TRQuant_V4_PTrade_*.py    # 策略代码文件
└── README.md                  # 本说明文档
```

## 🔧 故障排查

### 问题1: API调用失败
```
检查项:
1. PTrade API函数名是否正确
2. 参数格式是否符合PTrade规范
3. 股票代码格式是否为.SH/.SZ
```

### 问题2: 数据获取失败
```
检查项:
1. get_klines参数是否正确
2. 股票代码格式是否正确
3. 数据权限是否足够
```

### 问题3: 定时任务不执行
```
检查项:
1. schedule语法是否正确
2. 时间格式是否正确（'HH:MM'）
3. weekday参数是否正确
```

### 问题4: 基本面数据无法获取
```
说明: PTrade可能不支持某些基本面数据API
解决方案: 
1. 检查PTrade版本是否支持财务数据API
2. 考虑从其他数据源获取基本面数据
3. 调整策略，减少对基本面因子的依赖
```

## 📚 相关文档

- PTrade官方文档: http://180.169.107.9:7766/hub/help/api?weworkcfmcode
- PTrade策略编译环境: Python 3.11
- TRQuant策略文档: `docs/advisor_v4/`

## 📝 更新日志

- 2026-01-09: 初始版本，基于7个已验证因子

## 🔄 PTrade API适配说明

由于PTrade API与聚宽/BulletTrade有差异，策略代码中需要根据实际PTrade API调整以下部分：

### 1. 数据获取函数

```python
# 需要根据PTrade实际API调整
def get_price_ptrade(stocks, count=None, fields=None):
    # PTrade可能使用: get_klines(security, count, frequency='1d')
    # 或: get_market_data(stocks, fields, count)
    pass
```

### 2. 基本面数据获取

```python
# 需要根据PTrade实际API调整
def get_fundamentals_ptrade(stocks, date_str, fields=None):
    # PTrade可能使用: get_fundamentals(stocks, fields, date=date_str)
    # 或: get_financial_data(stocks, fields)
    pass
```

### 3. 订单函数

```python
# 需要根据PTrade实际API调整
def order_stock(stock_code, amount, price=0, order_type='market'):
    # PTrade可能使用: order(stock_code, amount, price=price)
    # 或: order_to(stock_code, target_amount)
    pass
```

### 4. 持仓查询

```python
# 需要根据PTrade实际API调整
def get_current_positions():
    # PTrade可能使用: get_positions()
    # 属性名可能不同: pos.total_qty, pos.cost_price等
    pass
```

### 5. 账户信息

```python
# 需要根据PTrade实际API调整
def get_account_info():
    # PTrade可能使用: get_account()
    # 属性名可能不同: account.total_asset, account.available_cash等
    pass
```

建议在实际使用前，先查阅PTrade官方API文档，确保所有API调用符合平台规范。
