"""
文件名: code_1_4_03.py
保存路径: code_library/001_Chapter1_System_Overview/1.4/001_Chapter1_Market_Analysis/1.4/code_1_4_03.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/001_Chapter1_System_Overview/1.4_Development_History_CN.md
提取时间: 2025-12-13 20:05:32
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 使用Chroma向量数据库
vector_db = ChromaDB()
results = vector_db.query(query, top_k=10)