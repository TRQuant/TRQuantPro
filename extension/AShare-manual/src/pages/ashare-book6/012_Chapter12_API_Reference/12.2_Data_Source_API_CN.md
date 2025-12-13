---
title: "12.2 数据源API"
description: "深入解析TRQuant数据源API接口，包括数据获取、数据查询、数据更新、数据源管理等接口的详细定义和使用方法"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 📡 12.2 数据源API

> **核心摘要：**
> 
> 本节系统介绍TRQuant数据源API接口，包括数据获取、数据查询、数据更新、数据源管理等接口的详细定义和使用方法。通过理解数据源API，帮助开发者掌握数据获取和处理的详细方法，为系统集成和扩展奠定基础。

TRQuant系统支持多种数据源（JQData、AKShare、Baostock、本地缓存），提供统一的数据源管理接口。本节详细说明数据源API的定义、参数说明、返回值格式等。

## 📋 章节概览

<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}
</script>

<div class="section-overview">
  <div class="section-item" onclick="scrollToSection('section-12-2-1')">
    <h4>🔌 12.2.1 数据源管理</h4>
    <p>数据源初始化、状态查询、数据源选择</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-12-2-2')">
    <h4>📊 12.2.2 价格数据获取</h4>
    <p>获取价格数据、数据格式、数据频率</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-12-2-3')">
    <h4>📈 12.2.3 基本面数据获取</h4>
    <p>获取基本面数据、财务指标、公司信息</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-12-2-4')">
    <h4>🔄 12.2.4 数据更新与缓存</h4>
    <p>数据更新、缓存管理、数据同步</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解数据源API**：掌握数据源API接口的定义和使用方法
- **获取数据**：掌握价格数据和基本面数据的获取方法
- **管理数据源**：掌握数据源状态查询和数据源选择方法
- **处理数据**：掌握数据格式转换和数据处理方法

## 📚 核心概念

### 数据源类型

- **JQData**：聚宽数据，主要数据源，支持实时和历史数据
- **AKShare**：免费数据源，支持A股历史数据
- **Baostock**：免费数据源，支持A股历史数据
- **本地缓存**：MongoDB缓存，提升数据获取速度

### 数据格式

- **价格数据**：DataFrame格式，索引为日期，列为字段（open、close、high、low、volume等）
- **基本面数据**：Dict格式，包含财务指标、公司信息等

<h2 id="section-12-2-1">🔌 12.2.1 数据源管理</h2>

数据源管理提供数据源初始化、状态查询、数据源选择等功能。

### 初始化数据源

```python
from core.data_source_manager import DataSourceManager

# 创建数据源管理器
ds_manager = DataSourceManager()

# 初始化所有数据源
success = ds_manager.initialize()
if success:
    print("数据源初始化成功")
else:
    print("数据源初始化失败")
```

### 查询数据源状态

```python
# 获取所有数据源状态
all_status = ds_manager.get_all_status()
for source_type, status in all_status.items():
    print(f"{source_type.value}: {status.is_available}")

# 获取指定数据源状态
from core.data_source_manager import DataSourceType
jq_status = ds_manager.get_source_status(DataSourceType.JQDATA)
if jq_status:
    print(f"JQData状态: {jq_status.is_available}")
    print(f"账户类型: {jq_status.account_type.value}")
    print(f"日期范围: {jq_status.start_date} ~ {jq_status.end_date}")

# 获取JQData账户类型
account_type = ds_manager.get_jqdata_account_type()
print(f"JQData账户类型: {account_type.value}")
```

### 获取可用日期范围

```python
# 获取所有数据源的最大日期范围
start_date, end_date = ds_manager.get_available_date_range()
print(f"可用日期范围: {start_date} ~ {end_date}")

# 获取指定数据源的日期范围
jq_start, jq_end = ds_manager.get_available_date_range(DataSourceType.JQDATA)
print(f"JQData日期范围: {jq_start} ~ {jq_end}")
```

<h2 id="section-12-2-2">📊 12.2.2 价格数据获取</h2>

价格数据获取提供统一的价格数据获取接口，支持多种数据频率和字段。

### 获取价格数据

```python
from core.data_source_manager import DataSourceManager, DataSourceType

# 初始化数据源管理器
ds_manager = DataSourceManager()
ds_manager.initialize()

# 获取价格数据
result = ds_manager.get_price(
    code="000001.XSHE",  # 股票代码
    start_date="2024-01-01",  # 开始日期
    end_date="2024-12-31",  # 结束日期
    frequency="daily",  # 数据频率: "daily", "1m", "5m", "15m", "30m", "60m"
    fields=["open", "close", "high", "low", "volume"],  # 字段列表
    prefer_source=None  # 优先数据源（可选）
)

# 检查结果
if result.success:
    data = result.data
    print(f"数据源: {result.source.value}")
    print(f"数据形状: {data.shape}")
    print(data.head())
else:
    print(f"获取数据失败: {result.error}")
```

### 数据格式说明

价格数据返回`DataFrame`格式：

- **索引**：日期（DatetimeIndex）
- **列**：字段名（open、close、high、low、volume等）
- **数据类型**：float64（价格和成交量）

```python
# 示例数据格式
#            open   close   high    low     volume
# 2024-01-02 10.50  10.60  10.70  10.45  1000000
# 2024-01-03 10.60  10.55  10.65  10.50   950000
# ...
```

### 数据频率支持

- **daily**：日线数据（默认）
- **1m**：1分钟数据
- **5m**：5分钟数据
- **15m**：15分钟数据
- **30m**：30分钟数据
- **60m**：60分钟数据

**注意**：不同数据源支持的数据频率不同：
- JQData：支持所有频率
- AKShare：仅支持日线数据
- Baostock：仅支持日线数据

### 指定数据源

```python
# 优先使用JQData
result = ds_manager.get_price(
    code="000001.XSHE",
    start_date="2024-01-01",
    end_date="2024-12-31",
    prefer_source=DataSourceType.JQDATA
)

# 如果JQData失败，自动降级到AKShare
# 如果AKShare失败，自动降级到Baostock
# 如果所有数据源都失败，返回错误
```

<h2 id="section-12-2-3">📈 12.2.3 基本面数据获取</h2>

基本面数据获取提供财务指标、公司信息等基本面数据。

### 获取基本面数据

```python
from core.data_source_manager import DataSourceManager

# 初始化数据源管理器
ds_manager = DataSourceManager()
ds_manager.initialize()

# 获取最新基本面数据
fundamentals = ds_manager.get_fundamentals(
    security="000001.XSHE",
    date=None  # None表示最新数据
)

# 获取指定日期的基本面数据
fundamentals = ds_manager.get_fundamentals(
    security="000001.XSHE",
    date="2024-12-01"
)

# 查看基本面数据
print(f"PE: {fundamentals.get('pe', 'N/A')}")
print(f"PB: {fundamentals.get('pb', 'N/A')}")
print(f"ROE: {fundamentals.get('roe', 'N/A')}")
print(f"总市值: {fundamentals.get('market_cap', 'N/A')}")
```

### 基本面数据字段

基本面数据包含以下字段：

- **财务指标**：PE、PB、PS、ROE、ROA、净利润率等
- **市值信息**：总市值、流通市值、总股本、流通股本等
- **公司信息**：公司名称、行业、地区等

<h2 id="section-12-2-4">🔄 12.2.4 数据更新与缓存</h2>

数据更新与缓存提供数据更新、缓存管理、数据同步等功能。

### 数据缓存

系统自动缓存数据到MongoDB，提升数据获取速度：

**设计原理**：
- **自动缓存**：首次获取数据时自动缓存，后续获取相同数据时从缓存读取
- **缓存键设计**：基于股票代码、日期范围、数据类型生成唯一缓存键
- **缓存策略**：历史数据永久缓存，实时数据设置TTL（Time To Live）

**为什么这样设计**：
1. **性能优化**：缓存避免重复请求数据源，大幅提升数据获取速度
2. **成本控制**：减少数据源API调用次数，降低数据获取成本
3. **可用性**：数据源不可用时，可以从缓存获取历史数据

**使用场景**：
- 重复获取相同数据时，自动使用缓存
- 数据源故障时，可以从缓存获取历史数据
- 批量获取数据时，缓存显著提升效率

**注意事项**：
- 缓存基于数据范围，部分重叠的数据不会复用缓存
- 实时数据需要设置TTL，避免使用过期数据
- 缓存占用存储空间，需要定期清理

```python
# 首次获取数据（从数据源获取并缓存）
# 设计原理：首次获取时，数据源返回数据后自动缓存到MongoDB
# 缓存键：基于code、start_date、end_date、frequency生成
result = ds_manager.get_price(
    code="000001.XSHE",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

# 再次获取相同数据（从缓存获取，速度更快）
# 设计原理：缓存命中时，直接从MongoDB读取，避免请求数据源
# 性能提升：缓存读取速度比数据源API快10-100倍
result = ds_manager.get_price(
    code="000001.XSHE",
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

### 数据更新

```python
# 更新指定股票的数据
ds_manager.update_data(
    code="000001.XSHE",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

# 更新所有股票的数据（谨慎使用，可能耗时较长）
ds_manager.update_all_data()
```

### 缓存管理

```python
# 清除指定股票的缓存
ds_manager.clear_cache(code="000001.XSHE")

# 清除所有缓存
ds_manager.clear_all_cache()

# 查看缓存状态
cache_status = ds_manager.get_cache_status()
print(f"缓存大小: {cache_status['size']}")
print(f"缓存文件数: {cache_status['file_count']}")
```

## 🔗 相关章节

- **12.1 模块API**：了解数据源管理模块的API接口
- **12.3 配置参考**：了解数据源配置参数
- **第2章：数据源**：了解数据源的详细功能

## 💡 关键要点

1. **统一接口**：所有数据源使用统一的API接口
2. **自动降级**：数据源失败时自动降级到备用数据源
3. **数据缓存**：自动缓存数据，提升获取速度
4. **数据格式**：统一的数据格式，便于处理

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了数据源API接口，包括数据获取、数据查询、数据更新、数据源管理等接口的详细定义和使用方法。通过理解数据源API，帮助开发者掌握数据获取和处理的详细方法。</p>
  
  <h3>下节预告</h3>
  <p>掌握了数据源API后，下一节将介绍配置参考，详细说明系统配置参数、数据库配置、数据源配置、策略配置等。通过理解配置参考，帮助开发者掌握系统配置的详细方法。</p>
  
  <a href="/ashare-book6/012_Chapter12_API_Reference/12.3_Config_Reference_CN" class="next-section">
    继续学习：12.3 配置参考 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
