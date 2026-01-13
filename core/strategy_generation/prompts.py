#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
策略生成Prompt模板
==================

固定几类Prompt，而非自由对话
"""

from typing import Dict, Any, List


# 短线策略生成模板
SHORT_TERM_STRATEGY_TEMPLATE = """
基于以下市场状态和可用因子，生成短线策略：

## 市场状态
- **当前状态**: {market_regime}
- **情绪指标**: {sentiment_indicators}
- **资金流向**: {capital_flow}

## 可用因子
{available_factors}

## 资金结构
- **总资金**: {total_capital}
- **可用资金**: {available_capital}
- **当前仓位**: {current_position}

## 要求
1. **明确入场信号**: 基于因子组合，给出具体的入场条件
2. **明确出场信号**: 给出止盈和止损条件
3. **风险控制措施**: 仓位控制、止损止盈、时间限制
4. **适用区间说明**: 策略在什么市场状态下有效
5. **失败案例参考**: 参考相关失败案例，避免类似错误

## 输出格式
### 策略逻辑
[详细描述策略逻辑]

### 入场信号
[具体入场条件]

### 出场信号
[止盈和止损条件]

### 风险控制
[仓位、止损、时间限制等]

### 适用区间
[策略有效的市场状态]

### 风险声明
[潜在风险和注意事项]

### 失败案例参考
[相关失败案例和避免方法]
"""


# 趋势策略生成模板
TREND_STRATEGY_TEMPLATE = """
基于以下市场状态和可用因子，生成趋势跟随策略：

## 市场状态
- **当前状态**: {market_regime}
- **趋势方向**: {trend_direction}
- **趋势强度**: {trend_strength}

## 可用因子
{available_factors}

## 资金结构
- **总资金**: {total_capital}
- **可用资金**: {available_capital}
- **当前仓位**: {current_position}

## 要求
1. **趋势确认**: 如何确认趋势成立
2. **入场时机**: 趋势中的最佳入场点
3. **持仓管理**: 如何管理趋势持仓
4. **趋势结束判断**: 如何判断趋势结束
5. **风险控制**: 趋势反转时的应对

## 输出格式
### 策略逻辑
[详细描述趋势跟随策略逻辑]

### 趋势确认
[如何确认趋势成立]

### 入场时机
[趋势中的最佳入场点]

### 持仓管理
[如何管理趋势持仓]

### 趋势结束判断
[如何判断趋势结束]

### 风险控制
[趋势反转时的应对措施]

### 适用区间
[策略有效的市场状态]

### 风险声明
[潜在风险和注意事项]
"""


# 风控/减仓模板
RISK_CONTROL_TEMPLATE = """
基于以下市场状态，生成风控/减仓策略：

## 市场状态
- **当前状态**: {market_regime}
- **风险信号**: {risk_signals}
- **当前仓位**: {current_position}

## 风险指标
{risk_indicators}

## 要求
1. **风险识别**: 识别当前主要风险
2. **减仓方案**: 具体的减仓步骤和比例
3. **防御策略**: 减仓后的防御性策略
4. **重新入场条件**: 什么条件下可以重新入场

## 输出格式
### 风险识别
[当前主要风险]

### 减仓方案
[具体减仓步骤和比例]

### 防御策略
[减仓后的防御性策略]

### 重新入场条件
[什么条件下可以重新入场]

### 风险声明
[潜在风险和注意事项]
"""


# 情绪周期策略模板
SENTIMENT_CYCLE_STRATEGY_TEMPLATE = """
基于以下情绪周期状态，生成策略：

## 情绪周期状态
- **当前阶段**: {sentiment_phase}
- **情绪指标**: {sentiment_indicators}
- **资金流向**: {capital_flow}

## 可用因子
{available_factors}

## 要求
1. **阶段特征**: 当前情绪阶段的特征
2. **策略选择**: 适合当前阶段的策略类型
3. **因子选择**: 当前阶段有效的因子
4. **风险控制**: 当前阶段的风险控制措施
5. **阶段转换**: 如何判断阶段转换

## 输出格式
### 阶段特征
[当前情绪阶段的特征]

### 策略选择
[适合当前阶段的策略类型]

### 因子选择
[当前阶段有效的因子]

### 风险控制
[当前阶段的风险控制措施]

### 阶段转换判断
[如何判断阶段转换]

### 适用区间
[策略有效的情绪阶段]

### 风险声明
[潜在风险和注意事项]
"""


def get_strategy_prompt(
    template_type: str,
    **kwargs
) -> str:
    """
    获取策略生成Prompt
    
    Args:
        template_type: 模板类型 (short_term/trend/risk_control/sentiment_cycle)
        **kwargs: 模板参数
        
    Returns:
        填充后的Prompt字符串
    """
    templates = {
        "short_term": SHORT_TERM_STRATEGY_TEMPLATE,
        "trend": TREND_STRATEGY_TEMPLATE,
        "risk_control": RISK_CONTROL_TEMPLATE,
        "sentiment_cycle": SENTIMENT_CYCLE_STRATEGY_TEMPLATE
    }
    
    template = templates.get(template_type)
    if not template:
        raise ValueError(f"未知的模板类型: {template_type}")
    
    return template.format(**kwargs)


def generate_strategy_prompt(
    market_regime: str,
    available_factors: List[str],
    strategy_type: str = "short_term",
    **kwargs
) -> str:
    """
    生成策略Prompt（便捷函数）
    
    Args:
        market_regime: 市场状态
        available_factors: 可用因子列表
        strategy_type: 策略类型
        **kwargs: 其他参数
        
    Returns:
        填充后的Prompt字符串
    """
    # 格式化因子列表
    factors_text = "\n".join(f"- {f}" for f in available_factors)
    
    # 默认参数
    defaults = {
        "market_regime": market_regime,
        "available_factors": factors_text,
        "total_capital": kwargs.get("total_capital", "100万"),
        "available_capital": kwargs.get("available_capital", "50万"),
        "current_position": kwargs.get("current_position", "50%"),
        "sentiment_indicators": kwargs.get("sentiment_indicators", "待补充"),
        "capital_flow": kwargs.get("capital_flow", "待补充"),
        "trend_direction": kwargs.get("trend_direction", "待判断"),
        "trend_strength": kwargs.get("trend_strength", "待判断"),
        "risk_signals": kwargs.get("risk_signals", "待识别"),
        "risk_indicators": kwargs.get("risk_indicators", "待补充"),
        "sentiment_phase": kwargs.get("sentiment_phase", market_regime),
    }
    
    defaults.update(kwargs)
    
    return get_strategy_prompt(strategy_type, **defaults)
