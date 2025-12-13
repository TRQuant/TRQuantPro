---
title: "5.3 股票评分"
description: "详细介绍候选池构建模块的股票评分系统，包括多因子评分、综合评分计算和评分排序方法"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 📈 5.3 股票评分

> **核心摘要：**
> 
> 本节系统介绍候选池构建模块的股票评分系统，通过技术面、资金面、基本面、情绪面四个维度对候选股票进行多因子评分，并计算综合评分。通过理解各维度评分方法、综合评分计算和评分排序方法，帮助开发者掌握如何构建全面的股票评分体系，为候选池排序和筛选提供准确依据。

股票评分系统对候选股票进行多因子评分，为候选池排序和筛选提供依据。

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
  <div class="section-item" onclick="scrollToSection('section-5-3-1')">
    <h4>📊 5.3.1 技术面评分</h4>
    <p>价格趋势、成交量、技术指标、突破信号等因子的评分方法</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-5-3-2')">
    <h4>💰 5.3.2 资金面评分</h4>
    <p>主力资金、北向资金、龙虎榜、换手率等因子的评分方法</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-5-3-3')">
    <h4>💼 5.3.3 基本面评分</h4>
    <p>盈利能力、成长性、估值水平、财务健康等因子的评分方法</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-5-3-4')">
    <h4>😊 5.3.4 情绪面评分</h4>
    <p>涨跌停、龙虎榜、市场情绪等因子的评分方法</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-5-3-5')">
    <h4>🔢 5.3.5 综合评分计算</h4>
    <p>加权平均计算、权重配置、主线热度融合</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-5-3-6')">
    <h4>📊 5.3.6 评分排序</h4>
    <p>按综合得分排序、按因子得分排序、多维度排序</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解多因子评分设计**：掌握技术面、资金面、基本面、情绪面四个维度的评分原理
- **实现各维度评分**：理解各维度独立评分的实现细节和代码逻辑
- **掌握综合评分计算**：理解加权平均计算和权重配置方法
- **应用评分排序**：掌握评分结果在候选池排序和筛选中的应用

## 📚 核心概念

### 模块定位

- **工作流位置**：步骤4 - 📦 候选池构建
- **核心职责**：多因子评分、综合评分计算、评分排序
- **服务对象**：候选池构建器、策略生成

### 评分设计原则

股票评分系统遵循以下设计原则：

1. **多维度评估**：覆盖技术面、资金面、基本面、情绪面四个维度，全面评估股票质量
2. **因子独立性**：每个因子独立评分，避免因子间相互影响
3. **权重可配置**：支持根据市场环境动态调整各维度权重
4. **主线融合**：结合主线热度，提升主线相关股票的评分
5. **可解释性**：每个因子的评分方法清晰透明，便于理解和调试

<h2 id="section-5-3-1">📊 5.3.1 技术面评分</h2>

技术面评分通过分析价格趋势、成交量、技术指标、突破信号等，评估股票的技术面强弱。

### 评分因子

技术面评分包括以下因子：

1. **价格趋势**（40%权重）
   - 数据来源：JQData、AKShare
   - 更新频率：每日
   - 评分方法：基于价格动量、趋势强度

2. **成交量**（30%权重）
   - 数据来源：JQData、AKShare
   - 更新频率：每日
   - 评分方法：基于成交量放大、量价配合

3. **技术指标**（20%权重）
   - 数据来源：技术分析计算
   - 更新频率：每日
   - 评分方法：基于MACD、RSI、KDJ等指标

4. **突破信号**（10%权重）
   - 数据来源：技术分析计算
   - 更新频率：每日
   - 评分方法：基于均线突破、价格突破

### 评分方法实现

```python
def score_technical_dimension(
    stock_code: str,
    price_data: pd.DataFrame,
    volume_data: pd.DataFrame,
    date: str
) -> float:
    """
    技术面评分
    
    Args:
        stock_code: 股票代码
        price_data: 价格数据（包含open, high, low, close）
        volume_data: 成交量数据
        date: 评分日期
    
    Returns:
        技术面评分（0-100分）
    """
    score = 0.0
    
    # 1. 价格趋势评分（0-40分）
    # 计算价格动量（20日收益率）
    returns_20d = (price_data['close'].iloc[-1] / price_data['close'].iloc[-21] - 1) * 100
    
    # 计算趋势强度（均线斜率）
    ma20 = price_data['close'].rolling(20).mean()
    ma60 = price_data['close'].rolling(60).mean()
    trend_strength = (ma20.iloc[-1] - ma20.iloc[-20]) / ma20.iloc[-20] * 100
    
    # 价格趋势评分
    if returns_20d > 20 and trend_strength > 5:
        trend_score = 40
    elif returns_20d > 10 and trend_strength > 2:
        trend_score = 35
    elif returns_20d > 5 and trend_strength > 0:
        trend_score = 30
    elif returns_20d > 0:
        trend_score = 25
    else:
        trend_score = max(0, 20 + returns_20d * 0.5)
    
    # 2. 成交量评分（0-30分）
    # 计算成交量放大倍数
    avg_volume_20d = volume_data['volume'].rolling(20).mean().iloc[-1]
    current_volume = volume_data['volume'].iloc[-1]
    volume_ratio = current_volume / avg_volume_20d if avg_volume_20d > 0 else 1
    
    # 成交量评分
    if volume_ratio > 3:
        volume_score = 30
    elif volume_ratio > 2:
        volume_score = 25
    elif volume_ratio > 1.5:
        volume_score = 20
    elif volume_ratio > 1:
        volume_score = 15
    else:
        volume_score = max(0, 10 + (volume_ratio - 0.5) * 10)
    
    # 3. 技术指标评分（0-20分）
    # 计算MACD、RSI、KDJ等指标
    macd_signal = calculate_macd_signal(price_data)
    rsi_value = calculate_rsi(price_data, period=14)
    kdj_signal = calculate_kdj_signal(price_data)
    
    # 技术指标评分
    indicator_score = 0
    if macd_signal == 'bullish':
        indicator_score += 7
    if 30 < rsi_value < 70:  # RSI在合理区间
        indicator_score += 7
    if kdj_signal == 'bullish':
        indicator_score += 6
    
    # 4. 突破信号评分（0-10分）
    # 检查是否站上均线
    current_price = price_data['close'].iloc[-1]
    ma20_current = ma20.iloc[-1]
    ma60_current = ma60.iloc[-1]
    
    breakthrough_score = 0
    if current_price > ma20_current and ma20_current > ma60_current:
        breakthrough_score = 10
    elif current_price > ma20_current:
        breakthrough_score = 7
    elif current_price > ma60_current:
        breakthrough_score = 5
    
    # 设计原理：技术面评分采用累加方式
    # 原因：多个技术指标综合评分，累加反映整体技术面强度
    # 评分维度：趋势强度、成交量、技术指标、突破信号
    # 为什么这样设计：单一指标可能误判，多指标综合更准确
    score = trend_score + volume_score + indicator_score + breakthrough_score
    
    # 设计原理：得分限制在0-100分
    # 原因：确保评分在合理范围内，便于后续比较和排序
    # 实现方式：使用min和max函数限制范围
    return min(100, max(0, score))
```

### 辅助函数实现

```python
def calculate_macd_signal(price_data: pd.DataFrame) -> str:
    """计算MACD信号"""
    ema12 = price_data['close'].ewm(span=12, adjust=False).mean()
    ema26 = price_data['close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    
    if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] <= signal.iloc[-2]:
        return 'bullish'  # 金叉
    elif macd.iloc[-1] < signal.iloc[-1] and macd.iloc[-2] >= signal.iloc[-2]:
        return 'bearish'  # 死叉
    else:
        return 'neutral'

def calculate_rsi(price_data: pd.DataFrame, period: int = 14) -> float:
    """计算RSI指标"""
    delta = price_data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def calculate_kdj_signal(price_data: pd.DataFrame) -> str:
    """计算KDJ信号"""
    low_min = price_data['low'].rolling(9).min()
    high_max = price_data['high'].rolling(9).max()
    rsv = (price_data['close'] - low_min) / (high_max - low_min) * 100
    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()
    j = 3 * k - 2 * d
    
    if k.iloc[-1] > d.iloc[-1] and k.iloc[-2] <= d.iloc[-2]:
        return 'bullish'  # K线上穿D线
    elif k.iloc[-1] < d.iloc[-1] and k.iloc[-2] >= d.iloc[-2]:
        return 'bearish'  # K线下穿D线
    else:
        return 'neutral'
```

<h2 id="section-5-3-2">💰 5.3.2 资金面评分</h2>

资金面评分通过分析主力资金、北向资金、龙虎榜、换手率等，评估股票的资金认可度。

### 评分因子

资金面评分包括以下因子：

1. **主力资金**（40%权重）
   - 数据来源：AKShare、JQData
   - 更新频率：每日
   - 评分方法：基于主力净流入、主力占比、资金持续性

2. **北向资金**（30%权重）
   - 数据来源：AKShare、JQData
   - 更新频率：每日
   - 评分方法：基于北向持仓、北向增持、北向占比

3. **龙虎榜**（20%权重）
   - 数据来源：AKShare
   - 更新频率：每日
   - 评分方法：基于上榜次数、净买入额、机构席位

4. **换手率**（10%权重）
   - 数据来源：JQData、AKShare
   - 更新频率：每日
   - 评分方法：基于换手率水平、换手率变化

### 评分方法实现

```python
def score_capital_dimension(
    stock_code: str,
    main_fund_data: Dict,
    northbound_data: Dict,
    lhb_data: Dict,
    turnover_data: Dict
) -> float:
    """
    资金面评分
    
    Args:
        stock_code: 股票代码
        main_fund_data: 主力资金数据
        northbound_data: 北向资金数据
        lhb_data: 龙虎榜数据
        turnover_data: 换手率数据
    
    Returns:
        资金面评分（0-100分）
    """
    score = 0.0
    
    # 1. 主力资金评分（0-40分）
    main_fund_inflow = main_fund_data.get('net_inflow', 0)  # 净流入（万元）
    main_fund_ratio = main_fund_data.get('main_ratio', 0)  # 主力占比
    consecutive_days = main_fund_data.get('consecutive_inflow_days', 0)  # 连续流入天数
    
    # 设计原理：主力资金评分采用分段评分
    # 原因：不同资金流入水平对应不同的评分，需要分段处理
    # 评分维度：净流入金额、主力占比、连续流入天数
    # 为什么这样设计：综合考虑多个维度，更准确反映主力资金认可度
    # 评分逻辑：
    # - 优秀（40分）：大额流入 + 高占比 + 持续流入
    # - 良好（35分）：中等流入 + 中等占比 + 持续流入
    # - 一般（30分）：小额流入 + 低占比
    # - 较差（20分）：小幅流出
    # - 很差（10-0分）：大幅流出
    if main_fund_inflow > 10000 and main_fund_ratio > 0.3 and consecutive_days >= 3:
        main_fund_score = 40
    elif main_fund_inflow > 5000 and main_fund_ratio > 0.2 and consecutive_days >= 2:
        main_fund_score = 35
    elif main_fund_inflow > 0 and main_fund_ratio > 0.1:
        main_fund_score = 30
    elif main_fund_inflow > -5000:
        main_fund_score = 20
    else:
        # 设计原理：线性评分
        # 原因：大幅流出时，流出越多得分越低
        # 公式：得分 = 10 + 净流入/1000，最低0分
        main_fund_score = max(0, 10 + main_fund_inflow / 1000)
    
    # 2. 北向资金评分（0-30分）
    northbound_position = northbound_data.get('position', 0)  # 持仓市值（万元）
    northbound_change = northbound_data.get('change_pct', 0)  # 增持幅度（%）
    northbound_ratio = northbound_data.get('ratio', 0)  # 占流通盘比例
    
    # 北向资金评分
    if northbound_position > 50000 and northbound_change > 5 and northbound_ratio > 0.05:
        northbound_score = 30
    elif northbound_position > 20000 and northbound_change > 2 and northbound_ratio > 0.02:
        northbound_score = 25
    elif northbound_position > 0 and northbound_change > 0:
        northbound_score = 20
    elif northbound_position > 0:
        northbound_score = 15
    else:
        northbound_score = 10
    
    # 3. 龙虎榜评分（0-20分）
    lhb_count = lhb_data.get('count', 0)  # 上榜次数（近20日）
    lhb_net_buy = lhb_data.get('net_buy', 0)  # 净买入额（万元）
    institution_count = lhb_data.get('institution_count', 0)  # 机构席位次数
    
    # 龙虎榜评分
    if lhb_count >= 3 and lhb_net_buy > 5000 and institution_count >= 1:
        lhb_score = 20
    elif lhb_count >= 2 and lhb_net_buy > 0:
        lhb_score = 15
    elif lhb_count >= 1:
        lhb_score = 10
    else:
        lhb_score = 5
    
    # 4. 换手率评分（0-10分）
    turnover_rate = turnover_data.get('turnover_rate', 0)  # 换手率（%）
    turnover_change = turnover_data.get('turnover_change', 0)  # 换手率变化（%）
    
    # 换手率评分（适度活跃为佳）
    if 3 <= turnover_rate <= 10 and turnover_change > 0:
        turnover_score = 10
    elif 2 <= turnover_rate <= 15:
        turnover_score = 8
    elif turnover_rate > 0:
        turnover_score = 5
    else:
        turnover_score = 0
    
    score = main_fund_score + northbound_score + lhb_score + turnover_score
    return min(100, max(0, score))
```

<h2 id="section-5-3-3">💼 5.3.3 基本面评分</h2>

基本面评分通过分析盈利能力、成长性、估值水平、财务健康等，评估股票的基本面质量。

### 评分因子

基本面评分包括以下因子：

1. **盈利能力**（35%权重）
   - 数据来源：JQData、Wind
   - 更新频率：季度
   - 评分方法：基于ROE、ROA、净利润率

2. **成长性**（35%权重）
   - 数据来源：JQData、Wind
   - 更新频率：季度
   - 评分方法：基于营收增速、净利润增速、营收质量

3. **估值水平**（20%权重）
   - 数据来源：JQData、Wind
   - 更新频率：每日
   - 评分方法：基于PE、PB、PEG

4. **财务健康**（10%权重）
   - 数据来源：JQData、Wind
   - 更新频率：季度
   - 评分方法：基于负债率、现金流、资产质量

### 评分方法实现

```python
def score_fundamental_dimension(
    stock_code: str,
    financial_data: Dict,
    valuation_data: Dict
) -> float:
    """
    基本面评分
    
    Args:
        stock_code: 股票代码
        financial_data: 财务数据
        valuation_data: 估值数据
    
    Returns:
        基本面评分（0-100分）
    """
    score = 0.0
    
    # 1. 盈利能力评分（0-35分）
    roe = financial_data.get('roe', 0)  # ROE（%）
    roa = financial_data.get('roa', 0)  # ROA（%）
    net_profit_margin = financial_data.get('net_profit_margin', 0)  # 净利润率（%）
    
    # 盈利能力评分
    profit_score = 0
    if roe > 20:
        profit_score += 12
    elif roe > 15:
        profit_score += 10
    elif roe > 10:
        profit_score += 8
    else:
        profit_score += max(0, roe / 10 * 8)
    
    if roa > 10:
        profit_score += 12
    elif roa > 7:
        profit_score += 10
    elif roa > 5:
        profit_score += 8
    else:
        profit_score += max(0, roa / 5 * 8)
    
    if net_profit_margin > 20:
        profit_score += 11
    elif net_profit_margin > 15:
        profit_score += 9
    elif net_profit_margin > 10:
        profit_score += 7
    else:
        profit_score += max(0, net_profit_margin / 10 * 7)
    
    profit_score = min(35, profit_score)
    
    # 2. 成长性评分（0-35分）
    revenue_growth = financial_data.get('revenue_growth', 0)  # 营收增速（%）
    profit_growth = financial_data.get('profit_growth', 0)  # 净利润增速（%）
    revenue_quality = financial_data.get('revenue_quality', 0)  # 营收质量（0-1）
    
    # 成长性评分
    growth_score = 0
    if revenue_growth > 30:
        growth_score += 12
    elif revenue_growth > 20:
        growth_score += 10
    elif revenue_growth > 10:
        growth_score += 8
    else:
        growth_score += max(0, revenue_growth / 10 * 8)
    
    if profit_growth > 50:
        growth_score += 12
    elif profit_growth > 30:
        growth_score += 10
    elif profit_growth > 20:
        growth_score += 8
    else:
        growth_score += max(0, profit_growth / 20 * 8)
    
    growth_score += revenue_quality * 11
    growth_score = min(35, growth_score)
    
    # 3. 估值水平评分（0-20分）
    pe = valuation_data.get('pe', 0)  # PE
    pb = valuation_data.get('pb', 0)  # PB
    peg = valuation_data.get('peg', 0)  # PEG
    
    # 估值水平评分（估值越低，评分越高）
    valuation_score = 0
    if 10 <= pe <= 25:
        valuation_score += 7
    elif 5 <= pe < 10 or 25 < pe <= 40:
        valuation_score += 5
    elif pe < 5 or 40 < pe <= 60:
        valuation_score += 3
    else:
        valuation_score += max(0, 7 - abs(pe - 20) / 10)
    
    if 1 <= pb <= 3:
        valuation_score += 7
    elif 0.5 <= pb < 1 or 3 < pb <= 5:
        valuation_score += 5
    else:
        valuation_score += max(0, 7 - abs(pb - 2) / 0.5)
    
    if 0.5 <= peg <= 1.5:
        valuation_score += 6
    elif 0.3 <= peg < 0.5 or 1.5 < peg <= 2:
        valuation_score += 4
    else:
        valuation_score += max(0, 6 - abs(peg - 1) / 0.5)
    
    valuation_score = min(20, valuation_score)
    
    # 4. 财务健康评分（0-10分）
    debt_ratio = financial_data.get('debt_ratio', 0)  # 负债率（%）
    cash_flow = financial_data.get('cash_flow', 0)  # 经营现金流（万元）
    asset_quality = financial_data.get('asset_quality', 0)  # 资产质量（0-1）
    
    # 财务健康评分
    health_score = 0
    if debt_ratio < 30:
        health_score += 4
    elif debt_ratio < 50:
        health_score += 3
    elif debt_ratio < 70:
        health_score += 2
    else:
        health_score += max(0, 4 - (debt_ratio - 30) / 10)
    
    if cash_flow > 0:
        health_score += 3
    elif cash_flow > -10000:
        health_score += 2
    else:
        health_score += 1
    
    health_score += asset_quality * 3
    health_score = min(10, health_score)
    
    score = profit_score + growth_score + valuation_score + health_score
    return min(100, max(0, score))
```

<h2 id="section-5-3-4">😊 5.3.4 情绪面评分</h2>

情绪面评分通过分析涨跌停、龙虎榜、市场情绪等，评估股票的市场情绪。

### 评分因子

情绪面评分包括以下因子：

1. **涨跌停**（50%权重）
   - 数据来源：AKShare、JQData
   - 更新频率：每日
   - 评分方法：基于涨停次数、跌停次数

2. **龙虎榜**（30%权重）
   - 数据来源：AKShare
   - 更新频率：每日
   - 评分方法：基于上榜次数、游资参与度

3. **市场情绪**（20%权重）
   - 数据来源：市场数据
   - 更新频率：每日
   - 评分方法：基于市场热度、资金情绪

### 评分方法实现

```python
def score_sentiment_dimension(
    stock_code: str,
    limit_data: Dict,
    lhb_data: Dict,
    market_sentiment: Dict
) -> float:
    """
    情绪面评分
    
    Args:
        stock_code: 股票代码
        limit_data: 涨跌停数据
        lhb_data: 龙虎榜数据
        market_sentiment: 市场情绪数据
    
    Returns:
        情绪面评分（0-100分）
    """
    score = 0.0
    
    # 1. 涨跌停评分（0-50分）
    limit_up_count = limit_data.get('limit_up_count', 0)  # 涨停次数（近20日）
    limit_down_count = limit_data.get('limit_down_count', 0)  # 跌停次数（近20日）
    
    # 涨跌停评分
    if limit_up_count >= 3 and limit_down_count == 0:
        limit_score = 50
    elif limit_up_count >= 2 and limit_down_count == 0:
        limit_score = 40
    elif limit_up_count >= 1 and limit_down_count == 0:
        limit_score = 30
    elif limit_up_count > limit_down_count:
        limit_score = 20
    elif limit_down_count == 0:
        limit_score = 15
    else:
        limit_score = max(0, 10 - limit_down_count * 5)
    
    # 2. 龙虎榜评分（0-30分）
    lhb_count = lhb_data.get('count', 0)  # 上榜次数（近20日）
    speculator_ratio = lhb_data.get('speculator_ratio', 0)  # 游资参与度（0-1）
    
    # 龙虎榜评分
    if lhb_count >= 3 and speculator_ratio > 0.5:
        lhb_score = 30
    elif lhb_count >= 2 and speculator_ratio > 0.3:
        lhb_score = 25
    elif lhb_count >= 1:
        lhb_score = 20
    else:
        lhb_score = 10
    
    # 3. 市场情绪评分（0-20分）
    market_heat = market_sentiment.get('heat', 0)  # 市场热度（0-1）
    capital_sentiment = market_sentiment.get('capital_sentiment', 0)  # 资金情绪（0-1）
    
    # 市场情绪评分
    sentiment_score = (market_heat * 0.6 + capital_sentiment * 0.4) * 20
    
    score = limit_score + lhb_score + sentiment_score
    return min(100, max(0, score))
```

<h2 id="section-5-3-5">🔢 5.3.5 综合评分计算</h2>

综合评分通过加权平均计算各维度评分，并结合主线热度，得到最终的股票评分。

### 权重配置

默认权重配置如下：

```python
DEFAULT_WEIGHTS = {
    'technical': 0.30,   # 技术面权重：30%
    'capital': 0.30,     # 资金面权重：30%
    'fundamental': 0.30, # 基本面权重：30%
    'sentiment': 0.10    # 情绪面权重：10%
}
```

### 综合评分计算实现

```python
def calculate_composite_score(
    technical_score: float,
    capital_score: float,
    fundamental_score: float,
    sentiment_score: float,
    mainline_heat: float = 0.0,
    weights: Dict = None
) -> float:
    """
    计算综合评分
    
    Args:
        technical_score: 技术面评分
        capital_score: 资金面评分
        fundamental_score: 基本面评分
        sentiment_score: 情绪面评分
        mainline_heat: 主线热度（0-1，可选）
        weights: 各维度权重字典（可选，默认使用DEFAULT_WEIGHTS）
    
    Returns:
        综合评分（0-100分）
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
    
    # 第一步：计算个股因子得分
    stock_factor = (
        technical_score * weights['technical'] +
        capital_score * weights['capital'] +
        fundamental_score * weights['fundamental'] +
        sentiment_score * weights['sentiment']
    )
    
    # 第二步：结合主线热度（如果提供）
    if mainline_heat > 0:
        # 主线热度权重15%，个股因子权重85%
        composite_score = (
            mainline_heat * 100 * 0.15 +  # 主线热度转换为0-100分
            stock_factor * 0.85
        )
    else:
        composite_score = stock_factor
    
    return min(100, max(0, composite_score))
```

### 完整实现示例

```python
class StockScorer:
    """股票评分系统"""
    
    def __init__(self, weights: Dict = None):
        self.weights = weights or DEFAULT_WEIGHTS
    
    def score_stock(
        self,
        stock_code: str,
        price_data: pd.DataFrame,
        volume_data: pd.DataFrame,
        main_fund_data: Dict,
        northbound_data: Dict,
        lhb_data: Dict,
        turnover_data: Dict,
        financial_data: Dict,
        valuation_data: Dict,
        limit_data: Dict,
        market_sentiment: Dict,
        mainline_heat: float = 0.0,
        date: str = None
    ) -> Dict:
        """
        对股票进行综合评分
        
        Returns:
            评分结果字典
        """
        # 1. 计算各维度评分
        technical_score = score_technical_dimension(
            stock_code, price_data, volume_data, date
        )
        
        capital_score = score_capital_dimension(
            stock_code, main_fund_data, northbound_data, lhb_data, turnover_data
        )
        
        fundamental_score = score_fundamental_dimension(
            stock_code, financial_data, valuation_data
        )
        
        sentiment_score = score_sentiment_dimension(
            stock_code, limit_data, lhb_data, market_sentiment
        )
        
        # 2. 计算综合评分
        composite_score = calculate_composite_score(
            technical_score,
            capital_score,
            fundamental_score,
            sentiment_score,
            mainline_heat,
            self.weights
        )
        
        return {
            'stock_code': stock_code,
            'scores': {
                'technical': technical_score,
                'capital': capital_score,
                'fundamental': fundamental_score,
                'sentiment': sentiment_score
            },
            'composite_score': composite_score,
            'mainline_heat': mainline_heat,
            'weights': self.weights,
            'timestamp': datetime.now().isoformat()
        }
```

<h2 id="section-5-3-6">📊 5.3.6 评分排序</h2>

评分排序根据综合得分对候选股票进行排序，支持多维度排序。

### 排序方法

#### 1. 按综合得分排序

```python
def sort_by_composite_score(stocks: List[CandidateStock]) -> List[CandidateStock]:
    """
    按综合得分排序
    
    Args:
        stocks: 候选股票列表
    
    Returns:
        排序后的股票列表
    """
    return sorted(stocks, key=lambda x: x.composite_score, reverse=True)
```

#### 2. 按因子得分排序

```python
def sort_by_factor_score(
    stocks: List[CandidateStock],
    factor: str = 'technical'
) -> List[CandidateStock]:
    """
    按因子得分排序
    
    Args:
        stocks: 候选股票列表
        factor: 因子名称（technical/capital/fundamental/sentiment）
    
    Returns:
        排序后的股票列表
    """
    factor_map = {
        'technical': 'technical_score',
        'capital': 'capital_score',
        'fundamental': 'fundamental_score',
        'sentiment': 'sentiment_score'
    }
    
    factor_key = factor_map.get(factor, 'composite_score')
    return sorted(stocks, key=lambda x: getattr(x, factor_key, 0), reverse=True)
```

#### 3. 多维度排序

```python
def sort_by_multiple_factors(
    stocks: List[CandidateStock],
    factors: List[Tuple[str, bool]] = None
) -> List[CandidateStock]:
    """
    多维度排序
    
    Args:
        stocks: 候选股票列表
        factors: 排序因子列表，每个元素为(因子名称, 是否降序)
                例如：[('composite_score', True), ('technical_score', True), ('fundamental_score', False)]
    
    Returns:
        排序后的股票列表
    """
    if factors is None:
        factors = [('composite_score', True)]
    
    def sort_key(stock):
        key_values = []
        for factor, reverse in factors:
            if factor == 'composite_score':
                value = stock.composite_score
            elif factor == 'technical_score':
                value = stock.technical_score
            elif factor == 'capital_score':
                value = stock.capital_score
            elif factor == 'fundamental_score':
                value = stock.fundamental_score
            elif factor == 'sentiment_score':
                value = stock.sentiment_score
            else:
                value = 0
            
            # 如果降序，取负值
            if reverse:
                key_values.append(-value)
            else:
                key_values.append(value)
        
        return tuple(key_values)
    
    return sorted(stocks, key=sort_key)
```

### 应用场景

评分排序结果用于：

1. **候选池排序**：按综合得分排序，优先选择高分股票
2. **策略选股**：根据策略需求选择特定因子排序
3. **风险控制**：结合多维度排序，避免单一维度偏差

## 🔗 相关章节

- **5.1 股票池管理**：了解股票池管理，为股票评分提供股票池
- **5.2 筛选规则**：了解筛选规则，筛选后的股票用于评分
- **第6章：因子库**：了解因子库，为股票评分提供因子数据
- **第7章：策略开发**：了解策略开发，股票评分结果用于策略选股
- **第10章：开发指南**：了解股票评分系统的开发规范

## 💡 关键要点

1. **多维度评分**：通过技术面、资金面、基本面、情绪面四个维度全面评估股票质量
2. **权重配置**：支持根据市场环境动态调整各维度权重
3. **主线融合**：结合主线热度，提升主线相关股票的评分
4. **评分排序**：支持按综合得分、因子得分、多维度排序

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了候选池构建模块的股票评分系统，通过技术面、资金面、基本面、情绪面四个维度对候选股票进行多因子评分，并计算综合评分。通过理解各维度评分方法、综合评分计算和评分排序方法，帮助开发者掌握如何构建全面的股票评分体系，为候选池排序和筛选提供准确依据。</p>
  
  <h3>下节预告</h3>
  <p>掌握了股票评分系统后，下一节将介绍MCP工具集成，包括知识库查询、数据收集工具等。通过理解MCP工具在候选池构建中的应用，帮助开发者掌握如何使用MCP工具提升候选池构建效率。</p>
  
  <a href="/ashare-book6/005_Chapter5_Candidate_Pool/5.4_MCP_Tool_Integration_CN" class="next-section">
    继续学习：5.4 MCP工具集成 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12

