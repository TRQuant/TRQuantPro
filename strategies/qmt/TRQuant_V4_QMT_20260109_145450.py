# -*- coding: utf-8 -*-
"""
TRQuant Advisor V4.0 - QMT策略代码
===================================

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

生成时间: 2026-01-09 14:54:50
平台: QMT (迅投)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# QMT核心模块
try:
    from xtquant import xtdata
    from xtquant.xttrader import XtQuantTrader
    from xtquant.xttype import StockAccount
    from xtquant import xtconstant
    QMT_AVAILABLE = True
except ImportError:
    print("⚠️ 警告: xtquant未安装，请运行: pip install xtquant")
    QMT_AVAILABLE = False
    xtdata = None
    XtQuantTrader = None
    StockAccount = None
    xtconstant = None

# ==================== 策略参数配置 ====================
# 选股参数
MAX_STOCKS = 10
MIN_TOTAL_SCORE = 30.0

# 仓位参数
SINGLE_POSITION_MAX = 0.2
MIN_CASH_RATIO = 0.05

# 调仓参数
REBALANCE_WEEKDAY = 0  # 0=周一

# 止损止盈参数
STOP_LOSS = -0.08
TAKE_PROFIT = 0.3
TRAILING_STOP = -0.08
TRAILING_STOP_TRIGGER = 0.15
TIME_STOP_DAYS = 20
PARTIAL_PROFIT_1 = 0.2
PARTIAL_PROFIT_1_RATIO = 0.5

# 因子权重（已验证因子，7因子理论权重）
FACTOR_WEIGHTS = {
    'momentum_20d': 1.0,        # 20日动量（核心）
    'rel_position': 0.9,        # 相对位置（核心）
    'market_cap': 0.85,         # 市值（核心）
    'momentum_5d': 0.75,        # 5日动量（确认）
    'turnover_rate': 0.7,       # 换手率（流动性）
    'roe': 0.5,                 # ROE（基本面底线）
    'growth': 0.4,              # 净利润增长率（成长性）
}

# 归一化权重
TOTAL_WEIGHT = sum(FACTOR_WEIGHTS.values())
FACTOR_WEIGHTS = {k: v / TOTAL_WEIGHT for k, v in FACTOR_WEIGHTS.items()}

# 选股阈值
MIN_MOMENTUM_20D = 5.0
MAX_REL_POSITION = 80.0
MIN_MARKET_CAP = 30.0
MAX_MARKET_CAP = 200.0
MIN_MOMENTUM_5D = -5.0
MAX_MOMENTUM_5D = 10.0
MIN_TURNOVER_RATE = 2.0
MAX_TURNOVER_RATE = 10.0
MIN_ROE = 0.0

# ==================== QMT交易对象初始化 ====================
# 请根据实际情况配置以下参数
QMT_PATH = r"D:\国金证券QMT交易端\userdata_mini"  # QMT路径，请修改为实际路径
SESSION_ID = 123456  # 会话ID，请修改为实际ID
ACCOUNT_ID = "your_account_id"  # 账户ID，请修改为实际账户ID

# 全局变量
xt_trader = None
account = None
g = type('G', (), {})()  # 全局状态对象
g.positions = {}  # 持仓记录 {股票代码: {'cost_price': 成本价, 'entry_date': 买入日期, 'highest_price': 最高价, 'partial_profit_1_done': False}}
g.stock_pool = []  # 股票池
g.last_rebalance_date = None  # 上次调仓日期


def init_qmt_trader():
    """初始化QMT交易对象"""
    global xt_trader, account
    if not QMT_AVAILABLE:
        print("❌ 错误: xtquant未安装")
        return False
    
    try:
        xt_trader = XtQuantTrader(QMT_PATH, SESSION_ID)
        xt_trader.start()
        
        account = StockAccount(ACCOUNT_ID)
        xt_trader.subscribe(account)
        
        print("✅ QMT交易对象初始化成功")
        return True
    except Exception as e:
        print(f"❌ QMT初始化失败: {e}")
        return False


# ==================== 数据获取函数 ====================
def get_stock_list():
    """获取股票池（沪深300成分股）"""
    try:
        # QMT获取指数成分股
        if xtdata:
            # 获取沪深300成分股
            index_code = "000300.SH"
            stock_list = xtdata.get_stock_list_in_sector(index_code)
            if stock_list:
                # 转换为聚宽格式（.XSHG/.XSHE）
                converted_list = []
                for stock in stock_list:
                    if stock.endswith('.SH'):
                        converted_list.append(stock.replace('.SH', '.XSHG'))
                    elif stock.endswith('.SZ'):
                        converted_list.append(stock.replace('.SZ', '.XSHE'))
                    else:
                        converted_list.append(stock)
                return converted_list
        return []
    except Exception as e:
        print(f"获取股票池失败: {e}")
        return []


def get_price_qmt(stocks, start_date=None, end_date=None, count=None, fields=None):
    """
    获取价格数据（QMT版本）
    
    Args:
        stocks: 股票代码列表
        start_date: 开始日期（YYYY-MM-DD）
        end_date: 结束日期（YYYY-MM-DD）
        count: 获取最近N条数据
        fields: 字段列表 ['open', 'high', 'low', 'close', 'volume']
    
    Returns:
        DataFrame，列名为股票代码
    """
    if not xtdata:
        return None
    
    try:
        # 转换股票代码格式（.XSHG -> .SH, .XSHE -> .SZ）
        qmt_stocks = []
        for stock in stocks:
            if stock.endswith('.XSHG'):
                qmt_stocks.append(stock.replace('.XSHG', '.SH'))
            elif stock.endswith('.XSHE'):
                qmt_stocks.append(stock.replace('.XSHE', '.SZ'))
            else:
                qmt_stocks.append(stock)
        
        # 转换日期格式
        if start_date:
            start_time = start_date.replace('-', '')
        else:
            start_time = ''
        
        if end_date:
            end_time = end_date.replace('-', '')
        else:
            end_time = ''
        
        # 默认字段
        if fields is None:
            fields = ['open', 'high', 'low', 'close', 'volume']
        
        # 获取数据
        data = xtdata.get_market_data(
            field_list=fields,
            stock_list=qmt_stocks,
            period='1d',
            start_time=start_time,
            end_time=end_time,
            count=count or -1
        )
        
        if data is None or len(data) == 0:
            return None
        
        # 转换为DataFrame（QMT返回格式可能需要调整）
        if isinstance(data, dict):
            # 如果是字典格式，转换为DataFrame
            df = pd.DataFrame(data)
        else:
            df = data
        
        return df
    
    except Exception as e:
        print(f"获取价格数据失败: {e}")
        return None


def get_fundamentals_qmt(stocks, date_str, fields=None):
    """
    获取基本面数据（QMT版本）
    
    Args:
        stocks: 股票代码列表
        date_str: 日期字符串（YYYY-MM-DD）
        fields: 字段列表 ['market_cap', 'roe', 'net_profit_growth_rate']
    
    Returns:
        DataFrame
    """
    if not xtdata:
        return None
    
    try:
        # 转换股票代码格式
        qmt_stocks = []
        for stock in stocks:
            if stock.endswith('.XSHG'):
                qmt_stocks.append(stock.replace('.XSHG', '.SH'))
            elif stock.endswith('.XSHE'):
                qmt_stocks.append(stock.replace('.XSHE', '.SZ'))
            else:
                qmt_stocks.append(stock)
        
        # 转换日期格式
        date_int = int(date_str.replace('-', ''))
        
        # 获取财务数据
        # 注意：QMT的财务数据API可能需要根据实际版本调整
        fundamentals = xtdata.get_financial_data(
            stock_list=qmt_stocks,
            field_list=fields or ['market_cap', 'roe', 'net_profit_growth_rate'],
            start_time=date_int,
            end_time=date_int
        )
        
        if fundamentals is None or len(fundamentals) == 0:
            return None
        
        # 转换为DataFrame
        df = pd.DataFrame(fundamentals)
        return df
    
    except Exception as e:
        print(f"获取基本面数据失败: {e}")
        return None


# ==================== 因子计算函数 ====================
def calculate_validated_factors(codes, date_str):
    """
    计算已验证因子（7因子）
    
    Args:
        codes: 股票代码列表
        date_str: 日期字符串（YYYY-MM-DD）
    
    Returns:
        DataFrame，包含所有因子值
    """
    if not codes:
        return None
    
    try:
        # 获取价格数据
        prices_20 = get_price_qmt(codes, end_date=date_str, count=20, fields=['close', 'volume'])
        prices_5 = get_price_qmt(codes, end_date=date_str, count=5, fields=['close', 'volume'])
        
        if prices_20 is None or prices_5 is None:
            return None
        
        # 获取基本面数据
        fundamentals = get_fundamentals_qmt(codes, date_str, fields=['market_cap', 'roe', 'net_profit_growth_rate'])
        
        # 初始化结果DataFrame
        result = pd.DataFrame({'code': codes})
        
        # 1. 20日动量
        if 'close' in prices_20.columns:
            result['momentum_20d'] = ((prices_20['close'].iloc[-1] - prices_20['close'].iloc[0]) / prices_20['close'].iloc[0] * 100).values
        else:
            result['momentum_20d'] = 0.0
        
        # 2. 相对位置（20日最高最低）
        if 'close' in prices_20.columns:
            high_20 = prices_20['close'].max()
            low_20 = prices_20['close'].min()
            current = prices_20['close'].iloc[-1]
            result['rel_position'] = ((current - low_20) / (high_20 - low_20) * 100).values
        else:
            result['rel_position'] = 0.0
        
        # 3. 市值（从基本面数据获取）
        if fundamentals is not None and 'market_cap' in fundamentals.columns:
            result['market_cap'] = fundamentals['market_cap'].values
        else:
            result['market_cap'] = 0.0
        
        # 4. 5日动量
        if 'close' in prices_5.columns:
            result['momentum_5d'] = ((prices_5['close'].iloc[-1] - prices_5['close'].iloc[0]) / prices_5['close'].iloc[0] * 100).values
        else:
            result['momentum_5d'] = 0.0
        
        # 5. 换手率（20日平均）
        if 'volume' in prices_20.columns:
            # 计算20日平均换手率（简化计算）
            result['turnover_rate'] = (prices_20['volume'].mean() / 1000000 * 100).values  # 简化计算
        else:
            result['turnover_rate'] = 0.0
        
        # 6. ROE（从基本面数据获取）
        if fundamentals is not None and 'roe' in fundamentals.columns:
            result['roe'] = fundamentals['roe'].values
        else:
            result['roe'] = 0.0
        
        # 7. 净利润增长率（从基本面数据获取）
        if fundamentals is not None and 'net_profit_growth_rate' in fundamentals.columns:
            result['growth'] = fundamentals['net_profit_growth_rate'].values
        else:
            result['growth'] = 0.0
        
        return result
    
    except Exception as e:
        print(f"计算因子失败: {e}")
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
    
    print(f"[选股] 选中 {len(selected)} 只股票，最高得分: {filtered['total_score'].max():.1f}")
    return selected


# ==================== 交易函数 ====================
def get_current_positions():
    """获取当前持仓"""
    global account
    if not account or not xt_trader:
        return {}
    
    try:
        positions = xt_trader.query_stock_positions(account)
        pos_dict = {}
        for pos in positions:
            stock_code = pos.m_strInstrumentID
            # 转换为聚宽格式
            if stock_code.endswith('.SH'):
                stock_code = stock_code.replace('.SH', '.XSHG')
            elif stock_code.endswith('.SZ'):
                stock_code = stock_code.replace('.SZ', '.XSHE')
            pos_dict[stock_code] = {
                'amount': pos.m_nVolume,
                'cost_price': pos.m_dCost,
                'current_price': pos.m_dPrice
            }
        return pos_dict
    except Exception as e:
        print(f"获取持仓失败: {e}")
        return {}


def get_account_info():
    """获取账户信息"""
    global account
    if not account or not xt_trader:
        return None
    
    try:
        account_info = xt_trader.query_stock_asset(account)
        return {
            'total_asset': account_info.m_dBalance,
            'cash': account_info.m_dAvailable,
            'market_value': account_info.m_dBalance - account_info.m_dAvailable
        }
    except Exception as e:
        print(f"获取账户信息失败: {e}")
        return None


def order_stock(stock_code, amount, price=0, order_type='market'):
    """
    下单函数
    
    Args:
        stock_code: 股票代码
        amount: 数量（正数买入，负数卖出）
        price: 价格（0表示市价）
        order_type: 订单类型（'market'或'limit'）
    
    Returns:
        订单ID
    """
    global xt_trader, account
    if not xt_trader or not account:
        print("❌ 交易对象未初始化")
        return None
    
    try:
        # 转换股票代码格式
        qmt_stock = stock_code
        if stock_code.endswith('.XSHG'):
            qmt_stock = stock_code.replace('.XSHG', '.SH')
        elif stock_code.endswith('.XSHE'):
            qmt_stock = stock_code.replace('.XSHE', '.SZ')
        
        # 确定买卖方向
        if amount > 0:
            direction = xtconstant.STOCK_BUY
        else:
            direction = xtconstant.STOCK_SELL
            amount = abs(amount)
        
        # 确定价格类型
        if order_type == 'market' or price == 0:
            price_type = xtconstant.LATEST_PRICE
            order_price = 0
        else:
            price_type = xtconstant.FIX_PRICE
            order_price = price
        
        # 下单
        order_id = xt_trader.order_stock(
            account,
            qmt_stock,
            direction,
            int(amount),
            price_type,
            order_price
        )
        
        print(f"[下单] {stock_code} {'买入' if amount > 0 else '卖出'} {abs(amount)}股，订单ID: {order_id}")
        return order_id
    
    except Exception as e:
        print(f"下单失败: {e}")
        return None


# ==================== 风控函数 ====================
def check_risk_control():
    """风控检查（止损止盈）"""
    current_date = datetime.now().strftime('%Y-%m-%d')
    positions = get_current_positions()
    
    for stock_code, pos_info in positions.items():
        if stock_code not in g.positions:
            # 初始化持仓记录
            g.positions[stock_code] = {
                'cost_price': pos_info['cost_price'],
                'entry_date': current_date,
                'highest_price': pos_info['current_price'],
                'partial_profit_1_done': False
            }
        
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
            print(f"[止损] {stock_code} 亏损 {pnl*100:.2f}%，卖出")
            order_stock(stock_code, -pos_info['amount'])
            del g.positions[stock_code]
            continue
        
        # 止盈
        if pnl >= TAKE_PROFIT:
            print(f"[止盈] {stock_code} 盈利 {pnl*100:.2f}%，卖出")
            order_stock(stock_code, -pos_info['amount'])
            del g.positions[stock_code]
            continue
        
        # 移动止损（盈利超过触发条件后启用）
        if pnl >= TRAILING_STOP_TRIGGER:
            trailing_pnl = (current_price - pos_record['highest_price']) / pos_record['highest_price']
            if trailing_pnl <= TRAILING_STOP:
                print(f"[移动止损] {stock_code} 从最高价回撤 {trailing_pnl*100:.2f}%，卖出")
                order_stock(stock_code, -pos_info['amount'])
                del g.positions[stock_code]
                continue
        
        # 分批止盈
        if not pos_record['partial_profit_1_done'] and pnl >= PARTIAL_PROFIT_1:
            sell_amount = int(pos_info['amount'] * PARTIAL_PROFIT_1_RATIO)
            print(f"[分批止盈] {stock_code} 盈利 {pnl*100:.2f}%，卖出{PARTIAL_PROFIT_1_RATIO*100:.0f}%")
            order_stock(stock_code, -sell_amount)
            pos_record['partial_profit_1_done'] = True
        
        # 时间止损
        entry_date = datetime.strptime(pos_record['entry_date'], '%Y-%m-%d')
        days_held = (datetime.now() - entry_date).days
        if days_held >= TIME_STOP_DAYS:
            print(f"[时间止损] {stock_code} 持仓{days_held}天，卖出")
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
    
    print(f"[调仓] 开始调仓，日期: {current_date}")
    
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
    target_positions = {}
    position_value = total_asset * SINGLE_POSITION_MAX
    for stock in selected_stocks:
        # 获取当前价格
        prices = get_price_qmt([stock], end_date=current_date, count=1, fields=['close'])
        if prices is None or len(prices) == 0:
            continue
        
        current_price = prices['close'].iloc[-1] if 'close' in prices.columns else 0
        if current_price == 0:
            continue
        
        target_amount = int(position_value / current_price / 100) * 100  # 整手
        if target_amount > 0:
            target_positions[stock] = target_amount
    
    # 卖出不在目标持仓中的股票
    for stock, pos_info in current_positions.items():
        if stock not in target_positions:
            print(f"[调仓] 卖出 {stock}")
            order_stock(stock, -pos_info['amount'])
            if stock in g.positions:
                del g.positions[stock]
    
    # 买入目标持仓中的股票
    for stock, target_amount in target_positions.items():
        current_amount = current_positions.get(stock, {}).get('amount', 0)
        diff = target_amount - current_amount
        
        if diff > 0:
            print(f"[调仓] 买入 {stock} {diff}股")
            order_stock(stock, diff)
            if stock not in g.positions:
                g.positions[stock] = {
                    'cost_price': get_price_qmt([stock], end_date=current_date, count=1, fields=['close'])['close'].iloc[-1] if 'close' in get_price_qmt([stock], end_date=current_date, count=1, fields=['close']).columns else 0,
                    'entry_date': current_date,
                    'highest_price': 0,
                    'partial_profit_1_done': False
                }
        elif diff < 0:
            print(f"[调仓] 卖出 {stock} {abs(diff)}股")
            order_stock(stock, diff)
    
    g.last_rebalance_date = current_date
    print(f"[调仓] 调仓完成")


# ==================== 主函数 ====================
def main():
    """主函数（QMT策略入口）"""
    print("=" * 60)
    print("TRQuant Advisor V4.0 - QMT策略启动")
    print("=" * 60)
    
    # 初始化QMT交易对象
    if not init_qmt_trader():
        print("❌ QMT初始化失败，策略无法运行")
        return
    
    # 初始化股票池
    g.stock_pool = get_stock_list()
    print(f"✅ 股票池初始化: {len(g.stock_pool)} 只股票")
    
    # 定时任务（使用schedule库）
    try:
        import schedule
        
        # 每周调仓（周一09:35）
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        weekday_name = weekdays[REBALANCE_WEEKDAY]
        getattr(schedule.every(), weekday_name).at("09:35").do(rebalance)
        
        # 每日风控检查（14:50）
        schedule.every().day.at("14:50").do(check_risk_control)
        
        weekday_names_cn = ['一', '二', '三', '四', '五']
        print("✅ 定时任务已设置")
        print(f"   调仓: 每周{weekday_names_cn[REBALANCE_WEEKDAY]} 09:35")
        print("   风控: 每日 14:50")
        
        # 主循环
        print("\n策略运行中... (按Ctrl+C停止)")
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n策略已停止")
    except Exception as e:
        print(f"策略运行错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
