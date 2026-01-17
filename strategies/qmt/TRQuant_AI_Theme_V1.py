#coding:gbk
"""
TRQuant AI Theme Strategy V1.0 - QMT Version
=============================================

AI Theme Stock Strategy - Momentum strategy based on fixed AI theme stocks

Features:
1. Fixed 15 AI core stocks pool
2. Weekly rebalancing (every 5 trading days)
3. Factor-based scoring
4. Huatai Securities standard commission
5. Complete stop-loss/take-profit and rotation logic

Stock Pool (15 AI Core Stocks):
- iFlyTek, Kingsoft Office, BlueFocus, Kunlun Tech, Fushi Holdings
- Yinli Media, Weining Health, Hundsun Tech, Tonghuashun, Yonyou
- Wondershare, Thunisoft, Talking Tom, NavInfo, Thundersoft

Backtest Parameters:
- Initial Capital: 1M RMB
- Rebalance: Weekly (5 trading days)
- Max Positions: 10
- Stop Loss: -8%
- Take Profit: +30%

Author: TRQuant Team
Version: V1.0
Date: 2026-01-12
"""

import numpy as np
from datetime import datetime

# ==================== Strategy Parameters ====================

# Rebalance period
REBALANCE_PERIOD = 5         # Weekly (5 trading days)
WARMUP_BARS = 22             # Warmup for 20-day calculation

# Position parameters
MAX_STOCKS = 10              # Max positions
MIN_SCORE = 40.0             # Min score threshold
CASH_RESERVE = 0.05          # Keep 5% cash

# Risk controls
STOP_LOSS_PCT = -0.08        # Stop loss: -8%
TAKE_PROFIT_PCT = 0.30       # Take profit: +30%
TRAILING_STOP_PCT = -0.09    # Trailing stop: -9%
TRAILING_TRIGGER_PCT = 0.15  # Trailing trigger: +15%

# Commission (Huatai Standard)
COMMISSION_RATE = 0.0001     # 0.01%
STAMP_TAX_RATE = 0.001       # 0.1% sell only
TRANSFER_FEE_RATE = 0.00001  # 0.001%
MIN_COMMISSION = 5.0         # Min 5 RMB

# ==================== AI Theme Stock Pool ====================

# 15 AI core stocks (SZ/SH format)
AI_THEME_STOCKS_SZ = [
    "002230.SZ",  # iFlyTek
    "300058.SZ",  # BlueFocus
    "300418.SZ",  # Kunlun Tech
    "300071.SZ",  # Fushi Holdings
    "300253.SZ",  # Weining Health
    "300033.SZ",  # Tonghuashun
    "300624.SZ",  # Wondershare
    "300229.SZ",  # Thunisoft
    "300459.SZ",  # Talking Tom
    "002405.SZ",  # NavInfo
    "300496.SZ",  # Thundersoft
]

AI_THEME_STOCKS_SH = [
    "688111.SH",  # Kingsoft Office
    "603598.SH",  # Yinli Media
    "600570.SH",  # Hundsun Tech
    "600588.SH",  # Yonyou
]

# Combined stock pool
AI_THEME_STOCKS = AI_THEME_STOCKS_SZ + AI_THEME_STOCKS_SH

# Stock name mapping
STOCK_NAMES = {
    "002230.SZ": "iFlyTek",
    "688111.SH": "Kingsoft",
    "300058.SZ": "BlueFocus",
    "300418.SZ": "Kunlun",
    "300071.SZ": "Fushi",
    "603598.SH": "Yinli",
    "300253.SZ": "Weining",
    "600570.SH": "Hundsun",
    "300033.SZ": "THS",
    "600588.SH": "Yonyou",
    "300624.SZ": "Wondershare",
    "300229.SZ": "Thunisoft",
    "300459.SZ": "TomCat",
    "002405.SZ": "NavInfo",
    "300496.SZ": "Thundersoft",
}


# ==================== Utility Functions ====================

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


def get_stock_name(code):
    """Get stock name"""
    return STOCK_NAMES.get(code, code)


def calculate_trade_cost(trade_value, direction):
    """
    Calculate trade cost (Huatai Standard)
    
    Args:
        trade_value: Trade amount
        direction: 'BUY' or 'SELL'
    
    Returns:
        Total trade cost
    """
    # Commission
    commission = trade_value * COMMISSION_RATE
    commission = max(commission, MIN_COMMISSION)
    
    # Transfer fee
    transfer_fee = trade_value * TRANSFER_FEE_RATE
    
    # Stamp tax (sell only)
    if direction == 'SELL':
        stamp_tax = trade_value * STAMP_TAX_RATE
    else:
        stamp_tax = 0
    
    return commission + transfer_fee + stamp_tax


def order_shares(stock, amount, price, ContextInfo, reason=""):
    """
    Execute trade order (simulation)
    
    Args:
        stock: Stock code
        amount: Quantity (positive=buy, negative=sell)
        price: Price
        ContextInfo: Context
        reason: Trade reason
    
    Returns:
        Success flag
    """
    if amount == 0 or price <= 0:
        return False
    
    direction = "BUY" if amount > 0 else "SELL"
    abs_amount = abs(amount)
    trade_value = abs_amount * price
    
    # Calculate trade cost
    fee = calculate_trade_cost(trade_value, direction)
    
    # Execute trade
    if direction == "BUY":
        total_cost = trade_value + fee
        if ContextInfo.money < total_cost:
            print(f"  [SKIP] {stock}: Insufficient funds ({ContextInfo.money:.2f} < {total_cost:.2f})")
            return False
        ContextInfo.money -= total_cost
    else:
        ContextInfo.money += trade_value - fee
    
    # Update holdings
    if stock not in ContextInfo.holdings:
        ContextInfo.holdings[stock] = 0
    
    if direction == "BUY":
        ContextInfo.holdings[stock] += abs_amount // 100
        ContextInfo.buypoint[stock] = price
        ContextInfo.highest_price[stock] = price
    else:
        lots = abs_amount // 100
        ContextInfo.holdings[stock] -= lots
        if ContextInfo.holdings[stock] <= 0:
            del ContextInfo.holdings[stock]
            if stock in ContextInfo.buypoint:
                del ContextInfo.buypoint[stock]
            if stock in ContextInfo.highest_price:
                del ContextInfo.highest_price[stock]
    
    # Record trade
    ContextInfo.total_fees += fee
    ContextInfo.trade_count += 1
    
    stock_name = get_stock_name(stock)
    reason_str = f" ({reason})" if reason else ""
    print(f"  [{direction}] {stock} {stock_name}: {abs_amount} @ {price:.2f}, Fee={fee:.2f}{reason_str}")
    
    return True


# ==================== Signal Generation ====================

def generate_signals(ContextInfo, stocks):
    """
    Generate buy/sell signals
    
    Buy signal: Price breaks above 20-day high (momentum breakout)
    Sell signal: Price falls below 60-day MA (trend breakdown)
    
    Args:
        ContextInfo: Context
        stocks: Stock list
    
    Returns:
        (buy_signals, sell_signals) dictionaries
    """
    buy = {s: 0 for s in stocks}
    sell = {s: 0 for s in stocks}
    
    # Get historical data - use mode=0 for all stocks
    data_high = ContextInfo.get_history_data(22, '1d', 'high', 0)
    data_high_pre = ContextInfo.get_history_data(2, '1d', 'high', 0)
    data_close60 = ContextInfo.get_history_data(62, '1d', 'close', 0)
    
    for k in stocks:
        if k not in data_close60:
            continue
        
        high_pre = data_high_pre.get(k, [])
        high_list = data_high.get(k, [])
        close60 = data_close60.get(k, [])
        
        if len(high_pre) < 2 or len(high_list) < 20 or len(close60) < 60:
            continue
        
        try:
            # Buy signal: yesterday high > 20-day max high (breakout)
            if high_pre[-2] > max(high_list[:-2]):
                buy[k] = 1
            
            # Sell signal: yesterday high < 60-day MA (trend breakdown)
            elif high_pre[-2] < np.mean(close60[:-2]):
                sell[k] = 1
        except:
            continue
    
    return buy, sell


# ==================== Factor Calculation ====================

def calculate_factor_scores(ContextInfo, stocks):
    """
    Calculate factor scores
    
    Factor system:
    1. 20-day momentum (40 pts): Optimal range 5%~30%
    2. Relative position (30 pts): Optimal range 40%~70%
    3. 5-day momentum (20 pts): Optimal range -2%~8%
    4. Volume ratio (10 pts): Optimal range 1.2~2.0
    
    Args:
        ContextInfo: Context
        stocks: Stock list
    
    Returns:
        {stock: score} dictionary
    """
    scores = {}
    
    # Get data
    data_close = ContextInfo.get_history_data(22, '1d', 'close', 0)
    data_high = ContextInfo.get_history_data(22, '1d', 'high', 0)
    data_low = ContextInfo.get_history_data(22, '1d', 'low', 0)
    data_volume = ContextInfo.get_history_data(22, '1d', 'volume', 0)
    
    for stock in stocks:
        if stock not in data_close:
            continue
        
        close = data_close.get(stock, [])
        high = data_high.get(stock, [])
        low = data_low.get(stock, [])
        volume = data_volume.get(stock, [])
        
        if len(close) < 20:
            continue
        
        try:
            # Factor 1: 20-day momentum (0-40 pts)
            if close[-20] > 0:
                m20 = (close[-1] - close[-20]) / close[-20] * 100
            else:
                m20 = 0
            
            # Optimal range: 5%~30%, peak at 17.5%
            if 5 <= m20 <= 30:
                m20_score = 40 - abs(m20 - 17.5) * 1.6
            else:
                m20_score = max(0, 20 - abs(m20 - 17.5))
            
            # Factor 2: Relative position (0-30 pts)
            if len(high) >= 20 and len(low) >= 20:
                h20 = max(high[-20:])
                l20 = min(low[-20:])
                if h20 > l20:
                    rel_pos = (close[-1] - l20) / (h20 - l20) * 100
                else:
                    rel_pos = 50
            else:
                rel_pos = 50
            
            # Optimal range: 40%~70%
            if 40 <= rel_pos <= 70:
                rp_score = 30
            elif rel_pos < 40:
                rp_score = 20 + rel_pos / 4
            else:
                rp_score = max(0, 30 - (rel_pos - 70) / 2)
            
            # Factor 3: 5-day momentum (0-20 pts)
            if len(close) >= 5 and close[-5] > 0:
                m5 = (close[-1] - close[-5]) / close[-5] * 100
            else:
                m5 = 0
            
            # Optimal range: -2%~8%
            if -2 <= m5 <= 8:
                m5_score = 20 - abs(m5 - 3) * 2
            else:
                m5_score = max(0, 10 - abs(m5 - 3))
            
            # Factor 4: Volume ratio (0-10 pts)
            if len(volume) >= 10:
                vol_5 = np.mean(volume[-5:])
                vol_10 = np.mean(volume[-10:-5]) if len(volume) >= 10 else vol_5
                if vol_10 > 0:
                    vol_ratio = vol_5 / vol_10
                else:
                    vol_ratio = 1
            else:
                vol_ratio = 1
            
            # Optimal range: 1.2~2.0
            if 1.2 <= vol_ratio <= 2.0:
                vol_score = 10
            elif vol_ratio > 2.0:
                vol_score = max(0, 10 - (vol_ratio - 2.0) * 5)
            else:
                vol_score = max(0, vol_ratio * 8)
            
            # Total score
            total_score = m20_score + rp_score + m5_score + vol_score
            scores[stock] = {
                'total': total_score,
                'm20': m20,
                'm20_score': m20_score,
                'rel_pos': rel_pos,
                'rp_score': rp_score,
                'm5': m5,
                'm5_score': m5_score,
                'vol_ratio': vol_ratio,
                'vol_score': vol_score,
            }
            
        except Exception as e:
            continue
    
    return scores


# ==================== Risk Control ====================

def check_risk_controls(ContextInfo, current_prices):
    """
    Check stop-loss/take-profit conditions
    
    Args:
        ContextInfo: Context
        current_prices: Current prices
    
    Returns:
        List of stocks to sell [(stock, reason)]
    """
    to_sell = []
    
    for stock in list(ContextInfo.holdings.keys()):
        if ContextInfo.holdings.get(stock, 0) <= 0:
            continue
        
        if stock not in current_prices or not current_prices[stock]:
            continue
        
        current_price = current_prices[stock][-1] if isinstance(current_prices[stock], list) else current_prices[stock]
        buy_price = ContextInfo.buypoint.get(stock, current_price)
        highest_price = ContextInfo.highest_price.get(stock, current_price)
        
        if current_price <= 0 or buy_price <= 0:
            continue
        
        # Update highest price
        if current_price > highest_price:
            ContextInfo.highest_price[stock] = current_price
            highest_price = current_price
        
        # Calculate P&L
        pnl = (current_price - buy_price) / buy_price
        
        # Stop loss check
        if pnl <= STOP_LOSS_PCT:
            to_sell.append((stock, f"STOP_LOSS {pnl*100:.1f}%"))
            continue
        
        # Take profit check
        if pnl >= TAKE_PROFIT_PCT:
            to_sell.append((stock, f"TAKE_PROFIT {pnl*100:.1f}%"))
            continue
        
        # Trailing stop check
        if pnl >= TRAILING_TRIGGER_PCT:
            from_high = (current_price - highest_price) / highest_price
            if from_high <= TRAILING_STOP_PCT:
                to_sell.append((stock, f"TRAILING {from_high*100:.1f}%"))
    
    return to_sell


# ==================== Initialization ====================

def init(ContextInfo):
    """
    Strategy initialization - QMT standard
    """
    # Set stock pool
    ContextInfo.s = AI_THEME_STOCKS
    ContextInfo.set_universe(ContextInfo.s)
    
    # Initialize variables
    ContextInfo.day = 0
    ContextInfo.holdings = {}
    ContextInfo.buypoint = {}
    ContextInfo.highest_price = {}
    ContextInfo.money = ContextInfo.capital
    ContextInfo.total_fees = 0
    ContextInfo.trade_count = 0
    ContextInfo.rebalance_count = 0
    ContextInfo.accountID = 'testS'
    
    # Print strategy info
    print("=" * 70)
    print("TRQuant AI Theme Strategy V1.0 - QMT Version")
    print("=" * 70)
    print()
    print("Strategy Configuration:")
    print(f"  Universe: AI Theme Stocks ({len(ContextInfo.s)} stocks)")
    print(f"  Capital: {ContextInfo.capital:,.2f}")
    print(f"  Max Positions: {MAX_STOCKS}")
    print(f"  Rebalance: Every {REBALANCE_PERIOD} days (Weekly)")
    print(f"  Min Score: {MIN_SCORE}")
    print()
    print("Risk Controls:")
    print(f"  Stop Loss: {STOP_LOSS_PCT*100:.1f}%")
    print(f"  Take Profit: {TAKE_PROFIT_PCT*100:.1f}%")
    print(f"  Trailing Stop: {TRAILING_STOP_PCT*100:.1f}% (trigger: {TRAILING_TRIGGER_PCT*100:.1f}%)")
    print()
    print("Commission (Huatai Standard):")
    print(f"  Rate: {COMMISSION_RATE*100:.2f}% (min {MIN_COMMISSION} RMB)")
    print(f"  Stamp Tax: {STAMP_TAX_RATE*100:.2f}% (sell only)")
    print(f"  Transfer Fee: {TRANSFER_FEE_RATE*100:.3f}%")
    print()
    print("AI Theme Stock Pool:")
    for i, stock in enumerate(ContextInfo.s, 1):
        print(f"  {i:2d}. {stock} - {get_stock_name(stock)}")
    print("=" * 70)


# ==================== Main Strategy Logic ====================

def handlebar(ContextInfo):
    """
    Main strategy logic - called for each bar
    
    Workflow:
    1. Check rebalance condition (weekly)
    2. Check risk controls (stop-loss/take-profit)
    3. Generate buy/sell signals
    4. Calculate factor scores
    5. Select stocks (Top N)
    6. Execute rotation sells
    7. Execute buys
    """
    d = ContextInfo.barpos
    
    # Get current prices
    current_prices = ContextInfo.get_history_data(1, '1d', 'open', 0)
    
    # Check risk controls (daily)
    if d > WARMUP_BARS:
        risk_sells = check_risk_controls(ContextInfo, current_prices)
        for stock, reason in risk_sells:
            if stock in current_prices and current_prices[stock]:
                price = current_prices[stock][-1] if isinstance(current_prices[stock], list) else current_prices[stock]
                amount = ContextInfo.holdings.get(stock, 0) * 100
                if amount > 0:
                    order_shares(stock, -amount, price, ContextInfo, reason)
    
    # Only execute on rebalance days after warmup
    if d <= WARMUP_BARS or d % REBALANCE_PERIOD != 0:
        return
    
    # Get current date
    try:
        nowDate = timetag_to_datetime(ContextInfo.get_bar_timetag(d))
        date_str = nowDate.strftime('%Y-%m-%d')
    except:
        date_str = f"Bar {d}"
    
    ContextInfo.rebalance_count += 1
    print()
    print("=" * 70)
    print(f"[Rebalance #{ContextInfo.rebalance_count}] {date_str}")
    print("=" * 70)
    
    # 1. Generate signals
    buys, sells = generate_signals(ContextInfo, ContextInfo.s)
    buy_count = sum(1 for v in buys.values() if v == 1)
    sell_count = sum(1 for v in sells.values() if v == 1)
    print(f"[Signals] Buy: {buy_count}, Sell: {sell_count}")
    
    # 2. Calculate factor scores
    factor_scores = calculate_factor_scores(ContextInfo, ContextInfo.s)
    print(f"[Factors] Calculated for {len(factor_scores)} stocks")
    
    # 3. Combine signals and scores
    candidates = {}
    for stock in ContextInfo.s:
        if stock in factor_scores:
            score_data = factor_scores[stock]
            total_score = score_data['total']
            
            # Buy signal bonus
            if buys.get(stock, 0) == 1:
                total_score += 10
            
            # Sell signal penalty
            if sells.get(stock, 0) == 1:
                total_score -= 20
            
            if total_score >= MIN_SCORE:
                candidates[stock] = {
                    'score': total_score,
                    'data': score_data,
                    'buy_signal': buys.get(stock, 0),
                    'sell_signal': sells.get(stock, 0),
                }
    
    print(f"[Candidates] {len(candidates)} stocks (score >= {MIN_SCORE})")
    
    # 4. Sort and select
    sorted_candidates = sorted(candidates.items(), key=lambda x: x[1]['score'], reverse=True)
    target_stocks = set(s for s, _ in sorted_candidates[:MAX_STOCKS])
    
    if sorted_candidates:
        print()
        print("[Top Candidates]")
        for i, (stock, data) in enumerate(sorted_candidates[:MAX_STOCKS], 1):
            sd = data['data']
            sig = "BUY" if data['buy_signal'] else ("SELL" if data['sell_signal'] else "-")
            print(f"  {i:2d}. {stock} {get_stock_name(stock):12s} Score={data['score']:.1f}")
            print(f"      M20={sd['m20']:.1f}%  RelPos={sd['rel_pos']:.0f}%  M5={sd['m5']:.1f}%  VolR={sd['vol_ratio']:.2f}  Sig={sig}")
    
    # 5. Rotation sells
    print()
    print("[Rotation Sells]")
    sold_count = 0
    for stock in list(ContextInfo.holdings.keys()):
        if ContextInfo.holdings.get(stock, 0) > 0:
            should_sell = (stock not in target_stocks) or (sells.get(stock, 0) == 1)
            if should_sell:
                if stock in current_prices and current_prices[stock]:
                    price = current_prices[stock][-1] if isinstance(current_prices[stock], list) else current_prices[stock]
                    amount = ContextInfo.holdings.get(stock, 0) * 100
                    if amount > 0:
                        reason = "SIGNAL" if sells.get(stock, 0) == 1 else "ROTATE"
                        order_shares(stock, -amount, price, ContextInfo, reason)
                        sold_count += 1
    
    if sold_count == 0:
        print("  No rotation sells")
    
    # 6. Calculate available funds
    available_money = ContextInfo.money * (1 - CASH_RESERVE)
    current_holding_count = len([s for s, h in ContextInfo.holdings.items() if h > 0])
    slots_available = MAX_STOCKS - current_holding_count
    
    if slots_available <= 0:
        print(f"[Buy] No slots available (current: {current_holding_count}/{MAX_STOCKS})")
    else:
        # 7. Execute buys
        print()
        print("[New Buys]")
        bought_count = 0
        
        for stock, data in sorted_candidates[:MAX_STOCKS]:
            if ContextInfo.holdings.get(stock, 0) > 0:
                continue
            
            if slots_available <= 0:
                break
            
            if stock not in current_prices or not current_prices[stock]:
                continue
            
            price = current_prices[stock][-1] if isinstance(current_prices[stock], list) else current_prices[stock]
            if price <= 0:
                continue
            
            # Calculate buy amount
            money_per_stock = available_money / slots_available
            shares = int(money_per_stock / price) // 100 * 100
            
            if shares >= 100:
                if order_shares(stock, shares, price, ContextInfo, "NEW"):
                    bought_count += 1
                    slots_available -= 1
                    available_money -= shares * price
        
        if bought_count == 0:
            print("  No new buys")
    
    # 8. Summary
    print()
    print("[Summary]")
    print(f"  Cash: {ContextInfo.money:,.2f}")
    print(f"  Total Fees: {ContextInfo.total_fees:,.2f}")
    print(f"  Trade Count: {ContextInfo.trade_count}")
    print(f"  Holdings ({len([s for s, h in ContextInfo.holdings.items() if h > 0])}):")
    
    for stock, lots in ContextInfo.holdings.items():
        if lots > 0:
            buy_price = ContextInfo.buypoint.get(stock, 0)
            if stock in current_prices and current_prices[stock]:
                curr_price = current_prices[stock][-1] if isinstance(current_prices[stock], list) else current_prices[stock]
                if buy_price > 0:
                    pnl = (curr_price - buy_price) / buy_price * 100
                    print(f"    {stock} {get_stock_name(stock):12s}: {lots} lots @ {buy_price:.2f} -> {curr_price:.2f} ({pnl:+.1f}%)")
                else:
                    print(f"    {stock} {get_stock_name(stock):12s}: {lots} lots")
    
    # Calculate returns
    if d > WARMUP_BARS:
        total_value = ContextInfo.money
        for stock, lots in ContextInfo.holdings.items():
            if lots > 0 and stock in current_prices and current_prices[stock]:
                price = current_prices[stock][-1] if isinstance(current_prices[stock], list) else current_prices[stock]
                total_value += lots * 100 * price
        
        profit_ratio = (total_value - ContextInfo.capital) / ContextInfo.capital * 100
        print()
        print(f"  Total Value: {total_value:,.2f}")
        print(f"  Profit: {profit_ratio:+.2f}%")
        
        # Paint
        if not ContextInfo.do_back_test:
            ContextInfo.paint('profit_ratio', profit_ratio / 100, -1, 0)
    
    print("=" * 70)
