---
title: "第七章：QMT实盘对接"
description: "学习将策略部署到QMT实盘"
lang: "zh-CN"
layout: "/src/layouts/Layout.astro"
currentBook: "ashare-trading"
updateDate: "2025-01-26"
---

# 第七章：QMT实盘对接

> **核心摘要：**
> 
> 本章介绍如何将策略部署到QMT平台进行实盘交易。

## 📖 本章要点

### QMT实盘特点

<div class="board-details">
  <div class="board-card">
    <h4>🏦 多券商支持</h4>
    <div class="board-content">
      <p>支持多家券商的QMT接口</p>
    </div>
  </div>

  <div class="board-card">
    <h4>📊 miniQMT</h4>
    <div class="board-content">
      <p>轻量级版本，适合个人投资者</p>
    </div>
  </div>

  <div class="board-card">
    <h4>⚡ 实时交易</h4>
    <div class="board-content">
      <p>支持实时行情和交易</p>
    </div>
  </div>
</div>

### xtquant实盘代码

```python
from xtquant import xtdata
from xtquant.xttrader import XtQuantTrader

# 创建交易对象
trader = XtQuantTrader(path, session_id)

# 连接交易服务器
trader.start()

# 下单
order_id = trader.order_stock(
    account_id,
    stock_code,
    xtconstant.STOCK_BUY,
    volume,
    xtconstant.FIX_PRICE,
    price
)
```

## 💎 核心要点总结

<div class="key-points">
  <div class="key-point">
    <h4>📊 xtquant是核心</h4>
    <p>掌握xtquant库是QMT实盘的基础</p>
  </div>
  <div class="key-point">
    <h4>🔄 与韬睿平台集成</h4>
    <p>通过QMT Bridge实现数据同步</p>
  </div>
</div>

---

**下一章：** [策略迭代与优化 →](/ashare-book5/008_Chapter8_Strategy_Iteration_CN)
