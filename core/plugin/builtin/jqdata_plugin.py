# -*- coding: utf-8 -*-
"""
聚宽数据源插件
=============

使用JQData获取A股行情数据
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime

from core.plugin import DataPlugin, PluginInfo, PluginType

logger = logging.getLogger(__name__)

# 尝试导入jqdata
JQDATA_AVAILABLE = False
try:
    import jqdatasdk as jq
    JQDATA_AVAILABLE = True
except ImportError:
    logger.warning("jqdatasdk未安装")


class JQDataPlugin(DataPlugin):
    """
    聚宽数据源插件
    
    支持:
    - 历史K线数据
    - 实时行情
    - 财务数据
    - 指数成分股
    """
    
    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="jqdata",
            type=PluginType.DATA,
            version="1.0.0",
            author="TRQuant",
            description="聚宽数据源插件，提供A股行情和财务数据",
            dependencies=[],
            config_schema={
                "username": {"type": "string", "required": True},
                "password": {"type": "string", "required": True},
            }
        )
    
    def __init__(self):
        super().__init__()
        self._authenticated = False
        self._subscriptions: Dict[str, List[Callable]] = {}
    
    def initialize(self) -> bool:
        """初始化并登录"""
        if not JQDATA_AVAILABLE:
            logger.error("jqdatasdk未安装，无法初始化")
            return False
        
        username = self._config.get("username", "")
        password = self._config.get("password", "")
        
        if not username or not password:
            logger.error("未配置聚宽账号")
            return False
        
        try:
            jq.auth(username, password)
            self._authenticated = True
            logger.info("✅ 聚宽数据源已连接")
            return True
        except Exception as e:
            logger.error(f"聚宽登录失败: {e}")
            return False
    
    def start(self) -> bool:
        """启动插件"""
        return self._authenticated
    
    def stop(self) -> bool:
        """停止插件"""
        if JQDATA_AVAILABLE and self._authenticated:
            try:
                jq.logout()
            except Exception:
                pass
        self._authenticated = False
        return True
    
    def get_bars(self, symbol: str, start_date: str, end_date: str,
                 frequency: str = "day") -> List[Dict]:
        """
        获取K线数据
        
        Args:
            symbol: 股票代码，如 "000001.XSHE"
            start_date: 开始日期
            end_date: 结束日期
            frequency: 频率，day/minute/week
        """
        if not self._authenticated:
            logger.error("未登录聚宽")
            return []
        
        try:
            # 转换频率
            freq_map = {
                "day": "daily",
                "daily": "daily",
                "minute": "minute",
                "1m": "1m",
                "5m": "5m",
                "15m": "15m",
                "30m": "30m",
                "60m": "60m",
                "week": "week",
                "month": "month",
            }
            jq_freq = freq_map.get(frequency, "daily")
            
            df = jq.get_price(
                symbol,
                start_date=start_date,
                end_date=end_date,
                frequency=jq_freq,
                fields=['open', 'high', 'low', 'close', 'volume', 'money'],
                skip_paused=True,
                fq='pre'  # 前复权
            )
            
            if df is None or df.empty:
                return []
            
            bars = []
            for idx, row in df.iterrows():
                bars.append({
                    "symbol": symbol,
                    "datetime": idx.strftime("%Y-%m-%d %H:%M:%S") if hasattr(idx, 'strftime') else str(idx),
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row["volume"]),
                    "amount": float(row["money"]),
                })
            
            return bars
            
        except Exception as e:
            logger.error(f"获取K线数据失败: {e}")
            return []
    
    def get_tick(self, symbol: str) -> Optional[Dict]:
        """获取实时行情"""
        if not self._authenticated:
            return None
        
        try:
            df = jq.get_current_data([symbol])
            if df is None or symbol not in df:
                return None
            
            data = df[symbol]
            return {
                "symbol": symbol,
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_price": data.last_price,
                "open": data.open,
                "high": data.high,
                "low": data.low,
                "volume": data.volume,
                "amount": data.money,
                "bid_price": data.bid_rows[0][0] if data.bid_rows else 0,
                "ask_price": data.ask_rows[0][0] if data.ask_rows else 0,
            }
        except Exception as e:
            logger.error(f"获取实时行情失败: {e}")
            return None
    
    def get_symbols(self, market: str = "") -> List[str]:
        """获取股票列表"""
        if not self._authenticated:
            return []
        
        try:
            if market.upper() == "SH":
                stocks = jq.get_all_securities(['stock'], date=datetime.now())
                return [s for s in stocks.index if s.endswith('.XSHG')]
            elif market.upper() == "SZ":
                stocks = jq.get_all_securities(['stock'], date=datetime.now())
                return [s for s in stocks.index if s.endswith('.XSHE')]
            else:
                stocks = jq.get_all_securities(['stock'], date=datetime.now())
                return list(stocks.index)
        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
            return []
    
    def get_index_stocks(self, index_code: str) -> List[str]:
        """获取指数成分股"""
        if not self._authenticated:
            return []
        
        try:
            return jq.get_index_stocks(index_code)
        except Exception as e:
            logger.error(f"获取指数成分股失败: {e}")
            return []
    
    def get_fundamentals(self, symbol: str, fields: List[str] = None) -> Dict:
        """获取财务数据"""
        if not self._authenticated:
            return {}
        
        try:
            from jqdatasdk import query, valuation
            
            q = query(valuation).filter(valuation.code == symbol)
            df = jq.get_fundamentals(q)
            
            if df is None or df.empty:
                return {}
            
            return df.iloc[0].to_dict()
        except Exception as e:
            logger.error(f"获取财务数据失败: {e}")
            return {}

