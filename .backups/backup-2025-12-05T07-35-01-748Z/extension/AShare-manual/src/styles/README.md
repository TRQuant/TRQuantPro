# 样式系统文档

## 📁 文件结构

```
src/styles/
├── style.css          # 主样式文件
├── components.css     # 组件样式库
└── README.md         # 本文档
```

## 🎨 VS Code 官方主题集成

### 主题特色
- **完整配色方案**：使用VS Code官方的Light Plus和Dark Plus主题
- **精确语法高亮**：支持20+种编程语言的Shiki语法高亮
- **智能主题切换**：根据系统主题或用户选择自动切换
- **响应式设计**：在所有设备上都有良好的显示效果
- **代码差异显示**：支持代码添加、删除、高亮、聚焦标记
- **缩进格式保持**：完美保持原始代码的缩进和格式

### 支持的语言
- **脚本语言**：Python, JavaScript, TypeScript, PHP, Ruby
- **标记语言**：HTML, CSS, SCSS, Less, Sass
- **数据库**：SQL, PostgreSQL, MySQL, MongoDB
- **系统脚本**：Bash/Shell, PowerShell, Batch
- **配置文件**：JSON, YAML, TOML, XML
- **文档格式**：Markdown, reStructuredText
- **编程语言**：C++, Java, C#, Go, Rust, Swift
- **以及更多**：总计支持100+种语言和文件格式

### 配色规范

#### 暗色主题 (Dark Modern)
```css
--editor-bg: #1e1e1e;           /* 编辑器背景 */
--editor-fg: #d4d4d4;           /* 默认文字 */
--keyword-color: #569cd6;       /* 关键字蓝 */
--string-color: #ce9178;        /* 字符串橙 */
--comment-color: #6a9955;       /* 注释绿 */
--number-color: #b5cea8;        /* 数字浅绿 */
--function-color: #dcdcaa;      /* 函数黄 */
--class-color: #4ec9b0;         /* 类型青 */
--variable-color: #9cdcfe;      /* 变量浅蓝 */
```

#### 亮色主题 (Light Modern)
```css
--editor-bg: #f6f8fa;           /* 编辑器背景 */
--editor-fg: #1f2328;           /* 默认文字 */
--keyword-color: #0000ff;       /* 关键字蓝 */
--string-color: #a31515;        /* 字符串红 */
--comment-color: #008000;       /* 注释绿 */
--number-color: #09885a;        /* 数字绿 */
--function-color: #795e26;      /* 函数棕 */
--class-color: #267f99;         /* 类型青 */
--variable-color: #001080;      /* 变量蓝 */
```

## 🚀 Shiki 语法高亮系统

### 核心特性
- **VS Code 主题**：使用官方的Light Plus和Dark Plus主题
- **双主题支持**：亮色/暗色模式自动切换
- **CSS变量驱动**：使用`--shiki-light`和`--shiki-dark`变量
- **转换器支持**：集成@shikijs/transformers增强功能
- **格式保持**：完美保持代码缩进和空白符

### 高级标记功能
```markdown
// [!code highlight]  - 高亮显示重要代码行
// [!code focus]      - 聚焦显示关键代码行
// [!code ++]         - 显示新增代码行（绿色）
// [!code --]         - 显示删除代码行（红色）
{1,3-5}              - 行号高亮（在代码块标题中）
```

### 技术实现
```typescript
// astro.config.mjs 配置示例
shikiConfig: {
  themes: {
    light: 'light-plus',
    dark: 'dark-plus'
  },
  transformers: [
    transformerNotationDiff(),
    transformerNotationHighlight(),
    transformerNotationFocus()
  ]
}
```

## 📋 代码复制功能

### 功能特点
- 🖱️ **智能显示**：鼠标悬停时显示复制按钮
- ⌨️ **快捷键支持**：`Ctrl+Shift+C` 快速复制
- ✅ **状态反馈**：复制成功后的视觉确认
- ♿ **无障碍支持**：键盘导航和屏幕阅读器支持
- 🔄 **降级处理**：API不可用时自动选择文本
- 📱 **响应式**：在移动设备上优化的触摸体验

### 使用方法

#### 鼠标操作
1. 将鼠标悬停在代码块上
2. 点击右上角出现的复制按钮
3. 按钮会显示"已复制"确认状态

#### 键盘快捷键
- `Ctrl+Shift+C`：复制当前焦点代码块
- `Tab`：导航到复制按钮
- `Enter` 或 `Space`：执行复制操作

#### 无障碍支持
- 所有按钮都有适当的ARIA标签
- 支持键盘导航
- 兼容屏幕阅读器
- 符合WCAG 2.1 AA标准

### 技术实现

#### 组件结构
```typescript
// CodeCopyButton.astro
interface CopyButtonProps {
  codeElement: HTMLElement;
  container: HTMLElement;
}

class CodeCopyManager {
  initCodeCopyButtons(): void;
  handleCopy(button: HTMLButtonElement, code: string): Promise<void>;
  handleThemeChange(): void;
}
```

#### CSS类名
```css
.code-container          /* 代码块容器 */
.copy-button            /* 复制按钮 */
.copy-button:hover      /* 悬停状态 */
.copy-button.copied     /* 复制成功状态 */
```

## 🧩 可视化组件库

### 1. 流程图组件
```html
<div class="framework-flow">
  <div class="flow-step">
    <div class="step-icon">🔍</div>
    <div class="step-title">步骤标题</div>
    <div class="step-desc">步骤描述</div>
  </div>
  <div class="flow-arrow">→</div>
</div>
```

### 2. 组件网格
```html
<div class="component-grid">
  <div class="component-card">
    <div class="component-icon">📊</div>
    <div class="component-name">组件名称</div>
    <div class="component-desc">组件描述</div>
  </div>
</div>
```

### 3. 多因子模型
```html
<div class="factor-model">
  <div class="factor-equation">
    <div class="factor-box">基本面因子</div>
    <div class="plus-sign">+</div>
    <div class="factor-box">技术面因子</div>
  </div>
</div>
```

### 4. 指标展示
```html
<div class="metrics-grid">
  <div class="metric-card">
    <div class="metric-value">15.2%</div>
    <div class="metric-label">年化收益</div>
    <div class="metric-benchmark">vs 11.8%</div>
  </div>
</div>
```

### 5. 标签系统
```html
<div class="indicator-grid">
  <div class="indicator-group">
    <div class="group-title">风险指标</div>
    <div class="group-items">
      <span class="indicator-tag">波动率</span>
      <span class="indicator-tag">最大回撤</span>
    </div>
  </div>
</div>
```

## 🎯 使用指南

### 组件选择表
| 场景 | 推荐组件 | 类名 |
|------|----------|------|
| 流程展示 | 流程图组件 | `.framework-flow` |
| 功能介绍 | 组件网格 | `.component-grid` |
| 数学模型 | 多因子模型 | `.factor-model` |
| 数据展示 | 指标展示 | `.metrics-grid` |
| 分类标签 | 标签系统 | `.indicator-grid` |

### 设计原则
1. **一致性**：使用统一的颜色、字体和间距
2. **简洁性**：避免过度装饰，突出内容
3. **响应式**：确保在所有设备上都能良好显示
4. **可访问性**：符合无障碍设计标准

### 技术要点
- **样式复用**：所有组件样式在`components.css`中统一管理
- **HTML结构**：使用语义化标签，便于SEO和无障碍访问
- **图标选择**：使用Unicode表情符号，确保跨平台兼容性
- **颜色系统**：基于CSS变量，支持主题切换

## 📱 响应式设计

### 断点设置
```css
/* 移动端 */
@media (max-width: 768px) {
  .component-grid {
    grid-template-columns: 1fr;
  }
}

/* 小屏幕 */
@media (max-width: 480px) {
  .copy-button {
    padding: 4px 8px;
    font-size: 11px;
  }
}
```

### 移动端优化
- 触摸友好的按钮尺寸（最小44px）
- 适中的字体大小和行高
- 简化的布局和导航
- 优化的加载性能

## 🔧 自定义和扩展

### 添加新主题
1. 在`components.css`中定义新的CSS变量
2. 创建对应的主题选择器
3. 更新主题切换逻辑

### 添加新组件
1. 在`components.css`中添加样式定义
2. 创建对应的Astro组件
3. 更新本文档的使用指南

### 性能优化
- 使用CSS变量减少重复代码
- 合理使用`!important`确保主题优先级
- 优化选择器性能
- 压缩和合并CSS文件

## 🐛 故障排除

### 常见问题

#### 代码复制不工作
1. 检查浏览器是否支持剪贴板API
2. 确认页面是HTTPS协议
3. 检查JavaScript是否正确加载

#### 主题切换异常
1. 检查CSS变量是否正确定义
2. 确认主题选择器的优先级
3. 清除浏览器缓存

#### 移动端显示问题
1. 检查响应式断点设置
2. 确认触摸事件是否正确绑定
3. 测试不同设备的兼容性

### 调试工具
- 浏览器开发者工具
- CSS变量检查器
- 响应式设计模式
- 无障碍测试工具

## 🚀 未来计划

### 即将添加的功能
- [ ] 更多编程语言的语法高亮支持
- [ ] 代码块的行号显示
- [ ] 代码搜索和高亮功能
- [ ] 主题自定义编辑器
- [ ] 代码块的折叠/展开功能

### 性能优化计划
- [ ] CSS文件的自动压缩
- [ ] 组件的懒加载
- [ ] 图标字体的优化
- [ ] 缓存策略的改进

---

如有问题或建议，请查看项目文档或提交Issue。 