/**
 * 市场状态面板
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';

export class MarketPanel {
    public static currentPanel: MarketPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._client = client;

        this._update();

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);

        this._panel.webview.onDidReceiveMessage(
            async (message) => {
                switch (message.command) {
                    case 'refresh':
                        await this._update();
                        break;
                    case 'getMarketStatus':
                        await vscode.commands.executeCommand('trquant.getMarketStatus');
                        break;
                    case 'getMainlines':
                        await vscode.commands.executeCommand('trquant.getMainlines');
                        break;
                    case 'generateStrategy':
                        await vscode.commands.executeCommand('trquant.generateStrategy');
                        break;
                }
            },
            null,
            this._disposables
        );
    }

    public static createOrShow(extensionUri: vscode.Uri, client: TRQuantClient) {
        const column = vscode.ViewColumn.Beside;

        if (MarketPanel.currentPanel) {
            MarketPanel.currentPanel._panel.reveal(column);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'trquantPanel',
            'TRQuant 控制台',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        MarketPanel.currentPanel = new MarketPanel(panel, extensionUri, client);
    }

    private async _update() {
        this._panel.webview.html = await this._getHtmlContent();
    }

    private async _getHtmlContent(): Promise<string> {
        // 获取最新数据
        let marketData = null;
        let mainlines = null;

        try {
            const marketResult = await this._client.getMarketStatus();
            if (marketResult.ok) marketData = marketResult.data;

            const mainlineResult = await this._client.getMainlines({ top_n: 5 });
            if (mainlineResult.ok) mainlines = mainlineResult.data;
        } catch (e) {
            // 忽略错误
        }

        const regimeColor = marketData?.regime === 'risk_on' ? '#10b981' : 
                           marketData?.regime === 'risk_off' ? '#ef4444' : '#f59e0b';

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
            padding-bottom: 16px;
            border-bottom: 1px solid #333;
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .logo-icon { font-size: 32px; }
        .logo-text {
            font-size: 20px;
            font-weight: bold;
        }
        .refresh-btn {
            background: #333;
            border: none;
            color: #fff;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
        }
        .refresh-btn:hover { background: #444; }

        .status-card {
            background: linear-gradient(135deg, ${regimeColor}22, ${regimeColor}11);
            border: 1px solid ${regimeColor}44;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .status-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-regime {
            font-size: 24px;
            font-weight: bold;
        }
        .status-badge {
            background: ${regimeColor};
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
        }
        .status-summary {
            margin-top: 12px;
            color: #d1d5db;
            line-height: 1.6;
        }

        .section {
            background: #252540;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }
        .section-title {
            font-size: 14px;
            color: #9ca3af;
            margin-bottom: 12px;
        }

        .mainline-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #333;
        }
        .mainline-item:last-child { border: none; }

        .actions {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-top: 20px;
        }
        .action-btn {
            background: #667eea;
            border: none;
            color: #fff;
            padding: 14px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        .action-btn:hover { background: #5a6fd6; }
        .action-btn.primary { background: #10b981; }
        .action-btn.primary:hover { background: #059669; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">
            <span class="logo-icon">📊</span>
            <span class="logo-text">TRQuant 控制台</span>
        </div>
        <button class="refresh-btn" onclick="refresh()">🔄 刷新</button>
    </div>

    <div class="status-card">
        <div class="status-header">
            <span class="status-regime">
                ${marketData?.regime === 'risk_on' ? '📈 风险偏好上升' : 
                  marketData?.regime === 'risk_off' ? '📉 风险偏好下降' : '➡️ 震荡市场'}
            </span>
            <span class="status-badge">${(marketData?.regime || 'UNKNOWN').toUpperCase()}</span>
        </div>
        <div class="status-summary">
            ${marketData?.summary || '正在获取市场状态...'}
        </div>
    </div>

    ${mainlines ? `
    <div class="section">
        <div class="section-title">🎯 热门主线 TOP 5</div>
        ${mainlines.slice(0, 5).map((m: any, i: number) => `
            <div class="mainline-item">
                <span>${i + 1}. ${m.name}</span>
                <span style="color: #667eea">${m.score?.toFixed(2)}</span>
            </div>
        `).join('')}
    </div>
    ` : ''}

    <div class="actions">
        <button class="action-btn" onclick="getMarketStatus()">
            📊 市场状态
        </button>
        <button class="action-btn" onclick="getMainlines()">
            🎯 投资主线
        </button>
        <button class="action-btn" onclick="recommendFactors()">
            📈 因子推荐
        </button>
        <button class="action-btn primary" onclick="generateStrategy()">
            🚀 生成策略
        </button>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        function refresh() { vscode.postMessage({ command: 'refresh' }); }
        function getMarketStatus() { vscode.postMessage({ command: 'getMarketStatus' }); }
        function getMainlines() { vscode.postMessage({ command: 'getMainlines' }); }
        function recommendFactors() { vscode.postMessage({ command: 'recommendFactors' }); }
        function generateStrategy() { vscode.postMessage({ command: 'generateStrategy' }); }
    </script>
</body>
</html>`;
    }

    public dispose() {
        MarketPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) x.dispose();
        }
    }
}

