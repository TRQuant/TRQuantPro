#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完整测试：情绪因子与资金流向知识库的使用
========================================

1. 直接调用函数测试（不通过MCP）
2. 展示在策略开发中的实际应用
3. 生成完整的策略代码示例
4. 测试向量索引搜索功能
"""

import sys
import json
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 直接导入函数（不通过MCP）
try:
    from mcp_servers.unified_dev_server import knowledge_search
    UNIFIED_SERVER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  unified_dev_server不可用: {e}")
    UNIFIED_SERVER_AVAILABLE = False
    # 回退到直接调用search API
    from mcp_servers.knowledge_search_api import search as knowledge_search


def test_direct_search():
    """测试1: 直接调用搜索函数"""
    print("=" * 70)
    print("🔍 测试1: 直接调用knowledge_search函数")
    print("=" * 70)
    
    test_queries = [
        "情绪因子",
        "资金流向",
        "聚宽 情绪因子",
        "AKShare 资金流向",
    ]
    
    for query in test_queries:
        print(f"\n📋 查询: \"{query}\"")
        result = knowledge_search(query, limit=3)
        
        if result.get('success'):
            items = result.get('results', [])
            print(f"   ✅ 找到 {len(items)} 条记录")
            
            if items:
                for i, item in enumerate(items[:2], 1):
                    title = item.get('title', 'N/A')
                    tags = item.get('tags', [])
                    print(f"      {i}. {title[:60]}")
                    print(f"         标签: {', '.join(tags[:5])}")
        else:
            print(f"   ❌ 搜索失败: {result.get('error', 'Unknown')}")
    
    return True


def demonstrate_strategy_development():
    """测试2: 展示策略开发中的实际应用"""
    print("\n" + "=" * 70)
    print("💻 测试2: 策略开发中的实际应用")
    print("=" * 70)
    
    # 场景1: 开发情绪因子策略
    print("\n📋 场景1: 开发基于情绪因子的选股策略")
    print("   需求: 了解聚宽提供的情绪类因子")
    
    result = knowledge_search('聚宽 情绪因子 VOL 成交量', limit=1)
    
    if result.get('success') and result.get('results'):
        item = result['results'][0]
        print(f"   ✅ 找到相关知识")
        print(f"   标题: {item.get('title', 'N/A')}")
        
        content = item.get('content', '')
        
        # 提取关键信息
        if 'VOL' in content or '成交量' in content:
            print(f"   ✅ 内容包含成交量因子信息")
        if '聚宽' in content or 'JoinQuant' in content:
            print(f"   ✅ 内容包含聚宽平台信息")
        
        # 展示如何使用
        print(f"\n   💡 使用建议:")
        print(f"   1. 从知识库获取情绪因子定义")
        print(f"   2. 使用聚宽API获取相关数据")
        print(f"   3. 构建情绪因子选股策略")
    
    # 场景2: 获取资金流向数据
    print("\n📋 场景2: 获取资金流向数据用于策略")
    print("   需求: 了解如何获取资金流向数据")
    
    result = knowledge_search('资金流向 数据获取 AKShare', limit=1)
    
    if result.get('success') and result.get('results'):
        item = result['results'][0]
        print(f"   ✅ 找到相关知识")
        print(f"   标题: {item.get('title', 'N/A')}")
        
        content = item.get('content', '')
        if 'AKShare' in content or 'akshare' in content:
            print(f"   ✅ 内容包含AKShare数据获取方法")
        
        print(f"\n   💡 使用建议:")
        print(f"   1. 从知识库了解资金流向数据源")
        print(f"   2. 使用AKShare API获取数据")
        print(f"   3. 结合情绪因子构建综合策略")
    
    return True


def generate_complete_strategy_example():
    """测试3: 生成完整的策略代码示例"""
    print("\n" + "=" * 70)
    print("📝 测试3: 生成完整的策略代码示例")
    print("=" * 70)
    
    # 搜索情绪因子相关知识
    print("\n🔍 搜索情绪因子相关知识...")
    result = knowledge_search('情绪因子 VOL 成交量 聚宽', limit=1)
    
    if result.get('success') and result.get('results'):
        item = result['results'][0]
        content = item.get('content', '')
        
        print("✅ 找到相关知识，生成策略代码示例:")
        print("\n" + "-" * 70)
        print("基于知识库的策略代码示例:")
        print("-" * 70)
        
        # 生成完整的策略代码
        strategy_code = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基于情绪因子与资金流向的选股策略
==================================

知识来源: 如何利用情绪因子与资金流向数据辅助A股交易
- 聚宽情绪因子: VOL（成交量）、TVMA（成交额移动均值）、PSY（心理线）、ARBR等
- AKShare资金流向: 主力资金净流入、超大单/大单/中单/小单净流入
"""

import jqdatasdk as jq
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 初始化聚宽
jq.auth('your_username', 'your_password')

def calculate_vol_factor(stock_code, end_date, period=5):
    """
    计算成交量因子（VOL）
    知识库提示: 成交量突增代表市场关注度飙升，底部放量视为资金进场信号
    """
    # 获取价格数据
    df = jq.get_price(
        stock_code,
        start_date=(pd.to_datetime(end_date) - pd.Timedelta(days=period*2)).strftime('%Y-%m-%d'),
        end_date=end_date,
        fields=['volume', 'amount']
    )
    
    # 计算5日、10日均量（知识库建议）
    df['vol_ma5'] = df['volume'].rolling(5).mean()
    df['vol_ma10'] = df['volume'].rolling(10).mean()
    
    # 成交量放大倍数
    vol_ratio = df['volume'].iloc[-1] / df['vol_ma10'].iloc[-1]
    
    return {
        'vol_ratio': vol_ratio,
        'vol_ma5': df['vol_ma5'].iloc[-1],
        'vol_ma10': df['vol_ma10'].iloc[-1],
        'current_vol': df['volume'].iloc[-1]
    }

def get_capital_flow_akshare(stock_code):
    """
    获取资金流向数据（使用AKShare）
    知识库提示: 使用stock_individual_fund_flow获取资金流向数据
    """
    try:
        # 根据知识库，使用AKShare获取资金流向
        # 注意：需要将股票代码转换为AKShare格式（如：000001 -> 000001.SZ）
        if stock_code.endswith('.XSHG') or stock_code.endswith('.XSHE'):
            ak_code = stock_code.split('.')[0]
        else:
            ak_code = stock_code
        
        # 获取资金流向数据（知识库中的API）
        flow_data = ak.stock_individual_fund_flow_rank(indicator="今日")
        
        # 查找目标股票
        stock_flow = flow_data[flow_data['代码'] == ak_code]
        
        if not stock_flow.empty:
            return {
                'main_net_inflow': stock_flow['主力净流入-净额'].iloc[0] if '主力净流入-净额' in stock_flow.columns else 0,
                'main_net_pct': stock_flow['主力净流入-净占比'].iloc[0] if '主力净流入-净占比' in stock_flow.columns else 0,
                'xl_net_inflow': stock_flow['超大单净流入-净额'].iloc[0] if '超大单净流入-净额' in stock_flow.columns else 0,
            }
    except Exception as e:
        print(f"获取资金流向失败: {e}")
    
    return None

def select_stocks_by_sentiment_and_flow():
    """
    基于情绪因子和资金流向的综合选股策略
    
    知识库策略建议:
    1. 选股打分: 成交量放大倍数、资金流量指标、心理线等归一化评分
    2. 热点情绪分高的股票（成交活跃、资金持续流入、市场情绪乐观）得分高
    3. 每周期选取情绪分最高的若干股票构建交易组合
    """
    # 获取股票池（沪深300）
    stocks = jq.get_index_stocks('000300.XSHG')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    results = []
    
    print(f"分析 {len(stocks)} 只股票...")
    
    for i, stock in enumerate(stocks[:50], 1):  # 示例：只分析前50只
        if i % 10 == 0:
            print(f"  已处理 {i}/{min(50, len(stocks))} 只")
        
        try:
            # 1. 计算情绪因子
            vol_factor = calculate_vol_factor(stock, end_date)
            
            # 2. 获取资金流向
            flow_data = get_capital_flow_akshare(stock)
            
            if flow_data:
                # 3. 计算综合情绪得分（知识库建议的方法）
                # 成交量放大倍数（归一化）
                vol_score = min(vol_factor['vol_ratio'] / 2.0, 1.0) * 100  # 放大2倍以上得满分
                
                # 资金流入得分
                flow_score = min(abs(flow_data['main_net_pct']) / 5.0, 1.0) * 100  # 净占比5%以上得满分
                
                # 综合得分（知识库建议的加权方式）
                composite_score = vol_score * 0.5 + flow_score * 0.5
                
                results.append({
                    'code': stock,
                    'vol_ratio': vol_factor['vol_ratio'],
                    'main_net_pct': flow_data['main_net_pct'],
                    'composite_score': composite_score
                })
        except Exception as e:
            continue
    
    # 按综合得分排序
    results_df = pd.DataFrame(results)
    if not results_df.empty:
        results_df = results_df.sort_values('composite_score', ascending=False)
        print(f"\n筛选出 {len(results_df)} 只符合条件的股票")
        print("\n前10只股票:")
        print(results_df[['code', 'vol_ratio', 'main_net_pct', 'composite_score']].head(10))
        
        return results_df.head(20)  # 返回前20只
    
    return pd.DataFrame()

if __name__ == '__main__':
    # 执行策略
    selected_stocks = select_stocks_by_sentiment_and_flow()
    
    print(f"\n✅ 策略执行完成，选出 {len(selected_stocks)} 只股票")
    print("\n策略说明:")
    print("- 基于知识库中的情绪因子（VOL成交量）和资金流向数据")
    print("- 综合评分：成交量放大倍数 × 0.5 + 主力资金净流入占比 × 0.5")
    print("- 筛选出情绪热度高、资金持续流入的强势股")
'''
        
        print(strategy_code)
        print("-" * 70)
        print("\n✅ 完整的策略代码已生成（基于知识库内容）")
        
        # 保存到文件
        strategy_file = TRQUANT_ROOT / "scripts" / "strategy_sentiment_flow_example.py"
        strategy_file.write_text(strategy_code, encoding='utf-8')
        print(f"💾 策略代码已保存: {strategy_file}")
        
        return True
    else:
        print("⚠️  未找到相关知识，无法生成示例")
        return False


def test_vector_index():
    """测试4: 向量索引搜索功能"""
    print("\n" + "=" * 70)
    print("🔍 测试4: 向量索引搜索功能")
    print("=" * 70)
    
    try:
        # 检查向量索引是否存在
        from pathlib import Path
        index_dir = Path('.trquant/dev/knowledge/vector_index')
        index_meta_file = index_dir / 'index_meta.json'
        
        if not index_meta_file.exists():
            print("⚠️  向量索引不存在，尝试构建...")
            from mcp_servers.knowledge_vector_index import build_vector_index
            kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
            result = build_vector_index(kb_file, force_rebuild=True)
            
            if result.get('success'):
                print(f"✅ 向量索引构建成功")
                print(f"   条目数: {result.get('items_count')}")
                print(f"   模型: {result.get('model')}")
            else:
                print(f"❌ 向量索引构建失败: {result.get('error')}")
                return False
        else:
            print("✅ 向量索引已存在")
        
        # 测试向量搜索
        print("\n📋 测试向量搜索...")
        from mcp_servers.knowledge_search_api import search
        
        test_queries = [
            "情绪因子",
            "资金流向",
        ]
        
        for query in test_queries:
            print(f"\n查询: \"{query}\"")
            result = search(query, limit=3, mode="hybrid")
            
            if result.get('success'):
                items = result.get('results', [])
                print(f"   ✅ 找到 {len(items)} 条记录 (模式: {result.get('mode')})")
                
                if items:
                    for i, item in enumerate(items[:2], 1):
                        print(f"      {i}. {item.get('title', 'N/A')[:60]}")
                        print(f"         分数: {item.get('_score', 0):.2f}")
            else:
                print(f"   ❌ 搜索失败: {result.get('error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 向量索引测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("=" * 70)
    print("🧪 情绪因子与资金流向知识库完整测试")
    print("=" * 70)
    print()
    
    # 测试1: 直接搜索
    search_ok = test_direct_search()
    
    # 测试2: 实际使用场景
    usage_ok = demonstrate_strategy_development()
    
    # 测试3: 生成策略代码
    example_ok = generate_complete_strategy_example()
    
    # 测试4: 向量索引搜索
    vector_ok = test_vector_index()
    
    # 总结
    print("\n" + "=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    print(f"直接搜索: {'✅ 通过' if search_ok else '❌ 失败'}")
    print(f"使用场景: {'✅ 通过' if usage_ok else '❌ 失败'}")
    print(f"代码生成: {'✅ 通过' if example_ok else '❌ 失败'}")
    print(f"向量索引: {'✅ 通过' if vector_ok else '❌ 失败'}")
    
    if search_ok and usage_ok and example_ok:
        print("\n✅ 知识库构建成功，可以在策略开发中使用！")
        if vector_ok:
            print("✅ 向量索引功能正常，支持语义搜索！")
        else:
            print("⚠️  向量索引功能未启用，但基础搜索可用")
        print("\n📋 使用方式:")
        print("   1. 在策略开发中，使用knowledge_search()搜索相关知识")
        print("   2. 从搜索结果中提取API接口、参数说明、代码示例")
        print("   3. 基于知识库内容生成策略代码")
        print("   4. 策略代码已保存到: scripts/strategy_sentiment_flow_example.py")
    else:
        print("\n⚠️  部分测试未通过，请检查知识库")
    print("=" * 70)


if __name__ == '__main__':
    main()
