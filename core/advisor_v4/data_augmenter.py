# -*- coding: utf-8 -*-
"""
数据增强器 - 改进负样本采样和数据平衡

功能：
1. 智能负样本采样（Hard Negative Mining）
2. 类别平衡（SMOTE、过采样、欠采样）
3. 时间窗口平衡
4. 困难样本挖掘
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
import logging
from collections import Counter

logger = logging.getLogger(__name__)


class DataAugmenter:
    """数据增强器"""
    
    def __init__(self,
                 strategy: str = 'balanced',
                 target_ratio: float = 2.0,
                 random_state: int = 42):
        """
        Args:
            strategy: 增强策略 ('balanced', 'smote', 'random_over', 'random_under')
            target_ratio: 目标负/正样本比例
            random_state: 随机种子
        """
        self.strategy = strategy
        self.target_ratio = target_ratio
        self.random_state = random_state
        
        self.info = {}
        self.original_distribution = {}
        self.augmented_distribution = {}
    
    def augment(self, 
                df: pd.DataFrame,
                label_col: str = 'label',
                target_ratio: float = None) -> pd.DataFrame:
        """数据增强
        
        Args:
            df: 输入DataFrame
            label_col: 标签列
            target_ratio: 目标负/正样本比例
            
        Returns:
            增强后的DataFrame
        """
        if label_col not in df.columns:
            logger.warning(f"缺少标签列 {label_col}")
            return df
        
        target_ratio = target_ratio or self.target_ratio
        
        # 记录原始分布
        self.original_distribution = dict(Counter(df[label_col]))
        n_positive = df[df[label_col] == 1].shape[0]
        n_negative = df[df[label_col] == 0].shape[0]
        
        print(f"\n数据增强:")
        print(f"  原始分布: 正样本={n_positive}, 负样本={n_negative}")
        print(f"  原始比例: {n_negative / max(n_positive, 1):.2f}:1")
        print(f"  目标比例: {target_ratio}:1")
        
        # 选择增强策略
        if self.strategy == 'balanced':
            result_df = self._balanced_augment(df, label_col, target_ratio)
        elif self.strategy == 'smote':
            result_df = self._smote_augment(df, label_col)
        elif self.strategy == 'random_over':
            result_df = self._random_oversample(df, label_col, target_ratio)
        elif self.strategy == 'random_under':
            result_df = self._random_undersample(df, label_col, target_ratio)
        elif self.strategy == 'hard_negative':
            result_df = self._hard_negative_mining(df, label_col, target_ratio)
        else:
            result_df = self._balanced_augment(df, label_col, target_ratio)
        
        # 记录增强后分布
        self.augmented_distribution = dict(Counter(result_df[label_col]))
        n_positive_new = result_df[result_df[label_col] == 1].shape[0]
        n_negative_new = result_df[result_df[label_col] == 0].shape[0]
        
        print(f"  增强后分布: 正样本={n_positive_new}, 负样本={n_negative_new}")
        print(f"  增强后比例: {n_negative_new / max(n_positive_new, 1):.2f}:1")
        
        self.info = {
            'strategy': self.strategy,
            'target_ratio': target_ratio,
            'original': self.original_distribution,
            'augmented': self.augmented_distribution,
        }
        
        return result_df
    
    def _balanced_augment(self, 
                          df: pd.DataFrame,
                          label_col: str,
                          target_ratio: float) -> pd.DataFrame:
        """平衡增强 - 结合过采样和欠采样"""
        positive_df = df[df[label_col] == 1]
        negative_df = df[df[label_col] == 0]
        
        n_positive = len(positive_df)
        n_negative = len(negative_df)
        
        # 计算目标数量
        target_negative = int(n_positive * target_ratio)
        
        if n_negative > target_negative:
            # 欠采样负样本
            negative_df = negative_df.sample(n=target_negative, random_state=self.random_state)
        elif n_negative < target_negative:
            # 过采样负样本
            n_to_add = target_negative - n_negative
            additional = negative_df.sample(n=n_to_add, replace=True, random_state=self.random_state)
            negative_df = pd.concat([negative_df, additional], ignore_index=True)
        
        # 合并
        result_df = pd.concat([positive_df, negative_df], ignore_index=True)
        
        # 打乱顺序
        result_df = result_df.sample(frac=1, random_state=self.random_state).reset_index(drop=True)
        
        return result_df
    
    def _smote_augment(self, 
                       df: pd.DataFrame,
                       label_col: str) -> pd.DataFrame:
        """SMOTE增强"""
        try:
            from imblearn.over_sampling import SMOTE
        except ImportError:
            logger.warning("imblearn未安装，回退到balanced策略")
            return self._balanced_augment(df, label_col, self.target_ratio)
        
        # 准备数据
        feature_cols = [c for c in df.columns if c != label_col and df[c].dtype in ['int64', 'float64']]
        
        X = df[feature_cols].values
        y = df[label_col].values
        
        # 填充NaN
        X = np.nan_to_num(X, nan=0.0)
        
        try:
            # 应用SMOTE
            smote = SMOTE(
                sampling_strategy='auto',
                random_state=self.random_state,
                k_neighbors=min(5, len(df[df[label_col] == 1]) - 1)
            )
            
            X_resampled, y_resampled = smote.fit_resample(X, y)
            
            # 重建DataFrame
            result_df = pd.DataFrame(X_resampled, columns=feature_cols)
            result_df[label_col] = y_resampled
            
            # 添加非数值列（使用第一行的值）
            for col in df.columns:
                if col not in result_df.columns:
                    result_df[col] = df[col].iloc[0]
            
            return result_df
        
        except Exception as e:
            logger.warning(f"SMOTE失败: {e}，回退到balanced策略")
            return self._balanced_augment(df, label_col, self.target_ratio)
    
    def _random_oversample(self, 
                           df: pd.DataFrame,
                           label_col: str,
                           target_ratio: float) -> pd.DataFrame:
        """随机过采样少数类"""
        positive_df = df[df[label_col] == 1]
        negative_df = df[df[label_col] == 0]
        
        n_positive = len(positive_df)
        n_negative = len(negative_df)
        
        # 计算需要过采样的数量
        target_positive = int(n_negative / target_ratio)
        
        if target_positive > n_positive:
            n_to_add = target_positive - n_positive
            additional = positive_df.sample(n=n_to_add, replace=True, random_state=self.random_state)
            positive_df = pd.concat([positive_df, additional], ignore_index=True)
        
        result_df = pd.concat([positive_df, negative_df], ignore_index=True)
        result_df = result_df.sample(frac=1, random_state=self.random_state).reset_index(drop=True)
        
        return result_df
    
    def _random_undersample(self, 
                            df: pd.DataFrame,
                            label_col: str,
                            target_ratio: float) -> pd.DataFrame:
        """随机欠采样多数类"""
        positive_df = df[df[label_col] == 1]
        negative_df = df[df[label_col] == 0]
        
        n_positive = len(positive_df)
        n_negative = len(negative_df)
        
        # 计算欠采样后的数量
        target_negative = int(n_positive * target_ratio)
        
        if n_negative > target_negative:
            negative_df = negative_df.sample(n=target_negative, random_state=self.random_state)
        
        result_df = pd.concat([positive_df, negative_df], ignore_index=True)
        result_df = result_df.sample(frac=1, random_state=self.random_state).reset_index(drop=True)
        
        return result_df
    
    def _hard_negative_mining(self, 
                              df: pd.DataFrame,
                              label_col: str,
                              target_ratio: float,
                              model=None) -> pd.DataFrame:
        """困难负样本挖掘
        
        选择与正样本特征相似但标签为负的样本
        """
        positive_df = df[df[label_col] == 1]
        negative_df = df[df[label_col] == 0]
        
        n_positive = len(positive_df)
        target_negative = int(n_positive * target_ratio)
        
        # 获取数值特征列
        feature_cols = [c for c in df.columns if c != label_col and df[c].dtype in ['int64', 'float64']]
        
        if len(feature_cols) == 0 or len(negative_df) <= target_negative:
            return self._balanced_augment(df, label_col, target_ratio)
        
        try:
            from sklearn.neighbors import NearestNeighbors
            from sklearn.preprocessing import StandardScaler
            
            # 标准化特征
            scaler = StandardScaler()
            positive_features = scaler.fit_transform(positive_df[feature_cols].fillna(0))
            negative_features = scaler.transform(negative_df[feature_cols].fillna(0))
            
            # 找到与正样本最相似的负样本
            nn = NearestNeighbors(n_neighbors=min(5, len(positive_df)), algorithm='ball_tree')
            nn.fit(positive_features)
            
            # 计算每个负样本与最近正样本的距离
            distances, _ = nn.kneighbors(negative_features)
            avg_distances = distances.mean(axis=1)
            
            # 选择距离最近的（即最困难的）负样本
            hard_indices = np.argsort(avg_distances)[:target_negative]
            hard_negative_df = negative_df.iloc[hard_indices]
            
            result_df = pd.concat([positive_df, hard_negative_df], ignore_index=True)
            result_df = result_df.sample(frac=1, random_state=self.random_state).reset_index(drop=True)
            
            return result_df
        
        except Exception as e:
            logger.warning(f"困难负样本挖掘失败: {e}，回退到balanced策略")
            return self._balanced_augment(df, label_col, target_ratio)
    
    def get_info(self) -> Dict:
        """获取增强信息"""
        return self.info


class TimeBalancedAugmenter:
    """时间平衡增强器 - 确保时间分布均匀"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.info = {}
    
    def augment(self, 
                df: pd.DataFrame,
                date_col: str = 'prediction_date',
                label_col: str = 'label',
                target_ratio: float = 2.0) -> pd.DataFrame:
        """按时间窗口平衡增强
        
        确保每个时间窗口内的正负样本比例一致
        """
        if date_col not in df.columns:
            logger.warning(f"缺少日期列 {date_col}")
            return df
        
        # 按月分组
        df['_month'] = pd.to_datetime(df[date_col]).dt.to_period('M')
        
        augmented_dfs = []
        
        for month in df['_month'].unique():
            month_df = df[df['_month'] == month].copy()
            
            positive_df = month_df[month_df[label_col] == 1]
            negative_df = month_df[month_df[label_col] == 0]
            
            n_positive = len(positive_df)
            n_negative = len(negative_df)
            
            if n_positive == 0 or n_negative == 0:
                augmented_dfs.append(month_df)
                continue
            
            # 平衡
            target_negative = int(n_positive * target_ratio)
            
            if n_negative > target_negative:
                negative_df = negative_df.sample(n=target_negative, random_state=self.random_state)
            elif n_negative < target_negative:
                n_to_add = target_negative - n_negative
                if n_to_add <= len(negative_df):
                    additional = negative_df.sample(n=n_to_add, replace=True, random_state=self.random_state)
                    negative_df = pd.concat([negative_df, additional], ignore_index=True)
            
            month_augmented = pd.concat([positive_df, negative_df], ignore_index=True)
            augmented_dfs.append(month_augmented)
        
        result_df = pd.concat(augmented_dfs, ignore_index=True)
        
        # 删除临时列
        result_df = result_df.drop(columns=['_month'])
        
        # 打乱
        result_df = result_df.sample(frac=1, random_state=self.random_state).reset_index(drop=True)
        
        return result_df


class StratifiedAugmenter:
    """分层增强器 - 按多个维度进行分层平衡"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
    
    def augment(self, 
                df: pd.DataFrame,
                stratify_cols: List[str],
                label_col: str = 'label',
                target_ratio: float = 2.0) -> pd.DataFrame:
        """分层增强
        
        Args:
            df: 输入DataFrame
            stratify_cols: 分层列（如行业、市值区间）
            label_col: 标签列
            target_ratio: 目标比例
        """
        # 创建分层key
        valid_cols = [c for c in stratify_cols if c in df.columns]
        
        if not valid_cols:
            logger.warning("无有效分层列，使用全局平衡")
            augmenter = DataAugmenter(target_ratio=target_ratio, random_state=self.random_state)
            return augmenter.augment(df, label_col)
        
        df['_strata'] = df[valid_cols].astype(str).agg('_'.join, axis=1)
        
        augmented_dfs = []
        
        for strata in df['_strata'].unique():
            strata_df = df[df['_strata'] == strata].copy()
            
            if len(strata_df) < 5:
                augmented_dfs.append(strata_df)
                continue
            
            augmenter = DataAugmenter(target_ratio=target_ratio, random_state=self.random_state)
            augmented = augmenter.augment(strata_df, label_col)
            augmented_dfs.append(augmented)
        
        result_df = pd.concat(augmented_dfs, ignore_index=True)
        result_df = result_df.drop(columns=['_strata'])
        result_df = result_df.sample(frac=1, random_state=self.random_state).reset_index(drop=True)
        
        return result_df


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("测试数据增强器...")
    
    # 创建不平衡的模拟数据
    np.random.seed(42)
    n_positive = 100
    n_negative = 500
    
    positive_df = pd.DataFrame({
        'code': [f'stock_{i}' for i in range(n_positive)],
        'prediction_date': pd.date_range('2024-01-01', periods=n_positive, freq='D').strftime('%Y-%m-%d').tolist(),
        'feature1': np.random.randn(n_positive),
        'feature2': np.random.randn(n_positive),
        'feature3': np.random.randn(n_positive),
        'label': 1,
    })
    
    negative_df = pd.DataFrame({
        'code': [f'stock_{i}' for i in range(n_positive, n_positive + n_negative)],
        'prediction_date': pd.date_range('2024-01-01', periods=n_negative, freq='D').strftime('%Y-%m-%d').tolist(),
        'feature1': np.random.randn(n_negative),
        'feature2': np.random.randn(n_negative),
        'feature3': np.random.randn(n_negative),
        'label': 0,
    })
    
    df = pd.concat([positive_df, negative_df], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"\n原始数据: {len(df)} 条")
    print(f"正样本: {len(df[df['label'] == 1])}")
    print(f"负样本: {len(df[df['label'] == 0])}")
    
    # 测试balanced策略
    print("\n=== 测试balanced策略 ===")
    augmenter = DataAugmenter(strategy='balanced', target_ratio=2.0)
    augmented_df = augmenter.augment(df)
    print(f"增强后: {len(augmented_df)} 条")
    
    # 测试hard_negative策略
    print("\n=== 测试hard_negative策略 ===")
    augmenter_hn = DataAugmenter(strategy='hard_negative', target_ratio=2.0)
    augmented_df_hn = augmenter_hn.augment(df)
    print(f"增强后: {len(augmented_df_hn)} 条")
    
    # 测试时间平衡增强
    print("\n=== 测试时间平衡增强 ===")
    time_augmenter = TimeBalancedAugmenter()
    time_augmented_df = time_augmenter.augment(df)
    print(f"增强后: {len(time_augmented_df)} 条")
    
    print("\n测试完成!")
