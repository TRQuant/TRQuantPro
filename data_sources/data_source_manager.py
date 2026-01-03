# -*- coding: utf-8 -*-
"""
数据源管理器
============

统一管理多个数据源，支持：
- 自动故障切换
- 数据源优先级
- 本地缓存
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import logging

from .base_source import BaseDataSource
from .cache_manager import MongoDBCache
from .jqdata_source import JQDataSource
from .akshare_source import AKShareSource

logger = logging.getLogger(__name__)


class DataSourceManager:
    """数据源管理器"""
    
    def __init__(self, use_cache: bool = True, 
                 mongo_uri: str = "mongodb://localhost:27017"):
        """
        初始化数据源管理器
        
        Args:
            use_cache: 是否使用缓存
            mongo_uri: MongoDB连接URI
        """
        self.use_cache = use_cache
        
        # 初始化缓存
        if use_cache:
            self.cache = MongoDBCache(uri=mongo_uri)
        else:
            self.cache = None
        
        # 初始化数据源
        self.sources: Dict[str, BaseDataSource] = {
            'jqdata': JQDataSource(),
            'akshare': AKShareSource(),
        }
        
        # 数据源优先级配置
        self.priority = {
            'daily': ['jqdata', 'akshare'],      # 日线数据优先级
            'minute': ['jqdata', 'akshare'],     # 分钟数据优先级
            'realtime': ['akshare', 'jqdata'],   # 实时数据优先级（AKShare无限制）
            'fundamental': ['jqdata'],            # 财务数据优先级
            'etf': ['akshare', 'jqdata'],        # ETF数据优先级
            'news': ['akshare'],                  # 新闻数据优先级
        }
        
        # 连接状态
        self._connected_sources = set()
    
    def connect_all(self) -> Dict[str, bool]:
        """连接所有数据源"""
        results = {}
        for name, source in self.sources.items():
            try:
                success = source.connect()
                results[name] = success
                if success:
                    self._connected_sources.add(name)
            except Exception as e:
                results[name] = False
                logger.error(f"连接{name}失败: {e}")
        
        return results
    
    def connect_source(self, name: str) -> bool:
        """连接指定数据源"""
        if name not in self.sources:
            return False
        
        try:
            success = self.sources[name].connect()
            if success:
                self._connected_sources.add(name)
            return success
        except Exception as e:
            logger.error(f"连接{name}失败: {e}")
            return False
    
    def disconnect_all(self):
        """断开所有数据源"""
        for source in self.sources.values():
            source.disconnect()
        self._connected_sources.clear()
    
    def get_status(self) -> Dict:
        """获取所有数据源状态"""
        status = {
            "sources": {},
            "cache": None,
            "connected_count": len(self._connected_sources)
        }
        
        for name, source in self.sources.items():
            health = source.health_check()
            status["sources"][name] = {
                "connected": source.is_connected,
                "health": health,
                "last_error": source.last_error
            }
            
            # 保存状态到缓存
            if self.cache:
                self.cache.save_source_status(name, health)
        
        # 缓存状态
        if self.cache:
            status["cache"] = self.cache.get_status()
        
        return status
    
    def _get_source(self, data_type: str) -> Optional[BaseDataSource]:
        """根据数据类型获取可用的数据源"""
        priority_list = self.priority.get(data_type, list(self.sources.keys()))
        
        for source_name in priority_list:
            if source_name in self._connected_sources:
                source = self.sources[source_name]
                if source.is_connected:
                    return source
        
        return None
    
    # ============================================================
    # 行情数据
    # ============================================================
    def get_daily_data(self, symbol: str, start_date: str, 
                       end_date: str, use_cache: bool = True) -> pd.DataFrame:
        """
        获取日线数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            use_cache: 是否使用缓存
            
        Returns:
            日线数据DataFrame
        """
        # 1. 尝试从缓存获取
        if use_cache and self.cache:
            cached = self.cache.get_market_data(symbol, start_date, end_date, "1d")
            if not cached.empty:
                # 检查是否需要更新
                cache_info = self.cache.get_cache_info(symbol, "1d")
                if cache_info['latest'] and cache_info['latest'] >= end_date:
                    logger.info(f"从缓存获取{symbol}日线数据")
                    return cached
        
        # 2. 从数据源获取
        for source_name in self.priority['daily']:
            if source_name not in self._connected_sources:
                continue
            
            source = self.sources[source_name]
            try:
                df = source.get_daily_data(symbol, start_date, end_date)
                if not df.empty:
                    # 保存到缓存
                    if self.cache:
                        self.cache.save_market_data(symbol, df, "1d", source_name)
                    
                    logger.info(f"从{source_name}获取{symbol}日线数据: {len(df)}条")
                    return df
            except Exception as e:
                logger.warning(f"{source_name}获取数据失败: {e}")
                continue
        
        logger.warning(f"无法获取{symbol}的日线数据")
        return pd.DataFrame()
    
    def get_minute_data(self, symbol: str, count: int = 240, 
                        period: str = "1m") -> pd.DataFrame:
        """获取分钟数据"""
        for source_name in self.priority['minute']:
            if source_name not in self._connected_sources:
                continue
            
            source = self.sources[source_name]
            try:
                df = source.get_minute_data(symbol, count, period)
                if not df.empty:
                    logger.info(f"从{source_name}获取{symbol}分钟数据: {len(df)}条")
                    return df
            except Exception as e:
                logger.warning(f"{source_name}获取分钟数据失败: {e}")
                continue
        
        return pd.DataFrame()
    
    # ============================================================
    # 基本面数据
    # ============================================================
    def get_stock_list(self, market: str = "A") -> pd.DataFrame:
        """获取股票列表"""
        source = self._get_source('daily')
        if source:
            return source.get_stock_list(market)
        return pd.DataFrame()
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        """获取指数成分股"""
        source = self._get_source('daily')
        if source:
            return source.get_index_stocks(index_code)
        return []
    
    def get_fundamentals(self, symbol: str) -> Dict:
        """获取财务数据"""
        # 先尝试缓存
        if self.cache:
            cached = self.cache.get_fundamental_data(symbol)
            if cached:
                return cached.get('data', {})
        
        # 从数据源获取
        source = self._get_source('fundamental')
        if source:
            data = source.get_fundamentals(symbol)
            if data and self.cache:
                self.cache.save_fundamental_data(
                    symbol, data, 
                    datetime.now().strftime('%Y-%m-%d')
                )
            return data
        
        return {}
    
    # ============================================================
    # ETF数据
    # ============================================================
    def get_etf_list(self) -> pd.DataFrame:
        """获取ETF列表"""
        source = self._get_source('etf')
        if source:
            return source.get_etf_list()
        return pd.DataFrame()
    
    def get_etf_realtime(self, symbols: List[str] = None) -> pd.DataFrame:
        """获取ETF实时行情"""
        source = self._get_source('etf')
        if source and hasattr(source, 'get_etf_realtime'):
            return source.get_etf_realtime(symbols)
        return pd.DataFrame()
    
    # ============================================================
    # 资讯数据
    # ============================================================
    def get_news(self, limit: int = 50) -> List[Dict]:
        """获取财经新闻"""
        source = self._get_source('news')
        if source and hasattr(source, 'get_news'):
            news = source.get_news(limit)
            
            # 保存到缓存
            if news and self.cache:
                self.cache.save_news(news)
            
            return news
        return []
    
    def get_stock_news(self, symbol: str, limit: int = 20) -> List[Dict]:
        """获取个股新闻"""
        source = self._get_source('news')
        if source and hasattr(source, 'get_stock_news'):
            return source.get_stock_news(symbol, limit)
        return []
    
    # ============================================================
    # 投资主线
    # ============================================================
    def get_hot_themes(self, limit: int = 10) -> List[Dict]:
        """获取热门投资主线"""
        if self.cache:
            return self.cache.get_hot_themes(limit)
        return []
    
    def save_theme(self, theme: Dict):
        """保存投资主线"""
        if self.cache:
            self.cache.save_theme(theme)
    
    # ============================================================
    # 观察池
    # ============================================================
    def get_watchlists(self) -> List[Dict]:
        """获取所有观察池"""
        if self.cache:
            return self.cache.get_watchlists()
        return []
    
    def save_watchlist(self, name: str, symbols: List[str], 
                       notes: str = "", theme_name: str = None):
        """保存观察池"""
        if self.cache:
            self.cache.save_watchlist(name, symbols, notes, theme_name)
    
    def delete_watchlist(self, name: str):
        """删除观察池"""
        if self.cache:
            self.cache.delete_watchlist(name)
    
    # ============================================================
    # 缓存管理
    # ============================================================
    def get_cache_status(self) -> Dict:
        """获取缓存状态"""
        if self.cache:
            return self.cache.get_status()
        return {"status": "disabled"}
    
    def clear_old_cache(self, days: int = 365):
        """清理旧缓存"""
        if self.cache:
            return self.cache.clear_old_data(days)
        return {}





