# 爬虫工具快速开始

## 🚀 5分钟快速上手

### 1. 安装依赖

```bash
# 基础爬虫（已包含）
pip install requests beautifulsoup4

# Selenium（可选，用于动态页面）
pip install selenium

# Lavague（可选，AI自动化）
pip install lavague
```

### 2. 基础使用示例

#### 示例A: 简单网页抓取

```python
# 在Cursor IDE中调用
result = await call_mcp("crawler.fetch", {
    "url": "https://www.example.com",
    "extract_text": True,
    "extract_links": True
})

print(result["text"])  # 页面文本
print(result["links"])  # 所有链接
```

#### 示例B: 抓取动态页面（Selenium）

```python
# 需要JavaScript渲染的页面
result = await call_mcp("crawler.selenium.fetch", {
    "url": "https://example.com/dynamic-page",
    "wait_time": 5,
    "wait_selector": ".content"  # 等待此元素加载
})
```

#### 示例C: AI自动化（Lavague）

```python
# 用自然语言描述操作
result = await call_mcp("crawler.lavague.execute", {
    "url": "https://example.com",
    "instruction": "点击登录按钮，填写用户名和密码，然后提交"
})
```

## 📋 工具对比

| 工具 | 速度 | 功能 | 适用场景 |
|------|------|------|----------|
| `crawler.fetch` | ⚡⚡⚡ 快 | 基础抓取 | 静态页面 |
| `crawler.selenium.*` | ⚡⚡ 中等 | 浏览器自动化 | 动态页面、交互操作 |
| `crawler.lavague.*` | ⚡ 较慢 | AI自动化 | 复杂操作、自然语言 |

## 🎯 实际应用示例

### 场景1: 抓取股票公告

```python
# 使用Selenium处理动态加载
result = await call_mcp("crawler.selenium.fetch", {
    "url": "http://data.eastmoney.com/notices/stock/000001.html",
    "wait_selector": ".notice-list"
})

# 提取公告标题
titles = await call_mcp("crawler.selenium.extract", {
    "selector": ".notice-title",
    "attribute": "text"
})
```

### 场景2: 自动登录并提取数据

```python
# 使用Lavague一步完成
result = await call_mcp("crawler.lavague.execute", {
    "url": "https://example.com/login",
    "instruction": "登录并提取用户信息",
    "max_actions": 10
})
```

## 📚 更多文档

- [完整使用指南](./CRAWLER_SELENIUM_LAVAGUE.md)
- [代码示例](./crawler_selenium_lavague_examples.py)












































