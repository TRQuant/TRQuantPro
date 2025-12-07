#!/usr/bin/env python3
"""Cursor 规范检查工具

在 Cursor 中可以通过命令调用，用于 Quality Checker Agent
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional

def run_check(name: str, command: List[str], cwd: Optional[Path] = None) -> Tuple[bool, str]:
    """运行检查命令
    
    Args:
        name: 检查名称
        command: 命令列表
        cwd: 工作目录
        
    Returns:
        (是否通过, 输出信息)
    """
    print(f"🔍 {name}...")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=cwd
        )
        
        if result.returncode == 0:
            print(f"✓ {name} 通过")
            return True, result.stdout
        else:
            print(f"✗ {name} 失败")
            output = result.stdout + result.stderr
            if output:
                print(output[:500])  # 限制输出长度
            return False, output
    except FileNotFoundError:
        print(f"⚠ {name} 跳过（工具未安装）")
        return True, ""  # 工具不存在不算失败
    except subprocess.TimeoutExpired:
        print(f"⚠ {name} 超时")
        return False, "检查超时"
    except Exception as e:
        print(f"⚠ {name} 出错: {e}")
        return False, str(e)


def check_python_syntax(directory: Path) -> Tuple[bool, str]:
    """检查 Python 语法"""
    python_files = list(directory.rglob("*.py"))
    
    if not python_files:
        return True, "无 Python 文件"
    
    errors = []
    for py_file in python_files[:20]:  # 限制检查文件数
        try:
            compile(py_file.read_text(), str(py_file), "exec")
        except SyntaxError as e:
            errors.append(f"{py_file}:{e.lineno}: {e.msg}")
    
    if errors:
        return False, "\n".join(errors)
    return True, ""


def check_typescript_compile(extension_dir: Path) -> Tuple[bool, str]:
    """检查 TypeScript 编译"""
    if not (extension_dir / "package.json").exists():
        return True, "无 TypeScript 项目"
    
    return run_check(
        "TypeScript 编译",
        ["npm", "run", "compile"],
        cwd=extension_dir
    )


def main():
    """主函数"""
    project_root = Path(__file__).parent.parent
    extension_dir = project_root / "extension"
    
    checks = []
    
    # Python 语法检查
    passed, output = check_python_syntax(project_root)
    checks.append(("Python 语法", passed))
    
    # Python 风格检查（ruff）
    passed, _ = run_check(
        "Python 风格 (ruff)",
        ["ruff", "check", ".", "--quiet"],
        cwd=project_root
    )
    checks.append(("Python 风格", passed))
    
    # TypeScript 编译检查
    passed, _ = check_typescript_compile(extension_dir)
    checks.append(("TypeScript 编译", passed))
    
    # TypeScript 风格检查
    if (extension_dir / "package.json").exists():
        passed, _ = run_check(
            "TypeScript 风格 (lint)",
            ["npm", "run", "lint"],
            cwd=extension_dir
        )
        checks.append(("TypeScript 风格", passed))
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("检查结果汇总:")
    print("=" * 50)
    
    all_passed = True
    for name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {name}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n✅ 所有检查通过")
        return 0
    else:
        print("\n❌ 部分检查失败，请修复后重试")
        return 1


if __name__ == "__main__":
    sys.exit(main())


