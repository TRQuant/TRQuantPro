"""
股票池构建模块

完整流程位置：
    五维量化 → 综合评分 → 主线识别 → 【候选池构建】→ 因子开发 → 策略生成 → 回测验证 → 实盘交易

三层数据保障架构：
    一级：实时API层（AKShare）
    二级：缓存层（JSON/MongoDB）
    三级：机构级数据源（JQData预留）

模块功能：
    1. 从主线识别结果提取强势股（与前置模块衔接）
    2. 全市场技术扫描发现独立强势股
    3. 整合外部筛选器（券商金股、GuruFocus）
    4. Fallback选股（龙头股+龙虎榜+涨停板）
    5. 按短中长期分类管理
    6. 输出标准化股票池（供后续因子开发和策略模块使用）
"""

from .models import StockPoolItem, StockPool, TradeSignal
from .pool_manager import StockPoolManager
from .selectors import (
    MainlineSelector,
    TechBreakoutScanner,
    PeriodSelector,
    ExternalDataParser
)
from .fallback_selector import FallbackSelector, build_fallback_pool, get_available_leaders
from .data_layer import (
    CacheManager, ThemeDataManager, SectorMemberCache,
    DataSourceStatus, get_cache_manager, get_theme_manager,
    get_sector_cache, get_jqdata_provider
)

__all__ = [
    # 数据模型
    'StockPoolItem',
    'StockPool',
    'TradeSignal',
    # 核心管理器
    'StockPoolManager',
    # 筛选器
    'MainlineSelector',
    'TechBreakoutScanner',
    'PeriodSelector',
    'ExternalDataParser',
    # Fallback
    'FallbackSelector',
    'build_fallback_pool',
    'get_available_leaders',
    # 数据层
    'CacheManager',
    'ThemeDataManager',
    'SectorMemberCache',
    'DataSourceStatus',
    'get_cache_manager',
    'get_theme_manager',
    'get_sector_cache',
    'get_jqdata_provider',
]

