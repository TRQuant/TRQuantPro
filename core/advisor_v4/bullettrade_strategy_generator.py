#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BulletTrade策略代码生成器 - 生成基于7个已验证因子的完整策略代码

功能：
1. 生成聚宽API风格的策略代码
2. 内联实现7个已验证因子的计算逻辑
3. 实现完整的选股、仓位、风控、止损止盈逻辑
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class StrategyConfig:
    """策略配置"""
    # 选股参数
    max_stocks: int = 10  # 最大持股数量
    min_total_score: float = 30.0  # 最小综合得分（降低阈值，确保有股票通过筛选）
    
    # 仓位参数
    single_position_max: float = 0.20  # 单票最大仓位（20%）
    min_cash_ratio: float = 0.05  # 最小现金保留（5%）
    allocation_method: str = "equal"  # "equal"（等权）或 "score_weighted"（按得分加权）
    
    # 调仓参数
    rebalance_weekday: int = 0  # 调仓日：0=周一
    
    # 止损止盈参数
    stop_loss: float = -0.08  # 固定止损（-8%）
    take_profit: float = 0.30  # 固定止盈（+30%）
    trailing_stop: float = -0.08  # 移动止损（-8%）
    trailing_stop_trigger: float = 0.15  # 移动止损触发条件（盈利15%后启用）
    time_stop_days: int = 20  # 时间止损（持仓超过20个交易日）
    
    # 分批止盈
    partial_profit_1: float = 0.20  # 第一批止盈（+20%）
    partial_profit_1_ratio: float = 0.50  # 第一批止盈比例（50%）
    
    # 市场环境判断
    index_ma_fast: int = 20
    index_ma_slow: int = 60
    risk_on_position: float = 0.95  # 风险开：95%仓位
    risk_mid_position: float = 0.50  # 风险中：50%仓位
    risk_off_position: float = 0.20  # 风险关：20%仓位
    
    # 因子筛选阈值
    min_momentum_20d: float = 5.0  # 最小20日动量（%）
    max_momentum_20d: float = 30.0  # 最大20日动量（%）
    max_rel_position: float = 80.0  # 最大相对位置（%）
    min_market_cap: float = 30.0  # 最小市值（亿）
    max_market_cap: float = 200.0  # 最大市值（亿）
    min_momentum_5d: float = -5.0  # 最小5日动量（%）
    max_momentum_5d: float = 10.0  # 最大5日动量（%）
    min_turnover_rate: float = 2.0  # 最小换手率（%）
    max_turnover_rate: float = 10.0  # 最大换手率（%）
    min_roe: float = 0.0  # 最小ROE（%）


class BulletTradeStrategyGenerator:
    """BulletTrade策略代码生成器"""
    
    def __init__(
        self,
        config: Optional[StrategyConfig] = None,
        cache_data_dir: Optional[str] = None,
    ):
        """
        初始化策略代码生成器
        
        Args:
            config: 策略配置
            cache_data_dir: 缓存数据目录
        """
        self.config = config or StrategyConfig()
        self.cache_data_dir = cache_data_dir
    
    def generate_strategy_code(self, cache_data_dir: str = None) -> str:
        """
        生成完整的策略代码
        
        Args:
            cache_data_dir: 缓存数据目录路径（覆盖初始化时的设置）
        
        Returns:
            策略代码字符串
        """
        # 使用传入的cache_data_dir或初始化时的设置
        cache_dir = cache_data_dir or self.cache_data_dir or ""
        # 转换为绝对路径（如果提供）
        if cache_dir:
            from pathlib import Path
            cache_dir = str(Path(cache_dir).absolute())
        
        code = f'''# -*- coding: utf-8 -*-
"""
TRQuant Advisor V4.0 完整因子策略 - BulletTrade版
================================================

基于完整7个已验证因子的多因子选股策略

因子体系:
- 已验证因子（100%权重）：7个因子，基于438个10%+案例

策略逻辑:
1. 选股：基于完整7因子综合得分排序
2. 仓位：等权或按得分加权，单票最大20%
3. 调仓：每周一次（周一）
4. 风控：止损-8%，止盈+30%，移动止损-8%，时间止损20天
"""

# ========== 导入说明 ==========
# BulletTrade引擎会自动注入以下函数到策略命名空间：
# - 数据API: get_price, attribute_history, get_current_data, get_trade_days, get_all_securities, get_index_stocks
# - 订单API: order, order_value, order_target, order_target_value, cancel_order, cancel_all_orders
# - 调度API: run_daily, run_weekly, run_monthly
# - 全局对象: g, log
# - 设置API: set_benchmark, set_order_cost, set_slippage, set_option
# 
# 但是 BulletTrade 不提供 get_fundamentals/query/valuation/indicator
# 因此我们需要直接使用 jqdatasdk 获取基本面数据

import numpy as np
import pandas as pd
import jqdatasdk
from jqdatasdk import query, valuation, indicator, get_fundamentals

# 认证jqdatasdk以获取基本面数据
_jqdata_auth_success = False
try:
    jqdatasdk.auth('13327806797', 'Taorui888')
    _jqdata_auth_success = True
except Exception as _auth_err:
    pass  # 认证失败时静默处理，稍后在使用时会报错

# ==================== 工具函数 ====================
def _flatten_multiindex_columns(df):
    """处理MultiIndex列名，展平为简单字符串"""
    if df is None or df.empty:
        return df
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[-1] if isinstance(col, tuple) else col for col in df.columns]
    return df

def _calculate_momentum(prices_df, codes, days, default=0.0):
    """通用动量计算函数"""
    result = {{}}
    if prices_df is None or prices_df.empty:
        return {{code: default for code in codes}}
    
    prices_df = _flatten_multiindex_columns(prices_df)
    has_code_col = 'code' in prices_df.columns
    
    if has_code_col:
        for code in codes:
            code_data = prices_df[prices_df['code'] == code]
            if len(code_data) >= days:
                close_values = pd.to_numeric(code_data['close'], errors='coerce')
                if close_values.notna().sum() >= days and close_values.iloc[0] > 0:
                    result[code] = (close_values.iloc[-1] / close_values.iloc[0] - 1.0) * 100.0
                else:
                    result[code] = default
            else:
                result[code] = default
    else:
        if len(prices_df) >= days:
            close_values = pd.to_numeric(prices_df['close'], errors='coerce')
            if close_values.notna().sum() >= days and close_values.iloc[0] > 0:
                momentum = (close_values.iloc[-1] / close_values.iloc[0] - 1.0) * 100.0
                for code in codes:
                    result[code] = momentum
            else:
                for code in codes:
                    result[code] = default
        else:
            for code in codes:
                result[code] = default
    
    return result

# ==================== 策略参数 ====================
MAX_STOCKS = {self.config.max_stocks}
SINGLE_POSITION = {self.config.single_position_max}
MIN_CASH_RATIO = {self.config.min_cash_ratio}

REBALANCE_WEEKDAY = {self.config.rebalance_weekday}

# 止损止盈
STOP_LOSS = {self.config.stop_loss}
TAKE_PROFIT = {self.config.partial_profit_1}
TAKE_PROFIT_FULL = {self.config.take_profit}
TRAILING_STOP = {self.config.trailing_stop}
TRAILING_STOP_TRIGGER = {self.config.trailing_stop_trigger}
TIME_STOP_DAYS = {self.config.time_stop_days}
PARTIAL_PROFIT_1_RATIO = {self.config.partial_profit_1_ratio}

# 市场环境判断（风险开关）
INDEX_MA_FAST = {self.config.index_ma_fast}
INDEX_MA_SLOW = {self.config.index_ma_slow}
RISK_ON_POS = {self.config.risk_on_position}
RISK_MID_POS = {self.config.risk_mid_position}
RISK_OFF_POS = {self.config.risk_off_position}

# 因子权重（已验证因子，7因子理论权重）
FACTOR_WEIGHTS = {{
    'momentum_20d': 1.0,        # 20日动量（核心）
    'rel_position': 0.9,        # 相对位置（核心）
    'market_cap': 0.85,         # 市值（核心）
    'momentum_5d': 0.75,        # 5日动量（确认）
    'turnover_rate': 0.7,       # 换手率（流动性）
    'roe': 0.5,                 # ROE（基本面底线）
    'growth': 0.4,              # 净利润增长率（成长性）
}}

# 归一化权重
TOTAL_WEIGHT = sum(FACTOR_WEIGHTS.values())
FACTOR_WEIGHTS = {{k: v / TOTAL_WEIGHT for k, v in FACTOR_WEIGHTS.items()}}

# 选股阈值
MIN_TOTAL_SCORE = {self.config.min_total_score}
MIN_MOMENTUM_20D = {self.config.min_momentum_20d}
MAX_REL_POSITION = {self.config.max_rel_position}
MIN_MARKET_CAP = {self.config.min_market_cap}
MAX_MARKET_CAP = {self.config.max_market_cap}
MIN_MOMENTUM_5D = {self.config.min_momentum_5d}
MAX_MOMENTUM_5D = {self.config.max_momentum_5d}
MIN_TURNOVER_RATE = {self.config.min_turnover_rate}
MAX_TURNOVER_RATE = {self.config.max_turnover_rate}
MIN_ROE = {self.config.min_roe}

# ==================== 缓存数据（避免重复API调用） ====================
# 注意：如果使用缓存数据，需要在回测前预加载数据到本地
# 缓存数据路径（由回测脚本注入）
CACHE_DATA_DIR = r'{cache_data_dir}'  # 默认使用空字符串，表示不使用缓存

_cached_prices = None
_cached_fundamentals_valuation = None
_cached_fundamentals_indicator = None

def load_cache_data():
    """加载缓存数据（如果可用）"""
    global _cached_prices, _cached_fundamentals_valuation, _cached_fundamentals_indicator
    
    if not CACHE_DATA_DIR or CACHE_DATA_DIR == '':
        log.info('[缓存] 未配置缓存数据目录，将使用API调用')
        return False
    
    try:
        import os
        from pathlib import Path
        
        cache_dir = Path(CACHE_DATA_DIR)
        if not cache_dir.exists():
            log.warn(f'[缓存] 缓存目录不存在: {{CACHE_DATA_DIR}}，将使用API调用')
            return False
        
        # 加载价格数据
        prices_file = cache_dir / 'daily_prices' / '2024H2_prices.parquet'
        if prices_file.exists():
            _cached_prices = pd.read_parquet(prices_file)
            log.info(f'[缓存] 价格数据已加载: {{len(_cached_prices)}} 条记录')
        
        # 加载基本面数据
        valuation_file = cache_dir / 'fundamentals' / 'valuation' / '2024H2_valuation.parquet'
        if valuation_file.exists():
            _cached_fundamentals_valuation = pd.read_parquet(valuation_file)
            log.info(f'[缓存] 估值数据已加载: {{len(_cached_fundamentals_valuation)}} 条记录')
        
        indicator_file = cache_dir / 'fundamentals' / 'indicator' / '2024H2_indicator.parquet'
        if indicator_file.exists():
            _cached_fundamentals_indicator = pd.read_parquet(indicator_file)
            log.info(f'[缓存] 财务指标已加载: {{len(_cached_fundamentals_indicator)}} 条记录')
        
        if _cached_prices is not None:
            log.info('[缓存] ✅ 缓存数据加载成功，将使用缓存数据（零Token消耗）')
            return True
        else:
            log.warn('[缓存] ⚠️  缓存数据未找到，将使用API调用')
            return False
    except Exception as e:
        log.warn(f'[缓存] 加载缓存数据失败: {{e}}，将使用API调用')
        return False

# ==================== 初始化 ====================
def initialize(context):
    """策略初始化"""
    # 基准设置
    set_benchmark('000300.XSHG')
    
    # 滑点设置（固定滑点0.1%）
    set_slippage(FixedSlippage(0.001))
    
    # 手续费设置（聚宽标准费率）
    set_order_cost(OrderCost(
        open_tax=0,              # 买入无印花税
        close_tax=0.001,         # 卖出印花税0.1%
        open_commission=0.0003,   # 买入佣金0.03%
        close_commission=0.0003, # 卖出佣金0.03%
        min_commission=5          # 最低佣金5元
    ), type='stock')
    
    # 真实价格模式（使用真实成交价）
    set_option('use_real_price', True)
    
    # 加载缓存数据（如果可用）
    use_cache = load_cache_data()
    context.use_cache = use_cache
    
    # 策略状态
    context.stock_pool = []
    context.trade_count = 0
    context.cost_prices = {{}}      # 持仓成本价
    context.highest_prices = {{}}   # 持仓最高价
    context.entry_dates = {{}}      # 持仓买入日期
    context.partial_profit_1_done = {{}}  # 是否已执行第一批止盈
    
    # 定时任务
    run_daily(before_market_open, time='09:00')
    run_weekly(market_open, weekday=REBALANCE_WEEKDAY, time='09:35')
    run_daily(check_risk, time='14:50')
    run_daily(after_market_close, time='15:30')
    
    log.info('=' * 60)
    log.info('策略初始化: TRQuant Advisor V4.0 完整因子策略（100%已验证因子）')
    log.info(f'持股: {{MAX_STOCKS}}只 | 单票仓位: {{SINGLE_POSITION*100:.0f}}%')
    log.info(f'调仓: 每周{{["一","二","三","四","五"][REBALANCE_WEEKDAY]}} | 因子: 7因子完整组合')
    log.info(f'数据源: {{"缓存数据（零Token）" if use_cache else "API调用（消耗Token）"}}')
    log.info('=' * 60)


def before_market_open(context):
    """盘前准备"""
    context.trade_count += 1
    
    # 每周更新股票池（周一）
    if context.trade_count % 5 == 1:
        # 获取沪深300成分股（必须传递当前日期，确保获取历史成分股）
        # 使用当前回测日期，确保获取正确的历史成分股
        _current_date = context.current_dt.strftime('%Y-%m-%d') if hasattr(context, 'current_dt') and context.current_dt else None
        if _current_date is None:
            log.error('[盘前] 无法获取当前日期，无法更新股票池')
            context.stock_pool = []
            return
        
        try:
            context.stock_pool = get_index_stocks('000300.XSHG', date=_current_date)
            if not context.stock_pool or len(context.stock_pool) == 0:
                log.error('[盘前] 获取指数成分股失败: 返回空列表，日期=' + str(_current_date))
                context.stock_pool = []
            else:
                log.info(f'[盘前] 更新股票池: {{len(context.stock_pool)}}只，日期=' + str(_current_date))
        except Exception as e:
            log.error('[盘前] 获取指数成分股失败: ' + str(e) + '，日期=' + str(_current_date))
            raise  # 不兜底，明确报错


def market_open(context):
    """开盘交易（调仓日）"""
    log.info(f'[调仓日] 第{{context.trade_count}}个交易日')
    
    # 1. 选股
    target_stocks = select_stocks(context)
    if not target_stocks:
        log.warn('[调仓] 未选出股票，保持当前持仓')
        return
    
    log.info(f'[调仓] 选股结果: {{len(target_stocks)}}只')
    for i, stock in enumerate(target_stocks[:5], 1):
        log.info(f'  {{i}}. {{stock}}')
    
    # 2. 调仓
    rebalance(context, target_stocks)


def select_stocks(context):
    """选股逻辑 - 完整7因子"""
    stocks = context.stock_pool
    if not stocks:
        log.warn('[选股] 股票池为空')
        return []
    
    log.info(f'[选股] 开始选股，股票池: {{len(stocks)}}只')
    current_date = context.current_dt.date()
    date_str = current_date.strftime('%Y-%m-%d')
    
    # 1. 基础过滤
    stocks = filter_basic(stocks, date_str)
    if not stocks:
        log.warn('[选股] 基础过滤后无股票')
        return []
    
    log.info(f'[选股] 基础过滤后: {{len(stocks)}}只')
    
    # 2. 计算因子
    factors_df = calculate_validated_factors(stocks, date_str)
    if factors_df is None or factors_df.empty:
        log.warn('[选股] 因子计算失败或结果为空')
        return []
    
    log.info(f'[选股] 因子计算完成: {{len(factors_df)}}只股票')
    if len(factors_df) > 0:
        log.info(f'[选股] 得分统计: min={{factors_df["total_score"].min():.1f}}, max={{factors_df["total_score"].max():.1f}}, mean={{factors_df["total_score"].mean():.1f}}')
        log.info(f'[选股] 20日动量: min={{factors_df["momentum_20d"].min():.1f}}%, max={{factors_df["momentum_20d"].max():.1f}}%')
        log.info(f'[选股] 市值: min={{factors_df["market_cap"].min():.1f}}亿, max={{factors_df["market_cap"].max():.1f}}亿')
    
    # 3. 综合得分筛选（逐步筛选，记录每步结果）
    candidates = factors_df.copy()
    initial_count = len(candidates)
    
    # 得分筛选
    before = len(candidates)
    candidates = candidates[candidates['total_score'] >= MIN_TOTAL_SCORE]
    after = len(candidates)
    log.info(f'[选股] 得分筛选 (≥{{MIN_TOTAL_SCORE}}): {{before}} → {{after}}只')
    
    # 20日动量筛选
    before = len(candidates)
    MAX_MOMENTUM_20D = {self.config.max_momentum_20d}
    candidates = candidates[
        (candidates['momentum_20d'] >= MIN_MOMENTUM_20D) &
        (candidates['momentum_20d'] <= MAX_MOMENTUM_20D)
    ]
    after = len(candidates)
    log.info(f'[选股] 20日动量筛选 ({{MIN_MOMENTUM_20D}}~{{MAX_MOMENTUM_20D}}%): {{before}} → {{after}}只')
    
    # 相对位置筛选
    before = len(candidates)
    candidates = candidates[candidates['rel_position'] <= MAX_REL_POSITION]
    after = len(candidates)
    log.info(f'[选股] 相对位置筛选 (≤{{MAX_REL_POSITION}}%): {{before}} → {{after}}只')
    
    # 市值筛选
    before = len(candidates)
    candidates = candidates[
        (candidates['market_cap'] >= MIN_MARKET_CAP) &
        (candidates['market_cap'] <= MAX_MARKET_CAP)
    ]
    after = len(candidates)
    log.info(f'[选股] 市值筛选 ({{MIN_MARKET_CAP}}~{{MAX_MARKET_CAP}}亿): {{before}} → {{after}}只')
    
    # 5日动量筛选
    before = len(candidates)
    candidates = candidates[
        (candidates['momentum_5d'] >= MIN_MOMENTUM_5D) &
        (candidates['momentum_5d'] <= MAX_MOMENTUM_5D)
    ]
    after = len(candidates)
    log.info(f'[选股] 5日动量筛选 ({{MIN_MOMENTUM_5D}}~{{MAX_MOMENTUM_5D}}%): {{before}} → {{after}}只')
    
    # 换手率筛选
    before = len(candidates)
    candidates = candidates[
        (candidates['turnover_rate'] >= MIN_TURNOVER_RATE) &
        (candidates['turnover_rate'] <= MAX_TURNOVER_RATE)
    ]
    after = len(candidates)
    log.info(f'[选股] 换手率筛选 ({{MIN_TURNOVER_RATE}}~{{MAX_TURNOVER_RATE}}%): {{before}} → {{after}}只')
    
    # ROE筛选
    before = len(candidates)
    candidates = candidates[candidates['roe'] >= MIN_ROE]
    after = len(candidates)
    log.info(f'[选股] ROE筛选 (≥{{MIN_ROE}}%): {{before}} → {{after}}只')
    
    if candidates.empty:
        log.warn(f'[选股] 无股票满足阈值条件 (初始{{initial_count}}只)')
        # 如果筛选后为空，尝试放宽条件
        log.info('[选股] 尝试放宽条件：仅按得分排序')
        candidates = factors_df.sort_values('total_score', ascending=False).head(MAX_STOCKS)
        if len(candidates) > 0:
            log.info(f'[选股] 放宽条件后选出: {{len(candidates)}}只')
        else:
            return []
    
    # 4. 排序取TOP N
    candidates = candidates.sort_values('total_score', ascending=False)
    selected = candidates.head(MAX_STOCKS)['code'].tolist()
    
    log.info(f'[选股] 最终选择: {{len(selected)}}只')
    log.info(f'[选股] 得分范围: {{candidates["total_score"].min():.1f}} ~ {{candidates["total_score"].max():.1f}}')
    
    return selected


def filter_basic(stocks, date_str):
    """基础过滤：排除ST、停牌、涨跌停"""
    if not stocks:
        log.warn('[基础过滤] 输入股票池为空')
        return []
    
    log.info(f'[基础过滤] 输入: {{len(stocks)}}只股票')
    filtered = []
    st_count = 0
    
    # 获取当前所有股票数据（聚宽API：get_current_data()不需要参数，返回dict）
    all_current_data = {{}}
    try:
        all_current_data = get_current_data()
        if not isinstance(all_current_data, dict):
            all_current_data = {{}}
    except Exception as e:
        log.warn(f'[基础过滤] 获取当前数据失败: {{e}}，仅做ST检查')
    
    for code in stocks:
        try:
            # 排除ST（通过代码名称判断）
            if 'ST' in code:
                st_count += 1
                continue
            
            # 检查停牌和涨跌停（如果get_current_data可用）
            if all_current_data and code in all_current_data:
                stock_data = all_current_data[code]
                if hasattr(stock_data, 'paused') and stock_data.paused:
                    continue
                if hasattr(stock_data, 'is_limit_up') and stock_data.is_limit_up:
                    continue
                if hasattr(stock_data, 'is_limit_down') and stock_data.is_limit_down:
                    continue
            
            filtered.append(code)
        except Exception:
            # 如果检查失败，仍然保留该股票（避免过度过滤）
            filtered.append(code)
            continue
    
    log.info(f'[基础过滤] 结果: {{len(filtered)}}只 (排除ST:{{st_count}}只)')
    return filtered


def calculate_validated_factors(codes, date_str):
    """
    计算已验证因子（7因子）
    
    优化说明：
    - 使用辅助函数处理MultiIndex列名和动量计算
    - 聚宽get_factor_values返回Z-score标准化值，不适合阈值筛选
    - 因此保留手工计算以获取原始值
    """
    if not codes:
        return None
    
    df = pd.DataFrame({{'code': codes}})
    log.info(f'[因子计算] 开始计算因子，股票数: {{len(codes)}}只，日期: {{date_str}}')
    
    # 1. 20日动量（使用优化后的辅助函数）
    try:
        prices_20 = get_price(codes, end_date=date_str, count=21, frequency='daily', fields=['close'], panel=False, fq='post')
        momentum_20d = _calculate_momentum(prices_20, codes, days=21, default=0.0)
        df['momentum_20d'] = df['code'].map(momentum_20d).fillna(0.0)
    except Exception as e:
        log.warn(f'[因子计算] 20日动量计算失败: {{e}}')
        df['momentum_20d'] = 0.0
    
    # 2. 相对位置（使用优化后的辅助函数）
    try:
        prices_pos = get_price(codes, end_date=date_str, count=21, frequency='daily', fields=['high', 'low', 'close'], panel=False, fq='post')
        prices_pos = _flatten_multiindex_columns(prices_pos)
        
        rel_position = {{}}
        if prices_pos is not None and not prices_pos.empty:
            has_code_col = 'code' in prices_pos.columns
            
            if has_code_col:
                for code in codes:
                    code_data = prices_pos[prices_pos['code'] == code]
                    if len(code_data) >= 20:
                        high_vals = pd.to_numeric(code_data['high'], errors='coerce')
                        low_vals = pd.to_numeric(code_data['low'], errors='coerce')
                        close_vals = pd.to_numeric(code_data['close'], errors='coerce')
                        high_20 = high_vals.tail(20).max()
                        low_20 = low_vals.tail(20).min()
                        close = close_vals.iloc[-1] if not close_vals.empty else 0.0
                        if high_20 > low_20 and pd.notna(close) and close > 0:
                            rel_position[code] = (close - low_20) / (high_20 - low_20) * 100.0
                        else:
                            rel_position[code] = 50.0
                    else:
                        rel_position[code] = 50.0
            else:
                # 单只股票fallback
                if len(prices_pos) >= 20:
                    high_vals = pd.to_numeric(prices_pos['high'], errors='coerce')
                    low_vals = pd.to_numeric(prices_pos['low'], errors='coerce')
                    close_vals = pd.to_numeric(prices_pos['close'], errors='coerce')
                    high_20 = high_vals.tail(20).max()
                    low_20 = low_vals.tail(20).min()
                    close = close_vals.iloc[-1]
                    rel_pos_val = (close - low_20) / (high_20 - low_20) * 100.0 if high_20 > low_20 else 50.0
                    for code in codes:
                        rel_position[code] = rel_pos_val
                else:
                    for code in codes:
                        rel_position[code] = 50.0
        
        df['rel_position'] = df['code'].map(rel_position).fillna(50.0)
    except Exception as e:
        log.warn(f'[因子计算] 相对位置计算失败: {{e}}')
        df['rel_position'] = 50.0
    
    # 3. 市值（从jqdatasdk获取）
    # 注意：JQData返回的market_cap单位已经是亿元，不需要再转换
    try:
        q = query(valuation.code, valuation.market_cap).filter(valuation.code.in_(codes))
        fund_df = get_fundamentals(q, date=date_str)
        if fund_df is not None and not fund_df.empty:
            log.info(f'[因子计算] 市值数据获取成功: {{len(fund_df)}}只股票')
            # JQData的market_cap单位是亿元，直接使用
            df['market_cap'] = df['code'].map(dict(zip(fund_df['code'], fund_df['market_cap']))).fillna(0.0)
            log.info(f'[因子计算] 市值范围: {{df["market_cap"].min():.1f}}亿 ~ {{df["market_cap"].max():.1f}}亿')
        else:
            log.warn('[因子计算] 市值数据为空')
            df['market_cap'] = 0.0
    except Exception as e:
        log.warn(f'[因子计算] 市值获取失败: {{e}}')
        df['market_cap'] = 0.0
    
    # 4. 5日动量（使用优化后的辅助函数）
    try:
        prices_5 = get_price(codes, end_date=date_str, count=6, frequency='daily', fields=['close'], panel=False, fq='post')
        momentum_5d = _calculate_momentum(prices_5, codes, days=6, default=0.0)
        df['momentum_5d'] = df['code'].map(momentum_5d).fillna(0.0)
    except Exception as e:
        log.warn(f'[因子计算] 5日动量计算失败: {{e}}')
        df['momentum_5d'] = 0.0
    
    # 5. 换手率（从valuation表获取）
    try:
        q = query(valuation.code, valuation.turnover_ratio).filter(valuation.code.in_(codes))
        fund_df = get_fundamentals(q, date=date_str)
        if fund_df is not None and not fund_df.empty:
            turnover_dict = dict(zip(fund_df['code'], fund_df['turnover_ratio']))
            df['turnover_rate'] = df['code'].map(turnover_dict).fillna(0.0)
        else:
            df['turnover_rate'] = 0.0
    except Exception as e:
        log.warn(f'[因子计算] 换手率计算失败: {{e}}')
        df['turnover_rate'] = 0.0
    
    # 6. ROE（从indicator表获取）
    try:
        q = query(indicator.code, indicator.roe).filter(indicator.code.in_(codes))
        fund_df = get_fundamentals(q, date=date_str)
        if fund_df is not None and not fund_df.empty:
            roe_dict = dict(zip(fund_df['code'], fund_df['roe']))
            df['roe'] = df['code'].map(roe_dict).fillna(0.0)
        else:
            df['roe'] = 0.0
    except Exception as e:
        log.warn(f'[因子计算] ROE计算失败: {{e}}')
        df['roe'] = 0.0
    
    # 7. 净利润增长率（从indicator表获取）
    try:
        q = query(indicator.code, indicator.inc_net_profit_year_on_year).filter(indicator.code.in_(codes))
        fund_df = get_fundamentals(q, date=date_str)
        if fund_df is not None and not fund_df.empty:
            growth_dict = dict(zip(fund_df['code'], fund_df['inc_net_profit_year_on_year']))
            df['growth'] = df['code'].map(growth_dict).fillna(0.0)
        else:
            df['growth'] = 0.0
    except Exception as e:
        log.warn(f'[因子计算] 净利润增长率计算失败: {{e}}')
        df['growth'] = 0.0
    
    # 计算因子得分（基于理论假设的最优区间）
    df = calculate_factor_scores(df)
    
    # 计算综合得分
    df['total_score'] = (
        df['momentum_20d_score'] * FACTOR_WEIGHTS['momentum_20d'] +
        df['rel_position_score'] * FACTOR_WEIGHTS['rel_position'] +
        df['market_cap_score'] * FACTOR_WEIGHTS['market_cap'] +
        df['momentum_5d_score'] * FACTOR_WEIGHTS['momentum_5d'] +
        df['turnover_rate_score'] * FACTOR_WEIGHTS['turnover_rate'] +
        df['roe_score'] * FACTOR_WEIGHTS['roe'] +
        df['growth_score'] * FACTOR_WEIGHTS['growth']
    ) * 100
    
    return df


def calculate_factor_scores(df):
    """计算因子得分（基于理论假设的最优区间，与ValidatedFactorCalculator保持一致）"""
    import numpy as np
    
    # 1. 20日动量得分（5%~30%最优，中心值17.5%）
    def score_momentum_20d(x):
        if pd.isna(x):
            return 0.0
        if 5.0 <= x <= 30.0:
            center = 17.5
            distance = abs(x - center)
            return max(0.0, 1.0 - distance / 12.5)
        elif x < 5.0:
            return max(0.0, x / 5.0 * 0.5)
        else:
            return max(0.0, 1.0 - (x - 30.0) / 20.0)
    df['momentum_20d_score'] = df['momentum_20d'].apply(score_momentum_20d)
    
    # 2. 相对位置得分（<80%最优，<30%满分）
    def score_rel_position(x):
        if pd.isna(x):
            return 0.5
        if x <= 30.0:
            return 1.0
        elif x <= 80.0:
            return 1.0 - (x - 30.0) / 50.0 * 0.3
        else:
            return max(0.0, 1.0 - (x - 80.0) / 20.0)
    df['rel_position_score'] = df['rel_position'].apply(score_rel_position)
    
    # 3. 市值得分（30~200亿最优，中心值115亿）
    def score_market_cap(x):
        if pd.isna(x) or x <= 0:
            return 0.0
        if 30.0 <= x <= 200.0:
            center = 115.0
            distance = abs(x - center)
            return max(0.0, 1.0 - distance / 85.0)
        elif x < 30.0:
            return max(0.0, x / 30.0 * 0.7)
        else:
            return max(0.0, 1.0 - (x - 200.0) / 300.0)
    df['market_cap_score'] = df['market_cap'].apply(score_market_cap)
    
    # 4. 5日动量得分（-5%~10%最优，中心值2.5%）
    def score_momentum_5d(x):
        if pd.isna(x):
            return 0.5
        if -5.0 <= x <= 10.0:
            center = 2.5
            distance = abs(x - center)
            return max(0.0, 1.0 - distance / 7.5)
        elif x < -5.0:
            return max(0.0, (x + 10.0) / 5.0 * 0.5)
        else:
            return max(0.0, 1.0 - (x - 10.0) / 15.0)
    df['momentum_5d_score'] = df['momentum_5d'].apply(score_momentum_5d)
    
    # 5. 换手率得分（2%~10%最优）
    def score_turnover_rate(x):
        if pd.isna(x) or x <= 0:
            return 0.0
        if 2.0 <= x <= 10.0:
            return 1.0
        elif x < 2.0:
            return x / 2.0 * 0.7
        else:
            return max(0.0, 1.0 - (x - 10.0) / 20.0)
    df['turnover_rate_score'] = df['turnover_rate'].apply(score_turnover_rate)
    
    # 6. ROE得分（>0最优，最高10%ROE得满分）
    def score_roe(x):
        if pd.isna(x):
            return 0.0
        if x > 0:
            return min(1.0, x / 10.0)
        else:
            return 0.0
    df['roe_score'] = df['roe'].apply(score_roe)
    
    # 7. 净利润增长率得分（>0最优，最高100%增长得满分）
    def score_growth(x):
        if pd.isna(x):
            return 0.0
        if x > 0:
            return min(1.0, x / 100.0)
        else:
            return 0.0
    df['growth_score'] = df['growth'].apply(score_growth)
    
    return df


def rebalance(context, target_stocks):
    """调仓逻辑"""
    current_positions = list(context.portfolio.positions.keys())
    current_positions = [s for s in current_positions if s in context.stock_pool]
    
    # 1. 卖出不在目标列表的股票
    for stock in current_positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)
            log.info(f'[调仓] 卖出: {{stock}}')
            # 清理记录
            context.cost_prices.pop(stock, None)
            context.highest_prices.pop(stock, None)
            context.entry_dates.pop(stock, None)
            context.partial_profit_1_done.pop(stock, None)
    
    # 2. 计算目标仓位（等权）
    total_value = context.portfolio.total_value
    cash_available = context.portfolio.available_cash
    target_value_per_stock = (total_value * (1 - MIN_CASH_RATIO)) / len(target_stocks)
    target_value_per_stock = min(target_value_per_stock, total_value * SINGLE_POSITION)
    
    # 3. 买入目标股票
    for stock in target_stocks:
        # 安全获取当前持仓价值（BulletTrade Position对象使用value或market_value）
        if stock in context.portfolio.positions:
            position = context.portfolio.positions[stock]
            if hasattr(position, 'value'):
                current_value = position.value
            elif hasattr(position, 'market_value'):
                current_value = position.market_value
            elif hasattr(position, 'total_amount') and hasattr(position, 'last_price'):
                current_value = position.total_amount * position.last_price
            else:
                current_value = 0.0
        else:
            current_value = 0.0
        
        target_value = target_value_per_stock
        
        if target_value > current_value * 1.1:  # 允许10%误差
            order_target_value(stock, target_value)
            log.info(f'[调仓] 买入: {{stock}} | 目标价值: {{target_value:.0f}}')
            
            # 记录成本价和买入日期
            if stock not in context.cost_prices:
                try:
                    current_data = get_current_data()
                    if stock in current_data:
                        context.cost_prices[stock] = current_data[stock].last_price
                        context.highest_prices[stock] = context.cost_prices[stock]
                        context.entry_dates[stock] = context.current_dt.date()
                        context.partial_profit_1_done[stock] = False
                except Exception as e:
                    log.warn(f'[调仓] 记录成本价失败: {{stock}}, {{e}}')


def check_risk(context):
    """风控检查（盘中）"""
    current_date = context.current_dt.date()
    
    for stock in list(context.portfolio.positions.keys()):
        if stock not in context.stock_pool:
            continue
        
        position = context.portfolio.positions[stock]
        if position.total_amount == 0:
            continue
        
        current_price = get_current_data()[stock].last_price
        cost_price = position.avg_cost
        
        if cost_price <= 0:
            continue
        
        # 更新最高价
        if stock not in context.highest_prices:
            context.highest_prices[stock] = current_price
        else:
            context.highest_prices[stock] = max(context.highest_prices[stock], current_price)
        
        # 1. 固定止损
        pnl_rate = (current_price / cost_price - 1.0)
        if pnl_rate <= STOP_LOSS:
            order_target_value(stock, 0)
            log.warn(f'[风控] 止损: {{stock}} | 亏损: {{pnl_rate:.2%}}')
            context.cost_prices.pop(stock, None)
            context.highest_prices.pop(stock, None)
            context.entry_dates.pop(stock, None)
            context.partial_profit_1_done.pop(stock, None)
            continue
        
        # 2. 第一批止盈（+20%，减仓50%）
        if pnl_rate >= TAKE_PROFIT and not context.partial_profit_1_done.get(stock, False):
            # BulletTrade Position对象使用value或market_value
            if hasattr(position, 'value'):
                current_value = position.value
            elif hasattr(position, 'market_value'):
                current_value = position.market_value
            elif hasattr(position, 'total_amount') and hasattr(position, 'last_price'):
                current_value = position.total_amount * position.last_price
            else:
                current_value = 0.0
            target_value = current_value * (1 - PARTIAL_PROFIT_1_RATIO)
            order_target_value(stock, target_value)
            log.info(f'[风控] 第一批止盈: {{stock}} | 盈利: {{pnl_rate:.2%}}，减仓{{PARTIAL_PROFIT_1_RATIO:.0%}}')
            context.partial_profit_1_done[stock] = True
            continue
        
        # 3. 第二批止盈（+30%，全部平仓）
        if pnl_rate >= TAKE_PROFIT_FULL:
            order_target_value(stock, 0)
            log.info(f'[风控] 第二批止盈: {{stock}} | 盈利: {{pnl_rate:.2%}}，全部平仓')
            context.cost_prices.pop(stock, None)
            context.highest_prices.pop(stock, None)
            context.entry_dates.pop(stock, None)
            context.partial_profit_1_done.pop(stock, None)
            continue
        
        # 4. 移动止损（达到一定盈利后）
        if pnl_rate >= TRAILING_STOP_TRIGGER:
            highest_price = context.highest_prices[stock]
            trailing_pnl_rate = (current_price / highest_price - 1.0)
            if trailing_pnl_rate <= TRAILING_STOP:
                order_target_value(stock, 0)
                log.warn(f'[风控] 移动止损: {{stock}} | 回撤: {{trailing_pnl_rate:.2%}}')
                context.cost_prices.pop(stock, None)
                context.highest_prices.pop(stock, None)
                context.entry_dates.pop(stock, None)
                context.partial_profit_1_done.pop(stock, None)
                continue
        
        # 5. 时间止损
        if stock in context.entry_dates:
            days_held = (current_date - context.entry_dates[stock]).days
            if days_held >= TIME_STOP_DAYS:
                order_target_value(stock, 0)
                log.info(f'[风控] 时间止损: {{stock}} | 持仓: {{days_held}}天')
                context.cost_prices.pop(stock, None)
                context.highest_prices.pop(stock, None)
                context.entry_dates.pop(stock, None)
                context.partial_profit_1_done.pop(stock, None)
                continue


def after_market_close(context):
    """盘后处理"""
    # 清理无效持仓记录
    for stock in list(context.cost_prices.keys()):
        if context.portfolio.positions[stock].total_amount == 0:
            context.cost_prices.pop(stock, None)
            context.highest_prices.pop(stock, None)
            context.entry_dates.pop(stock, None)
            context.partial_profit_1_done.pop(stock, None)
'''
        return code
    
    def save_strategy_code(self, output_path: str, cache_data_dir: Optional[str] = None):
        """
        保存策略代码到文件
        
        Args:
            output_path: 输出文件路径
            cache_data_dir: 缓存数据目录路径
        """
        code = self.generate_strategy_code(cache_data_dir=cache_data_dir)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
        logger.info(f"策略代码已保存: {output_path}")
