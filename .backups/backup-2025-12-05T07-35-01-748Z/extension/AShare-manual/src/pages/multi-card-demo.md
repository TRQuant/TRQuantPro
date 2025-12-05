---
title: 嵌套小卡片系统演示
description: 展示如何使用嵌套小卡片将复杂内容拆分为多个小卡片的演示页面
layout: /src/layouts/HandbookLayout.astro
---

import MultiCard from '../components/MultiCard.astro';

# 嵌套小卡片系统演示

## 🎯 系统概述

当单张卡片内容较多时，可以使用嵌套小卡片系统将复杂内容拆分为多个结构化的小卡片，提高可读性和用户体验。

## 📊 使用示例

### 1. 自适应网格布局

<MultiCard
  title="投资组合综合分析"
  subtitle="详细分析"
  theme="blue"
  layout="grid"
  cards={[
    {
      title: "财务健康度",
      label: "优秀",
      value: "95分",
      content: "现金流充裕，负债率低，<strong>ROE达到18.5%</strong>，远超行业平均水平"
    },
    {
      title: "市场表现",
      label: "良好", 
      value: "+15.2%",
      content: "年初至今涨幅显著，<strong>跑赢大盘8.3%</strong>，波动率控制良好"
    },
    {
      title: "估值水平",
      label: "合理",
      value: "PE 22.5x",
      content: "当前估值处于合理区间，<strong>PEG比率1.2</strong>，具备成长性"
    },
    {
      title: "风险评估",
      label: "低风险",
      value: "风险系数0.8",
      content: "Beta值较低，<strong>最大回撤12%</strong>，风险可控"
    }
  ]}
/>

### 2. 强制一行布局

<MultiCard
  title="关键财务指标"
  subtitle="Q3 2024"
  theme="green"
  layout="row"
  cards={[
    {
      title: "营收增长",
      label: "强劲",
      value: "+28.5%",
      content: "同比增长显著"
    },
    {
      title: "净利润率",
      label: "稳定",
      value: "15.8%",
      content: "盈利能力良好"
    },
    {
      title: "现金流",
      label: "健康",
      value: "$2.5B",
      content: "自由现金流充裕"
    }
  ]}
/>

### 3. 三列布局

<MultiCard
  title="技术分析总结"
  subtitle="技术面"
  theme="purple"
  layout="3col"
  cards={[
    {
      title: "趋势分析",
      label: "上涨",
      content: "多条均线呈多头排列，<strong>MACD金叉</strong>",
      items: ["MA20突破MA50", "成交量放大", "RSI指标健康"]
    },
    {
      title: "支撑阻力",
      label: "明确",
      content: "关键位置清晰，<strong>支撑位$85</strong>",
      items: ["支撑: $85, $80", "阻力: $95, $100", "突破目标: $105"]
    },
    {
      title: "买卖信号",
      label: "买入",
      content: "多个指标发出<strong>买入信号</strong>",
      items: ["KDJ金叉", "布林带突破", "成交量确认"]
    }
  ]}
/>

### 4. 四列紧凑布局

<MultiCard
  title="行业对比分析"
  subtitle="同行比较"
  theme="orange"
  layout="4col"
  cards={[
    {
      title: "市值",
      value: "$150B",
      content: "行业第2位"
    },
    {
      title: "P/E比率",
      value: "22.5x",
      content: "低于平均"
    },
    {
      title: "ROE",
      value: "18.5%",
      content: "行业领先"
    },
    {
      title: "增长率",
      value: "25%+",
      content: "超预期"
    }
  ]}
/>

### 5. 两列布局

<MultiCard
  title="风险管理策略"
  subtitle="风控措施"
  theme="red"
  layout="2col"
  cards={[
    {
      title: "止损策略",
      label: "严格执行",
      value: "-8%",
      content: "设置<strong>8%止损线</strong>，严格执行风险控制",
      items: ["技术止损: 跌破关键支撑", "时间止损: 横盘超过3个月", "基本面止损: 业绩大幅下滑"]
    },
    {
      title: "仓位管理",
      label: "动态调整",
      value: "20-30%",
      content: "根据市场情况<strong>动态调整仓位</strong>",
      items: ["牛市: 提升至30%", "震荡市: 维持20-25%", "熊市: 降至15%以下"]
    }
  ]}
/>

## 🎨 布局选项说明

| 布局类型 | 说明 | 适用场景 |
|---------|------|---------|
| `grid` | 自适应网格布局 | 内容长度不一致，需要自动调整 |
| `row` | 强制一行显示 | 内容简短，希望横向展示 |
| `2col` | 两列布局 | 内容较多，需要更大空间 |
| `3col` | 三列布局 | 平衡内容和空间利用 |
| `4col` | 四列紧凑布局 | 内容简短，数据密集展示 |

## 🔧 使用方法

### 在Markdown中使用

```markdown
import MultiCard from '../components/MultiCard.astro';

<MultiCard
  title="卡片标题"
  subtitle="副标题"
  theme="blue"
  layout="grid"
  cards={[
    {
      title: "小卡片标题",
      label: "状态标签",
      value: "重要数值",
      content: "详细内容描述",
      items: ["列表项1", "列表项2"]
    }
  ]}
/>
```

### HTML中直接使用

```html
<div class="status-cards">
  <div class="status-card blue multi-card">
    <div class="status-header">
      <h4>综合分析报告</h4>
      <div class="status-label">详细分析</div>
    </div>
    
    <div class="mini-cards-grid">
      <div class="mini-card">
        <div class="mini-card-header">
          <h5>财务状况</h5>
          <div class="mini-card-label">优秀</div>
        </div>
        <div class="mini-card-content">
          <span class="mini-card-value">95分</span>
          <p>现金流充裕，负债率低</p>
        </div>
      </div>
    </div>
  </div>
</div>
```

## ✨ 特性优势

- **🎯 智能检测**: 自动识别适合拆分的单张卡片
- **📱 响应式**: 完美适配各种屏幕尺寸
- **🎨 主题支持**: 支持7种主题色彩
- **🔧 灵活布局**: 5种布局模式可选
- **♿ 无障碍**: 符合WCAG 2.1标准
- **�� 暗色模式**: 完美支持暗色主题 