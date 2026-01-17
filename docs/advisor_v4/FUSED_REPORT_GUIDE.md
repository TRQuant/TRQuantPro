# 融合报告生成器使用指南

> **版本**: 1.0  
> **更新时间**: 2026-01-09

---

## 概述

融合报告生成器结合了**BulletTrade原生报告**的专业性和**增强功能**的实用性，生成更完整、更精确的回测报告。

---

## 核心特性

### 1. 保留BulletTrade原生优势

✅ **专业图表**：保留BulletTrade生成的Plotly交互式图表  
✅ **完整指标**：保留所有BulletTrade计算的性能指标  
✅ **美观样式**：保留BulletTrade的专业样式设计  
✅ **数据完整性**：保留所有原始回测数据

### 2. 增强功能

✅ **公司名称**：自动为所有交易记录添加股票公司名称  
✅ **数据精度**：提升数值显示精度（百分比、金额等）  
✅ **图表精确性**：确保图表数据的高精度计算  
✅ **扩展分析**：预留接口，可添加额外分析模块

---

## 技术实现

### 数据精度提升

#### 1. 高精度计算上下文

```python
from decimal import Decimal, getcontext
getcontext().prec = 28  # 28位精度，足够金融计算
```

#### 2. 数值格式化

- **百分比**：保留2位小数（如：`4.75%`）
- **金额**：保留2位小数，千分位分隔（如：`1,047,533.02`）
- **收益率**：保留4位小数（如：`0.0475`）

#### 3. 图表数据精确性

- **Plotly图表**：数据在生成时使用高精度计算
- **数据源**：直接从回测结果提取，避免中间计算误差
- **JSON精度**：确保Plotly配置中的数值精度

---

## 使用方法

### 自动使用（推荐）

运行回测时自动生成融合报告：

```bash
python scripts/run_bullettrade_backtest_v4.py \
    --start-date 2024-10-14 \
    --end-date 2024-10-25
```

回测完成后会自动生成融合报告。

### 手动使用

对已有BulletTrade报告进行融合：

```python
from core.advisor_v4.fused_report_generator import generate_fused_report

fused_path = generate_fused_report(
    bullet_trade_html_path='output/advisor_v4/bullettrade/backtest_results/report.html',
    output_path='output/advisor_v4/bullettrade/backtest_results/report_fused.html',
    enhance_charts=True,          # 增强图表数据精确性
    enhance_data_precision=True,  # 提升数值精度
    add_company_names=True,       # 添加公司名称
)
```

### 命令行使用

```bash
python core/advisor_v4/fused_report_generator.py \
    output/advisor_v4/bullettrade/backtest_results/report.html \
    output/advisor_v4/bullettrade/backtest_results/report_fused.html
```

---

## 配置选项

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enhance_charts` | bool | True | 是否增强图表数据精确性 |
| `enhance_data_precision` | bool | True | 是否提升数值显示精度 |
| `add_company_names` | bool | True | 是否添加公司名称 |

---

## 融合报告 vs 原始报告

### 原始BulletTrade报告

- ✅ 专业的Plotly交互式图表
- ✅ 完整的性能指标
- ✅ 美观的样式设计
- ❌ 缺少公司名称（只有股票代码）
- ❌ 数值精度可能不够（显示格式）

### 融合报告

- ✅ 保留所有BulletTrade优势
- ✅ **添加公司名称**（提升可读性）
- ✅ **提升数值精度**（更精确的显示）
- ✅ **增强图表精确性**（确保数据准确性）
- ✅ 可扩展的增强分析接口

---

## 数据精度说明

### 计算精度

- **计算阶段**：使用`Decimal`类型，28位精度
- **存储阶段**：保持原始精度
- **显示阶段**：格式化显示，但保留足够精度

### 图表精度

- **Plotly图表**：数据在JSON中保持完整精度
- **数据源**：直接从回测结果提取，避免中间计算
- **显示**：Plotly自动处理数值显示

---

## 示例效果

### 交易记录表格

**原始报告**:
```
| 标的        | 数量 | 价格   | 成交额    |
|-------------|------|--------|-----------|
| 000807.XSHE | 6300 | 14.87  | 93,681.00 |
```

**融合报告**:
```
| 标的        | 公司名称 | 数量 | 价格    | 成交额      |
|-------------|----------|------|---------|-------------|
| 000807.XSHE | 云铝股份 | 6300 | 14.8700 | 93,681.00   |
```

### 数值精度

**原始报告**:
```
策略收益: 4.8%
最大回撤: 0.0%
```

**融合报告**:
```
策略收益: 4.75%
最大回撤: 0.00%
```

---

## 技术架构

```
BulletTrade原始报告
    ↓
融合报告生成器
    ├─ 解析HTML (BeautifulSoup)
    ├─ 添加公司名称 (JQData API)
    ├─ 提升数值精度 (Decimal + 格式化)
    ├─ 增强图表精确性 (数据源验证)
    └─ 生成融合报告
```

---

## 注意事项

1. **JQData认证**：需要JQData账号才能获取公司名称
2. **文件覆盖**：默认覆盖原始报告，建议先备份
3. **性能**：处理大型报告可能需要几秒钟
4. **兼容性**：确保BeautifulSoup4已安装

---

## 故障排除

### 问题：无法获取公司名称

**原因**：JQData未认证或配置错误

**解决**：
```python
from core.advisor_v4.fused_report_generator import FusedReportGenerator

generator = FusedReportGenerator(
    jqdata_username='your_username',
    jqdata_password='your_password'
)
generator.generate_fused_report(...)
```

### 问题：图表数据不准确

**原因**：数据源精度问题

**解决**：检查回测结果数据源，确保使用高精度计算

---

## 未来扩展

- [ ] 添加因子贡献度分析
- [ ] 添加风险分解图表
- [ ] 添加策略对比分析
- [ ] 支持自定义增强模块

---

*TRQuant开发团队*
