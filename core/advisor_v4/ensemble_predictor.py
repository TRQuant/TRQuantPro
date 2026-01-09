# -*- coding: utf-8 -*-
"""
集成预测器 - 多模型融合提升预测性能

功能：
1. 多XGBoost模型集成（不同参数/特征子集）
2. Stacking集成
3. 加权投票
4. 模型多样性增强
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any, Callable
import pickle
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ModelMetrics:
    """模型指标"""
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
    auc: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            'accuracy': self.accuracy,
            'precision': self.precision,
            'recall': self.recall,
            'f1': self.f1,
            'auc': self.auc,
        }


class EnsemblePredictor:
    """集成预测器 - 多模型融合"""
    
    def __init__(self, 
                 n_models: int = 3,
                 ensemble_method: str = 'weighted_average',
                 random_state: int = 42):
        """
        Args:
            n_models: 模型数量
            ensemble_method: 集成方法 ('average', 'weighted_average', 'voting', 'stacking')
            random_state: 随机种子
        """
        self.n_models = n_models
        self.ensemble_method = ensemble_method
        self.random_state = random_state
        
        self.models = []
        self.weights = []
        self.feature_subsets = []
        self.scalers = []
        self.meta_model = None
        
        self.is_trained = False
    
    def train(self, 
              train_df: pd.DataFrame,
              val_df: pd.DataFrame,
              label_col: str = 'label') -> Dict:
        """训练集成模型
        
        Args:
            train_df: 训练数据
            val_df: 验证数据
            label_col: 标签列
            
        Returns:
            训练结果
        """
        from xgboost import XGBClassifier
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import roc_auc_score
        
        print(f"\n训练集成模型 ({self.n_models} 个模型, 方法={self.ensemble_method})...")
        
        # 获取所有数值特征
        feature_cols = [c for c in train_df.columns 
                        if c != label_col and train_df[c].dtype in ['int64', 'float64', 'float32']]
        
        print(f"  可用特征: {len(feature_cols)}")
        
        # 不同的模型配置
        model_configs = self._generate_diverse_configs()
        
        for i in range(self.n_models):
            print(f"\n  训练模型 {i+1}/{self.n_models}...")
            
            # 选择特征子集（Bootstrap特征）
            np.random.seed(self.random_state + i)
            n_features = max(int(len(feature_cols) * 0.7), 5)
            selected_features = np.random.choice(feature_cols, size=n_features, replace=False)
            self.feature_subsets.append(list(selected_features))
            
            # 准备数据
            X_train = train_df[selected_features].values
            y_train = train_df[label_col].values
            X_val = val_df[selected_features].values
            y_val = val_df[label_col].values
            
            # 标准化
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_val = scaler.transform(X_val)
            self.scalers.append(scaler)
            
            # 填充NaN
            X_train = np.nan_to_num(X_train, nan=0.0)
            X_val = np.nan_to_num(X_val, nan=0.0)
            
            # 获取模型配置
            config = model_configs[i % len(model_configs)]
            config['random_state'] = self.random_state + i
            config['use_label_encoder'] = False
            config['eval_metric'] = 'logloss'
            
            # 训练模型
            model = XGBClassifier(**config)
            model.fit(
                X_train, y_train,
                eval_set=[(X_val, y_val)],
                verbose=False
            )
            
            self.models.append(model)
            
            # 计算验证集AUC
            y_pred_proba = model.predict_proba(X_val)[:, 1]
            if len(np.unique(y_val)) >= 2:
                auc = roc_auc_score(y_val, y_pred_proba)
            else:
                auc = 0.5
            
            # 权重基于性能
            self.weights.append(auc)
            
            print(f"    特征数: {n_features}, AUC: {auc:.4f}")
        
        # 归一化权重
        weight_sum = sum(self.weights)
        self.weights = [w / weight_sum for w in self.weights]
        
        # Stacking方法需要训练元模型
        if self.ensemble_method == 'stacking':
            self._train_meta_model(train_df, val_df, label_col)
        
        self.is_trained = True
        
        # 评估集成效果
        ensemble_metrics = self.evaluate(val_df, label_col)
        
        print(f"\n  集成模型 AUC: {ensemble_metrics['auc']:.4f}")
        print(f"  权重: {[f'{w:.3f}' for w in self.weights]}")
        
        return {
            'n_models': self.n_models,
            'ensemble_method': self.ensemble_method,
            'individual_aucs': [w * weight_sum for w in self.weights],
            'ensemble_auc': ensemble_metrics['auc'],
            'weights': self.weights,
        }
    
    def _generate_diverse_configs(self) -> List[Dict]:
        """生成多样化的模型配置"""
        return [
            # 配置1: 保守型
            {
                'n_estimators': 100,
                'max_depth': 3,
                'learning_rate': 0.05,
                'subsample': 0.7,
                'colsample_bytree': 0.7,
                'min_child_weight': 5,
                'gamma': 0.3,
                'reg_alpha': 0.5,
                'reg_lambda': 2.0,
            },
            # 配置2: 平衡型
            {
                'n_estimators': 150,
                'max_depth': 4,
                'learning_rate': 0.08,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'min_child_weight': 3,
                'gamma': 0.2,
                'reg_alpha': 0.3,
                'reg_lambda': 1.5,
            },
            # 配置3: 深度型
            {
                'n_estimators': 200,
                'max_depth': 5,
                'learning_rate': 0.05,
                'subsample': 0.7,
                'colsample_bytree': 0.7,
                'min_child_weight': 5,
                'gamma': 0.3,
                'reg_alpha': 0.5,
                'reg_lambda': 2.0,
            },
            # 配置4: 快速型
            {
                'n_estimators': 100,
                'max_depth': 2,
                'learning_rate': 0.15,
                'subsample': 0.9,
                'colsample_bytree': 0.9,
                'min_child_weight': 1,
                'gamma': 0.05,
                'reg_alpha': 0.1,
                'reg_lambda': 0.5,
            },
            # 配置5: 激进型
            {
                'n_estimators': 250,
                'max_depth': 6,
                'learning_rate': 0.03,
                'subsample': 0.6,
                'colsample_bytree': 0.6,
                'min_child_weight': 7,
                'gamma': 0.4,
                'reg_alpha': 0.7,
                'reg_lambda': 2.5,
            },
        ]
    
    def _train_meta_model(self,
                          train_df: pd.DataFrame,
                          val_df: pd.DataFrame,
                          label_col: str):
        """训练Stacking的元模型"""
        from sklearn.linear_model import LogisticRegression
        
        # 生成第一层预测
        train_preds = self._get_base_predictions(train_df, label_col)
        val_preds = self._get_base_predictions(val_df, label_col)
        
        y_train = train_df[label_col].values
        y_val = val_df[label_col].values
        
        # 训练逻辑回归元模型
        self.meta_model = LogisticRegression(
            random_state=self.random_state,
            max_iter=1000
        )
        self.meta_model.fit(train_preds, y_train)
    
    def _get_base_predictions(self, df: pd.DataFrame, label_col: str) -> np.ndarray:
        """获取所有基模型的预测"""
        predictions = []
        
        for i, model in enumerate(self.models):
            features = self.feature_subsets[i]
            available_features = [f for f in features if f in df.columns]
            
            if not available_features:
                predictions.append(np.zeros(len(df)))
                continue
            
            X = df[available_features].values
            X = self.scalers[i].transform(X)
            X = np.nan_to_num(X, nan=0.0)
            
            pred = model.predict_proba(X)[:, 1]
            predictions.append(pred)
        
        return np.column_stack(predictions)
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """集成预测
        
        Args:
            df: 输入数据
            
        Returns:
            预测概率
        """
        if not self.is_trained:
            raise ValueError("模型未训练")
        
        predictions = []
        
        for i, model in enumerate(self.models):
            features = self.feature_subsets[i]
            available_features = [f for f in features if f in df.columns]
            
            if not available_features:
                predictions.append(np.zeros(len(df)))
                continue
            
            X = df[available_features].values
            X = self.scalers[i].transform(X)
            X = np.nan_to_num(X, nan=0.0)
            
            pred = model.predict_proba(X)[:, 1]
            predictions.append(pred)
        
        predictions = np.array(predictions)
        
        if self.ensemble_method == 'average':
            return predictions.mean(axis=0)
        
        elif self.ensemble_method == 'weighted_average':
            weighted_pred = np.zeros(len(df))
            for i, (pred, weight) in enumerate(zip(predictions, self.weights)):
                weighted_pred += pred * weight
            return weighted_pred
        
        elif self.ensemble_method == 'voting':
            # 硬投票
            binary_preds = (predictions > 0.5).astype(int)
            votes = binary_preds.sum(axis=0)
            return votes / len(self.models)
        
        elif self.ensemble_method == 'stacking':
            if self.meta_model is None:
                return predictions.mean(axis=0)
            
            base_preds = predictions.T
            return self.meta_model.predict_proba(base_preds)[:, 1]
        
        else:
            return predictions.mean(axis=0)
    
    def predict_binary(self, df: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        """二分类预测"""
        proba = self.predict(df)
        return (proba >= threshold).astype(int)
    
    def evaluate(self, df: pd.DataFrame, label_col: str = 'label') -> Dict:
        """评估模型
        
        Returns:
            评估指标
        """
        from sklearn.metrics import (
            accuracy_score, precision_score, recall_score, 
            f1_score, roc_auc_score
        )
        
        y_true = df[label_col].values
        y_pred_proba = self.predict(df)
        y_pred = (y_pred_proba >= 0.5).astype(int)
        
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1': f1_score(y_true, y_pred, zero_division=0),
        }
        
        if len(np.unique(y_true)) >= 2:
            metrics['auc'] = roc_auc_score(y_true, y_pred_proba)
        else:
            metrics['auc'] = 0.5
        
        return metrics
    
    def get_feature_importance(self) -> Dict[str, float]:
        """获取集成模型的特征重要性"""
        importance_sum = {}
        
        for i, model in enumerate(self.models):
            features = self.feature_subsets[i]
            importances = model.feature_importances_
            weight = self.weights[i]
            
            for feature, importance in zip(features, importances):
                if feature not in importance_sum:
                    importance_sum[feature] = 0
                importance_sum[feature] += importance * weight
        
        # 排序
        sorted_importance = dict(
            sorted(importance_sum.items(), key=lambda x: x[1], reverse=True)
        )
        
        return sorted_importance
    
    def save(self, path: str):
        """保存模型"""
        save_dict = {
            'n_models': self.n_models,
            'ensemble_method': self.ensemble_method,
            'random_state': self.random_state,
            'models': self.models,
            'weights': self.weights,
            'feature_subsets': self.feature_subsets,
            'scalers': self.scalers,
            'meta_model': self.meta_model,
            'is_trained': self.is_trained,
        }
        
        with open(path, 'wb') as f:
            pickle.dump(save_dict, f)
        
        print(f"集成模型已保存: {path}")
    
    def load(self, path: str):
        """加载模型"""
        with open(path, 'rb') as f:
            save_dict = pickle.load(f)
        
        self.n_models = save_dict['n_models']
        self.ensemble_method = save_dict['ensemble_method']
        self.random_state = save_dict['random_state']
        self.models = save_dict['models']
        self.weights = save_dict['weights']
        self.feature_subsets = save_dict['feature_subsets']
        self.scalers = save_dict['scalers']
        self.meta_model = save_dict['meta_model']
        self.is_trained = save_dict['is_trained']
        
        print(f"集成模型已加载: {path}")


class BaggingEnsemble:
    """Bagging集成 - 数据采样多样性"""
    
    def __init__(self, 
                 n_estimators: int = 5,
                 sample_ratio: float = 0.8,
                 random_state: int = 42):
        """
        Args:
            n_estimators: 模型数量
            sample_ratio: 每个模型使用的样本比例
            random_state: 随机种子
        """
        self.n_estimators = n_estimators
        self.sample_ratio = sample_ratio
        self.random_state = random_state
        
        self.models = []
        self.scalers = []
        self.feature_cols = None
    
    def train(self,
              train_df: pd.DataFrame,
              val_df: pd.DataFrame,
              label_col: str = 'label') -> Dict:
        """训练Bagging集成"""
        from xgboost import XGBClassifier
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import roc_auc_score
        
        print(f"\n训练Bagging集成 ({self.n_estimators} 个模型)...")
        
        # 获取特征列
        self.feature_cols = [c for c in train_df.columns 
                             if c != label_col and train_df[c].dtype in ['int64', 'float64', 'float32']]
        
        aucs = []
        
        for i in range(self.n_estimators):
            print(f"\n  训练模型 {i+1}/{self.n_estimators}...")
            
            # Bootstrap采样
            np.random.seed(self.random_state + i)
            sample_indices = np.random.choice(
                len(train_df), 
                size=int(len(train_df) * self.sample_ratio),
                replace=True
            )
            sample_df = train_df.iloc[sample_indices]
            
            # 准备数据
            X_train = sample_df[self.feature_cols].values
            y_train = sample_df[label_col].values
            X_val = val_df[self.feature_cols].values
            y_val = val_df[label_col].values
            
            # 标准化
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_val = scaler.transform(X_val)
            self.scalers.append(scaler)
            
            # 填充NaN
            X_train = np.nan_to_num(X_train, nan=0.0)
            X_val = np.nan_to_num(X_val, nan=0.0)
            
            # 训练模型
            model = XGBClassifier(
                n_estimators=150,
                max_depth=4,
                learning_rate=0.08,
                subsample=0.8,
                colsample_bytree=0.8,
                min_child_weight=3,
                gamma=0.2,
                reg_alpha=0.3,
                reg_lambda=1.5,
                random_state=self.random_state + i,
                use_label_encoder=False,
                eval_metric='logloss'
            )
            
            model.fit(X_train, y_train, verbose=False)
            self.models.append(model)
            
            # 计算AUC
            y_pred_proba = model.predict_proba(X_val)[:, 1]
            if len(np.unique(y_val)) >= 2:
                auc = roc_auc_score(y_val, y_pred_proba)
            else:
                auc = 0.5
            
            aucs.append(auc)
            print(f"    AUC: {auc:.4f}")
        
        # 评估集成效果
        ensemble_auc = self._evaluate_ensemble(val_df, label_col)
        
        print(f"\n  Bagging集成 AUC: {ensemble_auc:.4f}")
        print(f"  平均单模型 AUC: {np.mean(aucs):.4f}")
        
        return {
            'n_estimators': self.n_estimators,
            'individual_aucs': aucs,
            'mean_auc': np.mean(aucs),
            'ensemble_auc': ensemble_auc,
        }
    
    def _evaluate_ensemble(self, df: pd.DataFrame, label_col: str) -> float:
        """评估集成效果"""
        from sklearn.metrics import roc_auc_score
        
        y_true = df[label_col].values
        y_pred_proba = self.predict(df)
        
        if len(np.unique(y_true)) >= 2:
            return roc_auc_score(y_true, y_pred_proba)
        return 0.5
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """预测"""
        predictions = []
        
        for i, model in enumerate(self.models):
            X = df[self.feature_cols].values
            X = self.scalers[i].transform(X)
            X = np.nan_to_num(X, nan=0.0)
            
            pred = model.predict_proba(X)[:, 1]
            predictions.append(pred)
        
        return np.mean(predictions, axis=0)


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("测试集成预测器...")
    
    # 创建模拟数据
    np.random.seed(42)
    n_train = 800
    n_val = 200
    
    def generate_data(n):
        X = np.random.randn(n, 14)
        # 创建有规律的标签
        y = (X[:, 0] + 0.5 * X[:, 1] - 0.3 * X[:, 2] + np.random.randn(n) * 0.5 > 0).astype(int)
        
        df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(14)])
        df['label'] = y
        
        return df
    
    train_df = generate_data(n_train)
    val_df = generate_data(n_val)
    
    print(f"训练集: {len(train_df)} | 验证集: {len(val_df)}")
    print(f"正样本比例: {train_df['label'].mean():.2%}")
    
    # 测试EnsemblePredictor
    print("\n=== 测试加权平均集成 ===")
    ensemble = EnsemblePredictor(n_models=3, ensemble_method='weighted_average')
    result = ensemble.train(train_df, val_df)
    
    print(f"\n特征重要性 Top 5:")
    importance = ensemble.get_feature_importance()
    for feat, imp in list(importance.items())[:5]:
        print(f"  {feat}: {imp:.4f}")
    
    # 测试Stacking
    print("\n=== 测试Stacking集成 ===")
    stacking = EnsemblePredictor(n_models=3, ensemble_method='stacking')
    result_stacking = stacking.train(train_df, val_df)
    
    # 测试Bagging
    print("\n=== 测试Bagging集成 ===")
    bagging = BaggingEnsemble(n_estimators=3)
    result_bagging = bagging.train(train_df, val_df)
    
    print("\n测试完成!")
