# TRQuant 知识库管理工具 - 底层框架详解

> **更新时间**: 2026-01-09  
> **版本**: 1.0

---

## 📋 框架概览

TRQuant知识库管理工具采用**混合架构**，结合了多种技术栈：

### 核心框架

1. **存储层**: JSON文件 + ChromaDB（向量数据库）
2. **Embedding模型**: sentence-transformers
3. **检索方式**: 混合检索（向量语义搜索 + 关键词精确匹配）
4. **融合算法**: Reciprocal Rank Fusion (RRF)

---

## 🔧 技术栈详情

### 1. 向量数据库：ChromaDB

**位置**: `mcp_servers/knowledge_hybrid_search.py`, `mcp_servers/knowledge_vector_index.py`

**用途**:
- 存储知识条目的向量嵌入
- 支持语义相似度搜索
- 本地持久化存储

**实现**:
```python
import chromadb

# 初始化ChromaDB客户端
client = chromadb.PersistentClient(path=str(VECTOR_INDEX_DIR))
collection = client.get_collection(name="knowledge_base")

# 向量检索
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=limit
)
```

**存储位置**: `.trquant/dev/knowledge/vector_index/`

---

### 2. Embedding模型：sentence-transformers

**模型**: `paraphrase-multilingual-MiniLM-L12-v2`

**特点**:
- ✅ 支持中英文
- ✅ 轻量级（约80MB）
- ✅ 本地部署，无需API密钥
- ✅ 向量维度：384

**实现**:
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(texts)
```

**安装**:
```bash
pip install sentence-transformers
```

---

### 3. 混合检索（Hybrid Search）

**架构**: 向量检索 + 关键词检索 → RRF融合

**实现文件**:
- `mcp_servers/knowledge_hybrid_search.py` - 混合检索核心逻辑
- `mcp_servers/knowledge_search_api.py` - 统一搜索API
- `mcp_servers/unified_dev_server.py` - 集成到MCP工具

**检索流程**:
```
用户查询
    ↓
并行检索
    ├─→ 向量检索（ChromaDB）
    │   └─→ Top-K结果（语义相似度）
    │
    └─→ 关键词检索（JSON文件）
        └─→ Top-K结果（精确匹配）
    ↓
RRF融合（Reciprocal Rank Fusion）
    ↓
最终结果（Top-10）
```

---

### 4. 回退机制

**基础搜索**（当向量检索不可用时）:
- 纯关键词匹配
- 基于JSON文件的内存搜索
- 多维度评分（标题、内容、标签）

**实现位置**: `mcp_servers/unified_dev_server.py` (line 1867-1899)

---

## 📊 框架对比

### 当前实现 vs 其他框架

| 特性 | 当前实现 | LangChain | LlamaIndex | Haystack |
|------|---------|-----------|------------|----------|
| **向量数据库** | ChromaDB | 多种支持 | 多种支持 | 多种支持 |
| **Embedding** | sentence-transformers | 多种支持 | 多种支持 | 多种支持 |
| **检索方式** | 混合检索 | 可配置 | 可配置 | 可配置 |
| **复杂度** | 中等 | 高 | 高 | 高 |
| **依赖** | 轻量 | 重 | 重 | 重 |
| **本地部署** | ✅ | ✅ | ✅ | ✅ |

---

## 🚀 为什么选择当前方案？

### 1. ChromaDB（而非FAISS）

**选择ChromaDB的原因**:
- ✅ 更简单易用（API更友好）
- ✅ 自动管理索引
- ✅ 支持元数据过滤
- ✅ 持久化存储更简单

**FAISS的优势**（但未采用）:
- 性能略高
- 但需要手动管理索引
- API更底层

### 2. sentence-transformers（而非OpenAI Embeddings）

**选择sentence-transformers的原因**:
- ✅ 本地部署，数据隐私
- ✅ 免费开源
- ✅ 支持中英文
- ✅ 无需API密钥
- ✅ 离线使用

**OpenAI Embeddings的劣势**:
- ❌ 需要API密钥
- ❌ 数据上传到云端
- ❌ 有使用成本
- ❌ 需要网络连接

### 3. 混合检索（而非纯向量或纯关键词）

**选择混合检索的原因**:
- ✅ 精确匹配（关键词）保证API函数名、因子名100%准确
- ✅ 语义理解（向量）支持自然语言查询
- ✅ 两者互补，效果最佳

---

## 📁 文件结构

```
mcp_servers/
├── unified_dev_server.py          # MCP工具集成
├── knowledge_hybrid_search.py     # 混合检索实现
├── knowledge_vector_index.py      # 向量索引构建
└── knowledge_search_api.py         # 统一搜索API

.trquant/dev/knowledge/
├── knowledge_base.json            # 知识库JSON文件
└── vector_index/                  # ChromaDB向量索引
    ├── index_meta.json
    └── [ChromaDB数据文件]
```

---

## 🔍 使用示例

### 向量检索（如果启用）

```python
from mcp_servers.knowledge_hybrid_search import vector_search

# 向量语义搜索
results = vector_search("获取价格数据", limit=10)
```

### 混合检索（推荐）

```python
from mcp_servers.knowledge_search_api import search

# 自动选择最佳模式（向量+关键词）
results = search(
    query="获取价格数据",
    type_filter=None,
    limit=10,
    mode="auto"  # 或 "hybrid", "keyword", "basic"
)
```

### 基础搜索（回退模式）

```python
from mcp_servers.unified_dev_server import knowledge_search

# 纯关键词搜索
results = knowledge_search("get_price", limit=10)
```

---

## 📦 依赖安装

### 必需依赖

```bash
# 向量数据库
pip install chromadb

# Embedding模型
pip install sentence-transformers

# 其他依赖（通常已安装）
pip install numpy pandas
```

### 可选依赖

```bash
# 如果需要使用FAISS（当前未使用）
pip install faiss-cpu  # CPU版本
# 或
pip install faiss-gpu  # GPU版本（需要CUDA）
```

---

## ⚙️ 配置

### 向量索引配置

**位置**: `.trquant/dev/knowledge/vector_index/index_meta.json`

**配置项**:
- `embedding_model`: Embedding模型名称
- `vector_dimension`: 向量维度
- `collection_name`: ChromaDB集合名称

### 搜索模式配置

**模式选择**:
- `auto`: 自动选择（优先混合检索，失败则回退）
- `hybrid`: 强制混合检索
- `keyword`: 仅关键词检索
- `basic`: 基础文本搜索

---

## 🔄 工作流程

### 知识添加流程

```
knowledge_add()
    ↓
保存到JSON文件
    ↓
（可选）生成向量嵌入
    ↓
（可选）添加到ChromaDB
```

### 知识搜索流程

```
knowledge_search()
    ↓
尝试混合检索
    ├─→ 成功 → 返回结果
    └─→ 失败 → 回退到基础搜索
        └─→ 返回结果
```

---

## 📊 性能特点

### 向量检索
- **速度**: 中等（需要计算embedding）
- **准确性**: 高（语义理解）
- **资源消耗**: 中等（需要加载模型）

### 关键词检索
- **速度**: 快（内存搜索）
- **准确性**: 高（精确匹配）
- **资源消耗**: 低

### 混合检索
- **速度**: 中等（并行执行）
- **准确性**: 最高（两者互补）
- **资源消耗**: 中等

---

## 🚧 当前状态

### ✅ 已实现
- ChromaDB向量存储
- sentence-transformers embedding
- 混合检索框架
- RRF结果融合
- 回退机制

### ⚠️ 部分实现
- 向量索引构建（需要手动触发）
- 自动索引更新（添加知识时）

### ❌ 未实现
- LangChain集成（不需要，已有自定义实现）
- FAISS（可选，当前使用ChromaDB）
- 自动重排序（Reranker）

---

## 💡 总结

**当前知识库管理工具使用的框架**:

1. **向量数据库**: **ChromaDB**（不是FAISS）
2. **Embedding模型**: **sentence-transformers**（不是OpenAI）
3. **检索方式**: **混合检索**（向量+关键词）
4. **框架**: **自定义实现**（不是LangChain）

**为什么不用LangChain**:
- 已有完整的自定义实现
- 更轻量，依赖更少
- 更符合项目需求（量化研究场景）
- 更好的控制权

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-09
