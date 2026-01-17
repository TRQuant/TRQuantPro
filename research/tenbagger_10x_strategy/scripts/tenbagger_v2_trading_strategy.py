#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股早期识别系统 V2.0 - 交易策略设计
=====================================

入场策略:
- 信号: L2精选 + 市场趋势确认
- 时机: S1阶段优先，量价突破确认
- 买入: 分批建仓，首次50%，确认后加仓

仓位管理:
- 单票上限: 25% (激进)
- 持仓数量: 5-8只 (集中)
- 现金预留: 根据市场环境动态调整

风险控制:
- 止损: -15% 无条件执行
- 移动止盈: 利润回撤20%触发
- 目标止盈: 翻倍后减仓50%
- 时间止损: 30天无表现考虑替换

动态调整:
- 每周调仓检查
- 市场环境变化时调整仓位
- 个股基本面变化时重新评估

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_v2_trading_strategy.py
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import logging

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# 交易信号
# ============================================================

class TradeSignal(Enum):
    """交易信号"""
    STRONG_BUY = "强烈买入"
    BUY = "买入"
    HOLD = "持有"
    REDUCE = "减仓"
    SELL = "卖出"
    STRONG_SELL = "强烈卖出"


class EntryTiming(Enum):
    """入场时机"""
    IMMEDIATE = "立即入场"
    BREAKTHROUGH = "突破确认后入场"
    PULLBACK = "回调后入场"
    WAIT = "等待更好时机"


# ============================================================
# 入场策略
# ============================================================

@dataclass
class EntryStrategy:
    """入场策略"""
    signal: TradeSignal
    timing: EntryTiming
    
    # 入场参数
    target_price: float = 0.0           # 目标买入价
    price_range: Tuple[float, float] = (0.0, 0.0)  # 价格区间
    
    # 分批建仓
    batch_count: int = 2                # 分批次数
    first_batch_ratio: float = 0.5      # 首批比例
    
    # 确认条件
    volume_confirm: bool = True         # 需要成交量确认
    trend_confirm: bool = True          # 需要趋势确认
    
    # 理由
    reasons: List[str] = field(default_factory=list)
    
    def get_batch_ratios(self) -> List[float]:
        """获取分批比例"""
        if self.batch_count <= 1:
            return [1.0]
        
        first = self.first_batch_ratio
        remaining = 1 - first
        other_batch = remaining / (self.batch_count - 1)
        
        return [first] + [other_batch] * (self.batch_count - 1)


# ============================================================
# 仓位管理
# ============================================================

@dataclass
class PositionConfig:
    """仓位配置"""
    # 总仓位
    max_total_position: float = 0.8     # 最大总仓位 80%
    min_cash_reserve: float = 0.1       # 最小现金储备 10%
    
    # 单只股票
    max_single_position: float = 0.25   # 单票最大 25%
    min_single_position: float = 0.05   # 单票最小 5%
    
    # 持仓数量
    max_holdings: int = 8               # 最多持仓数
    min_holdings: int = 3               # 最少持仓数
    optimal_holdings: int = 5           # 最优持仓数
    
    # 行业分散
    max_industry_ratio: float = 0.40    # 单一行业最大 40%


class PositionManager:
    """仓位管理器"""
    
    def __init__(self, config: PositionConfig = None):
        self.config = config or PositionConfig()
    
    def calculate_position_size(self, 
                                 total_equity: float,
                                 stock_score: float,
                                 stock_stage: str,
                                 market_state: str,
                                 current_holdings: int) -> float:
        """计算仓位大小"""
        # 基础仓位
        base_position = total_equity * self.config.max_single_position
        
        # 根据得分调整
        score_multiplier = 1.0
        if stock_score >= 80:
            score_multiplier = 1.2
        elif stock_score >= 70:
            score_multiplier = 1.0
        elif stock_score >= 60:
            score_multiplier = 0.8
        else:
            score_multiplier = 0.6
        
        # 根据阶段调整
        stage_multiplier = 1.0
        if stock_stage in ['S0', 'S1']:
            stage_multiplier = 1.1  # 早期阶段加仓
        elif stock_stage in ['S4', 'S5']:
            stage_multiplier = 0.7  # 后期阶段减仓
        
        # 根据市场状态调整
        market_multiplier = 1.0
        if market_state == "强势上涨":
            market_multiplier = 1.2
        elif market_state == "上涨":
            market_multiplier = 1.0
        elif market_state == "中性震荡":
            market_multiplier = 0.8
        elif market_state == "下跌":
            market_multiplier = 0.5
        else:  # 强势下跌
            market_multiplier = 0.3
        
        # 根据当前持仓数调整
        if current_holdings >= self.config.max_holdings:
            holdings_multiplier = 0.0  # 不能再买
        elif current_holdings >= self.config.optimal_holdings:
            holdings_multiplier = 0.8
        else:
            holdings_multiplier = 1.0
        
        # 计算最终仓位
        final_position = base_position * score_multiplier * stage_multiplier * market_multiplier * holdings_multiplier
        
        # 限制范围
        final_position = max(
            total_equity * self.config.min_single_position,
            min(final_position, total_equity * self.config.max_single_position)
        )
        
        return final_position
    
    def should_add_position(self, 
                            current_position: float,
                            profit_pct: float,
                            stock_score: float) -> Tuple[bool, float]:
        """判断是否应该加仓"""
        # 已达到上限
        if current_position >= self.config.max_single_position:
            return False, 0
        
        # 亏损时不加仓
        if profit_pct < 0:
            return False, 0
        
        # 盈利>10%且得分高，考虑加仓
        if profit_pct > 10 and stock_score >= 70:
            add_ratio = min(0.1, self.config.max_single_position - current_position)
            return True, add_ratio
        
        return False, 0
    
    def should_reduce_position(self,
                               profit_pct: float,
                               holding_days: int,
                               stock_score: float) -> Tuple[bool, float]:
        """判断是否应该减仓"""
        # 翻倍止盈
        if profit_pct >= 100:
            return True, 0.5  # 减仓50%
        
        # 大幅盈利
        if profit_pct >= 80:
            return True, 0.3  # 减仓30%
        
        # 长时间持有无收益
        if holding_days > 60 and profit_pct < 10:
            return True, 0.5  # 减仓50%
        
        # 得分下降
        if stock_score < 50:
            return True, 0.5  # 减仓50%
        
        return False, 0


# ============================================================
# 风险控制
# ============================================================

@dataclass
class RiskConfig:
    """风险配置"""
    # 止损
    fixed_stop_loss: float = -0.15      # 固定止损 -15%
    trailing_stop_trigger: float = 0.50  # 移动止盈触发点 50%
    trailing_stop_ratio: float = 0.20   # 移动止盈回撤比例 20%
    
    # 止盈
    target_profit_1: float = 1.00       # 第一目标 100%
    target_profit_2: float = 2.00       # 第二目标 200%
    target_profit_3: float = 5.00       # 第三目标 500%
    
    # 减仓比例
    reduce_ratio_1: float = 0.30        # 第一目标减仓 30%
    reduce_ratio_2: float = 0.30        # 第二目标减仓 30%
    
    # 时间
    max_holding_days: int = 120         # 最长持有天数
    no_profit_days: int = 30            # 无盈利天数限制


class RiskController:
    """风险控制器"""
    
    def __init__(self, config: RiskConfig = None):
        self.config = config or RiskConfig()
    
    def check_stop_loss(self, profit_pct: float) -> Tuple[bool, str]:
        """检查止损"""
        if profit_pct <= self.config.fixed_stop_loss * 100:
            return True, f"触发固定止损 ({profit_pct:.1f}%)"
        return False, ""
    
    def check_trailing_stop(self, 
                            profit_pct: float,
                            highest_profit_pct: float) -> Tuple[bool, str]:
        """检查移动止盈"""
        # 只有盈利超过触发点才启用
        if highest_profit_pct < self.config.trailing_stop_trigger * 100:
            return False, ""
        
        # 计算从最高点的回撤
        drawdown = (profit_pct - highest_profit_pct) / highest_profit_pct
        
        if drawdown <= -self.config.trailing_stop_ratio:
            return True, f"触发移动止盈 (从高点{highest_profit_pct:.1f}%回撤至{profit_pct:.1f}%)"
        
        return False, ""
    
    def check_target_profit(self, profit_pct: float) -> Tuple[bool, float, str]:
        """检查目标止盈"""
        if profit_pct >= self.config.target_profit_3 * 100:
            return True, 0.5, f"达到第三目标 {self.config.target_profit_3*100:.0f}%，建议减仓50%"
        elif profit_pct >= self.config.target_profit_2 * 100:
            return True, self.config.reduce_ratio_2, f"达到第二目标 {self.config.target_profit_2*100:.0f}%"
        elif profit_pct >= self.config.target_profit_1 * 100:
            return True, self.config.reduce_ratio_1, f"达到第一目标 {self.config.target_profit_1*100:.0f}%"
        
        return False, 0, ""
    
    def check_time_stop(self, 
                        holding_days: int,
                        profit_pct: float) -> Tuple[bool, str]:
        """检查时间止损"""
        # 长期无盈利
        if holding_days >= self.config.no_profit_days and profit_pct < 10:
            return True, f"持有{holding_days}天，盈利仅{profit_pct:.1f}%，考虑换股"
        
        # 超长持有
        if holding_days >= self.config.max_holding_days:
            return True, f"持有超过{self.config.max_holding_days}天，重新评估"
        
        return False, ""
    
    def get_risk_signals(self, 
                         profit_pct: float,
                         highest_profit_pct: float,
                         holding_days: int) -> List[Dict]:
        """获取所有风险信号"""
        signals = []
        
        # 止损检查
        trigger, msg = self.check_stop_loss(profit_pct)
        if trigger:
            signals.append({
                'type': 'stop_loss',
                'action': 'sell',
                'urgency': 'high',
                'message': msg
            })
        
        # 移动止盈检查
        trigger, msg = self.check_trailing_stop(profit_pct, highest_profit_pct)
        if trigger:
            signals.append({
                'type': 'trailing_stop',
                'action': 'sell',
                'urgency': 'high',
                'message': msg
            })
        
        # 目标止盈检查
        trigger, ratio, msg = self.check_target_profit(profit_pct)
        if trigger:
            signals.append({
                'type': 'target_profit',
                'action': 'reduce',
                'reduce_ratio': ratio,
                'urgency': 'medium',
                'message': msg
            })
        
        # 时间止损检查
        trigger, msg = self.check_time_stop(holding_days, profit_pct)
        if trigger:
            signals.append({
                'type': 'time_stop',
                'action': 'review',
                'urgency': 'low',
                'message': msg
            })
        
        return signals


# ============================================================
# 交易策略主类
# ============================================================

class TenbaggerV2TradingStrategy:
    """十倍股V2交易策略"""
    
    def __init__(self):
        self.position_manager = PositionManager()
        self.risk_controller = RiskController()
    
    def generate_entry_strategy(self, 
                                 stock_data: Dict,
                                 market_state: str) -> EntryStrategy:
        """生成入场策略"""
        score = stock_data.get('adjusted_score', 0)
        stage = stock_data.get('stage', 'S3')
        price = stock_data.get('current_price', 0)
        ma_bullish = stock_data.get('ma_bullish', False)
        volume_ratio = stock_data.get('volume_ratio', 1.0)
        
        # 确定信号
        if score >= 80 and stage in ['S0', 'S1']:
            signal = TradeSignal.STRONG_BUY
        elif score >= 70 and stage in ['S0', 'S1', 'S2']:
            signal = TradeSignal.BUY
        elif score >= 60:
            signal = TradeSignal.HOLD
        else:
            signal = TradeSignal.WAIT if score >= 50 else TradeSignal.SELL
        
        # 确定时机
        if ma_bullish and volume_ratio > 1.2:
            timing = EntryTiming.IMMEDIATE
        elif ma_bullish:
            timing = EntryTiming.BREAKTHROUGH
        else:
            timing = EntryTiming.PULLBACK
        
        # 根据市场状态调整
        if market_state in ["下跌", "强势下跌"]:
            if signal == TradeSignal.STRONG_BUY:
                signal = TradeSignal.BUY
            elif signal == TradeSignal.BUY:
                signal = TradeSignal.HOLD
            timing = EntryTiming.WAIT
        
        # 构建策略
        strategy = EntryStrategy(
            signal=signal,
            timing=timing,
            target_price=price,
            price_range=(price * 0.95, price * 1.05),
            batch_count=2 if signal in [TradeSignal.STRONG_BUY, TradeSignal.BUY] else 1,
            first_batch_ratio=0.5
        )
        
        # 添加理由
        strategy.reasons = [
            f"综合得分: {score:.1f}",
            f"成长阶段: {stage}",
            f"市场状态: {market_state}",
            f"均线状态: {'多头' if ma_bullish else '非多头'}",
            f"量比: {volume_ratio:.2f}"
        ]
        
        return strategy
    
    def generate_exit_strategy(self, 
                                position_data: Dict) -> Dict:
        """生成出场策略"""
        profit_pct = position_data.get('profit_pct', 0)
        highest_profit_pct = position_data.get('highest_profit_pct', profit_pct)
        holding_days = position_data.get('holding_days', 0)
        
        # 获取风险信号
        risk_signals = self.risk_controller.get_risk_signals(
            profit_pct, highest_profit_pct, holding_days
        )
        
        # 确定出场策略
        if not risk_signals:
            return {
                'action': 'hold',
                'signal': TradeSignal.HOLD,
                'message': '无触发信号，继续持有',
                'risk_signals': []
            }
        
        # 找最高优先级信号
        high_urgency = [s for s in risk_signals if s['urgency'] == 'high']
        
        if high_urgency:
            signal = high_urgency[0]
            return {
                'action': signal['action'],
                'signal': TradeSignal.STRONG_SELL if signal['action'] == 'sell' else TradeSignal.REDUCE,
                'reduce_ratio': signal.get('reduce_ratio', 1.0),
                'message': signal['message'],
                'risk_signals': risk_signals
            }
        
        medium_urgency = [s for s in risk_signals if s['urgency'] == 'medium']
        if medium_urgency:
            signal = medium_urgency[0]
            return {
                'action': signal['action'],
                'signal': TradeSignal.REDUCE,
                'reduce_ratio': signal.get('reduce_ratio', 0.3),
                'message': signal['message'],
                'risk_signals': risk_signals
            }
        
        # 低优先级
        return {
            'action': 'review',
            'signal': TradeSignal.HOLD,
            'message': risk_signals[0]['message'],
            'risk_signals': risk_signals
        }
    
    def generate_weekly_plan(self, 
                              selections: List[Dict],
                              current_positions: Dict,
                              market_state: str,
                              total_equity: float) -> Dict:
        """生成周度交易计划"""
        plan = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'market_state': market_state,
            'total_equity': total_equity,
            'recommendations': [],
            'position_adjustments': [],
            'risk_alerts': [],
            'summary': {}
        }
        
        # 新股推荐
        for stock in selections[:5]:  # 最多5只
            entry_strategy = self.generate_entry_strategy(stock, market_state)
            
            if entry_strategy.signal in [TradeSignal.STRONG_BUY, TradeSignal.BUY]:
                position_size = self.position_manager.calculate_position_size(
                    total_equity=total_equity,
                    stock_score=stock.get('adjusted_score', 0),
                    stock_stage=stock.get('stage', ''),
                    market_state=market_state,
                    current_holdings=len(current_positions)
                )
                
                plan['recommendations'].append({
                    'code': stock.get('code'),
                    'name': stock.get('name', ''),
                    'signal': entry_strategy.signal.value,
                    'timing': entry_strategy.timing.value,
                    'score': stock.get('adjusted_score', 0),
                    'stage': stock.get('stage', ''),
                    'target_position': position_size,
                    'target_price': entry_strategy.target_price,
                    'batch_plan': entry_strategy.get_batch_ratios(),
                    'reasons': entry_strategy.reasons
                })
        
        # 持仓检查
        for code, pos in current_positions.items():
            exit_strategy = self.generate_exit_strategy(pos)
            
            if exit_strategy['action'] != 'hold':
                plan['position_adjustments'].append({
                    'code': code,
                    'action': exit_strategy['action'],
                    'signal': exit_strategy['signal'].value,
                    'message': exit_strategy['message'],
                    'reduce_ratio': exit_strategy.get('reduce_ratio', 0)
                })
            
            if exit_strategy['risk_signals']:
                for signal in exit_strategy['risk_signals']:
                    plan['risk_alerts'].append({
                        'code': code,
                        'type': signal['type'],
                        'urgency': signal['urgency'],
                        'message': signal['message']
                    })
        
        # 汇总
        plan['summary'] = {
            'new_recommendations': len(plan['recommendations']),
            'adjustments_needed': len(plan['position_adjustments']),
            'risk_alerts': len(plan['risk_alerts']),
            'market_advice': self._get_market_advice(market_state)
        }
        
        return plan
    
    def _get_market_advice(self, market_state: str) -> str:
        """获取市场建议"""
        advice = {
            "强势上涨": "市场强势，积极参与，可适当追涨龙头",
            "上涨": "市场向好，按计划执行，注意分批建仓",
            "中性震荡": "市场震荡，控制仓位，精选个股",
            "下跌": "市场转弱，减少操作，保留现金",
            "强势下跌": "市场危险，建议观望，不宜入场"
        }
        return advice.get(market_state, "保持观察")
    
    def print_weekly_plan(self, plan: Dict):
        """打印周度计划"""
        print(f"\n{'='*70}")
        print(f"📅 十倍股V2周度交易计划")
        print(f"{'='*70}")
        print(f"日期: {plan['date']}")
        print(f"市场状态: {plan['market_state']}")
        print(f"总权益: {plan['total_equity']:,.0f}")
        
        print(f"\n📈 市场建议: {plan['summary']['market_advice']}")
        
        if plan['recommendations']:
            print(f"\n🌟 新股推荐 ({len(plan['recommendations'])}只):")
            print("-" * 60)
            for i, rec in enumerate(plan['recommendations'], 1):
                print(f"\n{i}. {rec['code']} {rec['name']}")
                print(f"   信号: {rec['signal']} | 时机: {rec['timing']}")
                print(f"   得分: {rec['score']:.1f} | 阶段: {rec['stage']}")
                print(f"   目标仓位: {rec['target_position']:,.0f}")
                print(f"   分批计划: {[f'{r*100:.0f}%' for r in rec['batch_plan']]}")
                print(f"   理由: {'; '.join(rec['reasons'][:3])}")
        
        if plan['position_adjustments']:
            print(f"\n⚠️ 仓位调整 ({len(plan['position_adjustments'])}只):")
            print("-" * 60)
            for adj in plan['position_adjustments']:
                print(f"   {adj['code']}: {adj['signal']} - {adj['message']}")
                if adj.get('reduce_ratio'):
                    print(f"   建议减仓: {adj['reduce_ratio']*100:.0f}%")
        
        if plan['risk_alerts']:
            print(f"\n🚨 风险提示 ({len(plan['risk_alerts'])}条):")
            print("-" * 60)
            for alert in plan['risk_alerts']:
                urgency_icon = "🔴" if alert['urgency'] == 'high' else "🟡" if alert['urgency'] == 'medium' else "🟢"
                print(f"   {urgency_icon} {alert['code']}: {alert['message']}")
        
        print(f"\n{'='*70}")


# ============================================================
# 测试
# ============================================================

def test_trading_strategy():
    """测试交易策略"""
    strategy = TenbaggerV2TradingStrategy()
    
    # 模拟数据
    mock_selections = [
        {
            'code': '300750.XSHE',
            'name': '宁德时代',
            'adjusted_score': 78.5,
            'stage': 'S1',
            'current_price': 180.0,
            'ma_bullish': True,
            'volume_ratio': 1.5
        },
        {
            'code': '002475.XSHE',
            'name': '立讯精密',
            'adjusted_score': 72.3,
            'stage': 'S2',
            'current_price': 35.0,
            'ma_bullish': True,
            'volume_ratio': 1.2
        }
    ]
    
    mock_positions = {
        '600519.XSHG': {
            'profit_pct': 25.5,
            'highest_profit_pct': 30.0,
            'holding_days': 45
        },
        '000858.XSHE': {
            'profit_pct': -12.0,
            'highest_profit_pct': 5.0,
            'holding_days': 20
        }
    }
    
    # 生成周度计划
    plan = strategy.generate_weekly_plan(
        selections=mock_selections,
        current_positions=mock_positions,
        market_state="上涨",
        total_equity=1000000
    )
    
    # 打印计划
    strategy.print_weekly_plan(plan)


if __name__ == "__main__":
    test_trading_strategy()
