#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统构建测试脚本
================
验证所有新构建的模块是否正常工作
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_data_provider():
    """测试数据提供者"""
    print("\n1. 测试统一数据接口层...")
    try:
        from core.data.unified_data_provider import get_data_provider, DataRequest
        provider = get_data_provider()
        print(f"   ✅ 数据提供者已初始化")
        print(f"   缓存目录: {provider.cache_dir}")
        return True
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        return False

def test_fast_backtest():
    """测试快速回测引擎"""
    print("\n2. 测试快速回测引擎...")
    try:
        from core.backtest.fast_backtest_engine import FastBacktestEngine, BacktestConfig, SignalGenerator
        config = BacktestConfig(start_date="2025-01-01", end_date="2025-01-31")
        engine = FastBacktestEngine(config)
        print(f"   ✅ 快速回测引擎已初始化")
        print(f"   初始资金: {config.initial_capital}")
        return True
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        return False

def test_batch_manager():
    """测试批量回测管理器"""
    print("\n3. 测试批量回测管理器...")
    try:
        from core.backtest.batch_backtest_manager import BatchBacktestManager, StrategyConfig
        manager = BatchBacktestManager()
        print(f"   ✅ 批量回测管理器已初始化")
        print(f"   最大工作线程: {manager.max_workers}")
        return True
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        return False

def test_state_manager():
    """测试工作流状态管理器"""
    print("\n4. 测试工作流状态管理器...")
    try:
        from core.workflow.state_manager import get_state_manager, WorkflowStatus
        manager = get_state_manager()
        workflow = manager.create_workflow("测试工作流")
        print(f"   ✅ 状态管理器已初始化")
        print(f"   工作流ID: {workflow.workflow_id}")
        print(f"   步骤数: {workflow.total_steps}")
        return True
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        return False

def test_strategy_evolver():
    """测试策略进化框架"""
    print("\n5. 测试策略进化框架...")
    try:
        from core.evolution.strategy_evolver import StrategyEvolver, EvolutionConfig
        config = EvolutionConfig(population_size=5, generations=2)
        evolver = StrategyEvolver(config)
        evolver.initialize_population("momentum")
        print(f"   ✅ 策略进化框架已初始化")
        print(f"   种群大小: {len(evolver.population)}")
        return True
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        return False

def test_system_integration():
    """测试系统集成层"""
    print("\n6. 测试系统集成层...")
    try:
        from core.system_integration import get_system
        system = get_system()
        status = system.get_system_status()
        print(f"   ✅ 系统集成层已初始化")
        for k, v in status.items():
            if k != "data_stats":
                print(f"   {k}: {v}")
        return True
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        return False

def main():
    print("="*60)
    print("韬睿量化系统构建测试")
    print("="*60)
    
    results = []
    results.append(("统一数据接口层", test_data_provider()))
    results.append(("快速回测引擎", test_fast_backtest()))
    results.append(("批量回测管理器", test_batch_manager()))
    results.append(("工作流状态管理器", test_state_manager()))
    results.append(("策略进化框架", test_strategy_evolver()))
    results.append(("系统集成层", test_system_integration()))
    
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
