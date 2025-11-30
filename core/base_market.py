# -*- coding: utf-8 -*-
"""
市场抽象基类
===========

定义市场的通用接口，支持A股、美股等多市场扩展。
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime


class MarketType(Enum):
    """市场类型"""
    ASHARE = "ashare"       # A股
    USSTOCK = "usstock"     # 美股
    HKSTOCK = "hkstock"     # 港股
    CRYPTO = "crypto"       # 加密货币


@dataclass
class MarketConfig:
    """市场配置"""
    market_type: MarketType
    name: str
    name_en: str
    timezone: str
    currency: str
    trading_hours: Dict[str, str]
    t_plus: int                    # T+N 交易
    has_limit: bool                # 是否有涨跌停
    limit_pct: float               # 涨跌停幅度
    
    # 数据源配置
    data_sources: List[str]
    primary_data_source: str
    
    # 交易接口配置
    brokers: List[str]
    primary_broker: str


# 预定义市场配置
MARKET_CONFIGS = {
    MarketType.ASHARE: MarketConfig(
        market_type=MarketType.ASHARE,
        name="A股",
        name_en="China A-Share",
        timezone="Asia/Shanghai",
        currency="CNY",
        trading_hours={"open": "09:30", "close": "15:00", "break": "11:30-13:00"},
        t_plus=1,
        has_limit=True,
        limit_pct=0.10,  # 10%涨跌停（主板）
        data_sources=["jqdata", "akshare", "tushare", "wind"],
        primary_data_source="jqdata",
        brokers=["ptrade", "qmt", "miniquant"],
        primary_broker="ptrade",
    ),
    MarketType.USSTOCK: MarketConfig(
        market_type=MarketType.USSTOCK,
        name="美股",
        name_en="US Stock",
        timezone="America/New_York",
        currency="USD",
        trading_hours={"open": "09:30", "close": "16:00", "premarket": "04:00", "afterhours": "20:00"},
        t_plus=0,
        has_limit=False,
        limit_pct=0,
        data_sources=["yfinance", "alpha_vantage", "polygon", "iex"],
        primary_data_source="yfinance",
        brokers=["ibkr", "alpaca", "td_ameritrade"],
        primary_broker="ibkr",
    ),
}


class BaseMarket(ABC):
    """
    市场抽象基类
    
    所有市场实现必须继承此类。
    """
    
    def __init__(self, market_type: MarketType):
        self.market_type = market_type
        self.config = MARKET_CONFIGS.get(market_type)
        if not self.config:
            raise ValueError(f"未知的市场类型: {market_type}")
    
    @property
    def name(self) -> str:
        return self.config.name
    
    @property
    def is_trading_day(self) -> bool:
        """当前是否为交易日"""
        return self._check_trading_day(datetime.now())
    
    @abstractmethod
    def _check_trading_day(self, date: datetime) -> bool:
        """检查指定日期是否为交易日"""
        pass
    
    @abstractmethod
    def get_sectors(self) -> List[Dict]:
        """获取板块列表"""
        pass
    
    @abstractmethod
    def get_sector_stocks(self, sector_code: str) -> List[str]:
        """获取板块成分股"""
        pass
    
    @abstractmethod
    def get_index_list(self) -> List[Dict]:
        """获取指数列表"""
        pass
    
    @abstractmethod
    def get_stock_info(self, symbol: str) -> Dict:
        """获取股票基本信息"""
        pass
    
    @abstractmethod
    def get_realtime_quote(self, symbols: List[str]) -> Dict:
        """获取实时行情"""
        pass
    
    @abstractmethod
    def get_historical_data(self, symbol: str, start_date: str, end_date: str, 
                           period: str = "1d") -> Any:
        """获取历史数据"""
        pass
    
    @abstractmethod
    def get_fund_flow(self, symbol: str = None, sector: str = None) -> Dict:
        """获取资金流向"""
        pass
    
    def format_symbol(self, symbol: str) -> str:
        """格式化股票代码为统一格式"""
        prefix = self.config.market_type.value.upper()[:2]
        return f"{prefix}.{symbol}"
    
    def parse_symbol(self, unified_symbol: str) -> str:
        """解析统一格式的股票代码"""
        parts = unified_symbol.split(".")
        if len(parts) >= 2:
            return ".".join(parts[1:])
        return unified_symbol


