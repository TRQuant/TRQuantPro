/**
 * Astro集成：监控代码库目录变化，触发页面自动更新
 * 
 * 功能：
 * 1. 监控 code_library/ 目录的文件变化
 * 2. 当代码文件修改时，只更新包含该代码文件的Markdown文件
 * 3. 实现代码文件修改后页面自动刷新
 * 
 * 原理：
 * - 使用 chokidar 监控文件系统
 * - 检测到代码文件变化时，解析CodeFromFile标签，找到对应的Markdown文件
 * - 只更新相关的Markdown文件（添加时间戳注释）
 * - Astro检测到Markdown文件变化，触发重新构建
 * - Remark插件重新执行，读取最新的代码文件
 * 
 * 优化：
 * - 防抖处理：避免频繁更新
 * - 精确匹配：只更新相关的Markdown文件
 * - 安全更新：确保不会破坏文件内容
 */

import chokidar from 'chokidar';
import { join, relative, basename } from 'path';
import { readFile, writeFile } from 'fs/promises';
import { existsSync } from 'fs';

// 防抖定时器
let updateTimer = null;
const DEBOUNCE_DELAY = 500; // 500ms防抖

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
  // 匹配 <CodeFromFile filePath="..." />
  // 支持多种路径格式：
  // 1. 完整路径：code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
  // 2. 相对路径：003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py
  // 3. 文件名：code_3_2_2_analyze_price_dimension.py
  
  const escapedPath = codeFileRelativePath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const escapedFullPath = `code_library/${escapedPath}`;
  const escapedFileName = basename(codeFileRelativePath).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  
  const patterns = [
    // 完整路径匹配（包含 code_library/ 前缀）
    new RegExp(`<CodeFromFile[^>]*filePath=["']${escapedFullPath}["']`, 'i'),
    // 相对路径匹配（不包含 code_library/ 前缀）
    new RegExp(`<CodeFromFile[^>]*filePath=["']${escapedPath}["']`, 'i'),
    // 文件名匹配（更宽松，匹配任何包含该文件名的路径）
    new RegExp(`<CodeFromFile[^>]*filePath=["'][^"']*${escapedFileName}["']`, 'i'),
  ];
  
  return patterns.some(pattern => pattern.test(markdownContent));
}

/**
 * 安全地更新Markdown文件（添加时间戳注释）
 */
async function triggerMarkdownUpdate(markdownPath, logger) {
  try {
    if (!existsSync(markdownPath)) {
      return false;
    }
    
    const content = await readFile(markdownPath, 'utf-8');
    
    // 检查是否已经有时间戳注释
    const timestampPattern = /<!-- Code updated: .+? -->/;
    const timestamp = `<!-- Code updated: ${new Date().toISOString()} -->`;
    
    let updatedContent;
    if (timestampPattern.test(content)) {
      // 更新时间戳
      updatedContent = content.replace(timestampPattern, timestamp);
    } else {
      // 在文件末尾添加时间戳（不影响显示）
      updatedContent = content.trimEnd() + '\n' + timestamp + '\n';
    }
    
    // 只有当内容真正改变时才写入
    if (updatedContent !== content) {
      await writeFile(markdownPath, updatedContent, 'utf-8');
      logger.info(`[watch-code-library] 已更新: ${relative(process.cwd(), markdownPath)}`);
      return true;
    }
    
    return false;
  } catch (error) {
    logger.error(`[watch-code-library] 更新Markdown文件失败: ${markdownPath}`, error);
    return false;
  }
}

/**
 * 查找并更新包含指定代码文件的所有Markdown文件
 */
async function updateRelatedMarkdownFiles(codeFilePath, projectRoot, logger) {
  try {
    const { glob } = await import('glob');
    const codeFileRelativePath = getCodeFileRelativePath(codeFilePath, projectRoot);
    
    logger.info(`[watch-code-library] 查找包含代码文件的Markdown: ${codeFileRelativePath}`);
    
    // 查找所有Markdown文件
    const markdownFiles = await glob('src/pages/**/*.md', {
      cwd: join(projectRoot, 'extension/AShare-manual'),
      absolute: true
    });
    
    let updatedCount = 0;
    
    // 检查每个Markdown文件
    for (const file of markdownFiles) {
      try {
        const content = await readFile(file, 'utf-8');
        
        // 只更新包含该代码文件的Markdown文件
        if (markdownContainsCodeFile(content, codeFileRelativePath)) {
          const updated = await triggerMarkdownUpdate(file, logger);
          if (updated) {
            updatedCount++;
          }
        }
      } catch (error) {
        // 忽略单个文件的读取错误
        logger.warn(`[watch-code-library] 读取文件失败: ${file}`, error.message);
      }
    }
    
    if (updatedCount > 0) {
      logger.info(`[watch-code-library] 已更新 ${updatedCount} 个Markdown文件`);
    } else {
      logger.warn(`[watch-code-library] 未找到包含代码文件的Markdown: ${codeFileRelativePath}`);
    }
    
    return updatedCount;
  } catch (error) {
    logger.error(`[watch-code-library] 更新Markdown文件时出错:`, error);
    return 0;
  }
}

/**
 * 防抖处理：避免频繁更新
 */
function debouncedUpdate(codeFilePath, projectRoot, logger) {
  // 清除之前的定时器
  if (updateTimer) {
    clearTimeout(updateTimer);
  }
  
  // 设置新的定时器
  updateTimer = setTimeout(async () => {
    try {
      await updateRelatedMarkdownFiles(codeFilePath, projectRoot, logger);
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
            logger.warn(`[watch-code-library] 代码库目录不存在: ${codeLibraryPath}`);
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
                logger.info(`[watch-code-library] 📝 检测到代码文件变化: ${relative(codeLibraryPath, filePath)}`);
                
                // 使用防抖处理，避免频繁更新
                debouncedUpdate(filePath, projectRoot, logger);
              }
            } catch (error) {
              logger.error(`[watch-code-library] ❌ 处理文件变化时出错:`, error);
            }
          });
          
          watcher.on('error', (error) => {
            logger.error(`[watch-code-library] ❌ 监控错误:`, error);
          });
          
          // 清理函数：服务器关闭时停止监控
          server.hot.on('shutdown', () => {
            watcher.close();
            if (updateTimer) {
              clearTimeout(updateTimer);
            }
            logger.info(`[watch-code-library] 🔒 已停止监控`);
          });
          
        } catch (error) {
          logger.error(`[watch-code-library] ❌ 初始化失败:`, error);
          // 不抛出错误，避免阻止服务器启动
        }
      },
    },
  };
}
