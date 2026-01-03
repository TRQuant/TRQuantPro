# 市场趋势研究 Notebooks

本目录包含市场趋势环境综合评估的研究 Notebooks 和相关工具。

## 📁 目录结构

```
notebooks/research/
├── 01_market_trend_comprehensive.ipynb   # 综合趋势评估
├── 02_ibd_reversal_analysis.ipynb        # IBD反转信号分析
├── 03_multi_period_resonance.ipynb       # 多周期共振分析
├── 04_risk_assessment.ipynb              # 风险评估
├── 05_comprehensive_dashboard.ipynb      # 综合仪表盘
├── 06_market_visualization.ipynb         # 可视化仪表盘
├── config.yaml                           # 统一配置文件
├── output/                               # 输出目录
│   ├── data/                             # 数据输出
│   ├── reports/                          # HTML报告
│   └── charts/                           # 图表
├── .cache/                               # 数据缓存目录
└── README.md                             # 本文件
```

## 🚀 快速开始

### 1. 环境准备

确保已安装所需依赖：

```bash
pip install pandas numpy matplotlib plotly tqdm joblib pyyaml
```

### 2. 运行 Notebook

在 Jupyter 或 Cursor 中打开 Notebook，第一个代码单元会自动初始化环境：

```python
# 统一环境初始化（自动检测项目路径）
from notebooks.lib import setup_research_environment, ErrorBoundary, ResultSaver

env = setup_research_environment(verbose=True)
jq = env.get_jqdata_client()
```

### 3. 修改配置

编辑 `config.yaml` 修改默认参数：

```yaml
data:
  default_index: "000001.XSHG"  # 默认指数
  default_lookback_days: 365    # 默认回看天数

analysis:
  trend:
    periods:
      short:
        days: 40
        weight: 0.2
      # ...
```

## 📊 Notebook 说明

### 01_market_trend_comprehensive.ipynb
**综合趋势评估**

输出 8 个核心动态参数：
1. `trend_score` - 趋势得分 (-1.0 ~ 1.0)
2. `market_regime` - 市场阶段 (bull/bear/volatile/recovery/distribution)
3. `reversal_signal` - 反转信号强度
4. `suggested_position_ratio` - 建议仓位比例
5. `allocation_style_shift` - 风格轮动建议
6. `risk_exposure_score` - 风险暴露得分
7. `volatility_regime` - 波动率环境
8. `trade_frequency_suggestion` - 交易频率建议

### 02_ibd_reversal_analysis.ipynb
**IBD 反转信号分析**

- 跟踪日 (Follow-Through Day) 识别
- 分布日 (Distribution Day) 统计
- 市场状态判定

### 03_multi_period_resonance.ipynb
**多周期共振分析**

- 短期/中期/长期趋势共振
- 指标权重配置
- 共振热力图

### 04_risk_assessment.ipynb
**风险评估**

- VaR 风险价值计算
- 压力测试
- 风险暴露分析

### 05_comprehensive_dashboard.ipynb
**综合仪表盘**

- 核心指标一览
- 信号融合结果
- 策略建议汇总

### 06_market_visualization.ipynb
**可视化仪表盘**

- 趋势得分仪表
- K线图与技术指标
- 状态转换时间轴

## 🛠️ 工具库

### notebooks/lib/

| 模块 | 功能 |
|------|------|
| `research_init.py` | 统一环境初始化，自动检测项目路径 |
| `error_handling.py` | 错误处理装饰器和工具 |
| `result_saver.py` | 结果保存（JSON/CSV/HTML） |
| `data_cache.py` | 数据缓存，避免重复 API 调用 |
| `research_utils.py` | JQData 客户端和知识库接口 |
| `viz_utils.py` | 可视化工具函数 |

### 使用示例

```python
from notebooks.lib import (
    setup_research_environment,
    ErrorBoundary,
    ResultSaver,
    cached_get_price,
    safe_call
)

# 初始化环境
env = setup_research_environment()

# 安全调用（带错误处理）
@safe_call(default=None)
def risky_operation():
    return jq.get_price(...)

# 使用错误边界
with ErrorBoundary("获取数据") as eb:
    data = jq.get_price(...)
if eb.has_error:
    print(f"错误: {eb.error_message}")

# 保存结果
saver = ResultSaver("my_analysis")
saver.save_json(results)
saver.save_html_report(html_content)
```

## 📈 回测脚本

### scripts/backtest_comprehensive.py

```bash
# 使用默认配置
python scripts/backtest_comprehensive.py

# 指定日期范围
python scripts/backtest_comprehensive.py --start 2022-01-01 --end 2024-12-31

# 指定配置文件
python scripts/backtest_comprehensive.py --config my_config.yaml

# 查看帮助
python scripts/backtest_comprehensive.py --help
```

### scripts/compare_research_results.py

```bash
# 对比两个结果文件
python scripts/compare_research_results.py result1.json result2.json

# 对比目录中最新的5个结果
python scripts/compare_research_results.py --dir output/data --latest 5

# 查看帮助
python scripts/compare_research_results.py --help
```

## ⚙️ 配置说明

`config.yaml` 支持的主要配置项：

### 数据配置
```yaml
data:
  default_index: "000001.XSHG"
  indices:
    shanghai: "000001.XSHG"
    csi300: "000300.XSHG"
  cache:
    enabled: true
    ttl_hours: 24
```

### 分析参数
```yaml
analysis:
  trend:
    periods:
      short: { days: 40, weight: 0.2 }
      medium: { days: 120, weight: 0.3 }
      long: { days: 240, weight: 0.5 }
    indicator_weights:
      ma: 0.20
      macd: 0.18
      # ...
```

### 回测参数
```yaml
backtest:
  default_start_date: "2023-01-01"
  initial_capital: 1000000
  commission_rate: 0.0003
  walk_forward:
    train_window: 252
    test_window: 63
```

## 📝 最佳实践

1. **环境初始化**: 使用 `setup_research_environment()` 自动检测项目路径
2. **错误处理**: 使用 `ErrorBoundary` 或 `safe_call` 装饰器
3. **数据缓存**: 使用 `cached_get_price()` 避免重复 API 调用
4. **结果保存**: 使用 `ResultSaver` 自动添加时间戳和元数据
5. **配置管理**: 将参数放在 `config.yaml`，便于复用和修改

## 🔗 相关文档

- [市场趋势算法文档](../../docs/MARKET_TREND_ALGORITHMS.md)
- [市场状态定义](../../core/market_state_definitions.py)
- [PDF研究报告](../../docs/A股市场趋势环境判别与预测方法研究.pdf)

---

*更新日期: 2026-01-01*

