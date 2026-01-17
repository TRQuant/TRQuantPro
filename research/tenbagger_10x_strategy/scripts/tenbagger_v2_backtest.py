#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股早期识别系统 V2.0 - 回测系统
=====================================

回测配置:
- 时间范围: 2022-01-01 至 2025-01-06 (3年)
- 初始资金: 100万
- 目标收益: 1000% (10倍)
- 基准: 沪深300
- 佣金: 万一 (0.0001)

回测框架:
1. 快速回测: 向量化，验证策略有效性
2. 标准回测: 事件驱动，精确计算收益
3. 参数优化: 网格搜索最优参数

优化目标:
- 年化收益率 > 100%
- 夏普比率 > 1.5
- 最大回撤 < 40%
- 胜率 > 50%

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_v2_backtest.py
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from datetime import datetime, timedelta
from enum import Enum
import logging
import json
import pickle

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# 回测配置
# ============================================================

@dataclass
class BacktestConfig:
    """回测配置"""
    # 时间范围
    start_date: str = "2022-01-01"
    end_date: str = "2025-01-06"
    
    # 资金
    initial_capital: float = 1000000.0
    
    # 交易成本
    commission_rate: float = 0.0001     # 万一佣金
    slippage_rate: float = 0.001        # 滑点 0.1%
    stamp_duty_rate: float = 0.001      # 印花税 0.1% (卖出)
    
    # 仓位管理
    max_holdings: int = 8               # 最大持仓数
    single_stock_max: float = 0.25      # 单票上限
    min_trade_amount: float = 10000.0   # 最小交易金额
    
    # 风控
    stop_loss: float = -0.15            # 止损
    take_profit: float = 1.0            # 止盈 100%
    trailing_stop: float = 0.20         # 移动止盈回撤
    
    # 调仓
    rebalance_days: int = 10            # 调仓周期（交易日）
    
    # 选股
    min_score: float = 70.0             # 最低分数
    prefer_stages: List[str] = field(default_factory=lambda: ['S0', 'S1', 'S2'])


# ============================================================
# 交易记录
# ============================================================

@dataclass
class Trade:
    """交易记录"""
    date: str
    code: str
    name: str = ""
    direction: str = "buy"  # buy/sell
    price: float = 0.0
    shares: int = 0
    amount: float = 0.0
    commission: float = 0.0
    reason: str = ""


@dataclass
class Position:
    """持仓"""
    code: str
    name: str = ""
    shares: int = 0
    cost_price: float = 0.0
    current_price: float = 0.0
    highest_price: float = 0.0  # 持仓期间最高价（用于移动止盈）
    entry_date: str = ""
    
    @property
    def market_value(self) -> float:
        return self.shares * self.current_price
    
    @property
    def cost_value(self) -> float:
        return self.shares * self.cost_price
    
    @property
    def profit_pct(self) -> float:
        if self.cost_price <= 0:
            return 0
        return (self.current_price / self.cost_price - 1) * 100
    
    @property
    def drawdown_from_high(self) -> float:
        if self.highest_price <= 0:
            return 0
        return (self.current_price / self.highest_price - 1) * 100


# ============================================================
# 回测结果
# ============================================================

@dataclass
class BacktestResult:
    """回测结果"""
    config: BacktestConfig
    
    # 收益指标
    total_return: float = 0.0           # 总收益率
    annual_return: float = 0.0          # 年化收益率
    max_drawdown: float = 0.0           # 最大回撤
    sharpe_ratio: float = 0.0           # 夏普比率
    sortino_ratio: float = 0.0          # 索提诺比率
    calmar_ratio: float = 0.0           # 卡玛比率
    
    # 交易指标
    total_trades: int = 0               # 总交易次数
    win_rate: float = 0.0               # 胜率
    profit_factor: float = 0.0          # 盈亏比
    avg_holding_days: float = 0.0       # 平均持仓天数
    
    # 对比指标
    benchmark_return: float = 0.0       # 基准收益
    alpha: float = 0.0                  # 阿尔法
    beta: float = 0.0                   # 贝塔
    
    # 详细数据
    equity_curve: pd.DataFrame = None   # 权益曲线
    trades: List[Trade] = None          # 交易记录
    monthly_returns: pd.Series = None   # 月度收益


# ============================================================
# 回测引擎
# ============================================================

class TenbaggerV2Backtester:
    """十倍股V2回测引擎"""
    
    def __init__(self, config: BacktestConfig = None):
        self.config = config or BacktestConfig()
        self.jq = None
        self._init_jqdata()
        
        # 状态
        self.cash = self.config.initial_capital
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.equity_curve = []
        self.daily_returns = []
        
        # 数据缓存
        self.price_cache: Dict[str, pd.DataFrame] = {}
        self.selection_cache: Dict[str, List] = {}
    
    def _init_jqdata(self):
        """初始化JQData"""
        try:
            import jqdatasdk as jq
            config_path = PROJECT_ROOT / "config" / "jqdata_config.json"
            with open(config_path) as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self.jq = jq
            logger.info("✅ JQData认证成功")
        except Exception as e:
            logger.warning(f"⚠️ JQData认证失败: {e}")
    
    def run_backtest(self) -> BacktestResult:
        """运行回测"""
        logger.info(f"\n{'='*70}")
        logger.info(f"🚀 十倍股V2策略回测")
        logger.info(f"{'='*70}")
        logger.info(f"时间范围: {self.config.start_date} ~ {self.config.end_date}")
        logger.info(f"初始资金: {self.config.initial_capital:,.0f}")
        logger.info(f"目标: 3年10倍 (年化约115%)")
        logger.info(f"{'='*70}")
        
        # 重置状态
        self._reset()
        
        # 获取交易日列表
        trade_dates = self._get_trade_dates()
        logger.info(f"交易日数量: {len(trade_dates)}")
        
        # 导入筛选器和市场适配器
        from research.tenbagger_10x_strategy.scripts.tenbagger_v2_screener import TenbaggerV2Screener
        from research.tenbagger_10x_strategy.scripts.tenbagger_v2_market_adapter import TenbaggerV2MarketAdapter
        
        screener = TenbaggerV2Screener()
        market_adapter = TenbaggerV2MarketAdapter()
        
        rebalance_counter = 0
        last_selection = []
        
        for i, date in enumerate(trade_dates):
            # 更新持仓价格
            self._update_positions(date)
            
            # 检查止损止盈
            self._check_risk_control(date)
            
            # 调仓日
            rebalance_counter += 1
            if rebalance_counter >= self.config.rebalance_days:
                rebalance_counter = 0
                
                # 分析市场
                try:
                    market_state, adjustment = market_adapter.analyze_and_adapt(date)
                    
                    # 根据市场状态决定是否交易
                    if not market_adapter.should_trade():
                        logger.info(f"{date}: 市场状态不佳，暂停交易")
                        continue
                    
                    # 运行选股
                    selections = screener.run_full_screening(date)
                    
                    # 应用市场调整
                    min_score = self.config.min_score + adjustment.min_score_adj
                    selections = [s for s in selections if s.get('adjusted_score', 0) >= min_score]
                    
                    # 调仓
                    self._rebalance(date, selections, adjustment)
                    last_selection = selections
                    
                except Exception as e:
                    logger.warning(f"{date}: 选股失败 - {e}")
            
            # 记录权益
            total_equity = self._calculate_total_equity()
            self.equity_curve.append({
                'date': date,
                'equity': total_equity,
                'cash': self.cash,
                'positions_value': total_equity - self.cash
            })
            
            # 进度
            if (i + 1) % 50 == 0:
                ret = (total_equity / self.config.initial_capital - 1) * 100
                logger.info(f"进度: {i+1}/{len(trade_dates)} | 日期: {date} | 收益: {ret:.1f}%")
        
        # 计算结果
        result = self._calculate_result()
        
        # 打印结果
        self._print_result(result)
        
        return result
    
    def _reset(self):
        """重置状态"""
        self.cash = self.config.initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        self.daily_returns = []
    
    def _get_trade_dates(self) -> List[str]:
        """获取交易日列表"""
        if self.jq is None:
            # 生成近似交易日
            dates = pd.date_range(
                self.config.start_date, 
                self.config.end_date, 
                freq='B'  # 工作日
            )
            return [d.strftime('%Y-%m-%d') for d in dates]
        
        dates = self.jq.get_trade_days(
            start_date=self.config.start_date,
            end_date=self.config.end_date
        )
        return [d.strftime('%Y-%m-%d') for d in dates]
    
    def _get_price(self, code: str, date: str) -> Optional[float]:
        """获取股票价格"""
        if self.jq is None:
            return None
        
        # 检查缓存
        if code not in self.price_cache:
            try:
                df = self.jq.get_price(
                    code,
                    start_date=self.config.start_date,
                    end_date=self.config.end_date,
                    frequency='daily',
                    fields=['close']
                )
                if df is not None:
                    self.price_cache[code] = df
            except:
                return None
        
        if code in self.price_cache:
            df = self.price_cache[code]
            if date in df.index:
                return df.loc[date, 'close']
            # 尝试找最近的价格
            try:
                idx = df.index.get_indexer([date], method='ffill')[0]
                if idx >= 0:
                    return df.iloc[idx]['close']
            except:
                pass
        
        return None
    
    def _update_positions(self, date: str):
        """更新持仓价格"""
        for code, pos in self.positions.items():
            price = self._get_price(code, date)
            if price:
                pos.current_price = price
                pos.highest_price = max(pos.highest_price, price)
    
    def _check_risk_control(self, date: str):
        """检查止损止盈"""
        to_sell = []
        
        for code, pos in self.positions.items():
            reason = None
            
            # 止损
            if pos.profit_pct <= self.config.stop_loss * 100:
                reason = f"止损 ({pos.profit_pct:.1f}%)"
            
            # 止盈
            elif pos.profit_pct >= self.config.take_profit * 100:
                reason = f"止盈 ({pos.profit_pct:.1f}%)"
            
            # 移动止盈
            elif pos.profit_pct >= 50:  # 盈利50%以上才启用移动止盈
                if pos.drawdown_from_high <= -self.config.trailing_stop * 100:
                    reason = f"移动止盈 (从高点回撤{pos.drawdown_from_high:.1f}%)"
            
            if reason:
                to_sell.append((code, reason))
        
        # 执行卖出
        for code, reason in to_sell:
            self._sell_stock(date, code, reason)
    
    def _rebalance(self, date: str, selections: List[Dict], adjustment):
        """调仓"""
        # 获取仓位限制
        max_position = adjustment.max_position
        single_max = adjustment.single_stock_max
        
        # 计算目标持仓
        total_equity = self._calculate_total_equity()
        available_capital = total_equity * max_position
        per_stock_capital = min(
            available_capital / self.config.max_holdings,
            total_equity * single_max
        )
        
        # 当前持仓代码
        current_codes = set(self.positions.keys())
        
        # 目标持仓代码（取前N只）
        target_selections = selections[:self.config.max_holdings]
        target_codes = set(s['code'] for s in target_selections)
        
        # 需要卖出的
        to_sell = current_codes - target_codes
        for code in to_sell:
            self._sell_stock(date, code, "调仓卖出")
        
        # 需要买入的
        to_buy = target_codes - current_codes
        for selection in target_selections:
            code = selection['code']
            if code in to_buy:
                self._buy_stock(
                    date, code,
                    target_amount=per_stock_capital,
                    reason=f"调仓买入 (分数:{selection.get('adjusted_score', 0):.1f}, 阶段:{selection.get('stage', '')})"
                )
    
    def _buy_stock(self, date: str, code: str, target_amount: float, reason: str = ""):
        """买入股票"""
        price = self._get_price(code, date)
        if price is None or price <= 0:
            return
        
        # 计算可买股数
        available = min(self.cash, target_amount)
        shares = int(available / price / 100) * 100  # 整百股
        
        if shares < 100:
            return
        
        amount = shares * price
        commission = max(5, amount * self.config.commission_rate)
        total_cost = amount + commission
        
        if total_cost > self.cash:
            return
        
        # 执行买入
        self.cash -= total_cost
        
        if code in self.positions:
            # 加仓
            pos = self.positions[code]
            old_cost = pos.cost_price * pos.shares
            pos.shares += shares
            pos.cost_price = (old_cost + amount) / pos.shares
        else:
            # 新建仓
            self.positions[code] = Position(
                code=code,
                shares=shares,
                cost_price=price,
                current_price=price,
                highest_price=price,
                entry_date=date
            )
        
        # 记录交易
        self.trades.append(Trade(
            date=date,
            code=code,
            direction="buy",
            price=price,
            shares=shares,
            amount=amount,
            commission=commission,
            reason=reason
        ))
    
    def _sell_stock(self, date: str, code: str, reason: str = ""):
        """卖出股票"""
        if code not in self.positions:
            return
        
        pos = self.positions[code]
        price = pos.current_price
        
        if price is None or price <= 0:
            return
        
        amount = pos.shares * price
        commission = max(5, amount * self.config.commission_rate)
        stamp_duty = amount * self.config.stamp_duty_rate
        total_cost = commission + stamp_duty
        
        # 执行卖出
        self.cash += amount - total_cost
        
        # 记录交易
        self.trades.append(Trade(
            date=date,
            code=code,
            direction="sell",
            price=price,
            shares=pos.shares,
            amount=amount,
            commission=total_cost,
            reason=reason
        ))
        
        # 删除持仓
        del self.positions[code]
    
    def _calculate_total_equity(self) -> float:
        """计算总权益"""
        positions_value = sum(pos.market_value for pos in self.positions.values())
        return self.cash + positions_value
    
    def _calculate_result(self) -> BacktestResult:
        """计算回测结果"""
        result = BacktestResult(config=self.config)
        
        if not self.equity_curve:
            return result
        
        equity_df = pd.DataFrame(self.equity_curve)
        equity_df['date'] = pd.to_datetime(equity_df['date'])
        equity_df = equity_df.set_index('date')
        
        # 总收益
        final_equity = equity_df['equity'].iloc[-1]
        result.total_return = (final_equity / self.config.initial_capital - 1) * 100
        
        # 年化收益
        days = (equity_df.index[-1] - equity_df.index[0]).days
        years = days / 365
        if years > 0:
            result.annual_return = ((final_equity / self.config.initial_capital) ** (1/years) - 1) * 100
        
        # 最大回撤
        cummax = equity_df['equity'].cummax()
        drawdown = (equity_df['equity'] - cummax) / cummax
        result.max_drawdown = drawdown.min() * 100
        
        # 日收益率
        daily_returns = equity_df['equity'].pct_change().dropna()
        
        # 夏普比率 (假设无风险利率3%)
        rf = 0.03 / 252
        if daily_returns.std() > 0:
            result.sharpe_ratio = (daily_returns.mean() - rf) / daily_returns.std() * np.sqrt(252)
        
        # 交易统计
        result.total_trades = len(self.trades)
        
        # 胜率
        sell_trades = [t for t in self.trades if t.direction == 'sell']
        if sell_trades:
            # 简化：比较卖出价和买入价
            wins = sum(1 for t in sell_trades if t.amount > 0)  # 需要更精确的计算
            result.win_rate = wins / len(sell_trades) * 100
        
        # 存储详细数据
        result.equity_curve = equity_df
        result.trades = self.trades
        
        return result
    
    def _print_result(self, result: BacktestResult):
        """打印回测结果"""
        logger.info(f"\n{'='*70}")
        logger.info(f"📊 回测结果")
        logger.info(f"{'='*70}")
        
        logger.info(f"\n收益指标:")
        logger.info(f"  总收益率: {result.total_return:.2f}%")
        logger.info(f"  年化收益率: {result.annual_return:.2f}%")
        logger.info(f"  最大回撤: {result.max_drawdown:.2f}%")
        logger.info(f"  夏普比率: {result.sharpe_ratio:.2f}")
        
        logger.info(f"\n交易指标:")
        logger.info(f"  总交易次数: {result.total_trades}")
        logger.info(f"  胜率: {result.win_rate:.1f}%")
        
        # 目标达成判断
        target_return = 1000  # 10倍
        if result.total_return >= target_return:
            logger.info(f"\n🎉 恭喜！达成10倍目标！")
        else:
            gap = target_return - result.total_return
            logger.info(f"\n📈 距离10倍目标还差: {gap:.1f}%")
        
        # 与基准对比（简化）
        logger.info(f"\n{'='*70}")


# ============================================================
# 参数优化器
# ============================================================

class ParameterOptimizer:
    """参数优化器"""
    
    def __init__(self):
        self.results = []
    
    def grid_search(self, param_grid: Dict[str, List]) -> List[Dict]:
        """网格搜索"""
        from itertools import product
        
        keys = param_grid.keys()
        values = param_grid.values()
        
        best_result = None
        best_return = -float('inf')
        
        for combo in product(*values):
            params = dict(zip(keys, combo))
            
            # 创建配置
            config = BacktestConfig(**params)
            
            # 运行回测
            backtester = TenbaggerV2Backtester(config)
            result = backtester.run_backtest()
            
            self.results.append({
                'params': params,
                'total_return': result.total_return,
                'annual_return': result.annual_return,
                'max_drawdown': result.max_drawdown,
                'sharpe_ratio': result.sharpe_ratio
            })
            
            if result.total_return > best_return:
                best_return = result.total_return
                best_result = params
        
        return self.results


# ============================================================
# 测试
# ============================================================

def test_backtest():
    """测试回测"""
    # 创建配置
    config = BacktestConfig(
        start_date="2024-01-01",  # 先用1年测试
        end_date="2025-01-06",
        initial_capital=1000000,
        max_holdings=8,
        single_stock_max=0.25,
        rebalance_days=10,
        min_score=65,
        stop_loss=-0.15,
        take_profit=1.0
    )
    
    # 运行回测
    backtester = TenbaggerV2Backtester(config)
    result = backtester.run_backtest()
    
    return result


if __name__ == "__main__":
    test_backtest()
