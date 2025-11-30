# -*- coding: utf-8 -*-
"""
A股主线识别模块

参考PandaAI和机构级量化平台架构：
1. 真实数据源接入（AKShare/MongoDB）
2. 多维度分析引擎
3. Cursor IDE集成
4. 可视化工作流

使用方式：
    from markets.ashare.mainline import (
        MainlineAnalysisEngine,
        RealDataFetcher,
        generate_analysis_prompt,
    )
    
    # 运行分析
    engine = MainlineAnalysisEngine()
    result = engine.run_full_analysis()
    
    # 或直接生成Cursor Prompt
    prompt = generate_analysis_prompt()
"""

from .engine import AShareMainlineEngine
from .real_data_fetcher import RealDataFetcher, real_data_fetcher, DataFetchResult
from .analysis_engine import MainlineAnalysisEngine, MainlineResult, analysis_engine
from .cursor_integration import (
    CursorIntegration,
    generate_analysis_prompt,
    quick_analysis,
    strategy_prompt,
)

__all__ = [
    # 主线引擎
    'AShareMainlineEngine',
    'MainlineAnalysisEngine',
    'MainlineResult',
    'analysis_engine',
    
    # 数据获取
    'RealDataFetcher',
    'real_data_fetcher',
    'DataFetchResult',
    
    # Cursor集成
    'CursorIntegration',
    'generate_analysis_prompt',
    'quick_analysis',
    'strategy_prompt',
]


