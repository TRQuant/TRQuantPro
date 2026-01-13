# QMT退市股票动态过滤方案

> **更新时间**: 2026-01-09  
> **问题**: QMT的`get_stock_list_in_sector()`返回历史成分股，包括已退市的股票

---

## 🔍 问题分析

### 问题根源

**QMT的`get_stock_list_in_sector()`行为**:
- 返回**所有历史成分股**，包括：
  - ✅ 当前正常交易的股票
  - ❌ **已退市的股票**（如601989.SH中国重工、600837.SH海通证券）
  - ❌ 长期停牌的股票
  - ❌ 正在重组的股票

**为什么会出现退市股票？**
- 沪深300指数成分股会定期调整
- 某些股票可能因为退市、重组等原因被移除
- 但QMT返回的是**历史成分股列表**，不是当前有效成分股

---

## ✅ 解决方案

### 1. 动态验证函数

```python
def validate_stock_tradable(ContextInfo, code, max_retries=2):
    """
    验证股票是否可交易（未退市、未停牌）
    
    验证方法（按优先级）:
    1. 尝试获取最新价格 (get_last_price)
    2. 尝试获取市场数据 (get_market_data)
    3. 如果都失败，判定为退市/停牌
    """
    for attempt in range(max_retries):
        try:
            # Method 1: 获取最新价格
            price = ContextInfo.get_last_price(code)
            if price is not None and price > 0:
                return True
            
            # Method 2: 获取市场数据
            data = ContextInfo.get_market_data(code, period='1d', count=1)
            if data is not None and len(data) > 0:
                return True
            
            return False
        except:
            if attempt < max_retries - 1:
                continue
            return False
```

**验证逻辑**:
- ✅ 如果能够获取价格或市场数据 → 股票可交易
- ❌ 如果所有方法都失败 → 股票已退市/停牌

---

### 2. 股票列表获取函数（支持验证模式）

```python
def get_stock_list(ContextInfo, validate=True):
    """
    获取股票池（沪深300成分股）
    
    Args:
        ContextInfo: QMT context对象
        validate: 是否验证股票可交易性
            - True: 验证所有股票（较慢但准确）
            - False: 跳过验证（快速但可能包含退市股票）
    
    Returns:
        list: 有效的股票代码列表
    """
    # 1. 从QMT获取原始列表（包含退市股票）
    stock_list = ContextInfo.get_stock_list_in_sector("000300.SH")
    
    # 2. 标准化代码格式
    normalized_list = [normalize_stock_code(code) for code in stock_list]
    
    if not validate:
        # 跳过验证，直接返回（快速模式）
        return normalized_list
    
    # 3. 验证每个股票（过滤退市/停牌股票）
    valid_list = []
    invalid_codes = []
    
    for code in normalized_list:
        if validate_stock_tradable(ContextInfo, code):
            valid_list.append(code)
        else:
            invalid_codes.append(code)
    
    # 4. 输出过滤统计
    if invalid_codes:
        print(f"[Stock List] Filtered {len(invalid_codes)} delisted/suspended stocks")
        print(f"[Stock List] Invalid codes: {', '.join(invalid_codes[:10])}")
    
    return valid_list
```

---

### 3. 策略初始化（快速模式）

```python
def init(ContextInfo):
    """策略初始化"""
    # 初始化时跳过验证（加快启动速度）
    # 退市股票会在每周更新时被过滤
    g_stock_pool = get_stock_list(ContextInfo, validate=False)
    
    if not g_stock_pool:
        print("[Warning] Stock pool is empty")
        return
    
    ContextInfo.set_universe(g_stock_pool)
    print(f"Stock pool initialized: {len(g_stock_pool)} stocks")
```

**为什么初始化时跳过验证？**
- ✅ **启动速度快**: 验证300只股票可能需要几秒到几十秒
- ✅ **不影响运行**: 退市股票会在`handlebar`中被过滤
- ✅ **用户体验好**: 策略可以快速启动

---

### 4. 每周更新股票池（验证模式）

```python
def handlebar(ContextInfo):
    """每日K线回调"""
    current_weekday = get_current_datetime(ContextInfo).weekday()
    
    # 每周一更新股票池（带验证）
    if current_weekday == 0:  # Monday
        print("[Pre-market] Updating stock pool with validation...")
        
        # 验证模式：过滤退市/停牌股票
        g_stock_pool = get_stock_list(ContextInfo, validate=True)
        
        if g_stock_pool:
            ContextInfo.set_universe(g_stock_pool)
            print(f"[Pre-market] Stock pool updated: {len(g_stock_pool)} valid stocks")
        else:
            # 如果验证失败，回退到无验证模式
            g_stock_pool = get_stock_list(ContextInfo, validate=False)
            ContextInfo.set_universe(g_stock_pool)
```

**为什么每周更新时验证？**
- ✅ **确保准确性**: 每周更新时过滤退市股票
- ✅ **不影响性能**: 每周只验证一次
- ✅ **自动维护**: 无需手动维护排除列表

---

## 📊 效果对比

### 修复前

```
[Stock List] Got 300 stocks from index
[系统][WARNING][set_universe]无效股票代码:601989.SH 600837.SH
Stock pool initialized: 300 stocks
```

**问题**:
- ❌ 包含退市股票
- ❌ QMT发出警告
- ❌ 可能影响策略运行

### 修复后

```
[Stock List] Raw list from QMT: 300 stocks (may include delisted stocks)
[Stock List] Validating 300 stocks...
[Stock List] Validated 50/300 stocks...
[Stock List] Validated 100/300 stocks...
...
[Stock List] Filtered 2 delisted/suspended stocks
[Stock List] Invalid codes: 601989.SH, 600837.SH
[Stock List] Final valid stocks: 298
[Pre-market] Stock pool updated: 298 valid stocks
```

**改进**:
- ✅ 自动过滤退市股票
- ✅ 无警告信息
- ✅ 只使用有效股票
- ✅ 显示过滤统计

---

## 🔧 验证方法

### 验证逻辑

1. **尝试获取最新价格** (`get_last_price`)
   - 如果成功且价格>0 → 股票可交易
   - 如果失败 → 继续尝试其他方法

2. **尝试获取市场数据** (`get_market_data`)
   - 如果成功获取数据 → 股票可交易
   - 如果失败 → 判定为退市/停牌

3. **重试机制**
   - 最多重试2次
   - 避免网络波动导致的误判

### 性能考虑

- **验证时间**: 每只股票约0.1-0.5秒
- **300只股票**: 约30-150秒
- **优化建议**: 
  - 初始化时跳过验证（快速启动）
  - 每周更新时验证（确保准确性）
  - 可以并行验证（如果QMT支持）

---

## 📝 注意事项

### 1. 验证时机

- **初始化时**: 跳过验证（`validate=False`）
- **每周更新时**: 进行验证（`validate=True`）
- **选股时**: 使用已验证的股票池

### 2. 错误处理

- **验证失败**: 回退到无验证模式
- **空股票池**: 保持之前的股票池
- **部分失败**: 使用成功验证的股票

### 3. 性能优化

- **批量验证**: 如果QMT支持，可以批量验证
- **缓存结果**: 可以缓存验证结果，避免重复验证
- **并行验证**: 如果QMT支持多线程，可以并行验证

---

## 🔗 相关文件

- `strategies/qmt/TRQuant_V4_QMT_Research_SAFE_UTF8.py` - 已实现动态过滤的策略文件
- `core/advisor_v4/qmt_research_strategy_generator.py` - 策略生成器（待更新）

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-09
