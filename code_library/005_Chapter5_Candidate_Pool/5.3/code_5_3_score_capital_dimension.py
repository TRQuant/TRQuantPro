"""
文件名: code_5_3_score_capital_dimension.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.3/code_5_3_score_capital_dimension.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.3_Stock_Scoring_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: score_capital_dimension

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def score_capital_dimension(
    stock_code: str,
    main_fund_data: Dict,
    northbound_data: Dict,
    lhb_data: Dict,
    turnover_data: Dict
) -> float:
    """
    资金面评分
    
    Args:
        stock_code: 股票代码
        main_fund_data: 主力资金数据
        northbound_data: 北向资金数据
        lhb_data: 龙虎榜数据
        turnover_data: 换手率数据
    
    Returns:
        资金面评分（0-100分）
    """
    score = 0.0
    
    # 1. 主力资金评分（0-40分）
    main_fund_inflow = main_fund_data.get('net_inflow', 0)  # 净流入（万元）
    main_fund_ratio = main_fund_data.get('main_ratio', 0)  # 主力占比
    consecutive_days = main_fund_data.get('consecutive_inflow_days', 0)  # 连续流入天数
    
    # 设计原理：主力资金评分采用分段评分
    # 原因：不同资金流入水平对应不同的评分，需要分段处理
    # 评分维度：净流入金额、主力占比、连续流入天数
    # 为什么这样设计：综合考虑多个维度，更准确反映主力资金认可度
    # 评分逻辑：
    # - 优秀（40分）：大额流入 + 高占比 + 持续流入
    # - 良好（35分）：中等流入 + 中等占比 + 持续流入
    # - 一般（30分）：小额流入 + 低占比
    # - 较差（20分）：小幅流出
    # - 很差（10-0分）：大幅流出
    if main_fund_inflow > 10000 and main_fund_ratio > 0.3 and consecutive_days >= 3:
        main_fund_score = 40
    elif main_fund_inflow > 5000 and main_fund_ratio > 0.2 and consecutive_days >= 2:
        main_fund_score = 35
    elif main_fund_inflow > 0 and main_fund_ratio > 0.1:
        main_fund_score = 30
    elif main_fund_inflow > -5000:
        main_fund_score = 20
    else:
        # 设计原理：线性评分
        # 原因：大幅流出时，流出越多得分越低
        # 公式：得分 = 10 + 净流入/1000，最低0分
        main_fund_score = max(0, 10 + main_fund_inflow / 1000)
    
    # 2. 北向资金评分（0-30分）
    northbound_position = northbound_data.get('position', 0)  # 持仓市值（万元）
    northbound_change = northbound_data.get('change_pct', 0)  # 增持幅度（%）
    northbound_ratio = northbound_data.get('ratio', 0)  # 占流通盘比例
    
    # 北向资金评分
    if northbound_position > 50000 and northbound_change > 5 and northbound_ratio > 0.05:
        northbound_score = 30
    elif northbound_position > 20000 and northbound_change > 2 and northbound_ratio > 0.02:
        northbound_score = 25
    elif northbound_position > 0 and northbound_change > 0:
        northbound_score = 20
    elif northbound_position > 0:
        northbound_score = 15
    else:
        northbound_score = 10
    
    # 3. 龙虎榜评分（0-20分）
    lhb_count = lhb_data.get('count', 0)  # 上榜次数（近20日）
    lhb_net_buy = lhb_data.get('net_buy', 0)  # 净买入额（万元）
    institution_count = lhb_data.get('institution_count', 0)  # 机构席位次数
    
    # 龙虎榜评分
    if lhb_count >= 3 and lhb_net_buy > 5000 and institution_count >= 1:
        lhb_score = 20
    elif lhb_count >= 2 and lhb_net_buy > 0:
        lhb_score = 15
    elif lhb_count >= 1:
        lhb_score = 10
    else:
        lhb_score = 5
    
    # 4. 换手率评分（0-10分）
    turnover_rate = turnover_data.get('turnover_rate', 0)  # 换手率（%）
    turnover_change = turnover_data.get('turnover_change', 0)  # 换手率变化（%）
    
    # 换手率评分（适度活跃为佳）
    if 3 <= turnover_rate <= 10 and turnover_change > 0:
        turnover_score = 10
    elif 2 <= turnover_rate <= 15:
        turnover_score = 8
    elif turnover_rate > 0:
        turnover_score = 5
    else:
        turnover_score = 0
    
    score = main_fund_score + northbound_score + lhb_score + turnover_score
    return min(100, max(0, score))