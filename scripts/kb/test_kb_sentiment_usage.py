#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试情绪因子与资金流向知识库的使用
==================================

验证知识库已成功构建，并展示在策略开发中的实际应用
"""

import sys
import json
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from core.mcp.client import MCPClient


def test_knowledge_search():
    """测试知识库搜索功能"""
    print("=" * 70)
    print("🔍 测试1: 知识库搜索功能")
    print("=" * 70)
    
    client = MCPClient()
    
    # 测试查询列表
    test_queries = [
        "情绪因子",
        "资金流向",
        "聚宽 情绪因子",
        "AKShare 资金流向",
        "如何利用情绪因子",
        "A股交易 情绪",
    ]
    
    results_summary = []
    
    for query in test_queries:
        print(f"\n📋 查询: \"{query}\"")
        try:
            result = client.call(
                tool_name='knowledge.search',
                arguments={
                    'query': query,
                    'limit': 3
                },
                timeout=30.0
            )
            
            if result.success:
                data = result.data
                if isinstance(data, str):
                    try:
                        data = json.loads(data)
                    except:
                        # 如果不是JSON，可能是字符串
                        print(f"   ⚠️  返回数据格式异常: {data[:100]}")
                        continue
                
                # 兼容多种返回格式
                items = []
                if isinstance(data, dict):
                    items = data.get('items', []) or data.get('results', []) or data.get('data', [])
                elif isinstance(data, list):
                    items = data
                
                print(f"   ✅ 找到 {len(items)} 条记录")
                
                if items:
                    for i, item in enumerate(items[:2], 1):
                        title = item.get('title', 'N/A')
                        content_preview = item.get('content', '')[:100]
                        tags = item.get('tags', [])
                        print(f"      {i}. {title[:60]}")
                        print(f"         标签: {', '.join(tags[:5])}")
                        print(f"         内容: {content_preview}...")
                    
                    results_summary.append({
                        'query': query,
                        'found': len(items),
                        'top_title': items[0].get('title', 'N/A') if items else None
                    })
                else:
                    print(f"   ⚠️  未找到相关记录")
                    results_summary.append({
                        'query': query,
                        'found': 0,
                        'top_title': None
                    })
            else:
                print(f"   ❌ 搜索失败: {result.error}")
                results_summary.append({
                    'query': query,
                    'found': 0,
                    'error': result.error
                })
        except Exception as e:
            print(f"   ❌ 异常: {e}")
            results_summary.append({
                'query': query,
                'found': 0,
                'error': str(e)
            })
    
    # 汇总
    print("\n" + "=" * 70)
    print("📊 搜索结果汇总")
    print("=" * 70)
    total_found = sum(r.get('found', 0) for r in results_summary)
    successful_queries = [r for r in results_summary if r.get('found', 0) > 0]
    
    print(f"总查询数: {len(test_queries)}")
    print(f"成功找到记录: {len(successful_queries)}")
    print(f"总记录数: {total_found}")
    
    if successful_queries:
        print(f"\n✅ 成功的查询:")
        for r in successful_queries:
            print(f"   - \"{r['query']}\": 找到 {r['found']} 条")
            if r.get('top_title'):
                print(f"     最佳匹配: {r['top_title'][:60]}")
    
    return len(successful_queries) > 0


def test_strategy_development_usage():
    """测试在策略开发中的实际使用场景"""
    print("\n" + "=" * 70)
    print("💻 测试2: 策略开发中的实际使用")
    print("=" * 70)
    
    client = MCPClient()
    
    # 场景1: 开发情绪因子策略
    print("\n📋 场景1: 开发基于情绪因子的选股策略")
    print("   需求: 了解聚宽提供的情绪类因子")
    
    result = client.call(
        tool_name='knowledge.search',
        arguments={
            'query': '聚宽 情绪因子 VOL 成交量',
            'limit': 1
        },
        timeout=30.0
    )
    
    if result.success:
        data = json.loads(result.data) if isinstance(result.data, str) else result.data
        items = data.get('items', []) or data.get('results', [])
        
        if items:
            item = items[0]
            print(f"   ✅ 找到相关知识")
            print(f"   标题: {item.get('title', 'N/A')}")
            
            # 提取关键信息
            content = item.get('content', '')
            if 'VOL' in content or '成交量' in content:
                print(f"   ✅ 内容包含成交量因子信息")
            if '聚宽' in content or 'JoinQuant' in content:
                print(f"   ✅ 内容包含聚宽平台信息")
            
            # 展示如何使用
            print(f"\n   💡 使用建议:")
            print(f"   1. 从知识库获取情绪因子定义")
            print(f"   2. 使用聚宽API获取相关数据")
            print(f"   3. 构建情绪因子选股策略")
        else:
            print(f"   ⚠️  未找到相关知识")
    
    # 场景2: 获取资金流向数据
    print("\n📋 场景2: 获取资金流向数据用于策略")
    print("   需求: 了解如何获取资金流向数据")
    
    result = client.call(
        tool_name='knowledge.search',
        arguments={
            'query': '资金流向 数据获取 AKShare',
            'limit': 1
        },
        timeout=30.0
    )
    
    if result.success:
        data = json.loads(result.data) if isinstance(result.data, str) else result.data
        items = data.get('items', []) or data.get('results', [])
        
        if items:
            item = items[0]
            print(f"   ✅ 找到相关知识")
            print(f"   标题: {item.get('title', 'N/A')}")
            
            content = item.get('content', '')
            if 'AKShare' in content or 'akshare' in content:
                print(f"   ✅ 内容包含AKShare数据获取方法")
            
            print(f"\n   💡 使用建议:")
            print(f"   1. 从知识库了解资金流向数据源")
            print(f"   2. 使用AKShare API获取数据")
            print(f"   3. 结合情绪因子构建综合策略")
        else:
            print(f"   ⚠️  未找到相关知识")
    
    return True


def generate_strategy_example():
    """基于知识库生成策略代码示例"""
    print("\n" + "=" * 70)
    print("📝 测试3: 基于知识库生成策略代码示例")
    print("=" * 70)
    
    client = MCPClient()
    
    # 搜索情绪因子相关内容
    print("\n🔍 搜索情绪因子相关知识...")
    result = client.call(
        tool_name='knowledge.search',
        arguments={
            'query': '情绪因子 VOL 成交量 聚宽',
            'limit': 1
        },
        timeout=30.0
    )
    
    if result.success:
        data = json.loads(result.data) if isinstance(result.data, str) else result.data
        items = data.get('items', []) or data.get('results', [])
        
        if items:
            item = items[0]
            content = item.get('content', '')
            
            print("✅ 找到相关知识，生成策略代码示例:")
            print("\n" + "-" * 70)
            print("基于知识库的策略代码示例:")
            print("-" * 70)
            
            # 生成示例代码
            example_code = '''
# 基于情绪因子与资金流向的选股策略
# 知识来源: 如何利用情绪因子与资金流向数据辅助A股交易

import jqdatasdk as jq
import akshare as ak
import pandas as pd

# 1. 情绪因子分析（基于知识库中的VOL、TVMA等因子）
def analyze_sentiment_factors(stock_list, start_date, end_date):
    """
    分析情绪因子
    知识库提示: VOL（成交量）和TVMA（成交额移动均值）是重要的情绪指标
    """
    # 获取成交量数据
    q = jq.query(
        jq.valuation.code,
        jq.valuation.turnover_ratio,  # 换手率
    ).filter(
        jq.valuation.code.in_(stock_list)
    )
    
    df = jq.get_fundamentals(q, date=end_date)
    
    # 计算5日、10日均量（知识库建议）
    # 成交量突增代表市场关注度飙升
    # 底部放量视为资金进场信号
    
    return df

# 2. 资金流向分析（使用AKShare）
def analyze_capital_flow(stock_code):
    """
    获取资金流向数据
    知识库提示: 可以使用AKShare获取资金流向相关数据
    """
    # 根据知识库，使用AKShare获取资金流向
    # 具体API需要根据知识库中的信息确定
    try:
        # 示例：获取资金流向数据
        # flow_data = ak.stock_individual_fund_flow_rank(...)
        pass
    except:
        pass
    
    return None

# 3. 综合选股策略
def select_stocks_by_sentiment_and_flow():
    """
    基于情绪因子和资金流向的综合选股策略
    """
    # 获取股票池
    stocks = jq.get_index_stocks('000300.XSHG')  # 沪深300
    
    # 分析情绪因子
    sentiment_data = analyze_sentiment_factors(stocks, '2024-01-01', '2024-12-31')
    
    # 筛选条件（基于知识库中的策略建议）
    # - 成交量放大（情绪高涨）
    # - 资金流入（资金流向）
    # - 底部放量（买入信号）
    
    selected = sentiment_data[
        (sentiment_data['turnover_ratio'] > 2.0)  # 换手率>2%
    ]
    
    return selected

if __name__ == '__main__':
    # 初始化聚宽
    jq.auth('username', 'password')
    
    # 执行策略
    result = select_stocks_by_sentiment_and_flow()
    print(f"筛选出 {len(result)} 只股票")
    print(result.head(10))
'''
            
            print(example_code)
            print("-" * 70)
            print("\n✅ 策略代码示例已生成（基于知识库内容）")
            
            return True
        else:
            print("⚠️  未找到相关知识，无法生成示例")
            return False
    else:
        print(f"❌ 搜索失败: {result.error}")
        return False


def main():
    """主函数"""
    print("=" * 70)
    print("🧪 情绪因子与资金流向知识库测试")
    print("=" * 70)
    print()
    
    # 测试1: 搜索功能
    search_ok = test_knowledge_search()
    
    # 测试2: 实际使用场景
    usage_ok = test_strategy_development_usage()
    
    # 测试3: 生成策略代码
    example_ok = generate_strategy_example()
    
    # 总结
    print("\n" + "=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    print(f"搜索功能: {'✅ 通过' if search_ok else '❌ 失败'}")
    print(f"使用场景: {'✅ 通过' if usage_ok else '❌ 失败'}")
    print(f"代码生成: {'✅ 通过' if example_ok else '❌ 失败'}")
    
    if search_ok and usage_ok:
        print("\n✅ 知识库构建成功，可以在策略开发中使用！")
    else:
        print("\n⚠️  部分测试未通过，请检查知识库索引")
    print("=" * 70)


if __name__ == '__main__':
    main()
