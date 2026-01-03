"""
文件名: code_10_10_build_manual_kb_index.py
保存路径: code_library/010_Chapter10_Development_Guide/10.10/code_10_10_build_manual_kb_index.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.10_RAG_KB_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: build_manual_kb_index

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
    """
    build_manual_kb_index函数
    
    **设计原理**：
    - **核心功能**：实现build_manual_kb_index的核心逻辑
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
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi
import json
import pickle

def build_manual_kb_index():
        """
    build_manual_kb_index函数
    
    **设计原理**：
    - **核心功能**：实现build_manual_kb_index的核心逻辑
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
    
    # 1. 收集文件
    files = collect_manual_kb_files()
    print(f"✅ 共找到 {len(files)} 个文件")
    
    # 2. 切分文档
    all_documents = []
    for file_path in files:
        chunks = chunk_markdown(file_path)
        # 添加元数据
        for chunk in chunks:
            chunk.metadata.update(extract_metadata(file_path))
        all_documents.extend(chunks)
    
    print(f"✅ 共生成 {len(all_documents)} 个chunks")
    
    # 3. 构建向量索引
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    vectorstore = Chroma.from_documents(
        documents=all_documents,
        embedding=embeddings,
        persist_directory="data/kb/manual_kb"
    )
    
    # 4. 构建BM25索引
    tokenized_docs = [doc.page_content.split() for doc in all_documents]
    bm25_index = BM25Okapi(tokenized_docs)
    
    # 5. 保存索引
    with open("data/kb/manual_kb/bm25_index.pkl", 'wb') as f:
        pickle.dump(bm25_index, f)
    
    with open("data/kb/manual_kb/documents.json", 'w', encoding='utf-8') as f:
        json.dump([doc.dict() for doc in all_documents], f, ensure_ascii=False, indent=2)
    
    print("✅ Manual KB索引构建完成")

if __name__ == "__main__":
    build_manual_kb_index()