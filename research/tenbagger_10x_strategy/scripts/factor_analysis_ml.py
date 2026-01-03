#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
因子分析与机器学习模块
====================

功能:
1. 因子有效性检验（IC值、IR值）
2. 机器学习特征工程
3. 模型训练与验证（训练集/验证集）
4. 因子组合优化

代码位置: research/tenbagger_10x_strategy/scripts/factor_analysis_ml.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import pickle

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning("XGBoost not available, using GradientBoostingRegressor")

# ============================================================
# 因子有效性检验
# ============================================================

class FactorAnalyzer:
    """因子分析器"""
    
    def __init__(self):
        self.ic_results = {}
        self.ir_results = {}
    
    def calculate_ic(self, factor: pd.Series, forward_return: pd.Series) -> float:
        """
        计算信息系数（IC）
        IC = corr(factor, forward_return)
        """
        if len(factor) != len(forward_return):
            return np.nan
        
        # 对齐索引
        aligned = pd.DataFrame({'factor': factor, 'return': forward_return}).dropna()
        if len(aligned) < 10:
            return np.nan
        
        ic = aligned['factor'].corr(aligned['return'])
        return ic
    
    def calculate_ir(self, ic_series: pd.Series) -> float:
        """
        计算信息比率（IR）
        IR = mean(IC) / std(IC)
        """
        if len(ic_series) < 2:
            return np.nan
        
        mean_ic = ic_series.mean()
        std_ic = ic_series.std()
        
        if std_ic == 0:
            return np.nan
        
        ir = mean_ic / std_ic
        return ir
    
    def analyze_factor(self, factor_data: pd.DataFrame, return_data: pd.DataFrame, 
                      factor_name: str, forward_periods: list = [5, 10, 20]) -> dict:
        """
        分析单个因子的有效性
        
        Args:
            factor_data: 因子数据，index为日期，columns为股票代码
            return_data: 收益率数据，index为日期，columns为股票代码
            factor_name: 因子名称
            forward_periods: 前瞻期列表
        """
        results = {
            'factor_name': factor_name,
            'ic_mean': {},
            'ic_std': {},
            'ic_ir': {},
            'ic_positive_ratio': {}
        }
        
        # 对齐日期
        common_dates = factor_data.index.intersection(return_data.index)
        if len(common_dates) < 20:
            return results
        
        ic_series_list = {}
        
        for period in forward_periods:
            ic_values = []
            
            for date in common_dates[:-period]:
                try:
                    factor_values = factor_data.loc[date]
                    forward_returns = return_data.loc[date:].iloc[period] if date in return_data.index else None
                    
                    if forward_returns is None:
                        continue
                    
                    # 对齐股票代码
                    common_stocks = factor_values.index.intersection(forward_returns.index)
                    if len(common_stocks) < 10:
                        continue
                    
                    factor_aligned = factor_values[common_stocks]
                    return_aligned = forward_returns[common_stocks]
                    
                    # 计算IC
                    ic = self.calculate_ic(factor_aligned, return_aligned)
                    if not np.isnan(ic):
                        ic_values.append(ic)
                
                except Exception as e:
                    continue
            
            if len(ic_values) > 0:
                ic_series = pd.Series(ic_values)
                results['ic_mean'][period] = float(ic_series.mean())
                results['ic_std'][period] = float(ic_series.std())
                results['ic_ir'][period] = float(self.calculate_ir(ic_series))
                results['ic_positive_ratio'][period] = float((ic_series > 0).sum() / len(ic_series))
                ic_series_list[period] = ic_series
        
        return results

# ============================================================
# 机器学习特征工程
# ============================================================

class FeatureEngineer:
    """特征工程器"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []
    
    def create_features(self, fundamentals: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
        """
        创建特征矩阵
        
        Args:
            fundamentals: 基本面数据
            prices: 价格数据
        """
        features_list = []
        
        # 对齐日期和股票
        common_dates = fundamentals.index.intersection(prices.index)
        common_stocks = fundamentals.columns.intersection(prices.columns)
        
        for date in common_dates:
            feature_dict = {}
            
            # 基本面特征
            for stock in common_stocks:
                if stock not in fundamentals.columns or stock not in prices.columns:
                    continue
                
                fund = fundamentals.loc[date, stock] if isinstance(fundamentals.loc[date], pd.Series) else fundamentals.loc[date]
                price = prices.loc[date, stock] if isinstance(prices.loc[date], pd.Series) else prices.loc[date]
                
                if pd.isna(fund) or pd.isna(price):
                    continue
                
                # 估值特征
                feature_dict[f'{stock}_pe'] = fund.get('pe_ratio', np.nan)
                feature_dict[f'{stock}_pb'] = fund.get('pb_ratio', np.nan)
                feature_dict[f'{stock}_market_cap'] = fund.get('market_cap', np.nan)
                
                # 质量特征
                feature_dict[f'{stock}_roe'] = fund.get('roe', np.nan)
                feature_dict[f'{stock}_roa'] = fund.get('roa', np.nan)
                
                # 成长特征
                feature_dict[f'{stock}_revenue_growth'] = fund.get('revenue_growth', np.nan)
                feature_dict[f'{stock}_profit_growth'] = fund.get('profit_growth', np.nan)
                
                # 价格特征
                if isinstance(price, dict):
                    feature_dict[f'{stock}_close'] = price.get('close', np.nan)
                    feature_dict[f'{stock}_volume'] = price.get('volume', np.nan)
            
            if feature_dict:
                feature_dict['date'] = date
                features_list.append(feature_dict)
        
        if not features_list:
            return pd.DataFrame()
        
        features_df = pd.DataFrame(features_list)
        features_df.set_index('date', inplace=True)
        
        return features_df
    
    def normalize_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """标准化特征"""
        if features.empty:
            return features
        
        # 只标准化数值列
        numeric_cols = features.select_dtypes(include=[np.number]).columns
        features_normalized = features.copy()
        features_normalized[numeric_cols] = self.scaler.fit_transform(features[numeric_cols])
        
        return features_normalized

# ============================================================
# 机器学习模型
# ============================================================

class MLModel:
    """机器学习模型"""
    
    def __init__(self, model_type: str = 'xgboost'):
        self.model_type = model_type
        self.model = None
        self.feature_importance = None
        self.scaler = StandardScaler()
        
        if model_type == 'xgboost' and XGBOOST_AVAILABLE:
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            )
        elif model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        else:
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """训练模型"""
        # 标准化
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # 训练
        self.model.fit(X_train_scaled, y_train)
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=X_train.columns
            ).sort_values(ascending=False)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """预测"""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """评估模型"""
        y_pred = self.predict(X)
        
        mse = mean_squared_error(y, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y, y_pred)
        
        # IC值
        ic = np.corrcoef(y, y_pred)[0, 1]
        
        return {
            'mse': float(mse),
            'rmse': float(rmse),
            'r2': float(r2),
            'ic': float(ic) if not np.isnan(ic) else 0.0
        }
    
    def save(self, path: str):
        """保存模型"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'model_type': self.model_type
            }, f)
    
    def load(self, path: str):
        """加载模型"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_importance = data.get('feature_importance')
            self.model_type = data.get('model_type', 'xgboost')

# ============================================================
# 数据集划分
# ============================================================

class DataSplitter:
    """数据集划分器（时间序列）"""
    
    @staticmethod
    def split_time_series(data: pd.DataFrame, train_ratio: float = 0.7) -> tuple:
        """
        按时间序列划分训练集和验证集
        
        Args:
            data: 数据，index为日期
            train_ratio: 训练集比例
        """
        if data.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        sorted_dates = sorted(data.index)
        split_idx = int(len(sorted_dates) * train_ratio)
        
        train_dates = sorted_dates[:split_idx]
        val_dates = sorted_dates[split_idx:]
        
        train_data = data.loc[train_dates]
        val_data = data.loc[val_dates]
        
        return train_data, val_data
    
    @staticmethod
    def time_series_cv(data: pd.DataFrame, n_splits: int = 5) -> list:
        """
        时间序列交叉验证
        
        Returns:
            [(train_idx, val_idx), ...]
        """
        tscv = TimeSeriesSplit(n_splits=n_splits)
        splits = []
        
        for train_idx, val_idx in tscv.split(data):
            splits.append((train_idx, val_idx))
        
        return splits

# ============================================================
# 因子组合优化
# ============================================================

class FactorOptimizer:
    """因子组合优化器"""
    
    def __init__(self):
        self.best_factors = []
        self.factor_weights = {}
    
    def optimize_combination(self, factor_data: dict, return_data: pd.DataFrame, 
                           method: str = 'ic_weighted') -> dict:
        """
        优化因子组合
        
        Args:
            factor_data: {factor_name: factor_df}
            return_data: 收益率数据
            method: 优化方法 ('ic_weighted', 'ml_selected')
        """
        if method == 'ic_weighted':
            return self._ic_weighted_optimization(factor_data, return_data)
        elif method == 'ml_selected':
            return self._ml_selected_optimization(factor_data, return_data)
        else:
            return {}
    
    def _ic_weighted_optimization(self, factor_data: dict, return_data: pd.DataFrame) -> dict:
        """基于IC值的加权优化"""
        analyzer = FactorAnalyzer()
        factor_ics = {}
        
        for factor_name, factor_df in factor_data.items():
            results = analyzer.analyze_factor(factor_df, return_data, factor_name)
            # 使用平均IC值
            avg_ic = np.mean(list(results.get('ic_mean', {}).values()))
            if not np.isnan(avg_ic):
                factor_ics[factor_name] = abs(avg_ic)
        
        # 归一化权重
        total_ic = sum(factor_ics.values())
        if total_ic > 0:
            weights = {k: v / total_ic for k, v in factor_ics.items()}
        else:
            weights = {k: 1.0 / len(factor_ics) for k in factor_ics.keys()}
        
        return {
            'weights': weights,
            'factors': list(factor_ics.keys()),
            'method': 'ic_weighted'
        }
    
    def _ml_selected_optimization(self, factor_data: dict, return_data: pd.DataFrame) -> dict:
        """基于机器学习的选择优化"""
        # 简化实现：使用随机森林选择重要因子
        # 实际应用中可以使用更复杂的特征选择方法
        
        # 合并所有因子
        all_factors = pd.DataFrame()
        for factor_name, factor_df in factor_data.items():
            if all_factors.empty:
                all_factors = factor_df.copy()
                all_factors.columns = [f'{factor_name}_{col}' for col in all_factors.columns]
            else:
                factor_df_renamed = factor_df.copy()
                factor_df_renamed.columns = [f'{factor_name}_{col}' for col in factor_df_renamed.columns]
                all_factors = all_factors.join(factor_df_renamed, how='outer')
        
        # 对齐收益率
        common_dates = all_factors.index.intersection(return_data.index)
        if len(common_dates) < 50:
            return {}
        
        # 准备数据
        X = all_factors.loc[common_dates].fillna(0)
        y = return_data.loc[common_dates].mean(axis=1)  # 使用平均收益率作为目标
        
        # 训练模型
        model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
        model.fit(X, y)
        
        # 获取特征重要性
        importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        
        # 选择top因子
        top_n = min(10, len(importance))
        top_factors = importance.head(top_n).index.tolist()
        
        # 计算权重
        weights = {}
        for factor_name in factor_data.keys():
            factor_cols = [col for col in top_factors if col.startswith(factor_name)]
            if factor_cols:
                weights[factor_name] = importance[factor_cols].sum() / importance.sum()
        
        return {
            'weights': weights,
            'factors': list(weights.keys()),
            'method': 'ml_selected',
            'feature_importance': importance.to_dict()
        }

# ============================================================
# 主函数
# ============================================================

def main():
    """示例用法"""
    print("=" * 80)
    print("因子分析与机器学习模块")
    print("=" * 80)
    
    # 这里可以添加具体的测试代码
    print("✅ 模块加载成功")
    print("   功能:")
    print("   1. 因子有效性检验（IC值、IR值）")
    print("   2. 机器学习特征工程")
    print("   3. 模型训练与验证")
    print("   4. 因子组合优化")

if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
因子分析与机器学习模块
====================

功能:
1. 因子有效性检验（IC值、IR值）
2. 机器学习特征工程
3. 模型训练与验证（训练集/验证集）
4. 因子组合优化

代码位置: research/tenbagger_10x_strategy/scripts/factor_analysis_ml.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import pickle

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning("XGBoost not available, using GradientBoostingRegressor")

# ============================================================
# 因子有效性检验
# ============================================================

class FactorAnalyzer:
    """因子分析器"""
    
    def __init__(self):
        self.ic_results = {}
        self.ir_results = {}
    
    def calculate_ic(self, factor: pd.Series, forward_return: pd.Series) -> float:
        """
        计算信息系数（IC）
        IC = corr(factor, forward_return)
        """
        if len(factor) != len(forward_return):
            return np.nan
        
        # 对齐索引
        aligned = pd.DataFrame({'factor': factor, 'return': forward_return}).dropna()
        if len(aligned) < 10:
            return np.nan
        
        ic = aligned['factor'].corr(aligned['return'])
        return ic
    
    def calculate_ir(self, ic_series: pd.Series) -> float:
        """
        计算信息比率（IR）
        IR = mean(IC) / std(IC)
        """
        if len(ic_series) < 2:
            return np.nan
        
        mean_ic = ic_series.mean()
        std_ic = ic_series.std()
        
        if std_ic == 0:
            return np.nan
        
        ir = mean_ic / std_ic
        return ir
    
    def analyze_factor(self, factor_data: pd.DataFrame, return_data: pd.DataFrame, 
                      factor_name: str, forward_periods: list = [5, 10, 20]) -> dict:
        """
        分析单个因子的有效性
        
        Args:
            factor_data: 因子数据，index为日期，columns为股票代码
            return_data: 收益率数据，index为日期，columns为股票代码
            factor_name: 因子名称
            forward_periods: 前瞻期列表
        """
        results = {
            'factor_name': factor_name,
            'ic_mean': {},
            'ic_std': {},
            'ic_ir': {},
            'ic_positive_ratio': {}
        }
        
        # 对齐日期
        common_dates = factor_data.index.intersection(return_data.index)
        if len(common_dates) < 20:
            return results
        
        ic_series_list = {}
        
        for period in forward_periods:
            ic_values = []
            
            for date in common_dates[:-period]:
                try:
                    factor_values = factor_data.loc[date]
                    forward_returns = return_data.loc[date:].iloc[period] if date in return_data.index else None
                    
                    if forward_returns is None:
                        continue
                    
                    # 对齐股票代码
                    common_stocks = factor_values.index.intersection(forward_returns.index)
                    if len(common_stocks) < 10:
                        continue
                    
                    factor_aligned = factor_values[common_stocks]
                    return_aligned = forward_returns[common_stocks]
                    
                    # 计算IC
                    ic = self.calculate_ic(factor_aligned, return_aligned)
                    if not np.isnan(ic):
                        ic_values.append(ic)
                
                except Exception as e:
                    continue
            
            if len(ic_values) > 0:
                ic_series = pd.Series(ic_values)
                results['ic_mean'][period] = float(ic_series.mean())
                results['ic_std'][period] = float(ic_series.std())
                results['ic_ir'][period] = float(self.calculate_ir(ic_series))
                results['ic_positive_ratio'][period] = float((ic_series > 0).sum() / len(ic_series))
                ic_series_list[period] = ic_series
        
        return results

# ============================================================
# 机器学习特征工程
# ============================================================

class FeatureEngineer:
    """特征工程器"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []
    
    def create_features(self, fundamentals: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
        """
        创建特征矩阵
        
        Args:
            fundamentals: 基本面数据
            prices: 价格数据
        """
        features_list = []
        
        # 对齐日期和股票
        common_dates = fundamentals.index.intersection(prices.index)
        common_stocks = fundamentals.columns.intersection(prices.columns)
        
        for date in common_dates:
            feature_dict = {}
            
            # 基本面特征
            for stock in common_stocks:
                if stock not in fundamentals.columns or stock not in prices.columns:
                    continue
                
                fund = fundamentals.loc[date, stock] if isinstance(fundamentals.loc[date], pd.Series) else fundamentals.loc[date]
                price = prices.loc[date, stock] if isinstance(prices.loc[date], pd.Series) else prices.loc[date]
                
                if pd.isna(fund) or pd.isna(price):
                    continue
                
                # 估值特征
                feature_dict[f'{stock}_pe'] = fund.get('pe_ratio', np.nan)
                feature_dict[f'{stock}_pb'] = fund.get('pb_ratio', np.nan)
                feature_dict[f'{stock}_market_cap'] = fund.get('market_cap', np.nan)
                
                # 质量特征
                feature_dict[f'{stock}_roe'] = fund.get('roe', np.nan)
                feature_dict[f'{stock}_roa'] = fund.get('roa', np.nan)
                
                # 成长特征
                feature_dict[f'{stock}_revenue_growth'] = fund.get('revenue_growth', np.nan)
                feature_dict[f'{stock}_profit_growth'] = fund.get('profit_growth', np.nan)
                
                # 价格特征
                if isinstance(price, dict):
                    feature_dict[f'{stock}_close'] = price.get('close', np.nan)
                    feature_dict[f'{stock}_volume'] = price.get('volume', np.nan)
            
            if feature_dict:
                feature_dict['date'] = date
                features_list.append(feature_dict)
        
        if not features_list:
            return pd.DataFrame()
        
        features_df = pd.DataFrame(features_list)
        features_df.set_index('date', inplace=True)
        
        return features_df
    
    def normalize_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """标准化特征"""
        if features.empty:
            return features
        
        # 只标准化数值列
        numeric_cols = features.select_dtypes(include=[np.number]).columns
        features_normalized = features.copy()
        features_normalized[numeric_cols] = self.scaler.fit_transform(features[numeric_cols])
        
        return features_normalized

# ============================================================
# 机器学习模型
# ============================================================

class MLModel:
    """机器学习模型"""
    
    def __init__(self, model_type: str = 'xgboost'):
        self.model_type = model_type
        self.model = None
        self.feature_importance = None
        self.scaler = StandardScaler()
        
        if model_type == 'xgboost' and XGBOOST_AVAILABLE:
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            )
        elif model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        else:
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """训练模型"""
        # 标准化
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # 训练
        self.model.fit(X_train_scaled, y_train)
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=X_train.columns
            ).sort_values(ascending=False)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """预测"""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """评估模型"""
        y_pred = self.predict(X)
        
        mse = mean_squared_error(y, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y, y_pred)
        
        # IC值
        ic = np.corrcoef(y, y_pred)[0, 1]
        
        return {
            'mse': float(mse),
            'rmse': float(rmse),
            'r2': float(r2),
            'ic': float(ic) if not np.isnan(ic) else 0.0
        }
    
    def save(self, path: str):
        """保存模型"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'model_type': self.model_type
            }, f)
    
    def load(self, path: str):
        """加载模型"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_importance = data.get('feature_importance')
            self.model_type = data.get('model_type', 'xgboost')

# ============================================================
# 数据集划分
# ============================================================

class DataSplitter:
    """数据集划分器（时间序列）"""
    
    @staticmethod
    def split_time_series(data: pd.DataFrame, train_ratio: float = 0.7) -> tuple:
        """
        按时间序列划分训练集和验证集
        
        Args:
            data: 数据，index为日期
            train_ratio: 训练集比例
        """
        if data.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        sorted_dates = sorted(data.index)
        split_idx = int(len(sorted_dates) * train_ratio)
        
        train_dates = sorted_dates[:split_idx]
        val_dates = sorted_dates[split_idx:]
        
        train_data = data.loc[train_dates]
        val_data = data.loc[val_dates]
        
        return train_data, val_data
    
    @staticmethod
    def time_series_cv(data: pd.DataFrame, n_splits: int = 5) -> list:
        """
        时间序列交叉验证
        
        Returns:
            [(train_idx, val_idx), ...]
        """
        tscv = TimeSeriesSplit(n_splits=n_splits)
        splits = []
        
        for train_idx, val_idx in tscv.split(data):
            splits.append((train_idx, val_idx))
        
        return splits

# ============================================================
# 因子组合优化
# ============================================================

class FactorOptimizer:
    """因子组合优化器"""
    
    def __init__(self):
        self.best_factors = []
        self.factor_weights = {}
    
    def optimize_combination(self, factor_data: dict, return_data: pd.DataFrame, 
                           method: str = 'ic_weighted') -> dict:
        """
        优化因子组合
        
        Args:
            factor_data: {factor_name: factor_df}
            return_data: 收益率数据
            method: 优化方法 ('ic_weighted', 'ml_selected')
        """
        if method == 'ic_weighted':
            return self._ic_weighted_optimization(factor_data, return_data)
        elif method == 'ml_selected':
            return self._ml_selected_optimization(factor_data, return_data)
        else:
            return {}
    
    def _ic_weighted_optimization(self, factor_data: dict, return_data: pd.DataFrame) -> dict:
        """基于IC值的加权优化"""
        analyzer = FactorAnalyzer()
        factor_ics = {}
        
        for factor_name, factor_df in factor_data.items():
            results = analyzer.analyze_factor(factor_df, return_data, factor_name)
            # 使用平均IC值
            avg_ic = np.mean(list(results.get('ic_mean', {}).values()))
            if not np.isnan(avg_ic):
                factor_ics[factor_name] = abs(avg_ic)
        
        # 归一化权重
        total_ic = sum(factor_ics.values())
        if total_ic > 0:
            weights = {k: v / total_ic for k, v in factor_ics.items()}
        else:
            weights = {k: 1.0 / len(factor_ics) for k in factor_ics.keys()}
        
        return {
            'weights': weights,
            'factors': list(factor_ics.keys()),
            'method': 'ic_weighted'
        }
    
    def _ml_selected_optimization(self, factor_data: dict, return_data: pd.DataFrame) -> dict:
        """基于机器学习的选择优化"""
        # 简化实现：使用随机森林选择重要因子
        # 实际应用中可以使用更复杂的特征选择方法
        
        # 合并所有因子
        all_factors = pd.DataFrame()
        for factor_name, factor_df in factor_data.items():
            if all_factors.empty:
                all_factors = factor_df.copy()
                all_factors.columns = [f'{factor_name}_{col}' for col in all_factors.columns]
            else:
                factor_df_renamed = factor_df.copy()
                factor_df_renamed.columns = [f'{factor_name}_{col}' for col in factor_df_renamed.columns]
                all_factors = all_factors.join(factor_df_renamed, how='outer')
        
        # 对齐收益率
        common_dates = all_factors.index.intersection(return_data.index)
        if len(common_dates) < 50:
            return {}
        
        # 准备数据
        X = all_factors.loc[common_dates].fillna(0)
        y = return_data.loc[common_dates].mean(axis=1)  # 使用平均收益率作为目标
        
        # 训练模型
        model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
        model.fit(X, y)
        
        # 获取特征重要性
        importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        
        # 选择top因子
        top_n = min(10, len(importance))
        top_factors = importance.head(top_n).index.tolist()
        
        # 计算权重
        weights = {}
        for factor_name in factor_data.keys():
            factor_cols = [col for col in top_factors if col.startswith(factor_name)]
            if factor_cols:
                weights[factor_name] = importance[factor_cols].sum() / importance.sum()
        
        return {
            'weights': weights,
            'factors': list(weights.keys()),
            'method': 'ml_selected',
            'feature_importance': importance.to_dict()
        }

# ============================================================
# 主函数
# ============================================================

def main():
    """示例用法"""
    print("=" * 80)
    print("因子分析与机器学习模块")
    print("=" * 80)
    
    # 这里可以添加具体的测试代码
    print("✅ 模块加载成功")
    print("   功能:")
    print("   1. 因子有效性检验（IC值、IR值）")
    print("   2. 机器学习特征工程")
    print("   3. 模型训练与验证")
    print("   4. 因子组合优化")

if __name__ == "__main__":
    main()






















# -*- coding: utf-8 -*-
"""
因子分析与机器学习模块
====================

功能:
1. 因子有效性检验（IC值、IR值）
2. 机器学习特征工程
3. 模型训练与验证（训练集/验证集）
4. 因子组合优化

代码位置: research/tenbagger_10x_strategy/scripts/factor_analysis_ml.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import pickle

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning("XGBoost not available, using GradientBoostingRegressor")

# ============================================================
# 因子有效性检验
# ============================================================

class FactorAnalyzer:
    """因子分析器"""
    
    def __init__(self):
        self.ic_results = {}
        self.ir_results = {}
    
    def calculate_ic(self, factor: pd.Series, forward_return: pd.Series) -> float:
        """
        计算信息系数（IC）
        IC = corr(factor, forward_return)
        """
        if len(factor) != len(forward_return):
            return np.nan
        
        # 对齐索引
        aligned = pd.DataFrame({'factor': factor, 'return': forward_return}).dropna()
        if len(aligned) < 10:
            return np.nan
        
        ic = aligned['factor'].corr(aligned['return'])
        return ic
    
    def calculate_ir(self, ic_series: pd.Series) -> float:
        """
        计算信息比率（IR）
        IR = mean(IC) / std(IC)
        """
        if len(ic_series) < 2:
            return np.nan
        
        mean_ic = ic_series.mean()
        std_ic = ic_series.std()
        
        if std_ic == 0:
            return np.nan
        
        ir = mean_ic / std_ic
        return ir
    
    def analyze_factor(self, factor_data: pd.DataFrame, return_data: pd.DataFrame, 
                      factor_name: str, forward_periods: list = [5, 10, 20]) -> dict:
        """
        分析单个因子的有效性
        
        Args:
            factor_data: 因子数据，index为日期，columns为股票代码
            return_data: 收益率数据，index为日期，columns为股票代码
            factor_name: 因子名称
            forward_periods: 前瞻期列表
        """
        results = {
            'factor_name': factor_name,
            'ic_mean': {},
            'ic_std': {},
            'ic_ir': {},
            'ic_positive_ratio': {}
        }
        
        # 对齐日期
        common_dates = factor_data.index.intersection(return_data.index)
        if len(common_dates) < 20:
            return results
        
        ic_series_list = {}
        
        for period in forward_periods:
            ic_values = []
            
            for date in common_dates[:-period]:
                try:
                    factor_values = factor_data.loc[date]
                    forward_returns = return_data.loc[date:].iloc[period] if date in return_data.index else None
                    
                    if forward_returns is None:
                        continue
                    
                    # 对齐股票代码
                    common_stocks = factor_values.index.intersection(forward_returns.index)
                    if len(common_stocks) < 10:
                        continue
                    
                    factor_aligned = factor_values[common_stocks]
                    return_aligned = forward_returns[common_stocks]
                    
                    # 计算IC
                    ic = self.calculate_ic(factor_aligned, return_aligned)
                    if not np.isnan(ic):
                        ic_values.append(ic)
                
                except Exception as e:
                    continue
            
            if len(ic_values) > 0:
                ic_series = pd.Series(ic_values)
                results['ic_mean'][period] = float(ic_series.mean())
                results['ic_std'][period] = float(ic_series.std())
                results['ic_ir'][period] = float(self.calculate_ir(ic_series))
                results['ic_positive_ratio'][period] = float((ic_series > 0).sum() / len(ic_series))
                ic_series_list[period] = ic_series
        
        return results

# ============================================================
# 机器学习特征工程
# ============================================================

class FeatureEngineer:
    """特征工程器"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []
    
    def create_features(self, fundamentals: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
        """
        创建特征矩阵
        
        Args:
            fundamentals: 基本面数据
            prices: 价格数据
        """
        features_list = []
        
        # 对齐日期和股票
        common_dates = fundamentals.index.intersection(prices.index)
        common_stocks = fundamentals.columns.intersection(prices.columns)
        
        for date in common_dates:
            feature_dict = {}
            
            # 基本面特征
            for stock in common_stocks:
                if stock not in fundamentals.columns or stock not in prices.columns:
                    continue
                
                fund = fundamentals.loc[date, stock] if isinstance(fundamentals.loc[date], pd.Series) else fundamentals.loc[date]
                price = prices.loc[date, stock] if isinstance(prices.loc[date], pd.Series) else prices.loc[date]
                
                if pd.isna(fund) or pd.isna(price):
                    continue
                
                # 估值特征
                feature_dict[f'{stock}_pe'] = fund.get('pe_ratio', np.nan)
                feature_dict[f'{stock}_pb'] = fund.get('pb_ratio', np.nan)
                feature_dict[f'{stock}_market_cap'] = fund.get('market_cap', np.nan)
                
                # 质量特征
                feature_dict[f'{stock}_roe'] = fund.get('roe', np.nan)
                feature_dict[f'{stock}_roa'] = fund.get('roa', np.nan)
                
                # 成长特征
                feature_dict[f'{stock}_revenue_growth'] = fund.get('revenue_growth', np.nan)
                feature_dict[f'{stock}_profit_growth'] = fund.get('profit_growth', np.nan)
                
                # 价格特征
                if isinstance(price, dict):
                    feature_dict[f'{stock}_close'] = price.get('close', np.nan)
                    feature_dict[f'{stock}_volume'] = price.get('volume', np.nan)
            
            if feature_dict:
                feature_dict['date'] = date
                features_list.append(feature_dict)
        
        if not features_list:
            return pd.DataFrame()
        
        features_df = pd.DataFrame(features_list)
        features_df.set_index('date', inplace=True)
        
        return features_df
    
    def normalize_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """标准化特征"""
        if features.empty:
            return features
        
        # 只标准化数值列
        numeric_cols = features.select_dtypes(include=[np.number]).columns
        features_normalized = features.copy()
        features_normalized[numeric_cols] = self.scaler.fit_transform(features[numeric_cols])
        
        return features_normalized

# ============================================================
# 机器学习模型
# ============================================================

class MLModel:
    """机器学习模型"""
    
    def __init__(self, model_type: str = 'xgboost'):
        self.model_type = model_type
        self.model = None
        self.feature_importance = None
        self.scaler = StandardScaler()
        
        if model_type == 'xgboost' and XGBOOST_AVAILABLE:
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            )
        elif model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        else:
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """训练模型"""
        # 标准化
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # 训练
        self.model.fit(X_train_scaled, y_train)
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=X_train.columns
            ).sort_values(ascending=False)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """预测"""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """评估模型"""
        y_pred = self.predict(X)
        
        mse = mean_squared_error(y, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y, y_pred)
        
        # IC值
        ic = np.corrcoef(y, y_pred)[0, 1]
        
        return {
            'mse': float(mse),
            'rmse': float(rmse),
            'r2': float(r2),
            'ic': float(ic) if not np.isnan(ic) else 0.0
        }
    
    def save(self, path: str):
        """保存模型"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'model_type': self.model_type
            }, f)
    
    def load(self, path: str):
        """加载模型"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_importance = data.get('feature_importance')
            self.model_type = data.get('model_type', 'xgboost')

# ============================================================
# 数据集划分
# ============================================================

class DataSplitter:
    """数据集划分器（时间序列）"""
    
    @staticmethod
    def split_time_series(data: pd.DataFrame, train_ratio: float = 0.7) -> tuple:
        """
        按时间序列划分训练集和验证集
        
        Args:
            data: 数据，index为日期
            train_ratio: 训练集比例
        """
        if data.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        sorted_dates = sorted(data.index)
        split_idx = int(len(sorted_dates) * train_ratio)
        
        train_dates = sorted_dates[:split_idx]
        val_dates = sorted_dates[split_idx:]
        
        train_data = data.loc[train_dates]
        val_data = data.loc[val_dates]
        
        return train_data, val_data
    
    @staticmethod
    def time_series_cv(data: pd.DataFrame, n_splits: int = 5) -> list:
        """
        时间序列交叉验证
        
        Returns:
            [(train_idx, val_idx), ...]
        """
        tscv = TimeSeriesSplit(n_splits=n_splits)
        splits = []
        
        for train_idx, val_idx in tscv.split(data):
            splits.append((train_idx, val_idx))
        
        return splits

# ============================================================
# 因子组合优化
# ============================================================

class FactorOptimizer:
    """因子组合优化器"""
    
    def __init__(self):
        self.best_factors = []
        self.factor_weights = {}
    
    def optimize_combination(self, factor_data: dict, return_data: pd.DataFrame, 
                           method: str = 'ic_weighted') -> dict:
        """
        优化因子组合
        
        Args:
            factor_data: {factor_name: factor_df}
            return_data: 收益率数据
            method: 优化方法 ('ic_weighted', 'ml_selected')
        """
        if method == 'ic_weighted':
            return self._ic_weighted_optimization(factor_data, return_data)
        elif method == 'ml_selected':
            return self._ml_selected_optimization(factor_data, return_data)
        else:
            return {}
    
    def _ic_weighted_optimization(self, factor_data: dict, return_data: pd.DataFrame) -> dict:
        """基于IC值的加权优化"""
        analyzer = FactorAnalyzer()
        factor_ics = {}
        
        for factor_name, factor_df in factor_data.items():
            results = analyzer.analyze_factor(factor_df, return_data, factor_name)
            # 使用平均IC值
            avg_ic = np.mean(list(results.get('ic_mean', {}).values()))
            if not np.isnan(avg_ic):
                factor_ics[factor_name] = abs(avg_ic)
        
        # 归一化权重
        total_ic = sum(factor_ics.values())
        if total_ic > 0:
            weights = {k: v / total_ic for k, v in factor_ics.items()}
        else:
            weights = {k: 1.0 / len(factor_ics) for k in factor_ics.keys()}
        
        return {
            'weights': weights,
            'factors': list(factor_ics.keys()),
            'method': 'ic_weighted'
        }
    
    def _ml_selected_optimization(self, factor_data: dict, return_data: pd.DataFrame) -> dict:
        """基于机器学习的选择优化"""
        # 简化实现：使用随机森林选择重要因子
        # 实际应用中可以使用更复杂的特征选择方法
        
        # 合并所有因子
        all_factors = pd.DataFrame()
        for factor_name, factor_df in factor_data.items():
            if all_factors.empty:
                all_factors = factor_df.copy()
                all_factors.columns = [f'{factor_name}_{col}' for col in all_factors.columns]
            else:
                factor_df_renamed = factor_df.copy()
                factor_df_renamed.columns = [f'{factor_name}_{col}' for col in factor_df_renamed.columns]
                all_factors = all_factors.join(factor_df_renamed, how='outer')
        
        # 对齐收益率
        common_dates = all_factors.index.intersection(return_data.index)
        if len(common_dates) < 50:
            return {}
        
        # 准备数据
        X = all_factors.loc[common_dates].fillna(0)
        y = return_data.loc[common_dates].mean(axis=1)  # 使用平均收益率作为目标
        
        # 训练模型
        model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
        model.fit(X, y)
        
        # 获取特征重要性
        importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        
        # 选择top因子
        top_n = min(10, len(importance))
        top_factors = importance.head(top_n).index.tolist()
        
        # 计算权重
        weights = {}
        for factor_name in factor_data.keys():
            factor_cols = [col for col in top_factors if col.startswith(factor_name)]
            if factor_cols:
                weights[factor_name] = importance[factor_cols].sum() / importance.sum()
        
        return {
            'weights': weights,
            'factors': list(weights.keys()),
            'method': 'ml_selected',
            'feature_importance': importance.to_dict()
        }

# ============================================================
# 主函数
# ============================================================

def main():
    """示例用法"""
    print("=" * 80)
    print("因子分析与机器学习模块")
    print("=" * 80)
    
    # 这里可以添加具体的测试代码
    print("✅ 模块加载成功")
    print("   功能:")
    print("   1. 因子有效性检验（IC值、IR值）")
    print("   2. 机器学习特征工程")
    print("   3. 模型训练与验证")
    print("   4. 因子组合优化")

if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
因子分析与机器学习模块
====================

功能:
1. 因子有效性检验（IC值、IR值）
2. 机器学习特征工程
3. 模型训练与验证（训练集/验证集）
4. 因子组合优化

代码位置: research/tenbagger_10x_strategy/scripts/factor_analysis_ml.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import pickle

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning("XGBoost not available, using GradientBoostingRegressor")

# ============================================================
# 因子有效性检验
# ============================================================

class FactorAnalyzer:
    """因子分析器"""
    
    def __init__(self):
        self.ic_results = {}
        self.ir_results = {}
    
    def calculate_ic(self, factor: pd.Series, forward_return: pd.Series) -> float:
        """
        计算信息系数（IC）
        IC = corr(factor, forward_return)
        """
        if len(factor) != len(forward_return):
            return np.nan
        
        # 对齐索引
        aligned = pd.DataFrame({'factor': factor, 'return': forward_return}).dropna()
        if len(aligned) < 10:
            return np.nan
        
        ic = aligned['factor'].corr(aligned['return'])
        return ic
    
    def calculate_ir(self, ic_series: pd.Series) -> float:
        """
        计算信息比率（IR）
        IR = mean(IC) / std(IC)
        """
        if len(ic_series) < 2:
            return np.nan
        
        mean_ic = ic_series.mean()
        std_ic = ic_series.std()
        
        if std_ic == 0:
            return np.nan
        
        ir = mean_ic / std_ic
        return ir
    
    def analyze_factor(self, factor_data: pd.DataFrame, return_data: pd.DataFrame, 
                      factor_name: str, forward_periods: list = [5, 10, 20]) -> dict:
        """
        分析单个因子的有效性
        
        Args:
            factor_data: 因子数据，index为日期，columns为股票代码
            return_data: 收益率数据，index为日期，columns为股票代码
            factor_name: 因子名称
            forward_periods: 前瞻期列表
        """
        results = {
            'factor_name': factor_name,
            'ic_mean': {},
            'ic_std': {},
            'ic_ir': {},
            'ic_positive_ratio': {}
        }
        
        # 对齐日期
        common_dates = factor_data.index.intersection(return_data.index)
        if len(common_dates) < 20:
            return results
        
        ic_series_list = {}
        
        for period in forward_periods:
            ic_values = []
            
            for date in common_dates[:-period]:
                try:
                    factor_values = factor_data.loc[date]
                    forward_returns = return_data.loc[date:].iloc[period] if date in return_data.index else None
                    
                    if forward_returns is None:
                        continue
                    
                    # 对齐股票代码
                    common_stocks = factor_values.index.intersection(forward_returns.index)
                    if len(common_stocks) < 10:
                        continue
                    
                    factor_aligned = factor_values[common_stocks]
                    return_aligned = forward_returns[common_stocks]
                    
                    # 计算IC
                    ic = self.calculate_ic(factor_aligned, return_aligned)
                    if not np.isnan(ic):
                        ic_values.append(ic)
                
                except Exception as e:
                    continue
            
            if len(ic_values) > 0:
                ic_series = pd.Series(ic_values)
                results['ic_mean'][period] = float(ic_series.mean())
                results['ic_std'][period] = float(ic_series.std())
                results['ic_ir'][period] = float(self.calculate_ir(ic_series))
                results['ic_positive_ratio'][period] = float((ic_series > 0).sum() / len(ic_series))
                ic_series_list[period] = ic_series
        
        return results

# ============================================================
# 机器学习特征工程
# ============================================================

class FeatureEngineer:
    """特征工程器"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []
    
    def create_features(self, fundamentals: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
        """
        创建特征矩阵
        
        Args:
            fundamentals: 基本面数据
            prices: 价格数据
        """
        features_list = []
        
        # 对齐日期和股票
        common_dates = fundamentals.index.intersection(prices.index)
        common_stocks = fundamentals.columns.intersection(prices.columns)
        
        for date in common_dates:
            feature_dict = {}
            
            # 基本面特征
            for stock in common_stocks:
                if stock not in fundamentals.columns or stock not in prices.columns:
                    continue
                
                fund = fundamentals.loc[date, stock] if isinstance(fundamentals.loc[date], pd.Series) else fundamentals.loc[date]
                price = prices.loc[date, stock] if isinstance(prices.loc[date], pd.Series) else prices.loc[date]
                
                if pd.isna(fund) or pd.isna(price):
                    continue
                
                # 估值特征
                feature_dict[f'{stock}_pe'] = fund.get('pe_ratio', np.nan)
                feature_dict[f'{stock}_pb'] = fund.get('pb_ratio', np.nan)
                feature_dict[f'{stock}_market_cap'] = fund.get('market_cap', np.nan)
                
                # 质量特征
                feature_dict[f'{stock}_roe'] = fund.get('roe', np.nan)
                feature_dict[f'{stock}_roa'] = fund.get('roa', np.nan)
                
                # 成长特征
                feature_dict[f'{stock}_revenue_growth'] = fund.get('revenue_growth', np.nan)
                feature_dict[f'{stock}_profit_growth'] = fund.get('profit_growth', np.nan)
                
                # 价格特征
                if isinstance(price, dict):
                    feature_dict[f'{stock}_close'] = price.get('close', np.nan)
                    feature_dict[f'{stock}_volume'] = price.get('volume', np.nan)
            
            if feature_dict:
                feature_dict['date'] = date
                features_list.append(feature_dict)
        
        if not features_list:
            return pd.DataFrame()
        
        features_df = pd.DataFrame(features_list)
        features_df.set_index('date', inplace=True)
        
        return features_df
    
    def normalize_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """标准化特征"""
        if features.empty:
            return features
        
        # 只标准化数值列
        numeric_cols = features.select_dtypes(include=[np.number]).columns
        features_normalized = features.copy()
        features_normalized[numeric_cols] = self.scaler.fit_transform(features[numeric_cols])
        
        return features_normalized

# ============================================================
# 机器学习模型
# ============================================================

class MLModel:
    """机器学习模型"""
    
    def __init__(self, model_type: str = 'xgboost'):
        self.model_type = model_type
        self.model = None
        self.feature_importance = None
        self.scaler = StandardScaler()
        
        if model_type == 'xgboost' and XGBOOST_AVAILABLE:
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            )
        elif model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        else:
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """训练模型"""
        # 标准化
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # 训练
        self.model.fit(X_train_scaled, y_train)
        
        # 特征重要性
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.Series(
                self.model.feature_importances_,
                index=X_train.columns
            ).sort_values(ascending=False)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """预测"""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """评估模型"""
        y_pred = self.predict(X)
        
        mse = mean_squared_error(y, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y, y_pred)
        
        # IC值
        ic = np.corrcoef(y, y_pred)[0, 1]
        
        return {
            'mse': float(mse),
            'rmse': float(rmse),
            'r2': float(r2),
            'ic': float(ic) if not np.isnan(ic) else 0.0
        }
    
    def save(self, path: str):
        """保存模型"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'model_type': self.model_type
            }, f)
    
    def load(self, path: str):
        """加载模型"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_importance = data.get('feature_importance')
            self.model_type = data.get('model_type', 'xgboost')

# ============================================================
# 数据集划分
# ============================================================

class DataSplitter:
    """数据集划分器（时间序列）"""
    
    @staticmethod
    def split_time_series(data: pd.DataFrame, train_ratio: float = 0.7) -> tuple:
        """
        按时间序列划分训练集和验证集
        
        Args:
            data: 数据，index为日期
            train_ratio: 训练集比例
        """
        if data.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        sorted_dates = sorted(data.index)
        split_idx = int(len(sorted_dates) * train_ratio)
        
        train_dates = sorted_dates[:split_idx]
        val_dates = sorted_dates[split_idx:]
        
        train_data = data.loc[train_dates]
        val_data = data.loc[val_dates]
        
        return train_data, val_data
    
    @staticmethod
    def time_series_cv(data: pd.DataFrame, n_splits: int = 5) -> list:
        """
        时间序列交叉验证
        
        Returns:
            [(train_idx, val_idx), ...]
        """
        tscv = TimeSeriesSplit(n_splits=n_splits)
        splits = []
        
        for train_idx, val_idx in tscv.split(data):
            splits.append((train_idx, val_idx))
        
        return splits

# ============================================================
# 因子组合优化
# ============================================================

class FactorOptimizer:
    """因子组合优化器"""
    
    def __init__(self):
        self.best_factors = []
        self.factor_weights = {}
    
    def optimize_combination(self, factor_data: dict, return_data: pd.DataFrame, 
                           method: str = 'ic_weighted') -> dict:
        """
        优化因子组合
        
        Args:
            factor_data: {factor_name: factor_df}
            return_data: 收益率数据
            method: 优化方法 ('ic_weighted', 'ml_selected')
        """
        if method == 'ic_weighted':
            return self._ic_weighted_optimization(factor_data, return_data)
        elif method == 'ml_selected':
            return self._ml_selected_optimization(factor_data, return_data)
        else:
            return {}
    
    def _ic_weighted_optimization(self, factor_data: dict, return_data: pd.DataFrame) -> dict:
        """基于IC值的加权优化"""
        analyzer = FactorAnalyzer()
        factor_ics = {}
        
        for factor_name, factor_df in factor_data.items():
            results = analyzer.analyze_factor(factor_df, return_data, factor_name)
            # 使用平均IC值
            avg_ic = np.mean(list(results.get('ic_mean', {}).values()))
            if not np.isnan(avg_ic):
                factor_ics[factor_name] = abs(avg_ic)
        
        # 归一化权重
        total_ic = sum(factor_ics.values())
        if total_ic > 0:
            weights = {k: v / total_ic for k, v in factor_ics.items()}
        else:
            weights = {k: 1.0 / len(factor_ics) for k in factor_ics.keys()}
        
        return {
            'weights': weights,
            'factors': list(factor_ics.keys()),
            'method': 'ic_weighted'
        }
    
    def _ml_selected_optimization(self, factor_data: dict, return_data: pd.DataFrame) -> dict:
        """基于机器学习的选择优化"""
        # 简化实现：使用随机森林选择重要因子
        # 实际应用中可以使用更复杂的特征选择方法
        
        # 合并所有因子
        all_factors = pd.DataFrame()
        for factor_name, factor_df in factor_data.items():
            if all_factors.empty:
                all_factors = factor_df.copy()
                all_factors.columns = [f'{factor_name}_{col}' for col in all_factors.columns]
            else:
                factor_df_renamed = factor_df.copy()
                factor_df_renamed.columns = [f'{factor_name}_{col}' for col in factor_df_renamed.columns]
                all_factors = all_factors.join(factor_df_renamed, how='outer')
        
        # 对齐收益率
        common_dates = all_factors.index.intersection(return_data.index)
        if len(common_dates) < 50:
            return {}
        
        # 准备数据
        X = all_factors.loc[common_dates].fillna(0)
        y = return_data.loc[common_dates].mean(axis=1)  # 使用平均收益率作为目标
        
        # 训练模型
        model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
        model.fit(X, y)
        
        # 获取特征重要性
        importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        
        # 选择top因子
        top_n = min(10, len(importance))
        top_factors = importance.head(top_n).index.tolist()
        
        # 计算权重
        weights = {}
        for factor_name in factor_data.keys():
            factor_cols = [col for col in top_factors if col.startswith(factor_name)]
            if factor_cols:
                weights[factor_name] = importance[factor_cols].sum() / importance.sum()
        
        return {
            'weights': weights,
            'factors': list(weights.keys()),
            'method': 'ml_selected',
            'feature_importance': importance.to_dict()
        }

# ============================================================
# 主函数
# ============================================================

def main():
    """示例用法"""
    print("=" * 80)
    print("因子分析与机器学习模块")
    print("=" * 80)
    
    # 这里可以添加具体的测试代码
    print("✅ 模块加载成功")
    print("   功能:")
    print("   1. 因子有效性检验（IC值、IR值）")
    print("   2. 机器学习特征工程")
    print("   3. 模型训练与验证")
    print("   4. 因子组合优化")

if __name__ == "__main__":
    main()









































