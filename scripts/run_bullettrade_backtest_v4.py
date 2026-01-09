#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investment Advisor V4.0 BulletTrade回测脚本

功能：
1. 生成策略代码（基于7个已验证因子）
2. 执行BulletTrade回测
3. 生成回测报告

使用方法：
    python scripts/run_bullettrade_backtest_v4.py --start-date 2024-01-01 --end-date 2024-12-31
"""

from __future__ import annotations

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.bullettrade_backtest import BulletTradeBacktest, StrategyConfig
from core.bullettrade.config import BTConfig
from core.advisor_v4.data_preloader import DataPreloader
from core.advisor_v4.gpu_accelerator import USE_GPU, GPUTechnicalIndicatorCalculator
import time


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Investment Advisor V4.0 BulletTrade回测')
    parser.add_argument('--start-date', type=str, required=True, help='回测开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, required=True, help='回测结束日期 (YYYY-MM-DD)')
    parser.add_argument('--initial-capital', type=float, default=1000000.0, help='初始资金 (默认: 1000000)')
    parser.add_argument('--max-stocks', type=int, default=10, help='最大持股数量 (默认: 10)')
    parser.add_argument('--single-position', type=float, default=0.20, help='单票最大仓位 (默认: 0.20)')
    parser.add_argument('--stop-loss', type=float, default=-0.08, help='止损比例 (默认: -0.08)')
    parser.add_argument('--take-profit', type=float, default=0.30, help='止盈比例 (默认: 0.30)')
    parser.add_argument('--output-dir', type=str, default='output/advisor_v4/bullettrade', help='输出目录')
    parser.add_argument('--strategy-filename', type=str, default=None, help='策略文件名（可选）')
    parser.add_argument('--cache-dir', type=str, default='data/cache', help='数据缓存目录')
    parser.add_argument('--use-gpu', action='store_true', default=True, help='使用GPU加速（默认启用）')
    parser.add_argument('--no-gpu', dest='use_gpu', action='store_false', help='禁用GPU加速')
    parser.add_argument('--preload-data', action='store_true', default=True, help='预加载数据到缓存（默认启用）')
    parser.add_argument('--no-preload', dest='preload_data', action='store_false', help='禁用数据预加载')
    parser.add_argument('--min-total-score', type=float, default=30.0, help='最小综合得分 (默认: 30.0)')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Investment Advisor V4.0 BulletTrade回测")
    print("=" * 80)
    print(f"\n📋 回测参数:")
    print(f"   开始日期: {args.start_date}")
    print(f"   结束日期: {args.end_date}")
    print(f"   初始资金: {args.initial_capital:,.0f}")
    print(f"   最大持股: {args.max_stocks}只")
    print(f"   单票仓位: {args.single_position:.0%}")
    print(f"   止损: {args.stop_loss:.0%}")
    print(f"   止盈: {args.take_profit:.0%}")
    print(f"   输出目录: {args.output_dir}")
    print(f"   缓存目录: {args.cache_dir}")
    print(f"   GPU加速: {'✅ 启用' if args.use_gpu and USE_GPU else '❌ 禁用'}")
    print(f"   数据预加载: {'✅ 启用' if args.preload_data else '❌ 禁用'}")
    
    # GPU状态检查
    if args.use_gpu:
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                print(f"   GPU型号: {gpu_name}")
                print(f"   GPU显存: {gpu_memory:.1f} GB")
            else:
                print(f"   ⚠️  GPU不可用，将使用CPU")
        except ImportError:
            print(f"   ⚠️  PyTorch未安装，将使用CPU")
    
    # 数据预加载（如果启用）
    if args.preload_data:
        print("\n📥 数据预加载...")
        preload_start = time.time()
        preloader = DataPreloader(
            max_workers=3,  # JQData连接数
            cache_dir=args.cache_dir,
            verbose=True
        )
        preload_result = preloader.preload_market_data(
            start_date=args.start_date,
            end_date=args.end_date,
            force_refresh=False  # 使用缓存
        )
        preload_duration = time.time() - preload_start
        print(f"   ✅ 数据预加载完成")
        print(f"   耗时: {preload_duration:.1f} 秒")
        print(f"   股票数: {preload_result.total_stocks}")
        print(f"   数据大小: {preload_result.data_size_mb:.1f} MB")
        print(f"   缓存文件数: {len(preload_result.cache_paths)}")
    
    # 配置策略参数
    strategy_config = StrategyConfig(
        max_stocks=args.max_stocks,
        single_position_max=args.single_position,
        stop_loss=args.stop_loss,
        take_profit=args.take_profit,
        min_total_score=args.min_total_score,
    )
    
    # 配置回测参数
    bt_config = BTConfig(
        start_date=args.start_date,
        end_date=args.end_date,
        initial_capital=args.initial_capital,
        benchmark="000300.XSHG",
        frequency="day",
        data_provider="jqdata",
        output_dir=args.output_dir,
        generate_html=True,
        generate_csv=True,
    )
    
    # 创建回测接口（传递缓存目录）
    backtest = BulletTradeBacktest(
        strategy_config=strategy_config,
        bt_config=bt_config,
        output_dir=args.output_dir,
        cache_dir=args.cache_dir if args.preload_data else None
    )
    
    # 执行回测
    print("\n🚀 开始回测...")
    backtest_start = time.time()
    try:
        result = backtest.run_backtest(
            start_date=args.start_date,
            end_date=args.end_date,
            initial_capital=args.initial_capital,
            strategy_filename=args.strategy_filename,
        )
        
        # 输出回测结果
        backtest_duration = time.time() - backtest_start
        print("\n" + "=" * 80)
        print("📊 回测结果")
        print("=" * 80)
        print(f"\n⏱️  性能统计:")
        print(f"   回测耗时: {backtest_duration:.1f} 秒")
        if hasattr(result, 'runtime_seconds') and result.runtime_seconds > 0:
            print(f"   引擎耗时: {result.runtime_seconds:.1f} 秒")
        if args.preload_data:
            trading_days = result.trading_days if hasattr(result, 'trading_days') and result.trading_days > 0 else 0
            if trading_days > 0:
                print(f"   平均每交易日: {backtest_duration/trading_days:.2f} 秒")
        
        print(f"\n🚀 加速状态:")
        print(f"   GPU加速: {'✅ 已启用' if args.use_gpu and USE_GPU else '❌ 未启用'}")
        print(f"   数据缓存: {'✅ 已启用' if args.preload_data else '❌ 未启用'}")
        if args.preload_data:
            print(f"   缓存目录: {args.cache_dir}")
        
        print(f"\n📈 回测指标:")
        # 计算Calmar比率
        calmar_ratio = 0.0
        if result.max_drawdown != 0:
            calmar_ratio = result.annual_return / abs(result.max_drawdown)
        
        print(f"   总收益率: {result.total_return:.2f}%")  # 已经是百分比形式
        print(f"   年化收益: {result.annual_return:.2f}%")  # 已经是百分比形式
        print(f"   夏普比率: {result.sharpe_ratio:.2f}")
        print(f"   最大回撤: {result.max_drawdown:.2f}%")  # 已经是百分比形式
        print(f"   卡玛比率: {calmar_ratio:.2f}")
        print(f"   胜率: {result.win_rate:.2f}%")  # 已经是百分比形式
        print(f"   总交易次数: {result.total_trades}")
        if hasattr(result, 'trading_days') and result.trading_days > 0:
            print(f"   交易天数: {result.trading_days}")
        print(f"   报告路径: {result.report_path}")
        print("=" * 80)
        
        # 生成融合报告：结合BulletTrade报告和增强功能
        if result.report_path:
            try:
                from core.advisor_v4.fused_report_generator import generate_fused_report
                print("\n📝 正在生成融合报告（BulletTrade + 增强功能）...")
                fused_path = generate_fused_report(
                    bullet_trade_html_path=result.report_path,
                    output_path=None,  # 覆盖原文件
                    enhance_charts=True,  # 增强图表数据精确性
                    enhance_data_precision=True,  # 提升数值精度
                    add_company_names=True,  # 添加公司名称
                )
                print(f"   ✅ 融合报告已生成: {fused_path}")
            except Exception as e:
                print(f"   ⚠️  生成融合报告失败: {e}")
                import traceback
                traceback.print_exc()
                # 降级到简单的增强报告
                try:
                    from core.advisor_v4.enhance_html_report import enhance_html_report
                    print("   📝 降级到简单增强报告...")
                    enhanced_path = enhance_html_report(result.report_path)
                    print(f"   ✅ 增强后的报告: {enhanced_path}")
                except Exception as e2:
                    print(f"   ❌ 增强报告也失败: {e2}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 回测失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
