#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tenbagger Strategy V5 - 十倍股策略V5
====================================

核心目标：识别十倍股，长周期好收益

整合：
1. 十倍股识别系统（基本面+成长+估值+技术）
2. 市场环境判断（牛熊震荡10种细分）
3. 阶段化持仓策略（S0-S5）
4. 动态风控（止损止盈+仓位管理）
5. 长周期优化（季度调仓+趋势跟踪）
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
    AStockRegime, ASTOCK_REGIME_STRATEGY, AStockRegimeDetectorV2
)
from research.tenbagger_10x_strategy.knowledge.tenbagger_identification_kb import (
    TenbaggerStage, TenbaggerIdentifier, STAGE_POSITION_STRATEGY,
    TenbaggerCriteria
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
    stage_performance: Dict[str, float] = field(default_factory=dict)


class TenbaggerStrategyV5:
    """十倍股策略V5 - 长周期优化版"""
    
    def __init__(self, initial_capital: float = 1_000_000):
        self._jq = None
        self.initial_capital = initial_capital
        
        # 核心组件
        self.regime_detector = AStockRegimeDetectorV2()
        self.switch_decider = RegimeSwitchDecider()
        self.tenbagger_identifier = TenbaggerIdentifier()
        
        # 风控参数
        self.max_drawdown_limit = 0.15
        self.max_single_position = 0.25
        self.min_position_per_stock = 0.05
        
        # 长周期参数
        self.rebalance_interval = 10  # 双周调仓
        self.min_hold_days = 3  # 最短持有天数
        
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
    
    def _get_fundamentals(self, stocks: List[str], date: str) -> Dict[str, Dict]:
        """获取基本面数据"""
        self._ensure_jqdata()
        jq = self._jq
        
        try:
            q = jq.query(
                jq.valuation.code,
                jq.valuation.market_cap,  # 市值(亿)
                jq.valuation.pe_ratio,     # PE
                jq.indicator.roe,          # ROE
                jq.indicator.gross_profit_margin,  # 毛利率
                jq.indicator.net_profit_margin,    # 净利率
                jq.balance.total_liability / jq.balance.total_assets,  # 负债率
                jq.income.operating_revenue,  # 营收
                jq.income.net_profit,         # 净利润
            ).filter(
                jq.valuation.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            result = {}
            if df is not None and len(df) > 0:
                for _, row in df.iterrows():
                    code = row['code']
                    result[code] = {
                        'market_cap': row.get('market_cap', 0),
                        'pe': row.get('pe_ratio', 0),
                        'roe': row.get('roe', 0) / 100 if row.get('roe') else 0,
                        'gross_margin': row.get('gross_profit_margin', 0) / 100 if row.get('gross_profit_margin') else 0,
                        'net_margin': row.get('net_profit_margin', 0) / 100 if row.get('net_profit_margin') else 0,
                        'debt_ratio': 0.5,  # 默认值
                        'revenue': row.get('operating_revenue', 0),
                        'profit': row.get('net_profit', 0)
                    }
            return result
        except Exception as e:
            logger.warning(f"获取基本面数据失败: {e}")
            return {}
    
    def _get_growth_data(self, stock: str, date: str) -> Tuple[float, float]:
        """获取增长数据"""
        self._ensure_jqdata()
        jq = self._jq
        
        try:
            # 获取最近两年的年报数据
            end_dt = datetime.strptime(date, "%Y-%m-%d")
            years_ago = (end_dt - timedelta(days=400)).strftime("%Y-%m-%d")
            
            q = jq.query(
                jq.income.statDate,
                jq.income.operating_revenue,
                jq.income.net_profit
            ).filter(
                jq.income.code == stock
            )
            
            df = jq.get_fundamentals(q, statDate=end_dt.strftime("%Y"))
            df_prev = jq.get_fundamentals(q, statDate=(end_dt.year - 1))
            
            if df is not None and len(df) > 0 and df_prev is not None and len(df_prev) > 0:
                rev_now = df['operating_revenue'].iloc[0]
                rev_prev = df_prev['operating_revenue'].iloc[0]
                profit_now = df['net_profit'].iloc[0]
                profit_prev = df_prev['net_profit'].iloc[0]
                
                rev_growth = (rev_now / rev_prev - 1) if rev_prev > 0 else 0
                profit_growth = (profit_now / profit_prev - 1) if profit_prev > 0 else 0
                
                return rev_growth, profit_growth
        except:
            pass
        
        return 0, 0
    
    def _get_universe(self, date: str) -> List[str]:
        """获取股票池 - 扩大范围寻找十倍股"""
        self._ensure_jqdata()
        jq = self._jq
        
        # 沪深300 + 中证500 前200只
        stocks_300 = jq.get_index_stocks('000300.XSHG', date=date)[:100]
        stocks_500 = jq.get_index_stocks('000905.XSHG', date=date)[:100]
        
        # 合并去重
        all_stocks = list(set(stocks_300 + stocks_500))
        return all_stocks[:150]
    
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
    
    def _select_tenbagger_candidates(self, data: Dict, fundamentals: Dict,
                                     regime: AStockRegime, date: str) -> List[Tuple[str, float, TenbaggerStage]]:
        """选择十倍股候选"""
        candidates = []
        
        for stock, df in data['prices'].items():
            try:
                df_to_date = df[df.index <= date]
                if len(df_to_date) < 60:
                    continue
                
                # 基本面数据
                fund = fundamentals.get(stock, {})
                if not fund:
                    continue
                
                market_cap = fund.get('market_cap', 0)
                pe = fund.get('pe', 0)
                roe = fund.get('roe', 0)
                gross_margin = fund.get('gross_margin', 0)
                net_margin = fund.get('net_margin', 0)
                debt_ratio = fund.get('debt_ratio', 0.5)
                
                # 过滤条件（放宽以寻找更多标的）
                if market_cap <= 0 or market_cap > 800:  # 800亿以下
                    continue
                if pe <= 0 or pe > 100:  # PE异常
                    continue
                if roe < 0.05:  # ROE太低
                    continue
                
                # 增长数据（简化：用技术指标代替）
                closes = df_to_date['close']
                volumes = df_to_date['volume']
                
                # 动量计算
                momentum_20d = closes.iloc[-1] / closes.iloc[-20] - 1 if len(closes) >= 20 else 0
                momentum_60d = closes.iloc[-1] / closes.iloc[-60] - 1 if len(closes) >= 60 else 0
                
                # 成交量比
                vol_ratio = volumes.iloc[-5:].mean() / volumes.iloc[-20:].mean() if len(volumes) >= 20 else 1
                
                # 价格位置
                high_52w = closes.rolling(min(252, len(closes))).max().iloc[-1]
                low_52w = closes.rolling(min(252, len(closes))).min().iloc[-1]
                price_position = (closes.iloc[-1] - low_52w) / (high_52w - low_52w) if high_52w != low_52w else 0.5
                
                # 简化的增长估算（基于动量）
                revenue_growth = max(momentum_60d, 0.15)  # 至少15%
                profit_growth = max(momentum_60d * 1.5, 0.20)  # 放大
                
                # PEG估算
                peg = pe / (profit_growth * 100) if profit_growth > 0 else 99
                
                # 十倍股识别
                is_potential, total_score, stage, details = self.tenbagger_identifier.is_potential_tenbagger(
                    roe=roe,
                    gross_margin=gross_margin,
                    net_margin=net_margin,
                    debt_ratio=debt_ratio,
                    revenue_growth=revenue_growth,
                    profit_growth=profit_growth,
                    peg=peg,
                    pe=pe,
                    market_cap=market_cap,
                    momentum_20d=momentum_20d,
                    volume_ratio=vol_ratio,
                    price_position=price_position
                )
                
                # 根据市场环境调整
                if regime in [AStockRegime.BEAR_PANIC]:
                    # 恐慌期：不买入
                    continue
                elif regime in [AStockRegime.BEAR_GRINDING]:
                    # 熊市磨底：只选S2/S3，中等门槛
                    if stage not in [TenbaggerStage.S2_ACCELERATION, TenbaggerStage.S3_EXPANSION]:
                        continue
                    if total_score < 55:
                        continue
                elif regime in [AStockRegime.VOLATILE_DOWN]:
                    # 震荡向下：中等门槛
                    if total_score < 50:
                        continue
                elif regime in [AStockRegime.VOLATILE_RANGE]:
                    # 区间震荡：较低门槛
                    if total_score < 45:
                        continue
                else:
                    # 牛市/震荡向上：放宽条件
                    if total_score < 40:
                        continue
                
                # 排除衰退期
                if stage == TenbaggerStage.S5_DECLINE:
                    continue
                
                candidates.append((stock, total_score, stage))
                
            except Exception as e:
                pass
        
        # 按得分排序
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:10]  # 返回前10个
    
    def run_backtest(self, start_date: str, end_date: str) -> BacktestResult:
        """运行回测"""
        logger.info(f"开始十倍股策略V5回测: {start_date} 至 {end_date}")
        start_time = time.time()
        
        self._ensure_jqdata()
        jq = self._jq
        
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [d.strftime("%Y-%m-%d") if hasattr(d, 'strftime') else str(d) for d in trade_days]
        
        stocks = self._get_universe(start_date)
        data = self._preload_data(start_date, end_date, stocks)
        
        if not data['prices']:
            logger.error("没有可用数据")
            return BacktestResult(0, 0, 0, 0, 0, 0)
        
        # 初始化
        cash = self.initial_capital
        positions = {}  # {stock: (shares, cost, entry_date, stage)}
        equity_history = []
        trades = 0
        wins = 0
        total_sells = 0
        regime_returns = {r.value: [] for r in AStockRegime}
        stage_returns = {s.value: [] for s in TenbaggerStage}
        prev_value = self.initial_capital
        peak_value = self.initial_capital
        fundamentals_cache = {}
        last_fundamental_date = None
        
        # 重置状态
        self.switch_decider = RegimeSwitchDecider()
        
        for i, date in enumerate(trade_days):
            if i < 120:
                equity_history.append((date, cash))
                continue
            
            # 市场环境检测
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
                logger.info(f"[{date}] 环境切换 → {regime.value}")
            
            # 定期更新基本面（每月）
            if last_fundamental_date is None or (datetime.strptime(date, "%Y-%m-%d") - datetime.strptime(last_fundamental_date, "%Y-%m-%d")).days >= 30:
                fundamentals_cache = self._get_fundamentals(data['stocks'], date)
                last_fundamental_date = date
            
            # 计算当前持仓市值
            total_value = cash
            positions_value = {}
            
            for stock, (shares, cost, entry_date, stage) in list(positions.items()):
                if stock in data['prices']:
                    df = data['prices'][stock]
                    df_today = df[df.index <= date]
                    if len(df_today) > 0:
                        price = df_today['close'].iloc[-1]
                        value = price * shares
                        total_value += value
                        positions_value[stock] = value
                        
                        # 获取阶段止损止盈
                        stage_params = STAGE_POSITION_STRATEGY.get(stage, {})
                        stop_loss = stage_params.get('stop_loss', 0.15)
                        take_profit = stage_params.get('take_profit', 0.50)
                        
                        pnl_pct = price / cost - 1
                        hold_days = (datetime.strptime(date, "%Y-%m-%d") - datetime.strptime(entry_date, "%Y-%m-%d")).days
                        
                        should_sell = False
                        sell_reason = ""
                        
                        # 止损
                        if pnl_pct < -stop_loss:
                            should_sell = True
                            sell_reason = f"止损{pnl_pct*100:.1f}%"
                        # 止盈
                        elif pnl_pct > take_profit and hold_days >= self.min_hold_days:
                            should_sell = True
                            sell_reason = f"止盈{pnl_pct*100:.1f}%"
                        
                        if should_sell:
                            cash += price * shares
                            del positions[stock]
                            trades += 1
                            total_sells += 1
                            if pnl_pct > 0:
                                wins += 1
                            logger.info(f"[{date}] {sell_reason} {stock} ({stage.value})")
            
            # 更新峰值和回撤保护
            peak_value = max(peak_value, total_value)
            current_drawdown = (peak_value - total_value) / peak_value
            
            # 根据回撤调整仓位上限
            if current_drawdown > self.max_drawdown_limit:
                max_total_position = 0.3
            elif current_drawdown > 0.10:
                max_total_position = 0.5
            else:
                max_total_position = 0.8
            
            # 根据环境严格限制仓位
            if regime == AStockRegime.BEAR_PANIC:
                max_total_position = 0
                # 强制清仓
                for stock, (shares, cost, entry_date, stage) in list(positions.items()):
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
            elif regime == AStockRegime.BEAR_GRINDING:
                max_total_position = 0.10  # 熊市极低仓位
            elif regime == AStockRegime.VOLATILE_DOWN:
                max_total_position = min(max_total_position, 0.15)  # 震荡下跌低仓位
            elif regime == AStockRegime.VOLATILE_RANGE:
                max_total_position = min(max_total_position, 0.30)  # 区间震荡中仓位
            elif regime == AStockRegime.BULL_LATE:
                max_total_position = min(max_total_position, 0.50)  # 牛市末期谨慎
            
            # 计算当前仓位
            current_position_value = sum(positions_value.values())
            current_position_pct = current_position_value / total_value if total_value > 0 else 0
            
            # 如果当前仓位超过目标，减仓
            if current_position_pct > max_total_position * 1.1 and positions:
                # 选择表现最差的股票减仓
                to_sell = []
                for stock, (shares, cost, entry_date, stage) in positions.items():
                    if stock in positions_value:
                        df = data['prices'][stock]
                        df_today = df[df.index <= date]
                        if len(df_today) > 0:
                            price = df_today['close'].iloc[-1]
                            pnl_pct = price / cost - 1
                            to_sell.append((stock, shares, cost, price, pnl_pct, stage))
                
                to_sell.sort(key=lambda x: x[4])  # 按盈亏排序
                
                for stock, shares, cost, price, pnl_pct, stage in to_sell:
                    if current_position_pct <= max_total_position:
                        break
                    value = price * shares
                    cash += value
                    current_position_pct -= value / total_value
                    del positions[stock]
                    trades += 1
                    total_sells += 1
                    if pnl_pct > 0:
                        wins += 1
                    logger.info(f"[{date}] 减仓({regime.value}) {stock} 盈亏{pnl_pct*100:.1f}%")
            
            # 选股和买入
            if (i % self.rebalance_interval == 0 and 
                current_position_pct < max_total_position and
                regime != AStockRegime.BEAR_PANIC):
                
                candidates = self._select_tenbagger_candidates(data, fundamentals_cache, regime, date)
                
                for stock, score, stage in candidates:
                    if stock in positions:
                        continue
                    if len(positions) >= 5:  # 最多5只
                        break
                    if stock not in data['prices']:
                        continue
                    
                    # 计算可买金额
                    stage_params = STAGE_POSITION_STRATEGY.get(stage, {})
                    max_position = stage_params.get('max_position', 0.10)
                    
                    available = (max_total_position - current_position_pct) * total_value
                    max_per_stock = min(total_value * max_position, total_value * self.max_single_position)
                    buy_amount = min(available, max_per_stock, cash * 0.8)
                    
                    if buy_amount < total_value * self.min_position_per_stock:
                        continue
                    
                    df = data['prices'][stock]
                    df_today = df[df.index <= date]
                    if len(df_today) == 0:
                        continue
                    
                    price = df_today['close'].iloc[-1]
                    shares = int(buy_amount / price / 100) * 100
                    
                    if shares >= 100:
                        cost = price * shares
                        cash -= cost
                        current_position_pct += cost / total_value
                        positions[stock] = (shares, price, date, stage)
                        trades += 1
                        logger.info(f"[{date}] 买入 {stock} @{price:.2f} x{shares} 得分:{score:.0f} 阶段:{stage.value}")
            
            # 记录
            equity_history.append((date, total_value))
            daily_ret = total_value / prev_value - 1 if prev_value > 0 else 0
            regime_returns[regime.value].append(daily_ret)
            prev_value = total_value
            
            # 进度
            if i % 50 == 0 or switched:
                ret = (total_value / self.initial_capital - 1) * 100
                pos_pct = current_position_pct * 100
                logger.info(f"[{date}] 净值:{total_value:,.0f} 收益:{ret:.1f}% 仓位:{pos_pct:.0f}% 环境:{regime.value} 持股:{len(positions)}")
        
        elapsed = time.time() - start_time
        logger.info(f"回测完成，耗时: {elapsed:.1f}秒")
        
        return self._calc_result(equity_history, regime_returns, stage_returns, trades, wins, total_sells)
    
    def _calc_result(self, equity_history, regime_returns, stage_returns,
                     trades, wins, total_sells) -> BacktestResult:
        """计算回测结果"""
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
        stage_perf = {s: sum(rets) * 100 for s, rets in stage_returns.items() if rets}
        
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
            regime_performance=regime_perf,
            stage_performance=stage_perf
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
    logger.info(f"十倍股策略V5 - 周期: {period}")
    logger.info(f"时间范围: {start_date} 至 {end_date}")
    logger.info(f"{'='*60}")
    
    strategy = TenbaggerStrategyV5()
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

