#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试数据源检查功能
====================
直接测试，不需要重新安装扩展
使用方法: python scripts/test_datasource_quick.py
"""

import sys
import asyncio
from pathlib import Path

# 设置路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / 'mcp_servers'))

async def test_direct_provider():
    """测试1: 直接调用数据提供者"""
    print("=" * 60)
    print("测试1: 直接调用数据提供者")
    print("=" * 60)
    try:
        from core.data.unified_data_provider_v2 import get_data_provider_v2
        provider = get_data_provider_v2()
        health_status = provider.health_check()
        
        print(f"✅ 成功！找到 {len(health_status)} 个数据源:")
        for name, status in health_status.items():
            print(f"  - {name}: available={status.available}, latency={status.latency_ms}ms")
        return True
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_workflow_step():
    """测试2: 通过工作流步骤执行"""
    print("\n" + "=" * 60)
    print("测试2: 通过工作流步骤执行")
    print("=" * 60)
    try:
        from workflow_9steps_server import execute_step_data_source
        result = await execute_step_data_source({}, {})
        
        print(f"✅ 成功！结果: success={result.get('success')}")
        if result.get('health_status'):
            print(f"  找到 {len(result['health_status'])} 个数据源:")
            for name, status in result['health_status'].items():
                print(f"  - {name}: available={status.get('available')}")
        if result.get('error'):
            print(f"  ⚠️ 错误: {result['error']}")
        return result.get('success', False)
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_mcp_client():
    """测试3: 通过MCPClient调用"""
    print("\n" + "=" * 60)
    print("测试3: 通过MCPClient调用")
    print("=" * 60)
    try:
        from core.mcp.client import MCPClient
        from pathlib import Path
        
        client = MCPClient(project_root=Path.cwd())
        result = client.call('workflow9.run_step', {
            'workflow_id': 'test-workflow',
            'step_id': 'data_source',
            'args': {}
        })
        
        print(f"✅ 成功！结果: success={result.success}")
        if result.data:
            print(f"  数据: {result.data}")
        if result.error:
            print(f"  ⚠️ 错误: {result.error}")
        return result.success
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_bridge():
    """测试4: 通过bridge.py调用"""
    print("\n" + "=" * 60)
    print("测试4: 通过bridge.py调用")
    print("=" * 60)
    try:
        import json
        import subprocess
        from pathlib import Path
        
        bridge_path = Path(__file__).parent.parent / 'extension' / 'python' / 'bridge.py'
        venv_python = Path(__file__).parent.parent / 'venv' / 'bin' / 'python3'
        
        request = {
            'action': 'call_mcp_tool',
            'params': {
                'tool_name': 'workflow9.run_step',
                'arguments': {
                    'workflow_id': 'test-workflow',
                    'step_id': 'data_source',
                    'args': {}
                }
            }
        }
        
        result = subprocess.run(
            [str(venv_python), str(bridge_path)],
            input=json.dumps(request),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            print(f"✅ 成功！结果: ok={response.get('ok')}")
            if response.get('data'):
                print(f"  数据: {response['data']}")
            if response.get('error'):
                print(f"  ⚠️ 错误: {response['error']}")
            return response.get('ok', False)
        else:
            print(f"❌ 失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("🚀 数据源检查功能快速测试")
    print("=" * 60)
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"Python路径: {sys.executable}")
    print()
    
    results = []
    
    # 测试1: 直接调用
    results.append(await test_direct_provider())
    
    # 测试2: 工作流步骤
    results.append(await test_workflow_step())
    
    # 测试3: MCPClient
    results.append(await test_mcp_client())
    
    # 测试4: bridge.py
    results.append(await test_bridge())
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    print(f"测试1 (直接调用): {'✅' if results[0] else '❌'}")
    print(f"测试2 (工作流步骤): {'✅' if results[1] else '❌'}")
    print(f"测试3 (MCPClient): {'✅' if results[2] else '❌'}")
    print(f"测试4 (bridge.py): {'✅' if results[3] else '❌'}")
    print(f"\n通过率: {sum(results)}/{len(results)} ({sum(results)/len(results)*100:.0f}%)")
    
    if all(results):
        print("\n🎉 所有测试通过！")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息")

if __name__ == '__main__':
    asyncio.run(main())

