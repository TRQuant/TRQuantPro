"""
JQData增强版数据提供者

处理账号时间限制，自动读取配置

Author: TRQuant Team
Date: 2025-12-18
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class JQDataEnhanced:
    """增强版JQData数据提供者"""
    
    def __init__(self, config_path: str = None):
        self._jq = None
        self._authenticated = False
        self._permission_start = None
        self._permission_end = None
        self._config = {}
        
        # 加载配置
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '../../config/jqdata_config.json')
        
        self._load_config(config_path)
    
    def _load_config(self, config_path: str):
        """加载配置"""
        try:
            with open(config_path, 'r') as f:
                self._config = json.load(f)
            logger.info(f"JQData配置已加载: {config_path}")
        except Exception as e:
            logger.warning(f"JQData配置加载失败: {e}")
    
    def authenticate(self) -> bool:
        """认证"""
        if self._authenticated:
            return True
        
        try:
            import jqdatasdk as jq
            self._jq = jq
            
            # 禁用auth提示
            if hasattr(jq, 'JQDataClient'):
                jq.JQDataClient.enable_auth_prompt = False
            
            username = self._config.get('username', '')
            password = self._config.get('password', '')
            
            if not username or not password:
                logger.error("JQData账号信息缺失")
                return False
            
            jq.auth(username, password)
            self._authenticated = True
            
            # 检测权限范围
            self._detect_permission()
            
            logger.info(f"JQData认证成功，数据范围: {self._permission_start} ~ {self._permission_end}")
            return True
            
        except Exception as e:
            logger.error(f"JQData认证失败: {e}")
            return False
    
    def _detect_permission(self):
        """检测数据权限范围"""
        self._permission_start = datetime(2024, 9, 10)
        self._permission_end = datetime(2025, 9, 17)
        
        permission = self._config.get('permission', {})
        if not permission.get('auto_detect', True):
            start = permission.get('start_date')
            end = permission.get('end_date')
            if start:
                self._permission_start = datetime.fromisoformat(start)
            if end:
                self._permission_end = datetime.fromisoformat(end)
    
    def _get_valid_date(self) -> str:
        """获取有效的查询日期（在权限范围内）"""
        now = datetime.now()
        
        if now <= self._permission_end:
            query_date = now
        else:
            query_date = self._permission_end
        
        if query_date < self._permission_start:
            query_date = self._permission_start
        
        return query_date.strftime('%Y-%m-%d')
    
    def _adjust_date_range(self, start_date: datetime = None, end_date: datetime = None):
        """调整日期范围以适应权限"""
        now = datetime.now()
        
        if end_date is None:
            end_date = min(now, self._permission_end) if self._permission_end else now
        else:
            if self._permission_end and end_date > self._permission_end:
                end_date = self._permission_end
        
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        if self._permission_start and start_date < self._permission_start:
            start_date = self._permission_start
        
        return start_date, end_date
    
    def get_price(self, symbols: List[str], days: int = 30) -> Dict[str, Dict]:
        """获取行情数据"""
        if not self.authenticate():
            return {}
        
        start_date, end_date = self._adjust_date_range()
        start_date = max(start_date, end_date - timedelta(days=days))
        
        result = {}
        for symbol in symbols:
            try:
                df = self._jq.get_price(
                    symbol, 
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d'),
                    frequency='daily',
                    fields=['open', 'close', 'high', 'low', 'volume']
                )
                
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    prev_close = df.iloc[-2]['close'] if len(df) > 1 else latest['close']
                    
                    result[symbol] = {
                        "current_price": float(latest['close']),
                        "open": float(latest['open']),
                        "high": float(latest['high']),
                        "low": float(latest['low']),
                        "volume": int(latest['volume']),
                        "change_pct": float((latest['close'] - prev_close) / prev_close * 100) if prev_close else 0,
                        "data_date": str(df.index[-1].date())
                    }
            except Exception as e:
                logger.warning(f"获取{symbol}行情失败: {e}")
        
        return result
    
    def get_fundamentals(self, symbols: List[str]) -> Dict[str, Dict]:
        """获取财务数据"""
        if not self.authenticate():
            return {}
        
        from jqdatasdk import query, valuation, indicator
        
        # 使用有效日期
        query_date = self._get_valid_date()
        
        result = {}
        for symbol in symbols:
            try:
                # 估值数据
                q = query(
                    valuation.code,
                    valuation.pe_ratio,
                    valuation.pb_ratio,
                    valuation.market_cap,
                    valuation.circulating_market_cap
                ).filter(valuation.code == symbol)
                
                df = self._jq.get_fundamentals(q, date=query_date)
                
                fund_data = {}
                if df is not None and not df.empty:
                    row = df.iloc[0]
                    fund_data.update({
                        "pe_ratio": float(row.get('pe_ratio') or 0),
                        "pb_ratio": float(row.get('pb_ratio') or 0),
                        "market_cap": float(row.get('market_cap') or 0) ,  # 已经是亿元
                        "circulating_market_cap": float(row.get('circulating_market_cap') or 0)   # 已经是亿元
                    })
                
                # 财务指标
                q2 = query(
                    indicator.code,
                    indicator.roe,
                    indicator.gross_profit_margin,
                    indicator.inc_revenue_year_on_year,
                    indicator.inc_net_profit_year_on_year
                ).filter(indicator.code == symbol)
                
                df2 = self._jq.get_fundamentals(q2, date=query_date)
                
                if df2 is not None and not df2.empty:
                    row = df2.iloc[0]
                    fund_data.update({
                        "roe": float(row.get('roe') or 0),
                        "gross_margin": float(row.get('gross_profit_margin') or 0),
                        "revenue_growth": float(row.get('inc_revenue_year_on_year') or 0),
                        "profit_growth": float(row.get('inc_net_profit_year_on_year') or 0)
                    })
                
                if fund_data:
                    result[symbol] = fund_data
                    
            except Exception as e:
                logger.warning(f"获取{symbol}财务数据失败: {e}")
        
        return result
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """获取股票基本信息"""
        if not self.authenticate():
            return None
        
        try:
            info = self._jq.get_security_info(symbol)
            if info:
                return {
                    "symbol": symbol,
                    "name": info.display_name,
                    "type": info.type,
                    "start_date": str(info.start_date)
                }
        except Exception as e:
            logger.warning(f"获取{symbol}信息失败: {e}")
        
        return None
    
    def get_all_securities(self, types: List[str] = None) -> Dict[str, str]:
        """获取所有证券列表"""
        if not self.authenticate():
            return {}
        
        if types is None:
            types = ['stock']
        
        result = {}
        try:
            for t in types:
                df = self._jq.get_all_securities(types=t)
                if df is not None:
                    for idx, row in df.iterrows():
                        result[idx] = row['display_name']
        except Exception as e:
            logger.warning(f"获取证券列表失败: {e}")
        
        return result
    
    def get_industry(self, symbol: str) -> Optional[Dict]:
        """获取股票行业分类"""
        if not self.authenticate():
            return None
        
        try:
            industry = self._jq.get_industry(symbol)
            if industry and symbol in industry:
                return industry[symbol]
        except Exception as e:
            logger.warning(f"获取{symbol}行业失败: {e}")
        
        return None
    
    @property
    def is_authenticated(self) -> bool:
        return self._authenticated
    
    @property
    def permission_range(self) -> tuple:
        return (self._permission_start, self._permission_end)


# 全局实例
_jqdata_enhanced: Optional[JQDataEnhanced] = None


def get_jqdata_enhanced() -> JQDataEnhanced:
    global _jqdata_enhanced
    if _jqdata_enhanced is None:
        _jqdata_enhanced = JQDataEnhanced()
    return _jqdata_enhanced
