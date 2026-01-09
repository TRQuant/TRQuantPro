# PTrade API文档爬取总结

## 📊 爬取结果

### 总体统计

- **HTML页面**: 5个（已爬取）
  - `index.html` - 首页
  - `stra.html` - 策略代码
  - `trade.html` - 交易
  - `data.html` - 数据
  - `help.html` - 帮助

- **锚点内容块**: 161个（已提取并存入知识库）
  - 成功存入: 161个
  - 失败: 0个
  - 重复跳过: 0个

### 知识库条目

所有161个锚点内容块已成功存入RAG知识库，包括：

- API函数文档（如 `get_price`, `order`, `get_positions` 等）
- 策略开发指南
- 交易相关API
- 数据获取API
- 定时任务配置
- 回测相关功能
- 其他PTrade平台功能

## 📁 生成的文件

### 脚本文件

1. `scripts/crawl_ptrade_api_docs.py` - 主爬取脚本（爬取HTML页面）
2. `scripts/crawl_ptrade_anchor_sections.py` - 锚点内容提取脚本

### 数据文件

- `docs/ptrade_crawled/sidebar_links.json` - 侧栏链接列表（221个链接）
- `docs/ptrade_crawled/real_pages.json` - 真实页面列表（5个）
- `docs/ptrade_crawled/page_*.json` - 已爬取的HTML页面内容（47个）
- `docs/ptrade_crawled/section_*.json` - 锚点内容块（161个）
- `docs/ptrade_crawled/anchor_content_hashes.json` - 内容哈希（用于去重）
- `docs/ptrade_crawled/anchor_crawl.log` - 爬取日志

## 🔍 知识库标签

所有知识库条目都包含以下标签：

- `PTrade` - 平台标识
- `API文档` - 文档类型
- `量化交易` - 领域分类

根据内容自动添加的标签：

- `API接口` - API相关
- `交易` - 交易相关
- `数据` - 数据相关
- `委托下单` - 委托相关
- `持仓查询` - 持仓相关
- `财务数据` - 财务相关
- `历史数据` - 历史数据相关
- `定时任务` - 定时任务相关
- `策略开发` - 策略开发相关
- `回测` - 回测相关

## 📋 使用方法

### 搜索PTrade API文档

在Cursor Chat中使用知识库搜索：

```
请搜索PTrade API中关于订单委托的函数
```

或使用MCP工具：

```python
from mcp_servers.unified_dev_server import knowledge_search

results = knowledge_search("PTrade order API", limit=10)
```

### 查看已爬取的页面

```bash
# 查看侧栏链接
cat docs/ptrade_crawled/sidebar_links.json

# 查看真实页面列表
cat docs/ptrade_crawled/real_pages.json

# 查看某个内容块
cat docs/ptrade_crawled/section_*.json | head -1
```

## 🔧 脚本说明

### crawl_ptrade_api_docs.py

**功能**: 爬取PTrade API文档网站的所有HTML页面

**使用方法**:
```bash
python scripts/crawl_ptrade_api_docs.py
```

**特点**:
- 自动提取侧栏链接
- 过滤锚点链接，只爬取真实页面
- 提取页面内容、代码块、API函数
- 自动存入RAG知识库

### crawl_ptrade_anchor_sections.py

**功能**: 从主页面提取所有锚点链接对应的内容块

**使用方法**:
```bash
python scripts/crawl_ptrade_anchor_sections.py
```

**特点**:
- 提取所有带ID的元素作为内容块
- 自动提取标题、内容、代码块
- 智能分类和标签
- 自动存入RAG知识库

## ⚠️ 注意事项

1. **单页应用（SPA）**: PTrade API文档是单页应用，大部分内容通过锚点跳转，需要特殊处理

2. **内容去重**: 使用内容哈希避免重复存储

3. **文件名安全**: 锚点ID中的特殊字符会被替换为下划线

4. **知识库存储**: 所有内容都存入RAG知识库，可以通过 `knowledge_search` 搜索

## 📚 相关文档

- PTrade API官方文档: https://ptradeapi.com/
- 知识库搜索工具: `mcp_servers/unified_dev_server.py:knowledge_search()`
- 知识库添加工具: `mcp_servers/unified_dev_server.py:knowledge_add()`

## 🎯 下一步

1. ✅ 已完成：爬取HTML页面（5个）
2. ✅ 已完成：提取锚点内容块（161个）
3. ✅ 已完成：存入RAG知识库（161个条目）
4. 🔄 可选：验证知识库搜索功能
5. 🔄 可选：补充其他PTrade相关文档

---

**生成时间**: 2026-01-09  
**脚本版本**: v1.0  
**状态**: ✅ 完成
