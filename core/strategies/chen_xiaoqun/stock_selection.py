"""
选股逻辑模块

实现陈小群战法的选股策略：
1. 首板卡位术：启动期选股（连板数=1，流通市值<30亿，封板资金占比>=2%）
2. 龙头战法：加速期选股（最高连板股票）

新增：题材筛选功能（聚焦最强题材，避免杂毛股）
"""

import pandas as pd
from typing import List, Dict, Optional
from .utils import identify_exchange_and_convert
from .theme_analyzer import get_theme_priority


def select_first_board_stocks(
    limit_up_data: pd.DataFrame,
    date_str: Optional[str] = None,
    top_themes: Optional[List[Dict]] = None,
    prioritize_theme: bool = True
) -> List[Dict]:
    """
    首板卡位术选股（启动期）- 增加题材筛选
    
    选股条件（所有条件必须同时满足）：
    1. 连板数 = 1（首板）
    2. 流通市值 < 80亿（从50亿进一步放宽，适应市场环境）
    3. 封板资金占比 >= 1.0%（从1.5%降低，提高选股成功率）
    4. 板块效应：板块内至少2只跟风涨停（从3只降低，提高选股成功率）
    
    选股优先级（如果启用题材筛选）：
    1. 最强题材的股票（优先）
    2. 次强题材的股票（次优先）
    3. 其他题材的股票（最后）
    
    Args:
        limit_up_data: 涨停板数据（DataFrame，必须包含'代码'、'名称'、'连板数'、'流通市值'、'封板资金'等列）
        date_str: 日期字符串（可选，用于日志记录）
        top_themes: 最强题材列表（可选，如果不提供则不进行题材筛选）
        prioritize_theme: 是否优先选择主流题材（默认True）
    
    Returns:
        候选股票列表，每个元素包含：
        {
            'code': 股票代码,
            'jq_code': JQData格式代码,
            'name': 股票名称,
            'market_cap': 流通市值（亿元）,
            'limit_ratio': 封板资金占比（%）,
            'sector': 所属行业,
            'theme_priority': 题材优先级（如果启用题材筛选）
        }
        按题材优先级和封板资金占比排序（如果启用题材筛选）
    """
    if limit_up_data is None or limit_up_data.empty:
        return []
    
    candidates = []
    
    for idx, row in limit_up_data.iterrows():
        # 条件1: 连板数 = 1
        board_count = row.get('连板数', 0)
        if pd.isna(board_count) or board_count != 1:
            continue
        
        # 条件2: 流通市值 < 80亿（从50亿进一步放宽，适应市场环境）
        market_cap = row.get('流通市值', 0)
        if pd.isna(market_cap) or market_cap >= 80 * 1e8:
            continue
        
        # 条件3: 封板资金占比 >= 1.0%（从1.5%降低，提高选股成功率）
        limit_amount = row.get('封板资金', 0)
        if pd.isna(limit_amount) or limit_amount == 0:
            continue
        
        limit_ratio = limit_amount / market_cap
        if limit_ratio < 0.01:  # 从0.015降低到0.01
            continue
        
        # 条件4: 板块效应（板块内至少2只跟风涨停，从3只降低）
        sector = row.get('所属行业', '')
        if sector:
            sector_stocks = limit_up_data[limit_up_data['所属行业'] == sector]
            if len(sector_stocks) < 2:  # 从3降低到2
                continue  # 板块内涨停数不足2只，跳过
        
        # 转换为JQData格式
        code = str(row.get('代码', ''))
        jq_code, _, is_valid = identify_exchange_and_convert(code)
        
        if is_valid:
            candidate = {
                'code': code,
                'jq_code': jq_code,
                'name': row.get('名称', ''),
                'market_cap': market_cap / 1e8,  # 转换为亿元
                'limit_ratio': limit_ratio * 100,  # 转换为百分比
                'sector': sector,
                'sector_count': len(sector_stocks) if sector else 0  # 板块内涨停数
            }
            
            # 添加题材优先级（如果启用题材筛选）
            if top_themes and prioritize_theme:
                theme_priority = get_theme_priority(sector, top_themes)
                candidate['theme_priority'] = theme_priority
                # 获取题材强度
                for theme in top_themes:
                    if theme['sector'] == sector:
                        candidate['theme_strength'] = theme['strength_score']
                        break
                else:
                    candidate['theme_strength'] = 0
            
            candidates.append(candidate)
    
    # 排序：如果启用题材筛选，按题材优先级和封板资金占比排序；否则按封板资金占比排序
    if top_themes and prioritize_theme:
        candidates.sort(key=lambda x: (x.get('theme_priority', 999), -x.get('limit_ratio', 0)))
    else:
        candidates.sort(key=lambda x: (-x.get('limit_ratio', 0), x.get('sector_count', 0)), reverse=True)
    
    return candidates


def select_dragon_stocks(
    limit_up_data: pd.DataFrame,
    date_str: Optional[str] = None,
    top_themes: Optional[List[Dict]] = None,
    prioritize_theme: bool = True
) -> List[Dict]:
    """
    龙头战法选股（加速期）- 增加题材筛选
    
    选股条件：
    1. 连板数 >= 2（至少2板）
    2. 选择最高连板的股票（市场总龙头）
    3. 板块效应：板块内至少2只跟风涨停（从3只降低，优先选择板块龙头）
    
    选股优先级（如果启用题材筛选）：
    1. 最强题材的龙头（优先）
    2. 次强题材的龙头（次优先）
    3. 其他题材的龙头（最后）
    
    Args:
        limit_up_data: 涨停板数据（DataFrame，必须包含'代码'、'名称'、'连板数'等列）
        date_str: 日期字符串（可选，用于日志记录）
        top_themes: 最强题材列表（可选，如果不提供则不进行题材筛选）
        prioritize_theme: 是否优先选择主流题材（默认True）
    
    Returns:
        龙头股票列表，每个元素包含：
        {
            'code': 股票代码,
            'jq_code': JQData格式代码,
            'name': 股票名称,
            'board_count': 连板数,
            'sector': 所属行业,
            'theme_priority': 题材优先级（如果启用题材筛选）
        }
        按题材优先级和连板数排序（如果启用题材筛选）
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
            dragon = {
                'code': code,
                'jq_code': jq_code,
                'name': row.get('名称', ''),
                'board_count': int(row.get('连板数', 0)),
                'sector': row.get('所属行业', ''),
                'type': 'market_leader'  # 市场总龙头
            }
            
            # 添加题材优先级（如果启用题材筛选）
            if top_themes and prioritize_theme:
                sector = row.get('所属行业', '')
                theme_priority = get_theme_priority(sector, top_themes)
                dragon['theme_priority'] = theme_priority
                # 获取题材强度
                for theme in top_themes:
                    if theme['sector'] == sector:
                        dragon['theme_strength'] = theme['strength_score']
                        break
                else:
                    dragon['theme_strength'] = 0
            
            dragons.append(dragon)
    
    # 2. 板块龙头（每个板块的最高连板，板块内至少2只涨停）
    for sector in consecutive_boards['所属行业'].unique():
        sector_stocks = consecutive_boards[consecutive_boards['所属行业'] == sector]
        if len(sector_stocks) < 2:  # 板块内至少2只涨停（从3降低到2）
            continue
        
        sector_max_board = sector_stocks['连板数'].max()
        sector_leaders = sector_stocks[sector_stocks['连板数'] == sector_max_board]
        
        for idx, row in sector_leaders.iterrows():
            code = str(row.get('代码', ''))
            jq_code, _, is_valid = identify_exchange_and_convert(code)
            
            if is_valid and code not in [d['code'] for d in dragons]:
                dragon = {
                    'code': code,
                    'jq_code': jq_code,
                    'name': row.get('名称', ''),
                    'board_count': int(row.get('连板数', 0)),
                    'sector': sector,
                    'type': 'sector_leader',  # 板块龙头
                    'sector_count': len(sector_stocks)  # 板块内涨停数
                }
                
                # 添加题材优先级（如果启用题材筛选）
                if top_themes and prioritize_theme:
                    theme_priority = get_theme_priority(sector, top_themes)
                    dragon['theme_priority'] = theme_priority
                    # 获取题材强度
                    for theme in top_themes:
                        if theme['sector'] == sector:
                            dragon['theme_strength'] = theme['strength_score']
                            break
                    else:
                        dragon['theme_strength'] = 0
                
                dragons.append(dragon)
    
    # 排序：如果启用题材筛选，按题材优先级和连板数排序；否则按连板数排序
    if top_themes and prioritize_theme:
        dragons.sort(key=lambda x: (x.get('theme_priority', 999), -x.get('board_count', 0)))
    else:
        dragons.sort(key=lambda x: (-x.get('board_count', 0), x.get('sector_count', 0)), reverse=True)
    
    return dragons
