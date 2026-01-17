# Selenium和Lavague爬虫工具集成指南

## 📋 概述

TRQuant现在支持两种强大的浏览器自动化工具：

1. **Selenium** - 传统的浏览器自动化工具，适合精确控制
2. **Lavague** - AI驱动的浏览器自动化，可以理解自然语言指令

## 🚀 安装

### 基础依赖

```bash
# 安装Selenium
pip install selenium

# 安装Lavague
pip install lavague

# 安装浏览器驱动（Chrome）
# 方法1: 使用webdriver-manager（推荐）
pip install webdriver-manager

# 方法2: 手动下载chromedriver
# https://chromedriver.chromium.org/downloads
```

### 配置环境变量（可选）

```bash
# 如果手动下载了chromedriver，添加到PATH
export PATH=$PATH:/path/to/chromedriver
```

## 🔧 Selenium工具

### 1. `crawler.selenium.fetch` - 抓取动态网页

**适用场景**: 需要JavaScript渲染的页面

```python
# 在Cursor IDE中使用
await call_mcp("crawler.selenium.fetch", {
    "url": "https://example.com",
    "wait_time": 3,  # 等待时间（秒）
    "wait_selector": ".content",  # 等待元素选择器（可选）
    "headless": True  # 是否无头模式
})
```

**示例**: 抓取东方财富股票页面

```python
result = await call_mcp("crawler.selenium.fetch", {
    "url": "http://quote.eastmoney.com/sz000001.html",
    "wait_time": 5,
    "wait_selector": ".stock-info"
})
```

### 2. `crawler.selenium.click` - 点击元素

**适用场景**: 需要点击按钮、链接等交互操作

```python
await call_mcp("crawler.selenium.click", {
    "selector": "#login-button",  # CSS选择器
    "by": "css"  # 选择器类型: css/id/xpath/class/name
})
```

### 3. `crawler.selenium.extract` - 提取元素

**适用场景**: 提取页面中的特定元素数据

```python
# 提取文本
result = await call_mcp("crawler.selenium.extract", {
    "selector": ".stock-name",
    "attribute": "text"  # text/href/src等，不填默认提取文本
})

# 提取链接
result = await call_mcp("crawler.selenium.extract", {
    "selector": "a.stock-link",
    "attribute": "href"
})
```

## 🤖 Lavague AI工具

### 1. `crawler.lavague.execute` - 执行自然语言指令

**适用场景**: 复杂的多步骤操作，用自然语言描述

```python
# 执行登录操作
result = await call_mcp("crawler.lavague.execute", {
    "url": "https://example.com/login",
    "instruction": "点击登录按钮，填写用户名test和密码123456，然后点击提交",
    "max_actions": 10,  # 最大执行动作数
    "headless": True
})
```

**示例**: 自动搜索并提取数据

```python
result = await call_mcp("crawler.lavague.execute", {
    "url": "https://www.eastmoney.com",
    "instruction": "搜索'宁德时代'，点击第一个结果，提取股票代码和当前价格"
})
```

### 2. `crawler.lavague.extract` - AI提取数据

**适用场景**: 提取结构化数据，用自然语言描述

```python
result = await call_mcp("crawler.lavague.extract", {
    "url": "https://example.com/products",
    "description": "提取所有产品的名称、价格和评分，格式为JSON数组"
})
```

## 📝 完整使用示例

### 示例1: 使用Selenium爬取股票公告

```python
# 步骤1: 访问页面
result1 = await call_mcp("crawler.selenium.fetch", {
    "url": "http://data.eastmoney.com/notices/stock/000001.html",
    "wait_time": 5,
    "wait_selector": ".notice-list"
})

# 步骤2: 提取公告标题
result2 = await call_mcp("crawler.selenium.extract", {
    "selector": ".notice-title",
    "attribute": "text"
})

# 步骤3: 提取公告日期
result3 = await call_mcp("crawler.selenium.extract", {
    "selector": ".notice-date",
    "attribute": "text"
})
```

### 示例2: 使用Lavague自动登录并提取数据

```python
# 一步完成：登录并提取数据
result = await call_mcp("crawler.lavague.execute", {
    "url": "https://example.com",
    "instruction": """
    1. 点击登录按钮
    2. 填写用户名和密码
    3. 点击提交
    4. 等待页面加载完成
    5. 提取用户信息
    """,
    "max_actions": 15
})
```

### 示例3: 混合使用（Selenium + Lavague）

```python
# 使用Selenium精确控制导航
result1 = await call_mcp("crawler.selenium.fetch", {
    "url": "https://example.com/products",
    "wait_selector": ".product-list"
})

# 使用Lavague智能提取数据
result2 = await call_mcp("crawler.lavague.extract", {
    "description": "提取所有产品的名称、价格、库存和评分"
})
```

## ⚙️ 配置选项

### Selenium配置

- **headless**: `True`/`False` - 是否无头模式（不显示浏览器）
- **browser**: `"chrome"`/`"firefox"` - 浏览器类型
- **wait_time**: 等待时间（秒）
- **wait_selector**: CSS选择器，等待元素出现

### Lavague配置

- **headless**: `True`/`False` - 是否无头模式
- **model**: AI模型（默认: `"gpt-4o-mini"`）
- **max_actions**: 最大执行动作数（防止无限循环）

## 🎯 使用场景对比

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| 简单静态页面 | `crawler.fetch` | 速度快，资源占用少 |
| JavaScript渲染页面 | `crawler.selenium.fetch` | 支持动态内容 |
| 需要点击/填写表单 | `crawler.selenium.click` | 精确控制 |
| 复杂多步骤操作 | `crawler.lavague.execute` | 自然语言描述，AI自动执行 |
| 提取结构化数据 | `crawler.lavague.extract` | AI理解页面结构 |
| 需要精确控制 | Selenium系列 | 完全可控 |
| 快速原型开发 | Lavague系列 | 开发效率高 |

## ⚠️ 注意事项

1. **浏览器驱动**: 确保已安装并配置好浏览器驱动
2. **资源占用**: Selenium和Lavague会启动真实浏览器，资源占用较大
3. **速度**: 比requests慢，但能处理动态内容
4. **稳定性**: 网站结构变化可能导致选择器失效
5. **合规性**: 遵守网站的robots.txt和使用条款

## 🔍 故障排查

### Selenium常见问题

1. **驱动未找到**: 安装webdriver-manager或手动下载驱动
2. **元素未找到**: 增加wait_time或检查选择器
3. **页面加载慢**: 增加wait_time或使用wait_selector

### Lavague常见问题

1. **指令执行失败**: 简化指令或增加max_actions
2. **模型未配置**: 确保设置了OPENAI_API_KEY
3. **页面理解错误**: 提供更详细的指令描述

## 📚 更多资源

- [Selenium官方文档](https://www.selenium.dev/documentation/)
- [Lavague GitHub](https://github.com/lavague-ai/lavague)
- [示例代码](../examples/crawler_selenium_lavague_examples.py)












































