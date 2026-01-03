# 代码嵌入自动更新 - 工作版解决方案

## 🎯 核心问题

**代码文件保存后没有触发监控和自动更新，但重启后网页会有更新。**

这说明：
- ✅ Remark插件工作正常（重启后能看到更新）
- ❌ 文件监控没有正确触发
- ❌ 或者触发了但没有正确更新Markdown文件

## ✅ 工作版解决方案

### 关键改进

#### 1. 使用Vite的 `server.watcher.add()` 方法

**这是最可靠的方法**，直接让Vite监控外部目录：

```javascript
// 添加代码库目录到Vite的监控列表
server.watcher.add(codeLibraryPath);
```

**优势**：
- Vite原生支持，最可靠
- 自动处理文件变化事件
- 自动触发HMR更新

#### 2. 修复路径计算问题

**问题**：之前的路径计算可能不正确

**解决**：
```javascript
function getProjectRoot() {
  let root = process.cwd();
  
  if (root.includes('AShare-manual')) {
    const parts = root.split('/AShare-manual');
    root = parts[0];
  } else if (root.includes('extension')) {
    const parts = root.split('/extension');
    root = parts[0];
  }
  
  return resolve(root); // 使用resolve确保绝对路径
}
```

#### 3. 双重监控机制

1. **Vite原生监控**：使用 `server.watcher.add()`
2. **Vite事件监听**：监听 `server.watcher.on('change')`
3. **handleHotUpdate钩子**：处理Vite检测到的文件变化

#### 4. 文件保存完成检测

```javascript
// 在handleHotUpdate中，等待文件保存完成
await new Promise(resolve => setTimeout(resolve, 200));
```

## 🎯 完整工作流程

```
1. 用户保存文件 (Ctrl+S)
   ↓
2. Vite的watcher检测到文件变化（通过server.watcher.add()）
   ↓
3. Vite触发 'change' 事件
   ↓
4. 插件监听器捕获事件
   ↓
5. 等待200ms确保文件保存完成
   ↓
6. 防抖处理（500ms延迟）
   ↓
7. 验证文件是否真正改变（文件大小/修改时间）
   ↓
8. 查找包含该代码文件的所有Markdown文件
   ↓
9. 更新Markdown文件时间戳
   ↓
10. 触发Vite文件变化事件（watcher.emit）
   ↓
11. 失效模块（moduleGraph.invalidateModule）
   ↓
12. Vite处理HMR更新
   ↓
13. Astro重新构建相关页面
   ↓
14. Remark插件重新执行
   ↓
15. 读取最新代码文件
   ↓
16. 页面自动更新 ✅
```

## 📋 关键代码

### 1. 添加到Vite监控

```javascript
configureServer(server) {
  const codeLibraryPath = join(projectRoot, 'code_library');
  
  // 关键：使用Vite的watcher.add()方法
  server.watcher.add(codeLibraryPath);
  
  // 监听Vite的watcher事件
  server.watcher.on('change', async (filePath) => {
    if (filePath.includes('code_library') && filePath.endsWith('.py')) {
      // 处理文件变化
      debouncedUpdate(filePath);
    }
  });
}
```

### 2. handleHotUpdate钩子

```javascript
handleHotUpdate({ file, server }) {
  if (file.includes('code_library') && file.endsWith('.py')) {
    // 触发相关Markdown文件的更新
    debouncedUpdate(file);
    return null; // 不阻止其他插件处理
  }
}
```

## 🔧 配置说明

### 路径计算

确保正确计算项目根目录：

```javascript
function getProjectRoot() {
  let root = process.cwd();
  
  // 处理不同的工作目录
  if (root.includes('AShare-manual')) {
    root = root.split('/AShare-manual')[0];
  } else if (root.includes('extension')) {
    root = root.split('/extension')[0];
  }
  
  return resolve(root); // 使用resolve确保绝对路径
}
```

### 文件保存完成检测

```javascript
// 在触发更新前，等待文件保存完成
await new Promise(resolve => setTimeout(resolve, 200));
```

## 📋 测试步骤

### 1. 重启开发服务器

```bash
cd extension/AShare-manual
pkill -f "astro dev"
npm run dev
```

### 2. 检查启动日志

应该看到：
```
[vite-code-library-watcher] 🚀 插件开始初始化...
[vite-code-library-watcher] 📂 当前工作目录: /path/to/AShare-manual
[vite-code-library-watcher] 📂 项目根目录: /path/to/TRQuant
[vite-code-library-watcher] 📂 代码库路径: /path/to/TRQuant/code_library
[vite-code-library-watcher] ✅ 开始监控: /path/to/TRQuant/code_library
[vite-code-library-watcher] ✅ 已添加到Vite监控: /path/to/TRQuant/code_library
```

### 3. 修改并保存代码文件

```bash
# 在编辑器中修改并保存文件
vim code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
# 按 :w 保存
```

### 4. 观察控制台日志

应该看到：
```
[vite-code-library-watcher] 📝 Vite检测到代码文件变化: 003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
[vite-code-library-watcher] 🔍 查找包含代码文件的Markdown: ...
[vite-code-library-watcher] 📄 找到相关文件: ...
[vite-code-library-watcher] ✅ 找到 1 个相关Markdown文件
[vite-code-library-watcher] ✅ 已更新文件时间戳: ...
[vite-code-library-watcher] ✅ 已触发文件变化事件: ...
[vite-code-library-watcher] ✅ 已失效模块: ...
```

### 5. 检查浏览器

- 页面应该自动刷新
- 代码内容应该已更新

## 🐛 故障排查

### 问题1：没有看到"已添加到Vite监控"日志

**原因**：`server.watcher.add()` 可能不可用

**解决**：
1. 检查Vite版本（需要支持watcher.add）
2. 检查控制台是否有错误
3. 使用备用方案（监听watcher事件）

### 问题2：看到"Vite检测到代码文件变化"但没有更新

**原因**：路径匹配可能失败

**解决**：
1. 检查Markdown文件中的 `filePath` 属性
2. 查看路径匹配日志
3. 确保路径格式正确

### 问题3：路径计算错误

**症状**：看到"代码库目录不存在"警告

**解决**：
1. 检查控制台中的路径日志
2. 手动验证路径是否正确
3. 调整路径计算逻辑

## 🎉 关键特性

- ✅ **使用Vite原生监控**：`server.watcher.add()` 最可靠
- ✅ **双重保障**：Vite监控 + 事件监听 + handleHotUpdate
- ✅ **文件保存检测**：等待200ms确保文件保存完成
- ✅ **路径修复**：正确计算项目根目录
- ✅ **详细日志**：每个步骤都有日志输出

---

**更新时间**: 2025-12-13  
**版本**: 工作版 - 使用Vite原生监控  
**状态**: ✅ 完整实现

