# 代码嵌入自动更新 - 开发者工具检查指南

## 🔍 浏览器开发者工具检查

### Chrome DevTools

#### 1. Network标签

**检查HMR更新请求**：
1. 打开开发者工具（F12）
2. 切换到Network标签
3. 修改代码文件
4. 应该看到：
   - `__vite_ping` 请求（Vite心跳检测）
   - `*.md` 文件的HMR更新请求
   - 状态码应该是 `200` 或 `304`

**如果看不到HMR请求**：
- 检查控制台是否有错误
- 检查Vite插件是否正常加载
- 检查文件路径是否正确

#### 2. Console标签

**查看HMR日志**：
- 应该看到 `[vite-code-library-watcher]` 相关的日志
- 检查是否有错误信息

**常见错误**：
- `Module not found`: 文件路径不正确
- `HMR update failed`: HMR更新失败，会降级到文件时间戳方式

#### 3. Sources标签

**检查文件内容**：
1. 打开Sources标签
2. 找到对应的Markdown文件
3. 检查代码内容是否已更新
4. 检查时间戳注释是否正确

### Vite DevTools扩展

如果安装了Vite DevTools扩展：
1. 打开扩展面板
2. 查看HMR更新状态
3. 检查模块依赖关系
4. 查看构建时间

## 🔧 服务器端检查

### 控制台日志

**正常启动应该看到**：
```
[vite-code-library-watcher] ✅ 开始监控: /path/to/code_library
```

**修改代码文件应该看到**：
```
[vite-code-library-watcher] 📝 检测到代码文件变化: 003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
[vite-code-library-watcher] 找到 1 个相关Markdown文件
[vite-code-library-watcher] ✅ 已触发HMR更新: src/pages/ashare-book6/003_Chapter3_Market_Analysis/3.2_Market_Status_CN.md
```

### 错误排查

**如果看到警告**：
```
[vite-code-library-watcher] HMR API失败，使用文件时间戳方式
```
- 这是正常的降级机制
- 仍然会触发更新，只是方式不同

**如果看到错误**：
```
[vite-code-library-watcher] ❌ 处理文件变化时出错
```
- 检查代码库路径是否正确
- 检查文件权限
- 查看完整错误堆栈

## 📋 测试清单

### 基础测试

- [ ] 服务器正常启动
- [ ] 看到监控日志
- [ ] 修改代码文件后看到变化日志
- [ ] 浏览器自动刷新
- [ ] 代码内容已更新

### 高级测试

- [ ] Network标签看到HMR请求
- [ ] Console标签没有错误
- [ ] Sources标签文件内容正确
- [ ] 多次修改不会导致页面打不开
- [ ] 防抖机制正常工作（不会频繁更新）

## 🐛 常见问题

### 问题1：页面没有自动更新

**检查步骤**：
1. 打开浏览器开发者工具
2. 查看Console标签是否有错误
3. 查看Network标签是否有HMR请求
4. 检查服务器控制台日志

**解决方案**：
- 如果看到HMR失败警告，这是正常的降级机制
- 如果完全没有日志，检查插件是否加载
- 如果路径匹配失败，检查Markdown文件中的filePath属性

### 问题2：页面打不开

**这个问题应该已经解决**，因为：
- ✅ 使用Vite原生HMR API
- ✅ 不修改Markdown文件内容（除非降级）
- ✅ 完整的错误处理

**如果仍然出现问题**：
1. 检查控制台错误日志
2. 检查Vite插件代码
3. 暂时禁用插件测试

### 问题3：更新太频繁

**原因**：防抖机制可能没有正常工作

**解决方案**：
- 检查防抖延迟设置（默认300ms）
- 可以增加延迟时间
- 检查是否有多个监控实例

## 📝 调试技巧

### 1. 启用详细日志

在Vite插件中添加更多日志：
```javascript
console.log('[vite-code-library-watcher] 详细日志:', {
  codeFilePath,
  markdownFiles,
  fullPath
});
```

### 2. 检查模块图

在浏览器控制台：
```javascript
// 检查Vite模块图
console.log(__VITE_MODULE_GRAPH__);
```

### 3. 手动触发更新

在服务器控制台：
```javascript
// 手动触发HMR更新（如果插件暴露了API）
```

---

**更新时间**: 2025-12-13  
**状态**: ✅ 完整指南

