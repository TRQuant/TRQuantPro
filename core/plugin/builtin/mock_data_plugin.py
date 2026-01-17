# -*- coding: utf-8 -*-
"""
模拟数据插件
===========

用于测试和演示，生成模拟行情数据
"""

import logging
import random
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import numpy as np

from core.plugin import DataPlugin, PluginInfo, PluginType

logger = logging.getLogger(__name__)


class MockDataPlugin(DataPlugin):
    """
    模拟数据插件
    
    生成随机行情数据，用于:
    - 测试回测系统
    - 策略开发演示
    - 无网络环境下使用
    """
    
    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="mock_data",
            type=PluginType.DATA,
            version="1.0.0",
            author="TRQuant",
            description="模拟数据源插件，生成随机行情数据",
            dependencies=[],
            config_schema={
                "seed": {"type": "integer", "default": 42},
                "volatility": {"type": "number", "default": 0.02},
                "trend": {"type": "number", "default": 0.0001},
            }
        )
    
    def __init__(self):
        super().__init__()
        self._seed = 42
        self._volatility = 0.02
        self._trend = 0.0001
        self._price_cache: Dict[str, float] = {}
    
    def initialize(self) -> bool:
        """初始化"""
        self._seed = self._config.get("seed", 42)
        self._volatility = self._config.get("volatility", 0.02)
        self._trend = self._config.get("trend", 0.0001)
        random.seed(self._seed)
        np.random.seed(self._seed)
        logger.info(f"模拟数据插件初始化: seed={self._seed}, vol={self._volatility}")
        return True
    
    def start(self) -> bool:
        return True
    
    def stop(self) -> bool:
        return True
    
    def get_bars(self, symbol: str, start_date: str, end_date: str,
                 frequency: str = "day") -> List[Dict]:
        """
        生成模拟K线数据
        """
        # 解析日期
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        # 生成基础价格
        base_price = self._get_base_price(symbol)
        
        bars = []
        current = start
        price = base_price
        
        while current <= end:
            # 跳过周末
            if current.weekday() < 5:
                # 生成OHLC
                returns = np.random.normal(self._trend, self._volatility)
                price = price * (1 + returns)
                
                high = price * (1 + abs(np.random.normal(0, self._volatility * 0.5)))
                low = price * (1 - abs(np.random.normal(0, self._volatility * 0.5)))
                open_price = low + (high - low) * random.random()
                close_price = low + (high - low) * random.random()
                
                # 确保OHLC关系正确
                high = max(high, open_price, close_price)
                low = min(low, open_price, close_price)
                
                volume = random.randint(1000000, 10000000)
                amount = volume * price
                
                bars.append({
                    "symbol": symbol,
                    "datetime": current.strftime("%Y-%m-%d"),
                    "open": round(open_price, 2),
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "close": round(close_price, 2),
                    "volume": volume,
                    "amount": round(amount, 2),
                })
                
                price = close_price
            
            current += timedelta(days=1)
        
        # 缓存最新价格
        self._price_cache[symbol] = price
        
        return bars
    
    def get_tick(self, symbol: str) -> Optional[Dict]:
        """获取模拟实时行情"""
        base_price = self._price_cache.get(symbol, self._get_base_price(symbol))
        
        # 随机波动
        price = base_price * (1 + np.random.normal(0, 0.001))
        
        return {
            "symbol": symbol,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_price": round(price, 2),
            "open": round(price * 0.99, 2),
            "high": round(price * 1.01, 2),
            "low": round(price * 0.98, 2),
            "volume": random.randint(100000, 1000000),
            "amount": round(price * random.randint(100000, 1000000), 2),
            "bid_price": round(price * 0.999, 2),
            "ask_price": round(price * 1.001, 2),
        }
    
    def get_symbols(self, market: str = "") -> List[str]:
        """获取模拟股票列表"""
        # 生成一些模拟股票代码
        symbols = []
        
        if market.upper() != "SZ":
            # 上海
            for i in range(1, 51):
                symbols.append(f"60{str(i).zfill(4)}.SH")
        
        if market.upper() != "SH":
            # 深圳
            for i in range(1, 51):
                symbols.append(f"00{str(i).zfill(4)}.SZ")
        
        return symbols
    
    def _get_base_price(self, symbol: str) -> float:
        """根据股票代码生成基础价格"""
        # 使用代码hash生成确定性的基础价格
        code_num = sum(ord(c) for c in symbol)
        base = 10 + (code_num % 90)  # 10-100之间
        return float(base)

