# 聚宽API爬虫改进说明

> 改进时间: 2026-01-01
> 改进目标: 抓取侧栏链接中的具体API文档

---

## 🔍 问题分析

### 原有问题

1. **侧栏链接未被抓取**: 页面侧栏（表格中的链接）包含具体的API函数文档链接，但原有爬虫没有抓取到
2. **链接提取不够智能**: 原有方法仅使用BeautifulSoup解析HTML，可能无法处理JavaScript动态加载的链接
3. **目录结构缺失**: 页面目录中的子链接（如CNE5相关API函数）未被发现和抓取

### 示例页面分析

URL: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10446

该页面包含以下侧栏链接（在表格TD元素中）：
1. `get_all_factors` - 获取聚宽因子名称 (id=10447)
2. `get_factor_values` - 风险模型 - 风格因子（CNE5）(id=10448)
3. `get_index_style_exposure` - 获取重点宽基指数的风格暴露 (id=10767)
4. `get_factor_kanban_values` - 因子看板列表数据 (id=10449)
5. `get_factor_stats` - 因子看板分位数历史收益率 (id=10451)
6. `get_factor_style_returns` - 获取风格因子暴露收益率 (id=10318)
7. `get_factor_specific_returns` - 获取特异收益率 (id=10319)
8. `get_factor_cov` - 获取风格因子协方差矩阵 (id=10654)
9. 行业因子相关文档 (id=10452)
10. `normalize_code` - 代码格式转换 (id=9877)

---

## ✅ 改进方案

### 1. 添加JavaScript链接提取方法

新增 `extract_links_advanced()` 异步函数，使用Playwright的JavaScript执行环境直接提取链接：

```python
async def extract_links_advanced(page_obj, base_url: str) -> List[Dict[str, str]]:
    """使用JavaScript从页面中提取所有JQData相关链接（高级方法）"""
    # 在浏览器环境中执行JavaScript
    js_links = await page_obj.evaluate('''
        () => {
            const results = [];
            const allLinks = document.querySelectorAll('a[href*="/help/api/doc?name=JQDatadoc&id="]');
            // ... 提取和去重逻辑
            return results;
        }
    ''')
    return links
```

**优势**:
- ✅ 能获取JavaScript动态加载的链接
- ✅ 直接在浏览器环境中执行，更准确
- ✅ 不受HTML解析限制

### 2. 改进HTML解析备用方法

改进 `extract_links()` 函数，增加对表格中链接的特殊处理：

```python
# 方法2: 特别查找表格中的链接（侧栏目录通常在表格中）
for table in soup.find_all(['table', 'tbody']):
    for a in table.find_all('a', href=True):
        # ... 提取表格中的链接
```

### 3. 双重保障机制

在 `crawl_page()` 函数中，优先使用JavaScript方法，失败时回退到HTML解析：

```python
# 优先使用JavaScript方法提取链接（更准确）
sub_links = await extract_links_advanced(page_obj, BASE_URL)
# 如果JavaScript方法失败或结果为空，使用HTML解析备用方法
if not sub_links:
    sub_links = extract_links(html, BASE_URL)
```

---

## 🧪 测试结果

### 测试页面: id=10446 (风险模型 - 风格因子CNE5)

**改进前**:
- 提取到的链接数: 0-3个（仅主页面的导航链接）

**改进后**:
- 提取到的链接数: **10个**（包含所有侧栏API文档链接）

---

## 📋 改进文件

- `scripts/crawl_jqdata_all_subpages_to_kb.py`
  - 新增: `extract_links_advanced()` 函数
  - 改进: `extract_links()` 函数（增加表格链接提取）
  - 改进: `crawl_page()` 函数（使用双重保障机制）

---

## 🚀 使用方法

### 重新运行爬虫

```bash
cd /home/taotao/dev/QuantTest/TRQuant
# 清理旧的visited_urls（可选，如需重新抓取）
rm -f docs/jqdata_crawled/visited_urls.json

# 运行改进后的爬虫
venv/bin/python scripts/crawl_jqdata_all_subpages_to_kb.py
```

### 验证改进效果

改进后的爬虫将能够：
1. ✅ 抓取页面侧栏中的所有API文档链接
2. ✅ 递归抓取这些链接指向的具体API函数文档
3. ✅ 构建完整的API文档知识库

---

## 📊 预期结果

改进后，知识库将包含：
- **CNE5风格因子**的完整API文档（10个相关函数）
- **所有侧栏链接**指向的具体API文档
- **更完整的API文档覆盖**

---

*改进文档生成时间: 2026-01-01*

