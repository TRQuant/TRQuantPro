# 爬虫工具总结

> **生成时间**: 2026-01-09  
> **目的**: 确认可用的爬虫MCP工具，避免重复编写脚本

---

## ✅ 确认结果

### 1. xuanyuan（轩辕剑灵助手）

**状态**: ❌ **没有爬虫工具**

- **服务器**: `mcp_servers/xuanyuan_server.py`
- **工具总数**: 22个
- **工具类型**: 
  - 提示词管理（9个）
  - 错误分析（3个）
  - 调试工具（1个）
  - 命令工具（4个）
  - 记忆工具（4个）
  - 其他（1个）

**结论**: xuanyuan专注于Prompt Engineering和开发辅助，不包含爬虫功能。

---

### 2. unified_dev_server（统一开发工具服务器）

**状态**: ✅ **有完整的爬虫工具**

- **服务器**: `mcp_servers/unified_dev_server.py`
- **爬虫工具总数**: **10个**
- **工具分类**:
  - **基础爬虫工具**（5个）
  - **Selenium工具**（3个）
  - **Lavague AI工具**（2个）

---

## 📋 可用爬虫工具列表

### 基础爬虫工具（5个）

#### 1. `crawler.fetch` - 抓取网页内容

**功能**: 使用requests + BeautifulSoup抓取静态网页

**参数**:
- `url` (必需): 网页URL
- `extract_text` (可选, 默认True): 是否提取文本
- `extract_links` (可选, 默认False): 是否提取链接

**示例**:
```python
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='crawler.fetch',
    arguments={
        'url': 'https://ptradeapi.com/#新建策略',
        'extract_text': True,
        'extract_links': False
    },
    timeout=30.0
)
```

**限制**: 不支持JavaScript渲染的动态内容

---

#### 2. `crawler.search_docs` - 搜索文档

**功能**: 使用DuckDuckGo搜索文档

**参数**:
- `query` (必需): 搜索关键词
- `site` (可选): 限制搜索站点

---

#### 3. `crawler.download` - 下载文件

**功能**: 下载文件到本地

**参数**:
- `url` (必需): 文件URL
- `filename` (可选): 保存文件名

---

#### 4. `crawler.extract_code` - 提取代码块

**功能**: 从网页提取代码块

**参数**:
- `url` (必需): 网页URL
- `language` (可选): 代码语言

---

#### 5. `crawler.api_docs` - 获取API文档

**功能**: 从常用文档站点获取API文档

**参数**:
- `api_name` (必需): API名称
- `framework` (可选, 默认"python"): 框架类型

---

### Selenium工具（3个）- 支持动态页面

#### 6. `crawler.selenium.fetch` - 使用Selenium抓取动态网页

**功能**: 使用Selenium抓取需要JavaScript渲染的页面

**参数**:
- `url` (必需): 网页URL
- `wait_time` (可选, 默认3): 等待时间（秒）
- `wait_selector` (可选): 等待选择器
- `headless` (可选, 默认True): 无头模式

**示例**:
```python
result = client.call(
    tool_name='crawler.selenium.fetch',
    arguments={
        'url': 'https://ptradeapi.com/#新建策略',
        'wait_time': 5,
        'headless': True
    },
    timeout=60.0
)
```

**优势**: 支持JavaScript渲染的动态内容

**依赖**: 需要安装Selenium和浏览器驱动

---

#### 7. `crawler.selenium.click` - Selenium点击元素

**功能**: 点击页面元素

**参数**:
- `selector` (必需): 元素选择器
- `by` (可选, 默认"css"): 选择器类型（css/id/xpath/class/name）

---

#### 8. `crawler.selenium.extract` - Selenium提取元素

**功能**: 提取页面元素

**参数**:
- `selector` (必需): 元素选择器
- `attribute` (可选): 属性名

---

### Lavague AI工具（2个）- 智能爬虫

#### 9. `crawler.lavague.execute` - 使用Lavague AI执行自然语言指令

**功能**: 使用AI理解自然语言指令并执行网页操作

**参数**:
- `instruction` (必需): 自然语言指令
- `url` (可选): 目标URL
- `max_actions` (可选, 默认10): 最大操作次数
- `headless` (可选, 默认True): 无头模式

**示例**:
```python
result = client.call(
    tool_name='crawler.lavague.execute',
    arguments={
        'instruction': '提取"新建策略"页面的所有可调用接口',
        'url': 'https://ptradeapi.com/#新建策略',
        'max_actions': 10
    },
    timeout=120.0
)
```

**优势**: 智能理解自然语言，自动执行复杂操作

**依赖**: 需要安装Lavague

---

#### 10. `crawler.lavague.extract` - 使用Lavague AI提取数据

**功能**: 使用AI根据描述提取数据

**参数**:
- `description` (必需): 数据描述
- `url` (可选): 目标URL

---

## 🔧 工具映射修复

### 问题

MCPClient的`TOOL_SERVER_MAP`中缺少爬虫工具的映射，导致调用失败。

### 修复

已在 `core/mcp/client.py` 中添加爬虫工具映射：

```python
# 爬虫工具（unified_dev_server）
"crawler.fetch": "unified_dev_server",
"crawler.search_docs": "unified_dev_server",
"crawler.download": "unified_dev_server",
"crawler.extract_code": "unified_dev_server",
"crawler.api_docs": "unified_dev_server",
"crawler.selenium.fetch": "unified_dev_server",
"crawler.selenium.click": "unified_dev_server",
"crawler.selenium.extract": "unified_dev_server",
"crawler.lavague.execute": "unified_dev_server",
"crawler.lavague.extract": "unified_dev_server",
```

---

## 📊 工具对比

| 工具 | 支持JS | 智能理解 | 适用场景 |
|------|--------|----------|----------|
| `crawler.fetch` | ❌ | ❌ | 静态网页 |
| `crawler.selenium.fetch` | ✅ | ❌ | 动态网页 |
| `crawler.lavague.execute` | ✅ | ✅ | 复杂交互 |

---

## 💡 使用建议

### 对于PTrade API文档（单页应用SPA）

**推荐**: 使用 `crawler.selenium.fetch` 或 `crawler.lavague.extract`

**原因**:
- PTrade API文档是单页应用（SPA）
- 内容通过JavaScript动态加载
- 需要等待页面完全渲染

**示例**:
```python
# 方式1: 使用Selenium
result = client.call(
    tool_name='crawler.selenium.fetch',
    arguments={
        'url': 'https://ptradeapi.com/#新建策略',
        'wait_time': 5,
        'wait_selector': '[id="新建策略"]'  # 等待特定元素
    },
    timeout=60.0
)

# 方式2: 使用Lavague（更智能）
result = client.call(
    tool_name='crawler.lavague.extract',
    arguments={
        'description': '提取"新建策略"页面的所有可调用接口列表',
        'url': 'https://ptradeapi.com/#新建策略'
    },
    timeout=120.0
)
```

---

## 🎯 总结

1. ✅ **unified_dev_server有完整的爬虫工具**（10个）
2. ❌ **xuanyuan没有爬虫工具**（专注于Prompt Engineering）
3. ✅ **工具映射已修复**（可在MCPClient中正常调用）
4. ✅ **支持动态页面**（Selenium和Lavague工具）
5. ✅ **无需编写脚本**（直接使用MCP工具）

---

**建议**: 对于PTrade API文档等动态页面，使用 `crawler.selenium.fetch` 或 `crawler.lavague.extract`，而不是编写新的Playwright脚本。
