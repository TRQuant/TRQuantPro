#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
滚动验证框架 - 投资推荐系统可靠性验证

核心功能：
1. 训练集/测试集分离的滚动验证（Walk-forward Validation）
2. 推荐标的的实际收益追踪
3. 直观的量化指标（收益率、夏普比率、最大回撤、胜率等）
4. 避免过拟合的验证机制

设计原则：
- 结果可解释：每个推荐都有实际的回报数据
- 指标直观：使用标准的量化指标
- 过程透明：展示训练期和测试期的分离
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


@dataclass
class RecommendationResult:
    """单只股票推荐结果"""
    stock_code: str
    stock_name: str
    recommend_date: str  # 推荐日期
    recommend_price: float  # 推荐价格
    recommend_reason: str  # 推荐理由
    
    # 验证期收益
    return_5d: float = 0.0  # 5日收益
    return_10d: float = 0.0  # 10日收益
    return_20d: float = 0.0  # 20日收益
    return_max: float = 0.0  # 期间最大收益
    return_min: float = 0.0  # 期间最大回撤
    
    # 对比基准
    benchmark_5d: float = 0.0  # 基准5日收益
    benchmark_10d: float = 0.0  # 基准10日收益
    benchmark_20d: float = 0.0  # 基准20日收益
    
    # 超额收益
    alpha_5d: float = 0.0
    alpha_10d: float = 0.0
    alpha_20d: float = 0.0


@dataclass
class RollingPeriodResult:
    """单个滚动周期的结果"""
    train_start: str
    train_end: str
    test_start: str
    test_end: str
    
    recommendations: List[RecommendationResult] = field(default_factory=list)
    
    # 汇总指标
    avg_return_5d: float = 0.0
    avg_return_10d: float = 0.0
    avg_return_20d: float = 0.0
    win_rate_5d: float = 0.0  # 5日盈利比例
    win_rate_10d: float = 0.0
    win_rate_20d: float = 0.0
    avg_alpha_5d: float = 0.0  # 超额收益
    avg_alpha_10d: float = 0.0
    avg_alpha_20d: float = 0.0


@dataclass 
class ValidationSummary:
    """验证汇总结果"""
    total_periods: int = 0
    total_recommendations: int = 0
    
    # 平均收益率
    avg_return_5d: float = 0.0
    avg_return_10d: float = 0.0
    avg_return_20d: float = 0.0
    
    # 胜率
    win_rate_5d: float = 0.0
    win_rate_10d: float = 0.0
    win_rate_20d: float = 0.0
    
    # 超额收益（相对基准）
    avg_alpha_5d: float = 0.0
    avg_alpha_10d: float = 0.0
    avg_alpha_20d: float = 0.0
    
    # 风险指标
    sharpe_ratio: float = 0.0  # 夏普比率
    max_drawdown: float = 0.0  # 最大回撤
    volatility: float = 0.0  # 收益波动率
    
    # 一致性指标
    hit_rate: float = 0.0  # 推荐命中率（超过基准的比例）
    consistency: float = 0.0  # 跨周期一致性


class RollingValidator:
    """
    滚动验证器
    
    使用Walk-forward方法验证投资推荐系统：
    1. 将历史数据分为多个滚动窗口
    2. 每个窗口分为训练期和测试期
    3. 在训练期运行推荐系统
    4. 在测试期验证推荐效果
    """
    
    def __init__(
        self,
        train_months: int = 6,  # 训练期月数
        test_months: int = 1,   # 测试期月数
        step_months: int = 1,   # 滚动步长
        benchmark: str = "000300.XSHG",  # 基准指数
        top_n: int = 10,  # 每期推荐数量
    ):
        self.train_months = train_months
        self.test_months = test_months
        self.step_months = step_months
        self.benchmark = benchmark
        self.top_n = top_n
        
        self.jq = None
        self._init_jqdata()
        
        self.period_results: List[RollingPeriodResult] = []
    
    def _init_jqdata(self):
        """初始化JQData"""
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
    
    def generate_rolling_periods(
        self, 
        start_date: str, 
        end_date: str
    ) -> List[Dict[str, str]]:
        """生成滚动验证周期"""
        periods = []
        
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        current = start_dt
        
        while True:
            train_start = current
            train_end = train_start + timedelta(days=self.train_months * 30)
            test_start = train_end + timedelta(days=1)
            test_end = test_start + timedelta(days=self.test_months * 30)
            
            if test_end > end_dt:
                break
            
            periods.append({
                "train_start": train_start.strftime("%Y-%m-%d"),
                "train_end": train_end.strftime("%Y-%m-%d"),
                "test_start": test_start.strftime("%Y-%m-%d"),
                "test_end": test_end.strftime("%Y-%m-%d"),
            })
            
            current = current + timedelta(days=self.step_months * 30)
        
        return periods
    
    def get_recommendations(self, as_of_date: str) -> List[Dict]:
        """
        获取指定日期的投资推荐
        
        这里调用V3投资推荐系统
        """
        try:
            from core.advisor_v3.workflow_v3 import InvestmentAdvisorV3
            
            advisor = InvestmentAdvisorV3()
            result = advisor.run(target_date=as_of_date, save_to_db=False, generate_report=False)
            
            recommendations = []
            if result and "final_recommendations" in result:
                for stock in result["final_recommendations"][:self.top_n]:
                    recommendations.append({
                        "stock_code": stock.get("code", ""),
                        "stock_name": stock.get("name", ""),
                        "score": stock.get("total_score", 0),
                        "reason": stock.get("recommendation_reason", "综合评分推荐"),
                    })
            
            return recommendations
            
        except Exception as e:
            logger.warning(f"获取推荐失败 {as_of_date}: {e}")
            return []
    
    def get_stock_returns(
        self, 
        stock_code: str, 
        start_date: str, 
        hold_days: int = 20
    ) -> Dict[str, float]:
        """
        获取股票持有期收益
        
        返回：5日、10日、20日收益，最大收益，最大回撤
        """
        if not self.jq:
            return {}
        
        try:
            end_dt = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=hold_days + 10)
            
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
            
            base_price = df.iloc[0]['close']
            
            returns = {}
            
            # 5日收益
            if len(df) > 5:
                returns['return_5d'] = (df.iloc[5]['close'] / base_price - 1) * 100
            else:
                returns['return_5d'] = 0
            
            # 10日收益
            if len(df) > 10:
                returns['return_10d'] = (df.iloc[10]['close'] / base_price - 1) * 100
            else:
                returns['return_10d'] = returns.get('return_5d', 0)
            
            # 20日收益
            if len(df) > 20:
                returns['return_20d'] = (df.iloc[20]['close'] / base_price - 1) * 100
            else:
                returns['return_20d'] = (df.iloc[-1]['close'] / base_price - 1) * 100
            
            # 期间最大收益和最大回撤
            df['cum_return'] = (df['close'] / base_price - 1) * 100
            returns['return_max'] = df['cum_return'].max()
            returns['return_min'] = df['cum_return'].min()
            
            return returns
            
        except Exception as e:
            logger.warning(f"获取收益失败 {stock_code}: {e}")
            return {}
    
    def get_benchmark_returns(self, start_date: str, hold_days: int = 20) -> Dict[str, float]:
        """获取基准指数收益"""
        return self.get_stock_returns(self.benchmark, start_date, hold_days)
    
    def validate_period(self, period: Dict[str, str]) -> RollingPeriodResult:
        """验证单个滚动周期"""
        result = RollingPeriodResult(
            train_start=period["train_start"],
            train_end=period["train_end"],
            test_start=period["test_start"],
            test_end=period["test_end"],
        )
        
        # 在测试期开始日获取推荐
        recommendations = self.get_recommendations(period["test_start"])
        
        if not recommendations:
            logger.warning(f"周期 {period['test_start']} 无推荐")
            return result
        
        # 获取基准收益
        benchmark_returns = self.get_benchmark_returns(period["test_start"])
        
        # 验证每只推荐股票
        for rec in recommendations:
            stock_returns = self.get_stock_returns(rec["stock_code"], period["test_start"])
            
            if not stock_returns:
                continue
            
            # 获取推荐价格
            try:
                price_df = self.jq.get_price(
                    rec["stock_code"],
                    start_date=period["test_start"],
                    end_date=period["test_start"],
                    frequency='daily',
                    fields=['close']
                )
                recommend_price = price_df.iloc[0]['close'] if price_df is not None and len(price_df) > 0 else 0
            except:
                recommend_price = 0
            
            rec_result = RecommendationResult(
                stock_code=rec["stock_code"],
                stock_name=rec["stock_name"],
                recommend_date=period["test_start"],
                recommend_price=recommend_price,
                recommend_reason=rec.get("reason", ""),
                return_5d=stock_returns.get("return_5d", 0),
                return_10d=stock_returns.get("return_10d", 0),
                return_20d=stock_returns.get("return_20d", 0),
                return_max=stock_returns.get("return_max", 0),
                return_min=stock_returns.get("return_min", 0),
                benchmark_5d=benchmark_returns.get("return_5d", 0),
                benchmark_10d=benchmark_returns.get("return_10d", 0),
                benchmark_20d=benchmark_returns.get("return_20d", 0),
            )
            
            # 计算超额收益
            rec_result.alpha_5d = rec_result.return_5d - rec_result.benchmark_5d
            rec_result.alpha_10d = rec_result.return_10d - rec_result.benchmark_10d
            rec_result.alpha_20d = rec_result.return_20d - rec_result.benchmark_20d
            
            result.recommendations.append(rec_result)
        
        # 计算汇总指标
        if result.recommendations:
            returns_5d = [r.return_5d for r in result.recommendations]
            returns_10d = [r.return_10d for r in result.recommendations]
            returns_20d = [r.return_20d for r in result.recommendations]
            
            result.avg_return_5d = np.mean(returns_5d)
            result.avg_return_10d = np.mean(returns_10d)
            result.avg_return_20d = np.mean(returns_20d)
            
            result.win_rate_5d = sum(1 for r in returns_5d if r > 0) / len(returns_5d)
            result.win_rate_10d = sum(1 for r in returns_10d if r > 0) / len(returns_10d)
            result.win_rate_20d = sum(1 for r in returns_20d if r > 0) / len(returns_20d)
            
            alphas_5d = [r.alpha_5d for r in result.recommendations]
            alphas_10d = [r.alpha_10d for r in result.recommendations]
            alphas_20d = [r.alpha_20d for r in result.recommendations]
            
            result.avg_alpha_5d = np.mean(alphas_5d)
            result.avg_alpha_10d = np.mean(alphas_10d)
            result.avg_alpha_20d = np.mean(alphas_20d)
        
        return result
    
    def run_validation(
        self, 
        start_date: str, 
        end_date: str,
        verbose: bool = True
    ) -> ValidationSummary:
        """
        运行完整的滚动验证
        
        Args:
            start_date: 验证开始日期
            end_date: 验证结束日期
            verbose: 是否打印详细信息
        
        Returns:
            ValidationSummary: 验证汇总结果
        """
        if verbose:
            print("=" * 70)
            print("投资推荐系统 - 滚动验证（Walk-forward Validation）")
            print("=" * 70)
            print(f"\n验证参数:")
            print(f"  - 训练期: {self.train_months} 个月")
            print(f"  - 测试期: {self.test_months} 个月")
            print(f"  - 滚动步长: {self.step_months} 个月")
            print(f"  - 基准指数: {self.benchmark}")
            print(f"  - 每期推荐数: {self.top_n}")
            print(f"  - 验证区间: {start_date} ~ {end_date}")
        
        # 生成滚动周期
        periods = self.generate_rolling_periods(start_date, end_date)
        
        if verbose:
            print(f"\n生成 {len(periods)} 个滚动验证周期")
        
        # 逐周期验证
        self.period_results = []
        
        for i, period in enumerate(periods):
            if verbose:
                print(f"\n[{i+1}/{len(periods)}] 验证周期: "
                      f"训练 {period['train_start']}~{period['train_end']} | "
                      f"测试 {period['test_start']}~{period['test_end']}")
            
            result = self.validate_period(period)
            self.period_results.append(result)
            
            if verbose and result.recommendations:
                print(f"  推荐 {len(result.recommendations)} 只股票")
                print(f"  5日收益: {result.avg_return_5d:.2f}% | 胜率: {result.win_rate_5d:.1%}")
                print(f"  10日收益: {result.avg_return_10d:.2f}% | 胜率: {result.win_rate_10d:.1%}")
                print(f"  20日收益: {result.avg_return_20d:.2f}% | 胜率: {result.win_rate_20d:.1%}")
                print(f"  超额收益(20日): {result.avg_alpha_20d:.2f}%")
        
        # 汇总统计
        summary = self._calculate_summary()
        
        if verbose:
            self._print_summary(summary)
        
        return summary
    
    def _calculate_summary(self) -> ValidationSummary:
        """计算汇总统计"""
        summary = ValidationSummary()
        
        if not self.period_results:
            return summary
        
        # 收集所有推荐
        all_recommendations = []
        for pr in self.period_results:
            all_recommendations.extend(pr.recommendations)
        
        summary.total_periods = len(self.period_results)
        summary.total_recommendations = len(all_recommendations)
        
        if not all_recommendations:
            return summary
        
        # 平均收益率
        returns_5d = [r.return_5d for r in all_recommendations]
        returns_10d = [r.return_10d for r in all_recommendations]
        returns_20d = [r.return_20d for r in all_recommendations]
        
        summary.avg_return_5d = np.mean(returns_5d)
        summary.avg_return_10d = np.mean(returns_10d)
        summary.avg_return_20d = np.mean(returns_20d)
        
        # 胜率
        summary.win_rate_5d = sum(1 for r in returns_5d if r > 0) / len(returns_5d)
        summary.win_rate_10d = sum(1 for r in returns_10d if r > 0) / len(returns_10d)
        summary.win_rate_20d = sum(1 for r in returns_20d if r > 0) / len(returns_20d)
        
        # 超额收益
        alphas_5d = [r.alpha_5d for r in all_recommendations]
        alphas_10d = [r.alpha_10d for r in all_recommendations]
        alphas_20d = [r.alpha_20d for r in all_recommendations]
        
        summary.avg_alpha_5d = np.mean(alphas_5d)
        summary.avg_alpha_10d = np.mean(alphas_10d)
        summary.avg_alpha_20d = np.mean(alphas_20d)
        
        # 风险指标
        if len(returns_20d) > 1:
            summary.volatility = np.std(returns_20d)
            
            # 夏普比率（假设无风险利率3%年化，20日约0.25%）
            rf_rate = 0.25
            if summary.volatility > 0:
                summary.sharpe_ratio = (summary.avg_return_20d - rf_rate) / summary.volatility
            
            # 最大回撤
            cum_returns = np.cumsum(returns_20d)
            running_max = np.maximum.accumulate(cum_returns)
            drawdowns = cum_returns - running_max
            summary.max_drawdown = np.min(drawdowns)
        
        # 命中率（超过基准的比例）
        summary.hit_rate = sum(1 for r in all_recommendations if r.alpha_20d > 0) / len(all_recommendations)
        
        # 跨周期一致性（每期都有正收益的比例）
        positive_periods = sum(1 for pr in self.period_results 
                              if pr.recommendations and pr.avg_return_20d > 0)
        summary.consistency = positive_periods / len(self.period_results) if self.period_results else 0
        
        return summary
    
    def _print_summary(self, summary: ValidationSummary):
        """打印汇总结果"""
        print("\n" + "=" * 70)
        print("验证汇总结果")
        print("=" * 70)
        
        print(f"\n📊 基本统计:")
        print(f"  - 验证周期数: {summary.total_periods}")
        print(f"  - 总推荐数量: {summary.total_recommendations}")
        
        print(f"\n📈 收益率指标:")
        print(f"  {'指标':<15} {'5日':<12} {'10日':<12} {'20日':<12}")
        print(f"  {'-'*50}")
        print(f"  {'平均收益':<15} {summary.avg_return_5d:>8.2f}%    {summary.avg_return_10d:>8.2f}%    {summary.avg_return_20d:>8.2f}%")
        print(f"  {'胜率':<15} {summary.win_rate_5d:>8.1%}    {summary.win_rate_10d:>8.1%}    {summary.win_rate_20d:>8.1%}")
        print(f"  {'超额收益':<15} {summary.avg_alpha_5d:>8.2f}%    {summary.avg_alpha_10d:>8.2f}%    {summary.avg_alpha_20d:>8.2f}%")
        
        print(f"\n📉 风险指标:")
        print(f"  - 夏普比率: {summary.sharpe_ratio:.3f}")
        print(f"  - 最大回撤: {summary.max_drawdown:.2f}%")
        print(f"  - 收益波动率: {summary.volatility:.2f}%")
        
        print(f"\n✅ 可靠性指标:")
        print(f"  - 命中率（超额收益>0）: {summary.hit_rate:.1%}")
        print(f"  - 跨周期一致性: {summary.consistency:.1%}")
        
        # 评价
        print(f"\n📝 综合评价:")
        if summary.sharpe_ratio > 1.5:
            print("  ✅ 夏普比率优秀（>1.5），风险调整后收益很好")
        elif summary.sharpe_ratio > 1.0:
            print("  ✅ 夏普比率良好（>1.0），具有投资价值")
        elif summary.sharpe_ratio > 0.5:
            print("  ⚠️ 夏普比率一般（0.5-1.0），需要优化")
        else:
            print("  ❌ 夏普比率较低（<0.5），不建议使用")
        
        if summary.hit_rate > 0.6:
            print("  ✅ 命中率较高，系统选股能力强")
        elif summary.hit_rate > 0.5:
            print("  ⚠️ 命中率一般，系统有改进空间")
        else:
            print("  ❌ 命中率较低，需要检查选股逻辑")
        
        if summary.consistency > 0.7:
            print("  ✅ 跨周期表现稳定，系统可靠性高")
        elif summary.consistency > 0.5:
            print("  ⚠️ 跨周期表现波动，需要关注市场环境")
        else:
            print("  ❌ 跨周期表现不稳定，可能存在过拟合")
    
    def get_detailed_results(self) -> pd.DataFrame:
        """获取详细的推荐结果DataFrame"""
        records = []
        
        for pr in self.period_results:
            for rec in pr.recommendations:
                records.append({
                    "推荐日期": rec.recommend_date,
                    "股票代码": rec.stock_code,
                    "股票名称": rec.stock_name,
                    "推荐价格": rec.recommend_price,
                    "5日收益%": rec.return_5d,
                    "10日收益%": rec.return_10d,
                    "20日收益%": rec.return_20d,
                    "最大收益%": rec.return_max,
                    "最大回撤%": rec.return_min,
                    "基准5日%": rec.benchmark_5d,
                    "基准10日%": rec.benchmark_10d,
                    "基准20日%": rec.benchmark_20d,
                    "超额5日%": rec.alpha_5d,
                    "超额10日%": rec.alpha_10d,
                    "超额20日%": rec.alpha_20d,
                    "推荐理由": rec.recommend_reason,
                })
        
        return pd.DataFrame(records)
    
    def generate_html_report(self, output_path: str) -> str:
        """生成HTML验证报告"""
        summary = self._calculate_summary()
        details_df = self.get_detailed_results()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>投资推荐系统 - 滚动验证报告</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            padding: 30px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: #00d4ff;
            font-size: 28px;
            margin-bottom: 30px;
        }}
        .section {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
        }}
        .section h2 {{
            color: #00d4ff;
            margin-top: 0;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 10px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: rgba(0,212,255,0.1);
            border: 1px solid rgba(0,212,255,0.3);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            color: #00d4ff;
        }}
        .metric-label {{
            font-size: 14px;
            color: #999;
            margin-top: 5px;
        }}
        .positive {{ color: #00ff88; }}
        .negative {{ color: #ff4466; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        th {{
            background: rgba(0,212,255,0.2);
            color: #00d4ff;
        }}
        tr:hover {{
            background: rgba(255,255,255,0.05);
        }}
        .evaluation {{
            background: rgba(0,255,136,0.1);
            border-left: 4px solid #00ff88;
            padding: 15px 20px;
            margin: 20px 0;
        }}
        .warning {{
            background: rgba(255,170,0,0.1);
            border-left: 4px solid #ffaa00;
        }}
        .danger {{
            background: rgba(255,68,102,0.1);
            border-left: 4px solid #ff4466;
        }}
        .report-time {{
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 投资推荐系统 - 滚动验证报告</h1>
        
        <div class="section">
            <h2>验证参数</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">{summary.total_periods}</div>
                    <div class="metric-label">验证周期数</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary.total_recommendations}</div>
                    <div class="metric-label">总推荐数量</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{self.train_months}月</div>
                    <div class="metric-label">训练期长度</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{self.test_months}月</div>
                    <div class="metric-label">测试期长度</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>核心收益指标</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value {'positive' if summary.avg_return_20d > 0 else 'negative'}">{summary.avg_return_20d:.2f}%</div>
                    <div class="metric-label">20日平均收益</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary.win_rate_20d:.1%}</div>
                    <div class="metric-label">20日胜率</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value {'positive' if summary.avg_alpha_20d > 0 else 'negative'}">{summary.avg_alpha_20d:.2f}%</div>
                    <div class="metric-label">20日超额收益</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary.hit_rate:.1%}</div>
                    <div class="metric-label">命中率</div>
                </div>
            </div>
            
            <table>
                <tr>
                    <th>指标</th>
                    <th>5日</th>
                    <th>10日</th>
                    <th>20日</th>
                </tr>
                <tr>
                    <td>平均收益</td>
                    <td class="{'positive' if summary.avg_return_5d > 0 else 'negative'}">{summary.avg_return_5d:.2f}%</td>
                    <td class="{'positive' if summary.avg_return_10d > 0 else 'negative'}">{summary.avg_return_10d:.2f}%</td>
                    <td class="{'positive' if summary.avg_return_20d > 0 else 'negative'}">{summary.avg_return_20d:.2f}%</td>
                </tr>
                <tr>
                    <td>胜率</td>
                    <td>{summary.win_rate_5d:.1%}</td>
                    <td>{summary.win_rate_10d:.1%}</td>
                    <td>{summary.win_rate_20d:.1%}</td>
                </tr>
                <tr>
                    <td>超额收益</td>
                    <td class="{'positive' if summary.avg_alpha_5d > 0 else 'negative'}">{summary.avg_alpha_5d:.2f}%</td>
                    <td class="{'positive' if summary.avg_alpha_10d > 0 else 'negative'}">{summary.avg_alpha_10d:.2f}%</td>
                    <td class="{'positive' if summary.avg_alpha_20d > 0 else 'negative'}">{summary.avg_alpha_20d:.2f}%</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>风险指标</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">{summary.sharpe_ratio:.3f}</div>
                    <div class="metric-label">夏普比率</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value negative">{summary.max_drawdown:.2f}%</div>
                    <div class="metric-label">最大回撤</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary.volatility:.2f}%</div>
                    <div class="metric-label">收益波动率</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{summary.consistency:.1%}</div>
                    <div class="metric-label">跨周期一致性</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>综合评价</h2>
            {'<div class="evaluation">✅ 夏普比率优秀（>1.5），风险调整后收益很好</div>' if summary.sharpe_ratio > 1.5 else
             '<div class="evaluation">✅ 夏普比率良好（>1.0），具有投资价值</div>' if summary.sharpe_ratio > 1.0 else
             '<div class="evaluation warning">⚠️ 夏普比率一般（0.5-1.0），需要优化</div>' if summary.sharpe_ratio > 0.5 else
             '<div class="evaluation danger">❌ 夏普比率较低（<0.5），不建议使用</div>'}
            
            {'<div class="evaluation">✅ 命中率较高（>60%），系统选股能力强</div>' if summary.hit_rate > 0.6 else
             '<div class="evaluation warning">⚠️ 命中率一般（50-60%），系统有改进空间</div>' if summary.hit_rate > 0.5 else
             '<div class="evaluation danger">❌ 命中率较低（<50%），需要检查选股逻辑</div>'}
            
            {'<div class="evaluation">✅ 跨周期表现稳定（>70%），系统可靠性高</div>' if summary.consistency > 0.7 else
             '<div class="evaluation warning">⚠️ 跨周期表现波动（50-70%），需要关注市场环境</div>' if summary.consistency > 0.5 else
             '<div class="evaluation danger">❌ 跨周期表现不稳定（<50%），可能存在过拟合</div>'}
        </div>
        
        <div class="section">
            <h2>推荐明细（Top 20）</h2>
            <table>
                <tr>
                    <th>日期</th>
                    <th>代码</th>
                    <th>名称</th>
                    <th>推荐价</th>
                    <th>5日%</th>
                    <th>10日%</th>
                    <th>20日%</th>
                    <th>超额%</th>
                </tr>
"""
        
        # 添加明细行（最多20条）
        for _, row in details_df.head(20).iterrows():
            ret_5d_class = 'positive' if row['5日收益%'] > 0 else 'negative'
            ret_10d_class = 'positive' if row['10日收益%'] > 0 else 'negative'
            ret_20d_class = 'positive' if row['20日收益%'] > 0 else 'negative'
            alpha_class = 'positive' if row['超额20日%'] > 0 else 'negative'
            
            html += f"""
                <tr>
                    <td>{row['推荐日期']}</td>
                    <td>{row['股票代码']}</td>
                    <td>{row['股票名称']}</td>
                    <td>{row['推荐价格']:.2f}</td>
                    <td class="{ret_5d_class}">{row['5日收益%']:.2f}</td>
                    <td class="{ret_10d_class}">{row['10日收益%']:.2f}</td>
                    <td class="{ret_20d_class}">{row['20日收益%']:.2f}</td>
                    <td class="{alpha_class}">{row['超额20日%']:.2f}</td>
                </tr>
"""
        
        html += f"""
            </table>
        </div>
        
        <div class="report-time">
            报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path


# 快速验证函数
def quick_validate(months: int = 6, verbose: bool = True) -> ValidationSummary:
    """
    快速滚动验证
    
    Args:
        months: 验证历史月数
        verbose: 是否打印详情
    
    Returns:
        ValidationSummary
    """
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=months * 30)).strftime("%Y-%m-%d")
    
    validator = RollingValidator(
        train_months=3,  # 3个月训练
        test_months=1,   # 1个月测试
        step_months=1,   # 1个月滚动
        top_n=10,
    )
    
    return validator.run_validation(start_date, end_date, verbose=verbose)


if __name__ == "__main__":
    # 运行快速验证
    summary = quick_validate(months=12, verbose=True)
