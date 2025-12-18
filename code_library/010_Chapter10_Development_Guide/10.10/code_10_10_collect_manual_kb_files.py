"""
文件名: code_10_10_collect_manual_kb_files.py
保存路径: code_library/010_Chapter10_Development_Guide/10.10/code_10_10_collect_manual_kb_files.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.10_RAG_KB_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: collect_manual_kb_files

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def collect_manual_kb_files() -> List[Path]:
        """
    collect_manual_kb_files函数
    
    **设计原理**：
    - **核心功能**：实现collect_manual_kb_files的核心逻辑
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
    files = []
    project_root = Path(__file__).parent.parent.parent
    
    # 1. 开发手册
    manual_dir = project_root / "extension/AShare-manual/src/pages/ashare-book6"
    files.extend(manual_dir.rglob("*.md"))
    
    # 2. 设计文档
    docs_dir = project_root / "extension/AShare-manual/docs"
    files.extend(docs_dir.rglob("*.md"))
    
    # 3. 其他文档
    other_docs = project_root / "docs"
    if other_docs.exists():
        files.extend(other_docs.rglob("*.md"))
    
    return files