# -*- coding: utf-8 -*-
"""
动量策略插件
===========

经典动量策略实现
"""

import logging
from typing import Dict, List, Any, Optional
from collections import deque

from core.plugin import StrategyPlugin, PluginInfo, PluginType

logger = logging.getLogger(__name__)


class MomentumStrategyPlugin(StrategyPlugin):
    """
    动量策略插件
    
    策略逻辑:
    - 计算N日动量
    - 动量为正且大于阈值时买入
    - 动量转负或低于阈值时卖出
    """
    
    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="momentum_strategy",
            type=PluginType.STRATEGY,
            version="1.0.0",
            author="TRQuant",
            description="经典动量策略，基于N日收益率进行交易",
            dependencies=[],
            config_schema={
                "lookback_period": {"type": "integer", "default": 20},
                "momentum_threshold": {"type": "number", "default": 0.05},
                "max_positions": {"type": "integer", "default": 10},
                "position_size": {"type": "number", "default": 0.1},
            }
        )
    
    def __init__(self):
        super().__init__()
        self._lookback = 20
        self._threshold = 0.05
        self._max_positions = 10
        self._position_size = 0.1
        
        # 价格历史
        self._price_history: Dict[str, deque] = {}
        
        # 当前持仓
        self._positions: Dict[str, float] = {}
    
    def initialize(self) -> bool:
        """初始化策略参数"""
        self._lookback = self._config.get("lookback_period", 20)
        self._threshold = self._config.get("momentum_threshold", 0.05)
        self._max_positions = self._config.get("max_positions", 10)
        self._position_size = self._config.get("position_size", 0.1)
        
        logger.info(f"动量策略初始化: lookback={self._lookback}, threshold={self._threshold}")
        return True
    
    def start(self) -> bool:
        return True
    
    def stop(self) -> bool:
        return True
    
    def on_bar(self, bar: Dict) -> List[Dict]:
        """
        处理K线数据
        
        Args:
            bar: K线数据 {"symbol", "close", "volume", ...}
            
        Returns:
            交易信号列表
        """
        symbol = bar.get("symbol", "")
        close = bar.get("close", 0)
        
        if not symbol or close <= 0:
            return []
        
        # 更新价格历史
        if symbol not in self._price_history:
            self._price_history[symbol] = deque(maxlen=self._lookback + 1)
        
        self._price_history[symbol].append(close)
        
        # 数据不足
        if len(self._price_history[symbol]) < self._lookback:
            return []
        
        # 计算动量
        prices = list(self._price_history[symbol])
        momentum = (prices[-1] / prices[0]) - 1
        
        signals = []
        
        # 生成信号
        if symbol in self._positions:
            # 已持仓：检查是否卖出
            if momentum < 0 or momentum < self._threshold * 0.5:
                signals.append({
                    "symbol": symbol,
                    "action": "sell",
                    "volume": self._positions[symbol],
                    "reason": f"动量={momentum:.2%}, 低于阈值",
                })
                del self._positions[symbol]
        else:
            # 未持仓：检查是否买入
            if len(self._positions) < self._max_positions and momentum > self._threshold:
                signals.append({
                    "symbol": symbol,
                    "action": "buy",
                    "volume": 100,  # 简化：固定100股
                    "reason": f"动量={momentum:.2%}, 高于阈值",
                })
                self._positions[symbol] = 100
        
        return signals
    
    def on_trade(self, trade: Dict):
        """处理成交回报"""
        symbol = trade.get("symbol", "")
        direction = trade.get("direction", "")
        volume = trade.get("volume", 0)
        
        if direction == "buy":
            self._positions[symbol] = self._positions.get(symbol, 0) + volume
        elif direction == "sell":
            if symbol in self._positions:
                self._positions[symbol] -= volume
                if self._positions[symbol] <= 0:
                    del self._positions[symbol]
    
    def get_momentum(self, symbol: str) -> Optional[float]:
        """获取当前动量值"""
        if symbol not in self._price_history:
            return None
        
        prices = list(self._price_history[symbol])
        if len(prices) < 2:
            return None
        
        return (prices[-1] / prices[0]) - 1
    
    @property
    def positions(self) -> Dict[str, float]:
        """获取当前持仓"""
        return self._positions.copy()

