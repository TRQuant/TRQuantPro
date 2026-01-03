#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fast Backtest Strategy - 高速回测策略
=====================================

优化措施：
1. 批量获取数据，减少API调用
2. 预加载所有需要的数据
3. 内存中计算，避免重复查询
4. 简化选股逻辑，使用技术指标

目标：将回测速度从281秒/月提升到<10秒/月
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


class FastBacktestStrategy:
    """高速向量化回测策略"""
    
    def __init__(self, initial_capital: float = 1_000_000):
        self._jq = None
        self.initial_capital = initial_capital
        self.params = {
            'max_stocks': 5,
            'rebalance_freq': 5,  # 每5天调仓一次
            'stop_loss': 0.12,
            'take_profit': 0.50,
            'min_market_cap': 30e8,
            'max_market_cap': 1000e8,
        }
        
        # 缓存
        self._price_cache = {}
        self._trade_days_cache = None
        
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
        """获取股票池（简化版）"""
        self._ensure_jqdata()
        jq = self._jq
        
        # 使用沪深300成分股作为基础池
        stocks = jq.get_index_stocks('000300.XSHG', date=date)
        return stocks[:50]  # 限制为50只加速
    
    def _preload_data(self, start_date: str, end_date: str, stocks: List[str]) -> Dict:
        """预加载所有数据"""
        self._ensure_jqdata()
        jq = self._jq
        
        logger.info(f"预加载数据: {len(stocks)}只股票, {start_date} 至 {end_date}")
        start_time = time.time()
        
        # 批量获取价格数据
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
        
        # 获取指数数据（用于市场环境判断）
        index_data = jq.get_price(
            '000300.XSHG',
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['close'],
            skip_paused=True
        )
        
        elapsed = time.time() - start_time
        logger.info(f"数据预加载完成: {len(price_data)}只股票, 耗时{elapsed:.1f}秒")
        
        return {
            'prices': price_data,
            'index': index_data,
            'stocks': list(price_data.keys())
        }
    
    def _detect_regime(self, index_data: pd.DataFrame, date_idx: int) -> str:
        """基于指数判断市场环境（快速版）"""
        if date_idx < 20:
            return "VOLATILE"
        
        closes = index_data['close'].iloc[:date_idx+1]
        
        # 计算技术指标
        ma5 = closes.rolling(5).mean().iloc[-1]
        ma20 = closes.rolling(20).mean().iloc[-1]
        current = closes.iloc[-1]
        
        # 简单判断
        if current > ma5 > ma20:
            return "BULL"
        elif current < ma5 < ma20:
            return "BEAR"
        else:
            return "VOLATILE"
    
    def _score_stocks(self, data: Dict, trade_date: str) -> List[Tuple[str, float]]:
        """快速评分（基于动量）"""
        scores = []
        
        for stock, df in data['prices'].items():
            try:
                # 获取截止到当前日期的数据
                df_to_date = df[df.index <= trade_date]
                if len(df_to_date) < 20:
                    continue
                    
                closes = df_to_date['close']
                
                # 20日收益率
                ret20 = closes.iloc[-1] / closes.iloc[-20] - 1
                
                # 5日收益率
                ret5 = closes.iloc[-1] / closes.iloc[-5] - 1 if len(closes) >= 5 else 0
                
                # 波动率
                vol = closes.pct_change().std()
                
                # 综合得分
                score = ret20 * 0.5 + ret5 * 0.3 - vol * 0.2
                
                if score > -0.1:  # 放宽条件
                    scores.append((stock, score * 100))
            except Exception as e:
                pass
        
        # 按得分排序
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:self.params['max_stocks']]
    
    def run_backtest(self, start_date: str, end_date: str) -> BacktestResult:
        """运行快速回测"""
        logger.info(f"开始快速回测: {start_date} 至 {end_date}")
        start_time = time.time()
        
        self._ensure_jqdata()
        jq = self._jq
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [d.strftime("%Y-%m-%d") if hasattr(d, 'strftime') else str(d) for d in trade_days]
        
        # 获取股票池
        stocks = self._get_universe(start_date)
        
        # 预加载数据
        data = self._preload_data(start_date, end_date, stocks)
        
        if not data['prices']:
            logger.error("没有可用的价格数据")
            return BacktestResult(0, 0, 0, 0, 0, 0, 0)
        
        # 初始化
        cash = self.initial_capital
        positions = {}  # {stock: (shares, cost)}
        equity_history = []
        trades = 0
        regime_returns = {'BULL': [], 'BEAR': [], 'VOLATILE': []}
        prev_value = self.initial_capital
        wins = 0
        total_sells = 0
        
        # 逐日回测
        for i, date in enumerate(trade_days):
            # 市场环境
            if i < len(data['index']):
                regime = self._detect_regime(data['index'], i)
            else:
                regime = "VOLATILE"
            
            # 计算当前持仓市值
            total_value = cash
            for stock, (shares, cost) in list(positions.items()):
                if stock in data['prices']:
                    df = data['prices'][stock]
                    df_today = df[df.index <= date]
                    if len(df_today) > 0:
                        price = df_today['close'].iloc[-1]
                        total_value += price * shares
                        
                        # 止损止盈检查
                        pnl_pct = price / cost - 1
                        if pnl_pct < -self.params['stop_loss'] or pnl_pct > self.params['take_profit']:
                            cash += price * shares
                            del positions[stock]
                            trades += 1
                            total_sells += 1
                            if pnl_pct > 0:
                                wins += 1
            
            # 熊市减仓逻辑
            if regime == "BEAR":
                # 熊市：减仓到20%以下
                target_value = self.initial_capital * 0.2
                current_position_value = total_value - cash
                if current_position_value > target_value:
                    # 卖出最弱的股票
                    for stock, (shares, cost) in sorted(
                        positions.items(), 
                        key=lambda x: data['prices'].get(x[0], pd.DataFrame()).get('close', pd.Series([x[1][1]])).iloc[-1] / x[1][1] - 1
                    ):
                        if current_position_value <= target_value:
                            break
                        if stock in data['prices']:
                            df = data['prices'][stock]
                            df_today = df[df.index <= date]
                            if len(df_today) > 0:
                                price = df_today['close'].iloc[-1]
                                cash += price * shares
                                pnl_pct = price / cost - 1
                                current_position_value -= price * shares
                                del positions[stock]
                                trades += 1
                                total_sells += 1
                                if pnl_pct > 0:
                                    wins += 1
                                logger.info(f"[{date}] 熊市减仓 卖出 {stock} @{price:.2f}")
            
            # 定期调仓
            if i % self.params['rebalance_freq'] == 0 and regime != "BEAR":
                candidates = self._score_stocks(data, date)
                
                # 买入新股
                for stock, score in candidates:
                    if stock in positions:
                        continue
                    if len(positions) >= self.params['max_stocks']:
                        break
                    if stock not in data['prices']:
                        continue
                    
                    df = data['prices'][stock]
                    df_today = df[df.index <= date]
                    if len(df_today) == 0:
                        continue
                    
                    price = df_today['close'].iloc[-1]
                    max_amt = total_value * 0.2  # 单股20%
                    shares = int(min(max_amt, cash * 0.8) / price / 100) * 100
                    
                    if shares >= 100 and cash >= price * shares:
                        cost = price * shares
                        cash -= cost
                        positions[stock] = (shares, price)
                        trades += 1
                        logger.info(f"[{date}] 买入 {stock} @{price:.2f} x{shares} 得分:{score:.1f}")
            
            # 记录
            equity_history.append((date, total_value))
            daily_ret = total_value / prev_value - 1 if prev_value > 0 else 0
            regime_returns[regime].append(daily_ret)
            prev_value = total_value
            
            # 进度
            if i % 20 == 0:
                ret = (total_value / self.initial_capital - 1) * 100
                logger.info(f"[{date}] 净值:{total_value:,.0f} 收益:{ret:.1f}% 环境:{regime}")
        
        # 计算结果
        elapsed = time.time() - start_time
        logger.info(f"回测完成，耗时: {elapsed:.1f}秒")
        
        values = [x[1] for x in equity_history]
        if not values:
            return BacktestResult(0, 0, 0, 0, 0, 0, 0)
        
        total_ret = (values[-1] / self.initial_capital - 1) * 100
        years = max(len(values) / 252, 0.01)
        annual_ret = ((values[-1] / self.initial_capital) ** (1/years) - 1) * 100
        
        # 夏普
        returns = pd.Series(values).pct_change().dropna()
        sharpe = np.sqrt(252) * returns.mean() / returns.std() if len(returns) > 0 and returns.std() > 0 else 0
        
        # 最大回撤
        cummax = pd.Series(values).cummax()
        drawdown = (cummax - pd.Series(values)) / cummax
        max_dd = drawdown.max() * 100
        
        # 胜率
        win_rate = wins / total_sells * 100 if total_sells > 0 else 0
        
        # 环境表现
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
            regime_performance=regime_perf
        )


def quick_test(period: str = "1m"):
    """快速测试"""
    end_date = "2024-06-30"
    
    period_map = {
        "1m": 30, "3m": 90, "6m": 180, "1y": 365, "2y": 730, "3y": 1095
    }
    
    days = period_map.get(period, 30)
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    start_dt = end_dt - timedelta(days=days)
    start_date = start_dt.strftime("%Y-%m-%d")
    
    logger.info(f"{'='*60}")
    logger.info(f"快速回测 - 周期: {period}")
    logger.info(f"时间范围: {start_date} 至 {end_date}")
    logger.info(f"{'='*60}")
    
    strategy = FastBacktestStrategy()
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
        for regime, perf in result.regime_performance.items():
            logger.info(f"  {regime}: {perf:.2f}%")
    
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--period", default="1m", choices=["1m", "3m", "6m", "1y", "2y", "3y"])
    args = parser.parse_args()
    
    quick_test(args.period)

