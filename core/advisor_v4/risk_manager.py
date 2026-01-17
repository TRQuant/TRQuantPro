#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险控制模块 - 止损止盈、仓位控制、流动性保护

功能：
1. 止损止盈：固定止损、移动止损、固定止盈、分批止盈、时间止损
2. 持仓记录管理：跟踪持仓成本价、最高价、买入日期、分批止盈状态
3. 仓位控制：单票风险、总仓位控制（根据市场环境）
4. 流动性保护：买入前检查、卖出保护
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class PositionRecord:
    """持仓记录"""
    code: str
    entry_date: str  # 买入日期（YYYY-MM-DD）
    entry_price: float  # 成本价
    shares: int  # 持仓数量
    highest_price: float = 0.0  # 持仓期间最高价
    partial_profit_1_done: bool = False  # 是否已执行第一批止盈
    partial_profit_2_done: bool = False  # 是否已执行第二批止盈


@dataclass
class ExitSignal:
    """出场信号"""
    code: str
    exit_reason: str  # 出场原因
    exit_type: str  # "stop_loss"（止损）、"take_profit"（止盈）、"trailing_stop"（移动止损）、"time_stop"（时间止损）
    exit_ratio: float  # 平仓比例（0~1，1.0=全部平仓）
    entry_price: float  # 成本价
    current_price: float  # 当前价
    pnl_rate: float  # 盈亏比例
    holding_days: int  # 持仓天数


@dataclass
class RiskConfig:
    """风险控制配置"""
    # 止损止盈
    stop_loss: float = -0.08  # 固定止损（-8%）
    take_profit: float = 0.30  # 固定止盈（+30%）
    trailing_stop: float = -0.08  # 移动止损（-8%，从最高价回撤）
    trailing_stop_trigger: float = 0.15  # 移动止损触发条件（盈利15%后启用）
    time_stop_days: int = 20  # 时间止损（持仓超过20个交易日）
    
    # 分批止盈
    partial_profit_1: float = 0.20  # 第一批止盈（+20%）
    partial_profit_1_ratio: float = 0.50  # 第一批止盈比例（50%）
    partial_profit_2: float = 0.30  # 第二批止盈（+30%）
    partial_profit_2_ratio: float = 1.0  # 第二批止盈比例（100%，全部平仓）
    
    # 仓位控制
    single_position_max: float = 0.20  # 单票最大仓位（20%）
    single_loss_max: float = 0.02  # 单票最大亏损（总资产的2%）
    
    # 总仓位控制（根据市场环境）
    market_good_position: float = 0.95  # 市场环境好：95%仓位
    market_mid_position: float = 0.50  # 市场环境中：50%仓位
    market_bad_position: float = 0.20  # 市场环境差：20%仓位
    
    # 流动性保护
    min_turnover_rate: float = 2.0  # 最小换手率（%）
    min_avg_turnover: float = 3000.0  # 最小日均成交额（万元，过去5日）


class RiskManager:
    """风险控制模块（统一的风控模块，包含止损止盈、仓位控制、流动性保护）"""
    
    def __init__(
        self,
        config: Optional[RiskConfig] = None,
        jq=None,
        verbose: bool = True,
    ):
        """
        初始化风险管理器
        
        Args:
            config: 风险配置
            jq: JQData客户端（可选，用于获取市场数据）
            verbose: 是否输出详细信息
        """
        self.config = config or RiskConfig()
        self.jq = jq
        self.verbose = verbose
        self.positions: Dict[str, PositionRecord] = {}  # 持仓记录
    
    def check_stop_loss(
        self,
        code: str,
        entry_price: float,
        current_price: float,
    ) -> Tuple[bool, str]:
        """
        检查固定止损
        
        Args:
            code: 股票代码
            entry_price: 成本价
            current_price: 当前价
            
        Returns:
            (是否触发止损, 原因)
        """
        if entry_price <= 0:
            return False, ""
        
        pnl_rate = (current_price / entry_price - 1.0)
        
        if pnl_rate <= self.config.stop_loss:
            return True, f"固定止损（亏损{pnl_rate:.2%} <= {self.config.stop_loss:.2%}）"
        
        return False, ""
    
    def check_take_profit(
        self,
        code: str,
        entry_price: float,
        current_price: float,
        current_position_ratio: float = 1.0,
    ) -> Tuple[bool, float, str]:
        """
        检查固定止盈（支持分批止盈）
        
        Args:
            code: 股票代码
            entry_price: 成本价
            current_price: 当前价
            current_position_ratio: 当前持仓比例（1.0=100%，用于分批止盈）
            
        Returns:
            (是否触发止盈, 目标平仓比例, 原因)
        """
        if entry_price <= 0:
            return False, 0.0, ""
        
        pnl_rate = (current_price / entry_price - 1.0)
        
        # 第一批止盈（+20%）
        if pnl_rate >= self.config.partial_profit_1 and current_position_ratio >= 1.0:
            target_ratio = 1.0 - self.config.partial_profit_1_ratio
            return True, target_ratio, f"第一批止盈（盈利{pnl_rate:.2%} >= {self.config.partial_profit_1:.2%}，减仓{self.config.partial_profit_1_ratio:.0%}）"
        
        # 第二批止盈（+30%，全部平仓）
        if pnl_rate >= self.config.partial_profit_2:
            return True, 0.0, f"第二批止盈（盈利{pnl_rate:.2%} >= {self.config.partial_profit_2:.2%}，全部平仓）"
        
        return False, 0.0, ""
    
    def check_trailing_stop(
        self,
        code: str,
        highest_price: float,
        current_price: float,
        entry_price: float,
    ) -> Tuple[bool, str]:
        """
        检查移动止损
        
        Args:
            code: 股票代码
            highest_price: 持仓期间最高价
            current_price: 当前价
            entry_price: 成本价
            
        Returns:
            (是否触发移动止损, 原因)
        """
        if highest_price <= 0 or entry_price <= 0:
            return False, ""
        
        # 检查是否达到移动止损触发条件（盈利15%后启用）
        pnl_rate = (highest_price / entry_price - 1.0)
        if pnl_rate < self.config.trailing_stop_trigger:
            return False, ""
        
        # 检查从最高价回撤
        trailing_pnl_rate = (current_price / highest_price - 1.0)
        
        if trailing_pnl_rate <= self.config.trailing_stop:
            return True, f"移动止损（从最高价回撤{trailing_pnl_rate:.2%} <= {self.config.trailing_stop:.2%}）"
        
        return False, ""
    
    def check_time_stop(
        self,
        code: str,
        entry_date: str,
        current_date: str,
    ) -> Tuple[bool, str]:
        """
        检查时间止损
        
        Args:
            code: 股票代码
            entry_date: 买入日期（YYYY-MM-DD）
            current_date: 当前日期（YYYY-MM-DD）
            
        Returns:
            (是否触发时间止损, 原因)
        """
        try:
            entry_dt = datetime.strptime(entry_date, '%Y-%m-%d')
            current_dt = datetime.strptime(current_date, '%Y-%m-%d')
            days_held = (current_dt - entry_dt).days
            
            if days_held >= self.config.time_stop_days:
                return True, f"时间止损（持仓{days_held}天 >= {self.config.time_stop_days}天）"
        except Exception as e:
            logger.warning(f"时间止损检查失败 {code}: {e}")
        
        return False, ""
    
    def check_single_position_risk(
        self,
        code: str,
        position_value: float,
        total_value: float,
        entry_price: float,
        current_price: float,
    ) -> Tuple[bool, str]:
        """
        检查单票风险（仓位和亏损）
        
        Args:
            code: 股票代码
            position_value: 持仓市值
            total_value: 总资产
            entry_price: 成本价
            current_price: 当前价
            
        Returns:
            (是否超过风险限制, 原因)
        """
        # 检查单票仓位
        position_ratio = position_value / total_value if total_value > 0 else 0
        if position_ratio > self.config.single_position_max:
            return True, f"单票仓位超限（{position_ratio:.1%} > {self.config.single_position_max:.1%}）"
        
        # 检查单票亏损
        if entry_price > 0:
            pnl_rate = (current_price / entry_price - 1.0)
            loss_value = abs(position_value * pnl_rate) if pnl_rate < 0 else 0
            loss_ratio = loss_value / total_value if total_value > 0 else 0
            
            if loss_ratio > self.config.single_loss_max:
                return True, f"单票亏损超限（{loss_ratio:.1%} > {self.config.single_loss_max:.1%}）"
        
        return False, ""
    
    def get_market_environment(
        self,
        date: str,
    ) -> Tuple[str, float]:
        """
        判断市场环境（用于总仓位控制）
        
        Args:
            date: 日期
            
        Returns:
            (市场环境, 建议总仓位)
            市场环境: "good"（好）、"mid"（中）、"bad"（差）
        """
        if self.jq is None:
            # 如果没有JQData客户端，默认中等仓位
            return "mid", self.config.market_mid_position
        
        try:
            # 获取沪深300指数数据
            prices = self.jq.get_price(
                '000300.XSHG',
                end_date=date,
                count=60,
                frequency='daily',
                fields=['close'],
                fq='post'
            )
            
            if prices is None or len(prices) < 60:
                return "mid", self.config.market_mid_position
            
            close = prices['close']
            
            # 计算MA20和MA60
            ma20 = close.tail(20).mean()
            ma60 = close.tail(60).mean()
            ma20_prev = close.tail(21).head(20).mean()
            
            # 判断市场环境
            if ma20 > ma60:
                # 市场环境好：MA20 > MA60
                return "good", self.config.market_good_position
            elif ma20 < ma60 and ma20 < ma20_prev:
                # 市场环境差：MA20 < MA60 且 MA20下降
                return "bad", self.config.market_bad_position
            else:
                # 市场环境中：MA20 < MA60 但 MA20未下降
                return "mid", self.config.market_mid_position
                
        except Exception as e:
            logger.warning(f"市场环境判断失败@{date}: {e}")
            return "mid", self.config.market_mid_position
    
    def check_liquidity_before_buy(
        self,
        code: str,
        date: str,
        turnover_rate: Optional[float] = None,
        avg_turnover: Optional[float] = None,
    ) -> Tuple[bool, str]:
        """
        买入前流动性检查
        
        Args:
            code: 股票代码
            date: 日期
            turnover_rate: 换手率（%，如果提供则直接使用）
            avg_turnover: 日均成交额（万元，如果提供则直接使用）
            
        Returns:
            (是否通过检查, 原因)
        """
        if self.jq is None:
            # 如果没有JQData客户端，默认通过
            return True, ""
        
        try:
            # 检查换手率
            if turnover_rate is None:
                # 从JQData获取换手率
                q = self.jq.query(
                    self.jq.valuation.code,
                    self.jq.valuation.turnover_ratio,
                ).filter(self.jq.valuation.code == code)
                df = self.jq.get_fundamentals(q, date=date)
                if df is not None and not df.empty:
                    turnover_rate = df['turnover_ratio'].iloc[0]
            
            if turnover_rate is not None and turnover_rate < self.config.min_turnover_rate:
                return False, f"换手率不足（{turnover_rate:.2f}% < {self.config.min_turnover_rate:.2f}%）"
            
            # 检查日均成交额
            if avg_turnover is None:
                # 从JQData获取过去5日成交额
                start_dt = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=10)
                prices = self.jq.get_price(
                    code,
                    start_date=start_dt.strftime('%Y-%m-%d'),
                    end_date=date,
                    frequency='daily',
                    fields=['money'],
                    skip_paused=True,
                    fq='post'
                )
                if prices is not None and len(prices) >= 5:
                    avg_turnover = prices['money'].tail(5).mean() / 10000  # 转换为万元
            
            if avg_turnover is not None and avg_turnover < self.config.min_avg_turnover:
                return False, f"日均成交额不足（{avg_turnover:.0f}万元 < {self.config.min_avg_turnover:.0f}万元）"
            
            return True, ""
            
        except Exception as e:
            logger.warning(f"买入前流动性检查失败 {code}@{date}: {e}")
            # 检查失败时默认通过（避免过度限制）
            return True, ""
    
    def check_sell_protection(
        self,
        code: str,
        date: str,
    ) -> Tuple[bool, str, bool]:
        """
        卖出保护（涨停不能卖出，跌停优先卖出）
        
        Args:
            code: 股票代码
            date: 日期
            
        Returns:
            (是否可以卖出, 原因, 是否优先卖出)
        """
        if self.jq is None:
            return True, "", False
        
        try:
            current_data = self.jq.get_current_data([code])
            if code not in current_data:
                return True, "", False
            
            stock_data = current_data[code]
            
            # 涨停不能卖出
            if stock_data.is_limit_up:
                return False, "涨停不能卖出（挂单等待）", False
            
            # 跌停优先卖出
            if stock_data.is_limit_down:
                return True, "跌停优先卖出（及时止损）", True
            
            return True, "", False
            
        except Exception as e:
            logger.warning(f"卖出保护检查失败 {code}@{date}: {e}")
            return True, "", False
    
    # ==================== 持仓记录管理 ====================
    
    def add_position(
        self,
        code: str,
        entry_date: str,
        entry_price: float,
        shares: int,
    ):
        """
        添加持仓记录
        
        Args:
            code: 股票代码
            entry_date: 买入日期（YYYY-MM-DD）
            entry_price: 成本价
            shares: 持仓数量
        """
        self.positions[code] = PositionRecord(
            code=code,
            entry_date=entry_date,
            entry_price=entry_price,
            shares=shares,
            highest_price=entry_price,
        )
        
        if self.verbose:
            print(f"[添加持仓] {code}，买入日期: {entry_date}，成本价: {entry_price:.2f}，数量: {shares}")
    
    def remove_position(self, code: str):
        """
        移除持仓记录
        
        Args:
            code: 股票代码
        """
        if code in self.positions:
            del self.positions[code]
            if self.verbose:
                print(f"[移除持仓] {code}")
    
    def update_highest_price(self, code: str, current_price: float):
        """
        更新持仓最高价
        
        Args:
            code: 股票代码
            current_price: 当前价
        """
        if code in self.positions:
            self.positions[code].highest_price = max(
                self.positions[code].highest_price,
                current_price
            )
    
    def get_position_record(self, code: str) -> Optional[PositionRecord]:
        """
        获取持仓记录
        
        Args:
            code: 股票代码
            
        Returns:
            PositionRecord 或 None
        """
        return self.positions.get(code)
    
    # ==================== 统一的止损止盈检查（使用持仓记录） ====================
    
    def check_all_exit_signals(
        self,
        code: str,
        current_price: float,
        current_date: str,
    ) -> Optional[ExitSignal]:
        """
        检查所有止损止盈条件（按优先级，使用持仓记录）
        
        优先级：
        1. 固定止损（最优先，避免亏损扩大）
        2. 固定止盈（保护盈利）
        3. 移动止损（保护已实现盈利）
        4. 时间止损（最后检查）
        
        Args:
            code: 股票代码
            current_price: 当前价
            current_date: 当前日期（YYYY-MM-DD）
            
        Returns:
            如果触发任何止损止盈条件，返回ExitSignal；否则返回None
        """
        if code not in self.positions:
            return None
        
        # 更新最高价
        self.update_highest_price(code, current_price)
        
        pos = self.positions[code]
        
        # 1. 检查固定止损（最优先）
        pnl_rate = (current_price / pos.entry_price - 1.0)
        if pnl_rate <= self.config.stop_loss:
            holding_days = self._calculate_holding_days(pos.entry_date, current_date)
            return ExitSignal(
                code=code,
                exit_reason=f"固定止损（亏损{pnl_rate:.2%} <= {self.config.stop_loss:.2%}）",
                exit_type="stop_loss",
                exit_ratio=1.0,
                entry_price=pos.entry_price,
                current_price=current_price,
                pnl_rate=pnl_rate,
                holding_days=holding_days,
            )
        
        # 2. 检查固定止盈
        # 第一批止盈（+20%）
        if pnl_rate >= self.config.partial_profit_1 and not pos.partial_profit_1_done:
            pos.partial_profit_1_done = True
            holding_days = self._calculate_holding_days(pos.entry_date, current_date)
            return ExitSignal(
                code=code,
                exit_reason=f"第一批止盈（盈利{pnl_rate:.2%} >= {self.config.partial_profit_1:.2%}，减仓{self.config.partial_profit_1_ratio:.0%}）",
                exit_type="take_profit",
                exit_ratio=self.config.partial_profit_1_ratio,
                entry_price=pos.entry_price,
                current_price=current_price,
                pnl_rate=pnl_rate,
                holding_days=holding_days,
            )
        
        # 第二批止盈（+30%，全部平仓）
        if pnl_rate >= self.config.partial_profit_2 and not pos.partial_profit_2_done:
            pos.partial_profit_2_done = True
            holding_days = self._calculate_holding_days(pos.entry_date, current_date)
            return ExitSignal(
                code=code,
                exit_reason=f"第二批止盈（盈利{pnl_rate:.2%} >= {self.config.partial_profit_2:.2%}，全部平仓）",
                exit_type="take_profit",
                exit_ratio=1.0,
                entry_price=pos.entry_price,
                current_price=current_price,
                pnl_rate=pnl_rate,
                holding_days=holding_days,
            )
        
        # 3. 检查移动止损
        pnl_rate_from_entry = (pos.highest_price / pos.entry_price - 1.0)
        if pnl_rate_from_entry >= self.config.trailing_stop_trigger:
            trailing_pnl_rate = (current_price / pos.highest_price - 1.0)
            if trailing_pnl_rate <= self.config.trailing_stop:
                holding_days = self._calculate_holding_days(pos.entry_date, current_date)
                return ExitSignal(
                    code=code,
                    exit_reason=f"移动止损（从最高价{pos.highest_price:.2f}回撤{trailing_pnl_rate:.2%} <= {self.config.trailing_stop:.2%}）",
                    exit_type="trailing_stop",
                    exit_ratio=1.0,
                    entry_price=pos.entry_price,
                    current_price=current_price,
                    pnl_rate=pnl_rate,
                    holding_days=holding_days,
                )
        
        # 4. 检查时间止损
        holding_days = self._calculate_holding_days(pos.entry_date, current_date)
        if holding_days >= self.config.time_stop_days:
            return ExitSignal(
                code=code,
                exit_reason=f"时间止损（持仓{holding_days}天 >= {self.config.time_stop_days}天）",
                exit_type="time_stop",
                exit_ratio=1.0,
                entry_price=pos.entry_price,
                current_price=current_price,
                pnl_rate=pnl_rate,
                holding_days=holding_days,
            )
        
        return None
    
    def _calculate_holding_days(
        self,
        entry_date: str,
        current_date: Optional[str] = None,
    ) -> int:
        """
        计算持仓天数
        
        Args:
            entry_date: 买入日期（YYYY-MM-DD）
            current_date: 当前日期（YYYY-MM-DD），如果为None则使用今天
            
        Returns:
            持仓天数
        """
        try:
            entry_dt = datetime.strptime(entry_date, '%Y-%m-%d')
            if current_date:
                current_dt = datetime.strptime(current_date, '%Y-%m-%d')
            else:
                current_dt = datetime.now()
            
            return (current_dt - entry_dt).days
        except Exception as e:
            logger.warning(f"计算持仓天数失败 {entry_date}: {e}")
            return 0
