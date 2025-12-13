/**
 * Vite插件：监控代码库目录，触发HMR更新（最终版）
 * 
 * 核心改进：
 * 1. 使用chokidar的awaitWriteFinish确保文件保存完成
 * 2. 监听多个事件：change, add, unlink
 * 3. 添加文件内容验证确保文件真正保存
 * 4. 详细的调试日志
 * 5. 多重验证机制
 */

import chokidar from 'chokidar';
import { join, relative, basename } from 'path';
import { readFile, writeFile, stat } from 'fs/promises';
import { existsSync } from 'fs';

// 防抖定时器
let updateTimer = null;
const DEBOUNCE_DELAY = 500; // 增加到500ms，确保文件完全保存

// 全局状态
let watcher = null;
let projectRoot = null;
let viteServer = null;

// 文件状态跟踪（用于检测文件是否真正改变）
const fileStats = new Map();

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
 * 验证文件是否真正改变（通过文件大小和修改时间）
 */
async function verifyFileChanged(filePath) {
  try {
    const currentStat = await stat(filePath);
    const previousStat = fileStats.get(filePath);
    
    // 如果文件不存在于跟踪中，或者大小/修改时间改变，说明文件真正改变了
    if (!previousStat || 
        previousStat.size !== currentStat.size || 
        previousStat.mtime.getTime() !== currentStat.mtime.getTime()) {
      fileStats.set(filePath, {
        size: currentStat.size,
        mtime: currentStat.mtime
      });
      return true;
    }
    
    return false;
  } catch (error) {
    // 如果无法获取文件状态，假设文件已改变
    return true;
  }
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
    // 验证文件是否真正改变
    const fileChanged = await verifyFileChanged(codeFilePath);
    if (!fileChanged) {
      console.log(`[vite-code-library-watcher] ⚠️ 文件未真正改变，跳过更新: ${relative(join(projectRoot, 'code_library'), codeFilePath)}`);
      return;
    }
    
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
            
            // 等待一小段时间确保文件写入完成
            await new Promise(resolve => setTimeout(resolve, 50));
            
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

/**
 * 处理文件变化事件
 */
async function handleFileChange(filePath, eventType) {
  try {
    if (filePath.endsWith('.py')) {
      const relativePath = relative(join(projectRoot, 'code_library'), filePath);
      console.log(`[vite-code-library-watcher] 📝 检测到代码文件${eventType}: ${relativePath}`);
      
      // 等待一小段时间确保文件写入完成（即使使用了awaitWriteFinish）
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // 验证文件是否存在且可读
      if (!existsSync(filePath)) {
        console.log(`[vite-code-library-watcher] ⚠️ 文件不存在，跳过: ${relativePath}`);
        return;
      }
      
      // 尝试读取文件，确保文件可访问
      try {
        await readFile(filePath, 'utf-8');
      } catch (error) {
        console.warn(`[vite-code-library-watcher] ⚠️ 文件无法读取，可能仍在写入: ${relativePath}`);
        // 等待更长时间后重试
        setTimeout(() => {
          if (existsSync(filePath)) {
            debouncedUpdate(filePath);
          }
        }, 300);
        return;
      }
      
      // 使用防抖处理
      debouncedUpdate(filePath);
    }
  } catch (error) {
    console.error(`[vite-code-library-watcher] ❌ 处理文件${eventType}时出错:`, error);
  }
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
      // 关键配置：
      // 1. awaitWriteFinish: 等待文件写入完成
      // 2. stabilityThreshold: 文件稳定时间（文件大小不变的时间）
      // 3. pollInterval: 轮询间隔
      watcher = chokidar.watch(codeLibraryPath, {
        ignored: /(^|[\/\\])\../, // 忽略隐藏文件
        persistent: true,
        ignoreInitial: true, // 忽略初始扫描
        // 关键：等待文件写入完成
        awaitWriteFinish: {
          stabilityThreshold: 500, // 文件大小稳定500ms才触发（确保文件保存完成）
          pollInterval: 100 // 每100ms检查一次文件大小
        },
        // 使用轮询模式（更可靠，但可能稍慢）
        usePolling: false, // 默认使用原生事件，如果不可靠可以改为true
        // 深度监控子目录
        depth: 10
      });
      
      // 监听文件变化事件（文件修改）
      watcher.on('change', async (filePath) => {
        await handleFileChange(filePath, '变化');
      });
      
      // 监听文件添加事件（新文件）
      watcher.on('add', async (filePath) => {
        await handleFileChange(filePath, '添加');
      });
      
      // 监听文件删除事件（可选，用于清理）
      watcher.on('unlink', (filePath) => {
        if (filePath.endsWith('.py')) {
          const relativePath = relative(codeLibraryPath, filePath);
          console.log(`[vite-code-library-watcher] 🗑️ 检测到代码文件删除: ${relativePath}`);
          fileStats.delete(filePath);
        }
      });
      
      watcher.on('error', (error) => {
        console.error(`[vite-code-library-watcher] ❌ 监控错误:`, error);
      });
      
      watcher.on('ready', () => {
        console.log(`[vite-code-library-watcher] ✅ 文件监控已就绪`);
        console.log(`[vite-code-library-watcher] 📊 监控配置: awaitWriteFinish={stabilityThreshold: 500ms, pollInterval: 100ms}`);
      });
      
      // 清理函数
      server.httpServer?.once('close', () => {
        if (watcher) {
          watcher.close();
        }
        if (updateTimer) {
          clearTimeout(updateTimer);
        }
        fileStats.clear();
        console.log(`[vite-code-library-watcher] 🔒 已停止监控`);
      });
    }
  };
}

