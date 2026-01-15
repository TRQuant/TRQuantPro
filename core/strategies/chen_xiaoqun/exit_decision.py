"""
退出决策模块

基于陈小群策略的退出逻辑：
- 坚定持有：不爱做T，看准就坚定持有到巅峰
- 退出时机：只有明显见顶或预计停牌才走
"""

from typing import Dict, Optional
from datetime import datetime, timedelta
import pandas as pd


def should_exit_position(
    code: str,
    buy_date: str,
    current_date: str,
    current_price: float,
    cost_price: float,
    zhaban_rate: float,
    limit_up_count: int,
    max_height: int,
    emotion_cycle: str,
    min_holding_days: int = 3
) -> Dict:
    """
    判断是否应该退出持仓
    
    基于陈小群策略：
    - 坚定持有：至少持有min_holding_days天，除非出现明显见顶信号
    - 退出时机：只有明显见顶或预计停牌才走
    
    Args:
        code: 股票代码
        buy_date: 买入日期（YYYY-MM-DD）
        current_date: 当前日期（YYYY-MM-DD）
        current_price: 当前价格
        cost_price: 成本价格
        zhaban_rate: 当前炸板率（百分比）
        limit_up_count: 当前涨停家数
        max_height: 当前最高连板高度
        emotion_cycle: 当前情绪周期
        min_holding_days: 最小持有天数（默认3天）
    
    Returns:
        {
            'should_exit': bool,  # 是否应该退出
            'exit_reason': str,  # 退出原因
            'exit_type': str,  # 退出类型（'stop_loss'/'take_profit'/'climax'/'time_limit'）
            'holding_days': int,  # 持有天数
            'pnl_pct': float  # 盈亏百分比
        }
    """
    # 计算持有天数
    buy_dt = pd.to_datetime(buy_date)
    current_dt = pd.to_datetime(current_date)
    holding_days = (current_dt - buy_dt).days
    
    # 计算盈亏
    pnl_pct = (current_price - cost_price) / cost_price
    
    # 默认不退出
    should_exit = False
    exit_reason = ""
    exit_type = ""
    
    # ========== 退出条件1：明显见顶信号（最高优先级） ==========
    
    # 1.1 炸板率>40%且持有2天以上（见顶信号）
    if zhaban_rate > 40 and holding_days >= 2:
        should_exit = True
        exit_reason = f"炸板率{zhaban_rate:.1f}%过高（见顶信号）"
        exit_type = "climax"
        return {
            'should_exit': should_exit,
            'exit_reason': exit_reason,
            'exit_type': exit_type,
            'holding_days': holding_days,
            'pnl_pct': pnl_pct
        }
    
    # 1.2 持有3天以上且亏损>8%（止损）
    if holding_days >= 3 and pnl_pct < -0.08:
        should_exit = True
        exit_reason = f"持有{holding_days}天亏损{pnl_pct*100:.1f}%（止损）"
        exit_type = "stop_loss"
        return {
            'should_exit': should_exit,
            'exit_reason': exit_reason,
            'exit_type': exit_type,
            'holding_days': holding_days,
            'pnl_pct': pnl_pct
        }
    
    # 1.3 持有3天以上且盈利>20%（止盈，锁定利润）
    if holding_days >= 3 and pnl_pct > 0.20:
        should_exit = True
        exit_reason = f"持有{holding_days}天盈利{pnl_pct*100:.1f}%（止盈）"
        exit_type = "take_profit"
        return {
            'should_exit': should_exit,
            'exit_reason': exit_reason,
            'exit_type': exit_type,
            'holding_days': holding_days,
            'pnl_pct': pnl_pct
        }
    
    # ========== 退出条件2：时间限制（次优先级） ==========
    
    # 2.1 持有5天以上（时间限制，锁定利润或止损）
    if holding_days >= 5:
        should_exit = True
        if pnl_pct > 0:
            exit_reason = f"持有{holding_days}天盈利{pnl_pct*100:.1f}%（时间限制，锁定利润）"
            exit_type = "take_profit"
        else:
            exit_reason = f"持有{holding_days}天亏损{pnl_pct*100:.1f}%（时间限制，止损）"
            exit_type = "stop_loss"
        return {
            'should_exit': should_exit,
            'exit_reason': exit_reason,
            'exit_type': exit_type,
            'holding_days': holding_days,
            'pnl_pct': pnl_pct
        }
    
    # ========== 退出条件3：强过热期持续减仓（最低优先级） ==========
    
    # 3.1 强过热期且持有2天以上，可以减仓（但不要全部清仓）
    if emotion_cycle == "强过热期" and holding_days >= 2:
        # 只有在亏损或盈利很小的情况下才退出
        if pnl_pct < -0.03 or (pnl_pct < 0.05 and holding_days >= 3):
            should_exit = True
            exit_reason = f"强过热期且持有{holding_days}天，盈利{pnl_pct*100:.1f}%（减仓）"
            exit_type = "climax"
            return {
                'should_exit': should_exit,
                'exit_reason': exit_reason,
                'exit_type': exit_type,
                'holding_days': holding_days,
                'pnl_pct': pnl_pct
            }
    
    # ========== 默认：继续持有 ==========
    
    return {
        'should_exit': False,
        'exit_reason': f"继续持有（持有{holding_days}天，盈利{pnl_pct*100:.1f}%）",
        'exit_type': "hold",
        'holding_days': holding_days,
        'pnl_pct': pnl_pct
    }


def should_reduce_position(
    code: str,
    buy_date: str,
    current_date: str,
    current_price: float,
    cost_price: float,
    zhaban_rate: float,
    emotion_cycle: str,
    min_holding_days: int = 2
) -> Dict:
    """
    判断是否应该减仓（部分卖出）
    
    在强过热期可以逐步减仓，但不要全部清仓
    
    Args:
        code: 股票代码
        buy_date: 买入日期
        current_date: 当前日期
        current_price: 当前价格
        cost_price: 成本价格
        zhaban_rate: 当前炸板率
        emotion_cycle: 当前情绪周期
        min_holding_days: 最小持有天数（默认2天）
    
    Returns:
        {
            'should_reduce': bool,  # 是否应该减仓
            'reduce_ratio': float,  # 减仓比例（0-1）
            'reason': str  # 减仓原因
        }
    """
    # 计算持有天数
    buy_dt = pd.to_datetime(buy_date)
    current_dt = pd.to_datetime(current_date)
    holding_days = (current_dt - buy_dt).days
    
    # 计算盈亏
    pnl_pct = (current_price - cost_price) / cost_price
    
    # 默认不减仓
    should_reduce = False
    reduce_ratio = 0.0
    reason = ""
    
    # 减仓条件：强过热期且持有2天以上
    if emotion_cycle == "强过热期" and holding_days >= min_holding_days:
        # 如果盈利，减仓50%锁定利润
        if pnl_pct > 0.05:
            should_reduce = True
            reduce_ratio = 0.5
            reason = f"强过热期且盈利{pnl_pct*100:.1f}%，减仓50%锁定利润"
        # 如果亏损，减仓30%降低风险
        elif pnl_pct < -0.03:
            should_reduce = True
            reduce_ratio = 0.3
            reason = f"强过热期且亏损{pnl_pct*100:.1f}%，减仓30%降低风险"
    
    return {
        'should_reduce': should_reduce,
        'reduce_ratio': reduce_ratio,
        'reason': reason
    }
