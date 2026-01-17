# 十倍股策略系统文档

## 系统概述

基于历史数据挖掘和多因子模型的十倍股筛选与交易策略系统。

## 核心组件

### 1. 特征挖掘系统
**文件**: `scripts/tenbagger_feature_mining.py`

功能:
- 扫描历史2-3年内涨幅超过10倍的股票
- 提取起涨点的多维度特征
- 存储到SQLite数据库

### 2. 特征数据库
**位置**: `data/tenbagger_features.db`

表结构:
- `tenbagger_stocks`: 10倍股主表
- `stock_features`: 股票特征表
- `feature_statistics`: 特征统计表

### 3. 多因子策略
**文件**: `scripts/tenbagger_multifactor_strategy.py`

因子配置 (基于历史10倍股特征分析):
| 因子类型 | 权重 | 说明 |
|---------|------|------|
| 成长因子 | 30% | 营收增长率、利润增长率 |
| 质量因子 | 25% | ROE、ROA |
| 估值因子 | 15% | PE、PB（适度估值） |
| 动量因子 | 15% | 20日/60日动量 |
| 规模因子 | 10% | 市值50-200亿最优 |
| 技术因子 | 5% | 均线多头、新高 |

### 4. 回测引擎
提供三个版本:
- V1: 基础版 `run_tenbagger_backtest_jq.py`
- V2: 优化版 `run_tenbagger_backtest_v2.py`
- V3: 超级动量版 `run_tenbagger_backtest_v3.py`
- 多因子版: `tenbagger_multifactor_strategy.py`

## 历史10倍股特征总结

基于网络搜索和数据分析:

### 行业分布
- 电力设备 (新能源)
- 医药生物
- 电子/半导体
- 软件/AI

### 关键特征
1. **市值**: 50-200亿为最佳区间
2. **ROE**: > 10%
3. **成长性**: 营收增长 > 30%
4. **PE**: 15-35倍合理区间
5. **动量**: 起涨前已有正向动量
6. **民营企业**: 占比超70%

### 典型案例 (2023-2024)
- 寒武纪 (688256): AI芯片，涨幅387%
- 正丹股份 (300641): 化工，近10倍
- 艾融软件 (830799): 软件，近10倍

## 策略参数配置

```python
# 持仓管理
max_holdings = 10        # 分散持仓
single_stock_max = 0.15  # 单票15%

# 风控参数
stop_loss = -0.10        # 止损10%
take_profit = 0.80       # 止盈80%
trailing_stop = 0.15     # 移动止损15%
rebalance_days = 10      # 每10天调仓

# 筛选阈值
min_market_cap = 20      # 最小市值20亿
max_market_cap = 500     # 最大市值500亿
min_roe = 5              # ROE > 5%
min_revenue_growth = 10  # 营收增长 > 10%
```

## 使用方法

### 1. 运行特征挖掘
```bash
cd /home/taotao/dev/QuantTest/TRQuant
python scripts/tenbagger_feature_mining.py
```

### 2. 运行多因子回测
```bash
python scripts/tenbagger_multifactor_strategy.py 2024-01-01 2025-12-20
```

### 3. 查看报告
报告生成在 `reports/` 目录下

## 风险提示

⚠️ **重要**: 
- 历史回测不代表未来收益
- 10倍股极为稀少，占比仅2%
- 追求高收益必然承担高风险
- 投资有风险，入市需谨慎

## 后续优化方向

1. **数据源扩展**: 加入另类数据（舆情、资金流向）
2. **因子增强**: 加入机器学习因子权重优化
3. **风控升级**: 动态止损、波动率调整
4. **实盘对接**: QMT/Ptrade实盘交易

---
*创建时间: 2025-12-26*
*维护者: TRQuant Team*




## 系统概述

基于历史数据挖掘和多因子模型的十倍股筛选与交易策略系统。

## 核心组件

### 1. 特征挖掘系统
**文件**: `scripts/tenbagger_feature_mining.py`

功能:
- 扫描历史2-3年内涨幅超过10倍的股票
- 提取起涨点的多维度特征
- 存储到SQLite数据库

### 2. 特征数据库
**位置**: `data/tenbagger_features.db`

表结构:
- `tenbagger_stocks`: 10倍股主表
- `stock_features`: 股票特征表
- `feature_statistics`: 特征统计表

### 3. 多因子策略
**文件**: `scripts/tenbagger_multifactor_strategy.py`

因子配置 (基于历史10倍股特征分析):
| 因子类型 | 权重 | 说明 |
|---------|------|------|
| 成长因子 | 30% | 营收增长率、利润增长率 |
| 质量因子 | 25% | ROE、ROA |
| 估值因子 | 15% | PE、PB（适度估值） |
| 动量因子 | 15% | 20日/60日动量 |
| 规模因子 | 10% | 市值50-200亿最优 |
| 技术因子 | 5% | 均线多头、新高 |

### 4. 回测引擎
提供三个版本:
- V1: 基础版 `run_tenbagger_backtest_jq.py`
- V2: 优化版 `run_tenbagger_backtest_v2.py`
- V3: 超级动量版 `run_tenbagger_backtest_v3.py`
- 多因子版: `tenbagger_multifactor_strategy.py`

## 历史10倍股特征总结

基于网络搜索和数据分析:

### 行业分布
- 电力设备 (新能源)
- 医药生物
- 电子/半导体
- 软件/AI

### 关键特征
1. **市值**: 50-200亿为最佳区间
2. **ROE**: > 10%
3. **成长性**: 营收增长 > 30%
4. **PE**: 15-35倍合理区间
5. **动量**: 起涨前已有正向动量
6. **民营企业**: 占比超70%

### 典型案例 (2023-2024)
- 寒武纪 (688256): AI芯片，涨幅387%
- 正丹股份 (300641): 化工，近10倍
- 艾融软件 (830799): 软件，近10倍

## 策略参数配置

```python
# 持仓管理
max_holdings = 10        # 分散持仓
single_stock_max = 0.15  # 单票15%

# 风控参数
stop_loss = -0.10        # 止损10%
take_profit = 0.80       # 止盈80%
trailing_stop = 0.15     # 移动止损15%
rebalance_days = 10      # 每10天调仓

# 筛选阈值
min_market_cap = 20      # 最小市值20亿
max_market_cap = 500     # 最大市值500亿
min_roe = 5              # ROE > 5%
min_revenue_growth = 10  # 营收增长 > 10%
```

## 使用方法

### 1. 运行特征挖掘
```bash
cd /home/taotao/dev/QuantTest/TRQuant
python scripts/tenbagger_feature_mining.py
```

### 2. 运行多因子回测
```bash
python scripts/tenbagger_multifactor_strategy.py 2024-01-01 2025-12-20
```

### 3. 查看报告
报告生成在 `reports/` 目录下

## 风险提示

⚠️ **重要**: 
- 历史回测不代表未来收益
- 10倍股极为稀少，占比仅2%
- 追求高收益必然承担高风险
- 投资有风险，入市需谨慎

## 后续优化方向

1. **数据源扩展**: 加入另类数据（舆情、资金流向）
2. **因子增强**: 加入机器学习因子权重优化
3. **风控升级**: 动态止损、波动率调整
4. **实盘对接**: QMT/Ptrade实盘交易

---
*创建时间: 2025-12-26*
*维护者: TRQuant Team*























## 系统概述

基于历史数据挖掘和多因子模型的十倍股筛选与交易策略系统。

## 核心组件

### 1. 特征挖掘系统
**文件**: `scripts/tenbagger_feature_mining.py`

功能:
- 扫描历史2-3年内涨幅超过10倍的股票
- 提取起涨点的多维度特征
- 存储到SQLite数据库

### 2. 特征数据库
**位置**: `data/tenbagger_features.db`

表结构:
- `tenbagger_stocks`: 10倍股主表
- `stock_features`: 股票特征表
- `feature_statistics`: 特征统计表

### 3. 多因子策略
**文件**: `scripts/tenbagger_multifactor_strategy.py`

因子配置 (基于历史10倍股特征分析):
| 因子类型 | 权重 | 说明 |
|---------|------|------|
| 成长因子 | 30% | 营收增长率、利润增长率 |
| 质量因子 | 25% | ROE、ROA |
| 估值因子 | 15% | PE、PB（适度估值） |
| 动量因子 | 15% | 20日/60日动量 |
| 规模因子 | 10% | 市值50-200亿最优 |
| 技术因子 | 5% | 均线多头、新高 |

### 4. 回测引擎
提供三个版本:
- V1: 基础版 `run_tenbagger_backtest_jq.py`
- V2: 优化版 `run_tenbagger_backtest_v2.py`
- V3: 超级动量版 `run_tenbagger_backtest_v3.py`
- 多因子版: `tenbagger_multifactor_strategy.py`

## 历史10倍股特征总结

基于网络搜索和数据分析:

### 行业分布
- 电力设备 (新能源)
- 医药生物
- 电子/半导体
- 软件/AI

### 关键特征
1. **市值**: 50-200亿为最佳区间
2. **ROE**: > 10%
3. **成长性**: 营收增长 > 30%
4. **PE**: 15-35倍合理区间
5. **动量**: 起涨前已有正向动量
6. **民营企业**: 占比超70%

### 典型案例 (2023-2024)
- 寒武纪 (688256): AI芯片，涨幅387%
- 正丹股份 (300641): 化工，近10倍
- 艾融软件 (830799): 软件，近10倍

## 策略参数配置

```python
# 持仓管理
max_holdings = 10        # 分散持仓
single_stock_max = 0.15  # 单票15%

# 风控参数
stop_loss = -0.10        # 止损10%
take_profit = 0.80       # 止盈80%
trailing_stop = 0.15     # 移动止损15%
rebalance_days = 10      # 每10天调仓

# 筛选阈值
min_market_cap = 20      # 最小市值20亿
max_market_cap = 500     # 最大市值500亿
min_roe = 5              # ROE > 5%
min_revenue_growth = 10  # 营收增长 > 10%
```

## 使用方法

### 1. 运行特征挖掘
```bash
cd /home/taotao/dev/QuantTest/TRQuant
python scripts/tenbagger_feature_mining.py
```

### 2. 运行多因子回测
```bash
python scripts/tenbagger_multifactor_strategy.py 2024-01-01 2025-12-20
```

### 3. 查看报告
报告生成在 `reports/` 目录下

## 风险提示

⚠️ **重要**: 
- 历史回测不代表未来收益
- 10倍股极为稀少，占比仅2%
- 追求高收益必然承担高风险
- 投资有风险，入市需谨慎

## 后续优化方向

1. **数据源扩展**: 加入另类数据（舆情、资金流向）
2. **因子增强**: 加入机器学习因子权重优化
3. **风控升级**: 动态止损、波动率调整
4. **实盘对接**: QMT/Ptrade实盘交易

---
*创建时间: 2025-12-26*
*维护者: TRQuant Team*




## 系统概述

基于历史数据挖掘和多因子模型的十倍股筛选与交易策略系统。

## 核心组件

### 1. 特征挖掘系统
**文件**: `scripts/tenbagger_feature_mining.py`

功能:
- 扫描历史2-3年内涨幅超过10倍的股票
- 提取起涨点的多维度特征
- 存储到SQLite数据库

### 2. 特征数据库
**位置**: `data/tenbagger_features.db`

表结构:
- `tenbagger_stocks`: 10倍股主表
- `stock_features`: 股票特征表
- `feature_statistics`: 特征统计表

### 3. 多因子策略
**文件**: `scripts/tenbagger_multifactor_strategy.py`

因子配置 (基于历史10倍股特征分析):
| 因子类型 | 权重 | 说明 |
|---------|------|------|
| 成长因子 | 30% | 营收增长率、利润增长率 |
| 质量因子 | 25% | ROE、ROA |
| 估值因子 | 15% | PE、PB（适度估值） |
| 动量因子 | 15% | 20日/60日动量 |
| 规模因子 | 10% | 市值50-200亿最优 |
| 技术因子 | 5% | 均线多头、新高 |

### 4. 回测引擎
提供三个版本:
- V1: 基础版 `run_tenbagger_backtest_jq.py`
- V2: 优化版 `run_tenbagger_backtest_v2.py`
- V3: 超级动量版 `run_tenbagger_backtest_v3.py`
- 多因子版: `tenbagger_multifactor_strategy.py`

## 历史10倍股特征总结

基于网络搜索和数据分析:

### 行业分布
- 电力设备 (新能源)
- 医药生物
- 电子/半导体
- 软件/AI

### 关键特征
1. **市值**: 50-200亿为最佳区间
2. **ROE**: > 10%
3. **成长性**: 营收增长 > 30%
4. **PE**: 15-35倍合理区间
5. **动量**: 起涨前已有正向动量
6. **民营企业**: 占比超70%

### 典型案例 (2023-2024)
- 寒武纪 (688256): AI芯片，涨幅387%
- 正丹股份 (300641): 化工，近10倍
- 艾融软件 (830799): 软件，近10倍

## 策略参数配置

```python
# 持仓管理
max_holdings = 10        # 分散持仓
single_stock_max = 0.15  # 单票15%

# 风控参数
stop_loss = -0.10        # 止损10%
take_profit = 0.80       # 止盈80%
trailing_stop = 0.15     # 移动止损15%
rebalance_days = 10      # 每10天调仓

# 筛选阈值
min_market_cap = 20      # 最小市值20亿
max_market_cap = 500     # 最大市值500亿
min_roe = 5              # ROE > 5%
min_revenue_growth = 10  # 营收增长 > 10%
```

## 使用方法

### 1. 运行特征挖掘
```bash
cd /home/taotao/dev/QuantTest/TRQuant
python scripts/tenbagger_feature_mining.py
```

### 2. 运行多因子回测
```bash
python scripts/tenbagger_multifactor_strategy.py 2024-01-01 2025-12-20
```

### 3. 查看报告
报告生成在 `reports/` 目录下

## 风险提示

⚠️ **重要**: 
- 历史回测不代表未来收益
- 10倍股极为稀少，占比仅2%
- 追求高收益必然承担高风险
- 投资有风险，入市需谨慎

## 后续优化方向

1. **数据源扩展**: 加入另类数据（舆情、资金流向）
2. **因子增强**: 加入机器学习因子权重优化
3. **风控升级**: 动态止损、波动率调整
4. **实盘对接**: QMT/Ptrade实盘交易

---
*创建时间: 2025-12-26*
*维护者: TRQuant Team*









































