# TRQuant 十倍股早期识别系统完整文档

> **版本**: v1.0  
> **创建时间**: 2025-12-19  
> **状态**: ✅ 已实现并集成到MCP服务器

---

## 📋 系统概述

十倍股早期识别系统通过多维度数据分析、阶段状态机、评分卡引擎等核心模块，实现对高成长潜力股票的系统化识别与跟踪。

### 核心理念

```
十倍股发展路径: S0(观察) → S1(验证) → S2(导入) → S3(放量) → S4(加速) → S5(成熟)

识别窗口: S1-S3阶段是最佳介入期
```

---

## 🏗️ 系统架构

### 1. 核心模块

#### 1.1 十倍股评估引擎 (`TenbaggerEvaluator`)
**位置**: `mcp_servers/utils/tenbagger_evaluator.py`

**评估维度** (7个维度):
- **阶段评估** (20%): S0-S5阶段判断
- **评分卡** (25%): 7维评分卡
- **成长性** (15%): 财务成长指标
- **行业地位** (15%): 市场份额、竞争格局
- **另类数据** (10%): AltData信号
- **市场动量** (10%): 技术指标
- **风险调整** (5%): 风险因子

**等级划分**:
- **S+**: ≥85分 - 极高潜力
- **S**: ≥75分 - 高潜力
- **A**: ≥65分 - 中等潜力
- **B**: ≥50分 - 一般潜力
- **C**: ≥35分 - 低潜力
- **D**: <35分 - 不推荐

#### 1.2 MCP工具 (`tenbagger_tools.py`)
**位置**: `mcp_servers/utils/tenbagger_tools.py`

**工具列表** (7个):
1. `tenbagger.evaluate` - 综合评估股票的十倍股潜力
2. `tenbagger.report` - 获取股票的评估报告
3. `tenbagger.rank` - 获取所有已评估股票排名
4. `tenbagger.history` - 获取股票评估历史
5. `tenbagger.batch` - 批量评估多只股票
6. `tenbagger.filter` - 按等级筛选股票
7. `tenbagger.stats` - 获取评估统计信息

#### 1.3 阶段状态机 (`StageMachine`)
**位置**: `mcp_servers/utils/stage_machine.py`

**阶段定义**:
- **S0**: 观察期 - 早期信号，待验证
- **S1**: 验证期 - 初步验证，潜力待确认
- **S2**: 导入期 - 成长黄金期，最佳介入点
- **S3**: 放量期 - 快速增长，关注估值
- **S4**: 加速期 - 接近成熟，注意风险
- **S5**: 成熟期 - 增长放缓，估值偏高

#### 1.4 7维评分卡 (`ScoreCard`)
**位置**: `mcp_servers/utils/scorecard.py`

**评分维度**:
1. 盈利能力
2. 成长性
3. 财务健康
4. 估值水平
5. 行业地位
6. 管理质量
7. 市场表现

---

## 🔧 MCP服务器集成

### 集成位置
**文件**: `mcp_servers/trquant_core_server.py`

**集成代码**:
```python
from utils.tenbagger_tools import TENBAGGER_TOOLS, TENBAGGER_HANDLERS

for tool in TENBAGGER_TOOLS:
    TOOLS.append(tool)
    TOOL_HANDLERS[tool.name] = TENBAGGER_HANDLERS.get(tool.name)
```

**状态**: ✅ 已集成到 `trquant-core` MCP服务器

---

## 📊 使用方法

### 1. 评估单只股票
```python
from mcp_servers.utils.tenbagger_evaluator import get_evaluator

evaluator = get_evaluator()
data = {
    "stage": "S2",
    "scorecard": {"total_score": 75},
    "financials": {"revenue_growth": 0.3},
    "industry": {},
    "altdata": {},
    "technicals": {}
}
report = evaluator.evaluate("000001.XSHE", "股票名称", data)
```

### 2. 获取排名
```python
rankings = evaluator.rank_all()[:20]  # TOP20
for symbol, score, level in rankings:
    print(f"{symbol}: {score:.1f} ({level.value})")
```

### 3. 批量评估
```python
stocks = [
    {"symbol": "000001.XSHE", "name": "股票1", "data": {...}},
    {"symbol": "000002.XSHE", "name": "股票2", "data": {...}}
]
results = evaluator.batch_evaluate(stocks)
```

---

## 🔗 相关模块

### 数据源管理
- `mcp_servers/utils/datasource_manager.py` - 数据源管理器
- `mcp_servers/utils/datasource_tools.py` - 数据源MCP工具

### 事件抽取
- `mcp_servers/utils/event_extractor.py` - 从公告/互动易抽取事件

### 策略集成
- `mcp_servers/utils/strategy_pack.py` - 包含TenbaggerStrategy策略

---

## ⚠️ 注意事项

1. **数据依赖**: 需要JQData财务数据、阶段状态数据
2. **评估频率**: 建议每日更新评估结果
3. **历史追踪**: 系统自动保存评估历史，支持趋势分析
4. **等级筛选**: 建议关注S+和S级股票

---

## 📚 相关文档

- `docs/TENBAGGER_DEVELOPMENT_PLAN.md` - 开发计划
- `docs/SYSTEM_SUMMARY.md` - 系统总结
- `extension/python/tenbagger_commands.py` - Python命令接口
