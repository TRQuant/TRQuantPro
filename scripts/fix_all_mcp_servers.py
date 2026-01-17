#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复所有MCP服务器的MCP SDK导入错误提示
========================================

统一所有MCP服务器的错误提示，提供更详细的修复建议
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MCP_SERVERS_DIR = PROJECT_ROOT / "mcp_servers"


def fix_mcp_import_error(file_path: Path):
    """修复单个文件的MCP SDK导入错误提示"""
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # 模式1: logger.error("MCP SDK不可用，请安装: pip install mcp")
    pattern1 = r'logger\.error\("MCP SDK不可用，请安装: pip install mcp"\)'
    replacement1 = '''logger.error("MCP SDK不可用，请安装: pip install mcp")
    logger.error(f"当前Python路径: {sys.executable}")
    # 检查是否是系统Python
    if 'venv' not in sys.executable and 'virtualenv' not in sys.executable:
        logger.error("⚠️  检测到使用系统Python，请使用venv中的Python:")
        venv_python = Path(__file__).parent.parent / "venv" / "bin" / "python3"
        if venv_python.exists():
            logger.error(f"  建议使用: {venv_python}")'''
    
    # 模式2: logger.error(f"官方MCP SDK不可用，请安装: pip install mcp. 错误: {e}")
    pattern2 = r'logger\.error\(f"官方MCP SDK不可用，请安装: pip install mcp\. 错误: \{e\}"\)'
    replacement2 = '''logger.error(f"官方MCP SDK不可用: {e}")
    logger.error("请确保使用venv中的Python，并安装MCP SDK:")
    logger.error("  ./venv/bin/pip install mcp")
    logger.error(f"当前Python路径: {sys.executable}")
    # 检查是否是系统Python
    if 'venv' not in sys.executable and 'virtualenv' not in sys.executable:
        logger.error("⚠️  检测到使用系统Python，请使用venv中的Python:")
        venv_python = Path(__file__).parent.parent / "venv" / "bin" / "python3"
        if venv_python.exists():
            logger.error(f"  建议使用: {venv_python}")'''
    
    # 模式3: print(f'官方MCP SDK不可用，请安装: pip install mcp. 错误: {e}', file=sys.stderr)
    pattern3 = r"print\(f'官方MCP SDK不可用，请安装: pip install mcp\. 错误: \{e\}', file=sys\.stderr\)"
    replacement3 = '''print(f'官方MCP SDK不可用: {e}', file=sys.stderr)
        print('请确保使用venv中的Python，并安装MCP SDK:', file=sys.stderr)
        print('  ./venv/bin/pip install mcp', file=sys.stderr)
        print(f'当前Python路径: {sys.executable}', file=sys.stderr)
        # 检查是否是系统Python
        if 'venv' not in sys.executable and 'virtualenv' not in sys.executable:
            print('⚠️  检测到使用系统Python，请使用venv中的Python:', file=sys.stderr)
            venv_python = Path(__file__).parent.parent / "venv" / "bin" / "python3"
            if venv_python.exists():
                print(f'  建议使用: {venv_python}', file=sys.stderr)'''
    
    # 应用修复
    if re.search(pattern1, content):
        content = re.sub(pattern1, replacement1, content)
        # 确保导入了sys和Path
        if 'import sys' not in content:
            content = content.replace('import sys', 'import sys', 1) if 'import sys' in content else 'import sys\n' + content
        if 'from pathlib import Path' not in content:
            content = content.replace('from pathlib import Path', 'from pathlib import Path', 1) if 'from pathlib import Path' in content else 'from pathlib import Path\n' + content
    
    if re.search(pattern2, content):
        content = re.sub(pattern2, replacement2, content)
        # 确保导入了sys和Path
        if 'import sys' not in content:
            content = 'import sys\n' + content
        if 'from pathlib import Path' not in content:
            # 查找import语句的位置
            import_match = re.search(r'^(import |from )', content, re.MULTILINE)
            if import_match:
                insert_pos = import_match.start()
                content = content[:insert_pos] + 'from pathlib import Path\n' + content[insert_pos:]
            else:
                content = 'from pathlib import Path\n' + content
    
    if re.search(pattern3, content):
        content = re.sub(pattern3, replacement3, content)
        # 确保导入了sys和Path
        if 'import sys' not in content:
            content = 'import sys\n' + content
        if 'from pathlib import Path' not in content:
            import_match = re.search(r'^(import |from )', content, re.MULTILINE)
            if import_match:
                insert_pos = import_match.start()
                content = content[:insert_pos] + 'from pathlib import Path\n' + content[insert_pos:]
            else:
                content = 'from pathlib import Path\n' + content
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    """主函数"""
    print("=" * 70)
    print("🔧 修复所有MCP服务器的MCP SDK导入错误提示")
    print("=" * 70)
    print()
    
    fixed_count = 0
    total_count = 0
    
    # 遍历所有Python文件
    for py_file in MCP_SERVERS_DIR.rglob("*.py"):
        if py_file.name.startswith('__'):
            continue
        
        total_count += 1
        try:
            if fix_mcp_import_error(py_file):
                print(f"✅ 已修复: {py_file.relative_to(PROJECT_ROOT)}")
                fixed_count += 1
        except Exception as e:
            print(f"❌ 修复失败 {py_file.relative_to(PROJECT_ROOT)}: {e}")
    
    print()
    print("=" * 70)
    print(f"📊 修复完成: {fixed_count}/{total_count} 个文件")
    print("=" * 70)
    print()
    print("✅ 所有MCP服务器现在都会提供更详细的错误信息和修复建议")
    print()


if __name__ == '__main__':
    main()
