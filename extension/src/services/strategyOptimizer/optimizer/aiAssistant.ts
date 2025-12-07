/**
 * AI辅助模块
 * ===========
 * 
 * 使用AI能力辅助策略优化：
 * - 策略代码改写
 * - 自然语言解释生成
 * - 代码质量检查
 * - 优化建议生成
 */

import { logger } from '../../../utils/logger';
import { AIAssistant } from './interfaces';
import { BacktestResult, OptimizationContext } from './types';

const MODULE = 'AIAssistant';

/** AI优化请求 */
interface AIOptimizeRequest {
    strategyCode: string;
    backtestResult?: BacktestResult;
    optimizationGoal: string;
    constraints?: string[];
    context?: OptimizationContext;
}

/** AI优化结果 */
interface AIOptimizeResult {
    modifiedCode: string;
    changes: Array<{
        type: string;
        description: string;
        before: string | number | boolean | null | Record<string, unknown>;
        after: string | number | boolean | null | Record<string, unknown>;
        reason: string;
    }>;
    explanation: string;
}

/**
 * AI助手实现
 */
export class AIAssistantImpl implements AIAssistant {
    private apiEndpoint: string = '';
    private apiKey: string = '';
    
    constructor(apiEndpoint?: string, apiKey?: string) {
        this.apiEndpoint = apiEndpoint || '';
        this.apiKey = apiKey || '';
    }
    
    /**
     * 设置API配置
     */
    setConfig(apiEndpoint: string, apiKey: string): void {
        this.apiEndpoint = apiEndpoint;
        this.apiKey = apiKey;
    }
    
    /**
     * 使用AI优化策略
     */
    async optimizeStrategy(request: AIOptimizeRequest): Promise<AIOptimizeResult> {
        logger.info(`开始AI辅助优化: ${request.optimizationGoal}`, MODULE);
        
        // 构建优化提示
        const prompt = this.buildOptimizationPrompt(request);
        
        try {
            // 尝试调用Cursor内置AI
            const result = await this.callCursorAI(prompt);
            
            if (result) {
                return this.parseAIResponse(result, request.strategyCode);
            }
            
            // 如果Cursor AI不可用，使用规则引擎生成建议
            return this.generateRuleBasedOptimization(request);
            
        } catch (error) {
            logger.warn(`AI调用失败，使用规则引擎: ${error}`, MODULE);
            return this.generateRuleBasedOptimization(request);
        }
    }
    
    /**
     * 构建优化提示
     */
    private buildOptimizationPrompt(request: AIOptimizeRequest): string {
        let prompt = `你是一个专业的量化策略优化专家。请分析以下策略代码并根据优化目标进行改进。

## 优化目标
${request.optimizationGoal}

## 约束条件
${request.constraints?.join('\n') || '无特殊约束'}

## 策略代码
\`\`\`python
${request.strategyCode}
\`\`\`
`;

        if (request.backtestResult) {
            prompt += `
## 当前回测结果
- 总收益: ${(request.backtestResult.metrics.totalReturn * 100).toFixed(2)}%
- 夏普比率: ${request.backtestResult.metrics.sharpeRatio.toFixed(2)}
- 最大回撤: ${(request.backtestResult.metrics.maxDrawdown * 100).toFixed(2)}%
- 胜率: ${(request.backtestResult.metrics.winRate * 100).toFixed(2)}%
`;
        }

        if (request.context?.marketContext) {
            prompt += `
## 市场环境
- 市场状态: ${request.context.marketContext.regime}
`;
        }

        prompt += `
## 输出要求
请以JSON格式输出优化结果，包含：
1. modifiedCode: 修改后的完整策略代码
2. changes: 修改列表，每项包含 type, description, before, after, reason
3. explanation: 整体优化说明

请确保输出有效的JSON格式。
`;

        return prompt;
    }
    
    /**
     * 调用Cursor AI（通过VS Code API）
     */
    private async callCursorAI(_prompt: string): Promise<string | null> {
        try {
            // 尝试使用VS Code的语言模型API（如果可用）
            // 注意：这需要VS Code 1.90+版本和适当的权限
            
            // 目前返回null，让系统使用规则引擎
            // 未来可以集成Cursor的AI API
            return null;
        } catch (error) {
            logger.debug(`Cursor AI不可用: ${error}`, MODULE);
            return null;
        }
    }
    
    /**
     * 解析AI响应
     */
    private parseAIResponse(response: string, originalCode: string): AIOptimizeResult {
        try {
            // 尝试提取JSON
            const jsonMatch = response.match(/\{[\s\S]*\}/);
            if (jsonMatch) {
                const parsed = JSON.parse(jsonMatch[0]);
                return {
                    modifiedCode: parsed.modifiedCode || originalCode,
                    changes: parsed.changes || [],
                    explanation: parsed.explanation || '优化完成'
                };
            }
        } catch (error) {
            logger.warn(`解析AI响应失败: ${error}`, MODULE);
        }
        
        return {
            modifiedCode: originalCode,
            changes: [],
            explanation: '无法解析AI响应'
        };
    }
    
    /**
     * 基于规则的优化（当AI不可用时）
     */
    private generateRuleBasedOptimization(request: AIOptimizeRequest): AIOptimizeResult {
        const code = request.strategyCode;
        let modifiedCode = code;
        const changes: AIOptimizeResult['changes'] = [];
        
        // 规则1: 添加止损（如果没有）
        if (!code.includes('STOP_LOSS') && !code.includes('stop_loss')) {
            const insertPoint = code.indexOf('def initialize');
            if (insertPoint > 0) {
                const stopLossCode = `\n# 风险控制参数\nSTOP_LOSS = 0.08  # 止损线8%\nTAKE_PROFIT = 0.20  # 止盈线20%\n`;
                modifiedCode = modifiedCode.slice(0, insertPoint) + stopLossCode + modifiedCode.slice(insertPoint);
                changes.push({
                    type: 'risk_control',
                    description: '添加止损止盈参数',
                    before: null,
                    after: { STOP_LOSS: 0.08, TAKE_PROFIT: 0.20 },
                    reason: '策略缺少风险控制机制，添加止损止盈有助于控制回撤'
                });
            }
        }
        
        // 规则2: 优化持股数量
        const stockNumMatch = code.match(/(?:STOCK_NUM|stock_num|g\.stock_num)\s*=\s*(\d+)/);
        if (stockNumMatch) {
            const currentNum = parseInt(stockNumMatch[1]);
            if (currentNum < 5 || currentNum > 30) {
                const optimalNum = currentNum < 5 ? 10 : 20;
                modifiedCode = modifiedCode.replace(
                    stockNumMatch[0],
                    stockNumMatch[0].replace(stockNumMatch[1], String(optimalNum))
                );
                changes.push({
                    type: 'parameter',
                    description: '调整持股数量',
                    before: currentNum,
                    after: optimalNum,
                    reason: currentNum < 5 ? '持股过于集中，风险较高' : '持股过于分散，收益弹性降低'
                });
            }
        }
        
        // 规则3: 添加市场状态判断（如果是进攻型策略）
        if (request.optimizationGoal.includes('降低回撤') || request.optimizationGoal.includes('控制风险')) {
            if (!code.includes('市场状态') && !code.includes('market_regime')) {
                // 建议添加市场状态判断
                changes.push({
                    type: 'feature',
                    description: '建议添加市场状态判断',
                    before: null,
                    after: '市场状态判断逻辑',
                    reason: '在市场下行时降低仓位可有效控制回撤'
                });
            }
        }
        
        // 规则4: 优化因子权重（如果是多因子策略）
        if (request.optimizationGoal.includes('提高夏普') || request.optimizationGoal.includes('提高收益')) {
            const factorMatch = code.match(/factors?\s*=\s*\{[\s\S]*?\}/);
            if (factorMatch) {
                changes.push({
                    type: 'suggestion',
                    description: '建议优化因子权重',
                    before: '当前因子配置',
                    after: '建议根据回测结果调整因子权重',
                    reason: '因子权重优化可提高策略的风险调整收益'
                });
            }
        }
        
        // 生成解释
        let explanation = '基于规则引擎的优化分析：\n\n';
        
        if (changes.length === 0) {
            explanation += '当前策略结构良好，未发现明显可优化点。\n';
            explanation += '建议通过参数优化功能进一步测试不同参数组合。';
        } else {
            explanation += `发现 ${changes.length} 个优化点：\n\n`;
            for (const change of changes) {
                explanation += `• ${change.description}: ${change.reason}\n`;
            }
            explanation += '\n建议在回测环境中验证修改效果。';
        }
        
        return {
            modifiedCode,
            changes,
            explanation
        };
    }
    
    /**
     * 生成策略解释
     */
    async explainStrategy(strategyCode: string): Promise<string> {
        logger.info('生成策略解释', MODULE);
        
        // 分析策略结构
        const analysis = this.analyzeStrategyStructure(strategyCode);
        
        let explanation = `## 策略解读\n\n`;
        
        // 基本信息
        explanation += `### 基本信息\n`;
        explanation += `- **平台**: ${analysis.platform}\n`;
        explanation += `- **策略类型**: ${analysis.strategyType}\n`;
        explanation += `- **代码行数**: ${strategyCode.split('\n').length}\n\n`;
        
        // 核心逻辑
        explanation += `### 核心逻辑\n`;
        if (analysis.hasFactors) {
            explanation += `- 使用多因子选股模型\n`;
        }
        if (analysis.hasStopLoss) {
            explanation += `- 包含止损机制\n`;
        }
        if (analysis.hasTakeProfit) {
            explanation += `- 包含止盈机制\n`;
        }
        if (analysis.hasRebalance) {
            explanation += `- 定期调仓\n`;
        }
        
        // 参数
        explanation += `\n### 主要参数\n`;
        for (const param of analysis.parameters) {
            explanation += `- **${param.name}**: ${param.value} (${param.description})\n`;
        }
        
        // 风险提示
        explanation += `\n### 风险提示\n`;
        if (!analysis.hasStopLoss) {
            explanation += `- ⚠️ 策略未设置止损，在极端行情下可能面临较大损失\n`;
        }
        if (analysis.stockNum && analysis.stockNum < 5) {
            explanation += `- ⚠️ 持股集中度较高，单只股票波动影响较大\n`;
        }
        
        return explanation;
    }
    
    /**
     * 分析策略结构
     */
    private analyzeStrategyStructure(code: string): {
        platform: string;
        strategyType: string;
        hasFactors: boolean;
        hasStopLoss: boolean;
        hasTakeProfit: boolean;
        hasRebalance: boolean;
        stockNum: number | null;
        parameters: Array<{ name: string; value: string | number | boolean; description: string }>;
    } {
        // 判断平台
        let platform = '未知';
        if (code.includes('from jqdata') || code.includes('聚宽')) {
            platform = 'JoinQuant (聚宽)';
        } else if (code.includes('ContextInfo') || code.includes('QMT')) {
            platform = 'QMT (迅投)';
        } else if (code.includes('trade_api') || code.includes('ptrade')) {
            platform = 'PTrade (恒生)';
        }
        
        // 判断策略类型
        let strategyType = '量化选股';
        if (code.includes('factor') || code.includes('因子')) {
            strategyType = '多因子选股';
        } else if (code.includes('momentum') || code.includes('动量')) {
            strategyType = '动量策略';
        } else if (code.includes('value') || code.includes('价值')) {
            strategyType = '价值策略';
        }
        
        // 提取参数
        const parameters: Array<{ name: string; value: string | number | boolean; description: string }> = [];
        
        const paramPatterns = [
            { pattern: /STOCK_NUM\s*=\s*(\d+)/, name: 'STOCK_NUM', desc: '持股数量' },
            { pattern: /STOP_LOSS\s*=\s*([\d.]+)/, name: 'STOP_LOSS', desc: '止损线' },
            { pattern: /TAKE_PROFIT\s*=\s*([\d.]+)/, name: 'TAKE_PROFIT', desc: '止盈线' },
            { pattern: /MA_PERIOD\s*=\s*(\d+)/, name: 'MA_PERIOD', desc: '均线周期' },
        ];
        
        for (const { pattern, name, desc } of paramPatterns) {
            const match = code.match(pattern);
            if (match) {
                parameters.push({ name, value: match[1], description: desc });
            }
        }
        
        // 提取持股数量
        const stockNumMatch = code.match(/(?:STOCK_NUM|stock_num|g\.stock_num)\s*=\s*(\d+)/);
        const stockNum = stockNumMatch ? parseInt(stockNumMatch[1]) : null;
        
        return {
            platform,
            strategyType,
            hasFactors: /factor|因子/i.test(code),
            hasStopLoss: /stop.?loss|止损/i.test(code),
            hasTakeProfit: /take.?profit|止盈/i.test(code),
            hasRebalance: /rebalance|调仓|换仓/i.test(code),
            stockNum,
            parameters
        };
    }
    
    /**
     * 生成代码质量检查报告
     */
    async checkCodeQuality(strategyCode: string): Promise<{
        score: number;
        issues: Array<{
            severity: 'error' | 'warning' | 'info';
            message: string;
            line?: number;
            suggestion?: string;
        }>;
    }> {
        const issues: Array<{
            severity: 'error' | 'warning' | 'info';
            message: string;
            line?: number;
            suggestion?: string;
        }> = [];
        
        const lines = strategyCode.split('\n');
        let score = 100;
        
        // 检查常见问题
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const lineNum = i + 1;
            
            // 检查硬编码股票代码
            if (/['"]00\d{4}\.X|['"]60\d{4}\.X|['"]30\d{4}\.X/.test(line)) {
                issues.push({
                    severity: 'warning',
                    message: '发现硬编码股票代码',
                    line: lineNum,
                    suggestion: '建议使用股票池或动态选股，避免硬编码特定股票'
                });
                score -= 5;
            }
            
            // 检查print语句
            if (/^\s*print\(/.test(line) && !/^\s*#/.test(line)) {
                issues.push({
                    severity: 'info',
                    message: '使用print语句',
                    line: lineNum,
                    suggestion: '建议使用log.info替代print，便于日志管理'
                });
                score -= 2;
            }
            
            // 检查magic number
            if (/=\s*(?:0\.\d+|[1-9]\d*)(?!\d)/.test(line) && !/[A-Z_]{3,}\s*=/.test(line)) {
                if (!line.includes('#') && !line.includes('range') && !line.includes('index')) {
                    // 可能是魔数，但不一定
                }
            }
        }
        
        // 检查是否有docstring
        if (!strategyCode.includes('"""') && !strategyCode.includes("'''")) {
            issues.push({
                severity: 'info',
                message: '策略缺少文档字符串',
                suggestion: '建议添加策略说明，包括目标、参数、使用方法等'
            });
            score -= 5;
        }
        
        // 检查是否有错误处理
        if (!strategyCode.includes('try:') && !strategyCode.includes('except')) {
            issues.push({
                severity: 'warning',
                message: '策略缺少异常处理',
                suggestion: '建议在关键位置添加try-except，提高策略稳定性'
            });
            score -= 5;
        }
        
        // 检查是否有日志记录
        if (!strategyCode.includes('log.') && !strategyCode.includes('logging.')) {
            issues.push({
                severity: 'info',
                message: '策略缺少日志记录',
                suggestion: '建议添加日志记录，便于调试和监控'
            });
            score -= 3;
        }
        
        return {
            score: Math.max(0, score),
            issues
        };
    }
    
    /**
     * 生成因子建议
     */
    async suggestFactors(
        currentFactors: string[],
        marketContext: { regime: string }
    ): Promise<Array<{
        factor: string;
        category: string;
        description: string;
        expectedEffect: string;
        synergy: string[];
    }>> {
        const suggestions: Array<{
            factor: string;
            category: string;
            description: string;
            expectedEffect: string;
            synergy: string[];
        }> = [];
        
        // 根据市场状态推荐因子
        if (marketContext.regime === 'risk_on') {
            // 风险偏好市场
            if (!currentFactors.includes('momentum')) {
                suggestions.push({
                    factor: 'momentum',
                    category: '动量',
                    description: '过去N日收益率',
                    expectedEffect: '在上涨市场中捕捉趋势延续',
                    synergy: ['beta', 'turnover']
                });
            }
            if (!currentFactors.includes('beta')) {
                suggestions.push({
                    factor: 'beta',
                    category: '风险',
                    description: '相对市场的敏感度',
                    expectedEffect: '高Beta股票在牛市中表现更好',
                    synergy: ['momentum', 'growth']
                });
            }
        } else if (marketContext.regime === 'risk_off') {
            // 风险规避市场
            if (!currentFactors.includes('low_volatility')) {
                suggestions.push({
                    factor: 'low_volatility',
                    category: '风险',
                    description: '历史波动率',
                    expectedEffect: '低波动股票在下跌市场中更抗跌',
                    synergy: ['dividend', 'quality']
                });
            }
            if (!currentFactors.includes('dividend')) {
                suggestions.push({
                    factor: 'dividend',
                    category: '价值',
                    description: '股息率',
                    expectedEffect: '高股息股票提供下行保护',
                    synergy: ['low_volatility', 'value']
                });
            }
        }
        
        // 通用建议
        if (!currentFactors.includes('quality')) {
            suggestions.push({
                factor: 'quality',
                category: '质量',
                description: 'ROE、利润增长等质量指标',
                expectedEffect: '长期稳定收益',
                synergy: ['value', 'low_volatility']
            });
        }
        
        return suggestions;
    }
    
    /**
     * 生成策略说明（实现接口方法）
     */
    async generateExplanation(
        strategyCode: string,
        changes: Array<{
            type: string;
            description: string;
            before: string | number | boolean | null;
            after: string | number | boolean | null;
        }>
    ): Promise<string> {
        let explanation = `## 策略变更说明\n\n`;
        
        if (changes.length === 0) {
            explanation += '策略未发生变更。\n';
            return explanation;
        }
        
        explanation += `共进行了 ${changes.length} 项修改：\n\n`;
        
        for (const change of changes) {
            explanation += `### ${change.type}: ${change.description}\n`;
            explanation += `- **修改前**: ${JSON.stringify(change.before)}\n`;
            explanation += `- **修改后**: ${JSON.stringify(change.after)}\n\n`;
        }
        
        // 添加策略解释
        const strategyExplanation = await this.explainStrategy(strategyCode);
        explanation += '\n---\n\n' + strategyExplanation;
        
        return explanation;
    }
}

/**
 * 创建AI助手
 */
export function createAIAssistant(apiEndpoint?: string, apiKey?: string): AIAssistant {
    return new AIAssistantImpl(apiEndpoint, apiKey);
}

