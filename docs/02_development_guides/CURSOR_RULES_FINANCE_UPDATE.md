# JQData finance表调用规则已添加到.cursorrules

## ✅ 验证结果

规则已成功添加到 `.cursorrules` 文件：

### 规则位置
- 起始行：第 85 行
- 章节标题：`## 🔴 JQData finance表调用规则（关键！）`

### 包含内容

1. ✅ **查询方法权限对照表**
   - valuation/indicator: 使用 get_fundamentals()
   - finance表: 使用 run_query()

2. ✅ **正确调用方式示例**
   - valuation/indicator 表的正确用法
   - finance表的正确用法

3. ✅ **字段名差异说明**
   - valuation/indicator: 使用 statDate 参数
   - finance表: 使用 end_date 字段

4. ✅ **常见错误及修正**
   - 错误1: 对finance表使用get_fundamentals
   - 错误2: finance表使用statDate字段
   - 错误3: 对valuation/indicator使用run_query

5. ✅ **快速参考**
   - 查询方法对照
   - 日期格式说明

6. ✅ **数据限制说明**
   - get_fundamentals(): 无明确限制
   - run_query(): 最多5000条
   - run_offset_query(): 最多20万条

### 文件信息
- 文件路径: `/home/taotao/dev/QuantTest/TRQuant/.cursorrules`
- 规则版本: 6.1 (添加JQData finance表调用规则)
- 更新时间: 2025-12-20

### 关键规则摘要

**valuation/indicator表**:
```python
df = get_fundamentals(q, date='2025-09-18')  # 或 statDate='2024Q3'
```

**finance表**:
```python
df = finance.run_query(q)  # 必须使用run_query
# 字段使用 end_date，日期格式 '2024-09-30'
```

---

*验证时间: 2025-12-20*
