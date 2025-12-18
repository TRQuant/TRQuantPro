/**
 * TRQuant 监控面板
 * ================
 * 
 * 显示系统状态、MCP服务器状态、工作流任务状态、缓存统计
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';

const MODULE = 'MonitoringPanel';

interface ServerStatus {
    name: string;
    status: 'running' | 'stopped' | 'error';
    tools: number;
    lastCheck: string;
}

interface CacheStats {
    name: string;
    hits: number;
    misses: number;
    hitRate: number;
    size: number;
}

interface WorkflowTask {
    id: string;
    name: string;
    status: string;
    progress: number;
    startedAt: string;
}

export class MonitoringPanel {
    public static currentPanel: MonitoringPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];
    
    private _refreshInterval: NodeJS.Timeout | null = null;
    private _serverStatuses: ServerStatus[] = [];
    private _cacheStats: CacheStats[] = [];
    private _workflowTasks: WorkflowTask[] = [];

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._client = client;

        this._update();
        this._startAutoRefresh();

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);

        this._panel.webview.onDidReceiveMessage(
            async (message) => {
                switch (message.command) {
                    case 'refresh':
                        await this._refreshAll();
                        break;
                    case 'clearCache':
                        await this._clearCache(message.cacheName);
                        break;
                    case 'restartServer':
                        await this._restartServer(message.serverName);
                        break;
                }
            },
            null,
            this._disposables
        );
    }

    public static createOrShow(
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ): MonitoringPanel {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        if (MonitoringPanel.currentPanel) {
            MonitoringPanel.currentPanel._panel.reveal(column);
            return MonitoringPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'trquantMonitoring',
            '📊 TRQuant 监控',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
            }
        );

        MonitoringPanel.currentPanel = new MonitoringPanel(panel, extensionUri, client);
        return MonitoringPanel.currentPanel;
    }

    private _startAutoRefresh() {
        this._refreshInterval = setInterval(() => {
            this._refreshAll();
        }, 30000); // 30秒刷新一次
    }

    private async _refreshAll() {
        try {
            // 获取缓存统计
            const cacheResult = await this._client.callBridge<any>('run_workflow_step', { 
                step: 'cache_stats' 
            });
            if (cacheResult?.data?.caches) {
                const caches = cacheResult.data.caches as Record<string, any>;
                this._cacheStats = Object.entries(caches).map(([name, stats]) => ({
                    name,
                    hits: stats?.hits || 0,
                    misses: stats?.misses || 0,
                    hitRate: stats?.hit_rate || 0,
                    size: stats?.current_size || 0
                }));
            }

            // 获取工作流列表
            const workflowResult = await this._client.callBridge<any>('run_workflow_step', { 
                step: 'workflow_list',
                limit: 10 
            });
            const workflows = workflowResult?.data?.workflows || [];
            if (Array.isArray(workflows)) {
                this._workflowTasks = workflows.map((wf: any) => ({
                    id: wf.workflow_id || wf.id || '',
                    name: wf.name || '未命名工作流',
                    status: wf.status || 'unknown',
                    progress: this._calculateProgress(wf.steps),
                    startedAt: wf.created_at || ''
                }));
            }

            // 获取数据源健康状态
            const healthResult = await this._client.healthCheck();
            this._serverStatuses = [
                {
                    name: 'trquant-core',
                    status: healthResult ? 'running' : 'error',
                    tools: 22,
                    lastCheck: new Date().toISOString()
                },
                {
                    name: 'trquant-workflow',
                    status: 'running',
                    tools: 8,
                    lastCheck: new Date().toISOString()
                }
            ];

            this._update();
        } catch (error) {
            logger.error(`刷新监控数据失败: ${error}`, MODULE);
        }
    }

    private _calculateProgress(steps: any[]): number {
        if (!steps || steps.length === 0) return 0;
        const completed = steps.filter(s => s.status === 'completed').length;
        return Math.round((completed / steps.length) * 100);
    }

    private async _clearCache(cacheName: string) {
        try {
            await this._client.callBridge<any>('run_workflow_step', { 
                step: 'cache_clear',
                cache_name: cacheName 
            });
            vscode.window.showInformationMessage(`缓存 ${cacheName} 已清空`);
            await this._refreshAll();
        } catch (error) {
            vscode.window.showErrorMessage(`清空缓存失败: ${error}`);
        }
    }

    private async _restartServer(serverName: string) {
        vscode.window.showInformationMessage(`重启服务器 ${serverName} (功能开发中)`);
    }

    private _update() {
        this._panel.webview.html = this._getHtmlContent();
    }

    private _getHtmlContent(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TRQuant 监控</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            color: #e0e0e0;
            padding: 20px;
            min-height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid #333;
        }
        .header h1 {
            font-size: 24px;
            color: #58a6ff;
        }
        .refresh-btn {
            background: #238636;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }
        .refresh-btn:hover { background: #2ea043; }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .card {
            background: rgba(30, 30, 50, 0.8);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #333;
        }
        .card-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #58a6ff;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* 服务器状态 */
        .server-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            margin-bottom: 8px;
        }
        .server-name { font-weight: 500; }
        .server-status {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
        }
        .status-running { background: #238636; color: white; }
        .status-stopped { background: #6e7681; color: white; }
        .status-error { background: #da3633; color: white; }
        
        /* 缓存统计 */
        .cache-item {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 8px;
            padding: 12px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            margin-bottom: 8px;
        }
        .cache-name { font-weight: 500; }
        .cache-stats {
            display: flex;
            gap: 16px;
            font-size: 12px;
            color: #8b949e;
        }
        .hit-rate {
            color: #3fb950;
            font-weight: 600;
        }
        .clear-btn {
            background: #6e40c9;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
        }
        .clear-btn:hover { background: #8957e5; }
        
        /* 工作流任务 */
        .task-item {
            padding: 12px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            margin-bottom: 8px;
        }
        .task-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        .task-name { font-weight: 500; }
        .task-status {
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
        }
        .status-completed { background: #238636; }
        .status-running { background: #1f6feb; }
        .status-created { background: #6e7681; }
        .status-failed { background: #da3633; }
        .progress-bar {
            height: 4px;
            background: #30363d;
            border-radius: 2px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #58a6ff, #3fb950);
            transition: width 0.3s;
        }
        
        /* 系统摘要 */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 20px;
        }
        .summary-item {
            text-align: center;
            padding: 16px;
            background: rgba(30, 30, 50, 0.8);
            border-radius: 12px;
            border: 1px solid #333;
        }
        .summary-value {
            font-size: 32px;
            font-weight: 700;
            color: #58a6ff;
        }
        .summary-label {
            font-size: 12px;
            color: #8b949e;
            margin-top: 4px;
        }
        
        .empty-state {
            text-align: center;
            padding: 20px;
            color: #6e7681;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 系统监控</h1>
        <button class="refresh-btn" onclick="refresh()">🔄 刷新</button>
    </div>
    
    <div class="summary-grid">
        <div class="summary-item">
            <div class="summary-value">${this._serverStatuses.filter(s => s.status === 'running').length}</div>
            <div class="summary-label">运行中的服务器</div>
        </div>
        <div class="summary-item">
            <div class="summary-value">${this._workflowTasks.length}</div>
            <div class="summary-label">工作流任务</div>
        </div>
        <div class="summary-item">
            <div class="summary-value">${this._cacheStats.reduce((sum, c) => sum + c.hits, 0)}</div>
            <div class="summary-label">缓存命中</div>
        </div>
        <div class="summary-item">
            <div class="summary-value">${Math.round(this._cacheStats.reduce((sum, c) => sum + c.hitRate, 0) / Math.max(this._cacheStats.length, 1))}%</div>
            <div class="summary-label">平均命中率</div>
        </div>
    </div>
    
    <div class="grid">
        <!-- MCP服务器状态 -->
        <div class="card">
            <div class="card-title">🖥️ MCP服务器状态</div>
            ${this._serverStatuses.length > 0 ? this._serverStatuses.map(s => `
                <div class="server-item">
                    <div>
                        <div class="server-name">${s.name}</div>
                        <div style="font-size: 12px; color: #6e7681">${s.tools} 个工具</div>
                    </div>
                    <span class="server-status status-${s.status}">${s.status === 'running' ? '运行中' : s.status === 'error' ? '错误' : '已停止'}</span>
                </div>
            `).join('') : '<div class="empty-state">正在加载...</div>'}
        </div>
        
        <!-- 缓存统计 -->
        <div class="card">
            <div class="card-title">💾 缓存统计</div>
            ${this._cacheStats.length > 0 ? this._cacheStats.map(c => `
                <div class="cache-item">
                    <div>
                        <div class="cache-name">${c.name}</div>
                        <div class="cache-stats">
                            <span>命中: ${c.hits}</span>
                            <span>未中: ${c.misses}</span>
                            <span class="hit-rate">${c.hitRate}%</span>
                        </div>
                    </div>
                    <button class="clear-btn" onclick="clearCache('${c.name}')">清空</button>
                </div>
            `).join('') : '<div class="empty-state">无缓存数据</div>'}
            <button class="clear-btn" style="width: 100%; margin-top: 8px;" onclick="clearCache('all')">清空全部缓存</button>
        </div>
        
        <!-- 工作流任务 -->
        <div class="card" style="grid-column: span 2;">
            <div class="card-title">📋 最近工作流</div>
            ${this._workflowTasks.length > 0 ? this._workflowTasks.slice(0, 5).map(t => `
                <div class="task-item">
                    <div class="task-header">
                        <span class="task-name">${t.name}</span>
                        <span class="task-status status-${t.status}">${t.status}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${t.progress}%"></div>
                    </div>
                    <div style="font-size: 11px; color: #6e7681; margin-top: 4px;">
                        ${t.id} | ${t.startedAt.slice(0, 19).replace('T', ' ')}
                    </div>
                </div>
            `).join('') : '<div class="empty-state">暂无工作流任务</div>'}
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function refresh() {
            vscode.postMessage({ command: 'refresh' });
        }
        
        function clearCache(cacheName) {
            vscode.postMessage({ command: 'clearCache', cacheName });
        }
        
        // 页面加载时自动刷新
        refresh();
    </script>
</body>
</html>`;
    }

    public dispose() {
        MonitoringPanel.currentPanel = undefined;
        
        if (this._refreshInterval) {
            clearInterval(this._refreshInterval);
        }

        this._panel.dispose();

        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) {
                disposable.dispose();
            }
        }
    }
}
