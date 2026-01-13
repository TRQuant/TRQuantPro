#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识库综合测试脚本
==================

测试知识库的：
1. 解析和添加功能
2. 搜索功能
3. 策略生成功能
4. 知识质量验证
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_search
from mcp_servers.knowledge_search_api import search as hybrid_search
from core.mcp.client import MCPClient


def test_kb_parsing_and_storage():
    """测试1: 解析和存储功能"""
    print("=" * 70)
    print("测试1: 知识库解析和存储功能")
    print("=" * 70)
    print()
    
    kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
    
    if not kb_file.exists():
        print("❌ 知识库文件不存在")
        return False
    
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        items = kb.get('items', [])
        print(f"✅ 知识库文件存在")
        print(f"   总条目数: {len(items)}")
        
        # 检查V2知识域
        v2_items = [i for i in items if i.get('type') in ['market_regime', 'factor_behavior', 'strategy_pattern', 'failure_case']]
        print(f"   V2知识条目: {len(v2_items)}")
        
        # 检查知识完整性
        missing_fields = []
        for item in v2_items[:10]:  # 检查前10条
            if not item.get('title'):
                missing_fields.append('title')
            if not item.get('content'):
                missing_fields.append('content')
            if not item.get('type'):
                missing_fields.append('type')
        
        if missing_fields:
            print(f"⚠️  发现缺失字段: {set(missing_fields)}")
        else:
            print(f"✅ 知识条目完整性检查通过")
        
        return True
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        return False


def test_kb_search():
    """测试2: 知识库搜索功能"""
    print()
    print("=" * 70)
    print("测试2: 知识库搜索功能")
    print("=" * 70)
    print()
    
    test_queries = [
        ("MACD", "因子行为映射"),
        ("RSI", "技术指标"),
        ("主升期", "市场状态"),
        ("板块轮动", "策略模板"),
        ("资金流向", "因子行为"),
        ("BulletTrade", "实盘交易"),
    ]
    
    success_count = 0
    for query, expected_type in test_queries:
        print(f"📋 搜索: \"{query}\"")
        try:
            # 测试关键词搜索
            result = knowledge_search(query, limit=3)
            
            if result and isinstance(result, dict):
                items = result.get('items', []) or result.get('results', [])
                if items:
                    print(f"   ✅ 找到 {len(items)} 条记录")
                    for i, item in enumerate(items[:2], 1):
                        title = item.get('title', 'N/A')
                        kb_type = item.get('type', 'N/A')
                        print(f"      {i}. {title[:60]}")
                        print(f"         类型: {kb_type}")
                    success_count += 1
                else:
                    print(f"   ⚠️  未找到记录")
            else:
                print(f"   ⚠️  搜索结果格式异常: {type(result)}")
        except Exception as e:
            print(f"   ❌ 搜索失败: {e}")
        print()
    
    print(f"✅ 搜索测试完成: {success_count}/{len(test_queries)} 个查询成功")
    return success_count == len(test_queries)


def test_hybrid_search():
    """测试3: 混合搜索功能（向量+关键词）"""
    print()
    print("=" * 70)
    print("测试3: 混合搜索功能（向量+关键词）")
    print("=" * 70)
    print()
    
    test_queries = [
        "MACD金叉在主升期的有效性",
        "RSI超买超卖在不同市场状态",
        "板块轮动策略在主升期",
        "资金流入但指数不涨",
    ]
    
    success_count = 0
    for query in test_queries:
        print(f"📋 混合搜索: \"{query}\"")
        try:
            result = hybrid_search(query=query, limit=3, mode='hybrid')
            
            if result and isinstance(result, dict):
                if result.get('success'):
                    items = result.get('results', [])
                    if items:
                        print(f"   ✅ 找到 {len(items)} 条记录")
                        for i, item in enumerate(items[:2], 1):
                            title = item.get('title', 'N/A')
                            score = item.get('score', 0)
                            print(f"      {i}. {title[:60]} (相似度: {score:.3f})")
                        success_count += 1
                    else:
                        print(f"   ⚠️  未找到记录")
                else:
                    print(f"   ⚠️  搜索失败: {result.get('error', 'Unknown')}")
            else:
                print(f"   ⚠️  搜索结果格式异常")
        except Exception as e:
            print(f"   ❌ 搜索失败: {e}")
            import traceback
            traceback.print_exc()
        print()
    
    print(f"✅ 混合搜索测试完成: {success_count}/{len(test_queries)} 个查询成功")
    return success_count >= len(test_queries) * 0.5  # 至少50%成功


def test_strategy_generation():
    """测试4: 策略生成功能"""
    print()
    print("=" * 70)
    print("测试4: 策略生成功能（使用知识库）")
    print("=" * 70)
    print()
    
    # 测试场景：生成主升期策略
    test_scenarios = [
        {
            "market_state": "主升期",
            "query": "主升期策略模板",
            "expected_factors": ["资金流向", "板块轮动", "趋势跟随"]
        },
        {
            "market_state": "退潮期",
            "query": "退潮期策略模板",
            "expected_factors": ["防御性", "空仓", "低波动"]
        }
    ]
    
    success_count = 0
    for scenario in test_scenarios:
        print(f"📋 场景: {scenario['market_state']}")
        print(f"   查询: \"{scenario['query']}\"")
        
        try:
            # 搜索相关策略模板
            result = knowledge_search(scenario['query'], limit=5)
            
            if result and isinstance(result, dict):
                items = result.get('items', []) or result.get('results', [])
                if items:
                    print(f"   ✅ 找到 {len(items)} 条策略模板")
                    
                    # 检查是否包含预期的因子
                    found_factors = []
                    for item in items:
                        content = item.get('content', '')
                        for factor in scenario['expected_factors']:
                            if factor in content:
                                found_factors.append(factor)
                    
                    if found_factors:
                        print(f"   ✅ 找到预期因子: {', '.join(set(found_factors))}")
                        success_count += 1
                    else:
                        print(f"   ⚠️  未找到预期因子")
                else:
                    print(f"   ⚠️  未找到策略模板")
            else:
                print(f"   ⚠️  搜索结果格式异常")
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
        print()
    
    print(f"✅ 策略生成测试完成: {success_count}/{len(test_scenarios)} 个场景成功")
    return success_count == len(test_scenarios)


def test_knowledge_quality():
    """测试5: 知识质量验证"""
    print()
    print("=" * 70)
    print("测试5: 知识质量验证")
    print("=" * 70)
    print()
    
    kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
    
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        items = kb.get('items', [])
        v2_items = [i for i in items if i.get('type') in ['market_regime', 'factor_behavior', 'strategy_pattern', 'failure_case']]
        
        print(f"📊 检查 {len(v2_items)} 条V2知识...")
        print()
        
        # 检查项
        checks = {
            "有标题": 0,
            "有内容": 0,
            "有类型": 0,
            "有标签": 0,
            "有来源": 0,
            "有可靠性标注": 0,
            "内容长度>100": 0,
            "内容包含结论": 0,
        }
        
        for item in v2_items:
            if item.get('title'):
                checks["有标题"] += 1
            if item.get('content'):
                checks["有内容"] += 1
                content = item.get('content', '')
                if len(content) > 100:
                    checks["内容长度>100"] += 1
                if '结论' in content or 'Conclusion' in content:
                    checks["内容包含结论"] += 1
            if item.get('type'):
                checks["有类型"] += 1
            if item.get('tags'):
                checks["有标签"] += 1
            if item.get('source'):
                checks["有来源"] += 1
            content = item.get('content', '')
            if '可靠性' in content or 'reliability' in content.lower():
                checks["有可靠性标注"] += 1
        
        # 输出检查结果
        total = len(v2_items)
        for check_name, count in checks.items():
            pct = count / total * 100 if total > 0 else 0
            status = "✅" if pct >= 90 else "⚠️" if pct >= 70 else "❌"
            print(f"   {status} {check_name}: {count}/{total} ({pct:.1f}%)")
        
        # 检查可靠性分布
        print()
        print("📈 可靠性分布检查:")
        reliability_count = {"A级": 0, "B级": 0, "C级": 0, "D级": 0, "未标注": 0}
        for item in v2_items:
            content = item.get('content', '')
            tags = str(item.get('tags', []))
            if 'A级可靠性' in content or 'A级' in tags:
                reliability_count["A级"] += 1
            elif 'B级可靠性' in content or 'B级' in tags:
                reliability_count["B级"] += 1
            elif 'C级可靠性' in content or 'C级' in tags:
                reliability_count["C级"] += 1
            elif 'D级可靠性' in content or 'D级' in tags:
                reliability_count["D级"] += 1
            else:
                reliability_count["未标注"] += 1
        
        for level, count in reliability_count.items():
            pct = count / total * 100 if total > 0 else 0
            print(f"   - {level}: {count}条 ({pct:.1f}%)")
        
        # 总体评估
        print()
        quality_score = sum(checks.values()) / (len(checks) * total) * 100 if total > 0 else 0
        if quality_score >= 90:
            print(f"✅ 知识质量评分: {quality_score:.1f}% (优秀)")
        elif quality_score >= 70:
            print(f"⚠️  知识质量评分: {quality_score:.1f}% (良好)")
        else:
            print(f"❌ 知识质量评分: {quality_score:.1f}% (需改进)")
        
        return quality_score >= 70
        
    except Exception as e:
        print(f"❌ 质量验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mcp_client_search():
    """测试6: MCP客户端搜索功能"""
    print()
    print("=" * 70)
    print("测试6: MCP客户端搜索功能")
    print("=" * 70)
    print()
    
    try:
        client = MCPClient()
        
        test_queries = [
            "MACD",
            "主升期",
            "策略模板"
        ]
        
        success_count = 0
        for query in test_queries:
            print(f"📋 MCP搜索: \"{query}\"")
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
                            data = {"raw": data}
                    
                    # 兼容多种返回格式
                    items = []
                    if isinstance(data, dict):
                        items = data.get('items', []) or data.get('results', []) or []
                        # 如果data本身就是列表
                        if not items and isinstance(data.get('data'), list):
                            items = data.get('data', [])
                    elif isinstance(data, list):
                        items = data
                    
                    if items:
                        print(f"   ✅ 找到 {len(items)} 条记录")
                        for i, item in enumerate(items[:2], 1):
                            title = item.get('title', 'N/A') if isinstance(item, dict) else str(item)[:60]
                            print(f"      {i}. {title}")
                        success_count += 1
                    else:
                        print(f"   ⚠️  未找到记录")
                        print(f"   调试信息: result.data类型={type(result.data)}, 内容={str(result.data)[:200]}")
                else:
                    print(f"   ❌ 搜索失败: {result.error}")
            except Exception as e:
                print(f"   ❌ 异常: {e}")
                import traceback
                traceback.print_exc()
            print()
        
        print(f"✅ MCP搜索测试完成: {success_count}/{len(test_queries)} 个查询成功")
        return success_count >= len(test_queries) * 0.5
        
    except Exception as e:
        print(f"❌ MCP客户端测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("=" * 70)
    print("🧪 知识库综合测试")
    print("=" * 70)
    print()
    
    results = {}
    
    # 测试1: 解析和存储
    results["解析和存储"] = test_kb_parsing_and_storage()
    
    # 测试2: 搜索功能
    results["搜索功能"] = test_kb_search()
    
    # 测试3: 混合搜索
    results["混合搜索"] = test_hybrid_search()
    
    # 测试4: 策略生成
    results["策略生成"] = test_strategy_generation()
    
    # 测试5: 知识质量
    results["知识质量"] = test_knowledge_quality()
    
    # 测试6: MCP客户端搜索
    results["MCP客户端"] = test_mcp_client_search()
    
    # 总结
    print()
    print("=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    print()
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {status} {test_name}")
    
    print()
    print(f"总计: {passed}/{total} 个测试通过 ({passed/total*100:.1f}%)")
    print()
    
    if passed == total:
        print("✅ 所有测试通过！知识库功能正常")
    elif passed >= total * 0.8:
        print("⚠️  大部分测试通过，知识库基本可用")
    else:
        print("❌ 多个测试失败，需要检查知识库配置")
    
    print("=" * 70)
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
