#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查项目依赖是否已安装
"""

import sys
from pathlib import Path

def check_package(package_name, import_name=None):
    """检查包是否已安装"""
    if import_name is None:
        import_name = package_name.replace("-", "_")
    
    try:
        mod = __import__(import_name)
        version = getattr(mod, '__version__', 'installed')
        return True, version
    except ImportError:
        return False, None

def main():
    print("🐍 Python 版本:", sys.version.split()[0])
    print("📦 检查 Python 库安装状态...\n")
    
    # 核心依赖包列表
    packages = {
        # 核心依赖
        "numpy": "numpy",
        "pandas": "pandas",
        "matplotlib": "matplotlib",
        "scikit-learn": "sklearn",
        
        # 聚宽API
        "jqdatasdk": "jqdatasdk",
        
        # 可视化
        "plotly": "plotly",
        "seaborn": "seaborn",
        
        # GUI
        "PyQt6": ("PyQt6", "PyQt6.QtCore"),
        "pyqtgraph": "pyqtgraph",
        
        # Jupyter
        "jupyter": "jupyter",
        "notebook": "notebook",
        "ipykernel": "ipykernel",
        
        # Web
        "flask": "flask",
        "flask-cors": "flask_cors",
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        
        # 工具
        "python-dotenv": ("python-dotenv", "dotenv"),
        "pyyaml": "yaml",
        "tqdm": "tqdm",
        "requests": "requests",
        "watchdog": "watchdog",
        "pydantic": "pydantic",
    }
    
    installed = []
    missing = []
    
    for package_name, import_info in packages.items():
        if isinstance(import_info, tuple):
            package_name_display, import_name = import_info
        else:
            package_name_display = package_name
            import_name = import_info
        
        try:
            # 特殊处理 PyQt6
            if package_name == "PyQt6":
                import PyQt6
                from PyQt6 import QtCore
                version = QtCore.PYQT_VERSION_STR
            else:
                mod = __import__(import_name)
                version = getattr(mod, '__version__', 'installed')
            
            installed.append((package_name_display, version))
            print(f"✅ {package_name_display:25s} - {version}")
        except ImportError:
            missing.append(package_name_display)
            print(f"❌ {package_name_display:25s} - 未安装")
        except Exception as e:
            missing.append(package_name_display)
            print(f"❌ {package_name_display:25s} - 检查失败: {str(e)[:50]}")
    
    print("\n" + "="*60)
    print(f"\n📊 统计:")
    print(f"   ✅ 已安装: {len(installed)}/{len(packages)}")
    print(f"   ❌ 缺失: {len(missing)}/{len(packages)}")
    
    if missing:
        print(f"\n⚠️  缺少以下 {len(missing)} 个包:")
        for pkg in missing:
            print(f"   - {pkg}")
        print(f"\n💡 安装命令:")
        print(f"   pip install {' '.join(missing)}")
        return 1
    else:
        print("\n✅ 所有核心依赖包已安装！")
        return 0

if __name__ == "__main__":
    sys.exit(main())

