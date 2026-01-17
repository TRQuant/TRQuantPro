# Playwright智能爬虫工具指南 - 参考LaVague实现

> **创建时间**: 2026-01-17  
> **版本**: v1.0  
> **参考**: LaVague PlaywrightDriver实现

---

## 📋 概述

本工具参考LaVague的PlaywrightDriver实现方式，提供智能浏览器自动化功能，**完全基于Playwright，无需LLM API**。

### 核心特性（参考LaVague）

1. **wait_for_idle** - 等待页面稳定（networkidle + DOM稳定）
2. **智能元素定位** - 支持xpath、css等多种方式
3. **交互操作** - click、fill、scroll等
4. **内容提取** - HTML、文本、截图等

---

## 🎯 与现有功能的整合

### 已有功能

1. **cninfo_crawler.py** ✅
   - 已实现巨潮资讯网公告爬取
   - 使用API方式，速度快
   - 测试成功：可获取603986的28条公告

2. **BrowserAgent** ✅
   - 基于Playwright的浏览器自动化
   - 支持异步操作

3. **SeleniumCrawler** ✅
   - 基于Selenium的爬虫

### 新增功能

1. **PlaywrightSmartCrawler** ✅
   - 参考LaVague实现方式
   - 使用wait_for_idle机制
   - 支持智能元素定位和交互

---

## 🚀 使用方式

### 方式1: 使用现有cninfo工具（推荐，最快）

```python
# 在Cursor Chat中使用
"使用crawler.cninfo.fetch工具，获取股票603986最近90天的所有公告"
```

**优势**:
- ✅ 使用API方式，速度快
- ✅ 无需浏览器，资源消耗低
- ✅ 已测试成功

### 方式2: 使用Playwright智能爬虫（参考LaVague）

```python
from core.crawlers.playwright_smart_crawler import get_playwright_smart_crawler

# 创建爬虫（参考LaVague实现）
crawler = get_playwright_smart_crawler(headless=True)

# 导航到网页（参考LaVague的wait_for_idle机制）
crawler.navigate("http://www.cninfo.com.cn")

# 点击搜索框
crawler.fill("input[type='text']", "603986", enter=True)

# 等待结果加载
crawler.wait_for_idle()

# 提取公告列表
result = crawler.extract_text(".announcement-list")

# 关闭
crawler.close()
```

### 方式3: 使用MCP工具

```python
# 在Cursor Chat中使用
"使用crawler.playwright.navigate工具访问巨潮资讯网"
"使用crawler.playwright.fill工具填写搜索框"
"使用crawler.playwright.extract工具提取公告"
```

---

## 📊 对比：LaVague vs Playwright智能爬虫

| 特性 | LaVague | Playwright智能爬虫 |
|------|---------|-------------------|
| **LLM需求** | ✅ 需要（理解自然语言） | ❌ 不需要 |
| **API密钥** | ✅ 需要 | ❌ 不需要 |
| **wait_for_idle** | ✅ 支持 | ✅ 支持（参考实现） |
| **元素定位** | ✅ 智能（AI驱动） | ✅ 手动（xpath/css） |
| **速度** | ⚠️ 较慢（需要LLM调用） | ✅ 快 |
| **资源消耗** | ⚠️ 高（LLM + 浏览器） | ✅ 低（仅浏览器） |
| **适用场景** | 复杂自然语言任务 | 结构化数据提取 |

---

## 🔧 实现细节（参考LaVague）

### 1. wait_for_idle机制

**LaVague实现**:
```javascript
// 1. 等待networkidle
page.wait_for_load_state("networkidle", timeout=10s)

// 2. 等待DOM稳定（MutationObserver）
JS_WAIT_DOM_IDLE - 监听DOM变化，等待稳定
```

**我们的实现**:
```python
def wait_for_idle(self):
    # 1. 等待网络空闲（参考LaVague）
    self._page.wait_for_load_state("networkidle", timeout=10s)
    
    # 2. 等待DOM稳定（参考LaVague的JS_WAIT_DOM_IDLE）
    self._page.evaluate(JS_WAIT_DOM_IDLE, timeout, stabilityThreshold)
```

### 2. 浏览器配置

**LaVague配置**:
```python
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) ..."
args = [
    "--disable-web-security",
    "--disable-site-isolation-trials",
    "--disable-notifications",
]
```

**我们的配置**:
- ✅ 完全参考LaVague的配置
- ✅ 相同的user_agent
- ✅ 相同的浏览器参数

---

## 📝 完整示例

### 示例：提取股票公告（使用cninfo工具）

```python
# 在Cursor Chat中
"使用crawler.cninfo.fetch工具，获取股票603986最近90天的所有公告"
```

### 示例：使用Playwright智能爬虫

```python
from core.crawlers.playwright_smart_crawler import get_playwright_smart_crawler

crawler = get_playwright_smart_crawler(headless=True)

# 导航到巨潮资讯网
crawler.navigate("http://www.cninfo.com.cn")

# 搜索股票代码
crawler.fill("input.search-input", "603986", enter=True)

# 等待结果加载
crawler.wait_for_idle()

# 提取公告
announcements = crawler.extract_text(".announcement-item")

crawler.close()
```

---

## 🔗 相关文档

- **LaVague PlaywrightDriver**: `/tmp/lavague-source/lavague-integrations/drivers/lavague-drivers-playwright/`
- **LaVague BaseDriver**: `/tmp/lavague-source/lavague-core/lavague/core/base_driver.py`
- **现有cninfo爬虫**: `mcp_servers/crawlers/cninfo_crawler.py`
- **BrowserAgent**: `core/automation/browser_agent.py`

---

## ✅ 总结

1. **已有cninfo_crawler** ✅ - 使用API方式，速度快，已测试成功
2. **新增PlaywrightSmartCrawler** ✅ - 参考LaVague实现，支持智能交互
3. **整合到MCP工具** ✅ - 可通过Cursor Chat直接使用
4. **无需LLM API** ✅ - 完全基于Playwright，无需API密钥

---

**最后更新**: 2026-01-17  
**维护者**: TRQuant Team
