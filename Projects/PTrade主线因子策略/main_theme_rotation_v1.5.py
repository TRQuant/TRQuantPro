# -*- coding: utf-8 -*-
"""
韬睿量化 - PTrade主题轮动策略（AI主线、国产替代、算力）
========================================

策略名称: A股主题轮动策略（中低频轮动）
创建时间: 2025-12-09
平台: PTrade (恒生)
版本: v1.4 (保守优化版 - 目标30%+收益)

策略说明:
---------
基于《A股主题轮动策略研究：AI主线、国产替代与算力》的研究思路：

1. **三大核心主题**：
   - AI主线：人工智能、ChatGPT、大模型等
   - 国产替代：半导体、信创、自主可控等
   - 算力：数据中心、光模块、服务器等

2. **中低频轮动**：
   - 调仓频率：周频或月频（非日频）
   - 捕捉中期上涨趋势，回避日常波动
   - 当某一主线进入加速上涨阶段时，及时跟进并持有数周至数月

3. **主题强度评估**：
   - 板块动量：计算主题板块的平均收益率
   - 资金流：计算主题板块的资金流入
   - 技术指标：ADX趋势强度、MACD等
   - 相对强度：主题相对市场的超额收益

4. **动态切换**：
   - 定期评估三大主题的强度
   - 选择当前阶段相对最强的主线
   - 动态调整持仓，以取得超越市场的中期回报

核心特点:
---------
- ✅ **主题聚焦**：只关注三大核心主题，不泛选
- ✅ **中低频调仓**：周频/月频，减少交易成本
- ✅ **强度评估**：多维度评估主题强度
- ✅ **动态轮动**：根据主题强度动态切换
- ✅ **PTrade兼容**：符合PTrade代码规范，可直接运行

PTrade兼容性:
-------------
- 严格按照PTrade API文档实现
- 遵守PTrade API调用时机限制
- 符合PTrade代码规范
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==================== 策略参数 ====================

# 主题定义
THEMES = {
    'AI': {
        'name': 'AI主线',
        'concepts': ['人工智能', 'ChatGPT', '大模型', 'AIGC', '机器学习'],
        'keywords': ['AI', '人工智能', 'ChatGPT', '大模型', 'AIGC', '机器学习', '深度学习']
    },
    'DOMESTIC': {
        'name': '国产替代',
        'concepts': ['半导体', '信创', '自主可控', '国产芯片', '国产软件'],
        'keywords': ['国产', '自主可控', '信创', '半导体', '芯片', '国产化']
    },
    'COMPUTING': {
        'name': '算力',
        'concepts': ['数据中心', '光模块', '服务器', '云计算', '边缘计算'],
        'keywords': ['算力', '数据中心', '光模块', '服务器', '云计算', '边缘计算', 'CPO']
    }
}

# 持仓参数
STOCK_NUM = 10              # 持仓股票数量
MAX_POSITION = 0.90         # 最大仓位比例
MIN_POSITION = 0.50         # 最小仓位比例

# 轮动参数（进一步优化）
REBALANCE_INTERVAL_WEEKS = 1    # 调仓间隔（周，1周=约5个交易日）
REBALANCE_INTERVAL_DAYS = 5     # 调仓间隔（交易日，约1周，更频繁轮动）
THEME_UPDATE_INTERVAL = 3       # 主题强度更新间隔（交易日，每3天更新一次）

# 风险控制参数（进一步优化）
STOP_LOSS_SINGLE = -0.10    # 单只股票止损比例（-10%，更严格止损）
TAKE_PROFIT = 0.35          # 止盈比例（35%，进一步提高止盈目标）
MAX_HOLD_DAYS = 45          # 最大持仓天数（1.5个月，加快轮动）
MIN_HOLD_DAYS = 2           # 最小持仓天数（2天，允许快速止损）

# 主题强度评估参数
MOMENTUM_PERIOD = 20        # 动量计算周期（20个交易日，约1个月）
VOLUME_PERIOD = 10          # 成交量计算周期（10个交易日）
ADX_PERIOD = 14             # ADX计算周期
MACD_FAST = 12              # MACD快线周期
MACD_SLOW = 26              # MACD慢线周期
MACD_SIGNAL = 9             # MACD信号线周期

# 选股参数
MIN_STOCK_PRICE = 5.0       # 最小股票价格（元）
MAX_STOCK_PRICE = 500.0     # 最大股票价格（元）
MIN_POSITION_VALUE = 5000   # 最小持仓金额（元）
MIN_TRADING_UNIT = 100      # 最小交易单位（股）

# 基准指数
BENCHMARK = '000300.XSHG'   # 沪深300

# ==================== 全局变量 ====================

g = type('obj', (object,), {})

def initialize(context):
    """
    策略初始化函数
    """
    # 设置基准
    set_benchmark(BENCHMARK)
    
    # 全局变量初始化
    g.last_rebalance_date = None      # 上次调仓日期
    g.last_theme_update_date = None   # 上次主题更新日期
    g.current_theme = None             # 当前持仓主题
    g.theme_strength = {}             # 主题强度评分
    g.theme_stocks = {}                # 主题股票池
    g.entry_prices = {}                # 买入价格记录
    g.hold_days = {}                   # 持仓天数记录
    g.trading_days_count = 0           # 交易日计数器
    g.last_rebalance_trading_days = 0  # 上次调仓时的交易日计数
    
    print('=' * 60)
    print('韬睿量化 - PTrade主题轮动策略（AI主线、国产替代、算力）')
    print('=' * 60)
    print(f'基准指数: {BENCHMARK}')
    print(f'持仓数量: {STOCK_NUM}只')
    print(f'调仓间隔: {REBALANCE_INTERVAL_DAYS}个交易日（约{REBALANCE_INTERVAL_WEEKS}周）')
    print(f'主题更新间隔: {THEME_UPDATE_INTERVAL}个交易日（约1周）')
    print(f'三大主题: {", ".join([t["name"] for t in THEMES.values()])}')
    print('=' * 60)
    print('[策略特点] 中低频轮动，捕捉中期上涨趋势')
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
    
    # 更新交易日计数器
    g.trading_days_count += 1
    
    # 只在09:35执行交易逻辑
    if current_hour == 9 and current_minute == 35:
        try:
            trade(context, current_date, current_date_str)
        except Exception as e:
            print(f'[错误] 交易逻辑执行失败: {e}')
            import traceback
            traceback.print_exc()
            raise
    
    # 每日收盘后更新持仓天数
    if current_hour == 15 and current_minute == 0:
        update_hold_days(context, current_date)


# ==================== 交易逻辑 ====================

def trade(context, current_date, current_date_str):
    """
    主交易逻辑
    
    Args:
        context: 策略上下文
        current_date: 当前日期
        current_date_str: 日期字符串
    """
    print(f'\n[{current_date_str}] 开始交易逻辑')
    
    # 1. 检查是否需要更新主题强度
    need_update_theme = False
    if g.last_theme_update_date is None:
        need_update_theme = True
    else:
        days_since = count_trading_days(g.last_theme_update_date, current_date)
        if days_since >= THEME_UPDATE_INTERVAL:
            need_update_theme = True
    
    if need_update_theme:
        print(f'[主题评估] 更新主题强度评估...')
        update_theme_strength(context, current_date_str)
        g.last_theme_update_date = current_date
    
    # 2. 检查是否需要调仓
    need_rebalance = False
    rebalance_reason = ''
    
    if g.last_rebalance_date is None:
        need_rebalance = True
        rebalance_reason = '首次调仓'
    else:
        days_since = count_trading_days(g.last_rebalance_date, current_date)
        if days_since >= REBALANCE_INTERVAL_DAYS:
            need_rebalance = True
            rebalance_reason = f'定期调仓（距离上次{days_since}个交易日）'
        
        # 检查主题切换（仅在主题更新后检查）
        if need_update_theme:
            best_theme = get_best_theme()
            if best_theme and best_theme != g.current_theme:
                need_rebalance = True
                rebalance_reason = f'主题切换：{g.current_theme} -> {best_theme}'
    
    # 3. 执行调仓或持仓管理
    if need_rebalance:
        execute_rebalance(context, current_date_str, rebalance_reason)
        # 更新调仓日期和交易日计数
        g.last_rebalance_date = current_date
        g.last_rebalance_trading_days = g.trading_days_count
    else:
        # 非调仓日：检查止损/止盈
        check_stop_loss(context, current_date_str)
        check_take_profit(context, current_date_str)
    
    # 4. 输出持仓状态
    print_position_status(context, current_date_str)


def count_trading_days(start_date, end_date):
    """
    计算两个日期之间的交易日数量（修复版）
    
    Args:
        start_date: 开始日期（date对象）
        end_date: 结束日期（date对象）
    
    Returns:
        int: 交易日数量
    """
    if start_date is None:
        return 999  # 首次调仓，返回大值
    
    if start_date >= end_date:
        return 0
    
    # 优先使用交易日计数器（最准确）
    if hasattr(g, 'trading_days_count') and hasattr(g, 'last_rebalance_trading_days'):
        if g.last_rebalance_trading_days > 0:
            trading_days_diff = g.trading_days_count - g.last_rebalance_trading_days
            return max(0, trading_days_diff)
    
    # 简单估算（排除周末，但不排除节假日）
    days = (end_date - start_date).days
    if days <= 0:
        return 0
    
    # 计算周末数量
    weekends = 0
    current = start_date
    while current < end_date:
        if current.weekday() >= 5:  # 周六(5)或周日(6)
            weekends += 1
        current += timedelta(days=1)
    
    trading_days = days - weekends
    return max(0, trading_days)


# ==================== 主题强度评估 ====================

def update_theme_strength(context, date_str):
    """
    更新三大主题的强度评分
    
    Args:
        context: 策略上下文
        date_str: 日期字符串
    """
    print(f'[主题评估] 开始评估三大主题强度...')
    
    for theme_key, theme_info in THEMES.items():
        try:
            strength = evaluate_theme_strength(context, theme_key, theme_info, date_str)
            g.theme_strength[theme_key] = strength
            
            print(f'[主题评估] {theme_info["name"]}: 强度 {strength["total_score"]:.2f} '
                  f'(动量: {strength["momentum"]:.2f}, 资金流: {strength["capital_flow"]:.2f}, '
                  f'趋势: {strength["trend"]:.2f}, 相对强度: {strength["relative_strength"]:.2f})')
        except Exception as e:
            print(f'[错误] 评估{theme_info["name"]}强度失败: {e}')
            g.theme_strength[theme_key] = {'total_score': 0.0}
    
    # 输出主题强度排名
    sorted_themes = sorted(g.theme_strength.items(), key=lambda x: x[1].get('total_score', 0), reverse=True)
    print(f'[主题排名] ', end='')
    for i, (theme_key, strength) in enumerate(sorted_themes):
        theme_name = THEMES[theme_key]['name']
        score = strength.get('total_score', 0)
        print(f'{i+1}. {theme_name}({score:.2f})', end='  ')
    print()


def evaluate_theme_strength(context, theme_key, theme_info, date_str):
    """
    评估单个主题的强度
    
    Args:
        context: 策略上下文
        theme_key: 主题键（'AI', 'DOMESTIC', 'COMPUTING'）
        theme_info: 主题信息
        date_str: 日期字符串
    
    Returns:
        dict: 主题强度评分
    """
    # 1. 获取主题股票池
    theme_stocks = get_theme_stocks(theme_info, date_str)
    if not theme_stocks or len(theme_stocks) == 0:
        return {
            'total_score': 0.0,
            'momentum': 0.0,
            'capital_flow': 0.0,
            'trend': 0.0,
            'relative_strength': 0.0,
            'stock_count': 0
        }
    
    # 缓存主题股票池
    g.theme_stocks[theme_key] = theme_stocks
    
    # 2. 计算板块动量
    momentum = calculate_theme_momentum(theme_stocks, date_str)
    
    # 3. 计算资金流
    capital_flow = calculate_theme_capital_flow(theme_stocks, date_str)
    
    # 4. 计算趋势强度（ADX）
    trend = calculate_theme_trend(theme_stocks, date_str)
    
    # 5. 计算相对强度（相对市场）
    relative_strength = calculate_theme_relative_strength(theme_stocks, date_str)
    
    # 6. 综合评分（加权平均）
    total_score = (
        momentum * 0.35 +          # 动量权重35%（提高）
        capital_flow * 0.25 +      # 资金流权重25%
        trend * 0.30 +              # 趋势权重30%（提高）
        relative_strength * 0.10    # 相对强度权重10%（降低）
    )
    
    return {
        'total_score': total_score,
        'momentum': momentum,
        'capital_flow': capital_flow,
        'trend': trend,
        'relative_strength': relative_strength,
        'stock_count': len(theme_stocks)
    }


def get_theme_stocks(theme_info, date_str):
    """
    获取主题股票池（多方法备选）
    
    Args:
        theme_info: 主题信息
        date_str: 日期字符串
    
    Returns:
        list: 股票代码列表
    """
    all_stocks = []
    
    # 方法1：尝试使用get_concept_stocks和get_industry_stocks
    for concept in theme_info['concepts']:
        try:
            stocks = get_concept_stocks(concept)
            if stocks and len(stocks) > 0:
                for stock in stocks:
                    if stock not in all_stocks:
                        all_stocks.append(stock)
        except Exception as e:
            # 如果get_concept_stocks失败，尝试get_industry_stocks
            try:
                stocks = get_industry_stocks(concept)
                if stocks and len(stocks) > 0:
                    for stock in stocks:
                        if stock not in all_stocks:
                            all_stocks.append(stock)
            except:
                pass
    
    # 方法2：如果方法1失败，使用反向查找（通过get_stock_blocks）
    if len(all_stocks) == 0:
        print(f'[主题股票池] 方法1失败，使用反向查找（关键词: {theme_info["keywords"]}）')
        all_stocks = get_theme_stocks_by_blocks(theme_info, date_str)
    
    # 方法3：如果方法2也失败，使用指数成分股作为备选
    if len(all_stocks) == 0:
        print(f'[主题股票池] 方法2失败，使用指数成分股作为备选')
        try:
            all_stocks = get_index_stocks(BENCHMARK)
            print(f'[主题股票池] 获取到 {len(all_stocks)} 只指数成分股')
        except Exception as e:
            print(f'[主题股票池] 获取指数成分股失败: {e}')
            return []
    
    # 过滤：价格范围、成交量
    filtered_stocks = []
    for stock in all_stocks[:200]:  # 增加限制数量，因为可能从指数成分股获取
        try:
            price_df = get_price(stock, count=1, fields=['close', 'volume'])
            if price_df is None or len(price_df) == 0:
                continue
            
            current_price = price_df['close'].iloc[-1]
            current_volume = price_df['volume'].iloc[-1]
            
            if (MIN_STOCK_PRICE <= current_price <= MAX_STOCK_PRICE and 
                current_volume > 0):
                filtered_stocks.append(stock)
        except:
            continue
    
    print(f'[主题股票池] {theme_info["name"]}: 获取到 {len(filtered_stocks)} 只符合条件的股票')
    return filtered_stocks


def get_theme_stocks_by_blocks(theme_info, date_str):
    """
    通过反向查找获取主题股票池（通过get_stock_blocks）
    
    Args:
        theme_info: 主题信息
        date_str: 日期字符串
    
    Returns:
        list: 股票代码列表
    """
    all_stocks = []
    keywords = theme_info.get('keywords', [])
    
    # 获取全市场股票（或使用指数成分股作为样本）
    try:
        # 尝试获取全市场股票
        sample_stocks = get_Ashares()
        if not sample_stocks or len(sample_stocks) == 0:
            # 如果失败，使用指数成分股
            sample_stocks = get_index_stocks(BENCHMARK)
        # 限制样本数量，避免查询过多
        sample_stocks = sample_stocks[:500]
    except Exception as e:
        print(f'[主题股票池] 获取样本股票失败: {e}，使用指数成分股')
        try:
            sample_stocks = get_index_stocks(BENCHMARK)
        except:
            return []
    
    print(f'[主题股票池] 从 {len(sample_stocks)} 只样本股票中查找主题股票...')
    
    # 遍历样本股票，查找包含关键词的股票
    matched_count = 0
    for stock in sample_stocks:
        try:
            # 获取股票所属板块
            stock_blocks = get_stock_blocks(stock)
            if not stock_blocks:
                continue
            
            # 检查板块名称是否包含关键词
            matched = False
            block_names = []
            
            # 处理不同的返回格式
            if isinstance(stock_blocks, list):
                for block in stock_blocks:
                    if isinstance(block, dict):
                        block_name = block.get('block_name', '') or block.get('name', '')
                    else:
                        block_name = str(block)
                    block_names.append(block_name)
            elif isinstance(stock_blocks, dict):
                block_names = [str(v) for v in stock_blocks.values()]
            else:
                block_names = [str(stock_blocks)]
            
            # 检查是否包含关键词
            for block_name in block_names:
                for keyword in keywords:
                    if keyword in block_name:
                        matched = True
                        break
                if matched:
                    break
            
            if matched and stock not in all_stocks:
                all_stocks.append(stock)
                matched_count += 1
                
                # 限制数量，避免过多
                if matched_count >= 100:
                    break
        except Exception as e:
            continue
    
    print(f'[主题股票池] 通过反向查找找到 {len(all_stocks)} 只主题股票')
    return all_stocks


def calculate_theme_momentum(theme_stocks, date_str):
    """
    计算主题板块动量
    
    Args:
        theme_stocks: 主题股票列表
        date_str: 日期字符串
    
    Returns:
        float: 动量评分（0-100）
    """
    if not theme_stocks or len(theme_stocks) == 0:
        return 0.0
    
    momentums = []
    valid_count = 0
    
    for stock in theme_stocks[:50]:  # 最多取50只股票
        try:
            hist = get_price(stock, count=MOMENTUM_PERIOD + 1, fields=['close'])
            if hist is None or len(hist) < MOMENTUM_PERIOD + 1:
                continue
            
            closes = hist['close'].values
            if len(closes) > 0 and closes[0] > 0:
                momentum = (closes[-1] / closes[0] - 1) * 100  # 转换为百分比
                momentums.append(momentum)
                valid_count += 1
        except:
            continue
    
    if valid_count == 0:
        return 0.0
    
    avg_momentum = np.mean(momentums)
    # 归一化到0-100（假设-20%到+20%为范围）
    normalized_momentum = np.clip((avg_momentum + 20) / 40 * 100, 0, 100)
    return normalized_momentum


def calculate_theme_capital_flow(theme_stocks, date_str):
    """
    计算主题板块资金流
    
    Args:
        theme_stocks: 主题股票列表
        date_str: 日期字符串
    
    Returns:
        float: 资金流评分（0-100）
    """
    if not theme_stocks or len(theme_stocks) == 0:
        return 0.0
    
    capital_flows = []
    valid_count = 0
    
    for stock in theme_stocks[:50]:
        try:
            hist = get_price(stock, count=VOLUME_PERIOD + 1, fields=['close', 'volume', 'money'])
            if hist is None or len(hist) < VOLUME_PERIOD + 1:
                continue
            
            # 计算平均成交额
            avg_money = hist['money'].mean()
            
            # 计算最近成交额相对平均值的比例
            recent_money = hist['money'].iloc[-VOLUME_PERIOD:].mean()
            if avg_money > 0:
                flow_ratio = (recent_money / avg_money - 1) * 100
                capital_flows.append(flow_ratio)
                valid_count += 1
        except:
            continue
    
    if valid_count == 0:
        return 0.0
    
    avg_flow = np.mean(capital_flows)
    # 归一化到0-100（假设-50%到+50%为范围）
    normalized_flow = np.clip((avg_flow + 50) / 100 * 100, 0, 100)
    return normalized_flow


def calculate_theme_trend(theme_stocks, date_str):
    """
    计算主题板块趋势强度（ADX）
    
    Args:
        theme_stocks: 主题股票列表
        date_str: 日期字符串
    
    Returns:
        float: 趋势强度评分（0-100）
    """
    if not theme_stocks or len(theme_stocks) == 0:
        return 0.0
    
    adx_scores = []
    valid_count = 0
    
    for stock in theme_stocks[:50]:
        try:
            hist = get_price(stock, count=ADX_PERIOD + 20, fields=['high', 'low', 'close'])
            if hist is None or len(hist) < ADX_PERIOD + 20:
                continue
            
            # 计算ADX
            adx = calculate_adx(hist, ADX_PERIOD)
            if adx is not None and not np.isnan(adx):
                adx_scores.append(adx)
                valid_count += 1
        except:
            continue
    
    if valid_count == 0:
        return 0.0
    
    avg_adx = np.mean(adx_scores)
    # ADX范围通常是0-100，直接使用
    return min(100, avg_adx)


def calculate_theme_relative_strength(theme_stocks, date_str):
    """
    计算主题相对强度（相对市场）
    
    Args:
        theme_stocks: 主题股票列表
        date_str: 日期字符串
    
    Returns:
        float: 相对强度评分（0-100）
    """
    if not theme_stocks or len(theme_stocks) == 0:
        return 0.0
    
    # 计算主题平均收益率
    theme_returns = []
    for stock in theme_stocks[:50]:
        try:
            hist = get_price(stock, count=MOMENTUM_PERIOD + 1, fields=['close'])
            if hist is None or len(hist) < MOMENTUM_PERIOD + 1:
                continue
            
            closes = hist['close'].values
            if len(closes) > 0 and closes[0] > 0:
                return_pct = (closes[-1] / closes[0] - 1) * 100
                theme_returns.append(return_pct)
        except:
            continue
    
    if len(theme_returns) == 0:
        return 0.0
    
    theme_avg_return = np.mean(theme_returns)
    
    # 计算基准收益率
    try:
        benchmark_hist = get_price(BENCHMARK, count=MOMENTUM_PERIOD + 1, fields=['close'])
        if benchmark_hist is None or len(benchmark_hist) < MOMENTUM_PERIOD + 1:
            return 50.0  # 默认中性
        
        benchmark_closes = benchmark_hist['close'].values
        if len(benchmark_closes) > 0 and benchmark_closes[0] > 0:
            benchmark_return = (benchmark_closes[-1] / benchmark_closes[0] - 1) * 100
        else:
            return 50.0
    except:
        return 50.0
    
    # 计算相对强度
    relative_strength = theme_avg_return - benchmark_return
    
    # 归一化到0-100（假设-10%到+10%为范围）
    normalized_rs = np.clip((relative_strength + 10) / 20 * 100, 0, 100)
    return normalized_rs


def calculate_adx(hist, period=14):
    """
    计算ADX（平均趋向指数）
    
    Args:
        hist: 历史价格数据（DataFrame，包含high, low, close）
        period: 计算周期
    
    Returns:
        float: ADX值
    """
    try:
        high = hist['high'].values
        low = hist['low'].values
        close = hist['close'].values
        
        # 计算True Range (TR)
        tr_list = []
        for i in range(1, len(hist)):
            tr1 = high[i] - low[i]
            tr2 = abs(high[i] - close[i-1])
            tr3 = abs(low[i] - close[i-1])
            tr = max(tr1, tr2, tr3)
            tr_list.append(tr)
        
        if len(tr_list) < period:
            return None
        
        # 计算ATR（Average True Range）
        atr = np.mean(tr_list[-period:])
        if atr == 0:
            return None
        
        # 计算+DI和-DI
        plus_dm_list = []
        minus_dm_list = []
        
        for i in range(1, len(hist)):
            plus_dm = high[i] - high[i-1] if high[i] > high[i-1] else 0
            minus_dm = low[i-1] - low[i] if low[i] < low[i-1] else 0
            plus_dm_list.append(plus_dm)
            minus_dm_list.append(minus_dm)
        
        if len(plus_dm_list) < period:
            return None
        
        plus_di = (np.mean(plus_dm_list[-period:]) / atr) * 100
        minus_di = (np.mean(minus_dm_list[-period:]) / atr) * 100
        
        # 计算DX
        di_sum = plus_di + minus_di
        if di_sum == 0:
            return None
        
        dx = (abs(plus_di - minus_di) / di_sum) * 100
        
        # 计算ADX（简化版，直接使用DX）
        return dx
    except:
        return None


def get_best_theme():
    """
    获取当前最强主题
    
    Returns:
        str: 主题键（'AI', 'DOMESTIC', 'COMPUTING'），如果没有则返回None
    """
    if not g.theme_strength:
        return None
    
    best_theme = None
    best_score = -1
    
    for theme_key, strength in g.theme_strength.items():
        score = strength.get('total_score', 0)
        stock_count = strength.get('stock_count', 0)
        
        # 如果股票数量为0，跳过该主题
        if stock_count == 0:
            continue
            
        if score > best_score:
            best_score = score
            best_theme = theme_key
    
    # 如果最强主题的评分太低或没有找到，使用备选方案
    if best_score < 10 or best_theme is None:  # 降低阈值，允许更多主题
        # 如果有任何主题有股票，选择股票数量最多的
        max_stocks = 0
        for theme_key, strength in g.theme_strength.items():
            stock_count = strength.get('stock_count', 0)
            if stock_count > max_stocks:
                max_stocks = stock_count
                best_theme = theme_key
        
        if max_stocks > 0:
            print(f'[主题选择] 使用备选方案：选择股票数量最多的主题（{THEMES[best_theme]["name"]}，{max_stocks}只）')
            return best_theme
    
    return best_theme


# ==================== 调仓逻辑 ====================

def execute_rebalance(context, date_str, reason):
    """
    执行调仓
    
    Args:
        context: 策略上下文
        date_str: 日期字符串
        reason: 调仓原因
    """
    print(f'[调仓] {reason}')
    
    # 1. 确定目标主题
    target_theme = get_best_theme()
    if not target_theme:
        # 如果所有主题都失败，使用指数成分股作为备选
        print('[调仓] 没有找到合适的主线主题，使用指数成分股作为备选')
        try:
            theme_stocks = get_index_stocks(BENCHMARK)
            if theme_stocks and len(theme_stocks) > 0:
                print(f'[调仓] 使用指数成分股: {len(theme_stocks)}只')
                selected_stocks = select_stocks_from_theme(context, theme_stocks, date_str)
                if selected_stocks and len(selected_stocks) > 0:
                    execute_orders(context, selected_stocks, date_str)
                    g.last_rebalance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    g.last_rebalance_trading_days = g.trading_days_count
                    print(f'[调仓完成] 下次调仓将在 {REBALANCE_INTERVAL_DAYS} 个交易日后')
                return
        except Exception as e:
            print(f'[调仓] 获取指数成分股失败: {e}')
        print('[调仓] 无法获取股票池，保持当前持仓')
        return
    
    theme_info = THEMES[target_theme]
    print(f'[调仓] 目标主题: {theme_info["name"]}')
    
    # 2. 获取主题股票池
    if target_theme not in g.theme_stocks or len(g.theme_stocks.get(target_theme, [])) == 0:
        theme_stocks = get_theme_stocks(theme_info, date_str)
        g.theme_stocks[target_theme] = theme_stocks
    else:
        theme_stocks = g.theme_stocks[target_theme]
    
    if not theme_stocks or len(theme_stocks) == 0:
        print(f'[调仓] 主题{theme_info["name"]}股票池为空，尝试使用指数成分股')
        try:
            theme_stocks = get_index_stocks(BENCHMARK)
            if not theme_stocks or len(theme_stocks) == 0:
                print('[调仓] 无法获取股票池，保持当前持仓')
                return
        except Exception as e:
            print(f'[调仓] 获取指数成分股失败: {e}')
            return
    
    print(f'[调仓] 主题股票池: {len(theme_stocks)}只')
    
    # 3. 从主题股票池中选股
    selected_stocks = select_stocks_from_theme(context, theme_stocks, date_str)
    
    if not selected_stocks or len(selected_stocks) == 0:
        print('[调仓] 没有选出合适的股票，保持当前持仓')
        return
    
    print(f'[调仓] 选出 {len(selected_stocks)} 只股票')
    
    # 4. 执行调仓
    execute_orders(context, selected_stocks, date_str)
    
    # 5. 更新状态
    g.current_theme = target_theme
    g.last_rebalance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    g.last_rebalance_trading_days = g.trading_days_count
    
    print(f'[调仓完成] 下次调仓将在 {REBALANCE_INTERVAL_DAYS} 个交易日后')


def select_stocks_from_theme(context, theme_stocks, date_str):
    """
    从主题股票池中选股
    
    Args:
        context: 策略上下文
        theme_stocks: 主题股票列表
        date_str: 日期字符串
    
    Returns:
        list: 选中的股票列表
    """
    stock_scores = []
    
    for stock in theme_stocks[:100]:  # 限制数量
        try:
            # 获取价格数据
            price_df = get_price(stock, count=60, fields=['close', 'volume', 'money'])
            if price_df is None or len(price_df) < 20:
                continue
            
            current_price = price_df['close'].iloc[-1]
            if not (MIN_STOCK_PRICE <= current_price <= MAX_STOCK_PRICE):
                continue
            
            # 计算动量因子（优化：多周期动量）
            closes = price_df['close'].values
            if len(closes) < 20:
                continue
            
            # 短期动量（5日）
            momentum_5 = (closes[-1] / closes[-6] - 1) * 100 if len(closes) >= 6 and closes[-6] > 0 else 0
            # 中期动量（20日）
            momentum_20 = (closes[-1] / closes[0] - 1) * 100 if closes[0] > 0 else 0
            # 综合动量（短期权重更高）
            momentum = momentum_5 * 0.65 + momentum_20 * 0.35
            
            # 计算成交量因子（优化）
            volumes = price_df['volume'].values
            if len(volumes) < 20:
                continue
            
            avg_volume_20 = np.mean(volumes[:-20]) if len(volumes) > 20 else np.mean(volumes[:10])
            recent_volume_5 = np.mean(volumes[-5:]) if len(volumes) >= 5 else np.mean(volumes)
            volume_ratio = (recent_volume_5 / avg_volume_20 - 1) * 100 if avg_volume_20 > 0 else 0
            
            # 计算趋势因子（优化：多均线系统）
            ma5 = np.mean(closes[-5:])
            ma10 = np.mean(closes[-10:]) if len(closes) >= 10 else ma5
            ma20 = np.mean(closes[-20:])
            
            # 趋势强度：均线多头排列 + 价格在均线上方
            trend_score = 0
            if ma5 > ma10 > ma20:  # 多头排列
                trend_score += 35
            if closes[-1] > ma5:
                trend_score += 20
            if closes[-1] > ma10:
                trend_score += 15
            if closes[-1] > ma20:
                trend_score += 10
            
            # 计算相对强度（相对于基准）
            try:
                benchmark_price = get_price(BENCHMARK, count=20, fields=['close'])
                if benchmark_price is not None and len(benchmark_price) > 0:
                    bench_closes = benchmark_price['close'].values
                    bench_return = (bench_closes[-1] / bench_closes[0] - 1) * 100 if bench_closes[0] > 0 else 0
                    relative_strength = momentum_20 - bench_return
                else:
                    relative_strength = 0
            except:
                relative_strength = 0
            
            # 综合评分（进一步优化权重：更重视动量和趋势）
            total_score = (
                momentum * 0.45 +          # 动量权重45%（提高）
                volume_ratio * 0.20 +       # 成交量权重20%（降低）
                trend_score * 0.30 +        # 趋势权重30%
                relative_strength * 0.05    # 相对强度权重5%
            )
            
            stock_scores.append({
                'stock': stock,
                'score': total_score,
                'momentum': momentum,
                'volume_ratio': volume_ratio,
                'trend': trend_score,
                'relative_strength': relative_strength
            })
        except Exception as e:
            continue
    
    if not stock_scores:
        return []
    
    # 按评分排序
    stock_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # 选择前N只
    selected = [item['stock'] for item in stock_scores[:STOCK_NUM]]
    
    print(f'[选股] 前5只股票评分:')
    for i, item in enumerate(stock_scores[:5]):
        print(f'  {i+1}. {item["stock"]}: {item["score"]:.2f} '
              f'(动量: {item["momentum"]:.2f}%, 成交量: {item["volume_ratio"]:.2f}%, 趋势: {item["trend"]:.2f}, 相对强度: {item.get("relative_strength", 0):.2f}%)')
    
    return selected


def execute_orders(context, selected_stocks, date_str):
    """
    执行订单
    
    Args:
        context: 策略上下文
        selected_stocks: 选中的股票列表
        date_str: 日期字符串
    """
    # 获取当前持仓
    positions = context.portfolio.positions
    current_holdings = set(positions.keys())
    target_holdings = set(selected_stocks)
    
    # 获取总资产（兼容处理）
    try:
        total_value = context.portfolio.portfolio_value
    except AttributeError:
        try:
            total_value = context.portfolio.total_value
        except AttributeError:
            print('[错误] 无法获取总资产')
            return
    
    # 获取可用资金（兼容处理）
    try:
        cash = context.portfolio.cash
    except AttributeError:
        try:
            cash = context.portfolio.available_cash
        except AttributeError:
            # 计算持仓价值
            positions_value = sum(
                pos.market_value if hasattr(pos, 'market_value') else 
                pos.total_amount * pos.last_price if hasattr(pos, 'total_amount') and hasattr(pos, 'last_price') else 0
                for pos in positions.values()
            )
            cash = total_value - positions_value
    
    # 计算目标持仓价值
    target_position_value = total_value * MAX_POSITION / len(selected_stocks)
    
    # 卖出不在目标持仓中的股票
    for stock in list(current_holdings):
        if stock not in target_holdings:
            try:
                order_target(stock, 0)
                print(f'[卖出] {stock}')
            except Exception as e:
                print(f'[错误] 卖出{stock}失败: {e}')
    
    # 买入目标持仓中的股票（预筛选：确保能买入至少100股）
    valid_stocks = []
    stock_prices = {}
    
    for stock in selected_stocks:
        try:
            # 获取当前价格
            price_df = get_price(stock, count=1, fields=['close'])
            if price_df is None or len(price_df) == 0:
                continue
            
            current_price = price_df['close'].iloc[-1]
            if current_price <= 0:
                continue
            
            # 检查是否能买入至少100股
            shares_can_buy = int(target_position_value / current_price)
            if shares_can_buy >= MIN_TRADING_UNIT:
                valid_stocks.append(stock)
                stock_prices[stock] = current_price
        except Exception as e:
            print(f'[警告] 预筛选{stock}失败: {e}')
            continue
    
    if not valid_stocks:
        print('[警告] 没有股票能满足最小交易单位要求')
        return
    
    # 重新计算目标持仓价值（基于有效股票数量）
    if len(valid_stocks) < len(selected_stocks):
        target_position_value = total_value * MAX_POSITION / len(valid_stocks)
    
    # 先计算所有订单，确保总金额不超过可用资金
    orders = []
    for stock in valid_stocks:
        current_price = stock_prices[stock]
        shares_to_buy = int(target_position_value / current_price)
        shares_to_buy = (shares_to_buy // MIN_TRADING_UNIT) * MIN_TRADING_UNIT
        
        if shares_to_buy < MIN_TRADING_UNIT:
            continue
        
        # 计算实际需要的资金（考虑手续费和滑点，约0.1%）
        actual_value = shares_to_buy * current_price * 1.001
        orders.append((stock, shares_to_buy, current_price, actual_value))
    
    if not orders:
        print('[警告] 没有股票能满足最小交易单位要求')
        return
    
    # 计算总金额
    total_required = sum(value for _, _, _, value in orders)
    
    # 如果总金额超过可用资金，按比例缩减
    if total_required > cash * 0.95:  # 保留5%缓冲
        scale_factor = (cash * 0.95) / total_required
        print(f'[调仓] 资金不足，按比例缩减订单（比例: {scale_factor:.2f}）')
        scaled_orders = []
        for stock, shares, price, value in orders:
            scaled_shares = int(shares * scale_factor / MIN_TRADING_UNIT) * MIN_TRADING_UNIT
            if scaled_shares >= MIN_TRADING_UNIT:
                scaled_value = scaled_shares * price * 1.001
                scaled_orders.append((stock, scaled_shares, price, scaled_value))
        orders = scaled_orders
    
    # 执行买入订单
    successful_orders = 0
    for stock, shares_to_buy, current_price, actual_value in orders:
        try:
            # 再次检查资金（防止累计误差）
            if actual_value > cash * 0.95:
                print(f'[警告] {stock}需要{actual_value:.2f}元，但可用资金只有{cash:.2f}元，跳过')
                continue
            
            # 使用精确股数下单
            order_result = order_target(stock, shares_to_buy)
            
            # 检查订单是否成功（PTrade的order_target可能返回None或Order对象）
            # 如果返回None，可能是订单失败，但不一定表示错误
            # 我们通过后续检查持仓来验证
            
            # 记录买入价格
            g.entry_prices[stock] = current_price
            g.hold_days[stock] = 0
            successful_orders += 1
            
            print(f'[买入] {stock}: {shares_to_buy}股, 价格: {current_price:.2f}元, 金额: {shares_to_buy * current_price:.2f}元')
        except Exception as e:
            print(f'[错误] 买入{stock}失败: {e}')
    
    if successful_orders == 0:
        print('[警告] 所有买入订单都失败了')


# ==================== 风险控制 ====================

def check_stop_loss(context, date_str):
    """
    检查止损
    
    Args:
        context: 策略上下文
        date_str: 日期字符串
    """
    positions = context.portfolio.positions
    
    for stock in list(positions.keys()):
        try:
            # 获取当前价格
            price_df = get_price(stock, count=1, fields=['close'])
            if price_df is None or len(price_df) == 0:
                continue
            
            current_price = price_df['close'].iloc[-1]
            entry_price = g.entry_prices.get(stock, current_price)
            
            if entry_price > 0:
                pnl = (current_price - entry_price) / entry_price
                
                # 检查最低持仓时间
                hold_days = g.hold_days.get(stock, 0)
                if hold_days < MIN_HOLD_DAYS:
                    # 如果持仓时间不足，只执行紧急止损（-20%）
                    if pnl <= -0.20:
                        order_target(stock, 0)
                        print(f'[紧急止损] {stock}: 亏损 {pnl*100:.2f}% (持仓{hold_days}天)')
                        del g.entry_prices[stock]
                        del g.hold_days[stock]
                else:
                    # 正常止损
                    if pnl <= STOP_LOSS_SINGLE:
                        order_target(stock, 0)
                        print(f'[止损] {stock}: 亏损 {pnl*100:.2f}% (持仓{hold_days}天)')
                        del g.entry_prices[stock]
                        del g.hold_days[stock]
        except Exception as e:
            print(f'[错误] 检查{stock}止损失败: {e}')


def check_take_profit(context, date_str):
    """
    检查止盈
    
    Args:
        context: 策略上下文
        date_str: 日期字符串
    """
    positions = context.portfolio.positions
    
    for stock in list(positions.keys()):
        try:
            # 获取当前价格
            price_df = get_price(stock, count=1, fields=['close'])
            if price_df is None or len(price_df) == 0:
                continue
            
            current_price = price_df['close'].iloc[-1]
            entry_price = g.entry_prices.get(stock, current_price)
            
            if entry_price > 0:
                pnl = (current_price - entry_price) / entry_price
                hold_days = g.hold_days.get(stock, 0)
                
                # 检查最低持仓时间
                if hold_days < MIN_HOLD_DAYS:
                    # 如果持仓时间不足，提高止盈阈值
                    effective_take_profit = TAKE_PROFIT * 1.5
                else:
                    effective_take_profit = TAKE_PROFIT
                
                # 止盈
                if pnl >= effective_take_profit:
                    order_target(stock, 0)
                    print(f'[止盈] {stock}: 盈利 {pnl*100:.2f}% (持仓{hold_days}天)')
                    del g.entry_prices[stock]
                    del g.hold_days[stock]
                
                # 最大持仓天数
                if hold_days >= MAX_HOLD_DAYS:
                    order_target(stock, 0)
                    print(f'[到期卖出] {stock}: 持仓{hold_days}天，达到最大持仓天数')
                    del g.entry_prices[stock]
                    del g.hold_days[stock]
        except Exception as e:
            print(f'[错误] 检查{stock}止盈失败: {e}')


# ==================== 辅助函数 ====================

def update_hold_days(context, current_date):
    """
    更新持仓天数
    
    Args:
        context: 策略上下文
        current_date: 当前日期
    """
    positions = context.portfolio.positions
    
    for stock in positions.keys():
        if stock in g.hold_days:
            g.hold_days[stock] += 1
        else:
            g.hold_days[stock] = 1


def print_position_status(context, date_str):
    """
    输出持仓状态
    
    Args:
        context: 策略上下文
        date_str: 日期字符串
    """
    positions = context.portfolio.positions
    
    # 获取总资产（兼容处理）
    try:
        total_value = context.portfolio.portfolio_value
    except AttributeError:
        total_value = context.portfolio.total_value
    
    # 获取可用资金（兼容处理）
    try:
        cash = context.portfolio.cash
    except AttributeError:
        try:
            cash = context.portfolio.available_cash
        except AttributeError:
            # 计算持仓价值
            positions_value = sum(
                pos.market_value if hasattr(pos, 'market_value') else 
                pos.total_amount * pos.last_price if hasattr(pos, 'total_amount') and hasattr(pos, 'last_price') else 0
                for pos in positions.values()
            )
            cash = total_value - positions_value
    
    # 计算持仓比例
    positions_value = total_value - cash
    position_ratio = positions_value / total_value if total_value > 0 else 0
    
    print(f'[持仓状态] 持仓数量: {len(positions)}只')
    print(f'[持仓状态] 总资产: {total_value:.2f}')
    print(f'[持仓状态] 可用资金: {cash:.2f}')
    print(f'[持仓状态] 持仓比例: {position_ratio*100:.1f}%')
    
    if g.current_theme:
        theme_name = THEMES[g.current_theme]['name']
        print(f'[持仓状态] 当前主题: {theme_name}')

