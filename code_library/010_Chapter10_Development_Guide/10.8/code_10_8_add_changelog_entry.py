"""
文件名: code_10_8_add_changelog_entry.py
保存路径: code_library/010_Chapter10_Development_Guide/10.8/code_10_8_add_changelog_entry.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.8_Version_Release_Mechanism_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: add_changelog_entry

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# scripts/changelog_helper.py
#!/usr/bin/env python3
"""变更日志辅助工具"""
from pathlib import Path
from datetime import datetime
from core.version import get_version

def add_changelog_entry(category: str, description: str):
        """
    add_changelog_entry函数
    
    **设计原理**：
    - **核心功能**：实现add_changelog_entry的核心逻辑
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
    changelog_file = Path("CHANGELOG.md")
    
    if not changelog_file.exists():
        # 创建初始CHANGELOG
        changelog_file.write_text("""# 变更日志

所有重要的变更都会记录在此文件中。

## [未发布]

""")
    
    content = changelog_file.read_text(encoding='utf-8')
    
    # 在"## [未发布]"部分添加条目
    if "## [未发布]" in content:
        entry = f"- {description}\n"
        category_section = f"### {category}\n"
        
        if category_section in content:
            # 在现有分类下添加
            idx = content.find(category_section) + len(category_section)
            content = content[:idx] + entry + content[idx:]
        else:
            # 添加新分类
            idx = content.find("## [未发布]") + len("## [未发布]")
            content = content[:idx] + "\n\n" + category_section + entry + content[idx:]
    
    changelog_file.write_text(content, encoding='utf-8')
    print(f"✅ 已添加变更日志: [{category}] {description}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        add_changelog_entry(sys.argv[1], sys.argv[2])
    else:
        print("用法: python changelog_helper.py [类别] [描述]")
        print("类别: Added, Changed, Deprecated, Removed, Fixed, Security")