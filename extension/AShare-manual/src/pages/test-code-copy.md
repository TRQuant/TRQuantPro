---
title: "代码复制功能测试"
description: "测试代码复制功能和卡片颜色变体"
lang: zh-CN
alt: "代码复制功能测试"
layout: /src/layouts/HandbookLayout.astro
updateDate: "2025-01-03"
---

# 代码复制功能测试

这是一个测试页面，用于验证代码复制功能和新的卡片颜色变体系统。

## 📋 卡片颜色变体演示

以下是使用VS Code Dark主题配色的卡片颜色变体演示：

### 章节概览卡片变体

<div class="overview-grid">
  <div class="overview-card variant-blue">
    <div class="card-icon">🔵</div>
    <h3>蓝色主题</h3>
    <p>VS Code 关键字颜色 (#569cd6)</p>
  </div>
  <div class="overview-card variant-orange">
    <div class="card-icon">🟠</div>
    <h3>橙色主题</h3>
    <p>VS Code 字符串颜色 (#ce9178)</p>
  </div>
  <div class="overview-card variant-green">
    <div class="card-icon">🟢</div>
    <h3>绿色主题</h3>
    <p>VS Code 注释颜色 (#6a9955)</p>
  </div>
  <div class="overview-card variant-yellow">
    <div class="card-icon">🟡</div>
    <h3>黄色主题</h3>
    <p>VS Code 函数颜色 (#dcdcaa)</p>
  </div>
  <div class="overview-card variant-cyan">
    <div class="card-icon">🔷</div>
    <h3>青色主题</h3>
    <p>VS Code 类名颜色 (#4ec9b0)</p>
  </div>
  <div class="overview-card variant-purple">
    <div class="card-icon">🟣</div>
    <h3>紫色主题</h3>
    <p>VS Code 变量颜色 (#c586c0)</p>
  </div>
</div>

### 指标卡片变体

<div class="metrics-grid">
  <div class="metric-card variant-blue">
    <div class="metric-value">25.8%</div>
    <div class="metric-label">年化收益率</div>
    <div class="metric-benchmark">vs 基准 18.2%</div>
  </div>
  <div class="metric-card variant-orange">
    <div class="metric-value">15.2%</div>
    <div class="metric-label">波动率</div>
    <div class="metric-benchmark">vs 基准 12.8%</div>
  </div>
  <div class="metric-card variant-green">
    <div class="metric-value">1.68</div>
    <div class="metric-label">夏普比率</div>
    <div class="metric-benchmark">vs 基准 1.42</div>
  </div>
  <div class="metric-card variant-yellow">
    <div class="metric-value">-8.5%</div>
    <div class="metric-label">最大回撤</div>
    <div class="metric-benchmark">vs 基准 -12.3%</div>
  </div>
  <div class="metric-card variant-cyan">
    <div class="metric-value">89.5%</div>
    <div class="metric-label">胜率</div>
    <div class="metric-benchmark">vs 基准 76.2%</div>
  </div>
  <div class="metric-card variant-purple">
    <div class="metric-value">2.85</div>
    <div class="metric-label">卡尔玛比率</div>
    <div class="metric-benchmark">vs 基准 1.93</div>
  </div>
</div>

### 组件卡片变体

<div class="component-grid">
  <div class="component-card variant-blue">
    <h4>🔵 数据采集模块</h4>
    <p>实时获取多源数据，包括市场价格、新闻情绪、宏观指标等核心信息。</p>
  </div>
  <div class="component-card variant-orange">
    <h4>🟠 分析引擎</h4>
    <p>运用机器学习算法进行数据分析，识别市场趋势和交易机会。</p>
  </div>
  <div class="component-card variant-green">
    <h4>🟢 风险管理</h4>
    <p>实时监控投资组合风险，自动调整仓位以控制风险暴露。</p>
  </div>
  <div class="component-card variant-yellow">
    <h4>🟡 决策执行</h4>
    <p>基于分析结果自动生成交易信号，并执行相应的买卖操作。</p>
  </div>
  <div class="component-card variant-cyan">
    <h4>🔷 监控系统</h4>
    <p>7x24小时监控系统运行状态，确保交易策略的稳定执行。</p>
  </div>
  <div class="component-card variant-purple">
    <h4>🟣 报告生成</h4>
    <p>自动生成详细的投资报告，包括收益分析、风险评估等。</p>
  </div>
</div>

### 自动循环颜色演示

<div class="auto-color-cycle">
  <div class="overview-card">
    <div class="card-icon">1️⃣</div>
    <h3>自动蓝色</h3>
    <p>第1个卡片，自动应用蓝色主题</p>
  </div>
  <div class="overview-card">
    <div class="card-icon">2️⃣</div>
    <h3>自动橙色</h3>
    <p>第2个卡片，自动应用橙色主题</p>
  </div>
  <div class="overview-card">
    <div class="card-icon">3️⃣</div>
    <h3>自动绿色</h3>
    <p>第3个卡片，自动应用绿色主题</p>
  </div>
  <div class="overview-card">
    <div class="card-icon">4️⃣</div>
    <h3>自动黄色</h3>
    <p>第4个卡片，自动应用黄色主题</p>
  </div>
  <div class="overview-card">
    <div class="card-icon">5️⃣</div>
    <h3>自动青色</h3>
    <p>第5个卡片，自动应用青色主题</p>
  </div>
  <div class="overview-card">
    <div class="card-icon">6️⃣</div>
    <h3>自动紫色</h3>
    <p>第6个卡片，自动应用紫色主题</p>
  </div>
  <div class="overview-card">
    <div class="card-icon">7️⃣</div>
    <h3>循环蓝色</h3>
    <p>第7个卡片，循环回到蓝色主题</p>
  </div>
  <div class="overview-card">
    <div class="card-icon">8️⃣</div>
    <h3>循环橙色</h3>
    <p>第8个卡片，循环到橙色主题</p>
  </div>
</div>

## 📚 使用说明

### 1. 手动指定颜色变体

为卡片添加颜色变体类：

```html
<!-- 蓝色主题 -->
<div class="overview-card variant-blue">
  <h3>标题</h3>
  <p>内容</p>
</div>

<!-- 橙色主题 -->
<div class="metric-card variant-orange">
  <div class="metric-value">25.8%</div>
  <div class="metric-label">标签</div>
</div>

<!-- 绿色主题 -->
<div class="component-card variant-green">
  <h4>组件标题</h4>
  <p>组件描述</p>
</div>
```

### 2. 自动循环颜色

使用`auto-color-cycle`类让卡片自动循环颜色：

```html
<div class="auto-color-cycle">
  <div class="overview-card">
    <h3>第1个卡片</h3>
    <p>自动应用蓝色</p>
  </div>
  <div class="overview-card">
    <h3>第2个卡片</h3>
    <p>自动应用橙色</p>
  </div>
  <!-- 更多卡片... -->
</div>
```

### 3. 支持的卡片类型

- `overview-card` / `overview-item` - 章节概览卡片
- `metric-card` / `metric-item` - 指标卡片
- `component-card` - 组件卡片
- `strategy-card` - 策略卡片
- `flow-step` - 流程步骤卡片
- `key-points-cards` - 关键要点卡片（需要在容器上添加变体类）

### 4. 可用的颜色变体

- `variant-blue` - 蓝色 (#569cd6)
- `variant-orange` - 橙色 (#ce9178)
- `variant-green` - 绿色 (#6a9955)
- `variant-yellow` - 黄色 (#dcdcaa)
- `variant-cyan` - 青色 (#4ec9b0)
- `variant-purple` - 紫色 (#c586c0)

## 🎨 设计特点

1. **遵循VS Code Dark主题**：使用标准的VS Code暗色主题配色
2. **渐变背景**：每个颜色变体都有微妙的渐变背景效果
3. **左边框突出**：4px的彩色左边框突出显示
4. **响应式设计**：在不同屏幕尺寸下调整边框宽度
5. **暗色模式适配**：自动适配暗色和亮色主题
6. **自动循环**：支持自动循环6种颜色，避免手动分配

## 📊 代码复制功能测试

测试各种编程语言的代码复制功能：

```javascript
// JavaScript 示例
const investmentData = {
  portfolio: [
    { symbol: 'AAPL', weight: 0.15, return: 0.258 },
    { symbol: 'GOOGL', weight: 0.12, return: 0.195 },
    { symbol: 'MSFT', weight: 0.18, return: 0.224 }
  ],
  calculateReturn: function() {
    return this.portfolio.reduce((total, stock) => 
      total + (stock.weight * stock.return), 0
    );
  }
};

console.log(`投资组合年化收益率: ${investmentData.calculateReturn() * 100}%`);
```

```python
# Python 示例
import numpy as np
import pandas as pd

def calculate_portfolio_metrics(returns, weights):
    """计算投资组合指标"""
    portfolio_return = np.sum(returns * weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = portfolio_return / portfolio_volatility
    
    return {
        'return': portfolio_return,
        'volatility': portfolio_volatility,
        'sharpe_ratio': sharpe_ratio
    }

# 示例数据
returns = np.array([0.15, 0.12, 0.18])
weights = np.array([0.4, 0.35, 0.25])
cov_matrix = np.array([[0.04, 0.02, 0.01],
                       [0.02, 0.05, 0.015],
                       [0.01, 0.015, 0.06]])

metrics = calculate_portfolio_metrics(returns, weights)
print(f"投资组合指标: {metrics}")
```

```sql
-- SQL 示例
SELECT 
    stock_symbol,
    AVG(daily_return) as avg_return,
    STDDEV(daily_return) as volatility,
    (AVG(daily_return) / STDDEV(daily_return)) as sharpe_ratio
FROM stock_prices 
WHERE trade_date >= '2023-01-01'
    AND trade_date <= '2023-12-31'
GROUP BY stock_symbol
HAVING COUNT(*) >= 250
ORDER BY sharpe_ratio DESC
LIMIT 10;
```

现在您拥有了丰富的卡片颜色变体系统！🎉 