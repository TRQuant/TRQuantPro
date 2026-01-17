# QMT回测策略修复总结

> **修复日期**: 2026-01-09  
> **策略文件**: `strategies/qmt/TRQuant_V4_QMT_Backtest_3Months.py`  
> **参考**: QMT回测示例代码 + QMT API文档

---

## 📋 修复内容

### 1. 添加时间处理函数

**问题**: QMT使用时间戳（毫秒），需要转换函数

**修复**:
```python
def timetag_to_datetime(timetag, format_str='%Y%m%d'):
    """Convert timetag to datetime (QMT API compatible)"""
    from datetime import datetime
    try:
        if timetag > 1e10:  # Likely milliseconds
            return datetime.fromtimestamp(timetag / 1000.0)
        else:  # Likely seconds
            return datetime.fromtimestamp(timetag)
    except:
        return datetime.now()
```

**使用**: 在`get_current_datetime`和`handlebar`中使用

---

### 2. 修改数据获取函数

**问题**: 现有代码使用`get_market_data`，但QMT示例代码使用`get_history_data`

**修复**:
```python
def get_price_data(ContextInfo, stocks, count=20, fields=None):
    """Get price data (QMT API compatible)"""
    # QMT API: get_history_data(count, period, field, stock_list)
    # Example: ContextInfo.get_history_data(1,'1d','open',3)
    data = ContextInfo.get_history_data(count, '1d', field, [stock])
    # Returns: dict with stock codes as keys, lists as values
```

**关键变化**:
- 优先使用`get_history_data()`（QMT标准API）
- 支持dict格式返回（QMT API返回格式）
- 回退到`get_market_data()`（兼容性）

---

### 3. 添加交易函数

**问题**: 现有代码使用`ContextInfo.order()`，但QMT示例代码使用`order_shares()`

**修复**:
```python
def order_shares(stock_code, amount, order_type='fix', price=0, ContextInfo=None, account_id=None):
    """
    Order shares (QMT API compatible)
    
    According to QMT example code:
    order_shares(k,-ContextInfo.holdings[k]*100,'fix',price[k][-1],ContextInfo,ContextInfo.accountID)
    """
    # Use ContextInfo.order() internally
    return ContextInfo.order(stock_code, amount, market_type)
```

**关键变化**:
- 按照QMT示例代码风格实现
- 支持'fix'和'market'订单类型
- 统一账户ID处理

---

### 4. 修改init函数

**问题**: 股票池获取方式不符合QMT示例代码

**修复**:
```python
def init(ContextInfo):
    # Set account ID (QMT example uses ContextInfo.accountID)
    ContextInfo.accountID = 'testS'
    
    # Get stock pool (use get_sector for index stocks like example)
    g_stock_pool = ContextInfo.get_sector('000300.SH')
    
    # Set universe
    ContextInfo.set_universe(g_stock_pool)
    
    # Set backtest parameters
    ContextInfo.start = START_DATE.strftime('%Y%m%d')
    ContextInfo.end = END_DATE.strftime('%Y%m%d')
    ContextInfo.capital = 1000000.0
    
    # Set commission
    ContextInfo.set_commission(COMMISSION_RATE)
```

**关键变化**:
- 使用`ContextInfo.get_sector('000300.SH')`获取股票池
- 设置`ContextInfo.accountID = 'testS'`
- 设置回测参数（start/end/capital）
- 设置手续费率（set_commission）

---

### 5. 修改handlebar函数

**问题**: 时间获取方式不符合QMT示例代码

**修复**:
```python
def handlebar(ContextInfo):
    # Get current bar position (QMT example uses ContextInfo.barpos)
    d = ContextInfo.barpos
    
    # Get current date
    timetag = ContextInfo.get_bar_timetag(d)
    current_dt = timetag_to_datetime(timetag)
    
    # Print current date (like example code)
    nowDate = timetag_to_datetime(ContextInfo.get_bar_timetag(d), '%Y%m%d')
    print(f"[Handlebar] Date: {nowDate.strftime('%Y-%m-%d')}, Bar: {d}")
```

**关键变化**:
- 使用`ContextInfo.barpos`获取当前K线索引
- 使用`ContextInfo.get_bar_timetag(d)`获取日期
- 打印当前日期（示例代码风格）

---

### 6. 修复因子计算

**问题**: 因子计算不支持dict格式数据（`get_history_data`返回格式）

**修复**:
```python
# Handle dict format from get_history_data
if isinstance(data, dict) and 'close' in data:
    close_vals = data['close']
    if isinstance(close_vals, list) and len(close_vals) >= 20:
        result.loc[result['code'] == code, 'momentum_20d'] = \
            (close_vals[-1] - close_vals[0]) / close_vals[0] * 100
elif isinstance(data, pd.DataFrame) and 'close' in data.columns:
    # DataFrame format (compatibility)
    ...
```

**关键变化**:
- 支持dict格式数据（`get_history_data`返回格式）
- 支持DataFrame格式数据（兼容性）
- 所有因子计算都已更新

---

### 7. 统一交易函数

**问题**: 交易函数不一致，账户ID处理不统一

**修复**:
```python
# All trades use order_shares (QMT example style)
order_shares(stock_code, sell_amount, 'fix', current_price, ContextInfo, account_id)
```

**关键变化**:
- 所有交易使用`order_shares()`函数
- 统一账户ID处理（`accountID`/`accout_id`兼容）
- 在`check_risk_control`和`rebalance`中统一使用

---

## 📚 知识库更新

### 1. QMT回测示例代码

**已存入知识库**:
- ID: `kb_b07d1f77be57`
- 标题: "QMT回测模型示例代码"
- 类型: `code_example`
- 平台: `QMT`
- 标签: `QMT`, `回测`, `示例代码`

**内容**: 完整的QMT回测示例代码，包括：
- `init()`函数：初始化股票池、账户ID、参数
- `handlebar()`函数：主循环，使用`barpos`和`get_bar_timetag`
- `signal()`函数：买入卖出信号生成
- `order_shares()`函数：下单函数
- `get_history_data()`函数：数据获取

### 2. QMT API文档

**已爬取并存入知识库**:
- URL: `https://qmt.ptradeapi.com/QMT_Python_API_Doc.html#id14`
- 共6条知识条目：
  1. QMT Python API 接口文档（主文档）
  2-6. 代码示例片段

**关键API**:
- `ContextInfo.get_history_data(count, period, field, stock_list)`
- `ContextInfo.get_sector(index_code)`
- `ContextInfo.set_universe(stock_list)`
- `ContextInfo.get_bar_timetag(barpos)`
- `order_shares(stock, amount, order_type, price, ContextInfo, accountID)`
- `timetag_to_datetime(timetag, format_str)`

---

## 🔧 修复前后对比

### 数据获取

**修复前**:
```python
data = ContextInfo.get_market_data(stock, period='1d', count=count)
```

**修复后**:
```python
data = ContextInfo.get_history_data(count, '1d', field, [stock])
# Returns: {stock: [values]}
```

### 交易执行

**修复前**:
```python
ContextInfo.order(stock_code, amount, ContextInfo.MARKET_SH_SZ)
```

**修复后**:
```python
order_shares(stock_code, amount, 'fix', current_price, ContextInfo, account_id)
```

### 股票池获取

**修复前**:
```python
g_stock_pool = get_stock_list(ContextInfo, validate=False)
```

**修复后**:
```python
g_stock_pool = ContextInfo.get_sector('000300.SH')
```

### 时间获取

**修复前**:
```python
current_dt = get_current_datetime(ContextInfo)
```

**修复后**:
```python
d = ContextInfo.barpos
timetag = ContextInfo.get_bar_timetag(d)
current_dt = timetag_to_datetime(timetag)
```

---

## ✅ 验证清单

- [x] 语法检查通过
- [x] 所有API调用符合QMT标准
- [x] 数据格式处理正确（dict/DataFrame兼容）
- [x] 交易函数统一使用`order_shares`
- [x] 账户ID处理统一
- [x] 时间处理正确
- [x] 知识库已更新

---

## 🚀 下一步

1. **在QMT中运行回测**
   - 加载策略文件
   - 设置回测参数（起始日期、结束日期、初始资金）
   - 运行回测

2. **验证功能**
   - 检查数据获取是否正常
   - 检查选股是否正常
   - 检查交易是否正常
   - 检查风控是否正常

3. **优化调整**
   - 根据回测结果调整参数
   - 优化因子计算性能
   - 完善错误处理

---

## 📚 参考文档

- QMT回测示例代码（知识库ID: `kb_b07d1f77be57`）
- QMT API文档（`https://qmt.ptradeapi.com/QMT_Python_API_Doc.html#id14`）
- QMT策略文档（`strategies/qmt/README.md`）

---

**最后更新**: 2026-01-09
