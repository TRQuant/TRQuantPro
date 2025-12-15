---
title: "A.1 术语表"
description: "深入解析TRQuant系统术语表，包括核心概念、技术术语、业务术语等术语的定义和说明，确保全书术语使用统一"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 📖 A.1 术语表

> **核心摘要：**
> 
> 本节系统介绍TRQuant系统术语表，包括核心概念、技术术语、业务术语等术语的定义和说明。通过理解系统术语定义，帮助用户和开发者更好地理解和使用系统，确保全书术语使用统一。

本术语表定义了TRQuant系统中使用的关键术语，确保全书术语使用统一。术语按类别组织，包括核心概念、技术术语、业务术语等。

## 📋 章节概览

<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}
</script>

<div class="section-overview">
  <div class="section-item" onclick="scrollToSection('section-a-1-1')">
    <h4>🔤 A.1.1 核心概念</h4>
    <p>因子、主线、候选池、策略、回测等核心概念</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-a-1-2')">
    <h4>💻 A.1.2 技术术语</h4>
    <p>API、MCP、RAG、工作流、数据源等技术术语</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-a-1-3')">
    <h4>📊 A.1.3 业务术语</h4>
    <p>市场状态、投资主线、因子库、策略开发等业务术语</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-a-1-4')">
    <h4>📝 A.1.4 命名规范</h4>
    <p>文件命名、章节命名、代码命名等规范</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解核心概念**：掌握系统核心术语和概念定义
- **理解技术术语**：掌握技术相关的术语和定义
- **理解业务术语**：掌握业务相关的术语和定义
- **遵循命名规范**：掌握文件、章节、代码等命名规范

## 📚 核心概念

### 术语分类

- **核心概念**：系统核心术语和概念定义
- **技术术语**：技术相关的术语和定义
- **业务术语**：业务相关的术语和定义
- **命名规范**：文件、章节、代码等命名规范

<h2 id="section-a-1-1">🔤 A.1.1 核心概念</h2>

核心概念定义了TRQuant系统的基础术语。

### 量化投资术语

| 中文 | 英文 | 说明 |
|------|------|------|
| **因子** | Factor | 用于选股或策略的量化指标，如PE、ROE、动量等 |
| **主线** | Mainline | 投资主线，市场趋势方向，如AI、新能源等 |
| **候选池** | Candidate Pool | 策略选股的候选股票池，经过筛选的股票集合 |
| **策略模板** | Strategy Template | 策略的标准化模板，用于快速生成策略代码 |
| **回测** | Backtest | 使用历史数据验证策略的有效性和盈利能力 |
| **优化** | Optimization | 策略参数和因子权重的优化，提升策略表现 |
| **实盘** | Live Trading | 实际交易，与回测相对 |
| **风控** | Risk Control | 风险控制，包括止损、仓位控制等 |

### 系统架构术语

| 中文 | 英文 | 说明 |
|------|------|------|
| **工作流** | Workflow | 完整的投资流程，从数据获取到实盘交易 |
| **编排器** | Orchestrator | 工作流编排器，负责协调各步骤执行 |
| **数据源** | Data Source | 数据来源，如JQData、AKShare等 |
| **知识库** | Knowledge Base | 知识库，包括Manual KB、Engineering KB、Strategy KB |
| **MCP** | Model Context Protocol | 模型上下文协议，用于AI工具集成 |
| **RAG** | Retrieval Augmented Generation | 检索增强生成，用于知识检索和生成 |

<h2 id="section-a-1-2">💻 A.1.2 技术术语</h2>

技术术语定义了系统技术相关的术语。

### 开发技术术语

| 中文 | 英文 | 说明 |
|------|------|------|
| **API** | Application Programming Interface | 应用程序编程接口 |
| **MCP** | Model Context Protocol | 模型上下文协议，用于AI工具集成 |
| **RAG** | Retrieval Augmented Generation | 检索增强生成，用于知识检索和生成 |
| **GUI** | Graphical User Interface | 图形用户界面 |
| **CLI** | Command Line Interface | 命令行界面 |
| **IDE** | Integrated Development Environment | 集成开发环境 |

### 数据技术术语

| 中文 | 英文 | 说明 |
|------|------|------|
| **数据源** | Data Source | 数据来源，如JQData、AKShare等 |
| **数据缓存** | Data Cache | 数据缓存，提升数据获取速度 |
| **数据质量** | Data Quality | 数据质量，包括完整性、准确性等 |
| **时序数据** | Time Series Data | 时间序列数据，如价格、成交量等 |
| **OHLCV** | Open/High/Low/Close/Volume | 开高低收成交量数据 |

### 系统技术术语

| 中文 | 英文 | 说明 |
|------|------|------|
| **工作流** | Workflow | 完整的投资流程，从数据获取到实盘交易 |
| **编排器** | Orchestrator | 工作流编排器，负责协调各步骤执行 |
| **工件** | Artifact | 大输出的指针引用 |
| **追踪ID** | trace_id | 贯穿一次循环的唯一标识 |
| **确认令牌** | confirm_token | 写操作的安全令牌 |
| **证据** | Evidence | 操作记录和审计信息 |
| **dry_run** | dry_run | 模拟执行模式 |
| **execute** | execute | 实际执行模式 |

<h2 id="section-a-1-3">📊 A.1.3 业务术语</h2>

业务术语定义了量化投资业务相关的术语。

### 市场分析术语

| 中文 | 英文 | 说明 |
|------|------|------|
| **市场状态** | Market Regime | 市场状态，如risk_on、risk_off、neutral |
| **市场趋势** | Market Trend | 市场趋势，如上涨、下跌、震荡 |
| **市场阶段** | Market Phase | 市场阶段，如牛市、熊市、震荡、复苏 |
| **风格轮动** | Style Rotation | 风格轮动，如价值、成长、动量等风格的轮动 |

### 投资主线术语

| 中文 | 英文 | 说明 |
|------|------|------|
| **投资主线** | Investment Mainline | 投资主线，市场趋势方向 |
| **主线识别** | Mainline Identification | 投资主线识别，发现市场投资机会 |
| **主线评分** | Mainline Scoring | 投资主线评分，评估主线投资价值 |
| **主线筛选** | Mainline Filtering | 投资主线筛选，选择优质主线 |

### 因子库术语

| 中文 | 英文 | 说明 |
|------|------|------|
| **因子** | Factor | 用于选股或策略的量化指标 |
| **因子库** | Factor Library | 因子库，包含各种量化因子 |
| **因子计算** | Factor Calculation | 因子计算，计算因子值 |
| **因子评估** | Factor Evaluation | 因子评估，评估因子有效性 |
| **因子优化** | Factor Optimization | 因子优化，优化因子参数和权重 |

### 策略开发术语

| 中文 | 英文 | 说明 |
|------|------|------|
| **策略** | Strategy | 量化交易策略 |
| **策略生成** | Strategy Generation | 策略生成，自动生成策略代码 |
| **策略测试** | Strategy Testing | 策略测试，测试策略有效性 |
| **策略优化** | Strategy Optimization | 策略优化，优化策略参数 |
| **策略部署** | Strategy Deployment | 策略部署，部署到实盘 |

### 回测验证术语

| 中文 | 英文 | 说明 |
|------|------|------|
| **回测** | Backtest | 使用历史数据验证策略 |
| **回测引擎** | Backtest Engine | 回测引擎，执行回测计算 |
| **回测结果** | Backtest Result | 回测结果，包括收益、风险等指标 |
| **回测报告** | Backtest Report | 回测报告，详细的回测分析报告 |

<h2 id="section-a-1-4">📝 A.1.4 命名规范</h2>

命名规范定义了系统文件、章节、代码等的命名规则。

### 文件命名

#### 章节文件

- **格式**：`XXX_ChapterX_XXX_CN.md`
- **示例**：`001_Chapter1_System_Overview_CN.md`
- **说明**：
  - `XXX`：章节编号（001-013）
  - `ChapterX`：章节名称（Chapter1-Chapter13）
  - `XXX`：章节标题（System_Overview等）
  - `CN`：语言标识（CN表示中文）

#### 小节文件

- **格式**：`X.Y_XXX_CN.md`
- **示例**：`1.1_System_Architecture_CN.md`
- **说明**：
  - `X.Y`：小节编号（1.1、1.2等）
  - `XXX`：小节标题
  - `CN`：语言标识

### 章节命名

#### 主章节

- **格式**：`第X章：XXX`
- **示例**：`第1章：系统概述`
- **说明**：使用中文数字和冒号

#### 小节

- **格式**：`X.Y XXX`
- **示例**：`1.1 系统架构`
- **说明**：使用数字编号和空格

### 代码命名

#### Python代码

- **类名**：PascalCase（如 `DataSourceManager`）
- **函数名**：snake_case（如 `get_price`）
- **常量**：UPPER_SNAKE_CASE（如 `MAX_RETRY_COUNT`）
- **私有成员**：下划线前缀（如 `_internal_state`）

#### TypeScript代码

- **类名**：PascalCase（如 `TRQuantClient`）
- **函数名**：camelCase（如 `getPrice`）
- **常量**：UPPER_SNAKE_CASE（如 `MAX_RETRY_COUNT`）
- **私有成员**：下划线前缀（如 `_internalState`）

### 数据库命名

- **表名**：snake_case（如 `market_trend`）
- **字段名**：snake_case（如 `start_date`）
- **索引名**：`idx_表名_字段名`（如 `idx_market_trend_date`）

## 🔗 相关章节

- **第1章：系统概述**：了解系统整体架构和核心概念
- **第2-8章**：了解各模块的详细功能和术语
- **第12章：API参考**：了解API接口的命名规范

## 💡 关键要点

1. **术语统一**：全书术语使用统一，确保一致性
2. **中英文对照**：提供中英文对照，便于理解
3. **分类清晰**：术语按类别组织，便于查找
4. **命名规范**：遵循统一的命名规范，便于维护

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了系统术语表，包括核心概念、技术术语、业务术语等术语的定义和说明。通过理解系统术语定义，帮助用户和开发者更好地理解和使用系统。</p>
  
  <h3>下节预告</h3>
  <p>掌握了术语表后，下一节将介绍更新日志，详细说明系统版本更新历史、功能更新、Bug修复等。通过理解更新日志，帮助用户和开发者了解系统演进历程。</p>
  
  <a href="/ashare-book6/013_Appendix/A.2_Changelog_CN" class="next-section">
    继续学习：A.2 更新日志 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
