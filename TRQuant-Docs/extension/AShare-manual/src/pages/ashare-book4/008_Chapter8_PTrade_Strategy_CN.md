---
title: "第八章：PTrade策略开发"
description: "系统学习PTrade量化交易平台的策略开发方法"
lang: "zh-CN"
layout: "/src/layouts/Layout.astro"
currentBook: "ashare-quantitative"
updateDate: "2025-01-26"
---

# 第八章：PTrade策略开发

> **核心摘要：**
> 
> PTrade是国金证券提供的专业量化交易平台，支持Python策略开发和实盘交易。本章系统讲解PTrade平台的使用方法、策略框架、回测系统和实盘部署，帮助投资者将多因子模型转化为可实盘交易的策略。

## 📖 本章学习路径

<div class="chapters-grid">
  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">8.1</span>
      <h3>PTrade平台概述</h3>
    </div>
    <p>了解PTrade平台的功能特点和使用环境。</p>
    <a href="/ashare-book4/008_Chapter8/8.1_PTrade_Overview_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">8.2</span>
      <h3>策略框架</h3>
    </div>
    <p>掌握PTrade策略的基本框架和生命周期函数。</p>
    <a href="/ashare-book4/008_Chapter8/8.2_Strategy_Framework_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">8.3</span>
      <h3>数据获取</h3>
    </div>
    <p>学习PTrade中的行情数据和财务数据获取方法。</p>
    <a href="/ashare-book4/008_Chapter8/8.3_Data_Access_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">8.4</span>
      <h3>交易执行</h3>
    </div>
    <p>掌握PTrade的下单、撤单、持仓管理等交易功能。</p>
    <a href="/ashare-book4/008_Chapter8/8.4_Trade_Execution_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">8.5</span>
      <h3>多因子策略实现</h3>
    </div>
    <p>将多因子模型转化为PTrade策略代码。</p>
    <a href="/ashare-book4/008_Chapter8/8.5_Multi_Factor_Strategy_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">8.6</span>
      <h3>实盘部署</h3>
    </div>
    <p>学习PTrade策略的回测、模拟和实盘部署流程。</p>
    <a href="/ashare-book4/008_Chapter8/8.6_Live_Deployment_CN" class="chapter-link">开始学习 →</a>
  </div>
</div>

## 🎯 学习目标

- **掌握PTrade平台**：熟悉PTrade的功能和使用方法
- **理解策略框架**：掌握PTrade策略的生命周期和事件驱动机制
- **实现多因子策略**：将多因子模型转化为可执行的策略代码
- **完成实盘部署**：从回测到实盘的完整流程

## 📚 核心概念

<div class="tip-box">
  <h4>📖 PTrade平台特点</h4>
  <ul>
    <li><strong>Python支持：</strong>使用Python编写策略</li>
    <li><strong>事件驱动：</strong>基于事件的策略执行机制</li>
    <li><strong>回测系统：</strong>内置历史回测功能</li>
    <li><strong>实盘交易：</strong>支持真实资金交易</li>
    <li><strong>国金证券：</strong>需要国金证券账户</li>
  </ul>
</div>

---

**下一章：** [第九章：QMT策略开发 →](/ashare-book4/009_Chapter9_QMT_Strategy_CN)
