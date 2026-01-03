#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试因子MCP服务器
================
"""

import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))


async def test_factor_server():
    """测试因子服务器"""
    print("=" * 60)
    print("🐉 韬睿量化 - 因子MCP服务器测试")
    print("=" * 60)
    
    try:
        from factor_server import TOOLS, _handle_recommend
        
        print(f"\n📋 可用工具 ({len(TOOLS)}个):")
        for tool in TOOLS:
            print(f"  • {tool.name}: {tool.description[:40]}...")
        
        # 测试 factor.recommend (使用正确的参数名)
        print("\n📊 测试 factor.recommend...")
        
        test_cases = [
            {"market_state": "bull", "risk_preference": "aggressive"},
            {"market_state": "bear", "risk_preference": "moderate"},
            {"market_state": "neutral", "risk_preference": "conservative"},
        ]
        
        for case in test_cases:
            result = await _handle_recommend(case)
            
            if result.get("success"):
                factors = result.get("recommendations", [])
                print(f"\n  📈 市场: {case['market_state']}, 风险偏好: {case['risk_preference']}")
                print(f"  推荐因子数: {len(factors)}")
                for f in factors[:3]:
                    print(f"     • {f.get('name', 'N/A')} (ID: {f.get('id')})")
            else:
                print(f"  ⚠️ 失败: {result.get('error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    success = asyncio.run(test_factor_server())
    
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    print(f"  {'✅' if success else '❌'} 因子服务器测试: {'通过' if success else '失败'}")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
