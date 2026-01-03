"""
文件名: code_10_10_chunk_markdown.py
保存路径: code_library/010_Chapter10_Development_Guide/10.10/code_10_10_chunk_markdown.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.10_RAG_KB_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: chunk_markdown

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

def chunk_markdown(file_path: Path) -> List[Document]:
        """
    chunk_markdown函数
    
    **设计原理**：
    - **核心功能**：实现chunk_markdown的核心逻辑
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
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按标题切分
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    
    chunks = markdown_splitter.split_text(content)
    
    # 进一步切分（如果chunk太大）
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    all_chunks = []
    for chunk in chunks:
        sub_chunks = text_splitter.split_documents([chunk])
        all_chunks.extend(sub_chunks)
    
    return all_chunks