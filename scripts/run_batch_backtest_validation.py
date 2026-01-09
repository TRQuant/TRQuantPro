#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量回测验证脚本
================

使用方法:
    # 滚动窗口验证（默认）
    python scripts/run_batch_backtest_validation.py

    # 指定时间范围和窗口大小
    python scripts/run_batch_backtest_validation.py --start-date 2023-01-01 --end-date 2024-12-31 --window 6 --step 3
    
    # 季度验证
    python scripts/run_batch_backtest_validation.py --mode quarterly --start-year 2023 --end-year 2024
    
    # 年度验证
    python scripts/run_batch_backtest_validation.py --mode yearly --start-year 2020 --end-year 2024
    
    # 自定义时间段
    python scripts/run_batch_backtest_validation.py --mode custom --periods "2024-01-01,2024-06-30,H1_2024;2024-07-01,2024-12-31,H2_2024"
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.batch_backtest_validator import (
    BatchBacktestValidator,
    ValidationCriteria,
    BacktestPeriod
)
from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_custom_periods(periods_str: str):
    """解析自定义时间段字符串"""
    periods = []
    for period_def in periods_str.split(";"):
        parts = period_def.strip().split(",")
        if len(parts) >= 2:
            start_date = parts[0].strip()
            end_date = parts[1].strip()
            label = parts[2].strip() if len(parts) > 2 else f"{start_date}_{end_date}"
            periods.append((start_date, end_date, label))
    return periods


def main():
    parser = argparse.ArgumentParser(
        description='批量回测验证工具 - 支持多时间段回测验证',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 滚动窗口验证（默认半年窗口，每月滚动）
  python scripts/run_batch_backtest_validation.py --start-date 2024-01-01 --end-date 2024-12-31

  # 季度验证
  python scripts/run_batch_backtest_validation.py --mode quarterly --start-year 2023 --end-year 2024

  # 年度验证
  python scripts/run_batch_backtest_validation.py --mode yearly --start-year 2020 --end-year 2024

  # 自定义宽松验证标准
  python scripts/run_batch_backtest_validation.py --min-sharpe 0.3 --max-drawdown 0.30
        """
    )
    
    # 模式选择
    parser.add_argument('--mode', type=str, default='rolling',
                        choices=['rolling', 'quarterly', 'yearly', 'custom'],
                        help='验证模式: rolling(滚动窗口), quarterly(季度), yearly(年度), custom(自定义)')
    
    # 滚动窗口参数
    parser.add_argument('--start-date', type=str, default='2024-01-01',
                        help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, default='2024-12-31',
                        help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--window', type=int, default=6,
                        help='窗口大小（月，仅用于rolling模式）')
    parser.add_argument('--step', type=int, default=1,
                        help='滚动步长（月，仅用于rolling模式）')
    
    # 年度/季度参数
    parser.add_argument('--start-year', type=int, default=2024,
                        help='开始年份（用于quarterly/yearly模式）')
    parser.add_argument('--end-year', type=int, default=2024,
                        help='结束年份（用于quarterly/yearly模式）')
    
    # 自定义时间段
    parser.add_argument('--periods', type=str, default=None,
                        help='自定义时间段（格式: start,end,label;start,end,label;...）')
    
    # 策略参数
    parser.add_argument('--initial-capital', type=float, default=1000000.0,
                        help='初始资金')
    parser.add_argument('--max-stocks', type=int, default=10,
                        help='最大持股数量')
    parser.add_argument('--single-position', type=float, default=0.20,
                        help='单票最大仓位')
    parser.add_argument('--stop-loss', type=float, default=-0.08,
                        help='止损比例')
    parser.add_argument('--take-profit', type=float, default=0.30,
                        help='止盈比例')
    parser.add_argument('--min-total-score', type=float, default=30.0,
                        help='最小综合得分')
    
    # 验证标准
    parser.add_argument('--min-sharpe', type=float, default=0.5,
                        help='最低夏普比率')
    parser.add_argument('--max-drawdown', type=float, default=0.25,
                        help='最大允许回撤（绝对值）')
    parser.add_argument('--min-win-rate', type=float, default=0.35,
                        help='最低胜率')
    parser.add_argument('--min-return', type=float, default=-0.10,
                        help='最低总收益率')
    parser.add_argument('--min-trades', type=int, default=5,
                        help='最少交易次数')
    
    # 系统参数
    parser.add_argument('--cache-dir', type=str, default='data/cache',
                        help='数据缓存目录')
    parser.add_argument('--output-dir', type=str, default='output/advisor_v4/batch_validation',
                        help='输出目录')
    parser.add_argument('--no-gpu', action='store_true',
                        help='禁用GPU加速')
    parser.add_argument('--workers', type=int, default=3,
                        help='并行工作数')
    parser.add_argument('--quiet', action='store_true',
                        help='安静模式（减少输出）')
    
    args = parser.parse_args()
    
    # 打印启动信息
    print("=" * 70)
    print("🔍 批量回测验证工具 - Investment Advisor V4.0")
    print("=" * 70)
    print(f"\n📋 运行参数:")
    print(f"   验证模式: {args.mode}")
    
    if args.mode == 'rolling':
        print(f"   时间范围: {args.start_date} ~ {args.end_date}")
        print(f"   窗口大小: {args.window} 个月")
        print(f"   滚动步长: {args.step} 个月")
    elif args.mode in ['quarterly', 'yearly']:
        print(f"   年份范围: {args.start_year} ~ {args.end_year}")
    elif args.mode == 'custom':
        print(f"   自定义时间段: {args.periods}")
    
    print(f"\n📊 策略参数:")
    print(f"   初始资金: {args.initial_capital:,.0f}")
    print(f"   最大持股: {args.max_stocks}")
    print(f"   单票仓位: {args.single_position:.0%}")
    print(f"   止损: {args.stop_loss:.0%}")
    print(f"   止盈: {args.take_profit:.0%}")
    
    print(f"\n✅ 验证标准:")
    print(f"   最低夏普比率: {args.min_sharpe}")
    print(f"   最大回撤: {args.max_drawdown:.0%}")
    print(f"   最低胜率: {args.min_win_rate:.0%}")
    print(f"   最低收益率: {args.min_return:.0%}")
    print(f"   最少交易次数: {args.min_trades}")
    
    # 创建策略配置
    strategy_config = StrategyConfig(
        max_stocks=args.max_stocks,
        single_position_max=args.single_position,
        stop_loss=args.stop_loss,
        take_profit=args.take_profit,
        min_total_score=args.min_total_score
    )
    
    # 创建验证标准
    criteria = ValidationCriteria(
        min_sharpe=args.min_sharpe,
        max_drawdown=args.max_drawdown,
        min_win_rate=args.min_win_rate,
        min_total_return=args.min_return,
        min_trades=args.min_trades
    )
    
    # 创建验证器
    validator = BatchBacktestValidator(
        cache_dir=args.cache_dir,
        output_dir=args.output_dir,
        use_gpu=not args.no_gpu,
        max_workers=args.workers,
        verbose=not args.quiet
    )
    
    validator.set_criteria(criteria)
    
    # 根据模式执行验证
    try:
        if args.mode == 'rolling':
            summary = validator.run_rolling_validation(
                start_date=args.start_date,
                end_date=args.end_date,
                window_months=args.window,
                step_months=args.step,
                strategy_config=strategy_config,
                initial_capital=args.initial_capital
            )
        
        elif args.mode == 'quarterly':
            summary = validator.run_quarterly_validation(
                start_year=args.start_year,
                end_year=args.end_year,
                strategy_config=strategy_config,
                initial_capital=args.initial_capital
            )
        
        elif args.mode == 'yearly':
            summary = validator.run_yearly_validation(
                start_year=args.start_year,
                end_year=args.end_year,
                strategy_config=strategy_config,
                initial_capital=args.initial_capital
            )
        
        elif args.mode == 'custom':
            if not args.periods:
                print("❌ 错误: 自定义模式需要指定 --periods 参数")
                return 1
            
            period_defs = parse_custom_periods(args.periods)
            periods = validator.generate_custom_periods(period_defs)
            
            summary = validator.run_validation(
                periods=periods,
                strategy_config=strategy_config,
                initial_capital=args.initial_capital
            )
        
        # 输出最终结果
        print("\n" + "=" * 70)
        print("🎯 验证完成!")
        print("=" * 70)
        print(f"\n📈 结果概要:")
        print(f"   总时间段: {summary.total_periods}")
        print(f"   通过: {summary.passed_periods} ({summary.passed_periods/summary.total_periods*100:.1f}%)")
        print(f"   未通过: {summary.failed_periods}")
        print(f"   一致性得分: {summary.consistency_score:.2f}")
        print(f"   稳定性得分: {summary.stability_score:.2f}")
        
        # 结论
        if summary.passed_periods / summary.total_periods >= 0.8:
            print(f"\n✅ 策略验证通过! 策略在多个时间段表现稳定。")
        elif summary.passed_periods / summary.total_periods >= 0.6:
            print(f"\n⚠️ 策略部分通过。建议优化后再进行实盘。")
        else:
            print(f"\n❌ 策略验证未通过。需要重新审视策略逻辑。")
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断执行")
        return 130
    
    except Exception as e:
        print(f"\n❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
