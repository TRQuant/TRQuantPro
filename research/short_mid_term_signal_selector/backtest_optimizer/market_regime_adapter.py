# -*- coding: utf-8 -*-
"""
市场环境自适应器 (Market Regime Adapter)

核心功能：
1. 识别当前市场环境（牛市/熊市/震荡）
2. 根据环境调整策略参数
3. 不同环境使用不同的因子权重组合
4. 环境切换时平滑过渡
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# JQData
try:
    import jqdatasdk as jq
    HAS_JQDATA = True
except ImportError:
    HAS_JQDATA = False


class MarketRegime(Enum):
    """市场状态枚举"""
    STRONG_BULL = 'strong_bull'     # 强牛市
    BULL = 'bull'                    # 牛市
    NEUTRAL = 'neutral'              # 震荡市
    BEAR = 'bear'                    # 熊市
    STRONG_BEAR = 'strong_bear'     # 强熊市


@dataclass
class RegimeConfig:
    """市场环境配置"""
    regime: MarketRegime
    description: str
    
    # 策略参数
    position_limit: float           # 仓位上限
    single_stock_limit: float       # 单只股票仓位上限
    stop_loss_pct: float           # 止损比例
    take_profit_pct: float         # 止盈比例
    
    # 因子权重调整系数
    factor_adjustments: Dict[str, float]  # 因子权重乘数
    
    # 筛选条件调整
    min_score_threshold: float      # 最低得分阈值
    max_candidates: int             # 最大候选数


# 不同市场环境的策略配置
REGIME_CONFIGS = {
    MarketRegime.STRONG_BULL: RegimeConfig(
        regime=MarketRegime.STRONG_BULL,
        description='强牛市：全面上涨，风险偏好高',
        position_limit=0.9,
        single_stock_limit=0.15,
        stop_loss_pct=0.10,
        take_profit_pct=0.30,
        factor_adjustments={
            'roe': 0.8,
            'gross_margin': 0.8,
            'revenue_growth': 1.2,
            'profit_growth': 1.2,
            'pe_score': 0.7,
            'peg_score': 0.8,
            'trend_score': 1.3,
            'momentum_score': 1.5,
            'sector_weight': 1.2,
        },
        min_score_threshold=60,
        max_candidates=10
    ),
    
    MarketRegime.BULL: RegimeConfig(
        regime=MarketRegime.BULL,
        description='牛市：稳定上涨，适度进攻',
        position_limit=0.8,
        single_stock_limit=0.12,
        stop_loss_pct=0.08,
        take_profit_pct=0.25,
        factor_adjustments={
            'roe': 1.0,
            'gross_margin': 0.9,
            'revenue_growth': 1.1,
            'profit_growth': 1.1,
            'pe_score': 0.8,
            'peg_score': 0.9,
            'trend_score': 1.2,
            'momentum_score': 1.2,
            'sector_weight': 1.1,
        },
        min_score_threshold=65,
        max_candidates=8
    ),
    
    MarketRegime.NEUTRAL: RegimeConfig(
        regime=MarketRegime.NEUTRAL,
        description='震荡市：方向不明，精选个股',
        position_limit=0.6,
        single_stock_limit=0.10,
        stop_loss_pct=0.06,
        take_profit_pct=0.15,
        factor_adjustments={
            'roe': 1.2,
            'gross_margin': 1.2,
            'revenue_growth': 1.0,
            'profit_growth': 1.0,
            'pe_score': 1.1,
            'peg_score': 1.1,
            'trend_score': 0.8,
            'momentum_score': 0.7,
            'sector_weight': 0.9,
        },
        min_score_threshold=70,
        max_candidates=5
    ),
    
    MarketRegime.BEAR: RegimeConfig(
        regime=MarketRegime.BEAR,
        description='熊市：防守为主，严格选股',
        position_limit=0.4,
        single_stock_limit=0.08,
        stop_loss_pct=0.05,
        take_profit_pct=0.10,
        factor_adjustments={
            'roe': 1.3,
            'gross_margin': 1.3,
            'revenue_growth': 0.9,
            'profit_growth': 0.9,
            'pe_score': 1.3,
            'peg_score': 1.2,
            'trend_score': 0.6,
            'momentum_score': 0.5,
            'sector_weight': 0.7,
        },
        min_score_threshold=75,
        max_candidates=5
    ),
    
    MarketRegime.STRONG_BEAR: RegimeConfig(
        regime=MarketRegime.STRONG_BEAR,
        description='强熊市：现金为王，极度谨慎',
        position_limit=0.2,
        single_stock_limit=0.05,
        stop_loss_pct=0.03,
        take_profit_pct=0.08,
        factor_adjustments={
            'roe': 1.5,
            'gross_margin': 1.5,
            'revenue_growth': 0.7,
            'profit_growth': 0.7,
            'pe_score': 1.5,
            'peg_score': 1.3,
            'trend_score': 0.4,
            'momentum_score': 0.3,
            'sector_weight': 0.5,
        },
        min_score_threshold=80,
        max_candidates=3
    ),
}


@dataclass
class RegimeSignal:
    """市场状态信号"""
    regime: MarketRegime
    confidence: float           # 置信度 0-100
    
    # 技术指标
    index_return_20d: float     # 20日收益
    index_return_60d: float     # 60日收益
    ma_position: str            # 均线位置
    volatility_level: str       # 波动率水平
    
    # 市场宽度
    advance_decline_ratio: float  # 涨跌比
    stocks_above_ma20_pct: float  # 站上20日均线比例
    
    # 时间戳
    timestamp: datetime = field(default_factory=datetime.now)


class MarketRegimeAdapter:
    """
    市场环境自适应器
    
    设计原则：
    1. 多维度识别市场状态
    2. 平滑切换避免频繁变动
    3. 为不同环境提供差异化策略
    """
    
    def __init__(self, 
                 benchmark: str = '000300.XSHG',
                 lookback_days: int = 60):
        """
        Args:
            benchmark: 基准指数
            lookback_days: 回看天数
        """
        self.benchmark = benchmark
        self.lookback_days = lookback_days
        
        # 状态历史（用于平滑）
        self.regime_history: List[MarketRegime] = []
        self.signal_history: List[RegimeSignal] = []
        
        # 初始化JQData
        self._init_jqdata()
        
    def _init_jqdata(self):
        """初始化聚宽连接"""
        if not HAS_JQDATA:
            return
        try:
            if not jq.is_auth():
                from core.jqdata_auth import auth_jqdata
                auth_jqdata()
        except:
            pass
    
    def detect_regime(self, as_of_date: str = None) -> RegimeSignal:
        """
        检测当前市场状态
        
        Args:
            as_of_date: 基准日期，默认今天
            
        Returns:
            RegimeSignal: 市场状态信号
        """
        if as_of_date is None:
            as_of_date = datetime.now().strftime('%Y-%m-%d')
            
        print(f"\n🔍 检测市场状态: {as_of_date}")
        
        # 获取指数数据
        index_data = self._get_index_data(as_of_date)
        
        if index_data is None or len(index_data) < 20:
            print("⚠️ 数据不足，返回中性状态")
            return RegimeSignal(
                regime=MarketRegime.NEUTRAL,
                confidence=50,
                index_return_20d=0,
                index_return_60d=0,
                ma_position='neutral',
                volatility_level='medium',
                advance_decline_ratio=1.0,
                stocks_above_ma20_pct=50
            )
        
        # 计算技术指标
        returns_20d = self._calc_return(index_data, 20)
        returns_60d = self._calc_return(index_data, 60)
        ma_position = self._determine_ma_position(index_data)
        volatility = self._calc_volatility_level(index_data)
        
        # 获取市场宽度
        breadth = self._get_market_breadth(as_of_date)
        
        # 综合判断
        regime, confidence = self._determine_regime(
            returns_20d, returns_60d, 
            ma_position, volatility, breadth
        )
        
        signal = RegimeSignal(
            regime=regime,
            confidence=confidence,
            index_return_20d=returns_20d,
            index_return_60d=returns_60d,
            ma_position=ma_position,
            volatility_level=volatility,
            advance_decline_ratio=breadth.get('adv_dec_ratio', 1.0),
            stocks_above_ma20_pct=breadth.get('above_ma20_pct', 50)
        )
        
        # 应用平滑
        smoothed_regime = self._smooth_regime(regime)
        signal.regime = smoothed_regime
        
        # 记录历史
        self.regime_history.append(smoothed_regime)
        self.signal_history.append(signal)
        
        self._print_signal(signal)
        
        return signal
    
    def get_strategy_config(self, regime: MarketRegime = None) -> RegimeConfig:
        """
        获取策略配置
        
        Args:
            regime: 市场状态，None则使用最新检测结果
            
        Returns:
            RegimeConfig: 策略配置
        """
        if regime is None:
            if self.regime_history:
                regime = self.regime_history[-1]
            else:
                regime = MarketRegime.NEUTRAL
                
        return REGIME_CONFIGS.get(regime, REGIME_CONFIGS[MarketRegime.NEUTRAL])
    
    def adjust_factor_weights(self, 
                             base_weights: Dict[str, float],
                             regime: MarketRegime = None) -> Dict[str, float]:
        """
        根据市场环境调整因子权重
        
        Args:
            base_weights: 基础权重
            regime: 市场状态
            
        Returns:
            Dict: 调整后的权重
        """
        config = self.get_strategy_config(regime)
        
        adjusted = {}
        for factor, weight in base_weights.items():
            multiplier = config.factor_adjustments.get(factor, 1.0)
            adjusted[factor] = weight * multiplier
        
        # 归一化
        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: v/total for k, v in adjusted.items()}
            
        return adjusted
    
    def _get_index_data(self, as_of_date: str) -> Optional[pd.DataFrame]:
        """获取指数数据"""
        if not HAS_JQDATA:
            return None
            
        try:
            end_date = as_of_date
            start_date = (datetime.strptime(as_of_date, '%Y-%m-%d') - 
                         timedelta(days=self.lookback_days * 2)).strftime('%Y-%m-%d')
            
            df = jq.get_price(
                self.benchmark,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume']
            )
            return df
        except Exception as e:
            print(f"❌ 获取指数数据失败: {e}")
            return None
    
    def _calc_return(self, df: pd.DataFrame, days: int) -> float:
        """计算N日收益率"""
        if len(df) < days:
            return 0
        return (df['close'].iloc[-1] / df['close'].iloc[-days] - 1) * 100
    
    def _determine_ma_position(self, df: pd.DataFrame) -> str:
        """判断均线位置"""
        if len(df) < 60:
            return 'neutral'
            
        close = df['close'].iloc[-1]
        ma5 = df['close'].tail(5).mean()
        ma20 = df['close'].tail(20).mean()
        ma60 = df['close'].tail(60).mean()
        
        if close > ma5 > ma20 > ma60:
            return 'strong_bullish'
        elif close > ma20 > ma60:
            return 'bullish'
        elif close < ma5 < ma20 < ma60:
            return 'strong_bearish'
        elif close < ma20 < ma60:
            return 'bearish'
        else:
            return 'neutral'
    
    def _calc_volatility_level(self, df: pd.DataFrame) -> str:
        """计算波动率水平"""
        if len(df) < 20:
            return 'medium'
            
        returns = df['close'].pct_change().dropna()
        vol = returns.tail(20).std() * np.sqrt(252) * 100
        
        if vol > 30:
            return 'high'
        elif vol > 15:
            return 'medium'
        else:
            return 'low'
    
    def _get_market_breadth(self, as_of_date: str) -> Dict:
        """获取市场宽度指标"""
        if not HAS_JQDATA:
            return {'adv_dec_ratio': 1.0, 'above_ma20_pct': 50}
            
        try:
            # 获取全市场股票
            all_stocks = jq.get_all_securities(types=['stock'], date=as_of_date)
            codes = all_stocks.index.tolist()[:500]  # 限制数量
            
            # 获取价格数据
            df = jq.get_price(
                codes,
                start_date=(datetime.strptime(as_of_date, '%Y-%m-%d') - 
                           timedelta(days=30)).strftime('%Y-%m-%d'),
                end_date=as_of_date,
                frequency='daily',
                fields=['close'],
                panel=False
            )
            
            if df.empty:
                return {'adv_dec_ratio': 1.0, 'above_ma20_pct': 50}
            
            # 计算涨跌比
            latest = df.groupby('code').last()['close']
            prev = df.groupby('code').nth(-2)['close']
            
            advances = (latest > prev).sum()
            declines = (latest < prev).sum()
            adv_dec_ratio = advances / max(declines, 1)
            
            # 计算站上MA20比例
            above_ma20 = 0
            for code in codes[:200]:
                code_df = df[df['code'] == code]
                if len(code_df) >= 20:
                    ma20 = code_df['close'].tail(20).mean()
                    if code_df['close'].iloc[-1] > ma20:
                        above_ma20 += 1
                        
            above_ma20_pct = above_ma20 / 200 * 100 if len(codes) >= 200 else 50
            
            return {
                'adv_dec_ratio': adv_dec_ratio,
                'above_ma20_pct': above_ma20_pct
            }
            
        except Exception as e:
            print(f"⚠️ 获取市场宽度失败: {e}")
            return {'adv_dec_ratio': 1.0, 'above_ma20_pct': 50}
    
    def _determine_regime(self, 
                         ret_20d: float, 
                         ret_60d: float,
                         ma_pos: str,
                         volatility: str,
                         breadth: Dict) -> Tuple[MarketRegime, float]:
        """综合判断市场状态"""
        score = 0
        confidence_factors = []
        
        # 20日收益权重：30%
        if ret_20d > 10:
            score += 30
            confidence_factors.append(90)
        elif ret_20d > 5:
            score += 20
            confidence_factors.append(75)
        elif ret_20d > 0:
            score += 10
            confidence_factors.append(60)
        elif ret_20d > -5:
            score += -10
            confidence_factors.append(60)
        elif ret_20d > -10:
            score += -20
            confidence_factors.append(75)
        else:
            score += -30
            confidence_factors.append(90)
        
        # 60日收益权重：25%
        if ret_60d > 15:
            score += 25
        elif ret_60d > 5:
            score += 15
        elif ret_60d > -5:
            score += 0
        elif ret_60d > -15:
            score += -15
        else:
            score += -25
        
        # 均线位置权重：25%
        ma_scores = {
            'strong_bullish': 25,
            'bullish': 15,
            'neutral': 0,
            'bearish': -15,
            'strong_bearish': -25
        }
        score += ma_scores.get(ma_pos, 0)
        
        # 市场宽度权重：20%
        adv_dec = breadth.get('adv_dec_ratio', 1.0)
        above_ma20 = breadth.get('above_ma20_pct', 50)
        
        if adv_dec > 2 and above_ma20 > 70:
            score += 20
        elif adv_dec > 1.5 and above_ma20 > 60:
            score += 10
        elif adv_dec < 0.5 and above_ma20 < 30:
            score += -20
        elif adv_dec < 0.75 and above_ma20 < 40:
            score += -10
        
        # 波动率调整
        if volatility == 'high':
            score *= 0.9  # 高波动降低置信度
        
        # 判断状态
        if score >= 60:
            regime = MarketRegime.STRONG_BULL
        elif score >= 30:
            regime = MarketRegime.BULL
        elif score >= -30:
            regime = MarketRegime.NEUTRAL
        elif score >= -60:
            regime = MarketRegime.BEAR
        else:
            regime = MarketRegime.STRONG_BEAR
        
        # 计算置信度
        confidence = min(100, 50 + abs(score))
        
        return regime, confidence
    
    def _smooth_regime(self, current_regime: MarketRegime) -> MarketRegime:
        """平滑状态切换"""
        if len(self.regime_history) < 3:
            return current_regime
        
        # 统计最近5次状态
        recent = self.regime_history[-5:] + [current_regime]
        regime_counts = {}
        for r in recent:
            regime_counts[r] = regime_counts.get(r, 0) + 1
        
        # 返回出现最多的状态
        return max(regime_counts, key=regime_counts.get)
    
    def _print_signal(self, signal: RegimeSignal):
        """打印信号详情"""
        regime_emoji = {
            MarketRegime.STRONG_BULL: '🚀',
            MarketRegime.BULL: '📈',
            MarketRegime.NEUTRAL: '➡️',
            MarketRegime.BEAR: '📉',
            MarketRegime.STRONG_BEAR: '💥'
        }
        
        emoji = regime_emoji.get(signal.regime, '❓')
        config = REGIME_CONFIGS.get(signal.regime)
        
        print(f"\n{'='*50}")
        print(f"{emoji} 市场状态: {signal.regime.value}")
        print(f"{'='*50}")
        print(f"📊 置信度: {signal.confidence:.0f}%")
        print(f"📈 20日收益: {signal.index_return_20d:+.2f}%")
        print(f"📈 60日收益: {signal.index_return_60d:+.2f}%")
        print(f"📊 均线位置: {signal.ma_position}")
        print(f"📊 波动水平: {signal.volatility_level}")
        print(f"📊 涨跌比: {signal.advance_decline_ratio:.2f}")
        print(f"📊 站上MA20: {signal.stocks_above_ma20_pct:.1f}%")
        
        if config:
            print(f"\n💡 策略建议:")
            print(f"   {config.description}")
            print(f"   仓位上限: {config.position_limit*100:.0f}%")
            print(f"   止损线: {config.stop_loss_pct*100:.1f}%")


if __name__ == '__main__':
    print("🧪 测试市场环境适配器...")
    
    adapter = MarketRegimeAdapter()
    signal = adapter.detect_regime()
    
    # 获取策略配置
    config = adapter.get_strategy_config()
    print(f"\n当前策略配置: {config.description}")
