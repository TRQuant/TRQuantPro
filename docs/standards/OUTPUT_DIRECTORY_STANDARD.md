# 统一输出目录管理规范

> **版本**: V1.0  
> **生效日期**: 2026-01-08  
> **适用范围**: TRQuant 所有模块

---

## 📋 规范概述

**核心原则**：
- ✅ 所有生成的文件统一放在 `output/` 目录下
- ✅ 按总任务/模块设立子文件夹管理
- ✅ 使用 `OutputManager` 统一管理输出路径
- ✅ 禁止硬编码输出路径

---

## 📁 目录结构

```
output/
├── advisor_v4/              # Investment Advisor V4.0
│   ├── reports/             # HTML报告
│   │   ├── weekly_layout_20250908.html
│   │   └── weekly_layout_20250915.html
│   ├── backtest/            # 回测结果
│   │   ├── fast_20250908.json
│   │   ├── standard_20250908.json
│   │   └── precise_20250908.json
│   ├── models/              # 模型文件
│   │   ├── xgboost_model_v1.pkl
│   │   └── feature_pipeline_v1.pkl
│   ├── recommendations/      # 推荐结果
│   │   ├── recommendations_20250908.csv
│   │   └── weekly_layout_plan_20250908.json
│   ├── optimization/        # 优化结果
│   │   ├── rule_optimization_20250908.json
│   │   └── param_optimization_20250908.json
│   └── logs/                # 日志文件
│       └── advisor_v4_20250908.log
│
├── market_trend/            # 市场趋势分析
│   ├── reports/
│   ├── signals/
│   └── backtest/
│
├── tenbagger/               # 十倍股策略
│   ├── reports/
│   ├── screening/
│   └── backtest/
│
├── workflow/                # 工作流结果
│   ├── reports/
│   └── strategies/
│
└── shared/                  # 共享文件
    ├── data/
    └── cache/
```

---

## 🔧 使用方法

### 1. 基本使用

```python
from core.utils.output_manager import get_output_manager, OutputCategory, OutputType

# 获取输出管理器
manager = get_output_manager()

# 获取报告路径
report_path = manager.get_report_path(
    category=OutputCategory.ADVISOR_V4,
    filename="weekly_layout.html",
    add_timestamp=True  # 可选：添加时间戳
)

# 获取回测结果路径
backtest_path = manager.get_backtest_path(
    category=OutputCategory.ADVISOR_V4,
    filename="fast_validation.json",
    add_timestamp=True
)
```

### 2. 快捷方法

```python
from core.utils.output_manager import get_output_manager, OutputCategory

manager = get_output_manager()

# 报告
report_path = manager.get_report_path("advisor_v4", "weekly_layout.html")

# 回测
backtest_path = manager.get_backtest_path("advisor_v4", "fast_validation.json")

# 模型
model_path = manager.get_model_path("advisor_v4", "xgboost_model.pkl")

# 推荐
recommendation_path = manager.get_recommendation_path("advisor_v4", "recommendations.csv")

# 优化
optimization_path = manager.get_optimization_path("advisor_v4", "rule_optimization.json")

# 日志
log_path = manager.get_log_path("advisor_v4", "advisor_v4.log")
```

### 3. 便捷函数

```python
from core.utils.output_manager import get_output_path, OutputCategory, OutputType

# 直接获取路径
path = get_output_path(
    category=OutputCategory.ADVISOR_V4,
    output_type=OutputType.REPORTS,
    filename="weekly_layout.html",
    add_timestamp=True
)
```

---

## 📝 代码迁移指南

### ❌ 旧代码（禁止）

```python
# 硬编码路径
output_dir = Path("results/weekly_reports")
report_path = output_dir / "weekly_layout.html"

# 分散的路径定义
report_path = "results/recommendations_v4_20250908.csv"
backtest_path = "results/backtest_summary_v4.json"
```

### ✅ 新代码（推荐）

```python
from core.utils.output_manager import get_output_manager, OutputCategory

manager = get_output_manager()

# 统一使用 OutputManager
report_path = manager.get_report_path(
    OutputCategory.ADVISOR_V4,
    "weekly_layout.html",
    add_timestamp=True
)

recommendation_path = manager.get_recommendation_path(
    OutputCategory.ADVISOR_V4,
    "recommendations.csv",
    add_timestamp=True
)
```

---

## 🎯 输出类别定义

### OutputCategory（输出类别）

- `ADVISOR_V4`: Investment Advisor V4.0 系统
- `MARKET_TREND`: 市场趋势分析
- `TENBAGGER`: 十倍股策略
- `WORKFLOW`: 工作流结果
- `SHARED`: 共享文件

### OutputType（输出类型）

- `REPORTS`: HTML/PDF报告
- `BACKTEST`: 回测结果（JSON/CSV）
- `MODELS`: 模型文件（PKL/H5）
- `RECOMMENDATIONS`: 推荐结果（CSV/JSON）
- `OPTIMIZATION`: 优化结果（JSON）
- `LOGS`: 日志文件（LOG/TXT）
- `DATA`: 数据文件（CSV/PARQUET）
- `CACHE`: 缓存文件
- `SIGNALS`: 信号文件
- `SCREENING`: 筛选结果
- `STRATEGIES`: 策略文件

---

## 🔍 文件命名规范

### 时间戳格式

- **日期时间戳**: `YYYYMMDD_HHMMSS`（如：`20250908_143022`）
- **日期戳**: `YYYYMMDD`（如：`20250908`）

### 文件名规范

- **小写字母 + 下划线**: `weekly_layout_report.html`
- **包含版本号**: `model_v1.pkl`, `model_v2.pkl`
- **包含日期**: `recommendations_20250908.csv`
- **描述性命名**: `fast_validation_result.json` 而非 `result.json`

---

## 🧹 清理策略

### 自动清理

```python
from core.utils.output_manager import get_output_manager, OutputCategory, OutputType

manager = get_output_manager()

# 清理30天前的报告文件
deleted = manager.cleanup_old_files(
    category=OutputCategory.ADVISOR_V4,
    output_type=OutputType.REPORTS,
    keep_days=30,
    pattern="*.html"
)
```

### 手动清理

```bash
# 清理30天前的文件
find output/advisor_v4/reports -type f -mtime +30 -delete
```

---

## 📊 各模块迁移清单

### ✅ 已迁移

- `core/advisor_v4/weekly_report_generator.py` - 周度报告生成器

### ⚠️ 待迁移

- `core/advisor_v4/advisor_v4_workflow.py` - 主工作流（推荐结果、回测结果）
- `core/advisor_v4/xgboost_predictor.py` - 模型保存
- `core/advisor_v4/model_evolver.py` - 进化模型保存
- `core/advisor_v4/param_optimizer.py` - 优化结果保存
- `core/advisor_v4/hyperparameter_optimizer.py` - 优化历史图
- `core/market_trend/` - 市场趋势分析结果
- `research/tenbagger_10x_strategy/` - 十倍股策略结果

---

## ⚠️ 注意事项

1. **禁止硬编码路径**: 所有输出路径必须通过 `OutputManager` 获取
2. **自动创建目录**: `OutputManager` 会自动创建所需目录
3. **时间戳可选**: 根据需求决定是否添加时间戳
4. **版本管理**: 模型文件建议包含版本号
5. **清理策略**: 定期清理旧文件，避免磁盘空间不足

---

## 📚 参考

- **OutputManager 源码**: `core/utils/output_manager.py`
- **使用示例**: 见各模块的迁移代码

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-08
