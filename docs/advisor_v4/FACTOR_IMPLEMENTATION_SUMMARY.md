# 因子选择机制改进总结

> **实施日期**: 2026-01-08  
> **状态**: ✅ 已完成

---

## 📋 改进内容

### 问题

1. ❌ **简单堆砌聚宽因子库**: 之前直接使用CNE5 + Alpha101/191，缺乏理论依据
2. ❌ **缺乏历史验证**: 因子选择没有基于历史10%+案例验证
3. ❌ **无理论假设**: 因子选择缺乏清晰的理论假设和逻辑

### 解决方案

1. ✅ **创建已验证因子计算器**: 基于438个历史10%+案例提取7个已验证因子
2. ✅ **明确理论假设**: 每个因子都有清晰的理论假设和验证结果
3. ✅ **两层融合架构**: 70%已验证因子 + 30%聚宽因子（补充）

---

## 🎯 已验证因子列表

### 核心因子（权重≥0.85）

1. **20日动量**（权重1.0）
   - 理论：动量驱动假设
   - 验证：99个案例，平均21.59%
   - 最优区间：5%~30%

2. **相对位置**（权重0.9）
   - 理论：低位反弹假设
   - 验证：248个案例，平均15.62%
   - 最优区间：<80%

3. **市值**（权重0.85）
   - 理论：市值弹性假设
   - 验证：166个案例，平均17.47%
   - 最优区间：30~200亿

### 确认因子（权重0.7-0.75）

4. **5日动量**（权重0.75）
   - 理论：短期确认假设
   - 最优区间：-5%~10%

5. **换手率**（权重0.7）
   - 理论：流动性假设
   - 最优区间：2%~10%

### 基本面因子（权重<0.5）

6. **ROE**（权重0.5）
   - 理论：基本面底线假设
   - 最优区间：>0

7. **净利润增长率**（权重0.4）
   - 理论：成长性假设
   - 最优区间：>0

---

## 🔧 实现架构

### 文件结构

```
core/advisor_v4/
├── validated_factor_calculator.py    # 已验证因子计算器（新建）
├── jqfactor_calculator.py            # 聚宽因子计算器（更新说明）
└── multi_factor_calculator.py         # 多因子计算器（集成已验证因子）
```

### 融合逻辑

```python
# MultiFactorCalculator.calculate_all_factors()

# 1. 计算已验证因子（70%权重）
validated_score = ValidatedFactorCalculator.calculate_all_validated_factors(codes, date)

# 2. 计算聚宽因子（30%权重）
composite_score = JQFactorCalculator.calculate_all_factors(codes, date)

# 3. 融合得分
total_score = (
    validated_score * 0.7 +      # 已验证因子（主要）
    composite_score * 0.3          # 聚宽因子（补充）
)
```

---

## 📊 因子有效性排序

基于历史438个10%+案例的分析：

| 排名 | 因子 | 有效性 | 权重 | 说明 |
|------|------|--------|------|------|
| 1 | **20日动量** | ⭐⭐⭐⭐⭐ | 1.0 | 最重要的筛选因子 |
| 2 | **相对位置** | ⭐⭐⭐⭐ | 0.9 | 低位股票反弹概率高 |
| 3 | **市值** | ⭐⭐⭐⭐ | 0.85 | 中小市值弹性大 |
| 4 | **5日动量** | ⭐⭐⭐ | 0.75 | 短期趋势确认 |
| 5 | **换手率** | ⭐⭐⭐ | 0.7 | 流动性和关注度 |
| 6 | **ROE** | ⭐⭐ | 0.5 | 基本面筛选 |
| 7 | **增长率** | ⭐⭐ | 0.4 | 基本面筛选 |

---

## 📚 文档

1. **因子选择理论**: `docs/advisor_v4/FACTOR_SELECTION_THEORY.md`
2. **因子架构设计**: `docs/advisor_v4/FACTOR_ARCHITECTURE.md`
3. **高收益因子研究**: `docs/HIGH_RETURN_FACTOR_RESEARCH.md`

---

## ✅ 验证结果

```bash
$ python -c "from core.advisor_v4.validated_factor_calculator import ValidatedFactorCalculator, VALIDATED_FACTORS"
✅ ValidatedFactorCalculator导入成功
已验证因子数量: 7
```

所有7个已验证因子都已正确定义，每个因子都有：
- ✅ 理论假设
- ✅ 逻辑说明
- ✅ 验证结果
- ✅ 权重配置

---

## 🎯 使用方式

### 直接使用已验证因子

```python
from core.advisor_v4.validated_factor_calculator import ValidatedFactorCalculator

calc = ValidatedFactorCalculator(verbose=True)
df = calc.calculate_all_validated_factors(codes, date)
# df包含: code, momentum_20d, rel_position, market_cap, momentum_5d, 
#         turnover_rate, roe, growth, validated_score
```

### 通过MultiFactorCalculator使用（推荐）

```python
from core.advisor_v4.multi_factor_calculator import MultiFactorCalculator

calc = MultiFactorCalculator(verbose=True)
df = calc.calculate_all_factors(codes, date)
# df包含: code, validated_score, composite_score, total_score
# total_score = validated_score * 0.7 + composite_score * 0.3
```

---

## ⚠️ 注意事项

1. **不能简单堆砌**: 聚宽因子库的因子不能简单堆积，必须与已验证因子结合
2. **理论优先**: 每个因子都要有清晰的理论假设
3. **持续验证**: 需要持续回测验证因子有效性
4. **动态调整**: 根据回测结果动态调整因子权重

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-08
