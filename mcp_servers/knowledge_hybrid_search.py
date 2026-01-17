#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识库混合检索模块
================
结合向量检索和关键词检索，使用RRF融合结果
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys

TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

logger = logging.getLogger(__name__)

VECTOR_INDEX_DIR = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "vector_index"
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def vector_search(query: str, limit: int = 20) -> List[Dict]:
    """
    向量检索
    
    Args:
        query: 查询文本
        limit: 返回结果数量
        
    Returns:
        检索结果列表
    """
    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
        
        # 初始化模型
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        
        # 初始化ChromaDB客户端
        if not VECTOR_INDEX_DIR.exists():
            logger.warning("向量索引目录不存在，返回空结果")
            return []
        
        client = chromadb.PersistentClient(path=str(VECTOR_INDEX_DIR))
        collection_name = "knowledge_base"
        
        try:
            collection = client.get_collection(name=collection_name)
        except:
            logger.warning("向量索引集合不存在，返回空结果")
            return []
        
        # 生成查询向量
        query_embedding = model.encode(query).tolist()
        
        # 向量检索
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=limit
        )
        
        # 格式化结果
        formatted_results = []
        if results['ids'] and len(results['ids']) > 0:
            ids = results['ids'][0]
            documents = results['documents'][0] if results.get('documents') else []
            metadatas = results['metadatas'][0] if results.get('metadatas') else []
            distances = results['distances'][0] if results.get('distances') else []
            
            for i, kb_id in enumerate(ids):
                item = {
                    "id": kb_id,
                    "title": metadatas[i].get("title", "") if i < len(metadatas) else "",
                    "content": documents[i] if i < len(documents) else "",
                    "type": metadatas[i].get("type", "") if i < len(metadatas) else "",
                    "tags": metadatas[i].get("tags", "").split(",") if i < len(metadatas) and metadatas[i].get("tags") else [],
                    "_vector_score": 1.0 - distances[i] if i < len(distances) else 0.0,  # 距离转相似度
                    "_rank": i + 1
                }
                formatted_results.append(item)
        
        return formatted_results
        
    except Exception as e:
        logger.error(f"向量检索失败: {e}", exc_info=True)
        return []


def reciprocal_rank_fusion(results1: List[Dict], results2: List[Dict], k: int = 60) -> List[Dict]:
    """
    Reciprocal Rank Fusion (RRF) 融合两个检索结果
    
    Args:
        results1: 第一个检索结果（通常是关键词检索）
        results2: 第二个检索结果（通常是向量检索）
        k: RRF参数，通常为60
        
    Returns:
        融合后的结果列表
    """
    # 构建ID到结果的映射
    id_to_result = {}
    id_to_scores = {}
    
    # 处理第一个结果
    for rank, item in enumerate(results1, 1):
        item_id = item.get("id", "")
        if item_id:
            id_to_result[item_id] = item
            id_to_scores[item_id] = id_to_scores.get(item_id, 0) + 1.0 / (k + rank)
    
    # 处理第二个结果
    for rank, item in enumerate(results2, 1):
        item_id = item.get("id", "")
        if item_id:
            if item_id not in id_to_result:
                id_to_result[item_id] = item
            id_to_scores[item_id] = id_to_scores.get(item_id, 0) + 1.0 / (k + rank)
    
    # 按RRF分数排序
    fused_results = []
    for item_id, rrf_score in sorted(id_to_scores.items(), key=lambda x: x[1], reverse=True):
        result = id_to_result[item_id].copy()
        result["_rrf_score"] = rrf_score
        fused_results.append(result)
    
    return fused_results


def hybrid_search(
    query: str,
    keyword_results: List[Dict],
    vector_limit: int = 20,
    final_limit: int = 10
) -> List[Dict]:
    """
    混合检索：结合关键词检索和向量检索
    
    Args:
        query: 查询文本
        keyword_results: 关键词检索结果（已包含_score）
        vector_limit: 向量检索返回数量
        final_limit: 最终返回数量
        
    Returns:
        融合后的检索结果
    """
    try:
        # 向量检索
        vector_results = vector_search(query, limit=vector_limit)
        
        if not vector_results:
            # 如果向量检索失败，直接返回关键词结果
            logger.debug("向量检索返回空结果，仅使用关键词检索")
            return keyword_results[:final_limit]
        
        # RRF融合
        fused_results = reciprocal_rank_fusion(keyword_results, vector_results, k=60)
        
        # 限制返回数量
        return fused_results[:final_limit]
        
    except Exception as e:
        logger.error(f"混合检索失败: {e}", exc_info=True)
        # 失败时返回关键词检索结果
        return keyword_results[:final_limit]

