#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Professional Backtest Strategy V3 - A股专业回测策略V3
====================================================

整合A股市场环境知识库V2：
1. 10种细分市场环境
2. 牛市三阶段策略
3. 熊市两阶段策略
4. 震荡市三模式策略
5. 智能环境转换检测
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

# 导入A股知识库V2
from research.tenbagger_10x_strategy.knowledge.astock_regime_knowledge_v2 import (
    AStockRegime,
    ASTOCK_REGIME_STRATEGY,
    AStockRegimeDetectorV2,
    AStockBullStrategy,
    AStockBearStrategy,
    AStockVolatileStrategy
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


class ProfessionalBacktestV3:
    """A股专业回测策略V3"""
    
    def __init__(self, initial_capital: float = 1_000_000):
        self._jq = None
        self.initial_capital = initial_capital
        
        # A股专业检测器
        self.regime_detector = AStockRegimeDetectorV2()
        
        # A股专用策略
        self.bull_strategy = AStockBullStrategy()
        self.bear_strategy = AStockBearStrategy()
        self.volatile_strategy = AStockVolatileStrategy()
        
        # 状态追踪
        self.current_regime = AStockRegime.VOLATILE_RANGE
        self.regime_days = 0
        self._pending_regime = None
        self._pending_count = 0
        
        # 切换参数
        self.cooldown_days = 5  # 冷却期缩短到5天
        self.confirm_days = 2   # 确认天数缩短到2天
        
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
        return stocks[:100]  # 沪深300前100只
    
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
        
        # 指数数据
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
        
        return {
            'prices': price_data,
            'index': index_data,
            'stocks': list(price_data.keys())
        }
    
    def _detect_regime_with_confirmation(self, index_data: pd.DataFrame, 
                                          trade_date: str, day_idx: int) -> Tuple[AStockRegime, bool, Dict]:
        """带确认机制的A股市场环境检测"""
        if day_idx < 120:
            return AStockRegime.VOLATILE_RANGE, False, {'total': 0}
        
        df_to_date = index_data[index_data.index <= trade_date]
        if len(df_to_date) < 120:
            return AStockRegime.VOLATILE_RANGE, False, {'total': 0}
        
        prices = df_to_date['close']
        volumes = df_to_date['volume'] if 'volume' in df_to_date else None
        highs = df_to_date['high'] if 'high' in df_to_date else None
        lows = df_to_date['low'] if 'low' in df_to_date else None
        
        # 使用A股专业检测器
        detected_regime, score, details = self.regime_detector.detect_regime(prices, volumes, highs, lows)
        
        # 冷却期检查
        if self.regime_days < self.cooldown_days:
            self.regime_days += 1
            return self.current_regime, False, details
        
        # 确认机制
        if detected_regime != self.current_regime:
            # 同类环境可以快速切换（如BULL_EARLY -> BULL_MID）
            same_category = self._is_same_category(detected_regime, self.current_regime)
            
            if detected_regime == self._pending_regime:
                self._pending_count += 1
                required_confirms = 1 if same_category else self.confirm_days
                
                if self._pending_count >= required_confirms:
                    old_regime = self.current_regime
                    self.current_regime = detected_regime
                    self.regime_days = 0
                    self._pending_regime = None
                    self._pending_count = 0
                    logger.info(f"[{trade_date}] 环境切换: {old_regime.value} → {detected_regime.value} (分数:{score:.1f})")
                    return self.current_regime, True, details
            else:
                self._pending_regime = detected_regime
                self._pending_count = 1
        else:
            self._pending_regime = None
            self._pending_count = 0
        
        self.regime_days += 1
        return self.current_regime, False, details
    
    def _is_same_category(self, regime1: AStockRegime, regime2: AStockRegime) -> bool:
        """判断是否同类环境"""
        bull_regimes = {AStockRegime.BULL_EARLY, AStockRegime.BULL_MID, AStockRegime.BULL_LATE}
        bear_regimes = {AStockRegime.BEAR_PANIC, AStockRegime.BEAR_GRINDING}
        volatile_regimes = {AStockRegime.VOLATILE_UP, AStockRegime.VOLATILE_DOWN, AStockRegime.VOLATILE_RANGE}
        
        for category in [bull_regimes, bear_regimes, volatile_regimes]:
            if regime1 in category and regime2 in category:
                return True
        return False
    
    def _get_strategy_params(self, regime: AStockRegime) -> Dict:
        """获取策略参数"""
        return ASTOCK_REGIME_STRATEGY.get(regime, ASTOCK_REGIME_STRATEGY[AStockRegime.VOLATILE_RANGE])
    
    def _select_stocks(self, data: Dict, regime: AStockRegime, date: str) -> List[Tuple[str, float]]:
        """根据环境选股"""
        if regime in [AStockRegime.BULL_EARLY, AStockRegime.BULL_MID, AStockRegime.BULL_LATE]:
            return self.bull_strategy.select_stocks(data['prices'], regime, date)
        elif regime in [AStockRegime.BEAR_PANIC, AStockRegime.BEAR_GRINDING]:
            if self.bear_strategy.should_stay_cash(regime):
                return []
            return self.bear_strategy.select_stocks(data['prices'], date)
        elif regime in [AStockRegime.VOLATILE_UP, AStockRegime.VOLATILE_DOWN, AStockRegime.VOLATILE_RANGE]:
            return self.volatile_strategy.select_stocks(data['prices'], regime, date)
        else:
            return []
    
    def run_backtest(self, start_date: str, end_date: str) -> BacktestResult:
        """运行回测"""
        logger.info(f"开始A股专业回测V3: {start_date} 至 {end_date}")
        start_time = time.time()
        
        self._ensure_jqdata()
        jq = self._jq
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [d.strftime("%Y-%m-%d") if hasattr(d, 'strftime') else str(d) for d in trade_days]
        
        # 获取股票池和数据
        stocks = self._get_universe(start_date)
        data = self._preload_data(start_date, end_date, stocks)
        
        if not data['prices']:
            logger.error("没有可用的价格数据")
            return BacktestResult(0, 0, 0, 0, 0, 0, 0)
        
        # 初始化
        cash = self.initial_capital
        positions = {}  # {stock: (shares, cost, entry_date)}
        equity_history = []
        trades = 0
        regime_returns = {r.value: [] for r in AStockRegime}
        regime_days_count = {r.value: 0 for r in AStockRegime}
        prev_value = self.initial_capital
        wins = 0
        total_sells = 0
        
        # 重置状态
        self.current_regime = AStockRegime.VOLATILE_RANGE
        self.regime_days = 0
        self._pending_regime = None
        self._pending_count = 0
        
        # 逐日回测
        for i, date in enumerate(trade_days):
            # 检测市场环境
            regime, changed, details = self._detect_regime_with_confirmation(data['index'], date, i)
            regime_days_count[regime.value] += 1
            
            # 获取策略参数
            params = self._get_strategy_params(regime)
            target_position = params['position']
            stop_loss = params['stop_loss']
            take_profit = params['take_profit']
            max_stocks = params['max_stocks']
            rebalance_freq = params['rebalance_freq']
            
            # 计算当前持仓市值
            total_value = cash
            for stock, (shares, cost, entry_date) in list(positions.items()):
                if stock in data['prices']:
                    df = data['prices'][stock]
                    df_today = df[df.index <= date]
                    if len(df_today) > 0:
                        price = df_today['close'].iloc[-1]
                        total_value += price * shares
                        
                        # 止损止盈检查
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
                            logger.debug(f"[{date}] {sell_reason} {stock} @{price:.2f}")
            
            # 仓位管理
            current_position_value = total_value - cash
            target_value = total_value * target_position
            
            # 熊市恐慌期：强制清仓
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
                            logger.info(f"[{date}] 恐慌清仓 {stock} @{price:.2f} 盈亏{pnl_pct*100:.1f}%")
            
            # 其他熊市/震荡向下：减仓到目标
            elif regime in [AStockRegime.BEAR_GRINDING, AStockRegime.VOLATILE_DOWN, AStockRegime.BULL_LATE]:
                if current_position_value > target_value * 1.1:  # 超过目标10%才减
                    to_sell = []
                    for stock, (shares, cost, _) in positions.items():
                        if stock in data['prices']:
                            df = data['prices'][stock]
                            df_today = df[df.index <= date]
                            if len(df_today) > 0:
                                price = df_today['close'].iloc[-1]
                                pnl_pct = price / cost - 1
                                to_sell.append((stock, shares, cost, price, pnl_pct))
                    
                    to_sell.sort(key=lambda x: x[4])  # 先卖亏损的
                    
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
                        logger.info(f"[{date}] 减仓({regime.value}) {stock} @{price:.2f} 盈亏{pnl_pct*100:.1f}%")
            
            # 选股和买入
            if i % rebalance_freq == 0 and len(positions) < max_stocks and regime != AStockRegime.BEAR_PANIC:
                candidates = self._select_stocks(data, regime, date)
                
                # 最低得分门槛
                min_score = 20 if regime.value.startswith('VOLATILE') else 10
                candidates = [(s, sc) for s, sc in candidates if sc >= min_score]
                
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
                    max_per_stock = total_value * 0.25  # 单股最多25%
                    shares = int(min(max_per_stock, available_for_buy) / price / 100) * 100
                    
                    if shares >= 100:
                        cost = price * shares
                        cash -= cost
                        current_position_value += cost
                        positions[stock] = (shares, price, date)
                        trades += 1
                        logger.info(f"[{date}] 买入({regime.value}) {stock} @{price:.2f} x{shares} 得分:{score:.1f}")
            
            # 记录
            equity_history.append((date, total_value))
            daily_ret = total_value / prev_value - 1 if prev_value > 0 else 0
            regime_returns[regime.value].append(daily_ret)
            prev_value = total_value
            
            # 进度
            if i % 50 == 0 or changed:
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
    logger.info(f"A股专业回测V3 - 周期: {period}")
    logger.info(f"时间范围: {start_date} 至 {end_date}")
    logger.info(f"{'='*60}")
    
    strategy = ProfessionalBacktestV3()
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
        # 按收益排序显示
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







































