# QMT股票代码验证和过滤修复

> **修复时间**: 2026-01-09  
> **问题**: QMT回测时出现"无效股票代码"警告，即使代码格式正确

---

## 🔍 问题分析

### 错误现象

```
[系统][WARNING][set_universe]无效股票代码:601989.SH 600837.SH
```

### 根本原因

即使股票代码格式正确（`.SH`/`.SZ`），某些代码在QMT中可能：
1. **已退市**: 股票已从市场退市
2. **停牌**: 股票当前停牌，无法交易
3. **不存在**: 代码在QMT数据库中不存在
4. **数据缺失**: QMT无法获取该股票的数据

**解决方案**: 在设置`set_universe`之前，验证每个股票代码是否有效。

---

## ✅ 修复方案

### 1. 添加股票代码验证函数

```python
def validate_stock_code(ContextInfo, code):
    """
    Validate if a stock code is valid in QMT
    
    Args:
        ContextInfo: QMT context object
        code: Stock code to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Try to get the last price, if successful, the code is valid
        price = ContextInfo.get_last_price(code)
        return price is not None and price > 0
    except:
        return False
```

**验证方法**: 使用`get_last_price()`尝试获取股票最新价格，如果成功且价格>0，则认为代码有效。

---

### 2. 在获取股票列表时过滤无效代码

```python
def get_stock_list(ContextInfo):
    """Get stock pool (CSI 300 component stocks)"""
    try:
        index_code = "000300.SH"
        stock_list = ContextInfo.get_stock_list_in_sector(index_code)
        if not stock_list:
            return []
        
        # Normalize stock codes for QMT
        normalized_list = [normalize_stock_code(code) for code in stock_list]
        
        # Validate and filter invalid codes
        valid_list = []
        invalid_codes = []
        for code in normalized_list:
            if validate_stock_code(ContextInfo, code):
                valid_list.append(code)
            else:
                invalid_codes.append(code)
        
        if invalid_codes:
            print(f"[Stock List] Filtered {len(invalid_codes)} invalid codes: {', '.join(invalid_codes[:10])}{'...' if len(invalid_codes) > 10 else ''}")
        
        return valid_list
    except Exception as e:
        print(f"Failed to get stock list: {e}")
        return []
```

**改进点**:
- ✅ 自动验证每个代码
- ✅ 过滤无效代码
- ✅ 显示被过滤的代码列表（最多显示10个）
- ✅ 返回已验证的有效代码列表

---

### 3. 在初始化时添加错误处理

```python
def init(ContextInfo):
    # Set stock pool (CSI 300)
    g_stock_pool = get_stock_list(ContextInfo)
    if not g_stock_pool:
        print("[Warning] Stock pool is empty, cannot initialize strategy")
        return
    
    # Set universe with validated stock codes
    try:
        ContextInfo.set_universe(g_stock_pool)
        print(f"Stock pool initialized: {len(g_stock_pool)} stocks")
    except Exception as e:
        print(f"[Warning] Failed to set universe: {e}")
        # Try to set with a smaller subset if full list fails
        if len(g_stock_pool) > 50:
            print(f"[Fallback] Trying with first 50 stocks...")
            try:
                ContextInfo.set_universe(g_stock_pool[:50])
                print(f"Stock pool initialized (subset): 50 stocks")
            except Exception as e2:
                print(f"[Error] Failed to set universe even with subset: {e2}")
```

**改进点**:
- ✅ 检查股票池是否为空
- ✅ 捕获`set_universe`异常
- ✅ 回退机制：如果全部失败，尝试使用前50只股票
- ✅ 详细的错误日志

---

### 4. 在handlebar中更新股票池时也添加验证

```python
def handlebar(ContextInfo):
    # Update stock pool weekly (Monday)
    if current_weekday == 0:  # Monday
        g_stock_pool = get_stock_list(ContextInfo)
        if g_stock_pool:
            try:
                ContextInfo.set_universe(g_stock_pool)
                print(f"[Pre-market] Stock pool updated: {len(g_stock_pool)} stocks")
            except Exception as e:
                print(f"[Warning] Failed to update stock pool: {e}")
        else:
            print("[Warning] Stock pool is empty, keeping previous pool")
```

**改进点**:
- ✅ 使用已验证的股票列表
- ✅ 错误处理
- ✅ 如果更新失败，保持之前的股票池

---

## 📊 效果对比

### 修复前

```
[系统][WARNING][set_universe]无效股票代码:601989.SH 600837.SH
Stock pool initialized: 300 stocks
```

**问题**: 
- ❌ 包含无效代码
- ❌ QMT发出警告
- ❌ 可能影响策略运行

### 修复后

```
[Stock List] Filtered 2 invalid codes: 601989.SH, 600837.SH
Stock pool initialized: 298 stocks
```

**改进**:
- ✅ 自动过滤无效代码
- ✅ 无警告信息
- ✅ 只使用有效股票
- ✅ 显示过滤统计

---

## 🔧 验证方法

### 测试步骤

1. **运行策略**: 在QMT研究环境中运行修复后的策略
2. **检查日志**: 确认不再出现"无效股票代码"警告
3. **验证过滤**: 查看日志中是否显示被过滤的代码
4. **确认数量**: 确认股票池数量正确（300 - 无效数量）

### 预期输出

```
============================================================
TRQuant Advisor V4.0 - QMT Research Environment Strategy Started
============================================================
[Stock List] Filtered 2 invalid codes: 601989.SH, 600837.SH
Stock pool initialized: 298 stocks
Scheduled tasks set
   Rebalance: Every Monday (checked in handlebar)
   Risk Control: Daily 14:50
============================================================
```

---

## 📝 注意事项

### 1. 性能考虑

- **验证时间**: 每个代码验证需要调用`get_last_price()`，300只股票可能需要几秒钟
- **优化建议**: 可以考虑批量验证或缓存验证结果

### 2. 验证时机

- **初始化时**: `init()`函数中验证
- **每周更新**: `handlebar()`中周一更新时验证
- **选股时**: `select_stocks()`中也会使用已验证的股票池

### 3. 错误处理

- **空股票池**: 如果所有股票都无效，策略无法运行
- **部分无效**: 自动过滤，使用有效股票继续运行
- **验证失败**: 如果验证过程出错，返回空列表，保持之前的股票池

---

## 🔗 相关文件

- `strategies/qmt/TRQuant_V4_QMT_Research_SAFE_UTF8.py` - 已修复的策略文件
- `core/advisor_v4/qmt_research_strategy_generator.py` - 策略生成器（已更新）

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-09
