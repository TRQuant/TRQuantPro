#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动提交并推送脚本
保持版本号，自动commit和push到GitHub
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def get_version():
    """读取版本号"""
    version_file = Path(__file__).parent.parent / "VERSION"
    if version_file.exists():
        return version_file.read_text(encoding='utf-8').strip()
    return "2.0.0"

def run_cmd(cmd, check=True):
    """执行命令"""
    try:
        result = subprocess.run(
            cmd, shell=True, check=check,
            capture_output=True, text=True, encoding='utf-8'
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def main():
    """主函数"""
    import os
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # 读取版本号
    version = get_version()
    print(f"📦 当前版本: v{version}")
    
    # 检查是否有变更
    stdout, stderr, code = run_cmd("git status --porcelain", check=False)
    if not stdout:
        print("✅ 没有变更需要提交")
        return 0
    
    # 生成commit message
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_msg = f"""chore: auto commit [v{version}] - {timestamp}

自动提交更新
版本: v{version}
时间: {timestamp}"""
    
    # 添加所有变更
    print("📝 添加变更...")
    stdout, stderr, code = run_cmd("git add -A", check=False)
    if code != 0:
        print(f"❌ git add 失败: {stderr}")
        return 1
    
    # 提交
    print("💾 提交变更...")
    stdout, stderr, code = run_cmd(f'git commit -m "{commit_msg}"', check=False)
    if code != 0:
        if "nothing to commit" in stderr.lower():
            print("✅ 没有变更需要提交")
            return 0
        print(f"❌ git commit 失败: {stderr}")
        return 1
    
    print(f"✅ 提交成功: {stdout.split(chr(10))[0] if stdout else 'N/A'}")
    
    # 推送到远程
    print("📤 推送到GitHub...")
    stdout, stderr, code = run_cmd("git push origin main", check=False)
    if code != 0:
        print(f"⚠️  推送失败: {stderr}")
        print("   可能需要手动处理或检查网络连接")
        return 1
    
    print(f"✅ 推送成功 [v{version}]")
    return 0

if __name__ == "__main__":
    sys.exit(main())

