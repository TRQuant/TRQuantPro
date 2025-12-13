# 热度评分系统集成问题分析

## 🔍 问题诊断

### 问题1: 主线识别与热度评分数据不衔接

**现状**:
- 主线识别（专业主线识别Tab）使用 `ProMainlineEngine`，从 `pro_mainline_panel.py` 获取数据
- 热度评分（热度评分Tab）使用 `HeatmapEngine`，从 `heatmap_panel.py` 独立获取数据
- **两者完全独立，数据不共享**

**影响**:
- 主线识别排名第一的"海南自贸区"，在热度评分中排名第二
- 两个模块使用不同的数据源和计算逻辑，结果不一致

**根本原因**:
```python
# 主线识别数据流
pro_mainline_panel.py → RealDataFetcher → ProMainlineEngine

# 热度评分数据流（独立）
heatmap_panel.py → RealDataFetcher → HeatmapDataAggregator → HeatmapEngine
```

---

### 问题2: 归一化异常导致所有值相同

**现象**:
- 龙虎榜列：所有值都是100
- 涨停列：所有值都是0
- 趋势列：所有值都是"平稳"

**根本原因**:

```python
# heatmap_engine.py 中的归一化逻辑
def _normalize_value(self, value, params, target_min=0, target_max=100):
    min_val = params["min"]
    max_val = params["max"]
    
    if max_val == min_val:  # ⚠️ 如果所有值都相同
        return target_max if value > 0 else target_min  # 返回100或0
    
    normalized = (value - min_val) / (max_val - min_val)
    ...
```

**问题**:
1. 如果所有主线的龙虎榜次数都是0，`max_val == min_val == 0`
2. 归一化后，所有值都变成 `target_max` (100) 或 `target_min` (0)
3. 涨停数据可能都是0，导致归一化后都是0

**数据来源问题**:
```python
# HeatmapDataAggregator._count_lhb_for_sector()
# 当前逻辑：通过股票名称匹配板块名称（过于简单）
if sector_name in stock_name or stock_name in sector_name:
    count += 1
```

这个匹配逻辑可能无法正确统计龙虎榜次数。

---

### 问题3: 趋势计算缺失

**现象**: 所有主线的趋势都是"平稳"

**原因**:
```python
# heatmap_engine.py
prev_score = data.get("prev_total_score", 0)
if prev_score > 0:
    score.score_change = score.total_score - prev_score
    if score.score_change > 5:
        score.trend = "rising"
    ...
```

**问题**: 
- `data` 中没有 `prev_total_score` 字段
- 没有历史数据对比，无法计算趋势
- 默认都是 `trend = "stable"`

---

## 🎯 解决方案

### 方案1: 数据共享架构（推荐）

**目标**: 主线识别和热度评分共享同一数据源和结果

**架构设计**:
```
数据获取层 (RealDataFetcher)
    ↓
数据聚合层 (统一的数据结构)
    ↓
    ├─→ 主线识别引擎 (ProMainlineEngine)
    │       └─→ 热度评分引擎 (HeatmapEngine) ← 使用主线识别结果
    │
    └─→ 热度评分面板 (显示主线识别的热度评分)
```

**实现步骤**:
1. 修改 `HeatmapPanel`，从主线识别结果获取数据
2. 主线识别完成后，自动计算热度评分
3. 热度评分面板显示主线识别的热度维度得分

---

### 方案2: 修复归一化逻辑

**问题**: 当所有值相同时，归一化失效

**解决方案**:
```python
def _normalize_value(self, value, params, target_min=0, target_max=100):
    min_val = params["min"]
    max_val = params["max"]
    
    if max_val == min_val:
        # 如果所有值相同，返回中间值或0
        if value == 0:
            return target_min
        else:
            return (target_min + target_max) / 2  # 返回中间值
    
    normalized = (value - min_val) / (max_val - min_val)
    ...
```

---

### 方案3: 修复龙虎榜和涨停统计

**问题**: 当前统计逻辑无法正确匹配板块

**解决方案**:
1. 使用股票代码映射板块关系
2. 从AKShare获取板块成分股列表
3. 基于成分股统计龙虎榜和涨停

---

### 方案4: 实现趋势计算

**问题**: 缺少历史数据对比

**解决方案**:
1. 保存历史热度评分到MongoDB
2. 计算时读取上期数据
3. 计算趋势变化

---

## 📊 推荐实施顺序

1. **立即修复**: 归一化逻辑（方案2）- 解决显示问题
2. **短期优化**: 数据共享架构（方案1）- 解决数据不一致
3. **中期完善**: 修复统计逻辑（方案3）- 提高数据准确性
4. **长期增强**: 趋势计算（方案4）- 增加趋势分析

---

*问题分析时间: 2024-11-28*

