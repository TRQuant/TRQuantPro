# -*- coding: utf-8 -*-
"""
TRQuant 插件系统
===============

借鉴VN.Py模块化设计

使用方式:
    from core.plugin import (
        PluginManager, 
        get_plugin_manager,
        register_plugin,
        PluginType,
        PluginInfo,
        BasePlugin,
        DataPlugin,
        StrategyPlugin,
        BrokerPlugin,
        VisualizationPlugin,
        AnalysisPlugin,
        RiskPlugin,
    )
"""

from .plugin_manager import (
    PluginManager,
    get_plugin_manager,
    register_plugin,
    PluginType,
    PluginStatus,
    PluginInfo,
    BasePlugin,
    DataPlugin,
    StrategyPlugin,
    BrokerPlugin,
    VisualizationPlugin,
    AnalysisPlugin,
    RiskPlugin,
)

__all__ = [
    "PluginManager",
    "get_plugin_manager",
    "register_plugin",
    "PluginType",
    "PluginStatus",
    "PluginInfo",
    "BasePlugin",
    "DataPlugin",
    "StrategyPlugin",
    "BrokerPlugin",
    "VisualizationPlugin",
    "AnalysisPlugin",
    "RiskPlugin",
]

