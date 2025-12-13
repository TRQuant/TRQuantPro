---
title: "3.3 五维评分系统"
description: "详细介绍市场分析模块的五维评分系统，包括宏观、资金、行业、技术、估值五个维度的评分方法和综合评分计算"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
---

# 3.3 五维评分系统

## 概述

五维评分系统是市场分析模块的核心功能，通过综合评估**宏观、资金、行业、技术、估值**五个维度，为投资决策提供量化评分支持。

### 评分维度

1. **宏观维度** (20%权重) - 评估宏观经济环境
2. **资金维度** (25%权重) - 评估资金流向和资金面
3. **行业维度** (20%权重) - 评估行业景气度和成长性
4. **技术维度** (15%权重) - 评估技术形态和趋势
5. **估值维度** (20%权重) - 评估估值水平和性价比

### 综合评分

综合评分 = Σ(各维度评分 × 对应权重)

评分等级：
- **优秀** (≥80分)：投资价值高
- **良好** (60-79分)：投资价值中等
- **一般** (40-59分)：投资价值一般
- **较差** (<40分)：投资价值较低

---

## 1. 宏观维度评分

宏观维度评估宏观经济环境对市场的影响，包括GDP增速、CPI、PMI、货币政策等指标。

### 评分方法实现

<CodeFromFile
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_macro_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

### 评分标准

- **GDP增速** (30分)：5-7%为理想区间
- **CPI** (20分)：1.5-2.5%为理想区间
- **PMI** (25分)：≥50表示扩张
- **货币政策** (25分)：宽松>中性>紧缩

---

## 2. 资金维度评分

资金维度评估资金流向和资金面状况，包括主力资金、北向资金、融资融券、机构持仓等。

### 评分方法实现

<CodeFromFile
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_capital_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

### 评分标准

- **主力资金净流入** (40分)：净流入越大，评分越高
- **北向资金净流入** (25分)：反映外资态度
- **融资融券余额变化** (20分)：反映杠杆资金态度
- **机构持仓变化** (15分)：反映机构资金态度
- **连续流入天数** (加成)：连续流入天数越多，额外加分

---

## 3. 行业维度评分

行业维度评估行业景气度和成长性，包括收入增速、利润增速、行业PMI、政策支持等。

### 评分方法实现

<CodeFromFile
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_industry_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

### 评分标准

- **收入增速** (30分)：增速越高，评分越高
- **利润增速** (30分)：增速越高，评分越高
- **行业PMI** (25分)：≥50表示扩张
- **政策支持度** (15分)：政策支持越强，评分越高

---

## 4. 技术维度评分

技术维度评估技术形态和趋势强度，包括价格动量、成交量动量、趋势强度、突破信号等。

### 评分方法实现

<CodeFromFile
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_technical_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

### 评分标准

- **价格动量** (30分)：涨幅越大，评分越高
- **成交量动量** (25分)：量比越大，评分越高
- **趋势强度** (25分)：趋势越强，评分越高
- **突破信号** (20分)：出现突破信号，额外加分

---

## 5. 估值维度评分

估值维度评估估值水平和性价比，包括PE、PB及其历史分位数等。

### 评分方法实现

<CodeFromFile
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_score_valuation_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

### 评分标准

- **PE分位数** (30分)：分位数越低，估值越便宜，评分越高
- **PB分位数** (30分)：分位数越低，估值越便宜，评分越高
- **综合分位数** (20分)：综合考虑PE和PB的分位数

---

## 6. 综合评分计算

综合评分将五个维度的评分按权重加权求和，得到最终的综合评分。

### 综合评分实现

<CodeFromFile
  filePath="code_library/003_Chapter3_Market_Analysis/3.3/code_3_3_comprehensive_score.py"
  language="python"
  showDesignPrinciples="true"
/>

### 使用示例

```python
from code_library.003_Chapter3_Market_Analysis.3.3.code_3_3_comprehensive_score import calculate_comprehensive_score

# 准备各维度数据
macro_data = {
    'gdp_growth': 6.5,
    'cpi': 2.0,
    'pmi': 52.0,
    'monetary_policy': 'loose'
}

capital_data = {
    'main_force_net_inflow': 50000,
    'northbound_net_inflow': 20000,
    'margin_balance_change': 5.0,
    'institutional_holding_change': 3.0,
    'consecutive_inflow_days': 3
}

industry_data = {
    'revenue_growth': 15.0,
    'profit_growth': 25.0,
    'industry_pmi': 53.0,
    'policy_support': 0.8
}

technical_data = {
    'price_momentum': 12.0,
    'volume_momentum': 1.5,
    'trend_strength': 0.7,
    'breakout_signal': True
}

valuation_data = {
    'pe_ratio': 25.0,
    'pb_ratio': 3.0,
    'pe_percentile': 30.0,
    'pb_percentile': 35.0
}

# 计算综合评分
result = calculate_comprehensive_score(
    macro_data, capital_data, industry_data, 
    technical_data, valuation_data
)

print(f"综合评分: {result['comprehensive_score']}")
print(f"评分等级: {result['level']}")
```

---

## 总结

五维评分系统通过量化评估多个维度，为投资决策提供全面的参考依据。各维度权重可根据市场环境动态调整，以适应不同的投资策略和风险偏好。

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-13
