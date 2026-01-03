"""
市场环境识别器
==============

专注于准确识别市场环境，输出标准化参数供下游策略使用

输出:
- 市场状态 (bull/bear/sideways/transition_up/transition_down)
- 置信度
- 市场特征向量
- 风险评估
- 建议参数（仅供参考）
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, date
import logging
import json

logger = logging.getLogger(__name__)


class MarketRegime(Enum):
    """市场状态"""
    BULL = "bull"              # 牛市
    BEAR = "bear"              # 熊市
    SIDEWAYS = "sideways"      # 震荡
    TRANSITION_UP = "transition_up"      # 底部反转
    TRANSITION_DOWN = "transition_down"  # 顶部反转
    UNKNOWN = "unknown"
    
    @property
    def chinese(self) -> str:
        return {
            'bull': '牛市', 'bear': '熊市', 'sideways': '震荡',
            'transition_up': '底部反转', 'transition_down': '顶部反转',
            'unknown': '未知'
        }[self.value]


class VolatilityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class MarketFeatures:
    """市场特征向量"""
    trend_strength: float = 0.0      # 趋势强度 -100~+100
    volatility: float = 0.0          # 波动率 (年化%)
    volatility_level: str = "medium" # low/medium/high
    momentum_5d: float = 0.0         # 5日动量
    momentum_20d: float = 0.0        # 20日动量
    momentum_60d: float = 0.0        # 60日动量
    price_vs_ma20: float = 0.0       # 价格相对MA20 (%)
    price_vs_ma60: float = 0.0       # 价格相对MA60 (%)
    price_vs_ma250: float = 0.0      # 价格相对年线 (%)
    ma_alignment: str = "mixed"      # 均线排列 (bullish/bearish/mixed)
    rsi: float = 50.0                # RSI
    macd_signal: str = "neutral"     # MACD信号 (bullish/bearish/neutral)
    volume_ratio: float = 1.0        # 成交量比率
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class RiskAssessment:
    """风险评估"""
    drawdown_risk: str = "medium"    # 回撤风险 low/medium/high
    reversal_probability: float = 0.0 # 反转概率 0-100%
    max_drawdown_20d: float = 0.0    # 20日最大回撤
    current_drawdown: float = 0.0    # 当前回撤
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SuggestedParams:
    """建议参数（仅供参考，非强制）"""
    position_ratio: float = 50.0     # 建议仓位 0-100%
    stop_loss: float = 5.0           # 建议止损 %
    take_profit: float = 10.0        # 建议止盈 %
    holding_period: str = "medium"   # 建议持仓周期 short/medium/long
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MarketEnvironment:
    """市场环境识别结果"""
    # 核心结果
    regime: MarketRegime = MarketRegime.UNKNOWN
    confidence: float = 0.0          # 0-100%
    
    # 详细特征
    features: MarketFeatures = field(default_factory=MarketFeatures)
    risk: RiskAssessment = field(default_factory=RiskAssessment)
    suggested: SuggestedParams = field(default_factory=SuggestedParams)
    
    # 多模型投票
    model_votes: Dict[str, str] = field(default_factory=dict)
    
    # 元数据
    analysis_date: str = ""
    benchmark: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'regime': self.regime.value,
            'regime_cn': self.regime.chinese,
            'confidence': self.confidence,
            'features': self.features.to_dict(),
            'risk': self.risk.to_dict(),
            'suggested': self.suggested.to_dict(),
            'model_votes': self.model_votes,
            'analysis_date': self.analysis_date,
            'benchmark': self.benchmark
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class MarketEnvironmentAnalyzer:
    """
    市场环境分析器
    
    集成多种分析方法，输出统一的市场环境判断
    """
    
    def __init__(self, use_hmm: bool = True, use_technical: bool = True):
        self.use_hmm = use_hmm
        self.use_technical = use_technical
        self._hmm = None
        self._jq = None
        
    def _ensure_jqdata(self):
        if self._jq is None:
            import jqdatasdk as jq
            with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
                cfg = json.load(f)
            jq.auth(cfg['username'], cfg['password'])
            self._jq = jq
    
    def _load_hmm(self):
        if self._hmm is None and self.use_hmm:
            try:
                from core.hmm_fixed import FixedHMM
                self._hmm = FixedHMM(use_gpu=False)
            except Exception as e:
                logger.warning(f"HMM加载失败: {e}")
                self._hmm = None
    
    def analyze(self, 
                df: Optional[pd.DataFrame] = None,
                benchmark: str = "000001.XSHG",
                lookback_days: int = 250) -> MarketEnvironment:
        """
        分析市场环境
        
        Args:
            df: 价格数据，如果为None则自动获取
            benchmark: 基准指数
            lookback_days: 回看天数
            
        Returns:
            MarketEnvironment: 市场环境识别结果
        """
        # 获取数据
        if df is None:
            self._ensure_jqdata()
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=lookback_days + 100)
            
            df = self._jq.get_price(
                benchmark,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume']
            )
            df.index = pd.to_datetime(df.index)
        
        if df is None or len(df) < 60:
            return MarketEnvironment()
        
        # 计算技术指标
        features = self._calculate_features(df)
        
        # 多模型投票
        model_votes = {}
        
        # 1. 技术分析判断
        if self.use_technical:
            tech_regime = self._technical_regime(features)
            model_votes['technical'] = tech_regime.value
        
        # 2. HMM判断
        if self.use_hmm:
            self._load_hmm()
            if self._hmm:
                hmm_result = self._hmm.analyze(df)
                if hmm_result:
                    hmm_regime = self._map_hmm_to_regime(hmm_result.current_state.to_english())
                    model_votes['hmm'] = hmm_regime.value
        
        # 3. 动量判断
        mom_regime = self._momentum_regime(features)
        model_votes['momentum'] = mom_regime.value
        
        # 4. 均线判断
        ma_regime = self._ma_regime(features)
        model_votes['ma'] = ma_regime.value
        
        # 综合投票
        final_regime, confidence = self._vote_regime(model_votes)
        
        # 风险评估
        risk = self._assess_risk(df, features)
        
        # 建议参数
        suggested = self._suggest_params(final_regime, features, risk)
        
        return MarketEnvironment(
            regime=final_regime,
            confidence=confidence,
            features=features,
            risk=risk,
            suggested=suggested,
            model_votes=model_votes,
            analysis_date=date.today().strftime("%Y-%m-%d"),
            benchmark=benchmark
        )
    
    def _calculate_features(self, df: pd.DataFrame) -> MarketFeatures:
        """计算市场特征"""
        close = df['close']
        volume = df['volume']
        
        # 移动平均
        ma5 = close.rolling(5).mean()
        ma10 = close.rolling(10).mean()
        ma20 = close.rolling(20).mean()
        ma60 = close.rolling(60).mean()
        ma120 = close.rolling(120).mean()
        ma250 = close.rolling(250).mean()
        
        # 当前值
        current = close.iloc[-1]
        
        # 动量
        momentum_5d = (current / close.iloc[-6] - 1) * 100 if len(close) > 5 else 0
        momentum_20d = (current / close.iloc[-21] - 1) * 100 if len(close) > 20 else 0
        momentum_60d = (current / close.iloc[-61] - 1) * 100 if len(close) > 60 else 0
        
        # 波动率
        returns = close.pct_change()
        volatility = returns.rolling(20).std().iloc[-1] * np.sqrt(252) * 100
        
        if volatility < 15:
            vol_level = "low"
        elif volatility < 25:
            vol_level = "medium"
        else:
            vol_level = "high"
        
        # 价格相对MA
        price_vs_ma20 = (current / ma20.iloc[-1] - 1) * 100 if not pd.isna(ma20.iloc[-1]) else 0
        price_vs_ma60 = (current / ma60.iloc[-1] - 1) * 100 if not pd.isna(ma60.iloc[-1]) else 0
        price_vs_ma250 = (current / ma250.iloc[-1] - 1) * 100 if not pd.isna(ma250.iloc[-1]) else 0
        
        # 均线排列
        if ma5.iloc[-1] > ma10.iloc[-1] > ma20.iloc[-1] > ma60.iloc[-1]:
            ma_alignment = "bullish"
        elif ma5.iloc[-1] < ma10.iloc[-1] < ma20.iloc[-1] < ma60.iloc[-1]:
            ma_alignment = "bearish"
        else:
            ma_alignment = "mixed"
        
        # 趋势强度 (-100 ~ +100)
        trend_strength = (
            (30 if ma5.iloc[-1] > ma10.iloc[-1] else -30) +
            (25 if ma20.iloc[-1] > ma60.iloc[-1] else -25) +
            (20 if ma60.iloc[-1] > ma120.iloc[-1] else -20) +
            (15 if current > ma60.iloc[-1] else -15) +
            (10 if momentum_20d > 0 else -10)
        )
        
        # RSI
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = (100 - (100 / (1 + rs))).iloc[-1]
        
        # MACD
        exp12 = close.ewm(span=12).mean()
        exp26 = close.ewm(span=26).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9).mean()
        macd_hist = macd.iloc[-1] - signal.iloc[-1]
        
        if macd_hist > 0 and macd.iloc[-1] > macd.iloc[-2]:
            macd_signal = "bullish"
        elif macd_hist < 0 and macd.iloc[-1] < macd.iloc[-2]:
            macd_signal = "bearish"
        else:
            macd_signal = "neutral"
        
        # 成交量比率
        vol_ma20 = volume.rolling(20).mean().iloc[-1]
        volume_ratio = volume.iloc[-1] / vol_ma20 if vol_ma20 > 0 else 1.0
        
        return MarketFeatures(
            trend_strength=trend_strength,
            volatility=volatility,
            volatility_level=vol_level,
            momentum_5d=momentum_5d,
            momentum_20d=momentum_20d,
            momentum_60d=momentum_60d,
            price_vs_ma20=price_vs_ma20,
            price_vs_ma60=price_vs_ma60,
            price_vs_ma250=price_vs_ma250,
            ma_alignment=ma_alignment,
            rsi=rsi if not pd.isna(rsi) else 50,
            macd_signal=macd_signal,
            volume_ratio=volume_ratio
        )
    
    def _technical_regime(self, features: MarketFeatures) -> MarketRegime:
        """基于技术指标判断市场状态"""
        score = features.trend_strength
        
        # 考虑转换信号
        if score > 30 and features.momentum_20d > 5:
            return MarketRegime.BULL
        elif score < -30 and features.momentum_20d < -5:
            return MarketRegime.BEAR
        elif score < -20 and features.momentum_5d > 2 and features.rsi < 40:
            return MarketRegime.TRANSITION_UP  # 可能底部反转
        elif score > 20 and features.momentum_5d < -2 and features.rsi > 60:
            return MarketRegime.TRANSITION_DOWN  # 可能顶部反转
        else:
            return MarketRegime.SIDEWAYS
    
    def _momentum_regime(self, features: MarketFeatures) -> MarketRegime:
        """基于动量判断"""
        if features.momentum_20d > 8 and features.momentum_60d > 10:
            return MarketRegime.BULL
        elif features.momentum_20d < -8 and features.momentum_60d < -10:
            return MarketRegime.BEAR
        elif features.momentum_20d > 3 and features.momentum_60d < -5:
            return MarketRegime.TRANSITION_UP
        elif features.momentum_20d < -3 and features.momentum_60d > 5:
            return MarketRegime.TRANSITION_DOWN
        else:
            return MarketRegime.SIDEWAYS
    
    def _ma_regime(self, features: MarketFeatures) -> MarketRegime:
        """基于均线判断"""
        if features.ma_alignment == "bullish" and features.price_vs_ma60 > 5:
            return MarketRegime.BULL
        elif features.ma_alignment == "bearish" and features.price_vs_ma60 < -5:
            return MarketRegime.BEAR
        else:
            return MarketRegime.SIDEWAYS
    
    def _map_hmm_to_regime(self, hmm_state: str) -> MarketRegime:
        """映射HMM状态到市场状态"""
        mapping = {
            'bull': MarketRegime.BULL,
            'bear': MarketRegime.BEAR,
            'sideways': MarketRegime.SIDEWAYS
        }
        return mapping.get(hmm_state, MarketRegime.UNKNOWN)
    
    def _vote_regime(self, votes: Dict[str, str]) -> tuple:
        """多模型投票"""
        if not votes:
            return MarketRegime.UNKNOWN, 0.0
        
        # 统计投票
        vote_counts = {}
        for model, regime in votes.items():
            if regime not in vote_counts:
                vote_counts[regime] = 0
            # HMM权重更高
            weight = 1.5 if model == 'hmm' else 1.0
            vote_counts[regime] += weight
        
        # 找到最多票的状态
        max_regime = max(vote_counts, key=vote_counts.get)
        max_votes = vote_counts[max_regime]
        total_votes = sum(vote_counts.values())
        
        confidence = (max_votes / total_votes * 100) if total_votes > 0 else 0
        
        return MarketRegime(max_regime), confidence
    
    def _assess_risk(self, df: pd.DataFrame, features: MarketFeatures) -> RiskAssessment:
        """评估风险"""
        close = df['close']
        
        # 20日最大回撤
        rolling_max = close.rolling(20).max()
        drawdowns = (close - rolling_max) / rolling_max * 100
        max_dd_20d = drawdowns.iloc[-20:].min()
        
        # 当前回撤
        peak = close.max()
        current_dd = (close.iloc[-1] - peak) / peak * 100
        
        # 回撤风险
        if abs(current_dd) < 5:
            dd_risk = "low"
        elif abs(current_dd) < 15:
            dd_risk = "medium"
        else:
            dd_risk = "high"
        
        # 反转概率（基于RSI和技术超买超卖）
        reversal_prob = 0
        if features.rsi < 30:
            reversal_prob = 60 + (30 - features.rsi)  # 超卖，可能反弹
        elif features.rsi > 70:
            reversal_prob = 60 + (features.rsi - 70)  # 超买，可能回调
        else:
            reversal_prob = 20
        
        reversal_prob = min(reversal_prob, 90)
        
        return RiskAssessment(
            drawdown_risk=dd_risk,
            reversal_probability=reversal_prob,
            max_drawdown_20d=max_dd_20d,
            current_drawdown=current_dd
        )
    
    def _suggest_params(self, regime: MarketRegime, 
                        features: MarketFeatures,
                        risk: RiskAssessment) -> SuggestedParams:
        """建议参数（仅供参考）"""
        # 基础仓位
        base_position = {
            MarketRegime.BULL: 80,
            MarketRegime.BEAR: 20,
            MarketRegime.SIDEWAYS: 50,
            MarketRegime.TRANSITION_UP: 60,
            MarketRegime.TRANSITION_DOWN: 30,
            MarketRegime.UNKNOWN: 30
        }
        
        position = base_position.get(regime, 50)
        
        # 根据风险调整
        if risk.drawdown_risk == "high":
            position *= 0.7
        
        # 止损
        if features.volatility_level == "high":
            stop_loss = 8.0
        elif features.volatility_level == "low":
            stop_loss = 4.0
        else:
            stop_loss = 5.0
        
        # 止盈
        if regime == MarketRegime.BULL:
            take_profit = 15.0
        elif regime == MarketRegime.BEAR:
            take_profit = 5.0
        else:
            take_profit = 8.0
        
        # 持仓周期
        if regime in [MarketRegime.BULL, MarketRegime.BEAR]:
            holding = "long"
        elif regime in [MarketRegime.TRANSITION_UP, MarketRegime.TRANSITION_DOWN]:
            holding = "short"
        else:
            holding = "medium"
        
        return SuggestedParams(
            position_ratio=position,
            stop_loss=stop_loss,
            take_profit=take_profit,
            holding_period=holding
        )


def validate_accuracy(analyzer: MarketEnvironmentAnalyzer,
                      benchmark: str = "000001.XSHG",
                      start_date: str = "2021-01-01",
                      end_date: str = "2024-08-16") -> Dict:
    """
    验证市场环境识别准确性
    
    准确性定义：
    - bull: 未来20日涨幅 > 3%
    - bear: 未来20日跌幅 > 3%
    - sideways: 未来20日波动在 ±5% 内
    - transition_up: 未来10日涨幅 > 2%
    - transition_down: 未来10日跌幅 > 2%
    """
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        cfg = json.load(f)
    jq.auth(cfg['username'], cfg['password'])
    
    # 获取完整数据
    df_full = jq.get_price(
        benchmark,
        start_date=start_date,
        end_date=end_date,
        frequency='daily',
        fields=['open', 'high', 'low', 'close', 'volume']
    )
    df_full.index = pd.to_datetime(df_full.index)
    
    # 计算未来收益
    df_full['future_10d'] = df_full['close'].pct_change(10).shift(-10) * 100
    df_full['future_20d'] = df_full['close'].pct_change(20).shift(-20) * 100
    
    results = []
    sample_dates = df_full.index[250:-25:10]  # 每10天采样
    
    for dt in sample_dates:
        # 用历史数据分析
        hist_df = df_full.loc[:dt].tail(300)
        if len(hist_df) < 100:
            continue
        
        env = analyzer.analyze(df=hist_df, benchmark=benchmark)
        
        # 获取未来收益
        if dt in df_full.index:
            future_10d = df_full.loc[dt, 'future_10d']
            future_20d = df_full.loc[dt, 'future_20d']
        else:
            continue
        
        if pd.isna(future_20d):
            continue
        
        # 判断准确性
        regime = env.regime.value
        if regime == 'bull':
            correct = future_20d > 3
        elif regime == 'bear':
            correct = future_20d < -3
        elif regime == 'sideways':
            correct = abs(future_20d) < 5
        elif regime == 'transition_up':
            correct = future_10d > 2
        elif regime == 'transition_down':
            correct = future_10d < -2
        else:
            correct = False
        
        results.append({
            'date': dt.strftime('%Y-%m-%d'),
            'regime': regime,
            'confidence': env.confidence,
            'future_10d': future_10d,
            'future_20d': future_20d,
            'correct': correct
        })
    
    # 统计
    df_results = pd.DataFrame(results)
    
    stats = {
        'total': len(df_results),
        'overall_accuracy': df_results['correct'].mean() * 100,
        'by_regime': {}
    }
    
    for regime in df_results['regime'].unique():
        regime_df = df_results[df_results['regime'] == regime]
        stats['by_regime'][regime] = {
            'count': len(regime_df),
            'accuracy': regime_df['correct'].mean() * 100 if len(regime_df) > 0 else 0
        }
    
    return stats


if __name__ == "__main__":
    # 测试
    analyzer = MarketEnvironmentAnalyzer(use_hmm=True, use_technical=True)
    env = analyzer.analyze()
    print(env.to_json())

