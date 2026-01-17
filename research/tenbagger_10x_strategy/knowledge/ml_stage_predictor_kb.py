#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ML Stage Predictor Knowledge Base - ML阶段预测知识库
====================================================

使用机器学习方法预测十倍股阶段转换：

1. 特征工程定义
2. 阶段转换预测模型
3. 评分与排序算法
4. 防过拟合策略

注意：使用简单ML方法，避免复杂依赖
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import numpy as np


# ============== 特征定义 ==============

class FeatureCategory(Enum):
    """特征类别"""
    FUNDAMENTAL = "基本面"
    TECHNICAL = "技术面"
    ALTDATA = "另类数据"
    MARKET = "市场环境"


@dataclass
class FeatureDefinition:
    """特征定义"""
    name: str
    category: FeatureCategory
    description: str
    importance: float  # 重要性 0-1
    normalization: str  # 归一化方法: minmax/zscore/log/none
    missing_strategy: str  # 缺失处理: mean/median/zero/drop


# 十倍股阶段预测特征集
STAGE_PREDICTION_FEATURES = {
    # ========== 基本面特征 ==========
    "roe": FeatureDefinition(
        name="roe",
        category=FeatureCategory.FUNDAMENTAL,
        description="净资产收益率",
        importance=0.12,
        normalization="zscore",
        missing_strategy="median"
    ),
    "roe_trend": FeatureDefinition(
        name="roe_trend",
        category=FeatureCategory.FUNDAMENTAL,
        description="ROE变化趋势(同比)",
        importance=0.10,
        normalization="zscore",
        missing_strategy="zero"
    ),
    "revenue_growth": FeatureDefinition(
        name="revenue_growth",
        category=FeatureCategory.FUNDAMENTAL,
        description="营收增速",
        importance=0.15,
        normalization="zscore",
        missing_strategy="zero"
    ),
    "profit_growth": FeatureDefinition(
        name="profit_growth",
        category=FeatureCategory.FUNDAMENTAL,
        description="净利润增速",
        importance=0.15,
        normalization="zscore",
        missing_strategy="zero"
    ),
    "gross_margin": FeatureDefinition(
        name="gross_margin",
        category=FeatureCategory.FUNDAMENTAL,
        description="毛利率",
        importance=0.08,
        normalization="minmax",
        missing_strategy="median"
    ),
    "gross_margin_trend": FeatureDefinition(
        name="gross_margin_trend",
        category=FeatureCategory.FUNDAMENTAL,
        description="毛利率变化",
        importance=0.06,
        normalization="zscore",
        missing_strategy="zero"
    ),
    "operating_cash_flow": FeatureDefinition(
        name="operating_cash_flow",
        category=FeatureCategory.FUNDAMENTAL,
        description="经营现金流/营收",
        importance=0.07,
        normalization="zscore",
        missing_strategy="median"
    ),
    
    # ========== 技术面特征 ==========
    "momentum_20d": FeatureDefinition(
        name="momentum_20d",
        category=FeatureCategory.TECHNICAL,
        description="20日涨幅",
        importance=0.08,
        normalization="zscore",
        missing_strategy="zero"
    ),
    "momentum_60d": FeatureDefinition(
        name="momentum_60d",
        category=FeatureCategory.TECHNICAL,
        description="60日涨幅",
        importance=0.06,
        normalization="zscore",
        missing_strategy="zero"
    ),
    "relative_strength": FeatureDefinition(
        name="relative_strength",
        category=FeatureCategory.TECHNICAL,
        description="相对强度(vs指数)",
        importance=0.07,
        normalization="zscore",
        missing_strategy="zero"
    ),
    "volume_ratio": FeatureDefinition(
        name="volume_ratio",
        category=FeatureCategory.TECHNICAL,
        description="成交量比率(vs 20日均)",
        importance=0.05,
        normalization="log",
        missing_strategy="mean"
    ),
    "price_position": FeatureDefinition(
        name="price_position",
        category=FeatureCategory.TECHNICAL,
        description="价格位置(0-1区间)",
        importance=0.04,
        normalization="none",
        missing_strategy="mean"
    ),
    
    # ========== 另类数据特征 ==========
    "altdata_score": FeatureDefinition(
        name="altdata_score",
        category=FeatureCategory.ALTDATA,
        description="另类数据综合评分",
        importance=0.10,
        normalization="minmax",
        missing_strategy="zero"
    ),
    "event_count": FeatureDefinition(
        name="event_count",
        category=FeatureCategory.ALTDATA,
        description="近期事件数量",
        importance=0.05,
        normalization="log",
        missing_strategy="zero"
    ),
    
    # ========== 市场环境特征 ==========
    "market_regime_score": FeatureDefinition(
        name="market_regime_score",
        category=FeatureCategory.MARKET,
        description="市场环境评分(-100~100)",
        importance=0.08,
        normalization="minmax",
        missing_strategy="zero"
    ),
    "sector_momentum": FeatureDefinition(
        name="sector_momentum",
        category=FeatureCategory.MARKET,
        description="所属板块动量",
        importance=0.06,
        normalization="zscore",
        missing_strategy="zero"
    ),
}


# ============== 阶段转换概率模型 ==============

class StageTransitionModel:
    """阶段转换概率模型
    
    使用加权评分法替代复杂ML模型，避免过拟合
    """
    
    # 各阶段对应的特征权重（基于历史研究）
    STAGE_FEATURE_WEIGHTS = {
        "S0_to_S1": {
            "revenue_growth": 0.20,
            "profit_growth": 0.15,
            "altdata_score": 0.25,
            "event_count": 0.20,
            "momentum_20d": 0.10,
            "market_regime_score": 0.10,
        },
        "S1_to_S2": {
            "revenue_growth": 0.25,
            "profit_growth": 0.25,
            "gross_margin_trend": 0.15,
            "altdata_score": 0.15,
            "relative_strength": 0.10,
            "volume_ratio": 0.10,
        },
        "S2_to_S3": {
            "revenue_growth": 0.30,
            "profit_growth": 0.30,
            "roe_trend": 0.15,
            "operating_cash_flow": 0.10,
            "momentum_60d": 0.10,
            "sector_momentum": 0.05,
        },
        "S3_to_S4": {
            "roe": 0.20,
            "gross_margin": 0.15,
            "operating_cash_flow": 0.20,
            "profit_growth": 0.20,
            "relative_strength": 0.15,
            "market_regime_score": 0.10,
        },
    }
    
    # 阶段转换阈值
    TRANSITION_THRESHOLDS = {
        "S0_to_S1": 0.55,
        "S1_to_S2": 0.60,
        "S2_to_S3": 0.65,
        "S3_to_S4": 0.70,
    }
    
    def __init__(self):
        self.feature_stats = {}  # 用于归一化的统计信息
        
    def normalize_features(self, features: Dict[str, float]) -> Dict[str, float]:
        """特征归一化"""
        normalized = {}
        
        for name, value in features.items():
            if name not in STAGE_PREDICTION_FEATURES:
                continue
                
            feature_def = STAGE_PREDICTION_FEATURES[name]
            
            # 处理缺失值
            if value is None or np.isnan(value):
                if feature_def.missing_strategy == "zero":
                    value = 0
                elif feature_def.missing_strategy == "mean":
                    value = self.feature_stats.get(f"{name}_mean", 0)
                elif feature_def.missing_strategy == "median":
                    value = self.feature_stats.get(f"{name}_median", 0)
                else:
                    continue
                    
            # 归一化
            if feature_def.normalization == "minmax":
                min_val = self.feature_stats.get(f"{name}_min", 0)
                max_val = self.feature_stats.get(f"{name}_max", 1)
                if max_val > min_val:
                    value = (value - min_val) / (max_val - min_val)
                else:
                    value = 0.5
            elif feature_def.normalization == "zscore":
                mean_val = self.feature_stats.get(f"{name}_mean", 0)
                std_val = self.feature_stats.get(f"{name}_std", 1)
                if std_val > 0:
                    value = (value - mean_val) / std_val
                    value = 1 / (1 + np.exp(-value))  # sigmoid映射到0-1
                else:
                    value = 0.5
            elif feature_def.normalization == "log":
                value = np.log1p(max(value, 0))
                value = min(value / 5, 1)  # 经验归一化
                
            normalized[name] = np.clip(value, 0, 1)
            
        return normalized
    
    def predict_transition_probability(self, 
                                        current_stage: str,
                                        features: Dict[str, float]) -> Tuple[float, str, Dict]:
        """预测阶段转换概率
        
        Args:
            current_stage: 当前阶段 (S0, S1, S2, S3)
            features: 特征字典
            
        Returns:
            (转换概率, 下一阶段, 详细信息)
        """
        transition_key = f"{current_stage}_to_S{int(current_stage[1]) + 1}"
        
        if transition_key not in self.STAGE_FEATURE_WEIGHTS:
            return 0.0, current_stage, {"error": "Invalid stage"}
            
        weights = self.STAGE_FEATURE_WEIGHTS[transition_key]
        threshold = self.TRANSITION_THRESHOLDS[transition_key]
        
        # 归一化特征
        norm_features = self.normalize_features(features)
        
        # 计算加权分数
        score = 0.0
        feature_contributions = {}
        total_weight = 0.0
        
        for feature_name, weight in weights.items():
            if feature_name in norm_features:
                contribution = norm_features[feature_name] * weight
                score += contribution
                feature_contributions[feature_name] = {
                    "value": norm_features[feature_name],
                    "weight": weight,
                    "contribution": contribution
                }
                total_weight += weight
                
        # 归一化分数
        if total_weight > 0:
            score = score / total_weight
            
        # 判断是否转换
        next_stage = f"S{int(current_stage[1]) + 1}" if score >= threshold else current_stage
        
        return score, next_stage, {
            "current_stage": current_stage,
            "transition_key": transition_key,
            "score": score,
            "threshold": threshold,
            "will_transition": score >= threshold,
            "feature_contributions": feature_contributions
        }
    
    def predict_final_stage(self, features: Dict[str, float], 
                            initial_stage: str = "S0") -> Tuple[str, float, List[Dict]]:
        """预测最终阶段
        
        从初始阶段开始，连续预测直到无法转换
        
        Returns:
            (最终阶段, 总置信度, 转换路径)
        """
        current_stage = initial_stage
        total_confidence = 1.0
        path = []
        
        for _ in range(5):  # 最多5次转换
            if current_stage[1] >= '4':
                break
                
            prob, next_stage, details = self.predict_transition_probability(
                current_stage, features
            )
            
            path.append({
                "from": current_stage,
                "to": next_stage,
                "probability": prob,
                "transitioned": next_stage != current_stage
            })
            
            if next_stage == current_stage:
                break
                
            total_confidence *= prob
            current_stage = next_stage
            
        return current_stage, total_confidence, path


# ============== 十倍股评分排序算法 ==============

class TenbaggerRanker:
    """十倍股排序器
    
    综合评分排序，选出最有潜力的候选
    """
    
    SCORING_WEIGHTS = {
        "stage_probability": 0.30,    # 阶段转换概率
        "fundamental_score": 0.25,    # 基本面评分
        "momentum_score": 0.15,       # 动量评分
        "altdata_score": 0.15,        # 另类数据评分
        "valuation_score": 0.10,      # 估值评分
        "risk_score": 0.05,           # 风险调整
    }
    
    def __init__(self):
        self.transition_model = StageTransitionModel()
        
    def calculate_comprehensive_score(self, 
                                       stock_data: Dict[str, Any]) -> Tuple[float, Dict]:
        """计算综合评分
        
        Args:
            stock_data: {
                'features': {...},
                'current_stage': 'S1',
                'fundamental_metrics': {...},
                'technical_metrics': {...},
                'altdata_metrics': {...},
            }
            
        Returns:
            (综合评分0-100, 详细分数)
        """
        scores = {}
        details = {}
        
        features = stock_data.get('features', {})
        current_stage = stock_data.get('current_stage', 'S0')
        
        # 1. 阶段转换概率评分
        prob, predicted_stage, trans_details = self.transition_model.predict_transition_probability(
            current_stage, features
        )
        scores['stage_probability'] = prob * 100
        details['stage_prediction'] = trans_details
        
        # 2. 基本面评分
        fundamental = stock_data.get('fundamental_metrics', {})
        fund_score = self._calc_fundamental_score(fundamental)
        scores['fundamental_score'] = fund_score
        details['fundamental'] = {"score": fund_score}
        
        # 3. 动量评分
        technical = stock_data.get('technical_metrics', {})
        momentum_score = self._calc_momentum_score(technical)
        scores['momentum_score'] = momentum_score
        details['momentum'] = {"score": momentum_score}
        
        # 4. 另类数据评分
        altdata = stock_data.get('altdata_metrics', {})
        altdata_score = altdata.get('score', 50)
        scores['altdata_score'] = altdata_score
        details['altdata'] = {"score": altdata_score}
        
        # 5. 估值评分
        valuation = stock_data.get('valuation_metrics', {})
        val_score = self._calc_valuation_score(valuation)
        scores['valuation_score'] = val_score
        details['valuation'] = {"score": val_score}
        
        # 6. 风险调整
        risk = stock_data.get('risk_metrics', {})
        risk_score = self._calc_risk_score(risk)
        scores['risk_score'] = 100 - risk_score  # 风险越低分数越高
        details['risk'] = {"score": risk_score}
        
        # 综合评分
        total_score = sum(
            scores[k] * self.SCORING_WEIGHTS[k] 
            for k in self.SCORING_WEIGHTS
        )
        
        details['component_scores'] = scores
        details['total_score'] = total_score
        
        return total_score, details
    
    def _calc_fundamental_score(self, metrics: Dict) -> float:
        """计算基本面评分"""
        score = 50  # 基础分
        
        # ROE评分
        roe = metrics.get('roe', 0)
        if roe > 20:
            score += 15
        elif roe > 15:
            score += 10
        elif roe > 10:
            score += 5
            
        # 成长性评分
        growth = metrics.get('profit_growth', 0)
        if growth > 0.5:
            score += 20
        elif growth > 0.3:
            score += 15
        elif growth > 0.15:
            score += 10
            
        # 毛利率评分
        margin = metrics.get('gross_margin', 0)
        if margin > 0.4:
            score += 10
        elif margin > 0.3:
            score += 5
            
        # 现金流评分
        cf = metrics.get('operating_cash_flow', 0)
        if cf > 0.15:
            score += 5
        elif cf < 0:
            score -= 10
            
        return np.clip(score, 0, 100)
    
    def _calc_momentum_score(self, metrics: Dict) -> float:
        """计算动量评分"""
        score = 50
        
        m20 = metrics.get('momentum_20d', 0)
        m60 = metrics.get('momentum_60d', 0)
        rs = metrics.get('relative_strength', 0)
        
        # 短期动量
        if m20 > 0.15:
            score += 15
        elif m20 > 0.08:
            score += 10
        elif m20 < -0.10:
            score -= 15
            
        # 中期动量
        if m60 > 0.30:
            score += 15
        elif m60 > 0.15:
            score += 10
        elif m60 < -0.20:
            score -= 15
            
        # 相对强度
        if rs > 0.10:
            score += 10
        elif rs > 0.05:
            score += 5
        elif rs < -0.05:
            score -= 10
            
        return np.clip(score, 0, 100)
    
    def _calc_valuation_score(self, metrics: Dict) -> float:
        """计算估值评分"""
        score = 50
        
        pe = metrics.get('pe', 30)
        peg = metrics.get('peg', 1)
        pb = metrics.get('pb', 3)
        
        # PEG评分（核心）
        if 0 < peg < 0.5:
            score += 25
        elif 0.5 <= peg < 1:
            score += 15
        elif 1 <= peg < 1.5:
            score += 5
        elif peg > 2:
            score -= 10
            
        # PE评分
        if 10 < pe < 25:
            score += 10
        elif 25 <= pe < 40:
            score += 5
        elif pe > 60:
            score -= 10
            
        return np.clip(score, 0, 100)
    
    def _calc_risk_score(self, metrics: Dict) -> float:
        """计算风险评分（越高风险越大）"""
        score = 30  # 基础风险
        
        volatility = metrics.get('volatility', 0.3)
        beta = metrics.get('beta', 1.0)
        debt_ratio = metrics.get('debt_ratio', 0.5)
        
        # 波动率风险
        if volatility > 0.5:
            score += 20
        elif volatility > 0.35:
            score += 10
            
        # Beta风险
        if beta > 1.5:
            score += 15
        elif beta > 1.2:
            score += 10
            
        # 负债风险
        if debt_ratio > 0.7:
            score += 15
        elif debt_ratio > 0.5:
            score += 10
            
        return np.clip(score, 0, 100)
    
    def rank_candidates(self, candidates: List[Dict]) -> List[Dict]:
        """对候选股票排序
        
        Args:
            candidates: [{stock_code, stock_data}, ...]
            
        Returns:
            排序后的候选列表（含评分）
        """
        ranked = []
        
        for candidate in candidates:
            stock_code = candidate.get('stock_code', '')
            stock_data = candidate.get('stock_data', {})
            
            score, details = self.calculate_comprehensive_score(stock_data)
            
            ranked.append({
                'stock_code': stock_code,
                'score': score,
                'details': details,
                'predicted_stage': details.get('stage_prediction', {}).get('next_stage', 'S0'),
                'rank': 0  # 稍后填充
            })
            
        # 排序
        ranked.sort(key=lambda x: x['score'], reverse=True)
        
        # 添加排名
        for i, item in enumerate(ranked):
            item['rank'] = i + 1
            
        return ranked


# ============== 防过拟合策略 ==============

ANTI_OVERFIT_STRATEGIES = {
    "cross_validation": {
        "method": "时间序列交叉验证",
        "description": "使用滚动窗口，确保训练集在测试集之前",
        "n_splits": 5,
        "gap_days": 30  # 训练集和测试集间隔
    },
    
    "feature_selection": {
        "method": "特征重要性筛选",
        "description": "只使用重要性>0.05的特征",
        "min_importance": 0.05,
        "max_features": 15
    },
    
    "regularization": {
        "method": "加权评分正则化",
        "description": "权重衰减防止过度依赖单一特征",
        "weight_decay": 0.1
    },
    
    "ensemble": {
        "method": "多周期集成",
        "description": "综合短期、中期、长期特征",
        "periods": ["20d", "60d", "120d"]
    },
    
    "out_of_sample": {
        "method": "样本外验证",
        "description": "保留最近6个月数据作为验证集",
        "holdout_months": 6
    }
}


# ============== 导出 ==============

__all__ = [
    'FeatureCategory',
    'FeatureDefinition',
    'STAGE_PREDICTION_FEATURES',
    'StageTransitionModel',
    'TenbaggerRanker',
    'ANTI_OVERFIT_STRATEGIES'
]







































