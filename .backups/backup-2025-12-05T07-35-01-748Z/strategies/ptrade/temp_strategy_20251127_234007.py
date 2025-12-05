# -*- coding: utf-8 -*-
"""
================================================================================
test1 - PTrade多因子策略
================================================================================
【生成信息】
    生成时间: 2025-11-27 23:38:28
    生成工具: 韬睿量化 - 策略生成器
    
【策略配置】
    因子组合: 5日反转
    股票池: 沪深300
    持仓数量: 30 只
    调仓频率: 每月
    
【策略说明】
    本策略基于多因子模型，通过组合多个Alpha因子进行选股。
    策略会在每个调仓日计算所有股票的因子得分，选择得分最优的股票持有。
    
【风险提示】
    - 历史回测表现不代表未来收益
    - 请根据市场环境调整参数
    - 建议先在模拟盘验证后再实盘交易
================================================================================
"""

# =============================================================================
# 策略初始化
# =============================================================================
def initialize(context):
    """
    策略初始化函数 - 设置策略参数
    
    参数说明:
        context: PTrade策略上下文对象
    """
    # -------------------------------------------------------------------------
    # 核心参数配置
    # -------------------------------------------------------------------------
    g.stock_pool = '000300.XSHG'  # 股票池指数代码
    g.hold_num = 30                                      # 目标持仓数量
    g.factors = ['reversal_5d']                                  # 使用的因子列表
    g.rebalance = 'monthly'   # 调仓频率
    
    # -------------------------------------------------------------------------
    # 打印策略配置
    # -------------------------------------------------------------------------
    log.info("=" * 60)
    log.info("【test1】策略初始化完成")
    log.info(f"  股票池: {g.stock_pool}")
    log.info(f"  持仓数量: {g.hold_num} 只")
    log.info(f"  因子组合: {g.factors}")
    log.info(f"  调仓频率: {g.rebalance}")
    log.info("=" * 60)


# =============================================================================
# 盘前准备
# =============================================================================
def before_trading_start(context, data):
    """
    盘前准备函数 - 每个交易日开盘前执行
    
    功能:
        1. 获取最新的股票池成分股
        2. 设置可交易股票范围
    """
    # 获取股票池
    if g.stock_pool == '全A':
        # 全A股：获取所有上市股票
        g.stocks = list(get_all_securities(['stock']).index)
    else:
        # 指数成分股
        g.stocks = get_index_stocks(g.stock_pool)
    
    # 设置股票池（用于行情订阅）
    set_universe(g.stocks)
    
    log.info(f"[盘前] 股票池更新: {len(g.stocks)} 只")


# =============================================================================
# 盘中交易
# =============================================================================
def handle_data(context, data):
    """
    盘中交易函数 - 每个交易时间点执行
    
    核心逻辑:
        1. 判断是否为调仓日
        2. 计算多因子得分
        3. 选择得分最优的股票
        4. 执行调仓
    """
    # Step 1: 判断是否调仓日
    if not is_rebalance_day(context):
        return
    
    log.info(f"[调仓日] {context.current_dt.strftime('%Y-%m-%d')}")
    
    # Step 2: 计算因子得分
    scores = calculate_factor_scores(g.stocks, g.factors)
    
    if scores.empty:
        log.warning("[警告] 因子计算结果为空，跳过本次调仓")
        return
    
    # Step 3: 选股 - 选择得分最小（排名最靠前）的股票
    target_stocks = scores.nsmallest(g.hold_num, 'score')['code'].tolist()
    
    log.info(f"[选股] 目标持仓: {len(target_stocks)} 只")
    
    # Step 4: 执行调仓
    rebalance(context, target_stocks)


# =============================================================================
# 辅助函数：判断调仓日
# =============================================================================
def is_rebalance_day(context):
    """
    判断当前是否为调仓日
    
    返回:
        bool: True表示今天需要调仓
    """
    if g.rebalance == 'daily':
        return True
    elif g.rebalance == 'weekly':
        # 每周一调仓
        return context.current_dt.weekday() == 0
    elif g.rebalance == 'monthly':
        # 每月前5个交易日调仓
        return context.current_dt.day <= 5
    elif g.rebalance == 'quarterly':
        # 每季度初调仓（1月、4月、7月、10月）
        return context.current_dt.month in [1, 4, 7, 10] and context.current_dt.day <= 5
    return False


# =============================================================================
# 辅助函数：计算因子得分
# =============================================================================
def calculate_factor_scores(stocks, factors):
    """
    计算多因子综合得分
    
    参数:
        stocks: 股票列表
        factors: 因子列表
        
    返回:
        DataFrame: 包含股票代码和综合得分
    """
    import pandas as pd
    
    # 获取基本面数据
    df = get_fundamentals(
        query(valuation.code, valuation.pe_ratio, indicator.roe)
        .filter(valuation.code.in_(stocks))
    )
    
    if df.empty:
        return pd.DataFrame()
    
    # 计算综合得分（简化版）
    df['score'] = 0
    
    if 'ep' in factors:
        df['ep'] = 1 / df['pe_ratio'].replace(0, float('inf'))
        df['score'] += df['ep'].rank(ascending=False)
    
    if 'roe' in factors:
        df['score'] += df['roe'].rank(ascending=False)
    
    return df

def rebalance(context, target_stocks):
    """调仓函数"""
    # 卖出不在目标列表的股票
    for stock in context.portfolio.positions:
        if stock not in target_stocks:
            order_target(stock, 0)
    
    # 等权买入目标股票
    if len(target_stocks) > 0:
        weight = 1.0 / len(target_stocks)
        for stock in target_stocks:
            order_target_percent(stock, weight)
