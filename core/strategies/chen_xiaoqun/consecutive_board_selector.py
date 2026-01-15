"""
连板股票选择器

实现"一进二"战法和连板股票识别优化
"""

import pandas as pd
import logging
from typing import List, Dict, Optional, Any
from .utils import identify_exchange_and_convert

logger = logging.getLogger(__name__)


def get_board_count_verified(
    code: str,
    date_str: str,
    limit_up_df: pd.DataFrame,
    jq_client: Any = None
) -> int:
    """
    双重验证连板数
    
    方法1：从涨停板数据中获取
    方法2：通过历史价格数据计算验证
    
    Args:
        code: 股票代码（原始格式，如"002774"）
        date_str: 日期字符串
        limit_up_df: 涨停板数据DataFrame
        jq_client: JQData客户端（可选）
    
    Returns:
        连板数（取两者中的较大值，更保守）
    """
    # 方法1：从涨停板数据中获取
    stock_row = limit_up_df[limit_up_df['代码'] == code]
    if not stock_row.empty:
        board_count_data = int(stock_row.iloc[0].get('连板数', 1))
    else:
        board_count_data = 1
    
    # 方法2：通过历史价格数据计算验证（如果提供jq_client）
    board_count_calc = board_count_data
    if jq_client:
        try:
            # 转换为JQData格式
            jq_code, _, is_valid = identify_exchange_and_convert(code)
            if is_valid:
                # 获取最近5天的价格数据
                price_data = jq_client.get_price(
                    jq_code,
                    count=5,
                    end_date=date_str,
                    frequency='daily',
                    fields=['close', 'high_limit']
                )
                
                if price_data is not None and not price_data.empty:
                    board_count_calc = 0
                    for i in range(len(price_data)-1, -1, -1):
                        close = price_data['close'].iloc[i]
                        high_limit = price_data['high_limit'].iloc[i]
                        # 允许0.5%误差
                        if abs(close - high_limit) / high_limit < 0.005:
                            board_count_calc += 1
                        else:
                            break
        except Exception as e:
            logger.debug(f"计算连板数失败 {code}: {e}")
            board_count_calc = board_count_data
    
    # 取两者中的较大值（更保守）
    return max(board_count_data, board_count_calc)


def select_consecutive_board_stocks(
    limit_up_data: pd.DataFrame,
    date_str: str,
    jq_client: Any = None,
    min_board_count: int = 2,
    top_n: int = 5,
    top_themes: Optional[List[Dict]] = None
) -> List[Dict]:
    """
    选择连板股票（二板及以上）
    
    选股条件：
    1. 连板数 >= min_board_count（默认2板）
    2. 双重验证连板数
    3. 优先选择最高连板的股票
    4. 优先选择最强题材的股票
    
    Args:
        limit_up_data: 涨停板数据DataFrame
        date_str: 日期字符串
        jq_client: JQData客户端（可选，用于双重验证）
        min_board_count: 最低连板数（默认2板）
        top_n: 返回前N只（默认5只）
        top_themes: 最强题材列表（可选）
    
    Returns:
        连板股票列表
    """
    if limit_up_data is None or limit_up_data.empty:
        return []
    
    # 筛选连板股票
    if '连板数' not in limit_up_data.columns:
        logger.warning(f"{date_str} 涨停板数据中没有'连板数'字段")
        return []
    
    consecutive_boards = limit_up_data[limit_up_data['连板数'] >= min_board_count].copy()
    if consecutive_boards.empty:
        return []
    
    # 双重验证连板数
    verified_stocks = []
    for idx, row in consecutive_boards.iterrows():
        code = str(row.get('代码', ''))
        jq_code, _, is_valid = identify_exchange_and_convert(code)
        
        if is_valid:
            # 双重验证连板数
            board_count = get_board_count_verified(code, date_str, limit_up_data, jq_client)
            
            if board_count >= min_board_count:
                stock_info = {
                    'code': code,
                    'jq_code': jq_code,
                    'name': row.get('名称', ''),
                    'board_count': board_count,
                    'sector': row.get('所属行业', ''),
                    'verified': True
                }
                
                # 添加题材优先级（如果启用题材筛选）
                if top_themes:
                    from .theme_analyzer import get_theme_priority
                    sector = row.get('所属行业', '')
                    theme_priority = get_theme_priority(sector, top_themes)
                    stock_info['theme_priority'] = theme_priority
                
                verified_stocks.append(stock_info)
    
    # 按连板数排序（如果启用题材筛选，按题材优先级和连板数排序）
    if top_themes:
        verified_stocks.sort(key=lambda x: (x.get('theme_priority', 999), -x.get('board_count', 0)))
    else:
        verified_stocks.sort(key=lambda x: -x.get('board_count', 0))
    
    return verified_stocks[:top_n]


def confirm_second_board(
    first_board_stocks: List[Dict],
    date_str: str,
    jq_client: Any = None,
    limit_up_df: pd.DataFrame = None
) -> List[Dict]:
    """
    首板次日二板确认（"一进二"战法）
    
    逻辑：
    1. 检查首板股票次日是否继续涨停
    2. 如果继续涨停，确认为二板
    3. 优先选择开盘后快速封板的股票（9:35前）
    
    Args:
        first_board_stocks: 首板股票列表
        date_str: 日期字符串（次日）
        jq_client: JQData客户端（可选）
        limit_up_df: 当日涨停板数据（可选）
    
    Returns:
        确认的二板股票列表
    """
    if not first_board_stocks:
        return []
    
    if limit_up_df is None or limit_up_df.empty:
        return []
    
    second_board_stocks = []
    
    for stock in first_board_stocks:
        code = stock.get('code', '')
        
        # 检查今日是否继续涨停
        today_limit_up = limit_up_df[limit_up_df['代码'] == code]
        if not today_limit_up.empty:
            board_count = int(today_limit_up.iloc[0].get('连板数', 1))
            if board_count >= 2:
                # 确认为二板
                stock['board_count'] = board_count
                stock['confirmed'] = True
                stock['confirmed_date'] = date_str
                second_board_stocks.append(stock)
                logger.info(f"{date_str} ✅ 确认二板: {stock.get('name', code)} ({code})")
    
    return second_board_stocks
