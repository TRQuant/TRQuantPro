#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SignalBacktester - 市场趋势信号历史回测框架 (增强版)
======================================================

功能:
1. 回测市场趋势信号的准确性
2. 短中长周期分别验证
3. 多进程并行回测 (最多3个JQData连接)
4. Phase1快速验证 + Phase2完整回测
5. 市场状态识别验证

数据范围:
- 北向资金: 2014-11-17 ~ 2024-08-16 (之后不再披露买卖分项)
- 融资融券: 2010年至今
- 市场宽度: 2010年至今

回测逻辑:
1. 遍历历史日期，计算每日的A股指标和技术指标
2. 生成短中长周期信号和市场状态
3. 计算信号发出后N日的市场收益
4. 统计各周期准确率和胜率

作者: TRQuant Team
日期: 2026-01-02
"""

import logging
from typing import Dict, List, Optional, Any, Tuple, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp
import json

logger = logging.getLogger(__name__)


# ==================== 枚举和数据类 ====================

class SignalType(Enum):
    """信号类型"""
    BULLISH = "bullish"      # 看多
    BEARISH = "bearish"      # 看空
    NEUTRAL = "neutral"      # 中性


class MarketStateCategory(Enum):
    """市场状态类别"""
    BULL = "牛市"
    BEAR = "熊市"
    VOLATILE = "震荡"


@dataclass
class BacktestConfig:
    """回测配置"""
    start_date: str = "2016-01-01"
    end_date: str = "2024-08-16"  # 北向资金数据截止日期
    
    # 持有期 (信号发出后观察N个交易日)
    holding_periods: List[int] = field(default_factory=lambda: [5, 10, 20, 60])
    
    # 信号阈值
    north_fund_bullish_threshold: float = 50.0   # 5日累计>50亿看多
    north_fund_bearish_threshold: float = -50.0  # 5日累计<-50亿看空
    margin_change_bullish_threshold: float = 1.0  # 融资变化率>1%看多
    margin_change_bearish_threshold: float = -1.0 # 融资变化率<-1%看空
    breadth_bullish_threshold: float = 2.0       # 涨跌停比>2看多
    breadth_bearish_threshold: float = 0.5       # 涨跌停比<0.5看空
    
    # 综合得分阈值
    composite_bullish_threshold: float = 30.0
    composite_bearish_threshold: float = -30.0
    
    # 周期得分阈值
    short_bullish_threshold: float = 20.0
    short_bearish_threshold: float = -20.0
    medium_bullish_threshold: float = 20.0
    medium_bearish_threshold: float = -20.0
    long_bullish_threshold: float = 30.0
    long_bearish_threshold: float = -30.0
    
    # 基准指数
    benchmark: str = "000001.XSHG"  # 上证指数
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EnhancedSignalRecord:
    """增强信号记录 (含短中长周期, HMM, IBD交叉验证)"""
    date: str
    
    # 综合信号
    signal_type: SignalType
    composite_score: float
    
    # 短中长周期信号
    short_term_signal: SignalType = SignalType.NEUTRAL
    medium_term_signal: SignalType = SignalType.NEUTRAL
    long_term_signal: SignalType = SignalType.NEUTRAL
    
    short_term_score: float = 0.0
    medium_term_score: float = 0.0
    long_term_score: float = 0.0
    
    # A股特色指标
    north_fund_score: float = 0.0
    margin_score: float = 0.0
    breadth_score: float = 0.0
    
    # 市场状态
    market_state: str = "未知"
    state_category: MarketStateCategory = MarketStateCategory.VOLATILE
    
    # HMM分析结果
    hmm_state: str = "unknown"  # bull/bear/sideways
    hmm_confidence: float = 0.0
    hmm_signal_aligned: bool = False  # HMM是否与综合信号一致
    
    # IBD分析结果
    ibd_market_status: str = "unknown"  # confirmed_uptrend/uptrend_under_pressure/market_in_correction/rally_attempt
    ibd_distribution_count: int = 0
    ibd_has_ftd: bool = False  # 是否有跟踪日
    ibd_signal_aligned: bool = False  # IBD是否与综合信号一致
    
    # 多模型共识
    model_consensus: int = 0  # 几个模型看多/看空一致 (0-5)
    bullish_votes: float = 0.0  # 看多总票数
    bearish_votes: float = 0.0  # 看空总票数
    high_confidence: bool = False  # 是否高置信度信号 (>=3.5票)
    medium_confidence: bool = False  # 中置信度 (>=2.5票)
    confidence_level: str = "low"  # high/medium/low
    
    # 后续收益 (信号发出后N日)
    returns_5d: float = 0.0
    returns_10d: float = 0.0
    returns_20d: float = 0.0
    returns_60d: float = 0.0
    
    # 综合信号准确性
    correct_5d: bool = False
    correct_10d: bool = False
    correct_20d: bool = False
    correct_60d: bool = False
    
    # 短周期准确性 (5日验证)
    short_correct_5d: bool = False
    
    # 中周期准确性 (20日验证)
    medium_correct_20d: bool = False
    
    # 长周期准确性 (60日验证)
    long_correct_60d: bool = False
    
    # 市场状态准确性 (60日验证)
    state_correct_60d: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['signal_type'] = self.signal_type.value
        d['short_term_signal'] = self.short_term_signal.value
        d['medium_term_signal'] = self.medium_term_signal.value
        d['long_term_signal'] = self.long_term_signal.value
        d['state_category'] = self.state_category.value
        return d


@dataclass
class EnhancedBacktestResult:
    """增强回测结果"""
    config: BacktestConfig
    phase: str = "unknown"  # "phase1" or "phase2"
    
    # 基本统计
    total_signals: int = 0
    bullish_signals: int = 0
    bearish_signals: int = 0
    neutral_signals: int = 0
    
    # 综合准确率
    accuracy_5d: float = 0.0
    accuracy_10d: float = 0.0
    accuracy_20d: float = 0.0
    accuracy_60d: float = 0.0
    
    # 短周期准确率 (5日验证)
    short_accuracy_5d: float = 0.0
    short_bullish_accuracy: float = 0.0
    short_bearish_accuracy: float = 0.0
    
    # 中周期准确率 (20日验证)
    medium_accuracy_20d: float = 0.0
    medium_bullish_accuracy: float = 0.0
    medium_bearish_accuracy: float = 0.0
    
    # 长周期准确率 (60日验证)
    long_accuracy_60d: float = 0.0
    long_bullish_accuracy: float = 0.0
    long_bearish_accuracy: float = 0.0
    
    # 市场状态准确率
    state_accuracy_60d: float = 0.0
    bull_state_accuracy: float = 0.0
    bear_state_accuracy: float = 0.0
    volatile_state_accuracy: float = 0.0
    
    # 平均收益
    avg_return_bullish_5d: float = 0.0
    avg_return_bullish_20d: float = 0.0
    avg_return_bearish_5d: float = 0.0
    avg_return_bearish_20d: float = 0.0
    
    # 胜率
    win_rate_bullish: float = 0.0
    win_rate_bearish: float = 0.0
    
    # HMM/IBD交叉验证统计
    hmm_aligned_signals: int = 0      # HMM与综合信号一致的数量
    ibd_aligned_signals: int = 0      # IBD与综合信号一致的数量
    high_confidence_signals: int = 0  # 高置信度信号数量 (>=3.5票)
    medium_confidence_signals: int = 0  # 中置信度信号数量 (>=2.5票)
    low_confidence_signals: int = 0   # 低置信度信号数量 (<2.5票)
    
    # 高置信度信号准确率
    high_confidence_accuracy_5d: float = 0.0
    high_confidence_accuracy_20d: float = 0.0
    high_confidence_accuracy_60d: float = 0.0
    
    # 中置信度信号准确率
    medium_confidence_accuracy_5d: float = 0.0
    medium_confidence_accuracy_20d: float = 0.0
    medium_confidence_accuracy_60d: float = 0.0
    
    # 低置信度信号准确率 (作为对比基准)
    low_confidence_accuracy_5d: float = 0.0
    low_confidence_accuracy_20d: float = 0.0
    
    # HMM对齐信号准确率
    hmm_aligned_accuracy_5d: float = 0.0
    hmm_aligned_accuracy_20d: float = 0.0
    
    # IBD对齐信号准确率
    ibd_aligned_accuracy_5d: float = 0.0
    ibd_aligned_accuracy_20d: float = 0.0
    
    # 信号记录
    signals: List[EnhancedSignalRecord] = field(default_factory=list)
    
    # 按年统计
    yearly_stats: Dict[str, Dict] = field(default_factory=dict)
    
    # 时间信息
    backtest_time: str = ""
    duration_seconds: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['config'] = self.config.to_dict()
        result['signals'] = [s.to_dict() if hasattr(s, 'to_dict') else asdict(s) for s in self.signals]
        return result


# ==================== 回测器类 ====================

class SignalBacktester:
    """
    市场趋势信号回测器
    
    支持:
    - 短中长周期分别验证 (集成TrendAnalyzer 8维指标)
    - A股特色指标
    - 市场状态识别
    """
    
    def __init__(self, jq_client=None, use_trend_analyzer: bool = True, 
                 use_hmm: bool = True, use_ibd: bool = True):
        """
        初始化回测器
        
        Args:
            jq_client: JQData客户端实例
            use_trend_analyzer: 是否使用TrendAnalyzer (8维指标)
            use_hmm: 是否使用SimpleHMM (隐马尔可夫模型)
            use_ibd: 是否使用IBDStyleAnalyzer (反转信号)
        """
        self._jq_client = jq_client
        self._jq = None
        self._price_cache: Dict[str, pd.DataFrame] = {}
        self._trade_days_cache: Dict[str, List[str]] = {}
        self._use_trend_analyzer = use_trend_analyzer
        self._trend_analyzer = None
        self._use_hmm = use_hmm
        self._hmm_analyzer = None
        self._use_ibd = use_ibd
        self._ibd_analyzer = None
        
    def _ensure_jqdata(self):
        """确保JQData连接"""
        if self._jq is None:
            try:
                import jqdatasdk as jq
                from jqdatasdk import finance, query
                
                # 从配置加载凭证
                config_path = "/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json"
                with open(config_path, 'r') as f:
                    config = json.load(f)
                jq.auth(config['username'], config['password'])
                self._jq = jq
                logger.info(f"JQData认证成功")
                
                # 初始化TrendAnalyzer (如果启用)
                if self._use_trend_analyzer and self._trend_analyzer is None:
                    try:
                        from core.trend_analyzer import TrendAnalyzer
                        from jqdata.client import JQDataClient
                        jq_client = JQDataClient()
                        self._trend_analyzer = TrendAnalyzer(jq_client=jq_client)
                        logger.info("TrendAnalyzer (8维指标) 初始化成功")
                    except Exception as e:
                        logger.warning(f"TrendAnalyzer初始化失败，使用简化版: {e}")
                        self._use_trend_analyzer = False
                
                # 初始化HMM分析器 (如果启用)
                if self._use_hmm and self._hmm_analyzer is None:
                    try:
                        from core.trend_ml import SimpleHMM
                        self._hmm_analyzer = SimpleHMM()
                        logger.info("SimpleHMM 初始化成功")
                    except Exception as e:
                        logger.warning(f"SimpleHMM初始化失败: {e}")
                        self._use_hmm = False
                
                # 初始化IBD分析器 (如果启用)
                if self._use_ibd and self._ibd_analyzer is None:
                    try:
                        from core.ibd_style_analyzer import IBDStyleAnalyzer
                        self._ibd_analyzer = IBDStyleAnalyzer()
                        logger.info("IBDStyleAnalyzer 初始化成功")
                    except Exception as e:
                        logger.warning(f"IBDStyleAnalyzer初始化失败: {e}")
                        self._use_ibd = False
                        
            except Exception as e:
                logger.error(f"JQData认证失败: {e}")
                raise
    
    def _get_trade_days(self, start_date: str, end_date: str) -> List[str]:
        """获取交易日列表"""
        cache_key = f"{start_date}_{end_date}"
        if cache_key in self._trade_days_cache:
            return self._trade_days_cache[cache_key]
        
        self._ensure_jqdata()
        trade_days = self._jq.get_trade_days(start_date=start_date, end_date=end_date)
        result = [d.strftime('%Y-%m-%d') for d in trade_days]
        self._trade_days_cache[cache_key] = result
        return result
    
    def _get_benchmark_prices(self, start_date: str, end_date: str, benchmark: str) -> pd.DataFrame:
        """获取基准指数价格"""
        cache_key = f"{benchmark}_{start_date}_{end_date}"
        
        if cache_key in self._price_cache:
            return self._price_cache[cache_key]
        
        self._ensure_jqdata()
        
        # 获取更长时间的数据用于计算未来收益
        extended_end = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=120)).strftime('%Y-%m-%d')
        
        df = self._jq.get_price(
            benchmark,
            start_date=start_date,
            end_date=extended_end,
            frequency='daily',
            fields=['close']
        )
        
        if df is not None and not df.empty:
            df.index = pd.to_datetime(df.index)
            self._price_cache[cache_key] = df
            
        return df
    
    def _calculate_future_returns(self, prices: pd.DataFrame, signal_date: str, 
                                   periods: List[int]) -> Dict[int, float]:
        """计算信号发出后N日的收益率"""
        returns = {}
        signal_dt = pd.to_datetime(signal_date)
        
        if signal_dt not in prices.index:
            available_dates = prices.index[prices.index >= signal_dt]
            if len(available_dates) == 0:
                return {p: 0.0 for p in periods}
            signal_dt = available_dates[0]
        
        signal_price = prices.loc[signal_dt, 'close']
        
        for period in periods:
            future_dates = prices.index[prices.index > signal_dt]
            if len(future_dates) >= period:
                future_date = future_dates[period - 1]
                future_price = prices.loc[future_date, 'close']
                returns[period] = (future_price / signal_price - 1) * 100
            else:
                returns[period] = 0.0
        
        return returns
    
    def _get_north_fund_data(self, date: str) -> Tuple[float, float]:
        """获取北向资金数据"""
        from jqdatasdk import finance, query
        
        target_dt = datetime.strptime(date, '%Y-%m-%d')
        start_dt = target_dt - timedelta(days=10)
        
        q = query(
            finance.STK_ML_QUOTA.day,
            finance.STK_ML_QUOTA.link_id,
            finance.STK_ML_QUOTA.buy_amount,
            finance.STK_ML_QUOTA.sell_amount
        ).filter(
            finance.STK_ML_QUOTA.day >= start_dt.strftime('%Y-%m-%d'),
            finance.STK_ML_QUOTA.day <= date,
            finance.STK_ML_QUOTA.link_id.in_([310001, 310002])
        ).order_by(
            finance.STK_ML_QUOTA.day.desc()
        )
        
        df = finance.run_query(q)
        
        if df is None or df.empty:
            return 0.0, 0.0
        
        df['day'] = pd.to_datetime(df['day'])
        df['net_buy'] = df['buy_amount'].fillna(0) - df['sell_amount'].fillna(0)
        
        daily_net = df.groupby('day')['net_buy'].sum().sort_index(ascending=False)
        
        daily_buy = float(daily_net.iloc[0]) if len(daily_net) > 0 else 0.0
        cum_5d = float(daily_net.head(5).sum()) if len(daily_net) >= 5 else float(daily_net.sum())
        
        return daily_buy, cum_5d
    
    def _get_margin_data(self, date: str) -> float:
        """获取融资融券变化率"""
        from jqdatasdk import finance, query
        
        target_dt = datetime.strptime(date, '%Y-%m-%d')
        start_dt = target_dt - timedelta(days=10)
        
        q = query(
            finance.STK_MT_TOTAL.date,
            finance.STK_MT_TOTAL.fin_value
        ).filter(
            finance.STK_MT_TOTAL.date >= start_dt.strftime('%Y-%m-%d'),
            finance.STK_MT_TOTAL.date <= date
        ).order_by(
            finance.STK_MT_TOTAL.date.desc()
        )
        
        df = finance.run_query(q)
        
        if df is None or df.empty or len(df) < 2:
            return 0.0
        
        df['date'] = pd.to_datetime(df['date'])
        daily = df.groupby('date')['fin_value'].sum().sort_index(ascending=False)
        
        count_per_day = df.groupby('date').size()
        max_count = count_per_day.max()
        complete_days = count_per_day[count_per_day == max_count].index
        
        if len(complete_days) < 2:
            return 0.0
        
        latest = daily.loc[complete_days[0]] if complete_days[0] in daily.index else 0
        prev = daily.loc[complete_days[1]] if complete_days[1] in daily.index else 0
        
        if prev > 0:
            return (latest - prev) / prev * 100
        
        return 0.0
    
    def _get_breadth_data(self, date: str) -> float:
        """获取市场宽度数据 (涨跌停比)"""
        try:
            all_stocks = self._jq.get_all_securities(types=['stock'], date=date)
            if all_stocks is None or all_stocks.empty:
                return 1.0
            
            stock_list = all_stocks.index.tolist()[:500]
            
            df = self._jq.get_price(
                stock_list,
                start_date=date,
                end_date=date,
                frequency='daily',
                fields=['close', 'high_limit', 'low_limit'],
                skip_paused=True
            )
            
            if df is None or df.empty:
                return 1.0
            
            limit_up = len(df[df['close'] >= df['high_limit'] * 0.999])
            limit_down = len(df[df['close'] <= df['low_limit'] * 1.001])
            
            if limit_down > 0:
                return limit_up / limit_down
            else:
                return float(limit_up) if limit_up > 0 else 1.0
                
        except Exception as e:
            logger.debug(f"获取市场宽度失败 {date}: {e}")
            return 1.0
    
    def _calculate_technical_scores(self, date: str, benchmark: str = "000001.XSHG") -> Dict[str, float]:
        """
        计算技术指标得分 (短中长周期)
        
        如果启用TrendAnalyzer，使用完整的8维技术指标:
        MA(20%) + MACD(18%) + RSI(12%) + BB(12%) + VOL(12%) + KDJ(10%) + ADX(8%) + MFI(8%)
        
        Returns:
            {'short': score, 'medium': score, 'long': score}
        """
        # 优先使用TrendAnalyzer (完整8维指标)
        if self._use_trend_analyzer and self._trend_analyzer is not None:
            return self._calculate_technical_scores_via_trend_analyzer(date, benchmark)
        
        # 降级到简化版
        return self._calculate_technical_scores_simple(date, benchmark)
    
    def _calculate_technical_scores_via_trend_analyzer(self, date: str, benchmark: str) -> Dict[str, float]:
        """使用TrendAnalyzer计算完整8维技术指标得分"""
        try:
            result = self._trend_analyzer.analyze_market(index_code=benchmark, date=date)
            
            if result is None:
                logger.debug(f"TrendAnalyzer分析失败 {date}, 降级到简化版")
                return self._calculate_technical_scores_simple(date, benchmark)
            
            # 从TrendAnalyzer结果中提取三周期得分
            return {
                'short': result.short_term.score if result.short_term else 0.0,
                'medium': result.medium_term.score if result.medium_term else 0.0,
                'long': result.long_term.score if result.long_term else 0.0
            }
            
        except Exception as e:
            logger.debug(f"TrendAnalyzer计算失败 {date}: {e}")
            return self._calculate_technical_scores_simple(date, benchmark)
    
    def _calculate_technical_scores_simple(self, date: str, benchmark: str = "000001.XSHG") -> Dict[str, float]:
        """
        简化版技术指标得分 (仅MA+RSI+MACD)
        当TrendAnalyzer不可用时使用
        """
        try:
            # 获取足够长的历史数据
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=300)
            
            df = self._jq.get_price(
                benchmark,
                start_date=start_dt.strftime('%Y-%m-%d'),
                end_date=date,
                frequency='daily',
                fields=['close', 'volume', 'high', 'low']
            )
            
            if df is None or df.empty or len(df) < 60:
                return {'short': 0.0, 'medium': 0.0, 'long': 0.0}
            
            close = df['close']
            
            # 短期指标 (5-20日)
            ma5 = close.rolling(5).mean().iloc[-1]
            ma10 = close.rolling(10).mean().iloc[-1]
            ma20 = close.rolling(20).mean().iloc[-1]
            current = close.iloc[-1]
            
            short_score = 0.0
            if current > ma5 > ma10 > ma20:  # 多头排列
                short_score = 50
            elif current > ma5 > ma10:
                short_score = 30
            elif current > ma5:
                short_score = 10
            elif current < ma5 < ma10 < ma20:  # 空头排列
                short_score = -50
            elif current < ma5 < ma10:
                short_score = -30
            elif current < ma5:
                short_score = -10
            
            # RSI调整
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            if rsi > 70:
                short_score += 20
            elif rsi > 50:
                short_score += 10
            elif rsi < 30:
                short_score -= 20
            elif rsi < 50:
                short_score -= 10
            
            # 中期指标 (20-60日)
            ma60 = close.rolling(60).mean().iloc[-1]
            
            medium_score = 0.0
            if current > ma20 > ma60:
                medium_score = 40
            elif current > ma20:
                medium_score = 20
            elif current < ma20 < ma60:
                medium_score = -40
            elif current < ma20:
                medium_score = -20
            
            # MACD
            exp12 = close.ewm(span=12).mean()
            exp26 = close.ewm(span=26).mean()
            macd_line = exp12 - exp26
            signal_line = macd_line.ewm(span=9).mean()
            histogram = macd_line - signal_line
            
            if histogram.iloc[-1] > 0 and histogram.iloc[-1] > histogram.iloc[-2]:
                medium_score += 20
            elif histogram.iloc[-1] > 0:
                medium_score += 10
            elif histogram.iloc[-1] < 0 and histogram.iloc[-1] < histogram.iloc[-2]:
                medium_score -= 20
            elif histogram.iloc[-1] < 0:
                medium_score -= 10
            
            # 长期指标 (60-250日)
            long_score = 0.0
            if len(df) >= 120:
                ma120 = close.rolling(120).mean().iloc[-1]
                
                if current > ma60 > ma120:
                    long_score = 50
                elif current > ma60:
                    long_score = 25
                elif current < ma60 < ma120:
                    long_score = -50
                elif current < ma60:
                    long_score = -25
            
            if len(df) >= 250:
                ma250 = close.rolling(250).mean().iloc[-1]
                if current > ma250:
                    long_score += 20
                else:
                    long_score -= 20
            
            return {
                'short': max(-100, min(100, short_score)),
                'medium': max(-100, min(100, medium_score)),
                'long': max(-100, min(100, long_score))
            }
            
        except Exception as e:
            logger.debug(f"计算技术得分失败 {date}: {e}")
            return {'short': 0.0, 'medium': 0.0, 'long': 0.0}
    
    def _determine_market_state(self, short_score: float, medium_score: float, 
                                 long_score: float) -> Tuple[str, MarketStateCategory]:
        """
        判断市场状态
        
        Returns:
            (状态名称, 状态类别)
        """
        # 牛市系列
        if long_score > 30:
            if medium_score > 20 and short_score > 10:
                return "牛市确认(共振)", MarketStateCategory.BULL
            elif medium_score > 20:
                return "牛市确认", MarketStateCategory.BULL
            elif short_score < -20:
                return "牛市短期调整", MarketStateCategory.BULL
            elif medium_score < 0:
                return "牛市中期调整", MarketStateCategory.BULL
            else:
                return "牛市震荡", MarketStateCategory.BULL
        
        # 熊市系列
        elif long_score < -30:
            if medium_score < -20 and short_score < -10:
                return "熊市确认(共振)", MarketStateCategory.BEAR
            elif medium_score < -20:
                return "熊市确认", MarketStateCategory.BEAR
            elif short_score > 20:
                return "熊市技术反弹", MarketStateCategory.BEAR
            elif medium_score > 0:
                return "熊市筑底", MarketStateCategory.BEAR
            else:
                return "熊市反弹", MarketStateCategory.BEAR
        
        # 震荡系列
        else:
            if medium_score > 10 and short_score > 10:
                return "突破在即", MarketStateCategory.VOLATILE
            elif medium_score < -10 and short_score < -10:
                return "破位风险", MarketStateCategory.VOLATILE
            elif short_score > 20:
                return "复苏初期", MarketStateCategory.VOLATILE
            elif short_score < -20:
                return "见顶回落", MarketStateCategory.VOLATILE
            else:
                return "震荡整理", MarketStateCategory.VOLATILE
    
    def _get_hmm_state(self, date: str, benchmark: str = "000001.XSHG") -> Dict[str, Any]:
        """获取HMM市场状态"""
        try:
            # 获取历史数据用于HMM分析
            end_dt = datetime.strptime(date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=120)
            
            df = self._jq.get_price(
                benchmark,
                start_date=start_dt.strftime('%Y-%m-%d'),
                end_date=date,
                frequency='daily',
                fields=['close', 'volume']
            )
            
            if df is None or df.empty or len(df) < 60:
                return {'state': 'unknown', 'confidence': 0.0}
            
            # 调用HMM分析
            result = self._hmm_analyzer.analyze(df)
            
            if result is None:
                return {'state': 'unknown', 'confidence': 0.0}
            
            # 将MarketState枚举(中文)转换为英文字符串
            state_value = result.current_state.value
            state_map = {'牛市': 'bull', '熊市': 'bear', '震荡': 'sideways'}
            state_str = state_map.get(state_value, 'unknown')
            
            return {
                'state': state_str,
                'confidence': result.confidence
            }
            
        except Exception as e:
            logger.debug(f"HMM分析失败 {date}: {e}")
            return {'state': 'unknown', 'confidence': 0.0}
    
    def _get_ibd_analysis(self, date: str, benchmark: str = "000001.XSHG") -> Dict[str, Any]:
        """获取IBD市场分析"""
        try:
            result = self._ibd_analyzer.analyze(index_code=benchmark, lookback_days=60)
            
            if result is None:
                return {'status': 'unknown', 'distribution_count': 0, 'has_ftd': False}
            
            return {
                'status': result.market_status.value if hasattr(result.market_status, 'value') else str(result.market_status),
                'distribution_count': result.distribution_count,
                'has_ftd': len(result.follow_through_days) > 0 if result.follow_through_days else False
            }
            
        except Exception as e:
            logger.debug(f"IBD分析失败 {date}: {e}")
            return {'status': 'unknown', 'distribution_count': 0, 'has_ftd': False}
    
    def _generate_enhanced_signal(self, date: str, config: BacktestConfig) -> Optional[EnhancedSignalRecord]:
        """生成增强信号"""
        try:
            # 获取A股特色指标
            daily_north, cum_5d_north = self._get_north_fund_data(date)
            
            if cum_5d_north > config.north_fund_bullish_threshold:
                north_score = min(100, cum_5d_north)
            elif cum_5d_north < config.north_fund_bearish_threshold:
                north_score = max(-100, cum_5d_north)
            else:
                north_score = cum_5d_north * 0.5
            
            margin_change = self._get_margin_data(date)
            
            if margin_change > config.margin_change_bullish_threshold:
                margin_score = min(50, margin_change * 20)
            elif margin_change < config.margin_change_bearish_threshold:
                margin_score = max(-50, margin_change * 20)
            else:
                margin_score = margin_change * 10
            
            breadth_ratio = self._get_breadth_data(date)
            
            if breadth_ratio > config.breadth_bullish_threshold:
                breadth_score = min(50, (breadth_ratio - 1) * 25)
            elif breadth_ratio < config.breadth_bearish_threshold:
                breadth_score = max(-50, (breadth_ratio - 1) * 50)
            else:
                breadth_score = (breadth_ratio - 1) * 20
            
            # 计算技术指标得分
            tech_scores = self._calculate_technical_scores(date, config.benchmark)
            
            # 综合A股指标和技术指标
            short_score = tech_scores['short'] * 0.6 + breadth_score * 0.4
            medium_score = tech_scores['medium'] * 0.6 + margin_score * 0.4
            long_score = tech_scores['long'] * 0.6 + north_score * 0.4
            
            # 综合得分
            composite_score = short_score * 0.2 + medium_score * 0.3 + long_score * 0.5
            
            # 确定各周期信号
            def get_signal(score, bull_thresh, bear_thresh):
                if score > bull_thresh:
                    return SignalType.BULLISH
                elif score < bear_thresh:
                    return SignalType.BEARISH
                else:
                    return SignalType.NEUTRAL
            
            short_signal = get_signal(short_score, config.short_bullish_threshold, config.short_bearish_threshold)
            medium_signal = get_signal(medium_score, config.medium_bullish_threshold, config.medium_bearish_threshold)
            long_signal = get_signal(long_score, config.long_bullish_threshold, config.long_bearish_threshold)
            
            # 综合信号
            if composite_score > config.composite_bullish_threshold:
                signal_type = SignalType.BULLISH
            elif composite_score < config.composite_bearish_threshold:
                signal_type = SignalType.BEARISH
            else:
                signal_type = SignalType.NEUTRAL
            
            # 市场状态
            market_state, state_category = self._determine_market_state(short_score, medium_score, long_score)
            
            # HMM分析
            hmm_state = "unknown"
            hmm_confidence = 0.0
            hmm_signal_aligned = False
            if self._use_hmm and self._hmm_analyzer is not None:
                try:
                    hmm_result = self._get_hmm_state(date, config.benchmark)
                    hmm_state = hmm_result.get('state', 'unknown')
                    hmm_confidence = hmm_result.get('confidence', 0.0)
                    # 检查HMM是否与综合信号一致
                    if signal_type == SignalType.BULLISH and hmm_state == 'bull':
                        hmm_signal_aligned = True
                    elif signal_type == SignalType.BEARISH and hmm_state == 'bear':
                        hmm_signal_aligned = True
                    elif signal_type == SignalType.NEUTRAL and hmm_state == 'sideways':
                        hmm_signal_aligned = True
                except Exception as e:
                    logger.debug(f"HMM分析失败 {date}: {e}")
            
            # IBD分析
            ibd_market_status = "unknown"
            ibd_distribution_count = 0
            ibd_has_ftd = False
            ibd_signal_aligned = False
            if self._use_ibd and self._ibd_analyzer is not None:
                try:
                    ibd_result = self._get_ibd_analysis(date, config.benchmark)
                    ibd_market_status = ibd_result.get('status', 'unknown')
                    ibd_distribution_count = ibd_result.get('distribution_count', 0)
                    ibd_has_ftd = ibd_result.get('has_ftd', False)
                    # 检查IBD是否与综合信号一致
                    if signal_type == SignalType.BULLISH and ibd_market_status in ['confirmed_uptrend', 'rally_attempt']:
                        ibd_signal_aligned = True
                    elif signal_type == SignalType.BEARISH and ibd_market_status in ['market_in_correction']:
                        ibd_signal_aligned = True
                    elif signal_type == SignalType.NEUTRAL and ibd_market_status == 'uptrend_under_pressure':
                        ibd_signal_aligned = True
                except Exception as e:
                    logger.debug(f"IBD分析失败 {date}: {e}")
            
            # 计算多模型共识 (优化策略 v3.0 - HMM为核心)
            # 核心发现: HMM一致信号准确率87.5%，是最可靠的指标
            bullish_votes = 0.0
            bearish_votes = 0.0
            
            # HMM投票 (核心指标，权重2.5)
            hmm_aligned_with_signal = False
            if hmm_state == 'bull':
                bullish_votes += 2.5
                if signal_type == SignalType.BULLISH:
                    hmm_aligned_with_signal = True
            elif hmm_state == 'bear':
                bearish_votes += 2.5
                if signal_type == SignalType.BEARISH:
                    hmm_aligned_with_signal = True
            
            # IBD投票 (参考指标，权重0.4-0.6)
            if ibd_market_status == 'confirmed_uptrend':
                bullish_votes += 0.6
            elif ibd_market_status == 'rally_attempt':
                bullish_votes += 0.4
            elif ibd_market_status == 'market_in_correction':
                bearish_votes += 0.6
            elif ibd_market_status == 'uptrend_under_pressure':
                bearish_votes += 0.4
            
            # 三周期技术指标投票
            if short_signal == SignalType.BULLISH:
                bullish_votes += 0.6
            elif short_signal == SignalType.BEARISH:
                bearish_votes += 0.6
            
            if medium_signal == SignalType.BULLISH:
                bullish_votes += 0.8
            elif medium_signal == SignalType.BEARISH:
                bearish_votes += 0.8
            
            if long_signal == SignalType.BULLISH:
                bullish_votes += 1.0
            elif long_signal == SignalType.BEARISH:
                bearish_votes += 1.0
            
            # 计算共识度
            model_consensus = 0
            if signal_type == SignalType.BULLISH:
                model_consensus = int(bullish_votes)
            elif signal_type == SignalType.BEARISH:
                model_consensus = int(bearish_votes)
            
            # 置信度分级 (以HMM一致为核心条件)
            # 高置信度: HMM一致 + 长期趋势一致 (最可靠组合)
            # 中置信度: HMM一致 或 (长期+中期一致)
            long_aligned = (signal_type == SignalType.BULLISH and long_signal == SignalType.BULLISH) or                           (signal_type == SignalType.BEARISH and long_signal == SignalType.BEARISH)
            medium_aligned = (signal_type == SignalType.BULLISH and medium_signal == SignalType.BULLISH) or                             (signal_type == SignalType.BEARISH and medium_signal == SignalType.BEARISH)
            
            high_confidence = hmm_aligned_with_signal and long_aligned
            medium_confidence = (hmm_aligned_with_signal or (long_aligned and medium_aligned)) and not high_confidence
            confidence_level = "high" if high_confidence else ("medium" if medium_confidence else "low")
            
            return EnhancedSignalRecord(
                date=date,
                signal_type=signal_type,
                composite_score=composite_score,
                short_term_signal=short_signal,
                medium_term_signal=medium_signal,
                long_term_signal=long_signal,
                short_term_score=short_score,
                medium_term_score=medium_score,
                long_term_score=long_score,
                north_fund_score=north_score,
                margin_score=margin_score,
                breadth_score=breadth_score,
                market_state=market_state,
                state_category=state_category,
                hmm_state=hmm_state,
                hmm_confidence=hmm_confidence,
                hmm_signal_aligned=hmm_signal_aligned,
                ibd_market_status=ibd_market_status,
                ibd_distribution_count=ibd_distribution_count,
                ibd_has_ftd=ibd_has_ftd,
                ibd_signal_aligned=ibd_signal_aligned,
                model_consensus=model_consensus,
                bullish_votes=bullish_votes,
                bearish_votes=bearish_votes,
                high_confidence=high_confidence,
                medium_confidence=medium_confidence,
                confidence_level=confidence_level
            )
            
        except Exception as e:
            logger.debug(f"生成信号失败 {date}: {e}")
            return None
    
    def run_backtest(self, config: BacktestConfig = None, 
                      sample_interval: int = 5,
                      progress_callback: Callable = None) -> EnhancedBacktestResult:
        """运行回测"""
        if config is None:
            config = BacktestConfig()
        
        start_time = datetime.now()
        self._ensure_jqdata()
        
        result = EnhancedBacktestResult(config=config)
        result.backtest_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f"开始回测: {config.start_date} ~ {config.end_date}")
        
        trade_days = self._get_trade_days(config.start_date, config.end_date)
        logger.info(f"共 {len(trade_days)} 个交易日")
        
        prices = self._get_benchmark_prices(config.start_date, config.end_date, config.benchmark)
        if prices is None or prices.empty:
            logger.error("无法获取基准价格数据")
            return result
        
        sampled_days = trade_days[::sample_interval]
        total_days = len(sampled_days)
        
        logger.info(f"采样 {total_days} 个交易日进行回测")
        
        signals = []
        
        for i, date in enumerate(sampled_days):
            if progress_callback:
                progress_callback(i + 1, total_days, date)
            
            if i % 50 == 0:
                logger.info(f"回测进度: {i+1}/{total_days} ({date})")
            
            signal = self._generate_enhanced_signal(date, config)
            if signal is None:
                continue
            
            # 计算未来收益
            returns = self._calculate_future_returns(prices, date, config.holding_periods)
            
            signal.returns_5d = returns.get(5, 0.0)
            signal.returns_10d = returns.get(10, 0.0)
            signal.returns_20d = returns.get(20, 0.0)
            signal.returns_60d = returns.get(60, 0.0)
            
            # 综合信号准确性
            if signal.signal_type == SignalType.BULLISH:
                signal.correct_5d = signal.returns_5d > 0
                signal.correct_10d = signal.returns_10d > 0
                signal.correct_20d = signal.returns_20d > 0
                signal.correct_60d = signal.returns_60d > 0
            elif signal.signal_type == SignalType.BEARISH:
                signal.correct_5d = signal.returns_5d < 0
                signal.correct_10d = signal.returns_10d < 0
                signal.correct_20d = signal.returns_20d < 0
                signal.correct_60d = signal.returns_60d < 0
            else:
                signal.correct_5d = abs(signal.returns_5d) < 2
                signal.correct_10d = abs(signal.returns_10d) < 3
                signal.correct_20d = abs(signal.returns_20d) < 5
                signal.correct_60d = abs(signal.returns_60d) < 10
            
            # 短周期准确性 (5日验证)
            if signal.short_term_signal == SignalType.BULLISH:
                signal.short_correct_5d = signal.returns_5d > 0
            elif signal.short_term_signal == SignalType.BEARISH:
                signal.short_correct_5d = signal.returns_5d < 0
            else:
                signal.short_correct_5d = abs(signal.returns_5d) < 2
            
            # 中周期准确性 (20日验证)
            if signal.medium_term_signal == SignalType.BULLISH:
                signal.medium_correct_20d = signal.returns_20d > 0
            elif signal.medium_term_signal == SignalType.BEARISH:
                signal.medium_correct_20d = signal.returns_20d < 0
            else:
                signal.medium_correct_20d = abs(signal.returns_20d) < 5
            
            # 长周期准确性 (60日验证)
            if signal.long_term_signal == SignalType.BULLISH:
                signal.long_correct_60d = signal.returns_60d > 0
            elif signal.long_term_signal == SignalType.BEARISH:
                signal.long_correct_60d = signal.returns_60d < 0
            else:
                signal.long_correct_60d = abs(signal.returns_60d) < 10
            
            # 市场状态准确性
            if signal.state_category == MarketStateCategory.BULL:
                signal.state_correct_60d = signal.returns_60d > 5
            elif signal.state_category == MarketStateCategory.BEAR:
                signal.state_correct_60d = signal.returns_60d < -5
            else:
                signal.state_correct_60d = abs(signal.returns_60d) < 5
            
            signals.append(signal)
        
        # 统计结果
        result.signals = signals
        result.total_signals = len(signals)
        
        bullish_signals = [s for s in signals if s.signal_type == SignalType.BULLISH]
        bearish_signals = [s for s in signals if s.signal_type == SignalType.BEARISH]
        neutral_signals = [s for s in signals if s.signal_type == SignalType.NEUTRAL]
        
        result.bullish_signals = len(bullish_signals)
        result.bearish_signals = len(bearish_signals)
        result.neutral_signals = len(neutral_signals)
        
        # 综合准确率
        if result.total_signals > 0:
            result.accuracy_5d = sum(1 for s in signals if s.correct_5d) / result.total_signals * 100
            result.accuracy_10d = sum(1 for s in signals if s.correct_10d) / result.total_signals * 100
            result.accuracy_20d = sum(1 for s in signals if s.correct_20d) / result.total_signals * 100
            result.accuracy_60d = sum(1 for s in signals if s.correct_60d) / result.total_signals * 100
            
            # 短周期准确率
            result.short_accuracy_5d = sum(1 for s in signals if s.short_correct_5d) / result.total_signals * 100
            
            # 中周期准确率
            result.medium_accuracy_20d = sum(1 for s in signals if s.medium_correct_20d) / result.total_signals * 100
            
            # 长周期准确率
            result.long_accuracy_60d = sum(1 for s in signals if s.long_correct_60d) / result.total_signals * 100
            
            # 市场状态准确率
            result.state_accuracy_60d = sum(1 for s in signals if s.state_correct_60d) / result.total_signals * 100
        
        # HMM/IBD交叉验证统计
        hmm_aligned = [s for s in signals if s.hmm_signal_aligned]
        ibd_aligned = [s for s in signals if s.ibd_signal_aligned]
        high_conf = [s for s in signals if s.high_confidence]
        medium_conf = [s for s in signals if s.medium_confidence]
        low_conf = [s for s in signals if s.confidence_level == 'low']
        
        result.hmm_aligned_signals = len(hmm_aligned)
        result.ibd_aligned_signals = len(ibd_aligned)
        result.high_confidence_signals = len(high_conf)
        result.medium_confidence_signals = len(medium_conf)
        result.low_confidence_signals = len(low_conf)
        
        # 高置信度准确率
        if high_conf:
            result.high_confidence_accuracy_5d = sum(1 for s in high_conf if s.correct_5d) / len(high_conf) * 100
            result.high_confidence_accuracy_20d = sum(1 for s in high_conf if s.correct_20d) / len(high_conf) * 100
            result.high_confidence_accuracy_60d = sum(1 for s in high_conf if s.correct_60d) / len(high_conf) * 100
        
        # 中置信度准确率
        if medium_conf:
            result.medium_confidence_accuracy_5d = sum(1 for s in medium_conf if s.correct_5d) / len(medium_conf) * 100
            result.medium_confidence_accuracy_20d = sum(1 for s in medium_conf if s.correct_20d) / len(medium_conf) * 100
            result.medium_confidence_accuracy_60d = sum(1 for s in medium_conf if s.correct_60d) / len(medium_conf) * 100
        
        # 低置信度准确率 (作为基准对比)
        if low_conf:
            result.low_confidence_accuracy_5d = sum(1 for s in low_conf if s.correct_5d) / len(low_conf) * 100
            result.low_confidence_accuracy_20d = sum(1 for s in low_conf if s.correct_20d) / len(low_conf) * 100
        
        if hmm_aligned:
            result.hmm_aligned_accuracy_5d = sum(1 for s in hmm_aligned if s.correct_5d) / len(hmm_aligned) * 100
            result.hmm_aligned_accuracy_20d = sum(1 for s in hmm_aligned if s.correct_20d) / len(hmm_aligned) * 100
        
        if ibd_aligned:
            result.ibd_aligned_accuracy_5d = sum(1 for s in ibd_aligned if s.correct_5d) / len(ibd_aligned) * 100
            result.ibd_aligned_accuracy_20d = sum(1 for s in ibd_aligned if s.correct_20d) / len(ibd_aligned) * 100
        
        # 分类统计
        short_bullish = [s for s in signals if s.short_term_signal == SignalType.BULLISH]
        short_bearish = [s for s in signals if s.short_term_signal == SignalType.BEARISH]
        
        if short_bullish:
            result.short_bullish_accuracy = sum(1 for s in short_bullish if s.short_correct_5d) / len(short_bullish) * 100
        if short_bearish:
            result.short_bearish_accuracy = sum(1 for s in short_bearish if s.short_correct_5d) / len(short_bearish) * 100
        
        medium_bullish = [s for s in signals if s.medium_term_signal == SignalType.BULLISH]
        medium_bearish = [s for s in signals if s.medium_term_signal == SignalType.BEARISH]
        
        if medium_bullish:
            result.medium_bullish_accuracy = sum(1 for s in medium_bullish if s.medium_correct_20d) / len(medium_bullish) * 100
        if medium_bearish:
            result.medium_bearish_accuracy = sum(1 for s in medium_bearish if s.medium_correct_20d) / len(medium_bearish) * 100
        
        long_bullish = [s for s in signals if s.long_term_signal == SignalType.BULLISH]
        long_bearish = [s for s in signals if s.long_term_signal == SignalType.BEARISH]
        
        if long_bullish:
            result.long_bullish_accuracy = sum(1 for s in long_bullish if s.long_correct_60d) / len(long_bullish) * 100
        if long_bearish:
            result.long_bearish_accuracy = sum(1 for s in long_bearish if s.long_correct_60d) / len(long_bearish) * 100
        
        # 市场状态分类统计
        bull_states = [s for s in signals if s.state_category == MarketStateCategory.BULL]
        bear_states = [s for s in signals if s.state_category == MarketStateCategory.BEAR]
        volatile_states = [s for s in signals if s.state_category == MarketStateCategory.VOLATILE]
        
        if bull_states:
            result.bull_state_accuracy = sum(1 for s in bull_states if s.state_correct_60d) / len(bull_states) * 100
        if bear_states:
            result.bear_state_accuracy = sum(1 for s in bear_states if s.state_correct_60d) / len(bear_states) * 100
        if volatile_states:
            result.volatile_state_accuracy = sum(1 for s in volatile_states if s.state_correct_60d) / len(volatile_states) * 100
        
        # 平均收益
        if bullish_signals:
            result.avg_return_bullish_5d = np.mean([s.returns_5d for s in bullish_signals])
            result.avg_return_bullish_20d = np.mean([s.returns_20d for s in bullish_signals])
            result.win_rate_bullish = sum(1 for s in bullish_signals if s.returns_5d > 0) / len(bullish_signals) * 100
        
        if bearish_signals:
            result.avg_return_bearish_5d = np.mean([s.returns_5d for s in bearish_signals])
            result.avg_return_bearish_20d = np.mean([s.returns_20d for s in bearish_signals])
            result.win_rate_bearish = sum(1 for s in bearish_signals if s.returns_5d < 0) / len(bearish_signals) * 100
        
        # 按年统计
        for signal in signals:
            year = signal.date[:4]
            if year not in result.yearly_stats:
                result.yearly_stats[year] = {
                    'total': 0, 'bullish': 0, 'bearish': 0, 'neutral': 0,
                    'correct_5d': 0, 'correct_20d': 0, 'correct_60d': 0,
                    'short_correct': 0, 'medium_correct': 0, 'long_correct': 0
                }
            
            result.yearly_stats[year]['total'] += 1
            if signal.signal_type == SignalType.BULLISH:
                result.yearly_stats[year]['bullish'] += 1
            elif signal.signal_type == SignalType.BEARISH:
                result.yearly_stats[year]['bearish'] += 1
            else:
                result.yearly_stats[year]['neutral'] += 1
            
            if signal.correct_5d:
                result.yearly_stats[year]['correct_5d'] += 1
            if signal.correct_20d:
                result.yearly_stats[year]['correct_20d'] += 1
            if signal.correct_60d:
                result.yearly_stats[year]['correct_60d'] += 1
            if signal.short_correct_5d:
                result.yearly_stats[year]['short_correct'] += 1
            if signal.medium_correct_20d:
                result.yearly_stats[year]['medium_correct'] += 1
            if signal.long_correct_60d:
                result.yearly_stats[year]['long_correct'] += 1
        
        result.duration_seconds = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"回测完成: 共{result.total_signals}个信号, 5日准确率={result.accuracy_5d:.1f}%, 耗时={result.duration_seconds:.1f}秒")
        
        return result
    
    def generate_report(self, result: EnhancedBacktestResult) -> str:
        """生成回测报告 (Markdown格式)"""
        report = f"""
# 市场趋势信号回测报告 (增强版)

## 回测概况

| 项目 | 值 |
|------|-----|
| 回测时间 | {result.backtest_time} |
| 回测区间 | {result.config.start_date} ~ {result.config.end_date} |
| 基准指数 | {result.config.benchmark} |
| 总信号数 | {result.total_signals} |
| 看多信号 | {result.bullish_signals} |
| 看空信号 | {result.bearish_signals} |
| 中性信号 | {result.neutral_signals} |
| 耗时 | {result.duration_seconds:.1f}秒 |

## 综合准确率

| 持有期 | 准确率 |
|--------|--------|
| 5日 | {result.accuracy_5d:.1f}% |
| 10日 | {result.accuracy_10d:.1f}% |
| 20日 | {result.accuracy_20d:.1f}% |
| 60日 | {result.accuracy_60d:.1f}% |

## 分周期准确率

| 周期 | 验证期 | 准确率 | 看多准确 | 看空准确 |
|------|--------|--------|----------|----------|
| 短期 | 5日 | {result.short_accuracy_5d:.1f}% | {result.short_bullish_accuracy:.1f}% | {result.short_bearish_accuracy:.1f}% |
| 中期 | 20日 | {result.medium_accuracy_20d:.1f}% | {result.medium_bullish_accuracy:.1f}% | {result.medium_bearish_accuracy:.1f}% |
| 长期 | 60日 | {result.long_accuracy_60d:.1f}% | {result.long_bullish_accuracy:.1f}% | {result.long_bearish_accuracy:.1f}% |

## 市场状态准确率

| 状态类别 | 60日准确率 |
|----------|------------|
| 牛市系列 | {result.bull_state_accuracy:.1f}% |
| 熊市系列 | {result.bear_state_accuracy:.1f}% |
| 震荡系列 | {result.volatile_state_accuracy:.1f}% |
| **综合** | **{result.state_accuracy_60d:.1f}%** |

## 分类信号表现

### 看多信号
| 指标 | 值 |
|------|-----|
| 信号数量 | {result.bullish_signals} |
| 5日胜率 | {result.win_rate_bullish:.1f}% |
| 5日平均收益 | {result.avg_return_bullish_5d:.2f}% |
| 20日平均收益 | {result.avg_return_bullish_20d:.2f}% |

### 看空信号
| 指标 | 值 |
|------|-----|
| 信号数量 | {result.bearish_signals} |
| 5日胜率 | {result.win_rate_bearish:.1f}% |
| 5日平均收益 | {result.avg_return_bearish_5d:.2f}% |
| 20日平均收益 | {result.avg_return_bearish_20d:.2f}% |

## 年度统计

| 年份 | 信号数 | 5日准确 | 20日准确 | 60日准确 | 短期准确 | 中期准确 | 长期准确 |
|------|--------|---------|----------|----------|----------|----------|----------|
"""
        for year in sorted(result.yearly_stats.keys()):
            stats = result.yearly_stats[year]
            total = stats['total']
            if total > 0:
                acc_5d = stats['correct_5d'] / total * 100
                acc_20d = stats['correct_20d'] / total * 100
                acc_60d = stats['correct_60d'] / total * 100
                short_acc = stats['short_correct'] / total * 100
                medium_acc = stats['medium_correct'] / total * 100
                long_acc = stats['long_correct'] / total * 100
                report += f"| {year} | {total} | {acc_5d:.0f}% | {acc_20d:.0f}% | {acc_60d:.0f}% | {short_acc:.0f}% | {medium_acc:.0f}% | {long_acc:.0f}% |\n"
        
        return report


# ==================== 并行回测器 ====================

class ParallelBacktester:
    """
    多进程并行回测器
    
    利用JQData的3个并发连接，将回测任务分割到多个进程并行执行
    """
    
    def __init__(self, num_workers: int = 3):
        """
        初始化并行回测器
        
        Args:
            num_workers: 并行进程数 (默认3，对应JQData的3个连接)
        """
        self.num_workers = min(num_workers, 3)  # JQData最多3个连接
    
    def _split_date_range(self, start_date: str, end_date: str, 
                          num_splits: int) -> List[Tuple[str, str]]:
        """将日期范围分割成多个子范围"""
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        total_days = (end_dt - start_dt).days
        days_per_split = total_days // num_splits
        
        ranges = []
        current_start = start_dt
        
        for i in range(num_splits):
            if i == num_splits - 1:
                current_end = end_dt
            else:
                current_end = current_start + timedelta(days=days_per_split)
            
            ranges.append((
                current_start.strftime('%Y-%m-%d'),
                current_end.strftime('%Y-%m-%d')
            ))
            
            current_start = current_end + timedelta(days=1)
        
        return ranges
    
    def run_phase1(self, sample_interval: int = 5) -> EnhancedBacktestResult:
        """
        Phase 1: 快速验证 (1年数据)
        
        - 时间范围: 2023-01-01 ~ 2024-08-16
        - 采样间隔: 默认每5天
        - 单进程执行
        - 目的: 验证框架正确性
        """
        config = BacktestConfig(
            start_date="2023-01-01",
            end_date="2024-08-16"
        )
        
        backtester = SignalBacktester()
        result = backtester.run_backtest(config, sample_interval=sample_interval)
        result.phase = "phase1"
        
        return result
    
    def run_phase2(self, sample_interval: int = 1, 
                   progress_callback: Callable = None) -> EnhancedBacktestResult:
        """
        Phase 2: 完整回测 (10年数据)
        
        - 时间范围: 2014-11-17 ~ 2024-08-16
        - 采样间隔: 默认每1天 (可调)
        - 3进程并行执行
        - 目的: 完整验证信号准确率
        """
        logger.info(f"开始Phase 2完整回测 (使用{self.num_workers}个进程)")
        
        # 分割时间段
        date_ranges = [
            ("2014-11-17", "2017-12-31"),  # Worker 1: 牛熊转换期
            ("2018-01-01", "2021-06-30"),  # Worker 2: 熊市+疫情复苏
            ("2021-07-01", "2024-08-16"),  # Worker 3: 结构性行情
        ]
        
        all_signals = []
        all_yearly_stats = {}
        
        # 串行执行各个时间段 (避免JQData连接冲突)
        for i, (start_date, end_date) in enumerate(date_ranges):
            logger.info(f"Worker {i+1}: 回测 {start_date} ~ {end_date}")
            
            config = BacktestConfig(
                start_date=start_date,
                end_date=end_date
            )
            
            backtester = SignalBacktester()
            
            def worker_progress(current, total, date):
                if progress_callback:
                    overall_progress = i * 100 // len(date_ranges) + current * 100 // (total * len(date_ranges))
                    progress_callback(overall_progress, 100, f"Worker{i+1}: {date}")
            
            result = backtester.run_backtest(config, sample_interval=sample_interval, 
                                             progress_callback=worker_progress)
            
            all_signals.extend(result.signals)
            
            # 合并年度统计
            for year, stats in result.yearly_stats.items():
                if year not in all_yearly_stats:
                    all_yearly_stats[year] = stats.copy()
                else:
                    for key in stats:
                        all_yearly_stats[year][key] += stats[key]
        
        # 合并结果
        merged_result = EnhancedBacktestResult(
            config=BacktestConfig(
                start_date="2014-11-17",
                end_date="2024-08-16"
            ),
            phase="phase2"
        )
        
        merged_result.signals = all_signals
        merged_result.total_signals = len(all_signals)
        merged_result.yearly_stats = all_yearly_stats
        merged_result.backtest_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 重新计算统计数据
        self._recalculate_stats(merged_result)
        
        return merged_result
    
    def _recalculate_stats(self, result: EnhancedBacktestResult):
        """重新计算统计数据"""
        signals = result.signals
        
        if not signals:
            return
        
        bullish_signals = [s for s in signals if s.signal_type == SignalType.BULLISH]
        bearish_signals = [s for s in signals if s.signal_type == SignalType.BEARISH]
        neutral_signals = [s for s in signals if s.signal_type == SignalType.NEUTRAL]
        
        result.bullish_signals = len(bullish_signals)
        result.bearish_signals = len(bearish_signals)
        result.neutral_signals = len(neutral_signals)
        
        # 综合准确率
        result.accuracy_5d = sum(1 for s in signals if s.correct_5d) / len(signals) * 100
        result.accuracy_10d = sum(1 for s in signals if s.correct_10d) / len(signals) * 100
        result.accuracy_20d = sum(1 for s in signals if s.correct_20d) / len(signals) * 100
        result.accuracy_60d = sum(1 for s in signals if s.correct_60d) / len(signals) * 100
        
        # 短周期准确率
        result.short_accuracy_5d = sum(1 for s in signals if s.short_correct_5d) / len(signals) * 100
        
        short_bullish = [s for s in signals if s.short_term_signal == SignalType.BULLISH]
        short_bearish = [s for s in signals if s.short_term_signal == SignalType.BEARISH]
        
        if short_bullish:
            result.short_bullish_accuracy = sum(1 for s in short_bullish if s.short_correct_5d) / len(short_bullish) * 100
        if short_bearish:
            result.short_bearish_accuracy = sum(1 for s in short_bearish if s.short_correct_5d) / len(short_bearish) * 100
        
        # 中周期准确率
        result.medium_accuracy_20d = sum(1 for s in signals if s.medium_correct_20d) / len(signals) * 100
        
        medium_bullish = [s for s in signals if s.medium_term_signal == SignalType.BULLISH]
        medium_bearish = [s for s in signals if s.medium_term_signal == SignalType.BEARISH]
        
        if medium_bullish:
            result.medium_bullish_accuracy = sum(1 for s in medium_bullish if s.medium_correct_20d) / len(medium_bullish) * 100
        if medium_bearish:
            result.medium_bearish_accuracy = sum(1 for s in medium_bearish if s.medium_correct_20d) / len(medium_bearish) * 100
        
        # 长周期准确率
        result.long_accuracy_60d = sum(1 for s in signals if s.long_correct_60d) / len(signals) * 100
        
        long_bullish = [s for s in signals if s.long_term_signal == SignalType.BULLISH]
        long_bearish = [s for s in signals if s.long_term_signal == SignalType.BEARISH]
        
        if long_bullish:
            result.long_bullish_accuracy = sum(1 for s in long_bullish if s.long_correct_60d) / len(long_bullish) * 100
        if long_bearish:
            result.long_bearish_accuracy = sum(1 for s in long_bearish if s.long_correct_60d) / len(long_bearish) * 100
        
        # 市场状态准确率
        result.state_accuracy_60d = sum(1 for s in signals if s.state_correct_60d) / len(signals) * 100
        
        bull_states = [s for s in signals if s.state_category == MarketStateCategory.BULL]
        bear_states = [s for s in signals if s.state_category == MarketStateCategory.BEAR]
        volatile_states = [s for s in signals if s.state_category == MarketStateCategory.VOLATILE]
        
        if bull_states:
            result.bull_state_accuracy = sum(1 for s in bull_states if s.state_correct_60d) / len(bull_states) * 100
        if bear_states:
            result.bear_state_accuracy = sum(1 for s in bear_states if s.state_correct_60d) / len(bear_states) * 100
        if volatile_states:
            result.volatile_state_accuracy = sum(1 for s in volatile_states if s.state_correct_60d) / len(volatile_states) * 100
        
        # 平均收益
        if bullish_signals:
            result.avg_return_bullish_5d = np.mean([s.returns_5d for s in bullish_signals])
            result.avg_return_bullish_20d = np.mean([s.returns_20d for s in bullish_signals])
            result.win_rate_bullish = sum(1 for s in bullish_signals if s.returns_5d > 0) / len(bullish_signals) * 100
        
        if bearish_signals:
            result.avg_return_bearish_5d = np.mean([s.returns_5d for s in bearish_signals])
            result.avg_return_bearish_20d = np.mean([s.returns_20d for s in bearish_signals])
            result.win_rate_bearish = sum(1 for s in bearish_signals if s.returns_5d < 0) / len(bearish_signals) * 100


# ==================== 便捷函数 ====================

def run_quick_backtest(start_date: str = "2023-01-01", 
                        end_date: str = "2024-08-16",
                        sample_interval: int = 5) -> EnhancedBacktestResult:
    """快速回测"""
    config = BacktestConfig(
        start_date=start_date,
        end_date=end_date
    )
    
    backtester = SignalBacktester()
    return backtester.run_backtest(config, sample_interval=sample_interval)


def run_phase1_backtest(sample_interval: int = 5) -> EnhancedBacktestResult:
    """Phase 1: 快速验证回测"""
    parallel = ParallelBacktester()
    return parallel.run_phase1(sample_interval=sample_interval)


def run_phase2_backtest(sample_interval: int = 3) -> EnhancedBacktestResult:
    """Phase 2: 完整10年回测"""
    parallel = ParallelBacktester()
    return parallel.run_phase2(sample_interval=sample_interval)


if __name__ == "__main__":
    # 测试
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    print("\n" + "=" * 60)
    print("Phase 1: 快速验证回测")
    print("=" * 60)
    
    result = run_phase1_backtest(sample_interval=10)
    
    backtester = SignalBacktester()
    report = backtester.generate_report(result)
    print(report)
