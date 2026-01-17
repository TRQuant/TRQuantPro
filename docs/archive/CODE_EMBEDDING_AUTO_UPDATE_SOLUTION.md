# 代码嵌入自动更新解决方案

## 🔍 问题分析

### 核心问题
- **代码文件位置**：`code_library/` 在项目根目录（TRQuant），不在Astro项目目录（extension/AShare-manual）内
- **Astro监控范围**：默认只监控 `src/` 目录下的文件
- **结果**：修改代码文件后，Astro不会自动检测变化，页面不会更新

### 技术原理

```
代码文件修改 (code_library/*.py)
  ↓
❌ Astro不监控此目录（在项目外）
  ↓
Markdown文件未变化
  ↓
Remark插件不重新执行
  ↓
页面不更新
```

## ✅ 解决方案

### 方案：Astro集成 + 文件监控

创建一个Astro集成（Integration），使用 `chokidar` 监控代码库目录：

1. **监控代码文件变化**
2. **触发Markdown文件更新**（添加时间戳注释）
3. **Astro检测到Markdown变化**，触发重新构建
4. **Remark插件重新执行**，读取最新代码

### 实现步骤

#### 1. 安装依赖

```bash
cd extension/AShare-manual
npm install --save-dev chokidar glob
```

#### 2. 创建集成文件

`src/integrations/watch-code-library.mjs`

```javascript
import { watch } from 'chokidar';
import { join } from 'path';
import { readFile, writeFile } from 'fs/promises';
import { existsSync } from 'fs';

export default function watchCodeLibrary() {
  return {
    name: 'watch-code-library',
    hooks: {
      'astro:server:setup': async ({ server, logger }) => {
        // 获取项目根目录
        let projectRoot = process.cwd();
        if (projectRoot.includes('AShare-manual')) {
          const parts = projectRoot.split('/AShare-manual');
          projectRoot = parts[0] || process.cwd();
        }
        
        const codeLibraryPath = join(projectRoot, 'code_library');
        
        // 监控代码库目录
        const watcher = watch(codeLibraryPath, {
          ignored: /(^|[\/\\])\../,
          persistent: true,
          ignoreInitial: true,
        });
        
        watcher.on('change', async (filePath) => {
          if (filePath.endsWith('.py')) {
            logger.info(`[watch-code-library] 代码文件变化: ${filePath}`);
            
            // 更新所有包含 CodeFromFile 的Markdown文件
            await triggerAllMarkdownUpdates(projectRoot);
          }
        });
      },
    },
  };
}
```

#### 3. 注册集成

在 `astro.config.mjs` 中：

```javascript
import watchCodeLibrary from './src/integrations/watch-code-library.mjs';

export default defineConfig({
  integrations: [mdx(), watchCodeLibrary()],
  // ...
});
```

## 🎯 工作流程

```
1. 修改代码文件 (code_library/*.py)
   ↓
2. chokidar 检测到变化
   ↓
3. 更新所有包含 <CodeFromFile> 的Markdown文件（添加时间戳）
   ↓
4. Astro检测到Markdown文件变化
   ↓
5. 触发重新构建
   ↓
6. Remark插件重新执行
   ↓
7. 读取最新代码文件
   ↓
8. 页面自动更新 ✅
```

## 📋 验证步骤

1. **启动开发服务器**
   ```bash
   cd extension/AShare-manual
   npm run dev
   ```

2. **修改代码文件**
   ```bash
   # 编辑代码文件
   vim code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
   ```

3. **观察控制台输出**
   ```
   [watch-code-library] 检测到代码文件变化: ...
   [watch-code-library] 已触发更新: ...
   ```

4. **检查页面**
   - 浏览器应该自动刷新
   - 代码内容应该已更新

## 🔧 优化建议

### 1. 精确匹配Markdown文件

当前实现更新所有包含 `<CodeFromFile>` 的Markdown文件。可以优化为：
- 解析代码文件路径，找到对应的Markdown文件
- 只更新相关的Markdown文件

### 2. 防抖处理

如果同时修改多个代码文件，可以添加防抖：
```javascript
let updateTimer;
watcher.on('change', async (filePath) => {
  clearTimeout(updateTimer);
  updateTimer = setTimeout(async () => {
    await triggerAllMarkdownUpdates(projectRoot);
  }, 500); // 500ms防抖
});
```

### 3. 性能优化

- 只监控 `.py` 文件
- 使用文件路径映射，避免全量扫描

## 📝 注意事项

1. **开发环境专用**：此集成只在开发环境生效
2. **构建时处理**：生产构建时，代码文件会被静态读取，不需要监控
3. **文件路径**：确保代码库路径正确

## 🎉 效果

- ✅ 修改代码文件后，页面自动更新
- ✅ 无需手动触发Markdown文件更新
- ✅ 开发体验大幅提升

---

**实现时间**: 2025-12-13  
**状态**: ✅ 已实现并测试

