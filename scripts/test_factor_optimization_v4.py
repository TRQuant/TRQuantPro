#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
因子优化系统测试脚本
====================

快速验证因子优化系统是否正常工作
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.advisor_v4_workflow import AdvisorV4Workflow, AdvisorV4Config
from core.advisor_v4.factor_optimizer import FactorOptimizationConfig


def test_factor_optimization():
    """测试因子优化系统"""
    print("="*70)
    print("【因子优化系统测试】")
    print("="*70)
    
    # 创建V4工作流
    config = AdvisorV4Config()
    workflow = AdvisorV4Workflow(config=config, verbose=True)
    
    # 创建优化配置（快速测试模式）
    opt_config = FactorOptimizationConfig(
        enable_factor_selection=True,
        enable_weight_optimization=True,
        enable_fusion_optimization=True,
        optimization_method='grid',
        max_iterations=2,  # 快速测试：只迭代2次
        early_stop_patience=1,
        min_factors=3,
        max_factors=5,  # 快速测试：限制因子数量
    )
    
    # 运行优化（使用较短的时间范围）
    try:
        result = workflow.optimize_factors(
            start_date="2024-09-01",
            end_date="2024-12-31",
            config=opt_config,
        )
        
        if result and result.best_result:
            print("\n" + "="*70)
            print("【测试通过】")
            print("="*70)
            print(f"✅ 因子优化系统运行正常")
            print(f"   最优因子组合: {len(result.best_result.factor_selection)} 个因子")
            print(f"   综合得分: {result.best_result.multi_objective_score:.2f}")
            print(f"   优化耗时: {result.optimization_time_seconds:.1f} 秒")
            return True
        else:
            print("\n❌ 测试失败：未获得优化结果")
            return False
    
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_factor_optimization()
    sys.exit(0 if success else 1)
