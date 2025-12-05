# -*- coding: utf-8 -*-
"""
JQData数据源
============

聚宽数据源，提供A股行情、财务等数据。
"""

from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import logging
import time

from .base_source import BaseDataSource

logger = logging.getLogger(__name__)


class JQDataSource(BaseDataSource):
    """JQData数据源"""
    
    def __init__(self):
        super().__init__("JQData")
        self._jq = None
    
    def connect(self) -> bool:
        """连接JQData"""
        try:
            import jqdatasdk as jq
            
            # 尝试从配置文件读取账号
            from pathlib import Path
            import json
            
            config_path = Path.home() / ".local/share/trquant/config/jqdata_config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    username = config.get('username')
                    password = config.get('password')
                    
                    if username and password:
                        jq.auth(username, password)
                        self._jq = jq
                        self._connected = True
                        self._log_info("连接成功")
                        return True
            
            self._log_error("未找到JQData配置或配置无效")
            return False
            
        except ImportError:
            self._log_error("jqdatasdk未安装")
            return False
        except Exception as e:
            self._log_error(f"连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self._jq:
            try:
                self._jq.logout()
            except:
                pass
        self._connected = False
        self._jq = None
    
    def health_check(self) -> Dict:
        """健康检查"""
        if not self._connected:
            return {"status": "disconnected", "error": "未连接"}
        
        try:
            start = time.time()
            # 简单查询测试
            self._jq.get_price('000001.XSHE', count=1, fields=['close'])
            latency = int((time.time() - start) * 1000)
            
            # 获取配额信息
            query_count = self._jq.get_query_count()
            
            return {
                "status": "ok",
                "latency": latency,
                "quota": {
                    "spare": query_count.get('spare', 0),
                    "total": query_count.get('total', 0)
                }
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_daily_data(self, symbol: str, start_date: str, 
                       end_date: str) -> pd.DataFrame:
        """获取日线数据"""
        if not self._connected:
            self._log_error("未连接JQData")
            return pd.DataFrame()
        
        try:
            df = self._jq.get_price(
                symbol,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume', 'money'],
                skip_paused=False,
                fq='pre'  # 前复权
            )
            
            if df is not None and not df.empty:
                df = df.reset_index()
                df = df.rename(columns={'index': 'date', 'money': 'amount'})
                df['date'] = df['date'].dt.strftime('%Y-%m-%d')
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            self._log_error(f"获取日线数据失败: {e}")
            return pd.DataFrame()
    
    def get_minute_data(self, symbol: str, count: int = 240, 
                        period: str = "1m") -> pd.DataFrame:
        """获取分钟数据"""
        if not self._connected:
            self._log_error("未连接JQData")
            return pd.DataFrame()
        
        try:
            # JQData的分钟周期格式
            freq_map = {
                "1m": "1m",
                "5m": "5m",
                "15m": "15m",
                "30m": "30m",
                "60m": "60m",
            }
            freq = freq_map.get(period, "1m")
            
            df = self._jq.get_price(
                symbol,
                count=count,
                frequency=freq,
                fields=['open', 'high', 'low', 'close', 'volume', 'money'],
                skip_paused=False,
                fq='pre'
            )
            
            if df is not None and not df.empty:
                df = df.reset_index()
                df = df.rename(columns={'index': 'datetime', 'money': 'amount'})
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            self._log_error(f"获取分钟数据失败: {e}")
            return pd.DataFrame()
    
    def get_stock_list(self, market: str = "A") -> pd.DataFrame:
        """获取股票列表"""
        if not self._connected:
            return pd.DataFrame()
        
        try:
            stocks = self._jq.get_all_securities(types=['stock'])
            stocks = stocks.reset_index()
            stocks = stocks.rename(columns={'index': 'symbol'})
            return stocks
        except Exception as e:
            self._log_error(f"获取股票列表失败: {e}")
            return pd.DataFrame()
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        """获取指数成分股"""
        if not self._connected:
            return []
        
        try:
            stocks = self._jq.get_index_stocks(index_code)
            return stocks
        except Exception as e:
            self._log_error(f"获取指数成分股失败: {e}")
            return []
    
    def get_fundamentals(self, symbol: str, 
                         report_type: str = "quarterly") -> Dict:
        """获取财务数据"""
        if not self._connected:
            return {}
        
        try:
            from jqdatasdk import query, valuation, indicator, balance
            
            q = query(
                valuation.code,
                valuation.market_cap,
                valuation.pe_ratio,
                valuation.pb_ratio,
                indicator.roe,
                indicator.roa,
                indicator.gross_profit_margin,
            ).filter(valuation.code == symbol)
            
            df = self._jq.get_fundamentals(q)
            
            if df is not None and not df.empty:
                return df.iloc[0].to_dict()
            
            return {}
            
        except Exception as e:
            self._log_error(f"获取财务数据失败: {e}")
            return {}
    
    def get_etf_list(self) -> pd.DataFrame:
        """获取ETF列表"""
        if not self._connected:
            return pd.DataFrame()
        
        try:
            etfs = self._jq.get_all_securities(types=['etf'])
            etfs = etfs.reset_index()
            etfs = etfs.rename(columns={'index': 'symbol'})
            return etfs
        except Exception as e:
            self._log_error(f"获取ETF列表失败: {e}")
            return pd.DataFrame()





