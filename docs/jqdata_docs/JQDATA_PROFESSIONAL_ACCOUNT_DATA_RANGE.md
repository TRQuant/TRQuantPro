# 聚宽正式账号（股票专业版）历史数据期限

> **更新时间**: 2025-01-01  
> **数据来源**: 聚宽官方文档 + 网络验证  
> **账号类型**: 股票专业版（正式账号）

---

## 📊 历史数据起始日期

根据聚宽官方信息，**正式账号（股票专业版）**可获取的历史数据范围如下：

| 数据类型 | 起始日期 | 说明 |
|---------|---------|------|
| **股票数据** | **2005年1月1日** | 沪深A股历史行情数据 |
| **指数数据** | **2005年1月1日** | 各类指数历史数据 |
| **基金数据** | **2005年1月1日** | 场内基金历史数据 |
| **期货数据** | **2010年1月1日** | 期货合约历史数据（从合约上市日期开始） |
| **宏观经济数据** | **2000年1月1日** | 宏观经济指标数据（部分可追溯至1990年代） |

---

## ⚠️ 重要说明

### 1. 正式账号 vs 试用账号

| 项目 | 试用账号 | 正式账号（股票专业版） |
|------|----------|---------------------|
| **历史数据范围** | 前15个月~前3个月 | **2005-01-01 至今**（股票数据） |
| **数据限制** | 有期限限制 | **无限制** |
| **实时数据** | ❌ 不支持 | ✅ 支持 |
| **数据起始日期** | 动态滚动（相对日期） | **固定起始日期（2005-01-01）** |

### 2. 数据范围计算

**正式账号**：
- **开始日期**：`2005-01-01`（固定）
- **结束日期**：`今天`（或昨天，取决于数据更新时间）
- **总历史跨度**：约**20年**（从2005年到2025年）

**示例**（当前日期：2025-01-01）：
- 可获取的最早股票数据：`2005-01-01`
- 可获取的最新股票数据：`2024-12-31`（或更早，取决于数据延迟）

---

## 🔍 验证方法

### 方法1: 使用API查询账号信息

```python
from jqdatasdk import auth, get_account_info

# 认证
auth('your_username', 'your_password')

# 获取账号信息
account_info = get_account_info()
print(account_info)

# 查看数据范围
# 正式账号的date_range_start可能是None或2005-01-01
# date_range_end是今天或昨天
```

### 方法2: 尝试获取历史数据

```python
import jqdatasdk as jq

# 尝试获取2005-01-01的数据
try:
    data = jq.get_price(
        '000001.XSHE',  # 平安银行
        start_date='2005-01-01',
        end_date='2005-01-10',
        frequency='daily',
        fields=['close']
    )
    if data is not None and len(data) > 0:
        print("✅ 可以获取2005年数据")
        print(f"最早数据日期: {data.index.min()}")
    else:
        print("❌ 无法获取2005年数据")
except Exception as e:
    error_msg = str(e)
    if "账号权限仅能获取" in error_msg:
        # 解析错误信息中的日期范围
        print(f"权限限制: {error_msg}")
    else:
        print(f"其他错误: {e}")
```

### 方法3: 查看项目中的权限检测代码

项目中的权限检测代码位于：
- `jqdata/client.py` - `DataPermission`类
- `markets/ashare/stock_pool/data_layer.py` - `JQDataProvider._detect_permission()`方法

---

## 📝 使用建议

### 1. 历史数据回测

正式账号可以访问**20年历史数据**（2005-2025），非常适合：

- ✅ **长期策略回测**：可以回测10年、15年甚至20年的策略表现
- ✅ **市场周期分析**：包含多个完整的牛市、熊市、震荡市周期
- ✅ **因子有效性验证**：可以使用长期历史数据验证因子稳定性
- ✅ **极端市场测试**：包含2008年金融危机、2015年股灾等极端行情

### 2. 数据查询示例

```python
from jqdata.client import JQDataClient
from config.config_manager import get_config_manager

# 初始化
config_manager = get_config_manager()
jq_config = config_manager.get_jqdata_config()
jq_client = JQDataClient()
jq_client.authenticate(jq_config.get('username'), jq_config.get('password'))

# 获取20年历史数据（2005-01-01 至 2024-12-31）
historical_data = jq_client.get_price(
    stocks=['000001.XSHE', '600000.XSHG'],
    start_date='2005-01-01',
    end_date='2024-12-31',
    frequency='daily',
    fields=['open', 'high', 'low', 'close', 'volume']
)

print(f"数据范围: {historical_data.index.min()} 至 {historical_data.index.max()}")
print(f"总交易日数: {len(historical_data)}")
```

### 3. 主线研究数据范围建议

基于正式账号的数据范围，**市场主线研究**可以使用：

- **短期主线验证**（3-6个月）：使用最近1-2年数据
- **中期主线验证**（1-2年）：使用最近5年数据
- **长期主线验证**（3-5年）：使用最近10-15年数据
- **完整周期验证**：使用全部20年数据（2005-2025）

---

## 📚 相关文档

- [JQData基础数据范围](./JQDATA_BASIC_DATA_SCOPE.md) - 试用账号权限说明
- [市场主线研究完整指南](./MAINLINE_RESEARCH_COMPLETE_GUIDE.md) - 使用正式账号进行主线研究
- [JQData账号权限详情](./JQDATA_ACCOUNT_INFO.md) - 账号权限API说明

---

## ⚡ 快速参考

**正式账号历史数据起始日期**：
- 📈 **股票数据**: `2005-01-01`
- 📊 **指数数据**: `2005-01-01`
- 💰 **基金数据**: `2005-01-01`
- 📉 **期货数据**: `2010-01-01`
- 🌐 **宏观数据**: `2000-01-01`

**当前可获取的最新数据**：
- 最新日期：通常是`昨天`或`今天`（取决于数据更新延迟）
- 实时数据：✅ 支持（正式账号特性）

---

*最后更新: 2025-01-01 | 基于聚宽官方文档和网络验证*

