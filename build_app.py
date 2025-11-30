#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())






# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())






# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())






# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())






# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())






# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())






# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())






# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())






# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())






# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())




# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())

# -*- coding: utf-8 -*-
"""
JQQuant 应用打包脚本
使用PyInstaller将应用打包为可执行文件
"""
import subprocess
import sys
import os
from pathlib import Path

def build_app():
    """打包应用"""
    print("=" * 60)
    print("JQQuant 应用打包")
    print("=" * 60)
    print()
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 打包命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=JQQuant",
        "--windowed",  # 无控制台窗口
        "--onedir",    # 打包为目录
        "--clean",     # 清理临时文件
        "--noconfirm", # 不询问确认
        
        # 添加数据文件
        "--add-data=config:config",
        "--add-data=strategies:strategies",
        "--add-data=utils:utils",
        "--add-data=core:core",
        "--add-data=jqdata:jqdata",
        "--add-data=gui:gui",
        
        # 隐藏导入
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=jqdatasdk",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        
        # 主入口
        "JQQuant.py"
    ]
    
    # 如果有图标文件
    icon_path = project_root / "gui" / "resources" / "icon.ico"
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
    print("执行打包命令...")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✅ 打包成功！")
        print("=" * 60)
        print()
        print(f"可执行文件位置: {project_root / 'dist' / 'JQQuant'}")
        print()
        print("运行方式:")
        print("  Linux/Mac: ./dist/JQQuant/JQQuant")
        print("  Windows:   dist\\JQQuant\\JQQuant.exe")
    else:
        print()
        print("❌ 打包失败，请检查错误信息")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(build_app())














