# 聚宽API文档验证报告 - ID 10446

> URL: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10446
> 验证时间: 2026-01-01

---

## ✅ 验证结果

### 1. 是否已抓取？

**✅ 是，已在历史记录中找到**

- **位置**: `docs/jqdata_crawled/jqdata_9842_all_pages.json`
- **知识库条目**: 已在知识库中存在（但来源URL格式略有差异）
- **最近爬取**: 未在最近一次爬取的42个页面中（visited_urls.json中未记录）

---

## 📋 主要内容

### 文档标题
**风险模型 - 风格因子（CNE5）**

### 核心API函数列表

该文档介绍了聚宽CNE5风格因子相关的所有API函数：

| API函数 | 说明 | 历史范围 | 更新时间 |
|---------|------|----------|----------|
| `get_all_factors` | 获取聚宽因子名称 | - | - |
| `get_factor_values` | 获取风险模型-风格因子（CNE5） | 2005年至今 | 下个自然日5点、8点更新 |
| `get_index_style_exposure` | 获取重点宽基指数的风格暴露 | 2005年至今 | 9:00更新前一交易日 |
| `get_factor_kanban_values` | 因子看板列表数据 | 2005至今 | 9:00更新前一交易日 |
| `get_factor_stats` | 因子看板分位数历史收益率 | 2005至今 | 9:00更新前一交易日 |
| `get_factor_style_returns` | 获取风格因子暴露收益率 | 2005至今 | 9:00更新前一交易日 |
| `get_factor_specific_returns` | 获取特异收益率 | 2005至今 | 9:00更新前一交易日 |
| `get_factor_cov` | 获取风格因子协方差矩阵 | 2005至今 | 9:00更新前一交易日 |

### 行业因子

文档还介绍了行业因子的获取方法（使用 `get_factor_values`）：
- 证监会行业
- 聚宽行业(一二级)
- 申万行业(一二三级)

### 代码格式说明

文档包含了 `normalize_code(code)` 函数说明，介绍如何将标的代码转化成聚宽标准格式，包括各交易所的后缀规则。

---

## 🔗 子链接情况

### 检查结果

**❌ JSON文件中未保存子链接信息**

但根据文档内容，这些API函数应该都有对应的详细文档页面。

### 知识库中的相关条目

虽然主页面（id=10446）的子链接信息未保存，但相关的API函数文档已在知识库中存在：

| API函数 | 知识库条目数 |
|---------|-------------|
| `get_factor_kanban_values` | 32 条 |
| `get_factor_style_returns` | 20 条 |
| `get_factor_specific_returns` | 20 条 |
| `get_factor_values` | 26 条 |
| `get_all_factors` | 16 条 |
| `get_index_style_exposure` | 6 条 |
| `get_factor_cov` | 6 条 |

---

## 📝 建议

1. **重新抓取主页面**: 由于未在最近爬取中，建议重新抓取以确保内容最新
2. **抓取子链接**: 虽然相关API文档已存在，但建议从主页面提取并抓取所有子链接，确保完整性
3. **更新知识库标签**: 确保该页面被正确标记为"风险模型"、"CNE5风格因子"等标签

---

## 🔍 相关文档

- 历史记录文件: `docs/jqdata_crawled/jqdata_9842_all_pages.json`
- 知识库位置: `.trquant/dev/knowledge/knowledge_base.json`
- 网页链接: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10446

---

*报告生成时间: 2026-01-01 17:22*

