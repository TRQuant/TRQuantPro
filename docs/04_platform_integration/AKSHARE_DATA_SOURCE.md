# AKShare数据源使用指南

## ✅ 测试结果

**AKShare可以成功获取最近3个月的A股股价数据！**

### 测试数据
- 测试股票：000001 (平安银行), 600000 (浦发银行), 000002 (万科A)
- 数据量：每只股票59条（最近3个月）
- 数据完整性：✅ 开盘、收盘、最高、最低、成交量、成交额等

## 📋 使用方法

### 获取历史数据
```python
import akshare as ak
from datetime import datetime, timedelta

# 计算日期范围
end_date = datetime.now().strftime('%Y%m%d')
start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')

# 获取数据（注意：代码不含交易所后缀）
df = ak.stock_zh_a_hist(
    symbol="000001",  # 仅代码，不含.XSHE或.XSHG
    period="daily",
    start_date=start_date,  # YYYYMMDD格式
    end_date=end_date,
    adjust="qfq"  # 前复权，可选：qfq(前复权)/hfq(后复权)/""(不复权)
)

# 数据字段
# 日期、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率
```

### 获取实时价格
```python
# 获取所有A股实时行情
df_realtime = ak.stock_zh_a_spot_em()

# 查找特定股票
code = "000001"
matched = df_realtime[df_realtime['代码'] == code]
if len(matched) > 0:
    price = matched.iloc[0]['最新价']
```

## 🔄 代码格式转换

| JQData格式 | AKShare格式 |
|-----------|------------|
| 000001.XSHE | 000001 |
| 600000.XSHG | 600000 |

**注意**：AKShare不需要交易所后缀，只需要6位数字代码。

## ✅ 优势

1. **免费**：无API限制，无频率限制
2. **数据完整**：可以获取最近3个月甚至更久的历史数据
3. **实时数据**：可以获取实时行情
4. **数据质量**：支持前复权/后复权

## 🎯 在十倍股分析中的应用

已更新 `scripts/tenbagger_real_analysis.py`：
- ✅ 优先使用AKShare获取最近3个月数据
- ✅ 降级顺序：AKShare → AllTick → JQData
- ✅ 可以验证十倍股识别后的股价走势

## 📝 注意事项

1. **日期格式**：使用YYYYMMDD格式（如：20251220）
2. **代码格式**：仅使用6位数字代码，不含交易所后缀
3. **请求速度**：AKShare请求可能较慢，建议添加适当延迟
4. **数据更新**：数据可能有延迟，实时数据建议使用实时接口
