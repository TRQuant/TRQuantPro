---
title: "第二章：JQData数据接入"
description: "学习使用JQData获取A股数据"
lang: "zh-CN"
layout: "/src/layouts/Layout.astro"
currentBook: "ashare-trading"
updateDate: "2025-01-26"
---

# 第二章：JQData数据接入

> **核心摘要：**
> 
> 本章介绍如何使用JQData获取A股行情、财务等数据。

## 📖 本章要点

### JQData简介

<div class="tip-box">
  <h4>📊 JQData特点</h4>
  <ul>
    <li><strong>数据全面：</strong>涵盖行情、财务、因子等</li>
    <li><strong>接口简单：</strong>Python API易于使用</li>
    <li><strong>韬睿集成：</strong>韬睿平台默认数据源</li>
  </ul>
</div>

### 常用数据接口

```python
import jqdatasdk as jq

# 认证
jq.auth('账号', '密码')

# 获取行情数据
df = jq.get_price('000001.XSHE', 
                  start_date='2024-01-01',
                  end_date='2024-12-31',
                  frequency='daily')

# 获取财务数据
df = jq.get_fundamentals(
    jq.query(jq.valuation.pe_ratio),
    date='2024-12-31'
)

# 获取指数成分
stocks = jq.get_index_stocks('000300.XSHG')
```

### 数据处理流程

<div class="process-flow">
  <div class="process-step">
    <h4>获取数据</h4>
    <p>JQData API</p>
  </div>
  <span class="process-arrow">→</span>
  <div class="process-step">
    <h4>数据清洗</h4>
    <p>缺失值处理</p>
  </div>
  <span class="process-arrow">→</span>
  <div class="process-step">
    <h4>数据存储</h4>
    <p>本地缓存</p>
  </div>
  <span class="process-arrow">→</span>
  <div class="process-step">
    <h4>数据使用</h4>
    <p>策略回测</p>
  </div>
</div>

## 💎 核心要点总结

<div class="key-points">
  <div class="key-point">
    <h4>📊 JQData是基础</h4>
    <p>JQData是韬睿平台的默认数据源</p>
  </div>
  <div class="key-point">
    <h4>💾 本地缓存很重要</h4>
    <p>缓存数据可以加速回测，节省API调用</p>
  </div>
</div>

---

**下一章：** [韬睿回测引擎 →](/ashare-book5/003_Chapter3_Taorui_Backtest_CN)
