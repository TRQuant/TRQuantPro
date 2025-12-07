/**
 * 策略优化模块接口定义
 * =====================
 */

import {
    // OptimizationConfig, // 暂时未使用
    StrategyConfig,
    OptimizationTarget,
    BacktestResult,
    OptimizationResult,
    OptimizationProgress,
    OptimizationContext
} from './types';

/**
 * 优化算法接口
 */
export interface OptimizationAlgorithm {
    /**
     * 算法名称
     */
    name: string;
    
    /**
     * 执行优化
     */
    optimize(
        config: StrategyConfig,
        target: OptimizationTarget,
        context: OptimizationContext,
        onProgress?: (progress: OptimizationProgress) => void
    ): Promise<OptimizationResult>;
    
    /**
     * 停止优化
     */
    stop(): void;
}

/**
 * 回测接口
 */
export interface BacktestInterface {
    /**
     * 执行回测
     */
    runBacktest(
        strategyConfig: StrategyConfig,
        backtestConfig: {
            startDate: string;
            endDate: string;
            initialCapital: number;
            commission?: number;
        }
    ): Promise<BacktestResult>;
    
    /**
     * 批量回测
     */
    runBatchBacktests(
        strategyConfigs: StrategyConfig[],
        backtestConfig: {
            startDate: string;
            endDate: string;
            initialCapital: number;
            commission?: number;
        }
    ): Promise<BacktestResult[]>;
    
    /**
     * 检查回测任务状态
     */
    checkStatus(taskId: string): Promise<'pending' | 'running' | 'completed' | 'failed'>;
}

/**
 * 结果分析接口
 */
export interface ResultAnalyzer {
    /**
     * 分析回测结果
     */
    analyze(result: BacktestResult): {
        strengths: string[];
        weaknesses: string[];
        risks: string[];
        suggestions: string[];
    };
    
    /**
     * 对比两个回测结果
     */
    compare(result1: BacktestResult, result2: BacktestResult): {
        improvements: Array<{
            metric: string;
            change: number;
            percentage: number;
        }>;
        regressions: Array<{
            metric: string;
            change: number;
            percentage: number;
        }>;
        summary: string;
    };
    
    /**
     * 生成优化报告
     */
    generateReport(optimizationResult: OptimizationResult): string;
}

/**
 * 版本信息
 */
export interface VersionInfo {
    strategyId: string;
    version: string;
    timestamp: string;
    parameters: Record<string, string | number | boolean>;
    backtestResult?: BacktestResult;
    notes?: string;
}

/**
 * 版本管理接口
 */
export interface VersionManager {
    /**
     * 保存策略版本
     */
    saveVersion(version: {
        strategyId: string;
        version: string;
        parameters: Record<string, string | number | boolean>;
        code: string;
        backtestResult?: BacktestResult;
        generatedBy: 'algorithm' | 'ai' | 'user';
        notes?: string;
    }): Promise<void>;
    
    /**
     * 获取策略版本列表
     */
    getVersions(strategyId: string): Promise<VersionInfo[]>;
    
    /**
     * 获取版本详情
     */
    getVersion(strategyId: string, version: string): Promise<VersionInfo | null>;
    
    /**
     * 获取版本代码
     */
    getVersionCode(strategyId: string, version: string): Promise<string | null>;
    
    /**
     * 对比两个版本
     */
    compareVersions(
        strategyId: string,
        version1: string,
        version2: string
    ): Promise<{
        parameterChanges: Array<{
            parameter: string;
            oldValue: string | number | boolean;
            newValue: string | number | boolean;
        }>;
        performanceComparison: {
            metric: string;
            version1Value: number;
            version2Value: number;
            change: number;
            changePercent: number;
        }[];
        codeChanges?: {
            additions: number;
            deletions: number;
            diff: string;
        };
    }>;
    
    /**
     * 删除版本
     */
    deleteVersion(strategyId: string, version: string): Promise<void>;
}

/**
 * AI辅助接口
 */
export interface AIAssistant {
    /**
     * 根据回测结果改进策略
     */
    optimizeStrategy(request: {
        strategyCode: string;
        backtestResult: BacktestResult;
        optimizationGoal: string;
        constraints?: string[];
        context?: OptimizationContext;
    }): Promise<{
        modifiedCode: string;
        changes: Array<{
            type: string;
            description: string;
            before: string | number | boolean | null | Record<string, unknown>;
            after: string | number | boolean | null | Record<string, unknown>;
            reason: string;
        }>;
        explanation: string;
    }>;
    
    /**
     * 生成策略说明
     */
    generateExplanation(
        strategyCode: string,
        changes: Array<{
            type: string;
            description: string;
            before: string | number | boolean | null | Record<string, unknown>;
            after: string | number | boolean | null | Record<string, unknown>;
        }>
    ): Promise<string>;
}




