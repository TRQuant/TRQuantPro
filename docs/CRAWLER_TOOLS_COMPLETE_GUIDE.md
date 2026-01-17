# TRQuant 爬虫工具完整指南

> **版本**: v1.0  
> **更新**: 2026-01-16  
> **目的**: 所有爬虫工具和辅助功能的完整说明、测试结果和使用指南

---

## 📊 爬虫工具概览

### 工具分类统计

| 类别 | 数量 | 工具列表 |
|------|------|----------|
| **基础爬虫工具** | 5个 | fetch, search_docs, download, extract_code, api_docs |
| **Selenium工具** | 3个 | fetch, click, extract |
| **Lavague AI工具** | 2个 | execute, extract |
| **专用爬虫** | 4个 | CninfoCrawler, EastmoneyCrawler, BidCrawler, JobCrawler |
| **辅助工具** | 3个 | CrawlerIntegration, EventProcessor, DataPipeline |
| **总计** | **17个** | 完整的爬虫工具生态系统 |

---

## 🔧 1. 基础爬虫工具（5个）

### 1.1 `crawler.fetch` - 抓取网页内容

**功能**: 使用requests + BeautifulSoup抓取静态网页

**参数**:
- `url` (必需): 网页URL
- `extract_text` (可选, 默认True): 是否提取文本
- `extract_links` (可选, 默认False): 是否提取链接

**使用示例**:
```python
from mcp_servers.unified_dev_server import crawler_fetch

result = crawler_fetch(
    url="https://www.example.com",
    extract_text=True,
    extract_links=False
)
```

**限制**: 不支持JavaScript渲染的动态内容

**依赖**: `requests`, `beautifulsoup4`

---

### 1.2 `crawler.search_docs` - 搜索文档

**功能**: 使用DuckDuckGo搜索文档

**参数**:
- `query` (必需): 搜索关键词
- `site` (可选): 限制搜索站点

**使用示例**:
```python
from mcp_servers.unified_dev_server import crawler_search_docs

result = crawler_search_docs(
    query="Python requests",
    site=None
)
```

**依赖**: `duckduckgo-search`

---

### 1.3 `crawler.download` - 下载文件

**功能**: 下载文件到本地

**参数**:
- `url` (必需): 文件URL
- `filename` (可选): 保存文件名

**使用示例**:
```python
from mcp_servers.unified_dev_server import crawler_download

result = crawler_download(
    url="https://example.com/file.pdf",
    filename="downloaded_file.pdf"
)
```

**依赖**: `requests`

---

### 1.4 `crawler.extract_code` - 提取代码块

**功能**: 从网页提取代码块

**参数**:
- `url` (必需): 网页URL
- `language` (可选): 代码语言（如"python", "javascript"）

**使用示例**:
```python
from mcp_servers.unified_dev_server import crawler_extract_code

result = crawler_extract_code(
    url="https://github.com/scrapy/scrapy",
    language="python"
)
```

**依赖**: `requests`, `beautifulsoup4`

---

### 1.5 `crawler.api_docs` - 获取API文档

**功能**: 获取API文档（从官方文档网站）

**参数**:
- `api_name` (必需): API名称（如"requests.get"）
- `framework` (可选, 默认"python"): 框架类型

**使用示例**:
```python
from mcp_servers.unified_dev_server import crawler_api_docs

result = crawler_api_docs(
    api_name="requests.get",
    framework="python"
)
```

**依赖**: `requests`, `beautifulsoup4`

---

## 🌐 2. Selenium爬虫工具（3个）

### 2.1 `crawler.selenium.fetch` - 抓取动态网页

**功能**: 使用Selenium抓取JavaScript渲染的动态网页

**参数**:
- `url` (必需): 网页URL
- `wait_time` (可选, 默认3): 等待时间（秒）
- `wait_selector` (可选): 等待元素选择器（CSS选择器）
- `headless` (可选, 默认True): 是否无头模式

**使用示例**:
```python
from mcp_servers.unified_dev_server import crawler_selenium_fetch

result = crawler_selenium_fetch(
    url="https://www.example.com",
    wait_time=3,
    wait_selector=".content",
    headless=True
)
```

**依赖**: `selenium`, `webdriver-manager`

**浏览器支持**: Chrome, Firefox

---

### 2.2 `crawler.selenium.click` - 点击元素

**功能**: 使用Selenium点击页面元素

**参数**:
- `selector` (必需): 元素选择器
- `by` (可选, 默认"css"): 选择器类型（css, id, xpath, class, name）

**使用示例**:
```python
from mcp_servers.unified_dev_server import crawler_selenium_click

result = crawler_selenium_click(
    selector="#login-button",
    by="css"
)
```

**依赖**: `selenium`

---

### 2.3 `crawler.selenium.extract` - 提取元素

**功能**: 使用Selenium提取页面元素

**参数**:
- `selector` (必需): 元素选择器
- `attribute` (可选): 要提取的属性（如"text", "href"）

**使用示例**:
```python
from mcp_servers.unified_dev_server import crawler_selenium_extract

result = crawler_selenium_extract(
    selector=".price",
    attribute="text"
)
```

**依赖**: `selenium`

---

## 🤖 3. Lavague AI爬虫工具（2个）

### 3.1 `crawler.lavague.execute` - AI执行自然语言指令

**功能**: 使用Lavague AI执行自然语言指令（如"点击登录按钮"、"填写表单"）

**参数**:
- `instruction` (必需): 自然语言指令
- `url` (可选): 目标URL
- `max_actions` (可选, 默认10): 最大执行动作数
- `headless` (可选, 默认True): 是否无头模式

**使用示例**:
```python
from mcp_servers.unified_dev_server import crawler_lavague_execute

result = crawler_lavague_execute(
    instruction="点击登录按钮，填写用户名和密码",
    url="https://www.example.com/login",
    max_actions=10,
    headless=True
)
```

**依赖**: `lavague`, `selenium`

**特点**: 
- ✅ AI理解自然语言指令
- ✅ 自动识别页面元素
- ✅ 支持复杂交互流程

---

### 3.2 `crawler.lavague.extract` - AI提取数据

**功能**: 使用Lavague AI提取数据（基于自然语言描述）

**参数**:
- `description` (必需): 数据描述（如"提取所有价格"）
- `url` (可选): 目标URL

**使用示例**:
```python
from mcp_servers.unified_dev_server import crawler_lavague_extract

result = crawler_lavague_extract(
    description="提取所有股票价格",
    url="https://www.example.com/stocks"
)
```

**依赖**: `lavague`, `selenium`

---

## 🎯 4. 专用爬虫（4个）

### 4.1 CninfoCrawler - 巨潮资讯网爬虫

**功能**: 爬取上市公司公告

**位置**: `mcp_servers/crawlers/cninfo_crawler.py`

**主要方法**:
- `fetch_announcements()` - 获取公告列表
  - `stock_code`: 股票代码
  - `ann_type`: 公告类型
  - `start_date`: 开始日期
  - `end_date`: 结束日期
  - `page`: 页码

**使用示例**:
```python
from mcp_servers.crawlers.cninfo_crawler import get_cninfo_crawler

crawler = get_cninfo_crawler()
announcements = crawler.fetch_announcements(
    stock_code="000001",
    ann_type="年报",
    start_date="2024-01-01",
    end_date="2024-12-31",
    page=1
)
```

**MCP工具**: `crawler.cninfo.fetch`

---

### 4.2 EastmoneyCrawler - 东方财富网爬虫

**功能**: 爬取公告和研报

**位置**: `mcp_servers/crawlers/eastmoney_crawler.py`

**主要方法**:
- `fetch_announcements()` - 获取公告列表
- `fetch_research_reports()` - 获取研报列表

**使用示例**:
```python
from mcp_servers.crawlers.eastmoney_crawler import get_eastmoney_crawler

crawler = get_eastmoney_crawler()
announcements = crawler.fetch_announcements(
    stock_code="000001",
    days=30,
    page=1
)
reports = crawler.fetch_research_reports(
    stock_code="000001",
    page=1
)
```

**MCP工具**: `crawler.eastmoney.fetch`, `crawler.eastmoney.research`

---

### 4.3 BidCrawler - 招标中标数据爬虫

**功能**: 爬取招标中标数据

**位置**: `mcp_servers/crawlers/bid_crawler.py`

**主要方法**:
- `fetch_bids()` - 获取招标数据
  - `keyword`: 关键词
  - `region`: 地区
  - `page`: 页码
  - `page_size`: 每页数量

**使用示例**:
```python
from mcp_servers.crawlers.bid_crawler import get_bid_crawler

crawler = get_bid_crawler()
bids = crawler.fetch_bids(
    keyword="软件",
    region="北京",
    page=1,
    page_size=20
)
```

**MCP工具**: `crawler.bid.fetch`

---

### 4.4 JobCrawler - 招聘数据爬虫

**功能**: 爬取招聘数据

**位置**: `mcp_servers/crawlers/job_crawler.py`

**主要方法**:
- `fetch_jobs()` - 获取招聘信息
- `get_company_hiring_trend()` - 获取公司招聘趋势

**使用示例**:
```python
from mcp_servers.crawlers.job_crawler import get_job_crawler

crawler = get_job_crawler()
jobs = crawler.fetch_jobs(
    company_name="腾讯",
    job_type="Python开发",
    page=1
)
trend = crawler.get_company_hiring_trend(
    stock_code="00700",
    days=30
)
```

**MCP工具**: `crawler.job.fetch`, `crawler.job.trend`

---

## 🛠️ 5. 辅助工具（3个）

### 5.1 CrawlerIntegration - 爬虫集成工具

**功能**: 将爬虫数据与核心系统集成（存储到MongoDB）

**位置**: `mcp_servers/crawlers/crawler_integration.py`

**主要方法**:
- `process_announcements()` - 处理公告数据
- `crawl_and_store()` - 爬取并存储

**数据流**: 爬虫 → RawDoc(MongoDB) → Event提取 → Stage更新

**使用示例**:
```python
from mcp_servers.crawlers.crawler_integration import crawl_and_store

result = crawl_and_store(
    source="cninfo",
    stock_code="000001",
    page_size=10
)
```

---

### 5.2 EventProcessor - 事件处理器

**功能**: 从文档中提取事件（如业绩预告、重大合同等）

**位置**: `mcp_servers/crawlers/event_processor.py`

**主要方法**:
- `process_new_docs()` - 处理新文档
- `extract_events()` - 提取事件

**使用示例**:
```python
from mcp_servers.crawlers.event_processor import process_new_docs

result = process_new_docs(
    source="cninfo",
    days=7
)
```

---

### 5.3 DataPipeline - 数据管道

**功能**: 端到端数据管道（爬虫 → RawDoc → Event → Stage → Tenbagger评估）

**位置**: `mcp_servers/crawlers/pipeline.py`

**主要方法**:
- `run_full_pipeline()` - 执行完整管道

**使用示例**:
```python
from mcp_servers.crawlers.pipeline import run_pipeline

result = run_pipeline(
    source="cninfo",
    page_size=10
)
```

---

## 📋 6. 爬虫注册系统

### 功能

所有爬虫都继承自`BaseCrawler`基类，并可以通过注册系统统一管理。

**位置**: `mcp_servers/crawlers/base_crawler.py`

**主要函数**:
- `register_crawler()` - 注册爬虫
- `get_crawler()` - 获取爬虫
- `list_crawlers()` - 列出所有已注册的爬虫

**使用示例**:
```python
from mcp_servers.crawlers.base_crawler import list_crawlers, get_crawler

# 列出所有爬虫
crawlers = list_crawlers()
print(f"已注册的爬虫: {crawlers}")

# 获取特定爬虫
crawler = get_crawler("cninfo")
```

---

## 🔍 7. MCP工具集成

### 在unified_dev_server中的集成

所有爬虫工具都通过`unified_dev_server.py`集成到MCP协议中，可以在Cursor Chat中直接使用。

**工具前缀**: `crawler.*`

**可用工具**:
1. `crawler.fetch` - 基础网页抓取
2. `crawler.search_docs` - 搜索文档
3. `crawler.download` - 下载文件
4. `crawler.extract_code` - 提取代码块
5. `crawler.api_docs` - 获取API文档
6. `crawler.selenium.fetch` - Selenium抓取动态网页
7. `crawler.selenium.click` - Selenium点击元素
8. `crawler.selenium.extract` - Selenium提取元素
9. `crawler.lavague.execute` - Lavague AI执行指令
10. `crawler.lavague.extract` - Lavague AI提取数据

**使用方式**:
在Cursor Chat中：
```
"请使用crawler.fetch抓取 https://www.example.com"
"请使用crawler.selenium.fetch抓取动态网页 https://www.example.com"
"请使用crawler.lavague.execute执行指令：点击登录按钮"
```

---

## 📦 8. 依赖安装

### 基础依赖

```bash
pip install requests beautifulsoup4
```

### Selenium依赖

```bash
pip install selenium webdriver-manager
```

### Lavague依赖

```bash
pip install lavague
```

**注意**: Lavague需要配置API密钥（OpenAI或其他LLM服务）

### 完整依赖

```bash
pip install requests beautifulsoup4 selenium webdriver-manager lavague duckduckgo-search
```

---

## 🧪 9. 测试结果

### 测试脚本

位置: `scripts/test_crawlers.py`

**测试内容**:
1. 基础爬虫工具测试（5个）
2. Selenium爬虫工具测试（3个）
3. Lavague AI爬虫工具测试（2个）
4. 专用爬虫测试（4个）
5. 辅助工具测试（3个）
6. 爬虫注册系统测试
7. 依赖检查

**运行测试**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/test_crawlers.py
```

**测试结果文件**: `docs/CRAWLER_TEST_RESULTS.json`

---

## 💡 10. 使用建议

### 选择合适的工具

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| **静态网页** | `crawler.fetch` | 快速、轻量级 |
| **动态网页（JavaScript）** | `crawler.selenium.fetch` | 支持JavaScript渲染 |
| **复杂交互** | `crawler.lavague.execute` | AI理解自然语言指令 |
| **上市公司公告** | `CninfoCrawler` | 专用爬虫，数据准确 |
| **研报数据** | `EastmoneyCrawler` | 专用爬虫，数据丰富 |
| **批量处理** | `DataPipeline` | 端到端自动化 |

### 最佳实践

1. **静态内容优先**: 优先使用`crawler.fetch`，速度快、资源消耗少
2. **动态内容使用Selenium**: 需要JavaScript渲染时使用`crawler.selenium.fetch`
3. **复杂交互使用Lavague**: 需要复杂交互时使用`crawler.lavague.execute`
4. **专用爬虫优先**: 有专用爬虫时优先使用专用爬虫（数据更准确）
5. **批量处理使用管道**: 需要端到端处理时使用`DataPipeline`

---

## ⚠️ 11. 注意事项

### 1. 反爬虫机制

- 使用随机User-Agent
- 添加延迟（delay_range）
- 遵守robots.txt
- 避免过于频繁的请求

### 2. 错误处理

- 所有爬虫都返回`CrawlResult`对象，包含`success`和`error`字段
- 建议使用try-except包装爬虫调用
- 检查返回结果的`success`字段

### 3. 性能优化

- 使用连接池（Session）
- 批量处理数据
- 使用异步爬虫（asyncio）
- 缓存已爬取的数据

### 4. 数据存储

- 使用`CrawlerIntegration`自动存储到MongoDB
- 使用`RawDocStore`存储原始文档
- 使用`EventProcessor`提取事件

---

## 📚 12. 相关文档

- `docs/02_development_guides/WEB_CRAWLER_USAGE.md` - 网络爬虫功能使用指南
- `docs/ptrade_crawled/CRAWLER_TOOLS_SUMMARY.md` - 爬虫工具总结
- `mcp_servers/crawlers/README.md` - 爬虫模块文档（如果有）

---

**最后更新**: 2026-01-16  
**维护者**: TRQuant Team
