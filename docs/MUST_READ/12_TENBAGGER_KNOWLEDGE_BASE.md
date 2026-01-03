# 十倍股早期识别系统 - 知识库条目

> **用途**: 供MCP server调用参考  
> **更新时间**: 2025-12-19

---

## 📋 系统快速参考

### 核心模块调用
```python
# 1. 数据获取
from utils.datasource_manager import get_datasource_manager
manager = get_datasource_manager()
data = manager.fetch_for_tenbagger(["000001.XSHE"])

# 2. 阶段判断
from utils.stage_machine import StageMachine
sm = StageMachine()
record = sm.get_or_create("000001.XSHE")
stage = record.current_stage  # S0-S5

# 3. 综合评估
from utils.tenbagger_evaluator import get_evaluator
evaluator = get_evaluator()
report = evaluator.evaluate(symbol, name, {
    "stage": stage,
    "scorecard": {"total_score": 60.0},
    "financials": data["financials"][symbol]
})
```

### MCP工具调用
```python
# 通过MCP客户端
from core.mcp.client import MCPClient
client = MCPClient()

# 评估
result = client.call_tool("tenbagger.evaluate", {
    "symbol": "000001.XSHE",
    "name": "股票名称",
    "stage": "S2",
    "scorecard": {"total_score": 75},
    "financials": {...}
})

# 排名
rankings = client.call_tool("tenbagger.rank", {"top_n": 20})
```

---

## 🔧 数据源配置

### JQData
- **配置文件**: `config/jqdata_config.json`
- **状态**: ✅ 已认证
- **数据范围**: 2024-09-10 ~ 2025-09-17
- **模式**: 历史模式

### MongoDB
- **连接**: `mongodb://localhost:27017/jqquant`
- **状态**: ✅ 连接正常
- **集合**: 自动创建（stage_records, scorecards, tenbagger_reports）

---

## ⚠️ 注意事项

1. **ScoreCard.compute()**: events参数必须是列表，不能是字符串
2. **StageMachine**: 使用`override_stage()`而不是`update_stage()`
3. **JQData.get_price()**: 使用`get_price_by_count()`获取最近N条数据

---

## 📊 测试状态

- ✅ 数据源连接: 100% 通过
- ✅ 核心模块: 100% 通过
- ✅ MCP集成: 100% 通过
