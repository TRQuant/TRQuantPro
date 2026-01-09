"""
科技高成长策略历史回测
=====================================
用历史数据验证选股逻辑的有效性

回测框架：
1. 在历史时点运行选股策略
2. 计算选出股票在后续1周/1月/1季度的收益
3. 与基准（沪深300）对比
4. 统计胜率和超额收益
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

from jqdatasdk import (
    auth, get_price, get_fundamentals, query, valuation,
    indicator, get_trade_days, get_all_securities
)

from tech_growth_screener import TechGrowthScreener


@dataclass
class BacktestResult:
    """单次回测结果"""
    date: str
    stocks: List[str]
    names: List[str]
    
    # 收益率
    return_1w: float      # 1周收益
    return_1m: float      # 1月收益
    return_3m: float      # 3月收益
    
    # 基准收益
    benchmark_1w: float
    benchmark_1m: float
    benchmark_3m: float
    
    # 超额收益
    excess_1w: float
    excess_1m: float
    excess_3m: float


@dataclass
class HistoricalCase:
    """历史案例"""
    stock_code: str
    stock_name: str
    select_date: str
    select_price: float
    select_reason: str
    
    # 后续表现
    price_1w: float
    price_1m: float
    price_3m: float
    return_1w: float
    return_1m: float
    return_3m: float
    
    # 最大回撤
    max_drawdown: float
    
    # 成功/失败
    is_success: bool
    lesson: str


class TechGrowthBacktester:
    """科技高成长策略回测器"""
    
    def __init__(self):
        """初始化"""
        self.screener = TechGrowthScreener()
        self.benchmark = '000300.XSHG'  # 沪深300
        self.results: List[BacktestResult] = []
        self.historical_cases: List[HistoricalCase] = []
    
    def run_backtest(
        self,
        start_date: str = '2023-01-01',
        end_date: str = '2024-12-31',
        frequency: str = 'monthly',  # monthly/quarterly
        top_n: int = 5
    ) -> pd.DataFrame:
        """
        运行历史回测
        
        Args:
            start_date: 回测开始日期
            end_date: 回测结束日期
            frequency: 调仓频率
            top_n: 每次选股数量
        
        Returns:
            回测结果DataFrame
        """
        print(f"\n{'='*70}")
        print(f"📊 科技高成长策略历史回测")
        print(f"📅 回测期间: {start_date} ~ {end_date}")
        print(f"🔄 调仓频率: {frequency}")
        print(f"{'='*70}")
        
        # 获取调仓日期
        trade_days = get_trade_days(start_date, end_date)
        
        if frequency == 'monthly':
            # 每月第一个交易日
            rebalance_dates = self._get_monthly_dates(trade_days)
        else:
            # 每季度第一个交易日
            rebalance_dates = self._get_quarterly_dates(trade_days)
        
        print(f"📆 共 {len(rebalance_dates)} 个调仓点")
        
        self.results = []
        
        for i, date in enumerate(rebalance_dates):
            date_str = date.strftime('%Y-%m-%d')
            print(f"\n[{i+1}/{len(rebalance_dates)}] 📅 {date_str} 选股...")
            
            try:
                # 运行选股
                selections = self.screener.screen(top_n=top_n, date=date_str)
                
                if selections.empty:
                    print(f"   ⚠️ 未选出股票，跳过")
                    continue
                
                stocks = selections['code'].tolist()
                names = selections['name'].tolist()
                
                print(f"   ✅ 选出 {len(stocks)} 只: {', '.join(names)}")
                
                # 计算后续收益
                result = self._calculate_returns(date_str, stocks, names)
                
                if result:
                    self.results.append(result)
                    print(f"   📈 1周: {result.return_1w:+.1f}% (基准{result.benchmark_1w:+.1f}%)")
                    print(f"   📈 1月: {result.return_1m:+.1f}% (基准{result.benchmark_1m:+.1f}%)")
                    
            except Exception as e:
                print(f"   ❌ 回测失败: {e}")
                continue
        
        # 汇总统计
        summary = self._calculate_summary()
        
        return summary
    
    def _get_monthly_dates(self, trade_days) -> List:
        """获取每月第一个交易日"""
        dates = []
        current_month = None
        
        for day in trade_days:
            if day.month != current_month:
                dates.append(day)
                current_month = day.month
        
        return dates[:-3]  # 留出3个月计算收益
    
    def _get_quarterly_dates(self, trade_days) -> List:
        """获取每季度第一个交易日"""
        dates = []
        current_quarter = None
        
        for day in trade_days:
            quarter = (day.month - 1) // 3
            if quarter != current_quarter:
                dates.append(day)
                current_quarter = quarter
        
        return dates[:-1]  # 留出1季度计算收益
    
    def _calculate_returns(
        self,
        select_date: str,
        stocks: List[str],
        names: List[str]
    ) -> Optional[BacktestResult]:
        """计算选股后续收益"""
        try:
            # 获取未来价格数据
            future_end = (datetime.strptime(select_date, '%Y-%m-%d') + timedelta(days=120)).strftime('%Y-%m-%d')
            
            # 组合收益（等权重）
            portfolio_returns = {'1w': [], '1m': [], '3m': []}
            
            for code in stocks:
                df = get_price(
                    code,
                    start_date=select_date,
                    end_date=future_end,
                    fields=['close']
                )
                
                if df.empty or len(df) < 5:
                    continue
                
                base_price = df['close'].iloc[0]
                
                # 1周收益
                if len(df) >= 5:
                    price_1w = df['close'].iloc[4]
                    portfolio_returns['1w'].append((price_1w / base_price - 1) * 100)
                
                # 1月收益（约21个交易日）
                if len(df) >= 21:
                    price_1m = df['close'].iloc[20]
                    portfolio_returns['1m'].append((price_1m / base_price - 1) * 100)
                
                # 3月收益（约63个交易日）
                if len(df) >= 63:
                    price_3m = df['close'].iloc[62]
                    portfolio_returns['3m'].append((price_3m / base_price - 1) * 100)
            
            # 计算组合平均收益
            return_1w = np.mean(portfolio_returns['1w']) if portfolio_returns['1w'] else 0
            return_1m = np.mean(portfolio_returns['1m']) if portfolio_returns['1m'] else 0
            return_3m = np.mean(portfolio_returns['3m']) if portfolio_returns['3m'] else 0
            
            # 基准收益
            df_bench = get_price(
                self.benchmark,
                start_date=select_date,
                end_date=future_end,
                fields=['close']
            )
            
            if df_bench.empty:
                return None
            
            bench_base = df_bench['close'].iloc[0]
            
            benchmark_1w = ((df_bench['close'].iloc[4] / bench_base - 1) * 100) if len(df_bench) >= 5 else 0
            benchmark_1m = ((df_bench['close'].iloc[20] / bench_base - 1) * 100) if len(df_bench) >= 21 else 0
            benchmark_3m = ((df_bench['close'].iloc[62] / bench_base - 1) * 100) if len(df_bench) >= 63 else 0
            
            return BacktestResult(
                date=select_date,
                stocks=stocks,
                names=names,
                return_1w=return_1w,
                return_1m=return_1m,
                return_3m=return_3m,
                benchmark_1w=benchmark_1w,
                benchmark_1m=benchmark_1m,
                benchmark_3m=benchmark_3m,
                excess_1w=return_1w - benchmark_1w,
                excess_1m=return_1m - benchmark_1m,
                excess_3m=return_3m - benchmark_3m
            )
            
        except Exception as e:
            print(f"   计算收益失败: {e}")
            return None
    
    def _calculate_summary(self) -> pd.DataFrame:
        """计算回测统计"""
        if not self.results:
            return pd.DataFrame()
        
        # 转换为DataFrame
        data = []
        for r in self.results:
            data.append({
                'date': r.date,
                'stocks': ', '.join(r.names[:3]) + '...',
                'return_1w': r.return_1w,
                'return_1m': r.return_1m,
                'return_3m': r.return_3m,
                'benchmark_1w': r.benchmark_1w,
                'benchmark_1m': r.benchmark_1m,
                'benchmark_3m': r.benchmark_3m,
                'excess_1w': r.excess_1w,
                'excess_1m': r.excess_1m,
                'excess_3m': r.excess_3m
            })
        
        df = pd.DataFrame(data)
        
        print(f"\n{'='*70}")
        print(f"📊 回测统计汇总")
        print(f"{'='*70}")
        
        # 胜率统计
        win_rate_1w = (df['excess_1w'] > 0).mean() * 100
        win_rate_1m = (df['excess_1m'] > 0).mean() * 100
        win_rate_3m = (df['excess_3m'] > 0).mean() * 100
        
        print(f"\n📈 胜率（跑赢基准）:")
        print(f"   1周胜率: {win_rate_1w:.1f}%")
        print(f"   1月胜率: {win_rate_1m:.1f}%")
        print(f"   3月胜率: {win_rate_3m:.1f}%")
        
        # 平均收益
        print(f"\n📈 平均收益:")
        print(f"   组合1周: {df['return_1w'].mean():+.2f}% (基准{df['benchmark_1w'].mean():+.2f}%)")
        print(f"   组合1月: {df['return_1m'].mean():+.2f}% (基准{df['benchmark_1m'].mean():+.2f}%)")
        print(f"   组合3月: {df['return_3m'].mean():+.2f}% (基准{df['benchmark_3m'].mean():+.2f}%)")
        
        # 平均超额收益
        print(f"\n📈 平均超额收益:")
        print(f"   1周超额: {df['excess_1w'].mean():+.2f}%")
        print(f"   1月超额: {df['excess_1m'].mean():+.2f}%")
        print(f"   3月超额: {df['excess_3m'].mean():+.2f}%")
        
        # 最大单次收益/亏损
        print(f"\n📈 极值:")
        print(f"   最大1月收益: {df['return_1m'].max():+.2f}%")
        print(f"   最大1月亏损: {df['return_1m'].min():+.2f}%")
        
        return df
    
    def analyze_historical_cases(
        self,
        start_date: str = '2023-06-01',
        end_date: str = '2024-06-01',
        sample_size: int = 10
    ) -> List[HistoricalCase]:
        """
        分析历史典型案例
        找出成功和失败的案例进行归因分析
        """
        print(f"\n{'='*70}")
        print(f"🔍 历史案例分析")
        print(f"{'='*70}")
        
        # 选取几个历史时点
        test_dates = ['2023-06-01', '2023-09-01', '2024-01-02', '2024-06-03']
        
        all_cases = []
        
        for date_str in test_dates:
            print(f"\n📅 分析 {date_str} 选出的股票...")
            
            try:
                # 运行选股
                selections = self.screener.screen(top_n=5, date=date_str)
                
                if selections.empty:
                    continue
                
                for _, row in selections.iterrows():
                    case = self._analyze_single_case(
                        code=row['code'],
                        name=row['name'],
                        select_date=date_str,
                        select_reason=row['reason']
                    )
                    if case:
                        all_cases.append(case)
                        
            except Exception as e:
                print(f"   ❌ 分析失败: {e}")
                continue
        
        self.historical_cases = all_cases
        
        # 打印典型案例
        self._print_case_analysis(all_cases)
        
        return all_cases
    
    def _analyze_single_case(
        self,
        code: str,
        name: str,
        select_date: str,
        select_reason: str
    ) -> Optional[HistoricalCase]:
        """分析单个案例"""
        try:
            # 获取后续3个月价格
            future_end = (datetime.strptime(select_date, '%Y-%m-%d') + timedelta(days=100)).strftime('%Y-%m-%d')
            
            df = get_price(
                code,
                start_date=select_date,
                end_date=future_end,
                fields=['close', 'high', 'low']
            )
            
            if df.empty or len(df) < 63:
                return None
            
            select_price = df['close'].iloc[0]
            price_1w = df['close'].iloc[4] if len(df) > 4 else select_price
            price_1m = df['close'].iloc[20] if len(df) > 20 else select_price
            price_3m = df['close'].iloc[62] if len(df) > 62 else select_price
            
            return_1w = (price_1w / select_price - 1) * 100
            return_1m = (price_1m / select_price - 1) * 100
            return_3m = (price_3m / select_price - 1) * 100
            
            # 最大回撤
            cummax = df['close'].cummax()
            drawdown = ((df['close'] - cummax) / cummax * 100).min()
            
            # 判断成功/失败
            is_success = return_3m > 10
            
            # 归因分析
            if is_success:
                lesson = "高成长逻辑兑现，趋势延续"
            else:
                if drawdown < -20:
                    lesson = "回撤过大，需设好止损"
                elif return_1m > 10 and return_3m < 0:
                    lesson = "短期冲高后回落，应及时止盈"
                else:
                    lesson = "业绩或趋势未能持续"
            
            return HistoricalCase(
                stock_code=code,
                stock_name=name,
                select_date=select_date,
                select_price=select_price,
                select_reason=select_reason,
                price_1w=price_1w,
                price_1m=price_1m,
                price_3m=price_3m,
                return_1w=return_1w,
                return_1m=return_1m,
                return_3m=return_3m,
                max_drawdown=drawdown,
                is_success=is_success,
                lesson=lesson
            )
            
        except Exception as e:
            return None
    
    def _print_case_analysis(self, cases: List[HistoricalCase]):
        """打印案例分析"""
        if not cases:
            print("无有效案例")
            return
        
        success_cases = [c for c in cases if c.is_success]
        fail_cases = [c for c in cases if not c.is_success]
        
        print(f"\n📈 成功案例 ({len(success_cases)}个):")
        print("-" * 60)
        for c in success_cases[:5]:
            print(f"  {c.stock_name}({c.stock_code}) @ {c.select_date}")
            print(f"    选股理由: {c.select_reason}")
            print(f"    收益: 1周{c.return_1w:+.1f}% / 1月{c.return_1m:+.1f}% / 3月{c.return_3m:+.1f}%")
            print(f"    经验: {c.lesson}")
        
        print(f"\n📉 失败案例 ({len(fail_cases)}个):")
        print("-" * 60)
        for c in fail_cases[:5]:
            print(f"  {c.stock_name}({c.stock_code}) @ {c.select_date}")
            print(f"    选股理由: {c.select_reason}")
            print(f"    收益: 1周{c.return_1w:+.1f}% / 1月{c.return_1m:+.1f}% / 3月{c.return_3m:+.1f}%")
            print(f"    最大回撤: {c.max_drawdown:.1f}%")
            print(f"    教训: {c.lesson}")
        
        # 统计
        total = len(cases)
        success_rate = len(success_cases) / total * 100 if total > 0 else 0
        avg_return_success = np.mean([c.return_3m for c in success_cases]) if success_cases else 0
        avg_return_fail = np.mean([c.return_3m for c in fail_cases]) if fail_cases else 0
        
        print(f"\n📊 案例统计:")
        print(f"   总案例数: {total}")
        print(f"   成功率: {success_rate:.1f}%")
        print(f"   成功案例平均收益: {avg_return_success:+.1f}%")
        print(f"   失败案例平均收益: {avg_return_fail:+.1f}%")


def run_backtest():
    """运行回测"""
    # JQData认证
    auth('18610026017', 'Tt103003!')
    
    backtester = TechGrowthBacktester()
    
    # 运行回测
    results = backtester.run_backtest(
        start_date='2024-01-01',
        end_date='2024-12-01',
        frequency='monthly',
        top_n=5
    )
    
    # 分析历史案例
    cases = backtester.analyze_historical_cases()
    
    return results, cases


if __name__ == "__main__":
    run_backtest()
