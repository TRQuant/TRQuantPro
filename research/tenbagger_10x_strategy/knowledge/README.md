# 十倍股策略知识库索引

## 📚 知识库列表

### 核心知识库

| 文件 | 说明 | 主要内容 |
|------|------|----------|
| `long_term_holding_kb.py` | 长期持有策略 | 5大持有原则、历史案例、持有信号评估 |
| `batch_profit_taking_kb.py` | 分批止盈策略 | 5档阶梯止盈、市场/阶段调整规则 |
| `stage_transition_kb.py` | 阶段转换判断 | 6阶段生命周期、转换条件、预测器 |

### 市场环境知识库

| 文件 | 说明 |
|------|------|
| `astock_regime_knowledge_v2.py` | 10种A股市场环境识别 |
| `bear_market_exit_kb.py` | 熊市退出机制 |
| `mainline_rotation_kb.py` | 市场主线轮动 |

### 数据整合知识库

| 文件 | 说明 |
|------|------|
| `altdata_integration_kb.py` | 另类数据整合 |
| `ml_stage_predictor_kb.py` | ML阶段预测 |
| `tenbagger_identification_kb.py` | 十倍股识别 |

### 投资大师知识库

| 文件 | 说明 |
|------|------|
| `investment_master_kb.py` | 10位投资大师策略精华 |

---

## 🔧 使用方法

### 长期持有管理器

```python
from research.tenbagger_10x_strategy.knowledge.long_term_holding_kb import (
    LongTermHoldingManager, HoldingSignal
)

manager = LongTermHoldingManager()
signal, reason, msg = manager.evaluate_holding_signal(
    current_gain=0.35,
    max_gain=0.50,
    stage='S2_ACCELERATION',
    regime='VOLATILE',
    fundamentals={'profit_growth': 0.30, 'revenue_growth': 0.25, 'roe': 0.18}
)
print(f'信号: {signal.value}, 建议: {msg}')
```

### 分批止盈管理器

```python
from research.tenbagger_10x_strategy.knowledge.batch_profit_taking_kb import (
    BatchProfitManager
)

manager = BatchProfitManager()
should_sell, rule = manager.should_take_profit(
    gain=0.55,
    last_sell_threshold=0.30,
    regime='BULL',
    stage='S2_ACCELERATION'
)
if should_sell:
    print(f'建议卖出{rule.sell_ratio*100}%, 原因: {rule.reason}')
```

### 阶段转换预测器

```python
from research.tenbagger_10x_strategy.knowledge.stage_transition_kb import (
    StageTransitionPredictor, TenbaggerStage
)

predictor = StageTransitionPredictor()
stage, confidence = predictor.identify_current_stage(
    revenue_growth=0.35,
    profit_growth=0.45,
    market_cap=80,
    roe=0.15
)
print(f'当前阶段: {stage.value}, 置信度: {confidence:.2f}')
```

---

## 📊 策略版本

| 版本 | 状态 | 1年收益 | 夏普 | 说明 |
|------|------|---------|------|------|
| V9 | 基准 | -2.40% | -0.16 | 整合6个知识库 |
| V13 | **当前** | **+3.38%** | **1.24** | 跟踪止盈+高收益保护 |

---

*更新时间: 2024-12-27*







































