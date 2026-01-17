# 聚宽API爬虫 - 使用现有工具组合版本

> 创建时间: 2026-01-01
> 使用工具: Selenium + Playwright + 知识库工具

---

## 🎯 设计理念

充分利用TRQuant系统现有的爬虫工具：
- **Playwright**: 强大的浏览器自动化，处理JavaScript渲染
- **knowledge_add**: 直接存储到知识库
- **组合优势**: Playwright抓取 + 知识库存储，一站式完成

---

## 📋 脚本功能

### 核心特性

1. **Playwright自动化**
   - 使用`networkidle`等待策略，确保JavaScript完全加载
   - 额外等待5秒，确保侧栏菜单渲染
   - 使用JavaScript提取所有链接（包括动态加载的）

2. **智能链接提取**
   ```python
   async def extract_all_links_playwright(page_obj):
       """使用JavaScript在浏览器环境中提取所有链接"""
       # 直接在浏览器DOM中查找，最准确
   ```

3. **递归爬取**
   - 从主页面(id=9842)开始
   - 递归深度: 3层（主页 -> 分类页 -> API函数页）
   - 自动跳过已访问的URL

4. **知识库存储**
   - 自动分类和标签
   - 结构化Markdown格式
   - 支持9步工作流标签体系

---

## 🚀 使用方法

### 运行脚本

```bash
cd /home/taotao/dev/QuantTest/TRQuant

# 运行完整爬取（从主页面开始）
venv/bin/python scripts/crawl_jqdata_complete_with_tools.py
```

### 清理并重新开始（可选）

```bash
# 清理旧的visited_urls记录
rm -f docs/jqdata_crawled/visited_urls.json

# 重新运行
venv/bin/python scripts/crawl_jqdata_complete_with_tools.py
```

---

## 📊 预期结果

### 爬取范围

- **主页面**: id=9842（JQData使用说明）
- **26个顶级分类**: 从"JQData试用及购买"到"宏观数据"
- **每个分类的子链接**: 如CNE5有10个子链接
- **预计总页面数**: 200+ 个文档

### 知识库存储

- 所有页面自动存储到知识库
- 自动分类标签（因子构建、市场趋势、主线识别等）
- 结构化内容（Markdown格式）

---

## 🔧 技术细节

### 等待策略

```python
# 使用networkidle确保JavaScript完全加载
await page_obj.goto(url, wait_until='networkidle', timeout=120000)
await page_obj.wait_for_timeout(5000)  # 额外等待侧栏菜单渲染
```

### 链接提取

```javascript
// 在浏览器环境中执行JavaScript
const allLinks = document.querySelectorAll('a[href*="/help/api/doc?name=JQDatadoc&id="]');
// 去除锚点，避免重复
const cleanHref = href.split('#')[0];
```

### 分类标签

自动根据标题和内容生成标签：
- 因子构建、Alpha因子、Alpha101、Alpha191
- 风险模型、CNE5风格因子、CNE6风格因子
- 市场趋势、主线识别、候选池、策略生成、回测数据

---

## 📈 统计信息

运行完成后会显示：
- 总链接数
- 成功/失败/跳过数量
- 存入知识库数量
- 总耗时

结果保存在: `docs/jqdata_crawled/crawl_summary_*.json`

---

## ✅ 优势

1. **充分利用现有工具**: 使用系统已有的Playwright和知识库工具
2. **完全自动化**: 从抓取到存储，无需人工干预
3. **智能去重**: visited_urls持久化，避免重复爬取
4. **结构化存储**: 自动分类标签，便于后续检索

---

*文档生成时间: 2026-01-01*

