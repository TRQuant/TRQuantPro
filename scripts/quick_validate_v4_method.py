#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
V4.0方法快速验证脚本

目标：3分钟内验证方法可行性
步骤：
1. 快速数据检查（30秒）
2. 小样本训练验证（60秒）
3. 逻辑正确性检查（30秒）
4. 性能基线建立（60秒）

总耗时：<3分钟
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("V4.0方法快速验证")
print("="*70)

# ============================================================
# 步骤1: 快速数据检查（30秒）
# ============================================================
print("\n[步骤1] 数据质量检查（30秒）...")
start = datetime.now()

# 检查可用数据文件
data_files = {
    'predictive_features': 'results/predictive_features.csv',
    'training_data_v4': 'results/training_data_v4.csv',
    'negative_samples': 'results/negative_samples_extracted.csv',
}

available_files = {}
for name, path in data_files.items():
    if Path(path).exists():
        df = pd.read_csv(path)
        available_files[name] = {
            'path': path,
            'rows': len(df),
            'columns': list(df.columns),
            'label_col': 'label' if 'label' in df.columns else None,
        }
        print(f"  ✓ {name}: {len(df)} 行, {len(df.columns)} 列")

if not available_files:
    print("  ✗ 无可用数据文件")
    sys.exit(1)

# 检查特征完整性
print("\n  特征完整性检查:")
required_features = ['market_cap', 'roe', 'momentum_5d', 'momentum_20d']
for name, info in available_files.items():
    df = pd.read_csv(info['path'])
    missing = [f for f in required_features if f not in df.columns]
    if missing:
        print(f"    {name}: 缺失 {missing}")
    else:
        print(f"    {name}: ✓ 基础特征完整")

elapsed = (datetime.now() - start).total_seconds()
print(f"  ✓ 完成 ({elapsed:.1f}秒)")

# ============================================================
# 步骤2: 小样本训练验证（60秒）
# ============================================================
print("\n[步骤2] 小样本训练验证（60秒）...")
start = datetime.now()

# 选择最佳数据源
best_source = None
best_score = 0

for name, info in available_files.items():
    if info['label_col'] is None:
        continue
    
    df = pd.read_csv(info['path'])
    
    # 检查是否有正负样本
    if 'label' not in df.columns:
        continue
    
    pos_count = df['label'].sum() if df['label'].dtype in [int, bool] else 0
    neg_count = len(df) - pos_count
    
    if pos_count > 10 and neg_count > 10:
        score = min(pos_count, neg_count)
        if score > best_score:
            best_score = score
            best_source = (name, info)

if best_source is None:
    print("  ✗ 无有效训练数据（需要正负样本）")
    sys.exit(1)

name, info = best_source
print(f"  使用数据源: {name}")

# 加载数据
df = pd.read_csv(info['path'])

# 快速采样（最多500条）
np.random.seed(42)
if len(df) > 500:
    df = df.sample(n=500, random_state=42)
    print(f"  采样: {len(df)} 条")

# 准备特征
feature_cols = ['market_cap', 'roe', 'momentum_5d', 'momentum_20d']
available_features = [f for f in feature_cols if f in df.columns]

if len(available_features) < 2:
    print(f"  ✗ 可用特征太少: {available_features}")
    sys.exit(1)

print(f"  使用特征: {available_features}")

# 准备数据
X = df[available_features].fillna(0).replace([np.inf, -np.inf], 0).values
y = df['label'].values

# 简单划分
split_idx = int(len(X) * 0.7)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

print(f"  训练集: {len(X_train)} (正:{y_train.sum()}, 负:{len(y_train)-y_train.sum()})")
print(f"  测试集: {len(X_test)} (正:{y_test.sum()}, 负:{len(X_test)-y_test.sum()})")

# 快速训练
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = XGBClassifier(
    n_estimators=50,  # 快速训练
    max_depth=3,
    learning_rate=0.1,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss',
    verbose=False
)

model.fit(X_train_scaled, y_train)

# 评估
train_proba = model.predict_proba(X_train_scaled)[:, 1]
test_proba = model.predict_proba(X_test_scaled)[:, 1]

train_auc = roc_auc_score(y_train, train_proba) if len(np.unique(y_train)) > 1 else 0.5
test_auc = roc_auc_score(y_test, test_proba) if len(np.unique(y_test)) > 1 else 0.5

print(f"\n  训练结果:")
print(f"    训练AUC: {train_auc:.4f}")
print(f"    测试AUC: {test_auc:.4f}")
print(f"    AUC差距: {train_auc - test_auc:.4f}")

if test_auc > 0.55:
    print(f"  ✓ 模型有预测能力 (AUC > 0.55)")
elif test_auc > 0.50:
    print(f"  ⚠️ 模型预测能力弱 (AUC ≈ 0.50)")
else:
    print(f"  ✗ 模型无预测能力 (AUC < 0.50)")

elapsed = (datetime.now() - start).total_seconds()
print(f"  ✓ 完成 ({elapsed:.1f}秒)")

# ============================================================
# 步骤3: 逻辑正确性检查（30秒）
# ============================================================
print("\n[步骤3] 逻辑正确性检查（30秒）...")
start = datetime.now()

# 检查数据泄露
print("  检查数据泄露:")
leakage_checks = []

# 检查1: 特征分布
if len(available_features) > 0:
    pos_mask = y == 1
    neg_mask = y == 0
    
    for feat in available_features:
        if feat in df.columns:
            pos_mean = df.loc[pos_mask, feat].mean()
            neg_mean = df.loc[neg_mask, feat].mean()
            pos_std = df.loc[pos_mask, feat].std()
            
            if pos_std > 0:
                diff = abs(pos_mean - neg_mean) / pos_std
                if diff > 5:  # 差异过大
                    leakage_checks.append(f"    ⚠️ {feat}: 正负样本差异过大 ({diff:.2f}倍标准差)")
                else:
                    leakage_checks.append(f"    ✓ {feat}: 分布正常 (差异={diff:.2f}倍标准差)")

if leakage_checks:
    for check in leakage_checks[:5]:  # 只显示前5个
        print(check)

# 检查2: 时间顺序
if 'prediction_date' in df.columns or 'date' in df.columns:
    date_col = 'prediction_date' if 'prediction_date' in df.columns else 'date'
    dates = pd.to_datetime(df[date_col])
    is_sorted = dates.is_monotonic_increasing
    print(f"  时间顺序: {'✓ 已排序' if is_sorted else '⚠️ 未排序'}")

# 检查3: 特征有效性
print("  特征有效性:")
for feat, imp in zip(available_features, model.feature_importances_):
    status = '✓' if imp > 0.1 else '⚠️'
    print(f"    {feat}: {imp:.4f} {status}")

elapsed = (datetime.now() - start).total_seconds()
print(f"  ✓ 完成 ({elapsed:.1f}秒)")

# ============================================================
# 步骤4: 性能基线建立（60秒）
# ============================================================
print("\n[步骤4] 性能基线建立（60秒）...")
start = datetime.now()

# 建立基线
baselines = {
    '随机猜测': 0.50,
    '当前模型': test_auc,
    '目标AUC': 0.70,
}

print("  性能基线:")
for name, value in baselines.items():
    status = '✓' if value >= 0.70 else '⚠️' if value >= 0.55 else '✗'
    print(f"    {name}: {value:.4f} {status}")

# 差距分析
gap = 0.70 - test_auc
if gap > 0:
    print(f"\n  距离目标差距: {gap:.4f}")
    print(f"  需要改进: {gap/0.20*100:.0f}%")
    
    if gap < 0.10:
        print("  ✓ 接近目标，可通过特征工程和调优达到")
    elif gap < 0.20:
        print("  ⚠️ 需要显著改进，建议:")
        print("    - 增加更多有效特征")
        print("    - 改进数据质量")
        print("    - 优化模型架构")
    else:
        print("  ✗ 差距较大，需要重新审视方法")

elapsed = (datetime.now() - start).total_seconds()
print(f"  ✓ 完成 ({elapsed:.1f}秒)")

# ============================================================
# 总结
# ============================================================
print("\n" + "="*70)
print("验证总结")
print("="*70)

total_time = (datetime.now() - datetime.now()).total_seconds()  # 重新计算总时间

print(f"数据源: {best_source[0]}")
print(f"样本数: {len(df)}")
print(f"特征数: {len(available_features)}")
print(f"测试AUC: {test_auc:.4f}")
print(f"目标AUC: 0.70")
print(f"差距: {0.70 - test_auc:.4f}")

if test_auc >= 0.70:
    print("\n✅ 方法验证通过！可以直接用于预测系统")
elif test_auc >= 0.55:
    print("\n⚠️ 方法基本可行，但需要优化才能达到目标")
    print("建议:")
    print("  1. 使用完整数据集训练")
    print("  2. 添加更多有效特征")
    print("  3. 进行超参数调优")
else:
    print("\n✗ 方法不可行，需要重新设计")
    print("建议:")
    print("  1. 检查数据质量")
    print("  2. 重新设计特征")
    print("  3. 考虑其他预测方法")

print("="*70)
