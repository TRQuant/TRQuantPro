# TRQuant 知识库系统工具集

> **版本**: 1.0  
> **更新日期**: 2026-01-09  
> **来源**: `docs/01_architecture/TRQuant知识库系统实施方案.pdf`

---

## 📋 工具概览

根据PDF方案，已实现完整的知识库系统工具链：

| 工具 | 功能 | 文件 |
|------|------|------|
| **知识库构建器** | 核心构建功能 | `kb_builder.py` |
| **知识库爬虫** | 单URL爬取 | `kb_crawler.py` |
| **批量爬取工具** | 批量爬取多平台 | `kb_batch_crawl.py` |
| **知识库管理器** | 管理操作 | `kb_manager.py` |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装Python依赖
pip install chromadb sentence-transformers playwright beautifulsoup4

# 安装Playwright浏览器
playwright install chromium
```

### 2. 爬取网页并添加到知识库

```bash
# 爬取单个网页
python scripts/kb/kb_crawler.py \
    --url "https://www.joinquant.com/help/api" \
    --platform "JoinQuant" \
    --method "playwright" \
    --build-index

# 批量爬取平台文档
python scripts/kb/kb_batch_crawl.py \
    --platform JoinQuant \
    --build-index
```

### 3. 管理知识库

```bash
# 添加知识条目
python scripts/kb/kb_manager.py add \
    --title "聚宽get_price函数" \
    --content "get_price函数用于获取股票价格数据..." \
    --type "reference" \
    --tags "JoinQuant" "API" \
    --platform "JoinQuant"

# 搜索知识
python scripts/kb/kb_manager.py search \
    --query "如何获取股票价格" \
    --limit 10

# 显示统计
python scripts/kb/kb_manager.py stats

# 构建向量索引
python scripts/kb/kb_manager.py build-index --force

# 清理重复条目
python scripts/kb/kb_manager.py clean
```

---

## 📚 详细文档

- **系统实施方案**: `docs/KB_SYSTEM_IMPLEMENTATION.md`
- **框架详解**: `docs/KB_FRAMEWORK_DETAILS.md`
- **原始方案**: `docs/01_architecture/TRQuant知识库系统实施方案.pdf`

---

## 🔧 工具详解

### 1. kb_builder.py - 知识库构建器

**核心功能**:
- 加载/保存知识库JSON文件
- 添加知识条目（自动生成ID、去重）
- 构建向量索引（ChromaDB）
- 内容清洗和解析（HTML/Markdown/Text）
- 文本分块（语义段落拆分）

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

### 2. kb_crawler.py - 知识库爬虫

**功能**:
- 使用Playwright爬取网页（支持JavaScript渲染）
- 使用MCP工具爬取网页（Selenium）
- 自动处理并保存到知识库
- 支持内容清洗、解析、分块

**命令行参数**:
```bash
--url <URL>           # 目标URL（必需）
--platform <平台>     # 平台名称（可选）
--method <方法>       # 爬取方法：playwright/mcp（默认：playwright）
--build-index         # 爬取后构建向量索引
```

### 3. kb_batch_crawl.py - 批量爬取工具

**功能**:
- 批量爬取多个平台的文档
- 支持平台：JoinQuant、BulletTrade、PTrade、QMT
- 自动统计爬取结果
- 可选构建向量索引

**命令行参数**:
```bash
--platform <平台>     # 平台名称或"all"（默认：all）
--method <方法>       # 爬取方法：playwright/mcp（默认：playwright）
--build-index         # 爬取后构建向量索引
```

**配置平台URL**:
编辑 `kb_batch_crawl.py` 中的 `PLATFORM_URLS` 字典，添加或修改URL列表。

### 4. kb_manager.py - 知识库管理器

**功能**:
- 添加知识条目
- 搜索知识（混合检索）
- 显示统计信息
- 构建向量索引
- 清理重复条目

**命令列表**:
- `add` - 添加知识条目
- `search` - 搜索知识
- `stats` - 显示统计信息
- `build-index` - 构建向量索引
- `clean` - 清理重复条目

---

## 🔍 工作流程

### 完整流程示例

```bash
# 1. 批量爬取平台文档
python scripts/kb/kb_batch_crawl.py --platform JoinQuant --build-index

# 2. 查看统计
python scripts/kb/kb_manager.py stats

# 3. 搜索知识
python scripts/kb/kb_manager.py search --query "get_price函数"

# 4. 清理重复
python scripts/kb/kb_manager.py clean

# 5. 重建索引
python scripts/kb/kb_manager.py build-index --force
```

---

## 📊 数据存储

### 目录结构

```
.trquant/dev/knowledge/
├── knowledge_base.json          # 知识库JSON文件
├── vector_index/                # ChromaDB向量索引
│   ├── index_meta.json          # 索引元数据
│   └── ...                      # ChromaDB数据文件
├── raw_data/                    # 原始数据（爬取的HTML等）
└── processed_data/              # 处理后的数据
```

### 知识库JSON格式

```json
{
  "items": [
    {
      "id": "kb_xxx",
      "title": "标题",
      "content": "内容",
      "type": "reference",
      "tags": ["标签1", "标签2"],
      "source": "来源URL",
      "platform": "平台名称",
      "created_at": "2026-01-09 12:00:00",
      "useful_count": 0,
      "_score": 0
    }
  ],
  "updated_at": "2026-01-09 12:00:00"
}
```

---

## 🔧 技术栈

- **向量数据库**: ChromaDB
- **Embedding模型**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **网页爬虫**: Playwright、Selenium
- **HTML解析**: BeautifulSoup4
- **检索算法**: 混合检索（向量+关键词+RRF）

---

## 💡 最佳实践

### 1. 知识采集

- ✅ 优先抓取官方文档（准确性高）
- ✅ 保留结构信息（标题、代码块、列表）
- ✅ 添加元数据（平台、类型、标签）
- ✅ 定期更新（关注API变更）

### 2. 数据质量

- ✅ 定期清理重复（`kb_manager.py clean`）
- ✅ 验证准确性（随机抽查）
- ✅ 更新过期信息（及时更新）

### 3. 检索优化

- ✅ 使用混合检索（向量+关键词）
- ✅ 调整RRF参数（根据效果）
- ✅ 监控检索质量（记录反馈）

---

## 🐛 故障排查

### 问题1: Playwright未安装

```bash
# 安装Playwright
pip install playwright
playwright install chromium
```

### 问题2: ChromaDB依赖缺失

```bash
# 安装依赖
pip install chromadb sentence-transformers
```

### 问题3: 向量索引构建失败

```bash
# 检查知识库文件是否存在
ls -la .trquant/dev/knowledge/knowledge_base.json

# 强制重建索引
python scripts/kb/kb_manager.py build-index --force
```

---

## 📈 后续计划

- [ ] PDF文档解析支持
- [ ] 自动更新机制
- [ ] 检索质量评估
- [ ] 知识库可视化界面
- [ ] 多语言支持

---

**最后更新**: 2026-01-09
