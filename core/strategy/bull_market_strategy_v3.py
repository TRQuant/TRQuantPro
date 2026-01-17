# -*- coding: utf-8 -*-
"""
牛市极端高收益策略 V3.0 - 核心策略模块
========================================

目标：周频10%收益

核心特性：
1. 全A股覆盖（~5000只，排除科创/北交/ST/次新）
2. 多周期共振+HMM市场分析作为系统开关
3. 涨停+动量+资金流向多因子选股
4. 完整止损止盈系统

设计理念：
- 牛市专用策略，非牛市时自动降低仓位
- 追涨模式为主，重点捕捉涨停+突破信号
- 分批止盈锁定利润，移动止损保护盈利

作者: TRQuant Team
日期: 2026-01-12
"""

from __future__ import annotations

import os
import logging
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class SignalType(Enum):
    """信号类型"""
    FIRST_LIMIT_UP = "首板启动"      # 首次涨停
    CONSECUTIVE_LIMIT = "连板加速"   # 连续涨停
    BREAKOUT_60D = "突破60日新高"    # 突破信号
    STRONG_MOMENTUM = "强势动量"     # 动量信号
    VOLUME_SURGE = "放量启动"        # 量能信号


@dataclass
class BullMarketStrategyConfig:
    """
    牛市策略配置（V3.0优化版）
    
    基于2024政策牛市最优参数，同时兼顾其他牛市时段
    """
    # ============ 选股因子阈值 ============
    # 动量因子
    min_mom_20d: float = -1.25    # 最小20日动量（允许轻微负值）
    max_mom_20d: float = 25.0     # 最大20日动量（防止追高）
    min_mom_5d: float = 5.0       # 最小5日动量（短期趋势）
    
    # 位置因子
    max_rel_position: float = 80.0  # 最大相对位置（防止追高）
    
    # 量比因子
    min_vol_ratio: float = 1.0        # 最小量比（要求放量）
    vol_ratio_threshold_first: float = 2.5  # 首板放量阈值
    vol_ratio_threshold_breakout: float = 1.5  # 突破放量阈值
    
    # 涨停因子
    limit_up_threshold: float = 0.093  # 涨停阈值（9.3%）
    min_limit_up_score: float = 60.0   # 最小涨停评分
    
    # 突破因子
    breakout_ratio_min: float = 5.0  # 最小突破幅度
    mom_5d_threshold_breakout: float = 16.0  # 突破后的5日动量阈值
    
    # 资金流向
    min_flow_strength: float = 0.0  # 最小资金流向强度
    
    # ============ 信号评分 ============
    min_signal_score: float = 55.0  # 最小综合评分
    
    # ============ 仓位管理 ============
    max_positions: int = 3           # 最大持仓数（集中持股）
    single_position_max: float = 0.4  # 单只最大权重（40%）
    rebalance_period: int = 5        # 调仓周期（周频）
    
    # ============ 风险控制 ============
    # 固定止损止盈
    stop_loss_pct: float = -0.08     # 固定止损（-8%）
    take_profit_pct: float = 0.40    # 固定止盈（+40%）
    
    # 分批止盈
    partial_profit_1_pct: float = 0.20   # 第一批止盈（+20%）
    partial_profit_1_ratio: float = 0.50  # 第一批止盈比例（50%）
    
    # 移动止损
    trailing_stop_trigger: float = 0.15  # 移动止损触发（+15%）
    trailing_stop_pct: float = -0.08    # 移动止损回撤（-8%）
    
    # 时间止损
    time_stop_days: int = 20  # 最大持仓天数
    
    # ============ 市场环境 ============
    use_market_regime: bool = True    # 是否使用市场状态过滤
    min_market_score: float = 55.0    # 最小市场评分
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "BullMarketStrategyConfig":
        """从字典创建"""
        return cls(**d)


@dataclass
class StockSignal:
    """股票信号"""
    code: str                      # 股票代码
    signal_type: SignalType        # 信号类型
    score: float                   # 综合评分（0-100）
    factors: Dict[str, float]      # 因子值
    weight: float = 0.0            # 目标权重
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "signal_type": self.signal_type.value,
            "score": self.score,
            "factors": self.factors,
            "weight": self.weight,
        }


class BullMarketStrategyV3:
    """
    牛市极端高收益策略 V3.0
    
    特点：
    1. 专注牛市环境，使用多周期共振+HMM判断市场状态
    2. 多因子选股：涨停、动量、资金流向
    3. 集中持仓（3-5只），追求高收益
    4. 完整风控系统
    """
    
    VERSION = "3.0"
    
    def __init__(self, config: Optional[BullMarketStrategyConfig] = None):
        """
        初始化策略
        
        Args:
            config: 策略配置，默认使用优化参数
        """
        self.config = config or BullMarketStrategyConfig()
        self._market_analyzer = None
        
        logger.info(f"BullMarketStrategyV3 初始化: version={self.VERSION}")
    
    def _ensure_market_analyzer(self):
        """确保市场分析器初始化"""
        if self._market_analyzer is None:
            try:
                from core.market_trend_analyzer import (
                    MarketTrendAnalyzer,
                    MarketTrendAnalyzerConfig,
                )
                market_config = MarketTrendAnalyzerConfig(
                    scoring_style="smooth_grouped",
                    active_periods=["week", "month", "quarter"],
                )
                self._market_analyzer = MarketTrendAnalyzer(market_config)
                logger.info("市场分析器初始化成功")
            except Exception as e:
                logger.warning(f"市场分析器初始化失败: {e}")
                self._market_analyzer = None
    
    def check_market_regime(
        self,
        as_of_date: str,
        index_code: str = "000300.XSHG",
    ) -> Tuple[bool, float, str]:
        """
        检查市场状态
        
        Args:
            as_of_date: 检查日期
            index_code: 指数代码
        
        Returns:
            Tuple: (is_bull, score, regime_desc)
        """
        if not self.config.use_market_regime:
            return True, 70.0, "未启用市场状态检测"
        
        self._ensure_market_analyzer()
        
        if self._market_analyzer is None:
            return True, 60.0, "分析器不可用"
        
        try:
            signal = self._market_analyzer.analyze(index_code, as_of_date)
            if signal is None:
                return True, 60.0, "分析结果为空"
            
            signal_dict = signal.to_dict()
            score = signal_dict.get("composite_score", 50)
            direction = signal_dict.get("trend_direction", "震荡盘整")
            
            is_bull = (
                score >= self.config.min_market_score and
                direction in ["强势上涨", "上涨趋势", "弱势上涨"]
            )
            
            regime_desc = f"{signal_dict.get('regime', '震荡')} ({direction})"
            
            return is_bull, score, regime_desc
            
        except Exception as e:
            logger.warning(f"市场状态检测异常: {e}")
            return True, 60.0, f"检测异常: {e}"
    
    def calculate_stock_signals(
        self,
        close: pd.DataFrame,
        high: pd.DataFrame,
        low: pd.DataFrame,
        volume: pd.DataFrame,
        is_tradeable: Optional[pd.DataFrame] = None,
        as_of_date: Optional[str] = None,
    ) -> List[StockSignal]:
        """
        计算股票信号
        
        Args:
            close: 收盘价矩阵 (T x N)
            high: 最高价矩阵
            low: 最低价矩阵
            volume: 成交量矩阵
            is_tradeable: 可交易掩码
            as_of_date: 当前日期
        
        Returns:
            股票信号列表（按评分排序）
        """
        signals = []
        
        for stock in close.columns:
            try:
                signal = self._calculate_single_signal(
                    stock=stock,
                    close=close[stock],
                    high=high[stock],
                    low=low[stock],
                    volume=volume[stock],
                    is_tradeable=is_tradeable[stock] if is_tradeable is not None else None,
                )
                
                if signal is not None and signal.score >= self.config.min_signal_score:
                    signals.append(signal)
                    
            except Exception as e:
                logger.debug(f"计算信号失败 {stock}: {e}")
                continue
        
        # 按评分排序
        signals.sort(key=lambda x: x.score, reverse=True)
        
        return signals
    
    def _calculate_single_signal(
        self,
        stock: str,
        close: pd.Series,
        high: pd.Series,
        low: pd.Series,
        volume: pd.Series,
        is_tradeable: Optional[pd.Series] = None,
    ) -> Optional[StockSignal]:
        """
        计算单只股票信号
        
        Returns:
            StockSignal or None
        """
        if len(close) < 60:  # 数据不足
            return None
        
        # 检查可交易性
        if is_tradeable is not None and not is_tradeable.iloc[-1]:
            return None
        
        close_arr = close.values
        high_arr = high.values
        low_arr = low.values
        volume_arr = volume.values
        
        # ============ 计算因子 ============
        factors = {}
        
        # 1. 动量因子
        if len(close_arr) >= 21:
            mom_20d = (close_arr[-1] / close_arr[-21] - 1) * 100
            factors["mom_20d"] = mom_20d
        else:
            factors["mom_20d"] = 0
        
        if len(close_arr) >= 6:
            mom_5d = (close_arr[-1] / close_arr[-6] - 1) * 100
            factors["mom_5d"] = mom_5d
        else:
            factors["mom_5d"] = 0
        
        # 2. 相对位置
        if len(close_arr) >= 20:
            high_20d = np.max(high_arr[-20:])
            low_20d = np.min(low_arr[-20:])
            if high_20d > low_20d:
                rel_pos = (close_arr[-1] - low_20d) / (high_20d - low_20d) * 100
            else:
                rel_pos = 50
            factors["rel_position"] = rel_pos
        else:
            factors["rel_position"] = 50
        
        # 3. 量比
        if len(volume_arr) >= 20:
            vol_ma20 = np.mean(volume_arr[-20:])
            vol_ratio = volume_arr[-1] / (vol_ma20 + 1e-8)
            factors["vol_ratio"] = vol_ratio
        else:
            factors["vol_ratio"] = 1.0
        
        # 4. 涨停检测
        if len(close_arr) >= 2:
            daily_return = close_arr[-1] / close_arr[-2] - 1
            is_limit_up = daily_return >= self.config.limit_up_threshold
            factors["is_limit_up"] = 1 if is_limit_up else 0
            factors["daily_return"] = daily_return * 100
        else:
            factors["is_limit_up"] = 0
            factors["daily_return"] = 0
        
        # 近5日涨停次数
        limit_up_count = 0
        for i in range(min(5, len(close_arr) - 1)):
            idx = -(i + 1)
            if close_arr[idx] / close_arr[idx - 1] - 1 >= self.config.limit_up_threshold:
                limit_up_count += 1
        factors["limit_up_count_5d"] = limit_up_count
        
        # 5. 突破因子
        if len(close_arr) >= 60:
            high_60d = np.max(high_arr[-60:-1])  # 不含今日
            breakout = close_arr[-1] > high_60d
            breakout_ratio = (close_arr[-1] / high_60d - 1) * 100 if high_60d > 0 else 0
            factors["breakout_60d"] = 1 if breakout else 0
            factors["breakout_ratio"] = breakout_ratio
        else:
            factors["breakout_60d"] = 0
            factors["breakout_ratio"] = 0
        
        # 6. 资金流向估算
        if len(close_arr) >= 5:
            price_pos = (close_arr[-1] - low_arr[-1]) / (high_arr[-1] - low_arr[-1] + 1e-8)
            flow_strength = (price_pos - 0.5) * volume_arr[-1]
            # 标准化
            vol_mean = np.mean(volume_arr[-20:]) if len(volume_arr) >= 20 else volume_arr[-1]
            factors["flow_strength"] = flow_strength / (vol_mean + 1e-8)
        else:
            factors["flow_strength"] = 0
        
        # ============ 筛选条件 ============
        # 动量条件
        if not (self.config.min_mom_20d <= factors["mom_20d"] <= self.config.max_mom_20d):
            return None
        
        # 位置条件
        if factors["rel_position"] > self.config.max_rel_position:
            return None
        
        # 量比条件
        if factors["vol_ratio"] < self.config.min_vol_ratio:
            return None
        
        # ============ 信号类型判断 ============
        signal_type = None
        score = 0.0
        
        # 信号1: 首板启动
        if factors["is_limit_up"] and limit_up_count == 1:
            if factors["vol_ratio"] >= self.config.vol_ratio_threshold_first:
                signal_type = SignalType.FIRST_LIMIT_UP
                score = 85
            else:
                score = 70
        
        # 信号2: 连板加速
        elif limit_up_count >= 2:
            signal_type = SignalType.CONSECUTIVE_LIMIT
            score = 75 + min(limit_up_count * 5, 20)  # 最高95
        
        # 信号3: 突破60日新高
        elif factors["breakout_60d"] and factors["breakout_ratio"] >= self.config.breakout_ratio_min:
            if factors["mom_5d"] >= self.config.mom_5d_threshold_breakout:
                signal_type = SignalType.BREAKOUT_60D
                score = 80
            else:
                score = 65
        
        # 信号4: 强势动量
        elif factors["mom_5d"] >= 10 and factors["vol_ratio"] >= 1.5:
            signal_type = SignalType.STRONG_MOMENTUM
            score = 60 + min(factors["mom_5d"], 20)
        
        # 信号5: 放量启动
        elif factors["vol_ratio"] >= 3.0 and factors["mom_5d"] >= 5:
            signal_type = SignalType.VOLUME_SURGE
            score = 55 + min(factors["vol_ratio"] * 5, 30)
        
        else:
            return None  # 不符合任何信号
        
        # 资金流向加分
        if factors["flow_strength"] >= self.config.min_flow_strength:
            score += min(factors["flow_strength"] * 5, 10)
        
        # 限制评分范围
        score = max(0, min(100, score))
        
        if signal_type is None:
            signal_type = SignalType.STRONG_MOMENTUM
        
        return StockSignal(
            code=stock,
            signal_type=signal_type,
            score=score,
            factors=factors,
        )
    
    def select_top_stocks(
        self,
        signals: List[StockSignal],
        available_cash: float = 1000000.0,
    ) -> List[StockSignal]:
        """
        选择持仓股票并分配权重
        
        Args:
            signals: 股票信号列表（已排序）
            available_cash: 可用资金
        
        Returns:
            选中的股票信号（带权重）
        """
        if not signals:
            return []
        
        # 取前N只
        selected = signals[:self.config.max_positions]
        
        # 分配权重（按评分加权）
        total_score = sum(s.score for s in selected)
        
        for signal in selected:
            if total_score > 0:
                weight = signal.score / total_score
            else:
                weight = 1.0 / len(selected)
            
            # 限制单只权重
            weight = min(weight, self.config.single_position_max)
            signal.weight = weight
        
        # 归一化权重
        total_weight = sum(s.weight for s in selected)
        if total_weight > 0 and total_weight != 1.0:
            for signal in selected:
                signal.weight = signal.weight / total_weight
        
        return selected
    
    def generate_strategy_report(self) -> str:
        """
        生成策略说明报告
        
        Returns:
            Markdown格式的策略报告
        """
        report = f"""
# 牛市极端高收益策略 V{self.VERSION}

## 策略概述

本策略专注于牛市环境，通过多因子选股和严格风控追求周频10%的收益目标。

## 核心参数

### 选股参数
| 参数 | 值 | 说明 |
|------|-----|------|
| min_mom_20d | {self.config.min_mom_20d}% | 最小20日动量 |
| max_mom_20d | {self.config.max_mom_20d}% | 最大20日动量 |
| max_rel_position | {self.config.max_rel_position}% | 最大相对位置 |
| min_vol_ratio | {self.config.min_vol_ratio} | 最小量比 |
| limit_up_threshold | {self.config.limit_up_threshold*100:.1f}% | 涨停阈值 |
| min_signal_score | {self.config.min_signal_score} | 最小信号评分 |

### 仓位管理
| 参数 | 值 | 说明 |
|------|-----|------|
| max_positions | {self.config.max_positions} | 最大持仓数 |
| single_position_max | {self.config.single_position_max*100:.0f}% | 单只最大权重 |
| rebalance_period | {self.config.rebalance_period}天 | 调仓周期 |

### 风险控制
| 参数 | 值 | 说明 |
|------|-----|------|
| stop_loss_pct | {self.config.stop_loss_pct*100:.0f}% | 固定止损 |
| take_profit_pct | {self.config.take_profit_pct*100:.0f}% | 固定止盈 |
| partial_profit_1_pct | +{self.config.partial_profit_1_pct*100:.0f}% | 第一批止盈触发 |
| partial_profit_1_ratio | {self.config.partial_profit_1_ratio*100:.0f}% | 第一批止盈比例 |
| trailing_stop_trigger | +{self.config.trailing_stop_trigger*100:.0f}% | 移动止损触发 |
| trailing_stop_pct | {self.config.trailing_stop_pct*100:.0f}% | 移动止损回撤 |
| time_stop_days | {self.config.time_stop_days}天 | 时间止损 |

## 信号类型

1. **首板启动**: 首次涨停+放量，评分85+
2. **连板加速**: 连续涨停，评分75-95
3. **突破60日新高**: 突破+动量确认，评分80
4. **强势动量**: 5日动量>10%+放量，评分60-80
5. **放量启动**: 量比>3+动量>5%，评分55-85

## 使用建议

1. **牛市环境**: 仅在多周期共振确认牛市时使用
2. **仓位控制**: 严格遵守最大持仓限制
3. **止损纪律**: 严格执行止损，不补仓
4. **轮动操作**: 每周调仓，及时切换标的
"""
        return report


# 便捷函数
def create_bull_market_strategy(
    config_dict: Optional[Dict[str, Any]] = None
) -> BullMarketStrategyV3:
    """
    创建牛市策略实例
    
    Args:
        config_dict: 配置字典（可选）
    
    Returns:
        BullMarketStrategyV3实例
    """
    if config_dict:
        config = BullMarketStrategyConfig.from_dict(config_dict)
    else:
        config = BullMarketStrategyConfig()
    
    return BullMarketStrategyV3(config)
