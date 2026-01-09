# -*- coding: utf-8 -*-
# This file uses UTF-8 encoding, please ensure your editor opens it as UTF-8
"""
TRQuant Advisor V4.0 - QMT Research Environment Strategy Code
==============================================================

Strategy Description:
- Multi-factor stock selection strategy based on 7 validated factors
- 100% using validated factors, no Juquant factors
- Complete risk control and stop-loss/take-profit mechanism
- Suitable for QMT desktop app research environment, no trading account connection required

Factor List:
1. 20-day momentum (momentum_20d) - Core factor
2. Relative position (rel_position) - Core factor
3. Market cap (market_cap) - Core factor
4. 5-day momentum (momentum_5d) - Confirmation factor
5. Turnover rate (turnover_rate) - Liquidity factor
6. ROE (roe) - Fundamental factor
7. Net profit growth rate (growth) - Growth factor

Generated Time: 2026-01-09 15:31:43
Platform: QMT Research Environment
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==================== Strategy Parameters ====================
# Stock Selection Parameters
MAX_STOCKS = 10
MIN_TOTAL_SCORE = 30.0

# Position Parameters
SINGLE_POSITION_MAX = 0.2
MIN_CASH_RATIO = 0.05

# Rebalance Parameters
REBALANCE_WEEKDAY = 0  # 0=Monday

# Stop-Loss/Take-Profit Parameters
STOP_LOSS = -0.08
TAKE_PROFIT = 0.3
TAKE_PROFIT_PCT = 30.0
STOP_LOSS_PCT = 8.0
TRAILING_STOP = -0.08
TRAILING_STOP_TRIGGER = 0.15
TIME_STOP_DAYS = 20
PARTIAL_PROFIT_1 = 0.2
PARTIAL_PROFIT_1_RATIO = 0.5

# Factor Weights (Validated factors, 7-factor theoretical weights)
FACTOR_WEIGHTS = {
    'momentum_20d': 1.0,        # 20-day momentum (core)
    'rel_position': 0.9,        # Relative position (core)
    'market_cap': 0.85,         # Market cap (core)
    'momentum_5d': 0.75,        # 5-day momentum (confirmation)
    'turnover_rate': 0.7,       # Turnover rate (liquidity)
    'roe': 0.5,                 # ROE (fundamental baseline)
    'growth': 0.4,              # Net profit growth rate (growth)
}

# Normalize weights
TOTAL_WEIGHT = sum(FACTOR_WEIGHTS.values())
FACTOR_WEIGHTS = {k: v / TOTAL_WEIGHT for k, v in FACTOR_WEIGHTS.items()}

# Stock Selection Thresholds
MIN_MOMENTUM_20D = 5.0
MAX_REL_POSITION = 80.0
MIN_MARKET_CAP = 30.0
MAX_MARKET_CAP = 200.0
MIN_MOMENTUM_5D = -5.0
MAX_MOMENTUM_5D = 10.0
MIN_TURNOVER_RATE = 2.0
MAX_TURNOVER_RATE = 10.0
MIN_ROE = 0.0

# ==================== Global Variables ====================
# Position records {stock_code: {'cost_price': cost, 'entry_date': date, 'highest_price': high, 'partial_profit_1_done': False}}
g_positions = {}
g_last_rebalance_date = None  # Last rebalance date
g_stock_pool = []  # Stock pool


# ==================== Data Retrieval Functions ====================
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
    """Get stock pool (CSI 300 component stocks)"""
    try:
        # QMT research environment get index component stocks
        index_code = "000300.SH"
        stock_list = ContextInfo.get_stock_list_in_sector(index_code)
        if stock_list:
            # Normalize stock codes for QMT
            normalized_list = [normalize_stock_code(code) for code in stock_list]
            return normalized_list
        return []
    except Exception as e:
        print(f"Failed to get stock list: {e}")
        return []


def get_price_data(ContextInfo, stocks, count=20, fields=None):
    """
    Get price data (QMT research environment version)
    
    Args:
        ContextInfo: QMT context object
        stocks: Stock code list
        count: Get last N data points
        fields: Field list ['open', 'high', 'low', 'close', 'volume']
    
    Returns:
        DataFrame with stock codes as column names
    """
    try:
        if fields is None:
            fields = ['open', 'high', 'low', 'close', 'volume']
        
        # QMT research environment uses get_market_data
        # Note: Adjust according to actual QMT API
        result = {}
        for stock in stocks:
            try:
                # QMT research environment API: get_market_data(stock, period='1d', count=count)
                data = ContextInfo.get_market_data(
                    stock, 
                    period='1d', 
                    count=count,
                    fields=fields
                )
                if data is not None and len(data) > 0:
                    result[stock] = data
            except Exception as e:
                print(f"Failed to get {stock} data: {e}")
                continue
        
        # Convert to DataFrame
        if result:
            df = pd.DataFrame(result)
            return df
        return None
    
    except Exception as e:
        print(f"Failed to get price data: {e}")
        return None


def get_fundamentals_data(ContextInfo, stocks, date_str, fields=None):
    """
    Get fundamental data (QMT research environment version)
    
    Args:
        ContextInfo: QMT context object
        stocks: Stock code list
        date_str: Date string (YYYY-MM-DD)
        fields: Field list ['market_cap', 'roe', 'net_profit_growth_rate']
    
    Returns:
        DataFrame
    """
    try:
        if fields is None:
            fields = ['market_cap', 'roe', 'net_profit_growth_rate']
        
        # QMT research environment fundamental data API
        # Note: Adjust according to actual QMT API
        result = {}
        for stock in stocks:
            try:
                # QMT may use get_financial_data or similar API
                data = ContextInfo.get_financial_data(
                    stock,
                    fields=fields,
                    date=date_str
                )
                if data is not None:
                    result[stock] = data
            except Exception as e:
                print(f"Failed to get {stock} fundamental data: {e}")
                continue
        
        if result:
            df = pd.DataFrame(result).T  # Transpose, stock codes as index
            return df
        return None
    
    except Exception as e:
        print(f"Failed to get fundamental data: {e}")
        return None


# ==================== Factor Calculation Functions ====================
def calculate_validated_factors(ContextInfo, codes, date_str):
    """
    Calculate validated factors (7 factors)
    
    Args:
        ContextInfo: QMT context object
        codes: Stock code list
        date_str: Date string (YYYY-MM-DD)
    
    Returns:
        DataFrame containing all factor values
    """
    if not codes:
        return None
    
    try:
        # Get price data
        prices_20 = get_price_data(ContextInfo, codes, count=20)
        prices_5 = get_price_data(ContextInfo, codes, count=5)
        
        if prices_20 is None or prices_5 is None:
            return None
        
        # Get fundamental data
        fundamentals = get_fundamentals_data(ContextInfo, codes, date_str, 
                                            fields=['market_cap', 'roe', 'net_profit_growth_rate'])
        
        # Initialize result DataFrame
        result = pd.DataFrame({'code': codes})
        
        # 1. 20-day momentum
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
        
        # 2. Relative position (20-day high/low)
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
        
        # 3. Market cap (from fundamental data)
        if fundamentals is not None and 'market_cap' in fundamentals.columns:
            result['market_cap'] = result['code'].map(dict(zip(fundamentals.index, fundamentals['market_cap']))).fillna(0.0)
        else:
            result['market_cap'] = 0.0
        
        # 4. 5-day momentum
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
        
        # 5. Turnover rate (20-day average, simplified calculation)
        for code in codes:
            if code in prices_20.columns:
                try:
                    price_data = prices_20[code]
                    if len(price_data) >= 20:
                        volume_vals = price_data['volume'] if isinstance(price_data, pd.DataFrame) else price_data
                        # Simplified turnover rate calculation
                        result.loc[result['code'] == code, 'turnover_rate'] = volume_vals.mean() / 1000000 * 100 if len(volume_vals) > 0 else 0.0
                    else:
                        result.loc[result['code'] == code, 'turnover_rate'] = 0.0
                except:
                    result.loc[result['code'] == code, 'turnover_rate'] = 0.0
            else:
                result.loc[result['code'] == code, 'turnover_rate'] = 0.0
        
        # 6. ROE (from fundamental data)
        if fundamentals is not None and 'roe' in fundamentals.columns:
            result['roe'] = result['code'].map(dict(zip(fundamentals.index, fundamentals['roe']))).fillna(0.0)
        else:
            result['roe'] = 0.0
        
        # 7. Net profit growth rate (from fundamental data)
        if fundamentals is not None and 'net_profit_growth_rate' in fundamentals.columns:
            result['growth'] = result['code'].map(dict(zip(fundamentals.index, fundamentals['net_profit_growth_rate']))).fillna(0.0)
        else:
            result['growth'] = 0.0
        
        return result
    
    except Exception as e:
        print(f"Factor calculation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def calculate_factor_scores(factors_df):
    """
    Calculate factor scores (based on theoretical optimal intervals)
    
    Args:
        factors_df: Factor DataFrame
    
    Returns:
        DataFrame with score columns added
    """
    import numpy as np
    
    df = factors_df.copy()
    
    # 1. 20-day momentum score (5%~30% optimal, center 17.5%)
    momentum_20d = df['momentum_20d'].values
    optimal_center = 17.5
    optimal_range = 12.5
    df['momentum_20d_score'] = np.maximum(0, 1 - np.abs(momentum_20d - optimal_center) / optimal_range)
    
    # 2. Relative position score (50%~80% optimal)
    rel_position = df['rel_position'].values
    df['rel_position_score'] = np.where(
        (rel_position >= 50) & (rel_position <= 80),
        1.0,
        np.maximum(0, 1 - np.abs(rel_position - 65) / 50)
    )
    
    # 3. Market cap score (30~200 billion optimal)
    market_cap = df['market_cap'].values
    optimal_cap = 115  # Center value
    optimal_range_cap = 85
    df['market_cap_score'] = np.maximum(0, 1 - np.abs(market_cap - optimal_cap) / optimal_range_cap)
    
    # 4. 5-day momentum score (-2%~5% optimal)
    momentum_5d = df['momentum_5d'].values
    optimal_5d = 1.5
    optimal_range_5d = 3.5
    df['momentum_5d_score'] = np.maximum(0, 1 - np.abs(momentum_5d - optimal_5d) / optimal_range_5d)
    
    # 5. Turnover rate score (2%~8% optimal)
    turnover_rate = df['turnover_rate'].values
    optimal_turnover = 5.0
    optimal_range_turnover = 3.0
    df['turnover_rate_score'] = np.maximum(0, 1 - np.abs(turnover_rate - optimal_turnover) / optimal_range_turnover)
    
    # 6. ROE score (higher is better, threshold 0%)
    roe = df['roe'].values
    df['roe_score'] = np.where(roe >= 0, np.minimum(1.0, roe / 20.0), 0.0)  # 20% ROE is full score
    
    # 7. Net profit growth rate score (higher is better, threshold 0%)
    growth = df['growth'].values
    df['growth_score'] = np.where(growth >= 0, np.minimum(1.0, growth / 50.0), 0.0)  # 50% growth is full score
    
    # Calculate comprehensive score
    df['total_score'] = (
        df['momentum_20d_score'] * FACTOR_WEIGHTS['momentum_20d'] +
        df['rel_position_score'] * FACTOR_WEIGHTS['rel_position'] +
        df['market_cap_score'] * FACTOR_WEIGHTS['market_cap'] +
        df['momentum_5d_score'] * FACTOR_WEIGHTS['momentum_5d'] +
        df['turnover_rate_score'] * FACTOR_WEIGHTS['turnover_rate'] +
        df['roe_score'] * FACTOR_WEIGHTS['roe'] +
        df['growth_score'] * FACTOR_WEIGHTS['growth']
    ) * 100  # Convert to 0-100 score
    
    return df


# ==================== Stock Selection Functions ====================
def select_stocks(ContextInfo, date_str):
    """
    Stock selection function
    
    Args:
        ContextInfo: QMT context object
        date_str: Date string (YYYY-MM-DD)
    
    Returns:
        Selected stock code list
    """
    # Get stock pool
    stock_pool = get_stock_list(ContextInfo)
    if not stock_pool:
        print(f"[Stock Selection] Stock pool is empty")
        return []
    
    # Calculate factors
    factors_df = calculate_validated_factors(ContextInfo, stock_pool, date_str)
    if factors_df is None or factors_df.empty:
        print(f"[Stock Selection] Factor calculation failed")
        return []
    
    # Calculate scores
    factors_df = calculate_factor_scores(factors_df)
    
    # Filter
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
        print(f"[Stock Selection] No stocks passed the filter")
        return []
    
    # Sort by score, take top N
    filtered = filtered.sort_values('total_score', ascending=False)
    selected = filtered.head(MAX_STOCKS)['code'].tolist()
    
    print(f"[Stock Selection] Selected {len(selected)} stocks, highest score: {filtered['total_score'].max():.1f}")
    return selected


# ==================== Risk Control Functions ====================
def check_risk_control(ContextInfo):
    """Risk control check (stop-loss/take-profit)"""
    global g_positions
    
    current_date = ContextInfo.current_dt.strftime('%Y-%m-%d')
    positions = ContextInfo.get_trade_detail_data(ContextInfo.accout_id, 'stock', 'position')
    
    for pos in positions:
        stock_code = pos.m_strInstrumentID
        
        if stock_code not in g_positions:
            # Initialize position record
            g_positions[stock_code] = {
                'cost_price': pos.m_dCost,
                'entry_date': current_date,
                'highest_price': pos.m_dPrice,
                'partial_profit_1_done': False
            }
        
        pos_record = g_positions[stock_code]
        cost_price = pos_record['cost_price']
        current_price = pos.m_dPrice
        
        # Update highest price
        if current_price > pos_record['highest_price']:
            pos_record['highest_price'] = current_price
        
        # Calculate profit/loss
        pnl = (current_price - cost_price) / cost_price
        
        # Stop-loss
        if pnl <= STOP_LOSS:
            print(f"[Stop-Loss] {stock_code} loss {pnl*100:.2f}%, sell")
            ContextInfo.order(stock_code, -pos.m_nVolume, ContextInfo.MARKET_SH_SZ)
            del g_positions[stock_code]
            continue
        
        # Take-profit
        if pnl >= TAKE_PROFIT:
            print(f"[Take-Profit] {stock_code} profit {pnl*100:.2f}%, sell")
            ContextInfo.order(stock_code, -pos.m_nVolume, ContextInfo.MARKET_SH_SZ)
            del g_positions[stock_code]
            continue
        
        # Trailing stop (enabled after profit exceeds trigger condition)
        if pnl >= TRAILING_STOP_TRIGGER:
            trailing_pnl = (current_price - pos_record['highest_price']) / pos_record['highest_price']
            if trailing_pnl <= TRAILING_STOP:
                print(f"[Trailing Stop] {stock_code} retrace {trailing_pnl*100:.2f}% from high, sell")
                ContextInfo.order(stock_code, -pos.m_nVolume, ContextInfo.MARKET_SH_SZ)
                del g_positions[stock_code]
                continue
        
        # Partial profit-taking
        if not pos_record['partial_profit_1_done'] and pnl >= PARTIAL_PROFIT_1:
            sell_amount = int(pos.m_nVolume * PARTIAL_PROFIT_1_RATIO)
            print(f"[Partial Profit] {stock_code} profit {pnl*100:.2f}%, sell {PARTIAL_PROFIT_1_RATIO*100:.0f}%")
            ContextInfo.order(stock_code, -sell_amount, ContextInfo.MARKET_SH_SZ)
            pos_record['partial_profit_1_done'] = True
        
        # Time stop
        entry_date = datetime.strptime(pos_record['entry_date'], '%Y-%m-%d')
        days_held = (ContextInfo.current_dt - entry_date).days
        if days_held >= TIME_STOP_DAYS:
            print(f"[Time Stop] {stock_code} held {days_held} days, sell")
            ContextInfo.order(stock_code, -pos.m_nVolume, ContextInfo.MARKET_SH_SZ)
            del g_positions[stock_code]


# ==================== Rebalance Functions ====================
def rebalance(ContextInfo):
    """Rebalance function"""
    global g_last_rebalance_date, g_stock_pool
    
    current_date = ContextInfo.current_dt.strftime('%Y-%m-%d')
    current_weekday = ContextInfo.current_dt.weekday()
    
    # Check if rebalancing is needed (weekly on specified day)
    if current_weekday != REBALANCE_WEEKDAY:
        return
    
    if g_last_rebalance_date == current_date:
        return
    
    print(f"[Rebalance] Start rebalancing, date: {current_date}")
    
    # Stock selection
    selected_stocks = select_stocks(ContextInfo, current_date)
    if not selected_stocks:
        print("[Rebalance] No stocks available, skip rebalancing")
        return
    
    # Get account information
    account_info = ContextInfo.get_account_info(ContextInfo.accout_id)
    if not account_info:
        print("[Rebalance] Unable to get account information")
        return
    
    total_asset = account_info.m_dBalance
    cash = account_info.m_dAvailable
    current_positions = ContextInfo.get_trade_detail_data(ContextInfo.accout_id, 'stock', 'position')
    
    # Calculate target positions
    target_positions = {}
    position_value = total_asset * SINGLE_POSITION_MAX
    
    for stock in selected_stocks:
        # Get current price
        current_price = ContextInfo.get_last_price(stock)
        if current_price == 0:
            continue
        
        target_amount = int(position_value / current_price / 100) * 100  # Round lot
        if target_amount > 0:
            target_positions[stock] = target_amount
    
    # Sell stocks not in target positions
    for pos in current_positions:
        stock = pos.m_strInstrumentID
        if stock not in target_positions:
            print(f"[Rebalance] Sell {stock}")
            ContextInfo.order(stock, -pos.m_nVolume, ContextInfo.MARKET_SH_SZ)
            if stock in g_positions:
                del g_positions[stock]
    
    # Buy stocks in target positions
    for stock, target_amount in target_positions.items():
        # Find current position
        current_amount = 0
        for pos in current_positions:
            if pos.m_strInstrumentID == stock:
                current_amount = pos.m_nVolume
                break
        
        diff = target_amount - current_amount
        
        if diff > 0:
            print(f"[Rebalance] Buy {stock} {diff} shares")
            ContextInfo.order(stock, diff, ContextInfo.MARKET_SH_SZ)
            if stock not in g_positions:
                g_positions[stock] = {
                    'cost_price': ContextInfo.get_last_price(stock),
                    'entry_date': current_date,
                    'highest_price': 0,
                    'partial_profit_1_done': False
                }
        elif diff < 0:
            print(f"[Rebalance] Sell {stock} {abs(diff)} shares")
            ContextInfo.order(stock, diff, ContextInfo.MARKET_SH_SZ)
    
    g_last_rebalance_date = current_date
    print(f"[Rebalance] Rebalancing completed")


# ==================== QMT Research Environment Entry Functions ====================
def init(ContextInfo):
    """
    Strategy initialization
    QMT research environment entry function
    """
    global g_stock_pool
    
    print("=" * 60)
    print("TRQuant Advisor V4.0 - QMT Research Environment Strategy Started")
    print("=" * 60)
    
    # Set stock pool (CSI 300)
    index_code = "000300.SH"
    g_stock_pool = ContextInfo.get_stock_list_in_sector(index_code)
    # Normalize stock codes for QMT
    g_stock_pool = [normalize_stock_code(code) for code in g_stock_pool]
    ContextInfo.set_universe(g_stock_pool)
    
    print(f"Stock pool initialized: {len(g_stock_pool)} stocks")
    
    # Set scheduled tasks
    # QMT research environment uses run_time (without weekday parameter)
    # Note: QMT run_time() does not support weekday parameter
    # Weekly rebalancing will be checked in handlebar() function
    
    # Daily risk control check (14:50)
    ContextInfo.run_time('check_risk_control', '14:50:00', 'SH')
    
    print("Scheduled tasks set")
    weekday_cn = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    print(f"   Rebalance: Every {weekday_cn[REBALANCE_WEEKDAY]} (checked in handlebar)")
    print("   Risk Control: Daily 14:50")
    print("=" * 60)


def handlebar(ContextInfo):
    """
    Daily K-line callback
    QMT research environment main function
    """
    global g_stock_pool
    
    current_weekday = ContextInfo.current_dt.weekday()
    current_time = ContextInfo.current_dt.strftime('%H:%M:%S')
    
    # Update stock pool weekly (Monday)
    if current_weekday == 0:  # Monday
        index_code = "000300.SH"
        g_stock_pool = ContextInfo.get_stock_list_in_sector(index_code)
        # Normalize stock codes
        g_stock_pool = [normalize_stock_code(code) for code in g_stock_pool]
        ContextInfo.set_universe(g_stock_pool)
        print(f"[Pre-market] Stock pool updated: {len(g_stock_pool)} stocks")
    
    # Risk control check (daily before close, around 14:50)
    if current_time >= '14:50:00':
        check_risk_control(ContextInfo)
    
    # Rebalancing (weekly on specified day, around 09:35)
    if current_weekday == REBALANCE_WEEKDAY and current_time >= '09:35:00':
        rebalance(ContextInfo)
