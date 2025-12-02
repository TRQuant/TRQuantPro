/**
 * 推荐因子命令
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';

export async function recommendFactors(
    client: TRQuantClient,
    context: vscode.ExtensionContext
): Promise<void> {
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "TRQuant: 推荐因子...",
        cancellable: false
    }, async () => {
        try {
            // 先获取市场状态
            const marketStatus = await client.getMarketStatus();
            const regime = marketStatus.data?.regime || 'neutral';

            // 获取因子推荐
            const result = await client.recommendFactors({
                market_regime: regime
            });

            if (!result.ok || !result.data) {
                vscode.window.showErrorMessage(`获取因子推荐失败: ${result.error}`);
                return;
            }

            const factors = result.data;

            // 创建WebView显示
            const panel = vscode.window.createWebviewPanel(
                'trquantFactors',
                '📈 因子推荐',
                vscode.ViewColumn.Beside,
                { enableScripts: true }
            );

            panel.webview.html = getWebviewContent(factors, regime);

        } catch (error: any) {
            vscode.window.showErrorMessage(`错误: ${error.message}`);
        }
    });
}

function getWebviewContent(factors: any[], regime: string): string {
    // 按类别分组
    const grouped: Record<string, any[]> = {};
    for (const f of factors) {
        const cat = f.category || '其他';
        if (!grouped[cat]) grouped[cat] = [];
        grouped[cat].push(f);
    }

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
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        .regime-tag {
            background: ${regime === 'risk_on' ? '#10b981' : regime === 'risk_off' ? '#ef4444' : '#f59e0b'};
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 13px;
        }
        .category {
            margin-bottom: 24px;
        }
        .category-title {
            color: #9ca3af;
            font-size: 13px;
            margin-bottom: 12px;
            text-transform: uppercase;
        }
        .factor-card {
            background: #252540;
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .factor-info {
            flex: 1;
        }
        .factor-name {
            font-weight: bold;
            margin-bottom: 4px;
        }
        .factor-reason {
            color: #9ca3af;
            font-size: 12px;
        }
        .factor-weight {
            background: #667eea;
            padding: 6px 14px;
            border-radius: 16px;
            font-size: 13px;
            font-weight: bold;
        }
        .weight-high { background: #10b981; }
        .weight-medium { background: #f59e0b; }
        .weight-low { background: #6b7280; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📈 因子推荐</h1>
        <span class="regime-tag">市场: ${regime.toUpperCase()}</span>
    </div>
    
    ${Object.entries(grouped).map(([category, items]) => `
        <div class="category">
            <div class="category-title">📊 ${category}</div>
            ${items.map(f => {
                const weightClass = f.weight > 0.7 ? 'weight-high' : 
                                   f.weight > 0.4 ? 'weight-medium' : 'weight-low';
                return `
                <div class="factor-card">
                    <div class="factor-info">
                        <div class="factor-name">${f.name}</div>
                        <div class="factor-reason">${f.reason || ''}</div>
                    </div>
                    <span class="factor-weight ${weightClass}">${(f.weight * 100).toFixed(0)}%</span>
                </div>
                `;
            }).join('')}
        </div>
    `).join('')}
</body>
</html>`;
}

