---
title: "H.1 小节格式规范模版"
description: "基于7.1节总结的完整小节格式规范，包含所有样式类和内容结构的标准化模版"
lang: "zh-CN"
alt: "小节格式规范模版"
layout: "/src/layouts/HandbookLayout.astro"
updateDate: "2025-01-03"
---

# H.1 小节格式规范模版

**核心摘要：**
> 
> 本模版基于7.1节《系统性风险识别与分类》的完整格式总结，提供标准化的小节结构、样式类使用和内容组织方式。涵盖frontmatter配置、章节概览、核心内容、样式类应用、实践指南等完整要素，为后续章节创建提供统一的格式规范。

## 📋 Frontmatter标准配置

```yaml
---
title: "X.X 章节标题"
description: "SEO优化的页面描述，包含关键词和核心内容概述"
lang: "zh-CN"
alt: "页面替代标题"
layout: "/src/layouts/HandbookLayout.astro"
updateDate: "2025-01-03"
---
```

## 📖 页面结构标准

### 1. 页面标题与核心摘要
```markdown
# X.X 章节标题

**核心摘要：**
> 
> 核心摘要内容，使用引用块格式，概述章节主要内容、学习目标和实践价值。
```

### 2. 章节概览
```html
## 📖 章节概览

<div class="chapter-overview">
<div class="overview-grid">
<div class="overview-item">
<h4>🔍 主题一</h4>
<p>主题一的简要描述</p>
</div>
<div class="overview-item">
<h4>📊 主题二</h4>
<p>主题二的简要描述</p>
</div>
<!-- 更多overview-item... -->
</div>
</div>
```

## 🎨 样式类使用规范

### 📋 已使用样式类总结

#### 1. 布局容器类
- `chapter-overview` + `overview-grid` + `overview-item` - 章节概览
- `component-grid` + `component-card` - 组件网格布局
- `metrics-grid` + `metric-card` - 指标展示网格
- `status-cards` + `status-card` - 状态卡片系统

#### 2. 流程图类
- `framework-flow` + `flow-step` + `flow-arrow` - 标准流程图
- `framework-step` + `step-number` + `step-content` - 编号步骤流程

#### 3. 信息展示类
- `key-points-cards` + `key-point` + `key-point-icon` + `key-point-content` - 要点卡片
- `status-card` + `status-header` + `status-label` + `status-content` - 状态信息卡片
- `metric-card` + `metric-header` + `metric-content` + `metric-value` - 指标卡片

#### 4. 状态标识类
- `status-card.green` - 绿色（正常/免费）
- `status-card.yellow` - 黄色（警告/关注）
- `status-card.red` - 红色（危险/极高风险）
- `status-card.blue` - 蓝色（信息）
- `status-card.purple` - 紫色（专业/付费）
- `status-card.gray` - 灰色（中性）

### 📋 未使用但可用的样式类

#### 1. 时间轴类
- `evolution-timeline` + `evolution-stage` - 发展历程时间轴
- `timeline-event` - 时间轴事件

#### 2. 数据分析类
- `signal-grid` + `signal-item` - 信号分析网格
- `sentiment-grid` + `sentiment-item` - 情绪分析网格
- `flow-grid` + `flow-source` - 资金流向分析

#### 3. 组合展示类
- `strategy-grid` + `strategy-card` - 策略展示网格
- `feature-grid` + `feature-item` - 特性展示网格
- `alternative-portfolio` + `alternative-category` - 另类投资组合

#### 4. 专业工具类
- `risk-assessment` + `risk-category` - 风险评估
- `warning-thresholds` + `warning-card` - 预警阈值
- `learning-objectives` + `objective-item` - 学习目标

## 📝 内容结构标准模版

### 1. 理论基础部分
```markdown
## 🔍 理论基础标题

### 📚 子标题

内容描述段落...

<div class="key-points-cards">
<div class="key-point">
<span class="key-point-icon">💡</span>
<div class="key-point-content">
<strong>要点标题</strong>要点内容描述
</div>
</div>
<!-- 更多key-point... -->
</div>
```

### 2. 流程机制部分
```markdown
### 🔄 流程机制标题

流程描述段落...

<div class="framework-flow">
<div class="flow-step">
<h4>🔗 步骤标题</h4>
<p>步骤描述内容</p>
</div>
<div class="flow-arrow">→</div>
<!-- 更多flow-step... -->
</div>
```

### 3. 分类体系部分
```markdown
### 📊 分类体系标题

<div class="status-cards">
<div class="status-card green">
<div class="status-header">
<h4>分类名称</h4>
<span class="status-label">状态标签</span>
</div>
<div class="status-content">
<p><strong>特征</strong>：特征描述</p>
<p><strong>监测指标</strong>：<a href="链接" target="_blank">指标名称</a></p>
<p><strong>当前状态</strong>：状态描述</p>
</div>
</div>
<!-- 更多status-card... -->
</div>
```

### 4. 指标监测部分
```markdown
### 📈 指标监测标题

<div class="metrics-grid">
<div class="metric-card">
<div class="metric-header">
<h4>指标名称</h4>
<span class="metric-status normal">状态</span>
</div>
<div class="metric-content">
<div class="metric-value">数值</div>
<div class="metric-label">单位/描述</div>
<div class="metric-benchmark">基准信息 | 数据源: <a href="链接" target="_blank">来源</a></div>
</div>
</div>
<!-- 更多metric-card... -->
</div>
```

### 5. 工具方法部分
```markdown
### 🛠️ 工具方法标题

<div class="component-grid">
<div class="component-card">
<h4>工具名称</h4>
<p>工具描述和应用场景</p>
</div>
<!-- 更多component-card... -->
</div>
```

### 6. 实践应用部分
```markdown
### 💼 实践应用标题

<div class="framework-flow">
<div class="framework-step">
<div class="step-number">1</div>
<div class="step-content">
<h4>步骤标题</h4>
<p>步骤描述</p>
</div>
</div>
<div class="framework-arrow">→</div>
<!-- 更多framework-step... -->
</div>
```

### 7. 工具推荐部分
```markdown
### 🛠️ 工具推荐标题

<div class="status-cards">
<div class="status-card green">
<div class="status-header">
<h4>工具名称</h4>
<span class="status-label">免费</span>
</div>
<div class="status-content">
<p><strong>优势</strong>：优势描述</p>
<p><strong>API</strong>：<a href="链接" target="_blank">API文档</a></p>
</div>
</div>
<!-- 更多工具推荐... -->
</div>
```

### 8. 总结展望部分
```markdown
## 📊 总结与展望

### 核心要点回顾

<div class="key-points-cards">
<div class="key-point">
<span class="key-point-icon">💡</span>
<div class="key-point-content">
<strong>要点标题</strong>要点总结内容
</div>
</div>
<!-- 更多要点... -->
</div>

### 实践应用建议

**个人投资者**：针对个人投资者的建议...

**机构投资者**：针对机构投资者的建议...

### 下节预告

接下来的**X.X节 下节标题**将探讨...

---

*结尾总结段落，包含免责声明和风险提示。*
```

## 🎯 样式类选择指南

### 📊 根据内容类型选择样式类

#### 1. 概念解释 → `key-points-cards`
- 适用于要点列举、概念解释
- 支持图标和强调文本
- 响应式卡片布局

#### 2. 状态信息 → `status-cards`
- 适用于风险等级、工具分类
- 支持6种颜色主题
- 包含标题、标签、内容结构

#### 3. 数据指标 → `metrics-grid`
- 适用于数值展示、指标监测
- 支持状态标识和基准对比
- 突出显示数值信息

#### 4. 流程步骤 → `framework-flow`
- 适用于流程图、步骤说明
- 支持箭头连接和编号
- 响应式流程布局

#### 5. 组件展示 → `component-grid`
- 适用于工具介绍、方法说明
- 简洁的卡片布局
- 统一的标题和描述结构

### 🎨 颜色主题使用规范

#### 状态卡片颜色语义
- **绿色(green)**：正常状态、免费工具、低风险
- **黄色(yellow)**：警告状态、关注事项、中等风险
- **红色(red)**：危险状态、高风险、紧急情况
- **蓝色(blue)**：信息提示、中性状态
- **紫色(purple)**：专业工具、付费服务
- **灰色(gray)**：禁用状态、中性信息

## 📏 格式质量标准

### ✅ 必须遵循的格式要求

1. **HTML零空行**：所有HTML标签之间不允许空行
2. **样式类统一**：使用系统定义的样式类，不自定义CSS
3. **响应式设计**：确保移动端显示正常
4. **链接有效性**：所有外部链接必须有效且使用`target="_blank"`
5. **图标一致性**：使用emoji图标保持视觉一致性

### 🔍 内容质量标准

1. **数据时效性**：使用最新的市场数据和链接
2. **信息准确性**：确保所有数据来源可靠
3. **结构完整性**：包含理论、实践、工具、总结各部分
4. **可读性**：段落长度适中，层次清晰
5. **实用性**：提供具体的操作指导和工具推荐

## 📋 检查清单

### 生成前检查
- [ ] 是否使用了正确的frontmatter格式？
- [ ] 是否包含了核心摘要？
- [ ] 是否有章节概览？
- [ ] 样式类是否都在系统定义范围内？

### 生成后检查
- [ ] HTML标签间是否有空行？
- [ ] 所有链接是否有效？
- [ ] 移动端显示是否正常？
- [ ] 颜色主题是否语义正确？
- [ ] 是否包含总结和下节预告？

## 🚀 高级应用技巧

### 1. 混合布局使用
```html
<!-- 组合使用不同样式类 -->
<div class="component-grid">
  <div class="component-card">
    <h4>标题</h4>
    <div class="status-cards">
      <div class="status-card green">
        <!-- 嵌套状态卡片 -->
      </div>
    </div>
  </div>
</div>
```

### 2. 动态数据集成
```html
<!-- 集成实时数据链接 -->
<div class="metric-value">
  <a href="https://api.example.com" target="_blank">实时数据</a>
</div>
```

### 3. 渐进式信息展示
```html
<!-- 从简单到复杂的信息层次 -->
<div class="key-points-cards">
  <!-- 基础概念 -->
</div>
<div class="component-grid">
  <!-- 详细方法 -->
</div>
<div class="framework-flow">
  <!-- 具体步骤 -->
</div>
```

---

**📌 重要提醒**：本模版基于7.1节的实际格式总结，涵盖了所有已使用的样式类和内容结构。在创建新章节时，请严格按照此模版执行，确保格式统一性和视觉一致性。

**🔄 持续更新**：随着新章节的开发，本模版将持续更新，增加新的样式类和最佳实践案例。 