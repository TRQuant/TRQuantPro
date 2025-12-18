/**
 * 策略优化面板 V2 - MCP集成版
 * ============================
 * 
 * 调用 optimizer-server MCP 进行参数优化:
 * - Grid Search: 参数网格搜索
 * - Optuna: 智能优化
 * - Walk Forward: 滚动验证
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';
import { generateTraceId } from '../services/mcpClientV2';

const MODULE = 'OptimizerPanel';

// 优化方法
const OPTIMIZE_METHODS = [
    {
        id: 'grid_search',
        name: '网格搜索',
        icon: '🔲',
        tool: 'optimizer.grid_search',
        description: '穷举所有参数组合，找到最优配置'
    },
    {
        id: 'optuna',
        name: 'Optuna智能优化',
        icon: '🧠',
        tool: 'optimizer.optuna',
        description: 'TPE算法智能搜索最优参数'
    },
    {
        id: 'walk_forward',
        name: '滚动验证',
        icon: '📊',
        tool: 'optimizer.walk_forward',
        description: '样本外验证，防止过拟合'
    }
];

// 可优化参数
const OPTIMIZABLE_PARAMS = [
    { name: 'lookback', label: '回看周期', min: 5, max: 60, step: 5, default: [10, 20, 30] },
    { name: 'top_n', label: '选股数量', min: 3, max: 30, step: 3, default: [5, 10, 15] },
    { name: 'stop_loss', label: '止损比例', min: 0.03, max: 0.15, step: 0.02, default: [0.05, 0.08, 0.10] },
    { name: 'take_profit', label: '止盈比例', min: 0.10, max: 0.50, step: 0.05, default: [0.15, 0.20, 0.30] }
];

export class OptimizerPanel {
    public static currentPanel: OptimizerPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];
    
    private _strategyCode: string = '';
    private _baseResult: any = null;
    private _optimizeResults: any[] = [];

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient,
        options?: { code?: string; baseResult?: any }
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._client = client;
        this._strategyCode = options?.code || '';
        this._baseResult = options?.baseResult || null;

        this._panel.webview.html = this._getHtmlContent();
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        this._panel.webview.onDidReceiveMessage(
            message => this._handleMessage(message),
            null,
            this._disposables
        );
    }

    public static createOrShow(
        extensionUri: vscode.Uri,
        client: TRQuantClient,
        options?: { code?: string; baseResult?: any }
    ): OptimizerPanel {
        logger.info('创建优化面板V2', MODULE);
        
        const column = vscode.ViewColumn.One;

        if (OptimizerPanel.currentPanel) {
            OptimizerPanel.currentPanel._panel.reveal(column);
            return OptimizerPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'trquantOptimizerV2',
            '⚙️ 参数优化',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        OptimizerPanel.currentPanel = new OptimizerPanel(panel, extensionUri, client, options);
        return OptimizerPanel.currentPanel;
    }

    public dispose(): void {
        OptimizerPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }

    // ==================== 消息处理 ====================

    private async _handleMessage(message: any): Promise<void> {
        logger.info(`[OptimizerPanel] 收到消息: ${message.command}`, MODULE);

        switch (message.command) {
            case 'runOptimize':
                await this._runOptimize(message.method, message.config);
                break;
            case 'applyBest':
                await this._applyBestParams(message.params);
                break;
            case 'generateReport':
                await this._generateCompareReport();
                break;
        }
    }

    // ==================== MCP调用 ====================

    /**
     * 执行优化
     */
    private async _runOptimize(method: string, config: any): Promise<void> {
        const methodInfo = OPTIMIZE_METHODS.find(m => m.id === method);
        if (!methodInfo) {
            vscode.window.showErrorMessage(`未知优化方法: ${method}`);
            return;
        }

        this._postMessage({ command: 'optimizeStarted', method });

        try {
            const startTime = Date.now();
            
            const args: any = {
                strategy_type: config.strategyType || 'momentum',
                securities: config.securities || ['000001.XSHE', '600000.XSHG'],
                start_date: config.startDate,
                end_date: config.endDate
            };

            if (method === 'grid_search') {
                args.param_ranges = config.paramRanges;
            } else if (method === 'optuna') {
                args.param_space = config.paramRanges;
                args.n_trials = config.nTrials || 50;
            } else if (method === 'walk_forward') {
                args.window_size = config.windowSize || 252;
            }

            logger.info(`执行优化: ${methodInfo.tool}`, MODULE, args);

            const response = await this._client.callBridge('call_mcp_tool', {
                tool_name: methodInfo.tool,
                arguments: args,
                trace_id: generateTraceId()
            });

            const resp = response as any;
            const duration = (Date.now() - startTime) / 1000;

            if (resp.ok && resp.data) {
                this._optimizeResults = resp.data.all_results || [];
                
                this._postMessage({
                    command: 'optimizeCompleted',
                    method,
                    result: resp.data,
                    duration
                });

                logger.info(`优化完成: ${method}, 耗时 ${duration.toFixed(2)}s`, MODULE);
            } else {
                throw new Error(resp.error || '优化失败');
            }
        } catch (error: any) {
            logger.error(`优化失败: ${error.message}`, MODULE);
            this._postMessage({
                command: 'optimizeFailed',
                method,
                error: error.message
            });
            vscode.window.showErrorMessage(`优化失败: ${error.message}`);
        }
    }

    /**
     * 应用最优参数
     */
    private async _applyBestParams(params: Record<string, unknown>): Promise<void> {
        // 触发策略生成面板，使用最优参数
        await vscode.commands.executeCommand('trquant.openStrategyGenerator', { params });
    }

    /**
     * 生成对比报告
     */
    private async _generateCompareReport(): Promise<void> {
        if (this._optimizeResults.length === 0) {
            vscode.window.showWarningMessage('请先运行优化');
            return;
        }

        try {
            const response = await this._client.callBridge('call_mcp_tool', {
                tool_name: 'report.compare',
                arguments: {
                    results: this._optimizeResults.slice(0, 10)
                },
                trace_id: generateTraceId()
            });

            const resp = response as any;
            if (resp.ok && resp.data) {
                vscode.window.showInformationMessage(`对比报告已生成: ${resp.data.file_path}`);
            }
        } catch (error: any) {
            vscode.window.showErrorMessage(`报告生成失败: ${error.message}`);
        }
    }

    // ==================== UI通信 ====================

    private _postMessage(message: any): void {
        this._panel.webview.postMessage(message);
    }

    // ==================== HTML内容 ====================

    private _getHtmlContent(): string {
        const methodsHtml = OPTIMIZE_METHODS.map(m => `
            <div class="method-card" data-method="${m.id}">
                <span class="method-icon">${m.icon}</span>
                <div class="method-info">
                    <div class="method-name">${m.name}</div>
                    <div class="method-desc">${m.description}</div>
                </div>
                <input type="radio" name="method" value="${m.id}" ${m.id === 'grid_search' ? 'checked' : ''}>
            </div>
        `).join('');

        const paramsHtml = OPTIMIZABLE_PARAMS.map(p => `
            <div class="param-config">
                <div class="param-header">
                    <label>
                        <input type="checkbox" class="param-enabled" data-param="${p.name}" checked>
                        ${p.label}
                    </label>
                </div>
                <div class="param-values">
                    <input type="text" class="param-range" data-param="${p.name}" 
                           value="${p.default.join(', ')}" 
                           placeholder="输入值，逗号分隔">
                </div>
            </div>
        `).join('');

        const defaultStartDate = new Date();
        defaultStartDate.setMonth(defaultStartDate.getMonth() - 6);
        const startDateStr = defaultStartDate.toISOString().split('T')[0];
        const endDateStr = new Date().toISOString().split('T')[0];

        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>参数优化</title>
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
            grid-template-columns: 400px 1fr;
            gap: 24px;
        }
        
        .config-panel, .result-panel {
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
        
        .methods-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 24px;
        }
        
        .method-card {
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
        
        .method-card:hover,
        .method-card:has(input:checked) {
            border-color: var(--accent);
        }
        
        .method-icon { font-size: 24px; }
        .method-info { flex: 1; }
        .method-name { font-weight: 600; }
        .method-desc { font-size: 12px; color: var(--text-secondary); }
        
        .method-card input { display: none; }
        
        .params-config {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 24px;
        }
        
        .param-config {
            background: var(--bg-tertiary);
            border-radius: 8px;
            padding: 12px;
        }
        
        .param-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }
        
        .param-header label {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }
        
        .param-range {
            width: 100%;
            padding: 8px;
            background: var(--bg-primary);
            border: 1px solid var(--border-primary);
            border-radius: 4px;
            color: var(--text-primary);
            font-size: 13px;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
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
            padding: 8px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 4px;
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
        
        .progress-container {
            margin-bottom: 24px;
        }
        
        .progress-bar {
            height: 8px;
            background: var(--bg-tertiary);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent), var(--success));
            width: 0%;
            transition: width 0.3s;
        }
        
        .progress-text {
            text-align: center;
            margin-top: 8px;
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .best-result {
            background: rgba(63, 185, 80, 0.1);
            border: 2px solid var(--success);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
        }
        
        .best-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--success);
            margin-bottom: 12px;
        }
        
        .best-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .best-metric {
            text-align: center;
        }
        
        .best-metric-value {
            font-size: 20px;
            font-weight: 700;
            color: var(--success);
        }
        
        .best-metric-label {
            font-size: 11px;
            color: var(--text-secondary);
        }
        
        .best-params {
            font-size: 13px;
            color: var(--text-secondary);
        }
        
        .results-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .results-table th, .results-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid var(--border-primary);
            font-size: 13px;
        }
        
        .results-table th {
            color: var(--text-secondary);
            font-weight: 600;
        }
        
        .results-table tr:hover {
            background: var(--bg-tertiary);
        }
        
        .placeholder {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚙️ 参数优化</h1>
        <p style="color: var(--text-secondary);">搜索最优策略参数，提升策略表现</p>
    </div>
    
    <div class="main-grid">
        <div class="config-panel">
            <div class="section-title">🔧 优化方法</div>
            <div class="methods-list">
                ${methodsHtml}
            </div>
            
            <div class="section-title">📊 参数范围</div>
            <div class="params-config">
                ${paramsHtml}
            </div>
            
            <div class="section-title">📅 回测区间</div>
            <div class="form-row">
                <div class="form-group">
                    <label>开始日期</label>
                    <input type="date" id="start-date" value="${startDateStr}">
                </div>
                <div class="form-group">
                    <label>结束日期</label>
                    <input type="date" id="end-date" value="${endDateStr}">
                </div>
            </div>
            
            <button class="btn btn-primary" id="optimize-btn" onclick="runOptimize()">
                🚀 开始优化
            </button>
        </div>
        
        <div class="result-panel">
            <div class="section-title">📈 优化结果</div>
            
            <div class="progress-container" id="progress" style="display: none;">
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill"></div>
                </div>
                <div class="progress-text" id="progress-text">准备中...</div>
            </div>
            
            <div id="result-content">
                <div class="placeholder">配置参数范围并点击"开始优化"</div>
            </div>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function getSelectedMethod() {
            const checked = document.querySelector('input[name="method"]:checked');
            return checked ? checked.value : 'grid_search';
        }
        
        function getParamRanges() {
            const ranges = {};
            document.querySelectorAll('.param-config').forEach(config => {
                const enabled = config.querySelector('.param-enabled');
                const input = config.querySelector('.param-range');
                
                if (enabled.checked) {
                    const param = enabled.dataset.param;
                    const values = input.value.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v));
                    if (values.length > 0) {
                        ranges[param] = values;
                    }
                }
            });
            return ranges;
        }
        
        function runOptimize() {
            const btn = document.getElementById('optimize-btn');
            btn.disabled = true;
            btn.textContent = '优化中...';
            
            document.getElementById('progress').style.display = 'block';
            
            vscode.postMessage({
                command: 'runOptimize',
                method: getSelectedMethod(),
                config: {
                    paramRanges: getParamRanges(),
                    startDate: document.getElementById('start-date').value,
                    endDate: document.getElementById('end-date').value,
                    strategyType: 'momentum',
                    securities: ['000001.XSHE', '600000.XSHG', '000002.XSHE']
                }
            });
        }
        
        function applyBest(params) {
            vscode.postMessage({ command: 'applyBest', params });
        }
        
        function formatPercent(value) {
            return (value * 100).toFixed(2) + '%';
        }
        
        function renderResult(result) {
            const content = document.getElementById('result-content');
            const best = result.best_params || {};
            const allResults = result.all_results || [];
            
            let html = '';
            
            // 最佳结果
            html += \`
                <div class="best-result">
                    <div class="best-title">🏆 最优参数组合</div>
                    <div class="best-metrics">
                        <div class="best-metric">
                            <div class="best-metric-value">\${(result.best_sharpe || 0).toFixed(2)}</div>
                            <div class="best-metric-label">夏普比率</div>
                        </div>
                        <div class="best-metric">
                            <div class="best-metric-value">\${formatPercent(result.best_return || 0)}</div>
                            <div class="best-metric-label">总收益</div>
                        </div>
                        <div class="best-metric">
                            <div class="best-metric-value">\${result.total_trials || 0}</div>
                            <div class="best-metric-label">测试组合数</div>
                        </div>
                    </div>
                    <div class="best-params">
                        <strong>最优参数:</strong> \${JSON.stringify(best)}
                    </div>
                    <button class="btn btn-primary" style="margin-top: 12px;" onclick='applyBest(\${JSON.stringify(best)})'>
                        ✅ 应用最优参数
                    </button>
                </div>
            \`;
            
            // 所有结果表格
            if (allResults.length > 0) {
                html += \`
                    <div class="section-title">📋 所有结果 (Top 20)</div>
                    <table class="results-table">
                        <tr>
                            <th>排名</th>
                            <th>参数</th>
                            <th>夏普</th>
                            <th>收益</th>
                            <th>回撤</th>
                        </tr>
                        \${allResults.slice(0, 20).map((r, i) => \`
                            <tr>
                                <td>\${i + 1}</td>
                                <td>\${JSON.stringify(r.params || {})}</td>
                                <td>\${(r.sharpe || 0).toFixed(2)}</td>
                                <td>\${formatPercent(r.return_pct || 0)}</td>
                                <td>\${formatPercent(Math.abs(r.drawdown || 0))}</td>
                            </tr>
                        \`).join('')}
                    </table>
                \`;
            }
            
            content.innerHTML = html;
        }
        
        window.addEventListener('message', event => {
            const message = event.data;
            const btn = document.getElementById('optimize-btn');
            const progress = document.getElementById('progress');
            
            switch (message.command) {
                case 'optimizeStarted':
                    document.getElementById('progress-fill').style.width = '10%';
                    document.getElementById('progress-text').textContent = '正在搜索最优参数...';
                    break;
                    
                case 'optimizeCompleted':
                    btn.disabled = false;
                    btn.textContent = '🚀 开始优化';
                    progress.style.display = 'none';
                    renderResult(message.result);
                    break;
                    
                case 'optimizeFailed':
                    btn.disabled = false;
                    btn.textContent = '🚀 开始优化';
                    progress.style.display = 'none';
                    document.getElementById('result-content').innerHTML = 
                        '<div class="placeholder" style="color: var(--error);">优化失败: ' + message.error + '</div>';
                    break;
            }
        });
        
        // 方法卡片点击
        document.querySelectorAll('.method-card').forEach(card => {
            card.addEventListener('click', () => {
                card.querySelector('input').checked = true;
            });
        });
    </script>
</body>
</html>`;
    }
}
