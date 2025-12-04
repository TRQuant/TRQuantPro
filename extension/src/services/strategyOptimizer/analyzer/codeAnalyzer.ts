/**
 * 策略代码分析器
 * ==============
 * 
 * 解析Python策略代码，提取核心逻辑、API调用、因子使用等信息
 */

import {
    StrategyAnalysis,
    CodeBlock,
    APIUsage,
    FactorUsage,
    IndicatorUsage,
    CompatibilityScore,
    Platform
} from '../types';

// ============================================================
// API识别模式
// ============================================================

const JOINQUANT_APIS = [
    // 数据获取
    { pattern: /get_price\s*\(/g, name: 'get_price', category: 'data' },
    { pattern: /get_fundamentals\s*\(/g, name: 'get_fundamentals', category: 'data' },
    { pattern: /get_current_data\s*\(/g, name: 'get_current_data', category: 'data' },
    { pattern: /get_extras\s*\(/g, name: 'get_extras', category: 'data' },
    { pattern: /get_index_stocks\s*\(/g, name: 'get_index_stocks', category: 'data' },
    { pattern: /get_industry_stocks\s*\(/g, name: 'get_industry_stocks', category: 'data' },
    { pattern: /get_concept_stocks\s*\(/g, name: 'get_concept_stocks', category: 'data' },
    { pattern: /get_all_securities\s*\(/g, name: 'get_all_securities', category: 'data' },
    { pattern: /history\s*\(/g, name: 'history', category: 'data' },
    { pattern: /attribute_history\s*\(/g, name: 'attribute_history', category: 'data' },
    
    // 交易相关
    { pattern: /order\s*\(/g, name: 'order', category: 'trade' },
    { pattern: /order_target\s*\(/g, name: 'order_target', category: 'trade' },
    { pattern: /order_target_value\s*\(/g, name: 'order_target_value', category: 'trade' },
    { pattern: /order_value\s*\(/g, name: 'order_value', category: 'trade' },
    { pattern: /cancel_order\s*\(/g, name: 'cancel_order', category: 'trade' },
    { pattern: /get_open_orders\s*\(/g, name: 'get_open_orders', category: 'trade' },
    
    // 设置相关
    { pattern: /set_benchmark\s*\(/g, name: 'set_benchmark', category: 'setting' },
    { pattern: /set_option\s*\(/g, name: 'set_option', category: 'setting' },
    { pattern: /set_slippage\s*\(/g, name: 'set_slippage', category: 'setting' },
    { pattern: /set_order_cost\s*\(/g, name: 'set_order_cost', category: 'setting' },
    { pattern: /set_universe\s*\(/g, name: 'set_universe', category: 'setting' },
    
    // 日志
    { pattern: /log\.info\s*\(/g, name: 'log.info', category: 'log' },
    { pattern: /log\.warn\s*\(/g, name: 'log.warn', category: 'log' },
    { pattern: /log\.error\s*\(/g, name: 'log.error', category: 'log' },
    
    // 定时任务
    { pattern: /run_daily\s*\(/g, name: 'run_daily', category: 'schedule' },
    { pattern: /run_weekly\s*\(/g, name: 'run_weekly', category: 'schedule' },
    { pattern: /run_monthly\s*\(/g, name: 'run_monthly', category: 'schedule' },
];

const PTRADE_APIS = [
    { pattern: /get_history\s*\(/g, name: 'get_history', category: 'data' },
    { pattern: /get_snapshot\s*\(/g, name: 'get_snapshot', category: 'data' },
    { pattern: /get_Ede\s*\(/g, name: 'get_Ede', category: 'data' },
    { pattern: /order_target_percent\s*\(/g, name: 'order_target_percent', category: 'trade' },
    { pattern: /order_lots\s*\(/g, name: 'order_lots', category: 'trade' },
    { pattern: /on_bar\s*\(/g, name: 'on_bar', category: 'entry' },
];

// ============================================================
// 因子识别模式
// ============================================================

const FACTOR_PATTERNS = [
    // 价值因子
    { pattern: /\bpe\b|\bPE\b|pe_ratio|市盈率/gi, type: 'value', name: 'PE' },
    { pattern: /\bpb\b|\bPB\b|pb_ratio|市净率/gi, type: 'value', name: 'PB' },
    { pattern: /\bps\b|\bPS\b|ps_ratio|市销率/gi, type: 'value', name: 'PS' },
    { pattern: /\bpcf\b|\bPCF\b|市现率/gi, type: 'value', name: 'PCF' },
    { pattern: /dividend|股息|分红/gi, type: 'value', name: 'Dividend' },
    
    // 成长因子
    { pattern: /revenue_growth|营收增长/gi, type: 'growth', name: 'RevenueGrowth' },
    { pattern: /profit_growth|利润增长|净利润增长/gi, type: 'growth', name: 'ProfitGrowth' },
    { pattern: /eps_growth|每股收益增长/gi, type: 'growth', name: 'EPSGrowth' },
    { pattern: /roe_growth|ROE增长/gi, type: 'growth', name: 'ROEGrowth' },
    
    // 质量因子
    { pattern: /\broe\b|\bROE\b|净资产收益率/gi, type: 'quality', name: 'ROE' },
    { pattern: /\broa\b|\bROA\b|总资产收益率/gi, type: 'quality', name: 'ROA' },
    { pattern: /gross_margin|毛利率/gi, type: 'quality', name: 'GrossMargin' },
    { pattern: /net_margin|净利率/gi, type: 'quality', name: 'NetMargin' },
    { pattern: /asset_turnover|资产周转/gi, type: 'quality', name: 'AssetTurnover' },
    
    // 动量因子
    { pattern: /momentum|动量/gi, type: 'momentum', name: 'Momentum' },
    { pattern: /return_\d+d|收益率/gi, type: 'momentum', name: 'Return' },
    { pattern: /relative_strength|相对强度/gi, type: 'momentum', name: 'RelativeStrength' },
    
    // 波动因子
    { pattern: /volatility|波动率/gi, type: 'volatility', name: 'Volatility' },
    { pattern: /\bbeta\b|贝塔/gi, type: 'volatility', name: 'Beta' },
    { pattern: /std_dev|标准差/gi, type: 'volatility', name: 'StdDev' },
];

// ============================================================
// 技术指标识别
// ============================================================

const INDICATOR_PATTERNS = [
    { pattern: /\bMA\b|移动平均|ma\(/gi, type: 'ma', name: 'MA' },
    { pattern: /\bEMA\b|指数平均|ema\(/gi, type: 'ma', name: 'EMA' },
    { pattern: /\bMACD\b|macd/gi, type: 'macd', name: 'MACD' },
    { pattern: /\bRSI\b|rsi|相对强弱/gi, type: 'rsi', name: 'RSI' },
    { pattern: /\bKDJ\b|kdj/gi, type: 'kdj', name: 'KDJ' },
    { pattern: /\bBOLL\b|布林|boll/gi, type: 'boll', name: 'BOLL' },
    { pattern: /\bATR\b|atr|平均真实波幅/gi, type: 'atr', name: 'ATR' },
];

// ============================================================
// 代码分析器类
// ============================================================

export class CodeAnalyzer {
    
    /**
     * 分析策略代码
     */
    analyze(code: string, filename?: string): StrategyAnalysis {
        const lines = code.split('\n');
        
        // 提取元信息
        const meta = this.extractMeta(code, filename);
        
        // 提取代码块
        const blocks = this.extractCodeBlocks(code);
        
        // 分类组件
        const components = this.categorizeComponents(blocks);
        
        // 分析依赖
        const dependencies = this.analyzeDependencies(code, lines);
        
        // 计算兼容性
        const compatibility = this.calculateCompatibility(dependencies.apis);
        
        // 统计信息
        const stats = this.calculateStats(code, blocks);
        
        return {
            meta,
            components,
            dependencies,
            compatibility,
            stats
        };
    }
    
    /**
     * 提取元信息（从docstring和注释）
     */
    private extractMeta(code: string, filename?: string): StrategyAnalysis['meta'] {
        const meta: StrategyAnalysis['meta'] = {
            name: filename?.replace('.py', '') || '未命名策略',
            description: ''
        };
        
        // 提取docstring
        const docstringMatch = code.match(/^[\s\S]*?"""([\s\S]*?)"""/);
        if (docstringMatch) {
            const docstring = docstringMatch[1];
            
            // 提取名称
            const nameMatch = docstring.match(/^(.+?)\s*[-=]/m);
            if (nameMatch) {
                meta.name = nameMatch[1].trim();
            }
            
            // 提取创建时间
            const createTimeMatch = docstring.match(/创建时间[：:]\s*(.+)/);
            if (createTimeMatch) {
                meta.createTime = createTimeMatch[1].trim();
            }
            
            // 提取回测区间
            const backtestMatch = docstring.match(/回测区间[：:]\s*(\d{4}-\d{2}-\d{2})\s*至\s*(\d{4}-\d{2}-\d{2})/);
            if (backtestMatch) {
                meta.backtestPeriod = {
                    start: backtestMatch[1],
                    end: backtestMatch[2]
                };
            }
            
            // 提取基准
            const benchmarkMatch = docstring.match(/基准[指数]*[：:]\s*(\S+)/);
            if (benchmarkMatch) {
                meta.benchmark = benchmarkMatch[1];
            }
            
            // 提取描述
            const descMatch = docstring.match(/策略[说明特色]*[：:]*\n?([\s\S]*?)(?=\n\n|迁移|平台|$)/);
            if (descMatch) {
                meta.description = descMatch[1].trim().replace(/^[-\d.\s]+/gm, '').trim();
            }
        }
        
        return meta;
    }
    
    /**
     * 提取代码块（函数、类、变量定义）
     */
    private extractCodeBlocks(code: string): CodeBlock[] {
        const blocks: CodeBlock[] = [];
        const lines = code.split('\n');
        
        let currentBlock: Partial<CodeBlock> | null = null;
        let blockIndent = 0;
        let inDocstring = false;
        let docstringChar = '';
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const trimmedLine = line.trim();
            const indent = line.length - line.trimStart().length;
            
            // 处理docstring
            if (trimmedLine.startsWith('"""') || trimmedLine.startsWith("'''")) {
                if (!inDocstring) {
                    inDocstring = true;
                    docstringChar = trimmedLine.substring(0, 3);
                    if (trimmedLine.endsWith(docstringChar) && trimmedLine.length > 3) {
                        inDocstring = false;
                    }
                } else if (trimmedLine.endsWith(docstringChar)) {
                    inDocstring = false;
                }
                continue;
            }
            
            if (inDocstring) continue;
            
            // 检测函数定义
            const funcMatch = trimmedLine.match(/^def\s+(\w+)\s*\(/);
            if (funcMatch) {
                // 保存之前的块
                if (currentBlock && currentBlock.startLine !== undefined) {
                    currentBlock.endLine = i - 1;
                    currentBlock.content = lines.slice(currentBlock.startLine, i).join('\n');
                    blocks.push(currentBlock as CodeBlock);
                }
                
                currentBlock = {
                    type: 'function',
                    name: funcMatch[1],
                    startLine: i,
                    endLine: i,
                    content: ''
                };
                blockIndent = indent;
                continue;
            }
            
            // 检测类定义
            const classMatch = trimmedLine.match(/^class\s+(\w+)/);
            if (classMatch) {
                if (currentBlock && currentBlock.startLine !== undefined) {
                    currentBlock.endLine = i - 1;
                    currentBlock.content = lines.slice(currentBlock.startLine, i).join('\n');
                    blocks.push(currentBlock as CodeBlock);
                }
                
                currentBlock = {
                    type: 'class',
                    name: classMatch[1],
                    startLine: i,
                    endLine: i,
                    content: ''
                };
                blockIndent = indent;
                continue;
            }
            
            // 检测全局变量
            const varMatch = trimmedLine.match(/^([A-Z_][A-Z0-9_]*)\s*=/);
            if (varMatch && indent === 0 && !currentBlock) {
                // 找到变量结束位置
                let endLine = i;
                for (let j = i + 1; j < lines.length; j++) {
                    const nextLine = lines[j];
                    const nextTrimmed = nextLine.trim();
                    const nextIndent = nextLine.length - nextLine.trimStart().length;
                    
                    if (nextTrimmed === '' || (nextIndent === 0 && !nextTrimmed.startsWith('#'))) {
                        break;
                    }
                    endLine = j;
                }
                
                blocks.push({
                    type: 'variable',
                    name: varMatch[1],
                    startLine: i,
                    endLine: endLine,
                    content: lines.slice(i, endLine + 1).join('\n')
                });
                continue;
            }
            
            // 检测块结束
            if (currentBlock && indent <= blockIndent && trimmedLine !== '' && !trimmedLine.startsWith('#')) {
                currentBlock.endLine = i - 1;
                currentBlock.content = lines.slice(currentBlock.startLine!, i).join('\n');
                blocks.push(currentBlock as CodeBlock);
                currentBlock = null;
            }
        }
        
        // 处理最后一个块
        if (currentBlock && currentBlock.startLine !== undefined) {
            currentBlock.endLine = lines.length - 1;
            currentBlock.content = lines.slice(currentBlock.startLine).join('\n');
            blocks.push(currentBlock as CodeBlock);
        }
        
        return blocks;
    }
    
    /**
     * 分类组件
     */
    private categorizeComponents(blocks: CodeBlock[]): StrategyAnalysis['components'] {
        const components: StrategyAnalysis['components'] = {
            stockSelection: [],
            timing: [],
            riskControl: [],
            execution: [],
            utilities: []
        };
        
        for (const block of blocks) {
            const name = block.name.toLowerCase();
            const content = block.content.toLowerCase();
            
            // 选股相关
            if (name.includes('select') || name.includes('filter') || name.includes('stock') ||
                content.includes('选股') || content.includes('stock_pool') || content.includes('get_index_stocks')) {
                block.category = 'selection';
                components.stockSelection.push(block);
            }
            // 择时相关
            else if (name.includes('timing') || name.includes('signal') || name.includes('market') ||
                     content.includes('择时') || content.includes('信号') || content.includes('趋势')) {
                block.category = 'timing';
                components.timing.push(block);
            }
            // 风控相关
            else if (name.includes('risk') || name.includes('stop') || name.includes('control') ||
                     content.includes('止损') || content.includes('止盈') || content.includes('风控')) {
                block.category = 'risk';
                components.riskControl.push(block);
            }
            // 执行相关
            else if (name.includes('execute') || name.includes('trade') || name.includes('order') ||
                     name.includes('handle_data') || name.includes('rebalance') ||
                     content.includes('order') || content.includes('交易')) {
                block.category = 'execution';
                components.execution.push(block);
            }
            // 工具函数
            else {
                block.category = 'util';
                components.utilities.push(block);
            }
        }
        
        return components;
    }
    
    /**
     * 分析依赖
     */
    private analyzeDependencies(code: string, lines: string[]): StrategyAnalysis['dependencies'] {
        const apis: APIUsage[] = [];
        const factors: FactorUsage[] = [];
        const indicators: IndicatorUsage[] = [];
        const imports: string[] = [];
        
        // 提取imports
        const importMatches = code.matchAll(/^(?:from\s+(\S+)\s+)?import\s+(.+)$/gm);
        for (const match of importMatches) {
            if (match[1]) {
                imports.push(`${match[1]}.${match[2]}`);
            } else {
                imports.push(match[2]);
            }
        }
        
        // 检测JoinQuant APIs
        for (const apiDef of JOINQUANT_APIS) {
            let match;
            while ((match = apiDef.pattern.exec(code)) !== null) {
                const lineNum = code.substring(0, match.index).split('\n').length;
                const contextLine = lines[lineNum - 1] || '';
                
                apis.push({
                    name: apiDef.name,
                    platform: 'joinquant',
                    line: lineNum,
                    params: {},
                    context: contextLine.trim(),
                    canConvert: true
                });
            }
            // 重置regex
            apiDef.pattern.lastIndex = 0;
        }
        
        // 检测PTrade APIs
        for (const apiDef of PTRADE_APIS) {
            let match;
            while ((match = apiDef.pattern.exec(code)) !== null) {
                const lineNum = code.substring(0, match.index).split('\n').length;
                const contextLine = lines[lineNum - 1] || '';
                
                apis.push({
                    name: apiDef.name,
                    platform: 'ptrade',
                    line: lineNum,
                    params: {},
                    context: contextLine.trim(),
                    canConvert: true
                });
            }
            apiDef.pattern.lastIndex = 0;
        }
        
        // 检测因子使用
        const factorSet = new Set<string>();
        for (const factorDef of FACTOR_PATTERNS) {
            if (factorDef.pattern.test(code)) {
                if (!factorSet.has(factorDef.name)) {
                    factorSet.add(factorDef.name);
                    factors.push({
                        name: factorDef.name,
                        type: factorDef.type as FactorUsage['type']
                    });
                }
            }
            factorDef.pattern.lastIndex = 0;
        }
        
        // 检测指标使用
        const indicatorSet = new Set<string>();
        for (const indDef of INDICATOR_PATTERNS) {
            if (indDef.pattern.test(code)) {
                if (!indicatorSet.has(indDef.name)) {
                    indicatorSet.add(indDef.name);
                    indicators.push({
                        name: indDef.name,
                        type: indDef.type as IndicatorUsage['type']
                    });
                }
            }
            indDef.pattern.lastIndex = 0;
        }
        
        return { apis, factors, indicators, imports };
    }
    
    /**
     * 计算兼容性得分
     */
    private calculateCompatibility(apis: APIUsage[]): StrategyAnalysis['compatibility'] {
        // 统计各平台API
        const joinquantApis = apis.filter(a => a.platform === 'joinquant');
        const ptradeApis = apis.filter(a => a.platform === 'ptrade');
        
        // 确定源平台
        let sourcePlatform: Platform = 'joinquant';
        if (ptradeApis.length > joinquantApis.length) {
            sourcePlatform = 'ptrade';
        }
        
        // 计算兼容性
        const calculateScore = (targetPlatform: Platform): CompatibilityScore => {
            if (targetPlatform === sourcePlatform) {
                return {
                    score: 100,
                    level: 'full',
                    issues: [],
                    suggestions: []
                };
            }
            
            const issues: CompatibilityScore['issues'] = [];
            const sourceApis = sourcePlatform === 'joinquant' ? joinquantApis : ptradeApis;
            
            for (const api of sourceApis) {
                // 检查是否有对应的转换
                const hasMapping = this.hasAPIMapping(api.name, sourcePlatform, targetPlatform);
                
                if (!hasMapping) {
                    issues.push({
                        severity: 'error',
                        line: api.line,
                        message: `API '${api.name}' 在 ${targetPlatform} 中没有直接对应`,
                        api: api.name,
                        suggestion: `需要手动实现或寻找替代方案`
                    });
                } else {
                    issues.push({
                        severity: 'info',
                        line: api.line,
                        message: `API '${api.name}' 可自动转换`,
                        api: api.name,
                        suggestion: `将自动转换为对应API`
                    });
                }
            }
            
            const errorCount = issues.filter(i => i.severity === 'error').length;
            const totalApis = sourceApis.length || 1;
            const score = Math.max(0, 100 - (errorCount / totalApis) * 100);
            
            let level: CompatibilityScore['level'];
            if (score >= 95) level = 'full';
            else if (score >= 80) level = 'high';
            else if (score >= 60) level = 'medium';
            else if (score >= 30) level = 'low';
            else level = 'none';
            
            return {
                score: Math.round(score),
                level,
                issues,
                suggestions: this.generateSuggestions(issues, targetPlatform)
            };
        };
        
        return {
            sourcePlatform,
            joinquant: calculateScore('joinquant'),
            ptrade: calculateScore('ptrade'),
            qmt: calculateScore('qmt')
        };
    }
    
    /**
     * 检查是否有API映射
     */
    private hasAPIMapping(apiName: string, source: Platform, target: Platform): boolean {
        const mappings: Record<string, any> = {
            'get_price': { joinquant: 'get_price', ptrade: 'get_history', qmt: 'ContextInfo.get_market_data' },
            'get_current_data': { joinquant: 'get_current_data', ptrade: 'get_snapshot', qmt: 'ContextInfo.get_full_tick' },
            'order_target_value': { joinquant: 'order_target_value', ptrade: 'order_target_percent', qmt: 'order_target_volume' },
            'order': { joinquant: 'order', ptrade: 'order_lots', qmt: 'order_volume' },
            'set_benchmark': { joinquant: 'set_benchmark', ptrade: null, qmt: null },
            'log.info': { joinquant: 'log.info', ptrade: 'print', qmt: 'print' },
            'run_daily': { joinquant: 'run_daily', ptrade: null, qmt: null },
            'get_index_stocks': { joinquant: 'get_index_stocks', ptrade: null, qmt: 'ContextInfo.get_stock_list_in_sector' },
        };
        
        const mapping = mappings[apiName];
        if (!mapping) return false;
        return mapping[target] !== null;
    }
    
    /**
     * 生成优化建议
     */
    private generateSuggestions(issues: CompatibilityScore['issues'], targetPlatform: Platform): string[] {
        const suggestions: string[] = [];
        const errorApis = issues.filter(i => i.severity === 'error').map(i => i.api);
        
        if (errorApis.length === 0) {
            suggestions.push('代码可直接转换，无需手动修改');
        } else {
            suggestions.push(`需要处理 ${errorApis.length} 个不兼容的API调用`);
            
            if (errorApis.includes('run_daily')) {
                suggestions.push('PTrade不支持run_daily，需要在on_bar中实现日频逻辑');
            }
            
            if (errorApis.includes('set_benchmark')) {
                suggestions.push('PTrade无需设置基准，可删除此行');
            }
            
            if (targetPlatform === 'ptrade') {
                suggestions.push('需要添加 on_bar() 作为入口函数');
                suggestions.push('建议添加 initialize() 和 before_trading_start() 函数');
            }
        }
        
        return suggestions;
    }
    
    /**
     * 计算统计信息
     */
    private calculateStats(code: string, blocks: CodeBlock[]): StrategyAnalysis['stats'] {
        const lines = code.split('\n');
        const totalLines = lines.length;
        
        let commentLines = 0;
        let codeLines = 0;
        let inDocstring = false;
        
        for (const line of lines) {
            const trimmed = line.trim();
            
            if (trimmed.startsWith('"""') || trimmed.startsWith("'''")) {
                if (!inDocstring) {
                    inDocstring = true;
                    if (trimmed.length > 3 && (trimmed.endsWith('"""') || trimmed.endsWith("'''"))) {
                        inDocstring = false;
                    }
                } else {
                    inDocstring = false;
                }
                commentLines++;
                continue;
            }
            
            if (inDocstring) {
                commentLines++;
                continue;
            }
            
            if (trimmed.startsWith('#') || trimmed === '') {
                commentLines++;
            } else {
                codeLines++;
            }
        }
        
        const functionCount = blocks.filter(b => b.type === 'function').length;
        const classCount = blocks.filter(b => b.type === 'class').length;
        
        // 计算复杂度
        let complexity: 'low' | 'medium' | 'high';
        if (functionCount <= 5 && totalLines <= 200) {
            complexity = 'low';
        } else if (functionCount <= 15 && totalLines <= 500) {
            complexity = 'medium';
        } else {
            complexity = 'high';
        }
        
        return {
            totalLines,
            codeLines,
            commentLines,
            functionCount,
            classCount,
            complexity
        };
    }
}

// 导出单例
export const codeAnalyzer = new CodeAnalyzer();

