# 代码嵌入功能实现研究

## 🔍 研究目标

实现Astro中代码嵌入功能，要求：
1. 代码与文档分离
2. 代码更新后文档自动显示最新版本
3. 支持Shiki代码高亮
4. 支持设计原理展示

## 📚 技术调研

### 1. Astro Markdown处理流程

```
Markdown文件
  ↓
Remark插件（AST转换）
  ↓
Rehype插件（HTML转换）
  ↓
Shiki代码高亮
  ↓
最终HTML
```

### 2. Remark插件工作原理

Remark插件工作在AST（抽象语法树）层面，可以：
- 访问和修改AST节点
- 替换节点
- 插入新节点

### 3. 关键问题

**问题1：如何生成代码块节点？**

Astro使用Shiki处理代码高亮，Shiki只处理Markdown代码块（`type: 'code'`），不处理HTML代码块。

**解决方案**：在Remark插件中生成AST代码块节点，而不是HTML节点。

### 4. 实现方案对比

#### 方案A：直接生成HTML（当前问题）
```javascript
node.value = `<pre><code>...</code></pre>`;
```
- ❌ 绕过了Shiki，没有代码高亮
- ✅ 简单直接

#### 方案B：生成AST代码块节点（推荐）
```javascript
parent.children.splice(index, 1, {
  type: 'code',
  lang: 'python',
  value: codeContent
});
```
- ✅ Shiki自动处理代码高亮
- ✅ 符合Astro的处理流程
- ⚠️ 需要正确处理AST节点替换

#### 方案C：生成Markdown文本（备选）
```javascript
node.value = `\`\`\`python\n${codeContent}\n\`\`\``;
```
- ⚠️ 需要重新解析，可能有问题
- ❌ 设计原理HTML无法混合

## 🎯 最佳实践

### 1. AST节点结构

```javascript
{
  type: 'code',
  lang: 'python',      // 语言标识
  value: 'code...',    // 代码内容
  meta: null           // 元数据（可选）
}
```

### 2. 节点替换方法

```javascript
// 使用visit获取parent和index
visit(tree, 'html', (node, index, parent) => {
  // 替换节点
  parent.children.splice(index, 1, ...newNodes);
});
```

### 3. 设计原理展示

设计原理需要HTML格式，可以：
- 先插入HTML节点（设计原理）
- 再插入代码块节点（代码）
- 两个节点顺序排列

## 🔧 实现细节

### 关键代码

```javascript
// 1. 查找CodeFromFile标签
visit(tree, 'html', (node, index, parent) => {
  const match = node.value.match(/<CodeFromFile\s+([^>]*)\s*\/?>/);
  if (match) {
    codeNodes.push({ node, index, parent, attrs: match[1] });
  }
});

// 2. 读取代码文件
const codeContent = await readFile(fullPath, 'utf-8');

// 3. 创建节点数组
const nodesToInsert = [];
if (showDesignPrinciples && designPrinciples) {
  nodesToInsert.push({
    type: 'html',
    value: formatDesignPrinciples(designPrinciples)
  });
}
nodesToInsert.push({
  type: 'code',
  lang: language,
  value: cleanCode
});

// 4. 替换节点
if (parent && typeof index === 'number') {
  parent.children.splice(index, 1, ...nodesToInsert);
}
```

## 📖 参考资源

### 官方文档
- [Astro Markdown Content](https://docs.astro.build/en/guides/markdown-content/)
- [Remark Plugins](https://github.com/remarkjs/remark/blob/main/doc/plugins.md)
- [Shiki Documentation](https://shiki.matsu.io/)

### 相关项目
- [remark-code-blocks](https://github.com/remarkjs/remark-code-blocks)
- [Astro Code Examples](https://github.com/withastro/astro/tree/main/examples)

## ✅ 验证要点

1. **AST节点替换**：确保parent和index正确
2. **代码高亮**：验证Shiki是否处理代码块
3. **设计原理**：HTML节点是否正确显示
4. **路径解析**：代码文件路径是否正确
5. **错误处理**：文件不存在时的错误提示

## 🚀 下一步

1. 修复AST节点替换逻辑
2. 测试代码高亮功能
3. 验证设计原理显示
4. 优化错误处理

