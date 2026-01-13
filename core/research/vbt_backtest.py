# -*- coding: utf-8 -*-
"""
vectorbt回测封装 - 向量化组合回测
=================================

功能：
1. 基于target_weights的组合回测
2. 支持周调仓逻辑
3. 输出标准化BacktestResult
4. 支持止损止盈（账户级）
5. 性能统计

与现有系统集成：
- 输入：DataMatrices + FactorMatrices + SignalParams
- 输出：BacktestResult（兼容现有评分函数）
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import time

import pandas as pd
import numpy as np

try:
    import vectorbt as vbt
    VBT_AVAILABLE = True
except ImportError:
    VBT_AVAILABLE = False

from .data_provider import DataMatrices
from .factors import FactorMatrices, FactorCalculator
from .signals import SignalMatrices, SignalEngine, SignalParams

logger = logging.getLogger(__name__)


@dataclass
class PositionTracker:
    """持仓跟踪器
    
    跟踪每个股票的持仓状态
    """
    cost_prices: Dict[str, float] = field(default_factory=dict)  # 成本价
    highest_prices: Dict[str, float] = field(default_factory=dict)  # 最高价
    entry_dates: Dict[str, datetime] = field(default_factory=dict)  # 入场日期
    partial_profit_done: Dict[str, bool] = field(default_factory=dict)  # 分批止盈标记
    
    def update_cost_price(self, stock: str, price: float, date: datetime):
        """更新成本价（仅在买入时调用）"""
        self.cost_prices[stock] = price
        self.highest_prices[stock] = price
        self.entry_dates[stock] = date
        self.partial_profit_done[stock] = False
    
    def update_highest_price(self, stock: str, price: float):
        """更新最高价"""
        if stock not in self.highest_prices:
            self.highest_prices[stock] = price
        else:
            self.highest_prices[stock] = max(self.highest_prices[stock], price)
    
    def remove_position(self, stock: str):
        """移除持仓（平仓时调用）"""
        self.cost_prices.pop(stock, None)
        self.highest_prices.pop(stock, None)
        self.entry_dates.pop(stock, None)
        self.partial_profit_done.pop(stock, None)
    
    def get_cost_price(self, stock: str) -> Optional[float]:
        """获取成本价"""
        return self.cost_prices.get(stock)
    
    def get_highest_price(self, stock: str) -> Optional[float]:
        """获取最高价"""
        return self.highest_prices.get(stock)
    
    def get_entry_date(self, stock: str) -> Optional[datetime]:
        """获取入场日期"""
        return self.entry_dates.get(stock)
    
    def is_partial_profit_done(self, stock: str) -> bool:
        """是否已完成分批止盈"""
        return self.partial_profit_done.get(stock, False)
    
    def mark_partial_profit_done(self, stock: str):
        """标记已完成分批止盈"""
        self.partial_profit_done[stock] = True


@dataclass
class BacktestResult:
    """回测结果
    
    兼容现有评分函数的结构
    """
    # 核心指标
    total_return: float = 0.0       # 总收益率 (%)
    annual_return: float = 0.0      # 年化收益率 (%)
    sharpe_ratio: float = 0.0       # 夏普比率
    max_drawdown: float = 0.0       # 最大回撤 (%)
    win_rate: float = 0.0           # 胜率 (%)
    total_trades: int = 0           # 总交易次数
    
    # 扩展指标（周收益10%+策略关注）
    weekly_return_mean: float = 0.0      # 周均收益率 (%)
    weekly_return_std: float = 0.0       # 周收益波动
    max_consecutive_losses: int = 0      # 最大连续亏损次数
    turnover: float = 0.0                # 平均换手率
    avg_exposure: float = 0.0            # 平均仓位暴露
    
    # 元数据
    start_date: str = ""
    end_date: str = ""
    trading_days: int = 0
    benchmark_return: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "total_return": self.total_return,
            "annual_return": self.annual_return,
            "sharpe_ratio": self.sharpe_ratio,
            "max_drawdown": self.max_drawdown,
            "win_rate": self.win_rate,
            "total_trades": self.total_trades,
            "weekly_return_mean": self.weekly_return_mean,
            "weekly_return_std": self.weekly_return_std,
            "max_consecutive_losses": self.max_consecutive_losses,
            "turnover": self.turnover,
            "avg_exposure": self.avg_exposure,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "trading_days": self.trading_days,
            "benchmark_return": self.benchmark_return,
        }


class VBTBacktest:
    """vectorbt回测引擎
    
    核心功能：
    1. 基于target_weights进行组合回测
    2. 支持交易成本（佣金+印花税+滑点）
    3. 支持止损止盈
    4. 输出标准化结果
    
    使用示例：
    ```python
    backtest = VBTBacktest(initial_capital=1000000)
    result = backtest.run(data_matrices, factor_matrices, signal_params)
    print(f"年化收益: {result.annual_return:.2%}")
    ```
    """
    
    def __init__(
        self,
        initial_capital: float = 1000000.0,
        commission_rate: float = 0.0003,      # 佣金率
        stamp_tax: float = 0.001,             # 印花税（卖出）
        slippage: float = 0.001,              # 滑点
        risk_free_rate: float = 0.03,         # 无风险利率
    ):
        """
        初始化回测引擎
        
        Args:
            initial_capital: 初始资金
            commission_rate: 佣金率
            stamp_tax: 印花税
            slippage: 滑点
            risk_free_rate: 无风险利率（计算夏普比率）
        """
        if not VBT_AVAILABLE:
            raise ImportError("vectorbt未安装，请运行: pip install vectorbt")
        
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.stamp_tax = stamp_tax
        self.slippage = slippage
        self.risk_free_rate = risk_free_rate
    
    def run(
        self,
        data: DataMatrices,
        factors: FactorMatrices,
        params: SignalParams,
    ) -> BacktestResult:
        """
        运行回测
        
        Args:
            data: 数据矩阵
            factors: 因子矩阵
            params: 信号参数
        
        Returns:
            BacktestResult
        """
        start_time = time.time()
        
        # 1. 生成信号
        engine = SignalEngine(params=params)
        signals = engine.generate_signals(data, factors, params)
        
        # 2. 运行vectorbt回测
        result = self._run_vbt_backtest(data, signals, params)
        
        elapsed = time.time() - start_time
        logger.info(f"回测完成，耗时: {elapsed:.2f}秒")
        
        return result
    
    def run_with_signals(
        self,
        data: DataMatrices,
        signals: SignalMatrices,
    ) -> BacktestResult:
        """
        使用预先生成的信号运行回测
        
        Args:
            data: 数据矩阵
            signals: 信号矩阵
        
        Returns:
            BacktestResult
        """
        return self._run_vbt_backtest(data, signals, SignalParams())
    
    def _run_vbt_backtest(
        self,
        data: DataMatrices,
        signals: SignalMatrices,
        params: SignalParams,
    ) -> BacktestResult:
        """
        执行vectorbt回测
        
        使用持仓跟踪和止损止盈逻辑实现基于target_weights的回测
        """
        close = data.close
        target_weights = signals.target_weights
        
        # 确保索引对齐
        close = close.reindex(target_weights.index)
        
        # 初始化持仓跟踪器
        tracker = PositionTracker()
        
        # 应用止损止盈，调整target_weights
        adjusted_weights = self._apply_stop_loss_take_profit(
            target_weights, close, tracker, params
        )
        
        # 计算每日收益率
        returns = close.pct_change(fill_method=None).fillna(0)
        
        # 计算组合收益率（基于调整后的weights）
        portfolio_returns = (returns * adjusted_weights.shift(1)).sum(axis=1)
        
        # 精确计算交易成本
        trade_costs = self._calculate_trade_costs(
            adjusted_weights, portfolio_returns, close
        )
        
        # 净收益率
        net_returns = portfolio_returns - trade_costs
        
        # 计算累计收益
        cumulative_returns = (1 + net_returns).cumprod()
        
        # 计算指标
        result = self._calculate_metrics(
            net_returns, 
            cumulative_returns, 
            adjusted_weights,
            close,
        )
        
        return result
    
    def _apply_stop_loss_take_profit(
        self,
        target_weights: pd.DataFrame,
        close: pd.DataFrame,
        tracker: PositionTracker,
        params: SignalParams,
    ) -> pd.DataFrame:
        """
        应用止损止盈规则，调整target_weights
        
        Args:
            target_weights: 原始目标权重矩阵 (T x N)
            close: 收盘价矩阵 (T x N)
            tracker: 持仓跟踪器
            params: 信号参数
        
        Returns:
            调整后的权重矩阵 (T x N)
        """
        adjusted_weights = target_weights.copy()
        symbols = list(target_weights.columns)
        
        # 逐日处理
        for i, date in enumerate(target_weights.index):
            # 使用调整后的权重作为前一日权重（第一次迭代使用target_weights）
            if i > 0:
                prev_weights = adjusted_weights.iloc[i-1]
            else:
                prev_weights = pd.Series(0.0, index=symbols)
            curr_weights = target_weights.iloc[i].copy()
            
            # 获取当前价格
            current_prices = close.loc[date]
            
            # 检查每个持仓
            for stock in symbols:
                prev_weight = prev_weights.get(stock, 0.0)
                curr_weight = curr_weights.get(stock, 0.0)
                
                # 如果有持仓
                if prev_weight > 1e-6:
                    cost_price = tracker.get_cost_price(stock)
                    if cost_price is None:
                        # 如果没有成本价记录，使用上一个交易日的价格作为成本价
                        if i > 0:
                            cost_price = close.iloc[i-1].get(stock)
                            if cost_price is not None and not np.isnan(cost_price):
                                tracker.update_cost_price(stock, cost_price, date)
                                cost_price = tracker.get_cost_price(stock)
                    
                    if cost_price is not None and cost_price > 0:
                        current_price = current_prices.get(stock)
                        if current_price is not None and not np.isnan(current_price):
                            # 更新最高价
                            tracker.update_highest_price(stock, current_price)
                            
                            # 计算盈亏率
                            pnl_rate = (current_price / cost_price - 1.0)
                            highest_price = tracker.get_highest_price(stock) or current_price
                            
                            # 1. 硬止损（立即全仓止损）
                            if pnl_rate <= params.stop_loss_pct:
                                adjusted_weights.loc[date, stock] = 0.0
                                tracker.remove_position(stock)
                                continue
                            
                            # 1.5. 软止损（亏损-8%且持仓>=3天，减仓50%）
                            # 新增：V4参数支持
                            soft_stop_pct = getattr(params, 'soft_stop_loss_pct', -0.08)
                            soft_stop_days = getattr(params, 'soft_stop_days', 3)
                            soft_stop_ratio = getattr(params, 'soft_stop_ratio', 0.5)
                            entry_date = tracker.get_entry_date(stock)
                            if entry_date is not None and pnl_rate <= soft_stop_pct:
                                # 计算持仓天数
                                holding_days = i - list(target_weights.index).index(entry_date) if entry_date in target_weights.index else 0
                                if holding_days >= soft_stop_days:
                                    # 软止损：减仓而非全平
                                    adjusted_weights.loc[date, stock] = prev_weight * (1 - soft_stop_ratio)
                                    continue
                            
                            # 2. 全止盈（+40%，全部平仓）
                            if pnl_rate >= params.take_profit_pct:
                                adjusted_weights.loc[date, stock] = 0.0
                                tracker.remove_position(stock)
                                continue
                            
                            # 3. 第一批止盈（+20%，减仓50%）
                            if pnl_rate >= params.partial_profit_1_pct and not tracker.is_partial_profit_done(stock):
                                adjusted_weights.loc[date, stock] = prev_weight * (1 - params.partial_profit_1_ratio)
                                tracker.mark_partial_profit_done(stock)
                                continue
                            
                            # 4. 移动止损（达到一定盈利后）
                            if pnl_rate >= params.trailing_stop_trigger:
                                trailing_pnl_rate = (current_price / highest_price - 1.0)
                                if trailing_pnl_rate <= params.trailing_stop_pct:
                                    adjusted_weights.loc[date, stock] = 0.0
                                    tracker.remove_position(stock)
                                    continue
                            
                            # 5. 时间止损
                            entry_date = tracker.get_entry_date(stock)
                            if entry_date is not None:
                                # 计算持仓天数（交易日）
                                if isinstance(date, pd.Timestamp):
                                    date_val = date
                                else:
                                    date_val = pd.Timestamp(date)
                                if isinstance(entry_date, pd.Timestamp):
                                    entry_date_val = entry_date
                                else:
                                    entry_date_val = pd.Timestamp(entry_date)
                                days_held = (date_val - entry_date_val).days
                                if days_held >= params.time_stop_days:
                                    adjusted_weights.loc[date, stock] = 0.0
                                    tracker.remove_position(stock)
                                    continue
                
                # 如果买入（权重从0变为非0）
                if prev_weight < 1e-6 and curr_weight > 1e-6:
                    current_price = current_prices.get(stock)
                    if current_price is not None and not np.isnan(current_price):
                        tracker.update_cost_price(stock, current_price, date)
            
            # 确保权重和为1（归一化）
            total_weight = adjusted_weights.loc[date].sum()
            if total_weight > 1.0:
                adjusted_weights.loc[date] = adjusted_weights.loc[date] / total_weight
            elif total_weight < 0:
                adjusted_weights.loc[date] = 0.0
        
        return adjusted_weights
    
    def _calculate_trade_costs(
        self,
        weights: pd.DataFrame,
        portfolio_returns: pd.Series,
        close: pd.DataFrame,
    ) -> pd.Series:
        """
        精确计算交易成本
        
        Args:
            weights: 权重矩阵 (T x N)
            portfolio_returns: 组合收益率序列
            close: 收盘价矩阵 (T x N)
        
        Returns:
            交易成本序列
        """
        # 计算权重变化
        weight_changes = weights.diff().fillna(0)
        
        # 计算组合价值（基于累计收益）
        cumulative_returns = (1 + portfolio_returns).cumprod()
        portfolio_values = self.initial_capital * cumulative_returns
        
        # 计算买入和卖出金额
        buy_changes = weight_changes.clip(lower=0)  # 买入部分（权重增加）
        sell_changes = (-weight_changes).clip(lower=0)  # 卖出部分（权重减少）
        
        # 买入成本 = 买入金额 * (佣金率 + 滑点)
        buy_costs = buy_changes.multiply(portfolio_values, axis=0).sum(axis=1) * \
                    (self.commission_rate + self.slippage)
        
        # 卖出成本 = 卖出金额 * (佣金率 + 印花税 + 滑点)
        sell_costs = sell_changes.multiply(portfolio_values, axis=0).sum(axis=1) * \
                     (self.commission_rate + self.stamp_tax + self.slippage)
        
        # 总成本（转换为收益率）
        total_costs = buy_costs + sell_costs
        trade_costs = total_costs / portfolio_values
        
        return trade_costs.fillna(0)
    
    def _calculate_metrics(
        self,
        returns: pd.Series,
        cumulative_returns: pd.Series,
        weights: pd.DataFrame,
        close: pd.DataFrame,
    ) -> BacktestResult:
        """
        计算回测指标
        """
        result = BacktestResult()
        
        # 基本信息
        result.start_date = str(returns.index[0].date())
        result.end_date = str(returns.index[-1].date())
        result.trading_days = len(returns)
        
        # 总收益率
        result.total_return = (cumulative_returns.iloc[-1] - 1) * 100
        
        # 年化收益率（假设252交易日）
        years = len(returns) / 252
        if years > 0:
            result.annual_return = ((cumulative_returns.iloc[-1]) ** (1/years) - 1) * 100
        
        # 夏普比率
        excess_returns = returns - self.risk_free_rate / 252
        if excess_returns.std() > 0:
            result.sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
        
        # 最大回撤
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = (cumulative_returns - rolling_max) / rolling_max
        result.max_drawdown = abs(drawdowns.min()) * 100
        
        # 胜率（按日计算）
        winning_days = (returns > 0).sum()
        total_trading_days = (returns != 0).sum()
        if total_trading_days > 0:
            result.win_rate = winning_days / total_trading_days * 100
        
        # 交易次数（权重变化次数）
        weight_changes = weights.diff().abs()
        result.total_trades = int((weight_changes > 0.001).sum().sum())
        
        # 周收益统计
        weekly_returns = returns.resample('W').apply(lambda x: (1+x).prod() - 1)
        result.weekly_return_mean = weekly_returns.mean() * 100
        result.weekly_return_std = weekly_returns.std() * 100
        
        # 最大连续亏损
        is_loss = returns < 0
        loss_groups = (~is_loss).cumsum()
        if is_loss.any():
            result.max_consecutive_losses = is_loss.groupby(loss_groups).sum().max()
        
        # 换手率
        result.turnover = weight_changes.sum(axis=1).mean() * 100
        
        # 平均仓位
        result.avg_exposure = weights.sum(axis=1).mean() * 100
        
        return result


def run_vbt_backtest(
    data: DataMatrices,
    factors: FactorMatrices,
    params: SignalParams,
    initial_capital: float = 1000000.0,
) -> BacktestResult:
    """
    便捷函数：运行vectorbt回测
    
    Args:
        data: 数据矩阵
        factors: 因子矩阵
        params: 信号参数
        initial_capital: 初始资金
    
    Returns:
        BacktestResult
    """
    backtest = VBTBacktest(initial_capital=initial_capital)
    return backtest.run(data, factors, params)


def calculate_composite_score(result: BacktestResult, weights: Optional[Dict[str, float]] = None) -> float:
    """
    计算综合评分
    
    默认权重：
    - 年化收益 35%
    - 夏普比率 25%
    - 最大回撤 20%（越小越好）
    - 胜率 20%
    
    Args:
        result: 回测结果
        weights: 权重字典
    
    Returns:
        综合评分
    """
    if weights is None:
        weights = {
            "annual_return": 0.35,
            "sharpe_ratio": 0.25,
            "max_drawdown": 0.20,
            "win_rate": 0.20,
        }
    
    # 标准化各指标
    # 年化收益：直接使用（期望10-50%）
    annual_score = result.annual_return / 30 * 100  # 30%为基准
    
    # 夏普比率：期望1-3
    sharpe_score = result.sharpe_ratio / 2 * 100  # 2为基准
    
    # 最大回撤：越小越好（期望5-20%）
    drawdown_score = max(0, (30 - result.max_drawdown)) / 30 * 100  # 30%为最差
    
    # 胜率：期望45-60%
    winrate_score = result.win_rate / 55 * 100  # 55%为基准
    
    # 加权求和
    score = (
        weights.get("annual_return", 0.35) * annual_score +
        weights.get("sharpe_ratio", 0.25) * sharpe_score +
        weights.get("max_drawdown", 0.20) * drawdown_score +
        weights.get("win_rate", 0.20) * winrate_score
    )
    
    return score
