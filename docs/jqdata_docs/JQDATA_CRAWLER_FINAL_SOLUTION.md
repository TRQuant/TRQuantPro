# 聚宽API知识库爬虫 - 最终解决方案

> 创建时间: 2026-01-01
> 使用工具: **Playwright** (Selenium的现代替代，更强大)

---

## ✅ 最终方案

### 工具选择

经过分析，我们选择使用 **Playwright** 而不是Selenium，原因：

1. **Playwright更现代**: 由Microsoft开发，专为现代Web应用设计
2. **更好的JavaScript支持**: 原生支持等待策略（networkidle）
3. **更快的性能**: 更高效的浏览器自动化
4. **已集成**: 项目中已使用Playwright

### 脚本位置

- **主脚本**: `scripts/crawl_jqdata_complete_with_tools.py`
- **文档**: `docs/JQDATA_CRAWLER_WITH_TOOLS.md`

---

## 🎯 核心功能

### 1. 完整的链接提取

```python
async def extract_all_links_playwright(page_obj):
    """使用JavaScript在浏览器环境中提取所有链接"""
    # 直接在DOM中查找，确保获取所有链接（包括动态加载的）
    const allLinks = document.querySelectorAll('a[href*="/help/api/doc?name=JQDatadoc&id="]');
```

**优势**:
- ✅ 能获取JavaScript动态加载的链接
- ✅ 包括侧栏菜单中的所有链接
- ✅ 包括表格中的链接
- ✅ 包括二级菜单中的链接

### 2. 智能等待策略

```python
# 使用networkidle确保JavaScript完全加载
await page_obj.goto(url, wait_until='networkidle', timeout=120000)
await page_obj.wait_for_timeout(5000)  # 额外等待5秒，确保侧栏菜单渲染
```

**三层降级策略**:
1. `networkidle` - 等待网络请求完成（最佳）
2. `load` - 等待页面load事件
3. `domcontentloaded` - 基本DOM加载

### 3. 递归爬取

- **起始页面**: id=9842（JQData使用说明主页）
- **递归深度**: 3层
  - 第1层: 主页面（58个链接）
  - 第2层: 26个分类页面
  - 第3层: 每个分类的子链接（如CNE5的10个子链接）

### 4. 知识库自动存储

- 自动分类和标签生成
- 结构化Markdown格式
- 支持9步工作流标签体系
- 直接调用`knowledge_add`存储

---

## 📊 预期爬取范围

### 主页面（id=9842）

包含58个链接：
- **26个顶级分类**（从"JQData试用及购买"到"宏观数据"）
- **32个具体API函数文档**

### 每个分类的子链接

例如"风险模型 - 风格因子（CNE5）"（id=10446）：
- 10个子链接（get_all_factors, get_factor_values等）

### 预计总页面数

- **26个分类页面**
- **每个分类平均5-10个子链接**
- **预计总数**: 200+ 个文档页面

---

## 🚀 使用方法

### 运行爬虫

```bash
cd /home/taotao/dev/QuantTest/TRQuant

# 运行完整爬取
venv/bin/python scripts/crawl_jqdata_complete_with_tools.py
```

### 清理并重新开始（可选）

```bash
# 清理visited_urls记录
rm -f docs/jqdata_crawled/visited_urls.json

# 重新运行
venv/bin/python scripts/crawl_jqdata_complete_with_tools.py
```

---

## 📈 运行状态

脚本运行时会显示：
- 实时爬取进度
- 每个页面的链接数
- 成功/失败统计

完成后会显示：
- 总链接数
- 成功/失败/跳过数量
- 存入知识库数量
- 总耗时

结果保存在: `docs/jqdata_crawled/crawl_summary_*.json`

---

## 🔍 技术细节

### Playwright优势

1. **networkidle等待**: 确保JavaScript完全执行，侧栏菜单完全渲染
2. **JavaScript执行**: 直接在浏览器环境中执行代码，提取链接最准确
3. **异步支持**: 高效的并发处理
4. **错误处理**: 完善的异常处理和重试机制

### 与Selenium对比

| 特性 | Playwright | Selenium |
|------|------------|----------|
| 等待策略 | networkidle（原生） | 需要手动实现 |
| JavaScript执行 | 原生支持 | 支持但较慢 |
| 性能 | ⚡⚡⚡ 快 | ⚡⚡ 中等 |
| 现代Web支持 | ✅ 优秀 | ⚠️ 一般 |

**结论**: Playwright更适合现代Web应用，特别是需要处理JavaScript渲染的场景。

---

## ✅ 验证清单

运行完成后检查：

- [ ] `visited_urls.json` 中包含所有58+个链接
- [ ] 26个分类页面是否全部被抓取
- [ ] 每个分类的子链接是否被递归抓取
- [ ] 知识库条目数是否显著增加（预计从841增加到1000+）
- [ ] 标签分类是否正确（因子构建、风险模型等）

---

## 📝 相关文档

- `docs/JQDATA_CRAWLER_WITH_TOOLS.md` - 详细使用说明
- `docs/JQDATA_CRAWLER_FULL_IMPROVEMENT.md` - 改进说明
- `docs/JQDATA_10446_VERIFICATION.md` - 验证报告

---

*最终方案文档生成时间: 2026-01-01*

