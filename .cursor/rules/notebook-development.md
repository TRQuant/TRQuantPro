---
name: "Notebook开发规范"
description: "Jupyter Notebook开发规范和最佳实践"
type: "auto-attached"
autoAttach:
  - "**/*.ipynb"
tags: ["notebook", "research", "jupyter"]
---

# Notebook开发规范

## 初始化模式

### 标准初始化（第一个Cell）

所有Notebook的第一个代码cell必须包含路径设置：

```python
# 添加项目根目录到 Python 路径（必须在导入前执行）
import sys
from pathlib import Path

# 自动检测项目根目录
current_dir = Path.cwd()
project_root = None
for parent in [current_dir] + list(current_dir.parents):
    if (parent / 'core').exists() and (parent / 'config').exists():
        project_root = parent
        break

if project_root is None:
    # 回退到默认路径
    project_root = Path('/home/taotao/.cursor/worktrees/TRQuant/ope')

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f'✅ 项目根目录已添加到路径: {project_root}')

# 使用统一环境初始化（推荐）
from notebooks.lib import setup_research_environment
env = setup_research_environment(verbose=True)
```

## 导入规范

### 直接导入Core模块

```python
# ✅ 推荐
from core.market_trend_analyzer import MarketTrendAnalyzer
from core.trend_analyzer import TrendAnalyzer
from core.candidate_pool_builder import CandidatePoolBuilder

# ❌ 不推荐（除非需要工作流集成）
from core.mcp.client import MCPClient
```

### 导入顺序

1. 标准库
2. 第三方库
3. 本地Core模块
4. Notebook工具库

## 可视化规范

### 使用Plotly进行交互式可视化

```python
import plotly.graph_objects as go
import plotly.express as px

fig = go.Figure(...)
fig.update_layout(
    title="市场趋势分析",
    xaxis_title="日期",
    yaxis_title="趋势得分",
    template="plotly_dark"  # 使用暗色主题
)
fig.show()
```

### 使用ChartEngine生成专业图表

```python
from core.visualization.chart_engine import ChartEngine

engine = ChartEngine()
chart = engine.create_trend_chart(data)
chart.show()
```

### 图表要求

- ✅ 必须包含标题
- ✅ 必须包含轴标签
- ✅ 必须包含图例（如果有多个系列）
- ✅ 使用暗色主题（`plotly_dark`）

## 数据保存规范

### 保存分析结果

```python
from notebooks.lib import ResultSaver

saver = ResultSaver(output_dir="notebooks/research/output")
saver.save_dataframe(df, "market_trend_analysis.csv")
saver.save_figure(fig, "market_trend_chart.html")
```

### 输出目录结构

```
notebooks/research/output/
├── data/          # 数据文件
├── charts/        # 图表文件
└── reports/       # HTML报告
```

## 错误处理

### 使用ErrorBoundary

```python
from notebooks.lib import ErrorBoundary

with ErrorBoundary("市场趋势分析", suppress=True) as eb:
    result = analyzer.analyze(...)
    if eb.has_error:
        print(f"⚠️ 分析失败: {eb.error_message}")
```

## 代码组织

### Cell组织原则

1. **Cell 1**: 路径设置和环境初始化
2. **Cell 2**: 导入依赖库
3. **Cell 3-N**: 数据获取和分析
4. **Cell N+1**: 可视化
5. **Cell N+2**: 结果保存

### Markdown Cell使用

- 每个主要部分使用Markdown Cell说明
- 包含目标、方法、结果说明
- 使用标题层级组织内容
