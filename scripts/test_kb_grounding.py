#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 KB Grounding MCP 服务器
"""
import sys
import asyncio
import json
from pathlib import Path

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.kb_grounding_server import (
    handle_answer_with_evidence,
    handle_code_with_evidence,
    handle_verify_citations
)


async def test_answer_with_evidence():
    """测试 answer_with_evidence"""
    print("=" * 70)
    print("测试: kb.answer_with_evidence")
    print("=" * 70)
    
    result = await handle_answer_with_evidence({
        "question": "如何使用JQData查询财务数据？",
        "mode": "code",
        "min_evidence_count": 3,
        "max_context_blocks": 10
    })
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()
    
    # 检查关键字段
    assert "context_blocks" in result
    assert "evidence_sufficient" in result
    assert "citation_format" in result
    
    print("✅ answer_with_evidence 测试通过")
    print()


async def test_code_with_evidence():
    """测试 code_with_evidence"""
    print("=" * 70)
    print("测试: kb.code_with_evidence")
    print("=" * 70)
    
    result = await handle_code_with_evidence({
        "task": "实现JQData财务数据获取函数",
        "file_path": "/home/taotao/dev/QuantTest/TRQuant/utils/data_fetcher.py",
        "module": "jqdata",
        "min_evidence_count": 5
    })
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()
    
    # 检查关键字段
    assert "context_blocks" in result
    assert "interface_contracts" in result
    assert "project_constraints" in result
    assert "anti_patterns" in result
    assert "evidence_sufficient" in result
    
    print("✅ code_with_evidence 测试通过")
    print()


async def test_verify_citations():
    """测试 verify_citations"""
    print("=" * 70)
    print("测试: kb.verify_citations")
    print("=" * 70)
    
    # 测试内容（带引用）
    content = """
    使用JQData获取财务数据 [KB:kb_xxx]。
    
    使用get_fundamentals查询valuation表 [KB:kb_yyy]。
    
    这是无引用的技术断言，应该被标记为未验证。
    """
    
    evidence_ids = ["kb_xxx", "kb_yyy"]
    
    result = await handle_verify_citations({
        "content": content,
        "evidence_ids": evidence_ids,
        "min_coverage": 0.7
    })
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()
    
    # 检查关键字段
    assert "coverage" in result
    assert "pass" in result
    assert "unverified_sentences" in result
    
    print("✅ verify_citations 测试通过")
    print()


async def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("KB Grounding MCP 服务器测试")
    print("=" * 70 + "\n")
    
    try:
        await test_answer_with_evidence()
        await test_code_with_evidence()
        await test_verify_citations()
        
        print("=" * 70)
        print("✅ 所有测试通过！")
        print("=" * 70)
        
    except Exception as e:
        print("=" * 70)
        print(f"❌ 测试失败: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

