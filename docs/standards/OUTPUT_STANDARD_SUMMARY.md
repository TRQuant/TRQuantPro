# 统一输出目录管理规范 - 实施总结

> **实施日期**: 2026-01-08  
> **状态**: ✅ 已完成核心模块迁移

---

## ✅ 已完成工作

### 1. 创建OutputManager工具类

**文件**: `core/utils/output_manager.py`

**功能**:
- ✅ 统一的输出目录管理
- ✅ 按任务/模块分类（OutputCategory）
- ✅ 按文件类型分类（OutputType）
- ✅ 自动创建目录
- ✅ 时间戳支持
- ✅ 文件清理功能

**目录结构**:
```
output/
├── advisor_v4/          # Investment Advisor V4.0
│   ├── reports/         # HTML报告
│   ├── backtest/        # 回测结果
│   ├── models/          # 模型文件
│   ├── recommendations/ # 推荐结果
│   ├── optimization/    # 优化结果
│   ├── data/           # 数据文件
│   └── logs/           # 日志文件
├── market_trend/        # 市场趋势分析
├── tenbagger/           # 十倍股策略
├── workflow/            # 工作流结果
└── shared/              # 共享文件
```

### 2. 更新核心模块

#### ✅ WeeklyReportGenerator

**文件**: `core/advisor_v4/weekly_report_generator.py`

**变更**:
- ✅ 使用`OutputManager`管理报告输出路径
- ✅ 输出到`output/advisor_v4/reports/`

#### ✅ AdvisorV4Workflow

**文件**: `core/advisor_v4/advisor_v4_workflow.py`

**变更**:
- ✅ 添加`_init_output_paths()`方法自动初始化路径
- ✅ 推荐结果保存到`output/advisor_v4/recommendations/`
- ✅ 回测结果保存到`output/advisor_v4/backtest/`
- ✅ 优化结果保存到`output/advisor_v4/optimization/`
- ✅ 配置路径自动初始化（如果为None）

### 3. 创建规范文档

**文档**:
1. ✅ `docs/standards/OUTPUT_DIRECTORY_STANDARD.md` - 输出目录规范
2. ✅ `docs/standards/OUTPUT_MIGRATION_GUIDE.md` - 迁移指南
3. ✅ `docs/standards/OUTPUT_STANDARD_SUMMARY.md` - 实施总结（本文档）

---

## 📊 测试验证

### 测试结果

```bash
$ python scripts/v4_full_integration_test.py
✅ 所有测试通过！
📄 生成的报告: output/advisor_v4/reports/v4_full_integration_test.html
```

### 验证内容

- ✅ OutputManager导入成功
- ✅ 路径生成正确（`output/advisor_v4/reports/`）
- ✅ 目录自动创建
- ✅ 报告生成成功

---

## 🎯 使用示例

### 基本使用

```python
from core.utils.output_manager import get_output_manager, OutputCategory

# 获取管理器
manager = get_output_manager()

# 获取报告路径
report_path = manager.get_report_path(
    category=OutputCategory.ADVISOR_V4,
    filename="weekly_layout.html",
    add_timestamp=True
)

# 获取回测路径
backtest_path = manager.get_backtest_path(
    category=OutputCategory.ADVISOR_V4,
    filename="backtest_summary.json",
    add_timestamp=True
)
```

### 便捷函数

```python
from core.utils.output_manager import get_output_path, OutputCategory, OutputType

# 直接获取路径
path = get_output_path(
    category=OutputCategory.ADVISOR_V4,
    output_type=OutputType.REPORTS,
    filename="weekly_layout.html"
)
```

---

## ⚠️ 待迁移模块

以下模块仍使用硬编码路径，建议逐步迁移：

1. **XGBoostPredictor** - 模型保存路径
2. **ModelEvolver** - 进化模型保存路径
3. **ParamOptimizer** - 优化结果保存路径
4. **HyperparameterOptimizer** - 优化历史图保存路径
5. **PredictorFactorExtractor** - 预测特征保存路径

---

## 📝 迁移检查清单

### 代码检查

- [ ] 搜索硬编码路径：`grep -r "results/" core/`
- [ ] 搜索硬编码路径：`grep -r "models/" core/`
- [ ] 检查`.to_csv()`调用
- [ ] 检查`.to_json()`调用
- [ ] 检查`.save()`调用

### 迁移步骤

1. 导入`OutputManager`
2. 替换硬编码路径
3. 测试验证
4. 更新文档

---

## 🔍 路径映射表

| 旧路径 | 新路径 | 状态 |
|--------|-------|------|
| `results/weekly_reports/*.html` | `output/advisor_v4/reports/*.html` | ✅ 已迁移 |
| `results/backtest_*.json` | `output/advisor_v4/backtest/*.json` | ✅ 已迁移 |
| `results/recommendations_*.csv` | `output/advisor_v4/recommendations/*.csv` | ✅ 已迁移 |
| `results/optimization_*.json` | `output/advisor_v4/optimization/*.json` | ✅ 已迁移 |
| `models/*.pkl` | `output/advisor_v4/models/*.pkl` | ⚠️ 待迁移 |
| `results/*.csv` (数据) | `output/advisor_v4/data/*.csv` | ⚠️ 待迁移 |

---

## 📚 参考文档

1. **输出目录规范**: `docs/standards/OUTPUT_DIRECTORY_STANDARD.md`
2. **迁移指南**: `docs/standards/OUTPUT_MIGRATION_GUIDE.md`
3. **OutputManager源码**: `core/utils/output_manager.py`

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-08
