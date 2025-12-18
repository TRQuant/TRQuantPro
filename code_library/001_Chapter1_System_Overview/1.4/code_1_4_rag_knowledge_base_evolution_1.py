"""
文件名: code_1_4_04.py
保存路径: code_library/001_Chapter1_System_Overview/1.4/code_1_4_04.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/001_Chapter1_System_Overview/1.4_Development_History_CN.md
提取时间: 2025-12-13 20:18:15
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 向量检索 + BM25检索
vector_results = vector_db.query(query, top_k=10)
bm25_results = bm25_index.search(query, top_k=10)
# 结果融合
merged_results = merge_results(vector_results, bm25_results)