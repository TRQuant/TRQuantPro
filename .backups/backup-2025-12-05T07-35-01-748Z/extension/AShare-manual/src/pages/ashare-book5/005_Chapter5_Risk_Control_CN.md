---
title: "第五章：风险控制系统"
description: "学习设计和实施风险控制系统"
lang: "zh-CN"
layout: "/src/layouts/Layout.astro"
currentBook: "ashare-trading"
updateDate: "2025-01-26"
---

# 第五章：风险控制系统

> **核心摘要：**
> 
> 本章介绍量化策略的风险控制系统设计。

## 📖 本章要点

### 三层风控体系

<div class="exchange-grid">
  <div class="exchange-card">
    <div class="exchange-header">
      <span class="exchange-icon">🛡️</span>
      <h3>事前风控</h3>
    </div>
    <div class="exchange-content">
      <p><strong>内容：</strong>仓位限制、单股限制</p>
      <p><strong>时机：</strong>下单前检查</p>
    </div>
  </div>

  <div class="exchange-card">
    <div class="exchange-header">
      <span class="exchange-icon">⚡</span>
      <h3>事中风控</h3>
    </div>
    <div class="exchange-content">
      <p><strong>内容：</strong>实时监控、异常报警</p>
      <p><strong>时机：</strong>交易过程中</p>
    </div>
  </div>

  <div class="exchange-card">
    <div class="exchange-header">
      <span class="exchange-icon">📊</span>
      <h3>事后风控</h3>
    </div>
    <div class="exchange-content">
      <p><strong>内容：</strong>日终检查、风险报告</p>
      <p><strong>时机：</strong>交易结束后</p>
    </div>
  </div>
</div>

### 风控参数设置

<div class="comparison-table">
  <table>
    <thead>
      <tr>
        <th>参数</th>
        <th>说明</th>
        <th>建议值</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>最大仓位</strong></td>
        <td>总仓位上限</td>
        <td>80%</td>
      </tr>
      <tr>
        <td><strong>单股上限</strong></td>
        <td>单只股票仓位</td>
        <td>10%</td>
      </tr>
      <tr>
        <td><strong>日亏损限制</strong></td>
        <td>单日最大亏损</td>
        <td>3%</td>
      </tr>
      <tr>
        <td><strong>止损线</strong></td>
        <td>单股止损</td>
        <td>-8%</td>
      </tr>
    </tbody>
  </table>
</div>

## 💎 核心要点总结

<div class="key-points">
  <div class="key-point">
    <h4>🛡️ 风控是生命线</h4>
    <p>没有风控的策略是赌博</p>
  </div>
  <div class="key-point">
    <h4>📊 三层防护</h4>
    <p>事前、事中、事后全方位风控</p>
  </div>
</div>

---

**下一章：** [PTrade实盘对接 →](/ashare-book5/006_Chapter6_PTrade_Live_CN)
