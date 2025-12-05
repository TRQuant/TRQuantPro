---
title: "第二章：价值因子构建"
description: "系统学习PE、PB、PS、股息率等经典价值因子的定义、计算、回测和A股应用"
lang: "zh-CN"
layout: "/src/layouts/Layout.astro"
currentBook: "ashare-quantitative"
updateDate: "2025-01-26"
---

# 第二章：价值因子构建

> **核心摘要：**
> 
> 价值因子是量化投资最经典、最持久的因子类别，源于格雷厄姆的价值投资理念。本章系统讲解PE、PB、PS、股息率等经典价值因子的定义、计算方法、A股有效性验证和实战应用，帮助投资者构建科学的价值评估体系。本章内容与第一册第五章（基本面分析）形成呼应，将主观的估值分析转化为可量化、可回测的因子模型。

## 📖 本章学习路径

按照以下顺序学习，构建完整的价值因子体系：

<div class="chapters-grid">
  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">2.1</span>
      <h3>价值因子概述</h3>
    </div>
    <p>理解价值因子的理论基础、经济学逻辑和A股有效性，掌握价值投资与量化的结合方式。</p>
    <div class="chapter-features">
      <span class="feature-tag">📚 理论基础</span>
      <span class="feature-tag">💡 经济逻辑</span>
      <span class="feature-tag">📊 A股验证</span>
    </div>
    <a href="/ashare-book4/002_Chapter2/2.1_Value_Overview_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">2.2</span>
      <h3>市盈率因子（PE）</h3>
    </div>
    <p>深入学习PE因子的多种计算方式（TTM、静态、动态），A股PE因子的特点和应用技巧。</p>
    <div class="chapter-features">
      <span class="feature-tag">📈 PE_TTM</span>
      <span class="feature-tag">🔄 行业中性化</span>
      <span class="feature-tag">⚠️ 陷阱规避</span>
    </div>
    <a href="/ashare-book4/002_Chapter2/2.2_PE_Factor_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">2.3</span>
      <h3>市净率因子（PB）</h3>
    </div>
    <p>掌握PB因子的计算方法、适用行业和局限性，理解净资产质量对PB因子的影响。</p>
    <div class="chapter-features">
      <span class="feature-tag">🏦 金融适用</span>
      <span class="feature-tag">🏭 重资产行业</span>
      <span class="feature-tag">📊 净资产质量</span>
    </div>
    <a href="/ashare-book4/002_Chapter2/2.3_PB_Factor_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">2.4</span>
      <h3>市销率因子（PS）</h3>
    </div>
    <p>学习PS因子在成长股和亏损股估值中的应用，理解营收质量对PS因子的影响。</p>
    <div class="chapter-features">
      <span class="feature-tag">🚀 成长股适用</span>
      <span class="feature-tag">📉 亏损股估值</span>
      <span class="feature-tag">💰 营收质量</span>
    </div>
    <a href="/ashare-book4/002_Chapter2/2.4_PS_Factor_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">2.5</span>
      <h3>股息率因子</h3>
    </div>
    <p>掌握股息率因子的计算和应用，理解高股息策略在A股的有效性和适用场景。</p>
    <div class="chapter-features">
      <span class="feature-tag">💰 现金回报</span>
      <span class="feature-tag">🛡️ 防御属性</span>
      <span class="feature-tag">📅 分红政策</span>
    </div>
    <a href="/ashare-book4/002_Chapter2/2.5_Dividend_Factor_CN" class="chapter-link">开始学习 →</a>
  </div>

  <div class="chapter-card">
    <div class="chapter-header">
      <span class="chapter-number">2.6</span>
      <h3>价值因子组合</h3>
    </div>
    <p>学习如何组合多个价值因子，构建复合价值因子，提升选股效果。</p>
    <div class="chapter-features">
      <span class="feature-tag">🔄 因子组合</span>
      <span class="feature-tag">⚖️ 权重分配</span>
      <span class="feature-tag">📊 回测验证</span>
    </div>
    <a href="/ashare-book4/002_Chapter2/2.6_Value_Composite_CN" class="chapter-link">开始学习 →</a>
  </div>
</div>

## 🎯 学习目标

通过本章学习，您将能够：

- **理解价值因子本质**：掌握价值投资的量化表达，理解低估值股票长期跑赢的逻辑
- **计算各类价值因子**：熟练计算PE、PB、PS、股息率等因子
- **识别因子陷阱**：避免价值陷阱，理解不同行业的估值差异
- **构建复合因子**：组合多个价值因子，提升选股效果
- **回测验证因子**：使用韬睿平台验证价值因子在A股的有效性

## 📚 核心概念

### 价值因子理论基础

<div class="tip-box">
  <h4>📖 价值因子的经济学逻辑</h4>
  <p><strong>核心假设：</strong>市场对股票的定价存在偏差，低估值股票被市场低估，未来会回归合理价值。</p>
  <p><strong>理论支撑：</strong></p>
  <ul>
    <li><strong>格雷厄姆价值投资：</strong>以低于内在价值的价格买入，获取安全边际</li>
    <li><strong>Fama-French三因子：</strong>HML因子（高账面市值比-低账面市值比）长期有正收益</li>
    <li><strong>行为金融学：</strong>投资者过度反应导致低估值股票被过度抛售</li>
  </ul>
  <p><strong>参考：</strong>第一册5.5节估值方法</p>
</div>

### 主要价值因子概览

<div class="comparison-table">
  <table>
    <thead>
      <tr>
        <th>因子名称</th>
        <th>计算公式</th>
        <th>适用行业</th>
        <th>优点</th>
        <th>局限性</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>PE（市盈率）</strong></td>
        <td>市值 / 净利润</td>
        <td>盈利稳定行业</td>
        <td>直观、应用广泛</td>
        <td>亏损股无法使用</td>
      </tr>
      <tr>
        <td><strong>PB（市净率）</strong></td>
        <td>市值 / 净资产</td>
        <td>金融、重资产</td>
        <td>适用范围广</td>
        <td>轻资产公司不适用</td>
      </tr>
      <tr>
        <td><strong>PS（市销率）</strong></td>
        <td>市值 / 营业收入</td>
        <td>成长股、亏损股</td>
        <td>亏损股可用</td>
        <td>忽略盈利能力</td>
      </tr>
      <tr>
        <td><strong>股息率</strong></td>
        <td>每股股息 / 股价</td>
        <td>成熟行业</td>
        <td>现金回报明确</td>
        <td>成长股不适用</td>
      </tr>
      <tr>
        <td><strong>EP（盈利收益率）</strong></td>
        <td>净利润 / 市值</td>
        <td>同PE</td>
        <td>便于跨资产比较</td>
        <td>同PE</td>
      </tr>
    </tbody>
  </table>
</div>

### 价值因子在A股的表现

<div class="exchange-grid">
  <div class="exchange-card">
    <div class="exchange-header">
      <span class="exchange-icon">📈</span>
      <h3>长期有效</h3>
    </div>
    <div class="exchange-content">
      <p><strong>历史表现：</strong>2005-2024年，低PE/PB组合年化超额收益约5-8%</p>
      <p><strong>有效性：</strong>价值因子在A股长期有效，但存在周期性</p>
    </div>
  </div>

  <div class="exchange-card">
    <div class="exchange-header">
      <span class="exchange-icon">🔄</span>
      <h3>周期性特征</h3>
    </div>
    <div class="exchange-content">
      <p><strong>强势期：</strong>2016-2018年、2021-2023年价值风格占优</p>
      <p><strong>弱势期：</strong>2019-2020年成长风格占优，价值因子表现较弱</p>
    </div>
  </div>

  <div class="exchange-card">
    <div class="exchange-header">
      <span class="exchange-icon">🏭</span>
      <h3>行业差异大</h3>
    </div>
    <div class="exchange-content">
      <p><strong>高PE行业：</strong>科技、医药、消费（成长溢价）</p>
      <p><strong>低PE行业：</strong>银行、地产、周期（估值折价）</p>
      <p><strong>启示：</strong>需要行业中性化处理</p>
    </div>
  </div>
</div>

## 🔗 相关章节

本章为因子构建核心章节，与以下章节紧密关联：

### 与第一册的关联
- **第一册第五章**：基本面分析框架 - 价值因子的财务数据来源
- **第一册5.5节**：估值方法 - PE、PB等估值指标的主观分析方法
- **第一册第六章**：选股框架 - 价值因子在选股中的应用

### 与第二册的关联
- **第二册第一章**：经济周期 - 价值因子的周期性表现
- **第二册第四章**：行业轮动 - 不同行业的估值差异

### 与本册其他章节的关联
- **第一章**：量化投资概述 - 因子投资的理论基础
- **第三章-第六章**：其他因子类别 - 与价值因子的组合使用
- **第七章**：多因子模型 - 价值因子在多因子模型中的权重

## 💡 学习建议

<div class="board-details">
  <div class="board-card">
    <h4>🎯 学习方法建议</h4>
    <div class="board-content">
      <ol>
        <li><strong>理解逻辑：</strong>先理解价值投资的核心逻辑，不要只记公式</li>
        <li><strong>动手计算：</strong>使用JQData获取数据，亲手计算各类价值因子</li>
        <li><strong>回测验证：</strong>使用韬睿平台回测价值因子在A股的有效性</li>
        <li><strong>结合实例：</strong>分析具体股票的估值，理解因子的实际意义</li>
      </ol>
    </div>
  </div>

  <div class="board-card">
    <h4>⚠️ 常见误区提醒</h4>
    <div class="board-content">
      <ul>
        <li><strong>价值陷阱：</strong>低估值不等于便宜，可能是基本面恶化</li>
        <li><strong>行业忽视：</strong>不同行业估值水平差异大，需要行业中性化</li>
        <li><strong>单一因子：</strong>单一价值因子效果有限，需要组合使用</li>
        <li><strong>时效性：</strong>价值因子有周期性，不是任何时候都有效</li>
      </ul>
    </div>
  </div>
</div>

## 📊 本章知识图谱

```
价值因子构建
├── 2.1 价值因子概述
│   ├── 理论基础（格雷厄姆、Fama-French）
│   ├── 经济学逻辑
│   ├── A股有效性验证
│   └── 价值陷阱识别
├── 2.2 市盈率因子（PE）
│   ├── PE_TTM / 静态PE / 动态PE
│   ├── EP（盈利收益率）
│   ├── 行业中性化处理
│   └── A股PE因子回测
├── 2.3 市净率因子（PB）
│   ├── PB计算方法
│   ├── 适用行业分析
│   ├── 净资产质量调整
│   └── A股PB因子回测
├── 2.4 市销率因子（PS）
│   ├── PS计算方法
│   ├── 成长股估值应用
│   ├── 营收质量分析
│   └── A股PS因子回测
├── 2.5 股息率因子
│   ├── 股息率计算
│   ├── 高股息策略
│   ├── 分红政策分析
│   └── A股股息率因子回测
└── 2.6 价值因子组合
    ├── 因子组合方法
    ├── 权重分配策略
    ├── 复合价值因子构建
    └── 组合回测验证
```

---

**下一章：** [第三章：成长因子构建 →](/ashare-book4/003_Chapter3_Growth_Factors_CN)
