/**
 * 回测面板 V2 - MCP集成版
 * =======================
 * 
 * 调用 backtest-server MCP 执行三层回测:
 * - Fast: 快速回测 (<5秒)
 * - Standard: 标准回测 (<30秒)
 * - Precise: BulletTrade/QMT 精确回测
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';
import { generateTraceId } from '../services/mcpClientV2';

const MODULE = 'BacktestPanel';

// 回测层级
const BACKTEST_LEVELS = [
    {
        id: 'fast',
        name: '快速回测',
        icon: '⚡',
        color: '#3fb950',
        tool: 'backtest.fast',
        description: '向量化计算，<5秒完成，用于策略初筛',
        features: ['向量化计算', '无滑点模拟', '秒级响应']
    },
    {
        id: 'standard',
        name: '标准回测',
        icon: '📊',
        color: '#58a6ff',
        tool: 'backtest.standard',
        description: '事件驱动，完整交易成本模拟',
        features: ['事件驱动', '交易成本', '持仓管理']
    },
    {
        id: 'bullettrade',
        name: 'BulletTrade',
        icon: '🎯',
        color: '#d29922',
        tool: 'backtest.bullettrade',
        description: 'BulletTrade引擎，支持复杂策略',
        features: ['完整模拟', 'HTML报告', '分钟级数据']
    },
    {
        id: 'qmt',
        name: 'QMT回测',
        icon: '📈',
        color: '#a371f7',
        tool: 'backtest.qmt',
        description: 'xtquant引擎，生产级回测',
        features: ['生产级引擎', 'Tick数据', '实盘一致']
    }
];

export class BacktestPanel {
    public static currentPanel: BacktestPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];
    
    private _lastResult: any = null;
    private _strategyCode: string = '';

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient,
        options?: { code?: string }
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._client = client;
        this._strategyCode = options?.code || '';

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
        options?: { code?: string }
    ): BacktestPanel {
        logger.info('创建回测面板V2', MODULE);
        
        const column = vscode.ViewColumn.One;

        if (BacktestPanel.currentPanel) {
            BacktestPanel.currentPanel._panel.reveal(column);
            if (options?.code) {
                BacktestPanel.currentPanel._strategyCode = options.code;
            }
            return BacktestPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'trquantBacktestV2',
            '🔄 回测验证',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        BacktestPanel.currentPanel = new BacktestPanel(panel, extensionUri, client, options);
        return BacktestPanel.currentPanel;
    }

    public dispose(): void {
        BacktestPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }

    // ==================== 消息处理 ====================

    private async _handleMessage(message: any): Promise<void> {
        logger.info(`[BacktestPanel] 收到消息: ${message.command}`, MODULE);

        switch (message.command) {
            case 'runBacktest':
                await this._runBacktest(message.level, message.config);
                break;
            case 'generateReport':
                await this._generateReport();
                break;
            case 'openReport':
                await this._openReport();
                break;
            case 'optimize':
                await this._openOptimizer();
                break;
        }
    }

    // ==================== MCP调用 ====================

    /**
     * 执行回测
     */
    private async _runBacktest(level: string, config: any): Promise<void> {
        const levelInfo = BACKTEST_LEVELS.find(l => l.id === level);
        if (!levelInfo) {
            vscode.window.showErrorMessage(`未知回测层级: ${level}`);
            return;
        }

        this._postMessage({ command: 'backtestStarted', level });

        try {
            const startTime = Date.now();
            
            // 构建参数
            const args: any = {
                start_date: config.startDate,
                end_date: config.endDate,
                initial_capital: config.initialCapital || 1000000
            };

            if (level === 'fast' || level === 'standard') {
                args.securities = config.securities || ['000001.XSHE', '600000.XSHG', '000002.XSHE'];
                args.strategy = config.strategy || 'momentum';
                args.lookback = config.lookback || 20;
                args.top_n = config.topN || 10;
            }

            if (level === 'bullettrade' || level === 'qmt') {
                args.strategy_code = this._strategyCode || config.strategyCode;
                args.strategy_file = config.strategyFile;
            }

            logger.info(`执行回测: ${levelInfo.tool}`, MODULE, args);

            const response = await this._client.callBridge('call_mcp_tool', {
                tool_name: levelInfo.tool,
                arguments: args,
                trace_id: generateTraceId()
            });

            const resp = response as any;
            const duration = (Date.now() - startTime) / 1000;

            if (resp.ok && resp.data) {
                this._lastResult = resp.data;
                
                this._postMessage({
                    command: 'backtestCompleted',
                    level,
                    result: resp.data,
                    duration
                });

                logger.info(`回测完成: ${level}, 耗时 ${duration.toFixed(2)}s`, MODULE);
            } else {
                throw new Error(resp.error || '回测失败');
            }
        } catch (error: any) {
            logger.error(`回测失败: ${error.message}`, MODULE);
            this._postMessage({
                command: 'backtestFailed',
                level,
                error: error.message
            });
            vscode.window.showErrorMessage(`回测失败: ${error.message}`);
        }
    }

    /**
     * 生成报告
     */
    private async _generateReport(): Promise<void> {
        if (!this._lastResult) {
            vscode.window.showWarningMessage('请先运行回测');
            return;
        }

        try {
            const response = await this._client.callBridge('call_mcp_tool', {
                tool_name: 'report.generate',
                arguments: {
                    result: this._lastResult,
                    format: 'html',
                    title: '回测报告'
                },
                trace_id: generateTraceId()
            });

            const resp = response as any;
            if (resp.ok && resp.data) {
                vscode.window.showInformationMessage(`报告已生成: ${resp.data.file_path}`);
                
                // 尝试打开报告
                if (resp.data.file_path) {
                    vscode.env.openExternal(vscode.Uri.file(resp.data.file_path));
                }
            }
        } catch (error: any) {
            vscode.window.showErrorMessage(`报告生成失败: ${error.message}`);
        }
    }

    /**
     * 打开报告
     */
    private async _openReport(): Promise<void> {
        // 打开报告面板
        await vscode.commands.executeCommand('trquant.openReportPanel', { result: this._lastResult });
    }

    /**
     * 打开优化器
     */
    private async _openOptimizer(): Promise<void> {
        await vscode.commands.executeCommand('trquant.openOptimizerPanel', { 
            code: this._strategyCode,
            baseResult: this._lastResult 
        });
    }

    // ==================== UI通信 ====================

    private _postMessage(message: any): void {
        this._panel.webview.postMessage(message);
    }

    // ==================== HTML内容 ====================

    private _getHtmlContent(): string {
        const levelsHtml = BACKTEST_LEVELS.map(l => `
            <div class="level-card" data-level="${l.id}">
                <div class="level-header">
                    <span class="level-icon" style="color: ${l.color}">${l.icon}</span>
                    <span class="level-name">${l.name}</span>
                </div>
                <div class="level-desc">${l.description}</div>
                <div class="level-features">
                    ${l.features.map(f => `<span class="feature-tag">${f}</span>`).join('')}
                </div>
                <button class="btn btn-run" onclick="runBacktest('${l.id}')">▶ 执行</button>
            </div>
        `).join('');

        const defaultStartDate = new Date();
        defaultStartDate.setMonth(defaultStartDate.getMonth() - 3);
        const startDateStr = defaultStartDate.toISOString().split('T')[0];
        const endDateStr = new Date().toISOString().split('T')[0];

        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>回测验证</title>
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
        
        .header {
            margin-bottom: 24px;
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 8px;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }
        
        .config-section, .result-section {
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            padding: 20px;
        }
        
        .section-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .config-form {
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .form-group label {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .form-group input, .form-group select {
            padding: 8px 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 14px;
        }
        
        .levels-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        
        .level-card {
            background: var(--bg-tertiary);
            border: 2px solid transparent;
            border-radius: 10px;
            padding: 16px;
            transition: all 0.2s;
        }
        
        .level-card:hover {
            border-color: var(--accent);
        }
        
        .level-card.running {
            border-color: var(--warning);
            animation: pulse 1.5s infinite;
        }
        
        .level-card.completed {
            border-color: var(--success);
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .level-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }
        
        .level-icon {
            font-size: 20px;
        }
        
        .level-name {
            font-weight: 600;
        }
        
        .level-desc {
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 12px;
        }
        
        .level-features {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            margin-bottom: 12px;
        }
        
        .feature-tag {
            font-size: 10px;
            padding: 2px 6px;
            background: rgba(88, 166, 255, 0.1);
            color: var(--accent);
            border-radius: 4px;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .btn-run {
            width: 100%;
            background: var(--success);
            color: white;
        }
        
        .btn-run:hover {
            opacity: 0.9;
        }
        
        .btn-run:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 24px;
        }
        
        .metric-card {
            background: var(--bg-tertiary);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 4px;
        }
        
        .metric-value.positive { color: var(--success); }
        .metric-value.negative { color: var(--error); }
        
        .metric-label {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .result-actions {
            display: flex;
            gap: 12px;
        }
        
        .btn-secondary {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border-primary);
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
        <h1>🔄 回测验证</h1>
        <p style="color: var(--text-secondary);">三层回测架构：快速筛选 → 标准验证 → 精确模拟</p>
    </div>
    
    <div class="main-grid">
        <div class="config-section">
            <div class="section-title">⚙️ 回测配置</div>
            
            <div class="config-form">
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
                <div class="form-row">
                    <div class="form-group">
                        <label>初始资金</label>
                        <input type="number" id="initial-capital" value="1000000">
                    </div>
                    <div class="form-group">
                        <label>策略类型</label>
                        <select id="strategy">
                            <option value="momentum">动量策略</option>
                            <option value="mean_reversion">均值回归</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <label>股票代码 (逗号分隔)</label>
                    <input type="text" id="securities" value="000001.XSHE, 600000.XSHG, 000002.XSHE, 600036.XSHG">
                </div>
            </div>
            
            <div class="section-title">📊 回测层级</div>
            <div class="levels-grid">
                ${levelsHtml}
            </div>
        </div>
        
        <div class="result-section">
            <div class="section-title">📈 回测结果</div>
            
            <div id="result-content">
                <div class="placeholder">选择回测层级并执行</div>
            </div>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function getConfig() {
            return {
                startDate: document.getElementById('start-date').value,
                endDate: document.getElementById('end-date').value,
                initialCapital: parseInt(document.getElementById('initial-capital').value),
                strategy: document.getElementById('strategy').value,
                securities: document.getElementById('securities').value.split(',').map(s => s.trim())
            };
        }
        
        function runBacktest(level) {
            const card = document.querySelector('[data-level="' + level + '"]');
            const btn = card.querySelector('.btn-run');
            
            btn.disabled = true;
            btn.textContent = '执行中...';
            card.classList.add('running');
            
            vscode.postMessage({
                command: 'runBacktest',
                level,
                config: getConfig()
            });
        }
        
        function formatPercent(value) {
            return (value * 100).toFixed(2) + '%';
        }
        
        function renderResult(result) {
            const metrics = result.metrics || result;
            const content = document.getElementById('result-content');
            
            const totalReturn = metrics.total_return || 0;
            const annualReturn = metrics.annual_return || 0;
            const sharpe = metrics.sharpe_ratio || 0;
            const maxDrawdown = metrics.max_drawdown || 0;
            const winRate = metrics.win_rate || 0;
            const trades = metrics.total_trades || 0;
            
            content.innerHTML = \`
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value \${totalReturn >= 0 ? 'positive' : 'negative'}">\${formatPercent(totalReturn)}</div>
                        <div class="metric-label">总收益</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value \${annualReturn >= 0 ? 'positive' : 'negative'}">\${formatPercent(annualReturn)}</div>
                        <div class="metric-label">年化收益</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value \${sharpe >= 1 ? 'positive' : ''}">\${sharpe.toFixed(2)}</div>
                        <div class="metric-label">夏普比率</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value negative">\${formatPercent(Math.abs(maxDrawdown))}</div>
                        <div class="metric-label">最大回撤</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value \${winRate >= 0.5 ? 'positive' : ''}">\${formatPercent(winRate)}</div>
                        <div class="metric-label">胜率</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">\${trades}</div>
                        <div class="metric-label">交易次数</div>
                    </div>
                </div>
                <div class="result-actions">
                    <button class="btn btn-secondary" onclick="generateReport()">📄 生成报告</button>
                    <button class="btn btn-secondary" onclick="optimize()">⚙️ 参数优化</button>
                </div>
            \`;
        }
        
        function generateReport() {
            vscode.postMessage({ command: 'generateReport' });
        }
        
        function optimize() {
            vscode.postMessage({ command: 'optimize' });
        }
        
        window.addEventListener('message', event => {
            const message = event.data;
            
            switch (message.command) {
                case 'backtestStarted': {
                    // 已在runBacktest中处理
                    break;
                }
                
                case 'backtestCompleted': {
                    const card = document.querySelector('[data-level="' + message.level + '"]');
                    const btn = card.querySelector('.btn-run');
                    
                    btn.disabled = false;
                    btn.textContent = '✅ 完成 (' + message.duration.toFixed(1) + 's)';
                    card.classList.remove('running');
                    card.classList.add('completed');
                    
                    renderResult(message.result);
                    break;
                }
                
                case 'backtestFailed': {
                    const card = document.querySelector('[data-level="' + message.level + '"]');
                    const btn = card.querySelector('.btn-run');
                    
                    btn.disabled = false;
                    btn.textContent = '❌ 重试';
                    card.classList.remove('running');
                    
                    document.getElementById('result-content').innerHTML = 
                        '<div class="placeholder" style="color: var(--error);">回测失败: ' + message.error + '</div>';
                    break;
                }
            }
        });
    </script>
</body>
</html>`;
    }
}
