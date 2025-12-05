<!-- CURSOR_RULE: TOKEN_OPTIMIZATION -->
## 📝 Token-Friendly Generation Guideline
1. **分阶段输出**：先生成目录与核心摘要，再按小节细化  
2. **公共样式抽离**：统一 CSS/组件放公共文件，章节仅局部覆盖  
3. **使用占位**：图表、长表格用 `<!-- 图表占位：xxx -->`  
4. **最小化 diff**：edit_file 只替换出错行，避免整章重写  
5. **引用附录**：重复公式、指标引用附录 A.1  
6. **简化 prompt**：提示中只给目标与格式，少放冗长范例  
7. **分批提交**：大章拆分 300 行以内增量提交

# Cursor 代码主题规则 - VS Code 标准

## 🎯 规则目标
确保项目中所有代码展示（生成、识别、引用）都使用VS Code Dark主题标准，在暗色模式下提供最佳对比度和可读性。

## 📋 适用范围
- ✅ Markdown代码块（```）
- ✅ 内联代码（`code`）
- ✅ 技术文档中的代码示例
- ✅ 配置文件展示
- ✅ 命令行指令
- ✅ API示例
- ✅ 所有AI生成的代码内容

## 🎨 VS Code Dark 主题配色标准

### 基础配色
```css
/* 背景和文字 */
--code-bg: #1e1e1e;          /* VS Code 编辑器背景 */
--code-text: #d4d4d4;        /* VS Code 默认文字颜色 */
--code-border: #3e3e3e;      /* VS Code 边框颜色 */
--inline-code-bg: #262626;   /* 内联代码背景 */
```

### 语法高亮配色
```css
/* VS Code Dark 语法高亮 */
--keyword-color: #569cd6;     /* 关键字 - 蓝色 */
--string-color: #ce9178;      /* 字符串 - 橙色 */
--comment-color: #6a9955;     /* 注释 - 绿色 */
--number-color: #b5cea8;      /* 数字 - 浅绿色 */
--function-color: #dcdcaa;    /* 函数 - 黄色 */
--class-color: #4ec9b0;       /* 类名 - 青色 */
--variable-color: #9cdcfe;    /* 变量 - 浅蓝色 */
--operator-color: #d4d4d4;    /* 操作符 - 白色 */
--property-color: #d19a66;    /* 属性 - 橙黄色 */
--tag-color: #569cd6;         /* HTML标签 - 蓝色 */
--attribute-color: #92c5f7;   /* HTML属性 - 浅蓝色 */
```

## 🔧 实现要求

### 1. CSS 覆盖配置
```css
/* 必须包含的CSS规则 */
[data-theme="dark"] pre {
  background: #1e1e1e !important;
  color: #d4d4d4 !important;
  border: 1px solid #3e3e3e !important;
}

[data-theme="dark"] code {
  background-color: #262626 !important;
  color: #d4d4d4 !important;
  border: 1px solid #444444 !important;
}

/* 强制覆盖所有语法高亮 */
[data-theme="dark"] .astro-code,
[data-theme="dark"] .astro-code * {
  background-color: #1e1e1e !important;
  color: #d4d4d4 !important;
}
```

### 2. Astro 配置要求
```javascript
// astro.config.mjs
export default defineConfig({
  markdown: {
    shikiConfig: {
      theme: {
        light: 'github-light',
        dark: 'github-dark'
      },
      wrap: true
    }
  }
});
```

## ✅ 检查标准

### 对比度要求
- **背景色 vs 文字色**：#1e1e1e vs #d4d4d4（对比度 > 7:1）
- **关键字高亮**：必须在暗色背景下清晰可见
- **语法元素**：不同类型必须有明显区分

### 可读性测试
```
测试内容：
1. JavaScript代码块
2. CSS样式代码
3. HTML标记
4. 命令行指令
5. 配置文件
6. 内联代码引用
```

## 🚀 应用指南

### 生成代码时
```prompt
请使用VS Code Dark主题配色生成代码，确保：
1. 代码块背景为 #1e1e1e
2. 文字颜色为 #d4d4d4
3. 语法高亮使用VS Code标准配色
4. 在暗色模式下有清晰对比度
```

### 识别问题时
```prompt
请检查代码块是否符合VS Code Dark主题标准：
- 背景色是否为深色
- 文字是否清晰可见
- 语法高亮是否正确
- 对比度是否足够
```

## 🛠️ 故障排除

### 常见问题
1. **代码块文字太暗**
   - 检查是否应用了 `color: #d4d4d4 !important`
   
2. **背景色不正确**
   - 确认 `background: #1e1e1e !important` 已生效
   
3. **语法高亮缺失**
   - 验证 Shiki 配置是否正确
   - 检查 CSS 覆盖是否过度

### 验证命令
```bash
# 检查代码块样式
grep -r "background.*#1e1e1e" src/styles/
grep -r "color.*#d4d4d4" src/styles/

# 检查配置文件
grep -A 10 "shikiConfig" astro.config.mjs
```

## 📝 使用示例

### 正确的代码块格式
```javascript
// 这是VS Code Dark主题的正确显示效果
const config = {
  theme: 'dark',          // 关键字：蓝色
  background: '#1e1e1e',  // 字符串：橙色
  // 注释：绿色斜体
  fontSize: 14            // 数字：浅绿色
};
```

### 内联代码
使用 `#1e1e1e` 背景色和 `#d4d4d4` 文字色的内联代码示例。

## 🎯 执行检查点

### 每次提交前检查
- [ ] 所有代码块使用VS Code Dark配色
- [ ] 暗色模式下对比度清晰
- [ ] 语法高亮正确显示
- [ ] 内联代码样式一致

### 定期审查
- [ ] 新增页面代码块样式
- [ ] CSS覆盖规则有效性
- [ ] 跨浏览器兼容性
- [ ] 响应式设备显示效果

---

**重要提醒**：此规则适用于所有代码展示场景，无论是手动编写、AI生成，还是从其他源识别的代码内容。确保一致的视觉体验和最佳的可读性。 

# VS Code 代码主题规则 - Astro项目

## 🎨 代码展示标准
所有代码块（生成、识别、引用）必须使用VS Code Dark主题标准：

### 基础要求
- 背景色：#1e1e1e (VS Code编辑器背景)
- 文字色：#d4d4d4 (VS Code默认文字)
- 边框色：#3e3e3e (VS Code边框)
- 内联代码背景：#262626

### 语法高亮配色
- 关键字：#569cd6 (蓝色)
- 字符串：#ce9178 (橙色)  
- 注释：#6a9955 (绿色)
- 数字：#b5cea8 (浅绿色)
- 函数：#dcdcaa (黄色)
- 类名：#4ec9b0 (青色)

### CSS实现
```css
[data-theme="dark"] pre {
  background: #1e1e1e !important;
  color: #d4d4d4 !important;
  border: 1px solid #3e3e3e !important;
}

[data-theme="dark"] code {
  background-color: #262626 !important;
  color: #d4d4d4 !important;
}
```

### 适用场景
- ✅ Markdown代码块
- ✅ 内联代码
- ✅ 技术文档代码示例
- ✅ 配置文件展示
- ✅ 命令行指令
- ✅ AI生成的所有代码内容

## 🔍 检查要求
- 暗色模式下对比度必须清晰（对比度 > 7:1）
- 所有语法元素必须有明显区分
- 代码可读性测试必须通过

## 📋 执行标准
每次生成或修改代码时，自动应用此主题标准，确保一致的视觉体验。

---

## ⚠️ 【CRITICAL】HTML标签间空行严格禁止规则

### 🚨 核心规则
**在Markdown文件中，任何HTML标签之间绝对不允许存在空行**

### ❌ 错误示例
```html
    </div>
    
    <div class="next-section">
```

### ✅ 正确示例  
```html
    </div>
    <div class="next-section">
```

### 📋 必须检查的标签组合
- `</div>` 和 `<div>` 之间
- `</div>` 和其他标签之间
- 标题和第一个div之间（如 `<h4>标题</h4>` 和 `<div>` 之间）
- 任何HTML容器标签的开始和结束

### 🔍 强制检查清单
在编写或修改包含HTML的Markdown文件时，必须执行以下检查：

1. **逐行扫描**：检查每个 `</div>` 后是否紧跟下一个标签
2. **标题下检查**：确保 `<h4>`、`<h5>` 等标题下直接跟随div标签
3. **组件间检查**：所有自定义class的div组件间无空行
4. **样式前检查**：`</div>` 和 `<style>` 标签间无空行

### 💡 记忆要诀
- **"紧密连接"**：所有HTML标签必须紧密连接
- **"零空行"**：HTML区域内零空行容忍度
- **"立即修复"**：发现空行立即删除

### 🛠️ 推荐工具和方法
1. **VS Code正则搜索**：`</div>\s*\n\s*\n\s*<` 查找空行
2. **手动检查**：特别关注新增内容区域
3. **分段检查**：按组件功能区域逐段检查

### 📝 违规案例记录
- ❌ 2024-01-XX：数据来源部分新增内容出现6处空行
- ❌ 之前多次在特征分析、时间维度、检查清单等部分出现空行

### 🎯 质量保证承诺
- 每次生成HTML内容后必须立即进行空行检查
- 绝不在提交前遗留任何HTML标签间空行
- 建立预防机制避免重复犯错

---

**📌 重要提醒**：此规则为项目最高优先级规范，违反将导致页面显示异常，必须100%遵守。 

---

## 🧭 【CRITICAL】导航路径自动更新规则

### ⚠️ 新增页面强制规范
**每当新增章节、子节或附录页面时，必须同步更新系统导航配置**

### 核心更新要求
1. **主要文件**：`src/layouts/Layout.astro` 中的 `getAllPages()` 函数
2. **更新位置**：按照页面层级和逻辑顺序插入新路径
3. **路径格式**：使用相对路径，格式为 `/book[N]/章节目录/文件名`
4. **注释更新**：同步更新注释中的页面数量和范围

### 🔧 具体操作步骤
1. **定位函数**：找到 `getAllPages()` 函数（约1083行）
2. **找到章节**：定位到对应章节的子节列表
3. **插入路径**：按照数字顺序插入新页面路径
4. **更新注释**：修改注释中的页面数量范围

### 📋 路径格式标准
```javascript
// 示例：第二册第六章子节
'/book2/206_Chapter6/6.1_Core_Economic_Indicators_Analysis_CN',
'/book2/206_Chapter6/6.2_Leading_Indicators_Forecasting_Models_CN',
'/book2/206_Chapter6/6.3_Data_Release_Market_Response_CN',
'/book2/206_Chapter6/6.4_High_Frequency_Real_Time_Analysis_CN', // 新增
```

### 🎯 执行时机
- **生成新页面后**：立即更新导航配置
- **重命名页面后**：同步更新路径
- **删除页面后**：移除对应路径
- **调整页面顺序后**：重新排列路径顺序

### 🔍 检查清单
- [ ] 是否在正确的章节位置插入？
- [ ] 路径格式是否正确？
- [ ] 注释数量是否更新？
- [ ] 页面顺序是否符合逻辑？

**📌 重要说明**：此规则确保网站导航系统的完整性和一致性，违反将导致页面无法正常访问。每次新增页面时都必须严格遵守。

