/**
 * Vite插件：监控代码库目录，触发HMR更新（工作版）
 * 
 * 核心改进：
 * 1. 使用Vite的server.watcher.add()直接让Vite监控外部文件
 * 2. 修复路径计算问题
 * 3. 使用handleHotUpdate处理Vite检测到的文件变化
 * 4. 确保文件保存完成才触发
 */

import { join, relative, basename, resolve } from 'path';
import { readFile, writeFile, stat } from 'fs/promises';
import { existsSync } from 'fs';

// 防抖定时器
let updateTimer = null;
const DEBOUNCE_DELAY = 500;

// 全局状态
let projectRoot = null;
let viteServer = null;

// 文件状态跟踪
const fileStats = new Map();

/**
 * 获取项目根目录（TRQuant）
 * 代码库路径：/home/taotao/dev/QuantTest/TRQuant/code_library
 */
function getProjectRoot() {
  // 直接使用已知路径（最可靠）
  const KNOWN_CODE_LIBRARY = '/home/taotao/dev/QuantTest/TRQuant/code_library';
  const KNOWN_PROJECT_ROOT = '/home/taotao/dev/QuantTest/TRQuant';
  
  // 首先检查已知路径是否存在
  if (existsSync(KNOWN_CODE_LIBRARY)) {
    console.log(`[vite-code-library-watcher] ✅ 使用已知路径: ${KNOWN_PROJECT_ROOT}`);
    return KNOWN_PROJECT_ROOT;
  }
  
  // 如果已知路径不存在，尝试从当前目录计算（备用方案）
  let root = process.cwd();
  
  // 方法1：查找 TRQuant 目录
  const trquantIndex = root.indexOf('/TRQuant/');
  if (trquantIndex !== -1) {
    root = root.substring(0, trquantIndex + '/TRQuant'.length);
  }
  // 方法2：如果路径以 TRQuant 结尾（在根目录）
  else if (root.endsWith('TRQuant')) {
    root = root;
  }
  // 方法3：如果包含 AShare-manual，向上查找
  else if (root.includes('AShare-manual')) {
    const parts = root.split('/AShare-manual');
    if (parts[0].endsWith('/extension')) {
      root = parts[0].split('/extension')[0];
    } else {
      root = parts[0];
    }
  }
  // 方法4：如果包含 extension，向上查找
  else if (root.includes('/extension')) {
    const parts = root.split('/extension');
    root = parts[0];
  }
  
  root = resolve(root);
  
  // 验证：检查code_library是否存在
  const codeLibraryPath = join(root, 'code_library');
  if (!existsSync(codeLibraryPath)) {
    console.error(`[vite-code-library-watcher] ❌ 路径计算错误:`);
    console.error(`  当前目录: ${process.cwd()}`);
    console.error(`  计算根目录: ${root}`);
    console.error(`  代码库路径: ${codeLibraryPath}`);
    console.error(`  已知路径: ${KNOWN_CODE_LIBRARY}`);
    throw new Error(`无法找到代码库目录。请检查路径配置。`);
  }
  
  return root;
}

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
 * 验证文件是否真正改变
 */
async function verifyFileChanged(filePath) {
  try {
    const currentStat = await stat(filePath);
    const previousStat = fileStats.get(filePath);
    
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
          relatedFiles.push({
            relative: relativePath.replace(/\\/g, '/'),
            absolute: file
          });
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
      const relativePath = getCodeFileRelativePath(codeFilePath, projectRoot);
      console.log(`[vite-code-library-watcher] ⚠️ 文件未真正改变，跳过更新: ${relativePath}`);
      return;
    }
    
    const markdownFiles = await findRelatedMarkdownFiles(codeFilePath);
    
    if (markdownFiles.length === 0) {
      const relativePath = getCodeFileRelativePath(codeFilePath, projectRoot);
      console.warn(`[vite-code-library-watcher] ⚠️ 未找到包含代码文件的Markdown: ${relativePath}`);
      return;
    }
    
    console.log(`[vite-code-library-watcher] ✅ 找到 ${markdownFiles.length} 个相关Markdown文件`);
    
    // 触发HMR更新 - 更新Markdown文件时间戳并通知Vite
    for (const { relative: fileRelative, absolute: fileAbsolute } of markdownFiles) {
      try {
        if (existsSync(fileAbsolute)) {
          // 读取文件内容
          const content = await readFile(fileAbsolute, 'utf-8');
          
          // 更新时间戳注释
          const timestamp = `<!-- Code updated: ${new Date().toISOString()} -->`;
          const timestampPattern = /<!-- Code updated: .+? -->/;
          let updatedContent;
          
          if (timestampPattern.test(content)) {
            updatedContent = content.replace(timestampPattern, timestamp);
          } else {
            updatedContent = content.trimEnd() + '\n' + timestamp + '\n';
          }
          
          // 只有当内容改变时才写入
          if (updatedContent !== content) {
            await writeFile(fileAbsolute, updatedContent, 'utf-8');
            console.log(`[vite-code-library-watcher] ✅ 已更新文件时间戳: ${fileRelative}`);
            
            // 等待文件写入完成
            await new Promise(resolve => setTimeout(resolve, 50));
            
            // 方法1: 使用Vite的watcher.emit触发文件变化事件
            if (viteServer.watcher && typeof viteServer.watcher.emit === 'function') {
              viteServer.watcher.emit('change', fileAbsolute);
              console.log(`[vite-code-library-watcher] ✅ 已触发文件变化事件: ${fileRelative}`);
            }
            
            // 方法2: 使用Vite的模块图失效机制
            try {
              const module = viteServer.moduleGraph.getModuleById(fileAbsolute);
              if (module) {
                viteServer.moduleGraph.invalidateModule(module);
                console.log(`[vite-code-library-watcher] ✅ 已失效模块: ${fileRelative}`);
              }
            } catch (error) {
              // 忽略，文件时间戳更新已经足够
            }
          }
        }
      } catch (error) {
        console.error(`[vite-code-library-watcher] ❌ 更新文件失败: ${fileRelative}`, error.message);
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
      projectRoot = getProjectRoot();
      const codeLibraryPath = join(projectRoot, 'code_library');
      
      console.log(`[vite-code-library-watcher] 📂 当前工作目录: ${process.cwd()}`);
      console.log(`[vite-code-library-watcher] 📂 项目根目录: ${projectRoot}`);
      console.log(`[vite-code-library-watcher] 📂 代码库路径: ${codeLibraryPath}`);
      
      if (!existsSync(codeLibraryPath)) {
        console.warn(`[vite-code-library-watcher] ⚠️ 代码库目录不存在: ${codeLibraryPath}`);
        return;
      }
      
      console.log(`[vite-code-library-watcher] ✅ 开始监控: ${codeLibraryPath}`);
      
      // 关键：使用Vite的watcher.add()方法直接让Vite监控外部目录
      // 这是最可靠的方法，因为Vite会直接处理文件变化
      try {
        if (server.watcher && typeof server.watcher.add === 'function') {
          // 添加代码库目录到Vite的监控列表
          server.watcher.add(codeLibraryPath);
          console.log(`[vite-code-library-watcher] ✅ 已添加到Vite监控: ${codeLibraryPath}`);
        } else {
          console.warn(`[vite-code-library-watcher] ⚠️ server.watcher.add() 不可用`);
        }
      } catch (error) {
        console.error(`[vite-code-library-watcher] ❌ 添加到Vite监控失败:`, error);
      }
      
      // 监听Vite的watcher事件（当Vite检测到文件变化时）
      if (server.watcher) {
        server.watcher.on('change', async (filePath) => {
          // 只处理代码库目录下的Python文件
          if (filePath.includes('code_library') && filePath.endsWith('.py')) {
            const relativePath = relative(codeLibraryPath, filePath);
            console.log(`[vite-code-library-watcher] 📝 Vite检测到代码文件变化: ${relativePath}`);
            
            // 等待文件保存完成（额外保险）
            await new Promise(resolve => setTimeout(resolve, 200));
            
            // 使用防抖处理
            debouncedUpdate(filePath);
          }
        });
        
        server.watcher.on('add', async (filePath) => {
          if (filePath.includes('code_library') && filePath.endsWith('.py')) {
            const relativePath = relative(codeLibraryPath, filePath);
            console.log(`[vite-code-library-watcher] 📝 Vite检测到代码文件添加: ${relativePath}`);
            
            await new Promise(resolve => setTimeout(resolve, 200));
            debouncedUpdate(filePath);
          }
        });
      }
      
      // 清理函数
      server.httpServer?.once('close', () => {
        if (updateTimer) {
          clearTimeout(updateTimer);
        }
        fileStats.clear();
        console.log(`[vite-code-library-watcher] 🔒 已停止监控`);
      });
    },
    
    // 处理HMR更新 - 当Vite检测到文件变化时
    handleHotUpdate({ file, server }) {
      // 如果代码文件变化，触发相关Markdown文件的更新
      if (file.includes('code_library') && file.endsWith('.py')) {
        console.log(`[vite-code-library-watcher] 🔥 handleHotUpdate: ${file}`);
        debouncedUpdate(file);
        // 返回null表示不阻止其他插件处理
        return null;
      }
    }
  };
}

