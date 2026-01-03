# 十倍股综合策略

## 策略概述

基于TRQuant十倍股框架开发的综合量化策略，整合所有数据源、聚宽因子库和风控模块。

## 策略特点

1. **数据源整合**
   - JQData：财务数据、行情数据、因子数据
   - AKShare：实时行情、另类数据
   - MongoDB：十倍股评估结果、历史数据

2. **聚宽因子库**
   - CNE5风格因子：size, beta, momentum, reversal, volatility
   - CNE6风格因子pro：size, beta, momentum, reversal, volatility, growth, earnings_yield
   - 聚宽因子库：通过FactorPoolIntegration获取

3. **十倍股评估**
   - 7维度综合评估体系
   - 阶段评估（S0-S5）
   - 评分卡评估
   - 成长性、行业地位、另类数据、动量、风险评估

4. **增强风控**
   - 止损：亏损超过8%自动止损
   - 止盈：盈利超过30%自动止盈
   - 移动止损：盈利超过10%后，从高点回撤5%触发
   - 仓位管理：总仓位上限90%，单票上限10%

## 文件结构

```
strategies/
├── tenbagger_comprehensive_strategy.py  # 策略主文件
└── README_TENBAGGER_STRATEGY.md         # 说明文档

scripts/
├── backtest_tenbagger_strategy.py       # 回测脚本
└── generate_tenbagger_strategy_report.py # 报告生成器
```

## 使用方法

### 1. 聚宽平台运行

策略代码是为聚宽平台设计的，可以直接在聚宽平台上运行：

1. 登录聚宽平台
2. 创建新策略
3. 复制 `tenbagger_comprehensive_strategy.py` 的内容
4. 设置回测参数并运行

### 2. 本地回测（需要适配）

如果需要本地回测，需要：
1. 适配聚宽API到本地回测引擎
2. 或使用聚宽SDK进行回测

### 3. 生成报告

即使没有实际回测结果，也可以生成报告展示：

```bash
python scripts/generate_tenbagger_strategy_report.py
```

## 策略参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_total_position | 0.90 | 总仓位上限 |
| single_stock_max | 0.10 | 单票上限 |
| stop_loss | -0.08 | 止损比例 |
| take_profit | 0.30 | 止盈比例 |
| trailing_stop | 0.05 | 移动止损回撤 |
| rebalance_frequency | 5 | 调仓频率（交易日） |
| min_tenbagger_score | 65 | 最低十倍股评分 |
| min_eval_level | 'A' | 最低评估等级 |

## 代码位置说明

所有关键函数都在代码中标注了位置，格式为：
```python
# 代码位置: strategies/tenbagger_comprehensive_strategy.py:function_name()
```

## 报告内容

生成的HTML报告包括：
1. **策略设计**：mermaid流程图展示策略逻辑
2. **代码实现**：完整策略代码（prism高亮）
3. **回测结果**：收益、风险、交易统计等指标
4. **结果分析**：详细的策略表现分析

## 注意事项

1. 策略需要JQData账号认证
2. 需要MongoDB连接（用于十倍股数据）
3. 部分功能需要特色数据权限
4. 建议在聚宽平台上运行以获得最佳体验




## 策略概述

基于TRQuant十倍股框架开发的综合量化策略，整合所有数据源、聚宽因子库和风控模块。

## 策略特点

1. **数据源整合**
   - JQData：财务数据、行情数据、因子数据
   - AKShare：实时行情、另类数据
   - MongoDB：十倍股评估结果、历史数据

2. **聚宽因子库**
   - CNE5风格因子：size, beta, momentum, reversal, volatility
   - CNE6风格因子pro：size, beta, momentum, reversal, volatility, growth, earnings_yield
   - 聚宽因子库：通过FactorPoolIntegration获取

3. **十倍股评估**
   - 7维度综合评估体系
   - 阶段评估（S0-S5）
   - 评分卡评估
   - 成长性、行业地位、另类数据、动量、风险评估

4. **增强风控**
   - 止损：亏损超过8%自动止损
   - 止盈：盈利超过30%自动止盈
   - 移动止损：盈利超过10%后，从高点回撤5%触发
   - 仓位管理：总仓位上限90%，单票上限10%

## 文件结构

```
strategies/
├── tenbagger_comprehensive_strategy.py  # 策略主文件
└── README_TENBAGGER_STRATEGY.md         # 说明文档

scripts/
├── backtest_tenbagger_strategy.py       # 回测脚本
└── generate_tenbagger_strategy_report.py # 报告生成器
```

## 使用方法

### 1. 聚宽平台运行

策略代码是为聚宽平台设计的，可以直接在聚宽平台上运行：

1. 登录聚宽平台
2. 创建新策略
3. 复制 `tenbagger_comprehensive_strategy.py` 的内容
4. 设置回测参数并运行

### 2. 本地回测（需要适配）

如果需要本地回测，需要：
1. 适配聚宽API到本地回测引擎
2. 或使用聚宽SDK进行回测

### 3. 生成报告

即使没有实际回测结果，也可以生成报告展示：

```bash
python scripts/generate_tenbagger_strategy_report.py
```

## 策略参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_total_position | 0.90 | 总仓位上限 |
| single_stock_max | 0.10 | 单票上限 |
| stop_loss | -0.08 | 止损比例 |
| take_profit | 0.30 | 止盈比例 |
| trailing_stop | 0.05 | 移动止损回撤 |
| rebalance_frequency | 5 | 调仓频率（交易日） |
| min_tenbagger_score | 65 | 最低十倍股评分 |
| min_eval_level | 'A' | 最低评估等级 |

## 代码位置说明

所有关键函数都在代码中标注了位置，格式为：
```python
# 代码位置: strategies/tenbagger_comprehensive_strategy.py:function_name()
```

## 报告内容

生成的HTML报告包括：
1. **策略设计**：mermaid流程图展示策略逻辑
2. **代码实现**：完整策略代码（prism高亮）
3. **回测结果**：收益、风险、交易统计等指标
4. **结果分析**：详细的策略表现分析

## 注意事项

1. 策略需要JQData账号认证
2. 需要MongoDB连接（用于十倍股数据）
3. 部分功能需要特色数据权限
4. 建议在聚宽平台上运行以获得最佳体验























## 策略概述

基于TRQuant十倍股框架开发的综合量化策略，整合所有数据源、聚宽因子库和风控模块。

## 策略特点

1. **数据源整合**
   - JQData：财务数据、行情数据、因子数据
   - AKShare：实时行情、另类数据
   - MongoDB：十倍股评估结果、历史数据

2. **聚宽因子库**
   - CNE5风格因子：size, beta, momentum, reversal, volatility
   - CNE6风格因子pro：size, beta, momentum, reversal, volatility, growth, earnings_yield
   - 聚宽因子库：通过FactorPoolIntegration获取

3. **十倍股评估**
   - 7维度综合评估体系
   - 阶段评估（S0-S5）
   - 评分卡评估
   - 成长性、行业地位、另类数据、动量、风险评估

4. **增强风控**
   - 止损：亏损超过8%自动止损
   - 止盈：盈利超过30%自动止盈
   - 移动止损：盈利超过10%后，从高点回撤5%触发
   - 仓位管理：总仓位上限90%，单票上限10%

## 文件结构

```
strategies/
├── tenbagger_comprehensive_strategy.py  # 策略主文件
└── README_TENBAGGER_STRATEGY.md         # 说明文档

scripts/
├── backtest_tenbagger_strategy.py       # 回测脚本
└── generate_tenbagger_strategy_report.py # 报告生成器
```

## 使用方法

### 1. 聚宽平台运行

策略代码是为聚宽平台设计的，可以直接在聚宽平台上运行：

1. 登录聚宽平台
2. 创建新策略
3. 复制 `tenbagger_comprehensive_strategy.py` 的内容
4. 设置回测参数并运行

### 2. 本地回测（需要适配）

如果需要本地回测，需要：
1. 适配聚宽API到本地回测引擎
2. 或使用聚宽SDK进行回测

### 3. 生成报告

即使没有实际回测结果，也可以生成报告展示：

```bash
python scripts/generate_tenbagger_strategy_report.py
```

## 策略参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_total_position | 0.90 | 总仓位上限 |
| single_stock_max | 0.10 | 单票上限 |
| stop_loss | -0.08 | 止损比例 |
| take_profit | 0.30 | 止盈比例 |
| trailing_stop | 0.05 | 移动止损回撤 |
| rebalance_frequency | 5 | 调仓频率（交易日） |
| min_tenbagger_score | 65 | 最低十倍股评分 |
| min_eval_level | 'A' | 最低评估等级 |

## 代码位置说明

所有关键函数都在代码中标注了位置，格式为：
```python
# 代码位置: strategies/tenbagger_comprehensive_strategy.py:function_name()
```

## 报告内容

生成的HTML报告包括：
1. **策略设计**：mermaid流程图展示策略逻辑
2. **代码实现**：完整策略代码（prism高亮）
3. **回测结果**：收益、风险、交易统计等指标
4. **结果分析**：详细的策略表现分析

## 注意事项

1. 策略需要JQData账号认证
2. 需要MongoDB连接（用于十倍股数据）
3. 部分功能需要特色数据权限
4. 建议在聚宽平台上运行以获得最佳体验




## 策略概述

基于TRQuant十倍股框架开发的综合量化策略，整合所有数据源、聚宽因子库和风控模块。

## 策略特点

1. **数据源整合**
   - JQData：财务数据、行情数据、因子数据
   - AKShare：实时行情、另类数据
   - MongoDB：十倍股评估结果、历史数据

2. **聚宽因子库**
   - CNE5风格因子：size, beta, momentum, reversal, volatility
   - CNE6风格因子pro：size, beta, momentum, reversal, volatility, growth, earnings_yield
   - 聚宽因子库：通过FactorPoolIntegration获取

3. **十倍股评估**
   - 7维度综合评估体系
   - 阶段评估（S0-S5）
   - 评分卡评估
   - 成长性、行业地位、另类数据、动量、风险评估

4. **增强风控**
   - 止损：亏损超过8%自动止损
   - 止盈：盈利超过30%自动止盈
   - 移动止损：盈利超过10%后，从高点回撤5%触发
   - 仓位管理：总仓位上限90%，单票上限10%

## 文件结构

```
strategies/
├── tenbagger_comprehensive_strategy.py  # 策略主文件
└── README_TENBAGGER_STRATEGY.md         # 说明文档

scripts/
├── backtest_tenbagger_strategy.py       # 回测脚本
└── generate_tenbagger_strategy_report.py # 报告生成器
```

## 使用方法

### 1. 聚宽平台运行

策略代码是为聚宽平台设计的，可以直接在聚宽平台上运行：

1. 登录聚宽平台
2. 创建新策略
3. 复制 `tenbagger_comprehensive_strategy.py` 的内容
4. 设置回测参数并运行

### 2. 本地回测（需要适配）

如果需要本地回测，需要：
1. 适配聚宽API到本地回测引擎
2. 或使用聚宽SDK进行回测

### 3. 生成报告

即使没有实际回测结果，也可以生成报告展示：

```bash
python scripts/generate_tenbagger_strategy_report.py
```

## 策略参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_total_position | 0.90 | 总仓位上限 |
| single_stock_max | 0.10 | 单票上限 |
| stop_loss | -0.08 | 止损比例 |
| take_profit | 0.30 | 止盈比例 |
| trailing_stop | 0.05 | 移动止损回撤 |
| rebalance_frequency | 5 | 调仓频率（交易日） |
| min_tenbagger_score | 65 | 最低十倍股评分 |
| min_eval_level | 'A' | 最低评估等级 |

## 代码位置说明

所有关键函数都在代码中标注了位置，格式为：
```python
# 代码位置: strategies/tenbagger_comprehensive_strategy.py:function_name()
```

## 报告内容

生成的HTML报告包括：
1. **策略设计**：mermaid流程图展示策略逻辑
2. **代码实现**：完整策略代码（prism高亮）
3. **回测结果**：收益、风险、交易统计等指标
4. **结果分析**：详细的策略表现分析

## 注意事项

1. 策略需要JQData账号认证
2. 需要MongoDB连接（用于十倍股数据）
3. 部分功能需要特色数据权限
4. 建议在聚宽平台上运行以获得最佳体验









































