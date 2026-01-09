#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
半年基准回测脚本
================

Phase 0 任务: 执行半年基准回测（2024-07-01至2024-12-31），验证系统可行性

功能：
1. 数据预加载（并行下载）
2. 因子计算（GPU加速）
3. BulletTrade回测执行
4. 结果分析和报告生成

使用方法：
    python scripts/run_6month_baseline_backtest.py
    python scripts/run_6month_baseline_backtest.py --start-date 2024-07-01 --end-date 2024-12-31
    python scripts/run_6month_baseline_backtest.py --force-refresh  # 强制刷新缓存
"""

from __future__ import annotations

import sys
import argparse
import time
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='半年基准回测（Phase 0）')
    parser.add_argument('--start-date', type=str, default='2024-07-01', help='回测开始日期 (默认: 2024-07-01)')
    parser.add_argument('--end-date', type=str, default='2024-12-31', help='回测结束日期 (默认: 2024-12-31)')
    parser.add_argument('--initial-capital', type=float, default=1000000.0, help='初始资金 (默认: 1000000)')
    parser.add_argument('--cache-dir', type=str, default='data/cache', help='数据缓存目录')
    parser.add_argument('--output-dir', type=str, default='output/advisor_v4/baseline', help='输出目录')
    parser.add_argument('--force-refresh', action='store_true', help='强制刷新缓存')
    parser.add_argument('--max-stocks', type=int, default=10, help='最大持股数量 (默认: 10)')
    parser.add_argument('--single-position', type=float, default=0.20, help='单票最大仓位 (默认: 0.20)')
    parser.add_argument('--stop-loss', type=float, default=-0.08, help='止损比例 (默认: -0.08)')
    parser.add_argument('--take-profit', type=float, default=0.30, help='止盈比例 (默认: 0.30)')
    parser.add_argument('--min-score', type=float, default=30.0, help='最低综合得分阈值 (默认: 30.0)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🎯 半年基准回测 - Phase 0")
    print("=" * 70)
    print(f"\n📋 回测参数:")
    print(f"   时间段: {args.start_date} ~ {args.end_date}")
    print(f"   初始资金: {args.initial_capital:,.0f}")
    print(f"   缓存目录: {args.cache_dir}")
    print(f"   输出目录: {args.output_dir}")
    print(f"   强制刷新: {'是' if args.force_refresh else '否'}")
    print(f"\n📊 策略参数:")
    print(f"   最大持股: {args.max_stocks}只")
    print(f"   单票仓位: {args.single_position:.0%}")
    print(f"   止损: {args.stop_loss:.0%}")
    print(f"   止盈: {args.take_profit:.0%}")
    print(f"   最低得分: {args.min_score}")
    
    start_time = time.time()
    
    # 导入模块
    from core.advisor_v4.data_preloader import DataPreloader, preload_6month_data
    from core.advisor_v4.parallel_backtest_runner import ParallelBacktestRunner, run_6month_baseline_backtest
    from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig
    
    # Step 1: 数据预加载
    print(f"\n{'='*70}")
    print("📥 Step 1: 数据预加载")
    print("=" * 70)
    
    preloader = DataPreloader(
        max_workers=3,
        cache_dir=args.cache_dir,
        verbose=True
    )
    
    preload_result = preloader.preload_market_data(
        start_date=args.start_date,
        end_date=args.end_date,
        force_refresh=args.force_refresh
    )
    
    if not preload_result.success:
        print(f"\n❌ 数据预加载失败:")
        for err in preload_result.errors:
            print(f"   - {err}")
        return 1
    
    print(f"\n✅ 数据预加载完成")
    print(f"   股票数: {preload_result.total_stocks}")
    print(f"   数据大小: {preload_result.data_size_mb:.1f} MB")
    print(f"   耗时: {preload_result.duration_seconds:.1f} 秒")
    
    # 下载指数数据
    index_paths = preloader.preload_index_data(
        start_date=args.start_date,
        end_date=args.end_date,
        force_refresh=args.force_refresh
    )
    print(f"   指数数据: {len(index_paths)} 个")
    
    # Step 2: 执行回测
    print(f"\n{'='*70}")
    print("🚀 Step 2: 执行回测")
    print("=" * 70)
    
    # 配置策略
    strategy_config = StrategyConfig(
        max_stocks=args.max_stocks,
        single_position_max=args.single_position,
        stop_loss=args.stop_loss,
        take_profit=args.take_profit,
        trailing_stop=0.15,
        time_stop_days=20,
        min_total_score=args.min_score
    )
    
    # 创建运行器
    runner = ParallelBacktestRunner(
        cache_dir=args.cache_dir,
        output_dir=args.output_dir,
        use_gpu=True,
        max_workers=3,
        verbose=True
    )
    
    # 执行回测
    backtest_result = runner.run_backtest_with_cache(
        start_date=args.start_date,
        end_date=args.end_date,
        strategy_config=strategy_config,
        initial_capital=args.initial_capital,
        task_id="6month_baseline"
    )
    
    # Step 3: 结果分析
    print(f"\n{'='*70}")
    print("📊 Step 3: 回测结果")
    print("=" * 70)
    
    total_time = time.time() - start_time
    
    if backtest_result.success:
        print(f"\n✅ 回测成功完成！")
        print(f"\n📈 绩效指标:")
        # 注意: BTResult中的返回值已经是小数形式(如0.0952表示9.52%)
        total_return_pct = backtest_result.total_return * 100 if abs(backtest_result.total_return) < 10 else backtest_result.total_return
        annual_return_pct = backtest_result.annual_return * 100 if abs(backtest_result.annual_return) < 10 else backtest_result.annual_return
        max_drawdown_pct = backtest_result.max_drawdown * 100 if abs(backtest_result.max_drawdown) < 10 else backtest_result.max_drawdown
        win_rate_pct = backtest_result.win_rate * 100 if abs(backtest_result.win_rate) < 10 else backtest_result.win_rate
        
        print(f"   总收益率: {total_return_pct:.2f}%")
        print(f"   年化收益: {annual_return_pct:.2f}%")
        print(f"   夏普比率: {backtest_result.sharpe_ratio:.2f}")
        print(f"   最大回撤: {max_drawdown_pct:.2f}%")
        print(f"   卡玛比率: {backtest_result.calmar_ratio:.2f}")
        print(f"   胜率: {win_rate_pct:.2f}%")
        print(f"   总交易次数: {backtest_result.total_trades}")
        
        print(f"\n📁 输出文件:")
        print(f"   报告路径: {backtest_result.report_path}")
        
        # 绩效评估
        print(f"\n📋 绩效评估:")
        if backtest_result.sharpe_ratio >= 1.0:
            print(f"   ✅ 夏普比率 >= 1.0: 通过")
        else:
            print(f"   ⚠️  夏普比率 < 1.0: 需要优化")
        
        if abs(backtest_result.max_drawdown) <= 0.20:
            print(f"   ✅ 最大回撤 <= 20%: 通过")
        else:
            print(f"   ⚠️  最大回撤 > 20%: 需要优化")
        
        if backtest_result.win_rate >= 0.50:
            print(f"   ✅ 胜率 >= 50%: 通过")
        else:
            print(f"   ⚠️  胜率 < 50%: 需要优化")
        
    else:
        print(f"\n❌ 回测失败: {backtest_result.error}")
        return 1
    
    print(f"\n⏱️  总耗时: {total_time:.1f} 秒")
    print(f"   - 数据预加载: {preload_result.duration_seconds:.1f} 秒")
    print(f"   - 回测执行: {backtest_result.duration_seconds:.1f} 秒")
    
    # 保存执行日志
    log_path = Path(args.output_dir) / "execution_log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    import json
    execution_log = {
        "timestamp": datetime.now().isoformat(),
        "parameters": {
            "start_date": args.start_date,
            "end_date": args.end_date,
            "initial_capital": args.initial_capital,
            "strategy_config": {
                "max_stocks": args.max_stocks,
                "single_position_max": args.single_position,
                "stop_loss": args.stop_loss,
                "take_profit": args.take_profit,
                "min_total_score": args.min_score
            }
        },
        "preload": {
            "success": preload_result.success,
            "total_stocks": preload_result.total_stocks,
            "data_size_mb": preload_result.data_size_mb,
            "duration_seconds": preload_result.duration_seconds
        },
        "backtest": backtest_result.to_dict(),
        "total_duration_seconds": total_time
    }
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(execution_log, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 执行日志已保存: {log_path}")
    
    print(f"\n{'='*70}")
    print("✅ Phase 0 完成！")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
