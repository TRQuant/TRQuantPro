"""
市场状态识别库 v4.0

完整的14种市场状态定义与识别
支持JQData和akshare双数据源
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MarketState(Enum):
    """
    14种市场状态定义
    
    牛市系列 (4种):
    - BULL_STRONG: 强势牛市
    - BULL_NORMAL: 正常牛市
    - BULL_LATE: 牛市后期
    - BULL_PULLBACK: 牛市回调
    
    熊市系列 (4种):
    - BEAR_STRONG: 强势熊市
    - BEAR_NORMAL: 正常熊市
    - BEAR_LATE: 熊市后期
    - BEAR_BOUNCE: 熊市反弹
    
    震荡系列 (4种):
    - RANGE_HIGH: 高位震荡
    - RANGE_MID: 中位震荡
    - RANGE_LOW: 低位震荡
    - RANGE_WIDE: 宽幅震荡
    
    转折系列 (2种):
    - TURNING_UP: 底部反转
    - TURNING_DOWN: 顶部反转
    """
    BULL_STRONG = "强势牛市"
    BULL_NORMAL = "正常牛市"
    BULL_LATE = "牛市后期"
    BULL_PULLBACK = "牛市回调"
    
    BEAR_STRONG = "强势熊市"
    BEAR_NORMAL = "正常熊市"
    BEAR_LATE = "熊市后期"
    BEAR_BOUNCE = "熊市反弹"
    
    RANGE_HIGH = "高位震荡"
    RANGE_MID = "中位震荡"
    RANGE_LOW = "低位震荡"
    RANGE_WIDE = "宽幅震荡"
    
    TURNING_UP = "底部反转"
    TURNING_DOWN = "顶部反转"
    
    @property
    def category(self) -> str:
        """类别: bull/bear/range/turning"""
        if 'BULL' in self.name:
            return 'bull'
        elif 'BEAR' in self.name:
            return 'bear'
        elif 'RANGE' in self.name:
            return 'range'
        else:
            return 'turning'
    
    @property
    def direction(self) -> int:
        """方向: 1=多, -1=空, 0=中性"""
        if self.category == 'bull' or self == MarketState.TURNING_UP:
            return 1
        elif self.category == 'bear' or self == MarketState.TURNING_DOWN:
            return -1
        return 0


# 14种状态的量化定义
STATE_DEFINITIONS = {
    MarketState.BULL_STRONG: {
        'description': '全面上涨，远超年线，接近年内高点',
        'conditions': {
            'mom_120d': ('>',  15),   # 120日动量 > 15%
            'vs_ma250': ('>',  10),   # 年线偏离 > 10%
            'pos_250d': ('>',  80),   # 250日位置 > 80%
            'ma_bull':  ('==', True)  # 均线多头排列
        },
        'position': (0.8, 1.0),
        'risk': 'low',
        'strategy': 'trend_following'
    },
    MarketState.BULL_NORMAL: {
        'description': '稳健上涨，高于年线，位于较高位置',
        'conditions': {
            'mom_120d': ('>',  10),
            'vs_ma250': ('>',  5),
            'pos_250d': ('>',  60)
        },
        'position': (0.6, 0.8),
        'risk': 'low',
        'strategy': 'trend_following'
    },
    MarketState.BULL_LATE: {
        'description': '上涨动能减弱，位置较高',
        'conditions': {
            'mom_120d': ('>',  5),
            'vs_ma250': ('>',  0),
            'pos_250d': ('>',  70),
            'momentum_weakening': ('==', True)  # 动能减弱
        },
        'position': (0.4, 0.6),
        'risk': 'medium',
        'strategy': 'cautious_long'
    },
    MarketState.BULL_PULLBACK: {
        'description': '中期趋势向上，短期回调',
        'conditions': {
            'mom_120d': ('>',  5),
            'vs_ma250': ('>',  0),
            'mom_20d':  ('<',  0)
        },
        'position': (0.5, 0.7),
        'risk': 'medium',
        'strategy': 'buy_dip'
    },
    MarketState.BEAR_STRONG: {
        'description': '全面下跌，远低于年线，接近年内低点',
        'conditions': {
            'mom_120d': ('<', -15),
            'vs_ma250': ('<', -10),
            'pos_250d': ('<',  20),
            'ma_bear':  ('==', True)
        },
        'position': (0.0, 0.2),
        'risk': 'high',
        'strategy': 'defensive'
    },
    MarketState.BEAR_NORMAL: {
        'description': '稳定下跌，低于年线',
        'conditions': {
            'mom_120d': ('<', -10),
            'vs_ma250': ('<', -5),
            'pos_250d': ('<',  40)
        },
        'position': (0.1, 0.3),
        'risk': 'high',
        'strategy': 'defensive'
    },
    MarketState.BEAR_LATE: {
        'description': '下跌动能减弱，位置较低',
        'conditions': {
            'mom_120d': ('<', -5),
            'vs_ma250': ('<',  0),
            'pos_250d': ('<',  30),
            'momentum_recovering': ('==', True)
        },
        'position': (0.3, 0.5),
        'risk': 'medium',
        'strategy': 'accumulate'
    },
    MarketState.BEAR_BOUNCE: {
        'description': '中期趋势向下，短期反弹',
        'conditions': {
            'mom_120d': ('<', -5),
            'vs_ma250': ('<',  0),
            'mom_20d':  ('>',  0)
        },
        'position': (0.2, 0.4),
        'risk': 'medium',
        'strategy': 'reduce_on_rally'
    },
    MarketState.RANGE_HIGH: {
        'description': '在年内高位区间波动',
        'conditions': {
            'pos_250d':     ('>',  70),
            'abs_mom_60d':  ('<',  8)
        },
        'position': (0.4, 0.6),
        'risk': 'medium',
        'strategy': 'range_trading'
    },
    MarketState.RANGE_MID: {
        'description': '在年内中间位置波动',
        'conditions': {
            'pos_250d':     ('between', (30, 70)),
            'abs_mom_60d':  ('<',  5)
        },
        'position': (0.3, 0.5),
        'risk': 'medium',
        'strategy': 'range_trading'
    },
    MarketState.RANGE_LOW: {
        'description': '在年内低位区间波动',
        'conditions': {
            'pos_250d':     ('<',  30),
            'abs_mom_60d':  ('<',  8)
        },
        'position': (0.4, 0.6),
        'risk': 'medium',
        'strategy': 'accumulate'
    },
    MarketState.RANGE_WIDE: {
        'description': '大幅波动但无明确方向',
        'conditions': {
            'abs_mom_120d': ('<',  10),
            'abs_mom_60d':  ('>',  8)
        },
        'position': (0.3, 0.5),
        'risk': 'high',
        'strategy': 'volatility_trading'
    },
    MarketState.TURNING_UP: {
        'description': '长期下跌后开始上涨',
        'conditions': {
            'mom_120d':  ('<',  0),
            'mom_60d':   ('>',  5),
            'mom_20d':   ('>',  3),
            'pos_250d':  ('<',  50)
        },
        'position': (0.5, 0.7),
        'risk': 'medium',
        'strategy': 'early_long'
    },
    MarketState.TURNING_DOWN: {
        'description': '长期上涨后开始下跌',
        'conditions': {
            'mom_120d':  ('>',  0),
            'mom_60d':   ('<', -5),
            'mom_20d':   ('<', -3),
            'pos_250d':  ('>',  50)
        },
        'position': (0.2, 0.4),
        'risk': 'high',
        'strategy': 'reduce_position'
    }
}


@dataclass
class MarketIndicators:
    """市场指标数据"""
    # 动量指标
    mom_5d: float = 0.0
    mom_10d: float = 0.0
    mom_20d: float = 0.0
    mom_60d: float = 0.0
    mom_120d: float = 0.0
    
    # 均线偏离
    vs_ma5: float = 0.0
    vs_ma10: float = 0.0
    vs_ma20: float = 0.0
    vs_ma60: float = 0.0
    vs_ma120: float = 0.0
    vs_ma250: float = 0.0
    
    # 位置指标
    pos_20d: float = 50.0
    pos_60d: float = 50.0
    pos_250d: float = 50.0
    
    # 均线排列
    ma_bull: bool = False
    ma_bear: bool = False
    
    # 波动率
    volatility_20d: float = 0.0
    
    # 辅助指标
    abs_mom_60d: float = 0.0
    abs_mom_120d: float = 0.0
    momentum_weakening: bool = False
    momentum_recovering: bool = False
    
    def to_dict(self) -> dict:
        return {
            'mom_5d': round(self.mom_5d, 2),
            'mom_10d': round(self.mom_10d, 2),
            'mom_20d': round(self.mom_20d, 2),
            'mom_60d': round(self.mom_60d, 2),
            'mom_120d': round(self.mom_120d, 2),
            'vs_ma20': round(self.vs_ma20, 2),
            'vs_ma60': round(self.vs_ma60, 2),
            'vs_ma250': round(self.vs_ma250, 2),
            'pos_250d': round(self.pos_250d, 2),
            'ma_bull': self.ma_bull,
            'ma_bear': self.ma_bear,
            'volatility_20d': round(self.volatility_20d, 2)
        }


@dataclass
class MarketStateResult:
    """市场状态识别结果"""
    state: MarketState
    confidence: float          # 0-100
    score: float              # -100到100
    indicators: MarketIndicators
    position_range: Tuple[float, float]
    risk_level: str
    strategy: str
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    data_source: str = 'unknown'
    
    def to_dict(self) -> dict:
        return {
            'state': self.state.name,
            'state_name': self.state.value,
            'category': self.state.category,
            'direction': self.state.direction,
            'confidence': round(self.confidence, 2),
            'score': round(self.score, 2),
            'position_min': self.position_range[0],
            'position_max': self.position_range[1],
            'suggested_position': (self.position_range[0] + self.position_range[1]) / 2,
            'risk_level': self.risk_level,
            'strategy': self.strategy,
            'description': self.description,
            'indicators': self.indicators.to_dict(),
            'timestamp': self.timestamp.isoformat(),
            'data_source': self.data_source
        }


class MarketStateIdentifier:
    """
    市场状态识别器
    
    支持双数据源（JQData + akshare）
    完整的14种状态识别
    """
    
    def __init__(self, use_akshare: bool = False):
        """
        初始化
        
        Args:
            use_akshare: 是否使用akshare（更新数据源）
        """
        self.use_akshare = use_akshare
        self._jq_authenticated = False
    
    def identify(self, 
                 df: pd.DataFrame = None,
                 symbol: str = '000001.XSHG') -> MarketStateResult:
        """
        识别市场状态
        
        Args:
            df: OHLCV数据（可选）
            symbol: 指数代码
            
        Returns:
            MarketStateResult
        """
        # 获取数据
        if df is None:
            df, source = self._get_data(symbol)
        else:
            source = 'provided'
        
        # 计算指标
        indicators = self._calculate_indicators(df)
        
        # 识别状态
        state, confidence, score = self._determine_state(indicators)
        
        # 获取状态定义
        state_def = STATE_DEFINITIONS.get(state, {})
        
        return MarketStateResult(
            state=state,
            confidence=confidence,
            score=score,
            indicators=indicators,
            position_range=state_def.get('position', (0.3, 0.5)),
            risk_level=state_def.get('risk', 'medium'),
            strategy=state_def.get('strategy', 'balanced'),
            description=state_def.get('description', ''),
            data_source=source
        )
    
    def _get_data(self, symbol: str) -> Tuple[pd.DataFrame, str]:
        """获取数据"""
        # 优先使用JQData (聚宽)
        try:
            import jqdatasdk as jq
            
            if not self._jq_authenticated:
                import json
                with open('/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json') as f:
                    cfg = json.load(f)
                jq.auth(cfg['username'], cfg['password'])
                self._jq_authenticated = True
            
            from datetime import datetime
            today = datetime.now().strftime('%Y-%m-%d')
            df = jq.get_price(symbol, count=300, end_date=today, frequency='daily',
                             fields=['open', 'high', 'low', 'close', 'volume'])
            if df is not None and len(df) > 0:
                logger.info(f"JQData获取数据成功: {symbol}, {len(df)}条")
                return df, 'jqdata'
        except Exception as e:
            logger.warning(f"JQData获取数据失败: {e}")
        
        # 备用: akshare
        if self.use_akshare:
            try:
                import akshare as ak
                
                # 转换代码格式
                if symbol == '000001.XSHG':
                    ak_symbol = 'sh000001'
                elif symbol == '399001.XSHE':
                    ak_symbol = 'sz399001'
                else:
                    ak_symbol = symbol
                
                df = ak.stock_zh_index_daily(symbol=ak_symbol)
                df = df.tail(300).copy()
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                
                return df, 'akshare'
            except Exception as e:
                logger.warning(f"akshare获取数据失败: {e}")
        
        # 回退到JQData
        try:
            import jqdatasdk as jq
            
            if not self._jq_authenticated:
                import json
                with open('/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json') as f:
                    cfg = json.load(f)
                jq.auth(cfg['username'], cfg['password'])
                self._jq_authenticated = True
            
            from datetime import datetime
            today = datetime.now().strftime('%Y-%m-%d')
            df = jq.get_price(symbol, count=300, end_date=today, frequency='daily',
                             fields=['open', 'high', 'low', 'close', 'volume'])
            return df, 'jqdata'
        except Exception as e:
            logger.error(f"JQData获取数据失败: {e}")
            raise
    
    def _calculate_indicators(self, df: pd.DataFrame) -> MarketIndicators:
        """计算指标"""
        close = df['close']
        current = close.iloc[-1]
        
        # 动量
        def safe_mom(n):
            if len(close) > n:
                return (current / close.iloc[-n-1] - 1) * 100
            return 0.0
        
        mom_5d = safe_mom(5)
        mom_10d = safe_mom(10)
        mom_20d = safe_mom(20)
        mom_60d = safe_mom(60)
        mom_120d = safe_mom(120)
        
        # 均线
        def safe_ma(n):
            return close.rolling(n, min_periods=1).mean().iloc[-1]
        
        ma5 = safe_ma(5)
        ma10 = safe_ma(10)
        ma20 = safe_ma(20)
        ma60 = safe_ma(60)
        ma120 = safe_ma(120)
        ma250 = safe_ma(250)
        
        # 偏离度
        vs_ma5 = (current / ma5 - 1) * 100
        vs_ma10 = (current / ma10 - 1) * 100
        vs_ma20 = (current / ma20 - 1) * 100
        vs_ma60 = (current / ma60 - 1) * 100
        vs_ma120 = (current / ma120 - 1) * 100
        vs_ma250 = (current / ma250 - 1) * 100 if ma250 > 0 else 0
        
        # 位置
        def safe_pos(n):
            high_n = close.rolling(n, min_periods=1).max().iloc[-1]
            low_n = close.rolling(n, min_periods=1).min().iloc[-1]
            if high_n > low_n:
                return (current - low_n) / (high_n - low_n) * 100
            return 50.0
        
        pos_20d = safe_pos(20)
        pos_60d = safe_pos(60)
        pos_250d = safe_pos(250)
        
        # 均线排列
        ma_bull = ma5 > ma10 > ma20 > ma60
        ma_bear = ma5 < ma10 < ma20 < ma60
        
        # 波动率
        returns = close.pct_change().dropna()
        volatility_20d = returns.tail(20).std() * np.sqrt(252) * 100 if len(returns) >= 20 else 15
        
        # 动能变化
        momentum_weakening = mom_60d < mom_120d and mom_120d > 0
        momentum_recovering = mom_60d > mom_120d and mom_120d < 0
        
        return MarketIndicators(
            mom_5d=mom_5d,
            mom_10d=mom_10d,
            mom_20d=mom_20d,
            mom_60d=mom_60d,
            mom_120d=mom_120d,
            vs_ma5=vs_ma5,
            vs_ma10=vs_ma10,
            vs_ma20=vs_ma20,
            vs_ma60=vs_ma60,
            vs_ma120=vs_ma120,
            vs_ma250=vs_ma250,
            pos_20d=pos_20d,
            pos_60d=pos_60d,
            pos_250d=pos_250d,
            ma_bull=ma_bull,
            ma_bear=ma_bear,
            volatility_20d=volatility_20d,
            abs_mom_60d=abs(mom_60d),
            abs_mom_120d=abs(mom_120d),
            momentum_weakening=momentum_weakening,
            momentum_recovering=momentum_recovering
        )
    
    def _determine_state(self, ind: MarketIndicators) -> Tuple[MarketState, float, float]:
        """确定市场状态"""
        
        # 按优先级检查各状态
        # 强势牛市
        if ind.mom_120d > 15 and ind.vs_ma250 > 10 and ind.pos_250d > 80 and ind.ma_bull:
            return MarketState.BULL_STRONG, 90.0, 80.0
        
        # 正常牛市
        if ind.mom_120d > 10 and ind.vs_ma250 > 5 and ind.pos_250d > 60:
            conf = min(90, 60 + (ind.mom_120d - 10) * 2)
            return MarketState.BULL_NORMAL, conf, 60.0
        
        # 牛市后期
        if ind.mom_120d > 5 and ind.vs_ma250 > 0 and ind.pos_250d > 70 and ind.momentum_weakening:
            return MarketState.BULL_LATE, 70.0, 40.0
        
        # 牛市回调
        if ind.mom_120d > 5 and ind.vs_ma250 > 0 and ind.mom_20d < 0:
            return MarketState.BULL_PULLBACK, 75.0, 30.0
        
        # 强势熊市
        if ind.mom_120d < -15 and ind.vs_ma250 < -10 and ind.pos_250d < 20 and ind.ma_bear:
            return MarketState.BEAR_STRONG, 90.0, -80.0
        
        # 正常熊市
        if ind.mom_120d < -10 and ind.vs_ma250 < -5 and ind.pos_250d < 40:
            conf = min(90, 60 + abs(ind.mom_120d + 10) * 2)
            return MarketState.BEAR_NORMAL, conf, -60.0
        
        # 熊市后期
        if ind.mom_120d < -5 and ind.vs_ma250 < 0 and ind.pos_250d < 30 and ind.momentum_recovering:
            return MarketState.BEAR_LATE, 70.0, -40.0
        
        # 熊市反弹
        if ind.mom_120d < -5 and ind.vs_ma250 < 0 and ind.mom_20d > 0:
            return MarketState.BEAR_BOUNCE, 65.0, -30.0
        
        # 底部反转
        if ind.mom_120d < 0 and ind.mom_60d > 5 and ind.mom_20d > 3 and ind.pos_250d < 50:
            return MarketState.TURNING_UP, 70.0, 25.0
        
        # 顶部反转
        if ind.mom_120d > 0 and ind.mom_60d < -5 and ind.mom_20d < -3 and ind.pos_250d > 50:
            return MarketState.TURNING_DOWN, 70.0, -25.0
        
        # 高位震荡
        if ind.pos_250d > 70 and ind.abs_mom_60d < 8:
            return MarketState.RANGE_HIGH, 60.0, 10.0
        
        # 低位震荡
        if ind.pos_250d < 30 and ind.abs_mom_60d < 8:
            return MarketState.RANGE_LOW, 60.0, -10.0
        
        # 宽幅震荡
        if ind.abs_mom_120d < 10 and ind.abs_mom_60d > 8:
            return MarketState.RANGE_WIDE, 55.0, 0.0
        
        # 中位震荡
        if 30 <= ind.pos_250d <= 70 and ind.abs_mom_60d < 5:
            return MarketState.RANGE_MID, 50.0, 0.0
        
        # 默认：根据动量方向判断
        if ind.mom_60d > 0:
            return MarketState.BULL_NORMAL, 50.0, ind.mom_60d * 2
        elif ind.mom_60d < 0:
            return MarketState.BEAR_NORMAL, 50.0, ind.mom_60d * 2
        else:
            return MarketState.RANGE_MID, 40.0, 0.0
    
    def backtest(self, 
                 df: pd.DataFrame,
                 start_idx: int = 250) -> pd.DataFrame:
        """
        历史回测
        
        Args:
            df: 历史数据
            start_idx: 开始索引
            
        Returns:
            回测结果DataFrame
        """
        results = []
        
        for i in range(start_idx, len(df)):
            hist_df = df.iloc[:i+1].copy()
            
            try:
                indicators = self._calculate_indicators(hist_df)
                state, confidence, score = self._determine_state(indicators)
                
                # 计算未来收益（用于验证）
                future_5d = (df['close'].iloc[min(i+5, len(df)-1)] / df['close'].iloc[i] - 1) * 100 if i+5 < len(df) else None
                future_20d = (df['close'].iloc[min(i+20, len(df)-1)] / df['close'].iloc[i] - 1) * 100 if i+20 < len(df) else None
                
                results.append({
                    'date': df.index[i],
                    'close': df['close'].iloc[i],
                    'state': state.name,
                    'state_name': state.value,
                    'category': state.category,
                    'confidence': confidence,
                    'score': score,
                    'mom_120d': indicators.mom_120d,
                    'vs_ma250': indicators.vs_ma250,
                    'pos_250d': indicators.pos_250d,
                    'future_5d': future_5d,
                    'future_20d': future_20d
                })
            except:
                continue
        
        return pd.DataFrame(results)


# 便捷函数
def identify_market_state(symbol: str = '000001.XSHG', 
                          df: pd.DataFrame = None) -> MarketStateResult:
    """
    识别市场状态
    
    Args:
        symbol: 指数代码
        df: OHLCV数据（可选）
        
    Returns:
        MarketStateResult
    """
    identifier = MarketStateIdentifier(use_akshare=False)
    return identifier.identify(df=df, symbol=symbol)


def get_market_params(symbol: str = '000001.XSHG') -> Dict:
    """
    获取市场参数（供下游使用）
    """
    result = identify_market_state(symbol)
    return result.to_dict()


def get_all_states() -> List[Dict]:
    """获取所有状态定义"""
    return [
        {
            'state': state.name,
            'name': state.value,
            'category': state.category,
            'direction': state.direction,
            **STATE_DEFINITIONS.get(state, {})
        }
        for state in MarketState
    ]


def print_state_summary(result: MarketStateResult) -> str:
    """打印状态摘要"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"市场状态: {result.state.value} ({result.state.name})")
    lines.append("=" * 60)
    lines.append(f"类别: {result.state.category}")
    lines.append(f"方向: {'多' if result.state.direction > 0 else ('空' if result.state.direction < 0 else '中性')}")
    lines.append(f"置信度: {result.confidence:.1f}%")
    lines.append(f"得分: {result.score:+.1f}")
    lines.append(f"\n描述: {result.description}")
    lines.append(f"\n【建议参数】")
    lines.append(f"  仓位: {result.position_range[0]:.0%} - {result.position_range[1]:.0%}")
    lines.append(f"  风险: {result.risk_level}")
    lines.append(f"  策略: {result.strategy}")
    lines.append(f"\n【关键指标】")
    lines.append(f"  120日动量: {result.indicators.mom_120d:+.2f}%")
    lines.append(f"  年线偏离: {result.indicators.vs_ma250:+.2f}%")
    lines.append(f"  250日位置: {result.indicators.pos_250d:.1f}%")
    lines.append(f"\n数据源: {result.data_source}")
    lines.append(f"时间: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    return "\n".join(lines)

