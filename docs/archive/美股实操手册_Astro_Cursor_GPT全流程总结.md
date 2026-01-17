
# 《美股投资实操手册》Astro + Cursor + GPT 项目构建完整流程文档

---

## 🧭 一、项目目标与核心定位

本项目目标是将原始 Word 文档版的《美股投资实操手册》转化为可交互、结构清晰、可集成 GPT / 回测 / 实盘系统的现代化金融教育平台。

核心需求包括：

- ✅ 每章内容结构化呈现（Markdown 格式）
- ✅ 支持 GPT 插入提示框与图表组件
- ✅ 使用 Astro 构建静态站点，支持中文命名
- ✅ 使用 Cursor + GPT 提高写作与开发效率
- ✅ 支持未来接入量化回测与实盘执行系统

---

## 🧱 二、手册 Markdown 构建阶段（Day 1）

### 📂 内容初始化

- 将原始 Word 文档拆分为独立章节
- 每章转为 UTF-8 编码的 `.md` 文件
- 命名格式：`001_序言.md`、`002_第一章：xxx.md`

### ✍️ 标准结构设计（每章 md）

```markdown
---
title: 第一章：xxx
layout: ../layouts/HandbookLayout.astro
slug: /chapter-001
---

# 第一章：xxx

:::gpt-tip
- 提示1
- 提示2
:::

<ChartPlaceholder title="图表标题" />

## 小节标题

正文内容...

[返回首页](../index.md)
```

---

## 🖥️ 三、Astro 项目搭建（Day 1）

- 使用命令初始化 Astro 项目：

```bash
npm create astro@latest
```

- 目录结构如下：

```
src/
├─ pages/               # 所有章节 Markdown 页面
├─ layouts/
│    └─ HandbookLayout.astro
├─ styles/
│    └─ global.css
astro.config.mjs
package.json
```

- 运行项目：

```bash
npm install
npm run dev
```

访问 `http://localhost:4321/` 查看站点页面。

---

## 🔁 四、slug 路由规范与链接跳转（Day 2）

### 🔧 问题：

Astro 默认以中文文件名作为 URL，会导致 `/第二章：xxx` 报 404。

### ✅ 解决方案：

在每个 `.md` 的 YAML 区增加 `slug` 字段：

```yaml
slug: /chapter-002
```

并在跳转时统一使用 slug：

```markdown
[下一章](../chapter-003)
```

我们定义了如下 slug 映射规范：

- `/preface` → 序言
- `/chapter-001` ~ `/chapter-010` → 正文
- `/appendix` → 附录
- `/example-001` ~ `/example-006` → 示例页

同时生成了 `slug_映射对照表.md` 供全局管理。

---

## 🧠 五、Cursor 中的开发技巧（Day 2~3）

### ✅ 内容协作

- 使用 `Ctrl + K` 调出 GPT 提示
- 右键段落 → Ask GPT
- 自动摘要、提问、生成策略代码、改写风格

### ✅ 批量操作技巧

- `Ctrl + Shift + F`：多文件全局搜索
- 批量修改 title、slug、跳转链接

### ✅ 调试技巧

- Terminal 输入 `npm run dev`
- 输入 `ls` 确认是否在项目根目录
- 若卡住：删除 node_modules 并重新安装依赖

---

## 🎨 六、页面样式与布局调整

- 修改 `global.css` 设置统一背景颜色：

```css
body {
  @apply bg-green-100;
}
```

- 或在 `HandbookLayout.astro` 中：

```astro
<main class="bg-green-100 px-6 py-8">
  <slot />
</main>
```

---

## 🔗 七、目录导航页与章节跳转（建议）

生成 `index.md` 目录页，结构如下：

```markdown
# 手册目录

- [序言](../preface)
- [第一章：xxx](../chapter-001)
- [第二章：xxx](../chapter-002)
...
```

也支持顶部导航组件：`<NavBar />`

---

## 📦 八、文件成果与打包输出

已生成：

- ✅ 所有章节标准 Markdown 模板（含 GPT 提示与图表占位）
- ✅ slug 映射对照表 Markdown
- ✅ Astro 项目 zip 包（可部署）

---

## 🔮 九、未来扩展方向

| 模块 | 可拓展功能 |
|------|-------------|
| 📈 图表集成 | TradingView iframe、绘图组件 |
| 📊 数据回测 | QuantConnect 策略页面嵌入 |
| 🧠 智能问答 | GPT 问答模块嵌入页面（章节理解、策略诊断） |
| 🧾 策略模拟 | GPT 生成策略 → QuantConnect 回测 → IBKR 实盘 |
| 📱 多端适配 | 移动端 UI 优化，支持 PWA、小程序等 |

---

## ✅ 十、你已掌握的能力总结

- 内容结构化编写与发布（.md）
- Astro + Tailwind 样式与组件控制
- Cursor + GPT 辅助编辑与开发
- slug 路由设计与多页面跳转
- 本地运行、调试、打包与部署能力

你已进入 **AI+内容+技术+金融系统开发的黄金工作流**！
