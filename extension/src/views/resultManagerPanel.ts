/**
 * TRQuant 结果管理面板
 * ====================
 * 
 * 管理历史回测结果：列表、筛选、对比、导出
 */

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';

const MODULE = 'ResultManagerPanel';

interface BacktestResult {
    id: string;
    name: string;
    strategy: string;
    startDate: string;
    endDate: string;
    totalReturn: number;
    sharpeRatio: number;
    maxDrawdown: number;
    winRate: number;
    createdAt: string;
    filePath: string;
}

export class ResultManagerPanel {
    public static currentPanel: ResultManagerPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];
    
    private _results: BacktestResult[] = [];
    private _selectedResults: string[] = [];
    private _sortField: string = 'createdAt';
    private _sortOrder: 'asc' | 'desc' = 'desc';
    private _filterStrategy: string = '';

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._client = client;

        this._loadResults();
        this._update();

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);

        this._panel.webview.onDidReceiveMessage(
            async (message) => {
                switch (message.command) {
                    case 'refresh':
                        this._loadResults();
                        this._update();
                        break;
                    case 'viewResult':
                        await this._viewResult(message.resultId);
                        break;
                    case 'deleteResult':
                        await this._deleteResult(message.resultId);
                        break;
                    case 'compareResults':
                        await this._compareResults(message.resultIds);
                        break;
                    case 'exportResults':
                        await this._exportResults(message.resultIds);
                        break;
                    case 'toggleSelect':
                        this._toggleSelect(message.resultId);
                        this._update();
                        break;
                    case 'sort':
                        this._sort(message.field);
                        this._update();
                        break;
                    case 'filter':
                        this._filterStrategy = message.strategy;
                        this._update();
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
    ): ResultManagerPanel {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        if (ResultManagerPanel.currentPanel) {
            ResultManagerPanel.currentPanel._panel.reveal(column);
            return ResultManagerPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'trquantResultManager',
            '📁 回测结果管理',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
            }
        );

        ResultManagerPanel.currentPanel = new ResultManagerPanel(panel, extensionUri, client);
        return ResultManagerPanel.currentPanel;
    }

    private _loadResults() {
        this._results = [];
        
        // 扫描回测结果目录
        const resultsDir = path.join(this._extensionUri.fsPath, '..', 'backtest_results');
        
        try {
            if (fs.existsSync(resultsDir)) {
                const items = fs.readdirSync(resultsDir);
                
                for (const item of items) {
                    const itemPath = path.join(resultsDir, item);
                    const stat = fs.statSync(itemPath);
                    
                    if (stat.isDirectory()) {
                        // 查找metrics.json
                        const metricsPath = path.join(itemPath, 'metrics.json');
                        if (fs.existsSync(metricsPath)) {
                            try {
                                const metrics = JSON.parse(fs.readFileSync(metricsPath, 'utf-8'));
                                this._results.push({
                                    id: item,
                                    name: metrics.name || item,
                                    strategy: metrics.strategy || '未知策略',
                                    startDate: metrics.start_date || '',
                                    endDate: metrics.end_date || '',
                                    totalReturn: metrics.total_return || 0,
                                    sharpeRatio: metrics.sharpe_ratio || 0,
                                    maxDrawdown: metrics.max_drawdown || 0,
                                    winRate: metrics.win_rate || 0,
                                    createdAt: stat.mtime.toISOString(),
                                    filePath: itemPath
                                });
                            } catch (e) {
                                logger.warn(`解析metrics失败: ${metricsPath}`, MODULE);
                            }
                        }
                    } else if (item.endsWith('.json') && item !== 'metrics.json') {
                        // 单独的结果文件
                        try {
                            const data = JSON.parse(fs.readFileSync(itemPath, 'utf-8'));
                            this._results.push({
                                id: item.replace('.json', ''),
                                name: data.name || item,
                                strategy: data.strategy || '未知策略',
                                startDate: data.start_date || '',
                                endDate: data.end_date || '',
                                totalReturn: data.total_return || data.metrics?.total_return || 0,
                                sharpeRatio: data.sharpe_ratio || data.metrics?.sharpe_ratio || 0,
                                maxDrawdown: data.max_drawdown || data.metrics?.max_drawdown || 0,
                                winRate: data.win_rate || data.metrics?.win_rate || 0,
                                createdAt: stat.mtime.toISOString(),
                                filePath: itemPath
                            });
                        } catch (e) {
                            logger.warn(`解析结果文件失败: ${itemPath}`, MODULE);
                        }
                    }
                }
            }
        } catch (error) {
            logger.error(`加载结果失败: ${error}`, MODULE);
        }
        
        logger.info(`加载了 ${this._results.length} 个回测结果`, MODULE);
    }

    private _toggleSelect(resultId: string) {
        const index = this._selectedResults.indexOf(resultId);
        if (index >= 0) {
            this._selectedResults.splice(index, 1);
        } else {
            this._selectedResults.push(resultId);
        }
    }

    private _sort(field: string) {
        if (this._sortField === field) {
            this._sortOrder = this._sortOrder === 'asc' ? 'desc' : 'asc';
        } else {
            this._sortField = field;
            this._sortOrder = 'desc';
        }
    }

    private async _viewResult(resultId: string) {
        const result = this._results.find(r => r.id === resultId);
        if (result) {
            // 打开报告HTML或JSON
            const htmlPath = path.join(result.filePath, 'report.html');
            if (fs.existsSync(htmlPath)) {
                vscode.env.openExternal(vscode.Uri.file(htmlPath));
            } else if (fs.existsSync(result.filePath)) {
                vscode.workspace.openTextDocument(result.filePath).then(doc => {
                    vscode.window.showTextDocument(doc);
                });
            }
        }
    }

    private async _deleteResult(resultId: string) {
        const confirm = await vscode.window.showWarningMessage(
            `确定要删除回测结果 "${resultId}" 吗？`,
            '删除', '取消'
        );
        
        if (confirm === '删除') {
            const result = this._results.find(r => r.id === resultId);
            if (result) {
                try {
                    if (fs.statSync(result.filePath).isDirectory()) {
                        fs.rmSync(result.filePath, { recursive: true });
                    } else {
                        fs.unlinkSync(result.filePath);
                    }
                    vscode.window.showInformationMessage(`已删除: ${resultId}`);
                    this._loadResults();
                    this._update();
                } catch (error) {
                    vscode.window.showErrorMessage(`删除失败: ${error}`);
                }
            }
        }
    }

    private async _compareResults(resultIds: string[]) {
        if (resultIds.length < 2) {
            vscode.window.showWarningMessage('请选择至少2个结果进行对比');
            return;
        }
        
        const results = this._results.filter(r => resultIds.includes(r.id));
        
        // 生成对比报告
        let comparison = '# 回测结果对比\n\n';
        comparison += '| 指标 | ' + results.map(r => r.name).join(' | ') + ' |\n';
        comparison += '| --- | ' + results.map(() => '---').join(' | ') + ' |\n';
        comparison += '| 总收益 | ' + results.map(r => `${(r.totalReturn * 100).toFixed(2)}%`).join(' | ') + ' |\n';
        comparison += '| 夏普比率 | ' + results.map(r => r.sharpeRatio.toFixed(2)).join(' | ') + ' |\n';
        comparison += '| 最大回撤 | ' + results.map(r => `${(r.maxDrawdown * 100).toFixed(2)}%`).join(' | ') + ' |\n';
        comparison += '| 胜率 | ' + results.map(r => `${(r.winRate * 100).toFixed(2)}%`).join(' | ') + ' |\n';
        
        const doc = await vscode.workspace.openTextDocument({
            content: comparison,
            language: 'markdown'
        });
        await vscode.window.showTextDocument(doc);
    }

    private async _exportResults(resultIds: string[]) {
        const results = resultIds.length > 0 
            ? this._results.filter(r => resultIds.includes(r.id))
            : this._results;
        
        const csv = this._generateCSV(results);
        
        const uri = await vscode.window.showSaveDialog({
            defaultUri: vscode.Uri.file('backtest_results.csv'),
            filters: { 'CSV': ['csv'] }
        });
        
        if (uri) {
            fs.writeFileSync(uri.fsPath, csv, 'utf-8');
            vscode.window.showInformationMessage(`已导出 ${results.length} 条结果`);
        }
    }

    private _generateCSV(results: BacktestResult[]): string {
        const headers = ['ID', '名称', '策略', '开始日期', '结束日期', '总收益', '夏普比率', '最大回撤', '胜率', '创建时间'];
        const rows = results.map(r => [
            r.id, r.name, r.strategy, r.startDate, r.endDate,
            (r.totalReturn * 100).toFixed(2) + '%',
            r.sharpeRatio.toFixed(2),
            (r.maxDrawdown * 100).toFixed(2) + '%',
            (r.winRate * 100).toFixed(2) + '%',
            r.createdAt
        ]);
        
        return [headers, ...rows].map(row => row.join(',')).join('\n');
    }

    private _getFilteredResults(): BacktestResult[] {
        let results = [...this._results];
        
        // 筛选
        if (this._filterStrategy) {
            results = results.filter(r => 
                r.strategy.toLowerCase().includes(this._filterStrategy.toLowerCase()) ||
                r.name.toLowerCase().includes(this._filterStrategy.toLowerCase())
            );
        }
        
        // 排序
        results.sort((a, b) => {
            let aVal = (a as any)[this._sortField];
            let bVal = (b as any)[this._sortField];
            
            if (typeof aVal === 'string') {
                return this._sortOrder === 'asc' 
                    ? aVal.localeCompare(bVal)
                    : bVal.localeCompare(aVal);
            }
            
            return this._sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
        });
        
        return results;
    }

    private _update() {
        this._panel.webview.html = this._getHtmlContent();
    }

    private _getHtmlContent(): string {
        const results = this._getFilteredResults();
        const strategies = [...new Set(this._results.map(r => r.strategy))];
        
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>回测结果管理</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            color: #e0e0e0;
            padding: 20px;
            min-height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .header h1 { font-size: 24px; color: #58a6ff; }
        .toolbar {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        .search-input {
            padding: 8px 12px;
            border: 1px solid #333;
            border-radius: 6px;
            background: #1e1e2e;
            color: #e0e0e0;
            width: 200px;
        }
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }
        .btn-primary { background: #238636; color: white; }
        .btn-secondary { background: #6e40c9; color: white; }
        .btn-danger { background: #da3633; color: white; }
        .btn:hover { opacity: 0.9; }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .results-table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(30, 30, 50, 0.8);
            border-radius: 12px;
            overflow: hidden;
        }
        .results-table th, .results-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #333;
        }
        .results-table th {
            background: #1e1e2e;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
        }
        .results-table th:hover { background: #2a2a3e; }
        .results-table tr:hover { background: rgba(88, 166, 255, 0.1); }
        
        .checkbox {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        .positive { color: #3fb950; }
        .negative { color: #da3633; }
        
        .actions {
            display: flex;
            gap: 8px;
        }
        .action-btn {
            padding: 4px 8px;
            font-size: 12px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            background: #30363d;
            color: #e0e0e0;
        }
        .action-btn:hover { background: #484f58; }
        
        .stats-bar {
            display: flex;
            gap: 24px;
            margin-bottom: 16px;
            padding: 12px;
            background: rgba(30, 30, 50, 0.8);
            border-radius: 8px;
        }
        .stat-item { display: flex; flex-direction: column; }
        .stat-value { font-size: 20px; font-weight: 700; color: #58a6ff; }
        .stat-label { font-size: 12px; color: #8b949e; }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #6e7681;
        }
        
        .sort-icon { margin-left: 4px; font-size: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📁 回测结果管理</h1>
        <button class="btn btn-primary" onclick="refresh()">🔄 刷新</button>
    </div>
    
    <div class="stats-bar">
        <div class="stat-item">
            <span class="stat-value">${this._results.length}</span>
            <span class="stat-label">总结果数</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">${strategies.length}</span>
            <span class="stat-label">策略类型</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">${this._selectedResults.length}</span>
            <span class="stat-label">已选择</span>
        </div>
        <div class="stat-item">
            <span class="stat-value ${this._results.length > 0 && Math.max(...this._results.map(r => r.totalReturn)) > 0 ? 'positive' : ''}">${this._results.length > 0 ? (Math.max(...this._results.map(r => r.totalReturn)) * 100).toFixed(1) + '%' : 'N/A'}</span>
            <span class="stat-label">最佳收益</span>
        </div>
    </div>
    
    <div class="toolbar">
        <input type="text" class="search-input" placeholder="搜索策略或名称..." 
               value="${this._filterStrategy}" oninput="filter(this.value)">
        <button class="btn btn-secondary" onclick="compareSelected()" ${this._selectedResults.length < 2 ? 'disabled' : ''}>
            📊 对比选中 (${this._selectedResults.length})
        </button>
        <button class="btn btn-secondary" onclick="exportSelected()">
            📥 导出${this._selectedResults.length > 0 ? '选中' : '全部'}
        </button>
    </div>
    
    ${results.length > 0 ? `
    <table class="results-table">
        <thead>
            <tr>
                <th width="40"></th>
                <th onclick="sort('name')">名称 ${this._sortField === 'name' ? (this._sortOrder === 'asc' ? '↑' : '↓') : ''}</th>
                <th onclick="sort('strategy')">策略</th>
                <th onclick="sort('totalReturn')">总收益 ${this._sortField === 'totalReturn' ? (this._sortOrder === 'asc' ? '↑' : '↓') : ''}</th>
                <th onclick="sort('sharpeRatio')">夏普</th>
                <th onclick="sort('maxDrawdown')">最大回撤</th>
                <th onclick="sort('createdAt')">创建时间 ${this._sortField === 'createdAt' ? (this._sortOrder === 'asc' ? '↑' : '↓') : ''}</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            ${results.map(r => `
            <tr>
                <td><input type="checkbox" class="checkbox" ${this._selectedResults.includes(r.id) ? 'checked' : ''} 
                    onchange="toggleSelect('${r.id}')"></td>
                <td>${r.name}</td>
                <td>${r.strategy}</td>
                <td class="${r.totalReturn >= 0 ? 'positive' : 'negative'}">${(r.totalReturn * 100).toFixed(2)}%</td>
                <td>${r.sharpeRatio.toFixed(2)}</td>
                <td class="negative">${(r.maxDrawdown * 100).toFixed(2)}%</td>
                <td>${r.createdAt.slice(0, 10)}</td>
                <td class="actions">
                    <button class="action-btn" onclick="viewResult('${r.id}')">👁️</button>
                    <button class="action-btn" onclick="deleteResult('${r.id}')">🗑️</button>
                </td>
            </tr>
            `).join('')}
        </tbody>
    </table>
    ` : '<div class="empty-state">暂无回测结果<br><br>执行回测后，结果将显示在这里</div>'}
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function refresh() { vscode.postMessage({ command: 'refresh' }); }
        function viewResult(id) { vscode.postMessage({ command: 'viewResult', resultId: id }); }
        function deleteResult(id) { vscode.postMessage({ command: 'deleteResult', resultId: id }); }
        function toggleSelect(id) { vscode.postMessage({ command: 'toggleSelect', resultId: id }); }
        function sort(field) { vscode.postMessage({ command: 'sort', field }); }
        function filter(strategy) { vscode.postMessage({ command: 'filter', strategy }); }
        
        function compareSelected() {
            vscode.postMessage({ command: 'compareResults', resultIds: ${JSON.stringify(this._selectedResults)} });
        }
        function exportSelected() {
            vscode.postMessage({ command: 'exportResults', resultIds: ${JSON.stringify(this._selectedResults)} });
        }
    </script>
</body>
</html>`;
    }

    public dispose() {
        ResultManagerPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) disposable.dispose();
        }
    }
}
