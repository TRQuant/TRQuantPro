# -*- coding: utf-8 -*-
"""
牛市高回报策略 V4.0 - 全量回测脚本
==================================

多时段全A股回测，验证策略有效性

开发记录：
- 2026-01-12: 创建V4全量回测脚本
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
import json

# 设置项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / 'output/bull_market_v4/backtest.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_period_backtest(
    period_name: str,
    start_date: str,
    end_date: str,
    max_stocks: int = 1000,
) -> dict:
    """
    运行单时段回测
    
    Args:
        period_name: 时段名称
        start_date: 开始日期
        end_date: 结束日期
        max_stocks: 最大股票数
        
    Returns:
        回测结果字典
    """
    from core.research.data_provider import ResearchDataProvider
    from core.research.factors import FactorCalculator
    from core.research.signals import SignalEngine, SignalParams
    from core.research.vbt_backtest import VBTBacktest
    from core.strategy.bull_market_strategy_v4 import BullMarketStrategyV4
    
    logger.info(f"\n{'='*60}")
    logger.info(f"回测时段: {period_name} ({start_date} ~ {end_date})")
    logger.info(f"{'='*60}")
    
    try:
        # 1. 初始化策略
        strategy = BullMarketStrategyV4()
        
        # 2. 市场趋势分析
        market_context = strategy.analyze_market(start_date)
        logger.info(f"市场状态: {market_context.strategy_mode.value}, 得分: {market_context.ensemble_score:.1f}")
        
        # 3. 获取股票池
        provider = ResearchDataProvider(use_cache=True)
        all_stocks = provider.get_all_a_stocks(date=start_date, min_days_listed=60)
        
        # 限制股票数量
        test_stocks = all_stocks[:max_stocks]
        logger.info(f"股票池: {len(test_stocks)}只 (全A: {len(all_stocks)}只)")
        
        # 4. 获取数据
        data = provider.get_data_matrices(test_stocks, start_date, end_date)
        logger.info(f"数据: {data.shape[0]}天 x {data.shape[1]}只股票")
        
        # 5. 计算因子
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(data, factor_list=[
            'mom_20d', 'mom_5d', 'rel_position', 
            'vol_ratio', 'vol_ratio_5d',
            'is_limit_up', 'limit_up_count_5d', 'is_first_limit_up', 'limit_up_vol_ratio',
            'breakout_60d', 'breakout_ratio',
            'main_flow', 'flow_strength',
        ])
        
        # 6. 生成信号
        params = SignalParams()
        signal_engine = SignalEngine(params)
        signals = signal_engine.generate_signals(data, factors)
        
        # 7. 运行回测
        backtest = VBTBacktest()
        result = backtest.run_with_signals(data, signals)
        
        # 计算周收益
        trading_days = result.trading_days
        weekly_return = (1 + result.total_return) ** (5 / trading_days) - 1 if trading_days > 0 else 0
        
        logger.info(f"回测结果:")
        logger.info(f"  总收益: {result.total_return:.2%}")
        logger.info(f"  年化收益: {result.annual_return:.2%}")
        logger.info(f"  夏普比率: {result.sharpe_ratio:.2f}")
        logger.info(f"  最大回撤: {result.max_drawdown:.2%}")
        logger.info(f"  胜率: {result.win_rate:.1f}%")
        logger.info(f"  交易次数: {result.total_trades}")
        logger.info(f"  周收益(估算): {weekly_return:.2%}")
        
        return {
            "period": period_name,
            "start_date": start_date,
            "end_date": end_date,
            "market_score": market_context.ensemble_score,
            "market_mode": market_context.strategy_mode.value,
            "stocks_count": len(test_stocks),
            "trading_days": result.trading_days,
            "total_return": result.total_return,
            "annual_return": result.annual_return,
            "sharpe_ratio": result.sharpe_ratio,
            "max_drawdown": result.max_drawdown,
            "win_rate": result.win_rate,
            "total_trades": result.total_trades,
            "weekly_return": weekly_return,
            "success": True,
        }
        
    except Exception as e:
        logger.error(f"回测失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            "period": period_name,
            "start_date": start_date,
            "end_date": end_date,
            "success": False,
            "error": str(e),
        }


def main():
    """主函数"""
    
    # 创建输出目录
    output_dir = PROJECT_ROOT / "output/bull_market_v4"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("=" * 70)
    logger.info("牛市高回报策略 V4.0 - 全量回测")
    logger.info("=" * 70)
    
    # 定义多个牛市时段
    bull_periods = [
        # 2024年政策牛（最重要）
        {"name": "2024_policy_bull", "start": "2024-09-20", "end": "2024-10-15"},
        # 2024年底反弹
        {"name": "2024_year_end", "start": "2024-11-15", "end": "2024-12-15"},
        # 2020年夏季牛
        {"name": "2020_summer_bull", "start": "2020-06-15", "end": "2020-07-15"},
        # 2019年春季牛
        {"name": "2019_spring_bull", "start": "2019-02-01", "end": "2019-04-15"},
    ]
    
    results = []
    
    for period in bull_periods:
        result = run_period_backtest(
            period_name=period["name"],
            start_date=period["start"],
            end_date=period["end"],
            max_stocks=1000,  # 每个时段测试1000只股票
        )
        results.append(result)
    
    # 汇总结果
    logger.info("\n" + "=" * 70)
    logger.info("回测结果汇总")
    logger.info("=" * 70)
    
    successful_results = [r for r in results if r.get("success")]
    
    if successful_results:
        logger.info(f"\n{'时段':<20} {'周收益':<10} {'总收益':<12} {'夏普':<8} {'回撤':<10} {'胜率':<8}")
        logger.info("-" * 70)
        
        for r in successful_results:
            logger.info(
                f"{r['period']:<20} "
                f"{r['weekly_return']:>8.2%} "
                f"{r['total_return']:>10.2%} "
                f"{r['sharpe_ratio']:>6.2f} "
                f"{r['max_drawdown']:>8.2%} "
                f"{r['win_rate']:>6.1f}%"
            )
        
        # 计算平均
        avg_weekly = sum(r['weekly_return'] for r in successful_results) / len(successful_results)
        avg_sharpe = sum(r['sharpe_ratio'] for r in successful_results) / len(successful_results)
        logger.info("-" * 70)
        logger.info(f"{'平均':<20} {avg_weekly:>8.2%} {'-':>10} {avg_sharpe:>6.2f}")
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = output_dir / f"backtest_results_{timestamp}.json"
    
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": timestamp,
            "version": "V4.0",
            "results": results,
        }, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n结果已保存: {result_file}")
    
    # 生成报告
    report_file = output_dir / f"backtest_report_{timestamp}.md"
    generate_report(results, report_file)
    logger.info(f"报告已生成: {report_file}")
    
    return results


def generate_report(results: list, output_path: Path):
    """生成Markdown报告"""
    
    report = []
    report.append("# 牛市高回报策略 V4.0 - 回测报告\n")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    report.append("\n## 一、回测概览\n")
    report.append("| 时段 | 周收益 | 总收益 | 夏普比率 | 最大回撤 | 胜率 | 交易次数 |")
    report.append("|------|--------|--------|----------|----------|------|----------|")
    
    successful = [r for r in results if r.get("success")]
    for r in successful:
        report.append(
            f"| {r['period']} | {r['weekly_return']:.2%} | {r['total_return']:.2%} | "
            f"{r['sharpe_ratio']:.2f} | {r['max_drawdown']:.2%} | "
            f"{r['win_rate']:.1f}% | {r['total_trades']} |"
        )
    
    if successful:
        avg_weekly = sum(r['weekly_return'] for r in successful) / len(successful)
        avg_sharpe = sum(r['sharpe_ratio'] for r in successful) / len(successful)
        report.append(f"| **平均** | **{avg_weekly:.2%}** | - | **{avg_sharpe:.2f}** | - | - | - |")
    
    report.append("\n## 二、策略参数\n")
    report.append("```")
    report.append("涨停因子:")
    report.append("  - limit_up_threshold: 9.3%")
    report.append("  - vol_ratio_threshold_first: 2.5")
    report.append("止损止盈:")
    report.append("  - 硬止损: -10%")
    report.append("  - 软止损: -8% (持仓>=3天)")
    report.append("  - 第一批止盈: +20% (减仓50%)")
    report.append("  - 全止盈: +40%")
    report.append("  - 移动止损: 盈利+15%后, 回撤-9%")
    report.append("  - 时间止损: 20天")
    report.append("```")
    
    report.append("\n## 三、信号优先级\n")
    report.append("1. **首板启动** (80-90分): 首次涨停 + 量比 > 2.5")
    report.append("2. **连板加速** (70-80分): 近5日涨停次数 >= 2")
    report.append("3. **强势突破** (65-75分): 突破60日高点 + 5日动量 > 16% + 量比 > 1.5")
    report.append("4. **量价齐升** (60-70分): 5日动量 > 10% + 量比 > 2.0")
    
    report.append("\n## 四、下一步优化建议\n")
    report.append("根据回测结果，建议关注以下优化方向：\n")
    report.append("1. 调整止损止盈参数")
    report.append("2. 优化信号评分权重")
    report.append("3. 增加市场趋势过滤")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))


if __name__ == "__main__":
    main()
