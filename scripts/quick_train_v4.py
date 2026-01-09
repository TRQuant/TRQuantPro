#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速训练V4模型 - 使用已有的历史案例数据
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    print(f"\n{'='*60}")
    print(f"  Investment Advisor V4.0 - 快速训练")
    print(f"{'='*60}\n")
    
    # 加载历史高收益案例
    cases_file = 'results/high_return_cases_full_train.csv'
    print(f"加载历史案例: {cases_file}")
    
    try:
        cases_df = pd.read_csv(cases_file)
        print(f"加载成功: {len(cases_df)} 条案例")
    except FileNotFoundError:
        print(f"文件不存在，尝试其他路径...")
        cases_file = 'results/high_return_cases_10pct.csv'
        try:
            cases_df = pd.read_csv(cases_file)
            print(f"加载成功: {len(cases_df)} 条案例")
        except:
            print("无历史案例数据，使用模拟数据训练")
            cases_df = None
    
    if cases_df is not None:
        # 准备训练数据
        print("\n准备训练数据...")
        
        # 特征列
        feature_cols = [
            'market_cap', 'roe', 'growth', 'revenue_growth',
            'momentum_5d', 'momentum_20d', 'rel_position', 'turnover',
        ]
        
        # 检查可用列
        available_cols = [c for c in feature_cols if c in cases_df.columns]
        print(f"可用特征: {available_cols}")
        
        # 构建特征矩阵
        X = cases_df[available_cols].copy()
        
        # 处理缺失值
        X = X.fillna(X.median())
        X = X.replace([np.inf, -np.inf], 0)
        
        # 标签：所有历史案例都是正样本（>=10%收益）
        y_positive = np.ones(len(X))
        
        # 生成负样本（使用类似分布但标签为0）
        n_negative = min(len(X) * 2, 2000)
        
        # 对每个特征添加随机扰动生成负样本
        X_negative = pd.DataFrame()
        for col in available_cols:
            mean = X[col].mean()
            std = X[col].std()
            # 负样本特征偏离正样本
            X_negative[col] = np.random.normal(mean * 0.7, std * 1.5, n_negative)
        
        y_negative = np.zeros(n_negative)
        
        # 合并
        X_train = pd.concat([X, X_negative], ignore_index=True)
        y_train = np.concatenate([y_positive, y_negative])
        
        # 打乱
        shuffle_idx = np.random.permutation(len(X_train))
        X_train = X_train.iloc[shuffle_idx]
        y_train = y_train[shuffle_idx]
        
        print(f"训练数据: {len(X_train)} 样本")
        print(f"正样本: {(y_train == 1).sum()}")
        print(f"负样本: {(y_train == 0).sum()}")
    else:
        # 使用模拟数据
        print("\n生成模拟训练数据...")
        np.random.seed(42)
        n_samples = 2000
        
        feature_cols = [
            'market_cap', 'roe', 'growth', 'momentum_5d', 
            'momentum_20d', 'rel_position', 'turnover',
        ]
        
        X_train = pd.DataFrame({
            'market_cap': np.random.uniform(30, 300, n_samples),
            'roe': np.random.uniform(-10, 30, n_samples),
            'growth': np.random.uniform(-50, 200, n_samples),
            'momentum_5d': np.random.uniform(-10, 20, n_samples),
            'momentum_20d': np.random.uniform(-20, 40, n_samples),
            'rel_position': np.random.uniform(0, 100, n_samples),
            'turnover': np.random.uniform(1, 15, n_samples),
        })
        
        y_train = np.random.randint(0, 2, n_samples)
        available_cols = feature_cols
    
    # 训练XGBoost模型
    print("\n训练XGBoost模型...")
    
    from core.advisor_v4.xgboost_predictor import XGBoostPredictor
    
    # 添加label列
    train_df = X_train.copy()
    train_df['label'] = y_train
    train_df['code'] = [f'stock_{i}' for i in range(len(train_df))]
    
    # 划分训练/验证集
    from sklearn.model_selection import train_test_split
    train_split, val_split = train_test_split(train_df, test_size=0.2, random_state=42)
    
    # 训练
    predictor = XGBoostPredictor(
        model_path='models/xgb_high_return_v4.pkl',
        verbose=True
    )
    
    # 更新特征列
    predictor.FEATURE_COLUMNS = available_cols
    
    predictor.train(train_split, val_split)
    predictor.save()
    
    print(f"\n✅ 模型训练完成!")
    print(f"模型已保存至: models/xgb_high_return_v4.pkl")
    
    # 显示特征重要性
    print(f"\n【特征重要性】")
    for feat, imp in predictor.get_top_features(10):
        print(f"  {feat}: {imp:.4f}")


if __name__ == '__main__':
    main()
