"""
文件名: code_10_8_validate_version.py
保存路径: code_library/010_Chapter10_Development_Guide/10.8/code_10_8_validate_version.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.8_Version_Release_Mechanism_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: validate_version

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

# core/version.py
import re
from pathlib import Path

def validate_version(version: str) -> bool:
        """
    validate_version函数
    
    **设计原理**：
    - **核心功能**：实现validate_version的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version))

def get_version() -> str:
    """获取当前版本号"""
    version_file = Path(__file__).parent.parent / "VERSION"
    
    if version_file.exists():
        version = version_file.read_text().strip()
        if validate_version(version):
            return version
    
    return "2.0.0"  # 默认版本