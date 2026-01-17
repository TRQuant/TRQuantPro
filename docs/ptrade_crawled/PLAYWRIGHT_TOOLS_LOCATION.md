# Playwright工具位置说明

> **生成时间**: 2026-01-09  
> **目的**: 说明Playwright工具的位置和使用方式

---

## 📋 Playwright工具位置

### 1. 浏览器MCP工具（基于Playwright）✅

**位置**: Cursor内置的 `cursor-ide-browser` MCP服务器

**工具列表**:
- `browser_navigate` - 导航到指定URL
- `browser_snapshot` - 获取页面的可访问性快照（用于AI理解页面结构）
- `browser_click` - 点击页面元素
- `browser_type` - 在输入框中输入文本
- `browser_take_screenshot` - 截取页面截图
- `browser_wait_for` - 等待特定文本或元素出现
- `browser_hover` - 鼠标悬停
- `browser_select_option` - 选择下拉选项
- `browser_press_key` - 按键操作
- `browser_navigate_back` - 返回上一页
- `browser_resize` - 调整窗口大小
- `browser_console_messages` - 获取控制台消息
- `browser_network_requests` - 获取网络请求
- `browser_tabs` - 标签页管理

**特点**:
- ✅ 基于Playwright实现
- ✅ 已集成到Cursor IDE
- ✅ 可以直接在Cursor Chat中使用
- ✅ 支持JavaScript渲染的动态页面

**使用方式**:
```python
# 在Cursor Chat中直接使用
"请使用browser_navigate工具访问 https://ptradeapi.com/#新建策略"
"请使用browser_snapshot工具获取页面快照"
```

---

### 2. unified_dev_server中的爬虫工具

**位置**: `mcp_servers/unified_dev_server.py`

**工具列表**:
- `crawler.fetch` - 基础爬虫（requests + BeautifulSoup）
- `crawler.selenium.fetch` - Selenium工具（支持动态页面）
- `crawler.lavague.execute` - Lavague AI工具

**状态**: ⚠️ **没有专门的Playwright MCP工具**

---

### 3. Playwright Python库

**位置**: 已安装在虚拟环境中

**安装路径**:
- `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/playwright`
- `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/lib/python3.12/site-packages/playwright/`

**使用方式**:
```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    await page.goto('https://ptradeapi.com/#新建策略')
    content = await page.content()
    await browser.close()
```

**已使用的脚本**:
- `scripts/crawl_ptrade_api_docs.py` - 使用Playwright爬取PTrade API文档
- `scripts/crawl_ptrade_anchor_sections.py` - 使用Playwright提取锚点内容
- `scripts/crawl_jqdata_complete_with_tools.py` - 使用Playwright爬取JQData文档

---

## 🎯 推荐使用方式

### 方式1: 使用浏览器MCP工具（推荐）✅

**优点**:
- ✅ 已集成，无需额外配置
- ✅ 直接在Cursor Chat中使用
- ✅ 支持所有Playwright功能
- ✅ AI可以理解页面结构

**使用示例**:
```
请使用browser_navigate工具访问 https://ptradeapi.com/#新建策略
然后使用browser_snapshot获取页面快照
```

---

### 方式2: 使用unified_dev_server的爬虫工具

**适用场景**:
- 需要批量爬取
- 需要自动化流程
- 需要存储到知识库

**工具选择**:
- **静态页面**: `crawler.fetch`
- **动态页面**: `crawler.selenium.fetch`
- **智能提取**: `crawler.lavague.extract`

---

### 方式3: 编写Playwright脚本

**适用场景**:
- 复杂的爬取逻辑
- 需要自定义处理
- 批量处理

**示例**:
```python
#!/usr/bin/env python3
from playwright.async_api import async_playwright

async def crawl_page(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        content = await page.content()
        await browser.close()
        return content
```

---

## 📊 工具对比

| 工具 | 基于 | 位置 | 使用方式 | 适用场景 |
|------|------|------|----------|----------|
| `browser_*` | Playwright | cursor-ide-browser | Cursor Chat | 交互式浏览和提取 |
| `crawler.selenium.fetch` | Selenium | unified_dev_server | MCP工具 | 批量爬取动态页面 |
| `crawler.lavague.extract` | Lavague | unified_dev_server | MCP工具 | 智能提取数据 |
| Playwright脚本 | Playwright | Python脚本 | 直接运行 | 复杂自定义逻辑 |

---

## 💡 建议

### 对于PTrade API文档爬取

**推荐**: 使用浏览器MCP工具（`browser_navigate` + `browser_snapshot`）

**原因**:
1. ✅ 已集成，无需配置
2. ✅ 支持JavaScript渲染
3. ✅ AI可以理解页面结构
4. ✅ 可以直接在Cursor Chat中使用

**使用流程**:
```
1. browser_navigate(url="https://ptradeapi.com/#新建策略")
2. browser_wait_for(time=3)  # 等待页面加载
3. browser_snapshot()  # 获取页面快照
4. 从快照中提取需要的内容
```

---

## 🔧 如果需要添加Playwright MCP工具

可以在 `mcp_servers/unified_dev_server.py` 中添加：

```python
def crawler_playwright_fetch(url: str, wait_time: int = 3, headless: bool = True) -> Dict:
    """使用Playwright抓取动态网页"""
    try:
        from playwright.async_api import async_playwright
        import asyncio
        
        async def fetch():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=headless)
                page = await browser.new_page()
                await page.goto(url, wait_until='networkidle', timeout=60000)
                await page.wait_for_timeout(wait_time * 1000)
                
                content = await page.content()
                text = await page.inner_text('body')
                
                await browser.close()
                return {"success": True, "html": content, "text": text}
        
        return asyncio.run(fetch())
    except Exception as e:
        return {"success": False, "error": str(e)}
```

---

## ✅ 总结

1. **Playwright已安装** ✅
   - 位置: `venv/bin/playwright`
   - 版本: 已安装

2. **浏览器MCP工具基于Playwright** ✅
   - 工具: `browser_navigate`, `browser_snapshot` 等
   - 位置: cursor-ide-browser MCP服务器
   - 使用: 直接在Cursor Chat中使用

3. **unified_dev_server没有Playwright工具** ⚠️
   - 有Selenium工具（`crawler.selenium.fetch`）
   - 有Lavague工具（`crawler.lavague.extract`）
   - 可以添加Playwright工具（如需要）

4. **推荐使用方式**:
   - **交互式浏览**: 使用浏览器MCP工具
   - **批量爬取**: 使用Selenium或Lavague工具
   - **复杂逻辑**: 编写Playwright脚本

---

**结论**: Playwright工具主要在**浏览器MCP工具（cursor-ide-browser）**中，可以直接在Cursor Chat中使用，无需编写脚本。
