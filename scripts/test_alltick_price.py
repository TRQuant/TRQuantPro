#!/usr/bin/env python3
"""
测试AllTick API获取个股最近3个月股价
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_sources.alltick_source import AllTickSource

def test_alltick_price():
    """测试AllTick获取股价"""
    print("=" * 60)
    print("🧪 AllTick API 股价数据测试")
    print("=" * 60)
    
    # 初始化AllTick
    print("\n1️⃣ 初始化AllTick数据源...")
    alltick = AllTickSource()
    
    # 连接
    print("2️⃣ 连接AllTick API...")
    if not alltick.connect():
        print("   ❌ AllTick连接失败")
        return False
    print("   ✅ AllTick连接成功")
    
    # 测试单个股票（减少请求频率）
    test_symbols = [
        "000001.XSHE",  # 平安银行
    ]
    
    # 计算日期范围（最近3个月，但只获取少量数据测试）
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    import time
    
    print(f"\n3️⃣ 测试获取最近3个月股价数据")
    print(f"   日期范围: {start_date} 至 {end_date}")
    print(f"   测试股票: {', '.join(test_symbols)}")
    
    results = {}
    
    for symbol in test_symbols:
        print(f"\n   📊 测试 {symbol}...")
        
        try:
            # 先测试获取少量数据（避免429错误）
            print(f"      尝试获取最近10条K线数据...")
            df = alltick.get_price(symbol, count=10, frequency='daily')
            
            # 如果成功，再尝试获取更多
            if df is not None and len(df) > 0:
                print(f"      ✅ 成功获取{len(df)}条数据，继续获取更多...")
                time.sleep(1)  # 添加延迟避免频率限制
                
                # 尝试获取更多数据
                df_more = alltick.get_historical_prices(
                    symbol,
                    start_date=start_date,
                    end_date=end_date,
                    frequency='daily'
                )
                if df_more is not None and len(df_more) > 0:
                    df = df_more
            
            if df is not None and len(df) > 0:
                print(f"      ✅ 成功获取 {len(df)} 条数据")
                print(f"      日期范围: {df.index[0].strftime('%Y-%m-%d')} 至 {df.index[-1].strftime('%Y-%m-%d')}")
                print(f"      最新价格: {df['close'].iloc[-1]:.2f}")
                print(f"      最高价: {df['high'].max():.2f}")
                print(f"      最低价: {df['low'].min():.2f}")
                print(f"      平均成交量: {df['volume'].mean():.0f}")
                
                results[symbol] = {
                    'success': True,
                    'count': len(df),
                    'latest_price': float(df['close'].iloc[-1]),
                    'date_range': f"{df.index[0].strftime('%Y-%m-%d')} 至 {df.index[-1].strftime('%Y-%m-%d')}"
                }
            else:
                print(f"      ⚠️ 未获取到数据")
                results[symbol] = {'success': False, 'error': '无数据'}
                
        except Exception as e:
            print(f"      ❌ 获取失败: {e}")
            results[symbol] = {'success': False, 'error': str(e)}
    
    # 测试实时价格
    print(f"\n4️⃣ 测试获取实时价格...")
    for symbol in test_symbols:
        try:
            price_info = alltick.get_realtime_price(symbol)
            if price_info:
                print(f"   {symbol}: {price_info['price']:.2f} (来源: AllTick实时)")
                results[symbol]['realtime_price'] = price_info['price']
            else:
                print(f"   {symbol}: 无法获取实时价格")
        except Exception as e:
            print(f"   {symbol}: 实时价格获取失败 - {e}")
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    success_count = sum(1 for r in results.values() if r.get('success'))
    print(f"   成功: {success_count}/{len(test_symbols)}")
    
    for symbol, result in results.items():
        if result.get('success'):
            print(f"   ✅ {symbol}: {result['count']}条数据, 最新价{result['latest_price']:.2f}")
        else:
            print(f"   ❌ {symbol}: {result.get('error', '未知错误')}")
    
    return success_count > 0

if __name__ == '__main__':
    success = test_alltick_price()
    sys.exit(0 if success else 1)

