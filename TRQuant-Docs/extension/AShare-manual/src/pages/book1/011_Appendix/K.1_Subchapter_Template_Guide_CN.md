---
title: "K.1 小节页面模板指南"
description: "Astro投资手册小节页面标准格式与内容模块完整示例"
lang: "zh-CN"
alt: "小节模板指南"
layout: "/src/layouts/HandbookLayout.astro"
updateDate: "2025-01-03"
---
# K.1 小节页面模板指南

> **核心摘要：**
> 
>本指南提供Astro投资手册小节页面的完整标准格式与各类内容模块示例，包括公式展示、数据表格、图片处理、互动元素等。通过标准化模板，确保全书内容格式统一、可读性强、可维护性高。

## 📋 章节导航
<div class="chapter-overview">
  <div class="overview-grid">
    <div class="overview-item">
      <h4>K.1.1 基础结构模板</h4>
      <p>Frontmatter、核心摘要、章节导航等基础结构</p>
    </div>
    <div class="overview-item">
      <h4>K.1.2 内容模块示例</h4>
      <p>公式、表格、图片、互动元素等各类内容展示</p>
    </div>
    <div class="overview-item">
      <h4>K.1.3 格式规范说明</h4>
      <p>缩进、空行、样式类等格式要求详细说明</p>
    </div>
    <div class="overview-item">
      <h4>K.1.4 扩展性设计</h4>
      <p>模板弹性扩展、自定义内容块设计原则</p>
    </div>
  </div>
</div>

## K.1.1 基础页面结构模板

### Frontmatter 标准格式

```yaml
---
title: "小节标题"
description: "页面描述（简明扼要，利于SEO）"
lang: "zh-CN"
alt: "可选替代标题"
layout: /src/layouts/HandbookLayout.astro
updateDate: "2025-01-03"
---
```

### 核心摘要固定格式

```markdown
**核心摘要：**
> 
>本小节核心观点、方法或结论简要总结。可多行，便于读者快速把握重点。支持换行和详细描述，但建议控制在3-5行内。
```

### 章节导航标准结构

```html
## 📋 章节导航
<div class="chapter-overview">
  <div class="overview-grid">
    <div class="overview-item">
      <h4>小节要点1</h4>
      <p>简要描述要点内容，支持多行扩展。</p>
    </div>
    <div class="overview-item">
      <h4>小节要点2</h4>
      <p>可根据实际内容增减overview-item数量。</p>
    </div>
    <!-- 可继续添加overview-item，保持2空格缩进，无空行 -->
  </div>
</div>
```

## K.1.2 内容模块展示示例

### 公式展示模块

<div class="info-block">
  <div class="info-title">夏普比率计算公式</div>
  <div class="info-content">
    <div class="formula-display">
      夏普比率 = (投资组合收益率 - 无风险收益率) / 投资组合标准差
    </div>
    <div class="formula-latex">
      $$\text{<GlossaryTerm term="Sharpe" /> Ratio} = \frac{R_p - R_f}{\sigma_p}$$
    </div>
  </div>
  <div class="info-explanation">
    其中：R_p为投资组合收益率，R_f为无风险收益率，σ_p为投资组合标准差。夏普比率越高，表示单位风险获得的超额收益越多。
  </div>
</div>

### 夏普比率公式示例（MathJax推荐写法）

夏普比率定义如下：

$$
\text{<GlossaryTerm term="Sharpe" /> Ratio} = \frac{R_p - R_f}{\sigma_p}
$$

其中 $R_p$ 为投资组合收益率，$R_f$ 为无风险收益率，$\sigma_p$ 为投资组合标准差。

### 数据表格模块

<div class="info-block">
  <div class="info-title">主要财务指标对比</div>
  <div class="info-content">
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>指标</th>
            <th>公司A</th>
            <th>公司B</th>
            <th>行业平均</th>
            <th>评级</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>ROE (%)</td>
            <td class="positive">15.2</td>
            <td class="neutral">12.8</td>
            <td>11.5</td>
            <td><span class="rating excellent">优秀</span></td>
          </tr>
          <tr>
            <td>P/E</td>
            <td>18.5</td>
            <td>22.3</td>
            <td>20.1</td>
            <td><span class="rating good">良好</span></td>
          </tr>
          <tr>
            <td>负债率 (%)</td>
            <td class="negative">65.2</td>
            <td>45.8</td>
            <td>52.3</td>
            <td><span class="rating warning">注意</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="info-explanation">
    表格数据支持颜色编码：正值用绿色，负值用红色，中性值用默认色。评级标签支持优秀、良好、注意、风险等级别。
  </div>
</div>

### 图片展示模块

<div class="info-block">
  <div class="info-title">投资组合收益曲线</div>
  <div class="info-content">
    <div class="image-container">
      <img src="/images/portfolio-performance.png" alt="投资组合收益曲线图" class="responsive-image" />
      <div class="image-caption">
        图1: 2020-2024年投资组合收益曲线对比（数据来源：Wind金融终端）
      </div>
    </div>
  </div>
  <div class="info-explanation">
    图片支持响应式显示，自动适配不同屏幕尺寸。建议使用WebP格式，并提供详细的alt描述和数据来源。
  </div>
</div>

### 互动元素模块

<div class="info-block">
  <div class="info-title">风险评估工具</div>
  <div class="info-content">
    <div class="interactive-element">
      <div class="risk-calculator">
        <div class="input-group">
          <label>投资金额 (万元):</label>
          <input type="number" id="investment-amount" value="100" min="1" max="10000" />
        </div>
        <div class="input-group">
          <label>风险偏好:</label>
          <select id="risk-preference">
            <option value="conservative">保守型</option>
            <option value="moderate">稳健型</option>
            <option value="aggressive">积极型</option>
          </select>
        </div>
        <div class="result-display">
          <div class="result-item">
            <span class="label">建议股票比例:</span>
            <span class="value" id="stock-ratio">60%</span>
          </div>
          <div class="result-item">
            <span class="label">预期年化收益:</span>
            <span class="value" id="expected-return">8.5%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="info-explanation">
    互动元素支持实时计算和动态显示。可集成简单的JavaScript逻辑，提供更好的用户体验。
  </div>
</div>

### 代码示例模块

<div class="info-block">
  <div class="info-title">Python股票数据获取</div>
  <div class="info-content">
    <div class="code-block">
      <div class="code-header">
        <span class="language">Python</span>
        <button class="copy-btn">复制代码</button>
      </div>
      <pre><code class="language-python">
import yfinance as yf
import pandas as pd

# 获取股票数据
def get_stock_data(symbol, period='1y'):
    """
    获取股票历史数据
    
    Args:
        symbol: 股票代码
        period: 时间周期
    
    Returns:
        DataFrame: 股票数据
    """
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data

# 示例使用
aapl_data = get_stock_data('AAPL', '2y')
print(aapl_data.head())
      </code></pre>
    </div>
  </div>
  <div class="info-explanation">
    代码块支持语法高亮、复制功能，并提供详细的注释说明。建议包含完整的函数文档和使用示例。
  </div>
</div>

### 警告提示模块

<div class="warning-block">
  <div class="warning-icon">⚠️</div>
  <div class="warning-content">
    <div class="warning-title">投资风险提示</div>
    <div class="warning-text">
      股票投资存在市场风险，历史业绩不代表未来表现。投资者应根据自身风险承受能力谨慎投资，必要时咨询专业投资顾问。
    </div>
  </div>
</div>

### 成功案例模块

<div class="success-block">
  <div class="success-icon">✅</div>
  <div class="success-content">
    <div class="success-title">成功案例</div>
    <div class="success-text">
      通过应用本章介绍的价值投资策略，投资者在2020-2023年期间实现了年化15.2%的收益，显著超越市场基准。
    </div>
  </div>
</div>

### 引用文献模块

<div class="reference-block">
  <div class="reference-title">参考文献</div>
  <div class="reference-list">
    <div class="reference-item">
      [1] Graham, B., & Dodd, D. (2008). Security Analysis. McGraw-Hill Education.
    </div>
    <div class="reference-item">
      [2] Buffett, W. (2020). Berkshire Hathaway Annual Report. Berkshire Hathaway Inc.
    </div>
    <div class="reference-item">
      [3] 中国证监会. (2023). 《证券投资基金管理办法》. 中国证监会官网.
    </div>
  </div>
</div>

## K.1.3 格式规范详细说明

### HTML标签缩进规范

```html
<!-- 正确：2空格缩进，无空行 -->
<div class="info-block">
  <div class="info-title">标题</div>
  <div class="info-content">
    内容
  </div>
</div>

<!-- 错误：4空格缩进，有空行 -->
<div class="info-block">

    <div class="info-title">标题</div>
    
    <div class="info-content">
        内容
    </div>
    
</div>
```

### CSS类命名规范

- `.info-block`: 信息块容器
- `.info-title`: 信息块标题
- `.info-content`: 信息块内容
- `.info-explanation`: 信息块说明
- `.overview-item`: 概览项目
- `.chapter-overview`: 章节概览容器
- `.warning-block`: 警告提示块
- `.success-block`: 成功案例块
- `.reference-block`: 参考文献块

### 响应式设计要求

```css
/* 移动端适配 */
@media (max-width: 768px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .responsive-image {
    max-width: 100%;
    height: auto;
  }
}
```

## K.1.4 扩展性设计原则

### 自定义内容块

```html
<!-- 可扩展的内容块结构 -->
<div class="custom-block [type-class]">
  <div class="custom-header">
    <div class="custom-icon">[图标]</div>
    <div class="custom-title">[标题]</div>
  </div>
  <div class="custom-content">
    [内容区域]
  </div>
  <div class="custom-footer">
    [底部信息]
  </div>
</div>
```

### 主题变量支持

```css
/* 支持主题切换的CSS变量 */
.info-block {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
}

.warning-block {
  background: var(--warning-bg);
  border-left: 4px solid var(--warning-color);
}
```

### 多语言支持

```markdown
<!-- 中文版本 -->
**核心摘要：**
> 
>中文摘要内容

<!-- 英文版本 -->
**Core Summary:**
> 
>English summary content
```

## K.1.5 模板使用指南

### 快速开始

1. 复制基础模板结构
2. 填写frontmatter信息
3. 编写核心摘要
4. 设计章节导航
5. 添加内容模块
6. 检查格式规范
7. 测试响应式显示

### 内容模块选择

- **公式密集型**: 使用info-block + formula-display
- **数据分析型**: 使用table-container + data-table
- **案例研究型**: 使用image-container + success-block
- **工具介绍型**: 使用interactive-element + code-block
- **风险提示型**: 使用warning-block + reference-block

### 质量检查清单

- [ ] Frontmatter字段完整
- [ ] 核心摘要格式正确
- [ ] HTML标签无空行
- [ ] 2空格缩进一致
- [ ] 响应式图片设置
- [ ] 代码语法高亮
- [ ] 表格数据准确
- [ ] 引用来源标注
- [ ] 多端显示测试

<style>
/* 模板专用样式 */
.formula-display {
  background: var(--code-bg);
  padding: 1rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  text-align: center;
  margin: 0.5rem 0;
}

.formula-latex {
  text-align: center;
  margin: 1rem 0;
}

.table-container {
  overflow-x: auto;
  margin: 1rem 0;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
}

.data-table th,
.data-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.data-table th {
  background: var(--card-bg);
  font-weight: 600;
}

.positive {
  color: var(--success-color);
}

.negative {
  color: var(--error-color);
}

.neutral {
  color: var(--text-secondary);
}

.rating {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.rating.excellent {
  background: var(--success-bg);
  color: var(--success-color);
}

.rating.good {
  background: var(--info-bg);
  color: var(--info-color);
}

.rating.warning {
  background: var(--warning-bg);
  color: var(--warning-color);
}

.image-container {
  text-align: center;
  margin: 1rem 0;
}

.responsive-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.image-caption {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
  font-style: italic;
}

.interactive-element {
  background: var(--card-bg);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.risk-calculator {
  max-width: 400px;
  margin: 0 auto;
}

.input-group {
  margin-bottom: 1rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--input-bg);
  color: var(--text-primary);
}

.result-display {
  margin-top: 1.5rem;
  padding: 1rem;
  background: var(--highlight-bg);
  border-radius: 4px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.result-item:last-child {
  margin-bottom: 0;
}

.result-item .label {
  font-weight: 500;
}

.result-item .value {
  color: var(--primary-color);
  font-weight: 600;
}

.code-block {
  margin: 1rem 0;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--code-header-bg);
  padding: 0.5rem 1rem;
  border-radius: 4px 4px 0 0;
  border-bottom: 1px solid var(--border-color);
}

.language {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.copy-btn {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.75rem;
}

.copy-btn:hover {
  background: var(--primary-dark);
}

.warning-block,
.success-block {
  display: flex;
  align-items: flex-start;
  margin: 1.5rem 0;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid;
}

.warning-block {
  background: var(--warning-bg);
  border-left-color: var(--warning-color);
}

.success-block {
  background: var(--success-bg);
  border-left-color: var(--success-color);
}

.warning-icon,
.success-icon {
  font-size: 1.25rem;
  margin-right: 0.75rem;
  margin-top: 0.125rem;
}

.warning-title,
.success-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.warning-text,
.success-text {
  line-height: 1.6;
}

.reference-block {
  margin: 2rem 0;
  padding: 1.5rem;
  background: var(--card-bg);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.reference-title {
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.reference-item {
  margin-bottom: 0.75rem;
  padding-left: 1rem;
  position: relative;
  line-height: 1.6;
}

.reference-item:last-child {
  margin-bottom: 0;
}

.reference-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.75rem;
  width: 4px;
  height: 4px;
  background: var(--primary-color);
  border-radius: 50%;
}

@media (max-width: 768px) {
  .overview-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .interactive-element {
    padding: 1rem;
  }
  
  .risk-calculator {
    max-width: 100%;
  }
  
  .code-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .warning-block,
  .success-block {
    flex-direction: column;
    text-align: center;
  }
  
  .warning-icon,
  .success-icon {
    margin-right: 0;
    margin-bottom: 0.5rem;
  }
}
</style>

## 📊 可视化组件使用总结

### 🎯 组件选择指南

| 使用场景 | 推荐组件 | 主要特点 |
|---------|---------|---------|
| 系统架构、流程展示 | 流程图组件 | 清晰的步骤展示，支持箭头连接 |
| 功能模块、工具介绍 | 组件网格 | 响应式布局，图标+文字说明 |
| 投资模型、因子分析 | 多因子模型 | 公式展示+分类详述 |
| 指标监控、数据展示 | 指标展示 | 分类展示，图标标识 |
| 关键词、标签分类 | 标签系统 | 颜色区分，分组展示 |

### 🎨 设计原则

1. **一致性原则**：同一页面使用相同风格的组件
2. **简洁性原则**：避免过度装饰，突出内容本身
3. **响应式原则**：确保在不同设备上都有良好体验
4. **可访问性原则**：使用语义化图标和清晰的文字描述

### 🔧 技术要点

1. **样式复用**：所有组件样式已统一定义在 `/src/styles/components.css`
2. **HTML结构**：严格遵循模板结构，保持HTML标签间零空行
3. **图标选择**：使用emoji图标，确保跨平台兼容性
4. **颜色系统**：依赖CSS变量，自动适配亮色/暗色主题

### 📝 使用建议

1. **选择合适组件**：根据内容类型选择最适合的可视化组件
2. **保持内容简洁**：每个卡片的描述控制在1-2行内
3. **合理使用图标**：选择与内容相关的语义化图标
4. **注意布局平衡**：避免单行卡片数量过多或过少
5. **测试响应式效果**：确保在移动端也有良好显示效果

### 🚀 扩展性设计

如需自定义样式，可在页面中添加局部CSS覆盖：

```css
<style>
.my-custom-flow .flow-step {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  }
</style>
```

### 📚 参考示例

完整的可视化组件使用示例可参考：
- `src/pages/007_Chapter7/7.7_QuantConnect_IBKR_Integration_CN.md`
- `src/styles/README.md` - 详细的组件使用文档

---

> **所有上述写法在本页面均应被MathJax自动渲染为数学公式。**

---
---
title: "K.1 小节页面模板指南"
description: "Astro投资手册小节页面标准格式与内容模块完整示例"
lang: "zh-CN"
alt: "小节模板指南"
layout: /src/layouts/HandbookLayout.astro
updateDate: "2025-01-03"
---

# K.1 小节页面模板指南

> **核心摘要：**
> 
>本指南提供Astro投资手册小节页面的完整标准格式与各类内容模块示例，包括公式展示、数据表格、图片处理、互动元素等。通过标准化模板，确保全书内容格式统一、可读性强、可维护性高。

## 📋 章节导航
<div class="chapter-overview">
  <div class="overview-grid">
    <div class="overview-item">
      <h4>K.1.1 基础结构模板</h4>
      <p>Frontmatter、核心摘要、章节导航等基础结构</p>
    </div>
    <div class="overview-item">
      <h4>K.1.2 内容模块示例</h4>
      <p>公式、表格、图片、互动元素等各类内容展示</p>
    </div>
    <div class="overview-item">
      <h4>K.1.3 格式规范说明</h4>
      <p>缩进、空行、样式类等格式要求详细说明</p>
    </div>
    <div class="overview-item">
      <h4>K.1.4 扩展性设计</h4>
      <p>模板弹性扩展、自定义内容块设计原则</p>
    </div>
  </div>
</div>

## K.1.1 基础页面结构模板

### Frontmatter 标准格式

```yaml
---
title: "小节标题"
description: "页面描述（简明扼要，利于SEO）"
lang: "zh-CN"
alt: "可选替代标题"
layout: /src/layouts/HandbookLayout.astro
updateDate: "2025-01-03"
---
```

### 核心摘要固定格式

```markdown
**核心摘要：**
> 
>本小节核心观点、方法或结论简要总结。可多行，便于读者快速把握重点。支持换行和详细描述，但建议控制在3-5行内。
```

### 章节导航标准结构

```html
## 📋 章节导航
<div class="chapter-overview">
  <div class="overview-grid">
    <div class="overview-item">
      <h4>小节要点1</h4>
      <p>简要描述要点内容，支持多行扩展。</p>
    </div>
    <div class="overview-item">
      <h4>小节要点2</h4>
      <p>可根据实际内容增减overview-item数量。</p>
    </div>
    <!-- 可继续添加overview-item，保持2空格缩进，无空行 -->
  </div>
</div>
```

## K.1.2 内容模块展示示例

### 公式展示模块

<div class="info-block">
  <div class="info-title">夏普比率计算公式</div>
  <div class="info-content">
    <div class="formula-display">
      夏普比率 = (投资组合收益率 - 无风险收益率) / 投资组合标准差
    </div>
    <div class="formula-latex">
      $$\text{<GlossaryTerm term="Sharpe" /> Ratio} = \frac{R_p - R_f}{\sigma_p}$$
    </div>
  </div>
  <div class="info-explanation">
    其中：R_p为投资组合收益率，R_f为无风险收益率，σ_p为投资组合标准差。夏普比率越高，表示单位风险获得的超额收益越多。
  </div>
</div>

### 夏普比率公式示例（MathJax推荐写法）

夏普比率定义如下：

$$
\text{<GlossaryTerm term="Sharpe" /> Ratio} = \frac{R_p - R_f}{\sigma_p}
$$

其中 $R_p$ 为投资组合收益率，$R_f$ 为无风险收益率，$\sigma_p$ 为投资组合标准差。

### 数据表格模块

<div class="info-block">
  <div class="info-title">主要财务指标对比</div>
  <div class="info-content">
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>指标</th>
            <th>公司A</th>
            <th>公司B</th>
            <th>行业平均</th>
            <th>评级</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>ROE (%)</td>
            <td class="positive">15.2</td>
            <td class="neutral">12.8</td>
            <td>11.5</td>
            <td><span class="rating excellent">优秀</span></td>
          </tr>
          <tr>
            <td>P/E</td>
            <td>18.5</td>
            <td>22.3</td>
            <td>20.1</td>
            <td><span class="rating good">良好</span></td>
          </tr>
          <tr>
            <td>负债率 (%)</td>
            <td class="negative">65.2</td>
            <td>45.8</td>
            <td>52.3</td>
            <td><span class="rating warning">注意</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="info-explanation">
    表格数据支持颜色编码：正值用绿色，负值用红色，中性值用默认色。评级标签支持优秀、良好、注意、风险等级别。
  </div>
</div>

### 图片展示模块

<div class="info-block">
  <div class="info-title">投资组合收益曲线</div>
  <div class="info-content">
    <div class="image-container">
      <img src="/images/portfolio-performance.png" alt="投资组合收益曲线图" class="responsive-image" />
      <div class="image-caption">
        图1: 2020-2024年投资组合收益曲线对比（数据来源：Wind金融终端）
      </div>
    </div>
  </div>
  <div class="info-explanation">
    图片支持响应式显示，自动适配不同屏幕尺寸。建议使用WebP格式，并提供详细的alt描述和数据来源。
  </div>
</div>

### 互动元素模块

<div class="info-block">
  <div class="info-title">风险评估工具</div>
  <div class="info-content">
    <div class="interactive-element">
      <div class="risk-calculator">
        <div class="input-group">
          <label>投资金额 (万元):</label>
          <input type="number" id="investment-amount" value="100" min="1" max="10000" />
        </div>
        <div class="input-group">
          <label>风险偏好:</label>
          <select id="risk-preference">
            <option value="conservative">保守型</option>
            <option value="moderate">稳健型</option>
            <option value="aggressive">积极型</option>
          </select>
        </div>
        <div class="result-display">
          <div class="result-item">
            <span class="label">建议股票比例:</span>
            <span class="value" id="stock-ratio">60%</span>
          </div>
          <div class="result-item">
            <span class="label">预期年化收益:</span>
            <span class="value" id="expected-return">8.5%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="info-explanation">
    互动元素支持实时计算和动态显示。可集成简单的JavaScript逻辑，提供更好的用户体验。
  </div>
</div>

### 代码示例模块

<div class="info-block">
  <div class="info-title">Python股票数据获取</div>
  <div class="info-content">
    <div class="code-block">
      <div class="code-header">
        <span class="language">Python</span>
        <button class="copy-btn">复制代码</button>
      </div>
      <pre><code class="language-python">
import yfinance as yf
import pandas as pd

# 获取股票数据
def get_stock_data(symbol, period='1y'):
    """
    获取股票历史数据
    
    Args:
        symbol: 股票代码
        period: 时间周期
    
    Returns:
        DataFrame: 股票数据
    """
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data

# 示例使用
aapl_data = get_stock_data('AAPL', '2y')
print(aapl_data.head())
      </code></pre>
    </div>
  </div>
  <div class="info-explanation">
    代码块支持语法高亮、复制功能，并提供详细的注释说明。建议包含完整的函数文档和使用示例。
  </div>
</div>

### 警告提示模块

<div class="warning-block">
  <div class="warning-icon">⚠️</div>
  <div class="warning-content">
    <div class="warning-title">投资风险提示</div>
    <div class="warning-text">
      股票投资存在市场风险，历史业绩不代表未来表现。投资者应根据自身风险承受能力谨慎投资，必要时咨询专业投资顾问。
    </div>
  </div>
</div>

### 成功案例模块

<div class="success-block">
  <div class="success-icon">✅</div>
  <div class="success-content">
    <div class="success-title">成功案例</div>
    <div class="success-text">
      通过应用本章介绍的价值投资策略，投资者在2020-2023年期间实现了年化15.2%的收益，显著超越市场基准。
    </div>
  </div>
</div>

### 引用文献模块

<div class="reference-block">
  <div class="reference-title">参考文献</div>
  <div class="reference-list">
    <div class="reference-item">
      [1] Graham, B., & Dodd, D. (2008). Security Analysis. McGraw-Hill Education.
    </div>
    <div class="reference-item">
      [2] Buffett, W. (2020). Berkshire Hathaway Annual Report. Berkshire Hathaway Inc.
    </div>
    <div class="reference-item">
      [3] 中国证监会. (2023). 《证券投资基金管理办法》. 中国证监会官网.
    </div>
  </div>
</div>

## K.1.3 格式规范详细说明

### HTML标签缩进规范

```html
<!-- 正确：2空格缩进，无空行 -->
<div class="info-block">
  <div class="info-title">标题</div>
  <div class="info-content">
    内容
  </div>
</div>

<!-- 错误：4空格缩进，有空行 -->
<div class="info-block">

    <div class="info-title">标题</div>
    
    <div class="info-content">
        内容
    </div>
    
</div>
```

### CSS类命名规范

- `.info-block`: 信息块容器
- `.info-title`: 信息块标题
- `.info-content`: 信息块内容
- `.info-explanation`: 信息块说明
- `.overview-item`: 概览项目
- `.chapter-overview`: 章节概览容器
- `.warning-block`: 警告提示块
- `.success-block`: 成功案例块
- `.reference-block`: 参考文献块

### 响应式设计要求

```css
/* 移动端适配 */
@media (max-width: 768px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .responsive-image {
    max-width: 100%;
    height: auto;
  }
}
```

## K.1.4 扩展性设计原则

### 自定义内容块

```html
<!-- 可扩展的内容块结构 -->
<div class="custom-block [type-class]">
  <div class="custom-header">
    <div class="custom-icon">[图标]</div>
    <div class="custom-title">[标题]</div>
  </div>
  <div class="custom-content">
    [内容区域]
  </div>
  <div class="custom-footer">
    [底部信息]
  </div>
</div>
```

### 主题变量支持

```css
/* 支持主题切换的CSS变量 */
.info-block {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
}

.warning-block {
  background: var(--warning-bg);
  border-left: 4px solid var(--warning-color);
}
```

### 多语言支持

```markdown
<!-- 中文版本 -->
**核心摘要：**
> 
>中文摘要内容

<!-- 英文版本 -->
**Core Summary:**
> 
>English summary content
```

## K.1.5 模板使用指南

### 快速开始

1. 复制基础模板结构
2. 填写frontmatter信息
3. 编写核心摘要
4. 设计章节导航
5. 添加内容模块
6. 检查格式规范
7. 测试响应式显示

### 内容模块选择

- **公式密集型**: 使用info-block + formula-display
- **数据分析型**: 使用table-container + data-table
- **案例研究型**: 使用image-container + success-block
- **工具介绍型**: 使用interactive-element + code-block
- **风险提示型**: 使用warning-block + reference-block

### 质量检查清单

- [ ] Frontmatter字段完整
- [ ] 核心摘要格式正确
- [ ] HTML标签无空行
- [ ] 2空格缩进一致
- [ ] 响应式图片设置
- [ ] 代码语法高亮
- [ ] 表格数据准确
- [ ] 引用来源标注
- [ ] 多端显示测试

<style>
/* 模板专用样式 */
.formula-display {
  background: var(--code-bg);
  padding: 1rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  text-align: center;
  margin: 0.5rem 0;
}

.formula-latex {
  text-align: center;
  margin: 1rem 0;
}

.table-container {
  overflow-x: auto;
  margin: 1rem 0;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
}

.data-table th,
.data-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.data-table th {
  background: var(--card-bg);
  font-weight: 600;
}

.positive {
  color: var(--success-color);
}

.negative {
  color: var(--error-color);
}

.neutral {
  color: var(--text-secondary);
}

.rating {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.rating.excellent {
  background: var(--success-bg);
  color: var(--success-color);
}

.rating.good {
  background: var(--info-bg);
  color: var(--info-color);
}

.rating.warning {
  background: var(--warning-bg);
  color: var(--warning-color);
}

.image-container {
  text-align: center;
  margin: 1rem 0;
}

.responsive-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.image-caption {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
  font-style: italic;
}

.interactive-element {
  background: var(--card-bg);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.risk-calculator {
  max-width: 400px;
  margin: 0 auto;
}

.input-group {
  margin-bottom: 1rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--input-bg);
  color: var(--text-primary);
}

.result-display {
  margin-top: 1.5rem;
  padding: 1rem;
  background: var(--highlight-bg);
  border-radius: 4px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.result-item:last-child {
  margin-bottom: 0;
}

.result-item .label {
  font-weight: 500;
}

.result-item .value {
  color: var(--primary-color);
  font-weight: 600;
}

.code-block {
  margin: 1rem 0;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--code-header-bg);
  padding: 0.5rem 1rem;
  border-radius: 4px 4px 0 0;
  border-bottom: 1px solid var(--border-color);
}

.language {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.copy-btn {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.75rem;
}

.copy-btn:hover {
  background: var(--primary-dark);
}

.warning-block,
.success-block {
  display: flex;
  align-items: flex-start;
  margin: 1.5rem 0;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid;
}

.warning-block {
  background: var(--warning-bg);
  border-left-color: var(--warning-color);
}

.success-block {
  background: var(--success-bg);
  border-left-color: var(--success-color);
}

.warning-icon,
.success-icon {
  font-size: 1.25rem;
  margin-right: 0.75rem;
  margin-top: 0.125rem;
}

.warning-title,
.success-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.warning-text,
.success-text {
  line-height: 1.6;
}

.reference-block {
  margin: 2rem 0;
  padding: 1.5rem;
  background: var(--card-bg);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.reference-title {
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.reference-item {
  margin-bottom: 0.75rem;
  padding-left: 1rem;
  position: relative;
  line-height: 1.6;
}

.reference-item:last-child {
  margin-bottom: 0;
}

.reference-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.75rem;
  width: 4px;
  height: 4px;
  background: var(--primary-color);
  border-radius: 50%;
}

@media (max-width: 768px) {
  .overview-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .table-container {
    overflow-x: auto;
  }
  
  .interactive-element {
    padding: 1rem;
  }
  
  .risk-calculator {
    max-width: 100%;
  }
  
  .code-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .warning-block,
  .success-block {
    flex-direction: column;
    text-align: center;
  }
  
  .warning-icon,
  .success-icon {
    margin-right: 0;
    margin-bottom: 0.5rem;
  }
}
</style>

## 📊 可视化组件使用总结

### 🎯 组件选择指南

| 使用场景 | 推荐组件 | 主要特点 |
|---------|---------|---------|
| 系统架构、流程展示 | 流程图组件 | 清晰的步骤展示，支持箭头连接 |
| 功能模块、工具介绍 | 组件网格 | 响应式布局，图标+文字说明 |
| 投资模型、因子分析 | 多因子模型 | 公式展示+分类详述 |
| 指标监控、数据展示 | 指标展示 | 分类展示，图标标识 |
| 关键词、标签分类 | 标签系统 | 颜色区分，分组展示 |

### 🎨 设计原则

1. **一致性原则**：同一页面使用相同风格的组件
2. **简洁性原则**：避免过度装饰，突出内容本身
3. **响应式原则**：确保在不同设备上都有良好体验
4. **可访问性原则**：使用语义化图标和清晰的文字描述

### 🔧 技术要点

1. **样式复用**：所有组件样式已统一定义在 `/src/styles/components.css`
2. **HTML结构**：严格遵循模板结构，保持HTML标签间零空行
3. **图标选择**：使用emoji图标，确保跨平台兼容性
4. **颜色系统**：依赖CSS变量，自动适配亮色/暗色主题

### 📝 使用建议

1. **选择合适组件**：根据内容类型选择最适合的可视化组件
2. **保持内容简洁**：每个卡片的描述控制在1-2行内
3. **合理使用图标**：选择与内容相关的语义化图标
4. **注意布局平衡**：避免单行卡片数量过多或过少
5. **测试响应式效果**：确保在移动端也有良好显示效果

### 🚀 扩展性设计

如需自定义样式，可在页面中添加局部CSS覆盖：

```css
<style>
.my-custom-flow .flow-step {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  }
</style>
```

### 📚 参考示例

完整的可视化组件使用示例可参考：
- `src/pages/007_Chapter7/7.7_QuantConnect_IBKR_Integration_CN.md`
- `src/styles/README.md` - 详细的组件使用文档

---

> **所有上述写法在本页面均应被MathJax自动渲染为数学公式。**

---