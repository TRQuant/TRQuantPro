# 代码嵌入自动更新 v3 - 使用HMR API

## 🔍 问题分析

### 之前的问题
1. 修改Markdown文件时间戳的方式不够可靠
2. Astro可能不会检测到文件变化
3. 需要更直接的方法触发HMR更新

## ✅ v3 改进方案

### 核心改进

1. **使用 server.watch() API**
   - 直接通知Vite服务器文件变化
   - 触发HMR更新，而不是依赖文件时间戳

2. **更可靠的路径匹配**
   - 支持完整路径、相对路径、文件名三种匹配方式
   - 精确查找包含代码文件的Markdown文件

3. **降级方案**
   - 如果 `server.watch()` 不可用，回退到文件时间戳方式

### 关键代码

```javascript
// 使用 server.watch() 通知Vite文件变化
server.watch(fullPath);

// 降级方案：修改文件时间戳
const timestamp = `<!-- Code updated: ${new Date().toISOString()} -->`;
await writeFile(fullPath, updatedContent, 'utf-8');
```

## 🎯 工作流程

```
1. 修改代码文件 (code_library/*.py)
   ↓
2. chokidar 检测到变化（等待200ms确保写入完成）
   ↓
3. 防抖处理（300ms延迟）
   ↓
4. 查找包含该代码文件的所有Markdown文件
   ↓
5. 使用 server.watch() 通知Vite文件变化
   ↓
6. Vite触发HMR更新
   ↓
7. Astro重新构建相关页面
   ↓
8. Remark插件重新执行
   ↓
9. 读取最新代码文件
   ↓
10. 页面自动更新 ✅
```

## 📋 使用说明

### 1. 重启开发服务器

```bash
cd extension/AShare-manual
npm run dev
```

### 2. 观察控制台

应该看到：
```
[watch-code-library] ✅ 开始监控: /path/to/code_library
```

### 3. 修改代码文件

```bash
cd /home/taotao/dev/QuantTest/TRQuant
echo "" >> code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
```

### 4. 检查控制台日志

应该看到：
```
[watch-code-library] 📝 检测到代码文件变化: 003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
[watch-code-library] 找到 1 个相关Markdown文件
[watch-code-library] ✅ 已触发HMR更新: src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.2_Market_Status_CN.md
```

### 5. 检查浏览器

- 页面应该自动刷新
- 代码内容应该已更新

## 🔧 技术细节

### server.watch() API

这是Vite开发服务器提供的API，用于通知服务器文件已变化：

```javascript
server.watch(filePath);
```

### 降级方案

如果 `server.watch()` 不可用，使用文件时间戳方式：

```javascript
const timestamp = `<!-- Code updated: ${new Date().toISOString()} -->`;
const updatedContent = content.replace(/<!-- Code updated: .+? -->/, timestamp) 
  || content.trimEnd() + '\n' + timestamp + '\n';
await writeFile(fullPath, updatedContent, 'utf-8');
```

## 🎉 优势

- ✅ 更直接：使用HMR API，不依赖文件时间戳
- ✅ 更可靠：Vite直接处理文件变化
- ✅ 更快速：减少不必要的文件写入
- ✅ 有降级：如果API不可用，回退到时间戳方式

## 🐛 故障排查

### 问题：没有看到HMR更新日志

1. **检查 server.watch() 是否可用**
   - 查看控制台是否有警告
   - 如果不可用，会使用降级方案

2. **检查路径匹配**
   - 确保Markdown文件中的 `filePath` 属性正确
   - 查看控制台是否有"未找到包含代码文件的Markdown"警告

3. **检查文件监控**
   - 确保看到"检测到代码文件变化"日志
   - 如果没有，检查代码库路径是否正确

---

**更新时间**: 2025-12-13  
**版本**: v3.0 - 使用HMR API  
**状态**: ✅ 已实现

