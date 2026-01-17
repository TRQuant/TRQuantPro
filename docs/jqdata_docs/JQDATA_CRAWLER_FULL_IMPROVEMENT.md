# 聚宽API爬虫完整改进说明

> 改进时间: 2026-01-01
> 问题: 侧栏链接（26个顶级分类 + 二级菜单）未被抓取

---

## 🔍 问题分析

### 发现的问题

1. **主页面58个链接，但只爬取了1个**
   - 主页面(id=9842)包含58个文档链接
   - 前26个是顶级分类（从"JQData试用及购买"到"宏观数据"）
   - 后面的32个是各个分类下的具体API函数文档
   - 之前的爬取只抓取了主页面本身，**没有抓取侧栏中的26个分类链接**

2. **二级菜单未被识别**
   - 某些分类下有二级菜单（如"风险模型 - 风格因子（CNE5）"下有10个子链接）
   - 之前的爬虫没有递归抓取这些二级菜单

3. **等待时间不足**
   - 侧栏菜单通过JavaScript动态加载
   - 原来的等待策略（domcontentloaded + 3秒）不足以确保菜单完全渲染

---

## ✅ 改进方案

### 1. 改进页面加载等待策略

**原来**:
```python
await page_obj.goto(url, wait_until='domcontentloaded', timeout=120000)
await page_obj.wait_for_timeout(3000)  # 3秒
```

**改进后**:
```python
await page_obj.goto(url, wait_until='networkidle', timeout=120000)  # 等待网络空闲
await page_obj.wait_for_timeout(5000)  # 增加到5秒，确保侧栏菜单渲染
```

**三层降级策略**:
1. 优先: `networkidle` - 等待网络请求完成，确保JavaScript执行
2. 降级: `load` - 等待页面load事件
3. 最后: `domcontentloaded` - 基本DOM加载

### 2. 增强链接提取逻辑

**改进 `extract_links_advanced()` 函数**:

```python
async def extract_links_advanced(page_obj, base_url: str):
    """使用JavaScript从页面中提取所有JQData相关链接"""
    # 方法1: 查找所有文档链接（包括侧栏、表格、目录）
    const allLinks = document.querySelectorAll('a[href*="/help/api/doc?name=JQDatadoc&id="]');
    
    # 方法2: 特别查找侧栏菜单链接
    const menuLinks = document.querySelectorAll('ul a, nav a, aside a');
    
    # 去除URL锚点，避免重复
    const cleanHref = href.split('#')[0];
```

**关键改进**:
- ✅ 使用`networkidle`等待策略，确保JavaScript完全执行
- ✅ 增加等待时间到5-10秒，确保侧栏菜单渲染
- ✅ 提取所有类型的链接（侧栏、表格、目录）
- ✅ 去除URL锚点，避免重复抓取

### 3. 双重保障机制

```python
# 优先使用JavaScript方法提取链接（更准确）
sub_links = await extract_links_advanced(page_obj, BASE_URL)
# 如果JavaScript方法失败或结果为空，使用HTML解析备用方法
if not sub_links:
    sub_links = extract_links(html, BASE_URL)
```

---

## 📊 主页面链接结构

### 26个顶级分类（从JQData试用及购买到宏观数据）

| # | ID | 分类名称 |
|---|----|---------|
| 1 | 10868 | JQData试用及购买 |
| 2 | 10031 | JQData使用指南 |
| 3 | 10748 | JQData安装/登录/流量查询/查看账号权限 |
| 4 | 10749 | JQData常见报错 |
| 5 | 10261 | JQData数据范围及更新时间 |
| 6 | 10276 | JQData数据处理规则 ⭐ |
| 7 | 9836 | 全市场通用 ⭐ |
| 8 | 9842 | 沪深A股 |
| 9 | 9878 | 股票-单季度/年度财务数据（含新接口） |
| 10 | 9892 | 股票-报告期财务数据⭐ |
| 11 | 10006 | 上市公司相关信息 |
| 12 | 9903 | 期货 |
| 13 | 9913 | 期权 |
| 14 | 9926 | 基金 |
| 15 | 9927 | 指数⭐ |
| 16 | 9928 | 债券（含可转债⭐） |
| 17 | 9960 | Tick数据 |
| 18 | 10664 | 资金流因子 |
| 19 | 9961 | 舆情数据 |
| 20 | 10446 | 风险模型 - 风格因子（CNE5）⭐ |
| 21 | 10634 | 风险模型-风格因子pro（CNE6）⭐ |
| 22 | 9962 | 聚宽因子⭐ |
| 23 | 9963 | alpha101和alpha191 |
| 24 | 9964 | 技术指标 |
| 25 | 9965 | 宏观数据 |

### 每个分类下的子链接

例如，"风险模型 - 风格因子（CNE5）"（id=10446）下有10个子链接：
1. `get_all_factors` (id=10447)
2. `get_factor_values` (id=10448)
3. `get_index_style_exposure` (id=10767)
4. `get_factor_kanban_values` (id=10449)
5. `get_factor_stats` (id=10451)
6. `get_factor_style_returns` (id=10318)
7. `get_factor_specific_returns` (id=10319)
8. `get_factor_cov` (id=10654)
9. 行业因子相关 (id=10452)
10. `normalize_code` (id=9877)

---

## 🔧 当前覆盖情况

### 已爬取统计

从 `visited_urls.json` 检查：
- **已覆盖**: 1/25 个顶级分类（仅id=9842）
- **未覆盖**: 24个顶级分类
- **总链接数**: 主页面有58个链接，应全部抓取

---

## 🚀 下一步行动

### 重新运行爬虫

```bash
cd /home/taotao/dev/QuantTest/TRQuant

# 可选：清理visited_urls以重新抓取主页面
rm -f docs/jqdata_crawled/visited_urls.json

# 运行改进后的爬虫（从主页面id=9842开始）
venv/bin/python scripts/crawl_jqdata_all_subpages_to_kb.py
```

### 预期结果

改进后的爬虫将：
1. ✅ 从主页面提取所有58个链接（26个分类 + 32个具体API）
2. ✅ 递归抓取每个分类页面及其子链接
3. ✅ 抓取二级菜单中的所有API函数文档
4. ✅ 构建完整的API文档知识库（预计200+个文档）

---

## 📋 验证清单

运行爬虫后，检查：

- [ ] 主页面26个分类是否全部被抓取
- [ ] 每个分类下的子链接是否被递归抓取
- [ ] 二级菜单（如CNE5的10个子链接）是否全部抓取
- [ ] `visited_urls.json` 中是否包含所有58+个链接
- [ ] 知识库条目数是否显著增加（预计从841增加到1000+）

---

*改进文档生成时间: 2026-01-01*

