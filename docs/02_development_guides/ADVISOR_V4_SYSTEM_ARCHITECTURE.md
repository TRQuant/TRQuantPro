# Investment Advisor V4.0 系统架构说明文档

> **版本**: V4.0  
> **生成时间**: 2026-01-08  
> **维护者**: TRQuant Team

---

## 📋 目录

1. [系统概述](#系统概述)
2. [系统架构](#系统架构)
3. [代码组织结构](#代码组织结构)
4. [数据流向](#数据流向)
5. [运行流程](#运行流程)
6. [模块详细说明](#模块详细说明)
7. [输出文件结构](#输出文件结构)
8. [配置说明](#配置说明)
9. [依赖关系](#依赖关系)
10. [关键设计决策](#关键设计决策)

---

## 1. 系统概述

### 1.1 系统定位

**Investment Advisor V4.0** 是一个基于机器学习的多因子预测投资系统，核心特点是：

- **预测性因子**: 使用 T-1周（T-5交易日）时刻的数据预测 T 时刻的高收益
- **机器学习模型**: XGBoost 自动学习因子组合和权重
- **完整交易系统**: 入场、出场、仓位、风控一体化
- **参数优化**: 基于遗传算法和递归优化的因子选择、权重优化
- **防过拟合**: 特征工程流水线、时序交叉验证、Walk-Forward验证、过拟合检测

### 1.2 核心功能

1. **训练模式**: 从历史案例提取预测因子，训练 XGBoost 模型
2. **回测模式**: 支持三层回测（Fast/Standard/Precise）
3. **推荐模式**: 生成本周投资推荐（Weekly Layout）
4. **优化模式**: 使用递归优化算法优化因子选择、因子权重、融合权重
5. **策略生成**: 生成聚宽格式策略代码
6. **数据存储**: MongoDB 存储策略、回测结果、推荐记录

---

## 2. 系统架构

### 2.1 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                   表现层 (Entry Points)                      │
│  - scripts/test_advisor_v4_e2e.py (端到端测试)              │
│  - scripts/train_advisor_v4.py (训练脚本)                   │
│  - scripts/run_advisor_v4.py (运行脚本)                     │
│  - scripts/validate_advisor_v4.py (验证脚本)                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                   工作流层 (Workflow)                        │
│  - core/advisor_v4/advisor_v4_workflow.py                   │
│    ├── train() - 训练流程                                   │
│    ├── backtest() - 回测流程                                │
│    ├── recommend() - 推荐流程                               │
│    ├── optimize_factors() - 因子优化流程                    │
│    └── generate_weekly_layout_report() - 报告生成           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                   核心模块层 (Core Modules)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 数据层 (Data Layer)                                   │  │
│  │  - predictor_factor_extractor.py (因子提取)           │  │
│  │  - predictor_factor_extractor_parallel.py (并行提取)  │  │
│  │  - multi_factor_calculator.py (多维因子计算)          │  │
│  │  - validated_factor_calculator.py (已验证因子)        │  │
│  │  - data_validator.py (数据验证清洗)                   │  │
│  │  - data_augmenter.py (数据增强)                       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 模型层 (Model Layer)                                  │  │
│  │  - xgboost_predictor.py (XGBoost预测器)               │  │
│  │  - feature_pipeline.py (特征工程流水线)               │  │
│  │  - cross_validator.py (交叉验证)                      │  │
│  │  - ensemble_predictor.py (集成预测器)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 策略层 (Strategy Layer)                               │  │
│  │  - trading_strategy.py (交易策略)                     │  │
│  │  - rule_based_strategy.py (规则引擎)                  │  │
│  │  - weekly_layout_planner.py (周度布局规划)            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 优化层 (Optimization Layer)                           │  │
│  │  - factor_optimizer.py (因子优化器)                   │  │
│  │  - param_optimizer.py (参数优化器)                    │  │
│  │  - hyperparameter_optimizer.py (超参数优化)           │  │
│  │  - model_evolver.py (模型进化)                        │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 回测层 (Backtest Layer)                               │  │
│  │  - backtest_engine.py (回测引擎)                      │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 输出层 (Output Layer)                                 │  │
│  │  - weekly_report_generator.py (报告生成器)            │  │
│  │  - factor_optimization_report_generator.py (优化报告) │  │
│  │  - joinquant_strategy_generator.py (策略代码生成)     │  │
│  │  - data_storage.py (MongoDB存储)                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                   基础设施层 (Infrastructure)                │
│  - core/utils/output_manager.py (输出路径管理)              │
│  - core/backtest/unified_backtest_manager.py (统一回测)     │
│  - config/config_manager.py (配置管理)                      │
│  - JQData (聚宽数据接口)                                    │
│  - MongoDB (数据存储)                                       │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 核心组件关系

```
┌─────────────────────────────────────────────────────────────┐
│                  AdvisorV4Workflow (工作流)                  │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Factor       │  │ MultiFactor  │  │ Predictor    │     │
│  │ Extractor    │→ │ Calculator   │→ │ Factor       │     │
│  │              │  │              │  │ Extractor    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         ↓                ↓                ↓                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Data Pipeline (数据流水线)                │  │
│  │  - DataValidator (验证清洗)                          │  │
│  │  - FeaturePipeline (特征工程)                        │  │
│  │  - CrossValidator (交叉验证)                         │  │
│  └──────────────────────────────────────────────────────┘  │
│         ↓                                                    │
│  ┌──────────────┐                                           │
│  │ XGBoost      │                                           │
│  │ Predictor    │                                           │
│  └──────────────┘                                           │
│         ↓                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Trading      │  │ Rule-Based   │  │ Weekly       │     │
│  │ Strategy     │→ │ Strategy     │→ │ Layout       │     │
│  │              │  │              │  │ Planner      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         ↓                                                    │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ Backtest     │  │ Factor       │                        │
│  │ Engine       │  │ Optimizer    │                        │
│  └──────────────┘  └──────────────┘                        │
│         ↓                ↓                                   │
│  ┌──────────────────────────────────────┐                  │
│  │      Output & Storage (输出存储)     │                  │
│  │  - ReportGenerator                   │                  │
│  │  - DataStorage (MongoDB)             │                  │
│  └──────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 代码组织结构

### 3.1 目录结构

```
TRQuant/ope/
├── core/
│   └── advisor_v4/                    # V4核心模块目录
│       ├── __init__.py                # 模块导出定义
│       ├── advisor_v4_workflow.py     # ⭐ 主工作流（1460行）
│       │
│       ├── 数据层 (Data Layer)
│       ├── predictor_factor_extractor.py              # 因子提取器（基础版）
│       ├── predictor_factor_extractor_parallel.py     # 因子提取器（并行+GPU）
│       ├── multi_factor_calculator.py                 # 多维因子计算器
│       ├── validated_factor_calculator.py             # 已验证因子计算器
│       ├── jqfactor_calculator.py                     # 聚宽因子计算器
│       ├── data_validator.py                          # 数据验证和清洗
│       ├── data_augmenter.py                          # 数据增强
│       │
│       ├── 模型层 (Model Layer)
│       ├── xgboost_predictor.py                       # XGBoost预测器
│       ├── feature_pipeline.py                        # 特征工程流水线（734行）
│       ├── cross_validator.py                         # 交叉验证（时序/Walk-Forward）
│       ├── ensemble_predictor.py                      # 集成预测器
│       │
│       ├── 策略层 (Strategy Layer)
│       ├── trading_strategy.py                        # 交易策略（入场/出场/仓位）
│       ├── rule_based_strategy.py                     # 规则引擎（可解释过滤）
│       ├── weekly_layout_planner.py                   # 周度布局规划器
│       │
│       ├── 优化层 (Optimization Layer)
│       ├── factor_optimizer.py                        # 因子优化器（递归优化）
│       ├── param_optimizer.py                         # 参数优化器（遗传算法）
│       ├── hyperparameter_optimizer.py                # 超参数优化器
│       ├── rule_optimizer.py                          # 规则优化器
│       ├── model_evolver.py                           # 模型进化器
│       │
│       ├── 回测层 (Backtest Layer)
│       ├── backtest_engine.py                         # 回测引擎
│       │
│       ├── 输出层 (Output Layer)
│       ├── weekly_report_generator.py                 # 周度报告生成器
│       ├── factor_optimization_report_generator.py    # 因子优化报告生成器
│       ├── joinquant_strategy_generator.py            # 聚宽策略代码生成器
│       ├── data_storage.py                            # MongoDB数据存储
│       │
│       └── 工具层 (Utility Layer)
│       ├── feature_expander.py                        # 特征扩展器
│       └── gpu_accelerator.py                         # GPU加速器
│
├── scripts/                            # 脚本入口
│   ├── test_advisor_v4_e2e.py         # ⭐ 端到端测试脚本
│   ├── train_advisor_v4.py            # 训练脚本
│   ├── run_advisor_v4.py              # 运行脚本
│   ├── validate_advisor_v4.py         # 验证脚本
│   └── evolve_advisor_v4.py           # 进化脚本
│
├── output/
│   └── advisor_v4/                    # 输出目录（OutputManager管理）
│       ├── data/                      # 数据文件
│       │   ├── high_return_cases_full_train.csv
│       │   ├── high_return_cases_cleaned.csv
│       │   ├── predictive_features.csv
│       │   └── training_data_v4.csv
│       ├── models/                    # 模型文件
│       │   ├── xgb_high_return_v4.pkl
│       │   └── feature_pipeline_v4.pkl
│       ├── backtest/                  # 回测结果（4037个JSON文件）
│       ├── reports/                   # HTML报告
│       │   ├── weekly_layout_*.html
│       │   ├── factor_optimization_report_*.html
│       │   └── e2e_test_summary_*.json
│       ├── recommendations/           # 推荐结果
│       └── optimization/              # 优化结果（待创建）
│
└── docs/
    └── 02_development_guides/
        └── ADVISOR_V4_SYSTEM_ARCHITECTURE.md  # 本文档
```

### 3.2 关键文件说明

#### 3.2.1 主工作流文件

**`core/advisor_v4/advisor_v4_workflow.py`** (1460行)

这是系统的核心文件，负责整合所有模块，提供统一的接口。

**主要类**:
- `AdvisorV4Config`: 配置类，包含所有可配置参数
- `AdvisorV4Workflow`: 主工作流类

**主要方法**:
```python
# 训练流程
def train(skip_extraction=False, skip_negative_sampling=False, 
          use_feature_pipeline=None, use_cv=None, cv_method=None)

# 回测流程
def backtest(start_date=None, end_date=None, rebalance_freq='weekly',
             backtest_levels=None, save_to_db=True)

# 推荐流程
def recommend(date=None, top_n=10, fast_mode=False)

# 周度布局推荐
def recommend_weekly_layout(anchor_date=None, top_n=5)

# 因子优化流程
def optimize_factors(start_date=None, end_date=None, max_iterations=10,
                     fast_mode=False)

# 报告生成
def generate_weekly_layout_report(anchor_date=None, top_n=5,
                                  output_filename=None, fast_mode=False)
```

#### 3.2.2 端到端测试脚本

**`scripts/test_advisor_v4_e2e.py`** (935行)

提供完整的端到端测试功能，包括：
- 环境检查（JQData、GPU、MongoDB、数据文件）
- 数据验证和清洗
- 模型训练
- 因子优化
- 回测验证
- 推荐生成
- 报告生成
- 结果汇总

**运行方式**:
```bash
# 快速模式（跳过训练和优化）
python scripts/test_advisor_v4_e2e.py

# 完整模式（包含递归优化，耗时较长）
python scripts/test_advisor_v4_e2e.py --full

# 跳过特定阶段
python scripts/test_advisor_v4_e2e.py --skip-training --skip-optimization
```

---

## 4. 数据流向

### 4.1 训练流程数据流

```
┌─────────────────────────────────────────────────────────────┐
│ 输入: high_return_cases_full_train.csv (历史高收益案例)    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 0: 数据验证和清洗                                      │
│  - DataValidator.validate_and_clean()                       │
│  输出: high_return_cases_cleaned.csv                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 1: 因子提取（并行+GPU加速）                            │
│  - ParallelPredictorFactorExtractor.extract_from_historical │
│  输出: predictive_features.csv (T-1周时刻的因子数据)        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: 构建训练数据集                                      │
│  - _build_training_dataset()                                │
│  操作: 正样本 + 负样本采样                                   │
│  输出: training_data_v4.csv                                 │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: 特征工程流水线                                      │
│  - FeaturePipeline.fit_transform()                          │
│  操作: 特征选择 + 标准化                                     │
│  输出: 转换后的训练集和验证集                                 │
│  保存: feature_pipeline_v4.pkl                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: 交叉验证（可选）                                    │
│  - TimeSeriesCrossValidator / WalkForwardValidator          │
│  输出: CVResult (验证稳定性)                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: 训练XGBoost模型                                     │
│  - XGBoostPredictor.train()                                 │
│  操作: 正则化 + 早停                                         │
│  输出: xgb_high_return_v4.pkl                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 6: 过拟合检测                                          │
│  - XGBoostPredictor.detect_overfitting()                    │
│  输出: 过拟合报告                                            │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 推荐流程数据流

```
┌─────────────────────────────────────────────────────────────┐
│ 输入: 当前日期 (date)                                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 1: 获取股票池                                          │
│  - JQData.get_all_securities()                              │
│  过滤: 排除688开头、ST股票                                   │
│  快速模式: 100只股票 / 完整模式: 500只股票                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: 计算多维因子                                        │
│  - MultiFactorCalculator.calculate_all_factors()            │
│  因子类型:                                                  │
│    - 技术因子 (动量、相对强度、RSI等)                        │
│    - 基本面因子 (ROE、PE、PB等)                              │
│    - 资金因子 (换手率、成交量等)                             │
│    - 情绪因子 (涨跌幅、波动率等)                             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: 应用特征流水线（如果已训练）                        │
│  - FeaturePipeline.transform()                              │
│  操作: 特征选择 + 标准化                                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: 模型预测                                            │
│  - XGBoostPredictor.predict()                               │
│  输出: 每只股票的高收益概率 (probability)                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: 规则引擎融合                                        │
│  - RuleBasedStrategy.score_candidates()                     │
│  操作: 可解释过滤 + 打分融合                                 │
│  输出: total_score (预测概率70% + 规则得分30%)               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 6: 生成交易信号                                        │
│  - TradingStrategy.generate_entry_signals()                 │
│  过滤: min_probability, min_score                           │
│  输出: List[TradeSignal]                                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 7: 周度布局规划                                        │
│  - WeeklyLayoutPlanner.build_from_candidates()              │
│  输出: WeeklyLayoutPlan                                     │
│    - targets: List[LayoutTarget]                            │
│    - entry_plan: Dict[str, EntryPlan]                       │
│    - exit_plan: Dict[str, ExitPlan]                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 8: 生成HTML报告                                        │
│  - WeeklyReportGenerator.generate()                         │
│  输出: weekly_layout_YYYY-MM-DD.html                        │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 因子优化流程数据流

```
┌─────────────────────────────────────────────────────────────┐
│ 输入: 优化区间 (start_date, end_date)                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 迭代优化（递归优化）                                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Phase 1: 因子选择优化                               │    │
│  │  - FactorOptimizer.optimize_factor_selection()     │    │
│  │  操作: 从候选因子池中选择最优因子组合                │    │
│  │  评估: Walk-Forward回测 + 多目标优化                 │    │
│  │  输出: 最优因子组合 ['momentum_20d', 'rel_position'│    │
│  │        , 'market_cap']                              │    │
│  └────────────────────────────────────────────────────┘    │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Phase 2: 因子权重优化                               │    │
│  │  - FactorOptimizer.optimize_factor_weights()       │    │
│  │  操作: 优化已选因子的权重分配                        │    │
│  │  评估: Walk-Forward回测                             │    │
│  │  输出: 最优因子权重 {factor: weight}                │    │
│  └────────────────────────────────────────────────────┘    │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Phase 3: 融合权重优化                               │    │
│  │  - FactorOptimizer.optimize_fusion_weights()       │    │
│  │  操作: 优化"已验证因子"与"聚宽因子"的融合权重        │    │
│  │  评估: Walk-Forward回测                             │    │
│  │  输出: 最优融合权重 (已验证因子50% / 聚宽因子50%)    │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  早停机制: 连续3次迭代无改进则停止                           │
│  缓存机制: 相同参数组合命中缓存，跳过回测                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 生成优化报告                                                │
│  - FactorOptimizationReportGenerator.generate()             │
│  输出: factor_optimization_report_YYYYMMDD_HHMMSS.html      │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. 运行流程

### 5.1 完整运行流程（端到端）

```python
# scripts/test_advisor_v4_e2e.py

# Step 1: 环境检查
check_environment()
  - 检查JQData连接
  - 检查GPU可用性
  - 检查MongoDB连接
  - 检查数据文件存在性
  - 检查Python环境

# Step 2: 数据验证和清洗
run_data_validation()
  - DataValidator.validate_and_clean()
  - 保存清洗后的数据

# Step 3: 模型训练（可选）
if not skip_training:
    run_model_training()
      - workflow.train(skip_extraction=False)
      - 因子提取（并行+GPU）
      - 构建训练数据集
      - 特征工程
      - 交叉验证
      - 模型训练
      - 过拟合检测

# Step 4: 因子优化（可选，完整模式）
if not skip_optimization and full_mode:
    run_factor_optimization()
      - workflow.optimize_factors(fast_mode=False)
      - 递归优化（因子选择 + 权重优化 + 融合权重优化）
      - 生成优化报告

# Step 5: 回测验证（可选）
if not skip_backtest:
    run_backtest()
      - workflow.backtest()
      - 三层回测（Fast/Standard/Precise）
      - 保存回测结果到MongoDB

# Step 6: 推荐生成
run_recommendation()
  - workflow.recommend_weekly_layout()
    - workflow.recommend()  # 生成信号
    - WeeklyLayoutPlanner.build_from_candidates()  # 构建布局计划
  - 保存推荐到JSON和MongoDB

# Step 7: 报告生成
generate_report()
  - workflow.generate_weekly_layout_report()
    - WeeklyReportGenerator.generate()
  - 生成HTML报告

# Step 8: 结果汇总
generate_summary()
  - 汇总所有阶段结果
  - 保存到e2e_test_summary_YYYYMMDD_HHMMSS.json
```

### 5.2 快速模式 vs 完整模式

#### 快速模式（默认）

```python
python scripts/test_advisor_v4_e2e.py
```

**特点**:
- 跳过模型训练（使用已有模型）
- 跳过因子优化（使用默认因子组合）
- 跳过回测验证
- 推荐时使用快速模式（100只股票）
- **总耗时**: ~2-3分钟

**适用场景**: 快速验证推荐功能、日常使用

#### 完整模式

```python
python scripts/test_advisor_v4_e2e.py --full
```

**特点**:
- 执行完整训练流程（因子提取 + 模型训练）
- 执行递归因子优化（因子选择 + 权重优化 + 融合权重优化）
- 执行回测验证
- 推荐时使用完整模式（500只股票）
- **总耗时**: ~60-120分钟（取决于数据量和优化迭代次数）

**适用场景**: 系统全面验证、模型重训练、因子优化

### 5.3 单阶段运行

```python
# 只运行训练
python scripts/test_advisor_v4_e2e.py --skip-optimization --skip-backtest --skip-recommendation --skip-report

# 只运行推荐
python scripts/test_advisor_v4_e2e.py --skip-training --skip-optimization --skip-backtest --skip-report

# 只运行报告生成
python scripts/test_advisor_v4_e2e.py --skip-training --skip-optimization --skip-backtest --skip-recommendation
```

---

## 6. 模块详细说明

### 6.1 数据层模块

#### 6.1.1 PredictorFactorExtractor (基础版)

**文件**: `core/advisor_v4/predictor_factor_extractor.py`

**功能**: 从历史高收益案例中提取预测性因子（T-1周时刻）

**主要方法**:
- `extract_from_historical_cases()`: 从历史案例提取因子

**输出**: `predictive_features.csv`

#### 6.1.2 ParallelPredictorFactorExtractor (并行版)

**文件**: `core/advisor_v4/predictor_factor_extractor_parallel.py`

**功能**: 并行版本的因子提取器，支持GPU加速

**特点**:
- 多进程并行（最多3个JQData连接）
- GPU批量计算技术指标
- 断点续传（checkpoint机制）

**主要方法**:
- `extract_from_historical_cases()`: 并行提取因子

#### 6.1.3 MultiFactorCalculator

**文件**: `core/advisor_v4/multi_factor_calculator.py`

**功能**: 计算多维因子（技术、基本面、资金、情绪）

**因子维度**:
1. **技术因子**: 动量、相对强度、RSI、MACD等
2. **基本面因子**: ROE、PE、PB、营收增长率等
3. **资金因子**: 换手率、成交量、资金流向等
4. **情绪因子**: 涨跌幅、波动率、市场情绪等

**主要方法**:
- `calculate_all_factors()`: 计算所有因子
- `calculate_technical_factors()`: 计算技术因子
- `calculate_fundamental_factors()`: 计算基本面因子

#### 6.1.4 DataValidator

**文件**: `core/advisor_v4/data_validator.py`

**功能**: 数据验证和清洗

**验证项**:
- 缺失值检查
- 异常值检测
- 重复数据检测
- 数据类型验证
- 数据范围验证

**主要方法**:
- `validate_and_clean()`: 验证并清洗数据
- `clip_outliers()`: 截断异常值
- `get_report()`: 获取验证报告

### 6.2 模型层模块

#### 6.2.1 XGBoostPredictor

**文件**: `core/advisor_v4/xgboost_predictor.py`

**功能**: XGBoost预测模型，包含防过拟合机制

**特点**:
- 正则化参数（L1/L2）
- 早停机制
- 过拟合检测
- 特征重要性分析

**主要方法**:
- `train()`: 训练模型
- `predict()`: 预测概率
- `predict_proba()`: 预测概率（详细）
- `detect_overfitting()`: 过拟合检测
- `evaluate()`: 模型评估

#### 6.2.2 FeaturePipeline

**文件**: `core/advisor_v4/feature_pipeline.py` (734行)

**功能**: 特征工程流水线（特征选择 + 标准化）

**流水线步骤**:
1. **数据验证和清洗**: DataValidator
2. **特征派生**: FeatureEngineer（创建新特征）
3. **特征选择**: FeatureSelector（选择Top K特征）
4. **特征标准化**: StandardScaler

**特征选择方法**:
- `mutual_info`: 互信息
- `f_score`: F统计量
- `combined`: 组合方法（默认）

**主要方法**:
- `fit_transform()`: 在训练集上拟合并转换
- `transform()`: 在测试集上转换
- `save()` / `load()`: 保存/加载流水线

#### 6.2.3 CrossValidator

**文件**: `core/advisor_v4/cross_validator.py`

**功能**: 时序交叉验证和Walk-Forward验证

**验证方法**:
1. **TimeSeriesCrossValidator**: 时序交叉验证（固定折数）
2. **WalkForwardValidator**: Walk-Forward验证（滚动窗口）

**主要类**:
- `TimeSeriesCrossValidator`: 时序CV
- `WalkForwardValidator`: Walk-Forward CV
- `OverfittingDetector`: 过拟合检测器

### 6.3 策略层模块

#### 6.3.1 TradingStrategy

**文件**: `core/advisor_v4/trading_strategy.py`

**功能**: 交易策略（入场、出场、仓位管理）

**主要类**:
- `TradingConfig`: 交易配置
- `TradeSignal`: 交易信号
- `Position`: 持仓信息
- `TradingStrategy`: 交易策略

**主要方法**:
- `generate_entry_signals()`: 生成入场信号
- `generate_exit_signals()`: 生成出场信号
- `calculate_position_size()`: 计算仓位大小

#### 6.3.2 RuleBasedStrategy

**文件**: `core/advisor_v4/rule_based_strategy.py`

**功能**: 规则引擎（可解释过滤和打分）

**特点**:
- 基于规则的过滤（市值、流动性、涨跌停等）
- 可解释性打分
- 与预测模型融合（70%预测 + 30%规则）

**主要方法**:
- `score_candidates()`: 对候选股票打分
- `apply_rules()`: 应用规则过滤

#### 6.3.3 WeeklyLayoutPlanner

**文件**: `core/advisor_v4/weekly_layout_planner.py`

**功能**: 周度布局规划器

**主要数据结构**:
- `LayoutTarget`: 布局标的
- `EntryPlan`: 入场计划（分批建仓）
- `ExitPlan`: 出场计划（止盈/止损）
- `WeeklyLayoutPlan`: 周度布局计划

**主要方法**:
- `build_from_candidates()`: 从候选列表构建布局计划
- `build_with_entry_plans()`: 构建包含入场计划的布局

### 6.4 优化层模块

#### 6.4.1 FactorOptimizer

**文件**: `core/advisor_v4/factor_optimizer.py`

**功能**: 因子优化器（递归优化）

**优化流程**:
1. **因子选择优化**: 从候选因子池中选择最优组合
2. **因子权重优化**: 优化已选因子的权重分配
3. **融合权重优化**: 优化"已验证因子"与"聚宽因子"的融合权重

**优化方法**:
- 网格搜索（Grid Search）
- 多目标优化（Sharpe比率、命中率、总收益率、稳定性）

**缓存机制**:
- 相同参数组合命中缓存，跳过回测
- 使用MD5哈希参数组合作为缓存键

**主要方法**:
- `optimize_factor_selection()`: 优化因子选择
- `optimize_factor_weights()`: 优化因子权重
- `optimize_fusion_weights()`: 优化融合权重
- `optimize()`: 完整优化流程

### 6.5 回测层模块

#### 6.5.1 BacktestEngine

**文件**: `core/advisor_v4/backtest_engine.py`

**功能**: 回测引擎

**回测层级**:
1. **Fast**: 快速回测（向量化计算，<5秒）
2. **Standard**: 标准回测（事件驱动，<30秒）
3. **Precise**: 精确回测（完整模拟，需要BulletTrade/QMT）

**主要方法**:
- `run()`: 运行回测
- `calculate_metrics()`: 计算绩效指标

### 6.6 输出层模块

#### 6.6.1 WeeklyReportGenerator

**文件**: `core/advisor_v4/weekly_report_generator.py`

**功能**: 生成周度布局HTML报告

**报告内容**:
- 市场展望
- 推荐标的列表（代码、名称、概率、得分、价格、止盈、止损、仓位）
- 入场计划（分批建仓）
- 出场计划（止盈/止损）
- 风险控制建议

#### 6.6.2 FactorOptimizationReportGenerator

**文件**: `core/advisor_v4/factor_optimization_report_generator.py`

**功能**: 生成因子优化报告

**报告内容**:
- 优化参数配置
- 最优因子组合
- 最优因子权重
- 最优融合权重
- 优化过程（迭代历史）
- 回测绩效指标

#### 6.6.3 DataStorage

**文件**: `core/advisor_v4/data_storage.py`

**功能**: MongoDB数据存储

**存储内容**:
- 策略代码记录
- 回测结果记录
- 推荐记录
- 模型参数记录

**主要方法**:
- `save_strategy_code()`: 保存策略代码
- `save_backtest_result()`: 保存回测结果
- `save_recommendation()`: 保存推荐记录

---

## 7. 输出文件结构

### 7.1 输出目录结构

```
output/advisor_v4/
├── data/                          # 数据文件
│   ├── high_return_cases_full_train.csv          # 原始高收益案例
│   ├── high_return_cases_cleaned.csv             # 清洗后的数据
│   ├── high_return_cases_cleaned_validation_report.txt  # 验证报告
│   ├── predictive_features.csv                   # 预测因子数据
│   └── training_data_v4.csv                      # 训练数据集
│
├── models/                        # 模型文件
│   ├── xgb_high_return_v4.pkl                    # XGBoost模型
│   └── feature_pipeline_v4.pkl                   # 特征流水线
│
├── backtest/                      # 回测结果（4037个JSON文件）
│   ├── backtest_summary_YYYYMMDD_HHMMSS.json     # 回测摘要
│   └── ...
│
├── reports/                       # HTML报告
│   ├── weekly_layout_YYYY-MM-DD.html             # 周度布局报告
│   ├── factor_optimization_report_YYYYMMDD_HHMMSS.html  # 因子优化报告
│   ├── e2e_test_summary_YYYYMMDD_HHMMSS.json     # 端到端测试汇总
│   └── e2e_test.log                               # 测试日志
│
├── recommendations/               # 推荐结果
│   └── recommendations_YYYYMMDD.json              # 推荐JSON
│
└── optimization/                  # 优化结果（待创建）
    └── factor_optimization_YYYYMMDD_HHMMSS.json
```

### 7.2 关键输出文件说明

#### 7.2.1 模型文件

**`xgb_high_return_v4.pkl`**
- 类型: XGBoost模型（pickle格式）
- 大小: ~几MB
- 用途: 用于预测股票高收益概率

**`feature_pipeline_v4.pkl`**
- 类型: FeaturePipeline对象（pickle格式）
- 大小: ~几百KB
- 用途: 特征选择和标准化

#### 7.2.2 报告文件

**`weekly_layout_YYYY-MM-DD.html`**
- 类型: HTML报告
- 内容: 周度投资布局建议
- 包含: 推荐标的、入场计划、出场计划、风险控制

**`factor_optimization_report_YYYYMMDD_HHMMSS.html`**
- 类型: HTML报告
- 内容: 因子优化结果
- 包含: 最优因子组合、权重、优化过程、回测绩效

#### 7.2.3 回测结果文件

**`backtest_summary_YYYYMMDD_HHMMSS.json`**
- 类型: JSON格式
- 内容: 回测绩效指标
- 字段:
  ```json
  {
    "start_date": "2025-04-29",
    "end_date": "2025-08-28",
    "initial_capital": 1000000,
    "final_capital": 1042500.78,
    "total_return": 0.0425,
    "annualized_return": 0.1330,
    "max_drawdown": -0.0515,
    "sharpe_ratio": 1.1389,
    "total_trades": 346,
    "win_rate": 0.1190,
    "hit_10pct_rate": 0.0
  }
  ```

---

## 8. 配置说明

### 8.1 AdvisorV4Config 配置项

```python
@dataclass
class AdvisorV4Config:
    # 数据路径（使用OutputManager自动管理）
    high_return_cases_path: Optional[str] = None
    predictive_features_path: Optional[str] = None
    training_data_path: Optional[str] = None
    model_path: Optional[str] = None
    feature_pipeline_path: Optional[str] = None
    
    # 训练配置（周频）
    lookback_weeks: int = 1              # 预测因子提前周数
    train_start: str = "2024-09-01"
    train_end: str = "2025-06-30"
    val_start: str = "2025-07-01"
    val_end: str = "2025-09-30"
    test_start: str = "2025-09-30"
    test_end: str = "2025-12-31"
    
    # 交易配置
    trading_config: TradingConfig = field(default_factory=TradingConfig)
    
    # 特征工程配置
    use_feature_pipeline: bool = True    # 是否使用特征流水线
    top_k_features: int = 10             # 选择Top K特征
    feature_select_method: str = 'combined'  # 特征选择方法
    
    # 交叉验证配置
    use_cv: bool = True                  # 是否使用交叉验证
    cv_method: str = 'walk_forward'      # 'time_series' 或 'walk_forward'
    cv_n_splits: int = 5                 # 时序CV折数
    cv_train_months: int = 3             # Walk-Forward训练月数
    cv_test_months: int = 1              # Walk-Forward测试月数
    
    # 正则化配置
    use_regularization: bool = True      # 是否使用增强正则化
    early_stopping_rounds: int = 20      # 早停轮数
```

### 8.2 TradingConfig 配置项

```python
@dataclass
class TradingConfig:
    min_probability: float = 0.6         # 最小预测概率阈值
    min_score: float = 70.0              # 最小得分阈值
    max_position_per_stock: float = 0.20 # 单票最大仓位
    take_profit: float = 0.15            # 止盈比例
    stop_loss: float = -0.08             # 止损比例
    trailing_stop: float = 0.03          # 追踪止损比例
```

### 8.3 FactorOptimizationConfig 配置项

```python
@dataclass
class FactorOptimizationConfig:
    candidate_factors: List[str] = field(default_factory=lambda: [
        'momentum_5d', 'momentum_10d', 'momentum_20d',
        'rel_position', 'market_cap', 'turnover_rate',
        'roe', 'pe_ratio', 'pb_ratio'
    ])
    max_selected_factors: int = 5        # 最多选择因子数
    optimization_objectives: List[str] = field(default_factory=lambda: [
        'sharpe_ratio', 'hit_rate', 'total_return', 'stability'
    ])
    max_iterations: int = 10             # 最大迭代次数
    early_stop_patience: int = 3         # 早停耐心值
    cache_enabled: bool = True           # 是否启用缓存
```

---

## 9. 依赖关系

### 9.1 外部依赖

```python
# 核心依赖
pandas >= 1.5.0
numpy >= 1.20.0
scikit-learn >= 1.0.0
xgboost >= 1.6.0

# 数据源
jqdatasdk  # 聚宽数据接口

# 数据库
pymongo >= 4.0.0

# GPU加速（可选）
torch >= 1.10.0  # 用于GPU批量计算技术指标

# 可视化（可选）
plotly >= 5.0.0  # 用于生成交互式图表

# 工具库
tqdm >= 4.60.0   # 进度条
```

### 9.2 内部依赖

```python
# 项目内部模块
core.utils.output_manager      # 输出路径管理
core.backtest.unified_backtest_manager  # 统一回测管理器
config.config_manager          # 配置管理
```

### 9.3 模块依赖图

```
advisor_v4_workflow.py
  ├── predictor_factor_extractor.py
  ├── multi_factor_calculator.py
  ├── xgboost_predictor.py
  ├── feature_pipeline.py
  ├── cross_validator.py
  ├── trading_strategy.py
  ├── rule_based_strategy.py
  ├── weekly_layout_planner.py
  ├── factor_optimizer.py
  ├── backtest_engine.py
  ├── weekly_report_generator.py
  ├── data_storage.py
  └── data_validator.py

feature_pipeline.py
  ├── data_validator.py
  ├── feature_expander.py (内部)
  └── scikit-learn

xgboost_predictor.py
  └── xgboost

factor_optimizer.py
  ├── backtest_engine.py
  └── cross_validator.py

multi_factor_calculator.py
  ├── validated_factor_calculator.py
  ├── jqfactor_calculator.py
  └── jqdatasdk
```

---

## 10. 关键设计决策

### 10.1 周频时间口径

**设计**: 系统采用"自然周"作为唯一时间口径，动态适配节假日。

**原因**:
- A股市场存在节假日停牌
- 固定交易日数不适用于实际交易
- 自然周便于理解和执行

**实现**:
- `get_trading_days_in_week()`: 获取自然周的交易日列表
- `get_week_start_end()`: 获取自然周的首尾交易日
- `get_prev_week_anchor()`: 获取前一周锚点交易日

### 10.2 预测性因子设计

**设计**: 使用 T-1周（T-5交易日）时刻的数据预测 T 时刻的高收益。

**原因**:
- 避免未来信息泄露（look-ahead bias）
- 符合实际交易场景（提前一周布局）
- 提高预测的可信度

### 10.3 防过拟合机制

**设计**: 多层次防过拟合机制。

**机制**:
1. **特征工程流水线**: 特征选择 + 标准化
2. **交叉验证**: 时序CV / Walk-Forward验证
3. **正则化**: L1/L2正则化 + 早停
4. **过拟合检测**: 训练集/验证集性能差距检测

**原因**:
- 机器学习模型容易过拟合
- 金融数据噪声大、样本少
- 过拟合会导致实盘表现差

### 10.4 递归优化架构

**设计**: 三层递归优化（因子选择 → 因子权重 → 融合权重）。

**原因**:
- 因子组合空间大，需要分阶段优化
- 不同阶段优化目标不同
- 递归优化可以逐步收敛到最优解

**优化策略**:
- 网格搜索 + 多目标优化
- 早停机制（连续3次无改进）
- 缓存机制（避免重复回测）

### 10.5 输出路径统一管理

**设计**: 使用 `OutputManager` 统一管理所有输出路径。

**原因**:
- 避免硬编码路径
- 统一目录结构
- 便于版本管理和清理

**实现**:
```python
from core.utils.output_manager import get_output_manager, OutputCategory, OutputType

output_manager = get_output_manager()
data_path = output_manager.get_path(
    OutputCategory.ADVISOR_V4, 
    OutputType.DATA, 
    "predictive_features.csv"
)
```

### 10.6 快速模式设计

**设计**: 提供快速模式和完整模式两种运行方式。

**快速模式特点**:
- 减少股票数量（100只 vs 500只）
- 跳过耗时步骤（训练、优化）
- 降低阈值以确保推荐生成

**原因**:
- 日常使用需要快速响应
- 完整流程耗时较长（60-120分钟）
- 快速模式可以快速验证功能

---

## 11. 已知问题和待优化项

### 11.1 已知问题

1. **`deepcopy` 导入问题** (已修复)
   - 问题: `recommend()` 函数中 `deepcopy` 在条件块内导入，但在条件块外使用
   - 状态: ✅ 已修复，将导入移到函数开头

2. **`LayoutTarget` 属性访问问题** (已修复)
   - 问题: 代码试图访问 `t.entry_plan`，但 `entry_plan` 在 `WeeklyLayoutPlan` 中，不在 `LayoutTarget` 中
   - 状态: ✅ 已修复，改为从 `layout_plan.entry_plan` 字典中访问

3. **因子优化报告未生成**
   - 问题: 优化报告HTML文件路径未正确生成或保存
   - 状态: ⚠️ 待确认

### 11.2 待优化项

1. **GPU加速优化**
   - 当前: GPU加速仅用于技术指标批量计算
   - 优化: 扩展到更多计算密集型操作

2. **并行优化**
   - 当前: 因子提取支持并行，因子优化不支持
   - 优化: 因子优化的Walk-Forward回测可以并行化

3. **缓存优化**
   - 当前: 因子优化使用MD5哈希缓存
   - 优化: 可以扩展到更多场景，使用Redis等外部缓存

4. **错误处理**
   - 当前: 部分错误处理不够完善
   - 优化: 增加更详细的错误信息和降级方案

5. **文档完善**
   - 当前: 部分模块缺少详细文档
   - 优化: 补充API文档和使用示例

---

## 12. 使用示例

### 12.1 基本使用

```python
from core.advisor_v4 import AdvisorV4Workflow, AdvisorV4Config

# 创建配置
config = AdvisorV4Config(
    train_start="2024-09-01",
    train_end="2025-06-30",
    test_start="2025-09-30",
    test_end="2025-12-31"
)

# 创建工作流
workflow = AdvisorV4Workflow(config, verbose=True)

# 训练模型
workflow.train()

# 生成推荐
signals = workflow.recommend(date="2025-12-31", top_n=10)

# 生成周度布局报告
report_path = workflow.generate_weekly_layout_report(
    anchor_date="2025-12-31",
    top_n=5
)
print(f"报告已生成: {report_path}")
```

### 12.2 因子优化使用

```python
# 执行因子优化
optimization_result = workflow.optimize_factors(
    start_date="2025-09-30",
    end_date="2025-12-31",
    max_iterations=10,
    fast_mode=False  # 完整模式
)

print(f"最优因子组合: {optimization_result.best_factor_selection}")
print(f"最优因子权重: {optimization_result.best_factor_weights}")
print(f"最优融合权重: {optimization_result.best_fusion_weights}")
```

### 12.3 端到端测试使用

```bash
# 快速模式（跳过训练和优化）
python scripts/test_advisor_v4_e2e.py

# 完整模式（包含递归优化）
python scripts/test_advisor_v4_e2e.py --full

# 自定义选项
python scripts/test_advisor_v4_e2e.py \
    --skip-training \
    --skip-optimization \
    --skip-backtest \
    --skip-report
```

---

## 13. 总结

### 13.1 系统特点

1. **完整性**: 从数据输入到推荐输出，完整的投资决策流程
2. **可扩展性**: 模块化设计，易于扩展新功能
3. **可维护性**: 统一的输出管理、清晰的代码结构
4. **防过拟合**: 多层次防过拟合机制
5. **性能优化**: GPU加速、并行处理、缓存机制

### 13.2 核心价值

1. **预测性**: 基于历史数据预测未来高收益
2. **自动化**: 从因子提取到推荐生成全自动化
3. **可解释性**: 规则引擎提供可解释的过滤和打分
4. **优化性**: 递归优化确保因子组合和权重最优
5. **实用性**: 周度布局规划符合实际交易场景

---

**文档版本**: V1.0  
**最后更新**: 2026-01-08  
**维护者**: TRQuant Team
