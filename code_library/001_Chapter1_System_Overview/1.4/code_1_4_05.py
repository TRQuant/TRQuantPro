"""
文件名: code_1_4_05.py
保存路径: code_library/001_Chapter1_System_Overview/1.4/code_1_4_05.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/001_Chapter1_System_Overview/1.4_Development_History_CN.md
提取时间: 2025-12-13 20:18:15
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 混合检索 + 重排序
candidates = merge_results(vector_results, bm25_results)
reranked_results = cross_encoder.rerank(query, candidates)