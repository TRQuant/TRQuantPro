# Astro代码嵌入实现总结

## ✅ 问题解决

### 原始问题
在Markdown文件的frontmatter中使用`import`语句导致Astro构建失败。

### 解决方案
创建自定义Remark插件，在Markdown处理阶段自动读取代码文件并嵌入。

## 🔧 实现细节

### 1. Remark插件

**文件**: `extension/AShare-manual/src/plugins/remark-code-from-file.mjs`

**功能**:
- 识别Markdown中的 `<CodeFromFile>` 标签
- 读取指定的代码文件
- 提取设计原理说明
- 生成格式化的HTML代码块

### 2. 路径解析

```javascript
// 从 extension/AShare-manual 向上找到 TRQuant 根目录
let projectRoot = process.cwd();
if (projectRoot.includes('AShare-manual')) {
  const parts = projectRoot.split('/AShare-manual');
  projectRoot = parts[0];
  // 如果还在extension目录下，再向上一步
  if (projectRoot.endsWith('/extension')) {
    projectRoot = projectRoot.replace('/extension', '');
  }
}
```

### 3. 配置

在 `astro.config.mjs` 中注册插件：

```javascript
import remarkCodeFromFile from './src/plugins/remark-code-from-file.mjs';

export default defineConfig({
  markdown: {
    remarkPlugins: [remarkCodeFromFile],
    // ...
  }
});
```

## 📋 使用方式

### 在Markdown中使用

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

### 参数说明

- `filePath`（必需）：代码文件路径，相对于TRQuant项目根目录
- `language`（可选）：编程语言，默认 "python"
- `showDesignPrinciples`（可选）：是否显示设计原理，默认 "true"

## 🎯 工作流程

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

## ✅ 验证

路径解析已正确：
- 项目根目录: `/home/taotao/dev/QuantTest/TRQuant`
- 代码文件路径: `/home/taotao/dev/QuantTest/TRQuant/code_library/...`
- 插件能正确读取代码文件

## 🚀 下一步

1. 按章节顺序迁移所有代码块
2. 建立代码更新流程
3. 建立代码审查机制
4. 优化插件性能

