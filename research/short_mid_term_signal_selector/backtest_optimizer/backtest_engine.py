# -*- coding: utf-8 -*-
"""
回测引擎 (Backtest Engine)

核心功能：
1. 历史时点筛选模拟
2. 多周期收益率计算
3. 风险调整收益评估
4. 回测结果统计分析
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
import warnings

# JQData
try:
    import jqdatasdk as jq
    HAS_JQDATA = True
except ImportError:
    HAS_JQDATA = False


@dataclass
class BacktestPeriod:
    """回测周期定义"""
    name: str           # 周期名称
    days: int           # 交易日数量
    description: str    # 描述
    
# 标准回测周期
BACKTEST_PERIODS = {
    'week': BacktestPeriod('周', 5, '1周后收益'),
    'month': BacktestPeriod('月', 21, '1月后收益'),
    'quarter': BacktestPeriod('季', 63, '1季后收益'),
    'year': BacktestPeriod('年', 252, '1年后收益'),
    'five_year': BacktestPeriod('五年', 1260, '5年后收益'),
}


@dataclass
class StockReturn:
    """单只股票收益记录"""
    code: str
    name: str
    select_date: str        # 筛选日期
    select_score: float     # 筛选时得分
    select_price: float     # 筛选时价格
    sector: str             # 所属板块
    
    # 各周期收益率
    return_week: Optional[float] = None
    return_month: Optional[float] = None
    return_quarter: Optional[float] = None
    return_year: Optional[float] = None
    return_five_year: Optional[float] = None
    
    # 风险指标
    max_drawdown: Optional[float] = None    # 最大回撤
    volatility: Optional[float] = None      # 波动率
    sharpe: Optional[float] = None          # 夏普比率


@dataclass
class BacktestResult:
    """回测结果"""
    test_date: str                          # 回测基准日期
    stocks: List[StockReturn]               # 股票收益列表
    benchmark_returns: Dict[str, float]     # 基准收益（沪深300）
    
    # 策略统计
    avg_returns: Dict[str, float] = field(default_factory=dict)    # 平均收益
    win_rates: Dict[str, float] = field(default_factory=dict)      # 胜率
    excess_returns: Dict[str, float] = field(default_factory=dict) # 超额收益
    
    # 元数据
    factor_weights: Dict[str, float] = field(default_factory=dict) # 当时使用的因子权重
    market_regime: str = ''                 # 当时的市场环境


class BacktestEngine:
    """
    回测引擎
    
    设计原则：
    1. 严格使用历史数据，避免未来信息泄露
    2. 支持多周期收益验证
    3. 计算风险调整后收益
    4. 支持滚动回测
    """
    
    def __init__(self, 
                 screener_func: Callable,
                 periods: List[str] = None,
                 benchmark: str = '000300.XSHG'):
        """
        Args:
            screener_func: 筛选函数，输入日期返回筛选结果
            periods: 要计算的周期列表，默认全部
            benchmark: 基准指数代码
        """
        self.screener_func = screener_func
        self.periods = periods or list(BACKTEST_PERIODS.keys())
        self.benchmark = benchmark
        
        # 初始化JQData
        self._init_jqdata()
        
    def _init_jqdata(self):
        """初始化聚宽连接"""
        if not HAS_JQDATA:
            raise ImportError("需要安装jqdatasdk")
        
        try:
            # 检查是否已认证
            if not jq.is_auth():
                from core.jqdata_auth import auth_jqdata
                auth_jqdata()
        except:
            pass
    
    def run_single_backtest(self, 
                           test_date: str,
                           top_n: int = 30,
                           factor_weights: Dict[str, float] = None) -> BacktestResult:
        """
        运行单次回测
        
        Args:
            test_date: 回测基准日期 (YYYY-MM-DD)
            top_n: 筛选股票数量
            factor_weights: 因子权重配置
            
        Returns:
            BacktestResult: 回测结果
        """
        print(f"\n{'='*60}")
        print(f"📅 回测日期: {test_date}")
        print(f"{'='*60}")
        
        # 1. 获取筛选结果
        print(f"🔍 执行筛选...")
        try:
            selected_stocks = self.screener_func(
                as_of_date=test_date,
                top_n=top_n,
                factor_weights=factor_weights
            )
        except Exception as e:
            print(f"❌ 筛选失败: {e}")
            return None
        
        if not selected_stocks:
            print("⚠️ 未筛选到股票")
            return None
            
        print(f"✅ 筛选出 {len(selected_stocks)} 只股票")
        
        # 2. 计算各周期收益
        stock_returns = []
        for stock in selected_stocks:
            code = stock.get('code', stock.get('股票代码'))
            name = stock.get('name', stock.get('名称', ''))
            score = stock.get('total_score', stock.get('综合分', 0))
            sector = stock.get('sector', stock.get('所属板块', ''))
            
            # 获取筛选日价格
            select_price = self._get_price_on_date(code, test_date)
            
            # 创建收益记录
            sr = StockReturn(
                code=code,
                name=name,
                select_date=test_date,
                select_score=score,
                select_price=select_price or 0,
                sector=sector
            )
            
            # 计算各周期收益
            for period_key in self.periods:
                period = BACKTEST_PERIODS[period_key]
                future_date = self._get_future_date(test_date, period.days)
                
                if future_date:
                    ret = self._calc_return(code, test_date, future_date)
                    setattr(sr, f'return_{period_key}', ret)
            
            # 计算风险指标（基于季度数据）
            if sr.return_quarter is not None:
                risk_metrics = self._calc_risk_metrics(code, test_date, 63)
                sr.max_drawdown = risk_metrics.get('max_drawdown')
                sr.volatility = risk_metrics.get('volatility')
                sr.sharpe = risk_metrics.get('sharpe')
            
            stock_returns.append(sr)
            
        # 3. 计算基准收益
        benchmark_returns = {}
        for period_key in self.periods:
            period = BACKTEST_PERIODS[period_key]
            future_date = self._get_future_date(test_date, period.days)
            if future_date:
                benchmark_returns[period_key] = self._calc_return(
                    self.benchmark, test_date, future_date
                )
        
        # 4. 统计分析
        result = BacktestResult(
            test_date=test_date,
            stocks=stock_returns,
            benchmark_returns=benchmark_returns,
            factor_weights=factor_weights or {}
        )
        
        # 计算策略统计
        self._calc_strategy_stats(result)
        
        return result
    
    def run_rolling_backtest(self,
                            start_date: str,
                            end_date: str,
                            frequency: str = 'month',
                            top_n: int = 30,
                            factor_weights: Dict[str, float] = None) -> List[BacktestResult]:
        """
        滚动回测
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            frequency: 回测频率 (week/month/quarter)
            top_n: 每次筛选股票数
            factor_weights: 因子权重
            
        Returns:
            List[BacktestResult]: 回测结果列表
        """
        print(f"\n{'='*60}")
        print(f"📊 滚动回测: {start_date} -> {end_date}")
        print(f"📅 频率: {frequency}")
        print(f"{'='*60}")
        
        # 获取回测日期序列
        test_dates = self._get_test_dates(start_date, end_date, frequency)
        print(f"📆 共 {len(test_dates)} 个回测点")
        
        results = []
        for i, test_date in enumerate(test_dates):
            print(f"\n[{i+1}/{len(test_dates)}] ", end='')
            result = self.run_single_backtest(
                test_date=test_date,
                top_n=top_n,
                factor_weights=factor_weights
            )
            if result:
                results.append(result)
        
        # 汇总统计
        self._print_rolling_summary(results)
        
        return results
    
    def _get_price_on_date(self, code: str, date: str) -> Optional[float]:
        """获取指定日期的收盘价"""
        try:
            df = jq.get_price(
                code, 
                start_date=date, 
                end_date=date,
                frequency='daily',
                fields=['close']
            )
            if not df.empty:
                return float(df['close'].iloc[0])
        except:
            pass
        return None
    
    def _get_future_date(self, base_date: str, days: int) -> Optional[str]:
        """获取N个交易日后的日期"""
        try:
            trade_days = jq.get_trade_days(
                start_date=base_date,
                count=days + 5  # 多取几天以防节假日
            )
            if len(trade_days) > days:
                future = trade_days[days]
                # 检查是否超过今天
                if future <= datetime.now().date():
                    return str(future)
        except:
            pass
        return None
    
    def _calc_return(self, code: str, start_date: str, end_date: str) -> Optional[float]:
        """计算区间收益率"""
        try:
            # 获取开始日价格
            df_start = jq.get_price(
                code,
                start_date=start_date,
                end_date=start_date,
                frequency='daily',
                fields=['close']
            )
            
            # 获取结束日价格
            df_end = jq.get_price(
                code,
                start_date=end_date,
                end_date=end_date,
                frequency='daily',
                fields=['close']
            )
            
            if not df_start.empty and not df_end.empty:
                p0 = float(df_start['close'].iloc[0])
                p1 = float(df_end['close'].iloc[0])
                return (p1 - p0) / p0 * 100  # 百分比
        except:
            pass
        return None
    
    def _calc_risk_metrics(self, code: str, start_date: str, days: int) -> Dict:
        """计算风险指标"""
        metrics = {}
        try:
            end_date = self._get_future_date(start_date, days)
            if not end_date:
                return metrics
                
            df = jq.get_price(
                code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['close']
            )
            
            if len(df) < 10:
                return metrics
            
            # 日收益率
            returns = df['close'].pct_change().dropna()
            
            # 波动率（年化）
            metrics['volatility'] = float(returns.std() * np.sqrt(252) * 100)
            
            # 最大回撤
            cummax = df['close'].cummax()
            drawdown = (df['close'] - cummax) / cummax
            metrics['max_drawdown'] = float(drawdown.min() * 100)
            
            # 夏普比率（假设无风险利率2%）
            rf = 0.02 / 252
            excess_return = returns.mean() - rf
            if returns.std() > 0:
                metrics['sharpe'] = float(excess_return / returns.std() * np.sqrt(252))
                
        except:
            pass
        return metrics
    
    def _calc_strategy_stats(self, result: BacktestResult):
        """计算策略统计"""
        for period_key in self.periods:
            returns = []
            for stock in result.stocks:
                ret = getattr(stock, f'return_{period_key}')
                if ret is not None:
                    returns.append(ret)
            
            if returns:
                # 平均收益
                result.avg_returns[period_key] = np.mean(returns)
                
                # 胜率
                win_count = sum(1 for r in returns if r > 0)
                result.win_rates[period_key] = win_count / len(returns) * 100
                
                # 超额收益
                benchmark_ret = result.benchmark_returns.get(period_key, 0)
                if benchmark_ret is not None:
                    result.excess_returns[period_key] = np.mean(returns) - benchmark_ret
    
    def _get_test_dates(self, start_date: str, end_date: str, frequency: str) -> List[str]:
        """获取回测日期序列"""
        freq_days = {
            'week': 5,
            'month': 21,
            'quarter': 63
        }
        step = freq_days.get(frequency, 21)
        
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        dates = []
        for i in range(0, len(trade_days), step):
            dates.append(str(trade_days[i]))
        return dates
    
    def _print_rolling_summary(self, results: List[BacktestResult]):
        """打印滚动回测汇总"""
        if not results:
            return
            
        print(f"\n{'='*60}")
        print("📊 滚动回测汇总")
        print(f"{'='*60}")
        
        for period_key in self.periods:
            period = BACKTEST_PERIODS[period_key]
            
            avg_returns = [r.avg_returns.get(period_key, 0) for r in results if r.avg_returns.get(period_key)]
            win_rates = [r.win_rates.get(period_key, 0) for r in results if r.win_rates.get(period_key)]
            excess_returns = [r.excess_returns.get(period_key, 0) for r in results if r.excess_returns.get(period_key)]
            
            if avg_returns:
                print(f"\n📅 {period.description}:")
                print(f"   平均收益: {np.mean(avg_returns):.2f}% (波动: {np.std(avg_returns):.2f}%)")
                print(f"   平均胜率: {np.mean(win_rates):.1f}%")
                print(f"   平均超额: {np.mean(excess_returns):.2f}%")


def create_default_screener():
    """创建默认筛选函数（用于测试）"""
    from research.short_mid_term_signal_selector.tenbagger_mainline_screener import MainlineScreener
    
    def screener_func(as_of_date: str, top_n: int = 30, factor_weights: Dict = None):
        screener = MainlineScreener()
        # 这里需要适配MainlineScreener使其支持历史日期
        results = screener.screen(top_n=top_n)
        return results
    
    return screener_func


if __name__ == '__main__':
    # 测试回测引擎
    print("🧪 测试回测引擎...")
    
    # 这里需要一个支持历史日期的筛选函数
    # engine = BacktestEngine(screener_func=create_default_screener())
    # result = engine.run_single_backtest('2025-01-01', top_n=10)
