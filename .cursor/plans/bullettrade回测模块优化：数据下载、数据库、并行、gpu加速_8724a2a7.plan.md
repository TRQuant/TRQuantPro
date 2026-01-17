---
name: BulletTrade回测模块优化：数据下载、数据库、并行、GPU加速
overview: 优化BulletTrade回测模块，确保数据下载、数据库调取、并行处理和GPU加速功能完整集成，不跳过数据挖掘关键步骤。
todos: []
---

# BulletTrade回测模块优化计划

## 目标

优化BulletTrade回测系统，确保：

1. **数据下载**：利用 `DataPreloader` 并行下载数据到MongoDB
2. **数据库调取**：从MongoDB读取数据，避免重复API调用
3. **并行处理**：安全模式的并行回测（3个JQData连接 + 线程池）
4. **GPU加速**：因子计算使用GPU批量加速

## 当前问题分析

1. **数据下载未集成**：工作流和回测模块未使用 `DataPreloader` 和 `JQDataMongoDBStorage`
2. **数据库调取缺失**：回测时重复从JQData API获取数据，未利用MongoDB缓存
3. **并行处理不足**：`_run_initial_backtest` 和进化过程都是串行执行
4. **GPU加速未集成**：因子计算未使用 `GPUTechnicalIndicatorCalculator`
5. **数据挖掘被跳过**：`skip_mining=True` 跳过了关键的数据挖掘步骤

## 实施步骤

### 阶段1: 增强数据预加载模块（数据下载 + 数据库 + 多时间段支持）

**文件**: `core/advisor_v4/data_preloader.py`

**优化内容**:

- 确保MongoDB存储自动启用（`use_mongodb=True`）
- 添加数据完整性检查（验证已下载数据是否完整）
- 添加增量更新逻辑（只下载缺失日期范围的数据）
- 优化并行下载性能（充分利用3个JQData连接）
- 支持多时间段批量预加载（适用于3个历史牛市时间段）

**关键修改**:

```python
# 确保在初始化时启用MongoDB
def __init__(self, use_mongodb=True, ...):
    self.storage = JQDataMongoDBStorage() if use_mongodb and MONGODB_STORAGE_AVAILABLE else None
    
# 添加数据完整性检查
def check_data_completeness(self, start_date, end_date, stocks=None) -> Dict[str, Any]:
    """检查MongoDB中数据是否完整"""
    if self.storage is None:
        return {'is_complete': False, 'reason': 'MongoDB not available'}
    
    # 查询MongoDB中的数据范围
    # 返回完整性状态、缺失日期范围等
    return {
        'is_complete': True/False,
        'covered_date_range': (...),
        'missing_date_ranges': [...],
        'total_stocks': ...,
        'covered_stocks': ...
    }

# 添加多时间段批量预加载
def preload_multiple_periods(
    self,
    periods: List[Tuple[str, str]],
    force_refresh: bool = False,
    show_progress: bool = True
) -> Dict[str, PreloadResult]:
    """批量预加载多个时间段的数据"""
    results = {}
    
    for period_start, period_end in periods:
        if show_progress:
            print(f"预加载时间段: {period_start} ~ {period_end}")
        
        # 检查完整性
        completeness = self.check_data_completeness(period_start, period_end)
        
        if completeness.get('is_complete') and not force_refresh:
            if show_progress:
                print(f"  数据已完整，跳过下载")
            continue
        
        # 下载缺失的数据
        result = self.preload_market_data(
            start_date=period_start,
            end_date=period_end,
            force_refresh=force_refresh
        )
        
        results[f"{period_start}_{period_end}"] = result
    
    return results
```

### 阶段2: 优化回测引擎（集成数据库调取 + GPU加速）

**文件**: `core/bullettrade/recursive_backtest_engine.py`

**优化内容**:

- 在执行回测前，先检查并预加载数据（使用 `DataPreloader`）
- 策略生成时传递缓存目录，确保使用MongoDB数据
- 因子计算时使用 `GPUTechnicalIndicatorCalculator`（如果可用）

**关键修改**:

```python
def __init__(self, ...):
    # 初始化数据预加载器
    from core.advisor_v4.data_preloader import DataPreloader
    self.data_preloader = DataPreloader(
        use_mongodb=True,
        cache_dir=base_config.cache_dir,
        max_workers=3  # 安全模式：3个连接
    )
    
    # 初始化GPU加速器（如果可用）
    try:
        from core.advisor_v4.gpu_accelerator import GPUTechnicalIndicatorCalculator
        self.gpu_calculator = GPUTechnicalIndicatorCalculator(use_gpu=True)
    except:
        self.gpu_calculator = None

def run_backtest(self, ...):
    # 1. 预加载数据（从MongoDB或下载）
    self._ensure_data_loaded(...)
    
    # 2. 生成策略（传递GPU计算器）
    strategy_code = self._generate_strategy_code(..., gpu_calculator=self.gpu_calculator)
    
    # 3. 执行回测（使用已加载的数据）
```

### 阶段3: 优化工作流（确保数据挖掘 + 并行回测）

**文件**: `core/workflow/bull_market_strategy_workflow.py`

**优化内容**:

- 移除 `skip_mining` 参数，强制执行数据挖掘
- 数据挖掘阶段使用 `DataPreloader` 预加载数据
- 回测阶段使用 `ParallelBacktestRunner` 并行执行多个回测任务
- 进化过程中使用并行回测加速

**关键修改**:

```python
def execute(self, workflow_id, skip_mining=False, skip_evolution=False):
    # 强制执行数据挖掘（除非明确要求跳过）
    if not skip_mining:
        # 阶段2: 数据挖掘（使用DataPreloader预加载数据）
        mining_result = self._mine_high_return_cases()
        
    # 阶段5: 执行回测（使用并行回测）
    if self.config.use_parallel_backtest:
        initial_backtest_result = self._run_parallel_initial_backtest(strategy_result)
    else:
        initial_backtest_result = self._run_initial_backtest(strategy_result)
        
def _run_parallel_initial_backtest(self, strategy_result):
    """并行执行初始回测（多时间段验证）"""
    from core.advisor_v4.parallel_backtest_runner import ParallelBacktestRunner
    
    runner = ParallelBacktestRunner(
        cache_dir=self.config.cache_dir,
        use_gpu=True,  # 启用GPU加速
        max_workers=3,  # 安全模式：3个线程
        verbose=self.verbose
    )
    
    # 创建多个回测任务（不同时间段）
    periods = [
        (self.config.backtest_start_date, self.config.backtest_end_date),
        # 可以添加更多时间段用于验证
    ]
    
    summary = runner.run_parallel_backtests(periods, strategy_config=...)
    return summary.best_result.to_dict() if summary.best_result else {}
```

### 阶段4: 优化进化控制器（并行进化回测）

**文件**: `core/evolution/evolution_controller.py`

**优化内容**:

- 使用 `ParallelBacktestRunner` 并行执行每代个体的回测
- 确保数据预加载在进化开始前完成
- GPU加速因子计算集成到个体评估中

**关键修改**:

```python
def run_evolution(self, ...):
    # 1. 预加载数据（一次加载，多次使用）
    self._preload_all_data()
    
    # 2. 初始化并行回测运行器
    from core.advisor_v4.parallel_backtest_runner import ParallelBacktestRunner
    self.parallel_runner = ParallelBacktestRunner(
        cache_dir=self.cache_dir,
        use_gpu=True,
        max_workers=3,  # 安全模式
        verbose=self.verbose
    )
    
    # 3. 在评估函数中使用并行回测
    def evaluate_population_parallel(individuals):
        tasks = [创建回测任务 for each individual]
        summary = self.parallel_runner.run_parallel_backtests(tasks)
        return [提取结果 for each individual]
```

### 阶段5: 优化策略生成器（传递GPU计算器）

**文件**: `core/advisor_v4/bullettrade_strategy_generator.py`

**优化内容**:

- 接受 `gpu_calculator` 参数（可选）
- 在因子计算时使用GPU加速（如果提供）
- 确保策略代码生成时使用MongoDB缓存数据

### 阶段6: 配置文件增强 + 历史牛市时间段配置

**文件**: `core/workflow/bull_market_strategy_workflow.py` (WorkflowConfig)

**新增配置项**:

```python
@dataclass
class WorkflowConfig:
    # ... 现有配置 ...
    
    # 数据相关 - 历史牛市时间段（用于数据挖掘）
    historical_bull_market_periods: List[Tuple[str, str]] = field(default_factory=lambda: [
        # 第三次牛市（股权分置改革牛）：2005年中 - 2007年10月
        ("2005-07-01", "2007-10-31"),
        # 第四次牛市（杠杆牛）：2014年中 - 2015年6月
        ("2014-07-01", "2015-06-30"),
        # 第五次牛市（结构性牛/核心资产牛）：2019年初 - 2021年初
        ("2019-01-01", "2021-03-31"),
    ])
    
    # 数据挖掘配置
    mining_start_date: str = "2005-07-01"   # 数据挖掘开始日期（最早的历史牛市）
    mining_end_date: str = "2021-03-31"     # 数据挖掘结束日期（最新的历史牛市）
    use_mongodb: bool = True                 # 是否使用MongoDB存储
    force_refresh_data: bool = False         # 是否强制刷新数据
    
    # 并行相关
    use_parallel_backtest: bool = True       # 是否使用并行回测
    max_parallel_workers: int = 3            # 最大并行工作数（安全模式：3）
    
    # GPU相关
    use_gpu_acceleration: bool = True        # 是否使用GPU加速
    gpu_batch_size: int = 100                # GPU批处理大小
```

**优化数据挖掘阶段**:

```python
def _mine_high_return_cases(self) -> Dict[str, Any]:
    """阶段2: 挖掘历史牛市高回报案例（多个时间段）"""
    try:
        from core.data_mining.bull_market_high_return_miner import BullMarketHighReturnMiner
        
        miner = BullMarketHighReturnMiner(
            min_return_pct=self.config.min_return_pct,
            verbose=self.verbose
        )
        
        all_cases = []
        
        # 遍历所有历史牛市时间段
        for period_start, period_end in self.config.historical_bull_market_periods:
            if self.verbose:
                print(f"  挖掘时间段: {period_start} ~ {period_end}")
            
            # 预加载该时间段的数据
            self._preload_data_for_period(period_start, period_end)
            
            # 挖掘该时间段的高回报案例
            cases = miner.mine_high_return_cases(
                start_date=period_start,
                end_date=period_end,
                min_bull_score=self.config.min_bull_score
            )
            
            all_cases.extend(cases)
            
            if self.verbose:
                print(f"    找到 {len(cases)} 个高回报案例")
        
        # 保存合并后的所有案例
        csv_path = str(self.output_dir / 'bull_market_high_return_cases.csv')
        if all_cases:
            miner.save_to_csv(all_cases, csv_path)
        
        return {
            'case_count': len(all_cases),
            'csv_path': csv_path,
            'periods_processed': len(self.config.historical_bull_market_periods),
            'avg_return': sum([c.return_pct for c in all_cases]) / len(all_cases) if all_cases else 0.0,
        }
    except Exception as e:
        logger.error(f"数据挖掘失败: {e}")
        return {'case_count': 0, 'error': str(e)}

def _preload_data_for_period(self, start_date: str, end_date: str):
    """为指定时间段预加载数据"""
    from core.advisor_v4.data_preloader import DataPreloader
    
    preloader = DataPreloader(
        use_mongodb=True,
        cache_dir=self.config.cache_dir,
        max_workers=3,  # 安全模式
        verbose=self.verbose
    )
    
    # 检查数据完整性
    completeness = preloader.check_data_completeness(
        start_date=start_date,
        end_date=end_date,
        stocks=None  # 将获取所有A股
    )
    
    # 如果数据不完整，进行下载
    if not completeness.get('is_complete', False):
        if self.verbose:
            print(f"    预加载数据: {start_date} ~ {end_date}")
        
        preloader.preload_market_data(
            start_date=start_date,
            end_date=end_date,
            force_refresh=self.config.force_refresh_data
        )
```

## 数据流程优化

```
阶段1: 市场状态检测
    ↓
阶段2: 数据挖掘（强制执行，覆盖3个历史牛市）
    ├─→ 遍历历史牛市时间段：
    │   ├─→ 第三次牛市（2005-07-01 ~ 2007-10-31）
    │   ├─→ 第四次牛市（2014-07-01 ~ 2015-06-30）
    │   └─→ 第五次牛市（2019-01-01 ~ 2021-03-31）
    ├─→ 每个时间段：
    │   ├─→ DataPreloader 并行下载数据（3个JQData连接）
    │   ├─→ JQDataMongoDBStorage 保存到MongoDB
    │   ├─→ 验证数据完整性
    │   └─→ 挖掘高回报案例（周回报≥10%）
    └─→ 合并所有时间段的高回报案例
    ↓
阶段3: 模式提取
    ├─→ 从MongoDB读取数据（避免重复下载）
    └─→ GPU加速因子计算（如果可用）
    ↓
阶段4: 策略生成
    ├─→ 使用MongoDB缓存数据
    └─→ GPU加速因子计算
    ↓
阶段5: 初始回测
    ├─→ ParallelBacktestRunner 并行执行（3个线程）
    ├─→ 从MongoDB读取数据
    └─→ GPU加速因子计算
    ↓
阶段6: 进化优化
    ├─→ ParallelBacktestRunner 并行评估每代个体
    ├─→ 复用已加载的数据
    └─→ GPU加速因子计算
```

## 性能优化预期

| 优化项 | 当前 | 优化后 | 提升倍数 |

|--------|------|--------|---------|

| 数据下载 | 串行，每次重复 | 并行3连接，MongoDB缓存 | 3-5x |

| 数据读取 | 每次API调用 | MongoDB本地读取 | 10-50x |

| 因子计算 | CPU单线程 | GPU批量计算 | 10-50x |

| 回测执行 | 串行 | 并行3线程 | 2-3x |

| 总体提升 | - | - | **20-100x** |

## 实施顺序

1. **阶段1**：增强数据预加载模块（确保MongoDB集成 + 数据完整性检查）
2. **阶段2**：优化回测引擎（集成数据库调取和GPU）
3. **阶段3**：优化工作流（确保数据挖掘覆盖3个历史牛市 + 并行回测）
4. **阶段4**：优化进化控制器（并行进化回测）
5. **阶段5**：优化策略生成器（GPU加速）
6. **阶段6**：配置文件增强（添加历史牛市时间段配置）

## 验证测试

1. **数据预加载测试**：

   - 测试3个历史牛市时间段的数据下载
   - 测试MongoDB存储和读取
   - 测试数据完整性检查

2. **数据挖掘测试**：

   - 测试每个历史牛市时间段的高回报案例挖掘
   - 验证案例数量和平均回报率
   - 验证CSV输出格式

3. **GPU加速测试**：

   - 测试GPU加速因子计算
   - 验证GPU降级机制（GPU不可用时使用CPU）

4. **并行回测测试**：

   - 测试并行回测执行（3个线程）
   - 验证回测结果一致性

5. **完整工作流测试**：

   - 测试完整工作流（包含3个历史牛市数据挖掘）
   - 验证各阶段数据传递正确性

6. **性能对比测试**：

   - 对比优化前后的性能（数据下载、因子计算、回测执行）
   - 验证预期提升倍数（20-100x）

## 注意事项

1. **历史数据范围**：

   - 三次历史牛市跨度约16年（2005-2021）
   - 数据量较大，需要充分使用MongoDB缓存
   - 首次下载可能需要较长时间，建议分批下载

2. **安全模式并行**：

   - 最多3个JQData连接，避免API限制
   - 数据下载时使用3个进程并行
   - 回测执行时使用3个线程并行

3. **GPU降级**：

   - 如果GPU不可用，自动降级到CPU
   - GPU批处理大小可根据显存调整（默认100）

4. **MongoDB可用性**：

   - 如果MongoDB不可用，使用文件缓存（Parquet格式）
   - 确保MongoDB连接稳定，避免数据丢失

5. **数据完整性**：

   - 每次使用前检查数据完整性
   - 支持增量更新（只下载缺失日期范围）
   - 记录数据下载进度，支持断点续传

6. **错误处理**：

   - 所有优化都要有完善的错误处理和降级机制
   - 单个时间段数据下载失败不应影响其他时间段
   - 记录详细的错误日志，便于问题排查

7. **数据挖掘策略**：

   - 每个历史牛市时间段独立挖掘，最后合并结果
   - 使用统一的高回报标准（周回报≥10%）
   - 确保挖掘的案例具有代表性（覆盖不同行业、市值）