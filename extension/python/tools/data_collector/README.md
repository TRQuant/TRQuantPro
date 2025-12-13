# 数据收集工具

> 整合开源工具，实现知识库数据自动收集

## 📦 已整合的开源工具

### 1. Scrapy - 网页爬虫框架
- **GitHub**: https://github.com/scrapy/scrapy
- **用途**: 大规模网页爬取
- **安装**: `pip install scrapy`

### 2. Beautiful Soup - HTML解析
- **GitHub**: https://github.com/waylan/beautifulsoup4
- **用途**: HTML/XML解析
- **安装**: `pip install beautifulsoup4`

### 3. Playwright - 浏览器自动化
- **GitHub**: https://github.com/microsoft/playwright
- **用途**: 处理动态网页、JavaScript渲染
- **安装**: `pip install playwright && playwright install`

### 4. arXiv API - 学术论文下载
- **官方**: https://arxiv.org/help/api
- **用途**: 下载arXiv论文
- **安装**: `pip install arxiv feedparser`

### 5. PyPDF2/pdfplumber - PDF处理
- **GitHub**: https://github.com/py-pdf/pypdf2
- **用途**: PDF解析和提取
- **安装**: `pip install pypdf2 pdfplumber`

### 6. requests-html - 简单爬虫
- **GitHub**: https://github.com/psf/requests-html
- **用途**: 简单网页爬取
- **安装**: `pip install requests-html`

## 🚀 快速开始

```bash
# 安装所有依赖
pip install -r requirements-collector.txt

# 运行示例
python tools/data_collector/examples/crawl_example.py
```

## 📚 使用示例

### 爬取网页
```python
from tools.data_collector.web_crawler import WebCrawler

crawler = WebCrawler(output_dir="data/collected")
files = crawler.collect("https://example.com")
```

### 下载arXiv论文
```python
from tools.data_collector.academic_scraper import AcademicScraper

scraper = AcademicScraper(output_dir="data/papers")
files = scraper.collect("arxiv", "quantitative+trading", max_results=50)
```

