# -*- coding: ascii -*-
# QMT Simple Test Strategy
# Purpose: Test if QMT callbacks are being called

def init(ContextInfo):
    print("=" * 60)
    print("[TEST] init() function called")
    print("=" * 60)
    print("[TEST] If you see this, init() is working")
    print("[TEST] Now waiting for handlebar() to be called...")
    print("=" * 60)


def before_trading_start(ContextInfo):
    print("=" * 60)
    print("[TEST] before_trading_start() function called")
    print("=" * 60)


def handlebar(ContextInfo):
    print("=" * 60)
    print("[TEST] handlebar() function called")
    try:
        if hasattr(ContextInfo, 'current_dt'):
            print(f"[TEST] Current date: {ContextInfo.current_dt}")
        elif hasattr(ContextInfo, 'bartime'):
            print(f"[TEST] Current time: {ContextInfo.bartime}")
        else:
            print("[TEST] Cannot get current date/time")
    except Exception as e:
        print(f"[TEST] Error getting date/time: {e}")
    print("=" * 60)


def after_trading_end(ContextInfo):
    print("=" * 60)
    print("[TEST] after_trading_end() function called")
    print("=" * 60)
