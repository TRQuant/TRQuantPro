/**
 * BulletTrade 回测面板
 * ===================
 * 
 * 策略回测配置、执行和结果展示
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';

const MODULE = 'BulletTradeBacktestPanel';

interface BacktestConfig {
    strategyPath: string;
    startDate: string;
    endDate: string;
    frequency: string;
    initialCapital: number;
    benchmark: string;
    commissionRate: number;
    slippage: number;
    dataProvider: string;
}

interface BacktestResult {
    success: boolean;
    metrics?: {
        totalReturn: number;
        annualReturn: number;
        maxDrawdown: number;
        sharpeRatio: number;
        winRate: number;
        tradeCount: number;
        profitFactor: number;
        volatility: number;
    };
    equityCurve?: Array<{ date: string; equity: number; dailyReturn: number }>;
    trades?: Array<{ date: string; symbol: string; direction: string; price: number; volume: number }>;
    error?: string;
}

export class BulletTradeBacktestPanel {
    public static currentPanel: BulletTradeBacktestPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];
    
    private _config: BacktestConfig = {
        strategyPath: '',
        startDate: '2020-01-01',
        endDate: '2023-12-31',
        frequency: 'day',
        initialCapital: 1000000,
        benchmark: '000300.XSHG',
        commissionRate: 0.0003,
        slippage: 0.001,
        dataProvider: 'mock'
    };
    
    private _result: BacktestResult | null = null;
    private _isRunning: boolean = false;

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
        this.updateContent();
    }

    public static createOrShow(
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ): BulletTradeBacktestPanel {
        const column = vscode.ViewColumn.One;

        if (BulletTradeBacktestPanel.currentPanel) {
            BulletTradeBacktestPanel.currentPanel._panel.reveal(column);
            return BulletTradeBacktestPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'bullettradeBacktest',
            '🧪 BulletTrade 回测',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        BulletTradeBacktestPanel.currentPanel = new BulletTradeBacktestPanel(panel, extensionUri, client);
        return BulletTradeBacktestPanel.currentPanel;
    }

    private async handleMessage(message: { command: string; [key: string]: unknown }): Promise<void> {
        logger.debug(`收到消息: ${message.command}`, MODULE);
        
        switch (message.command) {
            case 'selectStrategy':
                await this.selectStrategy();
                break;
            case 'updateConfig':
                this.updateConfig(message.config as Partial<BacktestConfig>);
                break;
            case 'runBacktest':
                await this.runBacktest();
                break;
            case 'exportResult':
                await this.exportResult();
                break;
            case 'analyzeWithAI':
                await this.analyzeWithAI();
                break;
            default:
                logger.warn(`未知命令: ${message.command}`, MODULE);
        }
    }

    private async selectStrategy(): Promise<void> {
        const options: vscode.OpenDialogOptions = {
            canSelectMany: false,
            filters: {
                'Python Strategy': ['py']
            },
            title: '选择策略文件'
        };

        const fileUri = await vscode.window.showOpenDialog(options);
        if (fileUri && fileUri[0]) {
            this._config.strategyPath = fileUri[0].fsPath;
            this.updateContent();
        }
    }

    private updateConfig(config: Partial<BacktestConfig>): void {
        this._config = { ...this._config, ...config };
        this.updateContent();
    }

    private async runBacktest(): Promise<void> {
        if (this._isRunning) {
            vscode.window.showWarningMessage('回测正在运行中...');
            return;
        }

        if (!this._config.strategyPath) {
            vscode.window.showErrorMessage('请先选择策略文件');
            return;
        }

        this._isRunning = true;
        this._result = null;
        this.updateContent();

        try {
            // 调用 Python 后端执行回测
            const response = await this._client.callBridge<Record<string, unknown>>('run_bt_backtest', {
                strategy_path: this._config.strategyPath,
                start_date: this._config.startDate,
                end_date: this._config.endDate,
                frequency: this._config.frequency,
                initial_capital: this._config.initialCapital,
                benchmark: this._config.benchmark,
                commission_rate: this._config.commissionRate,
                slippage: this._config.slippage,
                data_provider: this._config.dataProvider
            });

            if (response.ok && response.data) {
                const data = response.data as Record<string, unknown>;
                this._result = {
                    success: data.success as boolean,
                    metrics: data.metrics as BacktestResult['metrics'],
                    equityCurve: data.equity_curve as BacktestResult['equityCurve'],
                    trades: data.trades as BacktestResult['trades'],
                    error: data.error as string | undefined
                };
                vscode.window.showInformationMessage('✅ 回测完成！');
            } else {
                this._result = {
                    success: false,
                    error: response.error || '回测执行失败'
                };
                vscode.window.showErrorMessage(`回测失败: ${response.error}`);
            }
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            this._result = {
                success: false,
                error: errorMsg
            };
            vscode.window.showErrorMessage(`回测失败: ${errorMsg}`);
        } finally {
            this._isRunning = false;
            this.updateContent();
        }
    }

    private async exportResult(): Promise<void> {
        if (!this._result || !this._result.success) {
            vscode.window.showWarningMessage('没有可导出的回测结果');
            return;
        }

        const options: vscode.SaveDialogOptions = {
            filters: {
                'JSON': ['json'],
                'Markdown': ['md']
            },
            title: '导出回测结果'
        };

        const fileUri = await vscode.window.showSaveDialog(options);
        if (fileUri) {
            const fs = require('fs');
            const ext = fileUri.fsPath.split('.').pop();
            
            if (ext === 'json') {
                fs.writeFileSync(fileUri.fsPath, JSON.stringify(this._result, null, 2));
            } else {
                // 生成 Markdown 报告
                const report = this.generateMarkdownReport();
                fs.writeFileSync(fileUri.fsPath, report);
            }
            
            vscode.window.showInformationMessage(`结果已导出到: ${fileUri.fsPath}`);
        }
    }

    private generateMarkdownReport(): string {
        if (!this._result || !this._result.metrics) {
            return '# 回测报告\n\n暂无数据';
        }

        const m = this._result.metrics;
        return `# 📊 策略回测报告

## 基本信息

- **策略文件**: ${this._config.strategyPath}
- **回测区间**: ${this._config.startDate} ~ ${this._config.endDate}
- **初始资金**: ¥${this._config.initialCapital.toLocaleString()}
- **基准指数**: ${this._config.benchmark}

## 核心指标

| 指标 | 值 |
|------|-----|
| 总收益率 | ${m.totalReturn.toFixed(2)}% |
| 年化收益 | ${m.annualReturn.toFixed(2)}% |
| 最大回撤 | ${m.maxDrawdown.toFixed(2)}% |
| 夏普比率 | ${m.sharpeRatio.toFixed(2)} |
| 胜率 | ${m.winRate.toFixed(2)}% |
| 交易次数 | ${m.tradeCount} |
| 盈亏比 | ${m.profitFactor.toFixed(2)} |
| 波动率 | ${m.volatility.toFixed(2)}% |

---
*报告由 TRQuant 自动生成*
`;
    }

    private async analyzeWithAI(): Promise<void> {
        if (!this._result || !this._result.success) {
            vscode.window.showWarningMessage('没有可分析的回测结果');
            return;
        }

        vscode.window.showInformationMessage('🤖 AI 正在分析回测结果...');
        
        try {
            const response = await this._client.callBridge<{ analysis: string }>('analyze_bt_result', {
                result: this._result
            });

            if (response.ok && response.data) {
                // 在新窗口显示分析结果
                const doc = await vscode.workspace.openTextDocument({
                    content: response.data.analysis || String(response.data),
                    language: 'markdown'
                });
                await vscode.window.showTextDocument(doc);
            }
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            vscode.window.showErrorMessage(`AI 分析失败: ${errorMsg}`);
        }
    }

    private updateContent(): void {
        this._panel.webview.html = this.generateHtml();
    }

    private generateHtml(): string {
        const metrics = this._result?.metrics;
        
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BulletTrade 回测</title>
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
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-dark);
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
            border-bottom: 1px solid var(--border-color);
        }
        
        .header h1 {
            font-size: 24px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .header-actions {
            display: flex;
            gap: 12px;
        }
        
        .btn {
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #f0b429 0%, #e85d04 100%);
            color: #fff;
            font-weight: 600;
        }
        
        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(240, 180, 41, 0.3);
        }
        
        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-secondary {
            background: var(--bg-secondary);
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
        }
        
        .btn-secondary:hover {
            background: var(--bg-hover);
            border-color: var(--accent-blue);
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 24px;
        }
        
        .config-panel {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
        }
        
        .config-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .form-group {
            margin-bottom: 16px;
        }
        
        .form-label {
            display: block;
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }
        
        .form-input {
            width: 100%;
            padding: 10px 12px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 14px;
        }
        
        .form-input:focus {
            outline: none;
            border-color: var(--accent-blue);
        }
        
        .form-select {
            width: 100%;
            padding: 10px 12px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 14px;
        }
        
        .file-select {
            display: flex;
            gap: 8px;
        }
        
        .file-select input {
            flex: 1;
        }
        
        .file-select button {
            padding: 10px 16px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-secondary);
            cursor: pointer;
        }
        
        .file-select button:hover {
            background: var(--bg-hover);
        }
        
        .result-panel {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
        }
        
        .result-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .metric-card {
            background: var(--bg-card);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }
        
        .metric-label {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 700;
        }
        
        .metric-value.positive { color: var(--accent-green); }
        .metric-value.negative { color: var(--accent-red); }
        .metric-value.neutral { color: var(--accent-blue); }
        
        .empty-state {
            text-align: center;
            padding: 60px 40px;
            color: var(--text-muted);
        }
        
        .empty-state .icon {
            font-size: 48px;
            margin-bottom: 16px;
        }
        
        .running-state {
            text-align: center;
            padding: 60px 40px;
        }
        
        .running-state .spinner {
            width: 48px;
            height: 48px;
            border: 4px solid var(--border-color);
            border-top-color: var(--accent-gold);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 16px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .trades-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .trades-table th,
        .trades-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        .trades-table th {
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 600;
        }
        
        .trade-buy { color: var(--accent-red); }
        .trade-sell { color: var(--accent-green); }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 BulletTrade 回测</h1>
        <div class="header-actions">
            <button class="btn btn-secondary" onclick="vscode.postMessage({command: 'exportResult'})" ${!this._result?.success ? 'disabled' : ''}>
                📁 导出结果
            </button>
            <button class="btn btn-secondary" onclick="vscode.postMessage({command: 'analyzeWithAI'})" ${!this._result?.success ? 'disabled' : ''}>
                🤖 AI分析
            </button>
            <button class="btn btn-primary" onclick="vscode.postMessage({command: 'runBacktest'})" ${this._isRunning ? 'disabled' : ''}>
                ${this._isRunning ? '⏳ 运行中...' : '▶️ 运行回测'}
            </button>
        </div>
    </div>
    
    <div class="main-grid">
        <div class="config-panel">
            <div class="config-title">⚙️ 回测配置</div>
            
            <div class="form-group">
                <label class="form-label">策略文件</label>
                <div class="file-select">
                    <input type="text" class="form-input" value="${this._config.strategyPath}" readonly placeholder="请选择策略文件">
                    <button onclick="vscode.postMessage({command: 'selectStrategy'})">选择</button>
                </div>
            </div>
            
            <div class="form-group">
                <label class="form-label">开始日期</label>
                <input type="date" class="form-input" value="${this._config.startDate}" 
                    onchange="updateConfig('startDate', this.value)">
            </div>
            
            <div class="form-group">
                <label class="form-label">结束日期</label>
                <input type="date" class="form-input" value="${this._config.endDate}"
                    onchange="updateConfig('endDate', this.value)">
            </div>
            
            <div class="form-group">
                <label class="form-label">数据频率</label>
                <select class="form-select" onchange="updateConfig('frequency', this.value)">
                    <option value="day" ${this._config.frequency === 'day' ? 'selected' : ''}>日线</option>
                    <option value="minute" ${this._config.frequency === 'minute' ? 'selected' : ''}>分钟线</option>
                </select>
            </div>
            
            <div class="form-group">
                <label class="form-label">初始资金</label>
                <input type="number" class="form-input" value="${this._config.initialCapital}"
                    onchange="updateConfig('initialCapital', parseFloat(this.value))">
            </div>
            
            <div class="form-group">
                <label class="form-label">基准指数</label>
                <select class="form-select" onchange="updateConfig('benchmark', this.value)">
                    <option value="000300.XSHG" ${this._config.benchmark === '000300.XSHG' ? 'selected' : ''}>沪深300</option>
                    <option value="000905.XSHG" ${this._config.benchmark === '000905.XSHG' ? 'selected' : ''}>中证500</option>
                    <option value="000001.XSHG" ${this._config.benchmark === '000001.XSHG' ? 'selected' : ''}>上证指数</option>
                </select>
            </div>
            
            <div class="form-group">
                <label class="form-label">数据源</label>
                <select class="form-select" onchange="updateConfig('dataProvider', this.value)">
                    <option value="mock" ${this._config.dataProvider === 'mock' ? 'selected' : ''}>模拟数据</option>
                    <option value="jqdata" ${this._config.dataProvider === 'jqdata' ? 'selected' : ''}>聚宽数据</option>
                    <option value="miniqmt" ${this._config.dataProvider === 'miniqmt' ? 'selected' : ''}>MiniQMT</option>
                    <option value="tushare" ${this._config.dataProvider === 'tushare' ? 'selected' : ''}>TuShare</option>
                </select>
            </div>
            
            <div class="form-group">
                <label class="form-label">佣金费率</label>
                <input type="number" class="form-input" value="${this._config.commissionRate}" step="0.0001"
                    onchange="updateConfig('commissionRate', parseFloat(this.value))">
            </div>
            
            <div class="form-group">
                <label class="form-label">滑点</label>
                <input type="number" class="form-input" value="${this._config.slippage}" step="0.001"
                    onchange="updateConfig('slippage', parseFloat(this.value))">
            </div>
        </div>
        
        <div class="result-panel">
            <div class="result-title">
                <span>📊 回测结果</span>
            </div>
            
            ${this._isRunning ? `
                <div class="running-state">
                    <div class="spinner"></div>
                    <div>回测运行中，请稍候...</div>
                </div>
            ` : this._result ? (this._result.success && metrics ? `
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">总收益率</div>
                        <div class="metric-value ${metrics.totalReturn >= 0 ? 'positive' : 'negative'}">${metrics.totalReturn.toFixed(2)}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">年化收益</div>
                        <div class="metric-value ${metrics.annualReturn >= 0 ? 'positive' : 'negative'}">${metrics.annualReturn.toFixed(2)}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">最大回撤</div>
                        <div class="metric-value negative">${metrics.maxDrawdown.toFixed(2)}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">夏普比率</div>
                        <div class="metric-value neutral">${metrics.sharpeRatio.toFixed(2)}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">胜率</div>
                        <div class="metric-value neutral">${metrics.winRate.toFixed(2)}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">交易次数</div>
                        <div class="metric-value neutral">${metrics.tradeCount}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">盈亏比</div>
                        <div class="metric-value ${metrics.profitFactor >= 1 ? 'positive' : 'negative'}">${metrics.profitFactor.toFixed(2)}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">波动率</div>
                        <div class="metric-value neutral">${metrics.volatility.toFixed(2)}%</div>
                    </div>
                </div>
                
                ${this._result.trades && this._result.trades.length > 0 ? `
                    <h3 style="margin-bottom: 12px; font-size: 14px;">📝 交易记录 (最近20笔)</h3>
                    <table class="trades-table">
                        <thead>
                            <tr>
                                <th>时间</th>
                                <th>代码</th>
                                <th>方向</th>
                                <th>价格</th>
                                <th>数量</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this._result.trades.slice(0, 20).map(t => `
                                <tr>
                                    <td>${t.date}</td>
                                    <td>${t.symbol}</td>
                                    <td class="${t.direction === 'buy' ? 'trade-buy' : 'trade-sell'}">${t.direction === 'buy' ? '买入' : '卖出'}</td>
                                    <td>¥${t.price.toFixed(2)}</td>
                                    <td>${t.volume}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                ` : ''}
            ` : `
                <div class="empty-state">
                    <div class="icon">❌</div>
                    <div>回测失败</div>
                    <div style="margin-top: 8px; font-size: 14px;">${this._result.error || '未知错误'}</div>
                </div>
            `) : `
                <div class="empty-state">
                    <div class="icon">🧪</div>
                    <div>配置回测参数后点击运行</div>
                    <div style="margin-top: 8px; font-size: 14px;">支持聚宽API兼容的策略文件</div>
                </div>
            `}
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function updateConfig(key, value) {
            vscode.postMessage({
                command: 'updateConfig',
                config: { [key]: value }
            });
        }
    </script>
</body>
</html>`;
    }

    public dispose(): void {
        BulletTradeBacktestPanel.currentPanel = undefined;
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) {
                d.dispose();
            }
        }
    }
}

export function registerBulletTradeBacktestPanel(
    context: vscode.ExtensionContext,
    client: TRQuantClient
): void {
    const disposable = vscode.commands.registerCommand('trquant.openBulletTradeBacktest', () => {
        BulletTradeBacktestPanel.createOrShow(context.extensionUri, client);
    });
    
    context.subscriptions.push(disposable);
    logger.info('BulletTrade回测面板已注册', MODULE);
}

