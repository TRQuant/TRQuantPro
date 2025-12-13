/**
 * 结果分析器实现
 * ==============
 * 
 * 收集每次回测的关键绩效指标，将不同方案结果进行对比分析
 */

import { ResultAnalyzer } from '../interfaces';
import { BacktestResult, OptimizationResult } from '../types';
import { logger } from '../../../../utils/logger';

const MODULE = 'ResultAnalyzer';

export class ResultAnalyzerImpl implements ResultAnalyzer {
    analyze(result: BacktestResult): {
        strengths: string[];
        weaknesses: string[];
        risks: string[];
        suggestions: string[];
    } {
        const m = result.metrics;
        const strengths: string[] = [];
        const weaknesses: string[] = [];
        const risks: string[] = [];
        const suggestions: string[] = [];
        
        // 分析收益指标
        if (m.annualReturn > 0.15) {
            strengths.push(`年化收益率较高: ${(m.annualReturn * 100).toFixed(2)}%`);
        } else if (m.annualReturn < 0.05) {
            weaknesses.push(`年化收益率较低: ${(m.annualReturn * 100).toFixed(2)}%`);
            suggestions.push('考虑调整选股逻辑或增加因子权重');
        }
        
        // 分析风险指标
        if (m.sharpeRatio > 1.5) {
            strengths.push(`夏普比率良好: ${m.sharpeRatio.toFixed(2)}`);
        } else if (m.sharpeRatio < 0.5) {
            weaknesses.push(`夏普比率偏低: ${m.sharpeRatio.toFixed(2)}`);
            suggestions.push('考虑降低波动率或提高收益稳定性');
        }
        
        if (m.maxDrawdown < 0.15) {
            strengths.push(`最大回撤控制良好: ${(m.maxDrawdown * 100).toFixed(2)}%`);
        } else if (m.maxDrawdown > 0.3) {
            risks.push(`最大回撤较大: ${(m.maxDrawdown * 100).toFixed(2)}%`);
            suggestions.push('建议增加止损机制或降低仓位');
        }
        
        // 分析交易指标
        if (m.winRate > 0.5) {
            strengths.push(`胜率较高: ${(m.winRate * 100).toFixed(2)}%`);
        } else if (m.winRate < 0.4) {
            weaknesses.push(`胜率偏低: ${(m.winRate * 100).toFixed(2)}%`);
            suggestions.push('考虑优化入场时机或增加过滤条件');
        }
        
        if (m.totalTrades < 10) {
            weaknesses.push(`交易次数过少: ${m.totalTrades}`);
            suggestions.push('策略可能过于保守，考虑放宽选股条件');
        } else if (m.totalTrades > 500) {
            risks.push(`交易频率过高: ${m.totalTrades}，可能产生过多手续费`);
            suggestions.push('考虑增加交易过滤条件，降低换手率');
        }
        
        return { strengths, weaknesses, risks, suggestions };
    }
    
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
    } {
        const improvements: Array<{
            metric: string;
            change: number;
            percentage: number;
        }> = [];
        const regressions: Array<{
            metric: string;
            change: number;
            percentage: number;
        }> = [];
        
        const metrics = ['annualReturn', 'sharpeRatio', 'calmarRatio', 'winRate', 'profitFactor'];
        const metricNames: Record<string, string> = {
            annualReturn: '年化收益率',
            sharpeRatio: '夏普比率',
            calmarRatio: '卡玛比率',
            winRate: '胜率',
            profitFactor: '盈亏比'
        };
        
        for (const metric of metrics) {
            const v1 = (result1.metrics as any)[metric] || 0;
            const v2 = (result2.metrics as any)[metric] || 0;
            const change = v2 - v1;
            const percentage = v1 !== 0 ? (change / Math.abs(v1)) * 100 : 0;
            
            if (change > 0) {
                improvements.push({
                    metric: metricNames[metric] || metric,
                    change: change,
                    percentage: percentage
                });
            } else if (change < 0) {
                regressions.push({
                    metric: metricNames[metric] || metric,
                    change: change,
                    percentage: percentage
                });
            }
        }
        
        const summary = `优化后策略在 ${improvements.length} 个指标上有所提升，在 ${regressions.length} 个指标上有所下降。`;
        
        return { improvements, regressions, summary };
    }
    
    generateReport(optimizationResult: OptimizationResult): string {
        const { bestStrategy, comparison, progress } = optimizationResult;
        
        let report = `# 策略优化报告\n\n`;
        report += `## 基本信息\n\n`;
        report += `- 优化ID: ${optimizationResult.optimizationId}\n`;
        report += `- 算法: ${optimizationResult.algorithm}\n`;
        report += `- 优化时间: ${optimizationResult.timestamp}\n`;
        report += `- 总迭代次数: ${progress.iterations.length}\n\n`;
        
        report += `## 最佳策略\n\n`;
        report += `- 版本: ${bestStrategy.version}\n`;
        report += `- 评分: ${bestStrategy.score.toFixed(4)}\n`;
        report += `- 参数: ${JSON.stringify(bestStrategy.parameters, null, 2)}\n\n`;
        
        report += `## 性能对比\n\n`;
        report += `| 指标 | 优化前 | 优化后 | 变化 |\n`;
        report += `|------|--------|--------|------|\n`;
        
        for (const imp of comparison.improvement) {
            report += `| ${imp.metric} | ${imp.before.toFixed(4)} | ${imp.after.toFixed(4)} | ${imp.change > 0 ? '+' : ''}${imp.change.toFixed(2)}% |\n`;
        }
        
        report += `\n## 优化过程\n\n`;
        report += `- 总迭代: ${progress.iterations.length}\n`;
        report += `- 最佳评分: ${progress.bestScore.toFixed(4)}\n`;
        report += `- 耗时: ${(progress.elapsedTime || 0).toFixed(2)} 秒\n\n`;
        
        return report;
    }
}

