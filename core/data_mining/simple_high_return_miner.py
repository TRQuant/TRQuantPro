#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单高回报股票挖掘器 - 从零开始的正确实现

设计原则：
1. 批量获取数据，不逐股票调用API
2. 直接在DataFrame上计算回报率
3. 不需要牛市评分（指定时间段默认为牛市研究）
4. 小步验证，先确保能找到数据

作者: TRQuant Team
日期: 2026-01-10
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np

# 确保项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class SimpleHighReturnMiner:
    """简单高回报股票挖掘器
    
    核心逻辑：
    1. 批量获取指定时间段的所有股票价格数据
    2. 计算各周期回报率（短期5日、中期20日、长期60日）
    3. 筛选超过阈值的高回报案例
    4. 输出案例列表供后续因子分析
    """
    
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
    
    def get_stock_universe(self, date: str, max_stocks: int = 500) -> List[str]:
        """获取股票池
        
        Args:
            date: 日期
            max_stocks: 最大股票数量
        
        Returns:
            股票代码列表
        """
        if not self.jq:
            return []
        
        all_stocks = self.jq.get_all_securities(types=['stock'], date=date)
        
        # 过滤：排除ST、新股（上市不满1年）
        one_year_ago = (pd.to_datetime(date) - timedelta(days=365)).strftime('%Y-%m-%d')
        
        valid = all_stocks[
            ~all_stocks['display_name'].str.contains('ST|\\*|退', na=False) &
            (all_stocks['start_date'].astype(str) < one_year_ago)
        ]
        
        # 随机采样或全部
        stocks = valid.index.tolist()
        if len(stocks) > max_stocks:
            # 按市值或其他方式选择，这里简单截取
            stocks = stocks[:max_stocks]
        
        self._log(f"📊 股票池: {len(stocks)}只股票")
        return stocks
    
    def load_price_data(self, stocks: List[str], start_date: str, end_date: str) -> pd.DataFrame:
        """批量加载价格数据
        
        Args:
            stocks: 股票列表
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            包含 date, code, close 等列的 DataFrame
        """
        if not self.jq:
            return pd.DataFrame()
        
        # 扩展开始日期以计算回报率所需的历史数据
        ext_start = (pd.to_datetime(start_date) - timedelta(days=120)).strftime('%Y-%m-%d')
        
        self._log(f"📥 加载价格数据: {ext_start} ~ {end_date}")
        
        # 关键：panel=False 返回长格式 DataFrame
        price_data = self.jq.get_price(
            stocks,
            start_date=ext_start,
            end_date=end_date,
            frequency='daily',
            fields=['close', 'volume', 'money'],
            skip_paused=True,
            fq='post',  # 后复权
            panel=False
        )
        
        if price_data is None or price_data.empty:
            self._log("❌ 价格数据为空")
            return pd.DataFrame()
        
        # 标准化列名
        if 'time' in price_data.columns:
            price_data = price_data.rename(columns={'time': 'date'})
        
        price_data['date'] = pd.to_datetime(price_data['date']).dt.strftime('%Y-%m-%d')
        
        self._log(f"✅ 加载 {len(price_data)} 条价格记录, {price_data['code'].nunique()} 只股票")
        
        return price_data
    
    def calculate_returns(self, price_data: pd.DataFrame) -> pd.DataFrame:
        """计算各周期回报率
        
        Args:
            price_data: 价格数据 (date, code, close, ...)
        
        Returns:
            添加了回报率列的 DataFrame
        """
        if price_data.empty:
            return price_data
        
        self._log("📊 计算回报率...")
        
        # 按股票分组计算
        result_list = []
        
        for code, group in price_data.groupby('code'):
            df = group.sort_values('date').copy()
            
            # 计算各周期回报率（往前看）
            df['return_5d'] = df['close'].pct_change(5).shift(-5) * 100  # 5日后回报
            df['return_20d'] = df['close'].pct_change(20).shift(-20) * 100  # 20日后回报
            df['return_60d'] = df['close'].pct_change(60).shift(-60) * 100  # 60日后回报
            
            # 也计算往前看的回报（即当前价格相对N日前的涨幅）
            df['mom_5d'] = df['close'].pct_change(5) * 100  # 5日动量
            df['mom_20d'] = df['close'].pct_change(20) * 100  # 20日动量
            df['mom_60d'] = df['close'].pct_change(60) * 100  # 60日动量
            
            result_list.append(df)
        
        result = pd.concat(result_list, ignore_index=True)
        self._log(f"✅ 回报率计算完成")
        
        return result
    
    def find_high_return_cases(
        self,
        price_data: pd.DataFrame,
        start_date: str,
        end_date: str,
        min_return_5d: float = 8.0,
        min_return_20d: float = 20.0,
        min_return_60d: float = 50.0,
        max_cases: int = 1000
    ) -> Dict[str, pd.DataFrame]:
        """查找高回报案例
        
        Args:
            price_data: 带回报率的价格数据
            start_date: 筛选开始日期
            end_date: 筛选结束日期
            min_return_5d: 5日最小回报率阈值
            min_return_20d: 20日最小回报率阈值
            min_return_60d: 60日最小回报率阈值
            max_cases: 最大案例数
        
        Returns:
            {'short': DataFrame, 'medium': DataFrame, 'long': DataFrame}
        """
        if price_data.empty:
            return {}
        
        # 只在目标时间范围内筛选
        mask = (price_data['date'] >= start_date) & (price_data['date'] <= end_date)
        filtered = price_data[mask].copy()
        
        self._log(f"📊 在 {start_date} ~ {end_date} 范围内筛选高回报案例")
        self._log(f"   数据点: {len(filtered)}")
        
        results = {}
        
        # 短期高回报（5日 >= 8%）
        short_cases = filtered[filtered['return_5d'] >= min_return_5d].copy()
        short_cases = short_cases.nlargest(max_cases, 'return_5d')
        results['short'] = short_cases
        self._log(f"   短期(5日>={min_return_5d}%): {len(short_cases)} 案例")
        
        # 中期高回报（20日 >= 20%）
        medium_cases = filtered[filtered['return_20d'] >= min_return_20d].copy()
        medium_cases = medium_cases.nlargest(max_cases, 'return_20d')
        results['medium'] = medium_cases
        self._log(f"   中期(20日>={min_return_20d}%): {len(medium_cases)} 案例")
        
        # 长期高回报（60日 >= 50%）
        long_cases = filtered[filtered['return_60d'] >= min_return_60d].copy()
        long_cases = long_cases.nlargest(max_cases, 'return_60d')
        results['long'] = long_cases
        self._log(f"   长期(60日>={min_return_60d}%): {len(long_cases)} 案例")
        
        return results
    
    def mine(
        self,
        start_date: str,
        end_date: str,
        max_stocks: int = 500,
        min_return_5d: float = 8.0,
        min_return_20d: float = 20.0,
        min_return_60d: float = 50.0,
    ) -> Dict[str, pd.DataFrame]:
        """执行挖掘
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            max_stocks: 最大股票数
            min_return_5d: 5日最小回报率
            min_return_20d: 20日最小回报率
            min_return_60d: 60日最小回报率
        
        Returns:
            {'short': DataFrame, 'medium': DataFrame, 'long': DataFrame}
        """
        self._log(f"\n{'='*60}")
        self._log(f"🔍 开始挖掘高回报股票")
        self._log(f"   时间范围: {start_date} ~ {end_date}")
        self._log(f"   阈值: 5日>={min_return_5d}%, 20日>={min_return_20d}%, 60日>={min_return_60d}%")
        self._log(f"{'='*60}\n")
        
        # Step 1: 获取股票池
        stocks = self.get_stock_universe(end_date, max_stocks)
        if not stocks:
            self._log("❌ 股票池为空")
            return {}
        
        # Step 2: 加载价格数据
        price_data = self.load_price_data(stocks, start_date, end_date)
        if price_data.empty:
            self._log("❌ 价格数据为空")
            return {}
        
        # Step 3: 计算回报率
        price_data = self.calculate_returns(price_data)
        
        # Step 4: 筛选高回报案例
        results = self.find_high_return_cases(
            price_data, start_date, end_date,
            min_return_5d, min_return_20d, min_return_60d
        )
        
        # 统计
        total = sum(len(df) for df in results.values())
        self._log(f"\n✅ 挖掘完成，共找到 {total} 个高回报案例")
        
        return results
    
    def save_results(self, results: Dict[str, pd.DataFrame], output_dir: str):
        """保存结果到文件
        
        Args:
            results: mine() 返回的结果
            output_dir: 输出目录
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for period, df in results.items():
            if not df.empty:
                file_path = output_path / f"high_return_{period}.csv"
                df.to_csv(file_path, index=False)
                self._log(f"💾 保存 {period} 案例到: {file_path}")


def main():
    """测试入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='简单高回报股票挖掘器')
    parser.add_argument('--start-date', default='2019-01-01', help='开始日期')
    parser.add_argument('--end-date', default='2019-06-30', help='结束日期')
    parser.add_argument('--max-stocks', type=int, default=200, help='最大股票数')
    parser.add_argument('--min-return-5d', type=float, default=8.0, help='5日最小回报率')
    parser.add_argument('--min-return-20d', type=float, default=20.0, help='20日最小回报率')
    parser.add_argument('--min-return-60d', type=float, default=50.0, help='60日最小回报率')
    parser.add_argument('--output-dir', default='output/research/high_return_cases', help='输出目录')
    
    args = parser.parse_args()
    
    miner = SimpleHighReturnMiner(verbose=True)
    
    results = miner.mine(
        start_date=args.start_date,
        end_date=args.end_date,
        max_stocks=args.max_stocks,
        min_return_5d=args.min_return_5d,
        min_return_20d=args.min_return_20d,
        min_return_60d=args.min_return_60d,
    )
    
    if results:
        miner.save_results(results, args.output_dir)
        
        # 打印示例
        for period, df in results.items():
            if not df.empty:
                print(f"\n📈 {period.upper()} 案例示例 (前5):")
                print(df[['date', 'code', 'close', f'return_{5 if period=="short" else 20 if period=="medium" else 60}d']].head())


if __name__ == '__main__':
    main()
