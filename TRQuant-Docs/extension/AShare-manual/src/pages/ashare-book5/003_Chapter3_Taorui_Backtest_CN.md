---
title: "第三章：韬睿回测引擎"
description: "学习使用韬睿量化平台的回测功能"
lang: "zh-CN"
layout: "/src/layouts/Layout.astro"
currentBook: "ashare-trading"
updateDate: "2025-01-26"
---

# 第三章：韬睿回测引擎

> **核心摘要：**
> 
> 本章介绍韬睿量化平台的回测引擎使用方法。

## 📖 本章要点

### 回测引擎特点

<div class="board-details">
  <div class="board-card">
    <h4>⚡ 高性能</h4>
    <div class="board-content">
      <p>优化的回测引擎，支持大规模数据回测</p>
    </div>
  </div>

  <div class="board-card">
    <h4>📊 丰富指标</h4>
    <div class="board-content">
      <p>自动计算夏普、回撤、胜率等指标</p>
    </div>
  </div>

  <div class="board-card">
    <h4>📈 可视化</h4>
    <div class="board-content">
      <p>净值曲线、持仓分布等图表展示</p>
    </div>
  </div>

  <div class="board-card">
    <h4>🔗 Cursor集成</h4>
    <div class="board-content">
      <p>回测结果可被Cursor读取，用于策略迭代</p>
    </div>
  </div>
</div>

### 回测配置参数

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
        <td><strong>初始资金</strong></td>
        <td>回测起始资金</td>
        <td>100万</td>
      </tr>
      <tr>
        <td><strong>佣金率</strong></td>
        <td>交易佣金</td>
        <td>万分之2.5</td>
      </tr>
      <tr>
        <td><strong>印花税</strong></td>
        <td>卖出印花税</td>
        <td>千分之1</td>
      </tr>
      <tr>
        <td><strong>滑点</strong></td>
        <td>成交价偏差</td>
        <td>0.1%</td>
      </tr>
    </tbody>
  </table>
</div>

## 💎 核心要点总结

<div class="key-points">
  <div class="key-point">
    <h4>📊 参数要合理</h4>
    <p>设置合理的成本参数，避免高估收益</p>
  </div>
  <div class="key-point">
    <h4>🔗 与Cursor联动</h4>
    <p>回测结果可用于AI辅助策略优化</p>
  </div>
</div>

---

**下一章：** [回测报告解读 →](/ashare-book5/004_Chapter4_Report_Analysis_CN)
