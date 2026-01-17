# TRQuant知识库系统实施方案

> **版本**: 1.0  
> **更新日期**: 2026-01-09  
> **来源**: `docs/01_architecture/TRQuant知识库系统实施方案.pdf`

---

## 📋 系统概述

TRQuant知识库系统是一个完整的RAG（检索增强生成）系统，支持从知识采集到策略生成的完整闭环流程。

### 核心功能

1. **知识采集** - 多源数据抓取（网页、PDF、Markdown）
2. **数据处理** - 清洗、解析、结构化
3. **向量存储** - ChromaDB向量数据库
4. **混合检索** - 向量检索 + 关键词检索 + RRF融合
5. **知识管理** - 添加、搜索、统计、清理

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────┐
│  知识采集层 (Knowledge Crawler)          │
│  - 网页爬虫 (Playwright/Selenium)       │
│  - PDF解析                               │
│  - Markdown处理                          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  数据处理层 (Data Processor)            │
│  - 内容清洗                              │
│  - 结构解析                              │
│  - 文本分块                              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  存储层 (Storage)                        │
│  - JSON文件 (知识条目)                   │
│  - ChromaDB (向量索引)                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  检索层 (Retrieval)                      │
│  - 向量检索 (语义相似度)                 │
│  - 关键词检索 (精确匹配)                 │
│  - RRF融合 (结果融合)                    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  应用层 (Application)                     │
│  - MCP工具 (kb.add, kb.search)           │
│  - 策略生成                              │
│  - 代码转换                              │
└─────────────────────────────────────────┘
```

---

## 🛠️ 工具集

### 1. 知识库构建器 (`kb_builder.py`)

**位置**: `scripts/kb/kb_builder.py`

**功能**:
- 加载/保存知识库JSON文件
- 添加知识条目
- 构建向量索引
- 内容清洗和解析
- 文本分块

**使用示例**:
```python
from scripts.kb.kb_builder import KnowledgeBaseBuilder

builder = KnowledgeBaseBuilder()

# 添加知识
kb_id = builder.add_knowledge(
    title="聚宽API文档",
    content="...",
    type="reference",
    tags=["JoinQuant", "API"],
    source="https://www.joinquant.com/help/api",
    platform="JoinQuant"
)

# 构建向量索引
result = builder.build_vector_index(force_rebuild=False)
```

### 2. 知识库爬虫 (`kb_crawler.py`)

**位置**: `scripts/kb/kb_crawler.py`

**功能**:
- 使用Playwright爬取网页
- 使用MCP工具爬取网页
- 自动处理并保存到知识库

**使用示例**:
```bash
# 爬取网页并保存
python scripts/kb/kb_crawler.py \
    --url "https://www.joinquant.com/help/api" \
    --platform "JoinQuant" \
    --method "playwright" \
    --build-index
```

### 3. 知识库管理器 (`kb_manager.py`)

**位置**: `scripts/kb/kb_manager.py`

**功能**:
- 添加知识条目
- 搜索知识
- 显示统计信息
- 构建向量索引
- 清理重复条目

**使用示例**:
```bash
# 添加知识
python scripts/kb/kb_manager.py add \
    --title "聚宽API" \
    --content "..." \
    --platform "JoinQuant"

# 搜索知识
python scripts/kb/kb_manager.py search \
    --query "get_price函数" \
    --limit 10

# 显示统计
python scripts/kb/kb_manager.py stats

# 构建索引
python scripts/kb/kb_manager.py build-index --force

# 清理重复
python scripts/kb/kb_manager.py clean
```

---

## 📊 数据流程

### 1. 知识采集

**多源数据抓取**:
- **网页**: 使用Playwright或MCP工具（Selenium）
- **PDF**: 使用PDF解析库（待实现）
- **Markdown**: 直接解析

**结构化抓取**:
- 保留章节标题、副标题、列表、代码块
- 提取元数据（来源URL、发布时间、平台等）

**重点内容优先**:
- 策略编写和平台API相关知识
- 每个平台的策略框架、关键API、示例策略

### 2. 数据清洗与解析

**内容筛选**:
- 过滤导航菜单、广告、版权信息
- 合并分页内容
- 统一编码为UTF-8

**结构解析**:
- HTML → Markdown格式
- 保留标题层级（#、##、###）
- 代码块使用```包裹
- 添加元数据标签

**分段与摘要**:
- 按语义段落拆分（每段数百字）
- 提取重点摘要
- 统一术语（消歧和一致性）

### 3. 向量知识库构建

**Embedding文本片段**:
- 使用`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- 支持中英文，向量维度384
- 批量处理（batch_size=32）

**存储到ChromaDB**:
- 本地持久化存储
- 元数据包含：id、title、type、tags、platform
- 支持增量更新

**索引优化**:
- 定期重建索引
- 清理重复条目
- 监控索引质量

### 4. 混合检索

**向量检索**:
- 语义相似度搜索
- 支持同义词和概念相似度

**关键词检索**:
- 精确匹配API函数名、因子名
- 增强搜索（代码块、API函数、因子名提取）

**RRF融合**:
- Reciprocal Rank Fusion算法
- 融合向量检索和关键词检索结果
- 返回Top-K结果

---

## 🔧 技术栈

### 核心依赖

```python
# 向量数据库
chromadb>=0.4.0

# Embedding模型
sentence-transformers>=2.2.0

# 网页爬虫
playwright>=1.40.0
selenium>=4.15.0

# HTML解析
beautifulsoup4>=4.12.0
```

### 安装

```bash
# 安装依赖
pip install chromadb sentence-transformers playwright beautifulsoup4

# 安装Playwright浏览器
playwright install chromium
```

---

## 📁 目录结构

```
.trquant/dev/knowledge/
├── knowledge_base.json          # 知识库JSON文件
├── vector_index/                # ChromaDB向量索引
│   ├── index_meta.json          # 索引元数据
│   └── ...                      # ChromaDB数据文件
├── raw_data/                    # 原始数据（爬取的HTML等）
└── processed_data/              # 处理后的数据

scripts/kb/
├── kb_builder.py               # 知识库构建器
├── kb_crawler.py               # 知识库爬虫
└── kb_manager.py               # 知识库管理器

mcp_servers/
├── knowledge_vector_index.py    # 向量索引构建
├── knowledge_hybrid_search.py  # 混合检索
└── knowledge_search_api.py     # 统一搜索API
```

---

## 🚀 快速开始

### 1. 爬取网页并添加到知识库

```bash
# 爬取聚宽API文档
python scripts/kb/kb_crawler.py \
    --url "https://www.joinquant.com/help/api" \
    --platform "JoinQuant" \
    --method "playwright" \
    --build-index
```

### 2. 手动添加知识

```bash
python scripts/kb/kb_manager.py add \
    --title "聚宽get_price函数" \
    --content "get_price函数用于获取股票价格数据..." \
    --type "reference" \
    --tags "JoinQuant" "API" \
    --platform "JoinQuant"
```

### 3. 搜索知识

```bash
python scripts/kb/kb_manager.py search \
    --query "如何获取股票价格" \
    --limit 10
```

### 4. 构建向量索引

```bash
python scripts/kb/kb_manager.py build-index --force
```

### 5. 查看统计

```bash
python scripts/kb/kb_manager.py stats
```

---

## 🔍 MCP工具集成

知识库系统已集成到MCP工具中：

### 1. `kb.add` - 添加知识

```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='kb.add',
    arguments={
        'title': '知识标题',
        'content': '知识内容...',
        'category': 'JoinQuant'
    }
)
```

### 2. `kb.search` - 搜索知识

```python
result = client.call(
    tool_name='kb.search',
    arguments={
        'query': '查询文本',
        'limit': 10
    }
)
```

---

## 📈 最佳实践

### 1. 知识采集

- **优先抓取官方文档**: 确保准确性
- **保留结构信息**: 标题、代码块、列表
- **添加元数据**: 平台、类型、标签

### 2. 数据质量

- **定期清理重复**: 使用`kb_manager.py clean`
- **验证准确性**: 随机抽查知识条目
- **更新过期信息**: 及时更新API变更

### 3. 检索优化

- **使用混合检索**: 结合向量和关键词
- **调整RRF参数**: 根据效果调整k值
- **监控检索质量**: 记录用户反馈

---

## 🔄 持续维护

### 1. 定期更新

- 每周更新一次知识库
- 关注平台API变更
- 添加新的策略示例

### 2. 质量监控

- 检查知识条目准确性
- 清理重复和过期内容
- 优化检索效果

### 3. 性能优化

- 定期重建向量索引
- 优化分块策略
- 缓存热门查询结果

---

## 📚 参考文档

- `docs/KB_FRAMEWORK_DETAILS.md` - 知识库框架详解
- `docs/knowledge_base/KB_COMPREHENSIVE_SUMMARY.md` - 知识库综合总结
- `docs/01_architecture/TRQuant知识库系统实施方案.pdf` - 原始方案文档

---

## ✅ 实施状态

- ✅ 知识库构建器 (`kb_builder.py`)
- ✅ 知识库爬虫 (`kb_crawler.py`)
- ✅ 知识库管理器 (`kb_manager.py`)
- ✅ 向量索引构建 (`knowledge_vector_index.py`)
- ✅ 混合检索 (`knowledge_hybrid_search.py`)
- ✅ MCP工具集成 (`unified_dev_server.py`)
- ⏳ PDF解析（待实现）
- ⏳ 自动更新机制（待实现）

---

**最后更新**: 2026-01-09
