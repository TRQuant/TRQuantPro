# -*- coding: utf-8 -*-
"""
超参数优化器 - 使用Optuna进行贝叶斯优化

功能：
1. XGBoost超参数自动搜索
2. 贝叶斯优化（TPE采样器）
3. 交叉验证评估
4. 早停机制
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
import logging
import warnings

logger = logging.getLogger(__name__)

# 抑制optuna的日志
try:
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
except ImportError:
    optuna = None


class HyperparameterOptimizer:
    """超参数优化器 - 使用Optuna进行贝叶斯优化"""
    
    # 默认搜索空间
    DEFAULT_SEARCH_SPACE = {
        'n_estimators': {'type': 'int', 'low': 100, 'high': 300, 'step': 50},
        'max_depth': {'type': 'int', 'low': 3, 'high': 8},
        'learning_rate': {'type': 'float', 'low': 0.01, 'high': 0.2, 'log': True},
        'subsample': {'type': 'float', 'low': 0.6, 'high': 1.0},
        'colsample_bytree': {'type': 'float', 'low': 0.6, 'high': 1.0},
        'min_child_weight': {'type': 'int', 'low': 1, 'high': 10},
        'gamma': {'type': 'float', 'low': 0, 'high': 0.5},
        'reg_alpha': {'type': 'float', 'low': 0, 'high': 1.0},
        'reg_lambda': {'type': 'float', 'low': 0.5, 'high': 3.0},
        'scale_pos_weight': {'type': 'float', 'low': 1, 'high': 5},
    }
    
    def __init__(self, 
                 search_space: Dict = None,
                 metric: str = 'auc',
                 cv_folds: int = 3,
                 random_state: int = 42):
        """
        Args:
            search_space: 搜索空间定义
            metric: 优化目标（'auc', 'f1', 'precision'）
            cv_folds: 交叉验证折数
            random_state: 随机种子
        """
        self.search_space = search_space or self.DEFAULT_SEARCH_SPACE
        self.metric = metric
        self.cv_folds = cv_folds
        self.random_state = random_state
        
        self.study = None
        self.best_params = None
        self.history = []
    
    def optimize(self,
                 train_df: pd.DataFrame,
                 val_df: pd.DataFrame,
                 feature_cols: List[str] = None,
                 label_col: str = 'label',
                 n_trials: int = 50,
                 timeout: int = 600) -> Dict:
        """优化超参数
        
        Args:
            train_df: 训练数据
            val_df: 验证数据
            feature_cols: 特征列
            label_col: 标签列
            n_trials: 试验次数
            timeout: 超时时间（秒）
            
        Returns:
            最佳参数
        """
        if optuna is None:
            logger.warning("Optuna未安装，使用网格搜索")
            return self._grid_search(train_df, val_df, feature_cols, label_col)
        
        from xgboost import XGBClassifier
        from sklearn.metrics import roc_auc_score, f1_score, precision_score
        from sklearn.preprocessing import StandardScaler
        
        # 准备数据
        if feature_cols is None:
            from .xgboost_predictor import XGBoostPredictor
            feature_cols = XGBoostPredictor.FEATURE_COLUMNS
        
        available_cols = [c for c in feature_cols if c in train_df.columns]
        
        X_train = train_df[available_cols].values
        y_train = train_df[label_col].values
        X_val = val_df[available_cols].values
        y_val = val_df[label_col].values
        
        # 标准化
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)
        
        # 填充NaN
        X_train = np.nan_to_num(X_train, nan=0.0)
        X_val = np.nan_to_num(X_val, nan=0.0)
        
        def objective(trial):
            params = self._sample_params(trial)
            
            # 固定参数
            params['random_state'] = self.random_state
            params['use_label_encoder'] = False
            params['eval_metric'] = 'logloss'
            
            try:
                model = XGBClassifier(**params)
                model.fit(
                    X_train, y_train,
                    eval_set=[(X_val, y_val)],
                    verbose=False
                )
                
                y_pred_proba = model.predict_proba(X_val)[:, 1]
                y_pred = model.predict(X_val)
                
                if self.metric == 'auc':
                    if len(np.unique(y_val)) < 2:
                        return 0.5
                    score = roc_auc_score(y_val, y_pred_proba)
                elif self.metric == 'f1':
                    score = f1_score(y_val, y_pred, zero_division=0)
                elif self.metric == 'precision':
                    score = precision_score(y_val, y_pred, zero_division=0)
                else:
                    score = roc_auc_score(y_val, y_pred_proba)
                
                return score
                
            except Exception as e:
                logger.warning(f"试验失败: {e}")
                return 0.0
        
        # 创建study
        sampler = optuna.samplers.TPESampler(seed=self.random_state)
        self.study = optuna.create_study(
            direction='maximize',
            sampler=sampler
        )
        
        # 运行优化
        print(f"开始超参数优化: {n_trials} 次试验, 超时 {timeout}秒")
        
        self.study.optimize(
            objective, 
            n_trials=n_trials,
            timeout=timeout,
            show_progress_bar=True,
            callbacks=[self._callback]
        )
        
        # 获取最佳参数
        self.best_params = self.study.best_params
        self.best_params['random_state'] = self.random_state
        self.best_params['use_label_encoder'] = False
        self.best_params['eval_metric'] = 'logloss'
        
        print(f"\n最佳参数 ({self.metric} = {self.study.best_value:.4f}):")
        for key, value in self.best_params.items():
            if key not in ['random_state', 'use_label_encoder', 'eval_metric']:
                print(f"  {key}: {value}")
        
        return self.best_params
    
    def _sample_params(self, trial) -> Dict:
        """从搜索空间采样参数"""
        params = {}
        
        for name, space in self.search_space.items():
            if space['type'] == 'int':
                if 'step' in space:
                    params[name] = trial.suggest_int(
                        name, space['low'], space['high'], step=space['step']
                    )
                else:
                    params[name] = trial.suggest_int(
                        name, space['low'], space['high']
                    )
            elif space['type'] == 'float':
                params[name] = trial.suggest_float(
                    name, space['low'], space['high'],
                    log=space.get('log', False)
                )
            elif space['type'] == 'categorical':
                params[name] = trial.suggest_categorical(
                    name, space['choices']
                )
        
        return params
    
    def _callback(self, study, trial):
        """优化回调"""
        self.history.append({
            'trial': trial.number,
            'value': trial.value,
            'params': trial.params,
            'datetime': trial.datetime_complete.isoformat() if trial.datetime_complete else None,
        })
    
    def _grid_search(self,
                     train_df: pd.DataFrame,
                     val_df: pd.DataFrame,
                     feature_cols: List[str],
                     label_col: str) -> Dict:
        """网格搜索（Optuna不可用时的回退方案）"""
        from xgboost import XGBClassifier
        from sklearn.metrics import roc_auc_score
        from sklearn.preprocessing import StandardScaler
        from itertools import product
        from tqdm import tqdm
        
        # 准备数据
        if feature_cols is None:
            from .xgboost_predictor import XGBoostPredictor
            feature_cols = XGBoostPredictor.FEATURE_COLUMNS
        
        available_cols = [c for c in feature_cols if c in train_df.columns]
        
        X_train = train_df[available_cols].values
        y_train = train_df[label_col].values
        X_val = val_df[available_cols].values
        y_val = val_df[label_col].values
        
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)
        
        X_train = np.nan_to_num(X_train, nan=0.0)
        X_val = np.nan_to_num(X_val, nan=0.0)
        
        # 简化的网格
        param_grid = {
            'n_estimators': [100, 150, 200],
            'max_depth': [3, 4, 5, 6],
            'learning_rate': [0.03, 0.05, 0.1],
            'subsample': [0.7, 0.8, 0.9],
            'colsample_bytree': [0.7, 0.8],
            'min_child_weight': [3, 5],
        }
        
        # 生成参数组合
        keys = list(param_grid.keys())
        combinations = list(product(*[param_grid[k] for k in keys]))
        
        best_score = 0
        best_params = {}
        
        for combo in tqdm(combinations, desc="网格搜索"):
            params = dict(zip(keys, combo))
            params['random_state'] = self.random_state
            params['use_label_encoder'] = False
            params['eval_metric'] = 'logloss'
            
            try:
                model = XGBClassifier(**params)
                model.fit(X_train, y_train, verbose=False)
                
                y_pred_proba = model.predict_proba(X_val)[:, 1]
                
                if len(np.unique(y_val)) >= 2:
                    score = roc_auc_score(y_val, y_pred_proba)
                else:
                    score = 0.5
                
                if score > best_score:
                    best_score = score
                    best_params = params.copy()
            
            except Exception as e:
                continue
        
        self.best_params = best_params
        print(f"网格搜索完成: 最佳AUC = {best_score:.4f}")
        
        return best_params
    
    def get_history(self) -> List[Dict]:
        """获取优化历史"""
        return self.history
    
    def get_best_trial_info(self) -> Dict:
        """获取最佳试验信息"""
        if self.study is None:
            return {}
        
        best_trial = self.study.best_trial
        
        return {
            'number': best_trial.number,
            'value': best_trial.value,
            'params': best_trial.params,
            'datetime': best_trial.datetime_complete.isoformat() if best_trial.datetime_complete else None,
        }
    
    def plot_optimization_history(self, save_path: str = None):
        """绘制优化历史"""
        if self.study is None or optuna is None:
            logger.warning("无优化历史可绘制")
            return
        
        try:
            import plotly.graph_objects as go
            from optuna.visualization import plot_optimization_history
            
            fig = plot_optimization_history(self.study)
            
            if save_path:
                fig.write_html(save_path)
                print(f"优化历史图已保存: {save_path}")
            else:
                fig.show()
        
        except Exception as e:
            logger.warning(f"绘图失败: {e}")
    
    def plot_param_importances(self, save_path: str = None):
        """绘制参数重要性"""
        if self.study is None or optuna is None:
            logger.warning("无参数重要性可绘制")
            return
        
        try:
            from optuna.visualization import plot_param_importances
            
            fig = plot_param_importances(self.study)
            
            if save_path:
                fig.write_html(save_path)
                print(f"参数重要性图已保存: {save_path}")
            else:
                fig.show()
        
        except Exception as e:
            logger.warning(f"绘图失败: {e}")


# ============================================================
# 快速超参数搜索
# ============================================================

class QuickHyperparameterSearch:
    """快速超参数搜索 - 简化版，无需Optuna"""
    
    PARAM_CONFIGS = {
        'conservative': {
            'n_estimators': 100,
            'max_depth': 3,
            'learning_rate': 0.05,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'min_child_weight': 5,
            'gamma': 0.3,
            'reg_alpha': 0.5,
            'reg_lambda': 2.0,
        },
        'balanced': {
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
        'aggressive': {
            'n_estimators': 200,
            'max_depth': 5,
            'learning_rate': 0.1,
            'subsample': 0.9,
            'colsample_bytree': 0.9,
            'min_child_weight': 2,
            'gamma': 0.1,
            'reg_alpha': 0.1,
            'reg_lambda': 1.0,
        },
        'deep': {
            'n_estimators': 250,
            'max_depth': 6,
            'learning_rate': 0.05,
            'subsample': 0.7,
            'colsample_bytree': 0.7,
            'min_child_weight': 5,
            'gamma': 0.3,
            'reg_alpha': 0.5,
            'reg_lambda': 2.0,
        },
        'shallow_fast': {
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
    }
    
    def __init__(self):
        self.results = {}
    
    def search(self,
               train_df: pd.DataFrame,
               val_df: pd.DataFrame,
               feature_cols: List[str] = None,
               label_col: str = 'label') -> Dict:
        """快速搜索最佳配置"""
        from xgboost import XGBClassifier
        from sklearn.metrics import roc_auc_score
        from sklearn.preprocessing import StandardScaler
        
        # 准备数据
        if feature_cols is None:
            from .xgboost_predictor import XGBoostPredictor
            feature_cols = XGBoostPredictor.FEATURE_COLUMNS
        
        available_cols = [c for c in feature_cols if c in train_df.columns]
        
        X_train = train_df[available_cols].values
        y_train = train_df[label_col].values
        X_val = val_df[available_cols].values
        y_val = val_df[label_col].values
        
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)
        
        X_train = np.nan_to_num(X_train, nan=0.0)
        X_val = np.nan_to_num(X_val, nan=0.0)
        
        best_score = 0
        best_config = None
        best_params = None
        
        for config_name, params in self.PARAM_CONFIGS.items():
            try:
                full_params = params.copy()
                full_params['random_state'] = 42
                full_params['use_label_encoder'] = False
                full_params['eval_metric'] = 'logloss'
                
                model = XGBClassifier(**full_params)
                model.fit(X_train, y_train, verbose=False)
                
                y_pred_proba = model.predict_proba(X_val)[:, 1]
                
                if len(np.unique(y_val)) >= 2:
                    score = roc_auc_score(y_val, y_pred_proba)
                else:
                    score = 0.5
                
                self.results[config_name] = {
                    'auc': score,
                    'params': full_params,
                }
                
                print(f"  {config_name}: AUC = {score:.4f}")
                
                if score > best_score:
                    best_score = score
                    best_config = config_name
                    best_params = full_params.copy()
            
            except Exception as e:
                logger.warning(f"配置 {config_name} 失败: {e}")
                continue
        
        print(f"\n最佳配置: {best_config} (AUC = {best_score:.4f})")
        
        return best_params


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("测试超参数优化器...")
    
    # 创建模拟数据
    np.random.seed(42)
    n_train = 800
    n_val = 200
    
    # 创建有一定规律的数据
    def generate_data(n):
        X = np.random.randn(n, 14)
        y = (X[:, 0] + 0.5 * X[:, 1] + np.random.randn(n) * 0.5 > 0).astype(int)
        
        df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(14)])
        df['label'] = y
        
        return df
    
    train_df = generate_data(n_train)
    val_df = generate_data(n_val)
    
    print(f"训练集: {len(train_df)} | 验证集: {len(val_df)}")
    print(f"正样本比例: {train_df['label'].mean():.2%}")
    
    # 测试快速搜索
    print("\n快速搜索测试:")
    quick_search = QuickHyperparameterSearch()
    best_params = quick_search.search(
        train_df, val_df,
        feature_cols=[f'feature_{i}' for i in range(14)],
        label_col='label'
    )
    
    # 测试Optuna优化（如果可用）
    if optuna is not None:
        print("\nOptuna优化测试（5次试验）:")
        optimizer = HyperparameterOptimizer(metric='auc')
        best_params = optimizer.optimize(
            train_df, val_df,
            feature_cols=[f'feature_{i}' for i in range(14)],
            label_col='label',
            n_trials=5,
            timeout=60
        )
    
    print("\n测试完成!")
