/**
 * 策略分析器
 * ===========
 * 
 * 分析用户策略代码，提取关键信息：
 * - 使用的因子
 * - 风控参数（止损/止盈/仓位）
 * - 选股逻辑
 * - 交易频率
 * 
 * 为优化建议提供数据基础
 */

import { logger } from '../../../utils/logger';

const MODULE = 'StrategyAnalyzer';

/** 策略分析结果 */
export interface StrategyAnalysis {
    // 基本信息
    name: string;
    platform: 'ptrade' | 'qmt' | 'joinquant' | 'unknown';
    
    // 因子信息
    factors: FactorInfo[];
    
    // 风控参数
    riskControl: RiskControlInfo;
    
    // 选股信息
    stockSelection: StockSelectionInfo;
    
    // 交易信息
    trading: TradingInfo;
    
    // 问题和建议
    issues: StrategyIssue[];
}

export interface FactorInfo {
    name: string;
    type: 'momentum' | 'value' | 'quality' | 'growth' | 'technical' | 'other';
    weight?: number;
    code: string;  // 代码片段
}

export interface RiskControlInfo {
    stopLoss?: number;      // 止损线
    takeProfit?: number;    // 止盈线
    maxPosition?: number;   // 最大仓位
    singleStockMax?: number; // 单股最大仓位
    hasDrawdownControl: boolean;
}

export interface StockSelectionInfo {
    universe: string;       // 股票池
    filters: string[];      // 筛选条件
    sortBy?: string;        // 排序依据
    topN?: number;          // 选股数量
}

export interface TradingInfo {
    frequency: 'daily' | 'weekly' | 'monthly' | 'intraday';
    rebalanceDay?: string;
    hasTimingLogic: boolean;
}

export interface StrategyIssue {
    type: 'warning' | 'error' | 'suggestion';
    category: 'risk' | 'factor' | 'performance' | 'code';
    message: string;
    line?: number;
    suggestion?: string;
}

/** 因子识别模式 */
const FACTOR_PATTERNS: Array<{
    pattern: RegExp;
    name: string;
    type: FactorInfo['type'];
}> = [
    // 动量因子
    { pattern: /momentum|动量|涨幅|收益率/gi, name: '动量因子', type: 'momentum' },
    { pattern: /rsi|相对强弱/gi, name: 'RSI', type: 'momentum' },
    { pattern: /macd/gi, name: 'MACD', type: 'momentum' },
    
    // 价值因子
    { pattern: /pe_ratio|市盈率|PE/gi, name: '市盈率', type: 'value' },
    { pattern: /pb_ratio|市净率|PB/gi, name: '市净率', type: 'value' },
    { pattern: /ps_ratio|市销率/gi, name: '市销率', type: 'value' },
    
    // 质量因子
    { pattern: /roe|净资产收益率/gi, name: 'ROE', type: 'quality' },
    { pattern: /roa|资产收益率/gi, name: 'ROA', type: 'quality' },
    { pattern: /gross_margin|毛利率/gi, name: '毛利率', type: 'quality' },
    
    // 成长因子
    { pattern: /revenue_growth|营收增长/gi, name: '营收增长', type: 'growth' },
    { pattern: /profit_growth|利润增长/gi, name: '利润增长', type: 'growth' },
    { pattern: /eps_growth|EPS增长/gi, name: 'EPS增长', type: 'growth' },
    
    // 技术因子
    { pattern: /ma\d+|均线|moving_average/gi, name: '均线', type: 'technical' },
    { pattern: /volatility|波动率/gi, name: '波动率', type: 'technical' },
    { pattern: /volume|成交量|换手率/gi, name: '成交量', type: 'technical' },
];

/** 风控参数模式 */
const RISK_PATTERNS = {
    stopLoss: /stop_loss|止损|止损线?\s*[=:]\s*([\d.]+)/gi,
    takeProfit: /take_profit|止盈|止盈线?\s*[=:]\s*([\d.]+)/gi,
    maxPosition: /max_position|最大仓位|总仓位\s*[=:]\s*([\d.]+)/gi,
    singleStockMax: /single.*max|单股.*仓位\s*[=:]\s*([\d.]+)/gi,
    drawdown: /drawdown|回撤|最大回撤/gi,
};

/** 平台识别模式 */
const PLATFORM_PATTERNS = {
    ptrade: /PTrade|恒生|run_daily|run_weekly/i,
    qmt: /QMT|迅投|xtquant/i,
    joinquant: /聚宽|jqdata|set_benchmark/i,
};

/**
 * 策略分析器类
 */
export class StrategyAnalyzer {
    
    /**
     * 分析策略代码
     */
    analyze(code: string, fileName?: string): StrategyAnalysis {
        logger.info(`开始分析策略: ${fileName || '未命名'}`, MODULE);
        
        const analysis: StrategyAnalysis = {
            name: this.extractName(code, fileName),
            platform: this.detectPlatform(code),
            factors: this.extractFactors(code),
            riskControl: this.extractRiskControl(code),
            stockSelection: this.extractStockSelection(code),
            trading: this.extractTradingInfo(code),
            issues: [],
        };
        
        // 检测问题
        analysis.issues = this.detectIssues(analysis, code);
        
        logger.info(`策略分析完成: ${analysis.factors.length}个因子, ${analysis.issues.length}个问题`, MODULE);
        return analysis;
    }
    
    /**
     * 提取策略名称
     */
    private extractName(code: string, fileName?: string): string {
        // 从文档字符串提取
        const docMatch = code.match(/"""[\s\S]*?([^\n]+)[\s\S]*?"""/);
        if (docMatch) {
            return docMatch[1].trim();
        }
        
        // 从文件名提取
        if (fileName) {
            return fileName.replace(/\.(py|txt)$/, '');
        }
        
        return '未命名策略';
    }
    
    /**
     * 检测平台
     */
    private detectPlatform(code: string): StrategyAnalysis['platform'] {
        for (const [platform, pattern] of Object.entries(PLATFORM_PATTERNS)) {
            if (pattern.test(code)) {
                return platform as StrategyAnalysis['platform'];
            }
        }
        return 'unknown';
    }
    
    /**
     * 提取因子信息
     */
    private extractFactors(code: string): FactorInfo[] {
        const factors: FactorInfo[] = [];
        const seen = new Set<string>();
        
        for (const { pattern, name, type } of FACTOR_PATTERNS) {
            const matches = code.matchAll(pattern);
            for (const match of matches) {
                if (!seen.has(name)) {
                    seen.add(name);
                    
                    // 提取包含该因子的代码行
                    const lineStart = code.lastIndexOf('\n', match.index) + 1;
                    const lineEnd = code.indexOf('\n', match.index);
                    const codeLine = code.slice(lineStart, lineEnd > 0 ? lineEnd : undefined).trim();
                    
                    factors.push({
                        name,
                        type,
                        code: codeLine.slice(0, 100),
                    });
                }
            }
        }
        
        return factors;
    }
    
    /**
     * 提取风控参数
     */
    private extractRiskControl(code: string): RiskControlInfo {
        const riskControl: RiskControlInfo = {
            hasDrawdownControl: RISK_PATTERNS.drawdown.test(code),
        };
        
        // 提取止损
        const stopLossMatch = code.match(/stop_loss\s*[=:]\s*([\d.]+)/i) ||
                              code.match(/止损.*?([\d.]+)/);
        if (stopLossMatch) {
            riskControl.stopLoss = parseFloat(stopLossMatch[1]);
        }
        
        // 提取止盈
        const takeProfitMatch = code.match(/take_profit\s*[=:]\s*([\d.]+)/i) ||
                                code.match(/止盈.*?([\d.]+)/);
        if (takeProfitMatch) {
            riskControl.takeProfit = parseFloat(takeProfitMatch[1]);
        }
        
        // 提取仓位
        const maxPosMatch = code.match(/max_position\s*[=:]\s*([\d.]+)/i) ||
                           code.match(/最大仓位.*?([\d.]+)/);
        if (maxPosMatch) {
            riskControl.maxPosition = parseFloat(maxPosMatch[1]);
        }
        
        // 单股仓位
        const singleMaxMatch = code.match(/single.*max\s*[=:]\s*([\d.]+)/i);
        if (singleMaxMatch) {
            riskControl.singleStockMax = parseFloat(singleMaxMatch[1]);
        }
        
        return riskControl;
    }
    
    /**
     * 提取选股信息
     */
    private extractStockSelection(code: string): StockSelectionInfo {
        const info: StockSelectionInfo = {
            universe: '未知',
            filters: [],
        };
        
        // 股票池
        if (/沪深300|000300/i.test(code)) {
            info.universe = '沪深300';
        } else if (/中证500|000905/i.test(code)) {
            info.universe = '中证500';
        } else if (/创业板/i.test(code)) {
            info.universe = '创业板';
        } else if (/全市场|all_stocks/i.test(code)) {
            info.universe = '全市场';
        }
        
        // 筛选条件
        if (/ST/i.test(code)) info.filters.push('排除ST');
        if (/停牌|is_paused/i.test(code)) info.filters.push('排除停牌');
        if (/涨跌停|limit/i.test(code)) info.filters.push('排除涨跌停');
        if (/市值.*?亿|market_cap/i.test(code)) info.filters.push('市值筛选');
        
        // 选股数量
        const topNMatch = code.match(/g\.stock_num\s*=\s*(\d+)/i) ||
                         code.match(/top.*?(\d+)/i);
        if (topNMatch) {
            info.topN = parseInt(topNMatch[1]);
        }
        
        return info;
    }
    
    /**
     * 提取交易信息
     */
    private extractTradingInfo(code: string): TradingInfo {
        const info: TradingInfo = {
            frequency: 'daily',
            hasTimingLogic: false,
        };
        
        // 频率
        if (/run_monthly|月度/i.test(code)) {
            info.frequency = 'monthly';
        } else if (/run_weekly|周度|每周/i.test(code)) {
            info.frequency = 'weekly';
        } else if (/分钟|intraday|minute/i.test(code)) {
            info.frequency = 'intraday';
        }
        
        // 调仓日
        const rebalanceMatch = code.match(/rebalance_day\s*=\s*['"]?(\w+)['"]?/i);
        if (rebalanceMatch) {
            info.rebalanceDay = rebalanceMatch[1];
        }
        
        // 择时逻辑
        info.hasTimingLogic = /择时|timing|大盘.*判断|市场.*状态/i.test(code);
        
        return info;
    }
    
    /**
     * 检测策略问题
     */
    private detectIssues(analysis: StrategyAnalysis, code: string): StrategyIssue[] {
        const issues: StrategyIssue[] = [];
        
        // 风控检查
        if (!analysis.riskControl.stopLoss) {
            issues.push({
                type: 'warning',
                category: 'risk',
                message: '未设置止损线',
                suggestion: '建议设置8%-15%的止损线控制风险',
            });
        }
        
        if (!analysis.riskControl.maxPosition) {
            issues.push({
                type: 'suggestion',
                category: 'risk',
                message: '未明确设置最大仓位',
                suggestion: '建议设置总仓位上限，如80%',
            });
        }
        
        if (analysis.riskControl.stopLoss && analysis.riskControl.stopLoss > 0.2) {
            issues.push({
                type: 'warning',
                category: 'risk',
                message: `止损线过宽 (${(analysis.riskControl.stopLoss * 100).toFixed(0)}%)`,
                suggestion: '建议止损线不超过15%',
            });
        }
        
        // 因子检查
        if (analysis.factors.length === 0) {
            issues.push({
                type: 'warning',
                category: 'factor',
                message: '未识别到明确的选股因子',
                suggestion: '建议使用量化因子（如动量、价值、质量）进行选股',
            });
        }
        
        if (analysis.factors.length === 1) {
            issues.push({
                type: 'suggestion',
                category: 'factor',
                message: '仅使用单一因子',
                suggestion: '建议组合多个低相关因子提高稳定性',
            });
        }
        
        // 选股检查
        if (analysis.stockSelection.topN && analysis.stockSelection.topN < 5) {
            issues.push({
                type: 'warning',
                category: 'risk',
                message: `持股数量过少 (${analysis.stockSelection.topN}只)`,
                suggestion: '建议持有5-20只股票分散风险',
            });
        }
        
        // 代码质量
        if (!/def\s+initialize/i.test(code)) {
            issues.push({
                type: 'error',
                category: 'code',
                message: '缺少initialize函数',
                suggestion: '需要定义initialize(context)初始化函数',
            });
        }
        
        return issues;
    }
}

/** 创建分析器实例 */
export function createStrategyAnalyzer(): StrategyAnalyzer {
    return new StrategyAnalyzer();
}

