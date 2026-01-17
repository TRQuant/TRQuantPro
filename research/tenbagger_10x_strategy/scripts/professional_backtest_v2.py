#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Professional Backtest Strategy V2 - 专业回测策略V2
================================================

整合专业知识库：
1. 专业市场环境检测器（4因子评分）
2. 震荡市专用策略（均值回归）
3. 熊市专用策略（超跌反弹+极低仓位）
4. 智能策略切换算法
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
from research.tenbagger_10x_strategy.knowledge.market_regime_knowledge import (
    MarketRegime,
    ProfessionalRegimeDetector,
    REGIME_STRATEGY_MAP,
    VolatileMarketStrategy,
    BearMarketStrategy
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


class ProfessionalBacktestV2:
    """专业回测策略V2
    
    核心改进：
    1. 专业4因子市场环境检测
    2. 震荡市：均值回归策略
    3. 熊市：超跌反弹+极低仓位
    4. 智能切换：冷却期+确认机制
    """
    
    def __init__(self, initial_capital: float = 1_000_000):
        self._jq = None
        self.initial_capital = initial_capital
        
        # 专业检测器
        self.regime_detector = ProfessionalRegimeDetector()
        self.volatile_strategy = VolatileMarketStrategy()
        self.bear_strategy = BearMarketStrategy()
        
        # 状态
        self.current_regime = MarketRegime.VOLATILE
        self.regime_days = 0
        self.last_regime_change = None
        
        # 冷却期设置
        self.cooldown_days = 10  # 环境切换后10天冷却期
        self.confirm_days = 3    # 新环境需连续3天确认
        self._pending_regime = None
        self._pending_count = 0
        
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
        return stocks[:80]  # 沪深300前80只
    
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
            fields=['close', 'volume'],
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
                                          trade_date: str, day_idx: int) -> Tuple[MarketRegime, bool, Dict]:
        """带确认机制的市场环境检测"""
        if day_idx < 60:
            return MarketRegime.VOLATILE, False, {'total': 0}
        
        # 获取截止到当前日期的数据
        df_to_date = index_data[index_data.index <= trade_date]
        if len(df_to_date) < 60:
            return MarketRegime.VOLATILE, False, {'total': 0}
        
        prices = df_to_date['close']
        volumes = df_to_date['volume'] if 'volume' in df_to_date else None
        
        # 使用专业检测器
        detected_regime, score, details = self.regime_detector.detect_regime(prices, volumes)
        
        # 冷却期检查
        if self.regime_days < self.cooldown_days:
            self.regime_days += 1
            return self.current_regime, False, details
        
        # 确认机制
        if detected_regime != self.current_regime:
            if detected_regime == self._pending_regime:
                self._pending_count += 1
                if self._pending_count >= self.confirm_days:
                    # 确认切换
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
    
    def _get_strategy_params(self, regime: MarketRegime) -> Dict:
        """获取当前环境的策略参数"""
        return REGIME_STRATEGY_MAP.get(regime, REGIME_STRATEGY_MAP[MarketRegime.VOLATILE])
    
    def _score_stocks_momentum(self, data: Dict, trade_date: str) -> List[Tuple[str, float]]:
        """动量策略选股（牛市/复苏期）"""
        scores = []
        
        for stock, df in data['prices'].items():
            try:
                df_to_date = df[df.index <= trade_date]
                if len(df_to_date) < 20:
                    continue
                    
                closes = df_to_date['close']
                
                # 20日收益率
                ret20 = closes.iloc[-1] / closes.iloc[-20] - 1
                
                # 5日收益率
                ret5 = closes.iloc[-1] / closes.iloc[-5] - 1 if len(closes) >= 5 else 0
                
                # 趋势强度
                ma5 = closes.rolling(5).mean().iloc[-1]
                ma20 = closes.rolling(20).mean().iloc[-1]
                trend = 1 if ma5 > ma20 else -1
                
                # 综合得分：趋势向上的动量股
                if trend > 0 and ret20 > 0:
                    score = ret20 * 50 + ret5 * 30 + trend * 20
                    scores.append((stock, score * 100))
            except:
                pass
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:5]
    
    def _score_stocks_mean_reversion(self, data: Dict, trade_date: str) -> List[Tuple[str, float]]:
        """均值回归策略选股（震荡市）
        
        优化策略：
        1. 更严格的超跌条件
        2. 支撑位确认
        3. 成交量配合
        """
        scores = []
        
        for stock, df in data['prices'].items():
            try:
                df_to_date = df[df.index <= trade_date]
                if len(df_to_date) < 30:
                    continue
                    
                closes = df_to_date['close']
                volumes = df_to_date['volume'] if 'volume' in df_to_date else None
                
                ma20 = closes.rolling(20).mean().iloc[-1]
                ma10 = closes.rolling(10).mean().iloc[-1]
                current = closes.iloc[-1]
                deviation = (current - ma20) / ma20
                
                # 支撑位（20日最低）
                support = closes.rolling(20).min().iloc[-1]
                distance_to_support = (current - support) / support
                
                # RSI
                delta = closes.diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rs = gain / loss.replace(0, 1e-10)
                rsi = 100 - (100 / (1 + rs.iloc[-1]))
                
                # 成交量萎缩（说明抛压减少）
                vol_ratio = 1.0
                if volumes is not None:
                    vol_ma5 = volumes.rolling(5).mean().iloc[-1]
                    vol_ma20 = volumes.rolling(20).mean().iloc[-1]
                    vol_ratio = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1
                
                # 更严格的超跌反弹条件
                # 1. 价格接近支撑位（<3%）
                # 2. RSI极度超跌（<30）
                # 3. 成交量萎缩（量比<0.8）
                if distance_to_support < 0.03 and rsi < 30 and vol_ratio < 0.9:
                    score = (3 - distance_to_support * 100) + (30 - rsi) + (0.9 - vol_ratio) * 50
                    scores.append((stock, score))
                # 次选：明显偏离均值
                elif deviation < -0.06 and rsi < 35:
                    score = abs(deviation) * 80 + (35 - rsi) * 0.5
                    scores.append((stock, score))
            except:
                pass
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:2]  # 震荡市最多2只
    
    def _score_stocks_oversold(self, data: Dict, trade_date: str) -> List[Tuple[str, float]]:
        """超跌策略选股（熊市）"""
        scores = []
        
        for stock, df in data['prices'].items():
            try:
                df_to_date = df[df.index <= trade_date]
                if len(df_to_date) < 60:
                    continue
                    
                closes = df_to_date['close']
                
                # 60日高点回撤
                high_60 = closes.rolling(60).max().iloc[-1]
                current = closes.iloc[-1]
                drawdown = (high_60 - current) / high_60
                
                # RSI
                delta = closes.diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rs = gain / loss.replace(0, 1e-10)
                rsi = 100 - (100 / (1 + rs.iloc[-1]))
                
                # 超跌条件：跌幅>25%且RSI<30
                if drawdown > 0.25 and rsi < 30:
                    score = drawdown * 100 + (30 - rsi)
                    scores.append((stock, score))
            except:
                pass
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:2]  # 熊市最多2只
    
    def run_backtest(self, start_date: str, end_date: str) -> BacktestResult:
        """运行回测"""
        logger.info(f"开始专业回测V2: {start_date} 至 {end_date}")
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
        regime_returns = {r.value: [] for r in MarketRegime}
        regime_days_count = {r.value: 0 for r in MarketRegime}
        prev_value = self.initial_capital
        wins = 0
        total_sells = 0
        
        # 重置状态
        self.current_regime = MarketRegime.VOLATILE
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
                            logger.info(f"[{date}] {sell_reason} {stock} @{price:.2f}")
            
            # 仓位管理
            current_position_value = total_value - cash
            target_value = total_value * target_position
            
            # 熊市/派发期：强制减仓
            if regime in [MarketRegime.BEAR, MarketRegime.DISTRIBUTION]:
                if current_position_value > target_value:
                    # 卖出最弱的持仓
                    to_sell = []
                    for stock, (shares, cost, _) in positions.items():
                        if stock in data['prices']:
                            df = data['prices'][stock]
                            df_today = df[df.index <= date]
                            if len(df_today) > 0:
                                price = df_today['close'].iloc[-1]
                                pnl_pct = price / cost - 1
                                to_sell.append((stock, shares, cost, price, pnl_pct))
                    
                    # 按盈亏排序，先卖亏损的
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
                        logger.info(f"[{date}] 减仓({regime.value}) {stock} @{price:.2f} 盈亏{pnl_pct*100:.1f}%")
            
            # 选股和买入
            if i % params.get('rebalance_freq', 5) == 0 and len(positions) < max_stocks:
                # 根据环境选择策略
                if regime in [MarketRegime.BULL, MarketRegime.RECOVERY]:
                    candidates = self._score_stocks_momentum(data, date)
                    min_score = 100  # 牛市门槛低
                elif regime == MarketRegime.VOLATILE:
                    candidates = self._score_stocks_mean_reversion(data, date)
                    min_score = 20  # 震荡市门槛高，宁可空仓
                elif regime in [MarketRegime.BEAR, MarketRegime.DISTRIBUTION]:
                    candidates = self._score_stocks_oversold(data, date)
                    min_score = 40  # 熊市只做高确定性
                else:
                    candidates = []
                    min_score = 0
                
                # 过滤低分候选
                candidates = [(s, sc) for s, sc in candidates if sc >= min_score]
                
                # 震荡市特殊处理：信号不够强就空仓观望
                if regime == MarketRegime.VOLATILE and len(candidates) == 0:
                    # 如果没有好的机会，卖出现有持仓
                    if len(positions) > 0 and self.regime_days > 5:
                        for stock, (shares, cost, _) in list(positions.items()):
                            if stock in data['prices']:
                                df = data['prices'][stock]
                                df_today = df[df.index <= date]
                                if len(df_today) > 0:
                                    price = df_today['close'].iloc[-1]
                                    pnl_pct = price / cost - 1
                                    # 保本或小亏就卖
                                    if pnl_pct > -0.05:
                                        cash += price * shares
                                        del positions[stock]
                                        trades += 1
                                        total_sells += 1
                                        if pnl_pct > 0:
                                            wins += 1
                                        logger.info(f"[{date}] 观望清仓(VOLATILE) {stock} @{price:.2f} 盈亏{pnl_pct*100:.1f}%")
                
                # 买入
                for stock, score in candidates:
                    if stock in positions:
                        continue
                    if len(positions) >= max_stocks:
                        break
                    if stock not in data['prices']:
                        continue
                    
                    # 检查可用资金
                    available_for_buy = min(
                        cash * 0.8,
                        target_value - current_position_value
                    )
                    
                    if available_for_buy < total_value * 0.05:  # 少于5%不买
                        break
                    
                    df = data['prices'][stock]
                    df_today = df[df.index <= date]
                    if len(df_today) == 0:
                        continue
                    
                    price = df_today['close'].iloc[-1]
                    max_per_stock = total_value * 0.2  # 单股最多20%
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
            if i % 40 == 0 or changed:
                ret = (total_value / self.initial_capital - 1) * 100
                pos_pct = (total_value - cash) / total_value * 100
                logger.info(f"[{date}] 净值:{total_value:,.0f} 收益:{ret:.1f}% 仓位:{pos_pct:.0f}% 环境:{regime.value}")
        
        # 计算结果
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
    
    period_map = {
        "3m": 90, "6m": 180, "1y": 365, "2y": 730, "3y": 1095
    }
    
    days = period_map.get(period, 365)
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    start_dt = end_dt - timedelta(days=days)
    start_date = start_dt.strftime("%Y-%m-%d")
    
    logger.info(f"{'='*60}")
    logger.info(f"专业回测V2 - 周期: {period}")
    logger.info(f"时间范围: {start_date} 至 {end_date}")
    logger.info(f"{'='*60}")
    
    strategy = ProfessionalBacktestV2()
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
        for regime, perf in sorted(result.regime_performance.items()):
            days = result.regime_days.get(regime, 0)
            logger.info(f"  {regime}: {perf:.2f}% ({days}天)")
    
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--period", default="1y", choices=["3m", "6m", "1y", "2y", "3y"])
    args = parser.parse_args()
    
    quick_test(args.period)

