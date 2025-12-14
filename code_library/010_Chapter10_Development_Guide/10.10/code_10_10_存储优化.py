"""
文件名: code_10_10_存储优化.py
保存路径: code_library/010_Chapter10_Development_Guide/10.10/code_10_10_存储优化.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.10_RAG_KB_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 存储优化

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 压缩向量存储
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="data/kb/manual_kb",
    collection_metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
)