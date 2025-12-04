/**
 * 平台适配器
 * ==========
 * 
 * 在不同量化平台间转换策略代码
 * 支持: JoinQuant ↔ PTrade ↔ QMT
 */

import {
    Platform,
    APIMapping,
    ConversionResult,
    CodeChange,
    StrategyAnalysis
} from '../types';

// ============================================================
// API映射定义
// ============================================================

const API_MAPPINGS: APIMapping[] = [
    // ============ 数据获取 ============
    {
        source: { platform: 'joinquant', api: 'get_price', signature: 'get_price(security, start_date, end_date, frequency, fields, skip_paused, fq, count, panel, fill_paused)' },
        target: { platform: 'ptrade', api: 'get_history', signature: 'get_history(count, frequency, field, security_list, skip_paused, fq, bar_count)' },
        paramMapping: {
            'security': 'security_list',
            'count': 'count',
            'frequency': (v) => v === '1d' ? 'daily' : v,
            'fields': 'field',
            'skip_paused': 'skip_paused',
            'fq': 'fq'
        },
        notes: [
            'PTrade的get_history返回格式与JoinQuant不同',
            '需要处理返回数据的格式转换',
            'PTrade不支持start_date/end_date参数，需要用count替代'
        ],
        examples: {
            before: `df = get_price('000001.XSHE', count=20, end_date='2024-01-01', frequency='daily', fields=['close', 'volume'])`,
            after: `df = get_history(count=20, frequency='daily', field=['close', 'volume'], security_list=['000001.XSHE'])`
        }
    },
    {
        source: { platform: 'joinquant', api: 'get_current_data', signature: 'get_current_data(security)' },
        target: { platform: 'ptrade', api: 'get_snapshot', signature: 'get_snapshot(stock_code)' },
        paramMapping: {
            'security': 'stock_code'
        },
        notes: ['返回数据结构不同，需要适配字段名'],
        examples: {
            before: `current = get_current_data('000001.XSHE')`,
            after: `current = get_snapshot('000001.XSHE')`
        }
    },
    {
        source: { platform: 'joinquant', api: 'history', signature: 'history(count, unit, field, security_list, df, skip_paused, fq)' },
        target: { platform: 'ptrade', api: 'get_history', signature: 'get_history(count, frequency, field, security_list, skip_paused, fq, bar_count)' },
        paramMapping: {
            'count': 'count',
            'unit': (v) => v === '1d' ? 'daily' : v === '1m' ? 'minute' : v,
            'field': 'field',
            'security_list': 'security_list',
            'skip_paused': 'skip_paused',
            'fq': 'fq'
        },
        notes: ['unit参数需要转换为frequency'],
        examples: {
            before: `df = history(20, '1d', 'close', ['000001.XSHE'])`,
            after: `df = get_history(count=20, frequency='daily', field='close', security_list=['000001.XSHE'])`
        }
    },
    {
        source: { platform: 'joinquant', api: 'get_index_stocks', signature: 'get_index_stocks(index_symbol, date)' },
        target: { platform: 'ptrade', api: 'get_index_stocks', signature: 'get_index_stocks(index_code)' },
        paramMapping: {
            'index_symbol': (v: string) => v.replace('.XSHG', '.SH').replace('.XSHE', '.SZ')
        },
        notes: ['股票代码后缀需要转换: .XSHG→.SH, .XSHE→.SZ'],
        examples: {
            before: `stocks = get_index_stocks('000300.XSHG')`,
            after: `stocks = get_index_stocks('000300.SH')`
        }
    },
    
    // ============ 交易执行 ============
    {
        source: { platform: 'joinquant', api: 'order_target_value', signature: 'order_target_value(security, value)' },
        target: { platform: 'ptrade', api: 'order_target_percent', signature: 'order_target_percent(stock_code, percent)' },
        paramMapping: {
            'security': 'stock_code',
            'value': (v, ctx) => `${v} / context.portfolio.total_value`  // 需要转换为百分比
        },
        notes: [
            'PTrade使用百分比而非金额',
            '需要计算: percent = value / portfolio.total_value'
        ],
        examples: {
            before: `order_target_value('000001.XSHE', 100000)`,
            after: `order_target_percent('000001.XSHE', 100000 / context.portfolio.total_value)`
        }
    },
    {
        source: { platform: 'joinquant', api: 'order', signature: 'order(security, amount, style)' },
        target: { platform: 'ptrade', api: 'order_lots', signature: 'order_lots(stock_code, lots, limit_price)' },
        paramMapping: {
            'security': 'stock_code',
            'amount': (v) => `${v} // 100`  // 转换为手数
        },
        notes: ['PTrade使用手数(100股=1手)而非股数'],
        examples: {
            before: `order('000001.XSHE', 1000)`,
            after: `order_lots('000001.XSHE', 10)`
        }
    },
    {
        source: { platform: 'joinquant', api: 'order_target', signature: 'order_target(security, amount)' },
        target: { platform: 'ptrade', api: 'order_target_volume', signature: 'order_target_volume(stock_code, volume)' },
        paramMapping: {
            'security': 'stock_code',
            'amount': 'volume'
        },
        notes: ['参数名不同但逻辑相同'],
        examples: {
            before: `order_target('000001.XSHE', 1000)`,
            after: `order_target_volume('000001.XSHE', 1000)`
        }
    },
    
    // ============ 设置相关 ============
    {
        source: { platform: 'joinquant', api: 'set_benchmark', signature: 'set_benchmark(security)' },
        target: { platform: 'ptrade', api: '', signature: '' },
        paramMapping: {},
        notes: ['PTrade不需要设置基准，此行可删除或注释'],
        examples: {
            before: `set_benchmark('000300.XSHG')`,
            after: `# set_benchmark('000300.XSHG')  # PTrade不需要此设置`
        }
    },
    {
        source: { platform: 'joinquant', api: 'set_option', signature: 'set_option(option_name, value)' },
        target: { platform: 'ptrade', api: '', signature: '' },
        paramMapping: {},
        notes: ['PTrade配置方式不同，大部分选项在策略配置文件中设置'],
        examples: {
            before: `set_option('use_real_price', True)`,
            after: `# PTrade在配置文件中设置use_real_price`
        }
    },
    {
        source: { platform: 'joinquant', api: 'set_slippage', signature: 'set_slippage(slippage)' },
        target: { platform: 'ptrade', api: '', signature: '' },
        paramMapping: {},
        notes: ['PTrade滑点在交易配置中设置'],
        examples: {
            before: `set_slippage(PriceRelatedSlippage(0.002))`,
            after: `# PTrade在交易配置中设置滑点`
        }
    },
    {
        source: { platform: 'joinquant', api: 'set_order_cost', signature: 'set_order_cost(cost, type)' },
        target: { platform: 'ptrade', api: '', signature: '' },
        paramMapping: {},
        notes: ['PTrade费用在账户配置中设置'],
        examples: {
            before: `set_order_cost(OrderCost(open_tax=0, close_tax=0.001, open_commission=0.0003, close_commission=0.0003), type='stock')`,
            after: `# PTrade在账户配置中设置交易费用`
        }
    },
    
    // ============ 日志 ============
    {
        source: { platform: 'joinquant', api: 'log.info', signature: 'log.info(msg)' },
        target: { platform: 'ptrade', api: 'print', signature: 'print(msg)' },
        paramMapping: { 'msg': 'msg' },
        notes: ['PTrade使用print输出日志'],
        examples: {
            before: `log.info('策略开始运行')`,
            after: `print('[INFO] 策略开始运行')`
        }
    },
    {
        source: { platform: 'joinquant', api: 'log.warn', signature: 'log.warn(msg)' },
        target: { platform: 'ptrade', api: 'print', signature: 'print(msg)' },
        paramMapping: { 'msg': 'msg' },
        notes: ['建议添加[WARN]前缀'],
        examples: {
            before: `log.warn('风险提示')`,
            after: `print('[WARN] 风险提示')`
        }
    },
    {
        source: { platform: 'joinquant', api: 'log.error', signature: 'log.error(msg)' },
        target: { platform: 'ptrade', api: 'print', signature: 'print(msg)' },
        paramMapping: { 'msg': 'msg' },
        notes: ['建议添加[ERROR]前缀'],
        examples: {
            before: `log.error('执行失败')`,
            after: `print('[ERROR] 执行失败')`
        }
    },
    
    // ============ 定时任务 ============
    {
        source: { platform: 'joinquant', api: 'run_daily', signature: 'run_daily(func, time)' },
        target: { platform: 'ptrade', api: '', signature: '' },
        paramMapping: {},
        notes: [
            'PTrade不支持run_daily',
            '需要在on_bar中根据时间判断执行',
            '示例: if context.current_dt.hour == 9 and context.current_dt.minute == 30:'
        ],
        examples: {
            before: `run_daily(my_func, '09:30')`,
            after: `# 在on_bar中添加时间判断:\n# if context.current_dt.strftime('%H:%M') == '09:30':\n#     my_func(context)`
        }
    },
];

// ============================================================
// 代码模板
// ============================================================

const PTRADE_TEMPLATE = `# -*- coding: utf-8 -*-
"""
{strategy_name} - PTrade版本
============================

原平台: JoinQuant
转换时间: {convert_time}
转换工具: TRQuant Strategy Optimizer

注意事项:
---------
1. 请检查股票代码后缀是否正确(.XSHG→.SH, .XSHE→.SZ)
2. 确认交易费用和滑点配置
3. 测试数据获取函数返回格式
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ============================================================
# 全局变量
# ============================================================

{global_variables}

# ============================================================
# 初始化函数
# ============================================================

def initialize(context):
    """
    策略初始化 (PTrade版本)
    在策略启动时调用一次
    """
{initialize_code}

# ============================================================
# 盘前处理
# ============================================================

def before_trading_start(context, data):
    """
    每日盘前调用
    用于数据准备和状态更新
    """
{before_trading_code}

# ============================================================
# 交易逻辑 (主入口)
# ============================================================

def on_bar(context, data):
    """
    PTrade主入口函数
    每个bar调用一次
    """
    current_time = context.current_dt.strftime('%H:%M')
    
    # 开盘执行 (对应JoinQuant的run_daily 09:30)
    if current_time == '09:31':
        handle_open(context, data)
    
    # 盘中执行
    handle_bar(context, data)
    
    # 收盘执行 (对应JoinQuant的run_daily 14:50)
    if current_time == '14:50':
        handle_close(context, data)

def handle_open(context, data):
    """开盘执行逻辑"""
{handle_open_code}

def handle_bar(context, data):
    """盘中执行逻辑"""
{handle_bar_code}

def handle_close(context, data):
    """收盘执行逻辑"""
{handle_close_code}

# ============================================================
# 选股模块
# ============================================================

{selection_functions}

# ============================================================
# 风控模块
# ============================================================

{risk_functions}

# ============================================================
# 工具函数
# ============================================================

{utility_functions}
`;

// ============================================================
// 平台适配器类
// ============================================================

export class PlatformAdapter {
    private mappings: APIMapping[] = API_MAPPINGS;
    
    /**
     * 转换代码到目标平台
     */
    convert(
        code: string,
        analysis: StrategyAnalysis,
        targetPlatform: Platform
    ): ConversionResult {
        const changes: CodeChange[] = [];
        const warnings: string[] = [];
        const errors: string[] = [];
        
        let convertedCode = code;
        const sourcePlatform = analysis.compatibility.sourcePlatform;
        
        if (sourcePlatform === targetPlatform) {
            return {
                success: true,
                targetPlatform,
                originalCode: code,
                convertedCode: code,
                changes: [],
                warnings: ['源平台与目标平台相同，无需转换'],
                errors: [],
                stats: {
                    totalChanges: 0,
                    apiChanges: 0,
                    structureChanges: 0,
                    addedLines: 0,
                    removedLines: 0
                }
            };
        }
        
        // JoinQuant → PTrade
        if (sourcePlatform === 'joinquant' && targetPlatform === 'ptrade') {
            return this.convertJoinQuantToPTrade(code, analysis);
        }
        
        // PTrade → JoinQuant
        if (sourcePlatform === 'ptrade' && targetPlatform === 'joinquant') {
            return this.convertPTradeToJoinQuant(code, analysis);
        }
        
        // 其他转换暂不支持
        return {
            success: false,
            targetPlatform,
            originalCode: code,
            convertedCode: code,
            changes: [],
            warnings: [],
            errors: [`暂不支持 ${sourcePlatform} → ${targetPlatform} 的转换`],
            stats: {
                totalChanges: 0,
                apiChanges: 0,
                structureChanges: 0,
                addedLines: 0,
                removedLines: 0
            }
        };
    }
    
    /**
     * JoinQuant → PTrade 转换
     */
    private convertJoinQuantToPTrade(
        code: string,
        analysis: StrategyAnalysis
    ): ConversionResult {
        const changes: CodeChange[] = [];
        const warnings: string[] = [];
        const errors: string[] = [];
        
        let convertedCode = code;
        const lines = code.split('\n');
        
        // 1. 替换API调用
        for (const api of analysis.dependencies.apis) {
            const mapping = this.findMapping(api.name, 'joinquant', 'ptrade');
            
            if (mapping) {
                if (mapping.target.api === '') {
                    // 需要删除或注释的API
                    const lineContent = lines[api.line - 1];
                    const newContent = `# ${lineContent.trim()}  # PTrade不需要此设置`;
                    
                    convertedCode = this.replaceLine(convertedCode, api.line, newContent);
                    changes.push({
                        type: 'api_replace',
                        line: api.line,
                        original: lineContent.trim(),
                        converted: newContent,
                        reason: mapping.notes?.[0] || 'PTrade不支持此API'
                    });
                } else {
                    // 替换API
                    const regex = new RegExp(`\\b${api.name}\\s*\\(`, 'g');
                    const newApi = `${mapping.target.api}(`;
                    
                    convertedCode = convertedCode.replace(regex, newApi);
                    changes.push({
                        type: 'api_replace',
                        line: api.line,
                        original: api.name,
                        converted: mapping.target.api,
                        reason: `API转换: ${api.name} → ${mapping.target.api}`
                    });
                }
                
                if (mapping.notes) {
                    warnings.push(...mapping.notes);
                }
            } else {
                errors.push(`第${api.line}行: API '${api.name}' 无法自动转换`);
            }
        }
        
        // 2. 转换股票代码后缀
        convertedCode = convertedCode.replace(/\.XSHG/g, '.SH');
        convertedCode = convertedCode.replace(/\.XSHE/g, '.SZ');
        changes.push({
            type: 'param_change',
            line: 0,
            original: '.XSHG/.XSHE',
            converted: '.SH/.SZ',
            reason: '股票代码后缀转换'
        });
        
        // 3. 替换log调用
        convertedCode = convertedCode.replace(/log\.info\s*\(\s*f?(['"])/g, "print('[INFO] ' + $1");
        convertedCode = convertedCode.replace(/log\.info\s*\(/g, "print('[INFO]', ");
        convertedCode = convertedCode.replace(/log\.warn\s*\(\s*f?(['"])/g, "print('[WARN] ' + $1");
        convertedCode = convertedCode.replace(/log\.warn\s*\(/g, "print('[WARN]', ");
        convertedCode = convertedCode.replace(/log\.error\s*\(\s*f?(['"])/g, "print('[ERROR] ' + $1");
        convertedCode = convertedCode.replace(/log\.error\s*\(/g, "print('[ERROR]', ");
        
        // 4. 添加PTrade结构
        if (!convertedCode.includes('def on_bar')) {
            warnings.push('需要添加 on_bar() 入口函数');
            
            // 在文件末尾添加on_bar框架
            convertedCode += `

# ============================================================
# PTrade入口函数 (自动生成)
# ============================================================

def on_bar(context, data):
    """
    PTrade主入口函数
    请将handle_data中的逻辑迁移到此函数
    """
    handle_data(context, data)
`;
            changes.push({
                type: 'structure_change',
                line: 0,
                original: '',
                converted: 'def on_bar(context, data)',
                reason: '添加PTrade入口函数'
            });
        }
        
        // 5. 处理run_daily
        const runDailyMatches = code.matchAll(/run_daily\s*\(\s*(\w+)\s*,\s*['"](\d{2}:\d{2})['"]\s*\)/g);
        for (const match of runDailyMatches) {
            const funcName = match[1];
            const time = match[2];
            warnings.push(`run_daily(${funcName}, '${time}') 需要在on_bar中用时间判断实现`);
        }
        
        // 6. 更新docstring
        const now = new Date().toLocaleString('zh-CN');
        const newDocstring = `"""
${analysis.meta.name} - PTrade版本
============================

原平台: JoinQuant
转换时间: ${now}
转换工具: TRQuant Strategy Optimizer

原始信息:
---------
${analysis.meta.description || '无描述'}

注意事项:
---------
1. 请检查股票代码后缀是否正确
2. 确认交易费用和滑点配置
3. 测试数据获取函数返回格式
"""`;
        
        // 替换原docstring
        convertedCode = convertedCode.replace(/^[\s\S]*?"""[\s\S]*?"""/, newDocstring);
        
        const success = errors.length === 0;
        
        return {
            success,
            targetPlatform: 'ptrade',
            originalCode: code,
            convertedCode,
            changes,
            warnings,
            errors,
            stats: {
                totalChanges: changes.length,
                apiChanges: changes.filter(c => c.type === 'api_replace').length,
                structureChanges: changes.filter(c => c.type === 'structure_change').length,
                addedLines: changes.filter(c => c.type === 'add').length,
                removedLines: changes.filter(c => c.type === 'remove').length
            }
        };
    }
    
    /**
     * PTrade → JoinQuant 转换
     */
    private convertPTradeToJoinQuant(
        code: string,
        analysis: StrategyAnalysis
    ): ConversionResult {
        const changes: CodeChange[] = [];
        const warnings: string[] = [];
        
        let convertedCode = code;
        
        // 1. 转换股票代码后缀
        convertedCode = convertedCode.replace(/\.SH\b/g, '.XSHG');
        convertedCode = convertedCode.replace(/\.SZ\b/g, '.XSHE');
        
        // 2. 替换API
        convertedCode = convertedCode.replace(/\bget_history\s*\(/g, 'get_price(');
        convertedCode = convertedCode.replace(/\bget_snapshot\s*\(/g, 'get_current_data(');
        convertedCode = convertedCode.replace(/\border_target_percent\s*\(/g, 'order_target_value(');
        convertedCode = convertedCode.replace(/\border_lots\s*\(/g, 'order(');
        
        // 3. 替换print为log
        convertedCode = convertedCode.replace(/print\s*\(\s*\[INFO\]\s*/g, 'log.info(');
        convertedCode = convertedCode.replace(/print\s*\(\s*\[WARN\]\s*/g, 'log.warn(');
        convertedCode = convertedCode.replace(/print\s*\(\s*\[ERROR\]\s*/g, 'log.error(');
        
        warnings.push('order_target_percent需要手动转换为金额形式');
        warnings.push('on_bar逻辑需要拆分到handle_data和run_daily');
        
        return {
            success: true,
            targetPlatform: 'joinquant',
            originalCode: code,
            convertedCode,
            changes,
            warnings,
            errors: [],
            stats: {
                totalChanges: changes.length,
                apiChanges: changes.filter(c => c.type === 'api_replace').length,
                structureChanges: 0,
                addedLines: 0,
                removedLines: 0
            }
        };
    }
    
    /**
     * 查找API映射
     */
    private findMapping(
        apiName: string,
        source: Platform,
        target: Platform
    ): APIMapping | undefined {
        return this.mappings.find(m => 
            m.source.platform === source &&
            m.source.api === apiName
        );
    }
    
    /**
     * 替换指定行
     */
    private replaceLine(code: string, lineNum: number, newContent: string): string {
        const lines = code.split('\n');
        if (lineNum > 0 && lineNum <= lines.length) {
            const indent = lines[lineNum - 1].match(/^\s*/)?.[0] || '';
            lines[lineNum - 1] = indent + newContent;
        }
        return lines.join('\n');
    }
    
    /**
     * 获取所有API映射
     */
    getAllMappings(): APIMapping[] {
        return this.mappings;
    }
    
    /**
     * 添加自定义映射
     */
    addMapping(mapping: APIMapping): void {
        this.mappings.push(mapping);
    }
}

// 导出单例
export const platformAdapter = new PlatformAdapter();






