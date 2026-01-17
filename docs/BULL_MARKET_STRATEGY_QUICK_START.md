# 牛市策略系统 - 快速启动指南

> **目标**: 月回报率30%的BulletTrade策略  
> **状态**: ✅ 系统已完全实现，可以立即使用

---

## 🚀 最快启动方式

### 方式1: 执行完整工作流（一键运行）

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
python -m core.workflow.bull_market_strategy_workflow
```

或者使用Python脚本：

```python
from core.workflow.bull_market_strategy_workflow import BullMarketStrategyWorkflow, WorkflowConfig

config = WorkflowConfig(
    backtest_start_date='2024-10-01',
    backtest_end_date='2024-12-31',
    evolution_population_size=30,  # 快速测试用小种群
    evolution_generations=5,       # 快速测试用少代数
)

workflow = BullMarketStrategyWorkflow(config=config, verbose=True)
result = workflow.execute(skip_mining=True, skip_evolution=False)

print(f"结果: 是否达标={result.reached_target}, 最佳月收益率={result.best_backtest_result['monthly_return']*100:.2f}%")
```

### 方式2: 分步骤执行

#### 步骤1: 检测市场状态（必须）
```python
from core.market_regime.bull_market_signal_aggregator import BullMarketSignalAggregator

aggregator = BullMarketSignalAggregator(verbose=True)
signal = aggregator.aggregate()

if signal.bull_probability < 30:
    print("⚠️ 非牛市，不建议执行策略")
    exit(0)

print(f"✅ 牛市概率: {signal.bull_probability:.1f}%, 强度: {signal.strength_level}")
```

#### 步骤2: 执行进化优化（推荐）
```python
from core.evolution.evolution_controller import EvolutionController
from core.evolution.bull_market_strategy_evolver import EvolutionConfig
from core.bullettrade.recursive_backtest_engine import BacktestConfig

backtest_config = BacktestConfig(
    start_date='2024-10-01',
    end_date='2024-12-31',
    initial_capital=1000000.0
)

evolution_config = EvolutionConfig(
    population_size=50,
    generations=10,
    target_monthly_return=0.30,
)

controller = EvolutionController(
    backtest_config=backtest_config,
    evolution_config=evolution_config,
    verbose=True
)

result = controller.run_evolution()
print(f"最佳月收益率: {result.best_individual.backtest_result.monthly_return*100:.2f}%")
```

---

## 📋 核心模块使用

### 1. 市场状态检测

```python
from core.market_regime.bull_market_detector import BullMarketDetector

detector = BullMarketDetector(benchmark='000300.XSHG', verbose=True)
result = detector.detect(date='2025-01-10')

print(f"是否为牛市: {result.is_bull}")
print(f"强度等级: {result.strength.value}")
print(f"强度得分: {result.strength_score:.1f}/100")
print(f"仓位建议: {result.position_suggestion*100:.0f}%")
```

### 2. 数据挖掘

```python
from core.data_mining.bull_market_high_return_miner import BullMarketHighReturnMiner

miner = BullMarketHighReturnMiner(min_return_pct=10.0, verbose=True)
cases = miner.mine_high_return_cases(
    start_date='2024-09-01',
    end_date='2025-09-13',
    min_bull_score=60.0
)

miner.save_to_csv(cases, 'output/bull_cases.csv')
print(f"找到 {len(cases)} 个高回报案例")
```

### 3. 模式提取

```python
from core.pattern_recognition.bull_market_pattern_extractor import BullMarketPatternExtractor

extractor = BullMarketPatternExtractor(n_clusters=4, verbose=True)
patterns = extractor.extract_patterns(cases_df)  # cases_df来自CSV

extractor.save_patterns(patterns, 'output/bull_patterns.json')
print(f"提取 {len(patterns)} 个模式")
```

### 4. 策略生成

```python
from core.advisor_v4.bullettrade_strategy_generator import BulletTradeStrategyGenerator, StrategyConfig

config = StrategyConfig()
config.max_stocks = 12
config.min_total_score = 30.0

generator = BulletTradeStrategyGenerator(config=config)
strategy_code = generator.generate_strategy_code()

# 保存策略代码
with open('output/strategy.py', 'w', encoding='utf-8') as f:
    f.write(strategy_code)
```

### 5. 回测执行

```python
from core.bullettrade.recursive_backtest_engine import RecursiveBacktestEngine, BacktestConfig

backtest_config = BacktestConfig(
    start_date='2024-10-01',
    end_date='2024-12-31',
    initial_capital=1000000.0
)

engine = RecursiveBacktestEngine(backtest_config, verbose=True)
result = engine.run_backtest(
    strategy_params={
        'max_stocks': 10,
        'min_total_score': 30.0,
        'rebalance_days': 5,
    }
)

print(f"月收益率: {result.monthly_return*100:.2f}%")
print(f"是否达标: {result.meets_target()}")
```

---

## 🎯 关键配置参数

### 回测配置
```python
BacktestConfig(
    start_date='2024-10-01',      # 回测开始日期
    end_date='2024-12-31',        # 回测结束日期
    initial_capital=1000000.0,    # 初始资金（100万）
    benchmark='000300.XSHG',      # 基准指数（沪深300）
)
```

### 进化配置
```python
EvolutionConfig(
    population_size=50,            # 种群大小（建议30-100）
    generations=10,                # 进化代数（建议5-20）
    target_monthly_return=0.30,    # 目标月回报率（30%）
    max_drawdown_limit=-0.20,      # 最大回撤限制（-20%）
    min_sharpe_ratio=2.0,          # 最小夏普比率
    elite_ratio=0.1,               # 精英比例（10%）
    crossover_rate=0.7,            # 交叉率（70%）
    mutation_rate=0.3,             # 变异率（30%）
)
```

### 工作流配置
```python
WorkflowConfig(
    mining_start_date='2024-09-01',     # 数据挖掘开始日期
    mining_end_date='2025-09-13',       # 数据挖掘结束日期
    backtest_start_date='2024-10-01',   # 回测开始日期
    backtest_end_date='2024-12-31',     # 回测结束日期
    evolution_population_size=50,       # 进化种群大小
    evolution_generations=10,           # 进化代数
    target_monthly_return=0.30,         # 目标月回报率
)
```

---

## ⚙️ 环境要求

### Python包依赖
```bash
pip install pandas numpy scikit-learn jqdatasdk
```

### 配置文件
- JQData配置: `config/jqdata_config.json` 或环境变量
- BulletTrade: 需要安装BulletTrade引擎

### 数据目录
```bash
mkdir -p output/evolution output/backtest_cache data
```

---

## 📊 输出文件

### 数据文件
- `data/bull_market_high_return_cases.csv` - 高回报案例数据
- `data/bull_market_patterns.json` - 提取的模式数据

### 回测结果
- `output/evolution/{run_id}_result.json` - 进化结果
- `output/recursive_backtest_results.json` - 回测结果汇总

### 工作流结果
- `output/bull_market_strategy/{workflow_id}_result.json` - 工作流执行结果

### 知识库
- `.trquant/dev/knowledge/knowledge_base.json` - 知识库主文件

---

## 🔧 故障排除

### 问题1: JQData连接失败
```python
# 检查配置文件
from config.config_manager import get_config_manager
config = get_config_manager().get_config('jqdata')
print(f"JQData配置: {config}")
```

### 问题2: BulletTrade引擎不可用
```bash
# 检查BulletTrade安装
python -c "import bullettrade; print('✅ BulletTrade可用')"
```

### 问题3: 进化优化太慢
```python
# 使用小种群快速测试
evolution_config = EvolutionConfig(
    population_size=10,  # 小种群
    generations=3,       # 少代数
)
```

### 问题4: 内存不足
```python
# 减少股票池大小
miner = BullMarketHighReturnMiner(min_return_pct=10.0)
cases = miner.mine_high_return_cases(
    universe=universe[:500]  # 限制股票池大小
)
```

---

## 📞 支持

- **完整文档**: `docs/BULL_MARKET_STRATEGY_COMPLETE_IMPLEMENTATION.md`
- **实施状态**: `docs/BULL_MARKET_STRATEGY_IMPLEMENTATION_STATUS.md`
- **标准流程**: `docs/kb/STANDARD_DEVELOPMENT_WORKFLOW.md`

---

**系统已就绪，可以开始使用！** 🎉
