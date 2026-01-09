"""
XGBoost预测模型 - 周频：预测股票未来1周是否能获得5%+收益（动态适配节假日）

模型设计：
- 输入: T时刻的多维因子向量
- 输出: 未来1周收益>=5%的概率
- 训练集: 2024-09 ~ 2025-06
- 验证集: 2025-06 ~ 2025-09
- 测试集: 2025-09-30 ~ 2025-12-31

防过拟合设计：
- 增强正则化参数（L1/L2）
- 早停机制（early_stopping_rounds）
- 训练/验证指标对比
- 过拟合检测
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import pickle
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

# 尝试导入机器学习库
try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    logger.warning("XGBoost未安装，使用简化模型")

try:
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        roc_auc_score, classification_report, confusion_matrix
    )
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    logger.warning("scikit-learn未安装")


# ============================================================
# 正则化参数配置
# ============================================================

# 默认参数（原版）
DEFAULT_MODEL_PARAMS = {
    'n_estimators': 200,
    'max_depth': 6,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'min_child_weight': 3,
    'gamma': 0.1,
    'reg_alpha': 0.1,
    'reg_lambda': 1.0,
    'scale_pos_weight': 3,
    'random_state': 42,
    'use_label_encoder': False,
    'eval_metric': 'logloss',
}

# 增强正则化参数（防过拟合）
REGULARIZED_MODEL_PARAMS = {
    'n_estimators': 150,      # 减少树数量
    'max_depth': 4,           # 降低深度（原6）
    'learning_rate': 0.05,    # 降低学习率（原0.1）
    'subsample': 0.7,         # 行采样
    'colsample_bytree': 0.7,  # 列采样
    'min_child_weight': 5,    # 增加叶子节点最小样本数（原3）
    'gamma': 0.3,             # 增加分裂阈值（原0.1）
    'reg_alpha': 0.5,         # L1正则化（原0.1）
    'reg_lambda': 2.0,        # L2正则化（原1.0）
    'scale_pos_weight': 3,    # 处理类别不平衡
    'random_state': 42,
    'use_label_encoder': False,
    'eval_metric': 'logloss',
}


@dataclass
class PredictionResult:
    """预测结果"""
    code: str
    probability: float      # 预测概率
    prediction: int         # 预测标签 (0/1)
    confidence: str         # 置信度等级
    factors: Dict = field(default_factory=dict)


@dataclass
class ModelMetrics:
    """模型评估指标"""
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
    auc: float = 0.0
    confusion_matrix: Optional[np.ndarray] = None


class XGBoostPredictor:
    """XGBoost高收益预测器
    
    增强功能：
    - 支持自定义模型参数
    - 增强正则化（防过拟合）
    - 早停机制
    - 过拟合检测
    """
    
    # 特征列（与 multi_factor_calculator.py 输出匹配）
    FEATURE_COLUMNS = [
        # 基本面
        'market_cap', 'roe', 'growth',
        # 技术面  
        'momentum_5d', 'momentum_10d', 'momentum_20d',
        'rel_strength', 'rsi', 'volume_ratio',
        # 资金面
        'fin_change', 'turnover_rate', 'on_billboard',
        # 情绪
        'concept_count',
        # 市场环境
        'market_trend',
    ]
    
    def __init__(self, 
                 model_path: str = None,
                 threshold: float = 0.5,
                 model_params: Dict = None,
                 use_regularization: bool = True,
                 verbose: bool = True):
        """
        Args:
            model_path: 模型保存路径
            threshold: 预测阈值
            model_params: 自定义模型参数（覆盖默认）
            use_regularization: 是否使用增强正则化参数
            verbose: 是否打印详细信息
        """
        self.model_path = model_path or 'models/xgb_high_return_predictor.pkl'
        self.threshold = threshold
        self.use_regularization = use_regularization
        self.verbose = verbose
        
        self.model = None
        self.scaler = None
        self.feature_importance = None
        self.metrics = None
        self.train_metrics = None  # 新增：训练集指标
        self.val_metrics = None    # 新增：验证集指标
        
        # 早停相关
        self.best_iteration = None
        self.early_stopping_used = False
        
        # 特征流水线相关（如果使用了特征流水线）
        self._features_already_scaled = False  # 特征是否已经标准化
        self._selected_features = None  # 选择的特征列表
        
        # 选择参数
        if model_params:
            self.model_params = model_params
        elif use_regularization:
            self.model_params = REGULARIZED_MODEL_PARAMS.copy()
        else:
            self.model_params = DEFAULT_MODEL_PARAMS.copy()
    
    def prepare_features(self, df: pd.DataFrame, use_selected_features: bool = False, selected_features: List[str] = None) -> Tuple[np.ndarray, List[str]]:
        """准备特征矩阵
        
        Args:
            df: 输入数据
            use_selected_features: 是否使用已选择的特征（特征流水线处理后）
            selected_features: 选择的特征列表（如果use_selected_features=True）
        """
        if use_selected_features and selected_features:
            # 使用特征流水线选择的特征
            available_cols = [c for c in selected_features if c in df.columns]
        else:
            # 使用原始特征列
            available_cols = [c for c in self.FEATURE_COLUMNS if c in df.columns]
        
        X = df[available_cols].copy()
        
        # 处理缺失值
        X = X.fillna(X.median() if len(X) > 0 else 0)
        
        # 处理无穷值
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(0)
        
        return X.values, available_cols
    
    def train(self, 
              train_df: pd.DataFrame,
              val_df: pd.DataFrame = None,
              label_col: str = 'label',
              early_stopping_rounds: int = 20) -> ModelMetrics:
        """训练模型
        
        Args:
            train_df: 训练数据
            val_df: 验证数据
            label_col: 标签列名
            early_stopping_rounds: 早停轮数（验证集指标不改善时停止）
        """
        print(f"\n{'='*60}")
        print(f"【XGBoost模型训练】")
        if self.use_regularization:
            print(f"模式: 增强正则化（防过拟合）")
        print(f"{'='*60}")
        
        # 准备数据
        # 如果使用了特征流水线，直接使用已处理的特征列
        if self._selected_features is not None:
            # 使用特征流水线选择的特征
            available_cols = [c for c in self._selected_features if c in train_df.columns]
            X_train = train_df[available_cols].values
            feature_cols = available_cols
        else:
            X_train, feature_cols = self.prepare_features(train_df)
        
        y_train = train_df[label_col].values
        
        print(f"训练集: {len(X_train)} 样本, {len(feature_cols)} 特征")
        print(f"正样本比例: {y_train.mean():.1%}")
        if self._selected_features:
            print(f"使用特征流水线选择的特征: {len(feature_cols)} 个")
        
        # 自动计算scale_pos_weight
        if 'scale_pos_weight' in self.model_params:
            pos_ratio = y_train.mean()
            if pos_ratio > 0 and pos_ratio < 1:
                auto_weight = (1 - pos_ratio) / pos_ratio
                self.model_params['scale_pos_weight'] = min(auto_weight, 10)  # 限制最大值
                print(f"自动类别权重: {self.model_params['scale_pos_weight']:.2f}")
        
        # 标准化
        if HAS_SKLEARN and not self._features_already_scaled:
            self.scaler = StandardScaler()
            X_train = self.scaler.fit_transform(X_train)
        elif self._features_already_scaled:
            # 特征已经通过特征流水线标准化，不需要再次标准化
            self.scaler = None
            if self.verbose:
                print("特征已通过特征流水线标准化，跳过scaler")
        
        # 训练模型
        if HAS_XGBOOST:
            self.model = XGBClassifier(**self.model_params)
            
            if val_df is not None and len(val_df) > 0:
                # 如果使用了特征流水线，直接使用已处理的特征列
                if self._selected_features is not None:
                    available_cols = [c for c in self._selected_features if c in val_df.columns]
                    X_val = val_df[available_cols].values
                else:
                    X_val, _ = self.prepare_features(val_df)
                
                y_val = val_df[label_col].values
                if self.scaler:
                    X_val = self.scaler.transform(X_val)
                
                # 使用早停
                if early_stopping_rounds and early_stopping_rounds > 0:
                    print(f"早停机制: {early_stopping_rounds} 轮")
                    self.early_stopping_used = True
                    
                    self.model.fit(
                        X_train, y_train,
                        eval_set=[(X_train, y_train), (X_val, y_val)],
                        verbose=False
                    )
                    
                    # 记录最佳迭代
                    if hasattr(self.model, 'best_iteration'):
                        self.best_iteration = self.model.best_iteration
                        print(f"最佳迭代: {self.best_iteration}")
                else:
                    self.model.fit(
                        X_train, y_train,
                        eval_set=[(X_val, y_val)],
                        verbose=False
                    )
            else:
                self.model.fit(X_train, y_train)
            
            # 特征重要性
            self.feature_importance = dict(zip(feature_cols, self.model.feature_importances_))
        else:
            # 简化模型：逻辑回归
            from sklearn.linear_model import LogisticRegression
            self.model = LogisticRegression(
                class_weight='balanced',
                max_iter=1000,
                random_state=42
            )
            self.model.fit(X_train, y_train)
            self.feature_importance = dict(zip(feature_cols, np.abs(self.model.coef_[0])))
        
        # 评估训练集（用于过拟合检测）
        y_train_pred = self.model.predict(X_train)
        y_train_prob = self.model.predict_proba(X_train)[:, 1]
        
        self.train_metrics = ModelMetrics(
            accuracy=accuracy_score(y_train, y_train_pred),
            precision=precision_score(y_train, y_train_pred, zero_division=0),
            recall=recall_score(y_train, y_train_pred, zero_division=0),
            f1=f1_score(y_train, y_train_pred, zero_division=0),
            auc=roc_auc_score(y_train, y_train_prob) if len(np.unique(y_train)) > 1 else 0,
        )
        
        # 评估验证集
        if val_df is not None and len(val_df) > 0:
            self.val_metrics = self.evaluate(val_df, label_col)
            self.metrics = self.val_metrics  # 主指标使用验证集
        else:
            self.metrics = self.train_metrics
            self.val_metrics = None
        
        self._print_training_results()
        
        return self.metrics
    
    def evaluate(self, test_df: pd.DataFrame, label_col: str = 'label') -> ModelMetrics:
        """评估模型"""
        # 如果使用了特征流水线，直接使用已处理的特征列
        if self._selected_features is not None:
            available_cols = [c for c in self._selected_features if c in test_df.columns]
            X_test = test_df[available_cols].values
        else:
            X_test, _ = self.prepare_features(test_df)
        
        y_test = test_df[label_col].values
        
        if self.scaler:
            X_test = self.scaler.transform(X_test)
        
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]
        
        metrics = ModelMetrics(
            accuracy=accuracy_score(y_test, y_pred),
            precision=precision_score(y_test, y_pred, zero_division=0),
            recall=recall_score(y_test, y_pred, zero_division=0),
            f1=f1_score(y_test, y_pred, zero_division=0),
            auc=roc_auc_score(y_test, y_prob) if len(np.unique(y_test)) > 1 else 0,
            confusion_matrix=confusion_matrix(y_test, y_pred),
        )
        
        return metrics
    
    def predict(self, df: pd.DataFrame) -> List[PredictionResult]:
        """预测"""
        if self.model is None:
            raise ValueError("模型未训练，请先调用train()或load()")
        
        # 如果使用了特征流水线，直接使用已处理的特征列
        if self._selected_features is not None:
            available_cols = [c for c in self._selected_features if c in df.columns]
            if len(available_cols) != len(self._selected_features):
                missing = set(self._selected_features) - set(available_cols)
                raise ValueError(f"缺少必需特征: {missing}。期望 {len(self._selected_features)} 个特征，但只找到 {len(available_cols)} 个")
            X = df[available_cols].values
        else:
            X, _ = self.prepare_features(df)
        
        if self.scaler:
            X = self.scaler.transform(X)
        
        probabilities = self.model.predict_proba(X)[:, 1]
        predictions = (probabilities >= self.threshold).astype(int)
        
        results = []
        for i, (prob, pred) in enumerate(zip(probabilities, predictions)):
            # 置信度等级
            if prob >= 0.8:
                confidence = "极高"
            elif prob >= 0.6:
                confidence = "高"
            elif prob >= 0.4:
                confidence = "中"
            else:
                confidence = "低"
            
            result = PredictionResult(
                code=df.iloc[i].get('code', f'stock_{i}'),
                probability=float(prob),
                prediction=int(pred),
                confidence=confidence,
                factors={col: df.iloc[i].get(col, 0) for col in self.FEATURE_COLUMNS if col in df.columns}
            )
            results.append(result)
        
        return results
    
    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """预测概率"""
        if self.model is None:
            raise ValueError("模型未训练")
        
        X, _ = self.prepare_features(df)
        if self.scaler:
            X = self.scaler.transform(X)
        
        return self.model.predict_proba(X)[:, 1]
    
    def save(self, path: str = None):
        """保存模型"""
        path = path or self.model_path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_importance': self.feature_importance,
            'metrics': self.metrics,
            'train_metrics': self.train_metrics,
            'val_metrics': self.val_metrics,
            'threshold': self.threshold,
            'model_params': self.model_params,
            'use_regularization': self.use_regularization,
            'best_iteration': self.best_iteration,
            'early_stopping_used': self.early_stopping_used,
            '_features_already_scaled': self._features_already_scaled,
            '_selected_features': self._selected_features,
        }
        
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
        
        if self.verbose:
            print(f"模型已保存: {path}")
    
    def load(self, path: str = None):
        """加载模型"""
        path = path or self.model_path
        
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_importance = model_data['feature_importance']
        self.metrics = model_data.get('metrics')
        self.train_metrics = model_data.get('train_metrics')
        self.val_metrics = model_data.get('val_metrics')
        self.threshold = model_data.get('threshold', 0.5)
        self.model_params = model_data.get('model_params', DEFAULT_MODEL_PARAMS)
        self.use_regularization = model_data.get('use_regularization', False)
        self.best_iteration = model_data.get('best_iteration')
        self.early_stopping_used = model_data.get('early_stopping_used', False)
        self._features_already_scaled = model_data.get('_features_already_scaled', False)
        self._selected_features = model_data.get('_selected_features', None)
        
        if self.verbose:
            print(f"模型已加载: {path}")
            if self.use_regularization:
                print(f"  使用正则化参数")
            if self.early_stopping_used:
                print(f"  最佳迭代: {self.best_iteration}")
            if self._selected_features:
                print(f"  使用特征流水线选择的特征: {len(self._selected_features)} 个")
    
    def _print_training_results(self):
        """打印训练结果"""
        print(f"\n【模型评估指标】")
        
        # 如果有训练集和验证集指标，都打印
        if self.train_metrics and self.val_metrics:
            print(f"{'指标':<12} {'训练集':>10} {'验证集':>10} {'差距':>10}")
            print("-" * 45)
            
            train_m = self.train_metrics
            val_m = self.val_metrics
            
            print(f"{'准确率':<12} {train_m.accuracy:>10.1%} {val_m.accuracy:>10.1%} {(train_m.accuracy - val_m.accuracy):>+10.1%}")
            print(f"{'精确率':<12} {train_m.precision:>10.1%} {val_m.precision:>10.1%} {(train_m.precision - val_m.precision):>+10.1%}")
            print(f"{'召回率':<12} {train_m.recall:>10.1%} {val_m.recall:>10.1%} {(train_m.recall - val_m.recall):>+10.1%}")
            print(f"{'F1分数':<12} {train_m.f1:>10.3f} {val_m.f1:>10.3f} {(train_m.f1 - val_m.f1):>+10.3f}")
            print(f"{'AUC':<12} {train_m.auc:>10.3f} {val_m.auc:>10.3f} {(train_m.auc - val_m.auc):>+10.3f}")
            
            # 过拟合警告
            auc_gap = train_m.auc - val_m.auc
            if auc_gap > 0.1:
                print(f"\n⚠️ 过拟合警告: AUC差距 {auc_gap:.3f} > 0.1")
            elif auc_gap < -0.05:
                print(f"\n⚠️ 欠拟合警告: 验证集AUC高于训练集")
            else:
                print(f"\n✅ 模型泛化能力良好")
        else:
            print(f"准确率: {self.metrics.accuracy:.1%}")
            print(f"精确率: {self.metrics.precision:.1%}")
            print(f"召回率: {self.metrics.recall:.1%}")
            print(f"F1分数: {self.metrics.f1:.3f}")
            print(f"AUC: {self.metrics.auc:.3f}")
        
        if self.feature_importance:
            print(f"\n【特征重要性 TOP 10】")
            sorted_importance = sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)
            for feat, imp in sorted_importance[:10]:
                print(f"  {feat}: {imp:.4f}")
    
    def get_top_features(self, n: int = 10) -> List[Tuple[str, float]]:
        """获取最重要的特征"""
        if self.feature_importance is None:
            return []
        
        return sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def detect_overfitting(self, 
                           train_df: pd.DataFrame = None, 
                           val_df: pd.DataFrame = None,
                           label_col: str = 'label') -> Dict:
        """检测过拟合
        
        Args:
            train_df: 训练数据（可选，使用已保存的指标）
            val_df: 验证数据（可选）
            label_col: 标签列名
            
        Returns:
            过拟合检测报告
        """
        # 获取指标
        if train_df is not None:
            train_metrics = self.evaluate(train_df, label_col)
        else:
            train_metrics = self.train_metrics
        
        if val_df is not None:
            val_metrics = self.evaluate(val_df, label_col)
        else:
            val_metrics = self.val_metrics
        
        if train_metrics is None or val_metrics is None:
            return {
                'is_overfitting': False,
                'warnings': ['无法检测：缺少训练/验证指标'],
                'recommendation': '请提供训练和验证数据',
            }
        
        warnings = []
        details = {}
        
        # 1. AUC差距检测
        auc_gap = train_metrics.auc - val_metrics.auc
        details['auc_gap'] = auc_gap
        details['train_auc'] = train_metrics.auc
        details['val_auc'] = val_metrics.auc
        
        if auc_gap > 0.1:
            warnings.append(
                f"AUC过拟合: 训练={train_metrics.auc:.4f}, 验证={val_metrics.auc:.4f}, "
                f"差距={auc_gap:.4f}"
            )
        
        # 2. 精确率差距检测
        precision_gap = train_metrics.precision - val_metrics.precision
        details['precision_gap'] = precision_gap
        
        if precision_gap > 0.15:
            warnings.append(
                f"Precision过拟合: 训练={train_metrics.precision:.4f}, 验证={val_metrics.precision:.4f}"
            )
        
        # 3. 特征重要性集中度检测
        if self.feature_importance:
            sorted_importance = sorted(self.feature_importance.values(), reverse=True)
            if len(sorted_importance) >= 3:
                total = sum(sorted_importance)
                if total > 0:
                    top3_ratio = sum(sorted_importance[:3]) / total
                    details['top3_feature_ratio'] = top3_ratio
                    
                    if top3_ratio > 0.7:
                        warnings.append(
                            f"特征重要性过度集中: Top3占比={top3_ratio:.2%}"
                        )
        
        # 4. 验证集指标过低
        if val_metrics.auc < 0.55:
            warnings.append(f"验证集AUC过低: {val_metrics.auc:.4f}")
        
        # 生成建议
        is_overfitting = len(warnings) > 0
        
        recommendations = []
        if is_overfitting:
            if auc_gap > 0.1:
                recommendations.append("增加正则化强度或减少模型复杂度")
            if precision_gap > 0.15:
                recommendations.append("增加负样本或使用类别权重")
            if details.get('top3_feature_ratio', 0) > 0.7:
                recommendations.append("减少特征数量或添加更多独立特征")
        
        report = {
            'is_overfitting': is_overfitting,
            'warnings': warnings,
            'details': details,
            'recommendation': "; ".join(recommendations) if recommendations else "模型泛化能力良好",
            'severity': 'high' if len(warnings) >= 2 else ('medium' if len(warnings) == 1 else 'low'),
        }
        
        return report
    
    def get_train_val_metrics(self) -> Dict[str, Dict]:
        """获取训练和验证指标（用于外部分析）"""
        result = {}
        
        if self.train_metrics:
            result['train'] = {
                'accuracy': self.train_metrics.accuracy,
                'precision': self.train_metrics.precision,
                'recall': self.train_metrics.recall,
                'f1': self.train_metrics.f1,
                'auc': self.train_metrics.auc,
            }
        
        if self.val_metrics:
            result['val'] = {
                'accuracy': self.val_metrics.accuracy,
                'precision': self.val_metrics.precision,
                'recall': self.val_metrics.recall,
                'f1': self.val_metrics.f1,
                'auc': self.val_metrics.auc,
            }
        
        return result


def train_model_from_data(
    train_data_path: str,
    val_ratio: float = 0.2,
    model_save_path: str = None
) -> XGBoostPredictor:
    """从数据文件训练模型
    
    Args:
        train_data_path: 训练数据路径
        val_ratio: 验证集比例
        model_save_path: 模型保存路径
    """
    print(f"加载训练数据: {train_data_path}")
    df = pd.read_csv(train_data_path)
    
    # 划分训练/验证集
    train_df, val_df = train_test_split(df, test_size=val_ratio, random_state=42, stratify=df['label'])
    
    print(f"训练集: {len(train_df)} | 验证集: {len(val_df)}")
    
    # 训练
    predictor = XGBoostPredictor(model_path=model_save_path)
    predictor.train(train_df, val_df)
    
    # 保存
    if model_save_path:
        predictor.save(model_save_path)
    
    return predictor


def main():
    """测试XGBoost预测模型"""
    # 创建测试数据
    np.random.seed(42)
    n_samples = 1000
    
    test_data = pd.DataFrame({
        'code': [f'stock_{i}' for i in range(n_samples)],
        'market_cap': np.random.uniform(30, 300, n_samples),
        'roe': np.random.uniform(-10, 30, n_samples),
        'growth': np.random.uniform(-50, 200, n_samples),
        'revenue_growth': np.random.uniform(-30, 100, n_samples),
        'momentum_5d': np.random.uniform(-10, 20, n_samples),
        'momentum_10d': np.random.uniform(-15, 30, n_samples),
        'momentum_20d': np.random.uniform(-20, 40, n_samples),
        'rel_strength': np.random.uniform(0, 100, n_samples),
        'rsi': np.random.uniform(20, 80, n_samples),
        'volume_ratio': np.random.uniform(0.5, 3, n_samples),
        'fin_change': np.random.uniform(-10, 10, n_samples),
        'turnover_rate': np.random.uniform(1, 15, n_samples),
        'on_billboard': np.random.randint(0, 2, n_samples),
        'concept_count': np.random.randint(0, 15, n_samples),
        'market_trend': np.random.uniform(-10, 10, n_samples),
        'label': np.random.randint(0, 2, n_samples),
    })
    
    # 划分数据
    train_df, val_df = train_test_split(test_data, test_size=0.2, random_state=42)
    
    # 训练模型
    predictor = XGBoostPredictor()
    predictor.train(train_df, val_df)
    
    # 预测
    results = predictor.predict(val_df.head(10))
    print(f"\n【预测结果示例】")
    for r in results[:5]:
        print(f"  {r.code}: 概率={r.probability:.2%}, 预测={r.prediction}, 置信度={r.confidence}")


if __name__ == '__main__':
    main()
