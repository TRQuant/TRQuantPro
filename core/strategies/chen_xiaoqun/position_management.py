"""
持仓管理模块

实现陈小群战法的持仓管理策略：
1. 三板加速术：分析2板及以上股票的三板潜力
2. 持仓监控：监控持仓股票的关键指标
3. 止盈止损判断：根据市场情况给出操作建议
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional


def analyze_third_board(
    limit_up_data: pd.DataFrame,
    date_str: Optional[str] = None
) -> pd.DataFrame:
    """
    三板加速术分析：评估2板及以上股票的三板潜力
    
    评估条件：
    1. 连板数（2板冲3板、3板冲4板等）
    2. 换手率分析（缩量或放量）
    3. 板块效应（板块内涨停数量）
    4. 封板资金（资金共识强度）
    
    Args:
        limit_up_data: 涨停板数据（DataFrame，必须包含'代码'、'名称'、'连板数'、'换手率'、'所属行业'、'封板资金'等列）
        date_str: 日期字符串（可选，用于日志记录）
    
    Returns:
        DataFrame，包含以下列：
        - 代码、名称、连板数、换手率、所属行业、封板资金
        - 三板潜力（'高'/'中'/'低'）
        - 评分（0-5分）
        - 评估因素（列表）
    """
    if limit_up_data is None or limit_up_data.empty:
        return pd.DataFrame()
    
    # 筛选2板以上的股票
    if '连板数' not in limit_up_data.columns:
        return pd.DataFrame()
    
    two_plus_boards = limit_up_data[limit_up_data['连板数'] >= 2].copy()
    
    if two_plus_boards.empty:
        return pd.DataFrame()
    
    results = []
    
    for idx, row in two_plus_boards.iterrows():
        code = row.get('代码', '')
        name = row.get('名称', '')
        board_count = row.get('连板数', 0)
        turnover = row.get('换手率', 0)
        sector = row.get('所属行业', '')
        limit_amount = row.get('封板资金', 0)
        
        # 评估三板潜力
        score = 0.0
        factors = []
        
        # 条件1: 连板数（2板冲3板、3板冲4板等）
        if board_count == 2:
            score += 1.0
            factors.append(f"当前2板，今日冲击3板 ✅")
        elif board_count >= 3:
            score += 1.5
            factors.append(f"当前{board_count}板，连板强势 ✅✅")
        
        # 条件2: 换手率分析（缩量或放量）
        if turnover < 10:
            score += 1.0
            factors.append(f"换手率{turnover:.2f}%，缩量涨停（筹码锁定）✅")
        elif turnover < 25:
            score += 0.5
            factors.append(f"换手率{turnover:.2f}%，放量涨停（新资金入场）⚠️")
        else:
            score += 0.3
            factors.append(f"换手率{turnover:.2f}%，放量过大（分歧较大）⚠️⚠️")
        
        # 条件3: 板块效应（板块内涨停数量）
        if sector and '所属行业' in limit_up_data.columns:
            sector_count = len(limit_up_data[limit_up_data['所属行业'] == sector])
            if sector_count >= 3:
                score += 1.0
                factors.append(f"板块效应强（{sector}板块{sector_count}只涨停）✅")
            elif sector_count >= 2:
                score += 0.5
                factors.append(f"板块效应中等（{sector}板块{sector_count}只涨停）⚠️")
            else:
                score += 0.2
                factors.append(f"板块效应弱（{sector}板块仅{sector_count}只涨停）⚠️⚠️")
        
        # 条件4: 封板资金（资金共识强度）
        if limit_amount:
            limit_amount_yi = limit_amount / 1e8  # 转换为亿元
            if limit_amount_yi >= 5:
                score += 1.0
                factors.append(f"封板资金{limit_amount_yi:.2f}亿（资金共识强）✅")
            elif limit_amount_yi >= 2:
                score += 0.5
                factors.append(f"封板资金{limit_amount_yi:.2f}亿（资金共识中等）⚠️")
            else:
                score += 0.3
                factors.append(f"封板资金{limit_amount_yi:.2f}亿（资金共识弱）⚠️⚠️")
        
        # 分类潜力等级
        if score >= 4.0:
            potential = '高'
        elif score >= 3.0:
            potential = '中'
        else:
            potential = '低'
        
        results.append({
            '代码': code,
            '名称': name,
            '当前连板': int(board_count),
            '换手率': turnover,
            '所属行业': sector,
            '封板资金': limit_amount,
            '三板潜力': potential,
            '评分': score,
            '评估因素': factors
        })
    
    result_df = pd.DataFrame(results)
    # 按评分排序（从高到低）
    if not result_df.empty:
        result_df = result_df.sort_values('评分', ascending=False)
    
    return result_df


def monitor_position(
    stock_code: str,
    stock_name: str,
    limit_up_data: pd.DataFrame
) -> Tuple[str, int, List[str]]:
    """
    监控单只股票的持仓状态
    
    Args:
        stock_code: 股票代码
        stock_name: 股票名称
        limit_up_data: 当日涨停板数据（DataFrame）
    
    Returns:
        (status, risk_level, signals)
        - status: 持仓状态（'holding'/'warning'/'exit'）
        - risk_level: 风险等级（0-100）
        - signals: 信号列表
    """
    status = 'holding'
    risk_level = 0
    signals: List[str] = []
    
    if limit_up_data is None or limit_up_data.empty:
        return 'warning', 50, ['无法获取市场数据']
    
    stock_in_zt = limit_up_data[limit_up_data['代码'] == stock_code]
    
    if stock_in_zt.empty:
        status = 'warning'
        risk_level += 30
        signals.append("⚠️  股票今日未涨停，需要关注")
    else:
        stock_info = stock_in_zt.iloc[0]
        board_count = stock_info.get('连板数', 'N/A')
        signals.append(f"✅ 股票今日涨停（连板数: {board_count}）")
        
        limit_amount = stock_info.get('封板资金', 0)
        if limit_amount:
            limit_amount_yi = limit_amount / 1e8
            if limit_amount_yi < 0.5:
                risk_level += 20
                signals.append(f"⚠️  封板资金较少（{limit_amount_yi:.2f}亿）")
            else:
                signals.append(f"✅ 封板资金充足（{limit_amount_yi:.2f}亿）")
        
        sector = stock_info.get('所属行业', '')
        if sector and '所属行业' in limit_up_data.columns:
            sector_count = len(limit_up_data[limit_up_data['所属行业'] == sector])
            if sector_count < 2:
                risk_level += 15
                signals.append(f"⚠️  板块效应减弱（{sector}仅{sector_count}只涨停）")
            else:
                signals.append(f"✅ 板块效应良好（{sector}有{sector_count}只涨停）")
    
    if risk_level >= 50:
        status = 'exit'
    elif risk_level >= 30:
        status = 'warning'
    
    return status, risk_level, signals


def judge_stop_loss(
    zhaban_rate: float,
    limit_up_count: Optional[int] = None,
    max_height: Optional[int] = None,
    emotion_cycle: Optional[str] = None,
    limit_up_count_today: Optional[int] = None,
    max_height_today: Optional[int] = None
) -> Dict:
    """
    止盈止损判断：根据市场情况给出操作建议
    
    Args:
        zhaban_rate: 当前炸板率（百分比）
        limit_up_count: 昨日涨停家数（可选）
        max_height: 昨日最高连板（可选）
        emotion_cycle: 当前情绪周期（可选）
        limit_up_count_today: 今日涨停家数（可选）
        max_height_today: 今日最高连板（可选）
    
    Returns:
        {
            'market_risk': 市场风险等级（0-100）,
            'risk_level_text': 风险评级文本,
            'market_signals': 市场信号列表,
            'operation_advice': 操作建议
        }
    """
    market_risk = 0
    market_signals: List[str] = []
    
    # 1. 炸板率风险
    if zhaban_rate > 30:
        market_risk += 30
        market_signals.append(f"🔴 炸板率过高 ({zhaban_rate:.2f}%)，市场情绪不稳")
    elif zhaban_rate > 25:
        market_risk += 15
        market_signals.append(f"🟡 炸板率偏高 ({zhaban_rate:.2f}%)")
    else:
        market_signals.append(f"🟢 炸板率正常 ({zhaban_rate:.2f}%)")
    
    # 2. 涨停家数变化
    if limit_up_count is not None and limit_up_count_today is not None:
        if limit_up_count_today < limit_up_count * 0.7:
            market_risk += 25
            market_signals.append(f"🔴 涨停家数大幅下降 ({limit_up_count} → {limit_up_count_today})")
        else:
            market_signals.append(f"🟢 涨停家数稳定 (今日{limit_up_count_today}只)")
    
    # 3. 连板高度变化
    if max_height is not None and max_height_today is not None:
        if max_height_today < max_height - 1:
            market_risk += 20
            market_signals.append(f"🔴 连板高度下降 ({max_height}板 → {max_height_today}板)")
        else:
            market_signals.append(f"🟢 连板高度稳定 (今日最高{max_height_today}板)")
    
    # 4. 情绪周期风险（支持新的周期细分）
    if emotion_cycle == "强过热期":
        market_risk += 30
        market_signals.append("🔴 当前处于强过热期，建议逐步减仓")
    elif emotion_cycle == "弱过热期":
        market_risk += 15
        market_signals.append("🟡 当前处于弱过热期，谨慎持有，仓位控制在20-30%")
    elif emotion_cycle == "过热期":
        market_risk += 20
        market_signals.append("🟡 当前处于过热期，注意及时止盈")
    elif emotion_cycle == "退潮期":
        market_risk += 40
        market_signals.append("🔴 当前处于退潮期，建议清仓观望")
    
    # 风险评级
    if market_risk >= 50:
        risk_level_text = "🔴 高风险"
        operation_advice = "减仓/止盈，建议仓位30%以下"
    elif market_risk >= 30:
        risk_level_text = "🟡 中等风险"
        operation_advice = "持仓观察，建议仓位50%左右"
    else:
        risk_level_text = "🟢 低风险"
        operation_advice = "正常持仓，根据策略执行"
    
    return {
        'market_risk': market_risk,
        'risk_level_text': risk_level_text,
        'market_signals': market_signals,
        'operation_advice': operation_advice
    }
