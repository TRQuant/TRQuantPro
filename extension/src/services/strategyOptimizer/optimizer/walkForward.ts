/**
 * Walk-Forward 分析
 * ==================
 * 
 * 防过拟合机制，通过滚动窗口验证策略稳定性：
 * - 训练集/测试集分割
 * - 滚动窗口优化
 * - 样本外验证
 * - 稳健性评估
 */

import { logger } from '../../../utils/logger';
import { BacktestResult, StrategyConfig, OptimizationTarget } from './types';
import { BacktestInterface, OptimizationAlgorithm } from './interfaces';

const MODULE = 'WalkForward';

/** Walk-Forward 配置 */
export interface WalkForwardConfig {
    /** 训练窗口大小（交易日） */
    trainingWindow: number;
    /** 测试窗口大小（交易日） */
    testingWindow: number;
    /** 滚动步长（交易日） */
    stepSize: number;
    /** 最小训练数据量（交易日） */
    minTrainingDays: number;
    /** 是否使用扩展窗口（累积训练数据） */
    expandingWindow: boolean;
}

/** Walk-Forward 周期结果 */
export interface WalkForwardPeriodResult {
    periodIndex: number;
    trainingStart: string;
    trainingEnd: string;
    testingStart: string;
    testingEnd: string;
    optimizedParameters: Record<string, any>;
    trainingMetrics: BacktestResult['metrics'];
    testingMetrics: BacktestResult['metrics'];
    outOfSampleReturn: number;
}

/** Walk-Forward 分析结果 */
export interface WalkForwardResult {
    /** 总周期数 */
    totalPeriods: number;
    /** 各周期结果 */
    periodResults: WalkForwardPeriodResult[];
    /** 样本外综合表现 */
    aggregatedMetrics: {
        totalReturn: number;
        annualizedReturn: number;
        sharpeRatio: number;
        maxDrawdown: number;
        winRate: number;
        profitablePeriods: number;
    };
    /** 稳健性指标 */
    robustnessMetrics: {
        /** 样本内外收益比 */
        isOosRatio: number;
        /** 参数稳定性（参数变化标准差） */
        parameterStability: Record<string, number>;
        /** 周期一致性（正收益周期占比） */
        periodConsistency: number;
        /** 综合稳健性评分 */
        robustnessScore: number;
    };
    /** 诊断信息 */
    diagnostics: {
        overfittingRisk: 'low' | 'medium' | 'high';
        warnings: string[];
        recommendations: string[];
    };
}

/**
 * Walk-Forward 分析器
 */
export class WalkForwardAnalyzer {
    private backtestInterface: BacktestInterface;
    private optimizer: OptimizationAlgorithm;
    
    constructor(
        backtestInterface: BacktestInterface,
        optimizer: OptimizationAlgorithm
    ) {
        this.backtestInterface = backtestInterface;
        this.optimizer = optimizer;
    }
    
    /**
     * 执行 Walk-Forward 分析
     */
    async analyze(
        strategy: StrategyConfig,
        target: OptimizationTarget,
        config: WalkForwardConfig,
        dateRange: { start: string; end: string },
        onProgress?: (progress: { period: number; total: number; status: string }) => void
    ): Promise<WalkForwardResult> {
        logger.info('开始 Walk-Forward 分析', MODULE, {
            trainingWindow: config.trainingWindow,
            testingWindow: config.testingWindow
        });
        
        // 生成时间窗口
        const periods = this.generatePeriods(dateRange, config);
        logger.info(`生成 ${periods.length} 个分析周期`, MODULE);
        
        const periodResults: WalkForwardPeriodResult[] = [];
        
        // 遍历每个周期
        for (let i = 0; i < periods.length; i++) {
            const period = periods[i];
            
            if (onProgress) {
                onProgress({
                    period: i + 1,
                    total: periods.length,
                    status: `分析周期 ${i + 1}/${periods.length}`
                });
            }
            
            try {
                // 1. 在训练集上优化参数
                const optimizationResult = await this.optimizeOnTraining(
                    strategy,
                    target,
                    period.trainingStart,
                    period.trainingEnd
                );
                
                // 2. 在测试集上验证
                const testResult = await this.validateOnTesting(
                    strategy,
                    optimizationResult.parameters,
                    period.testingStart,
                    period.testingEnd
                );
                
                periodResults.push({
                    periodIndex: i,
                    trainingStart: period.trainingStart,
                    trainingEnd: period.trainingEnd,
                    testingStart: period.testingStart,
                    testingEnd: period.testingEnd,
                    optimizedParameters: optimizationResult.parameters,
                    trainingMetrics: optimizationResult.metrics,
                    testingMetrics: testResult.metrics,
                    outOfSampleReturn: testResult.metrics.totalReturn
                });
                
            } catch (error) {
                logger.warn(`周期 ${i + 1} 分析失败: ${error}`, MODULE);
            }
        }
        
        // 计算综合指标
        const aggregatedMetrics = this.calculateAggregatedMetrics(periodResults);
        const robustnessMetrics = this.calculateRobustnessMetrics(periodResults, strategy);
        const diagnostics = this.generateDiagnostics(periodResults, robustnessMetrics);
        
        return {
            totalPeriods: periods.length,
            periodResults,
            aggregatedMetrics,
            robustnessMetrics,
            diagnostics
        };
    }
    
    /**
     * 生成时间周期
     */
    private generatePeriods(
        dateRange: { start: string; end: string },
        config: WalkForwardConfig
    ): Array<{
        trainingStart: string;
        trainingEnd: string;
        testingStart: string;
        testingEnd: string;
    }> {
        const periods: Array<{
            trainingStart: string;
            trainingEnd: string;
            testingStart: string;
            testingEnd: string;
        }> = [];
        
        const startDate = new Date(dateRange.start);
        const endDate = new Date(dateRange.end);
        
        // 计算需要的总天数
        const totalDays = Math.floor((endDate.getTime() - startDate.getTime()) / (24 * 60 * 60 * 1000));
        const minDays = config.trainingWindow + config.testingWindow;
        
        if (totalDays < minDays) {
            logger.warn(`数据范围不足: 需要至少 ${minDays} 天`, MODULE);
            return periods;
        }
        
        let currentStart = new Date(startDate);
        
        while (true) {
            // 训练期
            const trainingStart = new Date(currentStart);
            const trainingEnd = new Date(trainingStart);
            trainingEnd.setDate(trainingEnd.getDate() + config.trainingWindow);
            
            // 测试期
            const testingStart = new Date(trainingEnd);
            testingStart.setDate(testingStart.getDate() + 1);
            const testingEnd = new Date(testingStart);
            testingEnd.setDate(testingEnd.getDate() + config.testingWindow);
            
            // 检查是否超出范围
            if (testingEnd > endDate) {
                break;
            }
            
            periods.push({
                trainingStart: this.formatDate(trainingStart),
                trainingEnd: this.formatDate(trainingEnd),
                testingStart: this.formatDate(testingStart),
                testingEnd: this.formatDate(testingEnd)
            });
            
            // 移动窗口
            if (config.expandingWindow) {
                // 扩展窗口：训练起点不变，只移动测试期
                currentStart = new Date(trainingStart);
                config.trainingWindow += config.stepSize;
            } else {
                // 滚动窗口
                currentStart.setDate(currentStart.getDate() + config.stepSize);
            }
        }
        
        return periods;
    }
    
    /**
     * 在训练集上优化参数
     */
    private async optimizeOnTraining(
        strategy: StrategyConfig,
        target: OptimizationTarget,
        startDate: string,
        endDate: string
    ): Promise<{
        parameters: Record<string, any>;
        metrics: BacktestResult['metrics'];
    }> {
        // 克隆策略配置（日期范围在回测时传入）
        const trainingStrategy: StrategyConfig = {
            ...strategy
        };
        
        // 存储日期范围到固定参数中，供回测时使用
        trainingStrategy.fixedParameters = {
            ...strategy.fixedParameters,
            __startDate: startDate,
            __endDate: endDate
        };
        
        // 设置回测接口给算法
        if ((this.optimizer as any).setBacktestInterface) {
            (this.optimizer as any).setBacktestInterface(this.backtestInterface);
        }
        
        // 执行优化
        const result = await this.optimizer.optimize(
            trainingStrategy,
            target,
            { marketContext: { regime: 'neutral', timestamp: new Date().toISOString() } },
            undefined
        );
        
        return {
            parameters: result.bestStrategy.parameters,
            metrics: result.bestStrategy.backtestResult.metrics
        };
    }
    
    /**
     * 在测试集上验证
     */
    private async validateOnTesting(
        strategy: StrategyConfig,
        parameters: Record<string, any>,
        startDate: string,
        endDate: string
    ): Promise<BacktestResult> {
        // 用优化后的参数运行回测
        const testStrategy: StrategyConfig = {
            ...strategy,
            parameters
        };
        
        return await this.backtestInterface.runBacktest(testStrategy, {
            startDate,
            endDate,
            initialCapital: 1000000,
            commission: 0.0003
        });
    }
    
    /**
     * 计算综合指标
     */
    private calculateAggregatedMetrics(
        periodResults: WalkForwardPeriodResult[]
    ): WalkForwardResult['aggregatedMetrics'] {
        if (periodResults.length === 0) {
            return {
                totalReturn: 0,
                annualizedReturn: 0,
                sharpeRatio: 0,
                maxDrawdown: 0,
                winRate: 0,
                profitablePeriods: 0
            };
        }
        
        // 累计收益（复利）
        let cumulativeReturn = 1;
        let maxDrawdown = 0;
        let currentPeak = 1;
        let profitablePeriods = 0;
        const returns: number[] = [];
        
        for (const result of periodResults) {
            const periodReturn = result.outOfSampleReturn;
            returns.push(periodReturn);
            
            cumulativeReturn *= (1 + periodReturn);
            
            if (cumulativeReturn > currentPeak) {
                currentPeak = cumulativeReturn;
            }
            const drawdown = (currentPeak - cumulativeReturn) / currentPeak;
            if (drawdown > maxDrawdown) {
                maxDrawdown = drawdown;
            }
            
            if (periodReturn > 0) {
                profitablePeriods++;
            }
        }
        
        const totalReturn = cumulativeReturn - 1;
        
        // 年化收益（假设每个周期30天）
        const totalDays = periodResults.length * 30;
        const annualizedReturn = Math.pow(1 + totalReturn, 365 / totalDays) - 1;
        
        // 夏普比率
        const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
        const stdReturn = Math.sqrt(
            returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length
        );
        const sharpeRatio = stdReturn > 0 ? (avgReturn * 12) / (stdReturn * Math.sqrt(12)) : 0;
        
        // 胜率
        const winRate = profitablePeriods / periodResults.length;
        
        return {
            totalReturn,
            annualizedReturn,
            sharpeRatio,
            maxDrawdown,
            winRate,
            profitablePeriods
        };
    }
    
    /**
     * 计算稳健性指标
     */
    private calculateRobustnessMetrics(
        periodResults: WalkForwardPeriodResult[],
        strategy: StrategyConfig
    ): WalkForwardResult['robustnessMetrics'] {
        if (periodResults.length === 0) {
            return {
                isOosRatio: 0,
                parameterStability: {},
                periodConsistency: 0,
                robustnessScore: 0
            };
        }
        
        // 样本内外收益比
        const avgIsReturn = periodResults.reduce((sum, r) => sum + r.trainingMetrics.totalReturn, 0) / periodResults.length;
        const avgOosReturn = periodResults.reduce((sum, r) => sum + r.outOfSampleReturn, 0) / periodResults.length;
        const isOosRatio = avgIsReturn !== 0 ? avgOosReturn / avgIsReturn : 0;
        
        // 参数稳定性
        const parameterStability: Record<string, number> = {};
        if (strategy.parameterRanges) {
            for (const range of strategy.parameterRanges) {
                const values = periodResults.map(r => r.optimizedParameters[range.name] || 0);
                const mean = values.reduce((a, b) => a + b, 0) / values.length;
                const std = Math.sqrt(
                    values.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / values.length
                );
                // 归一化标准差
                const rangeMax = range.max ?? 0;
                const rangeMin = range.min ?? 0;
                const range_size = rangeMax - rangeMin;
                parameterStability[range.name] = range_size > 0 ? std / range_size : 0;
            }
        }
        
        // 周期一致性
        const profitablePeriods = periodResults.filter(r => r.outOfSampleReturn > 0).length;
        const periodConsistency = profitablePeriods / periodResults.length;
        
        // 综合稳健性评分
        const avgParamStability = Object.values(parameterStability).length > 0
            ? Object.values(parameterStability).reduce((a, b) => a + b, 0) / Object.values(parameterStability).length
            : 0;
        
        // 评分公式：样本外表现权重40%，参数稳定性30%，周期一致性30%
        let robustnessScore = 0;
        
        // 样本内外比（理想值接近1）
        const oosScore = Math.max(0, Math.min(100, isOosRatio * 100));
        robustnessScore += oosScore * 0.4;
        
        // 参数稳定性（值越小越好）
        const stabilityScore = Math.max(0, (1 - avgParamStability) * 100);
        robustnessScore += stabilityScore * 0.3;
        
        // 周期一致性
        robustnessScore += periodConsistency * 100 * 0.3;
        
        return {
            isOosRatio,
            parameterStability,
            periodConsistency,
            robustnessScore: Math.round(robustnessScore)
        };
    }
    
    /**
     * 生成诊断信息
     */
    private generateDiagnostics(
        periodResults: WalkForwardPeriodResult[],
        robustnessMetrics: WalkForwardResult['robustnessMetrics']
    ): WalkForwardResult['diagnostics'] {
        const warnings: string[] = [];
        const recommendations: string[] = [];
        
        // 判断过拟合风险
        let overfittingRisk: 'low' | 'medium' | 'high' = 'low';
        
        // 样本内外差异大
        if (robustnessMetrics.isOosRatio < 0.5) {
            overfittingRisk = 'high';
            warnings.push('样本外收益显著低于样本内，存在过拟合风险');
            recommendations.push('考虑减少参数数量或缩小参数范围');
        } else if (robustnessMetrics.isOosRatio < 0.7) {
            overfittingRisk = 'medium';
            warnings.push('样本外收益明显低于样本内');
            recommendations.push('建议增加训练数据量或简化策略');
        }
        
        // 参数不稳定
        const unstableParams = Object.entries(robustnessMetrics.parameterStability)
            .filter(([_, stability]) => stability > 0.3)
            .map(([name, _]) => name);
        
        if (unstableParams.length > 0) {
            if (overfittingRisk === 'low') overfittingRisk = 'medium';
            warnings.push(`参数不稳定: ${unstableParams.join(', ')}`);
            recommendations.push('考虑固定这些参数或缩小其范围');
        }
        
        // 周期一致性低
        if (robustnessMetrics.periodConsistency < 0.5) {
            if (overfittingRisk !== 'high') overfittingRisk = 'medium';
            warnings.push('策略在不同周期表现不一致');
            recommendations.push('策略可能对特定市场环境敏感，建议添加市场状态过滤');
        }
        
        // 正面反馈
        if (robustnessMetrics.robustnessScore >= 70) {
            recommendations.push('策略稳健性良好，可考虑实盘测试');
        }
        
        if (periodResults.length < 5) {
            warnings.push('分析周期较少，结果可能不够可靠');
            recommendations.push('建议使用更长的历史数据进行验证');
        }
        
        return {
            overfittingRisk,
            warnings,
            recommendations
        };
    }
    
    /**
     * 格式化日期
     */
    private formatDate(date: Date): string {
        return date.toISOString().split('T')[0];
    }
}

/**
 * 创建 Walk-Forward 分析器
 */
export function createWalkForwardAnalyzer(
    backtestInterface: BacktestInterface,
    optimizer: OptimizationAlgorithm
): WalkForwardAnalyzer {
    return new WalkForwardAnalyzer(backtestInterface, optimizer);
}

/**
 * 默认 Walk-Forward 配置
 */
export const DEFAULT_WALK_FORWARD_CONFIG: WalkForwardConfig = {
    trainingWindow: 252,  // 1年
    testingWindow: 63,    // 1季度
    stepSize: 63,         // 每季度滚动
    minTrainingDays: 126, // 最少半年
    expandingWindow: false
};

