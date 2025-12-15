# 代码嵌入自动更新功能验证

## ✅ 功能确认

**是的，代码文件修改后，网页端会自动更新！**

## 🔧 实现机制

### 1. Vite插件监控

在 `astro.config.mjs` 中已配置：

```javascript
import viteCodeLibraryWatcher from './src/plugins/vite-code-library-watcher-working.mjs';

vite: {
  plugins: [viteCodeLibraryWatcher()],
  // ...
}
```

### 2. 监控机制

插件使用以下机制实现自动更新：

1. **Vite原生监控**：使用 `server.watcher.add()` 直接让Vite监控代码库目录
2. **文件变化检测**：监听 `server.watcher.on('change')` 事件
3. **精确匹配**：只更新包含该代码文件的Markdown页面
4. **HMR触发**：通过多种方式触发HMR更新：
   - `moduleGraph.invalidateModule()` - 失效模块
   - `watcher.emit('change')` - 触发文件变化事件
   - 文件时间戳更新（降级方案）

### 3. 工作流程

```
1. 修改代码文件 (code_library/*.py)
   ↓
2. Vite检测到文件变化（通过server.watcher.add()）
   ↓
3. 等待200ms确保文件保存完成
   ↓
4. 防抖处理（500ms延迟）
   ↓
5. 查找包含该代码文件的所有Markdown文件
   ↓
6. 更新Markdown文件时间戳
   ↓
7. 触发HMR更新
   ↓
8. Astro重新构建相关页面
   ↓
9. Remark插件重新执行
   ↓
10. 读取最新代码文件
   ↓
11. 页面自动更新 ✅
```

## 📋 验证步骤

### 步骤1：启动开发服务器

```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension/AShare-manual
npm run dev
```

### 步骤2：检查启动日志

应该看到以下日志：

```
[vite-code-library-watcher] 🚀 插件开始初始化...
[vite-code-library-watcher] ✅ 使用已知路径: /home/taotao/dev/QuantTest/TRQuant
[vite-code-library-watcher] 📂 当前工作目录: /path/to/AShare-manual
[vite-code-library-watcher] 📂 项目根目录: /home/taotao/dev/QuantTest/TRQuant
[vite-code-library-watcher] 📂 代码库路径: /home/taotao/dev/QuantTest/TRQuant/code_library
[vite-code-library-watcher] ✅ 开始监控: /home/taotao/dev/QuantTest/TRQuant/code_library
[vite-code-library-watcher] ✅ 已添加到Vite监控: /home/taotao/dev/QuantTest/TRQuant/code_library
```

### 步骤3：打开包含代码的页面

在浏览器中打开包含 `<CodeFromFile>` 标签的页面，例如：
- 第3章3.1节：趋势分析（包含SMA、EMA、MACD等指标）
- 第3章3.2节：市场状态判断（包含价格、成交量、情绪、技术维度分析）

### 步骤4：修改代码文件

在编辑器中修改代码文件，例如：

```bash
# 修改SMA计算函数
vim code_library/003_Chapter3_Market_Analysis/3.1/code_3_1_1_calculate_sma.py

# 添加一行注释
echo "# 测试自动更新 - $(date)" >> code_library/003_Chapter3_Market_Analysis/3.1/code_3_1_1_calculate_sma.py
```

保存文件（Ctrl+S）

### 步骤5：观察控制台日志

应该看到以下日志：

```
[vite-code-library-watcher] 📝 Vite检测到代码文件变化: 003_Chapter3_Market_Analysis/3.1/code_3_1_1_calculate_sma.py
[vite-code-library-watcher] 🔍 查找包含代码文件的Markdown: 003_Chapter3_Market_Analysis/3.1/code_3_1_1_calculate_sma.py
[vite-code-library-watcher] 📄 找到相关文件: src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.1_Trend_Analysis_CN.md
[vite-code-library-watcher] ✅ 找到 1 个相关Markdown文件
[vite-code-library-watcher] ✅ 已更新文件时间戳: src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.1_Trend_Analysis_CN.md
[vite-code-library-watcher] ✅ 已触发文件变化事件: src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.1_Trend_Analysis_CN.md
[vite-code-library-watcher] ✅ 已失效模块: src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.1_Trend_Analysis_CN.md
```

### 步骤6：检查浏览器

- **页面应该自动刷新**（无需手动刷新）
- **代码内容应该已更新**（显示最新的代码）
- **代码高亮应该正常**（Shiki语法高亮）

## 🎯 验证要点

### ✅ 成功标志

1. **控制台日志**：看到文件变化检测和HMR更新日志
2. **页面自动刷新**：浏览器页面自动更新，无需手动刷新
3. **代码内容更新**：代码显示最新修改的内容
4. **无错误**：控制台没有错误信息

### ❌ 如果未更新

如果页面没有自动更新，检查以下几点：

1. **开发服务器是否运行**：确保 `npm run dev` 正在运行
2. **插件是否加载**：检查启动日志中是否有插件初始化信息
3. **路径是否正确**：检查日志中的代码库路径是否正确
4. **文件是否保存**：确保文件已保存（Ctrl+S）
5. **Markdown文件是否包含CodeFromFile标签**：确保Markdown文件中使用了 `<CodeFromFile>` 标签

## 🔍 调试方法

### 1. 检查插件配置

```bash
# 检查astro.config.mjs
cat extension/AShare-manual/astro.config.mjs | grep vite-code-library-watcher
```

### 2. 检查代码库路径

```bash
# 验证代码库路径是否存在
ls -la /home/taotao/dev/QuantTest/TRQuant/code_library
```

### 3. 手动触发测试

```bash
# 修改测试文件
echo "# 测试 $(date)" >> code_library/003_Chapter3_Market_Analysis/3.1/code_3_1_1_calculate_sma.py
```

### 4. 查看浏览器控制台

打开浏览器开发者工具（F12），查看：
- **Console标签**：是否有错误信息
- **Network标签**：是否有HMR相关的WebSocket消息

## 📊 当前状态

- ✅ **Vite插件已配置**：`vite-code-library-watcher-working.mjs`
- ✅ **路径已修复**：直接使用已知路径 `/home/taotao/dev/QuantTest/TRQuant/code_library`
- ✅ **监控机制已实现**：使用Vite原生监控 + 事件监听
- ✅ **HMR更新已实现**：多重保障机制确保更新

## 🎉 结论

**代码文件修改后，网页端会自动更新！**

只要：
1. 开发服务器正在运行
2. 代码文件在 `code_library` 目录下
3. Markdown文件使用了 `<CodeFromFile>` 标签

修改代码文件并保存后，相关页面会自动更新，无需手动刷新。

---

**更新时间**: 2025-12-13  
**版本**: 工作版 - 已验证  
**状态**: ✅ 功能正常

