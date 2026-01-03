#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完整系统测试"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_all():
    print("="*60)
    print("韬睿量化系统完整测试")
    print("="*60)
    
    results = []
    
    # 1. 数据接口层
    print("\n1. 测试统一数据接口层...")
    try:
        from core.data.unified_data_provider import get_data_provider
        provider = get_data_provider()
        print(f"   ✅ 通过 - 缓存目录: {provider.cache_dir}")
        results.append(("数据接口层", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("数据接口层", False))
    
    # 2. 快速回测引擎
    print("\n2. 测试快速回测引擎...")
    try:
        from core.backtest.fast_backtest_engine import BacktestConfig, FastBacktestEngine
        config = BacktestConfig(start_date="2025-01-01", end_date="2025-01-31")
        engine = FastBacktestEngine(config)
        print(f"   ✅ 通过 - 初始资金: {config.initial_capital}")
        results.append(("快速回测引擎", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("快速回测引擎", False))
    
    # 3. 批量回测管理器
    print("\n3. 测试批量回测管理器...")
    try:
        from core.backtest.batch_backtest_manager import BatchBacktestManager
        manager = BatchBacktestManager()
        print(f"   ✅ 通过 - 最大工作线程: {manager.max_workers}")
        results.append(("批量回测管理器", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("批量回测管理器", False))
    
    # 4. 工作流状态管理器
    print("\n4. 测试工作流状态管理器...")
    try:
        from core.workflow.state_manager import get_state_manager
        mgr = get_state_manager()
        wf = mgr.create_workflow("测试")
        print(f"   ✅ 通过 - 工作流ID: {wf.workflow_id}")
        results.append(("状态管理器", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("状态管理器", False))
    
    # 5. 策略进化框架
    print("\n5. 测试策略进化框架...")
    try:
        from core.evolution.strategy_evolver import StrategyEvolver, EvolutionConfig
        config = EvolutionConfig(population_size=5, generations=2)
        evolver = StrategyEvolver(config)
        evolver.initialize_population()
        print(f"   ✅ 通过 - 种群大小: {len(evolver.population)}")
        results.append(("策略进化框架", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("策略进化框架", False))
    
    # 6. 策略模板库
    print("\n6. 测试策略模板库...")
    try:
        from core.templates.strategy_templates import list_templates, get_template
        templates = list_templates()
        mom = get_template("momentum")
        print(f"   ✅ 通过 - 模板数: {len(templates)}, 动量模板参数: {len(mom.get_default_params())}")
        results.append(("策略模板库", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("策略模板库", False))
    
    # 7. 可视化报告
    print("\n7. 测试可视化报告生成...")
    try:
        from core.visualization.report_generator import ReportGenerator
        gen = ReportGenerator()
        print(f"   ✅ 通过 - 输出目录: {gen.output_dir}")
        results.append(("可视化报告", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("可视化报告", False))
    
    # 8. 系统集成层
    print("\n8. 测试系统集成层...")
    try:
        from core.system_integration import get_system
        system = get_system()
        status = system.get_system_status()
        print(f"   ✅ 通过 - 组件状态: {status}")
        results.append(("系统集成层", True))
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        results.append(("系统集成层", False))
    
    # 汇总
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    passed = sum(1 for _, r in results if r)
    for name, result in results:
        print(f"  {name}: {'✅ 通过' if result else '❌ 失败'}")
    print(f"\n总计: {passed}/{len(results)} 通过")
    print("="*60)
    
    return passed == len(results)

if __name__ == "__main__":
    success = test_all()
    sys.exit(0 if success else 1)
