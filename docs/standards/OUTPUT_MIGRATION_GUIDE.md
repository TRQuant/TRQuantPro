# 输出目录迁移指南

> **版本**: V1.0  
> **生效日期**: 2026-01-08  
> **目的**: 指导将现有硬编码路径迁移到统一的OutputManager

---

## 📋 迁移原则

1. **统一使用OutputManager**: 所有输出路径通过`OutputManager`获取
2. **按任务分类**: 使用`OutputCategory`枚举分类
3. **按类型分类**: 使用`OutputType`枚举分类
4. **自动创建目录**: `OutputManager`会自动创建所需目录
5. **向后兼容**: 保留旧路径作为默认值（逐步迁移）

---

## 🔄 迁移步骤

### 步骤1: 导入OutputManager

```python
from core.utils.output_manager import (
    get_output_manager,
    OutputCategory,
    OutputType
)
```

### 步骤2: 获取管理器实例

```python
output_manager = get_output_manager()
```

### 步骤3: 替换硬编码路径

#### ❌ 旧代码

```python
# 硬编码路径
report_path = "results/weekly_reports/weekly_layout.html"
backtest_path = "results/backtest_summary_v4.json"
model_path = "models/xgb_high_return_v4.pkl"
```

#### ✅ 新代码

```python
# 使用OutputManager
report_path = output_manager.get_report_path(
    category=OutputCategory.ADVISOR_V4,
    filename="weekly_layout.html",
    add_timestamp=True  # 可选
)

backtest_path = output_manager.get_backtest_path(
    category=OutputCategory.ADVISOR_V4,
    filename="backtest_summary.json",
    add_timestamp=True
)

model_path = output_manager.get_model_path(
    category=OutputCategory.ADVISOR_V4,
    filename="xgb_high_return_v4.pkl"
)
```

---

## 📝 常见迁移场景

### 场景1: HTML报告生成

#### ❌ 旧代码

```python
output_dir = Path("results/weekly_reports")
report_path = output_dir / "weekly_layout.html"
```

#### ✅ 新代码

```python
from core.utils.output_manager import get_output_manager, OutputCategory

output_manager = get_output_manager()
report_path = output_manager.get_report_path(
    category=OutputCategory.ADVISOR_V4,
    filename="weekly_layout.html",
    add_timestamp=True
)
```

### 场景2: CSV数据保存

#### ❌ 旧代码

```python
df.to_csv("results/recommendations_v4_20250908.csv", index=False)
```

#### ✅ 新代码

```python
from core.utils.output_manager import get_output_manager, OutputCategory

output_manager = get_output_manager()
path = output_manager.get_recommendation_path(
    category=OutputCategory.ADVISOR_V4,
    filename="recommendations.csv",
    add_timestamp=True
)
df.to_csv(path, index=False)
```

### 场景3: JSON结果保存

#### ❌ 旧代码

```python
import json
with open("results/backtest_summary_v4.json", "w") as f:
    json.dump(data, f)
```

#### ✅ 新代码

```python
from core.utils.output_manager import get_output_manager, OutputCategory
import json

output_manager = get_output_manager()
path = output_manager.get_backtest_path(
    category=OutputCategory.ADVISOR_V4,
    filename="backtest_summary.json",
    add_timestamp=True
)
with open(path, "w") as f:
    json.dump(data, f)
```

### 场景4: 模型文件保存

#### ❌ 旧代码

```python
model_path = "models/xgb_high_return_v4.pkl"
predictor.save(model_path)
```

#### ✅ 新代码

```python
from core.utils.output_manager import get_output_manager, OutputCategory

output_manager = get_output_manager()
model_path = output_manager.get_model_path(
    category=OutputCategory.ADVISOR_V4,
    filename="xgb_high_return_v4.pkl"
)
predictor.save(str(model_path))
```

---

## 📊 已迁移模块

### ✅ 已完成

1. **WeeklyReportGenerator** (`core/advisor_v4/weekly_report_generator.py`)
   - ✅ 使用`OutputManager`管理报告输出路径
   - ✅ 输出到`output/advisor_v4/reports/`

2. **AdvisorV4Workflow** (`core/advisor_v4/advisor_v4_workflow.py`)
   - ✅ 推荐结果保存路径
   - ✅ 回测结果保存路径
   - ✅ 优化结果保存路径
   - ✅ 配置路径自动初始化

### ⚠️ 待迁移

1. **XGBoostPredictor** (`core/advisor_v4/xgboost_predictor.py`)
   - ⚠️ 模型保存路径

2. **ModelEvolver** (`core/advisor_v4/model_evolver.py`)
   - ⚠️ 进化模型保存路径

3. **ParamOptimizer** (`core/advisor_v4/param_optimizer.py`)
   - ⚠️ 优化结果保存路径

4. **HyperparameterOptimizer** (`core/advisor_v4/hyperparameter_optimizer.py`)
   - ⚠️ 优化历史图保存路径

5. **PredictorFactorExtractor** (`core/advisor_v4/predictor_factor_extractor.py`)
   - ⚠️ 预测特征保存路径

---

## 🎯 输出类别映射

### Advisor V4.0 相关

| 旧路径 | 新路径 | OutputCategory | OutputType |
|--------|-------|----------------|------------|
| `results/weekly_reports/*.html` | `output/advisor_v4/reports/*.html` | `ADVISOR_V4` | `REPORTS` |
| `results/backtest_*.json` | `output/advisor_v4/backtest/*.json` | `ADVISOR_V4` | `BACKTEST` |
| `results/recommendations_*.csv` | `output/advisor_v4/recommendations/*.csv` | `ADVISOR_V4` | `RECOMMENDATIONS` |
| `models/*.pkl` | `output/advisor_v4/models/*.pkl` | `ADVISOR_V4` | `MODELS` |
| `results/optimization_*.json` | `output/advisor_v4/optimization/*.json` | `ADVISOR_V4` | `OPTIMIZATION` |
| `results/*.csv` (数据) | `output/advisor_v4/data/*.csv` | `ADVISOR_V4` | `DATA` |

---

## ⚠️ 注意事项

1. **路径类型**: `OutputManager.get_path()` 返回 `Path` 对象，需要转换为字符串时使用 `str(path)`
2. **时间戳**: 使用 `add_timestamp=True` 自动添加时间戳，格式为 `YYYYMMDD_HHMMSS`
3. **目录创建**: `OutputManager` 会自动创建所需目录，无需手动创建
4. **向后兼容**: 如果配置中指定了路径，将使用指定路径；如果为`None`，则使用`OutputManager`自动生成

---

## 📚 参考

- **OutputManager 源码**: `core/utils/output_manager.py`
- **输出目录规范**: `docs/standards/OUTPUT_DIRECTORY_STANDARD.md`
- **使用示例**: 见已迁移模块的代码

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-08
