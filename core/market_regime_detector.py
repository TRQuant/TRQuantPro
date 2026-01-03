"""
市场环境识别器 - 多指数版
===========================

支持上证指数和深证成指，使用针对各市场优化的参数

验证结果 (外样本 2023.07-2024.08):
- 上证: 置信度>=70准确率90.5%
- 深证: 置信度>=70准确率78.7%

使用方法:
    from core.market_regime_detector import MarketRegimeDetector, quick_regime_check
    
    # 方法1: 快速检查
    result = quick_regime_check()  # 默认上证
    result = quick_regime_check(benchmark='399001.XSHE')  # 深证
    
    # 方法2: 详细分析
    detector = MarketRegimeDetector()
    result = detector.analyze(benchmark='000001.XSHG')
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, date, timedelta
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# 配置路径
CONFIG_DIR = Path("/home/taotao/dev/QuantTest/TRQuant/config")


class MarketRegime(Enum):
    """市场状态"""
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    UNKNOWN = "unknown"
    
    @property
    def chinese(self) -> str:
        return {'bull': '牛市', 'bear': '熊市', 'sideways': '震荡', 'unknown': '未知'}[self.value]


@dataclass
class MarketIndicators:
    """市场指标"""
    trend_strength: float = 0.0      # 趋势强度 -100~+100
    momentum_60d: float = 0.0        # 60日动量 (%)
    momentum_20d: float = 0.0        # 20日动量 (%)
    momentum_5d: float = 0.0         # 5日动量 (%)
    price_vs_ma60: float = 0.0       # 价格相对MA60 (%)
    price_vs_ma250: float = 0.0      # 价格相对年线 (%)
    volatility: float = 0.0          # 年化波动率 (%)
    rsi: float = 50.0                # RSI
    ma_alignment: str = "mixed"      # 均线排列 (bullish/bearish/mixed)


@dataclass
class RegimeResult:
    """识别结果"""
    regime: MarketRegime
    confidence: float              # 0-100
    bull_score: float = 0.0
    bear_score: float = 0.0
    indicators: MarketIndicators = None
    benchmark: str = ""
    benchmark_name: str = ""
    analysis_date: str = ""
    is_reliable: bool = False      # 置信度>=70为可靠
    
    def to_dict(self) -> Dict:
        return {
            'regime': self.regime.value,
            'regime_cn': self.regime.chinese,
            'confidence': round(self.confidence, 1),
            'is_reliable': self.is_reliable,
            'bull_score': round(self.bull_score, 1),
            'bear_score': round(self.bear_score, 1),
            'indicators': asdict(self.indicators) if self.indicators else {},
            'benchmark': self.benchmark,
            'benchmark_name': self.benchmark_name,
            'analysis_date': self.analysis_date
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def summary(self) -> str:
        """简要摘要"""
        status = "✅可靠" if self.is_reliable else "⚠️观望"
        return f"{self.benchmark_name}: {self.regime.chinese} ({self.confidence:.0f}%) {status}"


class MarketRegimeDetector:
    """
    市场环境识别器
    
    特点:
    1. 支持上证/深证双指数
    2. 使用各市场优化参数
    3. 分层识别+置信度筛选
    """
    
    # 市场名称映射
    MARKET_NAMES = {
        '000001.XSHG': '上证指数',
        '399001.XSHE': '深证成指'
    }
    
    # 默认参数(如果配置文件不存在)
    DEFAULT_PARAMS = {
        '000001.XSHG': {
            'ts_bull': 30, 'ts_bear': -30,
            'm60_bull': 10, 'm60_bear': -10,
            'm20_bull': 5, 'm20_bear': -5
        },
        '399001.XSHE': {
            'ts_bull': 60, 'ts_bear': -60,
            'm60_bull': 10, 'm60_bear': -10,
            'm20_bull': 5, 'm20_bear': -5
        }
    }
    
    def __init__(self):
        self._jq = None
        self._params = self._load_params()
    
    def _load_params(self) -> Dict:
        """加载优化参数"""
        params_file = CONFIG_DIR / "market_env_params.json"
        if params_file.exists():
            try:
                with open(params_file) as f:
                    return json.load(f)
            except:
                pass
        return self.DEFAULT_PARAMS
    
    def _ensure_jqdata(self):
        """确保JQData连接"""
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
                lookback_days: int = 300) -> RegimeResult:
        """
        分析市场环境
        
        Args:
            df: 价格数据，如果为None则自动获取
            benchmark: 指数代码
            lookback_days: 回看天数
            
        Returns:
            RegimeResult: 识别结果
        """
        # 获取数据
        if df is None:
            self._ensure_jqdata()
            end = datetime.now()
            start = end - timedelta(days=lookback_days + 100)
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
            return RegimeResult(
                regime=MarketRegime.UNKNOWN,
                confidence=0,
                benchmark=benchmark,
                benchmark_name=self.MARKET_NAMES.get(benchmark, benchmark)
            )
        
        # 计算指标
        indicators = self._calculate_indicators(df)
        
        # 获取市场参数
        params = self._params.get(benchmark, self.DEFAULT_PARAMS.get(benchmark, self.DEFAULT_PARAMS['000001.XSHG']))
        
        # 分层识别
        regime, confidence, bull_score, bear_score = self._identify_regime(indicators, params)
        
        return RegimeResult(
            regime=regime,
            confidence=confidence,
            bull_score=bull_score,
            bear_score=bear_score,
            indicators=indicators,
            benchmark=benchmark,
            benchmark_name=self.MARKET_NAMES.get(benchmark, benchmark),
            analysis_date=date.today().strftime("%Y-%m-%d"),
            is_reliable=confidence >= 70
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
        
        # 动量
        mom_60d = (close.iloc[-1] / close.iloc[-61] - 1) * 100 if len(close) > 60 else 0
        mom_20d = (close.iloc[-1] / close.iloc[-21] - 1) * 100 if len(close) > 20 else 0
        mom_5d = (close.iloc[-1] / close.iloc[-6] - 1) * 100 if len(close) > 5 else 0
        
        # 价格位置
        price_vs_ma60 = (close.iloc[-1] / ma60.iloc[-1] - 1) * 100 if not pd.isna(ma60.iloc[-1]) else 0
        price_vs_ma250 = (close.iloc[-1] / ma250.iloc[-1] - 1) * 100 if not pd.isna(ma250.iloc[-1]) else 0
        
        # 趋势强度
        ts = (
            (30 if ma5.iloc[-1] > ma10.iloc[-1] else -30) +
            (25 if ma20.iloc[-1] > ma60.iloc[-1] else -25) +
            (20 if ma60.iloc[-1] > ma120.iloc[-1] else -20) +
            (15 if close.iloc[-1] > ma60.iloc[-1] else -15) +
            (10 if mom_20d > 0 else -10)
        )
        
        # 均线排列
        if ma5.iloc[-1] > ma10.iloc[-1] > ma20.iloc[-1] > ma60.iloc[-1]:
            ma_alignment = "bullish"
        elif ma5.iloc[-1] < ma10.iloc[-1] < ma20.iloc[-1] < ma60.iloc[-1]:
            ma_alignment = "bearish"
        else:
            ma_alignment = "mixed"
        
        # 波动率
        returns = close.pct_change()
        volatility = returns.rolling(20).std().iloc[-1] * np.sqrt(252) * 100
        
        # RSI
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi = (100 - (100 / (1 + gain / loss))).iloc[-1]
        
        return MarketIndicators(
            trend_strength=ts,
            momentum_60d=mom_60d,
            momentum_20d=mom_20d,
            momentum_5d=mom_5d,
            price_vs_ma60=price_vs_ma60,
            price_vs_ma250=price_vs_ma250 if not pd.isna(price_vs_ma250) else 0,
            volatility=volatility if not pd.isna(volatility) else 0,
            rsi=rsi if not pd.isna(rsi) else 50,
            ma_alignment=ma_alignment
        )
    
    def _identify_regime(self, ind: MarketIndicators, params: Dict) -> Tuple[MarketRegime, float, float, float]:
        """分层识别市场状态"""
        ts_bull = params['ts_bull']
        ts_bear = params['ts_bear']
        m60_bull = params['m60_bull']
        m60_bear = params['m60_bear']
        m20_bull = params['m20_bull']
        m20_bear = params['m20_bear']
        
        bull_score = 0.0
        bear_score = 0.0
        
        # 趋势强度贡献
        if ind.trend_strength > ts_bull:
            bull_score += 30
        elif ind.trend_strength > ts_bull - 20:
            bull_score += 15
        if ind.trend_strength < ts_bear:
            bear_score += 30
        elif ind.trend_strength < ts_bear + 20:
            bear_score += 15
        
        # 60日动量贡献
        if ind.momentum_60d > m60_bull:
            bull_score += 30
        elif ind.momentum_60d > m60_bull - 5:
            bull_score += 15
        if ind.momentum_60d < m60_bear:
            bear_score += 30
        elif ind.momentum_60d < m60_bear + 5:
            bear_score += 15
        
        # 20日动量贡献
        if ind.momentum_20d > m20_bull:
            bull_score += 20
        if ind.momentum_20d < m20_bear:
            bear_score += 20
        
        # 价格位置贡献
        if ind.price_vs_ma60 > 5:
            bull_score += 20
        elif ind.price_vs_ma60 > 0:
            bull_score += 10
        if ind.price_vs_ma60 < -5:
            bear_score += 20
        elif ind.price_vs_ma60 < 0:
            bear_score += 10
        
        # 决策
        if bull_score >= 60 and bull_score > bear_score + 20:
            regime = MarketRegime.BULL
            confidence = bull_score
        elif bear_score >= 60 and bear_score > bull_score + 20:
            regime = MarketRegime.BEAR
            confidence = bear_score
        else:
            regime = MarketRegime.SIDEWAYS
            confidence = 100 - max(bull_score, bear_score)
        
        return regime, confidence, bull_score, bear_score
    
    def analyze_both(self) -> Dict[str, RegimeResult]:
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
        
        # 综合判断
        if sh.regime == sz.regime:
            combined_regime = sh.regime.value
            combined_confidence = (sh.confidence + sz.confidence) / 2
        elif sh.is_reliable and not sz.is_reliable:
            combined_regime = sh.regime.value
            combined_confidence = sh.confidence
        elif sz.is_reliable and not sh.is_reliable:
            combined_regime = sz.regime.value
            combined_confidence = sz.confidence
        else:
            combined_regime = 'sideways'
            combined_confidence = 50
        
        return {
            'combined': {
                'regime': combined_regime,
                'regime_cn': MarketRegime(combined_regime).chinese,
                'confidence': round(combined_confidence, 1),
                'is_reliable': combined_confidence >= 70,
                'consensus': sh.regime == sz.regime
            },
            'shanghai': sh.to_dict(),
            'shenzhen': sz.to_dict(),
            'analysis_date': date.today().strftime("%Y-%m-%d")
        }


def quick_regime_check(benchmark: str = "000001.XSHG") -> Dict:
    """
    快速获取市场状态
    
    Args:
        benchmark: 指数代码，默认上证
        
    Returns:
        包含市场状态的字典
    """
    detector = MarketRegimeDetector()
    result = detector.analyze(benchmark=benchmark)
    return result.to_dict()


def get_market_environment() -> Dict:
    """
    获取完整市场环境（双指数）
    
    Returns:
        包含上证、深证和综合判断的字典
    """
    detector = MarketRegimeDetector()
    return detector.get_combined_view()


if __name__ == "__main__":
    # 测试
    print("=" * 70)
    print("🎯 市场环境识别器测试")
    print("=" * 70)
    
    env = get_market_environment()
    
    print(f"\n📊 综合判断:")
    print(f"  状态: {env['combined']['regime_cn']}")
    print(f"  置信度: {env['combined']['confidence']:.0f}%")
    print(f"  可靠性: {'✅' if env['combined']['is_reliable'] else '⚠️'}")
    print(f"  共识: {'✅一致' if env['combined']['consensus'] else '❌分歧'}")
    
    print(f"\n📈 上证指数:")
    sh = env['shanghai']
    print(f"  {sh['regime_cn']} ({sh['confidence']:.0f}%)")
    
    print(f"\n📈 深证成指:")
    sz = env['shenzhen']
    print(f"  {sz['regime_cn']} ({sz['confidence']:.0f}%)")

