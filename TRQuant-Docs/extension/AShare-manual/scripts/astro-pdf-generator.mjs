#!/usr/bin/env node

/**
 * Astro PDF Generator
 * 基于Puppeteer的高性能PDF生成解决方案
 * 支持单页、章节、整册PDF生成
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

class AstroPDFGenerator {
  constructor(options = {}) {
    this.baseURL = options.baseURL || baseURL;
    this.outputDir = options.outputDir || outputDir;
    this.browser = null;
    this.concurrency = options.concurrency || 3; // 限制并发数
    this.activePages = new Set();
  }

  async init() {
    // 确保输出目录存在
    await fs.mkdir(this.outputDir, { recursive: true });
    
    // 启动浏览器
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

  async generateSinglePDF(url, filename) {
    const page = await this.browser.newPage();
    this.activePages.add(page);
    
    try {
      // 设置页面和PDF选项
      await page.setViewport({ width: 1920, height: 1080 });
      await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
      
      console.log(`📄 正在生成: ${url}`);
      
      // 访问页面
      await page.goto(url, { 
        waitUntil: ['networkidle0', 'domcontentloaded'],
        timeout: 30000 
      });
      
      // 等待页面完全加载
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
              background: white !important;
              font-family: Arial, sans-serif !important;
            }
            
            * { 
              -webkit-print-color-adjust: exact !important;
              print-color-adjust: exact !important;
            }
            
            .chapter-overview { 
              page-break-inside: avoid !important; 
              margin: 20px 0 !important;
            }
            
            h1, h2, h3, h4, h5, h6 { 
              page-break-after: avoid !important; 
              margin-top: 20px !important;
            }
            
            pre, code { 
              page-break-inside: avoid !important; 
              font-size: 10pt !important;
            }
            
            table { 
              page-break-inside: avoid !important; 
            }
          }
        `
      });
      
      // 生成PDF
      const pdfBuffer = await page.pdf({
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
          <div style="font-size: 10px; width: 100%; text-align: center; color: #666;">
            <span class="title"></span>
          </div>
        `,
        footerTemplate: `
          <div style="font-size: 10px; width: 100%; text-align: center; color: #666;">
            <span class="pageNumber"></span> / <span class="totalPages"></span>
          </div>
        `
      });
      
      // 保存PDF
      const outputPath = join(this.outputDir, filename);
      await fs.writeFile(outputPath, pdfBuffer);
      
      console.log(`✅ PDF 已保存: ${outputPath}`);
      return outputPath;
      
    } catch (error) {
      console.error(`❌ 生成PDF失败: ${url}`, error);
      throw error;
    } finally {
      this.activePages.delete(page);
      await page.close();
    }
  }

  async generateChapterPDF(chapterPath) {
    console.log(`📚 正在生成章节PDF: ${chapterPath}`);
    
    // 获取章节下所有页面
    const pages = await this.getChapterPages(chapterPath);
    console.log(`找到 ${pages.length} 个页面`);
    
    const pdfPaths = [];
    
    // 限制并发生成
    for (let i = 0; i < pages.length; i += this.concurrency) {
      const batch = pages.slice(i, i + this.concurrency);
      const batchPromises = batch.map(async (page) => {
        const url = `${this.baseURL}${page.url}`;
        const filename = `${page.name}.pdf`;
        return this.generateSinglePDF(url, filename);
      });
      
      const batchResults = await Promise.allSettled(batchPromises);
      for (const result of batchResults) {
        if (result.status === 'fulfilled') {
          pdfPaths.push(result.value);
        }
      }
    }
    
    // 合并PDF
    if (pdfPaths.length > 1) {
      const mergedPath = await this.mergePDFs(pdfPaths, `${chapterPath.replace(/\//g, '_')}.pdf`);
      
      // 清理临时文件
      for (const path of pdfPaths) {
        await fs.unlink(path).catch(() => {});
      }
      
      return mergedPath;
    }
    
    return pdfPaths[0];
  }

  async generateBookPDF(bookPath) {
    console.log(`📖 正在生成整册PDF: ${bookPath}`);
    
    // 获取书籍下所有章节
    const chapters = await this.getBookChapters(bookPath);
    console.log(`找到 ${chapters.length} 个章节`);
    
    const pdfPaths = [];
    
    for (const chapter of chapters) {
      try {
        const chapterPDF = await this.generateChapterPDF(chapter);
        pdfPaths.push(chapterPDF);
      } catch (error) {
        console.error(`❌ 章节生成失败: ${chapter}`, error);
      }
    }
    
    // 合并所有章节PDF
    if (pdfPaths.length > 0) {
      const mergedPath = await this.mergePDFs(pdfPaths, `${bookPath.replace(/\//g, '_')}_complete.pdf`);
      
      // 清理临时文件
      for (const path of pdfPaths) {
        await fs.unlink(path).catch(() => {});
      }
      
      return mergedPath;
    }
    
    throw new Error('没有找到任何章节');
  }

  async mergePDFs(pdfPaths, outputFilename) {
    console.log(`🔄 正在合并 ${pdfPaths.length} 个PDF文件...`);
    
    const mergedPdf = await PDFDocument.create();
    
    for (const pdfPath of pdfPaths) {
      try {
        const pdfBytes = await fs.readFile(pdfPath);
        const pdf = await PDFDocument.load(pdfBytes);
        const pages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
        pages.forEach((page) => mergedPdf.addPage(page));
      } catch (error) {
        console.error(`❌ 合并PDF失败: ${pdfPath}`, error);
      }
    }
    
    const mergedPdfBytes = await mergedPdf.save();
    const outputPath = join(this.outputDir, outputFilename);
    await fs.writeFile(outputPath, mergedPdfBytes);
    
    console.log(`✅ 合并完成: ${outputPath}`);
    return outputPath;
  }

  async getChapterPages(chapterPath) {
    // 根据项目结构获取章节页面
    const pattern = `src/pages/${chapterPath}/**/*.md`;
    const files = await glob(pattern);
    
    return files.map(file => {
      const relativePath = file.replace('src/pages/', '').replace('.md', '');
      const name = relativePath.split('/').pop();
      return {
        url: `/${relativePath}`,
        name: name,
        file: file
      };
    }).sort((a, b) => a.name.localeCompare(b.name));
  }

  async getBookChapters(bookPath) {
    // 获取书籍下所有章节目录
    const pattern = `src/pages/${bookPath}/*/`;
    const dirs = await glob(pattern);
    
    return dirs
      .map(dir => dir.replace('src/pages/', '').replace(/\/$/, ''))
      .filter(dir => /\d+_Chapter\d+/.test(dir))
      .sort();
  }
}

// 命令行接口
async function main() {
  const [,, command, ...args] = process.argv;
  
  if (!command) {
    console.log(`
使用方法:
  npm run pdf:single <URL>     # 生成单页PDF
  npm run pdf:chapter <path>   # 生成章节PDF  
  npm run pdf:book <path>      # 生成整册PDF
  npm run pdf:all              # 生成所有PDF

示例:
  npm run pdf:single /book1/001_Chapter1/1.1_Self_Awareness_and_Investment_Wisdom_CN
  npm run pdf:chapter book1/001_Chapter1
  npm run pdf:book book1
  npm run pdf:all
    `);
    return;
  }
  
  const generator = new AstroPDFGenerator();
  
  try {
    await generator.init();
    
    switch (command) {
      case 'single':
        if (!args[0]) {
          console.error('❌ 请提供页面URL');
          return;
        }
        const url = args[0].startsWith('http') ? args[0] : `${baseURL}${args[0]}`;
        const filename = `${args[0].split('/').pop()}.pdf`;
        await generator.generateSinglePDF(url, filename);
        break;
        
      case 'chapter':
        if (!args[0]) {
          console.error('❌ 请提供章节路径');
          return;
        }
        await generator.generateChapterPDF(args[0]);
        break;
        
      case 'book':
        if (!args[0]) {
          console.error('❌ 请提供书籍路径');
          return;
        }
        await generator.generateBookPDF(args[0]);
        break;
        
      case 'all':
        // 生成所有书籍
        const books = ['book1', 'book2'];
        for (const book of books) {
          try {
            await generator.generateBookPDF(book);
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
  main();
}

export default AstroPDFGenerator; 

