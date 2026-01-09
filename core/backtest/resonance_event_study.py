"""
Resonance Event Study - 共振阶段事件研究回测
==============================================

核心功能：
1. 划分共振阶段（确认/预确认/非共振）
2. 计算各阶段的前向收益、最大回撤、波动率、胜率
3. 分组对比统计
4. 输出可复现实验结果

参考：事件研究法（Event Study）、A股行情特点
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

from core.resonance_state_model import (
    ResonanceConfig,
    ResonancePhase,
    MarketSwitchOutput,
)
from core.market_trend_analyzer import (
    MarketTrendAnalyzer,
    MarketTrendAnalyzerConfig,
    MarketTrendSignal,
)

logger = logging.getLogger(__name__)


# ============ 事件研究数据结构 ============

@dataclass
class EventStudyResult:
    """单次事件研究结果"""
    date: str                           # 事件日期
    phase: str                          # 共振阶段
    confirm_streak: int                 # 确认次数
    
    # 前向收益（%）
    forward_return_5d: float = 0.0
    forward_return_20d: float = 0.0
    forward_return_60d: float = 0.0
    
    # 最大回撤（%）
    max_drawdown_5d: float = 0.0
    max_drawdown_20d: float = 0.0
    max_drawdown_60d: float = 0.0
    
    # 波动率（年化）
    volatility_20d: float = 0.0
    
    # 其他指标
    win_5d: bool = False                # 5日是否盈利
    win_20d: bool = False               # 20日是否盈利
    win_60d: bool = False               # 60日是否盈利
    
    def to_dict(self) -> Dict:
        return {
            "date": self.date,
            "phase": self.phase,
            "confirm_streak": self.confirm_streak,
            "forward_return_5d": self.forward_return_5d,
            "forward_return_20d": self.forward_return_20d,
            "forward_return_60d": self.forward_return_60d,
            "max_drawdown_5d": self.max_drawdown_5d,
            "max_drawdown_20d": self.max_drawdown_20d,
            "max_drawdown_60d": self.max_drawdown_60d,
            "volatility_20d": self.volatility_20d,
            "win_5d": self.win_5d,
            "win_20d": self.win_20d,
            "win_60d": self.win_60d,
        }


@dataclass
class GroupStats:
    """分组统计结果"""
    group_name: str                     # 分组名称
    count: int                          # 样本数
    
    # 平均前向收益
    avg_return_5d: float = 0.0
    avg_return_20d: float = 0.0
    avg_return_60d: float = 0.0
    
    # 收益标准差
    std_return_5d: float = 0.0
    std_return_20d: float = 0.0
    std_return_60d: float = 0.0
    
    # 平均最大回撤
    avg_drawdown_5d: float = 0.0
    avg_drawdown_20d: float = 0.0
    avg_drawdown_60d: float = 0.0
    
    # 胜率
    win_rate_5d: float = 0.0
    win_rate_20d: float = 0.0
    win_rate_60d: float = 0.0
    
    # 夏普比率（简化）
    sharpe_20d: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "group_name": self.group_name,
            "count": self.count,
            "avg_return_5d": self.avg_return_5d,
            "avg_return_20d": self.avg_return_20d,
            "avg_return_60d": self.avg_return_60d,
            "std_return_5d": self.std_return_5d,
            "std_return_20d": self.std_return_20d,
            "std_return_60d": self.std_return_60d,
            "avg_drawdown_5d": self.avg_drawdown_5d,
            "avg_drawdown_20d": self.avg_drawdown_20d,
            "avg_drawdown_60d": self.avg_drawdown_60d,
            "win_rate_5d": self.win_rate_5d,
            "win_rate_20d": self.win_rate_20d,
            "win_rate_60d": self.win_rate_60d,
            "sharpe_20d": self.sharpe_20d,
        }


@dataclass
class EventStudySummary:
    """事件研究汇总结果"""
    index_code: str                     # 指数代码
    start_date: str                     # 开始日期
    end_date: str                       # 结束日期
    total_samples: int                  # 总样本数
    
    # 分组统计
    group_stats: Dict[str, GroupStats] = field(default_factory=dict)
    
    # 详细结果
    results: List[EventStudyResult] = field(default_factory=list)
    
    # 比较统计
    comparison: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "index_code": self.index_code,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_samples": self.total_samples,
            "group_stats": {k: v.to_dict() for k, v in self.group_stats.items()},
            "comparison": self.comparison,
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        """转换为DataFrame"""
        return pd.DataFrame([r.to_dict() for r in self.results])


# ============ 事件研究引擎 ============

class ResonanceEventStudy:
    """
    共振阶段事件研究引擎
    
    功能：
    1. 运行MarketTrendAnalyzer获取历史共振信号
    2. 划分阶段：confirmed (>=2), preconfirm (1), non-resonant (0)
    3. 计算各阶段的前向表现
    4. 输出分组对比统计
    """
    
    # 分组定义
    GROUP_DEFINITIONS = {
        "confirmed_bull": lambda p, s, c: p in ["全周期共振-牛", "部分共振-牛"] and c >= 2,
        "preconfirm_bull": lambda p, s, c: p in ["全周期共振-牛", "部分共振-牛"] and c == 1,
        "confirmed_bear": lambda p, s, c: p in ["全周期共振-熊", "部分共振-熊"] and c >= 2,
        "preconfirm_bear": lambda p, s, c: p in ["全周期共振-熊", "部分共振-熊"] and c == 1,
        "divergent": lambda p, s, c: p == "周期分歧",
        "non_resonant": lambda p, s, c: c == 0,
    }
    
    def __init__(
        self,
        analyzer: MarketTrendAnalyzer = None,
        config: ResonanceConfig = None,
    ):
        """
        初始化引擎
        
        Args:
            analyzer: MarketTrendAnalyzer实例
            config: 共振配置
        """
        self.analyzer = analyzer or MarketTrendAnalyzer()
        self.config = config or ResonanceConfig()
        
        self._jq = None
        self._price_cache: Dict[str, pd.DataFrame] = {}
    
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
                        logger.info("ResonanceEventStudy: JQData连接成功")
            except Exception as e:
                logger.warning(f"JQData连接失败: {e}")
    
    def _get_price_data(
        self,
        index_code: str,
        start_date: str,
        end_date: str,
    ) -> Optional[pd.DataFrame]:
        """获取价格数据"""
        cache_key = f"{index_code}_{start_date}_{end_date}"
        if cache_key in self._price_cache:
            return self._price_cache[cache_key]
        
        self._ensure_jqdata()
        if self._jq is None:
            return None
        
        try:
            df = self._jq.get_price(
                index_code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume']
            )
            
            if df is not None and not df.empty:
                df = df.reset_index()
                if 'index' in df.columns:
                    df = df.rename(columns={'index': 'date'})
                self._price_cache[cache_key] = df
                return df
                
        except Exception as e:
            logger.error(f"获取价格数据失败 {index_code}: {e}")
        
        return None
    
    def run_event_study(
        self,
        index_code: str,
        start_date: str,
        end_date: str,
        forward_days: List[int] = None,
    ) -> EventStudySummary:
        """
        运行事件研究
        
        Args:
            index_code: 指数代码
            start_date: 开始日期
            end_date: 结束日期
            forward_days: 前向天数列表，默认[5, 20, 60]
        
        Returns:
            EventStudySummary
        """
        forward_days = forward_days or [5, 20, 60]
        
        # 1. 获取价格数据（需要额外的前向天数）
        extended_end = self._add_trading_days(end_date, max(forward_days) + 10)
        price_df = self._get_price_data(index_code, start_date, extended_end)
        
        if price_df is None or len(price_df) < 100:
            logger.error("价格数据不足")
            return EventStudySummary(
                index_code=index_code,
                start_date=start_date,
                end_date=end_date,
                total_samples=0,
            )
        
        # 2. 获取交易日列表
        trading_dates = self._get_trading_dates(start_date, end_date)
        
        # 3. 运行共振分析
        logger.info(f"运行共振分析: {len(trading_dates)}个交易日")
        signals = self.analyzer.batch_analyze_composite(trading_dates)
        
        if not signals:
            logger.warning("无有效共振信号")
            return EventStudySummary(
                index_code=index_code,
                start_date=start_date,
                end_date=end_date,
                total_samples=0,
            )
        
        # 4. 计算前向表现
        results: List[EventStudyResult] = []
        
        for signal in signals:
            result = self._calculate_forward_performance(
                signal, price_df, forward_days
            )
            if result:
                results.append(result)
        
        # 5. 分组统计
        group_stats = self._calculate_group_stats(results)
        
        # 6. 比较统计
        comparison = self._calculate_comparison(group_stats)
        
        return EventStudySummary(
            index_code=index_code,
            start_date=start_date,
            end_date=end_date,
            total_samples=len(results),
            group_stats=group_stats,
            results=results,
            comparison=comparison,
        )
    
    def _calculate_forward_performance(
        self,
        signal: MarketTrendSignal,
        price_df: pd.DataFrame,
        forward_days: List[int],
    ) -> Optional[EventStudyResult]:
        """计算单个信号的前向表现"""
        try:
            event_date = signal.date
            
            # 找到事件日期的索引
            price_df['date_str'] = price_df['date'].astype(str).str[:10]
            idx = price_df[price_df['date_str'] == event_date].index
            
            if len(idx) == 0:
                return None
            
            event_idx = idx[0]
            event_price = price_df.loc[event_idx, 'close']
            
            # 获取阶段信息
            phase = signal.resonance_phase.value if signal.resonance_phase else "周期分歧"
            confirm_streak = signal.confirm_streak
            
            result = EventStudyResult(
                date=event_date,
                phase=phase,
                confirm_streak=confirm_streak,
            )
            
            # 计算各期限的前向表现
            for days in forward_days:
                future_idx = event_idx + days
                
                if future_idx >= len(price_df):
                    continue
                
                future_price = price_df.loc[future_idx, 'close']
                forward_return = (future_price / event_price - 1) * 100
                
                # 计算期间最大回撤
                period_prices = price_df.loc[event_idx:future_idx, 'close']
                max_drawdown = self._calculate_max_drawdown(period_prices)
                
                if days == 5:
                    result.forward_return_5d = forward_return
                    result.max_drawdown_5d = max_drawdown
                    result.win_5d = forward_return > 0
                elif days == 20:
                    result.forward_return_20d = forward_return
                    result.max_drawdown_20d = max_drawdown
                    result.win_20d = forward_return > 0
                    
                    # 计算波动率
                    returns = period_prices.pct_change().dropna()
                    result.volatility_20d = float(returns.std() * np.sqrt(252))
                elif days == 60:
                    result.forward_return_60d = forward_return
                    result.max_drawdown_60d = max_drawdown
                    result.win_60d = forward_return > 0
            
            return result
            
        except Exception as e:
            logger.debug(f"计算前向表现失败: {e}")
            return None
    
    def _calculate_max_drawdown(self, prices: pd.Series) -> float:
        """计算最大回撤"""
        if len(prices) < 2:
            return 0.0
        
        cummax = prices.cummax()
        drawdown = (prices - cummax) / cummax * 100
        return float(drawdown.min())
    
    def _calculate_group_stats(
        self,
        results: List[EventStudyResult],
    ) -> Dict[str, GroupStats]:
        """计算分组统计"""
        groups: Dict[str, List[EventStudyResult]] = {
            "confirmed_bull": [],
            "preconfirm_bull": [],
            "confirmed_bear": [],
            "preconfirm_bear": [],
            "divergent": [],
            "non_resonant": [],
        }
        
        # 分组
        for r in results:
            for group_name, condition in self.GROUP_DEFINITIONS.items():
                if condition(r.phase, 0, r.confirm_streak):
                    groups[group_name].append(r)
                    break
        
        # 统计
        stats = {}
        for group_name, group_results in groups.items():
            if not group_results:
                continue
            
            stats[group_name] = self._calc_single_group_stats(group_name, group_results)
        
        return stats
    
    def _calc_single_group_stats(
        self,
        group_name: str,
        results: List[EventStudyResult],
    ) -> GroupStats:
        """计算单个分组的统计"""
        n = len(results)
        
        returns_5d = [r.forward_return_5d for r in results]
        returns_20d = [r.forward_return_20d for r in results]
        returns_60d = [r.forward_return_60d for r in results]
        
        drawdowns_5d = [r.max_drawdown_5d for r in results]
        drawdowns_20d = [r.max_drawdown_20d for r in results]
        drawdowns_60d = [r.max_drawdown_60d for r in results]
        
        wins_5d = [r.win_5d for r in results]
        wins_20d = [r.win_20d for r in results]
        wins_60d = [r.win_60d for r in results]
        
        # 计算夏普比率（简化）
        avg_20d = np.mean(returns_20d)
        std_20d = np.std(returns_20d)
        sharpe = avg_20d / std_20d if std_20d > 0 else 0
        
        return GroupStats(
            group_name=group_name,
            count=n,
            avg_return_5d=float(np.mean(returns_5d)),
            avg_return_20d=float(np.mean(returns_20d)),
            avg_return_60d=float(np.mean(returns_60d)),
            std_return_5d=float(np.std(returns_5d)),
            std_return_20d=float(np.std(returns_20d)),
            std_return_60d=float(np.std(returns_60d)),
            avg_drawdown_5d=float(np.mean(drawdowns_5d)),
            avg_drawdown_20d=float(np.mean(drawdowns_20d)),
            avg_drawdown_60d=float(np.mean(drawdowns_60d)),
            win_rate_5d=float(np.mean(wins_5d)),
            win_rate_20d=float(np.mean(wins_20d)),
            win_rate_60d=float(np.mean(wins_60d)),
            sharpe_20d=float(sharpe),
        )
    
    def _calculate_comparison(
        self,
        group_stats: Dict[str, GroupStats],
    ) -> Dict[str, Any]:
        """计算组间比较"""
        comparison = {}
        
        # 确认牛 vs 非共振
        if "confirmed_bull" in group_stats and "non_resonant" in group_stats:
            bull = group_stats["confirmed_bull"]
            non = group_stats["non_resonant"]
            
            comparison["bull_vs_non_resonant"] = {
                "return_diff_20d": bull.avg_return_20d - non.avg_return_20d,
                "drawdown_diff_20d": bull.avg_drawdown_20d - non.avg_drawdown_20d,
                "win_rate_diff_20d": bull.win_rate_20d - non.win_rate_20d,
                "sharpe_diff": bull.sharpe_20d - non.sharpe_20d,
            }
        
        # 确认熊 vs 非共振
        if "confirmed_bear" in group_stats and "non_resonant" in group_stats:
            bear = group_stats["confirmed_bear"]
            non = group_stats["non_resonant"]
            
            comparison["bear_vs_non_resonant"] = {
                "return_diff_20d": bear.avg_return_20d - non.avg_return_20d,
                "drawdown_diff_20d": bear.avg_drawdown_20d - non.avg_drawdown_20d,
                "win_rate_diff_20d": bear.win_rate_20d - non.win_rate_20d,
                "sharpe_diff": bear.sharpe_20d - non.sharpe_20d,
            }
        
        # 确认 vs 预确认
        if "confirmed_bull" in group_stats and "preconfirm_bull" in group_stats:
            conf = group_stats["confirmed_bull"]
            pre = group_stats["preconfirm_bull"]
            
            comparison["confirmed_vs_preconfirm_bull"] = {
                "return_diff_20d": conf.avg_return_20d - pre.avg_return_20d,
                "win_rate_diff_20d": conf.win_rate_20d - pre.win_rate_20d,
            }
        
        return comparison
    
    def _get_trading_dates(self, start_date: str, end_date: str) -> List[str]:
        """获取交易日列表"""
        self._ensure_jqdata()
        if self._jq is None:
            # 回退：简单生成日期
            dates = []
            current = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            while current <= end:
                if current.weekday() < 5:  # 简单排除周末
                    dates.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)
            return dates
        
        try:
            dates = self._jq.get_trade_days(start_date=start_date, end_date=end_date)
            return [d.strftime("%Y-%m-%d") for d in dates]
        except:
            return []
    
    def _add_trading_days(self, date_str: str, days: int) -> str:
        """添加交易日"""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            # 简化：假设1.5倍日历日
            dt = dt + timedelta(days=int(days * 1.5))
            return dt.strftime("%Y-%m-%d")
        except:
            return date_str
    
    def generate_report(
        self,
        summary: EventStudySummary,
    ) -> str:
        """
        生成文字报告
        
        Args:
            summary: 事件研究汇总
        
        Returns:
            报告文本
        """
        lines = [
            "=" * 60,
            "共振阶段事件研究报告",
            "=" * 60,
            f"指数代码: {summary.index_code}",
            f"研究期间: {summary.start_date} ~ {summary.end_date}",
            f"总样本数: {summary.total_samples}",
            "",
            "-" * 60,
            "分组统计",
            "-" * 60,
        ]
        
        for group_name, stats in summary.group_stats.items():
            lines.append(f"\n【{group_name}】(n={stats.count})")
            lines.append(f"  平均收益 - 5日: {stats.avg_return_5d:.2f}%, 20日: {stats.avg_return_20d:.2f}%, 60日: {stats.avg_return_60d:.2f}%")
            lines.append(f"  平均回撤 - 5日: {stats.avg_drawdown_5d:.2f}%, 20日: {stats.avg_drawdown_20d:.2f}%, 60日: {stats.avg_drawdown_60d:.2f}%")
            lines.append(f"  胜    率 - 5日: {stats.win_rate_5d:.1%}, 20日: {stats.win_rate_20d:.1%}, 60日: {stats.win_rate_60d:.1%}")
            lines.append(f"  夏普比率 - 20日: {stats.sharpe_20d:.2f}")
        
        if summary.comparison:
            lines.append("")
            lines.append("-" * 60)
            lines.append("组间比较")
            lines.append("-" * 60)
            
            for comp_name, comp_stats in summary.comparison.items():
                lines.append(f"\n【{comp_name}】")
                for k, v in comp_stats.items():
                    lines.append(f"  {k}: {v:.2f}")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
