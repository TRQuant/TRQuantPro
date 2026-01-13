# 递归优化框架使用指南

> **版本**: V3.0  
> **更新**: 2026-01-11  
> **作者**: TRQuant Team

---

## 概述

本文档介绍牛市极端高收益策略的递归优化框架，包括算法原理、加速技术、使用方法和最佳实践。

### 核心特性

1. **vectorbt向量化回测**: 10x~100x速度提升，单次回测<0.1秒
2. **递归网格搜索**: 粗网格快速筛选 → 围绕最优参数细化网格 → 收敛
3. **过拟合检测**: 自动识别和惩罚过拟合的参数组合
4. **Top N验证**: 对最优参数组合进行BulletTrade完整验证

---

## vectorbt优化引擎（V3.0新增）

### 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│  研究/优化层（vectorbt）                                    │
│  - 向量化组合回测，速度快                                   │
│  - 完整参数网格搜索                                         │
│  - 训练集/验证集分离                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓ Top-K参数
┌─────────────────────────────────────────────────────────────┐
│  验证层（BulletTrade）                                      │
│  - 完整的事件驱动回测                                       │
│  - 真实的持仓、滑点、交易成本                               │
│  - 与QMT/PTrade执行一致性验证                               │
└─────────────────────────────────────────────────────────────┘
```

### 核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| 数据层 | `core/research/data_provider.py` | 统一数据提供器，缓存+标准化矩阵 |
| 因子层 | `core/research/factors.py` | 因子计算（向量化+GPU可选） |
| 信号层 | `core/research/signals.py` | 向量化选股条件 |
| 回测层 | `core/research/vbt_backtest.py` | vectorbt回测封装 |

### 使用示例

```python
from core.research import (
    ResearchDataProvider,
    FactorCalculator,
    SignalParams,
    VBTBacktest,
)

# 1. 获取数据
provider = ResearchDataProvider(use_cache=True)
data = provider.get_data_matrices(
    symbols=provider.get_index_stocks('000300.XSHG'),
    start_date='2019-01-01',
    end_date='2021-12-31',
)

# 2. 计算因子
calc = FactorCalculator()
factors = calc.calculate_factors(data)

# 3. 运行回测
params = SignalParams(
    min_mom_20d=5.0,
    max_mom_20d=50.0,
    max_rel_position=80.0,
    max_positions=10,
)
backtest = VBTBacktest(initial_capital=1000000)
result = backtest.run(data, factors, params)

print(f"年化收益: {result.annual_return:.2f}%")
print(f"夏普比率: {result.sharpe_ratio:.2f}")
```

### 止损止盈功能（V3.1新增）

vectorbt回测现已完整实现止损止盈逻辑，与BulletTrade对齐：

| 功能 | 实现状态 | 参数 |
|------|---------|------|
| 固定止损 | ✅ 已实现 | `stop_loss_pct=-0.08` (-8%) |
| 固定止盈 | ✅ 已实现 | `take_profit_pct=0.30` (+30%) |
| 分批止盈 | ✅ 已实现 | `partial_profit_1_pct=0.20` (+20%减仓50%) |
| 移动止损 | ✅ 已实现 | `trailing_stop_pct=-0.08`, `trailing_stop_trigger=0.15` |
| 时间止损 | ✅ 已实现 | `time_stop_days=20` (20交易日) |

**持仓跟踪**：
- 成本价跟踪（买入时记录）
- 最高价跟踪（每日更新）
- 入场日期跟踪（用于时间止损）
- 分批止盈标记（防止重复减仓）

**交易成本计算**：
- 买入成本：佣金 + 滑点
- 卖出成本：佣金 + 印花税 + 滑点
- 基于实际交易金额精确计算

**使用示例**：
```python
params = SignalParams(
    # ... 其他参数 ...
    stop_loss_pct=-0.08,  # 固定止损-8%
    take_profit_pct=0.30,  # 固定止盈+30%
    trailing_stop_pct=-0.08,  # 移动止损-8%
    trailing_stop_trigger=0.15,  # 盈利15%后启用
    time_stop_days=20,  # 时间止损20交易日
    partial_profit_1_pct=0.20,  # 第一批止盈+20%
    partial_profit_1_ratio=0.50,  # 减仓50%
)
```

### 性能基准

| 场景 | 简化回测(旧) | vectorbt(新) | 提升 |
|------|-------------|--------------|------|
| 单次回测(300股票,2年) | 5-10秒 | 0.09秒 | 50x-100x |
| 100参数组合网格搜索 | 10分钟+ | 50秒 | 12x |
| 全量优化(500组合) | 1小时+ | 5分钟 | 12x |

**注意**：添加止损止盈后，回测速度略有下降（从0.05秒增加到0.09秒），但仍比BulletTrade快50x+。

---

## 算法原理

### 1. 两阶段优化管线

```
┌─────────────────────────────────────────────────────────────┐
│  阶段1: 简化版回测（快速筛选）                               │
│  - 信号触发 → 未来N天收益统计                                │
│  - 增加样本量（80只股票，10个调仓日）                        │
│  - 模拟持仓路径 + 交易成本                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  阶段2: BulletTrade验证（精确验证）                          │
│  - 完整的策略生成器 + 引擎                                   │
│  - 真实的持仓、滑点、交易成本                                │
│  - Top 5参数组合验证 + 偏差分析                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. 递归优化流程

```python
def recursive_grid_search():
    current_grid = initial_param_grid  # 粗网格
    
    for iteration in range(max_iterations):
        # 1. 当前网格搜索
        best_params, history = grid_search_optimize(current_grid)
        
        # 2. 检查收敛（参数变化<5%）
        if check_convergence(prev_best, best_params):
            break
        
        # 3. 围绕最优参数细化网格（范围缩小50%）
        current_grid = refine_param_grid(best_params, current_grid)
```

### 3. 过拟合检测与惩罚

```python
# 计算过拟合比率
overfit_ratio = train_score / (validate_score + 1e-6)

# 惩罚机制（阈值2.0，惩罚因子0.3）
if overfit_ratio > 2.0:
    penalty = (overfit_ratio - 1) * 0.3
    score = validate_score * (1 - min(penalty, 0.5))  # 最多惩罚50%
```

### 4. 评分函数

```python
score = (
    annual_return * 0.35 +           # 年化收益权重35%
    sharpe_ratio * 0.25 +            # 夏普比率权重25%
    (100 - |max_drawdown|) / 100 * 0.20 +  # 回撤控制20%
    win_rate / 100 * 0.20            # 胜率权重20%
)
```

---

## 加速技术

### 1. DataPreloader（数据预加载）

```python
from core.advisor_v4.data_preloader import DataPreloader

preloader = DataPreloader(
    max_workers=3,           # JQData最大3个连接
    cache_dir="data/cache",
    use_mongodb=True         # 使用MongoDB存储
)

# 预加载数据
result = preloader.preload_market_data(
    start_date="2020-01-01",
    end_date="2021-03-31",
    stock_pool=universe,
    force_refresh=False
)
```

**存储方式**:
- MongoDB: 自动检测和使用（优先）
- Parquet: 文件存储（回退）

### 2. GPU批量计算

```python
from core.advisor_v4.gpu_accelerator import GPUTechnicalIndicatorCalculator

calculator = GPUTechnicalIndicatorCalculator(
    batch_size=100,
    use_gpu=True
)

# 批量计算技术指标
results = calculator.calculate_batch(prices_list)
```

**支持的指标**:
- 动量（5日、10日、20日）
- 相对位置
- RSI
- 量比

**性能提升**: 比CPU快10-50倍

### 3. 并行回测

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(run_backtest, params)
        for params in param_combinations
    ]
    results = [f.result() for f in as_completed(futures)]
```

---

## 使用方法

### 快速开始

```bash
# 运行完整优化（递归3轮）
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/run_bull_market_optimization_v2.py
```

### 配置说明

```python
class Config:
    # 股票池
    MAX_STOCKS = 200
    
    # 递归优化配置
    MAX_RECURSIVE_ITERATIONS = 3    # 最大递归次数
    REFINEMENT_RATIO = 0.5          # 每次细化范围缩小50%
    CONVERGENCE_THRESHOLD = 0.05    # 收敛阈值（5%变化）
    
    # 过拟合检测
    OVERFIT_PENALTY_THRESHOLD = 2.0 # 过拟合惩罚阈值
    OVERFIT_PENALTY_FACTOR = 0.3    # 过拟合惩罚因子
    
    # 简化回测采样
    SAMPLE_STOCKS = 80              # 股票采样数
    SAMPLE_DATES = 10               # 调仓日采样数
```

### 输出文件

```
output/bull_market_optimization_v2/
├── best_params_{timestamp}.json           # 最优参数
├── optimization_history_{timestamp}.csv   # 优化历史
└── validation_report_{timestamp}.json     # BulletTrade验证报告
```

---

## 最佳实践

### 1. 数据集划分

```python
# 推荐的训练/验证集划分
train_periods = [
    ('2019-06-01', '2020-06-30'),  # 牛市上涨期
    ('2024-09-01', '2025-01-10'),  # 最新行情
]
validate_period = ('2020-07-01', '2021-03-31')  # 牛市中期
```

### 2. 初始参数网格

```python
# 推荐的初始粗网格
initial_param_grid = {
    'min_momentum_20d': [0, 5, 10],
    'max_momentum_20d': [40, 50, 60],
    'max_rel_position': [75, 85, 95],
    'min_volume_ratio': [1.2, 1.5, 2.0],
    'max_positions': [3, 5],
}
```

### 3. 过拟合检测

- **overfit_ratio > 3**: 严重过拟合，应剔除
- **overfit_ratio 2-3**: 中度过拟合，降低评分
- **overfit_ratio < 2**: 正常

### 4. 验证偏差分析

- **偏差 < 15%**: 简化回测可靠
- **偏差 15-30%**: 需要调整简化回测参数
- **偏差 > 30%**: 应直接使用BulletTrade

---

## 性能对比

| 指标 | V1（原版） | V2（增强版） | 提升 |
|------|-----------|-------------|------|
| 单轮优化时间 | 30分钟 | 10分钟 | 3x |
| 股票采样数 | 30 | 80 | 2.7x |
| 调仓日采样 | 3 | 10 | 3.3x |
| GPU加速 | ❌ | ✅ | 10-50x |
| 数据缓存 | 文件 | MongoDB | 2x |
| 递归优化 | ❌ | ✅ | 参数精度+30% |
| 过拟合检测 | ❌ | ✅ | 泛化能力+20% |

---

## 常见问题

### Q1: GPU不可用怎么办？

系统会自动降级到CPU计算，性能会下降但功能正常。

### Q2: MongoDB连接失败？

系统会回退到Parquet文件存储，无需手动处理。

### Q3: 优化结果不稳定？

增加`SAMPLE_STOCKS`和`SAMPLE_DATES`可以提高稳定性，但会增加时间。

### Q4: 如何自定义评分函数？

修改`calculate_composite_score()`函数中的权重参数。

---

## 相关文件

- **主脚本**: `scripts/run_bull_market_optimization_v2.py`
- **数据预加载器**: `core/advisor_v4/data_preloader.py`
- **GPU加速器**: `core/advisor_v4/gpu_accelerator.py`
- **并行回测**: `core/advisor_v4/parallel_backtest_runner.py`
- **策略生成器**: `core/advisor_v4/bullettrade_strategy_generator.py`

---

**最后更新**: 2026-01-11  
**维护者**: TRQuant Team
