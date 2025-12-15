---
title: "3.2 市场状态"
description: "深入解析市场状态判断机制，包括市场状态分类、多维度判断、状态评分和AI辅助识别"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 🎯 3.2 市场状态

> **核心摘要：**
> 
> 本节系统介绍TRQuant系统的市场状态判断功能，包括市场状态分类体系、多维度判断机制、状态评分方法和AI辅助识别。通过理解risk_on（牛市/风险偏好）、risk_off（熊市/风险规避）、neutral（震荡市）三种状态的判断逻辑，掌握价格指标、成交量指标、情绪指标、技术指标的综合判断方法，以及状态强度、持续性、可靠性的评分机制，帮助开发者构建准确的市场状态判断系统。

## 📋 章节概览

<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}
</script>

<div class="section-overview">
  <div class="section-item" onclick="scrollToSection('section-3-2-1')">
    <h4>📊 3.2.1 市场状态分类</h4>
    <p>risk_on、risk_off、neutral三种状态的分类标准</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-3-2-2')">
    <h4>🔍 3.2.2 多维度判断</h4>
    <p>价格指标、成交量指标、情绪指标、技术指标的综合判断</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-3-2-3')">
    <h4>📈 3.2.3 状态评分</h4>
    <p>状态强度、持续性、可靠性的多维度评分</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-3-2-4')">
    <h4>🤖 3.2.4 AI辅助识别</h4>
    <p>AI市场状态识别、智能状态预测、多模型融合</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-3-2-5')">
    <h4>🔄 3.2.5 自动化实现</h4>
    <p>定时判断、自动更新、状态告警机制</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-3-2-6')">
    <h4>🛠️ 3.2.6 MCP工具使用</h4>
    <p>使用trquant_market_status获取市场状态、使用MCP工具查询相关文档</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解状态分类**：掌握risk_on、risk_off、neutral三种状态的分类标准和特征
- **掌握多维度判断**：理解价格、成交量、情绪、技术等多维度指标的综合判断方法
- **熟悉状态评分**：理解状态强度、持续性、可靠性的评分计算和权重设置
- **了解AI辅助**：掌握AI技术在市场状态识别和预测中的应用
- **实现自动化**：理解定时判断、自动更新、状态告警的实现机制
- **使用MCP工具**：掌握使用trquant_market_status等MCP工具获取市场状态

<h2 id="section-3-2-1">📊 3.2.1 市场状态分类</h2>

市场状态分类是市场状态判断的基础，将市场状态分为三类：risk_on（牛市/风险偏好）、risk_off（熊市/风险规避）、neutral（震荡市）。

### 设计原则

<div class="key-points">
  <div class="key-point">
    <h4>🎯 明确分类</h4>
    <p>三种状态定义清晰，避免模糊判断</p>
  </div>
  <div class="key-point">
    <h4>📊 多维度综合</h4>
    <p>综合考虑价格、成交量、情绪、技术等多个维度</p>
  </div>
  <div class="key-point">
    <h4>⚡ 实时更新</h4>
    <p>市场状态实时更新，及时反映市场变化</p>
  </div>
  <div class="key-point">
    <h4>🔧 可配置参数</h4>
    <p>判断阈值和权重可配置，适应不同市场环境</p>
  </div>
</div>

### 状态定义

#### Risk_On（牛市/风险偏好）

Risk_On状态表示市场处于牛市或风险偏好阶段，特征包括：

- **价格特征**：指数持续上涨，涨幅较大
- **成交量特征**：成交量放大，资金流入明显
- **情绪特征**：投资者情绪乐观，风险偏好上升
- **技术特征**：技术指标强势，突破关键阻力位

```python
from enum import Enum
from typing import Dict, Any
import pandas as pd
import numpy as np

class MarketRegime(Enum):
    """市场状态枚举"""
    RISK_ON = "risk_on"      # 牛市/风险偏好
    RISK_OFF = "risk_off"     # 熊市/风险规避
    NEUTRAL = "neutral"       # 震荡市

def classify_risk_on(data: pd.DataFrame, 
                    lookback_days: int = 20) -> bool:
    """
    判断是否为risk_on状态
    
    Args:
        data: 市场数据（指数数据）
        lookback_days: 回看天数
    
    Returns:
        是否为risk_on状态
    """
    if len(data) < lookback_days:
        return False
    
    recent_data = data.tail(lookback_days)
    
    # 条件1：价格涨幅 > 5%
    price_change = (recent_data['close'].iloc[-1] - recent_data['close'].iloc[0]) / \
                   recent_data['close'].iloc[0]
    condition1 = price_change > 0.05
    
    # 条件2：成交量放大（平均成交量 > 前20日均值的1.2倍）
    avg_volume = recent_data['volume'].mean()
    prev_avg_volume = data['volume'].iloc[:-lookback_days].tail(20).mean()
    condition2 = avg_volume > prev_avg_volume * 1.2
    
    # 条件3：技术指标强势（RSI > 60）
    from core.market_analysis.trend_analysis import calculate_rsi
    rsi = calculate_rsi(data, period=14)
    condition3 = rsi.iloc[-1] > 60
    
    # 条件4：移动平均线多头排列
    from core.market_analysis.trend_analysis import calculate_sma
    sma_5 = calculate_sma(data, period=5)
    sma_20 = calculate_sma(data, period=20)
    condition4 = sma_5.iloc[-1] > sma_20.iloc[-1]
    
    # 综合判断：至少满足3个条件
    return sum([condition1, condition2, condition3, condition4]) >= 3
```

#### Risk_Off（熊市/风险规避）

Risk_Off状态表示市场处于熊市或风险规避阶段，特征包括：

- **价格特征**：指数持续下跌，跌幅较大
- **成交量特征**：成交量萎缩，资金流出明显
- **情绪特征**：投资者情绪悲观，风险规避上升
- **技术特征**：技术指标弱势，跌破关键支撑位

```python
def classify_risk_off(data: pd.DataFrame, 
                     lookback_days: int = 20) -> bool:
    """
    判断是否为risk_off状态
    
    Args:
        data: 市场数据（指数数据）
        lookback_days: 回看天数
    
    Returns:
        是否为risk_off状态
    """
    if len(data) < lookback_days:
        return False
    
    recent_data = data.tail(lookback_days)
    
    # 条件1：价格跌幅 > 5%
    price_change = (recent_data['close'].iloc[-1] - recent_data['close'].iloc[0]) / \
                   recent_data['close'].iloc[0]
    condition1 = price_change < -0.05
    
    # 条件2：成交量萎缩（平均成交量 < 前20日均值的0.8倍）
    avg_volume = recent_data['volume'].mean()
    prev_avg_volume = data['volume'].iloc[:-lookback_days].tail(20).mean()
    condition2 = avg_volume < prev_avg_volume * 0.8
    
    # 条件3：技术指标弱势（RSI < 40）
    from core.market_analysis.trend_analysis import calculate_rsi
    rsi = calculate_rsi(data, period=14)
    condition3 = rsi.iloc[-1] < 40
    
    # 条件4：移动平均线空头排列
    from core.market_analysis.trend_analysis import calculate_sma
    sma_5 = calculate_sma(data, period=5)
    sma_20 = calculate_sma(data, period=20)
    condition4 = sma_5.iloc[-1] < sma_20.iloc[-1]
    
    # 设计原理：综合判断采用多数投票机制
    # 原因：单一指标可能误判，多个指标综合判断更准确
    # 实现方式：至少满足3个条件（4个条件中的3个），提高判断准确性
    # 为什么这样设计：避免单一指标的偶然性，提高判断的鲁棒性
    return sum([condition1, condition2, condition3, condition4]) >= 3
```

#### Neutral（震荡市）

Neutral状态表示市场处于震荡市，无明显趋势，特征包括：

- **价格特征**：价格在一定区间内震荡，涨跌幅较小
- **成交量特征**：成交量平稳，无明显放大或萎缩
- **情绪特征**：投资者情绪中性，观望情绪浓厚
- **技术特征**：技术指标中性，无明显方向性

```python
def classify_neutral(data: pd.DataFrame, 
                    lookback_days: int = 20) -> bool:
    """
    判断是否为neutral状态
    
    Args:
        data: 市场数据（指数数据）
        lookback_days: 回看天数
    
    Returns:
        是否为neutral状态
    """
    if len(data) < lookback_days:
        return False
    
    recent_data = data.tail(lookback_days)
    
    # 条件1：价格波动 < 3%
    price_change = abs((recent_data['close'].iloc[-1] - recent_data['close'].iloc[0]) / \
                      recent_data['close'].iloc[0])
    condition1 = price_change < 0.03
    
    # 条件2：成交量平稳（平均成交量在前后均值的0.9-1.1倍之间）
    avg_volume = recent_data['volume'].mean()
    prev_avg_volume = data['volume'].iloc[:-lookback_days].tail(20).mean()
    volume_ratio = avg_volume / prev_avg_volume
    condition2 = 0.9 <= volume_ratio <= 1.1
    
    # 条件3：技术指标中性（40 < RSI < 60）
    from core.market_analysis.trend_analysis import calculate_rsi
    rsi = calculate_rsi(data, period=14)
    condition3 = 40 < rsi.iloc[-1] < 60
    
    # 条件4：移动平均线纠缠
    from core.market_analysis.trend_analysis import calculate_sma
    sma_5 = calculate_sma(data, period=5)
    sma_20 = calculate_sma(data, period=20)
    ma_diff = abs(sma_5.iloc[-1] - sma_20.iloc[-1]) / sma_20.iloc[-1]
    condition4 = ma_diff < 0.02
    
    # 综合判断：至少满足3个条件
    return sum([condition1, condition2, condition3, condition4]) >= 3
```

<h2 id="section-3-2-2">🔍 3.2.2 多维度判断</h2>

市场状态判断需要综合考虑多个维度，包括价格指标、成交量指标、情绪指标、技术指标等。

### 价格指标

价格指标反映市场的基本走势：

<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
def analyze_price_dimension(data: pd.DataFrame) -> Dict[str, float]:
    """
    分析价格维度
    
    **设计原理**：
    - **多周期分析**：同时分析1日、5日、20日涨跌幅，提供不同时间尺度的价格变化
    - **相对位置**：计算价格在近期高低点之间的相对位置，反映价格水平
    - **趋势强度**：通过移动平均线斜率判断价格趋势，反映趋势强度
    
    **为什么这样设计**：
    1. **全面性**：多周期分析提供全面的价格变化信息
    2. **相对性**：相对位置比绝对价格更有意义，便于不同时期对比
    3. **趋势性**：趋势强度反映价格变化的方向和速度
    
    **使用场景**：
    - 市场状态判断时，分析价格维度
    - 策略生成时，根据价格维度选择策略类型
    - 风险控制时，根据价格位置调整仓位
    
    Args:
        data: 市场数据
    
    Returns:
        价格维度评分字典
    """
    # 设计原理：多周期涨跌幅计算
    # 原因：不同周期的涨跌幅反映不同时间尺度的价格变化
    # 1日：短期波动，反映当日市场情绪
    # 5日：中期变化，反映一周市场走势
    # 20日：长期趋势，反映一个月市场方向
    price_change_1d = (data['close'].iloc[-1] - data['close'].iloc[-2]) / data['close'].iloc[-2]
    price_change_5d = (data['close'].iloc[-1] - data['close'].iloc[-6]) / data['close'].iloc[-6]
    price_change_20d = (data['close'].iloc[-1] - data['close'].iloc[-21]) / data['close'].iloc[-21]
    
    # 设计原理：价格相对位置计算
    # 原因：相对位置比绝对价格更有意义，反映价格在近期区间的位置
    # 公式：位置 = (当前价格 - 最低价) / (最高价 - 最低价)
    # 取值范围：0-1，0表示最低点，1表示最高点
    # 为什么这样设计：便于判断价格是否处于高位或低位，指导交易决策
    recent_high = data['high'].tail(20).max()
    recent_low = data['low'].tail(20).min()
    price_position = (data['close'].iloc[-1] - recent_low) / (recent_high - recent_low)
    
    # 设计原理：价格趋势强度计算
    # 原因：移动平均线斜率反映价格趋势的方向和强度
    # 公式：趋势 = (当前MA - 5日前MA) / 5日前MA
    # 正值表示上升趋势，负值表示下降趋势，绝对值表示趋势强度
    # 为什么这样设计：趋势强度比趋势方向更有价值，强趋势更可靠
    from core.market_analysis.trend_analysis import calculate_sma
    sma_20 = calculate_sma(data, period=20)
    price_trend = (sma_20.iloc[-1] - sma_20.iloc[-5]) / sma_20.iloc[-5]
    
    return {
        'price_change_1d': price_change_1d,
        'price_change_5d': price_change_5d,
        'price_change_20d': price_change_20d,
        'price_position': price_position,
        'price_trend': price_trend
    }
```
-->

### 成交量指标

成交量指标反映市场资金流向：

<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_volume_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

### 情绪指标

情绪指标反映市场投资者情绪：

<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_sentiment_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
def analyze_sentiment_dimension(data: pd.DataFrame) -> Dict[str, float]:
    """
    分析情绪维度（需要额外的情绪数据源）
    
    Args:
        data: 市场数据
    
    Returns:
        情绪维度评分字典
    """
    # 1. 涨跌停板数量（需要额外数据源）
    # limit_up_count: 涨停板数量
    # limit_down_count: 跌停板数量
    # sentiment_score = (limit_up_count - limit_down_count) / (limit_up_count + limit_down_count + 1)
    
    # 2. 融资融券余额变化（需要额外数据源）
    # margin_balance_change: 融资余额变化率
    
    # 3. 北向资金流向（需要额外数据源）
    # northbound_flow: 北向资金净流入
    
    # 简化版本：使用价格波动率作为情绪代理指标
    volatility = data['close'].pct_change().tail(20).std()
    
    return {
        'volatility': volatility,
        # 'sentiment_score': sentiment_score,
        # 'margin_balance_change': margin_balance_change,
        # 'northbound_flow': northbound_flow
    }
```

### 技术指标

技术指标反映市场的技术形态：

<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_technical_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
def analyze_technical_dimension(data: pd.DataFrame) -> Dict[str, float]:
    """
    分析技术维度
    
    Args:
        data: 市场数据
    
    Returns:
        技术维度评分字典
    """
    from core.market_analysis.trend_analysis import (
        calculate_sma, calculate_ema, calculate_macd, 
        calculate_rsi, calculate_bollinger_bands
    )
    
    # 1. 移动平均线排列
    sma_5 = calculate_sma(data, period=5)
    sma_20 = calculate_sma(data, period=20)
    sma_60 = calculate_sma(data, period=60)
    
    ma_alignment = 0.0
    if sma_5.iloc[-1] > sma_20.iloc[-1] > sma_60.iloc[-1]:
        ma_alignment = 1.0  # 多头排列
    elif sma_5.iloc[-1] < sma_20.iloc[-1] < sma_60.iloc[-1]:
        ma_alignment = -1.0  # 空头排列
    
    # 2. MACD指标
    macd_data = calculate_macd(data)
    macd_signal = 1.0 if macd_data['DIF'].iloc[-1] > macd_data['DEA'].iloc[-1] else -1.0
    
    # 3. RSI指标
    rsi = calculate_rsi(data, period=14)
    rsi_score = (rsi.iloc[-1] - 50) / 50  # 归一化到-1到1
    
    # 4. 布林带位置
    bb = calculate_bollinger_bands(data)
    bb_position = (data['close'].iloc[-1] - bb['middle'].iloc[-1]) / \
                  (bb['upper'].iloc[-1] - bb['lower'].iloc[-1])
    
    return {
        'ma_alignment': ma_alignment,
        'macd_signal': macd_signal,
        'rsi_score': rsi_score,
        'bb_position': bb_position
    }
```
-->

### 综合判断

综合多个维度的指标，判断市场状态：

```python
class MarketStatusAnalyzer:
    """市场状态分析器"""
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        初始化分析器
        
        Args:
            weights: 各维度权重，默认均等权重
        """
        if weights is None:
            self.weights = {
                'price': 0.3,
                'volume': 0.2,
                'sentiment': 0.2,
                'technical': 0.3
            }
        else:
            self.weights = weights
    
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        综合分析市场状态
        
        Args:
            data: 市场数据
        
        Returns:
            市场状态分析结果
        """
        # 分析各维度
        price_scores = analyze_price_dimension(data)
        volume_scores = analyze_volume_dimension(data)
        sentiment_scores = analyze_sentiment_dimension(data)
        technical_scores = analyze_technical_dimension(data)
        
        # 计算各维度得分（归一化到0-1）
        price_score = self._normalize_price_score(price_scores)
        volume_score = self._normalize_volume_score(volume_scores)
        sentiment_score = self._normalize_sentiment_score(sentiment_scores)
        technical_score = self._normalize_technical_score(technical_scores)
        
        # 加权综合得分
        total_score = (
            price_score * self.weights['price'] +
            volume_score * self.weights['volume'] +
            sentiment_score * self.weights['sentiment'] +
            technical_score * self.weights['technical']
        )
        
        # 判断市场状态
        if total_score > 0.6:
            regime = MarketRegime.RISK_ON
        elif total_score < 0.4:
            regime = MarketRegime.RISK_OFF
        else:
            regime = MarketRegime.NEUTRAL
        
        return {
            'regime': regime.value,
            'total_score': total_score,
            'dimension_scores': {
                'price': price_score,
                'volume': volume_score,
                'sentiment': sentiment_score,
                'technical': technical_score
            },
            'raw_scores': {
                'price': price_scores,
                'volume': volume_scores,
                'sentiment': sentiment_scores,
                'technical': technical_scores
            }
        }
    
    def _normalize_price_score(self, scores: Dict[str, float]) -> float:
        """归一化价格得分"""
        # 综合涨跌幅、价格位置、价格趋势
        score = (
            scores['price_change_20d'] * 0.4 +
            scores['price_position'] * 0.3 +
            scores['price_trend'] * 0.3
        )
        return max(0, min(1, (score + 0.1) / 0.2))  # 归一化到0-1
    
    def _normalize_volume_score(self, scores: Dict[str, float]) -> float:
        """归一化成交量得分"""
        score = (
            scores['volume_change_5d'] * 0.3 +
            scores['volume_ratio'] * 0.4 +
            scores['price_volume_match'] * 0.3
        )
        return max(0, min(1, (score + 0.1) / 0.2))
    
    def _normalize_sentiment_score(self, scores: Dict[str, float]) -> float:
        """归一化情绪得分"""
        # 简化版本：使用波动率
        volatility = scores.get('volatility', 0.02)
        score = 1.0 - min(1.0, volatility / 0.05)  # 波动率越低，情绪越稳定
        return score
    
    def _normalize_technical_score(self, scores: Dict[str, float]) -> float:
        """归一化技术得分"""
        score = (
            (scores['ma_alignment'] + 1) / 2 * 0.3 +
            (scores['macd_signal'] + 1) / 2 * 0.3 +
            (scores['rsi_score'] + 1) / 2 * 0.2 +
            (scores['bb_position'] + 0.5) * 0.2
        )
        return max(0, min(1, score))
```

<h2 id="section-3-2-3">📈 3.2.3 状态评分</h2>

状态评分用于量化市场状态的强度、持续性和可靠性。

### 状态强度评分

状态强度反映当前状态的强烈程度：

```python
def calculate_regime_strength(data: pd.DataFrame, 
                              regime: MarketRegime) -> float:
    """
    计算市场状态强度（0-100）
    
    Args:
        data: 市场数据
        regime: 市场状态
    
    Returns:
        状态强度得分
    """
    analyzer = MarketStatusAnalyzer()
    result = analyzer.analyze(data)
    
    if regime == MarketRegime.RISK_ON:
        # risk_on强度 = 综合得分 * 100
        strength = result['total_score'] * 100
    elif regime == MarketRegime.RISK_OFF:
        # risk_off强度 = (1 - 综合得分) * 100
        strength = (1 - result['total_score']) * 100
    else:  # neutral
        # neutral强度 = |综合得分 - 0.5| * 200（越接近0.5越强）
        strength = abs(result['total_score'] - 0.5) * 200
    
    return min(100, max(0, strength))
```

### 状态持续性评估

状态持续性评估当前状态能够持续的概率：

```python
def assess_regime_persistence(data: pd.DataFrame,
                             regime: MarketRegime,
                             lookback: int = 10) -> float:
    """
    评估市场状态持续性（0-1）
    
    Args:
        data: 市场数据
        regime: 当前市场状态
        lookback: 回看周期
    
    Returns:
        状态持续性得分
    """
    analyzer = MarketStatusAnalyzer()
    
    # 计算历史状态
    historical_regimes = []
    for i in range(lookback, len(data)):
        historical_data = data.iloc[:i+1]
        result = analyzer.analyze(historical_data)
        historical_regimes.append(result['regime'])
    
    # 计算一致性
    consistency = sum([1 for r in historical_regimes if r == regime.value]) / len(historical_regimes)
    
    # 计算持续时间
    duration = 0
    for i in range(len(historical_regimes) - 1, -1, -1):
        if historical_regimes[i] == regime.value:
            duration += 1
        else:
            break
    
    # 持续性得分 = 一致性 * 0.6 + 持续时间因子 * 0.4
    duration_factor = min(1.0, duration / lookback)
    persistence = consistency * 0.6 + duration_factor * 0.4
    
    return persistence
```

<h2 id="section-3-2-4">🤖 3.2.4 AI辅助识别</h2>

AI辅助识别使用机器学习技术，提高市场状态判断的准确性。

### AI状态识别模型

```python
import torch
import torch.nn as nn
from sklearn.ensemble import RandomForestClassifier

class MarketRegimeClassifier:
    """市场状态分类器（使用随机森林）"""
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.feature_names = None
    
    def extract_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        提取特征
        
        Args:
            data: 市场数据
        
        Returns:
            特征DataFrame
        """
        features = pd.DataFrame()
        
        # 价格特征
        price_scores = analyze_price_dimension(data)
        features['price_change_20d'] = price_scores['price_change_20d']
        features['price_position'] = price_scores['price_position']
        features['price_trend'] = price_scores['price_trend']
        
        # 成交量特征
        volume_scores = analyze_volume_dimension(data)
        features['volume_ratio'] = volume_scores['volume_ratio']
        features['volume_trend'] = volume_scores['volume_trend']
        
        # 技术特征
        technical_scores = analyze_technical_dimension(data)
        features['ma_alignment'] = technical_scores['ma_alignment']
        features['rsi_score'] = technical_scores['rsi_score']
        
        # 更多特征...
        
        return features
    
    def train(self, X: pd.DataFrame, y: pd.Series):
        """
        训练模型
        
        Args:
            X: 特征数据
            y: 标签数据（'risk_on', 'risk_off', 'neutral'）
        """
        self.model.fit(X, y)
        self.feature_names = X.columns.tolist()
    
    def predict(self, data: pd.DataFrame) -> str:
        """
        预测市场状态
        
        Args:
            data: 市场数据
        
        Returns:
            预测的市场状态
        """
        features = self.extract_features(data)
        prediction = self.model.predict(features.iloc[[-1]])[0]
        return prediction
```

<h2 id="section-3-2-5">🔄 3.2.5 自动化实现</h2>

市场状态判断模块支持自动化运行，定时判断市场状态，自动更新结果。

```python
import schedule
import time
from datetime import datetime

class MarketStatusMonitor:
    """市场状态监控器"""
    
    def __init__(self):
        self.analyzer = MarketStatusAnalyzer()
        self.current_status = None
        self.last_update_time = None
    
    def check_status(self, symbol: str = '000001.SH'):
        """
        检查市场状态
        
        Args:
            symbol: 股票代码或指数代码
        """
        # 获取数据
        data = get_market_data(symbol,
                              start_date=(datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d'),
                              end_date=datetime.now().strftime('%Y-%m-%d'))
        
        # 分析市场状态
        result = self.analyzer.analyze(data)
        
        # 计算状态强度
        regime = MarketRegime(result['regime'])
        strength = calculate_regime_strength(data, regime)
        
        # 评估持续性
        persistence = assess_regime_persistence(data, regime)
        
        # 更新状态
        self.current_status = {
            'symbol': symbol,
            'regime': result['regime'],
            'strength': strength,
            'persistence': persistence,
            'total_score': result['total_score'],
            'dimension_scores': result['dimension_scores'],
            'timestamp': datetime.now()
        }
        
        self.last_update_time = datetime.now()
        
        logger.info(f"市场状态更新: {self.current_status}")
        
        # 如果状态变化，发送告警
        if self._should_alert():
            self._send_alert()
        
        return self.current_status
    
    def start_auto_monitor(self, interval_minutes: int = 30):
        """
        启动自动监控
        
        Args:
            interval_minutes: 监控间隔（分钟）
        """
        schedule.every(interval_minutes).minutes.do(self.check_status)
        
        # 立即执行一次
        self.check_status()
        
        # 持续运行
        while True:
            schedule.run_pending()
            time.sleep(60)
```

<h2 id="section-3-2-6">🛠️ 3.2.6 MCP工具使用</h2>

市场状态判断模块与MCP工具深度集成，支持通过MCP工具获取市场状态。

### TRQuant MCP工具

#### trquant_market_status

获取A股市场当前状态，包括市场Regime（risk_on/risk_off/neutral）、指数趋势和风格轮动。

**使用示例**：

```python
# 通过MCP调用获取市场状态
market_status = mcp_client.call_tool(
    "trquant_market_status",
    {"universe": "CN_EQ"}
)

# 返回结果示例
{
    "regime": "risk_on",  # 市场状态：risk_on/risk_off/neutral
    "index_trend": {
        "shanghai": "up",      # 上证指数趋势：up/down/sideways
        "shenzhen": "up",      # 深证成指趋势
        "chuangye": "up"       # 创业板指趋势
    },
    "style_rotation": {
        "large_cap": 0.6,      # 大盘股风格强度
        "mid_cap": 0.3,        # 中盘股风格强度
        "small_cap": 0.1       # 小盘股风格强度
    }
}

# 在代码中使用
if market_status['regime'] == 'risk_on':
    # 牛市策略
    strategy = generate_bull_market_strategy()
elif market_status['regime'] == 'risk_off':
    # 熊市策略
    strategy = generate_bear_market_strategy()
else:
    # 震荡市策略
    strategy = generate_neutral_market_strategy()
```

### KB MCP Server工具

#### kb.query

查询知识库，获取市场状态判断相关的文档和代码：

```python
# 查询市场状态判断相关的知识
results = mcp_client.call_tool(
    "kb.query",
    {
        "query": "市场状态判断 risk_on risk_off 多维度分析",
        "collection": "manual_kb",
        "top_k": 5
    }
)
```

### Data Collector MCP工具

#### data_collector.crawl_web

爬取网页内容，收集市场状态相关的研究资料：

```python
# 爬取市场状态分析相关网页
content = mcp_client.call_tool(
    "data_collector.crawl_web",
    {
        "url": "https://example.com/market-regime-analysis",
        "extract_text": True
    }
)
```

## 🔗 相关章节

- **第2章：数据源模块** - 了解数据获取机制，为市场状态判断提供数据支撑
- **第3章：市场分析模块** - 了解市场分析模块的整体设计
- **第3.1节：趋势分析** - 趋势分析结果用于市场状态判断
- **第4章：投资主线识别** - 市场状态判断结果用于主线识别
- **第5章：候选池构建** - 市场状态判断结果用于股票池筛选
- **第6章：因子库** - 市场状态判断结果用于因子推荐
- **第7章：策略开发** - 市场状态判断结果用于策略生成
- **第10章：开发指南** - 了解市场状态判断模块的开发规范

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了市场状态判断功能，包括市场状态分类体系、多维度判断机制和状态评分方法。通过理解市场环境评估技术，帮助开发者掌握如何全面判断市场状态，为投资决策提供宏观视角。</p>
  
  <h3>下节预告</h3>
  <p>掌握了市场状态判断后，下一节将介绍五维评分系统，包括宏观、资金、行业、技术、估值五个维度的评分方法和综合评分计算。通过理解五维评分系统的设计原理，帮助开发者掌握如何构建全面的市场环境评估体系。</p>
  
  <a href="/ashare-book6/003_Chapter3_Market_Analysis/3.3_Five_Dimensional_Scoring_CN" class="next-section">
    继续学习：3.3 五维评分系统 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
<!-- Code updated: 2025-12-13T10:53:43.750Z -->
