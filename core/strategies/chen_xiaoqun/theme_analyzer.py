"""
题材分析模块

用于识别最强题材，支持陈小群策略的题材驱动选股逻辑。
"""

import pandas as pd
from typing import List, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


def identify_top_themes(
    limit_up_data: Union[pd.DataFrame, Dict],
    top_n: int = 3,
    df_key_candidates: Optional[List[str]] = None
) -> List[Dict]:
    """
    识别最强题材（涨停家数最多的板块）
    
    这是陈小群策略的核心要素：聚焦最强题材，避免杂毛股。
    
    Args:
        limit_up_data: 涨停板数据
            - DataFrame: 明细数据（必须包含'所属行业'列）
            - Dict: 容器字典，会尝试从以下key提取DataFrame:
                'limit_up_df', 'limit_up_detail', 'stocks_df', 'data', 'df'
        top_n: 返回前N个最强题材（默认3个）
        df_key_candidates: 当输入为dict时，尝试提取DataFrame的key列表
    
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
    if df_key_candidates is None:
        df_key_candidates = ["limit_up_df", "limit_up_detail", "stocks_df", "data", "df"]
    
    # 1) 统一抽取 DataFrame
    if limit_up_data is None:
        logger.debug("涨停板数据为None，返回空列表")
        return []
    
    df = None
    if isinstance(limit_up_data, dict):
        # 尝试从dict中提取DataFrame
        for k in df_key_candidates:
            v = limit_up_data.get(k)
            if isinstance(v, pd.DataFrame):
                df = v
                logger.debug(f"从dict中提取到DataFrame，key={k}")
                break
        if df is None:
            logger.debug("limit_up_data为dict但未找到涨停明细DataFrame，跳过题材识别")
            return []
    elif isinstance(limit_up_data, pd.DataFrame):
        df = limit_up_data
    else:
        logger.warning(f"limit_up_data类型异常: {type(limit_up_data)}，跳过题材识别")
        return []
    
    # 2) 空表保护
    if df.empty:
        logger.debug("涨停明细DataFrame为空，返回空列表")
        return []
    
    # 3) 检查是否有题材字段（支持多种命名）
    theme_col = None
    for cand in ["所属行业", "板块", "题材", "概念", "industry", "theme", "concept", "sector"]:
        if cand in df.columns:
            theme_col = cand
            break
    
    if theme_col is None:
        logger.warning("涨停明细df缺少题材字段，跳过题材识别")
        return []
    
    # 4) 按板块统计涨停家数
    sector_counts = df.groupby(theme_col).size().sort_values(ascending=False)
    
    if sector_counts.empty:
        logger.warning("无法统计板块数据")
        return []
    
    # 5) 计算强度评分（涨停家数占比）
    total_limit_up = len(df)
    
    # 6) 返回前N个最强题材
    top_themes = []
    for sector, count in sector_counts.head(top_n).items():
        sector_stocks = df[df[theme_col] == sector]
        
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
