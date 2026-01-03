# -*- coding: utf-8 -*-
"""
AllTick数据源
=============

AllTick API客户端，用于获取实时和历史行情数据
支持：Forex、US & HK Stocks、Crypto、Commodities

API文档: https://alltick.co/
"""

import logging
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from .base_source import BaseDataSource

logger = logging.getLogger(__name__)


class AllTickSource(BaseDataSource):
    """AllTick数据源"""
    
    def __init__(self, api_token: str = None):
        """
        初始化AllTick数据源
        
        Args:
            api_token: AllTick API Token
        """
        super().__init__(name="AllTick")
        self.api_token = api_token or "e194fd5add8cf29b303c858939d25b59-c-app"
        self.base_url = "https://quote.alltick.io/quote-b-api"
        self.connected = False
        
    def connect(self, **kwargs) -> bool:
        """连接AllTick API"""
        try:
            # 测试API连接
            test_url = f"{self.base_url}/kline"
            params = {
                "token": self.api_token,
                "query": '{"data":{"code":"BTCUSDT","kline_type":"8","kline_timestamp_end":"0","query_kline_num":"1","adjust_type":"0"}}'
            }
            response = requests.get(test_url, params=params, timeout=5)
            
            if response.status_code == 200:
                self.connected = True
                self._connected = True
                logger.info("✅ AllTick API连接成功")
                return True
            else:
                logger.warning(f"AllTick API连接失败: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"AllTick API连接异常: {e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        self.connected = False
        logger.info("AllTick API已断开")
    
    def is_connected(self) -> bool:
        """检查连接状态"""
        return self.connected or self._connected
    
    def _convert_symbol(self, symbol: str) -> str:
        """
        转换股票代码格式
        JQData格式 -> AllTick格式
        
        Examples:
            000001.XSHE -> 000001.SZ (深交所)
            600000.XSHG -> 600000.SH (上交所)
        """
        if '.' in symbol:
            code, exchange = symbol.split('.')
            if exchange == 'XSHE':
                return f"{code}.SZ"
            elif exchange == 'XSHG':
                return f"{code}.SH"
            else:
                return code
        return symbol
    
    def get_price(self, symbol: str, end_date: str = None, count: int = 1, 
                  frequency: str = 'daily') -> Optional[pd.DataFrame]:
        """
        获取K线数据
        
        Args:
            symbol: 股票代码（JQData格式或AllTick格式）
            end_date: 结束日期（格式：YYYY-MM-DD）
            count: 获取K线数量
            frequency: 频率 ('daily', '1m', '5m', '15m', '30m', '60m')
        
        Returns:
            DataFrame with columns: [open, high, low, close, volume]
        """
        if not self.connected:
            if not self.connect():
                return None
        
        try:
            # 转换代码格式
            alltick_symbol = self._convert_symbol(symbol)
            
            # 转换K线类型
            kline_type_map = {
                'daily': '8',      # 日线
                '1m': '1',         # 1分钟
                '5m': '5',         # 5分钟
                '15m': '15',       # 15分钟
                '30m': '30',       # 30分钟
                '60m': '60',       # 60分钟
            }
            kline_type = kline_type_map.get(frequency, '8')
            
            # 转换时间戳
            if end_date:
                end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
            else:
                end_timestamp = 0  # 0表示最新
            
            # 构建查询（根据AllTick API文档格式）
            import json
            query_data = {
                "data": {
                    "code": alltick_symbol,
                    "kline_type": kline_type,
                    "kline_timestamp_end": str(end_timestamp),
                    "query_kline_num": str(count),
                    "adjust_type": "0"  # 0=不复权, 1=前复权, 2=后复权
                }
            }
            
            # 发送请求（query参数需要是JSON字符串）
            url = f"{self.base_url}/kline"
            params = {
                "token": self.api_token,
                "query": json.dumps(query_data)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # 解析响应
            if 'data' in data and 'kline' in data['data']:
                klines = data['data']['kline']
                if not klines:
                    logger.warning(f"{symbol}: 未获取到K线数据")
                    return None
                
                # 转换为DataFrame
                records = []
                for k in klines:
                    records.append({
                        'date': datetime.fromtimestamp(int(k.get('timestamp', 0))),
                        'open': float(k.get('open', 0)),
                        'high': float(k.get('high', 0)),
                        'low': float(k.get('low', 0)),
                        'close': float(k.get('close', 0)),
                        'volume': float(k.get('volume', 0))
                    })
                
                df = pd.DataFrame(records)
                df.set_index('date', inplace=True)
                df.sort_index(inplace=True)
                
                return df
            else:
                logger.warning(f"{symbol}: API响应格式异常")
                return None
                
        except Exception as e:
            logger.error(f"{symbol}: 获取价格数据失败 - {e}")
            return None
    
    def get_latest_price(self, symbol: str) -> Optional[float]:
        """
        获取最新价格
        
        Args:
            symbol: 股票代码
        
        Returns:
            最新价格
        """
        df = self.get_price(symbol, count=1, frequency='daily')
        if df is not None and len(df) > 0:
            return float(df['close'].iloc[-1])
        return None
    
    def get_realtime_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        获取实时价格（最后价格）
        
        Args:
            symbol: 股票代码
        
        Returns:
            {'price': float, 'volume': float, 'timestamp': datetime}
        """
        try:
            alltick_symbol = self._convert_symbol(symbol)
            
            # 使用last_price接口
            url = f"{self.base_url}/last_price"
            params = {
                "token": self.api_token,
                "code": alltick_symbol
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and 'price' in data['data']:
                return {
                    'price': float(data['data']['price']),
                    'volume': float(data['data'].get('volume', 0)),
                    'timestamp': datetime.now()
                }
            else:
                # 降级到K线数据
                df = self.get_price(symbol, count=1)
                if df is not None and len(df) > 0:
                    return {
                        'price': float(df['close'].iloc[-1]),
                        'volume': float(df['volume'].iloc[-1]),
                        'timestamp': df.index[-1]
                    }
                return None
                
        except Exception as e:
            logger.error(f"{symbol}: 获取实时价格失败 - {e}")
            return None
    
    def get_historical_prices(self, symbol: str, start_date: str, 
                             end_date: str, frequency: str = 'daily') -> Optional[pd.DataFrame]:
        """
        获取历史价格数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            frequency: 频率
        
        Returns:
            DataFrame
        """
        # AllTick API需要按日期范围查询，这里简化处理
        # 实际使用时可能需要分批请求
        try:
            # 计算日期差
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            days = (end - start).days + 1
            
            # 限制最大查询天数（避免超时）
            max_days = 500
            if days > max_days:
                logger.warning(f"日期范围过大，限制为{max_days}天")
                days = max_days
            
            return self.get_price(symbol, end_date=end_date, count=days, frequency=frequency)
        except Exception as e:
            logger.error(f"{symbol}: 获取历史价格失败 - {e}")
            return None
    
    def get_multiple_prices(self, symbols: List[str], end_date: str = None) -> Dict[str, float]:
        """
        批量获取最新价格
        
        Args:
            symbols: 股票代码列表
            end_date: 结束日期
        
        Returns:
            {symbol: price} 字典
        """
        results = {}
        for symbol in symbols:
            price = self.get_latest_price(symbol)
            if price:
                results[symbol] = price
        return results


    def get_daily_data(self, symbol: str, start_date: str = None, end_date: str = None) -> Optional[pd.DataFrame]:
        """获取日线数据（BaseDataSource接口）"""
        if not start_date:
            start_date = "2020-01-01"
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        return self.get_historical_prices(symbol, start_date, end_date, frequency='daily')
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查（BaseDataSource接口）"""
        try:
            if self.connect():
                return {
                    "status": "healthy",
                    "connected": True,
                    "name": self.name
                }
            else:
                return {
                    "status": "unhealthy",
                    "connected": False,
                    "name": self.name,
                    "error": "连接失败"
                }
        except Exception as e:
            return {
                "status": "error",
                "connected": False,
                "name": self.name,
                "error": str(e)
            }
