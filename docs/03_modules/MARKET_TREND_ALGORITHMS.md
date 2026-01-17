# 市场趋势判断算法汇总

> **文档版本**: v1.0  
> **最后更新**: 2025-01-01  
> **说明**: 本文档汇总了TRQuant项目中已实现的所有市场趋势判断算法

---

## 📊 算法总览

项目中已实现 **5种** 市场趋势判断算法，覆盖从技术分析到机器学习的多种方法：

| 算法名称 | 文件路径 | 特点 | 适用场景 |
|---------|---------|------|---------|
| **TrendAnalyzer** | `core/trend_analyzer.py` | 多周期技术指标融合 | 综合趋势分析 |
| **MarketRegimeDetector** | `core/market_regime/market_regime_detector.py` | 多维度综合评分 | 市场环境判断 |
| **IBDStyleAnalyzer** | `core/ibd_style_analyzer.py` | IBD跟踪日/分布日 | 反转点识别 |
| **TrendClassifier (HMM)** | `core/trend_ml.py` | 隐马尔可夫模型 | 状态概率预测 |
| **简化趋势分析** | `Projects/PTrade主线因子策略/main_v2.5.py` | 均线+成交量+波动率 | 实盘策略集成 |

---

## 1️⃣ TrendAnalyzer - 多周期趋势分析引擎

### 📍 位置
`core/trend_analyzer.py`

### 🎯 核心算法

#### 1.1 多周期分析
```python
PERIOD_CONFIG = {
    TrendPeriod.SHORT: {
        "days": 40,      # 短期趋势(1-8周)
        "ma_fast": 5,
        "ma_slow": 20,
        "weight": 0.2,   # 权重20%
    },
    TrendPeriod.MEDIUM: {
        "days": 120,     # 中期趋势(9-24周)
        "ma_fast": 20,
        "ma_slow": 60,
        "weight": 0.3,   # 权重30%
    },
    TrendPeriod.LONG: {
        "days": 240,     # 长期趋势(25-48周)
        "ma_fast": 60,
        "ma_slow": 250,
        "weight": 0.5,   # 权重50%
    },
}
```

#### 1.2 8维度技术指标体系

| 指标 | 权重 | 说明 |
|------|------|------|
| **均线系统** (MA) | 20% | 多周期均线排列、价格相对均线位置 |
| **MACD** | 18% | 动能指标、金叉死叉信号 |
| **RSI** | 10% | 超买超卖指标 |
| **布林带** (BB) | 10% | 价格波动区间、突破信号 |
| **成交量趋势** (VOL) | 12% | 量价关系、放量缩量 |
| **KDJ** | 10% | 随机指标、超买超卖 |
| **ADX** | 10% | 趋势强度指标 |
| **资金流向** (FLOW) | 10% | 北向资金、主力资金 |

#### 1.3 市场阶段判断

基于多周期共振分析，判断市场阶段：

- **牛市确认(全周期共振)**: 短中长期全部看涨
- **牛市确认**: 长期看涨 + 中期看涨
- **牛市震荡**: 长期看涨但中期不确定
- **牛市短期调整**: 长期看涨但短期下跌
- **熊市确认(全周期共振)**: 短中长期全部看跌
- **熊市确认**: 长期看跌 + 中期看跌
- **熊市反弹**: 长期看跌但中期上涨
- **突破在即**: 震荡中全周期转多
- **破位风险**: 震荡中全周期转空
- **复苏初期**: 短期转强，中期跟随
- **见顶回落**: 短期转弱，中期跟随
- **窄幅震荡**: 各周期均无明显趋势
- **宽幅震荡**: 短期波动大，中期方向不明

### 💻 使用示例

```python
from core.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer(jq_client=jq_client)
result = analyzer.analyze_market(index_code="000001.XSHG")

print(f"市场阶段: {result.market_phase}")
print(f"综合得分: {result.composite_score}")
print(f"短期趋势: {result.short_term.score}")
print(f"中期趋势: {result.medium_term.score}")
print(f"长期趋势: {result.long_term.score}")
```

---

## 2️⃣ MarketRegimeDetector - 市场环境检测器

### 📍 位置
`core/market_regime/market_regime_detector.py`

### 🎯 核心算法

#### 2.1 四维度综合评分体系

| 维度 | 权重 | 指标组成 |
|------|------|---------|
| **宏观层面** | 15% | PMI、M2增速、利率 |
| **市场层面** | 35% | 指数趋势、成交量、涨跌比、均线系统 |
| **情绪层面** | 20% | 换手率、新高新低比、融资余额 |
| **技术层面** | 30% | 均线系统、动量指标、波动率 |

#### 2.2 市场环境分类

```python
class MarketRegime(Enum):
    BULL = "BULL"              # 牛市
    BEAR = "BEAR"              # 熊市
    VOLATILE = "VOLATILE"      # 震荡市
    RECOVERY = "RECOVERY"      # 复苏期（熊转牛）
    DISTRIBUTION = "DISTRIBUTION"  # 派发期（牛转熊）
```

#### 2.3 评分计算方法

**宏观得分** (-100 to 100):
- PMI贡献: `(PMI - 50) * 3` (50为中性)
- M2增速贡献: `M2_growth * 2`
- 利率贡献: `-interest_rate * 5` (利率下降利好)

**市场得分** (-100 to 100):
- 均线排列: 多头排列 +20, 空头排列 -20
- 指数位置: `(index_position - 0.5) * 60`
- 成交量: 放量(>1.5倍) +10, 缩量(<0.7倍) -10
- 涨跌比: `(advance_decline - 0.5) * 40`

**综合得分** = `macro_score * 0.15 + market_score * 0.35 + sentiment_score * 0.20 + technical_score * 0.30`

### 💻 使用示例

```python
from core.market_regime.market_regime_detector import MarketRegimeDetector, get_market_regime_detector

detector = get_market_regime_detector()
result = detector.detect_regime(date="2025-01-01")

print(f"市场环境: {result.regime.value}")
print(f"置信度: {result.confidence}")
print(f"综合得分: {result.score}")
print(f"策略建议: {result.strategy_advice}")
```

---

## 3️⃣ IBDStyleAnalyzer - IBD风格市场分析器

### 📍 位置
`core/ibd_style_analyzer.py`

### 🎯 核心算法

#### 3.1 IBD分析方法

参考 **Investor's Business Daily (IBD)** 的市场分析方法：

1. **跟踪日 (Follow-Through Day)**: 底部反转确认
   - 涨幅 > 1.2%
   - 成交量 > 平均成交量
   - 在低点后至少第4天

2. **分布日 (Distribution Day)**: 机构抛售信号
   - 跌幅 > 0.2%
   - 成交量 > 平均成交量
   - 25日内有效
   - 超过5个分布日视为承压

3. **市场状态判断**:
   - `CONFIRMED_UPTREND`: 确认上涨
   - `UPTREND_UNDER_PRESSURE`: 上涨承压
   - `MARKET_IN_CORRECTION`: 市场调整
   - `RALLY_ATTEMPT`: 反弹尝试

#### 3.2 技术指标

- 价格相对50日均线位置
- 价格相对200日均线位置
- 50日均线相对200日均线位置
- 市场宽度: 在50日均线上方的股票比例
- 新高新低数量

### 💻 使用示例

```python
from core.ibd_style_analyzer import IBDStyleAnalyzer

analyzer = IBDStyleAnalyzer()
result = analyzer.analyze(index_code="000001.XSHG")

print(f"市场状态: {result.market_status.value}")
print(f"分布日数量: {result.distribution_count}")
print(f"跟踪日数量: {len(result.follow_through_days)}")
print(f"交易建议: {result.recommendation}")
```

---

## 4️⃣ TrendClassifier (HMM) - 机器学习趋势分类

### 📍 位置
`core/trend_ml.py`

### 🎯 核心算法

#### 4.1 隐马尔可夫模型 (HMM)

使用HMM识别市场的三种隐藏状态：
- **BULL**: 牛市
- **BEAR**: 熊市
- **SIDEWAYS**: 震荡

#### 4.2 观测变量

- **价格变化率**: 日收益率
- **成交量变化率**: 成交量变化百分比
- **波动率**: 20日滚动标准差 * √252

#### 4.3 状态转移矩阵

```python
TRANSITION_MATRIX = [
    [0.85, 0.05, 0.10],  # Bull -> Bull/Bear/Sideways
    [0.05, 0.80, 0.15],  # Bear -> Bull/Bear/Sideways
    [0.20, 0.20, 0.60],  # Sideways -> Bull/Bear/Sideways
]
```

#### 4.4 规则分类器 (TrendClassifier)

基于技术指标的规则分类，无需训练：

| 特征 | 权重 | 说明 |
|------|------|------|
| 均线交叉 | 20% | 多周期均线排列 |
| MACD信号 | 18% | MACD金叉死叉 |
| RSI水平 | 12% | 超买超卖 |
| 价格位置 | 15% | 相对60日均线 |
| 成交量趋势 | 12% | 量价关系 |
| 波动率 | 10% | 市场波动水平 |
| 动量 | 13% | 价格动量 |

### 💻 使用示例

```python
from core.trend_ml import SimpleHMM, TrendClassifier

# 方法1: HMM模型
hmm = SimpleHMM()
hmm_result = hmm.analyze(df)
print(f"当前状态: {hmm_result.current_state.value}")
print(f"状态概率: {hmm_result.state_probability}")

# 方法2: 规则分类器
classifier = TrendClassifier()
classify_result = classifier.classify(df)
print(f"趋势类别: {classify_result['trend_class']}")
print(f"置信度: {classify_result['confidence']}")
```

---

## 5️⃣ 简化趋势分析 (PTrade策略版)

### 📍 位置
`Projects/PTrade主线因子策略/main_v2.5.py`

### 🎯 核心算法

#### 5.1 简化指标体系

- **均线系统**: MA5, MA20, MA60
- **成交量**: 量价关系
- **波动率**: 20日滚动标准差

#### 5.2 评分规则

```python
score = 0

# 价格相对MA20
if current_price > ma20: score += 20
elif current_price < ma20: score -= 20

# MA20相对MA60
if ma20 > ma60: score += 30
elif ma20 < ma60: score -= 30

# 价格相对MA60位置
if current_price > ma60 * 1.05: score += 30
elif current_price < ma60 * 0.95: score -= 30

# 成交量
if volume_ratio > 1.2: score += 10
elif volume_ratio < 0.8: score -= 10

# 波动率
if volatility < 0.15: score += 5
elif volatility > 0.30: score -= 5
```

#### 5.3 市场阶段分类

- `bull`: score >= 60
- `weak_bull`: score >= 30
- `neutral`: -30 <= score < 30
- `weak_bear`: -60 <= score < -30
- `bear`: score < -60

### 💻 使用示例

```python
def analyze_market_trend_v2(context, date_str):
    result = analyze_market_trend_v2(context, date_str)
    print(f"市场阶段: {result['market_phase']}")
    print(f"综合得分: {result['composite_score']}")
```

---

## 🔄 算法对比与选择建议

| 算法 | 复杂度 | 实时性 | 准确性 | 适用场景 |
|------|--------|--------|--------|---------|
| **TrendAnalyzer** | 高 | 中 | 高 | 综合趋势分析，多周期判断 |
| **MarketRegimeDetector** | 高 | 中 | 高 | 市场环境判断，策略切换 |
| **IBDStyleAnalyzer** | 中 | 高 | 中 | 反转点识别，精准入场 |
| **TrendClassifier (HMM)** | 中 | 高 | 中 | 状态概率预测，风险控制 |
| **简化趋势分析** | 低 | 高 | 中 | 实盘策略，快速判断 |

### 💡 推荐组合使用

1. **日常监控**: `TrendAnalyzer` + `MarketRegimeDetector`
2. **策略切换**: `MarketRegimeDetector` (判断环境) → `TrendAnalyzer` (确认趋势)
3. **精准入场**: `IBDStyleAnalyzer` (跟踪日确认)
4. **风险控制**: `TrendClassifier` (状态概率预警)
5. **实盘策略**: 简化趋势分析 (快速执行)

---

## 📚 相关文档

- [研究-实战工作流文档](./RESEARCH_LIVE_WORKFLOW.md)
- [主线识别算法](./docs/主线识别算法.md)
- [因子权重调整](./docs/因子权重调整.md)

---

## 🔧 集成到Notebook

所有算法都可以在Jupyter Notebook中使用：

```python
import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from core.trend_analyzer import TrendAnalyzer
from core.market_regime.market_regime_detector import get_market_regime_detector
from core.ibd_style_analyzer import IBDStyleAnalyzer

# 使用TrendAnalyzer
analyzer = TrendAnalyzer()
result = analyzer.analyze_market("000001.XSHG")
print(result.market_phase)
```

---

*文档维护者: TRQuant开发团队*  
*最后更新: 2025-01-01*

