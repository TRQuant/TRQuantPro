/**
 * TRQuant 策略管理面板
 * 
 * 功能:
 * - 策略库管理
 * - 回测历史查看
 * - 绩效跟踪
 * - 策略文档
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export class StrategyManagerPanel {
    public static currentPanel: StrategyManagerPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _disposables: vscode.Disposable[] = [];
    private readonly _extensionUri: vscode.Uri;

    public static readonly viewType = 'trquant.strategyManager';

    public static createOrShow(extensionUri: vscode.Uri) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        if (StrategyManagerPanel.currentPanel) {
            StrategyManagerPanel.currentPanel._panel.reveal(column);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            StrategyManagerPanel.viewType,
            '📊 策略管理',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        StrategyManagerPanel.currentPanel = new StrategyManagerPanel(panel, extensionUri);
    }

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
        this._panel = panel;
        this._extensionUri = extensionUri;

        this._update();

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);

        this._panel.webview.onDidReceiveMessage(
            async message => {
                switch (message.command) {
                    case 'loadStrategies':
                        await this._loadStrategies();
                        break;
                    case 'loadBacktestHistory':
                        await this._loadBacktestHistory();
                        break;
                    case 'openStrategy':
                        await this._openStrategy(message.path);
                        break;
                    case 'runBacktest':
                        await this._runBacktest(message.strategyPath);
                        break;
                    case 'viewBacktestResult':
                        await this._viewBacktestResult(message.resultId);
                        break;
                    case 'refresh':
                        await this._refresh();
                        break;
                }
            },
            null,
            this._disposables
        );
    }

    private async _loadStrategies() {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) return;

        const rootPath = workspaceFolders[0].uri.fsPath;
        const strategiesDir = path.join(rootPath, 'strategies');
        
        const strategies: any[] = [];
        
        // 扫描策略目录
        const categories = ['bullettrade', 'ptrade', 'qmt', 'unified'];
        
        for (const category of categories) {
            const categoryPath = path.join(strategiesDir, category);
            if (fs.existsSync(categoryPath)) {
                const files = fs.readdirSync(categoryPath).filter(f => f.endsWith('.py'));
                for (const file of files) {
                    const filePath = path.join(categoryPath, file);
                    const stats = fs.statSync(filePath);
                    strategies.push({
                        name: file.replace('.py', ''),
                        path: filePath,
                        category: category,
                        modified: stats.mtime.toISOString(),
                        size: stats.size
                    });
                }
            }
        }

        this._panel.webview.postMessage({
            command: 'strategiesLoaded',
            strategies: strategies
        });
    }

    private async _loadBacktestHistory() {
        // 从MongoDB加载回测历史
        // 这里先返回模拟数据，实际应通过MCP调用
        const history = [
            {
                id: '1',
                strategyName: 'TRQuant_momentum_v3',
                startDate: '2024-01-01',
                endDate: '2024-06-30',
                totalReturn: 0.25,
                sharpeRatio: 1.8,
                maxDrawdown: 0.08,
                timestamp: new Date().toISOString()
            },
            {
                id: '2',
                strategyName: 'TRQuant_value_strategy',
                startDate: '2024-01-01',
                endDate: '2024-06-30',
                totalReturn: 0.15,
                sharpeRatio: 1.2,
                maxDrawdown: 0.12,
                timestamp: new Date().toISOString()
            }
        ];

        this._panel.webview.postMessage({
            command: 'backtestHistoryLoaded',
            history: history
        });
    }

    private async _openStrategy(strategyPath: string) {
        const doc = await vscode.workspace.openTextDocument(strategyPath);
        await vscode.window.showTextDocument(doc);
    }

    private async _runBacktest(strategyPath: string) {
        vscode.window.showInformationMessage(`开始回测: ${path.basename(strategyPath)}`);
        // 调用MCP执行回测
        // TODO: 集成backtest_server的backtest.bullettrade工具
    }

    private async _viewBacktestResult(resultId: string) {
        vscode.window.showInformationMessage(`查看回测结果: ${resultId}`);
        // 打开回测报告
    }

    private async _refresh() {
        await this._loadStrategies();
        await this._loadBacktestHistory();
    }

    private _update() {
        this._panel.webview.html = this._getHtmlContent();
        this._loadStrategies();
        this._loadBacktestHistory();
    }

    private _getHtmlContent(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>策略管理</title>
    <style>
        :root {
            --bg-primary: #1e1e2e;
            --bg-secondary: #2d2d3d;
            --bg-card: #363646;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --accent: #00d9ff;
            --accent-green: #00ff88;
            --accent-red: #ff4444;
            --border: #404050;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'PingFang SC', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 1rem;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }
        
        .header h1 {
            font-size: 1.5rem;
            background: linear-gradient(90deg, var(--accent), var(--accent-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .tab {
            padding: 0.75rem 1.5rem;
            background: var(--bg-secondary);
            border: none;
            border-radius: 8px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .tab.active {
            background: var(--accent);
            color: var(--bg-primary);
        }
        
        .tab:hover:not(.active) {
            background: var(--bg-card);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid var(--border);
        }
        
        .strategy-list {
            display: grid;
            gap: 0.75rem;
        }
        
        .strategy-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background: var(--bg-secondary);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .strategy-item:hover {
            background: var(--bg-card);
            transform: translateX(5px);
        }
        
        .strategy-name {
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .strategy-meta {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
        
        .category-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .category-bullettrade { background: rgba(0, 217, 255, 0.2); color: var(--accent); }
        .category-ptrade { background: rgba(0, 255, 136, 0.2); color: var(--accent-green); }
        .category-qmt { background: rgba(255, 170, 0, 0.2); color: #ffaa00; }
        .category-unified { background: rgba(136, 136, 255, 0.2); color: #8888ff; }
        
        .btn {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: var(--accent);
            color: var(--bg-primary);
        }
        
        .btn-primary:hover {
            opacity: 0.8;
        }
        
        .btn-outline {
            background: transparent;
            border: 1px solid var(--accent);
            color: var(--accent);
        }
        
        .btn-outline:hover {
            background: var(--accent);
            color: var(--bg-primary);
        }
        
        .backtest-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .backtest-table th,
        .backtest-table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        
        .backtest-table th {
            color: var(--text-secondary);
            font-weight: 500;
        }
        
        .positive { color: var(--accent-green); }
        .negative { color: var(--accent-red); }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }
        
        .stat-card {
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--accent);
        }
        
        .stat-label {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }
        
        .actions {
            display: flex;
            gap: 0.5rem;
        }
        
        .empty-state {
            text-align: center;
            padding: 3rem;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 策略管理中心</h1>
        <button class="btn btn-outline" onclick="refresh()">🔄 刷新</button>
    </div>
    
    <div class="tabs">
        <button class="tab active" onclick="switchTab('strategies')">📁 策略库</button>
        <button class="tab" onclick="switchTab('backtest')">📈 回测历史</button>
        <button class="tab" onclick="switchTab('performance')">🎯 绩效跟踪</button>
    </div>
    
    <div id="strategies" class="tab-content active">
        <div class="card">
            <h3 style="margin-bottom: 1rem;">策略列表</h3>
            <div id="strategyList" class="strategy-list">
                <div class="empty-state">加载中...</div>
            </div>
        </div>
    </div>
    
    <div id="backtest" class="tab-content">
        <div class="card">
            <h3 style="margin-bottom: 1rem;">回测历史记录</h3>
            <table class="backtest-table">
                <thead>
                    <tr>
                        <th>策略名称</th>
                        <th>回测区间</th>
                        <th>总收益</th>
                        <th>夏普比率</th>
                        <th>最大回撤</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody id="backtestHistory">
                </tbody>
            </table>
        </div>
    </div>
    
    <div id="performance" class="tab-content">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="totalStrategies">0</div>
                <div class="stat-label">策略总数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="totalBacktests">0</div>
                <div class="stat-label">回测次数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value positive" id="avgReturn">0%</div>
                <div class="stat-label">平均收益</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="avgSharpe">0</div>
                <div class="stat-label">平均夏普</div>
            </div>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        let strategies = [];
        let backtestHistory = [];
        
        function switchTab(tabId) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }
        
        function renderStrategies() {
            const container = document.getElementById('strategyList');
            
            if (strategies.length === 0) {
                container.innerHTML = '<div class="empty-state">暂无策略</div>';
                return;
            }
            
            container.innerHTML = strategies.map(s => \`
                <div class="strategy-item" onclick="openStrategy('\${s.path}')">
                    <div>
                        <div class="strategy-name">\${s.name}</div>
                        <div class="strategy-meta">修改时间: \${new Date(s.modified).toLocaleString()}</div>
                    </div>
                    <div class="actions">
                        <span class="category-badge category-\${s.category}">\${s.category}</span>
                        <button class="btn btn-primary" onclick="event.stopPropagation(); runBacktest('\${s.path}')">回测</button>
                    </div>
                </div>
            \`).join('');
            
            document.getElementById('totalStrategies').textContent = strategies.length;
        }
        
        function renderBacktestHistory() {
            const tbody = document.getElementById('backtestHistory');
            
            tbody.innerHTML = backtestHistory.map(h => \`
                <tr>
                    <td>\${h.strategyName}</td>
                    <td>\${h.startDate} ~ \${h.endDate}</td>
                    <td class="\${h.totalReturn >= 0 ? 'positive' : 'negative'}">\${(h.totalReturn * 100).toFixed(2)}%</td>
                    <td>\${h.sharpeRatio.toFixed(2)}</td>
                    <td class="negative">\${(h.maxDrawdown * 100).toFixed(2)}%</td>
                    <td>
                        <button class="btn btn-outline" onclick="viewResult('\${h.id}')">查看</button>
                    </td>
                </tr>
            \`).join('');
            
            document.getElementById('totalBacktests').textContent = backtestHistory.length;
            
            if (backtestHistory.length > 0) {
                const avgReturn = backtestHistory.reduce((sum, h) => sum + h.totalReturn, 0) / backtestHistory.length;
                const avgSharpe = backtestHistory.reduce((sum, h) => sum + h.sharpeRatio, 0) / backtestHistory.length;
                document.getElementById('avgReturn').textContent = (avgReturn * 100).toFixed(2) + '%';
                document.getElementById('avgSharpe').textContent = avgSharpe.toFixed(2);
            }
        }
        
        function openStrategy(path) {
            vscode.postMessage({ command: 'openStrategy', path: path });
        }
        
        function runBacktest(path) {
            vscode.postMessage({ command: 'runBacktest', strategyPath: path });
        }
        
        function viewResult(id) {
            vscode.postMessage({ command: 'viewBacktestResult', resultId: id });
        }
        
        function refresh() {
            vscode.postMessage({ command: 'refresh' });
        }
        
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'strategiesLoaded':
                    strategies = message.strategies;
                    renderStrategies();
                    break;
                case 'backtestHistoryLoaded':
                    backtestHistory = message.history;
                    renderBacktestHistory();
                    break;
            }
        });
        
        // 初始加载
        vscode.postMessage({ command: 'loadStrategies' });
        vscode.postMessage({ command: 'loadBacktestHistory' });
    </script>
</body>
</html>`;
    }

    public dispose() {
        StrategyManagerPanel.currentPanel = undefined;

        this._panel.dispose();

        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) {
                disposable.dispose();
            }
        }
    }
}

