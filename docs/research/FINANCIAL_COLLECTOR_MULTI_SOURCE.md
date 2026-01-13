# FinancialCollector多数据源支持说明

> **更新时间**: 2026-01-11  
> **状态**: ✅ eastmoney已实现，sina/cls待优化

---

## 📋 数据源支持情况

### 新闻数据源

FinancialCollector已配置3个新闻数据源：

1. **eastmoney (东方财富)** ✅ 已实现
   - URL: https://finance.eastmoney.com/a/cywjh.html
   - 状态: ✅ 已实现，稳定可用
   - 解析方式: 通用文本解析

2. **sina (新浪财经)** ⚠️ 已配置但待优化
   - URL: https://finance.sina.com.cn/
   - 状态: ⚠️ 已配置，可用通用解析，但不够精确
   - 解析方式: 通用文本解析（可能需要优化）

3. **cls (财联社)** ⚠️ 已配置但待优化
   - URL: https://www.cls.cn/telegraph
   - 状态: ⚠️ 已配置，可用通用解析，但不够精确
   - 解析方式: 通用文本解析（可能需要优化）

### 公告数据源

1. **eastmoney (东方财富公告)** ✅ 已实现
   - URL: https://data.eastmoney.com/notices/stock/{code}.html
   - 状态: ✅ 已实现

2. **cninfo (巨潮资讯)** ⚠️ 待实现
   - URL: http://www.cninfo.com.cn/new/disclosure
   - 状态: ⚠️ 待实现

---

## 🔍 为什么目前主要使用eastmoney？

### 当前实现方式

`fetch_news` 方法使用**通用文本解析**逻辑 (`_parse_news`)，理论上所有数据源都可以使用：

```python
async def fetch_news(self, source: str = "eastmoney", limit: int = 10):
    """抓取财经新闻"""
    source_config = self.NEWS_SOURCES.get(source)
    url = source_config["url"]
    
    # 1. 访问网页
    nav_result = await browser.navigate(url)
    
    # 2. 获取页面内容
    content_result = await browser.get_content()
    
    # 3. 通用文本解析
    news_items = self._parse_news(content, source, limit)
```

### 解析逻辑

`_parse_news` 使用关键词匹配方式：

```python
def _parse_news(self, content: str, source: str, limit: int):
    """解析新闻内容"""
    news_items = []
    
    lines = content.split()
    for line in lines:
        # 关键词匹配
        if any(kw in line for kw in self.NEWS_KEYWORDS):
            news_items.append(NewsItem(...))
```

**问题**:
- 这种方式对eastmoney比较有效
- 对sina和cls可能不够精确（页面结构不同）
- 需要为每个数据源定制解析逻辑

---

## 🚀 如何使用多个数据源

### 方式1: 手动指定多个数据源

```python
from core.data_collection import FinancialCollector

async with FinancialCollector(headless=True) as collector:
    all_news = []
    
    # 从eastmoney抓取
    result1 = await collector.fetch_news("eastmoney", limit=10)
    if result1.success:
        all_news.extend(result1.data)
    
    # 从sina抓取
    result2 = await collector.fetch_news("sina", limit=10)
    if result2.success:
        all_news.extend(result2.data)
    
    # 从cls抓取
    result3 = await collector.fetch_news("cls", limit=10)
    if result3.success:
        all_news.extend(result3.data)
    
    # 去重
    unique_news = []
    seen_titles = set()
    for news in all_news:
        title = news.get('title', '')
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_news.append(news)
```

### 方式2: 使用演示脚本

```bash
# 实时演示多数据源抓取
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/demo_multi_source_news_live.py
```

### 方式3: 更新投资热点报告脚本

已更新 `scripts/generate_investment_hotspot_report.py`，现在会尝试从多个数据源抓取：

```python
# 从多个数据源抓取
sources = ["eastmoney", "sina", "cls"]
for source in sources:
    news_result = await collector.fetch_news(source, limit=10)
    if news_result.success:
        all_news.extend(news_result.data)
```

---

## 📊 实时演示脚本

### 脚本位置

- **多数据源实时演示**: `scripts/demo_multi_source_news_live.py`
- **单数据源实时演示**: `scripts/demo_financial_collector_live.py`

### 运行方式

```bash
# 多数据源实时演示
./venv/bin/python scripts/demo_multi_source_news_live.py

# 单数据源实时演示
./venv/bin/python scripts/demo_financial_collector_live.py
```

### 演示内容

1. **实时显示抓取进度**
   - 数据源信息
   - 连接状态
   - 抓取进度
   - 耗时统计

2. **多数据源抓取**
   - 从eastmoney、sina、cls抓取
   - 显示每个数据源的结果
   - 汇总统计

3. **结果显示**
   - 每个数据源的新闻数量
   - 新闻列表（前5条）
   - 数据源分布统计

---

## 🔧 优化建议

### 1. 为每个数据源定制解析逻辑

目前所有数据源都使用通用解析，建议为每个数据源定制解析逻辑：

```python
def _parse_news(self, content: str, source: str, limit: int):
    """解析新闻内容（根据数据源选择解析方式）"""
    if source == "eastmoney":
        return self._parse_eastmoney_news(content, limit)
    elif source == "sina":
        return self._parse_sina_news(content, limit)
    elif source == "cls":
        return self._parse_cls_news(content, limit)
    else:
        return self._parse_generic_news(content, limit)
```

### 2. 使用CSS选择器精确提取

不同网站的HTML结构不同，可以使用CSS选择器精确提取：

```python
def _parse_eastmoney_news(self, content: str, limit: int):
    """解析东方财富新闻（使用CSS选择器）"""
    # 使用CSS选择器提取新闻标题
    # 例如: .news-list-item .title
    pass
```

### 3. 使用BeautifulSoup解析HTML

可以使用BeautifulSoup解析HTML结构：

```python
from bs4 import BeautifulSoup

def _parse_eastmoney_news(self, html: str, limit: int):
    """解析东方财富新闻（使用BeautifulSoup）"""
    soup = BeautifulSoup(html, 'html.parser')
    news_items = []
    
    # 查找新闻列表
    news_list = soup.select('.news-list-item')
    for item in news_list[:limit]:
        title = item.select_one('.title')
        url = item.select_one('a')['href']
        # ...
        news_items.append(NewsItem(...))
    
    return news_items
```

---

## 📚 相关文档

- **FinancialCollector**: `core/data_collection/financial_collector.py`
- **多数据源演示**: `scripts/demo_multi_source_news_live.py`
- **单数据源演示**: `scripts/demo_financial_collector_live.py`
- **投资热点报告**: `scripts/generate_investment_hotspot_report.py`

---

## ✅ 当前状态总结

### 已实现

- ✅ eastmoney (东方财富) - 稳定可用
- ✅ 通用文本解析逻辑
- ✅ 多数据源配置
- ✅ 实时演示脚本

### 待优化

- ⚠️ sina (新浪财经) - 需要优化解析逻辑
- ⚠️ cls (财联社) - 需要优化解析逻辑
- ⚠️ cninfo (巨潮资讯) - 公告数据源待实现

### 建议

1. **短期**: 继续使用eastmoney数据源（最稳定）
2. **中期**: 为sina和cls定制解析逻辑
3. **长期**: 支持更多数据源，使用统一的解析框架

---

**文档更新时间**: 2026-01-11  
**维护者**: TRQuant Team
