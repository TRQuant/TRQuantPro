#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
9步工作流集成测试
=================
测试workflow_9steps_server调用真实MCP服务器
"""

import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))


async def test_workflow():
    """测试完整9步工作流"""
    print("=" * 60)
    print("🐉 韬睿量化 - 9步工作流集成测试")
    print("=" * 60)
    
    # 导入workflow服务器
    try:
        from workflow_9steps_server import (
            _handle_tool,
            WORKFLOW_9STEPS,
            STEP_EXECUTORS
        )
        print("✅ workflow_9steps_server 导入成功")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    
    # 检查步骤执行器
    print(f"\n📋 步骤执行器检查 ({len(STEP_EXECUTORS)}个):")
    for step_id, executor in STEP_EXECUTORS.items():
        print(f"  ✅ {step_id}: {executor.__name__}")
    
    # 创建工作流
    print("\n" + "-" * 40)
    print("📋 步骤1: 创建工作流")
    result = await _handle_tool("workflow9.create", {"name": "集成测试工作流"})
    print(f"  结果: {result}")
    
    if not result.get("success"):
        print("❌ 创建工作流失败")
        return False
    
    workflow_id = result.get("workflow_id")
    print(f"  工作流ID: {workflow_id}")
    
    # 逐步执行
    step_results = []
    for i, step in enumerate(WORKFLOW_9STEPS, 1):
        print(f"\n" + "-" * 40)
        print(f"📋 步骤{i}: {step['name']} ({step['id']})")
        
        result = await _handle_tool("workflow9.run_step", {
            "workflow_id": workflow_id,
            "step_id": step["id"],
            "args": {}
        })
        
        step_result = result.get("step_result", {})
        success = step_result.get("success", True)
        summary = step_result.get("summary", "")
        
        emoji = "✅" if success else "❌"
        print(f"  {emoji} 结果: {summary or ('成功' if success else step_result.get('error', '失败'))}")
        
        step_results.append({"step": step["name"], "success": success})
    
    # 获取上下文
    print("\n" + "-" * 40)
    print("📋 最终上下文")
    context_result = await _handle_tool("workflow9.get_context", {"workflow_id": workflow_id})
    context = context_result.get("context", {})
    print(f"  上下文键: {list(context.keys())}")
    
    # 汇总
    print("\n" + "=" * 60)
    print("📊 测试汇总")
    print("=" * 60)
    
    passed = sum(1 for r in step_results if r["success"])
    for r in step_results:
        emoji = "✅" if r["success"] else "❌"
        print(f"  {emoji} {r['step']}")
    
    print(f"\n结果: {passed}/{len(step_results)} 步骤通过")
    
    return passed == len(step_results)


if __name__ == "__main__":
    success = asyncio.run(test_workflow())
    sys.exit(0 if success else 1)
