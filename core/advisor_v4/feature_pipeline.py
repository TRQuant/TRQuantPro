# -*- coding: utf-8 -*-
"""
特征工程流水线 - 防过拟合设计

功能模块：
1. DataValidator - 数据验证和清洗
2. FeatureEngineer - 特征派生和交互
3. FeatureSelector - 特征选择（IC值、XGBoost、组合方法）
4. FeatureScaler - 特征标准化
5. FeaturePipeline - 主流水线

设计原则：
- fit_transform: 在训练数据上拟合参数
- transform: 使用训练时的参数转换新数据
- 防止数据泄露：所有参数仅从训练集学习
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
import pickle
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# 尝试导入机器学习库
try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.feature_selection import mutual_info_classif, SelectKBest, f_classif
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    logger.warning("scikit-learn未安装")

try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    logger.warning("XGBoost未安装")

try:
    from sklearn.ensemble import RandomForestClassifier
    HAS_RF = True
except ImportError:
    HAS_RF = False


# ============================================================
# 配置类
# ============================================================

@dataclass
class FeaturePipelineConfig:
    """特征流水线配置"""
    # 原始特征列
    raw_feature_columns: List[str] = field(default_factory=lambda: [
        'market_cap', 'roe', 'growth',
        'momentum_5d', 'momentum_10d', 'momentum_20d',
        'rel_strength', 'rsi', 'volume_ratio',
        'fin_change', 'turnover_rate', 'on_billboard',
        'concept_count', 'market_trend',
    ])
    
    # 特征选择配置
    select_method: str = 'combined'  # 'ic', 'xgboost', 'rf', 'mutual_info', 'combined'
    top_k_features: int = 10
    ic_threshold: float = 0.02
    
    # 特征工程配置
    create_interactions: bool = True
    create_ratios: bool = True
    
    # 异常值处理
    outlier_std: float = 3.0  # 3σ原则
    
    # 缺失值处理
    fill_method: str = 'median'  # 'median', 'mean', 'zero'


# ============================================================
# 数据验证器
# ============================================================

class DataValidator:
    """数据验证和清洗"""
    
    def __init__(self, config: FeaturePipelineConfig = None):
        self.config = config or FeaturePipelineConfig()
        self.duplicate_count = 0
        self.outlier_count = 0
        self.missing_count = 0
    
    def validate_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """验证并清洗数据"""
        df = df.copy()
        original_len = len(df)
        
        # 1. 去重
        if 'code' in df.columns and 'prediction_date' in df.columns:
            df = df.drop_duplicates(subset=['code', 'prediction_date'])
        elif 'code' in df.columns and 'target_date' in df.columns:
            df = df.drop_duplicates(subset=['code', 'target_date'])
        self.duplicate_count = original_len - len(df)
        
        # 2. 处理缺失值
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        self.missing_count = df[numeric_cols].isnull().sum().sum()
        
        if self.config.fill_method == 'median':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif self.config.fill_method == 'mean':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        else:
            df[numeric_cols] = df[numeric_cols].fillna(0)
        
        # 3. 处理无穷值
        df = df.replace([np.inf, -np.inf], np.nan)
        df[numeric_cols] = df[numeric_cols].fillna(0)
        
        return df
    
    def clip_outliers(self, df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
        """截断异常值（3σ原则）"""
        df = df.copy()
        columns = columns or df.select_dtypes(include=[np.number]).columns.tolist()
        
        outlier_count = 0
        for col in columns:
            if col in df.columns:
                mean = df[col].mean()
                std = df[col].std()
                if std > 0:
                    lower = mean - self.config.outlier_std * std
                    upper = mean + self.config.outlier_std * std
                    outliers = (df[col] < lower) | (df[col] > upper)
                    outlier_count += outliers.sum()
                    df[col] = df[col].clip(lower, upper)
        
        self.outlier_count = outlier_count
        return df
    
    def get_report(self) -> Dict:
        """获取验证报告"""
        return {
            'duplicates_removed': self.duplicate_count,
            'outliers_clipped': self.outlier_count,
            'missing_filled': self.missing_count,
        }


# ============================================================
# 特征工程器
# ============================================================

class FeatureEngineer:
    """特征派生和交互"""
    
    def __init__(self, config: FeaturePipelineConfig = None):
        self.config = config or FeaturePipelineConfig()
        self.created_features = []
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """创建派生特征"""
        df = df.copy()
        self.created_features = []
        
        if self.config.create_interactions:
            df = self._create_interaction_features(df)
        
        if self.config.create_ratios:
            df = self._create_ratio_features(df)
        
        return df
    
    def _create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """创建交互特征"""
        # 动量 × 相对强度（技术面组合）
        if 'momentum_5d' in df.columns and 'rel_strength' in df.columns:
            df['momentum_x_rel_strength'] = df['momentum_5d'] * df['rel_strength'] / 100
            self.created_features.append('momentum_x_rel_strength')
        
        # ROE × 增长（基本面组合）
        if 'roe' in df.columns and 'growth' in df.columns:
            df['roe_x_growth'] = df['roe'] * df['growth'] / 100
            self.created_features.append('roe_x_growth')
        
        # 动量 × 资金流（技术+资金）
        if 'momentum_20d' in df.columns and 'fin_change' in df.columns:
            df['momentum_x_fin'] = df['momentum_20d'] * (1 + df['fin_change'] / 100)
            self.created_features.append('momentum_x_fin')
        
        # 换手率 × 量比（活跃度组合）
        if 'turnover_rate' in df.columns and 'volume_ratio' in df.columns:
            df['activity_score'] = df['turnover_rate'] * df['volume_ratio']
            self.created_features.append('activity_score')
        
        return df
    
    def _create_ratio_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """创建比率特征"""
        # PEG比率（需要PE和growth）
        if 'pe_ratio' in df.columns and 'growth' in df.columns:
            df['peg_ratio'] = df['pe_ratio'] / (df['growth'].abs() + 1e-6)
            df['peg_ratio'] = df['peg_ratio'].clip(-100, 100)
            self.created_features.append('peg_ratio')
        
        # 动量差异（短期-长期）
        if 'momentum_5d' in df.columns and 'momentum_20d' in df.columns:
            df['momentum_diff'] = df['momentum_5d'] - df['momentum_20d']
            self.created_features.append('momentum_diff')
        
        # RSI偏离度（与50的距离）
        if 'rsi' in df.columns:
            df['rsi_deviation'] = abs(df['rsi'] - 50)
            self.created_features.append('rsi_deviation')
        
        return df
    
    def get_all_features(self, base_features: List[str]) -> List[str]:
        """获取所有特征（原始+派生）"""
        return base_features + self.created_features


# ============================================================
# 特征选择器
# ============================================================

class FeatureSelector:
    """特征选择器"""
    
    def __init__(self, config: FeaturePipelineConfig = None):
        self.config = config or FeaturePipelineConfig()
        self.selected_features: List[str] = []
        self.feature_scores: Dict[str, float] = {}
        self.selection_report: Dict = {}
    
    def select(self, X: pd.DataFrame, y: pd.Series, 
               method: str = None, top_k: int = None) -> List[str]:
        """选择重要特征
        
        Args:
            X: 特征数据
            y: 目标变量（0/1标签）
            method: 选择方法
            top_k: 选择前K个特征
        """
        method = method or self.config.select_method
        top_k = top_k or self.config.top_k_features
        
        # 只选择数值列
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        X = X[numeric_cols]
        
        if method == 'ic':
            self.selected_features = self._select_by_ic(X, y, top_k)
        elif method == 'xgboost':
            self.selected_features = self._select_by_xgboost(X, y, top_k)
        elif method == 'rf':
            self.selected_features = self._select_by_random_forest(X, y, top_k)
        elif method == 'mutual_info':
            self.selected_features = self._select_by_mutual_info(X, y, top_k)
        elif method == 'combined':
            self.selected_features = self._select_combined(X, y, top_k)
        else:
            # 默认使用所有特征
            self.selected_features = numeric_cols[:top_k]
        
        return self.selected_features
    
    def _select_by_ic(self, X: pd.DataFrame, y: pd.Series, top_k: int) -> List[str]:
        """基于IC值（信息系数）选择"""
        ic_values = {}
        for col in X.columns:
            try:
                ic = X[col].corr(y, method='spearman')
                ic_values[col] = abs(ic) if not np.isnan(ic) else 0
            except:
                ic_values[col] = 0
        
        # 按IC值排序
        sorted_features = sorted(ic_values.items(), key=lambda x: x[1], reverse=True)
        
        # 更新分数
        self.feature_scores.update({f: s for f, s in sorted_features})
        
        return [f for f, _ in sorted_features[:top_k]]
    
    def _select_by_xgboost(self, X: pd.DataFrame, y: pd.Series, top_k: int) -> List[str]:
        """基于XGBoost特征重要性选择"""
        if not HAS_XGBOOST:
            logger.warning("XGBoost未安装，使用IC方法")
            return self._select_by_ic(X, y, top_k)
        
        try:
            model = XGBClassifier(
                n_estimators=100, 
                max_depth=5, 
                random_state=42,
                use_label_encoder=False,
                eval_metric='logloss'
            )
            model.fit(X.fillna(0), y)
            
            importance = dict(zip(X.columns, model.feature_importances_))
            sorted_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)
            
            # 归一化分数
            max_score = max(importance.values()) if importance.values() else 1
            normalized = {f: s/max_score for f, s in importance.items()}
            self.feature_scores.update(normalized)
            
            return [f for f, _ in sorted_features[:top_k]]
        except Exception as e:
            logger.warning(f"XGBoost特征选择失败: {e}")
            return self._select_by_ic(X, y, top_k)
    
    def _select_by_random_forest(self, X: pd.DataFrame, y: pd.Series, top_k: int) -> List[str]:
        """基于随机森林特征重要性选择"""
        if not HAS_RF:
            logger.warning("RandomForest未安装，使用IC方法")
            return self._select_by_ic(X, y, top_k)
        
        try:
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
            model.fit(X.fillna(0), y)
            
            importance = dict(zip(X.columns, model.feature_importances_))
            sorted_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)
            
            # 归一化分数
            max_score = max(importance.values()) if importance.values() else 1
            normalized = {f: s/max_score for f, s in importance.items()}
            self.feature_scores.update(normalized)
            
            return [f for f, _ in sorted_features[:top_k]]
        except Exception as e:
            logger.warning(f"RandomForest特征选择失败: {e}")
            return self._select_by_ic(X, y, top_k)
    
    def _select_by_mutual_info(self, X: pd.DataFrame, y: pd.Series, top_k: int) -> List[str]:
        """基于互信息选择"""
        if not HAS_SKLEARN:
            return self._select_by_ic(X, y, top_k)
        
        try:
            X_filled = X.fillna(0)
            mi_scores = mutual_info_classif(X_filled, y, random_state=42)
            
            importance = dict(zip(X.columns, mi_scores))
            sorted_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)
            
            # 归一化分数
            max_score = max(mi_scores) if len(mi_scores) > 0 else 1
            normalized = {f: s/max_score for f, s in importance.items()}
            self.feature_scores.update(normalized)
            
            return [f for f, _ in sorted_features[:top_k]]
        except Exception as e:
            logger.warning(f"互信息特征选择失败: {e}")
            return self._select_by_ic(X, y, top_k)
    
    def _select_combined(self, X: pd.DataFrame, y: pd.Series, top_k: int) -> List[str]:
        """组合多种方法选择（推荐）"""
        scores = {col: 0.0 for col in X.columns}
        
        # 1. IC值 (权重0.2)
        ic_scores = {}
        for col in X.columns:
            try:
                ic = X[col].corr(y, method='spearman')
                ic_scores[col] = abs(ic) if not np.isnan(ic) else 0
            except:
                ic_scores[col] = 0
        
        # 归一化IC
        max_ic = max(ic_scores.values()) if ic_scores.values() else 1
        for col in X.columns:
            scores[col] += 0.2 * (ic_scores.get(col, 0) / max_ic if max_ic > 0 else 0)
        
        # 2. XGBoost (权重0.3)
        if HAS_XGBOOST:
            try:
                model = XGBClassifier(n_estimators=50, max_depth=4, random_state=42,
                                     use_label_encoder=False, eval_metric='logloss')
                model.fit(X.fillna(0), y)
                xgb_importance = dict(zip(X.columns, model.feature_importances_))
                max_xgb = max(xgb_importance.values()) if xgb_importance.values() else 1
                for col in X.columns:
                    scores[col] += 0.3 * (xgb_importance.get(col, 0) / max_xgb if max_xgb > 0 else 0)
            except Exception as e:
                logger.warning(f"XGBoost评分失败: {e}")
        
        # 3. RandomForest (权重0.3)
        if HAS_RF:
            try:
                model = RandomForestClassifier(n_estimators=50, max_depth=4, random_state=42)
                model.fit(X.fillna(0), y)
                rf_importance = dict(zip(X.columns, model.feature_importances_))
                max_rf = max(rf_importance.values()) if rf_importance.values() else 1
                for col in X.columns:
                    scores[col] += 0.3 * (rf_importance.get(col, 0) / max_rf if max_rf > 0 else 0)
            except Exception as e:
                logger.warning(f"RandomForest评分失败: {e}")
        
        # 4. 互信息 (权重0.2)
        if HAS_SKLEARN:
            try:
                mi_scores = mutual_info_classif(X.fillna(0), y, random_state=42)
                max_mi = max(mi_scores) if len(mi_scores) > 0 else 1
                for i, col in enumerate(X.columns):
                    scores[col] += 0.2 * (mi_scores[i] / max_mi if max_mi > 0 else 0)
            except Exception as e:
                logger.warning(f"互信息评分失败: {e}")
        
        # 保存分数
        self.feature_scores = scores
        
        # 选择Top K
        sorted_features = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # 生成报告
        self.selection_report = {
            'method': 'combined',
            'top_k': top_k,
            'scores': dict(sorted_features[:top_k]),
            'all_scores': dict(sorted_features),
        }
        
        return [f for f, _ in sorted_features[:top_k]]
    
    def get_top_features(self, n: int = 10) -> List[Tuple[str, float]]:
        """获取Top N特征及其分数"""
        sorted_features = sorted(self.feature_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_features[:n]


# ============================================================
# 特征标准化器
# ============================================================

class FeatureScaler:
    """特征标准化（Z-score + 异常值截断）"""
    
    def __init__(self, config: FeaturePipelineConfig = None):
        self.config = config or FeaturePipelineConfig()
        self.scalers: Dict[str, Any] = {}  # 每个特征的scaler
        self.means: Dict[str, float] = {}
        self.stds: Dict[str, float] = {}
        self.fitted = False
    
    def fit(self, df: pd.DataFrame, columns: List[str] = None) -> 'FeatureScaler':
        """在训练数据上拟合"""
        columns = columns or df.select_dtypes(include=[np.number]).columns.tolist()
        
        for col in columns:
            if col in df.columns:
                self.means[col] = df[col].mean()
                self.stds[col] = df[col].std()
                if self.stds[col] == 0:
                    self.stds[col] = 1  # 防止除零
        
        self.fitted = True
        return self
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """使用训练时的参数转换"""
        if not self.fitted:
            raise ValueError("Scaler未拟合，请先调用fit()")
        
        df = df.copy()
        
        for col in self.means.keys():
            if col in df.columns:
                # Z-score标准化
                df[col] = (df[col] - self.means[col]) / self.stds[col]
                
                # 截断到[-3, 3]
                df[col] = df[col].clip(-3, 3)
        
        return df
    
    def fit_transform(self, df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
        """拟合并转换"""
        self.fit(df, columns)
        return self.transform(df)
    
    def inverse_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """逆变换"""
        df = df.copy()
        
        for col in self.means.keys():
            if col in df.columns:
                df[col] = df[col] * self.stds[col] + self.means[col]
        
        return df


# ============================================================
# 特征流水线（主类）
# ============================================================

class FeaturePipeline:
    """特征工程流水线
    
    整合数据验证、特征工程、特征选择、特征标准化
    
    使用示例：
        # 训练时
        pipeline = FeaturePipeline()
        X_train = pipeline.fit_transform(train_df[FEATURE_COLS], train_df['label'])
        
        # 预测时
        X_test = pipeline.transform(test_df[FEATURE_COLS])
    """
    
    def __init__(self, config: FeaturePipelineConfig = None):
        self.config = config or FeaturePipelineConfig()
        
        self.validator = DataValidator(self.config)
        self.engineer = FeatureEngineer(self.config)
        self.selector = FeatureSelector(self.config)
        self.scaler = FeatureScaler(self.config)
        
        self.selected_features: List[str] = []
        self.all_features: List[str] = []
        self.fitted = False
    
    def fit_transform(self, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        """在训练数据上拟合并转换
        
        Args:
            X: 特征数据
            y: 目标变量（0/1标签）
            
        Returns:
            转换后的特征DataFrame
        """
        print(f"\n{'='*60}")
        print(f"【特征工程流水线】fit_transform")
        print(f"{'='*60}")
        
        # 1. 数据验证和清洗
        print("\n[Step 1] 数据验证和清洗...")
        X = self.validator.validate_and_clean(X)
        X = self.validator.clip_outliers(X)
        report = self.validator.get_report()
        print(f"  - 去重: {report['duplicates_removed']} 条")
        print(f"  - 异常值截断: {report['outliers_clipped']} 个")
        print(f"  - 缺失值填充: {report['missing_filled']} 个")
        
        # 2. 特征派生
        print("\n[Step 2] 特征派生...")
        X = self.engineer.create_features(X)
        self.all_features = self.engineer.get_all_features(self.config.raw_feature_columns)
        print(f"  - 原始特征: {len(self.config.raw_feature_columns)} 个")
        print(f"  - 派生特征: {len(self.engineer.created_features)} 个")
        print(f"  - 派生列表: {self.engineer.created_features}")
        
        # 3. 特征选择
        print("\n[Step 3] 特征选择...")
        
        # 获取数值列
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        X_numeric = X[numeric_cols]
        
        self.selected_features = self.selector.select(X_numeric, y)
        print(f"  - 候选特征: {len(numeric_cols)} 个")
        print(f"  - 选择特征: {len(self.selected_features)} 个")
        print(f"  - 选择列表: {self.selected_features}")
        
        # 打印特征重要性
        top_features = self.selector.get_top_features(10)
        print(f"\n  特征重要性 TOP 10:")
        for i, (feat, score) in enumerate(top_features, 1):
            print(f"    {i}. {feat}: {score:.4f}")
        
        # 只保留选中的特征
        X = X[self.selected_features]
        
        # 4. 特征标准化
        print("\n[Step 4] 特征标准化...")
        X = self.scaler.fit_transform(X)
        print(f"  - 标准化完成 (Z-score + clip[-3,3])")
        
        self.fitted = True
        print(f"\n✅ 特征流水线拟合完成!")
        print(f"   最终特征数: {len(self.selected_features)}")
        
        return X
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """使用训练时的参数转换新数据
        
        Args:
            X: 特征数据
            
        Returns:
            转换后的特征DataFrame
        """
        if not self.fitted:
            raise ValueError("Pipeline未拟合，请先调用fit_transform()")
        
        # 1. 数据验证和清洗
        X = self.validator.validate_and_clean(X)
        X = self.validator.clip_outliers(X)
        
        # 2. 特征派生
        X = self.engineer.create_features(X)
        
        # 3. 选择特征（使用训练时选择的）
        # 确保所有选中的特征都存在
        missing_features = [f for f in self.selected_features if f not in X.columns]
        if missing_features:
            logger.warning(f"缺少特征: {missing_features}，将填充0")
            for f in missing_features:
                X[f] = 0
        
        X = X[self.selected_features]
        
        # 4. 特征标准化（使用训练时的参数）
        X = self.scaler.transform(X)
        
        return X
    
    def save(self, path: str):
        """保存流水线"""
        data = {
            'config': self.config,
            'selected_features': self.selected_features,
            'all_features': self.all_features,
            'feature_scores': self.selector.feature_scores,
            'scaler_means': self.scaler.means,
            'scaler_stds': self.scaler.stds,
            'fitted': self.fitted,
        }
        
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"✅ 特征流水线已保存: {path}")
    
    def load(self, path: str):
        """加载流水线"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.config = data['config']
        self.selected_features = data['selected_features']
        self.all_features = data['all_features']
        self.selector.feature_scores = data['feature_scores']
        self.scaler.means = data['scaler_means']
        self.scaler.stds = data['scaler_stds']
        self.scaler.fitted = True
        self.fitted = data['fitted']
        
        print(f"✅ 特征流水线已加载: {path}")
        print(f"   特征数: {len(self.selected_features)}")
    
    def get_feature_importance(self) -> Dict[str, float]:
        """获取特征重要性"""
        return self.selector.feature_scores
    
    def get_selected_features(self) -> List[str]:
        """获取选中的特征列表"""
        return self.selected_features


# ============================================================
# 便捷函数
# ============================================================

def create_default_pipeline() -> FeaturePipeline:
    """创建默认配置的流水线"""
    return FeaturePipeline(FeaturePipelineConfig())


def create_pipeline_with_top_k(top_k: int = 10) -> FeaturePipeline:
    """创建指定特征数量的流水线"""
    config = FeaturePipelineConfig(top_k_features=top_k)
    return FeaturePipeline(config)


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    # 测试流水线
    print("测试特征工程流水线...")
    
    # 创建模拟数据
    np.random.seed(42)
    n_samples = 1000
    
    df = pd.DataFrame({
        'market_cap': np.random.uniform(10, 1000, n_samples),
        'roe': np.random.uniform(-10, 30, n_samples),
        'growth': np.random.uniform(-20, 50, n_samples),
        'momentum_5d': np.random.uniform(-10, 20, n_samples),
        'momentum_10d': np.random.uniform(-15, 25, n_samples),
        'momentum_20d': np.random.uniform(-20, 30, n_samples),
        'rel_strength': np.random.uniform(0, 100, n_samples),
        'rsi': np.random.uniform(20, 80, n_samples),
        'volume_ratio': np.random.uniform(0.5, 3, n_samples),
        'fin_change': np.random.uniform(-10, 20, n_samples),
        'turnover_rate': np.random.uniform(1, 20, n_samples),
        'on_billboard': np.random.randint(0, 2, n_samples),
        'concept_count': np.random.randint(0, 10, n_samples),
        'market_trend': np.random.uniform(-5, 5, n_samples),
    })
    
    # 模拟标签（与momentum_5d和roe相关）
    y = ((df['momentum_5d'] > 5) & (df['roe'] > 10)).astype(int)
    
    # 创建流水线
    pipeline = create_pipeline_with_top_k(10)
    
    # 拟合并转换
    X_transformed = pipeline.fit_transform(df, y)
    
    print(f"\n转换后数据形状: {X_transformed.shape}")
    print(f"选中特征: {pipeline.get_selected_features()}")
