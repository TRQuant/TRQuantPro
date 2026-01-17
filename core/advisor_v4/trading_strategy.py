"""
交易策略引擎 - 完整的买卖规则和风控机制

入场规则：
- 模型预测概率 >= 阈值
- 多因子综合得分 TOP N
- 流动性过滤

出场规则：
- 目标止盈: +10%
- 移动止盈: 最高点回撤3%
- 固定止损: -5%
- 时间止损: 持有5天强制平仓

仓位管理：
- 单票仓位: 10%
- 最大持仓: 10只
- 行业分散: 单行业不超过30%

风控规则：
- 大盘熊市减仓50%
- 连续亏损降低仓位
- 最大回撤触发清仓
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SignalType(Enum):
    """信号类型"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class ExitReason(Enum):
    """出场原因"""
    TARGET_PROFIT = "target_profit"     # 目标止盈
    TRAILING_STOP = "trailing_stop"     # 移动止盈
    STOP_LOSS = "stop_loss"             # 固定止损
    TIME_EXIT = "time_exit"             # 时间止损
    MANUAL = "manual"                   # 手动平仓


@dataclass
class TradeSignal:
    """交易信号"""
    code: str
    name: str
    signal_type: SignalType
    signal_date: str
    probability: float          # 模型预测概率
    score: float               # 综合得分
    entry_price: float = 0.0
    target_price: float = 0.0   # 目标价
    stop_loss_price: float = 0.0  # 止损价
    position_size: float = 0.0   # 建议仓位
    factors: Dict = field(default_factory=dict)


@dataclass
class Position:
    """持仓"""
    code: str
    name: str
    entry_date: str
    entry_price: float
    shares: int
    cost: float
    current_price: float = 0.0
    highest_price: float = 0.0  # 持仓期间最高价
    unrealized_pnl: float = 0.0
    unrealized_return: float = 0.0
    holding_days: int = 0
    target_price: float = 0.0
    stop_loss_price: float = 0.0
    trailing_stop_price: float = 0.0
    industry: str = ""


@dataclass 
class Trade:
    """交易记录"""
    code: str
    name: str
    entry_date: str
    entry_price: float
    exit_date: str
    exit_price: float
    shares: int
    pnl: float
    return_pct: float
    holding_days: int
    exit_reason: ExitReason
    industry: str = ""


@dataclass
class TradingConfig:
    """交易配置"""
    # 入场规则
    min_probability: float = 0.5        # 最低预测概率
    min_score: float = 60.0             # 最低综合得分
    min_liquidity: float = 1000.0       # 最低日成交额（万元）
    max_candidates: int = 20            # 最大候选数量
    
    # 出场规则
    target_return: float = 0.10         # 目标收益率 10%
    stop_loss: float = -0.05            # 止损 -5%
    trailing_stop: float = 0.03         # 移动止盈回撤 3%
    max_holding_days: int = 5           # 最大持有天数
    
    # 仓位管理
    position_size: float = 0.10         # 单票仓位 10%
    max_positions: int = 10             # 最大持仓数量
    max_industry_exposure: float = 0.30  # 单行业最大敞口 30%
    
    # 风控规则
    max_drawdown: float = 0.08          # 最大回撤 8%
    market_bear_scale: float = 0.50     # 熊市仓位缩减
    consecutive_loss_scale: float = 0.20  # 连续亏损仓位缩减


class TradingStrategy:
    """交易策略引擎"""
    
    def __init__(self, config: TradingConfig = None, initial_capital: float = 1000000):
        """
        Args:
            config: 交易配置
            initial_capital: 初始资金
        """
        self.config = config or TradingConfig()
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.cash = initial_capital
        
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.daily_equity: List[Dict] = []
        
        self.consecutive_losses = 0
        self.peak_equity = initial_capital
        self.current_drawdown = 0.0
        
        # 市场环境
        self.market_regime = "neutral"  # bull/bear/neutral
    
    def set_market_regime(self, regime: str):
        """设置市场环境"""
        self.market_regime = regime
    
    def calculate_position_size(self, signal: TradeSignal) -> float:
        """计算建议仓位大小"""
        base_size = self.config.position_size
        
        # 根据预测概率调整
        if signal.probability >= 0.8:
            prob_scale = 1.2
        elif signal.probability >= 0.6:
            prob_scale = 1.0
        else:
            prob_scale = 0.8
        
        # 根据市场环境调整
        if self.market_regime == "bear":
            market_scale = self.config.market_bear_scale
        elif self.market_regime == "bull":
            market_scale = 1.2
        else:
            market_scale = 1.0
        
        # 根据连续亏损调整
        if self.consecutive_losses >= 3:
            loss_scale = 1 - self.config.consecutive_loss_scale * min(self.consecutive_losses - 2, 3)
        else:
            loss_scale = 1.0
        
        # 根据回撤调整
        if self.current_drawdown > 0.05:
            drawdown_scale = 0.5
        else:
            drawdown_scale = 1.0
        
        final_size = base_size * prob_scale * market_scale * loss_scale * drawdown_scale
        
        # 限制最大仓位
        return min(final_size, 0.15)
    
    def check_industry_exposure(self, industry: str) -> bool:
        """检查行业敞口"""
        if not industry:
            return True
        
        total_exposure = sum(
            p.cost / self.current_capital 
            for p in self.positions.values() 
            if p.industry == industry
        )
        
        return total_exposure < self.config.max_industry_exposure
    
    def generate_entry_signals(self, 
                               candidates: pd.DataFrame,
                               date: str) -> List[TradeSignal]:
        """生成入场信号
        
        Args:
            candidates: 候选股票DataFrame，需包含probability, total_score等列
            date: 交易日期
        """
        signals = []
        
        # 过滤条件
        filtered = candidates[
            (candidates['probability'] >= self.config.min_probability) &
            (candidates['total_score'] >= self.config.min_score)
        ]
        
        # 流动性过滤
        if 'avg_money' in filtered.columns:
            filtered = filtered[filtered['avg_money'] >= self.config.min_liquidity]
        
        # 按综合得分排序
        filtered = filtered.nlargest(self.config.max_candidates, 'total_score')
        
        for _, row in filtered.iterrows():
            code = row['code']
            
            # 检查是否已持仓
            if code in self.positions:
                continue
            
            # 检查持仓数量
            if len(self.positions) >= self.config.max_positions:
                break
            
            # 检查行业敞口
            industry = row.get('industry', '')
            if not self.check_industry_exposure(industry):
                continue
            
            # 计算仓位
            entry_price = row.get('current_price', row.get('close', 0))
            if entry_price <= 0:
                continue
            
            signal = TradeSignal(
                code=code,
                name=row.get('name', code),
                signal_type=SignalType.BUY,
                signal_date=date,
                probability=row['probability'],
                score=row['total_score'],
                entry_price=entry_price,
                target_price=entry_price * (1 + self.config.target_return),
                stop_loss_price=entry_price * (1 + self.config.stop_loss),
                position_size=self.calculate_position_size(
                    TradeSignal(code=code, name='', signal_type=SignalType.BUY,
                               signal_date=date, probability=row['probability'],
                               score=row['total_score'])
                ),
                factors={
                    'momentum_20d': row.get('momentum_20d', 0),
                    'rel_strength': row.get('rel_strength', 0),
                    'roe': row.get('roe', 0),
                    'industry': industry,
                    # phase6.2: 规则引擎输出（可解释）
                    'rule_score': row.get('rule_score', None),
                    'rule_passed': row.get('rule_passed', None),
                    'rule_reasons': row.get('rule_reasons', None),
                    'total_score_raw': row.get('total_score_raw', None),
                }
            )
            signals.append(signal)
        
        return signals
    
    def check_exit_conditions(self, 
                              position: Position,
                              current_price: float,
                              high_price: float,
                              current_date: str) -> Tuple[bool, ExitReason]:
        """检查出场条件
        
        Args:
            position: 持仓
            current_price: 当前价格
            high_price: 今日最高价
            current_date: 当前日期
        """
        # 更新持仓信息
        position.current_price = current_price
        position.highest_price = max(position.highest_price, high_price)
        position.unrealized_return = (current_price / position.entry_price) - 1
        position.unrealized_pnl = (current_price - position.entry_price) * position.shares
        
        entry_dt = datetime.strptime(position.entry_date, '%Y-%m-%d')
        current_dt = datetime.strptime(current_date, '%Y-%m-%d')
        position.holding_days = (current_dt - entry_dt).days
        
        # 检查目标止盈
        if current_price >= position.target_price:
            return True, ExitReason.TARGET_PROFIT
        
        # 检查固定止损
        if current_price <= position.stop_loss_price:
            return True, ExitReason.STOP_LOSS
        
        # 检查移动止盈
        if position.highest_price > position.entry_price * 1.05:  # 盈利5%后启动移动止盈
            trailing_stop = position.highest_price * (1 - self.config.trailing_stop)
            position.trailing_stop_price = trailing_stop
            if current_price <= trailing_stop:
                return True, ExitReason.TRAILING_STOP
        
        # 检查时间止损
        if position.holding_days >= self.config.max_holding_days:
            return True, ExitReason.TIME_EXIT
        
        return False, None
    
    def execute_entry(self, signal: TradeSignal):
        """执行入场"""
        # 计算可用资金
        available_cash = self.cash * signal.position_size / self.config.position_size
        
        if available_cash < signal.entry_price * 100:
            return None
        
        # 计算买入股数（整百）
        shares = int(available_cash / signal.entry_price / 100) * 100
        if shares < 100:
            return None
        
        cost = shares * signal.entry_price
        
        # 更新资金
        self.cash -= cost
        
        # 创建持仓
        position = Position(
            code=signal.code,
            name=signal.name,
            entry_date=signal.signal_date,
            entry_price=signal.entry_price,
            shares=shares,
            cost=cost,
            current_price=signal.entry_price,
            highest_price=signal.entry_price,
            target_price=signal.target_price,
            stop_loss_price=signal.stop_loss_price,
            industry=signal.factors.get('industry', ''),
        )
        
        self.positions[signal.code] = position
        
        return position
    
    def execute_exit(self, code: str, exit_price: float, exit_date: str, reason: ExitReason) -> Trade:
        """执行出场"""
        if code not in self.positions:
            return None
        
        position = self.positions[code]
        
        # 计算盈亏
        pnl = (exit_price - position.entry_price) * position.shares
        return_pct = (exit_price / position.entry_price) - 1
        
        # 更新资金
        self.cash += position.shares * exit_price
        
        # 创建交易记录
        trade = Trade(
            code=code,
            name=position.name,
            entry_date=position.entry_date,
            entry_price=position.entry_price,
            exit_date=exit_date,
            exit_price=exit_price,
            shares=position.shares,
            pnl=pnl,
            return_pct=return_pct,
            holding_days=position.holding_days,
            exit_reason=reason,
            industry=position.industry,
        )
        
        self.trades.append(trade)
        
        # 更新连续亏损计数
        if pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
        
        # 删除持仓
        del self.positions[code]
        
        return trade
    
    def update_equity(self, date: str, prices: Dict[str, float]):
        """更新权益"""
        # 更新持仓市值
        position_value = sum(
            prices.get(code, pos.current_price) * pos.shares
            for code, pos in self.positions.items()
        )
        
        self.current_capital = self.cash + position_value
        
        # 更新最大回撤
        self.peak_equity = max(self.peak_equity, self.current_capital)
        self.current_drawdown = (self.peak_equity - self.current_capital) / self.peak_equity
        
        self.daily_equity.append({
            'date': date,
            'equity': self.current_capital,
            'cash': self.cash,
            'position_value': position_value,
            'drawdown': self.current_drawdown,
            'positions': len(self.positions),
        })
    
    def get_performance_summary(self) -> Dict:
        """获取绩效摘要"""
        if not self.trades:
            return {}
        
        trades_df = pd.DataFrame([vars(t) for t in self.trades])
        
        total_trades = len(trades_df)
        winning_trades = (trades_df['pnl'] > 0).sum()
        losing_trades = (trades_df['pnl'] < 0).sum()
        
        total_pnl = trades_df['pnl'].sum()
        total_return = (self.current_capital / self.initial_capital) - 1
        
        avg_return = trades_df['return_pct'].mean()
        avg_win = trades_df[trades_df['pnl'] > 0]['return_pct'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['pnl'] < 0]['return_pct'].mean() if losing_trades > 0 else 0
        
        # 按出场原因统计
        exit_stats = trades_df.groupby('exit_reason').agg({
            'pnl': ['count', 'sum', 'mean'],
            'return_pct': 'mean',
        }).round(4)
        
        # 计算夏普比率
        if len(self.daily_equity) > 1:
            equity_df = pd.DataFrame(self.daily_equity)
            daily_returns = equity_df['equity'].pct_change().dropna()
            sharpe = daily_returns.mean() / daily_returns.std() * np.sqrt(252) if daily_returns.std() > 0 else 0
        else:
            sharpe = 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': winning_trades / total_trades if total_trades > 0 else 0,
            'total_pnl': total_pnl,
            'total_return': total_return,
            'avg_return': avg_return,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': abs(avg_win / avg_loss) if avg_loss != 0 else 0,
            'max_drawdown': max(e['drawdown'] for e in self.daily_equity) if self.daily_equity else 0,
            'sharpe_ratio': sharpe,
            'exit_stats': exit_stats.to_dict() if not exit_stats.empty else {},
            'hit_10pct': (trades_df['return_pct'] >= 0.10).mean(),
            'hit_5pct': (trades_df['return_pct'] >= 0.05).mean(),
        }


def main():
    """测试交易策略"""
    # 创建策略
    config = TradingConfig(
        target_return=0.10,
        stop_loss=-0.05,
        max_holding_days=5,
    )
    strategy = TradingStrategy(config, initial_capital=1000000)
    
    # 模拟候选股票
    candidates = pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE', '600000.XSHG'],
        'name': ['平安银行', '万科A', '浦发银行'],
        'probability': [0.75, 0.60, 0.55],
        'total_score': [72, 65, 58],
        'current_price': [10.5, 8.2, 7.8],
        'avg_money': [5000, 3000, 2000],
        'momentum_20d': [5, 3, -2],
        'rel_strength': [60, 45, 30],
        'roe': [12, 8, 6],
        'industry': ['银行', '地产', '银行'],
    })
    
    # 生成信号
    signals = strategy.generate_entry_signals(candidates, '2025-12-20')
    print(f"生成 {len(signals)} 个入场信号:")
    for sig in signals:
        print(f"  {sig.name}: 概率={sig.probability:.0%}, 得分={sig.score:.1f}, 仓位={sig.position_size:.1%}")
    
    # 执行入场
    for sig in signals:
        pos = strategy.execute_entry(sig)
        if pos:
            print(f"  买入 {pos.name}: {pos.shares}股 @ {pos.entry_price}")


if __name__ == '__main__':
    main()
