# -*- coding: utf-8 -*-
"""
主题周期判断器 V1.0
==================

功能:
1. 判断主题/主线所处的周期阶段
2. 基于周期阶段调整策略参数
3. 提供不同周期的因子权重配置

主题周期定义:
- EARLY (初期): 龙头启动，1-3天，跟风股滞后
- MIDDLE (中期): 板块扩散，1-2周，涨停家数增加
- LATE (后期): 分化加剧，2-3周+，龙头高位震荡
- EXHAUSTED (衰竭): 龙头见顶，风险释放

数据源: JQData (聚宽)

作者: TRQuant Team
版本: V1.0
日期: 2026-01-12
"""

from __future__ import annotations

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# ============== 数据结构 ==============

class ThemeCycle(Enum):
    """主题周期"""
    EARLY = "early"           # 初期: 龙头启动, 1-3天
    MIDDLE = "middle"         # 中期: 板块扩散, 1-2周
    LATE = "late"             # 后期: 分化加剧, 2-3周+
    EXHAUSTED = "exhausted"   # 衰竭: 龙头见顶
    UNKNOWN = "unknown"       # 未知


@dataclass
class CycleParams:
    """周期参数配置"""
    cycle: ThemeCycle
    
    # 仓位配置
    position_cap: float = 0.8       # 仓位上限
    single_position_max: float = 0.2 # 单只上限
    max_positions: int = 5          # 最大持仓数
    
    # 止损止盈
    stop_loss_pct: float = -0.10    # 止损
    take_profit_pct: float = 0.30   # 止盈
    trailing_stop_pct: float = -0.09 # 移动止损
    
    # 信号权重
    signal_weights: Dict[str, float] = field(default_factory=dict)
    
    # 说明
    description: str = ""


# 周期参数映射表
CYCLE_PARAMS_MAP: Dict[ThemeCycle, CycleParams] = {
    ThemeCycle.EARLY: CycleParams(
        cycle=ThemeCycle.EARLY,
        position_cap=0.60,
        single_position_max=0.15,
        max_positions=5,
        stop_loss_pct=-0.08,
        take_profit_pct=0.25,
        trailing_stop_pct=-0.07,
        signal_weights={
            "first_limit_up": 0.35,      # 初期重视首板
            "consecutive_limit": 0.25,
            "strong_breakout": 0.20,
            "vol_price_rise": 0.20,
        },
        description="初期: 龙头刚启动，仓位谨慎，重视首板信号"
    ),
    ThemeCycle.MIDDLE: CycleParams(
        cycle=ThemeCycle.MIDDLE,
        position_cap=0.80,
        single_position_max=0.20,
        max_positions=5,
        stop_loss_pct=-0.10,
        take_profit_pct=0.35,
        trailing_stop_pct=-0.09,
        signal_weights={
            "first_limit_up": 0.15,      # 中期首板机会减少
            "consecutive_limit": 0.30,   # 连板加速更重要
            "strong_breakout": 0.30,
            "vol_price_rise": 0.25,
        },
        description="中期: 板块扩散，可加仓，重视连板和突破"
    ),
    ThemeCycle.LATE: CycleParams(
        cycle=ThemeCycle.LATE,
        position_cap=0.50,
        single_position_max=0.15,
        max_positions=4,
        stop_loss_pct=-0.07,
        take_profit_pct=0.20,
        trailing_stop_pct=-0.06,
        signal_weights={
            "first_limit_up": 0.10,      # 后期首板风险高
            "consecutive_limit": 0.15,
            "strong_breakout": 0.35,     # 强势突破更安全
            "vol_price_rise": 0.40,      # 量价齐升更可靠
        },
        description="后期: 分化加剧，控制仓位，重视量价信号"
    ),
    ThemeCycle.EXHAUSTED: CycleParams(
        cycle=ThemeCycle.EXHAUSTED,
        position_cap=0.20,
        single_position_max=0.10,
        max_positions=3,
        stop_loss_pct=-0.05,
        take_profit_pct=0.15,
        trailing_stop_pct=-0.04,
        signal_weights={
            "first_limit_up": 0.05,
            "consecutive_limit": 0.10,
            "strong_breakout": 0.40,
            "vol_price_rise": 0.45,
        },
        description="衰竭: 龙头见顶，大幅降仓，以防守为主"
    ),
    ThemeCycle.UNKNOWN: CycleParams(
        cycle=ThemeCycle.UNKNOWN,
        position_cap=0.40,
        single_position_max=0.15,
        max_positions=4,
        stop_loss_pct=-0.08,
        take_profit_pct=0.25,
        trailing_stop_pct=-0.07,
        signal_weights={
            "first_limit_up": 0.25,
            "consecutive_limit": 0.25,
            "strong_breakout": 0.25,
            "vol_price_rise": 0.25,
        },
        description="未知: 均衡配置"
    )
}


@dataclass
class CycleJudgeResult:
    """周期判断结果"""
    cycle: ThemeCycle
    confidence: float = 0.0         # 置信度 (0-1)
    days_in_cycle: int = 0          # 已在当前周期的天数
    expected_remaining: int = 0     # 预计剩余天数
    
    # 判断依据
    factors: Dict[str, float] = field(default_factory=dict)
    
    # 周期参数
    params: Optional[CycleParams] = None
    
    # 说明
    reasoning: str = ""
    
    def __post_init__(self):
        if self.params is None:
            self.params = CYCLE_PARAMS_MAP.get(self.cycle, CYCLE_PARAMS_MAP[ThemeCycle.UNKNOWN])


# ============== 主题周期判断器 ==============

class ThemeCycleJudge:
    """
    主题周期判断器
    
    基于以下指标判断主题所处周期:
    1. 主线启动天数
    2. 涨停家数趋势
    3. 龙头涨幅/换手率
    4. 板块分化度
    5. 成交量变化
    """
    
    def __init__(self, jq=None):
        """
        初始化主题周期判断器
        
        Args:
            jq: JQData实例（可选）
        """
        self.jq = jq
        self._ensure_jqdata()
        
        # 周期阈值配置
        self.config = {
            "early_max_days": 3,        # 初期最多3天
            "middle_max_days": 10,      # 中期最多10天（2周）
            "late_max_days": 15,        # 后期最多15天（3周）
            
            "limit_up_growth_threshold": 0.3,  # 涨停家数增长阈值
            "leader_exhausted_drawdown": -0.15, # 龙头回撤触发衰竭
            "divergence_threshold": 0.3,  # 分化度阈值
        }
        
        logger.info("ThemeCycleJudge 初始化完成")
    
    def _ensure_jqdata(self):
        """确保JQData可用"""
        if self.jq is None:
            try:
                import jqdatasdk as jq
                with open("/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json") as f:
                    config = json.load(f)
                jq.auth(config['username'], config['password'])
                self.jq = jq
                logger.info("JQData认证成功")
            except Exception as e:
                logger.warning(f"JQData认证失败: {e}")
    
    def judge_cycle(
        self,
        mainline_name: str,
        mainline_stocks: List[str],
        date: str,
        history_days: int = 20
    ) -> CycleJudgeResult:
        """
        判断主题所处周期
        
        Args:
            mainline_name: 主线名称
            mainline_stocks: 主线成分股
            date: 判断日期
            history_days: 回看天数
        
        Returns:
            CycleJudgeResult: 周期判断结果
        """
        result = CycleJudgeResult(cycle=ThemeCycle.UNKNOWN)
        
        if not mainline_stocks or self.jq is None:
            result.reasoning = "数据不足，无法判断周期"
            return result
        
        try:
            # 1. 获取价格数据
            end_date = pd.to_datetime(date)
            start_date = end_date - timedelta(days=history_days * 2)
            
            price_df = self.jq.get_price(
                mainline_stocks[:50],  # 最多取50只
                start_date=str(start_date.date()),
                end_date=str(end_date.date()),
                frequency='daily',
                fields=['close', 'high', 'low', 'volume', 'pre_close'],
                panel=False,
                skip_paused=True
            )
            
            if price_df is None or price_df.empty:
                result.reasoning = "获取价格数据失败"
                return result
            
            # 2. 计算各项指标
            factors = {}
            
            # 2.1 计算启动天数
            startup_days, startup_date = self._calculate_startup_days(price_df, mainline_stocks)
            factors['startup_days'] = startup_days
            
            # 2.2 计算涨停家数趋势
            limit_up_trend = self._calculate_limit_up_trend(price_df)
            factors['limit_up_trend'] = limit_up_trend
            
            # 2.3 计算龙头状态
            leader_status = self._calculate_leader_status(price_df, mainline_stocks)
            factors['leader_pnl'] = leader_status.get('leader_pnl', 0)
            factors['leader_drawdown'] = leader_status.get('leader_drawdown', 0)
            
            # 2.4 计算板块分化度
            divergence = self._calculate_divergence(price_df)
            factors['divergence'] = divergence
            
            # 2.5 计算成交量变化
            volume_change = self._calculate_volume_change(price_df)
            factors['volume_change'] = volume_change
            
            # 3. 综合判断周期
            cycle, confidence = self._determine_cycle(factors)
            
            # 4. 计算预计剩余天数
            expected_remaining = self._estimate_remaining_days(cycle, startup_days)
            
            # 5. 构建结果
            result = CycleJudgeResult(
                cycle=cycle,
                confidence=confidence,
                days_in_cycle=startup_days,
                expected_remaining=expected_remaining,
                factors=factors,
                params=CYCLE_PARAMS_MAP.get(cycle, CYCLE_PARAMS_MAP[ThemeCycle.UNKNOWN]),
                reasoning=self._generate_reasoning(mainline_name, cycle, factors)
            )
            
            logger.info(f"主题周期判断: {mainline_name} -> {cycle.value} "
                       f"(置信度: {confidence:.0%}, 已持续: {startup_days}天)")
            
        except Exception as e:
            logger.error(f"周期判断失败: {e}")
            result.reasoning = f"判断失败: {e}"
        
        return result
    
    def _calculate_startup_days(
        self,
        price_df: pd.DataFrame,
        stocks: List[str]
    ) -> Tuple[int, Optional[datetime]]:
        """计算主线启动天数"""
        try:
            # 计算板块平均涨幅
            pivot_close = price_df.pivot(index='time', columns='code', values='close')
            sector_returns = pivot_close.pct_change().mean(axis=1)
            
            # 寻找连续上涨的起点
            cumulative = (1 + sector_returns).cumprod()
            
            # 从最高点回溯找起点
            peak_idx = cumulative.idxmax()
            
            # 简化: 从5日前开始计算
            startup_idx = max(0, len(cumulative) - 10)
            startup_date = cumulative.index[startup_idx] if startup_idx < len(cumulative) else None
            
            if startup_date:
                days = (peak_idx - startup_date).days
                return max(1, days), startup_date
            
        except Exception as e:
            logger.warning(f"计算启动天数失败: {e}")
        
        return 5, None  # 默认5天
    
    def _calculate_limit_up_trend(self, price_df: pd.DataFrame) -> float:
        """计算涨停家数趋势"""
        try:
            # 计算涨停
            price_df = price_df.copy()
            price_df['pct_change'] = (price_df['close'] / price_df['pre_close'] - 1) * 100
            price_df['is_limit_up'] = price_df['pct_change'] >= 9.5
            
            # 按日统计涨停家数
            daily_limit_up = price_df.groupby('time')['is_limit_up'].sum()
            
            if len(daily_limit_up) >= 5:
                # 计算5日趋势
                recent = daily_limit_up.iloc[-5:].mean()
                earlier = daily_limit_up.iloc[-10:-5].mean() if len(daily_limit_up) >= 10 else recent
                
                if earlier > 0:
                    return (recent - earlier) / earlier
            
        except Exception as e:
            logger.warning(f"计算涨停趋势失败: {e}")
        
        return 0.0
    
    def _calculate_leader_status(
        self,
        price_df: pd.DataFrame,
        stocks: List[str]
    ) -> Dict[str, float]:
        """计算龙头股状态"""
        result = {'leader_pnl': 0.0, 'leader_drawdown': 0.0, 'leader_stock': ''}
        
        try:
            # 找龙头（期间涨幅最大的股票）
            pivot_close = price_df.pivot(index='time', columns='code', values='close')
            
            total_returns = (pivot_close.iloc[-1] / pivot_close.iloc[0] - 1) * 100
            leader_stock = total_returns.idxmax()
            
            result['leader_stock'] = leader_stock
            result['leader_pnl'] = total_returns[leader_stock]
            
            # 计算龙头从最高点的回撤
            leader_prices = pivot_close[leader_stock]
            peak = leader_prices.max()
            current = leader_prices.iloc[-1]
            
            result['leader_drawdown'] = (current / peak - 1) * 100
            
        except Exception as e:
            logger.warning(f"计算龙头状态失败: {e}")
        
        return result
    
    def _calculate_divergence(self, price_df: pd.DataFrame) -> float:
        """计算板块分化度"""
        try:
            # 计算各股票收益率的标准差
            pivot_close = price_df.pivot(index='time', columns='code', values='close')
            
            # 最近5日收益率
            recent_returns = (pivot_close.iloc[-1] / pivot_close.iloc[-5] - 1) * 100
            
            # 分化度 = 收益率标准差 / 平均收益率
            mean_return = recent_returns.mean()
            std_return = recent_returns.std()
            
            if abs(mean_return) > 0.01:
                return std_return / abs(mean_return)
            
        except Exception as e:
            logger.warning(f"计算分化度失败: {e}")
        
        return 0.5
    
    def _calculate_volume_change(self, price_df: pd.DataFrame) -> float:
        """计算成交量变化"""
        try:
            # 按日汇总成交量
            daily_volume = price_df.groupby('time')['volume'].sum()
            
            if len(daily_volume) >= 10:
                recent = daily_volume.iloc[-5:].mean()
                earlier = daily_volume.iloc[-10:-5].mean()
                
                if earlier > 0:
                    return (recent - earlier) / earlier
            
        except Exception as e:
            logger.warning(f"计算成交量变化失败: {e}")
        
        return 0.0
    
    def _determine_cycle(self, factors: Dict[str, float]) -> Tuple[ThemeCycle, float]:
        """综合判断周期"""
        startup_days = factors.get('startup_days', 5)
        limit_up_trend = factors.get('limit_up_trend', 0)
        leader_drawdown = factors.get('leader_drawdown', 0)
        divergence = factors.get('divergence', 0.5)
        volume_change = factors.get('volume_change', 0)
        
        # 衰竭判断（优先级最高）
        if leader_drawdown < self.config['leader_exhausted_drawdown']:
            return ThemeCycle.EXHAUSTED, 0.8
        
        # 根据启动天数初步判断
        if startup_days <= self.config['early_max_days']:
            base_cycle = ThemeCycle.EARLY
            confidence = 0.7
        elif startup_days <= self.config['middle_max_days']:
            base_cycle = ThemeCycle.MIDDLE
            confidence = 0.7
        elif startup_days <= self.config['late_max_days']:
            base_cycle = ThemeCycle.LATE
            confidence = 0.7
        else:
            base_cycle = ThemeCycle.EXHAUSTED
            confidence = 0.6
        
        # 根据其他指标调整
        # 涨停趋势增加说明还在加速
        if limit_up_trend > self.config['limit_up_growth_threshold']:
            if base_cycle == ThemeCycle.LATE:
                base_cycle = ThemeCycle.MIDDLE
                confidence += 0.1
        
        # 分化度高说明进入后期
        if divergence > self.config['divergence_threshold']:
            if base_cycle == ThemeCycle.MIDDLE:
                base_cycle = ThemeCycle.LATE
                confidence += 0.1
        
        # 成交量萎缩可能衰竭
        if volume_change < -0.3:
            if base_cycle == ThemeCycle.LATE:
                base_cycle = ThemeCycle.EXHAUSTED
                confidence += 0.1
        
        return base_cycle, min(confidence, 0.95)
    
    def _estimate_remaining_days(self, cycle: ThemeCycle, current_days: int) -> int:
        """估计剩余天数"""
        max_days = {
            ThemeCycle.EARLY: self.config['early_max_days'],
            ThemeCycle.MIDDLE: self.config['middle_max_days'],
            ThemeCycle.LATE: self.config['late_max_days'],
            ThemeCycle.EXHAUSTED: 0,
            ThemeCycle.UNKNOWN: 5,
        }
        
        remaining = max_days.get(cycle, 5) - current_days
        return max(0, remaining)
    
    def _generate_reasoning(
        self,
        mainline_name: str,
        cycle: ThemeCycle,
        factors: Dict[str, float]
    ) -> str:
        """生成判断理由"""
        parts = [f"主线[{mainline_name}]判断为{cycle.value}周期"]
        
        parts.append(f"已启动{factors.get('startup_days', 0)}天")
        
        limit_trend = factors.get('limit_up_trend', 0)
        if limit_trend > 0.3:
            parts.append("涨停家数持续增加")
        elif limit_trend < -0.3:
            parts.append("涨停家数明显减少")
        
        divergence = factors.get('divergence', 0)
        if divergence > 0.5:
            parts.append("板块分化加剧")
        
        leader_dd = factors.get('leader_drawdown', 0)
        if leader_dd < -10:
            parts.append(f"龙头回撤{leader_dd:.1f}%")
        
        return "，".join(parts)
    
    def get_cycle_params(self, cycle: ThemeCycle) -> CycleParams:
        """获取周期参数"""
        return CYCLE_PARAMS_MAP.get(cycle, CYCLE_PARAMS_MAP[ThemeCycle.UNKNOWN])
    
    def batch_judge(
        self,
        mainlines: List[Dict[str, Any]],
        date: str
    ) -> List[CycleJudgeResult]:
        """批量判断多个主线的周期"""
        results = []
        
        for ml in mainlines:
            name = ml.get('name', '')
            stocks = ml.get('stocks', [])
            
            result = self.judge_cycle(name, stocks, date)
            results.append(result)
        
        return results


# ============== 测试函数 ==============

def test_theme_cycle_judge():
    """测试主题周期判断器"""
    print("="*60)
    print("主题周期判断器测试")
    print("="*60)
    
    judge = ThemeCycleJudge()
    
    # 测试用例
    test_cases = [
        {
            "mainline": "人工智能",
            "stocks": ["002415.XSHE", "300369.XSHE", "300674.XSHE", "300468.XSHE"],
            "date": "2024-09-30"
        },
        {
            "mainline": "新能源汽车",
            "stocks": ["300750.XSHE", "002594.XSHE", "300014.XSHE"],
            "date": "2024-10-10"
        }
    ]
    
    for tc in test_cases:
        print(f"\n测试主线: {tc['mainline']}")
        result = judge.judge_cycle(
            mainline_name=tc['mainline'],
            mainline_stocks=tc['stocks'],
            date=tc['date']
        )
        
        print(f"  周期: {result.cycle.value}")
        print(f"  置信度: {result.confidence:.0%}")
        print(f"  已持续: {result.days_in_cycle}天")
        print(f"  预计剩余: {result.expected_remaining}天")
        print(f"  理由: {result.reasoning}")
        print(f"  参数: 仓位上限={result.params.position_cap:.0%}, "
              f"止损={result.params.stop_loss_pct:.0%}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_theme_cycle_judge()
