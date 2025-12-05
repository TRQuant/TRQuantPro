# test2

📊 **多因子策略**

基于多因子评分的选股策略，适合各种市场环境

## 项目信息

| 属性 | 值 |
|------|-----|
| 平台 | PTRADE |
| 策略风格 | multi_factor |
| 股票池 | HS300, ZZ500, ZZ800, ZZ1000 |
| 回测周期 | 2024-12-03 ~ 2025-08-03 |
| 初始资金 | ¥1,000,000 |

## 风控参数

- 单票最大仓位: 10%
- 止损线: 8%
- 止盈线: 20%

## 目录结构

```
test2/
├── .trquant/           # 项目配置
│   └── project.json
├── strategies/         # 策略代码
├── data/              # 数据文件
├── reports/           # 分析报告
├── backtest/          # 回测结果
├── config/            # 配置文件
└── README.md
```

## 快速开始

1. 在Cursor中打开项目
2. 按 `Ctrl+Shift+P` 输入 `TRQuant`
3. 执行 `TRQuant: Run Backtest` 运行回测

## 使用TRQuant命令

- **获取市场状态**: 分析当前市场环境
- **推荐因子**: 获取适合当前市场的因子
- **运行回测**: 执行策略回测
- **分析结果**: 分析回测表现

---

*由TRQuant Cursor Extension自动生成*
