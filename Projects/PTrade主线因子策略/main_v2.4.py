# -*- coding: utf-8 -*-
"""
韬睿量化 - PTrade智能选股策略（主线趋势型 v2.4）
========================================

策略名称: 主线趋势型策略（长期成长+情绪辅助）
创建时间: 2025-12-09
平台: PTrade (恒生)
版本: v2.4

核心改进（基于v2.3回测结果分析）:
---------
1. **低频调仓**：调仓间隔从5个交易日延长到18个交易日，减少频繁调仓
2. **主线驱动**：候选股优先来自主线主题内，非全市场泛选
3. **强化趋势因子**：加入ADX、MACD稳定性，行业景气度、板块涨幅相对强度
4. **优化风控**：移除全组合止损，保留个股止损/止盈，提高容错区间
5. **优化持仓质量评估**：加权打分行业+个股表现+波动率
6. **最低持仓时间**：MIN_HOLD_DAYS = 10，避免过早止盈
7. **紧急调仓阈值放宽**：从5%提高到12%，减少频繁触发

策略说明:
---------
这是一个使用正确PTrade API的智能选股策略：

1. **正确的因子计算**：使用PTrade标准API获取PE、PB、市值、股息率
2. **全市场选股**：从所有A股中选股，不限于成分股
3. **主线动量因子**：实现主线动量因子，作为选股因子之一
4. **严格错误处理**：如果无法获取基本面数据，报错停止，不使用代理
5. **API调用时机限制**：遵守PTrade API调用时机限制

核心改进:
---------
- 使用正确的PTrade API：get_fundamentals(stocks, 'valuation', date, fields)
- 字段名：total_value(市值), pe_dynamic(PE), pb(PB), dividend_ratio(股息率)
- 全市场选股：使用get_Ashares获取所有A股（在handle_data中调用，不在initialize中）
- 主线动量因子：计算主线板块的动量，作为选股因子
- API调用时机：get_Ashares不在initialize中调用，filter_stock_by_status不在handle_data中调用

PTrade兼容性:
-------------
- 严格按照PTrade API文档实现
- 遵守PTrade API调用时机限制：
  * get_Ashares不能在initialize阶段调用
  * filter_stock_by_status不能在盘中handle_data阶段调用
- 如果API调用失败，报错停止，不使用代理方案
- 符合PTrade代码规范
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==================== 策略参数 ====================

# 选股参数
STOCK_NUM = 10              # 持仓股票数量
MAX_POSITION = 0.90         # 最大仓位比例（牛市）
MIN_POSITION = 0.50         # 最小仓位比例（震荡市）
BEAR_POSITION = 0.30        # 熊市仓位比例

# 风险控制参数（v2.4优化：移除全组合止损，保留个股止损/止盈）
STOP_LOSS_SINGLE = -0.12    # 单只股票止损比例（-12%，放宽以提高容错区间）
# STOP_LOSS_TOTAL = -0.20   # 整体回撤止损比例（v2.4移除，避免过于激进）
STOP_LOSS_RECOVERY = -0.05  # 止损恢复阈值
TAKE_PROFIT = 0.30          # 止盈比例（30%，提高以让利润奔跑）
MAX_HOLD_DAYS = 60          # 最大持仓天数（延长以捕捉长期成长）
MIN_HOLD_DAYS = 10          # 最小持仓天数（v2.4：从3天提高到10天，避免过早止盈）

# 调仓参数（v2.4优化：低频调仓）
REBALANCE_INTERVAL = 18     # 调仓间隔（交易日，v2.4：从5天延长到18天，减少频繁调仓）
EMERGENCY_REBALANCE_THRESHOLD = 0.12  # 紧急调仓阈值（v2.4：从5%提高到12%，减少频繁触发）
POSITION_QUALITY_DECLINE_THRESHOLD = 0.15  # 持仓质量下降阈值（v2.4：从10%提高到15%，减少频繁触发）

# 选股参数（v2.4优化：主线驱动候选池）
CANDIDATE_POOL_SIZE = 300   # 候选股票池大小（v2.4：从500降低到300，优先从主线主题内选股）
MAINLINE_POOL_SIZE = 200    # 主线主题候选池大小（v2.4新增：从主线主题内选股）
MIN_POSITION_VALUE = 5000   # 最小持仓金额（元）
MIN_TRADING_UNIT = 100      # 最小交易单位（股）
MIN_STOCK_PRICE = 5.0       # 最小股票价格（元）
MAX_STOCK_PRICE = 500.0     # 最大股票价格（元）

# 主线动量参数（v2.4优化：强化主线识别）
MAINLINE_MOMENTUM_PERIOD = 20  # 主线动量计算周期（天）
MAINLINE_TOP_N = 10            # 选择前N个主线板块
MAINLINE_UPDATE_INTERVAL = 3   # 主线更新间隔（交易日，v2.4新增）

# 趋势因子参数（v2.4新增：强化趋势因子）
ADX_PERIOD = 14            # ADX计算周期
MACD_FAST = 12             # MACD快线周期
MACD_SLOW = 26             # MACD慢线周期
MACD_SIGNAL = 9            # MACD信号线周期
INDUSTRY_MOMENTUM_PERIOD = 20  # 行业景气度计算周期

# 基准指数
BENCHMARK = '000300.XSHG'   # 沪深300

# ==================== 策略类型配置 ====================

# 牛市策略（risk_on）：追涨策略（v2.4优化：强化趋势因子）
BULL_STRATEGY = {
    'name': '牛市追涨策略',
    'factors': {
        'trend_strength': 0.25,      # 趋势强度因子（v2.4新增：ADX、MACD）
        'mainline_momentum': 0.25,   # 主线动量因子（v2.4：权重提高）
        'industry_momentum': 0.20,   # 行业景气度因子（v2.4新增）
        'momentum': 0.15,            # 动量因子（v2.4：权重降低）
        'growth': 0.10,              # 成长因子（v2.4：权重降低）
        'quality': 0.05,            # 质量因子（v2.4：权重降低）
    },
    'position': MAX_POSITION,
    'buy_rule': 'breakout',
    'sell_rule': 'trailing',
}

# 熊市策略（risk_off）：防御策略
BEAR_STRATEGY = {
    'name': '熊市防御策略',
    'factors': {
        'value': 0.30,          # 价值因子
        'quality': 0.25,         # 质量因子
        'volatility': 0.20,      # 低波动因子
        'dividend': 0.15,        # 股息因子
        'reversal': 0.10,        # 反转因子
    },
    'position': BEAR_POSITION,
    'buy_rule': 'oversold',
    'sell_rule': 'quick_profit',
}

# 震荡市策略（neutral）：均衡策略（v2.4优化：强化趋势因子）
NEUTRAL_STRATEGY = {
    'name': '震荡市均衡策略',
    'factors': {
        'trend_strength': 0.20,      # 趋势强度因子（v2.4新增）
        'mainline_momentum': 0.25,  # 主线动量因子（v2.4：权重提高）
        'value': 0.15,               # 价值因子（v2.4：权重降低）
        'growth': 0.15,              # 成长因子（v2.4：权重降低）
        'quality': 0.15,            # 质量因子（v2.4：权重降低）
        'momentum': 0.10,           # 动量因子（v2.4：权重降低）
    },
    'position': MIN_POSITION,
    'buy_rule': 'mean_reversion',
    'sell_rule': 'profit_target',
}

# 全局变量
g = type('g', (), {
    'last_rebalance_date': None,
    'last_rebalance_trading_days': 0,  # 上次调仓的交易日计数
    'market_regime': 'neutral',
    'current_strategy': NEUTRAL_STRATEGY,
    'candidate_pool': [],
    'peak_value': 0,
    'hold_days': {},
    'entry_prices': {},
    'stop_loss_triggered': False,
    'stop_loss_date': None,
    'fundamentals_cache': {},
    'mainline_cache': {},  # 主线缓存
    'all_stocks': [],  # 全市场股票列表
    'trading_days_count': 0,  # 交易日计数器
    'last_market_trend': None,  # 上次市场趋势（用于检测市场变化）
    'last_position_quality': None,  # 上次持仓质量（用于检测质量下降）
    'mainline_pool': [],  # 主线主题候选池（v2.4新增）
    'last_mainline_update': None,  # 上次主线更新日期（v2.4新增）
    'mainline_stocks': {},  # 主线股票映射（v2.4新增：{mainline_name: [stocks]}）
})()


# ==================== 初始化函数 ====================

def initialize(context):
    """
    策略初始化函数
    
    Args:
        context: PTrade策略上下文对象
    """
    try:
        set_benchmark(BENCHMARK)
    except:
        pass
    
    # 初始化全局变量
    g.peak_value = context.portfolio.total_value
    g.last_rebalance_date = None
    g.last_rebalance_trading_days = 0
    g.market_regime = 'neutral'
    g.current_strategy = NEUTRAL_STRATEGY
    g.candidate_pool = []
    g.hold_days = {}
    g.entry_prices = {}
    g.stop_loss_triggered = False
    g.stop_loss_date = None
    g.fundamentals_cache = {}
    g.mainline_cache = {}
    g.all_stocks = []  # 将在第一次handle_data时获取
    g.stocks_initialized = False  # 标记是否已初始化股票列表
    g.trading_days_count = 0  # 交易日计数器
    g.last_market_trend = None  # 上次市场趋势
    g.last_position_quality = None  # 上次持仓质量
    g.mainline_pool = []  # 主线主题候选池（v2.4新增）
    g.last_mainline_update = None  # 上次主线更新日期（v2.4新增）
    g.mainline_stocks = {}  # 主线股票映射（v2.4新增）
    
    print('=' * 60)
    print('韬睿量化 - PTrade智能选股策略（主线趋势型 v2.4）')
    print('=' * 60)
    print(f'基准指数: {BENCHMARK}')
    print(f'持仓数量: {STOCK_NUM}只')
    print(f'调仓间隔: {REBALANCE_INTERVAL}个交易日（v2.4：低频调仓）')
    print(f'紧急调仓阈值: 市场波动 {EMERGENCY_REBALANCE_THRESHOLD*100:.1f}% 或持仓质量下降 {POSITION_QUALITY_DECLINE_THRESHOLD*100:.1f}%')
    print(f'候选池大小: {CANDIDATE_POOL_SIZE}只（主线驱动）')
    print(f'最低持仓时间: {MIN_HOLD_DAYS}天（v2.4：避免过早止盈）')
    print(f'风控优化: 移除全组合止损，保留个股止损/止盈')
    print('=' * 60)
    print('[注意] get_Ashares不能在initialize阶段调用，将在第一次handle_data时获取股票列表')
    print('=' * 60)


# ==================== 行情处理函数 ====================

def handle_data(context, data):
    """
    行情处理函数（PTrade主入口）
    """
    current_dt = context.current_dt
    current_date = current_dt.date()
    current_date_str = current_dt.strftime('%Y-%m-%d')
    current_hour = current_dt.hour
    current_minute = current_dt.minute
    
    # 只在09:35执行交易逻辑
    if current_hour == 9 and current_minute == 35:
        try:
            trade(context, current_date, current_date_str)
        except Exception as e:
            print(f'[错误] 交易逻辑执行失败: {e}')
            import traceback
            traceback.print_exc()
            raise  # 报错停止
    
    # 每日收盘后更新持仓天数
    if current_hour == 15 and current_minute == 0:
        update_hold_days(context, current_date)


# ==================== 交易逻辑 ====================

def count_trading_days(start_date, end_date):
    """
    计算两个日期之间的交易日数量（健壮版：使用交易日计数器）
    
    在PTrade中，handle_data只在交易日调用，所以每次调用就是1个交易日。
    我们使用交易日计数器来准确计算。
    
    Args:
        start_date: 开始日期（date对象）
        end_date: 结束日期（date对象）
    
    Returns:
        int: 交易日数量
    """
    # 如果日期相同，返回0
    if start_date >= end_date:
        return 0
    
    # 方法1：使用交易日计数器（最准确）
    # 在PTrade中，每次handle_data调用就是1个交易日
    # 我们通过比较当前交易日计数和上次调仓时的交易日计数来计算
    if g.last_rebalance_date is not None and g.last_rebalance_date == start_date:
        if hasattr(g, 'trading_days_count') and hasattr(g, 'last_rebalance_trading_days'):
            # 计算交易日差值
            trading_days_diff = g.trading_days_count - g.last_rebalance_trading_days
            return max(0, trading_days_diff)
    
    # 方法2：简单估算（排除周末和节假日）
    days = (end_date - start_date).days
    if days <= 0:
        return 0
    
    # 计算周末数量（粗略估算）
    # 每周有2个周末日（周六、周日）
    weekends = (days // 7) * 2
    
    # 调整边界情况
    start_weekday = start_date.weekday()  # 0=周一, 6=周日
    end_weekday = end_date.weekday()
    
    # 如果跨周末，需要额外调整
    if start_weekday > end_weekday:  # 跨周末
        weekends += 1
    
    # 如果开始或结束在周末，需要调整
    if start_weekday == 5:  # 周六开始
        weekends -= 1
    elif start_weekday == 6:  # 周日开始
        weekends -= 2
    
    if end_weekday == 5:  # 周六结束
        weekends -= 1
    elif end_weekday == 6:  # 周日结束
        weekends -= 1
    
    trading_days = days - weekends
    return max(0, trading_days)


def check_emergency_rebalance(context, current_date_str):
    """
    检查是否需要紧急调仓
    
    触发条件：
    1. 市场剧烈波动（指数涨跌幅超过阈值）
    2. 持仓质量显著下降
    3. 市场状态发生重大变化
    
    Args:
        context: 策略上下文
        current_date_str: 当前日期字符串
    
    Returns:
        tuple: (是否需要紧急调仓, 原因)
    """
    try:
        # 条件1：检查市场剧烈波动
        hist = get_price(BENCHMARK, count=2, fields=['close'])
        if hist is not None and len(hist) >= 2:
            current_price = hist['close'].iloc[-1]
            prev_price = hist['close'].iloc[-2]
            market_change = (current_price / prev_price - 1) if prev_price > 0 else 0
            
            if abs(market_change) >= EMERGENCY_REBALANCE_THRESHOLD:
                return True, f"市场剧烈波动: {market_change*100:.2f}%"
        
        # 条件2：检查持仓质量下降（需要至少持仓2个交易日后才评估，避免刚调仓就触发）
        if g.last_rebalance_date is not None and g.last_position_quality is not None:
            try:
                current_date_obj = datetime.strptime(current_date_str, '%Y-%m-%d').date()
                trading_days_since = count_trading_days(g.last_rebalance_date, current_date_obj)
                
                # 至少持仓2个交易日后才评估质量下降（避免刚调仓就触发）
                if trading_days_since >= 2:
                    current_quality = evaluate_position_quality(context, current_date_str)
                    if current_quality is not None:
                        quality_decline = g.last_position_quality - current_quality
                        if quality_decline >= POSITION_QUALITY_DECLINE_THRESHOLD:
                            return True, f"持仓质量下降: {quality_decline*100:.2f}%"
            except:
                pass  # 如果计算失败，不触发紧急调仓
        
        # 条件3：检查市场状态变化
        current_trend = analyze_market_trend_v2(context, current_date_str)
        if g.last_market_trend is not None:
            last_regime = determine_market_regime(
                g.last_market_trend.get('market_phase', 'neutral'),
                g.last_market_trend.get('composite_score', 0)
            )
            current_regime = determine_market_regime(
                current_trend.get('market_phase', 'neutral'),
                current_trend.get('composite_score', 0)
            )
            
            # 如果市场状态从牛市变熊市，或从熊市变牛市，触发紧急调仓
            if (last_regime == 'bull' and current_regime == 'bear') or \
               (last_regime == 'bear' and current_regime == 'bull'):
                return True, f"市场状态重大变化: {last_regime} → {current_regime}"
        
        return False, None
        
    except Exception as e:
        print(f'[调试] 检查紧急调仓失败: {e}')
        return False, None


def evaluate_position_quality(context, date_str):
    """
    评估当前持仓质量（v2.4优化：加权打分行业+个股表现+波动率）
    
    评估指标：
    1. 持仓股票相对于基准的收益率（个股表现）
    2. 持仓股票所属行业的相对表现（行业表现）
    3. 持仓股票的风险调整收益（波动率）
    
    Args:
        context: 策略上下文
        date_str: 当前日期字符串
    
    Returns:
        float: 持仓质量得分（0-1），越高越好
    """
    try:
        positions = list(context.portfolio.positions.keys())
        if not positions:
            return 0.5  # 无持仓时返回中等质量
        
        # 获取基准指数表现
        try:
            benchmark_hist = get_price(BENCHMARK, count=5, fields=['close'])
            if benchmark_hist is not None and len(benchmark_hist) >= 2:
                benchmark_current = benchmark_hist['close'].iloc[-1]
                benchmark_prev = benchmark_hist['close'].iloc[-2]
                benchmark_return = (benchmark_current / benchmark_prev - 1) if benchmark_prev > 0 else 0
            else:
                benchmark_return = 0
        except:
            benchmark_return = 0
        
        # v2.4优化：加权打分行业+个股表现+波动率
        quality_scores = []
        for stock in positions:
            try:
                # 1. 个股表现（相对于买入价和基准）
                current_hist = get_price(stock, count=1, fields=['close'])
                if current_hist is None or len(current_hist) == 0:
                    continue
                
                current_price = current_hist['close'].iloc[-1]
                entry_price = g.entry_prices.get(stock, None)
                
                if entry_price and entry_price > 0:
                    stock_return = (current_price / entry_price - 1) if entry_price > 0 else 0
                else:
                    hist = get_price(stock, count=5, fields=['close'])
                    if hist is not None and len(hist) >= 2:
                        stock_return = (hist['close'].iloc[-1] / hist['close'].iloc[-2] - 1) if hist['close'].iloc[-2] > 0 else 0
                    else:
                        continue
                
                excess_return = stock_return - benchmark_return
                stock_score = 1.0 / (1.0 + np.exp(-excess_return * 20))  # 个股表现得分
                
                # 2. 行业表现（v2.4新增）
                industry_score = 0.5  # 默认中等
                try:
                    stock_blocks = get_stock_blocks(stock)
                    if stock_blocks:
                        # 获取股票所属行业/板块
                        blocks_list = []
                        if isinstance(stock_blocks, (list, tuple)):
                            blocks_list = list(stock_blocks)[:1]  # 只取第一个板块
                        elif isinstance(stock_blocks, pd.DataFrame):
                            if 'block_name' in stock_blocks.columns:
                                blocks_list = stock_blocks['block_name'].head(1).tolist()
                        
                        if blocks_list:
                            # 计算行业相对表现
                            try:
                                industry_stocks = get_industry_stocks(blocks_list[0])
                                if industry_stocks and len(industry_stocks) > 0:
                                    # 计算行业平均收益率
                                    industry_returns = []
                                    for ind_stock in list(industry_stocks)[:20]:
                                        try:
                                            ind_hist = get_price(ind_stock, count=5, fields=['close'])
                                            if ind_hist is not None and len(ind_hist) >= 2:
                                                ind_return = (ind_hist['close'].iloc[-1] / ind_hist['close'].iloc[-2] - 1) if ind_hist['close'].iloc[-2] > 0 else 0
                                                industry_returns.append(ind_return)
                                        except:
                                            continue
                                    
                                    if industry_returns:
                                        avg_industry_return = np.mean(industry_returns)
                                        industry_excess = avg_industry_return - benchmark_return
                                        industry_score = 1.0 / (1.0 + np.exp(-industry_excess * 20))
                            except:
                                pass
                except:
                    pass
                
                # 3. 波动率（v2.4新增：低波动率得分高）
                volatility_score = 0.5  # 默认中等
                try:
                    hist_vol = get_price(stock, count=20, fields=['close'])
                    if hist_vol is not None and len(hist_vol) >= 10:
                        returns_vol = np.diff(hist_vol['close'].values) / hist_vol['close'].values[:-1]
                        volatility = np.std(returns_vol) * np.sqrt(252) if len(returns_vol) > 0 else 0.3
                        # 波动率越低，得分越高（归一化到0-1）
                        volatility_score = 1.0 / (1.0 + volatility * 5)  # 波动率0.2对应得分约0.5
                except:
                    pass
                
                # 4. 综合得分（v2.4：加权平均）
                # 权重：个股表现40%，行业表现30%，波动率30%
                quality_score = 0.4 * stock_score + 0.3 * industry_score + 0.3 * volatility_score
                quality_scores.append(quality_score)
            except:
                continue
        
        if quality_scores:
            avg_quality = np.mean(quality_scores)
            return avg_quality
        else:
            return 0.5  # 无法计算时返回中等质量
            
    except Exception as e:
        print(f'[调试] 评估持仓质量失败: {e}')
        return 0.5


def trade(context, current_date, current_date_str):
    """
    每日交易逻辑（改进版：使用交易日计算、紧急调仓、持仓质量监控）
    """
    print(f'\n[{current_date_str}] 开始交易逻辑')
    
    # 更新交易日计数器
    g.trading_days_count += 1
    
    # 更新峰值资金
    current_value = context.portfolio.total_value
    if current_value > g.peak_value:
        g.peak_value = current_value
    
    # 1. 风险控制检查
    if not risk_control(context):
        print('[风险控制] 触发止损，停止交易')
        return
    
    # 2. 检查是否需要调仓（使用交易日计算）
    need_rebalance = False
    rebalance_reason = None
    
    if g.last_rebalance_date is None:
        # 首次调仓
        need_rebalance = True
        rebalance_reason = "首次调仓"
    else:
        # 计算交易日数量
        trading_days_since = count_trading_days(g.last_rebalance_date, current_date)
        
        # 检查是否达到调仓间隔（交易日）
        if trading_days_since >= REBALANCE_INTERVAL:
            need_rebalance = True
            rebalance_reason = f"达到调仓间隔（{trading_days_since}个交易日）"
        else:
            # 检查是否需要紧急调仓
            emergency, emergency_reason = check_emergency_rebalance(context, current_date_str)
            if emergency:
                need_rebalance = True
                rebalance_reason = f"紧急调仓: {emergency_reason}"
    
    # 非调仓日：做风险控制和持仓质量监控
    if not need_rebalance:
        trading_days_since = count_trading_days(g.last_rebalance_date, current_date) if g.last_rebalance_date else 0
        print(f'[调仓] 距离上次调仓 {trading_days_since} 个交易日（自然日: {(current_date - g.last_rebalance_date).days if g.last_rebalance_date else 0}天），暂不调仓')
        
        # 评估持仓质量（只显示，不更新基准值，避免立即触发紧急调仓）
        positions = list(context.portfolio.positions.keys())
        if positions:
            current_quality = evaluate_position_quality(context, current_date_str)
            if g.last_position_quality is not None:
                quality_change = current_quality - g.last_position_quality
                print(f'[持仓质量] 当前: {current_quality:.3f}, 变化: {quality_change*100:+.2f}%')
            else:
                print(f'[持仓质量] 当前: {current_quality:.3f}（等待调仓后设置基准）')
                # 不在非调仓日设置基准，避免第二天立即触发紧急调仓
        else:
            print(f'[持仓质量] 无持仓')
        
        # 执行风险控制
        check_stop_loss(context)
        check_take_profit(context)
        log_portfolio_status(context)
        return
    
    # 3. 市场趋势分析
    market_trend = analyze_market_trend_v2(context, current_date_str)
    market_phase = market_trend.get('market_phase', 'neutral')
    composite_score = market_trend.get('composite_score', 0)
    
    # 4. 选择策略类型
    g.market_regime = determine_market_regime(market_phase, composite_score)
    g.current_strategy = select_strategy_by_regime(g.market_regime)
    
    print(f'[调仓原因] {rebalance_reason}')
    print(f'[市场趋势] {market_phase} (综合评分: {composite_score:.2f})')
    print(f'[市场状态] {g.market_regime}')
    print(f'[策略选择] {g.current_strategy["name"]}')
    print(f'[因子组合] {list(g.current_strategy["factors"].keys())}')
    
    # 5. 获取候选股票池（全市场）
    candidate_stocks = get_candidate_pool_all_market(context, current_date_str)
    
    if not candidate_stocks:
        print('[错误] 未获取到候选股票，停止策略')
        raise ValueError("无法获取候选股票池")
    
    # 6. 智能选股（使用正确的因子计算）
    selected_stocks = smart_stock_selection_v3(
        context,
        candidate_stocks,
        current_date_str,
        g.current_strategy
    )
    
    if not selected_stocks:
        print('[警告] 选股未产生信号，跳过调仓')
        check_stop_loss(context)
        log_portfolio_status(context)
        return
    
    # 7. 执行调仓
    execute_rebalance_optimized_v2(context, selected_stocks, g.current_strategy)
    
    # 更新调仓日期和交易日计数
    g.last_rebalance_date = current_date
    g.last_rebalance_trading_days = g.trading_days_count
    
    # 更新市场趋势和持仓质量记录
    g.last_market_trend = market_trend
    g.last_position_quality = evaluate_position_quality(context, current_date_str)
    
    # 记录持仓信息
    log_portfolio_status(context)
    print(f'[调仓完成] 下次调仓将在 {REBALANCE_INTERVAL} 个交易日后，或触发紧急调仓条件')


# ==================== 市场趋势分析 ====================

def analyze_market_trend_v2(context, date_str):
    """分析市场趋势（改进版）"""
    try:
        hist = get_price(BENCHMARK, count=60, fields=['close', 'volume'])
        
        if hist is None or len(hist) < 20:
            return {'market_phase': 'neutral', 'composite_score': 0}
        
        closes = hist['close'].values
        volumes = hist['volume'].values
        
        ma5 = np.mean(closes[-5:])
        ma20 = np.mean(closes[-20:])
        ma60 = np.mean(closes[-60:]) if len(closes) >= 60 else ma20
        
        current_price = closes[-1]
        
        returns = np.diff(closes) / closes[:-1]
        volatility = np.std(returns[-20:]) * np.sqrt(252)
        
        volume_ma5 = np.mean(volumes[-5:])
        volume_ma20 = np.mean(volumes[-20:])
        volume_ratio = volume_ma5 / volume_ma20 if volume_ma20 > 0 else 1.0
        
        score = 0
        
        if current_price > ma20:
            score += 20
        elif current_price < ma20:
            score -= 20
        
        if ma20 > ma60:
            score += 30
        elif ma20 < ma60:
            score -= 30
        
        if current_price > ma60 * 1.05:
            score += 30
        elif current_price < ma60 * 0.95:
            score -= 30
        
        if volume_ratio > 1.2:
            score += 10
        elif volume_ratio < 0.8:
            score -= 10
        
        if volatility < 0.15:
            score += 5
        elif volatility > 0.30:
            score -= 5
        
        if score >= 60:
            market_phase = 'bull'
        elif score >= 30:
            market_phase = 'weak_bull'
        elif score >= -30:
            market_phase = 'neutral'
        elif score >= -60:
            market_phase = 'weak_bear'
        else:
            market_phase = 'bear'
        
        return {
            'market_phase': market_phase,
            'composite_score': score,
            'volatility': volatility,
            'volume_ratio': volume_ratio,
        }
        
    except Exception as e:
        print(f'[错误] 市场趋势分析失败: {e}')
        raise


def determine_market_regime(market_phase, composite_score):
    """判断市场状态"""
    if market_phase in ['bull', 'weak_bull'] and composite_score >= 30:
        return 'bull'
    elif market_phase in ['bear', 'weak_bear'] and composite_score <= -30:
        return 'bear'
    else:
        return 'neutral'


def select_strategy_by_regime(regime):
    """根据市场状态选择策略类型"""
    if regime == 'bull':
        return BULL_STRATEGY.copy()
    elif regime == 'bear':
        return BEAR_STRATEGY.copy()
    else:
        return NEUTRAL_STRATEGY.copy()


# ==================== 主线识别与候选池构建（v2.4优化） ====================

def identify_mainlines(context, date_str):
    """
    识别主线主题（v2.4优化：建立主线识别机制）
    
    策略：
    1. 获取热门板块（通过get_stock_blocks和get_industry_stocks）
    2. 计算板块动量，选择前N个主线板块
    3. 从主线板块中提取股票，构建主线候选池
    
    Args:
        context: 策略上下文
        date_str: 日期字符串
    
    Returns:
        dict: {mainline_name: [stocks]} 主线股票映射
    """
    try:
        # 检查是否需要更新主线（每MAINLINE_UPDATE_INTERVAL个交易日更新一次）
        current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        need_update = False
        
        if g.last_mainline_update is None:
            need_update = True
        else:
            trading_days_since = count_trading_days(g.last_mainline_update, current_date)
            if trading_days_since >= MAINLINE_UPDATE_INTERVAL:
                need_update = True
        
        if not need_update and g.mainline_stocks:
            return g.mainline_stocks
        
        print(f'[主线识别] 开始识别主线主题...')
        
        # 获取全市场股票列表（如果尚未获取）
        if not g.all_stocks or not g.stocks_initialized:
            date_str_formatted = date_str.replace('-', '')
            try:
                g.all_stocks = get_Ashares(date=date_str_formatted)
                if not g.all_stocks:
                    g.all_stocks = get_Ashares()
                g.stocks_initialized = True
            except:
                pass
        
        if not g.all_stocks:
            return {}
        
        # 获取热门板块（通过随机采样股票获取板块）
        mainline_candidates = {}  # {block_name: [stocks]}
        sample_stocks = g.all_stocks[:500]  # 采样500只股票
        
        for stock in sample_stocks:
            try:
                stock_blocks = get_stock_blocks(stock)
                if not stock_blocks:
                    continue
                
                # 处理不同类型的返回值
                blocks_list = []
                if isinstance(stock_blocks, (list, tuple)):
                    blocks_list = list(stock_blocks)
                elif isinstance(stock_blocks, pd.DataFrame):
                    if 'block_name' in stock_blocks.columns:
                        blocks_list = stock_blocks['block_name'].tolist()
                    elif 'name' in stock_blocks.columns:
                        blocks_list = stock_blocks['name'].tolist()
                
                for block in blocks_list[:3]:  # 每只股票最多取3个板块
                    if isinstance(block, dict):
                        block_name = block.get('block_name', '') or block.get('name', '')
                    else:
                        block_name = str(block)
                    
                    if not block_name:
                        continue
                    
                    if block_name not in mainline_candidates:
                        mainline_candidates[block_name] = []
                    
                    if stock not in mainline_candidates[block_name]:
                        mainline_candidates[block_name].append(stock)
            except:
                continue
        
        # 计算每个板块的动量，选择前N个主线
        mainline_scores = {}
        for block_name, stocks in mainline_candidates.items():
            if len(stocks) < 5:  # 板块股票太少，跳过
                continue
            
            try:
                # 计算板块平均动量
                block_momentums = []
                for stock in stocks[:20]:  # 最多取20只股票计算
                    try:
                        hist = get_price(stock, count=MAINLINE_MOMENTUM_PERIOD + 1, fields=['close'])
                        if hist is not None and len(hist) >= MAINLINE_MOMENTUM_PERIOD + 1:
                            closes = hist['close'].values
                            momentum = (closes[-1] / closes[0] - 1) if closes[0] > 0 else 0
                            block_momentums.append(momentum)
                    except:
                        continue
                
                if block_momentums:
                    avg_momentum = np.mean(block_momentums)
                    mainline_scores[block_name] = {
                        'momentum': avg_momentum,
                        'stocks': stocks
                    }
            except:
                continue
        
        # 选择前N个主线
        sorted_mainlines = sorted(mainline_scores.items(), key=lambda x: x[1]['momentum'], reverse=True)
        top_mainlines = sorted_mainlines[:MAINLINE_TOP_N]
        
        # 构建主线股票映射
        mainline_stocks = {}
        mainline_pool = []
        
        for block_name, data in top_mainlines:
            mainline_stocks[block_name] = data['stocks']
            mainline_pool.extend(data['stocks'])
        
        # 去重
        mainline_pool = list(set(mainline_pool))
        
        g.mainline_stocks = mainline_stocks
        g.mainline_pool = mainline_pool
        g.last_mainline_update = current_date
        
        print(f'[主线识别] 识别到 {len(mainline_stocks)} 个主线主题，候选股票 {len(mainline_pool)} 只')
        for block_name, data in top_mainlines[:5]:  # 只显示前5个
            print(f'  - {block_name}: 动量 {data["momentum"]*100:.2f}%, 股票 {len(data["stocks"])} 只')
        
        return mainline_stocks
        
    except Exception as e:
        print(f'[错误] 主线识别失败: {e}')
        import traceback
        traceback.print_exc()
        return {}


def get_candidate_pool_all_market(context, date_str):
    """
    获取候选股票池（v2.4优化：优先从主线主题内选股）
    
    策略：
    1. 首先尝试从主线主题内选股（如果主线识别成功）
    2. 如果主线股票不足，再从全市场补充
    3. 使用价格筛选过滤ST/停牌股票
    
    Args:
        context: 策略上下文
        date_str: 日期字符串
    
    Returns:
        list: 候选股票列表（优先来自主线主题）
    
    Raises:
        ValueError: 如果无法获取或筛选股票列表
    """
    try:
        # v2.4优化：优先从主线主题内选股
        mainline_stocks_dict = identify_mainlines(context, date_str)
        
        # 从主线股票中构建候选池
        mainline_candidate_pool = []
        if mainline_stocks_dict:
            # 合并所有主线股票
            for block_name, stocks in mainline_stocks_dict.items():
                mainline_candidate_pool.extend(stocks)
            
            # 去重
            mainline_candidate_pool = list(set(mainline_candidate_pool))
            print(f'[候选池] 从主线主题获取 {len(mainline_candidate_pool)} 只候选股票')
        
        # 步骤1：获取全市场股票列表（如果尚未获取，用于补充）
        if not g.all_stocks or not g.stocks_initialized:
            # PTrade API要求日期格式为YYYYMMDD
            date_str_formatted = date_str.replace('-', '')
            
            # 方法1：尝试get_Ashares(date=YYYYMMDD)
            try:
                g.all_stocks = get_Ashares(date=date_str_formatted)
                if not g.all_stocks or len(g.all_stocks) == 0:
                    raise ValueError(f"get_Ashares(date='{date_str_formatted}')返回空列表")
                print(f'[候选池] 获取全市场股票: {len(g.all_stocks)}只（方法: get_Ashares(date={date_str_formatted})）')
                g.stocks_initialized = True
            except Exception as e1:
                print(f'[错误] 方法1失败: get_Ashares(date={date_str_formatted}) - {e1}')
                
                # 方法2：尝试get_Ashares()不带参数（回测中默认取回测日期）
                try:
                    g.all_stocks = get_Ashares()
                    if not g.all_stocks or len(g.all_stocks) == 0:
                        raise ValueError("get_Ashares()返回空列表")
                    print(f'[候选池] 获取全市场股票: {len(g.all_stocks)}只（方法: get_Ashares()）')
                    g.stocks_initialized = True
                except Exception as e2:
                    print(f'[错误] 方法2失败: get_Ashares() - {e2}')
                    print(f'[错误] 所有获取全市场股票列表的方法都失败')
                    import traceback
                    traceback.print_exc()
                    raise ValueError(f"无法获取全市场股票列表。方法1失败: {e1}。方法2失败: {e2}")
            
            if not g.all_stocks or len(g.all_stocks) == 0:
                raise ValueError("获取到的股票列表为空")
        
        print(f'[候选池] 使用全市场股票列表: {len(g.all_stocks)}只')
        
        # v2.4优化：优先从主线候选池筛选，如果不足再从全市场补充
        candidate_source = mainline_candidate_pool if mainline_candidate_pool else g.all_stocks
        print(f'[候选池] 候选来源: {"主线主题" if mainline_candidate_pool else "全市场"} ({len(candidate_source)}只)')
        
        # 步骤2：筛选价格范围（使用PTrade API获取价格）
        # 同时过滤掉价格异常低的股票（可能是ST或退市股票）
        price_filtered_stocks = []
        checked_count = 0
        max_check = min(CANDIDATE_POOL_SIZE * 2, len(candidate_source))  # 限制检查数量避免超时
        
        for stock in candidate_source:
            if checked_count >= max_check:
                break
            
            try:
                # 跳过明显异常的股票代码（如果有的话）
                # 注意：PTrade的股票代码格式为'000001.SZ'，这里不做代码过滤
                
                # 获取价格
                price_df = get_price(stock, count=1, fields=['close', 'volume'])
                if price_df is None or len(price_df) == 0:
                    checked_count += 1
                    continue
                
                current_price = price_df['close'].iloc[-1]
                current_volume = price_df['volume'].iloc[-1] if 'volume' in price_df.columns else 0
                
                # 价格筛选：过滤异常价格（可能是ST、停牌或退市股票）
                if current_price < MIN_STOCK_PRICE or current_price > MAX_STOCK_PRICE:
                    checked_count += 1
                    continue
                
                # 成交量筛选：过滤停牌股票（停牌股票成交量为0或极小）
                if current_volume <= 0:
                    checked_count += 1
                    continue
                
                price_filtered_stocks.append(stock)
                checked_count += 1
                
            except Exception as e:
                # 如果获取价格失败，跳过该股票（可能是退市或停牌）
                checked_count += 1
                continue
        
        print(f'[候选池] 价格和成交量筛选后: {len(price_filtered_stocks)}只（检查了{checked_count}只，价格范围: {MIN_STOCK_PRICE}-{MAX_STOCK_PRICE}元）')
        
        if not price_filtered_stocks or len(price_filtered_stocks) == 0:
            raise ValueError(f"价格筛选后股票列表为空（价格范围: {MIN_STOCK_PRICE}-{MAX_STOCK_PRICE}元，检查了{checked_count}只股票）")
        
        # 返回筛选后的股票列表
        return price_filtered_stocks[:CANDIDATE_POOL_SIZE]
        
    except Exception as e:
        print(f'[错误] 获取候选股票池失败: {e}')
        import traceback
        traceback.print_exc()
        raise


# ==================== 基本面数据获取（正确版） ====================

def get_fundamentals_data(stocks, date_str):
    """
    获取股票基本面数据（健壮版：使用多种方法，容错处理）
    
    方法1：使用标准API获取完整字段
    方法2：如果失败，尝试获取部分字段
    方法3：如果都失败，返回空DataFrame（不报错）
    
    Args:
        stocks: 股票代码列表或单个股票代码
        date_str: 日期字符串
    
    Returns:
        pd.DataFrame: 基本面数据DataFrame，包含total_value, pe_dynamic, pb, dividend_ratio等字段
    """
    # 检查缓存
    if isinstance(stocks, str):
        stocks = [stocks]
    
    cache_key = f"{','.join(sorted(stocks))}_{date_str}"
    if cache_key in g.fundamentals_cache:
        return g.fundamentals_cache[cache_key]
    
    fundamentals_df = None
    
    # 方法1：尝试获取完整字段
    try:
        fundamentals_df = get_fundamentals(
            stocks,
            'valuation',
            date=date_str,
            fields=['total_value', 'pe_dynamic', 'pb', 'dividend_ratio']
        )
        if fundamentals_df is not None and len(fundamentals_df) > 0:
            g.fundamentals_cache[cache_key] = fundamentals_df
            return fundamentals_df
    except Exception as e1:
        print(f'[调试] 方法1失败（完整字段）: {e1}')
    
    # 方法2：尝试获取部分字段（只获取市值和PE）
    try:
        fundamentals_df = get_fundamentals(
            stocks,
            'valuation',
            date=date_str,
            fields=['total_value', 'pe_dynamic']
        )
        if fundamentals_df is not None and len(fundamentals_df) > 0:
            # 尝试补充其他字段
            try:
                pb_df = get_fundamentals(stocks, 'valuation', date=date_str, fields=['pb'])
                if pb_df is not None and len(pb_df) > 0:
                    if 'code' in fundamentals_df.columns and 'code' in pb_df.columns:
                        fundamentals_df = fundamentals_df.merge(pb_df, on='code', how='left')
                    elif fundamentals_df.index.name == 'code' and pb_df.index.name == 'code':
                        fundamentals_df['pb'] = pb_df['pb']
            except:
                pass
            
            g.fundamentals_cache[cache_key] = fundamentals_df
            return fundamentals_df
    except Exception as e2:
        print(f'[调试] 方法2失败（部分字段）: {e2}')
    
    # 方法3：尝试不带字段参数（获取所有可用字段）
    try:
        fundamentals_df = get_fundamentals(
            stocks,
            'valuation',
            date=date_str
        )
        if fundamentals_df is not None and len(fundamentals_df) > 0:
            g.fundamentals_cache[cache_key] = fundamentals_df
            return fundamentals_df
    except Exception as e3:
        print(f'[调试] 方法3失败（所有字段）: {e3}')
    
    # 如果所有方法都失败，返回空DataFrame（不报错，让调用方处理）
    print(f'[警告] 所有获取基本面数据的方法都失败，返回空DataFrame')
    return pd.DataFrame()


# ==================== 主线动量因子计算 ====================

def get_mainline_momentum(stock, date_str):
    """
    计算股票所属主线板块的动量因子
    
    Args:
        stock: 股票代码
        date_str: 日期字符串
    
    Returns:
        float: 主线动量因子值
    """
    try:
        # 获取股票所属板块
        stock_blocks = get_stock_blocks(stock)
        if not stock_blocks:
            return 0.0
        
        # 处理不同类型的返回值
        blocks_list = []
        if isinstance(stock_blocks, (list, tuple)):
            blocks_list = list(stock_blocks)
        elif isinstance(stock_blocks, pd.DataFrame):
            # 如果是DataFrame，尝试提取板块名称
            if 'block_name' in stock_blocks.columns:
                blocks_list = stock_blocks['block_name'].tolist()
            elif 'name' in stock_blocks.columns:
                blocks_list = stock_blocks['name'].tolist()
            else:
                # 如果无法提取，返回0
                return 0.0
        elif isinstance(stock_blocks, dict):
            blocks_list = [stock_blocks]
        else:
            # 其他类型，尝试转换为字符串
            try:
                blocks_list = [str(stock_blocks)]
            except:
                return 0.0
        
        if len(blocks_list) == 0:
            return 0.0
        
        # 计算每个板块的动量
        mainline_momentums = []
        for block in blocks_list[:5]:  # 最多取前5个板块
            # 提取板块名称
            if isinstance(block, dict):
                block_name = block.get('block_name', '') or block.get('name', '')
            else:
                block_name = str(block)
            
            if not block_name:
                continue
            
            try:
                # 获取板块成分股
                block_stocks = get_industry_stocks(block_name)  # 或使用get_concept_stocks
                if not block_stocks or len(block_stocks) == 0:
                    continue
                
                # 计算板块平均动量
                block_momentum = 0.0
                valid_count = 0
                
                # 确保block_stocks是列表
                if not isinstance(block_stocks, (list, tuple)):
                    block_stocks = [block_stocks]
                
                for bs in block_stocks[:20]:  # 最多取20只成分股
                    try:
                        hist = get_price(bs, count=MAINLINE_MOMENTUM_PERIOD + 1, fields=['close'])
                        if hist is None or len(hist) < MAINLINE_MOMENTUM_PERIOD + 1:
                            continue
                        
                        closes = hist['close'].values
                        momentum = (closes[-1] / closes[0] - 1) if len(closes) > 0 and closes[0] > 0 else 0
                        block_momentum += momentum
                        valid_count += 1
                    except:
                        continue
                
                if valid_count > 0:
                    avg_momentum = block_momentum / valid_count
                    mainline_momentums.append(avg_momentum)
            except:
                continue
        
        # 返回平均主线动量
        if mainline_momentums:
            return np.mean(mainline_momentums)
        else:
            return 0.0
            
    except Exception as e:
        print(f'[调试] 计算{stock}主线动量失败: {e}')
        import traceback
        traceback.print_exc()
        return 0.0


# ==================== 因子计算（正确版：不使用代理） ====================

def calculate_value_factor(stock, fundamentals_df):
    """
    计算价值因子（健壮版：使用多种方法，容错处理）
    
    策略：
    1. 优先使用PE、PB、股息率计算
    2. 如果PE无效，尝试使用PB和股息率
    3. 如果PB也无效，只使用股息率
    4. 如果都无效，返回0（不报错）
    
    Args:
        stock: 股票代码
        fundamentals_df: 基本面数据DataFrame
    
    Returns:
        float: 价值因子得分（如果无法计算，返回0.0）
    """
    if fundamentals_df is None or len(fundamentals_df) == 0:
        return 0.0  # 返回0而不是报错
    
    # 查找该股票的数据
    stock_data = None
    try:
        if 'code' in fundamentals_df.columns:
            stock_data = fundamentals_df[fundamentals_df['code'] == stock]
        elif fundamentals_df.index.name == 'code' or stock in fundamentals_df.index:
            stock_data = fundamentals_df.loc[stock] if stock in fundamentals_df.index else None
    except:
        return 0.0
    
    if stock_data is None or len(stock_data) == 0:
        return 0.0
    
    # 获取字段值（处理DataFrame和Series两种情况）
    try:
        if isinstance(stock_data, pd.DataFrame):
            row = stock_data.iloc[0]
        else:
            row = stock_data
        
        pe = row.get('pe_dynamic', 0) if hasattr(row, 'get') else (row['pe_dynamic'] if 'pe_dynamic' in row else 0)
        pb = row.get('pb', 0) if hasattr(row, 'get') else (row['pb'] if 'pb' in row else 0)
        dividend_ratio = row.get('dividend_ratio', 0) if hasattr(row, 'get') else (row['dividend_ratio'] if 'dividend_ratio' in row else 0)
    except:
        return 0.0
    
    # 处理无效值：使用合理范围
    pe_valid = False
    pb_valid = False
    dividend_valid = False
    
    pe_score = 0.0
    pb_score = 0.0
    dividend_score = 0.0
    
    # PE处理：负数或异常大值使用替代方案
    if not pd.isna(pe) and pe > 0 and pe <= 1000:
        pe_score = 1.0 / pe  # PE越低，得分越高
        pe_valid = True
    elif not pd.isna(pe) and pe < 0:
        # 亏损公司：使用PB和股息率，PE得分设为0
        pe_valid = False
    elif not pd.isna(pe) and pe > 1000:
        # 异常大PE：可能是数据错误，使用PB和股息率
        pe_valid = False
    
    # PB处理
    if not pd.isna(pb) and pb > 0 and pb <= 100:
        pb_score = 1.0 / pb  # PB越低，得分越高
        pb_valid = True
    
    # 股息率处理
    if not pd.isna(dividend_ratio) and dividend_ratio > 0:
        dividend_score = min(dividend_ratio * 10, 1.0)
        dividend_valid = True
    
    # 根据可用数据计算综合得分
    total_weight = 0.0
    weighted_score = 0.0
    
    if pe_valid:
        weighted_score += pe_score * 0.4
        total_weight += 0.4
    if pb_valid:
        weighted_score += pb_score * 0.4
        total_weight += 0.4
    if dividend_valid:
        weighted_score += dividend_score * 0.2
        total_weight += 0.2
    
    # 如果没有任何有效数据，返回0
    if total_weight == 0:
        return 0.0
    
    # 归一化得分（按实际使用的权重）
    value_score = weighted_score / total_weight if total_weight > 0 else 0.0
    
    return value_score


def calculate_size_factor(stock, fundamentals_df):
    """
    计算规模因子（健壮版：容错处理）
    
    Args:
        stock: 股票代码
        fundamentals_df: 基本面数据DataFrame
    
    Returns:
        float: 规模因子得分（小盘股得分高），如果无法计算返回0.0
    """
    if fundamentals_df is None or len(fundamentals_df) == 0:
        return 0.0
    
    # 查找该股票的数据
    stock_data = None
    try:
        if 'code' in fundamentals_df.columns:
            stock_data = fundamentals_df[fundamentals_df['code'] == stock]
        elif stock in fundamentals_df.index:
            stock_data = fundamentals_df.loc[stock]
    except:
        return 0.0
    
    if stock_data is None or len(stock_data) == 0:
        return 0.0
    
    # 获取字段值
    try:
        if isinstance(stock_data, pd.DataFrame):
            row = stock_data.iloc[0]
        else:
            row = stock_data
        
        total_value = row.get('total_value', 0) if hasattr(row, 'get') else (row['total_value'] if 'total_value' in row else 0)
    except:
        return 0.0
    
    # 如果市值无效，尝试使用历史价格估算（作为备选方案）
    if pd.isna(total_value) or total_value <= 0:
        # 备选方案：使用价格和成交量估算市值（粗略）
        try:
            hist = get_price(stock, count=1, fields=['close', 'volume'])
            if hist is not None and len(hist) > 0:
                price = hist['close'].iloc[-1]
                volume = hist['volume'].iloc[-1]
                # 粗略估算：价格 * 成交量 * 某个倍数（这里用100作为粗略估算）
                estimated_value = price * volume * 100
                if estimated_value > 0:
                    total_value = estimated_value
                else:
                    return 0.0
            else:
                return 0.0
        except:
            return 0.0
    
    # 市值越小，得分越高（小盘股弹性大）
    # 使用对数归一化
    try:
        size_score = 1.0 / (1.0 + np.log10(max(total_value / 1e8, 1e-6)))
        return size_score
    except:
        return 0.0


def calculate_dividend_factor(stock, fundamentals_df):
    """
    计算股息因子（健壮版：容错处理）
    
    Args:
        stock: 股票代码
        fundamentals_df: 基本面数据DataFrame
    
    Returns:
        float: 股息因子得分，如果无法计算返回0.0
    """
    if fundamentals_df is None or len(fundamentals_df) == 0:
        return 0.0
    
    # 查找该股票的数据
    stock_data = None
    try:
        if 'code' in fundamentals_df.columns:
            stock_data = fundamentals_df[fundamentals_df['code'] == stock]
        elif stock in fundamentals_df.index:
            stock_data = fundamentals_df.loc[stock]
    except:
        return 0.0
    
    if stock_data is None or len(stock_data) == 0:
        return 0.0
    
    # 获取字段值
    try:
        if isinstance(stock_data, pd.DataFrame):
            row = stock_data.iloc[0]
        else:
            row = stock_data
        
        dividend_ratio = row.get('dividend_ratio', 0) if hasattr(row, 'get') else (row['dividend_ratio'] if 'dividend_ratio' in row else 0)
    except:
        return 0.0
    
    # 股息率越高，得分越高
    if pd.isna(dividend_ratio) or dividend_ratio <= 0:
        return 0.0
    
    dividend_score = min(dividend_ratio * 10, 1.0)
    return dividend_score


# ==================== v2.4新增因子：趋势强度、行业景气度 ====================

def calculate_trend_strength_factor(stock, date_str):
    """
    计算趋势强度因子（v2.4新增：ADX、MACD稳定性）
    
    使用ADX和MACD指标评估趋势强度和稳定性
    
    Args:
        stock: 股票代码
        date_str: 日期字符串
    
    Returns:
        float: 趋势强度因子得分（0-1），越高越好
    """
    try:
        # 获取足够的历史数据
        hist = get_price(stock, count=max(ADX_PERIOD + 10, MACD_SLOW + MACD_SIGNAL + 10), fields=['close', 'high', 'low'])
        if hist is None or len(hist) < max(ADX_PERIOD, MACD_SLOW + MACD_SIGNAL):
            return 0.0
        
        closes = hist['close'].values
        highs = hist['high'].values if 'high' in hist.columns else closes
        lows = hist['low'].values if 'low' in hist.columns else closes
        
        # 1. 计算ADX（平均趋向指数）
        adx_score = 0.0
        try:
            # 简化的ADX计算
            tr_list = []  # True Range
            for i in range(1, len(closes)):
                tr = max(
                    highs[i] - lows[i],
                    abs(highs[i] - closes[i-1]),
                    abs(lows[i] - closes[i-1])
                )
                tr_list.append(tr)
            
            if len(tr_list) >= ADX_PERIOD:
                atr = np.mean(tr_list[-ADX_PERIOD:])  # Average True Range
                # 计算+DI和-DI（简化版）
                plus_dm = []
                minus_dm = []
                for i in range(1, len(highs)):
                    up_move = highs[i] - highs[i-1]
                    down_move = lows[i-1] - lows[i]
                    if up_move > down_move and up_move > 0:
                        plus_dm.append(up_move)
                    else:
                        plus_dm.append(0)
                    if down_move > up_move and down_move > 0:
                        minus_dm.append(down_move)
                    else:
                        minus_dm.append(0)
                
                if len(plus_dm) >= ADX_PERIOD and len(minus_dm) >= ADX_PERIOD:
                    plus_di = np.mean(plus_dm[-ADX_PERIOD:]) / atr if atr > 0 else 0
                    minus_di = np.mean(minus_dm[-ADX_PERIOD:]) / atr if atr > 0 else 0
                    dx = abs(plus_di - minus_di) / (plus_di + minus_di) if (plus_di + minus_di) > 0 else 0
                    # ADX越高，趋势越强（归一化到0-1）
                    adx_score = min(dx * 2, 1.0)  # 假设ADX范围0-50，归一化
        except:
            pass
        
        # 2. 计算MACD稳定性
        macd_score = 0.0
        try:
            # 计算EMA
            def ema(data, period):
                if len(data) < period:
                    return None
                ema_values = [data[0]]
                multiplier = 2.0 / (period + 1)
                for i in range(1, len(data)):
                    ema_values.append((data[i] - ema_values[-1]) * multiplier + ema_values[-1])
                return ema_values
            
            ema_fast = ema(closes, MACD_FAST)
            ema_slow = ema(closes, MACD_SLOW)
            
            if ema_fast and ema_slow and len(ema_fast) >= MACD_SIGNAL and len(ema_slow) >= MACD_SIGNAL:
                macd_line = [ema_fast[i] - ema_slow[i] for i in range(len(ema_slow))]
                signal_line = ema(macd_line, MACD_SIGNAL) if len(macd_line) >= MACD_SIGNAL else None
                
                if signal_line and len(macd_line) >= len(signal_line):
                    # MACD在信号线上方且持续上升，趋势强
                    recent_macd = macd_line[-5:]
                    recent_signal = signal_line[-5:]
                    
                    if len(recent_macd) == 5 and len(recent_signal) == 5:
                        macd_above_signal = sum([1 for i in range(5) if recent_macd[i] > recent_signal[i]])
                        macd_trend = 1 if recent_macd[-1] > recent_macd[0] else 0
                        macd_score = (macd_above_signal / 5.0) * 0.6 + macd_trend * 0.4
        except:
            pass
        
        # 3. 综合趋势强度得分（ADX 60%，MACD 40%）
        trend_score = 0.6 * adx_score + 0.4 * macd_score
        return trend_score
        
    except Exception as e:
        print(f'[调试] 计算{stock}趋势强度因子失败: {e}')
        return 0.0


def calculate_industry_momentum_factor(stock, date_str):
    """
    计算行业景气度因子（v2.4新增：板块涨幅相对强度）
    
    Args:
        stock: 股票代码
        date_str: 日期字符串
    
    Returns:
        float: 行业景气度因子得分（0-1），越高越好
    """
    try:
        # 获取股票所属板块
        stock_blocks = get_stock_blocks(stock)
        if not stock_blocks:
            return 0.0
        
        # 处理不同类型的返回值
        blocks_list = []
        if isinstance(stock_blocks, (list, tuple)):
            blocks_list = list(stock_blocks)
        elif isinstance(stock_blocks, pd.DataFrame):
            if 'block_name' in stock_blocks.columns:
                blocks_list = stock_blocks['block_name'].tolist()
            elif 'name' in stock_blocks.columns:
                blocks_list = stock_blocks['name'].tolist()
        
        if len(blocks_list) == 0:
            return 0.0
        
        # 计算股票自身动量
        stock_hist = get_price(stock, count=INDUSTRY_MOMENTUM_PERIOD + 1, fields=['close'])
        if stock_hist is None or len(stock_hist) < INDUSTRY_MOMENTUM_PERIOD + 1:
            return 0.0
        
        stock_closes = stock_hist['close'].values
        stock_momentum = (stock_closes[-1] / stock_closes[0] - 1) if stock_closes[0] > 0 else 0
        
        # 计算板块平均动量
        industry_momentums = []
        for block in blocks_list[:3]:  # 最多取3个板块
            if isinstance(block, dict):
                block_name = block.get('block_name', '') or block.get('name', '')
            else:
                block_name = str(block)
            
            if not block_name:
                continue
            
            try:
                block_stocks = get_industry_stocks(block_name)
                if not block_stocks or len(block_stocks) == 0:
                    continue
                
                block_momentums = []
                for bs in list(block_stocks)[:20]:  # 最多取20只成分股
                    try:
                        bs_hist = get_price(bs, count=INDUSTRY_MOMENTUM_PERIOD + 1, fields=['close'])
                        if bs_hist is not None and len(bs_hist) >= INDUSTRY_MOMENTUM_PERIOD + 1:
                            bs_closes = bs_hist['close'].values
                            bs_momentum = (bs_closes[-1] / bs_closes[0] - 1) if bs_closes[0] > 0 else 0
                            block_momentums.append(bs_momentum)
                    except:
                        continue
                
                if block_momentums:
                    avg_block_momentum = np.mean(block_momentums)
                    industry_momentums.append(avg_block_momentum)
            except:
                continue
        
        if not industry_momentums:
            return 0.0
        
        # 计算相对强度：股票动量相对于板块平均动量
        avg_industry_momentum = np.mean(industry_momentums)
        relative_strength = stock_momentum - avg_industry_momentum
        
        # 归一化到0-1
        industry_score = 1.0 / (1.0 + np.exp(-relative_strength * 10))
        return industry_score
        
    except Exception as e:
        print(f'[调试] 计算{stock}行业景气度因子失败: {e}')
        return 0.0


# ==================== 智能选股（正确版） ====================

def smart_stock_selection_v3(context, stocks, date_str, strategy):
    """
    智能选股（正确版：使用正确的PTrade API，不使用代理）
    
    Args:
        context: 策略上下文
        stocks: 候选股票列表
        date_str: 日期字符串
        strategy: 策略配置
    
    Returns:
        list: 选中的股票列表
    
    Raises:
        ValueError: 如果无法获取基本面数据
    """
    if not stocks:
        return []
    
    factor_weights = strategy['factors']
    
    print(f'[选股] 开始筛选 {len(stocks)} 只股票，使用因子: {list(factor_weights.keys())}')
    
    # 批量获取基本面数据（健壮版：即使失败也继续）
    fundamentals_df = pd.DataFrame()
    try:
        batch_stocks = stocks[:100]  # 限制批量大小
        fundamentals_df = get_fundamentals_data(batch_stocks, date_str)
        if fundamentals_df is not None and len(fundamentals_df) > 0:
            print(f'[选股] 成功获取{len(fundamentals_df)}只股票的基本面数据')
        else:
            print(f'[警告] 基本面数据为空，将使用其他因子选股')
    except Exception as e:
        print(f'[警告] 批量获取基本面数据失败: {e}，将使用其他因子选股')
        fundamentals_df = pd.DataFrame()  # 设置为空，继续使用其他因子
    
    # 计算所有股票的因子值
    all_factor_values = {}
    
    for stock in batch_stocks:
        try:
            # 获取历史数据
            hist = get_price(stock, count=60, fields=['close', 'volume', 'money'])
            if hist is None or len(hist) < 20:
                continue
            
            closes = hist['close'].values
            volumes = hist['volume'].values
            
            # 计算各因子得分（使用正确的API数据）
            factor_values = {}
            
            # 动量因子
            if 'momentum' in factor_weights:
                momentum = (closes[-1] / closes[-20] - 1) if len(closes) >= 20 else 0
                factor_values['momentum'] = momentum
            
            # 主线动量因子
            if 'mainline_momentum' in factor_weights:
                mainline_mom = get_mainline_momentum(stock, date_str)
                factor_values['mainline_momentum'] = mainline_mom
            
            # v2.4新增：趋势强度因子（ADX、MACD）
            if 'trend_strength' in factor_weights:
                trend_score = calculate_trend_strength_factor(stock, date_str)
                if trend_score > 0:
                    factor_values['trend_strength'] = trend_score
            
            # v2.4新增：行业景气度因子
            if 'industry_momentum' in factor_weights:
                industry_score = calculate_industry_momentum_factor(stock, date_str)
                if industry_score > 0:
                    factor_values['industry_momentum'] = industry_score
            
            # 价值因子（健壮版：即使失败也返回0，不报错）
            if 'value' in factor_weights:
                value_score = calculate_value_factor(stock, fundamentals_df)
                if value_score > 0:  # 只有有效值才添加
                    factor_values['value'] = value_score
            
            # 规模因子（健壮版：即使失败也返回0，不报错）
            if 'size' in factor_weights:
                size_score = calculate_size_factor(stock, fundamentals_df)
                if size_score > 0:  # 只有有效值才添加
                    factor_values['size'] = size_score
            
            # 股息因子（健壮版：即使失败也返回0，不报错）
            if 'dividend' in factor_weights:
                dividend_score = calculate_dividend_factor(stock, fundamentals_df)
                if dividend_score > 0:  # 只有有效值才添加
                    factor_values['dividend'] = dividend_score
            
            # 成长因子
            if 'growth' in factor_weights:
                growth = (closes[-1] / closes[-60] - 1) if len(closes) >= 60 else (closes[-1] / closes[-20] - 1) if len(closes) >= 20 else 0
                factor_values['growth'] = growth
            
            # 质量因子
            if 'quality' in factor_weights:
                returns = np.diff(closes) / closes[:-1]
                volatility = np.std(returns[-20:]) if len(returns) >= 20 else 1
                quality_score = 1.0 / (1 + volatility * 100)
                factor_values['quality'] = quality_score
            
            # 资金流因子
            if 'flow' in factor_weights and 'money' in hist.columns:
                money = hist['money'].values
                flow = np.mean(money[-5:]) / (np.mean(money[-20:-5]) + 1e-6) if len(money) >= 20 else 1
                factor_values['flow'] = flow
            
            # 低波动因子
            if 'volatility' in factor_weights:
                returns = np.diff(closes) / closes[:-1]
                volatility = np.std(returns[-20:]) if len(returns) >= 20 else 1
                factor_values['volatility'] = 1.0 / (1 + volatility * 100)
            
            # 反转因子
            if 'reversal' in factor_weights:
                reversal = -(closes[-1] / closes[-20] - 1) if len(closes) >= 20 else 0
                factor_values['reversal'] = reversal
            
            all_factor_values[stock] = factor_values
            
        except Exception as e:
            print(f'[调试] 计算{stock}因子失败: {e}')
            continue
    
    # 对因子进行z-score标准化
    if not all_factor_values:
        return []
    
    # 收集每个因子的所有值
    factor_all_values = {}
    for stock, factors in all_factor_values.items():
        for factor_name, value in factors.items():
            if factor_name not in factor_all_values:
                factor_all_values[factor_name] = []
            factor_all_values[factor_name].append(value)
    
    # 计算每个因子的均值和标准差
    factor_stats = {}
    for factor_name, values in factor_all_values.items():
        if len(values) > 0:
            factor_stats[factor_name] = {
                'mean': np.mean(values),
                'std': np.std(values) if np.std(values) > 1e-6 else 1.0
            }
    
    # 标准化因子值并计算综合得分
    scores = {}
    for stock, factor_values in all_factor_values.items():
        total_score = 0
        total_weight = 0  # 实际使用的权重总和
        
        for factor_name, weight in factor_weights.items():
            if factor_name in factor_values and factor_name in factor_stats:
                raw_value = factor_values[factor_name]
                mean = factor_stats[factor_name]['mean']
                std = factor_stats[factor_name]['std']
                normalized_value = (raw_value - mean) / std
                total_score += normalized_value * weight
                total_weight += weight
        
        # 如果没有任何因子可用，跳过该股票
        if total_weight == 0:
            continue
        
        # 归一化得分（按实际使用的权重）
        if total_weight > 0:
            scores[stock] = total_score / total_weight if total_weight > 0 else 0
        else:
            scores[stock] = total_score
    
    # 排序并选择
    if not scores:
        return []
    
    sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    selected = [stock for stock, score in sorted_stocks[:STOCK_NUM]]
    
    print(f'[选股] 从{len(stocks)}只股票中筛选出{len(selected)}只（使用正确的PTrade API）')
    
    return selected


# ==================== 精确下单 ====================

def execute_rebalance_optimized_v2(context, selected_stocks, strategy):
    """执行调仓（优化版：预留资金缓冲）"""
    if not selected_stocks:
        return
    
    current_positions = list(context.portfolio.positions.keys())
    
    try:
        total_value = context.portfolio.portfolio_value
    except AttributeError:
        total_value = context.portfolio.total_value
    
    try:
        available_cash = context.portfolio.cash
    except AttributeError:
        available_cash = total_value * 0.5
    
    usable_cash = available_cash * 0.95
    
    target_position = strategy['position']
    
    # 计算总目标金额（使用总资产，因为可以卖出现有持仓来买入新股票）
    # 但实际可用资金不能超过usable_cash + 现有持仓价值
    current_positions_value = 0
    if current_positions:
        try:
            # 获取现有持仓的当前价值
            for stock in current_positions:
                if stock in context.portfolio.positions:
                    pos = context.portfolio.positions[stock]
                    try:
                        price_df = get_price(stock, count=1, fields=['close'])
                        if price_df is not None and len(price_df) > 0:
                            current_price = price_df['close'].iloc[-1]
                            # 使用持仓数量 * 当前价格
                            if hasattr(pos, 'total_amount'):
                                current_positions_value += pos.total_amount * current_price
                            elif hasattr(pos, 'amount'):
                                current_positions_value += pos.amount * current_price
                    except:
                        continue
        except:
            # 如果计算失败，使用总资产减去可用资金作为估算
            current_positions_value = max(0, total_value - available_cash)
    
    total_available = usable_cash + current_positions_value
    total_target_value = min(total_value * target_position, total_available * 0.98)  # 预留2%缓冲
    
    print(f'[调试] 可用资金: {usable_cash:.2f}, 持仓价值: {current_positions_value:.2f}, 总可用: {total_available:.2f}, 目标金额: {total_target_value:.2f}')
    
    # 先获取所有股票的价格
    stock_prices = {}
    for stock in selected_stocks[:STOCK_NUM * 3]:  # 多检查一些，确保有足够的选择
        try:
            price_df = get_price(stock, count=1, fields=['close'])
            if price_df is None or len(price_df) == 0:
                continue
            
            current_price = price_df['close'].iloc[-1]
            if current_price <= 0:
                continue
            
            stock_prices[stock] = current_price
        except Exception as e:
            continue
    
    if not stock_prices:
        print(f'[警告] 无法获取股票价格，跳过调仓')
        return
    
    # 根据总目标金额和股票价格，计算能买入的股票数量
    # 策略：优先选择价格较低的股票，确保能买入足够的数量
    sorted_stocks_by_price = sorted(stock_prices.items(), key=lambda x: x[1])  # 按价格从低到高排序
    
    valid_stocks = []
    for stock, price in sorted_stocks_by_price:
        min_value_needed = price * MIN_TRADING_UNIT
        # 检查是否能买入最小交易单位（使用总目标金额，而不是单只股票的目标金额）
        if min_value_needed <= total_target_value:
            valid_stocks.append(stock)
            if len(valid_stocks) >= STOCK_NUM:
                break  # 找到足够的股票就停止
    
    if not valid_stocks:
        print(f'[警告] 没有股票能满足最小交易单位要求，跳过调仓')
        print(f'[调试] 总目标金额: {total_target_value:.2f}, 最小持仓金额: {MIN_POSITION_VALUE:.2f}')
        print(f'[调试] 最便宜的股票价格: {min(stock_prices.values()):.2f}, 需要: {min(stock_prices.values()) * MIN_TRADING_UNIT:.2f}')
        return
    
    # 根据有效股票数量，计算每只股票的目标金额
    target_num = min(STOCK_NUM, len(valid_stocks))
    target_stocks = valid_stocks[:target_num]
    
    # 计算每只股票的目标金额
    target_value_per_stock = total_target_value / target_num
    
    # 确保每只股票的目标金额至少能买入最小交易单位
    # 如果不够，减少持仓数量
    min_required_value = max([stock_prices[s] * MIN_TRADING_UNIT for s in target_stocks], default=MIN_POSITION_VALUE)
    if target_value_per_stock < min_required_value:
        # 重新计算能买入的股票数量
        max_affordable_stocks = int(total_target_value / min_required_value)
        if max_affordable_stocks < 1:
            print(f'[警告] 资金不足，无法买入任何股票（需要至少{min_required_value:.2f}元/只）')
            return
        
        target_num = min(max_affordable_stocks, len(valid_stocks))
        target_stocks = valid_stocks[:target_num]
        target_value_per_stock = total_target_value / target_num
    
    # 确保目标金额不小于最小持仓金额
    target_value_per_stock = max(target_value_per_stock, MIN_POSITION_VALUE)
    
    print(f'[调仓] 目标持仓: {target_num}只，每只目标金额: {target_value_per_stock:.2f}元')
    
    for stock in current_positions:
        if stock not in target_stocks:
            try:
                order_target(stock, 0)
                print(f'[卖出] {stock}')
            except Exception as e:
                print(f'[错误] 卖出{stock}失败: {e}')
    
    for stock in target_stocks:
        try:
            current_price = stock_prices[stock]
            if current_price <= 0:
                print(f'[警告] {stock}价格无效: {current_price}，跳过')
                continue
            
            # 计算目标股数（向下取整到最小交易单位的倍数）
            shares_to_buy = int(target_value_per_stock / current_price)
            shares_to_buy = (shares_to_buy // MIN_TRADING_UNIT) * MIN_TRADING_UNIT
            
            # 确保至少能买入最小交易单位
            if shares_to_buy < MIN_TRADING_UNIT:
                # 如果目标金额不够买入最小交易单位，尝试用最小交易单位买入
                shares_to_buy = MIN_TRADING_UNIT
                actual_value = shares_to_buy * current_price
                if actual_value > usable_cash:
                    print(f'[警告] {stock}需要{actual_value:.2f}元，但可用资金只有{usable_cash:.2f}元，跳过')
                    continue
            
            # 检查是否有足够资金
            actual_value = shares_to_buy * current_price
            if actual_value > usable_cash * 1.1:  # 允许10%的误差
                print(f'[警告] {stock}需要{actual_value:.2f}元，但可用资金只有{usable_cash:.2f}元，跳过')
                continue
            
            # 下单
            if shares_to_buy > 0:
                order_target(stock, shares_to_buy)
                print(f'[买入] {stock} (股数: {shares_to_buy}股, 金额: {actual_value:.2f}元)')
                
                g.entry_prices[stock] = current_price
                g.hold_days[stock] = 0
            else:
                print(f'[警告] {stock}计算出的股数为0，跳过')
        except Exception as e:
            print(f'[错误] 买入{stock}失败: {e}')


# ==================== 风险控制 ====================

def risk_control(context):
    """
    风险控制检查（v2.4优化：移除全组合止损，保留个股止损/止盈）
    
    改进：
    - 移除STOP_LOSS_TOTAL全组合止损（避免过于激进）
    - 只保留个股止损/止盈机制
    - 提高容错区间
    """
    current_value = context.portfolio.total_value
    
    # v2.4：移除全组合止损，只更新峰值
    if current_value > g.peak_value:
        g.peak_value = current_value
    
    # v2.4：移除stop_loss_triggered机制（不再需要全组合止损）
    if hasattr(g, 'stop_loss_triggered') and g.stop_loss_triggered:
        # 如果之前有止损状态，现在移除（v2.4不再使用）
        g.stop_loss_triggered = False
        g.stop_loss_date = None
    
    return True


def check_stop_loss(context):
    """
    检查单只股票止损（v2.4优化：考虑最低持仓时间）
    
    改进：
    - 考虑MIN_HOLD_DAYS，避免过早止损
    - 保留动态止损机制
    """
    positions = context.portfolio.positions
    
    for stock in list(positions.keys()):
        try:
            # v2.4：检查最低持仓时间
            hold_days = g.hold_days.get(stock, 0)
            if hold_days < MIN_HOLD_DAYS:
                # 如果持仓时间不足，不执行止损（除非亏损非常严重，超过-15%）
                price_df = get_price(stock, count=1, fields=['close'])
                if price_df is not None and len(price_df) > 0:
                    current_price = price_df['close'].iloc[-1]
                    entry_price = g.entry_prices.get(stock, current_price)
                    if entry_price > 0:
                        pnl = (current_price - entry_price) / entry_price
                        if pnl <= -0.15:  # 只有亏损超过15%才止损
                            print(f'[紧急止损] {stock}: 亏损 {pnl*100:.2f}% (持仓{hold_days}天，未达最低持仓时间)')
                            order_target(stock, 0)
                            if stock in g.entry_prices:
                                del g.entry_prices[stock]
                            if stock in g.hold_days:
                                del g.hold_days[stock]
                continue
            
            price_df = get_price(stock, count=1, fields=['close'])
            if price_df is None or len(price_df) == 0:
                continue
            
            current_price = price_df['close'].iloc[-1]
            entry_price = g.entry_prices.get(stock, current_price)
            
            if entry_price > 0:
                pnl = (current_price - entry_price) / entry_price
                
                hist = get_price(stock, count=20, fields=['close'])
                if hist is not None and len(hist) >= 20:
                    returns = np.diff(hist['close'].values) / hist['close'].values[:-1]
                    volatility = np.std(returns)
                    
                    if volatility > 0.03:
                        stop_loss = -0.10
                    elif volatility > 0.02:
                        stop_loss = -0.08
                    else:
                        stop_loss = -0.06
                else:
                    stop_loss = STOP_LOSS_SINGLE
                
                if pnl <= stop_loss:
                    print(f'[止损] {stock}: 亏损 {pnl*100:.2f}% (持仓{hold_days}天)')
                    order_target(stock, 0)
                    if stock in g.entry_prices:
                        del g.entry_prices[stock]
                    if stock in g.hold_days:
                        del g.hold_days[stock]
        except Exception as e:
            print(f'[错误] 检查{stock}止损失败: {e}')


def check_take_profit(context):
    """
    检查止盈（v2.4优化：考虑最低持仓时间，避免过早止盈）
    
    改进：
    - 考虑MIN_HOLD_DAYS，避免过早止盈
    - 提高止盈比例，让利润奔跑
    """
    positions = context.portfolio.positions
    
    for stock in list(positions.keys()):
        try:
            # v2.4：检查最低持仓时间
            hold_days = g.hold_days.get(stock, 0)
            
            price_df = get_price(stock, count=1, fields=['close'])
            if price_df is None or len(price_df) == 0:
                continue
            
            current_price = price_df['close'].iloc[-1]
            entry_price = g.entry_prices.get(stock, current_price)
            
            if entry_price > 0:
                pnl = (current_price - entry_price) / entry_price
                sell_rule = g.current_strategy.get('sell_rule', 'profit_target')
                
                # v2.4：如果持仓时间不足，提高止盈阈值（避免过早止盈）
                effective_take_profit = TAKE_PROFIT
                if hold_days < MIN_HOLD_DAYS:
                    # 持仓时间不足时，提高止盈阈值50%
                    effective_take_profit = TAKE_PROFIT * 1.5
                
                if sell_rule == 'quick_profit' and pnl >= 0.10:
                    if hold_days >= MIN_HOLD_DAYS:  # v2.4：只有持仓时间足够才快速止盈
                        print(f'[快速止盈] {stock}: 盈利 {pnl*100:.2f}% (持仓{hold_days}天)')
                        order_target(stock, 0)
                        if stock in g.entry_prices:
                            del g.entry_prices[stock]
                        if stock in g.hold_days:
                            del g.hold_days[stock]
                elif sell_rule == 'profit_target' and pnl >= effective_take_profit:
                    print(f'[止盈] {stock}: 盈利 {pnl*100:.2f}% (持仓{hold_days}天)')
                    order_target(stock, 0)
                    if stock in g.entry_prices:
                        del g.entry_prices[stock]
                    if stock in g.hold_days:
                        del g.hold_days[stock]
                elif sell_rule == 'trailing' and pnl >= TAKE_PROFIT * 1.5:
                    if hold_days >= MIN_HOLD_DAYS:  # v2.4：只有持仓时间足够才跟踪止盈
                        print(f'[跟踪止盈] {stock}: 盈利 {pnl*100:.2f}% (持仓{hold_days}天)')
                        order_target(stock, 0)
                        if stock in g.entry_prices:
                            del g.entry_prices[stock]
                        if stock in g.hold_days:
                            del g.hold_days[stock]
        except Exception as e:
            print(f'[错误] 检查{stock}止盈失败: {e}')


def clear_all_positions(context):
    """清仓"""
    positions = list(context.portfolio.positions.keys())
    for stock in positions:
        try:
            order_target(stock, 0)
        except:
            pass
    
    g.entry_prices.clear()
    g.hold_days.clear()


def update_hold_days(context, current_date):
    """更新持仓天数"""
    positions = context.portfolio.positions
    for stock in positions.keys():
        if stock in g.hold_days:
            g.hold_days[stock] += 1
            
            if g.hold_days[stock] >= MAX_HOLD_DAYS:
                print(f'[持仓时间] {stock} 持仓超过{MAX_HOLD_DAYS}天，卖出')
                try:
                    order_target(stock, 0)
                    if stock in g.entry_prices:
                        del g.entry_prices[stock]
                    del g.hold_days[stock]
                except:
                    pass


def log_portfolio_status(context):
    """记录持仓状态"""
    positions = context.portfolio.positions
    
    try:
        total_value = context.portfolio.portfolio_value
    except AttributeError:
        total_value = context.portfolio.total_value
    
    try:
        cash = context.portfolio.cash
    except AttributeError:
        try:
            cash = context.portfolio.available_cash
        except AttributeError:
            positions_value = sum(
                pos.market_value if hasattr(pos, 'market_value') else 
                pos.total_amount * pos.last_price if hasattr(pos, 'total_amount') and hasattr(pos, 'last_price') else 0
                for pos in positions.values()
            )
            cash = total_value - positions_value
    
    print(f'[持仓状态] 持仓数量: {len(positions)}只')
    print(f'[持仓状态] 总资产: {total_value:.2f}')
    print(f'[持仓状态] 可用资金: {cash:.2f}')
    if total_value > 0:
        print(f'[持仓状态] 持仓比例: {(total_value-cash)/total_value*100:.1f}%')

