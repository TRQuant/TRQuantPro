---
title: "第一章：策略回测基础"
description: "理解回测原理和常见陷阱"
lang: "zh-CN"
layout: "/src/layouts/Layout.astro"
currentBook: "ashare-trading"
updateDate: "2025-01-26"
---

# 第一章：策略回测基础

> **核心摘要：**
> 
> 本章介绍策略回测的基本原理和常见陷阱，帮助投资者正确进行回测。

## 📖 本章要点

### 回测的基本原理

<div class="tip-box">
  <h4>📊 回测定义</h4>
  <p>回测是指使用历史数据模拟策略的执行过程，评估策略在过去的表现，从而推断其未来可能的表现。</p>
</div>

### 常见回测陷阱

<div class="exchange-grid">
  <div class="exchange-card">
    <div class="exchange-header">
      <span class="exchange-icon">👀</span>
      <h3>未来函数</h3>
    </div>
    <div class="exchange-content">
      <p><strong>问题：</strong>使用了未来才知道的数据</p>
      <p><strong>例如：</strong>用当日收盘价决定当日买入</p>
      <p><strong>解决：</strong>严格使用T-1数据</p>
    </div>
  </div>

  <div class="exchange-card">
    <div class="exchange-header">
      <span class="exchange-icon">📈</span>
      <h3>过拟合</h3>
    </div>
    <div class="exchange-content">
      <p><strong>问题：</strong>过度优化参数</p>
      <p><strong>表现：</strong>回测好，实盘差</p>
      <p><strong>解决：</strong>样本外测试</p>
    </div>
  </div>

  <div class="exchange-card">
    <div class="exchange-header">
      <span class="exchange-icon">💰</span>
      <h3>忽略成本</h3>
    </div>
    <div class="exchange-content">
      <p><strong>问题：</strong>未考虑交易成本</p>
      <p><strong>包括：</strong>佣金、印花税、滑点</p>
      <p><strong>解决：</strong>设置合理成本参数</p>
    </div>
  </div>

  <div class="exchange-card">
    <div class="exchange-header">
      <span class="exchange-icon">📊</span>
      <h3>幸存者偏差</h3>
    </div>
    <div class="exchange-content">
      <p><strong>问题：</strong>只用存活股票</p>
      <p><strong>影响：</strong>高估策略表现</p>
      <p><strong>解决：</strong>使用全量历史数据</p>
    </div>
  </div>
</div>

## 💎 核心要点总结

<div class="key-points">
  <div class="key-point">
    <h4>⚠️ 回测不等于实盘</h4>
    <p>回测好不代表实盘好，要保持谨慎</p>
  </div>
  <div class="key-point">
    <h4>📊 避免常见陷阱</h4>
    <p>未来函数、过拟合、忽略成本是最常见的问题</p>
  </div>
  <div class="key-point">
    <h4>🔄 样本外验证</h4>
    <p>必须保留样本外数据进行验证</p>
  </div>
</div>

---

**下一章：** [JQData数据接入 →](/ashare-book5/002_Chapter2_JQData_Integration_CN)
