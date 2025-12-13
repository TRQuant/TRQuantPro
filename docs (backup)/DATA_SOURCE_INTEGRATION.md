# 数据源集成接口文档

## 📋 概述

五维评分系统支持多数据源切换，当前已实现AKShare，预留聚宽（JQData）和万德（Wind）接口。

## 🔌 支持的数据源

### 1. AKShare（当前使用）✅

- **状态**: 已启用
- **类型**: 免费开源
- **数据提供商**: 同花顺、东方财富
- **特点**: 
  - 免费使用
  - 数据更新及时
  - 覆盖A股主要数据

**API示例**:
```python
# 行业板块资金流向
ak.stock_fund_flow_industry(symbol='即时')

# 概念板块资金流向
ak.stock_fund_flow_concept(symbol='即时')

# 涨停池
ak.stock_zt_pool_em(date='YYYYMMDD')

# 龙虎榜
ak.stock_lhb_detail_em(start_date, end_date)

# 北向资金
ak.stock_hsgt_fund_flow_summary_em()
```

---

### 2. 聚宽JQData（下一阶段）⏳

- **状态**: 待开通
- **类型**: 付费专业数据
- **数据提供商**: 聚宽
- **特点**:
  - Level2数据
  - 因子数据
  - 实时行情
  - 历史数据完整

**预留接口**:
```python
# 行业板块资金流向（预留）
jq.get_money_flow(industry='xxx')

# 概念板块资金流向（预留）
jq.get_concept_money_flow(concept='xxx')

# 涨停池（预留）
jq.get_limit_up_stocks(date='xxx')

# 龙虎榜（预留）
jq.get_dragon_tiger_list(date='xxx')

# 北向资金（预留）
jq.get_northbound_flow(date='xxx')
```

**接入步骤**:
1. 购买JQData账号
2. 安装JQData SDK: `pip install jqdatasdk`
3. 在`real_data_fetcher.py`中实现JQData数据获取方法
4. 在`five_dimension_engine.py`中启用JQData数据源

---

### 3. 万德Wind（未来扩展）⏳

- **状态**: 待开通
- **类型**: 机构级数据
- **数据提供商**: 万德
- **特点**:
  - 全球市场数据
  - 另类数据
  - 深度研报
  - 机构级数据质量

**预留接口**:
```python
# 行业板块资金流向（预留）
w.wsd(industry, 'money_flow', start_date, end_date)

# 概念板块资金流向（预留）
w.wsd(concept, 'money_flow', start_date, end_date)

# 涨停池（预留）
w.wset('limitup', date='xxx')

# 龙虎榜（预留）
w.wset('lhb', date='xxx')

# 北向资金（预留）
w.wsd('northbound', 'net_inflow', start_date, end_date)
```

**接入步骤**:
1. 购买Wind终端和API授权
2. 安装WindPy: `pip install WindPy`
3. 在`real_data_fetcher.py`中实现Wind数据获取方法
4. 在`five_dimension_engine.py`中启用Wind数据源

---

## 🔧 数据源切换

### 在UI中切换

每个维度Tab和综合评分Tab都提供数据源选择器：

```
数据源: [AKShare（免费） - ✅ 已启用 ▼]
        [聚宽JQData（付费） - ⏳ 待开通]
        [万德Wind（机构级） - ⏳ 待开通]
```

### 在代码中切换

```python
from markets.ashare.mainline.five_dimension_engine import FiveDimensionEngine, DataSourceType

# 使用AKShare（默认）
engine = FiveDimensionEngine(data_source=DataSourceType.AKSHARE)

# 切换到JQData（待实现）
engine = FiveDimensionEngine(data_source=DataSourceType.JQDATA)

# 切换到Wind（待实现）
engine = FiveDimensionEngine(data_source=DataSourceType.WIND)

# 动态切换
engine.set_data_source(DataSourceType.JQDATA)
```

---

## 📝 数据源适配器接口

### 需要实现的方法

在`real_data_fetcher.py`中，需要为每个数据源实现以下方法：

```python
class RealDataFetcher:
    def fetch_sector_flow(self, data_source: str = "akshare") -> DataFetchResult:
        """获取行业板块资金流向"""
        if data_source == "akshare":
            # 当前实现
            ...
        elif data_source == "jqdata":
            # TODO: 实现JQData接口
            return self._fetch_jqdata_sector_flow()
        elif data_source == "wind":
            # TODO: 实现Wind接口
            return self._fetch_wind_sector_flow()
    
    def fetch_concept_board(self, data_source: str = "akshare") -> DataFetchResult:
        """获取概念板块资金流向"""
        ...
    
    def fetch_market_sentiment(self, data_source: str = "akshare") -> DataFetchResult:
        """获取市场情绪（涨停池）"""
        ...
    
    def fetch_dragon_tiger(self, data_source: str = "akshare") -> DataFetchResult:
        """获取龙虎榜"""
        ...
    
    def fetch_northbound_flow(self, data_source: str = "akshare") -> DataFetchResult:
        """获取北向资金"""
        ...
```

### 数据格式统一

所有数据源返回的数据格式需要统一：

```python
# 行业/概念板块数据格式
{
    "sector_name": "板块名称",
    "change_pct": 涨跌幅(float),
    "main_net_inflow": 净流入(float),
    "inflow": 流入总额(float),
    "leader_stock": "龙头股票名称",
    "leader_change": 龙头涨幅(float),
}

# 涨停池数据格式
{
    "up_limit_count": 涨停总数(int),
    "continuous_limit": {连板数: 数量},
}

# 龙虎榜数据格式
[
    {
        "代码": "股票代码",
        "名称": "股票名称",
        "净买入额": 净买入额(float),
        "所属行业": "行业名称",
    }
]

# 北向资金数据格式
{
    "today_net": 当日净流入(float),
    "week_net": 本周净流入(float),
    "month_net": 本月净流入(float),
}
```

---

## 🚀 接入JQData（下一阶段）

### 1. 安装依赖

```bash
pip install jqdatasdk
```

### 2. 配置账号

```python
import jqdatasdk as jq
jq.auth('username', 'password')  # 或使用API Key
```

### 3. 实现数据获取方法

在`real_data_fetcher.py`中添加：

```python
def _fetch_jqdata_sector_flow(self) -> DataFetchResult:
    """使用JQData获取行业板块资金流向"""
    try:
        import jqdatasdk as jq
        
        # TODO: 实现JQData API调用
        # 示例（需要根据实际JQData API调整）
        # data = jq.get_money_flow(industry='all')
        
        return DataFetchResult(
            success=True,
            data=[],  # 转换后的数据
            source="jqdata",
            fetch_time=datetime.now(),
        )
    except Exception as e:
        logger.error(f"JQData获取失败: {e}")
        return DataFetchResult(
            success=False,
            data=None,
            source="jqdata",
            fetch_time=datetime.now(),
            error=str(e),
        )
```

### 4. 启用数据源

在`five_dimension_engine.py`中，JQData配置已预留，只需实现数据获取方法即可自动启用。

---

## 🚀 接入Wind（未来扩展）

### 1. 安装依赖

```bash
pip install WindPy
```

### 2. 配置Wind终端

- 安装Wind终端
- 获取API授权
- 启动Wind终端

### 3. 实现数据获取方法

在`real_data_fetcher.py`中添加：

```python
def _fetch_wind_sector_flow(self) -> DataFetchResult:
    """使用Wind获取行业板块资金流向"""
    try:
        from WindPy import w
        w.start()
        
        # TODO: 实现Wind API调用
        # 示例（需要根据实际Wind API调整）
        # data = w.wsd(industry_list, 'money_flow', start_date, end_date)
        
        return DataFetchResult(
            success=True,
            data=[],  # 转换后的数据
            source="wind",
            fetch_time=datetime.now(),
        )
    except Exception as e:
        logger.error(f"Wind获取失败: {e}")
        return DataFetchResult(
            success=False,
            data=None,
            source="wind",
            fetch_time=datetime.now(),
            error=str(e),
        )
```

---

## 📊 数据源对比

| 特性 | AKShare | JQData | Wind |
|------|---------|--------|------|
| **费用** | 免费 | 付费 | 机构级 |
| **数据质量** | 良好 | 优秀 | 优秀 |
| **Level2数据** | ❌ | ✅ | ✅ |
| **实时性** | 良好 | 优秀 | 优秀 |
| **历史数据** | 有限 | 完整 | 完整 |
| **全球市场** | ❌ | 有限 | ✅ |
| **另类数据** | ❌ | 有限 | ✅ |
| **API稳定性** | 良好 | 优秀 | 优秀 |

---

## 🔄 数据源优先级

系统按以下优先级选择数据源：

1. **用户选择的数据源**（如果可用）
2. **AKShare**（默认，始终可用）
3. **缓存数据**（如果API失败）

---

## 📌 注意事项

1. **数据格式统一**: 所有数据源返回的数据格式必须统一，便于引擎处理
2. **错误处理**: 如果选择的数据源不可用，自动回退到AKShare
3. **缓存机制**: 所有数据源都支持MongoDB缓存，减少API调用
4. **数据源状态**: UI中显示数据源状态（已启用/待开通），避免用户困惑

---

## 🎯 下一步计划

1. **阶段1（当前）**: ✅ AKShare数据源已实现
2. **阶段2（下一阶段）**: ⏳ 接入聚宽JQData
3. **阶段3（未来）**: ⏳ 接入万德Wind

---

*最后更新: 2024-12-19*

