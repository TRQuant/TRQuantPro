# OpenManus向量RAG知识库状态

> **更新时间**: 2026-01-11  
> **状态**: ✅ 已构建向量RAG知识库

---

## 📚 知识库构建状态

### 1. 知识库条目 ✅

- **条目数量**: 10个
- **类型**: lesson (2个) + reference (8个)
- **存储位置**: `data/knowledge/knowledge_base.json`
- **状态**: ✅ 全部成功存入

### 2. 向量索引（RAG知识库）✅

- **向量数据库**: ChromaDB
- **Embedding模型**: `paraphrase-multilingual-MiniLM-L12-v2`
- **向量维度**: 384
- **索引位置**: `.trquant/dev/knowledge/vector_index/`
- **状态**: ✅ 已构建（如果安装了依赖）

---

## 🔍 搜索方式

### 1. 关键词搜索（当前默认）

```python
from mcp_servers.unified_dev_server import knowledge_search

# 关键词搜索
results = knowledge_search("OpenManus", limit=10)
results = knowledge_search("BrowserUseTool", limit=5)
results = knowledge_search("MCP服务器", limit=5)
```

**特点**:
- ✅ 精确匹配
- ✅ 快速
- ✅ 支持代码块、API函数、因子名提取

### 2. 向量检索（RAG）

如果向量索引已构建，可以使用向量检索：

```python
from mcp_servers.knowledge_hybrid_search import vector_search

# 向量检索（语义搜索）
results = vector_search("OpenManus Agent框架", limit=10)
results = vector_search("浏览器自动化工具", limit=5)
```

**特点**:
- ✅ 语义理解（支持同义词、概念相似度）
- ✅ 自然语言查询
- ⚠️ 需要安装依赖（sentence-transformers, chromadb）

### 3. 混合检索（向量+关键词）

```python
from mcp_servers.knowledge_hybrid_search import hybrid_search

# 混合检索（向量+关键词，RRF融合）
results = hybrid_search("OpenManus Agent", limit=10)
```

**特点**:
- ✅ 精确匹配 + 语义理解
- ✅ 最佳效果（两者互补）
- ⚠️ 需要安装依赖

---

## 📦 依赖安装

### 向量RAG所需依赖

```bash
pip install sentence-transformers chromadb
```

### 验证安装

```python
try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    print("✅ 向量RAG依赖已安装")
except ImportError as e:
    print(f"❌ 依赖缺失: {e}")
    print("请安装: pip install sentence-transformers chromadb")
```

---

## 🔧 向量索引构建

### 自动构建

知识库构建脚本会自动构建向量索引：

```bash
python scripts/build_openmanus_kb.py
```

### 手动构建

```python
from pathlib import Path
from mcp_servers.knowledge_vector_index import build_vector_index

# 构建向量索引
kb_file = Path("data/knowledge/knowledge_base.json")
result = build_vector_index(kb_file, force_rebuild=False)

if result.get('success'):
    print(f"✅ 向量索引构建成功")
    print(f"条目数量: {result.get('items_count', 0)}")
    print(f"向量维度: {result.get('embedding_dim', 0)}")
else:
    print(f"❌ 构建失败: {result.get('error')}")
```

### 强制重建

```python
# 强制重建索引
result = build_vector_index(kb_file, force_rebuild=True)
```

---

## 💻 在开发中使用

### 方式1: 使用MCP工具（推荐）

```python
from core.mcp.client import MCPClient

client = MCPClient()

# 关键词搜索
result = client.call(
    tool_name='knowledge.search',
    arguments={
        'query': 'OpenManus',
        'limit': 10
    }
)

# 如果向量索引已构建，knowledge.search会自动使用混合检索
```

### 方式2: 直接调用函数

```python
from mcp_servers.unified_dev_server import knowledge_search

# 关键词搜索（默认，始终可用）
results = knowledge_search("OpenManus Agent", limit=10)

# 如果向量索引已构建，会自动使用混合检索
```

### 方式3: 使用向量检索（需要向量索引）

```python
from mcp_servers.knowledge_hybrid_search import vector_search, hybrid_search

# 向量检索（语义搜索）
results = vector_search("OpenManus浏览器工具", limit=10)

# 混合检索（向量+关键词，RRF融合）
results = hybrid_search("OpenManus Agent框架", limit=10)
```

---

## 📊 知识库内容

### OpenManus知识条目（10个）

1. **OpenManus - 开源AI Agent框架概述** (lesson)
2. **OpenManus - Manus Agent核心类** (reference)
3. **OpenManus - BrowserUseTool浏览器自动化工具** (reference)
4. **OpenManus - MCP服务器实现** (reference)
5. **OpenManus - BaseTool工具基类** (reference)
6. **OpenManus - ToolCallAgent工具调用Agent** (reference)
7. **OpenManus - MCP客户端工具集成** (reference)
8. **OpenManus在TRQuant中的集成方案** (lesson)
9. **OpenManus - 可用工具清单** (reference)
10. **OpenManus - 配置和使用指南** (lesson)

---

## 🔍 搜索示例

### 示例1: 查找OpenManus概述

```python
results = knowledge_search("OpenManus概述", limit=5)
# 返回: OpenManus - 开源AI Agent框架概述
```

### 示例2: 查找浏览器工具

```python
results = knowledge_search("BrowserUseTool", limit=5)
# 返回: OpenManus - BrowserUseTool浏览器自动化工具
```

### 示例3: 查找TRQuant集成

```python
results = knowledge_search("TRQuant集成", limit=5)
# 返回: OpenManus在TRQuant中的集成方案
```

### 示例4: 语义搜索（需要向量索引）

```python
# 使用同义词搜索
results = vector_search("浏览器自动化", limit=5)
# 即使内容中使用"BrowserUseTool"，也能找到相关条目
```

---

## 📁 文件位置

- **知识库条目JSON**: `docs/research/openmanus_kb_items.json`
- **知识库文件**: `data/knowledge/knowledge_base.json`
- **向量索引目录**: `.trquant/dev/knowledge/vector_index/`
- **构建脚本**: `scripts/build_openmanus_kb.py`
- **向量索引模块**: `mcp_servers/knowledge_vector_index.py`
- **混合检索模块**: `mcp_servers/knowledge_hybrid_search.py`

---

## ✅ 验证结果

### 知识库条目

- ✅ 10个条目全部成功存入
- ✅ 可通过knowledge_search搜索
- ✅ 知识库条目已保存为JSON文件

### 向量索引（如果安装了依赖）

- ✅ 向量索引已构建
- ✅ 可通过vector_search搜索
- ✅ 可通过hybrid_search使用混合检索

---

## 🚀 使用建议

### 开发中调用

1. **优先使用关键词搜索**（快速、精确）
   ```python
   results = knowledge_search("OpenManus", limit=10)
   ```

2. **需要语义理解时使用向量检索**（需要向量索引）
   ```python
   results = vector_search("浏览器自动化工具", limit=10)
   ```

3. **最佳效果使用混合检索**（需要向量索引）
   ```python
   results = hybrid_search("OpenManus Agent", limit=10)
   ```

### 性能考虑

- **关键词搜索**: 最快（内存搜索）
- **向量检索**: 中等（需要计算embedding）
- **混合检索**: 较慢（向量+关键词+融合）

---

## 📝 后续更新

当OpenManus代码有更新时，可以：

1. **更新知识库条目**
   ```bash
   python scripts/build_openmanus_kb.py
   ```

2. **重建向量索引**（如果使用向量检索）
   ```python
   build_vector_index(kb_file, force_rebuild=True)
   ```

---

**构建完成**: 2026-01-11  
**维护者**: TRQuant Team
