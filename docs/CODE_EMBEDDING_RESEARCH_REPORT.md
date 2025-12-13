# 代码嵌入功能实现研究报告

**研究时间**: 2025-12-13  
**研究员**: 轩辕剑灵（AI Assistant）  
**研究目标**: 实现Astro中代码嵌入功能，支持代码高亮和自动更新

## 🔍 问题分析

### 当前问题
1. **代码高亮缺失**：生成的HTML代码块绕过了Shiki，没有语法高亮
2. **显示错误**：代码块格式不正确，显示为纯文本
3. **设计原理显示**：需要同时支持HTML（设计原理）和代码块（代码）

### 根本原因
- Remark插件直接生成HTML `<pre><code>`，绕过了Astro的Shiki处理流程
- Shiki只处理AST中的`code`类型节点，不处理HTML代码块

## 📚 技术调研结果

### 1. Astro Markdown处理流程

```
Markdown文件
  ↓
Remark插件（AST转换层）
  ├─ 可以修改AST节点
  ├─ 可以替换节点
  └─ 可以插入新节点
  ↓
Rehype插件（HTML转换层）
  ↓
Shiki代码高亮（处理code类型节点）
  ↓
最终HTML输出
```

### 2. 关键发现

#### 发现1：Shiki处理机制
- Shiki在Rehype阶段处理代码高亮
- 只处理AST中的`type: 'code'`节点
- 不处理HTML中的`<pre><code>`标签

#### 发现2：AST节点结构
```javascript
// 代码块节点结构
{
  type: 'code',
  lang: 'python',      // 语言标识（必需）
  value: 'code...',    // 代码内容（必需）
  meta: null           // 元数据（可选）
}

// HTML节点结构
{
  type: 'html',
  value: '<div>...</div>'
}
```

#### 发现3：节点替换方法
```javascript
// 使用visit获取parent和index
visit(tree, 'html', (node, index, parent) => {
  // 从后往前处理，避免索引变化
  // 替换节点
  parent.children.splice(index, 1, ...newNodes);
});
```

### 3. 参考资源

#### 官方文档
- [Astro Markdown Content](https://docs.astro.build/en/guides/markdown-content/)
- [Remark Plugins](https://github.com/remarkjs/remark/blob/main/doc/plugins.md)
- [Shiki Documentation](https://shiki.matsu.io/)

#### 相关项目
- [remark-code-blocks](https://github.com/mrzmmr/remark-code-block) - 提取代码块
- [Astro Examples](https://github.com/withastro/astro/tree/main/examples)

## ✅ 解决方案

### 方案：生成AST代码块节点

**核心思路**：
1. 在Remark插件中生成AST `code`节点，而不是HTML
2. 设计原理作为HTML节点单独插入
3. 两个节点顺序排列，让Shiki处理代码块

### 实现代码

```javascript
// 1. 查找CodeFromFile标签
visit(tree, 'html', (node, index, parent) => {
  const match = node.value.match(/<CodeFromFile\s+([^>]*)\s*\/?>/);
  if (match) {
    codeNodes.push({ node, index, parent, attrs: match[1] });
  }
});

// 2. 从后往前处理（避免索引变化）
for (let i = codeNodes.length - 1; i >= 0; i--) {
  const { node, index, parent, attrs } = codeNodes[i];
  
  // 3. 读取代码文件
  const codeContent = await readFile(fullPath, 'utf-8');
  
  // 4. 创建节点数组
  const nodesToInsert = [];
  
  // 4.1 设计原理（HTML节点）
  if (showDesignPrinciples && designPrinciples) {
    nodesToInsert.push({
      type: 'html',
      value: formatDesignPrinciples(designPrinciples)
    });
  }
  
  // 4.2 代码块（AST节点，让Shiki处理）
  nodesToInsert.push({
    type: 'code',
    lang: language,
    value: cleanCode,
    meta: null
  });
  
  // 5. 替换节点
  if (parent && typeof index === 'number') {
    parent.children.splice(index, 1, ...nodesToInsert);
  }
}
```

## 🎯 关键要点

### 1. AST节点类型
- **`code`节点**：让Shiki处理代码高亮
- **`html`节点**：用于设计原理展示

### 2. 节点替换顺序
- 从后往前处理，避免索引变化
- 使用`parent.children.splice`替换节点

### 3. 设计原理处理
- 设计原理作为HTML节点单独插入
- 代码块作为AST节点插入
- 两个节点顺序排列

## 🔧 实现细节

### 文件结构
```
extension/AShare-manual/
├── src/
│   └── plugins/
│       └── remark-code-from-file-v2.mjs  # 修复后的插件
└── astro.config.mjs                      # 注册插件
```

### 配置
```javascript
// astro.config.mjs
import remarkCodeFromFile from './src/plugins/remark-code-from-file-v2.mjs';

export default defineConfig({
  markdown: {
    remarkPlugins: [remarkCodeFromFile],
    syntaxHighlight: {
      type: 'shiki',  // 使用Shiki处理代码高亮
    }
  }
});
```

## ✅ 验证要点

1. **AST节点替换**：确保parent和index正确
2. **代码高亮**：验证Shiki是否处理代码块
3. **设计原理**：HTML节点是否正确显示
4. **路径解析**：代码文件路径是否正确
5. **错误处理**：文件不存在时的错误提示

## 🚀 下一步行动

1. ✅ 修复AST节点替换逻辑
2. ⏳ 测试代码高亮功能
3. ⏳ 验证设计原理显示
4. ⏳ 优化错误处理
5. ⏳ 按章节迁移代码

## 📊 研究总结

### 成功要点
- ✅ 理解了Astro的Markdown处理流程
- ✅ 找到了Shiki代码高亮的工作原理
- ✅ 确定了AST节点替换的正确方法
- ✅ 设计了设计原理和代码块的混合方案

### 技术难点
- ⚠️ AST节点替换需要正确处理parent和index
- ⚠️ 从后往前处理避免索引变化
- ⚠️ HTML节点和代码块节点的混合使用

### 最佳实践
1. 使用AST节点而不是HTML，让Shiki处理代码高亮
2. 设计原理使用HTML节点，代码使用AST节点
3. 从后往前处理节点，避免索引问题
4. 完善的错误处理和路径解析

---

**研究完成时间**: 2025-12-13  
**状态**: ✅ 研究完成，方案确定，准备实施

