/**
 * 策略学习引擎
 * ============
 * 
 * 从多个来源学习和积累量化策略知识：
 * 1. 文档学习 - 解析API文档、最佳实践
 * 2. 历史学习 - 分析成功策略的模式
 * 3. 反馈学习 - 根据用户反馈优化
 */

import * as fs from 'fs';
import * as path from 'path';
import { KnowledgeStore, getKnowledgeStore } from './knowledgeStore';
import { codeAnalyzer } from '../analyzer/codeAnalyzer';
import {
    StrategyPattern,
    BestPractice,
    UserFeedback,
    StrategyAnalysis,
    Platform
} from '../types';

// ============================================================
// 学习引擎类
// ============================================================

export class StrategyLearner {
    private store: KnowledgeStore;
    private learningLog: string[] = [];
    
    constructor(storagePath: string) {
        this.store = getKnowledgeStore(storagePath);
    }
    
    // ============================================================
    // 文档学习
    // ============================================================
    
    /**
     * 从文档中学习
     */
    async learnFromDocuments(docPaths: string[]): Promise<{
        learned: number;
        patterns: string[];
        practices: string[];
    }> {
        const result = {
            learned: 0,
            patterns: [] as string[],
            practices: [] as string[]
        };
        
        for (const docPath of docPaths) {
            try {
                if (!fs.existsSync(docPath)) continue;
                
                const content = fs.readFileSync(docPath, 'utf-8');
                const ext = path.extname(docPath).toLowerCase();
                
                if (ext === '.md' || ext === '.txt') {
                    const extracted = this.extractFromMarkdown(content);
                    result.patterns.push(...extracted.patterns);
                    result.practices.push(...extracted.practices);
                } else if (ext === '.py') {
                    const extracted = this.extractFromPython(content, docPath);
                    result.patterns.push(...extracted.patterns);
                }
                
                result.learned++;
            } catch (e) {
                this.log(`学习文档失败 ${docPath}: ${e}`);
            }
        }
        
        this.store.autoSave();
        return result;
    }
    
    /**
     * 从Markdown文档提取知识
     */
    private extractFromMarkdown(content: string): {
        patterns: string[];
        practices: string[];
    } {
        const patterns: string[] = [];
        const practices: string[] = [];
        
        // 提取代码块
        const codeBlocks = content.matchAll(/```python\n([\s\S]*?)```/g);
        for (const match of codeBlocks) {
            const code = match[1];
            
            // 检测函数定义
            const funcMatch = code.match(/def\s+(\w+)\s*\([^)]*\):/);
            if (funcMatch) {
                const funcName = funcMatch[1];
                
                // 根据函数名判断类型
                if (funcName.includes('select') || funcName.includes('filter') || funcName.includes('stock')) {
                    this.addLearnedPattern({
                        id: `doc_${funcName}_${Date.now()}`,
                        name: this.formatFunctionName(funcName),
                        category: 'selection',
                        description: `从文档学习的选股函数`,
                        codeTemplate: code,
                        effectiveness: 70,
                        usageCount: 0
                    });
                    patterns.push(funcName);
                } else if (funcName.includes('stop') || funcName.includes('risk') || funcName.includes('position')) {
                    this.addLearnedPattern({
                        id: `doc_${funcName}_${Date.now()}`,
                        name: this.formatFunctionName(funcName),
                        category: 'risk',
                        description: `从文档学习的风控函数`,
                        codeTemplate: code,
                        effectiveness: 75,
                        usageCount: 0
                    });
                    patterns.push(funcName);
                }
            }
        }
        
        // 提取最佳实践（标题+内容）
        const sections = content.matchAll(/##\s+(.+?)\n([\s\S]*?)(?=\n##|\n#|$)/g);
        for (const match of sections) {
            const title = match[1].trim();
            const body = match[2].trim();
            
            // 检测是否是最佳实践相关内容
            if (title.includes('建议') || title.includes('实践') || 
                title.includes('注意') || title.includes('技巧') ||
                body.includes('推荐') || body.includes('应该')) {
                
                this.addLearnedPractice({
                    id: `doc_bp_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
                    title: title,
                    category: this.categorizeByKeywords(body),
                    description: body.slice(0, 200),
                    example: this.extractFirstCodeBlock(body) || '',
                    references: ['文档学习']
                });
                practices.push(title);
            }
        }
        
        return { patterns, practices };
    }
    
    /**
     * 从Python文件提取模式
     */
    private extractFromPython(code: string, filePath: string): {
        patterns: string[];
    } {
        const patterns: string[] = [];
        const analysis = codeAnalyzer.analyze(code, path.basename(filePath));
        
        // 提取选股模式
        for (const block of analysis.components.stockSelection) {
            if (block.content.length > 100) {  // 有实质内容
                this.addLearnedPattern({
                    id: `py_${block.name}_${Date.now()}`,
                    name: this.formatFunctionName(block.name),
                    category: 'selection',
                    description: `从 ${path.basename(filePath)} 学习的选股逻辑`,
                    codeTemplate: block.content,
                    effectiveness: 70,
                    usageCount: 0
                });
                patterns.push(block.name);
            }
        }
        
        // 提取风控模式
        for (const block of analysis.components.riskControl) {
            if (block.content.length > 50) {
                this.addLearnedPattern({
                    id: `py_${block.name}_${Date.now()}`,
                    name: this.formatFunctionName(block.name),
                    category: 'risk',
                    description: `从 ${path.basename(filePath)} 学习的风控逻辑`,
                    codeTemplate: block.content,
                    effectiveness: 75,
                    usageCount: 0
                });
                patterns.push(block.name);
            }
        }
        
        return { patterns };
    }
    
    // ============================================================
    // 历史学习
    // ============================================================
    
    /**
     * 从历史策略学习
     */
    async learnFromHistory(strategies: Array<{
        code: string;
        filename: string;
        performance?: {
            returns: number;
            sharpe: number;
            maxDrawdown: number;
        };
    }>): Promise<{
        analyzed: number;
        successPatterns: string[];
        failurePatterns: string[];
    }> {
        const result = {
            analyzed: 0,
            successPatterns: [] as string[],
            failurePatterns: [] as string[]
        };
        
        for (const strategy of strategies) {
            try {
                const analysis = codeAnalyzer.analyze(strategy.code, strategy.filename);
                
                // 判断策略是否成功（基于performance）
                const isSuccess = strategy.performance && 
                    strategy.performance.returns > 0.1 && 
                    strategy.performance.sharpe > 1.0 &&
                    strategy.performance.maxDrawdown > -0.2;
                
                // 提取模式并更新有效性
                if (isSuccess) {
                    this.extractAndUpdatePatterns(analysis, 'success');
                    result.successPatterns.push(strategy.filename);
                } else if (strategy.performance && strategy.performance.returns < -0.1) {
                    this.extractAndUpdatePatterns(analysis, 'failure');
                    result.failurePatterns.push(strategy.filename);
                }
                
                result.analyzed++;
            } catch (e) {
                this.log(`分析策略失败 ${strategy.filename}: ${e}`);
            }
        }
        
        this.store.autoSave();
        return result;
    }
    
    /**
     * 提取并更新模式有效性
     */
    private extractAndUpdatePatterns(
        analysis: StrategyAnalysis, 
        outcome: 'success' | 'failure'
    ): void {
        const delta = outcome === 'success' ? 5 : -3;
        
        // 检查使用的因子
        for (const factor of analysis.dependencies.factors) {
            const patternId = `factor_${factor.type}`;
            const existing = this.store.getPatternById(patternId);
            if (existing) {
                this.store.updatePatternEffectiveness(
                    patternId, 
                    Math.max(0, Math.min(100, existing.effectiveness + delta))
                );
            }
        }
        
        // 检查风控模块
        if (analysis.components.riskControl.length > 0) {
            // 有风控的策略成功，增加风控模式的有效性
            if (outcome === 'success') {
                this.store.updatePatternEffectiveness('fixed_stop_loss', 
                    Math.min(100, this.store.getPatternById('fixed_stop_loss')?.effectiveness || 80 + 2));
            }
        } else {
            // 无风控且失败，记录教训
            if (outcome === 'failure') {
                this.log('学习: 无风控策略更容易失败');
            }
        }
    }
    
    // ============================================================
    // 反馈学习
    // ============================================================
    
    /**
     * 记录用户反馈
     */
    recordFeedback(feedback: Omit<UserFeedback, 'timestamp' | 'resolved'>): void {
        this.store.addFeedback({
            ...feedback,
            timestamp: new Date().toISOString(),
            resolved: false
        });
        this.store.autoSave();
    }
    
    /**
     * 处理反馈并学习
     */
    async processFeedback(): Promise<{
        processed: number;
        improvements: string[];
    }> {
        const result = {
            processed: 0,
            improvements: [] as string[]
        };
        
        const pendingFeedback = this.store.getFeedback(false);
        
        for (const feedback of pendingFeedback) {
            try {
                switch (feedback.type) {
                    case 'correction':
                        // 用户纠正了转换结果
                        this.learnFromCorrection(feedback);
                        result.improvements.push(`修正了 ${feedback.strategyId} 的转换规则`);
                        break;
                        
                    case 'improvement':
                        // 用户提出了改进建议
                        this.addLearnedPractice({
                            id: `feedback_${Date.now()}`,
                            title: '用户建议的最佳实践',
                            category: '用户贡献',
                            description: feedback.content,
                            example: '',
                            references: ['用户反馈']
                        });
                        result.improvements.push(`添加了新的最佳实践`);
                        break;
                        
                    case 'bug':
                        // 记录bug，不学习
                        this.log(`Bug反馈: ${feedback.content}`);
                        break;
                }
                
                this.store.resolveFeedback(feedback.timestamp);
                result.processed++;
            } catch (e) {
                this.log(`处理反馈失败: ${e}`);
            }
        }
        
        this.store.autoSave();
        return result;
    }
    
    /**
     * 从用户纠正中学习
     */
    private learnFromCorrection(feedback: UserFeedback): void {
        // 解析纠正内容，提取新的映射规则
        const correctionMatch = feedback.content.match(/(\w+)\s*(?:->|→|应该是)\s*(\w+)/);
        if (correctionMatch) {
            const [, original, corrected] = correctionMatch;
            this.log(`学习纠正: ${original} -> ${corrected}`);
            // 这里可以更新API映射
        }
    }
    
    // ============================================================
    // 推荐系统
    // ============================================================
    
    /**
     * 基于分析结果推荐模式
     */
    recommendPatterns(analysis: StrategyAnalysis): StrategyPattern[] {
        const recommendations: StrategyPattern[] = [];
        const allPatterns = this.store.getPatterns();
        
        // 如果缺少风控，推荐风控模式
        if (analysis.components.riskControl.length === 0) {
            const riskPatterns = allPatterns
                .filter(p => p.category === 'risk')
                .sort((a, b) => b.effectiveness - a.effectiveness)
                .slice(0, 3);
            recommendations.push(...riskPatterns);
        }
        
        // 如果选股简单，推荐更复杂的选股模式
        if (analysis.components.stockSelection.length <= 1) {
            const selectionPatterns = allPatterns
                .filter(p => p.category === 'selection')
                .sort((a, b) => b.effectiveness - a.effectiveness)
                .slice(0, 2);
            recommendations.push(...selectionPatterns);
        }
        
        // 根据使用的因子推荐相关模式
        for (const factor of analysis.dependencies.factors) {
            const relatedPatterns = allPatterns.filter(p => 
                p.codeTemplate.toLowerCase().includes(factor.type)
            );
            if (relatedPatterns.length > 0) {
                recommendations.push(relatedPatterns[0]);
            }
        }
        
        // 去重
        const uniqueIds = new Set<string>();
        return recommendations.filter(p => {
            if (uniqueIds.has(p.id)) return false;
            uniqueIds.add(p.id);
            return true;
        });
    }
    
    /**
     * 推荐最佳实践
     */
    recommendBestPractices(analysis: StrategyAnalysis): BestPractice[] {
        const recommendations: BestPractice[] = [];
        const allPractices = this.store.getBestPractices();
        
        // 检查是否缺少止损
        const hasStopLoss = analysis.components.riskControl.some(
            b => b.content.toLowerCase().includes('stop_loss') || 
                 b.content.includes('止损')
        );
        if (!hasStopLoss) {
            const stopLossPractice = allPractices.find(bp => bp.id === 'bp_stop_loss');
            if (stopLossPractice) recommendations.push(stopLossPractice);
        }
        
        // 检查是否过滤ST
        const hasSTFilter = analysis.components.stockSelection.some(
            b => b.content.toLowerCase().includes('is_st') ||
                 b.content.includes('ST')
        );
        if (!hasSTFilter) {
            const stPractice = allPractices.find(bp => bp.id === 'bp_avoid_st');
            if (stPractice) recommendations.push(stPractice);
        }
        
        // 检查日志记录
        const hasLogging = analysis.dependencies.apis.some(
            api => api.name.includes('log')
        );
        if (!hasLogging) {
            const logPractice = allPractices.find(bp => bp.id === 'bp_logging');
            if (logPractice) recommendations.push(logPractice);
        }
        
        return recommendations;
    }
    
    // ============================================================
    // 辅助方法
    // ============================================================
    
    private addLearnedPattern(pattern: StrategyPattern): void {
        this.store.addPattern(pattern);
        this.log(`学习新模式: ${pattern.name}`);
    }
    
    private addLearnedPractice(practice: BestPractice): void {
        this.store.addBestPractice(practice);
        this.log(`学习新实践: ${practice.title}`);
    }
    
    private formatFunctionName(name: string): string {
        return name
            .replace(/_/g, ' ')
            .replace(/([A-Z])/g, ' $1')
            .trim()
            .split(' ')
            .map(w => w.charAt(0).toUpperCase() + w.slice(1))
            .join(' ');
    }
    
    private categorizeByKeywords(text: string): string {
        const lower = text.toLowerCase();
        if (lower.includes('风控') || lower.includes('止损') || lower.includes('风险')) return '风控';
        if (lower.includes('选股') || lower.includes('筛选') || lower.includes('因子')) return '选股';
        if (lower.includes('执行') || lower.includes('下单') || lower.includes('交易')) return '执行';
        if (lower.includes('调试') || lower.includes('日志') || lower.includes('记录')) return '调试';
        return '通用';
    }
    
    private extractFirstCodeBlock(text: string): string | null {
        const match = text.match(/```(?:python)?\n([\s\S]*?)```/);
        return match ? match[1] : null;
    }
    
    private log(message: string): void {
        const entry = `[${new Date().toISOString()}] ${message}`;
        this.learningLog.push(entry);
        console.log(`[StrategyLearner] ${message}`);
    }
    
    /**
     * 获取学习日志
     */
    getLearningLog(): string[] {
        return this.learningLog;
    }
    
    /**
     * 获取知识库统计
     */
    getStats() {
        return this.store.getStats();
    }
    
    /**
     * 保存所有更改
     */
    save(): void {
        this.store.save();
    }
}

// 导出工厂函数
export function createStrategyLearner(storagePath: string): StrategyLearner {
    return new StrategyLearner(storagePath);
}






