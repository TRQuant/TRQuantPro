"""
市场环境识别器 v3.0

核心设计：
1. TrendAnalyzer (80%) + HMM (20%) 加权投票
2. IBD 保留作为参考信息，不参与评价
3. 三周期（周/月/季度）独立判断
4. 动态阈值自适应
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
import json
import logging
import os

from core.market_env_features import MarketFeatureCalculator, MarketFeatures
from core.trend_analyzer_v2 import TrendAnalyzerV2, TrendAnalysisResult, TrendState
from core.hmm_v2 import HMMV2, HMMResult, HMMState

logger = logging.getLogger(__name__)


class MarketEnvironment(Enum):
    """市场环境"""
    # 牛市系列
    STRONG_BULL = "强势牛市"
    BULL = "牛市"
    WEAK_BULL = "弱势牛市"
    
    # 熊市系列
    STRONG_BEAR = "强势熊市"
    BEAR = "熊市"
    WEAK_BEAR = "弱势熊市"
    
    # 震荡系列
    HIGH_RANGE = "高位震荡"
    MID_RANGE = "中位震荡"
    LOW_RANGE = "低位震荡"
    
    # 转折系列
    RECOVERY = "复苏"
    DISTRIBUTION = "派发"
    
    NEUTRAL = "中性"
    
    @property
    def direction(self) -> int:
        """方向: 1=多, -1=空, 0=中性"""
        if self in [MarketEnvironment.STRONG_BULL, MarketEnvironment.BULL, 
                    MarketEnvironment.WEAK_BULL, MarketEnvironment.RECOVERY]:
            return 1
        elif self in [MarketEnvironment.STRONG_BEAR, MarketEnvironment.BEAR,
                     MarketEnvironment.WEAK_BEAR, MarketEnvironment.DISTRIBUTION]:
            return -1
        return 0
    
    @property
    def category(self) -> str:
        """类别"""
        if 'BULL' in self.name or self == MarketEnvironment.RECOVERY:
            return 'bull'
        elif 'BEAR' in self.name or self == MarketEnvironment.DISTRIBUTION:
            return 'bear'
        elif 'RANGE' in self.name:
            return 'range'
        return 'neutral'


@dataclass
class PeriodResult:
    """单周期结果"""
    period: str
    period_name: str
    environment: MarketEnvironment
    score: float           # -100 到 100
    confidence: float      # 0 到 100
    trend_result: Dict     # TrendAnalyzer结果
    hmm_result: Dict       # HMM结果
    
    def to_dict(self) -> dict:
        return {
            'period': self.period,
            'period_name': self.period_name,
            'environment': self.environment.name,
            'environment_name': self.environment.value,
            'direction': self.environment.direction,
            'category': self.environment.category,
            'score': round(self.score, 2),
            'confidence': round(self.confidence, 2),
            'trend_result': self.trend_result,
            'hmm_result': self.hmm_result
        }


@dataclass
class IBDReference:
    """IBD参考信息（不参与评价）"""
    market_status: str
    distribution_days: int
    follow_through_days: int
    recommendation: str
    details: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            'market_status': self.market_status,
            'distribution_days': self.distribution_days,
            'follow_through_days': self.follow_through_days,
            'recommendation': self.recommendation,
            'details': self.details,
            '_note': '仅作参考，不参与评价'
        }


@dataclass
class MarketEnvResultV3:
    """市场环境识别结果 v3"""
    # 三周期结果
    weekly: PeriodResult
    monthly: PeriodResult
    quarterly: PeriodResult
    
    # 综合结果
    combined_environment: MarketEnvironment
    combined_score: float
    combined_confidence: float
    
    # 多周期一致性
    multi_period_alignment: bool
    alignment_strength: float  # 0-100
    
    # IBD参考（不参与评价）
    ibd_reference: IBDReference
    
    # 下游参数
    position_min: float
    position_max: float
    risk_level: str
    strategy_type: str
    
    def to_dict(self) -> dict:
        return {
            'weekly': self.weekly.to_dict(),
            'monthly': self.monthly.to_dict(),
            'quarterly': self.quarterly.to_dict(),
            'combined': {
                'environment': self.combined_environment.name,
                'environment_name': self.combined_environment.value,
                'direction': self.combined_environment.direction,
                'category': self.combined_environment.category,
                'score': round(self.combined_score, 2),
                'confidence': round(self.combined_confidence, 2)
            },
            'multi_period_alignment': self.multi_period_alignment,
            'alignment_strength': round(self.alignment_strength, 2),
            'ibd_reference': self.ibd_reference.to_dict(),
            'downstream_params': {
                'position_min': self.position_min,
                'position_max': self.position_max,
                'suggested_position': (self.position_min + self.position_max) / 2,
                'risk_level': self.risk_level,
                'strategy_type': self.strategy_type
            }
        }


# 仓位映射
POSITION_MAP = {
    MarketEnvironment.STRONG_BULL: (0.8, 1.0),
    MarketEnvironment.BULL: (0.6, 0.8),
    MarketEnvironment.WEAK_BULL: (0.4, 0.6),
    MarketEnvironment.STRONG_BEAR: (0.0, 0.2),
    MarketEnvironment.BEAR: (0.1, 0.3),
    MarketEnvironment.WEAK_BEAR: (0.2, 0.4),
    MarketEnvironment.HIGH_RANGE: (0.4, 0.6),
    MarketEnvironment.MID_RANGE: (0.3, 0.5),
    MarketEnvironment.LOW_RANGE: (0.4, 0.6),
    MarketEnvironment.RECOVERY: (0.5, 0.7),
    MarketEnvironment.DISTRIBUTION: (0.2, 0.4),
    MarketEnvironment.NEUTRAL: (0.3, 0.5),
}

STRATEGY_MAP = {
    'bull': 'trend_following',
    'bear': 'defensive',
    'range': 'mean_reversion',
    'neutral': 'balanced'
}

RISK_MAP = {
    'bull': 'low',
    'bear': 'high',
    'range': 'medium',
    'neutral': 'medium'
}


class MarketEnvIdentifierV3:
    """
    市场环境识别器 v3.0
    
    权重分配：
    - TrendAnalyzer: 80%
    - HMM: 20%
    - IBD: 0%（仅作参考）
    """
    
    # 权重配置
    WEIGHTS = {
        'trend_analyzer': 0.80,
        'hmm': 0.20
    }
    
    # 周期权重
    PERIOD_WEIGHTS = {
        'weekly': 0.20,
        'monthly': 0.30,
        'quarterly': 0.50
    }
    
    def __init__(self, config_path: str = None):
        """
        初始化
        
        Args:
            config_path: 可选的配置文件路径
        """
        self.trend_analyzer = TrendAnalyzerV2()
        self.hmm_3state = HMMV2(n_states=3)
        self.hmm_5state = HMMV2(n_states=5)
        self.feature_calculator = MarketFeatureCalculator()
        
        # 加载配置
        if config_path and os.path.exists(config_path):
            self._load_config(config_path)
    
    def _load_config(self, config_path: str):
        """加载配置"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            # 可以从配置加载自定义权重等
        except Exception as e:
            logger.warning(f"加载配置失败: {e}")
    
    def identify(self, df: pd.DataFrame) -> MarketEnvResultV3:
        """
        识别市场环境
        
        Args:
            df: OHLCV数据（需要至少250天）
            
        Returns:
            MarketEnvResultV3
        """
        # 1. TrendAnalyzer分析
        trend_result = self.trend_analyzer.analyze(df)
        
        # 2. HMM分析
        hmm_result = self.hmm_3state.analyze(df)
        
        # 3. 计算三周期结果
        weekly = self._calculate_period_result('weekly', trend_result.weekly, hmm_result)
        monthly = self._calculate_period_result('monthly', trend_result.monthly, hmm_result)
        quarterly = self._calculate_period_result('quarterly', trend_result.quarterly, hmm_result)
        
        # 4. 计算综合结果
        combined_score = self._calculate_combined_score(weekly, monthly, quarterly)
        combined_confidence = self._calculate_combined_confidence(weekly, monthly, quarterly)
        combined_environment = self._score_to_environment(combined_score, 
                                                          self.feature_calculator.calculate(df))
        
        # 5. 计算多周期一致性
        alignment, alignment_strength = self._check_alignment(weekly, monthly, quarterly)
        
        # 6. IBD参考（简化实现，不参与评价）
        ibd_reference = self._get_ibd_reference(df)
        
        # 7. 获取下游参数
        position_range = POSITION_MAP.get(combined_environment, (0.3, 0.5))
        category = combined_environment.category
        
        return MarketEnvResultV3(
            weekly=weekly,
            monthly=monthly,
            quarterly=quarterly,
            combined_environment=combined_environment,
            combined_score=combined_score,
            combined_confidence=combined_confidence,
            multi_period_alignment=alignment,
            alignment_strength=alignment_strength,
            ibd_reference=ibd_reference,
            position_min=position_range[0],
            position_max=position_range[1],
            risk_level=RISK_MAP.get(category, 'medium'),
            strategy_type=STRATEGY_MAP.get(category, 'balanced')
        )
    
    def _calculate_period_result(self, 
                                  period: str,
                                  trend_period_result,
                                  hmm_result: HMMResult) -> PeriodResult:
        """计算单周期结果"""
        period_names = {'weekly': '周级别', 'monthly': '月级别', 'quarterly': '季度级别'}
        
        # TrendAnalyzer得分（-100到100）
        trend_score = trend_period_result.score
        trend_confidence = trend_period_result.confidence
        
        # HMM得分转换（-100到100）
        hmm_score = self._hmm_to_score(hmm_result)
        hmm_confidence = hmm_result.confidence
        
        # 加权组合
        combined_score = (
            trend_score * self.WEIGHTS['trend_analyzer'] +
            hmm_score * self.WEIGHTS['hmm']
        )
        
        combined_confidence = (
            trend_confidence * self.WEIGHTS['trend_analyzer'] +
            hmm_confidence * self.WEIGHTS['hmm']
        )
        
        # 转换为环境
        environment = self._trend_state_to_environment(trend_period_result.state)
        
        return PeriodResult(
            period=period,
            period_name=period_names.get(period, period),
            environment=environment,
            score=combined_score,
            confidence=combined_confidence,
            trend_result=trend_period_result.to_dict(),
            hmm_result=hmm_result.to_dict()
        )
    
    def _hmm_to_score(self, hmm_result: HMMResult) -> float:
        """将HMM结果转换为得分"""
        state = hmm_result.current_state
        confidence = hmm_result.confidence / 100  # 0-1
        
        if state == HMMState.BULL:
            return 60 * confidence
        elif state == HMMState.BEAR:
            return -60 * confidence
        elif state == HMMState.RECOVERY:
            return 40 * confidence
        elif state == HMMState.DISTRIBUTION:
            return -40 * confidence
        else:
            return 0
    
    def _trend_state_to_environment(self, trend_state: TrendState) -> MarketEnvironment:
        """TrendState转换为MarketEnvironment"""
        mapping = {
            TrendState.STRONG_BULL: MarketEnvironment.STRONG_BULL,
            TrendState.BULL: MarketEnvironment.BULL,
            TrendState.WEAK_BULL: MarketEnvironment.WEAK_BULL,
            TrendState.NEUTRAL: MarketEnvironment.NEUTRAL,
            TrendState.WEAK_BEAR: MarketEnvironment.WEAK_BEAR,
            TrendState.BEAR: MarketEnvironment.BEAR,
            TrendState.STRONG_BEAR: MarketEnvironment.STRONG_BEAR,
        }
        return mapping.get(trend_state, MarketEnvironment.NEUTRAL)
    
    def _calculate_combined_score(self,
                                   weekly: PeriodResult,
                                   monthly: PeriodResult,
                                   quarterly: PeriodResult) -> float:
        """计算综合得分"""
        return (
            weekly.score * self.PERIOD_WEIGHTS['weekly'] +
            monthly.score * self.PERIOD_WEIGHTS['monthly'] +
            quarterly.score * self.PERIOD_WEIGHTS['quarterly']
        )
    
    def _calculate_combined_confidence(self,
                                        weekly: PeriodResult,
                                        monthly: PeriodResult,
                                        quarterly: PeriodResult) -> float:
        """计算综合置信度"""
        base_confidence = (
            weekly.confidence * self.PERIOD_WEIGHTS['weekly'] +
            monthly.confidence * self.PERIOD_WEIGHTS['monthly'] +
            quarterly.confidence * self.PERIOD_WEIGHTS['quarterly']
        )
        
        # 一致性加成
        directions = [
            weekly.environment.direction,
            monthly.environment.direction,
            quarterly.environment.direction
        ]
        
        if all(d == 1 for d in directions) or all(d == -1 for d in directions):
            base_confidence = min(100, base_confidence * 1.3)
        elif len(set(directions)) == 3:
            base_confidence *= 0.7
        
        return base_confidence
    
    def _score_to_environment(self, score: float, features: MarketFeatures) -> MarketEnvironment:
        """得分转换为市场环境"""
        # 获取位置信息用于区分高/中/低位震荡
        pos_250d = features.quarterly.position_in_range
        
        if score >= 50:
            return MarketEnvironment.STRONG_BULL
        elif score >= 25:
            return MarketEnvironment.BULL
        elif score >= 10:
            return MarketEnvironment.WEAK_BULL
        elif score > -10:
            # 震荡区间
            if pos_250d > 70:
                return MarketEnvironment.HIGH_RANGE
            elif pos_250d < 30:
                return MarketEnvironment.LOW_RANGE
            else:
                return MarketEnvironment.MID_RANGE
        elif score > -25:
            return MarketEnvironment.WEAK_BEAR
        elif score > -50:
            return MarketEnvironment.BEAR
        else:
            return MarketEnvironment.STRONG_BEAR
    
    def _check_alignment(self,
                         weekly: PeriodResult,
                         monthly: PeriodResult,
                         quarterly: PeriodResult) -> Tuple[bool, float]:
        """检查多周期一致性"""
        directions = [
            weekly.environment.direction,
            monthly.environment.direction,
            quarterly.environment.direction
        ]
        
        # 计算一致性强度
        if all(d == 1 for d in directions):
            return True, 100.0
        elif all(d == -1 for d in directions):
            return True, 100.0
        elif directions.count(1) == 2:
            return True, 66.7
        elif directions.count(-1) == 2:
            return True, 66.7
        elif directions.count(0) >= 2:
            return False, 33.3
        else:
            return False, 0.0
    
    def _get_ibd_reference(self, df: pd.DataFrame) -> IBDReference:
        """
        获取IBD参考信息
        
        注意：此信息仅供参考，不参与市场环境评价
        """
        close = df['close']
        volume = df.get('volume', pd.Series([1]*len(df), index=df.index))
        
        # 简化的IBD实现
        recent = df.tail(50)
        
        # 分配日统计
        change_pct = recent['close'].pct_change() * 100
        vol_increase = recent.get('volume', pd.Series([1]*len(recent))).diff() > 0
        distribution_days = ((change_pct < -0.2) & vol_increase).sum()
        
        # 跟进日检测（简化）
        follow_through_days = ((change_pct > 1.5) & vol_increase).sum()
        
        # 市场状态
        if distribution_days >= 5:
            market_status = "market_in_correction"
            recommendation = "谨慎操作，等待确认信号"
        elif follow_through_days > 0 and distribution_days < 3:
            market_status = "confirmed_uptrend"
            recommendation = "可积极布局，但需设好止损"
        elif distribution_days >= 3:
            market_status = "uptrend_under_pressure"
            recommendation = "减少仓位，关注支撑位"
        else:
            market_status = "rally_attempt"
            recommendation = "观望为主，等待突破确认"
        
        return IBDReference(
            market_status=market_status,
            distribution_days=distribution_days,
            follow_through_days=follow_through_days,
            recommendation=recommendation,
            details={
                'recent_trend': (close.iloc[-1] / close.iloc[-20] - 1) * 100,
                'volatility': change_pct.std()
            }
        )


# 便捷函数
def identify_market_env_v3(df: pd.DataFrame = None,
                          benchmark: str = '000001.XSHG') -> MarketEnvResultV3:
    """
    识别市场环境 (v3)
    
    Args:
        df: OHLCV数据，如果不提供则使用JQData获取
        benchmark: 指数代码
        
    Returns:
        MarketEnvResultV3
    """
    identifier = MarketEnvIdentifierV3()
    
    if df is None:
        import jqdatasdk as jq
        df = jq.get_price(
            benchmark,
            count=300,
            frequency='daily',
            fields=['open', 'high', 'low', 'close', 'volume']
        )
    
    return identifier.identify(df)


def get_market_params_v3(df: pd.DataFrame = None,
                        benchmark: str = '000001.XSHG') -> Dict:
    """
    获取市场环境参数 (v3)
    
    Args:
        df: OHLCV数据
        benchmark: 指数代码
        
    Returns:
        下游参数字典
    """
    result = identify_market_env_v3(df, benchmark)
    
    return {
        # 基本信息
        'environment': result.combined_environment.name,
        'environment_name': result.combined_environment.value,
        'category': result.combined_environment.category,
        'direction': result.combined_environment.direction,
        'score': result.combined_score,
        'confidence': result.combined_confidence,
        
        # 多周期
        'weekly_env': result.weekly.environment.name,
        'monthly_env': result.monthly.environment.name,
        'quarterly_env': result.quarterly.environment.name,
        'multi_period_alignment': result.multi_period_alignment,
        
        # 仓位控制
        'position_min': result.position_min,
        'position_max': result.position_max,
        'suggested_position': (result.position_min + result.position_max) / 2,
        
        # 风险控制
        'risk_level': result.risk_level,
        'stop_loss_pct': 0.05 if result.risk_level == 'high' else (0.08 if result.risk_level == 'medium' else 0.10),
        
        # 策略选择
        'strategy_type': result.strategy_type,
        
        # IBD参考
        'ibd_reference': result.ibd_reference.to_dict()
    }


def get_env_summary_v3(result: MarketEnvResultV3) -> str:
    """生成市场环境摘要"""
    lines = []
    lines.append("=" * 60)
    lines.append("市场环境识别 v3.0 (TA 80% + HMM 20%)")
    lines.append("=" * 60)
    
    # 三周期
    for period in ['weekly', 'monthly', 'quarterly']:
        pr = getattr(result, period)
        direction = "↑" if pr.environment.direction > 0 else ("↓" if pr.environment.direction < 0 else "→")
        lines.append(f"\n【{pr.period_name}】 {direction} {pr.environment.value}")
        lines.append(f"  得分: {pr.score:+.1f} | 置信度: {pr.confidence:.1f}%")
    
    # 综合
    lines.append(f"\n{'='*40}")
    lines.append("【综合判断】")
    direction = "↑" if result.combined_environment.direction > 0 else ("↓" if result.combined_environment.direction < 0 else "→")
    lines.append(f"  环境: {direction} {result.combined_environment.value}")
    lines.append(f"  得分: {result.combined_score:+.1f}")
    lines.append(f"  置信度: {result.combined_confidence:.1f}%")
    lines.append(f"  多周期一致: {'是' if result.multi_period_alignment else '否'} ({result.alignment_strength:.0f}%)")
    
    # 下游参数
    lines.append(f"\n【建议参数】")
    lines.append(f"  仓位: {result.position_min:.0%} - {result.position_max:.0%}")
    lines.append(f"  风险: {result.risk_level}")
    lines.append(f"  策略: {result.strategy_type}")
    
    # IBD参考
    lines.append(f"\n【IBD参考】(不参与评价)")
    lines.append(f"  状态: {result.ibd_reference.market_status}")
    lines.append(f"  分配日: {result.ibd_reference.distribution_days}天")
    lines.append(f"  建议: {result.ibd_reference.recommendation}")
    
    return "\n".join(lines)

