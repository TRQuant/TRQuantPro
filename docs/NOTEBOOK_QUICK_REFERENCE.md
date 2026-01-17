# Notebook 快速参考卡片

> **目标**: `01_市场趋势判断回测验证.ipynb` 版本管理快速指南

## 🎯 三大核心功能

| 功能 | Cell位置 | 作用 |
|------|----------|------|
| **版本标签** | Cell 16, 20 | 避免结果覆盖，每次运行创建新版本 |
| **结果选择器** | Cell 22 | 列出所有历史版本，显示关键指标 |
| **结果比较** | Cell 23 | 对比多个版本，自动分析差异 |

---

## ⚡ 快速使用

### 1️⃣ 设置版本标签（Cell 16 或 20）

```python
# ============ 配置区域 ============
USE_CACHE = False           # False=创建新记录, True=使用缓存
VERSION_TAG = 'v1.0'        # 自定义标签
# VERSION_TAG = None        # None=自动时间戳
# =================================
```

### 2️⃣ 查看历史版本（Cell 22）

直接运行，输出：
```
[1] 2026-01-04 23:30 | v1.0 | 信号:239 | 准确率:61.5%
    ID: 695ae896cf1ec34386c0bc3a
[2] 2026-01-04 20:15 | 优化后 | 信号:235 | 准确率:63.2%
    ID: 695ae896cf1ec34386c0bc3d
```

### 3️⃣ 对比版本（Cell 23）

```python
# ============ 配置区域 ============
RESULT_IDS_TO_COMPARE = [
    "695ae896cf1ec34386c0bc3a",  # v1.0
    "695ae896cf1ec34386c0bc3d",  # 优化后
]
# =================================
```

---

## 📋 典型工作流

```
┌─────────────────────┐
│ 1. 运行基准版本     │  VERSION_TAG = 'v1.0_baseline'
│    Cell 16/20       │  USE_CACHE = False
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 2. 修改算法         │  编辑 core/signal_backtest.py
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 3. 运行新版本       │  VERSION_TAG = 'v1.1_optimized'
│    Cell 16/20       │  USE_CACHE = False
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 4. 查看历史         │  运行 Cell 22
│    Cell 22          │  记录ID
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ 5. 对比版本         │  设置ID列表
│    Cell 23          │  运行 Cell 23
└─────────────────────┘
```

---

## ⚠️ 重要提醒

### ✅ 务必遵守

1. **修改算法后** → 设置 `USE_CACHE=False`
2. **重要版本** → 设置有意义的 `VERSION_TAG`
3. **运行后** → 在Cell 22中验证版本已保存

### ❌ 避免错误

```python
# ❌ 错误：修改算法后使用缓存
VERSION_TAG = 'v1.1'
USE_CACHE = True  # 会加载v1.0的缓存！

# ✅ 正确
VERSION_TAG = 'v1.1'
USE_CACHE = False  # 创建新记录
```

---

## 💡 版本命名建议

| 类型 | 示例 | 适用场景 |
|------|------|----------|
| **语义化** | `v1.0`, `v1.1`, `v2.0` | 正式版本 |
| **描述性** | `优化参数`, `修复bug` | 实验版本 |
| **日期+描述** | `20260104_优化阈值` | 需要时间追溯 |

---

## 📊 对比指标说明

| 指标 | 含义 | 期望值 |
|------|------|--------|
| **5日准确率** | 短期信号准确率 | > 55% |
| **20日准确率** | 中期信号准确率 | > 60% |
| **60日准确率** | 长期信号准确率 | > 65% |
| **市场状态准确率** | 状态判断准确率 | > 60% |

### 改进判断

- 提升 **> 2%** → 显著改进 ✅
- 提升 **< 0.5%** → 改进不明显 ⚠️
- 下降 → 需要回滚 ❌

---

## 🔍 故障排除

### 问题1: 版本标签未更新

**手动修复**:
```python
from bson import ObjectId
from core.market_trend_storage import MarketTrendStorage

storage = MarketTrendStorage()
storage.db[storage.BACKTEST_COLLECTION].update_one(
    {'_id': ObjectId('结果ID')},
    {'$set': {'version_tag': '期望的标签'}}
)
```

### 问题2: 结果被覆盖

**检查**:
- 是否设置了 `USE_CACHE=False`？
- 是否修改了配置参数？

**解决**: 下次运行前确保 `USE_CACHE=False`

### 问题3: 对比工具无输出

**检查**:
- `RESULT_IDS_TO_COMPARE` 是否为空？
- ID格式是否正确（24位十六进制）？

**解决**: 从Cell 22复制正确的ID

---

## 📚 详细文档

- **完整指南**: [docs/NOTEBOOK_VERSION_MANAGEMENT.md](./NOTEBOOK_VERSION_MANAGEMENT.md)
- **存储架构**: [docs/BACKTEST_RESULT_STORAGE.md](./BACKTEST_RESULT_STORAGE.md)
- **缓存机制**: [docs/NOTEBOOK_CACHE_UPDATE.md](./NOTEBOOK_CACHE_UPDATE.md)

---

## 💾 数据库查询

### 查询最新结果

```python
from core.market_trend_storage import MarketTrendStorage

storage = MarketTrendStorage()
results = storage.query_backtest_results(
    backtest_type='signal_phase2',
    limit=1,
    sort_by='created_at',
    sort_order=-1
)
```

### 加载指定结果

```python
result = storage.load_backtest_result('结果ID')
```

### 查询特定版本

```python
results = storage.query_backtest_results(
    backtest_type='signal_phase2',
    filters={'version_tag': 'v1.0'}
)
```

---

## 🎯 最佳实践速记

1. ✅ **每次修改算法** → `USE_CACHE=False`
2. ✅ **设置有意义的标签** → `VERSION_TAG='描述性名称'`
3. ✅ **对比2-3个版本** → 不要一次对比太多
4. ✅ **关注准确率提升** → > 2%为显著改进
5. ✅ **定期清理测试版本** → 保持数据库整洁

---

**最后更新**: 2026-01-04  
**相关Notebook**: `notebooks/research/01_市场趋势判断回测验证.ipynb`
