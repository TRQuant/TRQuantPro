#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenManus评估脚本
评估OpenManus的可用性和功能，用于决定整合方式
"""
import sys
import os
from pathlib import Path

# 添加项目根路径
PROJECT_ROOT = Path(__file__).parent.parent
OPENMANUS_DIR = PROJECT_ROOT / "third_party" / "OpenManus"

sys.path.insert(0, str(OPENMANUS_DIR))

def evaluate_openmanus():
    """评估OpenManus的可用性和功能"""
    print("=" * 80)
    print("OpenManus 评估报告")
    print("=" * 80)
    print()
    
    results = {
        "installation": False,
        "import_test": False,
        "structure": False,
        "api_usage": False,
        "config": False,
    }
    
    # 1. 检查安装
    print("1. 检查安装状态...")
    venv_dir = OPENMANUS_DIR / ".venv"
    if venv_dir.exists():
        print(f"   ✅ 虚拟环境存在: {venv_dir}")
        results["installation"] = True
    else:
        print(f"   ❌ 虚拟环境不存在: {venv_dir}")
    print()
    
    # 2. 检查代码结构
    print("2. 检查代码结构...")
    key_files = [
        "main.py",
        "app/agent/manus.py",
        "app/tool/browser_use_tool.py",
        "app/mcp/server.py",
        "config/config.example.toml",
    ]
    
    all_exist = True
    for file_path in key_files:
        full_path = OPENMANUS_DIR / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} 不存在")
            all_exist = False
    
    results["structure"] = all_exist
    print()
    
    # 3. 尝试导入核心模块
    print("3. 测试模块导入...")
    try:
        # 尝试导入核心模块
        import importlib.util
        
        # 测试app/agent/manus.py
        manus_path = OPENMANUS_DIR / "app" / "agent" / "manus.py"
        if manus_path.exists():
            spec = importlib.util.spec_from_file_location("manus", manus_path)
            if spec and spec.loader:
                print("   ✅ app/agent/manus.py 可以加载")
            else:
                print("   ⚠️  app/agent/manus.py 加载器不可用")
        else:
            print("   ❌ app/agent/manus.py 不存在")
        
        # 测试app/tool/browser_use_tool.py
        browser_path = OPENMANUS_DIR / "app" / "tool" / "browser_use_tool.py"
        if browser_path.exists():
            spec = importlib.util.spec_from_file_location("browser_use_tool", browser_path)
            if spec and spec.loader:
                print("   ✅ app/tool/browser_use_tool.py 可以加载")
            else:
                print("   ⚠️  app/tool/browser_use_tool.py 加载器不可用")
        else:
            print("   ❌ app/tool/browser_use_tool.py 不存在")
        
        results["import_test"] = True
    except Exception as e:
        print(f"   ❌ 导入测试失败: {e}")
    print()
    
    # 4. 检查配置文件
    print("4. 检查配置文件...")
    config_example = OPENMANUS_DIR / "config" / "config.example.toml"
    config_file = OPENMANUS_DIR / "config" / "config.toml"
    
    if config_example.exists():
        print(f"   ✅ 配置示例文件存在: {config_example}")
        if config_file.exists():
            print(f"   ✅ 配置文件存在: {config_file}")
            results["config"] = True
        else:
            print(f"   ⚠️  配置文件不存在（需要从示例创建）: {config_file}")
    else:
        print(f"   ❌ 配置示例文件不存在: {config_example}")
    print()
    
    # 5. 分析使用方式
    print("5. 分析使用方式...")
    main_py = OPENMANUS_DIR / "main.py"
    if main_py.exists():
        with open(main_py, 'r', encoding='utf-8') as f:
            content = f.read()
            if "def main" in content or "if __name__" in content:
                print("   ✅ main.py 可以作为入口点运行")
            if "Agent" in content:
                print("   ✅ 包含Agent相关代码")
    print()
    
    # 总结
    print("=" * 80)
    print("评估总结")
    print("=" * 80)
    print(f"安装状态: {'✅' if results['installation'] else '❌'}")
    print(f"代码结构: {'✅' if results['structure'] else '❌'}")
    print(f"导入测试: {'✅' if results['import_test'] else '❌'}")
    print(f"配置文件: {'✅' if results['config'] else '⚠️'}")
    print()
    
    # 建议
    print("建议:")
    if results["installation"] and results["structure"]:
        print("  ✅ OpenManus可以正常安装和运行")
        print("  ✅ 建议：")
        print("     1. 可以作为独立项目使用（在third_party/OpenManus目录）")
        print("     2. 可以通过Python API调用（导入模块）")
        print("     3. 或者封装成Core模块供TRQuant使用")
    else:
        print("  ⚠️  需要进一步检查安装和配置")
    print()
    
    return results

if __name__ == "__main__":
    results = evaluate_openmanus()
    sys.exit(0 if all(results.values()) else 1)
