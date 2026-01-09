"""
V3.0 筛选条件回测验证模块
========================

用于验证筛选条件的历史有效性，支持:
1. 单周期回测
2. 滚动回测
3. 多策略对比
4. 参数敏感性分析

回测指标:
- 总收益率
- 年化收益
- 最大回撤
- 夏普比率
- 胜率
- 盈亏比
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ============ 数据结构 ============

@dataclass
class BacktestMetrics:
    """回测指标"""
    total_return: float = 0.0          # 总收益率
    annual_return: float = 0.0          # 年化收益
    max_drawdown: float = 0.0           # 最大回撤
    sharpe_ratio: float = 0.0           # 夏普比率
    sortino_ratio: float = 0.0          # 索提诺比率
    calmar_ratio: float = 0.0           # 卡尔玛比率
    win_rate: float = 0.0               # 胜率
    profit_factor: float = 0.0          # 盈亏比
    trade_count: int = 0                # 交易次数
    avg_holding_days: float = 0.0       # 平均持仓天数
    
    def to_dict(self) -> Dict:
        return {
            "total_return": round(self.total_return * 100, 2),
            "annual_return": round(self.annual_return * 100, 2),
            "max_drawdown": round(self.max_drawdown * 100, 2),
            "sharpe_ratio": round(self.sharpe_ratio, 2),
            "sortino_ratio": round(self.sortino_ratio, 2),
            "calmar_ratio": round(self.calmar_ratio, 2),
            "win_rate": round(self.win_rate * 100, 1),
            "profit_factor": round(self.profit_factor, 2),
            "trade_count": self.trade_count,
            "avg_holding_days": round(self.avg_holding_days, 1),
        }
    
    def __str__(self) -> str:
        return f"""
收益: {self.total_return*100:.1f}% | 年化: {self.annual_return*100:.1f}%
回撤: {self.max_drawdown*100:.1f}% | 夏普: {self.sharpe_ratio:.2f}
胜率: {self.win_rate*100:.1f}% | 盈亏比: {self.profit_factor:.2f}
交易: {self.trade_count}次 | 持仓: {self.avg_holding_days:.0f}天
""".strip()


@dataclass
class TradeRecord:
    """交易记录"""
    stock_code: str
    stock_name: str
    entry_date: str
    entry_price: float
    exit_date: str
    exit_price: float
    return_pct: float
    holding_days: int
    exit_reason: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "stock_code": self.stock_code,
            "stock_name": self.stock_name,
            "entry_date": self.entry_date,
            "entry_price": round(self.entry_price, 2),
            "exit_date": self.exit_date,
            "exit_price": round(self.exit_price, 2),
            "return_pct": round(self.return_pct * 100, 2),
            "holding_days": self.holding_days,
            "exit_reason": self.exit_reason,
        }


@dataclass
class BacktestResult:
    """回测结果"""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    metrics: BacktestMetrics
    trades: List[TradeRecord] = field(default_factory=list)
    equity_curve: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "strategy_name": self.strategy_name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "initial_capital": self.initial_capital,
            "final_capital": round(self.final_capital, 2),
            "metrics": self.metrics.to_dict(),
            "trade_count": len(self.trades),
        }


# ============ 回测引擎 ============

class BacktestVerifierV3:
    """
    V3.0 筛选条件回测验证器
    
    用于验证 FilterOptionsV3 筛选条件的历史有效性
    """
    
    def __init__(
        self,
        initial_capital: float = 1000000,
        max_positions: int = 10,
        position_size: float = 0.10,
        stop_loss: float = 0.10,
        take_profit: float = 0.30,
        holding_period: int = 30,
    ):
        """
        初始化
        
        Args:
            initial_capital: 初始资金
            max_positions: 最大持仓数
            position_size: 单只股票仓位
            stop_loss: 止损比例
            take_profit: 止盈比例
            holding_period: 默认持仓周期 (天)
        """
        self.initial_capital = initial_capital
        self.max_positions = max_positions
        self.position_size = position_size
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.holding_period = holding_period
        
        self._jq_client = None
    
    def _ensure_jq_client(self):
        """确保JQData客户端已初始化"""
        if self._jq_client is None:
            try:
                from jqdata.client import JQDataClient
                self._jq_client = JQDataClient()
            except Exception as e:
                logger.error(f"JQData初始化失败: {e}")
                raise
    
    def run_backtest(
        self,
        filter_options,
        start_date: str,
        end_date: str,
        rebalance_freq: int = 30,
        strategy_name: str = "V3筛选策略",
    ) -> BacktestResult:
        """
        执行回测
        
        Args:
            filter_options: FilterOptionsV3 筛选选项
            start_date: 开始日期 YYYY-MM-DD
            end_date: 结束日期 YYYY-MM-DD
            rebalance_freq: 调仓频率 (天)
            strategy_name: 策略名称
            
        Returns:
            BacktestResult 回测结果
        """
        from .filter_options_v3 import StockFilterV3, FilterOptionsV3
        
        self._ensure_jq_client()
        
        logger.info(f"BacktestVerifierV3: 开始回测 {start_date} ~ {end_date}")
        
        # 初始化
        capital = self.initial_capital
        positions = {}  # {stock_code: {"entry_date", "entry_price", "shares"}}
        trades = []
        equity_curve = []
        
        # 获取交易日序列
        trade_dates = self._get_trade_dates(start_date, end_date)
        
        filter_v3 = StockFilterV3(filter_options)
        
        # 遍历交易日
        for i, date in enumerate(trade_dates):
            date_str = date.strftime("%Y-%m-%d")
            
            # 检查止损止盈
            capital, closed_trades = self._check_stop_orders(
                positions, date_str, capital
            )
            trades.extend(closed_trades)
            
            # 调仓日
            if i % rebalance_freq == 0:
                # 获取当日股票数据
                stocks_data = self._get_stocks_data(date_str)
                
                if stocks_data:
                    # 筛选股票
                    filtered = filter_v3.filter_stocks(stocks_data)
                    
                    # 执行调仓
                    capital, new_trades = self._rebalance(
                        positions, filtered, date_str, capital
                    )
                    trades.extend(new_trades)
            
            # 记录净值
            nav = self._calculate_nav(positions, date_str, capital)
            equity_curve.append({
                "date": date_str,
                "nav": nav,
                "capital": capital,
                "positions": len(positions),
            })
        
        # 清仓
        end_date_str = trade_dates[-1].strftime("%Y-%m-%d")
        capital, final_trades = self._close_all_positions(
            positions, end_date_str, capital
        )
        trades.extend(final_trades)
        
        # 计算指标
        metrics = self._calculate_metrics(trades, equity_curve)
        
        return BacktestResult(
            strategy_name=strategy_name,
            start_date=start_date,
            end_date=end_date,
            initial_capital=self.initial_capital,
            final_capital=capital,
            metrics=metrics,
            trades=trades,
            equity_curve=equity_curve,
        )
    
    def _get_trade_dates(self, start_date: str, end_date: str) -> List[datetime]:
        """获取交易日序列"""
        try:
            import jqdatasdk as jq
            dates = jq.get_trade_days(start_date, end_date)
            return [pd.to_datetime(d) for d in dates]
        except Exception as e:
            logger.warning(f"获取交易日失败: {e}, 使用工作日代替")
            dates = pd.date_range(start_date, end_date, freq='B')
            return dates.tolist()
    
    def _get_stocks_data(self, date: str) -> List[Dict]:
        """获取股票数据"""
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation, indicator
            
            # 获取基本面数据
            q = query(
                valuation.code,
                valuation.market_cap,
                valuation.pe_ratio,
                indicator.roe,
                indicator.inc_net_profit_year_on_year,
                indicator.inc_revenue_year_on_year,
            ).filter(
                valuation.market_cap > 0
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df is None or df.empty:
                return []
            
            # 获取价格数据
            stocks = df['code'].tolist()[:500]  # 限制数量
            
            price_df = jq.get_price(
                stocks,
                end_date=date,
                count=60,
                fields=['close', 'volume', 'high', 'low'],
                skip_paused=True,
            )
            
            result = []
            for _, row in df.iterrows():
                stock_code = row['code']
                
                try:
                    if stock_code in price_df:
                        prices = price_df[stock_code] if isinstance(price_df, dict) else price_df.xs(stock_code, level='code') if hasattr(price_df, 'xs') else None
                        
                        if prices is not None and len(prices) >= 20:
                            close = prices['close'].iloc[-1]
                            close_20d = prices['close'].iloc[-20]
                            close_5d = prices['close'].iloc[-5]
                            high_60d = prices['high'].max()
                            low_60d = prices['low'].min()
                            vol_20d = prices['volume'].iloc[-20:].mean()
                            
                            stock_data = {
                                "code": stock_code,
                                "name": "",
                                "market_cap": row.get('market_cap', 0),
                                "pe_ratio": row.get('pe_ratio', 0),
                                "roe": row.get('roe', 0) / 100 if row.get('roe') else 0,
                                "profit_growth": row.get('inc_net_profit_year_on_year', 0) / 100 if row.get('inc_net_profit_year_on_year') else 0,
                                "revenue_growth": row.get('inc_revenue_year_on_year', 0) / 100 if row.get('inc_revenue_year_on_year') else 0,
                                "mom_5d": (close - close_5d) / close_5d if close_5d > 0 else 0,
                                "mom_20d": (close - close_20d) / close_20d if close_20d > 0 else 0,
                                "price_pos_60d": (close - low_60d) / (high_60d - low_60d) if high_60d > low_60d else 0.5,
                                "vol_ratio": prices['volume'].iloc[-1] / vol_20d if vol_20d > 0 else 1,
                                "above_ma20": close > prices['close'].iloc[-20:].mean(),
                                "close": close,
                            }
                            result.append(stock_data)
                except Exception as e:
                    continue
            
            return result
            
        except Exception as e:
            logger.error(f"获取股票数据失败: {e}")
            return []
    
    def _check_stop_orders(
        self,
        positions: Dict,
        date: str,
        capital: float,
    ) -> Tuple[float, List[TradeRecord]]:
        """检查止损止盈"""
        trades = []
        to_close = []
        
        for stock_code, pos in positions.items():
            try:
                current_price = self._get_current_price(stock_code, date)
                if current_price is None:
                    continue
                
                entry_price = pos["entry_price"]
                return_pct = (current_price - entry_price) / entry_price
                
                should_close = False
                exit_reason = ""
                
                # 止损
                if return_pct <= -self.stop_loss:
                    should_close = True
                    exit_reason = f"止损 {return_pct*100:.1f}%"
                
                # 止盈
                elif return_pct >= self.take_profit:
                    should_close = True
                    exit_reason = f"止盈 {return_pct*100:.1f}%"
                
                # 持有到期
                entry_date = datetime.strptime(pos["entry_date"], "%Y-%m-%d")
                current_date = datetime.strptime(date, "%Y-%m-%d")
                holding_days = (current_date - entry_date).days
                
                if holding_days >= self.holding_period:
                    should_close = True
                    exit_reason = f"持有到期 {holding_days}天"
                
                if should_close:
                    to_close.append(stock_code)
                    trade = TradeRecord(
                        stock_code=stock_code,
                        stock_name=pos.get("name", ""),
                        entry_date=pos["entry_date"],
                        entry_price=entry_price,
                        exit_date=date,
                        exit_price=current_price,
                        return_pct=return_pct,
                        holding_days=holding_days,
                        exit_reason=exit_reason,
                    )
                    trades.append(trade)
                    capital += pos["shares"] * current_price
                    
            except Exception as e:
                logger.warning(f"检查止损止盈失败: {stock_code} - {e}")
        
        for code in to_close:
            del positions[code]
        
        return capital, trades
    
    def _rebalance(
        self,
        positions: Dict,
        filtered_stocks: List[Dict],
        date: str,
        capital: float,
    ) -> Tuple[float, List[TradeRecord]]:
        """调仓"""
        trades = []
        
        # 计算可用资金
        available_capital = capital
        open_slots = self.max_positions - len(positions)
        
        if open_slots <= 0 or not filtered_stocks:
            return capital, trades
        
        # 按某种逻辑排序 (这里简单按动量排序)
        filtered_stocks.sort(key=lambda x: x.get("mom_20d", 0), reverse=True)
        
        # 买入新股票
        for stock in filtered_stocks[:open_slots]:
            stock_code = stock["code"]
            
            if stock_code in positions:
                continue
            
            try:
                price = stock.get("close") or self._get_current_price(stock_code, date)
                if price is None or price <= 0:
                    continue
                
                # 计算购买金额和股数
                position_capital = available_capital * self.position_size
                shares = int(position_capital / price / 100) * 100  # 取整到100股
                
                if shares < 100:
                    continue
                
                cost = shares * price
                available_capital -= cost
                capital -= cost
                
                positions[stock_code] = {
                    "entry_date": date,
                    "entry_price": price,
                    "shares": shares,
                    "name": stock.get("name", ""),
                }
                
            except Exception as e:
                logger.warning(f"买入失败: {stock_code} - {e}")
        
        return capital, trades
    
    def _close_all_positions(
        self,
        positions: Dict,
        date: str,
        capital: float,
    ) -> Tuple[float, List[TradeRecord]]:
        """清仓"""
        trades = []
        
        for stock_code, pos in list(positions.items()):
            try:
                current_price = self._get_current_price(stock_code, date)
                if current_price is None:
                    continue
                
                return_pct = (current_price - pos["entry_price"]) / pos["entry_price"]
                entry_date = datetime.strptime(pos["entry_date"], "%Y-%m-%d")
                current_date = datetime.strptime(date, "%Y-%m-%d")
                holding_days = (current_date - entry_date).days
                
                trade = TradeRecord(
                    stock_code=stock_code,
                    stock_name=pos.get("name", ""),
                    entry_date=pos["entry_date"],
                    entry_price=pos["entry_price"],
                    exit_date=date,
                    exit_price=current_price,
                    return_pct=return_pct,
                    holding_days=holding_days,
                    exit_reason="清仓",
                )
                trades.append(trade)
                capital += pos["shares"] * current_price
                
            except Exception as e:
                logger.warning(f"清仓失败: {stock_code} - {e}")
        
        positions.clear()
        return capital, trades
    
    def _get_current_price(self, stock_code: str, date: str) -> Optional[float]:
        """获取当日收盘价"""
        try:
            import jqdatasdk as jq
            df = jq.get_price(stock_code, end_date=date, count=1, fields=['close'])
            if df is not None and not df.empty:
                return df['close'].iloc[-1]
        except Exception:
            pass
        return None
    
    def _calculate_nav(
        self,
        positions: Dict,
        date: str,
        capital: float,
    ) -> float:
        """计算净值"""
        nav = capital
        
        for stock_code, pos in positions.items():
            try:
                price = self._get_current_price(stock_code, date)
                if price:
                    nav += pos["shares"] * price
            except Exception:
                continue
        
        return nav
    
    def _calculate_metrics(
        self,
        trades: List[TradeRecord],
        equity_curve: List[Dict],
    ) -> BacktestMetrics:
        """计算回测指标"""
        metrics = BacktestMetrics()
        
        if not equity_curve:
            return metrics
        
        # 净值序列
        navs = [e["nav"] for e in equity_curve]
        initial_nav = navs[0]
        final_nav = navs[-1]
        
        # 总收益率
        metrics.total_return = (final_nav - initial_nav) / initial_nav
        
        # 年化收益
        days = len(equity_curve)
        if days > 0:
            metrics.annual_return = (1 + metrics.total_return) ** (252 / days) - 1
        
        # 最大回撤
        peak = navs[0]
        max_dd = 0
        for nav in navs:
            if nav > peak:
                peak = nav
            dd = (peak - nav) / peak
            if dd > max_dd:
                max_dd = dd
        metrics.max_drawdown = max_dd
        
        # 日收益率
        returns = []
        for i in range(1, len(navs)):
            ret = (navs[i] - navs[i-1]) / navs[i-1]
            returns.append(ret)
        
        # 夏普比率
        if returns:
            avg_return = np.mean(returns) * 252
            std_return = np.std(returns) * np.sqrt(252)
            risk_free = 0.03
            if std_return > 0:
                metrics.sharpe_ratio = (avg_return - risk_free) / std_return
        
        # 索提诺比率
        if returns:
            downside_returns = [r for r in returns if r < 0]
            if downside_returns:
                downside_std = np.std(downside_returns) * np.sqrt(252)
                if downside_std > 0:
                    metrics.sortino_ratio = (avg_return - risk_free) / downside_std
        
        # 卡尔玛比率
        if metrics.max_drawdown > 0:
            metrics.calmar_ratio = metrics.annual_return / metrics.max_drawdown
        
        # 交易统计
        metrics.trade_count = len(trades)
        
        if trades:
            # 胜率
            wins = [t for t in trades if t.return_pct > 0]
            metrics.win_rate = len(wins) / len(trades)
            
            # 盈亏比
            total_win = sum(t.return_pct for t in wins)
            losses = [t for t in trades if t.return_pct <= 0]
            total_loss = abs(sum(t.return_pct for t in losses))
            if total_loss > 0:
                metrics.profit_factor = total_win / total_loss
            
            # 平均持仓天数
            metrics.avg_holding_days = np.mean([t.holding_days for t in trades])
        
        return metrics
    
    def compare_strategies(
        self,
        strategies: List[Tuple[str, Any]],
        start_date: str,
        end_date: str,
    ) -> Dict[str, BacktestResult]:
        """
        对比多个策略
        
        Args:
            strategies: [(名称, FilterOptionsV3), ...] 策略列表
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            {策略名: 回测结果} 字典
        """
        results = {}
        
        for name, options in strategies:
            logger.info(f"回测策略: {name}")
            result = self.run_backtest(
                options,
                start_date,
                end_date,
                strategy_name=name,
            )
            results[name] = result
        
        return results
    
    def get_comparison_summary(self, results: Dict[str, BacktestResult]) -> str:
        """获取策略对比摘要"""
        if not results:
            return "无回测结果"
        
        lines = ["📊 策略对比", "━" * 40]
        
        header = f"{'策略':<15} | {'收益%':>8} | {'回撤%':>8} | {'夏普':>6} | {'胜率%':>6}"
        lines.append(header)
        lines.append("-" * 55)
        
        for name, result in results.items():
            m = result.metrics
            line = f"{name:<15} | {m.total_return*100:>8.1f} | {m.max_drawdown*100:>8.1f} | {m.sharpe_ratio:>6.2f} | {m.win_rate*100:>6.1f}"
            lines.append(line)
        
        return "\n".join(lines)


# ============ 便捷函数 ============

def verify_filter(
    filter_options,
    start_date: str,
    end_date: str,
    **kwargs,
) -> BacktestResult:
    """
    便捷函数：验证筛选条件
    """
    verifier = BacktestVerifierV3(**kwargs)
    return verifier.run_backtest(filter_options, start_date, end_date)


def compare_filters(
    strategies: List[Tuple[str, Any]],
    start_date: str,
    end_date: str,
) -> Dict[str, BacktestResult]:
    """
    便捷函数：对比筛选策略
    """
    verifier = BacktestVerifierV3()
    return verifier.compare_strategies(strategies, start_date, end_date)
