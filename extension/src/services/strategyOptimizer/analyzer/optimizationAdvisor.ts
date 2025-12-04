/**
 * 优化建议生成器
 * ===============
 * 
 * 基于策略分析结果和知识库，生成具体的优化建议
 * 
 * 优化维度：
 * 1. 风险控制优化
 * 2. 因子组合优化
 * 3. 选股逻辑优化
 * 4. 代码结构优化
 */

import { logger } from '../../../utils/logger';
import { StrategyAnalysis, StrategyIssue } from './strategyAnalyzer';
import { KnowledgeStore } from '../learner/knowledgeStore';
import { BestPractice } from '../types';

const MODULE = 'OptimizationAdvisor';

/** 优化建议 */
export interface OptimizationAdvice {
    id: string;
    category: 'risk' | 'factor' | 'selection' | 'code' | 'performance';
    priority: 'high' | 'medium' | 'low';
    title: string;
    description: string;
    currentState?: string;     // 当前状态
    suggestedState?: string;   // 建议状态
    codeExample?: string;      // 代码示例
    source?: string;           // 知识来源
    impact: string;            // 预期影响
}

/** 优化报告 */
export interface OptimizationReport {
    strategyName: string;
    platform: string;
    analysisTime: string;
    overallScore: number;      // 0-100
    scoreBreakdown: {
        risk: number;
        factor: number;
        selection: number;
        code: number;
    };
    advices: OptimizationAdvice[];
    summary: string;
}

/**
 * 优化建议生成器
 */
export class OptimizationAdvisor {
    private knowledgeStore: KnowledgeStore | null = null;
    
    constructor(knowledgeStore?: KnowledgeStore) {
        this.knowledgeStore = knowledgeStore || null;
    }
    
    /**
     * 设置知识库
     */
    setKnowledgeStore(store: KnowledgeStore): void {
        this.knowledgeStore = store;
    }
    
    /**
     * 生成优化报告
     */
    generateReport(analysis: StrategyAnalysis): OptimizationReport {
        logger.info(`生成优化报告: ${analysis.name}`, MODULE);
        
        const advices: OptimizationAdvice[] = [];
        
        // 1. 风控优化建议
        advices.push(...this.generateRiskAdvices(analysis));
        
        // 2. 因子优化建议
        advices.push(...this.generateFactorAdvices(analysis));
        
        // 3. 选股优化建议
        advices.push(...this.generateSelectionAdvices(analysis));
        
        // 4. 代码优化建议
        advices.push(...this.generateCodeAdvices(analysis));
        
        // 5. 从知识库获取额外建议
        if (this.knowledgeStore) {
            advices.push(...this.getKnowledgeBasedAdvices(analysis));
        }
        
        // 计算评分
        const scores = this.calculateScores(analysis, advices);
        
        // 生成摘要
        const summary = this.generateSummary(analysis, scores, advices);
        
        return {
            strategyName: analysis.name,
            platform: analysis.platform,
            analysisTime: new Date().toISOString(),
            overallScore: scores.overall,
            scoreBreakdown: {
                risk: scores.risk,
                factor: scores.factor,
                selection: scores.selection,
                code: scores.code,
            },
            advices: advices.sort((a, b) => {
                const priorityOrder = { high: 0, medium: 1, low: 2 };
                return priorityOrder[a.priority] - priorityOrder[b.priority];
            }),
            summary,
        };
    }
    
    /**
     * 风控优化建议
     */
    private generateRiskAdvices(analysis: StrategyAnalysis): OptimizationAdvice[] {
        const advices: OptimizationAdvice[] = [];
        const risk = analysis.riskControl;
        
        // 止损建议
        if (!risk.stopLoss) {
            advices.push({
                id: 'risk_stop_loss',
                category: 'risk',
                priority: 'high',
                title: '添加止损机制',
                description: '策略缺少止损设置，在市场大幅下跌时可能造成重大损失',
                suggestedState: '止损线 8%',
                codeExample: `# 止损设置
STOP_LOSS = 0.08  # 8%止损

def check_stop_loss(context, stock):
    cost = context.portfolio.positions[stock].avg_cost
    price = context.portfolio.positions[stock].price
    if (cost - price) / cost >= STOP_LOSS:
        order_target(stock, 0)
        log.info(f'{stock} 触发止损')`,
                impact: '显著降低最大回撤',
                source: 'A股实操手册-风控篇',
            });
        } else if (risk.stopLoss > 0.15) {
            advices.push({
                id: 'risk_stop_loss_tight',
                category: 'risk',
                priority: 'medium',
                title: '收紧止损线',
                description: `当前止损线 ${(risk.stopLoss * 100).toFixed(0)}% 过于宽松`,
                currentState: `${(risk.stopLoss * 100).toFixed(0)}%`,
                suggestedState: '8-12%',
                impact: '减少单次交易损失',
            });
        }
        
        // 止盈建议
        if (!risk.takeProfit) {
            advices.push({
                id: 'risk_take_profit',
                category: 'risk',
                priority: 'medium',
                title: '添加止盈机制',
                description: '建议设置动态止盈，锁定利润',
                suggestedState: '止盈线 20-30%',
                codeExample: `# 止盈设置
TAKE_PROFIT = 0.20  # 20%止盈

def check_take_profit(context, stock):
    cost = context.portfolio.positions[stock].avg_cost
    price = context.portfolio.positions[stock].price
    if (price - cost) / cost >= TAKE_PROFIT:
        order_target(stock, 0)
        log.info(f'{stock} 触发止盈')`,
                impact: '锁定收益，避免利润回吐',
            });
        }
        
        // 仓位控制
        if (!risk.maxPosition) {
            advices.push({
                id: 'risk_position',
                category: 'risk',
                priority: 'medium',
                title: '设置仓位上限',
                description: '建议设置最大仓位控制，保留现金应对风险',
                suggestedState: '最大仓位 80%',
                codeExample: `MAX_POSITION = 0.8  # 最大仓位80%`,
                impact: '保留流动性，便于抄底',
            });
        }
        
        // 回撤控制
        if (!risk.hasDrawdownControl) {
            advices.push({
                id: 'risk_drawdown',
                category: 'risk',
                priority: 'low',
                title: '添加回撤控制',
                description: '建议监控组合回撤，触发阈值时降低仓位',
                suggestedState: '回撤超15%减仓50%',
                impact: '控制组合级别风险',
            });
        }
        
        return advices;
    }
    
    /**
     * 因子优化建议
     */
    private generateFactorAdvices(analysis: StrategyAnalysis): OptimizationAdvice[] {
        const advices: OptimizationAdvice[] = [];
        const factors = analysis.factors;
        
        if (factors.length === 0) {
            advices.push({
                id: 'factor_missing',
                category: 'factor',
                priority: 'high',
                title: '添加量化因子',
                description: '策略缺少明确的量化因子，建议使用因子选股',
                suggestedState: '多因子组合',
                codeExample: `# 推荐因子组合
factors = {
    'momentum': 0.3,    # 动量因子
    'value': 0.3,       # 价值因子
    'quality': 0.2,     # 质量因子
    'volatility': 0.2,  # 低波因子
}`,
                impact: '提高选股的科学性和稳定性',
                source: 'A股实操手册-因子篇',
            });
        } else if (factors.length === 1) {
            advices.push({
                id: 'factor_single',
                category: 'factor',
                priority: 'medium',
                title: '增加因子多样性',
                description: `当前仅使用 ${factors[0].name}，建议组合多因子`,
                currentState: factors[0].name,
                suggestedState: '3-5个低相关因子',
                impact: '降低单因子失效风险，提高稳定性',
            });
        }
        
        // 检查因子类型分布
        const typeCount: Record<string, number> = {};
        for (const f of factors) {
            typeCount[f.type] = (typeCount[f.type] || 0) + 1;
        }
        
        if (factors.length >= 2 && Object.keys(typeCount).length === 1) {
            advices.push({
                id: 'factor_diversity',
                category: 'factor',
                priority: 'medium',
                title: '增加因子类型多样性',
                description: '当前因子类型单一，建议混合不同类型因子',
                currentState: `全部为${factors[0].type}类型`,
                suggestedState: '动量+价值+质量组合',
                impact: '因子互补，适应不同市场环境',
            });
        }
        
        return advices;
    }
    
    /**
     * 选股优化建议
     */
    private generateSelectionAdvices(analysis: StrategyAnalysis): OptimizationAdvice[] {
        const advices: OptimizationAdvice[] = [];
        const selection = analysis.stockSelection;
        
        // 股票池建议
        if (selection.universe === '未知' || selection.universe === '全市场') {
            advices.push({
                id: 'selection_universe',
                category: 'selection',
                priority: 'medium',
                title: '缩小股票池范围',
                description: '全市场选股可能包含流动性差的股票',
                suggestedState: '沪深300/中证500成分股',
                impact: '提高流动性，降低冲击成本',
            });
        }
        
        // 持股数量
        if (selection.topN && selection.topN > 30) {
            advices.push({
                id: 'selection_topn_reduce',
                category: 'selection',
                priority: 'low',
                title: '减少持股数量',
                description: `当前持股${selection.topN}只，可能过于分散`,
                currentState: `${selection.topN}只`,
                suggestedState: '10-20只',
                impact: '提高选股集中度和收益弹性',
            });
        } else if (selection.topN && selection.topN < 5) {
            advices.push({
                id: 'selection_topn_increase',
                category: 'selection',
                priority: 'high',
                title: '增加持股数量',
                description: `当前持股${selection.topN}只，风险过于集中`,
                currentState: `${selection.topN}只`,
                suggestedState: '5-10只',
                impact: '分散风险，降低波动',
            });
        }
        
        // 筛选条件
        if (!selection.filters.includes('排除ST')) {
            advices.push({
                id: 'selection_filter_st',
                category: 'selection',
                priority: 'medium',
                title: '排除ST股票',
                description: '建议过滤ST/*ST股票，避免退市风险',
                codeExample: `# 排除ST股票
stocks = [s for s in stocks if not get_extras('is_st', s)]`,
                impact: '降低踩雷风险',
            });
        }
        
        return advices;
    }
    
    /**
     * 代码优化建议
     */
    private generateCodeAdvices(analysis: StrategyAnalysis): OptimizationAdvice[] {
        const advices: OptimizationAdvice[] = [];
        
        // 从issues中提取代码相关问题
        for (const issue of analysis.issues) {
            if (issue.category === 'code') {
                advices.push({
                    id: `code_${issue.message.replace(/\s+/g, '_').toLowerCase()}`,
                    category: 'code',
                    priority: issue.type === 'error' ? 'high' : 'low',
                    title: issue.message,
                    description: issue.suggestion || '',
                    impact: '代码规范性',
                });
            }
        }
        
        return advices;
    }
    
    /**
     * 从知识库获取建议
     */
    private getKnowledgeBasedAdvices(analysis: StrategyAnalysis): OptimizationAdvice[] {
        if (!this.knowledgeStore) return [];
        
        const advices: OptimizationAdvice[] = [];
        
        // 获取相关最佳实践
        const bestPractices = this.knowledgeStore.getBestPractices();
        
        for (const practice of bestPractices.slice(0, 5)) {
            // 检查策略是否已应用该实践
            const isApplied = this.checkPracticeApplied(practice, analysis);
            
            if (!isApplied) {
                advices.push({
                    id: `kb_${practice.id}`,
                    category: this.mapPracticeCategory(practice.category),
                    priority: 'medium',
                    title: practice.title,
                    description: practice.description,
                    codeExample: practice.example,
                    source: practice.references?.[0] || '知识库',
                    impact: '来自实操经验的优化建议',
                });
            }
        }
        
        return advices;
    }
    
    /**
     * 检查策略是否已应用某实践
     */
    private checkPracticeApplied(practice: BestPractice, analysis: StrategyAnalysis): boolean {
        const desc = practice.description.toLowerCase();
        
        // 简单关键词匹配
        if (desc.includes('止损') && analysis.riskControl.stopLoss) return true;
        if (desc.includes('止盈') && analysis.riskControl.takeProfit) return true;
        if (desc.includes('多因子') && analysis.factors.length >= 3) return true;
        
        return false;
    }
    
    /**
     * 映射知识库类别到建议类别
     */
    private mapPracticeCategory(category: string): OptimizationAdvice['category'] {
        const mapping: Record<string, OptimizationAdvice['category']> = {
            'risk': 'risk',
            'selection': 'selection',
            'trading': 'performance',
            'position': 'risk',
        };
        return mapping[category] || 'performance';
    }
    
    /**
     * 计算评分
     */
    private calculateScores(
        analysis: StrategyAnalysis,
        advices: OptimizationAdvice[]
    ): { overall: number; risk: number; factor: number; selection: number; code: number } {
        // 基础分
        let risk = 70, factor = 70, selection = 70, code = 80;
        
        // 风控评分
        if (analysis.riskControl.stopLoss) risk += 10;
        if (analysis.riskControl.takeProfit) risk += 5;
        if (analysis.riskControl.maxPosition) risk += 5;
        if (analysis.riskControl.hasDrawdownControl) risk += 10;
        
        // 因子评分
        factor += Math.min(analysis.factors.length * 10, 30);
        
        // 选股评分
        if (analysis.stockSelection.topN && analysis.stockSelection.topN >= 5 && analysis.stockSelection.topN <= 20) {
            selection += 10;
        }
        selection += analysis.stockSelection.filters.length * 5;
        
        // 代码评分
        const codeIssues = analysis.issues.filter(i => i.category === 'code');
        code -= codeIssues.filter(i => i.type === 'error').length * 20;
        code -= codeIssues.filter(i => i.type === 'warning').length * 5;
        
        // 根据高优先级建议扣分
        const highPriorityCount = advices.filter(a => a.priority === 'high').length;
        const deduction = highPriorityCount * 5;
        
        return {
            risk: Math.max(0, Math.min(100, risk - deduction)),
            factor: Math.max(0, Math.min(100, factor - deduction)),
            selection: Math.max(0, Math.min(100, selection - deduction)),
            code: Math.max(0, Math.min(100, code)),
            overall: Math.round((risk + factor + selection + code) / 4 - deduction),
        };
    }
    
    /**
     * 生成摘要
     */
    private generateSummary(
        analysis: StrategyAnalysis,
        scores: { overall: number; risk: number; factor: number; selection: number; code: number },
        advices: OptimizationAdvice[]
    ): string {
        const highPriority = advices.filter(a => a.priority === 'high');
        const mediumPriority = advices.filter(a => a.priority === 'medium');
        
        let summary = `策略 "${analysis.name}" 整体评分 ${scores.overall}/100。`;
        
        if (highPriority.length > 0) {
            summary += `\n\n🔴 发现 ${highPriority.length} 个高优先级问题需要优先处理：`;
            for (const a of highPriority.slice(0, 3)) {
                summary += `\n  • ${a.title}`;
            }
        }
        
        if (mediumPriority.length > 0) {
            summary += `\n\n🟡 发现 ${mediumPriority.length} 个中等优先级优化建议。`;
        }
        
        // 亮点
        const highlights: string[] = [];
        if (analysis.riskControl.stopLoss && analysis.riskControl.takeProfit) {
            highlights.push('风控完善');
        }
        if (analysis.factors.length >= 3) {
            highlights.push('多因子选股');
        }
        if (analysis.trading.hasTimingLogic) {
            highlights.push('包含择时逻辑');
        }
        
        if (highlights.length > 0) {
            summary += `\n\n✅ 策略亮点：${highlights.join('、')}`;
        }
        
        return summary;
    }
}

/** 创建优化建议生成器 */
export function createOptimizationAdvisor(knowledgeStore?: KnowledgeStore): OptimizationAdvisor {
    return new OptimizationAdvisor(knowledgeStore);
}

