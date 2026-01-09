# 知识库扩展架构设计

> **创建时间**: 2026-01-03  
> **说明**: 知识库扩展的架构设计和存储方案

---

## 📋 当前状态

### 已有知识库

- ✅ **聚宽网站爬虫**: `scripts/crawl_jqdata_*.py`
- ✅ **知识库存储**: `data/kb/`, `docs/joinquant_kb_comprehensive/`
- ✅ **MCP知识库服务器**: `mcp_servers/kb_server.py`
- ✅ **向量索引**: 使用现有知识库向量搜索功能

---

## 🏗️ 扩展架构

### 知识库分类结构

```
知识库
├── 技术文档 (technical_docs)
│   ├── 聚宽文档 (joinquant) ✅
│   ├── 订阅网站文档 (subscription) 🆕
│   ├── 开源项目文档 (open_source) 🆕
│   └── API文档 (api_docs) 🆕
│
├── 理论知识 (theoretical_knowledge) 🆕
│   ├── 投资书籍 (books)
│   ├── 学术论文 (papers)
│   └── 行业报告 (reports)
│
├── 数据文档 (data_docs) 🆕
│   ├── 财报数据 (financial_reports)
│   ├── 公告数据 (announcements)
│   └── 研究报告 (research_reports)
│
└── 实践经验 (practical_experience) ✅
    ├── 策略案例 (strategy_cases)
    ├── 开发经验 (dev_experience)
    └── 问题解决 (solutions)
```

---

## 📁 存储结构

### 目录结构

```
data/kb/
├── technical_docs/
│   ├── joinquant/          # 聚宽文档（已有）
│   ├── subscription/       # 订阅网站文档（新增）
│   ├── open_source/        # 开源项目文档（新增）
│   └── api_docs/           # API文档（新增）
│
├── theoretical_knowledge/
│   ├── books/              # 书籍内容（新增）
│   │   ├── metadata.json   # 书籍元数据
│   │   ├── chapters/       # 章节内容（Markdown）
│   │   └── index/          # 索引文件
│   ├── papers/             # 学术论文（新增）
│   │   ├── metadata.json   # 论文元数据
│   │   ├── content/        # 论文内容
│   │   └── citations/      # 引用关系
│   └── reports/            # 行业报告（新增）
│
├── data_docs/
│   ├── financial_reports/  # 财报数据（新增）
│   │   ├── raw/            # 原始PDF/Excel
│   │   ├── extracted/      # 提取的结构化数据
│   │   └── metadata.json   # 财报元数据
│   ├── announcements/      # 公告数据（已有部分）
│   └── research_reports/   # 研究报告（新增）
│
└── practical_experience/   # 实践经验（已有部分）
    ├── strategy_cases/
    ├── dev_experience/
    └── solutions/
```

### 元数据格式

#### 书籍元数据 (books/metadata.json)

```json
{
  "books": [
    {
      "id": "book_001",
      "title": "书籍标题",
      "author": "作者",
      "isbn": "ISBN号",
      "publish_date": "2024-01-01",
      "publisher": "出版社",
      "language": "zh/en",
      "tags": ["量化", "投资"],
      "chapters": [
        {
          "chapter_id": "ch_001",
          "title": "第一章",
          "file_path": "chapters/ch_001.md",
          "page_range": "1-50"
        }
      ],
      "created_at": "2026-01-03T10:00:00",
      "updated_at": "2026-01-03T10:00:00"
    }
  ]
}
```

#### 论文元数据 (papers/metadata.json)

```json
{
  "papers": [
    {
      "id": "paper_001",
      "title": "论文标题",
      "authors": ["作者1", "作者2"],
      "journal": "期刊名称",
      "year": 2024,
      "doi": "DOI号",
      "arxiv_id": "arXiv:xxxx.xxxxx",
      "tags": ["量化", "因子"],
      "abstract": "摘要",
      "citations": ["paper_002", "paper_003"],
      "file_path": "content/paper_001.md",
      "created_at": "2026-01-03T10:00:00"
    }
  ]
}
```

#### 财报元数据 (financial_reports/metadata.json)

```json
{
  "reports": [
    {
      "id": "report_001",
      "stock_code": "000001",
      "stock_name": "平安银行",
      "report_type": "annual",  # annual/quarterly
      "report_date": "2024-12-31",
      "publish_date": "2025-03-15",
      "source": "cninfo",  # cninfo/eastmoney
      "raw_file": "raw/report_001.pdf",
      "extracted_file": "extracted/report_001.json",
      "key_metrics": {
        "revenue": 1000000000,
        "net_profit": 100000000
      },
      "created_at": "2026-01-03T10:00:00"
    }
  ]
}
```

---

## 🔍 索引策略

### 多级索引

1. **文档级索引**: 整篇文档的向量表示
2. **章节级索引**: 书籍章节、论文章节的向量表示
3. **段落级索引**: 段落的向量表示（用于精确检索）

### 索引实现

```python
# 使用现有知识库向量搜索功能
# 扩展支持多级索引

索引结构:
{
  "document_level": {
    "doc_id": "vector_embedding"
  },
  "chapter_level": {
    "doc_id_chapter_id": "vector_embedding"
  },
  "paragraph_level": {
    "doc_id_chapter_id_para_id": "vector_embedding"
  }
}
```

### 语义搜索优化

- **Embedding模型选择**: 
  - 中文: `text2vec-chinese` 或 `m3e-base`
  - 英文: `sentence-transformers/all-MiniLM-L6-v2`
- **混合搜索**: 向量搜索 + 关键词搜索
- **重排序**: 使用更强大的模型对搜索结果重排序

---

## 📊 数据流程

### 数据采集流程

```
1. 爬虫/采集
   ↓
2. 原始数据存储 (raw/)
   ↓
3. 数据解析和提取
   ↓
4. 结构化数据存储 (extracted/)
   ↓
5. 元数据生成 (metadata.json)
   ↓
6. 向量索引构建
   ↓
7. 知识库更新
```

### 数据访问流程

```
用户查询
   ↓
关键词提取 + 向量化
   ↓
多级索引搜索
   ↓
结果合并和重排序
   ↓
返回结果（文档 + 摘要 + 元数据）
```

---

## 🔧 技术方案

### 数据解析

- **PDF解析**: 
  - `PyPDF2`: 基础PDF解析
  - `pdfplumber`: 表格提取
  - `pypdf`: 现代化PDF处理
- **OCR支持**: 
  - `Tesseract`: OCR引擎
  - `paddleocr`: 中文OCR（可选）
- **Excel解析**: 
  - `pandas`: Excel文件读取
  - `openpyxl`: Excel处理

### 向量化

- **现有系统**: 使用现有知识库向量搜索
- **模型选择**: 根据内容类型选择合适模型
- **批量处理**: 支持批量向量化

### 存储

- **文件系统**: JSON文件存储元数据
- **向量索引**: 使用现有向量索引系统
- **数据库（可选）**: MongoDB用于大规模数据

---

## 📝 实施计划

### Phase 1: 架构设计 ✅
- [x] 设计目录结构
- [x] 定义元数据格式
- [x] 设计索引策略

### Phase 2: 订阅网站爬虫
- [ ] 实现爬虫框架
- [ ] 支持登录认证
- [ ] 增量爬取

### Phase 3: 书本信息收集
- [ ] PDF解析
- [ ] OCR支持
- [ ] 结构化提取
- [ ] 元数据管理

### Phase 4: 财报信息收集增强
- [ ] 完善cninfo爬虫
- [ ] 完善eastmoney爬虫
- [ ] 财报解析
- [ ] 数据提取

### Phase 5: 研究报告爬虫
- [ ] PDF/HTML解析
- [ ] 引用关系提取
- [ ] 关键词提取
- [ ] 分类标注

### Phase 6: 索引和搜索优化
- [ ] 多级索引实现
- [ ] 语义搜索优化
- [ ] 混合搜索
- [ ] 重排序

### Phase 7: 管理工具开发
- [ ] MCP工具扩展
- [ ] 管理脚本
- [ ] 质量检查

---

## 🔗 相关文件

- 知识库服务器: `mcp_servers/kb_server.py`
- 爬虫框架: `mcp_servers/crawlers/`
- 现有知识库: `data/kb/`
- 聚宽知识库: `docs/joinquant_kb_comprehensive/`

---

*创建时间: 2026-01-03*





