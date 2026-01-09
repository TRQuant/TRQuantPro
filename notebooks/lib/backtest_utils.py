"""
回测结果工具模块
================

为Jupyter Notebook提供便捷的回测结果查询和管理功能。

功能:
- 列出回测结果
- 加载指定的回测结果
- 查找缓存结果
- 对比多个结果（可选）

使用方式:
    from notebooks.lib.backtest_utils import list_backtest_results, load_backtest_result
    
    # 列出最近的回测结果
    results = list_backtest_results(backtest_type='signal_phase1', limit=10)
    
    # 加载指定结果
    result = load_backtest_result(result_id)
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# 尝试导入MarketTrendStorage
try:
    from core.market_trend_storage import MarketTrendStorage
    STORAGE_AVAILABLE = True
except ImportError:
    STORAGE_AVAILABLE = False
    logger.warning("MarketTrendStorage不可用，回测结果工具功能受限")


def list_backtest_results(
    backtest_type: Optional[str] = None,
    limit: int = 10,
    sort_by: str = 'created_at'
) -> List[Dict[str, Any]]:
    """
    列出回测结果
    
    Args:
        backtest_type: 回测类型（如'signal_phase1', 'signal_phase2'），None表示所有类型
        limit: 返回结果数量限制
        sort_by: 排序字段（'created_at', 'start_date', 'duration_seconds'等）
        
    Returns:
        结果列表（包含元数据和摘要，不包含完整结果数据）
        
    Example:
        >>> results = list_backtest_results(backtest_type='signal_phase1', limit=5)
        >>> for r in results:
        ...     print(f"ID: {r['_id']}, 创建时间: {r['created_at']}, 准确率: {r['summary'].get('accuracy_5d', 0):.1f}%")
    """
    if not STORAGE_AVAILABLE:
        logger.warning("MarketTrendStorage不可用，无法列出回测结果")
        return []
    
    try:
        storage = MarketTrendStorage()
        if not storage.is_connected():
            logger.warning("MongoDB未连接，无法列出回测结果")
            return []
        
        results = storage.list_backtest_results(
            backtest_type=backtest_type,
            limit=limit,
            sort_by=sort_by
        )
        
        return results
        
    except Exception as e:
        logger.error(f"列出回测结果失败: {e}")
        return []


def load_backtest_result(result_id: str) -> Optional[Any]:
    """
    加载完整的回测结果
    
    Args:
        result_id: 结果ID（MongoDB _id的字符串形式）
        
    Returns:
        EnhancedBacktestResult对象或字典，失败返回None
        
    Example:
        >>> result = load_backtest_result('507f1f77bcf86cd799439011')
        >>> print(f"总信号数: {result.total_signals}")
        >>> print(f"准确率: {result.accuracy_5d:.1f}%")
    """
    if not STORAGE_AVAILABLE:
        logger.warning("MarketTrendStorage不可用，无法加载回测结果")
        return None
    
    try:
        storage = MarketTrendStorage()
        if not storage.is_connected():
            logger.warning("MongoDB未连接，无法加载回测结果")
            return None
        
        result = storage.load_backtest_result(result_id)
        return result
        
    except Exception as e:
        logger.error(f"加载回测结果失败: {e}")
        return None


def find_cached_result(
    config: Dict[str, Any],
    backtest_type: str
) -> Optional[Dict[str, Any]]:
    """
    查找缓存结果
    
    Args:
        config: 配置字典（包含start_date, end_date, sample_interval等）
        backtest_type: 回测类型（如'signal_phase1', 'signal_phase2'）
        
    Returns:
        缓存的文档（包含_id和摘要），未找到返回None
        
    Example:
        >>> config = {
        ...     'start_date': '2023-01-01',
        ...     'end_date': '2024-08-16',
        ...     'sample_interval': 5
        ... }
        >>> cached = find_cached_result(config, 'signal_phase1')
        >>> if cached:
        ...     print(f"找到缓存结果: {cached['_id']}")
        ...     result = load_backtest_result(cached['_id'])
    """
    if not STORAGE_AVAILABLE:
        logger.warning("MarketTrendStorage不可用，无法查找缓存")
        return None
    
    try:
        storage = MarketTrendStorage()
        if not storage.is_connected():
            logger.warning("MongoDB未连接，无法查找缓存")
            return None
        
        cached = storage.find_cached_backtest(config, backtest_type)
        return cached
        
    except Exception as e:
        logger.error(f"查找缓存失败: {e}")
        return None


def query_backtest_results(
    backtest_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    sort_by: str = 'created_at'
) -> List[Dict[str, Any]]:
    """
    查询回测结果（灵活查询接口）
    
    Args:
        backtest_type: 回测类型（可选）
        start_date: 开始日期（可选，用于过滤回测区间）
        end_date: 结束日期（可选，用于过滤回测区间）
        limit: 返回结果数量限制
        sort_by: 排序字段
        
    Returns:
        结果列表
        
    Example:
        >>> # 查询2023年的所有Phase 1回测
        >>> results = query_backtest_results(
        ...     backtest_type='signal_phase1',
        ...     start_date='2023-01-01',
        ...     end_date='2023-12-31',
        ...     limit=20
        ... )
    """
    if not STORAGE_AVAILABLE:
        logger.warning("MarketTrendStorage不可用，无法查询回测结果")
        return []
    
    try:
        storage = MarketTrendStorage()
        if not storage.is_connected():
            logger.warning("MongoDB未连接，无法查询回测结果")
            return []
        
        results = storage.query_backtest_results(
            backtest_type=backtest_type,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            sort_by=sort_by
        )
        
        return results
        
    except Exception as e:
        logger.error(f"查询回测结果失败: {e}")
        return []


def list_results_by_version(
    backtest_type: Optional[str] = None,
    algorithm_version: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    按版本列出回测结果
    
    Args:
        backtest_type: 回测类型（可选）
        algorithm_version: 算法版本（可选）
        limit: 返回结果数量限制
        
    Returns:
        结果列表（按创建时间排序）
        
    Example:
        >>> # 列出所有Phase 1的结果
        >>> results = list_results_by_version(backtest_type='signal_phase1')
        
        >>> # 列出特定版本的结果
        >>> results = list_results_by_version(
        ...     backtest_type='signal_phase1',
        ...     algorithm_version='v1a2b3c4d'
        ... )
    """
    if not STORAGE_AVAILABLE:
        logger.warning("MarketTrendStorage不可用，无法列出结果")
        return []
    
    try:
        storage = MarketTrendStorage()
        if not storage.is_connected():
            logger.warning("MongoDB未连接，无法列出结果")
            return []
        
        results = storage.list_results_by_version(
            backtest_type=backtest_type,
            algorithm_version=algorithm_version,
            limit=limit
        )
        
        return results
        
    except Exception as e:
        logger.error(f"列出结果失败: {e}")
        return []


def compare_versions(result_id1: str, result_id2: str) -> Optional[Dict[str, Any]]:
    """
    比较两个版本的回测结果
    
    Args:
        result_id1: 结果ID 1
        result_id2: 结果ID 2
        
    Returns:
        比较结果字典，失败返回None
        
    Example:
        >>> comparison = compare_versions(result_id1='...', result_id2='...')
        >>> print(f"5日准确率差异: {comparison['metrics_diff']['accuracy_5d']['diff']:.1f}%")
        >>> print(f"摘要: {comparison['summary']}")
    """
    if not STORAGE_AVAILABLE:
        logger.warning("MarketTrendStorage不可用，无法比较版本")
        return None
    
    try:
        storage = MarketTrendStorage()
        if not storage.is_connected():
            logger.warning("MongoDB未连接，无法比较版本")
            return None
        
        comparison = storage.compare_versions(result_id1, result_id2)
        return comparison
        
    except Exception as e:
        logger.error(f"比较版本失败: {e}")
        return None


def visualize_from_database(
    result_id: str,
    version: Optional[str] = None
):
    """
    从数据库加载结果并创建可视化对象
    
    Args:
        result_id: 结果ID（MongoDB _id的字符串形式）
        version: 版本标签（可选，用于过滤）
        
    Returns:
        BacktestVisualization实例
        
    Example:
        >>> from notebooks.lib.backtest_utils import visualize_from_database
        
        >>> # 从数据库加载并创建可视化对象
        >>> viz = visualize_from_database(result_id='507f1f77bcf86cd799439011')
        
        >>> # 生成图表
        >>> fig = viz.create_accuracy_heatmap()
        >>> fig.show()
    """
    if not STORAGE_AVAILABLE:
        raise ImportError("MarketTrendStorage不可用")
    
    try:
        from core.backtest_visualization import BacktestVisualization
        return BacktestVisualization.from_database(result_id, version=version)
    except Exception as e:
        logger.error(f"从数据库加载可视化失败: {e}")
        raise


def visualize_from_cache(
    config: Dict[str, Any],
    backtest_type: str,
    version: Optional[str] = None
):
    """
    从缓存加载结果并创建可视化对象
    
    Args:
        config: 配置字典
        backtest_type: 回测类型
        version: 算法版本（可选）
        
    Returns:
        BacktestVisualization实例，未找到返回None
        
    Example:
        >>> from notebooks.lib.backtest_utils import visualize_from_cache
        
        >>> config = {
        ...     'start_date': '2023-01-01',
        ...     'end_date': '2024-08-16',
        ...     'sample_interval': 5
        ... }
        >>> viz = visualize_from_cache(config, 'signal_phase1')
        >>> if viz:
        ...     fig = viz.create_accuracy_heatmap()
        ...     fig.show()
    """
    if not STORAGE_AVAILABLE:
        logger.warning("MarketTrendStorage不可用")
        return None
    
    try:
        from core.backtest_visualization import BacktestVisualization
        return BacktestVisualization.from_cache(config, backtest_type, version=version)
    except Exception as e:
        logger.error(f"从缓存加载可视化失败: {e}")
        return None


def format_backtest_summary(result_dict: Dict[str, Any]) -> str:
    """
    格式化回测结果摘要（用于显示）
    
    Args:
        result_dict: 结果字典（来自list_backtest_results或query_backtest_results）
        
    Returns:
        格式化的字符串
        
    Example:
        >>> results = list_backtest_results(limit=1)
        >>> if results:
        ...     print(format_backtest_summary(results[0]))
    """
    summary = result_dict.get('summary', {})
    backtest_type = result_dict.get('backtest_type', 'unknown')
    created_at = result_dict.get('created_at', '')
    result_id = result_dict.get('_id', '')
    
    lines = [
        f"回测类型: {backtest_type}",
        f"结果ID: {result_id}",
        f"创建时间: {created_at[:19] if created_at else 'N/A'}",
    ]
    
    # 添加版本信息
    algorithm_version = result_dict.get('algorithm_version')
    version_tag = result_dict.get('version_tag')
    if algorithm_version:
        lines.append(f"算法版本: {algorithm_version}")
    if version_tag:
        lines.append(f"版本标签: {version_tag}")
    migrated_from = result_dict.get('migrated_from')
    if migrated_from:
        lines.append(f"迁移来源: {migrated_from}")
    
    if summary:
        lines.append("\n关键指标:")
        if 'total_signals' in summary:
            lines.append(f"  总信号数: {summary['total_signals']}")
        if 'accuracy_5d' in summary:
            lines.append(f"  5日准确率: {summary['accuracy_5d']:.1f}%")
        if 'accuracy_20d' in summary:
            lines.append(f"  20日准确率: {summary['accuracy_20d']:.1f}%")
        if 'accuracy_60d' in summary:
            lines.append(f"  60日准确率: {summary['accuracy_60d']:.1f}%")
        if 'duration_seconds' in summary:
            lines.append(f"  耗时: {summary['duration_seconds']:.1f}秒")
    
    return "\n".join(lines)

