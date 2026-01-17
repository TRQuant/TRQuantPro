#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AKShare知识库使用测试示例
==========================

演示如何在策略开发中使用AKShare知识库
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.mcp.client import MCPClient
import json


def test_search_akshare_api():
    """测试搜索AKShare API"""
    print("=" * 70)
    print("🔍 测试1: 搜索AKShare实时行情API")
    print("=" * 70)
    print()
    
    client = MCPClient()
    
    result = client.call(
        tool_name='knowledge.search',
        arguments={
            'query': 'AKShare 实时行情 A股',
            'limit': 3
        },
        timeout=30.0
    )
    
    if result.success:
        data = result.data
        if isinstance(data, str):
            data = json.loads(data)
        
        items = data.get('items', []) or data.get('results', [])
        print(f"✅ 找到 {len(items)} 条结果")
        print()
        
        for i, item in enumerate(items, 1):
            print(f"[{i}] {item.get('title', 'N/A')}")
            print(f"    类型: {item.get('type', 'N/A')}")
            print(f"    标签: {', '.join(item.get('tags', [])[:5])}")
            content = item.get('content', '')
            # 提取API函数名
            import re
            api_match = re.search(r'接口:\s*(\w+)', content)
            if api_match:
                print(f"    API: {api_match.group(1)}")
            print(f"    内容预览: {content[:150]}...")
            print()
    else:
        print(f"❌ 搜索失败: {result.error}")
    
    print()


def test_generate_strategy_code():
    """测试基于知识库生成策略代码"""
    print("=" * 70)
    print("💻 测试2: 基于知识库生成策略代码")
    print("=" * 70)
    print()
    
    # 模拟策略需求
    requirement = """
    需求: 获取所有A股实时行情，筛选出涨跌幅>5%且成交量放大的股票
    """
    print(f"📋 策略需求:")
    print(requirement)
    print()
    
    # 搜索相关知识
    client = MCPClient()
    result = client.call(
        tool_name='knowledge.search',
        arguments={
            'query': 'AKShare 实时行情 stock_zh_a_spot_em',
            'limit': 1
        },
        timeout=30.0
    )
    
    if result.success:
        data = result.data
        if isinstance(data, str):
            data = json.loads(data)
        
        items = data.get('items', []) or data.get('results', [])
        if items:
            item = items[0]
            content = item.get('content', '')
            
            # 提取API信息
            import re
            api_match = re.search(r'接口:\s*(\w+)', content)
            api_name = api_match.group(1) if api_match else 'stock_zh_a_spot_em'
            
            print(f"✅ 找到相关API: {api_name}")
            print()
            
            # 生成策略代码
            print("📝 生成的策略代码:")
            print()
            print("```python")
            print("import akshare as ak")
            print("import pandas as pd")
            print()
            print("def select_stocks_by_momentum():")
            print("    \"\"\"")
            print("    基于实时行情选股策略")
            print("    \"\"\"")
            print(f"    # 使用AKShare API: {api_name}")
            print(f"    df = ak.{api_name}()")
            print()
            print("    # 数据清洗")
            print("    df['涨跌幅_数值'] = df['涨跌幅'].str.replace('%', '').astype(float)")
            print("    df['量比_数值'] = df['量比'].astype(float)")
            print("    df['换手率_数值'] = df['换手率'].str.replace('%', '').astype(float)")
            print()
            print("    # 筛选条件")
            print("    selected = df[")
            print("        (df['涨跌幅_数值'] > 5.0) &")
            print("        (df['量比_数值'] > 1.5) &")
            print("        (df['换手率_数值'] > 2.0)")
            print("    ]")
            print()
            print("    return selected[['代码', '名称', '最新价', '涨跌幅', '量比', '换手率']]")
            print()
            print("# 执行策略")
            print("if __name__ == '__main__':")
            print("    result = select_stocks_by_momentum()")
            print("    print(f'筛选出 {len(result)} 只股票:')")
            print("    print(result.head(20))")
            print("```")
            print()
        else:
            print("❌ 未找到相关API")
    else:
        print(f"❌ 搜索失败: {result.error}")
    
    print()


def test_knowledge_base_statistics():
    """测试知识库统计"""
    print("=" * 70)
    print("📊 测试3: 知识库统计")
    print("=" * 70)
    print()
    
    import json
    from pathlib import Path
    
    kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
    if kb_file.exists():
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        items = kb.get('items', [])
        akshare_items = [i for i in items if 'AKShare' in i.get('title', '') or 'akshare' in i.get('content', '').lower()]
        
        print(f"总知识条目数: {len(items)}")
        print(f"AKShare相关条目数: {len(akshare_items)}")
        print()
        
        # 按类型统计
        type_counts = {}
        for item in akshare_items:
            kb_type = item.get('type', 'unknown')
            type_counts[kb_type] = type_counts.get(kb_type, 0) + 1
        
        print("按类型分布:")
        for kb_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {kb_type}: {count}条")
        print()
        
        # 按标签统计
        tag_counts = {}
        for item in akshare_items:
            tags = item.get('tags', [])
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        print("热门标签 (Top 10):")
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  - {tag}: {count}次")
        print()
    else:
        print("❌ 知识库文件不存在")
    
    print()


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 AKShare知识库使用测试")
    print("=" * 70)
    print()
    
    # 测试1: 搜索AKShare API
    test_search_akshare_api()
    
    # 测试2: 生成策略代码
    test_generate_strategy_code()
    
    # 测试3: 知识库统计
    test_knowledge_base_statistics()
    
    print("=" * 70)
    print("✅ 测试完成")
    print("=" * 70)


if __name__ == '__main__':
    main()
