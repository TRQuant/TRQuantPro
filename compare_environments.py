#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比较 venv 和 conda base 环境的包差异
"""

import sys
from pathlib import Path

def parse_packages(file_path):
    """解析包列表"""
    packages = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # 处理各种格式
                if '==' in line:
                    pkg_name = line.split('==')[0].strip()
                    version = line.split('==')[1].strip()
                elif '>=' in line:
                    pkg_name = line.split('>=')[0].strip()
                    version = line.split('>=')[1].strip()
                elif '@' in line:
                    # 跳过 conda 的特殊格式
                    continue
                else:
                    pkg_name = line.strip()
                    version = None
                packages[pkg_name.lower()] = {
                    'name': pkg_name,
                    'version': version,
                    'full': line
                }
    except FileNotFoundError:
        pass
    return packages

def main():
    venv_file = "/tmp/venv_packages.txt"
    conda_file = "/tmp/conda_packages.txt"
    
    venv_pkgs = parse_packages(venv_file)
    conda_pkgs = parse_packages(conda_file)
    
    print("📊 环境包比较")
    print("="*60)
    print(f"venv 包总数: {len(venv_pkgs)}")
    print(f"conda 包总数: {len(conda_pkgs)}")
    print()
    
    # 找出缺失的包
    exclude = {'pip', 'setuptools', 'wheel', 'pkg-resources'}
    missing = {
        name: info for name, info in venv_pkgs.items() 
        if name not in conda_pkgs and name not in exclude
    }
    
    # 分类整理
    categories = {
        "可视化/图表": ["graphviz", "networkx", "pyecharts", "plotly", "seaborn", "matplotlib"],
        "数据源": ["akshare", "tushare", "pyqlib", "jqdatasdk"],
        "技术指标": ["ta-lib", "talib"],
        "量化分析": ["bullet-trade", "alphalens", "empyrical", "pyportfolioopt", "optuna"],
        "Web/API": ["scrapy", "selenium", "playwright", "flask", "fastapi"],
        "工具库": ["bottleneck", "openpyxl", "xlrd", "gitpython", "loguru", "pymongo"],
        "机器学习(可选)": ["torch", "transformers", "lightgbm", "xgboost", "tensorflow"],
    }
    
    categorized = {cat: [] for cat in categories}
    other = []
    
    for name, info in missing.items():
        found = False
        for category, keywords in categories.items():
            if any(kw in name.lower() for kw in keywords):
                categorized[category].append(info['full'])
                found = True
                break
        if not found:
            other.append(info['full'])
    
    print(f"⚠️  conda base 环境中缺失 {len(missing)} 个包\n")
    
    for category, packages in categorized.items():
        if packages:
            print(f"{category} ({len(packages)} 个):")
            for pkg in sorted(packages)[:10]:  # 只显示前10个
                pkg_name = pkg.split('==')[0].split('>=')[0]
                print(f"   - {pkg_name}")
            if len(packages) > 10:
                print(f"   ... 还有 {len(packages) - 10} 个")
            print()
    
    if other:
        print(f"其他包 ({len(other)} 个，仅显示前20个):")
        for pkg in sorted(other)[:20]:
            pkg_name = pkg.split('==')[0].split('>=')[0]
            print(f"   - {pkg_name}")
        if len(other) > 20:
            print(f"   ... 还有 {len(other) - 20} 个")
        print()
    
    # 推荐安装列表
    priority = [
        "graphviz", "networkx", "TA-Lib", "akshare",
        "bullet-trade", "pyqlib", "openpyxl", "Bottleneck",
        "GitPython", "loguru"
    ]
    
    print("💡 推荐优先安装的包:")
    priority_found = []
    for pkg in priority:
        for name, info in missing.items():
            if pkg.lower() in name.lower():
                priority_found.append(info['full'])
                break
    
    for pkg in priority_found:
        pkg_name = pkg.split('==')[0].split('>=')[0]
        version = pkg.split('==')[1] if '==' in pkg else ''
        print(f"   - {pkg_name:20s} {version}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

