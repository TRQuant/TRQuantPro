#!/usr/bin/env python3
"""JQData Query 调用示例测试脚本"""

import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from jqdatasdk import query, valuation, indicator, get_fundamentals
from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

def main():
    print("=" * 70)
    print("JQData Query 调用示例测试")
    print("=" * 70)
    print()
    
    # 认证
    jq_client = JQDataClient()
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    jq_client.authenticate(jq_config['username'], jq_config['password'])
    
    test_date = jq_client.get_available_end_date()
    test_symbol = "000001.XSHE"
    
    print(f"测试日期: {test_date}")
    print(f"测试股票: {test_symbol}")
    print()
    
    # 示例1: 基本查询
    print("📝 示例1: 基本查询")
    try:
        q = query(valuation).filter(valuation.code == test_symbol)
        df = get_fundamentals(q, date=test_date)
        if df is not None and not df.empty:
            print(f"   ✅ 成功: 返回 {len(df)} 行数据")
            print(f"   字段: {list(df.columns)[:5]}...")
        else:
            print("   ⚠️ 未返回数据")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print()
    
    # 示例2: 指定字段查询
    print("📝 示例2: 指定字段查询")
    try:
        q = query(
            valuation.code,
            valuation.pe_ratio,
            valuation.pb_ratio,
            valuation.market_cap
        ).filter(valuation.code == test_symbol)
        df = get_fundamentals(q, date=test_date)
        if df is not None and not df.empty:
            print(f"   ✅ 成功: 返回字段 {list(df.columns)}")
            row = df.iloc[0]
            print(f"   PE: {row.get('pe_ratio')}, PB: {row.get('pb_ratio')}")
        else:
            print("   ⚠️ 未返回数据")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print()
    
    # 示例3: 组合表查询
    print("📝 示例3: 组合估值和财务指标")
    try:
        q = query(
            valuation.code,
            valuation.pe_ratio,
            indicator.roe,
            indicator.gross_profit_margin
        ).filter(
            valuation.code == indicator.code,
            valuation.code == test_symbol
        )
        df = get_fundamentals(q, date=test_date)
        if df is not None and not df.empty:
            print(f"   ✅ 成功: 返回字段 {list(df.columns)}")
        else:
            print("   ⚠️ 未返回数据")
    except Exception as e:
        print(f"   ❌ 失败: {e}")
    
    print()
    print("=" * 70)
    print("✅ 测试完成")
    print("=" * 70)

if __name__ == "__main__":
    main()
