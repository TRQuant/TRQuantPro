"""
文件名: code_10_10_index_optimization.py
保存路径: code_library/010_Chapter10_Development_Guide/10.10/code_10_10_index_optimization.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.10_RAG_KB_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 索引优化

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 使用更小的chunk size
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 减小chunk size
    chunk_overlap=100
)

# 使用更快的embedding模型
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'}  # 或 'cuda' 如果有GPU
)