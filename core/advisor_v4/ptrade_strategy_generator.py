#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTrade策略代码生成器 - 生成基于7个已验证因子的完整策略代码

功能：
1. 生成PTrade平台格式的策略代码
2. 内联实现7个已验证因子的计算逻辑
3. 实现完整的选股、仓位、风控、止损止盈逻辑
4. 适配PTrade的API和回调机制
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from .bullettrade_strategy_generator import StrategyConfig

logger = logging.getLogger(__name__)


class PTradeStrategyGenerator:
    """PTrade策略代码生成器"""
    
    def __init__(
        self,
        config: Optional[StrategyConfig] = None,
    ):
        """
        初始化PTrade策略代码生成器
        
        Args:
            config: 策略配置
        """
        self.config = config or StrategyConfig()
    
    def generate_strategy_code(self) -> str:
        """
        生成完整的PTrade策略代码
        
        Returns:
            策略代码字符串
        """
        return f'''# -*- coding: utf-8 -*-
"""
TRQuant Advisor V4.0 - PTrade策略代码
=====================================

策略说明:
- 基于7个已验证因子的多因子选股策略
- 100%使用已验证因子，不使用聚宽因子
- 完整的风险控制和止损止盈机制

因子列表:
1. 20日动量 (momentum_20d) - 核心因子
2. 相对位置 (rel_position) - 核心因子
3. 市值 (market_cap) - 核心因子
4. 5日动量 (momentum_5d) - 确认因子
5. 换手率 (turnover_rate) - 流动性因子
6. ROE (roe) - 基本面因子
7. 净利润增长率 (growth) - 成长性因子

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
平台: PTrade (恒生)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# PTrade平台API（实际运行时由平台提供）
# from ptrade import *

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
g = type('G', (), {{}})()  # 全局状态对象
g.positions = {{}}  # 持仓记录 {{股票代码: {{'cost_price': 成本价, 'entry_date': 买入日期, 'highest_price': 最高价, 'partial_profit_1_done': False}}}}
g.stock_pool = []  # 股票池
g.last_rebalance_date = None  # 上次调仓日期


# ==================== 数据获取函数 ====================
def get_stock_list():
    """获取股票池（沪深300成分股）"""
    try:
        # PTrade获取指数成分股
        # 注意：PTrade API可能不同，需要根据实际API调整
        index_code = "000300.SH"  # PTrade使用.SH/.SZ格式
        stock_list = get_index_component(index_code)  # PTrade API
        if stock_list:
            return stock_list
        return []
    except Exception as e:
        print(f"获取股票池失败: {{e}}")
        return []


def get_price_ptrade(stocks, count=None, fields=None):
    """
    获取价格数据（PTrade版本）
    
    Args:
        stocks: 股票代码列表（.SH/.SZ格式）
        count: 获取最近N条数据
        fields: 字段列表 ['open', 'high', 'low', 'close', 'volume']
    
    Returns:
        DataFrame，列名为股票代码
    """
    try:
        # PTrade使用get_klines API
        # get_klines(security, count, frequency='1d')
        # 注意：PTrade API可能需要逐个股票获取，或支持批量获取
        
        if fields is None:
            fields = ['open', 'high', 'low', 'close', 'volume']
        
        result = {{}}
        for stock in stocks:
            try:
                # PTrade API: get_klines(security, count, frequency='1d')
                klines = get_klines(stock, count or 20, frequency='1d')
                if klines is not None and len(klines) > 0:
                    result[stock] = klines
            except Exception as e:
                print(f"获取{{stock}}数据失败: {{e}}")
                continue
        
        # 转换为DataFrame（根据PTrade返回格式调整）
        if result:
            # PTrade返回格式可能是字典或DataFrame，需要根据实际情况调整
            df = pd.DataFrame(result)
            return df
        return None
    
    except Exception as e:
        print(f"获取价格数据失败: {{e}}")
        return None


def get_fundamentals_ptrade(stocks, date_str, fields=None):
    """
    获取基本面数据（PTrade版本）
    
    Args:
        stocks: 股票代码列表
        date_str: 日期字符串（YYYY-MM-DD）
        fields: 字段列表 ['market_cap', 'roe', 'net_profit_growth_rate']
    
    Returns:
        DataFrame
    """
    try:
        # PTrade基本面数据API
        # 注意：PTrade可能使用不同的API获取基本面数据
        # 需要根据实际PTrade API文档调整
        
        if fields is None:
            fields = ['market_cap', 'roe', 'net_profit_growth_rate']
        
        # PTrade可能使用get_fundamentals或类似API
        # fundamentals = get_fundamentals(stocks, fields, date=date_str)
        
        # 如果PTrade不支持基本面数据，返回None
        print("⚠️ 警告: PTrade基本面数据获取需要根据实际API调整")
        return None
    
    except Exception as e:
        print(f"获取基本面数据失败: {{e}}")
        return None


# ==================== 因子计算函数 ====================
def calculate_validated_factors(codes, date_str):
    """
    计算已验证因子（7因子）
    
    Args:
        codes: 股票代码列表（.SH/.SZ格式）
        date_str: 日期字符串（YYYY-MM-DD）
    
    Returns:
        DataFrame，包含所有因子值
    """
    if not codes:
        return None
    
    try:
        # 获取价格数据
        prices_20 = get_price_ptrade(codes, count=20)
        prices_5 = get_price_ptrade(codes, count=5)
        
        if prices_20 is None or prices_5 is None:
            return None
        
        # 获取基本面数据
        fundamentals = get_fundamentals_ptrade(codes, date_str, fields=['market_cap', 'roe', 'net_profit_growth_rate'])
        
        # 初始化结果DataFrame
        result = pd.DataFrame({{'code': codes}})
        
        # 1. 20日动量
        for code in codes:
            if code in prices_20.columns or code in prices_20.index:
                try:
                    price_data = prices_20[code] if code in prices_20.columns else prices_20.loc[code]
                    if len(price_data) >= 20:
                        close_vals = price_data['close'] if isinstance(price_data, pd.Series) else price_data
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
            if code in prices_20.columns or code in prices_20.index:
                try:
                    price_data = prices_20[code] if code in prices_20.columns else prices_20.loc[code]
                    if len(price_data) >= 20:
                        high_vals = price_data['high'] if isinstance(price_data, pd.Series) else price_data
                        low_vals = price_data['low'] if isinstance(price_data, pd.Series) else price_data
                        close_vals = price_data['close'] if isinstance(price_data, pd.Series) else price_data
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
            result['market_cap'] = result['code'].map(dict(zip(fundamentals['code'], fundamentals['market_cap']))).fillna(0.0)
        else:
            result['market_cap'] = 0.0
        
        # 4. 5日动量
        for code in codes:
            if code in prices_5.columns or code in prices_5.index:
                try:
                    price_data = prices_5[code] if code in prices_5.columns else prices_5.loc[code]
                    if len(price_data) >= 5:
                        close_vals = price_data['close'] if isinstance(price_data, pd.Series) else price_data
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
        
        # 5. 换手率（20日平均）
        for code in codes:
            if code in prices_20.columns or code in prices_20.index:
                try:
                    price_data = prices_20[code] if code in prices_20.columns else prices_20.loc[code]
                    if len(price_data) >= 20:
                        volume_vals = price_data['volume'] if isinstance(price_data, pd.Series) else price_data
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
            result['roe'] = result['code'].map(dict(zip(fundamentals['code'], fundamentals['roe']))).fillna(0.0)
        else:
            result['roe'] = 0.0
        
        # 7. 净利润增长率（从基本面数据获取）
        if fundamentals is not None and 'net_profit_growth_rate' in fundamentals.columns:
            result['growth'] = result['code'].map(dict(zip(fundamentals['code'], fundamentals['net_profit_growth_rate']))).fillna(0.0)
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
def select_stocks(date_str):
    """
    选股函数
    
    Args:
        date_str: 日期字符串（YYYY-MM-DD）
    
    Returns:
        选中的股票代码列表
    """
    # 获取股票池
    stock_pool = get_stock_list()
    if not stock_pool:
        print(f"[选股] 股票池为空")
        return []
    
    # 计算因子
    factors_df = calculate_validated_factors(stock_pool, date_str)
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


# ==================== 交易函数 ====================
def get_current_positions():
    """获取当前持仓"""
    try:
        # PTrade获取持仓API
        positions = get_positions()  # PTrade API
        pos_dict = {{}}
        for pos in positions:
            stock_code = pos.stock_code  # 根据PTrade实际API调整
            pos_dict[stock_code] = {{
                'amount': pos.total_qty,  # 根据PTrade实际API调整
                'cost_price': pos.cost_price,  # 根据PTrade实际API调整
                'current_price': pos.current_price  # 根据PTrade实际API调整
            }}
        return pos_dict
    except Exception as e:
        print(f"获取持仓失败: {{e}}")
        return {{}}


def get_account_info():
    """获取账户信息"""
    try:
        # PTrade获取账户信息API
        account = get_account()  # PTrade API
        return {{
            'total_asset': account.total_asset,  # 根据PTrade实际API调整
            'cash': account.available_cash,  # 根据PTrade实际API调整
            'market_value': account.market_value  # 根据PTrade实际API调整
        }}
    except Exception as e:
        print(f"获取账户信息失败: {{e}}")
        return None


def order_stock(stock_code, amount, price=0, order_type='market'):
    """
    下单函数
    
    Args:
        stock_code: 股票代码（.SH/.SZ格式）
        amount: 数量（正数买入，负数卖出）
        price: 价格（0表示市价）
        order_type: 订单类型（'market'或'limit'）
    
    Returns:
        订单ID
    """
    try:
        # PTrade下单API
        # 注意：PTrade API可能需要根据实际文档调整
        
        if amount > 0:
            # 买入
            if order_type == 'market' or price == 0:
                order_id = order(stock_code, amount)  # 市价单
            else:
                order_id = order(stock_code, amount, price=price)  # 限价单
        else:
            # 卖出
            amount = abs(amount)
            if order_type == 'market' or price == 0:
                order_id = order(stock_code, -amount)  # 市价单
            else:
                order_id = order(stock_code, -amount, price=price)  # 限价单
        
        print(f"[下单] {{stock_code}} {{'买入' if amount > 0 else '卖出'}} {{abs(amount)}}股，订单ID: {{order_id}}")
        return order_id
    
    except Exception as e:
        print(f"下单失败: {{e}}")
        return None


# ==================== 风控函数 ====================
def check_risk_control():
    """风控检查（止损止盈）"""
    current_date = datetime.now().strftime('%Y-%m-%d')
    positions = get_current_positions()
    
    for stock_code, pos_info in positions.items():
        if stock_code not in g.positions:
            # 初始化持仓记录
            g.positions[stock_code] = {{
                'cost_price': pos_info['cost_price'],
                'entry_date': current_date,
                'highest_price': pos_info['current_price'],
                'partial_profit_1_done': False
            }}
        
        pos_record = g.positions[stock_code]
        cost_price = pos_record['cost_price']
        current_price = pos_info['current_price']
        
        # 更新最高价
        if current_price > pos_record['highest_price']:
            pos_record['highest_price'] = current_price
        
        # 计算盈亏
        pnl = (current_price - cost_price) / cost_price
        
        # 止损
        if pnl <= STOP_LOSS:
            print(f"[止损] {{stock_code}} 亏损 {{pnl*100:.2f}}%，卖出")
            order_stock(stock_code, -pos_info['amount'])
            del g.positions[stock_code]
            continue
        
        # 止盈
        if pnl >= TAKE_PROFIT:
            print(f"[止盈] {{stock_code}} 盈利 {{pnl*100:.2f}}%，卖出")
            order_stock(stock_code, -pos_info['amount'])
            del g.positions[stock_code]
            continue
        
        # 移动止损（盈利超过触发条件后启用）
        if pnl >= TRAILING_STOP_TRIGGER:
            trailing_pnl = (current_price - pos_record['highest_price']) / pos_record['highest_price']
            if trailing_pnl <= TRAILING_STOP:
                print(f"[移动止损] {{stock_code}} 从最高价回撤 {{trailing_pnl*100:.2f}}%，卖出")
                order_stock(stock_code, -pos_info['amount'])
                del g.positions[stock_code]
                continue
        
        # 分批止盈
        if not pos_record['partial_profit_1_done'] and pnl >= PARTIAL_PROFIT_1:
            sell_amount = int(pos_info['amount'] * PARTIAL_PROFIT_1_RATIO)
            print(f"[分批止盈] {{stock_code}} 盈利 {{pnl*100:.2f}}%，卖出{{PARTIAL_PROFIT_1_RATIO*100:.0f}}%")
            order_stock(stock_code, -sell_amount)
            pos_record['partial_profit_1_done'] = True
        
        # 时间止损
        entry_date = datetime.strptime(pos_record['entry_date'], '%Y-%m-%d')
        days_held = (datetime.now() - entry_date).days
        if days_held >= TIME_STOP_DAYS:
            print(f"[时间止损] {{stock_code}} 持仓{{days_held}}天，卖出")
            order_stock(stock_code, -pos_info['amount'])
            del g.positions[stock_code]


# ==================== 调仓函数 ====================
def rebalance():
    """调仓函数"""
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_weekday = datetime.now().weekday()
    
    # 检查是否需要调仓（每周指定日期）
    if current_weekday != REBALANCE_WEEKDAY:
        return
    
    if g.last_rebalance_date == current_date:
        return
    
    print(f"[调仓] 开始调仓，日期: {{current_date}}")
    
    # 选股
    selected_stocks = select_stocks(current_date)
    if not selected_stocks:
        print("[调仓] 无股票可选，跳过调仓")
        return
    
    # 获取账户信息
    account_info = get_account_info()
    if not account_info:
        print("[调仓] 无法获取账户信息")
        return
    
    total_asset = account_info['total_asset']
    cash = account_info['cash']
    current_positions = get_current_positions()
    
    # 计算目标仓位
    target_positions = {{}}
    position_value = total_asset * SINGLE_POSITION_MAX
    for stock in selected_stocks:
        # 获取当前价格
        prices = get_price_ptrade([stock], count=1)
        if prices is None or len(prices) == 0:
            continue
        
        # 根据PTrade返回格式获取价格
        try:
            if stock in prices.columns:
                current_price = prices[stock].iloc[-1]['close'] if isinstance(prices[stock], pd.Series) else prices[stock].iloc[-1]
            else:
                current_price = prices.iloc[-1]['close'] if 'close' in prices.columns else 0
        except:
            current_price = 0
        
        if current_price == 0:
            continue
        
        target_amount = int(position_value / current_price / 100) * 100  # 整手
        if target_amount > 0:
            target_positions[stock] = target_amount
    
    # 卖出不在目标持仓中的股票
    for stock, pos_info in current_positions.items():
        if stock not in target_positions:
            print(f"[调仓] 卖出 {{stock}}")
            order_stock(stock, -pos_info['amount'])
            if stock in g.positions:
                del g.positions[stock]
    
    # 买入目标持仓中的股票
    for stock, target_amount in target_positions.items():
        current_amount = current_positions.get(stock, {{}}).get('amount', 0)
        diff = target_amount - current_amount
        
        if diff > 0:
            print(f"[调仓] 买入 {{stock}} {{diff}}股")
            order_stock(stock, diff)
            if stock not in g.positions:
                g.positions[stock] = {{
                    'cost_price': get_price_ptrade([stock], count=1)[stock].iloc[-1]['close'] if stock in get_price_ptrade([stock], count=1).columns else 0,
                    'entry_date': current_date,
                    'highest_price': 0,
                    'partial_profit_1_done': False
                }}
        elif diff < 0:
            print(f"[调仓] 卖出 {{stock}} {{abs(diff)}}股")
            order_stock(stock, diff)
    
    g.last_rebalance_date = current_date
    print(f"[调仓] 调仓完成")


# ==================== PTrade策略入口函数 ====================
def initialize(context):
    """
    策略初始化
    PTrade入口函数
    """
    print("=" * 60)
    print("TRQuant Advisor V4.0 - PTrade策略启动")
    print("=" * 60)
    
    # 初始化股票池
    g.stock_pool = get_stock_list()
    print(f"✅ 股票池初始化: {{len(g.stock_pool)}} 只股票")
    
    # 设置定时任务
    # PTrade使用schedule语法
    weekday_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    weekday_name = weekday_names[REBALANCE_WEEKDAY]
    
    # 每周调仓（周一09:35）
    schedule(time='09:35', func=rebalance, weekday=weekday_name)  # PTrade schedule语法
    
    # 每日风控检查（14:50）
    schedule(time='14:50', func=check_risk_control)  # PTrade schedule语法
    
    print("✅ 定时任务已设置")
    print(f"   调仓: 每周{{['一','二','三','四','五'][REBALANCE_WEEKDAY]}} 09:35")
    print("   风控: 每日 14:50")
    print("=" * 60)


def before_market_open(context):
    """盘前准备"""
    # 每周更新股票池（周一）
    current_date = datetime.now().strftime('%Y-%m-%d')
    if datetime.now().weekday() == 0:  # 周一
        g.stock_pool = get_stock_list()
        print(f"[盘前] 股票池已更新: {{len(g.stock_pool)}} 只股票")


def handle_data(context, data):
    """盘中处理（PTrade可能不需要此函数，或使用不同回调）"""
    # PTrade可能使用不同的回调机制
    # 根据实际PTrade API调整
    pass


def after_market_close(context):
    """盘后处理"""
    # 记录日志、更新状态等
    pass
'''
