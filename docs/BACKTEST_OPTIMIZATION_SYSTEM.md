# 回测优化系统设计文档

## 1. 系统概述

### 1.1 核心目标
- **算法验证**: 通过历史回测验证筛选算法的有效性
- **自动优化**: 基于回测表现自动调整因子权重
- **市场适应**: 根据不同市场环境调整策略参数
- **防过拟合**: 通过交叉验证和正则化防止过度拟合
- **精选输出**: 最终浓缩到5个最优投资标的

### 1.2 设计原则
```
抓主要逻辑 → 防止过拟合 → 持续优化
```

## 2. 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     回测优化系统 (Backtest Optimizer)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │ 市场环境识别 │───▶│ 因子权重优化 │───▶│ 最终选股器   │      │
│  │ MarketRegime │    │ FactorOptim  │    │ FinalSelect  │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────────────────────────────────────────────┐       │
│  │               回测引擎 (BacktestEngine)              │       │
│  │  - 历史时点模拟    - 多周期收益计算                  │       │
│  │  - 风险指标评估    - 滚动回测验证                    │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 3. 模块详解

### 3.1 回测引擎 (BacktestEngine)

**功能**: 验证筛选算法的历史表现

**回测周期**:
| 周期 | 交易日 | 用途 |
|------|--------|------|
| 周 | 5 | 短期验证，信号有效性 |
| 月 | 21 | 主要验证周期 |
| 季 | 63 | 中期趋势验证 |
| 年 | 252 | 长期价值验证 |
| 五年 | 1260 | 超长期验证 |

**核心指标**:
- 平均收益率
- 胜率 (正收益占比)
- 超额收益 (相对沪深300)
- 夏普比率
- 最大回撤

**关键代码**:
```python
class BacktestEngine:
    def run_rolling_backtest(self, start_date, end_date, frequency='month'):
        """滚动回测 - 模拟历史时点的实际筛选"""
        for test_date in test_dates:
            # 1. 使用历史数据执行筛选
            selected = screener_func(as_of_date=test_date)
            
            # 2. 计算各周期实际收益
            for period in ['week', 'month', 'quarter', 'year']:
                future_return = calc_return(test_date, test_date + period)
                
            # 3. 与基准对比
            benchmark_return = calc_benchmark_return(...)
```

### 3.2 因子权重优化器 (FactorOptimizer)

**目标**: 学习最优的因子权重组合

**因子分类**:
```
├── 基本面因子 (Fundamental)
│   ├── ROE
│   └── 毛利率
├── 成长因子 (Growth)  
│   ├── 营收增长
│   └── 利润增长
├── 估值因子 (Valuation)
│   ├── PE估值
│   └── PEG
├── 技术因子 (Technical)
│   ├── 趋势强度
│   └── 动量
└── 板块因子 (Sector)
    └── 主线板块权重
```

**防过拟合机制**:

1. **时序交叉验证**:
```python
# 训练/验证集划分 (70%/30%)
train_results = backtest_results[:split_idx]
val_results = backtest_results[split_idx:]

# 5折时序交叉验证
for fold in range(5):
    train_fold = ...
    val_fold = ...
    score = evaluate(optimized_weights, val_fold)
```

2. **L2正则化**:
```python
# 惩罚极端权重
def objective(weights):
    score = evaluate(weights)
    penalty = regularization * np.sum(weights ** 2)
    return -score + penalty  # 最小化负得分+惩罚
```

3. **权重约束**:
```python
# 每个因子权重限制在[0.01, 0.5]
bounds = [(0.01, 0.5) for _ in factors]
```

**优化算法**:
- 贝叶斯优化 (默认，高效)
- 网格搜索 (全面但慢)
- 随机搜索 (快速探索)

### 3.3 市场环境适配器 (MarketRegimeAdapter)

**市场状态定义**:
| 状态 | 描述 | 仓位上限 | 止损 |
|------|------|----------|------|
| STRONG_BULL | 强牛市 | 90% | 10% |
| BULL | 牛市 | 80% | 8% |
| NEUTRAL | 震荡市 | 60% | 6% |
| BEAR | 熊市 | 40% | 5% |
| STRONG_BEAR | 强熊市 | 20% | 3% |

**识别维度**:
- 20日/60日收益率
- 均线位置 (MA5/MA20/MA60)
- 波动率水平
- 市场宽度 (涨跌比、站上MA20比例)

**因子权重调整**:
```python
# 牛市：强调动量和成长
BULL_ADJUSTMENTS = {
    'momentum_score': 1.5,  # 动量权重×1.5
    'growth_score': 1.2,
    'value_score': 0.7,     # 估值权重×0.7
}

# 熊市：强调价值和防守
BEAR_ADJUSTMENTS = {
    'momentum_score': 0.5,
    'growth_score': 0.9,
    'value_score': 1.5,
    'roe': 1.3,
}
```

### 3.4 最终选股器 (FinalSelector)

**浓缩原则**: 从30只候选 → 5只最优

**筛选步骤**:
```
Step 1: 综合得分计算
├── 原始得分 × 0.4
├── 成长性得分 × 0.25
├── 估值得分 × 0.15
└── 动量得分 × 0.20

Step 2: 分散化约束
├── 每个板块最多2只
└── 至少覆盖3个板块

Step 3: 风险过滤
├── 市值 > 30亿
└── PE合理 (0-200)

Step 4: 最终选择Top 5
└── 优先保证板块多样性
```

**仓位分配**:
```python
# 基于得分的权重
base_weight = stock_score / total_score

# 约束：每只10%-30%
weight = max(0.10, min(0.30, base_weight))

# 止损/止盈设置
if regime == 'bear':
    stop_loss = 5%
    take_profit = 10%
elif regime == 'bull':
    stop_loss = 10%
    take_profit = 30%
```

## 4. 奖励机制设计

### 4.1 收益率奖励
```python
def calculate_reward(backtest_result):
    """
    奖励 = 收益率 + 超额收益 + 胜率奖励
    """
    # 基础奖励：绝对收益
    base_reward = avg_return
    
    # 超额奖励：跑赢基准
    excess_reward = excess_return * 1.5  # 超额收益加权
    
    # 胜率奖励：稳定性
    win_rate_reward = (win_rate - 50) * 0.5  # 超过50%胜率有奖励
    
    # 风险惩罚：高波动扣分
    risk_penalty = -max_drawdown * 0.3
    
    return base_reward + excess_reward + win_rate_reward + risk_penalty
```

### 4.2 多周期验证
```python
# 短中长期都要验证
period_weights = {
    'week': 0.1,    # 短期权重低（噪音大）
    'month': 0.4,   # 月度为主
    'quarter': 0.3, # 季度验证
    'year': 0.2,    # 年度参考
}

total_reward = sum(
    period_weights[p] * calc_reward(results[p])
    for p in period_weights
)
```

### 4.3 持续学习
```python
class AdaptiveWeightManager:
    """自适应权重管理器"""
    
    def update(self, new_performance):
        """根据最新表现更新权重"""
        for factor, perf in new_performance.items():
            # 指数移动平均更新
            self.weights[factor] = (
                (1 - learning_rate) * self.weights[factor] +
                learning_rate * perf
            )
        
        # 定期衰减（防止过度依赖旧数据）
        self.weights *= (1 - decay_rate)
```

## 5. 使用示例

### 5.1 快速模式（日常使用）
```python
from backtest_optimizer import run_quick_optimization

# 快速获取Top 5推荐
results = run_quick_optimization(top_n=5)

# 查看结果
for stock in results['final_selection']['stocks']:
    print(f"{stock['code']} {stock['name']} - 仓位{stock['weight']*100:.1f}%")
```

### 5.2 完整模式（定期优化）
```python
from backtest_optimizer import OptimizationPipeline

pipeline = OptimizationPipeline()

results = pipeline.run_full_pipeline(
    screener_func=my_screener,
    backtest_start='2024-01-01',
    backtest_end='2025-01-01',
    optimize_weights=True,
    top_n_candidates=30,
    final_count=5
)

# 获取优化后的权重
optimized_weights = results['factor_optimization']['optimized_weights']

# 查看改进幅度
improvement = results['factor_optimization']['improvement']
print(f"相比默认权重提升: {improvement:+.1f}%")
```

### 5.3 市场环境自适应
```python
from backtest_optimizer import MarketRegimeAdapter

adapter = MarketRegimeAdapter()

# 检测当前市场状态
signal = adapter.detect_regime()
print(f"市场状态: {signal.regime.value}")
print(f"置信度: {signal.confidence}%")

# 获取对应策略配置
config = adapter.get_strategy_config()
print(f"建议仓位: {config.position_limit * 100}%")
print(f"止损线: {config.stop_loss_pct * 100}%")
```

## 6. 最佳实践

### 6.1 防止过拟合
- ✅ 使用时序交叉验证
- ✅ 样本外测试验证
- ✅ L2正则化
- ✅ 限制因子数量（<10个）
- ❌ 不要在全样本上优化

### 6.2 参数设置建议
```yaml
回测区间: 至少12个月
回测频率: 月度
验证集比例: 30%
正则化强度: 0.1
因子权重范围: [0.01, 0.5]
最终选股数: 5只
每板块上限: 2只
```

### 6.3 定期更新策略
- 每月：更新市场环境检测
- 每季：重新运行因子优化
- 每年：全面回顾算法有效性

## 7. 文件结构

```
research/short_mid_term_signal_selector/backtest_optimizer/
├── __init__.py                 # 模块导出
├── backtest_engine.py          # 回测引擎
├── factor_optimizer.py         # 因子优化器
├── market_regime_adapter.py    # 市场环境适配器
├── final_selector.py           # 最终选股器
└── run_optimization.py         # 运行脚本
```

## 8. 后续改进方向

1. **机器学习增强**: 使用XGBoost/LightGBM学习因子权重
2. **组合优化**: 引入均值-方差优化
3. **实时监控**: 对已持仓股票进行实时跟踪
4. **风险预警**: 建立风险预警机制
5. **多策略融合**: 支持多策略组合

---

*文档版本: v1.0*
*最后更新: 2026-01-05*
