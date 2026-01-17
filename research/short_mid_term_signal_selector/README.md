## Short/Mid-term Signal Selector (A-shares + ETFs)

这是一个**独立子模块**，用于在近期行情（短期-中期）下，基于多因子模型生成：
- **候选个股清单**（高成长潜力、趋势跟随、流动性过滤）
- **候选ETF清单**（宽基/行业/主题，偏趋势与动量）
- 一份**可直接阅读的 HTML 报告**（包含参数、Top列表、因子贡献与图表）

### 设计原则
- **不接入现有框架**：此目录自包含、单独运行；只复用已有的 JQData 配置与认证方式。
- **短-中期导向**：更强调动量/趋势/量价确认；基本面成长因子作为可选增强（需要有权限/字段可用）。
- **可扩展**：后续可以在此目录内继续加入风控、仓位、持仓期与交易规则。

### 运行方式
在项目根目录执行：

```bash
python3 -m research.short_mid_term_signal_selector.run_report
```

输出文件：
- `output/reports/short_mid_term_selector_{timestamp}.html`

