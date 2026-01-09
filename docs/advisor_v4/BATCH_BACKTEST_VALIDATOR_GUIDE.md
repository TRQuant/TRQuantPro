# 批量回测验证器使用指南

## 1. 概述

批量回测验证器（`BatchBacktestValidator`）是一个用于验证策略稳定性和一致性的工具。它支持：

- **多时间段回测**：滚动窗口、季度、年度、自定义时间段
- **市场环境标签**：预留接口，等待算法确认后实现
- **验证标准**：可自定义夏普比率、最大回撤、胜率等指标阈值
- **结果汇总**：自动生成 JSON、CSV、HTML 报告

## 2. 文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 验证器核心 | `core/advisor_v4/batch_backtest_validator.py` | 主要逻辑 |
| 命令行脚本 | `scripts/run_batch_backtest_validation.py` | CLI 工具 |

## 3. 快速开始

### 3.1 滚动窗口验证（推荐）

```bash
# 使用半年窗口，每月滚动
python scripts/run_batch_backtest_validation.py \
    --start-date 2024-01-01 \
    --end-date 2024-12-31 \
    --window 6 \
    --step 1
```

### 3.2 季度验证

```bash
python scripts/run_batch_backtest_validation.py \
    --mode quarterly \
    --start-year 2023 \
    --end-year 2024
```

### 3.3 年度验证

```bash
python scripts/run_batch_backtest_validation.py \
    --mode yearly \
    --start-year 2020 \
    --end-year 2024
```

### 3.4 自定义时间段

```bash
python scripts/run_batch_backtest_validation.py \
    --mode custom \
    --periods "2024-01-01,2024-06-30,H1_2024;2024-07-01,2024-12-31,H2_2024"
```

## 4. 参数说明

### 4.1 验证模式

| 参数 | 说明 |
|------|------|
| `--mode rolling` | 滚动窗口验证（默认） |
| `--mode quarterly` | 季度验证 |
| `--mode yearly` | 年度验证 |
| `--mode custom` | 自定义时间段 |

### 4.2 时间参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--start-date` | 2024-01-01 | 开始日期（rolling/custom模式） |
| `--end-date` | 2024-12-31 | 结束日期（rolling/custom模式） |
| `--window` | 6 | 窗口大小（月，rolling模式） |
| `--step` | 1 | 滚动步长（月，rolling模式） |
| `--start-year` | 2024 | 开始年份（quarterly/yearly模式） |
| `--end-year` | 2024 | 结束年份（quarterly/yearly模式） |

### 4.3 策略参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--initial-capital` | 1000000 | 初始资金 |
| `--max-stocks` | 10 | 最大持股数量 |
| `--single-position` | 0.20 | 单票最大仓位 |
| `--stop-loss` | -0.08 | 止损比例 |
| `--take-profit` | 0.30 | 止盈比例 |
| `--min-total-score` | 30.0 | 最小综合得分 |

### 4.4 验证标准

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--min-sharpe` | 0.5 | 最低夏普比率 |
| `--max-drawdown` | 0.25 | 最大允许回撤 |
| `--min-win-rate` | 0.35 | 最低胜率 |
| `--min-return` | -0.10 | 最低总收益率 |
| `--min-trades` | 5 | 最少交易次数 |

### 4.5 系统参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--cache-dir` | data/cache | 数据缓存目录 |
| `--output-dir` | output/advisor_v4/batch_validation | 输出目录 |
| `--no-gpu` | False | 禁用GPU加速 |
| `--workers` | 3 | 并行工作数 |
| `--quiet` | False | 安静模式 |

## 5. 输出文件

验证完成后，会在 `output/advisor_v4/batch_validation/` 目录生成：

| 文件 | 说明 |
|------|------|
| `validation_summary_YYYYMMDD_HHMMSS.json` | 详细验证结果（JSON） |
| `validation_results_YYYYMMDD_HHMMSS.csv` | 验证结果表格（CSV） |
| `validation_report_YYYYMMDD_HHMMSS.html` | 可视化报告（HTML） |

## 6. Python API 使用

```python
from core.advisor_v4.batch_backtest_validator import (
    BatchBacktestValidator,
    ValidationCriteria
)
from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig

# 创建验证器
validator = BatchBacktestValidator(
    cache_dir="data/cache",
    output_dir="output/advisor_v4/batch_validation",
    use_gpu=True,
    max_workers=3,
    verbose=True
)

# 设置验证标准
validator.set_criteria(ValidationCriteria(
    min_sharpe=0.5,
    max_drawdown=0.25,
    min_win_rate=0.35
))

# 运行滚动窗口验证
summary = validator.run_rolling_validation(
    start_date="2024-01-01",
    end_date="2024-12-31",
    window_months=6,
    step_months=1
)

# 查看结果
print(f"通过率: {summary.passed_periods / summary.total_periods * 100:.1f}%")
print(f"一致性得分: {summary.consistency_score:.2f}")
print(f"稳定性得分: {summary.stability_score:.2f}")
```

## 7. 验证结果解读

### 7.1 整体指标

| 指标 | 说明 | 理想值 |
|------|------|--------|
| 通过率 | 通过验证标准的时间段比例 | ≥80% |
| 一致性得分 | 收益率稳定性（1.0最佳） | ≥0.7 |
| 稳定性得分 | 夏普比率稳定性（1.0最佳） | ≥0.7 |

### 7.2 单时间段指标

| 指标 | 说明 | 及格标准（默认） |
|------|------|------------------|
| 夏普比率 | 风险调整后收益 | ≥0.5 |
| 最大回撤 | 最大亏损幅度 | ≤25% |
| 胜率 | 盈利交易占比 | ≥35% |
| 总收益率 | 时间段总收益 | ≥-10% |
| 交易次数 | 完成交易数量 | ≥5 |

### 7.3 验证结论

| 通过率 | 结论 | 建议 |
|--------|------|------|
| ≥80% | ✅ 策略验证通过 | 可以进入实盘测试 |
| 60%-80% | ⚠️ 策略部分通过 | 建议优化后再测试 |
| <60% | ❌ 策略验证未通过 | 需要重新审视策略逻辑 |

## 8. 市场环境识别（预留）

市场环境识别模块（`MarketEnvironmentDetector`）已预留接口，等待用户确认算法后实现。

接口示例：

```python
# 预留接口
def detect_market_environment(start_date: str, end_date: str) -> MarketEnvironment:
    """
    识别市场环境
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        MarketEnvironment: BULL(牛市), BEAR(熊市), SIDEWAYS(震荡市)
    """
    pass

# 设置识别器
validator.set_market_env_detector(detect_market_environment)
```

## 9. 常见问题

### Q1: 验证太慢怎么办？

- 减少窗口数量：增大 `--step` 参数
- 使用GPU加速：确保安装 PyTorch CUDA 版本
- 使用缓存数据：数据会自动缓存，重复验证会更快

### Q2: 验证标准太严格？

可以放宽验证标准：

```bash
python scripts/run_batch_backtest_validation.py \
    --min-sharpe 0.3 \
    --max-drawdown 0.30 \
    --min-win-rate 0.30
```

### Q3: 如何只验证特定时间段？

使用自定义模式：

```bash
python scripts/run_batch_backtest_validation.py \
    --mode custom \
    --periods "2020-03-01,2020-06-30,疫情期间;2024-09-01,2024-11-30,牛市阶段"
```

## 10. 更新日志

- **v1.0** (2026-01-09): 初始版本
  - 支持滚动窗口、季度、年度、自定义时间段验证
  - 自动生成 JSON/CSV/HTML 报告
  - 预留市场环境识别接口
