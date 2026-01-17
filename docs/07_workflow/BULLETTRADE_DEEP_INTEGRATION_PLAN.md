# BulletTrade深度集成计划

> **当前状态**: BulletTrade已基础集成（命令行调用）
> **目标**: 实现深度集成（Python API + 工作流自动化）

---

## 📊 当前集成状态

### ✅ 已实现
1. **命令行集成**
   - 通过 `bullet-trade backtest` 命令执行回测
   - 策略文件存储在 `strategies/bullettrade/`
   - 回测结果保存在 `backtest_results/`

2. **策略兼容性**
   - 支持聚宽API风格策略（`from jqdata import *`）
   - 策略转换器（BulletTrade → PTrade）

3. **配置管理**
   - `.env` 文件配置JQData账号
   - 回测参数通过命令行传递

### ❌ 未实现（深度集成目标）

---

## 🎯 深度集成的具体内容

### 1. Python API集成（而非命令行）

**当前方式**:
```bash
bullet-trade backtest strategies/bullettrade/my_strategy.py \
  --start 2024-01-01 --end 2024-12-31 \
  --cash 1000000
```

**深度集成后**:
```python
from core.bullettrade import BulletTradeEngine, BTConfig

# 创建配置
config = BTConfig(
    start_date="2024-01-01",
    end_date="2024-12-31",
    initial_capital=1000000,
    commission_rate=0.0003,
    data_provider="jqdata"
)

# 创建引擎
engine = BulletTradeEngine(config)

# 执行回测
result = engine.run_backtest(
    strategy_path="strategies/bullettrade/my_strategy.py"
)

# 获取结果
print(f"总收益率: {result.total_return:.2%}")
print(f"夏普比率: {result.sharpe_ratio:.2f}")
```

**需要实现**:
- `core/bullettrade/engine.py` - BulletTrade引擎封装
- `core/bullettrade/config.py` - 配置类
- `core/bullettrade/result.py` - 结果类

---

### 2. MCP服务器集成

**在 `backtest_server.py` 中直接调用BulletTrade API**:

```python
async def _handle_bullettrade_backtest(args: Dict) -> Dict:
    from core.bullettrade import BulletTradeEngine, BTConfig
    
    config = BTConfig(
        start_date=args["start_date"],
        end_date=args["end_date"],
        initial_capital=args.get("initial_capital", 1000000)
    )
    
    engine = BulletTradeEngine(config)
    result = engine.run_backtest(args["strategy_path"])
    
    return {
        "success": True,
        "metrics": {
            "total_return": result.total_return,
            "sharpe_ratio": result.sharpe_ratio,
            "max_drawdown": result.max_drawdown
        },
        "report_path": result.report_path
    }
```

**新增工具**:
- `backtest.bullettrade` - 使用BulletTrade引擎回测
- `backtest.bullettrade_compare` - BulletTrade批量对比
- `backtest.bullettrade_optimize` - BulletTrade参数优化

---

### 3. 工作流自动化集成

**8步骤工作流中自动使用BulletTrade**:

```python
# 在 workflow_orchestrator.py 中
def step_6_backtest(self, strategy_code: str):
    """步骤6: 回测验证"""
    # 自动使用BulletTrade回测
    from core.bullettrade import BulletTradeEngine, BTConfig
    
    config = BTConfig(
        start_date=self.start_date,
        end_date=self.end_date,
        data_provider="jqdata"
    )
    
    engine = BulletTradeEngine(config)
    result = engine.run_backtest(strategy_code)
    
    # 自动保存结果到数据库
    self.db.backtest_results.insert_one({
        "strategy_id": self.strategy_id,
        "total_return": result.total_return,
        "sharpe_ratio": result.sharpe_ratio,
        "report_path": result.report_path,
        "timestamp": datetime.now()
    })
    
    return result
```

---

### 4. 数据源集成

**支持BulletTrade的多数据源**:

```python
# 在 unified_data_provider.py 中
class BulletTradeDataProvider:
    """BulletTrade数据提供者"""
    
    def __init__(self):
        from bullet_trade.data import DataProvider
        self.provider = DataProvider()
    
    def get_price(self, securities, start_date, end_date):
        """通过BulletTrade获取数据"""
        return self.provider.get_price(
            securities=securities,
            start_date=start_date,
            end_date=end_date
        )
```

**数据源优先级**:
1. JQData（通过BulletTrade）
2. AKShare
3. Mock数据

---

### 5. 实时回测支持

**支持实时数据回测**:

```python
# 实时回测功能
async def _handle_realtime_backtest(args: Dict):
    from core.bullettrade import BulletTradeEngine, BTConfig
    
    config = BTConfig(
        data_provider="realtime",  # 实时数据源
        broker="simulator"  # 模拟券商
    )
    
    engine = BulletTradeEngine(config)
    
    # 实时回测（逐日推进）
    for date in date_range:
        result = engine.run_daily(strategy_path, date)
        yield result
```

---

### 6. 结果自动存储和分析

**自动存储回测结果到MongoDB**:

```python
# 在 BulletTradeEngine 中
def run_backtest(self, strategy_path: str):
    result = self._execute_backtest(strategy_path)
    
    # 自动存储
    self._save_to_database(result)
    
    # 自动生成报告
    self._generate_report(result)
    
    return result

def _save_to_database(self, result):
    """保存到MongoDB"""
    from pymongo import MongoClient
    client = MongoClient("localhost", 27017)
    db = client["trquant"]
    
    db.backtest_results.insert_one({
        "strategy_path": result.strategy_path,
        "start_date": result.start_date,
        "end_date": result.end_date,
        "metrics": {
            "total_return": result.total_return,
            "sharpe_ratio": result.sharpe_ratio,
            "max_drawdown": result.max_drawdown
        },
        "daily_returns": result.daily_returns,
        "trades": result.trades,
        "timestamp": datetime.now()
    })
```

---

---

## 📋 实施计划

### 阶段1: Python API封装（2天）
- [ ] 创建 `core/bullettrade/engine.py`
- [ ] 创建 `core/bullettrade/config.py`
- [ ] 创建 `core/bullettrade/result.py`
- [ ] 测试基本回测功能

### 阶段2: MCP服务器集成（1天）
- [ ] 在 `backtest_server.py` 中添加BulletTrade工具
- [ ] 实现 `backtest.bullettrade` 工具
- [ ] 实现 `backtest.bullettrade_compare` 工具

### 阶段3: 工作流集成（1天）
- [ ] 在 `workflow_orchestrator.py` 中集成BulletTrade
- [ ] 步骤6自动使用BulletTrade回测
- [ ] 结果自动保存到数据库

### 阶段4: 数据源集成（1天）
- [ ] 创建 `BulletTradeDataProvider`
- [ ] 集成到 `unified_data_provider.py`
- [ ] 测试数据获取

---

## 🎯 预期效果

### 当前（基础集成）
- ❌ 需要手动执行命令行
- ❌ 结果需要手动查看
- ❌ 无法在MCP服务器中调用
- ❌ 无法自动化工作流

### 深度集成后
- ✅ 通过Python API直接调用
- ✅ MCP服务器可直接使用
- ✅ 工作流自动执行回测
- ✅ 结果自动存储和分析
- ✅ 支持实时回测和实盘交易

---

## 📝 总结

**"深度集成" = 从命令行调用 → Python API集成**

具体包括：
1. **Python API封装** - 直接调用BulletTrade引擎
2. **MCP服务器集成** - 在MCP工具中直接使用
3. **工作流自动化** - 8步骤工作流自动回测
4. **数据源集成** - 统一数据接口支持BulletTrade
5. **结果自动化** - 自动存储、分析、报告
6. **实盘支持** - 支持BulletTrade的实盘交易接口

**预计工时**: 5天

---

## 🎯 与QMT回测的关系

### 回测引擎选择策略

**当前阶段（聚焦信息获取 → 回测验证）**:
- **BulletTrade**: 用于聚宽风格策略回测（已集成，需深度集成）
- **QMT**: 用于QMT平台策略回测（待设计）

**回测引擎对比**:

| 特性 | BulletTrade | QMT |
|------|-------------|-----|
| **策略格式** | 聚宽风格（`from jqdata import *`） | QMT原生格式 |
| **数据源** | JQData/AKShare | QMT数据源 |
| **使用场景** | 策略研究和开发 | QMT平台部署前验证 |
| **集成状态** | ✅ 已集成（需深度集成） | ⏳ 待设计 |

**工作流中的使用**:
1. **策略生成**: 生成聚宽风格策略 → 使用BulletTrade回测
2. **策略转换**: 转换为QMT格式 → 使用QMT回测验证
3. **结果对比**: 对比两个平台的回测结果

**注意**: 实盘交易功能放到项目最后阶段开发

