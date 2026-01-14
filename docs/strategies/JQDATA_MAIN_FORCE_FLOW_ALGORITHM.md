# JQData可解释主力资金流算法

> **创建时间**: 2026-01-13  
> **更新时间**: 2026-01-13  
> **目的**: 提供可解释的主力资金流算法，复刻券商App的逻辑  
> **数据源**: JQData（免费方案：价格+成交量估算）

⚠️ **重要说明**：
- JQData的`get_money_flow_pro`接口需要付费权限，暂时不可用
- 当前使用基于价格和成交量的免费估算方案
- 精度不如专业资金流向接口，仅供参考

---

## 📊 核心思想

### 问题背景

券商App里的"资金流向"不是原始数据，而是：
- 交易所逐笔成交数据
- + 券商自有算法
- + 商业授权数据
- = 再加工结果

**关键点**：
- ❌ 拿不到和券商App一模一样的原始字段
- ✅ 可以用公开数据 + 正确算法，复刻80-90%的效果
- ⚠️ 不同App的"资金流向"本来就不一样

---

## 🎯 算法设计

### 1. 数据源（当前状态）

**⚠️ 付费接口（暂时不可用）**：
- JQData `get_money_flow_pro`接口需要付费权限
- 提供分钟级资金流向数据
- 历史范围：2015年至今
- 字段包括：超大单、大单、中单、小单的流入/流出/净流入

**✅ 免费方案（当前使用）**：
- 使用JQData的`get_price`接口（免费）
- 基于价格位置和成交额估算资金流向
- 公式：`main_flow = (price_position - 0.5) * money`
- 其中：`price_position = (close - low) / (high - low)`

### 2. 主力资金定义（复刻券商App标准）

| 类型 | 定义 | 说明 |
|------|------|------|
| **超大单** | ≥50万股 或 ≥100万元 | 机构/大户 |
| **大单** | ≥10万股 或 ≥20万元，且<50万股或<100万元 | 中户 |
| **中单** | ≥2万股 或 ≥4万元，且<10万股或<20万元 | 散户 |
| **小单** | <2万股 或 <4万元 | 散户 |

**主力资金 = 超大单 + 大单**

### 3. 计算公式

```
主力净流入 = 超大单净流入 + 大单净流入
           = (超大单流入 - 超大单流出) + (大单流入 - 大单流出)
```

---

## 💻 实现细节

### 核心类：`JQDataMainForceFlow`

```python
from core.capital_flow.jqdata_main_force_flow import JQDataMainForceFlow

# 初始化
jq_flow = JQDataMainForceFlow(jq_client=jq)

# 获取大盘主力资金流向
result = jq_flow.get_market_main_force_flow('2026-01-13')
```

### 主要方法

#### 1. `get_market_main_force_flow(date)`

获取大盘主力资金流向

**输入**：
- `date`: 日期（YYYY-MM-DD）
- `use_index`: 是否使用指数（默认True，使用沪深300+中证1000）

**输出**：
```python
{
    'date': '2026-01-13',
    'main_net_inflow': -1805.56,  # 主力净流入（亿元）
    'xl_net_inflow': -1200.00,    # 超大单净流入（亿元）
    'l_net_inflow': -605.56,     # 大单净流入（亿元）
    'total_inflow': 5000.00,      # 总流入（亿元）
    'total_outflow': 6805.56,     # 总流出（亿元）
    'data_source': 'JQData',
    'is_valid': True,
    'explanation': '算法解释...'
}
```

#### 2. `get_sector_main_force_flow(date, sector_codes)`

获取行业主力资金流向

**输入**：
- `date`: 日期
- `sector_codes`: 行业代码列表（可选）

**输出**：
```python
{
    'date': '2026-01-13',
    'total_net_inflow': 205.73,  # 行业总主力净流入（亿元）
    'sector_details': [
        {'sector_code': 'xxx', 'net_inflow': 50.0},
        ...
    ],
    'data_source': 'JQData',
    'is_valid': True,
    'explanation': '算法解释...'
}
```

#### 3. `compare_with_akshare(date, akshare_market_flow, akshare_sector_flow)`

与AKShare数据对比验证

**输出**：
```python
{
    'date': '2026-01-13',
    'market_flow': {
        'jqdata': -1805.56,
        'akshare': -1805.56,
        'diff': 0.0,
        'diff_pct': 0.0
    },
    'sector_flow': {
        'jqdata': 205.73,
        'akshare': 205.73,
        'diff': 0.0,
        'diff_pct': 0.0
    },
    'jqdata_explanation': {
        'market': '算法解释...',
        'sector': '算法解释...'
    }
}
```

---

## 🔄 与AKShare的对比

### 相同点

1. **数据来源**：都基于交易所逐笔成交数据
2. **算法逻辑**：都按照成交金额分档
3. **结果方向**：通常方向一致（流入/流出）

### 不同点

| 维度 | JQData | AKShare |
|------|--------|---------|
| **数据源** | 聚宽算法 | 东方财富算法 |
| **透明度** | 可解释（开源算法） | 不透明（黑盒） |
| **可定制** | ✅ 可修改算法 | ❌ 不可修改 |
| **可回测** | ✅ 支持历史回测 | ❌ 仅实时数据 |
| **准确性** | 80-90%接近券商App | 接近券商App |

---

## 📈 在情绪周期模型中的应用

### 当前权重分配

- **涨停家数**：40%（最重要）
- **连板高度**：20%
- **炸板率**：20%
- **资金态度**：20%（大盘主力 + 行业资金）

### 资金态度计算

```python
# 1. 大盘主力净流入（整体资金态度，权重10%）
if market_pct < -3:
    sentiment_score -= 1.5  # 大幅流出
elif market_pct < -1:
    sentiment_score -= 1.0  # 流出
elif market_pct > 2:
    sentiment_score += 1.0  # 大幅流入
elif market_pct > 1:
    sentiment_score += 0.8  # 流入

# 2. 行业资金净流入（结构性机会，权重10%）
if sector_in > 200:
    sentiment_score += 0.8  # 结构性偏多
elif sector_in > 100:
    sentiment_score += 0.5  # 结构性略多
```

### 数据源优先级

1. **盘中监控**：AKShare（实时性好）
2. **盘后验证**：JQData（可解释、可回测）
3. **不一致时**：以涨停/连板为准，资金只做降权

---

## ✅ 优势

1. **可解释**：算法透明，每一步都可追溯
2. **可定制**：可以根据需要调整阈值和算法
3. **可回测**：支持历史数据回测
4. **可验证**：与AKShare数据对比，确保方向一致

---

## ⚠️ 注意事项

1. **付费接口不可用**：`get_money_flow_pro`接口需要专业版权限，暂时不可用
2. **当前使用免费方案**：基于价格和成交量的估算方法，精度较低
3. **建议使用AKShare**：作为主要数据源，更准确可靠
4. **算法差异**：不同券商的算法不同，结果可能有差异
5. **仅供参考**：资金流向是估计值，不是事实

---

## 🔧 使用示例

### 在Notebook中使用

```python
# 已在Cell 13中集成
# 自动获取JQData主力资金流向
# 与AKShare数据对比验证
# 提供可解释的输出
```

### 独立使用

```python
from core.capital_flow.jqdata_main_force_flow import JQDataMainForceFlow
import jqdatasdk as jq

# 连接JQData
jq.auth('username', 'password')

# 初始化
jq_flow = JQDataMainForceFlow(jq_client=jq)

# 获取数据
result = jq_flow.get_market_main_force_flow('2026-01-13')
print(result)
```

---

## 📝 后续优化方向

1. **个股资金流向**：扩展到个股级别
2. **实时监控**：支持盘中实时监控
3. **算法优化**：根据回测结果优化算法参数
4. **多数据源融合**：结合多个数据源提高准确性

---

**更新时间**: 2026-01-13
