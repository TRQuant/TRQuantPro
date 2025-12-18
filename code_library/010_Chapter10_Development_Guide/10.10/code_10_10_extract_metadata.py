"""
文件名: code_10_10_extract_metadata.py
保存路径: code_library/010_Chapter10_Development_Guide/10.10/code_10_10_extract_metadata.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.10_RAG_KB_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: extract_metadata

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

import re
from datetime import datetime

def extract_metadata(file_path: Path) -> Dict[str, Any]:
        """
    extract_metadata函数
    
    **设计原理**：
    - **核心功能**：实现extract_metadata的核心逻辑
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
    rel_path = file_path.relative_to(project_root)
    
    # 从路径提取信息
    parts = rel_path.parts
    metadata = {
        "file_path": str(rel_path),
        "doc_id": file_path.stem,
        "lang": "zh" if "_CN" in file_path.name else "en",
        "updated_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
    }
    
    # 提取章节信息
    if "Chapter" in str(rel_path):
        chapter_match = re.search(r'(\d+)_Chapter', str(rel_path))
        if chapter_match:
            metadata["chapter"] = int(chapter_match.group(1))
    
    return metadata