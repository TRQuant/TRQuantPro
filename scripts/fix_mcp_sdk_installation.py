#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复MCP SDK安装问题
==================

确保MCP SDK在正确的位置安装，并验证所有MCP服务器可以正常导入
"""

import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
VENV_PYTHON = PROJECT_ROOT / "venv" / "bin" / "python3"
VENV_PIP = PROJECT_ROOT / "venv" / "bin" / "pip"


def check_mcp_installation():
    """检查MCP SDK安装情况"""
    print("=" * 70)
    print("🔍 检查MCP SDK安装情况")
    print("=" * 70)
    print()
    
    # 检查venv Python
    if not VENV_PYTHON.exists():
        print(f"❌ Venv Python不存在: {VENV_PYTHON}")
        return False
    
    print(f"✅ Venv Python存在: {VENV_PYTHON}")
    
    # 检查MCP SDK是否已安装
    try:
        result = subprocess.run(
            [str(VENV_PYTHON), "-c", "import mcp; print('MCP SDK已安装')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ MCP SDK在venv中已安装")
            print(f"   输出: {result.stdout.strip()}")
        else:
            print("❌ MCP SDK在venv中未安装")
            print(f"   错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False
    
    # 检查MCP SDK版本
    try:
        result = subprocess.run(
            [str(VENV_PIP), "show", "mcp"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ MCP SDK版本信息:")
            for line in result.stdout.split('\n'):
                if 'Version:' in line or 'Location:' in line:
                    print(f"   {line.strip()}")
    except Exception as e:
        print(f"⚠️ 无法获取版本信息: {e}")
    
    print()
    return True


def install_mcp_sdk():
    """安装MCP SDK到venv"""
    print("=" * 70)
    print("📦 安装MCP SDK到venv")
    print("=" * 70)
    print()
    
    if not VENV_PIP.exists():
        print(f"❌ Venv pip不存在: {VENV_PIP}")
        return False
    
    try:
        print(f"正在安装MCP SDK...")
        result = subprocess.run(
            [str(VENV_PIP), "install", "mcp"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("✅ MCP SDK安装成功")
            if result.stdout:
                print("   输出:")
                for line in result.stdout.split('\n')[-5:]:
                    if line.strip():
                        print(f"   {line}")
            return True
        else:
            print("❌ MCP SDK安装失败")
            print(f"   错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 安装过程出错: {e}")
        return False


def verify_mcp_import():
    """验证MCP SDK可以正常导入"""
    print("=" * 70)
    print("✅ 验证MCP SDK导入")
    print("=" * 70)
    print()
    
    try:
        result = subprocess.run(
            [str(VENV_PYTHON), "-c", """
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
print('✅ MCP SDK所有模块导入成功')
print('   - Server: OK')
print('   - stdio_server: OK')
print('   - Tool: OK')
print('   - TextContent: OK')
            """],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print("❌ MCP SDK导入失败")
            print(f"   错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        return False


def test_mcp_server_import():
    """测试MCP服务器是否可以正常导入"""
    print("=" * 70)
    print("🧪 测试MCP服务器导入")
    print("=" * 70)
    print()
    
    test_servers = [
        "mcp_servers.unified_dev_server",
        "mcp_servers.enhanced_dev_workflow_server",
    ]
    
    success_count = 0
    for server_name in test_servers:
        try:
            result = subprocess.run(
                [str(VENV_PYTHON), "-c", f"import sys; sys.path.insert(0, '{PROJECT_ROOT}'); import {server_name}; print('✅ {server_name} 导入成功')"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(PROJECT_ROOT)
            )
            
            if result.returncode == 0:
                print(f"✅ {server_name} 导入成功")
                success_count += 1
            else:
                print(f"❌ {server_name} 导入失败")
                if result.stderr:
                    error_lines = result.stderr.split('\n')
                    for line in error_lines[-3:]:
                        if line.strip() and 'MCP SDK' in line:
                            print(f"   错误: {line.strip()}")
        except Exception as e:
            print(f"❌ {server_name} 测试出错: {e}")
    
    print()
    print(f"测试结果: {success_count}/{len(test_servers)} 个服务器导入成功")
    return success_count == len(test_servers)


def main():
    """主函数"""
    print("=" * 70)
    print("🔧 修复MCP SDK安装问题")
    print("=" * 70)
    print()
    
    # 步骤1: 检查当前安装情况
    if not check_mcp_installation():
        print()
        print("⚠️ MCP SDK未安装，开始安装...")
        print()
        if not install_mcp_sdk():
            print("❌ 安装失败，请手动运行: ./venv/bin/pip install mcp")
            return False
    
    print()
    
    # 步骤2: 验证导入
    if not verify_mcp_import():
        print("❌ 验证失败，请检查安装")
        return False
    
    print()
    
    # 步骤3: 测试MCP服务器导入
    if not test_mcp_server_import():
        print("⚠️ 部分MCP服务器导入失败，但MCP SDK本身已安装")
    
    print()
    print("=" * 70)
    print("✅ 修复完成")
    print("=" * 70)
    print()
    print("📝 建议:")
    print("   1. 确保所有MCP服务器使用venv中的Python")
    print("   2. 检查MCP服务器启动脚本是否正确指向venv Python")
    print("   3. 如果仍有问题，检查Python路径配置")
    print()
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
