# 网络爬虫功能使用指南

## 概述

TRQuant系统提供了多种网络爬虫功能，包括浏览器MCP工具和Python爬虫工具。

## 1. 浏览器MCP工具（推荐）✅

### 已集成的工具

这些工具已经通过MCP协议集成，可以直接在Cursor中使用：

- **`browser_navigate`** - 导航到指定URL
- **`browser_snapshot`** - 获取页面的可访问性快照（用于AI理解页面结构）
- **`browser_click`** - 点击页面元素
- **`browser_type`** - 在输入框中输入文本
- **`browser_take_screenshot`** - 截取页面截图
- **`browser_wait_for`** - 等待特定文本或元素出现
- **`browser_hover`** - 鼠标悬停
- **`browser_select_option`** - 选择下拉选项

### 使用示例

```python
# 1. 导航到网页
browser_navigate(url="https://example.com")

# 2. 获取页面快照（AI可理解的页面结构）
browser_snapshot()

# 3. 点击元素
browser_click(element="登录按钮", ref="ref-xxx")

# 4. 输入文本
browser_type(element="搜索框", ref="ref-xxx", text="搜索内容")

# 5. 截图
browser_take_screenshot(filename="page.png", fullPage=True)
```

### 实际演示

刚才已经成功使用浏览器工具爬取了GitHub上的Scrapy项目页面：
- URL: https://github.com/scrapy/scrapy
- 获取了完整的页面快照（2600+行，200KB）
- 可以进一步提取页面内容、点击链接、填写表单等

## 2. Python爬虫工具

### 位置

`extension/python/tools/data_collector/`

### 可用工具

1. **`web_crawler.py`** - 基于requests+BeautifulSoup的网页爬虫
   - 支持多层级爬取
   - 遵守robots.txt
   - 支持代理和重试

2. **`academic_scraper.py`** - 学术论文爬取
   - 支持arXiv API
   - 支持其他学术数据库

3. **`pdf_downloader.py`** - PDF下载工具
   - 批量下载PDF
   - 支持多种来源

4. **`source_recommender.py`** - 数据源推荐
   - 根据需求推荐数据源
   - 评估数据源质量

### 使用示例

```python
from tools.data_collector.web_crawler import WebCrawler
from pathlib import Path

# 创建爬虫实例
crawler = WebCrawler(
    output_dir=Path("data/collected"),
    delay_range=(1, 3),
    respect_robots=True
)

# 爬取网页
files = crawler.collect(
    url="https://example.com",
    max_depth=2,
    allowed_domains=["example.com"]
)
```

## 3. MCP服务器（待实现）

### 当前状态

`mcp_servers/data_collector_server.py` 文件存在但为空，需要实现。

### 建议实现

将Python爬虫工具封装为MCP服务器，提供以下工具：

- `data_collector.crawl` - 爬取网页
- `data_collector.scrape` - 提取特定内容
- `data_collector.download` - 下载文件
- `data_collector.academic` - 爬取学术论文

## 4. 使用场景对比

| 场景 | 推荐工具 | 原因 |
|------|---------|------|
| 快速浏览网页 | 浏览器MCP工具 | 已集成，使用简单 |
| 提取页面内容 | 浏览器MCP工具 | AI可理解页面结构 |
| 批量爬取 | Python爬虫工具 | 性能更好，支持并发 |
| 学术论文 | Python爬虫工具 | 有专门的学术爬虫 |
| 动态网页 | 浏览器MCP工具 | 支持JavaScript渲染 |
| 大规模爬取 | Python爬虫工具 | 更灵活，可定制 |

## 5. 最佳实践

### 使用浏览器MCP工具时

1. **先导航，再快照**
   ```python
   browser_navigate(url="...")
   browser_snapshot()  # 获取页面结构
   ```

2. **使用ref进行精确操作**
   - 从snapshot中获取元素的ref
   - 使用ref而不是文本进行点击/输入

3. **等待页面加载**
   ```python
   browser_wait_for(text="加载完成")
   ```

### 使用Python爬虫工具时

1. **遵守robots.txt**
   ```python
   crawler = WebCrawler(respect_robots=True)
   ```

2. **设置合理的延迟**
   ```python
   crawler = WebCrawler(delay_range=(1, 3))
   ```

3. **使用代理（如需要）**
   ```python
   crawler = WebCrawler(proxy_config={"http": "proxy:port"})
   ```

## 6. 总结

**当前可用的网络爬虫功能：**

✅ **浏览器MCP工具** - 已集成，可直接使用
- 适合：快速浏览、内容提取、交互操作
- 优势：AI可理解、支持JavaScript、使用简单

⚠️ **Python爬虫工具** - 已实现，需要直接调用
- 适合：批量爬取、大规模数据收集
- 优势：性能好、可定制、支持多种场景

⏳ **data_collector_server** - 待实现
- 建议：将Python工具封装为MCP服务器
- 优势：统一接口、便于AI调用

**推荐使用方式：**
- 日常使用：浏览器MCP工具
- 批量任务：Python爬虫工具
- 未来：实现data_collector_server统一接口









