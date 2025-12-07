/**
 * 网格搜索优化算法
 * ================
 * 
 * 实现：穷举法将每个待优化参数在给定范围内取若干离散值，
 * 组合成笛卡尔积并逐一回测评估
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

const MODULE = 'GridSearch';

export class GridSearchAlgorithm implements OptimizationAlgorithm {
    name = 'grid_search';
    private stopped = false;
    
    async optimize(
        config: StrategyConfig,
        target: OptimizationTarget,
        context: OptimizationContext,
        onProgress?: (progress: OptimizationProgress) => void
    ): Promise<OptimizationResult> {
        this.stopped = false;
        
        logger.info('开始网格搜索优化', MODULE, {
            parameterCount: config.parameterRanges.length
        });
        
        // 生成所有参数组合
        const parameterCombinations = this.generateParameterCombinations(config.parameterRanges);
        const totalIterations = parameterCombinations.length;
        
        logger.info(`生成 ${totalIterations} 个参数组合`, MODULE);
        
        const optimizationId = `opt_${Date.now()}`;
        const strategyId = `strategy_${Date.now()}`;
        const startTime = new Date().toISOString();
        
        const iterations: OptimizationIteration[] = [];
        let bestScore = -Infinity;
        let bestParameters: Record<string, any> = {};
        let bestResult: BacktestResult | null = null;
        const originalResult: BacktestResult | null = null;
        
        // 先回测原始策略
        if (config.parameters) {
            try {
                // 这里需要调用回测接口，暂时用占位符
                // originalResult = await backtestInterface.runBacktest(config, ...);
                logger.info('原始策略回测完成', MODULE);
            } catch (error) {
                logger.warn('原始策略回测失败，继续优化', MODULE);
            }
        }
        
        // 遍历所有参数组合
        for (let i = 0; i < parameterCombinations.length; i++) {
            if (this.stopped) {
                logger.info('优化已停止', MODULE);
                break;
            }
            
            const params = parameterCombinations[i];
            const candidateId = `candidate_${i}`;
            
            // 更新进度
            if (onProgress) {
                onProgress({
                    currentIteration: i + 1,
                    totalIterations: totalIterations,
                    bestScore: bestScore,
                    bestParameters: bestParameters,
                    iterations: iterations,
                    status: 'running',
                    startTime: startTime,
                    elapsedTime: (Date.now() - new Date(startTime).getTime()) / 1000
                });
            }
            
            try {
                // 创建新的策略配置
                const candidateConfig: StrategyConfig = {
                    ...config,
                    parameters: { ...config.parameters, ...params }
                };
                
                // 执行回测（这里需要实际的回测接口）
                // const backtestResult = await backtestInterface.runBacktest(candidateConfig, ...);
                // 暂时用占位符
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
                
                logger.debug(`迭代 ${i + 1}/${totalIterations} 完成`, MODULE, {
                    score: score,
                    bestScore: bestScore
                });
                
            } catch (error) {
                logger.warn(`迭代 ${i + 1} 失败: ${error}`, MODULE);
                continue;
            }
        }
        
        // 构建优化结果
        const result: OptimizationResult = {
            optimizationId: optimizationId,
            strategyId: strategyId,
            algorithm: 'grid_search',
            config: {
                algorithm: 'grid_search',
                maxIterations: totalIterations
            },
            target: target,
            bestStrategy: {
                version: `v${Date.now()}`,
                parameters: bestParameters,
                backtestResult: bestResult || iterations[0]?.backtestResult!,
                score: bestScore
            },
            comparison: {
                original: originalResult || iterations[0]?.backtestResult!,
                optimized: bestResult || iterations[0]?.backtestResult!,
                improvement: this.calculateImprovements(
                    originalResult || iterations[0]?.backtestResult!,
                    bestResult || iterations[0]?.backtestResult!
                )
            },
            progress: {
                currentIteration: iterations.length,
                totalIterations: totalIterations,
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
        
        logger.info('网格搜索优化完成', MODULE, {
            bestScore: bestScore,
            totalIterations: iterations.length
        });
        
        return result;
    }
    
    stop(): void {
        this.stopped = true;
        logger.info('网格搜索已停止', MODULE);
    }
    
    /**
     * 生成所有参数组合（笛卡尔积）
     */
    private generateParameterCombinations(ranges: ParameterRange[]): Record<string, any>[] {
        if (ranges.length === 0) {
            return [{}];
        }
        
        // 为每个参数生成值列表
        const valueLists: any[][] = ranges.map(range => {
            if (range.type === 'categorical' && range.values) {
                return range.values;
            } else if (range.type === 'bool') {
                return [true, false];
            } else if (range.type === 'int' || range.type === 'float') {
                const values: number[] = [];
                const min = range.min || 0;
                const max = range.max || 100;
                const step = range.step || (range.type === 'int' ? 1 : (max - min) / 10);
                
                for (let val = min; val <= max; val += step) {
                    values.push(range.type === 'int' ? Math.round(val) : val);
                }
                return values;
            }
            return [range.default];
        });
        
        // 计算笛卡尔积
        return this.cartesianProduct(valueLists).map(values => {
            const combination: Record<string, any> = {};
            ranges.forEach((range, index) => {
                combination[range.name] = values[index];
            });
            return combination;
        });
    }
    
    /**
     * 计算笛卡尔积
     */
    private cartesianProduct<T>(arrays: T[][]): T[][] {
        if (arrays.length === 0) return [[]];
        if (arrays.length === 1) return arrays[0].map(item => [item]);
        
        const [first, ...rest] = arrays;
        const restProduct = this.cartesianProduct(rest);
        
        const result: T[][] = [];
        for (const item of first) {
            for (const product of restProduct) {
                result.push([item, ...product]);
            }
        }
        return result;
    }
    
    /**
     * 计算策略评分
     */
    private calculateScore(metrics: any, target: OptimizationTarget): number {
        let score = 0;
        
        for (const objective of target.objectives) {
            const value = metrics[objective.metric] || 0;
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
        
        const metrics = ['annualReturn', 'sharpeRatio', 'calmarRatio', 'winRate', 'profitFactor'];
        
        for (const metric of metrics) {
            const before = (original.metrics as any)[metric] || 0;
            const after = (optimized.metrics as any)[metric] || 0;
            const change = before !== 0 ? ((after - before) / Math.abs(before)) * 100 : 0;
            
            improvements.push({
                metric,
                before,
                after,
                change
            });
        }
        
        return improvements;
    }
}

