#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
短期动量策略筛选器

基于第五次牛市(2019-2021)研究成果，实现三种动量策略的股票筛选。

策略一：强动量突破策略 (mom_5d >= 15%)
策略二：加速突破策略 (mom_5d > 10% AND mom_20d > 30%)
策略三：回调反弹策略 (mom_5d < 0 AND mom_20d > 15%)

作者: TRQuant Team
日期: 2026-01-10
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import numpy as np

# 确保项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class StrategyType(Enum):
    """策略类型"""
    STRONG_BREAKOUT = "strong_breakout"       # 强动量突破
    ACCELERATED_BREAKOUT = "accelerated_breakout"  # 加速突破
    PULLBACK_REBOUND = "pullback_rebound"     # 回调反弹
    ALL = "all"                                # 所有策略


@dataclass
class ScreenResult:
    """筛选结果"""
    code: str
    name: str
    strategy: str
    mom_5d: float
    mom_20d: float
    mom_60d: float
    close: float
    volume: float
    score: float
    recommendation: str
    
    def to_dict(self) -> Dict:
        return {
            'code': self.code,
            'name': self.name,
            'strategy': self.strategy,
            'mom_5d': self.mom_5d,
            'mom_20d': self.mom_20d,
            'mom_60d': self.mom_60d,
            'close': self.close,
            'volume': self.volume,
            'score': self.score,
            'recommendation': self.recommendation
        }


class MomentumStrategyScreener:
    """短期动量策略筛选器
    
    基于历史研究成果，实现三种动量策略的实时股票筛选。
    
    研究发现：
    - 强动量突破(mom_5d>=15%): 均值回报47.2%, 极端收益概率38.5%
    - 加速突破(mom_5d>10% & mom_20d>30%): 均值回报47.2%, 更稳定
    - 回调反弹(mom_5d<0 & mom_20d>15%): 均值回报48.0%, 低吸机会
    """
    
    # 策略参数（基于研究结果）
    STRATEGY_PARAMS = {
        StrategyType.STRONG_BREAKOUT: {
            'mom_5d_min': 15.0,
            'expected_return': 47.2,
            'extreme_prob': 38.5,
            'description': '强动量突破：追强势龙头'
        },
        StrategyType.ACCELERATED_BREAKOUT: {
            'mom_5d_min': 10.0,
            'mom_20d_min': 30.0,
            'expected_return': 47.2,
            'extreme_prob': 33.3,
            'description': '加速突破：双因子确认'
        },
        StrategyType.PULLBACK_REBOUND: {
            'mom_5d_max': 0.0,
            'mom_20d_min': 15.0,
            'expected_return': 48.0,
            'extreme_prob': 7.0,
            'description': '回调反弹：低吸强势股'
        }
    }
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.jq = None
        self._init_jqdata()
    
    def _init_jqdata(self):
        """初始化JQData连接"""
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            cm = get_config_manager()
            cfg = cm.get_config('jqdata')
            jq.auth(cfg['username'], cfg['password'])
            
            if jq.is_auth():
                self.jq = jq
                if self.verbose:
                    print("✅ JQData连接成功")
            else:
                print("❌ JQData认证失败")
        except Exception as e:
            print(f"❌ JQData初始化失败: {e}")
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def get_stock_universe(self, date: str = None, max_stocks: int = 500) -> List[str]:
        """获取股票池"""
        if not self.jq:
            return []
        
        if date is None:
            trade_days = self.jq.get_trade_days(end_date=datetime.now(), count=5)
            date = trade_days[-1].strftime('%Y-%m-%d')
        
        all_stocks = self.jq.get_all_securities(types=['stock'], date=date)
        
        # 过滤ST、次新股
        one_year_ago = (pd.to_datetime(date) - timedelta(days=365)).strftime('%Y-%m-%d')
        
        valid = all_stocks[
            ~all_stocks['display_name'].str.contains('ST|\\*|退', na=False) &
            (all_stocks['start_date'].astype(str) < one_year_ago)
        ]
        
        stocks = valid.index.tolist()
        if len(stocks) > max_stocks:
            stocks = stocks[:max_stocks]
        
        return stocks, valid
    
    def calculate_momentum(self, stocks: List[str], date: str = None) -> pd.DataFrame:
        """计算动量因子
        
        Args:
            stocks: 股票列表
            date: 计算日期
        
        Returns:
            包含动量因子的DataFrame
        """
        if not self.jq:
            return pd.DataFrame()
        
        if date is None:
            trade_days = self.jq.get_trade_days(end_date=datetime.now(), count=5)
            date = trade_days[-1].strftime('%Y-%m-%d')
        
        # 获取历史数据（需要60天历史来计算60日动量）
        start_date = (pd.to_datetime(date) - timedelta(days=120)).strftime('%Y-%m-%d')
        
        self._log(f"📥 获取价格数据: {start_date} ~ {date}")
        
        price_data = self.jq.get_price(
            stocks,
            start_date=start_date,
            end_date=date,
            frequency='daily',
            fields=['close', 'volume'],
            skip_paused=True,
            fq='post',
            panel=False
        )
        
        if price_data is None or price_data.empty:
            return pd.DataFrame()
        
        # 标准化列名
        if 'time' in price_data.columns:
            price_data = price_data.rename(columns={'time': 'date'})
        
        price_data['date'] = pd.to_datetime(price_data['date']).dt.strftime('%Y-%m-%d')
        
        # 计算每只股票的动量
        results = []
        for code in price_data['code'].unique():
            stock_data = price_data[price_data['code'] == code].sort_values('date')
            
            if len(stock_data) < 60:
                continue
            
            latest = stock_data.iloc[-1]
            
            # 计算动量
            close_5d_ago = stock_data.iloc[-6]['close'] if len(stock_data) >= 6 else latest['close']
            close_20d_ago = stock_data.iloc[-21]['close'] if len(stock_data) >= 21 else latest['close']
            close_60d_ago = stock_data.iloc[-61]['close'] if len(stock_data) >= 61 else latest['close']
            
            mom_5d = (latest['close'] / close_5d_ago - 1) * 100 if close_5d_ago > 0 else 0
            mom_20d = (latest['close'] / close_20d_ago - 1) * 100 if close_20d_ago > 0 else 0
            mom_60d = (latest['close'] / close_60d_ago - 1) * 100 if close_60d_ago > 0 else 0
            
            results.append({
                'code': code,
                'close': latest['close'],
                'volume': latest['volume'],
                'mom_5d': mom_5d,
                'mom_20d': mom_20d,
                'mom_60d': mom_60d,
                'date': latest['date']
            })
        
        return pd.DataFrame(results)
    
    def apply_strategy_filter(
        self,
        momentum_df: pd.DataFrame,
        strategy: StrategyType
    ) -> pd.DataFrame:
        """应用策略筛选条件
        
        Args:
            momentum_df: 动量数据
            strategy: 策略类型
        
        Returns:
            符合条件的股票
        """
        if momentum_df.empty:
            return momentum_df
        
        params = self.STRATEGY_PARAMS.get(strategy, {})
        
        if strategy == StrategyType.STRONG_BREAKOUT:
            # 强动量突破: mom_5d >= 15%
            mask = momentum_df['mom_5d'] >= params['mom_5d_min']
        
        elif strategy == StrategyType.ACCELERATED_BREAKOUT:
            # 加速突破: mom_5d > 10% AND mom_20d > 30%
            mask = (momentum_df['mom_5d'] > params['mom_5d_min']) & \
                   (momentum_df['mom_20d'] > params['mom_20d_min'])
        
        elif strategy == StrategyType.PULLBACK_REBOUND:
            # 回调反弹: mom_5d < 0 AND mom_20d > 15%
            mask = (momentum_df['mom_5d'] < params['mom_5d_max']) & \
                   (momentum_df['mom_20d'] > params['mom_20d_min'])
        
        else:
            mask = pd.Series([True] * len(momentum_df))
        
        filtered = momentum_df[mask].copy()
        filtered['strategy'] = strategy.value
        
        return filtered
    
    def calculate_score(self, row: pd.Series, strategy: StrategyType) -> float:
        """计算推荐评分
        
        评分逻辑：
        - 动量强度越高，分数越高
        - 多周期动量一致性加分
        - 基于历史研究的权重调整
        """
        score = 50.0  # 基础分
        
        if strategy == StrategyType.STRONG_BREAKOUT:
            # 5日动量权重最高
            score += min(row['mom_5d'] - 15, 20) * 2  # 15%以上每1%加2分
            if row['mom_20d'] > 20:
                score += 10  # 20日动量确认加分
            if row['mom_5d'] > row['mom_20d'] / 4:
                score += 5  # 加速趋势加分
        
        elif strategy == StrategyType.ACCELERATED_BREAKOUT:
            # 双因子平衡
            score += min(row['mom_5d'] - 10, 15) * 1.5
            score += min(row['mom_20d'] - 30, 30) * 0.5
            if row['mom_60d'] > 30:
                score += 5  # 长期趋势确认
        
        elif strategy == StrategyType.PULLBACK_REBOUND:
            # 回调深度适中且中期强势
            score += min(row['mom_20d'] - 15, 30) * 1
            if -5 < row['mom_5d'] < 0:
                score += 10  # 轻度回调最佳
            if row['mom_60d'] > 20:
                score += 5  # 长期趋势支撑
        
        return min(max(score, 0), 100)  # 限制在0-100
    
    def get_recommendation(self, score: float) -> str:
        """根据评分给出推荐"""
        if score >= 80:
            return "★★★ 强烈推荐"
        elif score >= 65:
            return "★★ 推荐"
        elif score >= 50:
            return "★ 观望"
        else:
            return "- 不推荐"
    
    def screen(
        self,
        strategy: StrategyType = StrategyType.ALL,
        date: str = None,
        max_stocks: int = 500,
        top_n: int = 20
    ) -> List[ScreenResult]:
        """执行筛选
        
        Args:
            strategy: 策略类型
            date: 筛选日期
            max_stocks: 最大股票数
            top_n: 返回前N名
        
        Returns:
            筛选结果列表
        """
        self._log(f"\n{'='*60}")
        self._log(f"🔍 短期动量策略筛选")
        self._log(f"   策略: {strategy.value}")
        self._log(f"   日期: {date or '最新'}")
        self._log(f"{'='*60}\n")
        
        # 获取股票池
        stocks, stock_info = self.get_stock_universe(date, max_stocks)
        if not stocks:
            self._log("❌ 股票池为空")
            return []
        
        self._log(f"📊 股票池: {len(stocks)}只股票")
        
        # 计算动量
        momentum_df = self.calculate_momentum(stocks, date)
        if momentum_df.empty:
            self._log("❌ 动量数据为空")
            return []
        
        self._log(f"✅ 计算动量: {len(momentum_df)}只股票")
        
        # 应用策略筛选
        results = []
        
        strategies_to_apply = [strategy] if strategy != StrategyType.ALL else [
            StrategyType.STRONG_BREAKOUT,
            StrategyType.ACCELERATED_BREAKOUT,
            StrategyType.PULLBACK_REBOUND
        ]
        
        for strat in strategies_to_apply:
            filtered = self.apply_strategy_filter(momentum_df, strat)
            
            if filtered.empty:
                self._log(f"   {strat.value}: 0只股票符合条件")
                continue
            
            # 计算评分
            filtered['score'] = filtered.apply(lambda r: self.calculate_score(r, strat), axis=1)
            filtered['recommendation'] = filtered['score'].apply(self.get_recommendation)
            
            # 排序取Top N
            filtered = filtered.nlargest(top_n, 'score')
            
            self._log(f"   {strat.value}: {len(filtered)}只股票符合条件")
            
            # 转换为结果对象
            for _, row in filtered.iterrows():
                code = row['code']
                name = stock_info.loc[code, 'display_name'] if code in stock_info.index else ''
                
                results.append(ScreenResult(
                    code=code,
                    name=name,
                    strategy=strat.value,
                    mom_5d=row['mom_5d'],
                    mom_20d=row['mom_20d'],
                    mom_60d=row['mom_60d'],
                    close=row['close'],
                    volume=row['volume'],
                    score=row['score'],
                    recommendation=row['recommendation']
                ))
        
        # 按评分排序
        results.sort(key=lambda x: x.score, reverse=True)
        
        self._log(f"\n✅ 筛选完成，共{len(results)}只股票")
        
        return results[:top_n * len(strategies_to_apply)]
    
    def print_results(self, results: List[ScreenResult]):
        """打印筛选结果"""
        if not results:
            print("❌ 无符合条件的股票")
            return
        
        print(f"\n{'='*80}")
        print(f"{'股票代码':<12} {'名称':<8} {'策略':<20} {'5日动量':>8} {'20日动量':>8} {'评分':>6} {'推荐'}")
        print(f"{'='*80}")
        
        for r in results:
            print(f"{r.code:<12} {r.name:<8} {r.strategy:<20} {r.mom_5d:>7.1f}% {r.mom_20d:>7.1f}% {r.score:>5.0f} {r.recommendation}")
        
        print(f"{'='*80}")
    
    def to_dataframe(self, results: List[ScreenResult]) -> pd.DataFrame:
        """转换为DataFrame"""
        return pd.DataFrame([r.to_dict() for r in results])


def main():
    """测试入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='短期动量策略筛选器')
    parser.add_argument('--strategy', default='all', 
                        choices=['strong_breakout', 'accelerated_breakout', 'pullback_rebound', 'all'],
                        help='策略类型')
    parser.add_argument('--date', default=None, help='筛选日期 (YYYY-MM-DD)')
    parser.add_argument('--max-stocks', type=int, default=500, help='最大股票数')
    parser.add_argument('--top-n', type=int, default=10, help='返回Top N')
    parser.add_argument('--output', default=None, help='输出CSV文件路径')
    
    args = parser.parse_args()
    
    strategy_map = {
        'strong_breakout': StrategyType.STRONG_BREAKOUT,
        'accelerated_breakout': StrategyType.ACCELERATED_BREAKOUT,
        'pullback_rebound': StrategyType.PULLBACK_REBOUND,
        'all': StrategyType.ALL
    }
    
    screener = MomentumStrategyScreener(verbose=True)
    
    results = screener.screen(
        strategy=strategy_map[args.strategy],
        date=args.date,
        max_stocks=args.max_stocks,
        top_n=args.top_n
    )
    
    screener.print_results(results)
    
    if args.output:
        df = screener.to_dataframe(results)
        df.to_csv(args.output, index=False)
        print(f"\n💾 结果已保存到: {args.output}")


if __name__ == '__main__':
    main()
