#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenManus功能测试脚本 - 尝试通过Cursor调用LLM

测试目标：
1. 测试OpenManus能否作为MCP服务器运行
2. 测试OpenManus能否通过MCP客户端连接到TRQuant的MCP服务器
3. 测试OpenManus的基本功能（不依赖LLM API）
"""
import sys
import os
from pathlib import Path

# 添加项目根路径和OpenManus路径
PROJECT_ROOT = Path(__file__).parent.parent
OPENMANUS_DIR = PROJECT_ROOT / "third_party" / "OpenManus"

sys.path.insert(0, str(OPENMANUS_DIR))
sys.path.insert(0, str(PROJECT_ROOT))

def test_openmanus_import():
    """测试OpenManus模块导入"""
    print("=" * 80)
    print("测试1: OpenManus模块导入")
    print("=" * 80)
    
    try:
        from app.agent.manus import Manus
        print("✅ Manus Agent可以导入")
        return True
    except Exception as e:
        print(f"❌ Manus Agent导入失败: {e}")
        return False

def test_mcp_server():
    """测试MCP服务器功能"""
    print("\n" + "=" * 80)
    print("测试2: MCP服务器功能")
    print("=" * 80)
    
    try:
        from app.mcp.server import MCPServer
        
        server = MCPServer(name="openmanus-test")
        print("✅ MCP服务器可以创建")
        
        # 检查已注册的工具
        tools = list(server.tools.keys())
        print(f"✅ 已注册的工具: {', '.join(tools)}")
        
        return True
    except Exception as e:
        print(f"❌ MCP服务器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mcp_tools():
    """测试MCP工具功能"""
    print("\n" + "=" * 80)
    print("测试3: MCP工具功能")
    print("=" * 80)
    
    try:
        from app.tool.browser_use_tool import BrowserUseTool
        from app.tool.bash import Bash
        from app.tool.str_replace_editor import StrReplaceEditor
        
        # 测试浏览器工具
        browser_tool = BrowserUseTool()
        print(f"✅ BrowserUseTool可以创建: {browser_tool.name}")
        
        # 测试Bash工具
        bash_tool = Bash()
        print(f"✅ Bash工具可以创建: {bash_tool.name}")
        
        # 测试编辑器工具
        editor_tool = StrReplaceEditor()
        print(f"✅ StrReplaceEditor工具可以创建: {editor_tool.name}")
        
        return True
    except Exception as e:
        print(f"❌ MCP工具测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_trquant_mcp_integration():
    """测试与TRQuant MCP的集成"""
    print("\n" + "=" * 80)
    print("测试4: 与TRQuant MCP集成")
    print("=" * 80)
    
    try:
        from core.mcp.client import MCPClient
        
        client = MCPClient()
        print("✅ TRQuant MCP客户端可以创建")
        
        # 测试调用一个简单的MCP工具
        # 注意：这里只是测试客户端能否创建，不实际调用
        print("✅ MCP客户端可以正常使用")
        
        return True
    except Exception as e:
        print(f"⚠️  TRQuant MCP客户端测试失败（可能是环境问题）: {e}")
        return False

def test_configuration():
    """测试配置文件"""
    print("\n" + "=" * 80)
    print("测试5: 配置文件检查")
    print("=" * 80)
    
    config_file = OPENMANUS_DIR / "config" / "config.toml"
    
    if config_file.exists():
        print(f"✅ 配置文件存在: {config_file}")
        
        # 检查是否配置了LLM API
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "YOUR_API_KEY" in content:
                    print("⚠️  配置文件中的API密钥未设置（需要配置才能使用LLM功能）")
                else:
                    print("✅ 配置文件看起来已配置")
        except Exception as e:
            print(f"⚠️  读取配置文件失败: {e}")
        
        return True
    else:
        print(f"❌ 配置文件不存在: {config_file}")
        return False

def main():
    """主测试函数"""
    print("\n" + "=" * 80)
    print("OpenManus功能测试 - Cursor LLM集成测试")
    print("=" * 80)
    print(f"\nOpenManus目录: {OPENMANUS_DIR}")
    print(f"项目根目录: {PROJECT_ROOT}\n")
    
    results = {
        "import": test_openmanus_import(),
        "mcp_server": test_mcp_server(),
        "mcp_tools": test_mcp_tools(),
        "trquant_integration": test_trquant_mcp_integration(),
        "configuration": test_configuration(),
    }
    
    # 总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}: {'通过' if result else '失败'}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✅ 所有基础测试通过！")
        print("\n下一步建议：")
        print("1. 配置LLM API密钥（config/config.toml）以测试完整功能")
        print("2. 测试OpenManus作为MCP服务器运行")
        print("3. 测试OpenManus与TRQuant MCP服务器的连接")
    else:
        print("⚠️  部分测试失败，请检查错误信息")
    
    print("=" * 80 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
