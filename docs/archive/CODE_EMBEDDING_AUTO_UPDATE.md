# 代码嵌入自动更新机制

## 🔍 问题分析

### 当前情况
- ✅ 代码文件已修改
- ⚠️ 页面未自动更新

### 原因分析

Astro开发服务器的文件监控机制：
1. **默认监控范围**：只监控 `src/` 目录下的文件
2. **代码文件位置**：`code_library/` 在项目根目录，不在 `src/` 下
3. **Remark插件执行时机**：在Markdown文件处理时执行，不是实时监控

### 工作流程

```
代码文件修改 (code_library/*.py)
  ↓
❌ Astro不监控此目录
  ↓
Markdown文件未变化
  ↓
Remark插件不重新执行
  ↓
页面不更新
```

## ✅ 解决方案

### 方案1：配置Vite监控代码库目录（推荐）

在 `astro.config.mjs` 中配置Vite监控外部文件：

```javascript
export default defineConfig({
  vite: {
    server: {
      watch: {
        // 监控代码库目录
        ignored: ['**/node_modules/**', '**/.git/**'],
        // 不忽略 code_library
      },
      // 或者使用 fs.watch 监控外部目录
    }
  }
});
```

### 方案2：修改Markdown文件触发更新

当代码文件修改后，可以：
1. 修改对应的Markdown文件（添加/删除空格）
2. 触发Astro重新构建
3. Remark插件重新执行，读取最新代码

### 方案3：使用文件系统事件（高级）

创建一个开发工具，监控 `code_library/` 目录：
- 检测文件变化
- 自动触发Markdown文件更新
- 或直接调用Astro的重新构建API

## 🔧 实现方案1：配置Vite监控

### 步骤1：更新 astro.config.mjs

```javascript
export default defineConfig({
  vite: {
    server: {
      watch: {
        ignored: ['**/node_modules/**', '**/.git/**', '**/*.mmd'],
        // 监控项目根目录的 code_library
        // 注意：需要相对路径或绝对路径
      },
      // 使用 fs.watch 监控外部目录
      fs: {
        strict: false,  // 允许访问项目外的文件
      }
    }
  }
});
```

### 步骤2：创建文件监控脚本（可选）

```javascript
// scripts/watch-code-library.mjs
import { watch } from 'fs';
import { join } from 'path';

const codeLibraryPath = join(process.cwd(), '..', '..', 'code_library');

watch(codeLibraryPath, { recursive: true }, (eventType, filename) => {
  if (filename && filename.endsWith('.py')) {
    console.log(`代码文件变化: ${filename}`);
    // 触发Astro重新构建
    // 或修改对应的Markdown文件
  }
});
```

## 📋 当前验证结果

### 测试步骤
1. ✅ 修改代码文件：添加 `test_field` 字段
2. ⚠️ 页面未自动更新（需要手动触发）

### 原因
- Astro开发服务器不监控 `code_library/` 目录
- 需要配置Vite监控或手动触发更新

## 🎯 推荐方案

### 短期方案（立即可用）
修改代码后，手动触发更新：
1. 修改对应的Markdown文件（添加空格）
2. 或重启开发服务器

### 长期方案（最佳实践）
配置Vite监控代码库目录，实现真正的自动更新。

## 📝 注意事项

1. **构建时 vs 运行时**
   - Remark插件在构建时执行
   - 需要触发重新构建才能看到更新

2. **文件监控范围**
   - 默认只监控 `src/` 目录
   - 外部目录需要额外配置

3. **性能考虑**
   - 监控大量文件可能影响性能
   - 建议只监控必要的目录

