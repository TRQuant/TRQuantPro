---
title: "第六章：PTrade实盘对接"
description: "学习将策略部署到PTrade实盘"
lang: "zh-CN"
layout: "/src/layouts/Layout.astro"
currentBook: "ashare-trading"
updateDate: "2025-01-26"
---

# 第六章：PTrade实盘对接

> **核心摘要：**
> 
> 本章介绍如何将策略部署到国金证券PTrade平台进行实盘交易。

## 📖 本章要点

### PTrade实盘流程

<div class="process-flow">
  <div class="process-step">
    <h4>1. 策略开发</h4>
    <p>Cursor生成</p>
  </div>
  <span class="process-arrow">→</span>
  <div class="process-step">
    <h4>2. 回测验证</h4>
    <p>韬睿回测</p>
  </div>
  <span class="process-arrow">→</span>
  <div class="process-step">
    <h4>3. 策略同步</h4>
    <p>PTrade Bridge</p>
  </div>
  <span class="process-arrow">→</span>
  <div class="process-step">
    <h4>4. 模拟交易</h4>
    <p>PTrade模拟</p>
  </div>
  <span class="process-arrow">→</span>
  <div class="process-step">
    <h4>5. 实盘交易</h4>
    <p>PTrade实盘</p>
  </div>
</div>

### PTrade Bridge功能

<div class="board-details">
  <div class="board-card">
    <h4>🔗 策略同步</h4>
    <div class="board-content">
      <p>将本地策略同步到PTrade平台</p>
    </div>
  </div>

  <div class="board-card">
    <h4>📊 数据回传</h4>
    <div class="board-content">
      <p>获取PTrade回测和交易数据</p>
    </div>
  </div>

  <div class="board-card">
    <h4>🔄 状态监控</h4>
    <div class="board-content">
      <p>监控策略运行状态</p>
    </div>
  </div>
</div>

## 💎 核心要点总结

<div class="key-points">
  <div class="key-point">
    <h4>🔗 Bridge是桥梁</h4>
    <p>PTrade Bridge连接韬睿平台和PTrade</p>
  </div>
  <div class="key-point">
    <h4>⚠️ 先模拟后实盘</h4>
    <p>务必先在模拟环境验证策略</p>
  </div>
</div>

---

**下一章：** [QMT实盘对接 →](/ashare-book5/007_Chapter7_QMT_Live_CN)
