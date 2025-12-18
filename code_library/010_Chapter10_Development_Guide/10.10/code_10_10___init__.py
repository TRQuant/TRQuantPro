"""
文件名: code_10_10___init__.py
保存路径: code_library/010_Chapter10_Development_Guide/10.10/code_10_10___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.10_RAG_KB_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import numpy as np
from typing import Dict, List, Optional

class KBServer:
    """知识库服务器"""
    
    def __init__(self):
        self.manual_vectorstore = None
        self.engineering_vectorstore = None
        self.manual_bm25 = None
        self.engineering_bm25 = None
        self.manual_docs = None
        self.engineering_docs = None
        self.reranker = None
        self._load_indices()
    
    def query(
        self,
        query: str,
        scope: str = "both",  # "manual", "engineering", "both"
        top_k: int = 10,
        use_reranker: bool = False
    ) -> List[Dict[str, Any]]:
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
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
        
        # 1. 向量检索
        vector_results = self._vector_search(query, scope, top_k * 2)
        
        # 2. BM25检索
        bm25_results = self._bm25_search(query, scope, top_k * 2)
        
        # 3. 结果融合
        merged_results = self._merge_results(vector_results, bm25_results)
        
        # 4. 重排序（可选）
        if use_reranker:
            merged_results = self._rerank_results(query, merged_results, top_k)
        else:
            merged_results = merged_results[:top_k]
        
        return merged_results
    
    def _vector_search(self, query: str, scope: str, top_k: int) -> List[Dict]:
        """向量检索"""
        results = []
        
        if scope in ["manual", "both"] and self.manual_vectorstore:
            vector_results = self.manual_vectorstore.similarity_search_with_score(
                query, k=top_k
            )
            for doc, score in vector_results:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score),
                    "source": "manual",
                    "method": "vector"
                })
        
        if scope in ["engineering", "both"] and self.engineering_vectorstore:
            vector_results = self.engineering_vectorstore.similarity_search_with_score(
                query, k=top_k
            )
            for doc, score in vector_results:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score),
                    "source": "engineering",
                    "method": "vector"
                })
        
        return results
    
    def _bm25_search(self, query: str, scope: str, top_k: int) -> List[Dict]:
        """BM25检索"""
        results = []
        query_tokens = query.lower().split()
        
        if scope in ["manual", "both"] and self.manual_bm25 and self.manual_docs:
            bm25_scores = self.manual_bm25.get_scores(query_tokens)
            top_indices = np.argsort(bm25_scores)[-top_k:][::-1]
            
            for idx in top_indices:
                if bm25_scores[idx] > 0:
                    doc = self.manual_docs[idx]
                    results.append({
                        "content": doc.get("page_content", ""),
                        "metadata": doc.get("metadata", {}),
                        "score": float(bm25_scores[idx]),
                        "source": "manual",
                        "method": "bm25"
                    })
        
        if scope in ["engineering", "both"] and self.engineering_bm25 and self.engineering_docs:
            bm25_scores = self.engineering_bm25.get_scores(query_tokens)
            top_indices = np.argsort(bm25_scores)[-top_k:][::-1]
            
            for idx in top_indices:
                if bm25_scores[idx] > 0:
                    doc = self.engineering_docs[idx]
                    results.append({
                        "content": doc.get("page_content", ""),
                        "metadata": doc.get("metadata", {}),
                        "score": float(bm25_scores[idx]),
                        "source": "engineering",
                        "method": "bm25"
                    })
        
        return results
    
    def _merge_results(self, vector_results: List[Dict], bm25_results: List[Dict]) -> List[Dict]:
        """融合结果（使用Reciprocal Rank Fusion）"""
        combined = {}
        
        # 向量检索结果
        for i, result in enumerate(vector_results):
            doc_id = result["metadata"].get("doc_id", f"{result['source']}_{i}")
            if doc_id not in combined:
                combined[doc_id] = {
                    "result": result,
                    "vector_rank": i + 1,
                    "bm25_rank": None
                }
            else:
                combined[doc_id]["vector_rank"] = i + 1
        
        # BM25检索结果
        for i, result in enumerate(bm25_results):
            doc_id = result["metadata"].get("doc_id", f"{result['source']}_{i}")
            if doc_id not in combined:
                combined[doc_id] = {
                    "result": result,
                    "vector_rank": None,
                    "bm25_rank": i + 1
                }
            else:
                combined[doc_id]["bm25_rank"] = i + 1
        
        # 计算RRF分数
        for doc_id, info in combined.items():
            rrf_score = 0
            if info["vector_rank"]:
                rrf_score += 1.0 / (60 + info["vector_rank"])
            if info["bm25_rank"]:
                rrf_score += 1.0 / (60 + info["bm25_rank"])
            info["result"]["rrf_score"] = rrf_score
        
        # 按RRF分数排序
        sorted_results = sorted(
            combined.values(),
            key=lambda x: x["result"]["rrf_score"],
            reverse=True
        )
        return [item["result"] for item in sorted_results]
    
    def _rerank_results(
        self,
        query: str,
        results: List[Dict[str, Any]],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """使用reranker重新排序结果"""
        if not self.reranker:
            try:
                from sentence_transformers import CrossEncoder
                self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
            except ImportError:
                return results[:top_k]
        
        pairs = [[query, result["content"][:512]] for result in results]
        scores = self.reranker.predict(pairs)
        
        # 更新分数并排序
        for i, result in enumerate(results):
            result["rerank_score"] = float(scores[i])
            result["score"] = float(scores[i])
        
        results.sort(key=lambda x: x["rerank_score"], reverse=True)
        return results[:top_k]