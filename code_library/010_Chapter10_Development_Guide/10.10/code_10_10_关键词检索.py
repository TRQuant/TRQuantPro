"""
文件名: code_10_10_关键词检索.py
保存路径: code_library/010_Chapter10_Development_Guide/10.10/code_10_10_关键词检索.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.10_RAG_KB_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 关键词检索

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import numpy as np

from rank_bm25 import BM25Okapi

# 构建BM25索引
tokenized_docs = [doc.page_content.split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

# 检索
query_tokens = query.split()
scores = bm25.get_scores(query_tokens)
top_indices = np.argsort(scores)[-top_k:][::-1]