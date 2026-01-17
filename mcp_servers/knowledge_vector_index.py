#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识库向量索引构建模块
====================
使用sentence-transformers生成向量并存储到ChromaDB
"""

import logging
import json
from pathlib import Path
from typing import List, Dict, Any
import sys

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

logger = logging.getLogger(__name__)

# 向量索引文件
VECTOR_INDEX_DIR = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "vector_index"
VECTOR_INDEX_DIR.mkdir(parents=True, exist_ok=True)

# Embedding模型配置
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def build_vector_index(kb_file: Path, force_rebuild: bool = False) -> Dict:
    """
    构建向量索引
    
    Args:
        kb_file: 知识库JSON文件路径
        force_rebuild: 是否强制重建索引
        
    Returns:
        构建结果
    """
    try:
        # 检查索引是否存在
        index_meta_file = VECTOR_INDEX_DIR / "index_meta.json"
        if index_meta_file.exists() and not force_rebuild:
            logger.info("向量索引已存在，跳过构建")
            meta = json.loads(index_meta_file.read_text(encoding='utf-8'))
            return {
                "success": True,
                "message": "索引已存在",
                "items_count": meta.get("items_count", 0),
                "model": meta.get("model", ""),
                "index_path": str(VECTOR_INDEX_DIR)
            }
        
        # 导入依赖
        try:
            from sentence_transformers import SentenceTransformer
            import chromadb
        except ImportError as e:
            logger.error(f"依赖缺失: {e}")
            return {
                "success": False,
                "error": f"依赖缺失: {e}。请安装: pip install sentence-transformers chromadb"
            }
        
        # 加载知识库
        if not kb_file.exists():
            return {"success": False, "error": f"知识库文件不存在: {kb_file}"}
        
        kb = json.loads(kb_file.read_text(encoding='utf-8'))
        items = kb.get("items", [])
        
        if not items:
            return {"success": False, "error": "知识库为空"}
        
        logger.info(f"开始构建向量索引，共 {len(items)} 条知识条目")
        
        # 初始化embedding模型
        logger.info(f"加载embedding模型: {EMBEDDING_MODEL_NAME}")
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        
        # 初始化ChromaDB客户端
        client = chromadb.PersistentClient(path=str(VECTOR_INDEX_DIR))
        
        # 获取或创建集合
        collection_name = "knowledge_base"
        try:
            collection = client.get_collection(name=collection_name)
            if force_rebuild:
                client.delete_collection(name=collection_name)
                collection = client.create_collection(name=collection_name)
        except:
            collection = client.create_collection(name=collection_name)
        
        # 准备文本和元数据
        texts = []
        metadatas = []
        ids = []
        
        for idx, item in enumerate(items):
            # 组合标题和内容
            # 使用索引作为唯一ID
            unique_id = f"kb_idx_{idx}"
            original_id = item.get("id", unique_id)
            text = f"{item.get('title', '')}\n{item.get('content', '')}"
            texts.append(text)
            
            # 元数据
            metadata = {
                "id": original_id,  # 保留原始ID用于检索
                "index": idx,  # 索引位置
                "title": item.get("title", "")[:500],  # 限制长度
                "type": item.get("type", ""),
                "tags": ",".join(item.get("tags", []))[:500],  # 标签用逗号连接
            }
            metadatas.append(metadata)
            ids.append(unique_id)  # 使用索引作为唯一ID
        
        # 生成向量（批量处理）
        logger.info("正在生成向量...")
        batch_size = 32
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_embeddings = model.encode(batch_texts, show_progress_bar=False)
            embeddings.extend(batch_embeddings.tolist())
            
            if (i + batch_size) % 100 == 0:
                logger.info(f"已处理 {min(i+batch_size, len(texts))}/{len(texts)} 条")
        
        # 添加到ChromaDB
        logger.info("正在存储向量到ChromaDB...")
        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        # 保存元数据
        meta = {
            "items_count": len(items),
            "model": EMBEDDING_MODEL_NAME,
            "embedding_dim": len(embeddings[0]) if embeddings else 384,
            "index_path": str(VECTOR_INDEX_DIR)
        }
        index_meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
        
        logger.info(f"✅ 向量索引构建完成，共 {len(items)} 条，向量维度 {meta['embedding_dim']}")
        
        return {
            "success": True,
            "message": "索引构建成功",
            "items_count": len(items),
            "model": EMBEDDING_MODEL_NAME,
            "embedding_dim": meta["embedding_dim"],
            "index_path": str(VECTOR_INDEX_DIR)
        }
        
    except Exception as e:
        logger.error(f"构建向量索引失败: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # 测试构建索引
    logging.basicConfig(level=logging.INFO)
    
    kb_file = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "knowledge_base.json"
    result = build_vector_index(kb_file, force_rebuild=False)
    print(json.dumps(result, ensure_ascii=False, indent=2))

