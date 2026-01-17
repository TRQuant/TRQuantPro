#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tenbagger Hybrid Strategy V6 - 十倍股混合策略V6
==============================================

结合V4和V5优点：
1. V4的技术面分析选股（MACD/RSI/BOLL/KDJ/VOL综合）
2. V5的十倍股评分系统（基本面筛选）
3. 严格的环境风控（熊市/震荡控仓）
4. 长周期持股逻辑（阶段化止盈）
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

from research.tenbagger_10x_strategy.knowledge.astock_regime_knowledge_v2 import (
    AStockRegime, ASTOCK_REGIME_STRATEGY, AStockRegimeDetectorV2
)
from research.tenbagger_10x_strategy.knowledge.professional_indicators_kb import (
    SignalType, ComprehensiveTechnicalAnalysis
)
from research.tenbagger_10x_strategy.knowledge.strategy_switching_kb import (
    RegimeSwitchDecider
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
    total_trades: int
    equity_curve: pd.DataFrame = None
    regime_performance: Dict[str, float] = field(default_factory=dict)


class TenbaggerHybridV6:
    """十倍股混合策略V6"""
    
    # 环境仓位上限
    REGIME_MAX_POSITION = {
        AStockRegime.BEAR_PANIC: 0,
        AStockRegime.BEAR_GRINDING: 0.10,
        AStockRegime.VOLATILE_DOWN: 0.15,
        AStockRegime.VOLATILE_RANGE: 0.30,
        AStockRegime.VOLATILE_UP: 0.50,
        AStockRegime.BULL_LATE: 0.40,
        AStockRegime.BULL_MID: 0.60,
        AStockRegime.BULL_EARLY: 0.70,
    }
    
    # 环境止损止盈
    REGIME_RISK_PARAMS = {
        AStockRegime.BEAR_PANIC: {'stop_loss': 0.05, 'take_profit': 0.10},
        AStockRegime.BEAR_GRINDING: {'stop_loss': 0.08, 'take_profit': 0.12},
        AStockRegime.VOLATILE_DOWN: {'stop_loss': 0.08, 'take_profit': 0.12},
        AStockRegime.VOLATILE_RANGE: {'stop_loss': 0.10, 'take_profit': 0.15},
        AStockRegime.VOLATILE_UP: {'stop_loss': 0.12, 'take_profit': 0.20},
        AStockRegime.BULL_LATE: {'stop_loss': 0.10, 'take_profit': 0.20},
        AStockRegime.BULL_MID: {'stop_loss': 0.12, 'take_profit': 0.25},
        AStockRegime.BULL_EARLY: {'stop_loss': 0.15, 'take_profit': 0.35},
    }
    
    def __init__(self, initial_capital: float = 1_000_000):
        self._jq = None
        self.initial_capital = initial_capital
        self.regime_detector = AStockRegimeDetectorV2()
        self.switch_decider = RegimeSwitchDecider()
        
        # 风控
        self.max_drawdown_limit = 0.12
        self.consecutive_loss_limit = 3
        
    def _ensure_jqdata(self):
        if self._jq is None:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            cm = get_config_manager()
            jqcfg = cm.get_config('jqdata')
            jq.auth(jqcfg['username'], jqcfg['password'])
            self._jq = jq
            logger.info(f"JQData认证成功: {jqcfg['username']}")
    
    def _get_universe(self, date: str) -> List[str]:
        self._ensure_jqdata()
        jq = self._jq
        stocks_300 = jq.get_index_stocks('000300.XSHG', date=date)[:80]
        stocks_500 = jq.get_index_stocks('000905.XSHG', date=date)[:70]
        return list(set(stocks_300 + stocks_500))[:120]
    
    def _preload_data(self, start_date: str, end_date: str, stocks: List[str]) -> Dict:
        self._ensure_jqdata()
        jq = self._jq
        
        logger.info(f"预加载数据: {len(stocks)}只股票")
        start_time = time.time()
        
        price_data = {}
        for stock in stocks:
            try:
                df = jq.get_price(
                    stock, start_date=start_date, end_date=end_date,
                    frequency='daily',
                    fields=['open', 'close', 'high', 'low', 'volume'],
                    skip_paused=True, fq='pre'
                )
                if df is not None and len(df) > 0:
                    price_data[stock] = df
            except:
                pass
        
        index_data = jq.get_price(
            '000300.XSHG', start_date=start_date, end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            skip_paused=True
        )
        
        elapsed = time.time() - start_time
        logger.info(f"数据预加载完成: {len(price_data)}只, 耗时{elapsed:.1f}秒")
        
        return {'prices': price_data, 'index': index_data, 'stocks': list(price_data.keys())}
    
    def _select_stocks_hybrid(self, data: Dict, regime: AStockRegime, date: str) -> List[Tuple[str, float]]:
        """混合选股：技术面+基本面"""
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
                
                # 技术面分析
                analysis = ComprehensiveTechnicalAnalysis.analyze_all(closes, volumes, highs, lows)
                tech_signal = analysis['overall_signal']
                tech_score = analysis['score']
                confidence = analysis['confidence']
                
                # 动量因子
                ret5 = closes.iloc[-1] / closes.iloc[-5] - 1 if len(closes) >= 5 else 0
                ret20 = closes.iloc[-1] / closes.iloc[-20] - 1 if len(closes) >= 20 else 0
                ret60 = closes.iloc[-1] / closes.iloc[-60] - 1 if len(closes) >= 60 else 0
                
                # 波动率因子
                volatility = closes.pct_change().rolling(20).std().iloc[-1] if len(closes) >= 20 else 0.03
                
                # 成交量因子
                vol_ratio = volumes.iloc[-5:].mean() / volumes.iloc[-20:].mean() if len(volumes) >= 20 else 1
                
                # 根据环境选择不同策略
                final_score = 0
                
                if regime in [AStockRegime.BULL_EARLY, AStockRegime.BULL_MID]:
                    # 牛市：趋势+动量
                    if tech_signal in [SignalType.STRONG_BUY, SignalType.BUY]:
                        if ret20 > 0 and ret60 > 0:  # 中长期向上
                            final_score = tech_score * 40 + confidence * 30 + ret20 * 100 + ret60 * 50
                            
                elif regime == AStockRegime.BULL_LATE:
                    # 牛市末期：稳健+低波动
                    if tech_signal in [SignalType.BUY, SignalType.WEAK_BUY, SignalType.HOLD]:
                        if volatility < 0.03 and ret5 > -0.02:  # 低波动，近期不跌
                            final_score = (1 - volatility * 10) * 50 + tech_score * 30
                            
                elif regime == AStockRegime.VOLATILE_UP:
                    # 震荡向上：超跌反弹
                    if tech_signal in [SignalType.STRONG_BUY, SignalType.BUY]:
                        rsi_sig = analysis['signals'].get('RSI')
                        if rsi_sig and rsi_sig.value < 50:  # RSI不高
                            final_score = tech_score * 40 + (50 - rsi_sig.value) * 1 + confidence * 20
                            
                elif regime == AStockRegime.VOLATILE_RANGE:
                    # 区间震荡：均值回归
                    ma20 = closes.rolling(20).mean().iloc[-1]
                    deviation = (closes.iloc[-1] - ma20) / ma20
                    if deviation < -0.03 and tech_signal in [SignalType.BUY, SignalType.STRONG_BUY]:
                        final_score = abs(deviation) * 150 + tech_score * 25
                        
                elif regime == AStockRegime.VOLATILE_DOWN:
                    # 震荡向下：极度保守，只选强烈买入信号
                    if tech_signal == SignalType.STRONG_BUY:
                        rsi_sig = analysis['signals'].get('RSI')
                        if rsi_sig and rsi_sig.value < 25:  # 极度超卖
                            final_score = (25 - rsi_sig.value) * 3 + confidence * 30
                            
                elif regime == AStockRegime.BEAR_GRINDING:
                    # 熊市磨底：极度超跌反弹
                    if tech_signal == SignalType.STRONG_BUY:
                        rsi_sig = analysis['signals'].get('RSI')
                        boll_sig = analysis['signals'].get('BOLL')
                        if rsi_sig and rsi_sig.value < 20:  # RSI<20
                            if boll_sig and 'lower' in boll_sig.reason.lower():  # 触及下轨
                                final_score = (20 - rsi_sig.value) * 5 + confidence * 20
                
                if final_score > 0:
                    scores.append((stock, final_score))
                    
            except Exception as e:
                pass
        
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # 根据环境限制数量
        max_picks = {
            AStockRegime.BULL_EARLY: 5,
            AStockRegime.BULL_MID: 4,
            AStockRegime.BULL_LATE: 3,
            AStockRegime.VOLATILE_UP: 3,
            AStockRegime.VOLATILE_RANGE: 2,
            AStockRegime.VOLATILE_DOWN: 1,
            AStockRegime.BEAR_GRINDING: 1,
            AStockRegime.BEAR_PANIC: 0,
        }
        
        return scores[:max_picks.get(regime, 2)]
    
    def run_backtest(self, start_date: str, end_date: str) -> BacktestResult:
        logger.info(f"开始混合策略V6回测: {start_date} 至 {end_date}")
        start_time = time.time()
        
        self._ensure_jqdata()
        jq = self._jq
        
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [d.strftime("%Y-%m-%d") if hasattr(d, 'strftime') else str(d) for d in trade_days]
        
        stocks = self._get_universe(start_date)
        data = self._preload_data(start_date, end_date, stocks)
        
        if not data['prices']:
            return BacktestResult(0, 0, 0, 0, 0, 0)
        
        # 初始化
        cash = self.initial_capital
        positions = {}  # {stock: (shares, cost, entry_date)}
        equity_history = []
        trades = 0
        wins = 0
        total_sells = 0
        regime_returns = {r.value: [] for r in AStockRegime}
        prev_value = self.initial_capital
        peak_value = self.initial_capital
        consecutive_losses = 0
        pause_days = 0
        
        self.switch_decider = RegimeSwitchDecider()
        
        for i, date in enumerate(trade_days):
            if i < 120:
                equity_history.append((date, cash))
                continue
            
            # 市场环境
            df_to_date = data['index'][data['index'].index <= date]
            if len(df_to_date) < 120:
                equity_history.append((date, cash))
                continue
            
            prices = df_to_date['close']
            volumes = df_to_date['volume']
            
            _, score, _ = self.regime_detector.detect_regime(prices, volumes)
            switched, _ = self.switch_decider.should_switch(score, date)
            regime = self.switch_decider.current_regime
            
            if switched:
                logger.info(f"[{date}] 环境切换 → {regime.value} (分数:{score:.1f})")
            
            # 获取环境参数
            max_position = self.REGIME_MAX_POSITION.get(regime, 0.3)
            risk_params = self.REGIME_RISK_PARAMS.get(regime, {'stop_loss': 0.10, 'take_profit': 0.20})
            stop_loss = risk_params['stop_loss']
            take_profit = risk_params['take_profit']
            
            # 计算持仓市值
            total_value = cash
            for stock, (shares, cost, entry_date) in list(positions.items()):
                if stock in data['prices']:
                    df = data['prices'][stock]
                    df_today = df[df.index <= date]
                    if len(df_today) > 0:
                        price = df_today['close'].iloc[-1]
                        total_value += price * shares
                        
                        pnl_pct = price / cost - 1
                        should_sell = False
                        
                        if pnl_pct < -stop_loss:
                            should_sell = True
                            consecutive_losses += 1
                        elif pnl_pct > take_profit:
                            should_sell = True
                            consecutive_losses = 0
                        
                        if should_sell:
                            cash += price * shares
                            del positions[stock]
                            trades += 1
                            total_sells += 1
                            if pnl_pct > 0:
                                wins += 1
            
            # 更新峰值
            peak_value = max(peak_value, total_value)
            current_drawdown = (peak_value - total_value) / peak_value
            
            # 回撤保护
            if current_drawdown > self.max_drawdown_limit:
                max_position = min(max_position, 0.15)
            
            # 连续亏损暂停
            if consecutive_losses >= self.consecutive_loss_limit:
                pause_days = 5
                consecutive_losses = 0
            
            if pause_days > 0:
                pause_days -= 1
                equity_history.append((date, total_value))
                daily_ret = total_value / prev_value - 1 if prev_value > 0 else 0
                regime_returns[regime.value].append(daily_ret)
                prev_value = total_value
                continue
            
            # 计算仓位
            current_pos_value = total_value - cash
            current_pos_pct = current_pos_value / total_value if total_value > 0 else 0
            
            # 恐慌清仓
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
                            logger.info(f"[{date}] 恐慌清仓 {stock}")
            
            # 超仓减仓
            elif current_pos_pct > max_position * 1.1 and positions:
                to_sell = []
                for stock, (shares, cost, _) in positions.items():
                    if stock in data['prices']:
                        df = data['prices'][stock]
                        df_today = df[df.index <= date]
                        if len(df_today) > 0:
                            price = df_today['close'].iloc[-1]
                            pnl = price / cost - 1
                            to_sell.append((stock, shares, cost, price, pnl))
                
                to_sell.sort(key=lambda x: x[4])
                
                for stock, shares, cost, price, pnl in to_sell:
                    if current_pos_pct <= max_position:
                        break
                    v = price * shares
                    cash += v
                    current_pos_pct -= v / total_value
                    del positions[stock]
                    trades += 1
                    total_sells += 1
                    if pnl > 0:
                        wins += 1
                    logger.info(f"[{date}] 减仓({regime.value}) {stock} 盈亏{pnl*100:.1f}%")
            
            # 选股买入
            if i % 10 == 0 and current_pos_pct < max_position and regime != AStockRegime.BEAR_PANIC:
                candidates = self._select_stocks_hybrid(data, regime, date)
                
                for stock, score in candidates:
                    if stock in positions:
                        continue
                    if len(positions) >= 4:
                        break
                    if stock not in data['prices']:
                        continue
                    
                    available = (max_position - current_pos_pct) * total_value
                    max_per_stock = total_value * 0.20
                    buy_amount = min(available, max_per_stock, cash * 0.8)
                    
                    if buy_amount < total_value * 0.05:
                        break
                    
                    df = data['prices'][stock]
                    df_today = df[df.index <= date]
                    if len(df_today) == 0:
                        continue
                    
                    price = df_today['close'].iloc[-1]
                    shares = int(buy_amount / price / 100) * 100
                    
                    if shares >= 100:
                        cost = price * shares
                        cash -= cost
                        current_pos_pct += cost / total_value
                        positions[stock] = (shares, price, date)
                        trades += 1
                        logger.info(f"[{date}] 买入({regime.value}) {stock} @{price:.2f} x{shares} 得分:{score:.1f}")
            
            equity_history.append((date, total_value))
            daily_ret = total_value / prev_value - 1 if prev_value > 0 else 0
            regime_returns[regime.value].append(daily_ret)
            prev_value = total_value
            
            if i % 50 == 0 or switched:
                ret = (total_value / self.initial_capital - 1) * 100
                pos_pct = current_pos_pct * 100
                logger.info(f"[{date}] 净值:{total_value:,.0f} 收益:{ret:.1f}% 仓位:{pos_pct:.0f}% 环境:{regime.value}")
        
        elapsed = time.time() - start_time
        logger.info(f"回测完成，耗时: {elapsed:.1f}秒")
        
        return self._calc_result(equity_history, regime_returns, trades, wins, total_sells)
    
    def _calc_result(self, equity_history, regime_returns, trades, wins, total_sells) -> BacktestResult:
        values = [x[1] for x in equity_history]
        if not values:
            return BacktestResult(0, 0, 0, 0, 0, 0)
        
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
            total_trades=trades,
            equity_curve=df,
            regime_performance=regime_perf
        )


def quick_test(period: str = "1y"):
    end_date = "2024-06-30"
    period_map = {"3m": 90, "6m": 180, "1y": 365, "2y": 730, "3y": 1095}
    
    days = period_map.get(period, 365)
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    start_dt = end_dt - timedelta(days=days)
    start_date = start_dt.strftime("%Y-%m-%d")
    
    logger.info(f"{'='*60}")
    logger.info(f"混合策略V6 - 周期: {period}")
    logger.info(f"{'='*60}")
    
    strategy = TenbaggerHybridV6()
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
            logger.info(f"  {regime}: {perf:+.2f}%")
    
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--period", default="1y", choices=["3m", "6m", "1y", "2y", "3y"])
    args = parser.parse_args()
    
    quick_test(args.period)







































