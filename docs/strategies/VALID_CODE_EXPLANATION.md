# 有效代码（Valid Code）说明

> **创建时间**: 2026-01-14  
> **版本**: v1.0

## 问题说明

在运行 `01_market_environment_judgment.ipynb` 时，您可能会看到：

```
✅ 获取成功！涨停家数: 102只
✅ 有效代码: 99只
```

**疑问**：为什么涨停家数和有效代码数量不一样？

## 概念解释

### 1. 涨停家数（Limit Up Count）

**定义**：从AKShare获取的**所有涨停股票数量**

**来源**：`ak.stock_zt_pool_em(date=today_str)`

**特点**：
- 包含所有涨停股票（无论是否能查询历史数据）
- 数据来源：AKShare（东方财富/同花顺算法）
- 格式：6位数字代码（如：`002044`、`600343`）

### 2. 有效代码（Valid Code）

**定义**：能够**成功转换为JQData格式**的股票数量

**转换过程**：
1. AKShare代码格式：`002044`（6位数字）
2. 转换为JQData格式：`002044.XSHE`（代码 + 交易所后缀）
3. 验证：检查JQData中是否有该股票的历史数据

**转换规则**：
```python
def convert_code_to_jq(code):
    """将AKShare股票代码转换为JQData格式"""
    code_str = str(code)
    if len(code_str) == 6:
        if code_str.startswith('00') or code_str.startswith('30'):
            return f"{code_str}.XSHE"  # 深市（深圳交易所）
        elif code_str.startswith('60') or code_str.startswith('68'):
            return f"{code_str}.XSHG"  # 沪市（上海交易所）
    return None  # 无法转换
```

## 为什么会有差异？

### 差异原因

1. **新股票**：刚上市的新股票，JQData可能还没有历史数据
2. **退市股票**：已退市的股票，JQData中可能已删除
3. **代码格式不匹配**：某些特殊代码（如科创板、创业板特殊代码）可能无法转换
4. **数据源差异**：AKShare和JQData的数据覆盖范围不完全一致

### 示例

假设某日有102只涨停股票：
- **涨停家数**：102只（AKShare数据）
- **有效代码**：99只（能转换为JQData格式）
- **无法转换**：3只（可能是新股票、退市股票或代码格式不匹配）

## 对分析结果的影响

### 1. 情绪周期判断

**使用数据**：**涨停家数**（102只）

**原因**：
- 情绪周期判断主要看**市场整体热度**
- 涨停家数反映市场真实情况（无论是否能查询历史数据）
- 使用原始涨停家数更准确

**判断标准**：
- <10只：退潮期
- 10-30只：启动期
- 30-60只：加速期
- >60只：过热期

### 2. 连板高度计算

**使用数据**：**有效代码**（99只）

**原因**：
- 连板高度需要查询JQData历史价格数据
- 只有能转换为JQData格式的股票才能计算连板高度
- 无法转换的股票无法计算连板高度

**影响**：
- 如果无法转换的股票恰好是连板高度很高的股票，可能会影响最高连板数的统计
- 但通常这种情况较少，因为新股票或退市股票很少出现在涨停板中

### 3. 炸板率计算

**使用数据**：**涨停家数**（102只）

**原因**：
- 炸板率 = 炸板数量 / (涨停数量 + 炸板数量)
- 使用原始涨停家数更准确

## 代码实现

```python
# 1. 获取涨停板数据（AKShare）
limit_up_data = ak.stock_zt_pool_em(date=today_str)
limit_up_count = len(limit_up_data)  # 涨停家数：102只

# 2. 转换为JQData格式
limit_up_data['jq_code'] = limit_up_data['代码'].apply(convert_code_to_jq)

# 3. 过滤有效代码
valid_data = limit_up_data[limit_up_data['jq_code'].notna()].copy()
valid_count = len(valid_data)  # 有效代码：99只

# 4. 统计无法转换的代码
invalid_count = limit_up_count - valid_count  # 无法转换：3只

# 5. 使用数据
# - 情绪周期判断：使用 limit_up_count（102只）
# - 连板高度计算：使用 valid_data（99只）
# - 炸板率计算：使用 limit_up_count（102只）
```

## 优化建议

### 1. 显示无法转换的股票

如果无法转换的股票数量较多（>5只），可以显示具体是哪些股票：

```python
if invalid_count > 0:
    invalid_stocks = limit_up_data[limit_up_data['jq_code'].isna()]
    print(f"\n⚠️  无法转换的股票（{invalid_count}只）:")
    for idx, row in invalid_stocks.iterrows():
        print(f"   {row['代码']} {row['名称']}")
```

### 2. 使用AKShare数据补充

对于无法转换的股票，可以使用AKShare的历史数据来计算连板高度（如果AKShare提供该功能）。

### 3. 数据源统一

考虑统一使用一个数据源（如全部使用AKShare或全部使用JQData），避免格式转换问题。

## 常见问题

### Q1: 为什么不能直接用AKShare的数据？

**A**: AKShare主要用于实时数据，历史数据查询功能不如JQData完善。JQData提供更完整的历史价格数据，更适合计算连板高度。

### Q2: 差异会影响情绪周期判断吗？

**A**: 通常不会。差异通常只有1-5只股票，对整体判断影响很小。但如果差异很大（>10只），需要检查数据源是否有问题。

### Q3: 如何减少差异？

**A**: 
1. 定期更新代码转换规则
2. 检查JQData数据覆盖范围
3. 对于无法转换的股票，使用AKShare数据补充

## 总结

- **涨停家数**：市场真实涨停数量（用于情绪周期判断）
- **有效代码**：能查询历史数据的股票数量（用于连板高度计算）
- **差异原因**：新股票、退市股票、代码格式不匹配
- **影响**：通常很小，不影响整体判断

**建议**：关注涨停家数（用于情绪周期判断），有效代码主要用于连板高度计算。
