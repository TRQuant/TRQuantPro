# HTML报告增强功能 - 添加公司名称

> **版本**: 1.0  
> **更新时间**: 2026-01-09

---

## 功能说明

在BulletTrade生成的HTML回测报告中，自动为所有交易记录表格添加"公司名称"列，提升报告可读性。

---

## 实现方式

### 1. 增强模块

**文件**: `core/advisor_v4/enhance_html_report.py`

**功能**:
- 解析HTML报告
- 识别所有包含股票代码的表格
- 通过JQData API获取股票名称
- 在股票代码列后插入"公司名称"列

### 2. 自动集成

**文件**: `scripts/run_bullettrade_backtest_v4.py`

**修改**: 在回测完成后自动调用增强功能

```python
# 增强HTML报告：添加公司名称
if result.report_path:
    from core.advisor_v4.enhance_html_report import enhance_html_report
    enhanced_path = enhance_html_report(result.report_path)
```

---

## 支持的表格类型

| 表格类型 | 列名识别 | 状态 |
|----------|----------|------|
| 每日持仓 | `标的` | ✅ 已支持 |
| 交易记录分组 | `标的` | ✅ 已支持 |
| trades.csv表格 | `security` | ✅ 已支持 |
| 分标的盈亏 | `code` | ✅ 已支持 |
| 开仓次数 | `标的` | ✅ 已支持 |

---

## 使用示例

### 自动使用（推荐）

运行回测时自动增强：

```bash
python scripts/run_bullettrade_backtest_v4.py \
    --start-date 2024-10-14 \
    --end-date 2024-10-25
```

回测完成后会自动增强HTML报告。

### 手动使用

对已有HTML报告进行增强：

```python
from core.advisor_v4.enhance_html_report import enhance_html_report

enhanced_path = enhance_html_report('output/advisor_v4/bullettrade/backtest_results/report.html')
print(f"增强后的报告: {enhanced_path}")
```

或使用命令行：

```bash
python core/advisor_v4/enhance_html_report.py \
    output/advisor_v4/bullettrade/backtest_results/report.html
```

---

## 技术细节

### 股票名称获取

使用JQData API批量获取：

```python
import jqdatasdk
securities = jqdatasdk.get_all_securities(['stock'], date=None)
name_map = {code: securities.loc[code, 'display_name'] for code in codes}
```

### HTML解析

使用BeautifulSoup解析和修改HTML：

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
# 查找表格，添加列
```

### 列识别逻辑

支持多种列名格式：
- `标的`
- `股票代码`
- `code`
- `security`

---

## 验证结果

最新回测报告验证：
- ✅ 14个交易记录表格全部添加了公司名称
- ✅ 公司名称正确显示（如：000807.XSHE → 云铝股份）
- ✅ 表格格式保持完整

---

## 示例效果

**增强前**:
```
| 标的        | 数量 | 价格 |
|-------------|------|------|
| 000807.XSHE | 6300 | 14.87|
```

**增强后**:
```
| 标的        | 公司名称 | 数量 | 价格 |
|-------------|----------|------|------|
| 000807.XSHE | 云铝股份 | 6300 | 14.87|
```

---

*TRQuant开发团队*
