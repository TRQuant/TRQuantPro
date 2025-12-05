#!/usr/bin/env node

// 批量添加金融术语脚本
// 自动在Markdown文件中识别金融术语并添加GlossaryTerm组件

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 金融术语列表
const FINANCE_TERMS = [
  'CAGR', 'TAM', 'ROE', 'PEG', 'EBITDA', '护城河', '高倍股', 
  '自由现金流', '估值', '技术分析', 'PE', 'PB', 'PS', 'DCF',
  'Beta', 'Alpha', 'Sharpe', '夏普比率', '波动率', '流动性'
];

// 需要处理的目录
const CHAPTER_DIRS = [
  '../src/pages/book1',
  '../src/pages/book2'
];

// 统计信息
const stats = {
  totalFiles: 0,
  processedFiles: 0,
  modifiedFiles: 0,
  totalTerms: 0,
  errors: []
};

// 处理单个文件
async function processFile(filePath) {
  try {
    stats.totalFiles++;
    console.log(`📄 处理文件: ${path.relative(process.cwd(), filePath)}`);
    
    let content = await fs.readFile(filePath, 'utf-8');
    let modified = false;
    let termsAdded = 0;
    
    // 检查是否已经导入了GlossaryTerm组件
    const hasImport = content.includes('import GlossaryTerm');
    const hasGlossaryTerms = content.includes('<GlossaryTerm');
    
    // 如果没有导入，添加导入语句
    if (!hasImport) {
      const importStatement = '\nimport GlossaryTerm from \'../../../components/GlossaryTerm.astro\';\n';
      
      // 在frontmatter后添加导入
      const frontmatterEnd = content.indexOf('\n---\n', content.indexOf('---') + 3);
      if (frontmatterEnd !== -1) {
        content = content.slice(0, frontmatterEnd + 4) + importStatement + content.slice(frontmatterEnd + 4);
        modified = true;
      }
    }
    
    // 避免处理已经包含GlossaryTerm的内容
    if (hasGlossaryTerms) {
      console.log(`⏭️  跳过已处理文件: ${path.relative(process.cwd(), filePath)}`);
      return { modified: false, termsAdded: 0 };
    }
    
    // 处理每个金融术语
    for (const term of FINANCE_TERMS) {
      const pattern = new RegExp(`\\b${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi');
      
      // 避免替换HTML标签内的内容
      const htmlRegex = /<[^>]*>/g;
      const htmlMatches = [];
      let htmlIndex = 0;
      
      // 临时替换HTML标签
      content = content.replace(htmlRegex, (match) => {
        const placeholder = `__HTML_${htmlIndex}__`;
        htmlMatches[htmlIndex] = match;
        htmlIndex++;
        return placeholder;
      });
      
      // 替换术语
      const newContent = content.replace(pattern, (match) => {
        // 检查是否在HTML标签中
        if (match.includes('__HTML_')) {
          return match;
        }
        
        // 检查是否已经被处理过
        if (match.includes('GlossaryTerm')) {
          return match;
        }
        
        // 替换为GlossaryTerm组件
        termsAdded++;
        return `<GlossaryTerm term="${term}" />`;
      });
      
      if (newContent !== content) {
        content = newContent;
        modified = true;
      }
      
      // 恢复HTML标签
      htmlMatches.forEach((match, index) => {
        content = content.replace(`__HTML_${index}__`, match);
      });
    }
    
    if (modified) {
      // 备份原文件
      const backupPath = filePath + '.backup';
      await fs.writeFile(backupPath, await fs.readFile(filePath, 'utf-8'));
      
      // 写入修改后的内容
      await fs.writeFile(filePath, content);
      
      stats.modifiedFiles++;
      stats.totalTerms += termsAdded;
      console.log(`✅ 已更新: ${path.relative(process.cwd(), filePath)} (添加 ${termsAdded} 个术语)`);
    } else {
      console.log(`⏭️  无需修改: ${path.relative(process.cwd(), filePath)}`);
    }
    
    stats.processedFiles++;
    return { modified, termsAdded };
    
  } catch (error) {
    const errorMsg = `处理文件失败: ${path.relative(process.cwd(), filePath)} - ${error.message}`;
    console.error(`❌ ${errorMsg}`);
    stats.errors.push(errorMsg);
    return { modified: false, termsAdded: 0 };
  }
}

// 递归处理目录
async function processDirectory(dirPath) {
  try {
    const items = await fs.readdir(dirPath, { withFileTypes: true });
    
    for (const item of items) {
      const fullPath = path.join(dirPath, item.name);
      
      if (item.isDirectory()) {
        // 递归处理子目录
        await processDirectory(fullPath);
      } else if (item.isFile() && item.name.endsWith('.md')) {
        // 处理Markdown文件
        await processFile(fullPath);
      }
    }
  } catch (error) {
    const errorMsg = `处理目录失败: ${dirPath} - ${error.message}`;
    console.error(`❌ ${errorMsg}`);
    stats.errors.push(errorMsg);
  }
}

// 生成报告
function generateReport() {
  console.log('\n📊 处理报告');
  console.log('='.repeat(50));
  console.log(`📁 总文件数: ${stats.totalFiles}`);
  console.log(`✅ 成功处理: ${stats.processedFiles}`);
  console.log(`🔄 修改文件: ${stats.modifiedFiles}`);
  console.log(`📝 添加术语: ${stats.totalTerms}`);
  console.log(`❌ 错误数量: ${stats.errors.length}`);
  
  if (stats.errors.length > 0) {
    console.log('\n❌ 错误详情:');
    stats.errors.forEach((error, index) => {
      console.log(`${index + 1}. ${error}`);
    });
  }
  
  console.log('\n💡 建议:');
  console.log('- 检查备份文件 (*.backup)');
  console.log('- 验证修改后的文件内容');
  console.log('- 测试GlossaryTerm组件功能');
}

// 主函数
async function main() {
  console.log('🚀 开始批量添加金融术语...');
  console.log(`📋 处理术语: ${FINANCE_TERMS.join(', ')}`);
  console.log(`📁 处理目录: ${CHAPTER_DIRS.join(', ')}`);
  
  const startTime = Date.now();
  
  for (const dir of CHAPTER_DIRS) {
    const fullDirPath = path.resolve(__dirname, dir);
    console.log(`\n📁 处理目录: ${fullDirPath}`);
    
    try {
      await processDirectory(fullDirPath);
    } catch (error) {
      console.error(`❌ 处理目录失败: ${fullDirPath}`, error);
    }
  }
  
  const endTime = Date.now();
  const duration = ((endTime - startTime) / 1000).toFixed(2);
  
  console.log(`\n⏱️  处理完成，耗时: ${duration}秒`);
  generateReport();
  
  // 保存报告到文件
  const reportPath = path.join(__dirname, 'glossary-batch-report.json');
  await fs.writeFile(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    duration: `${duration}s`,
    stats,
    terms: FINANCE_TERMS
  }, null, 2));
  
  console.log(`📄 详细报告已保存: ${reportPath}`);
}

// 运行脚本
main().catch(console.error); 
 