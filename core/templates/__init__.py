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

# 导出器
from core.templates.strategy_exporter import (
    StrategyExporter,
    export_strategy,
)

__all__ = [
    # V2 策略系统
    "StrategyTemplateV2",
    "StrategyFactory",
    "Platform",
    "StrategyCategory",
    "ParamSpec",
    "MomentumTemplateV2",
    "MeanReversionTemplateV2",
    "RotationTemplateV2",
    "create_strategy",
    "list_strategies",
    # V1 兼容
    "StrategyTemplate",
    "MomentumTemplate",
    "ValueTemplate",
    "TrendTemplate",
    "MultiFactorTemplate",
    "get_template",
    # 导出器
    "StrategyExporter",
    "export_strategy",
]
