# 个股分析模块集成总结

> **创建时间**: 2026-01-06  
> **状态**: 设计完成，待实施

---

## 📍 模块位置

### 在工作流中的位置

```
研究阶段流程：
R0 数据源检测
  ↓
R1 市场趋势分析
  ↓
R2 主线轮动研究
  ↓
R3 因子组合开发
  ↓
R4 投资标的筛选 ← 输出：候选股票池（10-30只）
  ↓
【新增】R4.5 个股深度分析 ← 本模块
  ↓
R5 风控模块设计 ← 输入：个股分析报告（风险评估）
  ↓
R6 策略开发与回测
```

### 文件位置

```
core/
└── investment_analysis.py          # 核心分析器（待创建）

scripts/
└── reports/
    └── stock_analysis_report.py    # HTML报告生成器（可复用现有代码）

docs/07_workflow/
├── STOCK_ANALYSIS_MODULE_DESIGN.md  # 详细设计文档
└── STOCK_ANALYSIS_INTEGRATION_SUMMARY.md  # 本文件

output/
└── reports/
    └── stock_analysis/              # 报告输出目录
```

---

## 🎯 核心功能

1. **数据整合**：JQData（价格/财务）+ CNINFO（年报/公告）+ 补充数据源
2. **多维度分析**：历史验证、财务分析、技术分析、事件研究、同概念对比
3. **研报级报告**：多Tab HTML报告，包含交互式图表和可追溯链接

---

## 🔧 应用方式

### 方式1: 工作流自动调用
```python
from core.workflow_orchestrator import WorkflowOrchestrator

orchestrator = WorkflowOrchestrator()
orchestrator.run_full_workflow()  # 自动执行R0-R6，包含R4.5个股分析
```

### 方式2: 独立调用（研究工具）
```python
from core.investment_analysis import InvestmentAnalyzer

analyzer = InvestmentAnalyzer()
result = analyzer.analyze("603778.XSHG")
print(f"报告路径: {result.report_path}")
```

### 方式3: 批量分析
```python
analyzer = InvestmentAnalyzer()
results = analyzer.batch_analyze(["603778.XSHG", "688270.XSHG", ...])
```

---

## 📊 输出结果

### 结构化数据（MongoDB）
- 集合：`trquant.stock_analysis`
- 字段：`stock_code`, `analysis_date`, `summary`, `risk_level`, `recommendation`, `confidence`, `report_path`

### HTML报告（文件系统）
- 路径：`output/reports/stock_analysis/{stock_code}_{date}.html`
- 格式：多Tab HTML，包含交互式图表

---

## ✅ 实施清单

- [x] 设计文档完成
- [ ] 创建核心模块 `core/investment_analysis.py`
- [ ] 集成到 `WorkflowOrchestrator`
- [ ] 更新系统架构文档（添加R4.5节点）
- [ ] 创建研究Notebook `03_stock_analysis.ipynb`
- [ ] 单元测试
- [ ] 集成测试

---

## 📚 相关文档

- **详细设计**：`docs/07_workflow/STOCK_ANALYSIS_MODULE_DESIGN.md`
- **系统架构**：`notebooks/research/00_system_architecture_workflow.ipynb`
- **工作流文档**：`docs/07_workflow/WORKFLOW.md`
