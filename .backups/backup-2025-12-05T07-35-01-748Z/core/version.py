# -*- coding: utf-8 -*-
"""
版本管理模块
"""
from pathlib import Path

def get_version():
    """获取当前版本号"""
    version_file = Path(__file__).parent.parent / "VERSION"
    if version_file.exists():
        with open(version_file, 'r', encoding='utf-8') as f:
            version = f.read().strip()
        return version
    return "2.0.0"  # 默认版本

def increment_version(part='patch'):
    """
    递增版本号
    part: 'major', 'minor', 'patch'
    """
    version_file = Path(__file__).parent.parent / "VERSION"
    current_version = get_version()
    parts = current_version.split('.')
    
    if part == 'major':
        parts[0] = str(int(parts[0]) + 1)
        parts[1] = '0'
        parts[2] = '0'
    elif part == 'minor':
        parts[1] = str(int(parts[1]) + 1)
        parts[2] = '0'
    else:  # patch
        parts[2] = str(int(parts[2]) + 1)
    
    new_version = '.'.join(parts)
    
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write(new_version)
    
    return new_version

__version__ = get_version()

