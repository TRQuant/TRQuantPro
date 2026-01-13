#coding:gbk
"""
QMT Basic Live Trading Template
===============================

A minimal template for live trading in QMT.

IMPORTANT: Live trading requires:
1. Valid QMT trading account
2. Account ID configuration
3. Proper risk management

Template Parameters (customize below):
- ACCOUNT_ID: Your trading account ID
- MAX_STOCKS: Maximum positions
- REBALANCE_DAY: Day of week for rebalancing (0=Monday)
"""
import numpy as np
from datetime import datetime

# ==================== Account Settings ====================
ACCOUNT_ID = 'your_account_id'  # CHANGE THIS to your account ID

# Trading parameters
MAX_STOCKS = 5          # Fewer positions for live trading
REBALANCE_DAY = 0       # Monday
REBALANCE_TIME = '09:35:00'
COMMISSION_RATE = 0.0003

# Risk limits for live trading
MAX_SINGLE_POSITION = 0.15  # 15% max per position
MAX_DRAWDOWN = 0.10         # 10% max portfolio drawdown


# ==================== Helper Functions ====================
def order_shares(stock_code, amount, order_type, price, ContextInfo, account_id):
    """Execute order with validation"""
    if amount == 0:
        return
    
    # Validate order size
    if abs(amount) < 100:
        print(f"  [Warning] Order size too small: {amount}")
        return
    
    try:
        ContextInfo.order(stock_code, amount, order_type, price, account_id)
        direction = "BUY" if amount > 0 else "SELL"
        print(f"  [{direction}] {stock_code}: {abs(amount)} shares @ {price:.2f}")
    except Exception as e:
        print(f"  [Order Error] {stock_code}: {e}")


def get_current_time():
    """Get current time string"""
    return datetime.now().strftime('%H:%M:%S')


def is_trading_time():
    """Check if current time is valid for trading"""
    current = get_current_time()
    # Morning session: 09:30 - 11:30
    # Afternoon session: 13:00 - 15:00
    morning = '09:30:00' <= current <= '11:30:00'
    afternoon = '13:00:00' <= current <= '14:55:00'
    return morning or afternoon


# ==================== Signal Logic ====================
def generate_signals(ContextInfo):
    """Generate buy/sell signals"""
    buy = {}
    sell = {}
    
    # Get price data
    data_high = ContextInfo.get_history_data(22, '1d', 'high', 3)
    data_high_pre = ContextInfo.get_history_data(2, '1d', 'high', 3)
    data_close60 = ContextInfo.get_history_data(62, '1d', 'close', 3)
    
    for k in ContextInfo.s:
        buy[k] = 0
        sell[k] = 0
        
        if k not in data_close60:
            continue
            
        high_pre = data_high_pre.get(k, [])
        high_22 = data_high.get(k, [])
        close_60 = data_close60.get(k, [])
        
        if len(high_pre) >= 2 and len(high_22) >= 20 and len(close_60) >= 60:
            if high_pre[-2] > max(high_22[:-2]):
                buy[k] = 1
            elif high_pre[-2] < np.mean(close_60[:-2]):
                sell[k] = 1
    
    return buy, sell


# ==================== Main Functions ====================
def init(ContextInfo):
    """Strategy initialization"""
    if ACCOUNT_ID == 'your_account_id':
        print("ERROR: Please configure your ACCOUNT_ID before live trading!")
        return
    
    ContextInfo.s = ContextInfo.get_sector('000300.SH')
    ContextInfo.set_universe(ContextInfo.s)
    
    ContextInfo.holdings = {}
    ContextInfo.buypoint = {}
    ContextInfo.accountID = ACCOUNT_ID
    
    # Schedule rebalancing
    ContextInfo.run_time('rebalance', REBALANCE_TIME, 'SH')
    
    print("=" * 60)
    print("QMT Live Trading Template - INITIALIZED")
    print("=" * 60)
    print(f"Account: {ACCOUNT_ID}")
    print(f"Universe: HS300 ({len(ContextInfo.s)} stocks)")
    print(f"Max Positions: {MAX_STOCKS}")
    print(f"Rebalance: {['Mon','Tue','Wed','Thu','Fri'][REBALANCE_DAY]} @ {REBALANCE_TIME}")
    print("=" * 60)


def handlebar(ContextInfo):
    """Main strategy logic for live trading"""
    if not is_trading_time():
        return
    
    # Get current weekday
    current_weekday = datetime.now().weekday()
    
    # Only trade on rebalance day
    if current_weekday != REBALANCE_DAY:
        return
    
    # Additional check - run_time should handle this, but double-check
    current_time = get_current_time()
    if current_time < REBALANCE_TIME:
        return
    
    # Proceed with rebalancing
    rebalance(ContextInfo)


def rebalance(ContextInfo):
    """Execute rebalancing"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting rebalance...")
    
    # Generate signals
    buys, sells = generate_signals(ContextInfo)
    
    # Get current price
    price = ContextInfo.get_history_data(1, '1d', 'close', 3)
    
    # Get account info
    try:
        account_info = ContextInfo.get_account_info(ContextInfo.accountID)
        balance = getattr(account_info, 'm_dBalance', 0)
        market_value = getattr(account_info, 'm_dMarketValue', 0)
        total_value = balance + market_value
    except:
        print("  [Error] Cannot get account info")
        return
    
    # Get current positions
    try:
        positions = ContextInfo.get_trade_detail_data(ContextInfo.accountID, 'stock', 'position')
        for pos in positions:
            stock = pos.m_strInstrumentID if hasattr(pos, 'm_strInstrumentID') else str(pos)
            volume = pos.m_nVolume if hasattr(pos, 'm_nVolume') else 0
            ContextInfo.holdings[stock] = volume // 100
    except:
        pass
    
    # Execute sells first
    for stock, lots in list(ContextInfo.holdings.items()):
        if lots > 0 and sells.get(stock, 0) == 1:
            if stock in price and price[stock]:
                sell_price = price[stock][-1] if isinstance(price[stock], list) else price[stock]
                sell_amount = lots * 100
                order_shares(stock, -sell_amount, 'fix', sell_price, ContextInfo, ContextInfo.accountID)
    
    # Get buy candidates
    buy_stocks = [k for k, v in buys.items() if v == 1]
    
    # Count current positions
    current_positions = sum(1 for v in ContextInfo.holdings.values() if v > 0)
    available_slots = MAX_STOCKS - current_positions
    
    if available_slots > 0 and buy_stocks:
        buy_stocks = buy_stocks[:available_slots]
        
        # Calculate position size
        position_size = min(MAX_SINGLE_POSITION, 1.0 / MAX_STOCKS)
        money_per_stock = total_value * position_size
        
        for stock in buy_stocks:
            if ContextInfo.holdings.get(stock, 0) == 0:
                if stock in price and price[stock]:
                    buy_price = price[stock][-1] if isinstance(price[stock], list) else price[stock]
                    if buy_price > 0:
                        order_amount = int(money_per_stock / buy_price) // 100 * 100
                        if order_amount >= 100:
                            order_shares(stock, order_amount, 'fix', buy_price, ContextInfo, ContextInfo.accountID)
    
    print(f"  [Done] Rebalance completed")
