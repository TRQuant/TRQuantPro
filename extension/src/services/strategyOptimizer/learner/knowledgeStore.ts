/**
 * 知识存储模块
 * ============
 * 
 * 持久化存储学习到的知识：
 * - API映射规则
 * - 策略模式
 * - 最佳实践
 * - 用户反馈
 */

import * as fs from 'fs';
import * as path from 'path';
import {
    LearningData,
    StrategyPattern,
    APIMapping,
    BestPractice,
    UserFeedback
} from '../types';

// ============================================================
// 知识存储类
// ============================================================

export class KnowledgeStore {
    private dataPath: string;
    private data: LearningData;
    private isDirty: boolean = false;
    
    constructor(storagePath: string) {
        this.dataPath = path.join(storagePath, 'knowledge.json');
        this.data = this.load();
    }
    
    /**
     * 加载知识库
     */
    private load(): LearningData {
        try {
            if (fs.existsSync(this.dataPath)) {
                const content = fs.readFileSync(this.dataPath, 'utf-8');
                return JSON.parse(content);
            }
        } catch (e) {
            console.error('[KnowledgeStore] 加载失败:', e);
        }
        
        // 返回默认数据
        return this.getDefaultData();
    }
    
    /**
     * 获取默认知识库
     */
    private getDefaultData(): LearningData {
        return {
            patterns: this.getBuiltinPatterns(),
            apiMappings: [],
            bestPractices: this.getBuiltinBestPractices(),
            userFeedback: []
        };
    }
    
    /**
     * 内置策略模式
     */
    private getBuiltinPatterns(): StrategyPattern[] {
        return [
            {
                id: 'multi_factor_selection',
                name: '多因子选股',
                category: 'selection',
                description: '基于多个量化因子对股票进行综合评分筛选',
                codeTemplate: `
def select_stocks_by_factors(stocks, factor_weights):
    """多因子选股"""
    scores = {}
    for stock in stocks:
        score = 0
        for factor, weight in factor_weights.items():
            factor_value = get_factor_value(stock, factor)
            score += factor_value * weight
        scores[stock] = score
    # 返回得分最高的股票
    return sorted(scores, key=scores.get, reverse=True)
`,
                effectiveness: 85,
                usageCount: 100
            },
            {
                id: 'momentum_timing',
                name: '动量择时',
                category: 'timing',
                description: '基于价格动量判断市场趋势',
                codeTemplate: `
def check_momentum_signal(index_code, lookback=20):
    """动量择时信号"""
    prices = get_price(index_code, count=lookback, fields=['close'])
    returns = prices['close'].pct_change(lookback-1).iloc[-1]
    
    if returns > 0.05:
        return 'bullish'
    elif returns < -0.05:
        return 'bearish'
    return 'neutral'
`,
                effectiveness: 70,
                usageCount: 80
            },
            {
                id: 'fixed_stop_loss',
                name: '固定止损',
                category: 'risk',
                description: '当亏损达到阈值时自动止损',
                codeTemplate: `
def check_stop_loss(context, stock, stop_loss_pct=-0.08):
    """固定止损检查"""
    if stock not in context.portfolio.positions:
        return False
    
    position = context.portfolio.positions[stock]
    cost = position.avg_cost
    current_price = position.price
    
    profit_pct = (current_price - cost) / cost
    return profit_pct <= stop_loss_pct
`,
                effectiveness: 90,
                usageCount: 150
            },
            {
                id: 'trailing_stop',
                name: '移动止损',
                category: 'risk',
                description: '根据最高价动态调整止损线',
                codeTemplate: `
def check_trailing_stop(context, stock, trail_pct=0.10):
    """移动止损检查"""
    if stock not in g.highest_prices:
        return False
    
    highest = g.highest_prices[stock]
    current = get_current_data()[stock].last_price
    
    # 更新最高价
    if current > highest:
        g.highest_prices[stock] = current
        return False
    
    # 检查回撤
    drawdown = (highest - current) / highest
    return drawdown >= trail_pct
`,
                effectiveness: 85,
                usageCount: 90
            },
            {
                id: 'equal_weight_execution',
                name: '等权重执行',
                category: 'execution',
                description: '对目标股票进行等权重配置',
                codeTemplate: `
def execute_equal_weight(context, target_stocks, max_position=0.10):
    """等权重执行"""
    if not target_stocks:
        return
    
    total_value = context.portfolio.total_value
    weight = min(1.0 / len(target_stocks), max_position)
    
    for stock in target_stocks:
        target_value = total_value * weight
        order_target_value(stock, target_value)
`,
                effectiveness: 80,
                usageCount: 120
            },
            {
                id: 'market_regime_position',
                name: '市场状态仓位管理',
                category: 'risk',
                description: '根据市场状态动态调整总仓位',
                codeTemplate: `
POSITION_BY_REGIME = {
    'risk_on': 0.90,   # 牛市高仓位
    'risk_off': 0.50,  # 熊市低仓位
    'neutral': 0.70,   # 震荡中仓位
}

def get_target_position(regime):
    """获取目标仓位"""
    return POSITION_BY_REGIME.get(regime, 0.70)
`,
                effectiveness: 88,
                usageCount: 85
            }
        ];
    }
    
    /**
     * 内置最佳实践
     */
    private getBuiltinBestPractices(): BestPractice[] {
        return [
            {
                id: 'bp_stop_loss',
                title: '必须设置止损',
                category: '风控',
                description: '任何策略都应该有止损机制，建议单票止损线设置在-8%左右',
                example: `
# 推荐的止损设置
STOP_LOSS = -0.08  # 8%止损
TAKE_PROFIT = 0.20  # 20%止盈

def check_risk(context, stock):
    profit = get_profit_pct(context, stock)
    if profit <= STOP_LOSS:
        order_target_value(stock, 0)
        log.warn(f'止损: {stock}')
`,
                references: ['量化投资策略与技术', 'A股量化实战']
            },
            {
                id: 'bp_position_limit',
                title: '控制单票仓位',
                category: '风控',
                description: '单票仓位不宜超过总资金的10%，避免个股风险集中',
                example: `
# 推荐的仓位控制
MAX_SINGLE_POSITION = 0.10  # 单票最大10%
MAX_TOTAL_POSITION = 0.80   # 总仓位最大80%

def calculate_position(context, stock, score):
    max_value = context.portfolio.total_value * MAX_SINGLE_POSITION
    target_value = min(calculated_value, max_value)
    return target_value
`,
                references: ['组合管理', '风险平价']
            },
            {
                id: 'bp_avoid_st',
                title: '过滤ST股票',
                category: '选股',
                description: '在选股池中排除ST、*ST股票，避免退市风险',
                example: `
def filter_st_stocks(stocks):
    """过滤ST股票"""
    current_data = get_current_data()
    return [s for s in stocks 
            if not current_data[s].is_st 
            and not current_data[s].name.startswith('ST')
            and not current_data[s].name.startswith('*ST')]
`,
                references: ['A股交易规则']
            },
            {
                id: 'bp_avoid_suspension',
                title: '过滤停牌股票',
                category: '选股',
                description: '交易前检查股票是否停牌，避免无效下单',
                example: `
def filter_paused_stocks(stocks):
    """过滤停牌股票"""
    current_data = get_current_data()
    return [s for s in stocks 
            if not current_data[s].paused]
`,
                references: ['交易系统设计']
            },
            {
                id: 'bp_limit_check',
                title: '涨跌停检查',
                category: '执行',
                description: '下单前检查是否涨跌停，避免无效委托',
                example: `
def can_trade(stock):
    """检查是否可交易"""
    current_data = get_current_data()
    data = current_data[stock]
    
    # 涨停不能买入
    if data.last_price >= data.high_limit * 0.995:
        return False, 'buy'
    
    # 跌停不能卖出
    if data.last_price <= data.low_limit * 1.005:
        return False, 'sell'
    
    return True, None
`,
                references: ['A股交易规则', '程序化交易']
            },
            {
                id: 'bp_rebalance_frequency',
                title: '合理的调仓频率',
                category: '执行',
                description: '调仓频率不宜过高，建议周频或月频，减少交易成本',
                example: `
# 推荐的调仓设置
REBALANCE_DAYS = 20  # 月度调仓

def should_rebalance(context):
    """判断是否需要调仓"""
    if not hasattr(g, 'last_rebalance_date'):
        g.last_rebalance_date = context.current_dt.date()
        return True
    
    days_since = (context.current_dt.date() - g.last_rebalance_date).days
    if days_since >= REBALANCE_DAYS:
        g.last_rebalance_date = context.current_dt.date()
        return True
    
    return False
`,
                references: ['交易成本分析']
            },
            {
                id: 'bp_logging',
                title: '完善的日志记录',
                category: '调试',
                description: '记录关键操作日志，便于回测分析和问题排查',
                example: `
def log_trade(context, stock, action, amount, price):
    """记录交易日志"""
    log.info(f'[{context.current_dt}] {action}: {stock}, '
             f'数量: {amount}, 价格: {price:.2f}')

def log_daily_summary(context):
    """记录每日总结"""
    pv = context.portfolio.total_value
    cash = context.portfolio.cash
    positions = len(context.portfolio.positions)
    log.info(f'日终: 总值={pv:.0f}, 现金={cash:.0f}, 持仓={positions}只')
`,
                references: ['量化系统设计']
            }
        ];
    }
    
    /**
     * 保存知识库
     */
    save(): void {
        try {
            const dir = path.dirname(this.dataPath);
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
            fs.writeFileSync(this.dataPath, JSON.stringify(this.data, null, 2), 'utf-8');
            this.isDirty = false;
        } catch (e) {
            console.error('[KnowledgeStore] 保存失败:', e);
        }
    }
    
    /**
     * 自动保存（如果有更改）
     */
    autoSave(): void {
        if (this.isDirty) {
            this.save();
        }
    }
    
    // ============================================================
    // 策略模式
    // ============================================================
    
    getPatterns(category?: string): StrategyPattern[] {
        if (category) {
            return this.data.patterns.filter(p => p.category === category);
        }
        return this.data.patterns;
    }
    
    getPatternById(id: string): StrategyPattern | undefined {
        return this.data.patterns.find(p => p.id === id);
    }
    
    addPattern(pattern: StrategyPattern): void {
        const existing = this.data.patterns.findIndex(p => p.id === pattern.id);
        if (existing >= 0) {
            this.data.patterns[existing] = pattern;
        } else {
            this.data.patterns.push(pattern);
        }
        this.isDirty = true;
    }
    
    updatePatternEffectiveness(id: string, effectiveness: number): void {
        const pattern = this.data.patterns.find(p => p.id === id);
        if (pattern) {
            pattern.effectiveness = effectiveness;
            pattern.usageCount++;
            this.isDirty = true;
        }
    }
    
    // ============================================================
    // API映射
    // ============================================================
    
    getAPIMappings(): APIMapping[] {
        return this.data.apiMappings;
    }
    
    addAPIMapping(mapping: APIMapping): void {
        const existing = this.data.apiMappings.findIndex(
            m => m.source.api === mapping.source.api && 
                 m.source.platform === mapping.source.platform &&
                 m.target.platform === mapping.target.platform
        );
        if (existing >= 0) {
            this.data.apiMappings[existing] = mapping;
        } else {
            this.data.apiMappings.push(mapping);
        }
        this.isDirty = true;
    }
    
    // ============================================================
    // 最佳实践
    // ============================================================
    
    getBestPractices(category?: string): BestPractice[] {
        if (category) {
            return this.data.bestPractices.filter(bp => bp.category === category);
        }
        return this.data.bestPractices;
    }
    
    addBestPractice(practice: BestPractice): void {
        const existing = this.data.bestPractices.findIndex(bp => bp.id === practice.id);
        if (existing >= 0) {
            this.data.bestPractices[existing] = practice;
        } else {
            this.data.bestPractices.push(practice);
        }
        this.isDirty = true;
    }
    
    // ============================================================
    // 用户反馈
    // ============================================================
    
    getFeedback(resolved?: boolean): UserFeedback[] {
        if (resolved !== undefined) {
            return this.data.userFeedback.filter(f => f.resolved === resolved);
        }
        return this.data.userFeedback;
    }
    
    addFeedback(feedback: UserFeedback): void {
        this.data.userFeedback.push(feedback);
        this.isDirty = true;
    }
    
    resolveFeedback(timestamp: string): void {
        const feedback = this.data.userFeedback.find(f => f.timestamp === timestamp);
        if (feedback) {
            feedback.resolved = true;
            this.isDirty = true;
        }
    }
    
    // ============================================================
    // 统计
    // ============================================================
    
    getStats(): {
        patterns: number;
        apiMappings: number;
        bestPractices: number;
        feedback: { total: number; resolved: number; pending: number };
    } {
        return {
            patterns: this.data.patterns.length,
            apiMappings: this.data.apiMappings.length,
            bestPractices: this.data.bestPractices.length,
            feedback: {
                total: this.data.userFeedback.length,
                resolved: this.data.userFeedback.filter(f => f.resolved).length,
                pending: this.data.userFeedback.filter(f => !f.resolved).length
            }
        };
    }
}

// 单例
let instance: KnowledgeStore | null = null;

export function getKnowledgeStore(storagePath: string): KnowledgeStore {
    if (!instance) {
        instance = new KnowledgeStore(storagePath);
    }
    return instance;
}






