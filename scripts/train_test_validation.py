#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
训练集/测试集分离验证

训练集: 2024-09-01 ~ 2025-08-31 (密集滚动验证，优化参数)
测试集: 2025-09-01 ~ 至今 (独立验证，检验过拟合)

这是标准的机器学习验证方法，用于验证投资推荐系统的可靠性
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TrainTestValidator:
    """训练集/测试集分离验证器"""
    
    def __init__(self):
        self.jq = None
        self._init_jqdata()
        
        # 筛选参数（可调优）
        self.params = {
            "market_cap_min": 30,
            "market_cap_max": 800,
            "roe_min": 8,
            "growth_min": 15,
            "ret_20d_min": -10,
            "ret_20d_max": 40,
        }
        
        self.train_results = []
        self.test_results = []
    
    def _init_jqdata(self):
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            config_mgr = get_config_manager()
            jq_config = config_mgr.get_config('jqdata')
            if jq_config:
                jq.auth(jq_config.get('username'), jq_config.get('password'))
                if jq.is_auth():
                    self.jq = jq
                    logger.info("JQData初始化成功")
        except Exception as e:
            logger.warning(f"JQData初始化失败: {e}")
    
    def get_trade_dates(self, start_date: str, end_date: str, interval: int = 15) -> List[str]:
        """获取交易日列表（每隔interval天取一个）"""
        if not self.jq:
            return []
        
        trade_days = self.jq.get_trade_days(start_date=start_date, end_date=end_date)
        dates = [d.strftime("%Y-%m-%d") for d in trade_days[::interval]]
        return dates
    
    def get_stock_recommendations(self, date: str, top_n: int = 15) -> List[Dict]:
        """获取指定日期的股票推荐"""
        if not self.jq:
            return []
        
        try:
            # 获取所有A股
            stocks = self.jq.get_all_securities(types=['stock'], date=date)
            stocks = stocks[~stocks.index.str.startswith('688')]  # 排除科创板
            stocks = stocks[~stocks['display_name'].str.contains('ST')]  # 排除ST
            stock_list = stocks.index.tolist()[:1000]
            
            # 获取基本面数据
            q = self.jq.query(
                self.jq.valuation.code,
                self.jq.valuation.market_cap,
                self.jq.indicator.roe,
                self.jq.indicator.inc_net_profit_year_on_year,
            ).filter(
                self.jq.valuation.code.in_(stock_list),
                self.jq.valuation.market_cap.between(
                    self.params["market_cap_min"], 
                    self.params["market_cap_max"]
                ),
            )
            
            df = self.jq.get_fundamentals(q, date=date)
            
            if df is None or df.empty:
                return []
            
            # 筛选
            df = df[df['roe'] > self.params["roe_min"]]
            df = df[df['inc_net_profit_year_on_year'] > self.params["growth_min"]]
            df = df.dropna()
            
            if df.empty:
                return []
            
            # 获取近期涨幅进行二次筛选
            end_dt = datetime.strptime(date, "%Y-%m-%d")
            start_dt = end_dt - timedelta(days=30)
            
            results = []
            for code in df['code'].head(top_n * 3).tolist():
                try:
                    price_df = self.jq.get_price(
                        code,
                        start_date=start_dt.strftime("%Y-%m-%d"),
                        end_date=date,
                        frequency='daily',
                        fields=['close']
                    )
                    
                    if price_df is not None and len(price_df) >= 10:
                        ret_20d = (price_df.iloc[-1]['close'] / price_df.iloc[0]['close'] - 1) * 100
                        
                        # 排除暴涨暴跌
                        if self.params["ret_20d_min"] < ret_20d < self.params["ret_20d_max"]:
                            stock_info = df[df['code'] == code].iloc[0]
                            
                            # 获取名称
                            sec_info = self.jq.get_security_info(code)
                            name = sec_info.display_name if sec_info else code
                            
                            # 综合评分
                            score = (
                                stock_info['roe'] * 0.4 + 
                                stock_info['inc_net_profit_year_on_year'] * 0.4 - 
                                abs(ret_20d) * 0.2
                            )
                            
                            results.append({
                                "code": code,
                                "name": name,
                                "market_cap": stock_info['market_cap'],
                                "roe": stock_info['roe'],
                                "growth": stock_info['inc_net_profit_year_on_year'],
                                "ret_20d": ret_20d,
                                "score": score,
                            })
                except:
                    continue
            
            # 按评分排序
            results = sorted(results, key=lambda x: x['score'], reverse=True)
            return results[:top_n]
            
        except Exception as e:
            logger.warning(f"获取推荐失败 {date}: {e}")
            return []
    
    def get_stock_returns(self, stock_code: str, start_date: str) -> Dict[str, float]:
        """获取股票未来收益"""
        if not self.jq:
            return {}
        
        try:
            end_dt = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=35)
            
            df = self.jq.get_price(
                stock_code,
                start_date=start_date,
                end_date=end_dt.strftime("%Y-%m-%d"),
                frequency='daily',
                fields=['close'],
                skip_paused=True,
                fq='post'
            )
            
            if df is None or len(df) < 2:
                return {}
            
            df = df.reset_index()
            df.columns = ['date', 'close']
            base = df.iloc[0]['close']
            
            returns = {"base_price": base}
            
            if len(df) > 5:
                returns['ret_5d'] = (df.iloc[5]['close'] / base - 1) * 100
            if len(df) > 10:
                returns['ret_10d'] = (df.iloc[10]['close'] / base - 1) * 100
            if len(df) > 20:
                returns['ret_20d'] = (df.iloc[20]['close'] / base - 1) * 100
            else:
                returns['ret_20d'] = (df.iloc[-1]['close'] / base - 1) * 100
            
            # 最大收益和最大回撤
            cum_ret = (df['close'] / base - 1) * 100
            returns['ret_max'] = cum_ret.max()
            returns['ret_min'] = cum_ret.min()
            
            return returns
        except:
            return {}
    
    def get_benchmark_returns(self, start_date: str) -> Dict[str, float]:
        """获取基准收益"""
        return self.get_stock_returns("000300.XSHG", start_date)
    
    def validate_period(self, date: str, top_n: int = 15) -> Dict[str, Any]:
        """验证单个周期"""
        # 获取推荐
        recommendations = self.get_stock_recommendations(date, top_n=top_n)
        
        if not recommendations:
            return {"date": date, "stocks": [], "metrics": None}
        
        # 获取基准收益
        bench = self.get_benchmark_returns(date)
        bench_20d = bench.get('ret_20d', 0)
        
        # 验证每只股票
        stock_results = []
        for rec in recommendations:
            returns = self.get_stock_returns(rec['code'], date)
            if returns and 'ret_20d' in returns:
                stock_results.append({
                    "code": rec['code'],
                    "name": rec['name'],
                    "roe": rec['roe'],
                    "growth": rec['growth'],
                    "ret_5d": returns.get('ret_5d', 0),
                    "ret_10d": returns.get('ret_10d', 0),
                    "ret_20d": returns.get('ret_20d', 0),
                    "ret_max": returns.get('ret_max', 0),
                    "ret_min": returns.get('ret_min', 0),
                    "alpha_20d": returns.get('ret_20d', 0) - bench_20d,
                })
        
        if not stock_results:
            return {"date": date, "stocks": [], "metrics": None}
        
        # 计算指标
        metrics = {
            "n_stocks": len(stock_results),
            "avg_ret_5d": np.mean([s['ret_5d'] for s in stock_results]),
            "avg_ret_10d": np.mean([s['ret_10d'] for s in stock_results]),
            "avg_ret_20d": np.mean([s['ret_20d'] for s in stock_results]),
            "win_rate_5d": sum(1 for s in stock_results if s['ret_5d'] > 0) / len(stock_results),
            "win_rate_10d": sum(1 for s in stock_results if s['ret_10d'] > 0) / len(stock_results),
            "win_rate_20d": sum(1 for s in stock_results if s['ret_20d'] > 0) / len(stock_results),
            "avg_alpha_20d": np.mean([s['alpha_20d'] for s in stock_results]),
            "hit_rate": sum(1 for s in stock_results if s['alpha_20d'] > 0) / len(stock_results),
            "bench_20d": bench_20d,
        }
        
        return {"date": date, "stocks": stock_results, "metrics": metrics}
    
    def run_train_validation(
        self,
        train_start: str = "2024-09-01",
        train_end: str = "2025-08-31",
        interval: int = 10,  # 每10天验证一次（密集）
        top_n: int = 15,
    ) -> Dict[str, Any]:
        """运行训练集验证"""
        print("=" * 70)
        print("训练集验证（密集滚动）")
        print("=" * 70)
        print(f"周期: {train_start} ~ {train_end}")
        print(f"间隔: 每 {interval} 个交易日")
        print(f"每期推荐: {top_n} 只")
        
        dates = self.get_trade_dates(train_start, train_end, interval)
        print(f"验证日期数: {len(dates)}")
        
        self.train_results = []
        
        for i, date in enumerate(dates):
            print(f"\r[{i+1}/{len(dates)}] {date}", end="", flush=True)
            result = self.validate_period(date, top_n=top_n)
            self.train_results.append(result)
        
        print()
        
        # 汇总
        summary = self._calculate_summary(self.train_results, "训练集")
        return summary
    
    def run_test_validation(
        self,
        test_start: str = "2025-09-01",
        test_end: str = None,
        interval: int = 10,
        top_n: int = 15,
    ) -> Dict[str, Any]:
        """运行测试集验证"""
        if test_end is None:
            test_end = datetime.now().strftime("%Y-%m-%d")
        
        print("\n" + "=" * 70)
        print("测试集验证（独立验证）")
        print("=" * 70)
        print(f"周期: {test_start} ~ {test_end}")
        print(f"间隔: 每 {interval} 个交易日")
        print(f"每期推荐: {top_n} 只")
        
        dates = self.get_trade_dates(test_start, test_end, interval)
        print(f"验证日期数: {len(dates)}")
        
        self.test_results = []
        
        for i, date in enumerate(dates):
            print(f"\r[{i+1}/{len(dates)}] {date}", end="", flush=True)
            result = self.validate_period(date, top_n=top_n)
            self.test_results.append(result)
        
        print()
        
        # 汇总
        summary = self._calculate_summary(self.test_results, "测试集")
        return summary
    
    def _calculate_summary(self, results: List[Dict], name: str) -> Dict[str, Any]:
        """计算汇总统计"""
        all_stocks = []
        valid_periods = 0
        
        for r in results:
            if r['stocks']:
                all_stocks.extend(r['stocks'])
                valid_periods += 1
        
        if not all_stocks:
            print(f"\n{name}: 无有效数据")
            return {}
        
        # 收集所有收益
        rets_5d = [s['ret_5d'] for s in all_stocks]
        rets_10d = [s['ret_10d'] for s in all_stocks]
        rets_20d = [s['ret_20d'] for s in all_stocks]
        alphas = [s['alpha_20d'] for s in all_stocks]
        
        summary = {
            "name": name,
            "total_periods": len(results),
            "valid_periods": valid_periods,
            "total_recommendations": len(all_stocks),
            
            # 收益率
            "avg_return_5d": np.mean(rets_5d),
            "avg_return_10d": np.mean(rets_10d),
            "avg_return_20d": np.mean(rets_20d),
            
            # 胜率
            "win_rate_5d": sum(1 for r in rets_5d if r > 0) / len(rets_5d),
            "win_rate_10d": sum(1 for r in rets_10d if r > 0) / len(rets_10d),
            "win_rate_20d": sum(1 for r in rets_20d if r > 0) / len(rets_20d),
            
            # 超额收益
            "avg_alpha_20d": np.mean(alphas),
            "hit_rate": sum(1 for a in alphas if a > 0) / len(alphas),
            
            # 风险指标
            "volatility": np.std(rets_20d),
            "max_loss": min(rets_20d),
            "max_gain": max(rets_20d),
            
            # 夏普比率
            "sharpe_ratio": (np.mean(rets_20d) - 0.25) / np.std(rets_20d) if np.std(rets_20d) > 0 else 0,
            
            # 一致性
            "consistency": sum(1 for r in results if r['metrics'] and r['metrics'].get('avg_ret_20d', 0) > 0) / valid_periods if valid_periods > 0 else 0,
        }
        
        self._print_summary(summary)
        return summary
    
    def _print_summary(self, s: Dict):
        """打印汇总"""
        print(f"\n{'='*50}")
        print(f"{s['name']} 汇总统计")
        print(f"{'='*50}")
        
        print(f"\n📊 基本统计:")
        print(f"  - 验证周期数: {s['valid_periods']} / {s['total_periods']}")
        print(f"  - 总推荐数量: {s['total_recommendations']}")
        
        print(f"\n📈 收益率指标:")
        print(f"  {'指标':<12} {'5日':<12} {'10日':<12} {'20日':<12}")
        print(f"  {'-'*48}")
        print(f"  {'平均收益':<12} {s['avg_return_5d']:>8.2f}%    {s['avg_return_10d']:>8.2f}%    {s['avg_return_20d']:>8.2f}%")
        print(f"  {'胜率':<12} {s['win_rate_5d']:>8.1%}    {s['win_rate_10d']:>8.1%}    {s['win_rate_20d']:>8.1%}")
        
        print(f"\n📊 超额收益:")
        print(f"  - 平均超额收益(20日): {s['avg_alpha_20d']:.2f}%")
        print(f"  - 命中率(超额>0): {s['hit_rate']:.1%}")
        
        print(f"\n📉 风险指标:")
        print(f"  - 夏普比率: {s['sharpe_ratio']:.3f}")
        print(f"  - 波动率: {s['volatility']:.2f}%")
        print(f"  - 最大单笔亏损: {s['max_loss']:.2f}%")
        print(f"  - 最大单笔盈利: {s['max_gain']:.2f}%")
        
        print(f"\n✅ 一致性:")
        print(f"  - 跨周期盈利比例: {s['consistency']:.1%}")
    
    def compare_train_test(self):
        """对比训练集和测试集结果"""
        if not self.train_results or not self.test_results:
            print("请先运行训练集和测试集验证")
            return
        
        train_summary = self._get_summary_dict(self.train_results)
        test_summary = self._get_summary_dict(self.test_results)
        
        print("\n" + "=" * 70)
        print("训练集 vs 测试集 对比")
        print("=" * 70)
        
        print(f"\n{'指标':<20} {'训练集':<15} {'测试集':<15} {'差异':<15}")
        print("-" * 65)
        
        metrics = [
            ("平均20日收益", "avg_return_20d", "%"),
            ("20日胜率", "win_rate_20d", "%"),
            ("超额收益", "avg_alpha_20d", "%"),
            ("命中率", "hit_rate", "%"),
            ("夏普比率", "sharpe_ratio", ""),
            ("跨周期一致性", "consistency", "%"),
        ]
        
        for name, key, suffix in metrics:
            train_val = train_summary.get(key, 0)
            test_val = test_summary.get(key, 0)
            diff = test_val - train_val
            
            if suffix == "%":
                if key in ["win_rate_20d", "hit_rate", "consistency"]:
                    print(f"{name:<20} {train_val:>10.1%}     {test_val:>10.1%}     {diff:>+10.1%}")
                else:
                    print(f"{name:<20} {train_val:>10.2f}%    {test_val:>10.2f}%    {diff:>+10.2f}%")
            else:
                print(f"{name:<20} {train_val:>12.3f}   {test_val:>12.3f}   {diff:>+12.3f}")
        
        # 评价
        print(f"\n📝 过拟合检测:")
        
        alpha_diff = test_summary.get('avg_alpha_20d', 0) - train_summary.get('avg_alpha_20d', 0)
        if abs(alpha_diff) < 2:
            print("  ✅ 超额收益稳定，无明显过拟合")
        elif alpha_diff < -5:
            print("  ❌ 测试集超额收益明显下降，可能存在过拟合")
        else:
            print("  ⚠️ 测试集和训练集有差异，需关注")
        
        hit_diff = test_summary.get('hit_rate', 0) - train_summary.get('hit_rate', 0)
        if abs(hit_diff) < 0.1:
            print("  ✅ 命中率稳定，选股逻辑有效")
        elif hit_diff < -0.15:
            print("  ❌ 测试集命中率下降明显，选股逻辑可能失效")
        else:
            print("  ⚠️ 命中率有波动，需持续观察")
        
        if test_summary.get('avg_alpha_20d', 0) > 0 and test_summary.get('hit_rate', 0) > 0.5:
            print("\n  🎯 结论: 系统在测试集上表现良好，可信度高")
        else:
            print("\n  ⚠️ 结论: 系统需要进一步优化")
    
    def _get_summary_dict(self, results: List[Dict]) -> Dict:
        """计算汇总字典"""
        all_stocks = []
        valid_periods = 0
        
        for r in results:
            if r['stocks']:
                all_stocks.extend(r['stocks'])
                valid_periods += 1
        
        if not all_stocks:
            return {}
        
        rets_20d = [s['ret_20d'] for s in all_stocks]
        alphas = [s['alpha_20d'] for s in all_stocks]
        
        return {
            "avg_return_20d": np.mean(rets_20d),
            "win_rate_20d": sum(1 for r in rets_20d if r > 0) / len(rets_20d),
            "avg_alpha_20d": np.mean(alphas),
            "hit_rate": sum(1 for a in alphas if a > 0) / len(alphas),
            "sharpe_ratio": (np.mean(rets_20d) - 0.25) / np.std(rets_20d) if np.std(rets_20d) > 0 else 0,
            "consistency": sum(1 for r in results if r['metrics'] and r['metrics'].get('avg_ret_20d', 0) > 0) / valid_periods if valid_periods > 0 else 0,
        }
    
    def get_all_results_df(self) -> pd.DataFrame:
        """获取所有结果的DataFrame"""
        records = []
        
        for dataset, results in [("训练集", self.train_results), ("测试集", self.test_results)]:
            for r in results:
                for s in r['stocks']:
                    records.append({
                        "数据集": dataset,
                        "推荐日期": r['date'],
                        "股票代码": s['code'],
                        "股票名称": s['name'],
                        "ROE": s['roe'],
                        "增长率": s['growth'],
                        "5日收益%": s['ret_5d'],
                        "10日收益%": s['ret_10d'],
                        "20日收益%": s['ret_20d'],
                        "最大收益%": s['ret_max'],
                        "最大回撤%": s['ret_min'],
                        "超额收益%": s['alpha_20d'],
                    })
        
        return pd.DataFrame(records)
    
    def save_results(self, output_dir: str = "results"):
        """保存结果"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        df = self.get_all_results_df()
        if not df.empty:
            csv_path = f"{output_dir}/train_test_validation_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"\n详细结果已保存: {csv_path}")


def main():
    validator = TrainTestValidator()
    
    # 训练集验证（密集）
    train_summary = validator.run_train_validation(
        train_start="2024-09-01",
        train_end="2025-08-31",
        interval=10,  # 每10天
        top_n=15,
    )
    
    # 测试集验证
    test_summary = validator.run_test_validation(
        test_start="2025-09-01",
        test_end=None,  # 至今
        interval=10,
        top_n=15,
    )
    
    # 对比
    validator.compare_train_test()
    
    # 保存结果
    validator.save_results()


if __name__ == "__main__":
    main()
