# JQData API文档重新抓取报告

> **抓取时间**: 2025-12-28  
> **来源URL**: https://www.joinquant.com/help/api/doc?name=JQDatadoc

---

## ✅ 抓取结果

- **总文档数**: 16
- **成功**: 16
- **失败**: 0
- **成功率**: 100%
- **总内容**: 51,449 字符

---

## 📄 抓取的文档列表

1. run_offset_query
2. 股票1天/分钟行情数据
3. 基金1天/分钟行情数据
4. 获取多个季度/年度的历史财务数据
5. 获取多个标的在指定交易日范围内的市值表数据
6. 获取期货合约的信息
7. 获取因子看板列表数据
8. 获取因子看板分位数历史收益率
9. 获取风格因子暴露收益率
10. 获取特异收益率（无法被风格因子解释的收益）
11. 批量获取alpha101因子
12. 批量获取alpha191因子
13. 可转债交易标的列表
14. 1天/分钟行情数据
15. 指定时间周期的分钟/日行情
16. 可转债Tick数据

---

## 📁 文件位置

- **文档文件**: `docs/jqdata_crawled/*.txt` (新增16个)
- **批次结果**: 
  - `docs/jqdata_crawled/batch_1_5.json`
  - `docs/jqdata_crawled/batch_6_16.json`
- **链接列表**: `/tmp/jqdata_doc_links.json`

---

## 💡 说明

本次抓取了JQData API文档列表页面的16个文档链接。

**注意**: 由于页面结构可能不同，本次抓取的文档数量(16个)与之前记录的52个不同。可能是：
1. 页面结构变化，链接展示方式不同
2. 部分文档链接在页面其他位置（如侧边栏、目录树等）
3. 文档分类或组织方式调整

如果需要抓取更多文档，建议：
1. 检查页面完整结构，包括侧边栏、目录树等
2. 使用不同的选择器提取链接
3. 访问更多相关页面

---

## 🔧 使用方法

### 查看抓取的文档
```bash
cd /home/taotao/dev/QuantTest/TRQuant
ls -lh docs/jqdata_crawled/*.txt | tail -20
```

### 继续抓取更多文档
```bash
# 1. 提取链接
/home/taotao/dev/QuantTest/TRQuant/venv/bin/python scripts/extract_jqdata_links.py

# 2. 使用批次脚本抓取
/home/taotao/dev/QuantTest/TRQuant/venv/bin/python scripts/crawl_jqdata_batch.py <起始索引> <批次大小>
```

---

*报告生成时间: 2025-12-28*







