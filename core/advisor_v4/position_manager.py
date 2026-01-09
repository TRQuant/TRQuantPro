#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仓位管理模块 - 目标仓位计算、仓位分配策略、调仓逻辑

功能：
1. 目标仓位计算：最大持股数量、单票最大仓位、总仓位上限
2. 仓位分配策略：等权分配或按得分加权
3. 调仓逻辑：调仓频率、调仓触发条件
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class PositionConfig:
    """仓位配置"""
    max_stocks: int = 10  # 最大持股数量
    single_position_max: float = 0.20  # 单票最大仓位（20%）
    total_position_max: float = 0.95  # 总仓位上限（95%）
    min_cash_ratio: float = 0.05  # 最小现金保留（5%）
    
    # 仓位分配策略
    allocation_method: str = "equal"  # "equal"（等权）或 "score_weighted"（按得分加权）
    
    # 调仓配置
    rebalance_frequency: str = "weekly"  # "weekly"（每周）或 "daily"（每日）
    rebalance_weekday: int = 0  # 调仓日：0=周一，1=周二，...，4=周五
    
    # 调仓触发条件
    min_score_threshold: float = 60.0  # 持仓股票得分低于此阈值时触发调仓
    score_drop_threshold: float = 10.0  # 持仓股票得分下降超过此阈值时触发调仓


class PositionManager:
    """仓位管理模块"""
    
    def __init__(
        self,
        config: Optional[PositionConfig] = None,
        verbose: bool = True,
    ):
        """
        初始化仓位管理器
        
        Args:
            config: 仓位配置
            verbose: 是否输出详细信息
        """
        self.config = config or PositionConfig()
        self.verbose = verbose
    
    def calculate_target_positions_equal(
        self,
        selected_stocks: List[str],
        total_value: float,
    ) -> Dict[str, float]:
        """
        等权分配仓位
        
        Args:
            selected_stocks: 选中的股票代码列表
            total_value: 总资产价值
            
        Returns:
            股票代码 -> 目标仓位（0~1）的字典
        """
        if not selected_stocks:
            return {}
        
        # 计算每只股票的等权仓位
        position_per_stock = (1 - self.config.min_cash_ratio) / len(selected_stocks)
        
        # 限制单票最大仓位
        position_per_stock = min(position_per_stock, self.config.single_position_max)
        
        # 构建仓位字典
        positions = {code: position_per_stock for code in selected_stocks}
        
        if self.verbose:
            total_pos = sum(positions.values())
            print(f"[等权分配] {len(selected_stocks)}只股票，单票仓位: {position_per_stock:.1%}，总仓位: {total_pos:.1%}")
        
        return positions
    
    def calculate_target_positions_score_weighted(
        self,
        selected_stocks: List[str],
        total_value: float,
        scores: Dict[str, float],
    ) -> Dict[str, float]:
        """
        按得分加权分配仓位
        
        Args:
            selected_stocks: 选中的股票代码列表
            total_value: 总资产价值
            scores: 股票代码 -> 综合得分的字典
            
        Returns:
            股票代码 -> 目标仓位（0~1）的字典
        """
        if not selected_stocks:
            return {}
        
        # 获取选中股票的得分
        stock_scores = [scores.get(code, 0) for code in selected_stocks]
        
        if sum(stock_scores) == 0:
            # 如果所有得分都是0，回退到等权分配
            return self.calculate_target_positions_equal(selected_stocks, total_value)
        
        # 计算权重（归一化）
        weights = np.array(stock_scores)
        weights = weights / weights.sum()
        
        # 计算每只股票的仓位（基于总仓位上限）
        total_position = 1 - self.config.min_cash_ratio
        positions_raw = weights * total_position
        
        # 限制单票最大仓位
        positions = {}
        for i, code in enumerate(selected_stocks):
            positions[code] = min(positions_raw[i], self.config.single_position_max)
        
        # 如果总仓位超过上限，按比例缩减
        total_pos = sum(positions.values())
        if total_pos > self.config.total_position_max:
            scale = self.config.total_position_max / total_pos
            positions = {code: pos * scale for code, pos in positions.items()}
        
        if self.verbose:
            total_pos = sum(positions.values())
            print(f"[按得分加权] {len(selected_stocks)}只股票，总仓位: {total_pos:.1%}")
            print(f"  仓位范围: {min(positions.values()):.1%} ~ {max(positions.values()):.1%}")
        
        return positions
    
    def calculate_target_positions(
        self,
        selected_stocks: List[str],
        total_value: float,
        scores: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """
        计算目标仓位（根据配置的分配策略）
        
        Args:
            selected_stocks: 选中的股票代码列表
            total_value: 总资产价值
            scores: 股票代码 -> 综合得分的字典（按得分加权时需要）
            
        Returns:
            股票代码 -> 目标仓位（0~1）的字典
        """
        if not selected_stocks:
            return {}
        
        # 限制最大持股数量
        if len(selected_stocks) > self.config.max_stocks:
            selected_stocks = selected_stocks[:self.config.max_stocks]
            if self.verbose:
                print(f"[仓位限制] 超过最大持股数量，只保留前{self.config.max_stocks}只")
        
        # 根据分配策略计算仓位
        if self.config.allocation_method == "score_weighted" and scores:
            return self.calculate_target_positions_score_weighted(
                selected_stocks, total_value, scores
            )
        else:
            return self.calculate_target_positions_equal(selected_stocks, total_value)
    
    def should_rebalance(
        self,
        current_positions: Dict[str, float],
        target_positions: Dict[str, float],
        current_scores: Optional[Dict[str, float]] = None,
        previous_scores: Optional[Dict[str, float]] = None,
    ) -> Tuple[bool, List[str]]:
        """
        判断是否需要调仓
        
        Args:
            current_positions: 当前持仓（股票代码 -> 仓位）
            target_positions: 目标持仓（股票代码 -> 仓位）
            current_scores: 当前综合得分（股票代码 -> 得分）
            previous_scores: 上次综合得分（股票代码 -> 得分）
            
        Returns:
            (是否需要调仓, 调仓原因列表)
        """
        reasons = []
        
        # 1. 股票池变化（新股票进入或旧股票退出）
        current_codes = set(current_positions.keys())
        target_codes = set(target_positions.keys())
        
        new_stocks = target_codes - current_codes
        removed_stocks = current_codes - target_codes
        
        if new_stocks or removed_stocks:
            reasons.append(f"股票池变化（新增{len(new_stocks)}只，移除{len(removed_stocks)}只）")
        
        # 2. 持仓股票得分下降（低于阈值）
        if current_scores:
            for code in current_codes & target_codes:
                score = current_scores.get(code, 0)
                if score < self.config.min_score_threshold:
                    reasons.append(f"{code}得分低于阈值（{score:.1f} < {self.config.min_score_threshold}）")
        
        # 3. 持仓股票得分大幅下降
        if current_scores and previous_scores:
            for code in current_codes & target_codes:
                current_score = current_scores.get(code, 0)
                previous_score = previous_scores.get(code, 0)
                score_drop = previous_score - current_score
                if score_drop > self.config.score_drop_threshold:
                    reasons.append(f"{code}得分大幅下降（{previous_score:.1f} -> {current_score:.1f}，下降{score_drop:.1f}）")
        
        # 4. 仓位差异过大（如果目标仓位与当前仓位差异超过10%，也需要调仓）
        for code in current_codes & target_codes:
            current_pos = current_positions.get(code, 0)
            target_pos = target_positions.get(code, 0)
            if abs(current_pos - target_pos) > 0.10:  # 差异超过10%
                reasons.append(f"{code}仓位差异过大（当前{current_pos:.1%} vs 目标{target_pos:.1%}）")
                break  # 只要有一只股票差异过大就触发调仓
        
        should_rebalance = len(reasons) > 0
        
        if self.verbose and should_rebalance:
            print(f"[调仓判断] 需要调仓，原因: {'; '.join(reasons)}")
        
        return should_rebalance, reasons
    
    def get_rebalance_actions(
        self,
        current_positions: Dict[str, float],
        target_positions: Dict[str, float],
    ) -> Dict[str, Dict[str, float]]:
        """
        获取调仓操作（买入/卖出/调整）
        
        Args:
            current_positions: 当前持仓（股票代码 -> 仓位）
            target_positions: 目标持仓（股票代码 -> 仓位）
            
        Returns:
            {
                'buy': {股票代码: 目标仓位},
                'sell': {股票代码: 目标仓位（0）},
                'adjust': {股票代码: 目标仓位}
            }
        """
        current_codes = set(current_positions.keys())
        target_codes = set(target_positions.keys())
        
        actions = {
            'buy': {},
            'sell': {},
            'adjust': {},
        }
        
        # 卖出：当前持仓但不在目标持仓中
        for code in current_codes - target_codes:
            actions['sell'][code] = 0.0
        
        # 买入：在目标持仓中但当前未持仓
        for code in target_codes - current_codes:
            actions['buy'][code] = target_positions[code]
        
        # 调整：在目标持仓中且当前已持仓，但仓位不同
        for code in current_codes & target_codes:
            current_pos = current_positions.get(code, 0)
            target_pos = target_positions.get(code, 0)
            if abs(current_pos - target_pos) > 0.01:  # 差异超过1%才调整
                actions['adjust'][code] = target_pos
        
        if self.verbose:
            print(f"[调仓操作] 买入{len(actions['buy'])}只，卖出{len(actions['sell'])}只，调整{len(actions['adjust'])}只")
        
        return actions
