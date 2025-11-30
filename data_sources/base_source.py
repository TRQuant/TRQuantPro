# -*- coding: utf-8 -*-
"""
数据源基类
=========

定义数据源的统一接口。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from datetime import datetime
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class BaseDataSource(ABC):
    """数据源基类"""
    
    def __init__(self, name: str):
        """
        初始化数据源
        
        Args:
            name: 数据源名称
        """
        self.name = name
        self._connected = False
        self._last_error = None
    
    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self._connected
    
    @property
    def last_error(self) -> Optional[str]:
        """最后一次错误信息"""
        return self._last_error
    
    @abstractmethod
    def connect(self) -> bool:
        """
        连接数据源
        
        Returns:
            是否连接成功
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """断开连接"""
        pass
    
    @abstractmethod
    def health_check(self) -> Dict:
        """
        健康检查
        
        Returns:
            {"status": "ok/error", "latency": ms, "error": "..."}
        """
        pass
    
    # ============================================================
    # 行情数据接口
    # ============================================================
    @abstractmethod
    def get_daily_data(self, symbol: str, start_date: str, 
                       end_date: str) -> pd.DataFrame:
        """
        获取日线数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            DataFrame with columns: date, open, high, low, close, volume, amount
        """
        pass
    
    def get_minute_data(self, symbol: str, count: int = 240, 
                        period: str = "1m") -> pd.DataFrame:
        """
        获取分钟数据
        
        Args:
            symbol: 股票代码
            count: 数据条数
            period: 周期 (1m, 5m, 15m, 30m, 60m)
            
        Returns:
            DataFrame
        """
        raise NotImplementedError(f"{self.name}不支持分钟数据")
    
    def get_realtime_quote(self, symbols: List[str]) -> Dict:
        """
        获取实时行情
        
        Args:
            symbols: 股票代码列表
            
        Returns:
            {symbol: {price, change, volume, ...}}
        """
        raise NotImplementedError(f"{self.name}不支持实时行情")
    
    # ============================================================
    # 基本面数据接口
    # ============================================================
    def get_stock_list(self, market: str = "A") -> pd.DataFrame:
        """
        获取股票列表
        
        Args:
            market: 市场 (A, HK, US)
            
        Returns:
            DataFrame with columns: symbol, name, industry, ...
        """
        raise NotImplementedError(f"{self.name}不支持股票列表")
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        """
        获取指数成分股
        
        Args:
            index_code: 指数代码
            
        Returns:
            股票代码列表
        """
        raise NotImplementedError(f"{self.name}不支持指数成分股")
    
    def get_fundamentals(self, symbol: str, 
                         report_type: str = "quarterly") -> Dict:
        """
        获取财务数据
        
        Args:
            symbol: 股票代码
            report_type: 报告类型 (quarterly, annual)
            
        Returns:
            财务数据字典
        """
        raise NotImplementedError(f"{self.name}不支持财务数据")
    
    # ============================================================
    # ETF数据接口
    # ============================================================
    def get_etf_list(self) -> pd.DataFrame:
        """
        获取ETF列表
        
        Returns:
            DataFrame with columns: symbol, name, ...
        """
        raise NotImplementedError(f"{self.name}不支持ETF列表")
    
    def get_etf_realtime(self, symbols: List[str] = None) -> pd.DataFrame:
        """
        获取ETF实时行情
        
        Args:
            symbols: ETF代码列表，None表示全部
            
        Returns:
            DataFrame
        """
        raise NotImplementedError(f"{self.name}不支持ETF实时行情")
    
    # ============================================================
    # 辅助方法
    # ============================================================
    def _log_error(self, error: str):
        """记录错误"""
        self._last_error = error
        logger.error(f"[{self.name}] {error}")
    
    def _log_info(self, msg: str):
        """记录信息"""
        logger.info(f"[{self.name}] {msg}")





