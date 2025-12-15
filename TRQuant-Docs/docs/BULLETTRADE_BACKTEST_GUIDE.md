# BulletTrade回测指南

## 📁 策略文件位置

```
strategies/bullettrade/TRQuant_momentum_v3_bt.py
```

## 🔧 配置说明

### 1. 环境配置 (.env)

```bash
# BulletTrade 配置
DEFAULT_DATA_PROVIDER=jqdata
JQDATA_USERNAME=18072069583
JQDATA_PASSWORD=%5Diamond
DEFAULT_BROKER=simulator
```

### 2. 运行回测命令

```bash
# 激活虚拟环境
source extension/venv/bin/activate

# 运行回测
bullet-trade backtest strategies/bullettrade/TRQuant_momentum_v3_bt.py \
  --start 2025-03-17 \
  --end 2025-09-13 \
  --cash 1000000 \
  --benchmark 000300.XSHG \
  --output backtest_results/bullettrade_v3 \
  --auto-report
```

## 📊 回测参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 回测区间 | 2025-03-17 ~ 2025-09-13 | 聚宽账号数据范围 |
| 初始资金 | 1,000,000 | 100万 |
| 基准指数 | 000300.XSHG | 沪深300 |
| 数据源 | JQData | 聚宽数据 |

## ⚠️ 重要说明

1. **使用BulletTrade引擎**: 不是直接调用聚宽API，而是通过BulletTrade回测引擎
2. **数据源限制**: 聚宽账号数据范围 2024-09-06 至 2025-09-13
3. **API兼容性**: 策略代码使用聚宽风格API，BulletTrade会自动适配

## 🔍 关键修复

1. **滑点设置**: 使用 `FixedSlippage(0.001)` (BulletTrade支持)
2. **数据获取**: 限制股票数量避免超时
3. **错误处理**: 增强异常处理和日志输出

## 📈 回测结果位置

```
backtest_results/bullettrade_v3/
├── backtest.log          # 回测日志
├── metrics.json          # 绩效指标
├── daily_records.csv     # 每日记录
├── report.html           # HTML报告
└── ...
```

## 🚀 下一步

1. 检查回测日志确认策略正常运行
2. 查看HTML报告分析绩效
3. 根据结果优化策略参数
