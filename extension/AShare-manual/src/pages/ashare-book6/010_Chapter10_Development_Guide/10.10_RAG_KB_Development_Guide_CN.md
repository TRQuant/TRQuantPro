---
title: "10.10 RAG知识库开发指南"
description: "深入解析TRQuant RAG知识库开发，包括RAG技术原理、知识库架构、索引构建、检索策略、性能优化等核心技术，为知识库构建和维护提供完整的开发指导"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 📚 10.10 RAG知识库开发指南

> **核心摘要：**
> 
> 本节系统介绍TRQuant RAG知识库开发，包括RAG技术原理、知识库架构、索引构建、检索策略、性能优化等核心技术。通过理解RAG知识库开发的完整方法，帮助开发者掌握知识库的构建和维护技巧，为构建专业级的智能检索系统奠定基础。

RAG (Retrieval-Augmented Generation) 是一种结合信息检索和文本生成的技术。TRQuant系统通过RAG知识库实现智能化的文档检索和代码检索，为开发过程提供上下文信息。

## 📋 章节概览

<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}
</script>

<div class="section-overview">
  <div class="section-item" onclick="scrollToSection('section-10-10-1')">
    <h4>🔬 10.10.1 RAG技术原理</h4>
    <p>RAG概述、工作流程、核心组件、技术优势</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-10-2')">
    <h4>🏗️ 10.10.2 知识库架构</h4>
    <p>知识库体系、Manual KB、Engineering KB、数据来源</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-10-3')">
    <h4>🔨 10.10.3 索引构建</h4>
    <p>构建流程、文档切分、向量化、BM25索引、元数据提取</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-10-4')">
    <h4>🔍 10.10.4 检索策略</h4>
    <p>混合检索、结果融合、重排序、查询扩展、结果过滤</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-10-5')">
    <h4>⚡ 10.10.5 性能优化</h4>
    <p>索引优化、检索优化、存储优化、缓存策略</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解RAG技术**：掌握RAG技术原理和核心组件
- **设计知识库架构**：理解知识库体系结构和数据组织
- **构建索引**：掌握索引构建流程和文档处理技巧
- **实现检索策略**：掌握混合检索和结果融合方法
- **优化性能**：掌握性能优化技巧和最佳实践

## 📚 核心概念

### RAG技术

- **检索增强生成**：结合信息检索和文本生成
- **向量检索**：基于语义相似度的检索
- **关键词检索**：基于BM25的关键词匹配
- **重排序**：使用CrossEncoder提升相关性

### 知识库体系

- **Manual KB**：手册知识库（开发手册、设计文档）
- **Engineering KB**：工程知识库（代码、API、配置）
- **Strategy KB**：策略知识库（研究卡、策略规则）

### 检索策略

- **混合检索**：向量检索 + BM25检索
- **结果融合**：Reciprocal Rank Fusion (RRF)
- **重排序**：CrossEncoder重新排序

<h2 id="section-10-10-1">🔬 10.10.1 RAG技术原理</h2>

RAG (Retrieval-Augmented Generation) 是一种增强生成式AI的技术，通过检索相关文档来增强LLM的生成能力。

### RAG概述

```
传统生成式AI:
用户问题 → LLM → 回答（基于训练数据）

RAG增强:
用户问题 → 检索相关文档 → LLM（基于检索内容） → 回答（基于最新知识）
```

### RAG工作流程

```
用户查询
    ↓
查询理解
    ↓
向量检索 ←──┐
    ↓        │
BM25检索    │
    ↓        │
结果融合    │
    ↓        │
重排序      │
    ↓        │
上下文构建  │
    ↓        │
LLM生成    │
    ↓        │
最终回答    │
    └────────┘
    知识库
```

### 核心组件

#### 向量数据库（Vector Database）

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 初始化embedding模型
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'}
)

# 创建向量库
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="data/kb/manual_kb"
)
```

#### 关键词检索（BM25）

```python
from rank_bm25 import BM25Okapi

# 构建BM25索引
tokenized_docs = [doc.page_content.split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

# 检索
query_tokens = query.split()
scores = bm25.get_scores(query_tokens)
top_indices = np.argsort(scores)[-top_k:][::-1]
```

#### 重排序（Reranker）

```python
from sentence_transformers import CrossEncoder

# 初始化reranker
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# 重排序
pairs = [[query, doc.page_content[:512]] for doc in results]
scores = reranker.predict(pairs)

# 按分数排序
sorted_indices = np.argsort(scores)[::-1]
reranked_results = [results[i] for i in sorted_indices]
```

### RAG的优势

1. **实时性**：可以访问最新知识，无需重新训练模型
2. **准确性**：基于实际文档，减少幻觉
3. **可追溯性**：可以引用来源，便于验证
4. **可扩展性**：可以轻松添加新知识

<h2 id="section-10-10-2">🏗️ 10.10.2 知识库架构</h2>

TRQuant系统包含三个知识库：Manual KB、Engineering KB和Strategy KB。

### 知识库体系

```
知识库体系
├── Manual KB (手册知识库)
│   ├── 开发手册 (ashare-book6/**/*.md)
│   ├── 设计文档 (docs/**/*.md)
│   └── 使用指南 (extension/AShare-manual/docs/**/*.md)
│
├── Engineering KB (工程知识库)
│   ├── 代码文件 (core/**, extension/**, mcp_servers/**)
│   ├── 类定义 (classes)
│   ├── 函数定义 (functions)
│   └── 配置信息 (configs)
│
└── Strategy KB (策略知识库)
    ├── 研究卡 (research cards)
    ├── 策略规则 (strategy rules)
    └── 回测结果 (backtest results)
```

### Manual KB架构

#### 数据来源

```python
def collect_manual_kb_files() -> List[Path]:
    """收集Manual KB文件"""
    files = []
    project_root = Path(__file__).parent.parent.parent
    
    # 1. 开发手册
    manual_dir = project_root / "extension/AShare-manual/src/pages/ashare-book6"
    files.extend(manual_dir.rglob("*.md"))
    
    # 2. 设计文档
    docs_dir = project_root / "extension/AShare-manual/docs"
    files.extend(docs_dir.rglob("*.md"))
    
    # 3. 其他文档
    other_docs = project_root / "docs"
    if other_docs.exists():
        files.extend(other_docs.rglob("*.md"))
    
    return files
```

#### 文档切分

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

def chunk_markdown(file_path: Path) -> List[Document]:
    """切分Markdown文档"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按标题切分
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    
    chunks = markdown_splitter.split_text(content)
    
    # 进一步切分（如果chunk太大）
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    all_chunks = []
    for chunk in chunks:
        sub_chunks = text_splitter.split_documents([chunk])
        all_chunks.extend(sub_chunks)
    
    return all_chunks
```

### Engineering KB架构

#### 代码解析

```python
import ast
from langchain.schema import Document

def extract_symbols(file_path: Path) -> List[Document]:
    """提取代码符号（类、函数）"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
        symbols = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # 提取类定义
                docstring = ast.get_docstring(node) or ""
                code = ast.get_source_segment(content, node)
                
                symbols.append(Document(
                    page_content=f"{node.name}\n\n{docstring}\n\n{code}",
                    metadata={
                        "type": "class",
                        "name": node.name,
                        "file_path": str(file_path),
                        "line": node.lineno
                    }
                ))
            
            elif isinstance(node, ast.FunctionDef):
                # 提取函数定义
                docstring = ast.get_docstring(node) or ""
                code = ast.get_source_segment(content, node)
                
                symbols.append(Document(
                    page_content=f"{node.name}\n\n{docstring}\n\n{code}",
                    metadata={
                        "type": "function",
                        "name": node.name,
                        "file_path": str(file_path),
                        "line": node.lineno
                    }
                ))
        
        return symbols
    
    except SyntaxError:
        return []
```

<h2 id="section-10-10-3">🔨 10.10.3 索引构建</h2>

索引构建包括文档收集、切分、向量化、BM25索引构建等步骤。

### 构建流程

```
收集文件
    ↓
文档切分
    ↓
提取元数据
    ↓
生成向量
    ↓
构建索引
  ├── Chroma (向量索引)
  └── BM25 (关键词索引)
    ↓
保存索引
```

### Manual KB索引构建

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建Manual KB索引"""
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi
import json
import pickle

def build_manual_kb_index():
    """构建Manual KB索引"""
    
    # 1. 收集文件
    files = collect_manual_kb_files()
    print(f"✅ 共找到 {len(files)} 个文件")
    
    # 2. 切分文档
    all_documents = []
    for file_path in files:
        chunks = chunk_markdown(file_path)
        # 添加元数据
        for chunk in chunks:
            chunk.metadata.update(extract_metadata(file_path))
        all_documents.extend(chunks)
    
    print(f"✅ 共生成 {len(all_documents)} 个chunks")
    
    # 3. 构建向量索引
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    vectorstore = Chroma.from_documents(
        documents=all_documents,
        embedding=embeddings,
        persist_directory="data/kb/manual_kb"
    )
    
    # 4. 构建BM25索引
    tokenized_docs = [doc.page_content.split() for doc in all_documents]
    bm25_index = BM25Okapi(tokenized_docs)
    
    # 5. 保存索引
    with open("data/kb/manual_kb/bm25_index.pkl", 'wb') as f:
        pickle.dump(bm25_index, f)
    
    with open("data/kb/manual_kb/documents.json", 'w', encoding='utf-8') as f:
        json.dump([doc.dict() for doc in all_documents], f, ensure_ascii=False, indent=2)
    
    print("✅ Manual KB索引构建完成")

if __name__ == "__main__":
    build_manual_kb_index()
```

### 元数据提取

```python
import re
from datetime import datetime

def extract_metadata(file_path: Path) -> Dict[str, Any]:
    """提取文档元数据"""
    rel_path = file_path.relative_to(project_root)
    
    # 从路径提取信息
    parts = rel_path.parts
    metadata = {
        "file_path": str(rel_path),
        "doc_id": file_path.stem,
        "lang": "zh" if "_CN" in file_path.name else "en",
        "updated_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
    }
    
    # 提取章节信息
    if "Chapter" in str(rel_path):
        chapter_match = re.search(r'(\d+)_Chapter', str(rel_path))
        if chapter_match:
            metadata["chapter"] = int(chapter_match.group(1))
    
    return metadata
```

<h2 id="section-10-10-4">🔍 10.10.4 检索策略</h2>

检索策略包括混合检索、结果融合、重排序等。

### 混合检索（Hybrid Search）

```python
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
        """查询知识库"""
        
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
```

<h2 id="section-10-10-5">⚡ 10.10.5 性能优化</h2>

性能优化包括索引优化、检索优化、存储优化等。

### 索引优化

```python
# 使用更小的chunk size
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 减小chunk size
    chunk_overlap=100
)

# 使用更快的embedding模型
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'}  # 或 'cuda' 如果有GPU
)
```

### 检索优化

```python
# 缓存查询结果
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(query: str, scope: str, top_k: int):
    """缓存查询结果"""
    return kb.query(query, scope, top_k)

# 异步检索
import asyncio

async def async_query(query: str, scope: str, top_k: int):
    """异步查询"""
    tasks = []
    if scope in ["manual", "both"]:
        tasks.append(self._async_vector_search(query, "manual", top_k))
    if scope in ["engineering", "both"]:
        tasks.append(self._async_vector_search(query, "engineering", top_k))
    
    results = await asyncio.gather(*tasks)
    return self._merge_results(*results)
```

### 存储优化

```python
# 压缩向量存储
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="data/kb/manual_kb",
    collection_metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
)
```

## 🔗 相关章节

- **10.7 MCP服务器开发指南**：了解知识库MCP服务器的实现
- **10.9 MCP × Cursor × 工具链联用规范**：了解知识库在工具链中的使用
- **第1章：系统概述**：了解系统整体架构

## 💡 关键要点

1. **RAG技术原理**：检索增强生成，结合向量检索和关键词检索
2. **知识库架构**：Manual KB、Engineering KB、Strategy KB三个知识库
3. **索引构建**：文档切分、向量化、BM25索引构建
4. **检索策略**：混合检索、结果融合、重排序
5. **性能优化**：索引优化、检索优化、存储优化

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了RAG知识库开发，包括RAG技术原理、知识库架构、索引构建、检索策略、性能优化等核心技术。通过理解RAG知识库开发的完整方法，帮助开发者掌握知识库的构建和维护技巧。</p>
  
  <h3>下节预告</h3>
  <p>掌握了RAG知识库开发后，下一节将介绍开发流程方法论，包括问题识别、深入研究、方案设计、实现验证、文档化等。通过理解开发流程方法论，帮助开发者掌握系统化的开发方法。</p>
  
  <a href="/ashare-book6/010_Chapter10_Development_Guide/10.11_Development_Methodology_CN" class="next-section">
    继续学习：10.11 开发流程方法论 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
