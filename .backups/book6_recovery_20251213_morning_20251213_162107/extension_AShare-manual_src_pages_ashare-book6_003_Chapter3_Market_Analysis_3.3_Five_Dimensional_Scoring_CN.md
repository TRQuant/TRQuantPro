---
title: "3.3 五维评分系统"
description: "详细介绍市场分析模块的五维评分系统，包括宏观、资金、行业、技术、估值五个维度的评分方法和综合评分计算"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 📊 3.3 五维评分系统

> **核心摘要：**
> 
> 本节系统介绍市场分析模块的五维评分系统，通过宏观、资金、行业、技术、估值五个维度全面评估市场环境。通过理解各维度评分方法、综合评分计算和评分应用场景，帮助开发者掌握如何构建全面的市场环境评估体系。五维评分系统为后续的主线识别、因子推荐、策略生成提供准确的市场环境判断依据。

五维评分系统是市场分析模块的综合评估功能，通过宏观、资金、行业、技术、估值五个维度，全面评估市场环境。

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
  <div class="section-item" onclick="scrollToSection('section-3-3-1')">
    <h4>🌍 3.3.1 宏观维度评分</h4>
    <p>GDP增速、CPI、PMI、货币政策等宏观指标的评分方法和实现</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-3-3-2')">
    <h4>💰 3.3.2 资金维度评分</h4>
    <p>北向资金、融资融券、公募基金仓位等资金流向指标的评分方法</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-3-3-3')">
    <h4>🏭 3.3.3 行业维度评分</h4>
    <p>行业轮动、行业景气度、行业估值等指标的评分方法</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-3-3-4')">
    <h4>📈 3.3.4 技术维度评分</h4>
    <p>指数趋势、技术形态、技术指标等指标的评分方法</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-3-3-5')">
    <h4>💎 3.3.5 估值维度评分</h4>
    <p>市场估值水平、行业估值、个股估值等指标的评分方法</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-3-3-6')">
    <h4>🔢 3.3.6 综合评分计算</h4>
    <p>加权平均计算、权重配置、评分应用场景</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解五维评分设计**：掌握五个维度的评分原理和计算方法
- **实现各维度评分**：理解各维度独立评分的实现细节和代码逻辑
- **掌握综合评分计算**：理解加权平均计算和权重配置方法
- **应用评分结果**：掌握评分结果在主线识别、因子推荐、策略生成中的应用

## 📚 核心概念

### 模块定位

- **工作流位置**：步骤2 - 📈 市场趋势
- **核心职责**：五维评分、综合评估、市场环境判断
- **服务对象**：主线识别、因子推荐、策略生成、策略优化

### 五维评分设计原则

五维评分系统遵循以下设计原则：

1. **全面性**：覆盖宏观、资金、行业、技术、估值五个维度，全面评估市场环境
2. **独立性**：每个维度独立评分（0-100分），避免维度间相互影响
3. **可解释性**：每个维度的评分方法清晰透明，便于理解和调试
4. **可调整性**：支持根据市场变化动态调整各维度权重和评分方法
5. **实用性**：评分结果直接应用于后续的投资决策流程

<h2 id="section-3-3-1">🌍 3.3.1 宏观维度评分</h2>

宏观维度评分通过分析宏观经济指标，评估整体经济环境对市场的影响。

### 评分指标

宏观维度评分包括以下指标：

1. **GDP增速**：反映经济增长水平
   - 数据来源：国家统计局、Wind、JQData
   - 更新频率：季度
   - 评分权重：30%

2. **CPI（消费者物价指数）**：反映通胀水平
   - 数据来源：国家统计局、Wind、JQData
   - 更新频率：月度
   - 评分权重：20%

3. **PMI（采购经理人指数）**：反映制造业景气度
   - 数据来源：国家统计局、Wind、JQData
   - 更新频率：月度
   - 评分权重：30%

4. **货币政策**：利率、准备金率等
   - 数据来源：央行公告、Wind、JQData
   - 更新频率：不定期
   - 评分权重：20%

### 评分方法实现

<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_macro_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
def score_macro_dimension(gdp_growth: float, cpi: float, pmi: float, 
                         monetary_policy: str) -> float:
    """
    宏观维度评分
    
    Args:
        gdp_growth: GDP增速（%）
        cpi: CPI（%）
        pmi: PMI（50为荣枯线）
        monetary_policy: 货币政策（'loose'宽松/'neutral'中性/'tight'紧缩）
    
    Returns:
        宏观维度评分（0-100分）
    """
    score = 0.0
    
    # 1. GDP增速评分（0-30分）
    # 理想区间：5-7%
    if 5 <= gdp_growth <= 7:
        gdp_score = 30
    elif 4 <= gdp_growth < 5 or 7 < gdp_growth <= 8:
        gdp_score = 25
    elif 3 <= gdp_growth < 4 or 8 < gdp_growth <= 9:
        gdp_score = 20
    elif 2 <= gdp_growth < 3 or 9 < gdp_growth <= 10:
        gdp_score = 15
    else:
        gdp_score = max(0, 30 - abs(gdp_growth - 6) * 5)
    
    # 2. CPI评分（0-20分）
    # 理想区间：1.5-2.5%
    if 1.5 <= cpi <= 2.5:
        cpi_score = 20
    elif 1.0 <= cpi < 1.5 or 2.5 < cpi <= 3.0:
        cpi_score = 15
    elif 0.5 <= cpi < 1.0 or 3.0 < cpi <= 3.5:
        cpi_score = 10
    else:
        cpi_score = max(0, 20 - abs(cpi - 2.0) * 10)
    
    # 3. PMI评分（0-30分）
    # 50为荣枯线，>50表示扩张
    if pmi >= 52:
        pmi_score = 30
    elif 50 <= pmi < 52:
        pmi_score = 25
    elif 48 <= pmi < 50:
        pmi_score = 15
    elif 46 <= pmi < 48:
        pmi_score = 10
    else:
        pmi_score = max(0, (pmi - 40) * 1.5)
    
    # 4. 货币政策评分（0-20分）
    policy_scores = {
        'loose': 20,    # 宽松：利好市场
        'neutral': 15,  # 中性：中性
        'tight': 5      # 紧缩：利空市场
 <CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_get_macro_indicators.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
import jqdatasdk as jq
import pandas as pd
from datetime import datetime, timedelta

def get_macro_indicators():
    """获取宏观指标数据"""
    # 初始化JQData
    jq.auth('username', 'password')
    
    # 获取GDP增速（季度数据）
    gdp_data = jq.get_macro_data('GDP_YOY', start_date='2020-01-01')
    latest_gdp = gdp_data.iloc[-1]['value'] if not gdp_data.empty else 5.0
    
    # 获取CPI（月度数据）
    cpi_data = jq.get_macro_data('CPI_YOY', start_date='2020-01-01')
    latest_cpi = cpi_data.iloc[-1]['value'] if not cpi_data.empty else 2.0
    
    # 获取PMI（月度数据）
    pmi_data = jq.get_macro_data('PMI', start_date='2020-01-01')
    latest_pmi = pmi_data.iloc[-1]['value'] if not pmi_data.empty else 50.0
    
    # 判断货币政策（简化处理，实际应从央行公告分析）
    # 可以通过利率、准备金率等指标判断
    interest_rate = jq.get_macro_data('INTEREST_RATE_1Y', start_date='2020-01-01')
    if not interest_rate.empty:
        latest_rate = interest_rate.iloc[-1]['value']
        if latest_rate < 3.0:
            monetary_policy = 'loose'
        elif latest_rate > 4.0:
            monetary_policy = 'tight'
        else:
            monetary_policy = 'neutral'
    else:
        monetary_policy = 'neutral'
    
    return {
        'gdp_growth': latest_gdp,
        'cpi': latest_cpi,
        'pmi': latest_pmi,
        'monetary_policy': monetary_policy
    }
```
-->onetary_policy = 'neutral'
    
    return {
        'gdp_growth': latest_gdp,
        'cpi': latest_cpi,
        'pmi': latest_pmi,
        'monetary_policy': m<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_capital_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
def score_capital_dimension(northbound_flow: float, margin_balance: float, 
                           fund_position: float) -> float:
    """
    资金维度评分
    
    Args:
        northbound_flow: 北向资金净流入（亿元，近20日累计）
        margin_balance: 融资融券余额（亿元）
        fund_position: 公募基金仓位（%，0-100）
    
    Returns:
        资金维度评分（0-100分）
    """
    score = 0.0
    
    # 1. 北向资金评分（0-40分）
    # 正流入越多，评分越高
    if northbound_flow > 100:
        northbound_score = 40
    elif northbound_flow > 50:
        northbound_score = 35
    elif northbound_flow > 20:
        northbound_score = 30
    elif northbound_flow > 0:
        northbound_score = 25
    elif northbound_flow > -20:
        northbound_score = 20
    elif northbound_flow > -50:
        northbound_score = 15
    else:
        northbound_score = max(0, 40 + northbound_flow * 0.4)
    
    # 2. 融资融券评分（0-30分）
    # 余额越高，市场情绪越乐观
    # 参考历史分位数：50分位约15000亿，75分位约18000亿
    if margin_balance > 18000:
        margin_score = 30
    elif margin_balance > 15000:
        margin_score = 25
    elif margin_balance > 12000:
        margin_score = 20
    elif margin_balance > 10000:
        margin_score = 15
    else:
        margin_score = max(0, margin_balance / 10000 * 1.5)
    
    # 3. 公募基金仓位评分（0-30分）
    # 仓位越高，市场越乐观
    # 历史平均仓位约75-80%
    if fund_position > 85:
        fund_score = 30
    elif fund_position > 80:
        fund_score = 25
    elif fund_position > 75:
        fund_score = 20
    elif fund_position > 70:
        fund_score = <CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_get_capital_indicators.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def get_capital_indicators():
    """获取资金指标数据"""
    # 1. 获取北向资金（近20日累计净流入）
    try:
        northbound_data = ak.stock_hsgt_fund_flow_summary_em()
        if not northbound_data.empty:
            # 取最近20日数据
            recent_data = northbound_data.tail(20)
            northbound_flow = recent_data['今日'].sum() / 100  # 转为亿元
        else:
            northbound_flow = 0
    except:
        northbound_flow = 0
    
    # 2. 获取融资融券余额
    try:
        margin_data = ak.stock_margin_underlying_info_szse()
        if not margin_data.empty:
            margin_balance = margin_data.iloc[-1]['融资余额'] / 100000000  # 转为亿元
        else:
            margin_balance = 15000  # 默认值
    except:
        margin_balance = 15000
    
    # 3. 获取公募基金仓位（从基金季报计算，这里简化处理）
    # 实际应从基金季报数据计算
    fund_position = 75.0  # 默认值，实际应从数据库查询
    
    return {
        'northbound_flow': northbound_flow,
        'margin_balance': margin_balance,
        'fund_position': fund_position
    }
```
-->    
    # 2. 获取融资融券余额
    try:
        margin_data = ak.stock_margin_underlying_info_szse()
        if not margin_data.empty:
            margin_balance = margin_data.ilo<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_industry_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
def score_industry_dimension(rotation_strength: float, industry_sentiment: float, 
                            industry_valuation: float) -> float:
    """
    行业维度评分
    
    Args:
        rotation_strength: 行业轮动强度（0-1，1表示轮动最活跃）
        industry_sentiment: 行业景气度（0-1，1表示最景气）
        industry_valuation: 行业估值分位数（0-100，50表示中位数）
    
    Returns:
        行业维度评分（0-100分）
    """
    score = 0.0
    
    # 1. 行业轮动评分（0-30分）
    # 轮动强度越高，市场越活跃
    rotation_score = min(30, max(0, rotation_strength * 30))
    
    # 2. 行业景气度评分（0-40分）
    # 景气度越高，市场环境越好
    sentiment_score = min(40, max(0, industry_sentiment * 40))
    
    # 3. 行业估值评分（0-30分）
    # 估值分位数在40-60之间为合理区间
    if 40 <= industry_valuation <= 60:
        valuation_score = 30
    elif 30 <= industry_valuation < 40 or 60 < industry_valuation <= 70:
        valuation_score = 25
    elif 20 <= industry_valuation < 30 or 70 < industry_valuation <= 80:
        valuation_score = 20
    else:
        valuation_score = max(0, 30 - abs(industry_valuation - 50) * 0.6)
    
    score = rotation_score + sentiment_score + valuation_score
    return min(100, max(0, score))
```
-->e = 0.0
    
    # 1. 行业轮动评分（0-30分）
    # 轮动强度越高，市场越活跃
    rotation_score = min(30, max(0, rotation_strength * 30))
    
    # 2. 行业景气度评分（0-40分）
 <CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_technical_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
def score_technical_dimension(index_trend: float, technical_pattern: float, 
                              technical_indicators: float) -> float:
    """
    技术维度评分
    
    Args:
        index_trend: 指数趋势强度（0-1，1表示最强上升趋势）
        technical_pattern: 技术形态评分（0-1，1表示最佳形态）
        technical_indicators: 技术指标评分（0-1，1表示最佳指标）
    
    Returns:
        技术维度评分（0-100分）
    """
    score = 0.0
    
    # 1. 指数趋势评分（0-40分）
    trend_score = min(40, max(0, index_trend * 40))
    
    # 2. 技术形态评分（0-30分）
    pattern_score = min(30, max(0, technical_pattern * 30))
    
    # 3. 技术指标评分（0-30分）
    indicator_score = min(30, max(0, technical_indicators * 30))
    
    score = trend_score + pattern_score + indicator_score
    return min(100, max(0, score))
```
-->a
   - 更新频率：每日
   - 评分权重：40%

2. **技术形态评分**：技术形态评分
   - 数据来源：技术分析
   - 更新频率：每日
   - 评分权重：30%

3. **技术指标**：MACD、RSI等指标
   - 数据来源：技术分析
   - 更新频率：每日<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_valuation_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
def score_valuation_dimension(market_valuation: float, industry_valuation: float, 
                             stock_valuation: float) -> float:
    """
    估值维度评分
    
    Args:
        market_valuation: 市场估值分位数（0-100，30表示历史30%分位）
        industry_valuation: 行业估值分位数（0-100，50表示中位数）
        stock_valuation: 个股估值评分（0-100，越高表示估值越合理）
    
    Returns:
        估值维度评分（0-100分）
    """
    score = 0.0
    
    # 1. 市场估值评分（0-40分）
    # 估值分位数越低，评分越高（估值越低，越有吸引力）
    if market_valuation < 20:
        market_score = 40
    elif market_valuation < 30:
        market_score = 35
    elif market_valuation < 40:
        market_score = 30
    elif market_valuation < 50:
        market_score = 25
    elif market_valuation < 60:
        market_score = 20
    else:
        market_score = max(0, 40 - (market_valuation - 30) * 0.8)
    
    # 2. 行业估值评分（0-30分）
    # 估值分位数在40-60之间为合理区间
    if 40 <= industry_valuation <= 60:
        industry_score = 30
    elif 30 <= industry_valuation < 40 or 60 < industry_valuation <= 70:
        industry_score = 25
    elif 20 <= industry_valuation < 30 or 70 < industry_valuation <= 80:
        industry_score = 20
    else:
        industry_score = max(0, 30 - abs(industry_valuation - 50) * 0.6)
    
    # 3. 个股估值评分（0-30分）
    stock_score = min(30, max(0, stock_valuation * 0.3))
    
    scor<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_07.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
DEFAULT_WEIGHTS = {
    'macro': 0.20,      # 宏观维度权重：20%
    'ca<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_calculate_comprehensive_score.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
def calculate_comprehensive_score(scores: dict, weights: dict = None) -> float:
    """
    计算综合评分
    
    Args:
        scores: 各维度评分字典
            {
                'macro': 75.0,
                'capital': 80.0,
                'industry': 70.0,
                'technical': 65.0,
                'valuation': 60.0
            }
        weights: 各维度权重字典（可选，默认使用DEFAULT_WEIGHTS）
    
    Returns:
        综合评分（0-100分）
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
    
    # 计算加权平均
    weighted_sum = sum(scores[dim] * weights[dim] for dim in scores if dim in weights)
    total_weight = sum(weights[dim] for dim in scores if di<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3___init__.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：
```python
class FiveDimensionScorer:
    """五维评分系统"""
    
    def __init__(self, weights: dict = None):
        self.weights = weights or DEFAULT_WEIGHTS
    
    def score_market_environment(self) -> dict:
        """
        评估市场环境
        
        Returns:
            评分结果字典
        """
        # 1. 获取各维度数据
        macro_data = get_macro_indicators()
        capital_data = get_capital_indicators()
        industry_data = get_industry_indicators()
        technical_data = get_technical_indicators()
        valuation_data = get_valuation_indicators()
        
        # 2. 计算各维度评分
        scores = {
            'macro': score_macro_dimension(**macro_data),
            'capital': score_capital_dimension(**capital_data),
            'industry': score_industry_dimension(**industry_data),
            'technical': score_technical_dimension(**technical_data),
            'valuation': score_valuation_dimension(**valuation_data)
        }
        
        # 3. 计算综合评分
        comprehensive_score = calculate_comprehensive_score(scores, self.weights)
        
        return {
            'scores': scores,
            'comprehensive_score': comprehensive_score,
            'weights': self.weights,
            'timestamp': datetime.now().isoformat()
        }
```
-->is None:
        weights = DEFAULT_WEIGHTS
    
    # 计算加权平均
    weighted_sum = sum(scores[dim] * weights[dim] for dim in scores if dim in weights)
    total_weight = sum(weights[dim] for dim in scores if dim in weights)
    
    if total_weight == 0:
        return 0.0
    
    comprehensive_score = weighted_sum / total_weight
    return min(100, max(0, comprehensive_score))
```

### 完整实现示例

```python
class FiveDimensionScorer:
    """五维评分系统"""
    
    def __init__(self, weights: dict = None):
        self.weights = weights or DEFAULT_WEIGHTS
    
    def score_market_environment(self) -> dict:
        """
        评估市场环境
        
        Returns:
            评分结果字典
        """
        # 1. 获取各维度数据
        macro_data = get_macro_indicators()
        capital_data = get_capital_indicators()
        industry_data = get_industry_indicators()
        technical_data = get_technical_indicators()
        valuation_data = get_valuation_indicators()
        
        # 2. 计算各维度评分
        scores = {
            'macro': score_macro_dimension(**macro_data),
            'capital': score_capital_dimension(**capital_data),
            'industry': score_industry_dimension(**industry_data),
            'technical': score_technical_dimension(**technical_data),
            'valuation': score_valuation_dimension(**valuation_data)
        }
        
        # 3. 计算综合评分
        comprehensive_score = calculate_comprehensive_score(scores, self.weights)
        
        return {
            'scores': scores,
            'comprehensive_score': comprehensive_score,
            'weights': self.weights,
            'timestamp': datetime.now().isoformat()
        }
```

### 评分应用场景

五维评分结果用于：

1. **主线识别**：高评分维度对应的行业/主题优先考虑
2. **因子推荐**：根据评分维度推荐相应的因子
3. **策略生成**：根据评分结果调整策略参数
4. **策略优化**：根据评分变化动态优化策略

## 🔗 相关章节

- **3.1 趋势分析**：了解技术指标分析，为技术维度评分提供基础
- **3.2 市场状态**：了解市场状态判断，为综合评分提供参考
- **第4章：投资主线识别**：了解如何使用五维评分结果进行主线识别
- **第6章：因子库**：了解如何使用五维评分结果进行因子推荐
- **第7章：策略开发**：了解如何使用五维评分结果进行策略生成

## 💡 关键要点

1. **五维评分设计**：通过宏观、资金、行业、技术、估值五个维度全面评估市场环境
2. **独立评分**：每个维度独立评分（0-100分），然后加权平均得到综合评分
3. **权重配置**：支持根据市场变化动态调整各维度权重
4. **评分应用**：评分结果用于主线识别、因子推荐、策略生成和策略优化

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了市场分析模块的五维评分系统，通过宏观、资金、行业、技术、估值五个维度全面评估市场环境。通过理解各维度评分方法、综合评分计算和评分应用场景，帮助开发者掌握如何构建全面的市场环境评估体系。</p>
  
  <h3>下节预告</h3>
  <p>掌握了五维评分系统后，下一节将介绍MCP工具集成，包括trquant_market_status、trquant_mainlines、知识库查询等工具的使用。通过理解MCP工具在市场分析中的应用，帮助开发者掌握如何使用MCP工具提升市场分析效率。</p>
  
  <a href="/ashare-book6/003_Chapter3_Market_Analysis/3.4_MCP_Tool_Integration_CN" class="next-section">
    继续学习：3.4 MCP工具集成 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
<!-- Code updated: 2025-12-13T13:40:57.055Z -->
