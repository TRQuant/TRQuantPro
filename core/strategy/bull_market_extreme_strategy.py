# -*- coding: utf-8 -*-
"""
牛市极端高收益策略模块

================================================================================
策略概述
================================================================================
本策略基于历史牛市（2014-2015杠杆牛、2019-2021结构牛）的高回报案例挖掘，
采用自适应机制在不同市场状态下切换策略：

1. 牛市状态：追涨策略 - 涨停板启动、连板加速、强势突破
2. 震荡市状态：低位布局 - 相对位置<50%、超卖反弹、放量底部

================================================================================
核心信号
================================================================================
- 首板启动：首次涨停+放量>3倍+突破60日高 → 评分75
- 连板加速：2连板或以上 → 评分60
- 强势突破：突破60日高>5%+5日动量>15%+量比>1.5 → 评分60
- 量价齐升：5日动量>20%+量比>1.5+成交额爆发>2倍 → 评分55

================================================================================
风控机制
================================================================================
- 止损：-10%（绝对执行）
- 止盈：+25%（分批）
- 最大持仓：2只股票
- 空仓等待：无强信号时持现金

作者: TRQuant Team
日期: 2026-01-10
版本: 1.0
================================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
import pandas as pd
import logging

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

logger = logging.getLogger(__name__)


# =============================================================================
# 数据类定义
# =============================================================================

class MarketState(Enum):
    """
    市场状态枚举
    
    市场状态决定了策略的选股逻辑和仓位管理方式：
    - BULL: 牛市 → 追涨策略，高仓位（70-90%）
    - NEUTRAL: 震荡市 → 低位布局，中等仓位（40-60%）
    - BEAR: 熊市 → 防守策略，低仓位（10-30%）
    """
    BULL = "bull"           # 牛市：追涨策略
    NEUTRAL = "neutral"     # 震荡市：低位布局
    BEAR = "bear"           # 熊市：防守策略


class SignalType(Enum):
    """
    信号类型枚举
    
    定义不同的买入信号类型，用于策略执行和报告生成
    """
    FIRST_LIMIT_UP = "首板启动"      # 首次涨停板信号
    CONSECUTIVE_LIMIT_UP = "连板加速"  # 连续涨停信号
    STRONG_BREAKOUT = "强势突破"      # 突破新高信号
    VOLUME_PRICE_RISE = "量价齐升"    # 量价配合信号
    LOW_POSITION_REBOUND = "低位反弹"  # 超卖反弹信号
    NO_SIGNAL = "无信号"              # 无有效信号


@dataclass
class StrategyConfig:
    """
    策略配置参数
    
    包含所有可调节的策略参数，用于回测优化和实盘调整
    
    Attributes:
        signal_threshold: 信号阈值，评分超过此值才会触发买入
        max_positions: 最大持仓股票数量
        stop_loss_pct: 止损比例（负数）
        take_profit_pct: 止盈比例
        position_size_pct: 单只股票最大仓位比例
        rebalance_days: 调仓周期（交易日）
        warmup_days: 预热期天数
        universe_size: 股票池大小限制
        enable_market_state_detection: 是否启用市场状态检测
    """
    # 信号参数
    signal_threshold: float = 60.0        # 信号评分阈值
    max_positions: int = 2                # 最大持仓数量
    
    # 风控参数
    stop_loss_pct: float = -10.0          # 止损比例 (%)
    take_profit_pct: float = 25.0         # 止盈比例 (%)
    
    # 仓位参数
    position_size_pct: float = 50.0       # 单只股票最大仓位 (%)
    
    # 调仓参数
    rebalance_days: int = 5               # 周频调仓
    warmup_days: int = 60                 # 预热期60天
    
    # 股票池参数
    universe_size: int = 500              # 股票池大小
    
    # 功能开关
    enable_market_state_detection: bool = True  # 启用市场状态检测
    
    # 牛市信号参数
    limit_up_threshold: float = 9.5       # 涨停判定阈值 (%)
    volume_explosion_threshold: float = 3.0  # 量比爆发阈值
    momentum_5d_threshold: float = 10.0   # 5日动量阈值
    breakout_threshold: float = 5.0       # 突破幅度阈值 (%)
    
    # 震荡市信号参数
    rel_position_low: float = 50.0        # 相对位置低位阈值
    rsi_oversold: float = 30.0            # RSI超卖阈值


@dataclass
class Signal:
    """
    交易信号
    
    封装一个交易信号的完整信息
    
    Attributes:
        code: 股票代码
        name: 股票名称
        signal_type: 信号类型
        score: 评分（0-100）
        factors: 相关因子字典
        date: 信号日期
        price: 当前价格
        reason: 信号说明
    """
    code: str                             # 股票代码
    name: str = ""                        # 股票名称
    signal_type: SignalType = SignalType.NO_SIGNAL  # 信号类型
    score: float = 0.0                    # 评分
    factors: Dict[str, float] = field(default_factory=dict)  # 因子值
    date: str = ""                        # 信号日期
    price: float = 0.0                    # 当前价格
    reason: str = ""                      # 信号说明


@dataclass 
class Position:
    """
    持仓信息
    
    Attributes:
        code: 股票代码
        shares: 持股数量
        cost: 成本价
        entry_date: 买入日期
        max_price: 持仓期间最高价（用于移动止盈）
    """
    code: str
    shares: int
    cost: float
    entry_date: str
    max_price: float = 0.0
    
    def __post_init__(self):
        if self.max_price == 0.0:
            self.max_price = self.cost


@dataclass
class Order:
    """
    交易订单
    
    Attributes:
        code: 股票代码
        direction: 方向 (BUY/SELL)
        shares: 数量
        price: 价格
        reason: 原因
    """
    code: str
    direction: str  # BUY / SELL
    shares: int
    price: float
    reason: str = ""


# =============================================================================
# 核心策略类
# =============================================================================

class BullMarketExtremeStrategy:
    """
    牛市极端高收益策略
    
    这是策略的核心类，负责：
    1. 市场状态检测
    2. 因子计算
    3. 信号评分
    4. 交易信号生成
    5. 风险控制
    
    使用示例：
    ```python
    config = StrategyConfig(
        signal_threshold=60,
        max_positions=2,
        stop_loss_pct=-10.0
    )
    strategy = BullMarketExtremeStrategy(config)
    
    # 检测市场状态
    market_state = strategy.detect_market_state(index_data, date)
    
    # 生成信号
    signals = strategy.generate_signals(price_data, universe, date)
    
    # 执行风控
    orders = strategy.apply_risk_control(positions, current_prices)
    ```
    """
    
    def __init__(self, config: Optional[StrategyConfig] = None):
        """
        初始化策略
        
        Args:
            config: 策略配置，如果为None则使用默认配置
        """
        self.config = config or StrategyConfig()
        self._current_market_state = MarketState.NEUTRAL
        self._market_state_history: List[Tuple[str, MarketState]] = []
        
        logger.info(f"策略初始化完成: {self.__class__.__name__}")
        logger.info(f"信号阈值: {self.config.signal_threshold}")
        logger.info(f"最大持仓: {self.config.max_positions}")
        logger.info(f"止损/止盈: {self.config.stop_loss_pct}%/{self.config.take_profit_pct}%")
    
    # =========================================================================
    # 市场状态检测
    # =========================================================================
    
    def detect_market_state(
        self, 
        index_data: pd.DataFrame,
        date: str
    ) -> MarketState:
        """
        检测市场状态
        
        通过分析指数（沪深300）的多周期趋势来判断市场状态。
        
        判断逻辑：
        1. 短期动量（20日）> 10% → 牛市信号
        2. 中期动量（60日）> 20% → 牛市信号
        3. 价格 > MA20 > MA60 → 牛市信号
        4. 综合评分 > 0.5 → 牛市，< -0.5 → 熊市，否则震荡
        
        Args:
            index_data: 指数价格数据，需包含 date/close 列
            date: 当前日期
            
        Returns:
            MarketState: 市场状态
        """
        if not self.config.enable_market_state_detection:
            return MarketState.NEUTRAL
        
        if index_data is None or index_data.empty:
            return MarketState.NEUTRAL
        
        try:
            # 确保数据格式正确
            df = index_data.copy()
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df[df['date'] <= pd.to_datetime(date)]
            
            if len(df) < 60:
                return MarketState.NEUTRAL
            
            close = df['close'].values
            
            # 计算动量指标
            mom_20d = (close[-1] / close[-20] - 1) * 100 if len(close) >= 20 else 0
            mom_60d = (close[-1] / close[-60] - 1) * 100 if len(close) >= 60 else 0
            
            # 计算均线
            ma_20 = np.mean(close[-20:]) if len(close) >= 20 else close[-1]
            ma_60 = np.mean(close[-60:]) if len(close) >= 60 else close[-1]
            
            # 综合评分
            bull_score = 0.0
            bear_score = 0.0
            
            # 短期动量权重0.3
            if mom_20d > 10:
                bull_score += 0.3
            elif mom_20d < -10:
                bear_score += 0.3
            
            # 中期动量权重0.4
            if mom_60d > 20:
                bull_score += 0.4
            elif mom_60d < -20:
                bear_score += 0.4
            
            # 均线关系权重0.3
            if close[-1] > ma_20 > ma_60:
                bull_score += 0.3
            elif close[-1] < ma_20 < ma_60:
                bear_score += 0.3
            
            # 判断市场状态
            if bull_score > 0.5:
                state = MarketState.BULL
            elif bear_score > 0.5:
                state = MarketState.BEAR
            else:
                state = MarketState.NEUTRAL
            
            # 记录状态变化
            self._current_market_state = state
            self._market_state_history.append((date, state))
            
            logger.debug(f"市场状态检测 [{date}]: {state.value} "
                        f"(bull={bull_score:.2f}, bear={bear_score:.2f})")
            
            return state
            
        except Exception as e:
            logger.error(f"市场状态检测失败: {e}")
            return MarketState.NEUTRAL
    
    # =========================================================================
    # 因子计算
    # =========================================================================
    
    def calculate_extreme_factors(
        self,
        price_data: pd.DataFrame,
        code: str,
        date: str
    ) -> Dict[str, Any]:
        """
        计算极端信号因子
        
        计算用于识别高收益机会的技术因子，包括：
        
        涨停相关因子：
        - limit_up_count: 近5日涨停次数
        - limit_up_recent: 最近2日涨停次数
        - is_first_limit_up: 是否首板（近30日首次涨停）
        
        动量因子：
        - mom_1d/3d/5d/10d/20d: 各周期动量
        - mom_acceleration: 动量加速度
        
        量价因子：
        - volume_ratio_1d/5d: 量比
        - money_explosion: 成交额爆发
        - money_change: 成交额变化率
        
        技术位置因子：
        - rel_position_20d/60d: 相对位置
        - breakout_60d: 是否突破60日高点
        - breakout_ratio: 突破幅度
        
        连续特征：
        - consecutive_up_days: 连续上涨天数
        - consecutive_vol_up_days: 连续放量天数
        
        Args:
            price_data: 价格数据（需包含code/date/open/close/high/low/volume/money）
            code: 股票代码
            date: 计算日期
            
        Returns:
            Dict: 因子字典
        """
        result: Dict[str, Any] = {'code': code, 'date': date}
        
        try:
            # 筛选股票数据
            stock_data = price_data[price_data['code'] == code].copy()
            
            if 'date' in stock_data.columns:
                stock_data['date'] = pd.to_datetime(stock_data['date'])
                stock_data = stock_data.sort_values('date')
            
            target_dt = pd.to_datetime(date)
            historical = stock_data[stock_data['date'] <= target_dt].tail(65)
            
            if len(historical) < 25:
                return result
            
            # 提取数据数组
            close = historical['close'].values
            high = historical['high'].values
            low = historical['low'].values
            volume = historical['volume'].values
            money = historical['money'].values if 'money' in historical.columns else volume * close
            
            result['close'] = close[-1]
            
            # -----------------------------------------------------------------
            # 涨停特征计算
            # -----------------------------------------------------------------
            limit_up_threshold = self.config.limit_up_threshold / 100
            
            # 近5日涨停计数
            limit_up_count = 0
            limit_up_recent = 0
            for j in range(max(len(close)-5, 1), len(close)):
                if close[j] / close[j-1] - 1 > limit_up_threshold:
                    limit_up_count += 1
                    if j >= len(close) - 2:
                        limit_up_recent += 1
            
            result['limit_up_count'] = limit_up_count
            result['limit_up_recent'] = limit_up_recent
            
            # 首板识别
            is_first_limit_up = False
            if len(close) >= 30:
                # 检查最近1天是否涨停
                if close[-1] / close[-2] - 1 > limit_up_threshold:
                    # 检查前29天是否没有涨停
                    prev_limit_ups = sum(
                        1 for j in range(len(close)-30, len(close)-1)
                        if j > 0 and close[j] / close[j-1] - 1 > limit_up_threshold
                    )
                    if prev_limit_ups == 0:
                        is_first_limit_up = True
            
            result['is_first_limit_up'] = is_first_limit_up
            
            # -----------------------------------------------------------------
            # 动量因子计算
            # -----------------------------------------------------------------
            if len(close) >= 2:
                result['mom_1d'] = (close[-1] / close[-2] - 1) * 100
            if len(close) >= 4:
                result['mom_3d'] = (close[-1] / close[-4] - 1) * 100
            if len(close) >= 6:
                result['mom_5d'] = (close[-1] / close[-6] - 1) * 100
            if len(close) >= 11:
                result['mom_10d'] = (close[-1] / close[-11] - 1) * 100
            if len(close) >= 21:
                result['mom_20d'] = (close[-1] / close[-21] - 1) * 100
            
            # 动量加速度
            if len(close) >= 11:
                mom_5d_now = (close[-1] / close[-6] - 1) * 100
                mom_5d_prev = (close[-6] / close[-11] - 1) * 100
                result['mom_acceleration'] = mom_5d_now - mom_5d_prev
            
            # -----------------------------------------------------------------
            # 量价因子计算
            # -----------------------------------------------------------------
            if len(volume) >= 20:
                vol_1d = volume[-1]
                vol_5d = np.mean(volume[-5:])
                vol_20d = np.mean(volume[-20:])
                result['volume_ratio_1d'] = vol_1d / vol_20d if vol_20d > 0 else 1
                result['volume_ratio_5d'] = vol_5d / vol_20d if vol_20d > 0 else 1
            
            if len(money) >= 20:
                money_1d = money[-1]
                money_5d = np.sum(money[-5:])
                money_5d_prev = np.sum(money[-10:-5])
                money_20d_avg = np.mean(money[-20:])
                
                result['money_explosion'] = money_1d / money_20d_avg if money_20d_avg > 0 else 1
                result['money_change'] = (money_5d / money_5d_prev - 1) * 100 if money_5d_prev > 0 else 0
            
            # -----------------------------------------------------------------
            # 技术位置因子
            # -----------------------------------------------------------------
            # 20日相对位置
            if len(high) >= 20:
                high_20 = np.max(high[-20:])
                low_20 = np.min(low[-20:])
                if high_20 > low_20:
                    result['rel_position_20d'] = (close[-1] - low_20) / (high_20 - low_20) * 100
            
            # 60日相对位置
            if len(high) >= 60:
                high_60 = np.max(high[-60:])
                low_60 = np.min(low[-60:])
                if high_60 > low_60:
                    result['rel_position_60d'] = (close[-1] - low_60) / (high_60 - low_60) * 100
            
            # 突破新高
            if len(high) >= 60:
                high_60_prev = np.max(high[-60:-1])  # 不包含当日
                result['breakout_60d'] = close[-1] > high_60_prev
                result['breakout_ratio'] = (close[-1] / high_60_prev - 1) * 100 if high_60_prev > 0 else 0
            
            # -----------------------------------------------------------------
            # RSI计算（用于超卖判断）
            # -----------------------------------------------------------------
            if len(close) >= 15:
                deltas = np.diff(close[-15:])
                gains = np.where(deltas > 0, deltas, 0)
                losses = np.where(deltas < 0, -deltas, 0)
                avg_gain = np.mean(gains)
                avg_loss = np.mean(losses)
                if avg_loss > 0:
                    rs = avg_gain / avg_loss
                    result['rsi'] = 100 - (100 / (1 + rs))
                else:
                    result['rsi'] = 100
            
            # 均线偏离
            if len(close) >= 20:
                ma_20 = np.mean(close[-20:])
                result['ma_deviation'] = (close[-1] / ma_20 - 1) * 100
            
            # -----------------------------------------------------------------
            # 连续特征
            # -----------------------------------------------------------------
            # 连续上涨天数
            up_days = 0
            for j in range(len(close)-1, max(len(close)-11, 0), -1):
                if j > 0 and close[j] > close[j-1]:
                    up_days += 1
                else:
                    break
            result['consecutive_up_days'] = up_days
            
            # 连续放量天数
            vol_up_days = 0
            for j in range(len(volume)-1, max(len(volume)-11, 0), -1):
                if j > 0 and volume[j] > volume[j-1]:
                    vol_up_days += 1
                else:
                    break
            result['consecutive_vol_up_days'] = vol_up_days
            
        except Exception as e:
            logger.error(f"因子计算失败 [{code}]: {e}")
        
        return result
    
    # =========================================================================
    # 信号评分
    # =========================================================================
    
    def score_extreme_signal(
        self,
        factors: Dict[str, Any],
        market_state: MarketState = MarketState.NEUTRAL
    ) -> Tuple[float, SignalType]:
        """
        极端信号评分
        
        根据市场状态和因子值，计算综合评分并确定信号类型。
        
        牛市评分逻辑：
        - 首板启动：首次涨停+放量>3倍+突破 → 评分75
        - 连板加速：近期有涨停 → 评分60
        - 强势突破：突破60日高+动量强+放量 → 评分60
        - 量价齐升：动量>20%+放量>1.5+爆发>2 → 评分55
        
        震荡市评分逻辑：
        - 相对位置<50%权重40%
        - 量比>1.2权重25%
        - RSI<30权重20%
        - 均线偏离<-5%权重15%
        
        Args:
            factors: 因子字典
            market_state: 市场状态
            
        Returns:
            Tuple[float, SignalType]: (评分, 信号类型)
        """
        score = 0.0
        signal_type = SignalType.NO_SIGNAL
        
        if market_state == MarketState.BULL:
            # -----------------------------------------------------------------
            # 牛市追涨策略评分
            # -----------------------------------------------------------------
            
            # 策略1: 首板启动（最强信号）
            is_first_limit_up = factors.get('is_first_limit_up', False)
            
            if is_first_limit_up:
                score = 50
                signal_type = SignalType.FIRST_LIMIT_UP
                
                # 放量加分
                vol_ratio = factors.get('volume_ratio_1d', 1)
                if vol_ratio > self.config.volume_explosion_threshold:
                    score += 25
                elif vol_ratio > 2:
                    score += 15
                
                # 突破加分
                if factors.get('breakout_60d', False):
                    score += 15
                
                return score, signal_type
            
            # 策略2: 连板加速
            limit_up_recent = factors.get('limit_up_recent', 0)
            limit_up_count = factors.get('limit_up_count', 0)
            
            if limit_up_recent >= 1:
                score = 40
                signal_type = SignalType.CONSECUTIVE_LIMIT_UP
                
                if limit_up_count >= 2:
                    score += 20
                
                return score, signal_type
            
            # 策略3: 强势突破
            breakout_60d = factors.get('breakout_60d', False)
            breakout_ratio = factors.get('breakout_ratio', 0)
            mom_5d = factors.get('mom_5d', 0)
            vol_ratio_5d = factors.get('volume_ratio_5d', 1)
            
            if (breakout_60d and 
                breakout_ratio > self.config.breakout_threshold and
                mom_5d > self.config.momentum_5d_threshold and
                vol_ratio_5d > 1.5):
                score = 60
                signal_type = SignalType.STRONG_BREAKOUT
                return score, signal_type
            
            # 策略4: 量价齐升
            money_explosion = factors.get('money_explosion', 1)
            
            if (mom_5d > 20 and vol_ratio_5d > 1.5 and money_explosion > 2):
                score = 55
                signal_type = SignalType.VOLUME_PRICE_RISE
                
                # 连续上涨加分
                up_days = factors.get('consecutive_up_days', 0)
                if up_days >= 4:
                    score += 15
                
                return score, signal_type
            
            # 策略5: 动量加速
            mom_acceleration = factors.get('mom_acceleration', 0)
            
            if mom_acceleration > 15 and mom_5d > 10:
                score = 50
                signal_type = SignalType.VOLUME_PRICE_RISE
                return score, signal_type
        
        else:
            # -----------------------------------------------------------------
            # 震荡市/熊市低位布局策略评分
            # -----------------------------------------------------------------
            score = 50.0
            
            # 相对位置（权重40%）
            rel_pos = factors.get('rel_position_20d', 50)
            if rel_pos < 20:
                score += 25
            elif rel_pos < 35:
                score += 20
            elif rel_pos < self.config.rel_position_low:
                score += 15
            elif rel_pos > 80:
                score -= 15
            
            # 量比（权重25%）
            vol_ratio = factors.get('volume_ratio_5d', 1)
            if vol_ratio > 1.5:
                score += 15
            elif vol_ratio > 1.2:
                score += 10
            elif vol_ratio > 1.0:
                score += 5
            
            # RSI（权重20%）
            rsi = factors.get('rsi', 50)
            if rsi < self.config.rsi_oversold:
                score += 15
                signal_type = SignalType.LOW_POSITION_REBOUND
            elif rsi < 40:
                score += 10
            elif rsi < 50:
                score += 5
            elif rsi > 75:
                score -= 10
            
            # 均线偏离（权重15%）
            ma_dev = factors.get('ma_deviation', 0)
            if ma_dev < -15:
                score += 12
            elif ma_dev < -10:
                score += 8
            elif ma_dev < -5:
                score += 5
            elif ma_dev > 10:
                score -= 5
            
            if signal_type == SignalType.NO_SIGNAL and score >= self.config.signal_threshold:
                signal_type = SignalType.LOW_POSITION_REBOUND
        
        return score, signal_type
    
    # =========================================================================
    # 信号生成
    # =========================================================================
    
    def generate_signals(
        self,
        price_data: pd.DataFrame,
        universe: List[str],
        date: str,
        market_state: Optional[MarketState] = None
    ) -> List[Signal]:
        """
        生成交易信号
        
        遍历股票池，计算每只股票的因子和评分，筛选出达到阈值的信号。
        
        流程：
        1. 遍历股票池
        2. 计算每只股票的因子
        3. 评分并确定信号类型
        4. 筛选评分 >= 阈值的信号
        5. 按评分排序返回
        
        Args:
            price_data: 价格数据
            universe: 股票池列表
            date: 信号日期
            market_state: 市场状态（可选，如果不传则使用当前状态）
            
        Returns:
            List[Signal]: 信号列表（按评分降序排列）
        """
        if market_state is None:
            market_state = self._current_market_state
        
        signals: List[Signal] = []
        
        for code in universe:
            try:
                # 计算因子
                factors = self.calculate_extreme_factors(price_data, code, date)
                
                if not factors or 'close' not in factors:
                    continue
                
                # 评分
                score, signal_type = self.score_extreme_signal(factors, market_state)
                
                # 筛选信号
                if score >= self.config.signal_threshold and signal_type != SignalType.NO_SIGNAL:
                    signal = Signal(
                        code=code,
                        signal_type=signal_type,
                        score=score,
                        factors=factors,
                        date=date,
                        price=factors.get('close', 0),
                        reason=self._generate_signal_reason(factors, signal_type)
                    )
                    signals.append(signal)
                    
            except Exception as e:
                logger.debug(f"信号生成失败 [{code}]: {e}")
                continue
        
        # 按评分排序
        signals.sort(key=lambda x: x.score, reverse=True)
        
        logger.info(f"信号生成完成 [{date}]: 共{len(signals)}个信号 (市场状态={market_state.value})")
        
        return signals
    
    def _generate_signal_reason(self, factors: Dict, signal_type: SignalType) -> str:
        """生成信号说明"""
        reasons = []
        
        if signal_type == SignalType.FIRST_LIMIT_UP:
            reasons.append("首板启动")
            if factors.get('volume_ratio_1d', 0) > 3:
                reasons.append(f"放量{factors['volume_ratio_1d']:.1f}倍")
            if factors.get('breakout_60d'):
                reasons.append("突破60日高点")
                
        elif signal_type == SignalType.CONSECUTIVE_LIMIT_UP:
            reasons.append(f"连板({factors.get('limit_up_count', 0)}板)")
            
        elif signal_type == SignalType.STRONG_BREAKOUT:
            reasons.append(f"突破60日高+{factors.get('breakout_ratio', 0):.1f}%")
            reasons.append(f"5日动量{factors.get('mom_5d', 0):.1f}%")
            
        elif signal_type == SignalType.VOLUME_PRICE_RISE:
            reasons.append(f"5日动量{factors.get('mom_5d', 0):.1f}%")
            reasons.append(f"量比{factors.get('volume_ratio_5d', 0):.2f}")
            
        elif signal_type == SignalType.LOW_POSITION_REBOUND:
            rel_pos = factors.get('rel_position_20d', 50)
            rsi = factors.get('rsi', 50)
            reasons.append(f"相对位置{rel_pos:.1f}%")
            if rsi < 30:
                reasons.append(f"RSI超卖({rsi:.1f})")
        
        return " | ".join(reasons) if reasons else str(signal_type.value)
    
    # =========================================================================
    # 风险控制
    # =========================================================================
    
    def apply_risk_control(
        self,
        positions: Dict[str, Position],
        current_prices: Dict[str, float]
    ) -> List[Order]:
        """
        应用风险控制
        
        检查所有持仓的止损止盈条件，生成平仓订单。
        
        止损条件：
        - 亏损 <= stop_loss_pct（默认-10%）
        
        止盈条件：
        - 盈利 >= take_profit_pct（默认+25%）
        
        Args:
            positions: 当前持仓字典
            current_prices: 当前价格字典
            
        Returns:
            List[Order]: 平仓订单列表
        """
        orders: List[Order] = []
        
        for code, pos in positions.items():
            if code not in current_prices:
                continue
            
            current_price = current_prices[code]
            pnl_pct = (current_price / pos.cost - 1) * 100
            
            # 更新最高价
            pos.max_price = max(pos.max_price, current_price)
            
            # 止损检查
            if pnl_pct <= self.config.stop_loss_pct:
                order = Order(
                    code=code,
                    direction='SELL',
                    shares=pos.shares,
                    price=current_price,
                    reason=f"止损: {pnl_pct:.1f}%"
                )
                orders.append(order)
                logger.info(f"触发止损 [{code}]: {pnl_pct:.1f}%")
            
            # 止盈检查
            elif pnl_pct >= self.config.take_profit_pct:
                order = Order(
                    code=code,
                    direction='SELL',
                    shares=pos.shares,
                    price=current_price,
                    reason=f"止盈: {pnl_pct:.1f}%"
                )
                orders.append(order)
                logger.info(f"触发止盈 [{code}]: {pnl_pct:.1f}%")
        
        return orders
    
    # =========================================================================
    # 辅助方法
    # =========================================================================
    
    def get_strategy_description(self) -> str:
        """获取策略描述"""
        return f"""
牛市极端高收益策略 v1.0

【策略概述】
自适应周频策略，根据市场状态切换选股逻辑

【市场状态】
- 牛市：追涨策略（涨停板、强动量、突破）
- 震荡市：低位布局（超卖反弹、放量底部）
- 熊市：防守策略（降低仓位）

【核心信号】
1. 首板启动: 首次涨停+放量>3倍+突破60日高 (评分75)
2. 连板加速: 2连板或以上 (评分60)
3. 强势突破: 突破60日高>5%+5日动量>15%+量比>1.5 (评分60)
4. 量价齐升: 5日动量>20%+量比>1.5+成交额爆发>2倍 (评分55)
5. 低位反弹: 相对位置<50%+RSI<30+放量 (评分70)

【风控规则】
- 止损: {self.config.stop_loss_pct}%
- 止盈: {self.config.take_profit_pct}%
- 最大持仓: {self.config.max_positions}只
- 单票仓位: {self.config.position_size_pct}%

【参数配置】
- 信号阈值: {self.config.signal_threshold}
- 调仓周期: {self.config.rebalance_days}天
- 涨停阈值: {self.config.limit_up_threshold}%
- 量比爆发阈值: {self.config.volume_explosion_threshold}
"""
    
    def get_strategy_code(self) -> str:
        """
        获取策略Python代码
        
        返回格式化的策略代码字符串，用于报告展示
        """
        return '''# -*- coding: utf-8 -*-
"""
================================================================================
牛市极端高收益策略 - BulletTrade版本
================================================================================
策略说明：
  本策略基于历史牛市数据挖掘，采用自适应机制在不同市场状态下切换选股逻辑
  
核心信号：
  1. 首板启动: 首次涨停+放量>3倍+突破60日高
  2. 连板加速: 2连板或以上
  3. 强势突破: 突破60日高>5%+5日动量>15%+量比>1.5
  4. 量价齐升: 5日动量>20%+量比>1.5+成交额爆发>2倍

风控规则：
  - 止损: -10%
  - 止盈: +25%
  - 最大持仓: 2只

作者: TRQuant Team
日期: 2026-01-10
================================================================================
"""

from jqdata import *
import numpy as np
import pandas as pd

# =============================================================================
# 策略参数配置
# =============================================================================

# 信号参数
SIGNAL_THRESHOLD = 60         # 信号评分阈值
MAX_POSITIONS = 2             # 最大持仓数量

# 风控参数
STOP_LOSS_PCT = -10.0         # 止损比例 (%)
TAKE_PROFIT_PCT = 25.0        # 止盈比例 (%)

# 因子阈值
LIMIT_UP_THRESHOLD = 0.095    # 涨停判定阈值
VOLUME_EXPLOSION_THRESHOLD = 3.0  # 量比爆发阈值
MOMENTUM_5D_THRESHOLD = 10.0  # 5日动量阈值
BREAKOUT_THRESHOLD = 5.0      # 突破幅度阈值 (%)


# =============================================================================
# 初始化函数
# =============================================================================

def initialize(context):
    """
    策略初始化
    
    设置基准、滑点、手续费等基础参数
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 开启动态复权
    set_option('use_real_price', True)
    
    # 设置滑点
    set_slippage(FixedSlippage(0.02))
    
    # 设置手续费
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0001,
        close_commission=0.0001,
        min_commission=5
    ), type='stock')
    
    # 策略变量
    context.positions = {}        # 持仓记录
    context.trade_count = 0       # 交易计数
    context.rebalance_day = 0     # 调仓计数
    
    # 打印策略信息
    log.info("="*60)
    log.info("牛市极端高收益策略 v1.0 初始化完成")
    log.info(f"信号阈值: {SIGNAL_THRESHOLD}")
    log.info(f"最大持仓: {MAX_POSITIONS}")
    log.info(f"止损/止盈: {STOP_LOSS_PCT}%/{TAKE_PROFIT_PCT}%")
    log.info("="*60)


# =============================================================================
# 每日盘前处理
# =============================================================================

def before_trading_start(context):
    """
    盘前处理
    
    1. 获取股票池
    2. 检测市场状态
    """
    # 获取沪深300成分股
    context.universe = get_index_stocks('000300.XSHG')
    
    # 检测市场状态
    context.market_state = detect_market_state(context)
    
    log.info(f"[{context.current_dt.date()}] 市场状态: {context.market_state}")


# =============================================================================
# 市场状态检测
# =============================================================================

def detect_market_state(context):
    """
    检测市场状态
    
    通过分析沪深300指数判断当前市场状态
    
    Returns:
        str: 'BULL' / 'NEUTRAL' / 'BEAR'
    """
    # 获取指数数据
    index_data = get_price(
        '000300.XSHG',
        end_date=context.current_dt,
        frequency='daily',
        fields=['close'],
        count=60,
        fq='post'
    )
    
    if len(index_data) < 60:
        return 'NEUTRAL'
    
    close = index_data['close'].values
    
    # 计算动量
    mom_20d = (close[-1] / close[-20] - 1) * 100
    mom_60d = (close[-1] / close[-60] - 1) * 100
    
    # 计算均线
    ma_20 = np.mean(close[-20:])
    ma_60 = np.mean(close[-60:])
    
    # 综合评分
    bull_score = 0.0
    bear_score = 0.0
    
    if mom_20d > 10:
        bull_score += 0.3
    elif mom_20d < -10:
        bear_score += 0.3
    
    if mom_60d > 20:
        bull_score += 0.4
    elif mom_60d < -20:
        bear_score += 0.4
    
    if close[-1] > ma_20 > ma_60:
        bull_score += 0.3
    elif close[-1] < ma_20 < ma_60:
        bear_score += 0.3
    
    if bull_score > 0.5:
        return 'BULL'
    elif bear_score > 0.5:
        return 'BEAR'
    else:
        return 'NEUTRAL'


# =============================================================================
# 每日交易处理
# =============================================================================

def handle_data(context, data):
    """
    每日交易主逻辑
    
    1. 检查止损止盈
    2. 周频调仓时生成信号
    3. 执行买卖
    """
    context.rebalance_day += 1
    
    # 1. 风控检查
    check_risk_control(context, data)
    
    # 2. 周频调仓（每5个交易日）
    if context.rebalance_day % 5 == 0:
        rebalance(context, data)


# =============================================================================
# 风险控制
# =============================================================================

def check_risk_control(context, data):
    """
    检查止损止盈
    """
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.total_amount == 0:
            continue
        
        current_price = data[stock].close
        cost = pos.avg_cost
        pnl_pct = (current_price / cost - 1) * 100
        
        # 止损
        if pnl_pct <= STOP_LOSS_PCT:
            order_target(stock, 0)
            log.info(f"[止损] {stock}: {pnl_pct:.1f}%")
            context.trade_count += 1
        
        # 止盈
        elif pnl_pct >= TAKE_PROFIT_PCT:
            order_target(stock, 0)
            log.info(f"[止盈] {stock}: {pnl_pct:.1f}%")
            context.trade_count += 1


# =============================================================================
# 调仓逻辑
# =============================================================================

def rebalance(context, data):
    """
    调仓主逻辑
    """
    # 1. 计算所有股票的信号评分
    signals = []
    for stock in context.universe:
        try:
            score, signal_type = calculate_signal_score(stock, context, data)
            if score >= SIGNAL_THRESHOLD:
                signals.append({
                    'stock': stock,
                    'score': score,
                    'signal_type': signal_type
                })
        except:
            continue
    
    # 2. 按评分排序
    signals.sort(key=lambda x: x['score'], reverse=True)
    
    # 3. 选择目标股票
    target_stocks = [s['stock'] for s in signals[:MAX_POSITIONS]]
    
    log.info(f"[调仓] 信号数={len(signals)}, 目标={target_stocks}")
    
    # 4. 卖出不在目标列表的股票
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target(stock, 0)
            log.info(f"[卖出-轮动] {stock}")
            context.trade_count += 1
    
    # 5. 买入目标股票
    if target_stocks:
        cash = context.portfolio.available_cash
        per_stock_cash = cash / len(target_stocks) * 0.95
        
        for stock in target_stocks:
            if stock not in context.portfolio.positions:
                order_value(stock, per_stock_cash)
                log.info(f"[买入] {stock}")
                context.trade_count += 1


# =============================================================================
# 信号评分计算
# =============================================================================

def calculate_signal_score(stock, context, data):
    """
    计算股票的信号评分
    
    Args:
        stock: 股票代码
        context: 上下文
        data: 数据
        
    Returns:
        Tuple[float, str]: (评分, 信号类型)
    """
    # 获取历史数据
    df = get_price(
        stock,
        end_date=context.current_dt,
        frequency='daily',
        fields=['open', 'close', 'high', 'low', 'volume', 'money'],
        count=65,
        fq='post'
    )
    
    if len(df) < 25:
        return 0, 'NO_SIGNAL'
    
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    volume = df['volume'].values
    money = df['money'].values
    
    # 计算因子
    factors = {}
    
    # 涨停判断
    limit_up_count = sum(
        1 for i in range(max(len(close)-5, 1), len(close))
        if close[i] / close[i-1] - 1 > LIMIT_UP_THRESHOLD
    )
    factors['limit_up_count'] = limit_up_count
    
    # 首板判断
    is_first_limit_up = False
    if len(close) >= 30:
        if close[-1] / close[-2] - 1 > LIMIT_UP_THRESHOLD:
            prev_limit_ups = sum(
                1 for i in range(len(close)-30, len(close)-1)
                if i > 0 and close[i] / close[i-1] - 1 > LIMIT_UP_THRESHOLD
            )
            if prev_limit_ups == 0:
                is_first_limit_up = True
    factors['is_first_limit_up'] = is_first_limit_up
    
    # 动量
    factors['mom_5d'] = (close[-1] / close[-6] - 1) * 100 if len(close) >= 6 else 0
    
    # 量比
    vol_5d = np.mean(volume[-5:])
    vol_20d = np.mean(volume[-20:])
    factors['volume_ratio_5d'] = vol_5d / vol_20d if vol_20d > 0 else 1
    factors['volume_ratio_1d'] = volume[-1] / vol_20d if vol_20d > 0 else 1
    
    # 成交额爆发
    money_20d_avg = np.mean(money[-20:])
    factors['money_explosion'] = money[-1] / money_20d_avg if money_20d_avg > 0 else 1
    
    # 突破
    high_60_prev = np.max(high[-60:-1]) if len(high) >= 60 else high[-1]
    factors['breakout_60d'] = close[-1] > high_60_prev
    factors['breakout_ratio'] = (close[-1] / high_60_prev - 1) * 100 if high_60_prev > 0 else 0
    
    # 相对位置
    high_20 = np.max(high[-20:])
    low_20 = np.min(low[-20:])
    factors['rel_position_20d'] = (close[-1] - low_20) / (high_20 - low_20) * 100 if high_20 > low_20 else 50
    
    # RSI
    deltas = np.diff(close[-15:])
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)
    factors['rsi'] = 100 - (100 / (1 + avg_gain/avg_loss)) if avg_loss > 0 else 100
    
    # 根据市场状态评分
    return score_signal(factors, context.market_state)


def score_signal(factors, market_state):
    """
    信号评分
    """
    score = 0.0
    signal_type = 'NO_SIGNAL'
    
    if market_state == 'BULL':
        # 首板启动
        if factors.get('is_first_limit_up', False):
            score = 50
            signal_type = 'FIRST_LIMIT_UP'
            if factors.get('volume_ratio_1d', 1) > 3:
                score += 25
            if factors.get('breakout_60d', False):
                score += 15
            return score, signal_type
        
        # 连板加速
        if factors.get('limit_up_count', 0) >= 1:
            score = 40
            signal_type = 'CONSECUTIVE_LIMIT_UP'
            if factors.get('limit_up_count', 0) >= 2:
                score += 20
            return score, signal_type
        
        # 强势突破
        if (factors.get('breakout_60d', False) and
            factors.get('breakout_ratio', 0) > 5 and
            factors.get('mom_5d', 0) > 15 and
            factors.get('volume_ratio_5d', 1) > 1.5):
            score = 60
            signal_type = 'STRONG_BREAKOUT'
            return score, signal_type
        
        # 量价齐升
        if (factors.get('mom_5d', 0) > 20 and
            factors.get('volume_ratio_5d', 1) > 1.5 and
            factors.get('money_explosion', 1) > 2):
            score = 55
            signal_type = 'VOLUME_PRICE_RISE'
            return score, signal_type
    
    else:
        # 低位布局评分
        score = 50.0
        
        rel_pos = factors.get('rel_position_20d', 50)
        if rel_pos < 20:
            score += 25
        elif rel_pos < 35:
            score += 20
        elif rel_pos < 50:
            score += 15
        
        vol_ratio = factors.get('volume_ratio_5d', 1)
        if vol_ratio > 1.5:
            score += 15
        elif vol_ratio > 1.2:
            score += 10
        
        rsi = factors.get('rsi', 50)
        if rsi < 30:
            score += 15
            signal_type = 'LOW_POSITION_REBOUND'
        elif rsi < 40:
            score += 10
    
    return score, signal_type


# =============================================================================
# 策略结束处理
# =============================================================================

def after_trading_end(context):
    """
    每日收盘后处理
    """
    pass
'''


# =============================================================================
# 便捷函数
# =============================================================================

def create_default_strategy() -> BullMarketExtremeStrategy:
    """创建默认配置的策略实例"""
    return BullMarketExtremeStrategy(StrategyConfig())


def create_aggressive_strategy() -> BullMarketExtremeStrategy:
    """创建激进配置的策略实例"""
    config = StrategyConfig(
        signal_threshold=50.0,
        max_positions=3,
        stop_loss_pct=-8.0,
        take_profit_pct=30.0,
        position_size_pct=35.0
    )
    return BullMarketExtremeStrategy(config)


def create_conservative_strategy() -> BullMarketExtremeStrategy:
    """创建保守配置的策略实例"""
    config = StrategyConfig(
        signal_threshold=70.0,
        max_positions=2,
        stop_loss_pct=-12.0,
        take_profit_pct=20.0,
        position_size_pct=40.0
    )
    return BullMarketExtremeStrategy(config)
