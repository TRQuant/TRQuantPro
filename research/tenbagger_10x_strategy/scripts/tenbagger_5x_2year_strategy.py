#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TenBagger 5X 2Year Strategy - 两年5倍回报策略（优化版）
======================================================

市场环境判断优化：
- 冷却期：环境切换后保持20个交易日
- 确认机制：新环境需连续5天符合条件
- 定期检查：每月初才评估，避免频繁切换
"""

import sys
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass, field

# 导入优化后的市场环境判断模块
try:
    from core.market_regime.comprehensive_regime_detector import (
        ComprehensiveRegimeDetector, MarketRegime, detect_market_regime
    )
    USE_COMPREHENSIVE_REGIME = True
except ImportError:
    USE_COMPREHENSIVE_REGIME = False

PROJECT_ROOT = "/home/taotao/dev/QuantTest/TRQuant"
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TradeRecord:
    date: str
    stock: str
    action: str
    price: float
    shares: int
    value: float
    reason: str


@dataclass
class PositionInfo:
    stock: str
    shares: int
    avg_cost: float
    current_price: float
    pnl: float
    pnl_pct: float
    holding_days: int
    entry_date: str


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
    trades: List[TradeRecord] = field(default_factory=list)
    monthly_returns: pd.Series = None
    regime_performance: Dict[str, float] = field(default_factory=dict)


class TenBagger5X2YearStrategy:
    """两年5倍回报策略（含市场环境冷却期机制）"""
    
    def __init__(self):
        self._jq = None
        self.params = {
            'regime_cooldown': 20,       # 冷却期天数
            'regime_confirm_days': 5,    # 确认天数
            'regime_check_interval': 20, # 检查间隔
            'max_stocks': 5,
            'single_stock_max': 0.25,
            'stop_loss': 0.12,
            'take_profit': 0.50,
            'min_market_cap': 30e8,
            'max_market_cap': 1000e8,
        }
        self.positions: Dict[str, PositionInfo] = {}
        self.cash = 1000000.0
        self.initial_capital = 1000000.0
        self.equity_history = []
        self.trades = []
        self.current_regime = "VOLATILE"
        
        # 冷却期状态
        self._regime_days_held = 0
        self._pending_regime = None
        self._pending_regime_count = 0
        self._last_check_index = -999

    def _ensure_jqdata(self):
        if self._jq is None:
            import jqdatasdk as jq
            import json
            with open(f"{PROJECT_ROOT}/config/jqdata_config.json") as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self._jq = jq
            logger.info(f"JQData认证成功: {config['username']}")

    def _calc_raw_regime(self, date: str) -> str:
        """计算原始市场环境"""
        self._ensure_jqdata()
        jq = self._jq
        try:
            end = datetime.strptime(date, "%Y-%m-%d")
            start = end - timedelta(days=120)
            df = jq.get_price("000001.XSHG", start_date=start.strftime("%Y-%m-%d"),
                             end_date=date, frequency='daily', fields=['close', 'volume'])
            if df is None or len(df) < 60:
                return "VOLATILE"
            
            close = df['close'].values
            volume = df['volume'].values
            ma20 = np.mean(close[-20:])
            ma60 = np.mean(close[-60:])
            current = close[-1]
            mom_20 = (current / close[-20] - 1) * 100
            mom_60 = (current / close[-60] - 1) * 100
            returns = np.diff(np.log(close[-30:]))
            volatility = np.std(returns) * np.sqrt(252) * 100
            vol_ratio = np.mean(volume[-5:]) / np.mean(volume[-20:])
            
            score = 0
            if current > ma20 > ma60: score += 30
            elif current < ma20 < ma60: score -= 30
            score += min(20, max(-20, mom_20 * 2))
            score += min(10, max(-10, mom_60))
            if volatility < 15: score += 10
            elif volatility > 30: score -= 10
            if vol_ratio > 1.2: score += 10
            elif vol_ratio < 0.8: score -= 10
            
            if score > 30:
                return "DISTRIBUTION" if mom_20 > 20 else "BULL"
            elif score < -30:
                return "RECOVERY" if mom_20 < -20 and volatility < 20 else "BEAR"
            return "VOLATILE"
        except Exception as e:
            logger.error(f"计算环境失败: {e}")
            return "VOLATILE"

    def detect_market_regime(self, date: str, idx: int) -> Tuple[str, bool, str]:
        """检测市场环境（带冷却期和确认机制）"""
        self._regime_days_held += 1
        cooldown = self.params['regime_cooldown']
        confirm = self.params['regime_confirm_days']
        interval = self.params['regime_check_interval']
        
        # 冷却期内不检查
        if self._regime_days_held < cooldown:
            return self.current_regime, False, f"冷却期({self._regime_days_held}/{cooldown})"
        
        # 非检查周期
        if idx - self._last_check_index < interval:
            return self.current_regime, False, "非检查周期"
        
        self._last_check_index = idx
        new_regime = self._calc_raw_regime(date)
        
        if new_regime == self.current_regime:
            self._pending_regime = None
            self._pending_regime_count = 0
            return self.current_regime, False, f"环境稳定({self.current_regime})"
        
        if self._pending_regime == new_regime:
            self._pending_regime_count += 1
        else:
            self._pending_regime = new_regime
            self._pending_regime_count = 1
        
        if self._pending_regime_count >= confirm:
            old = self.current_regime
            self.current_regime = new_regime
            self._regime_days_held = 0
            self._pending_regime = None
            self._pending_regime_count = 0
            reason = f"切换: {old}->{new_regime} (确认{confirm}天)"
            logger.info(f"[{date}] *** 环境{reason}")
            return self.current_regime, True, reason
        
        return self.current_regime, False, f"待确认:{new_regime}({self._pending_regime_count}/{confirm})"

    def get_universe(self, date: str) -> List[str]:
        self._ensure_jqdata()
        try:
            from jqdatasdk import query, valuation
            q = query(valuation.code).filter(
                valuation.market_cap > self.params['min_market_cap'] / 1e8,
                valuation.market_cap < self.params['max_market_cap'] / 1e8,
                valuation.pe_ratio > 0, valuation.pe_ratio < 100
            ).order_by(valuation.market_cap.desc()).limit(300)
            df = self._jq.get_fundamentals(q, date=date)
            return df['code'].tolist() if df is not None else []
        except:
            return []

    def score_stock(self, stock: str, date: str) -> float:
        self._ensure_jqdata()
        try:
            end = datetime.strptime(date, "%Y-%m-%d")
            start = end - timedelta(days=120)
            df = self._jq.get_price(stock, start_date=start.strftime("%Y-%m-%d"),
                                   end_date=date, frequency='daily', fields=['close', 'volume'])
            if df is None or len(df) < 60:
                return 0.0
            
            close = df['close'].values
            score = 50.0
            mom_20 = (close[-1] / close[-20] - 1) * 100
            if 5 < mom_20 < 30: score += 10
            elif mom_20 > 50: score -= 5
            elif mom_20 < -10: score -= 10
            
            from jqdatasdk import query, indicator
            q = query(indicator.inc_revenue_year_on_year, indicator.inc_net_profit_year_on_year,
                     indicator.roe).filter(indicator.code == stock)
            fund = self._jq.get_fundamentals(q, date=date)
            if fund is not None and len(fund) > 0:
                rev = fund['inc_revenue_year_on_year'].iloc[0] or 0
                profit = fund['inc_net_profit_year_on_year'].iloc[0] or 0
                roe = fund['roe'].iloc[0] or 0
                if rev > 30: score += 10
                elif rev > 15: score += 5
                if profit > 50: score += 10
                elif profit > 20: score += 5
                if roe > 15: score += 5
            
            return max(0, min(100, score))
        except:
            return 0.0

    def select_stocks(self, date: str) -> List[Tuple[str, float]]:
        universe = self.get_universe(date)
        scores = [(s, self.score_stock(s, date)) for s in universe[:100]]
        scores = [(s, sc) for s, sc in scores if sc > 60]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:self.params['max_stocks'] * 2]

    def get_target_position(self) -> float:
        return {'BULL': 0.85, 'RECOVERY': 0.70, 'VOLATILE': 0.50,
                'DISTRIBUTION': 0.35, 'BEAR': 0.15}.get(self.current_regime, 0.5)

    def execute_trades(self, date: str, candidates: List[Tuple[str, float]]):
        self._ensure_jqdata()
        jq = self._jq
        target_pos = self.get_target_position()
        total_val = self.get_total_value(date)
        target_inv = total_val * target_pos
        
        # 止损止盈
        for stock, pos in list(self.positions.items()):
            try:
                p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                if p is None or len(p) == 0: continue
                price = p['close'].iloc[-1]
                pnl_pct = price / pos.avg_cost - 1
                pos.current_price = price
                pos.pnl_pct = pnl_pct
                pos.pnl = (price - pos.avg_cost) * pos.shares
                pos.holding_days += 1
                
                if pnl_pct < -self.params['stop_loss']:
                    self._sell(stock, date, price, "止损")
                elif pnl_pct > self.params['take_profit']:
                    self._sell(stock, date, price, "止盈")
                elif pos.holding_days > 60 and pnl_pct < 0.05:
                    self._sell(stock, date, price, "超时")
            except:
                pass
        
        # 调仓
        curr_inv = sum(p.current_price * p.shares for p in self.positions.values())
        if curr_inv > target_inv * 1.1:
            for stock in sorted(self.positions.keys(), key=lambda x: self.positions[x].pnl_pct):
                if curr_inv <= target_inv: break
                try:
                    p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                    if p is not None and len(p) > 0:
                        self._sell(stock, date, p['close'].iloc[-1], "减仓")
                        curr_inv -= self.positions.get(stock, PositionInfo("",0,0,0,0,0,0,"")).current_price * self.positions.get(stock, PositionInfo("",0,0,0,0,0,0,"")).shares
                except:
                    pass
        
        # 买入
        if len(self.positions) < self.params['max_stocks'] and self.cash > total_val * 0.1:
            for stock, score in candidates:
                if stock in self.positions or len(self.positions) >= self.params['max_stocks']:
                    continue
                try:
                    p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                    if p is None or len(p) == 0: continue
                    price = p['close'].iloc[-1]
                    max_amt = total_val * self.params['single_stock_max']
                    shares = int(min(max_amt, self.cash * 0.9) / price / 100) * 100
                    if shares >= 100:
                        self._buy(stock, date, price, shares, f"得分{score:.0f}")
                except:
                    pass

    def _buy(self, stock: str, date: str, price: float, shares: int, reason: str):
        value = price * shares
        if value > self.cash: return
        self.cash -= value
        self.positions[stock] = PositionInfo(stock, shares, price, price, 0, 0, 0, date)
        self.trades.append(TradeRecord(date, stock, "BUY", price, shares, value, reason))
        logger.info(f"[{date}] 买入 {stock} @{price:.2f} x{shares} ({reason})")

    def _sell(self, stock: str, date: str, price: float, reason: str):
        if stock not in self.positions: return
        pos = self.positions[stock]
        value = price * pos.shares
        self.cash += value
        pnl = (price - pos.avg_cost) * pos.shares
        self.trades.append(TradeRecord(date, stock, "SELL", price, pos.shares, value, reason))
        logger.info(f"[{date}] 卖出 {stock} @{price:.2f} 盈亏{pnl:.0f} ({reason})")
        del self.positions[stock]

    def get_total_value(self, date: str) -> float:
        self._ensure_jqdata()
        total = self.cash
        for stock, pos in self.positions.items():
            try:
                p = self._jq.get_price(stock, end_date=date, count=1, fields=['close'])
                total += (p['close'].iloc[-1] if p is not None and len(p) > 0 else pos.current_price) * pos.shares
            except:
                total += pos.current_price * pos.shares
        return total

    def run_backtest(self, start_date: str, end_date: str) -> BacktestResult:
        logger.info(f"开始回测: {start_date} 至 {end_date}")
        logger.info(f"冷却期={self.params['regime_cooldown']}天, 确认={self.params['regime_confirm_days']}天")
        
        self._ensure_jqdata()
        self.positions = {}
        self.cash = self.initial_capital
        self.equity_history = []
        self.trades = []
        self._regime_days_held = 0
        self._pending_regime = None
        self._pending_regime_count = 0
        self._last_check_index = -999
        
        trade_days = self._jq.get_trade_days(start_date=start_date, end_date=end_date)
        regime_returns = {r: [] for r in ['BULL', 'BEAR', 'VOLATILE', 'RECOVERY', 'DISTRIBUTION']}
        prev_value = self.initial_capital
        
        for i, td in enumerate(trade_days):
            date = td.strftime("%Y-%m-%d") if hasattr(td, 'strftime') else str(td)
            
            # 环境检测（带冷却期）
            regime, changed, reason = self.detect_market_regime(date, i)
            
            # 只在真正切换或首次时输出
            if changed or i == 0:
                logger.info(f"[{date}] 环境: {regime} | {reason}")
            
            if i % 5 == 0:
                candidates = self.select_stocks(date)
            else:
                candidates = []
            
            self.execute_trades(date, candidates)
            
            total = self.get_total_value(date)
            self.equity_history.append((date, total))
            regime_returns[self.current_regime].append((total / prev_value - 1) if prev_value > 0 else 0)
            prev_value = total
            
            if i % 20 == 0:
                ret = (total / self.initial_capital - 1) * 100
                logger.info(f"[{date}] 净值:{total:.0f} 收益:{ret:.1f}% 环境:{self.current_regime} 持续:{self._regime_days_held}天")
        
        return self._calc_result(regime_returns)

    def _calc_result(self, regime_returns: Dict[str, List[float]]) -> BacktestResult:
        if not self.equity_history:
            return BacktestResult(0, 0, 0, 0, 0, 0, 0)
        
        dates = [x[0] for x in self.equity_history]
        values = [x[1] for x in self.equity_history]
        
        df = pd.DataFrame({'date': dates, 'equity': values})
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df['return'] = df['equity'].pct_change()
        
        total_ret = (values[-1] / self.initial_capital - 1) * 100
        years = len(values) / 252
        annual_ret = ((values[-1] / self.initial_capital) ** (1/years) - 1) * 100 if years > 0 else 0
        
        rets = df['return'].dropna()
        sharpe = np.sqrt(252) * rets.mean() / rets.std() if len(rets) > 0 and rets.std() > 0 else 0
        
        df['cummax'] = df['equity'].cummax()
        df['dd'] = (df['cummax'] - df['equity']) / df['cummax']
        max_dd = df['dd'].max() * 100
        
        wins = len([t for t in self.trades if t.action == 'SELL' and 
                   any(b.stock == t.stock and b.action == 'BUY' and b.price < t.price for b in self.trades)])
        total_sells = len([t for t in self.trades if t.action == 'SELL'])
        win_rate = wins / total_sells * 100 if total_sells > 0 else 0
        
        regime_perf = {r: sum(rets) * 100 for r, rets in regime_returns.items() if rets}
        
        return BacktestResult(
            total_return=total_ret, annualized_return=annual_ret, sharpe_ratio=sharpe,
            max_drawdown=max_dd, win_rate=win_rate, profit_factor=0, total_trades=len(self.trades),
            equity_curve=df, trades=self.trades, regime_performance=regime_perf
        )


def main():
    strategy = TenBagger5X2YearStrategy()
    result = strategy.run_backtest("2022-01-01", "2024-12-31")
    
    print("\n" + "="*60)
    print("两年5倍回报策略 - 回测结果")
    print("="*60)
    print(f"总收益率: {result.total_return:.2f}%")
    print(f"年化收益率: {result.annualized_return:.2f}%")
    print(f"夏普比率: {result.sharpe_ratio:.2f}")
    print(f"最大回撤: {result.max_drawdown:.2f}%")
    print(f"胜率: {result.win_rate:.1f}%")
    print(f"总交易: {result.total_trades}")
    print("\n各环境收益:")
    for r, ret in result.regime_performance.items():
        print(f"  {r}: {ret:.2f}%")


if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
TenBagger 5X 2Year Strategy - 两年5倍回报策略（优化版）
======================================================

市场环境判断优化：
- 冷却期：环境切换后保持20个交易日
- 确认机制：新环境需连续5天符合条件
- 定期检查：每月初才评估，避免频繁切换
"""

import sys
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass, field

# 导入优化后的市场环境判断模块
try:
    from core.market_regime.comprehensive_regime_detector import (
        ComprehensiveRegimeDetector, MarketRegime, detect_market_regime
    )
    USE_COMPREHENSIVE_REGIME = True
except ImportError:
    USE_COMPREHENSIVE_REGIME = False

PROJECT_ROOT = "/home/taotao/dev/QuantTest/TRQuant"
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TradeRecord:
    date: str
    stock: str
    action: str
    price: float
    shares: int
    value: float
    reason: str


@dataclass
class PositionInfo:
    stock: str
    shares: int
    avg_cost: float
    current_price: float
    pnl: float
    pnl_pct: float
    holding_days: int
    entry_date: str


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
    trades: List[TradeRecord] = field(default_factory=list)
    monthly_returns: pd.Series = None
    regime_performance: Dict[str, float] = field(default_factory=dict)


class TenBagger5X2YearStrategy:
    """两年5倍回报策略（含市场环境冷却期机制）"""
    
    def __init__(self):
        self._jq = None
        self.params = {
            'regime_cooldown': 20,       # 冷却期天数
            'regime_confirm_days': 5,    # 确认天数
            'regime_check_interval': 20, # 检查间隔
            'max_stocks': 5,
            'single_stock_max': 0.25,
            'stop_loss': 0.12,
            'take_profit': 0.50,
            'min_market_cap': 30e8,
            'max_market_cap': 1000e8,
        }
        self.positions: Dict[str, PositionInfo] = {}
        self.cash = 1000000.0
        self.initial_capital = 1000000.0
        self.equity_history = []
        self.trades = []
        self.current_regime = "VOLATILE"
        
        # 冷却期状态
        self._regime_days_held = 0
        self._pending_regime = None
        self._pending_regime_count = 0
        self._last_check_index = -999

    def _ensure_jqdata(self):
        if self._jq is None:
            import jqdatasdk as jq
            import json
            with open(f"{PROJECT_ROOT}/config/jqdata_config.json") as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self._jq = jq
            logger.info(f"JQData认证成功: {config['username']}")

    def _calc_raw_regime(self, date: str) -> str:
        """计算原始市场环境"""
        self._ensure_jqdata()
        jq = self._jq
        try:
            end = datetime.strptime(date, "%Y-%m-%d")
            start = end - timedelta(days=120)
            df = jq.get_price("000001.XSHG", start_date=start.strftime("%Y-%m-%d"),
                             end_date=date, frequency='daily', fields=['close', 'volume'])
            if df is None or len(df) < 60:
                return "VOLATILE"
            
            close = df['close'].values
            volume = df['volume'].values
            ma20 = np.mean(close[-20:])
            ma60 = np.mean(close[-60:])
            current = close[-1]
            mom_20 = (current / close[-20] - 1) * 100
            mom_60 = (current / close[-60] - 1) * 100
            returns = np.diff(np.log(close[-30:]))
            volatility = np.std(returns) * np.sqrt(252) * 100
            vol_ratio = np.mean(volume[-5:]) / np.mean(volume[-20:])
            
            score = 0
            if current > ma20 > ma60: score += 30
            elif current < ma20 < ma60: score -= 30
            score += min(20, max(-20, mom_20 * 2))
            score += min(10, max(-10, mom_60))
            if volatility < 15: score += 10
            elif volatility > 30: score -= 10
            if vol_ratio > 1.2: score += 10
            elif vol_ratio < 0.8: score -= 10
            
            if score > 30:
                return "DISTRIBUTION" if mom_20 > 20 else "BULL"
            elif score < -30:
                return "RECOVERY" if mom_20 < -20 and volatility < 20 else "BEAR"
            return "VOLATILE"
        except Exception as e:
            logger.error(f"计算环境失败: {e}")
            return "VOLATILE"

    def detect_market_regime(self, date: str, idx: int) -> Tuple[str, bool, str]:
        """检测市场环境（带冷却期和确认机制）"""
        self._regime_days_held += 1
        cooldown = self.params['regime_cooldown']
        confirm = self.params['regime_confirm_days']
        interval = self.params['regime_check_interval']
        
        # 冷却期内不检查
        if self._regime_days_held < cooldown:
            return self.current_regime, False, f"冷却期({self._regime_days_held}/{cooldown})"
        
        # 非检查周期
        if idx - self._last_check_index < interval:
            return self.current_regime, False, "非检查周期"
        
        self._last_check_index = idx
        new_regime = self._calc_raw_regime(date)
        
        if new_regime == self.current_regime:
            self._pending_regime = None
            self._pending_regime_count = 0
            return self.current_regime, False, f"环境稳定({self.current_regime})"
        
        if self._pending_regime == new_regime:
            self._pending_regime_count += 1
        else:
            self._pending_regime = new_regime
            self._pending_regime_count = 1
        
        if self._pending_regime_count >= confirm:
            old = self.current_regime
            self.current_regime = new_regime
            self._regime_days_held = 0
            self._pending_regime = None
            self._pending_regime_count = 0
            reason = f"切换: {old}->{new_regime} (确认{confirm}天)"
            logger.info(f"[{date}] *** 环境{reason}")
            return self.current_regime, True, reason
        
        return self.current_regime, False, f"待确认:{new_regime}({self._pending_regime_count}/{confirm})"

    def get_universe(self, date: str) -> List[str]:
        self._ensure_jqdata()
        try:
            from jqdatasdk import query, valuation
            q = query(valuation.code).filter(
                valuation.market_cap > self.params['min_market_cap'] / 1e8,
                valuation.market_cap < self.params['max_market_cap'] / 1e8,
                valuation.pe_ratio > 0, valuation.pe_ratio < 100
            ).order_by(valuation.market_cap.desc()).limit(300)
            df = self._jq.get_fundamentals(q, date=date)
            return df['code'].tolist() if df is not None else []
        except:
            return []

    def score_stock(self, stock: str, date: str) -> float:
        self._ensure_jqdata()
        try:
            end = datetime.strptime(date, "%Y-%m-%d")
            start = end - timedelta(days=120)
            df = self._jq.get_price(stock, start_date=start.strftime("%Y-%m-%d"),
                                   end_date=date, frequency='daily', fields=['close', 'volume'])
            if df is None or len(df) < 60:
                return 0.0
            
            close = df['close'].values
            score = 50.0
            mom_20 = (close[-1] / close[-20] - 1) * 100
            if 5 < mom_20 < 30: score += 10
            elif mom_20 > 50: score -= 5
            elif mom_20 < -10: score -= 10
            
            from jqdatasdk import query, indicator
            q = query(indicator.inc_revenue_year_on_year, indicator.inc_net_profit_year_on_year,
                     indicator.roe).filter(indicator.code == stock)
            fund = self._jq.get_fundamentals(q, date=date)
            if fund is not None and len(fund) > 0:
                rev = fund['inc_revenue_year_on_year'].iloc[0] or 0
                profit = fund['inc_net_profit_year_on_year'].iloc[0] or 0
                roe = fund['roe'].iloc[0] or 0
                if rev > 30: score += 10
                elif rev > 15: score += 5
                if profit > 50: score += 10
                elif profit > 20: score += 5
                if roe > 15: score += 5
            
            return max(0, min(100, score))
        except:
            return 0.0

    def select_stocks(self, date: str) -> List[Tuple[str, float]]:
        universe = self.get_universe(date)
        scores = [(s, self.score_stock(s, date)) for s in universe[:100]]
        scores = [(s, sc) for s, sc in scores if sc > 60]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:self.params['max_stocks'] * 2]

    def get_target_position(self) -> float:
        return {'BULL': 0.85, 'RECOVERY': 0.70, 'VOLATILE': 0.50,
                'DISTRIBUTION': 0.35, 'BEAR': 0.15}.get(self.current_regime, 0.5)

    def execute_trades(self, date: str, candidates: List[Tuple[str, float]]):
        self._ensure_jqdata()
        jq = self._jq
        target_pos = self.get_target_position()
        total_val = self.get_total_value(date)
        target_inv = total_val * target_pos
        
        # 止损止盈
        for stock, pos in list(self.positions.items()):
            try:
                p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                if p is None or len(p) == 0: continue
                price = p['close'].iloc[-1]
                pnl_pct = price / pos.avg_cost - 1
                pos.current_price = price
                pos.pnl_pct = pnl_pct
                pos.pnl = (price - pos.avg_cost) * pos.shares
                pos.holding_days += 1
                
                if pnl_pct < -self.params['stop_loss']:
                    self._sell(stock, date, price, "止损")
                elif pnl_pct > self.params['take_profit']:
                    self._sell(stock, date, price, "止盈")
                elif pos.holding_days > 60 and pnl_pct < 0.05:
                    self._sell(stock, date, price, "超时")
            except:
                pass
        
        # 调仓
        curr_inv = sum(p.current_price * p.shares for p in self.positions.values())
        if curr_inv > target_inv * 1.1:
            for stock in sorted(self.positions.keys(), key=lambda x: self.positions[x].pnl_pct):
                if curr_inv <= target_inv: break
                try:
                    p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                    if p is not None and len(p) > 0:
                        self._sell(stock, date, p['close'].iloc[-1], "减仓")
                        curr_inv -= self.positions.get(stock, PositionInfo("",0,0,0,0,0,0,"")).current_price * self.positions.get(stock, PositionInfo("",0,0,0,0,0,0,"")).shares
                except:
                    pass
        
        # 买入
        if len(self.positions) < self.params['max_stocks'] and self.cash > total_val * 0.1:
            for stock, score in candidates:
                if stock in self.positions or len(self.positions) >= self.params['max_stocks']:
                    continue
                try:
                    p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                    if p is None or len(p) == 0: continue
                    price = p['close'].iloc[-1]
                    max_amt = total_val * self.params['single_stock_max']
                    shares = int(min(max_amt, self.cash * 0.9) / price / 100) * 100
                    if shares >= 100:
                        self._buy(stock, date, price, shares, f"得分{score:.0f}")
                except:
                    pass

    def _buy(self, stock: str, date: str, price: float, shares: int, reason: str):
        value = price * shares
        if value > self.cash: return
        self.cash -= value
        self.positions[stock] = PositionInfo(stock, shares, price, price, 0, 0, 0, date)
        self.trades.append(TradeRecord(date, stock, "BUY", price, shares, value, reason))
        logger.info(f"[{date}] 买入 {stock} @{price:.2f} x{shares} ({reason})")

    def _sell(self, stock: str, date: str, price: float, reason: str):
        if stock not in self.positions: return
        pos = self.positions[stock]
        value = price * pos.shares
        self.cash += value
        pnl = (price - pos.avg_cost) * pos.shares
        self.trades.append(TradeRecord(date, stock, "SELL", price, pos.shares, value, reason))
        logger.info(f"[{date}] 卖出 {stock} @{price:.2f} 盈亏{pnl:.0f} ({reason})")
        del self.positions[stock]

    def get_total_value(self, date: str) -> float:
        self._ensure_jqdata()
        total = self.cash
        for stock, pos in self.positions.items():
            try:
                p = self._jq.get_price(stock, end_date=date, count=1, fields=['close'])
                total += (p['close'].iloc[-1] if p is not None and len(p) > 0 else pos.current_price) * pos.shares
            except:
                total += pos.current_price * pos.shares
        return total

    def run_backtest(self, start_date: str, end_date: str) -> BacktestResult:
        logger.info(f"开始回测: {start_date} 至 {end_date}")
        logger.info(f"冷却期={self.params['regime_cooldown']}天, 确认={self.params['regime_confirm_days']}天")
        
        self._ensure_jqdata()
        self.positions = {}
        self.cash = self.initial_capital
        self.equity_history = []
        self.trades = []
        self._regime_days_held = 0
        self._pending_regime = None
        self._pending_regime_count = 0
        self._last_check_index = -999
        
        trade_days = self._jq.get_trade_days(start_date=start_date, end_date=end_date)
        regime_returns = {r: [] for r in ['BULL', 'BEAR', 'VOLATILE', 'RECOVERY', 'DISTRIBUTION']}
        prev_value = self.initial_capital
        
        for i, td in enumerate(trade_days):
            date = td.strftime("%Y-%m-%d") if hasattr(td, 'strftime') else str(td)
            
            # 环境检测（带冷却期）
            regime, changed, reason = self.detect_market_regime(date, i)
            
            # 只在真正切换或首次时输出
            if changed or i == 0:
                logger.info(f"[{date}] 环境: {regime} | {reason}")
            
            if i % 5 == 0:
                candidates = self.select_stocks(date)
            else:
                candidates = []
            
            self.execute_trades(date, candidates)
            
            total = self.get_total_value(date)
            self.equity_history.append((date, total))
            regime_returns[self.current_regime].append((total / prev_value - 1) if prev_value > 0 else 0)
            prev_value = total
            
            if i % 20 == 0:
                ret = (total / self.initial_capital - 1) * 100
                logger.info(f"[{date}] 净值:{total:.0f} 收益:{ret:.1f}% 环境:{self.current_regime} 持续:{self._regime_days_held}天")
        
        return self._calc_result(regime_returns)

    def _calc_result(self, regime_returns: Dict[str, List[float]]) -> BacktestResult:
        if not self.equity_history:
            return BacktestResult(0, 0, 0, 0, 0, 0, 0)
        
        dates = [x[0] for x in self.equity_history]
        values = [x[1] for x in self.equity_history]
        
        df = pd.DataFrame({'date': dates, 'equity': values})
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df['return'] = df['equity'].pct_change()
        
        total_ret = (values[-1] / self.initial_capital - 1) * 100
        years = len(values) / 252
        annual_ret = ((values[-1] / self.initial_capital) ** (1/years) - 1) * 100 if years > 0 else 0
        
        rets = df['return'].dropna()
        sharpe = np.sqrt(252) * rets.mean() / rets.std() if len(rets) > 0 and rets.std() > 0 else 0
        
        df['cummax'] = df['equity'].cummax()
        df['dd'] = (df['cummax'] - df['equity']) / df['cummax']
        max_dd = df['dd'].max() * 100
        
        wins = len([t for t in self.trades if t.action == 'SELL' and 
                   any(b.stock == t.stock and b.action == 'BUY' and b.price < t.price for b in self.trades)])
        total_sells = len([t for t in self.trades if t.action == 'SELL'])
        win_rate = wins / total_sells * 100 if total_sells > 0 else 0
        
        regime_perf = {r: sum(rets) * 100 for r, rets in regime_returns.items() if rets}
        
        return BacktestResult(
            total_return=total_ret, annualized_return=annual_ret, sharpe_ratio=sharpe,
            max_drawdown=max_dd, win_rate=win_rate, profit_factor=0, total_trades=len(self.trades),
            equity_curve=df, trades=self.trades, regime_performance=regime_perf
        )


def main():
    strategy = TenBagger5X2YearStrategy()
    result = strategy.run_backtest("2022-01-01", "2024-12-31")
    
    print("\n" + "="*60)
    print("两年5倍回报策略 - 回测结果")
    print("="*60)
    print(f"总收益率: {result.total_return:.2f}%")
    print(f"年化收益率: {result.annualized_return:.2f}%")
    print(f"夏普比率: {result.sharpe_ratio:.2f}")
    print(f"最大回撤: {result.max_drawdown:.2f}%")
    print(f"胜率: {result.win_rate:.1f}%")
    print(f"总交易: {result.total_trades}")
    print("\n各环境收益:")
    for r, ret in result.regime_performance.items():
        print(f"  {r}: {ret:.2f}%")


if __name__ == "__main__":
    main()



















# -*- coding: utf-8 -*-
"""
TenBagger 5X 2Year Strategy - 两年5倍回报策略（优化版）
======================================================

市场环境判断优化：
- 冷却期：环境切换后保持20个交易日
- 确认机制：新环境需连续5天符合条件
- 定期检查：每月初才评估，避免频繁切换
"""

import sys
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass, field

# 导入优化后的市场环境判断模块
try:
    from core.market_regime.comprehensive_regime_detector import (
        ComprehensiveRegimeDetector, MarketRegime, detect_market_regime
    )
    USE_COMPREHENSIVE_REGIME = True
except ImportError:
    USE_COMPREHENSIVE_REGIME = False

PROJECT_ROOT = "/home/taotao/dev/QuantTest/TRQuant"
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TradeRecord:
    date: str
    stock: str
    action: str
    price: float
    shares: int
    value: float
    reason: str


@dataclass
class PositionInfo:
    stock: str
    shares: int
    avg_cost: float
    current_price: float
    pnl: float
    pnl_pct: float
    holding_days: int
    entry_date: str


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
    trades: List[TradeRecord] = field(default_factory=list)
    monthly_returns: pd.Series = None
    regime_performance: Dict[str, float] = field(default_factory=dict)


class TenBagger5X2YearStrategy:
    """两年5倍回报策略（含市场环境冷却期机制）"""
    
    def __init__(self):
        self._jq = None
        self.params = {
            'regime_cooldown': 20,       # 冷却期天数
            'regime_confirm_days': 5,    # 确认天数
            'regime_check_interval': 20, # 检查间隔
            'max_stocks': 5,
            'single_stock_max': 0.25,
            'stop_loss': 0.12,
            'take_profit': 0.50,
            'min_market_cap': 30e8,
            'max_market_cap': 1000e8,
        }
        self.positions: Dict[str, PositionInfo] = {}
        self.cash = 1000000.0
        self.initial_capital = 1000000.0
        self.equity_history = []
        self.trades = []
        self.current_regime = "VOLATILE"
        
        # 冷却期状态
        self._regime_days_held = 0
        self._pending_regime = None
        self._pending_regime_count = 0
        self._last_check_index = -999

    def _ensure_jqdata(self):
        if self._jq is None:
            import jqdatasdk as jq
            import json
            with open(f"{PROJECT_ROOT}/config/jqdata_config.json") as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self._jq = jq
            logger.info(f"JQData认证成功: {config['username']}")

    def _calc_raw_regime(self, date: str) -> str:
        """计算原始市场环境"""
        self._ensure_jqdata()
        jq = self._jq
        try:
            end = datetime.strptime(date, "%Y-%m-%d")
            start = end - timedelta(days=120)
            df = jq.get_price("000001.XSHG", start_date=start.strftime("%Y-%m-%d"),
                             end_date=date, frequency='daily', fields=['close', 'volume'])
            if df is None or len(df) < 60:
                return "VOLATILE"
            
            close = df['close'].values
            volume = df['volume'].values
            ma20 = np.mean(close[-20:])
            ma60 = np.mean(close[-60:])
            current = close[-1]
            mom_20 = (current / close[-20] - 1) * 100
            mom_60 = (current / close[-60] - 1) * 100
            returns = np.diff(np.log(close[-30:]))
            volatility = np.std(returns) * np.sqrt(252) * 100
            vol_ratio = np.mean(volume[-5:]) / np.mean(volume[-20:])
            
            score = 0
            if current > ma20 > ma60: score += 30
            elif current < ma20 < ma60: score -= 30
            score += min(20, max(-20, mom_20 * 2))
            score += min(10, max(-10, mom_60))
            if volatility < 15: score += 10
            elif volatility > 30: score -= 10
            if vol_ratio > 1.2: score += 10
            elif vol_ratio < 0.8: score -= 10
            
            if score > 30:
                return "DISTRIBUTION" if mom_20 > 20 else "BULL"
            elif score < -30:
                return "RECOVERY" if mom_20 < -20 and volatility < 20 else "BEAR"
            return "VOLATILE"
        except Exception as e:
            logger.error(f"计算环境失败: {e}")
            return "VOLATILE"

    def detect_market_regime(self, date: str, idx: int) -> Tuple[str, bool, str]:
        """检测市场环境（带冷却期和确认机制）"""
        self._regime_days_held += 1
        cooldown = self.params['regime_cooldown']
        confirm = self.params['regime_confirm_days']
        interval = self.params['regime_check_interval']
        
        # 冷却期内不检查
        if self._regime_days_held < cooldown:
            return self.current_regime, False, f"冷却期({self._regime_days_held}/{cooldown})"
        
        # 非检查周期
        if idx - self._last_check_index < interval:
            return self.current_regime, False, "非检查周期"
        
        self._last_check_index = idx
        new_regime = self._calc_raw_regime(date)
        
        if new_regime == self.current_regime:
            self._pending_regime = None
            self._pending_regime_count = 0
            return self.current_regime, False, f"环境稳定({self.current_regime})"
        
        if self._pending_regime == new_regime:
            self._pending_regime_count += 1
        else:
            self._pending_regime = new_regime
            self._pending_regime_count = 1
        
        if self._pending_regime_count >= confirm:
            old = self.current_regime
            self.current_regime = new_regime
            self._regime_days_held = 0
            self._pending_regime = None
            self._pending_regime_count = 0
            reason = f"切换: {old}->{new_regime} (确认{confirm}天)"
            logger.info(f"[{date}] *** 环境{reason}")
            return self.current_regime, True, reason
        
        return self.current_regime, False, f"待确认:{new_regime}({self._pending_regime_count}/{confirm})"

    def get_universe(self, date: str) -> List[str]:
        self._ensure_jqdata()
        try:
            from jqdatasdk import query, valuation
            q = query(valuation.code).filter(
                valuation.market_cap > self.params['min_market_cap'] / 1e8,
                valuation.market_cap < self.params['max_market_cap'] / 1e8,
                valuation.pe_ratio > 0, valuation.pe_ratio < 100
            ).order_by(valuation.market_cap.desc()).limit(300)
            df = self._jq.get_fundamentals(q, date=date)
            return df['code'].tolist() if df is not None else []
        except:
            return []

    def score_stock(self, stock: str, date: str) -> float:
        self._ensure_jqdata()
        try:
            end = datetime.strptime(date, "%Y-%m-%d")
            start = end - timedelta(days=120)
            df = self._jq.get_price(stock, start_date=start.strftime("%Y-%m-%d"),
                                   end_date=date, frequency='daily', fields=['close', 'volume'])
            if df is None or len(df) < 60:
                return 0.0
            
            close = df['close'].values
            score = 50.0
            mom_20 = (close[-1] / close[-20] - 1) * 100
            if 5 < mom_20 < 30: score += 10
            elif mom_20 > 50: score -= 5
            elif mom_20 < -10: score -= 10
            
            from jqdatasdk import query, indicator
            q = query(indicator.inc_revenue_year_on_year, indicator.inc_net_profit_year_on_year,
                     indicator.roe).filter(indicator.code == stock)
            fund = self._jq.get_fundamentals(q, date=date)
            if fund is not None and len(fund) > 0:
                rev = fund['inc_revenue_year_on_year'].iloc[0] or 0
                profit = fund['inc_net_profit_year_on_year'].iloc[0] or 0
                roe = fund['roe'].iloc[0] or 0
                if rev > 30: score += 10
                elif rev > 15: score += 5
                if profit > 50: score += 10
                elif profit > 20: score += 5
                if roe > 15: score += 5
            
            return max(0, min(100, score))
        except:
            return 0.0

    def select_stocks(self, date: str) -> List[Tuple[str, float]]:
        universe = self.get_universe(date)
        scores = [(s, self.score_stock(s, date)) for s in universe[:100]]
        scores = [(s, sc) for s, sc in scores if sc > 60]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:self.params['max_stocks'] * 2]

    def get_target_position(self) -> float:
        return {'BULL': 0.85, 'RECOVERY': 0.70, 'VOLATILE': 0.50,
                'DISTRIBUTION': 0.35, 'BEAR': 0.15}.get(self.current_regime, 0.5)

    def execute_trades(self, date: str, candidates: List[Tuple[str, float]]):
        self._ensure_jqdata()
        jq = self._jq
        target_pos = self.get_target_position()
        total_val = self.get_total_value(date)
        target_inv = total_val * target_pos
        
        # 止损止盈
        for stock, pos in list(self.positions.items()):
            try:
                p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                if p is None or len(p) == 0: continue
                price = p['close'].iloc[-1]
                pnl_pct = price / pos.avg_cost - 1
                pos.current_price = price
                pos.pnl_pct = pnl_pct
                pos.pnl = (price - pos.avg_cost) * pos.shares
                pos.holding_days += 1
                
                if pnl_pct < -self.params['stop_loss']:
                    self._sell(stock, date, price, "止损")
                elif pnl_pct > self.params['take_profit']:
                    self._sell(stock, date, price, "止盈")
                elif pos.holding_days > 60 and pnl_pct < 0.05:
                    self._sell(stock, date, price, "超时")
            except:
                pass
        
        # 调仓
        curr_inv = sum(p.current_price * p.shares for p in self.positions.values())
        if curr_inv > target_inv * 1.1:
            for stock in sorted(self.positions.keys(), key=lambda x: self.positions[x].pnl_pct):
                if curr_inv <= target_inv: break
                try:
                    p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                    if p is not None and len(p) > 0:
                        self._sell(stock, date, p['close'].iloc[-1], "减仓")
                        curr_inv -= self.positions.get(stock, PositionInfo("",0,0,0,0,0,0,"")).current_price * self.positions.get(stock, PositionInfo("",0,0,0,0,0,0,"")).shares
                except:
                    pass
        
        # 买入
        if len(self.positions) < self.params['max_stocks'] and self.cash > total_val * 0.1:
            for stock, score in candidates:
                if stock in self.positions or len(self.positions) >= self.params['max_stocks']:
                    continue
                try:
                    p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                    if p is None or len(p) == 0: continue
                    price = p['close'].iloc[-1]
                    max_amt = total_val * self.params['single_stock_max']
                    shares = int(min(max_amt, self.cash * 0.9) / price / 100) * 100
                    if shares >= 100:
                        self._buy(stock, date, price, shares, f"得分{score:.0f}")
                except:
                    pass

    def _buy(self, stock: str, date: str, price: float, shares: int, reason: str):
        value = price * shares
        if value > self.cash: return
        self.cash -= value
        self.positions[stock] = PositionInfo(stock, shares, price, price, 0, 0, 0, date)
        self.trades.append(TradeRecord(date, stock, "BUY", price, shares, value, reason))
        logger.info(f"[{date}] 买入 {stock} @{price:.2f} x{shares} ({reason})")

    def _sell(self, stock: str, date: str, price: float, reason: str):
        if stock not in self.positions: return
        pos = self.positions[stock]
        value = price * pos.shares
        self.cash += value
        pnl = (price - pos.avg_cost) * pos.shares
        self.trades.append(TradeRecord(date, stock, "SELL", price, pos.shares, value, reason))
        logger.info(f"[{date}] 卖出 {stock} @{price:.2f} 盈亏{pnl:.0f} ({reason})")
        del self.positions[stock]

    def get_total_value(self, date: str) -> float:
        self._ensure_jqdata()
        total = self.cash
        for stock, pos in self.positions.items():
            try:
                p = self._jq.get_price(stock, end_date=date, count=1, fields=['close'])
                total += (p['close'].iloc[-1] if p is not None and len(p) > 0 else pos.current_price) * pos.shares
            except:
                total += pos.current_price * pos.shares
        return total

    def run_backtest(self, start_date: str, end_date: str) -> BacktestResult:
        logger.info(f"开始回测: {start_date} 至 {end_date}")
        logger.info(f"冷却期={self.params['regime_cooldown']}天, 确认={self.params['regime_confirm_days']}天")
        
        self._ensure_jqdata()
        self.positions = {}
        self.cash = self.initial_capital
        self.equity_history = []
        self.trades = []
        self._regime_days_held = 0
        self._pending_regime = None
        self._pending_regime_count = 0
        self._last_check_index = -999
        
        trade_days = self._jq.get_trade_days(start_date=start_date, end_date=end_date)
        regime_returns = {r: [] for r in ['BULL', 'BEAR', 'VOLATILE', 'RECOVERY', 'DISTRIBUTION']}
        prev_value = self.initial_capital
        
        for i, td in enumerate(trade_days):
            date = td.strftime("%Y-%m-%d") if hasattr(td, 'strftime') else str(td)
            
            # 环境检测（带冷却期）
            regime, changed, reason = self.detect_market_regime(date, i)
            
            # 只在真正切换或首次时输出
            if changed or i == 0:
                logger.info(f"[{date}] 环境: {regime} | {reason}")
            
            if i % 5 == 0:
                candidates = self.select_stocks(date)
            else:
                candidates = []
            
            self.execute_trades(date, candidates)
            
            total = self.get_total_value(date)
            self.equity_history.append((date, total))
            regime_returns[self.current_regime].append((total / prev_value - 1) if prev_value > 0 else 0)
            prev_value = total
            
            if i % 20 == 0:
                ret = (total / self.initial_capital - 1) * 100
                logger.info(f"[{date}] 净值:{total:.0f} 收益:{ret:.1f}% 环境:{self.current_regime} 持续:{self._regime_days_held}天")
        
        return self._calc_result(regime_returns)

    def _calc_result(self, regime_returns: Dict[str, List[float]]) -> BacktestResult:
        if not self.equity_history:
            return BacktestResult(0, 0, 0, 0, 0, 0, 0)
        
        dates = [x[0] for x in self.equity_history]
        values = [x[1] for x in self.equity_history]
        
        df = pd.DataFrame({'date': dates, 'equity': values})
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df['return'] = df['equity'].pct_change()
        
        total_ret = (values[-1] / self.initial_capital - 1) * 100
        years = len(values) / 252
        annual_ret = ((values[-1] / self.initial_capital) ** (1/years) - 1) * 100 if years > 0 else 0
        
        rets = df['return'].dropna()
        sharpe = np.sqrt(252) * rets.mean() / rets.std() if len(rets) > 0 and rets.std() > 0 else 0
        
        df['cummax'] = df['equity'].cummax()
        df['dd'] = (df['cummax'] - df['equity']) / df['cummax']
        max_dd = df['dd'].max() * 100
        
        wins = len([t for t in self.trades if t.action == 'SELL' and 
                   any(b.stock == t.stock and b.action == 'BUY' and b.price < t.price for b in self.trades)])
        total_sells = len([t for t in self.trades if t.action == 'SELL'])
        win_rate = wins / total_sells * 100 if total_sells > 0 else 0
        
        regime_perf = {r: sum(rets) * 100 for r, rets in regime_returns.items() if rets}
        
        return BacktestResult(
            total_return=total_ret, annualized_return=annual_ret, sharpe_ratio=sharpe,
            max_drawdown=max_dd, win_rate=win_rate, profit_factor=0, total_trades=len(self.trades),
            equity_curve=df, trades=self.trades, regime_performance=regime_perf
        )


def main():
    strategy = TenBagger5X2YearStrategy()
    result = strategy.run_backtest("2022-01-01", "2024-12-31")
    
    print("\n" + "="*60)
    print("两年5倍回报策略 - 回测结果")
    print("="*60)
    print(f"总收益率: {result.total_return:.2f}%")
    print(f"年化收益率: {result.annualized_return:.2f}%")
    print(f"夏普比率: {result.sharpe_ratio:.2f}")
    print(f"最大回撤: {result.max_drawdown:.2f}%")
    print(f"胜率: {result.win_rate:.1f}%")
    print(f"总交易: {result.total_trades}")
    print("\n各环境收益:")
    for r, ret in result.regime_performance.items():
        print(f"  {r}: {ret:.2f}%")


if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
TenBagger 5X 2Year Strategy - 两年5倍回报策略（优化版）
======================================================

市场环境判断优化：
- 冷却期：环境切换后保持20个交易日
- 确认机制：新环境需连续5天符合条件
- 定期检查：每月初才评估，避免频繁切换
"""

import sys
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass, field

# 导入优化后的市场环境判断模块
try:
    from core.market_regime.comprehensive_regime_detector import (
        ComprehensiveRegimeDetector, MarketRegime, detect_market_regime
    )
    USE_COMPREHENSIVE_REGIME = True
except ImportError:
    USE_COMPREHENSIVE_REGIME = False

PROJECT_ROOT = "/home/taotao/dev/QuantTest/TRQuant"
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TradeRecord:
    date: str
    stock: str
    action: str
    price: float
    shares: int
    value: float
    reason: str


@dataclass
class PositionInfo:
    stock: str
    shares: int
    avg_cost: float
    current_price: float
    pnl: float
    pnl_pct: float
    holding_days: int
    entry_date: str


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
    trades: List[TradeRecord] = field(default_factory=list)
    monthly_returns: pd.Series = None
    regime_performance: Dict[str, float] = field(default_factory=dict)


class TenBagger5X2YearStrategy:
    """两年5倍回报策略（含市场环境冷却期机制）"""
    
    def __init__(self):
        self._jq = None
        self.params = {
            'regime_cooldown': 20,       # 冷却期天数
            'regime_confirm_days': 5,    # 确认天数
            'regime_check_interval': 20, # 检查间隔
            'max_stocks': 5,
            'single_stock_max': 0.25,
            'stop_loss': 0.12,
            'take_profit': 0.50,
            'min_market_cap': 30e8,
            'max_market_cap': 1000e8,
        }
        self.positions: Dict[str, PositionInfo] = {}
        self.cash = 1000000.0
        self.initial_capital = 1000000.0
        self.equity_history = []
        self.trades = []
        self.current_regime = "VOLATILE"
        
        # 冷却期状态
        self._regime_days_held = 0
        self._pending_regime = None
        self._pending_regime_count = 0
        self._last_check_index = -999

    def _ensure_jqdata(self):
        if self._jq is None:
            import jqdatasdk as jq
            import json
            with open(f"{PROJECT_ROOT}/config/jqdata_config.json") as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self._jq = jq
            logger.info(f"JQData认证成功: {config['username']}")

    def _calc_raw_regime(self, date: str) -> str:
        """计算原始市场环境"""
        self._ensure_jqdata()
        jq = self._jq
        try:
            end = datetime.strptime(date, "%Y-%m-%d")
            start = end - timedelta(days=120)
            df = jq.get_price("000001.XSHG", start_date=start.strftime("%Y-%m-%d"),
                             end_date=date, frequency='daily', fields=['close', 'volume'])
            if df is None or len(df) < 60:
                return "VOLATILE"
            
            close = df['close'].values
            volume = df['volume'].values
            ma20 = np.mean(close[-20:])
            ma60 = np.mean(close[-60:])
            current = close[-1]
            mom_20 = (current / close[-20] - 1) * 100
            mom_60 = (current / close[-60] - 1) * 100
            returns = np.diff(np.log(close[-30:]))
            volatility = np.std(returns) * np.sqrt(252) * 100
            vol_ratio = np.mean(volume[-5:]) / np.mean(volume[-20:])
            
            score = 0
            if current > ma20 > ma60: score += 30
            elif current < ma20 < ma60: score -= 30
            score += min(20, max(-20, mom_20 * 2))
            score += min(10, max(-10, mom_60))
            if volatility < 15: score += 10
            elif volatility > 30: score -= 10
            if vol_ratio > 1.2: score += 10
            elif vol_ratio < 0.8: score -= 10
            
            if score > 30:
                return "DISTRIBUTION" if mom_20 > 20 else "BULL"
            elif score < -30:
                return "RECOVERY" if mom_20 < -20 and volatility < 20 else "BEAR"
            return "VOLATILE"
        except Exception as e:
            logger.error(f"计算环境失败: {e}")
            return "VOLATILE"

    def detect_market_regime(self, date: str, idx: int) -> Tuple[str, bool, str]:
        """检测市场环境（带冷却期和确认机制）"""
        self._regime_days_held += 1
        cooldown = self.params['regime_cooldown']
        confirm = self.params['regime_confirm_days']
        interval = self.params['regime_check_interval']
        
        # 冷却期内不检查
        if self._regime_days_held < cooldown:
            return self.current_regime, False, f"冷却期({self._regime_days_held}/{cooldown})"
        
        # 非检查周期
        if idx - self._last_check_index < interval:
            return self.current_regime, False, "非检查周期"
        
        self._last_check_index = idx
        new_regime = self._calc_raw_regime(date)
        
        if new_regime == self.current_regime:
            self._pending_regime = None
            self._pending_regime_count = 0
            return self.current_regime, False, f"环境稳定({self.current_regime})"
        
        if self._pending_regime == new_regime:
            self._pending_regime_count += 1
        else:
            self._pending_regime = new_regime
            self._pending_regime_count = 1
        
        if self._pending_regime_count >= confirm:
            old = self.current_regime
            self.current_regime = new_regime
            self._regime_days_held = 0
            self._pending_regime = None
            self._pending_regime_count = 0
            reason = f"切换: {old}->{new_regime} (确认{confirm}天)"
            logger.info(f"[{date}] *** 环境{reason}")
            return self.current_regime, True, reason
        
        return self.current_regime, False, f"待确认:{new_regime}({self._pending_regime_count}/{confirm})"

    def get_universe(self, date: str) -> List[str]:
        self._ensure_jqdata()
        try:
            from jqdatasdk import query, valuation
            q = query(valuation.code).filter(
                valuation.market_cap > self.params['min_market_cap'] / 1e8,
                valuation.market_cap < self.params['max_market_cap'] / 1e8,
                valuation.pe_ratio > 0, valuation.pe_ratio < 100
            ).order_by(valuation.market_cap.desc()).limit(300)
            df = self._jq.get_fundamentals(q, date=date)
            return df['code'].tolist() if df is not None else []
        except:
            return []

    def score_stock(self, stock: str, date: str) -> float:
        self._ensure_jqdata()
        try:
            end = datetime.strptime(date, "%Y-%m-%d")
            start = end - timedelta(days=120)
            df = self._jq.get_price(stock, start_date=start.strftime("%Y-%m-%d"),
                                   end_date=date, frequency='daily', fields=['close', 'volume'])
            if df is None or len(df) < 60:
                return 0.0
            
            close = df['close'].values
            score = 50.0
            mom_20 = (close[-1] / close[-20] - 1) * 100
            if 5 < mom_20 < 30: score += 10
            elif mom_20 > 50: score -= 5
            elif mom_20 < -10: score -= 10
            
            from jqdatasdk import query, indicator
            q = query(indicator.inc_revenue_year_on_year, indicator.inc_net_profit_year_on_year,
                     indicator.roe).filter(indicator.code == stock)
            fund = self._jq.get_fundamentals(q, date=date)
            if fund is not None and len(fund) > 0:
                rev = fund['inc_revenue_year_on_year'].iloc[0] or 0
                profit = fund['inc_net_profit_year_on_year'].iloc[0] or 0
                roe = fund['roe'].iloc[0] or 0
                if rev > 30: score += 10
                elif rev > 15: score += 5
                if profit > 50: score += 10
                elif profit > 20: score += 5
                if roe > 15: score += 5
            
            return max(0, min(100, score))
        except:
            return 0.0

    def select_stocks(self, date: str) -> List[Tuple[str, float]]:
        universe = self.get_universe(date)
        scores = [(s, self.score_stock(s, date)) for s in universe[:100]]
        scores = [(s, sc) for s, sc in scores if sc > 60]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:self.params['max_stocks'] * 2]

    def get_target_position(self) -> float:
        return {'BULL': 0.85, 'RECOVERY': 0.70, 'VOLATILE': 0.50,
                'DISTRIBUTION': 0.35, 'BEAR': 0.15}.get(self.current_regime, 0.5)

    def execute_trades(self, date: str, candidates: List[Tuple[str, float]]):
        self._ensure_jqdata()
        jq = self._jq
        target_pos = self.get_target_position()
        total_val = self.get_total_value(date)
        target_inv = total_val * target_pos
        
        # 止损止盈
        for stock, pos in list(self.positions.items()):
            try:
                p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                if p is None or len(p) == 0: continue
                price = p['close'].iloc[-1]
                pnl_pct = price / pos.avg_cost - 1
                pos.current_price = price
                pos.pnl_pct = pnl_pct
                pos.pnl = (price - pos.avg_cost) * pos.shares
                pos.holding_days += 1
                
                if pnl_pct < -self.params['stop_loss']:
                    self._sell(stock, date, price, "止损")
                elif pnl_pct > self.params['take_profit']:
                    self._sell(stock, date, price, "止盈")
                elif pos.holding_days > 60 and pnl_pct < 0.05:
                    self._sell(stock, date, price, "超时")
            except:
                pass
        
        # 调仓
        curr_inv = sum(p.current_price * p.shares for p in self.positions.values())
        if curr_inv > target_inv * 1.1:
            for stock in sorted(self.positions.keys(), key=lambda x: self.positions[x].pnl_pct):
                if curr_inv <= target_inv: break
                try:
                    p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                    if p is not None and len(p) > 0:
                        self._sell(stock, date, p['close'].iloc[-1], "减仓")
                        curr_inv -= self.positions.get(stock, PositionInfo("",0,0,0,0,0,0,"")).current_price * self.positions.get(stock, PositionInfo("",0,0,0,0,0,0,"")).shares
                except:
                    pass
        
        # 买入
        if len(self.positions) < self.params['max_stocks'] and self.cash > total_val * 0.1:
            for stock, score in candidates:
                if stock in self.positions or len(self.positions) >= self.params['max_stocks']:
                    continue
                try:
                    p = jq.get_price(stock, end_date=date, count=1, fields=['close'])
                    if p is None or len(p) == 0: continue
                    price = p['close'].iloc[-1]
                    max_amt = total_val * self.params['single_stock_max']
                    shares = int(min(max_amt, self.cash * 0.9) / price / 100) * 100
                    if shares >= 100:
                        self._buy(stock, date, price, shares, f"得分{score:.0f}")
                except:
                    pass

    def _buy(self, stock: str, date: str, price: float, shares: int, reason: str):
        value = price * shares
        if value > self.cash: return
        self.cash -= value
        self.positions[stock] = PositionInfo(stock, shares, price, price, 0, 0, 0, date)
        self.trades.append(TradeRecord(date, stock, "BUY", price, shares, value, reason))
        logger.info(f"[{date}] 买入 {stock} @{price:.2f} x{shares} ({reason})")

    def _sell(self, stock: str, date: str, price: float, reason: str):
        if stock not in self.positions: return
        pos = self.positions[stock]
        value = price * pos.shares
        self.cash += value
        pnl = (price - pos.avg_cost) * pos.shares
        self.trades.append(TradeRecord(date, stock, "SELL", price, pos.shares, value, reason))
        logger.info(f"[{date}] 卖出 {stock} @{price:.2f} 盈亏{pnl:.0f} ({reason})")
        del self.positions[stock]

    def get_total_value(self, date: str) -> float:
        self._ensure_jqdata()
        total = self.cash
        for stock, pos in self.positions.items():
            try:
                p = self._jq.get_price(stock, end_date=date, count=1, fields=['close'])
                total += (p['close'].iloc[-1] if p is not None and len(p) > 0 else pos.current_price) * pos.shares
            except:
                total += pos.current_price * pos.shares
        return total

    def run_backtest(self, start_date: str, end_date: str) -> BacktestResult:
        logger.info(f"开始回测: {start_date} 至 {end_date}")
        logger.info(f"冷却期={self.params['regime_cooldown']}天, 确认={self.params['regime_confirm_days']}天")
        
        self._ensure_jqdata()
        self.positions = {}
        self.cash = self.initial_capital
        self.equity_history = []
        self.trades = []
        self._regime_days_held = 0
        self._pending_regime = None
        self._pending_regime_count = 0
        self._last_check_index = -999
        
        trade_days = self._jq.get_trade_days(start_date=start_date, end_date=end_date)
        regime_returns = {r: [] for r in ['BULL', 'BEAR', 'VOLATILE', 'RECOVERY', 'DISTRIBUTION']}
        prev_value = self.initial_capital
        
        for i, td in enumerate(trade_days):
            date = td.strftime("%Y-%m-%d") if hasattr(td, 'strftime') else str(td)
            
            # 环境检测（带冷却期）
            regime, changed, reason = self.detect_market_regime(date, i)
            
            # 只在真正切换或首次时输出
            if changed or i == 0:
                logger.info(f"[{date}] 环境: {regime} | {reason}")
            
            if i % 5 == 0:
                candidates = self.select_stocks(date)
            else:
                candidates = []
            
            self.execute_trades(date, candidates)
            
            total = self.get_total_value(date)
            self.equity_history.append((date, total))
            regime_returns[self.current_regime].append((total / prev_value - 1) if prev_value > 0 else 0)
            prev_value = total
            
            if i % 20 == 0:
                ret = (total / self.initial_capital - 1) * 100
                logger.info(f"[{date}] 净值:{total:.0f} 收益:{ret:.1f}% 环境:{self.current_regime} 持续:{self._regime_days_held}天")
        
        return self._calc_result(regime_returns)

    def _calc_result(self, regime_returns: Dict[str, List[float]]) -> BacktestResult:
        if not self.equity_history:
            return BacktestResult(0, 0, 0, 0, 0, 0, 0)
        
        dates = [x[0] for x in self.equity_history]
        values = [x[1] for x in self.equity_history]
        
        df = pd.DataFrame({'date': dates, 'equity': values})
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df['return'] = df['equity'].pct_change()
        
        total_ret = (values[-1] / self.initial_capital - 1) * 100
        years = len(values) / 252
        annual_ret = ((values[-1] / self.initial_capital) ** (1/years) - 1) * 100 if years > 0 else 0
        
        rets = df['return'].dropna()
        sharpe = np.sqrt(252) * rets.mean() / rets.std() if len(rets) > 0 and rets.std() > 0 else 0
        
        df['cummax'] = df['equity'].cummax()
        df['dd'] = (df['cummax'] - df['equity']) / df['cummax']
        max_dd = df['dd'].max() * 100
        
        wins = len([t for t in self.trades if t.action == 'SELL' and 
                   any(b.stock == t.stock and b.action == 'BUY' and b.price < t.price for b in self.trades)])
        total_sells = len([t for t in self.trades if t.action == 'SELL'])
        win_rate = wins / total_sells * 100 if total_sells > 0 else 0
        
        regime_perf = {r: sum(rets) * 100 for r, rets in regime_returns.items() if rets}
        
        return BacktestResult(
            total_return=total_ret, annualized_return=annual_ret, sharpe_ratio=sharpe,
            max_drawdown=max_dd, win_rate=win_rate, profit_factor=0, total_trades=len(self.trades),
            equity_curve=df, trades=self.trades, regime_performance=regime_perf
        )


def main():
    strategy = TenBagger5X2YearStrategy()
    result = strategy.run_backtest("2022-01-01", "2024-12-31")
    
    print("\n" + "="*60)
    print("两年5倍回报策略 - 回测结果")
    print("="*60)
    print(f"总收益率: {result.total_return:.2f}%")
    print(f"年化收益率: {result.annualized_return:.2f}%")
    print(f"夏普比率: {result.sharpe_ratio:.2f}")
    print(f"最大回撤: {result.max_drawdown:.2f}%")
    print(f"胜率: {result.win_rate:.1f}%")
    print(f"总交易: {result.total_trades}")
    print("\n各环境收益:")
    for r, ret in result.regime_performance.items():
        print(f"  {r}: {ret:.2f}%")


if __name__ == "__main__":
    main()






































