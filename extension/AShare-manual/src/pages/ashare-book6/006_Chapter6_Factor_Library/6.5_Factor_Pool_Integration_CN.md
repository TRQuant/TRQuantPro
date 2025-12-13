---
title: "6.5 候选池集成"
description: "深入解析因子与候选池集成机制，包括因子评分、主线融合、综合评分系统和选股信号生成"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 🔗 6.5 候选池集成

> **核心摘要：**
> 
> 本节系统介绍TRQuant系统的因子与候选池集成机制，包括从候选池获取股票、计算多因子评分、融合主线评分和因子评分、生成综合评分和选股信号。通过理解因子评分系统、主线融合算法、综合评分计算和选股信号生成，帮助开发者掌握因子与候选池集成的核心实现，为构建完整的选股系统奠定基础。

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
  <div class="section-item" onclick="scrollToSection('section-6-5-1')">
    <h4>🏗️ 6.5.1 集成架构</h4>
    <p>集成设计、模块组成、数据流</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-6-5-2')">
    <h4>📊 6.5.2 因子评分系统</h4>
    <p>多因子评分、权重配置、评分计算</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-6-5-3')">
    <h4>🔗 6.5.3 主线融合</h4>
    <p>主线评分、融合算法、权重配置</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-6-5-4')">
    <h4>⚖️ 6.5.4 综合评分</h4>
    <p>综合评分计算、排名筛选、信号生成</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-6-5-5')">
    <h4>📈 6.5.5 选股信号</h4>
    <p>信号生成、信号强度、入选理由</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-6-5-6')">
    <h4>🛠️ 6.5.6 MCP工具使用</h4>
    <p>使用MCP工具查询候选池集成相关文档</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解集成架构**：掌握因子与候选池集成的设计架构和模块组成
- **掌握因子评分**：理解多因子评分、权重配置和评分计算
- **熟悉主线融合**：理解主线评分、融合算法和权重配置
- **了解综合评分**：掌握综合评分计算、排名筛选和信号生成
- **实现选股信号**：理解信号生成、信号强度和入选理由
- **使用MCP工具**：掌握使用MCP工具进行候选池集成相关研究

<h2 id="section-6-5-1">🏗️ 6.5.1 集成架构</h2>

因子与候选池集成是连接因子库和候选池模块的桥梁，实现从候选股票池到最终选股信号的完整流程。

### 设计原则

<div class="key-points">
  <div class="key-point">
    <h4>🔗 模块解耦</h4>
    <p>因子模块与候选池模块解耦，通过集成模块连接</p>
  </div>
  <div class="key-point">
    <h4>⚖️ 权重可配</h4>
    <p>因子权重和主线权重可配置，适应不同策略</p>
  </div>
  <div class="key-point">
    <h4>📊 多维度评分</h4>
    <p>综合考虑因子评分和主线评分，生成综合评分</p>
  </div>
  <div class="key-point">
    <h4>🎯 信号明确</h4>
    <p>生成清晰的选股信号，包含信号强度和入选理由</p>
  </div>
</div>

### 集成架构

```python
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from dataclasses import dataclass, field

from .factor_manager import FactorManager
from .factor_evaluator import FactorEvaluator
from .factor_storage import FactorStorage

@dataclass
class StockSignal:
    """股票信号"""
    
    code: str  # 股票代码
    name: str = ""  # 股票名称
    
    # 评分
    factor_score: float = 0.0  # 因子综合评分
    mainline_score: float = 0.0  # 主线评分
    combined_score: float = 0.0  # 综合评分
    
    # 因子明细
    factor_details: Dict[str, float] = field(default_factory=dict)
    
    # 分类
    period: str = "medium"  # 短/中/长期
    sector: str = ""  # 板块
    mainline: str = ""  # 所属主线
    
    # 信号强度
    signal_strength: str = "medium"  # strong/medium/weak
    entry_reason: str = ""  # 入选理由
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "factor_score": self.factor_score,
            "mainline_score": self.mainline_score,
            "combined_score": self.combined_score,
            "factor_details": self.factor_details,
            "period": self.period,
            "sector": self.sector,
            "mainline": self.mainline,
            "signal_strength": self.signal_strength,
            "entry_reason": self.entry_reason,
        }

class FactorPoolIntegration:
    """
    因子与候选池集成
    
    将因子模块与现有候选池模块对接，
    实现从候选股票池到最终选股信号的完整流程
    """
    
    # 默认因子权重配置
    DEFAULT_FACTOR_WEIGHTS = {
        "short": {
            "PriceMomentum": 0.3,
            "Reversal": 0.2,
            "CompositeFlow": 0.3,
            "RelativeStrength": 0.2,
        },
        "medium": {
            "CompositeValue": 0.25,
            "CompositeGrowth": 0.25,
            "CompositeMomentum": 0.25,
            "CompositeQuality": 0.25,
        },
        "long": {
            "CompositeValue": 0.35,
            "CompositeGrowth": 0.30,
            "CompositeQuality": 0.25,
            "PriceMomentum": 0.10,
        },
    }
    
    def __init__(
        self,
        jq_client=None,
        factor_manager: Optional[FactorManager] = None,
        factor_storage: Optional[FactorStorage] = None,
        mainline_weight: float = 0.4,
        factor_weight: float = 0.6,
    ):
        """
        初始化
        
        Args:
            jq_client: JQData客户端
            factor_manager: 因子管理器（可选，自动创建）
            factor_storage: 因子存储（可选，自动创建）
            mainline_weight: 主线评分权重
            factor_weight: 因子评分权重
        """
        self.jq_client = jq_client
        
        # 因子管理器
        if factor_manager:
            self.factor_manager = factor_manager
        else:
            self.factor_manager = FactorManager(jq_client=jq_client)
        
        # 因子存储
        if factor_storage:
            self.factor_storage = factor_storage
        else:
            self.factor_storage = FactorStorage()
        
        # 权重配置
        self.mainline_weight = mainline_weight
        self.factor_weight = factor_weight
```

<h2 id="section-6-5-2">📊 6.5.2 因子评分系统</h2>

因子评分系统负责计算每只股票的多因子综合评分。

### 多因子评分

```python
def calculate_factor_score(
    self,
    stocks: List[str],
    date: Union[str, datetime],
    period: str = "medium",
    factor_weights: Optional[Dict[str, float]] = None,
) -> pd.Series:
    """
    计算因子综合评分
    
    Args:
        stocks: 股票列表
        date: 日期
        period: 投资周期（short/medium/long）
        factor_weights: 因子权重（可选，使用默认权重）
    
    Returns:
        pd.Series: 因子综合评分（index为股票代码）
    """
    if factor_weights is None:
        factor_weights = self.DEFAULT_FACTOR_WEIGHTS.get(period, {})
    
    if not factor_weights:
        logger.warning(f"未找到周期 {period} 的因子权重配置")
        return pd.Series(index=stocks, dtype=float)
    
    # 计算各因子值
    factor_results = {}
    for factor_name in factor_weights.keys():
        try:
            result = self.factor_manager.calculate_factor(
                factor_name, stocks, date
            )
            if result and not result.values.empty:
                factor_results[factor_name] = result.values
        except Exception as e:
            logger.warning(f"因子计算失败: {factor_name}, 错误: {e}")
            continue
    
    if not factor_results:
        logger.warning("所有因子计算失败")
        return pd.Series(index=stocks, dtype=float)
    
    # 对齐所有因子的股票列表
    all_stocks = set()
    for values in factor_results.values():
        all_stocks.update(values.index)
    
    # 构建因子值DataFrame
    factor_df = pd.DataFrame(index=list(all_stocks))
    for name, values in factor_results.items():
        factor_df[name] = values
    
    # 标准化各因子
    for name in factor_df.columns:
        factor_df[name] = (factor_df[name] - factor_df[name].mean()) / factor_df[name].std()
    
    # 加权组合
    combined_score = pd.Series(0.0, index=factor_df.index)
    total_weight = 0
    
    for factor_name, weight in factor_weights.items():
        if factor_name in factor_df.columns:
            combined_score += factor_df[factor_name] * weight
            total_weight += weight
    
    # 归一化
    if total_weight > 0:
        combined_score = combined_score / total_weight
    
    # 重新索引到原始股票列表
    combined_score = combined_score.reindex(stocks)
    
    return combined_score
```

<h2 id="section-6-5-3">🔗 6.5.3 主线融合</h2>

主线融合将因子评分与主线评分结合，生成综合评分。

### 融合算法

```python
def process_candidate_pool(
    self,
    stocks: List[str],
    date: Union[str, datetime],
    period: str = "medium",
    mainline_scores: Optional[Dict[str, float]] = None,
    factor_weights: Optional[Dict[str, float]] = None,
    top_n: int = 30,
) -> List[StockSignal]:
    """
    处理候选池，生成选股信号
    
    Args:
        stocks: 候选股票列表
        date: 日期
        period: 投资周期
        mainline_scores: 主线评分字典 {股票代码: 主线评分}
        factor_weights: 因子权重（可选）
        top_n: 返回前N只股票
    
    Returns:
        List[StockSignal]: 选股信号列表
    """
    # 1. 计算因子评分
    factor_scores = self.calculate_factor_score(
        stocks, date, period, factor_weights
    )
    
    # 2. 获取主线评分（如果提供）
    if mainline_scores is None:
        mainline_scores = {}
    
    # 3. 计算综合评分
    combined_scores = pd.Series(0.0, index=stocks)
    
    for stock in stocks:
        factor_score = factor_scores.get(stock, 0.0)
        mainline_score = mainline_scores.get(stock, 0.0)
        
        # 融合评分
        combined_score = (
            factor_score * self.factor_weight +
            mainline_score * self.mainline_weight
        )
        
        combined_scores[stock] = combined_score
    
    # 4. 排序并选择前N只
    top_stocks = combined_scores.nlargest(top_n)
    
    # 5. 生成选股信号
    signals = []
    for stock, combined_score in top_stocks.items():
        factor_score = factor_scores.get(stock, 0.0)
        mainline_score = mainline_scores.get(stock, 0.0)
        
        # 获取因子明细
        factor_details = {}
        for factor_name in factor_weights or {}:
            try:
                result = self.factor_manager.calculate_factor(
                    factor_name, [stock], date
                )
                if result and not result.values.empty:
                    factor_details[factor_name] = result.values.iloc[0]
            except:
                pass
        
        # 确定信号强度
        if combined_score > 0.8:
            signal_strength = "strong"
        elif combined_score > 0.5:
            signal_strength = "medium"
        else:
            signal_strength = "weak"
        
        # 生成入选理由
        entry_reason = self._generate_entry_reason(
            stock, factor_score, mainline_score, factor_details
        )
        
        signal = StockSignal(
            code=stock,
            factor_score=factor_score,
            mainline_score=mainline_score,
            combined_score=combined_score,
            factor_details=factor_details,
            period=period,
            signal_strength=signal_strength,
            entry_reason=entry_reason,
        )
        
        signals.append(signal)
    
    return signals

def _generate_entry_reason(
    self,
    stock: str,
    factor_score: float,
    mainline_score: float,
    factor_details: Dict[str, float]
) -> str:
    """
    生成入选理由
    
    Args:
        stock: 股票代码
        factor_score: 因子评分
        mainline_score: 主线评分
        factor_details: 因子明细
    
    Returns:
        str: 入选理由
    """
    reasons = []
    
    if factor_score > 0.7:
        reasons.append("因子评分优秀")
    
    if mainline_score > 0.7:
        reasons.append("主线契合度高")
    
    # 找出表现最好的因子
    if factor_details:
        best_factor = max(factor_details.items(), key=lambda x: abs(x[1]))
        reasons.append(f"{best_factor[0]}因子表现突出")
    
    if not reasons:
        reasons.append("综合评分较高")
    
    return "；".join(reasons)
```

<h2 id="section-6-5-4">⚖️ 6.5.4 综合评分</h2>

综合评分是因子评分和主线评分的加权组合。

### 评分计算

综合评分计算公式：

```
综合评分 = 因子评分 × 因子权重 + 主线评分 × 主线权重
```

其中：
- **因子权重**：默认0.6，可配置
- **主线权重**：默认0.4，可配置
- **权重归一化**：确保因子权重 + 主线权重 = 1.0

<h2 id="section-6-5-5">📈 6.5.5 选股信号</h2>

选股信号包含股票代码、评分、信号强度、入选理由等信息。

### 信号生成

选股信号生成流程：

1. **计算因子评分**：使用多因子加权组合
2. **获取主线评分**：从主线识别模块获取
3. **计算综合评分**：融合因子评分和主线评分
4. **排序筛选**：按综合评分排序，选择前N只
5. **生成信号**：为每只股票生成选股信号

### 信号强度

信号强度根据综合评分确定：

- **strong**：综合评分 > 0.8
- **medium**：综合评分 > 0.5
- **weak**：综合评分 ≤ 0.5

<h2 id="section-6-5-6">🛠️ 6.5.6 MCP工具使用</h2>

候选池集成模块与MCP工具集成，支持知识库查询等功能。

### KB MCP Server工具

#### kb.query

查询知识库，获取候选池集成相关的文档和代码：

```python
# 查询候选池集成相关的知识
results = mcp_client.call_tool(
    "kb.query",
    {
        "query": "因子评分 主线融合 综合评分 选股信号",
        "collection": "manual_kb",
        "top_k": 5
    }
)
```

## 🔗 相关章节

- **第4章：投资主线识别** - 主线识别结果为候选池集成提供主线评分
- **第5章：候选池构建** - 候选池为因子计算提供股票列表
- **第6章：因子库** - 了解因子库模块的整体设计
- **第6.1节：因子计算** - 因子计算为候选池集成提供因子值
- **第6.2节：因子管理** - 因子管理为候选池集成提供因子列表
- **第6.3节：因子优化** - 因子优化结果用于候选池集成的权重配置
- **第7章：策略开发** - 选股信号用于策略生成
- **第10章：开发指南** - 了解候选池集成模块的开发规范

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了因子与候选池的集成机制，包括因子评分、主线融合、综合评分和选股信号生成。通过理解因子与候选池的集成，帮助开发者掌握如何将因子库与候选池模块有机结合，实现完整的选股流程，为策略生成提供高质量的股票候选池。</p>
  
  <h3>下节预告</h3>
  <p>掌握了因子库模块后，下一章将介绍策略开发模块，包括策略模板管理、策略生成器和策略规范化器。通过理解策略开发的核心实现，帮助开发者掌握如何构建专业级的策略开发系统。</p>
  
  <a href="/ashare-book6/007_Chapter7_Strategy_Development/007_Chapter7_Strategy_Development_CN" class="next-section">
    继续学习：第7章：策略开发 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12

