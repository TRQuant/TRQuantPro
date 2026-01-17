#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
V4.8开发经验归档到RAG知识库

将V4.8策略开发过程中的完整经验、优化过程、问题解决方案存入知识库，
遵循标准开发流程，为后续策略开发提供参考。
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 导入知识库工具
try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError:
    KB_AVAILABLE = False
    print("⚠️ MCP工具不可用，将使用直接文件操作")


def create_v48_knowledge_items() -> List[Dict[str, Any]]:
    """创建V4.8开发经验的知识库条目"""
    
    kb_items = []
    
    # ==================== 1. V4.8策略核心逻辑 ====================
    kb_items.append({
        'title': 'QMT周频因子策略V4.8 - 核心交易逻辑',
        'content': '''# QMT周频因子策略V4.8 - 核心交易逻辑

## 策略概述

TRQuant周频因子策略V4.8是一个基于7个验证因子的多因子选股策略，采用每两周调仓的频率进行轮动持仓。

## 核心特点

1. **因子驱动**: 基于438个历史10%+周收益案例验证的7个因子
2. **轮动策略**: 每两周换仓，保持持仓为当前最优的Top 10股票
3. **风险控制**: 跌破20日均线自动止损，保留10%现金储备
4. **成本优化**: 每两周调仓频率，交易成本仅0.56%

## 交易流程（9步）

```
每个交易日 (handlebar)
    ↓
检查是否满足调仓条件 (每10个交易日)
    ↓
[是] → 数据加载 (价量数据 + 基本面数据)
    ↓
因子计算 (7个因子：动量、相对位置、市值等)
    ↓
因子筛选 (硬阈值过滤)
    ↓
因子评分 (加权综合评分)
    ↓
选股 (Top 10，分数≥30)
    ↓
[轮动卖出] 卖出不在Top 10的持仓
    ↓
[止损卖出] 卖出跌破20日均线的持仓
    ↓
[买入] 买入新的Top 10股票（等权重分配）
    ↓
[否] → 跳过（持仓不变）
```

## 7个验证因子

| 因子 | 权重 | 说明 |
|------|------|------|
| momentum_20d | 19.61% | 20日动量（核心因子，5%~30%最优） |
| rel_position | 17.65% | 相对位置（0-100%，<80%避免追高） |
| market_cap | 16.67% | 市值（20-300亿，单位：100M） |
| momentum_5d | 14.71% | 5日短期动量（-5%~10%正常波动） |
| turnover_rate | 13.73% | 换手率（2%~10%，流动性指标） |
| roe | 9.80% | 净资产收益率（>0%表示盈利） |
| growth | 7.84% | 净利润增长率（>0%表示成长） |

## 关键参数设置

- **REBALANCE_PERIOD**: 10个交易日（每两周调仓）
- **MAX_STOCKS**: 10只（最大持仓数量）
- **MIN_TOTAL_SCORE**: 30.0（最低入选分数）
- **WARMUP_BARS**: 22（预热期，用于积累历史数据）

## 换仓触发条件

1. **定期换仓**: 每10个交易日（barpos % REBALANCE_PERIOD == 0）
2. **止损换仓**: 持仓跌破20日均线（current_price < ma20 * 0.95）

## V4.9优化（渐进式轮动 + 动态止损止盈）

- **渐进式轮动**: Top15且盈利≥5%的持仓保留50%仓位
- **动态止损**: -8%绝对止损 + MA20*0.97止损
- **动态止盈**: 盈利15%/20%后，回撤≥5%触发止盈
- **仓位约束**: 保留持仓后自动限制新开仓数量

## 代码位置

- 策略文件: `strategies/qmt/TRQuant_Weekly_Factor_V4.py`
- 策略文档: `docs/qmt/STRATEGY_COMPREHENSIVE_GUIDE.md`
- 回测结果: `docs/qmt/V4.8_PERFORMANCE_ANALYSIS.md`

## 回测表现

- **最终回报率**: +9.53%（3个月，2025-10-20至2025-12-29）
- **年化回报率**: ~38%
- **交易成本**: 0.56%（极低）
- **最大回撤**: ~2.5%（控制良好）
''',
        'type': 'development_experience',
        'tags': ['qmt', 'v4.8', 'factor_strategy', 'trading_logic', 'backtest_optimization'],
        'source': 'strategies/qmt/TRQuant_Weekly_Factor_V4.py'
    })
    
    # ==================== 2. 因子优化过程 ====================
    kb_items.append({
        'title': 'V4.8因子优化过程 - 从438案例到7因子体系',
        'content': '''# V4.8因子优化过程 - 从438案例到7因子体系

## 研究基础

基于历史数据挖掘438个周收益≥10%的高回报案例（2024-09-01 ~ 2025-03-16），通过逆向因子挖掘方法提取规律。

## 案例分类统计

| 类型 | 数量 | 占比 | 平均收益 | 特征 |
|------|------|------|---------|------|
| **小市值型** (市值<50亿) | 166 | 37.9% | 17.47% | 小盘股、弹性大、易被资金炒作 |
| **低位反弹型** (5日动量<0) | 248 | 56.6% | 15.62% | 低位盘整、近期回调、等待反弹 |
| **动量驱动型** (20日动量>15%) | 99 | 22.6% | 21.59% | 强趋势、高位运行、基本面一般 |
| **优质成长型** (ROE>5 & 增长>10%) | 11 | 2.5% | 13.64% | 基本面优秀、低位蓄势、数量稀少 |

## 关键发现

**高收益主要来自动量驱动和低位反弹，而非传统价值成长。**

## 因子特征分析

### 动量驱动型（99案例，平均21.59%）

| 因子 | 25%分位 | 中位数 | 75%分位 |
|------|---------|--------|---------|
| 市值(亿) | 43.1 | 71.5 | 161.0 |
| **20日动量(%)** | **19.5** | **26.2** | **35.7** |
| 5日动量(%) | -1.6 | 4.2 | 10.6 |
| 相对位置(%) | 61.9 | 82.2 | 100.0 |

**特征**: 强趋势、高位运行、基本面一般

### 低位反弹型（248案例，平均15.62%）

| 因子 | 25%分位 | 中位数 | 75%分位 |
|------|---------|--------|---------|
| 市值(亿) | 38.4 | 62.8 | 130.3 |
| 20日动量(%) | -10.2 | -3.8 | 4.7 |
| **5日动量(%)** | **-5.2** | **-3.0** | **-1.2** |
| **相对位置(%)** | **1.2** | **26.9** | **55.1** |

**特征**: 低位盘整、近期回调、等待反弹

## 因子权重确定

基于438案例的统计分析，确定7个因子的权重：

```python
FACTOR_WEIGHTS = {
    'momentum_20d': 1.00,    # 核心：20日动量（5%~30%最优）
    'rel_position': 0.90,    # 相对位置（<80%最优）
    'market_cap': 0.85,      # 市值（30~200亿最优）
    'momentum_5d': 0.75,     # 5日动量（-5%~10%最优）
    'turnover_rate': 0.70,   # 换手率（2%~8%最优）
    'roe': 0.50,             # ROE（>0，>10%更优）
    'growth': 0.40,          # 净利润增长（>0%）
}
# 归一化后
TOTAL_WEIGHT = sum(FACTOR_WEIGHTS.values())
FACTOR_WEIGHTS = {k: v / TOTAL_WEIGHT for k, v in FACTOR_WEIGHTS.items()}
```

## 筛选条件提炼

### 组合1: 适度动量型（推荐）

**历史匹配**: 55个案例，平均收益 **18.38%**

```python
conditions = {
    "market_cap": (30, 200),      # 市值30~200亿
    "momentum_20d": (5, 30),       # 20日动量5%~30%
    "momentum_5d": (-5, 10),       # 5日动量-5%~10%
    "roe_min": 0,                  # ROE > 0
}
```

**逻辑**: 捕捉正在上涨但未过热的趋势股

### 组合2: 低位反弹型

**历史匹配**: 93个案例，平均收益 **14.97%**

```python
conditions = {
    "market_cap": (30, 150),      # 市值30~150亿
    "momentum_20d": (-10, 15),     # 20日动量-10%~15%
    "momentum_5d": (-8, 2),        # 5日动量-8%~2%
    "rel_position_max": 60,        # 相对位置<60%
}
```

**逻辑**: 捕捉低位反弹机会

## V4.8优化调整

- **MIN_MOMENTUM_20D**: 5.0% → -5.0%（允许轻微负动量，适应弱市）
- **MIN_MARKET_CAP**: 30.0 → 20.0（扩大市值范围）
- **MAX_MARKET_CAP**: 200.0 → 300.0（允许更大市值）
- **REBALANCE_PERIOD**: 5 → 10（降低交易成本）

## 参考资料

- 完整研究报告: `docs/HIGH_RETURN_FACTOR_RESEARCH.md`
- 高收益推荐器: `core/advisor_v3/high_return_recommender.py`
''',
        'type': 'development_experience',
        'tags': ['factor_research', 'data_mining', 'v4.8', '438_cases'],
        'source': 'docs/HIGH_RETURN_FACTOR_RESEARCH.md'
    })
    
    # ==================== 3. QMT回测优化经验 ====================
    kb_items.append({
        'title': 'QMT回测优化经验 - 缓存机制与价格备用',
        'content': '''# QMT回测优化经验 - 缓存机制与价格备用

## 问题1: 数据加载缓慢（每次回测都重新下载）

### 问题描述
- 每次调仓都需要重新调用`get_history_data`下载5404只股票的数据
- 回测速度慢，重复回测时浪费时间和资源

### 解决方案: 三级缓存机制

```python
# 1. 内存缓存（同一bar内复用）
_data_cache = {}

# 2. 磁盘缓存（跨回测会话持久化）
_cache_dir = get_cache_dir()  # qmt_cache/
cache_file = f"qmt_data_{cache_hash}.pkl"

# 3. API调用（缓存未命中时）
data = ContextInfo.get_history_data(days, period, field, mode)
```

### 关键修复: 缓存键包含barpos

**错误做法**:
```python
# 历史数据不包含barpos → 不同bar使用相同缓存 → 数据错误
cache_key = f"{field}_{days}"  # ❌ 错误
```

**正确做法**:
```python
# 历史数据必须包含barpos，因为get_history_data是相对于当前bar的
cache_key = f"{field}_{days}_bar{barpos}"  # ✅ 正确
```

### 效果
- 首次回测: 正常速度（需要下载数据）
- 重复回测: 几乎瞬时（从磁盘缓存加载）
- 缓存命中率: 95%+（除首次外）

## 问题2: 选中的股票无法买入（缺少open价格）

### 问题描述
- 策略选中了10只股票，但只有1-2只能成功买入
- 日志显示: `[Buy Warning] {stock}: Not in current_prices (skipping)`
- 原因: `get_history_data('open', 1)` 只返回部分股票的数据

### 解决方案: 价格备用机制

```python
# 1. 优先尝试获取open价格
open_prices = get_all_stock_data(ContextInfo, target_stocks, 'open', 1)

# 2. 备用: 使用close价格（从close_22获取最新收盘价）
for stock in missing_stocks:
    if stock in close_22 and len(close_22[stock]) > 0:
        close_price = close_22[stock][-1]
        if close_price > 0:
            current_prices[stock] = [close_price]  # 使用close作为open的近似
```

### 效果
- 买入成功率: 25% → 90%+（大幅提升）
- 价格精度: open价格优先，close价格备用（可接受）
- 策略执行: 不再因缺少价格数据而跳过选中的股票

## 问题3: 缓存键优化导致的bug

### 问题描述
- 尝试优化缓存键，移除日期/barpos信息以复用缓存
- 结果: 所有调仓周期都选中相同的股票（使用过期缓存）

### 根本原因
QMT的`get_history_data`是**相对于当前bar位置**的：
- Bar 5770: `get_history_data(22, '1d', 'close', 0)` 返回bar 5749-5770的数据
- Bar 5780: `get_history_data(22, '1d', 'close', 0)` 返回bar 5759-5780的数据

**即使days相同，不同bar的数据窗口也不同！**

### 修复
```python
# 历史数据（days > 1）必须包含barpos
def _get_cache_file_path(field, days, barpos=None):
    if days > 1:  # 历史数据
        cache_key = f"{field}_{days}_bar{barpos}"  # ✅ 包含barpos
    else:  # 当前日数据
        cache_key = f"{field}_{days}_bar{barpos}"  # ✅ 也包含barpos（统一处理）
```

## 最佳实践

1. **缓存策略**:
   - 内存缓存: 同一bar内复用（最快）
   - 磁盘缓存: 跨会话持久化（需包含barpos）
   - API调用: 缓存未命中时使用（最慢）

2. **价格数据获取**:
   - 优先使用open价格（交易价格）
   - 备用使用close价格（历史数据中的最新收盘价）
   - 确保所有选中股票都有价格数据

3. **缓存键设计**:
   - 必须包含所有影响数据内容的参数（field, days, barpos）
   - 不要为了"复用"而省略关键参数
   - 测试验证: 不同bar位置的数据是否不同

## 代码位置

- 缓存实现: `strategies/qmt/TRQuant_Weekly_Factor_V4.py` (get_all_stock_data函数)
- 价格备用: `strategies/qmt/TRQuant_Weekly_Factor_V4.py` (handlebar函数，买入逻辑)
- 缓存文档: `docs/qmt/QMT_CACHE_OPTIMIZATION_FIX.md`
''',
        'type': 'development_experience',
        'tags': ['qmt', 'backtest_optimization', 'cache', 'data_loading', 'v4.8'],
        'source': 'strategies/qmt/TRQuant_Weekly_Factor_V4.py'
    })
    
    # ==================== 4. 回测结果分析与优化方向 ====================
    kb_items.append({
        'title': 'V4.8回测结果深度分析 - +9.53%回报率的成功要素',
        'content': '''# V4.8回测结果深度分析 - +9.53%回报率的成功要素

## 回测基本信息

- **回测周期**: 2025-10-20 至 2025-12-29 (约3个月)
- **最终回报率**: **+9.53%** (年化约38%)
- **交易成本**: 0.56% (5,590.39) - 极低
- **交易次数**: 100次
- **持仓数量**: 10只（满仓）
- **最大回撤**: ~2.5%（控制良好）
- **夏普比率**: ~2.5（优秀）

## 分阶段表现分析

### 阶段1: 首次建仓 (2025-10-20 → 2025-11-03)
- **回报率**: +1.61% (14天)
- **操作**: 买入10只股票（全部成功，价格备用机制生效）
- **评价**: ✅ 开局良好

### 阶段2: 第一次轮动 (2025-11-03 → 2025-11-17)
- **回报率**: +1.12% (累计 +2.73%)
- **操作**: 100%轮动（10只全换）
- **问题**: 买入后部分股票下跌（选股质量问题）
- **评价**: ⚠️ 轮动及时，但选股质量需提升

### 阶段3: 市场回调期 (2025-11-17 → 2025-12-01)
- **回报率**: -0.69% (累计 +2.04%)
- **操作**: 80%轮动（8只换）
- **问题**: 市场回调，整体表现不佳
- **评价**: ⚠️ 经历市场调整，策略基本稳定

### 阶段4: 深度调整 (2025-12-01 → 2025-12-15)
- **回报率**: -0.03% (累计 +2.01%)
- **操作**: 100%轮动（10只全换）
- **问题**: 选股通过率下降（18/5404 = 0.33%），市场环境不利
- **评价**: ⚠️ 市场环境不利，策略处于防守状态

### 阶段5: 大幅反弹 (2025-12-15 → 2025-12-29)
- **回报率**: **+7.52%** (累计 +9.53%)
- **操作**: 90%轮动（9只换）
- **成功因素**: 
  - 选股质量提升（Top 10分数75+）
  - 市场环境转好，股票集体上涨
  - 策略在调整期坚持持仓，获得反弹收益
- **评价**: ✅ 策略在反弹期表现优秀，大幅盈利

## 关键成功因素

1. ✅ **价格备用机制**: 买入成功率100%（vs之前25%）
2. ✅ **轮动及时**: 能够快速切换到更好的股票
3. ✅ **持仓坚持**: 在市场调整期坚持持仓，获得反弹收益
4. ✅ **成本控制**: 交易成本仅0.56%，不影响收益
5. ✅ **分散化**: 10只股票分散投资，降低单一股票风险

## 待改进问题

1. ⚠️ **轮动过于频繁**: 平均每次换80-100%，可能错过持续上涨
   - 案例: 300136.SZ上涨45.9%，但在轮动时被卖出
   - 优化: V4.9已实现渐进式轮动（保留Top15且盈利>5%的持仓）

2. ⚠️ **没有止盈机制**: 300136.SZ上涨45.9%后没有止盈
   - 优化: V4.9已实现动态止盈（+15%/+20%后回撤≥5%触发）

3. ⚠️ **止损阈值过宽**: 5%缓冲可能太大，止损机制未触发
   - 优化: V4.9调整为MA20*0.97（3%缓冲）

4. ⚠️ **选股质量波动**: 阶段4-5通过率下降（0.33%-0.80%波动）
   - 优化建议: 提高MIN_TOTAL_SCORE至32.0，添加趋势确认

5. ⚠️ **一次性买入**: 可能在不佳价格成交
   - 优化建议: 渐进式建仓（分3次买入：50%+30%+20%）

## 持仓表现Top 5

| 股票 | 买入价格 | 卖出价格 | 收益率 | 持有期 | 评价 |
|------|----------|----------|--------|--------|------|
| 300136.SZ | 36.31 | 53.00 | **+45.9%** | 14天 | ✅ 最佳 |
| 002384.SZ | 80.00 | 87.40 | +9.25% | 14天 | ✅ 优秀 |
| 002709.SZ | 40.91 | 42.83 | +4.69% | 14天 | ✅ 良好 |
| 002460.SZ | 68.10 | 69.92 | +2.67% | 14天 | ✅ 良好 |
| 688981.SH | 123.80 | 127.19 | +2.74% | 14天 | ✅ 良好 |

## 选股质量分析

| 调仓次数 | 通过筛选股票数 | 通过率 | Top 1分数 | 评价 |
|---------|--------------|--------|-----------|------|
| #1 | 43 | 0.80% | 80.5 | ✅ 高 |
| #2 | 35 | 0.65% | 74.7 | ✅ 良好 |
| #3 | 27 | 0.50% | 75.2 | ✅ 良好 |
| #4 | 25 | 0.46% | 69.4 | ⚠️ 下降 |
| #5 | 18 | 0.33% | 72.8 | ⚠️ 最低 |
| #6 | 35 | 0.65% | 75.3 | ✅ 恢复 |

**发现**: 选股通过率在0.33%-0.80%之间波动，与市场环境相关

## 轮动效果分析

- **阶段2**: 100%轮动（10只全换）
- **阶段3**: 80%轮动（8只换）
- **阶段4**: 100%轮动（10只全换）
- **阶段5**: 90%轮动（9只换）

**问题**: 轮动过于频繁，可能错过持续上涨的股票
**优化**: V4.9实现渐进式轮动，保留Top15且盈利>5%的持仓

## 优化建议

### 短期优化（已实现V4.9）
1. ✅ 渐进式轮动（保留Top15且盈利>5%的持仓）
2. ✅ 动态止损止盈（+15%/+20%后回撤≥5%触发）

### 中期优化（待实现）
3. ⏳ 渐进式建仓（分3次买入：50%+30%+20%）
4. ⏳ 提高选股质量标准（MIN_TOTAL_SCORE提高至32.0）
5. ⏳ 添加趋势确认（5日和20日动量方向一致）

### 长期优化（未来方向）
6. ⏳ 行业轮动（跟随市场热点）
7. ⏳ 机器学习优化（因子权重和阈值）
8. ⏳ 多策略组合（趋势+反转+套利）

## 参考资料

- 完整分析报告: `docs/qmt/V4.8_PERFORMANCE_ANALYSIS.md`
- 策略指南: `docs/qmt/STRATEGY_COMPREHENSIVE_GUIDE.md`
''',
        'type': 'development_experience',
        'tags': ['backtest_analysis', 'performance', 'v4.8', 'optimization', '9.53%'],
        'source': 'docs/qmt/V4.8_PERFORMANCE_ANALYSIS.md'
    })
    
    # ==================== 5. 渐进式轮动与动态止损止盈实现 ====================
    kb_items.append({
        'title': 'V4.9渐进式轮动与动态止损止盈实现',
        'content': '''# V4.9渐进式轮动与动态止损止盈实现

## 背景

V4.8回测中发现的问题：
1. 轮动过于频繁（100%换仓），可能错过持续上涨的股票（如300136.SZ上涨45.9%）
2. 没有止盈机制，无法锁定利润
3. 止损阈值过宽（5%缓冲），整个回测期间未触发

## V4.9优化方案

### 1. 渐进式轮动（保留优质持仓）

#### 核心逻辑
如果持仓股票仍在Top15且盈利≥5%，保留50%仓位，而不是全额卖出。

#### 实现代码

```python
# 参数配置
RETAIN_TOP_RANK = 15         # 在排名前15时可考虑保留
RETAIN_MIN_PNL = 5.0         # 至少盈利5%才保留
RETAIN_KEEP_RATIO = 0.5      # 保留50%仓位

def should_retain_position(stock, lots, close_data, ContextInfo, rank_map):
    """判断是否保留持仓"""
    rank = rank_map.get(stock)
    if rank is None or rank > RETAIN_TOP_RANK:
        return 0, None, None
    
    entry_price = ContextInfo.buypoint.get(stock, 0)
    current_price = close_data[stock][-1]
    pnl_pct = (current_price - entry_price) / entry_price * 100
    
    if pnl_pct < RETAIN_MIN_PNL:
        return 0, rank, pnl_pct
    
    keep_lots = int(lots * RETAIN_KEEP_RATIO)
    if keep_lots <= 0 and lots > 1:
        keep_lots = 1
    if keep_lots >= lots:
        keep_lots = max(lots - 1, 0)  # 留至少1手做轮动
    
    return keep_lots, rank, pnl_pct
```

#### 轮动逻辑调整

```python
# 卖出逻辑
for stock in current_holdings:
    if stock not in target_stocks:
        keep_lots, keep_rank, keep_pnl = should_retain_position(...)
        lots_to_sell = lots - keep_lots  # 只卖出部分仓位
        
        if keep_lots > 0:
            print(f"  [RETAIN] {stock}: Keeping {keep_lots} lots "
                  f"(rank #{keep_rank}, P&L {keep_pnl:.2f}%)")
```

#### 仓位约束

```python
# 买入时限制新开仓数量，避免超过MAX_STOCKS
active_positions = sum(1 for v in ContextInfo.holdings.values() if v > 0)
available_slots = max(0, MAX_STOCKS - active_positions)
stocks_to_buy = stocks_to_buy[:available_slots]  # 限制数量
```

### 2. 动态止损止盈

#### 参数配置

```python
STOP_LOSS_THRESHOLD = -8.0   # 绝对止损：亏损超过-8%
STOP_LOSS_MA_BUFFER = 0.97   # MA20止损缓冲：跌破MA20*0.97
TAKE_PROFIT_LEVEL_1 = 15.0   # 第一段止盈：盈利≥15%
TAKE_PROFIT_LEVEL_2 = 20.0   # 第二段止盈：盈利≥20%
TAKE_PROFIT_TRAIL = 5.0      # 回撤幅度：从峰值回撤5%触发止盈
```

#### 持仓统计

```python
# 为每只持仓记录entry_price和max_price
def update_position_stats_on_buy(ContextInfo, stock, price, shares):
    """买入时更新持仓统计"""
    stats = ensure_position_stats(ContextInfo)
    total_shares = ContextInfo.holdings.get(stock, 0) * 100
    
    # 计算平均成本
    prev_entry = stats.get(stock, {}).get('entry_price', price)
    prev_shares = max(total_shares - shares, 0)
    
    if total_shares > 0 and prev_shares > 0:
        new_entry = ((prev_entry * prev_shares) + (price * shares)) / total_shares
    else:
        new_entry = price
    
    stats[stock] = {
        'entry_price': new_entry,
        'max_price': max(stats[stock].get('max_price', price), price)
    }

def update_position_max_price(ContextInfo, stock, current_price):
    """更新最大价格（用于追踪止盈）"""
    stats = ensure_position_stats(ContextInfo)
    if stock in stats:
        stats[stock]['max_price'] = max(stats[stock].get('max_price', current_price), current_price)
```

#### 退出信号判断

```python
def evaluate_exit_signal(entry_price, current_price, ma20, max_price):
    """评估退出信号"""
    pnl_pct = (current_price - entry_price) / entry_price * 100
    
    # 1. 绝对止损
    if pnl_pct <= STOP_LOSS_THRESHOLD:
        return True, f"PnL {pnl_pct:.2f}% <= {STOP_LOSS_THRESHOLD}%"
    
    # 2. MA20止损
    if ma20 and ma20 > 0 and current_price < ma20 * STOP_LOSS_MA_BUFFER:
        return True, f"Price {current_price:.2f} < MA20*{STOP_LOSS_MA_BUFFER}"
    
    # 3. 动态止盈（回撤触发）
    if max_price and max_price > 0:
        max_gain_pct = (max_price - entry_price) / entry_price * 100
        drawdown_pct = (current_price - max_price) / max_price * 100
        
        # 盈利20%后，回撤≥5%触发止盈
        if max_gain_pct >= TAKE_PROFIT_LEVEL_2 and drawdown_pct <= -TAKE_PROFIT_TRAIL:
            return True, f"Trailing take-profit (gain {max_gain_pct:.2f}%, drawdown {drawdown_pct:.2f}%)"
        # 盈利15%后，回撤≥5%触发止盈
        if max_gain_pct >= TAKE_PROFIT_LEVEL_1 and drawdown_pct <= -TAKE_PROFIT_TRAIL:
            return True, f"Trailing take-profit (gain {max_gain_pct:.2f}%, drawdown {drawdown_pct:.2f}%)"
    
    return False, ""
```

#### 退出检查流程

```python
def check_exit_signals(ContextInfo, close_data, current_prices):
    """检查持仓的退出信号"""
    for stock in current_holdings:
        lots = ContextInfo.holdings.get(stock, 0)
        if lots <= 0:
            continue
        
        # 计算MA20
        close_list = close_data[stock]
        ma20 = np.mean(close_list[-20:])
        current_price = close_list[-1]
        
        # 更新最大价格
        stats = update_position_max_price(ContextInfo, stock, current_price)
        entry_price = stats.get('entry_price', ContextInfo.buypoint.get(stock, 0))
        max_price = stats.get('max_price', current_price)
        
        # 评估退出信号
        exit_signal, reason = evaluate_exit_signal(entry_price, current_price, ma20, max_price)
        
        if exit_signal:
            print(f"  [SELL-EXIT] {stock}: {reason}")
            order_shares(stock, -lots * 100, current_price, ContextInfo)
```

## 预期效果

1. **减少不必要轮动**: 保留Top15且盈利>5%的持仓，避免错过持续上涨
2. **保护利润**: 动态止盈机制，在盈利回撤时及时锁定收益
3. **控制亏损**: 绝对止损（-8%）+ MA20止损（更严格）
4. **仓位管理**: 保留持仓后自动限制新开仓数量

## 代码位置

- 参数定义: `strategies/qmt/TRQuant_Weekly_Factor_V4.py` (141-152行)
- 保留逻辑: `strategies/qmt/TRQuant_Weekly_Factor_V4.py` (should_retain_position函数)
- 退出信号: `strategies/qmt/TRQuant_Weekly_Factor_V4.py` (evaluate_exit_signal函数)
- 退出检查: `strategies/qmt/TRQuant_Weekly_Factor_V4.py` (check_exit_signals函数)
''',
        'type': 'development_experience',
        'tags': ['v4.9', 'progressive_rotation', 'dynamic_stop_loss', 'take_profit', 'position_management'],
        'source': 'strategies/qmt/TRQuant_Weekly_Factor_V4.py'
    })
    
    return kb_items


def add_to_knowledge_base(kb_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """将知识库条目添加到RAG知识库"""
    if not KB_AVAILABLE:
        return {
            'success': False,
            'error': 'MCP工具不可用',
            'items': kb_items
        }
    
    results = {
        'success': 0,
        'failed': 0,
        'errors': [],
        'knowledge_ids': []
    }
    
    print(f"\n📚 准备存入 {len(kb_items)} 个V4.8开发经验条目...")
    print("=" * 70)
    
    for i, item in enumerate(kb_items, 1):
        print(f"\n[{i}/{len(kb_items)}] {item['title']}")
        
        try:
            result = knowledge_add(
                title=item['title'],
                content=item['content'],
                type=item['type'],
                tags=item['tags'],
                source=item.get('source', '')
            )
            
            if result.get('success') or result.get('knowledge_id'):
                results['success'] += 1
                kb_id = result.get('knowledge_id') or result.get('id') or 'unknown'
                results['knowledge_ids'].append(kb_id)
                print(f"  ✅ 成功存入 (ID: {kb_id})")
            else:
                results['failed'] += 1
                error_msg = result.get('error', 'Unknown error')
                results['errors'].append(f"{item['title']}: {error_msg}")
                print(f"  ❌ 失败: {error_msg}")
                
        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{item['title']}: {str(e)}")
            print(f"  ❌ 异常: {str(e)}")
    
    print("\n" + "=" * 70)
    print("📊 存入结果")
    print("=" * 70)
    print(f"成功: {results['success']} 个")
    print(f"失败: {results['failed']} 个")
    print(f"总计: {len(kb_items)} 个")
    
    return results


def main():
    """主函数"""
    print("=" * 70)
    print("V4.8开发经验归档到RAG知识库")
    print("=" * 70)
    
    # 创建知识库条目
    kb_items = create_v48_knowledge_items()
    
    # 存入知识库
    results = add_to_knowledge_base(kb_items)
    
    # 输出总结
    print("\n" + "=" * 70)
    if results['success'] > 0:
        print(f"✅ 成功归档 {results['success']} 条V4.8开发经验到知识库")
        if results['knowledge_ids']:
            print(f"   知识ID: {', '.join(results['knowledge_ids'][:5])}")
            if len(results['knowledge_ids']) > 5:
                print(f"   ... 还有 {len(results['knowledge_ids']) - 5} 条")
    else:
        print("❌ 归档失败，请检查错误信息")
        for error in results['errors']:
            print(f"   - {error}")
    print("=" * 70)
    
    return results


if __name__ == '__main__':
    main()
