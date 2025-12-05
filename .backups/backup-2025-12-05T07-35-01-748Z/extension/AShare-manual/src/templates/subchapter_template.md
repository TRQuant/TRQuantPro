---
# 页面元数据，所有字段必填，便于SEO和内容管理
# title: 小节标题（如"7.1 GuruFocus与Morningstar工具"）
# description: 页面描述（简明扼要，利于SEO）
# lang: 语言（如"zh-CN"）
# alt: 替代标题（可选，用于多语言或别名）
# layout: 布局文件路径（如"../../layouts/HandbookLayout.astro"）
# updateDate: 最后更新日期（如"2025-01-03"）
title: "小节标题"
description: "页面描述（简明扼要，利于SEO）"
lang: "zh-CN"
alt: "可选替代标题"
layout: /src/layouts/HandbookLayout.astro
updateDate: "2025-01-03"
---

**核心摘要：**
> 
>本小节核心观点、方法或结论简要总结。可多行，便于读者快速把握重点。

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
    <div class="overview-item">
      <h4>小节要点3</h4>
      <p>保持2空格缩进，HTML标签间无空行。</p>
    </div>
    <div class="overview-item">
      <h4>小节要点4</h4>
      <p>支持弹性扩展，可增减卡片数量。</p>
    </div>
  </div>
</div>

## 1. 主要内容标题

正文内容，支持Markdown与HTML混排。

### 1.1 子标题

正文内容描述。

### 1.2 公式展示示例

<div class="info-block">
  <div class="info-title">公式/算法标题</div>
  <div class="info-content">
    <div class="formula-display">
      公式内容 = (参数1 + 参数2) / 参数3
    </div>
  </div>
  <div class="info-explanation">
    公式说明、推导过程、应用场景等补充信息。
  </div>
</div>

### 1.3 数据表格示例

<div class="info-block">
  <div class="info-title">数据表格标题</div>
  <div class="info-content">
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>项目</th>
            <th>数值1</th>
            <th>数值2</th>
            <th>评级</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>指标A</td>
            <td class="positive">15.2%</td>
            <td>12.8%</td>
            <td><span class="rating excellent">优秀</span></td>
          </tr>
          <tr>
            <td>指标B</td>
            <td class="negative">-5.1%</td>
            <td>-2.3%</td>
            <td><span class="rating warning">注意</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="info-explanation">
    表格数据说明、来源、计算方法等。
  </div>
</div>

### 1.4 图片展示示例

<div class="info-block">
  <div class="info-title">图片标题</div>
  <div class="info-content">
    <div class="image-container">
      <img src="/images/example.png" alt="图片描述" class="responsive-image" />
      <div class="image-caption">
        图1: 图片说明（数据来源：来源名称）
      </div>
    </div>
  </div>
  <div class="info-explanation">
    图片相关说明、分析、结论等。
  </div>
</div>

### 1.5 代码示例

<div class="info-block">
  <div class="info-title">代码示例标题</div>
  <div class="info-content">
    <div class="code-block">
      <div class="code-header">
        <span class="language">Python</span>
        <button class="copy-btn">复制代码</button>
      </div>
      <pre><code class="language-python">
# 示例代码
def example_function(param1, param2):
    """
    函数说明
    """
    result = param1 + param2
    return result

# 使用示例
result = example_function(10, 20)
print(result)
      </code></pre>
    </div>
  </div>
  <div class="info-explanation">
    代码说明、功能介绍、使用方法等。
  </div>
</div>

## 2. 警告提示示例

<div class="warning-block">
  <div class="warning-icon">⚠️</div>
  <div class="warning-content">
    <div class="warning-title">重要提示</div>
    <div class="warning-text">
      这里是重要的警告或提示信息，需要读者特别注意的内容。
    </div>
  </div>
</div>

## 3. 成功案例示例

<div class="success-block">
  <div class="success-icon">✅</div>
  <div class="success-content">
    <div class="success-title">成功案例</div>
    <div class="success-text">
      这里是成功案例的描述，展示积极的结果或正面的经验。
    </div>
  </div>
</div>

## 4. 参考文献

<div class="reference-block">
  <div class="reference-title">参考文献</div>
  <div class="reference-list">
    <div class="reference-item">
      [1] 作者名. (年份). 文献标题. 出版社或期刊名.
    </div>
    <div class="reference-item">
      [2] 作者名. (年份). 文献标题. 网站名称. URL链接.
    </div>
  </div>
</div>

<!--
【使用说明】
1. 复制此模板创建新的小节页面
2. 修改frontmatter中的title、description等信息
3. 编写核心摘要，保持引用格式
4. 根据内容调整章节导航的overview-item数量
5. 选择合适的内容模块：info-block、warning-block、success-block等
6. 严格遵守2空格缩进、HTML标签间无空行的格式规范
7. 完整的格式说明和示例请参考：K.1 小节页面模板指南
--> 