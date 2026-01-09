"""
V3.0 A股动量评分模块
====================

专为A股设计的动量评分系统，包含以下特性:

1. A股特征适配:
   - 涨跌停板机制 (±10%/20%)
   - T+1交易制度
   - 北向资金影响
   - 板块联动效应
   - 连板股的特殊动量

2. 多维度评分:
   - 价格动量 (短/中/长期)
   - 相对强度 (RS Rating)
   - 成交量动量
   - 资金流动量
   - 情绪动量 (涨停/连板)

3. 可扩展接口:
   - 自定义因子权重
   - 自定义评分函数
   - 插件式因子扩展
   - 回测反馈优化
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Callable, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ============ 可扩展接口定义 ============

class MomentumFactorBase(ABC):
    """
    动量因子基类 - 可扩展接口
    
    实现自定义因子只需继承此类并实现 calculate 方法
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """因子名称"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """因子描述"""
        pass
    
    @property
    def weight(self) -> float:
        """默认权重"""
        return 1.0
    
    @abstractmethod
    def calculate(self, data: Dict[str, Any]) -> float:
        """
        计算因子值
        
        Args:
            data: 股票数据字典，包含价格、成交量等
            
        Returns:
            0-100的评分
        """
        pass


# ============ 内置动量因子 ============

class PriceMomentumFactor(MomentumFactorBase):
    """价格动量因子"""
    
    @property
    def name(self) -> str:
        return "价格动量"
    
    @property
    def description(self) -> str:
        return "基于价格变化的动量评分 (5/10/20/60日)"
    
    def __init__(self, periods: List[int] = None, weights: List[float] = None):
        self.periods = periods or [5, 10, 20, 60]
        self.weights = weights or [0.35, 0.30, 0.20, 0.15]
    
    def calculate(self, data: Dict[str, Any]) -> float:
        score = 0.0
        
        for period, weight in zip(self.periods, self.weights):
            mom_key = f"mom_{period}d"
            if mom_key in data and data[mom_key] is not None:
                mom = data[mom_key] * 100  # 转换为百分比
                # 映射到0-100分
                # 涨幅10%=80分, 0%=50分, -10%=20分
                period_score = max(0, min(100, 50 + mom * 3))
                score += period_score * weight
        
        return score


class RelativeStrengthFactor(MomentumFactorBase):
    """相对强度因子 (IBD RS Rating)"""
    
    @property
    def name(self) -> str:
        return "相对强度"
    
    @property
    def description(self) -> str:
        return "相对于大盘的强度评分 (IBD RS Rating风格)"
    
    def __init__(self, benchmark: str = "000300.XSHG"):
        self.benchmark = benchmark
    
    def calculate(self, data: Dict[str, Any]) -> float:
        # 计算相对强度
        rs_252d = data.get("rs_252d", 50)  # 年度相对强度
        rs_63d = data.get("rs_63d", 50)    # 季度相对强度
        
        # 权重: 年度 0.4 + 季度 0.6 (IBD风格)
        score = rs_252d * 0.4 + rs_63d * 0.6
        
        return max(0, min(100, score))


class VolumeMomentumFactor(MomentumFactorBase):
    """成交量动量因子"""
    
    @property
    def name(self) -> str:
        return "成交量动量"
    
    @property
    def description(self) -> str:
        return "基于成交量变化的动量评分"
    
    def calculate(self, data: Dict[str, Any]) -> float:
        vol_ratio = data.get("vol_ratio", 1.0)  # 量比
        vol_ma_ratio = data.get("vol_ma_ratio", 1.0)  # 成交量/均量比
        
        # 量比评分 (1.5-3为最佳)
        if 1.5 <= vol_ratio <= 3.0:
            vol_score = 80 + (vol_ratio - 1.5) * 10
        elif vol_ratio > 3.0:
            vol_score = max(50, 100 - (vol_ratio - 3.0) * 5)  # 过高扣分
        else:
            vol_score = 50 + (vol_ratio - 1.0) * 30
        
        # 均量比评分
        if vol_ma_ratio >= 1.2:
            ma_score = min(100, 70 + (vol_ma_ratio - 1.0) * 15)
        else:
            ma_score = max(30, 50 + (vol_ma_ratio - 1.0) * 50)
        
        return max(0, min(100, vol_score * 0.6 + ma_score * 0.4))


class FundsFlowFactor(MomentumFactorBase):
    """资金流动量因子"""
    
    @property
    def name(self) -> str:
        return "资金流动量"
    
    @property
    def description(self) -> str:
        return "基于资金流入流出的动量评分"
    
    def calculate(self, data: Dict[str, Any]) -> float:
        net_inflow = data.get("net_inflow", 0)  # 主力净流入(亿)
        north_flow = data.get("north_flow", 0)  # 北向资金净流入(亿)
        
        # 主力净流入评分
        # 净流入>1亿=高分, 0=中等, <-1亿=低分
        if net_inflow > 0:
            main_score = min(100, 60 + net_inflow * 10)
        else:
            main_score = max(0, 60 + net_inflow * 15)
        
        # 北向资金评分
        if north_flow > 0:
            north_score = min(100, 60 + north_flow * 5)
        else:
            north_score = max(0, 60 + north_flow * 8)
        
        return max(0, min(100, main_score * 0.7 + north_score * 0.3))


class SentimentMomentumFactor(MomentumFactorBase):
    """情绪动量因子 (A股特色)"""
    
    @property
    def name(self) -> str:
        return "情绪动量"
    
    @property
    def description(self) -> str:
        return "基于涨停板、连板等A股特有指标的动量评分"
    
    def calculate(self, data: Dict[str, Any]) -> float:
        # 涨停历史
        limit_up_count = data.get("limit_up_count_20d", 0)  # 20日涨停次数
        continuous_limit = data.get("continuous_limit", 0)  # 连板次数
        
        # 价格位置
        price_pos_60d = data.get("price_pos_60d", 0.5)  # 60日价格位置
        
        # 涨停评分 (A股特色)
        if continuous_limit >= 3:
            limit_score = min(100, 70 + continuous_limit * 5)  # 连板加分
        elif limit_up_count >= 2:
            limit_score = 60 + limit_up_count * 5
        elif limit_up_count >= 1:
            limit_score = 55
        else:
            limit_score = 45
        
        # 价格位置评分 (0.3-0.7为最佳, 不追高不抄底)
        if 0.3 <= price_pos_60d <= 0.7:
            pos_score = 80
        elif price_pos_60d > 0.7:
            pos_score = max(40, 80 - (price_pos_60d - 0.7) * 100)  # 过高扣分
        else:
            pos_score = max(40, 80 - (0.3 - price_pos_60d) * 100)  # 过低扣分
        
        return max(0, min(100, limit_score * 0.6 + pos_score * 0.4))


class TrendConfirmationFactor(MomentumFactorBase):
    """趋势确认因子"""
    
    @property
    def name(self) -> str:
        return "趋势确认"
    
    @property
    def description(self) -> str:
        return "基于均线、MACD等确认趋势的评分"
    
    def calculate(self, data: Dict[str, Any]) -> float:
        # 均线多头排列
        ma_alignment = data.get("ma_alignment", 0)  # 1=多头, 0=混乱, -1=空头
        
        # 金叉信号
        golden_cross = data.get("ma_golden_cross", 0)  # 1=金叉, 0=无, -1=死叉
        
        # MACD
        macd_hist = data.get("macd_hist", 0)
        macd_trend = data.get("macd_trend", 0)  # 1=上升, -1=下降
        
        # 均线评分
        if ma_alignment > 0:
            ma_score = 80
        elif ma_alignment == 0:
            ma_score = 50
        else:
            ma_score = 20
        
        # 金叉评分
        cross_score = 50 + golden_cross * 30
        
        # MACD评分
        if macd_hist > 0 and macd_trend > 0:
            macd_score = 85
        elif macd_hist > 0:
            macd_score = 65
        elif macd_hist < 0 and macd_trend < 0:
            macd_score = 15
        else:
            macd_score = 35
        
        return max(0, min(100, ma_score * 0.4 + cross_score * 0.3 + macd_score * 0.3))


# ============ V3 专用数据结构 ============

@dataclass
class MomentumScoreV3:
    """V3.0 动量评分结果"""
    
    # 股票信息
    stock_code: str
    stock_name: str = ""
    
    # 综合评分
    total_score: float = 0.0
    rank: int = 0
    
    # 各因子得分
    factor_scores: Dict[str, float] = field(default_factory=dict)
    
    # 评级和信号
    rating: str = "C"  # A/B/C/D/F
    signal: str = "观察"  # 强买/买入/持有/观察/卖出
    
    # 原始数据
    change_pct: float = 0.0
    volume_ratio: float = 1.0
    
    def to_dict(self) -> Dict:
        return {
            "stock_code": self.stock_code,
            "stock_name": self.stock_name,
            "total_score": round(self.total_score, 1),
            "rank": self.rank,
            "rating": self.rating,
            "signal": self.signal,
            "factor_scores": {k: round(v, 1) for k, v in self.factor_scores.items()},
            "change_pct": round(self.change_pct, 2),
            "volume_ratio": round(self.volume_ratio, 2),
        }


# ============ A股动量评分器 ============

class MomentumScorerV3:
    """
    V3.0 A股动量评分器
    
    特性:
    1. 内置6个A股适配的动量因子
    2. 支持自定义因子扩展
    3. 可配置权重
    4. 回测反馈接口
    
    使用示例:
    ```python
    scorer = MomentumScorerV3()
    
    # 计算单只股票
    result = scorer.score_stock("000001.XSHE", stock_data)
    
    # 批量计算
    results = scorer.score_stocks(stocks_data)
    
    # 添加自定义因子
    scorer.add_factor(MyCustomFactor(), weight=0.15)
    
    # 获取前20强
    top20 = scorer.get_top_momentum(20)
    ```
    """
    
    # 默认因子权重配置
    DEFAULT_FACTOR_WEIGHTS = {
        "价格动量": 0.30,
        "相对强度": 0.20,
        "成交量动量": 0.15,
        "资金流动量": 0.15,
        "情绪动量": 0.10,
        "趋势确认": 0.10,
    }
    
    def __init__(
        self,
        factor_weights: Optional[Dict[str, float]] = None,
        use_builtin_factors: bool = True,
    ):
        """
        初始化
        
        Args:
            factor_weights: 自定义因子权重
            use_builtin_factors: 是否使用内置因子
        """
        self.factors: List[MomentumFactorBase] = []
        self.factor_weights = factor_weights or self.DEFAULT_FACTOR_WEIGHTS.copy()
        self._results: List[MomentumScoreV3] = []
        
        if use_builtin_factors:
            self._init_builtin_factors()
    
    def _init_builtin_factors(self):
        """初始化内置因子"""
        self.factors = [
            PriceMomentumFactor(),
            RelativeStrengthFactor(),
            VolumeMomentumFactor(),
            FundsFlowFactor(),
            SentimentMomentumFactor(),
            TrendConfirmationFactor(),
        ]
        logger.info(f"MomentumScorerV3: 已加载 {len(self.factors)} 个内置因子")
    
    def add_factor(
        self,
        factor: MomentumFactorBase,
        weight: float = 0.1,
        replace_existing: bool = False,
    ):
        """
        添加自定义因子
        
        Args:
            factor: 因子实例
            weight: 权重
            replace_existing: 是否替换同名因子
        """
        if replace_existing:
            self.factors = [f for f in self.factors if f.name != factor.name]
        
        self.factors.append(factor)
        self.factor_weights[factor.name] = weight
        
        # 归一化权重
        total_weight = sum(self.factor_weights.values())
        if total_weight > 0:
            self.factor_weights = {k: v / total_weight for k, v in self.factor_weights.items()}
        
        logger.info(f"MomentumScorerV3: 添加因子 '{factor.name}', 权重={weight:.2f}")
    
    def remove_factor(self, factor_name: str):
        """移除因子"""
        self.factors = [f for f in self.factors if f.name != factor_name]
        if factor_name in self.factor_weights:
            del self.factor_weights[factor_name]
        logger.info(f"MomentumScorerV3: 移除因子 '{factor_name}'")
    
    def set_weight(self, factor_name: str, weight: float):
        """设置因子权重"""
        if factor_name in self.factor_weights:
            self.factor_weights[factor_name] = weight
            logger.info(f"MomentumScorerV3: 设置因子 '{factor_name}' 权重={weight:.2f}")
    
    def score_stock(self, stock_code: str, data: Dict[str, Any]) -> MomentumScoreV3:
        """
        计算单只股票的动量评分
        
        Args:
            stock_code: 股票代码
            data: 股票数据字典
            
        Returns:
            MomentumScoreV3 评分结果
        """
        result = MomentumScoreV3(
            stock_code=stock_code,
            stock_name=data.get("name", ""),
            change_pct=data.get("change_pct", 0),
            volume_ratio=data.get("vol_ratio", 1),
        )
        
        # 计算各因子得分
        total_score = 0.0
        total_weight = 0.0
        
        for factor in self.factors:
            try:
                score = factor.calculate(data)
                weight = self.factor_weights.get(factor.name, 0.1)
                
                result.factor_scores[factor.name] = score
                total_score += score * weight
                total_weight += weight
                
            except Exception as e:
                logger.warning(f"因子 '{factor.name}' 计算失败: {e}")
                result.factor_scores[factor.name] = 50  # 默认中等分
        
        # 计算综合得分
        if total_weight > 0:
            result.total_score = total_score / total_weight * total_weight  # 已加权
        
        # 设置评级和信号
        result.rating = self._get_rating(result.total_score)
        result.signal = self._get_signal(result.total_score)
        
        return result
    
    def score_stocks(self, stocks_data: Dict[str, Dict]) -> List[MomentumScoreV3]:
        """
        批量计算动量评分
        
        Args:
            stocks_data: {stock_code: data_dict} 格式的数据
            
        Returns:
            排序后的评分结果列表
        """
        results = []
        
        for stock_code, data in stocks_data.items():
            try:
                result = self.score_stock(stock_code, data)
                results.append(result)
            except Exception as e:
                logger.warning(f"股票 {stock_code} 评分失败: {e}")
        
        # 排序并设置排名
        results.sort(key=lambda x: x.total_score, reverse=True)
        for i, r in enumerate(results):
            r.rank = i + 1
        
        self._results = results
        return results
    
    def get_top_momentum(self, n: int = 20) -> List[MomentumScoreV3]:
        """获取前N强动量股"""
        return self._results[:n] if self._results else []
    
    def get_high_momentum(self, threshold: float = 70) -> List[MomentumScoreV3]:
        """获取高动量股 (得分 >= threshold)"""
        return [r for r in self._results if r.total_score >= threshold]
    
    def _get_rating(self, score: float) -> str:
        """获取评级"""
        if score >= 85:
            return "A+"
        elif score >= 75:
            return "A"
        elif score >= 65:
            return "B+"
        elif score >= 55:
            return "B"
        elif score >= 45:
            return "C"
        elif score >= 35:
            return "D"
        else:
            return "F"
    
    def _get_signal(self, score: float) -> str:
        """获取信号"""
        if score >= 80:
            return "强买"
        elif score >= 65:
            return "买入"
        elif score >= 50:
            return "持有"
        elif score >= 35:
            return "观察"
        else:
            return "卖出"
    
    def update_weights_from_backtest(
        self,
        backtest_results: Dict[str, float],
        learning_rate: float = 0.1,
    ):
        """
        根据回测结果更新因子权重
        
        Args:
            backtest_results: {factor_name: return_contribution} 回测中各因子贡献
            learning_rate: 学习率
        """
        # 计算调整
        total_contribution = sum(abs(v) for v in backtest_results.values())
        if total_contribution == 0:
            return
        
        for factor_name, contribution in backtest_results.items():
            if factor_name in self.factor_weights:
                # 正贡献增加权重，负贡献减少权重
                adjustment = contribution / total_contribution * learning_rate
                new_weight = max(0.05, self.factor_weights[factor_name] + adjustment)
                self.factor_weights[factor_name] = new_weight
        
        # 归一化
        total = sum(self.factor_weights.values())
        self.factor_weights = {k: v / total for k, v in self.factor_weights.items()}
        
        logger.info(f"MomentumScorerV3: 权重已更新 - {self.factor_weights}")
    
    def get_factor_info(self) -> List[Dict]:
        """获取因子信息列表"""
        return [
            {
                "name": f.name,
                "description": f.description,
                "weight": round(self.factor_weights.get(f.name, 0) * 100, 1),
            }
            for f in self.factors
        ]
    
    def get_summary(self) -> str:
        """获取评分摘要"""
        if not self._results:
            return "暂无评分结果"
        
        high_momentum = len([r for r in self._results if r.total_score >= 70])
        very_high = len([r for r in self._results if r.total_score >= 85])
        
        top5 = self._results[:5]
        top5_text = "\n".join([
            f"   {i+1}. {r.stock_name or r.stock_code} ({r.total_score:.1f}分) - {r.signal}"
            for i, r in enumerate(top5)
        ])
        
        summary = f"""
📊 动量评分摘要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 统计:
   • 评分股票: {len(self._results)} 只
   • 极强动量(≥85): {very_high} 只
   • 强动量(≥70): {high_momentum} 只

🏆 Top 5 动量股:
{top5_text}

📊 因子权重:
   • 价格动量: {self.factor_weights.get('价格动量', 0)*100:.0f}%
   • 相对强度: {self.factor_weights.get('相对强度', 0)*100:.0f}%
   • 成交量动量: {self.factor_weights.get('成交量动量', 0)*100:.0f}%
   • 资金流动量: {self.factor_weights.get('资金流动量', 0)*100:.0f}%
   • 情绪动量: {self.factor_weights.get('情绪动量', 0)*100:.0f}%
   • 趋势确认: {self.factor_weights.get('趋势确认', 0)*100:.0f}%
"""
        return summary.strip()


# ============ 便捷函数 ============

def score_momentum(
    stocks_data: Dict[str, Dict],
    factor_weights: Optional[Dict[str, float]] = None,
) -> List[MomentumScoreV3]:
    """
    便捷函数：计算动量评分
    
    Args:
        stocks_data: 股票数据字典
        factor_weights: 自定义权重
        
    Returns:
        评分结果列表
    """
    scorer = MomentumScorerV3(factor_weights=factor_weights)
    return scorer.score_stocks(stocks_data)


def get_top_momentum(
    stocks_data: Dict[str, Dict],
    n: int = 20,
) -> List[MomentumScoreV3]:
    """
    便捷函数：获取前N强动量股
    """
    scorer = MomentumScorerV3()
    scorer.score_stocks(stocks_data)
    return scorer.get_top_momentum(n)
