"""
Stock Filters - 个股筛选过滤器
================================

A股本土化过滤器：
1. RS相对强度（必须加）
2. 流动性过滤（A股必需）
3. 涨跌停修正（防止庄股/极端波动）

输出：
- filter mask（是否通过）
- ranking_features（供后续因子组合/选股排名用）
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

from core.resonance_state_model import (
    ResonanceConfig,
    StockFilterOutput,
    ExtendedInvestmentFilters,
    calculate_rs,
    detect_limit_days,
    detect_gap,
    detect_atr_abnormal,
)

logger = logging.getLogger(__name__)


# ============ 过滤结果数据结构 ============

@dataclass
class StockFilterResult:
    """
    批量过滤结果
    """
    date: str                           # 分析日期
    total_stocks: int                   # 总股票数
    passed_stocks: int                  # 通过数
    filtered_stocks: int                # 被过滤数
    
    # 过滤统计
    filter_stats: Dict[str, int] = field(default_factory=dict)  # {原因: 数量}
    
    # 详细结果
    results: List[StockFilterOutput] = field(default_factory=list)
    
    # 通过的股票代码列表
    passed_codes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "date": self.date,
            "total_stocks": self.total_stocks,
            "passed_stocks": self.passed_stocks,
            "filtered_stocks": self.filtered_stocks,
            "filter_stats": self.filter_stats,
            "passed_codes": self.passed_codes,
        }


# ============ 个股过滤引擎 ============

class StockFilterEngine:
    """
    个股筛选过滤引擎
    
    功能：
    1. RS相对强度计算与过滤
    2. 流动性过滤（成交额、市值、换手率）
    3. 涨跌停/跳空/ATR异常修正
    4. 输出过滤mask和ranking_features
    """
    
    def __init__(
        self,
        config: ResonanceConfig = None,
        filters: ExtendedInvestmentFilters = None,
    ):
        """
        初始化引擎
        
        Args:
            config: 共振配置
            filters: 扩展的投资标的筛选参数
        """
        self.config = config or ResonanceConfig()
        self.filters = filters or ExtendedInvestmentFilters()
        
        self._jq = None
        self._price_cache: Dict[str, pd.DataFrame] = {}
        self._benchmark_cache: Dict[str, pd.DataFrame] = {}
    
    def _ensure_jqdata(self):
        """确保JQData连接"""
        if self._jq is None:
            try:
                import jqdatasdk as jq
                from config.config_manager import get_config_manager
                
                config_mgr = get_config_manager()
                jq_config = config_mgr.get_config('jqdata')
                if jq_config:
                    jq.auth(jq_config.get('username'), jq_config.get('password'))
                    if jq.is_auth():
                        self._jq = jq
                        logger.info("StockFilterEngine: JQData连接成功")
            except Exception as e:
                logger.warning(f"JQData连接失败: {e}")
    
    def _get_price_data(
        self,
        code: str,
        as_of_date: str,
        days: int = 150,
    ) -> Optional[pd.DataFrame]:
        """获取价格数据"""
        cache_key = f"{code}_{as_of_date}_{days}"
        if cache_key in self._price_cache:
            return self._price_cache[cache_key]
        
        self._ensure_jqdata()
        if self._jq is None:
            return None
        
        try:
            df = self._jq.get_price(
                code,
                end_date=as_of_date,
                count=days,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume', 'money']
            )
            
            if df is not None and not df.empty:
                df = df.reset_index()
                if 'index' in df.columns:
                    df = df.rename(columns={'index': 'date'})
                self._price_cache[cache_key] = df
                return df
                
        except Exception as e:
            logger.debug(f"获取价格数据失败 {code}: {e}")
        
        return None
    
    def _get_benchmark_data(
        self,
        as_of_date: str,
        benchmark_code: str = "000300.XSHG",
        days: int = 150,
    ) -> Optional[pd.DataFrame]:
        """获取基准指数数据"""
        cache_key = f"bench_{benchmark_code}_{as_of_date}_{days}"
        if cache_key in self._benchmark_cache:
            return self._benchmark_cache[cache_key]
        
        df = self._get_price_data(benchmark_code, as_of_date, days)
        if df is not None:
            self._benchmark_cache[cache_key] = df
        return df
    
    def filter_stocks(
        self,
        stock_codes: List[str],
        as_of_date: str,
        filters: ExtendedInvestmentFilters = None,
        benchmark_code: str = "000300.XSHG",
    ) -> StockFilterResult:
        """
        批量过滤股票
        
        Args:
            stock_codes: 股票代码列表
            as_of_date: 分析日期
            filters: 过滤参数（可覆盖默认）
            benchmark_code: 基准指数代码
        
        Returns:
            StockFilterResult
        """
        filters = filters or self.filters
        results: List[StockFilterOutput] = []
        filter_stats: Dict[str, int] = {}
        passed_codes: List[str] = []
        
        # 获取基准数据
        benchmark_df = self._get_benchmark_data(as_of_date, benchmark_code)
        
        for code in stock_codes:
            result = self.filter_single_stock(
                code, as_of_date, filters, benchmark_df
            )
            if result:
                results.append(result)
                
                if result.pass_filter:
                    passed_codes.append(code)
                else:
                    for reason in result.filter_reasons:
                        filter_stats[reason] = filter_stats.get(reason, 0) + 1
        
        return StockFilterResult(
            date=as_of_date,
            total_stocks=len(stock_codes),
            passed_stocks=len(passed_codes),
            filtered_stocks=len(stock_codes) - len(passed_codes),
            filter_stats=filter_stats,
            results=results,
            passed_codes=passed_codes,
        )
    
    def filter_single_stock(
        self,
        stock_code: str,
        as_of_date: str,
        filters: ExtendedInvestmentFilters = None,
        benchmark_df: Optional[pd.DataFrame] = None,
    ) -> Optional[StockFilterOutput]:
        """
        过滤单只股票
        
        Args:
            stock_code: 股票代码
            as_of_date: 分析日期
            filters: 过滤参数
            benchmark_df: 基准指数数据
        
        Returns:
            StockFilterOutput
        """
        filters = filters or self.filters
        
        # 获取数据
        df = self._get_price_data(stock_code, as_of_date)
        if df is None or len(df) < 20:
            return None
        
        if benchmark_df is None:
            benchmark_df = self._get_benchmark_data(as_of_date)
        
        try:
            # 计算指标
            output = StockFilterOutput(
                stock_code=stock_code,
                stock_name=self._get_stock_name(stock_code),
            )
            
            filter_reasons: List[str] = []
            penalty = 0.0
            
            # ===== 1. RS相对强度 =====
            rs_20d = self._calc_rs(df, benchmark_df, 20)
            rs_60d = self._calc_rs(df, benchmark_df, 60)
            rs_120d = self._calc_rs(df, benchmark_df, 120)
            rs_composite = rs_20d * 0.5 + rs_60d * 0.3 + rs_120d * 0.2
            
            output.rs_20d = rs_20d
            output.rs_60d = rs_60d
            output.rs_120d = rs_120d
            output.rs_composite = rs_composite
            
            if rs_20d < filters.rs_20d_min:
                filter_reasons.append(f"RS_20d过低({rs_20d:.1f}<{filters.rs_20d_min})")
            if rs_60d < filters.rs_60d_min:
                filter_reasons.append(f"RS_60d过低({rs_60d:.1f}<{filters.rs_60d_min})")
            
            # ===== 2. 流动性 =====
            avg_turnover = self._calc_avg_turnover(df, 20)
            market_cap = self._get_market_cap(stock_code, as_of_date)
            turnover_rate = self._calc_turnover_rate(df, 5)
            
            output.avg_turnover = avg_turnover
            output.market_cap = market_cap
            output.turnover_rate = turnover_rate
            
            if avg_turnover < filters.min_turnover:
                filter_reasons.append(f"成交额不足({avg_turnover/1e6:.0f}M<{filters.min_turnover/1e6:.0f}M)")
            if market_cap < filters.min_market_cap:
                filter_reasons.append(f"市值过小({market_cap/1e8:.0f}亿<{filters.min_market_cap/1e8:.0f}亿)")
            if turnover_rate > filters.max_turnover_rate:
                filter_reasons.append(f"换手率过高({turnover_rate:.1%}>{filters.max_turnover_rate:.1%})")
                penalty += self.config.limit_up_penalty * 0.5  # 轻度惩罚
            
            # ===== 3. 涨跌停/异常检测 =====
            limit_up_days, limit_down_days = detect_limit_days(df, lookback=10)
            max_gap = detect_gap(df, lookback=5)
            atr_ratio, is_atr_abnormal = detect_atr_abnormal(
                df, period=14, multiplier=filters.max_atr_multiplier
            )
            
            output.limit_up_days = limit_up_days
            output.limit_down_days = limit_down_days
            output.max_gap_pct = max_gap
            output.atr_ratio = atr_ratio
            
            if limit_up_days > filters.max_limit_up_days:
                filter_reasons.append(f"连板过多({limit_up_days}>{filters.max_limit_up_days})")
                penalty += self.config.limit_up_penalty
            
            if limit_down_days > 2:
                penalty += self.config.limit_down_penalty
            
            if max_gap > filters.max_gap_pct:
                filter_reasons.append(f"跳空过大({max_gap:.1f}%>{filters.max_gap_pct}%)")
                penalty += self.config.gap_penalty
            
            if is_atr_abnormal:
                filter_reasons.append(f"ATR异常({atr_ratio:.1f}x)")
                penalty += self.config.atr_penalty
            
            output.penalty_score = penalty
            output.pass_filter = len(filter_reasons) == 0
            output.filter_reasons = filter_reasons
            
            # ===== 4. 生成ranking_features =====
            output.ranking_features = self._generate_ranking_features(
                df, benchmark_df, rs_composite, avg_turnover, penalty
            )
            
            return output
            
        except Exception as e:
            logger.debug(f"过滤股票失败 {stock_code}: {e}")
            return None
    
    def _calc_rs(
        self,
        stock_df: pd.DataFrame,
        benchmark_df: Optional[pd.DataFrame],
        window: int,
    ) -> float:
        """计算RS相对强度"""
        if benchmark_df is None or len(stock_df) < window or len(benchmark_df) < window:
            return 0.0
        
        stock_close = stock_df['close']
        bench_close = benchmark_df['close']
        
        return calculate_rs(stock_close, bench_close, window)
    
    def _calc_avg_turnover(self, df: pd.DataFrame, period: int) -> float:
        """计算平均成交额"""
        if len(df) < period:
            return 0.0
        
        # 优先用money字段（成交额），否则用volume * close估算
        if 'money' in df.columns:
            return float(df['money'].tail(period).mean())
        else:
            return float((df['volume'] * df['close']).tail(period).mean())
    
    def _get_market_cap(self, stock_code: str, as_of_date: str) -> float:
        """获取市值"""
        self._ensure_jqdata()
        if self._jq is None:
            return 0.0
        
        try:
            # 使用聚宽估值数据
            q = self._jq.query(
                self._jq.valuation.market_cap
            ).filter(
                self._jq.valuation.code == stock_code
            )
            
            df = self._jq.get_fundamentals(q, date=as_of_date)
            if df is not None and not df.empty:
                return float(df['market_cap'].iloc[0]) * 1e8  # 单位：亿 -> 元
        except Exception as e:
            logger.debug(f"获取市值失败 {stock_code}: {e}")
        
        return 0.0
    
    def _calc_turnover_rate(self, df: pd.DataFrame, period: int) -> float:
        """计算平均换手率（近期）"""
        # 简化：用成交量/流通股本估算
        # 实际应用应从估值数据获取
        if len(df) < period:
            return 0.0
        
        # 返回近N日平均日换手率的估计
        # 这里简化处理，返回0
        return 0.0
    
    def _get_stock_name(self, stock_code: str) -> str:
        """获取股票名称"""
        self._ensure_jqdata()
        if self._jq is None:
            return ""
        
        try:
            info = self._jq.get_security_info(stock_code)
            if info:
                return info.display_name
        except:
            pass
        return ""
    
    def _generate_ranking_features(
        self,
        df: pd.DataFrame,
        benchmark_df: Optional[pd.DataFrame],
        rs_composite: float,
        avg_turnover: float,
        penalty: float,
    ) -> Dict[str, float]:
        """
        生成排名特征
        
        供后续因子组合/选股排名使用
        """
        features = {
            "rs_composite": rs_composite,
            "avg_turnover_log": np.log10(avg_turnover + 1),
            "penalty": penalty,
        }
        
        close = df['close']
        
        # 动量因子
        if len(close) >= 5:
            features["mom_5d"] = (close.iloc[-1] / close.iloc[-5] - 1) * 100
        if len(close) >= 20:
            features["mom_20d"] = (close.iloc[-1] / close.iloc[-20] - 1) * 100
        if len(close) >= 60:
            features["mom_60d"] = (close.iloc[-1] / close.iloc[-60] - 1) * 100
        
        # 波动率
        if len(close) >= 20:
            returns = close.pct_change().tail(20)
            features["vol_20d"] = float(returns.std() * np.sqrt(252))
        
        # 成交量变化
        if 'volume' in df.columns and len(df) >= 10:
            vol = df['volume']
            vol_ma5 = vol.rolling(5).mean()
            vol_ma20 = vol.rolling(20).mean()
            if vol_ma20.iloc[-1] > 0:
                features["vol_ratio"] = float(vol_ma5.iloc[-1] / vol_ma20.iloc[-1])
        
        # 距离高点
        if len(close) >= 60:
            high_60 = close.tail(60).max()
            features["pct_from_high_60d"] = (close.iloc[-1] / high_60 - 1) * 100
        
        # 综合得分（简单加权）
        score = (
            rs_composite * 0.3 +
            features.get("mom_20d", 0) * 0.3 +
            features.get("vol_ratio", 1) * 10 * 0.1 +
            penalty * 0.3  # 惩罚项（负数）
        )
        features["composite_rank_score"] = float(score)
        
        return features
    
    def rank_stocks(
        self,
        filter_result: StockFilterResult,
        sort_by: str = "composite_rank_score",
        ascending: bool = False,
    ) -> List[StockFilterOutput]:
        """
        对通过过滤的股票进行排名
        
        Args:
            filter_result: 过滤结果
            sort_by: 排序字段
            ascending: 升序/降序
        
        Returns:
            排序后的股票列表
        """
        passed_results = [r for r in filter_result.results if r.pass_filter]
        
        def get_sort_key(r: StockFilterOutput) -> float:
            return r.ranking_features.get(sort_by, 0)
        
        passed_results.sort(key=get_sort_key, reverse=not ascending)
        
        return passed_results
    
    def get_top_n(
        self,
        stock_codes: List[str],
        as_of_date: str,
        top_n: int = 10,
        filters: ExtendedInvestmentFilters = None,
    ) -> List[str]:
        """
        获取TopN股票
        
        Args:
            stock_codes: 候选股票列表
            as_of_date: 分析日期
            top_n: 返回数量
            filters: 过滤参数
        
        Returns:
            TopN股票代码列表
        """
        result = self.filter_stocks(stock_codes, as_of_date, filters)
        ranked = self.rank_stocks(result)
        
        return [r.stock_code for r in ranked[:top_n]]
