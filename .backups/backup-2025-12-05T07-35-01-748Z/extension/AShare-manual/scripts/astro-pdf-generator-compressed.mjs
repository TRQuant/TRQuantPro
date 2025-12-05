#!/usr/bin/env node

/**
 * Astro PDF Generator - Compressed Version
 * 直接生成压缩版本的PDF，大幅减小文件大小
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

class AstroPDFGeneratorCompressed {
  constructor(options = {}) {
    this.baseURL = options.baseURL || baseURL;
    this.outputDir = options.outputDir || outputDir;
    this.browser = null;
    this.concurrency = options.concurrency || 2; // 降低并发数
    this.activePages = new Set();
    this.language = options.language || 'CN';
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
        '--window-size=1200,800', // 减小窗口大小
        '--disable-images', // 禁用图片加载以加快速度
        '--disable-javascript' // 禁用JavaScript
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
      // 设置更小的视口
      await page.setViewport({ width: 1200, height: 800 });
      await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
      
      // 禁用图片和CSS以加快加载
      await page.setRequestInterception(true);
      page.on('request', (req) => {
        if (req.resourceType() === 'image' || req.resourceType() === 'stylesheet') {
          req.abort();
        } else {
          req.continue();
        }
      });
      
      console.log(`📄 正在生成: ${url}`);
      
      // 访问页面
      await page.goto(url, { 
        waitUntil: 'domcontentloaded', // 只等待DOM加载
        timeout: 15000 // 减少超时时间
      });
      
      // 等待页面完全加载
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 添加优化的打印样式
      await page.addStyleTag({
        content: `
          @media print {
            * { 
              font-size: 10pt !important; 
              line-height: 1.3 !important; 
              color: #000 !important;
              background: #fff !important;
              font-family: Arial, sans-serif !important;
            }
            
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
            
            h1, h2, h3, h4, h5, h6 {
              color: #000 !important;
              border-bottom: 1px solid #ccc !important;
              page-break-after: avoid !important;
              font-size: 12pt !important;
            }
            
            pre, code {
              background: #f5f5f5 !important;
              border: 1px solid #ddd !important;
              color: #000 !important;
              font-family: 'Courier New', monospace !important;
              font-size: 9pt !important;
            }
            
            table {
              border-collapse: collapse !important;
              width: 100% !important;
              font-size: 9pt !important;
            }
            
            th, td {
              border: 1px solid #ddd !important;
              padding: 4px !important;
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
        printBackground: false, // 不打印背景以减小文件大小
        margin: {
          top: '1.5cm',
          right: '1cm',
          bottom: '1.5cm',
          left: '1cm'
        },
        displayHeaderFooter: false, // 不显示页眉页脚
        preferCSSPageSize: true
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
    console.log(`📚 开始生成 ${bookPath} 的 ${language} 版本PDF（压缩版）...`);
    
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
        const filename = `${file.filename.replace('.md', '')}_compressed.pdf`;
        return await this.generateSinglePDF(file.url, filename);
      });
      
      const batchResults = await Promise.all(batchPromises);
      pdfs.push(...batchResults);
      
      // 添加延迟避免过载
      if (i + batchSize < files.length) {
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    }

    // 合并PDF
    if (pdfs.length > 1) {
      const mergedFilename = `${bookPath}_${language}_Complete_compressed.pdf`;
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
}

// 命令行接口
async function main() {
  const [,, command, ...args] = process.argv;
  
  if (!command) {
    console.log(`
使用方法:
  node scripts/astro-pdf-generator-compressed.mjs book <path> <LANG>

示例:
  node scripts/astro-pdf-generator-compressed.mjs book book1 CN
    `);
    return;
  }
  
  const generator = new AstroPDFGeneratorCompressed();
  
  try {
    await generator.init();
    
    switch (command) {
      case 'book':
        if (!args[0] || !args[1]) {
          console.error('❌ 请提供书籍路径和语言参数 (CN/EN)');
          return;
        }
        await generator.generateBookPDF(args[0], args[1]);
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

export default AstroPDFGeneratorCompressed; 