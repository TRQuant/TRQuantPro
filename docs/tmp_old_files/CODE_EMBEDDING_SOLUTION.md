# Astro代码嵌入解决方案

## 🎯 问题分析

### 原始问题
在Markdown文件的frontmatter中使用`import`语句会导致Astro构建失败，因为：
1. Markdown的frontmatter必须是纯YAML格式
2. 不能包含JavaScript/TypeScript的import语句
3. Astro的Markdown处理器不支持在frontmatter中导入组件

### 错误信息
```
[astro:markdown] Could not load ... end of the stream or a document separator is expected
```

## ✅ 解决方案

### 方案：自定义Remark插件

创建一个remark插件，在Markdown处理阶段自动读取代码文件并嵌入。

### 实现步骤

#### 1. 创建Remark插件

文件：`src/plugins/remark-code-from-file.mjs`

```javascript
import { readFile } from 'fs/promises';
import { join } from 'path';
import { visit } from 'unist-util-visit';

export default function remarkCodeFromFile() {
  return async (tree, file) => {
    // 查找所有 <CodeFromFile> 标签
    visit(tree, 'html', (node) => {
      const match = node.value.match(/<CodeFromFile\s+([^>]*)\s*\/?>/);
      if (match) {
        // 处理代码嵌入
        // ...
      }
    });
  };
}
```

#### 2. 在astro.config.mjs中注册插件

```javascript
import remarkCodeFromFile from './src/plugins/remark-code-from-file.mjs';

export default defineConfig({
  markdown: {
    remarkPlugins: [remarkCodeFromFile],
    // ...
  }
});
```

#### 3. 在Markdown中使用

```markdown
---
title: "3.2 市场状态"
---

价格指标反映市场的基本走势：

<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>
```

## 🔧 工作原理

### 构建时处理

1. **Markdown解析**：Astro解析Markdown文件
2. **插件处理**：remark插件识别`<CodeFromFile>`标签
3. **文件读取**：插件读取指定的代码文件
4. **内容处理**：提取设计原理，格式化代码
5. **HTML生成**：生成格式化的HTML代码块
6. **替换节点**：替换原始标签为生成的HTML

### 路径解析

```javascript
// 从 extension/AShare-manual 向上找到 TRQuant 根目录
let projectRoot = process.cwd();
if (projectRoot.includes('AShare-manual')) {
  const parts = projectRoot.split('AShare-manual');
  projectRoot = parts[0];
}
const fullPath = join(projectRoot, filePath);
```

## 📋 使用方式

### 基本用法

```markdown
<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
/>
```

### 完整参数

```markdown
<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>
```

### 参数说明

- `filePath`（必需）：代码文件路径，相对于TRQuant项目根目录
- `language`（可选）：编程语言，默认 "python"
- `showDesignPrinciples`（可选）：是否显示设计原理，默认 "true"

## 🎨 功能特性

### 1. 自动提取设计原理

从代码注释中提取设计原理说明：

```python
def analyze_price_dimension(data: pd.DataFrame) -> Dict[str, float]:
    """
    分析价格维度
    
    **设计原理**：
    - **多周期分析**：同时分析1日、5日、20日涨跌幅
    - **相对位置**：计算价格在近期高低点之间的相对位置
    """
    # ...
```

### 2. 代码格式化

自动生成格式化的HTML代码块，包含：
- 设计原理展示区域
- 代码高亮
- 样式支持

### 3. 错误处理

如果代码文件不存在或读取失败，显示友好的错误信息：

```html
<div class="code-error">
  <p>⚠️ 无法加载代码文件: xxx. 错误: xxx</p>
</div>
```

## 🔄 工作流程

```
1. 修改代码文件
   ↓
2. 保存到 code_library/
   ↓
3. 运行 npm run build
   ↓
4. Remark插件自动读取最新代码
   ↓
5. 文档显示最新代码
```

## ✅ 优势

1. **无需import**：Markdown文件中不需要import语句
2. **自动更新**：代码更新后，重新构建即可显示最新版本
3. **设计原理展示**：自动提取和显示设计原理
4. **错误处理**：友好的错误提示
5. **路径自动解析**：自动处理项目路径

## 🚀 下一步

1. 按章节顺序迁移所有代码块
2. 建立代码更新流程
3. 建立代码审查机制
4. 优化插件性能

