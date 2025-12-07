/**
 * 策略优化模块主入口
 * ===================
 * 
 * 根据《策略优化模块设计方案》实现的核心优化引擎
 */

import * as vscode from 'vscode';
import { logger } from '../../../utils/logger';
import {
    OptimizationConfig,
    StrategyConfig,
    OptimizationTarget,
    OptimizationResult,
    OptimizationContext,
    BacktestResult
} from './types';
import { OptimizationAlgorithm, BacktestInterface, ResultAnalyzer, VersionManager, AIAssistant } from './interfaces';

const MODULE = 'StrategyOptimizer';

/**
 * 策略优化引擎
 * 
 * 核心组件：
 * - 优化决策引擎：根据评估结果决定如何调整策略
 * - 回测接口组件：与回测系统对接，批量提交候选策略
 * - 结果分析与记录组件：收集、对比、记录优化结果
 */
export class StrategyOptimizationEngine {
    private algorithms: Map<string, OptimizationAlgorithm> = new Map();
    private backtestInterface: BacktestInterface | null = null;
    private resultAnalyzer: ResultAnalyzer | null = null;
    private versionManager: VersionManager | null = null;
    private aiAssistant: AIAssistant | null = null;
    
    constructor() {
        // 初始化将在 registerStrategyOptimizer 中完成
    }
    
    /**
     * 注册优化算法
     */
    registerAlgorithm(name: string, algorithm: OptimizationAlgorithm): void {
        this.algorithms.set(name, algorithm);
        logger.info(`优化算法已注册: ${name}`, MODULE);
    }
    
    /**
     * 设置回测接口
     */
    setBacktestInterface(backtest: BacktestInterface): void {
        this.backtestInterface = backtest;
        logger.info('回测接口已设置', MODULE);
    }
    
    /**
     * 设置结果分析器
     */
    setResultAnalyzer(analyzer: ResultAnalyzer): void {
        this.resultAnalyzer = analyzer;
        logger.info('结果分析器已设置', MODULE);
    }
    
    /**
     * 设置版本管理器
     */
    setVersionManager(manager: VersionManager): void {
        this.versionManager = manager;
        logger.info('版本管理器已设置', MODULE);
    }
    
    /**
     * 设置AI助手
     */
    setAIAssistant(assistant: AIAssistant): void {
        this.aiAssistant = assistant;
        logger.info('AI助手已设置', MODULE);
    }
    
    /**
     * 执行策略优化
     */
    async optimize(
        strategyConfig: StrategyConfig,
        optimizationConfig: OptimizationConfig,
        target: OptimizationTarget,
        context: OptimizationContext,
        onProgress?: (progress: any) => void
    ): Promise<OptimizationResult> {
        if (!this.backtestInterface) {
            throw new Error('回测接口未设置');
        }
        
        const algorithm = this.algorithms.get(optimizationConfig.algorithm);
        if (!algorithm) {
            throw new Error(`优化算法未找到: ${optimizationConfig.algorithm}`);
        }
        
        logger.info('开始策略优化', MODULE, {
            algorithm: optimizationConfig.algorithm,
            strategyId: strategyConfig.code?.substring(0, 50) || 'unknown'
        });
        
        try {
            const result = await algorithm.optimize(
                strategyConfig,
                target,
                context,
                onProgress
            );
            
            // 保存版本
            if (this.versionManager && strategyConfig.code) {
                await this.versionManager.saveVersion({
                    strategyId: result.strategyId,
                    version: result.bestStrategy.version,
                    parameters: result.bestStrategy.parameters,
                    code: strategyConfig.code,
                    backtestResult: result.bestStrategy.backtestResult,
                    generatedBy: 'algorithm',
                    notes: `优化算法: ${optimizationConfig.algorithm}`
                });
            }
            
            logger.info('策略优化完成', MODULE, {
                optimizationId: result.optimizationId,
                improvement: result.comparison.improvement.length
            });
            
            return result;
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            logger.error(`策略优化失败: ${errorMsg}`, MODULE);
            throw error;
        }
    }
    
    /**
     * 使用AI辅助优化策略
     */
    async optimizeWithAI(
        strategyCode: string,
        backtestResult: BacktestResult,
        optimizationGoal: string,
        context: OptimizationContext,
        constraints?: string[]
    ): Promise<{
        modifiedCode: string;
        changes: Array<{
            type: string;
            description: string;
            before: any;
            after: any;
            reason: string;
        }>;
        explanation: string;
    }> {
        if (!this.aiAssistant) {
            throw new Error('AI助手未设置');
        }
        
        logger.info('开始AI辅助优化', MODULE);
        
        try {
            const result = await this.aiAssistant.optimizeStrategy({
                strategyCode,
                backtestResult,
                optimizationGoal,
                constraints,
                context
            });
            
            logger.info('AI辅助优化完成', MODULE, {
                changesCount: result.changes.length
            });
            
            return result;
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            logger.error(`AI辅助优化失败: ${errorMsg}`, MODULE);
            throw error;
        }
    }
    
    /**
     * 获取可用算法列表
     */
    getAvailableAlgorithms(): string[] {
        return Array.from(this.algorithms.keys());
    }
    
    /**
     * 获取回测接口
     */
    getBacktestInterface(): BacktestInterface | null {
        return this.backtestInterface;
    }
    
    /**
     * 获取结果分析器
     */
    getResultAnalyzer(): ResultAnalyzer | null {
        return this.resultAnalyzer;
    }
    
    /**
     * 获取版本管理器
     */
    getVersionManager(): VersionManager | null {
        return this.versionManager;
    }
    
    /**
     * 获取AI助手
     */
    getAIAssistant(): AIAssistant | null {
        return this.aiAssistant;
    }
}

// 单例实例
let optimizationEngine: StrategyOptimizationEngine | null = null;

/**
 * 获取策略优化引擎实例
 */
export function getOptimizationEngine(): StrategyOptimizationEngine {
    if (!optimizationEngine) {
        optimizationEngine = new StrategyOptimizationEngine();
    }
    return optimizationEngine;
}

/**
 * 导出类型
 */
export * from './types';
export type { OptimizationAlgorithm, BacktestInterface, ResultAnalyzer, VersionManager, AIAssistant, VersionInfo } from './interfaces';

/**
 * 导出算法
 */
export { GridSearchAlgorithm } from './algorithms/gridSearch';
export { RandomSearchAlgorithm } from './algorithms/randomSearch';

/**
 * 导出组件实现
 */
export { BacktestInterfaceImpl } from './backtest/backtestInterface';
export { ResultAnalyzerImpl } from './analyzer/resultAnalyzer';
export { VersionManagerImpl, createVersionManager } from './versionManager';
export { AIAssistantImpl, createAIAssistant } from './aiAssistant';

/**
 * 导出 Walk-Forward 分析
 */
export { 
    WalkForwardAnalyzer, 
    createWalkForwardAnalyzer,
    DEFAULT_WALK_FORWARD_CONFIG,
    type WalkForwardConfig,
    type WalkForwardResult,
    type WalkForwardPeriodResult
} from './walkForward';

