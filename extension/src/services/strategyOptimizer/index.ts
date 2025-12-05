/**
 * 策略优化器服务
 * ==============
 * 
 * 主入口文件，整合分析、适配、报告生成、学习功能
 */

import * as vscode from 'vscode';
import { codeAnalyzer } from './analyzer/codeAnalyzer';
import { platformAdapter } from './adapters/platformAdapter';
import { reportGenerator } from './generator/reportGenerator';
import { createStrategyLearner, StrategyLearner, createManualLearner, ManualLearner } from './learner';
import { 
    createStrategyAnalyzer, 
    StrategyAnalyzer,
    StrategyAnalysis as NewStrategyAnalysis 
} from './analyzer/strategyAnalyzer';
import { 
    createOptimizationAdvisor, 
    OptimizationAdvisor, 
    OptimizationReport 
} from './analyzer/optimizationAdvisor';
import {
    StrategyAnalysis,
    ConversionResult,
    StrategyReport,
    Platform,
    StrategyPattern,
    BestPractice
} from './types';

// 导出类型
export * from './types';

// ============================================================
// 策略优化器服务类
// ============================================================

export class StrategyOptimizerService {
    private static instance: StrategyOptimizerService;
    private learner: StrategyLearner | null = null;
    private manualLearner: ManualLearner | null = null;
    private storagePath: string = '';
    private manualPath: string = '';
    
    // 新增：策略分析器和优化建议生成器
    private strategyAnalyzer: StrategyAnalyzer;
    private optimizationAdvisor: OptimizationAdvisor;
    
    private constructor() {
        this.strategyAnalyzer = createStrategyAnalyzer();
        this.optimizationAdvisor = createOptimizationAdvisor();
    }
    
    static getInstance(): StrategyOptimizerService {
        if (!StrategyOptimizerService.instance) {
            StrategyOptimizerService.instance = new StrategyOptimizerService();
        }
        return StrategyOptimizerService.instance;
    }
    
    /**
     * 初始化学习引擎
     */
    initLearner(storagePath: string, manualPath?: string): void {
        this.storagePath = storagePath;
        this.learner = createStrategyLearner(storagePath);
        
        // 初始化手册学习器
        if (manualPath) {
            this.manualPath = manualPath;
            this.manualLearner = createManualLearner(storagePath, manualPath);
        }
    }
    
    /**
     * 获取学习引擎
     */
    getLearner(): StrategyLearner | null {
        return this.learner;
    }
    
    /**
     * 获取手册学习器
     */
    getManualLearner(): ManualLearner | null {
        return this.manualLearner;
    }
    
    /**
     * 从A股实操手册学习
     */
    async learnFromManual(): Promise<{
        success: boolean;
        stats: any;
        log: string[];
    }> {
        if (!this.manualLearner) {
            return { success: false, stats: {}, log: ['手册学习器未初始化'] };
        }
        return this.manualLearner.learnFromManual();
    }
    
    /**
     * 监听手册更新
     */
    watchManualUpdates(callback?: (file: string) => void): any {
        if (!this.manualLearner) return null;
        return this.manualLearner.watchForUpdates(callback);
    }
    
    /**
     * 分析策略代码
     */
    analyzeStrategy(code: string, filename?: string): StrategyAnalysis {
        return codeAnalyzer.analyze(code, filename);
    }
    
    /**
     * 转换到目标平台
     */
    convertToPlatform(
        code: string,
        targetPlatform: Platform,
        analysis?: StrategyAnalysis
    ): ConversionResult {
        // 如果没有提供分析结果，先分析
        const strategyAnalysis = analysis || this.analyzeStrategy(code);
        return platformAdapter.convert(code, strategyAnalysis, targetPlatform);
    }
    
    /**
     * 生成策略报告
     */
    generateReport(
        code: string,
        format: 'json' | 'markdown' | 'html' = 'html'
    ): StrategyReport | string {
        const analysis = this.analyzeStrategy(code);
        
        switch (format) {
            case 'json':
                return reportGenerator.generate(analysis);
            case 'markdown':
                return reportGenerator.generateMarkdown(analysis);
            case 'html':
                return reportGenerator.generateHTML(analysis);
            default:
                return reportGenerator.generateHTML(analysis);
        }
    }
    
    /**
     * 一键优化（分析 + 转换 + 报告）
     */
    async optimizeStrategy(
        code: string,
        targetPlatform: Platform,
        filename?: string
    ): Promise<{
        analysis: StrategyAnalysis;
        conversion: ConversionResult;
        report: string;
    }> {
        // 1. 分析
        const analysis = this.analyzeStrategy(code, filename);
        
        // 2. 转换
        const conversion = platformAdapter.convert(code, analysis, targetPlatform);
        
        // 3. 生成报告
        const report = reportGenerator.generateHTML(analysis, conversion);
        
        return { analysis, conversion, report };
    }
    
    /**
     * 快速检查兼容性
     */
    checkCompatibility(code: string): {
        sourcePlatform: Platform;
        compatibility: Record<Platform, { score: number; level: string }>;
    } {
        const analysis = this.analyzeStrategy(code);
        
        return {
            sourcePlatform: analysis.compatibility.sourcePlatform,
            compatibility: {
                joinquant: {
                    score: analysis.compatibility.joinquant.score,
                    level: analysis.compatibility.joinquant.level
                },
                ptrade: {
                    score: analysis.compatibility.ptrade.score,
                    level: analysis.compatibility.ptrade.level
                },
                qmt: {
                    score: analysis.compatibility.qmt.score,
                    level: analysis.compatibility.qmt.level
                },
                universal: { score: 100, level: 'full' }
            }
        };
    }
    
    /**
     * 获取API映射
     */
    getAPIMappings() {
        return platformAdapter.getAllMappings();
    }
    
    /**
     * 获取平台信息
     */
    getPlatformInfo(platform: Platform) {
        const { PLATFORMS } = require('./types');
        return PLATFORMS[platform];
    }
    
    // ============================================================
    // 学习引擎方法
    // ============================================================
    
    /**
     * 从文档学习
     */
    async learnFromDocuments(docPaths: string[]): Promise<{
        learned: number;
        patterns: string[];
        practices: string[];
    }> {
        if (!this.learner) {
            return { learned: 0, patterns: [], practices: [] };
        }
        return this.learner.learnFromDocuments(docPaths);
    }
    
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
        if (!this.learner) {
            return { analyzed: 0, successPatterns: [], failurePatterns: [] };
        }
        return this.learner.learnFromHistory(strategies);
    }
    
    /**
     * 记录用户反馈
     */
    recordFeedback(feedback: {
        strategyId: string;
        type: 'correction' | 'improvement' | 'bug' | 'feature';
        content: string;
    }): void {
        if (this.learner) {
            this.learner.recordFeedback(feedback);
        }
    }
    
    /**
     * 获取推荐模式
     */
    getRecommendedPatterns(code: string): StrategyPattern[] {
        if (!this.learner) return [];
        const analysis = this.analyzeStrategy(code);
        return this.learner.recommendPatterns(analysis);
    }
    
    /**
     * 获取推荐最佳实践
     */
    getRecommendedPractices(code: string): BestPractice[] {
        if (!this.learner) return [];
        const analysis = this.analyzeStrategy(code);
        return this.learner.recommendBestPractices(analysis);
    }
    
    /**
     * 获取学习统计
     */
    getLearningStats(): {
        patterns: number;
        apiMappings: number;
        bestPractices: number;
        feedback: { total: number; resolved: number; pending: number };
    } | null {
        if (!this.learner) return null;
        return this.learner.getStats();
    }
    
    /**
     * 保存学习数据
     */
    saveLearningData(): void {
        if (this.learner) {
            this.learner.save();
        }
    }
    
    // ============================================================
    // 策略分析与优化建议（新增）
    // ============================================================
    
    /**
     * 深度分析策略（新分析器）
     * 提取因子、风控、选股、交易等详细信息
     */
    analyzeStrategyDeep(code: string, fileName?: string): NewStrategyAnalysis {
        return this.strategyAnalyzer.analyze(code, fileName);
    }
    
    /**
     * 生成优化建议报告
     * 基于分析结果和知识库生成具体优化建议
     */
    generateOptimizationReport(code: string, fileName?: string): OptimizationReport {
        // 1. 深度分析
        const analysis = this.strategyAnalyzer.analyze(code, fileName);
        
        // 2. 如果有知识库，设置给优化建议生成器
        // 注：当前版本暂不集成知识库，后续可通过 learner 获取
        
        // 3. 生成优化报告
        return this.optimizationAdvisor.generateReport(analysis);
    }
    
    /**
     * 快速优化检查
     * 返回高优先级问题列表
     */
    quickOptimizationCheck(code: string): Array<{
        priority: 'high' | 'medium' | 'low';
        title: string;
        suggestion: string;
    }> {
        const report = this.generateOptimizationReport(code);
        return report.advices
            .filter(a => a.priority === 'high')
            .map(a => ({
                priority: a.priority,
                title: a.title,
                suggestion: a.description,
            }));
    }
    
    /**
     * 获取策略评分
     */
    getStrategyScore(code: string): {
        overall: number;
        risk: number;
        factor: number;
        selection: number;
        code: number;
    } {
        const report = this.generateOptimizationReport(code);
        return {
            overall: report.overallScore,
            ...report.scoreBreakdown,
        };
    }
}

// 导出单例
export const strategyOptimizer = StrategyOptimizerService.getInstance();

// 导出子模块
export { codeAnalyzer } from './analyzer/codeAnalyzer';
export { platformAdapter } from './adapters/platformAdapter';
export { reportGenerator } from './generator/reportGenerator';
export { createStrategyLearner, StrategyLearner, createManualLearner, ManualLearner } from './learner';

// 导出新分析器
export { 
    createStrategyAnalyzer, 
    StrategyAnalyzer,
    StrategyAnalysis as DeepStrategyAnalysis,
    FactorInfo,
    RiskControlInfo,
    StockSelectionInfo,
    TradingInfo,
    StrategyIssue
} from './analyzer/strategyAnalyzer';
export { 
    createOptimizationAdvisor, 
    OptimizationAdvisor, 
    OptimizationAdvice,
    OptimizationReport 
} from './analyzer/optimizationAdvisor';

// ============================================================
// VS Code Extension 集成函数
// ============================================================

/**
 * 注册策略优化器命令和服务
 * 在 extension.ts 的 activate 函数中调用
 */
export function registerStrategyOptimizer(
    context: vscode.ExtensionContext,
    client?: any
): void {
    const logger = require('../../utils/logger').logger;
    const path = require('path');
    const MODULE = 'StrategyOptimizer';
    
    // 初始化学习引擎存储路径
    const storagePath = context.globalStorageUri.fsPath;
    const manualPath = context.extensionPath 
        ? path.join(context.extensionPath, 'AShare-manual')
        : undefined;
    
    // 初始化策略优化器
    try {
        strategyOptimizer.initLearner(storagePath, manualPath);
        logger.info('策略优化器学习引擎已初始化', MODULE);
    } catch (error: any) {
        logger.warn(`初始化学习引擎失败: ${error}`, MODULE);
    }
    
    // 注册命令（如果需要额外的命令，可以在这里添加）
    // 主要的命令已在 strategyOptimizerPanel 中注册
    
    logger.info('策略优化器服务已注册', MODULE);
}
