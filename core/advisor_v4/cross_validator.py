# -*- coding: utf-8 -*-
"""
交叉验证模块 - 防止过拟合的验证策略

功能：
1. TimeSeriesSplit - 时序交叉验证
2. WalkForwardValidator - 滚动前进验证
3. OverfittingDetector - 过拟合检测

设计原则：
- 时序数据必须按时间划分，避免数据泄露
- 训练集在时间上必须早于验证/测试集
- 多折验证评估模型稳定性
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable, Any
from datetime import datetime, timedelta
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

# 尝试导入机器学习库
try:
    from sklearn.model_selection import TimeSeriesSplit
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        roc_auc_score, confusion_matrix
    )
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    logger.warning("scikit-learn未安装")


# ============================================================
# 数据类
# ============================================================

@dataclass
class CVFoldResult:
    """单折验证结果"""
    fold: int
    train_size: int
    val_size: int
    train_period: str
    val_period: str
    metrics: Dict[str, float]


@dataclass
class CVResult:
    """交叉验证结果"""
    method: str
    n_folds: int
    fold_results: List[CVFoldResult]
    
    # 汇总指标
    mean_auc: float = 0.0
    std_auc: float = 0.0
    mean_precision: float = 0.0
    std_precision: float = 0.0
    mean_recall: float = 0.0
    std_recall: float = 0.0
    mean_f1: float = 0.0
    std_f1: float = 0.0
    
    # 过拟合风险
    is_stable: bool = True
    stability_warning: str = ""


@dataclass
class WalkForwardPeriod:
    """Walk-Forward单期"""
    period_id: int
    train_start: str
    train_end: str
    test_start: str
    test_end: str


# ============================================================
# 时序交叉验证
# ============================================================

class TimeSeriesCrossValidator:
    """时序交叉验证器
    
    使用sklearn的TimeSeriesSplit，确保：
    - 训练集在时间上早于验证集
    - 每折验证集不重叠
    """
    
    def __init__(self, n_splits: int = 5, verbose: bool = True):
        """
        Args:
            n_splits: 折数
            verbose: 是否打印详细信息
        """
        self.n_splits = n_splits
        self.verbose = verbose
        self.results: List[CVFoldResult] = []
    
    def validate(self, 
                 df: pd.DataFrame,
                 train_func: Callable[[pd.DataFrame], Any],
                 eval_func: Callable[[Any, pd.DataFrame], Dict[str, float]],
                 date_column: str = 'prediction_date') -> CVResult:
        """执行时序交叉验证
        
        Args:
            df: 数据（必须包含日期列）
            train_func: 训练函数，输入训练数据，返回模型
            eval_func: 评估函数，输入(模型, 验证数据)，返回指标字典
            date_column: 日期列名
            
        Returns:
            CVResult
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"【时序交叉验证】{self.n_splits} 折")
            print(f"{'='*60}")
        
        # 按日期排序
        df = df.sort_values(date_column).reset_index(drop=True)
        
        if not HAS_SKLEARN:
            logger.warning("sklearn未安装，使用简单划分")
            return self._simple_split_validate(df, train_func, eval_func, date_column)
        
        tscv = TimeSeriesSplit(n_splits=self.n_splits)
        
        fold_results = []
        
        for fold, (train_idx, val_idx) in enumerate(tscv.split(df)):
            train_df = df.iloc[train_idx]
            val_df = df.iloc[val_idx]
            
            # 获取时间范围
            train_start = train_df[date_column].min()
            train_end = train_df[date_column].max()
            val_start = val_df[date_column].min()
            val_end = val_df[date_column].max()
            
            if self.verbose:
                print(f"\n[Fold {fold+1}/{self.n_splits}]")
                print(f"  训练期: {train_start} ~ {train_end} ({len(train_df)} 样本)")
                print(f"  验证期: {val_start} ~ {val_end} ({len(val_df)} 样本)")
            
            # 训练
            try:
                model = train_func(train_df)
            except Exception as e:
                logger.warning(f"Fold {fold+1} 训练失败: {e}")
                continue
            
            # 评估
            try:
                metrics = eval_func(model, val_df)
            except Exception as e:
                logger.warning(f"Fold {fold+1} 评估失败: {e}")
                metrics = {'auc': 0, 'precision': 0, 'recall': 0, 'f1': 0}
            
            if self.verbose:
                print(f"  指标: AUC={metrics.get('auc', 0):.4f}, "
                      f"Precision={metrics.get('precision', 0):.4f}, "
                      f"Recall={metrics.get('recall', 0):.4f}, "
                      f"F1={metrics.get('f1', 0):.4f}")
            
            fold_result = CVFoldResult(
                fold=fold + 1,
                train_size=len(train_df),
                val_size=len(val_df),
                train_period=f"{train_start} ~ {train_end}",
                val_period=f"{val_start} ~ {val_end}",
                metrics=metrics
            )
            fold_results.append(fold_result)
        
        # 汇总结果
        result = self._summarize_results(fold_results, 'time_series_split')
        
        if self.verbose:
            self._print_summary(result)
        
        return result
    
    def _simple_split_validate(self, df, train_func, eval_func, date_column):
        """简单划分验证（sklearn不可用时）"""
        fold_results = []
        
        n = len(df)
        fold_size = n // self.n_splits
        
        for fold in range(self.n_splits - 1):
            train_end = (fold + 1) * fold_size
            val_start = train_end
            val_end = val_start + fold_size
            
            train_df = df.iloc[:train_end]
            val_df = df.iloc[val_start:val_end]
            
            model = train_func(train_df)
            metrics = eval_func(model, val_df)
            
            fold_results.append(CVFoldResult(
                fold=fold + 1,
                train_size=len(train_df),
                val_size=len(val_df),
                train_period=f"0 ~ {train_end}",
                val_period=f"{val_start} ~ {val_end}",
                metrics=metrics
            ))
        
        return self._summarize_results(fold_results, 'simple_split')
    
    def _summarize_results(self, fold_results: List[CVFoldResult], method: str) -> CVResult:
        """汇总结果"""
        if not fold_results:
            return CVResult(method=method, n_folds=0, fold_results=[])
        
        aucs = [r.metrics.get('auc', 0) for r in fold_results]
        precisions = [r.metrics.get('precision', 0) for r in fold_results]
        recalls = [r.metrics.get('recall', 0) for r in fold_results]
        f1s = [r.metrics.get('f1', 0) for r in fold_results]
        
        result = CVResult(
            method=method,
            n_folds=len(fold_results),
            fold_results=fold_results,
            mean_auc=np.mean(aucs),
            std_auc=np.std(aucs),
            mean_precision=np.mean(precisions),
            std_precision=np.std(precisions),
            mean_recall=np.mean(recalls),
            std_recall=np.std(recalls),
            mean_f1=np.mean(f1s),
            std_f1=np.std(f1s),
        )
        
        # 稳定性检测
        if result.std_auc > 0.1:
            result.is_stable = False
            result.stability_warning = f"AUC方差过大: {result.std_auc:.4f}"
        
        return result
    
    def _print_summary(self, result: CVResult):
        """打印汇总"""
        print(f"\n{'='*60}")
        print(f"【交叉验证汇总】")
        print(f"{'='*60}")
        print(f"方法: {result.method}")
        print(f"折数: {result.n_folds}")
        print(f"\n指标汇总:")
        print(f"  AUC:       {result.mean_auc:.4f} ± {result.std_auc:.4f}")
        print(f"  Precision: {result.mean_precision:.4f} ± {result.std_precision:.4f}")
        print(f"  Recall:    {result.mean_recall:.4f} ± {result.std_recall:.4f}")
        print(f"  F1:        {result.mean_f1:.4f} ± {result.std_f1:.4f}")
        
        if not result.is_stable:
            print(f"\n⚠️ 稳定性警告: {result.stability_warning}")
        else:
            print(f"\n✅ 模型稳定性良好")


# ============================================================
# Walk-Forward滚动验证
# ============================================================

class WalkForwardValidator:
    """Walk-Forward滚动前进验证器
    
    原理：
    - 在训练窗口上训练
    - 在测试窗口上验证
    - 滚动前进，重复此过程
    
    特点：
    - 更接近实际交易场景
    - 可以观察模型在不同时期的表现
    """
    
    def __init__(self,
                 train_months: int = 3,
                 test_months: int = 1,
                 step_months: int = 1,
                 verbose: bool = True):
        """
        Args:
            train_months: 训练窗口（月数）
            test_months: 测试窗口（月数）
            step_months: 滚动步长（月数）
            verbose: 是否打印详细信息
        """
        self.train_months = train_months
        self.test_months = test_months
        self.step_months = step_months
        self.verbose = verbose
        self.periods: List[WalkForwardPeriod] = []
    
    def generate_periods(self, 
                        start_date: str, 
                        end_date: str) -> List[WalkForwardPeriod]:
        """生成滚动验证周期"""
        periods = []
        
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        current = start_dt
        period_id = 0
        
        while True:
            train_start = current
            train_end = train_start + timedelta(days=self.train_months * 30)
            test_start = train_end + timedelta(days=1)
            test_end = test_start + timedelta(days=self.test_months * 30)
            
            if test_end > end_dt:
                break
            
            periods.append(WalkForwardPeriod(
                period_id=period_id,
                train_start=train_start.strftime("%Y-%m-%d"),
                train_end=train_end.strftime("%Y-%m-%d"),
                test_start=test_start.strftime("%Y-%m-%d"),
                test_end=test_end.strftime("%Y-%m-%d"),
            ))
            
            current = current + timedelta(days=self.step_months * 30)
            period_id += 1
        
        self.periods = periods
        return periods
    
    def validate(self,
                 df: pd.DataFrame,
                 train_func: Callable[[pd.DataFrame], Any],
                 eval_func: Callable[[Any, pd.DataFrame], Dict[str, float]],
                 date_column: str = 'prediction_date') -> CVResult:
        """执行Walk-Forward验证
        
        Args:
            df: 数据
            train_func: 训练函数
            eval_func: 评估函数
            date_column: 日期列名
            
        Returns:
            CVResult
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"【Walk-Forward滚动验证】")
            print(f"训练窗口: {self.train_months} 月 | 测试窗口: {self.test_months} 月")
            print(f"{'='*60}")
        
        # 确保日期列是字符串格式
        if date_column in df.columns:
            df = df.copy()
            df[date_column] = pd.to_datetime(df[date_column]).dt.strftime("%Y-%m-%d")
        
        # 获取数据日期范围
        dates = sorted(df[date_column].unique())
        start_date = dates[0]
        end_date = dates[-1]
        
        # 生成周期
        periods = self.generate_periods(start_date, end_date)
        
        if not periods:
            # 如果无法生成Walk-Forward周期，降级为简单时序划分
            logger.warning(f"无法生成Walk-Forward验证周期（数据时间跨度不足：{start_date} ~ {end_date}），降级为简单时序划分")
            # 简单划分：前80%训练，后20%验证
            n = len(df)
            split_idx = int(n * 0.8)
            train_df = df.iloc[:split_idx]
            test_df = df.iloc[split_idx:]
            
            if len(train_df) < 10 or len(test_df) < 5:
                logger.warning("数据量太少，无法执行验证")
                return CVResult(method='walk_forward', n_folds=0, fold_results=[])
            
            # 执行单次验证
            try:
                model = train_func(train_df)
                metrics = eval_func(model, test_df)
                
                fold_result = CVFoldResult(
                    fold=1,
                    train_size=len(train_df),
                    val_size=len(test_df),
                    train_period=f"{train_df[date_column].min()} ~ {train_df[date_column].max()}",
                    val_period=f"{test_df[date_column].min()} ~ {test_df[date_column].max()}",
                    metrics=metrics
                )
                
                result = self._summarize_results([fold_result], 'simple_walk_forward_fallback')
                if self.verbose:
                    print(f"  降级验证：训练集 {len(train_df)} 样本，验证集 {len(test_df)} 样本")
                    print(f"  指标: AUC={metrics.get('auc', 0):.4f}")
                return result
            except Exception as e:
                logger.warning(f"降级验证失败: {e}")
                return CVResult(method='walk_forward', n_folds=0, fold_results=[])
        
        if self.verbose:
            print(f"生成 {len(periods)} 个验证周期")
        
        fold_results = []
        
        for period in tqdm(periods, desc="Walk-Forward验证", disable=not self.verbose):
            # 获取训练和测试数据
            train_df = df[
                (df[date_column] >= period.train_start) & 
                (df[date_column] <= period.train_end)
            ]
            test_df = df[
                (df[date_column] >= period.test_start) & 
                (df[date_column] <= period.test_end)
            ]
            
            if len(train_df) < 10 or len(test_df) < 5:
                if self.verbose:
                    print(f"  Period {period.period_id}: 样本不足，跳过")
                continue
            
            if self.verbose:
                print(f"\n[Period {period.period_id}]")
                print(f"  训练: {period.train_start} ~ {period.train_end} ({len(train_df)} 样本)")
                print(f"  测试: {period.test_start} ~ {period.test_end} ({len(test_df)} 样本)")
            
            # 训练
            try:
                model = train_func(train_df)
            except Exception as e:
                logger.warning(f"Period {period.period_id} 训练失败: {e}")
                continue
            
            # 评估
            try:
                metrics = eval_func(model, test_df)
            except Exception as e:
                logger.warning(f"Period {period.period_id} 评估失败: {e}")
                metrics = {'auc': 0, 'precision': 0, 'recall': 0, 'f1': 0}
            
            if self.verbose:
                print(f"  指标: AUC={metrics.get('auc', 0):.4f}, "
                      f"Precision={metrics.get('precision', 0):.4f}, "
                      f"Recall={metrics.get('recall', 0):.4f}")
            
            fold_result = CVFoldResult(
                fold=period.period_id,
                train_size=len(train_df),
                val_size=len(test_df),
                train_period=f"{period.train_start} ~ {period.train_end}",
                val_period=f"{period.test_start} ~ {period.test_end}",
                metrics=metrics
            )
            fold_results.append(fold_result)
        
        # 汇总结果
        result = self._summarize_results(fold_results)
        
        if self.verbose:
            self._print_summary(result)
        
        return result
    
    def _summarize_results(self, fold_results: List[CVFoldResult]) -> CVResult:
        """汇总结果"""
        if not fold_results:
            return CVResult(method='walk_forward', n_folds=0, fold_results=[])
        
        aucs = [r.metrics.get('auc', 0) for r in fold_results]
        precisions = [r.metrics.get('precision', 0) for r in fold_results]
        recalls = [r.metrics.get('recall', 0) for r in fold_results]
        f1s = [r.metrics.get('f1', 0) for r in fold_results]
        
        result = CVResult(
            method='walk_forward',
            n_folds=len(fold_results),
            fold_results=fold_results,
            mean_auc=np.mean(aucs),
            std_auc=np.std(aucs),
            mean_precision=np.mean(precisions),
            std_precision=np.std(precisions),
            mean_recall=np.mean(recalls),
            std_recall=np.std(recalls),
            mean_f1=np.mean(f1s),
            std_f1=np.std(f1s),
        )
        
        # 稳定性检测
        warnings = []
        if result.std_auc > 0.1:
            warnings.append(f"AUC方差过大: {result.std_auc:.4f}")
        if result.std_precision > 0.15:
            warnings.append(f"Precision方差过大: {result.std_precision:.4f}")
        
        if warnings:
            result.is_stable = False
            result.stability_warning = "; ".join(warnings)
        
        return result
    
    def _print_summary(self, result: CVResult):
        """打印汇总"""
        print(f"\n{'='*60}")
        print(f"【Walk-Forward验证汇总】")
        print(f"{'='*60}")
        print(f"验证周期数: {result.n_folds}")
        print(f"\n指标汇总:")
        print(f"  AUC:       {result.mean_auc:.4f} ± {result.std_auc:.4f}")
        print(f"  Precision: {result.mean_precision:.4f} ± {result.std_precision:.4f}")
        print(f"  Recall:    {result.mean_recall:.4f} ± {result.std_recall:.4f}")
        print(f"  F1:        {result.mean_f1:.4f} ± {result.std_f1:.4f}")
        
        if not result.is_stable:
            print(f"\n⚠️ 稳定性警告: {result.stability_warning}")
        else:
            print(f"\n✅ 模型稳定性良好")


# ============================================================
# 过拟合检测器
# ============================================================

class OverfittingDetector:
    """过拟合检测器"""
    
    def __init__(self, 
                 auc_gap_threshold: float = 0.1,
                 precision_gap_threshold: float = 0.15,
                 top_feature_threshold: float = 0.7):
        """
        Args:
            auc_gap_threshold: AUC差距阈值（训练-验证）
            precision_gap_threshold: 精确率差距阈值
            top_feature_threshold: Top3特征占比阈值
        """
        self.auc_gap_threshold = auc_gap_threshold
        self.precision_gap_threshold = precision_gap_threshold
        self.top_feature_threshold = top_feature_threshold
    
    def detect(self,
               train_metrics: Dict[str, float],
               val_metrics: Dict[str, float],
               feature_importance: Dict[str, float] = None) -> Dict:
        """检测过拟合
        
        Args:
            train_metrics: 训练集指标
            val_metrics: 验证集指标
            feature_importance: 特征重要性（可选）
            
        Returns:
            检测报告
        """
        warnings = []
        details = {}
        
        # 1. AUC差距检测
        train_auc = train_metrics.get('auc', 0)
        val_auc = val_metrics.get('auc', 0)
        auc_gap = train_auc - val_auc
        
        details['auc_gap'] = auc_gap
        details['train_auc'] = train_auc
        details['val_auc'] = val_auc
        
        if auc_gap > self.auc_gap_threshold:
            warnings.append(
                f"AUC过拟合: 训练={train_auc:.4f}, 验证={val_auc:.4f}, "
                f"差距={auc_gap:.4f} > {self.auc_gap_threshold}"
            )
        
        # 2. 精确率差距检测
        train_precision = train_metrics.get('precision', 0)
        val_precision = val_metrics.get('precision', 0)
        precision_gap = train_precision - val_precision
        
        details['precision_gap'] = precision_gap
        
        if precision_gap > self.precision_gap_threshold:
            warnings.append(
                f"Precision过拟合: 训练={train_precision:.4f}, 验证={val_precision:.4f}, "
                f"差距={precision_gap:.4f} > {self.precision_gap_threshold}"
            )
        
        # 3. 特征重要性集中度检测
        if feature_importance:
            sorted_importance = sorted(feature_importance.values(), reverse=True)
            if len(sorted_importance) >= 3:
                total = sum(sorted_importance)
                if total > 0:
                    top3_ratio = sum(sorted_importance[:3]) / total
                    details['top3_feature_ratio'] = top3_ratio
                    
                    if top3_ratio > self.top_feature_threshold:
                        warnings.append(
                            f"特征重要性过度集中: Top3占比={top3_ratio:.2%} > {self.top_feature_threshold:.0%}"
                        )
        
        # 4. 验证集指标过低检测
        if val_auc < 0.5:
            warnings.append(f"验证集AUC过低: {val_auc:.4f} < 0.5（不如随机）")
        
        # 生成报告
        is_overfitting = len(warnings) > 0
        
        report = {
            'is_overfitting': is_overfitting,
            'warnings': warnings,
            'details': details,
            'recommendation': self._get_recommendation(warnings) if is_overfitting else "模型泛化能力良好",
            'severity': 'high' if len(warnings) >= 2 else ('medium' if len(warnings) == 1 else 'low'),
        }
        
        return report
    
    def _get_recommendation(self, warnings: List[str]) -> str:
        """根据警告生成建议"""
        recommendations = []
        
        for warning in warnings:
            if "AUC过拟合" in warning:
                recommendations.append("增加正则化强度（L1/L2）或减少模型复杂度")
            elif "Precision过拟合" in warning:
                recommendations.append("增加负样本数量或使用类别权重平衡")
            elif "特征重要性过度集中" in warning:
                recommendations.append("考虑减少特征数量或添加更多独立特征")
            elif "AUC过低" in warning:
                recommendations.append("检查数据质量或特征有效性")
        
        return "; ".join(set(recommendations))
    
    def print_report(self, report: Dict):
        """打印检测报告"""
        print(f"\n{'='*60}")
        print(f"【过拟合检测报告】")
        print(f"{'='*60}")
        
        if report['is_overfitting']:
            print(f"⚠️ 检测到过拟合风险 (严重程度: {report['severity']})")
            print(f"\n警告:")
            for i, warning in enumerate(report['warnings'], 1):
                print(f"  {i}. {warning}")
            print(f"\n建议: {report['recommendation']}")
        else:
            print(f"✅ 未检测到过拟合")
        
        print(f"\n详细指标:")
        for key, value in report['details'].items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")


# ============================================================
# 便捷函数
# ============================================================

def run_time_series_cv(df: pd.DataFrame,
                       train_func: Callable,
                       eval_func: Callable,
                       n_splits: int = 5,
                       date_column: str = 'prediction_date') -> CVResult:
    """便捷函数：运行时序交叉验证"""
    validator = TimeSeriesCrossValidator(n_splits=n_splits)
    return validator.validate(df, train_func, eval_func, date_column)


def run_walk_forward_cv(df: pd.DataFrame,
                        train_func: Callable,
                        eval_func: Callable,
                        train_months: int = 3,
                        test_months: int = 1,
                        date_column: str = 'prediction_date') -> CVResult:
    """便捷函数：运行Walk-Forward验证"""
    validator = WalkForwardValidator(train_months=train_months, test_months=test_months)
    return validator.validate(df, train_func, eval_func, date_column)


def detect_overfitting(train_metrics: Dict,
                       val_metrics: Dict,
                       feature_importance: Dict = None) -> Dict:
    """便捷函数：检测过拟合"""
    detector = OverfittingDetector()
    return detector.detect(train_metrics, val_metrics, feature_importance)


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("测试交叉验证模块...")
    
    # 创建模拟数据
    np.random.seed(42)
    n_samples = 500
    
    # 生成日期范围
    dates = pd.date_range(start='2024-01-01', periods=n_samples, freq='D')
    
    df = pd.DataFrame({
        'prediction_date': dates.strftime('%Y-%m-%d'),
        'feature1': np.random.randn(n_samples),
        'feature2': np.random.randn(n_samples),
        'label': np.random.randint(0, 2, n_samples),
    })
    
    # 定义简单的训练和评估函数
    def simple_train(train_df):
        """简单训练函数"""
        return {'mean': train_df['feature1'].mean()}
    
    def simple_eval(model, val_df):
        """简单评估函数"""
        # 模拟指标
        return {
            'auc': np.random.uniform(0.5, 0.7),
            'precision': np.random.uniform(0.4, 0.6),
            'recall': np.random.uniform(0.4, 0.6),
            'f1': np.random.uniform(0.4, 0.6),
        }
    
    # 测试时序交叉验证
    print("\n" + "="*60)
    print("测试时序交叉验证")
    print("="*60)
    
    ts_cv = TimeSeriesCrossValidator(n_splits=3, verbose=True)
    ts_result = ts_cv.validate(df, simple_train, simple_eval)
    
    # 测试Walk-Forward验证
    print("\n" + "="*60)
    print("测试Walk-Forward验证")
    print("="*60)
    
    wf_cv = WalkForwardValidator(train_months=2, test_months=1, verbose=True)
    wf_result = wf_cv.validate(df, simple_train, simple_eval)
    
    # 测试过拟合检测
    print("\n" + "="*60)
    print("测试过拟合检测")
    print("="*60)
    
    train_metrics = {'auc': 0.85, 'precision': 0.75, 'recall': 0.70, 'f1': 0.72}
    val_metrics = {'auc': 0.65, 'precision': 0.55, 'recall': 0.60, 'f1': 0.57}
    feature_importance = {'f1': 0.5, 'f2': 0.3, 'f3': 0.15, 'f4': 0.05}
    
    detector = OverfittingDetector()
    report = detector.detect(train_metrics, val_metrics, feature_importance)
    detector.print_report(report)
