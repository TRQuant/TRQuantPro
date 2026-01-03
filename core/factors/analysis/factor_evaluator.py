# -*- coding: utf-8 -*-
"""
因子评估器
==========

综合因子评估，提供多维度分析指标
"""
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class FactorScore:
    """因子评分"""
    factor_name: str
    ic_score: float = 0.0       # IC得分 (0-100)
    ir_score: float = 0.0       # IR得分 (0-100)
    stability_score: float = 0.0  # 稳定性得分 (0-100)
    monotonicity_score: float = 0.0  # 单调性得分 (0-100)
    turnover_score: float = 0.0  # 换手率得分 (0-100)
    total_score: float = 0.0    # 综合得分 (0-100)
    rank: int = 0
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "factor_name": self.factor_name,
            "ic_score": round(self.ic_score, 2),
            "ir_score": round(self.ir_score, 2),
            "stability_score": round(self.stability_score, 2),
            "monotonicity_score": round(self.monotonicity_score, 2),
            "turnover_score": round(self.turnover_score, 2),
            "total_score": round(self.total_score, 2),
            "rank": self.rank,
        }


class FactorEvaluator:
    """因子评估器"""
    
    def __init__(
        self,
        ic_weight: float = 0.3,
        ir_weight: float = 0.25,
        stability_weight: float = 0.2,
        monotonicity_weight: float = 0.15,
        turnover_weight: float = 0.1,
    ):
        """
        初始化
        
        Args:
            ic_weight: IC得分权重
            ir_weight: IR得分权重
            stability_weight: 稳定性得分权重
            monotonicity_weight: 单调性得分权重
            turnover_weight: 换手率得分权重
        """
        self.weights = {
            'ic': ic_weight,
            'ir': ir_weight,
            'stability': stability_weight,
            'monotonicity': monotonicity_weight,
            'turnover': turnover_weight,
        }
        
        # 标准化权重
        total = sum(self.weights.values())
        self.weights = {k: v/total for k, v in self.weights.items()}
    
    def evaluate_factor(
        self,
        factor_name: str,
        factor_data: pd.DataFrame,
        returns: pd.DataFrame,
        prices: Optional[pd.DataFrame] = None,
    ) -> FactorScore:
        """
        评估单个因子
        
        Args:
            factor_name: 因子名称
            factor_data: 因子数据
            returns: 收益率数据
            prices: 价格数据（可选，用于换手率计算）
        
        Returns:
            因子评分
        """
        # 计算IC
        ic_series = self._calculate_ic_series(factor_data, returns)
        ic_mean = ic_series.mean() if len(ic_series) > 0 else 0
        ic_std = ic_series.std() if len(ic_series) > 0 else 1
        
        # 计算各项得分
        ic_score = self._score_ic(ic_mean)
        ir_score = self._score_ir(ic_mean / (ic_std + 1e-8))
        stability_score = self._score_stability(ic_series)
        monotonicity_score = self._score_monotonicity(factor_data, returns)
        turnover_score = self._score_turnover(factor_data)
        
        # 计算综合得分
        total_score = (
            self.weights['ic'] * ic_score +
            self.weights['ir'] * ir_score +
            self.weights['stability'] * stability_score +
            self.weights['monotonicity'] * monotonicity_score +
            self.weights['turnover'] * turnover_score
        )
        
        return FactorScore(
            factor_name=factor_name,
            ic_score=ic_score,
            ir_score=ir_score,
            stability_score=stability_score,
            monotonicity_score=monotonicity_score,
            turnover_score=turnover_score,
            total_score=total_score,
            details={
                'ic_mean': ic_mean,
                'ic_std': ic_std,
                'ir': ic_mean / (ic_std + 1e-8),
                'ic_positive_ratio': (ic_series > 0).mean() if len(ic_series) > 0 else 0,
            }
        )
    
    def evaluate_factors(
        self,
        factors: Dict[str, pd.DataFrame],
        returns: pd.DataFrame,
        prices: Optional[pd.DataFrame] = None,
    ) -> List[FactorScore]:
        """
        评估多个因子并排序
        
        Args:
            factors: 因子字典 {因子名: 因子数据}
            returns: 收益率数据
            prices: 价格数据
        
        Returns:
            排序后的因子评分列表
        """
        scores = []
        for name, data in factors.items():
            score = self.evaluate_factor(name, data, returns, prices)
            scores.append(score)
        
        # 按综合得分排序
        scores.sort(key=lambda x: x.total_score, reverse=True)
        
        # 设置排名
        for i, score in enumerate(scores):
            score.rank = i + 1
        
        return scores
    
    def _calculate_ic_series(
        self,
        factor_data: pd.DataFrame,
        returns: pd.DataFrame
    ) -> pd.Series:
        """计算IC序列"""
        ic_list = []
        dates = factor_data.index.intersection(returns.index)
        
        for date in dates:
            try:
                factor_row = factor_data.loc[date].dropna()
                ret_row = returns.loc[date].dropna()
                common = factor_row.index.intersection(ret_row.index)
                
                if len(common) > 10:
                    ic = factor_row[common].rank().corr(ret_row[common].rank())
                    if not np.isnan(ic):
                        ic_list.append((date, ic))
            except:
                continue
        
        return pd.Series(dict(ic_list)) if ic_list else pd.Series()
    
    def _score_ic(self, ic_mean: float) -> float:
        """
        IC得分
        IC > 0.1: 优秀(90-100)
        IC > 0.05: 良好(70-90)
        IC > 0.03: 一般(50-70)
        IC > 0: 较弱(30-50)
        IC <= 0: 无效(0-30)
        """
        abs_ic = abs(ic_mean)
        if abs_ic > 0.1:
            return 90 + min(10, (abs_ic - 0.1) * 100)
        elif abs_ic > 0.05:
            return 70 + (abs_ic - 0.05) * 400
        elif abs_ic > 0.03:
            return 50 + (abs_ic - 0.03) * 1000
        elif abs_ic > 0:
            return 30 + abs_ic * 667
        else:
            return max(0, 30 + ic_mean * 300)
    
    def _score_ir(self, ir: float) -> float:
        """
        IR得分
        IR > 0.5: 优秀(90-100)
        IR > 0.3: 良好(70-90)
        IR > 0.1: 一般(50-70)
        IR > 0: 较弱(30-50)
        """
        abs_ir = abs(ir)
        if abs_ir > 0.5:
            return 90 + min(10, (abs_ir - 0.5) * 20)
        elif abs_ir > 0.3:
            return 70 + (abs_ir - 0.3) * 100
        elif abs_ir > 0.1:
            return 50 + (abs_ir - 0.1) * 100
        elif abs_ir > 0:
            return 30 + abs_ir * 200
        else:
            return max(0, 30 + ir * 60)
    
    def _score_stability(self, ic_series: pd.Series) -> float:
        """
        稳定性得分（IC正向比例）
        > 0.7: 优秀(90-100)
        > 0.6: 良好(70-90)
        > 0.5: 一般(50-70)
        """
        if len(ic_series) == 0:
            return 50.0
        
        positive_ratio = (ic_series > 0).mean()
        if positive_ratio > 0.7:
            return 90 + min(10, (positive_ratio - 0.7) * 33)
        elif positive_ratio > 0.6:
            return 70 + (positive_ratio - 0.6) * 200
        elif positive_ratio > 0.5:
            return 50 + (positive_ratio - 0.5) * 200
        else:
            return max(0, positive_ratio * 100)
    
    def _score_monotonicity(
        self,
        factor_data: pd.DataFrame,
        returns: pd.DataFrame,
        quantiles: int = 5
    ) -> float:
        """
        单调性得分（分位数收益单调递增/递减）
        """
        try:
            quantile_returns = []
            dates = factor_data.index.intersection(returns.index)
            
            for date in list(dates)[:50]:  # 采样计算
                factor_row = factor_data.loc[date].dropna()
                ret_row = returns.loc[date].dropna()
                common = factor_row.index.intersection(ret_row.index)
                
                if len(common) < quantiles * 5:
                    continue
                
                factor_values = factor_row[common]
                ret_values = ret_row[common]
                
                try:
                    bins = pd.qcut(factor_values, quantiles, labels=False, duplicates='drop')
                    q_ret = [ret_values[bins == q].mean() for q in range(quantiles)]
                    quantile_returns.append(q_ret)
                except:
                    continue
            
            if not quantile_returns:
                return 50.0
            
            # 计算平均分位数收益
            avg_returns = np.mean(quantile_returns, axis=0)
            
            # 检查单调性
            diffs = np.diff(avg_returns)
            if np.all(diffs > 0) or np.all(diffs < 0):
                return 100.0  # 完全单调
            
            # 计算单调程度
            monotonic_ratio = max(
                np.sum(diffs > 0) / len(diffs),
                np.sum(diffs < 0) / len(diffs)
            )
            
            return monotonic_ratio * 100
            
        except Exception as e:
            logger.debug(f"单调性计算失败: {e}")
            return 50.0
    
    def _score_turnover(self, factor_data: pd.DataFrame) -> float:
        """
        换手率得分（因子值变化频率，低换手更好）
        """
        try:
            # 计算因子排名变化
            ranks = factor_data.rank(axis=1, pct=True)
            rank_changes = ranks.diff().abs()
            avg_change = rank_changes.mean().mean()
            
            # 换手率越低得分越高
            if avg_change < 0.1:
                return 90 + min(10, (0.1 - avg_change) * 100)
            elif avg_change < 0.2:
                return 70 + (0.2 - avg_change) * 200
            elif avg_change < 0.3:
                return 50 + (0.3 - avg_change) * 200
            else:
                return max(0, 50 - (avg_change - 0.3) * 100)
                
        except Exception as e:
            logger.debug(f"换手率计算失败: {e}")
            return 50.0
    
    def generate_report(self, scores: List[FactorScore]) -> Dict[str, Any]:
        """生成因子评估报告"""
        if not scores:
            return {"error": "无因子评分数据"}
        
        report = {
            "total_factors": len(scores),
            "top_factors": [s.to_dict() for s in scores[:5]],
            "average_score": np.mean([s.total_score for s in scores]),
            "score_distribution": {
                "excellent": len([s for s in scores if s.total_score >= 80]),
                "good": len([s for s in scores if 60 <= s.total_score < 80]),
                "average": len([s for s in scores if 40 <= s.total_score < 60]),
                "poor": len([s for s in scores if s.total_score < 40]),
            },
            "all_factors": [s.to_dict() for s in scores],
        }
        
        return report
