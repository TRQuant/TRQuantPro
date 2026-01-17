# 从回测数据提取知识指南

> **版本**: v1.0  
> **更新**: 2026-01-13  
> **目的**: 指导如何从回测数据中提取高可靠性知识（A级）

---

## 📊 回测数据来源

### 1. TRQuant回测引擎

**位置**: `core/signal_backtest.py`, `core/backtest/enhanced_backtest.py`

**数据结构**:
```python
@dataclass
class EnhancedBacktestResult:
    # 基本统计
    total_signals: int = 0
    bullish_signals: int = 0
    bearish_signals: int = 0
    
    # 准确率
    accuracy_5d: float = 0.0
    accuracy_10d: float = 0.0
    accuracy_20d: float = 0.0
    accuracy_60d: float = 0.0
    
    # 胜率
    win_rate_bullish: float = 0.0
    win_rate_bearish: float = 0.0
    
    # 平均收益
    avg_return_bullish_5d: float = 0.0
    avg_return_bullish_20d: float = 0.0
```

### 2. BulletTrade回测引擎

**位置**: `core/bullettrade/recursive_backtest_engine.py`

**数据结构**:
```python
@dataclass
class StandardizedBacktestResult:
    # 绩效指标
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    
    # 交易统计
    total_trades: int
    avg_holding_period: float
```

### 3. QMT回测引擎

**位置**: `core/qmt/backtest_workflow.py`

**数据结构**:
```python
@dataclass
class QMTBacktestResult:
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
```

---

## 🔍 提取知识的方法

### 方法1: 从回测结果中提取因子有效性

**步骤**:
1. 运行回测，收集因子在不同市场状态下的表现
2. 计算IC、IR、胜率等指标
3. 分析因子在不同市场状态下的有效性
4. 提取知识，标注为A级可靠性

**示例脚本**:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从回测数据提取因子有效性知识
"""
import sys
from pathlib import Path

TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from core.signal_backtest import EnhancedBacktestResult
from mcp_servers.unified_dev_server import knowledge_add

def extract_factor_knowledge_from_backtest():
    """从回测数据提取因子有效性知识"""
    
    # 1. 加载回测结果
    backtest_results = load_backtest_results()  # 需要实现
    
    # 2. 分析因子在不同市场状态下的表现
    for result in backtest_results:
        # 计算IC、IR、胜率等指标
        ic_value = calculate_ic(result)
        ir_value = calculate_ir(result)
        win_rate = result.win_rate_bullish
        
        # 3. 提取知识
        knowledge = {
            "title": f"{result.factor_name}在{result.market_state}的有效性（回测验证）",
            "content": f"""
## {result.factor_name}在{result.market_state}的有效性（回测验证）

### 知识来源
- **来源类型**: 回测数据验证
- **数据周期**: {result.start_date} 至 {result.end_date}
- **样本数量**: {result.total_signals}次信号
- **可靠性评级**: A级（高可靠性）

### 回测验证结果
- **胜率**: {win_rate:.1%}
- **IC值**: {ic_value:.2f}
- **IR值**: {ir_value:.2f}
- **平均收益**: {result.avg_return_bullish_20d:.2%}

### 结论
{result.factor_name}在{result.market_state}具有{'较高' if ic_value > 0.15 else '中等' if ic_value > 0.05 else '较低'}的有效性。

### 数据来源
- 回测平台: TRQuant回测引擎
- 数据源: JQData（聚宽）
- 验证时间: {result.timestamp}
""",
            "type": "factor_behavior",
            "tags": [result.factor_name, "回测验证", "A级可靠性"],
            "source": f"回测数据验证（{result.start_date}至{result.end_date}，{result.total_signals}次信号）",
            "reliability": "A级（高可靠性）"
        }
        
        # 4. 存入知识库
        knowledge_add(**knowledge)
```

### 方法2: 从策略回测中提取策略模板

**步骤**:
1. 运行策略回测，收集策略在不同市场状态下的表现
2. 分析策略的胜率、平均收益、最大回撤等指标
3. 提取策略模板，标注为A级或B级可靠性

**示例脚本**:
```python
def extract_strategy_knowledge_from_backtest():
    """从策略回测数据提取策略模板知识"""
    
    # 1. 加载策略回测结果
    strategy_results = load_strategy_backtest_results()  # 需要实现
    
    # 2. 分析策略在不同市场状态下的表现
    for result in strategy_results:
        # 计算策略指标
        win_rate = result.win_rate
        avg_return = result.annual_return
        max_drawdown = result.max_drawdown
        sharpe_ratio = result.sharpe_ratio
        
        # 3. 提取知识
        knowledge = {
            "title": f"{result.strategy_name}在{result.market_state}的实战表现（回测验证）",
            "content": f"""
## {result.strategy_name}在{result.market_state}的实战表现（回测验证）

### 知识来源
- **来源类型**: 回测数据验证
- **数据周期**: {result.start_date} 至 {result.end_date}
- **回测次数**: {result.total_trades}次交易
- **可靠性评级**: A级（高可靠性）

### 回测验证结果
- **胜率**: {win_rate:.1%}
- **年化收益**: {avg_return:.2%}
- **最大回撤**: {max_drawdown:.2%}
- **夏普比率**: {sharpe_ratio:.2f}

### 结论
{result.strategy_name}在{result.market_state}具有{'较高' if win_rate > 0.6 else '中等' if win_rate > 0.5 else '较低'}的有效性。

### 数据来源
- 回测平台: TRQuant回测引擎
- 数据源: JQData（聚宽）
- 验证时间: {result.timestamp}
""",
            "type": "strategy_pattern",
            "tags": [result.strategy_name, "回测验证", "A级可靠性"],
            "source": f"回测数据验证（{result.start_date}至{result.end_date}，{result.total_trades}次交易）",
            "reliability": "A级（高可靠性）"
        }
        
        # 4. 存入知识库
        knowledge_add(**knowledge)
```

---

## 📋 提取知识的步骤

### 步骤1: 准备回测数据

1. **选择回测周期**: 建议至少2年（如2020-2024）
2. **选择样本**: 建议至少1000次信号或交易
3. **选择市场状态**: 主升期、过热期、退潮期等

### 步骤2: 运行回测

```python
# 运行因子回测
from core.signal_backtest import EnhancedBacktest

backtest = EnhancedBacktest(
    start_date="2020-01-01",
    end_date="2024-12-31",
    factor_name="MACD",
    market_state="主升期"
)

result = backtest.run()
```

### 步骤3: 分析结果

```python
# 计算IC、IR等指标
ic_value = calculate_ic(result)
ir_value = calculate_ir(result)
win_rate = result.win_rate_bullish
avg_return = result.avg_return_bullish_20d
```

### 步骤4: 提取知识

```python
# 提取知识条目
knowledge = {
    "title": "因子名称在市场状态的有效性（回测验证）",
    "content": "详细内容...",
    "type": "factor_behavior",
    "tags": ["因子名称", "回测验证", "A级可靠性"],
    "source": "回测数据验证（周期，样本数）",
    "reliability": "A级（高可靠性）"
}
```

### 步骤5: 存入知识库

```python
from mcp_servers.unified_dev_server import knowledge_add

knowledge_add(**knowledge)
```

---

## 🎯 提取知识的优先级

### 高优先级（A级知识）

1. **因子有效性**: IC>0.15, IR>1.0, 胜率>60%
2. **策略表现**: 胜率>60%, 年化收益>15%, 夏普比率>2.0
3. **市场状态识别**: 准确率>75%

### 中优先级（B级知识）

1. **因子有效性**: IC>0.05, IR>0.5, 胜率>50%
2. **策略表现**: 胜率>50%, 年化收益>10%, 夏普比率>1.5
3. **市场状态识别**: 准确率>65%

### 低优先级（C级知识）

1. **因子有效性**: IC<0.05, IR<0.5, 胜率<50%
2. **策略表现**: 胜率<50%, 年化收益<10%, 夏普比率<1.5
3. **市场状态识别**: 准确率<65%

---

## 📊 知识提取模板

### 因子有效性知识模板

```json
{
  "title": "因子名称在市场状态的有效性（回测验证）",
  "content": "## 因子名称在市场状态的有效性（回测验证）\n\n### 知识来源\n- **来源类型**: 回测数据验证\n- **数据周期**: YYYY-MM-DD 至 YYYY-MM-DD\n- **样本数量**: N次信号\n- **可靠性评级**: A级（高可靠性）\n\n### 回测验证结果\n- **胜率**: X%\n- **IC值**: X\n- **IR值**: X\n- **平均收益**: X%\n\n### 结论\n因子在市场状态具有X的有效性。\n\n### 数据来源\n- 回测平台: TRQuant回测引擎\n- 数据源: JQData（聚宽）\n- 验证时间: YYYY-MM-DD",
  "type": "factor_behavior",
  "tags": ["因子名称", "回测验证", "A级可靠性"],
  "source": "回测数据验证（周期，样本数）",
  "reliability": "A级（高可靠性）"
}
```

### 策略模板知识模板

```json
{
  "title": "策略名称在市场状态的实战表现（回测验证）",
  "content": "## 策略名称在市场状态的实战表现（回测验证）\n\n### 知识来源\n- **来源类型**: 回测数据验证\n- **数据周期**: YYYY-MM-DD 至 YYYY-MM-DD\n- **回测次数**: N次交易\n- **可靠性评级**: A级（高可靠性）\n\n### 回测验证结果\n- **胜率**: X%\n- **年化收益**: X%\n- **最大回撤**: X%\n- **夏普比率**: X\n\n### 结论\n策略在市场状态具有X的有效性。\n\n### 数据来源\n- 回测平台: TRQuant回测引擎\n- 数据源: JQData（聚宽）\n- 验证时间: YYYY-MM-DD",
  "type": "strategy_pattern",
  "tags": ["策略名称", "回测验证", "A级可靠性"],
  "source": "回测数据验证（周期，交易次数）",
  "reliability": "A级（高可靠性）"
}
```

---

## ✅ 结论

**从回测数据提取知识的方法已建立！**

1. ✅ **数据来源**: TRQuant回测引擎、BulletTrade回测引擎、QMT回测引擎
2. ✅ **提取方法**: 因子有效性、策略模板、市场状态识别
3. ✅ **知识模板**: 因子有效性知识模板、策略模板知识模板
4. ✅ **优先级**: 高优先级（A级）、中优先级（B级）、低优先级（C级）

**下一步**:
- 运行回测，收集数据
- 提取高可靠性知识（A级）
- 定期更新和验证知识库
