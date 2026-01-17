# 策略平台适配指南

## 📊 问题背景

在PTrade中运行策略时出现：
```
ModuleNotFoundError: No module named 'jqdata'
```

**根本原因**: PTrade、聚宽(JQData)、BulletTrade是不同的平台，API有本质差异。

## 🔧 解决方案

### 1. 策略生成器（推荐）

直接生成平台原生策略：

```python
from tools.strategy_generator import generate_strategy

# 生成PTrade策略
result = generate_strategy(
    platform='ptrade',  # 指定目标平台
    style='momentum_growth',
    factors=['momentum_20d', 'ROE_ttm'],
    risk_params={'max_stocks': 5, 'stop_loss': 0.08},
    output_path='strategies/ptrade/my_strategy.py'
)
```

**支持的平台**:
- `ptrade`: PTrade交易终端
- `jqdata`: 聚宽研究平台
- `bullettrade`: BulletTrade本地回测
- `qmt`: QMT量化交易

### 2. 策略转换器

将现有策略转换为其他平台格式：

```python
from core.strategy_converter import convert_strategy_to_ptrade

result = convert_strategy_to_ptrade(
    'strategies/bullettrade/my_strategy.py',
    'strategies/ptrade/my_strategy_ptrade.py'
)

print(f"转换: {'成功' if result['success'] else '失败'}")
print(f"警告: {result['warnings']}")
```

## 📁 策略文件位置

| 平台 | 目录 | 说明 |
|------|------|------|
| PTrade | `strategies/ptrade/` | PTrade原生策略 |
| BulletTrade | `strategies/bullettrade/` | 本地回测策略 |
| 聚宽 | `strategies/jqdata/` | 聚宽研究策略 |
| QMT | `strategies/qmt/` | QMT策略 |

## 🔍 关键API差异

### 模块导入
| 平台 | 导入方式 |
|------|---------|
| PTrade | 不需要导入，API内置 |
| 聚宽/BulletTrade | `from jqdata import *` |
| QMT | `from xtquant import xtdata` |

### 滑点设置
| 平台 | 代码 |
|------|------|
| PTrade | `set_slippage(0.001)` |
| 聚宽/BulletTrade | `set_slippage(FixedSlippage(0.001))` |

### 佣金设置
| 平台 | 代码 |
|------|------|
| PTrade | `set_commission(commission=0.0003, min_commission=5)` |
| 聚宽 | `set_order_cost(OrderCost(...), type='stock')` |

### 数据获取
| 平台 | 代码 |
|------|------|
| PTrade | `get_history(20, '1d', stocks, ['close'])` |
| 聚宽 | `get_price(stocks, end_date=..., count=20, ...)` |

## 📋 可用策略文件

### PTrade原生策略
```
strategies/ptrade/TRQuant_momentum_v3_ptrade_native.py  # 手动适配
strategies/ptrade/TRQuant_momentum_v4_ptrade.py        # 生成器生成
```

### BulletTrade改进策略
```
strategies/bullettrade/TRQuant_momentum_v3_improved.py  # 改进版（已修复选股问题）
```

## 🚀 使用流程

### 方案A: 直接生成PTrade策略

```bash
cd /home/taotao/dev/QuantTest/TRQuant

# 使用生成器
python tools/strategy_generator.py ptrade momentum_growth > strategies/ptrade/new_strategy.py

# 或在Python中
python << 'PYEOF'
from tools.strategy_generator import generate_strategy

result = generate_strategy(
    platform='ptrade',
    style='momentum_growth',
    factors=['momentum_20d', 'ROE_ttm'],
    output_path='strategies/ptrade/new_strategy.py'
)
print(f"生成{'成功' if result['success'] else '失败'}")
PYEOF
```

### 方案B: 转换现有策略

```bash
python core/strategy_converter.py strategies/bullettrade/my_strategy.py
# 输出: strategies/bullettrade/my_strategy_ptrade.py
```

## ✅ 检查清单

在PTrade运行策略前，确保：

- [ ] 无 `from jqdata import *`
- [ ] `set_slippage()` 使用数值参数
- [ ] `set_commission()` 使用PTrade格式
- [ ] 数据获取使用 `get_history()`
- [ ] 属性名称正确（open/up_limit/down_limit）

## 📝 相关文档

- `docs/PTRADE_API_COMPATIBILITY.md` - 详细API对照表
- `docs/BULLETTRADE_IMPROVEMENTS.md` - BulletTrade回测改进
- `core/strategy_converter.py` - 策略转换器源码
- `tools/strategy_generator.py` - 策略生成器源码
