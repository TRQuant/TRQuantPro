# Investment Advisor V4.0 BulletTrade回测指南

> **版本**: V1.0  
> **日期**: 2026-01-08  
> **Python环境**: `ope/venv/bin/python3`

---

## 📋 目录

1. [环境准备](#环境准备)
2. [策略代码规范](#策略代码规范)
3. [回测执行](#回测执行)
4. [结果分析](#结果分析)
5. [常见问题](#常见问题)

---

## 🔧 环境准备

### Python环境

**使用项目虚拟环境**:
```bash
# 使用ope/venv/bin/python3
/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python3
```

### 依赖检查

确保已安装以下依赖：
- `bullet-trade` - BulletTrade回测引擎
- `jqdatasdk` - 聚宽数据API
- `pandas`, `numpy` - 数据处理

---

## 📝 策略代码规范

### 聚宽API规范

根据聚宽RAG知识库，策略代码必须遵循以下规范：

#### 1. 导入规范

```python
# BulletTrade与聚宽API兼容
from jqdata import *
from jqlib.technical_analysis import *
import numpy as np
import pandas as pd
```

**说明**:
- `from jqdata import *` - 导入所有聚宽API函数（BulletTrade兼容）
- `from jqlib.technical_analysis import *` - 导入技术分析函数（可选）

#### 2. 初始化函数规范

```python
def initialize(context):
    """策略初始化"""
    # 基准设置
    set_benchmark('000300.XSHG')
    
    # 滑点设置（固定滑点0.1%）
    set_slippage(FixedSlippage(0.001))
    
    # 手续费设置（聚宽标准费率）
    set_order_cost(OrderCost(
        open_tax=0,              # 买入无印花税
        close_tax=0.001,         # 卖出印花税0.1%
        open_commission=0.0003,   # 买入佣金0.03%
        close_commission=0.0003, # 卖出佣金0.03%
        min_commission=5          # 最低佣金5元
    ), type='stock')
    
    # 真实价格模式（使用真实成交价）
    set_option('use_real_price', True)
    
    # 定时任务
    run_daily(before_market_open, time='09:00')
    run_weekly(market_open, weekday=0, time='09:35')  # 0=周一
    run_daily(check_risk, time='14:50')
    run_daily(after_market_close, time='15:30')
```

#### 3. 数据获取API规范

**get_price()** - 获取价格数据:

```python
# 单只股票
prices = get_price('000001.XSHE', 
                   end_date='2024-12-20', 
                   count=21, 
                   frequency='daily', 
                   fields=['close'], 
                   panel=False, 
                   fq='post')

# 多只股票（panel=False时返回DataFrame，包含code列）
prices = get_price(['000001.XSHE', '000002.XSHE'], 
                   end_date='2024-12-20', 
                   count=21, 
                   frequency='daily', 
                   fields=['close'], 
                   panel=False, 
                   fq='post')

# 处理多只股票数据
if 'code' in prices.columns:
    # 多只股票：按code分组
    for code in codes:
        code_data = prices[prices['code'] == code]
        # 处理单只股票数据
else:
    # 单只股票：直接使用
    # 处理数据
```

**get_fundamentals()** - 获取财务数据:

```python
# 查询市值
q = query(valuation.code, valuation.market_cap).filter(
    valuation.code.in_(codes)
)
fund_df = get_fundamentals(q, date=date_str)

# 查询ROE
q = query(indicator.code, indicator.roe).filter(
    indicator.code.in_(codes)
)
fund_df = get_fundamentals(q, date=date_str)
```

**get_index_stocks()** - 获取指数成分股:

```python
# 获取沪深300成分股
stocks = get_index_stocks('000300.XSHG')
```

#### 4. 交易执行API规范

```python
# 按目标金额下单
order_target_value(stock, target_value)

# 按目标数量下单
order_target(stock, target_amount)

# 按金额下单
order_value(stock, value)

# 按数量下单
order(stock, amount)
```

#### 5. 定时任务规范

```python
# 每日运行
run_daily(func, time='09:00')

# 每周运行（weekday: 0=周一, 1=周二, ..., 4=周五）
run_weekly(func, weekday=0, time='09:35')

# 每月运行
run_monthly(func, tradingday=1, time='09:00')
```

---

## 🚀 回测执行

### 方法1: 使用回测脚本（推荐）

```bash
# 使用项目虚拟环境
/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python3 \
    scripts/run_bullettrade_backtest_v4.py \
    --start-date 2024-01-01 \
    --end-date 2024-12-31 \
    --initial-capital 1000000 \
    --max-stocks 10 \
    --single-position 0.20 \
    --stop-loss -0.08 \
    --take-profit 0.30
```

### 方法2: 使用Python API

```python
from core.advisor_v4.bullettrade_backtest import BulletTradeBacktest, StrategyConfig
from core.bullettrade.config import BTConfig

# 配置策略参数
strategy_config = StrategyConfig(
    max_stocks=10,
    single_position_max=0.20,
    stop_loss=-0.08,
    take_profit=0.30,
)

# 配置回测参数
bt_config = BTConfig(
    start_date="2024-01-01",
    end_date="2024-12-31",
    initial_capital=1000000.0,
    benchmark="000300.XSHG",
)

# 创建回测接口
backtest = BulletTradeBacktest(
    strategy_config=strategy_config,
    bt_config=bt_config,
    output_dir="output/advisor_v4/bullettrade"
)

# 执行回测
result = backtest.run_backtest(
    start_date="2024-01-01",
    end_date="2024-12-31",
    initial_capital=1000000.0,
)

# 查看结果
print(f"总收益率: {result.total_return:.2%}")
print(f"夏普比率: {result.sharpe_ratio:.2f}")
print(f"最大回撤: {result.max_drawdown:.2%}")
```

### 方法3: 简化接口

```python
from core.advisor_v4.bullettrade_backtest import run_backtest_simple

# 一键回测
result = run_backtest_simple(
    start_date="2024-01-01",
    end_date="2024-12-31",
    initial_capital=1000000.0,
)
```

---

## 📊 结果分析

### 回测结果指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| **总收益率** | 整个回测期间的总收益率 | > 20% |
| **年化收益** | 年化收益率 | > 15% |
| **夏普比率** | 风险调整后收益 | > 1.0 |
| **最大回撤** | 最大回撤幅度 | < 20% |
| **卡玛比率** | 年化收益/最大回撤 | > 0.5 |
| **胜率** | 盈利交易占比 | > 50% |
| **总交易次数** | 总交易次数 | - |

### 结果文件

回测完成后，会在输出目录生成以下文件：

```
output/advisor_v4/bullettrade/
├── advisor_v4_validated_factors_YYYYMMDD_HHMMSS.py  # 策略代码
├── backtest_results/
│   ├── summary_YYYY-MM-DD_YYYY-MM-DD.json          # 回测摘要
│   ├── backtest.log                                 # 回测日志
│   ├── nav_curve.csv                                # 净值曲线
│   ├── trades.csv                                   # 交易记录
│   └── report.html                                  # HTML报告（如果启用）
```

---

## ❓ 常见问题

### 1. get_price返回格式问题

**问题**: `get_price` 多只股票时返回格式不一致

**解决**: 检查 `'code'` 列是否存在：

```python
prices = get_price(codes, end_date=date_str, count=21, 
                   frequency='daily', fields=['close'], 
                   panel=False, fq='post')

if 'code' in prices.columns:
    # 多只股票：按code分组
    for code in codes:
        code_data = prices[prices['code'] == code]
        # 处理数据
else:
    # 单只股票：直接使用
    # 处理数据
```

### 2. query导入问题

**问题**: `query` 未定义

**解决**: 确保使用 `from jqdata import *`，这会导入所有聚宽API函数，包括 `query`。

### 3. run_weekly参数问题

**问题**: `run_weekly` 的 `weekday` 参数值

**解决**: 
- `0` = 周一
- `1` = 周二
- `2` = 周三
- `3` = 周四
- `4` = 周五

### 4. BulletTrade引擎导入失败

**问题**: `ImportError: 无法导入BulletTrade`

**解决**: 
```bash
# 安装BulletTrade
pip install bullet-trade

# 或使用项目虚拟环境
/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/pip install bullet-trade
```

### 5. 策略代码语法错误

**问题**: 生成的策略代码有语法错误

**解决**: 
1. 检查生成的策略代码文件
2. 使用Python语法检查：
   ```bash
   python -m py_compile strategies/bullettrade/advisor_v4_validated_factors_*.py
   ```

---

## 📚 参考文档

1. **聚宽API知识库**: `DevMustRead/JQDATA_API_KNOWLEDGE_BASE.md`
2. **BulletTrade文档**: `docs/07_workflow/BULLETTRADE_BACKTEST_GUIDE.md`
3. **策略设计文档**: `docs/advisor_v4/COMPLETE_FACTOR_STRATEGY_DESIGN.md`
4. **完整实现文档**: `docs/advisor_v4/VALIDATED_FACTOR_STRATEGY_COMPLETE.md`

---

## ✅ 检查清单

在执行回测前，请确认：

- [ ] Python环境：使用 `ope/venv/bin/python3`
- [ ] 策略代码：已生成并符合聚宽API规范
- [ ] 数据源：JQData已配置并可访问
- [ ] BulletTrade：已安装并可导入
- [ ] 回测参数：日期、资金、参数已正确设置
- [ ] 输出目录：有写入权限

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-08  
**版本**: V1.0
