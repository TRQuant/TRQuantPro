#coding:gbk
# TRQuant Weekly Simple Strategy V4.0
# Based on QMT example - using price signals only
# Proven to work in QMT backtest
import pandas as pd
import numpy as np
from datetime import datetime

# ==================== Strategy Parameters ====================
REBALANCE_PERIOD = 5         # Weekly (5 trading days)
WARMUP_BARS = 22             # Warmup for 20-day calculation
MAX_STOCKS = 10              # Max positions
WEIGHT = [0.1] * 10          # Equal weight

# Commission (Huatai Standard)
COMMISSION_RATE = 0.0001     # 0.01%
STAMP_TAX_RATE = 0.001       # 0.1% sell only
MIN_COMMISSION = 5.0


def timetag_to_datetime(timetag, format_str='%Y%m%d'):
    """Convert timetag to datetime"""
    try:
        if timetag > 1e10:
            dt = datetime.fromtimestamp(timetag / 1000.0)
        else:
            dt = datetime.fromtimestamp(timetag)
        return dt
    except:
        return datetime.now()


def order_shares(stock, amount, order_type, price, ContextInfo, accountID):
    """Execute order - works for both API mode and manual simulation"""
    if amount == 0 or price <= 0:
        return False
    
    direction = "BUY" if amount > 0 else "SELL"
    abs_amount = abs(amount)
    trade_value = abs_amount * price
    
    # Calculate fee
    if amount > 0:
        fee = max(trade_value * COMMISSION_RATE, MIN_COMMISSION)
        total_cost = trade_value + fee
        if ContextInfo.money < total_cost:
            return False
        ContextInfo.money -= total_cost
    else:
        fee = trade_value * (COMMISSION_RATE + STAMP_TAX_RATE)
        ContextInfo.money += trade_value - fee
    
    # Update holdings
    if stock not in ContextInfo.holdings:
        ContextInfo.holdings[stock] = 0
    
    if amount > 0:
        ContextInfo.holdings[stock] += abs_amount // 100
        ContextInfo.buypoint[stock] = price
    else:
        lots = abs_amount // 100
        ContextInfo.holdings[stock] -= lots
        if ContextInfo.holdings[stock] <= 0:
            del ContextInfo.holdings[stock]
            if stock in ContextInfo.buypoint:
                del ContextInfo.buypoint[stock]
    
    ContextInfo.profit -= fee
    print(f'{direction}: {stock} {abs_amount} @ {price:.2f} fee={fee:.2f}')
    return True


def signal(ContextInfo):
    """
    Generate buy/sell signals based on proven price signals
    
    Buy signal: Price breaks above 20-day high (momentum breakout)
    Sell signal: Price falls below 60-day MA (trend breakdown)
    
    This is the same logic from the QMT example code that worked!
    """
    buy = {i: 0 for i in ContextInfo.s}
    sell = {i: 0 for i in ContextInfo.s}
    
    # Get historical data - mode 0 returns dict for all stocks
    data_high = ContextInfo.get_history_data(22, '1d', 'high', 0)
    data_high_pre = ContextInfo.get_history_data(2, '1d', 'high', 0)
    data_close60 = ContextInfo.get_history_data(62, '1d', 'close', 0)
    
    for k in ContextInfo.s:
        if k not in data_close60:
            continue
        
        high_pre = data_high_pre.get(k, [])
        high_list = data_high.get(k, [])
        close60 = data_close60.get(k, [])
        
        if len(high_pre) < 2 or len(high_list) < 20 or len(close60) < 60:
            continue
        
        # Buy signal: yesterday's high > 20-day max high (breakout)
        if high_pre[-2] > max(high_list[:-2]):
            buy[k] = 1
        
        # Sell signal: yesterday's high < 60-day MA (trend breakdown)
        elif high_pre[-2] < np.mean(close60[:-2]):
            sell[k] = 1
    
    return buy, sell


def calculate_factor_rank(ContextInfo, candidates):
    """
    Calculate factor scores for ranking candidates
    
    Uses only price-based factors that work in QMT:
    1. 20-day momentum (momentum_20d)
    2. Relative position (rel_position)  
    3. 5-day momentum (momentum_5d)
    4. Volume ratio (volume_ratio)
    """
    rank_total = {}
    
    # Get data
    data_close = ContextInfo.get_history_data(22, '1d', 'close', 0)
    data_high = ContextInfo.get_history_data(22, '1d', 'high', 0)
    data_low = ContextInfo.get_history_data(22, '1d', 'low', 0)
    data_volume = ContextInfo.get_history_data(22, '1d', 'volume', 0)
    
    for stock in candidates:
        if stock not in data_close:
            continue
        
        close = data_close.get(stock, [])
        high = data_high.get(stock, [])
        low = data_low.get(stock, [])
        volume = data_volume.get(stock, [])
        
        if len(close) < 20:
            continue
        
        try:
            # Factor 1: 20-day momentum (score 0-40)
            if close[-20] > 0:
                m20 = (close[-1] - close[-20]) / close[-20] * 100
            else:
                m20 = 0
            
            # Optimal range: 5%~30%, score = 40 at 15%
            if 5 <= m20 <= 30:
                m20_score = 40 - abs(m20 - 17.5) * 1.6
            else:
                m20_score = max(0, 20 - abs(m20 - 17.5))
            
            # Factor 2: Relative position (score 0-30)
            if len(high) >= 20 and len(low) >= 20:
                h20 = max(high[-20:])
                l20 = min(low[-20:])
                if h20 > l20:
                    rel_pos = (close[-1] - l20) / (h20 - l20) * 100
                else:
                    rel_pos = 50
            else:
                rel_pos = 50
            
            # Optimal: 40%~70%, avoid extremes
            if 40 <= rel_pos <= 70:
                rp_score = 30
            elif rel_pos < 40:
                rp_score = 20 + rel_pos / 4
            else:
                rp_score = max(0, 30 - (rel_pos - 70) / 2)
            
            # Factor 3: 5-day momentum (score 0-20)
            if len(close) >= 5 and close[-5] > 0:
                m5 = (close[-1] - close[-5]) / close[-5] * 100
            else:
                m5 = 0
            
            # Optimal: -2%~8%
            if -2 <= m5 <= 8:
                m5_score = 20 - abs(m5 - 3) * 2
            else:
                m5_score = max(0, 10 - abs(m5 - 3))
            
            # Factor 4: Volume trend (score 0-10)
            if len(volume) >= 10:
                vol_5 = np.mean(volume[-5:])
                vol_10 = np.mean(volume[-10:-5]) if len(volume) >= 10 else vol_5
                if vol_10 > 0:
                    vol_ratio = vol_5 / vol_10
                else:
                    vol_ratio = 1
            else:
                vol_ratio = 1
            
            # Optimal: 1.2~2.0 (increasing volume)
            if 1.2 <= vol_ratio <= 2.0:
                vol_score = 10
            elif vol_ratio > 2.0:
                vol_score = max(0, 10 - (vol_ratio - 2.0) * 5)
            else:
                vol_score = max(0, vol_ratio * 8)
            
            # Total score
            total_score = m20_score + rp_score + m5_score + vol_score
            rank_total[stock] = total_score
            
        except Exception as e:
            continue
    
    return rank_total


def init(ContextInfo):
    """Initialize strategy - QMT standard"""
    # Use HS300 index constituents
    ContextInfo.s = ContextInfo.get_sector('000300.SH')
    ContextInfo.set_universe(ContextInfo.s)
    
    # Initialize variables
    ContextInfo.day = 0
    ContextInfo.holdings = {i: 0 for i in ContextInfo.s}
    ContextInfo.weight = WEIGHT
    ContextInfo.buypoint = {}
    ContextInfo.money = ContextInfo.capital
    ContextInfo.profit = 0
    ContextInfo.accountID = 'testS'
    
    print("=" * 60)
    print("TRQuant Weekly Simple Strategy V4.0")
    print("=" * 60)
    print(f"Universe: HS300 ({len(ContextInfo.s)} stocks)")
    print(f"Capital: {ContextInfo.capital:.2f}")
    print(f"Max Positions: {MAX_STOCKS}")
    print(f"Rebalance: Every {REBALANCE_PERIOD} days (Weekly)")
    print(f"Commission: {COMMISSION_RATE*100:.2f}% (min {MIN_COMMISSION})")
    print("=" * 60)


def handlebar(ContextInfo):
    """Main strategy logic - QMT standard"""
    d = ContextInfo.barpos
    
    # Get current prices
    price = ContextInfo.get_history_data(1, '1d', 'open', 0)
    
    # Only trade after warmup and on rebalance days
    if d > WARMUP_BARS and d % REBALANCE_PERIOD == 0:
        nowDate = timetag_to_datetime(ContextInfo.get_bar_timetag(d), '%Y%m%d')
        print(f'\n[{nowDate.strftime("%Y-%m-%d")}] Rebalancing...')
        
        # Generate signals
        buys, sells = signal(ContextInfo)
        
        # Get candidates with buy signal
        candidates = [k for k, v in buys.items() if v == 1]
        
        if not candidates:
            print('  No buy signals')
        else:
            # Rank by factor scores
            rank_total = calculate_factor_rank(ContextInfo, candidates)
            
            if not rank_total:
                print('  No valid candidates after ranking')
            else:
                # Sort by score, select top N
                tmp = sorted(rank_total.items(), key=lambda x: x[1], reverse=True)
                tmp_stock = set(s for s, _ in tmp[:MAX_STOCKS])
                
                print(f'  Candidates: {len(rank_total)}, Selected: {len(tmp_stock)}')
                for s, score in tmp[:5]:
                    print(f'    {s}: {score:.1f}')
                
                # Step 1: Sell positions not in target list (rotation)
                for k in list(ContextInfo.holdings.keys()):
                    if ContextInfo.holdings.get(k, 0) > 0:
                        # Sell if not in target list OR has sell signal
                        if k not in tmp_stock or sells.get(k, 0) == 1:
                            if k in price and price[k]:
                                sell_price = price[k][-1] if isinstance(price[k], list) else price[k]
                                sell_amount = ContextInfo.holdings[k] * 100
                                order_shares(k, -sell_amount, 'fix', sell_price, ContextInfo, ContextInfo.accountID)
                
                # Step 2: Calculate money per stock
                money_dist = {k: w * ContextInfo.money for k, w in zip(tmp_stock, ContextInfo.weight[:len(tmp_stock)])}
                
                # Step 3: Buy new positions
                for k in tmp_stock:
                    if ContextInfo.holdings.get(k, 0) == 0:
                        if k in price and price[k]:
                            buy_price = price[k][-1] if isinstance(price[k], list) else price[k]
                            if buy_price > 0:
                                order_amt = int(money_dist[k] / buy_price) // 100 * 100
                                if order_amt >= 100:
                                    order_shares(k, order_amt, 'fix', buy_price, ContextInfo, ContextInfo.accountID)
                
                # Summary
                print(f'  Cash: {ContextInfo.money:.2f}, Profit: {ContextInfo.profit:.2f}')
    
    # Paint profit ratio
    profit_ratio = ContextInfo.profit / ContextInfo.capital
    if not ContextInfo.do_back_test:
        ContextInfo.paint('profit_ratio', profit_ratio, -1, 0)
