#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
因子优化命令行工具
==================

功能：
- 运行因子选择和权重优化
- 支持配置优化范围、验证方法、优化目标
- 生成优化报告

用法：
    python scripts/optimize_factors_v4.py --start-date 2024-01-01 --end-date 2025-12-31
    python scripts/optimize_factors_v4.py --quick  # 快速测试模式
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import argparse
from datetime import datetime, timedelta
from core.advisor_v4.advisor_v4_workflow import AdvisorV4Workflow, AdvisorV4Config
from core.advisor_v4.factor_optimizer import FactorOptimizationConfig


def main():
    parser = argparse.ArgumentParser(description="因子优化工具 - 递归优化因子选择和权重")
    
    # 日期参数
    parser.add_argument(
        '--start-date',
        type=str,
        default=None,
        help='优化开始日期 (YYYY-MM-DD)，默认使用config中的train_start',
    )
    parser.add_argument(
        '--end-date',
        type=str,
        default=None,
        help='优化结束日期 (YYYY-MM-DD)，默认使用config中的test_end',
    )
    
    # 优化配置
    parser.add_argument(
        '--enable-factor-selection',
        action='store_true',
        default=True,
        help='启用因子选择优化（默认启用）',
    )
    parser.add_argument(
        '--disable-factor-selection',
        action='store_false',
        dest='enable_factor_selection',
        help='禁用因子选择优化',
    )
    parser.add_argument(
        '--enable-weight-optimization',
        action='store_true',
        default=True,
        help='启用权重优化（默认启用）',
    )
    parser.add_argument(
        '--disable-weight-optimization',
        action='store_false',
        dest='enable_weight_optimization',
        help='禁用权重优化',
    )
    parser.add_argument(
        '--enable-fusion-optimization',
        action='store_true',
        default=True,
        help='启用融合权重优化（默认启用）',
    )
    parser.add_argument(
        '--disable-fusion-optimization',
        action='store_false',
        dest='enable_fusion_optimization',
        help='禁用融合权重优化',
    )
    
    # 优化方法
    parser.add_argument(
        '--optimization-method',
        type=str,
        choices=['grid', 'bayesian', 'genetic'],
        default='grid',
        help='优化方法（默认：grid）',
    )
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=10,
        help='最大迭代次数（默认：10）',
    )
    parser.add_argument(
        '--early-stop-patience',
        type=int,
        default=3,
        help='早停耐心值（默认：3）',
    )
    
    # Walk-Forward验证配置
    parser.add_argument(
        '--train-months',
        type=int,
        default=3,
        help='Walk-Forward训练窗口（月，默认：3）',
    )
    parser.add_argument(
        '--test-months',
        type=int,
        default=1,
        help='Walk-Forward测试窗口（月，默认：1）',
    )
    parser.add_argument(
        '--step-months',
        type=int,
        default=1,
        help='Walk-Forward滚动步长（月，默认：1）',
    )
    
    # 多目标权重
    parser.add_argument(
        '--sharpe-weight',
        type=float,
        default=0.4,
        help='夏普比率权重（默认：0.4）',
    )
    parser.add_argument(
        '--hit-rate-weight',
        type=float,
        default=0.3,
        help='命中率权重（默认：0.3）',
    )
    parser.add_argument(
        '--return-weight',
        type=float,
        default=0.3,
        help='收益率权重（默认：0.3）',
    )
    
    # 快速测试模式
    parser.add_argument(
        '--quick',
        action='store_true',
        help='快速测试模式（减少迭代次数和搜索空间）',
    )
    
    # 其他选项
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='输出详细信息（默认启用）',
    )
    
    args = parser.parse_args()
    
    # 快速测试模式调整
    if args.quick:
        args.max_iterations = 3
        args.early_stop_patience = 2
        print("⚠️ 快速测试模式：减少迭代次数和搜索空间")
    
    # 验证权重和
    total_weight = args.sharpe_weight + args.hit_rate_weight + args.return_weight
    if abs(total_weight - 1.0) > 0.01:
        print(f"⚠️ 警告：目标权重和不为1.0 ({total_weight:.2f})，将自动归一化")
        args.sharpe_weight /= total_weight
        args.hit_rate_weight /= total_weight
        args.return_weight /= total_weight
    
    # 创建优化配置
    opt_config = FactorOptimizationConfig(
        enable_factor_selection=args.enable_factor_selection,
        enable_weight_optimization=args.enable_weight_optimization,
        enable_fusion_optimization=args.enable_fusion_optimization,
        optimization_method=args.optimization_method,
        max_iterations=args.max_iterations,
        early_stop_patience=args.early_stop_patience,
        train_months=args.train_months,
        test_months=args.test_months,
        step_months=args.step_months,
        objective_weights={
            'sharpe': args.sharpe_weight,
            'hit_rate': args.hit_rate_weight,
            'return': args.return_weight,
        },
    )
    
    # 创建V4工作流
    v4_config = AdvisorV4Config()
    workflow = AdvisorV4Workflow(config=v4_config, verbose=args.verbose)
    
    # 运行优化
    print(f"\n{'='*70}")
    print("【因子优化工具】")
    print(f"{'='*70}")
    print(f"优化配置:")
    print(f"  因子选择: {'启用' if opt_config.enable_factor_selection else '禁用'}")
    print(f"  权重优化: {'启用' if opt_config.enable_weight_optimization else '禁用'}")
    print(f"  融合权重优化: {'启用' if opt_config.enable_fusion_optimization else '禁用'}")
    print(f"  优化方法: {opt_config.optimization_method}")
    print(f"  最大迭代次数: {opt_config.max_iterations}")
    print(f"  目标权重: 夏普{opt_config.objective_weights['sharpe']:.1%} / "
          f"命中率{opt_config.objective_weights['hit_rate']:.1%} / "
          f"收益率{opt_config.objective_weights['return']:.1%}")
    print(f"{'='*70}\n")
    
    try:
        result = workflow.optimize_factors(
            start_date=args.start_date,
            end_date=args.end_date,
            config=opt_config,
        )
        
        # 输出结果摘要
        if result and result.best_result:
            best = result.best_result
            print(f"\n{'='*70}")
            print("【优化完成】")
            print(f"{'='*70}")
            print(f"最优因子组合: {', '.join(best.factor_selection)} ({len(best.factor_selection)}个因子)")
            print(f"最优融合权重: 已验证 {best.fusion_weight:.1%} / 聚宽 {1-best.fusion_weight:.1%}")
            print(f"综合得分: {best.multi_objective_score:.2f}")
            print(f"夏普比率: {best.sharpe_ratio:.3f}")
            print(f"命中率: {best.hit_rate:.2%}")
            print(f"总收益率: {best.total_return:.2%}")
            print(f"稳定性得分: {best.stability_score:.3f}")
            print(f"过拟合风险: {best.overfitting_risk.upper()}")
            print(f"优化耗时: {result.optimization_time_seconds:.1f} 秒")
            print(f"{'='*70}")
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断优化")
        return 1
    except Exception as e:
        print(f"\n❌ 优化失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
