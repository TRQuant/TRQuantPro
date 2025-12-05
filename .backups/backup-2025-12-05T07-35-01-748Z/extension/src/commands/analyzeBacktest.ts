/**
 * 回测分析命令
 * ==============
 * 
 * 功能：
 * - 分析回测结果文件
 * - 提供诊断和优化建议
 * - 生成详细分析报告
 * 
 * 遵循：
 * - 单一职责原则
 * - 命令模式
 */

import * as vscode from 'vscode';
import * as path from 'path';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';
import { ErrorHandler } from '../utils/errors';
import { BacktestResult, BacktestMetrics } from '../types';

const MODULE = 'AnalyzeBacktest';

/**
 * 执行回测分析命令
 */
export async function analyzeBacktest(
    client: TRQuantClient,
    context: vscode.ExtensionContext
): Promise<void> {
    logger.info('执行回测分析命令', MODULE);

    try {
        // 选择输入方式
        const inputMethod = await vscode.window.showQuickPick([
            { label: '📂 从文件导入', value: 'file', description: '选择回测结果文件' },
            { label: '📝 手动输入', value: 'manual', description: '输入关键指标' },
            { label: '📋 从剪贴板', value: 'clipboard', description: '从剪贴板读取指标' }
        ], {
            placeHolder: '选择回测数据来源'
        });

        if (!inputMethod) return;

        let metrics: BacktestMetrics | undefined;

        switch (inputMethod.value) {
            case 'file':
                metrics = await loadFromFile();
                break;
            case 'manual':
                metrics = await manualInput();
                break;
            case 'clipboard':
                metrics = await loadFromClipboard();
                break;
        }

        if (!metrics) {
            vscode.window.showWarningMessage('未能获取回测数据');
            return;
        }

        // 分析回测结果
        await analyzeWithProgress(client, context, metrics);

    } catch (error) {
        ErrorHandler.handle(error, MODULE);
    }
}

/**
 * 从文件加载回测结果
 */
async function loadFromFile(): Promise<BacktestMetrics | undefined> {
    const files = await vscode.window.showOpenDialog({
        canSelectMany: false,
        filters: {
            'JSON文件': ['json'],
            'CSV文件': ['csv'],
            '所有文件': ['*']
        },
        title: '选择回测结果文件'
    });

    if (!files || files.length === 0) return undefined;

    const filePath = files[0].fsPath;
    const content = await vscode.workspace.fs.readFile(files[0]);
    const text = Buffer.from(content).toString('utf-8');

    try {
        if (filePath.endsWith('.json')) {
            const data = JSON.parse(text);
            return extractMetrics(data);
        } else if (filePath.endsWith('.csv')) {
            return parseCSVMetrics(text);
        }
    } catch (error) {
        logger.error(`解析文件失败: ${error}`, MODULE);
        vscode.window.showErrorMessage('文件解析失败，请检查格式');
    }

    return undefined;
}

/**
 * 从剪贴板加载
 */
async function loadFromClipboard(): Promise<BacktestMetrics | undefined> {
    const text = await vscode.env.clipboard.readText();
    
    if (!text.trim()) {
        vscode.window.showWarningMessage('剪贴板为空');
        return undefined;
    }

    try {
        const data = JSON.parse(text);
        return extractMetrics(data);
    } catch {
        // 尝试解析为CSV格式
        try {
            return parseCSVMetrics(text);
        } catch {
            vscode.window.showErrorMessage('无法解析剪贴板内容');
            return undefined;
        }
    }
}

/**
 * 手动输入指标
 */
async function manualInput(): Promise<BacktestMetrics | undefined> {
    const totalReturn = await vscode.window.showInputBox({
        prompt: '总收益率 (%)',
        value: '0',
        validateInput: v => isNaN(parseFloat(v)) ? '请输入数字' : null
    });
    if (!totalReturn) return undefined;

    const sharpeRatio = await vscode.window.showInputBox({
        prompt: '夏普比率',
        value: '0',
        validateInput: v => isNaN(parseFloat(v)) ? '请输入数字' : null
    });
    if (!sharpeRatio) return undefined;

    const maxDrawdown = await vscode.window.showInputBox({
        prompt: '最大回撤 (%)',
        value: '0',
        validateInput: v => isNaN(parseFloat(v)) ? '请输入数字' : null
    });
    if (!maxDrawdown) return undefined;

    const winRate = await vscode.window.showInputBox({
        prompt: '胜率 (%)',
        value: '50',
        validateInput: v => isNaN(parseFloat(v)) ? '请输入数字' : null
    });
    if (!winRate) return undefined;

    const tradeCount = await vscode.window.showInputBox({
        prompt: '交易次数',
        value: '0',
        validateInput: v => isNaN(parseInt(v)) ? '请输入整数' : null
    });
    if (!tradeCount) return undefined;

    return {
        total_return: parseFloat(totalReturn) / 100,
        annual_return: parseFloat(totalReturn) / 100, // 简化处理
        sharpe_ratio: parseFloat(sharpeRatio),
        max_drawdown: parseFloat(maxDrawdown) / 100,
        win_rate: parseFloat(winRate) / 100,
        trade_count: parseInt(tradeCount),
        profit_loss_ratio: 1.0 // 默认值
    };
}

/**
 * 从数据中提取指标
 */
function extractMetrics(data: any): BacktestMetrics {
    return {
        total_return: data.total_return ?? data.totalReturn ?? data.return ?? 0,
        annual_return: data.annual_return ?? data.annualReturn ?? data.cagr ?? 0,
        sharpe_ratio: data.sharpe_ratio ?? data.sharpeRatio ?? data.sharpe ?? 0,
        max_drawdown: data.max_drawdown ?? data.maxDrawdown ?? data.mdd ?? 0,
        win_rate: data.win_rate ?? data.winRate ?? 0,
        trade_count: data.trade_count ?? data.tradeCount ?? data.trades ?? 0,
        profit_loss_ratio: data.profit_loss_ratio ?? data.plRatio ?? 1.0
    };
}

/**
 * 解析CSV格式指标
 */
function parseCSVMetrics(text: string): BacktestMetrics {
    const lines = text.trim().split('\n');
    const metrics: Record<string, number> = {};

    for (const line of lines) {
        const [key, value] = line.split(/[,\t:=]/);
        if (key && value) {
            metrics[key.trim().toLowerCase().replace(/\s+/g, '_')] = parseFloat(value.trim());
        }
    }

    return extractMetrics(metrics);
}

/**
 * 带进度条分析
 */
async function analyzeWithProgress(
    client: TRQuantClient,
    context: vscode.ExtensionContext,
    metrics: BacktestMetrics
): Promise<void> {
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "TRQuant",
        cancellable: false
    }, async (progress) => {
        progress.report({ message: '分析回测结果...', increment: 0 });

        const result = await client.analyzeBacktest({
            backtest_data: { metrics }
        });

        progress.report({ increment: 60 });

        if (!result.ok || !result.data) {
            // 使用本地分析
            const localResult = analyzeLocally(metrics);
            showAnalysisPanel(context, metrics, localResult);
        } else {
            showAnalysisPanel(context, metrics, result.data);
        }

        progress.report({ increment: 40 });
    });
}

/**
 * 本地分析回测结果
 */
function analyzeLocally(metrics: BacktestMetrics): BacktestResult {
    const diagnosis: string[] = [];
    const suggestions: string[] = [];

    // 分析总收益
    if (metrics.total_return < 0) {
        diagnosis.push('⚠️ 策略亏损，需要全面检视');
        suggestions.push('检查入场信号是否过于激进');
        suggestions.push('考虑增加更多过滤条件');
    } else if (metrics.total_return < 0.1) {
        diagnosis.push('💡 收益较低，存在优化空间');
        suggestions.push('尝试调整因子权重');
    } else if (metrics.total_return > 0.5) {
        diagnosis.push('✅ 收益表现优秀');
    }

    // 分析夏普比率
    if (metrics.sharpe_ratio < 0.5) {
        diagnosis.push('⚠️ 夏普比率偏低，风险调整收益不佳');
        suggestions.push('增加止损条件或降低仓位');
    } else if (metrics.sharpe_ratio > 2) {
        diagnosis.push('✅ 夏普比率优秀，策略质量高');
    } else {
        diagnosis.push('💡 夏普比率一般，可以优化');
    }

    // 分析最大回撤
    if (metrics.max_drawdown > 0.3) {
        diagnosis.push('⚠️ 最大回撤过大，风控需要加强');
        suggestions.push('降低单票仓位至5%以下');
        suggestions.push('增加组合分散度');
    } else if (metrics.max_drawdown > 0.2) {
        diagnosis.push('💡 最大回撤中等，建议优化');
        suggestions.push('考虑增加动态止损');
    } else {
        diagnosis.push('✅ 最大回撤控制良好');
    }

    // 分析胜率
    if (metrics.win_rate < 0.4) {
        diagnosis.push('⚠️ 胜率偏低');
        suggestions.push('优化选股条件');
        suggestions.push('增加确认信号');
    } else if (metrics.win_rate > 0.6) {
        diagnosis.push('✅ 胜率较高');
    }

    // 分析交易频率
    if (metrics.trade_count < 10) {
        diagnosis.push('💡 交易次数较少，统计意义有限');
        suggestions.push('延长回测周期');
    } else if (metrics.trade_count > 500) {
        diagnosis.push('💡 交易频繁，注意交易成本');
        suggestions.push('考虑降低换仓频率');
    }

    // 综合评分
    const score = calculateScore(metrics);
    if (score >= 80) {
        diagnosis.unshift('🏆 策略综合评分: 优秀 (' + score + '/100)');
    } else if (score >= 60) {
        diagnosis.unshift('📊 策略综合评分: 良好 (' + score + '/100)');
    } else if (score >= 40) {
        diagnosis.unshift('📋 策略综合评分: 一般 (' + score + '/100)');
    } else {
        diagnosis.unshift('⚠️ 策略综合评分: 较差 (' + score + '/100)');
    }

    return {
        metrics,
        trades: [],
        diagnosis,
        suggestions: suggestions.length > 0 ? suggestions : ['策略表现良好，保持观察']
    };
}

/**
 * 计算综合评分
 */
function calculateScore(metrics: BacktestMetrics): number {
    let score = 50; // 基础分

    // 收益评分 (最多30分)
    if (metrics.total_return > 0.5) score += 30;
    else if (metrics.total_return > 0.2) score += 20;
    else if (metrics.total_return > 0) score += 10;
    else score -= 20;

    // 夏普评分 (最多25分)
    if (metrics.sharpe_ratio > 2) score += 25;
    else if (metrics.sharpe_ratio > 1) score += 15;
    else if (metrics.sharpe_ratio > 0.5) score += 5;
    else score -= 10;

    // 回撤评分 (最多25分)
    if (metrics.max_drawdown < 0.1) score += 25;
    else if (metrics.max_drawdown < 0.2) score += 15;
    else if (metrics.max_drawdown < 0.3) score += 5;
    else score -= 15;

    // 胜率评分 (最多20分)
    if (metrics.win_rate > 0.6) score += 20;
    else if (metrics.win_rate > 0.5) score += 10;
    else if (metrics.win_rate > 0.4) score += 0;
    else score -= 10;

    return Math.max(0, Math.min(100, score));
}

/**
 * 显示分析面板
 */
function showAnalysisPanel(
    context: vscode.ExtensionContext,
    metrics: BacktestMetrics,
    result: BacktestResult
): void {
    const panel = vscode.window.createWebviewPanel(
        'trquantBacktestAnalysis',
        '📊 回测分析报告',
        vscode.ViewColumn.Beside,
        { enableScripts: true }
    );

    panel.webview.html = generateAnalysisHtml(metrics, result);

    panel.webview.onDidReceiveMessage(
        async (message) => {
            switch (message.command) {
                case 'copyReport':
                    const report = generateTextReport(metrics, result);
                    await vscode.env.clipboard.writeText(report);
                    vscode.window.showInformationMessage('报告已复制到剪贴板');
                    break;
                case 'optimizeStrategy':
                    vscode.commands.executeCommand('trquant.generateStrategy');
                    break;
            }
        },
        undefined,
        context.subscriptions
    );
}

/**
 * 生成分析HTML
 */
function generateAnalysisHtml(metrics: BacktestMetrics, result: BacktestResult): string {
    const score = calculateScore(metrics);
    const scoreColor = score >= 80 ? '#10b981' : score >= 60 ? '#f59e0b' : '#ef4444';

    return `<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>回测分析报告</title>
    <style>
        :root {
            --bg-primary: #1a1a2e;
            --bg-secondary: #252540;
            --bg-tertiary: #2d2d4a;
            --text-primary: #ffffff;
            --text-secondary: #9ca3af;
            --primary: #667eea;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --border: #3d3d5c;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 24px;
            line-height: 1.6;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }

        .header-title {
            font-size: 24px;
            font-weight: 600;
        }

        .score-badge {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: ${scoreColor}22;
            border: 3px solid ${scoreColor};
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .score-value {
            font-size: 28px;
            font-weight: 700;
            color: ${scoreColor};
        }

        .score-label {
            font-size: 12px;
            color: var(--text-secondary);
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .metric-card {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            border: 1px solid var(--border);
        }

        .metric-value {
            font-size: 24px;
            font-weight: 700;
            color: var(--primary);
        }

        .metric-label {
            color: var(--text-secondary);
            font-size: 13px;
            margin-top: 4px;
        }

        .positive { color: var(--success); }
        .negative { color: var(--danger); }

        .section {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            border: 1px solid var(--border);
        }

        .section-title {
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .diagnosis-item, .suggestion-item {
            padding: 12px 16px;
            margin-bottom: 8px;
            background: var(--bg-tertiary);
            border-radius: 8px;
            font-size: 14px;
        }

        .actions {
            display: flex;
            gap: 12px;
            margin-top: 24px;
        }

        .btn {
            padding: 12px 24px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
        }

        .btn-primary:hover { background: #5a6fd6; }

        .btn-secondary {
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }

        .btn-secondary:hover { background: #3d3d5c; }

        .timestamp {
            text-align: center;
            color: var(--text-muted);
            font-size: 12px;
            margin-top: 24px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <div class="header-title">📊 回测分析报告</div>
        </div>
        <div class="score-badge">
            <div class="score-value">${score}</div>
            <div class="score-label">综合评分</div>
        </div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value ${metrics.total_return >= 0 ? 'positive' : 'negative'}">
                ${(metrics.total_return * 100).toFixed(2)}%
            </div>
            <div class="metric-label">总收益</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${metrics.sharpe_ratio.toFixed(2)}</div>
            <div class="metric-label">夏普比率</div>
        </div>
        <div class="metric-card">
            <div class="metric-value negative">${(metrics.max_drawdown * 100).toFixed(2)}%</div>
            <div class="metric-label">最大回撤</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${(metrics.win_rate * 100).toFixed(1)}%</div>
            <div class="metric-label">胜率</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${metrics.trade_count}</div>
            <div class="metric-label">交易次数</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${metrics.profit_loss_ratio.toFixed(2)}</div>
            <div class="metric-label">盈亏比</div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">🔍 诊断结果</div>
        ${result.diagnosis.map(d => `<div class="diagnosis-item">${d}</div>`).join('')}
    </div>

    <div class="section">
        <div class="section-title">💡 优化建议</div>
        ${result.suggestions.map(s => `<div class="suggestion-item">${s}</div>`).join('')}
    </div>

    <div class="actions">
        <button class="btn btn-primary" onclick="optimizeStrategy()">
            🚀 生成优化策略
        </button>
        <button class="btn btn-secondary" onclick="copyReport()">
            📋 复制报告
        </button>
    </div>

    <div class="timestamp">
        生成时间: ${new Date().toLocaleString('zh-CN')}
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        
        function copyReport() {
            vscode.postMessage({ command: 'copyReport' });
        }
        
        function optimizeStrategy() {
            vscode.postMessage({ command: 'optimizeStrategy' });
        }
    </script>
</body>
</html>`;
}

/**
 * 生成文本报告
 */
function generateTextReport(metrics: BacktestMetrics, result: BacktestResult): string {
    const score = calculateScore(metrics);
    
    return `# 回测分析报告

## 综合评分: ${score}/100

## 关键指标
- 总收益: ${(metrics.total_return * 100).toFixed(2)}%
- 夏普比率: ${metrics.sharpe_ratio.toFixed(2)}
- 最大回撤: ${(metrics.max_drawdown * 100).toFixed(2)}%
- 胜率: ${(metrics.win_rate * 100).toFixed(1)}%
- 交易次数: ${metrics.trade_count}
- 盈亏比: ${metrics.profit_loss_ratio.toFixed(2)}

## 诊断结果
${result.diagnosis.map(d => `- ${d}`).join('\n')}

## 优化建议
${result.suggestions.map(s => `- ${s}`).join('\n')}

---
生成时间: ${new Date().toLocaleString('zh-CN')}
`;
}
