# TRQuant 平台模块可视化、数据库整合与工作流设计优化方案（修正版）

> **创建时间**: 2024-12-17  
> **版本**: v2.0（基于原PDF文档修正）  
> **状态**: 优化实施中

---

## 📋 文档说明

本文档基于《TRQuant 平台模块可视化、数据库整合与工作流设计优化方案》PDF原文，结合当前系统实际架构进行修正。**重点是优化现有架构，而非改变整体设计**。

---

## 一、TRQuant 9步投资工作流（当前标准定义）

### 1.1 工作流步骤定义（不可更改）

| 步骤 | ID | 名称 | 图标 | MCP工具 | 描述 |
|-----|-----|------|-----|---------|------|
| 1 | `data_source` | 信息获取 | 📡 | `data_source.health_check` | 检查数据源连接状态 |
| 2 | `market_trend` | 市场趋势 | 📈 | `market.status` | 分析当前市场状态 |
| 3 | `mainline` | 投资主线 | 🔥 | `market.mainlines` | 识别投资主线 |
| 4 | `candidate_pool` | 候选池构建 | 📦 | `data_source.candidate_pool` | 构建候选股票池 |
| 5 | `factor` | 因子构建 | 🧮 | `factor.recommend` | 推荐量化因子 |
| 6 | `strategy` | 策略生成 | 💻 | `template.generate` | 生成策略代码 |
| 7 | `backtest` | 回测验证 | 🔄 | `backtest.quick` | 执行回测验证 |
| 8 | `optimization` | 策略优化 | ⚙️ | `optimizer.grid_search` | 参数优化 |
| 9 | `report` | 报告生成 | 📄 | `report.generate` | 生成研究报告 |

### 1.2 工作流数据流图

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TRQuant 9步投资工作流                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
│  │ 1.信息  │───▶│ 2.市场  │───▶│ 3.投资  │───▶│ 4.候选  │          │
│  │   获取  │    │   趋势  │    │   主线  │    │   池    │          │
│  └─────────┘    └─────────┘    └─────────┘    └────┬────┘          │
│       │              │              │              │                 │
│       │              ▼              ▼              ▼                 │
│       │         ┌────────────────────────────────────┐              │
│       │         │         工作流上下文(Context)        │              │
│       │         │  • market_status  • mainlines      │              │
│       │         │  • candidate_pool • factors        │              │
│       │         └────────────────────────────────────┘              │
│       │              │              │              │                 │
│       ▼              ▼              ▼              ▼                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐          │
│  │ 5.因子  │───▶│ 6.策略  │───▶│ 7.回测  │───▶│ 8.优化  │          │
│  │   构建  │    │   生成  │    │   验证  │    │         │          │
│  └─────────┘    └─────────┘    └─────────┘    └────┬────┘          │
│                                                     │                │
│                                                     ▼                │
│                                              ┌─────────┐            │
│                                              │ 9.报告  │            │
│                                              │   生成  │            │
│                                              └─────────┘            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 二、MCP服务器架构（当前标准）

### 2.1 6层MCP服务器架构

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP服务器层次架构                          │
├─────────────────────────────────────────────────────────────┤
│  L0: 官方服务器                                              │
│      └── filesystem (~15 tools)                             │
├─────────────────────────────────────────────────────────────┤
│  L1: 核心量化服务器 (trquant-core)                          │
│      ├── data.*       数据源管理 (9 tools)                  │
│      ├── market.*     市场分析 (11 tools)                   │
│      ├── factor.*     因子库 (6 tools)                      │
│      ├── strategy.*   策略管理 (4 tools)                    │
│      ├── backtest.*   回测引擎 (5 tools)                    │
│      └── optimizer.*  参数优化 (4 tools)                    │
├─────────────────────────────────────────────────────────────┤
│  L2: 工作流服务器                                            │
│      ├── trquant-workflow (6 tools) - 9步工作流             │
│      └── trquant-project (17 tools) - 项目+任务管理         │
├─────────────────────────────────────────────────────────────┤
│  L3: 交易与开发服务器                                        │
│      ├── trquant-trading (5 tools) - 交易执行               │
│      └── trquant-dev (15 tools) - 代码+测试                 │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 服务器与9步工作流映射

| 工作流步骤 | 调用的MCP服务器 | 工具命名空间 |
|-----------|---------------|-------------|
| 1. 信息获取 | trquant-core | `data.health_check`, `data.get_price` |
| 2. 市场趋势 | trquant-core | `market.status`, `market.trend` |
| 3. 投资主线 | trquant-core | `market.mainlines`, `market.five_dimension_score` |
| 4. 候选池 | trquant-core | `data.candidate_pool`, `data.get_index_stocks` |
| 5. 因子构建 | trquant-core | `factor.recommend`, `factor.calculate` |
| 6. 策略生成 | trquant-core | `strategy.generate`, `strategy.list_templates` |
| 7. 回测验证 | trquant-core | `backtest.quick`, `backtest.jqdata` |
| 8. 策略优化 | trquant-core | `optimizer.grid_search`, `optimizer.optuna` |
| 9. 报告生成 | trquant-core | `report.generate`, `report.export` |

---

## 三、模块功能边界与接口规范

### 3.1 数据模块 (Data)

**职责**: 市场原始数据的采集、清洗与标准化存储

**接口定义**:
```python
# 输入
{
    "symbols": ["000001.XSHE", "600000.XSHG"],
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "fields": ["open", "high", "low", "close", "volume"]
}

# 输出
{
    "success": True,
    "data": pd.DataFrame,  # 时间序列数据
    "timestamp": "2024-12-17T10:00:00"
}
```

**9步工作流中的作用**:
- 步骤1（信息获取）: 检查数据源连接状态
- 步骤4（候选池）: 获取指数成分股、构建候选池

### 3.2 市场模块 (Market)

**职责**: 市场状态分析、趋势判断、投资主线识别

**接口定义**:
```python
# market.status 输入
{"universe": "CN_EQ"}

# market.status 输出
{
    "success": True,
    "data": {
        "regime": "risk_on",  # risk_on/risk_off/neutral
        "index_trend": {"上证指数": "上涨", "创业板": "震荡"},
        "style_rotation": "小盘成长"
    }
}

# market.mainlines 输出
{
    "success": True,
    "data": {
        "mainlines": [
            {"name": "AI算力", "score": 85, "sectors": ["半导体", "通信设备"]},
            {"name": "新能源", "score": 72, "sectors": ["光伏", "储能"]}
        ]
    }
}
```

**9步工作流中的作用**:
- 步骤2（市场趋势）: 判断市场整体状态
- 步骤3（投资主线）: 识别当前投资主线

### 3.3 因子模块 (Factor)

**职责**: 基于市场状态推荐和计算alpha因子

**接口定义**:
```python
# factor.recommend 输入
{"market_regime": "risk_on", "top_n": 10}

# factor.recommend 输出
{
    "success": True,
    "data": {
        "factors": [
            {"name": "momentum_20d", "category": "动量", "weight": 0.25},
            {"name": "roe", "category": "质量", "weight": 0.20}
        ]
    }
}
```

**9步工作流中的作用**:
- 步骤5（因子构建）: 根据市场状态推荐因子

### 3.4 策略模块 (Strategy)

**职责**: 根据因子和市场信息生成策略代码

**接口定义**:
```python
# strategy.generate 输入
{
    "factors": ["momentum_20d", "roe"],
    "style": "multi_factor",
    "platform": "ptrade"
}

# strategy.generate 输出
{
    "success": True,
    "data": {
        "code": "# PTrade策略代码...",
        "template_name": "multi_factor_ptrade"
    }
}
```

**9步工作流中的作用**:
- 步骤6（策略生成）: 生成可执行的策略代码

### 3.5 回测模块 (Backtest)

**职责**: 在历史数据上模拟策略执行，评估业绩指标

**接口定义**:
```python
# backtest.quick 输入
{
    "strategy_code": "...",
    "start_date": "2023-01-01",
    "end_date": "2024-01-01",
    "initial_capital": 1000000
}

# backtest.quick 输出
{
    "success": True,
    "data": {
        "total_return": 0.25,
        "annual_return": 0.25,
        "sharpe_ratio": 1.5,
        "max_drawdown": 0.15,
        "equity_curve": [...],
        "trades": [...]
    }
}
```

**9步工作流中的作用**:
- 步骤7（回测验证）: 验证策略历史表现

### 3.6 优化模块 (Optimizer)

**职责**: 策略参数优化和组合优化

**接口定义**:
```python
# optimizer.grid_search 输入
{
    "strategy_code": "...",
    "param_grid": {
        "lookback": [10, 20, 30],
        "hold_days": [5, 10, 20]
    }
}

# optimizer.grid_search 输出
{
    "success": True,
    "data": {
        "best_params": {"lookback": 20, "hold_days": 10},
        "best_sharpe": 1.8,
        "all_results": [...]
    }
}
```

**9步工作流中的作用**:
- 步骤8（策略优化）: 寻找最优参数组合

### 3.7 报告模块 (Report)

**职责**: 生成完整的研究报告

**9步工作流中的作用**:
- 步骤9（报告生成）: 输出HTML/PDF研究报告

---

## 四、数据库架构（Polyglot Persistence）

### 4.1 数据库选型

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRQuant 数据存储架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │   PostgreSQL     │  │ ClickHouse/TSDB  │  │     Redis      │ │
│  │   (关系型主库)    │  │  (时序分析库)     │  │   (缓存/队列)  │ │
│  ├──────────────────┤  ├──────────────────┤  ├────────────────┤ │
│  │ • 用户账户       │  │ • 历史行情数据   │  │ • 实时行情快照 │ │
│  │ • 策略配置       │  │ • 因子值矩阵     │  │ • 会话状态     │ │
│  │ • 交易记录       │  │ • 回测净值曲线   │  │ • 任务队列     │ │
│  │ • 工作流状态     │  │ • 性能指标统计   │  │ • MCP调用缓存  │ │
│  └──────────────────┘  └──────────────────┘  └────────────────┘ │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │   MinIO/S3       │  │     Chroma       │  │    MongoDB     │ │
│  │  (对象存储)       │  │   (向量数据库)    │  │  (文档存储)    │ │
│  ├──────────────────┤  ├──────────────────┤  ├────────────────┤ │
│  │ • 策略代码文件   │  │ • 代码嵌入向量   │  │ • 研报文档     │ │
│  │ • 回测报告PDF    │  │ • 文档嵌入向量   │  │ • 开发日志     │ │
│  │ • 研究文档       │  │ • RAG知识库      │  │ • 系统配置     │ │
│  └──────────────────┘  └──────────────────┘  └────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 缓存策略（优化重点）

#### 4.2.1 Redis缓存层

```python
# 缓存配置
CACHE_CONFIG = {
    # 市场状态缓存 - 5分钟有效
    "market.status": {"ttl": 300, "key_pattern": "market:status:{universe}"},
    
    # 投资主线缓存 - 30分钟有效
    "market.mainlines": {"ttl": 1800, "key_pattern": "market:mainlines:{time_horizon}"},
    
    # 因子推荐缓存 - 1小时有效
    "factor.recommend": {"ttl": 3600, "key_pattern": "factor:recommend:{regime}"},
    
    # 候选池缓存 - 1天有效
    "data.candidate_pool": {"ttl": 86400, "key_pattern": "data:pool:{index}:{date}"},
    
    # 回测结果缓存 - 永久（按策略hash）
    "backtest.quick": {"ttl": -1, "key_pattern": "backtest:{strategy_hash}:{params_hash}"}
}
```

#### 4.2.2 工作流上下文缓存

```python
class WorkflowContextCache:
    """工作流上下文缓存管理器"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 3600  # 1小时
    
    async def save_step_result(self, workflow_id: str, step_id: str, result: dict):
        """保存步骤结果到缓存"""
        key = f"workflow:{workflow_id}:step:{step_id}"
        await self.redis.setex(key, self.ttl, json.dumps(result))
    
    async def get_step_result(self, workflow_id: str, step_id: str) -> Optional[dict]:
        """从缓存获取步骤结果"""
        key = f"workflow:{workflow_id}:step:{step_id}"
        data = await self.redis.get(key)
        return json.loads(data) if data else None
    
    async def get_context(self, workflow_id: str) -> dict:
        """获取完整工作流上下文"""
        context = {}
        for step in WORKFLOW_9STEPS:
            result = await self.get_step_result(workflow_id, step["id"])
            if result:
                context[step["id"]] = result
        return context
```

---

## 五、工作流引擎优化

### 5.1 DAG依赖管理

```python
# 9步工作流依赖关系定义
WORKFLOW_DEPENDENCIES = {
    "data_source": [],                          # 步骤1无依赖
    "market_trend": ["data_source"],            # 步骤2依赖步骤1
    "mainline": ["market_trend"],               # 步骤3依赖步骤2
    "candidate_pool": ["mainline"],             # 步骤4依赖步骤3
    "factor": ["market_trend", "candidate_pool"],  # 步骤5依赖步骤2、4
    "strategy": ["factor", "candidate_pool"],   # 步骤6依赖步骤5、4
    "backtest": ["strategy"],                   # 步骤7依赖步骤6
    "optimization": ["backtest"],               # 步骤8依赖步骤7
    "report": ["optimization", "backtest"]      # 步骤9依赖步骤7、8
}
```

### 5.2 异步执行与状态管理

```python
class WorkflowEngine:
    """工作流引擎（优化版）"""
    
    def __init__(self):
        self.cache = WorkflowContextCache(redis_client)
        self.task_queue = asyncio.Queue()
    
    async def execute_step(self, workflow_id: str, step_id: str) -> dict:
        """执行单个步骤（带缓存）"""
        
        # 1. 检查缓存
        cached_result = await self.cache.get_step_result(workflow_id, step_id)
        if cached_result:
            logger.info(f"✅ 步骤 {step_id} 使用缓存结果")
            return cached_result
        
        # 2. 检查依赖
        dependencies = WORKFLOW_DEPENDENCIES.get(step_id, [])
        context = {}
        for dep in dependencies:
            dep_result = await self.cache.get_step_result(workflow_id, dep)
            if not dep_result:
                raise ValueError(f"依赖步骤 {dep} 未完成")
            context[dep] = dep_result
        
        # 3. 执行步骤
        result = await self._call_mcp_tool(step_id, context)
        
        # 4. 保存到缓存
        await self.cache.save_step_result(workflow_id, step_id, result)
        
        return result
    
    async def _call_mcp_tool(self, step_id: str, context: dict) -> dict:
        """调用对应的MCP工具"""
        step_info = next((s for s in WORKFLOW_9STEPS if s["id"] == step_id), None)
        if not step_info:
            raise ValueError(f"未知步骤: {step_id}")
        
        mcp_tool = step_info["mcp_tool"]
        # 根据step_id调用对应的处理函数...
        return await self._execute_mcp_call(mcp_tool, context)
```

### 5.3 错误处理与恢复机制

```python
class WorkflowErrorHandler:
    """工作流错误处理器"""
    
    async def handle_step_error(self, workflow_id: str, step_id: str, error: Exception):
        """处理步骤执行错误"""
        
        error_info = {
            "step_id": step_id,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.now().isoformat(),
            "recoverable": self._is_recoverable(error)
        }
        
        # 记录错误
        await self._log_error(workflow_id, error_info)
        
        # 判断是否可恢复
        if error_info["recoverable"]:
            return await self._attempt_recovery(workflow_id, step_id, error)
        else:
            raise error
    
    def _is_recoverable(self, error: Exception) -> bool:
        """判断错误是否可恢复"""
        recoverable_errors = (
            ConnectionError,
            TimeoutError,
            # JSON解析错误等
        )
        return isinstance(error, recoverable_errors)
```

---

## 六、前端可视化优化

### 6.1 双前端架构（保持不变）

| 前端 | 技术栈 | 主要功能 |
|-----|-------|---------|
| **Cursor扩展** | TypeScript + React + ECharts | 9步工作流可视化、市场分析、策略生成 |
| **PyQt6桌面** | Python + PyQt6 + PyQtGraph | 策略管理、回测执行、实时监控 |

### 6.2 9步工作流可视化组件

```typescript
// 工作流面板配置
const WORKFLOW_CONFIG = {
  steps: [
    { id: "data_source", name: "信息获取", icon: "📡", color: "#58a6ff" },
    { id: "market_trend", name: "市场趋势", icon: "📈", color: "#667eea" },
    { id: "mainline", name: "投资主线", icon: "🔥", color: "#F59E0B" },
    { id: "candidate_pool", name: "候选池构建", icon: "📦", color: "#a371f7" },
    { id: "factor", name: "因子构建", icon: "🧮", color: "#3fb950" },
    { id: "strategy", name: "策略生成", icon: "💻", color: "#d29922" },
    { id: "backtest", name: "回测验证", icon: "🔄", color: "#1E3A5F" },
    { id: "optimization", name: "策略优化", icon: "⚙️", color: "#7C3AED" },
    { id: "report", name: "报告生成", icon: "📄", color: "#EC4899" }
  ],
  
  // 图表配置
  charts: {
    market_trend: "line",      // 市场趋势折线图
    mainline: "radar",         // 投资主线雷达图
    factor: "heatmap",         // 因子暴露热力图
    backtest: "area",          // 收益曲线面积图
    optimization: "scatter"    // 参数优化散点图
  }
};
```

### 6.3 数据可视化增强

```typescript
// ECharts图表配置示例
const getBacktestChart = (data: BacktestResult) => ({
  title: { text: "回测收益曲线" },
  xAxis: { type: "time", data: data.dates },
  yAxis: { type: "value", name: "累计收益率" },
  series: [
    { name: "策略收益", type: "line", data: data.equity_curve, areaStyle: {} },
    { name: "基准收益", type: "line", data: data.benchmark_curve }
  ],
  tooltip: { trigger: "axis" }
});
```

---

## 七、优化实施计划

### Phase 1: 缓存层实施（1周）

| 任务 | 优先级 | 状态 |
|-----|-------|------|
| Redis缓存配置 | 高 | 📅 计划中 |
| 工作流上下文缓存 | 高 | 📅 计划中 |
| MCP调用结果缓存 | 中 | 📅 计划中 |

### Phase 2: 工作流引擎优化（1周）

| 任务 | 优先级 | 状态 |
|-----|-------|------|
| DAG依赖管理实现 | 高 | 📅 计划中 |
| 异步执行优化 | 高 | 📅 计划中 |
| 错误处理与恢复 | 中 | 📅 计划中 |

### Phase 3: 前端可视化增强（1周）

| 任务 | 优先级 | 状态 |
|-----|-------|------|
| 工作流状态可视化 | 高 | 📅 计划中 |
| 图表组件增强 | 中 | 📅 计划中 |
| 实时进度显示 | 中 | 📅 计划中 |

### Phase 4: 数据库整合（2周）

| 任务 | 优先级 | 状态 |
|-----|-------|------|
| PostgreSQL部署 | 高 | 📅 计划中 |
| ClickHouse时序库 | 中 | 📅 计划中 |
| Chroma向量库 | 中 | 📅 计划中 |

---

## 八、验收标准

### 8.1 性能指标

| 指标 | 目标值 | 当前值 |
|-----|-------|-------|
| 工作流完整执行时间 | < 60秒 | 待测 |
| 单步缓存命中率 | > 80% | 待测 |
| MCP调用响应时间 | < 2秒 | 待测 |
| GUI渲染帧率 | > 30fps | 待测 |

### 8.2 功能验收

- [ ] 9步工作流完整执行无错误
- [ ] 缓存正确命中，避免重复计算
- [ ] 工作流状态可持久化和恢复
- [ ] 前端图表正确渲染数据
- [ ] 错误处理正确，可恢复执行

---

## 九、参考文档

1. `/home/taotao/dev/QuantTest/TRQuant/mcp_servers/workflow_9steps_server.py` - 9步工作流定义
2. `/home/taotao/dev/QuantTest/TRQuant/docs/MCP_SERVER_CONSOLIDATION.md` - MCP服务器整合方案
3. `/home/taotao/dev/QuantTest/TRQuant/docs/FRONTEND_ARCHITECTURE_AND_PLAN.md` - 前端架构文档
4. `/home/taotao/dev/QuantTest/TRQuant/docs/DATABASE_ARCHITECTURE_AND_KB_BACKGROUND.md` - 数据库架构

---

**文档维护**: TRQuant Dev Team  
**最后更新**: 2024-12-17  
**版本**: v2.0 (修正版)

