"""
A股特色市场指标分析模块
========================

优先使用聚宽JQData获取数据，AKShare作为备用数据源。

包含以下分析器：
1. NorthFundAnalyzer - 北向资金分析 (沪深港通)
2. MarginAnalyzer - 两融分析 (融资融券)
3. MarketBreadthAnalyzer - 市场宽度分析 (涨跌停、新高新低、均线多头占比)
4. AStockIndicatorAggregator - 综合指标聚合器

数据源优先级: JQData > AKShare > 缓存
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Dict, Optional, List, Any, Tuple
from enum import Enum
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# =============================================================================
# 数据结构定义
# =============================================================================

@dataclass
class NorthFundData:
    """北向资金数据"""
    date: str
    # 当日数据
    net_buy_amount: float = 0.0  # 当日净买入额(亿元)
    sh_net_buy: float = 0.0      # 沪股通净买入(亿元)
    sz_net_buy: float = 0.0      # 深股通净买入(亿元)
    # 累计数据
    net_buy_5d: float = 0.0      # 5日累计净买入(亿元)
    net_buy_10d: float = 0.0     # 10日累计净买入(亿元)
    net_buy_20d: float = 0.0     # 20日累计净买入(亿元)
    # 信号
    signal_score: float = 0.0    # -100 ~ +100
    signal_description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "net_buy_amount": self.net_buy_amount,
            "sh_net_buy": self.sh_net_buy,
            "sz_net_buy": self.sz_net_buy,
            "net_buy_5d": self.net_buy_5d,
            "net_buy_10d": self.net_buy_10d,
            "net_buy_20d": self.net_buy_20d,
            "signal_score": self.signal_score,
            "signal_description": self.signal_description,
        }


@dataclass
class MarginData:
    """融资融券数据"""
    date: str
    # 融资数据
    fin_balance: float = 0.0        # 融资余额(亿元)
    fin_buy_amount: float = 0.0     # 融资买入额(亿元)
    fin_balance_change: float = 0.0 # 融资余额变化(亿元)
    fin_change_rate: float = 0.0    # 融资余额变化率(%)
    # 融券数据
    sec_balance: float = 0.0        # 融券余额(亿元)
    sec_sell_amount: float = 0.0    # 融券卖出额(亿元)
    # 综合指标
    total_balance: float = 0.0      # 两融余额(亿元)
    fin_sec_ratio: float = 0.0      # 融资/融券比例
    # 信号
    signal_score: float = 0.0       # -100 ~ +100
    signal_description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "fin_balance": self.fin_balance,
            "fin_buy_amount": self.fin_buy_amount,
            "fin_balance_change": self.fin_balance_change,
            "fin_change_rate": self.fin_change_rate,
            "sec_balance": self.sec_balance,
            "sec_sell_amount": self.sec_sell_amount,
            "total_balance": self.total_balance,
            "fin_sec_ratio": self.fin_sec_ratio,
            "signal_score": self.signal_score,
            "signal_description": self.signal_description,
        }


@dataclass
class MarketBreadthData:
    """市场宽度数据"""
    date: str
    # 涨跌停统计
    limit_up_count: int = 0         # 涨停家数
    limit_down_count: int = 0       # 跌停家数
    limit_up_down_ratio: float = 0.0  # 涨停/跌停比
    # 涨跌家数
    up_count: int = 0               # 上涨家数
    down_count: int = 0             # 下跌家数
    flat_count: int = 0             # 平盘家数
    up_down_ratio: float = 0.0      # 上涨/下跌比
    # 新高新低
    new_high_count: int = 0         # 创新高家数(60日)
    new_low_count: int = 0          # 创新低家数(60日)
    new_high_low_ratio: float = 0.0 # 新高/新低比
    # 均线多头
    ma_bullish_count: int = 0       # 均线多头排列家数
    ma_bullish_ratio: float = 0.0   # 均线多头占比(%)
    # 换手率
    avg_turnover_rate: float = 0.0  # 市场平均换手率(%)
    # 信号
    signal_score: float = 0.0       # -100 ~ +100
    signal_description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "limit_up_count": self.limit_up_count,
            "limit_down_count": self.limit_down_count,
            "limit_up_down_ratio": self.limit_up_down_ratio,
            "up_count": self.up_count,
            "down_count": self.down_count,
            "flat_count": self.flat_count,
            "up_down_ratio": self.up_down_ratio,
            "new_high_count": self.new_high_count,
            "new_low_count": self.new_low_count,
            "new_high_low_ratio": self.new_high_low_ratio,
            "ma_bullish_count": self.ma_bullish_count,
            "ma_bullish_ratio": self.ma_bullish_ratio,
            "avg_turnover_rate": self.avg_turnover_rate,
            "signal_score": self.signal_score,
            "signal_description": self.signal_description,
        }


@dataclass
class AStockIndicatorResult:
    """A股综合指标结果"""
    date: str
    north_fund: Optional[NorthFundData] = None
    margin: Optional[MarginData] = None
    market_breadth: Optional[MarketBreadthData] = None
    # 综合评分
    composite_score: float = 0.0    # -100 ~ +100
    signal_level: str = "neutral"   # bullish/bearish/neutral
    recommendation: str = ""
    # 元数据
    data_source: str = "jqdata"
    success: bool = True
    error_message: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "north_fund": self.north_fund.to_dict() if self.north_fund else None,
            "margin": self.margin.to_dict() if self.margin else None,
            "market_breadth": self.market_breadth.to_dict() if self.market_breadth else None,
            "composite_score": self.composite_score,
            "signal_level": self.signal_level,
            "recommendation": self.recommendation,
            "data_source": self.data_source,
            "success": self.success,
            "error_message": self.error_message,
        }


# =============================================================================
# 北向资金分析器
# =============================================================================

class NorthFundAnalyzer:
    """
    北向资金分析器
    
    数据源: JQData finance.STK_HK_HOLD_INFO / finance.STK_ML_QUOTA
    备用: AKShare
    
    判断阈值:
    - 5日累计净买入 > 100亿: 看多信号
    - 5日累计净买入 < -100亿: 看空信号
    - 单日净买入 > 50亿: 强势流入
    - 单日净买入 < -50亿: 强势流出
    """
    
    # 阈值配置
    THRESHOLDS = {
        "daily_strong_inflow": 50.0,    # 单日强势流入(亿元)
        "daily_strong_outflow": -50.0,  # 单日强势流出(亿元)
        "5d_bullish": 100.0,            # 5日累计看多阈值
        "5d_bearish": -100.0,           # 5日累计看空阈值
        "10d_bullish": 200.0,           # 10日累计看多阈值
        "10d_bearish": -200.0,          # 10日累计看空阈值
    }
    
    def __init__(self, jq_client=None):
        self.jq_client = jq_client
        self._cache: Dict[str, NorthFundData] = {}
    
    def analyze(self, target_date: Optional[str] = None) -> NorthFundData:
        """
        分析北向资金状况
        
        Args:
            target_date: 目标日期，默认为最新可用日期
        
        Returns:
            NorthFundData: 北向资金数据
        """
        if target_date is None:
            target_date = date.today().strftime('%Y-%m-%d')
        
        # 检查缓存
        if target_date in self._cache:
            return self._cache[target_date]
        
        result = NorthFundData(date=target_date)
        
        try:
            # 优先使用JQData
            if self.jq_client and self.jq_client.is_authenticated():
                result = self._fetch_from_jqdata(target_date)
            else:
                # 备用: AKShare
                result = self._fetch_from_akshare(target_date)
            
            # 计算信号
            result = self._calculate_signal(result)
            
            # 缓存结果
            self._cache[target_date] = result
            
        except Exception as e:
            logger.error(f"北向资金分析失败: {e}")
            result.signal_description = f"数据获取失败: {str(e)}"
        
        return result
    
    def _fetch_from_jqdata(self, target_date: str) -> NorthFundData:
        """
        从JQData获取北向资金数据
        
        重要说明:
        - 2024-08-18之后，北向资金不再披露买入/卖出分项，只有sum_amount(成交总额)
        - 2024-08-16及之前的历史数据完整，可计算净买入
        - 此函数适用于历史回测(2014-11 ~ 2024-08)
        """
        import jqdatasdk as jq
        from jqdatasdk import finance, query
        
        result = NorthFundData(date=target_date)
        
        # 数据披露截止日期
        DISCLOSURE_CUTOFF = '2024-08-16'
        
        try:
            target_dt = datetime.strptime(target_date, '%Y-%m-%d')
            cutoff_dt = datetime.strptime(DISCLOSURE_CUTOFF, '%Y-%m-%d')
            
            # 如果目标日期在披露截止日期之后，无法获取净买入数据
            if target_dt > cutoff_dt:
                logger.warning(f"北向资金自2024-08-18起不再披露买卖分项，{target_date}无法计算净买入")
                # 尝试使用AKShare历史数据
                return self._fetch_from_akshare(target_date)
            
            # 获取历史数据 (30天)
            start_date = target_dt - timedelta(days=30)
            
            q = query(
                finance.STK_ML_QUOTA.day,
                finance.STK_ML_QUOTA.link_id,
                finance.STK_ML_QUOTA.link_name,
                finance.STK_ML_QUOTA.buy_amount,
                finance.STK_ML_QUOTA.sell_amount,
                finance.STK_ML_QUOTA.sum_amount
            ).filter(
                finance.STK_ML_QUOTA.day >= start_date.strftime('%Y-%m-%d'),
                finance.STK_ML_QUOTA.day <= target_date,
                finance.STK_ML_QUOTA.link_id.in_([310001, 310002])  # 沪股通、深股通
            ).order_by(
                finance.STK_ML_QUOTA.day.desc()
            )
            
            df = finance.run_query(q)
            
            if df is not None and not df.empty:
                # 转换日期
                df['day'] = pd.to_datetime(df['day'])
                
                # 计算净买入
                df['net_buy'] = df['buy_amount'].fillna(0) - df['sell_amount'].fillna(0)
                
                # 获取最新日期数据
                latest_date = df['day'].max()
                latest_data = df[df['day'] == latest_date]
                
                # 沪股通
                sh_data = latest_data[latest_data['link_id'] == 310001]
                if not sh_data.empty:
                    result.sh_net_buy = float(sh_data['net_buy'].iloc[0])
                
                # 深股通
                sz_data = latest_data[latest_data['link_id'] == 310002]
                if not sz_data.empty:
                    result.sz_net_buy = float(sz_data['net_buy'].iloc[0])
                
                result.net_buy_amount = result.sh_net_buy + result.sz_net_buy
                result.date = latest_date.strftime('%Y-%m-%d')
                
                # 计算累计净买入 (按日期分组)
                daily_net = df.groupby('day')['net_buy'].sum().sort_index(ascending=False)
                
                if len(daily_net) >= 5:
                    result.net_buy_5d = float(daily_net.head(5).sum())
                if len(daily_net) >= 10:
                    result.net_buy_10d = float(daily_net.head(10).sum())
                if len(daily_net) >= 20:
                    result.net_buy_20d = float(daily_net.head(20).sum())
                
                logger.info(f"JQData北向资金({result.date}): 沪股通={result.sh_net_buy:.2f}亿, 深股通={result.sz_net_buy:.2f}亿, 合计={result.net_buy_amount:.2f}亿, 5日累计={result.net_buy_5d:.2f}亿")
            else:
                logger.warning(f"JQData未返回{target_date}的北向资金数据")
                return self._fetch_from_akshare(target_date)
                
        except Exception as e:
            logger.warning(f"JQData获取北向资金失败: {e}")
            import traceback
            traceback.print_exc()
            return self._fetch_from_akshare(target_date)
        
        return result
    
    def _fetch_from_akshare(self, target_date: str) -> NorthFundData:
        """
        从AKShare获取北向资金数据
        
        使用 stock_hsgt_hist_em 接口获取历史北向资金数据
        字段: 日期, 当日成交净买额, 买入成交额, 卖出成交额, 历史累计净买额, 
              当日资金流入, 当日余额, 持股市值 等
        """
        result = NorthFundData(date=target_date)
        
        try:
            import akshare as ak
            
            # 获取北向资金历史数据
            df = ak.stock_hsgt_hist_em(symbol='北向资金')
            
            if df is not None and not df.empty:
                df['日期'] = pd.to_datetime(df['日期'])
                
                # 过滤有效数据（净买额不为空）
                df_valid = df[df['当日成交净买额'].notna()].copy()
                df_valid = df_valid.sort_values('日期', ascending=False)
                
                # 获取最近的数据
                target_dt = pd.to_datetime(target_date)
                recent = df_valid[df_valid['日期'] <= target_dt].head(20)
                
                if not recent.empty:
                    latest = recent.iloc[0]
                    latest_date = latest['日期'].strftime('%Y-%m-%d')
                    
                    # 北向资金净流入(亿元) - 字段是 "当日成交净买额"
                    result.net_buy_amount = float(latest.get('当日成交净买额', 0) or 0)
                    # 注意: AKShare的北向资金数据是合计，不分沪股通/深股通
                    # 如需分开，需要分别查询沪股通和深股通
                    result.date = latest_date  # 更新为实际数据日期
                    
                    # 计算累计净买入
                    if len(recent) >= 5:
                        result.net_buy_5d = recent.head(5)['当日成交净买额'].sum()
                    if len(recent) >= 10:
                        result.net_buy_10d = recent.head(10)['当日成交净买额'].sum()
                    if len(recent) >= 20:
                        result.net_buy_20d = recent.head(20)['当日成交净买额'].sum()
                    
                    logger.info(f"AKShare北向资金({latest_date}): 当日={result.net_buy_amount:.2f}亿, 5日累计={result.net_buy_5d:.2f}亿")
                else:
                    logger.warning(f"AKShare无 {target_date} 之前的有效北向资金数据")
                    
        except Exception as e:
            logger.error(f"AKShare获取北向资金失败: {e}")
            import traceback
            traceback.print_exc()
        
        return result
    
    def _calculate_signal(self, data: NorthFundData) -> NorthFundData:
        """计算北向资金信号"""
        score = 0.0
        descriptions = []
        
        # 1. 单日净买入信号 (权重30%)
        if data.net_buy_amount >= self.THRESHOLDS["daily_strong_inflow"]:
            score += 30
            descriptions.append(f"单日强势流入{data.net_buy_amount:.1f}亿")
        elif data.net_buy_amount <= self.THRESHOLDS["daily_strong_outflow"]:
            score -= 30
            descriptions.append(f"单日强势流出{abs(data.net_buy_amount):.1f}亿")
        else:
            # 线性插值
            score += (data.net_buy_amount / 50) * 15
        
        # 2. 5日累计信号 (权重40%)
        if data.net_buy_5d >= self.THRESHOLDS["5d_bullish"]:
            score += 40
            descriptions.append(f"5日累计流入{data.net_buy_5d:.1f}亿,看多")
        elif data.net_buy_5d <= self.THRESHOLDS["5d_bearish"]:
            score -= 40
            descriptions.append(f"5日累计流出{abs(data.net_buy_5d):.1f}亿,看空")
        else:
            score += (data.net_buy_5d / 100) * 20
        
        # 3. 10日趋势信号 (权重30%)
        if data.net_buy_10d >= self.THRESHOLDS["10d_bullish"]:
            score += 30
            descriptions.append("10日趋势向好")
        elif data.net_buy_10d <= self.THRESHOLDS["10d_bearish"]:
            score -= 30
            descriptions.append("10日趋势转弱")
        else:
            score += (data.net_buy_10d / 200) * 15
        
        # 限制范围
        data.signal_score = max(-100, min(100, score))
        data.signal_description = "; ".join(descriptions) if descriptions else "北向资金中性"
        
        return data


# =============================================================================
# 融资融券分析器
# =============================================================================

class MarginAnalyzer:
    """
    融资融券分析器
    
    数据源: JQData finance.STK_MT_TOTAL
    备用: AKShare
    
    判断阈值:
    - 融资余额变化率 > 2%: 看多信号
    - 融资余额变化率 < -2%: 看空信号
    - 融资/融券比例 > 50: 极度乐观
    - 融资买入占比 > 10%: 市场过热
    """
    
    THRESHOLDS = {
        "fin_change_bullish": 2.0,   # 融资增长看多(%)
        "fin_change_bearish": -2.0,  # 融资下降看空(%)
        "fin_sec_ratio_high": 50.0,  # 融资/融券高比例
        "fin_sec_ratio_low": 10.0,   # 融资/融券低比例
    }
    
    def __init__(self, jq_client=None):
        self.jq_client = jq_client
        self._cache: Dict[str, MarginData] = {}
    
    def analyze(self, target_date: Optional[str] = None) -> MarginData:
        """分析融资融券状况"""
        if target_date is None:
            target_date = date.today().strftime('%Y-%m-%d')
        
        if target_date in self._cache:
            return self._cache[target_date]
        
        result = MarginData(date=target_date)
        
        try:
            if self.jq_client and self.jq_client.is_authenticated():
                result = self._fetch_from_jqdata(target_date)
            else:
                result = self._fetch_from_akshare(target_date)
            
            result = self._calculate_signal(result)
            self._cache[target_date] = result
            
        except Exception as e:
            logger.error(f"融资融券分析失败: {e}")
            result.signal_description = f"数据获取失败: {str(e)}"
        
        return result
    
    def _fetch_from_jqdata(self, target_date: str) -> MarginData:
        """
        从JQData获取融资融券数据
        
        JQData STK_MT_TOTAL 表字段:
        - fin_value: 融资余额 (元)
        - fin_buy_value: 融资买入额 (元)
        - sec_value: 融券余额 (元)
        - sec_volume: 融券余量 (股)
        - sec_sell_volume: 融券卖出量 (股)
        - fin_sec_value: 融资融券余额 (元)
        """
        import jqdatasdk as jq
        from jqdatasdk import finance, query
        
        result = MarginData(date=target_date)
        
        try:
            # 获取融资融券汇总数据
            end_date = datetime.strptime(target_date, '%Y-%m-%d')
            start_date = end_date - timedelta(days=10)
            
            # 查询时先不限制交易所，获取所有数据
            q = query(
                finance.STK_MT_TOTAL
            ).filter(
                finance.STK_MT_TOTAL.date >= start_date.strftime('%Y-%m-%d'),
                finance.STK_MT_TOTAL.date <= target_date
            ).order_by(
                finance.STK_MT_TOTAL.date.desc()
            ).limit(20)
            
            df = finance.run_query(q)
            
            if df is not None and not df.empty:
                # 转换日期
                df['date'] = pd.to_datetime(df['date'])
                
                # 按日期统计每日的交易所数量，找到数据完整的最新日期
                daily_exchange_count = df.groupby('date')['exchange_code'].nunique()
                max_exchanges = daily_exchange_count.max()  # 正常应该是2（上交所+深交所）
                
                # 找到数据完整（有两个交易所数据）的最新日期
                complete_dates = daily_exchange_count[daily_exchange_count == max_exchanges].index
                
                if len(complete_dates) > 0:
                    latest_date = complete_dates.max()
                    latest_data = df[df['date'] == latest_date]
                    
                    # 获取前一个完整数据日期用于计算变化率
                    prev_complete_dates = complete_dates[complete_dates < latest_date]
                    if len(prev_complete_dates) > 0:
                        prev_date = prev_complete_dates.max()
                        prev_data = df[df['date'] == prev_date]
                    else:
                        prev_data = pd.DataFrame()
                else:
                    # 如果没有完整数据，使用最新数据
                    latest_date = df['date'].max()
                    latest_data = df[df['date'] == latest_date]
                    prev_data = pd.DataFrame()
                    logger.warning(f"两融数据不完整，只有 {daily_exchange_count[latest_date]} 个交易所数据")
                
                # 汇总当日数据 (fin_value 是融资余额，单位是元)
                latest_fin = latest_data['fin_value'].sum() / 100000000  # 转亿
                latest_sec = latest_data['sec_value'].sum() / 100000000
                latest_fin_buy = latest_data['fin_buy_value'].sum() / 100000000
                latest_total = latest_data['fin_sec_value'].sum() / 100000000
                
                result.fin_balance = latest_fin
                result.sec_balance = latest_sec
                result.fin_buy_amount = latest_fin_buy
                result.total_balance = latest_total
                result.date = latest_date.strftime('%Y-%m-%d')
                
                # 计算变化率（只在数据完整时计算）
                if not prev_data.empty:
                    prev_fin = prev_data['fin_value'].sum() / 100000000
                    if prev_fin > 0:
                        result.fin_balance_change = latest_fin - prev_fin
                        result.fin_change_rate = (result.fin_balance_change / prev_fin) * 100
                
                # 融资/融券比例
                if latest_sec > 0:
                    result.fin_sec_ratio = latest_fin / latest_sec
                
                logger.info(f"JQData两融({result.date}): 融资余额={result.fin_balance:.2f}亿, 变化率={result.fin_change_rate:.2f}%")
            else:
                logger.warning("JQData未返回两融数据，尝试AKShare")
                return self._fetch_from_akshare(target_date)
                
        except Exception as e:
            logger.warning(f"JQData获取两融失败: {e}, 尝试AKShare")
            import traceback
            traceback.print_exc()
            return self._fetch_from_akshare(target_date)
        
        return result
    
    def _fetch_from_akshare(self, target_date: str) -> MarginData:
        """从AKShare获取融资融券数据"""
        result = MarginData(date=target_date)
        
        try:
            import akshare as ak
            
            # 获取沪深两市融资融券汇总
            df = ak.stock_margin_sse()  # 上交所
            df2 = ak.stock_margin_szse()  # 深交所
            
            # 简单处理最新数据
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                result.fin_balance = float(latest.get('融资余额', 0) or 0) / 100000000
            
            if df2 is not None and not df2.empty:
                latest2 = df2.iloc[-1]
                result.fin_balance += float(latest2.get('融资余额', 0) or 0) / 100000000
            
            logger.info(f"AKShare两融: 融资余额={result.fin_balance:.2f}亿")
            
        except Exception as e:
            logger.error(f"AKShare获取两融失败: {e}")
        
        return result
    
    def _calculate_signal(self, data: MarginData) -> MarginData:
        """计算融资融券信号"""
        score = 0.0
        descriptions = []
        
        # 1. 融资余额变化率信号 (权重50%)
        if data.fin_change_rate >= self.THRESHOLDS["fin_change_bullish"]:
            score += 50
            descriptions.append(f"融资增长{data.fin_change_rate:.1f}%,资金入场")
        elif data.fin_change_rate <= self.THRESHOLDS["fin_change_bearish"]:
            score -= 50
            descriptions.append(f"融资下降{abs(data.fin_change_rate):.1f}%,资金离场")
        else:
            score += (data.fin_change_rate / 2) * 25
        
        # 2. 融资/融券比例信号 (权重30%)
        if data.fin_sec_ratio >= self.THRESHOLDS["fin_sec_ratio_high"]:
            # 极度乐观可能过热
            score += 15
            descriptions.append("融资/融券比例极高,市场乐观")
        elif data.fin_sec_ratio <= self.THRESHOLDS["fin_sec_ratio_low"]:
            score -= 15
            descriptions.append("融资/融券比例偏低")
        else:
            score += ((data.fin_sec_ratio - 30) / 20) * 15
        
        # 3. 融资余额绝对水平 (权重20%)
        # 这里简化处理，实际应该对比历史分位数
        if data.fin_balance > 15000:  # 超过1.5万亿
            score += 10
        elif data.fin_balance < 10000:  # 低于1万亿
            score -= 10
        
        data.signal_score = max(-100, min(100, score))
        data.signal_description = "; ".join(descriptions) if descriptions else "两融中性"
        
        return data


# =============================================================================
# 市场宽度分析器
# =============================================================================

class MarketBreadthAnalyzer:
    """
    市场宽度分析器
    
    数据源: JQData get_price (涨跌停价、成交量)
    
    指标:
    - 涨停/跌停家数比 > 3:1 看多
    - 新高/新低家数比 > 5:1 看多
    - 均线多头占比 > 60% 看多
    - 市场换手率 1.5%-3% 正常, >5% 过热
    """
    
    THRESHOLDS = {
        "limit_up_down_bullish": 3.0,    # 涨跌停比看多
        "limit_up_down_bearish": 0.33,   # 涨跌停比看空
        "new_high_low_bullish": 5.0,     # 新高新低比看多
        "ma_bullish_high": 60.0,         # 均线多头占比看多(%)
        "ma_bullish_low": 40.0,          # 均线多头占比看空(%)
        "turnover_normal_low": 1.5,      # 正常换手率下限(%)
        "turnover_normal_high": 3.0,     # 正常换手率上限(%)
        "turnover_overheat": 5.0,        # 过热换手率(%)
    }
    
    def __init__(self, jq_client=None):
        self.jq_client = jq_client
        self._cache: Dict[str, MarketBreadthData] = {}
    
    def analyze(self, target_date: Optional[str] = None) -> MarketBreadthData:
        """分析市场宽度"""
        if target_date is None:
            target_date = date.today().strftime('%Y-%m-%d')
        
        if target_date in self._cache:
            return self._cache[target_date]
        
        result = MarketBreadthData(date=target_date)
        
        try:
            if self.jq_client and self.jq_client.is_authenticated():
                result = self._fetch_from_jqdata(target_date)
            else:
                result = self._fetch_from_akshare(target_date)
            
            result = self._calculate_signal(result)
            self._cache[target_date] = result
            
        except Exception as e:
            logger.error(f"市场宽度分析失败: {e}")
            result.signal_description = f"数据获取失败: {str(e)}"
        
        return result
    
    def _fetch_from_jqdata(self, target_date: str) -> MarketBreadthData:
        """
        从JQData获取市场宽度数据
        
        注意: 如果查询当天数据且市场未收盘，可能返回空数据
        此时会自动回退到前一交易日或使用AKShare
        """
        import jqdatasdk as jq
        
        result = MarketBreadthData(date=target_date)
        
        try:
            # 获取所有A股
            all_stocks = jq.get_all_securities(types=['stock'], date=target_date)
            if all_stocks is None or all_stocks.empty:
                logger.warning("无法获取股票列表")
                return self._fetch_from_akshare(target_date)
            
            stock_list = all_stocks.index.tolist()
            
            # 先尝试获取目标日期，如果失败则尝试前一交易日
            dates_to_try = [target_date]
            trade_days = jq.get_trade_days(
                start_date=(datetime.strptime(target_date, '%Y-%m-%d') - timedelta(days=10)).strftime('%Y-%m-%d'),
                end_date=target_date
            )
            if len(trade_days) > 1:
                dates_to_try.append(trade_days[-2].strftime('%Y-%m-%d'))
            
            df = None
            actual_date = target_date
            
            for try_date in dates_to_try:
                # 分批获取以避免超时 (每批500只)
                batch_size = 500
                all_data = []
                
                for i in range(0, min(len(stock_list), 2000), batch_size):  # 限制最多2000只
                    batch = stock_list[i:i+batch_size]
                    try:
                        batch_df = jq.get_price(
                            batch,
                            start_date=try_date,
                            end_date=try_date,
                            frequency='daily',
                            fields=['close', 'high_limit', 'low_limit', 'pre_close', 'volume', 'money'],
                            skip_paused=True
                        )
                        if batch_df is not None and not batch_df.empty:
                            all_data.append(batch_df)
                    except Exception as e:
                        logger.debug(f"批次{i}获取失败: {e}")
                        continue
                
                if all_data:
                    df = pd.concat(all_data)
                    actual_date = try_date
                    break
                else:
                    logger.debug(f"{try_date} 无数据，尝试前一交易日")
            
            if df is None or df.empty:
                logger.warning("JQData未返回市场宽度数据，使用AKShare")
                return self._fetch_from_akshare(target_date)
            
            result.date = actual_date
            
            # 统计涨跌停
            if 'high_limit' in df.columns and 'close' in df.columns:
                # 涨停: 收盘价 >= 涨停价 * 0.999 (允许小误差)
                limit_up = df[df['close'] >= df['high_limit'] * 0.999]
                limit_down = df[df['close'] <= df['low_limit'] * 1.001]
                
                result.limit_up_count = len(limit_up)
                result.limit_down_count = len(limit_down)
                
                if result.limit_down_count > 0:
                    result.limit_up_down_ratio = result.limit_up_count / result.limit_down_count
                else:
                    result.limit_up_down_ratio = result.limit_up_count if result.limit_up_count > 0 else 1.0
            
            # 统计涨跌家数
            if 'close' in df.columns and 'pre_close' in df.columns:
                df_change = df.copy()
                df_change['change'] = df_change['close'] - df_change['pre_close']
                result.up_count = len(df_change[df_change['change'] > 0])
                result.down_count = len(df_change[df_change['change'] < 0])
                result.flat_count = len(df_change[df_change['change'] == 0])
                
                if result.down_count > 0:
                    result.up_down_ratio = result.up_count / result.down_count
                else:
                    result.up_down_ratio = result.up_count if result.up_count > 0 else 1.0
            
            # 计算换手率 (简化: 使用成交金额/总市值估算)
            if 'money' in df.columns:
                total_money = df['money'].sum() / 100000000  # 亿元
                # 假设A股总市值约80万亿
                result.avg_turnover_rate = (total_money / 800000) * 100
            
            logger.info(f"JQData市场宽度({actual_date}): 涨停{result.limit_up_count}家, 跌停{result.limit_down_count}家, 涨{result.up_count}/跌{result.down_count}")
            
            # 计算均线多头占比 (需要更多历史数据)
            result = self._calculate_ma_breadth(result, actual_date)
            
        except Exception as e:
            logger.warning(f"JQData获取市场宽度失败: {e}")
            import traceback
            traceback.print_exc()
            return self._fetch_from_akshare(target_date)
        
        return result
    
    def _calculate_ma_breadth(self, result: MarketBreadthData, target_date: str) -> MarketBreadthData:
        """计算均线多头占比 (简化版)"""
        # 这个计算比较耗时，这里只做简单估算
        # 实际应该遍历所有股票计算MA5 > MA20 > MA60的比例
        
        # 根据涨跌比例估算均线多头占比
        if result.up_down_ratio > 2:
            result.ma_bullish_ratio = 65.0
        elif result.up_down_ratio > 1:
            result.ma_bullish_ratio = 55.0
        elif result.up_down_ratio > 0.5:
            result.ma_bullish_ratio = 45.0
        else:
            result.ma_bullish_ratio = 35.0
        
        return result
    
    def _fetch_from_akshare(self, target_date: str) -> MarketBreadthData:
        """
        从AKShare获取市场宽度数据
        
        使用涨停池和跌停池接口获取涨跌停统计
        """
        result = MarketBreadthData(date=target_date)
        
        try:
            import akshare as ak
            
            # 尝试获取目标日期的涨停池
            date_str = target_date.replace('-', '')
            
            # 获取涨停池
            try:
                df_up = ak.stock_zt_pool_em(date=date_str)
                if df_up is not None and not df_up.empty:
                    result.limit_up_count = len(df_up)
                    logger.debug(f"AKShare涨停池: {result.limit_up_count}只")
            except Exception as e:
                logger.debug(f"获取涨停池失败: {e}")
            
            # 获取跌停池 (stock_zt_pool_dtgc_em 是跌停股池)
            try:
                df_down = ak.stock_zt_pool_dtgc_em(date=date_str)
                if df_down is not None and not df_down.empty:
                    result.limit_down_count = len(df_down)
                    logger.debug(f"AKShare跌停池: {result.limit_down_count}只")
            except Exception as e:
                logger.debug(f"获取跌停池失败: {e}")
            
            # 计算涨跌停比
            if result.limit_down_count > 0:
                result.limit_up_down_ratio = result.limit_up_count / result.limit_down_count
            elif result.limit_up_count > 0:
                result.limit_up_down_ratio = float(result.limit_up_count)
            else:
                result.limit_up_down_ratio = 1.0
            
            # 尝试获取市场涨跌统计
            try:
                # 获取大盘涨跌统计
                df_market = ak.stock_market_activity_legu()
                if df_market is not None and not df_market.empty:
                    # 查找上涨家数和下跌家数
                    for _, row in df_market.iterrows():
                        item = str(row.get('item', ''))
                        value = row.get('value', 0)
                        if '上涨' in item:
                            result.up_count = int(value) if value else 0
                        elif '下跌' in item:
                            result.down_count = int(value) if value else 0
                        elif '平盘' in item:
                            result.flat_count = int(value) if value else 0
                    
                    if result.down_count > 0:
                        result.up_down_ratio = result.up_count / result.down_count
            except Exception as e:
                logger.debug(f"获取市场涨跌统计失败: {e}")
            
            logger.info(f"AKShare市场宽度: 涨停{result.limit_up_count}家, 跌停{result.limit_down_count}家")
            
        except Exception as e:
            logger.error(f"AKShare获取市场宽度失败: {e}")
            import traceback
            traceback.print_exc()
        
        return result
    
    def _calculate_signal(self, data: MarketBreadthData) -> MarketBreadthData:
        """计算市场宽度信号"""
        score = 0.0
        descriptions = []
        
        # 1. 涨跌停比信号 (权重35%)
        if data.limit_up_down_ratio >= self.THRESHOLDS["limit_up_down_bullish"]:
            score += 35
            descriptions.append(f"涨跌停比{data.limit_up_down_ratio:.1f}:1,市场强势")
        elif data.limit_up_down_ratio <= self.THRESHOLDS["limit_up_down_bearish"]:
            score -= 35
            descriptions.append(f"跌停多于涨停,市场弱势")
        else:
            # 线性插值
            ratio_score = (data.limit_up_down_ratio - 1) / 2 * 17.5
            score += ratio_score
        
        # 2. 涨跌家数比信号 (权重25%)
        if data.up_down_ratio > 2:
            score += 25
            descriptions.append("普涨格局")
        elif data.up_down_ratio < 0.5:
            score -= 25
            descriptions.append("普跌格局")
        else:
            score += (data.up_down_ratio - 1) * 12.5
        
        # 3. 均线多头占比信号 (权重25%)
        if data.ma_bullish_ratio >= self.THRESHOLDS["ma_bullish_high"]:
            score += 25
            descriptions.append(f"均线多头{data.ma_bullish_ratio:.0f}%,趋势向好")
        elif data.ma_bullish_ratio <= self.THRESHOLDS["ma_bullish_low"]:
            score -= 25
            descriptions.append(f"均线空头居多,趋势转弱")
        else:
            score += ((data.ma_bullish_ratio - 50) / 10) * 12.5
        
        # 4. 换手率信号 (权重15%)
        if data.avg_turnover_rate >= self.THRESHOLDS["turnover_overheat"]:
            # 过热,可能见顶
            score -= 15
            descriptions.append(f"换手率{data.avg_turnover_rate:.1f}%过热")
        elif data.avg_turnover_rate < self.THRESHOLDS["turnover_normal_low"]:
            # 地量,可能筑底
            score += 10
            descriptions.append("成交低迷,可能筑底")
        else:
            # 正常范围
            score += 5
        
        data.signal_score = max(-100, min(100, score))
        data.signal_description = "; ".join(descriptions) if descriptions else "市场宽度中性"
        
        return data


# =============================================================================
# 综合指标聚合器
# =============================================================================

class AStockIndicatorAggregator:
    """
    A股特色指标综合聚合器
    
    整合北向资金、融资融券、市场宽度三大类指标，
    计算综合评分并给出投资建议。
    
    权重分配:
    - 北向资金: 35%
    - 融资融券: 25%
    - 市场宽度: 40%
    """
    
    WEIGHTS = {
        "north_fund": 0.35,
        "margin": 0.25,
        "market_breadth": 0.40,
    }
    
    def __init__(self, jq_client=None):
        self.jq_client = jq_client
        self.north_fund_analyzer = NorthFundAnalyzer(jq_client)
        self.margin_analyzer = MarginAnalyzer(jq_client)
        self.market_breadth_analyzer = MarketBreadthAnalyzer(jq_client)
    
    def analyze(self, target_date: Optional[str] = None) -> AStockIndicatorResult:
        """
        综合分析A股特色指标
        
        Args:
            target_date: 目标日期
        
        Returns:
            AStockIndicatorResult: 综合分析结果
        """
        if target_date is None:
            target_date = date.today().strftime('%Y-%m-%d')
        
        result = AStockIndicatorResult(date=target_date)
        
        try:
            # 获取各指标数据
            result.north_fund = self.north_fund_analyzer.analyze(target_date)
            result.margin = self.margin_analyzer.analyze(target_date)
            result.market_breadth = self.market_breadth_analyzer.analyze(target_date)
            
            # 计算综合得分
            scores = {
                "north_fund": result.north_fund.signal_score if result.north_fund else 0,
                "margin": result.margin.signal_score if result.margin else 0,
                "market_breadth": result.market_breadth.signal_score if result.market_breadth else 0,
            }
            
            result.composite_score = sum(
                scores[k] * self.WEIGHTS[k] for k in scores
            )
            
            # 判断信号级别
            if result.composite_score >= 30:
                result.signal_level = "bullish"
                result.recommendation = "A股资金面和情绪面向好，可适当加仓"
            elif result.composite_score <= -30:
                result.signal_level = "bearish"
                result.recommendation = "A股资金面和情绪面转弱，建议减仓观望"
            else:
                result.signal_level = "neutral"
                result.recommendation = "A股资金面中性，维持现有仓位"
            
            result.success = True
            result.data_source = "jqdata" if self.jq_client else "akshare"
            
            logger.info(f"A股综合指标: 得分={result.composite_score:.1f}, 信号={result.signal_level}")
            
        except Exception as e:
            result.success = False
            result.error_message = str(e)
            logger.error(f"A股综合指标分析失败: {e}")
        
        return result
    
    def get_history(
        self, 
        start_date: str, 
        end_date: str,
        include_details: bool = False
    ) -> pd.DataFrame:
        """
        获取历史A股特色指标数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            include_details: 是否包含详细数据
        
        Returns:
            DataFrame: 历史数据
        """
        import jqdatasdk as jq
        
        # 获取交易日列表
        trade_days = jq.get_trade_days(start_date, end_date)
        
        records = []
        for day in trade_days:
            day_str = day.strftime('%Y-%m-%d')
            try:
                result = self.analyze(day_str)
                record = {
                    "date": day_str,
                    "composite_score": result.composite_score,
                    "signal_level": result.signal_level,
                    "north_fund_score": result.north_fund.signal_score if result.north_fund else 0,
                    "margin_score": result.margin.signal_score if result.margin else 0,
                    "breadth_score": result.market_breadth.signal_score if result.market_breadth else 0,
                }
                
                if include_details and result.north_fund:
                    record["north_fund_5d"] = result.north_fund.net_buy_5d
                    record["north_fund_daily"] = result.north_fund.net_buy_amount
                
                if include_details and result.margin:
                    record["fin_balance"] = result.margin.fin_balance
                    record["fin_change_rate"] = result.margin.fin_change_rate
                
                if include_details and result.market_breadth:
                    record["limit_up_count"] = result.market_breadth.limit_up_count
                    record["limit_down_count"] = result.market_breadth.limit_down_count
                    record["up_down_ratio"] = result.market_breadth.up_down_ratio
                
                records.append(record)
                
            except Exception as e:
                logger.debug(f"获取{day_str}数据失败: {e}")
                continue
        
        return pd.DataFrame(records)


# =============================================================================
# 便捷函数
# =============================================================================

def get_astock_indicators(
    jq_client=None, 
    target_date: Optional[str] = None
) -> AStockIndicatorResult:
    """
    获取A股特色指标的便捷函数
    
    Args:
        jq_client: JQData客户端
        target_date: 目标日期
    
    Returns:
        AStockIndicatorResult
    """
    aggregator = AStockIndicatorAggregator(jq_client)
    return aggregator.analyze(target_date)


def get_north_fund(
    jq_client=None,
    target_date: Optional[str] = None
) -> NorthFundData:
    """获取北向资金数据"""
    analyzer = NorthFundAnalyzer(jq_client)
    return analyzer.analyze(target_date)


def get_margin_data(
    jq_client=None,
    target_date: Optional[str] = None
) -> MarginData:
    """获取融资融券数据"""
    analyzer = MarginAnalyzer(jq_client)
    return analyzer.analyze(target_date)


def get_market_breadth(
    jq_client=None,
    target_date: Optional[str] = None
) -> MarketBreadthData:
    """获取市场宽度数据"""
    analyzer = MarketBreadthAnalyzer(jq_client)
    return analyzer.analyze(target_date)

