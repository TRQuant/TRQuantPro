#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试陈小群游资战法知识库
====================

测试知识库搜索和使用功能
"""

import sys
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_search


def test_chen_xiaoqun_kb():
    """测试陈小群游资战法知识库"""
    
    print("=" * 70)
    print("🧪 测试陈小群游资战法知识库")
    print("=" * 70)
    print()
    
    # 测试搜索
    test_queries = [
        "陈小群三板斧战法",
        "龙头战法",
        "合力情绪战法",
        "情绪周期",
        "选股三高",
        "航天发展",
        "中交地产"
    ]
    
    for query in test_queries:
        print(f"🔍 搜索: {query}")
        result = knowledge_search(query, limit=5)
        
        if result.get("success") and result.get("results"):
            print(f"   找到 {result.get('total', 0)} 条结果")
            for i, item in enumerate(result["results"][:3], 1):
                title = item.get("title", "未知标题")
                score = item.get("score", 0)
                print(f"   {i}. {title} (相关性: {score:.2f})")
        else:
            print(f"   ❌ 未找到结果")
        print()
    
    # 测试策略生成场景
    print("=" * 70)
    print("📝 测试策略生成场景")
    print("=" * 70)
    print()
    
    scenario_queries = [
        "如何识别龙头股",
        "首板卡位选股条件",
        "情绪周期四个阶段",
        "游资战法仓位管理"
    ]
    
    for query in scenario_queries:
        print(f"💡 场景: {query}")
        result = knowledge_search(query, limit=3)
        
        if result.get("success") and result.get("results"):
            print(f"   相关知识点:")
            for i, item in enumerate(result["results"], 1):
                title = item.get("title", "未知标题")
                print(f"   {i}. {title}")
        else:
            print(f"   ❌ 未找到相关知识点")
        print()
    
    print("=" * 70)
    print("✅ 测试完成")
    print("=" * 70)


if __name__ == "__main__":
    test_chen_xiaoqun_kb()
