/**
 * 分析回测结果命令
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';

export async function analyzeBacktest(
    client: TRQuantClient,
    context: vscode.ExtensionContext
): Promise<void> {
    // 选择回测结果文件
    const files = await vscode.window.showOpenDialog({
        canSelectMany: false,
        filters: {
            'JSON/HTML': ['json', 'html'],
            'All': ['*']
        },
        title: '选择回测结果文件'
    });

    if (!files || files.length === 0) return;

    const filePath = files[0].fsPath;

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "TRQuant: 分析回测结果...",
        cancellable: false
    }, async () => {
        try {
            const result = await client.analyzeBacktest({
                backtest_file: filePath
            });

            if (!result.ok || !result.data) {
                vscode.window.showErrorMessage(`分析回测失败: ${result.error}`);
                return;
            }

            const analysis = result.data;

            // 创建WebView显示分析结果
            const panel = vscode.window.createWebviewPanel(
                'trquantBacktest',
                '📊 回测分析',
                vscode.ViewColumn.Beside,
                { enableScripts: true }
            );

            panel.webview.html = getWebviewContent(analysis);

        } catch (error: any) {
            vscode.window.showErrorMessage(`错误: ${error.message}`);
        }
    });
}

function getWebviewContent(analysis: any): string {
    const metrics = analysis.metrics || {};
    const diagnosis = analysis.diagnosis || [];
    const suggestions = analysis.suggestions || [];

    return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #1a1a2e;
            color: #fff;
            padding: 20px;
            margin: 0;
        }
        h1 { margin-bottom: 24px; }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        .metric-card {
            background: #252540;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 4px;
        }
        .metric-label {
            color: #9ca3af;
            font-size: 13px;
        }
        .positive { color: #10b981; }
        .negative { color: #ef4444; }
        .section {
            background: #252540;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }
        .section h3 {
            margin: 0 0 12px 0;
            color: #9ca3af;
            font-size: 14px;
        }
        .diagnosis-item {
            padding: 8px 0;
            border-bottom: 1px solid #333;
        }
        .diagnosis-item:last-child { border: none; }
        .suggestion {
            background: #667eea22;
            border-left: 4px solid #667eea;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 0 8px 8px 0;
        }
    </style>
</head>
<body>
    <h1>📊 回测分析报告</h1>
    
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value ${(metrics.total_return || 0) > 0 ? 'positive' : 'negative'}">
                ${(metrics.total_return || 0).toFixed(2)}%
            </div>
            <div class="metric-label">总收益率</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${(metrics.sharpe_ratio || 0).toFixed(2)}</div>
            <div class="metric-label">夏普比率</div>
        </div>
        <div class="metric-card">
            <div class="metric-value negative">${(metrics.max_drawdown || 0).toFixed(2)}%</div>
            <div class="metric-label">最大回撤</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${(metrics.win_rate || 0).toFixed(1)}%</div>
            <div class="metric-label">胜率</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${metrics.trade_count || 0}</div>
            <div class="metric-label">交易次数</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${(metrics.profit_loss_ratio || 0).toFixed(2)}</div>
            <div class="metric-label">盈亏比</div>
        </div>
    </div>

    ${diagnosis.length > 0 ? `
    <div class="section">
        <h3>🔍 问题诊断</h3>
        ${diagnosis.map((d: string) => `<div class="diagnosis-item">• ${d}</div>`).join('')}
    </div>
    ` : ''}

    ${suggestions.length > 0 ? `
    <div class="section">
        <h3>💡 优化建议</h3>
        ${suggestions.map((s: string) => `<div class="suggestion">${s}</div>`).join('')}
    </div>
    ` : ''}
</body>
</html>`;
}

