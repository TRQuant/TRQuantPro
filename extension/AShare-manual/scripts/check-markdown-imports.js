#!/usr/bin/env node

/**
 * 检查Markdown文件中的错误import语句
 * 用于防止在Markdown文件中使用Astro组件的import
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 项目根目录
const projectRoot = path.join(__dirname, '..');
const pagesDir = path.join(projectRoot, 'src', 'pages');

// 错误文件列表
const errorFiles = [];

/**
 * 递归搜索目录中的Markdown文件
 */
function findMarkdownFiles(dir) {
  const files = [];
  
  try {
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        files.push(...findMarkdownFiles(fullPath));
      } else if (item.endsWith('.md')) {
        files.push(fullPath);
      }
    }
  } catch (error) {
    console.error(`Error reading directory ${dir}:`, error.message);
  }
  
  return files;
}

/**
 * 检查单个文件中的错误import
 */
function checkFileForImports(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    const errors = [];
    
    lines.forEach((line, index) => {
      // 检查是否有import语句
      if (line.trim().startsWith('import')) {
        // 检查是否import Astro组件
        if (line.includes('.astro')) {
          errors.push({
            line: index + 1,
            content: line.trim(),
            type: 'astro_import'
          });
        }
      }
    });
    
    if (errors.length > 0) {
      errorFiles.push({
        file: path.relative(projectRoot, filePath),
        errors
      });
    }
  } catch (error) {
    console.error(`Error reading file ${filePath}:`, error.message);
  }
}

/**
 * 主函数
 */
function main() {
  console.log('🔍 检查Markdown文件中的错误import语句...\n');
  
  // 查找所有Markdown文件
  const markdownFiles = findMarkdownFiles(pagesDir);
  console.log(`📁 找到 ${markdownFiles.length} 个Markdown文件`);
  
  // 检查每个文件
  markdownFiles.forEach(file => {
    checkFileForImports(file);
  });
  
  // 输出结果
  if (errorFiles.length === 0) {
    console.log('✅ 所有Markdown文件都没有错误的import语句！');
    process.exit(0);
  } else {
    console.log(`❌ 发现 ${errorFiles.length} 个文件包含错误的import语句：\n`);
    
    errorFiles.forEach(({ file, errors }) => {
      console.log(`📄 ${file}:`);
      errors.forEach(error => {
        console.log(`  第${error.line}行: ${error.content}`);
      });
      console.log('');
    });
    
    console.log('🚨 请修复以上错误：');
    console.log('   - 移除Markdown文件中的Astro组件import语句');
    console.log('   - 使用内容处理器或布局文件注入组件');
    console.log('   - 参考 docs/markdown-import-rules.md 了解正确做法');
    
    process.exit(1);
  }
}

// 运行检查
main(); 