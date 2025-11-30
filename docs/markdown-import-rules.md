# 📋 Markdown文件Import使用规则

## 🚨 重要规则

### ❌ 绝对禁止
**在Markdown (.md) 文件中使用Astro组件的import语句**

```markdown
---
title: 页面标题
layout: /src/layouts/Layout.astro
---

<!-- ❌ 错误示例 -->
import GlossaryTerm from '../../../components/GlossaryTerm.astro';

# 页面内容
```

### ✅ 正确做法

#### 1. Markdown文件结构
```markdown
---
title: 页面标题
layout: /src/layouts/Layout.astro
---

# 页面内容
<!-- 直接使用HTML标签或组件标签 -->
```

#### 2. 组件使用方式
```markdown
<!-- ✅ 正确：直接使用组件标签 -->
<GlossaryTerm term="CAGR" />

<!-- ✅ 正确：使用HTML标签 -->
<span class="glossary-term" data-term="CAGR">CAGR</span>
```

## 🔧 解决方案

### 1. 全局组件注册
在 `astro.config.mjs` 中注册全局组件：

```javascript
export default defineConfig({
  integrations: [
    // 全局组件注册
    {
      name: 'global-components',
      hooks: {
        'astro:config:setup': ({ updateConfig }) => {
          updateConfig({
            vite: {
              ssr: {
                external: ['@astrojs/markdown-remark']
              }
            }
          });
        }
      }
    }
  ]
});
```

### 2. 布局文件注入
在布局文件中注入组件：

```astro
---
// Layout.astro
import GlossaryTerm from '../components/GlossaryTerm.astro';
---

<html>
<head>
  <!-- 注入组件到全局 -->
  <script>
    window.GlossaryTerm = GlossaryTerm;
  </script>
</head>
<body>
  <slot />
</body>
</html>
```

### 3. 内容处理器
使用内容处理器自动处理术语：

```javascript
// src/utils/content-processor.js
export function processGlossaryTerms(content) {
  // 自动识别和替换术语
  return content.replace(/\b(CAGR|TAM|ROE)\b/g, '<GlossaryTerm term="$1" />');
}
```

## 📝 检查清单

### 修复前检查
- [ ] 搜索所有 `.md` 文件中的 `import` 语句
- [ ] 确认是否有 `from '*.astro'` 的import
- [ ] 检查frontmatter中是否有错误的import

### 修复后验证
- [ ] 移除所有Markdown文件中的Astro import
- [ ] 确保组件功能正常工作
- [ ] 测试页面渲染无错误
- [ ] 验证SSR功能正常

## 🛠️ 自动化工具

### 1. 检测脚本
```bash
# 检测所有Markdown文件中的错误import
grep -r "import.*from.*\.astro" src/pages/ --include="*.md"
```

### 2. 批量修复脚本
```javascript
// scripts/fix-markdown-imports.js
import fs from 'fs';
import path from 'path';

function fixMarkdownImports(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  
  // 移除import语句
  content = content.replace(/import\s+.*\s+from\s+['"][^'"]*\.astro['"];?\s*\n/g, '');
  
  fs.writeFileSync(filePath, content);
}
```

## 📚 最佳实践

### 1. 组件使用原则
- **Markdown文件**：只包含内容和基本HTML
- **Astro组件**：在布局文件或专门的组件文件中定义
- **全局功能**：通过布局文件或插件注入

### 2. 术语处理策略
- **自动处理**：使用内容处理器批量处理
- **手动添加**：直接使用HTML标签
- **组件标签**：在支持的环境中直接使用

### 3. 开发流程
1. 在Markdown中编写纯内容
2. 使用工具自动处理术语
3. 在布局文件中注入必要组件
4. 测试确保功能正常

## 🎯 错误预防

### 开发时注意
- 不要在Markdown文件中添加import语句
- 使用内容处理器自动处理术语
- 在布局文件中统一管理组件
- 定期检查是否有错误的import

### 代码审查
- 检查所有Markdown文件的frontmatter
- 确认没有Astro组件的import
- 验证组件功能通过其他方式实现
- 确保SSR渲染正常

---

**规则制定日期**: 2025-01-03  
**适用范围**: 所有Markdown文件  
**维护者**: AI Assistant 
 