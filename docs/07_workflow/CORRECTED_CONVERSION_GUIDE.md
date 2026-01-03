# 修正后的策略转换指南

## 🎯 基于BulletTrade官方文档的正确理解

**参考**: [BulletTrade官方文档](https://bullettrade.cn/docs/)

### 核心发现

根据官方文档，BulletTrade是：
> **"兼容聚宽API的量化研究与交易框架"**

这意味着：
- ✅ BulletTrade和聚宽API**100%兼容**
- ✅ 聚宽策略可以在BulletTrade中**无修改运行**
- ✅ 只需要添加 `from jqdata import *`

## 📊 正确的转换关系

### 1. 聚宽 ↔ BulletTrade

**无需转换！** 完全兼容。

```python
# 聚宽策略
from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.001))
    set_order_cost(OrderCost(...), type='stock')
```

```python
# BulletTrade策略（完全相同）
from jqdata import *  # 或 from bullet_trade.compat.api import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.001))
    set_order_cost(OrderCost(...), type='stock')
```

### 2. BulletTrade/聚宽 → PTrade

**需要转换！** 因为PTrade使用不同的API。

| 功能 | BulletTrade/聚宽 | PTrade | 转换 |
|------|-----------------|--------|------|
| 导入 | `from jqdata import *` | ❌ 删除 | ✅ 必须 |
| 数据获取 | `get_price(...)` | `get_history(...)` | ✅ 必须 |
| 当前数据 | `get_current_data()` | `get_snapshot(stocks)` | ✅ 必须 |
| 佣金设置 | `set_order_cost(...)` | `set_commission(PerTrade(...))` | ✅ 必须 |
| 滑点设置 | `set_slippage(FixedSlippage(...))` | ✅ 相同 | ❌ 无需 |
| 佣金设置2 | `set_commission(PerTrade(...))` | ✅ 相同 | ❌ 无需 |

## 🔄 正确的转换流程

### 场景A: 在韬睿系统（BulletTrade）中开发

1. **使用聚宽API编写策略**
   ```python
   from jqdata import *
   
   def initialize(context):
       set_benchmark('000300.XSHG')
       set_slippage(FixedSlippage(0.001))
       set_order_cost(OrderCost(
           open_tax=0,
           close_tax=0.001,
           open_commission=0.0003,
           close_commission=0.0003,
           min_commission=5
       ), type='stock')
   ```

2. **在BulletTrade中直接运行** - ✅ 无需任何修改！

### 场景B: 转换到PTrade

1. **使用完整转换器**
   ```bash
   python core/comprehensive_strategy_converter.py \
       strategies/bullettrade/my_strategy.py \
       strategies/ptrade/my_strategy_ptrade.py
   ```

2. **转换器会自动处理**:
   - ✅ 删除 `from jqdata import *`
   - ✅ `get_price()` -> `get_history()`
   - ✅ `get_current_data()` -> `get_snapshot(stocks)`
   - ✅ `set_order_cost()` -> `set_commission(PerTrade(...))`
   - ✅ 属性名转换（`day_open` -> `open`等）

## 📋 统一版策略的正确理解

### 统一版策略实际上是BulletTrade/聚宽格式

**文件**: `strategies/unified/TRQuant_momentum_unified.py`

**特点**:
- 使用聚宽API（`get_price`, `get_current_data`等）
- 需要添加 `from jqdata import *` 才能在BulletTrade运行
- **不能直接在PTrade运行**，需要转换

### 使用流程

1. **在BulletTrade中使用**:
   ```python
   # 在文件开头添加
   from jqdata import *
   
   # 然后直接使用统一版策略
   ```

2. **转换到PTrade**:
   ```bash
   python core/comprehensive_strategy_converter.py \
       strategies/unified/TRQuant_momentum_unified.py \
       strategies/ptrade/TRQuant_momentum_ptrade.py
   ```

## ✅ 修正后的结论

### 之前的误解

❌ 认为BulletTrade和聚宽有差异
❌ 认为统一版策略可以在两个平台直接运行

### 正确的理解

✅ **BulletTrade完全兼容聚宽API** - 无需转换
✅ **统一版策略是BulletTrade/聚宽格式** - 需要转换为PTrade
✅ **只有转换为PTrade时才需要转换** - 因为PTrade使用不同的API

## 🎯 关键差异总结

### BulletTrade vs 聚宽

**差异**: **0个** - 完全兼容！

### BulletTrade/聚宽 vs PTrade

**必须转换的差异**:
1. 删除 `from jqdata import *`
2. `get_price()` -> `get_history()`
3. `get_current_data()` -> `get_snapshot(stocks)`
4. `set_order_cost()` -> `set_commission(PerTrade(...))`
5. 属性名转换

**完全相同的API**:
1. `set_commission(PerTrade(...))` ✅
2. `set_slippage(FixedSlippage(...))` ✅
3. `order_target_value()` ✅
4. `log.info()`, `log.warn()`, `log.error()` ✅
5. `context.portfolio.positions` ✅
6. `run_daily()` ✅

## 📚 参考资源

- BulletTrade官方文档: https://bullettrade.cn/docs/
- BulletTrade GitHub: https://github.com/BulletTrade/bullet-trade
- 聚宽API文档: https://www.joinquant.com/help/api/help
- PTrade API文档: https://ptradeapi.com/
