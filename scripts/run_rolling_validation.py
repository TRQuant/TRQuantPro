#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行投资推荐系统的滚动验证

这个脚本验证投资推荐系统的可靠性：
1. 使用训练集/测试集分离（Walk-forward）
2. 计算直观的量化指标（收益率、夏普比率、胜率）
3. 验证是否存在过拟合

使用方法:
    python scripts/run_rolling_validation.py --months 12
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SimpleStockRecommender:
    """
    简化的选股推荐器
    
    使用市场趋势分析 + 基本面筛选来生成推荐
    这样可以更快速地进行滚动验证
    """
    
    def __init__(self):
        self.jq = None
        self._init_jqdata()
    
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
    
    def get_market_trend(self, date: str) -> Dict[str, Any]:
        """获取市场趋势"""
        try:
            from core.market_trend_analyzer import MarketTrendAnalyzer, MarketTrendAnalyzerConfig
            
            config = MarketTrendAnalyzerConfig()
            analyzer = MarketTrendAnalyzer(config)
            signal = analyzer.analyze("000300.XSHG", as_of_date=date)
            
            if signal:
                return {
                    "score": signal.ensemble_score,
                    "position_cap": signal.workflow_params.position_target,
                    "market_phase": signal.market_phase.value if signal.market_phase else "unknown",
                }
            return {"score": 0, "position_cap": 0.5, "market_phase": "unknown"}
        except Exception as e:
            logger.warning(f"市场趋势分析失败: {e}")
            return {"score": 0, "position_cap": 0.5, "market_phase": "unknown"}
    
    def get_stock_pool(self, date: str, top_n: int = 20) -> List[Dict]:
        """
        获取推荐股票池
        
        筛选条件：
        1. 市值50-500亿
        2. ROE > 10%
        3. 净利润增长 > 20%
        4. 技术面：近期涨幅适中
        """
        if not self.jq:
            return []
        
        try:
            # 获取所有A股
            stocks = self.jq.get_all_securities(types=['stock'], date=date)
            stocks = stocks[~stocks.index.str.startswith('688')]  # 排除科创板
            stocks = stocks[~stocks.index.str.contains('ST')]
            stock_list = stocks.index.tolist()[:500]  # 限制数量
            
            # 获取基本面数据
            q = self.jq.query(
                self.jq.valuation.code,
                self.jq.valuation.market_cap,
                self.jq.valuation.pe_ratio,
                self.jq.indicator.roe,
                self.jq.indicator.inc_net_profit_year_on_year,
            ).filter(
                self.jq.valuation.code.in_(stock_list),
                self.jq.valuation.market_cap.between(50, 500),  # 50-500亿市值
            )
            
            df = self.jq.get_fundamentals(q, date=date)
            
            if df is None or df.empty:
                return []
            
            # 筛选
            df = df[df['roe'] > 10]  # ROE > 10%
            df = df[df['inc_net_profit_year_on_year'] > 20]  # 增长 > 20%
            df = df.dropna()
            
            if df.empty:
                return []
            
            # 获取近期涨幅
            end_dt = datetime.strptime(date, "%Y-%m-%d")
            start_dt = end_dt - timedelta(days=30)
            
            results = []
            for code in df['code'].head(top_n * 2).tolist():
                try:
                    price_df = self.jq.get_price(
                        code,
                        start_date=start_dt.strftime("%Y-%m-%d"),
                        end_date=date,
                        frequency='daily',
                        fields=['close']
                    )
                    
                    if price_df is not None and len(price_df) >= 5:
                        ret_20d = (price_df.iloc[-1]['close'] / price_df.iloc[0]['close'] - 1) * 100
                        
                        # 涨幅在 -5% ~ 30% 之间（排除暴涨暴跌）
                        if -5 < ret_20d < 30:
                            stock_info = df[df['code'] == code].iloc[0]
                            
                            # 获取名称
                            sec_info = self.jq.get_security_info(code)
                            name = sec_info.display_name if sec_info else code
                            
                            results.append({
                                "code": code,
                                "name": name,
                                "market_cap": stock_info['market_cap'],
                                "roe": stock_info['roe'],
                                "growth": stock_info['inc_net_profit_year_on_year'],
                                "ret_20d": ret_20d,
                                "score": stock_info['roe'] * 0.4 + stock_info['inc_net_profit_year_on_year'] * 0.4 - abs(ret_20d) * 0.2,
                            })
                except:
                    continue
            
            # 按综合分排序
            results = sorted(results, key=lambda x: x['score'], reverse=True)
            return results[:top_n]
            
        except Exception as e:
            logger.warning(f"获取股票池失败: {e}")
            return []
    
    def recommend(self, date: str, top_n: int = 10) -> List[Dict]:
        """生成推荐"""
        # 获取市场趋势
        trend = self.get_market_trend(date)
        
        # 获取股票池
        pool = self.get_stock_pool(date, top_n=top_n * 2)
        
        # 根据市场环境调整推荐数量
        if trend['position_cap'] < 0.3:
            actual_n = max(3, int(top_n * 0.5))  # 弱市少推荐
        elif trend['position_cap'] > 0.7:
            actual_n = top_n  # 强市正常推荐
        else:
            actual_n = int(top_n * 0.7)
        
        return pool[:actual_n]


class SimpleRollingValidator:
    """
    简化的滚动验证器
    
    直接验证选股效果，不依赖复杂的V3工作流
    """
    
    def __init__(
        self,
        train_months: int = 3,
        test_months: int = 1,
        step_months: int = 1,
        top_n: int = 10,
    ):
        self.train_months = train_months
        self.test_months = test_months
        self.step_months = step_months
        self.top_n = top_n
        
        self.recommender = SimpleStockRecommender()
        self.jq = self.recommender.jq
        
        self.results = []
    
    def get_stock_returns(self, stock_code: str, start_date: str) -> Dict[str, float]:
        """获取股票未来收益"""
        if not self.jq:
            return {}
        
        try:
            end_dt = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=30)
            
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
            
            returns = {}
            if len(df) > 5:
                returns['ret_5d'] = (df.iloc[5]['close'] / base - 1) * 100
            if len(df) > 10:
                returns['ret_10d'] = (df.iloc[10]['close'] / base - 1) * 100
            if len(df) > 20:
                returns['ret_20d'] = (df.iloc[20]['close'] / base - 1) * 100
            else:
                returns['ret_20d'] = (df.iloc[-1]['close'] / base - 1) * 100
            
            returns['ret_max'] = ((df['close'] / base - 1) * 100).max()
            returns['ret_min'] = ((df['close'] / base - 1) * 100).min()
            
            return returns
        except:
            return {}
    
    def get_benchmark_returns(self, start_date: str) -> Dict[str, float]:
        """获取基准收益"""
        return self.get_stock_returns("000300.XSHG", start_date)
    
    def validate_period(self, test_date: str) -> Dict[str, Any]:
        """验证单个周期"""
        # 获取推荐
        recommendations = self.recommender.recommend(test_date, top_n=self.top_n)
        
        if not recommendations:
            return {"date": test_date, "stocks": [], "metrics": {}}
        
        # 获取基准收益
        bench = self.get_benchmark_returns(test_date)
        
        # 验证每只股票
        stock_results = []
        for rec in recommendations:
            returns = self.get_stock_returns(rec['code'], test_date)
            if returns:
                stock_results.append({
                    "code": rec['code'],
                    "name": rec['name'],
                    "ret_5d": returns.get('ret_5d', 0),
                    "ret_10d": returns.get('ret_10d', 0),
                    "ret_20d": returns.get('ret_20d', 0),
                    "ret_max": returns.get('ret_max', 0),
                    "ret_min": returns.get('ret_min', 0),
                    "alpha_5d": returns.get('ret_5d', 0) - bench.get('ret_5d', 0),
                    "alpha_10d": returns.get('ret_10d', 0) - bench.get('ret_10d', 0),
                    "alpha_20d": returns.get('ret_20d', 0) - bench.get('ret_20d', 0),
                })
        
        # 计算指标
        if stock_results:
            metrics = {
                "avg_ret_5d": np.mean([s['ret_5d'] for s in stock_results]),
                "avg_ret_10d": np.mean([s['ret_10d'] for s in stock_results]),
                "avg_ret_20d": np.mean([s['ret_20d'] for s in stock_results]),
                "win_rate_5d": sum(1 for s in stock_results if s['ret_5d'] > 0) / len(stock_results),
                "win_rate_10d": sum(1 for s in stock_results if s['ret_10d'] > 0) / len(stock_results),
                "win_rate_20d": sum(1 for s in stock_results if s['ret_20d'] > 0) / len(stock_results),
                "avg_alpha_5d": np.mean([s['alpha_5d'] for s in stock_results]),
                "avg_alpha_10d": np.mean([s['alpha_10d'] for s in stock_results]),
                "avg_alpha_20d": np.mean([s['alpha_20d'] for s in stock_results]),
                "bench_5d": bench.get('ret_5d', 0),
                "bench_10d": bench.get('ret_10d', 0),
                "bench_20d": bench.get('ret_20d', 0),
            }
        else:
            metrics = {}
        
        return {
            "date": test_date,
            "stocks": stock_results,
            "metrics": metrics,
        }
    
    def run(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """运行滚动验证"""
        print("=" * 70)
        print("投资推荐系统 - 滚动验证（Walk-forward Validation）")
        print("=" * 70)
        print(f"\n验证参数:")
        print(f"  - 训练期: {self.train_months} 个月")
        print(f"  - 测试期: {self.test_months} 个月")
        print(f"  - 每期推荐数: {self.top_n}")
        print(f"  - 验证区间: {start_date} ~ {end_date}")
        
        # 生成测试日期列表
        test_dates = []
        current = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=self.train_months * 30)
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current < end_dt:
            # 获取最近的交易日
            try:
                trade_days = self.jq.get_trade_days(
                    start_date=(current - timedelta(days=7)).strftime("%Y-%m-%d"),
                    end_date=current.strftime("%Y-%m-%d")
                )
                if len(trade_days) > 0:
                    test_dates.append(trade_days[-1].strftime("%Y-%m-%d"))
            except:
                test_dates.append(current.strftime("%Y-%m-%d"))
            
            current += timedelta(days=self.step_months * 30)
        
        print(f"\n生成 {len(test_dates)} 个验证周期")
        
        # 验证
        self.results = []
        for i, date in enumerate(test_dates):
            print(f"\n[{i+1}/{len(test_dates)}] 验证日期: {date}")
            
            result = self.validate_period(date)
            self.results.append(result)
            
            if result['metrics']:
                m = result['metrics']
                print(f"  推荐 {len(result['stocks'])} 只股票")
                print(f"  5日: 收益 {m['avg_ret_5d']:.2f}% | 胜率 {m['win_rate_5d']:.1%} | 超额 {m['avg_alpha_5d']:.2f}%")
                print(f"  10日: 收益 {m['avg_ret_10d']:.2f}% | 胜率 {m['win_rate_10d']:.1%} | 超额 {m['avg_alpha_10d']:.2f}%")
                print(f"  20日: 收益 {m['avg_ret_20d']:.2f}% | 胜率 {m['win_rate_20d']:.1%} | 超额 {m['avg_alpha_20d']:.2f}%")
                print(f"  基准: 5日 {m['bench_5d']:.2f}% | 10日 {m['bench_10d']:.2f}% | 20日 {m['bench_20d']:.2f}%")
        
        # 汇总
        summary = self._calculate_summary()
        self._print_summary(summary)
        
        return summary
    
    def _calculate_summary(self) -> Dict[str, Any]:
        """计算汇总"""
        all_stocks = []
        for r in self.results:
            all_stocks.extend(r['stocks'])
        
        if not all_stocks:
            return {}
        
        # 收集所有收益
        rets_5d = [s['ret_5d'] for s in all_stocks]
        rets_10d = [s['ret_10d'] for s in all_stocks]
        rets_20d = [s['ret_20d'] for s in all_stocks]
        alphas_20d = [s['alpha_20d'] for s in all_stocks]
        
        summary = {
            "total_periods": len(self.results),
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
            "avg_alpha_5d": np.mean([s['alpha_5d'] for s in all_stocks]),
            "avg_alpha_10d": np.mean([s['alpha_10d'] for s in all_stocks]),
            "avg_alpha_20d": np.mean([s['alpha_20d'] for s in all_stocks]),
            
            # 风险指标
            "volatility": np.std(rets_20d),
            "max_drawdown": min(rets_20d),
            
            # 夏普比率 (假设无风险0.25%)
            "sharpe_ratio": (np.mean(rets_20d) - 0.25) / np.std(rets_20d) if np.std(rets_20d) > 0 else 0,
            
            # 命中率（超额收益>0）
            "hit_rate": sum(1 for a in alphas_20d if a > 0) / len(alphas_20d),
            
            # 跨周期一致性
            "consistency": sum(1 for r in self.results if r['metrics'] and r['metrics'].get('avg_ret_20d', 0) > 0) / len(self.results) if self.results else 0,
        }
        
        return summary
    
    def _print_summary(self, summary: Dict[str, Any]):
        """打印汇总"""
        if not summary:
            print("\n无有效数据")
            return
        
        print("\n" + "=" * 70)
        print("验证汇总结果")
        print("=" * 70)
        
        print(f"\n📊 基本统计:")
        print(f"  - 验证周期数: {summary['total_periods']}")
        print(f"  - 总推荐数量: {summary['total_recommendations']}")
        
        print(f"\n📈 收益率指标:")
        print(f"  {'指标':<12} {'5日':<12} {'10日':<12} {'20日':<12}")
        print(f"  {'-'*48}")
        print(f"  {'平均收益':<12} {summary['avg_return_5d']:>8.2f}%    {summary['avg_return_10d']:>8.2f}%    {summary['avg_return_20d']:>8.2f}%")
        print(f"  {'胜率':<12} {summary['win_rate_5d']:>8.1%}    {summary['win_rate_10d']:>8.1%}    {summary['win_rate_20d']:>8.1%}")
        print(f"  {'超额收益':<12} {summary['avg_alpha_5d']:>8.2f}%    {summary['avg_alpha_10d']:>8.2f}%    {summary['avg_alpha_20d']:>8.2f}%")
        
        print(f"\n📉 风险指标:")
        print(f"  - 夏普比率: {summary['sharpe_ratio']:.3f}")
        print(f"  - 最大单笔亏损: {summary['max_drawdown']:.2f}%")
        print(f"  - 收益波动率: {summary['volatility']:.2f}%")
        
        print(f"\n✅ 可靠性指标:")
        print(f"  - 命中率（超额收益>0）: {summary['hit_rate']:.1%}")
        print(f"  - 跨周期一致性: {summary['consistency']:.1%}")
        
        # 评价
        print(f"\n📝 综合评价:")
        
        if summary['sharpe_ratio'] > 1.5:
            print("  ✅ 夏普比率优秀（>1.5），风险调整后收益很好")
        elif summary['sharpe_ratio'] > 1.0:
            print("  ✅ 夏普比率良好（>1.0），具有投资价值")
        elif summary['sharpe_ratio'] > 0.5:
            print("  ⚠️ 夏普比率一般（0.5-1.0），需要优化")
        else:
            print("  ❌ 夏普比率较低（<0.5），不建议使用")
        
        if summary['hit_rate'] > 0.6:
            print("  ✅ 命中率较高（>60%），系统选股能力强")
        elif summary['hit_rate'] > 0.5:
            print("  ⚠️ 命中率一般（50-60%），系统有改进空间")
        else:
            print("  ❌ 命中率较低（<50%），需要检查选股逻辑")
        
        if summary['consistency'] > 0.7:
            print("  ✅ 跨周期表现稳定（>70%），系统可靠性高")
        elif summary['consistency'] > 0.5:
            print("  ⚠️ 跨周期表现波动（50-70%），需要关注市场环境")
        else:
            print("  ❌ 跨周期表现不稳定（<50%），可能存在过拟合")
    
    def get_detailed_df(self) -> pd.DataFrame:
        """获取详细结果DataFrame"""
        records = []
        for r in self.results:
            for s in r['stocks']:
                records.append({
                    "推荐日期": r['date'],
                    "股票代码": s['code'],
                    "股票名称": s['name'],
                    "5日收益%": s['ret_5d'],
                    "10日收益%": s['ret_10d'],
                    "20日收益%": s['ret_20d'],
                    "最大收益%": s['ret_max'],
                    "最大回撤%": s['ret_min'],
                    "超额5日%": s['alpha_5d'],
                    "超额10日%": s['alpha_10d'],
                    "超额20日%": s['alpha_20d'],
                })
        return pd.DataFrame(records)
    
    def save_report(self, output_dir: str = "results"):
        """保存报告"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 保存CSV
        df = self.get_detailed_df()
        csv_path = f"{output_dir}/rolling_validation_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"\n详细结果已保存: {csv_path}")
        
        return csv_path


def main():
    parser = argparse.ArgumentParser(description="运行投资推荐系统滚动验证")
    parser.add_argument("--months", type=int, default=12, help="验证历史月数")
    parser.add_argument("--train", type=int, default=3, help="训练期月数")
    parser.add_argument("--test", type=int, default=1, help="测试期月数")
    parser.add_argument("--top_n", type=int, default=10, help="每期推荐数量")
    args = parser.parse_args()
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=args.months * 30)).strftime("%Y-%m-%d")
    
    validator = SimpleRollingValidator(
        train_months=args.train,
        test_months=args.test,
        top_n=args.top_n,
    )
    
    summary = validator.run(start_date, end_date)
    
    # 保存结果
    validator.save_report()


if __name__ == "__main__":
    main()
