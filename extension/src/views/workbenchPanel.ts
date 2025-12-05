/**
 * TRQuant 量化工作台
 * ===================
 * 
 * 全新的量化投资工作台界面
 * 提供市场分析、策略开发、回测验证等核心功能
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';
import { MarketStatus, Mainline, Factor } from '../types';

const MODULE = 'WorkbenchPanel';

export class WorkbenchPanel {
    public static currentPanel: WorkbenchPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];
    
    // 缓存数据
    private _marketStatus: MarketStatus | null = null;
    private _mainlines: Mainline[] = [];
    private _factors: Factor[] = [];

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._client = client;

        this._panel.webview.onDidReceiveMessage(
            message => this.handleMessage(message),
            null,
            this._disposables
        );

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        
        // 初始加载
        this.updateContent();
        this.refreshAllData();
    }

    public static createOrShow(
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ): WorkbenchPanel {
        const column = vscode.ViewColumn.One;

        if (WorkbenchPanel.currentPanel) {
            WorkbenchPanel.currentPanel._panel.reveal(column);
            return WorkbenchPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'trquantWorkbench',
            '⚡ TRQuant 量化工作台',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        WorkbenchPanel.currentPanel = new WorkbenchPanel(panel, extensionUri, client);
        return WorkbenchPanel.currentPanel;
    }

    private async handleMessage(message: any): Promise<void> {
        console.log('[WorkbenchPanel] 收到消息:', message.command);
        
        switch (message.command) {
            case 'refreshAll':
                await this.refreshAllData();
                break;
            case 'refreshMarket':
                await this.refreshMarketStatus();
                break;
            case 'refreshMainlines':
                await this.refreshMainlines();
                break;
            case 'refreshFactors':
                await this.refreshFactors();
                break;
            case 'createProject':
                vscode.commands.executeCommand('trquant.createProject');
                break;
            case 'generateStrategy':
                vscode.commands.executeCommand('trquant.generateStrategy');
                break;
            case 'runBacktest':
                vscode.commands.executeCommand('trquant.runBacktest');
                break;
            case 'optimizeStrategy':
                vscode.commands.executeCommand('trquant.optimizeStrategy');
                break;
            case 'openWorkflowPanel':
                vscode.commands.executeCommand('trquant.launchDesktopSystem');
                break;
            default:
                logger.warn(`未知命令: ${message.command}`, MODULE);
        }
    }

    private async refreshAllData(): Promise<void> {
        await Promise.all([
            this.refreshMarketStatus(),
            this.refreshMainlines(),
            this.refreshFactors()
        ]);
    }

    private async refreshMarketStatus(): Promise<void> {
        try {
            const response = await this._client.getMarketStatus({});
            if (response.ok && response.data) {
                this._marketStatus = response.data;
                this._panel.webview.postMessage({
                    command: 'updateMarketStatus',
                    data: response.data
                });
                this.updateContent();
            }
        } catch (error) {
            logger.error(`获取市场状态失败: ${error}`, MODULE);
        }
    }

    private async refreshMainlines(): Promise<void> {
        try {
            const response = await this._client.getMainlines({ time_horizon: 'short', top_n: 5 });
            if (response.ok && response.data) {
                this._mainlines = response.data;
                this._panel.webview.postMessage({
                    command: 'updateMainlines',
                    data: response.data
                });
                this.updateContent();
            }
        } catch (error) {
            logger.error(`获取投资主线失败: ${error}`, MODULE);
        }
    }

    private async refreshFactors(): Promise<void> {
        try {
            const marketRegime = this._marketStatus?.regime || 'neutral';
            const response = await this._client.recommendFactors({ market_regime: marketRegime, top_n: 5 });
            if (response.ok && response.data) {
                this._factors = response.data;
                this._panel.webview.postMessage({
                    command: 'updateFactors',
                    data: response.data
                });
                this.updateContent();
            }
        } catch (error) {
            logger.error(`获取推荐因子失败: ${error}`, MODULE);
        }
    }

    private updateContent(): void {
        this._panel.webview.html = this.generateHtml();
    }

    private getRegimeText(regime?: string): string {
        const regimeMap: Record<string, string> = {
            'risk_on': '风险偏好上升',
            'risk_off': '风险偏好下降',
            'neutral': '震荡市场'
        };
        return regime ? regimeMap[regime] || regime : '';
    }

    private generateHtml(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TRQuant 量化工作台</title>
    <!-- 立即禁用 Service Worker（必须在任何脚本执行前） -->
    <script>
        (function() {
            // 检测是否为 VS Code webview 环境
            const isWebview = 
                location.protocol === 'vscode-webview:' ||
                typeof acquireVsCodeApi === 'function';
            
            // 关键：没有 serviceWorker 就不要继续（避免在不支持的环境里调用 SW API）
            if (!('serviceWorker' in navigator) || !navigator.serviceWorker) return;
            
            // 在 webview 里，直接阻断 register（不要 getRegistrations / unregister）
            if (isWebview) {
                try {
                    navigator.serviceWorker.register = function() {
                        console.warn('[TRQuant WorkbenchPanel] SW register blocked in webview');
                        try { 
                            // 打印调用栈以定位注册来源
                            console.warn(new Error('[TRQuant WorkbenchPanel] SW register stack').stack); 
                        } catch(e) {
                            console.warn('[TRQuant WorkbenchPanel] Stack trace error:', e);
                        }
                        return Promise.reject(new Error('Service Worker disabled in VS Code webview'));
                    };
                } catch(e) {
                    console.warn('[TRQuant WorkbenchPanel] Failed to block Service Worker:', e);
                }
            }
        })();
    </script>
    <style>
        :root {
            --bg-dark: #0a0e14;
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #1c2128;
            --bg-hover: #262c36;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --text-muted: #6e7681;
            --accent-gold: #f0b429;
            --accent-green: #3fb950;
            --accent-blue: #58a6ff;
            --accent-purple: #a371f7;
            --accent-red: #f85149;
            --border-color: #30363d;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 24px;
        }
        
        .header {
            background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
            padding: 24px 32px;
            border-radius: 12px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid var(--border-color);
        }
        
        .header-left {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .logo {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #f0b429 0%, #e85d04 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            color: #fff;
        }
        
        .header-title h1 {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(90deg, var(--accent-gold), #fff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .header-title .subtitle {
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 4px;
        }
        
        .header-btn {
            padding: 10px 20px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-secondary);
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .header-btn:hover {
            background: var(--bg-hover);
            border-color: var(--accent-blue);
            color: var(--text-primary);
        }
        
        .main-container {
            max-width: 1600px;
            margin: 0 auto;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        
        .card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.2s;
        }
        
        .card:hover {
            border-color: var(--accent-blue);
            transform: translateY(-2px);
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        
        .card-title {
            font-size: 16px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .card-body {
            color: var(--text-secondary);
        }
        
        .market-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            margin-bottom: 24px;
        }
        
        .market-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }
        
        .market-card .label {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }
        
        .market-card .value {
            font-size: 20px;
            font-weight: 700;
        }
        
        .quick-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }
        
        .quick-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
        }
        
        .quick-card:hover {
            transform: translateY(-2px);
            border-color: var(--accent-blue);
        }
        
        .quick-icon {
            font-size: 32px;
            margin-bottom: 12px;
        }
        
        .quick-title {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .quick-desc {
            font-size: 12px;
            color: var(--text-muted);
        }
        
        .list-item {
            padding: 12px;
            background: var(--bg-card);
            border-radius: 8px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .empty-state {
            text-align: center;
            padding: 32px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-left">
            <div class="logo">⚡</div>
            <div class="header-title">
                <h1>TRQuant 量化工作台</h1>
                <div class="subtitle">专业量化投资分析平台</div>
            </div>
        </div>
        <div>
            <button class="header-btn" onclick="vscode.postMessage({command: 'refreshAll'})">
                🔄 刷新数据
            </button>
        </div>
    </div>
    
    <div class="main-container">
        <!-- 市场状态 -->
        <div class="market-grid" id="marketGrid">
            <div class="market-card">
                <div class="label">市场状态</div>
                <div class="value" id="marketRegime">${this.getRegimeText(this._marketStatus?.regime) || '加载中...'}</div>
            </div>
            <div class="market-card">
                <div class="label">上证指数</div>
                <div class="value" id="shIndex">-</div>
            </div>
            <div class="market-card">
                <div class="label">深证成指</div>
                <div class="value" id="szIndex">-</div>
            </div>
            <div class="market-card">
                <div class="label">创业板指</div>
                <div class="value" id="cyIndex">-</div>
            </div>
            <div class="market-card">
                <div class="label">风格轮动</div>
                <div class="value" id="marketStyle">${this._marketStatus?.style_rotation || '-'}</div>
            </div>
        </div>
        
        <!-- 核心功能 -->
        <div class="quick-grid">
            <div class="quick-card" onclick="vscode.postMessage({command: 'createProject'})">
                <div class="quick-icon">📁</div>
                <div class="quick-title">新建项目</div>
                <div class="quick-desc">创建量化策略项目</div>
            </div>
            <div class="quick-card" onclick="vscode.postMessage({command: 'generateStrategy'})">
                <div class="quick-icon">🤖</div>
                <div class="quick-title">生成策略</div>
                <div class="quick-desc">AI智能生成策略代码</div>
            </div>
            <div class="quick-card" onclick="vscode.postMessage({command: 'runBacktest'})">
                <div class="quick-icon">🧪</div>
                <div class="quick-title">运行回测</div>
                <div class="quick-desc">策略回测验证</div>
            </div>
            <div class="quick-card" onclick="vscode.postMessage({command: 'optimizeStrategy'})">
                <div class="quick-icon">🔍</div>
                <div class="quick-title">策略优化</div>
                <div class="quick-desc">分析并优化策略</div>
            </div>
        </div>
        
        <!-- 投资主线 & 推荐因子 -->
        <div class="grid">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">🔥 投资主线 TOP5</div>
                    <button class="header-btn" style="padding: 6px 12px; font-size: 12px;" onclick="vscode.postMessage({command: 'refreshMainlines'})">刷新</button>
                </div>
                <div class="card-body">
                    <div id="mainlineList">
                        ${this._mainlines.length > 0 
                            ? this._mainlines.map((m, i) => `
                                <div class="list-item">
                                    <div>
                                        <strong>${i + 1}. ${m.name}</strong>
                                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">${m.industries?.join(', ') || ''}</div>
                                    </div>
                                    <div style="color: var(--accent-gold); font-weight: 600;">${m.score?.toFixed(2) || '0.00'}</div>
                                </div>
                            `).join('')
                            : '<div class="empty-state">点击刷新获取投资主线</div>'
                        }
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="card-title">📊 推荐因子</div>
                    <button class="header-btn" style="padding: 6px 12px; font-size: 12px;" onclick="vscode.postMessage({command: 'refreshFactors'})">刷新</button>
                </div>
                <div class="card-body">
                    <div id="factorList">
                        ${this._factors.length > 0 
                            ? this._factors.map((f, i) => `
                                <div class="list-item">
                                    <div>
                                        <strong>${f.name || `因子 ${i + 1}`}</strong>
                                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">${f.category || ''}</div>
                                    </div>
                                    <div style="color: var(--accent-purple); font-weight: 600;">${f.weight?.toFixed(2) || '0.00'}</div>
                                </div>
                            `).join('')
                            : '<div class="empty-state">点击刷新获取推荐因子</div>'
                        }
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 工作流入口 -->
        <div class="card">
            <div class="card-header">
                <div class="card-title">🖥️ 完整工作流</div>
            </div>
            <div class="card-body">
                <p style="margin-bottom: 16px; color: var(--text-secondary);">
                    打开桌面系统查看完整的8步骤投资工作流，包括信息获取、市场趋势、投资主线、候选池、因子构建、策略开发、回测验证和实盘交易。
                </p>
                <button class="header-btn" style="width: 100%;" onclick="vscode.postMessage({command: 'openWorkflowPanel'})">
                    🖥️ 打开桌面系统
                </button>
            </div>
        </div>
    </div>
    
    <script>
        // Service Worker 已在 <head> 中禁用，这里不再重复
        const vscode = acquireVsCodeApi();
        
        // 监听来自扩展的消息
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'updateMarketStatus':
                    if (message.data) {
                        const regimeMap = {
                            'risk_on': '风险偏好上升',
                            'risk_off': '风险偏好下降',
                            'neutral': '震荡市场'
                        };
                        const regimeText = regimeMap[message.data.regime] || message.data.regime || '-';
                        document.getElementById('marketRegime').textContent = regimeText;
                        document.getElementById('marketStyle').textContent = message.data.style_rotation || '-';
                        if (message.data.indices && message.data.indices.length >= 3) {
                            document.getElementById('shIndex').textContent = message.data.indices[0]?.value?.toFixed(2) || '-';
                            document.getElementById('szIndex').textContent = message.data.indices[1]?.value?.toFixed(2) || '-';
                            document.getElementById('cyIndex').textContent = message.data.indices[2]?.value?.toFixed(2) || '-';
                        }
                    }
                    break;
                case 'updateMainlines':
                    const mainlineList = document.getElementById('mainlineList');
                    if (message.data && message.data.length > 0) {
                        mainlineList.innerHTML = message.data.map((m, i) => \`
                            <div class="list-item">
                                <div>
                                    <strong>\${i + 1}. \${m.name}</strong>
                                    <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">\${m.industries?.join(', ') || ''}</div>
                                </div>
                                <div style="color: var(--accent-gold); font-weight: 600;">\${m.score?.toFixed(2) || '0.00'}</div>
                            </div>
                        \`).join('');
                    } else {
                        mainlineList.innerHTML = '<div class="empty-state">暂无数据</div>';
                    }
                    break;
                case 'updateFactors':
                    const factorList = document.getElementById('factorList');
                    if (message.data && message.data.length > 0) {
                        factorList.innerHTML = message.data.map((f, i) => \`
                            <div class="list-item">
                                <div>
                                    <strong>\${f.name || \`因子 \${i + 1}\`}</strong>
                                    <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">\${f.category || ''}</div>
                                </div>
                                <div style="color: var(--accent-purple); font-weight: 600;">\${f.weight?.toFixed(2) || '0.00'}</div>
                            </div>
                        \`).join('');
                    } else {
                        factorList.innerHTML = '<div class="empty-state">暂无数据</div>';
                    }
                    break;
            }
        });
    </script>
</body>
</html>`;
    }

    public dispose() {
        WorkbenchPanel.currentPanel = undefined;
        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) {
                disposable.dispose();
            }
        }
    }
}

/**
 * 注册工作台面板
 */
export function registerWorkbenchPanel(
    context: vscode.ExtensionContext,
    client: TRQuantClient
): void {
    console.log('[WorkbenchPanel] 注册工作台面板命令');
    
    const disposable = vscode.commands.registerCommand('trquant.openWorkbench', () => {
        WorkbenchPanel.createOrShow(context.extensionUri, client);
    });
    
    context.subscriptions.push(disposable);
    logger.info('量化工作台面板已注册', MODULE);
}

