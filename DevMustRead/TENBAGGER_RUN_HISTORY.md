# 十倍股筛选系统运行历史记录

> **文档创建时间**: 2025-12-19  
> **目的**: 记录十倍股筛选系统的运行方式和历史

---

## 📅 2025-12-19 早上运行记录

### 运行时间
- **文件创建时间**: 2025-12-19 10:23:12 (北京时间)
- **脚本位置**: `scripts/run_tenbagger_screening.py`
- **输出文档**: `docs/TENBAGGER_RECOMMENDATION_LIST.md`

### 运行方式

**执行命令**:
```bash
cd /home/taotao/dev/QuantTest/TRQuant
python3 scripts/run_tenbagger_screening.py
```

### 运行流程

#### 步骤1: 获取投资主线和候选池

**使用的模块**:
- `core.mainline_scanner.MainlineBasedScanner`
- `jqdata.client.JQDataClient`
- `config.config_manager.get_config_manager`

**关键代码**:
```python
# 初始化JQData
config = get_config_manager().get_jqdata_config()
jq_client = JQDataClient(
    username=config.get("username"),
    password=config.get("password")
)

# 扫描主线
scanner = MainlineBasedScanner(jq_client=jq_client)
result = scanner.scan_from_mainlines(
    period="medium",
    min_score=60.0,
    max_mainlines=10,
    max_stocks_per_mainline=20
)

mainlines = result.get("mainlines", [])
stocks = result.get("stocks", [])
```

**结果**:
- 获取到多条投资主线
- 从主线中提取候选股票（限制30只进行评估）

#### 步骤2: 批量评估十倍股潜力

**使用的模块**:
- `extension.python.tenbagger_commands.tenbagger_evaluate`

**关键代码**:
```python
from extension.python.tenbagger_commands import tenbagger_evaluate

for stock_info in stock_list:
    symbol = stock_info["symbol"]
    name = stock_info["name"]
    
    result = tenbagger_evaluate(symbol)
    
    evaluated_stocks.append({
        "symbol": symbol,
        "name": name,
        "mainline": stock_info.get("mainline", "未知"),
        "stage": result.get("stage", "S0"),
        "scorecard_score": result.get("scorecard_score", 0),
        "total_score": result.get("total_score", 0),
        "eval_level": result.get("eval_level", "D"),
        "recommendation": result.get("recommendation", "")
    })
```

**评估结果**:
- 评估股票数: 15只
- 推荐股票数: 14只
- S级: 1只 | A级: 13只 | B级: 1只

#### 步骤3: 排序和筛选

**筛选标准**:
- 按总分降序排序
- 筛选A级及以上（总分 >= 50.0）

**等级分布**:
- S级: 1只（中际旭创 300308.XSHE）
- A级: 13只
- B级: 1只

**阶段分布**:
- S1阶段（验证期）: 1只
- S2阶段（导入期，最佳介入点）: 13只
- S3阶段（放量期）: 1只

#### 步骤4: 生成推荐列表报告

**报告内容**:
1. 推荐概览（评估数、推荐数、等级分布、阶段分布）
2. TOP 5 重点推荐（详细分析）
3. 完整推荐名录（表格形式）
4. 按主线分类（人工智能、商业航天、新能源、半导体）
5. 投资建议（S2阶段重点推荐）
6. 风险提示
7. 评估说明

**报告保存位置**: `docs/TENBAGGER_RECOMMENDATION_LIST.md`

---

## 🔍 运行结果分析

### TOP 5 推荐股票

| 排名 | 代码 | 名称 | 阶段 | 等级 | 总分 | 评分卡 | 主线 |
|------|------|------|------|------|------|--------|------|
| 1 | 300308.XSHE | 中际旭创 | S3 | **S** | 75.5 | 100.0 | 人工智能 |
| 2 | 001696.XSHE | 宗申动力 | S2 | A | 73.0 | 100.0 | 商业航天 |
| 3 | 002006.XSHE | 精工科技 | S2 | A | 73.0 | 100.0 | 商业航天 |
| 4 | 300750.XSHE | 宁德时代 | S2 | A | 71.5 | 100.0 | 新能源 |
| 5 | 688012.XSHG | 中微公司 | S2 | A | 71.5 | 100.0 | 半导体 |

### 主线分布

- **商业航天**: 5只
- **人工智能**: 4只
- **新能源**: 2只
- **半导体**: 3只

---

## 📝 关键发现

1. **评分卡分数异常**: 大部分股票的评分卡分数都是100.0分，这可能表示：
   - 评分卡计算逻辑需要检查
   - 或者这些股票确实在财务指标上表现优秀

2. **阶段分布集中**: 13只股票处于S2阶段（导入期），这是十倍股的最佳介入点

3. **主线集中**: 主要集中在4条主线：商业航天、人工智能、新能源、半导体

---

## 🔄 与当前MCP工作流程的对比

### 早上运行方式（直接调用Python模块）

```python
# 方式1: 使用MainlineBasedScanner获取候选池
scanner = MainlineBasedScanner(jq_client=jq_client)
result = scanner.scan_from_mainlines(...)

# 方式2: 使用tenbagger_commands评估
from extension.python.tenbagger_commands import tenbagger_evaluate
result = tenbagger_evaluate(symbol)
```

### 当前MCP工作流程（通过MCP工具）

```python
# 方式1: 使用MCP工具获取数据
client.call("datasource.fetch_all", {"symbols": [...]})

# 方式2: 使用MCP工具批量评估
client.call("tenbagger.batch", {"stocks": [...]})
```

### 两种方式的区别

| 对比项 | 早上运行方式 | MCP工作流程 |
|--------|-------------|------------|
| **候选池获取** | `MainlineBasedScanner.scan_from_mainlines()` | 从9步工作流或直接指定 |
| **数据获取** | 内嵌在`tenbagger_evaluate`中 | `datasource.fetch_all` |
| **评估方式** | `tenbagger_commands.tenbagger_evaluate()` | `tenbagger.batch` MCP工具 |
| **优势** | 简单直接，一步到位 | 模块化，可扩展，符合MCP架构 |

---

## 💡 建议

1. **保持两种方式兼容**: 
   - Python直接调用方式（`tenbagger_commands`）适合脚本和快速测试
   - MCP工具方式适合GUI和分布式调用

2. **统一数据源**:
   - 确保两种方式使用相同的数据源和评估逻辑

3. **记录运行日志**:
   - 建议在脚本中添加日志记录功能，保存每次运行的详细日志

---

## 📚 相关文档

- `docs/TENBAGGER_MCP_WORKFLOW.md` - MCP工作流程文档
- `docs/TENBAGGER_RECOMMENDATION_LIST.md` - 推荐列表（早上运行结果）
- `scripts/run_tenbagger_screening.py` - 运行脚本

---

*文档版本: 1.0 | 创建时间: 2025-12-19*

