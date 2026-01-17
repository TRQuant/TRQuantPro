#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Investment Advisor V4.0 - 模型进化脚本

功能：
1. 加载训练数据
2. 执行递归进化优化
3. 保存最佳模型和报告
4. 支持断点续传

目标：AUC >= 0.70

用法：
    ./venv/bin/python scripts/evolve_advisor_v4.py --target-auc 0.70 --max-iterations 20
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

from core.advisor_v4.model_evolver import ModelEvolver, EvolutionConfig, EvolutionResult
from core.advisor_v4.xgboost_predictor import XGBoostPredictor


def load_training_data(data_path: str = None, 
                       val_ratio: float = 0.15,
                       test_ratio: float = 0.15) -> tuple:
    """加载并划分训练数据
    
    Args:
        data_path: 数据文件路径
        val_ratio: 验证集比例
        test_ratio: 测试集比例
        
    Returns:
        (train_df, val_df, test_df)
    """
    # 默认数据路径
    if data_path is None:
        data_path = project_root / 'results' / 'training_data_v4.csv'
    
    data_path = Path(data_path)
    
    if not data_path.exists():
        logger.warning(f"数据文件不存在: {data_path}")
        logger.info("尝试加载预测因子文件...")
        
        # 尝试加载预测因子文件
        predictive_path = project_root / 'results' / 'predictive_features.csv'
        if predictive_path.exists():
            df = pd.read_csv(predictive_path)
            logger.info(f"已加载预测因子: {len(df)} 条")
        else:
            logger.error("无可用数据文件，请先运行训练数据生成")
            sys.exit(1)
    else:
        df = pd.read_csv(data_path)
        logger.info(f"已加载训练数据: {len(df)} 条")
    
    # 检查必要列
    if 'label' not in df.columns:
        # 尝试从其他列生成label
        if 'return_5d' in df.columns:
            df['label'] = (df['return_5d'] >= 0.10).astype(int)
            logger.info(f"从return_5d生成label（10%阈值）")
        elif 'target_return' in df.columns:
            df['label'] = (df['target_return'] >= 0.10).astype(int)
            logger.info(f"从target_return生成label")
        else:
            logger.error("无法找到或生成label列")
            sys.exit(1)
    
    # 按时间排序
    if 'prediction_date' in df.columns:
        df = df.sort_values('prediction_date')
    elif 'target_date' in df.columns:
        df = df.sort_values('target_date')
        df = df.rename(columns={'target_date': 'prediction_date'})
    
    # 划分数据集
    n = len(df)
    train_end = int(n * (1 - val_ratio - test_ratio))
    val_end = int(n * (1 - test_ratio))
    
    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()
    
    logger.info(f"数据划分: 训练={len(train_df)}, 验证={len(val_df)}, 测试={len(test_df)}")
    logger.info(f"正样本比例: 训练={train_df['label'].mean():.2%}, 验证={val_df['label'].mean():.2%}, 测试={test_df['label'].mean():.2%}")
    
    return train_df, val_df, test_df


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """准备特征
    
    确保所有必要特征存在，填充缺失值
    """
    result_df = df.copy()
    
    # XGBoost使用的特征列
    feature_cols = XGBoostPredictor.FEATURE_COLUMNS
    
    # 检查缺失特征
    missing_cols = [c for c in feature_cols if c not in result_df.columns]
    
    if missing_cols:
        logger.warning(f"缺失特征: {missing_cols}")
        
        # 尝试从其他列映射
        mapping = {
            'momentum_5d': 'price_change_5d',
            'momentum_10d': 'price_change_10d',
            'momentum_20d': 'price_change_20d',
            'market_cap': 'circulating_market_cap',
            'roe': 'roe_ttm',
            'growth': 'net_profit_growth',
            'volume_ratio': 'volume_ratio_5d',
            'fin_change': 'financing_balance_change',
            'turnover_rate': 'turnover_rate_avg',
            'concept_count': 'num_concepts',
            'market_trend': 'market_score',
        }
        
        for target, source in mapping.items():
            if target in missing_cols and source in result_df.columns:
                result_df[target] = result_df[source]
                missing_cols.remove(target)
        
        # 对仍然缺失的特征填0
        for col in missing_cols:
            result_df[col] = 0
            logger.info(f"  填充特征 {col} = 0")
    
    # 填充NaN
    for col in feature_cols:
        if col in result_df.columns:
            if result_df[col].isna().any():
                median_val = result_df[col].median()
                if pd.isna(median_val):
                    median_val = 0
                result_df[col] = result_df[col].fillna(median_val)
    
    return result_df


def run_evolution(args) -> EvolutionResult:
    """运行进化优化"""
    
    print("\n" + "="*70)
    print("Investment Advisor V4.0 - 模型进化优化")
    print("="*70)
    print(f"目标 AUC: {args.target_auc}")
    print(f"最大迭代: {args.max_iterations}")
    print(f"早停耐心: {args.patience}")
    print("="*70 + "\n")
    
    # 1. 加载数据
    logger.info("步骤1: 加载训练数据...")
    train_df, val_df, test_df = load_training_data(
        args.data_path,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio
    )
    
    # 2. 准备特征
    logger.info("步骤2: 准备特征...")
    train_df = prepare_features(train_df)
    val_df = prepare_features(val_df)
    test_df = prepare_features(test_df)
    
    # 3. 创建进化器
    logger.info("步骤3: 创建模型进化器...")
    config = EvolutionConfig(
        target_auc=args.target_auc,
        max_iterations=args.max_iterations,
        patience=args.patience,
        min_improvement=args.min_improvement,
    )
    
    evolver = ModelEvolver(config, verbose=True)
    
    # 4. 执行进化
    logger.info("步骤4: 开始进化优化...")
    start_time = datetime.now()
    
    result = evolver.evolve(train_df, val_df, test_df)
    
    duration = (datetime.now() - start_time).total_seconds()
    
    # 5. 输出结果
    print("\n" + "="*70)
    print("进化结果")
    print("="*70)
    
    if result.success:
        print(f"✅ 成功达到目标!")
    else:
        print(f"⚠️ 未达到目标 (原因: {result.reason})")
    
    print(f"最佳AUC: {result.best_auc:.4f}")
    print(f"达到迭代: {result.best_iteration}")
    print(f"总迭代: {result.total_iterations}")
    print(f"耗时: {duration:.1f}秒")
    print(f"模型路径: {result.best_model_path}")
    print("="*70 + "\n")
    
    # 6. 保存报告
    report_path = evolver.save_report(result)
    
    # 7. 打印进化历史
    if args.show_history:
        print("\n进化历史:")
        print("-"*60)
        for item in result.history:
            print(f"  迭代{item.iteration}: AUC={item.val_auc:.4f} ({item.improvement:+.4f}), "
                  f"策略={item.strategy_name}")
        print("-"*60)
    
    return result


def run_quick_test(args):
    """快速测试模式"""
    print("\n快速测试模式...")
    
    # 创建模拟数据
    np.random.seed(42)
    n_samples = 500
    
    # 创建有规律的数据
    X = np.random.randn(n_samples, 14)
    y = (X[:, 0] + 0.5 * X[:, 1] - 0.3 * X[:, 2] + np.random.randn(n_samples) * 0.5 > 0).astype(int)
    
    df = pd.DataFrame(X, columns=[
        'market_cap', 'roe', 'growth', 'momentum_5d', 'momentum_10d', 
        'momentum_20d', 'rel_strength', 'rsi', 'volume_ratio', 'fin_change',
        'turnover_rate', 'on_billboard', 'concept_count', 'market_trend'
    ])
    df['label'] = y
    df['code'] = [f'stock_{i}' for i in range(n_samples)]
    df['prediction_date'] = pd.date_range('2024-01-01', periods=n_samples, freq='D').strftime('%Y-%m-%d').tolist()
    
    # 划分数据
    train_df = df.iloc[:350]
    val_df = df.iloc[350:425]
    test_df = df.iloc[425:]
    
    print(f"模拟数据: 训练={len(train_df)}, 验证={len(val_df)}, 测试={len(test_df)}")
    
    # 创建进化器
    config = EvolutionConfig(
        target_auc=0.65,  # 较低的目标用于测试
        max_iterations=5,
        patience=2,
    )
    
    evolver = ModelEvolver(config, verbose=True)
    
    # 运行进化
    result = evolver.evolve(train_df, val_df, test_df)
    
    print(f"\n测试结果: success={result.success}, best_auc={result.best_auc:.4f}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Investment Advisor V4.0 - 模型进化优化',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 默认参数运行
  ./venv/bin/python scripts/evolve_advisor_v4.py

  # 指定目标和迭代次数
  ./venv/bin/python scripts/evolve_advisor_v4.py --target-auc 0.70 --max-iterations 30

  # 快速测试模式
  ./venv/bin/python scripts/evolve_advisor_v4.py --test

  # 使用指定数据文件
  ./venv/bin/python scripts/evolve_advisor_v4.py --data-path results/training_data_v4.csv
        """
    )
    
    # 进化参数
    parser.add_argument('--target-auc', type=float, default=0.70,
                        help='目标AUC (默认: 0.70)')
    parser.add_argument('--max-iterations', type=int, default=20,
                        help='最大迭代次数 (默认: 20)')
    parser.add_argument('--patience', type=int, default=5,
                        help='早停耐心值 (默认: 5)')
    parser.add_argument('--min-improvement', type=float, default=0.005,
                        help='最小改进阈值 (默认: 0.005)')
    
    # 数据参数
    parser.add_argument('--data-path', type=str, default=None,
                        help='训练数据路径')
    parser.add_argument('--val-ratio', type=float, default=0.15,
                        help='验证集比例 (默认: 0.15)')
    parser.add_argument('--test-ratio', type=float, default=0.15,
                        help='测试集比例 (默认: 0.15)')
    
    # 其他参数
    parser.add_argument('--show-history', action='store_true', default=True,
                        help='显示进化历史')
    parser.add_argument('--test', action='store_true',
                        help='快速测试模式（使用模拟数据）')
    
    args = parser.parse_args()
    
    try:
        if args.test:
            result = run_quick_test(args)
        else:
            result = run_evolution(args)
        
        # 返回码
        if result.success:
            sys.exit(0)
        else:
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        sys.exit(130)
    
    except Exception as e:
        logger.exception(f"进化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
