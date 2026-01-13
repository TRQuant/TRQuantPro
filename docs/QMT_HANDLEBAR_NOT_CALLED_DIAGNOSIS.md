# QMT handlebar函数未被调用问题诊断

## 问题现象

策略初始化成功（`init()`函数被调用），但看不到`handlebar()`函数的日志输出。

## 可能原因

### 1. QMT回测设置问题

**检查项**：
- ✅ 回测日期范围是否正确设置（2025-10-11 到 2026-01-09）
- ✅ 初始资金是否设置（建议至少100万）
- ✅ 回测模式是否正确（研究环境 vs 实盘环境）
- ✅ 是否点击了"运行"或"开始回测"按钮

**解决方案**：
1. 确认回测设置中日期范围包含交易日
2. 确认初始资金不为0
3. 确认回测已实际启动（不只是加载策略）

### 2. QMT版本问题

**检查项**：
- QMT版本是否支持研究环境回测
- 是否需要特定版本才支持`handlebar()`回调

**解决方案**：
1. 检查QMT版本号
2. 查看QMT官方文档，确认版本要求
3. 尝试更新到最新版本

### 3. 策略文件加载问题

**检查项**：
- 策略文件是否正确加载到QMT
- 文件编码是否正确（ASCII）
- 是否有语法错误

**解决方案**：
1. 确认文件路径正确
2. 确认文件编码为ASCII（已修复）
3. 确认没有语法错误（已通过语法检查）

### 4. QMT回调函数注册问题

**检查项**：
- QMT是否自动识别`handlebar()`函数
- 是否需要显式注册回调函数

**解决方案**：
1. 确认函数名正确：`handlebar(ContextInfo)`
2. 确认函数在模块顶层（不在类内）
3. 尝试添加`before_trading_start()`和`after_trading_end()`回调（已添加）

## 已实现的回调函数

当前策略已实现以下回调函数：

1. **`init(ContextInfo)`** ✅
   - 策略初始化
   - 已确认被调用

2. **`before_trading_start(ContextInfo)`** ✅
   - 每个交易日开盘前调用
   - 已添加，用于诊断

3. **`handlebar(ContextInfo)`** ✅
   - 每个交易日盘中调用（K线回调）
   - 已增强日志，但未看到输出

4. **`after_trading_end(ContextInfo)`** ✅
   - 每个交易日收盘后调用
   - 已增强日志，但未看到输出

## 诊断步骤

### 步骤1：检查回测设置

1. 打开QMT回测设置
2. 确认：
   - 起始日期：2025-10-11
   - 结束日期：2026-01-09
   - 初始资金：>= 1000000
   - 回测模式：研究环境

### 步骤2：检查日志输出

运行回测后，查看日志：

**如果看到**：
- `[Init]` 日志 ✅（已确认）
- `[Before Trading]` 日志 ❓（需要确认）
- `[Handlebar]` 日志 ❓（需要确认）
- `[After Trading]` 日志 ❓（需要确认）

### 步骤3：检查QMT版本

1. 查看QMT版本号
2. 确认是否支持研究环境回测
3. 查看QMT官方文档

### 步骤4：尝试简化测试

创建一个最简单的测试策略：

```python
# -*- coding: ascii -*-
def init(ContextInfo):
    print("[Test] init() called")

def handlebar(ContextInfo):
    print("[Test] handlebar() called")

def before_trading_start(ContextInfo):
    print("[Test] before_trading_start() called")

def after_trading_end(ContextInfo):
    print("[Test] after_trading_end() called")
```

如果这个简单策略也没有输出`handlebar()`日志，说明是QMT配置或版本问题。

## 可能的解决方案

### 方案1：检查QMT回测模式

确保使用的是"研究环境"回测，而不是"实盘环境"。

### 方案2：检查日期范围

确保回测日期范围包含交易日（2025-10-11到2026-01-09应该包含多个交易日）。

### 方案3：检查初始资金

确保初始资金不为0，建议至少100万。

### 方案4：联系QMT技术支持

如果以上方案都不行，可能需要联系QMT技术支持，询问：
1. 研究环境回测的正确使用方法
2. `handlebar()`回调函数的调用时机
3. 是否有特定的配置要求

## 参考文档

- `strategies/qmt/README_RESEARCH.md` - QMT研究环境API说明
- `docs/QMT_BACKTEST_NO_TRADES_FIX.md` - QMT回测无交易记录问题修复
- `docs/QMT_ENCODING_FIX.md` - QMT编码问题修复

## 更新日期

2026-01-09
