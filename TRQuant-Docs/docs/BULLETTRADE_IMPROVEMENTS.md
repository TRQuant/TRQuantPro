# BulletTrade回测改进建议

## 🚨 问题诊断

### 回测结果
- **策略收益**: 0.00%
- **交易次数**: 0次
- **持仓**: 始终为0只
- **资金**: 未变化（¥1,000,000）

### 核心问题
**策略在整个回测期间没有执行任何交易**

## 🔍 根本原因

### 1. 选股条件过于严格
```python
# 原代码：要求5日和20日动量都>0
valid = (mom_short > 0) & (mom_long > 0)
```
- 在震荡市场中，可能没有股票同时满足两个条件
- 导致选股函数返回空列表

### 2. 数据获取问题
- 聚宽账号连接限制："最多只能开启1个连接"
- 可能影响数据获取的稳定性

### 3. 日志不足
- 无法看到选股过程的详细信息
- 难以定位问题

## ✅ 改进方案

### 改进版策略文件
```
strategies/bullettrade/TRQuant_momentum_v3_improved.py
```

### 关键改进点

#### 1. 放宽选股条件（三级策略）
```python
# 方案1: 至少一个动量>0（宽松）
valid1 = (mom_short > 0) | (mom_long > 0)

# 方案2: 两个动量都>0（严格）
valid2 = (mom_short > 0) & (mom_long > 0)

# 优先使用严格条件，不足时使用宽松条件
if len(score2) >= MAX_STOCKS:
    score = score2  # 严格条件
elif len(score1) >= MAX_STOCKS:
    score = score1  # 宽松条件
else:
    score = (mom_short * 0.5 + mom_long * 0.5).dropna()  # 综合得分
```

#### 2. 添加兜底策略
```python
def fallback_select(context, stocks):
    """兜底选股策略 - 市值排序"""
    # 如果动量选股失败，使用市值排序
    # 确保至少能选出股票
```

#### 3. 增强日志输出
```python
log.info(f'[选股] 开始选股，股票池: {len(stocks)}只')
log.info(f'[选股] 过滤后: {len(stocks)}只')
log.info(f'[选股] 动量计算完成: 短期{len(mom_short.dropna())}只')
log.info(f'[选股] 选股成功: {len(selected)}只 - {selected}')
```

#### 4. 优化数据获取
- 限制单次获取股票数量（30只）
- 添加异常处理和重试机制
- 处理数据格式异常

#### 5. 改进调仓逻辑
- 添加买入/卖出计数
- 详细的交易日志
- 异常处理

## 📊 预期改进效果

| 指标 | 改进前 | 改进后（预期） |
|------|--------|---------------|
| 交易次数 | 0次 | >0次 |
| 持仓天数 | 0天 | >0天 |
| 策略收益 | 0% | 有收益/亏损 |
| 选股成功率 | 0% | >50% |

## 🚀 运行改进版策略

```bash
source extension/venv/bin/activate

bullet-trade backtest strategies/bullettrade/TRQuant_momentum_v3_improved.py \
  --start 2025-03-17 \
  --end 2025-09-13 \
  --cash 1000000 \
  --benchmark 000300.XSHG \
  --output backtest_results/bullettrade_v3_improved \
  --auto-report
```

## 📋 检查清单

运行改进版后，检查以下内容：

- [ ] 日志中是否有"选股成功"记录
- [ ] 是否有"买入"和"卖出"记录
- [ ] 持仓是否>0
- [ ] 资金是否有变化
- [ ] 是否有交易记录

## 💡 进一步优化建议

1. **参数优化**
   - 调整动量周期（5日/20日）
   - 调整调仓频率（5天）
   - 调整持股数量（5只）

2. **策略优化**
   - 添加成交量确认
   - 添加技术指标过滤
   - 添加行业轮动逻辑

3. **风控优化**
   - 动态止损
   - 仓位管理
   - 风险预算

4. **数据优化**
   - 使用本地数据缓存
   - 优化数据获取频率
   - 处理连接限制问题
