# 标准知识库构建流程

> **版本**: v1.0  
> **更新**: 2026-01-12  
> **目的**: 定义标准化的RAG知识库构建步骤，确保知识库构建过程的可重复性和可维护性

---

## 📋 流程概述

标准知识库构建流程包含4个核心步骤：

```
┌─────────────────────────────────────────┐
│  步骤1: 使用MCP工具下载/智能爬取        │
│  - 优先使用MCP工具                      │
│  - 智能选择爬虫工具（基础/Selenium）   │
│  - 支持回退机制                         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  步骤2: 构建完整的RAG知识库             │
│  - 内容解析和结构化                      │
│  - 智能分类和标签                       │
│  - 去重和验证                           │
│  - 存入知识库（优先MCP工具）            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  步骤3: 测试并完善                      │
│  - 知识库搜索测试                       │
│  - 内容质量验证                         │
│  - 覆盖率检查                           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  步骤4: 工具和流程进化                  │
│  - 记录问题和改进                       │
│  - 更新工具和流程                       │
│  - 文档化最佳实践                       │
└─────────────────────────────────────────┘
```

---

## 🔧 步骤1: 使用MCP工具下载/智能爬取

### 1.1 工具选择策略

**优先顺序**:
1. **Playwright** (直接调用Python库) ⭐ 推荐
   - 最快、最可靠
   - 支持JavaScript渲染
   - 自动等待页面加载
   - 使用 `fetch_with_playwright(url)`
   
2. **OpenManus** (通过MCP工具或直接调用)
   - 智能浏览器工具
   - 支持复杂交互和内容提取
   - MCP工具: `MCPClient.call('browser_use', ...)`
   - 直接调用: `OpenManusBrowserTool().navigate(url)`
   
3. **MCP工具 - 基础爬虫** (`crawler.fetch`)
   - 最快，适合静态内容
   - 使用 `MCPClient.call('crawler.fetch', ...)`
   
4. **MCP工具 - Selenium** (`crawler.selenium.fetch`)
   - 处理JavaScript渲染的动态内容
   - 使用 `MCPClient.call('crawler.selenium.fetch', ...)`
   
5. **直接函数调用 - 基础爬虫**
   - 回退方案
   - 使用 `direct_crawler_fetch(...)`
   
6. **直接函数调用 - Selenium**
   - 最终回退方案
   - 使用 `direct_crawler_selenium_fetch(...)`

### 1.2 实现示例

```python
def fetch_with_playwright(url: str, wait_time: int = 5) -> Dict[str, Any]:
    """使用Playwright抓取页面（推荐）"""
    from playwright.async_api import async_playwright
    import asyncio
    
    async def fetch():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(wait_time * 1000)
            
            html = await page.content()
            title = await page.title()
            text = await page.inner_text('body')
            
            await browser.close()
            return {
                'success': True,
                'html': html,
                'text': text,
                'title': title
            }
    
    return asyncio.run(fetch())

def fetch_with_best_tool(url: str) -> Dict[str, Any]:
    """使用最佳工具抓取页面"""
    # 1. 优先使用Playwright
    result = fetch_with_playwright(url)
    if result.get('success'):
        return result
    
    # 2. 尝试OpenManus
    # 3. 尝试MCP工具
    # 4. 回退到直接函数调用
    # ...
```

### 1.3 最佳实践

- ✅ **优先使用MCP工具**: 符合MCP标准，便于追踪和调试
- ✅ **智能选择工具**: 根据内容类型选择最合适的工具
- ✅ **实现回退机制**: 确保即使MCP工具失败也能继续工作
- ✅ **设置合理超时**: 避免长时间等待
- ✅ **记录调用方法**: 便于问题排查

---

## 📚 步骤2: 构建完整的RAG知识库

### 2.1 内容解析

**针对不同文档类型**:

1. **Sphinx文档** (如AKShare)
   - 提取所有有ID的元素作为锚点内容块
   - 提取标题、内容、代码块
   - 处理章节结构

2. **Markdown文档**
   - 按标题层级分割
   - 提取代码块
   - 保留链接和引用

3. **API文档**
   - 提取函数/方法定义
   - 提取参数说明
   - 提取示例代码

### 2.2 智能分类和标签

**分类规则**:
- `lesson`: 教程、入门、快速指南
- `practice`: 示例、案例、演示
- `reference`: API文档、参考手册、配置说明

**标签生成**:
- 基于内容关键词自动生成
- 支持自定义标签
- 去重处理

### 2.3 去重和验证

**去重机制**:
- 使用内容哈希（MD5）
- 保存已处理的内容哈希
- 支持断点续传

**验证规则**:
- 内容长度检查（过滤太短的内容）
- 标题验证
- 代码块验证

### 2.4 存入知识库

**优先使用MCP工具**:
```python
result = client.call(
    tool_name='knowledge.add',
    arguments={
        'title': '知识条目标题',
        'content': '知识内容...',
        'type': 'reference',
        'tags': ['标签1', '标签2'],
        'source': '来源URL'
    },
    timeout=30.0
)
```

**回退机制**:
```python
if not success:
    result = direct_knowledge_add(
        title='知识条目标题',
        content='知识内容...',
        type='reference',
        tags=['标签1', '标签2'],
        source='来源URL'
    )
```

---

## 🧪 步骤3: 测试并完善

### 3.1 知识库搜索测试

```python
# 测试搜索功能
from core.mcp.client import MCPClient

client = MCPClient()
result = client.call(
    tool_name='knowledge.search',
    arguments={
        'query': 'AKShare 股票数据',
        'limit': 10
    }
)

# 验证结果
assert result.success
assert len(result.data.get('items', [])) > 0
```

### 3.2 内容质量验证

- ✅ 标题是否清晰
- ✅ 内容是否完整
- ✅ 代码示例是否正确
- ✅ 链接是否有效

### 3.3 覆盖率检查

- 统计已爬取的页面数
- 统计已保存的知识条目数
- 检查是否有遗漏的重要页面

---

## 🔄 步骤4: 工具和流程进化

### 4.1 记录问题和改进

**问题记录**:
- 哪些页面爬取失败？
- 哪些内容解析有问题？
- 哪些知识条目质量不高？

**改进建议**:
- 优化爬虫策略
- 改进内容解析逻辑
- 增强分类和标签规则

### 4.2 更新工具和流程

- 根据实际使用情况优化工具
- 更新流程文档
- 添加新的工具支持

### 4.3 文档化最佳实践

- 记录成功案例
- 总结失败教训
- 分享经验技巧

---

## 📁 项目结构

```
scripts/kb/
├── build_kb_akshare.py          # AKShare知识库构建脚本
├── build_kb_template.py         # 知识库构建模板（待创建）
└── utils/
    ├── crawler_utils.py         # 爬虫工具封装（待创建）
    ├── parser_utils.py          # 内容解析工具（待创建）
    └── kb_utils.py              # 知识库工具封装（待创建）

docs/knowledge_base/
├── STANDARD_KB_BUILD_PROCESS.md  # 本文档
├── KB_BUILD_EXAMPLES.md          # 构建示例（待创建）
└── KB_QUALITY_GUIDE.md           # 质量指南（待创建）
```

---

## 🎯 使用示例

### 构建AKShare知识库

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/kb/build_kb_akshare.py
```

### 自定义知识库构建

参考 `build_kb_akshare.py` 创建新的构建脚本：

1. 修改 `BASE_URL` 和 `START_URL`
2. 调整 `extract_sections_from_html()` 函数以适应目标网站结构
3. 调整 `classify_and_tag()` 函数以优化分类和标签
4. 运行脚本

---

## 📊 统计信息

每次构建会生成统计信息：

- 爬取页面数
- 找到内容块数
- 成功保存数
- 保存失败数
- 跳过重复数
- 总耗时

---

## 🔗 相关文档

- [MCP工具调用方式](../CLAUDE.md#mcp工具使用)
- [知识库管理指南](./KB_MANAGEMENT_GUIDE.md) (待创建)
- [爬虫工具总结](../ptrade_crawled/CRAWLER_TOOLS_SUMMARY.md)

---

**最后更新**: 2026-01-12  
**维护者**: TRQuant Team
