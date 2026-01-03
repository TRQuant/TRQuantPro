"""
文件名: code_10_10_rerank.py
保存路径: code_library/010_Chapter10_Development_Guide/10.10/code_10_10_rerank.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.10_RAG_KB_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 重排序

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import numpy as np

from sentence_transformers import CrossEncoder

# 初始化reranker
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# 重排序
pairs = [[query, doc.page_content[:512]] for doc in results]
scores = reranker.predict(pairs)

# 按分数排序
sorted_indices = np.argsort(scores)[::-1]
reranked_results = [results[i] for i in sorted_indices]