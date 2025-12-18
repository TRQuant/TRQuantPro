# -*- coding: utf-8 -*-
"""
策略模板模块
===========
提供多种预定义策略模板，支持多平台导出
"""

# V2 版本（推荐）
from core.templates.strategy_templates_v2 import (
    StrategyTemplateV2,
    StrategyFactory,
    Platform,
    StrategyCategory,
    ParamSpec,
    MomentumTemplateV2,
    MeanReversionTemplateV2,
    RotationTemplateV2,
    create_strategy,
    list_strategies,
)

# V1 版本（兼容）
from core.templates.strategy_templates import (
    StrategyTemplate,
    MomentumTemplate,
    ValueTemplate,
    TrendTemplate,
    MultiFactorTemplate,
    get_template,
)

# 兼容函数
def get_any_template(name: str):
    """获取任意模板（V1或V2）"""
    try:
        return create_strategy(name)
    except:
        pass
    try:
        return get_template(name)
    except:
        pass
    return MultiFactorTemplate()


def list_templates():
    """列出V1模板"""
    return ["momentum", "value", "trend", "multi_factor"]


def list_advanced_templates():
    """列出V2高级模板"""
    try:
        return list_strategies()
    except:
        return ["momentum_v2", "mean_reversion_v2", "rotation_v2"]


def get_all_template_info():
    """获取所有模板信息"""
    templates = []
    
    # V1模板
    for name in list_templates():
        templates.append({
            "name": name,
            "version": "v1",
            "description": f"{name}策略模板"
        })
    
    # V2模板
    for name in list_advanced_templates():
        templates.append({
            "name": name,
            "version": "v2",
            "description": f"{name}高级策略模板"
        })
    
    return templates


__all__ = [
    # V2
    "StrategyTemplateV2", "StrategyFactory", "Platform", "StrategyCategory",
    "ParamSpec", "MomentumTemplateV2", "MeanReversionTemplateV2", "RotationTemplateV2",
    "create_strategy", "list_strategies",
    # V1
    "StrategyTemplate", "MomentumTemplate", "ValueTemplate", "TrendTemplate",
    "MultiFactorTemplate", "get_template",
    # 兼容
    "get_any_template", "list_templates", "list_advanced_templates", "get_all_template_info",
]
