#coding:gbk
"""
QMT Basic Backtest Template
===========================

A minimal template for QMT backtesting.

Features:
- HS300 universe
- 20-day rebalance cycle
- Simple price breakout strategy

Usage:
1. Copy this file to QMT strategy folder
2. Modify signal logic as needed
3. Run backtest in QMT

Template Parameters (customize below):
- REBALANCE_PERIOD: Days between rebalances
- MAX_STOCKS: Maximum positions
- WARMUP_BARS: Bars to wait before trading
"""
import numpy as np
from datetime import datetime

# ==================== Template Parameters ====================
REBALANCE_PERIOD = 20   # Rebalance every N trading days
MAX_STOCKS = 10         # Maximum number of stocks to hold
WARMUP_BARS = 60        # Wait N bars before first trade
COMMISSION_RATE = 0.0003  # 0.03% commission


# ==================== Helper Functions ====================
def timetag_to_datetime(timetag, format_str='%Y%m%d'):
    """Convert QMT timetag to datetime"""
    try:
        if timetag > 1e10:
            return datetime.fromtimestamp(timetag / 1000.0)
        return datetime.fromtimestamp(timetag)
    except:
        return datetime.now()


def order_shares(stock_code, amount, order_type, price, ContextInfo, account_id):
    """Execute order"""
    if amount == 0:
        return
    try:
        ContextInfo.order(stock_code, amount, order_type, price, account_id)
        direction = "BUY" if amount > 0 else "SELL"
        print(f"  [{direction}] {stock_code}: {abs(amount)} shares @ {price:.2f}")
    except Exception as e:
        print(f"  [Order Error] {stock_code}: {e}")


# ==================== Signal Logic ====================
def generate_signals(ContextInfo):
    """
    Generate buy/sell signals
    
    Returns:
        tuple: (buy_dict, sell_dict)
    """
    buy = {i: 0 for i in ContextInfo.s}
    sell = {i: 0 for i in ContextInfo.s}
    
    # Get price data
    data_high = ContextInfo.get_history_data(22, '1d', 'high', 3)
    data_high_pre = ContextInfo.get_history_data(2, '1d', 'high', 3)
    data_close60 = ContextInfo.get_history_data(62, '1d', 'close', 3)
    
    for k in ContextInfo.s:
        if k not in data_close60:
            continue
            
        high_pre = data_high_pre.get(k, [])
        high_22 = data_high.get(k, [])
        close_60 = data_close60.get(k, [])
        
        if len(high_pre) >= 2 and len(high_22) >= 20 and len(close_60) >= 60:
            # Buy signal: breakout 20-day high
            if high_pre[-2] > max(high_22[:-2]):
                buy[k] = 1
            # Sell signal: below 60-day MA
            elif high_pre[-2] < np.mean(close_60[:-2]):
                sell[k] = 1
    
    return buy, sell


# ==================== Main Functions ====================
def init(ContextInfo):
    """Strategy initialization"""
    # Get HS300 constituents
    ContextInfo.s = ContextInfo.get_sector('000300.SH')
    ContextInfo.set_universe(ContextInfo.s)
    
    # Initialize tracking
    ContextInfo.holdings = {i: 0 for i in ContextInfo.s}
    ContextInfo.weight = [1.0 / MAX_STOCKS] * MAX_STOCKS
    ContextInfo.buypoint = {}
    ContextInfo.money = ContextInfo.capital
    ContextInfo.profit = 0
    ContextInfo.accountID = 'testS'
    
    print("=" * 60)
    print("QMT Basic Backtest Template")
    print("=" * 60)
    print(f"Universe: HS300 ({len(ContextInfo.s)} stocks)")
    print(f"Capital: {ContextInfo.capital:.2f}")
    print(f"Max Positions: {MAX_STOCKS}")
    print(f"Rebalance Period: {REBALANCE_PERIOD} days")
    print("=" * 60)


def handlebar(ContextInfo):
    """Main strategy logic"""
    d = ContextInfo.barpos
    price = ContextInfo.get_history_data(1, '1d', 'open', 3)
    
    # Only trade after warmup and on rebalance days
    if d > WARMUP_BARS and d % REBALANCE_PERIOD == 0:
        nowDate = timetag_to_datetime(ContextInfo.get_bar_timetag(d))
        print(f"\n[Bar {d}] {nowDate.strftime('%Y-%m-%d')}")
        
        # Generate signals
        buys, sells = generate_signals(ContextInfo)
        
        # Get buy candidates
        buy_stocks = [k for k, v in buys.items() if v == 1][:MAX_STOCKS]
        
        if buy_stocks:
            print(f"Buy candidates: {len(buy_stocks)} stocks")
            
            # Sell existing positions if sell signal
            for k in ContextInfo.s:
                if ContextInfo.holdings[k] > 0 and sells[k] == 1:
                    if k in price and price[k]:
                        sell_price = price[k][-1] if isinstance(price[k], list) else price[k]
                        sell_amount = ContextInfo.holdings[k] * 100
                        
                        order_shares(k, -sell_amount, 'fix', sell_price, ContextInfo, ContextInfo.accountID)
                        
                        fee = sell_price * sell_amount * COMMISSION_RATE
                        ContextInfo.money += sell_price * sell_amount - fee
                        ContextInfo.holdings[k] = 0
            
            # Calculate position sizes
            money_per_stock = {k: w * ContextInfo.money for k, w in zip(buy_stocks, ContextInfo.weight[:len(buy_stocks)])}
            
            # Buy new positions
            for k in buy_stocks:
                if ContextInfo.holdings[k] == 0 and buys.get(k, 0) == 1:
                    if k in price and price[k]:
                        buy_price = price[k][-1] if isinstance(price[k], list) else price[k]
                        if buy_price > 0:
                            order_amount = int(money_per_stock[k] / buy_price) // 100
                            
                            if order_amount > 0:
                                order_shares(k, order_amount * 100, 'fix', buy_price, ContextInfo, ContextInfo.accountID)
                                
                                ContextInfo.buypoint[k] = buy_price
                                fee = buy_price * order_amount * 100 * COMMISSION_RATE
                                ContextInfo.money -= buy_price * order_amount * 100 + fee
                                ContextInfo.holdings[k] = order_amount
            
            print(f"[Summary] Cash: {ContextInfo.money:.2f}, Profit: {ContextInfo.profit:.2f}")
    
    # Track profit ratio
    profit_ratio = ContextInfo.profit / ContextInfo.capital if ContextInfo.capital > 0 else 0
    if not ContextInfo.do_back_test:
        ContextInfo.paint('profit_ratio', profit_ratio, -1, 0)
