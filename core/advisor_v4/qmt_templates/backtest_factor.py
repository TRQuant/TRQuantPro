#coding:gbk
"""
QMT Multi-Factor Backtest Template
==================================

A comprehensive template for factor-based stock selection in QMT.

Features:
- 7-factor stock selection (momentum, relative position, etc.)
- Factor scoring system
- Configurable thresholds
- Risk control (stop-loss/take-profit)

Template Parameters (customize below):
- FACTOR_WEIGHTS: Factor importance weights
- SELECTION_THRESHOLDS: Factor selection criteria
- RISK_PARAMS: Stop-loss and take-profit settings
"""
import numpy as np
from datetime import datetime

# ==================== Template Parameters ====================
# Rebalance settings
REBALANCE_PERIOD = 20
MAX_STOCKS = 10
WARMUP_BARS = 60
COMMISSION_RATE = 0.0003

# Factor weights (sum to 1.0)
FACTOR_WEIGHTS = {
    'momentum_20d': 0.20,
    'rel_position': 0.18,
    'momentum_5d': 0.15,
    'turnover_rate': 0.14,
    'market_cap': 0.17,
    'roe': 0.10,
    'growth': 0.06,
}

# Selection thresholds
MIN_TOTAL_SCORE = 20.0

# Risk parameters
STOP_LOSS = -0.08       # -8% stop loss
TAKE_PROFIT = 0.30      # 30% take profit


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


# ==================== Factor Calculation ====================
def calculate_factor_score(ContextInfo, stock, d):
    """
    Calculate factor score for a stock
    
    Returns:
        float: Score between 0-100, or None if calculation fails
    """
    try:
        # Get historical data
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
        
        # Calculate factors
        factors = {}
        
        # 1. 20-day momentum
        if len(close) >= 20:
            factors['momentum_20d'] = (close[-1] - close[-20]) / close[-20] * 100 if close[-20] > 0 else 0
        else:
            factors['momentum_20d'] = 0
        
        # 2. 5-day momentum
        if len(close) >= 5:
            factors['momentum_5d'] = (close[-1] - close[-5]) / close[-5] * 100 if close[-5] > 0 else 0
        else:
            factors['momentum_5d'] = 0
        
        # 3. Relative position
        if len(high) >= 20 and len(low) >= 20:
            high_20 = max(high[-20:])
            low_20 = min(low[-20:])
            if high_20 > low_20:
                factors['rel_position'] = (close[-1] - low_20) / (high_20 - low_20) * 100
            else:
                factors['rel_position'] = 50
        else:
            factors['rel_position'] = 50
        
        # 4. Turnover rate (simplified)
        if len(volume) >= 5:
            avg_volume = sum(volume[-5:]) / 5
            factors['turnover_rate'] = avg_volume / 1000000 * 5
        else:
            factors['turnover_rate'] = 3
        
        # 5-7. Simplified factors (use defaults for backtest)
        factors['market_cap'] = 100
        factors['roe'] = 10
        factors['growth'] = 5
        
        # Calculate scores
        score = 0.0
        
        # Momentum 20d score (5%~30% optimal)
        m20 = factors['momentum_20d']
        if 5 <= m20 <= 30:
            m20_score = 1.0 - abs(m20 - 17.5) / 12.5
        else:
            m20_score = max(0, 1.0 - abs(m20 - 17.5) / 25.0)
        score += m20_score * FACTOR_WEIGHTS['momentum_20d']
        
        # Relative position score (50%~80% optimal)
        rp = factors['rel_position']
        if 50 <= rp <= 80:
            rp_score = 1.0
        else:
            rp_score = max(0, 1.0 - abs(rp - 65) / 50.0)
        score += rp_score * FACTOR_WEIGHTS['rel_position']
        
        # Momentum 5d score (-2%~5% optimal)
        m5 = factors['momentum_5d']
        if -2 <= m5 <= 5:
            m5_score = 1.0 - abs(m5 - 1.5) / 3.5
        else:
            m5_score = max(0, 1.0 - abs(m5 - 1.5) / 10.0)
        score += m5_score * FACTOR_WEIGHTS['momentum_5d']
        
        # Turnover rate score (2%~8% optimal)
        tr = factors['turnover_rate']
        if 2 <= tr <= 8:
            tr_score = 1.0 - abs(tr - 5) / 3.0
        else:
            tr_score = max(0, 1.0 - abs(tr - 5) / 10.0)
        score += tr_score * FACTOR_WEIGHTS['turnover_rate']
        
        # Add default scores for simplified factors
        score += 0.5 * (FACTOR_WEIGHTS['market_cap'] + FACTOR_WEIGHTS['roe'] + FACTOR_WEIGHTS['growth'])
        
        return score * 100
        
    except Exception as e:
        return None


def select_stocks(ContextInfo, d):
    """
    Select stocks based on factor scores
    
    Returns:
        list: Selected stock codes sorted by score
    """
    scores = {}
    
    for stock in ContextInfo.s:
        score = calculate_factor_score(ContextInfo, stock, d)
        if score is not None and score >= MIN_TOTAL_SCORE:
            scores[stock] = score
    
    # Sort by score and return top N
    sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [s[0] for s in sorted_stocks[:MAX_STOCKS]], dict(sorted_stocks[:MAX_STOCKS])


# ==================== Risk Control ====================
def check_risk(ContextInfo, price):
    """Check stop-loss and take-profit"""
    positions_to_close = []
    
    for stock, lots in ContextInfo.holdings.items():
        if lots > 0 and stock in ContextInfo.buypoint:
            entry_price = ContextInfo.buypoint[stock]
            if stock in price and price[stock]:
                current_price = price[stock][-1] if isinstance(price[stock], list) else price[stock]
                
                pnl = (current_price - entry_price) / entry_price
                
                if pnl <= STOP_LOSS:
                    print(f"  [Stop-Loss] {stock}: {pnl*100:.1f}%")
                    positions_to_close.append((stock, current_price, 'stop_loss'))
                elif pnl >= TAKE_PROFIT:
                    print(f"  [Take-Profit] {stock}: {pnl*100:.1f}%")
                    positions_to_close.append((stock, current_price, 'take_profit'))
    
    return positions_to_close


# ==================== Main Functions ====================
def init(ContextInfo):
    """Strategy initialization"""
    ContextInfo.s = ContextInfo.get_sector('000300.SH')
    ContextInfo.set_universe(ContextInfo.s)
    
    ContextInfo.holdings = {i: 0 for i in ContextInfo.s}
    ContextInfo.weight = [1.0 / MAX_STOCKS] * MAX_STOCKS
    ContextInfo.buypoint = {}
    ContextInfo.money = ContextInfo.capital
    ContextInfo.profit = 0
    ContextInfo.accountID = 'testS'
    
    print("=" * 60)
    print("QMT Multi-Factor Backtest Template")
    print("=" * 60)
    print(f"Universe: HS300 ({len(ContextInfo.s)} stocks)")
    print(f"Capital: {ContextInfo.capital:.2f}")
    print(f"Max Positions: {MAX_STOCKS}")
    print(f"Rebalance Period: {REBALANCE_PERIOD} days")
    print(f"Min Score: {MIN_TOTAL_SCORE}")
    print(f"Stop-Loss: {STOP_LOSS*100:.0f}%")
    print(f"Take-Profit: {TAKE_PROFIT*100:.0f}%")
    print("=" * 60)


def handlebar(ContextInfo):
    """Main strategy logic"""
    d = ContextInfo.barpos
    price = ContextInfo.get_history_data(1, '1d', 'open', 3)
    
    # Check risk control every day
    if d > WARMUP_BARS:
        close_positions = check_risk(ContextInfo, price)
        for stock, close_price, reason in close_positions:
            sell_amount = ContextInfo.holdings[stock] * 100
            order_shares(stock, -sell_amount, 'fix', close_price, ContextInfo, ContextInfo.accountID)
            
            fee = close_price * sell_amount * COMMISSION_RATE
            ContextInfo.money += close_price * sell_amount - fee
            ContextInfo.holdings[stock] = 0
    
    # Rebalance on schedule
    if d > WARMUP_BARS and d % REBALANCE_PERIOD == 0:
        nowDate = timetag_to_datetime(ContextInfo.get_bar_timetag(d))
        print(f"\n[Bar {d}] {nowDate.strftime('%Y-%m-%d')} - Rebalancing")
        
        # Select stocks by factor score
        selected_stocks, scores = select_stocks(ContextInfo, d)
        
        if selected_stocks:
            print(f"Selected {len(selected_stocks)} stocks:")
            for stock in selected_stocks[:5]:
                print(f"  {stock}: score={scores[stock]:.1f}")
            
            # Sell positions not in selection
            for stock in ContextInfo.s:
                if ContextInfo.holdings[stock] > 0 and stock not in selected_stocks:
                    if stock in price and price[stock]:
                        sell_price = price[stock][-1] if isinstance(price[stock], list) else price[stock]
                        sell_amount = ContextInfo.holdings[stock] * 100
                        
                        order_shares(stock, -sell_amount, 'fix', sell_price, ContextInfo, ContextInfo.accountID)
                        
                        fee = sell_price * sell_amount * COMMISSION_RATE
                        ContextInfo.money += sell_price * sell_amount - fee
                        ContextInfo.holdings[stock] = 0
            
            # Buy selected stocks
            money_per_stock = {k: w * ContextInfo.money for k, w in zip(selected_stocks, ContextInfo.weight[:len(selected_stocks)])}
            
            for stock in selected_stocks:
                if ContextInfo.holdings[stock] == 0:
                    if stock in price and price[stock]:
                        buy_price = price[stock][-1] if isinstance(price[stock], list) else price[stock]
                        if buy_price > 0:
                            order_amount = int(money_per_stock[stock] / buy_price) // 100
                            
                            if order_amount > 0:
                                order_shares(stock, order_amount * 100, 'fix', buy_price, ContextInfo, ContextInfo.accountID)
                                
                                ContextInfo.buypoint[stock] = buy_price
                                fee = buy_price * order_amount * 100 * COMMISSION_RATE
                                ContextInfo.money -= buy_price * order_amount * 100 + fee
                                ContextInfo.holdings[stock] = order_amount
            
            print(f"[Summary] Cash: {ContextInfo.money:.2f}, Profit: {ContextInfo.profit:.2f}")
    
    # Track profit ratio
    profit_ratio = ContextInfo.profit / ContextInfo.capital if ContextInfo.capital > 0 else 0
    if not ContextInfo.do_back_test:
        ContextInfo.paint('profit_ratio', profit_ratio, -1, 0)
