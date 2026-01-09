#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量回测性能测试脚本
====================

测试内容：
1. 数据下载和缓存功能
2. 并行处理性能
3. GPU加速效果
4. 输出详细的性能报告
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
import logging

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.batch_backtest_validator import (
    BatchBacktestValidator,
    ValidationCriteria
)
from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig

# GPU检查
try:
    import torch
    GPU_AVAILABLE = torch.cuda.is_available()
    if GPU_AVAILABLE:
        GPU_NAME = torch.cuda.get_device_name(0)
        GPU_MEMORY = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    else:
        GPU_NAME = "N/A"
        GPU_MEMORY = 0
except ImportError:
    GPU_AVAILABLE = False
    GPU_NAME = "PyTorch未安装"
    GPU_MEMORY = 0

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_system_info():
    """打印系统信息"""
    print("=" * 80)
    print("🖥️  系统信息")
    print("=" * 80)
    print(f"   GPU可用: {'✅ 是' if GPU_AVAILABLE else '❌ 否'}")
    if GPU_AVAILABLE:
        print(f"   GPU型号: {GPU_NAME}")
        print(f"   GPU显存: {GPU_MEMORY:.1f} GB")
    print()


def test_data_preloading(validator, start_date, end_date):
    """测试数据预加载"""
    print("=" * 80)
    print("📥 测试1: 数据下载和缓存")
    print("=" * 80)
    
    start_time = time.time()
    
    # 预加载数据
    result = validator.data_preloader.preload_market_data(
        start_date=start_date,
        end_date=end_date,
        force_refresh=False  # 使用缓存
    )
    
    duration = time.time() - start_time
    
    print(f"\n✅ 数据预加载完成")
    print(f"   耗时: {duration:.1f} 秒")
    print(f"   股票数: {result.total_stocks}")
    print(f"   交易日数: {result.total_trading_days}")
    print(f"   数据大小: {result.data_size_mb:.1f} MB")
    print(f"   缓存文件数: {len(result.cache_paths)}")
    
    # 检查缓存状态
    cache_info = validator.data_preloader.get_cache_info()
    print(f"\n📦 缓存状态:")
    for subdir, info in cache_info.get("cached_files", {}).items():
        print(f"   {subdir}: {info['count']} 个文件, {info['size_mb']:.1f} MB")
    
    return {
        "duration": duration,
        "total_stocks": result.total_stocks,
        "data_size_mb": result.data_size_mb,
        "cache_files": len(result.cache_paths)
    }


def test_parallel_processing(validator, periods):
    """测试并行处理"""
    print("\n" + "=" * 80)
    print("⚡ 测试2: 并行处理性能")
    print("=" * 80)
    
    print(f"\n📊 并行配置:")
    print(f"   并行工作数: {validator.max_workers}")
    print(f"   时间段数: {len(periods)}")
    
    # 测试串行执行（模拟）
    print(f"\n🔄 执行回测（并行模式）...")
    
    start_time = time.time()
    
    # 执行验证（实际是并行的）
    summary = validator.run_validation(
        periods=periods,
        preload_data=False,  # 数据已预加载
        strategy_config=StrategyConfig(
            max_stocks=10,
            single_position_max=0.20,
            stop_loss=-0.08,
            take_profit=0.30,
            min_total_score=30.0
        ),
        initial_capital=1000000.0
    )
    
    duration = time.time() - start_time
    
    print(f"\n✅ 并行回测完成")
    print(f"   总耗时: {duration:.1f} 秒")
    print(f"   平均每个时间段: {duration/len(periods):.1f} 秒")
    print(f"   总时间段数: {summary.total_periods}")
    print(f"   通过数: {summary.passed_periods}")
    print(f"   未通过数: {summary.failed_periods}")
    
    return {
        "total_duration": duration,
        "avg_per_period": duration / len(periods) if periods else 0,
        "total_periods": summary.total_periods,
        "passed": summary.passed_periods,
        "failed": summary.failed_periods
    }


def test_gpu_acceleration(validator):
    """测试GPU加速"""
    print("\n" + "=" * 80)
    print("🚀 测试3: GPU加速功能")
    print("=" * 80)
    
    gpu_status = {
        "available": GPU_AVAILABLE,
        "name": GPU_NAME,
        "memory_gb": GPU_MEMORY,
        "enabled": validator.use_gpu
    }
    
    print(f"\n📊 GPU状态:")
    print(f"   GPU可用: {'✅ 是' if GPU_AVAILABLE else '❌ 否'}")
    if GPU_AVAILABLE:
        print(f"   GPU型号: {GPU_NAME}")
        print(f"   GPU显存: {GPU_MEMORY:.1f} GB")
    print(f"   加速启用: {'✅ 是' if validator.use_gpu else '❌ 否'}")
    
    if validator.runner.gpu_calculator:
        print(f"   GPU计算器: ✅ 已初始化")
    else:
        print(f"   GPU计算器: ❌ 未初始化")
    
    # 如果有GPU，测试计算性能
    if GPU_AVAILABLE and validator.use_gpu:
        try:
            import torch
            import numpy as np
            
            print(f"\n🧪 GPU性能测试:")
            
            # 测试GPU计算速度
            test_data = torch.randn(1000, 100).cuda()
            start_time = time.time()
            for _ in range(100):
                _ = torch.matmul(test_data, test_data.T)
            torch.cuda.synchronize()
            gpu_time = time.time() - start_time
            
            # 测试CPU计算速度
            test_data_cpu = torch.randn(1000, 100)
            start_time = time.time()
            for _ in range(100):
                _ = torch.matmul(test_data_cpu, test_data_cpu.T)
            cpu_time = time.time() - start_time
            
            speedup = cpu_time / gpu_time if gpu_time > 0 else 0
            
            print(f"   GPU计算时间: {gpu_time:.3f} 秒")
            print(f"   CPU计算时间: {cpu_time:.3f} 秒")
            print(f"   加速比: {speedup:.1f}x")
            
            gpu_status["gpu_time"] = gpu_time
            gpu_status["cpu_time"] = cpu_time
            gpu_status["speedup"] = speedup
        except Exception as e:
            print(f"   ⚠️  GPU性能测试失败: {e}")
            gpu_status["test_error"] = str(e)
    
    return gpu_status


def generate_performance_report(results):
    """生成性能报告"""
    print("\n" + "=" * 80)
    print("📊 性能报告")
    print("=" * 80)
    
    print(f"\n⏱️  时间统计:")
    print(f"   数据预加载: {results['preload']['duration']:.1f} 秒")
    print(f"   并行回测: {results['parallel']['total_duration']:.1f} 秒")
    print(f"   平均每时间段: {results['parallel']['avg_per_period']:.1f} 秒")
    print(f"   总耗时: {results['preload']['duration'] + results['parallel']['total_duration']:.1f} 秒")
    
    print(f"\n💾 数据统计:")
    print(f"   股票数: {results['preload']['total_stocks']}")
    print(f"   数据大小: {results['preload']['data_size_mb']:.1f} MB")
    print(f"   缓存文件数: {results['preload']['cache_files']}")
    
    print(f"\n⚡ 并行处理:")
    print(f"   并行工作数: {results['parallel']['workers']}")
    print(f"   总时间段数: {results['parallel']['total_periods']}")
    print(f"   通过数: {results['parallel']['passed']}")
    print(f"   未通过数: {results['parallel']['failed']}")
    
    print(f"\n🚀 GPU加速:")
    print(f"   GPU可用: {'✅ 是' if results['gpu']['available'] else '❌ 否'}")
    print(f"   加速启用: {'✅ 是' if results['gpu']['enabled'] else '❌ 否'}")
    if results['gpu'].get('speedup'):
        print(f"   加速比: {results['gpu']['speedup']:.1f}x")
    
    # 保存报告
    report_path = Path("output/advisor_v4/batch_validation") / f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 性能报告已保存: {report_path}")


def main():
    """主函数"""
    print("=" * 80)
    print("🧪 批量回测性能测试")
    print("=" * 80)
    print(f"   测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 打印系统信息
    print_system_info()
    
    # 测试参数（使用较短的时间段，快速验证）
    start_date = "2024-07-01"
    end_date = "2024-12-31"
    window_months = 3  # 3个月窗口
    step_months = 1    # 每月滚动
    
    print("📋 测试参数:")
    print(f"   时间范围: {start_date} ~ {end_date}")
    print(f"   窗口大小: {window_months} 个月")
    print(f"   滚动步长: {step_months} 个月")
    print()
    
    # 创建验证器
    validator = BatchBacktestValidator(
        cache_dir="data/cache",
        output_dir="output/advisor_v4/batch_validation",
        use_gpu=True,
        max_workers=3,
        verbose=True
    )
    
    # 设置验证标准（宽松一些，确保能通过）
    validator.set_criteria(ValidationCriteria(
        min_sharpe=0.3,
        max_drawdown=0.30,
        min_win_rate=0.30,
        min_total_return=-0.15,
        min_trades=3
    ))
    
    results = {}
    
    # 测试1: 数据预加载
    preload_result = test_data_preloading(validator, start_date, end_date)
    results["preload"] = preload_result
    
    # 生成测试时间段
    periods = validator.generate_rolling_periods(
        start_date=start_date,
        end_date=end_date,
        window_months=window_months,
        step_months=step_months
    )
    
    print(f"\n📅 生成时间段: {len(periods)} 个")
    for i, period in enumerate(periods[:3]):  # 只显示前3个
        print(f"   [{i+1}] {period.label}: {period.start_date} ~ {period.end_date}")
    if len(periods) > 3:
        print(f"   ... 还有 {len(periods) - 3} 个时间段")
    
    # 测试2: 并行处理
    parallel_result = test_parallel_processing(validator, periods)
    parallel_result["workers"] = validator.max_workers
    results["parallel"] = parallel_result
    
    # 测试3: GPU加速
    gpu_result = test_gpu_acceleration(validator)
    results["gpu"] = gpu_result
    
    # 生成性能报告
    generate_performance_report(results)
    
    print("\n" + "=" * 80)
    print("✅ 性能测试完成!")
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断测试")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
