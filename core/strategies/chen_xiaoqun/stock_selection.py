"""
选股逻辑模块

实现陈小群战法的选股策略：
1. 首板卡位术：启动期选股（连板数=1，流通市值<30亿，封板资金占比>=2%）
2. 龙头战法：加速期选股（最高连板股票）
"""

import pandas as pd
from typing import List, Dict, Optional
from .utils import identify_exchange_and_convert


def select_first_board_stocks(
    limit_up_data: pd.DataFrame,
    date_str: Optional[str] = None
) -> List[Dict]:
    """
    首板卡位术选股（启动期）
    
    选股条件（所有条件必须同时满足）：
    1. 连板数 = 1（首板）
    2. 流通市值 < 50亿（从30亿放宽，适应市场环境）
    3. 封板资金占比 >= 1.5%（从2%降低，提高选股成功率）
    4. 板块效应：板块内至少3只跟风涨停（新增）
    
    Args:
        limit_up_data: 涨停板数据（DataFrame，必须包含'代码'、'名称'、'连板数'、'流通市值'、'封板资金'等列）
        date_str: 日期字符串（可选，用于日志记录）
    
    Returns:
        候选股票列表，每个元素包含：
        {
            'code': 股票代码,
            'jq_code': JQData格式代码,
            'name': 股票名称,
            'market_cap': 流通市值（亿元）,
            'limit_ratio': 封板资金占比（%）,
            'sector': 所属行业
        }
        按封板资金占比从高到低排序
    """
    if limit_up_data is None or limit_up_data.empty:
        return []
    
    candidates = []
    
    for idx, row in limit_up_data.iterrows():
        # 条件1: 连板数 = 1
        board_count = row.get('连板数', 0)
        if pd.isna(board_count) or board_count != 1:
            continue
        
        # 条件2: 流通市值 < 50亿（从30亿放宽，适应市场环境）
        market_cap = row.get('流通市值', 0)
        if pd.isna(market_cap) or market_cap >= 50 * 1e8:
            continue
        
        # 条件3: 封板资金占比 >= 1.5%（从2%降低，提高选股成功率）
        limit_amount = row.get('封板资金', 0)
        if pd.isna(limit_amount) or limit_amount == 0:
            continue
        
        limit_ratio = limit_amount / market_cap
        if limit_ratio < 0.015:  # 从0.02降低到0.015
            continue
        
        # 条件4: 板块效应（板块内至少3只跟风涨停）
        sector = row.get('所属行业', '')
        if sector:
            sector_stocks = limit_up_data[limit_up_data['所属行业'] == sector]
            if len(sector_stocks) < 3:
                continue  # 板块内涨停数不足3只，跳过
        
        # 转换为JQData格式
        code = str(row.get('代码', ''))
        jq_code, _, is_valid = identify_exchange_and_convert(code)
        
        if is_valid:
            candidates.append({
                'code': code,
                'jq_code': jq_code,
                'name': row.get('名称', ''),
                'market_cap': market_cap / 1e8,  # 转换为亿元
                'limit_ratio': limit_ratio * 100,  # 转换为百分比
                'sector': sector,
                'sector_count': len(sector_stocks) if sector else 0  # 板块内涨停数
            })
    
    # 按封板资金占比和板块效应排序（从高到低）
    candidates.sort(key=lambda x: (x['limit_ratio'], x.get('sector_count', 0)), reverse=True)
    return candidates


def select_dragon_stocks(
    limit_up_data: pd.DataFrame,
    date_str: Optional[str] = None
) -> List[Dict]:
    """
    龙头战法选股（加速期）
    
    选股条件：
    1. 连板数 >= 2（至少2板）
    2. 选择最高连板的股票（市场总龙头）
    3. 板块效应：板块内至少3只跟风涨停（新增，优先选择板块龙头）
    
    Args:
        limit_up_data: 涨停板数据（DataFrame，必须包含'代码'、'名称'、'连板数'等列）
        date_str: 日期字符串（可选，用于日志记录）
    
    Returns:
        龙头股票列表，每个元素包含：
        {
            'code': 股票代码,
            'jq_code': JQData格式代码,
            'name': 股票名称,
            'board_count': 连板数,
            'sector': 所属行业
        }
        按连板数从高到低排序
    """
    if limit_up_data is None or limit_up_data.empty:
        return []
    
    # 筛选连板股票
    if '连板数' not in limit_up_data.columns:
        return []
    
    consecutive_boards = limit_up_data[limit_up_data['连板数'] >= 2].copy()
    if consecutive_boards.empty:
        return []
    
    # 按连板数排序
    consecutive_boards = consecutive_boards.sort_values('连板数', ascending=False)
    
    dragons = []
    max_board = consecutive_boards['连板数'].max()
    
    # 1. 市场总龙头（最高连板）
    top_dragons = consecutive_boards[consecutive_boards['连板数'] == max_board]
    
    for idx, row in top_dragons.iterrows():
        code = str(row.get('代码', ''))
        jq_code, _, is_valid = identify_exchange_and_convert(code)
        
        if is_valid:
            dragons.append({
                'code': code,
                'jq_code': jq_code,
                'name': row.get('名称', ''),
                'board_count': int(row.get('连板数', 0)),
                'sector': row.get('所属行业', ''),
                'type': 'market_leader'  # 市场总龙头
            })
    
    # 2. 板块龙头（每个板块的最高连板，板块内至少3只涨停）
    for sector in consecutive_boards['所属行业'].unique():
        sector_stocks = consecutive_boards[consecutive_boards['所属行业'] == sector]
        if len(sector_stocks) < 3:  # 板块内至少3只涨停
            continue
        
        sector_max_board = sector_stocks['连板数'].max()
        sector_leaders = sector_stocks[sector_stocks['连板数'] == sector_max_board]
        
        for idx, row in sector_leaders.iterrows():
            code = str(row.get('代码', ''))
            jq_code, _, is_valid = identify_exchange_and_convert(code)
            
            if is_valid and code not in [d['code'] for d in dragons]:
                dragons.append({
                    'code': code,
                    'jq_code': jq_code,
                    'name': row.get('名称', ''),
                    'board_count': int(row.get('连板数', 0)),
                    'sector': sector,
                    'type': 'sector_leader',  # 板块龙头
                    'sector_count': len(sector_stocks)  # 板块内涨停数
                })
    
    # 按连板数和板块效应排序（从高到低）
    dragons.sort(key=lambda x: (x['board_count'], x.get('sector_count', 0)), reverse=True)
    return dragons
