#!/usr/bin/env python3
"""
测试AKShare获取个股最近3个月股价
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_akshare_price():
    """测试AKShare获取股价"""
    print("=" * 60)
    print("🧪 AKShare API 股价数据测试")
    print("=" * 60)
    
    try:
        import akshare as ak
        print("\n1️⃣ AKShare导入成功")
    except ImportError:
        print("\n❌ AKShare未安装，请运行: pip install akshare")
        return False
    
    # 测试股票列表（使用AKShare格式）
    test_stocks = [
        {"code": "000001", "name": "平安银行", "market": "sz"},  # 深交所
        {"code": "600000", "name": "浦发银行", "market": "sh"},  # 上交所
        {"code": "000002", "name": "万科A", "market": "sz"},
    ]
    
    # 计算日期范围（最近3个月）
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
    
    print(f"\n2️⃣ 测试获取最近3个月股价数据")
    print(f"   日期范围: {start_date} 至 {end_date}")
    print(f"   测试股票: {len(test_stocks)}只")
    
    results = {}
    
    for stock in test_stocks:
        symbol = f"{stock['code']}.X{stock['market'].upper()}E" if stock['market'] == 'sz' else f"{stock['code']}.XSHG"
        print(f"\n   📊 测试 {stock['name']} ({stock['code']})...")
        
        try:
            # 方法1: 使用stock_zh_a_hist（A股历史数据）
            print(f"      尝试方法1: stock_zh_a_hist...")
            df = ak.stock_zh_a_hist(
                symbol=stock['code'],
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"  # 前复权
            )
            
            if df is not None and len(df) > 0:
                print(f"      ✅ 成功获取 {len(df)} 条数据")
                print(f"      日期范围: {df['日期'].iloc[0]} 至 {df['日期'].iloc[-1]}")
                print(f"      最新收盘价: {df['收盘'].iloc[-1]:.2f}")
                print(f"      最高价: {df['最高'].max():.2f}")
                print(f"      最低价: {df['最低'].min():.2f}")
                print(f"      平均成交量: {df['成交量'].mean():.0f}")
                
                results[symbol] = {
                    'success': True,
                    'method': 'stock_zh_a_hist',
                    'count': len(df),
                    'latest_price': float(df['收盘'].iloc[-1]),
                    'date_range': f"{df['日期'].iloc[0]} 至 {df['日期'].iloc[-1]}"
                }
            else:
                print(f"      ⚠️ 方法1未获取到数据，尝试方法2...")
                
                # 方法2: 使用stock_zh_a_hist_min_em（分钟数据，但可以获取日线）
                try:
                    import time
                    time.sleep(1)  # 避免请求过快
                    
                    # 获取最近90天的数据
                    df2 = ak.stock_zh_a_hist_min_em(
                        symbol=stock['code'],
                        start_date=start_date,
                        end_date=end_date,
                        period="daily",
                        adjust="qfq"
                    )
                    
                    if df2 is not None and len(df2) > 0:
                        print(f"      ✅ 方法2成功获取 {len(df2)} 条数据")
                        results[symbol] = {
                            'success': True,
                            'method': 'stock_zh_a_hist_min_em',
                            'count': len(df2),
                            'latest_price': float(df2['收盘'].iloc[-1]) if '收盘' in df2.columns else float(df2.iloc[-1, 1])
                        }
                    else:
                        raise Exception("方法2也无数据")
                        
                except Exception as e2:
                    print(f"      ❌ 方法2也失败: {e2}")
                    results[symbol] = {'success': False, 'error': str(e2)}
                    
        except Exception as e:
            print(f"      ❌ 获取失败: {e}")
            results[symbol] = {'success': False, 'error': str(e)}
    
    # 测试实时价格
    print(f"\n3️⃣ 测试获取实时价格...")
    try:
        # 使用stock_zh_a_spot_em获取实时行情
        print("   使用stock_zh_a_spot_em获取实时行情...")
        df_realtime = ak.stock_zh_a_spot_em()
        
        if df_realtime is not None and len(df_realtime) > 0:
            print(f"   ✅ 成功获取 {len(df_realtime)} 只股票的实时行情")
            
            # 查找测试股票
            for stock in test_stocks:
                code = stock['code']
                matched = df_realtime[df_realtime['代码'] == code]
                if len(matched) > 0:
                    row = matched.iloc[0]
                    print(f"   {stock['name']} ({code}): {row.get('最新价', 'N/A')} 元")
                    if stock['code'] + '.XSHE' in results or stock['code'] + '.XSHG' in results:
                        symbol = stock['code'] + '.XSHE' if stock['market'] == 'sz' else stock['code'] + '.XSHG'
                        if symbol in results:
                            results[symbol]['realtime_price'] = float(row.get('最新价', 0))
        else:
            print("   ⚠️ 未获取到实时行情数据")
    except Exception as e:
        print(f"   ⚠️ 实时价格获取失败: {e}")
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    success_count = sum(1 for r in results.values() if r.get('success'))
    print(f"   成功: {success_count}/{len(test_stocks)}")
    
    for symbol, result in results.items():
        if result.get('success'):
            method = result.get('method', 'unknown')
            print(f"   ✅ {symbol}: {result['count']}条数据, 最新价{result['latest_price']:.2f} (方法: {method})")
            if 'realtime_price' in result:
                print(f"      实时价格: {result['realtime_price']:.2f}")
        else:
            print(f"   ❌ {symbol}: {result.get('error', '未知错误')}")
    
    return success_count > 0

if __name__ == '__main__':
    success = test_akshare_price()
    sys.exit(0 if success else 1)

