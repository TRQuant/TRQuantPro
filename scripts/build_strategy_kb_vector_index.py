#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
构建陈小群策略知识库向量索引

使用sentence-transformers生成向量并存储到ChromaDB
"""

import sys
from pathlib import Path
import json
import logging

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 知识库文件
STRATEGY_KB_FILE = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "strategy_knowledge" / "chen_xiaoqun_kb.json"
VECTOR_INDEX_DIR = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "vector_index"
VECTOR_INDEX_DIR.mkdir(parents=True, exist_ok=True)

# Embedding模型配置
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def build_strategy_kb_vector_index(force_rebuild: bool = False) -> dict:
    """
    构建策略知识库向量索引
    
    Args:
        force_rebuild: 是否强制重建索引
        
    Returns:
        构建结果
    """
    try:
        # 检查索引是否存在
        index_meta_file = VECTOR_INDEX_DIR / "strategy_kb_meta.json"
        if index_meta_file.exists() and not force_rebuild:
            logger.info("策略知识库向量索引已存在，跳过构建")
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
        if not STRATEGY_KB_FILE.exists():
            return {"success": False, "error": f"知识库文件不存在: {STRATEGY_KB_FILE}"}
        
        kb = json.loads(STRATEGY_KB_FILE.read_text(encoding='utf-8'))
        items = kb.get("items", [])
        
        if not items:
            return {"success": False, "error": "知识库为空"}
        
        logger.info(f"开始构建向量索引，共 {len(items)} 条知识条目")
        
        # 初始化embedding模型
        logger.info(f"加载embedding模型: {EMBEDDING_MODEL_NAME}")
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        
        # 初始化ChromaDB客户端
        client = chromadb.PersistentClient(path=str(VECTOR_INDEX_DIR))
        
        # 获取或创建集合（使用独立的集合名称）
        collection_name = "strategy_knowledge_base"
        try:
            # 如果存在且需要重建，先删除
            if force_rebuild:
                try:
                    client.delete_collection(name=collection_name)
                    logger.info("已删除旧索引集合")
                except:
                    pass
            
            collection = client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "陈小群策略知识库向量索引"}
            )
        except Exception as e:
            logger.error(f"创建集合失败: {e}")
            return {"success": False, "error": f"创建集合失败: {e}"}
        
        # 准备数据
        texts = []
        metadatas = []
        ids = []
        
        for item in items:
            # 组合文本：标题 + 内容 + 标签
            text_parts = [item.get("title", "")]
            text_parts.append(item.get("content", ""))
            if item.get("tags"):
                text_parts.append(" ".join(item.get("tags", [])))
            
            text = "\n".join(text_parts)
            texts.append(text)
            
            # 元数据
            metadatas.append({
                "id": item.get("id", ""),
                "title": item.get("title", ""),
                "type": item.get("type", ""),
                "tags": ",".join(item.get("tags", [])),
                "source": item.get("source", "")
            })
            
            # ID
            ids.append(item.get("id", f"item_{len(ids)}"))
        
        # 批量生成向量
        logger.info("正在生成向量...")
        batch_size = 32
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = model.encode(batch_texts, show_progress_bar=False)
            embeddings.extend(batch_embeddings.tolist())
            logger.info(f"已处理 {min(i + batch_size, len(texts))}/{len(texts)} 条")
        
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
            "index_path": str(VECTOR_INDEX_DIR),
            "collection_name": collection_name,
            "created": json.dumps({"timestamp": __import__("datetime").datetime.now().isoformat()})
        }
        index_meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
        
        logger.info(f"✅ 向量索引构建完成，共 {len(items)} 条，向量维度 {meta['embedding_dim']}")
        
        return {
            "success": True,
            "message": "向量索引构建成功",
            "items_count": len(items),
            "model": EMBEDDING_MODEL_NAME,
            "embedding_dim": meta["embedding_dim"],
            "index_path": str(VECTOR_INDEX_DIR),
            "collection_name": collection_name
        }
        
    except Exception as e:
        logger.error(f"构建向量索引失败: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


def test_vector_search(query: str = "情绪周期", limit: int = 5):
    """测试向量搜索"""
    try:
        from sentence_transformers import SentenceTransformer
        import chromadb
        
        # 初始化模型
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        
        # 初始化ChromaDB客户端
        client = chromadb.PersistentClient(path=str(VECTOR_INDEX_DIR))
        collection_name = "strategy_knowledge_base"
        
        try:
            collection = client.get_collection(name=collection_name)
        except:
            logger.error("向量索引集合不存在，请先构建索引")
            return None
        
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
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "title": results['metadatas'][0][i].get("title", ""),
                    "type": results['metadatas'][0][i].get("type", ""),
                    "tags": results['metadatas'][0][i].get("tags", "").split(","),
                    "score": 1.0 - results['distances'][0][i] if i < len(results['distances'][0]) else 0.0,
                    "content_preview": results['documents'][0][i][:200] + "..." if len(results['documents'][0][i]) > 200 else results['documents'][0][i]
                })
        
        return formatted_results
        
    except Exception as e:
        logger.error(f"向量搜索测试失败: {e}")
        return None


def main():
    """主函数"""
    print("=" * 80)
    print("构建陈小群策略知识库向量索引")
    print("=" * 80)
    
    # 构建向量索引
    result = build_strategy_kb_vector_index(force_rebuild=False)
    
    if result.get("success"):
        print(f"\n✅ {result.get('message')}")
        print(f"   条目数: {result.get('items_count')}")
        print(f"   模型: {result.get('model')}")
        print(f"   向量维度: {result.get('embedding_dim')}")
        print(f"   索引路径: {result.get('index_path')}")
        print(f"   集合名称: {result.get('collection_name')}")
        
        # 测试搜索
        print("\n" + "=" * 80)
        print("测试向量搜索")
        print("=" * 80)
        test_results = test_vector_search("情绪周期", limit=3)
        if test_results:
            print(f"\n查询: '情绪周期'")
            print(f"找到 {len(test_results)} 条结果:\n")
            for i, item in enumerate(test_results, 1):
                print(f"{i}. [{item['type']}] {item['title']}")
                print(f"   相似度: {item['score']:.4f}")
                print(f"   标签: {', '.join(item['tags'][:5])}")
                print(f"   预览: {item['content_preview']}")
                print()
    else:
        print(f"\n❌ 构建失败: {result.get('error')}")


if __name__ == "__main__":
    main()
