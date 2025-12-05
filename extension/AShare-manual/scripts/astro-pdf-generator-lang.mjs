#!/usr/bin/env node

/**
 * Astro PDF Generator with Language Filter
 * 支持语言过滤的PDF生成解决方案
 * 可以按中文(CN)或英文(EN)分别生成PDF
 */

import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { promises as fs } from 'fs';

const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer');
const { PDFDocument } = require('pdf-lib');
const { glob } = require('glob');

const __dirname = dirname(fileURLToPath(import.meta.url));
const baseURL = 'http://localhost:4321';
const outputDir = join(__dirname, '../dist/pdf');

class AstroPDFGeneratorWithLang {
  constructor(options = {}) {
    this.baseURL = options.baseURL || baseURL;
    this.outputDir = options.outputDir || outputDir;
    this.browser = null;
    this.concurrency = options.concurrency || 3;
    this.activePages = new Set();
    this.language = options.language || 'CN'; // 默认中文
  }

  async init() {
    await fs.mkdir(this.outputDir, { recursive: true });
    
    console.log('🚀 正在启动 Puppeteer 浏览器...');
    this.browser = await puppeteer.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu',
        '--window-size=1920,1080'
      ]
    });
    
    console.log('✅ 浏览器已启动');
  }

  async cleanup() {
    if (this.browser) {
      await this.browser.close();
      console.log('🔄 浏览器已关闭');
    }
  }

  // 获取指定语言的文件列表
  async getLanguageFiles(bookPath, language = 'CN') {
    const projectRoot = join(__dirname, '..');
    const bookDir = join(projectRoot, 'src/pages', bookPath);
    
    if (!(await fs.stat(bookDir).catch(() => false))) {
      throw new Error(`书籍路径不存在: ${bookPath}`);
    }

    const files = [];
    
    // 获取所有Markdown文件
    const allFiles = await glob('**/*.md', { 
      cwd: bookDir,
      absolute: true 
    });

    // 按语言过滤文件
    for (const file of allFiles) {
      const filename = file.split('/').pop();
      
      // 匹配语言后缀
      if (filename.includes(`_${language}.md`)) {
        files.push({
          path: file,
          filename: filename,
          relativePath: file.replace(bookDir, '').replace(/^\/+/, ''),
          url: this.getPageURL(bookPath, file.replace(bookDir, '').replace(/^\/+/, ''))
        });
      }
    }

    // 按章节顺序排序
    files.sort((a, b) => {
      const aMatch = a.filename.match(/^(\d+\.?\d*)/);
      const bMatch = b.filename.match(/^(\d+\.?\d*)/);
      
      if (aMatch && bMatch) {
        const aNum = parseFloat(aMatch[1]);
        const bNum = parseFloat(bMatch[1]);
        return aNum - bNum;
      }
      
      return a.filename.localeCompare(b.filename);
    });

    return files;
  }

  // 生成页面URL
  getPageURL(bookPath, filePath) {
    const urlPath = filePath
      .replace(/\.md$/, '')
      .replace(/\\/g, '/')
      .replace(/^\/+/, '');
    
    return `${this.baseURL}/${bookPath}/${urlPath}`;
  }

  async generateSinglePDF(url, filename) {
    const page = await this.browser.newPage();
    this.activePages.add(page);
    
    try {
      await page.setViewport({ width: 1920, height: 1080 });
      await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
      
      console.log(`📄 正在生成: ${url}`);
      
      await page.goto(url, { 
        waitUntil: ['networkidle0', 'domcontentloaded'],
        timeout: 30000 
      });
      
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // 添加打印样式
      await page.addStyleTag({
        content: `
          @media print {
            .no-print, .pdf-export-btn, .nav-container, .sidebar, .toc-container,
            nav, .navbar, header, footer, .breadcrumb, .pagination, button, input, select, textarea,
            .interactive, .tooltip, .modal, .dropdown, .menu, .navigation { 
              display: none !important; 
            }
            
            .emoji, .icon, .card-icon, .decorative-image,
            h1::before, h2::before, h3::before, h4::before, h5::before, h6::before,
            *::before, *::after { 
              display: none !important; 
              content: none !important; 
            }
            
            body { 
              font-size: 11pt !important; 
              line-height: 1.4 !important; 
              color: #000 !important;
              background: #fff !important;
              font-family: Arial, sans-serif !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
              color: #000 !important;
              border-bottom: 1px solid #ccc !important;
              page-break-after: avoid !important;
            }
            
            pre, code {
              background: #f5f5f5 !important;
              border: 1px solid #ddd !important;
              color: #000 !important;
              font-family: 'Courier New', monospace !important;
            }
            
            table {
              border-collapse: collapse !important;
              width: 100% !important;
            }
            
            th, td {
              border: 1px solid #ddd !important;
              padding: 8px !important;
            }
            
            img {
              max-width: 100% !important;
              height: auto !important;
              border: 1px solid #ddd !important;
            }
            
            .page-break { page-break-before: always !important; }
            .no-break { page-break-inside: avoid !important; }
          }
        `
      });
      
      const outputPath = join(this.outputDir, filename);
      await page.pdf({
        path: outputPath,
        format: 'A4',
        printBackground: true,
        margin: {
          top: '2cm',
          right: '1.5cm',
          bottom: '2cm',
          left: '1.5cm'
        },
        displayHeaderFooter: true,
        headerTemplate: `
          <div style="font-size: 10px; text-align: center; width: 100%; margin: 0 1cm;">
            <span class="title"></span>
          </div>
        `,
        footerTemplate: `
          <div style="font-size: 10px; text-align: center; width: 100%; margin: 0 1cm;">
            <span class="pageNumber"></span> / <span class="totalPages"></span>
          </div>
        `
      });

      console.log(`✅ 生成成功: ${outputPath}`);
      return outputPath;
    } catch (error) {
      console.error(`❌ 生成失败 ${url}:`, error);
      throw error;
    } finally {
      this.activePages.delete(page);
      await page.close();
    }
  }

  // 生成指定语言的整册PDF
  async generateBookPDF(bookPath, language = 'CN') {
    console.log(`📚 开始生成 ${bookPath} 的 ${language} 版本PDF...`);
    
    const files = await this.getLanguageFiles(bookPath, language);
    
    if (files.length === 0) {
      console.log(`⚠️  未找到 ${language} 语言的文件`);
      return;
    }

    console.log(`📋 找到 ${files.length} 个 ${language} 文件:`);
    files.forEach(file => {
      console.log(`  - ${file.filename}`);
    });

    const pdfs = [];
    const batchSize = this.concurrency;
    
    for (let i = 0; i < files.length; i += batchSize) {
      const batch = files.slice(i, i + batchSize);
      const batchPromises = batch.map(async (file) => {
        const filename = `${file.filename.replace('.md', '')}.pdf`;
        return await this.generateSinglePDF(file.url, filename);
      });
      
      const batchResults = await Promise.all(batchPromises);
      pdfs.push(...batchResults);
      
      // 添加延迟避免过载
      if (i + batchSize < files.length) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }

    // 合并PDF
    if (pdfs.length > 1) {
      const mergedFilename = `${bookPath}_${language}_Complete.pdf`;
      await this.mergePDFs(pdfs, mergedFilename);
      console.log(`✅ 整册PDF生成完成: ${mergedFilename}`);
    } else if (pdfs.length === 1) {
      console.log(`✅ 单文件PDF生成完成: ${pdfs[0]}`);
    }
  }

  // 合并多个PDF文件
  async mergePDFs(pdfPaths, outputFilename) {
    console.log(`🔗 正在合并 ${pdfPaths.length} 个PDF文件...`);
    
    const mergedPdf = await PDFDocument.create();
    
    for (const pdfPath of pdfPaths) {
      try {
        const pdfBytes = await fs.readFile(pdfPath);
        const pdf = await PDFDocument.load(pdfBytes);
        const copiedPages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
        copiedPages.forEach((page) => mergedPdf.addPage(page));
      } catch (error) {
        console.error(`❌ 合并PDF失败 ${pdfPath}:`, error);
      }
    }
    
    const mergedPdfBytes = await mergedPdf.save();
    const outputPath = join(this.outputDir, outputFilename);
    await fs.writeFile(outputPath, mergedPdfBytes);
    
    // 删除临时文件
    for (const pdfPath of pdfPaths) {
      try {
        await fs.unlink(pdfPath);
      } catch (error) {
        console.warn(`⚠️  删除临时文件失败: ${pdfPath}`);
      }
    }
    
    console.log(`✅ PDF合并完成: ${outputPath}`);
  }

  // 生成指定语言的章节PDF
  async generateChapterPDF(chapterPath, language = 'CN') {
    console.log(`📖 开始生成章节 ${chapterPath} 的 ${language} 版本PDF...`);
    
    const files = await this.getLanguageFiles(chapterPath, language);
    
    if (files.length === 0) {
      console.log(`⚠️  未找到 ${language} 语言的文件`);
      return;
    }

    const pdfs = [];
    for (const file of files) {
      const filename = `${file.filename.replace('.md', '')}.pdf`;
      const pdfPath = await this.generateSinglePDF(file.url, filename);
      pdfs.push(pdfPath);
    }

    // 合并章节PDF
    if (pdfs.length > 1) {
      const chapterName = chapterPath.split('/').pop();
      const mergedFilename = `${chapterName}_${language}_Complete.pdf`;
      await this.mergePDFs(pdfs, mergedFilename);
    }
  }
}

// 命令行接口
async function main() {
  const [,, command, ...args] = process.argv;
  
  if (!command) {
    console.log(`
使用方法:
  npm run pdf:lang:single <URL> <LANG>     # 生成单页PDF (CN/EN)
  npm run pdf:lang:chapter <path> <LANG>   # 生成章节PDF (CN/EN)
  npm run pdf:lang:book <path> <LANG>      # 生成整册PDF (CN/EN)
  npm run pdf:lang:all <LANG>              # 生成所有书籍PDF (CN/EN)

示例:
  npm run pdf:lang:single /book1/001_Chapter1/1.1_Self_Awareness_and_Investment_Wisdom_CN CN
  npm run pdf:lang:chapter book1/001_Chapter1 CN
  npm run pdf:lang:book book1 CN
  npm run pdf:lang:all CN
  npm run pdf:lang:all EN
    `);
    return;
  }
  
  const generator = new AstroPDFGeneratorWithLang();
  
  try {
    await generator.init();
    
    switch (command) {
      case 'single':
        if (!args[0] || !args[1]) {
          console.error('❌ 请提供页面URL和语言参数 (CN/EN)');
          return;
        }
        const url = args[0].startsWith('http') ? args[0] : `${baseURL}${args[0]}`;
        const filename = `${args[0].split('/').pop()}_${args[1]}.pdf`;
        await generator.generateSinglePDF(url, filename);
        break;
        
      case 'chapter':
        if (!args[0] || !args[1]) {
          console.error('❌ 请提供章节路径和语言参数 (CN/EN)');
          return;
        }
        await generator.generateChapterPDF(args[0], args[1]);
        break;
        
      case 'book':
        if (!args[0] || !args[1]) {
          console.error('❌ 请提供书籍路径和语言参数 (CN/EN)');
          return;
        }
        await generator.generateBookPDF(args[0], args[1]);
        break;
        
      case 'all':
        if (!args[0]) {
          console.error('❌ 请提供语言参数 (CN/EN)');
          return;
        }
        const books = ['book1', 'book2', 'book3'];
        for (const book of books) {
          try {
            await generator.generateBookPDF(book, args[0]);
          } catch (error) {
            console.error(`❌ 生成${book}失败:`, error);
          }
        }
        break;
        
      default:
        console.error('❌ 未知命令:', command);
    }
    
  } catch (error) {
    console.error('❌ 执行失败:', error);
  } finally {
    await generator.cleanup();
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export default AstroPDFGeneratorWithLang; 