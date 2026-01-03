#!/usr/bin/env python3
"""
十倍股V3系统调试测试

直接测试V3优化后的漏斗和评分逻辑
"""

import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

print("=" * 70)
print("十倍股V3系统调试测试")
print("=" * 70)
print()

# 1. 连接数据源
print("📡 Step 1: 连接数据源...")
from jqdata.client import JQDataClient
from config.config_manager import get_config_manager
from jqdatasdk import auth, is_auth

jq_client = JQDataClient()
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq_client.authenticate(jq_config['username'], jq_config['password'])

if jq_client.is_authenticated():
    print("  ✅ JQData已连接")
else:
    print("  ❌ JQData未连接")
    sys.exit(1)
print()

# 2. 获取测试股票数据
print("📊 Step 2: 获取测试股票数据...")
from mcp_servers.utils.tenbagger_v2.data_fetcher import TenbaggerDataFetcher

fetcher = TenbaggerDataFetcher(jq_client=jq_client)

# 测试股票
test_symbols = [
    ("000063.XSHE", "中兴通讯"),
    ("300124.XSHE", "汇川技术"),
    ("000858.XSHE", "五粮液"),
]

test_data = {}
for symbol, name in test_symbols:
    data = fetcher.fetch_complete_data(symbol)
    test_data[symbol] = {"name": name, "data": data}
    print(f"  {symbol} {name}:")
    print(f"    营收增速: {data.get('revenue_growth', 0):.1f}%")
    print(f"    利润增速: {data.get('profit_growth', 0):.1f}%")
    print(f"    毛利率: {data.get('gross_margin', 0):.1f}%")
    print(f"    ROE: {data.get('roe', 0):.2f}%")
    print(f"    市值: {data.get('market_cap', 0):.1f}亿")
    print(f"    avg_turnover: {data.get('avg_turnover', 'N/A')}")
    print(f"    turnover_ratio: {data.get('turnover_ratio', 'N/A')}")
print()

# 3. 测试L0过滤
print("🔍 Step 3: 测试L0过滤...")
from mcp_servers.utils.tenbagger_v2.candidate_funnel import CandidateFunnel, FunnelLevel

# 创建新的漏斗实例
funnel = CandidateFunnel()

# 显示L0配置
print("  L0过滤配置:")
for filter_id, config in funnel.L0_HARD_FILTERS.items():
    print(f"    {filter_id}: {config['name']}")
print()

for symbol, info in test_data.items():
    data = info["data"]
    name = info["name"]
    
    l0_passed, passed, failed = funnel.filter_l0(symbol, data)
    status = "✅" if l0_passed else "❌"
    print(f"  {symbol} {name}: {status}")
    if failed:
        print(f"    失败原因: {failed}")
print()

# 4. 测试L1评分
print("📈 Step 4: 测试L1评分...")
print("  L1信号配置 (V3):")
for sig_id, config in funnel.L1_EARLY_SIGNALS.items():
    print(f"    {sig_id}: {config['name']} (weight={config['weight']})")
print()

for symbol, info in test_data.items():
    data = info["data"]
    name = info["name"]
    
    l1_score, l1_scores = funnel.score_l1(symbol, data)
    print(f"  {symbol} {name}: 总分={l1_score:.1f}")
    for sig_name, score in l1_scores.items():
        print(f"    {sig_name}: {score:.1f}")
    print()

# 5. 完整漏斗评估
print("🏆 Step 5: 完整漏斗评估...")
for symbol, info in test_data.items():
    data = info["data"]
    name = info["name"]
    
    result = funnel.evaluate(symbol, name, data)
    
    level_emoji = {
        FunnelLevel.L2_TENBAGGER: "🌟",
        FunnelLevel.L1_EARLY: "⭐",
        FunnelLevel.L0_UNIVERSE: "📊",
        FunnelLevel.REJECTED: "❌"
    }
    
    print(f"  {symbol} {name}: {level_emoji.get(result.level, '?')} {result.level.value}")
    if result.failed_filters:
        print(f"    失败: {result.failed_filters}")
    if result.scores:
        print(f"    评分: L1={result.scores.get('L1总分', 'N/A'):.1f}")
print()

# 6. 统计
print("📊 统计:")
stats = funnel.get_stats()
print(f"  L0通过: {stats['l0_passed']}/{stats['l0_input']}")
print(f"  L1通过: {stats['l1_passed']}")
print(f"  L2通过: {stats['l2_passed']}")
print(f"  拒绝: {stats['rejected']}")
print()

print("测试完成!")

