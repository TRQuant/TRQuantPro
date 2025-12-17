/**
 * 报告面板 V2 - MCP集成版
 * =======================
 * 
 * 调用 report-server MCP 生成和管理报告:
 * - 回测报告
 * - 策略对比报告
 * - 策略诊断报告
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';
import { generateTraceId } from '../services/mcpClientV2';

const MODULE = 'ReportPanel';

// 报告类型
const REPORT_TYPES = [
    {
        id: 'backtest',
        name: '回测报告',
        icon: '📊',
        tool: 'report.generate',
        description: '详细的回测结果分析报告'
    },
    {
        id: 'compare',
        name: '对比报告',
        icon: '⚖️',
        tool: 'report.compare',
        description: '多策略/多参数对比分析'
    },
    {
        id: 'diagnosis',
        name: '诊断报告',
        icon: '🔍',
        tool: 'report.diagnosis',
        description: '策略问题诊断和优化建议'
    }
];

// 报告格式
const REPORT_FORMATS = [
    { id: 'html', name: 'HTML', icon: '🌐' },
    { id: 'pdf', name: 'PDF', icon: '📄' },
    { id: 'markdown', name: 'Markdown', icon: '📝' }
];

export class ReportPanel {
    public static currentPanel: ReportPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];
    
    private _backtestResult: any = null;
    private _reports: any[] = [];

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient,
        options?: { result?: any }
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._client = client;
        this._backtestResult = options?.result || null;

        this._panel.webview.html = this._getHtmlContent();
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        this._panel.webview.onDidReceiveMessage(
            message => this._handleMessage(message),
            null,
            this._disposables
        );
        
        // 加载报告列表
        this._loadReports();
    }

    public static createOrShow(
        extensionUri: vscode.Uri,
        client: TRQuantClient,
        options?: { result?: any }
    ): ReportPanel {
        logger.info('创建报告面板V2', MODULE);
        
        const column = vscode.ViewColumn.One;

        if (ReportPanel.currentPanel) {
            ReportPanel.currentPanel._panel.reveal(column);
            if (options?.result) {
                ReportPanel.currentPanel._backtestResult = options.result;
            }
            return ReportPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'trquantReportV2',
            '📄 报告中心',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        ReportPanel.currentPanel = new ReportPanel(panel, extensionUri, client, options);
        return ReportPanel.currentPanel;
    }

    public dispose(): void {
        ReportPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }

    // ==================== 消息处理 ====================

    private async _handleMessage(message: any): Promise<void> {
        logger.info(`[ReportPanel] 收到消息: ${message.command}`, MODULE);

        switch (message.command) {
            case 'generateReport':
                await this._generateReport(message.type, message.format, message.options);
                break;
            case 'openReport':
                await this._openReport(message.reportId);
                break;
            case 'deleteReport':
                await this._deleteReport(message.reportId);
                break;
            case 'refreshReports':
                await this._loadReports();
                break;
        }
    }

    // ==================== MCP调用 ====================

    /**
     * 加载报告列表
     */
    private async _loadReports(): Promise<void> {
        try {
            const response = await this._client.callBridge('call_mcp_tool', {
                tool_name: 'report.list',
                arguments: { limit: 20 },
                trace_id: generateTraceId()
            });

            const resp = response as any;
            if (resp.ok && resp.data) {
                this._reports = resp.data.reports || [];
                this._postMessage({
                    command: 'reportsLoaded',
                    reports: this._reports
                });
            }
        } catch (error: any) {
            logger.error(`加载报告列表失败: ${error.message}`, MODULE);
        }
    }

    /**
     * 生成报告
     */
    private async _generateReport(
        type: string,
        format: string,
        options: any
    ): Promise<void> {
        const typeInfo = REPORT_TYPES.find(t => t.id === type);
        if (!typeInfo) {
            vscode.window.showErrorMessage(`未知报告类型: ${type}`);
            return;
        }

        this._postMessage({ command: 'generating' });

        try {
            const args: any = {
                format,
                title: options.title || '韬睿量化报告',
                strategy_name: options.strategyName || '策略'
            };

            if (type === 'backtest') {
                args.result = this._backtestResult || options.result;
            } else if (type === 'compare') {
                args.results = options.results || [];
            } else if (type === 'diagnosis') {
                args.result = this._backtestResult || options.result;
            }

            logger.info(`生成报告: ${typeInfo.tool}`, MODULE);

            const response = await this._client.callBridge('call_mcp_tool', {
                tool_name: typeInfo.tool,
                arguments: args,
                trace_id: generateTraceId()
            });

            const resp = response as any;
            if (resp.ok && resp.data) {
                this._postMessage({
                    command: 'generated',
                    report: resp.data
                });

                vscode.window.showInformationMessage(
                    `报告已生成: ${resp.data.title}`,
                    '打开报告'
                ).then(selection => {
                    if (selection === '打开报告' && resp.data.file_path) {
                        vscode.env.openExternal(vscode.Uri.file(resp.data.file_path));
                    }
                });

                // 刷新列表
                await this._loadReports();
            } else {
                throw new Error(resp.error || '生成失败');
            }
        } catch (error: any) {
            logger.error(`报告生成失败: ${error.message}`, MODULE);
            this._postMessage({
                command: 'error',
                message: error.message
            });
            vscode.window.showErrorMessage(`报告生成失败: ${error.message}`);
        }
    }

    /**
     * 打开报告
     */
    private async _openReport(reportId: string): Promise<void> {
        try {
            const response = await this._client.callBridge('call_mcp_tool', {
                tool_name: 'report.get',
                arguments: { report_id: reportId },
                trace_id: generateTraceId()
            });

            const resp = response as any;
            if (resp.ok && resp.data && resp.data.file_path) {
                vscode.env.openExternal(vscode.Uri.file(resp.data.file_path));
            }
        } catch (error: any) {
            vscode.window.showErrorMessage(`打开报告失败: ${error.message}`);
        }
    }

    /**
     * 删除报告
     */
    private async _deleteReport(reportId: string): Promise<void> {
        const confirm = await vscode.window.showWarningMessage(
            '确定要删除这个报告吗？',
            '删除',
            '取消'
        );

        if (confirm !== '删除') return;

        try {
            await this._client.callBridge('call_mcp_tool', {
                tool_name: 'report.delete',
                arguments: { report_id: reportId },
                trace_id: generateTraceId()
            });

            vscode.window.showInformationMessage('报告已删除');
            await this._loadReports();
        } catch (error: any) {
            vscode.window.showErrorMessage(`删除失败: ${error.message}`);
        }
    }

    // ==================== UI通信 ====================

    private _postMessage(message: any): void {
        this._panel.webview.postMessage(message);
    }

    // ==================== HTML内容 ====================

    private _getHtmlContent(): string {
        const typesHtml = REPORT_TYPES.map(t => `
            <div class="type-card" data-type="${t.id}" onclick="selectType('${t.id}')">
                <span class="type-icon">${t.icon}</span>
                <div class="type-info">
                    <div class="type-name">${t.name}</div>
                    <div class="type-desc">${t.description}</div>
                </div>
            </div>
        `).join('');

        const formatsHtml = REPORT_FORMATS.map(f => `
            <label class="format-option">
                <input type="radio" name="format" value="${f.id}" ${f.id === 'html' ? 'checked' : ''}>
                <span class="format-label">${f.icon} ${f.name}</span>
            </label>
        `).join('');

        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>报告中心</title>
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --border-primary: #30363d;
            --accent: #58a6ff;
            --success: #3fb950;
            --warning: #d29922;
            --error: #f85149;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 24px;
        }
        
        .header h1 { font-size: 24px; margin-bottom: 8px; }
        .header { margin-bottom: 24px; }
        
        .main-grid {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 24px;
        }
        
        .generate-panel, .reports-panel {
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            padding: 20px;
        }
        
        .section-title {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 12px;
        }
        
        .types-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 24px;
        }
        
        .type-card {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: var(--bg-tertiary);
            border: 2px solid transparent;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .type-card:hover,
        .type-card.selected {
            border-color: var(--accent);
        }
        
        .type-icon { font-size: 24px; }
        .type-name { font-weight: 600; }
        .type-desc { font-size: 12px; color: var(--text-secondary); }
        
        .formats-list {
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
        }
        
        .format-option {
            cursor: pointer;
        }
        
        .format-option input {
            display: none;
        }
        
        .format-label {
            display: inline-block;
            padding: 8px 16px;
            background: var(--bg-tertiary);
            border: 2px solid transparent;
            border-radius: 6px;
            transition: all 0.2s;
        }
        
        .format-option input:checked + .format-label {
            border-color: var(--accent);
            background: rgba(88, 166, 255, 0.1);
        }
        
        .form-group {
            margin-bottom: 16px;
        }
        
        .form-group label {
            display: block;
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 4px;
        }
        
        .form-group input {
            width: 100%;
            padding: 8px 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 6px;
            color: var(--text-primary);
        }
        
        .btn {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: var(--accent);
            color: white;
        }
        
        .btn-primary:hover { opacity: 0.9; }
        .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .reports-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .report-card {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px;
            background: var(--bg-tertiary);
            border-radius: 8px;
            transition: all 0.2s;
        }
        
        .report-card:hover {
            background: rgba(88, 166, 255, 0.1);
        }
        
        .report-icon {
            font-size: 28px;
        }
        
        .report-info {
            flex: 1;
        }
        
        .report-title {
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .report-meta {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .report-actions {
            display: flex;
            gap: 8px;
        }
        
        .btn-small {
            padding: 6px 12px;
            font-size: 12px;
            border-radius: 4px;
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-primary);
        }
        
        .btn-small:hover {
            background: var(--accent);
            border-color: var(--accent);
        }
        
        .btn-danger:hover {
            background: var(--error);
            border-color: var(--error);
        }
        
        .placeholder {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: var(--accent);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📄 报告中心</h1>
        <p style="color: var(--text-secondary);">生成和管理投资研究报告</p>
    </div>
    
    <div class="main-grid">
        <div class="generate-panel">
            <div class="section-title">📋 报告类型</div>
            <div class="types-list">
                ${typesHtml}
            </div>
            
            <div class="section-title">📁 输出格式</div>
            <div class="formats-list">
                ${formatsHtml}
            </div>
            
            <div class="form-group">
                <label>报告标题</label>
                <input type="text" id="report-title" value="韬睿量化研究报告">
            </div>
            
            <div class="form-group">
                <label>策略名称</label>
                <input type="text" id="strategy-name" value="动量策略">
            </div>
            
            <button class="btn btn-primary" id="generate-btn" onclick="generateReport()">
                🚀 生成报告
            </button>
        </div>
        
        <div class="reports-panel">
            <div class="section-title">📚 历史报告</div>
            <div class="reports-list" id="reports-list">
                <div class="placeholder">加载中...</div>
            </div>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        let selectedType = 'backtest';
        
        function selectType(type) {
            selectedType = type;
            document.querySelectorAll('.type-card').forEach(card => {
                card.classList.toggle('selected', card.dataset.type === type);
            });
        }
        
        function getSelectedFormat() {
            const checked = document.querySelector('input[name="format"]:checked');
            return checked ? checked.value : 'html';
        }
        
        function generateReport() {
            const btn = document.getElementById('generate-btn');
            btn.disabled = true;
            btn.textContent = '生成中...';
            
            vscode.postMessage({
                command: 'generateReport',
                type: selectedType,
                format: getSelectedFormat(),
                options: {
                    title: document.getElementById('report-title').value,
                    strategyName: document.getElementById('strategy-name').value
                }
            });
        }
        
        function openReport(reportId) {
            vscode.postMessage({ command: 'openReport', reportId });
        }
        
        function deleteReport(reportId) {
            vscode.postMessage({ command: 'deleteReport', reportId });
        }
        
        function renderReports(reports) {
            const list = document.getElementById('reports-list');
            
            if (!reports || reports.length === 0) {
                list.innerHTML = '<div class="placeholder">暂无报告</div>';
                return;
            }
            
            list.innerHTML = reports.map(r => \`
                <div class="report-card">
                    <span class="report-icon">
                        \${r.format === 'html' ? '🌐' : r.format === 'pdf' ? '📄' : '📝'}
                    </span>
                    <div class="report-info">
                        <div class="report-title">\${r.title || '报告'}</div>
                        <div class="report-meta">
                            \${r.type || 'backtest'} · \${r.format || 'html'} · \${new Date(r.created_at).toLocaleDateString()}
                        </div>
                    </div>
                    <div class="report-actions">
                        <button class="btn-small" onclick="openReport('\${r.report_id}')">打开</button>
                        <button class="btn-small btn-danger" onclick="deleteReport('\${r.report_id}')">删除</button>
                    </div>
                </div>
            \`).join('');
        }
        
        // 初始化选中
        selectType('backtest');
        
        window.addEventListener('message', event => {
            const message = event.data;
            const btn = document.getElementById('generate-btn');
            
            switch (message.command) {
                case 'reportsLoaded':
                    renderReports(message.reports);
                    break;
                    
                case 'generating':
                    // 已在按钮上处理
                    break;
                    
                case 'generated':
                    btn.disabled = false;
                    btn.textContent = '🚀 生成报告';
                    break;
                    
                case 'error':
                    btn.disabled = false;
                    btn.textContent = '🚀 生成报告';
                    break;
            }
        });
    </script>
</body>
</html>`;
    }
}
