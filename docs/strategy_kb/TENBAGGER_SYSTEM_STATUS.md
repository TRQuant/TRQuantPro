# 十倍股识别系统状态总结

> **更新时间**: 2025-12-19  
> **状态**: V1 + V2 双版本并存

---

## 📊 当前系统架构

### V1 系统（原有）

**位置**: `mcp_servers/utils/tenbagger_evaluator.py`

**核心组件**:
- `TenbaggerEvaluator` - 综合评估器
- `StageMachine` - 阶段状态机（S0-S5）
- `ScoreCard` - 7维评分卡
- `DataSourceManager` - 数据源管理

**MCP工具** (7个):
- `tenbagger.evaluate` - 评估单只股票
- `tenbagger.report` - 获取报告
- `tenbagger.rank` - 获取排名
- `tenbagger.history` - 获取历史
- `tenbagger.batch` - 批量评估
- `tenbagger.filter` - 按等级筛选
- `tenbagger.stats` - 获取统计

**注册位置**: `mcp_servers/trquant_core_server.py`

---

### V2 系统（新增）

**位置**: `mcp_servers/utils/tenbagger_v2/`

**核心组件**:
1. **三层漏斗候选池** (`candidate_funnel.py`)
   - L0 可交易宇宙（硬过滤）
   - L1 早期结构候选（早期信号）
   - L2 十倍路径精评（通过率5%-20%）

2. **规则引擎** (`rule_engine.py`)
   - 10条一票否决规则
   - ST/退市、重大违规、现金流异常、高杠杆等

3. **三轴阶段状态机** (`tri_axis_stage.py`)
   - 基本面轴 / 资金轴 / 预期轴
   - S0观察 → S1验证 → S2导入(最佳) → S3放量

4. **评分引擎V2** (`scoring_engine_v2.py`)
   - 10个因子（缺失惩罚+分布自检）
   - 置信度调整

5. **通过率控制器** (`pass_rate_controller.py`)
   - 目标通过率5%-20%
   - 自动调整阈值

6. **报告生成器** (`report_generator.py`)
   - 标题自动生成
   - 一致性验证

**MCP工具** (7个):
- `tenbagger_v2.evaluate` - 【V2】评估单只股票
- `tenbagger_v2.batch` - 【V2】批量评估
- `tenbagger_v2.report` - 【V2】获取报告
- `tenbagger_v2.recommendations` - 【V2】获取推荐列表
- `tenbagger_v2.stats` - 【V2】获取统计（含通过率控制）
- `tenbagger_v2.generate_report` - 【V2】生成Markdown/JSON报告
- `tenbagger_v2.consistency_check` - 【V2】一致性检查

**注册位置**: `mcp_servers/trquant_core_server.py` (已集成)

---

## 🔄 MCP服务器更新状态

### ✅ 已更新

| 服务器 | 状态 | V1工具 | V2工具 |
|--------|------|--------|--------|
| `trquant_core_server.py` | ✅ 已更新 | 7个 | 7个 |

### 📝 更新内容

**文件**: `mcp_servers/trquant_core_server.py`

**添加内容**:
```python
# ==================== Tenbagger评估工具V2集成 ====================

try:
    from utils.tenbagger_tools_v2 import TENBAGGER_TOOLS_V2, TENBAGGER_HANDLERS_V2
    
    for tool in TENBAGGER_TOOLS_V2:
        TOOLS.append(tool)
        TOOL_HANDLERS[tool.name] = TENBAGGER_HANDLERS_V2.get(tool.name)
    
    TENBAGGER_V2_INTEGRATED = True
    logger.info(f"Tenbagger评估工具V2已集成: {len(TENBAGGER_TOOLS_V2)} 个")
except ImportError as e:
    TENBAGGER_V2_INTEGRATED = False
    logger.warning(f"Tenbagger评估工具V2集成失败: {e}")
```

---

## 📋 工具对比

| 功能 | V1工具 | V2工具 | 差异 |
|------|--------|--------|------|
| 单只评估 | `tenbagger.evaluate` | `tenbagger_v2.evaluate` | V2需要完整data参数 |
| 批量评估 | `tenbagger.batch` | `tenbagger_v2.batch` | V2使用三层漏斗 |
| 获取报告 | `tenbagger.report` | `tenbagger_v2.report` | V2包含更多元数据 |
| 排名 | `tenbagger.rank` | - | V2使用recommendations |
| 筛选 | `tenbagger.filter` | `tenbagger_v2.recommendations` | V2自动过滤推荐 |
| 统计 | `tenbagger.stats` | `tenbagger_v2.stats` | V2包含通过率控制 |
| 历史 | `tenbagger.history` | - | V2暂不支持 |
| 报告生成 | - | `tenbagger_v2.generate_report` | V2新增 |
| 一致性检查 | - | `tenbagger_v2.consistency_check` | V2新增 |

---

## 🚀 使用建议

### V1 vs V2 选择

**使用V1**:
- 需要快速评估，数据不完整
- 兼容现有代码
- 不需要严格的通过率控制

**使用V2**:
- 需要真正的"十倍股早期识别"
- 数据完整，需要三层漏斗筛选
- 需要通过率控制（5%-20%）
- 需要一致性报告

### 迁移建议

1. **新项目**: 直接使用V2工具
2. **现有项目**: 逐步迁移，V1和V2可并存
3. **数据准备**: V2需要更完整的数据（见`tenbagger_v2.evaluate`的data参数）

---

## 📚 相关文档

- `/docs/TENBAGGER_V2_DESIGN.md` - V2设计文档
- `/docs/TENBAGGER_SCORING_LOGIC.md` - 评分逻辑详解
- `/DevMustRead/TENBAGGER_V2_DESIGN.md` - 开发必读
- `/mcp_servers/utils/tenbagger_tools.py` - V1工具实现
- `/mcp_servers/utils/tenbagger_tools_v2.py` - V2工具实现

---

## ✅ 验证方法

### 检查V2工具是否已注册

```python
from core.mcp.client import MCPClient

client = MCPClient()
tools = client.list_tools()  # 或通过MCP协议查询

# 应该看到:
# - tenbagger.* (V1, 7个)
# - tenbagger_v2.* (V2, 7个)
```

### 测试V2工具

```python
# 使用V2评估
result = client.call_tool("tenbagger_v2.evaluate", {
    "symbol": "300001.SZ",
    "name": "测试股票",
    "data": {
        "is_st": False,
        "revenue_growth_qoq_change": 15,
        # ... 其他数据
    }
})
```

---

*文档版本: 1.0 | 创建时间: 2025-12-19*

