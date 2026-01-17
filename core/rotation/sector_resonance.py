"""
Sector Resonance Engine - 行业/主题轮动共振引擎
================================================

双层宇宙：
1. 行业层：申万一级行业指数
2. 主题层：主题ETF池

核心功能：
- 对每个行业/主题计算多周期共振分数
- 输出TopN行业 + TopN主题ETF
- 提供可追溯的scorecard

参考：A股行业轮动特性，主线板块跟踪
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

from core.resonance_state_model import (
    ResonanceConfig,
    SectorRotationOutput,
)

logger = logging.getLogger(__name__)


# ============ 申万一级行业定义 ============

# 申万一级行业指数代码映射（31个行业）
SW_L1_SECTORS = {
    "801010.SI": "农林牧渔",
    "801020.SI": "采掘",
    "801030.SI": "化工",
    "801040.SI": "钢铁",
    "801050.SI": "有色金属",
    "801080.SI": "电子",
    "801110.SI": "家用电器",
    "801120.SI": "食品饮料",
    "801130.SI": "纺织服装",
    "801140.SI": "轻工制造",
    "801150.SI": "医药生物",
    "801160.SI": "公用事业",
    "801170.SI": "交通运输",
    "801180.SI": "房地产",
    "801200.SI": "商业贸易",
    "801210.SI": "休闲服务",
    "801230.SI": "综合",
    "801710.SI": "建筑材料",
    "801720.SI": "建筑装饰",
    "801730.SI": "电气设备",
    "801740.SI": "国防军工",
    "801750.SI": "计算机",
    "801760.SI": "传媒",
    "801770.SI": "通信",
    "801780.SI": "银行",
    "801790.SI": "非银金融",
    "801880.SI": "汽车",
    "801890.SI": "机械设备",
    "801950.SI": "煤炭",
    "801960.SI": "石油石化",
    "801970.SI": "环保",
    "801980.SI": "美容护理",
}

# 主题ETF池（按热门主题分类）
THEME_ETF_POOL = {
    # 科技主题
    "512480.SH": "半导体ETF",
    "515050.SH": "5G通信ETF",
    "515030.SH": "新能源车ETF",
    "515790.SH": "光伏ETF",
    "516160.SH": "新能源ETF",
    "516800.SH": "智能汽车ETF",
    "159995.SZ": "芯片ETF",
    "159825.SZ": "农业ETF",
    
    # 消费主题
    "159928.SZ": "消费ETF",
    "515170.SH": "食品饮料ETF",
    "159869.SZ": "游戏ETF",
    
    # 医药主题
    "512010.SH": "医药ETF",
    "159992.SZ": "创新药ETF",
    
    # 金融主题
    "512880.SH": "证券ETF",
    "512800.SH": "银行ETF",
    "515180.SH": "保险ETF",
    
    # 周期主题
    "159611.SZ": "电力ETF",
    "512400.SH": "有色金属ETF",
    "515210.SH": "钢铁ETF",
    
    # 其他热门
    "512660.SH": "军工ETF",
    "512200.SH": "房地产ETF",
    "515380.SH": "创50ETF",
}


# ============ 得分数据结构 ============

@dataclass
class SectorScore:
    """行业得分"""
    sector_code: str                # 行业代码
    sector_name: str                # 行业名称
    
    # 多周期得分
    short_score: float = 0.0        # 短周期得分
    medium_score: float = 0.0       # 中周期得分
    long_score: float = 0.0         # 长周期得分
    
    # 综合得分
    composite_score: float = 0.0
    
    # 共振状态
    is_resonant: bool = False       # 是否共振
    resonance_direction: str = "neutral"  # bull/bear/neutral
    
    # 排名
    rank: int = 0
    
    # 技术指标
    momentum_20d: float = 0.0       # 20日动量
    momentum_60d: float = 0.0       # 60日动量
    volatility: float = 0.0         # 波动率
    relative_strength: float = 0.0  # 相对强度（vs大盘）
    
    def to_dict(self) -> Dict:
        return {
            "sector_code": self.sector_code,
            "sector_name": self.sector_name,
            "short_score": self.short_score,
            "medium_score": self.medium_score,
            "long_score": self.long_score,
            "composite_score": self.composite_score,
            "is_resonant": self.is_resonant,
            "resonance_direction": self.resonance_direction,
            "rank": self.rank,
            "momentum_20d": self.momentum_20d,
            "momentum_60d": self.momentum_60d,
            "volatility": self.volatility,
            "relative_strength": self.relative_strength,
        }


@dataclass
class ThemeETFScore:
    """主题ETF得分"""
    etf_code: str                   # ETF代码
    etf_name: str                   # ETF名称
    
    # 多周期得分
    short_score: float = 0.0
    medium_score: float = 0.0
    long_score: float = 0.0
    
    # 综合得分
    composite_score: float = 0.0
    
    # 共振状态
    is_resonant: bool = False
    resonance_direction: str = "neutral"
    
    # 排名
    rank: int = 0
    
    # 技术指标
    momentum_20d: float = 0.0
    momentum_60d: float = 0.0
    volatility: float = 0.0
    volume_ratio: float = 0.0       # 量比
    turnover_rate: float = 0.0      # 换手率
    
    def to_dict(self) -> Dict:
        return {
            "etf_code": self.etf_code,
            "etf_name": self.etf_name,
            "short_score": self.short_score,
            "medium_score": self.medium_score,
            "long_score": self.long_score,
            "composite_score": self.composite_score,
            "is_resonant": self.is_resonant,
            "resonance_direction": self.resonance_direction,
            "rank": self.rank,
            "momentum_20d": self.momentum_20d,
            "momentum_60d": self.momentum_60d,
            "volatility": self.volatility,
            "volume_ratio": self.volume_ratio,
            "turnover_rate": self.turnover_rate,
        }


# ============ 行业轮动引擎 ============

class SectorResonanceEngine:
    """
    行业/主题轮动共振引擎
    
    功能：
    1. 对申万一级行业计算共振分数
    2. 对主题ETF池计算共振分数
    3. 输出TopN行业 + TopN主题ETF
    """
    
    def __init__(
        self,
        config: ResonanceConfig = None,
        sector_pool: Dict[str, str] = None,
        etf_pool: Dict[str, str] = None,
    ):
        """
        初始化引擎
        
        Args:
            config: 共振配置
            sector_pool: 行业池 {code: name}，默认申万一级
            etf_pool: ETF池 {code: name}，默认主题ETF池
        """
        self.config = config or ResonanceConfig()
        self.sector_pool = sector_pool or SW_L1_SECTORS
        self.etf_pool = etf_pool or THEME_ETF_POOL
        
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
                        logger.info("SectorResonanceEngine: JQData连接成功")
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
    
    def analyze_sectors(
        self,
        as_of_date: str,
        top_n: int = None,
    ) -> Tuple[List[SectorScore], Dict[str, float]]:
        """
        分析行业共振
        
        Args:
            as_of_date: 分析日期
            top_n: 返回TopN行业，默认使用config
        
        Returns:
            (排序后的行业得分列表, {sector_code: score})
        """
        top_n = top_n or self.config.sector_topn
        scores: List[SectorScore] = []
        score_dict: Dict[str, float] = {}
        
        # 获取基准数据
        benchmark_df = self._get_benchmark_data(as_of_date)
        
        for code, name in self.sector_pool.items():
            score = self._analyze_single_sector(code, name, as_of_date, benchmark_df)
            if score:
                scores.append(score)
                score_dict[code] = score.composite_score
        
        # 排序
        scores.sort(key=lambda x: x.composite_score, reverse=True)
        
        # 更新排名
        for i, s in enumerate(scores):
            s.rank = i + 1
        
        return scores[:top_n], score_dict
    
    def analyze_theme_etfs(
        self,
        as_of_date: str,
        top_n: int = None,
    ) -> Tuple[List[ThemeETFScore], Dict[str, float]]:
        """
        分析主题ETF共振
        
        Args:
            as_of_date: 分析日期
            top_n: 返回TopN ETF，默认使用config
        
        Returns:
            (排序后的ETF得分列表, {etf_code: score})
        """
        top_n = top_n or self.config.theme_topn
        scores: List[ThemeETFScore] = []
        score_dict: Dict[str, float] = {}
        
        # 获取基准数据
        benchmark_df = self._get_benchmark_data(as_of_date)
        
        for code, name in self.etf_pool.items():
            score = self._analyze_single_etf(code, name, as_of_date, benchmark_df)
            if score:
                scores.append(score)
                score_dict[code] = score.composite_score
        
        # 排序
        scores.sort(key=lambda x: x.composite_score, reverse=True)
        
        # 更新排名
        for i, s in enumerate(scores):
            s.rank = i + 1
        
        return scores[:top_n], score_dict
    
    def analyze_full(
        self,
        as_of_date: str,
    ) -> SectorRotationOutput:
        """
        完整分析：行业 + 主题ETF
        
        Args:
            as_of_date: 分析日期
        
        Returns:
            SectorRotationOutput
        """
        # 行业分析
        sector_scores, sector_score_dict = self.analyze_sectors(as_of_date)
        sector_topn = [s.sector_code for s in sector_scores]
        sector_scorecard = [s.to_dict() for s in sector_scores]
        
        # 主题ETF分析
        theme_scores, theme_score_dict = self.analyze_theme_etfs(as_of_date)
        theme_topn = [s.etf_code for s in theme_scores]
        theme_scorecard = [s.to_dict() for s in theme_scores]
        
        return SectorRotationOutput(
            date=as_of_date,
            sector_scores=sector_score_dict,
            sector_topn=sector_topn,
            sector_scorecard=sector_scorecard,
            theme_scores=theme_score_dict,
            theme_topn=theme_topn,
            theme_scorecard=theme_scorecard,
        )
    
    def _analyze_single_sector(
        self,
        code: str,
        name: str,
        as_of_date: str,
        benchmark_df: Optional[pd.DataFrame],
    ) -> Optional[SectorScore]:
        """分析单个行业"""
        # 申万行业指数需要用聚宽的行业指数数据
        # 尝试转换代码格式
        jq_code = self._convert_sw_code(code)
        df = self._get_price_data(jq_code, as_of_date)
        
        if df is None or len(df) < 20:
            return None
        
        try:
            periods = self.config.periods
            
            # 计算各周期得分
            short_score = self._calc_period_score(df, periods.get("short", 5))
            medium_score = self._calc_period_score(df, periods.get("medium", 21))
            long_score = self._calc_period_score(df, periods.get("long", 63))
            
            # 综合得分（加权）
            composite = short_score * 0.2 + medium_score * 0.4 + long_score * 0.4
            
            # 判断共振
            is_resonant, direction = self._check_resonance(short_score, medium_score, long_score)
            
            # 技术指标
            momentum_20d = self._calc_momentum(df, 20)
            momentum_60d = self._calc_momentum(df, 60)
            volatility = self._calc_volatility(df, 20)
            relative_strength = self._calc_relative_strength(df, benchmark_df, 20)
            
            return SectorScore(
                sector_code=code,
                sector_name=name,
                short_score=short_score,
                medium_score=medium_score,
                long_score=long_score,
                composite_score=composite,
                is_resonant=is_resonant,
                resonance_direction=direction,
                momentum_20d=momentum_20d,
                momentum_60d=momentum_60d,
                volatility=volatility,
                relative_strength=relative_strength,
            )
            
        except Exception as e:
            logger.debug(f"分析行业失败 {code}: {e}")
            return None
    
    def _analyze_single_etf(
        self,
        code: str,
        name: str,
        as_of_date: str,
        benchmark_df: Optional[pd.DataFrame],
    ) -> Optional[ThemeETFScore]:
        """分析单个ETF"""
        # ETF代码格式转换
        jq_code = self._convert_etf_code(code)
        df = self._get_price_data(jq_code, as_of_date)
        
        if df is None or len(df) < 20:
            return None
        
        try:
            periods = self.config.periods
            
            # 计算各周期得分
            short_score = self._calc_period_score(df, periods.get("short", 5))
            medium_score = self._calc_period_score(df, periods.get("medium", 21))
            long_score = self._calc_period_score(df, periods.get("long", 63))
            
            # 综合得分
            composite = short_score * 0.25 + medium_score * 0.35 + long_score * 0.40
            
            # 判断共振
            is_resonant, direction = self._check_resonance(short_score, medium_score, long_score)
            
            # 技术指标
            momentum_20d = self._calc_momentum(df, 20)
            momentum_60d = self._calc_momentum(df, 60)
            volatility = self._calc_volatility(df, 20)
            volume_ratio = self._calc_volume_ratio(df)
            turnover_rate = 0.0  # ETF换手率需要额外数据
            
            return ThemeETFScore(
                etf_code=code,
                etf_name=name,
                short_score=short_score,
                medium_score=medium_score,
                long_score=long_score,
                composite_score=composite,
                is_resonant=is_resonant,
                resonance_direction=direction,
                momentum_20d=momentum_20d,
                momentum_60d=momentum_60d,
                volatility=volatility,
                volume_ratio=volume_ratio,
                turnover_rate=turnover_rate,
            )
            
        except Exception as e:
            logger.debug(f"分析ETF失败 {code}: {e}")
            return None
    
    def _convert_sw_code(self, code: str) -> str:
        """转换申万行业指数代码为聚宽格式"""
        # 申万一级行业指数：801010.SI -> 801010.XSHG
        if code.endswith(".SI"):
            return code.replace(".SI", ".XSHG")
        return code
    
    def _convert_etf_code(self, code: str) -> str:
        """转换ETF代码为聚宽格式"""
        # 上交所：512480.SH -> 512480.XSHG
        # 深交所：159995.SZ -> 159995.XSHE
        if code.endswith(".SH"):
            return code.replace(".SH", ".XSHG")
        elif code.endswith(".SZ"):
            return code.replace(".SZ", ".XSHE")
        return code
    
    def _calc_period_score(self, df: pd.DataFrame, period: int) -> float:
        """
        计算周期得分
        
        基于均线、动量、成交量等综合打分
        """
        if len(df) < period:
            return 0.0
        
        close = df['close']
        volume = df['volume']
        
        score = 0.0
        
        # 1. 趋势（均线斜率）
        ma = close.rolling(period).mean()
        if len(ma) >= 5 and ma.iloc[-5] > 0:
            slope = (ma.iloc[-1] - ma.iloc[-5]) / ma.iloc[-5] * 100
            score += np.clip(slope * 10, -30, 30)
        
        # 2. 价格位置
        if len(close) >= period:
            period_high = close.tail(period).max()
            period_low = close.tail(period).min()
            if period_high != period_low:
                position = (close.iloc[-1] - period_low) / (period_high - period_low)
                score += (position - 0.5) * 40  # -20 ~ +20
        
        # 3. 动量
        if len(close) >= period:
            momentum = (close.iloc[-1] / close.iloc[-period] - 1) * 100
            score += np.clip(momentum * 2, -30, 30)
        
        # 4. 成交量趋势
        if len(volume) >= period:
            vol_ma = volume.rolling(period).mean()
            vol_ratio = volume.iloc[-1] / vol_ma.iloc[-1] if vol_ma.iloc[-1] > 0 else 1.0
            if close.iloc[-1] > close.iloc[-2]:
                score += np.clip((vol_ratio - 1) * 20, -10, 20)
            else:
                score -= np.clip((vol_ratio - 1) * 15, -15, 10)
        
        return float(np.clip(score, -100, 100))
    
    def _check_resonance(
        self,
        short: float,
        medium: float,
        long: float,
        threshold: float = 15.0,
    ) -> Tuple[bool, str]:
        """
        检查共振状态
        
        Returns:
            (是否共振, 方向)
        """
        bullish = [short > threshold, medium > threshold, long > threshold]
        bearish = [short < -threshold, medium < -threshold, long < -threshold]
        
        if all(bullish):
            return True, "bull"
        elif all(bearish):
            return True, "bear"
        elif sum(bullish) >= 2:
            return False, "bull"  # 偏多但未共振
        elif sum(bearish) >= 2:
            return False, "bear"  # 偏空但未共振
        else:
            return False, "neutral"
    
    def _calc_momentum(self, df: pd.DataFrame, period: int) -> float:
        """计算动量"""
        if len(df) < period:
            return 0.0
        close = df['close']
        return float((close.iloc[-1] / close.iloc[-period] - 1) * 100)
    
    def _calc_volatility(self, df: pd.DataFrame, period: int) -> float:
        """计算波动率"""
        if len(df) < period:
            return 0.0
        returns = df['close'].pct_change().tail(period)
        return float(returns.std() * np.sqrt(252))  # 年化
    
    def _calc_relative_strength(
        self,
        df: pd.DataFrame,
        benchmark_df: Optional[pd.DataFrame],
        period: int,
    ) -> float:
        """计算相对强度（RS）"""
        if benchmark_df is None or len(df) < period or len(benchmark_df) < period:
            return 0.0
        
        stock_ret = (df['close'].iloc[-1] / df['close'].iloc[-period] - 1) * 100
        bench_ret = (benchmark_df['close'].iloc[-1] / benchmark_df['close'].iloc[-period] - 1) * 100
        
        return float(stock_ret - bench_ret)
    
    def _calc_volume_ratio(self, df: pd.DataFrame, period: int = 5) -> float:
        """计算量比"""
        if len(df) < period + 1:
            return 1.0
        
        volume = df['volume']
        vol_ma = volume.rolling(period).mean()
        
        if vol_ma.iloc[-1] > 0:
            return float(volume.iloc[-1] / vol_ma.iloc[-1])
        return 1.0
    
    def get_investable_sectors(
        self,
        as_of_date: str,
        min_score: float = 0.0,
    ) -> List[str]:
        """
        获取可投资行业列表
        
        Args:
            as_of_date: 分析日期
            min_score: 最小得分阈值
        
        Returns:
            行业代码列表
        """
        scores, _ = self.analyze_sectors(as_of_date, top_n=len(self.sector_pool))
        return [s.sector_code for s in scores if s.composite_score >= min_score]
    
    def get_investable_etfs(
        self,
        as_of_date: str,
        min_score: float = 0.0,
    ) -> List[str]:
        """
        获取可投资ETF列表
        
        Args:
            as_of_date: 分析日期
            min_score: 最小得分阈值
        
        Returns:
            ETF代码列表
        """
        scores, _ = self.analyze_theme_etfs(as_of_date, top_n=len(self.etf_pool))
        return [s.etf_code for s in scores if s.composite_score >= min_score]
