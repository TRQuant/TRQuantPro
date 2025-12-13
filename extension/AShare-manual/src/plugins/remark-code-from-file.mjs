/**
 * Remark插件：从文件读取代码并嵌入到Markdown中
 * 
 * 功能：
 * 1. 识别Markdown中的 `<CodeFromFile>` 标签
 * 2. 读取指定的代码文件
 * 3. 提取设计原理说明
 * 4. 替换为格式化的代码块
 * 
 * 使用方式：
 * <CodeFromFile filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py" />
 */

import { readFile } from 'fs/promises';
import { join } from 'path';
import { visit } from 'unist-util-visit';
import { toString } from 'mdast-util-to-string';

/**
 * 提取设计原理说明
 */
function extractDesignPrinciples(content) {
  const designMatch = content.match(/\*\*设计原理\*\*[：:]\s*\n(.*?)(?=\*\*|$)/s);
  if (designMatch) {
    return designMatch[1].trim();
  }
  return null;
}

/**
 * 移除设计原理注释，只保留代码
 */
function removeDesignPrinciples(content) {
  return content.replace(/\*\*设计原理\*\*[：:].*?(?=\*\*|$)/gs, '').trim();
}

/**
 * 格式化设计原理为HTML
 */
function formatDesignPrinciples(principles) {
  if (!principles) return '';
  
  const lines = principles.split('\n');
  const formatted = lines.map(line => {
    if (line.trim().startsWith('- **')) {
      const match = line.match(/- \*\*(.*?)\*\*[：:]\s*(.*)/);
      if (match) {
        return `<p><strong>${match[1]}</strong>：${match[2]}</p>`;
      }
    }
    return `<p>${line}</p>`;
  }).join('\n');
  
  return `
    <div class="design-principles">
      <h4>💡 设计原理</h4>
      <div class="principles-content">
        ${formatted}
      </div>
    </div>
  `;
}

/**
 * 创建代码块AST节点（让Shiki处理高亮）
 */
function createCodeBlockNode(codeContent, language = 'python') {
  return {
    type: 'code',
    lang: language,
    value: codeContent,
    meta: null
  };
}

/**
 * HTML转义
 */
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * 解析属性
 */
function parseAttributes(attrs) {
  const result = {};
  const regex = /(\w+)="([^"]*)"/g;
  let match;
  while ((match = regex.exec(attrs)) !== null) {
    result[match[1]] = match[2];
  }
  return result;
}

export default function remarkCodeFromFile() {
  return async (tree, file) => {
    const codeNodes = [];
    
    // 查找所有 CodeFromFile 标签
    visit(tree, 'html', (node, index, parent) => {
      const match = node.value.match(/<CodeFromFile\s+([^>]*)\s*\/?>/);
      if (match) {
        codeNodes.push({ node, index, parent, attrs: match[1] });
      }
    });
    
    // 处理每个 CodeFromFile 标签（从后往前处理，避免索引变化）
    for (let i = codeNodes.length - 1; i >= 0; i--) {
      const { node, index, parent, attrs } = codeNodes[i];
      const props = parseAttributes(attrs);
      const filePath = props.filePath;
      const language = props.language || 'python';
      const showDesignPrinciples = props.showDesignPrinciples !== 'false';
      
      if (!filePath) {
        node.value = `<div class="code-error"><p>⚠️ 缺少 filePath 属性</p></div>`;
        continue;
      }
      
      try {
        // 获取项目根目录
        // code_library在TRQuant项目根目录
        // 当前工作目录是 extension/AShare-manual，需要向上找到TRQuant根目录
        let projectRoot = process.cwd();
        
        // 如果当前在AShare-manual目录下，需要向上找到TRQuant根目录
        if (projectRoot.includes('AShare-manual')) {
          // 从 extension/AShare-manual 向上到 TRQuant 根目录
          // 例如: /home/taotao/dev/QuantTest/TRQuant/extension/AShare-manual
          // 需要得到: /home/taotao/dev/QuantTest/TRQuant
          const parts = projectRoot.split('/AShare-manual');
          projectRoot = parts[0] || process.cwd();
          
          // 如果还在extension目录下，再向上一步
          if (projectRoot.endsWith('/extension')) {
            projectRoot = projectRoot.replace('/extension', '');
          }
        } else if (projectRoot.includes('extension')) {
          // 从 extension 向上到 TRQuant 根目录
          const parts = projectRoot.split('/extension');
          projectRoot = parts[0] || process.cwd();
        }
        
        // 确保路径正确
        const fullPath = join(projectRoot, filePath);
        
        // 调试信息（仅在开发环境）
        if (process.env.NODE_ENV !== 'production') {
          console.log(`[remark-code-from-file] Loading: ${filePath}`);
          console.log(`[remark-code-from-file] Project root: ${projectRoot}`);
          console.log(`[remark-code-from-file] Full path: ${fullPath}`);
        }
        
        // 读取代码文件
        const codeContent = await readFile(fullPath, 'utf-8');
        
        // 提取设计原理
        let designPrinciples = null;
        if (showDesignPrinciples) {
          designPrinciples = extractDesignPrinciples(codeContent);
        }
        
        // 移除设计原理注释
        const cleanCode = removeDesignPrinciples(codeContent);
        
        // 创建要插入的节点数组
        const nodesToInsert = [];
        
        // 如果有设计原理，先插入HTML节点
        if (showDesignPrinciples && designPrinciples) {
          nodesToInsert.push({
            type: 'html',
            value: formatDesignPrinciples(designPrinciples)
          });
        }
        
        // 创建代码块AST节点（让Shiki处理高亮）
        const codeBlockNode = createCodeBlockNode(cleanCode, language);
        nodesToInsert.push(codeBlockNode);
        
        // 替换HTML节点为新的节点数组
        if (parent && typeof index === 'number') {
          parent.children.splice(index, 1, ...nodesToInsert);
        } else {
          // 降级方案：生成HTML包装的Markdown代码块
          // 使用div包装，内部包含设计原理和代码块
          const designHtml = showDesignPrinciples && designPrinciples 
            ? formatDesignPrinciples(designPrinciples) 
            : '';
          
          // 生成包含Markdown代码块的HTML
          // 使用特殊的div标记，让后续处理识别
          node.type = 'html';
          node.value = `${designHtml}<div class="code-from-file-wrapper">\`\`\`${language}\n${cleanCode}\n\`\`\`</div>`;
        }
      } catch (error) {
        node.value = `<div class="code-error"><p>⚠️ 无法加载代码文件: ${filePath}. 错误: ${error.message}</p></div>`;
        console.error(`[remark-code-from-file] Error loading ${filePath}:`, error);
      }
    }
  };
}

