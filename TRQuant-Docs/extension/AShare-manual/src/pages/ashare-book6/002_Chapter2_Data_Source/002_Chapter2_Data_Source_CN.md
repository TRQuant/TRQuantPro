---
title: "第2章：数据源模块"
description: "深入解析数据源管理、数据质量检查、数据接口设计和数据存储架构，为量化投资系统提供统一的数据获取能力"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 📡 第2章：数据源模块

> **核心摘要：**
> 
> 本章系统介绍TRQuant系统的数据源模块设计，包括统一的数据源管理、多数据源支持、数据质量检查机制和数据存储架构。通过理解数据源接口抽象、数据质量保证、缓存策略和数据库集成，帮助开发者掌握数据获取的核心能力，为后续市场分析、因子计算、策略开发等模块提供高质量数据支撑。

## 📖 本章学习路径

按照以下顺序学习，构建完整的数据源模块认知：

<div class="chapters-grid">
  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">2.1</span>
      <h3>数据源管理</h3>
    </div>
    <p>深入了解统一数据源管理机制、多数据源支持和数据源选择与切换机制，理解数据源接口抽象设计。</p>
    <div class="chapter-features">
      <span class="feature-tag">📡 统一接口</span>
      <span class="feature-tag">🔄 多数据源</span>
      <span class="feature-tag">⚡ 智能选择</span>
    </div>
    <a href="/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">2.2</span>
      <h3>数据质量</h3>
    </div>
    <p>系统讲解数据完整性检查、准确性验证、异常检测与数据清洗方法，确保数据质量。</p>
    <div class="chapter-features">
      <span class="feature-tag">✅ 完整性检查</span>
      <span class="feature-tag">🔍 准确性验证</span>
      <span class="feature-tag">🚨 异常检测</span>
    </div>
    <a href="/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">2.3</span>
      <h3>数据存储架构</h3>
    </div>
    <p>详细介绍分层/多存储（Polyglot Persistence）架构设计，包括PostgreSQL、ClickHouse/TimescaleDB、Redis等技术选型。</p>
    <div class="chapter-features">
      <span class="feature-tag">🗄️ PostgreSQL</span>
      <span class="feature-tag">⏱️ 时序库</span>
      <span class="feature-tag">⚡ Redis缓存</span>
    </div>
    <a href="/ashare-book6/002_Chapter2_Data_Source/2.3_Data_Storage_Architecture_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">2.4</span>
      <h3>MCP工具集成</h3>
    </div>
    <p>掌握数据源相关的MCP工具使用，包括知识库查询、数据收集工具等，提升开发效率。</p>
    <div class="chapter-features">
      <span class="feature-tag">🔍 知识库查询</span>
      <span class="feature-tag">📥 数据收集</span>
      <span class="feature-tag">🛠️ 工具集成</span>
    </div>
    <a href="/ashare-book6/002_Chapter2_Data_Source/2.4_MCP_Tool_Integration_CN" class="chapter-link">开始学习 →</a>
  </div>
</div>

## 🎯 学习目标

通过本章学习，您将能够：

- **掌握数据源管理**：理解统一数据源管理机制，能够配置和管理多个数据源
- **理解数据质量保证**：掌握数据完整性、准确性、异常检测等质量检查方法
- **熟悉数据存储架构**：理解分层/多存储架构设计，掌握数据分布和缓存策略
- **使用MCP工具**：掌握使用MCP工具进行数据查询、数据收集和知识检索

## 📚 核心概念

### 数据源管理

- **统一接口抽象**：通过`BaseDataSource`基类定义统一的数据源接口
- **多数据源支持**：支持JQData、AKShare、TuShare、Wind等多个数据源
- **智能选择机制**：根据数据质量、完整性、速度等指标自动选择最优数据源
- **故障自动切换**：当主数据源不可用时，自动切换到备用数据源
- **回测数据源**：JQData是BulletTrade回测引擎的主要数据源，用于策略回测验证

### 数据质量保证

- **完整性检查**：检查缺失值、时间序列连续性、字段完整性
- **准确性验证**：验证数据范围、业务逻辑、数据一致性
- **异常检测**：使用统计方法、机器学习方法检测异常值和异常模式
- **自动清洗**：AI辅助识别和处理异常数据

### 数据存储架构

- **分层/多存储（Polyglot Persistence）**：根据数据类型选择最适合的存储方案
- **PostgreSQL**：存储数据源配置、元数据、审计日志
- **ClickHouse/TimescaleDB**：存储行情数据、因子数据、回测输出
- **Redis**：缓存行情快照、任务队列、风控状态
- **Parquet/HDF5**：文件缓存，适合早期阶段或小规模数据

### MCP工具集成

- **kb.query**：查询知识库，获取数据源相关的文档和代码
- **data_collector.crawl_web**：爬取网页内容，收集数据源相关信息
- **data_collector.download_pdf**：下载PDF文档，获取数据源使用手册
- **data_collector.collect_academic**：收集学术论文，研究数据源技术

<h2 id="section-2-1">📡 2.1 数据源管理</h2>

数据源管理是数据源模块的核心功能，负责统一管理多个数据源，提供数据源注册、选择、切换等功能。

### 模块定位

- **工作流位置**：步骤1 - 📡 信息获取
- **核心职责**：统一数据源管理、数据质量检查、数据接口抽象
- **服务对象**：所有后续步骤（市场分析、主线识别、因子计算等）

### 接口设计

数据源模块采用**接口抽象**设计，通过`BaseDataSource`基类定义统一的数据源接口，所有具体数据源实现都必须遵循这个接口。

#### 数据源基类接口

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import pandas as pd

class BaseDataSource(ABC):
    """数据源基类 - 定义统一接口"""
    
    def __init__(self, name: str):
        self.name = name
        self._connected = False
        self._last_error = None
    
    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self._connected
    
    @abstractmethod
    def connect(self) -> bool:
        """连接数据源"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """断开连接"""
        pass
    
    @abstractmethod
    def health_check(self) -> Dict:
        """
        健康检查
        
        Returns:
            {"status": "ok/error", "latency": ms, "error": "..."}
        """
        pass
    
    @abstractmethod
    def get_daily_data(self, symbol: str, start_date: str, 
                       end_date: str) -> pd.DataFrame:
        """
        获取日线数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            DataFrame with columns: date, open, high, low, close, volume, amount
        """
        pass
    
    @abstractmethod
    def get_minute_data(self, symbol: str, count: int = 240, 
                        period: str = "1m") -> pd.DataFrame:
        """获取分钟线数据"""
        pass
```

#### 数据源管理器接口

```python
class DataSourceManager:
    """数据源管理器 - 统一管理多个数据源"""
    
    def __init__(self, use_cache: bool = True):
        self.sources: Dict[str, BaseDataSource] = {}
        self.priority: Dict[str, List[str]] = {}  # 数据源优先级
        self.cache = None  # 缓存管理器
    
    def add_source(self, name: str, source: BaseDataSource):
        """添加数据源"""
        self.sources[name] = source
    
    def get_data(self, symbol: str, start_date: str, end_date: str,
                 data_type: str = "daily", source: str = None) -> pd.DataFrame:
        """
        获取数据（自动选择最优数据源）
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            data_type: 数据类型（daily, minute, tick）
            source: 指定数据源（可选，不指定则自动选择）
        
        Returns:
            DataFrame格式的数据
        """
        # 1. 如果指定了数据源，直接使用
        if source and source in self.sources:
            return self._fetch_from_source(source, symbol, start_date, end_date, data_type)
        
        # 2. 自动选择最优数据源
        selected_source = self.select_source(data_type)
        
        # 3. 尝试获取数据，失败则切换到备用数据源
        try:
            return self._fetch_from_source(selected_source, symbol, start_date, end_date, data_type)
        except Exception as e:
            logger.warning(f"数据源 {selected_source} 获取失败: {e}")
            # 故障切换
            return self._failover_fetch(symbol, start_date, end_date, data_type, selected_source)
    
    def select_source(self, data_type: str, criteria: List[str] = None) -> str:
        """
        选择最优数据源
        
        Args:
            data_type: 数据类型
            criteria: 选择标准（data_quality, completeness, speed, cost）
        
        Returns:
            选中的数据源名称
        """
        if criteria is None:
            criteria = ["data_quality", "completeness", "speed"]
        
        # 根据优先级和标准选择
        candidates = self.priority.get(data_type, list(self.sources.keys()))
        
        for source_name in candidates:
            if source_name in self.sources:
                source = self.sources[source_name]
                # 健康检查
                health = source.health_check()
                if health["status"] == "ok":
                    return source_name
        
        # 如果所有数据源都不可用，返回第一个
        return candidates[0] if candidates else list(self.sources.keys())[0]
```

### 支持的数据源

TRQuant系统支持以下数据源：

<div class="comparison-table">
  <table>
    <thead>
      <tr>
        <th>数据源</th>
        <th>类型</th>
        <th>优势</th>
        <th>适用场景</th>
        <th>状态</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>JQData</strong></td>
        <td>商业数据源</td>
        <td>数据质量高、覆盖全面、API稳定</td>
        <td>日线数据、基本面数据、因子数据、<strong>BulletTrade回测数据源</strong></td>
        <td>✅ 主数据源</td>
      </tr>
      <tr>
        <td><strong>AKShare</strong></td>
        <td>开源数据源</td>
        <td>免费、无限制、数据源丰富</td>
        <td>实时数据、板块轮动、资金流</td>
        <td>✅ 备用数据源</td>
      </tr>
      <tr>
        <td><strong>TuShare</strong></td>
        <td>开源数据源</td>
        <td>免费、数据更新及时</td>
        <td>日线数据、财务数据</td>
        <td>✅ 备用数据源</td>
      </tr>
      <tr>
        <td><strong>Wind</strong></td>
        <td>商业数据源</td>
        <td>数据权威、覆盖全面</td>
        <td>机构级数据需求</td>
        <td>⏳ 可选</td>
      </tr>
    </tbody>
  </table>
</div>

### 数据源选择策略

系统根据以下策略自动选择最优数据源：

1. **数据质量优先**：选择数据质量最高的数据源
2. **完整性优先**：选择数据最完整的数据源
3. **速度优先**：选择访问速度最快的数据源
4. **成本考虑**：在满足质量要求的前提下选择成本最低的数据源

### 故障自动切换

当主数据源不可用时，系统自动切换到备用数据源：

```python
def _failover_fetch(self, symbol: str, start_date: str, end_date: str,
                    data_type: str, failed_source: str) -> pd.DataFrame:
    """故障切换获取数据"""
    # 获取备用数据源列表
    candidates = self.priority.get(data_type, [])
    
    # 排除失败的数据源
    candidates = [s for s in candidates if s != failed_source]
    
    # 尝试备用数据源
    for source_name in candidates:
        if source_name in self.sources:
            try:
                return self._fetch_from_source(source_name, symbol, start_date, end_date, data_type)
            except Exception as e:
                logger.warning(f"备用数据源 {source_name} 也失败: {e}")
                continue
    
    # 所有数据源都失败，抛出异常
    raise Exception(f"所有数据源都不可用，无法获取数据: {symbol}")
```

### 使用示例

#### 基础使用

```python
from data_sources import DataSourceManager

# 初始化数据源管理器
ds_manager = DataSourceManager(use_cache=True)

# 连接所有数据源
ds_manager.connect_all()

# 获取日线数据（自动选择最优数据源）
data = ds_manager.get_data(
    symbol="000001.XSHE",
    start_date="2024-01-01",
    end_date="2024-12-31",
    data_type="daily"
)

print(f"获取到 {len(data)} 条数据")
print(data.head())
```

#### 指定数据源

```python
# 指定使用JQData
data = ds_manager.get_data(
    symbol="000001.XSHE",
    start_date="2024-01-01",
    end_date="2024-12-31",
    data_type="daily",
    source="jqdata"  # 指定数据源
)
```

#### 数据源健康检查

```python
# 检查所有数据源状态
status = ds_manager.check_all_sources()
# 返回: {'jqdata': {'status': 'ok', 'latency': 120}, ...}

# 检查单个数据源
health = ds_manager.sources['jqdata'].health_check()
# 返回: {'status': 'ok', 'latency': 120, 'error': None}
```

详细内容请参考 [2.1 数据源管理](2.1_Data_Source_Management_CN.md) 小节。

<h2 id="section-2-2">✅ 2.2 数据质量</h2>

数据质量检查是数据源模块的重要功能，负责检查数据的完整性、准确性和一致性，确保后续步骤使用的数据质量。

### 质量检查维度

数据质量检查包括以下三个维度：

1. **完整性检查**：检查缺失值、时间序列连续性、字段完整性
2. **准确性验证**：验证数据范围、业务逻辑、数据一致性
3. **异常检测**：使用统计方法、机器学习方法检测异常值和异常模式

### 完整性检查

完整性检查确保数据没有缺失，时间序列连续，所有必需字段都存在：

```python
from core.data_quality import DataQualityChecker

quality_checker = DataQualityChecker()

# 检查数据完整性
completeness_result = quality_checker.check_completeness(
    data=data,
    required_fields=["open", "high", "low", "close", "volume"]
)

# 检查结果
if completeness_result["missing_values"] > 0:
    print(f"发现 {completeness_result['missing_values']} 个缺失值")
if not completeness_result["time_series_continuous"]:
    print("时间序列不连续")
```

### 准确性验证

准确性验证确保数据在合理范围内，符合业务逻辑：

```python
# 验证数据准确性
accuracy_result = quality_checker.validate_accuracy(
    data=data,
    rules={
        "high >= low": "最高价应大于等于最低价",
        "close >= low and close <= high": "收盘价应在最低价和最高价之间",
        "volume >= 0": "成交量应大于等于0"
    }
)

# 检查结果
if accuracy_result["violations"]:
    print(f"发现 {len(accuracy_result['violations'])} 个规则违反")
```

### 异常检测

异常检测使用统计方法和机器学习方法检测异常值：

```python
# 检测异常
anomaly_result = quality_checker.detect_anomalies(
    data=data,
    methods=["statistical", "isolation_forest", "dbscan"]
)

# 检查结果
if anomaly_result["anomalies"]:
    print(f"发现 {len(anomaly_result['anomalies'])} 个异常值")
    print(anomaly_result["anomalies"])
```

### 自动数据清洗

系统支持自动数据清洗，AI辅助识别和处理异常数据：

```python
# 自动清洗数据
cleaned_data = quality_checker.auto_clean(
    data=data,
    methods=["fill_missing", "remove_anomalies", "smooth"]
)

# 生成清洗报告
cleaning_report = quality_checker.generate_cleaning_report(
    original=data,
    cleaned=cleaned_data
)
```

详细内容请参考 [2.2 数据质量](2.2_Data_Quality_CN.md) 小节。

详细内容请参考 [2.3 数据存储架构](2.3_Data_Storage_Architecture_CN.md) 和 [2.4 MCP工具集成](2.4_MCP_Tool_Integration_CN.md) 小节。

## 🔗 相关章节

- **1.2 系统架构总览**：了解数据源模块在系统架构中的位置
- **1.9 数据库架构设计**：深入了解数据存储架构设计
- **2.1 数据源管理**：详细了解数据源管理实现
- **2.2 数据质量**：详细了解数据质量检查机制
- **第三章 市场分析**：了解如何使用数据源模块提供的数据
- **10.7 MCP Server开发指南**：掌握MCP工具开发方法
- **10.11 开发流程方法论**：掌握使用MCP工具进行研究的方法

## 💡 关键要点

1. **统一接口抽象**：通过`BaseDataSource`基类定义统一的数据源接口
2. **多数据源支持**：支持JQData、AKShare、TuShare、Wind等多个数据源
3. **智能选择机制**：根据数据质量、完整性、速度等指标自动选择最优数据源
4. **故障自动切换**：当主数据源不可用时，自动切换到备用数据源
5. **数据质量保证**：完整性检查、准确性验证、异常检测、自动清洗
6. **分层/多存储架构**：根据数据类型选择最适合的存储方案
7. **MCP工具集成**：支持通过MCP工具进行数据查询、数据收集和知识检索

---

<div class="chapter-navigation">
  <div class="nav-item prev">
    <span class="nav-label">上一章</span>
    <a href="../001_Chapter1_System_Overview/001_Chapter1_System_Overview_CN.md">📋 第1章：系统概述</a>
  </div>
  <div class="nav-item next">
    <span class="nav-label">下一章</span>
    <a href="../003_Chapter3_Market_Analysis/003_Chapter3_Market_Analysis_CN.md">📈 第3章：市场分析</a>
  </div>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12*
