"""
情绪周期判断模块

基于第一性原理 + 陈小群战法，判断市场情绪周期。

核心指标权重分配：
1. 涨停家数：40%（赚钱效应，最重要）
2. 连板高度：20%（情绪强度验证）
3. 炸板率：20%（风险信号）
4. 资金态度：20%（大盘主力 + 行业资金）

判断标准（基于2025-2026年市场数据优化）：
- 退潮期: <20只, <3板, >40%炸板率
- 启动期: 20-50只, 3-5板, 10-25%炸板率
- 加速期: 50-100只, 4-8板, 15-30%炸板率
- 过热期: >100只, >8板, >30%炸板率

周期细分（新增）：
- 强加速期: 50-80只, 4-6板, 15-25%炸板率（仓位60%+）
- 弱过热期: 80-120只, 6-10板, 25-35%炸板率（仓位20-30%，允许交易）
- 强过热期: >120只, >10板, >35%炸板率（仓位10-20%，逐步减仓）
"""

from typing import Dict, List, Optional


def judge_emotion_cycle(
    limit_up_count: int,
    max_height: int,
    zhaban_rate: float,
    avg_inflow: float,
    fund_sentiment_score: float = 0.0
) -> Dict:
    """
    判断市场情绪周期 - 基于第一性原理 + 陈小群战法
    
    第一性原理分析：
    市场情绪 = 赚钱效应 + 资金态度 + 风险信号
    
    核心指标权重分配（基于第一性原理）：
    1. 涨停家数：40%（赚钱效应，最重要）
    2. 连板高度：20%（情绪强度验证）
    3. 炸板率：20%（风险信号）
    4. 资金态度：20%（大盘主力 + 行业资金）
    
    判断标准（基于2025-2026年市场数据优化）:
    - 退潮期: <20只, <3板, >40%炸板率
    - 启动期: 20-50只, 3-5板, 10-25%炸板率
    - 加速期: 50-100只, 4-8板, 15-30%炸板率
    - 过热期: >100只, >8板, >30%炸板率
    
    周期细分（新增）:
    - 强加速期: 50-80只, 4-6板, 15-25%炸板率（仓位60%+）
    - 弱过热期: 80-120只, 6-10板, 25-35%炸板率（仓位20-30%，允许交易）
    - 强过热期: >120只, >10板, >35%炸板率（仓位10-20%，逐步减仓）
    
    Args:
        limit_up_count: 涨停家数
        max_height: 最高连板高度
        zhaban_rate: 炸板率（百分比，如36.65表示36.65%）
        avg_inflow: 大盘主力净流入百分比（如-2.26表示-2.26%）
        fund_sentiment_score: 资金态度评分（范围-2.0到+2.0，已在外部计算）
    
    Returns:
        {
            'cycle': 情绪周期（'退潮期'/'启动期'/'强加速期'/'加速期'/'弱过热期'/'强过热期'）,
            'position': 建议仓位（'0%'/'10%'/'60%+'/'50%+'/'20-30%'/'10-20%'）,
            'strategy': 推荐策略（'空仓等待'/'首板卡位术（10%试错仓）'/'龙头战法（重仓持有）'/'精选龙头（谨慎持有）'/'逐步减仓'）,
            'limit_up_count': 涨停家数,
            'max_height': 最高连板高度,
            'zhaban_rate': 炸板率,
            'avg_inflow': 大盘主力净流入百分比,
            'confidence_score': 置信度分数（0-5.0）,
            'confidence_level': 置信度等级（'高'/'中'/'低'）,
            'confidence_icon': 置信度图标（'🟢'/'🟡'/'🔴'）,
            'factors': 判断依据列表
        }
    """
    # 初始化置信度分数（总分5.0）
    confidence_score = 0.0
    factors: List[str] = []
    
    # ========== 1. 主要依据：涨停家数（权重40%，最重要） ==========
    # 基于2025-2026年市场数据优化判断标准
    if limit_up_count < 20:
        cycle = "退潮期"
        position = "0%"
        strategy = "空仓等待"
        confidence_score += 2.0  # 40%权重，满分2.0
        factors.append(f"涨停家数{limit_up_count}只（<20只，退潮期特征，权重40%）")
    elif limit_up_count < 50:
        cycle = "启动期"
        position = "10%"
        strategy = "首板卡位术（10%试错仓）"
        confidence_score += 2.0
        factors.append(f"涨停家数{limit_up_count}只（20-50只，启动期特征，权重40%）")
    elif limit_up_count < 80:
        # 强加速期：50-80只
        cycle = "强加速期"
        position = "60%+"
        strategy = "龙头战法（重仓持有）"
        confidence_score += 2.0
        factors.append(f"涨停家数{limit_up_count}只（50-80只，强加速期特征，权重40%）")
    elif limit_up_count < 100:
        # 加速期：80-100只（但接近过热期，需要更谨慎）
        # 如果连板高度>7板，可能已经接近过热期，降低仓位
        if max_height > 7:
            cycle = "弱过热期"  # 接近过热期，视为弱过热期
            position = "20-30%"
            strategy = "精选龙头（谨慎持有）"
            factors.append(f"涨停家数{limit_up_count}只（80-100只）+ 连板{max_height}板（>7板，接近过热期，权重40%）")
        else:
            cycle = "加速期"
            position = "50%+"
            strategy = "龙头战法（重仓持有）"
            factors.append(f"涨停家数{limit_up_count}只（80-100只，加速期特征，权重40%）")
        confidence_score += 2.0
    elif limit_up_count < 120:
        # 弱过热期：100-120只（允许交易）
        cycle = "弱过热期"
        position = "20-30%"
        strategy = "精选龙头（谨慎持有）"
        confidence_score += 2.0
        factors.append(f"涨停家数{limit_up_count}只（100-120只，弱过热期特征，权重40%）")
    else:
        # 强过热期：>120只
        cycle = "强过热期"
        position = "10-20%"
        strategy = "逐步减仓"
        confidence_score += 2.0
        factors.append(f"涨停家数{limit_up_count}只（>120只，强过热期特征，权重40%）")
    
    # ========== 2. 连板高度验证（权重20%，情绪强度验证） ==========
    height_score = 0.0
    if cycle == "退潮期" and max_height < 3:
        height_score = 1.0  # 20%权重，满分1.0
        factors.append(f"连板高度{max_height}板（<3板，符合退潮期，权重20%）")
    elif cycle == "启动期" and 3 <= max_height <= 5:
        height_score = 1.0
        factors.append(f"连板高度{max_height}板（3-5板，符合启动期，权重20%）")
    elif cycle == "强加速期" and 4 <= max_height <= 6:
        height_score = 1.0
        factors.append(f"连板高度{max_height}板（4-6板，符合强加速期，权重20%）")
    elif cycle == "加速期" and 4 <= max_height <= 8:
        height_score = 1.0
        factors.append(f"连板高度{max_height}板（4-8板，符合加速期，权重20%）")
    elif cycle == "弱过热期" and 6 <= max_height <= 10:
        height_score = 1.0
        factors.append(f"连板高度{max_height}板（6-10板，符合弱过热期，权重20%）")
    elif cycle == "强过热期" and max_height > 10:
        height_score = 1.0
        factors.append(f"连板高度{max_height}板（>10板，符合强过热期，权重20%）")
    elif cycle == "启动期" and max_height >= 3 and limit_up_count >= 45:
        # 有3板以上且涨停数接近50，可能进入加速期
        cycle = "强加速期"
        position = "60%+"
        strategy = "龙头战法（重仓持有）"
        height_score = 1.0
        factors.append(f"连板高度{max_height}板+涨停数{limit_up_count}只（接近强加速期，权重20%）")
    elif max_height == 0:
        height_score = 0.3  # 无连板数据，给部分分
        factors.append(f"连板高度{max_height}板（无连板数据，权重20%，部分得分）")
    else:
        # 连板高度与周期不完全匹配，给部分分
        height_score = 0.5
        factors.append(f"连板高度{max_height}板（与周期不完全匹配，权重20%，部分得分）")
    
    confidence_score += height_score
    
    # ========== 3. 炸板率验证（权重20%，风险信号） ==========
    risk_score = 0.0
    if cycle == "退潮期" and zhaban_rate > 40:
        risk_score = 1.0  # 20%权重，满分1.0
        factors.append(f"炸板率{zhaban_rate:.1f}%（>40%，确认退潮期，权重20%）")
    elif cycle == "启动期" and 10 <= zhaban_rate <= 25:
        risk_score = 1.0
        factors.append(f"炸板率{zhaban_rate:.1f}%（10-25%，符合启动期，权重20%）")
    elif cycle == "强加速期" and 15 <= zhaban_rate <= 25:
        risk_score = 1.0
        factors.append(f"炸板率{zhaban_rate:.1f}%（15-25%，符合强加速期，权重20%）")
    elif cycle == "加速期" and 15 <= zhaban_rate <= 30:
        risk_score = 1.0
        factors.append(f"炸板率{zhaban_rate:.1f}%（15-30%，符合加速期，权重20%）")
    elif cycle == "弱过热期" and 25 <= zhaban_rate <= 35:
        risk_score = 1.0
        factors.append(f"炸板率{zhaban_rate:.1f}%（25-35%，符合弱过热期，权重20%）")
    elif cycle == "强过热期" and zhaban_rate > 35:
        risk_score = 1.0
        factors.append(f"炸板率{zhaban_rate:.1f}%（>35%，符合强过热期，权重20%）")
    elif cycle in ["加速期", "强加速期"] and zhaban_rate > 30:
        # 炸板率过高，可能进入过热期
        if limit_up_count >= 100:
            cycle = "弱过热期"
            position = "20-30%"
            strategy = "精选龙头（谨慎持有）"
        else:
            cycle = "强过热期"
            position = "10-20%"
            strategy = "逐步减仓"
        risk_score = 1.0
        factors.append(f"炸板率{zhaban_rate:.1f}%（>30%，可能过热，权重20%）")
    elif cycle == "退潮期" and zhaban_rate <= 40:
        risk_score = 0.5  # 退潮期但炸板率不高，给部分分
        factors.append(f"炸板率{zhaban_rate:.1f}%（退潮期但炸板率不高，权重20%，部分得分）")
    else:
        # 炸板率与周期不完全匹配，给部分分
        risk_score = 0.5
        factors.append(f"炸板率{zhaban_rate:.1f}%（与周期不完全匹配，权重20%，部分得分）")
    
    confidence_score += risk_score
    
    # ========== 4. 资金态度验证（权重20%，大盘主力+行业资金） ==========
    # fund_sentiment_score已在外部计算（范围-2.0到+2.0），归一化到0-1.0
    if fund_sentiment_score != 0:
        # 将-2.0~+2.0映射到0~1.0
        fund_score = (fund_sentiment_score + 2.0) / 4.0  # 归一化到0-1.0
        confidence_score += fund_score
        if fund_sentiment_score > 0:
            factors.append(f"资金态度积极（评分{fund_sentiment_score:.1f}，权重20%）")
        else:
            factors.append(f"资金态度谨慎（评分{fund_sentiment_score:.1f}，权重20%）")
    else:
        # 资金态度中性，给部分分
        fund_score = 0.5
        confidence_score += fund_score
        factors.append(f"资金态度中性（权重20%，部分得分）")
    
    # 传统资金流向验证（保留作为补充，但不计入主要评分）
    if avg_inflow > 0.5 and cycle in ["启动期", "加速期"]:
        factors.append(f"💡 补充：大盘主力净流入{avg_inflow:.2f}%（支持上涨周期）")
    elif avg_inflow < -0.5 and cycle == "退潮期":
        factors.append(f"💡 补充：大盘主力净流出{avg_inflow:.2f}%（确认退潮期）")
    elif avg_inflow < -0.5 and cycle != "退潮期":
        factors.append(f"⚠️  补充：大盘主力净流出{avg_inflow:.2f}%（与周期判断不一致，需注意）")
    
    # 计算置信度等级
    if confidence_score >= 4:
        confidence_level = "高"
        confidence_icon = "🟢"
    elif confidence_score >= 3:
        confidence_level = "中"
        confidence_icon = "🟡"
    else:
        confidence_level = "低"
        confidence_icon = "🔴"
    
    return {
        'cycle': cycle,
        'position': position,
        'strategy': strategy,
        'limit_up_count': limit_up_count,
        'max_height': max_height,
        'zhaban_rate': zhaban_rate,
        'avg_inflow': avg_inflow,
        'confidence_score': confidence_score,
        'confidence_level': confidence_level,
        'confidence_icon': confidence_icon,
        'factors': factors
    }


def judge_emotion_cycle_with_confirmation(
    limit_up_count: int,
    max_height: int,
    zhaban_rate: float,
    avg_inflow: float,
    fund_sentiment_score: float = 0.0,
    history_cycles: Optional[List[str]] = None
) -> Dict:
    """
    带确认机制的情绪周期判断
    
    规则：
    1. 如果当前判断的周期与最近2天的周期不一致，需要连续2-3天确认
    2. 如果连续2-3天都是新周期，才确认周期转换
    3. 避免单日数据波动导致的误判
    
    Args:
        limit_up_count: 涨停家数
        max_height: 最高连板高度
        zhaban_rate: 炸板率（百分比）
        avg_inflow: 大盘主力净流入百分比
        fund_sentiment_score: 资金态度评分
        history_cycles: 最近3天的周期历史（列表，从旧到新）
    
    Returns:
        与judge_emotion_cycle相同的字典，可能包含'needs_confirmation'字段
    """
    # 当前周期判断
    current_result = judge_emotion_cycle(
        limit_up_count, max_height, zhaban_rate, avg_inflow, fund_sentiment_score
    )
    current_cycle = current_result['cycle']
    
    # 如果历史周期存在，检查是否需要确认
    if history_cycles and len(history_cycles) >= 2:
        last_2_cycles = history_cycles[-2:]
        last_cycle = last_2_cycles[-1]
        
        if current_cycle != last_cycle:
            # 周期不一致，需要确认
            if len(history_cycles) >= 3:
                # 检查连续2天是否都是新周期
                if current_cycle == history_cycles[-2]:
                    # 连续2天是新周期，确认转换
                    return current_result
                else:
                    # 单日波动，保持原周期
                    # 但使用当前周期的部分信息（如置信度）
                    return {
                        **current_result,
                        'cycle': last_cycle,  # 保持原周期
                        'needs_confirmation': True,
                        'suggested_cycle': current_cycle  # 建议的新周期
                    }
            else:
                # 历史数据不足，需要更多确认
                return {
                    **current_result,
                    'cycle': last_cycle,  # 保持原周期
                    'needs_confirmation': True,
                    'suggested_cycle': current_cycle
                }
    
    # 周期一致或无需确认，直接返回
    return current_result
