---
title: "2.3 数据存储架构"
description: "详细介绍数据源模块的分层/多存储（Polyglot Persistence）架构设计，包括PostgreSQL、ClickHouse/TimescaleDB、Redis等技术选型"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 🗄️ 2.3 数据存储架构

> **核心摘要：**
> 
> 本节详细介绍数据源模块的数据存储架构，采用**分层/多存储（Polyglot Persistence）**架构，根据数据类型选择最适合的存储方案。通过理解PostgreSQL主库、ClickHouse/TimescaleDB时序库、Redis缓存等技术的选型理由和数据分布策略，帮助开发者掌握数据存储的核心设计。

数据源模块的数据存储遵循系统的**分层/多存储（Polyglot Persistence）**架构，根据数据类型选择最适合的存储方案。

## 数据存储策略

<div class="key-points">
  <div class="key-point">
    <h4>📊 PostgreSQL（主库）</h4>
    <p>存储数据源配置、元数据、审计日志等强事务数据</p>
  </div>
  <div class="key-point">
    <h4>⏱️ ClickHouse/TimescaleDB（时序库）</h4>
    <p>存储行情数据（OHLCV日/分钟/Tick）、因子数据、回测输出等时序数据</p>
  </div>
  <div class="key-point">
    <h4>⚡ Redis（缓存）</h4>
    <p>缓存行情快照、数据更新任务队列、风控状态等临时数据</p>
  </div>
  <div class="key-point">
    <h4>📦 Parquet/HDF5（文件缓存）</h4>
    <p>文件缓存，适合早期阶段或小规模数据</p>
  </div>
</div>

## PostgreSQL存储（元数据）

数据源配置和元数据存储在PostgreSQL：

```sql
-- 数据源配置表
CREATE TABLE data_source_configs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    source_type VARCHAR(50) NOT NULL, -- jqdata, akshare, tushare
    config JSONB NOT NULL, -- 连接配置
    priority INTEGER DEFAULT 0, -- 优先级
    status VARCHAR(50) DEFAULT 'active', -- active, inactive, maintenance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## ClickHouse/TimescaleDB存储（行情数据）

行情数据存储在时序数据库：

```python
# 数据存储到ClickHouse
def store_market_data(symbol: str, data: pd.DataFrame):
    """存储行情数据到ClickHouse"""
    clickhouse_client.insert(
        'market_data_daily',
        data.to_dict('records')
    )
```

## Redis缓存（行情快照）

实时行情快照缓存到Redis：

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def cache_market_snapshot(symbol: str, data: dict):
    """缓存行情快照（TTL: 60秒）"""
    key = f"market:snapshot:{symbol}"
    r.setex(key, 60, json.dumps(data))
```

详细设计请参考 **1.9 数据库架构设计** 章节。

## 🔗 相关章节

- **1.2 系统架构总览**：了解数据源模块在系统架构中的位置
- **1.9 数据库架构设计**：深入了解数据存储架构设计
- **2.1 数据源管理**：详细了解数据源管理实现
- **2.2 数据质量**：详细了解数据质量检查机制
- **2.4 MCP工具集成**：了解MCP工具在数据源模块中的应用

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了数据源模块的数据存储架构，采用分层/多存储（Polyglot Persistence）架构，根据数据类型选择最适合的存储方案。通过理解PostgreSQL主库、ClickHouse/TimescaleDB时序库、Redis缓存等技术的选型理由和数据分布策略，帮助开发者掌握数据存储的核心设计。</p>
  
  <h3>下节预告</h3>
  <p>掌握了数据存储架构后，下一节将介绍MCP工具集成，包括知识库查询、数据收集工具等。通过理解MCP工具在数据源模块中的应用，帮助开发者掌握如何使用MCP工具提升开发效率。</p>
  
  <div style="display: flex; gap: 1rem; margin-top: 1rem;">
    <a href="/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN" class="next-section" style="flex: 1;">
      ← 2.2 数据质量
    </a>
    <a href="/ashare-book6/002_Chapter2_Data_Source/002_Chapter2_Data_Source_CN" class="next-section" style="flex: 1; text-align: center;">
      ← 返回第2章
    </a>
    <a href="/ashare-book6/002_Chapter2_Data_Source/2.4_MCP_Tool_Integration_CN" class="next-section" style="flex: 1; text-align: right;">
      继续学习：2.4 MCP工具集成 →
    </a>
  </div>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
