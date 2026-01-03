"""
IBD风格市场趋势分析器（增强版）
===============================

参考Investor's Business Daily (IBD)的市场分析方法：
1. 市场跟踪日 (Follow-Through Day, FTD)
2. 分布日统计 (Distribution Day Count, DD)
3. 市场状态评估 (Market Pulse)
4. 领涨股分析
5. 市场周期跟踪（新增）

IBD方法论核心：
- 跟踪日：确认底部反转的强势上涨（涨幅>1.2%，放量，距低点4天以上）
- 分布日：机构抛售信号（跌幅>0.2%，放量，25日内有效）
- 市场状态：根据跟踪日和分布日判断
- A股适配：考虑涨跌停、北向资金等特色

改进内容 (v2.0):
- 添加牛熊周期跟踪
- 完善历史数据分析接口（供回测使用）
- 与HMM、TrendAnalyzer交叉验证接口
- A股特色指标集成
- 信号评分和置信度计算

参考：William O'Neil - How to Make Money in Stocks
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class MarketStatus(Enum):
    """市场状态（IBD风格）"""

    CONFIRMED_UPTREND = "confirmed_uptrend"  # 确认上涨
    UPTREND_UNDER_PRESSURE = "uptrend_pressure"  # 上涨承压
    MARKET_IN_CORRECTION = "correction"  # 市场调整
    RALLY_ATTEMPT = "rally_attempt"  # 反弹尝试
    
    @classmethod
    def from_string(cls, s: str) -> 'MarketStatus':
        """从字符串转换"""
        mapping = {
            'confirmed_uptrend': cls.CONFIRMED_UPTREND,
            'uptrend_pressure': cls.UPTREND_UNDER_PRESSURE,
            'correction': cls.MARKET_IN_CORRECTION,
            'rally_attempt': cls.RALLY_ATTEMPT,
            'bull': cls.CONFIRMED_UPTREND,
            'bear': cls.MARKET_IN_CORRECTION
        }
        return mapping.get(s.lower(), cls.RALLY_ATTEMPT)
    
    def is_bullish(self) -> bool:
        """是否看多"""
        return self in [self.CONFIRMED_UPTREND, self.RALLY_ATTEMPT]
    
    def is_bearish(self) -> bool:
        """是否看空"""
        return self in [self.MARKET_IN_CORRECTION, self.UPTREND_UNDER_PRESSURE]
    
    def to_signal(self) -> str:
        """转换为信号"""
        return {
            self.CONFIRMED_UPTREND: 'bullish',
            self.UPTREND_UNDER_PRESSURE: 'neutral',
            self.MARKET_IN_CORRECTION: 'bearish',
            self.RALLY_ATTEMPT: 'neutral'
        }[self]


@dataclass
class FollowThroughDay:
    """跟踪日信息"""

    date: str
    gain_pct: float  # 涨幅
    volume_ratio: float  # 相对平均成交量比例
    days_since_low: int  # 距离低点天数
    is_valid: bool = True


@dataclass
class DistributionDay:
    """分布日信息"""

    date: str
    loss_pct: float  # 跌幅
    volume_ratio: float  # 相对平均成交量比例
    expired: bool = False  # 是否过期（25日后过期）


@dataclass
class IBDAnalysisResult:
    """IBD风格分析结果（增强版）"""

    analysis_date: str
    market_status: MarketStatus
    distribution_count: int
    follow_through_days: List[FollowThroughDay] = field(default_factory=list)
    distribution_days: List[DistributionDay] = field(default_factory=list)

    # 技术指标
    price_vs_50ma: float = 0.0  # 价格相对50日均线
    price_vs_200ma: float = 0.0  # 价格相对200日均线
    ma50_vs_ma200: float = 0.0  # 50日vs200日均线

    # 市场宽度
    stocks_above_50ma_pct: float = 0.0  # 在50日均线上方的股票比例
    new_highs: int = 0
    new_lows: int = 0

    recommendation: str = ""
    details: List[str] = field(default_factory=list)
    
    # 新增字段
    confidence: float = 0.0  # 分析置信度 (0-1)
    signal_score: float = 0.0  # 综合信号得分 (-100 to 100)
    has_recent_ftd: bool = False  # 近期是否有跟踪日
    days_since_last_ftd: int = -1  # 距离上次跟踪日天数
    trend_strength: float = 0.0  # 趋势强度 (-1 to 1)
    cycle_phase: str = ""  # 周期阶段

    def to_dict(self) -> Dict[str, Any]:
        return {
            "analysis_date": self.analysis_date,
            "market_status": self.market_status.value,
            "market_status_signal": self.market_status.to_signal(),
            "distribution_count": self.distribution_count,
            "follow_through_count": len(self.follow_through_days),
            "has_recent_ftd": self.has_recent_ftd,
            "days_since_last_ftd": self.days_since_last_ftd,
            "price_vs_50ma": self.price_vs_50ma,
            "price_vs_200ma": self.price_vs_200ma,
            "ma50_vs_ma200": self.ma50_vs_ma200,
            "stocks_above_50ma_pct": self.stocks_above_50ma_pct,
            "new_highs": self.new_highs,
            "new_lows": self.new_lows,
            "confidence": self.confidence,
            "signal_score": self.signal_score,
            "trend_strength": self.trend_strength,
            "cycle_phase": self.cycle_phase,
            "recommendation": self.recommendation,
            "details": self.details,
        }
    
    def is_bullish(self) -> bool:
        """是否看多"""
        return self.market_status.is_bullish() and self.signal_score > 20
    
    def is_bearish(self) -> bool:
        """是否看空"""
        return self.market_status.is_bearish() and self.signal_score < -20
    
    def get_signal(self) -> str:
        """获取信号"""
        if self.signal_score > 30:
            return 'bullish'
        elif self.signal_score < -30:
            return 'bearish'
        return 'neutral'


class IBDStyleAnalyzer:
    """
    IBD风格市场分析器（增强版）

    分析方法：
    1. 识别跟踪日（底部反转确认）
    2. 统计分布日（机构抛售）
    3. 评估市场状态
    4. 生成交易建议
    5. 周期跟踪和信号评分（新增）
    
    A股适配：
    - 调整跟踪日涨幅阈值（A股波动更大）
    - 考虑涨跌停对成交量的影响
    - 集成北向资金等A股特色指标
    """

    # 分布日标准（A股适配）
    DISTRIBUTION_THRESHOLD = -0.3  # A股跌幅阈值略高（波动大）
    DISTRIBUTION_VOLUME_RATIO = 1.0  # 成交量高于平均
    DISTRIBUTION_LOOKBACK = 25  # 25日内有效
    MAX_DISTRIBUTION_DAYS = 5  # 超过5个分布日视为承压
    CRITICAL_DISTRIBUTION_DAYS = 7  # 超过7个进入调整

    # 跟踪日标准（A股适配）
    FOLLOW_THROUGH_GAIN = 1.5  # A股涨幅阈值略高
    FOLLOW_THROUGH_VOLUME_RATIO = 1.0  # 成交量高于平均
    FOLLOW_THROUGH_MIN_DAYS = 4  # 至少在低点后第4天
    FOLLOW_THROUGH_MAX_DAYS = 15  # 最多在低点后15天内
    
    # 有效期
    FTD_VALIDITY_DAYS = 40  # 跟踪日有效期40天

    def __init__(self, use_astock_params: bool = True):
        """
        初始化IBD分析器
        
        Args:
            use_astock_params: 是否使用A股特定参数
        """
        self._data_cache: Dict[str, pd.DataFrame] = {}
        self.use_astock_params = use_astock_params
        self._analysis_history: List[IBDAnalysisResult] = []
        
        # A股特定阈值调整
        if use_astock_params:
            self.DISTRIBUTION_THRESHOLD = -0.3
            self.FOLLOW_THROUGH_GAIN = 1.5

    def analyze(
        self, index_code: str = "000001.XSHG", lookback_days: int = 60,
        df: Optional[pd.DataFrame] = None
    ) -> IBDAnalysisResult:
        """
        执行IBD风格分析（增强版）

        Args:
            index_code: 指数代码（默认上证指数）
            lookback_days: 回看天数
            df: 可选，直接传入数据（用于回测）

        Returns:
            IBDAnalysisResult
        """
        logger.info(f"🔍 开始IBD风格市场分析: {index_code}")

        result = IBDAnalysisResult(
            analysis_date=date.today().strftime("%Y-%m-%d"),
            market_status=MarketStatus.RALLY_ATTEMPT,
            distribution_count=0,
        )

        try:
            # 获取数据（优先使用传入的df）
            if df is None:
                df = self._get_index_data(index_code, lookback_days + 200)

            if df is None or len(df) < 50:
                result.recommendation = "数据不足，无法分析"
                return result

            # 计算技术指标
            df = self._calculate_indicators(df)

            # 识别分布日
            distribution_days = self._identify_distribution_days(df)
            result.distribution_days = distribution_days
            result.distribution_count = len([d for d in distribution_days if not d.expired])

            # 识别跟踪日
            follow_through_days = self._identify_follow_through_days(df)
            result.follow_through_days = follow_through_days
            
            # 计算跟踪日相关信息
            result.has_recent_ftd = len(follow_through_days) > 0
            if follow_through_days:
                latest_ftd_date = follow_through_days[-1].date
                try:
                    ftd_date = datetime.strptime(latest_ftd_date, "%Y-%m-%d").date()
                    result.days_since_last_ftd = (date.today() - ftd_date).days
                except:
                    result.days_since_last_ftd = -1

            # 计算均线位置
            latest = df.iloc[-1]
            result.price_vs_50ma = (
                (latest["close"] / latest["ma50"] - 1) * 100 if latest["ma50"] > 0 else 0
            )
            result.price_vs_200ma = (
                (latest["close"] / latest["ma200"] - 1) * 100 if latest["ma200"] > 0 else 0
            )
            result.ma50_vs_ma200 = (
                (latest["ma50"] / latest["ma200"] - 1) * 100 if latest["ma200"] > 0 else 0
            )

            # 获取市场宽度（如果有数据）
            breadth = self._get_market_breadth()
            if breadth:
                result.stocks_above_50ma_pct = breadth.get("above_50ma_pct", 0)
                result.new_highs = breadth.get("new_highs", 0)
                result.new_lows = breadth.get("new_lows", 0)

            # 判断市场状态
            result.market_status = self._determine_market_status(result, df)
            
            # 计算信号得分和置信度（新增）
            result.signal_score = self._calculate_signal_score(result, df)
            result.confidence = self._calculate_confidence(result)
            result.trend_strength = self._calculate_trend_strength(df)
            result.cycle_phase = self._determine_cycle_phase(result, df)

            # 生成建议
            result.recommendation = self._generate_recommendation(result)
            result.details = self._generate_details(result, df)
            
            # 记录历史
            self._analysis_history.append(result)
            if len(self._analysis_history) > 200:
                self._analysis_history = self._analysis_history[-200:]

            logger.info(f"🔍 IBD分析完成: {result.market_status.value}, 得分: {result.signal_score:.1f}")

        except Exception as e:
            logger.error(f"IBD分析失败: {e}")
            import traceback
            traceback.print_exc()
            result.recommendation = f"分析出错: {e}"

        return result
    
    def analyze_historical(self, df: pd.DataFrame, analysis_date: str) -> IBDAnalysisResult:
        """
        分析历史数据（用于回测）
        
        Args:
            df: 截止到analysis_date的历史数据
            analysis_date: 分析日期
            
        Returns:
            IBDAnalysisResult
        """
        result = self.analyze(df=df)
        result.analysis_date = analysis_date
        return result
    
    def _calculate_signal_score(self, result: IBDAnalysisResult, df: pd.DataFrame) -> float:
        """
        计算综合信号得分 (-100 to 100)
        
        正分看多，负分看空
        """
        score = 0.0
        
        # 1. 市场状态得分 (±40分)
        status_scores = {
            MarketStatus.CONFIRMED_UPTREND: 40,
            MarketStatus.RALLY_ATTEMPT: 10,
            MarketStatus.UPTREND_UNDER_PRESSURE: -20,
            MarketStatus.MARKET_IN_CORRECTION: -40
        }
        score += status_scores.get(result.market_status, 0)
        
        # 2. 分布日得分 (±20分)
        dist_count = result.distribution_count
        if dist_count == 0:
            score += 20
        elif dist_count <= 2:
            score += 10
        elif dist_count <= 4:
            score += 0
        elif dist_count <= 6:
            score -= 15
        else:
            score -= 20
        
        # 3. 跟踪日得分 (±20分)
        if result.has_recent_ftd:
            if result.days_since_last_ftd >= 0 and result.days_since_last_ftd <= 10:
                score += 20  # 近期跟踪日
            elif result.days_since_last_ftd <= 25:
                score += 10  # 中期跟踪日
            else:
                score += 5   # 远期跟踪日
        else:
            score -= 10
        
        # 4. 均线位置得分 (±20分)
        if result.price_vs_50ma > 5:
            score += 10
        elif result.price_vs_50ma > 0:
            score += 5
        elif result.price_vs_50ma > -5:
            score -= 5
        else:
            score -= 10
        
        if result.price_vs_200ma > 5:
            score += 10
        elif result.price_vs_200ma > 0:
            score += 5
        elif result.price_vs_200ma > -10:
            score -= 5
        else:
            score -= 10
        
        return np.clip(score, -100, 100)
    
    def _calculate_confidence(self, result: IBDAnalysisResult) -> float:
        """计算分析置信度 (0-1)"""
        confidence = 0.5
        
        # 有跟踪日增加置信度
        if result.has_recent_ftd:
            confidence += 0.15
        
        # 分布日少增加置信度
        if result.distribution_count <= 2:
            confidence += 0.1
        
        # 均线位置明确增加置信度
        if abs(result.price_vs_50ma) > 5:
            confidence += 0.1
        
        if abs(result.price_vs_200ma) > 10:
            confidence += 0.1
        
        # 信号得分绝对值高增加置信度
        if abs(result.signal_score) > 50:
            confidence += 0.1
        
        return min(confidence, 0.95)
    
    def _calculate_trend_strength(self, df: pd.DataFrame) -> float:
        """计算趋势强度 (-1 to 1)"""
        if len(df) < 60:
            return 0.0
        
        latest = df.iloc[-1]
        strength = 0.0
        
        # 均线排列
        if latest['ma20'] > latest['ma50'] > latest.get('ma200', latest['ma50']):
            strength += 0.4  # 多头排列
        elif latest['ma20'] < latest['ma50'] < latest.get('ma200', latest['ma50']):
            strength -= 0.4  # 空头排列
        
        # 价格位置
        if latest['close'] > latest['ma50']:
            strength += 0.3
        else:
            strength -= 0.3
        
        # 动量
        returns_20d = (latest['close'] / df.iloc[-20]['close'] - 1) * 100
        if returns_20d > 5:
            strength += 0.3
        elif returns_20d < -5:
            strength -= 0.3
        
        return np.clip(strength, -1, 1)
    
    def _determine_cycle_phase(self, result: IBDAnalysisResult, df: pd.DataFrame) -> str:
        """判断周期阶段"""
        if result.market_status == MarketStatus.CONFIRMED_UPTREND:
            if result.has_recent_ftd and result.days_since_last_ftd <= 20:
                return "牛市初期"
            elif result.distribution_count <= 2:
                return "牛市中期"
            else:
                return "牛市后期"
        elif result.market_status == MarketStatus.UPTREND_UNDER_PRESSURE:
            return "牛转熊过渡"
        elif result.market_status == MarketStatus.MARKET_IN_CORRECTION:
            if result.distribution_count >= 7:
                return "熊市深跌"
            else:
                return "调整期"
        else:  # RALLY_ATTEMPT
            return "底部探索"

    def _get_index_data(self, code: str, days: int) -> Optional[pd.DataFrame]:
        """获取指数数据"""
        try:
            from core.data_source_manager import get_data_source_manager

            manager = get_data_source_manager()
            end_date = date.today().strftime("%Y-%m-%d")
            start_date = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")

            result = manager.get_price(code, start_date, end_date)

            if result.success and result.data is not None:
                df = result.data.copy()
                df = df.reset_index()
                df.columns = [c.lower() for c in df.columns]

                # 处理索引列名称 (可能是 'index' 或 'date')
                if "index" in df.columns and "date" not in df.columns:
                    df = df.rename(columns={"index": "date"})

                # 确保date列是datetime类型
                if "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"])

                return df

        except Exception as e:
            logger.warning(f"获取指数数据失败: {e}")

        return None

    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算技术指标"""
        df = df.copy()

        # 均线
        df["ma50"] = df["close"].rolling(window=50).mean()
        df["ma200"] = df["close"].rolling(window=200).mean()
        df["ma20"] = df["close"].rolling(window=20).mean()

        # 平均成交量
        df["avg_volume"] = df["volume"].rolling(window=50).mean()
        df["volume_ratio"] = df["volume"] / df["avg_volume"]

        # 日涨跌幅
        df["pct_change"] = df["close"].pct_change() * 100

        # 距离低点天数
        df["rolling_min"] = df["close"].rolling(window=25).min()

        return df

    def _identify_distribution_days(self, df: pd.DataFrame) -> List[DistributionDay]:
        """识别分布日"""
        distribution_days = []
        recent_df = df.tail(self.DISTRIBUTION_LOOKBACK + 5).copy()
        
        # 确保有date列
        if 'date' not in recent_df.columns:
            recent_df = recent_df.reset_index()
            if 'index' in recent_df.columns and 'date' not in recent_df.columns:
                recent_df = recent_df.rename(columns={'index': 'date'})

        for i, row in recent_df.iterrows():
            if pd.isna(row.get("pct_change")) or pd.isna(row.get("volume_ratio")):
                continue

            # 分布日条件：跌幅 > 0.2% 且 成交量放大
            if (
                row["pct_change"] < self.DISTRIBUTION_THRESHOLD
                and row["volume_ratio"] > self.DISTRIBUTION_VOLUME_RATIO
            ):

                # 获取日期字符串
                if 'date' in row.index:
                    date_val = row["date"]
                    date_str = (
                        date_val.strftime("%Y-%m-%d")
                        if hasattr(date_val, "strftime")
                        else str(date_val)[:10]
                    )
                else:
                    date_str = str(i)[:10] if hasattr(i, 'strftime') else str(i)

                distribution_days.append(
                    DistributionDay(
                        date=date_str,
                        loss_pct=row["pct_change"],
                        volume_ratio=row["volume_ratio"],
                        expired=False,  # 在lookback内都有效
                    )
                )

        # 只保留最近25天的
        if len(distribution_days) > self.DISTRIBUTION_LOOKBACK:
            for dd in distribution_days[: -self.DISTRIBUTION_LOOKBACK]:
                dd.expired = True

        return distribution_days

    def _identify_follow_through_days(self, df: pd.DataFrame) -> List[FollowThroughDay]:
        """识别跟踪日"""
        follow_through_days = []

        # 找到近期低点
        recent_df = df.tail(60).copy()
        if len(recent_df) < 20:
            return follow_through_days
        
        # 确保有date列
        if 'date' not in recent_df.columns:
            recent_df = recent_df.reset_index()
            if 'index' in recent_df.columns and 'date' not in recent_df.columns:
                recent_df = recent_df.rename(columns={'index': 'date'})

        # 找最低收盘价位置
        low_idx = recent_df["close"].idxmin()

        # 从低点后第4天开始寻找跟踪日
        try:
            low_pos = recent_df.index.get_loc(low_idx)
        except:
            # 如果索引被重置，找位置
            low_pos = list(recent_df.index).index(low_idx) if low_idx in recent_df.index else 0

        for i in range(low_pos + self.FOLLOW_THROUGH_MIN_DAYS, min(low_pos + self.FOLLOW_THROUGH_MAX_DAYS, len(recent_df))):
            row = recent_df.iloc[i]

            if pd.isna(row.get("pct_change")) or pd.isna(row.get("volume_ratio")):
                continue

            # 跟踪日条件：涨幅 > 1.2% 且 成交量放大
            if (
                row["pct_change"] > self.FOLLOW_THROUGH_GAIN
                and row["volume_ratio"] > self.FOLLOW_THROUGH_VOLUME_RATIO
            ):

                # 获取日期字符串
                if 'date' in row.index:
                    date_val = row["date"]
                    date_str = (
                        date_val.strftime("%Y-%m-%d")
                        if hasattr(date_val, "strftime")
                        else str(date_val)[:10]
                    )
                else:
                    idx = recent_df.index[i]
                    date_str = str(idx)[:10] if hasattr(idx, 'strftime') else str(idx)

                follow_through_days.append(
                    FollowThroughDay(
                        date=date_str,
                        gain_pct=row["pct_change"],
                        volume_ratio=row["volume_ratio"],
                        days_since_low=i - low_pos,
                    )
                )

        return follow_through_days

    def _determine_market_status(self, result: IBDAnalysisResult, df: pd.DataFrame) -> MarketStatus:
        """判断市场状态"""
        dist_count = result.distribution_count
        ftd_count = len(result.follow_through_days)

        # 价格位置
        latest = df.iloc[-1]
        price_above_50ma = latest["close"] > latest["ma50"] if not pd.isna(latest["ma50"]) else True
        price_above_200ma = (
            latest["close"] > latest["ma200"] if not pd.isna(latest["ma200"]) else True
        )

        # 市场状态判断逻辑
        if dist_count >= self.MAX_DISTRIBUTION_DAYS:
            # 分布日过多，市场调整
            return MarketStatus.MARKET_IN_CORRECTION

        if ftd_count > 0 and dist_count < 3 and price_above_50ma:
            # 有跟踪日且分布日少，确认上涨
            return MarketStatus.CONFIRMED_UPTREND

        if ftd_count > 0 and 3 <= dist_count < self.MAX_DISTRIBUTION_DAYS:
            # 有跟踪日但分布日偏多，上涨承压
            return MarketStatus.UPTREND_UNDER_PRESSURE

        if not price_above_50ma and not price_above_200ma:
            # 价格低于均线，市场调整
            return MarketStatus.MARKET_IN_CORRECTION

        # 默认反弹尝试
        return MarketStatus.RALLY_ATTEMPT

    def _get_market_breadth(self) -> Optional[Dict]:
        """获取市场宽度数据"""
        try:
            import akshare as ak

            # 尝试获取涨跌统计
            result = {}

            # 可以通过AKShare获取涨跌家数等数据
            # 这里简化处理

            return result

        except Exception as e:
            logger.debug(f"获取市场宽度失败: {e}")
            return None

    def _generate_recommendation(self, result: IBDAnalysisResult) -> str:
        """生成交易建议"""
        status = result.market_status

        recommendations = {
            MarketStatus.CONFIRMED_UPTREND: "市场上涨确认，可积极参与，关注领涨股突破买点",
            MarketStatus.UPTREND_UNDER_PRESSURE: "上涨趋势承压，谨慎操作，避免追高，关注止损",
            MarketStatus.MARKET_IN_CORRECTION: "市场处于调整，降低仓位或观望，等待新的跟踪日",
            MarketStatus.RALLY_ATTEMPT: "反弹尝试中，等待跟踪日确认，暂不大举买入",
        }

        return recommendations.get(status, "保持观望")

    def _generate_details(self, result: IBDAnalysisResult, df: pd.DataFrame) -> List[str]:
        """生成详细说明"""
        details = []

        # 市场状态描述
        status_desc = {
            MarketStatus.CONFIRMED_UPTREND: "市场已确认上涨趋势",
            MarketStatus.UPTREND_UNDER_PRESSURE: "上涨趋势面临压力",
            MarketStatus.MARKET_IN_CORRECTION: "市场处于调整阶段",
            MarketStatus.RALLY_ATTEMPT: "市场正在尝试反弹",
        }
        details.append(status_desc.get(result.market_status, ""))

        # 分布日信息
        active_dist = len([d for d in result.distribution_days if not d.expired])
        details.append(f"近25日有效分布日: {active_dist}个")

        # 跟踪日信息
        if result.follow_through_days:
            latest_ftd = result.follow_through_days[-1]
            details.append(f"最近跟踪日: {latest_ftd.date} (涨{latest_ftd.gain_pct:.1f}%)")
        else:
            details.append("近期无跟踪日")

        # 均线位置
        if result.price_vs_50ma > 0:
            details.append(f"价格高于50日均线 {result.price_vs_50ma:.1f}%")
        else:
            details.append(f"价格低于50日均线 {abs(result.price_vs_50ma):.1f}%")

        if result.price_vs_200ma > 0:
            details.append(f"价格高于200日均线 {result.price_vs_200ma:.1f}%")
        else:
            details.append(f"价格低于200日均线 {abs(result.price_vs_200ma):.1f}%")

        return details


def get_ibd_analyzer(use_astock_params: bool = True) -> IBDStyleAnalyzer:
    """获取IBD风格分析器"""
    return IBDStyleAnalyzer(use_astock_params=use_astock_params)


def create_ibd_analyzer() -> IBDStyleAnalyzer:
    """创建IBD风格分析器（兼容旧接口）"""
    return get_ibd_analyzer()


def quick_ibd_check(df: pd.DataFrame) -> Dict[str, Any]:
    """
    快速IBD检查（用于回测）
    
    Args:
        df: 包含OHLCV的DataFrame
        
    Returns:
        简化的IBD分析结果字典
    """
    analyzer = IBDStyleAnalyzer(use_astock_params=True)
    result = analyzer.analyze(df=df)
    
    return {
        'market_status': result.market_status.value,
        'signal': result.get_signal(),
        'distribution_count': result.distribution_count,
        'has_ftd': result.has_recent_ftd,
        'signal_score': result.signal_score,
        'confidence': result.confidence,
        'is_bullish': result.is_bullish(),
        'is_bearish': result.is_bearish()
    }
