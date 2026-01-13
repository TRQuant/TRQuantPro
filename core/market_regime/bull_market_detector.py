#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市状态检测器

集成MarketRegimeDetector，细分牛市强度等级，并提供牛市强度指标。
"""

import sys
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import pandas as pd
import numpy as np
import logging

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

logger = logging.getLogger(__name__)


class BullMarketStrength(Enum):
    """牛市强度等级"""
    BULL_STRONG = "BULL_STRONG"        # 强牛市：指数>MA20>MA60，成交量放大，涨幅>2%
    BULL_NORMAL = "BULL_NORMAL"        # 正常牛市：指数>MA20，成交量正常，涨幅0-2%
    BULL_LATE = "BULL_LATE"            # 牛市后期：指数高位震荡，成交量萎缩，涨幅<0
    BULL_PULLBACK = "BULL_PULLBACK"    # 牛市回调：短期回调，但趋势未破


@dataclass
class BullMarketIndicators:
    """牛市指标"""
    # 指数趋势
    index_price: float = 0.0
    index_ma20: float = 0.0
    index_ma60: float = 0.0
    index_position: float = 0.5      # 指数相对位置（0-1）
    
    # 成交量
    volume_ratio: float = 1.0        # 成交量比（vs 20日均量）
    volume_trend: float = 0.0        # 成交量趋势（5日均量 vs 20日均量）
    
    # 涨幅
    daily_return: float = 0.0        # 日涨幅（%）
    weekly_return: float = 0.0       # 周涨幅（%）
    monthly_return: float = 0.0      # 月涨幅（%）
    
    # 资金流向
    advance_decline_ratio: float = 0.5  # 涨跌比
    limit_up_count: int = 0          # 涨停数量
    limit_down_count: int = 0        # 跌停数量
    
    # 板块轮动
    sector_rotation_score: float = 0.0  # 板块轮动得分（0-100）
    active_sectors: int = 0          # 活跃板块数量
    
    # 情绪指标
    turnover_rate: float = 0.0       # 平均换手率
    margin_balance_growth: float = 0.0  # 融资余额增长率
    
    # 技术指标
    rsi: float = 50.0               # RSI（相对强弱指标）
    macd_hist: float = 0.0          # MACD柱状图
    atr_ratio: float = 1.0          # ATR比率
    
    # 时间
    date: str = ""
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'index_price': self.index_price,
            'index_ma20': self.index_ma20,
            'index_ma60': self.index_ma60,
            'index_position': self.index_position,
            'volume_ratio': self.volume_ratio,
            'volume_trend': self.volume_trend,
            'daily_return': self.daily_return,
            'weekly_return': self.weekly_return,
            'monthly_return': self.monthly_return,
            'advance_decline_ratio': self.advance_decline_ratio,
            'limit_up_count': self.limit_up_count,
            'limit_down_count': self.limit_down_count,
            'sector_rotation_score': self.sector_rotation_score,
            'active_sectors': self.active_sectors,
            'turnover_rate': self.turnover_rate,
            'margin_balance_growth': self.margin_balance_growth,
            'rsi': self.rsi,
            'macd_hist': self.macd_hist,
            'atr_ratio': self.atr_ratio,
            'date': self.date,
        }


@dataclass
class BullMarketResult:
    """牛市检测结果"""
    is_bull: bool                    # 是否为牛市
    strength: BullMarketStrength     # 牛市强度等级
    strength_score: float            # 牛市强度得分（0-100）
    confidence: float                # 判断置信度（0-1）
    
    # 市场环境（来自MarketRegimeDetector）
    base_regime: str                 # 基础市场环境（BULL/BEAR/VOLATILE等）
    base_score: float                # 基础得分
    
    # 牛市指标
    indicators: BullMarketIndicators = field(default_factory=BullMarketIndicators)
    
    # 建议
    position_suggestion: float = 0.5  # 仓位建议（0-1）
    strategy_suggestion: str = ""     # 策略建议
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'is_bull': self.is_bull,
            'strength': self.strength.value if isinstance(self.strength, Enum) else str(self.strength),
            'strength_score': self.strength_score,
            'confidence': self.confidence,
            'base_regime': self.base_regime,
            'base_score': self.base_score,
            'indicators': self.indicators.to_dict(),
            'position_suggestion': self.position_suggestion,
            'strategy_suggestion': self.strategy_suggestion,
        }


class BullMarketDetector:
    """牛市状态检测器"""
    
    def __init__(self, benchmark: str = '000300.XSHG', verbose: bool = True):
        """
        初始化
        
        Args:
            benchmark: 基准指数（默认沪深300）
            verbose: 是否输出详细信息
        """
        self.benchmark = benchmark
        self.verbose = verbose
        self.jq = None
        self.regime_detector = None
        self._init_dependencies()
    
    def _init_dependencies(self):
        """初始化依赖"""
        try:
            # JQData
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            config_mgr = get_config_manager()
            jq_config = config_mgr.get_config('jqdata')
            jq.auth(jq_config.get('username'), jq_config.get('password'))
            self.jq = jq
            
            if self.verbose:
                print("✅ JQData连接成功")
        except Exception as e:
            logger.error(f"JQData连接失败: {e}")
            raise
        
        try:
            # MarketRegimeDetector
            from core.market_regime.market_regime_detector import MarketRegimeDetector, MarketRegime
            self.regime_detector = MarketRegimeDetector()
            if self.verbose:
                print("✅ MarketRegimeDetector初始化成功")
        except Exception as e:
            logger.warning(f"MarketRegimeDetector初始化失败: {e}")
            self.regime_detector = None
    
    def get_index_data(self, date: str, lookback_days: int = 60) -> Optional[pd.DataFrame]:
        """获取指数数据"""
        try:
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - pd.Timedelta(days=lookback_days + 30)
            
            df = self.jq.get_price(
                self.benchmark,
                start_date=start_dt.strftime('%Y-%m-%d'),
                end_date=date,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume'],
                skip_paused=True,
                fq='post'
            )
            
            if df is not None:
                df.index = pd.to_datetime(df.index)
            
            return df
        except Exception as e:
            logger.error(f"获取指数数据失败: {e}")
            return None
    
    def calculate_indicators(self, df: pd.DataFrame, date: str) -> BullMarketIndicators:
        """计算牛市指标"""
        if df is None or len(df) < 60:
            return BullMarketIndicators(date=date)
        
        # 最新数据
        latest = df.iloc[-1]
        close = df['close']
        volume = df['volume']
        
        # 指数趋势
        ma20 = close[-20:].mean()
        ma60 = close[-60:].mean() if len(close) >= 60 else ma20
        current_price = close.iloc[-1]
        
        # 相对位置
        high_60 = close[-60:].max() if len(close) >= 60 else close.max()
        low_60 = close[-60:].min() if len(close) >= 60 else close.min()
        index_position = (current_price - low_60) / (high_60 - low_60) if (high_60 - low_60) > 0 else 0.5
        
        # 成交量
        volume_ma20 = volume[-20:].mean()
        volume_ma5 = volume[-5:].mean() if len(volume) >= 5 else volume_ma20
        volume_ratio = latest['volume'] / volume_ma20 if volume_ma20 > 0 else 1.0
        volume_trend = (volume_ma5 / volume_ma20 - 1) * 100 if volume_ma20 > 0 else 0.0
        
        # 涨幅
        daily_return = (close.iloc[-1] / close.iloc[-2] - 1) * 100 if len(close) >= 2 else 0.0
        weekly_return = (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else daily_return
        monthly_return = (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else weekly_return
        
        # 技术指标
        # RSI
        delta = close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain[-14:].mean() if len(gain) >= 14 else gain.mean()
        avg_loss = loss[-14:].mean() if len(loss) >= 14 else loss.mean()
        rs = avg_gain / avg_loss if avg_loss > 0 else 100
        rsi = 100 - (100 / (1 + rs))
        
        # MACD
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        macd_hist = (macd_line - signal_line).iloc[-1]
        
        # ATR（简化）
        high_low = df['high'] - df['low']
        high_close = (df['high'] - close.shift()).abs()
        low_close = (df['low'] - close.shift()).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr[-14:].mean() if len(tr) >= 14 else tr.mean()
        atr_ratio = atr / current_price if current_price > 0 else 1.0
        
        # 获取涨跌比和涨跌停数量（简化，实际需要全市场数据）
        # 这里使用指数数据估算
        advance_decline_ratio = 0.5  # 默认
        limit_up_count = 0
        limit_down_count = 0
        
        # 板块轮动（简化）
        sector_rotation_score = 50.0  # 默认
        active_sectors = 0
        
        # 换手率（简化）
        turnover_rate = volume_ratio * 2.0  # 估算
        
        # 融资余额（简化，需要额外数据源）
        margin_balance_growth = 0.0
        
        return BullMarketIndicators(
            index_price=current_price,
            index_ma20=ma20,
            index_ma60=ma60,
            index_position=index_position,
            volume_ratio=volume_ratio,
            volume_trend=volume_trend,
            daily_return=daily_return,
            weekly_return=weekly_return,
            monthly_return=monthly_return,
            advance_decline_ratio=advance_decline_ratio,
            limit_up_count=limit_up_count,
            limit_down_count=limit_down_count,
            sector_rotation_score=sector_rotation_score,
            active_sectors=active_sectors,
            turnover_rate=turnover_rate,
            margin_balance_growth=margin_balance_growth,
            rsi=rsi,
            macd_hist=macd_hist,
            atr_ratio=atr_ratio,
            date=date,
        )
    
    def calculate_strength_score(self, indicators: BullMarketIndicators) -> float:
        """计算牛市强度得分（0-100）"""
        score = 0.0
        
        # 1. 趋势得分（30%）
        if indicators.index_price > indicators.index_ma20 > indicators.index_ma60:
            trend_score = 30.0
        elif indicators.index_price > indicators.index_ma20:
            trend_score = 20.0
        else:
            trend_score = 10.0
        score += trend_score
        
        # 2. 成交量得分（20%）
        if indicators.volume_ratio > 1.5:
            volume_score = 20.0
        elif indicators.volume_ratio > 1.2:
            volume_score = 15.0
        elif indicators.volume_ratio > 1.0:
            volume_score = 10.0
        else:
            volume_score = 5.0
        score += volume_score
        
        # 3. 涨幅得分（20%）
        if indicators.weekly_return > 2.0:
            return_score = 20.0
        elif indicators.weekly_return > 0:
            return_score = 15.0
        elif indicators.weekly_return > -1.0:
            return_score = 10.0
        else:
            return_score = 5.0
        score += return_score
        
        # 4. 资金流向得分（15%）
        if indicators.advance_decline_ratio > 0.7:
            flow_score = 15.0
        elif indicators.advance_decline_ratio > 0.6:
            flow_score = 12.0
        elif indicators.advance_decline_ratio > 0.5:
            flow_score = 10.0
        else:
            flow_score = 5.0
        score += flow_score
        
        # 5. 技术指标得分（15%）
        if indicators.rsi > 60 and indicators.macd_hist > 0:
            tech_score = 15.0
        elif indicators.rsi > 50:
            tech_score = 12.0
        else:
            tech_score = 8.0
        score += tech_score
        
        return min(100.0, max(0.0, score))
    
    def determine_strength(self, indicators: BullMarketIndicators, strength_score: float) -> BullMarketStrength:
        """确定牛市强度等级"""
        # 趋势判断
        is_strong_trend = (indicators.index_price > indicators.index_ma20 > indicators.index_ma60)
        is_weak_trend = (indicators.index_price < indicators.index_ma20)
        
        # 成交量判断
        is_volume_expand = indicators.volume_ratio > 1.3
        
        # 涨幅判断
        is_strong_return = indicators.weekly_return > 2.0
        is_pullback = indicators.weekly_return < -1.0
        
        # 综合判断
        if is_strong_trend and is_volume_expand and is_strong_return:
            return BullMarketStrength.BULL_STRONG
        elif is_strong_trend and not is_weak_trend:
            if is_pullback:
                return BullMarketStrength.BULL_PULLBACK
            else:
                return BullMarketStrength.BULL_NORMAL
        elif is_weak_trend or indicators.index_position < 0.5:
            return BullMarketStrength.BULL_LATE
        else:
            return BullMarketStrength.BULL_NORMAL
    
    def detect(self, date: str = None) -> BullMarketResult:
        """
        检测牛市状态
        
        Args:
            date: 日期（None表示今天）
        
        Returns:
            BullMarketResult
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 获取指数数据
        df = self.get_index_data(date)
        if df is None or len(df) < 60:
            return BullMarketResult(
                is_bull=False,
                strength=BullMarketStrength.BULL_NORMAL,
                strength_score=0.0,
                confidence=0.0,
                base_regime='UNKNOWN',
                base_score=0.0,
                indicators=BullMarketIndicators(date=date)
            )
        
        # 计算指标
        indicators = self.calculate_indicators(df, date)
        
        # 检测基础市场环境
        base_regime = 'VOLATILE'
        base_score = 50.0
        if self.regime_detector:
            try:
                regime_result = self.regime_detector.detect_regime(date=date)
                base_regime = regime_result.regime.value if hasattr(regime_result.regime, 'value') else str(regime_result.regime)
                base_score = regime_result.score if hasattr(regime_result, 'score') else 50.0
            except Exception as e:
                logger.warning(f"MarketRegimeDetector检测失败: {e}")
        
        # 判断是否为牛市
        is_bull = (base_regime == 'BULL' or 
                  (indicators.index_price > indicators.index_ma20 > indicators.index_ma60) or
                  base_score > 60.0)
        
        if not is_bull:
            return BullMarketResult(
                is_bull=False,
                strength=BullMarketStrength.BULL_NORMAL,
                strength_score=0.0,
                confidence=0.0,
                base_regime=base_regime,
                base_score=base_score,
                indicators=indicators
            )
        
        # 计算强度得分
        strength_score = self.calculate_strength_score(indicators)
        
        # 确定强度等级
        strength = self.determine_strength(indicators, strength_score)
        
        # 计算置信度
        confidence = min(1.0, strength_score / 100.0)
        
        # 生成建议
        position_suggestion = self._get_position_suggestion(strength, strength_score)
        strategy_suggestion = self._get_strategy_suggestion(strength, strength_score)
        
        result = BullMarketResult(
            is_bull=True,
            strength=strength,
            strength_score=strength_score,
            confidence=confidence,
            base_regime=base_regime,
            base_score=base_score,
            indicators=indicators,
            position_suggestion=position_suggestion,
            strategy_suggestion=strategy_suggestion,
        )
        
        if self.verbose:
            print(f"\n✅ 牛市检测结果 ({date})")
            print(f"  是否为牛市: {is_bull}")
            print(f"  强度等级: {strength.value}")
            print(f"  强度得分: {strength_score:.1f}/100")
            print(f"  置信度: {confidence:.2f}")
            print(f"  仓位建议: {position_suggestion*100:.0f}%")
            print(f"  策略建议: {strategy_suggestion}")
        
        return result
    
    def _get_position_suggestion(self, strength: BullMarketStrength, score: float) -> float:
        """获取仓位建议（0-1）"""
        if strength == BullMarketStrength.BULL_STRONG:
            return 0.9  # 90%
        elif strength == BullMarketStrength.BULL_NORMAL:
            return 0.7  # 70%
        elif strength == BullMarketStrength.BULL_LATE:
            return 0.4  # 40%
        elif strength == BullMarketStrength.BULL_PULLBACK:
            return 0.6  # 60%
        else:
            return 0.5
    
    def _get_strategy_suggestion(self, strength: BullMarketStrength, score: float) -> str:
        """获取策略建议"""
        if strength == BullMarketStrength.BULL_STRONG:
            return "激进做多：主线赛道龙头，高成长科技股，可加杠杆"
        elif strength == BullMarketStrength.BULL_NORMAL:
            return "积极做多：优质成长股，适度分散，关注板块轮动"
        elif strength == BullMarketStrength.BULL_LATE:
            return "谨慎做多：逐步减仓，锁定利润，关注风险信号"
        elif strength == BullMarketStrength.BULL_PULLBACK:
            return "逢低布局：回调是买入机会，但需控制仓位，分批建仓"
        else:
            return "观望为主：等待市场信号明确"


def main():
    """主函数：示例用法"""
    import argparse
    
    parser = argparse.ArgumentParser(description='检测牛市状态')
    parser.add_argument('--date', type=str, default=None, help='日期（YYYY-MM-DD，默认今天）')
    parser.add_argument('--benchmark', type=str, default='000300.XSHG', help='基准指数')
    
    args = parser.parse_args()
    
    # 创建检测器
    detector = BullMarketDetector(benchmark=args.benchmark, verbose=True)
    
    # 检测
    result = detector.detect(date=args.date)
    
    # 输出结果
    print("\n" + "="*60)
    print("牛市检测结果")
    print("="*60)
    print(result.to_dict())


if __name__ == '__main__':
    main()
