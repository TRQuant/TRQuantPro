# 知识库构建 - 完整爬虫工具列表

> **更新**: 2026-01-12  
> **目的**: 列出所有可用于知识库构建的爬虫工具及其使用方式

---

## 📋 工具优先级（AKShare知识库构建脚本）

### 1. ⭐ Playwright (推荐)

**类型**: 直接调用Python库  
**位置**: `playwright.async_api`  
**特点**:
- ✅ 最快、最可靠
- ✅ 支持JavaScript渲染
- ✅ 自动等待页面加载（networkidle）
- ✅ 支持多浏览器（Chromium、Firefox、WebKit）

**使用方式**:
```python
from playwright.async_api import async_playwright
import asyncio

async def fetch():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle', timeout=60000)
        html = await page.content()
        await browser.close()
        return html

html = asyncio.run(fetch())
```

**安装**:
```bash
pip install playwright
playwright install chromium
```

---

### 2. OpenManus

**类型**: MCP工具或直接调用  
**位置**: 
- MCP工具: `browser_use` (如果OpenManus MCP服务器已配置)
- 直接调用: `scripts/openmanus_browser_tool.py`

**特点**:
- ✅ 智能浏览器工具
- ✅ 支持复杂交互
- ✅ 支持内容提取
- ✅ 基于browser-use库

**使用方式**:

**方式1: MCP工具**
```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='browser_use',
    arguments={
        'action': 'go_to_url',
        'url': url
    }
)
```

**方式2: 直接调用**
```python
from scripts.openmanus_browser_tool import OpenManusBrowserTool
import asyncio

async def fetch():
    tool = OpenManusBrowserTool(headless=True)
    result = await tool.navigate(url)
    content = await tool.extract_content()
    await tool.close()
    return content

content = asyncio.run(fetch())
```

---

### 3. MCP工具 - 基础爬虫

**类型**: MCP工具  
**位置**: `mcp_servers/unified_dev_server.py`  
**工具名**: `crawler.fetch`

**特点**:
- ✅ 最快（适合静态内容）
- ✅ 使用requests + BeautifulSoup
- ⚠️ 不支持JavaScript渲染

**使用方式**:
```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='crawler.fetch',
    arguments={
        'url': url,
        'extract_text': True,
        'extract_links': True
    }
)
```

---

### 4. MCP工具 - Selenium

**类型**: MCP工具  
**位置**: `mcp_servers/unified_dev_server.py`  
**工具名**: `crawler.selenium.fetch`

**特点**:
- ✅ 支持JavaScript渲染
- ✅ 支持真实浏览器
- ⚠️ 速度较慢
- ⚠️ 资源消耗大

**使用方式**:
```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='crawler.selenium.fetch',
    arguments={
        'url': url,
        'wait_time': 10,
        'wait_selector': 'body',
        'headless': True
    }
)
```

---

### 5. MCP工具 - Lavague AI

**类型**: MCP工具  
**位置**: `mcp_servers/unified_dev_server.py`  
**工具名**: `crawler.lavague.execute`, `crawler.lavague.extract`

**特点**:
- ✅ AI驱动的浏览器自动化
- ✅ 可以理解自然语言指令
- ✅ 智能提取数据

**使用方式**:
```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='crawler.lavague.extract',
    arguments={
        'description': '提取页面所有文本内容',
        'url': url
    }
)
```

---

### 6. Cursor浏览器工具（基于Playwright）

**类型**: Cursor内置MCP工具  
**位置**: `cursor-ide-browser` MCP服务器  
**工具列表**:
- `browser_navigate` - 导航到URL
- `browser_snapshot` - 获取页面快照
- `browser_click` - 点击元素
- `browser_type` - 输入文本
- `browser_take_screenshot` - 截图
- 等等...

**特点**:
- ✅ 已集成到Cursor IDE
- ✅ 可以直接在Cursor Chat中使用
- ✅ 支持所有Playwright功能
- ✅ AI可以理解页面结构

**使用方式**:
```
在Cursor Chat中直接使用:
"请使用browser_navigate工具访问 https://akshare.akfamily.xyz/"
"请使用browser_snapshot工具获取页面快照"
```

---

## 🎯 工具选择建议

### 对于AKShare文档爬取

**推荐顺序**:
1. **Playwright** - 最快、最可靠
2. **OpenManus** - 智能提取（如果需要复杂交互）
3. **MCP Selenium** - 回退方案
4. **MCP基础爬虫** - 静态内容

### 对于交互式浏览

**推荐**: Cursor浏览器工具（`browser_navigate` + `browser_snapshot`）

### 对于批量爬取

**推荐**: Playwright脚本或MCP工具

---

## 📊 工具对比表

| 工具 | 类型 | JavaScript支持 | 速度 | 资源消耗 | 推荐场景 |
|------|------|----------------|------|----------|----------|
| Playwright | Python库 | ✅ | ⭐⭐⭐⭐⭐ | 中 | 批量爬取、动态页面 |
| OpenManus | MCP/直接调用 | ✅ | ⭐⭐⭐⭐ | 中 | 智能提取、复杂交互 |
| MCP基础爬虫 | MCP工具 | ❌ | ⭐⭐⭐⭐⭐ | 低 | 静态页面 |
| MCP Selenium | MCP工具 | ✅ | ⭐⭐⭐ | 高 | 动态页面（回退） |
| MCP Lavague | MCP工具 | ✅ | ⭐⭐⭐ | 中 | 智能提取 |
| Cursor浏览器 | Cursor内置 | ✅ | ⭐⭐⭐⭐ | 中 | 交互式浏览 |

---

## 🔧 在AKShare知识库构建脚本中的实现

脚本 `scripts/kb/build_kb_akshare.py` 实现了智能工具选择：

```python
def fetch_with_best_tool(url: str) -> Dict[str, Any]:
    """使用最佳工具抓取页面"""
    # 1. 优先使用Playwright
    result = fetch_with_playwright(url)
    if result.get('success'):
        return result
    
    # 2. 尝试OpenManus
    result = fetch_with_openmanus(url)
    if result.get('success'):
        return result
    
    # 3. 尝试MCP工具
    # ...
    
    # 4. 回退到直接函数调用
    # ...
```

**特点**:
- ✅ 自动选择最佳工具
- ✅ 支持多层回退
- ✅ 记录使用的工具（便于调试）

---

## 📝 相关文档

- [标准知识库构建流程](./STANDARD_KB_BUILD_PROCESS.md)
- [AKShare知识库构建总结](./AKSHARE_KB_BUILD_SUMMARY.md)
- [Playwright工具位置说明](../ptrade_crawled/PLAYWRIGHT_TOOLS_LOCATION.md)
- [爬虫工具总结](../ptrade_crawled/CRAWLER_TOOLS_SUMMARY.md)

---

**最后更新**: 2026-01-12  
**维护者**: TRQuant Team
