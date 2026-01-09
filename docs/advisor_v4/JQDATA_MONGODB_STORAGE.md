# JQData MongoDB存储模块

> **更新时间**: 2026-01-09  
> **目的**: 将JQData下载的数据存入MongoDB，后续直接调用，不用重复下载

---

## 📋 概述

`JQDataMongoDBStorage` 模块将JQData下载的数据存入MongoDB，实现：
- ✅ 数据持久化存储
- ✅ 避免重复下载
- ✅ 快速数据访问
- ✅ 自动去重和版本管理

---

## 🏗️ 架构设计

### 数据存储策略

```
JQData API
    ↓
DataPreloader (下载)
    ↓
JQDataMongoDBStorage (保存到MongoDB)
    ↓
MongoDB (持久化存储)
    ↓
后续调用 (直接从MongoDB读取)
```

### MongoDB集合

| 集合名称 | 用途 | 索引 |
|---------|------|------|
| `jqdata_daily_prices` | 日线价格数据 | `(code, date)`, `period_key` |
| `jqdata_valuation` | 估值数据 | `(code, date)`, `period_key` |
| `jqdata_indicator` | 财务指标数据 | `(code, date)`, `period_key` |
| `jqdata_trade_days` | 交易日数据 | `period_key` |
| `jqdata_index_stocks` | 指数成分股数据 | `(index_code, date)` |
| `jqdata_metadata` | 元数据 | - |

---

## 💻 使用方法

### 基本使用

```python
from core.advisor_v4.jqdata_mongodb_storage import JQDataMongoDBStorage
from core.advisor_v4.data_preloader import DataPreloader

# 创建存储管理器
storage = JQDataMongoDBStorage()

# 创建数据预加载器（默认启用MongoDB）
preloader = DataPreloader(use_mongodb=True)

# 预加载数据（自动保存到MongoDB）
result = preloader.preload_market_data(
    start_date="2024-10-08",
    end_date="2024-12-31",
    force_refresh=False  # 如果MongoDB中已有数据，不会重复下载
)
```

### 手动保存数据

```python
import pandas as pd
from core.advisor_v4.jqdata_mongodb_storage import JQDataMongoDBStorage

storage = JQDataMongoDBStorage()

# 保存价格数据
prices_df = pd.DataFrame(...)  # 价格数据
storage.save_daily_prices(
    df=prices_df,
    period_key="2024H2",
    start_date="2024-10-08",
    end_date="2024-12-31"
)

# 保存基本面数据
valuation_df = pd.DataFrame(...)  # 估值数据
storage.save_fundamentals(
    df=valuation_df,
    data_type="valuation",
    period_key="2024H2",
    date="2024-10-08"
)
```

### 加载数据

```python
# 从MongoDB加载价格数据
prices_df = storage.load_daily_prices(period_key="2024H2")

# 从MongoDB加载基本面数据
valuation_df = storage.load_fundamentals(
    data_type="valuation",
    period_key="2024H2",
    date="2024-10-08"
)

# 从MongoDB加载交易日数据
trade_days = storage.load_trade_days(period_key="2024H2")
```

### 检查数据是否存在

```python
# 检查价格数据是否存在
exists = storage.check_data_exists("daily_prices", "2024H2")

# 检查基本面数据是否存在
exists = storage.check_data_exists("valuation", "2024H2", date="2024-10-08")
```

---

## 🔧 DataPreloader集成

### 自动MongoDB存储

`DataPreloader` 已集成MongoDB存储，默认启用：

```python
from core.advisor_v4.data_preloader import DataPreloader

# 启用MongoDB存储（默认）
preloader = DataPreloader(use_mongodb=True)

# 预加载数据（自动保存到MongoDB）
result = preloader.preload_market_data(
    start_date="2024-10-08",
    end_date="2024-12-31"
)

# 后续调用时，如果MongoDB中已有数据，不会重复下载
result = preloader.preload_market_data(
    start_date="2024-10-08",
    end_date="2024-12-31",
    force_refresh=False  # 从MongoDB加载
)
```

### 数据加载优先级

1. **MongoDB**（如果启用且数据存在）
2. **Parquet文件**（如果MongoDB不可用或数据不存在）
3. **JQData API**（如果缓存中都没有）

---

## 📊 数据格式

### 价格数据

```python
{
    "code": "000001.XSHE",
    "time": "2024-10-08",
    "open": 10.5,
    "high": 10.8,
    "low": 10.3,
    "close": 10.6,
    "volume": 1000000,
    "money": 10600000,
    "period_key": "2024H2",
    "start_date": "2024-10-08",
    "end_date": "2024-12-31",
    "created_at": datetime
}
```

### 基本面数据

```python
{
    "code": "000001.XSHE",
    "date": "2024-10-08",
    "market_cap": 1000000000,
    "pe_ratio": 15.5,
    "pb_ratio": 2.3,
    "period_key": "2024H2",
    "created_at": datetime
}
```

### 交易日数据

```python
{
    "period_key": "2024H2",
    "trade_days": ["2024-10-08", "2024-10-09", ...],
    "start_date": "2024-10-08",
    "end_date": "2024-12-31",
    "updated_at": datetime
}
```

---

## ⚙️ 配置

### MongoDB连接

默认配置：
- **URI**: `mongodb://localhost:27017`
- **数据库**: `trquant_jqdata`

自定义配置：
```python
storage = JQDataMongoDBStorage(
    mongo_uri="mongodb://localhost:27017",
    db_name="trquant_jqdata"
)
```

### 文件存储备用

如果MongoDB不可用，自动使用文件存储：
- **路径**: `~/.local/share/trquant/jqdata/`
- **格式**: Parquet

---

## 🔍 数据查询

### 获取存储统计

```python
stats = storage.get_storage_stats()
print(stats)
# {
#     "connected": True,
#     "db_name": "trquant_jqdata",
#     "collections": {
#         "daily_prices": {"count": 1000000, "collection": "jqdata_daily_prices"},
#         "valuation": {"count": 500000, "collection": "jqdata_valuation"},
#         ...
#     }
# }
```

---

## ⚠️ 注意事项

1. **MongoDB连接**: 确保MongoDB服务正在运行
2. **数据去重**: 使用 `(code, date)` 或 `period_key` 作为唯一索引，自动去重
3. **版本管理**: 使用 `period_key` 管理不同时间段的数据
4. **增量更新**: 支持按日期增量更新基本面数据
5. **文件备用**: 如果MongoDB不可用，自动降级到文件存储

---

## 📚 相关文档

- **数据预加载器**: `docs/advisor_v4/COMPLETE_BACKTEST_REPORT.md`
- **MongoDB设置**: `docs/02_development_guides/MONGODB_SETUP.md`
- **系统架构**: `docs/advisor_v4/ADVISOR_V4_SYSTEM_ARCHITECTURE.md`

---

**最后更新**: 2026-01-09  
**维护者**: TRQuant Team
