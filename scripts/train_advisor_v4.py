#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
训练Advisor V4.0模型
===================

功能：
- 从历史高收益案例提取预测因子（支持GPU批量加速）
- 训练XGBoost模型
- 保存模型和特征流水线

用法:
    python scripts/train_advisor_v4.py [--use-gpu] [--batch-size 50] [--skip-extraction]
"""

import sys
from pathlib import Path
import argparse

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.advisor_v4_workflow import AdvisorV4Workflow, AdvisorV4Config


def main():
    parser = argparse.ArgumentParser(description="训练Advisor V4.0模型")
    parser.add_argument(
        '--use-gpu',
        action='store_true',
        default=True,
        help='使用GPU加速因子提取（默认启用）'
    )
    parser.add_argument(
        '--no-gpu',
        action='store_false',
        dest='use_gpu',
        help='禁用GPU加速（使用CPU）'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=50,
        help='GPU批处理大小（默认：50）'
    )
    parser.add_argument(
        '--skip-extraction',
        action='store_true',
        help='跳过因子提取（使用已有数据）'
    )
    parser.add_argument(
        '--skip-negative-sampling',
        action='store_true',
        help='跳过负样本采样'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("【Advisor V4.0 训练模式】")
    print("="*70)
    print(f"GPU加速: {'✅' if args.use_gpu else '❌'}")
    if args.use_gpu:
        print(f"批处理大小: {args.batch_size}")
    print("="*70)
    
    # 创建V4工作流（会自动初始化输出路径）
    config = AdvisorV4Config()
    workflow = AdvisorV4Workflow(config=config, verbose=True)
    
    # 如果启用GPU，确保并行提取器使用GPU
    if args.use_gpu and not args.skip_extraction:
        # 在workflow.train()中会自动使用ParallelPredictorFactorExtractor
        # 这里只是记录配置
        print(f"ℹ️  GPU批量加速将在因子提取阶段自动启用")
    
    # 如果高收益案例文件不存在，尝试从results目录复制
    from pathlib import Path
    from shutil import copy2
    
    cases_path = Path(workflow.config.high_return_cases_path)
    if not cases_path.exists():
        # 尝试从results目录查找
        results_file = Path(__file__).parent.parent / "results" / "high_return_cases_full_train.csv"
        if results_file.exists():
            print(f"📋 从results目录复制高收益案例文件...")
            cases_path.parent.mkdir(parents=True, exist_ok=True)
            copy2(results_file, cases_path)
            print(f"✅ 已复制: {cases_path}")
        else:
            print(f"⚠️ 警告: 高收益案例文件不存在: {cases_path}")
            print(f"   请先运行数据提取脚本生成高收益案例数据")
            return 1
    
    # 运行训练（自动包含数据验证、并行提取、算法验证）
    try:
        predictor = workflow.train()
        print("\n" + "="*70)
        print("【训练完成】")
        print("="*70)
        print(f"✅ 模型已保存: {workflow.config.model_path}")
        print(f"✅ 特征流水线已保存: {workflow.config.feature_pipeline_path}")
        
        # 显示过拟合检测结果
        if hasattr(workflow, 'predictor') and workflow.predictor:
            overfitting_report = workflow.predictor.detect_overfitting()
            if overfitting_report.get('is_overfitting'):
                print(f"\n⚠️ 过拟合检测: {overfitting_report.get('severity', 'unknown')} 风险")
                print(f"   建议: {overfitting_report.get('recommendation', 'N/A')}")
            else:
                print(f"\n✅ 模型泛化能力良好")
        
        return 0
    except Exception as e:
        print(f"\n❌ 训练失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
