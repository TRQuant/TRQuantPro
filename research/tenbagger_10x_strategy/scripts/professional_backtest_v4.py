#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Professional Backtest Strategy V4 - 专业回测策略V4
=================================================

整合扎实知识库：
1. 专业技术指标分析（MACD/RSI/BOLL/KDJ/VOL）
2. 策略切换决策器
3. 仓位调整策略
4. 风险控制规则
5. 策略过渡管理
"""

import sys
import os
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass, field

PROJECT_ROOT = "/home/taotao/dev/QuantTest/TRQuant"
sys.path.insert(0, PROJECT_ROOT)

# 导入知识库
from research.tenbagger_10x_strategy.knowledge.astock_regime_knowledge_v2 import (
    AStockRegime,
    ASTOCK_REGIME_STRATEGY,
    AStockRegimeDetectorV2
)
from research.tenbagger_10x_strategy.knowledge.professional_indicators_kb import (
    SignalType,
    ComprehensiveTechnicalAnalysis
)
from research.tenbagger_10x_strategy.knowledge.strategy_switching_kb import (
    RegimeSwitchDecider,
    PositionAdjustmentStrategy,
    StrategyTransitionManager,
    RISK_CONTROL_RULES
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class BacktestResult:
    total_return: float
    annualized_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    equity_curve: pd.DataFrame = None
    regime_performance: Dict[str, float] = field(default_factory=dict)
    regime_days: Dict[str, int] = field(default_factory=dict)


class ProfessionalBacktestV4:
    """专业回测策略V4 - 整合扎实知识库"""
    
    def __init__(self, initial_capital: float = 1_000_000):
        self._jq = None
        self.initial_capital = initial_capital
        
        # 知识库组件
        self.regime_detector = AStockRegimeDetectorV2()
        self.switch_decider = RegimeSwitchDecider()
        self.transition_manager = StrategyTransitionManager()
        
        # 风险控制
        self.max_drawdown_limit = 0.15
        self.consecutive_loss_count = 0
        self.pause_trading_days = 0
        
    def _ensure_jqdata(self):
        """确保JQData连接"""
        if self._jq is None:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            cm = get_config_manager()
            jqcfg = cm.get_config('jqdata')
            jq.auth(jqcfg['username'], jqcfg['password'])
            self._jq = jq
            logger.info(f"JQData认证成功: {jqcfg['username']}")
    
    def _get_universe(self, date: str) -> List[str]:
        """获取股票池"""
        self._ensure_jqdata()
        stocks = self._jq.get_index_stocks('000300.XSHG', date=date)
        return stocks[:100]
    
    def _preload_data(self, start_date: str, end_date: str, stocks: List[str]) -> Dict:
        """预加载数据"""
        self._ensure_jqdata()
        jq = self._jq
        
        logger.info(f"预加载数据: {len(stocks)}只股票")
        start_time = time.time()
        
        price_data = {}
        for stock in stocks:
            try:
                df = jq.get_price(
                    stock,
                    start_date=start_date,
                    end_date=end_date,
                    frequency='daily',
                    fields=['open', 'close', 'high', 'low', 'volume'],
                    skip_paused=True,
                    fq='pre'
                )
                if df is not None and len(df) > 0:
                    price_data[stock] = df
            except:
                pass
        
        index_data = jq.get_price(
            '000300.XSHG',
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            skip_paused=True
        )
        
        elapsed = time.time() - start_time
        logger.info(f"数据预加载完成: {len(price_data)}只, 耗时{elapsed:.1f}秒")
        
        return {'prices': price_data, 'index': index_data, 'stocks': list(price_data.keys())}
    
    def _select_stocks_with_indicators(self, data: Dict, regime: AStockRegime, 
                                       date: str) -> List[Tuple[str, float]]:
        """使用综合技术指标选股"""
        scores = []
        
        for stock, df in data['prices'].items():
            try:
                df_to_date = df[df.index <= date]
                if len(df_to_date) < 35:
                    continue
                
                closes = df_to_date['close']
                volumes = df_to_date['volume']
                highs = df_to_date['high']
                lows = df_to_date['low']
                
                # 综合技术分析
                analysis = ComprehensiveTechnicalAnalysis.analyze_all(
                    closes, volumes, highs, lows
                )
                
                overall_signal = analysis['overall_signal']
                tech_score = analysis['score']
                confidence = analysis['confidence']
                
                # 根据环境过滤
                if regime in [AStockRegime.BULL_EARLY, AStockRegime.BULL_MID]:
                    # 牛市：选择买入信号的股票
                    if overall_signal in [SignalType.STRONG_BUY, SignalType.BUY]:
                        # 额外检查：动量
                        ret20 = closes.iloc[-1] / closes.iloc[-20] - 1
                        if ret20 > 0:
                            score = tech_score * 50 + confidence * 30 + ret20 * 100
                            scores.append((stock, score))
                            
                elif regime in [AStockRegime.BULL_LATE]:
                    # 牛市末期：选择高位持稳的
                    if overall_signal in [SignalType.BUY, SignalType.WEAK_BUY, SignalType.HOLD]:
                        high_20 = closes.rolling(20).max().iloc[-1]
                        current = closes.iloc[-1]
                        drawdown = (high_20 - current) / high_20
                        if drawdown < 0.08:  # 回撤小于8%
                            score = (1 - drawdown) * 100 + confidence * 20
                            scores.append((stock, score))
                            
                elif regime in [AStockRegime.BEAR_GRINDING]:
                    # 熊市磨底：选择超跌反弹信号
                    if overall_signal in [SignalType.STRONG_BUY]:
                        rsi_signal = analysis['signals'].get('RSI')
                        if rsi_signal and rsi_signal.value < 30:
                            score = tech_score * 30 + (30 - rsi_signal.value) * 2
                            scores.append((stock, score))
                            
                elif regime in [AStockRegime.VOLATILE_UP]:
                    # 震荡向上：选择支撑位买入信号
                    if overall_signal in [SignalType.BUY, SignalType.WEAK_BUY]:
                        boll_signal = analysis['signals'].get('BOLL')
                        if boll_signal and 'lower' in boll_signal.reason.lower():
                            score = tech_score * 40 + confidence * 30
                            scores.append((stock, score))
                            
                elif regime in [AStockRegime.VOLATILE_DOWN]:
                    # 震荡向下：只选极度超跌
                    if overall_signal == SignalType.STRONG_BUY:
                        rsi_signal = analysis['signals'].get('RSI')
                        if rsi_signal and rsi_signal.value < 25:
                            score = (25 - rsi_signal.value) * 4 + confidence * 20
                            scores.append((stock, score))
                            
                elif regime in [AStockRegime.VOLATILE_RANGE]:
                    # 区间震荡：均值回归
                    ma20 = closes.rolling(20).mean().iloc[-1]
                    deviation = (closes.iloc[-1] - ma20) / ma20
                    if deviation < -0.03 and overall_signal in [SignalType.BUY, SignalType.STRONG_BUY]:
                        score = abs(deviation) * 200 + tech_score * 20
                        scores.append((stock, score))
                        
            except Exception as e:
                pass
        
        scores.sort(key=lambda x: x[1], reverse=True)
        max_stocks = ASTOCK_REGIME_STRATEGY.get(regime, {}).get('max_stocks', 3)
        return scores[:max_stocks]
    
    def run_backtest(self, start_date: str, end_date: str) -> BacktestResult:
        """运行回测"""
        logger.info(f"开始专业回测V4: {start_date} 至 {end_date}")
        start_time = time.time()
        
        self._ensure_jqdata()
        jq = self._jq
        
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [d.strftime("%Y-%m-%d") if hasattr(d, 'strftime') else str(d) for d in trade_days]
        
        stocks = self._get_universe(start_date)
        data = self._preload_data(start_date, end_date, stocks)
        
        if not data['prices']:
            logger.error("没有可用的价格数据")
            return BacktestResult(0, 0, 0, 0, 0, 0, 0)
        
        # 初始化
        cash = self.initial_capital
        positions = {}
        equity_history = []
        trades = 0
        regime_returns = {r.value: [] for r in AStockRegime}
        regime_days_count = {r.value: 0 for r in AStockRegime}
        prev_value = self.initial_capital
        wins = 0
        total_sells = 0
        peak_value = self.initial_capital
        
        # 重置状态
        self.switch_decider = RegimeSwitchDecider()
        self.transition_manager = StrategyTransitionManager()
        self.consecutive_loss_count = 0
        self.pause_trading_days = 0
        
        for i, date in enumerate(trade_days):
            if i < 120:
                equity_history.append((date, cash))
                continue
            
            # 检测市场环境
            df_to_date = data['index'][data['index'].index <= date]
            if len(df_to_date) < 120:
                equity_history.append((date, cash))
                continue
                
            prices = df_to_date['close']
            volumes = df_to_date['volume']
            
            _, score, details = self.regime_detector.detect_regime(prices, volumes)
            
            # 使用切换决策器
            switched, new_regime = self.switch_decider.should_switch(score, date)
            regime = self.switch_decider.current_regime
            
            if switched:
                logger.info(f"[{date}] 环境切换 → {regime.value} (分数:{score:.1f})")
                self.transition_manager.start_transition(
                    self.switch_decider.current_regime, new_regime, date
                )
            
            # 更新过渡状态
            self.transition_manager.update_transition()
            
            regime_days_count[regime.value] += 1
            
            # 获取策略参数（过渡期使用混合参数）
            if self.transition_manager.transition_in_progress:
                params = self.transition_manager.get_blended_params()
            else:
                params = ASTOCK_REGIME_STRATEGY.get(regime, ASTOCK_REGIME_STRATEGY[AStockRegime.VOLATILE_RANGE])
            
            target_position = params.get('position', 0.3)
            stop_loss = params.get('stop_loss', 0.10)
            take_profit = params.get('take_profit', 0.20)
            max_stocks = params.get('max_stocks', 3)
            rebalance_freq = params.get('rebalance_freq', 5)
            
            # 计算当前持仓市值
            total_value = cash
            for stock, (shares, cost, entry_date) in list(positions.items()):
                if stock in data['prices']:
                    df = data['prices'][stock]
                    df_today = df[df.index <= date]
                    if len(df_today) > 0:
                        price = df_today['close'].iloc[-1]
                        total_value += price * shares
                        
                        # 止损止盈
                        pnl_pct = price / cost - 1
                        should_sell = False
                        sell_reason = ""
                        
                        if pnl_pct < -stop_loss:
                            should_sell = True
                            sell_reason = f"止损{pnl_pct*100:.1f}%"
                        elif pnl_pct > take_profit:
                            should_sell = True
                            sell_reason = f"止盈{pnl_pct*100:.1f}%"
                        
                        if should_sell:
                            cash += price * shares
                            del positions[stock]
                            trades += 1
                            total_sells += 1
                            if pnl_pct > 0:
                                wins += 1
                                self.consecutive_loss_count = 0
                            else:
                                self.consecutive_loss_count += 1
                            logger.debug(f"[{date}] {sell_reason} {stock}")
            
            # 更新峰值
            peak_value = max(peak_value, total_value)
            current_drawdown = (peak_value - total_value) / peak_value
            
            # 风险控制：最大回撤保护
            if current_drawdown > self.max_drawdown_limit:
                target_position = 0.2
                
            # 风险控制：连续亏损暂停
            if self.consecutive_loss_count >= 3:
                self.pause_trading_days = 3
                self.consecutive_loss_count = 0
            
            if self.pause_trading_days > 0:
                self.pause_trading_days -= 1
                # 暂停期间不买入
                equity_history.append((date, total_value))
                daily_ret = total_value / prev_value - 1 if prev_value > 0 else 0
                regime_returns[regime.value].append(daily_ret)
                prev_value = total_value
                continue
            
            # 仓位管理
            current_position_value = total_value - cash
            target_value = total_value * target_position
            
            # 熊市恐慌期强制清仓
            if regime == AStockRegime.BEAR_PANIC:
                for stock, (shares, cost, _) in list(positions.items()):
                    if stock in data['prices']:
                        df = data['prices'][stock]
                        df_today = df[df.index <= date]
                        if len(df_today) > 0:
                            price = df_today['close'].iloc[-1]
                            pnl_pct = price / cost - 1
                            cash += price * shares
                            del positions[stock]
                            trades += 1
                            total_sells += 1
                            if pnl_pct > 0:
                                wins += 1
                            logger.info(f"[{date}] 恐慌清仓 {stock} 盈亏{pnl_pct*100:.1f}%")
            
            # 其他需要减仓的情况
            elif current_position_value > target_value * 1.1:
                to_sell = []
                for stock, (shares, cost, _) in positions.items():
                    if stock in data['prices']:
                        df = data['prices'][stock]
                        df_today = df[df.index <= date]
                        if len(df_today) > 0:
                            price = df_today['close'].iloc[-1]
                            pnl_pct = price / cost - 1
                            to_sell.append((stock, shares, cost, price, pnl_pct))
                
                to_sell.sort(key=lambda x: x[4])
                
                for stock, shares, cost, price, pnl_pct in to_sell:
                    if current_position_value <= target_value:
                        break
                    cash += price * shares
                    current_position_value -= price * shares
                    del positions[stock]
                    trades += 1
                    total_sells += 1
                    if pnl_pct > 0:
                        wins += 1
                    logger.info(f"[{date}] 减仓({regime.value}) {stock} 盈亏{pnl_pct*100:.1f}%")
            
            # 选股和买入
            if (i % rebalance_freq == 0 and len(positions) < max_stocks and 
                regime != AStockRegime.BEAR_PANIC):
                
                candidates = self._select_stocks_with_indicators(data, regime, date)
                
                for stock, score in candidates:
                    if stock in positions:
                        continue
                    if len(positions) >= max_stocks:
                        break
                    if stock not in data['prices']:
                        continue
                    
                    available_for_buy = min(cash * 0.8, target_value - current_position_value)
                    if available_for_buy < total_value * 0.05:
                        break
                    
                    df = data['prices'][stock]
                    df_today = df[df.index <= date]
                    if len(df_today) == 0:
                        continue
                    
                    price = df_today['close'].iloc[-1]
                    max_per_stock = total_value * 0.25
                    shares = int(min(max_per_stock, available_for_buy) / price / 100) * 100
                    
                    if shares >= 100:
                        cost = price * shares
                        cash -= cost
                        current_position_value += cost
                        positions[stock] = (shares, price, date)
                        trades += 1
                        logger.info(f"[{date}] 买入({regime.value}) {stock} @{price:.2f} x{shares} 得分:{score:.1f}")
            
            equity_history.append((date, total_value))
            daily_ret = total_value / prev_value - 1 if prev_value > 0 else 0
            regime_returns[regime.value].append(daily_ret)
            prev_value = total_value
            
            if i % 50 == 0 or switched:
                ret = (total_value / self.initial_capital - 1) * 100
                pos_pct = (total_value - cash) / total_value * 100
                logger.info(f"[{date}] 净值:{total_value:,.0f} 收益:{ret:.1f}% 仓位:{pos_pct:.0f}% 环境:{regime.value}")
        
        elapsed = time.time() - start_time
        logger.info(f"回测完成，耗时: {elapsed:.1f}秒")
        
        return self._calc_result(equity_history, regime_returns, regime_days_count, trades, wins, total_sells)
    
    def _calc_result(self, equity_history, regime_returns, regime_days_count, 
                     trades, wins, total_sells) -> BacktestResult:
        """计算回测结果"""
        values = [x[1] for x in equity_history]
        if not values:
            return BacktestResult(0, 0, 0, 0, 0, 0, 0)
        
        total_ret = (values[-1] / self.initial_capital - 1) * 100
        years = max(len(values) / 252, 0.01)
        annual_ret = ((values[-1] / self.initial_capital) ** (1/years) - 1) * 100
        
        returns = pd.Series(values).pct_change().dropna()
        sharpe = np.sqrt(252) * returns.mean() / returns.std() if len(returns) > 0 and returns.std() > 0 else 0
        
        cummax = pd.Series(values).cummax()
        drawdown = (cummax - pd.Series(values)) / cummax
        max_dd = drawdown.max() * 100
        
        win_rate = wins / total_sells * 100 if total_sells > 0 else 0
        
        regime_perf = {r: sum(rets) * 100 for r, rets in regime_returns.items() if rets}
        
        df = pd.DataFrame(equity_history, columns=['date', 'equity'])
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        return BacktestResult(
            total_return=total_ret,
            annualized_return=annual_ret,
            sharpe_ratio=sharpe,
            max_drawdown=max_dd,
            win_rate=win_rate,
            profit_factor=0,
            total_trades=trades,
            equity_curve=df,
            regime_performance=regime_perf,
            regime_days=regime_days_count
        )


def quick_test(period: str = "1y"):
    """快速测试"""
    end_date = "2024-06-30"
    period_map = {"3m": 90, "6m": 180, "1y": 365, "2y": 730, "3y": 1095}
    
    days = period_map.get(period, 365)
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    start_dt = end_dt - timedelta(days=days)
    start_date = start_dt.strftime("%Y-%m-%d")
    
    logger.info(f"{'='*60}")
    logger.info(f"专业回测V4 - 周期: {period}")
    logger.info(f"时间范围: {start_date} 至 {end_date}")
    logger.info(f"{'='*60}")
    
    strategy = ProfessionalBacktestV4()
    result = strategy.run_backtest(start_date, end_date)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"回测结果")
    logger.info(f"{'='*60}")
    logger.info(f"总收益率: {result.total_return:.2f}%")
    logger.info(f"年化收益率: {result.annualized_return:.2f}%")
    logger.info(f"夏普比率: {result.sharpe_ratio:.2f}")
    logger.info(f"最大回撤: {result.max_drawdown:.2f}%")
    logger.info(f"胜率: {result.win_rate:.1f}%")
    logger.info(f"交易次数: {result.total_trades}")
    
    if result.regime_performance:
        logger.info(f"\n市场环境表现:")
        sorted_perf = sorted(result.regime_performance.items(), key=lambda x: x[1], reverse=True)
        for regime, perf in sorted_perf:
            days = result.regime_days.get(regime, 0)
            if days > 0:
                logger.info(f"  {regime}: {perf:+.2f}% ({days}天)")
    
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--period", default="1y", choices=["3m", "6m", "1y", "2y", "3y"])
    args = parser.parse_args()
    
    quick_test(args.period)







































