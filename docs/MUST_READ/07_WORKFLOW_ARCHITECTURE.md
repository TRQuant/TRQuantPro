# TRQuant 9步工作流完整架构与实现方法

> **版本**: v1.0  
> **创建时间**: 2025-12-19  
> **目的**: 确保后续开发不重复已有模块，不缺失已有功能

---

## 📋 核心架构

### 1. 工作流编排器 (`WorkflowOrchestrator`)
**位置**: `core/workflow_orchestrator.py`

**职责**:
- 统一编排整个量化工作流程
- 直接调用现有模块，不重复实现逻辑
- 管理MongoDB数据存储

**关键方法**:
- `check_data_sources()` - 检测JQData/AKShare/MongoDB连接
- `analyze_market_trend()` - 调用TrendAnalyzer，保存到`market_trend`集合
- `identify_mainlines()` - 调用`_simple_mainline_analysis()`，直接使用AKShare API
- `build_candidate_pool()` - 调用CandidatePoolBuilder

**数据存储**:
- MongoDB数据库: `trquant`
- 集合:
  - `market_trend` - 市场趋势分析结果
  - `mainline_scores` - 投资主线评分
  - `candidate_pool` - 候选池结果
  - `factor_recommendations` - 因子推荐

### 2. 数据存储管理

#### 2.1 缓存管理器 (`CacheManager`)
**位置**: `core/cache_manager.py`

**功能**:
- 统一管理计算结果缓存
- 避免重复计算
- 支持缓存有效期检查

**缓存类型**:
- `mainline` → `mainline_mapped` (24小时有效)
- `candidate_pool` → `candidate_pool_cache` (12小时有效)
- `factor_filter` → `factor_filter_cache` (6小时有效)

#### 2.2 工作流状态管理器 (`WorkflowStateManager`)
**位置**: `core/workflow/state_manager.py`

**功能**:
- 工作流状态持久化
- 支持断点续传
- 文件系统 + MongoDB双重存储

**存储位置**:
- 文件: `data/workflow_states/{workflow_id}.json`
- MongoDB: `trquant.workflow_states`

#### 2.3 工作流存储 (`WorkflowStorage`)
**位置**: `mcp_servers/utils/workflow_storage.py`

**功能**:
- MCP服务器层的工作流状态存储
- JSON文件存储
- 支持查询和恢复

**存储位置**: `data/workflows/{workflow_id}.json`

### 3. 数据源调用

#### 3.1 投资主线识别
**实现**: `WorkflowOrchestrator._simple_mainline_analysis()`

**数据源优先级**:
1. `ak.stock_fund_flow_concept()` - 概念资金流（首选）
2. `ak.stock_board_concept_name_em()` - 概念板块
3. `ak.stock_board_industry_name_em()` - 行业板块
4. 默认配置（如果API都失败）

**数据存储**:
- MongoDB: `mainline_scores` 集合
- 字段: `name`, `rank`, `composite_score`, `change_pct`, `fund_flow`, `timestamp`, `data_source`

#### 3.2 候选池构建
**实现**: `CandidatePoolBuilder.build_from_mainline()`

**数据源**: JQData
- 获取板块成分股
- 技术突破筛选
- 财务因子筛选

**数据存储**:
- MongoDB: `candidate_pool` 集合
- 缓存: `candidate_pool_cache`

## 🔧 开发方法总结

### 1. 避免重复开发
- ✅ 使用 `WorkflowOrchestrator` 而不是重新实现
- ✅ 使用 `CandidatePoolBuilder` 而不是mock数据
- ✅ 使用 `CacheManager` 管理缓存

### 2. 数据源调用规范
- **投资主线**: 直接调用AKShare API (`ak.stock_fund_flow_concept()`)
- **候选池**: 使用JQData (`CandidatePoolBuilder`)
- **市场趋势**: 使用JQData (`TrendAnalyzer`)

### 3. 模块导入规范
- `from core.workflow_orchestrator import WorkflowOrchestrator`
- `from core.candidate_pool_builder import CandidatePoolBuilder`
- `from jqdata.client import JQDataClient` (不是`core.data.jqdata_provider`)
- `from core.mainline_scanner import MainlineBasedScanner` (不是`MainlineScanner`)

## ⚠️ 常见错误

1. **字段名错误**: `top_mainlines` vs `mainlines`
2. **导入路径错误**: `core.data.jqdata_provider.JQDataClient` (不存在)
3. **使用模拟数据**: 应该调用真实API
4. **MongoDB布尔值**: `if self.db:` → `if self.db is not None:`

## 📚 相关文档

- `docs/MUST_READ/06_MODULE_INDEX.md` - 模块索引
- `core/module_registry.py` - 模块注册表
- `docs/02_development_guides/WORKFLOW_STATE_PERSISTENCE.md` - 状态持久化设计
