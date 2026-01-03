# 代码嵌入自动更新问题排查

## 🐛 问题：网页打不开

### 症状
- 开发服务器启动后，浏览器无法访问页面
- 或页面加载失败

### 可能原因

1. **集成代码错误**
   - `watch-code-library.mjs` 集成在启动时抛出错误
   - 导致整个服务器无法启动

2. **依赖缺失**
   - `chokidar` 或 `glob` 未正确安装

3. **路径问题**
   - 项目根目录检测失败
   - 代码库路径不正确

### ✅ 解决方案

#### 1. 添加错误处理

在集成代码中添加 try-catch，确保错误不会阻止服务器启动：

```javascript
'astro:server:setup': async ({ server, logger }) => {
  try {
    // ... 监控代码
  } catch (error) {
    logger.error(`[watch-code-library] 初始化失败:`, error);
    // 不抛出错误，避免阻止服务器启动
  }
}
```

#### 2. 暂时禁用集成

如果问题持续，可以暂时禁用集成：

```javascript
// astro.config.mjs
integrations: [mdx()], // watchCodeLibrary() 暂时禁用
```

#### 3. 检查依赖

```bash
cd extension/AShare-manual
npm list chokidar glob
```

如果缺失，安装：
```bash
npm install --save-dev chokidar glob
```

#### 4. 验证集成代码

```bash
cd extension/AShare-manual
node -e "import('./src/integrations/watch-code-library.mjs').then(() => console.log('✅ 正常')).catch(e => console.error('❌ 错误:', e))"
```

### 🔧 修复后的代码

已更新 `watch-code-library.mjs`：
- ✅ 添加了完整的错误处理
- ✅ 确保错误不会阻止服务器启动
- ✅ 添加了详细的日志输出

### 📋 验证步骤

1. **重启开发服务器**
   ```bash
   cd extension/AShare-manual
   pkill -f "astro dev"
   npm run dev
   ```

2. **检查控制台输出**
   - 应该看到 `[watch-code-library] 开始监控` 日志
   - 不应该有错误信息

3. **访问页面**
   ```bash
   curl http://localhost:4321
   ```

4. **测试自动更新**
   - 修改代码文件
   - 观察控制台是否显示监控日志
   - 检查页面是否自动更新

### 🎯 最佳实践

1. **错误处理**：所有异步操作都应该有错误处理
2. **日志输出**：使用 logger 输出详细信息，便于调试
3. **优雅降级**：集成失败不应该阻止服务器启动
4. **测试验证**：每次修改后都要验证服务器能正常启动

---

**修复时间**: 2025-12-13  
**状态**: ✅ 已修复

