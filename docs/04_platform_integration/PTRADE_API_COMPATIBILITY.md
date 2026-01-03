# PTrade API兼容性指南

## 📊 问题根源

```
ModuleNotFoundError: No module named 'jqdata'
```

**原因**: PTrade和聚宽(JQData)是不同的平台，API有本质差异：
- 聚宽是数据提供商，需要`from jqdata import *`
- PTrade是交易终端，API是内置的，不需要导入

## 🔄 API差异对照表

### 1. 模块导入

| 聚宽/BulletTrade | PTrade |
|-----------------|--------|
| `from jqdata import *` | ❌ **删除** - PTrade API内置 |
| `from kuanke.user_space_api import *` | ❌ **删除** |

### 2. 滑点设置

| 聚宽/BulletTrade | PTrade |
|-----------------|--------|
| `set_slippage(FixedSlippage(0.001))` | `set_slippage(0.001)` |
| `set_slippage(PriceRelatedSlippage(0.002))` | `set_slippage(0.002)` |

### 3. 佣金设置

| 聚宽/BulletTrade | PTrade |
|-----------------|--------|
| `set_order_cost(OrderCost(open_tax=0, close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')` | `set_commission(commission=0.0003, min_commission=5)` |
| `set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))` | `set_commission(commission=0.0003, min_commission=5)` |

### 4. 数据获取

| 聚宽/BulletTrade | PTrade |
|-----------------|--------|
| `get_price(stocks, end_date=date, frequency='daily', fields=['close'], count=20, panel=False)` | `get_history(20, '1d', stocks, ['close'], skip_paused=False, fq='pre')` |
| `get_current_data()` | `get_snapshot(stocks)` |
| `data.day_open` | `snap.open` |
| `data.high_limit` | `snap.up_limit` |
| `data.low_limit` | `snap.down_limit` |
| `data.last_price` | `snap.last_px` |

### 5. ST股票检查

| 聚宽/BulletTrade | PTrade |
|-----------------|--------|
| `get_extras('is_st', stocks, ...)` | 通过股票名称判断: `'ST' in name` |

### 6. 股票信息

| 聚宽/BulletTrade | PTrade |
|-----------------|--------|
| `get_security_info(stock)` | `get_instrument(stock)` |

### 7. 定时任务

| 聚宽/BulletTrade | PTrade |
|-----------------|--------|
| `run_daily(func, time='09:00')` | `run_daily(func, '09:00')` |
| `run_weekly(func, weekday=1, time='09:00')` | `run_weekly(func, 1, '09:00')` |

## 📁 策略文件

### PTrade原生策略
```
strategies/ptrade/TRQuant_momentum_v3_ptrade_native.py
```

### 策略转换器
```python
from core.strategy_converter import convert_strategy_to_ptrade

# 转换策略文件
result = convert_strategy_to_ptrade(
    'strategies/bullettrade/TRQuant_momentum_v3_bt.py',
    'strategies/ptrade/TRQuant_momentum_v3_ptrade.py'
)

print(f"转换结果: {'成功' if result['success'] else '失败'}")
print(f"警告: {result['warnings']}")
print(f"错误: {result['errors']}")
```

## 🛠️ 转换命令

```bash
cd /home/taotao/dev/QuantTest/TRQuant

# 使用转换器
python core/strategy_converter.py strategies/bullettrade/TRQuant_momentum_v3_bt.py
```

## ✅ PTrade策略模板

```python
# -*- coding: utf-8 -*-
"""PTrade策略模板"""

# ========== 不要导入jqdata ==========
# ❌ from jqdata import *  

# ========== 策略参数 ==========
MAX_STOCKS = 5
BENCHMARK = '000300.XSHG'

# ========== 初始化 ==========
def initialize(context):
    set_benchmark(BENCHMARK)
    set_slippage(0.001)  # 直接数值
    set_commission(commission=0.0003, min_commission=5)
    
    g.trade_count = 0
    g.stock_pool = []
    
    run_daily(before_market_open, '09:00')
    run_daily(market_open, '09:35')

def before_market_open(context):
    g.stock_pool = get_index_stocks(BENCHMARK)

def market_open(context):
    # 获取历史数据（PTrade格式）
    prices = get_history(20, '1d', g.stock_pool[:30], ['close'])
    close_df = prices['close']
    
    # 选股逻辑
    momentum = close_df.pct_change(5).iloc[-1]
    selected = momentum.nlargest(MAX_STOCKS).index.tolist()
    
    # 调仓
    for stock in selected:
        order_target_value(stock, context.portfolio.total_value * 0.15)
```

## 🔍 常见错误及解决

### 错误1: ModuleNotFoundError: No module named 'jqdata'
```python
# ❌ 错误
from jqdata import *

# ✅ 正确
# 删除这行，PTrade API是内置的
```

### 错误2: InvalidArgument: set_slippage invalid argument
```python
# ❌ 错误
set_slippage(FixedSlippage(0.001))

# ✅ 正确
set_slippage(0.001)
```

### 错误3: get_price not defined
```python
# ❌ 错误（聚宽格式）
prices = get_price(stocks, end_date=date, frequency='daily', 
                   fields=['close'], count=20, panel=False)

# ✅ 正确（PTrade格式）
prices = get_history(20, '1d', stocks, ['close'])
close_df = prices['close']  # 返回dict格式
```

### 错误4: get_current_data属性错误
```python
# ❌ 错误
data.day_open
data.high_limit

# ✅ 正确（PTrade使用get_snapshot）
snap = get_snapshot([stock])
snap[stock].open
snap[stock].up_limit
```

## 📋 检查清单

在PTrade运行策略前，确保：

- [ ] 删除所有`from jqdata import *`
- [ ] `set_slippage()`使用数值参数
- [ ] `set_commission()`使用PTrade格式
- [ ] `get_price()`改为`get_history()`
- [ ] `get_current_data()`改为`get_snapshot()`
- [ ] 属性名称调整（day_open→open, high_limit→up_limit）
- [ ] `get_extras('is_st')`改为名称判断

## 🚀 TRQuant策略生成改进

为避免此问题，TRQuant系统应：

1. **生成时指定目标平台**
   ```python
   generate_strategy(factors, platform='ptrade')  # 或 'jqdata', 'bullettrade'
   ```

2. **内置平台适配器**
   - 根据目标平台自动选择正确的API

3. **转换验证**
   - 生成后自动进行语法检查
   - 检查是否有不兼容的API调用

## 📂 文件位置

| 文件 | 用途 |
|------|------|
| `strategies/ptrade/TRQuant_momentum_v3_ptrade_native.py` | PTrade原生策略 |
| `core/strategy_converter.py` | 策略转换器 |
| `docs/PTRADE_API_COMPATIBILITY.md` | 本文档 |
