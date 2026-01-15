"""
题材分析模块

用于识别最强题材，支持陈小群策略的题材驱动选股逻辑。
"""

import pandas as pd
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


def identify_top_themes(
    limit_up_data: pd.DataFrame,
    top_n: int = 3
) -> List[Dict]:
    """
    识别最强题材（涨停家数最多的板块）
    
    这是陈小群策略的核心要素：聚焦最强题材，避免杂毛股。
    
    Args:
        limit_up_data: 涨停板数据（DataFrame，必须包含'所属行业'列）
        top_n: 返回前N个最强题材（默认3个）
    
    Returns:
        [
            {
                'sector': '板块名称',
                'count': 涨停家数,
                'stocks': [股票列表],
                'strength_score': 强度评分（0-100）
            },
            ...
        ]
        按强度从高到低排序
    """
    if limit_up_data is None or limit_up_data.empty:
        logger.warning("涨停板数据为空，无法识别题材")
        return []
    
    # 检查是否有'所属行业'列
    if '所属行业' not in limit_up_data.columns:
        logger.warning("涨停板数据缺少'所属行业'列，无法识别题材")
        return []
    
    # 按板块统计涨停家数
    sector_counts = limit_up_data.groupby('所属行业').size().sort_values(ascending=False)
    
    if sector_counts.empty:
        logger.warning("无法统计板块数据")
        return []
    
    # 计算强度评分（涨停家数占比）
    total_limit_up = len(limit_up_data)
    
    # 返回前N个最强题材
    top_themes = []
    for sector, count in sector_counts.head(top_n).items():
        sector_stocks = limit_up_data[limit_up_data['所属行业'] == sector]
        
        # 计算强度评分（涨停家数占比 * 100）
        strength_score = (count / total_limit_up) * 100 if total_limit_up > 0 else 0
        
        top_themes.append({
            'sector': sector,
            'count': int(count),
            'stocks': sector_stocks.to_dict('records'),
            'strength_score': round(strength_score, 2)
        })
    
    logger.info(f"识别到 {len(top_themes)} 个最强题材: {[t['sector'] for t in top_themes]}")
    
    return top_themes


def is_mainstream_theme(
    sector: str,
    top_themes: List[Dict],
    threshold: int = 3
) -> bool:
    """
    判断是否为主流题材
    
    主流题材定义：前N个最强题材（默认前3个）
    
    Args:
        sector: 板块名称
        top_themes: 最强题材列表（来自identify_top_themes）
        threshold: 前N个题材视为主流（默认3个）
    
    Returns:
        True if 主流题材, False otherwise
    """
    if not top_themes:
        return False
    
    # 检查是否在前N个最强题材中
    top_sectors = [theme['sector'] for theme in top_themes[:threshold]]
    return sector in top_sectors


def get_theme_priority(
    sector: str,
    top_themes: List[Dict]
) -> int:
    """
    获取题材优先级
    
    优先级：1 = 最强题材，2 = 次强题材，...，999 = 非主流题材
    
    Args:
        sector: 板块名称
        top_themes: 最强题材列表
    
    Returns:
        优先级（1-N，999表示非主流）
    """
    if not top_themes:
        return 999
    
    for i, theme in enumerate(top_themes):
        if theme['sector'] == sector:
            return i + 1
    
    return 999  # 非主流题材
