#coding:gbk
"""
TRQuant Advisor V4.0 - QMT Backtest Strategy (Last 3 Months)
Based on QMT example code pattern - HS300 daily bar, rebalance every 20 trading days
Select top 10 stocks by 7-factor scores
"""
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# ==================== Strategy Parameters ====================
MAX_STOCKS = 10
MIN_TOTAL_SCORE = 20.0  # Lowered threshold for more selections
REBALANCE_PERIOD = 20   # Rebalance every 20 trading days
WARMUP_BARS = 60        # Wait for 60 bars before first trade

# Factor Weights (Validated factors)
FACTOR_WEIGHTS = {
    'momentum_20d': 1.0,
    'rel_position': 0.9,
    'market_cap': 0.85,
    'momentum_5d': 0.75,
    'turnover_rate': 0.7,
    'roe': 0.5,
    'growth': 0.4,
}
TOTAL_WEIGHT = sum(FACTOR_WEIGHTS.values())
FACTOR_WEIGHTS = {k: v / TOTAL_WEIGHT for k, v in FACTOR_WEIGHTS.items()}

# Commission Settings
COMMISSION_RATE = 0.0003  # 0.03% commission
STAMP_TAX_RATE = 0.001    # 0.1% stamp tax (sell only)
MIN_COMMISSION = 5.0      # Minimum commission (RMB)


# ==================== Helper Functions ====================
def timetag_to_datetime(timetag, format_str='%Y%m%d'):
    """Convert QMT timetag to datetime"""
    try:
        if timetag > 1e10:
            dt = datetime.fromtimestamp(timetag / 1000.0)
        else:
            dt = datetime.fromtimestamp(timetag)
        if format_str:
            return dt
        return dt
    except:
        return datetime.now()


def order_shares(stock_code, amount, order_type, price, ContextInfo, account_id):
    """
    Execute order in QMT backtest mode
    
    Note: QMT backtest mode may not support ContextInfo.order() directly.
    Instead, we update holdings and money manually to simulate trading.
    """
    if amount == 0 or price <= 0:
        return False
    
    direction = "BUY" if amount > 0 else "SELL"
    abs_amount = abs(amount)
    trade_value = abs_amount * price
    
    # Calculate fees
    if amount > 0:  # Buy
        fee = max(trade_value * COMMISSION_RATE, MIN_COMMISSION)
        total_cost = trade_value + fee
        
        # Check if enough money
        if ContextInfo.money < total_cost:
            print(f"  [{direction}] {stock_code}: Insufficient funds (need {total_cost:.2f}, have {ContextInfo.money:.2f})")
            return False
    else:  # Sell
        fee = trade_value * (COMMISSION_RATE + STAMP_TAX_RATE)
        lots_to_sell = abs_amount // 100
        
        # Check if enough holdings
        current_lots = ContextInfo.holdings.get(stock_code, 0)
        if current_lots < lots_to_sell:
            print(f"  [{direction}] {stock_code}: Insufficient holdings (need {lots_to_sell} lots, have {current_lots})")
            return False
    
    # Update holdings and money (simulate order execution)
    try:
        # Try QMT order API first (if available)
        if hasattr(ContextInfo, 'order'):
            ContextInfo.order(stock_code, amount, order_type, price, account_id)
        else:
            # Fallback: Manual position update for backtest
            if amount > 0:  # Buy
                if stock_code not in ContextInfo.holdings:
                    ContextInfo.holdings[stock_code] = 0
                ContextInfo.holdings[stock_code] += abs_amount // 100  # Convert to lots
                ContextInfo.money -= total_cost
            else:  # Sell
                if stock_code in ContextInfo.holdings:
                    ContextInfo.holdings[stock_code] -= lots_to_sell
                    ContextInfo.money += (trade_value - fee)
                    if ContextInfo.holdings[stock_code] == 0:
                        # Remove from holdings if fully sold
                        del ContextInfo.holdings[stock_code]
        
        print(f"  [{direction}] {stock_code}: {abs_amount} shares @ {price:.2f} (fee: {fee:.2f})")
        return True
    except Exception as e:
        # If order API fails, use manual update
        try:
            if amount > 0:  # Buy
                if stock_code not in ContextInfo.holdings:
                    ContextInfo.holdings[stock_code] = 0
                ContextInfo.holdings[stock_code] += abs_amount // 100
                ContextInfo.money -= total_cost
            else:  # Sell
                if stock_code in ContextInfo.holdings:
                    ContextInfo.holdings[stock_code] -= lots_to_sell
                    ContextInfo.money += (trade_value - fee)
                    if ContextInfo.holdings[stock_code] == 0:
                        del ContextInfo.holdings[stock_code]
            
            print(f"  [{direction}] {stock_code}: {abs_amount} shares @ {price:.2f} (fee: {fee:.2f}, manual)")
            return True
        except Exception as e2:
            print(f"  [Order Error] {stock_code}: {e2}")
            return False


def calculate_factor_score(momentum_20d, rel_position, momentum_5d, turnover_rate):
    """Calculate comprehensive factor score"""
    score = 0.0
    
    # Momentum 20d score (5%~30% optimal)
    if 5 <= momentum_20d <= 30:
        m20_score = 1.0 - abs(momentum_20d - 17.5) / 12.5
    else:
        m20_score = max(0, 1.0 - abs(momentum_20d - 17.5) / 25.0)
    score += m20_score * FACTOR_WEIGHTS['momentum_20d']
    
    # Relative position score (50%~80% optimal)
    if 50 <= rel_position <= 80:
        rp_score = 1.0
    else:
        rp_score = max(0, 1.0 - abs(rel_position - 65) / 50.0)
    score += rp_score * FACTOR_WEIGHTS['rel_position']
    
    # Momentum 5d score (-2%~5% optimal)
    if -2 <= momentum_5d <= 5:
        m5_score = 1.0 - abs(momentum_5d - 1.5) / 3.5
    else:
        m5_score = max(0, 1.0 - abs(momentum_5d - 1.5) / 10.0)
    score += m5_score * FACTOR_WEIGHTS['momentum_5d']
    
    # Turnover rate score (2%~8% optimal)
    if 2 <= turnover_rate <= 8:
        tr_score = 1.0 - abs(turnover_rate - 5) / 3.0
    else:
        tr_score = max(0, 1.0 - abs(turnover_rate - 5) / 10.0)
    score += tr_score * FACTOR_WEIGHTS['turnover_rate']
    
    # Add default scores for simplified factors
    score += 0.5 * (FACTOR_WEIGHTS['market_cap'] + FACTOR_WEIGHTS['roe'] + FACTOR_WEIGHTS['growth'])
    
    return score * 100


def get_stock_factors(ContextInfo, stock, d):
    """Calculate factors for a single stock"""
    try:
        # Get 22 days of price data for calculations
        data_close = ContextInfo.get_history_data(22, '1d', 'close', 3)
        data_high = ContextInfo.get_history_data(22, '1d', 'high', 3)
        data_low = ContextInfo.get_history_data(22, '1d', 'low', 3)
        data_volume = ContextInfo.get_history_data(22, '1d', 'volume', 3)
        
        if stock not in data_close or len(data_close[stock]) < 20:
            return None
        
        close = data_close[stock]
        high = data_high.get(stock, [])
        low = data_low.get(stock, [])
        volume = data_volume.get(stock, [])
        
        # 20-day momentum
        if len(close) >= 20:
            momentum_20d = (close[-1] - close[-20]) / close[-20] * 100 if close[-20] > 0 else 0
        else:
            momentum_20d = 0
        
        # 5-day momentum
        if len(close) >= 5:
            momentum_5d = (close[-1] - close[-5]) / close[-5] * 100 if close[-5] > 0 else 0
        else:
            momentum_5d = 0
        
        # Relative position (20-day)
        if len(high) >= 20 and len(low) >= 20:
            high_20 = max(high[-20:])
            low_20 = min(low[-20:])
            if high_20 > low_20:
                rel_position = (close[-1] - low_20) / (high_20 - low_20) * 100
            else:
                rel_position = 50
        else:
            rel_position = 50
        
        # Turnover rate (simplified)
        if len(volume) >= 5:
            avg_volume = sum(volume[-5:]) / 5
            turnover_rate = avg_volume / 1000000 * 5  # Simplified calculation
        else:
            turnover_rate = 3
        
        return {
            'momentum_20d': momentum_20d,
            'momentum_5d': momentum_5d,
            'rel_position': rel_position,
            'turnover_rate': turnover_rate
        }
    except Exception as e:
        return None


# ==================== Signal Generation ====================
def generate_signals(ContextInfo):
    """Generate buy/sell signals based on factor scores"""
    buy = {i: 0 for i in ContextInfo.s}
    sell = {i: 0 for i in ContextInfo.s}
    rank_total = {}
    
    # Get price data
    data_high = ContextInfo.get_history_data(22, '1d', 'high', 3)
    data_high_pre = ContextInfo.get_history_data(2, '1d', 'high', 3)
    data_close60 = ContextInfo.get_history_data(62, '1d', 'close', 3)
    
    for k in ContextInfo.s:
        if k in data_close60:
            if len(data_high_pre.get(k, [])) == 2 and len(data_high.get(k, [])) >= 20 and len(data_close60.get(k, [])) >= 60:
                # Price breakout signal
                if data_high_pre[k][-2] > max(data_high[k][:-2]):
                    buy[k] = 1  # Breakout 20-day high
                elif data_high_pre[k][-2] < np.mean(data_close60[k][:-2]):
                    sell[k] = 1  # Below 60-day MA
    
    # Calculate factor scores for buy candidates
    for k in ContextInfo.s:
        if buy[k] == 1:
            factors = get_stock_factors(ContextInfo, k, ContextInfo.barpos)
            if factors:
                score = calculate_factor_score(
                    factors['momentum_20d'],
                    factors['rel_position'],
                    factors['momentum_5d'],
                    factors['turnover_rate']
                )
                if score >= MIN_TOTAL_SCORE:
                    rank_total[k] = score
                else:
                    buy[k] = 0  # Remove from buy list if score too low
            else:
                buy[k] = 0  # Remove if can't calculate factors
    
    return buy, sell, rank_total


# ==================== Main Functions ====================
def init(ContextInfo):
    """Strategy initialization (QMT standard)"""
    # Get HS300 constituents
    ContextInfo.s = ContextInfo.get_sector('000300.SH')
    ContextInfo.set_universe(ContextInfo.s)
    
    # Initialize tracking variables
    ContextInfo.day = 0
    ContextInfo.holdings = {i: 0 for i in ContextInfo.s}
    ContextInfo.weight = [0.1] * MAX_STOCKS  # Equal weight for 10 stocks
    ContextInfo.buypoint = {}
    ContextInfo.money = ContextInfo.capital
    ContextInfo.profit = 0
    ContextInfo.accountID = 'testS'
    
    print("=" * 60)
    print("TRQuant Advisor V4.0 - QMT Backtest Strategy")
    print("=" * 60)
    print(f"Universe: HS300 ({len(ContextInfo.s)} stocks)")
    print(f"Initial Capital: {ContextInfo.capital:.2f}")
    print(f"Max Positions: {MAX_STOCKS}")
    print(f"Rebalance Period: Every {REBALANCE_PERIOD} trading days")
    print(f"Warmup Bars: {WARMUP_BARS}")
    print("=" * 60)


def handlebar(ContextInfo):
    """Main strategy logic (called for each bar)"""
    d = ContextInfo.barpos
    
    # Get current price data
    price = ContextInfo.get_history_data(1, '1d', 'open', 3)
    
    # Only trade after warmup period and on rebalance days
    if d > WARMUP_BARS and d % REBALANCE_PERIOD == 0:
        # Print current date
        nowDate = timetag_to_datetime(ContextInfo.get_bar_timetag(d), '%Y%m%d')
        print(f"\n[Bar {d}] {nowDate.strftime('%Y-%m-%d')} - Rebalancing")
        
        # Generate signals
        buys, sells, rank_total = generate_signals(ContextInfo)
        
        # Sort by factor score and select top stocks
        tmp = sorted(list(rank_total.items()), key=lambda item: item[1], reverse=True)
        
        # Select top N stocks
        if len(tmp) >= MAX_STOCKS:
            tmp_stock = {i[0] for i in tmp[:MAX_STOCKS]}
        else:
            tmp_stock = {i[0] for i in tmp}
        
        # Remove stocks not in top selection from buy list
        for k in list(buys.keys()):
            if k not in tmp_stock:
                buys[k] = 0
        
        if tmp_stock:
            print(f"Stock pool: {len(tmp_stock)} stocks")
            for stock, score in tmp[:5]:  # Print top 5
                print(f"  {stock}: score={score:.2f}")
            
            # Execute sells first
            for k in ContextInfo.s:
                if ContextInfo.holdings.get(k, 0) > 0 and sells.get(k, 0) == 1:
                    if k in price and price[k]:
                        sell_price = price[k][-1] if isinstance(price[k], list) else price[k]
                        sell_amount = ContextInfo.holdings[k] * 100
                        
                        print(f"\n[SELL] {k}")
                        if order_shares(k, -sell_amount, 'fix', sell_price, ContextInfo, ContextInfo.accountID):
                            # Update profit tracking (order_shares already updated holdings and money)
                            entry_price = ContextInfo.buypoint.get(k, sell_price)
                            if entry_price > 0:
                                ContextInfo.profit += (sell_price - entry_price) * sell_amount
                            if k in ContextInfo.buypoint:
                                del ContextInfo.buypoint[k]
            
            # Calculate money distribution for buys
            ContextInfo.money_distribution = {k: w * ContextInfo.money for k, w in zip(tmp_stock, ContextInfo.weight[:len(tmp_stock)])}
            
            # Execute buys
            for k in tmp_stock:
                if ContextInfo.holdings.get(k, 0) == 0 and buys.get(k, 0) == 1:
                    if k in price and price[k]:
                        buy_price = price[k][-1] if isinstance(price[k], list) else price[k]
                        if buy_price > 0:
                            order_amount = int(ContextInfo.money_distribution[k] / buy_price) // 100  # Lots
                            
                            if order_amount > 0:
                                print(f"\n[BUY] {k}")
                                if order_shares(k, order_amount * 100, 'fix', buy_price, ContextInfo, ContextInfo.accountID):
                                    # Update tracking (order_shares already updated holdings and money)
                                    ContextInfo.buypoint[k] = buy_price
                                    fee = buy_price * order_amount * 100 * COMMISSION_RATE
                                    ContextInfo.profit -= fee
            
            print(f"\n[Summary] Cash: {ContextInfo.money:.2f}, Profit: {ContextInfo.profit:.2f}, Capital: {ContextInfo.capital:.2f}")
    
    # Calculate and display profit ratio
    profit_ratio = ContextInfo.profit / ContextInfo.capital
    if not ContextInfo.do_back_test:
        ContextInfo.paint('profit_ratio', profit_ratio, -1, 0)


def after_trading_end(ContextInfo):
    """End of day summary"""
    d = ContextInfo.barpos
    if d % REBALANCE_PERIOD == 0:
        print(f"\n[EOD Bar {d}] Current positions:")
        active_positions = {k: v for k, v in ContextInfo.holdings.items() if v > 0}
        if active_positions:
            for stock, lots in active_positions.items():
                entry_price = ContextInfo.buypoint.get(stock, 0)
                print(f"  {stock}: {lots} lots @ {entry_price:.2f}")
        else:
            print("  No positions")
