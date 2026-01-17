#!/usr/bin/env python3
"""
JQData API 数据抓取测试脚本

测试目的：
1. 验证JQData连接和认证
2. 测试正确的字段名
3. 确认数据能够成功抓取

Author: TRQuant Team
Date: 2025-12-19
"""

import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from datetime import datetime, timedelta

print("=" * 70)
print("JQData API 数据抓取测试")
print("=" * 70)
print()

# ========== Step 1: 连接和认证 ==========
print("📡 Step 1: 连接JQData...")
print("-" * 50)

from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

jq_client = JQDataClient()
cm = get_config_manager()
config = cm.get_jqdata_config()

if not config:
    print("❌ 未找到JQData配置")
    sys.exit(1)

jq_client.authenticate(config['username'], config['password'])

if not jq_client.is_authenticated():
    print("❌ JQData认证失败")
    sys.exit(1)

perm = jq_client.get_permission()
print(f"✅ JQData认证成功")
print(f"   权限范围: {perm.start_date} 至 {perm.end_date}")
print(f"   最新可用日期: {jq_client.get_available_end_date()}")
print()

# 使用权限范围内的日期
test_date = jq_client.get_available_end_date()
test_symbol = "000001.XSHE"  # 平安银行

# ========== Step 2: 测试indicator表 ==========
print("📊 Step 2: 测试indicator表（财务指标）...")
print("-" * 50)

from jqdatasdk import query, indicator, finance, valuation

try:
    # 只查询确定存在的字段
    q = query(
        indicator.code,
        indicator.roe,
        indicator.gross_profit_margin,
        indicator.net_profit_margin,
        indicator.inc_revenue_year_on_year,
        indicator.inc_net_profit_year_on_year,
        indicator.current_ratio,
        indicator.eps,
        indicator.bps
    ).filter(
        indicator.code == test_symbol
    )
    
    df = jq_client.get_fundamentals(q, date=test_date)
    
    if df is not None and not df.empty:
        print(f"✅ indicator表查询成功")
        print(f"   字段: {list(df.columns)}")
        row = df.iloc[0]
        print(f"   ROE: {row.get('roe', 'N/A')}")
        print(f"   毛利率: {row.get('gross_profit_margin', 'N/A')}")
        print(f"   营收增长: {row.get('inc_revenue_year_on_year', 'N/A')}")
    else:
        print("⚠️ indicator表未返回数据")
except Exception as e:
    print(f"❌ indicator表查询失败: {e}")

print()

# ========== Step 3: 测试valuation表 ==========
print("📊 Step 3: 测试valuation表（估值数据）...")
print("-" * 50)

try:
    q_val = query(
        valuation.code,
        valuation.pe_ratio,
        valuation.pb_ratio,
        valuation.market_cap,
        valuation.circulating_market_cap
    ).filter(
        valuation.code == test_symbol
    )
    
    df_val = jq_client.get_fundamentals(q_val, date=test_date)
    
    if df_val is not None and not df_val.empty:
        print(f"✅ valuation表查询成功")
        print(f"   字段: {list(df_val.columns)}")
        row = df_val.iloc[0]
        print(f"   PE: {row.get('pe_ratio', 'N/A')}")
        print(f"   PB: {row.get('pb_ratio', 'N/A')}")
        print(f"   市值: {row.get('market_cap', 'N/A')}")
    else:
        print("⚠️ valuation表未返回数据")
except Exception as e:
    print(f"❌ valuation表查询失败: {e}")

print()

# ========== Step 4: 测试get_price ==========
print("📊 Step 4: 测试get_price（价格数据）...")
print("-" * 50)

try:
    # 使用权限范围内的日期
    end_date = test_date
    start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # 确保开始日期在权限范围内
    if perm.start_date > start_date:
        start_date = perm.start_date
    
    prices = jq_client.get_price(
        test_symbol,
        start_date=start_date,
        end_date=end_date,
        frequency='daily',
        fields=['open', 'close', 'high', 'low', 'volume']
    )
    
    if prices is not None and len(prices) > 0:
        print(f"✅ get_price查询成功")
        print(f"   数据条数: {len(prices)}")
        print(f"   字段: {list(prices.columns)}")
        print(f"   最新收盘价: {prices['close'].iloc[-1]}")
        print(f"   最新成交量: {prices['volume'].iloc[-1]}")
    else:
        print("⚠️ get_price未返回数据")
except Exception as e:
    print(f"❌ get_price查询失败: {e}")

print()

# ========== Step 5: 测试现金流量表（查找正确字段名）==========
print("📊 Step 5: 测试现金流量表...")
print("-" * 50)

# 获取季度日期
current_date = datetime.strptime(test_date, '%Y-%m-%d')
year = current_date.year
quarter = (current_date.month - 1) // 3 + 1
stat_date = f"{year}Q{quarter}"
print(f"   查询季度: {stat_date}")

# 测试不同的字段名
cashflow_fields = [
    ('net_operate_cash_flow', '经营活动现金流'),
    ('net_invest_cash_flow', '投资活动现金流'),
    ('net_finance_cash_flow', '筹资活动现金流'),
]

for field_name, field_desc in cashflow_fields:
    try:
        if hasattr(finance.STK_CASHFLOW_STATEMENT, field_name):
            q_cf = query(
                finance.STK_CASHFLOW_STATEMENT.code,
                getattr(finance.STK_CASHFLOW_STATEMENT, field_name)
            ).filter(
                finance.STK_CASHFLOW_STATEMENT.code == test_symbol
            )
            
            df_cf = jq_client.get_fundamentals(q_cf, statDate=stat_date)
            
            if df_cf is not None and not df_cf.empty:
                value = df_cf.iloc[0].get(field_name, 'N/A')
                print(f"✅ {field_name} ({field_desc}): {value}")
            else:
                print(f"⚠️ {field_name}: 未返回数据")
        else:
            print(f"❌ {field_name}: 字段不存在")
    except Exception as e:
        print(f"❌ {field_name}: {e}")

print()

# ========== Step 6: 测试资产负债表 ==========
print("📊 Step 6: 测试资产负债表...")
print("-" * 50)

balance_fields = [
    ('total_assets', '总资产'),
    ('total_liability', '总负债'),
]

for field_name, field_desc in balance_fields:
    try:
        if hasattr(finance.STK_BALANCE_SHEET, field_name):
            q_bs = query(
                finance.STK_BALANCE_SHEET.code,
                getattr(finance.STK_BALANCE_SHEET, field_name)
            ).filter(
                finance.STK_BALANCE_SHEET.code == test_symbol
            )
            
            df_bs = jq_client.get_fundamentals(q_bs, statDate=stat_date)
            
            if df_bs is not None and not df_bs.empty:
                value = df_bs.iloc[0].get(field_name, 'N/A')
                print(f"✅ {field_name} ({field_desc}): {value}")
            else:
                print(f"⚠️ {field_name}: 未返回数据")
        else:
            print(f"❌ {field_name}: 字段不存在")
    except Exception as e:
        print(f"❌ {field_name}: {e}")

print()

# ========== 总结 ==========
print("=" * 70)
print("📋 测试总结")
print("=" * 70)
print()
print(f"测试日期: {test_date}")
print(f"测试股票: {test_symbol}")
print()
print("可用的数据获取方式:")
print("  1. indicator表: ROE, 毛利率, 营收增长等")
print("  2. valuation表: PE, PB, 市值等")
print("  3. get_price: 价格, 成交量等")
print("  4. STK_CASHFLOW_STATEMENT: 现金流数据")
print("  5. STK_BALANCE_SHEET: 资产负债数据")
print()
print("测试完成!")

