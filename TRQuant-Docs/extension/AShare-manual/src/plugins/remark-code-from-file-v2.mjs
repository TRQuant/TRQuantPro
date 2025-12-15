/**
 * Remark插件：从文件读取代码并嵌入到Markdown中（支持Shiki代码高亮）
 * 
 * 功能：
 * 1. 识别Markdown中的 `<CodeFromFile>` 标签
 * 2. 读取指定的代码文件
 * 3. 提取设计原理说明
 * 4. 替换为AST代码块节点（让Shiki处理高亮）
 * 
 * 使用方式：
 * <CodeFromFile filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py" />
 */

import { readFile } from 'fs/promises';
import { join } from 'path';
import { visit } from 'unist-util-visit';

/**
 * 提取设计原理说明
 */
function extractDesignPrinciples(content) {
  // 匹配 **设计原理**：后面的内容，直到下一个 **开头的部分（如**为什么这样设计**）
  // 使用[\s\S]匹配包括换行符在内的所有字符，非贪婪匹配到下一个**为什么这样设计**之前
  const designMatch = content.match(/\*\*设计原理\*\*[：:]\s*\n([\s\S]*?)(?=\n\s*\*\*为什么这样设计\*\*|\n\s*\*\*[^*]|$)/);
  if (designMatch) {
    let principles = designMatch[1].trim();
    // 如果提取的内容为空或只有空白，返回null
    if (!principles || principles.length === 0) {
      return null;
    }
    return principles;
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
        let projectRoot = process.cwd();
        if (projectRoot.includes('AShare-manual')) {
          const parts = projectRoot.split('/AShare-manual');
          projectRoot = parts[0] || process.cwd();
          if (projectRoot.endsWith('/extension')) {
            projectRoot = projectRoot.replace('/extension', '');
          }
        } else if (projectRoot.includes('extension')) {
          const parts = projectRoot.split('/extension');
          projectRoot = parts[0] || process.cwd();
        }
        
        const fullPath = join(projectRoot, filePath);
        
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
        nodesToInsert.push({
          type: 'code',
          lang: language,
          value: cleanCode,
          meta: null
        });
        
        // 替换HTML节点为新的节点数组
        // 关键：使用AST节点替换，让Shiki处理代码高亮
        if (parent && typeof index === 'number') {
          // 替换节点：删除原HTML节点，插入新节点数组
          parent.children.splice(index, 1, ...nodesToInsert);
        } else {
          // 降级方案：如果无法获取parent，生成HTML包装
          // 注意：这种方式不会触发Shiki代码高亮
          const designHtml = showDesignPrinciples && designPrinciples 
            ? formatDesignPrinciples(designPrinciples) 
            : '';
          // 转义HTML特殊字符
          const escapedCode = cleanCode
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
          node.value = `${designHtml}<pre class="language-${language}"><code class="language-${language}">${escapedCode}</code></pre>`;
        }
      } catch (error) {
        node.value = `<div class="code-error"><p>⚠️ 无法加载代码文件: ${filePath}. 错误: ${error.message}</p></div>`;
        console.error(`[remark-code-from-file] Error loading ${filePath}:`, error);
      }
    }
  };
}

