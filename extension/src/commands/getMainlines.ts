/**
 * 获取投资主线命令
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';

export async function getMainlines(
    client: TRQuantClient,
    context: vscode.ExtensionContext
): Promise<void> {
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "TRQuant: 获取投资主线...",
        cancellable: false
    }, async () => {
        try {
            const result = await client.getMainlines({ top_n: 20 });

            if (!result.ok || !result.data) {
                vscode.window.showErrorMessage(`获取投资主线失败: ${result.error}`);
                return;
            }

            const mainlines = result.data;

            // 创建WebView显示
            const panel = vscode.window.createWebviewPanel(
                'trquantMainlines',
                '📊 投资主线',
                vscode.ViewColumn.Beside,
                { enableScripts: true }
            );

            panel.webview.html = getWebviewContent(mainlines);

        } catch (error: any) {
            vscode.window.showErrorMessage(`错误: ${error.message}`);
        }
    });
}

function getWebviewContent(mainlines: any[]): string {
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
        .mainline-card {
            background: #252540;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            border-left: 4px solid #667eea;
        }
        .mainline-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .mainline-name {
            font-size: 16px;
            font-weight: bold;
        }
        .mainline-score {
            background: #667eea;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
        }
        .mainline-industries {
            color: #9ca3af;
            font-size: 13px;
            margin-bottom: 8px;
        }
        .mainline-logic {
            color: #d1d5db;
            font-size: 13px;
            line-height: 1.5;
        }
        .rank {
            display: inline-block;
            width: 24px;
            height: 24px;
            background: #333;
            border-radius: 50%;
            text-align: center;
            line-height: 24px;
            margin-right: 8px;
            font-size: 12px;
        }
        .rank.top3 { background: #f59e0b; }
    </style>
</head>
<body>
    <h1>🎯 投资主线 TOP ${mainlines.length}</h1>
    
    ${mainlines.map((m, i) => `
        <div class="mainline-card">
            <div class="mainline-header">
                <div>
                    <span class="rank ${i < 3 ? 'top3' : ''}">${i + 1}</span>
                    <span class="mainline-name">${m.name}</span>
                </div>
                <span class="mainline-score">得分: ${m.score?.toFixed(2)}</span>
            </div>
            <div class="mainline-industries">
                🏭 ${(m.industries || []).join(', ')}
            </div>
            <div class="mainline-logic">
                💡 ${m.logic || ''}
            </div>
        </div>
    `).join('')}
</body>
</html>`;
}

