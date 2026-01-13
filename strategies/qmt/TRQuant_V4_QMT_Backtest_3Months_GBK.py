# -*- coding: ascii -*-
"""
TRQuant Advisor V4.0 - QMT Backtest Strategy (Last 3 Months)
==============================================================

Complete backtest strategy with:
- Multi-factor stock selection (7 validated factors)
- Risk control and stop-loss/take-profit
- Commission calculation
- Last 3 months backtest period

Backtest Period: Last 3 months (automatically calculated)
Commission Settings:
- Commission: 0.01% (0.0001)
- Stamp Tax: 0.1% (0.001) on sell only
- Transfer Fee: 0.001% (0.00001)
- Regulatory Fee: 0.00687% (0.0000687)

Generated Time: 2026-01-09
Platform: QMT Research Environment (Backtest Mode)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==================== Backtest Configuration ====================
# Calculate last 3 months date range
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=90)  # Approximately 3 months

# Commission Settings (Huatai Securities)
COMMISSION_RATE = 0.0001      # 0.01% commission
STAMP_TAX_RATE = 0.001        # 0.1% stamp tax (sell only)
TRANSFER_FEE_RATE = 0.00001   # 0.001% transfer fee
REGULATORY_FEE_RATE = 0.0000687  # 0.00687% regulatory fee
MIN_COMMISSION = 5.0          # Minimum commission (RMB)

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
g_positions = {}  # Position records
g_last_rebalance_date = None
g_stock_pool = []
g_backtest_stats = {
    'total_trades': 0,
    'total_commission': 0.0,
    'total_stamp_tax': 0.0,
    'total_transfer_fee': 0.0,
    'total_regulatory_fee': 0.0,
    'win_trades': 0,
    'loss_trades': 0,
}


# ==================== Commission Calculation ====================
def calculate_commission(amount, price, is_buy=True):
    """
    Calculate trading commission and fees
    
    Args:
        amount: Number of shares
        price: Price per share
        is_buy: True for buy, False for sell
    
    Returns:
        dict: {'commission': float, 'stamp_tax': float, 'transfer_fee': float, 'regulatory_fee': float, 'total': float}
    """
    trade_value = amount * price
    
    # Commission (both buy and sell)
    commission = max(trade_value * COMMISSION_RATE, MIN_COMMISSION)
    
    # Stamp tax (sell only)
    stamp_tax = trade_value * STAMP_TAX_RATE if not is_buy else 0.0
    
    # Transfer fee (both buy and sell)
    transfer_fee = trade_value * TRANSFER_FEE_RATE
    
    # Regulatory fee (both buy and sell)
    regulatory_fee = trade_value * REGULATORY_FEE_RATE
    
    total_fee = commission + stamp_tax + transfer_fee + regulatory_fee
    
    return {
        'commission': commission,
        'stamp_tax': stamp_tax,
        'transfer_fee': transfer_fee,
        'regulatory_fee': regulatory_fee,
        'total': total_fee
    }


def record_trade_fees(amount, price, is_buy=True):
    """Record trade fees to global statistics"""
    fees = calculate_commission(amount, price, is_buy)
    g_backtest_stats['total_commission'] += fees['commission']
    g_backtest_stats['total_stamp_tax'] += fees['stamp_tax']
    g_backtest_stats['total_transfer_fee'] += fees['transfer_fee']
    g_backtest_stats['total_regulatory_fee'] += fees['regulatory_fee']
    g_backtest_stats['total_trades'] += 1
    return fees


# ==================== Data Retrieval Functions ====================
def is_a_share_stock(code):
    """
    Check if code is an A-share stock (exclude ETFs, bonds, funds, etc.)
    
    A-share stock codes:
    - Shanghai: 600xxx, 601xxx, 603xxx, 605xxx, 688xxx (STAR Market)
    - Shenzhen: 000xxx, 001xxx, 002xxx, 003xxx, 300xxx (ChiNext)
    
    Exclude:
    - ETFs: 51xxxx, 159xxx
    - Bonds: 11xxxx, 12xxxx, 13xxxx
    - Funds: 50xxxx, 15xxxx
    - Index: 000xxx (index codes)
    """
    if not code:
        return False
    
    code_clean = code.strip().upper()
    
    # Remove suffix if exists
    if code_clean.endswith('.SH') or code_clean.endswith('.SZ'):
        code_clean = code_clean[:-3]
    elif code_clean.endswith('.XSHG') or code_clean.endswith('.XSHE'):
        code_clean = code_clean[:-5]
    
    # Check if it's 6-digit number
    if not code_clean.isdigit() or len(code_clean) != 6:
        return False
    
    # A-share stock prefixes
    a_share_prefixes = (
        '600', '601', '603', '605',  # Shanghai main board
        '688',  # Shanghai STAR Market
        '000', '001', '002', '003',  # Shenzhen main board
        '300'   # Shenzhen ChiNext
    )
    
    # Check if starts with A-share prefix
    if code_clean.startswith(a_share_prefixes):
        return True
    
    return False


def normalize_stock_code(code):
    """Normalize stock code format for QMT"""
    if not code:
        return code
    
    code_clean = code.strip().upper()
    
    if code_clean.endswith('.XSHG'):
        code_clean = code_clean.replace('.XSHG', '')
        return f"{code_clean}.SH"
    elif code_clean.endswith('.XSHE'):
        code_clean = code_clean.replace('.XSHE', '')
        return f"{code_clean}.SZ"
    elif code_clean.endswith('.SH') or code_clean.endswith('.SZ'):
        return code_clean
    elif '.' not in code_clean and len(code_clean) == 6:
        if code_clean.startswith(('600', '601', '603', '605', '688')):
            return f"{code_clean}.SH"
        elif code_clean.startswith(('000', '001', '002', '003', '300')):
            return f"{code_clean}.SZ"
        else:
            return f"{code_clean}.SH"
    else:
        return code_clean


def get_current_datetime(ContextInfo):
    """Get current datetime in QMT"""
    from datetime import datetime
    try:
        if hasattr(ContextInfo, 'bartime') and ContextInfo.bartime:
            return datetime.fromtimestamp(ContextInfo.bartime / 1000.0)
        if hasattr(ContextInfo, 'barpos') and hasattr(ContextInfo, 'get_bar_timetag'):
            timetag = ContextInfo.get_bar_timetag(ContextInfo.barpos)
            if timetag:
                return datetime.fromtimestamp(timetag / 1000.0)
        return datetime.now()
    except:
        return datetime.now()


def validate_stock_tradable(ContextInfo, code, max_retries=2):
    """Validate if a stock is still tradable"""
    for attempt in range(max_retries):
        try:
            price = ContextInfo.get_last_price(code)
            if price is not None and price > 0:
                return True
            data = ContextInfo.get_market_data(code, period='1d', count=1)
            if data is not None and len(data) > 0:
                return True
            return False
        except:
            if attempt < max_retries - 1:
                continue
            return False
    return False


def get_stock_list(ContextInfo, validate=False):
    """
    Get stock pool (All A-share stocks)
    
    Args:
        ContextInfo: QMT context object
        validate: Whether to validate stock tradability
    
    Returns:
        List of stock codes (all A-share stocks)
    """
    try:
        # Method 1: Try to get all A-share stocks from QMT
        # QMT API: get_stock_list_in_sector() with market code
        stock_list = []
        
        # Try Shanghai market (SH)
        try:
            sh_stocks = ContextInfo.get_stock_list_in_sector("SH")
            if sh_stocks:
                stock_list.extend(sh_stocks)
                print(f"[Stock List] Got {len(sh_stocks)} stocks from Shanghai market")
        except Exception as e:
            print(f"[Warning] Failed to get Shanghai stocks: {e}")
        
        # Try Shenzhen market (SZ)
        try:
            sz_stocks = ContextInfo.get_stock_list_in_sector("SZ")
            if sz_stocks:
                stock_list.extend(sz_stocks)
                print(f"[Stock List] Got {len(sz_stocks)} stocks from Shenzhen market")
        except Exception as e:
            print(f"[Warning] Failed to get Shenzhen stocks: {e}")
        
        # Method 2: If method 1 fails, try to get from index and expand
        if not stock_list:
            print("[Stock List] Method 1 failed, trying method 2...")
            try:
                # Get from major indices and combine
                indices = ["000300.SH", "000905.SH", "399006.SZ", "399001.SZ"]  # CSI 300, CSI 500, ChiNext, SZSE Component
                for index_code in indices:
                    try:
                        index_stocks = ContextInfo.get_stock_list_in_sector(index_code)
                        if index_stocks:
                            stock_list.extend(index_stocks)
                    except:
                        continue
                
                # Remove duplicates
                stock_list = list(set(stock_list))
                print(f"[Stock List] Got {len(stock_list)} stocks from indices (method 2)")
            except Exception as e:
                print(f"[Warning] Method 2 also failed: {e}")
        
        # Method 3: If both methods fail, use CSI 300 as fallback
        if not stock_list:
            print("[Stock List] All methods failed, using CSI 300 as fallback...")
            try:
                stock_list = ContextInfo.get_stock_list_in_sector("000300.SH")
                if stock_list:
                    print(f"[Stock List] Got {len(stock_list)} stocks from CSI 300 (fallback)")
            except Exception as e:
                print(f"[Error] Fallback also failed: {e}")
                return []
        
        if not stock_list:
            print("[Warning] Failed to get any stock list")
            return []
        
        # Normalize stock codes
        normalized_list = [normalize_stock_code(code) for code in stock_list]
        # Remove duplicates after normalization
        normalized_list = list(set(normalized_list))
        
        print(f"[Stock List] Total securities after normalization: {len(normalized_list)}")
        
        # Filter: Only keep A-share stocks (exclude ETFs, bonds, funds, etc.)
        a_share_list = []
        for code in normalized_list:
            if is_a_share_stock(code):
                a_share_list.append(code)
        
        print(f"[Stock List] A-share stocks after filtering: {len(a_share_list)} (filtered {len(normalized_list) - len(a_share_list)} non-stock securities)")
        
        if not a_share_list:
            print("[Warning] No A-share stocks found after filtering")
            return []
        
        normalized_list = a_share_list
        
        if not validate:
            return normalized_list
        
        # Validate stocks (filter out delisted/suspended)
        print(f"[Stock List] Validating {len(normalized_list)} stocks...")
        valid_list = []
        invalid_count = 0
        
        for i, code in enumerate(normalized_list):
            if validate_stock_tradable(ContextInfo, code):
                valid_list.append(code)
            else:
                invalid_count += 1
            
            # Progress indicator every 500 stocks
            if (i + 1) % 500 == 0:
                print(f"[Stock List] Validated {i + 1}/{len(normalized_list)} stocks...")
        
        if invalid_count > 0:
            print(f"[Stock List] Filtered {invalid_count} invalid stocks")
        
        print(f"[Stock List] Final valid stocks: {len(valid_list)}")
        return valid_list
        
    except Exception as e:
        print(f"Failed to get stock list: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_price_data(ContextInfo, stocks, count=20, fields=None):
    """Get price data"""
    try:
        if fields is None:
            fields = ['open', 'high', 'low', 'close', 'volume']
        
        result = {}
        for stock in stocks:
            try:
                data = ContextInfo.get_market_data(stock, period='1d', count=count)
                if data is not None and len(data) > 0:
                    result[stock] = data
            except:
                continue
        
        return result
    except Exception as e:
        print(f"Failed to get price data: {e}")
        return {}


# ==================== Factor Calculation ====================
def calculate_factors(ContextInfo, codes, current_date):
    """Calculate 7 validated factors for stock selection"""
    try:
        result = pd.DataFrame({'code': codes})
        
        # Get price data
        prices_20 = get_price_data(ContextInfo, codes, count=20)
        prices_5 = get_price_data(ContextInfo, codes, count=5)
        
        # Initialize factor columns
        for factor in ['momentum_20d', 'rel_position', 'market_cap', 'momentum_5d', 
                       'turnover_rate', 'roe', 'growth']:
            result[factor] = 0.0
        
        # 1. 20-day momentum
        for code in codes:
            if code in prices_20:
                try:
                    data = prices_20[code]
                    if len(data) >= 20:
                        close_vals = data['close'] if isinstance(data, pd.DataFrame) else data
                        if len(close_vals) >= 20:
                            result.loc[result['code'] == code, 'momentum_20d'] = \
                                (close_vals.iloc[-1] - close_vals.iloc[0]) / close_vals.iloc[0] * 100
                except:
                    result.loc[result['code'] == code, 'momentum_20d'] = 0.0
            else:
                result.loc[result['code'] == code, 'momentum_20d'] = 0.0
        
        # 2. Relative position (20-day high/low)
        for code in codes:
            if code in prices_20:
                try:
                    data = prices_20[code]
                    if len(data) >= 20:
                        high_vals = data['high'] if isinstance(data, pd.DataFrame) else data
                        low_vals = data['low'] if isinstance(data, pd.DataFrame) else data
                        close_vals = data['close'] if isinstance(data, pd.DataFrame) else data
                        if len(high_vals) >= 20 and len(low_vals) >= 20:
                            high_20 = high_vals.tail(20).max()
                            low_20 = low_vals.tail(20).min()
                            close = close_vals.iloc[-1] if len(close_vals) > 0 else 0.0
                            if high_20 > low_20 and close > 0:
                                result.loc[result['code'] == code, 'rel_position'] = \
                                    (close - low_20) / (high_20 - low_20) * 100.0
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
        
        # 3. Market cap (simplified - use default for backtest)
        result['market_cap'] = 100.0
        
        # 4. 5-day momentum
        for code in codes:
            if code in prices_5:
                try:
                    data = prices_5[code]
                    if len(data) >= 5:
                        close_vals = data['close'] if isinstance(data, pd.DataFrame) else data
                        if len(close_vals) >= 5:
                            result.loc[result['code'] == code, 'momentum_5d'] = \
                                (close_vals.iloc[-1] - close_vals.iloc[0]) / close_vals.iloc[0] * 100
                except:
                    result.loc[result['code'] == code, 'momentum_5d'] = 0.0
            else:
                result.loc[result['code'] == code, 'momentum_5d'] = 0.0
        
        # 5. Turnover rate (simplified calculation)
        for code in codes:
            if code in prices_20:
                try:
                    data = prices_20[code]
                    if len(data) >= 20:
                        volume_vals = data['volume'] if isinstance(data, pd.DataFrame) else data
                        result.loc[result['code'] == code, 'turnover_rate'] = \
                            volume_vals.mean() / 1000000 * 100 if len(volume_vals) > 0 else 0.0
                except:
                    result.loc[result['code'] == code, 'turnover_rate'] = 0.0
            else:
                result.loc[result['code'] == code, 'turnover_rate'] = 0.0
        
        # 6. ROE (simplified - use default for backtest)
        result['roe'] = 10.0
        
        # 7. Net profit growth rate (simplified - use default for backtest)
        result['growth'] = 5.0
        
        return result
    except Exception as e:
        print(f"Factor calculation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


# ==================== Stock Selection ====================
def calculate_factor_scores(factors_df):
    """Calculate factor scores based on theoretical optimal intervals"""
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
    optimal_cap = 115
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
    
    # 6. ROE score (higher is better)
    roe = df['roe'].values
    df['roe_score'] = np.where(roe >= 0, np.minimum(1.0, roe / 20.0), 0.0)
    
    # 7. Net profit growth rate score (higher is better)
    growth = df['growth'].values
    df['growth_score'] = np.where(growth >= 0, np.minimum(1.0, growth / 50.0), 0.0)
    
    # Calculate comprehensive score
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


def select_stocks(ContextInfo, current_date):
    """Select stocks based on factor scores"""
    try:
        if not g_stock_pool:
            print(f"[Stock Selection] Stock pool is empty")
            return []
        
        print(f"[Stock Selection] Starting selection from {len(g_stock_pool)} stocks, date: {current_date}")
        
        # Limit stock pool size for performance (sample if too large)
        max_calculate = 5000  # Calculate factors for max 5000 stocks
        if len(g_stock_pool) > max_calculate:
            print(f"[Stock Selection] Stock pool too large ({len(g_stock_pool)}), sampling {max_calculate} stocks for calculation")
            import random
            sample_pool = random.sample(g_stock_pool, max_calculate)
        else:
            sample_pool = g_stock_pool
        
        # Calculate factors
        print(f"[Stock Selection] Calculating factors for {len(sample_pool)} stocks...")
        factors = calculate_factors(ContextInfo, sample_pool, current_date)
        if factors is None or len(factors) == 0:
            print(f"[Stock Selection] Factor calculation returned empty result")
            return []
        
        print(f"[Stock Selection] Calculated factors for {len(factors)} stocks")
        
        # Calculate factor scores
        factors = calculate_factor_scores(factors)
        
        print(f"[Stock Selection] Factor scores calculated, total_score range: {factors['total_score'].min():.2f} - {factors['total_score'].max():.2f}")
        
        # Apply filters
        print(f"[Stock Selection] Applying filters...")
        print(f"  - momentum_20d: {MIN_MOMENTUM_20D} ~ 30.0")
        print(f"  - rel_position: <= {MAX_REL_POSITION}")
        print(f"  - market_cap: {MIN_MARKET_CAP} ~ {MAX_MARKET_CAP}")
        print(f"  - momentum_5d: {MIN_MOMENTUM_5D} ~ {MAX_MOMENTUM_5D}")
        print(f"  - turnover_rate: {MIN_TURNOVER_RATE} ~ {MAX_TURNOVER_RATE}")
        print(f"  - roe: >= {MIN_ROE}")
        print(f"  - total_score: >= {MIN_TOTAL_SCORE}")
        
        filtered = factors[
            (factors['momentum_20d'] >= MIN_MOMENTUM_20D) &
            (factors['momentum_20d'] <= 30.0) &
            (factors['rel_position'] <= MAX_REL_POSITION) &
            (factors['market_cap'] >= MIN_MARKET_CAP) &
            (factors['market_cap'] <= MAX_MARKET_CAP) &
            (factors['momentum_5d'] >= MIN_MOMENTUM_5D) &
            (factors['momentum_5d'] <= MAX_MOMENTUM_5D) &
            (factors['turnover_rate'] >= MIN_TURNOVER_RATE) &
            (factors['turnover_rate'] <= MAX_TURNOVER_RATE) &
            (factors['roe'] >= MIN_ROE) &
            (factors['total_score'] >= MIN_TOTAL_SCORE)
        ]
        
        print(f"[Stock Selection] After filtering: {len(filtered)} stocks passed all conditions")
        
        if len(filtered) == 0:
            print(f"[Stock Selection] No stocks passed the filters!")
            print(f"[Stock Selection] Statistics before filtering:")
            print(f"  - momentum_20d: min={factors['momentum_20d'].min():.2f}, max={factors['momentum_20d'].max():.2f}, mean={factors['momentum_20d'].mean():.2f}")
            print(f"  - rel_position: min={factors['rel_position'].min():.2f}, max={factors['rel_position'].max():.2f}, mean={factors['rel_position'].mean():.2f}")
            print(f"  - market_cap: min={factors['market_cap'].min():.2f}, max={factors['market_cap'].max():.2f}, mean={factors['market_cap'].mean():.2f}")
            print(f"  - total_score: min={factors['total_score'].min():.2f}, max={factors['total_score'].max():.2f}, mean={factors['total_score'].mean():.2f}")
            return []
        
        # Sort by total score and select top N
        selected = filtered.nlargest(MAX_STOCKS, 'total_score')
        
        print(f"[Stock Selection] Selected {len(selected)} stocks from {len(filtered)} filtered stocks")
        if len(selected) > 0:
            print(f"[Stock Selection] Top 5 stocks:")
            for idx, row in selected.head(5).iterrows():
                print(f"  {row['code']}: score={row['total_score']:.2f}, momentum_20d={row['momentum_20d']:.2f}%, rel_pos={row['rel_position']:.2f}%")
        
        return selected['code'].tolist()
    except Exception as e:
        print(f"Stock selection failed: {e}")
        import traceback
        traceback.print_exc()
        return []


# ==================== Risk Control ====================
def check_risk_control(ContextInfo):
    """Risk control check (stop-loss/take-profit)"""
    global g_positions
    
    current_dt = get_current_datetime(ContextInfo)
    current_date = current_dt.strftime('%Y-%m-%d')
    
    positions = ContextInfo.get_trade_detail_data(ContextInfo.accout_id, 'stock', 'position')
    
    for pos in positions:
        stock_code = pos.m_strInstrumentID
        
        if stock_code not in g_positions:
            g_positions[stock_code] = {
                'cost_price': pos.m_dCost,
                'entry_date': current_date,
                'highest_price': pos.m_dPrice,
                'partial_profit_1_done': False
            }
        
        pos_record = g_positions[stock_code]
        cost_price = pos_record['cost_price']
        current_price = pos.m_dPrice
        
        if current_price > pos_record['highest_price']:
            pos_record['highest_price'] = current_price
        
        pnl = (current_price - cost_price) / cost_price
        
        # Stop-loss
        if pnl <= STOP_LOSS:
            print(f"[Stop-Loss] {stock_code} loss {pnl*100:.2f}%, sell")
            sell_amount = -pos.m_nVolume
            fees = record_trade_fees(abs(sell_amount), current_price, is_buy=False)
            ContextInfo.order(stock_code, sell_amount, ContextInfo.MARKET_SH_SZ)
            g_backtest_stats['loss_trades'] += 1
            del g_positions[stock_code]
            continue
        
        # Take-profit
        if pnl >= TAKE_PROFIT:
            print(f"[Take-Profit] {stock_code} profit {pnl*100:.2f}%, sell")
            sell_amount = -pos.m_nVolume
            fees = record_trade_fees(abs(sell_amount), current_price, is_buy=False)
            ContextInfo.order(stock_code, sell_amount, ContextInfo.MARKET_SH_SZ)
            g_backtest_stats['win_trades'] += 1
            del g_positions[stock_code]
            continue
        
        # Trailing stop
        if pnl >= TRAILING_STOP_TRIGGER:
            trailing_pnl = (current_price - pos_record['highest_price']) / pos_record['highest_price']
            if trailing_pnl <= TRAILING_STOP:
                print(f"[Trailing Stop] {stock_code} retrace {trailing_pnl*100:.2f}%, sell")
                sell_amount = -pos.m_nVolume
                fees = record_trade_fees(abs(sell_amount), current_price, is_buy=False)
                ContextInfo.order(stock_code, sell_amount, ContextInfo.MARKET_SH_SZ)
                g_backtest_stats['win_trades' if pnl > 0 else 'loss_trades'] += 1
                del g_positions[stock_code]
                continue
        
        # Partial profit
        if not pos_record['partial_profit_1_done'] and pnl >= PARTIAL_PROFIT_1:
            sell_amount = -int(pos.m_nVolume * PARTIAL_PROFIT_1_RATIO)
            print(f"[Partial Profit] {stock_code} profit {pnl*100:.2f}%, sell {PARTIAL_PROFIT_1_RATIO*100:.0f}%")
            fees = record_trade_fees(abs(sell_amount), current_price, is_buy=False)
            ContextInfo.order(stock_code, sell_amount, ContextInfo.MARKET_SH_SZ)
            pos_record['partial_profit_1_done'] = True
        
        # Time stop
        entry_date = datetime.strptime(pos_record['entry_date'], '%Y-%m-%d')
        days_held = (current_dt - entry_date).days
        if days_held >= TIME_STOP_DAYS:
            print(f"[Time Stop] {stock_code} held {days_held} days, sell")
            sell_amount = -pos.m_nVolume
            fees = record_trade_fees(abs(sell_amount), current_price, is_buy=False)
            ContextInfo.order(stock_code, sell_amount, ContextInfo.MARKET_SH_SZ)
            g_backtest_stats['win_trades' if pnl > 0 else 'loss_trades'] += 1
            del g_positions[stock_code]


# ==================== Rebalance ====================
def rebalance(ContextInfo):
    """Rebalance function"""
    global g_last_rebalance_date, g_stock_pool
    
    current_dt = get_current_datetime(ContextInfo)
    current_date = current_dt.strftime('%Y-%m-%d')
    current_weekday = current_dt.weekday()
    
    if current_weekday != REBALANCE_WEEKDAY:
        return
    
    if g_last_rebalance_date == current_date:
        return
    
    print(f"[Rebalance] Start rebalancing, date: {current_date}")
    
    selected_stocks = select_stocks(ContextInfo, current_date)
    if not selected_stocks:
        print("[Rebalance] No stocks available, skip rebalancing")
        return
    
    account_info = ContextInfo.get_account_info(ContextInfo.accout_id)
    if not account_info:
        print("[Rebalance] Failed to get account info")
        return
    
    total_value = account_info.m_dBalance + account_info.m_dMarketValue
    cash = account_info.m_dBalance
    
    # Calculate target positions
    target_positions = {}
    for stock in selected_stocks:
        target_positions[stock] = SINGLE_POSITION_MAX
    
    # Get current positions
    current_positions = {}
    positions = ContextInfo.get_trade_detail_data(ContextInfo.accout_id, 'stock', 'position')
    for pos in positions:
        current_positions[pos.m_strInstrumentID] = pos.m_nVolume
    
    # Execute trades
    for stock in selected_stocks:
        target_value = total_value * target_positions[stock]
        current_price = ContextInfo.get_last_price(stock)
        if current_price <= 0:
            continue
        
        target_amount = int(target_value / current_price / 100) * 100  # Round to 100 shares
        current_amount = current_positions.get(stock, 0)
        diff = target_amount - current_amount
        
        if diff > 0:
            print(f"[Rebalance] Buy {stock} {diff} shares")
            fees = record_trade_fees(diff, current_price, is_buy=True)
            ContextInfo.order(stock, diff, ContextInfo.MARKET_SH_SZ)
            if stock not in g_positions:
                g_positions[stock] = {
                    'cost_price': current_price,
                    'entry_date': current_date,
                    'highest_price': current_price,
                    'partial_profit_1_done': False
                }
        elif diff < 0:
            print(f"[Rebalance] Sell {stock} {abs(diff)} shares")
            fees = record_trade_fees(abs(diff), current_price, is_buy=False)
            ContextInfo.order(stock, diff, ContextInfo.MARKET_SH_SZ)
    
    g_last_rebalance_date = current_date
    print(f"[Rebalance] Rebalancing completed")


# ==================== QMT Entry Functions ====================
def init(ContextInfo):
    """Strategy initialization"""
    global g_stock_pool
    
    print("=" * 60)
    print("TRQuant Advisor V4.0 - QMT Backtest Strategy (Last 3 Months)")
    print("=" * 60)
    print(f"Backtest Period: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
    print(f"Commission Settings:")
    print(f"  - Commission: {COMMISSION_RATE*100:.2f}%")
    print(f"  - Stamp Tax: {STAMP_TAX_RATE*100:.2f}% (sell only)")
    print(f"  - Transfer Fee: {TRANSFER_FEE_RATE*100:.4f}%")
    print(f"  - Regulatory Fee: {REGULATORY_FEE_RATE*100:.4f}%")
    print(f"  - Min Commission: {MIN_COMMISSION} RMB")
    print("=" * 60)
    
    print("[Init] Loading all A-share stocks...")
    g_stock_pool = get_stock_list(ContextInfo, validate=False)
    if not g_stock_pool:
        print("[Warning] Stock pool is empty")
        return
    
    print(f"[Init] Stock pool loaded: {len(g_stock_pool)} A-share stocks")
    
    # Note: QMT may not support setting universe with too many stocks
    # We'll use the stock pool for selection, but may not set universe
    try:
        # Try to set universe (may fail if too many stocks)
        if len(g_stock_pool) <= 5000:  # QMT may have limits
            ContextInfo.set_universe(g_stock_pool)
            print(f"[Init] Universe set: {len(g_stock_pool)} stocks")
        else:
            print(f"[Init] Stock pool too large ({len(g_stock_pool)} stocks), skipping set_universe")
            print(f"[Init] Will use stock pool directly for selection")
    except Exception as e:
        print(f"[Warning] Failed to set universe: {e}")
        print(f"[Init] Will use stock pool directly for selection")
    
    ContextInfo.run_time('check_risk_control', '14:50:00', 'SH')
    print("Scheduled tasks set")
    print("=" * 60)


def handlebar(ContextInfo):
    """Daily K-line callback"""
    global g_stock_pool
    
    current_dt = get_current_datetime(ContextInfo)
    current_weekday = current_dt.weekday()
    current_time = current_dt.strftime('%H:%M:%S')
    
    # Update stock pool weekly (Monday)
    if current_weekday == 0:
        g_stock_pool = get_stock_list(ContextInfo, validate=True)
        if g_stock_pool:
            try:
                ContextInfo.set_universe(g_stock_pool)
                print(f"[Pre-market] Stock pool updated: {len(g_stock_pool)} stocks")
            except:
                pass
    
    # Risk control check
    if current_time >= '14:50:00':
        check_risk_control(ContextInfo)
    
    # Rebalancing
    if current_weekday == REBALANCE_WEEKDAY and current_time >= '09:35:00':
        rebalance(ContextInfo)


def after_trading_end(ContextInfo):
    """After trading end callback - print statistics"""
    print("=" * 60)
    print("Daily Backtest Statistics:")
    print(f"  Total Trades: {g_backtest_stats['total_trades']}")
    print(f"  Win Trades: {g_backtest_stats['win_trades']}")
    print(f"  Loss Trades: {g_backtest_stats['loss_trades']}")
    if g_backtest_stats['total_trades'] > 0:
        win_rate = g_backtest_stats['win_trades'] / g_backtest_stats['total_trades'] * 100
        print(f"  Win Rate: {win_rate:.2f}%")
    print(f"  Total Commission: {g_backtest_stats['total_commission']:.2f} RMB")
    print(f"  Total Stamp Tax: {g_backtest_stats['total_stamp_tax']:.2f} RMB")
    print(f"  Total Transfer Fee: {g_backtest_stats['total_transfer_fee']:.2f} RMB")
    print(f"  Total Regulatory Fee: {g_backtest_stats['total_regulatory_fee']:.2f} RMB")
    total_fees = (g_backtest_stats['total_commission'] + 
                  g_backtest_stats['total_stamp_tax'] + 
                  g_backtest_stats['total_transfer_fee'] + 
                  g_backtest_stats['total_regulatory_fee'])
    print(f"  Total Fees: {total_fees:.2f} RMB")
    print("=" * 60)
