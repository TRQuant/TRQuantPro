"""
市场环境识别模块 v1.0

核心设计：
1. 统一的市场状态定义（14状态）
2. 三种识别方法：TrendAnalyzer, HMM, IBD
3. 多方法投票机制
4. 输出结构化参数供下游使用

市场状态定义（基于历史数据客观定义）：
- 牛市系列: BULL_STRONG, BULL_NORMAL, BULL_LATE, BULL_PULLBACK
- 熊市系列: BEAR_STRONG, BEAR_NORMAL, BEAR_LATE, BEAR_BOUNCE
- 震荡系列: RANGE_HIGH, RANGE_MID, RANGE_LOW, RANGE_WIDE
- 转折系列: TURNING_UP, TURNING_DOWN
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
import json
import logging

logger = logging.getLogger(__name__)


class MarketState(Enum):
    """14种市场状态"""
    # 牛市系列
    BULL_STRONG = "强势牛市"
    BULL_NORMAL = "正常牛市"
    BULL_LATE = "牛市晚期"
    BULL_PULLBACK = "牛市回调"
    
    # 熊市系列
    BEAR_STRONG = "强势熊市"
    BEAR_NORMAL = "正常熊市"
    BEAR_LATE = "熊市晚期"
    BEAR_BOUNCE = "熊市反弹"
    
    # 震荡系列
    RANGE_HIGH = "高位震荡"
    RANGE_MID = "中位震荡"
    RANGE_LOW = "低位震荡"
    RANGE_WIDE = "宽幅震荡"
    
    # 转折系列
    TURNING_UP = "转折向上"
    TURNING_DOWN = "转折向下"
    
    # 未知
    UNKNOWN = "未知"
    
    @property
    def category(self) -> str:
        """返回状态类别"""
        if self.name.startswith('BULL'):
            return 'bull'
        elif self.name.startswith('BEAR'):
            return 'bear'
        elif self.name.startswith('RANGE'):
            return 'range'
        elif self.name.startswith('TURNING'):
            return 'turning'
        return 'unknown'


@dataclass
class MethodResult:
    """单个方法的识别结果"""
    method_name: str
    state: MarketState
    confidence: float  # 0-100
    details: Dict = field(default_factory=dict)


@dataclass
class MarketEnvResult:
    """市场环境识别最终结果"""
    # 最终状态
    state: MarketState
    category: str  # bull/bear/range/turning
    confidence: float  # 0-100
    
    # 三种方法的结果
    trend_result: Optional[MethodResult] = None
    hmm_result: Optional[MethodResult] = None
    ibd_result: Optional[MethodResult] = None
    
    # 一致性
    consensus: int = 0  # 0-3, 几种方法一致
    
    # 指标值
    indicators: Dict = field(default_factory=dict)
    
    # 下游参数
    position_advice: Tuple[float, float] = (0.3, 0.5)
    risk_level: str = "medium"  # low/medium/high
    
    def to_dict(self) -> dict:
        return {
            'state': self.state.name,
            'state_name': self.state.value,
            'category': self.category,
            'confidence': self.confidence,
            'consensus': self.consensus,
            'position_advice': self.position_advice,
            'risk_level': self.risk_level,
            'methods': {
                'trend': self.trend_result.state.name if self.trend_result else None,
                'hmm': self.hmm_result.state.name if self.hmm_result else None,
                'ibd': self.ibd_result.state.name if self.ibd_result else None,
            },
            'indicators': self.indicators
        }


class TrendAnalyzer:
    """
    方法1: 趋势分析器
    
    使用多周期动量和均线关系识别市场状态
    """
    
    def __init__(self, thresholds: Dict = None):
        self.thresholds = thresholds or {
            'long_bull': {'mom_120': 10, 'vs_ma250': 5},
            'long_bear': {'mom_120': -10, 'vs_ma250': -5},
            'mid_bull': {'mom_60': 5, 'vs_ma60': 0},
            'mid_bear': {'mom_60': -5, 'vs_ma60': 0},
            'short_bull': {'mom_20': 2},
            'short_bear': {'mom_20': -2}
        }
    
    def analyze(self, df: pd.DataFrame) -> MethodResult:
        """分析市场趋势"""
        df = self._calculate_indicators(df)
        row = df.iloc[-1]
        
        # 提取指标
        mom_20 = row.get('mom_20d', 0)
        mom_60 = row.get('mom_60d', 0)
        mom_120 = row.get('mom_120d', 0)
        vs_ma60 = row.get('vs_ma60', 0)
        vs_ma250 = row.get('vs_ma250', 0)
        pos_60d = row.get('pos_60d', 50)
        pos_250d = row.get('pos_250d', 50)
        ma_bull = row.get('ma_bull', 0)
        ma_bear = row.get('ma_bear', 0)
        vol = row.get('volatility', 15)
        
        # 趋势判断
        th = self.thresholds
        long_bull = mom_120 > th['long_bull']['mom_120'] and vs_ma250 > th['long_bull']['vs_ma250']
        long_bear = mom_120 < th['long_bear']['mom_120'] and vs_ma250 < th['long_bear']['vs_ma250']
        mid_bull = mom_60 > th['mid_bull']['mom_60'] and vs_ma60 > th['mid_bull']['vs_ma60']
        mid_bear = mom_60 < th['mid_bear']['mom_60'] and vs_ma60 < th['mid_bear']['vs_ma60']
        short_bull = mom_20 > th['short_bull']['mom_20']
        short_bear = mom_20 < th['short_bear']['mom_20']
        
        # 状态识别
        state = MarketState.UNKNOWN
        confidence = 50
        
        if long_bull:
            if mid_bull and short_bull and ma_bull:
                state = MarketState.BULL_STRONG
                confidence = 90
            elif mid_bull and not short_bull:
                state = MarketState.BULL_PULLBACK
                confidence = 70
            elif not mid_bull and mom_60 > 0:
                state = MarketState.BULL_LATE
                confidence = 60
            else:
                state = MarketState.BULL_NORMAL
                confidence = 65
        
        elif long_bear:
            if mid_bear and short_bear and ma_bear:
                state = MarketState.BEAR_STRONG
                confidence = 90
            elif mid_bear and not short_bear:
                state = MarketState.BEAR_BOUNCE
                confidence = 70
            elif not mid_bear and mom_60 < 0:
                state = MarketState.BEAR_LATE
                confidence = 60
            else:
                state = MarketState.BEAR_NORMAL
                confidence = 65
        
        elif mom_120 < -5 and mom_60 > 0 and short_bull and pos_60d > 60:
            state = MarketState.TURNING_UP
            confidence = 75
        
        elif mom_120 > 5 and mom_60 < 0 and short_bear and pos_60d < 40:
            state = MarketState.TURNING_DOWN
            confidence = 75
        
        else:
            # 震荡系列
            if pos_250d > 70:
                state = MarketState.RANGE_HIGH
                confidence = 60
            elif pos_250d < 30:
                state = MarketState.RANGE_LOW
                confidence = 60
            elif vol > 25:
                state = MarketState.RANGE_WIDE
                confidence = 55
            else:
                state = MarketState.RANGE_MID
                confidence = 50
        
        return MethodResult(
            method_name='TrendAnalyzer',
            state=state,
            confidence=confidence,
            details={
                'mom_20': mom_20,
                'mom_60': mom_60,
                'mom_120': mom_120,
                'vs_ma60': vs_ma60,
                'vs_ma250': vs_ma250,
                'pos_60d': pos_60d,
                'pos_250d': pos_250d
            }
        )
    
    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算指标"""
        df = df.copy()
        close = df['close']
        
        for p in [5, 10, 20, 60, 120, 250]:
            df[f'ma{p}'] = close.rolling(p, min_periods=1).mean()
        
        df['mom_20d'] = close.pct_change(20) * 100
        df['mom_60d'] = close.pct_change(60) * 100
        df['mom_120d'] = close.pct_change(120) * 100
        
        df['vs_ma60'] = (close / df['ma60'] - 1) * 100
        df['vs_ma250'] = (close / df['ma250'] - 1) * 100
        
        df['high_60d'] = close.rolling(60, min_periods=1).max()
        df['low_60d'] = close.rolling(60, min_periods=1).min()
        df['pos_60d'] = (close - df['low_60d']) / (df['high_60d'] - df['low_60d'] + 0.001) * 100
        
        df['high_250d'] = close.rolling(250, min_periods=1).max()
        df['low_250d'] = close.rolling(250, min_periods=1).min()
        df['pos_250d'] = (close - df['low_250d']) / (df['high_250d'] - df['low_250d'] + 0.001) * 100
        
        df['ma_bull'] = ((df['ma5'] > df['ma20']) & (df['ma20'] > df['ma60']) & (df['ma60'] > df['ma120'])).astype(int)
        df['ma_bear'] = ((df['ma5'] < df['ma20']) & (df['ma20'] < df['ma60']) & (df['ma60'] < df['ma120'])).astype(int)
        
        returns = close.pct_change()
        df['volatility'] = returns.rolling(20, min_periods=1).std() * np.sqrt(252) * 100
        
        return df


class HMMAnalyzer:
    """
    方法2: 隐马尔可夫模型分析器
    
    使用日收益率、波动率、成交量变化识别隐藏的市场状态
    """
    
    def __init__(self):
        # 三状态HMM: 牛市/熊市/震荡
        self.state_map = {
            0: 'bull',
            1: 'bear', 
            2: 'range'
        }
        
        # A股参数（基于历史数据调优）
        self.emission_params = {
            'bull': {'return_mean': 0.10, 'return_std': 1.2, 'vol_mean': 18, 'vol_std': 5},
            'bear': {'return_mean': -0.12, 'return_std': 1.8, 'vol_mean': 25, 'vol_std': 8},
            'range': {'return_mean': 0.02, 'return_std': 0.8, 'vol_mean': 14, 'vol_std': 4}
        }
        
        # 转移概率矩阵
        self.transition_matrix = np.array([
            [0.92, 0.03, 0.05],  # bull -> bull/bear/range
            [0.03, 0.90, 0.07],  # bear -> bull/bear/range
            [0.08, 0.07, 0.85]   # range -> bull/bear/range
        ])
    
    def analyze(self, df: pd.DataFrame) -> MethodResult:
        """分析市场状态"""
        df = self._calculate_observations(df)
        
        # 使用最近60天数据
        recent = df.tail(60)
        
        # 简化版：基于观测变量直接判断
        returns = recent['daily_return'].dropna()
        vol = recent['rolling_vol'].dropna()
        
        avg_return = returns.mean()
        avg_vol = vol.mean() if len(vol) > 0 else 15
        recent_return = returns.tail(20).mean() if len(returns) >= 20 else avg_return
        
        # 计算各状态的概率得分
        scores = {}
        for state_name, params in self.emission_params.items():
            return_score = self._gaussian_score(recent_return, params['return_mean'], params['return_std'])
            vol_score = self._gaussian_score(avg_vol, params['vol_mean'], params['vol_std'])
            scores[state_name] = return_score * vol_score
        
        # 选择最高得分状态
        total = sum(scores.values())
        probs = {k: v/total for k, v in scores.items()} if total > 0 else {'range': 1}
        
        best_state = max(probs, key=probs.get)
        confidence = probs[best_state] * 100
        
        # 映射到14状态
        state_mapping = {
            'bull': MarketState.BULL_NORMAL,
            'bear': MarketState.BEAR_NORMAL,
            'range': MarketState.RANGE_MID
        }
        
        # 细化状态
        if best_state == 'bull':
            if recent_return > 0.2:
                state = MarketState.BULL_STRONG
            elif avg_vol > 20:
                state = MarketState.BULL_LATE
            else:
                state = MarketState.BULL_NORMAL
        elif best_state == 'bear':
            if recent_return < -0.2:
                state = MarketState.BEAR_STRONG
            elif recent_return > 0:
                state = MarketState.BEAR_BOUNCE
            else:
                state = MarketState.BEAR_NORMAL
        else:
            if avg_vol > 22:
                state = MarketState.RANGE_WIDE
            else:
                state = MarketState.RANGE_MID
        
        return MethodResult(
            method_name='HMM',
            state=state,
            confidence=confidence,
            details={
                'avg_return': avg_return,
                'recent_return': recent_return,
                'avg_vol': avg_vol,
                'state_probs': probs
            }
        )
    
    def _calculate_observations(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算观测变量"""
        df = df.copy()
        close = df['close']
        
        df['daily_return'] = close.pct_change() * 100
        df['rolling_vol'] = df['daily_return'].rolling(20).std() * np.sqrt(252)
        
        if 'volume' in df.columns:
            df['vol_ratio'] = df['volume'] / df['volume'].rolling(20).mean()
        
        return df
    
    def _gaussian_score(self, x, mean, std):
        """高斯概率得分"""
        return np.exp(-0.5 * ((x - mean) / std) ** 2)


class IBDAnalyzer:
    """
    方法3: IBD风格分析器
    
    基于Follow-Through Days和Distribution Days识别市场状态
    """
    
    def __init__(self, params: Dict = None):
        self.params = params or {
            'ftd_min_gain': 1.5,
            'ftd_day_range': [4, 7],
            'dd_threshold': -0.2,
            'dd_max_count': 5,
            'dd_window': 21
        }
    
    def analyze(self, df: pd.DataFrame) -> MethodResult:
        """分析市场状态"""
        df = self._calculate_indicators(df)
        
        # 识别FTD和DD
        ftd_count, last_ftd = self._count_ftd(df)
        dd_count = self._count_dd(df)
        
        # 确定IBD市场状态
        recent = df.tail(20)
        trend = recent['close'].pct_change(periods=20).iloc[-1] * 100 if len(recent) >= 20 else 0
        
        if dd_count >= self.params['dd_max_count']:
            ibd_status = 'market_in_correction'
        elif ftd_count > 0 and dd_count < 3:
            ibd_status = 'confirmed_uptrend'
        elif ftd_count > 0 and dd_count >= 3:
            ibd_status = 'uptrend_under_pressure'
        else:
            ibd_status = 'rally_attempt'
        
        # 映射到14状态
        if ibd_status == 'confirmed_uptrend':
            if trend > 10:
                state = MarketState.BULL_STRONG
            else:
                state = MarketState.BULL_NORMAL
            confidence = 80
        elif ibd_status == 'uptrend_under_pressure':
            state = MarketState.BULL_LATE
            confidence = 60
        elif ibd_status == 'market_in_correction':
            if trend < -10:
                state = MarketState.BEAR_STRONG
            else:
                state = MarketState.BEAR_NORMAL
            confidence = 75
        else:  # rally_attempt
            if trend > 0:
                state = MarketState.TURNING_UP
            else:
                state = MarketState.RANGE_MID
            confidence = 50
        
        return MethodResult(
            method_name='IBD',
            state=state,
            confidence=confidence,
            details={
                'ibd_status': ibd_status,
                'ftd_count': ftd_count,
                'dd_count': dd_count,
                'last_ftd_days': last_ftd,
                'trend_20d': trend
            }
        )
    
    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算指标"""
        df = df.copy()
        close = df['close']
        volume = df.get('volume', pd.Series([1]*len(df), index=df.index))
        
        df['change'] = close.pct_change() * 100
        df['vol_change'] = volume.pct_change()
        df['low_60d'] = close.rolling(60, min_periods=1).min()
        
        return df
    
    def _count_ftd(self, df: pd.DataFrame) -> Tuple[int, int]:
        """计算Follow-Through Days"""
        recent = df.tail(60)
        ftd_count = 0
        last_ftd = -1
        
        for i in range(10, len(recent)):
            # 检查是否从低点反弹
            window = recent.iloc[i-10:i]
            if len(window) < 10:
                continue
            
            low_idx = window['close'].idxmin()
            days_from_low = (recent.index[i] - low_idx).days
            
            if self.params['ftd_day_range'][0] <= days_from_low <= self.params['ftd_day_range'][1]:
                if recent.iloc[i]['change'] >= self.params['ftd_min_gain']:
                    if recent.iloc[i].get('volume', 0) > recent.iloc[i-1].get('volume', 0):
                        ftd_count += 1
                        last_ftd = len(recent) - i
        
        return ftd_count, last_ftd
    
    def _count_dd(self, df: pd.DataFrame) -> int:
        """计算Distribution Days"""
        recent = df.tail(self.params['dd_window'])
        dd_count = 0
        
        for i in range(1, len(recent)):
            if recent.iloc[i]['change'] < self.params['dd_threshold']:
                if recent.iloc[i].get('volume', 0) > recent.iloc[i-1].get('volume', 0):
                    dd_count += 1
        
        return dd_count


class MarketEnvIdentifier:
    """
    市场环境识别器
    
    整合三种方法，通过投票机制输出最终状态
    """
    
    def __init__(self, config_path: str = None):
        self.trend_analyzer = TrendAnalyzer()
        self.hmm_analyzer = HMMAnalyzer()
        self.ibd_analyzer = IBDAnalyzer()
        
        # 加载配置
        if config_path:
            self._load_config(config_path)
        
        # 状态到仓位建议的映射
        self.position_map = {
            MarketState.BULL_STRONG: (0.8, 1.0),
            MarketState.BULL_NORMAL: (0.6, 0.8),
            MarketState.BULL_LATE: (0.5, 0.7),
            MarketState.BULL_PULLBACK: (0.5, 0.7),
            MarketState.BEAR_STRONG: (0.0, 0.2),
            MarketState.BEAR_NORMAL: (0.1, 0.3),
            MarketState.BEAR_LATE: (0.2, 0.4),
            MarketState.BEAR_BOUNCE: (0.2, 0.4),
            MarketState.RANGE_HIGH: (0.4, 0.6),
            MarketState.RANGE_MID: (0.3, 0.5),
            MarketState.RANGE_LOW: (0.4, 0.6),
            MarketState.RANGE_WIDE: (0.3, 0.5),
            MarketState.TURNING_UP: (0.5, 0.7),
            MarketState.TURNING_DOWN: (0.2, 0.4),
            MarketState.UNKNOWN: (0.3, 0.5)
        }
        
        # 状态到风险等级
        self.risk_map = {
            'bull': 'low',
            'bear': 'high',
            'range': 'medium',
            'turning': 'medium',
            'unknown': 'medium'
        }
    
    def identify(self, df: pd.DataFrame) -> MarketEnvResult:
        """
        识别市场环境
        
        Args:
            df: OHLCV数据，需要至少250天历史数据
            
        Returns:
            MarketEnvResult: 识别结果
        """
        # 三种方法分别识别
        trend_result = self.trend_analyzer.analyze(df)
        hmm_result = self.hmm_analyzer.analyze(df)
        ibd_result = self.ibd_analyzer.analyze(df)
        
        # 投票机制
        votes = {
            trend_result.state.category: trend_result.confidence,
            hmm_result.state.category: hmm_result.confidence,
            ibd_result.state.category: ibd_result.confidence
        }
        
        # 计算类别得分
        category_scores = {}
        for result in [trend_result, hmm_result, ibd_result]:
            cat = result.state.category
            if cat not in category_scores:
                category_scores[cat] = 0
            category_scores[cat] += result.confidence
        
        # 选择得分最高的类别
        best_category = max(category_scores, key=category_scores.get)
        
        # 从该类别的结果中选择置信度最高的状态
        category_results = [r for r in [trend_result, hmm_result, ibd_result] 
                          if r.state.category == best_category]
        best_result = max(category_results, key=lambda x: x.confidence)
        final_state = best_result.state
        
        # 计算一致性
        categories = [r.state.category for r in [trend_result, hmm_result, ibd_result]]
        consensus = categories.count(best_category)
        
        # 计算最终置信度
        final_confidence = best_result.confidence * (0.6 + 0.2 * consensus)
        final_confidence = min(100, final_confidence)
        
        # 获取仓位建议和风险等级
        position_advice = self.position_map.get(final_state, (0.3, 0.5))
        risk_level = self.risk_map.get(final_state.category, 'medium')
        
        # 提取关键指标
        indicators = {}
        if trend_result.details:
            indicators.update(trend_result.details)
        
        return MarketEnvResult(
            state=final_state,
            category=final_state.category,
            confidence=final_confidence,
            trend_result=trend_result,
            hmm_result=hmm_result,
            ibd_result=ibd_result,
            consensus=consensus,
            indicators=indicators,
            position_advice=position_advice,
            risk_level=risk_level
        )
    
    def _load_config(self, config_path: str):
        """加载配置"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            if 'trend_analyzer' in config:
                self.trend_analyzer.thresholds = config['trend_analyzer']
            if 'ibd' in config:
                self.ibd_analyzer.params = config['ibd']
        except Exception as e:
            logger.warning(f"加载配置失败: {e}")


# 便捷函数
def identify_market_env(df: pd.DataFrame = None, 
                       benchmark: str = '000001.XSHG') -> MarketEnvResult:
    """
    识别当前市场环境
    
    Args:
        df: OHLCV数据，如果不提供则使用JQData获取
        benchmark: 指数代码（仅当df为None时使用）
        
    Returns:
        MarketEnvResult
    """
    identifier = MarketEnvIdentifier()
    
    if df is None:
        import jqdatasdk as jq
        df = jq.get_price(
            benchmark,
            count=300,
            frequency='daily',
            fields=['open', 'high', 'low', 'close', 'volume']
        )
    
    return identifier.identify(df)


def get_downstream_params(result: MarketEnvResult) -> Dict:
    """
    获取下游工作流程所需参数
    
    Args:
        result: 市场环境识别结果
        
    Returns:
        Dict: 下游参数
    """
    return {
        # 基本信息
        'market_state': result.state.name,
        'market_state_name': result.state.value,
        'category': result.category,
        'confidence': result.confidence,
        
        # 仓位控制
        'position_min': result.position_advice[0],
        'position_max': result.position_advice[1],
        'suggested_position': (result.position_advice[0] + result.position_advice[1]) / 2,
        
        # 风险控制
        'risk_level': result.risk_level,
        'stop_loss_pct': 0.05 if result.risk_level == 'high' else (0.08 if result.risk_level == 'medium' else 0.10),
        
        # 策略选择建议
        'strategy_type': _get_strategy_type(result),
        
        # 方法一致性
        'consensus': result.consensus,
        'high_confidence': result.confidence >= 70 and result.consensus >= 2,
        
        # 原始指标
        'indicators': result.indicators
    }


def _get_strategy_type(result: MarketEnvResult) -> str:
    """根据市场状态推荐策略类型"""
    state = result.state
    
    if state in [MarketState.BULL_STRONG, MarketState.BULL_NORMAL]:
        return 'trend_following'
    elif state in [MarketState.BEAR_STRONG, MarketState.BEAR_NORMAL]:
        return 'defensive'
    elif state in [MarketState.RANGE_MID, MarketState.RANGE_HIGH, MarketState.RANGE_LOW]:
        return 'mean_reversion'
    elif state in [MarketState.TURNING_UP]:
        return 'reversal_long'
    elif state in [MarketState.TURNING_DOWN]:
        return 'reversal_short'
    else:
        return 'balanced'

