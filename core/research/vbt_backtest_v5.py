# -*- coding: utf-8 -*-
"""
vectorbt回测封装 V5.0 - 修复版
===============================

V5改进:
1. 修复最大回撤计算bug（之前显示正数或异常大的值）
2. 添加数值异常检测（NaN/Inf过滤，极端值限制）
3. 收益率合理性检查
4. 添加详细日志便于调试

作者: TRQuant Team
版本: V5.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import time
import warnings

import pandas as pd
import numpy as np

try:
    import vectorbt as vbt
    VBT_AVAILABLE = True
except ImportError:
    VBT_AVAILABLE = False

# 复用V4的基础类
from .vbt_backtest import (
    PositionTracker,
    BacktestResult,
)
from .data_provider import DataMatrices
from .factors import FactorMatrices, FactorCalculator
from .signals import SignalMatrices, SignalEngine, SignalParams

logger = logging.getLogger(__name__)


# ============ 数值异常检测与修复函数 ============

def sanitize_returns(
    returns: pd.Series,
    max_daily_return: float = 0.5,  # 单日最大收益50%
    min_daily_return: float = -0.5,  # 单日最大亏损50%
) -> pd.Series:
    """
    清理收益率序列，处理异常值
    
    Args:
        returns: 原始收益率序列
        max_daily_return: 单日收益上限
        min_daily_return: 单日收益下限
    
    Returns:
        清理后的收益率序列
    """
    # 替换NaN和Inf
    clean_returns = returns.copy()
    
    # 统计异常值
    nan_count = clean_returns.isna().sum()
    inf_count = np.isinf(clean_returns).sum()
    
    if nan_count > 0:
        logger.warning(f"收益率序列包含 {nan_count} 个NaN值，已替换为0")
        clean_returns = clean_returns.fillna(0)
    
    if inf_count > 0:
        logger.warning(f"收益率序列包含 {inf_count} 个Inf值，已限制范围")
        clean_returns = clean_returns.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    # 限制极端值
    extreme_high = (clean_returns > max_daily_return).sum()
    extreme_low = (clean_returns < min_daily_return).sum()
    
    if extreme_high > 0 or extreme_low > 0:
        logger.warning(f"收益率序列包含 {extreme_high} 个超上限值, {extreme_low} 个超下限值，已限制")
        clean_returns = clean_returns.clip(min_daily_return, max_daily_return)
    
    return clean_returns


def calculate_max_drawdown_v5(cumulative_returns: pd.Series) -> float:
    """
    V5版本：修复后的最大回撤计算
    
    最大回撤 = (峰值 - 谷值) / 峰值 * 100
    返回正数表示亏损百分比
    
    Args:
        cumulative_returns: 累计收益序列（1表示原值，1.1表示+10%）
    
    Returns:
        最大回撤百分比（正数，如20.5表示回撤20.5%）
    """
    if len(cumulative_returns) == 0:
        return 0.0
    
    # 清理异常值
    clean_cum = cumulative_returns.copy()
    
    # 检查NaN/Inf
    if clean_cum.isna().any() or np.isinf(clean_cum).any():
        logger.warning("累计收益包含异常值，进行清理")
        clean_cum = clean_cum.replace([np.inf, -np.inf], np.nan)
        clean_cum = clean_cum.ffill().fillna(1.0)
    
    # 检查是否有非正数（累计收益应该始终为正）
    if (clean_cum <= 0).any():
        logger.warning("累计收益包含非正数，修正为最小值0.01")
        clean_cum = clean_cum.clip(lower=0.01)
    
    # 计算滚动最大值
    rolling_max = clean_cum.expanding().max()
    
    # 计算回撤（负数）
    drawdowns = (clean_cum - rolling_max) / rolling_max
    
    # 最大回撤（取绝对值，返回正数）
    max_drawdown = abs(drawdowns.min()) * 100
    
    # 合理性检查：回撤不应超过100%
    if max_drawdown > 100:
        logger.warning(f"计算出的最大回撤 {max_drawdown:.2f}% 超过100%，限制为100%")
        max_drawdown = 100.0
    
    return max_drawdown


def check_result_sanity(result: BacktestResult) -> BacktestResult:
    """
    检查回测结果的合理性，标记异常
    
    Args:
        result: 原始回测结果
    
    Returns:
        检查后的回测结果
    """
    issues = []
    
    # 检查年化收益率
    if abs(result.annual_return) > 10000:
        issues.append(f"年化收益率 {result.annual_return:.2f}% 异常高")
        # 不直接修改，但记录
    
    # 检查夏普比率
    if abs(result.sharpe_ratio) > 50:
        issues.append(f"夏普比率 {result.sharpe_ratio:.2f} 异常")
    
    # 检查最大回撤
    if result.max_drawdown < 0:
        issues.append(f"最大回撤 {result.max_drawdown:.2f}% 为负数（已修复）")
        result.max_drawdown = abs(result.max_drawdown)
    
    if result.max_drawdown > 100:
        issues.append(f"最大回撤 {result.max_drawdown:.2f}% 超过100%（已修复）")
        result.max_drawdown = 100.0
    
    # 检查胜率
    if result.win_rate > 100 or result.win_rate < 0:
        issues.append(f"胜率 {result.win_rate:.2f}% 超出范围（已修复）")
        result.win_rate = max(0, min(100, result.win_rate))
    
    if issues:
        logger.warning(f"回测结果合理性检查发现问题: {issues}")
    
    return result


# ============ V5版本回测引擎 ============

class VBTBacktestV5:
    """
    V5版本回测引擎
    
    改进:
    1. 修复最大回撤计算
    2. 添加数值异常检测
    3. 支持市场类型适配参数
    """
    
    def __init__(
        self,
        initial_cash: float = 1_000_000,
        commission_rate: float = 0.0001,  # 华泰证券标准: 0.01%
        stamp_duty: float = 0.001,  # 印花税: 0.1% (仅卖出)
        slippage: float = 0.001,
        transfer_fee_rate: float = 0.00001,  # 过户费: 0.001% (买卖双向)
        regulatory_fee_rate: float = 0.0000687,  # 监管费: 0.00687% (买卖双向)
        min_commission: float = 5.0,  # 最低佣金: 5元
        risk_free_rate: float = 0.03,
    ):
        """
        初始化回测引擎（华泰证券标准）
        
        Args:
            initial_cash: 初始资金
            commission_rate: 佣金率（买卖双向，默认0.01%）
            stamp_duty: 印花税（仅卖出，默认0.1%）
            slippage: 滑点（默认0.1%）
            transfer_fee_rate: 过户费率（买卖双向，默认0.001%）
            regulatory_fee_rate: 监管费率（买卖双向，默认0.00687%）
            min_commission: 最低佣金（默认5元）
            risk_free_rate: 无风险利率
        """
        self.initial_cash = initial_cash
        self.commission_rate = commission_rate
        self.stamp_duty = stamp_duty
        self.slippage = slippage
        self.transfer_fee_rate = transfer_fee_rate
        self.regulatory_fee_rate = regulatory_fee_rate
        self.min_commission = min_commission
        self.risk_free_rate = risk_free_rate
        
        logger.info(f"VBTBacktestV5初始化: 资金={initial_cash:,.0f}, 佣金={commission_rate:.4%}, 印花税={stamp_duty:.4%}, "
                   f"过户费={transfer_fee_rate:.6%}, 监管费={regulatory_fee_rate:.6%}, 最低佣金={min_commission:.0f}元")
    
    def run_with_signals(
        self,
        data: DataMatrices,
        signals: SignalMatrices,
        params: SignalParams = None,
    ) -> BacktestResult:
        """
        基于信号运行回测
        
        Args:
            data: 数据矩阵
            signals: 信号矩阵
            params: 信号参数（用于止损止盈）
        
        Returns:
            回测结果
        """
        start_time = time.time()
        
        if params is None:
            params = SignalParams()
        
        # 获取数据
        close = data.close
        entries = signals.entries
        scores = signals.scores
        
        # 生成目标权重
        target_weights = self._generate_weights(entries, scores, params)
        
        # 应用止损止盈（如果有参数）
        tracker = PositionTracker()
        adjusted_weights = self._apply_stop_loss_take_profit_v5(
            target_weights, close, tracker, params
        )
        
        # 计算组合收益
        portfolio_returns = self._calculate_portfolio_returns(adjusted_weights, close)
        
        # 计算交易成本
        trade_costs = self._calculate_trade_costs_v5(adjusted_weights, close)
        
        # 净收益率
        net_returns = portfolio_returns - trade_costs
        
        # 清理收益率
        net_returns = sanitize_returns(net_returns)
        
        # 计算累计收益
        cumulative_returns = (1 + net_returns).cumprod()
        
        # 计算指标（使用V5版本）
        result = self._calculate_metrics_v5(
            net_returns, 
            cumulative_returns, 
            adjusted_weights,
            close,
        )
        
        # 合理性检查
        result = check_result_sanity(result)
        
        elapsed = time.time() - start_time
        logger.info(f"VBTBacktestV5完成: 总收益={result.total_return:.2f}%, 最大回撤={result.max_drawdown:.2f}%, 耗时={elapsed:.2f}s")
        
        return result
    
    def _generate_weights(
        self,
        entries: pd.DataFrame,
        scores: pd.DataFrame,
        params: SignalParams,
    ) -> pd.DataFrame:
        """生成目标权重矩阵"""
        # 按评分排序选取Top N
        max_positions = params.max_positions
        single_max = params.single_position_max
        
        weights = pd.DataFrame(0.0, index=entries.index, columns=entries.columns)
        
        for date in entries.index:
            # 当日入场信号
            entry_mask = entries.loc[date]
            entry_stocks = entry_mask[entry_mask].index.tolist()
            
            if not entry_stocks:
                continue
            
            # 按评分排序
            day_scores = scores.loc[date, entry_stocks]
            top_stocks = day_scores.nlargest(max_positions).index.tolist()
            
            # 等权分配
            if len(top_stocks) > 0:
                weight_per_stock = min(single_max, 1.0 / len(top_stocks))
                weights.loc[date, top_stocks] = weight_per_stock
        
        return weights
    
    def _apply_stop_loss_take_profit_v5(
        self,
        target_weights: pd.DataFrame,
        close: pd.DataFrame,
        tracker: PositionTracker,
        params: SignalParams,
    ) -> pd.DataFrame:
        """
        V5版本：应用止损止盈规则
        
        新增：涨停板特殊处理
        """
        adjusted_weights = target_weights.copy()
        symbols = list(target_weights.columns)
        
        # 计算涨停标记（日涨幅>9%）
        daily_returns = close / close.shift(1) - 1
        is_limit_up = daily_returns > 0.09
        
        # 逐日处理
        for i, date in enumerate(target_weights.index):
            if i > 0:
                prev_weights = adjusted_weights.iloc[i-1]
            else:
                prev_weights = pd.Series(0.0, index=symbols)
            curr_weights = target_weights.iloc[i].copy()
            current_prices = close.loc[date]
            
            for stock in symbols:
                prev_weight = prev_weights.get(stock, 0)
                curr_weight = curr_weights.get(stock, 0)
                current_price = current_prices.get(stock, np.nan)
                
                if pd.isna(current_price) or current_price <= 0:
                    adjusted_weights.loc[date, stock] = 0.0
                    continue
                
                # 新建仓
                if prev_weight < 0.001 and curr_weight > 0.001:
                    tracker.update_cost_price(stock, current_price, date)
                    adjusted_weights.loc[date, stock] = curr_weight
                    continue
                
                # 已有持仓
                if prev_weight > 0.001:
                    tracker.update_highest_price(stock, current_price)
                    cost_price = tracker.get_cost_price(stock)
                    highest_price = tracker.get_highest_price(stock)
                    
                    if cost_price is None or cost_price <= 0:
                        adjusted_weights.loc[date, stock] = prev_weight
                        continue
                    
                    pnl_rate = (current_price / cost_price - 1.0)
                    
                    # ===== 涨停板特殊处理 =====
                    # 涨停不卖：当日涨停时，不触发止盈卖出
                    stock_is_limit_up = is_limit_up.loc[date, stock] if stock in is_limit_up.columns else False
                    
                    if stock_is_limit_up and pnl_rate > 0:
                        # 涨停持有，不触发止盈
                        adjusted_weights.loc[date, stock] = prev_weight
                        logger.debug(f"{date}: {stock} 涨停中，持有不卖")
                        continue
                    
                    # ===== 止损逻辑 =====
                    # 1. 硬止损
                    if pnl_rate <= params.stop_loss_pct:
                        adjusted_weights.loc[date, stock] = 0.0
                        tracker.remove_position(stock)
                        logger.debug(f"{date}: {stock} 触发硬止损 {pnl_rate:.2%}")
                        continue
                    
                    # 2. 软止损（仅在非涨停时触发）
                    entry_date = tracker.get_entry_date(stock)
                    if entry_date is not None:
                        holding_days = (date - entry_date).days if hasattr(date, '__sub__') else 0
                        soft_stop_pct = getattr(params, 'soft_stop_loss_pct', -0.08)
                        soft_stop_days = getattr(params, 'soft_stop_loss_days', 3)
                        
                        if pnl_rate <= soft_stop_pct and holding_days >= soft_stop_days:
                            adjusted_weights.loc[date, stock] = prev_weight * 0.5
                            logger.debug(f"{date}: {stock} 触发软止损，减仓50%")
                            continue
                    
                    # ===== 止盈逻辑 =====
                    # 3. 第二批止盈（全部平仓）
                    if pnl_rate >= params.take_profit_pct:
                        adjusted_weights.loc[date, stock] = 0.0
                        tracker.remove_position(stock)
                        logger.debug(f"{date}: {stock} 触发全止盈 {pnl_rate:.2%}")
                        continue
                    
                    # 4. 第一批止盈（减仓50%）
                    partial_1_pct = getattr(params, 'partial_profit_1_pct', 0.2)
                    partial_1_ratio = getattr(params, 'partial_profit_1_ratio', 0.5)
                    
                    if pnl_rate >= partial_1_pct and not tracker.is_partial_profit_done(stock):
                        adjusted_weights.loc[date, stock] = prev_weight * (1 - partial_1_ratio)
                        tracker.mark_partial_profit_done(stock)
                        logger.debug(f"{date}: {stock} 触发第一批止盈，减仓{partial_1_ratio:.0%}")
                        continue
                    
                    # 5. 移动止损
                    trailing_trigger = getattr(params, 'trailing_stop_trigger', 0.12)
                    trailing_pct = getattr(params, 'trailing_stop_pct', -0.06)
                    
                    if highest_price and pnl_rate >= trailing_trigger:
                        trailing_pnl_rate = (current_price / highest_price - 1.0)
                        if trailing_pnl_rate <= trailing_pct:
                            adjusted_weights.loc[date, stock] = 0.0
                            tracker.remove_position(stock)
                            logger.debug(f"{date}: {stock} 触发移动止损")
                            continue
                    
                    # 6. 时间止损
                    time_stop_days = getattr(params, 'time_stop_days', 20)
                    if entry_date is not None:
                        holding_days = (date - entry_date).days if hasattr(date, '__sub__') else 0
                        if holding_days >= time_stop_days and pnl_rate < 0:
                            adjusted_weights.loc[date, stock] = 0.0
                            tracker.remove_position(stock)
                            logger.debug(f"{date}: {stock} 触发时间止损")
                            continue
                    
                    # 保持持仓
                    adjusted_weights.loc[date, stock] = prev_weight
        
        return adjusted_weights
    
    def _calculate_portfolio_returns(
        self,
        weights: pd.DataFrame,
        close: pd.DataFrame,
    ) -> pd.Series:
        """计算组合收益率"""
        # 对齐数据
        common_dates = weights.index.intersection(close.index)
        common_stocks = weights.columns.intersection(close.columns)
        
        weights_aligned = weights.loc[common_dates, common_stocks]
        close_aligned = close.loc[common_dates, common_stocks]
        
        # 计算个股收益率
        stock_returns = close_aligned / close_aligned.shift(1) - 1
        stock_returns = stock_returns.fillna(0)
        
        # 组合收益 = 权重 * 个股收益
        portfolio_returns = (weights_aligned.shift(1) * stock_returns).sum(axis=1)
        
        return portfolio_returns
    
    def _calculate_trade_costs_v5(
        self,
        weights: pd.DataFrame,
        close: pd.DataFrame,
    ) -> pd.Series:
        """
        V5版本：精确计算交易成本（华泰证券标准）
        
        区分买卖：
        - 买入：佣金 + 过户费 + 监管费 + 滑点
        - 卖出：佣金 + 过户费 + 监管费 + 印花税 + 滑点
        
        注意：最低佣金需要按实际交易金额计算，这里简化处理
        """
        weight_changes = weights.diff().fillna(0)
        
        # 买入量和卖出量
        buys = weight_changes.clip(lower=0)
        sells = (-weight_changes).clip(lower=0)
        
        # 计算实际交易金额（权重 * 价格）
        buy_amounts = buys * close
        sell_amounts = sells * close
        
        # 买入成本率 = 佣金 + 过户费 + 监管费 + 滑点
        buy_cost_rate = (self.commission_rate + 
                        self.transfer_fee_rate + 
                        self.regulatory_fee_rate + 
                        self.slippage)
        
        # 卖出成本率 = 佣金 + 过户费 + 监管费 + 印花税 + 滑点
        sell_cost_rate = (self.commission_rate + 
                         self.transfer_fee_rate + 
                         self.regulatory_fee_rate + 
                         self.stamp_duty + 
                         self.slippage)
        
        # 买入成本
        buy_costs = buy_amounts * buy_cost_rate
        
        # 卖出成本
        sell_costs = sell_amounts * sell_cost_rate
        
        # 总成本（按日期汇总）
        total_costs = (buy_costs + sell_costs).sum(axis=1)
        
        return total_costs
    
    def _calculate_metrics_v5(
        self,
        returns: pd.Series,
        cumulative_returns: pd.Series,
        weights: pd.DataFrame,
        close: pd.DataFrame,
    ) -> BacktestResult:
        """
        V5版本：计算回测指标（修复bug）
        """
        result = BacktestResult()
        
        # 基本信息
        result.start_date = str(returns.index[0].date()) if hasattr(returns.index[0], 'date') else str(returns.index[0])
        result.end_date = str(returns.index[-1].date()) if hasattr(returns.index[-1], 'date') else str(returns.index[-1])
        result.trading_days = len(returns)
        
        # 总收益率
        final_return = cumulative_returns.iloc[-1]
        
        # 检查异常值
        if np.isnan(final_return) or np.isinf(final_return):
            logger.warning(f"最终累计收益异常: {final_return}，设置为1.0")
            final_return = 1.0
        
        result.total_return = (final_return - 1) * 100
        
        # 年化收益率
        years = len(returns) / 252
        if years > 0 and final_return > 0:
            result.annual_return = ((final_return) ** (1/years) - 1) * 100
        else:
            result.annual_return = 0.0
        
        # 夏普比率
        excess_returns = returns - self.risk_free_rate / 252
        std = excess_returns.std()
        if std > 0 and not np.isnan(std):
            result.sharpe_ratio = np.sqrt(252) * excess_returns.mean() / std
        else:
            result.sharpe_ratio = 0.0
        
        # ===== V5修复：最大回撤计算 =====
        result.max_drawdown = calculate_max_drawdown_v5(cumulative_returns)
        
        # 胜率（按日计算）
        winning_days = (returns > 0).sum()
        total_trading_days = (returns != 0).sum()
        if total_trading_days > 0:
            result.win_rate = winning_days / total_trading_days * 100
        
        # 交易次数
        weight_changes = weights.diff().abs()
        result.total_trades = int((weight_changes > 0.001).sum().sum())
        
        # 周收益统计
        try:
            weekly_returns = returns.resample('W').apply(lambda x: (1+x).prod() - 1)
            result.weekly_return_mean = weekly_returns.mean() * 100
            result.weekly_return_std = weekly_returns.std() * 100
        except Exception as e:
            logger.warning(f"周收益计算失败: {e}")
            result.weekly_return_mean = 0.0
            result.weekly_return_std = 0.0
        
        # 最大连续亏损
        is_loss = returns < 0
        loss_groups = (~is_loss).cumsum()
        if is_loss.any():
            try:
                result.max_consecutive_losses = int(is_loss.groupby(loss_groups).sum().max())
            except:
                result.max_consecutive_losses = 0
        
        # 换手率
        result.turnover = weight_changes.sum(axis=1).mean() * 100
        
        # 平均仓位
        result.avg_exposure = weights.sum(axis=1).mean() * 100
        
        return result


# ============ 测试函数 ============

def test_vbt_backtest_v5():
    """测试V5回测引擎"""
    print("=" * 60)
    print("VBTBacktestV5 单元测试")
    print("=" * 60)
    
    # 测试1: 最大回撤计算
    print("\n1. 测试最大回撤计算...")
    
    # 模拟累计收益：1.0 -> 1.2 -> 0.9 -> 1.1
    test_cum = pd.Series([1.0, 1.2, 0.9, 1.1])
    # 最大回撤应该是 (1.2 - 0.9) / 1.2 = 25%
    mdd = calculate_max_drawdown_v5(test_cum)
    expected_mdd = 25.0
    print(f"   累计收益: {test_cum.tolist()}")
    print(f"   计算回撤: {mdd:.2f}%")
    print(f"   预期回撤: {expected_mdd:.2f}%")
    assert abs(mdd - expected_mdd) < 1, f"最大回撤计算错误: {mdd} vs {expected_mdd}"
    print("   ✓ 通过")
    
    # 测试2: 异常值处理
    print("\n2. 测试异常值处理...")
    
    test_cum_nan = pd.Series([1.0, np.nan, 1.1, np.inf, 0.9])
    mdd_nan = calculate_max_drawdown_v5(test_cum_nan)
    print(f"   含NaN/Inf的累计收益: {test_cum_nan.tolist()}")
    print(f"   计算回撤: {mdd_nan:.2f}%")
    assert 0 <= mdd_nan <= 100, f"回撤超出范围: {mdd_nan}"
    print("   ✓ 通过")
    
    # 测试3: 收益率清理
    print("\n3. 测试收益率清理...")
    
    test_returns = pd.Series([0.01, -0.02, 0.8, -0.6, np.nan, 0.03])
    clean_returns = sanitize_returns(test_returns)
    print(f"   原始收益: {test_returns.tolist()}")
    print(f"   清理后: {clean_returns.tolist()}")
    assert not clean_returns.isna().any(), "清理后仍有NaN"
    assert (clean_returns <= 0.5).all() and (clean_returns >= -0.5).all(), "清理后仍有极端值"
    print("   ✓ 通过")
    
    print("\n" + "=" * 60)
    print("所有测试通过!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_vbt_backtest_v5()
