---
title: "第4章：投资主线识别"
description: "深入解析投资主线识别模块，包括主线识别引擎、多维度评分系统、主线筛选机制和LLM综合分析，为量化投资系统提供投资方向指引"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 🔥 第4章：投资主线识别

> **核心摘要：**
> 
> 本章系统介绍TRQuant系统的投资主线识别模块设计，包括主线识别引擎、多维度评分系统、主线筛选机制和LLM综合分析。通过理解三层分析框架（宏观前瞻→中观验证→微观确认）、六维度评分体系（政策支持度、资金认可度、产业景气度、技术形态度、估值合理度、前瞻领先度）、主线生命周期管理和筛选算法，帮助开发者掌握投资主线识别的核心实现，为构建智能化的投资方向识别系统奠定基础。

## 📖 本章学习路径

按照以下顺序学习，构建完整的投资主线识别模块认知：

<div class="chapters-grid">
  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">4.1</span>
      <h3>主线评分</h3>
    </div>
    <p>深入了解六维度评分体系、因子评分方法和综合评分计算，理解投资主线评分的核心技术。</p>
    <div class="chapter-features">
      <span class="feature-tag">📊 六维度评分</span>
      <span class="feature-tag">🔢 因子评分</span>
      <span class="feature-tag">⭐ 综合评分</span>
    </div>
    <a href="/ashare-book6/004_Chapter4_Mainline_Identification/4.1_Mainline_Scoring_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">4.2</span>
      <h3>主线筛选</h3>
    </div>
    <p>系统讲解评分筛选、行业筛选、时间筛选的算法和实现，掌握主线筛选的核心技术。</p>
    <div class="chapter-features">
      <span class="feature-tag">🔍 评分筛选</span>
      <span class="feature-tag">🏭 行业筛选</span>
      <span class="feature-tag">⏰ 时间筛选</span>
    </div>
    <a href="/ashare-book6/004_Chapter4_Mainline_Identification/4.2_Mainline_Filtering_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">4.3</span>
      <h3>主线识别引擎</h3>
    </div>
    <p>详细介绍三层分析框架、主线发现流程和生命周期管理，理解主线识别的完整机制。</p>
    <div class="chapter-features">
      <span class="feature-tag">🏗️ 三层框架</span>
      <span class="feature-tag">🔄 发现流程</span>
      <span class="feature-tag">📈 生命周期</span>
    </div>
    <a href="/ashare-book6/004_Chapter4_Mainline_Identification/4.3_Mainline_Engine_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">4.4</span>
      <h3>MCP工具集成</h3>
    </div>
    <p>掌握投资主线识别相关的MCP工具使用，包括trquant_mainlines工具、知识库查询等。</p>
    <div class="chapter-features">
      <span class="feature-tag">🔍 知识库查询</span>
      <span class="feature-tag">📥 数据收集</span>
      <span class="feature-tag">🛠️ 工具集成</span>
    </div>
    <a href="/ashare-book6/004_Chapter4_Mainline_Identification/4.4_MCP_Tool_Integration_CN" class="chapter-link">开始学习 →</a>
  </div>
</div>

## 🎯 学习目标

通过本章学习，您将能够：

- **掌握主线评分**：理解六维度评分体系、因子评分方法和综合评分计算
- **理解主线筛选**：掌握评分筛选、行业筛选、时间筛选的算法和实现
- **熟悉识别引擎**：理解三层分析框架、主线发现流程和生命周期管理
- **使用MCP工具**：掌握使用trquant_mainlines等MCP工具获取投资主线

## 📚 核心概念

### 主线识别引擎

- **三层分析框架**：宏观前瞻（6-12个月）→ 中观验证（1-3个月）→ 微观确认（1-4周）
- **主线类型**：政策驱动型、产业趋势型、事件驱动型、周期轮动型、主题概念型
- **生命周期阶段**：启动期（emerging）、成长期（growing）、成熟期（mature）、衰退期（declining）
- **主线发现流程**：宏观前瞻分析 → 中观验证 → 综合生成主线 → 过滤 → 排序

### 六维度评分体系

- **政策支持度（Policy）**：政策提及频率、政策支持力度、政策持续性、政策落地进度
- **资金认可度（Capital）**：北向资金净流入、主力资金净流入、机构持仓变化、两融余额变化、行业ETF资金流入
- **产业景气度（Industry）**：营收增长、利润增长、订单积压、产能利用率、价格趋势
- **技术形态度（Technical）**：趋势强度、均线排列、量价配合、突破信号、RSI/MACD
- **估值合理度（Valuation）**：PE分位数、PB分位数、PEG比率、股息率
- **前瞻领先度（Foresight）**：领先指标、催化剂密度、一致预期修正、全球趋势

### 主线筛选机制

- **评分筛选**：最低评分阈值、评分排名、评分区间
- **行业筛选**：行业分类、行业权重、行业轮动
- **时间筛选**：时间窗口、时间持续性、时间趋势
- **综合筛选**：多条件组合筛选、智能筛选规则

### MCP工具集成

- **trquant_mainlines**：获取当前A股市场的投资主线（主线名称、评分、相关行业、投资逻辑）
- **kb.query**：查询知识库，获取主线识别相关的文档和代码
- **data_collector**：收集主线识别相关的数据和研究资料

<h2 id="section-4-1">📊 4.1 主线评分</h2>

主线评分是投资主线识别模块的核心功能，负责对识别出的投资主线进行多维度评分，为主线筛选和排序提供依据。

### 模块定位

- **工作流位置**：步骤3 - 🔥 投资主线
- **核心职责**：多维度评分、综合评分计算、评分排序
- **服务对象**：主线筛选、候选池构建、因子推荐、策略生成

详细内容请参考：[4.1 主线评分](4.1_Mainline_Scoring_CN.md)

<h2 id="section-4-2">🔍 4.2 主线筛选</h2>

主线筛选是投资主线识别模块的重要功能，负责根据评分、行业、时间等条件筛选出符合条件的投资主线。

### 模块定位

- **工作流位置**：步骤3 - 🔥 投资主线
- **核心职责**：评分筛选、行业筛选、时间筛选
- **服务对象**：候选池构建、因子推荐、策略生成

详细内容请参考：[4.2 主线筛选](4.2_Mainline_Filtering_CN.md)

详细内容请参考：[4.3 主线识别引擎](4.3_Mainline_Engine_CN.md)

详细内容请参考：[4.4 MCP工具集成](4.4_MCP_Tool_Integration_CN.md)

## 🔗 相关章节

- **第1章：系统概述** - 了解系统整体架构和设计理念
- **第2章：数据源模块** - 了解数据获取机制，为主线识别提供数据支撑
- **第3章：市场分析模块** - 市场分析结果用于主线识别
- **第5章：候选池构建** - 主线识别结果用于候选池构建
- **第6章：因子库** - 主线识别结果用于因子推荐
- **第7章：策略开发** - 主线识别结果用于策略生成
- **第8章：回测验证** - 主线识别结果用于回测环境设置
- **第10章：开发指南** - 了解主线识别模块的开发规范

---

<div class="chapter-navigation">
  <div class="nav-item prev">
    <span class="nav-label">上一章</span>
    <a href="../003_Chapter3_Market_Analysis/003_Chapter3_Market_Analysis_CN.md">📈 第3章：市场分析</a>
  </div>
  <div class="nav-item next">
    <span class="nav-label">下一章</span>
    <a href="../005_Chapter5_Candidate_Pool/005_Chapter5_Candidate_Pool_CN.md">📦 第5章：候选池构建</a>
  </div>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
