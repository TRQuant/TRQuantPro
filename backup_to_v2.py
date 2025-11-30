#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()


"""
JQQuant_V2 备份脚本 (Python版本)
用于将当前代码备份到JQQuant_V2仓库
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    import os
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("=" * 60)
    print("JQQuant_V2 备份脚本")
    print("=" * 60)
    print()
    
    # 检查git状态
    print("1. 检查git状态...")
    status_result = run_command("git status --short", check=False)
    if status_result.stdout.strip():
        print(status_result.stdout)
        print()
        response = input("是否提交所有更改到git? (y/n): ").strip().lower()
        if response == 'y':
            # 添加所有更改
            print("2. 添加所有更改...")
            run_command("git add -A")
            
            # 提交
            commit_msg = input("请输入提交信息 (默认: 备份更新): ").strip()
            if not commit_msg:
                commit_msg = "备份更新"
            print(f"3. 提交更改: {commit_msg}")
            run_command(f'git commit -m "{commit_msg}"')
        else:
            print("跳过提交，直接推送现有提交...")
    else:
        print("工作区干净，无需提交")
    
    # 推送到origin
    print()
    print("4. 推送到origin仓库...")
    origin_result = run_command("git push origin master", check=False)
    if origin_result.returncode == 0:
        print("✅ 推送到origin成功")
    else:
        print("❌ 推送到origin失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(origin_result.stderr)
    
    # 推送到backup (JQQuant_V2)
    print()
    print("5. 推送到backup仓库 (JQQuant_V2)...")
    backup_result = run_command("git push backup master", check=False)
    if backup_result.returncode == 0:
        print("✅ 推送到JQQuant_V2成功")
    else:
        print("❌ 推送到JQQuant_V2失败")
        print("提示: 可能需要配置git凭据或使用SSH")
        print(backup_result.stderr)
    
    print()
    print("=" * 60)
    print("备份流程完成！")
    print("=" * 60)
    print()
    print("远程仓库:")
    run_command("git remote -v", check=False)
    print()

if __name__ == '__main__':
    import os
    main()

