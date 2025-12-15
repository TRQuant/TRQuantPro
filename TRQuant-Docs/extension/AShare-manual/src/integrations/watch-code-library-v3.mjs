/**
 * Astro集成：监控代码库目录变化，触发页面自动更新（改进版）
 * 
 * 关键改进：
 * 1. 使用 server.watch() API 直接通知Vite监控外部文件
 * 2. 直接触发HMR更新，而不是修改Markdown文件
 * 3. 更可靠的路径匹配和错误处理
 */

import chokidar from 'chokidar';
import { join, relative, basename } from 'path';
import { readFile } from 'fs/promises';
import { existsSync } from 'fs';

// 防抖定时器
let updateTimer = null;
const DEBOUNCE_DELAY = 300; // 300ms防抖

/**
 * 从代码文件路径提取相对路径（用于匹配CodeFromFile标签）
 */
function getCodeFileRelativePath(filePath, projectRoot) {
  const codeLibraryPath = join(projectRoot, 'code_library');
  const relativePath = relative(codeLibraryPath, filePath);
  return relativePath.replace(/\\/g, '/'); // 统一使用正斜杠
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
async function findRelatedMarkdownFiles(codeFilePath, projectRoot) {
  try {
    const { glob } = await import('glob');
    const codeFileRelativePath = getCodeFileRelativePath(codeFilePath, projectRoot);
    
    // 查找所有Markdown文件
    const markdownFiles = await glob('src/pages/**/*.md', {
      cwd: join(projectRoot, 'extension/AShare-manual'),
      absolute: true
    });
    
    const relatedFiles = [];
    
    // 检查每个Markdown文件
    for (const file of markdownFiles) {
      try {
        const content = await readFile(file, 'utf-8');
        if (markdownContainsCodeFile(content, codeFileRelativePath)) {
          // 返回相对于Astro项目目录的路径
          const relativePath = relative(join(projectRoot, 'extension/AShare-manual'), file);
          relatedFiles.push(relativePath.replace(/\\/g, '/'));
        }
      } catch (error) {
        // 忽略单个文件的读取错误
      }
    }
    
    return relatedFiles;
  } catch (error) {
    console.error(`[watch-code-library] 查找Markdown文件失败:`, error);
    return [];
  }
}

/**
 * 触发HMR更新
 */
async function triggerHMRUpdate(codeFilePath, projectRoot, server, logger) {
  try {
    const markdownFiles = await findRelatedMarkdownFiles(codeFilePath, projectRoot);
    
    if (markdownFiles.length === 0) {
      logger.warn(`[watch-code-library] 未找到包含代码文件的Markdown: ${getCodeFileRelativePath(codeFilePath, projectRoot)}`);
      return;
    }
    
    logger.info(`[watch-code-library] 找到 ${markdownFiles.length} 个相关Markdown文件`);
    
    // 通知Vite服务器这些文件已更新
    for (const file of markdownFiles) {
      try {
        // 使用 server.watch() 通知Vite文件变化
        // 这会触发HMR更新
        const fullPath = join(projectRoot, 'extension/AShare-manual', file);
        if (existsSync(fullPath)) {
          // 触发文件变化事件
          server.watch(fullPath);
          logger.info(`[watch-code-library] ✅ 已触发HMR更新: ${file}`);
        }
      } catch (error) {
        logger.error(`[watch-code-library] 触发HMR更新失败: ${file}`, error);
      }
    }
    
    // 如果server.watch()不可用，尝试修改文件时间戳
    if (markdownFiles.length > 0 && !server.watch) {
      logger.warn(`[watch-code-library] server.watch() 不可用，使用文件时间戳方式`);
      const { writeFile } = await import('fs/promises');
      for (const file of markdownFiles) {
        try {
          const fullPath = join(projectRoot, 'extension/AShare-manual', file);
          const content = await readFile(fullPath, 'utf-8');
          const timestamp = `<!-- Code updated: ${new Date().toISOString()} -->`;
          const updatedContent = content.replace(/<!-- Code updated: .+? -->/, timestamp) || content.trimEnd() + '\n' + timestamp + '\n';
          if (updatedContent !== content) {
            await writeFile(fullPath, updatedContent, 'utf-8');
            logger.info(`[watch-code-library] ✅ 已更新文件时间戳: ${file}`);
          }
        } catch (error) {
          logger.error(`[watch-code-library] 更新文件时间戳失败: ${file}`, error);
        }
      }
    }
    
  } catch (error) {
    logger.error(`[watch-code-library] 触发HMR更新时出错:`, error);
  }
}

/**
 * 防抖处理：避免频繁更新
 */
function debouncedUpdate(codeFilePath, projectRoot, server, logger) {
  if (updateTimer) {
    clearTimeout(updateTimer);
  }
  
  updateTimer = setTimeout(async () => {
    try {
      await triggerHMRUpdate(codeFilePath, projectRoot, server, logger);
    } catch (error) {
      logger.error(`[watch-code-library] 防抖更新失败:`, error);
    } finally {
      updateTimer = null;
    }
  }, DEBOUNCE_DELAY);
}

export default function watchCodeLibrary() {
  return {
    name: 'watch-code-library',
    hooks: {
      'astro:server:setup': async ({ server, logger }) => {
        try {
          // 获取项目根目录（TRQuant）
          let projectRoot = process.cwd();
          if (projectRoot.includes('AShare-manual')) {
            const parts = projectRoot.split('/AShare-manual');
            projectRoot = parts[0] || process.cwd();
          } else if (projectRoot.includes('extension')) {
            const parts = projectRoot.split('/extension');
            projectRoot = parts[0] || process.cwd();
          }
          
          const codeLibraryPath = join(projectRoot, 'code_library');
          
          if (!existsSync(codeLibraryPath)) {
            logger.warn(`[watch-code-library] ⚠️ 代码库目录不存在: ${codeLibraryPath}`);
            return;
          }
          
          logger.info(`[watch-code-library] ✅ 开始监控: ${codeLibraryPath}`);
          
          // 使用 chokidar 监控代码库目录
          const watcher = chokidar.watch(codeLibraryPath, {
            ignored: /(^|[\/\\])\../, // 忽略隐藏文件
            persistent: true,
            ignoreInitial: true, // 忽略初始扫描
            awaitWriteFinish: {
              stabilityThreshold: 200, // 等待200ms确保文件写入完成
              pollInterval: 100
            }
          });
          
          watcher.on('change', async (filePath) => {
            try {
              if (filePath.endsWith('.py')) {
                const relativePath = relative(codeLibraryPath, filePath);
                logger.info(`[watch-code-library] 📝 检测到代码文件变化: ${relativePath}`);
                
                // 使用防抖处理，避免频繁更新
                debouncedUpdate(filePath, projectRoot, server, logger);
              }
            } catch (error) {
              logger.error(`[watch-code-library] ❌ 处理文件变化时出错:`, error);
            }
          });
          
          watcher.on('error', (error) => {
            logger.error(`[watch-code-library] ❌ 监控错误:`, error);
          });
          
          // 清理函数：服务器关闭时停止监控
          if (server.hot) {
            server.hot.on('shutdown', () => {
              watcher.close();
              if (updateTimer) {
                clearTimeout(updateTimer);
              }
              logger.info(`[watch-code-library] 🔒 已停止监控`);
            });
          }
          
        } catch (error) {
          logger.error(`[watch-code-library] ❌ 初始化失败:`, error);
          // 不抛出错误，避免阻止服务器启动
        }
      },
    },
  };
}

