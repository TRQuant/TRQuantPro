# 十倍股早期识别系统 - MCP工作流程

> **版本**: v1.0  
> **创建时间**: 2025-12-19  
> **与9步工作流区分**: 本流程专注于十倍股识别，非9步投资工作流

---

## 📋 流程概述

十倍股识别系统是**独立于9步投资工作流**的专有系统，有自己的MCP工具和数据流程。

### 核心区别

| 对比项 | 9步工作流 | 十倍股识别系统 |
|--------|-----------|----------------|
| **目标** | 完整投资决策流程 | 识别高成长潜力股 |
| **MCP服务器** | `workflow_9steps_server` | `trquant_core_server` |
| **核心工具前缀** | `workflow9.*` | `tenbagger.*`, `datasource.*` |
| **输出** | 策略+回测报告 | 十倍股推荐列表 |

---

## 🔄 标准工作流程

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      十倍股早期识别系统工作流程                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                │
│  │ 步骤1       │     │ 步骤2       │     │ 步骤3       │                │
│  │ 候选池获取   │ --> │ 数据获取    │ --> │ 阶段判断    │                │
│  │             │     │             │     │ (S0-S5)     │                │
│  └─────────────┘     └─────────────┘     └─────────────┘                │
│        │                   │                   │                         │
│        v                   v                   v                         │
│  candidate_pool.*    datasource.fetch_all  stage_machine              │
│                                                                          │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                │
│  │ 步骤4       │     │ 步骤5       │     │ 步骤6       │                │
│  │ 评分卡计算   │ --> │ 综合评估    │ --> │ 排名筛选    │                │
│  │ (7维)       │     │             │     │             │                │
│  └─────────────┘     └─────────────┘     └─────────────┘                │
│        │                   │                   │                         │
│        v                   v                   v                         │
│  scorecard            tenbagger.batch     tenbagger.filter             │
│                                                                          │
│  ┌─────────────┐                                                        │
│  │ 步骤7       │                                                        │
│  │ 生成报告    │                                                        │
│  │             │                                                        │
│  └─────────────┘                                                        │
│        │                                                                 │
│        v                                                                 │
│  推荐列表.md                                                            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ MCP工具详解

### 1. 数据源工具 (`datasource.*`)

| 工具名 | 功能 | 参数 |
|--------|------|------|
| `datasource.stats` | 获取数据源统计 | 无 |
| `datasource.fetch_financial` | 获取财务数据 | symbols, source |
| `datasource.fetch_price` | 获取行情数据 | symbols |
| `datasource.fetch_events` | 获取事件数据 | symbols |
| `datasource.fetch_altdata` | 获取另类数据 | symbols |
| `datasource.fetch_all` | 获取全部数据 | symbols |

### 2. 十倍股工具 (`tenbagger.*`)

| 工具名 | 功能 | 参数 |
|--------|------|------|
| `tenbagger.evaluate` | 评估单只股票 | symbol, name, stage, scorecard, financials, ... |
| `tenbagger.batch` | 批量评估 | stocks[] |
| `tenbagger.rank` | 获取排名 | top_n |
| `tenbagger.filter` | 按等级筛选 | min_level (S+/S/A/B/C/D) |
| `tenbagger.report` | 获取评估报告 | symbol |
| `tenbagger.history` | 获取评估历史 | symbol |
| `tenbagger.stats` | 获取统计信息 | 无 |

### 3. 辅助模块 (Python直接调用)

| 模块 | 功能 | 位置 |
|------|------|------|
| `StageMachine` | 阶段状态机 | `mcp_servers/utils/stage_machine.py` |
| `ScoreCard` | 7维评分卡 | `mcp_servers/utils/scorecard.py` |
| `DataSourceManager` | 数据源管理 | `mcp_servers/utils/datasource_manager.py` |
| `TenbaggerEvaluator` | 综合评估器 | `mcp_servers/utils/tenbagger_evaluator.py` |

---

## 📝 Python调用示例

### 方式1: 使用MCP工具 (推荐)

```python
from core.mcp.client import MCPClient

client = MCPClient()

# 1. 获取数据
data = client.call("datasource.fetch_all", {"symbols": ["000001.XSHE", "000002.XSHE"]})

# 2. 批量评估
result = client.call("tenbagger.batch", {"stocks": [
    {"symbol": "000001.XSHE", "name": "平安银行", "data": {...}},
    {"symbol": "000002.XSHE", "name": "万科A", "data": {...}}
]})

# 3. 获取排名
rankings = client.call("tenbagger.rank", {"top_n": 20})

# 4. 筛选A级以上
filtered = client.call("tenbagger.filter", {"min_level": "A"})
```

### 方式2: 使用Python命令接口 (便捷)

```python
from extension.python.tenbagger_commands import tenbagger_evaluate, tenbagger_ranking

# 评估单只股票
result = tenbagger_evaluate("000001.XSHE")

# 获取排名
rankings = tenbagger_ranking(limit=20)
```

### 方式3: 直接调用核心模块

```python
from mcp_servers.utils.datasource_manager import get_datasource_manager
from mcp_servers.utils.stage_machine import StageMachine
from mcp_servers.utils.scorecard import get_scorecard_engine
from mcp_servers.utils.tenbagger_evaluator import TenbaggerEvaluator

# 1. 获取数据
manager = get_datasource_manager()
data = manager.fetch_for_tenbagger(["000001.XSHE"])

# 2. 阶段判断
sm = StageMachine()
sm.get_or_create("000001.XSHE")
record = sm.get_stage("000001.XSHE")
stage = record.current_stage if record else "S0"

# 3. 评分卡
engine = get_scorecard_engine()
card = engine.compute(
    security_id="000001.XSHE",
    financial_data=data.get("financials", {}).get("000001.XSHE", {}),
    stage_record={"current_stage": stage}
)

# 4. 综合评估
evaluator = TenbaggerEvaluator()
report = evaluator.evaluate(
    "000001.XSHE", 
    "平安银行",
    {
        "stage": stage,
        "scorecard": {"total_score": card.total_score},
        "financials": data.get("financials", {}).get("000001.XSHE", {})
    }
)

print(f"评估结果: {report.eval_level.value}, 总分: {report.total_score}")
```

---

## 📊 评估等级说明

| 等级 | 分数范围 | 含义 | 建议操作 |
|------|----------|------|----------|
| S+ | ≥85 | 极高潜力 | 重点跟踪，考虑建仓 |
| S | ≥75 | 高潜力 | 纳入观察池 |
| A | ≥65 | 较高潜力 | 持续关注 |
| B | ≥50 | 中等潜力 | 备选 |
| C | ≥35 | 一般 | 暂不关注 |
| D | <35 | 较低 | 剔除 |

---

## 🔗 阶段定义 (S0-S5)

| 阶段 | 名称 | 说明 | 投资建议 |
|------|------|------|----------|
| S0 | 观察期 | 早期信号，待验证 | 不介入 |
| S1 | 验证期 | 初步验证，潜力待确认 | 少量试探 |
| S2 | 导入期 | **最佳介入点** | 积极布局 |
| S3 | 放量期 | 快速增长，关注估值 | 持有为主 |
| S4 | 加速期 | 接近成熟，注意风险 | 逐步减仓 |
| S5 | 成熟期 | 增长放缓，估值偏高 | 考虑退出 |

---

## ⚠️ 与9步工作流的整合点

虽然两个系统独立运作，但可以在以下点整合：

1. **候选池共享**: 9步工作流的候选池可作为十倍股筛选的输入
2. **主线判断**: 利用9步工作流的投资主线识别结果
3. **因子复用**: 9步工作流的因子计算结果可供评分卡参考

```python
# 整合示例：从9步工作流获取候选池，进行十倍股评估
from core.mcp.client import MCPClient

client = MCPClient()

# 从9步工作流获取候选池
workflow_result = client._call_workflow9_direct("workflow9.run_step", {
    "workflow_id": "xxx",
    "step_id": "candidate_pool"
})
stocks = workflow_result.get("step_result", {}).get("stocks", [])

# 转换为十倍股评估输入
symbols = [s.get("symbol") or s.get("security_id") for s in stocks if isinstance(s, dict)]

# 进行十倍股评估
for symbol in symbols:
    result = tenbagger_evaluate(symbol)
    print(f"{symbol}: {result.get('eval_level')}, {result.get('total_score')}")
```

---

## 📚 相关文档

- `docs/TENBAGGER_DEVELOPMENT_PLAN.md` - 开发计划
- `docs/MUST_READ/08_TENBAGGER_SYSTEM.md` - 系统概述
- `docs/TENBAGGER_RECOMMENDATION_LIST.md` - 推荐列表示例

---

*文档版本: 1.0 | 创建时间: 2025-12-19*
