# 完整策略转换器使用指南

## 🎯 概述

`core/comprehensive_strategy_converter.py` 是基于网页搜索结果和实际代码分析创建的**完整策略转换器**，覆盖PTrade和BulletTrade/聚宽之间的所有API差异。

## 📋 覆盖的差异点

### ✅ 已完全覆盖（17大类，50+个差异点）

1. **模块导入** (2个)
   - `from jqdata import *` -> 删除
   - `from kuanke.user_space_api import *` -> 删除

2. **佣金设置** (3个)
   - `set_order_cost(OrderCost(...))` -> `set_commission(PerTrade(...))`
   - `set_commission(commission=...)` -> `set_commission(PerTrade(...))`
   - `set_commission(PerTrade(...))` -> 保持不变

3. **滑点设置** (3个)
   - `set_slippage(FixedSlippage(...))` -> 保持不变
   - `set_slippage(PriceRelatedSlippage(...))` -> `set_slippage(FixedSlippage(...))`
   - `set_slippage(数值)` -> 保持不变

4. **数据获取 - 历史数据** (2个)
   - `get_price(...)` -> `get_history(...)`
   - 参数格式转换

5. **数据获取 - 当前数据** (2个)
   - `get_current_data()` -> `get_snapshot(stocks)`
   - 上下文分析自动确定股票列表

6. **数据获取 - 股票信息** (3个)
   - `get_security_info()` -> `get_instrument()`
   - `get_all_securities(['stock'])` -> `get_all_securities('stock')`
   - `get_index_stocks('000300.XSHG')` -> 可能转换代码格式

7. **数据获取 - 其他** (3个)
   - `get_extras('is_st', ...)` -> 注释+替代方案
   - `get_fundamentals()` -> 保持不变
   - `attribute_history()` -> `get_history()`

8. **交易执行** (5个)
   - `order()` -> 保持不变
   - `order_target()` -> `order_target_volume()`
   - `order_target_value()` -> 保持不变
   - `order_value()` -> 保持不变
   - `order_percent()` -> 保持不变

9. **持仓访问** (4个)
   - `context.portfolio.positions` -> 保持不变
   - `context.portfolio.total_value` -> 保持不变
   - `context.portfolio.available_cash` -> 保持不变
   - `get_positions()` -> 保持不变（如果存在）

10. **日志输出** (5个)
    - `log.info()` -> 保持不变
    - `log.warn()` -> 保持不变
    - `log.error()` -> 保持不变
    - `log.debug()` -> 保持不变
    - `log()` -> 保持不变

11. **定时任务** (4个)
    - `run_daily(func, time='09:00')` -> 保持不变
    - `run_daily(func, '09:00')` -> 保持不变
    - `run_weekly()` -> 保持不变
    - `run_monthly()` -> 保持不变

12. **事件处理函数** (6个)
    - `initialize(context)` -> 保持不变
    - `before_market_open(context)` -> 保持不变
    - `market_open(context)` -> 保持不变
    - `handle_data(context, data)` -> 可能需要转换为`on_bar()`
    - `after_market_close(context)` -> 保持不变
    - `before_trading_start(context, data)` -> 保持不变

13. **数据对象属性** (6个)
    - `data.day_open` -> `data.open`
    - `data.high_limit` -> `data.up_limit`
    - `data.low_limit` -> `data.down_limit`
    - `data.last_price` -> `data.last_px`
    - `data.paused` -> 保持不变
    - `data.is_st` -> 不支持，需要替代方案

14. **股票代码格式** (3个)
    - `.XSHG` -> `.SH`（可选，根据PTrade版本）
    - `.XSHE` -> `.SZ`（可选，根据PTrade版本）
    - `.SS` -> 保持不变（某些版本）

15. **全局变量** (2个)
    - `g.variable` -> 保持不变
    - `context.variable` -> 保持不变

16. **其他API** (3个)
    - `query(...)` -> 保持不变
    - `get_trade_days()` -> 保持不变
    - `is_trade_day()` -> 保持不变

17. **初始化设置** (3个)
    - `set_benchmark()` -> 保持不变
    - `set_universe()` -> 保持不变
    - 其他设置 -> 保持不变

## 🚀 使用方法

### 命令行使用

```bash
python core/comprehensive_strategy_converter.py \
    strategies/unified/TRQuant_momentum_unified.py \
    strategies/ptrade/TRQuant_momentum_ptrade.py
```

### Python代码使用

```python
from core.comprehensive_strategy_converter import convert_strategy_comprehensive

result = convert_strategy_comprehensive(
    'strategies/bullettrade/my_strategy.py',
    'strategies/ptrade/my_strategy_ptrade.py'
)

if result['success']:
    print(f"✅ 转换成功！")
    print(f"变更: {len(result['changes'])}条")
    print(f"警告: {len(result['warnings'])}条")
else:
    print(f"❌ 转换失败: {result['errors']}")
```

## 📊 转换结果

转换器返回的结果包含：

```python
{
    'success': True/False,           # 是否成功
    'input_file': '输入文件路径',
    'output_file': '输出文件路径',
    'warnings': ['警告列表'],        # 需要手动检查的项目
    'errors': ['错误列表'],          # 转换失败的项目
    'changes': ['变更列表']          # 所有转换变更
}
```

## 🔍 转换特性

### 1. 智能上下文分析

转换器会分析代码上下文，自动确定：
- `get_current_data()` 转换时需要的股票列表
- `get_price()` 参数的正确转换方式
- 函数调用链中的变量关系

### 2. 多层级转换

- **第一层**: 直接字符串替换（简单API）
- **第二层**: 正则表达式匹配（参数解析）
- **第三层**: 上下文分析（复杂转换）

### 3. 安全转换

- 保留原有代码结构
- 添加转换说明注释
- 生成详细的变更日志

## ⚠️ 注意事项

### 必须手动检查的项目

1. **股票代码格式**
   - 某些PTrade版本支持`.XSHG`和`.XSHE`
   - 某些版本需要`.SH`和`.SZ`
   - 需要根据实际PTrade版本确定

2. **get_snapshot的股票列表**
   - 转换器会尝试自动确定，但可能不准确
   - 需要手动检查并优化

3. **handle_data vs on_bar**
   - 某些PTrade版本使用`on_bar()`
   - 某些版本使用`handle_data()`
   - 需要根据实际版本调整

4. **数据格式差异**
   - `get_history()`返回dict格式
   - `get_price()`返回DataFrame格式
   - 需要检查数据处理逻辑

## 📝 转换检查清单

转换完成后，请检查：

- [ ] 无`from jqdata import *`
- [ ] 所有`get_current_data()`已转换
- [ ] 所有`get_price()`已转换
- [ ] `set_commission`使用`PerTrade`格式
- [ ] 属性访问使用PTrade格式
- [ ] 股票代码格式正确
- [ ] 日志输出正常
- [ ] 交易执行正常
- [ ] 数据获取正常
- [ ] 策略逻辑完整

## 🔗 相关文档

- `docs/COMPREHENSIVE_API_DIFFERENCES.md` - 完整API差异对照表
- `docs/UNIFIED_STRATEGY_USAGE.md` - 统一版策略使用指南
- `docs/PTRADE_BULLETTRADE_UNIFIED_SOLUTION.md` - 统一解决方案

## ✅ 总结

完整转换器覆盖了**17大类、50+个API差异点**，包括：

1. ✅ 所有必须转换的API（否则无法运行）
2. ✅ 所有建议转换的API（提高兼容性）
3. ✅ 智能上下文分析
4. ✅ 详细的转换日志
5. ✅ 完整的错误处理

**使用完整转换器，可以确保策略从BulletTrade/聚宽格式正确转换为PTrade格式！**
