# -*- coding: utf-8 -*-
"""
十倍股综合策略 - 基于TRQuant十倍股框架
========================================

策略特色:
---------
1. 整合所有数据源：JQData、AKShare、MongoDB
2. 使用聚宽因子库：CNE5/CNE6风格因子、聚宽因子
3. 十倍股评估体系：7维度综合评估
4. 增强风控模块：止盈止损、移动止损、仓位管理

代码位置:
---------
- 策略主文件: strategies/tenbagger_comprehensive_strategy.py
- 十倍股评估: mcp_servers/utils/tenbagger_evaluator.py
- 因子管理: core/factors/factor_pool_integration.py
- 风控模块: mcp_servers/utils/portfolio_manager.py

创建时间: 2025-12-26
回测区间: 2024-01-01 至 2025-12-25
基准指数: 000300.XSHG (沪深300)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入JQData
import jqdatasdk as jq

# 导入TRQuant核心模块
try:
    from jqdata.client import JQDataClient
    from core.mainline_scanner import MainlineBasedScanner
    from core.factors.factor_pool_integration import FactorPoolIntegration
    from mcp_servers.utils.tenbagger_evaluator import TenbaggerEvaluator, EvalLevel
    from mcp_servers.utils.portfolio_manager import RiskManager, RiskConfig
    from extension.python.tenbagger_commands import (
        tenbagger_scan_candidates,
        tenbagger_get_rankings
    )
except ImportError as e:
    logging.warning(f"部分模块导入失败: {e}")

# ============================================================
# 全局变量和配置
# ============================================================

g = type('g', (), {})()  # 全局变量容器

# 策略参数
g.params = {
    # 仓位管理
    'max_total_position': 0.90,      # 总仓位上限
    'single_stock_max': 0.10,        # 单票上限
    'min_cash': 0.10,                # 最低现金比例
    'max_holdings': 20,               # 最大持仓数
    
    # 风控参数
    'stop_loss': -0.08,               # 止损比例 -8%
    'take_profit': 0.30,              # 止盈比例 30%
    'trailing_stop': 0.05,            # 移动止损回撤 5%
    'max_drawdown_limit': -0.15,      # 最大回撤限制 -15%
    
    # 十倍股筛选
    'min_tenbagger_score': 65,        # 最低十倍股评分
    'min_eval_level': 'A',            # 最低评估等级
    'preferred_stages': ['S1', 'S2', 'S3'],  # 偏好阶段
    
    # 因子权重
    'tenbagger_weight': 0.40,         # 十倍股评分权重
    'factor_weight': 0.35,            # 聚宽因子权重
    'mainline_weight': 0.25,           # 主线评分权重
    
    # 调仓频率
    'rebalance_frequency': 5,         # 每5个交易日调仓一次
}

# 持仓记录
g.holdings = {}                        # 持仓字典 {code: entry_info}
g.cost_prices = {}                     # 成本价
g.highest_prices = {}                  # 最高价
g.entry_dates = {}                      # 建仓日期
g.last_rebalance_date = None            # 上次调仓日期

# 数据源客户端
g.jq_client = None
g.scanner = None
g.factor_integration = None
g.tenbagger_evaluator = None
g.risk_manager = None

# ============================================================
# 初始化函数
# ============================================================

def initialize(context):
    """
    策略初始化
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:initialize()
    """
    log.info("=" * 80)
    log.info("十倍股综合策略初始化")
    log.info("=" * 80)
    
    # 1. JQData认证
    try:
        from config.config_manager import get_config_manager
        config_manager = get_config_manager()
        jq_config = config_manager.get_jqdata_config()
        username = jq_config.get('username')
        password = jq_config.get('password')
        
        if username and password:
            jq.auth(username, password)
            log.info(f"✅ JQData认证成功: {username}")
            
            # 初始化JQData客户端
            g.jq_client = JQDataClient()
            g.jq_client.authenticate(username, password)
        else:
            log.warn("⚠️ JQData配置未找到，部分功能可能受限")
    except Exception as e:
        log.warn(f"⚠️ JQData初始化失败: {e}")
    
    # 2. 初始化主线扫描器
    try:
        g.scanner = MainlineBasedScanner(jq_client=g.jq_client)
        log.info("✅ 主线扫描器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 主线扫描器初始化失败: {e}")
    
    # 3. 初始化因子集成
    try:
        g.factor_integration = FactorPoolIntegration(jq_client=g.jq_client)
        log.info("✅ 因子集成模块初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 因子集成模块初始化失败: {e}")
    
    # 4. 初始化十倍股评估器
    try:
        g.tenbagger_evaluator = TenbaggerEvaluator()
        log.info("✅ 十倍股评估器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 十倍股评估器初始化失败: {e}")
    
    # 5. 初始化风控管理器
    try:
        risk_config = RiskConfig(
            stop_loss=g.params['stop_loss'],
            take_profit=g.params['take_profit'],
            trailing_stop=g.params['trailing_stop'],
            max_drawdown=g.params['max_drawdown_limit'],
            max_position=g.params['max_total_position'],
            single_stock_max=g.params['single_stock_max']
        )
        g.risk_manager = RiskManager(risk_config)
        log.info("✅ 风控管理器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 风控管理器初始化失败: {e}")
    
    # 6. 设置基准和手续费
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    
    # 手续费设置
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            close_today_commission=0,
            min_commission=5
        ),
        type='stock'
    )
    
    # 7. 运行函数设置
    run_daily(before_market_open, time='before_open', reference_security='000300.XSHG')
    run_daily(market_open, time='open', reference_security='000300.XSHG')
    run_daily(after_market_close, time='after_close', reference_security='000300.XSHG')
    
    log.info("=" * 80)
    log.info("策略初始化完成")
    log.info("=" * 80)

# ============================================================
# 盘前准备
# ============================================================

def before_market_open(context):
    """
    盘前准备
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:before_market_open()
    """
    log.info("📅 盘前准备开始")
    
    # 检查是否需要调仓
    current_date = context.current_dt.date()
    if g.last_rebalance_date is None or \
       (current_date - g.last_rebalance_date).days >= g.params['rebalance_frequency']:
        log.info(f"🔄 触发调仓检查 (上次调仓: {g.last_rebalance_date})")
        g.last_rebalance_date = current_date
    
    # 更新持仓记录
    update_holdings(context)

# ============================================================
# 开盘交易
# ============================================================

def market_open(context):
    """
    开盘交易逻辑
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:market_open()
    """
    log.info("🚀 开盘交易开始")
    
    # 1. 风控检查（优先执行）
    risk_control(context)
    
    # 2. 检查是否需要调仓
    current_date = context.current_dt.date()
    if g.last_rebalance_date == current_date:
        # 执行调仓
        rebalance(context)
    else:
        log.info("⏭️ 今日不调仓，继续持有")

# ============================================================
# 调仓逻辑
# ============================================================

def rebalance(context):
    """
    调仓逻辑
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:rebalance()
    
    流程:
    1. 获取十倍股候选池
    2. 计算聚宽因子评分
    3. 获取主线评分
    4. 综合评分排序
    5. 执行买卖操作
    """
    log.info("=" * 80)
    log.info("🔄 开始调仓")
    log.info("=" * 80)
    
    current_date = context.current_dt.date()
    current_datetime = context.current_dt
    
    # 1. 获取十倍股候选池
    candidate_stocks = get_tenbagger_candidates(context, current_date)
    log.info(f"📊 十倍股候选池: {len(candidate_stocks)} 只股票")
    
    if not candidate_stocks:
        log.warn("⚠️ 未找到符合条件的候选股票，保持当前持仓")
        return
    
    # 2. 计算聚宽因子评分
    factor_scores = calculate_jq_factors(context, candidate_stocks, current_date)
    log.info(f"📈 聚宽因子评分完成: {len(factor_scores)} 只股票")
    
    # 3. 获取主线评分
    mainline_scores = get_mainline_scores(context, candidate_stocks, current_date)
    log.info(f"🎯 主线评分完成: {len(mainline_scores)} 只股票")
    
    # 4. 获取十倍股评分
    tenbagger_scores = get_tenbagger_scores(context, candidate_stocks, current_date)
    log.info(f"⭐ 十倍股评分完成: {len(tenbagger_scores)} 只股票")
    
    # 5. 综合评分
    final_scores = combine_scores(
        candidate_stocks,
        tenbagger_scores,
        factor_scores,
        mainline_scores
    )
    
    # 6. 排序并选择目标股票
    target_stocks = select_target_stocks(final_scores, context)
    log.info(f"🎯 目标持仓: {len(target_stocks)} 只股票")
    
    # 7. 执行调仓
    execute_rebalance(context, target_stocks)

# ============================================================
# 数据获取函数
# ============================================================

def get_tenbagger_candidates(context, date) -> List[str]:
    """
    获取十倍股候选池
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_tenbagger_candidates()
    
    数据源: MongoDB (通过tenbagger_commands)
    """
    try:
        # 从数据库获取十倍股排名
        rankings = tenbagger_get_rankings(
            limit=100,
            min_score=g.params['min_tenbagger_score'],
            min_level=g.params['min_eval_level']
        )
        
        if rankings and len(rankings) > 0:
            # 提取股票代码
            stocks = [r.get('code', '') for r in rankings if r.get('code')]
            # 过滤掉ST、停牌等
            stocks = filter_tradable_stocks(context, stocks)
            return stocks[:50]  # 取前50只
    except Exception as e:
        log.warn(f"⚠️ 获取十倍股候选池失败: {e}")
    
    # 备用方案：从主线扫描获取
    try:
        if g.scanner:
            mainlines = g.scanner.scan_mainlines(date)
            stocks = []
            for mainline in mainlines[:5]:  # 取前5条主线
                stocks.extend(mainline.get('stocks', []))
            stocks = list(set(stocks))[:50]
            return filter_tradable_stocks(context, stocks)
    except Exception as e:
        log.warn(f"⚠️ 备用方案获取候选池失败: {e}")
    
    return []

def calculate_jq_factors(context, stocks: List[str], date) -> Dict[str, float]:
    """
    计算聚宽因子评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:calculate_jq_factors()
    
    使用的因子:
    - CNE5风格因子 (get_factor_values)
    - CNE6风格因子pro (get_factor_values)
    - 聚宽因子 (get_all_factors)
    """
    factor_scores = {}
    
    try:
        # 1. CNE5风格因子
        try:
            cne5_factors = ['size', 'beta', 'momentum', 'reversal', 'volatility']
            cne5_scores = {}
            for factor in cne5_factors:
                try:
                    values = jq.get_factor_values(
                        securities=stocks,
                        factors=[factor],
                        count=1,
                        end_date=date
                    )
                    if values is not None and not values.empty:
                        # 标准化并加权
                        normalized = (values[factor] - values[factor].mean()) / values[factor].std()
                        cne5_scores[factor] = normalized
                except Exception as e:
                    log.debug(f"CNE5因子 {factor} 计算失败: {e}")
            
            # 综合CNE5评分
            if cne5_scores:
                cne5_df = pd.DataFrame(cne5_scores)
                cne5_combined = cne5_df.mean(axis=1)
                for stock in stocks:
                    if stock in cne5_combined.index:
                        factor_scores[stock] = factor_scores.get(stock, 0) + cne5_combined[stock] * 0.3
        except Exception as e:
            log.warn(f"⚠️ CNE5因子计算失败: {e}")
        
        # 2. CNE6风格因子pro
        try:
            cne6_factors = ['size', 'beta', 'momentum', 'reversal', 'volatility', 'growth', 'earnings_yield']
            cne6_scores = {}
            for factor in cne6_factors:
                try:
                    values = jq.get_factor_values(
                        securities=stocks,
                        factors=[factor],
                        count=1,
                        end_date=date
                    )
                    if values is not None and not values.empty:
                        normalized = (values[factor] - values[factor].mean()) / values[factor].std()
                        cne6_scores[factor] = normalized
                except Exception as e:
                    log.debug(f"CNE6因子 {factor} 计算失败: {e}")
            
            if cne6_scores:
                cne6_df = pd.DataFrame(cne6_scores)
                cne6_combined = cne6_df.mean(axis=1)
                for stock in stocks:
                    if stock in cne6_combined.index:
                        factor_scores[stock] = factor_scores.get(stock, 0) + cne6_combined[stock] * 0.4
        except Exception as e:
            log.warn(f"⚠️ CNE6因子计算失败: {e}")
        
        # 3. 聚宽因子库
        try:
            if g.factor_integration:
                jq_factor_scores = g.factor_integration.process_candidate_pool(
                    stocks=stocks,
                    date=date,
                    period='medium',
                    top_n=len(stocks)
                )
                for signal in jq_factor_scores:
                    stock = signal.code
                    factor_scores[stock] = factor_scores.get(stock, 0) + signal.factor_score * 0.3
        except Exception as e:
            log.warn(f"⚠️ 聚宽因子库计算失败: {e}")
        
    except Exception as e:
        log.warn(f"⚠️ 因子计算总体失败: {e}")
    
    return factor_scores

def get_mainline_scores(context, stocks: List[str], date) -> Dict[str, float]:
    """
    获取主线评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_mainline_scores()
    
    数据源: MainlineBasedScanner
    """
    mainline_scores = {}
    
    try:
        if g.scanner:
            mainlines = g.scanner.scan_mainlines(date)
            # 构建股票到主线的映射
            stock_to_mainline = {}
            for mainline in mainlines:
                mainline_name = mainline.get('name', '')
                mainline_stocks = mainline.get('stocks', [])
                mainline_score = mainline.get('score', 0.5)
                for stock in mainline_stocks:
                    if stock in stocks:
                        if stock not in stock_to_mainline:
                            stock_to_mainline[stock] = []
                        stock_to_mainline[stock].append(mainline_score)
            
            # 计算平均主线评分
            for stock in stocks:
                if stock in stock_to_mainline:
                    scores = stock_to_mainline[stock]
                    mainline_scores[stock] = np.mean(scores) if scores else 0.5
                else:
                    mainline_scores[stock] = 0.5  # 默认值
    except Exception as e:
        log.warn(f"⚠️ 获取主线评分失败: {e}")
        # 默认值
        for stock in stocks:
            mainline_scores[stock] = 0.5
    
    return mainline_scores

def get_tenbagger_scores(context, stocks: List[str], date) -> Dict[str, float]:
    """
    获取十倍股评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_tenbagger_scores()
    
    数据源: MongoDB (通过tenbagger_commands)
    """
    tenbagger_scores = {}
    
    try:
        rankings = tenbagger_get_rankings(limit=200)
        if rankings:
            for ranking in rankings:
                code = ranking.get('code', '')
                if code in stocks:
                    total_score = ranking.get('total_score', 0)
                    eval_level = ranking.get('eval_level', 'D')
                    
                    # 转换为0-1评分
                    if eval_level == 'S+':
                        normalized_score = min(total_score / 100, 1.0)
                    elif eval_level == 'S':
                        normalized_score = min(total_score / 90, 1.0)
                    elif eval_level == 'A':
                        normalized_score = min(total_score / 80, 1.0)
                    else:
                        normalized_score = min(total_score / 70, 1.0)
                    
                    tenbagger_scores[code] = normalized_score
    except Exception as e:
        log.warn(f"⚠️ 获取十倍股评分失败: {e}")
    
    # 默认值
    for stock in stocks:
        if stock not in tenbagger_scores:
            tenbagger_scores[stock] = 0.5
    
    return tenbagger_scores

# ============================================================
# 评分组合函数
# ============================================================

def combine_scores(
    stocks: List[str],
    tenbagger_scores: Dict[str, float],
    factor_scores: Dict[str, float],
    mainline_scores: Dict[str, float]
) -> Dict[str, float]:
    """
    综合评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:combine_scores()
    """
    final_scores = {}
    
    for stock in stocks:
        tenbagger = tenbagger_scores.get(stock, 0.5)
        factor = factor_scores.get(stock, 0.5)
        mainline = mainline_scores.get(stock, 0.5)
        
        # 标准化因子评分到0-1
        if factor != 0.5:  # 如果有实际计算值
            factor = (factor + 3) / 6  # 假设因子评分在-3到3之间，标准化到0-1
            factor = max(0, min(1, factor))
        
        # 加权组合
        final_score = (
            tenbagger * g.params['tenbagger_weight'] +
            factor * g.params['factor_weight'] +
            mainline * g.params['mainline_weight']
        )
        
        final_scores[stock] = final_score
    
    return final_scores

def select_target_stocks(scores: Dict[str, float], context) -> List[str]:
    """
    选择目标股票
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:select_target_stocks()
    """
    # 按评分排序
    sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # 选择前N只
    max_holdings = g.params['max_holdings']
    target_stocks = [stock for stock, score in sorted_stocks[:max_holdings]]
    
    return target_stocks

# ============================================================
# 交易执行函数
# ============================================================

def execute_rebalance(context, target_stocks: List[str]):
    """
    执行调仓
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:execute_rebalance()
    """
    current_positions = list(context.portfolio.positions.keys())
    
    # 需要卖出的股票（不在目标列表中的持仓）
    to_sell = [s for s in current_positions if s not in target_stocks and context.portfolio.positions[s].total_amount > 0]
    
    # 需要买入的股票（在目标列表中但未持仓或持仓不足）
    to_buy = [s for s in target_stocks if s not in current_positions or context.portfolio.positions[s].total_amount == 0]
    
    # 需要调整的股票（在目标列表中但持仓比例需要调整）
    to_adjust = [s for s in target_stocks if s in current_positions and context.portfolio.positions[s].total_amount > 0]
    
    # 1. 先卖出
    for stock in to_sell:
        try:
            order_target_value(stock, 0)
            log.info(f"🔴 卖出: {stock}")
            # 清理记录
            g.holdings.pop(stock, None)
            g.cost_prices.pop(stock, None)
            g.highest_prices.pop(stock, None)
            g.entry_dates.pop(stock, None)
        except Exception as e:
            log.warn(f"⚠️ 卖出失败 {stock}: {e}")
    
    # 2. 计算目标仓位
    total_value = context.portfolio.total_value
    available_cash = context.portfolio.available_cash
    max_position_value = total_value * g.params['max_total_position']
    target_position_value = (max_position_value - (total_value - available_cash)) / len(target_stocks)
    target_position_value = min(target_position_value, total_value * g.params['single_stock_max'])
    
    # 3. 买入新股票
    for stock in to_buy:
        try:
            order_target_value(stock, target_position_value)
            log.info(f"🟢 买入: {stock}, 目标金额: {target_position_value:.2f}")
            # 记录建仓信息
            g.entry_dates[stock] = context.current_dt.date()
        except Exception as e:
            log.warn(f"⚠️ 买入失败 {stock}: {e}")
    
    # 4. 调整现有持仓
    for stock in to_adjust:
        try:
            current_value = context.portfolio.positions[stock].total_amount * \
                           context.portfolio.positions[stock].price
            if abs(current_value - target_position_value) > total_value * 0.01:  # 差异超过1%才调整
                order_target_value(stock, target_position_value)
                log.info(f"🔄 调整: {stock}, 目标金额: {target_position_value:.2f}")
        except Exception as e:
            log.warn(f"⚠️ 调整失败 {stock}: {e}")

# ============================================================
# 风控模块
# ============================================================

def risk_control(context):
    """
    风险控制
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:risk_control()
    
    功能:
    1. 止盈止损
    2. 移动止损
    3. 最大回撤限制
    4. 仓位管理
    """
    current_data = get_current_data()
    
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.total_amount == 0:
            continue
        
        current_price = current_data[stock].last_price
        cost_price = g.cost_prices.get(stock, pos.avg_cost)
        highest_price = g.highest_prices.get(stock, cost_price)
        
        if cost_price <= 0:
            continue
        
        # 更新最高价
        if current_price > highest_price:
            g.highest_prices[stock] = current_price
            highest_price = current_price
        
        profit = (current_price - cost_price) / cost_price
        drawdown_from_high = (highest_price - current_price) / highest_price if highest_price > 0 else 0
        
        # 1. 止损
        if profit < g.params['stop_loss']:
            log.warn(f'🛑 [止损] {stock} 亏损: {profit*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue
        
        # 2. 止盈
        if profit > g.params['take_profit']:
            log.info(f'🎯 [止盈] {stock} 盈利: {profit*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue
        
        # 3. 移动止损（盈利超过10%后启用）
        if profit > 0.10 and drawdown_from_high > g.params['trailing_stop']:
            log.info(f'📉 [移动止损] {stock} 从高点回撤: {drawdown_from_high*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue

def clean_stock_records(stock):
    """清理股票记录"""
    g.holdings.pop(stock, None)
    g.cost_prices.pop(stock, None)
    g.highest_prices.pop(stock, None)
    g.entry_dates.pop(stock, None)

def update_holdings(context):
    """更新持仓记录"""
    for stock, pos in context.portfolio.positions.items():
        if pos.total_amount > 0:
            if stock not in g.cost_prices:
                g.cost_prices[stock] = pos.avg_cost
            if stock not in g.highest_prices:
                g.highest_prices[stock] = pos.avg_cost
            if stock not in g.entry_dates:
                g.entry_dates[stock] = context.current_dt.date()

# ============================================================
# 辅助函数
# ============================================================

def filter_tradable_stocks(context, stocks: List[str]) -> List[str]:
    """过滤可交易股票"""
    current_data = get_current_data()
    tradable = []
    
    for stock in stocks:
        try:
            # 检查是否可交易
            if stock in current_data and current_data[stock].paused == False:
                # 检查是否ST
                info = jq.get_security_info(stock)
                if info and 'ST' not in info.display_name:
                    tradable.append(stock)
        except:
            continue
    
    return tradable

# ============================================================
# 盘后处理
# ============================================================

def after_market_close(context):
    """
    盘后处理
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:after_market_close()
    """
    # 更新持仓记录
    update_holdings(context)
    
    # 记录每日持仓
    log.info(f"📊 当前持仓数: {len([s for s in context.portfolio.positions.keys() if context.portfolio.positions[s].total_amount > 0])}")
    log.info(f"💰 总资产: {context.portfolio.total_value:.2f}")
    log.info(f"💵 可用现金: {context.portfolio.available_cash:.2f}")



"""
十倍股综合策略 - 基于TRQuant十倍股框架
========================================

策略特色:
---------
1. 整合所有数据源：JQData、AKShare、MongoDB
2. 使用聚宽因子库：CNE5/CNE6风格因子、聚宽因子
3. 十倍股评估体系：7维度综合评估
4. 增强风控模块：止盈止损、移动止损、仓位管理

代码位置:
---------
- 策略主文件: strategies/tenbagger_comprehensive_strategy.py
- 十倍股评估: mcp_servers/utils/tenbagger_evaluator.py
- 因子管理: core/factors/factor_pool_integration.py
- 风控模块: mcp_servers/utils/portfolio_manager.py

创建时间: 2025-12-26
回测区间: 2024-01-01 至 2025-12-25
基准指数: 000300.XSHG (沪深300)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入JQData
import jqdatasdk as jq

# 导入TRQuant核心模块
try:
    from jqdata.client import JQDataClient
    from core.mainline_scanner import MainlineBasedScanner
    from core.factors.factor_pool_integration import FactorPoolIntegration
    from mcp_servers.utils.tenbagger_evaluator import TenbaggerEvaluator, EvalLevel
    from mcp_servers.utils.portfolio_manager import RiskManager, RiskConfig
    from extension.python.tenbagger_commands import (
        tenbagger_scan_candidates,
        tenbagger_get_rankings
    )
except ImportError as e:
    logging.warning(f"部分模块导入失败: {e}")

# ============================================================
# 全局变量和配置
# ============================================================

g = type('g', (), {})()  # 全局变量容器

# 策略参数
g.params = {
    # 仓位管理
    'max_total_position': 0.90,      # 总仓位上限
    'single_stock_max': 0.10,        # 单票上限
    'min_cash': 0.10,                # 最低现金比例
    'max_holdings': 20,               # 最大持仓数
    
    # 风控参数
    'stop_loss': -0.08,               # 止损比例 -8%
    'take_profit': 0.30,              # 止盈比例 30%
    'trailing_stop': 0.05,            # 移动止损回撤 5%
    'max_drawdown_limit': -0.15,      # 最大回撤限制 -15%
    
    # 十倍股筛选
    'min_tenbagger_score': 65,        # 最低十倍股评分
    'min_eval_level': 'A',            # 最低评估等级
    'preferred_stages': ['S1', 'S2', 'S3'],  # 偏好阶段
    
    # 因子权重
    'tenbagger_weight': 0.40,         # 十倍股评分权重
    'factor_weight': 0.35,            # 聚宽因子权重
    'mainline_weight': 0.25,           # 主线评分权重
    
    # 调仓频率
    'rebalance_frequency': 5,         # 每5个交易日调仓一次
}

# 持仓记录
g.holdings = {}                        # 持仓字典 {code: entry_info}
g.cost_prices = {}                     # 成本价
g.highest_prices = {}                  # 最高价
g.entry_dates = {}                      # 建仓日期
g.last_rebalance_date = None            # 上次调仓日期

# 数据源客户端
g.jq_client = None
g.scanner = None
g.factor_integration = None
g.tenbagger_evaluator = None
g.risk_manager = None

# ============================================================
# 初始化函数
# ============================================================

def initialize(context):
    """
    策略初始化
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:initialize()
    """
    log.info("=" * 80)
    log.info("十倍股综合策略初始化")
    log.info("=" * 80)
    
    # 1. JQData认证
    try:
        from config.config_manager import get_config_manager
        config_manager = get_config_manager()
        jq_config = config_manager.get_jqdata_config()
        username = jq_config.get('username')
        password = jq_config.get('password')
        
        if username and password:
            jq.auth(username, password)
            log.info(f"✅ JQData认证成功: {username}")
            
            # 初始化JQData客户端
            g.jq_client = JQDataClient()
            g.jq_client.authenticate(username, password)
        else:
            log.warn("⚠️ JQData配置未找到，部分功能可能受限")
    except Exception as e:
        log.warn(f"⚠️ JQData初始化失败: {e}")
    
    # 2. 初始化主线扫描器
    try:
        g.scanner = MainlineBasedScanner(jq_client=g.jq_client)
        log.info("✅ 主线扫描器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 主线扫描器初始化失败: {e}")
    
    # 3. 初始化因子集成
    try:
        g.factor_integration = FactorPoolIntegration(jq_client=g.jq_client)
        log.info("✅ 因子集成模块初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 因子集成模块初始化失败: {e}")
    
    # 4. 初始化十倍股评估器
    try:
        g.tenbagger_evaluator = TenbaggerEvaluator()
        log.info("✅ 十倍股评估器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 十倍股评估器初始化失败: {e}")
    
    # 5. 初始化风控管理器
    try:
        risk_config = RiskConfig(
            stop_loss=g.params['stop_loss'],
            take_profit=g.params['take_profit'],
            trailing_stop=g.params['trailing_stop'],
            max_drawdown=g.params['max_drawdown_limit'],
            max_position=g.params['max_total_position'],
            single_stock_max=g.params['single_stock_max']
        )
        g.risk_manager = RiskManager(risk_config)
        log.info("✅ 风控管理器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 风控管理器初始化失败: {e}")
    
    # 6. 设置基准和手续费
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    
    # 手续费设置
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            close_today_commission=0,
            min_commission=5
        ),
        type='stock'
    )
    
    # 7. 运行函数设置
    run_daily(before_market_open, time='before_open', reference_security='000300.XSHG')
    run_daily(market_open, time='open', reference_security='000300.XSHG')
    run_daily(after_market_close, time='after_close', reference_security='000300.XSHG')
    
    log.info("=" * 80)
    log.info("策略初始化完成")
    log.info("=" * 80)

# ============================================================
# 盘前准备
# ============================================================

def before_market_open(context):
    """
    盘前准备
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:before_market_open()
    """
    log.info("📅 盘前准备开始")
    
    # 检查是否需要调仓
    current_date = context.current_dt.date()
    if g.last_rebalance_date is None or \
       (current_date - g.last_rebalance_date).days >= g.params['rebalance_frequency']:
        log.info(f"🔄 触发调仓检查 (上次调仓: {g.last_rebalance_date})")
        g.last_rebalance_date = current_date
    
    # 更新持仓记录
    update_holdings(context)

# ============================================================
# 开盘交易
# ============================================================

def market_open(context):
    """
    开盘交易逻辑
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:market_open()
    """
    log.info("🚀 开盘交易开始")
    
    # 1. 风控检查（优先执行）
    risk_control(context)
    
    # 2. 检查是否需要调仓
    current_date = context.current_dt.date()
    if g.last_rebalance_date == current_date:
        # 执行调仓
        rebalance(context)
    else:
        log.info("⏭️ 今日不调仓，继续持有")

# ============================================================
# 调仓逻辑
# ============================================================

def rebalance(context):
    """
    调仓逻辑
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:rebalance()
    
    流程:
    1. 获取十倍股候选池
    2. 计算聚宽因子评分
    3. 获取主线评分
    4. 综合评分排序
    5. 执行买卖操作
    """
    log.info("=" * 80)
    log.info("🔄 开始调仓")
    log.info("=" * 80)
    
    current_date = context.current_dt.date()
    current_datetime = context.current_dt
    
    # 1. 获取十倍股候选池
    candidate_stocks = get_tenbagger_candidates(context, current_date)
    log.info(f"📊 十倍股候选池: {len(candidate_stocks)} 只股票")
    
    if not candidate_stocks:
        log.warn("⚠️ 未找到符合条件的候选股票，保持当前持仓")
        return
    
    # 2. 计算聚宽因子评分
    factor_scores = calculate_jq_factors(context, candidate_stocks, current_date)
    log.info(f"📈 聚宽因子评分完成: {len(factor_scores)} 只股票")
    
    # 3. 获取主线评分
    mainline_scores = get_mainline_scores(context, candidate_stocks, current_date)
    log.info(f"🎯 主线评分完成: {len(mainline_scores)} 只股票")
    
    # 4. 获取十倍股评分
    tenbagger_scores = get_tenbagger_scores(context, candidate_stocks, current_date)
    log.info(f"⭐ 十倍股评分完成: {len(tenbagger_scores)} 只股票")
    
    # 5. 综合评分
    final_scores = combine_scores(
        candidate_stocks,
        tenbagger_scores,
        factor_scores,
        mainline_scores
    )
    
    # 6. 排序并选择目标股票
    target_stocks = select_target_stocks(final_scores, context)
    log.info(f"🎯 目标持仓: {len(target_stocks)} 只股票")
    
    # 7. 执行调仓
    execute_rebalance(context, target_stocks)

# ============================================================
# 数据获取函数
# ============================================================

def get_tenbagger_candidates(context, date) -> List[str]:
    """
    获取十倍股候选池
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_tenbagger_candidates()
    
    数据源: MongoDB (通过tenbagger_commands)
    """
    try:
        # 从数据库获取十倍股排名
        rankings = tenbagger_get_rankings(
            limit=100,
            min_score=g.params['min_tenbagger_score'],
            min_level=g.params['min_eval_level']
        )
        
        if rankings and len(rankings) > 0:
            # 提取股票代码
            stocks = [r.get('code', '') for r in rankings if r.get('code')]
            # 过滤掉ST、停牌等
            stocks = filter_tradable_stocks(context, stocks)
            return stocks[:50]  # 取前50只
    except Exception as e:
        log.warn(f"⚠️ 获取十倍股候选池失败: {e}")
    
    # 备用方案：从主线扫描获取
    try:
        if g.scanner:
            mainlines = g.scanner.scan_mainlines(date)
            stocks = []
            for mainline in mainlines[:5]:  # 取前5条主线
                stocks.extend(mainline.get('stocks', []))
            stocks = list(set(stocks))[:50]
            return filter_tradable_stocks(context, stocks)
    except Exception as e:
        log.warn(f"⚠️ 备用方案获取候选池失败: {e}")
    
    return []

def calculate_jq_factors(context, stocks: List[str], date) -> Dict[str, float]:
    """
    计算聚宽因子评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:calculate_jq_factors()
    
    使用的因子:
    - CNE5风格因子 (get_factor_values)
    - CNE6风格因子pro (get_factor_values)
    - 聚宽因子 (get_all_factors)
    """
    factor_scores = {}
    
    try:
        # 1. CNE5风格因子
        try:
            cne5_factors = ['size', 'beta', 'momentum', 'reversal', 'volatility']
            cne5_scores = {}
            for factor in cne5_factors:
                try:
                    values = jq.get_factor_values(
                        securities=stocks,
                        factors=[factor],
                        count=1,
                        end_date=date
                    )
                    if values is not None and not values.empty:
                        # 标准化并加权
                        normalized = (values[factor] - values[factor].mean()) / values[factor].std()
                        cne5_scores[factor] = normalized
                except Exception as e:
                    log.debug(f"CNE5因子 {factor} 计算失败: {e}")
            
            # 综合CNE5评分
            if cne5_scores:
                cne5_df = pd.DataFrame(cne5_scores)
                cne5_combined = cne5_df.mean(axis=1)
                for stock in stocks:
                    if stock in cne5_combined.index:
                        factor_scores[stock] = factor_scores.get(stock, 0) + cne5_combined[stock] * 0.3
        except Exception as e:
            log.warn(f"⚠️ CNE5因子计算失败: {e}")
        
        # 2. CNE6风格因子pro
        try:
            cne6_factors = ['size', 'beta', 'momentum', 'reversal', 'volatility', 'growth', 'earnings_yield']
            cne6_scores = {}
            for factor in cne6_factors:
                try:
                    values = jq.get_factor_values(
                        securities=stocks,
                        factors=[factor],
                        count=1,
                        end_date=date
                    )
                    if values is not None and not values.empty:
                        normalized = (values[factor] - values[factor].mean()) / values[factor].std()
                        cne6_scores[factor] = normalized
                except Exception as e:
                    log.debug(f"CNE6因子 {factor} 计算失败: {e}")
            
            if cne6_scores:
                cne6_df = pd.DataFrame(cne6_scores)
                cne6_combined = cne6_df.mean(axis=1)
                for stock in stocks:
                    if stock in cne6_combined.index:
                        factor_scores[stock] = factor_scores.get(stock, 0) + cne6_combined[stock] * 0.4
        except Exception as e:
            log.warn(f"⚠️ CNE6因子计算失败: {e}")
        
        # 3. 聚宽因子库
        try:
            if g.factor_integration:
                jq_factor_scores = g.factor_integration.process_candidate_pool(
                    stocks=stocks,
                    date=date,
                    period='medium',
                    top_n=len(stocks)
                )
                for signal in jq_factor_scores:
                    stock = signal.code
                    factor_scores[stock] = factor_scores.get(stock, 0) + signal.factor_score * 0.3
        except Exception as e:
            log.warn(f"⚠️ 聚宽因子库计算失败: {e}")
        
    except Exception as e:
        log.warn(f"⚠️ 因子计算总体失败: {e}")
    
    return factor_scores

def get_mainline_scores(context, stocks: List[str], date) -> Dict[str, float]:
    """
    获取主线评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_mainline_scores()
    
    数据源: MainlineBasedScanner
    """
    mainline_scores = {}
    
    try:
        if g.scanner:
            mainlines = g.scanner.scan_mainlines(date)
            # 构建股票到主线的映射
            stock_to_mainline = {}
            for mainline in mainlines:
                mainline_name = mainline.get('name', '')
                mainline_stocks = mainline.get('stocks', [])
                mainline_score = mainline.get('score', 0.5)
                for stock in mainline_stocks:
                    if stock in stocks:
                        if stock not in stock_to_mainline:
                            stock_to_mainline[stock] = []
                        stock_to_mainline[stock].append(mainline_score)
            
            # 计算平均主线评分
            for stock in stocks:
                if stock in stock_to_mainline:
                    scores = stock_to_mainline[stock]
                    mainline_scores[stock] = np.mean(scores) if scores else 0.5
                else:
                    mainline_scores[stock] = 0.5  # 默认值
    except Exception as e:
        log.warn(f"⚠️ 获取主线评分失败: {e}")
        # 默认值
        for stock in stocks:
            mainline_scores[stock] = 0.5
    
    return mainline_scores

def get_tenbagger_scores(context, stocks: List[str], date) -> Dict[str, float]:
    """
    获取十倍股评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_tenbagger_scores()
    
    数据源: MongoDB (通过tenbagger_commands)
    """
    tenbagger_scores = {}
    
    try:
        rankings = tenbagger_get_rankings(limit=200)
        if rankings:
            for ranking in rankings:
                code = ranking.get('code', '')
                if code in stocks:
                    total_score = ranking.get('total_score', 0)
                    eval_level = ranking.get('eval_level', 'D')
                    
                    # 转换为0-1评分
                    if eval_level == 'S+':
                        normalized_score = min(total_score / 100, 1.0)
                    elif eval_level == 'S':
                        normalized_score = min(total_score / 90, 1.0)
                    elif eval_level == 'A':
                        normalized_score = min(total_score / 80, 1.0)
                    else:
                        normalized_score = min(total_score / 70, 1.0)
                    
                    tenbagger_scores[code] = normalized_score
    except Exception as e:
        log.warn(f"⚠️ 获取十倍股评分失败: {e}")
    
    # 默认值
    for stock in stocks:
        if stock not in tenbagger_scores:
            tenbagger_scores[stock] = 0.5
    
    return tenbagger_scores

# ============================================================
# 评分组合函数
# ============================================================

def combine_scores(
    stocks: List[str],
    tenbagger_scores: Dict[str, float],
    factor_scores: Dict[str, float],
    mainline_scores: Dict[str, float]
) -> Dict[str, float]:
    """
    综合评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:combine_scores()
    """
    final_scores = {}
    
    for stock in stocks:
        tenbagger = tenbagger_scores.get(stock, 0.5)
        factor = factor_scores.get(stock, 0.5)
        mainline = mainline_scores.get(stock, 0.5)
        
        # 标准化因子评分到0-1
        if factor != 0.5:  # 如果有实际计算值
            factor = (factor + 3) / 6  # 假设因子评分在-3到3之间，标准化到0-1
            factor = max(0, min(1, factor))
        
        # 加权组合
        final_score = (
            tenbagger * g.params['tenbagger_weight'] +
            factor * g.params['factor_weight'] +
            mainline * g.params['mainline_weight']
        )
        
        final_scores[stock] = final_score
    
    return final_scores

def select_target_stocks(scores: Dict[str, float], context) -> List[str]:
    """
    选择目标股票
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:select_target_stocks()
    """
    # 按评分排序
    sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # 选择前N只
    max_holdings = g.params['max_holdings']
    target_stocks = [stock for stock, score in sorted_stocks[:max_holdings]]
    
    return target_stocks

# ============================================================
# 交易执行函数
# ============================================================

def execute_rebalance(context, target_stocks: List[str]):
    """
    执行调仓
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:execute_rebalance()
    """
    current_positions = list(context.portfolio.positions.keys())
    
    # 需要卖出的股票（不在目标列表中的持仓）
    to_sell = [s for s in current_positions if s not in target_stocks and context.portfolio.positions[s].total_amount > 0]
    
    # 需要买入的股票（在目标列表中但未持仓或持仓不足）
    to_buy = [s for s in target_stocks if s not in current_positions or context.portfolio.positions[s].total_amount == 0]
    
    # 需要调整的股票（在目标列表中但持仓比例需要调整）
    to_adjust = [s for s in target_stocks if s in current_positions and context.portfolio.positions[s].total_amount > 0]
    
    # 1. 先卖出
    for stock in to_sell:
        try:
            order_target_value(stock, 0)
            log.info(f"🔴 卖出: {stock}")
            # 清理记录
            g.holdings.pop(stock, None)
            g.cost_prices.pop(stock, None)
            g.highest_prices.pop(stock, None)
            g.entry_dates.pop(stock, None)
        except Exception as e:
            log.warn(f"⚠️ 卖出失败 {stock}: {e}")
    
    # 2. 计算目标仓位
    total_value = context.portfolio.total_value
    available_cash = context.portfolio.available_cash
    max_position_value = total_value * g.params['max_total_position']
    target_position_value = (max_position_value - (total_value - available_cash)) / len(target_stocks)
    target_position_value = min(target_position_value, total_value * g.params['single_stock_max'])
    
    # 3. 买入新股票
    for stock in to_buy:
        try:
            order_target_value(stock, target_position_value)
            log.info(f"🟢 买入: {stock}, 目标金额: {target_position_value:.2f}")
            # 记录建仓信息
            g.entry_dates[stock] = context.current_dt.date()
        except Exception as e:
            log.warn(f"⚠️ 买入失败 {stock}: {e}")
    
    # 4. 调整现有持仓
    for stock in to_adjust:
        try:
            current_value = context.portfolio.positions[stock].total_amount * \
                           context.portfolio.positions[stock].price
            if abs(current_value - target_position_value) > total_value * 0.01:  # 差异超过1%才调整
                order_target_value(stock, target_position_value)
                log.info(f"🔄 调整: {stock}, 目标金额: {target_position_value:.2f}")
        except Exception as e:
            log.warn(f"⚠️ 调整失败 {stock}: {e}")

# ============================================================
# 风控模块
# ============================================================

def risk_control(context):
    """
    风险控制
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:risk_control()
    
    功能:
    1. 止盈止损
    2. 移动止损
    3. 最大回撤限制
    4. 仓位管理
    """
    current_data = get_current_data()
    
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.total_amount == 0:
            continue
        
        current_price = current_data[stock].last_price
        cost_price = g.cost_prices.get(stock, pos.avg_cost)
        highest_price = g.highest_prices.get(stock, cost_price)
        
        if cost_price <= 0:
            continue
        
        # 更新最高价
        if current_price > highest_price:
            g.highest_prices[stock] = current_price
            highest_price = current_price
        
        profit = (current_price - cost_price) / cost_price
        drawdown_from_high = (highest_price - current_price) / highest_price if highest_price > 0 else 0
        
        # 1. 止损
        if profit < g.params['stop_loss']:
            log.warn(f'🛑 [止损] {stock} 亏损: {profit*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue
        
        # 2. 止盈
        if profit > g.params['take_profit']:
            log.info(f'🎯 [止盈] {stock} 盈利: {profit*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue
        
        # 3. 移动止损（盈利超过10%后启用）
        if profit > 0.10 and drawdown_from_high > g.params['trailing_stop']:
            log.info(f'📉 [移动止损] {stock} 从高点回撤: {drawdown_from_high*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue

def clean_stock_records(stock):
    """清理股票记录"""
    g.holdings.pop(stock, None)
    g.cost_prices.pop(stock, None)
    g.highest_prices.pop(stock, None)
    g.entry_dates.pop(stock, None)

def update_holdings(context):
    """更新持仓记录"""
    for stock, pos in context.portfolio.positions.items():
        if pos.total_amount > 0:
            if stock not in g.cost_prices:
                g.cost_prices[stock] = pos.avg_cost
            if stock not in g.highest_prices:
                g.highest_prices[stock] = pos.avg_cost
            if stock not in g.entry_dates:
                g.entry_dates[stock] = context.current_dt.date()

# ============================================================
# 辅助函数
# ============================================================

def filter_tradable_stocks(context, stocks: List[str]) -> List[str]:
    """过滤可交易股票"""
    current_data = get_current_data()
    tradable = []
    
    for stock in stocks:
        try:
            # 检查是否可交易
            if stock in current_data and current_data[stock].paused == False:
                # 检查是否ST
                info = jq.get_security_info(stock)
                if info and 'ST' not in info.display_name:
                    tradable.append(stock)
        except:
            continue
    
    return tradable

# ============================================================
# 盘后处理
# ============================================================

def after_market_close(context):
    """
    盘后处理
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:after_market_close()
    """
    # 更新持仓记录
    update_holdings(context)
    
    # 记录每日持仓
    log.info(f"📊 当前持仓数: {len([s for s in context.portfolio.positions.keys() if context.portfolio.positions[s].total_amount > 0])}")
    log.info(f"💰 总资产: {context.portfolio.total_value:.2f}")
    log.info(f"💵 可用现金: {context.portfolio.available_cash:.2f}")






















"""
十倍股综合策略 - 基于TRQuant十倍股框架
========================================

策略特色:
---------
1. 整合所有数据源：JQData、AKShare、MongoDB
2. 使用聚宽因子库：CNE5/CNE6风格因子、聚宽因子
3. 十倍股评估体系：7维度综合评估
4. 增强风控模块：止盈止损、移动止损、仓位管理

代码位置:
---------
- 策略主文件: strategies/tenbagger_comprehensive_strategy.py
- 十倍股评估: mcp_servers/utils/tenbagger_evaluator.py
- 因子管理: core/factors/factor_pool_integration.py
- 风控模块: mcp_servers/utils/portfolio_manager.py

创建时间: 2025-12-26
回测区间: 2024-01-01 至 2025-12-25
基准指数: 000300.XSHG (沪深300)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入JQData
import jqdatasdk as jq

# 导入TRQuant核心模块
try:
    from jqdata.client import JQDataClient
    from core.mainline_scanner import MainlineBasedScanner
    from core.factors.factor_pool_integration import FactorPoolIntegration
    from mcp_servers.utils.tenbagger_evaluator import TenbaggerEvaluator, EvalLevel
    from mcp_servers.utils.portfolio_manager import RiskManager, RiskConfig
    from extension.python.tenbagger_commands import (
        tenbagger_scan_candidates,
        tenbagger_get_rankings
    )
except ImportError as e:
    logging.warning(f"部分模块导入失败: {e}")

# ============================================================
# 全局变量和配置
# ============================================================

g = type('g', (), {})()  # 全局变量容器

# 策略参数
g.params = {
    # 仓位管理
    'max_total_position': 0.90,      # 总仓位上限
    'single_stock_max': 0.10,        # 单票上限
    'min_cash': 0.10,                # 最低现金比例
    'max_holdings': 20,               # 最大持仓数
    
    # 风控参数
    'stop_loss': -0.08,               # 止损比例 -8%
    'take_profit': 0.30,              # 止盈比例 30%
    'trailing_stop': 0.05,            # 移动止损回撤 5%
    'max_drawdown_limit': -0.15,      # 最大回撤限制 -15%
    
    # 十倍股筛选
    'min_tenbagger_score': 65,        # 最低十倍股评分
    'min_eval_level': 'A',            # 最低评估等级
    'preferred_stages': ['S1', 'S2', 'S3'],  # 偏好阶段
    
    # 因子权重
    'tenbagger_weight': 0.40,         # 十倍股评分权重
    'factor_weight': 0.35,            # 聚宽因子权重
    'mainline_weight': 0.25,           # 主线评分权重
    
    # 调仓频率
    'rebalance_frequency': 5,         # 每5个交易日调仓一次
}

# 持仓记录
g.holdings = {}                        # 持仓字典 {code: entry_info}
g.cost_prices = {}                     # 成本价
g.highest_prices = {}                  # 最高价
g.entry_dates = {}                      # 建仓日期
g.last_rebalance_date = None            # 上次调仓日期

# 数据源客户端
g.jq_client = None
g.scanner = None
g.factor_integration = None
g.tenbagger_evaluator = None
g.risk_manager = None

# ============================================================
# 初始化函数
# ============================================================

def initialize(context):
    """
    策略初始化
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:initialize()
    """
    log.info("=" * 80)
    log.info("十倍股综合策略初始化")
    log.info("=" * 80)
    
    # 1. JQData认证
    try:
        from config.config_manager import get_config_manager
        config_manager = get_config_manager()
        jq_config = config_manager.get_jqdata_config()
        username = jq_config.get('username')
        password = jq_config.get('password')
        
        if username and password:
            jq.auth(username, password)
            log.info(f"✅ JQData认证成功: {username}")
            
            # 初始化JQData客户端
            g.jq_client = JQDataClient()
            g.jq_client.authenticate(username, password)
        else:
            log.warn("⚠️ JQData配置未找到，部分功能可能受限")
    except Exception as e:
        log.warn(f"⚠️ JQData初始化失败: {e}")
    
    # 2. 初始化主线扫描器
    try:
        g.scanner = MainlineBasedScanner(jq_client=g.jq_client)
        log.info("✅ 主线扫描器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 主线扫描器初始化失败: {e}")
    
    # 3. 初始化因子集成
    try:
        g.factor_integration = FactorPoolIntegration(jq_client=g.jq_client)
        log.info("✅ 因子集成模块初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 因子集成模块初始化失败: {e}")
    
    # 4. 初始化十倍股评估器
    try:
        g.tenbagger_evaluator = TenbaggerEvaluator()
        log.info("✅ 十倍股评估器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 十倍股评估器初始化失败: {e}")
    
    # 5. 初始化风控管理器
    try:
        risk_config = RiskConfig(
            stop_loss=g.params['stop_loss'],
            take_profit=g.params['take_profit'],
            trailing_stop=g.params['trailing_stop'],
            max_drawdown=g.params['max_drawdown_limit'],
            max_position=g.params['max_total_position'],
            single_stock_max=g.params['single_stock_max']
        )
        g.risk_manager = RiskManager(risk_config)
        log.info("✅ 风控管理器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 风控管理器初始化失败: {e}")
    
    # 6. 设置基准和手续费
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    
    # 手续费设置
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            close_today_commission=0,
            min_commission=5
        ),
        type='stock'
    )
    
    # 7. 运行函数设置
    run_daily(before_market_open, time='before_open', reference_security='000300.XSHG')
    run_daily(market_open, time='open', reference_security='000300.XSHG')
    run_daily(after_market_close, time='after_close', reference_security='000300.XSHG')
    
    log.info("=" * 80)
    log.info("策略初始化完成")
    log.info("=" * 80)

# ============================================================
# 盘前准备
# ============================================================

def before_market_open(context):
    """
    盘前准备
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:before_market_open()
    """
    log.info("📅 盘前准备开始")
    
    # 检查是否需要调仓
    current_date = context.current_dt.date()
    if g.last_rebalance_date is None or \
       (current_date - g.last_rebalance_date).days >= g.params['rebalance_frequency']:
        log.info(f"🔄 触发调仓检查 (上次调仓: {g.last_rebalance_date})")
        g.last_rebalance_date = current_date
    
    # 更新持仓记录
    update_holdings(context)

# ============================================================
# 开盘交易
# ============================================================

def market_open(context):
    """
    开盘交易逻辑
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:market_open()
    """
    log.info("🚀 开盘交易开始")
    
    # 1. 风控检查（优先执行）
    risk_control(context)
    
    # 2. 检查是否需要调仓
    current_date = context.current_dt.date()
    if g.last_rebalance_date == current_date:
        # 执行调仓
        rebalance(context)
    else:
        log.info("⏭️ 今日不调仓，继续持有")

# ============================================================
# 调仓逻辑
# ============================================================

def rebalance(context):
    """
    调仓逻辑
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:rebalance()
    
    流程:
    1. 获取十倍股候选池
    2. 计算聚宽因子评分
    3. 获取主线评分
    4. 综合评分排序
    5. 执行买卖操作
    """
    log.info("=" * 80)
    log.info("🔄 开始调仓")
    log.info("=" * 80)
    
    current_date = context.current_dt.date()
    current_datetime = context.current_dt
    
    # 1. 获取十倍股候选池
    candidate_stocks = get_tenbagger_candidates(context, current_date)
    log.info(f"📊 十倍股候选池: {len(candidate_stocks)} 只股票")
    
    if not candidate_stocks:
        log.warn("⚠️ 未找到符合条件的候选股票，保持当前持仓")
        return
    
    # 2. 计算聚宽因子评分
    factor_scores = calculate_jq_factors(context, candidate_stocks, current_date)
    log.info(f"📈 聚宽因子评分完成: {len(factor_scores)} 只股票")
    
    # 3. 获取主线评分
    mainline_scores = get_mainline_scores(context, candidate_stocks, current_date)
    log.info(f"🎯 主线评分完成: {len(mainline_scores)} 只股票")
    
    # 4. 获取十倍股评分
    tenbagger_scores = get_tenbagger_scores(context, candidate_stocks, current_date)
    log.info(f"⭐ 十倍股评分完成: {len(tenbagger_scores)} 只股票")
    
    # 5. 综合评分
    final_scores = combine_scores(
        candidate_stocks,
        tenbagger_scores,
        factor_scores,
        mainline_scores
    )
    
    # 6. 排序并选择目标股票
    target_stocks = select_target_stocks(final_scores, context)
    log.info(f"🎯 目标持仓: {len(target_stocks)} 只股票")
    
    # 7. 执行调仓
    execute_rebalance(context, target_stocks)

# ============================================================
# 数据获取函数
# ============================================================

def get_tenbagger_candidates(context, date) -> List[str]:
    """
    获取十倍股候选池
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_tenbagger_candidates()
    
    数据源: MongoDB (通过tenbagger_commands)
    """
    try:
        # 从数据库获取十倍股排名
        rankings = tenbagger_get_rankings(
            limit=100,
            min_score=g.params['min_tenbagger_score'],
            min_level=g.params['min_eval_level']
        )
        
        if rankings and len(rankings) > 0:
            # 提取股票代码
            stocks = [r.get('code', '') for r in rankings if r.get('code')]
            # 过滤掉ST、停牌等
            stocks = filter_tradable_stocks(context, stocks)
            return stocks[:50]  # 取前50只
    except Exception as e:
        log.warn(f"⚠️ 获取十倍股候选池失败: {e}")
    
    # 备用方案：从主线扫描获取
    try:
        if g.scanner:
            mainlines = g.scanner.scan_mainlines(date)
            stocks = []
            for mainline in mainlines[:5]:  # 取前5条主线
                stocks.extend(mainline.get('stocks', []))
            stocks = list(set(stocks))[:50]
            return filter_tradable_stocks(context, stocks)
    except Exception as e:
        log.warn(f"⚠️ 备用方案获取候选池失败: {e}")
    
    return []

def calculate_jq_factors(context, stocks: List[str], date) -> Dict[str, float]:
    """
    计算聚宽因子评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:calculate_jq_factors()
    
    使用的因子:
    - CNE5风格因子 (get_factor_values)
    - CNE6风格因子pro (get_factor_values)
    - 聚宽因子 (get_all_factors)
    """
    factor_scores = {}
    
    try:
        # 1. CNE5风格因子
        try:
            cne5_factors = ['size', 'beta', 'momentum', 'reversal', 'volatility']
            cne5_scores = {}
            for factor in cne5_factors:
                try:
                    values = jq.get_factor_values(
                        securities=stocks,
                        factors=[factor],
                        count=1,
                        end_date=date
                    )
                    if values is not None and not values.empty:
                        # 标准化并加权
                        normalized = (values[factor] - values[factor].mean()) / values[factor].std()
                        cne5_scores[factor] = normalized
                except Exception as e:
                    log.debug(f"CNE5因子 {factor} 计算失败: {e}")
            
            # 综合CNE5评分
            if cne5_scores:
                cne5_df = pd.DataFrame(cne5_scores)
                cne5_combined = cne5_df.mean(axis=1)
                for stock in stocks:
                    if stock in cne5_combined.index:
                        factor_scores[stock] = factor_scores.get(stock, 0) + cne5_combined[stock] * 0.3
        except Exception as e:
            log.warn(f"⚠️ CNE5因子计算失败: {e}")
        
        # 2. CNE6风格因子pro
        try:
            cne6_factors = ['size', 'beta', 'momentum', 'reversal', 'volatility', 'growth', 'earnings_yield']
            cne6_scores = {}
            for factor in cne6_factors:
                try:
                    values = jq.get_factor_values(
                        securities=stocks,
                        factors=[factor],
                        count=1,
                        end_date=date
                    )
                    if values is not None and not values.empty:
                        normalized = (values[factor] - values[factor].mean()) / values[factor].std()
                        cne6_scores[factor] = normalized
                except Exception as e:
                    log.debug(f"CNE6因子 {factor} 计算失败: {e}")
            
            if cne6_scores:
                cne6_df = pd.DataFrame(cne6_scores)
                cne6_combined = cne6_df.mean(axis=1)
                for stock in stocks:
                    if stock in cne6_combined.index:
                        factor_scores[stock] = factor_scores.get(stock, 0) + cne6_combined[stock] * 0.4
        except Exception as e:
            log.warn(f"⚠️ CNE6因子计算失败: {e}")
        
        # 3. 聚宽因子库
        try:
            if g.factor_integration:
                jq_factor_scores = g.factor_integration.process_candidate_pool(
                    stocks=stocks,
                    date=date,
                    period='medium',
                    top_n=len(stocks)
                )
                for signal in jq_factor_scores:
                    stock = signal.code
                    factor_scores[stock] = factor_scores.get(stock, 0) + signal.factor_score * 0.3
        except Exception as e:
            log.warn(f"⚠️ 聚宽因子库计算失败: {e}")
        
    except Exception as e:
        log.warn(f"⚠️ 因子计算总体失败: {e}")
    
    return factor_scores

def get_mainline_scores(context, stocks: List[str], date) -> Dict[str, float]:
    """
    获取主线评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_mainline_scores()
    
    数据源: MainlineBasedScanner
    """
    mainline_scores = {}
    
    try:
        if g.scanner:
            mainlines = g.scanner.scan_mainlines(date)
            # 构建股票到主线的映射
            stock_to_mainline = {}
            for mainline in mainlines:
                mainline_name = mainline.get('name', '')
                mainline_stocks = mainline.get('stocks', [])
                mainline_score = mainline.get('score', 0.5)
                for stock in mainline_stocks:
                    if stock in stocks:
                        if stock not in stock_to_mainline:
                            stock_to_mainline[stock] = []
                        stock_to_mainline[stock].append(mainline_score)
            
            # 计算平均主线评分
            for stock in stocks:
                if stock in stock_to_mainline:
                    scores = stock_to_mainline[stock]
                    mainline_scores[stock] = np.mean(scores) if scores else 0.5
                else:
                    mainline_scores[stock] = 0.5  # 默认值
    except Exception as e:
        log.warn(f"⚠️ 获取主线评分失败: {e}")
        # 默认值
        for stock in stocks:
            mainline_scores[stock] = 0.5
    
    return mainline_scores

def get_tenbagger_scores(context, stocks: List[str], date) -> Dict[str, float]:
    """
    获取十倍股评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_tenbagger_scores()
    
    数据源: MongoDB (通过tenbagger_commands)
    """
    tenbagger_scores = {}
    
    try:
        rankings = tenbagger_get_rankings(limit=200)
        if rankings:
            for ranking in rankings:
                code = ranking.get('code', '')
                if code in stocks:
                    total_score = ranking.get('total_score', 0)
                    eval_level = ranking.get('eval_level', 'D')
                    
                    # 转换为0-1评分
                    if eval_level == 'S+':
                        normalized_score = min(total_score / 100, 1.0)
                    elif eval_level == 'S':
                        normalized_score = min(total_score / 90, 1.0)
                    elif eval_level == 'A':
                        normalized_score = min(total_score / 80, 1.0)
                    else:
                        normalized_score = min(total_score / 70, 1.0)
                    
                    tenbagger_scores[code] = normalized_score
    except Exception as e:
        log.warn(f"⚠️ 获取十倍股评分失败: {e}")
    
    # 默认值
    for stock in stocks:
        if stock not in tenbagger_scores:
            tenbagger_scores[stock] = 0.5
    
    return tenbagger_scores

# ============================================================
# 评分组合函数
# ============================================================

def combine_scores(
    stocks: List[str],
    tenbagger_scores: Dict[str, float],
    factor_scores: Dict[str, float],
    mainline_scores: Dict[str, float]
) -> Dict[str, float]:
    """
    综合评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:combine_scores()
    """
    final_scores = {}
    
    for stock in stocks:
        tenbagger = tenbagger_scores.get(stock, 0.5)
        factor = factor_scores.get(stock, 0.5)
        mainline = mainline_scores.get(stock, 0.5)
        
        # 标准化因子评分到0-1
        if factor != 0.5:  # 如果有实际计算值
            factor = (factor + 3) / 6  # 假设因子评分在-3到3之间，标准化到0-1
            factor = max(0, min(1, factor))
        
        # 加权组合
        final_score = (
            tenbagger * g.params['tenbagger_weight'] +
            factor * g.params['factor_weight'] +
            mainline * g.params['mainline_weight']
        )
        
        final_scores[stock] = final_score
    
    return final_scores

def select_target_stocks(scores: Dict[str, float], context) -> List[str]:
    """
    选择目标股票
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:select_target_stocks()
    """
    # 按评分排序
    sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # 选择前N只
    max_holdings = g.params['max_holdings']
    target_stocks = [stock for stock, score in sorted_stocks[:max_holdings]]
    
    return target_stocks

# ============================================================
# 交易执行函数
# ============================================================

def execute_rebalance(context, target_stocks: List[str]):
    """
    执行调仓
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:execute_rebalance()
    """
    current_positions = list(context.portfolio.positions.keys())
    
    # 需要卖出的股票（不在目标列表中的持仓）
    to_sell = [s for s in current_positions if s not in target_stocks and context.portfolio.positions[s].total_amount > 0]
    
    # 需要买入的股票（在目标列表中但未持仓或持仓不足）
    to_buy = [s for s in target_stocks if s not in current_positions or context.portfolio.positions[s].total_amount == 0]
    
    # 需要调整的股票（在目标列表中但持仓比例需要调整）
    to_adjust = [s for s in target_stocks if s in current_positions and context.portfolio.positions[s].total_amount > 0]
    
    # 1. 先卖出
    for stock in to_sell:
        try:
            order_target_value(stock, 0)
            log.info(f"🔴 卖出: {stock}")
            # 清理记录
            g.holdings.pop(stock, None)
            g.cost_prices.pop(stock, None)
            g.highest_prices.pop(stock, None)
            g.entry_dates.pop(stock, None)
        except Exception as e:
            log.warn(f"⚠️ 卖出失败 {stock}: {e}")
    
    # 2. 计算目标仓位
    total_value = context.portfolio.total_value
    available_cash = context.portfolio.available_cash
    max_position_value = total_value * g.params['max_total_position']
    target_position_value = (max_position_value - (total_value - available_cash)) / len(target_stocks)
    target_position_value = min(target_position_value, total_value * g.params['single_stock_max'])
    
    # 3. 买入新股票
    for stock in to_buy:
        try:
            order_target_value(stock, target_position_value)
            log.info(f"🟢 买入: {stock}, 目标金额: {target_position_value:.2f}")
            # 记录建仓信息
            g.entry_dates[stock] = context.current_dt.date()
        except Exception as e:
            log.warn(f"⚠️ 买入失败 {stock}: {e}")
    
    # 4. 调整现有持仓
    for stock in to_adjust:
        try:
            current_value = context.portfolio.positions[stock].total_amount * \
                           context.portfolio.positions[stock].price
            if abs(current_value - target_position_value) > total_value * 0.01:  # 差异超过1%才调整
                order_target_value(stock, target_position_value)
                log.info(f"🔄 调整: {stock}, 目标金额: {target_position_value:.2f}")
        except Exception as e:
            log.warn(f"⚠️ 调整失败 {stock}: {e}")

# ============================================================
# 风控模块
# ============================================================

def risk_control(context):
    """
    风险控制
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:risk_control()
    
    功能:
    1. 止盈止损
    2. 移动止损
    3. 最大回撤限制
    4. 仓位管理
    """
    current_data = get_current_data()
    
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.total_amount == 0:
            continue
        
        current_price = current_data[stock].last_price
        cost_price = g.cost_prices.get(stock, pos.avg_cost)
        highest_price = g.highest_prices.get(stock, cost_price)
        
        if cost_price <= 0:
            continue
        
        # 更新最高价
        if current_price > highest_price:
            g.highest_prices[stock] = current_price
            highest_price = current_price
        
        profit = (current_price - cost_price) / cost_price
        drawdown_from_high = (highest_price - current_price) / highest_price if highest_price > 0 else 0
        
        # 1. 止损
        if profit < g.params['stop_loss']:
            log.warn(f'🛑 [止损] {stock} 亏损: {profit*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue
        
        # 2. 止盈
        if profit > g.params['take_profit']:
            log.info(f'🎯 [止盈] {stock} 盈利: {profit*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue
        
        # 3. 移动止损（盈利超过10%后启用）
        if profit > 0.10 and drawdown_from_high > g.params['trailing_stop']:
            log.info(f'📉 [移动止损] {stock} 从高点回撤: {drawdown_from_high*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue

def clean_stock_records(stock):
    """清理股票记录"""
    g.holdings.pop(stock, None)
    g.cost_prices.pop(stock, None)
    g.highest_prices.pop(stock, None)
    g.entry_dates.pop(stock, None)

def update_holdings(context):
    """更新持仓记录"""
    for stock, pos in context.portfolio.positions.items():
        if pos.total_amount > 0:
            if stock not in g.cost_prices:
                g.cost_prices[stock] = pos.avg_cost
            if stock not in g.highest_prices:
                g.highest_prices[stock] = pos.avg_cost
            if stock not in g.entry_dates:
                g.entry_dates[stock] = context.current_dt.date()

# ============================================================
# 辅助函数
# ============================================================

def filter_tradable_stocks(context, stocks: List[str]) -> List[str]:
    """过滤可交易股票"""
    current_data = get_current_data()
    tradable = []
    
    for stock in stocks:
        try:
            # 检查是否可交易
            if stock in current_data and current_data[stock].paused == False:
                # 检查是否ST
                info = jq.get_security_info(stock)
                if info and 'ST' not in info.display_name:
                    tradable.append(stock)
        except:
            continue
    
    return tradable

# ============================================================
# 盘后处理
# ============================================================

def after_market_close(context):
    """
    盘后处理
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:after_market_close()
    """
    # 更新持仓记录
    update_holdings(context)
    
    # 记录每日持仓
    log.info(f"📊 当前持仓数: {len([s for s in context.portfolio.positions.keys() if context.portfolio.positions[s].total_amount > 0])}")
    log.info(f"💰 总资产: {context.portfolio.total_value:.2f}")
    log.info(f"💵 可用现金: {context.portfolio.available_cash:.2f}")



"""
十倍股综合策略 - 基于TRQuant十倍股框架
========================================

策略特色:
---------
1. 整合所有数据源：JQData、AKShare、MongoDB
2. 使用聚宽因子库：CNE5/CNE6风格因子、聚宽因子
3. 十倍股评估体系：7维度综合评估
4. 增强风控模块：止盈止损、移动止损、仓位管理

代码位置:
---------
- 策略主文件: strategies/tenbagger_comprehensive_strategy.py
- 十倍股评估: mcp_servers/utils/tenbagger_evaluator.py
- 因子管理: core/factors/factor_pool_integration.py
- 风控模块: mcp_servers/utils/portfolio_manager.py

创建时间: 2025-12-26
回测区间: 2024-01-01 至 2025-12-25
基准指数: 000300.XSHG (沪深300)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入JQData
import jqdatasdk as jq

# 导入TRQuant核心模块
try:
    from jqdata.client import JQDataClient
    from core.mainline_scanner import MainlineBasedScanner
    from core.factors.factor_pool_integration import FactorPoolIntegration
    from mcp_servers.utils.tenbagger_evaluator import TenbaggerEvaluator, EvalLevel
    from mcp_servers.utils.portfolio_manager import RiskManager, RiskConfig
    from extension.python.tenbagger_commands import (
        tenbagger_scan_candidates,
        tenbagger_get_rankings
    )
except ImportError as e:
    logging.warning(f"部分模块导入失败: {e}")

# ============================================================
# 全局变量和配置
# ============================================================

g = type('g', (), {})()  # 全局变量容器

# 策略参数
g.params = {
    # 仓位管理
    'max_total_position': 0.90,      # 总仓位上限
    'single_stock_max': 0.10,        # 单票上限
    'min_cash': 0.10,                # 最低现金比例
    'max_holdings': 20,               # 最大持仓数
    
    # 风控参数
    'stop_loss': -0.08,               # 止损比例 -8%
    'take_profit': 0.30,              # 止盈比例 30%
    'trailing_stop': 0.05,            # 移动止损回撤 5%
    'max_drawdown_limit': -0.15,      # 最大回撤限制 -15%
    
    # 十倍股筛选
    'min_tenbagger_score': 65,        # 最低十倍股评分
    'min_eval_level': 'A',            # 最低评估等级
    'preferred_stages': ['S1', 'S2', 'S3'],  # 偏好阶段
    
    # 因子权重
    'tenbagger_weight': 0.40,         # 十倍股评分权重
    'factor_weight': 0.35,            # 聚宽因子权重
    'mainline_weight': 0.25,           # 主线评分权重
    
    # 调仓频率
    'rebalance_frequency': 5,         # 每5个交易日调仓一次
}

# 持仓记录
g.holdings = {}                        # 持仓字典 {code: entry_info}
g.cost_prices = {}                     # 成本价
g.highest_prices = {}                  # 最高价
g.entry_dates = {}                      # 建仓日期
g.last_rebalance_date = None            # 上次调仓日期

# 数据源客户端
g.jq_client = None
g.scanner = None
g.factor_integration = None
g.tenbagger_evaluator = None
g.risk_manager = None

# ============================================================
# 初始化函数
# ============================================================

def initialize(context):
    """
    策略初始化
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:initialize()
    """
    log.info("=" * 80)
    log.info("十倍股综合策略初始化")
    log.info("=" * 80)
    
    # 1. JQData认证
    try:
        from config.config_manager import get_config_manager
        config_manager = get_config_manager()
        jq_config = config_manager.get_jqdata_config()
        username = jq_config.get('username')
        password = jq_config.get('password')
        
        if username and password:
            jq.auth(username, password)
            log.info(f"✅ JQData认证成功: {username}")
            
            # 初始化JQData客户端
            g.jq_client = JQDataClient()
            g.jq_client.authenticate(username, password)
        else:
            log.warn("⚠️ JQData配置未找到，部分功能可能受限")
    except Exception as e:
        log.warn(f"⚠️ JQData初始化失败: {e}")
    
    # 2. 初始化主线扫描器
    try:
        g.scanner = MainlineBasedScanner(jq_client=g.jq_client)
        log.info("✅ 主线扫描器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 主线扫描器初始化失败: {e}")
    
    # 3. 初始化因子集成
    try:
        g.factor_integration = FactorPoolIntegration(jq_client=g.jq_client)
        log.info("✅ 因子集成模块初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 因子集成模块初始化失败: {e}")
    
    # 4. 初始化十倍股评估器
    try:
        g.tenbagger_evaluator = TenbaggerEvaluator()
        log.info("✅ 十倍股评估器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 十倍股评估器初始化失败: {e}")
    
    # 5. 初始化风控管理器
    try:
        risk_config = RiskConfig(
            stop_loss=g.params['stop_loss'],
            take_profit=g.params['take_profit'],
            trailing_stop=g.params['trailing_stop'],
            max_drawdown=g.params['max_drawdown_limit'],
            max_position=g.params['max_total_position'],
            single_stock_max=g.params['single_stock_max']
        )
        g.risk_manager = RiskManager(risk_config)
        log.info("✅ 风控管理器初始化成功")
    except Exception as e:
        log.warn(f"⚠️ 风控管理器初始化失败: {e}")
    
    # 6. 设置基准和手续费
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    
    # 手续费设置
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            close_today_commission=0,
            min_commission=5
        ),
        type='stock'
    )
    
    # 7. 运行函数设置
    run_daily(before_market_open, time='before_open', reference_security='000300.XSHG')
    run_daily(market_open, time='open', reference_security='000300.XSHG')
    run_daily(after_market_close, time='after_close', reference_security='000300.XSHG')
    
    log.info("=" * 80)
    log.info("策略初始化完成")
    log.info("=" * 80)

# ============================================================
# 盘前准备
# ============================================================

def before_market_open(context):
    """
    盘前准备
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:before_market_open()
    """
    log.info("📅 盘前准备开始")
    
    # 检查是否需要调仓
    current_date = context.current_dt.date()
    if g.last_rebalance_date is None or \
       (current_date - g.last_rebalance_date).days >= g.params['rebalance_frequency']:
        log.info(f"🔄 触发调仓检查 (上次调仓: {g.last_rebalance_date})")
        g.last_rebalance_date = current_date
    
    # 更新持仓记录
    update_holdings(context)

# ============================================================
# 开盘交易
# ============================================================

def market_open(context):
    """
    开盘交易逻辑
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:market_open()
    """
    log.info("🚀 开盘交易开始")
    
    # 1. 风控检查（优先执行）
    risk_control(context)
    
    # 2. 检查是否需要调仓
    current_date = context.current_dt.date()
    if g.last_rebalance_date == current_date:
        # 执行调仓
        rebalance(context)
    else:
        log.info("⏭️ 今日不调仓，继续持有")

# ============================================================
# 调仓逻辑
# ============================================================

def rebalance(context):
    """
    调仓逻辑
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:rebalance()
    
    流程:
    1. 获取十倍股候选池
    2. 计算聚宽因子评分
    3. 获取主线评分
    4. 综合评分排序
    5. 执行买卖操作
    """
    log.info("=" * 80)
    log.info("🔄 开始调仓")
    log.info("=" * 80)
    
    current_date = context.current_dt.date()
    current_datetime = context.current_dt
    
    # 1. 获取十倍股候选池
    candidate_stocks = get_tenbagger_candidates(context, current_date)
    log.info(f"📊 十倍股候选池: {len(candidate_stocks)} 只股票")
    
    if not candidate_stocks:
        log.warn("⚠️ 未找到符合条件的候选股票，保持当前持仓")
        return
    
    # 2. 计算聚宽因子评分
    factor_scores = calculate_jq_factors(context, candidate_stocks, current_date)
    log.info(f"📈 聚宽因子评分完成: {len(factor_scores)} 只股票")
    
    # 3. 获取主线评分
    mainline_scores = get_mainline_scores(context, candidate_stocks, current_date)
    log.info(f"🎯 主线评分完成: {len(mainline_scores)} 只股票")
    
    # 4. 获取十倍股评分
    tenbagger_scores = get_tenbagger_scores(context, candidate_stocks, current_date)
    log.info(f"⭐ 十倍股评分完成: {len(tenbagger_scores)} 只股票")
    
    # 5. 综合评分
    final_scores = combine_scores(
        candidate_stocks,
        tenbagger_scores,
        factor_scores,
        mainline_scores
    )
    
    # 6. 排序并选择目标股票
    target_stocks = select_target_stocks(final_scores, context)
    log.info(f"🎯 目标持仓: {len(target_stocks)} 只股票")
    
    # 7. 执行调仓
    execute_rebalance(context, target_stocks)

# ============================================================
# 数据获取函数
# ============================================================

def get_tenbagger_candidates(context, date) -> List[str]:
    """
    获取十倍股候选池
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_tenbagger_candidates()
    
    数据源: MongoDB (通过tenbagger_commands)
    """
    try:
        # 从数据库获取十倍股排名
        rankings = tenbagger_get_rankings(
            limit=100,
            min_score=g.params['min_tenbagger_score'],
            min_level=g.params['min_eval_level']
        )
        
        if rankings and len(rankings) > 0:
            # 提取股票代码
            stocks = [r.get('code', '') for r in rankings if r.get('code')]
            # 过滤掉ST、停牌等
            stocks = filter_tradable_stocks(context, stocks)
            return stocks[:50]  # 取前50只
    except Exception as e:
        log.warn(f"⚠️ 获取十倍股候选池失败: {e}")
    
    # 备用方案：从主线扫描获取
    try:
        if g.scanner:
            mainlines = g.scanner.scan_mainlines(date)
            stocks = []
            for mainline in mainlines[:5]:  # 取前5条主线
                stocks.extend(mainline.get('stocks', []))
            stocks = list(set(stocks))[:50]
            return filter_tradable_stocks(context, stocks)
    except Exception as e:
        log.warn(f"⚠️ 备用方案获取候选池失败: {e}")
    
    return []

def calculate_jq_factors(context, stocks: List[str], date) -> Dict[str, float]:
    """
    计算聚宽因子评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:calculate_jq_factors()
    
    使用的因子:
    - CNE5风格因子 (get_factor_values)
    - CNE6风格因子pro (get_factor_values)
    - 聚宽因子 (get_all_factors)
    """
    factor_scores = {}
    
    try:
        # 1. CNE5风格因子
        try:
            cne5_factors = ['size', 'beta', 'momentum', 'reversal', 'volatility']
            cne5_scores = {}
            for factor in cne5_factors:
                try:
                    values = jq.get_factor_values(
                        securities=stocks,
                        factors=[factor],
                        count=1,
                        end_date=date
                    )
                    if values is not None and not values.empty:
                        # 标准化并加权
                        normalized = (values[factor] - values[factor].mean()) / values[factor].std()
                        cne5_scores[factor] = normalized
                except Exception as e:
                    log.debug(f"CNE5因子 {factor} 计算失败: {e}")
            
            # 综合CNE5评分
            if cne5_scores:
                cne5_df = pd.DataFrame(cne5_scores)
                cne5_combined = cne5_df.mean(axis=1)
                for stock in stocks:
                    if stock in cne5_combined.index:
                        factor_scores[stock] = factor_scores.get(stock, 0) + cne5_combined[stock] * 0.3
        except Exception as e:
            log.warn(f"⚠️ CNE5因子计算失败: {e}")
        
        # 2. CNE6风格因子pro
        try:
            cne6_factors = ['size', 'beta', 'momentum', 'reversal', 'volatility', 'growth', 'earnings_yield']
            cne6_scores = {}
            for factor in cne6_factors:
                try:
                    values = jq.get_factor_values(
                        securities=stocks,
                        factors=[factor],
                        count=1,
                        end_date=date
                    )
                    if values is not None and not values.empty:
                        normalized = (values[factor] - values[factor].mean()) / values[factor].std()
                        cne6_scores[factor] = normalized
                except Exception as e:
                    log.debug(f"CNE6因子 {factor} 计算失败: {e}")
            
            if cne6_scores:
                cne6_df = pd.DataFrame(cne6_scores)
                cne6_combined = cne6_df.mean(axis=1)
                for stock in stocks:
                    if stock in cne6_combined.index:
                        factor_scores[stock] = factor_scores.get(stock, 0) + cne6_combined[stock] * 0.4
        except Exception as e:
            log.warn(f"⚠️ CNE6因子计算失败: {e}")
        
        # 3. 聚宽因子库
        try:
            if g.factor_integration:
                jq_factor_scores = g.factor_integration.process_candidate_pool(
                    stocks=stocks,
                    date=date,
                    period='medium',
                    top_n=len(stocks)
                )
                for signal in jq_factor_scores:
                    stock = signal.code
                    factor_scores[stock] = factor_scores.get(stock, 0) + signal.factor_score * 0.3
        except Exception as e:
            log.warn(f"⚠️ 聚宽因子库计算失败: {e}")
        
    except Exception as e:
        log.warn(f"⚠️ 因子计算总体失败: {e}")
    
    return factor_scores

def get_mainline_scores(context, stocks: List[str], date) -> Dict[str, float]:
    """
    获取主线评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_mainline_scores()
    
    数据源: MainlineBasedScanner
    """
    mainline_scores = {}
    
    try:
        if g.scanner:
            mainlines = g.scanner.scan_mainlines(date)
            # 构建股票到主线的映射
            stock_to_mainline = {}
            for mainline in mainlines:
                mainline_name = mainline.get('name', '')
                mainline_stocks = mainline.get('stocks', [])
                mainline_score = mainline.get('score', 0.5)
                for stock in mainline_stocks:
                    if stock in stocks:
                        if stock not in stock_to_mainline:
                            stock_to_mainline[stock] = []
                        stock_to_mainline[stock].append(mainline_score)
            
            # 计算平均主线评分
            for stock in stocks:
                if stock in stock_to_mainline:
                    scores = stock_to_mainline[stock]
                    mainline_scores[stock] = np.mean(scores) if scores else 0.5
                else:
                    mainline_scores[stock] = 0.5  # 默认值
    except Exception as e:
        log.warn(f"⚠️ 获取主线评分失败: {e}")
        # 默认值
        for stock in stocks:
            mainline_scores[stock] = 0.5
    
    return mainline_scores

def get_tenbagger_scores(context, stocks: List[str], date) -> Dict[str, float]:
    """
    获取十倍股评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:get_tenbagger_scores()
    
    数据源: MongoDB (通过tenbagger_commands)
    """
    tenbagger_scores = {}
    
    try:
        rankings = tenbagger_get_rankings(limit=200)
        if rankings:
            for ranking in rankings:
                code = ranking.get('code', '')
                if code in stocks:
                    total_score = ranking.get('total_score', 0)
                    eval_level = ranking.get('eval_level', 'D')
                    
                    # 转换为0-1评分
                    if eval_level == 'S+':
                        normalized_score = min(total_score / 100, 1.0)
                    elif eval_level == 'S':
                        normalized_score = min(total_score / 90, 1.0)
                    elif eval_level == 'A':
                        normalized_score = min(total_score / 80, 1.0)
                    else:
                        normalized_score = min(total_score / 70, 1.0)
                    
                    tenbagger_scores[code] = normalized_score
    except Exception as e:
        log.warn(f"⚠️ 获取十倍股评分失败: {e}")
    
    # 默认值
    for stock in stocks:
        if stock not in tenbagger_scores:
            tenbagger_scores[stock] = 0.5
    
    return tenbagger_scores

# ============================================================
# 评分组合函数
# ============================================================

def combine_scores(
    stocks: List[str],
    tenbagger_scores: Dict[str, float],
    factor_scores: Dict[str, float],
    mainline_scores: Dict[str, float]
) -> Dict[str, float]:
    """
    综合评分
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:combine_scores()
    """
    final_scores = {}
    
    for stock in stocks:
        tenbagger = tenbagger_scores.get(stock, 0.5)
        factor = factor_scores.get(stock, 0.5)
        mainline = mainline_scores.get(stock, 0.5)
        
        # 标准化因子评分到0-1
        if factor != 0.5:  # 如果有实际计算值
            factor = (factor + 3) / 6  # 假设因子评分在-3到3之间，标准化到0-1
            factor = max(0, min(1, factor))
        
        # 加权组合
        final_score = (
            tenbagger * g.params['tenbagger_weight'] +
            factor * g.params['factor_weight'] +
            mainline * g.params['mainline_weight']
        )
        
        final_scores[stock] = final_score
    
    return final_scores

def select_target_stocks(scores: Dict[str, float], context) -> List[str]:
    """
    选择目标股票
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:select_target_stocks()
    """
    # 按评分排序
    sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # 选择前N只
    max_holdings = g.params['max_holdings']
    target_stocks = [stock for stock, score in sorted_stocks[:max_holdings]]
    
    return target_stocks

# ============================================================
# 交易执行函数
# ============================================================

def execute_rebalance(context, target_stocks: List[str]):
    """
    执行调仓
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:execute_rebalance()
    """
    current_positions = list(context.portfolio.positions.keys())
    
    # 需要卖出的股票（不在目标列表中的持仓）
    to_sell = [s for s in current_positions if s not in target_stocks and context.portfolio.positions[s].total_amount > 0]
    
    # 需要买入的股票（在目标列表中但未持仓或持仓不足）
    to_buy = [s for s in target_stocks if s not in current_positions or context.portfolio.positions[s].total_amount == 0]
    
    # 需要调整的股票（在目标列表中但持仓比例需要调整）
    to_adjust = [s for s in target_stocks if s in current_positions and context.portfolio.positions[s].total_amount > 0]
    
    # 1. 先卖出
    for stock in to_sell:
        try:
            order_target_value(stock, 0)
            log.info(f"🔴 卖出: {stock}")
            # 清理记录
            g.holdings.pop(stock, None)
            g.cost_prices.pop(stock, None)
            g.highest_prices.pop(stock, None)
            g.entry_dates.pop(stock, None)
        except Exception as e:
            log.warn(f"⚠️ 卖出失败 {stock}: {e}")
    
    # 2. 计算目标仓位
    total_value = context.portfolio.total_value
    available_cash = context.portfolio.available_cash
    max_position_value = total_value * g.params['max_total_position']
    target_position_value = (max_position_value - (total_value - available_cash)) / len(target_stocks)
    target_position_value = min(target_position_value, total_value * g.params['single_stock_max'])
    
    # 3. 买入新股票
    for stock in to_buy:
        try:
            order_target_value(stock, target_position_value)
            log.info(f"🟢 买入: {stock}, 目标金额: {target_position_value:.2f}")
            # 记录建仓信息
            g.entry_dates[stock] = context.current_dt.date()
        except Exception as e:
            log.warn(f"⚠️ 买入失败 {stock}: {e}")
    
    # 4. 调整现有持仓
    for stock in to_adjust:
        try:
            current_value = context.portfolio.positions[stock].total_amount * \
                           context.portfolio.positions[stock].price
            if abs(current_value - target_position_value) > total_value * 0.01:  # 差异超过1%才调整
                order_target_value(stock, target_position_value)
                log.info(f"🔄 调整: {stock}, 目标金额: {target_position_value:.2f}")
        except Exception as e:
            log.warn(f"⚠️ 调整失败 {stock}: {e}")

# ============================================================
# 风控模块
# ============================================================

def risk_control(context):
    """
    风险控制
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:risk_control()
    
    功能:
    1. 止盈止损
    2. 移动止损
    3. 最大回撤限制
    4. 仓位管理
    """
    current_data = get_current_data()
    
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.total_amount == 0:
            continue
        
        current_price = current_data[stock].last_price
        cost_price = g.cost_prices.get(stock, pos.avg_cost)
        highest_price = g.highest_prices.get(stock, cost_price)
        
        if cost_price <= 0:
            continue
        
        # 更新最高价
        if current_price > highest_price:
            g.highest_prices[stock] = current_price
            highest_price = current_price
        
        profit = (current_price - cost_price) / cost_price
        drawdown_from_high = (highest_price - current_price) / highest_price if highest_price > 0 else 0
        
        # 1. 止损
        if profit < g.params['stop_loss']:
            log.warn(f'🛑 [止损] {stock} 亏损: {profit*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue
        
        # 2. 止盈
        if profit > g.params['take_profit']:
            log.info(f'🎯 [止盈] {stock} 盈利: {profit*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue
        
        # 3. 移动止损（盈利超过10%后启用）
        if profit > 0.10 and drawdown_from_high > g.params['trailing_stop']:
            log.info(f'📉 [移动止损] {stock} 从高点回撤: {drawdown_from_high*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
            continue

def clean_stock_records(stock):
    """清理股票记录"""
    g.holdings.pop(stock, None)
    g.cost_prices.pop(stock, None)
    g.highest_prices.pop(stock, None)
    g.entry_dates.pop(stock, None)

def update_holdings(context):
    """更新持仓记录"""
    for stock, pos in context.portfolio.positions.items():
        if pos.total_amount > 0:
            if stock not in g.cost_prices:
                g.cost_prices[stock] = pos.avg_cost
            if stock not in g.highest_prices:
                g.highest_prices[stock] = pos.avg_cost
            if stock not in g.entry_dates:
                g.entry_dates[stock] = context.current_dt.date()

# ============================================================
# 辅助函数
# ============================================================

def filter_tradable_stocks(context, stocks: List[str]) -> List[str]:
    """过滤可交易股票"""
    current_data = get_current_data()
    tradable = []
    
    for stock in stocks:
        try:
            # 检查是否可交易
            if stock in current_data and current_data[stock].paused == False:
                # 检查是否ST
                info = jq.get_security_info(stock)
                if info and 'ST' not in info.display_name:
                    tradable.append(stock)
        except:
            continue
    
    return tradable

# ============================================================
# 盘后处理
# ============================================================

def after_market_close(context):
    """
    盘后处理
    
    代码位置: strategies/tenbagger_comprehensive_strategy.py:after_market_close()
    """
    # 更新持仓记录
    update_holdings(context)
    
    # 记录每日持仓
    log.info(f"📊 当前持仓数: {len([s for s in context.portfolio.positions.keys() if context.portfolio.positions[s].total_amount > 0])}")
    log.info(f"💰 总资产: {context.portfolio.total_value:.2f}")
    log.info(f"💵 可用现金: {context.portfolio.available_cash:.2f}")









































