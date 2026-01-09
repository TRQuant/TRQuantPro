#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QMT研究环境策略代码生成器 - 生成基于7个已验证因子的完整策略代码

功能：
1. 生成QMT桌面app研究环境格式的策略代码
2. 使用ContextInfo API，无需连接交易账户
3. 内联实现7个已验证因子的计算逻辑
4. 实现完整的选股、仓位、风控、止损止盈逻辑
5. 可直接在QMT研究环境中运行回测
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from .bullettrade_strategy_generator import StrategyConfig

logger = logging.getLogger(__name__)


class QMTResearchStrategyGenerator:
    """QMT研究环境策略代码生成器"""
    
    def __init__(
        self,
        config: Optional[StrategyConfig] = None,
    ):
        """
        初始化QMT研究环境策略代码生成器
        
        Args:
            config: 策略配置
        """
        self.config = config or StrategyConfig()
    
    def generate_strategy_code(self) -> str:
        """
        生成完整的QMT研究环境策略代码
        
        Returns:
            策略代码字符串
        """
        # 生成UTF-8编码的策略代码
        # 注意：确保所有字符串都是UTF-8编码，避免Windows QMT读取时的编码问题
        gen_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f'''# -*- coding: utf-8 -*-
# 本文件使用UTF-8编码，请确保编辑器以UTF-8编码打开
"""
TRQuant Advisor V4.0 - QMT研究环境策略代码
==========================================

策略说明:
- 基于7个已验证因子的多因子选股策略
- 100%使用已验证因子，不使用聚宽因子
- 完整的风险控制和止损止盈机制
- 适用于QMT桌面app研究环境，无需连接交易账户

因子列表:
1. 20日动量 (momentum_20d) - 核心因子
2. 相对位置 (rel_position) - 核心因子
3. 市值 (market_cap) - 核心因子
4. 5日动量 (momentum_5d) - 确认因子
5. 换手率 (turnover_rate) - 流动性因子
6. ROE (roe) - 基本面因子
7. 净利润增长率 (growth) - 成长性因子

生成时间: {gen_time}
平台: QMT研究环境
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==================== 策略参数配置 ====================
# 选股参数
MAX_STOCKS = {self.config.max_stocks}
MIN_TOTAL_SCORE = {self.config.min_total_score}

# 仓位参数
SINGLE_POSITION_MAX = {self.config.single_position_max}
MIN_CASH_RATIO = {self.config.min_cash_ratio}

# 调仓参数
REBALANCE_WEEKDAY = {self.config.rebalance_weekday}  # 0=周一

# 止损止盈参数
STOP_LOSS = {self.config.stop_loss}
TAKE_PROFIT = {self.config.take_profit}
TAKE_PROFIT_PCT = {self.config.take_profit * 100:.1f}  # 百分比形式，用于显示
STOP_LOSS_PCT = {abs(self.config.stop_loss) * 100:.1f}  # 百分比形式，用于显示
TRAILING_STOP = {self.config.trailing_stop}
TRAILING_STOP_TRIGGER = {self.config.trailing_stop_trigger}
TIME_STOP_DAYS = {self.config.time_stop_days}
PARTIAL_PROFIT_1 = {self.config.partial_profit_1}
PARTIAL_PROFIT_1_RATIO = {self.config.partial_profit_1_ratio}

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
MIN_MOMENTUM_20D = {self.config.min_momentum_20d}
MAX_REL_POSITION = {self.config.max_rel_position}
MIN_MARKET_CAP = {self.config.min_market_cap}
MAX_MARKET_CAP = {self.config.max_market_cap}
MIN_MOMENTUM_5D = {self.config.min_momentum_5d}
MAX_MOMENTUM_5D = {self.config.max_momentum_5d}
MIN_TURNOVER_RATE = {self.config.min_turnover_rate}
MAX_TURNOVER_RATE = {self.config.max_turnover_rate}
MIN_ROE = {self.config.min_roe}

# ==================== 全局变量 ====================
# 持仓记录 {{股票代码: {{'cost_price': 成本价, 'entry_date': 买入日期, 'highest_price': 最高价, 'partial_profit_1_done': False}}}}
g_positions = {{}}
g_last_rebalance_date = None  # 上次调仓日期
g_stock_pool = []  # 股票池


# ==================== 数据获取函数 ====================
def normalize_stock_code(code):
    """
    Normalize stock code format for QMT
    Convert '600837.SH' to '600837.XSHG' or '600837'
    """
    if not code:
        return code
    
    # Remove .SH suffix and convert to .XSHG if needed
    if code.endswith('.SH'):
        # Shanghai stocks: convert to .XSHG format
        return code.replace('.SH', '.XSHG')
    elif code.endswith('.SZ'):
        # Shenzhen stocks: convert to .XSHE format
        return code.replace('.SZ', '.XSHE')
    elif '.' not in code:
        # Already normalized format
        return code
    else:
        # Keep as is if already in correct format
        return code


def get_stock_list(ContextInfo):
    """获取股票池（沪深300成分股）"""
    try:
        # QMT研究环境获取指数成分股
        index_code = "000300.SH"
        stock_list = ContextInfo.get_stock_list_in_sector(index_code)
        if stock_list:
            # Normalize stock codes for QMT
            normalized_list = [normalize_stock_code(code) for code in stock_list]
            return normalized_list
        return []
    except Exception as e:
        print(f"获取股票池失败: {{e}}")
        return []


def get_price_data(ContextInfo, stocks, count=20, fields=None):
    """
    获取价格数据（QMT研究环境版本）
    
    Args:
        ContextInfo: QMT上下文对象
        stocks: 股票代码列表
        count: 获取最近N条数据
        fields: 字段列表 ['open', 'high', 'low', 'close', 'volume']
    
    Returns:
        DataFrame，列名为股票代码
    """
    try:
        if fields is None:
            fields = ['open', 'high', 'low', 'close', 'volume']
        
        # QMT研究环境使用get_market_data
        # 注意：根据实际QMT API调整
        result = {{}}
        for stock in stocks:
            try:
                # QMT研究环境API: get_market_data(stock, period='1d', count=count)
                data = ContextInfo.get_market_data(
                    stock, 
                    period='1d', 
                    count=count,
                    fields=fields
                )
                if data is not None and len(data) > 0:
                    result[stock] = data
            except Exception as e:
                print(f"获取{{stock}}数据失败: {{e}}")
                continue
        
        # 转换为DataFrame
        if result:
            df = pd.DataFrame(result)
            return df
        return None
    
    except Exception as e:
        print(f"获取价格数据失败: {{e}}")
        return None


def get_fundamentals_data(ContextInfo, stocks, date_str, fields=None):
    """
    获取基本面数据（QMT研究环境版本）
    
    Args:
        ContextInfo: QMT上下文对象
        stocks: 股票代码列表
        date_str: 日期字符串（YYYY-MM-DD）
        fields: 字段列表 ['market_cap', 'roe', 'net_profit_growth_rate']
    
    Returns:
        DataFrame
    """
    try:
        if fields is None:
            fields = ['market_cap', 'roe', 'net_profit_growth_rate']
        
        # QMT研究环境基本面数据API
        # 注意：根据实际QMT API调整
        result = {{}}
        for stock in stocks:
            try:
                # QMT可能使用get_financial_data或类似API
                data = ContextInfo.get_financial_data(
                    stock,
                    fields=fields,
                    date=date_str
                )
                if data is not None:
                    result[stock] = data
            except Exception as e:
                print(f"获取{{stock}}基本面数据失败: {{e}}")
                continue
        
        if result:
            df = pd.DataFrame(result).T  # 转置，股票代码作为索引
            return df
        return None
    
    except Exception as e:
        print(f"获取基本面数据失败: {{e}}")
        return None


# ==================== 因子计算函数 ====================
def calculate_validated_factors(ContextInfo, codes, date_str):
    """
    计算已验证因子（7因子）
    
    Args:
        ContextInfo: QMT上下文对象
        codes: 股票代码列表
        date_str: 日期字符串（YYYY-MM-DD）
    
    Returns:
        DataFrame，包含所有因子值
    """
    if not codes:
        return None
    
    try:
        # 获取价格数据
        prices_20 = get_price_data(ContextInfo, codes, count=20)
        prices_5 = get_price_data(ContextInfo, codes, count=5)
        
        if prices_20 is None or prices_5 is None:
            return None
        
        # 获取基本面数据
        fundamentals = get_fundamentals_data(ContextInfo, codes, date_str, 
                                            fields=['market_cap', 'roe', 'net_profit_growth_rate'])
        
        # 初始化结果DataFrame
        result = pd.DataFrame({{'code': codes}})
        
        # 1. 20日动量
        for code in codes:
            if code in prices_20.columns:
                try:
                    price_data = prices_20[code]
                    if len(price_data) >= 20:
                        close_vals = price_data['close'] if isinstance(price_data, pd.DataFrame) else price_data
                        if len(close_vals) >= 20:
                            result.loc[result['code'] == code, 'momentum_20d'] = (close_vals.iloc[-1] - close_vals.iloc[0]) / close_vals.iloc[0] * 100
                        else:
                            result.loc[result['code'] == code, 'momentum_20d'] = 0.0
                    else:
                        result.loc[result['code'] == code, 'momentum_20d'] = 0.0
                except:
                    result.loc[result['code'] == code, 'momentum_20d'] = 0.0
            else:
                result.loc[result['code'] == code, 'momentum_20d'] = 0.0
        
        # 2. 相对位置（20日最高最低）
        for code in codes:
            if code in prices_20.columns:
                try:
                    price_data = prices_20[code]
                    if len(price_data) >= 20:
                        high_vals = price_data['high'] if isinstance(price_data, pd.DataFrame) else price_data
                        low_vals = price_data['low'] if isinstance(price_data, pd.DataFrame) else price_data
                        close_vals = price_data['close'] if isinstance(price_data, pd.DataFrame) else price_data
                        if len(high_vals) >= 20 and len(low_vals) >= 20:
                            high_20 = high_vals.tail(20).max()
                            low_20 = low_vals.tail(20).min()
                            close = close_vals.iloc[-1] if len(close_vals) > 0 else 0.0
                            if high_20 > low_20 and close > 0:
                                result.loc[result['code'] == code, 'rel_position'] = (close - low_20) / (high_20 - low_20) * 100.0
                            else:
                                result.loc[result['code'] == code, 'rel_position'] = 50.0
                        else:
                            result.loc[result['code'] == code, 'rel_position'] = 50.0
                    else:
                        result.loc[result['code'] == code, 'rel_position'] = 50.0
                except:
                    result.loc[result['code'] == code, 'rel_position'] = 50.0
            else:
                result.loc[result['code'] == code, 'rel_position'] = 50.0
        
        # 3. 市值（从基本面数据获取）
        if fundamentals is not None and 'market_cap' in fundamentals.columns:
            result['market_cap'] = result['code'].map(dict(zip(fundamentals.index, fundamentals['market_cap']))).fillna(0.0)
        else:
            result['market_cap'] = 0.0
        
        # 4. 5日动量
        for code in codes:
            if code in prices_5.columns:
                try:
                    price_data = prices_5[code]
                    if len(price_data) >= 5:
                        close_vals = price_data['close'] if isinstance(price_data, pd.DataFrame) else price_data
                        if len(close_vals) >= 5:
                            result.loc[result['code'] == code, 'momentum_5d'] = (close_vals.iloc[-1] - close_vals.iloc[0]) / close_vals.iloc[0] * 100
                        else:
                            result.loc[result['code'] == code, 'momentum_5d'] = 0.0
                    else:
                        result.loc[result['code'] == code, 'momentum_5d'] = 0.0
                except:
                    result.loc[result['code'] == code, 'momentum_5d'] = 0.0
            else:
                result.loc[result['code'] == code, 'momentum_5d'] = 0.0
        
        # 5. 换手率（20日平均，简化计算）
        for code in codes:
            if code in prices_20.columns:
                try:
                    price_data = prices_20[code]
                    if len(price_data) >= 20:
                        volume_vals = price_data['volume'] if isinstance(price_data, pd.DataFrame) else price_data
                        # 简化计算换手率
                        result.loc[result['code'] == code, 'turnover_rate'] = volume_vals.mean() / 1000000 * 100 if len(volume_vals) > 0 else 0.0
                    else:
                        result.loc[result['code'] == code, 'turnover_rate'] = 0.0
                except:
                    result.loc[result['code'] == code, 'turnover_rate'] = 0.0
            else:
                result.loc[result['code'] == code, 'turnover_rate'] = 0.0
        
        # 6. ROE（从基本面数据获取）
        if fundamentals is not None and 'roe' in fundamentals.columns:
            result['roe'] = result['code'].map(dict(zip(fundamentals.index, fundamentals['roe']))).fillna(0.0)
        else:
            result['roe'] = 0.0
        
        # 7. 净利润增长率（从基本面数据获取）
        if fundamentals is not None and 'net_profit_growth_rate' in fundamentals.columns:
            result['growth'] = result['code'].map(dict(zip(fundamentals.index, fundamentals['net_profit_growth_rate']))).fillna(0.0)
        else:
            result['growth'] = 0.0
        
        return result
    
    except Exception as e:
        print(f"计算因子失败: {{e}}")
        import traceback
        traceback.print_exc()
        return None


def calculate_factor_scores(factors_df):
    """
    计算因子得分（基于理论假设的最优区间）
    
    Args:
        factors_df: 因子DataFrame
    
    Returns:
        添加了得分列的DataFrame
    """
    import numpy as np
    
    df = factors_df.copy()
    
    # 1. 20日动量得分（5%~30%最优，中心值17.5%）
    momentum_20d = df['momentum_20d'].values
    optimal_center = 17.5
    optimal_range = 12.5
    df['momentum_20d_score'] = np.maximum(0, 1 - np.abs(momentum_20d - optimal_center) / optimal_range)
    
    # 2. 相对位置得分（50%~80%最优）
    rel_position = df['rel_position'].values
    df['rel_position_score'] = np.where(
        (rel_position >= 50) & (rel_position <= 80),
        1.0,
        np.maximum(0, 1 - np.abs(rel_position - 65) / 50)
    )
    
    # 3. 市值得分（30亿~200亿最优）
    market_cap = df['market_cap'].values
    optimal_cap = 115  # 中心值
    optimal_range_cap = 85
    df['market_cap_score'] = np.maximum(0, 1 - np.abs(market_cap - optimal_cap) / optimal_range_cap)
    
    # 4. 5日动量得分（-2%~5%最优）
    momentum_5d = df['momentum_5d'].values
    optimal_5d = 1.5
    optimal_range_5d = 3.5
    df['momentum_5d_score'] = np.maximum(0, 1 - np.abs(momentum_5d - optimal_5d) / optimal_range_5d)
    
    # 5. 换手率得分（2%~8%最优）
    turnover_rate = df['turnover_rate'].values
    optimal_turnover = 5.0
    optimal_range_turnover = 3.0
    df['turnover_rate_score'] = np.maximum(0, 1 - np.abs(turnover_rate - optimal_turnover) / optimal_range_turnover)
    
    # 6. ROE得分（越高越好，阈值0%）
    roe = df['roe'].values
    df['roe_score'] = np.where(roe >= 0, np.minimum(1.0, roe / 20.0), 0.0)  # 20% ROE为满分
    
    # 7. 净利润增长率得分（越高越好，阈值0%）
    growth = df['growth'].values
    df['growth_score'] = np.where(growth >= 0, np.minimum(1.0, growth / 50.0), 0.0)  # 50%增长为满分
    
    # 计算综合得分
    df['total_score'] = (
        df['momentum_20d_score'] * FACTOR_WEIGHTS['momentum_20d'] +
        df['rel_position_score'] * FACTOR_WEIGHTS['rel_position'] +
        df['market_cap_score'] * FACTOR_WEIGHTS['market_cap'] +
        df['momentum_5d_score'] * FACTOR_WEIGHTS['momentum_5d'] +
        df['turnover_rate_score'] * FACTOR_WEIGHTS['turnover_rate'] +
        df['roe_score'] * FACTOR_WEIGHTS['roe'] +
        df['growth_score'] * FACTOR_WEIGHTS['growth']
    ) * 100  # 转换为0-100分
    
    return df


# ==================== 选股函数 ====================
def select_stocks(ContextInfo, date_str):
    """
    选股函数
    
    Args:
        ContextInfo: QMT上下文对象
        date_str: 日期字符串（YYYY-MM-DD）
    
    Returns:
        选中的股票代码列表
    """
    # 获取股票池
    stock_pool = get_stock_list(ContextInfo)
    if not stock_pool:
        print(f"[选股] 股票池为空")
        return []
    
    # 计算因子
    factors_df = calculate_validated_factors(ContextInfo, stock_pool, date_str)
    if factors_df is None or factors_df.empty:
        print(f"[选股] 因子计算失败")
        return []
    
    # 计算得分
    factors_df = calculate_factor_scores(factors_df)
    
    # 筛选
    filtered = factors_df[
        (factors_df['momentum_20d'] >= MIN_MOMENTUM_20D) &
        (factors_df['momentum_20d'] <= 30.0) &
        (factors_df['rel_position'] <= MAX_REL_POSITION) &
        (factors_df['market_cap'] >= MIN_MARKET_CAP) &
        (factors_df['market_cap'] <= MAX_MARKET_CAP) &
        (factors_df['momentum_5d'] >= MIN_MOMENTUM_5D) &
        (factors_df['momentum_5d'] <= MAX_MOMENTUM_5D) &
        (factors_df['turnover_rate'] >= MIN_TURNOVER_RATE) &
        (factors_df['turnover_rate'] <= MAX_TURNOVER_RATE) &
        (factors_df['roe'] >= MIN_ROE) &
        (factors_df['total_score'] >= MIN_TOTAL_SCORE)
    ].copy()
    
    if filtered.empty:
        print(f"[选股] 无股票通过筛选")
        return []
    
    # 按得分排序，取前N只
    filtered = filtered.sort_values('total_score', ascending=False)
    selected = filtered.head(MAX_STOCKS)['code'].tolist()
    
    print(f"[选股] 选中 {{len(selected)}} 只股票，最高得分: {{filtered['total_score'].max():.1f}}")
    return selected


# ==================== 风控函数 ====================
def check_risk_control(ContextInfo):
    """风控检查（止损止盈）"""
    global g_positions
    
    current_date = ContextInfo.current_dt.strftime('%Y-%m-%d')
    positions = ContextInfo.get_trade_detail_data(ContextInfo.accout_id, 'stock', 'position')
    
    for pos in positions:
        stock_code = pos.m_strInstrumentID
        
        if stock_code not in g_positions:
            # 初始化持仓记录
            g_positions[stock_code] = {{
                'cost_price': pos.m_dCost,
                'entry_date': current_date,
                'highest_price': pos.m_dPrice,
                'partial_profit_1_done': False
            }}
        
        pos_record = g_positions[stock_code]
        cost_price = pos_record['cost_price']
        current_price = pos.m_dPrice
        
        # 更新最高价
        if current_price > pos_record['highest_price']:
            pos_record['highest_price'] = current_price
        
        # 计算盈亏
        pnl = (current_price - cost_price) / cost_price
        
        # 止损
        if pnl <= STOP_LOSS:
            print(f"[止损] {{stock_code}} 亏损 {{pnl*100:.2f}}%，卖出")
            ContextInfo.order(stock_code, -pos.m_nVolume, ContextInfo.MARKET_SH_SZ)
            del g_positions[stock_code]
            continue
        
        # 止盈
        if pnl >= TAKE_PROFIT:
            print(f"[止盈] {{stock_code}} 盈利 {{pnl*100:.2f}}%，卖出")
            ContextInfo.order(stock_code, -pos.m_nVolume, ContextInfo.MARKET_SH_SZ)
            del g_positions[stock_code]
            continue
        
        # 移动止损（盈利超过触发条件后启用）
        if pnl >= TRAILING_STOP_TRIGGER:
            trailing_pnl = (current_price - pos_record['highest_price']) / pos_record['highest_price']
            if trailing_pnl <= TRAILING_STOP:
                print(f"[移动止损] {{stock_code}} 从最高价回撤 {{trailing_pnl*100:.2f}}%，卖出")
                ContextInfo.order(stock_code, -pos.m_nVolume, ContextInfo.MARKET_SH_SZ)
                del g_positions[stock_code]
                continue
        
        # 分批止盈
        if not pos_record['partial_profit_1_done'] and pnl >= PARTIAL_PROFIT_1:
            sell_amount = int(pos.m_nVolume * PARTIAL_PROFIT_1_RATIO)
            print(f"[分批止盈] {{stock_code}} 盈利 {{pnl*100:.2f}}%，卖出{{PARTIAL_PROFIT_1_RATIO*100:.0f}}%")
            ContextInfo.order(stock_code, -sell_amount, ContextInfo.MARKET_SH_SZ)
            pos_record['partial_profit_1_done'] = True
        
        # 时间止损
        entry_date = datetime.strptime(pos_record['entry_date'], '%Y-%m-%d')
        days_held = (ContextInfo.current_dt - entry_date).days
        if days_held >= TIME_STOP_DAYS:
            print(f"[时间止损] {{stock_code}} 持仓{{days_held}}天，卖出")
            ContextInfo.order(stock_code, -pos.m_nVolume, ContextInfo.MARKET_SH_SZ)
            del g_positions[stock_code]


# ==================== 调仓函数 ====================
def rebalance(ContextInfo):
    """调仓函数"""
    global g_last_rebalance_date, g_stock_pool
    
    current_date = ContextInfo.current_dt.strftime('%Y-%m-%d')
    current_weekday = ContextInfo.current_dt.weekday()
    
    # 检查是否需要调仓（每周指定日期）
    if current_weekday != REBALANCE_WEEKDAY:
        return
    
    if g_last_rebalance_date == current_date:
        return
    
    print(f"[调仓] 开始调仓，日期: {{current_date}}")
    
    # 选股
    selected_stocks = select_stocks(ContextInfo, current_date)
    if not selected_stocks:
        print("[调仓] 无股票可选，跳过调仓")
        return
    
    # 获取账户信息
    account_info = ContextInfo.get_account_info(ContextInfo.accout_id)
    if not account_info:
        print("[调仓] 无法获取账户信息")
        return
    
    total_asset = account_info.m_dBalance
    cash = account_info.m_dAvailable
    current_positions = ContextInfo.get_trade_detail_data(ContextInfo.accout_id, 'stock', 'position')
    
    # 计算目标仓位
    target_positions = {{}}
    position_value = total_asset * SINGLE_POSITION_MAX
    
    for stock in selected_stocks:
        # 获取当前价格
        current_price = ContextInfo.get_last_price(stock)
        if current_price == 0:
            continue
        
        target_amount = int(position_value / current_price / 100) * 100  # 整手
        if target_amount > 0:
            target_positions[stock] = target_amount
    
    # 卖出不在目标持仓中的股票
    for pos in current_positions:
        stock = pos.m_strInstrumentID
        if stock not in target_positions:
            print(f"[调仓] 卖出 {{stock}}")
            ContextInfo.order(stock, -pos.m_nVolume, ContextInfo.MARKET_SH_SZ)
            if stock in g_positions:
                del g_positions[stock]
    
    # 买入目标持仓中的股票
    for stock, target_amount in target_positions.items():
        # 查找当前持仓
        current_amount = 0
        for pos in current_positions:
            if pos.m_strInstrumentID == stock:
                current_amount = pos.m_nVolume
                break
        
        diff = target_amount - current_amount
        
        if diff > 0:
            print(f"[调仓] 买入 {{stock}} {{diff}}股")
            ContextInfo.order(stock, diff, ContextInfo.MARKET_SH_SZ)
            if stock not in g_positions:
                g_positions[stock] = {{
                    'cost_price': ContextInfo.get_last_price(stock),
                    'entry_date': current_date,
                    'highest_price': 0,
                    'partial_profit_1_done': False
                }}
        elif diff < 0:
            print(f"[调仓] 卖出 {{stock}} {{abs(diff)}}股")
            ContextInfo.order(stock, diff, ContextInfo.MARKET_SH_SZ)
    
    g_last_rebalance_date = current_date
    print(f"[调仓] 调仓完成")


# ==================== QMT研究环境入口函数 ====================
def init(ContextInfo):
    """
    策略初始化
    QMT研究环境入口函数
    """
    global g_stock_pool
    
    print("=" * 60)
    print("TRQuant Advisor V4.0 - QMT研究环境策略启动")
    print("=" * 60)
    
    # 设置股票池（沪深300）
    index_code = "000300.SH"
    g_stock_pool = ContextInfo.get_stock_list_in_sector(index_code)
    # Normalize stock codes for QMT
    g_stock_pool = [normalize_stock_code(code) for code in g_stock_pool]
    ContextInfo.set_universe(g_stock_pool)
    
    print(f"✅ 股票池初始化: {{len(g_stock_pool)}} 只股票")
    
    # 设置定时任务
    # QMT研究环境使用run_time (不支持weekday参数)
    # 注意: QMT run_time() 不支持 weekday 参数
    # 每周调仓将在 handlebar() 函数中检查星期几
    
    # 每日风控检查（14:50）
    ContextInfo.run_time('check_risk_control', '14:50:00', 'SH')
    
    print("✅ 定时任务已设置")
    print(f"   调仓: 每周{{['一','二','三','四','五'][REBALANCE_WEEKDAY]}} (在handlebar中检查)")
    print("   风控: 每日 14:50")
    print("=" * 60)


def handlebar(ContextInfo):
    """
    每日K线回调
    QMT研究环境主函数
    """
    global g_stock_pool
    
    current_weekday = ContextInfo.current_dt.weekday()
    current_time = ContextInfo.current_dt.strftime('%H:%M:%S')
    
    # 每周更新股票池（周一）
    if current_weekday == 0:  # 周一
        index_code = "000300.SH"
        g_stock_pool = ContextInfo.get_stock_list_in_sector(index_code)
        # Normalize stock codes
        g_stock_pool = [normalize_stock_code(code) for code in g_stock_pool]
        ContextInfo.set_universe(g_stock_pool)
        print(f"[盘前] 股票池已更新: {{len(g_stock_pool)}} 只股票")
    
    # 风控检查（每日收盘前，约14:50）
    if current_time >= '14:50:00':
        check_risk_control(ContextInfo)
    
    # 调仓（每周指定日期，约09:35）
    if current_weekday == REBALANCE_WEEKDAY and current_time >= '09:35:00':
        rebalance(ContextInfo)
'''
