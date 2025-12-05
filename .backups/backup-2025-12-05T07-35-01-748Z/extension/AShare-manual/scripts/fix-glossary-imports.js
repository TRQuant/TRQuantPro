#!/usr/bin/env node

// 修正金融术语导入脚本
// 移除错误的import语句，使用正确的span标签方式

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

// 本地金融术语库
const LOCAL_GLOSSARY = {
  'CAGR': {
    term: 'CAGR',
    fullName: 'Compound Annual Growth Rate',
    description: '复合年增长率，衡量投资或业务在特定时间段内的年均增长速度',
    category: '财务指标',
    example: '一家公司5年内从100万增长到200万，CAGR = (200/100)^(1/5) - 1 = 14.87%'
  },
  'TAM': {
    term: 'TAM',
    fullName: 'Total Addressable Market',
    description: '可寻址市场总规模，指产品或服务在特定市场中的最大潜在需求',
    category: '市场分析',
    example: '电动汽车TAM = 全球汽车市场 × 电动化渗透率'
  },
  'ROE': {
    term: 'ROE',
    fullName: 'Return on Equity',
    description: '净资产收益率，衡量公司利用股东投资创造利润的效率',
    category: '财务指标',
    example: 'ROE = 净利润 / 股东权益，通常>15%为优秀'
  },
  'PEG': {
    term: 'PEG',
    fullName: 'Price/Earnings to Growth',
    description: '市盈率相对盈利增长比率，用于评估成长股的估值合理性',
    category: '估值指标',
    example: 'PEG = PE / 盈利增长率，<1通常认为被低估'
  },
  'EBITDA': {
    term: 'EBITDA',
    fullName: 'Earnings Before Interest, Taxes, Depreciation and Amortization',
    description: '息税折旧摊销前利润，反映公司核心经营盈利能力',
    category: '财务指标',
    example: 'EBITDA = 净利润 + 利息 + 税费 + 折旧 + 摊销'
  },
  '护城河': {
    term: '护城河',
    fullName: 'Economic Moat',
    description: '企业长期竞争优势，能够抵御竞争对手侵蚀的能力',
    category: '投资分析',
    example: '品牌价值、专利技术、网络效应、规模经济等'
  },
  '高倍股': {
    term: '高倍股',
    fullName: 'Multibagger',
    description: '能够带来数倍回报的股票，通常指3-10倍以上收益',
    category: '投资概念',
    example: '如NVIDIA、特斯拉等在特定时期的表现'
  },
  '自由现金流': {
    term: '自由现金流',
    fullName: 'Free Cash Flow',
    description: '企业经营活动产生的现金减去资本支出后的净现金流',
    category: '财务指标',
    example: 'FCF = 经营现金流 - 资本支出'
  },
  '估值': {
    term: '估值',
    fullName: 'Valuation',
    description: '对企业或资产价值的评估，常用PE、PB、PS等指标',
    category: '投资分析',
    example: 'PE估值、DCF估值、相对估值等'
  },
  '技术分析': {
    term: '技术分析',
    fullName: 'Technical Analysis',
    description: '通过价格图表和交易量分析预测股价走势的方法',
    category: '分析方法',
    example: '移动平均线、RSI、MACD等技术指标'
  }
};

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
    
    // 移除错误的import语句
    const importPattern = /import\s+GlossaryTerm\s+from\s+['"][^'"]+['"];?\s*\n/g;
    if (importPattern.test(content)) {
      content = content.replace(importPattern, '');
      modified = true;
      console.log(`🗑️  移除了错误的import语句`);
    }
    
    // 移除已存在的GlossaryTerm组件调用
    const glossaryPattern = /<GlossaryTerm[^>]*\/>/g;
    if (glossaryPattern.test(content)) {
      content = content.replace(glossaryPattern, (match) => {
        // 提取term属性
        const termMatch = match.match(/term="([^"]+)"/);
        if (termMatch) {
          const term = termMatch[1];
          const definition = LOCAL_GLOSSARY[term.toUpperCase()] || LOCAL_GLOSSARY[term];
          if (definition) {
            termsAdded++;
            return `<span class="glossary-term" data-term="${term}" data-definition='${JSON.stringify(definition)}' title="${definition.description}">${term}</span>`;
          }
        }
        return match;
      });
      modified = true;
    }
    
    // 处理未处理的金融术语
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
        if (match.includes('glossary-term')) {
          return match;
        }
        
        // 替换为span标签
        const definition = LOCAL_GLOSSARY[term.toUpperCase()] || LOCAL_GLOSSARY[term];
        if (definition) {
          termsAdded++;
          return `<span class="glossary-term" data-term="${term}" data-definition='${JSON.stringify(definition)}' title="${definition.description}">${match}</span>`;
        }
        
        return match;
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
  
  console.log('\n💡 修正说明:');
  console.log('- 移除了错误的import语句');
  console.log('- 使用span标签替代GlossaryTerm组件');
  console.log('- 通过HandbookLayout全局处理悬浮提示');
}

// 主函数
async function main() {
  console.log('🔧 开始修正金融术语实现方式...');
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
  const reportPath = path.join(__dirname, 'glossary-fix-report.json');
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
 