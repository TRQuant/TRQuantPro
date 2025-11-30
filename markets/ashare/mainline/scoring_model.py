"""
A股主线识别 - 专业级评分模型

参考行业先进水平设计：
1. 多因子加权评分体系
2. 动态权重调整机制
3. 行业轮动时钟模型
4. 风险调整收益评估

评分维度（参考华泰、中金等券商研究框架）：
- 政策支持度 (Policy Score)
- 资金认可度 (Capital Score)
- 产业景气度 (Industry Score)
- 技术形态度 (Technical Score)
- 估值合理度 (Valuation Score)
- 前瞻领先度 (Foresight Score)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from datetime import datetime
import logging
import math

logger = logging.getLogger(__name__)


class ScoreLevel(Enum):
    """评分等级"""
    VERY_HIGH = "very_high"    # 90-100
    HIGH = "high"              # 75-89
    MEDIUM = "medium"          # 60-74
    LOW = "low"                # 40-59
    VERY_LOW = "very_low"      # 0-39


@dataclass
class FactorScore:
    """单因子评分"""
    name: str                    # 因子名称
    raw_value: float             # 原始值
    normalized_score: float      # 标准化得分 (0-100)
    weight: float                # 权重
    weighted_score: float        # 加权得分
    data_source: str             # 数据来源
    calculation_method: str      # 计算方法
    confidence: float            # 置信度 (0-1)
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "raw_value": self.raw_value,
            "normalized_score": round(self.normalized_score, 2),
            "weight": self.weight,
            "weighted_score": round(self.weighted_score, 2),
            "data_source": self.data_source,
            "calculation_method": self.calculation_method,
            "confidence": round(self.confidence, 2),
        }


@dataclass
class DimensionScore:
    """维度评分（包含多个因子）"""
    dimension: str               # 维度名称
    factors: List[FactorScore]   # 因子列表
    total_score: float           # 维度总分
    weight: float                # 维度权重
    weighted_score: float        # 加权得分
    level: ScoreLevel            # 评分等级
    interpretation: str          # 解读
    
    def to_dict(self) -> Dict:
        return {
            "dimension": self.dimension,
            "factors": [f.to_dict() for f in self.factors],
            "total_score": round(self.total_score, 2),
            "weight": self.weight,
            "weighted_score": round(self.weighted_score, 2),
            "level": self.level.value,
            "interpretation": self.interpretation,
        }


@dataclass
class MainlineScore:
    """主线综合评分"""
    mainline_name: str
    dimensions: List[DimensionScore]
    total_score: float
    level: ScoreLevel
    recommendation: str          # 投资建议
    risk_warning: str            # 风险提示
    analysis_time: datetime
    llm_analysis: Optional[str] = None  # LLM分析结论
    
    def to_dict(self) -> Dict:
        return {
            "mainline_name": self.mainline_name,
            "dimensions": [d.to_dict() for d in self.dimensions],
            "total_score": round(self.total_score, 2),
            "level": self.level.value,
            "recommendation": self.recommendation,
            "risk_warning": self.risk_warning,
            "analysis_time": self.analysis_time.isoformat(),
            "llm_analysis": self.llm_analysis,
        }


# ============================================================
# 评分参数配置（行业先进水平）
# ============================================================

SCORING_CONFIG = {
    # 维度权重配置（参考中金、华泰多因子框架）
    "dimension_weights": {
        "policy": 0.20,       # 政策支持度
        "capital": 0.25,      # 资金认可度
        "industry": 0.20,     # 产业景气度
        "technical": 0.15,    # 技术形态度
        "valuation": 0.10,    # 估值合理度
        "foresight": 0.10,    # 前瞻领先度
    },
    
    # 政策支持度因子
    "policy_factors": {
        "policy_mention_freq": {
            "weight": 0.30,
            "description": "近期政策提及频率",
            "data_source": "政策文件/新闻",
            "calculation": "近30天政策提及次数，标准化到0-100",
            "thresholds": {"high": 10, "medium": 5, "low": 2},
        },
        "policy_strength": {
            "weight": 0.35,
            "description": "政策支持力度",
            "data_source": "政策文件分析",
            "calculation": "政策级别×支持方向，1-5分制",
            "thresholds": {"high": 4, "medium": 3, "low": 2},
        },
        "policy_continuity": {
            "weight": 0.20,
            "description": "政策持续性",
            "data_source": "历史政策分析",
            "calculation": "连续支持月数/预期持续时间",
            "thresholds": {"high": 12, "medium": 6, "low": 3},
        },
        "policy_implementation": {
            "weight": 0.15,
            "description": "政策落地进度",
            "data_source": "执行情况跟踪",
            "calculation": "已落地措施数/计划措施数",
            "thresholds": {"high": 0.8, "medium": 0.5, "low": 0.3},
        },
    },
    
    # 资金认可度因子
    "capital_factors": {
        "northbound_flow": {
            "weight": 0.25,
            "description": "北向资金净流入",
            "data_source": "沪深港通数据",
            "calculation": "20日北向净流入/板块流通市值",
            "thresholds": {"high": 0.02, "medium": 0.01, "low": 0.005},
        },
        "main_force_flow": {
            "weight": 0.25,
            "description": "主力资金净流入",
            "data_source": "东方财富资金流向",
            "calculation": "5日主力净流入/板块成交额",
            "thresholds": {"high": 0.15, "medium": 0.08, "low": 0.03},
        },
        "institutional_holding": {
            "weight": 0.20,
            "description": "机构持仓变化",
            "data_source": "基金/保险持仓",
            "calculation": "季度机构持仓变化率",
            "thresholds": {"high": 0.10, "medium": 0.05, "low": 0.02},
        },
        "margin_trading": {
            "weight": 0.15,
            "description": "两融余额变化",
            "data_source": "交易所两融数据",
            "calculation": "20日融资余额变化率",
            "thresholds": {"high": 0.10, "medium": 0.05, "low": 0.02},
        },
        "etf_flow": {
            "weight": 0.15,
            "description": "行业ETF资金流入",
            "data_source": "ETF份额变化",
            "calculation": "20日ETF份额变化率",
            "thresholds": {"high": 0.08, "medium": 0.04, "low": 0.02},
        },
    },
    
    # 产业景气度因子
    "industry_factors": {
        "revenue_growth": {
            "weight": 0.25,
            "description": "行业收入增速",
            "data_source": "上市公司财报",
            "calculation": "行业整体营收同比增速",
            "thresholds": {"high": 0.20, "medium": 0.10, "low": 0.05},
        },
        "profit_growth": {
            "weight": 0.25,
            "description": "行业利润增速",
            "data_source": "上市公司财报",
            "calculation": "行业整体净利润同比增速",
            "thresholds": {"high": 0.25, "medium": 0.15, "low": 0.08},
        },
        "order_backlog": {
            "weight": 0.20,
            "description": "订单/合同负债",
            "data_source": "上市公司财报",
            "calculation": "合同负债同比增速",
            "thresholds": {"high": 0.30, "medium": 0.15, "low": 0.05},
        },
        "capacity_utilization": {
            "weight": 0.15,
            "description": "产能利用率",
            "data_source": "行业协会/统计局",
            "calculation": "产能利用率水平",
            "thresholds": {"high": 0.85, "medium": 0.75, "low": 0.65},
        },
        "price_trend": {
            "weight": 0.15,
            "description": "产品价格趋势",
            "data_source": "行业价格指数",
            "calculation": "产品价格同比变化",
            "thresholds": {"high": 0.10, "medium": 0.05, "low": 0.00},
        },
    },
    
    # 技术形态度因子
    "technical_factors": {
        "trend_strength": {
            "weight": 0.30,
            "description": "趋势强度",
            "data_source": "行情数据计算",
            "calculation": "ADX指标，>25为强趋势",
            "thresholds": {"high": 35, "medium": 25, "low": 15},
        },
        "ma_alignment": {
            "weight": 0.25,
            "description": "均线多头排列",
            "data_source": "行情数据计算",
            "calculation": "MA5>MA10>MA20>MA60得分",
            "thresholds": {"high": 4, "medium": 3, "low": 2},
        },
        "volume_price": {
            "weight": 0.20,
            "description": "量价配合度",
            "data_source": "行情数据计算",
            "calculation": "上涨放量/下跌缩量程度",
            "thresholds": {"high": 0.8, "medium": 0.6, "low": 0.4},
        },
        "breakout_signal": {
            "weight": 0.15,
            "description": "突破信号",
            "data_source": "行情数据计算",
            "calculation": "近期突破关键位置次数",
            "thresholds": {"high": 3, "medium": 2, "low": 1},
        },
        "rsi_macd": {
            "weight": 0.10,
            "description": "动量指标",
            "data_source": "行情数据计算",
            "calculation": "RSI+MACD综合得分",
            "thresholds": {"high": 70, "medium": 50, "low": 30},
        },
    },
    
    # 估值合理度因子
    "valuation_factors": {
        "pe_percentile": {
            "weight": 0.35,
            "description": "PE历史分位",
            "data_source": "行情数据计算",
            "calculation": "当前PE在5年历史分位",
            "thresholds": {"low": 0.30, "medium": 0.50, "high": 0.70},  # 估值越低越好
            "inverse": True,
        },
        "pb_percentile": {
            "weight": 0.25,
            "description": "PB历史分位",
            "data_source": "行情数据计算",
            "calculation": "当前PB在5年历史分位",
            "thresholds": {"low": 0.30, "medium": 0.50, "high": 0.70},
            "inverse": True,
        },
        "peg_ratio": {
            "weight": 0.25,
            "description": "PEG比率",
            "data_source": "财报+预期",
            "calculation": "PE/预期盈利增速",
            "thresholds": {"low": 0.8, "medium": 1.2, "high": 2.0},
            "inverse": True,
        },
        "dividend_yield": {
            "weight": 0.15,
            "description": "股息率",
            "data_source": "财报数据",
            "calculation": "近12个月股息/股价",
            "thresholds": {"high": 0.03, "medium": 0.02, "low": 0.01},
        },
    },
    
    # 前瞻领先度因子
    "foresight_factors": {
        "leading_indicator": {
            "weight": 0.30,
            "description": "领先指标变化",
            "data_source": "宏观先行指标",
            "calculation": "PMI新订单-产成品库存",
            "thresholds": {"high": 5, "medium": 2, "low": 0},
        },
        "catalyst_density": {
            "weight": 0.25,
            "description": "催化剂密度",
            "data_source": "事件日历",
            "calculation": "未来30天重要事件数",
            "thresholds": {"high": 5, "medium": 3, "low": 1},
        },
        "consensus_revision": {
            "weight": 0.25,
            "description": "盈利预期调整",
            "data_source": "分析师预期",
            "calculation": "近30天EPS预期调整幅度",
            "thresholds": {"high": 0.05, "medium": 0.02, "low": 0.00},
        },
        "global_trend": {
            "weight": 0.20,
            "description": "全球产业趋势",
            "data_source": "海外市场/研报",
            "calculation": "全球同行业表现相关性",
            "thresholds": {"high": 0.7, "medium": 0.5, "low": 0.3},
        },
    },
}


class ScoringModel:
    """专业级评分模型"""
    
    def __init__(self, config: Dict = None):
        self.config = config or SCORING_CONFIG
        self.dimension_weights = self.config["dimension_weights"]
    
    def calculate_mainline_score(
        self,
        mainline_name: str,
        raw_data: Dict[str, Any],
        llm_analysis: Optional[str] = None
    ) -> MainlineScore:
        """
        计算主线综合评分
        
        Args:
            mainline_name: 主线名称
            raw_data: 原始数据，格式：
                {
                    "policy": {...},
                    "capital": {...},
                    "industry": {...},
                    "technical": {...},
                    "valuation": {...},
                    "foresight": {...},
                }
            llm_analysis: LLM分析结论
        
        Returns:
            MainlineScore: 综合评分结果
        """
        dimensions = []
        
        # 计算各维度得分
        for dim_name, dim_weight in self.dimension_weights.items():
            dim_data = raw_data.get(dim_name, {})
            dim_score = self._calculate_dimension_score(dim_name, dim_data, dim_weight)
            dimensions.append(dim_score)
        
        # 计算总分
        total_score = sum(d.weighted_score for d in dimensions)
        level = self._get_score_level(total_score)
        
        # 生成投资建议
        recommendation = self._generate_recommendation(total_score, dimensions)
        risk_warning = self._generate_risk_warning(dimensions)
        
        return MainlineScore(
            mainline_name=mainline_name,
            dimensions=dimensions,
            total_score=total_score,
            level=level,
            recommendation=recommendation,
            risk_warning=risk_warning,
            analysis_time=datetime.now(),
            llm_analysis=llm_analysis,
        )
    
    def _calculate_dimension_score(
        self,
        dimension: str,
        data: Dict,
        weight: float
    ) -> DimensionScore:
        """计算维度得分"""
        factors_config = self.config.get(f"{dimension}_factors", {})
        factors = []
        
        for factor_name, factor_config in factors_config.items():
            raw_value = data.get(factor_name, 0)
            
            # 标准化得分
            thresholds = factor_config.get("thresholds", {})
            inverse = factor_config.get("inverse", False)
            normalized = self._normalize_score(raw_value, thresholds, inverse)
            
            # 加权得分
            factor_weight = factor_config.get("weight", 0.2)
            weighted = normalized * factor_weight
            
            factors.append(FactorScore(
                name=factor_name,
                raw_value=raw_value,
                normalized_score=normalized,
                weight=factor_weight,
                weighted_score=weighted,
                data_source=factor_config.get("data_source", "未知"),
                calculation_method=factor_config.get("calculation", ""),
                confidence=data.get(f"{factor_name}_confidence", 0.8),
            ))
        
        # 维度总分
        total = sum(f.weighted_score for f in factors) if factors else 50
        level = self._get_score_level(total)
        
        # 维度解读
        interpretation = self._interpret_dimension(dimension, total, factors)
        
        return DimensionScore(
            dimension=dimension,
            factors=factors,
            total_score=total,
            weight=weight,
            weighted_score=total * weight,
            level=level,
            interpretation=interpretation,
        )
    
    def _normalize_score(
        self,
        value: float,
        thresholds: Dict,
        inverse: bool = False
    ) -> float:
        """标准化得分到0-100"""
        high = thresholds.get("high", 1)
        medium = thresholds.get("medium", 0.5)
        low = thresholds.get("low", 0)
        
        if inverse:
            # 反向指标（如估值，越低越好）
            if value <= low:
                score = 90
            elif value <= medium:
                score = 70 + 20 * (medium - value) / (medium - low)
            elif value <= high:
                score = 50 + 20 * (high - value) / (high - medium)
            else:
                score = max(10, 50 - 40 * (value - high) / high)
        else:
            # 正向指标
            if value >= high:
                score = 90
            elif value >= medium:
                score = 70 + 20 * (value - medium) / (high - medium)
            elif value >= low:
                score = 50 + 20 * (value - low) / (medium - low)
            else:
                score = max(10, 50 * value / low) if low > 0 else 30
        
        return min(100, max(0, score))
    
    def _get_score_level(self, score: float) -> ScoreLevel:
        """获取评分等级"""
        if score >= 90:
            return ScoreLevel.VERY_HIGH
        elif score >= 75:
            return ScoreLevel.HIGH
        elif score >= 60:
            return ScoreLevel.MEDIUM
        elif score >= 40:
            return ScoreLevel.LOW
        else:
            return ScoreLevel.VERY_LOW
    
    def _interpret_dimension(
        self,
        dimension: str,
        score: float,
        factors: List[FactorScore]
    ) -> str:
        """生成维度解读"""
        interpretations = {
            "policy": {
                "very_high": "政策强力支持，处于政策红利期",
                "high": "政策环境友好，有明确支持方向",
                "medium": "政策中性，无明显利好利空",
                "low": "政策关注度下降，需警惕政策转向",
                "very_low": "政策可能收紧，存在政策风险",
            },
            "capital": {
                "very_high": "资金大幅流入，机构高度认可",
                "high": "资金持续流入，市场关注度高",
                "medium": "资金流向中性，观望情绪较重",
                "low": "资金流出迹象，需关注趋势变化",
                "very_low": "资金大幅流出，市场分歧明显",
            },
            "industry": {
                "very_high": "产业景气度极高，处于高速增长期",
                "high": "产业景气向上，基本面持续改善",
                "medium": "产业景气平稳，增长动能一般",
                "low": "产业景气下行，需关注基本面变化",
                "very_low": "产业景气低迷，基本面承压",
            },
            "technical": {
                "very_high": "技术形态极强，多头趋势明确",
                "high": "技术形态良好，上升趋势中",
                "medium": "技术形态中性，震荡整理",
                "low": "技术形态转弱，需警惕回调",
                "very_low": "技术形态破位，下降趋势中",
            },
            "valuation": {
                "very_high": "估值极具吸引力，安全边际高",
                "high": "估值合理偏低，性价比较好",
                "medium": "估值处于中等水平",
                "low": "估值偏高，需关注业绩兑现",
                "very_low": "估值过高，存在估值风险",
            },
            "foresight": {
                "very_high": "前瞻指标极强，领先优势明显",
                "high": "前瞻指标向好，预期改善",
                "medium": "前瞻指标中性，趋势不明",
                "low": "前瞻指标转弱，需关注拐点",
                "very_low": "前瞻指标恶化，下行风险大",
            },
        }
        
        level = self._get_score_level(score)
        return interpretations.get(dimension, {}).get(level.value, "")
    
    def _generate_recommendation(
        self,
        total_score: float,
        dimensions: List[DimensionScore]
    ) -> str:
        """生成投资建议"""
        if total_score >= 85:
            return "强烈推荐：多维度指标优异，建议积极配置"
        elif total_score >= 75:
            return "推荐：整体表现良好，建议适度超配"
        elif total_score >= 65:
            return "中性偏多：基本面尚可，建议标配并关注边际变化"
        elif total_score >= 55:
            return "中性：观望为主，等待更明确信号"
        elif total_score >= 45:
            return "中性偏空：多项指标转弱，建议低配"
        else:
            return "回避：风险较大，建议规避或减仓"
    
    def _generate_risk_warning(self, dimensions: List[DimensionScore]) -> str:
        """生成风险提示"""
        warnings = []
        
        for dim in dimensions:
            if dim.level in [ScoreLevel.LOW, ScoreLevel.VERY_LOW]:
                dim_names = {
                    "policy": "政策风险",
                    "capital": "资金流出风险",
                    "industry": "基本面下行风险",
                    "technical": "技术破位风险",
                    "valuation": "估值泡沫风险",
                    "foresight": "预期下修风险",
                }
                warnings.append(dim_names.get(dim.dimension, dim.dimension))
        
        if warnings:
            return "⚠️ 风险提示：" + "、".join(warnings)
        return "✅ 暂无明显风险信号"


# 全局实例
scoring_model = ScoringModel()

