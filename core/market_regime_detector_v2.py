"""
市场环境识别器 v2 - 16种细分状态版本
=====================================

支持:
- 上证指数 + 深证成指
- 16种市场状态细分 (基于MarketPhase)
- 短/中/长三周期分析
- 历史数据优化参数

市场状态体系:
- 牛市系列(5种): 牛市确认共振、牛市确认、牛市震荡、牛市短期调整、牛市中期调整
- 熊市系列(5种): 熊市确认共振、熊市确认、熊市反弹、熊市技术反弹、熊市筑底
- 震荡系列(6种): 突破在即、破位风险、复苏初期、见顶回落、窄幅震荡、宽幅震荡
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass, asdict, field
from datetime import datetime, date, timedelta
from pathlib import Path
import logging
import json

from core.market_state_definitions import (
    MarketPhase, MarketRegime, TrendDirection,
    PHASE_DESCRIPTIONS, REGIME_DESCRIPTIONS,
    determine_market_phase
)

logger = logging.getLogger(__name__)

CONFIG_DIR = Path("/home/taotao/dev/QuantTest/TRQuant/config")


@dataclass
class PeriodScores:
    """三周期得分"""
    short: float = 0.0    # 短期得分 (-100~100)
    medium: float = 0.0   # 中期得分 (-100~100)
    long: float = 0.0     # 长期得分 (-100~100)
    composite: float = 0.0  # 综合得分


@dataclass
class MarketIndicators:
    """市场指标"""
    # 价格动量
    momentum_5d: float = 0.0
    momentum_20d: float = 0.0
    momentum_60d: float = 0.0
    momentum_120d: float = 0.0
    
    # 均线位置
    price_vs_ma5: float = 0.0
    price_vs_ma20: float = 0.0
    price_vs_ma60: float = 0.0
    price_vs_ma120: float = 0.0
    price_vs_ma250: float = 0.0
    
    # 均线排列
    ma_alignment: str = "mixed"  # bullish/bearish/mixed
    
    # 技术指标
    rsi: float = 50.0
    macd_hist: float = 0.0
    
    # 波动率
    volatility: float = 0.0
    volatility_level: str = "medium"  # low/medium/high


@dataclass
class RegimeResultV2:
    """16状态识别结果"""
    # 细分状态
    phase: MarketPhase = MarketPhase.NARROW_RANGE
    phase_name: str = ""
    phase_category: str = ""  # bull/bear/volatile
    
    # 大类状态
    regime: MarketRegime = MarketRegime.VOLATILE
    regime_name: str = ""
    
    # 置信度
    confidence: float = 0.0
    is_reliable: bool = False  # 置信度>=70
    
    # 三周期得分
    scores: PeriodScores = field(default_factory=PeriodScores)
    
    # 仓位建议
    position_min: float = 0.3
    position_max: float = 0.5
    
    # 市场指标
    indicators: MarketIndicators = field(default_factory=MarketIndicators)
    
    # 元数据
    benchmark: str = ""
    benchmark_name: str = ""
    analysis_date: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'phase': self.phase.name,
            'phase_name': self.phase_name,
            'phase_category': self.phase_category,
            'regime': self.regime.name,
            'regime_name': self.regime_name,
            'confidence': round(self.confidence, 1),
            'is_reliable': self.is_reliable,
            'scores': asdict(self.scores),
            'position': {
                'min': round(self.position_min * 100),
                'max': round(self.position_max * 100),
                'recommended': round((self.position_min + self.position_max) / 2 * 100)
            },
            'indicators': asdict(self.indicators),
            'benchmark': self.benchmark,
            'benchmark_name': self.benchmark_name,
            'analysis_date': self.analysis_date
        }
    
    def summary(self) -> str:
        emoji = {"bull": "🐂", "bear": "🐻", "volatile": "〰️"}.get(self.phase_category, "❓")
        status = "✅" if self.is_reliable else "⚠️"
        return f"{emoji} {self.phase_name} ({self.confidence:.0f}%) {status}"


class MarketRegimeDetectorV2:
    """
    市场环境识别器 v2
    
    使用三周期分析判断16种市场状态
    """
    
    MARKET_NAMES = {
        '000001.XSHG': '上证指数',
        '399001.XSHE': '深证成指'
    }
    
    # 市场特定参数（根据历史数据优化）
    MARKET_PARAMS = {
        '000001.XSHG': {
            'vol_threshold_high': 25,  # 高波动阈值
            'vol_threshold_low': 15,   # 低波动阈值
            'momentum_sensitivity': 1.0
        },
        '399001.XSHE': {
            'vol_threshold_high': 30,
            'vol_threshold_low': 18,
            'momentum_sensitivity': 0.9  # 深证波动大，降低敏感度
        }
    }
    
    def __init__(self):
        self._jq = None
    
    def _ensure_jqdata(self):
        if self._jq is None:
            import jqdatasdk as jq
            config_file = CONFIG_DIR / "jqdata_config.json"
            with open(config_file) as f:
                cfg = json.load(f)
            jq.auth(cfg['username'], cfg['password'])
            self._jq = jq
    
    def analyze(self,
                df: Optional[pd.DataFrame] = None,
                benchmark: str = "000001.XSHG",
                lookback_days: int = 300) -> RegimeResultV2:
        """分析市场环境"""
        # 获取数据
        if df is None:
            self._ensure_jqdata()
            end = datetime.now()
            start = end - timedelta(days=lookback_days + 50)
            df = self._jq.get_price(
                benchmark,
                start_date=start.strftime('%Y-%m-%d'),
                end_date=end.strftime('%Y-%m-%d'),
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume']
            )
            if df is not None:
                df.index = pd.to_datetime(df.index)
        
        if df is None or len(df) < 120:
            return RegimeResultV2(benchmark=benchmark)
        
        # 计算指标
        indicators = self._calculate_indicators(df)
        
        # 计算三周期得分
        scores = self._calculate_period_scores(df, indicators, benchmark)
        
        # 判断市场阶段
        phase = determine_market_phase(scores.long, scores.medium, scores.short)
        
        # 获取阶段描述
        phase_desc = PHASE_DESCRIPTIONS.get(phase, {})
        phase_name = phase_desc.get('name', phase.value)
        phase_category = self._get_phase_category(phase)
        
        # 确定大类
        regime = self._phase_to_regime(phase, scores)
        regime_desc = REGIME_DESCRIPTIONS.get(regime, {})
        regime_name = regime_desc.get('name', regime.value)
        
        # 计算置信度
        confidence = self._calculate_confidence(scores, phase)
        
        # 仓位建议
        pos_range = phase_desc.get('position_range', (0.3, 0.5))
        
        return RegimeResultV2(
            phase=phase,
            phase_name=phase_name,
            phase_category=phase_category,
            regime=regime,
            regime_name=regime_name,
            confidence=confidence,
            is_reliable=confidence >= 70,
            scores=scores,
            position_min=pos_range[0],
            position_max=pos_range[1],
            indicators=indicators,
            benchmark=benchmark,
            benchmark_name=self.MARKET_NAMES.get(benchmark, benchmark),
            analysis_date=date.today().strftime("%Y-%m-%d")
        )
    
    def _calculate_indicators(self, df: pd.DataFrame) -> MarketIndicators:
        """计算市场指标"""
        close = df['close']
        
        # 移动平均
        ma5 = close.rolling(5).mean()
        ma10 = close.rolling(10).mean()
        ma20 = close.rolling(20).mean()
        ma60 = close.rolling(60).mean()
        ma120 = close.rolling(120).mean()
        ma250 = close.rolling(250).mean()
        
        current = close.iloc[-1]
        
        # 动量
        mom_5d = (current / close.iloc[-6] - 1) * 100 if len(close) > 5 else 0
        mom_20d = (current / close.iloc[-21] - 1) * 100 if len(close) > 20 else 0
        mom_60d = (current / close.iloc[-61] - 1) * 100 if len(close) > 60 else 0
        mom_120d = (current / close.iloc[-121] - 1) * 100 if len(close) > 120 else 0
        
        # 价格相对MA
        price_vs_ma5 = (current / ma5.iloc[-1] - 1) * 100 if not pd.isna(ma5.iloc[-1]) else 0
        price_vs_ma20 = (current / ma20.iloc[-1] - 1) * 100 if not pd.isna(ma20.iloc[-1]) else 0
        price_vs_ma60 = (current / ma60.iloc[-1] - 1) * 100 if not pd.isna(ma60.iloc[-1]) else 0
        price_vs_ma120 = (current / ma120.iloc[-1] - 1) * 100 if not pd.isna(ma120.iloc[-1]) else 0
        price_vs_ma250 = (current / ma250.iloc[-1] - 1) * 100 if not pd.isna(ma250.iloc[-1]) else 0
        
        # 均线排列
        if ma5.iloc[-1] > ma10.iloc[-1] > ma20.iloc[-1] > ma60.iloc[-1]:
            ma_alignment = "bullish"
        elif ma5.iloc[-1] < ma10.iloc[-1] < ma20.iloc[-1] < ma60.iloc[-1]:
            ma_alignment = "bearish"
        else:
            ma_alignment = "mixed"
        
        # RSI
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi = (100 - (100 / (1 + gain / loss))).iloc[-1]
        
        # MACD
        exp12 = close.ewm(span=12).mean()
        exp26 = close.ewm(span=26).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9).mean()
        macd_hist = (macd.iloc[-1] - signal.iloc[-1]) * 100 / current  # 归一化
        
        # 波动率
        returns = close.pct_change()
        volatility = returns.rolling(20).std().iloc[-1] * np.sqrt(252) * 100
        
        if volatility < 15:
            vol_level = "low"
        elif volatility < 25:
            vol_level = "medium"
        else:
            vol_level = "high"
        
        return MarketIndicators(
            momentum_5d=mom_5d,
            momentum_20d=mom_20d,
            momentum_60d=mom_60d,
            momentum_120d=mom_120d,
            price_vs_ma5=price_vs_ma5,
            price_vs_ma20=price_vs_ma20,
            price_vs_ma60=price_vs_ma60,
            price_vs_ma120=price_vs_ma120,
            price_vs_ma250=price_vs_ma250 if not pd.isna(price_vs_ma250) else 0,
            ma_alignment=ma_alignment,
            rsi=rsi if not pd.isna(rsi) else 50,
            macd_hist=macd_hist if not pd.isna(macd_hist) else 0,
            volatility=volatility if not pd.isna(volatility) else 0,
            volatility_level=vol_level
        )
    
    def _calculate_period_scores(self, df: pd.DataFrame, 
                                 ind: MarketIndicators, 
                                 benchmark: str) -> PeriodScores:
        """计算三周期得分"""
        params = self.MARKET_PARAMS.get(benchmark, self.MARKET_PARAMS['000001.XSHG'])
        sens = params['momentum_sensitivity']
        
        # 短期得分 (5-20日)
        short_score = 0.0
        short_score += np.clip(ind.momentum_5d * 5 * sens, -30, 30)
        short_score += np.clip(ind.price_vs_ma5 * 3, -20, 20)
        short_score += np.clip(ind.price_vs_ma20 * 2, -15, 15)
        short_score += np.clip((ind.rsi - 50) * 0.5, -15, 15)
        short_score += np.clip(ind.macd_hist * 10, -20, 20)
        
        # 中期得分 (20-60日)
        medium_score = 0.0
        medium_score += np.clip(ind.momentum_20d * 3 * sens, -30, 30)
        medium_score += np.clip(ind.momentum_60d * 2 * sens, -25, 25)
        medium_score += np.clip(ind.price_vs_ma60 * 2, -25, 25)
        medium_score += 20 if ind.ma_alignment == "bullish" else (-20 if ind.ma_alignment == "bearish" else 0)
        
        # 长期得分 (60-250日)
        long_score = 0.0
        long_score += np.clip(ind.momentum_60d * 2 * sens, -25, 25)
        long_score += np.clip(ind.momentum_120d * 1.5 * sens, -25, 25)
        long_score += np.clip(ind.price_vs_ma120 * 2, -25, 25)
        long_score += np.clip(ind.price_vs_ma250 * 1.5, -25, 25)
        
        # 综合得分 (加权)
        composite = short_score * 0.2 + medium_score * 0.3 + long_score * 0.5
        
        return PeriodScores(
            short=round(short_score, 1),
            medium=round(medium_score, 1),
            long=round(long_score, 1),
            composite=round(composite, 1)
        )
    
    def _get_phase_category(self, phase: MarketPhase) -> str:
        """获取阶段类别"""
        if 'BULL' in phase.name:
            return 'bull'
        elif 'BEAR' in phase.name:
            return 'bear'
        else:
            return 'volatile'
    
    def _phase_to_regime(self, phase: MarketPhase, scores: PeriodScores) -> MarketRegime:
        """从阶段转换为大类"""
        category = self._get_phase_category(phase)
        
        if category == 'bull':
            return MarketRegime.BULL
        elif category == 'bear':
            return MarketRegime.BEAR
        else:
            # 震荡细分
            if phase in [MarketPhase.RECOVERY_EARLY, MarketPhase.BREAKTHROUGH]:
                return MarketRegime.RECOVERY
            elif phase in [MarketPhase.TOP_FALL, MarketPhase.BREAK_RISK]:
                return MarketRegime.DISTRIBUTION
            else:
                return MarketRegime.VOLATILE
    
    def _calculate_confidence(self, scores: PeriodScores, phase: MarketPhase) -> float:
        """计算置信度"""
        category = self._get_phase_category(phase)
        
        # 基础置信度
        if category == 'bull':
            # 牛市：三周期越一致越高
            base = 50
            if scores.long > 30:
                base += 15
            if scores.medium > 20:
                base += 15
            if scores.short > 10:
                base += 10
            if scores.long > 30 and scores.medium > 20 and scores.short > 10:
                base += 10  # 共振加分
        elif category == 'bear':
            base = 50
            if scores.long < -30:
                base += 15
            if scores.medium < -20:
                base += 15
            if scores.short < -10:
                base += 10
            if scores.long < -30 and scores.medium < -20 and scores.short < -10:
                base += 10
        else:
            # 震荡：波动越小越高
            base = 60
            if abs(scores.long) < 30 and abs(scores.medium) < 20:
                base += 10
            if abs(scores.composite) < 20:
                base += 10
        
        return min(base, 100)
    
    def analyze_both(self) -> Dict[str, RegimeResultV2]:
        """同时分析上证和深证"""
        results = {}
        for benchmark in ['000001.XSHG', '399001.XSHE']:
            results[benchmark] = self.analyze(benchmark=benchmark)
        return results
    
    def get_combined_view(self) -> Dict:
        """获取综合视图"""
        results = self.analyze_both()
        
        sh = results['000001.XSHG']
        sz = results['399001.XSHE']
        
        # 判断共识
        consensus = sh.phase_category == sz.phase_category
        
        # 综合状态
        if consensus:
            combined_phase = sh.phase_name
            combined_category = sh.phase_category
            combined_confidence = (sh.confidence + sz.confidence) / 2
        else:
            # 不一致时取保守判断
            if sh.is_reliable and not sz.is_reliable:
                combined_phase = sh.phase_name
                combined_category = sh.phase_category
                combined_confidence = sh.confidence * 0.8
            elif sz.is_reliable and not sh.is_reliable:
                combined_phase = sz.phase_name
                combined_category = sz.phase_category
                combined_confidence = sz.confidence * 0.8
            else:
                combined_phase = "震荡分歧"
                combined_category = "volatile"
                combined_confidence = 50
        
        return {
            'combined': {
                'phase': combined_phase,
                'category': combined_category,
                'confidence': round(combined_confidence, 1),
                'is_reliable': combined_confidence >= 70,
                'consensus': consensus,
                'position': round((sh.position_min + sh.position_max + sz.position_min + sz.position_max) / 4 * 100)
            },
            'shanghai': sh.to_dict(),
            'shenzhen': sz.to_dict(),
            'analysis_date': date.today().strftime("%Y-%m-%d")
        }


def quick_market_check_v2(benchmark: str = "000001.XSHG") -> Dict:
    """快速检查（单指数）"""
    detector = MarketRegimeDetectorV2()
    result = detector.analyze(benchmark=benchmark)
    return result.to_dict()


def get_market_environment_v2() -> Dict:
    """获取完整市场环境（双指数+综合）"""
    detector = MarketRegimeDetectorV2()
    return detector.get_combined_view()


if __name__ == "__main__":
    print("=" * 70)
    print("🎯 市场环境识别器 v2 测试")
    print("=" * 70)
    
    env = get_market_environment_v2()
    
    print(f"\n📊 综合判断:")
    print(f"  状态: {env['combined']['phase']} ({env['combined']['category']})")
    print(f"  置信度: {env['combined']['confidence']:.0f}%")
    print(f"  可靠性: {'✅可靠' if env['combined']['is_reliable'] else '⚠️观望'}")
    print(f"  两市共识: {'✅一致' if env['combined']['consensus'] else '❌分歧'}")
    print(f"  建议仓位: {env['combined']['position']}%")
    
    print(f"\n📈 上证指数:")
    sh = env['shanghai']
    print(f"  状态: {sh['phase_name']} ({sh['phase_category']})")
    print(f"  三周期: 短{sh['scores']['short']:.0f} 中{sh['scores']['medium']:.0f} 长{sh['scores']['long']:.0f}")
    
    print(f"\n📈 深证成指:")
    sz = env['shenzhen']
    print(f"  状态: {sz['phase_name']} ({sz['phase_category']})")
    print(f"  三周期: 短{sz['scores']['short']:.0f} 中{sz['scores']['medium']:.0f} 长{sz['scores']['long']:.0f}")

