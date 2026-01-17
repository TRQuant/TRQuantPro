#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能安装剩余包，跳过有问题的包
"""

import subprocess
import sys
from pathlib import Path

# 已知有问题的包（需要跳过或特殊处理）
SKIP_PACKAGES = ["pyqlib"]  # PyPI 上找不到匹配版本

def install_packages_smart(requirements_file: Path):
    """智能安装包，跳过有问题的包"""
    
    if not requirements_file.exists():
        print(f"❌ 文件不存在: {requirements_file}")
        return
    
    # 读取所有包
    with open(requirements_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📦 准备处理 {len(lines)} 个包")
    print(f"⏭️  将跳过: {', '.join(SKIP_PACKAGES)}")
    print()
    
    # 先检查哪些包已安装
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'list', '--format=freeze'],
        capture_output=True,
        text=True
    )
    installed_packages = set()
    for line in result.stdout.split('\n'):
        if '==' in line:
            pkg_name = line.split('==')[0].split('[')[0].strip().lower()
            installed_packages.add(pkg_name)
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    already_installed = 0
    
    for idx, line in enumerate(lines, 1):
        # 提取包名
        if '==' in line:
            pkg_name = line.split('==')[0].split('[')[0].strip().lower()
            package_spec = line
        elif '>=' in line:
            pkg_name = line.split('>=')[0].split('[')[0].strip().lower()
            package_spec = line
        else:
            pkg_name = line.strip().lower()
            package_spec = line
        
        # 检查是否需要跳过
        if any(skip in pkg_name for skip in SKIP_PACKAGES):
            skip_count += 1
            if skip_count <= 5:  # 只显示前5个跳过的包
                print(f"⏭️  [{idx}/{len(lines)}] 跳过: {pkg_name}")
            continue
        
        # 检查是否已安装
        if pkg_name in installed_packages:
            already_installed += 1
            continue
        
        # 尝试安装
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', package_spec],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                success_count += 1
                if success_count % 5 == 0 or success_count <= 10:
                    print(f"✅ [{idx}/{len(lines)}] 安装成功: {pkg_name}")
            else:
                # 检查是否是"已安装"的情况
                if 'already satisfied' in result.stdout.lower():
                    already_installed += 1
                else:
                    fail_count += 1
                    if fail_count <= 10:  # 只显示前10个失败的包
                        error_msg = result.stderr[:100] if result.stderr else result.stdout[:100]
                        print(f"❌ [{idx}/{len(lines)}] 安装失败: {pkg_name}")
                        if 'ERROR' in error_msg:
                            print(f"   错误: {error_msg}")
        except subprocess.TimeoutExpired:
            fail_count += 1
            print(f"⏱️  [{idx}/{len(lines)}] 安装超时: {pkg_name}")
        except Exception as e:
            fail_count += 1
            if fail_count <= 10:
                print(f"❌ [{idx}/{len(lines)}] 安装异常: {pkg_name} - {str(e)[:50]}")
    
    print()
    print("="*60)
    print("📊 安装统计:")
    print(f"   ✅ 新安装: {success_count}")
    print(f"   ⏭️  跳过: {skip_count}")
    print(f"   📦 已安装: {already_installed}")
    print(f"   ❌ 失败: {fail_count}")
    print(f"   📋 总计: {len(lines)}")
    print("="*60)

if __name__ == "__main__":
    requirements_file = Path("original_requirements.txt")
    install_packages_smart(requirements_file)

