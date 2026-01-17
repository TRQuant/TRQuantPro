/**
 * Tenbagger Dashboard - 十倍股仪表盘
 * 
 * 展示十倍股候选池、评分排名、产业链热度等
 * 
 * @author TRQuant Team
 * @date 2025-12-18
 */

import * as vscode from 'vscode';
import { PythonBridge } from '../pythonBridge';

export class TenbaggerDashboardPanel {
    public static currentPanel: TenbaggerDashboardPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private _disposables: vscode.Disposable[] = [];

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
        this._panel = panel;
        this._extensionUri = extensionUri;

        this._panel.webview.html = this._getWebviewContent();

        this._panel.webview.onDidReceiveMessage(
            async (message) => {
                switch (message.command) {
                    case 'refresh':
                        await this._refreshData();
                        break;
                    case 'evaluate':
                        await this._evaluateStock(message.symbol);
                        break;
                    case 'viewDetail':
                        await this._viewStockDetail(message.symbol);
                        break;
                    case 'filterPool':
                        await this._filterPool(message.level);
                        break;
                }
            },
            null,
            this._disposables
        );

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    }

    public static createOrShow(extensionUri: vscode.Uri) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        if (TenbaggerDashboardPanel.currentPanel) {
            TenbaggerDashboardPanel.currentPanel._panel.reveal(column);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'tenbaggerDashboard',
            '🎯 十倍股仪表盘',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
            }
        );

        TenbaggerDashboardPanel.currentPanel = new TenbaggerDashboardPanel(panel, extensionUri);
    }

    private async _refreshData() {
        try {
            this._panel.webview.postMessage({ command: 'loading', loading: true });
            
            const bridge = PythonBridge.getInstance();
            
            // 获取候选池统计
            const poolStats = await bridge.executeCommand('candidate_pool_stats', {});
            
            // 获取Top候选股
            const topCandidates = await bridge.executeCommand('tenbagger_ranking', { limit: 10 });
            
            // 获取数据源状态
            const datasourceStats = await bridge.executeCommand('datasource_stats', {});
            
            this._panel.webview.postMessage({
                command: 'updateData',
                data: {
                    poolStats: poolStats || { level_counts: { L0: 0, L1: 0, L2: 0, L3: 0 } },
                    topCandidates: topCandidates || [],
                    datasourceStats: datasourceStats || {}
                }
            });
        } catch (error) {
            vscode.window.showErrorMessage(`刷新数据失败: ${error}`);
        } finally {
            this._panel.webview.postMessage({ command: 'loading', loading: false });
        }
    }

    private async _evaluateStock(symbol: string) {
        try {
            const bridge = PythonBridge.getInstance();
            const result = await bridge.executeCommand('tenbagger_evaluate', { symbol });
            
            this._panel.webview.postMessage({
                command: 'evaluationResult',
                data: result
            });
        } catch (error) {
            vscode.window.showErrorMessage(`评估失败: ${error}`);
        }
    }

    private async _viewStockDetail(symbol: string) {
        // 打开股票详情面板
        vscode.commands.executeCommand('trquant.openStockDetail', symbol);
    }

    private async _filterPool(level: string) {
        try {
            const bridge = PythonBridge.getInstance();
            const result = await bridge.executeCommand('candidate_pool_filter', { level });
            
            this._panel.webview.postMessage({
                command: 'poolFiltered',
                data: result
            });
        } catch (error) {
            vscode.window.showErrorMessage(`筛选失败: ${error}`);
        }
    }

    private _getWebviewContent(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>十倍股仪表盘</title>
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-card: #1f2937;
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent: #10b981;
            --accent-hover: #059669;
            --warning: #f59e0b;
            --danger: #ef4444;
            --purple: #8b5cf6;
            --blue: #3b82f6;
            --border: #374151;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 24px;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }
        
        .header h1 {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent) 0%, var(--blue) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .header-actions {
            display: flex;
            gap: 12px;
        }
        
        .btn {
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: var(--accent);
            color: white;
        }
        
        .btn-primary:hover {
            background: var(--accent-hover);
            transform: translateY(-1px);
        }
        
        .btn-secondary {
            background: var(--bg-card);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .stat-card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 14px;
            margin-bottom: 8px;
        }
        
        .stat-value {
            font-size: 32px;
            font-weight: 700;
        }
        
        .stat-value.l0 { color: var(--text-secondary); }
        .stat-value.l1 { color: var(--blue); }
        .stat-value.l2 { color: var(--purple); }
        .stat-value.l3 { color: var(--accent); }
        
        .stat-change {
            font-size: 12px;
            margin-top: 4px;
        }
        
        .stat-change.positive { color: var(--accent); }
        .stat-change.negative { color: var(--danger); }
        
        .main-content {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 24px;
        }
        
        .panel {
            background: var(--bg-card);
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow: hidden;
        }
        
        .panel-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .panel-title {
            font-size: 18px;
            font-weight: 600;
        }
        
        .panel-body {
            padding: 16px;
        }
        
        .candidate-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .candidate-table th,
        .candidate-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        
        .candidate-table th {
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 12px;
            text-transform: uppercase;
        }
        
        .candidate-table tr:hover {
            background: rgba(255, 255, 255, 0.02);
        }
        
        .stock-symbol {
            font-family: 'SF Mono', monospace;
            color: var(--blue);
        }
        
        .stock-name {
            color: var(--text-primary);
            font-weight: 500;
        }
        
        .stage-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .stage-s0 { background: rgba(156, 163, 175, 0.2); color: #9ca3af; }
        .stage-s1 { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
        .stage-s2 { background: rgba(139, 92, 246, 0.2); color: #8b5cf6; }
        .stage-s3 { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .stage-s4 { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
        .stage-s5 { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
        
        .score-bar {
            width: 100%;
            height: 8px;
            background: var(--bg-secondary);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .score-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s;
        }
        
        .score-fill.grade-s { background: linear-gradient(90deg, #10b981, #059669); }
        .score-fill.grade-a { background: linear-gradient(90deg, #3b82f6, #2563eb); }
        .score-fill.grade-b { background: linear-gradient(90deg, #8b5cf6, #7c3aed); }
        .score-fill.grade-c { background: linear-gradient(90deg, #f59e0b, #d97706); }
        .score-fill.grade-d { background: linear-gradient(90deg, #ef4444, #dc2626); }
        
        .grade-badge {
            display: inline-block;
            width: 32px;
            height: 32px;
            line-height: 32px;
            text-align: center;
            border-radius: 8px;
            font-weight: 700;
        }
        
        .grade-s { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .grade-a { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
        .grade-b { background: rgba(139, 92, 246, 0.2); color: #8b5cf6; }
        .grade-c { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
        .grade-d { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
        
        .action-btn {
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid var(--border);
            background: transparent;
            color: var(--text-primary);
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s;
        }
        
        .action-btn:hover {
            background: var(--accent);
            border-color: var(--accent);
        }
        
        .quick-eval {
            margin-top: 16px;
        }
        
        .quick-eval-input {
            display: flex;
            gap: 12px;
        }
        
        .quick-eval-input input {
            flex: 1;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 14px;
        }
        
        .quick-eval-input input:focus {
            outline: none;
            border-color: var(--accent);
        }
        
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .loading-spinner {
            width: 48px;
            height: 48px;
            border: 4px solid var(--border);
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .hidden { display: none !important; }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
        }
        
        .empty-state .icon {
            font-size: 48px;
            margin-bottom: 16px;
        }
    </style>
</head>
<body>
    <div class="loading-overlay hidden" id="loadingOverlay">
        <div class="loading-spinner"></div>
    </div>
    
    <header class="header">
        <h1>🎯 十倍股仪表盘</h1>
        <div class="header-actions">
            <button class="btn btn-secondary" onclick="openSettings()">⚙️ 设置</button>
            <button class="btn btn-primary" onclick="refreshData()">🔄 刷新数据</button>
        </div>
    </header>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">L0 观察池</div>
            <div class="stat-value l0" id="statL0">0</div>
            <div class="stat-change">全市场筛选</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">L1 候选池</div>
            <div class="stat-value l1" id="statL1">0</div>
            <div class="stat-change positive">↑ 市值/流动性筛选</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">L2 精选池</div>
            <div class="stat-value l2" id="statL2">0</div>
            <div class="stat-change positive">↑ 基本面筛选</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">L3 核心池</div>
            <div class="stat-value l3" id="statL3">0</div>
            <div class="stat-change positive">↑ Stage + ScoreCard</div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">📊 十倍股潜力排名 Top 10</span>
                <select class="action-btn" onchange="filterPool(this.value)">
                    <option value="all">全部</option>
                    <option value="L1">L1 候选</option>
                    <option value="L2">L2 精选</option>
                    <option value="L3">L3 核心</option>
                </select>
            </div>
            <div class="panel-body">
                <table class="candidate-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>股票</th>
                            <th>阶段</th>
                            <th>评分</th>
                            <th>等级</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="candidateTableBody">
                        <tr>
                            <td colspan="6">
                                <div class="empty-state">
                                    <div class="icon">📭</div>
                                    <p>暂无数据，点击刷新按钮获取最新数据</p>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">⚡ 快速评估</span>
            </div>
            <div class="panel-body">
                <div class="quick-eval">
                    <div class="quick-eval-input">
                        <input type="text" id="evalSymbol" placeholder="输入股票代码，如 300750.SZ" />
                        <button class="btn btn-primary" onclick="quickEvaluate()">评估</button>
                    </div>
                    <div id="evalResult" style="margin-top: 16px;"></div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function refreshData() {
            vscode.postMessage({ command: 'refresh' });
        }
        
        function quickEvaluate() {
            const symbol = document.getElementById('evalSymbol').value.trim();
            if (symbol) {
                vscode.postMessage({ command: 'evaluate', symbol });
            }
        }
        
        function viewDetail(symbol) {
            vscode.postMessage({ command: 'viewDetail', symbol });
        }
        
        function filterPool(level) {
            vscode.postMessage({ command: 'filterPool', level });
        }
        
        function openSettings() {
            // TODO: 打开设置面板
        }
        
        function updateStats(stats) {
            const lc = stats.level_counts || {};
            document.getElementById('statL0').textContent = lc.L0 || 0;
            document.getElementById('statL1').textContent = lc.L1 || 0;
            document.getElementById('statL2').textContent = lc.L2 || 0;
            document.getElementById('statL3').textContent = lc.L3 || 0;
        }
        
        function updateCandidates(candidates) {
            const tbody = document.getElementById('candidateTableBody');
            
            if (!candidates || candidates.length === 0) {
                tbody.innerHTML = \`
                    <tr>
                        <td colspan="6">
                            <div class="empty-state">
                                <div class="icon">📭</div>
                                <p>暂无数据，点击刷新按钮获取最新数据</p>
                            </div>
                        </td>
                    </tr>
                \`;
                return;
            }
            
            tbody.innerHTML = candidates.map((c, i) => \`
                <tr>
                    <td>\${i + 1}</td>
                    <td>
                        <div class="stock-symbol">\${c.symbol}</div>
                        <div class="stock-name">\${c.name || '-'}</div>
                    </td>
                    <td>
                        <span class="stage-badge stage-\${(c.stage || 's0').toLowerCase()}">\${c.stage || 'S0'}</span>
                    </td>
                    <td>
                        <div>\${(c.score || 0).toFixed(0)}分</div>
                        <div class="score-bar">
                            <div class="score-fill grade-\${getGradeClass(c.score)}" style="width: \${c.score || 0}%"></div>
                        </div>
                    </td>
                    <td>
                        <span class="grade-badge grade-\${getGradeClass(c.score)}">\${getGradeLetter(c.score)}</span>
                    </td>
                    <td>
                        <button class="action-btn" onclick="viewDetail('\${c.symbol}')">详情</button>
                    </td>
                </tr>
            \`).join('');
        }
        
        function getGradeClass(score) {
            if (score >= 90) return 's';
            if (score >= 75) return 'a';
            if (score >= 60) return 'b';
            if (score >= 45) return 'c';
            return 'd';
        }
        
        function getGradeLetter(score) {
            if (score >= 90) return 'S';
            if (score >= 75) return 'A';
            if (score >= 60) return 'B';
            if (score >= 45) return 'C';
            return 'D';
        }
        
        function showEvalResult(result) {
            const container = document.getElementById('evalResult');
            if (!result) {
                container.innerHTML = '<p style="color: var(--danger);">评估失败</p>';
                return;
            }
            
            container.innerHTML = \`
                <div style="background: var(--bg-secondary); padding: 16px; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                        <span style="font-weight: 600;">\${result.symbol} \${result.name || ''}</span>
                        <span class="grade-badge grade-\${getGradeClass(result.total_score)}">\${getGradeLetter(result.total_score)}</span>
                    </div>
                    <div style="font-size: 24px; font-weight: 700; color: var(--accent);">\${result.total_score?.toFixed(0) || 0}分</div>
                    <div style="color: var(--text-secondary); margin-top: 8px;">\${result.recommendation || ''}</div>
                </div>
            \`;
        }
        
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'loading':
                    document.getElementById('loadingOverlay').classList.toggle('hidden', !message.loading);
                    break;
                case 'updateData':
                    if (message.data.poolStats) {
                        updateStats(message.data.poolStats);
                    }
                    if (message.data.topCandidates) {
                        updateCandidates(message.data.topCandidates);
                    }
                    break;
                case 'evaluationResult':
                    showEvalResult(message.data);
                    break;
            }
        });
        
        // 初始化时刷新数据
        refreshData();
    </script>
</body>
</html>`;
    }

    public dispose() {
        TenbaggerDashboardPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) {
                disposable.dispose();
            }
        }
    }
}
