#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整回测验证脚本 v010926
========================

功能：
1. 使用MongoDB存储的数据运行3个月回测
2. 按周滚动窗口验证策略稳定性
3. 生成详细的验证报告

使用方法：
    python scripts/run_full_backtest_validation_010926.py
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.batch_backtest_validator import (
    BatchBacktestValidator,
    ValidationCriteria
)
from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig
from core.advisor_v4.data_preloader import DataPreloader

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='完整回测验证工具 v010926 - 3个月数据，按周滚动',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用默认参数（2024-10-01至2024-12-31，3个月窗口，每周滚动）
  python scripts/run_full_backtest_validation_010926.py

  # 自定义时间范围
  python scripts/run_full_backtest_validation_010926.py \\
      --start-date 2024-10-01 \\
      --end-date 2024-12-31

  # 自定义窗口大小和步长
  python scripts/run_full_backtest_validation_010926.py \\
      --window-weeks 12 \\
      --step-weeks 1
        """
    )
    
    # 时间参数
    parser.add_argument('--start-date', type=str, default='2024-10-01',
                        help='开始日期 (YYYY-MM-DD，默认: 2024-10-01)')
    parser.add_argument('--end-date', type=str, default='2024-12-31',
                        help='结束日期 (YYYY-MM-DD，默认: 2024-12-31)')
    parser.add_argument('--window-weeks', type=int, default=12,
                        help='窗口大小（周，默认: 12周，约3个月）')
    parser.add_argument('--step-weeks', type=int, default=1,
                        help='滚动步长（周，默认: 1周）')
    
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
    parser.add_argument('--max-drawdown', type=float, default=25.0,
                        help='最大允许回撤（百分比，默认: 25.0表示25%）')
    parser.add_argument('--min-win-rate', type=float, default=0.35,
                        help='最低胜率')
    parser.add_argument('--min-return', type=float, default=-0.10,
                        help='最低总收益率')
    parser.add_argument('--min-trades', type=int, default=5,
                        help='最少交易次数')
    
    # 系统参数
    parser.add_argument('--cache-dir', type=str, default='data/cache',
                        help='数据缓存目录')
    parser.add_argument('--output-dir', type=str, 
                        default='output/advisor_v4/full_validation_010926',
                        help='输出目录')
    parser.add_argument('--no-gpu', action='store_true',
                        help='禁用GPU加速')
    parser.add_argument('--workers', type=int, default=3,
                        help='并行工作数')
    parser.add_argument('--no-mongodb', dest='use_mongodb', action='store_false', default=True,
                        help='禁用MongoDB存储')
    parser.add_argument('--force-refresh', action='store_true',
                        help='强制刷新数据（不使用缓存）')
    parser.add_argument('--quiet', action='store_true',
                        help='安静模式（减少输出）')
    
    args = parser.parse_args()
    
    # 打印启动信息
    print("=" * 70)
    print("🔍 完整回测验证工具 v010926 - Investment Advisor V4.0")
    print("=" * 70)
    print(f"\n📋 运行参数:")
    print(f"   时间范围: {args.start_date} ~ {args.end_date}")
    approx_months = args.window_weeks / 4.3  # 一个月约4.3周
    print(f"   窗口大小: {args.window_weeks} 周（约 {approx_months:.1f} 个月）")
    print(f"   滚动步长: {args.step_weeks} 周")
    print(f"   MongoDB存储: {'✅ 启用' if args.use_mongodb else '❌ 禁用'}")
    
    print(f"\n📊 策略参数:")
    print(f"   初始资金: {args.initial_capital:,.0f}")
    print(f"   最大持股: {args.max_stocks}")
    print(f"   单票仓位: {args.single_position:.0%}")
    print(f"   止损: {args.stop_loss:.0%}")
    print(f"   止盈: {args.take_profit:.0%}")
    
    print(f"\n✅ 验证标准:")
    print(f"   最低夏普比率: {args.min_sharpe}")
    print(f"   最大回撤: {args.max_drawdown:.1f}%")
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
    
    # 确保DataPreloader使用MongoDB
    if args.use_mongodb:
        validator.data_preloader.use_mongodb = True
        if validator.data_preloader.mongodb_storage:
            print(f"\n✅ MongoDB存储已启用: {validator.data_preloader.mongodb_storage.db_name}")
        else:
            print(f"\n⚠️  MongoDB存储初始化失败，将使用文件存储")
    
    validator.set_criteria(criteria)
    
    # 按需加载模式：不预先下载全部数据，让BulletTrade按需获取
    # 这样可以避免下载4000+只股票的全部数据
    print(f"\n📋 数据加载模式: 按需加载 (On-Demand)")
    print(f"   BulletTrade将在回测时自动获取需要的数据")
    print(f"   已下载的数据会缓存到MongoDB，加速后续回测")
    
    # 执行按周滚动验证
    try:
        print(f"\n🔄 开始按周滚动验证...")
        summary = validator.run_weekly_rolling_validation(
            start_date=args.start_date,
            end_date=args.end_date,
            window_weeks=args.window_weeks,
            step_weeks=args.step_weeks,
            strategy_config=strategy_config,
            initial_capital=args.initial_capital
        )
        
        # 输出最终结果
        print("\n" + "=" * 70)
        print("🎯 验证完成!")
        print("=" * 70)
        print(f"\n📈 结果概要:")
        print(f"   总时间段: {summary.total_periods}")
        if summary.total_periods > 0:
            print(f"   通过: {summary.passed_periods} ({summary.passed_periods/summary.total_periods*100:.1f}%)")
            print(f"   未通过: {summary.failed_periods}")
            print(f"   平均收益率: {summary.avg_return:.2f}%")
            print(f"   平均夏普比率: {summary.avg_sharpe:.2f}")
            print(f"   平均最大回撤: {summary.avg_max_drawdown:.2f}%")
            print(f"   一致性得分: {summary.consistency_score:.2f}")
            print(f"   稳定性得分: {summary.stability_score:.2f}")
        
        # MongoDB使用统计
        if args.use_mongodb and validator.data_preloader.mongodb_storage:
            stats = validator.data_preloader.mongodb_storage.get_storage_stats()
            print(f"\n📊 MongoDB存储统计:")
            print(f"   连接状态: {'✅ 已连接' if stats['connected'] else '❌ 未连接'}")
            if stats['connected']:
                for name, info in stats['collections'].items():
                    if 'count' in info:
                        print(f"   {name}: {info['count']:,} 条记录")
        
        # 结论
        if summary.total_periods > 0:
            pass_rate = summary.passed_periods / summary.total_periods
            if pass_rate >= 0.8:
                print(f"\n✅ 策略验证通过! 策略在多个时间段表现稳定。")
            elif pass_rate >= 0.6:
                print(f"\n⚠️ 策略部分通过。建议优化后再进行实盘。")
            else:
                print(f"\n❌ 策略验证未通过。需要重新审视策略逻辑。")
        
        # 报告路径（查找最新的验证报告）
        output_dir = Path(args.output_dir)
        report_files = list(output_dir.glob("validation_report_*.html"))
        if report_files:
            # 按修改时间排序，取最新的
            latest_report = max(report_files, key=lambda p: p.stat().st_mtime)
            print(f"\n📄 验证报告: {latest_report}")
        
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
