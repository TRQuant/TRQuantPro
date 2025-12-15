#!/usr/bin/env node

/**
 * Astro PDF Export Script
 * 基于Puppeteer的现代化PDF生成解决方案
 * 支持单页、章节、整册导出
 */

import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { promises as fs } from 'fs';
import { glob } from 'glob';

const __dirname = dirname(fileURLToPath(import.meta.url));
const projectRoot = join(__dirname, '..');

class AstroPDFExporter {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || 'http://localhost:4321';
    this.outputDir = options.outputDir || join(projectRoot, 'dist/pdf');
    this.concurrent = options.concurrent || 3; // 并发数
    this.browser = null;
    this.pagePool = [];
  }

  async init() {
    console.log('🚀 初始化PDF导出器...');
    
    // 启动浏览器
    this.browser = await puppeteer.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu',
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding'
      ]
    });

    // 创建输出目录
    await fs.mkdir(this.outputDir, { recursive: true });

    // 预创建页面池
    for (let i = 0; i < this.concurrent; i++) {
      const page = await this.browser.newPage();
      await this.setupPage(page);
      this.pagePool.push(page);
    }

    console.log(`✅ 初始化完成，创建了 ${this.concurrent} 个页面实例`);
  }

  async setupPage(page) {
    // 设置视口
    await page.setViewport({ width: 1200, height: 800 });
    
    // 注入PDF优化样式
    await page.evaluateOnNewDocument(() => {
      // 在每个新页面加载时注入优化样式
      const style = document.createElement('style');
      style.textContent = `
        @media print {
          /* 隐藏导航和交互元素 */
          nav, .navbar, .sidebar, .pdf-export-dropdown, .theme-toggle,
          .back-to-top, .search-box, .print-hide, header, footer,
          .header, .footer, button, input, select, textarea,
          .interactive, .tooltip, .modal, .dropdown, .menu,
          .breadcrumb, .pagination, .toc-sidebar, .share-buttons,
          .reading-time, .mobile-menu-toggle { 
            display: none !important; 
          }
          
          /* 移除装饰性元素 */
          .emoji, .icon, .card-icon, .decorative-image,
          h1::before, h2::before, h3::before, h4::before, h5::before, h6::before,
          *::before, *::after { 
            display: none !important; 
            content: none !important; 
          }
          
          /* 优化打印样式 */
          * {
            background: transparent !important;
            box-shadow: none !important;
            text-shadow: none !important;
            filter: none !important;
            transition: none !important;
            animation: none !important;
          }
          
          html, body {
            background: white !important;
            color: black !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', sans-serif !important;
            font-size: 12pt !important;
            line-height: 1.4 !important;
            margin: 0 !important;
            padding: 0 !important;
          }
          
          /* 标题样式 */
          h1, h2, h3, h4, h5, h6 {
            color: black !important;
            font-weight: bold !important;
            page-break-after: avoid !important;
            margin: 0.5em 0 0.3em 0 !important;
          }
          
          h1 { font-size: 20pt !important; }
          h2 { font-size: 16pt !important; }
          h3 { font-size: 14pt !important; }
          h4 { font-size: 12pt !important; }
          
          /* 段落和文本 */
          p { 
            margin: 0.3em 0 !important; 
            orphans: 3 !important;
            widows: 3 !important;
          }
          
          /* 代码块 */
          pre, code {
            font-family: 'Monaco', 'Consolas', monospace !important;
            font-size: 10pt !important;
            background: #f5f5f5 !important;
            border: 1px solid #ddd !important;
            page-break-inside: avoid !important;
          }
          
          /* 表格 */
          table {
            border-collapse: collapse !important;
            width: 100% !important;
            page-break-inside: avoid !important;
          }
          
          th, td {
            border: 1px solid #ddd !important;
            padding: 8px !important;
            text-align: left !important;
          }
          
          /* 章节概览优化 */
          .chapter-overview, .overview-item, .card {
            background: transparent !important;
            border: 1px solid #ddd !important;
            margin: 0.5em 0 !important;
            padding: 0.5em !important;
            page-break-inside: avoid !important;
          }
          
          /* 分页控制 */
          .page-break-before { page-break-before: always !important; }
          .page-break-after { page-break-after: always !important; }
          .no-page-break { page-break-inside: avoid !important; }
        }
      `;
      document.head.appendChild(style);
    });
  }

  async getPage() {
    return this.pagePool.pop() || await this.browser.newPage();
  }

  async returnPage(page) {
    if (this.pagePool.length < this.concurrent) {
      this.pagePool.push(page);
    } else {
      await page.close();
    }
  }

  async exportPage(url, filename) {
    const page = await this.getPage();
    
    try {
      console.log(`📄 正在导出: ${url}`);
      
      // 导航到页面
      await page.goto(url, { 
        waitUntil: 'networkidle0',
        timeout: 30000 
      });

      // 等待内容加载
      await page.waitForTimeout(500);

      // 生成PDF
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

      console.log(`✅ 导出成功: ${outputPath}`);
      return outputPath;
    } catch (error) {
      console.error(`❌ 导出失败 ${url}:`, error);
      throw error;
    } finally {
      await this.returnPage(page);
    }
  }

  async exportChapter(chapterPages, chapterName) {
    console.log(`📚 开始导出章节: ${chapterName}`);
    
    const tasks = chapterPages.map((pageUrl, index) => ({
      url: pageUrl,
      filename: `${chapterName}_${index + 1}.pdf`
    }));

    // 并发导出所有页面
    const results = await this.processConcurrent(tasks, async (task) => {
      return await this.exportPage(task.url, task.filename);
    });

    console.log(`✅ 章节导出完成: ${chapterName}`);
    return results;
  }

  async exportFullBook(bookStructure) {
    console.log(`📖 开始导出整册: ${bookStructure.title}`);
    
    const allTasks = [];
    
    // 收集所有页面
    for (const chapter of bookStructure.chapters) {
      for (const section of chapter.sections) {
        allTasks.push({
          url: `${this.baseUrl}/${section.path}`,
          filename: `${bookStructure.id}_${chapter.id}_${section.id}.pdf`,
          chapter: chapter.title,
          section: section.title
        });
      }
    }

    // 并发导出所有页面
    const results = await this.processConcurrent(allTasks, async (task) => {
      return await this.exportPage(task.url, task.filename);
    });

    console.log(`✅ 整册导出完成: ${bookStructure.title}`);
    return results;
  }

  async processConcurrent(tasks, processor) {
    const results = [];
    
    for (let i = 0; i < tasks.length; i += this.concurrent) {
      const batch = tasks.slice(i, i + this.concurrent);
      const batchResults = await Promise.allSettled(
        batch.map(task => processor(task))
      );
      
      results.push(...batchResults);
      
      // 显示进度
      const progress = Math.min(i + this.concurrent, tasks.length);
      console.log(`⏳ 进度: ${progress}/${tasks.length}`);
    }
    
    return results;
  }

  async cleanup() {
    console.log('🧹 清理资源...');
    
    // 关闭所有页面
    for (const page of this.pagePool) {
      await page.close();
    }
    
    // 关闭浏览器
    if (this.browser) {
      await this.browser.close();
    }
    
    console.log('✅ 清理完成');
  }
}

// 使用示例
async function main() {
  const exporter = new AstroPDFExporter({
    baseUrl: 'http://localhost:4321',
    outputDir: './dist/pdf',
    concurrent: 3
  });

  try {
    await exporter.init();

    // 示例1: 导出单个页面
    // await exporter.exportPage('http://localhost:4321/book1/001_Chapter1/1.1_Self_Awareness_and_Investment_Wisdom_CN', 'wisdom.pdf');

    // 示例2: 导出整册
    const bookStructure = {
      id: 'book1',
      title: '美股投资实操手册I',
      chapters: [
        {
          id: 'chapter1',
          title: '第一章：认识自己与世界',
          sections: [
            { id: '1.1', title: '自我认知与投资智慧', path: 'book1/001_Chapter1/1.1_Self_Awareness_and_Investment_Wisdom_CN' },
            { id: '1.2', title: '理解世界', path: 'book1/001_Chapter1/1.2_Understanding_the_World_CN' },
            // ... 更多章节
          ]
        },
        // ... 更多章节
      ]
    };

    await exporter.exportFullBook(bookStructure);

  } catch (error) {
    console.error('❌ 导出过程中发生错误:', error);
  } finally {
    await exporter.cleanup();
  }
}

// 如果直接运行此脚本
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export default AstroPDFExporter; 

/**
 * Astro PDF Export Script
 * 基于Puppeteer的现代化PDF生成解决方案
 * 支持单页、章节、整册导出
 */

import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { promises as fs } from 'fs';
import { glob } from 'glob';

const __dirname = dirname(fileURLToPath(import.meta.url));
const projectRoot = join(__dirname, '..');

class AstroPDFExporter {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || 'http://localhost:4321';
    this.outputDir = options.outputDir || join(projectRoot, 'dist/pdf');
    this.concurrent = options.concurrent || 3; // 并发数
    this.browser = null;
    this.pagePool = [];
  }

  async init() {
    console.log('🚀 初始化PDF导出器...');
    
    // 启动浏览器
    this.browser = await puppeteer.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu',
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding'
      ]
    });

    // 创建输出目录
    await fs.mkdir(this.outputDir, { recursive: true });

    // 预创建页面池
    for (let i = 0; i < this.concurrent; i++) {
      const page = await this.browser.newPage();
      await this.setupPage(page);
      this.pagePool.push(page);
    }

    console.log(`✅ 初始化完成，创建了 ${this.concurrent} 个页面实例`);
  }

  async setupPage(page) {
    // 设置视口
    await page.setViewport({ width: 1200, height: 800 });
    
    // 注入PDF优化样式
    await page.evaluateOnNewDocument(() => {
      // 在每个新页面加载时注入优化样式
      const style = document.createElement('style');
      style.textContent = `
        @media print {
          /* 隐藏导航和交互元素 */
          nav, .navbar, .sidebar, .pdf-export-dropdown, .theme-toggle,
          .back-to-top, .search-box, .print-hide, header, footer,
          .header, .footer, button, input, select, textarea,
          .interactive, .tooltip, .modal, .dropdown, .menu,
          .breadcrumb, .pagination, .toc-sidebar, .share-buttons,
          .reading-time, .mobile-menu-toggle { 
            display: none !important; 
          }
          
          /* 移除装饰性元素 */
          .emoji, .icon, .card-icon, .decorative-image,
          h1::before, h2::before, h3::before, h4::before, h5::before, h6::before,
          *::before, *::after { 
            display: none !important; 
            content: none !important; 
          }
          
          /* 优化打印样式 */
          * {
            background: transparent !important;
            box-shadow: none !important;
            text-shadow: none !important;
            filter: none !important;
            transition: none !important;
            animation: none !important;
          }
          
          html, body {
            background: white !important;
            color: black !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', sans-serif !important;
            font-size: 12pt !important;
            line-height: 1.4 !important;
            margin: 0 !important;
            padding: 0 !important;
          }
          
          /* 标题样式 */
          h1, h2, h3, h4, h5, h6 {
            color: black !important;
            font-weight: bold !important;
            page-break-after: avoid !important;
            margin: 0.5em 0 0.3em 0 !important;
          }
          
          h1 { font-size: 20pt !important; }
          h2 { font-size: 16pt !important; }
          h3 { font-size: 14pt !important; }
          h4 { font-size: 12pt !important; }
          
          /* 段落和文本 */
          p { 
            margin: 0.3em 0 !important; 
            orphans: 3 !important;
            widows: 3 !important;
          }
          
          /* 代码块 */
          pre, code {
            font-family: 'Monaco', 'Consolas', monospace !important;
            font-size: 10pt !important;
            background: #f5f5f5 !important;
            border: 1px solid #ddd !important;
            page-break-inside: avoid !important;
          }
          
          /* 表格 */
          table {
            border-collapse: collapse !important;
            width: 100% !important;
            page-break-inside: avoid !important;
          }
          
          th, td {
            border: 1px solid #ddd !important;
            padding: 8px !important;
            text-align: left !important;
          }
          
          /* 章节概览优化 */
          .chapter-overview, .overview-item, .card {
            background: transparent !important;
            border: 1px solid #ddd !important;
            margin: 0.5em 0 !important;
            padding: 0.5em !important;
            page-break-inside: avoid !important;
          }
          
          /* 分页控制 */
          .page-break-before { page-break-before: always !important; }
          .page-break-after { page-break-after: always !important; }
          .no-page-break { page-break-inside: avoid !important; }
        }
      `;
      document.head.appendChild(style);
    });
  }

  async getPage() {
    return this.pagePool.pop() || await this.browser.newPage();
  }

  async returnPage(page) {
    if (this.pagePool.length < this.concurrent) {
      this.pagePool.push(page);
    } else {
      await page.close();
    }
  }

  async exportPage(url, filename) {
    const page = await this.getPage();
    
    try {
      console.log(`📄 正在导出: ${url}`);
      
      // 导航到页面
      await page.goto(url, { 
        waitUntil: 'networkidle0',
        timeout: 30000 
      });

      // 等待内容加载
      await page.waitForTimeout(500);

      // 生成PDF
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

      console.log(`✅ 导出成功: ${outputPath}`);
      return outputPath;
    } catch (error) {
      console.error(`❌ 导出失败 ${url}:`, error);
      throw error;
    } finally {
      await this.returnPage(page);
    }
  }

  async exportChapter(chapterPages, chapterName) {
    console.log(`📚 开始导出章节: ${chapterName}`);
    
    const tasks = chapterPages.map((pageUrl, index) => ({
      url: pageUrl,
      filename: `${chapterName}_${index + 1}.pdf`
    }));

    // 并发导出所有页面
    const results = await this.processConcurrent(tasks, async (task) => {
      return await this.exportPage(task.url, task.filename);
    });

    console.log(`✅ 章节导出完成: ${chapterName}`);
    return results;
  }

  async exportFullBook(bookStructure) {
    console.log(`📖 开始导出整册: ${bookStructure.title}`);
    
    const allTasks = [];
    
    // 收集所有页面
    for (const chapter of bookStructure.chapters) {
      for (const section of chapter.sections) {
        allTasks.push({
          url: `${this.baseUrl}/${section.path}`,
          filename: `${bookStructure.id}_${chapter.id}_${section.id}.pdf`,
          chapter: chapter.title,
          section: section.title
        });
      }
    }

    // 并发导出所有页面
    const results = await this.processConcurrent(allTasks, async (task) => {
      return await this.exportPage(task.url, task.filename);
    });

    console.log(`✅ 整册导出完成: ${bookStructure.title}`);
    return results;
  }

  async processConcurrent(tasks, processor) {
    const results = [];
    
    for (let i = 0; i < tasks.length; i += this.concurrent) {
      const batch = tasks.slice(i, i + this.concurrent);
      const batchResults = await Promise.allSettled(
        batch.map(task => processor(task))
      );
      
      results.push(...batchResults);
      
      // 显示进度
      const progress = Math.min(i + this.concurrent, tasks.length);
      console.log(`⏳ 进度: ${progress}/${tasks.length}`);
    }
    
    return results;
  }

  async cleanup() {
    console.log('🧹 清理资源...');
    
    // 关闭所有页面
    for (const page of this.pagePool) {
      await page.close();
    }
    
    // 关闭浏览器
    if (this.browser) {
      await this.browser.close();
    }
    
    console.log('✅ 清理完成');
  }
}

// 使用示例
async function main() {
  const exporter = new AstroPDFExporter({
    baseUrl: 'http://localhost:4321',
    outputDir: './dist/pdf',
    concurrent: 3
  });

  try {
    await exporter.init();

    // 示例1: 导出单个页面
    // await exporter.exportPage('http://localhost:4321/book1/001_Chapter1/1.1_Self_Awareness_and_Investment_Wisdom_CN', 'wisdom.pdf');

    // 示例2: 导出整册
    const bookStructure = {
      id: 'book1',
      title: '美股投资实操手册I',
      chapters: [
        {
          id: 'chapter1',
          title: '第一章：认识自己与世界',
          sections: [
            { id: '1.1', title: '自我认知与投资智慧', path: 'book1/001_Chapter1/1.1_Self_Awareness_and_Investment_Wisdom_CN' },
            { id: '1.2', title: '理解世界', path: 'book1/001_Chapter1/1.2_Understanding_the_World_CN' },
            // ... 更多章节
          ]
        },
        // ... 更多章节
      ]
    };

    await exporter.exportFullBook(bookStructure);

  } catch (error) {
    console.error('❌ 导出过程中发生错误:', error);
  } finally {
    await exporter.cleanup();
  }
}

// 如果直接运行此脚本
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export default AstroPDFExporter; 
 
 
 
 
 
 
 
 
 
 
 