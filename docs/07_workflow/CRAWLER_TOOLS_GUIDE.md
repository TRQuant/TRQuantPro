# 开源爬虫工具使用指南

> **更新时间**: 2025-12-19  
> **用途**: 高效爬取聚宽API文档，无需每次开发脚本

---

## 🛠️ 推荐工具

### 1. Playwright ⭐ 推荐

**特点**:
- ✅ 支持JavaScript渲染
- ✅ 比Selenium更快
- ✅ 支持多浏览器（Chromium、Firefox、WebKit）
- ✅ 自动等待页面加载
- ✅ 简单易用

**安装**:
```bash
pip install playwright
playwright install chromium
```

**使用示例**:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.joinquant.com/help/api/help?name=api')
    page.wait_for_timeout(3000)  # 等待JS加载
    html = page.content()
    browser.close()
```

**适用场景**: JavaScript渲染页面（如聚宽API文档）

---

### 2. Scrapy

**特点**:
- ✅ 大规模爬取
- ✅ 高性能
- ✅ 丰富的中间件和扩展
- ✅ 内置去重、重试等机制

**安装**:
```bash
pip install scrapy
```

**使用示例**:
```python
import scrapy

class JoinQuantSpider(scrapy.Spider):
    name = 'joinquant'
    start_urls = ['https://www.joinquant.com/help/api/help?name=api']
    
    def parse(self, response):
        # 解析页面
        yield {'url': response.url, 'text': response.text}
```

**适用场景**: 大规模、结构化爬取

**注意**: 处理JS需要配合Splash或Selenium

---

### 3. Selenium

**特点**:
- ✅ 支持JavaScript渲染
- ✅ 支持真实浏览器
- ✅ 功能强大

**缺点**:
- ⚠️ 速度较慢
- ⚠️ 资源消耗大

**安装**:
```bash
pip install selenium
# 需要下载浏览器驱动
```

**适用场景**: 需要真实浏览器交互的场景

---

### 4. Crawlee

**特点**:
- ✅ 支持JavaScript和Python
- ✅ 内置反爬虫机制
- ✅ 支持多种数据源

**安装**:
```bash
npm install crawlee
# 或
pip install crawlee
```

**适用场景**: 需要处理复杂反爬虫的网站

---

### 5. 易采集（EasySpider）

**特点**:
- ✅ 可视化、零代码
- ✅ 适合非技术人员
- ✅ 支持定时任务

**适用场景**: 非技术人员、简单爬取任务

---

## 📊 工具对比

| 工具 | JavaScript支持 | 速度 | 易用性 | 适用场景 |
|------|---------------|------|--------|----------|
| **Playwright** | ✅ 优秀 | ⚡ 快 | ⭐⭐⭐⭐⭐ | JS渲染页面（推荐） |
| **Scrapy** | ⚠️ 需配合 | ⚡⚡⚡ 很快 | ⭐⭐⭐ | 大规模爬取 |
| **Selenium** | ✅ 支持 | 🐌 慢 | ⭐⭐⭐ | 真实浏览器交互 |
| **Crawlee** | ✅ 支持 | ⚡ 快 | ⭐⭐⭐⭐ | 复杂反爬虫 |
| **EasySpider** | ✅ 支持 | ⚡ 快 | ⭐⭐⭐⭐⭐ | 可视化爬取 |

---

## 🎯 针对聚宽文档的推荐方案

### 方案1: Playwright（推荐）⭐

**优点**:
- 完美处理JavaScript渲染
- 速度快
- 代码简单

**实现**:
```python
from playwright.sync_api import sync_playwright

def crawl_joinquant_docs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        urls = [
            'https://www.joinquant.com/help/api/help?name=api',
            'https://www.joinquant.com/help/api/help?name=JQData',
            # ... 更多URL
        ]
        
        for url in urls:
            page.goto(url, wait_until='networkidle')
            page.wait_for_timeout(3000)
            html = page.content()
            # 保存或处理
            save_page(url, html)
        
        browser.close()
```

---

### 方案2: Scrapy + Playwright

**优点**:
- 结合Scrapy的框架优势
- Playwright处理JS

**实现**:
```python
# 使用scrapy-playwright插件
pip install scrapy-playwright

# 在Scrapy中使用
from scrapy_playwright.page import PageMethod

class JoinQuantSpider(scrapy.Spider):
    def start_requests(self):
        yield scrapy.Request(
            url='https://www.joinquant.com/help/api/help?name=api',
            meta={
                'playwright': True,
                'playwright_page_methods': [
                    PageMethod('wait_for_timeout', 3000),
                ],
            }
        )
```

---

## 🚀 快速开始

### 1. 安装Playwright

```bash
cd /home/taotao/dev/QuantTest/TRQuant
source venv/bin/activate
pip install playwright
playwright install chromium
```

### 2. 运行增强版爬虫

```bash
python scripts/crawl_joinquant_docs_enhanced.py
```

### 3. 查看结果

```bash
ls -lh docs/joinquant_crawled/
cat docs/joinquant_crawled/summary_enhanced.md
```

---

## 📝 已实现的增强版脚本

**文件**: `scripts/crawl_joinquant_docs_enhanced.py`

**特性**:
- ✅ 自动检测Playwright是否可用
- ✅ 优先使用Playwright处理JS页面
- ✅ 回退到requests处理简单页面
- ✅ 自动提取链接并继续爬取
- ✅ 保存完整结果

**使用**:
```bash
# 确保已安装Playwright
pip install playwright
playwright install chromium

# 运行
python scripts/crawl_joinquant_docs_enhanced.py
```

---

## 🔧 进阶使用

### 批量爬取所有API文档

```python
from playwright.sync_api import sync_playwright
import json

def crawl_all_api_docs():
    base_url = "https://www.joinquant.com/help/api/doc"
    
    # 获取所有文档ID（从sitemap或索引页）
    doc_ids = range(9800, 11000)  # 示例范围
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        results = {}
        for doc_id in doc_ids:
            url = f"{base_url}?name=JQDatadoc&id={doc_id}"
            try:
                page.goto(url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(2000)
                html = page.content()
                # 解析并保存
                results[doc_id] = parse_doc(html)
            except:
                continue
        
        browser.close()
        return results
```

---

## 📚 参考资源

- [Playwright文档](https://playwright.dev/python/)
- [Scrapy文档](https://docs.scrapy.org/)
- [Selenium文档](https://www.selenium.dev/documentation/)
- [Crawlee文档](https://crawlee.dev/)

---

## ✅ 总结

**推荐使用Playwright**:
- ✅ 完美处理JavaScript渲染
- ✅ 速度快、易用
- ✅ 适合聚宽文档爬取

**已提供增强版脚本**:
- `scripts/crawl_joinquant_docs_enhanced.py`
- 自动使用Playwright处理JS页面
- 无需每次开发新脚本

---

*文档版本: 1.0 | 创建时间: 2025-12-19*

