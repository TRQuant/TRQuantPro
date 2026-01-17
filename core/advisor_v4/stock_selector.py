#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选股逻辑模块 - 基于已验证因子的股票筛选和排序

功能：
1. 基础过滤：排除ST、停牌、涨跌停股票
2. 流动性过滤：日均成交额、换手率
3. 基本面过滤：ROE、净利润增长率
4. 因子筛选：7个已验证因子的最优区间筛选
5. 综合得分排序：按validated_score降序排序，取TOP N
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class StockFilterConfig:
    """选股过滤配置"""
    # 基础过滤
    exclude_st: bool = True  # 排除ST股票
    exclude_688: bool = False  # 排除688开头（科创板，可选）
    exclude_300: bool = False  # 排除300开头（创业板，可选）
    exclude_paused: bool = True  # 排除停牌股票
    exclude_limit_up: bool = True  # 排除涨停股票
    exclude_limit_down: bool = True  # 排除跌停股票
    
    # 流动性过滤
    min_avg_turnover: float = 5000.0  # 最小日均成交额（万元，过去20日）
    min_turnover_rate: float = 2.0  # 最小换手率（%）
    max_turnover_rate: float = 10.0  # 最大换手率（%）
    
    # 基本面过滤
    min_roe: float = 0.0  # 最小ROE（%）
    min_growth: float = -50.0  # 最小净利润增长率（%，避免严重恶化）
    
    # 因子筛选（基于已验证因子的最优区间）
    min_momentum_20d: float = 5.0  # 最小20日动量（%）
    max_momentum_20d: float = 30.0  # 最大20日动量（%）
    max_rel_position: float = 80.0  # 最大相对位置（%）
    min_market_cap: float = 30.0  # 最小市值（亿）
    max_market_cap: float = 200.0  # 最大市值（亿）
    min_momentum_5d: float = -5.0  # 最小5日动量（%）
    max_momentum_5d: float = 10.0  # 最大5日动量（%）
    
    # 综合得分筛选
    min_total_score: float = 60.0  # 最小综合得分
    
    # 选股数量
    top_n: int = 10  # 取TOP N只股票


class StockSelector:
    """选股逻辑模块"""
    
    def __init__(
        self,
        config: Optional[StockFilterConfig] = None,
        jq=None,
        verbose: bool = True,
    ):
        """
        初始化选股器
        
        Args:
            config: 选股配置
            jq: JQData客户端（可选，如果提供则进行实时过滤）
            verbose: 是否输出详细信息
        """
        self.config = config or StockFilterConfig()
        self.jq = jq
        self.verbose = verbose
    
    def filter_basic(self, codes: List[str], date: str) -> List[str]:
        """
        基础过滤：排除ST、停牌、涨跌停股票
        
        Args:
            codes: 股票代码列表
            date: 日期
            
        Returns:
            过滤后的股票代码列表
        """
        if not codes:
            return []
        
        if self.jq is None:
            # 如果没有JQData客户端，只做简单的代码过滤
            filtered = []
            for code in codes:
                if self.config.exclude_st and ('ST' in code or '*ST' in code):
                    continue
                if self.config.exclude_688 and code.startswith('688'):
                    continue
                if self.config.exclude_300 and code.startswith('300'):
                    continue
                filtered.append(code)
            return filtered
        
        filtered = []
        
        try:
            # 获取股票信息
            securities = self.jq.get_all_securities(['stock'], date=date)
            
            for code in codes:
                if code not in securities.index:
                    continue
                
                stock_info = securities.loc[code]
                
                # 排除ST股票
                if self.config.exclude_st:
                    if 'ST' in stock_info.get('display_name', '') or '*ST' in stock_info.get('display_name', ''):
                        continue
                
                # 排除688/300开头
                if self.config.exclude_688 and code.startswith('688'):
                    continue
                if self.config.exclude_300 and code.startswith('300'):
                    continue
                
                # 检查停牌
                if self.config.exclude_paused:
                    try:
                        current_data = self.jq.get_current_data([code])
                        if current_data[code].paused:
                            continue
                    except:
                        pass
                
                # 检查涨跌停
                if self.config.exclude_limit_up or self.config.exclude_limit_down:
                    try:
                        current_data = self.jq.get_current_data([code])
                        if self.config.exclude_limit_up and current_data[code].is_limit_up:
                            continue
                        if self.config.exclude_limit_down and current_data[code].is_limit_down:
                            continue
                    except:
                        pass
                
                filtered.append(code)
                
        except Exception as e:
            logger.warning(f"基础过滤失败@{date}: {e}")
            # 回退到简单过滤
            filtered = [c for c in codes if not (self.config.exclude_st and ('ST' in c or '*ST' in c))]
        
        if self.verbose:
            print(f"[基础过滤] {len(codes)} -> {len(filtered)} 只股票")
        
        return filtered
    
    def filter_liquidity(self, codes: List[str], date: str, factors_df: pd.DataFrame) -> pd.DataFrame:
        """
        流动性过滤：日均成交额、换手率
        
        Args:
            codes: 股票代码列表
            date: 日期
            factors_df: 因子数据DataFrame（必须包含turnover_rate列）
            
        Returns:
            过滤后的因子数据DataFrame
        """
        if factors_df.empty:
            return factors_df
        
        # 换手率过滤
        if 'turnover_rate' in factors_df.columns:
            mask = (
                (factors_df['turnover_rate'] >= self.config.min_turnover_rate) &
                (factors_df['turnover_rate'] <= self.config.max_turnover_rate)
            )
            factors_df = factors_df[mask].copy()
        
        # 日均成交额过滤（如果有avg_money列）
        if 'avg_money' in factors_df.columns:
            mask = factors_df['avg_money'] >= self.config.min_avg_turnover
            factors_df = factors_df[mask].copy()
        
        if self.verbose:
            print(f"[流动性过滤] 剩余 {len(factors_df)} 只股票")
        
        return factors_df
    
    def filter_fundamental(self, factors_df: pd.DataFrame) -> pd.DataFrame:
        """
        基本面过滤：ROE、净利润增长率
        
        Args:
            factors_df: 因子数据DataFrame（必须包含roe、growth列）
            
        Returns:
            过滤后的因子数据DataFrame
        """
        if factors_df.empty:
            return factors_df
        
        mask = pd.Series(True, index=factors_df.index)
        
        # ROE过滤
        if 'roe' in factors_df.columns:
            mask = mask & (factors_df['roe'] >= self.config.min_roe)
        
        # 净利润增长率过滤
        if 'growth' in factors_df.columns:
            mask = mask & (factors_df['growth'] >= self.config.min_growth)
        
        factors_df = factors_df[mask].copy()
        
        if self.verbose:
            print(f"[基本面过滤] 剩余 {len(factors_df)} 只股票")
        
        return factors_df
    
    def filter_factors(self, factors_df: pd.DataFrame) -> pd.DataFrame:
        """
        因子筛选：7个已验证因子的最优区间筛选
        
        Args:
            factors_df: 因子数据DataFrame（必须包含7个已验证因子的列）
            
        Returns:
            过滤后的因子数据DataFrame
        """
        if factors_df.empty:
            return factors_df
        
        mask = pd.Series(True, index=factors_df.index)
        
        # 20日动量筛选（5%~30%）
        if 'momentum_20d' in factors_df.columns:
            mask = mask & (
                (factors_df['momentum_20d'] >= self.config.min_momentum_20d) &
                (factors_df['momentum_20d'] <= self.config.max_momentum_20d)
            )
        
        # 相对位置筛选（<80%）
        if 'rel_position' in factors_df.columns:
            mask = mask & (factors_df['rel_position'] <= self.config.max_rel_position)
        
        # 市值筛选（30~200亿）
        if 'market_cap' in factors_df.columns:
            mask = mask & (
                (factors_df['market_cap'] >= self.config.min_market_cap) &
                (factors_df['market_cap'] <= self.config.max_market_cap)
            )
        
        # 5日动量筛选（-5%~10%）
        if 'momentum_5d' in factors_df.columns:
            mask = mask & (
                (factors_df['momentum_5d'] >= self.config.min_momentum_5d) &
                (factors_df['momentum_5d'] <= self.config.max_momentum_5d)
            )
        
        # 换手率筛选（2%~10%，已在流动性过滤中处理，这里只做二次确认）
        if 'turnover_rate' in factors_df.columns:
            mask = mask & (
                (factors_df['turnover_rate'] >= self.config.min_turnover_rate) &
                (factors_df['turnover_rate'] <= self.config.max_turnover_rate)
            )
        
        factors_df = factors_df[mask].copy()
        
        if self.verbose:
            print(f"[因子筛选] 剩余 {len(factors_df)} 只股票")
        
        return factors_df
    
    def select_top_n(self, factors_df: pd.DataFrame) -> List[str]:
        """
        综合得分排序：按validated_score或total_score降序排序，取TOP N
        
        Args:
            factors_df: 因子数据DataFrame（必须包含total_score或validated_score列）
            
        Returns:
            选中的股票代码列表
        """
        if factors_df.empty:
            return []
        
        # 确定得分列
        score_col = 'total_score'
        if score_col not in factors_df.columns:
            score_col = 'validated_score'
        
        if score_col not in factors_df.columns:
            logger.warning("因子数据中缺少total_score或validated_score列，无法排序")
            return factors_df['code'].head(self.config.top_n).tolist()
        
        # 综合得分筛选
        if self.config.min_total_score > 0:
            factors_df = factors_df[factors_df[score_col] >= self.config.min_total_score].copy()
        
        # 按得分降序排序
        factors_df = factors_df.sort_values(score_col, ascending=False)
        
        # 取TOP N
        selected_codes = factors_df.head(self.config.top_n)['code'].tolist()
        
        if self.verbose:
            print(f"[选股排序] 选中 {len(selected_codes)} 只股票")
            if len(selected_codes) > 0:
                print(f"  得分范围: {factors_df[score_col].min():.1f} ~ {factors_df[score_col].max():.1f}")
                print(f"  前3只: {selected_codes[:3]}")
        
        return selected_codes
    
    def select_stocks(
        self,
        codes: List[str],
        date: str,
        factors_df: pd.DataFrame,
    ) -> List[str]:
        """
        完整选股流程：基础过滤 -> 流动性过滤 -> 基本面过滤 -> 因子筛选 -> 综合得分排序
        
        Args:
            codes: 初始股票代码列表
            date: 日期
            factors_df: 因子数据DataFrame（必须包含所有需要的因子列）
            
        Returns:
            选中的股票代码列表
        """
        if not codes:
            return []
        
        if factors_df.empty:
            logger.warning("因子数据为空，无法选股")
            return []
        
        # 1. 基础过滤
        filtered_codes = self.filter_basic(codes, date)
        if not filtered_codes:
            return []
        
        # 只保留基础过滤后的股票
        factors_df = factors_df[factors_df['code'].isin(filtered_codes)].copy()
        
        # 2. 流动性过滤
        factors_df = self.filter_liquidity(filtered_codes, date, factors_df)
        
        # 3. 基本面过滤
        factors_df = self.filter_fundamental(factors_df)
        
        # 4. 因子筛选
        factors_df = self.filter_factors(factors_df)
        
        # 5. 综合得分排序
        selected_codes = self.select_top_n(factors_df)
        
        return selected_codes
