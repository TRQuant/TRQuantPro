# QMT回测无交易记录问题修复

## 问题描述

QMT回测策略初始化成功，股票池加载正常（4950只A股），但没有产生任何交易记录。

## 问题分析

根据知识库和QMT API文档，可能的原因包括：

1. **账户ID获取失败**：`ContextInfo.accout_id`可能不存在或为None
2. **账户信息获取失败**：无法获取账户信息导致无法计算仓位
3. **持仓查询失败**：无法获取当前持仓导致调仓逻辑无法执行
4. **选股条件过严**：没有股票通过筛选条件
5. **handlebar未正确调用**：调仓逻辑未执行

## 修复方案

### 1. 账户ID获取（多种方式兼容）

```python
# 在init()中获取账户ID
g_account_id = None
if hasattr(ContextInfo, 'accout_id'):
    g_account_id = ContextInfo.accout_id
elif hasattr(ContextInfo, 'account_id'):
    g_account_id = ContextInfo.account_id
elif hasattr(ContextInfo, 'm_strAccountID'):
    g_account_id = ContextInfo.m_strAccountID
```

### 2. 账户信息获取（支持有/无账户ID）

```python
# 在rebalance()中获取账户信息
try:
    if account_id:
        account_info = ContextInfo.get_account_info(account_id)
    else:
        account_info = ContextInfo.get_account_info()
except Exception as e:
    print(f"[Rebalance] Failed to get account info: {e}")
    return
```

### 3. 持仓查询（多种调用方式）

```python
# 在rebalance()和check_risk_control()中获取持仓
try:
    if account_id:
        positions = ContextInfo.get_trade_detail_data(account_id, 'stock', 'position')
    else:
        positions = ContextInfo.get_trade_detail_data('stock', 'position')
except Exception as e:
    print(f"Failed to get positions: {e}")
    positions = []
```

### 4. 选股失败详细日志

```python
# 在rebalance()中，如果选股失败，显示详细原因
if not selected_stocks:
    print("[Rebalance] No stocks available, skip rebalancing")
    print("[Rebalance] This may be due to:")
    print("  1. No stocks passed the factor filters")
    print("  2. Factor calculation failed")
    print("  3. Stock pool is empty")
    return
```

### 5. 详细日志输出

- **初始化日志**：显示账户ID、股票池大小
- **选股日志**：显示选股过程、因子计算、筛选结果
- **调仓日志**：显示账户信息、目标仓位、交易执行
- **风控日志**：显示持仓检查、止损止盈执行

## 修复文件

- `strategies/qmt/TRQuant_V4_QMT_Backtest_3Months.py`

## 关键修改

1. **全局变量**：添加`g_account_id`用于存储账户ID
2. **init()函数**：添加账户ID获取逻辑
3. **rebalance()函数**：
   - 添加账户ID获取
   - 改进账户信息获取（支持多种方式）
   - 改进持仓查询（支持多种方式）
   - 添加选股失败详细提示
   - 添加账户信息日志
4. **check_risk_control()函数**：
   - 添加账户ID获取
   - 改进持仓查询（支持多种方式）

## 测试建议

1. **运行回测**：查看日志输出，确认：
   - 账户ID是否正确获取
   - 选股是否成功
   - 账户信息是否正常
   - 调仓是否执行

2. **如果没有交易记录**，检查日志中的：
   - `[Rebalance] No stocks available` - 选股失败原因
   - `[Stock Selection] After filtering: 0 stocks` - 筛选条件是否过严
   - `[Rebalance] Failed to get account info` - 账户信息获取失败
   - `[Rebalance] Account info is None` - 账户信息为空

3. **如果选股失败**，检查：
   - 因子计算是否正常（查看`[Stock Selection] Calculated factors`日志）
   - 筛选条件是否合理（查看`[Stock Selection] Statistics before filtering`日志）
   - 是否需要调整`MIN_TOTAL_SCORE`等参数

## 参考文档

- `strategies/qmt/README_RESEARCH.md` - QMT研究环境API说明
- `docs/QMT_STOCK_CODE_VALIDATION_FIX.md` - QMT股票代码格式修复
- `docs/QMT_ENCODING_FIX.md` - QMT编码问题修复

## 更新日期

2026-01-09
