#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库MCP服务器
提供Manual KB和Engineering KB的检索和查询功能
"""
import sys
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "extension"))

try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    try:
        from langchain_huggingface import HuggingFaceEmbeddings as HFEmbeddings
    except ImportError:
        HFEmbeddings = HuggingFaceEmbeddings
    from rank_bm25 import BM25Okapi
    import numpy as np
except ImportError as e:
    print(f"❌ 缺少依赖: {e}", file=sys.stderr)
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KBServer:
    """知识库服务器"""
    
    def __init__(self):
        """初始化知识库服务器"""
        self.project_root = project_root
        self.manual_kb_path = project_root / "data/kb/manual_kb"
        self.engineering_kb_path = project_root / "data/kb/engineering_kb"
        
        # 初始化embedding模型
        try:
            self.embeddings = HFEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                model_kwargs={'device': 'cpu'}
            )
        except:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                model_kwargs={'device': 'cpu'}
            )
        
        # 加载向量库
        self.manual_vectorstore = None
        self.engineering_vectorstore = None
        
        # 加载BM25索引
        self.manual_bm25 = None
        self.engineering_bm25 = None
        self.manual_docs = None
        self.engineering_docs = None
        
        self._load_indices()
    
    def _load_indices(self):
        """加载索引"""
        try:
            # 加载Manual KB
            if (self.manual_kb_path / "chroma.sqlite3").exists():
                self.manual_vectorstore = Chroma(
                    persist_directory=str(self.manual_kb_path),
                    embedding_function=self.embeddings
                )
                logger.info("✅ Manual KB向量库加载成功")
            
            # 加载BM25索引
            if (self.manual_kb_path / "bm25_index.pkl").exists():
                with open(self.manual_kb_path / "bm25_index.pkl", 'rb') as f:
                    self.manual_bm25 = pickle.load(f)
                with open(self.manual_kb_path / "documents.json", 'r', encoding='utf-8') as f:
                    self.manual_docs = json.load(f)
                logger.info("✅ Manual KB BM25索引加载成功")
            
            # 加载Engineering KB
            if (self.engineering_kb_path / "chroma.sqlite3").exists():
                self.engineering_vectorstore = Chroma(
                    persist_directory=str(self.engineering_kb_path),
                    embedding_function=self.embeddings
                )
                logger.info("✅ Engineering KB向量库加载成功")
            
            # 加载BM25索引
            if (self.engineering_kb_path / "bm25_index.pkl").exists():
                with open(self.engineering_kb_path / "bm25_index.pkl", 'rb') as f:
                    self.engineering_bm25 = pickle.load(f)
                with open(self.engineering_kb_path / "documents.json", 'r', encoding='utf-8') as f:
                    self.engineering_docs = json.load(f)
                logger.info("✅ Engineering KB BM25索引加载成功")
        except Exception as e:
            logger.error(f"❌ 加载索引失败: {e}")
    
    def _rerank_results(
        self,
        query: str,
        results: List[Dict[str, Any]],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """使用reranker重新排序结果"""
        try:
            from sentence_transformers import CrossEncoder
            # 使用轻量级cross-encoder模型
            reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
            
            pairs = [[query, result["content"][:512]] for result in results]
            scores = reranker.predict(pairs)
            
            # 更新分数并排序
            for i, result in enumerate(results):
                result["rerank_score"] = float(scores[i])
                result["score"] = float(scores[i])  # 使用reranker分数
            
            results.sort(key=lambda x: x["rerank_score"], reverse=True)
            return results[:top_k]
        except ImportError:
            logger.warning("reranker未安装，跳过rerank步骤")
            return results[:top_k]
        except Exception as e:
            logger.warning(f"reranker失败: {e}，使用原始结果")
            return results[:top_k]
    
    def query(
        self,
        query: str,
        scope: str = "both",  # "manual", "engineering", "both"
        top_k: int = 10,
        use_reranker: bool = False
    ) -> List[Dict[str, Any]]:
        """
        查询知识库
        
        Args:
            query: 查询文本
            scope: 查询范围（manual, engineering, both）
            top_k: 返回结果数量
            use_reranker: 是否使用reranker
        
        Returns:
            检索结果列表
        """
        results = []
        
        # 向量检索
        if scope in ["manual", "both"] and self.manual_vectorstore:
            vector_results = self.manual_vectorstore.similarity_search_with_score(
                query, k=top_k * 2
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
                query, k=top_k * 2
            )
            for doc, score in vector_results:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score),
                    "source": "engineering",
                    "method": "vector"
                })
        
        # BM25检索
        if scope in ["manual", "both"] and self.manual_bm25 and self.manual_docs:
            query_tokens = query.lower().split()
            bm25_scores = self.manual_bm25.get_scores(query_tokens)
            top_indices = np.argsort(bm25_scores)[-top_k * 2:][::-1]
            
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
            query_tokens = query.lower().split()
            bm25_scores = self.engineering_bm25.get_scores(query_tokens)
            top_indices = np.argsort(bm25_scores)[-top_k * 2:][::-1]
            
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
        
        # 去重和排序
        seen = set()
        unique_results = []
        for result in results:
            key = (result["source"], result["metadata"].get("file_path", ""), 
                   result["metadata"].get("chunk_index", result["metadata"].get("symbol", "")))
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        # 按分数排序
        unique_results.sort(key=lambda x: x["score"], reverse=True)
        
        # 使用reranker重新排序（如果启用）
        if use_reranker and len(unique_results) > 0:
            unique_results = self._rerank_results(query, unique_results, top_k)
        else:
            unique_results = unique_results[:top_k]
        
        return unique_results
    
    def get_stats(self, scope: str = "both") -> Dict[str, Any]:
        """获取知识库统计信息"""
        stats = {}
        
        if scope in ["manual", "both"]:
            manual_stats_path = self.manual_kb_path / "stats.json"
            if manual_stats_path.exists():
                with open(manual_stats_path, 'r', encoding='utf-8') as f:
                    stats["manual"] = json.load(f)
        
        if scope in ["engineering", "both"]:
            engineering_stats_path = self.engineering_kb_path / "stats.json"
            if engineering_stats_path.exists():
                with open(engineering_stats_path, 'r', encoding='utf-8') as f:
                    stats["engineering"] = json.load(f)
        
        return stats


# MCP Server实现
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import asyncio

@dataclass
class MCPTool:
    """MCP工具定义"""
    name: str
    description: str
    input_schema: Dict[str, Any]


# 定义MCP工具
MCP_TOOLS: List[MCPTool] = [
    MCPTool(
        name="kb.query",
        description="查询知识库（Manual KB或Engineering KB）",
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "查询文本"
                },
                "scope": {
                    "type": "string",
                    "enum": ["manual", "engineering", "both"],
                    "default": "both",
                    "description": "查询范围：manual（手册）、engineering（工程）、both（两者）"
                },
                "top_k": {
                    "type": "integer",
                    "default": 10,
                    "description": "返回结果数量"
                },
                "use_reranker": {
                    "type": "boolean",
                    "default": False,
                    "description": "是否使用reranker重新排序"
                }
            },
            "required": ["query"]
        }
    ),
    MCPTool(
        name="kb.stats",
        description="获取知识库统计信息",
        input_schema={
            "type": "object",
            "properties": {
                "scope": {
                    "type": "string",
                    "enum": ["manual", "engineering", "both"],
                    "default": "both",
                    "description": "查询范围"
                }
            }
        }
    ),
    MCPTool(
        name="kb.index.build",
        description="构建知识库索引",
        input_schema={
            "type": "object",
            "properties": {
                "scope": {
                    "type": "string",
                    "enum": ["manual", "engineering", "both"],
                    "default": "both",
                    "description": "构建范围"
                }
            }
        }
    )
]


class KBMCPServer:
    """知识库MCP服务器"""
    
    def __init__(self):
        logger.info("知识库MCP服务器初始化")
        self.kb_server = KBServer()
    
    def list_tools(self) -> List[Dict]:
        """列出所有可用工具"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in MCP_TOOLS
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """调用工具"""
        try:
            if name == "kb.query":
                results = self.kb_server.query(
                    query=arguments.get("query", ""),
                    scope=arguments.get("scope", "both"),
                    top_k=arguments.get("top_k", 10),
                    use_reranker=arguments.get("use_reranker", False)
                )
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "results": results,
                                "count": len(results)
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            
            elif name == "kb.stats":
                stats = self.kb_server.get_stats(scope=arguments.get("scope", "both"))
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(stats, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            
            elif name == "kb.index.build":
                scope = arguments.get("scope", "both")
                # 调用构建脚本
                import subprocess
                import sys
                results = []
                
                if scope in ["manual", "both"]:
                    result = subprocess.run(
                        [sys.executable, str(project_root / "scripts/build_manual_kb_index.py")],
                        cwd=str(project_root),
                        capture_output=True,
                        text=True,
                        timeout=600  # 10分钟超时
                    )
                    results.append({
                        "scope": "manual",
                        "success": result.returncode == 0,
                        "output": result.stdout,
                        "error": result.stderr if result.returncode != 0 else None
                    })
                
                if scope in ["engineering", "both"]:
                    result = subprocess.run(
                        [sys.executable, str(project_root / "scripts/build_engineering_kb_index.py")],
                        cwd=str(project_root),
                        capture_output=True,
                        text=True,
                        timeout=600  # 10分钟超时
                    )
                    results.append({
                        "scope": "engineering",
                        "success": result.returncode == 0,
                        "output": result.stdout,
                        "error": result.stderr if result.returncode != 0 else None
                    })
                
                # 重新加载索引
                if any(r["success"] for r in results):
                    self.kb_server._load_indices()
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "success": all(r["success"] for r in results),
                                "results": results,
                                "message": "索引构建完成，已重新加载。方法论文档已包含在内。"
                            }, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            
            else:
                return {
                    "isError": True,
                    "content": [
                        {
                            "type": "text",
                            "text": f"未知工具: {name}"
                        }
                    ]
                }
        except Exception as e:
            logger.error(f"调用工具失败: {e}", exc_info=True)
            return {
                "isError": True,
                "content": [
                    {
                        "type": "text",
                        "text": f"错误: {str(e)}"
                    }
                ]
            }


# 主程序（用于测试）
if __name__ == "__main__":
    # 测试
    server = KBServer()
    results = server.query("如何构建策略", scope="both", top_k=5)
    print(f"查询结果: {len(results)} 条")
    for i, result in enumerate(results[:3], 1):
        print(f"\n结果 {i}:")
        print(f"  来源: {result['source']}")
        print(f"  分数: {result['score']:.4f}")
        print(f"  内容: {result['content'][:100]}...")

