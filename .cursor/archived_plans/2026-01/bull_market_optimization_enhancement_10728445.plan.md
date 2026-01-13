---
name: Bull Market Optimization Enhancement
overview: 基于算法分析，完善牛市策略优化框架：1) 修复BulletTrade验证功能 2) 实现真正的递归优化（粗网格→细网格） 3) 改进简化版回测准确性 4) 添加过拟合检测机制
todos:
  - id: phase1-fix-bt
    content: "Phase 1: 修复BulletTrade验证参数映射问题"
    status: completed
  - id: phase1-enhance-bt
    content: "Phase 1: 增强BulletTrade验证（Top 5验证+偏差分析）"
    status: completed
    dependencies:
      - phase1-fix-bt
  - id: phase2-recursive
    content: "Phase 2: 实现递归优化框架（粗网格→细网格）"
    status: completed
  - id: phase2-refine
    content: "Phase 2: 实现网格细化函数和收敛检测"
    status: completed
    dependencies:
      - phase2-recursive
  - id: phase3-sample
    content: "Phase 3: 改进简化回测（增加样本量）"
    status: completed
  - id: phase3-path
    content: "Phase 3: 模拟持仓路径和交易成本"
    status: completed
    dependencies:
      - phase3-sample
  - id: phase4-filter
    content: "Phase 4: 添加过拟合检测和筛选机制"
    status: completed
  - id: phase5-test
    content: "Phase 5: 集成测试和文档更新"
    status: completed
    dependencies:
      - phase1-enhance-bt
      - phase2-refine
      - phase3-path
      - phase4-filter
---

# 牛市策略优化框架完善计划

## 当前问题分析

基于算法分析，发现以下关键问题：

1. **BulletTrade验证失败**: 参数映射问题导致完整回测未执行
2. **简化版回测偏差**: 抽样随机性、缺少真实持仓路径、交易成本等
3. **非真正递归**: 当前只是单轮网格搜索，未实现粗网格→细网格的递归细化
4. **过拟合风险**: overfit_ratio显示部分组合训练/验证差距大（如2.67倍）

## 优化目标

1. **修复BulletTrade验证**: 确保最优参数能通过完整回测引擎验证
2. **实现递归优化**: 粗网格快速筛选 → 围绕最优参数细化网格
3. **改进简化回测**: 增加样本量、模拟持仓路径、考虑交易成本
4. **过拟合检测**: 自动筛选和剔除过拟合严重的参数组合

---

## Phase 1: 修复和完善BulletTrade验证 (1-2小时)

### 1.1 修复参数映射问题

**问题**: `run_bullettrade_backtest()` 中参数映射不完整，导致BulletTrade验证失败

**修复**:

- 检查 `StrategyConfig` 支持的所有参数
- 完善参数映射逻辑
- 添加参数验证和错误处理

**文件**: `scripts/run_bull_market_optimization.py`

### 1.2 增强BulletTrade验证

**改进**:

- 在网格搜索完成后，对Top 5参数组合都进行BulletTrade验证
- 对比简化版回测和BulletTrade回测结果，分析偏差
- 输出验证报告（包含偏差分析）

**输出**: `output/bull_market_optimization/validation_report_{timestamp}.md`

---

## Phase 2: 实现递归优化框架 (2-3小时)

### 2.1 递归优化设计

**核心思路**: 粗网格快速筛选 → 围绕最优参数细化网格 → 迭代优化

```python
def recursive_grid_search(
    jq_client,
    train_periods,
    validate_period,
    initial_param_grid,  # 粗网格
    universe,
    max_iterations=3,    # 最大递归次数
    refinement_ratio=0.5  # 每次细化范围缩小50%
) -> Tuple[BullMarketStrategyParams, List[Dict]]:
    """递归网格搜索"""
    current_grid = initial_param_grid
    best_params = None
    
    for iteration in range(max_iterations):
        # 1. 当前网格搜索
        best_params, history = grid_search_optimize(...)
        
        # 2. 围绕最优参数细化网格
        current_grid = refine_param_grid(best_params, current_grid, refinement_ratio)
        
        # 3. 检查是否收敛（最优参数变化小于阈值）
        if converged:
            break
```

### 2.2 网格细化函数

```python
def refine_param_grid(
    best_params: BullMarketStrategyParams,
    current_grid: Dict[str, List],
    refinement_ratio: float = 0.5
) -> Dict[str, List]:
    """围绕最优参数细化网格"""
    refined_grid = {}
    
    for param_name, param_value in asdict(best_params).items():
        if param_name not in current_grid:
            continue
        
        current_range = current_grid[param_name]
        center = param_value
        
        # 计算细化范围
        range_size = (max(current_range) - min(current_range)) * refinement_ratio
        new_min = max(center - range_size/2, min(current_range))
        new_max = min(center + range_size/2, max(current_range))
        
        # 生成新的参数值列表（保持相同数量）
        n_values = len(current_range)
        if isinstance(param_value, int):
            refined_grid[param_name] = list(np.linspace(new_min, new_max, n_values).astype(int))
        else:
            refined_grid[param_name] = list(np.linspace(new_min, new_max, n_values))
    
    return refined_grid
```

**文件**: `scripts/run_bull_market_optimization.py` (新增函数)

### 2.3 收敛检测

```python
def check_convergence(
    prev_best: Optional[BullMarketStrategyParams],
    current_best: BullMarketStrategyParams,
    threshold: float = 0.05  # 5%变化阈值
) -> bool:
    """检测是否收敛"""
    if prev_best is None:
        return False
    
    for param_name in asdict(current_best):
        prev_val = getattr(prev_best, param_name)
        curr_val = getattr(current_best, param_name)
        
        if isinstance(curr_val, (int, float)) and prev_val != 0:
            change_ratio = abs(curr_val - prev_val) / abs(prev_val)
            if change_ratio > threshold:
                return False
    
    return True
```

---

## Phase 3: 改进简化版回测准确性 (2-3小时)

### 3.1 增加样本量

**当前问题**: 只采样30只股票、3个调仓日，导致评估方差大

**改进**:

- 增加股票采样数: 30 → 80
- 增加调仓日采样: 3 → 10（均匀分布）
- 添加随机种子，确保可复现

### 3.2 模拟持仓路径

**当前问题**: 只计算信号收益，缺少持仓路径

**改进**:

- 维护模拟持仓字典
- 实现资金分配逻辑（等权或按得分加权）
- 跟踪持仓成本、盈亏

### 3.3 考虑交易成本

**改进**:

- 添加佣金计算（万分之一）
- 添加印花税（卖出时千分之一）
- 在收益计算中扣除交易成本

**文件**: `scripts/run_bull_market_optimization.py` (修改 `run_simplified_backtest()`)

---

## Phase 4: 添加过拟合检测机制 (1-2小时)

### 4.1 过拟合筛选

**在网格搜索中**:

```python
# 计算过拟合比率
overfit_ratio = train_score / (validate_score + 1e-6)

# 筛选条件
if overfit_ratio > 2.0:  # 训练是验证的2倍以上
    # 降低该组合的评分（惩罚过拟合）
    score = validate_score * (1 - (overfit_ratio - 1) * 0.3)
```

### 4.2 过拟合报告

**输出内容**:

- 过拟合严重的前10个组合
- 训练/验证差异分析
- 建议的参数范围调整

**文件**: `scripts/run_bull_market_optimization.py` (新增函数)

---

## Phase 5: 集成测试和文档 (1小时)

### 5.1 端到端测试

- 测试递归优化流程（2-3轮）
- 验证BulletTrade完整回测
- 对比改进前后的结果

### 5.2 更新文档

- 更新算法说明文档
- 添加使用示例
- 记录最佳实践

**文件**: `docs/optimization/RECURSIVE_OPTIMIZATION_GUIDE.md`

---

## 加速技术集成

**已有加速模块**（直接复用）:

| 模块 | 功能 | 文件 |

|------|------|------|

| DataPreloader | 并行数据下载+MongoDB/Parquet缓存 | `core/advisor_v4/data_preloader.py` |

| GPUTechnicalIndicatorCalculator | GPU批量计算技术指标 | `core/advisor_v4/gpu_accelerator.py` |

| ParallelBacktestRunner | 并行回测执行 | `core/advisor_v4/parallel_backtest_runner.py` |

| RecursiveBacktestEngine | 递归回测引擎 | `core/bullettrade/recursive_backtest_engine.py` |

**加速策略**:

1. **数据预加载**: 回测前调用 `DataPreloader.preload_market_data()` 缓存数据
2. **GPU批量计算**: 使用 `batch_calculate_technical_indicators()` 计算因子
3. **并行参数评估**: 使用 `ThreadPoolExecutor` 并行评估多个参数组合
4. **缓存复用**: 同一数据集只下载一次，多轮优化复用缓存

---

## 预期改进效果

| 改进项 | 预期效果 |

|--------|----------|

| BulletTrade验证 | 100%成功率，结果可复现 |

| 递归优化 | 参数精度提升20-30% |

| 简化回测准确性 | 与BulletTrade结果偏差<15% |

| 过拟合检测 | 自动剔除过拟合组合，提升泛化能力 |

| **加速效果** | **优化速度提升3-5倍** |

---

## 文件清单

**修改文件**:

- `scripts/run_bull_market_optimization.py` (主要修改)

**新增文件**:

- `scripts/recursive_optimizer.py` (递归优化核心逻辑，可选)
- `docs/optimization/RECURSIVE_OPTIMIZATION_GUIDE.md` (文档)

**输出文件**:

- `output/bull_market_optimization/validation_report_*.md` (验证报告)
- `output/bull_market_optimization/recursive_optimization_history_*.csv` (递归优化历史)