# -*- coding: utf-8 -*-
"""
AKShare数据源
=============

开源免费数据源，作为备用数据源。
"""

from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import logging
import time

from .base_source import BaseDataSource

logger = logging.getLogger(__name__)


class AKShareSource(BaseDataSource):
    """AKShare数据源"""
    
    def __init__(self):
        super().__init__("AKShare")
        self._ak = None
    
    def connect(self) -> bool:
        """连接AKShare（实际上是导入模块）"""
        try:
            import akshare as ak
            self._ak = ak
            self._connected = True
            self._log_info("AKShare加载成功")
            return True
        except ImportError:
            self._log_error("akshare未安装，请运行: pip install akshare")
            return False
        except Exception as e:
            self._log_error(f"加载失败: {e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        self._ak = None
        self._connected = False
    
    def health_check(self) -> Dict:
        """健康检查"""
        if not self._connected:
            return {"status": "disconnected", "error": "未加载"}
        
        try:
            start = time.time()
            # 简单测试：获取上证指数
            self._ak.stock_zh_index_spot_em()
            latency = int((time.time() - start) * 1000)
            
            return {
                "status": "ok",
                "latency": latency,
                "quota": {"spare": "unlimited", "total": "unlimited"}
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_daily_data(self, symbol: str, start_date: str, 
                       end_date: str) -> pd.DataFrame:
        """获取日线数据"""
        if not self._connected:
            self._log_error("AKShare未加载")
            return pd.DataFrame()
        
        try:
            # 转换股票代码格式
            # JQData格式: 000001.XSHE -> AKShare格式: 000001
            code = symbol.split('.')[0]
            
            # 使用东方财富接口
            df = self._ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=start_date.replace('-', ''),
                end_date=end_date.replace('-', ''),
                adjust="qfq"  # 前复权
            )
            
            if df is not None and not df.empty:
                # 重命名列
                df = df.rename(columns={
                    '日期': 'date',
                    '开盘': 'open',
                    '最高': 'high',
                    '最低': 'low',
                    '收盘': 'close',
                    '成交量': 'volume',
                    '成交额': 'amount'
                })
                
                # 选择需要的列
                cols = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount']
                df = df[[c for c in cols if c in df.columns]]
                
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            self._log_error(f"获取日线数据失败: {e}")
            return pd.DataFrame()
    
    def get_minute_data(self, symbol: str, count: int = 240, 
                        period: str = "1m") -> pd.DataFrame:
        """获取分钟数据"""
        if not self._connected:
            return pd.DataFrame()
        
        try:
            code = symbol.split('.')[0]
            
            # AKShare分钟数据接口
            # 注意：AKShare的分钟数据可能有限制
            df = self._ak.stock_zh_a_minute(
                symbol=code,
                period=period.replace('m', ''),
                adjust="qfq"
            )
            
            if df is not None and not df.empty:
                df = df.tail(count)  # 取最近的count条
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
            df = self._ak.stock_zh_a_spot_em()
            
            if df is not None and not df.empty:
                df = df.rename(columns={
                    '代码': 'symbol',
                    '名称': 'name'
                })
                return df[['symbol', 'name']]
            
            return pd.DataFrame()
            
        except Exception as e:
            self._log_error(f"获取股票列表失败: {e}")
            return pd.DataFrame()
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        """获取指数成分股"""
        if not self._connected:
            return []
        
        try:
            # 指数代码映射
            index_map = {
                '000300.XSHG': '000300',  # 沪深300
                '000905.XSHG': '000905',  # 中证500
                '000852.XSHG': '000852',  # 中证1000
                '399006.XSHE': '399006',  # 创业板指
            }
            
            code = index_map.get(index_code, index_code.split('.')[0])
            
            df = self._ak.index_stock_cons(symbol=code)
            
            if df is not None and not df.empty:
                return df['品种代码'].tolist()
            
            return []
            
        except Exception as e:
            self._log_error(f"获取指数成分股失败: {e}")
            return []
    
    def get_etf_list(self) -> pd.DataFrame:
        """获取ETF列表"""
        if not self._connected:
            return pd.DataFrame()
        
        try:
            df = self._ak.fund_etf_category_sina(symbol="ETF基金")
            
            if df is not None and not df.empty:
                df = df.rename(columns={
                    '代码': 'symbol',
                    '名称': 'name',
                    '最新价': 'price',
                    '涨跌幅': 'change_pct'
                })
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            self._log_error(f"获取ETF列表失败: {e}")
            return pd.DataFrame()
    
    def get_etf_realtime(self, symbols: List[str] = None) -> pd.DataFrame:
        """获取ETF实时行情"""
        if not self._connected:
            return pd.DataFrame()
        
        try:
            df = self._ak.fund_etf_category_sina(symbol="ETF基金")
            
            if df is not None and not df.empty:
                if symbols:
                    # 过滤指定的ETF
                    df = df[df['代码'].isin(symbols)]
                
                df = df.rename(columns={
                    '代码': 'symbol',
                    '名称': 'name',
                    '最新价': 'price',
                    '涨跌额': 'change',
                    '涨跌幅': 'change_pct',
                    '买入': 'bid',
                    '卖出': 'ask',
                    '昨收': 'pre_close',
                    '今开': 'open',
                    '最高': 'high',
                    '最低': 'low',
                    '成交量': 'volume',
                    '成交额': 'amount'
                })
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            self._log_error(f"获取ETF实时行情失败: {e}")
            return pd.DataFrame()
    
    def get_etf_history(self, symbol: str, start_date: str = None, 
                        end_date: str = None) -> pd.DataFrame:
        """获取ETF历史数据"""
        if not self._connected:
            return pd.DataFrame()
        
        try:
            # 转换代码格式 sz159995 -> 159995
            code = symbol.replace('sz', '').replace('sh', '').split('.')[0]
            
            df = self._ak.fund_etf_hist_sina(symbol=code)
            
            if df is not None and not df.empty:
                df = df.rename(columns={
                    'date': 'date',
                    'open': 'open',
                    'high': 'high',
                    'low': 'low',
                    'close': 'close',
                    'volume': 'volume'
                })
                
                # 日期过滤
                if start_date:
                    df = df[df['date'] >= start_date]
                if end_date:
                    df = df[df['date'] <= end_date]
                
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            self._log_error(f"获取ETF历史数据失败: {e}")
            return pd.DataFrame()
    
    # ============================================================
    # 资讯数据
    # ============================================================
    def get_news(self, limit: int = 50) -> List[Dict]:
        """获取财经新闻"""
        if not self._connected:
            return []
        
        try:
            # 东方财富快讯
            df = self._ak.stock_news_em(symbol="")
            
            if df is not None and not df.empty:
                news_list = []
                for _, row in df.head(limit).iterrows():
                    news_list.append({
                        'title': row.get('新闻标题', ''),
                        'content': row.get('新闻内容', ''),
                        'source': '东方财富',
                        'publish_time': row.get('发布时间', ''),
                        'url': row.get('新闻链接', '')
                    })
                return news_list
            
            return []
            
        except Exception as e:
            self._log_error(f"获取新闻失败: {e}")
            return []
    
    def get_stock_news(self, symbol: str, limit: int = 20) -> List[Dict]:
        """获取个股新闻"""
        if not self._connected:
            return []
        
        try:
            code = symbol.split('.')[0]
            df = self._ak.stock_news_em(symbol=code)
            
            if df is not None and not df.empty:
                news_list = []
                for _, row in df.head(limit).iterrows():
                    news_list.append({
                        'title': row.get('新闻标题', ''),
                        'content': row.get('新闻内容', ''),
                        'source': '东方财富',
                        'publish_time': row.get('发布时间', ''),
                        'symbol': symbol
                    })
                return news_list
            
            return []
            
        except Exception as e:
            self._log_error(f"获取个股新闻失败: {e}")
            return []





