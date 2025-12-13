---
title: "4.1 主线评分"
description: "深入解析主线评分机制，包括六维度评分体系、因子评分方法、综合评分计算和评分等级划分"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 📊 4.1 主线评分

> **核心摘要：**
> 
> 本节系统介绍TRQuant系统的主线评分机制，包括六维度评分体系（政策支持度、资金认可度、产业景气度、技术形态度、估值合理度、前瞻领先度）、因子评分方法、综合评分计算和评分等级划分。通过理解各维度的因子构成、评分计算方法、权重配置和综合评分算法，帮助开发者掌握主线评分的核心实现，为构建专业级的主线评分系统奠定基础。

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
  <div class="section-item" onclick="scrollToSection('section-4-1-1')">
    <h4>📊 4.1.1 六维度评分体系</h4>
    <p>政策支持度、资金认可度、产业景气度、技术形态度、估值合理度、前瞻领先度</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-4-1-2')">
    <h4>🔢 4.1.2 因子评分方法</h4>
    <p>因子原始值获取、标准化处理、阈值判断、因子得分计算</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-4-1-3')">
    <h4>⚖️ 4.1.3 综合评分计算</h4>
    <p>维度得分计算、权重配置、加权平均、综合得分计算</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-4-1-4')">
    <h4>📈 4.1.4 评分等级划分</h4>
    <p>评分等级定义、投资建议生成、风险提示生成</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-4-1-5')">
    <h4>🔄 4.1.5 动态权重调整</h4>
    <p>市场环境感知、权重动态调整、历史回测优化</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-4-1-6')">
    <h4>🛠️ 4.1.6 MCP工具使用</h4>
    <p>使用MCP工具查询评分相关文档、收集研究资料</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解六维度体系**：掌握六个评分维度的构成、因子配置和权重设置
- **掌握因子评分**：理解因子原始值获取、标准化处理、阈值判断和得分计算
- **熟悉综合评分**：理解维度得分计算、权重配置、加权平均和综合得分算法
- **了解等级划分**：掌握评分等级定义、投资建议生成和风险提示生成
- **实现动态调整**：理解市场环境感知、权重动态调整和历史回测优化
- **使用MCP工具**：掌握使用MCP工具进行评分相关研究

<h2 id="section-4-1-1">📊 4.1.1 六维度评分体系</h2>

主线评分采用六维度评分体系，参考行业先进水平（华泰、中金等券商研究框架），确保评分的专业性和全面性。

### 设计原则

<div class="key-points">
  <div class="key-point">
    <h4>📊 多维度综合</h4>
    <p>综合考虑政策、资金、产业、技术、估值、前瞻六个维度</p>
  </div>
  <div class="key-point">
    <h4>⚖️ 权重可配置</h4>
    <p>各维度权重可配置，适应不同市场环境</p>
  </div>
  <div class="key-point">
    <h4>🔢 因子可扩展</h4>
    <p>每个维度包含多个因子，因子可扩展和调整</p>
  </div>
  <div class="key-point">
    <h4>📈 动态调整</h4>
    <p>根据市场环境动态调整权重和阈值</p>
  </div>
</div>

### 维度配置

六维度评分体系的配置如下：

```python
SCORING_CONFIG = {
    # 维度权重配置（参考中金、华泰多因子框架）
    "dimension_weights": {
        "policy": 0.20,       # 政策支持度
        "capital": 0.25,      # 资金认可度
        "industry": 0.20,     # 产业景气度
        "technical": 0.15,    # 技术形态度
        "valuation": 0.10,    # 估值合理度
        "foresight": 0.10,    # 前瞻领先度
    },
    # ... 各维度因子配置
}
```

### 维度1：政策支持度（Policy）

政策支持度评估主线的政策支持力度，权重20%。

**因子构成**：

| 因子名称 | 权重 | 数据来源 | 计算方法 | 阈值（高/中/低） |
|---------|------|---------|---------|----------------|
| policy_mention_freq | 0.30 | 政策文件/新闻 | 近30天政策提及次数，标准化到0-100 | 10/5/2 |
| policy_strength | 0.35 | 政策文件分析 | 政策级别×支持方向，1-5分制 | 4/3/2 |
| policy_continuity | 0.20 | 历史政策分析 | 连续支持月数/预期持续时间 | 12/6/3 |
| policy_implementation | 0.15 | 执行情况跟踪 | 已落地措施数/计划措施数 | 0.8/0.5/0.3 |

**实现示例**：

```python
def calculate_policy_score(policy_data: Dict[str, float]) -> DimensionScore:
    """
    计算政策支持度得分
    
    Args:
        policy_data: 政策数据字典
            {
                "policy_mention_freq": 8,      # 政策提及频率
                "policy_strength": 4,          # 政策支持力度
                "policy_continuity": 12,       # 政策持续性
                "policy_implementation": 0.7   # 政策落地进度
            }
    
    Returns:
        DimensionScore: 政策支持度得分
    """
    factors = []
    total_score = 0.0
    
    # 因子1：政策提及频率
    mention_freq = policy_data.get("policy_mention_freq", 0)
    mention_score = min(100, mention_freq * 10)  # 标准化到0-100
    factor1 = FactorScore(
        name="policy_mention_freq",
        raw_value=mention_freq,
        normalized_score=mention_score,
        weight=0.30,
        weighted_score=mention_score * 0.30,
        data_source="政策文件/新闻",
        calculation_method="近30天政策提及次数，标准化到0-100",
        confidence=0.9
    )
    factors.append(factor1)
    total_score += factor1.weighted_score
    
    # 因子2：政策支持力度
    policy_strength = policy_data.get("policy_strength", 0)
    strength_score = (policy_strength / 5.0) * 100  # 1-5分制转0-100
    factor2 = FactorScore(
        name="policy_strength",
        raw_value=policy_strength,
        normalized_score=strength_score,
        weight=0.35,
        weighted_score=strength_score * 0.35,
        data_source="政策文件分析",
        calculation_method="政策级别×支持方向，1-5分制",
        confidence=0.85
    )
    factors.append(factor2)
    total_score += factor2.weighted_score
    
    # 因子3：政策持续性
    policy_continuity = policy_data.get("policy_continuity", 0)
    continuity_score = min(100, (policy_continuity / 12.0) * 100)  # 12个月为满分
    factor3 = FactorScore(
        name="policy_continuity",
        raw_value=policy_continuity,
        normalized_score=continuity_score,
        weight=0.20,
        weighted_score=continuity_score * 0.20,
        data_source="历史政策分析",
        calculation_method="连续支持月数/预期持续时间",
        confidence=0.8
    )
    factors.append(factor3)
    total_score += factor3.weighted_score
    
    # 因子4：政策落地进度
    implementation = policy_data.get("policy_implementation", 0)
    implementation_score = implementation * 100  # 0-1转0-100
    factor4 = FactorScore(
        name="policy_implementation",
        raw_value=implementation,
        normalized_score=implementation_score,
        weight=0.15,
        weighted_score=implementation_score * 0.15,
        data_source="执行情况跟踪",
        calculation_method="已落地措施数/计划措施数",
        confidence=0.75
    )
    factors.append(factor4)
    total_score += factor4.weighted_score
    
    # 确定评分等级
    level = ScoreLevel.VERY_HIGH if total_score >= 90 else \
            ScoreLevel.HIGH if total_score >= 75 else \
            ScoreLevel.MEDIUM if total_score >= 60 else \
            ScoreLevel.LOW if total_score >= 40 else \
            ScoreLevel.VERY_LOW
    
    return DimensionScore(
        dimension="policy",
        factors=factors,
        total_score=total_score,
        weight=0.20,
        weighted_score=total_score * 0.20,
        level=level,
        interpretation=f"政策支持度得分{total_score:.2f}，{level.value}"
    )
```

### 维度2：资金认可度（Capital）

资金认可度评估资金流向主线的强度，权重25%。

**因子构成**：

| 因子名称 | 权重 | 数据来源 | 计算方法 | 阈值（高/中/低） |
|---------|------|---------|---------|----------------|
| northbound_flow | 0.25 | 沪深港通数据 | 20日北向净流入/板块流通市值 | 0.02/0.01/0.005 |
| main_force_flow | 0.25 | 东方财富资金流向 | 5日主力净流入/板块成交额 | 0.15/0.08/0.03 |
| institutional_holding | 0.20 | 基金/保险持仓 | 季度机构持仓变化率 | 0.10/0.05/0.02 |
| margin_trading | 0.15 | 交易所两融数据 | 20日融资余额变化率 | 0.10/0.05/0.02 |
| etf_flow | 0.15 | ETF份额变化 | 20日ETF份额变化率 | 0.08/0.04/0.02 |

### 维度3：产业景气度（Industry）

产业景气度评估相关行业的景气程度，权重20%。

**因子构成**：

| 因子名称 | 权重 | 数据来源 | 计算方法 | 阈值（高/中/低） |
|---------|------|---------|---------|----------------|
| revenue_growth | 0.25 | 上市公司财报 | 行业整体营收同比增速 | 0.20/0.10/0.05 |
| profit_growth | 0.25 | 上市公司财报 | 行业整体净利润同比增速 | 0.25/0.15/0.08 |
| order_backlog | 0.20 | 上市公司财报 | 合同负债同比增速 | 0.30/0.15/0.05 |
| capacity_utilization | 0.15 | 行业协会/统计局 | 产能利用率水平 | 0.85/0.75/0.65 |
| price_trend | 0.15 | 行业价格指数 | 产品价格同比变化 | 0.10/0.05/0.00 |

### 维度4：技术形态度（Technical）

技术形态度评估技术形态的强度，权重15%。

**因子构成**：

| 因子名称 | 权重 | 数据来源 | 计算方法 | 阈值（高/中/低） |
|---------|------|---------|---------|----------------|
| trend_strength | 0.30 | 行情数据计算 | ADX指标，>25为强趋势 | 35/25/15 |
| ma_alignment | 0.25 | 行情数据计算 | MA5>MA10>MA20>MA60得分 | 4/3/2 |
| volume_price | 0.20 | 行情数据计算 | 上涨放量/下跌缩量程度 | 0.8/0.6/0.4 |
| breakout_signal | 0.15 | 行情数据计算 | 近期突破关键位置次数 | 3/2/1 |
| rsi_macd | 0.10 | 行情数据计算 | RSI+MACD综合得分 | 70/50/30 |

### 维度5：估值合理度（Valuation）

估值合理度评估相关股票的估值水平，权重10%。

**因子构成**：

| 因子名称 | 权重 | 数据来源 | 计算方法 | 阈值（低/中/高） | 反向 |
|---------|------|---------|---------|----------------|------|
| pe_percentile | 0.35 | 行情数据计算 | 当前PE在5年历史分位 | 0.30/0.50/0.70 | 是 |
| pb_percentile | 0.25 | 行情数据计算 | 当前PB在5年历史分位 | 0.30/0.50/0.70 | 是 |
| peg_ratio | 0.25 | 财报+预期 | PE/预期盈利增速 | 0.8/1.2/2.0 | 是 |
| dividend_yield | 0.15 | 财报数据 | 近12个月股息/股价 | 0.03/0.02/0.01 | 否 |

**注意**：估值因子中，PE、PB、PEG为反向指标（越低越好），需要反向处理。

### 维度6：前瞻领先度（Foresight）

前瞻领先度评估主线的前瞻性，权重10%。

**因子构成**：

| 因子名称 | 权重 | 数据来源 | 计算方法 | 阈值（高/中/低） |
|---------|------|---------|---------|----------------|
| leading_indicator | 0.30 | 宏观先行指标 | PMI新订单-产成品库存 | 5/2/0 |
| catalyst_density | 0.25 | 事件日历 | 未来30天重要事件数 | 5/3/1 |
| consensus_revision | 0.25 | 分析师预期 | 近30天EPS预期调整幅度 | 0.05/0.02/0.00 |
| global_trend | 0.20 | 海外市场/研报 | 全球同行业表现相关性 | 0.7/0.5/0.3 |

<h2 id="section-4-1-2">🔢 4.1.2 因子评分方法</h2>

因子评分是维度评分的基础，需要将原始值标准化到0-100分。

### 标准化方法

因子标准化采用阈值分段线性映射：

```python
def normalize_factor_value(
    raw_value: float,
    thresholds: Dict[str, float],
    inverse: bool = False
) -> float:
    """
    标准化因子值到0-100分
    
    **设计原理**：
    - **分段线性映射**：使用阈值分段，每段内线性插值
    - **阈值设计**：高/中/低三个阈值，对应100/60/30分
    - **反向支持**：支持正向指标（越大越好）和反向指标（越小越好）
    
    **为什么这样设计**：
    1. **直观性**：阈值分段比连续函数更直观，便于理解和调优
    2. **灵活性**：不同因子可以使用不同阈值，适应不同分布
    3. **鲁棒性**：分段线性映射对异常值不敏感，比非线性映射更稳定
    
    **阈值设计**：
    - **高阈值**：对应100分，表示优秀水平
    - **中阈值**：对应60分，表示中等水平
    - **低阈值**：对应30分，表示较差水平
    - **分段插值**：阈值之间线性插值，保证连续性
    
    **替代方案对比**：
    - **方案A：Z-score标准化**
      - 优点：统计意义明确
      - 缺点：需要历史数据，对异常值敏感
    - **方案B：分位数映射**
      - 优点：自适应，不依赖阈值
      - 缺点：需要大量历史数据，计算复杂
    - **当前方案：阈值分段线性映射**
      - 优点：直观、灵活、鲁棒
      - 缺点：需要人工设定阈值
    
    **使用场景**：
    - 主线评分时，将不同量纲的因子值标准化到统一尺度
    - 因子组合时，需要统一量纲
    - 因子评价时，需要比较不同因子的表现
    
    Args:
        raw_value: 原始值
        thresholds: 阈值字典 {"high": 高阈值, "medium": 中阈值, "low": 低阈值}
        inverse: 是否反向（越低越好）
    
    Returns:
        标准化得分（0-100）
    """
    if inverse:
        # 设计原理：反向指标处理
        # 原因：某些因子（如PE、PB）越低越好，需要反向评分
        # 反向指标：值越小，得分越高
        if raw_value <= thresholds["low"]:
            return 100
        elif raw_value <= thresholds["medium"]:
            # 设计原理：线性插值
            # 原因：保证连续性，避免跳跃
            # 线性插值：low->100, medium->60
            return 100 - (raw_value - thresholds["low"]) / \
                   (thresholds["medium"] - thresholds["low"]) * 40
        elif raw_value <= thresholds["high"]:
            # 线性插值：medium->60, high->30
            return 60 - (raw_value - thresholds["medium"]) / \
                   (thresholds["high"] - thresholds["medium"]) * 30
        else:
            # 设计原理：超过高阈值时得分递减
            # 原因：避免极端值获得过高分数
            return max(0, 30 - (raw_value - thresholds["high"]) * 10)
    else:
        # 设计原理：正向指标处理
        # 原因：大多数因子（如增长率、收益率）越大越好
        # 正向指标：值越大，得分越高
        if raw_value >= thresholds["high"]:
            return 100
        elif raw_value >= thresholds["medium"]:
            # 线性插值：medium->60, high->100
            return 60 + (raw_value - thresholds["medium"]) / \
                   (thresholds["high"] - thresholds["medium"]) * 40
        elif raw_value >= thresholds["low"]:
            # 线性插值：low->30, medium->60
            return 30 + (raw_value - thresholds["low"]) / \
                   (thresholds["medium"] - thresholds["low"]) * 30
        else:
            # 低于低阈值，得分递减
            return max(0, 30 - (thresholds["low"] - raw_value) * 10)
```

### 因子得分计算

```python
def calculate_factor_score(
    factor_name: str,
    raw_value: float,
    factor_config: Dict
) -> FactorScore:
    """
    计算因子得分
    
    Args:
        factor_name: 因子名称
        raw_value: 原始值
        factor_config: 因子配置
    
    Returns:
        FactorScore: 因子得分
    """
    thresholds = factor_config["thresholds"]
    inverse = factor_config.get("inverse", False)
    weight = factor_config["weight"]
    
    # 标准化得分
    normalized_score = normalize_factor_value(raw_value, thresholds, inverse)
    
    # 加权得分
    weighted_score = normalized_score * weight
    
    # 计算置信度（基于数据质量）
    confidence = calculate_confidence(factor_config)
    
    return FactorScore(
        name=factor_name,
        raw_value=raw_value,
        normalized_score=normalized_score,
        weight=weight,
        weighted_score=weighted_score,
        data_source=factor_config["data_source"],
        calculation_method=factor_config["calculation"],
        confidence=confidence
    )
```

<h2 id="section-4-1-3">⚖️ 4.1.3 综合评分计算</h2>

综合评分通过加权平均各维度得分得到。

### 维度得分计算

```python
def calculate_dimension_score(
    dimension_name: str,
    dimension_data: Dict[str, float],
    dimension_weight: float
) -> DimensionScore:
    """
    计算维度得分
    
    Args:
        dimension_name: 维度名称
        dimension_data: 维度数据字典
        dimension_weight: 维度权重
    
    Returns:
        DimensionScore: 维度得分
    """
    factors = []
    total_score = 0.0
    
    # 获取维度因子配置
    factor_configs = SCORING_CONFIG[f"{dimension_name}_factors"]
    
    # 计算各因子得分
    for factor_name, factor_config in factor_configs.items():
        raw_value = dimension_data.get(factor_name, 0)
        factor_score = calculate_factor_score(
            factor_name, raw_value, factor_config
        )
        factors.append(factor_score)
        total_score += factor_score.weighted_score
    
    # 确定评分等级
    level = get_score_level(total_score)
    
    return DimensionScore(
        dimension=dimension_name,
        factors=factors,
        total_score=total_score,
        weight=dimension_weight,
        weighted_score=total_score * dimension_weight,
        level=level,
        interpretation=f"{dimension_name}得分{total_score:.2f}"
    )
```

### 综合得分计算

```python
class ScoringModel:
    """专业级评分模型"""
    
    def __init__(self, config: Dict = None):
        self.config = config or SCORING_CONFIG
        self.dimension_weights = self.config["dimension_weights"]
    
    def calculate_mainline_score(
        self,
        mainline_name: str,
        raw_data: Dict[str, Any],
        llm_analysis: Optional[str] = None
    ) -> MainlineScore:
        """
        计算主线综合评分
        
        Args:
            mainline_name: 主线名称
            raw_data: 原始数据，格式：
                {
                    "policy": {...},
                    "capital": {...},
                    "industry": {...},
                    "technical": {...},
                    "valuation": {...},
                    "foresight": {...},
                }
            llm_analysis: LLM分析结论
        
        Returns:
            MainlineScore: 综合评分结果
        """
        dimensions = []
        
        # 计算各维度得分
        for dim_name, dim_weight in self.dimension_weights.items():
            dim_data = raw_data.get(dim_name, {})
            dim_score = calculate_dimension_score(dim_name, dim_data, dim_weight)
            dimensions.append(dim_score)
        
        # 计算总分（加权平均）
        total_score = sum(d.weighted_score for d in dimensions)
        level = get_score_level(total_score)
        
        # 生成投资建议
        recommendation = self._generate_recommendation(total_score, dimensions)
        risk_warning = self._generate_risk_warning(dimensions)
        
        return MainlineScore(
            mainline_name=mainline_name,
            dimensions=dimensions,
            total_score=total_score,
            level=level,
            recommendation=recommendation,
            risk_warning=risk_warning,
            analysis_time=datetime.now(),
            llm_analysis=llm_analysis
        )
```

<h2 id="section-4-1-4">📈 4.1.4 评分等级划分</h2>

评分等级用于快速判断主线的投资价值。

### 等级定义

```python
class ScoreLevel(Enum):
    """评分等级"""
    VERY_HIGH = "very_high"    # 90-100：强烈推荐
    HIGH = "high"              # 75-89：推荐
    MEDIUM = "medium"          # 60-74：中性
    LOW = "low"                # 40-59：谨慎
    VERY_LOW = "very_low"      # 0-39：不推荐

def get_score_level(score: float) -> ScoreLevel:
    """根据得分确定等级"""
    if score >= 90:
        return ScoreLevel.VERY_HIGH
    elif score >= 75:
        return ScoreLevel.HIGH
    elif score >= 60:
        return ScoreLevel.MEDIUM
    elif score >= 40:
        return ScoreLevel.LOW
    else:
        return ScoreLevel.VERY_LOW
```

### 投资建议生成

```python
def _generate_recommendation(
    total_score: float,
    dimensions: List[DimensionScore]
) -> str:
    """
    生成投资建议
    
    Args:
        total_score: 综合得分
        dimensions: 各维度得分
    
    Returns:
        投资建议：strong_buy/buy/hold/reduce/avoid
    """
    if total_score >= 90:
        return "strong_buy"
    elif total_score >= 75:
        return "buy"
    elif total_score >= 60:
        return "hold"
    elif total_score >= 40:
        return "reduce"
    else:
        return "avoid"
```

### 风险提示生成

```python
def _generate_risk_warning(dimensions: List[DimensionScore]) -> str:
    """
    生成风险提示
    
    Args:
        dimensions: 各维度得分
    
    Returns:
        风险提示文本
    """
    warnings = []
    
    # 检查各维度风险
    for dim in dimensions:
        if dim.level == ScoreLevel.LOW or dim.level == ScoreLevel.VERY_LOW:
            warnings.append(f"{dim.dimension}得分较低（{dim.total_score:.1f}分）")
    
    if warnings:
        return "；".join(warnings)
    else:
        return "各维度得分均衡，风险可控"
```

<h2 id="section-4-1-5">🔄 4.1.5 动态权重调整</h2>

根据市场环境动态调整各维度权重，提高评分的适应性。

### 市场环境感知

```python
def adjust_weights_by_market_regime(
    market_regime: str,
    base_weights: Dict[str, float]
) -> Dict[str, float]:
    """
    根据市场状态调整权重
    
    Args:
        market_regime: 市场状态（risk_on/risk_off/neutral）
        base_weights: 基础权重
    
    Returns:
        调整后的权重
    """
    if market_regime == "risk_on":
        # 牛市：提高技术、资金权重，降低估值权重
        adjusted = base_weights.copy()
        adjusted["technical"] *= 1.2
        adjusted["capital"] *= 1.1
        adjusted["valuation"] *= 0.8
    elif market_regime == "risk_off":
        # 熊市：提高估值、政策权重，降低技术权重
        adjusted = base_weights.copy()
        adjusted["valuation"] *= 1.3
        adjusted["policy"] *= 1.1
        adjusted["technical"] *= 0.7
    else:
        # 震荡市：保持基础权重
        adjusted = base_weights.copy()
    
    # 归一化权重
    total = sum(adjusted.values())
    return {k: v / total for k, v in adjusted.items()}
```

<h2 id="section-4-1-6">🛠️ 4.1.6 MCP工具使用</h2>

主线评分模块与MCP工具集成，支持知识库查询、数据收集等功能。

### KB MCP Server工具

#### kb.query

查询知识库，获取主线评分相关的文档和代码：

```python
# 查询主线评分相关的知识
results = mcp_client.call_tool(
    "kb.query",
    {
        "query": "主线评分 多维度评分 因子评分方法",
        "collection": "manual_kb",
        "top_k": 5
    }
)
```

### Data Collector MCP工具

#### data_collector.crawl_web

爬取网页内容，收集主线评分相关的研究资料：

```python
# 爬取评分模型相关网页
content = mcp_client.call_tool(
    "data_collector.crawl_web",
    {
        "url": "https://example.com/scoring-model",
        "extract_text": True
    }
)
```

## 🔗 相关章节

- **第2章：数据源模块** - 了解数据获取机制，为主线评分提供数据支撑
- **第3章：市场分析模块** - 市场分析结果用于权重调整
- **第4章：投资主线识别** - 了解主线识别模块的整体设计
- **第4.2节：主线筛选** - 主线评分结果用于主线筛选
- **第5章：候选池构建** - 主线评分结果用于候选池构建
- **第6章：因子库** - 主线评分结果用于因子推荐
- **第10章：开发指南** - 了解主线评分模块的开发规范

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了主线评分功能，包括六维度评分体系、因子评分方法和综合评分计算。通过理解投资主线评分的核心技术，帮助开发者掌握如何全面评估投资主线的价值和潜力。</p>
  
  <h3>下节预告</h3>
  <p>掌握了主线评分方法后，下一节将介绍主线筛选，包括评分筛选、行业筛选、时间筛选的算法和实现。通过理解主线筛选的核心技术，帮助开发者掌握如何从众多主线中筛选出最有价值的投资主线。</p>
  
  <a href="/ashare-book6/004_Chapter4_Mainline_Identification/4.2_Mainline_Filtering_CN" class="next-section">
    继续学习：4.2 主线筛选 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
