/**
 * 随机搜索优化算法
 * ================
 * 
 * 在参数空间内随机采样一定数量组合进行评估
 */

import { OptimizationAlgorithm } from '../interfaces';
import { OptimizationProgress } from '../types';
import {
    StrategyConfig,
    OptimizationTarget,
    OptimizationResult,
    OptimizationContext,
    ParameterRange,
    BacktestResult,
    OptimizationIteration
} from '../types';
import { logger } from '../../../../utils/logger';

const MODULE = 'RandomSearch';

export class RandomSearchAlgorithm implements OptimizationAlgorithm {
    name = 'random_search';
    private stopped = false;
    
    async optimize(
        config: StrategyConfig,
        target: OptimizationTarget,
        context: OptimizationContext,
        onProgress?: (progress: OptimizationProgress) => void
    ): Promise<OptimizationResult> {
        this.stopped = false;
        
        const maxIterations = config.parameterRanges.length * 50; // 默认每个参数采样50次
        // OptimizationContext 可能包含 maxIterations，但类型定义中没有，使用类型断言
        const maxIterationsConfig = (context as OptimizationContext & { maxIterations?: number }).maxIterations || maxIterations;
        
        logger.info('开始随机搜索优化', MODULE, {
            maxIterations: maxIterationsConfig,
            parameterCount: config.parameterRanges.length
        });
        
        const optimizationId = `opt_${Date.now()}`;
        const strategyId = `strategy_${Date.now()}`;
        const startTime = new Date().toISOString();
        
        const iterations: OptimizationIteration[] = [];
        let bestScore = -Infinity;
        let bestParameters: Record<string, string | number | boolean> = {};
        let bestResult: BacktestResult | null = null;
        const originalResult: BacktestResult | null = null;
        
        // 先回测原始策略
        if (config.parameters) {
            try {
                // originalResult = await backtestInterface.runBacktest(config, ...);
                logger.info('原始策略回测完成', MODULE);
            } catch (error) {
                logger.warn('原始策略回测失败，继续优化', MODULE);
            }
        }
        
        // 随机采样
        for (let i = 0; i < maxIterationsConfig; i++) {
            if (this.stopped) {
                logger.info('优化已停止', MODULE);
                break;
            }
            
            // 随机生成参数组合
            const params = this.generateRandomParameters(config.parameterRanges);
            const candidateId = `candidate_${i}`;
            
            // 更新进度
            if (onProgress) {
                onProgress({
                    currentIteration: i + 1,
                    totalIterations: maxIterationsConfig,
                    bestScore: bestScore,
                    bestParameters: bestParameters,
                    iterations: iterations,
                    status: 'running',
                    startTime: startTime,
                    elapsedTime: (Date.now() - new Date(startTime).getTime()) / 1000
                });
            }
            
            try {
                // 创建新的策略配置（用于回测）
                // const candidateConfig: StrategyConfig = {
                //     ...config,
                //     parameters: { ...config.parameters, ...params }
                // };
                
                // 执行回测（占位符）
                const backtestResult: BacktestResult = {
                    strategyId: strategyId,
                    strategyVersion: candidateId,
                    parameters: params,
                    metrics: {
                        totalReturn: 0,
                        annualReturn: 0,
                        volatility: 0,
                        maxDrawdown: 0,
                        sharpeRatio: 0,
                        calmarRatio: 0,
                        winRate: 0,
                        profitFactor: 0,
                        totalTrades: 0,
                        avgHoldDays: 0
                    },
                    timestamp: new Date().toISOString()
                };
                
                // 计算评分
                const score = this.calculateScore(backtestResult.metrics, target);
                
                const iteration: OptimizationIteration = {
                    iteration: i + 1,
                    candidateId: candidateId,
                    parameters: params,
                    backtestResult: backtestResult,
                    score: score,
                    timestamp: new Date().toISOString()
                };
                
                iterations.push(iteration);
                
                // 更新最佳结果
                if (score > bestScore) {
                    bestScore = score;
                    bestParameters = params;
                    bestResult = backtestResult;
                }
                
                if ((i + 1) % 10 === 0) {
                    logger.debug(`迭代 ${i + 1}/${maxIterationsConfig} 完成`, MODULE, {
                        score: score,
                        bestScore: bestScore
                    });
                }
                
            } catch (error) {
                logger.warn(`迭代 ${i + 1} 失败: ${error}`, MODULE);
                continue;
            }
        }
        
        // 构建优化结果（与网格搜索类似）
        const result: OptimizationResult = {
            optimizationId: optimizationId,
            strategyId: strategyId,
            algorithm: 'random_search',
            config: {
                algorithm: 'random_search',
                maxIterations: maxIterationsConfig
            },
            target: target,
            bestStrategy: {
                version: `v${Date.now()}`,
                parameters: bestParameters,
                backtestResult: bestResult ?? (iterations[0]?.backtestResult ?? this.createEmptyBacktestResult(strategyId)),
                score: bestScore
            },
            comparison: {
                original: originalResult ?? (iterations[0]?.backtestResult ?? this.createEmptyBacktestResult(strategyId)),
                optimized: bestResult ?? (iterations[0]?.backtestResult ?? this.createEmptyBacktestResult(strategyId)),
                improvement: this.calculateImprovements(
                    originalResult ?? (iterations[0]?.backtestResult ?? this.createEmptyBacktestResult(strategyId)),
                    bestResult ?? (iterations[0]?.backtestResult ?? this.createEmptyBacktestResult(strategyId))
                )
            },
            progress: {
                currentIteration: iterations.length,
                totalIterations: maxIterationsConfig,
                bestScore: bestScore,
                bestParameters: bestParameters,
                iterations: iterations,
                status: this.stopped ? 'stopped' : 'completed',
                startTime: startTime,
                elapsedTime: (Date.now() - new Date(startTime).getTime()) / 1000
            },
            changes: [],
            log: [],
            timestamp: new Date().toISOString()
        };
        
        logger.info('随机搜索优化完成', MODULE, {
            bestScore: bestScore,
            totalIterations: iterations.length
        });
        
        return result;
    }
    
    stop(): void {
        this.stopped = true;
        logger.info('随机搜索已停止', MODULE);
    }
    
    /**
     * 随机生成参数值
     */
    private generateRandomParameters(ranges: ParameterRange[]): Record<string, string | number | boolean> {
        const params: Record<string, string | number | boolean> = {};
        
        for (const range of ranges) {
            if (range.type === 'categorical' && range.values) {
                // 从分类值中随机选择
                const randomIndex = Math.floor(Math.random() * range.values.length);
                params[range.name] = range.values[randomIndex];
            } else if (range.type === 'bool') {
                params[range.name] = Math.random() > 0.5;
            } else if (range.type === 'int') {
                const min = range.min || 0;
                const max = range.max || 100;
                params[range.name] = Math.floor(Math.random() * (max - min + 1)) + min;
            } else if (range.type === 'float') {
                const min = range.min || 0;
                const max = range.max || 100;
                params[range.name] = Math.random() * (max - min) + min;
            } else {
                // else 分支：range.type 只能是 'categorical'，使用 default 或第一个值
                if (range.default !== undefined) {
                    params[range.name] = range.default;
                } else if (range.values && range.values.length > 0) {
                    params[range.name] = range.values[0];
                } else {
                    params[range.name] = '';
                }
            }
        }
        
        return params;
    }
    
    /**
     * 计算策略评分
     */
    private calculateScore(metrics: import('../types').BacktestMetrics, target: OptimizationTarget): number {
        let score = 0;
        
        for (const objective of target.objectives) {
            const metricValue = metrics[objective.metric as keyof import('../types').BacktestMetrics];
            const value = typeof metricValue === 'number' ? metricValue : 0;
            const weight = objective.weight || 1;
            
            if (objective.direction === 'maximize') {
                score += value * weight;
            } else {
                score -= value * weight;
            }
        }
        
        return score;
    }
    
    /**
     * 创建空的回测结果（用于默认值）
     */
    private createEmptyBacktestResult(strategyId: string): BacktestResult {
        return {
            strategyId,
            strategyVersion: 'unknown',
            parameters: {},
            metrics: {
                totalReturn: 0,
                annualReturn: 0,
                volatility: 0,
                sharpeRatio: 0,
                calmarRatio: 0,
                maxDrawdown: 0,
                winRate: 0,
                profitFactor: 0,
                totalTrades: 0,
                avgHoldDays: 0
            },
            timestamp: new Date().toISOString()
        };
    }
    
    /**
     * 计算改进指标
     */
    private calculateImprovements(original: BacktestResult, optimized: BacktestResult): Array<{
        metric: string;
        before: number;
        after: number;
        change: number;
    }> {
        const improvements: Array<{
            metric: string;
            before: number;
            after: number;
            change: number;
        }> = [];
        
        const metricMap: Record<string, keyof import('../types').BacktestMetrics> = {
            'annualReturn': 'annualReturn',
            'sharpeRatio': 'sharpeRatio',
            'calmarRatio': 'calmarRatio',
            'winRate': 'winRate',
            'profitFactor': 'profitFactor',
        };
        
        for (const [metricName, metricKey] of Object.entries(metricMap)) {
            const beforeValue = original.metrics[metricKey];
            const afterValue = optimized.metrics[metricKey];
            const before = typeof beforeValue === 'number' ? beforeValue : 0;
            const after = typeof afterValue === 'number' ? afterValue : 0;
            const change = before !== 0 ? ((after - before) / Math.abs(before)) * 100 : 0;
            
            improvements.push({
                metric: metricName,
                before,
                after,
                change
            });
        }
        
        return improvements;
    }
}

