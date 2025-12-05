/**
 * A股实操手册学习器
 * ==================
 * 
 * 自动从 AShare-manual 中学习：
 * - 策略模式
 * - 最佳实践
 * - API用法
 * - 风控规则
 * - 行业研究方法
 */

import * as fs from 'fs';
import * as path from 'path';
import { KnowledgeStore, getKnowledgeStore } from './knowledgeStore';
import {
    StrategyPattern,
    BestPractice,
    APIMapping,
    Platform
} from '../types';

// ============================================================
// 手册章节映射
// ============================================================

const MANUAL_SECTIONS = {
    'ashare-book1': {
        name: 'A股投资基础',
        chapters: {
            '001': { name: 'A股市场', category: '基础知识' },
            '002': { name: '投资心理', category: '交易心理' },
            '003': { name: '高倍股', category: '选股策略' },
            '004': { name: '行业分析', category: '行业研究' },
            '005': { name: '基本面', category: '基本面分析' },
            '006': { name: '选股筛选', category: '选股策略' },
            '007': { name: '交易执行', category: '交易执行' },
            '008': { name: '工具使用', category: '工具' },
            '009': { name: '案例分析', category: '实战案例' },
            '010': { name: '交易系统', category: '系统构建' },
        }
    },
    'ashare-book2': {
        name: '宏观经济',
        chapters: {
            '001': { name: '经济周期', category: '宏观择时' },
            '002': { name: '货币政策', category: '政策分析' },
            '003': { name: '财政政策', category: '政策分析' },
            '004': { name: '行业轮动', category: '行业轮动' },
            '005': { name: '市场情绪', category: '情绪分析' },
            '006': { name: '宏观数据', category: '数据分析' },
            '007': { name: '全球影响', category: '全球视野' },
            '008': { name: '风险监控', category: '风控' },
            '009': { name: '宏观择时', category: '宏观择时' },
            '010': { name: '宏观工具', category: '工具' },
        }
    },
    'ashare-book3': {
        name: '个股研究',
        chapters: {
            '001': { name: '研究框架', category: '研究方法' },
            '002': { name: '财务分析', category: '基本面分析' },
            '003': { name: '估值方法', category: '估值' },
            '004': { name: '行业龙头', category: '选股策略' },
            '005': { name: '消费案例', category: '行业研究' },
            '006': { name: '科技案例', category: '行业研究' },
            '007': { name: '周期案例', category: '行业研究' },
            '008': { name: '金融案例', category: '行业研究' },
            '009': { name: '医药案例', category: '行业研究' },
            '010': { name: '报告撰写', category: '研究方法' },
        }
    },
    'ashare-book4': {
        name: '技术分析',
        chapters: {
            '001': { name: '技术分析基础', category: '技术分析' },
            '002': { name: 'K线形态', category: '技术分析' },
            '003': { name: '趋势分析', category: '技术分析' },
            '004': { name: '量价关系', category: '技术分析' },
            '005': { name: '技术指标', category: '技术指标' },
        }
    },
    'ashare-book5': {
        name: '量化专题',
        chapters: {
            '001': { name: '回测基础', category: '回测' },
            '002': { name: 'JQData集成', category: '数据源' },
            '003': { name: '韬睿回测', category: '回测' },
            '004': { name: '报告分析', category: '回测分析' },
            '005': { name: '风险控制', category: '风控' },
            '006': { name: 'PTrade实盘', category: '实盘交易' },
            '007': { name: 'QMT实盘', category: '实盘交易' },
            '008': { name: '策略迭代', category: '策略优化' },
            '009': { name: '文件管理', category: '工具' },
            '010': { name: '完整工作流', category: '系统构建' },
        }
    },
    'ashare': {
        name: 'A股量化核心',
        chapters: {
            '001': { name: 'A股市场', category: '基础知识' },
            '002': { name: '因子框架', category: '因子投资' },
            '003': { name: '高倍股', category: '选股策略' },
            '004': { name: '行业轮动', category: '行业轮动' },
            '005': { name: '多因子', category: '多因子策略' },
            '006': { name: '交易执行', category: '交易执行' },
            '007': { name: '风险控制', category: '风控' },
            '008': { name: '回测系统', category: '回测' },
        }
    }
};

// ============================================================
// 知识提取模式
// ============================================================

const EXTRACTION_PATTERNS = {
    // 代码块提取
    codeBlock: /```python\n([\s\S]*?)```/g,
    
    // 函数定义
    funcDef: /def\s+(\w+)\s*\([^)]*\):\s*\n\s*"""([\s\S]*?)"""/g,
    
    // 最佳实践标记
    bestPractice: /(?:建议|注意|提示|最佳实践|推荐)[：:]\s*(.+?)(?:\n|$)/g,
    
    // 风控规则
    riskRule: /(?:止损|止盈|仓位|风控)[：:]?\s*(.+?)(?:\n|$)/gi,
    
    // 指标公式
    formula: /(?:公式|计算)[：:]\s*(.+?)(?:\n|$)/g,
    
    // API用法
    apiUsage: /(?:get_price|get_fundamentals|order|history|run_daily)\s*\([^)]+\)/g,
};

// ============================================================
// 手册学习器类
// ============================================================

export class ManualLearner {
    private store: KnowledgeStore;
    private manualPath: string;
    private learningLog: string[] = [];
    private stats = {
        filesScanned: 0,
        patternsExtracted: 0,
        practicesExtracted: 0,
        codeBlocksFound: 0
    };
    
    constructor(storagePath: string, manualPath: string) {
        this.store = getKnowledgeStore(storagePath);
        this.manualPath = manualPath;
    }
    
    /**
     * 扫描并学习整个手册
     */
    async learnFromManual(): Promise<{
        success: boolean;
        stats: any;
        log: string[];
    }> {
        this.log('开始扫描A股实操手册...');
        
        const pagesPath = path.join(this.manualPath, 'src', 'pages');
        
        if (!fs.existsSync(pagesPath)) {
            this.log(`手册路径不存在: ${pagesPath}`);
            return { success: false, stats: this.stats, log: this.learningLog };
        }
        
        // 扫描每个书籍目录
        for (const [bookDir, bookInfo] of Object.entries(MANUAL_SECTIONS)) {
            const bookPath = path.join(pagesPath, bookDir);
            if (fs.existsSync(bookPath)) {
                await this.scanBookDirectory(bookPath, bookDir, bookInfo);
            }
        }
        
        // 扫描docs目录的PDF/文档
        const docsPath = path.join(this.manualPath, 'docs');
        if (fs.existsSync(docsPath)) {
            await this.scanDocsDirectory(docsPath);
        }
        
        this.store.save();
        this.log(`学习完成！扫描${this.stats.filesScanned}个文件，提取${this.stats.patternsExtracted}个模式，${this.stats.practicesExtracted}个最佳实践`);
        
        return { success: true, stats: this.stats, log: this.learningLog };
    }
    
    /**
     * 扫描书籍目录
     */
    private async scanBookDirectory(
        bookPath: string, 
        bookDir: string, 
        bookInfo: any
    ): Promise<void> {
        this.log(`扫描: ${bookInfo.name} (${bookDir})`);
        
        const files = this.getAllMarkdownFiles(bookPath);
        
        for (const file of files) {
            try {
                const content = fs.readFileSync(file, 'utf-8');
                const filename = path.basename(file);
                
                // 确定章节信息
                const chapterMatch = filename.match(/(\d{3})_Chapter(\d+)/);
                const chapterNum = chapterMatch ? chapterMatch[1] : '000';
                const chapterInfo = (bookInfo.chapters as any)[chapterNum] || { name: '未知', category: '通用' };
                
                // 提取知识
                this.extractKnowledge(content, {
                    source: `${bookInfo.name} - ${chapterInfo.name}`,
                    category: chapterInfo.category,
                    file: filename
                });
                
                this.stats.filesScanned++;
            } catch (e) {
                this.log(`处理文件失败 ${file}: ${e}`);
            }
        }
    }
    
    /**
     * 扫描docs目录
     */
    private async scanDocsDirectory(docsPath: string): Promise<void> {
        this.log('扫描docs目录...');
        
        const mdFiles = fs.readdirSync(docsPath)
            .filter(f => f.endsWith('.md'))
            .map(f => path.join(docsPath, f));
        
        for (const file of mdFiles) {
            try {
                const content = fs.readFileSync(file, 'utf-8');
                const filename = path.basename(file);
                
                this.extractKnowledge(content, {
                    source: `文档: ${filename}`,
                    category: '参考文档',
                    file: filename
                });
                
                this.stats.filesScanned++;
            } catch (e) {
                // 忽略读取失败
            }
        }
    }
    
    /**
     * 获取所有Markdown文件
     */
    private getAllMarkdownFiles(dir: string): string[] {
        const files: string[] = [];
        
        const items = fs.readdirSync(dir, { withFileTypes: true });
        for (const item of items) {
            const fullPath = path.join(dir, item.name);
            if (item.isDirectory()) {
                files.push(...this.getAllMarkdownFiles(fullPath));
            } else if (item.name.endsWith('.md')) {
                files.push(fullPath);
            }
        }
        
        return files;
    }
    
    /**
     * 提取知识
     */
    private extractKnowledge(
        content: string, 
        meta: { source: string; category: string; file: string }
    ): void {
        // 1. 提取代码块
        const codeBlocks = content.matchAll(EXTRACTION_PATTERNS.codeBlock);
        for (const match of codeBlocks) {
            const code = match[1];
            this.stats.codeBlocksFound++;
            
            // 检测函数并提取为模式
            const funcMatch = code.match(/def\s+(\w+)\s*\([^)]*\):/);
            if (funcMatch) {
                const funcName = funcMatch[1];
                this.addPatternFromCode(funcName, code, meta);
            }
        }
        
        // 2. 提取最佳实践
        const practices = content.matchAll(EXTRACTION_PATTERNS.bestPractice);
        for (const match of practices) {
            const practiceText = match[1].trim();
            if (practiceText.length > 10 && practiceText.length < 200) {
                this.addPractice(practiceText, meta);
            }
        }
        
        // 3. 提取风控规则
        const riskRules = content.matchAll(EXTRACTION_PATTERNS.riskRule);
        for (const match of riskRules) {
            const ruleText = match[1].trim();
            if (ruleText.length > 5 && ruleText.length < 150) {
                this.addPractice(ruleText, { ...meta, category: '风控' });
            }
        }
    }
    
    /**
     * 从代码添加模式
     */
    private addPatternFromCode(
        funcName: string, 
        code: string, 
        meta: { source: string; category: string; file: string }
    ): void {
        // 根据函数名判断类型
        let category: 'selection' | 'timing' | 'risk' | 'execution' = 'execution';
        
        if (funcName.includes('select') || funcName.includes('filter') || funcName.includes('stock')) {
            category = 'selection';
        } else if (funcName.includes('stop') || funcName.includes('risk') || funcName.includes('position')) {
            category = 'risk';
        } else if (funcName.includes('timing') || funcName.includes('signal') || funcName.includes('trend')) {
            category = 'timing';
        }
        
        const pattern: StrategyPattern = {
            id: `manual_${funcName}_${Date.now()}`,
            name: this.formatFunctionName(funcName),
            category,
            description: `从${meta.source}学习的${category === 'selection' ? '选股' : category === 'risk' ? '风控' : category === 'timing' ? '择时' : '执行'}函数`,
            codeTemplate: code.trim(),
            effectiveness: 75,  // 手册中的代码质量较高
            usageCount: 0
        };
        
        this.store.addPattern(pattern);
        this.stats.patternsExtracted++;
    }
    
    /**
     * 添加最佳实践
     */
    private addPractice(text: string, meta: { source: string; category: string }): void {
        const practice: BestPractice = {
            id: `manual_bp_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`,
            title: text.slice(0, 50) + (text.length > 50 ? '...' : ''),
            category: meta.category,
            description: text,
            example: '',
            references: [meta.source]
        };
        
        this.store.addBestPractice(practice);
        this.stats.practicesExtracted++;
    }
    
    /**
     * 监听手册更新（文件变化）
     */
    watchForUpdates(callback?: (file: string) => void): fs.FSWatcher | null {
        const pagesPath = path.join(this.manualPath, 'src', 'pages');
        
        if (!fs.existsSync(pagesPath)) {
            return null;
        }
        
        this.log('开始监听手册更新...');
        
        const watcher = fs.watch(pagesPath, { recursive: true }, (event, filename) => {
            if (filename && filename.endsWith('.md')) {
                this.log(`检测到更新: ${filename}`);
                
                // 重新学习该文件
                const filePath = path.join(pagesPath, filename);
                if (fs.existsSync(filePath)) {
                    try {
                        const content = fs.readFileSync(filePath, 'utf-8');
                        this.extractKnowledge(content, {
                            source: '手册更新',
                            category: '更新内容',
                            file: filename
                        });
                        this.store.save();
                        
                        if (callback) {
                            callback(filename);
                        }
                    } catch (e) {
                        this.log(`处理更新失败: ${e}`);
                    }
                }
            }
        });
        
        return watcher;
    }
    
    /**
     * 获取特定章节的知识
     */
    getChapterKnowledge(bookDir: string, chapterNum: string): {
        patterns: StrategyPattern[];
        practices: BestPractice[];
    } {
        const bookInfo = MANUAL_SECTIONS[bookDir as keyof typeof MANUAL_SECTIONS];
        if (!bookInfo) {
            return { patterns: [], practices: [] };
        }
        
        const chapterInfo = (bookInfo.chapters as any)[chapterNum];
        if (!chapterInfo) {
            return { patterns: [], practices: [] };
        }
        
        const sourcePrefix = `${bookInfo.name} - ${chapterInfo.name}`;
        
        const patterns = this.store.getPatterns().filter(
            p => p.description.includes(sourcePrefix)
        );
        
        const practices = this.store.getBestPractices().filter(
            bp => bp.references.some(r => r.includes(sourcePrefix))
        );
        
        return { patterns, practices };
    }
    
    /**
     * 获取学习统计
     */
    getStats() {
        return {
            ...this.stats,
            knowledgeStore: this.store.getStats()
        };
    }
    
    // ============================================================
    // 辅助方法
    // ============================================================
    
    private formatFunctionName(name: string): string {
        return name
            .replace(/_/g, ' ')
            .replace(/([A-Z])/g, ' $1')
            .trim()
            .split(' ')
            .map(w => w.charAt(0).toUpperCase() + w.slice(1))
            .join(' ');
    }
    
    private log(message: string): void {
        const entry = `[${new Date().toISOString()}] ${message}`;
        this.learningLog.push(entry);
        console.log(`[ManualLearner] ${message}`);
    }
    
    getLearningLog(): string[] {
        return this.learningLog;
    }
}

// ============================================================
// 导出
// ============================================================

export function createManualLearner(storagePath: string, manualPath: string): ManualLearner {
    return new ManualLearner(storagePath, manualPath);
}

