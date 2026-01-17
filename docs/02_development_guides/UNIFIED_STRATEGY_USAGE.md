# 统一版策略使用指南

## 📋 问题回答

**Q: 统一版策略在韬睿量化系统（BulletTrade）可以运行，转到PTrade也可以直接运行吗？**

**A: 不能直接运行，需要转换。** 原因如下：

### 主要差异

| 功能 | BulletTrade | PTrade | 统一版策略 |
|------|------------|--------|-----------|
| **导入** | `from jqdata import *` | 不需要导入 | ❌ 缺少导入（BulletTrade需要） |
| **数据获取** | `get_price(...)` | `get_history(...)` | ⚠️ 使用try-except，但PTrade会失败 |
| **当前数据** | `get_current_data()` | `get_snapshot(stocks)` | ❌ 使用get_current_data() |
| **股票信息** | `get_security_info()` | `get_instrument()` | ⚠️ 使用get_security_info() |

## 🔄 转换方案

### 方案1: 使用自动转换工具（推荐）

```bash
# 转换统一版策略为PTrade格式
python scripts/convert_unified_to_ptrade.py \
    strategies/unified/TRQuant_momentum_unified.py \
    strategies/ptrade/TRQuant_momentum_ptrade.py
```

**转换工具会自动处理**:
- ✅ 删除`from jqdata import *`
- ✅ 转换`get_current_data()` -> `get_snapshot(stocks)`
- ✅ 转换`get_price()` -> `get_history()`
- ✅ 转换`get_security_info()` -> `get_instrument()`
- ✅ 修复数据获取逻辑

### 方案2: 使用策略转换器

```python
from core.strategy_converter import convert_strategy_to_ptrade

result = convert_strategy_to_ptrade(
    'strategies/unified/TRQuant_momentum_unified.py',
    'strategies/ptrade/TRQuant_momentum_ptrade.py'
)
```

### 方案3: 手动转换

需要修改以下内容：

#### 1. 删除导入（PTrade不需要）
```python
# ❌ 删除这行（如果存在）
from jqdata import *
```

#### 2. 转换数据获取
```python
# ❌ BulletTrade格式
try:
    prices = get_history(...)
except:
    prices = get_price(...)

# ✅ PTrade格式（直接使用get_history）
prices = get_history(MOMENTUM_LONG + 5, '1d', test_stocks, ['close'], 
                    skip_paused=False, fq='pre')
close_df = prices.get('close') if isinstance(prices, dict) else prices
```

#### 3. 转换当前数据获取
```python
# ❌ BulletTrade格式
current_data = get_current_data()

# ✅ PTrade格式
current_data = get_snapshot(stocks[:100])  # 需要传入股票列表
```

#### 4. 转换股票信息
```python
# ❌ BulletTrade格式
info = get_security_info(stock)

# ✅ PTrade格式
info = get_instrument(stock)
```

## 📊 详细对比

### 数据获取API差异

**BulletTrade (聚宽兼容)**:
```python
prices = get_price(
    stocks, 
    end_date=context.current_dt.strftime('%Y-%m-%d'),
    frequency='daily',
    fields=['close'],
    count=20,
    panel=False
)
# 返回: DataFrame (长格式或宽格式)
close_df = prices.pivot(index='time', columns='code', values='close')
```

**PTrade**:
```python
prices = get_history(
    20,           # count
    '1d',         # unit
    stocks,       # security_list
    ['close'],    # fields
    skip_paused=False,
    fq='pre'
)
# 返回: dict {'close': DataFrame}
close_df = prices['close']
```

### 当前数据获取差异

**BulletTrade**:
```python
current_data = get_current_data()  # 返回全局dict
data = current_data[stock]          # 获取单个股票数据
price = data.last_price            # 属性访问
```

**PTrade**:
```python
current_data = get_snapshot([stock1, stock2, ...])  # 需要传入股票列表
data = current_data[stock]                          # 获取单个股票数据
price = data.last_px                                # 属性名不同
```

## 🚀 推荐工作流程

### 在韬睿系统（BulletTrade）中开发

1. **使用统一版策略作为起点**
   ```bash
   cp strategies/unified/TRQuant_momentum_unified.py my_strategy.py
   ```

2. **在文件开头添加导入**
   ```python
   from jqdata import *
   ```

3. **在BulletTrade中测试和优化**

### 转换到PTrade

1. **使用转换工具**
   ```bash
   python scripts/convert_unified_to_ptrade.py my_strategy.py my_strategy_ptrade.py
   ```

2. **检查转换结果**
   - 确认没有`from jqdata import *`
   - 确认使用`get_history`而不是`get_price`
   - 确认使用`get_snapshot`而不是`get_current_data()`

3. **在PTrade中测试**

## ⚠️ 注意事项

### 1. get_snapshot需要股票列表

PTrade的`get_snapshot`必须传入股票列表，不能像`get_current_data()`那样获取所有股票。

**解决方案**:
```python
# 在filter_stocks中
current_data = get_snapshot(stocks[:100]) if len(stocks) > 0 else {}

# 在rebalance中
all_stocks = list(context.portfolio.positions.keys()) + target_stocks
current_data = get_snapshot(all_stocks[:100]) if len(all_stocks) > 0 else {}

# 在check_risk中
current_data = get_snapshot(list(context.portfolio.positions.keys())[:100]) \
               if len(context.portfolio.positions) > 0 else {}
```

### 2. 属性名称差异

| BulletTrade | PTrade |
|------------|--------|
| `data.last_price` | `data.last_px` |
| `data.day_open` | `data.open` |
| `data.high_limit` | `data.up_limit` |
| `data.low_limit` | `data.down_limit` |

**统一版策略已处理**: 使用`getattr(data, 'last_price', None) or getattr(data, 'last_px', None)`

### 3. 数据格式差异

- BulletTrade的`get_price`返回DataFrame（可能需要pivot）
- PTrade的`get_history`返回dict `{'close': DataFrame}`

## 📁 文件位置

| 文件 | 用途 |
|------|------|
| `strategies/unified/TRQuant_momentum_unified.py` | 统一版策略（BulletTrade格式） |
| `scripts/convert_unified_to_ptrade.py` | 自动转换工具 |
| `core/strategy_converter.py` | 通用策略转换器 |
| `strategies/ptrade/TRQuant_momentum_v3_ptrade_native.py` | PTrade原生策略（参考） |

## ✅ 总结

1. **统一版策略不能直接在PTrade运行** - 需要转换
2. **推荐使用自动转换工具** - `scripts/convert_unified_to_ptrade.py`
3. **主要转换点**:
   - 删除`from jqdata import *`
   - `get_current_data()` -> `get_snapshot(stocks)`
   - `get_price()` -> `get_history()`
   - `get_security_info()` -> `get_instrument()`

4. **最佳实践**:
   - 在BulletTrade中开发和测试
   - 使用转换工具转换为PTrade格式
   - 在PTrade中验证和优化
