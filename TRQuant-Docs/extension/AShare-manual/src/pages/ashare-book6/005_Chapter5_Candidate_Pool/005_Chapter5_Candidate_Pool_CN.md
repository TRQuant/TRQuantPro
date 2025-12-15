---
title: "第5章：候选池构建"
description: "深入解析候选池构建模块，包括股票池管理、筛选规则引擎、股票评分系统和候选池构建器，为量化投资系统提供可交易的股票候选池"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 📦 第5章：候选池构建

> **核心摘要：**
> 
> 本章系统介绍TRQuant系统的候选池构建模块设计，包括股票池管理、筛选规则引擎、股票评分系统和候选池构建器。通过理解股票池的创建、更新、维护机制，筛选规则的配置、组合、执行逻辑，股票评分的多因子评分、综合评分计算，以及候选池的构建流程和三层数据保障架构，帮助开发者掌握候选池构建的核心实现，为构建高效可靠的股票候选池系统奠定基础。

## 📖 本章学习路径

按照以下顺序学习，构建完整的候选池构建模块认知：

<div class="chapters-grid">
  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">5.1</span>
      <h3>股票池管理</h3>
    </div>
    <p>深入了解股票池的创建、更新、维护机制和三层数据保障架构，理解股票池管理的核心技术。</p>
    <div class="chapter-features">
      <span class="feature-tag">📊 股票池创建</span>
      <span class="feature-tag">🔄 数据保障</span>
      <span class="feature-tag">⚡ 三层架构</span>
    </div>
    <a href="/ashare-book6/005_Chapter5_Candidate_Pool/5.1_Stock_Pool_Management_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">5.2</span>
      <h3>筛选规则</h3>
    </div>
    <p>系统讲解基础筛选、主线筛选、行业筛选、技术筛选和规则组合逻辑，掌握筛选规则引擎。</p>
    <div class="chapter-features">
      <span class="feature-tag">🔍 基础筛选</span>
      <span class="feature-tag">🔥 主线筛选</span>
      <span class="feature-tag">🔗 规则组合</span>
    </div>
    <a href="/ashare-book6/005_Chapter5_Candidate_Pool/5.2_Filtering_Rules_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">5.3</span>
      <h3>股票评分</h3>
    </div>
    <p>详细介绍多因子评分、综合评分计算和评分排序方法，理解股票评分系统的实现。</p>
    <div class="chapter-features">
      <span class="feature-tag">📈 多因子评分</span>
      <span class="feature-tag">⚖️ 综合评分</span>
      <span class="feature-tag">🔢 评分排序</span>
    </div>
    <a href="/ashare-book6/005_Chapter5_Candidate_Pool/5.3_Stock_Scoring_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">5.4</span>
      <h3>MCP工具集成</h3>
    </div>
    <p>掌握候选池构建相关的MCP工具使用，包括知识库查询、数据收集工具等。</p>
    <div class="chapter-features">
      <span class="feature-tag">🔍 知识库查询</span>
      <span class="feature-tag">📥 数据收集</span>
      <span class="feature-tag">🛠️ 工具集成</span>
    </div>
    <a href="/ashare-book6/005_Chapter5_Candidate_Pool/5.4_MCP_Tool_Integration_CN" class="chapter-link">开始学习 →</a>
  </div>
</div>

## 🎯 学习目标

通过本章学习，您将能够：

- **掌握股票池管理**：理解股票池的创建、更新、维护机制和三层数据保障架构
- **理解筛选规则**：掌握基础筛选、主线筛选、行业筛选、技术筛选的规则配置和执行
- **熟悉股票评分**：理解多因子评分、综合评分计算和评分排序方法
- **使用MCP工具**：掌握使用MCP工具进行候选池构建相关研究

## 📚 核心概念

### 股票池管理

- **股票池类型**：基础股票池（全市场、行业）、自定义股票池、动态股票池
- **三层数据保障**：优先使用实时API → API失败时使用缓存 → 缓存失败时使用Fallback策略
- **股票池维护**：股票池合并、拆分、清理、验证
- **股票池更新**：定时更新、事件触发更新、增量更新

### 筛选规则引擎

- **基础筛选规则**：ST、停牌、涨跌停过滤、流动性筛选
- **主线筛选规则**：基于投资主线的行业匹配、龙头股筛选
- **行业筛选规则**：行业分类、行业权重、行业轮动
- **技术筛选规则**：技术突破、价格趋势、成交量配合
- **规则组合**：逻辑组合（AND、OR、NOT）、优先级设置、规则权重

### 股票评分系统

- **多因子评分**：基本面因子、技术面因子、资金面因子、情绪面因子
- **综合评分**：加权平均、综合得分计算
- **评分排序**：按综合得分排序、按因子得分排序

### MCP工具集成

- **kb.query**：查询知识库，获取候选池构建相关的文档和代码
- **data_collector**：收集候选池构建相关的数据和研究资料

<h2 id="section-5-1">📊 5.1 股票池管理</h2>

股票池管理是候选池构建模块的核心功能，负责管理多个股票池，包括股票池的创建、更新、维护等功能。

### 模块定位

- **工作流位置**：步骤4 - 📦 候选池构建
- **核心职责**：股票池创建、更新、维护
- **服务对象**：筛选规则引擎、候选池构建器

详细内容请参考：[5.1 股票池管理](5.1_Stock_Pool_Management_CN.md)

<h2 id="section-5-2">🔍 5.2 筛选规则</h2>

筛选规则是候选池构建模块的重要功能，负责根据投资主线、市场条件等设置筛选规则，从股票池中筛选出符合条件的候选股票。

### 模块定位

- **工作流位置**：步骤4 - 📦 候选池构建
- **核心职责**：筛选规则配置、规则执行、结果验证
- **服务对象**：候选池构建器、股票评分系统

详细内容请参考：[5.2 筛选规则](5.2_Filtering_Rules_CN.md)

详细内容请参考：[5.3 股票评分](5.3_Stock_Scoring_CN.md)

详细内容请参考：[5.4 MCP工具集成](5.4_MCP_Tool_Integration_CN.md)

## 🔗 相关章节

- **第1章：系统概述** - 了解系统整体架构和设计理念
- **第2章：数据源模块** - 了解数据获取机制，为候选池构建提供数据支撑
- **第3章：市场分析模块** - 市场分析结果用于筛选条件调整
- **第4章：投资主线识别** - 主线识别结果用于候选池构建
- **第6章：因子库** - 候选池用于因子计算
- **第7章：策略开发** - 候选池用于策略生成
- **第8章：回测验证** - 候选池用于回测验证
- **第10章：开发指南** - 了解候选池构建模块的开发规范

---

<div class="chapter-navigation">
  <div class="nav-item prev">
    <span class="nav-label">上一章</span>
    <a href="../004_Chapter4_Mainline_Identification/004_Chapter4_Mainline_Identification_CN.md">🔥 第4章：投资主线识别</a>
  </div>
  <div class="nav-item next">
    <span class="nav-label">下一章</span>
    <a href="../006_Chapter6_Factor_Library/006_Chapter6_Factor_Library_CN.md">📊 第6章：因子库</a>
  </div>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
