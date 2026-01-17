# TRQuant知识库V2使用指南

> **V2核心**: 从"资料仓库"升级为"决策智能系统"  
> **目标**: 服务于"研究 → 策略生成 → 实盘执行"的全链路自动化

---

## 🎯 V2核心改进

### 从"有没有知识、能不能搜到"
### 升级为"什么时候用、怎么用、自动怎么生成策略"

---

## 📚 V2新增知识域

### 1. 市场状态识别（Market Regime）

**回答的问题**: "什么时候用什么策略？"

**知识条目示例**:
- 情绪退潮判定标准
- 情绪过热判定标准
- 主升期判定标准

**使用方法**:
```python
from core.market_regime.regime_knowledge_base import RegimeKnowledgeBase

regime_kb = RegimeKnowledgeBase()

# 搜索特定市场状态的知识
knowledge = regime_kb.search_by_regime("退潮", limit=3)

# 获取策略建议
suggestions = regime_kb.get_regime_strategy_suggestions("退潮")
print(f"策略含义: {suggestions['strategy_implications']}")
```

---

### 2. 因子→行为映射（Factor → Behavior）

**回答的问题**: "这个因子反映了谁的行为？在什么阶段有效？"

**知识条目示例**:
- 主力资金净流入（money_flow_main）行为映射
- 成交量放大（volume_ratio）行为映射

**使用方法**:
```python
from mcp_servers.knowledge_search_api import search

# 搜索因子行为映射
result = search('主力资金 行为映射', type_filter='factor_behavior', limit=3)

for item in result.get('results', []):
    print(f"因子: {item['title']}")
    print(f"行为投影: {item['content']}")
```

---

### 3. 策略模板库（Strategy Pattern Library）

**回答的问题**: "在这种环境下，用什么结构的策略？"

**知识条目示例**:
- 情绪回暖 + 首板 → 次日冲高策略
- 高位连板 + 机构卖出 → 退潮空仓策略

**使用方法**:
```python
from mcp_servers.knowledge_search_api import search

# 搜索策略模板
result = search('首板 策略', type_filter='strategy_pattern', limit=3)

for item in result.get('results', []):
    print(f"策略模板: {item['title']}")
    print(f"适用场景: {item['content']}")
```

---

### 4. 失败案例/反例库（Failure Cases）

**回答的问题**: "为什么这个信号会失效？如何避免？"

**知识条目示例**:
- 游资榜单在退潮期的误导性
- 情绪指标在单边下跌中的反向误导

**使用方法**:
```python
from mcp_servers.knowledge_search_api import search

# 搜索失败案例
result = search('游资榜单 退潮期', type_filter='failure_case', limit=3)

for item in result.get('results', []):
    print(f"失败案例: {item['title']}")
    print(f"失败原因: {item['content']}")
```

---

## 🤖 V2新增工具

### 1. 市场情绪状态机

**功能**: 每天自动判断市场状态，限制策略生成空间

**使用方法**:
```python
from core.market_regime.state_machine import MarketRegimeStateMachine

sm = MarketRegimeStateMachine()

# 判断市场状态
indicators = {
    "limit_up_count": 8,          # 涨停家数
    "limit_down_count": 3,         # 跌停家数
    "limit_up_height": 2,          # 连板高度
    "limit_up_failure_rate": 0.35, # 炸板率
    "capital_net_inflow": -50,     # 资金净流入（亿）
    "turnover_rate": 1.2,          # 换手率
    "volume_ratio": 0.7            # 成交量比率
}

result = sm.update_regime(indicators)
print(f"市场状态: {result['regime']}")
print(f"最大仓位: {result['constraints']['max_position']}")
print(f"允许策略: {result['constraints']['allowed_strategies']}")
print(f"禁止策略: {result['constraints']['forbidden_strategies']}")

# 检查是否可以生成某类策略
can_generate, reason = sm.can_generate_strategy("追涨")
if not can_generate:
    print(f"❌ 禁止生成: {reason}")
```

**状态定义**:
- **冷启动**: 市场刚启动，情绪较低
- **主升**: 市场主升期，情绪健康
- **过热**: 市场过热，情绪极度亢奋
- **退潮**: 市场退潮，情绪下降
- **崩溃**: 市场崩溃，情绪极度恐慌

---

### 2. 因子评估引擎

**功能**: 自动化IC/IR/衰减分析，结果写回知识库

**使用方法**:
```python
from core.factor_evaluation.factor_evaluator import FactorEvaluator
import pandas as pd

evaluator = FactorEvaluator()

# 准备数据
factor_values = pd.Series([...])  # 因子值
returns = pd.Series([...])        # 收益率
regime_labels = pd.Series([...])  # 市场状态标签（可选）

# 评估因子
result = evaluator.evaluate_factor(
    factor_name="money_flow_main",
    factor_values=factor_values,
    returns=returns,
    regime_labels=regime_labels
)

if result['success']:
    print(f"IC均值: {result['ic_stats']['ic_mean']:.4f}")
    print(f"IR: {result['ic_stats']['ir']:.4f}")
    print(f"按状态IC: {result['ic_by_regime']}")
    print(f"知识库ID: {result['knowledge_id']}")
```

---

### 3. 策略生成Prompt模板

**功能**: 固定几类Prompt，而非自由对话

**使用方法**:
```python
from core.strategy_generation.prompts import generate_strategy_prompt

# 生成短线策略Prompt
prompt = generate_strategy_prompt(
    market_regime="退潮期",
    available_factors=["money_flow_main", "volume_ratio", "limit_up_count"],
    strategy_type="short_term",
    sentiment_indicators="涨停家数: 8, 炸板率: 35%",
    capital_flow="资金净流出: -50亿"
)

print(prompt)

# 生成风控策略Prompt
prompt = generate_strategy_prompt(
    market_regime="过热期",
    available_factors=["limit_up_count", "limit_up_height"],
    strategy_type="risk_control",
    risk_signals="涨停家数异常高: 95只",
    risk_indicators="市场情绪极度亢奋"
)
```

**模板类型**:
- `short_term`: 短线策略生成模板
- `trend`: 趋势策略生成模板
- `risk_control`: 风控/减仓模板
- `sentiment_cycle`: 情绪周期策略模板

---

## 🔄 完整工作流程示例

### 场景: 自动生成策略

```python
from core.market_regime.state_machine import MarketRegimeStateMachine
from core.strategy_generation.prompts import generate_strategy_prompt
from mcp_servers.knowledge_search_api import search

# 1. 判断市场状态
sm = MarketRegimeStateMachine()
indicators = get_today_indicators()  # 获取今日市场指标
regime_result = sm.update_regime(indicators)
market_regime = regime_result['regime']
constraints = regime_result['constraints']

print(f"当前市场状态: {market_regime}")
print(f"最大仓位: {constraints['max_position']}")

# 2. 检查策略类型是否允许
strategy_type = "短线策略"
can_generate, reason = sm.can_generate_strategy(strategy_type)
if not can_generate:
    print(f"❌ 禁止生成: {reason}")
    exit()

# 3. 搜索可用因子
factor_result = search('资金流向 因子', type_filter='factor_behavior', limit=5)
available_factors = [item['title'] for item in factor_result.get('results', [])]

# 4. 搜索策略模板
pattern_result = search(f'{market_regime} 策略', type_filter='strategy_pattern', limit=3)
strategy_patterns = pattern_result.get('results', [])

# 5. 搜索失败案例（避免错误）
failure_result = search(f'{market_regime} 失败', type_filter='failure_case', limit=3)
failure_cases = failure_result.get('results', [])

# 6. 生成策略Prompt
prompt = generate_strategy_prompt(
    market_regime=market_regime,
    available_factors=available_factors,
    strategy_type="short_term",
    sentiment_indicators=f"涨停家数: {indicators['limit_up_count']}, 炸板率: {indicators['limit_up_failure_rate']*100:.1f}%",
    capital_flow=f"资金净流入: {indicators['capital_net_inflow']}亿"
)

# 7. 使用Prompt生成策略（调用LLM）
strategy_code = generate_strategy_with_llm(prompt)

print("✅ 策略生成完成！")
```

---

## 📊 V2知识库统计

### 当前V2知识条目

| 知识域 | 条目数 | 状态 |
|--------|--------|------|
| 市场状态识别 | 3 | ✅ 已创建 |
| 因子行为映射 | 2 | ✅ 已创建 |
| 策略模板 | 2 | ✅ 已创建 |
| 失败案例 | 2 | ✅ 已创建 |
| **总计** | **9** | **✅ 基础完成** |

### 下一步补充计划

#### 市场状态识别（目标: 20+条）
- [ ] 冷启动期判定标准
- [ ] 崩溃期判定标准
- [ ] 各状态转换信号
- [ ] 状态持续时间统计

#### 因子行为映射（目标: 50+条）
- [ ] PSY心理线行为映射
- [ ] ARBR人气意愿指标行为映射
- [ ] VR成交量变异率行为映射
- [ ] 龙虎榜数据行为映射
- [ ] 涨停板数据行为映射

#### 策略模板（目标: 30+条）
- [ ] 趋势跟随策略模板
- [ ] 板块轮动策略模板
- [ ] 情绪周期策略模板
- [ ] 资金流向策略模板

#### 失败案例（目标: 20+条）
- [ ] 高换手率在不同阶段的含义
- [ ] 涨停板在不同情绪周期的可靠性
- [ ] 资金流入但指数不涨的原因
- [ ] 更多实战失败案例

---

## 🎯 使用建议

### 1. 策略开发流程

```
市场状态判断 → 可用策略模板 → 因子选择 → 失败案例检查 → 策略生成
```

### 2. 知识库搜索优先级

1. **先判断市场状态** - 使用市场状态机
2. **再搜索策略模板** - 按市场状态搜索
3. **选择有效因子** - 按市场状态筛选因子
4. **检查失败案例** - 避免已知错误

### 3. 策略生成约束

- **退潮期**: 禁止追涨、连板策略
- **过热期**: 禁止追涨、高位接盘
- **崩溃期**: 只允许防御性策略

---

## 📝 相关文件

- V2改进方案: `docs/knowledge_base/KB_V2_IMPROVEMENT_PLAN.md`
- V2使用指南: `docs/knowledge_base/KB_V2_USAGE_GUIDE.md` (本文档)
- V2迁移脚本: `scripts/kb/migrate_to_v2.py`
- V2测试脚本: `scripts/kb/test_v2_kb_usage.py`
- 市场状态知识库: `core/market_regime/regime_knowledge_base.py`
- 市场状态机: `core/market_regime/state_machine.py`
- 因子评估引擎: `core/factor_evaluation/factor_evaluator.py`
- 策略Prompt模板: `core/strategy_generation/prompts.py`

---

**V2知识库系统已就绪，开始从"资料仓库"向"决策智能系统"升级！**
