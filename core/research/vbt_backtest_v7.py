# -*- coding: utf-8 -*-
"""
VBT回测引擎 V7.0 - 专业级回测
=============================

对标BulletTrade专业标准:
1. 完整交易成本模型（佣金+印花税+滑点+最低佣金+过户费）
2. 多种订单执行模式（开盘/收盘/VWAP）
3. 完整止损止盈逻辑（固定/移动/时间/部分止盈）
4. 持仓状态跟踪（成本价/最高价/入场日/持有天数）
5. 标准化结果输出（13+指标）

作者: TRQuant Team
版本: V7.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import time

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# ============== 数据结构 ==============

class ExecutionMode(Enum):
    """订单执行模式"""
    OPEN = "open"      # 开盘价成交
    CLOSE = "close"    # 收盘价成交
    VWAP = "vwap"      # 成交量加权均价


@dataclass
class TradeCostModel:
    """交易成本模型（对标BulletTrade）"""
    commission_rate: float = 0.0003     # 佣金率 (万分之三)
    stamp_tax_rate: float = 0.001       # 印花税率 (千分之一，仅卖出)
    slippage: float = 0.001             # 滑点 (千分之一)
    min_commission: float = 5.0         # 最低佣金 (元)
    transfer_fee_rate: float = 0.00001  # 过户费率 (沪市)
    
    def calculate_buy_cost(self, amount: float) -> float:
        """计算买入成本"""
        commission = max(amount * self.commission_rate, self.min_commission)
        slippage_cost = amount * self.slippage
        transfer_fee = amount * self.transfer_fee_rate
        return commission + slippage_cost + transfer_fee
    
    def calculate_sell_cost(self, amount: float) -> float:
        """计算卖出成本"""
        commission = max(amount * self.commission_rate, self.min_commission)
        stamp_tax = amount * self.stamp_tax_rate  # 仅卖出
        slippage_cost = amount * self.slippage
        transfer_fee = amount * self.transfer_fee_rate
        return commission + stamp_tax + slippage_cost + transfer_fee


@dataclass
class PositionState:
    """持仓状态"""
    stock: str
    shares: float = 0.0
    cost_price: float = 0.0           # 成本价
    current_price: float = 0.0        # 当前价
    highest_price: float = 0.0        # 持有期最高价
    lowest_price: float = float('inf') # 持有期最低价
    entry_date: Optional[datetime] = None
    holding_days: int = 0
    partial_profit_done: bool = False  # 是否已部分止盈
    unrealized_pnl: float = 0.0       # 未实现盈亏
    unrealized_pnl_pct: float = 0.0   # 未实现盈亏率
    
    def update(self, current_price: float, current_date: datetime):
        """更新持仓状态"""
        self.current_price = current_price
        self.highest_price = max(self.highest_price, current_price)
        self.lowest_price = min(self.lowest_price, current_price)
        
        if self.entry_date:
            self.holding_days = (current_date - self.entry_date).days
        
        if self.cost_price > 0:
            self.unrealized_pnl = (current_price - self.cost_price) * self.shares
            self.unrealized_pnl_pct = (current_price / self.cost_price - 1) * 100


@dataclass
class TradeRecord:
    """交易记录"""
    date: datetime
    stock: str
    action: str  # BUY / SELL
    shares: float
    price: float
    amount: float
    cost: float
    reason: str = ""
    
    @property
    def net_amount(self) -> float:
        """净金额（买入为负，卖出为正）"""
        if self.action == "BUY":
            return -(self.amount + self.cost)
        else:
            return self.amount - self.cost


@dataclass
class StopLossConfig:
    """止损止盈配置"""
    # 固定止损止盈
    stop_loss_pct: float = -0.10           # 固定止损 (-10%)
    take_profit_pct: float = 0.30          # 固定止盈 (+30%)
    
    # 移动止损
    trailing_stop_pct: float = -0.09       # 移动止损回撤 (-9%)
    trailing_stop_trigger: float = 0.15    # 移动止损触发（盈利+15%后启用）
    
    # 时间止损
    time_stop_days: int = 20               # 时间止损（20个交易日）
    
    # 部分止盈
    partial_profit_1_pct: float = 0.20     # 第一批止盈 (+20%)
    partial_profit_1_ratio: float = 0.50   # 第一批止盈比例（减仓50%）
    
    # 软止损（根据市场状态调整）
    soft_stop_enabled: bool = True
    soft_stop_bull_adjust: float = 1.2     # 牛市放宽20%
    soft_stop_bear_adjust: float = 0.8     # 熊市收紧20%


@dataclass
class BacktestResultV7:
    """回测结果V7（对标BulletTrade 13+指标）"""
    # 基本信息
    start_date: str = ""
    end_date: str = ""
    initial_capital: float = 1000000.0
    final_capital: float = 0.0
    
    # 核心收益指标
    total_return: float = 0.0          # 总收益率 (%)
    annual_return: float = 0.0         # 年化收益率 (%)
    monthly_return: float = 0.0        # 月收益率 (%)
    weekly_return: float = 0.0         # 周收益率 (%)
    
    # 风险指标
    max_drawdown: float = 0.0          # 最大回撤 (%)
    max_drawdown_duration: int = 0     # 最大回撤持续天数
    volatility: float = 0.0            # 年化波动率 (%)
    downside_volatility: float = 0.0   # 下行波动率 (%)
    
    # 风险调整收益
    sharpe_ratio: float = 0.0          # 夏普比率
    sortino_ratio: float = 0.0         # 索提诺比率
    calmar_ratio: float = 0.0          # 卡玛比率
    
    # 交易统计
    total_trades: int = 0              # 总交易次数
    win_trades: int = 0                # 盈利交易次数
    loss_trades: int = 0               # 亏损交易次数
    trade_win_rate: float = 0.0        # 交易胜率 (%)
    daily_win_rate: float = 0.0        # 日胜率 (%)
    avg_win: float = 0.0               # 平均盈利 (%)
    avg_loss: float = 0.0              # 平均亏损 (%)
    profit_loss_ratio: float = 0.0     # 盈亏比
    avg_holding_period: float = 0.0    # 平均持仓周期 (天)
    
    # 其他统计
    trading_days: int = 0              # 交易天数
    total_commission: float = 0.0      # 总手续费
    total_slippage: float = 0.0        # 总滑点成本
    
    # 时间序列数据
    equity_curve: Optional[pd.Series] = None
    daily_returns: Optional[pd.Series] = None
    drawdown_curve: Optional[pd.Series] = None
    positions_history: Optional[pd.DataFrame] = None
    trades: List[TradeRecord] = field(default_factory=list)
    
    # 元信息
    runtime_seconds: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'initial_capital': self.initial_capital,
            'final_capital': self.final_capital,
            'total_return': self.total_return,
            'annual_return': self.annual_return,
            'monthly_return': self.monthly_return,
            'weekly_return': self.weekly_return,
            'max_drawdown': self.max_drawdown,
            'max_drawdown_duration': self.max_drawdown_duration,
            'volatility': self.volatility,
            'sharpe_ratio': self.sharpe_ratio,
            'sortino_ratio': self.sortino_ratio,
            'calmar_ratio': self.calmar_ratio,
            'total_trades': self.total_trades,
            'trade_win_rate': self.trade_win_rate,
            'daily_win_rate': self.daily_win_rate,
            'profit_loss_ratio': self.profit_loss_ratio,
            'avg_holding_period': self.avg_holding_period,
            'trading_days': self.trading_days,
        }


# ============== 专业回测引擎 ==============

class VBTBacktestV7:
    """
    专业回测引擎V7 - 对标BulletTrade标准
    
    特性:
    1. 完整交易成本模型
    2. 多种订单执行模式
    3. 完整止损止盈逻辑
    4. 持仓状态跟踪
    5. 标准化结果输出
    """
    
    def __init__(
        self,
        initial_capital: float = 1000000.0,
        cost_model: Optional[TradeCostModel] = None,
        stop_loss_config: Optional[StopLossConfig] = None,
        execution_mode: ExecutionMode = ExecutionMode.CLOSE,
        risk_free_rate: float = 0.03,
    ):
        self.initial_capital = initial_capital
        self.cost_model = cost_model or TradeCostModel()
        self.stop_loss_config = stop_loss_config or StopLossConfig()
        self.execution_mode = execution_mode
        self.risk_free_rate = risk_free_rate
        
        # 状态变量
        self.cash = initial_capital
        self.positions: Dict[str, PositionState] = {}
        self.trades: List[TradeRecord] = []
        self.daily_records: List[Dict] = []
        
        logger.info(f"VBTBacktestV7初始化: 资金={initial_capital:,.0f}, "
                   f"佣金={self.cost_model.commission_rate:.4%}, "
                   f"滑点={self.cost_model.slippage:.4%}")
    
    def run(
        self,
        close: pd.DataFrame,
        open_: Optional[pd.DataFrame] = None,
        high: Optional[pd.DataFrame] = None,
        low: Optional[pd.DataFrame] = None,
        volume: Optional[pd.DataFrame] = None,
        target_weights: pd.DataFrame = None,
        signals: Optional[pd.DataFrame] = None,
        market_state: Optional[pd.Series] = None,
    ) -> BacktestResultV7:
        """
        运行回测
        
        Args:
            close: 收盘价矩阵 (T x N)
            open_: 开盘价矩阵 (T x N)
            high: 最高价矩阵 (T x N)
            low: 最低价矩阵 (T x N)
            volume: 成交量矩阵 (T x N)
            target_weights: 目标权重矩阵 (T x N)
            signals: 买卖信号矩阵 (T x N), 1=买入, -1=卖出, 0=持有
            market_state: 市场状态 (T), 用于软止损调整
        
        Returns:
            BacktestResultV7: 回测结果
        """
        start_time = time.time()
        
        # 初始化
        self._reset()
        dates = close.index
        stocks = close.columns.tolist()
        
        # 确定执行价格
        exec_price = self._get_execution_price(close, open_, high, low, volume)
        
        # 如果没有提供target_weights，使用signals生成
        if target_weights is None and signals is not None:
            target_weights = self._signals_to_weights(signals)
        
        if target_weights is None:
            raise ValueError("必须提供 target_weights 或 signals")
        
        # 逐日回测
        for i, date in enumerate(dates):
            current_prices = close.loc[date]
            exec_prices = exec_price.loc[date]
            target = target_weights.loc[date]
            
            # 1. 更新持仓状态
            self._update_positions(date, current_prices)
            
            # 2. 检查止损止盈
            market_adjust = 1.0
            if market_state is not None and date in market_state.index:
                market_adjust = self._get_market_adjust(market_state.loc[date])
            
            sell_stocks = self._check_stop_loss_take_profit(date, current_prices, market_adjust)
            
            # 3. 执行卖出
            for stock, reason in sell_stocks:
                if stock in self.positions:
                    self._execute_sell(date, stock, exec_prices.get(stock, current_prices.get(stock)), reason)
            
            # 4. 计算目标持仓
            total_value = self._calculate_total_value(current_prices)
            
            # 5. 执行调仓
            self._rebalance(date, target, exec_prices, total_value)
            
            # 6. 记录每日状态
            self._record_daily(date, current_prices)
        
        # 计算结果
        result = self._calculate_result(dates)
        result.runtime_seconds = time.time() - start_time
        
        logger.info(f"VBTBacktestV7完成: 总收益={result.total_return:.2f}%, "
                   f"夏普={result.sharpe_ratio:.2f}, "
                   f"最大回撤={result.max_drawdown:.2f}%, "
                   f"交易次数={result.total_trades}, "
                   f"耗时={result.runtime_seconds:.2f}s")
        
        return result
    
    def _reset(self):
        """重置状态"""
        self.cash = self.initial_capital
        self.positions = {}
        self.trades = []
        self.daily_records = []
    
    def _get_execution_price(
        self,
        close: pd.DataFrame,
        open_: Optional[pd.DataFrame],
        high: Optional[pd.DataFrame],
        low: Optional[pd.DataFrame],
        volume: Optional[pd.DataFrame],
    ) -> pd.DataFrame:
        """获取执行价格"""
        if self.execution_mode == ExecutionMode.OPEN and open_ is not None:
            return open_
        elif self.execution_mode == ExecutionMode.VWAP and all(x is not None for x in [high, low, close, volume]):
            # 简化VWAP: (H + L + C) / 3
            return (high + low + close) / 3
        else:
            return close
    
    def _signals_to_weights(self, signals: pd.DataFrame) -> pd.DataFrame:
        """将信号转换为权重"""
        weights = pd.DataFrame(0.0, index=signals.index, columns=signals.columns)
        
        for date in signals.index:
            buy_stocks = signals.loc[date][signals.loc[date] > 0].index.tolist()
            if buy_stocks:
                weight = 1.0 / len(buy_stocks)
                weights.loc[date, buy_stocks] = weight
        
        return weights
    
    def _update_positions(self, date: datetime, prices: pd.Series):
        """更新持仓状态"""
        for stock, pos in self.positions.items():
            if stock in prices.index and not pd.isna(prices[stock]):
                pos.update(prices[stock], date)
    
    def _get_market_adjust(self, market_state: Any) -> float:
        """获取市场状态调整系数"""
        if not self.stop_loss_config.soft_stop_enabled:
            return 1.0
        
        # 根据市场状态调整止损
        if isinstance(market_state, str):
            if market_state in ['bull', 'strong_bull', '牛市', '强牛']:
                return self.stop_loss_config.soft_stop_bull_adjust
            elif market_state in ['bear', 'strong_bear', '熊市', '强熊']:
                return self.stop_loss_config.soft_stop_bear_adjust
        
        return 1.0
    
    def _check_stop_loss_take_profit(
        self, 
        date: datetime, 
        prices: pd.Series,
        market_adjust: float = 1.0
    ) -> List[Tuple[str, str]]:
        """检查止损止盈"""
        sell_list = []
        cfg = self.stop_loss_config
        
        for stock, pos in self.positions.items():
            if pos.shares <= 0:
                continue
            
            price = prices.get(stock)
            if price is None or pd.isna(price):
                continue
            
            pnl_pct = (price / pos.cost_price - 1) if pos.cost_price > 0 else 0
            
            # 调整后的止损阈值
            adjusted_stop_loss = cfg.stop_loss_pct * market_adjust
            
            # 1. 固定止损
            if pnl_pct <= adjusted_stop_loss:
                sell_list.append((stock, f"固定止损({pnl_pct:.1%})"))
                continue
            
            # 2. 固定止盈
            if pnl_pct >= cfg.take_profit_pct:
                sell_list.append((stock, f"固定止盈({pnl_pct:.1%})"))
                continue
            
            # 3. 部分止盈
            if not pos.partial_profit_done and pnl_pct >= cfg.partial_profit_1_pct:
                # 标记已部分止盈，减仓在_execute_sell中处理
                pos.partial_profit_done = True
                sell_list.append((stock, f"部分止盈({pnl_pct:.1%})"))
                continue
            
            # 4. 移动止损（盈利触发后启用）
            if pnl_pct >= cfg.trailing_stop_trigger:
                highest_pnl = (pos.highest_price / pos.cost_price - 1) if pos.cost_price > 0 else 0
                drawdown_from_high = pnl_pct - highest_pnl
                
                if drawdown_from_high <= cfg.trailing_stop_pct:
                    sell_list.append((stock, f"移动止损({drawdown_from_high:.1%})"))
                    continue
            
            # 5. 时间止损
            if pos.holding_days >= cfg.time_stop_days and pnl_pct < 0.05:
                sell_list.append((stock, f"时间止损({pos.holding_days}天)"))
                continue
        
        return sell_list
    
    def _calculate_total_value(self, prices: pd.Series) -> float:
        """计算总资产"""
        position_value = 0.0
        for stock, pos in self.positions.items():
            price = prices.get(stock, pos.current_price)
            if not pd.isna(price):
                position_value += pos.shares * price
        
        return self.cash + position_value
    
    def _execute_sell(self, date: datetime, stock: str, price: float, reason: str):
        """执行卖出"""
        if stock not in self.positions:
            return
        
        pos = self.positions[stock]
        
        # 判断是否部分卖出
        if "部分止盈" in reason:
            sell_shares = pos.shares * self.stop_loss_config.partial_profit_1_ratio
        else:
            sell_shares = pos.shares
        
        if sell_shares <= 0:
            return
        
        amount = sell_shares * price
        cost = self.cost_model.calculate_sell_cost(amount)
        
        # 更新现金
        self.cash += amount - cost
        
        # 记录交易
        trade = TradeRecord(
            date=date,
            stock=stock,
            action="SELL",
            shares=sell_shares,
            price=price,
            amount=amount,
            cost=cost,
            reason=reason
        )
        self.trades.append(trade)
        
        # 更新持仓
        pos.shares -= sell_shares
        if pos.shares <= 0.01:  # 清仓
            del self.positions[stock]
        
        logger.debug(f"卖出 {stock}: {sell_shares:.0f}股 @ {price:.2f}, 原因: {reason}")
    
    def _execute_buy(self, date: datetime, stock: str, price: float, amount: float):
        """执行买入"""
        if amount <= 0 or pd.isna(price) or price <= 0:
            return
        
        cost = self.cost_model.calculate_buy_cost(amount)
        
        if self.cash < amount + cost:
            # 资金不足，调整买入金额
            amount = self.cash - cost
            if amount <= 0:
                return
        
        shares = amount / price
        
        # 更新现金
        self.cash -= (amount + cost)
        
        # 记录交易
        trade = TradeRecord(
            date=date,
            stock=stock,
            action="BUY",
            shares=shares,
            price=price,
            amount=amount,
            cost=cost,
            reason="调仓买入"
        )
        self.trades.append(trade)
        
        # 更新持仓
        if stock in self.positions:
            pos = self.positions[stock]
            total_shares = pos.shares + shares
            pos.cost_price = (pos.cost_price * pos.shares + price * shares) / total_shares
            pos.shares = total_shares
        else:
            self.positions[stock] = PositionState(
                stock=stock,
                shares=shares,
                cost_price=price,
                current_price=price,
                highest_price=price,
                lowest_price=price,
                entry_date=date,
                holding_days=0
            )
        
        logger.debug(f"买入 {stock}: {shares:.0f}股 @ {price:.2f}")
    
    def _rebalance(
        self, 
        date: datetime, 
        target_weights: pd.Series, 
        prices: pd.Series,
        total_value: float
    ):
        """调仓"""
        # 计算目标持仓金额
        target_amounts = target_weights * total_value
        
        # 计算当前持仓金额
        current_amounts = pd.Series(0.0, index=target_weights.index)
        for stock in target_weights.index:
            if stock in self.positions:
                pos = self.positions[stock]
                price = prices.get(stock, pos.current_price)
                if not pd.isna(price):
                    current_amounts[stock] = pos.shares * price
        
        # 计算差额
        diff = target_amounts - current_amounts
        
        # 先卖后买
        # 卖出
        for stock in diff[diff < -100].index:  # 差额超过100元才调仓
            sell_amount = -diff[stock]
            price = prices.get(stock)
            if price and not pd.isna(price) and stock in self.positions:
                pos = self.positions[stock]
                sell_shares = min(sell_amount / price, pos.shares)
                if sell_shares > 0:
                    self._execute_sell(date, stock, price, "调仓卖出")
        
        # 买入
        for stock in diff[diff > 100].index:  # 差额超过100元才调仓
            buy_amount = diff[stock]
            price = prices.get(stock)
            if price and not pd.isna(price):
                self._execute_buy(date, stock, price, buy_amount)
    
    def _record_daily(self, date: datetime, prices: pd.Series):
        """记录每日状态"""
        total_value = self._calculate_total_value(prices)
        
        position_value = total_value - self.cash
        
        record = {
            'date': date,
            'total_value': total_value,
            'cash': self.cash,
            'position_value': position_value,
            'num_positions': len(self.positions),
        }
        
        self.daily_records.append(record)
    
    def _calculate_result(self, dates: pd.DatetimeIndex) -> BacktestResultV7:
        """计算回测结果"""
        result = BacktestResultV7()
        
        if not self.daily_records:
            return result
        
        # 转换为DataFrame
        df = pd.DataFrame(self.daily_records)
        df.set_index('date', inplace=True)
        
        # 基本信息
        result.start_date = str(dates[0].date())
        result.end_date = str(dates[-1].date())
        result.initial_capital = self.initial_capital
        result.final_capital = df['total_value'].iloc[-1]
        result.trading_days = len(df)
        
        # 收益曲线
        result.equity_curve = df['total_value']
        
        # 日收益率
        result.daily_returns = df['total_value'].pct_change().fillna(0)
        
        # 收益指标
        result.total_return = (result.final_capital / self.initial_capital - 1) * 100
        
        years = result.trading_days / 252
        if years > 0:
            result.annual_return = ((1 + result.total_return / 100) ** (1 / years) - 1) * 100
        
        months = result.trading_days / 21
        if months > 0:
            result.monthly_return = ((1 + result.total_return / 100) ** (1 / months) - 1) * 100
        
        weeks = result.trading_days / 5
        if weeks > 0:
            result.weekly_return = ((1 + result.total_return / 100) ** (1 / weeks) - 1) * 100
        
        # 风险指标
        daily_returns = result.daily_returns.dropna()
        
        if len(daily_returns) > 0:
            result.volatility = daily_returns.std() * np.sqrt(252) * 100
            
            # 下行波动率
            negative_returns = daily_returns[daily_returns < 0]
            if len(negative_returns) > 0:
                result.downside_volatility = negative_returns.std() * np.sqrt(252) * 100
            
            # 最大回撤
            cumulative = (1 + daily_returns).cumprod()
            peak = cumulative.expanding().max()
            drawdown = (cumulative - peak) / peak
            result.max_drawdown = drawdown.min() * 100
            result.drawdown_curve = drawdown * 100
            
            # 最大回撤持续天数
            is_dd = drawdown < 0
            dd_groups = (is_dd != is_dd.shift()).cumsum()
            dd_durations = is_dd.groupby(dd_groups).sum()
            result.max_drawdown_duration = int(dd_durations.max()) if len(dd_durations) > 0 else 0
            
            # 夏普比率
            excess_return = daily_returns.mean() * 252 - self.risk_free_rate
            if result.volatility > 0:
                result.sharpe_ratio = excess_return / (result.volatility / 100)
            
            # 索提诺比率
            if result.downside_volatility > 0:
                result.sortino_ratio = excess_return / (result.downside_volatility / 100)
            
            # 卡玛比率
            if result.max_drawdown < 0:
                result.calmar_ratio = result.annual_return / abs(result.max_drawdown)
            
            # 日胜率
            result.daily_win_rate = (daily_returns > 0).mean() * 100
        
        # 交易统计
        result.trades = self.trades
        result.total_trades = len(self.trades)
        
        # 按股票聚合交易
        trade_pnls = []
        stock_trades: Dict[str, List[TradeRecord]] = {}
        
        for trade in self.trades:
            if trade.stock not in stock_trades:
                stock_trades[trade.stock] = []
            stock_trades[trade.stock].append(trade)
        
        for stock, trades in stock_trades.items():
            buy_amount = sum(t.amount for t in trades if t.action == "BUY")
            sell_amount = sum(t.amount for t in trades if t.action == "SELL")
            total_cost = sum(t.cost for t in trades)
            
            if buy_amount > 0:
                pnl_pct = (sell_amount - buy_amount - total_cost) / buy_amount * 100
                trade_pnls.append(pnl_pct)
        
        if trade_pnls:
            wins = [p for p in trade_pnls if p > 0]
            losses = [p for p in trade_pnls if p <= 0]
            
            result.win_trades = len(wins)
            result.loss_trades = len(losses)
            result.trade_win_rate = len(wins) / len(trade_pnls) * 100 if trade_pnls else 0
            result.avg_win = np.mean(wins) if wins else 0
            result.avg_loss = np.mean(losses) if losses else 0
            
            if result.avg_loss != 0:
                result.profit_loss_ratio = abs(result.avg_win / result.avg_loss)
        
        # 平均持仓周期
        holding_periods = []
        for stock, pos in self.positions.items():
            if pos.holding_days > 0:
                holding_periods.append(pos.holding_days)
        
        if holding_periods:
            result.avg_holding_period = np.mean(holding_periods)
        
        # 总手续费
        result.total_commission = sum(t.cost for t in self.trades)
        
        return result


# ============== 测试函数 ==============

def test_vbt_backtest_v7():
    """测试VBTBacktestV7"""
    import jqdatasdk as jq
    import json
    
    # 认证JQData
    with open("/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    
    # 获取测试数据
    stocks = ['000001.XSHE', '600519.XSHG', '000858.XSHE', '002415.XSHE', '300750.XSHE']
    
    price_data = jq.get_price(
        stocks,
        start_date='2024-09-20',
        end_date='2024-10-15',
        frequency='daily',
        fields=['open', 'close', 'high', 'low', 'volume'],
        panel=False
    )
    
    # 转换为矩阵格式
    close = price_data.pivot(index='time', columns='code', values='close')
    open_ = price_data.pivot(index='time', columns='code', values='open')
    high = price_data.pivot(index='time', columns='code', values='high')
    low = price_data.pivot(index='time', columns='code', values='low')
    volume = price_data.pivot(index='time', columns='code', values='volume')
    
    # 创建等权重目标
    weights = pd.DataFrame(0.2, index=close.index, columns=close.columns)
    
    # 运行回测
    engine = VBTBacktestV7(initial_capital=1000000)
    result = engine.run(
        close=close,
        open_=open_,
        high=high,
        low=low,
        volume=volume,
        target_weights=weights
    )
    
    print("\n" + "="*60)
    print("VBTBacktestV7 测试结果")
    print("="*60)
    print(f"回测区间: {result.start_date} ~ {result.end_date}")
    print(f"初始资金: {result.initial_capital:,.0f}")
    print(f"最终资金: {result.final_capital:,.0f}")
    print(f"总收益率: {result.total_return:.2f}%")
    print(f"年化收益: {result.annual_return:.2f}%")
    print(f"周收益率: {result.weekly_return:.2f}%")
    print(f"夏普比率: {result.sharpe_ratio:.2f}")
    print(f"最大回撤: {result.max_drawdown:.2f}%")
    print(f"交易次数: {result.total_trades}")
    print(f"交易胜率: {result.trade_win_rate:.1f}%")
    print(f"日胜率: {result.daily_win_rate:.1f}%")
    print(f"耗时: {result.runtime_seconds:.2f}s")
    
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_vbt_backtest_v7()
