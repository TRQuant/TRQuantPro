"""
文件名: code_10_8_increment_version.py
保存路径: code_library/010_Chapter10_Development_Guide/10.8/code_10_8_increment_version.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.8_Version_Release_Mechanism_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: increment_version

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# core/version.py
def increment_version(part="patch"):
        """
    increment_version函数
    
    **设计原理**：
    - **核心功能**：实现increment_version的核心逻辑
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
    version_file = Path(__file__).parent.parent / "VERSION"
    
    if not version_file.exists():
        current_version = "2.0.0"
    else:
        current_version = version_file.read_text().strip()
    
    major, minor, patch = map(int, current_version.split('.'))
    
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"无效的版本部分: {part}")
    
    new_version = f"{major}.{minor}.{patch}"
    
    # 更新版本文件
    version_file.write_text(new_version + "\n")
    
    return new_version