# PTrade/BulletTrade统一解决方案

## 🎯 问题解决

### 原始问题
```
TypeError: set_commission() got an unexpected keyword argument 'commission'
```

### 根本原因
PTrade和BulletTrade都使用`PerTrade`对象设置佣金，而不是关键字参数：
- ❌ 错误：`set_commission(commission=0.0003, min_commission=5)`
- ✅ 正确：`set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))`

## ✅ 解决方案

### 1. API知识库（MongoDB）

**位置**: `trquant.platform_api_kb`

**内容**:
- PTrade API规范
- BulletTrade API规范
- 平台兼容性信息
- API使用示例

**初始化**:
```python
python3 -c "from pymongo import MongoClient; ..."  # 已执行
```

### 2. 统一版策略

**文件**: `strategies/unified/TRQuant_momentum_unified.py`

**特点**:
- 同时兼容PTrade和BulletTrade
- 使用`PerTrade`设置佣金
- 使用`FixedSlippage`设置滑点
- 自动适配数据获取API

**使用方法**:
```python
# PTrade: 直接使用
# BulletTrade: 在文件开头添加 "from jqdata import *"
```

### 3. 策略生成器更新

**文件**: `tools/strategy_generator.py`

**改进**:
- PTrade模板使用`PerTrade`格式
- BulletTrade模板使用`PerTrade`格式（与PTrade兼容）
- 自动计算`sell_cost = commission + 0.001`（印花税）

### 4. 策略转换器更新

**文件**: `core/strategy_converter.py`

**改进**:
- 正确转换`set_order_cost` -> `set_commission(PerTrade(...))`
- 修复错误的`set_commission(commission=...)`格式
- 保留`PerTrade`格式（两个平台都支持）

### 5. 平台API知识库MCP服务器

**文件**: `mcp_servers/platform_api_server.py`

**功能**:
- 查询平台API信息
- 获取平台兼容性
- 为策略生成提供API规范

## 📋 API对照表

### set_commission

| 平台 | 正确格式 |
|------|---------|
| PTrade | `set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))` |
| BulletTrade | `set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))` |
| 聚宽 | `set_order_cost(OrderCost(open_tax=0, close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')` |

### set_slippage

| 平台 | 正确格式 |
|------|---------|
| PTrade | `set_slippage(FixedSlippage(0.001))` |
| BulletTrade | `set_slippage(FixedSlippage(0.001))` |

### 数据获取

| 平台 | API |
|------|-----|
| PTrade | `get_history(count, '1d', stocks, ['close'], skip_paused=False, fq='pre')` |
| BulletTrade | `get_price(stocks, end_date=date, frequency='daily', fields=['close'], count=20, panel=False)` |

## 🚀 使用流程

### 方案1: 使用统一版策略（推荐）

```bash
# 1. 复制统一版策略
cp strategies/unified/TRQuant_momentum_unified.py /path/to/ptrade/

# 2. 在PTrade中直接运行
# 或在BulletTrade中，在文件开头添加 "from jqdata import *"
```

### 方案2: 使用策略生成器

```python
from tools.strategy_generator import generate_strategy

result = generate_strategy(
    platform='ptrade',  # 或 'bullettrade'
    style='momentum_growth',
    factors=['momentum_20d', 'ROE_ttm'],
    risk_params={
        'max_stocks': 5,
        'stop_loss': 0.08,
        'take_profit': 0.30,
    },
    output_path='strategies/ptrade/my_strategy.py'
)
```

### 方案3: 转换现有策略

```python
from core.strategy_converter import convert_strategy_to_ptrade

result = convert_strategy_to_ptrade(
    'strategies/bullettrade/my_strategy.py',
    'strategies/ptrade/my_strategy_ptrade.py'
)
```

## 📊 验证清单

在PTrade运行策略前，检查：

- [ ] 无`from jqdata import *`（PTrade不需要）
- [ ] `set_commission`使用`PerTrade`格式
- [ ] `set_slippage`使用`FixedSlippage`格式
- [ ] 数据获取API正确（`get_history`或`get_price`）
- [ ] 属性名称正确（`open`/`up_limit`等）

## 🔍 故障排查

### 错误1: set_commission参数错误
```
TypeError: set_commission() got an unexpected keyword argument 'commission'
```
**解决**: 使用`PerTrade`格式：
```python
set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
```

### 错误2: ModuleNotFoundError: No module named 'jqdata'
**解决**: PTrade不需要导入，删除`from jqdata import *`

### 错误3: get_price not defined
**解决**: PTrade使用`get_history`，BulletTrade使用`get_price`

## 📁 相关文件

| 文件 | 用途 |
|------|------|
| `strategies/unified/TRQuant_momentum_unified.py` | 统一版策略（推荐） |
| `tools/strategy_generator.py` | 策略生成器 |
| `core/strategy_converter.py` | 策略转换器 |
| `mcp_servers/platform_api_server.py` | API知识库MCP服务器 |
| `docs/PTRADE_API_COMPATIBILITY.md` | API兼容性文档 |

## ✅ 完成状态

- [x] API知识库创建
- [x] 统一版策略创建
- [x] 策略生成器更新
- [x] 策略转换器更新
- [x] MCP服务器创建
- [x] 文档完善

## 🎉 总结

现在TRQuant系统可以：
1. **生成兼容策略**: 自动生成PTrade和BulletTrade兼容的策略代码
2. **转换策略**: 将现有策略转换为目标平台格式
3. **查询API**: 通过MCP服务器查询平台API规范
4. **统一运行**: 使用统一版策略在两个平台无缝运行

**关键发现**: PTrade和BulletTrade在`set_commission`和`set_slippage`上使用相同的API格式（`PerTrade`和`FixedSlippage`），这使得代码可以在两个平台间无缝迁移。
