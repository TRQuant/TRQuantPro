"""
十倍股V2系统 - 数据获取模块

基于JQData API测试结果，使用可用字段获取数据

可用字段（试用账户）：
1. indicator表：roe, roa, net_profit_margin, gross_profit_margin,
                inc_revenue_year_on_year, inc_net_profit_year_on_year, eps
                ocf_to_operating_profit, ocf_to_revenue（现金流代理指标）
2. valuation表：pe_ratio, pb_ratio, ps_ratio, pcf_ratio,
                market_cap, circulating_market_cap, turnover_ratio
3. get_price：open, close, high, low, volume

权限限制（试用账户）：
- finance.STK_CASHFLOW_STATEMENT（现金流量表）：返回"非法查询"错误
- finance.STK_BALANCE_SHEET（资产负债表）：返回"非法查询"错误
- 标准字段名：使用snake_case命名（如net_operate_cash_flow, total_assets）

替代方案：
- 现金流数据：使用indicator表的ocf_to_operating_profit和ocf_to_revenue
- 资产负债率：使用默认值或估算

Author: TRQuant Team
Date: 2025-12-19
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class TenbaggerDataFetcher:
    """
    十倍股数据获取器
    
    基于JQData试用账户可用字段实现
    """
    
    def __init__(self, jq_client=None):
        """
        初始化数据获取器
        
        Args:
            jq_client: JQDataClient实例（必须已认证）
        """
        self.jq_client = jq_client
        self.permission = None
        self._available_end_date = None
        
        if jq_client:
            if not jq_client.is_authenticated():
                logger.warning("JQDataClient未认证")
            else:
                self.permission = jq_client.get_permission()
                self._available_end_date = jq_client.get_available_end_date()
    
    def _get_valid_date(self, requested_date: Optional[str] = None) -> str:
        """获取有效的查询日期（在权限范围内）"""
        if not self.permission or not self.permission.detected:
            return requested_date or datetime.now().strftime('%Y-%m-%d')
        
        if requested_date is None:
            return self._available_end_date
        
        if self.permission.is_date_in_range(requested_date):
            return requested_date
        else:
            logger.warning(f"请求日期 {requested_date} 不在权限范围内，使用 {self._available_end_date}")
            return self._available_end_date
    
    def fetch_indicator_data(self, symbol: str, date: Optional[str] = None) -> Dict[str, Any]:
        """
        获取财务指标数据（indicator表）
        
        可用字段：roe, roa, net_profit_margin, gross_profit_margin,
                 inc_revenue_year_on_year, inc_net_profit_year_on_year, eps
        """
        if not self.jq_client or not self.jq_client.is_authenticated():
            logger.warning(f"{symbol}: JQData未认证")
            return {}
        
        data = {}
        valid_date = self._get_valid_date(date)
        
        try:
            from jqdatasdk import query, indicator
            
            # 只查询确定存在的字段
            q = query(
                indicator.code,
                indicator.roe,
                indicator.roa,
                indicator.net_profit_margin,
                indicator.gross_profit_margin,
                indicator.inc_revenue_year_on_year,
                indicator.inc_net_profit_year_on_year,
                indicator.eps
            ).filter(
                indicator.code == symbol
            )
            
            df = self.jq_client.get_fundamentals(q, date=valid_date)
            
            if df is not None and not df.empty:
                row = df.iloc[0]
                data = {
                    "roe": self._safe_float(row.get('roe')),
                    "roa": self._safe_float(row.get('roa')),
                    "net_profit_margin": self._safe_float(row.get('net_profit_margin')),
                    "gross_margin": self._safe_float(row.get('gross_profit_margin')),
                    "revenue_growth": self._safe_float(row.get('inc_revenue_year_on_year')),
                    "profit_growth": self._safe_float(row.get('inc_net_profit_year_on_year')),
                    "eps": self._safe_float(row.get('eps')),
                }
                logger.debug(f"{symbol}: 财务指标获取成功")
            else:
                logger.warning(f"{symbol}: indicator表未返回数据")
                
        except Exception as e:
            logger.warning(f"{symbol}: 获取财务指标失败 - {e}")
        
        return data
    
    def fetch_valuation_data(self, symbol: str, date: Optional[str] = None) -> Dict[str, Any]:
        """
        获取估值数据（valuation表）
        
        可用字段：pe_ratio, pb_ratio, ps_ratio, pcf_ratio,
                 market_cap, circulating_market_cap, turnover_ratio
        """
        if not self.jq_client or not self.jq_client.is_authenticated():
            logger.warning(f"{symbol}: JQData未认证")
            return {}
        
        data = {}
        valid_date = self._get_valid_date(date)
        
        try:
            from jqdatasdk import query, valuation
            
            q = query(
                valuation.code,
                valuation.pe_ratio,
                valuation.pb_ratio,
                valuation.ps_ratio,
                valuation.pcf_ratio,
                valuation.market_cap,
                valuation.circulating_market_cap,
                valuation.turnover_ratio
            ).filter(
                valuation.code == symbol
            )
            
            df = self.jq_client.get_fundamentals(q, date=valid_date)
            
            if df is not None and not df.empty:
                row = df.iloc[0]
                data = {
                    "pe_ratio": self._safe_float(row.get('pe_ratio')),
                    "pb_ratio": self._safe_float(row.get('pb_ratio')),
                    "ps_ratio": self._safe_float(row.get('ps_ratio')),
                    "pcf_ratio": self._safe_float(row.get('pcf_ratio')),
                    "market_cap": self._safe_float(row.get('market_cap')),  # JQData返回值已是亿元
                    "circulating_market_cap": self._safe_float(row.get('circulating_market_cap')),
                    "turnover_ratio": self._safe_float(row.get('turnover_ratio')),
                }
                logger.debug(f"{symbol}: 估值数据获取成功")
            else:
                logger.warning(f"{symbol}: valuation表未返回数据")
                
        except Exception as e:
            logger.warning(f"{symbol}: 获取估值数据失败 - {e}")
        
        return data
    
    def fetch_price_data(self, symbol: str, days: int = 60) -> Dict[str, Any]:
        """
        获取市场价格数据（get_price）
        
        可用字段：open, close, high, low, volume
        """
        if not self.jq_client or not self.jq_client.is_authenticated():
            logger.warning(f"{symbol}: JQData未认证")
            return {}
        
        data = {}
        
        try:
            # 计算日期范围（确保在权限范围内）
            if self.permission and self.permission.detected:
                end_date = self._available_end_date
                start_date_dt = datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days)
                perm_start_dt = datetime.strptime(self.permission.start_date, '%Y-%m-%d')
                
                if start_date_dt < perm_start_dt:
                    start_date_dt = perm_start_dt
                
                start_date = start_date_dt.strftime('%Y-%m-%d')
            else:
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # 获取价格数据
            prices = self.jq_client.get_price(
                symbol,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['open', 'close', 'high', 'low', 'volume']
            )
            
            if prices is None or len(prices) == 0:
                logger.warning(f"{symbol}: 未获取到价格数据")
                return {}
            
            # 计算技术指标
            data["latest_close"] = self._safe_float(prices['close'].iloc[-1])
            data["latest_volume"] = self._safe_float(prices['volume'].iloc[-1])
            
            # 涨跌幅
            if len(prices) > 1:
                first_close = self._safe_float(prices['close'].iloc[0])
                if first_close > 0:
                    data["price_change_pct"] = (data["latest_close"] / first_close - 1) * 100
                else:
                    data["price_change_pct"] = 0
            else:
                data["price_change_pct"] = 0
            
            # 成交量变化
            if len(prices) >= 20:
                recent_vol = prices['volume'].tail(5).mean()
                avg_vol = prices['volume'].tail(20).mean()
                data["volume_ratio"] = recent_vol / avg_vol if avg_vol > 0 else 1.0
            else:
                data["volume_ratio"] = 1.0
            
            # 均线趋势
            if len(prices) >= 20:
                ma5 = prices['close'].tail(5).mean()
                ma20 = prices['close'].tail(20).mean()
                if data["latest_close"] > ma5 > ma20:
                    data["ma_trend"] = "bullish"
                elif data["latest_close"] < ma5:
                    data["ma_trend"] = "bearish"
                else:
                    data["ma_trend"] = "neutral"
            else:
                data["ma_trend"] = "neutral"
            
            # 相对强度（近20日涨幅）
            if len(prices) >= 20:
                price_20d_ago = self._safe_float(prices['close'].iloc[-20])
                if price_20d_ago > 0:
                    change = (data["latest_close"] / price_20d_ago - 1) * 100
                    data["relative_strength"] = min(100, max(0, 50 + change))
                else:
                    data["relative_strength"] = 50
            else:
                data["relative_strength"] = 50
            
            # 突破信号
            if len(prices) >= 20:
                high_20 = prices['high'].tail(20).max()
                data["breakout_signal"] = data["latest_close"] >= high_20 * 0.95
            else:
                data["breakout_signal"] = False
            
            logger.debug(f"{symbol}: 价格数据获取成功 ({len(prices)}条)")
            
        except Exception as e:
            logger.warning(f"{symbol}: 获取价格数据失败 - {e}")
        
        return data
    
    def fetch_complete_data(self, symbol: str, date: Optional[str] = None) -> Dict[str, Any]:
        """
        获取完整的评估数据
        
        整合indicator + valuation + price数据
        """
        data = {}
        
        # 1. 获取财务指标
        indicator_data = self.fetch_indicator_data(symbol, date)
        data.update(indicator_data)
        
        # 2. 获取估值数据
        valuation_data = self.fetch_valuation_data(symbol, date)
        data.update(valuation_data)
        
        # 3. 获取价格数据
        price_data = self.fetch_price_data(symbol)
        data.update(price_data)
        
        # 4. 检查ST状态
        data["is_st"] = False
        if self.jq_client:
            try:
                all_secs = self.jq_client.get_all_securities(['stock'])
                if all_secs is not None and symbol in all_secs.index:
                    name = all_secs.loc[symbol, 'display_name']
                    data["is_st"] = "ST" in name or "*ST" in name
                    data["stock_name"] = name
            except Exception as e:
                logger.debug(f"{symbol}: 获取ST状态失败 - {e}")
        
        # 5. 添加默认值（用于评估系统）
        self._set_defaults(data)
        
        # 6. 计算数据完整度
        filled_count = sum(1 for v in data.values() if v is not None and v != 0)
        data["data_quality"] = filled_count / max(len(data), 1)
        
        return data
    
    def _safe_float(self, value, default: float = 0.0) -> float:
        """安全转换为浮点数"""
        if value is None:
            return default
        try:
            import math
            result = float(value)
            if math.isnan(result) or math.isinf(result):
                return default
            return result
        except (ValueError, TypeError):
            return default
    
    def _set_defaults(self, data: Dict[str, Any]):
        """设置默认值"""
        defaults = {
            # 财务指标默认值
            "roe": 0,
            "roa": 0,
            "net_profit_margin": 0,
            "gross_margin": 0,
            "revenue_growth": 0,
            "profit_growth": 0,
            "eps": 0,
            "debt_ratio": 50,  # 默认50%
            "current_ratio": 1.5,
            
            # 估值默认值
            "pe_ratio": 20,
            "pb_ratio": 2,
            "ps_ratio": 2,
            "pcf_ratio": 10,
            "market_cap": 100,  # 亿元
            "circulating_market_cap": 80,
            "turnover_ratio": 1,
            
            # 价格数据默认值
            "latest_close": 0,
            "latest_volume": 0,
            "price_change_pct": 0,
            "volume_ratio": 1.0,
            "ma_trend": "neutral",
            "relative_strength": 50,
            "breakout_signal": False,
            
            # L0硬过滤默认值
            "is_st": False,
            "delisting_risk": False,
            "major_violation": False,
            "trading_days_ratio": 0.95,
            "financial_report_count": 4,
            "missing_ratio": 0.0,
            "avg_turnover": 0.02,  # 默认2%，用于流动性检查
            
            # 其他默认值
            "cash_flow_improvement": False,
            "cash_flow_ratio": 0,
            "cash_flow_negative_years": 0,
            "revenue_growth_qoq_change": 0,
            "profit_growth_change": 0,
            "gross_margin_change": 0,
            "consecutive_improvement_quarters": 0,
            
            # 市值/PE分位数
            "market_cap_percentile": 0.5,
            "pe_percentile": 0.5,
            
            # 其他
            "event_count": 0,
            "analyst_coverage": 0,
            "research_report_count": 0,
            "announcement_count_3m": 0,
        }
        
        for key, default_value in defaults.items():
            data.setdefault(key, default_value)
        
        # 使用turnover_ratio设置avg_turnover
        if data.get("turnover_ratio") and data.get("turnover_ratio") > 0:
            data["avg_turnover"] = data["turnover_ratio"] / 100  # turnover_ratio是百分比
        
        # 根据市值计算分位数
        if data.get("market_cap", 0) > 0:
            mc = data["market_cap"]
            if mc > 1000:
                data["market_cap_percentile"] = 0.9
            elif mc > 500:
                data["market_cap_percentile"] = 0.7
            elif mc > 100:
                data["market_cap_percentile"] = 0.5
            else:
                data["market_cap_percentile"] = 0.3
        
        # 根据PE计算分位数
        if data.get("pe_ratio", 0) > 0:
            pe = data["pe_ratio"]
            if pe < 10:
                data["pe_percentile"] = 0.2
            elif pe < 20:
                data["pe_percentile"] = 0.4
            elif pe < 40:
                data["pe_percentile"] = 0.6
            else:
                data["pe_percentile"] = 0.8


def get_data_fetcher(jq_client=None) -> TenbaggerDataFetcher:
    """获取数据获取器实例"""
    return TenbaggerDataFetcher(jq_client=jq_client)
