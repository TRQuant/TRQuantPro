#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Investment Advisor V4.0 验证脚本

功能：
1. 在测试集上验证模型泛化能力
2. 检测过拟合情况
3. 生成详细验证报告

使用方法:
    python scripts/validate_advisor_v4.py --test-start 2025-09-30 --test-end 2025-12-31
"""

import sys
from pathlib import Path

# 设置项目根目录
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """主入口"""
    parser = argparse.ArgumentParser(description='Investment Advisor V4.0 验证脚本')
    parser.add_argument('--test-start', type=str, default='2025-09-30',
                       help='测试集开始日期')
    parser.add_argument('--test-end', type=str, default='2025-12-31',
                       help='测试集结束日期')
    parser.add_argument('--model-path', type=str, default='models/xgb_high_return_v4.pkl',
                       help='模型路径')
    parser.add_argument('--feature-pipeline-path', type=str, default='models/feature_pipeline_v4.pkl',
                       help='特征流水线路径')
    parser.add_argument('--training-data-path', type=str, default='results/training_data_v4.csv',
                       help='训练数据路径')
    parser.add_argument('--output-dir', type=str, default='results/validation',
                       help='输出目录')
    parser.add_argument('--verbose', action='store_true', default=True,
                       help='详细输出')
    
    args = parser.parse_args()
    
    print(f"\n{'='*70}")
    print(f"  Investment Advisor V4.0 - 模型验证")
    print(f"  测试期: {args.test_start} ~ {args.test_end}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 导入模块
    from core.advisor_v4.xgboost_predictor import XGBoostPredictor
    from core.advisor_v4.feature_pipeline import FeaturePipeline
    from core.advisor_v4.cross_validator import OverfittingDetector
    
    # 加载模型
    print("[Step 1] 加载模型...")
    predictor = XGBoostPredictor(model_path=args.model_path)
    try:
        predictor.load()
        print(f"  ✅ 模型加载成功: {args.model_path}")
    except Exception as e:
        print(f"  ❌ 模型加载失败: {e}")
        return
    
    # 加载特征流水线（如果存在）
    feature_pipeline = None
    if Path(args.feature_pipeline_path).exists():
        print("\n[Step 2] 加载特征流水线...")
        try:
            feature_pipeline = FeaturePipeline()
            feature_pipeline.load(args.feature_pipeline_path)
            print(f"  ✅ 特征流水线加载成功")
            print(f"  选中特征: {feature_pipeline.get_selected_features()}")
        except Exception as e:
            print(f"  ⚠️ 特征流水线加载失败: {e}")
    
    # 加载训练数据
    print("\n[Step 3] 加载验证数据...")
    try:
        training_df = pd.read_csv(args.training_data_path)
        print(f"  总数据: {len(training_df)} 条")
    except Exception as e:
        print(f"  ❌ 训练数据加载失败: {e}")
        return
    
    # 划分数据集
    train_df = training_df[training_df['prediction_date'] < '2025-07-01']
    val_df = training_df[
        (training_df['prediction_date'] >= '2025-07-01') & 
        (training_df['prediction_date'] < args.test_start)
    ]
    test_df = training_df[
        (training_df['prediction_date'] >= args.test_start) & 
        (training_df['prediction_date'] <= args.test_end)
    ]
    
    print(f"  训练集: {len(train_df)} 条 (< 2025-07-01)")
    print(f"  验证集: {len(val_df)} 条 (2025-07-01 ~ {args.test_start})")
    print(f"  测试集: {len(test_df)} 条 ({args.test_start} ~ {args.test_end})")
    
    if len(test_df) == 0:
        print(f"  ⚠️ 测试集为空，可能需要扩展训练数据")
        # 尝试使用验证集作为测试集
        if len(val_df) > 0:
            print(f"  使用验证集作为测试集...")
            test_df = val_df
    
    # 应用特征流水线（如果存在）
    if feature_pipeline is not None and feature_pipeline.fitted:
        print("\n[Step 4] 应用特征流水线...")
        try:
            feature_cols = [c for c in XGBoostPredictor.FEATURE_COLUMNS if c in test_df.columns]
            X_test = test_df[feature_cols].copy()
            X_test_transformed = feature_pipeline.transform(X_test)
            
            # 更新测试数据
            for col in X_test_transformed.columns:
                if col in test_df.columns:
                    test_df = test_df.copy()
                    test_df[col] = X_test_transformed[col].values
            
            print(f"  ✅ 特征转换完成")
        except Exception as e:
            print(f"  ⚠️ 特征转换失败: {e}")
    
    # 评估测试集
    print("\n[Step 5] 评估测试集...")
    test_metrics = predictor.evaluate(test_df, 'label')
    
    print(f"\n{'='*50}")
    print(f"【测试集评估结果】")
    print(f"{'='*50}")
    print(f"准确率:   {test_metrics.accuracy:.1%}")
    print(f"精确率:   {test_metrics.precision:.1%}")
    print(f"召回率:   {test_metrics.recall:.1%}")
    print(f"F1分数:   {test_metrics.f1:.4f}")
    print(f"AUC:      {test_metrics.auc:.4f}")
    
    if test_metrics.confusion_matrix is not None:
        print(f"\n混淆矩阵:")
        cm = test_metrics.confusion_matrix
        print(f"  真负 TN: {cm[0][0]:5d}  |  假正 FP: {cm[0][1]:5d}")
        print(f"  假负 FN: {cm[1][0]:5d}  |  真正 TP: {cm[1][1]:5d}")
    
    # 与训练/验证集对比
    print("\n[Step 6] 过拟合检测...")
    
    train_val_metrics = predictor.get_train_val_metrics()
    
    if 'train' in train_val_metrics and 'val' in train_val_metrics:
        train_m = train_val_metrics['train']
        val_m = train_val_metrics['val']
        
        print(f"\n{'='*65}")
        print(f"{'指标':<12} {'训练集':>12} {'验证集':>12} {'测试集':>12} {'状态':>8}")
        print(f"{'='*65}")
        
        def status_emoji(train_val, val_test):
            """根据差距判断状态"""
            if train_val > 0.1 or val_test > 0.1:
                return "⚠️"
            elif train_val > 0.05 or val_test > 0.05:
                return "⚡"
            else:
                return "✅"
        
        auc_status = status_emoji(
            train_m['auc'] - val_m['auc'],
            val_m['auc'] - test_metrics.auc
        )
        
        print(f"{'准确率':<12} {train_m['accuracy']:>12.1%} {val_m['accuracy']:>12.1%} {test_metrics.accuracy:>12.1%}")
        print(f"{'精确率':<12} {train_m['precision']:>12.1%} {val_m['precision']:>12.1%} {test_metrics.precision:>12.1%}")
        print(f"{'召回率':<12} {train_m['recall']:>12.1%} {val_m['recall']:>12.1%} {test_metrics.recall:>12.1%}")
        print(f"{'F1分数':<12} {train_m['f1']:>12.4f} {val_m['f1']:>12.4f} {test_metrics.f1:>12.4f}")
        print(f"{'AUC':<12} {train_m['auc']:>12.4f} {val_m['auc']:>12.4f} {test_metrics.auc:>12.4f} {auc_status:>8}")
        print(f"{'='*65}")
        
        # 计算过拟合指标
        train_val_gap = train_m['auc'] - val_m['auc']
        val_test_gap = val_m['auc'] - test_metrics.auc
        train_test_gap = train_m['auc'] - test_metrics.auc
        
        print(f"\n过拟合指标:")
        print(f"  训练-验证 AUC差距: {train_val_gap:+.4f} {'⚠️ 过拟合' if train_val_gap > 0.1 else '✅ 正常'}")
        print(f"  验证-测试 AUC差距: {val_test_gap:+.4f} {'⚠️ 泛化下降' if val_test_gap > 0.1 else '✅ 正常'}")
        print(f"  训练-测试 AUC差距: {train_test_gap:+.4f} {'⚠️ 严重过拟合' if train_test_gap > 0.15 else '✅ 正常'}")
    
    # 过拟合检测报告
    detector = OverfittingDetector()
    report = None
    
    if 'train' in train_val_metrics:
        train_dict = {
            'auc': train_val_metrics['train']['auc'],
            'precision': train_val_metrics['train']['precision'],
        }
        test_dict = {
            'auc': test_metrics.auc,
            'precision': test_metrics.precision,
        }
        
        report = detector.detect(train_dict, test_dict, predictor.feature_importance)
        
        print(f"\n{'='*50}")
        print(f"【过拟合检测报告】")
        print(f"{'='*50}")
        
        if report['is_overfitting']:
            print(f"⚠️ 检测到过拟合风险 (严重程度: {report['severity']})")
            for warning in report['warnings']:
                print(f"   - {warning}")
            print(f"\n建议: {report['recommendation']}")
        else:
            print(f"✅ 模型泛化能力良好")
    
    # 特征重要性分析
    print(f"\n{'='*50}")
    print(f"【特征重要性 TOP 10】")
    print(f"{'='*50}")
    
    top_features = predictor.get_top_features(10)
    total_importance = sum(imp for _, imp in top_features)
    
    for i, (feat, imp) in enumerate(top_features, 1):
        bar = "█" * int(imp / max(top_features[0][1], 0.01) * 20)
        print(f"  {i:2d}. {feat:<20} {imp:.4f} ({imp/total_importance*100:.1f}%) {bar}")
    
    # 保存验证报告
    print(f"\n[Step 7] 保存验证报告...")
    
    validation_report = {
        'timestamp': datetime.now().isoformat(),
        'test_period': f"{args.test_start} ~ {args.test_end}",
        'test_samples': len(test_df),
        'metrics': {
            'test': {
                'accuracy': float(test_metrics.accuracy),
                'precision': float(test_metrics.precision),
                'recall': float(test_metrics.recall),
                'f1': float(test_metrics.f1),
                'auc': float(test_metrics.auc),
            },
        },
        'feature_importance': dict(top_features),
        'overfitting_analysis': {
            'is_overfitting': report.get('is_overfitting', False) if report else False,
            'warnings': report.get('warnings', []) if report else [],
        },
        'feature_pipeline_used': feature_pipeline is not None,
    }
    
    if 'train' in train_val_metrics:
        validation_report['metrics']['train'] = train_val_metrics['train']
        validation_report['metrics']['val'] = train_val_metrics['val']
    
    # 转换numpy类型为Python原生类型（JSON序列化兼容）
    def convert_to_native(obj):
        """递归转换numpy类型为Python原生类型"""
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_to_native(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_native(item) for item in obj]
        else:
            return obj
    
    validation_report = convert_to_native(validation_report)
    
    report_path = output_dir / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(validation_report, f, indent=2, ensure_ascii=False)
    
    print(f"  验证报告已保存: {report_path}")
    
    # 总结
    print(f"\n{'='*70}")
    print(f"【验证总结】")
    print(f"{'='*70}")
    
    # 判断模型质量
    quality_score = 0
    quality_notes = []
    
    if test_metrics.auc >= 0.65:
        quality_score += 2
        quality_notes.append("✅ 测试集AUC良好 (≥0.65)")
    elif test_metrics.auc >= 0.55:
        quality_score += 1
        quality_notes.append("⚡ 测试集AUC一般 (0.55-0.65)")
    else:
        quality_notes.append("⚠️ 测试集AUC较低 (<0.55)")
    
    if test_metrics.precision >= 0.5:
        quality_score += 1
        quality_notes.append("✅ 精确率可接受 (≥50%)")
    else:
        quality_notes.append("⚠️ 精确率较低 (<50%)")
    
    if 'train' in train_val_metrics:
        if train_val_metrics['train']['auc'] - test_metrics.auc < 0.1:
            quality_score += 1
            quality_notes.append("✅ 训练-测试差距小，泛化能力好")
        else:
            quality_notes.append("⚠️ 训练-测试差距大，可能过拟合")
    
    for note in quality_notes:
        print(f"  {note}")
    
    overall_quality = "优秀" if quality_score >= 4 else ("良好" if quality_score >= 3 else ("一般" if quality_score >= 2 else "待优化"))
    print(f"\n  总体评价: {overall_quality} (得分: {quality_score}/4)")
    
    print(f"\n{'='*70}\n")


if __name__ == '__main__':
    main()
