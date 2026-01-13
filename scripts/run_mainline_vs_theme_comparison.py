#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
动态主线选股 vs 固定主题选股 回测对比脚本

功能:
1. 在相同的牛市时段进行回测
2. 对比动态主线选股和固定主题选股的表现
3. 生成详细的对比报告

回测时段:
- 2024政策牛 (2024-09-20 ~ 2024-10-15)
- 2024年末行情 (2024-11-15 ~ 2024-12-15)
- 2020夏季牛市 (2020-06-15 ~ 2020-07-31)

目标: 验证动态主线选股是否优于固定主题选股

作者: TRQuant Team
版本: V1.0
日期: 2026-01-12
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field

import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'/home/taotao/.cursor/worktrees/TRQuant/ope/output/comparison_backtest_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

# 导入策略模块
from core.strategy.bull_market_strategy_v6 import BullMarketStrategyV6, StrategyDecision
from core.research.vbt_backtest_v5 import VBTBacktestV5
from core.research.data_provider import ResearchDataProvider
from core.research.factors import FactorCalculator


@dataclass
class BacktestResult:
    """回测结果"""
    period_name: str
    selection_mode: str  # dynamic_mainline / fixed_theme
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    weekly_return: float = 0.0
    buy_targets_count: int = 0
    top_mainlines: List[str] = field(default_factory=list)
    reasoning: str = ""


@dataclass
class ComparisonReport:
    """对比报告"""
    mainline_results: List[BacktestResult] = field(default_factory=list)
    theme_results: List[BacktestResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""


def run_backtest_for_mode(
    strategy: BullMarketStrategyV6,
    backtest_engine: VBTBacktestV5,
    data_provider: ResearchDataProvider,
    factor_calculator: FactorCalculator,
    period_name: str,
    start_date: str,
    end_date: str,
    use_mainline: bool,
    ai_theme_stocks: List[str],
) -> BacktestResult:
    """
    为特定模式运行回测
    
    Args:
        strategy: 策略引擎
        backtest_engine: 回测引擎
        data_provider: 数据提供器
        factor_calculator: 因子计算器
        period_name: 时段名称
        start_date: 开始日期
        end_date: 结束日期
        use_mainline: 是否使用主线模式
        ai_theme_stocks: AI主题股票列表 (固定主题模式使用)
    
    Returns:
        BacktestResult: 回测结果
    """
    mode_name = "dynamic_mainline" if use_mainline else "fixed_theme"
    logger.info(f"\n{'='*60}")
    logger.info(f"回测: {period_name} - {'动态主线' if use_mainline else '固定主题'}模式")
    logger.info(f"{'='*60}")
    logger.info(f"时段: {start_date} ~ {end_date}")
    
    result = BacktestResult(
        period_name=period_name,
        selection_mode=mode_name,
    )
    
    try:
        # 1. 做出策略决策
        candidate_stocks = ai_theme_stocks if not use_mainline else []
        
        decision = strategy.make_decision(
            as_of_date=start_date,
            candidate_stocks=candidate_stocks,
            use_mainline=use_mainline,
        )
        
        result.buy_targets_count = len(decision.buy_targets)
        result.top_mainlines = [ml.get("name", "") for ml in decision.top_mainlines[:3]]
        result.reasoning = decision.reasoning
        
        if not decision.allow_trade:
            logger.warning(f"策略决策: 不允许交易 - {decision.reasoning}")
            return result
        
        # 2. 获取选中股票
        selected_stocks = [t["stock"] for t in decision.buy_targets]
        
        if not selected_stocks:
            logger.warning("没有选中任何股票")
            return result
        
        logger.info(f"选中 {len(selected_stocks)} 只股票: {selected_stocks[:5]}")
        
        # 3. 获取行情数据
        price_data = data_provider.get_data_matrices(
            symbols=selected_stocks,
            start_date=start_date,
            end_date=end_date,
            frequency="daily",
        )
        
        if price_data is None or price_data.close.empty:
            logger.warning("无法获取价格数据")
            return result
        
        # 4. 计算因子
        factors = factor_calculator.calculate_factors(
            data=price_data,
            factor_list=["mom_20d", "mom_5d", "vol_ratio", "is_limit_up"],
        )
        
        # 5. 简化回测: 计算等权重组合收益
        close = price_data.close
        trading_days = close.index
        num_stocks = len(selected_stocks)
        
        if num_stocks == 0 or len(trading_days) < 2:
            logger.warning("股票数量或交易日数量不足")
            return result
        
        # 计算日收益率
        daily_returns = close.pct_change().fillna(0)
        
        # 等权重组合收益率
        portfolio_returns = daily_returns.mean(axis=1)
        
        # 扣除交易成本 (首日买入成本)
        commission = 0.0003  # 万分之三
        stamp_duty = 0.001   # 千分之一 (卖出时)
        
        # 累计收益
        cumulative_returns = (1 + portfolio_returns).cumprod()
        
        # 总收益率
        total_return = (cumulative_returns.iloc[-1] - 1) * 100
        
        # 扣除交易成本后的收益
        total_return_net = total_return - (commission * 2 + stamp_duty) * 100  # 买卖各一次
        
        # 年化收益
        trading_days_count = len(trading_days)
        years = trading_days_count / 252
        if years > 0:
            annual_return = ((1 + total_return_net / 100) ** (1 / years) - 1) * 100
        else:
            annual_return = 0.0
        
        # 夏普比率
        if portfolio_returns.std() > 0:
            sharpe_ratio = (portfolio_returns.mean() * 252) / (portfolio_returns.std() * np.sqrt(252))
        else:
            sharpe_ratio = 0.0
        
        # 最大回撤
        peak = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = abs(drawdown.min()) * 100
        
        # 周收益率
        weekly_return = 0.0
        if trading_days_count > 0:
            weekly_return = ((1 + total_return_net / 100) ** (5 / trading_days_count) - 1) * 100
        
        # 6. 填充结果
        result.total_return = total_return_net
        result.annual_return = annual_return
        result.sharpe_ratio = sharpe_ratio
        result.max_drawdown = max_drawdown
        result.win_rate = (portfolio_returns > 0).mean() * 100
        result.total_trades = num_stocks
        result.weekly_return = weekly_return
        
        logger.info(f"回测完成: 总收益={result.total_return:.2f}%, 周收益={result.weekly_return:.2f}%, 夏普={result.sharpe_ratio:.2f}")
        
    except Exception as e:
        logger.error(f"回测失败: {e}")
        import traceback
        traceback.print_exc()
    
    return result


def run_comparison():
    """运行对比回测"""
    logger.info("="*60)
    logger.info("动态主线选股 vs 固定主题选股 对比回测")
    logger.info("="*60)
    
    # 定义回测时段
    test_periods = {
        "2024_policy_bull": {
            "start_date": "2024-09-20",
            "end_date": "2024-10-15",
            "description": "2024政策牛（924大涨）",
        },
        "2024_year_end": {
            "start_date": "2024-11-15",
            "end_date": "2024-12-15",
            "description": "2024年末行情",
        },
        "2020_summer_bull": {
            "start_date": "2020-06-15",
            "end_date": "2020-07-31",
            "description": "2020夏季牛市",
        },
    }
    
    # 固定AI主题股票池
    ai_theme_stocks = [
        "002230.XSHE",  # 科大讯飞
        "688111.XSHG",  # 金山办公
        "300369.XSHE",  # 绿盟科技
        "300033.XSHE",  # 同花顺
        "300212.XSHE",  # 易华录
        "002280.XSHE",  # 联络互动
        "300052.XSHE",  # 中青宝
        "300229.XSHE",  # 拓尔思
        "300418.XSHE",  # 昆仑万维
        "300674.XSHE",  # 宇信科技
        "002415.XSHE",  # 海康威视
        "002410.XSHE",  # 广联达
        "300496.XSHE",  # 中科创达
        "300468.XSHE",  # 四方精创
        "002405.XSHE",  # 四维图新
    ]
    
    # 初始化组件
    logger.info("\n初始化策略组件...")
    
    # 动态主线模式策略
    strategy_mainline = BullMarketStrategyV6(use_dynamic_mainline=True)
    
    # 固定主题模式策略
    strategy_theme = BullMarketStrategyV6(use_dynamic_mainline=False)
    
    backtest_engine = VBTBacktestV5()
    data_provider = ResearchDataProvider()
    factor_calculator = FactorCalculator(use_gpu=False)
    
    # 存储结果
    mainline_results = []
    theme_results = []
    
    # 对每个时段进行回测
    for period_name, period_config in test_periods.items():
        logger.info(f"\n\n{'#'*60}")
        logger.info(f"时段: {period_name} - {period_config['description']}")
        logger.info(f"{'#'*60}")
        
        # 动态主线模式回测
        mainline_result = run_backtest_for_mode(
            strategy=strategy_mainline,
            backtest_engine=backtest_engine,
            data_provider=data_provider,
            factor_calculator=factor_calculator,
            period_name=period_name,
            start_date=period_config["start_date"],
            end_date=period_config["end_date"],
            use_mainline=True,
            ai_theme_stocks=[],
        )
        mainline_results.append(mainline_result)
        
        # 固定主题模式回测
        theme_result = run_backtest_for_mode(
            strategy=strategy_theme,
            backtest_engine=backtest_engine,
            data_provider=data_provider,
            factor_calculator=factor_calculator,
            period_name=period_name,
            start_date=period_config["start_date"],
            end_date=period_config["end_date"],
            use_mainline=False,
            ai_theme_stocks=ai_theme_stocks,
        )
        theme_results.append(theme_result)
    
    # 生成对比报告
    report = generate_comparison_report(mainline_results, theme_results, test_periods)
    
    # 保存报告
    save_report(report)
    
    return report


def generate_comparison_report(
    mainline_results: List[BacktestResult],
    theme_results: List[BacktestResult],
    test_periods: Dict,
) -> ComparisonReport:
    """生成对比报告"""
    report = ComparisonReport(
        mainline_results=mainline_results,
        theme_results=theme_results,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    
    # 计算汇总统计
    mainline_returns = [r.total_return for r in mainline_results if r.total_return != 0]
    theme_returns = [r.total_return for r in theme_results if r.total_return != 0]
    
    mainline_weekly = [r.weekly_return for r in mainline_results if r.weekly_return != 0]
    theme_weekly = [r.weekly_return for r in theme_results if r.weekly_return != 0]
    
    report.summary = {
        "periods_tested": len(test_periods),
        "mainline": {
            "avg_total_return": np.mean(mainline_returns) if mainline_returns else 0,
            "avg_weekly_return": np.mean(mainline_weekly) if mainline_weekly else 0,
            "max_return": max(mainline_returns) if mainline_returns else 0,
            "min_return": min(mainline_returns) if mainline_returns else 0,
            "win_periods": sum(1 for r in mainline_returns if r > 0),
        },
        "theme": {
            "avg_total_return": np.mean(theme_returns) if theme_returns else 0,
            "avg_weekly_return": np.mean(theme_weekly) if theme_weekly else 0,
            "max_return": max(theme_returns) if theme_returns else 0,
            "min_return": min(theme_returns) if theme_returns else 0,
            "win_periods": sum(1 for r in theme_returns if r > 0),
        },
    }
    
    # 计算胜率对比
    mainline_wins = 0
    for ml, th in zip(mainline_results, theme_results):
        if ml.total_return > th.total_return:
            mainline_wins += 1
    
    report.summary["mainline_vs_theme_wins"] = mainline_wins
    report.summary["mainline_advantage"] = (
        report.summary["mainline"]["avg_total_return"] - 
        report.summary["theme"]["avg_total_return"]
    )
    
    return report


def save_report(report: ComparisonReport):
    """保存对比报告"""
    output_dir = Path("/home/taotao/.cursor/worktrees/TRQuant/ope/output/comparison")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Markdown报告
    md_content = []
    md_content.append("# 动态主线选股 vs 固定主题选股 对比报告")
    md_content.append(f"\n生成时间: {report.timestamp}")
    
    md_content.append("\n## 1. 汇总统计")
    md_content.append("\n| 指标 | 动态主线 | 固定主题 | 差异 |")
    md_content.append("|------|---------|---------|------|")
    
    ml_avg = report.summary["mainline"]["avg_total_return"]
    th_avg = report.summary["theme"]["avg_total_return"]
    ml_weekly = report.summary["mainline"]["avg_weekly_return"]
    th_weekly = report.summary["theme"]["avg_weekly_return"]
    
    md_content.append(f"| 平均总收益率 | {ml_avg:.2f}% | {th_avg:.2f}% | {ml_avg-th_avg:+.2f}% |")
    md_content.append(f"| 平均周收益率 | {ml_weekly:.2f}% | {th_weekly:.2f}% | {ml_weekly-th_weekly:+.2f}% |")
    md_content.append(f"| 最高收益 | {report.summary['mainline']['max_return']:.2f}% | {report.summary['theme']['max_return']:.2f}% | - |")
    md_content.append(f"| 盈利时段数 | {report.summary['mainline']['win_periods']} | {report.summary['theme']['win_periods']} | - |")
    md_content.append(f"| 主线胜出次数 | {report.summary['mainline_vs_theme_wins']}/{report.summary['periods_tested']} | - | - |")
    
    md_content.append("\n## 2. 分时段对比")
    md_content.append("\n| 时段 | 主线收益 | 主题收益 | 主线周收益 | 主题周收益 | 胜出 |")
    md_content.append("|------|---------|---------|-----------|-----------|------|")
    
    for ml, th in zip(report.mainline_results, report.theme_results):
        winner = "主线" if ml.total_return > th.total_return else "主题"
        md_content.append(
            f"| {ml.period_name} | {ml.total_return:.2f}% | {th.total_return:.2f}% | "
            f"{ml.weekly_return:.2f}% | {th.weekly_return:.2f}% | {winner} |"
        )
    
    md_content.append("\n## 3. 动态主线详情")
    for result in report.mainline_results:
        md_content.append(f"\n### {result.period_name}")
        md_content.append(f"- **Top主线**: {', '.join(result.top_mainlines) if result.top_mainlines else '无'}")
        md_content.append(f"- **买入标的数**: {result.buy_targets_count}")
        md_content.append(f"- **总收益**: {result.total_return:.2f}%")
        md_content.append(f"- **周收益**: {result.weekly_return:.2f}%")
        md_content.append(f"- **夏普比率**: {result.sharpe_ratio:.2f}")
        md_content.append(f"- **最大回撤**: {result.max_drawdown:.2f}%")
        md_content.append(f"- **决策理由**: {result.reasoning}")
    
    md_content.append("\n## 4. 结论与建议")
    
    if report.summary["mainline_advantage"] > 0:
        md_content.append(f"\n**动态主线选股优于固定主题选股**")
        md_content.append(f"- 平均收益优势: +{report.summary['mainline_advantage']:.2f}%")
        md_content.append(f"- 胜出比例: {report.summary['mainline_vs_theme_wins']}/{report.summary['periods_tested']}")
        md_content.append("\n建议:")
        md_content.append("1. 继续使用动态主线选股模式")
        md_content.append("2. 可适当提高主线权重（当前70%）")
        md_content.append("3. 关注市场主线的持续性")
    else:
        md_content.append(f"\n**固定主题选股优于动态主线选股**")
        md_content.append(f"- 固定主题优势: +{-report.summary['mainline_advantage']:.2f}%")
        md_content.append("\n建议:")
        md_content.append("1. 检查主线识别的准确性")
        md_content.append("2. 考虑调整五维权重配置")
        md_content.append("3. 增加主线与主题的融合")
    
    # 保存Markdown
    md_path = output_dir / f"comparison_report_{timestamp}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    logger.info(f"报告已保存: {md_path}")
    
    # 保存JSON
    json_data = {
        "timestamp": report.timestamp,
        "summary": report.summary,
        "mainline_results": [
            {
                "period": r.period_name,
                "total_return": r.total_return,
                "weekly_return": r.weekly_return,
                "sharpe_ratio": r.sharpe_ratio,
                "max_drawdown": r.max_drawdown,
                "top_mainlines": r.top_mainlines,
            } for r in report.mainline_results
        ],
        "theme_results": [
            {
                "period": r.period_name,
                "total_return": r.total_return,
                "weekly_return": r.weekly_return,
                "sharpe_ratio": r.sharpe_ratio,
                "max_drawdown": r.max_drawdown,
            } for r in report.theme_results
        ],
    }
    
    json_path = output_dir / f"comparison_data_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    logger.info(f"数据已保存: {json_path}")
    
    # 打印报告
    print("\n" + "="*60)
    print("\n".join(md_content))
    print("="*60)


if __name__ == "__main__":
    run_comparison()
