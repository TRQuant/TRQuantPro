/**
 * Vite插件：监控代码库目录，触发HMR更新（修复版）
 * 
 * 关键修复：
 * 1. 确保插件正确加载
 * 2. 使用更可靠的HMR触发方式
 * 3. 添加详细的调试日志
 */

import chokidar from 'chokidar';
import { join, relative, basename } from 'path';
import { readFile, writeFile } from 'fs/promises';
import { existsSync } from 'fs';

// 防抖定时器
let updateTimer = null;
const DEBOUNCE_DELAY = 300;

// 全局状态
let watcher = null;
let projectRoot = null;
let viteServer = null;

/**
 * 从代码文件路径提取相对路径
 */
function getCodeFileRelativePath(filePath, root) {
  const codeLibraryPath = join(root, 'code_library');
  const relativePath = relative(codeLibraryPath, filePath);
  return relativePath.replace(/\\/g, '/');
}

/**
 * 检查Markdown文件是否包含指定的代码文件
 */
function markdownContainsCodeFile(markdownContent, codeFileRelativePath) {
  const escapedPath = codeFileRelativePath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const escapedFullPath = `code_library/${escapedPath}`;
  const escapedFileName = basename(codeFileRelativePath).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  
  const patterns = [
    new RegExp(`<CodeFromFile[^>]*filePath=["']${escapedFullPath}["']`, 'i'),
    new RegExp(`<CodeFromFile[^>]*filePath=["']${escapedPath}["']`, 'i'),
    new RegExp(`<CodeFromFile[^>]*filePath=["'][^"']*${escapedFileName}["']`, 'i'),
  ];
  
  return patterns.some(pattern => pattern.test(markdownContent));
}

/**
 * 查找包含指定代码文件的所有Markdown文件
 */
async function findRelatedMarkdownFiles(codeFilePath) {
  try {
    const { glob } = await import('glob');
    const codeFileRelativePath = getCodeFileRelativePath(codeFilePath, projectRoot);
    
    console.log(`[vite-code-library-watcher] 🔍 查找包含代码文件的Markdown: ${codeFileRelativePath}`);
    
    const markdownFiles = await glob('src/pages/**/*.md', {
      cwd: join(projectRoot, 'extension/AShare-manual'),
      absolute: true
    });
    
    const relatedFiles = [];
    
    for (const file of markdownFiles) {
      try {
        const content = await readFile(file, 'utf-8');
        if (markdownContainsCodeFile(content, codeFileRelativePath)) {
          const relativePath = relative(join(projectRoot, 'extension/AShare-manual'), file);
          relatedFiles.push(relativePath.replace(/\\/g, '/'));
          console.log(`[vite-code-library-watcher] 📄 找到相关文件: ${relativePath}`);
        }
      } catch (error) {
        // 忽略读取错误
      }
    }
    
    return relatedFiles;
  } catch (error) {
    console.error(`[vite-code-library-watcher] ❌ 查找Markdown文件失败:`, error);
    return [];
  }
}

/**
 * 触发HMR更新 - 使用最可靠的方式
 */
async function triggerHMRUpdate(codeFilePath) {
  if (!viteServer) {
    console.warn(`[vite-code-library-watcher] ⚠️ Vite服务器未初始化`);
    return;
  }
  
  try {
    const markdownFiles = await findRelatedMarkdownFiles(codeFilePath);
    
    if (markdownFiles.length === 0) {
      const relativePath = getCodeFileRelativePath(codeFilePath, projectRoot);
      console.warn(`[vite-code-library-watcher] ⚠️ 未找到包含代码文件的Markdown: ${relativePath}`);
      return;
    }
    
    console.log(`[vite-code-library-watcher] ✅ 找到 ${markdownFiles.length} 个相关Markdown文件`);
    
    // 触发HMR更新 - 使用最可靠的方式：修改文件时间戳
    for (const file of markdownFiles) {
      try {
        const fullPath = join(projectRoot, 'extension/AShare-manual', file);
        if (existsSync(fullPath)) {
          // 读取文件内容
          const content = await readFile(fullPath, 'utf-8');
          
          // 更新时间戳注释
          const timestamp = `<!-- Code updated: ${new Date().toISOString()} -->`;
          const timestampPattern = /<!-- Code updated: .+? -->/;
          let updatedContent;
          
          if (timestampPattern.test(content)) {
            updatedContent = content.replace(timestampPattern, timestamp);
          } else {
            // 在文件末尾添加时间戳
            updatedContent = content.trimEnd() + '\n' + timestamp + '\n';
          }
          
          // 只有当内容改变时才写入
          if (updatedContent !== content) {
            await writeFile(fullPath, updatedContent, 'utf-8');
            console.log(`[vite-code-library-watcher] ✅ 已更新文件时间戳: ${file}`);
            
            // 尝试触发Vite文件变化事件
            try {
              if (viteServer.watcher && typeof viteServer.watcher.emit === 'function') {
                viteServer.watcher.emit('change', fullPath);
                console.log(`[vite-code-library-watcher] ✅ 已触发文件变化事件: ${file}`);
              }
            } catch (error) {
              // 忽略，文件时间戳更新已经足够
              console.log(`[vite-code-library-watcher] ⚠️ 无法触发文件变化事件，但文件已更新: ${file}`);
            }
          } else {
            console.log(`[vite-code-library-watcher] ⚠️ 文件内容未改变: ${file}`);
          }
        }
      } catch (error) {
        console.error(`[vite-code-library-watcher] ❌ 更新文件失败: ${file}`, error.message);
      }
    }
  } catch (error) {
    console.error(`[vite-code-library-watcher] ❌ 触发HMR更新时出错:`, error);
  }
}

/**
 * 防抖处理
 */
function debouncedUpdate(codeFilePath) {
  if (updateTimer) {
    clearTimeout(updateTimer);
  }
  
  updateTimer = setTimeout(async () => {
    try {
      await triggerHMRUpdate(codeFilePath);
    } catch (error) {
      console.error(`[vite-code-library-watcher] ❌ 防抖更新失败:`, error);
    } finally {
      updateTimer = null;
    }
  }, DEBOUNCE_DELAY);
}

export default function viteCodeLibraryWatcher() {
  return {
    name: 'vite-code-library-watcher',
    enforce: 'pre',
    
    // 配置服务器
    configureServer(server) {
      console.log(`[vite-code-library-watcher] 🚀 插件开始初始化...`);
      
      viteServer = server;
      
      // 获取项目根目录
      projectRoot = process.cwd();
      if (projectRoot.includes('AShare-manual')) {
        const parts = projectRoot.split('/AShare-manual');
        projectRoot = parts[0] || process.cwd();
      } else if (projectRoot.includes('extension')) {
        const parts = projectRoot.split('/extension');
        projectRoot = parts[0] || process.cwd();
      }
      
      const codeLibraryPath = join(projectRoot, 'code_library');
      
      console.log(`[vite-code-library-watcher] 📂 项目根目录: ${projectRoot}`);
      console.log(`[vite-code-library-watcher] 📂 代码库路径: ${codeLibraryPath}`);
      
      if (!existsSync(codeLibraryPath)) {
        console.warn(`[vite-code-library-watcher] ⚠️ 代码库目录不存在: ${codeLibraryPath}`);
        return;
      }
      
      console.log(`[vite-code-library-watcher] ✅ 开始监控: ${codeLibraryPath}`);
      
      // 使用 chokidar 监控代码库目录
      watcher = chokidar.watch(codeLibraryPath, {
        ignored: /(^|[\/\\])\../,
        persistent: true,
        ignoreInitial: true,
        awaitWriteFinish: {
          stabilityThreshold: 200,
          pollInterval: 100
        }
      });
      
      watcher.on('change', async (filePath) => {
        try {
          if (filePath.endsWith('.py')) {
            const relativePath = relative(codeLibraryPath, filePath);
            console.log(`[vite-code-library-watcher] 📝 检测到代码文件变化: ${relativePath}`);
            
            // 使用防抖处理
            debouncedUpdate(filePath);
          }
        } catch (error) {
          console.error(`[vite-code-library-watcher] ❌ 处理文件变化时出错:`, error);
        }
      });
      
      watcher.on('error', (error) => {
        console.error(`[vite-code-library-watcher] ❌ 监控错误:`, error);
      });
      
      watcher.on('ready', () => {
        console.log(`[vite-code-library-watcher] ✅ 文件监控已就绪`);
      });
      
      // 清理函数
      server.httpServer?.once('close', () => {
        if (watcher) {
          watcher.close();
        }
        if (updateTimer) {
          clearTimeout(updateTimer);
        }
        console.log(`[vite-code-library-watcher] 🔒 已停止监控`);
      });
    }
  };
}

