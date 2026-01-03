# TRQuant 数据库架构与知识库构建背景信息报告

> **创建时间**: 2024-12-17  
> **文档版本**: v1.0  
> **状态**: 架构设计完成，部分实施中

---

## 📊 一、数据库架构总览

### 1.1 设计理念：分层/多存储（Polyglot Persistence）

TRQuant采用**分层/多存储（Polyglot Persistence）**架构，根据数据类型选择最适合的存储方案。

**设计原则**:
- **按数据类型选择存储**: 强事务用PostgreSQL，时序数据用时序库，文档用对象存储
- **性能优先**: 每种数据类型使用最优化的存储引擎
- **成本优化**: 避免过度设计，小规模数据可用文件缓存
- **可扩展性**: 支持从文件缓存平滑迁移到专业数据库

---

## 🗄️ 二、数据库种类与架构

### 2.1 PostgreSQL（主数据库）

**定位**: 强事务/强审计类数据（OLTP）

#### 存储内容

| 数据类型 | 表/功能 | 说明 |
|---------|--------|------|
| **策略仓库** | `strategy`, `strategy_param` | 策略元数据、版本、参数集 |
| **审批流** | `approval_workflow` | 策略评审、风控审批 |
| **实盘账务** | `account`, `order`, `execution` | 账户、订单、成交、持仓 |
| **审计日志** | `audit_log` (按日分区) | 操作记录（不可篡改） |
| **数据源配置** | `data_source_configs` | 数据源元数据 |

#### 技术特点

- ✅ ACID事务保证
- ✅ 强约束（外键、唯一键）
- ✅ JSONB支持半结构化数据
- ✅ GIN索引支持文档内检索
- ✅ 审计表按日分区

---

### 2.2 ClickHouse/TimescaleDB（时序分析库）

**定位**: 时间序列/分析类数据（OLAP/TSDB）

#### 存储内容

| 数据类型 | 表/功能 | 说明 |
|---------|--------|------|
| **行情数据** | `market_data` | OHLCV（日/分钟/Tick） |
| **因子数据** | `factor_data` | 每日/每分钟因子矩阵 |
| **回测输出** | `equity_curve`, `trade_log` | 净值曲线、交易明细 |
| **实盘监控** | `pnl_curve`, `drawdown` | PnL曲线、回撤 |

#### 技术选型

- **ClickHouse**: 适合高频聚合分析、大规模数据、极致性能
- **TimescaleDB**: 适合一体化方案、中等规模、SQL生态

---

### 2.3 MinIO/S3（对象存储）

**定位**: 文档/半结构化文件存储

#### 存储内容

- **回测报告**: HTML/PDF格式
- **图表产物**: 策略图表、分析图表
- **研究文档**: 研究笔记、策略说明

#### 技术特点

- 数据库只存元数据（hash、路径、生成时间）
- 支持版本管理
- 支持访问控制

---

### 2.4 Redis（缓存/队列）

**定位**: 缓存和任务队列

#### 存储内容

| 数据类型 | Key模式 | TTL |
|---------|---------|-----|
| **行情快照缓存** | `market:snapshot:{symbol}` | 60秒 |
| **任务队列** | `queue:backtest` | - |
| **风控状态机** | `risk:state:{account_id}` | 1小时 |

---

### 2.5 Chroma（向量数据库）

**定位**: 知识库向量检索

#### 存储内容

| 知识库 | Chunks数量 | 说明 |
|--------|-----------|------|
| **Manual KB** | 35,527 chunks | 开发手册知识库 |
| **Engineering KB** | 14,945 symbols | 工程知识库 |

#### 技术特点

- ✅ 语义相似度检索
- ✅ 混合检索（向量 + BM25 + 重排序）
- ✅ 元数据过滤
- ✅ 持久化存储

---

## 📚 三、知识库构建背景

### 3.1 RAG技术原理

RAG (Retrieval-Augmented Generation) 通过检索相关文档来增强LLM的生成能力。

```
传统生成式AI:
用户问题 → LLM → 回答（基于训练数据）

RAG增强:
用户问题 → 检索相关文档 → LLM（基于检索内容） → 回答（基于最新知识）
```

### 3.2 知识库分类

#### Manual KB（开发手册知识库）

**数据源**:
- `extension/AShare-manual/src/pages/dev-book/**.md`
- `docs/**.md`

**切分策略**:
- 按标题层级切（H1/H2/H3），每chunk 300–800 tokens
- 代码块单独成chunk
- metadata: `doc_id, path, chapter, section, version`

**当前状态**: ✅ 35,527 chunks已构建

#### Engineering KB（工程知识库）

**数据源**:
- 代码文件（`core/`, `extension/`, `mcp_servers/`）
- 配置文件、API schema

**切分策略**:
- 符号级切分：class/function为一个chunk
- metadata: `file_path, symbol, start_line, end_line, commit`

**当前状态**: ✅ 14,945 symbols已构建

### 3.3 混合检索策略

1. **关键词召回（BM25）**: 专有名词、函数名
2. **向量召回（Embedding）**: 语义相似
3. **Reranker**: 重排候选，输出Top-K

---

## 🔧 四、实施状态

| 数据库 | 状态 | 说明 |
|--------|------|------|
| **PostgreSQL** | 📅 设计完成，待实施 | 预计2025-01-31 |
| **ClickHouse/TimescaleDB** | 📅 设计完成，待选型 | 预计2025-02-28 |
| **MinIO/S3** | 📅 设计完成，待部署 | 预计2025-03-15 |
| **Redis** | 📅 设计完成，待部署 | 预计2025-02-15 |
| **Chroma** | ✅ 已部署 | Manual KB + Engineering KB已构建 |

---

**文档维护**: TRQuant Team  
**最后更新**: 2024-12-17
