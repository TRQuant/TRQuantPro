/**
 * BulletTrade 实盘交易面板
 * =========================
 * 
 * 实盘交易监控、持仓管理和风控
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';

const MODULE = 'BulletTradeLivePanel';

interface Position {
    symbol: string;
    name: string;
    volume: number;
    cost: number;
    price: number;
    pnl: number;
    pnlRatio: number;
}

interface Trade {
    time: string;
    symbol: string;
    name: string;
    direction: string;
    price: number;
    volume: number;
    amount: number;
    status: string;
}

interface AccountInfo {
    totalValue: number;
    cash: number;
    positionsValue: number;
    dailyPnl: number;
    dailyReturn: number;
}

interface LiveConfig {
    strategyPath: string;
    broker: string;
    riskControl: {
        maxDrawdown: number;
        maxDailyLoss: number;
        maxPositionRatio: number;
        stopLoss: number;
        takeProfit: number;
    };
}

export class BulletTradeLivePanel {
    public static currentPanel: BulletTradeLivePanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];
    
    private _isRunning: boolean = false;
    private _accountInfo: AccountInfo = {
        totalValue: 0,
        cash: 0,
        positionsValue: 0,
        dailyPnl: 0,
        dailyReturn: 0
    };
    private _positions: Position[] = [];
    private _trades: Trade[] = [];
    private _config: LiveConfig = {
        strategyPath: '',
        broker: 'mock',
        riskControl: {
            maxDrawdown: 0.2,
            maxDailyLoss: 0.05,
            maxPositionRatio: 0.3,
            stopLoss: 0.08,
            takeProfit: 0.2
        }
    };

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
    ): BulletTradeLivePanel {
        const column = vscode.ViewColumn.One;

        if (BulletTradeLivePanel.currentPanel) {
            BulletTradeLivePanel.currentPanel._panel.reveal(column);
            return BulletTradeLivePanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'bullettradeLive',
            '📈 BulletTrade 实盘',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        BulletTradeLivePanel.currentPanel = new BulletTradeLivePanel(panel, extensionUri, client);
        return BulletTradeLivePanel.currentPanel;
    }

    private async handleMessage(message: { command: string; [key: string]: unknown }): Promise<void> {
        logger.debug(`收到消息: ${message.command}`, MODULE);
        
        switch (message.command) {
            case 'selectStrategy':
                await this.selectStrategy();
                break;
            case 'updateConfig':
                this.updateConfig(message.config as Partial<LiveConfig>);
                break;
            case 'startTrading':
                await this.startTrading();
                break;
            case 'stopTrading':
                await this.stopTrading();
                break;
            case 'refreshData':
                await this.refreshData();
                break;
            case 'generateDailyReport':
                await this.generateDailyReport();
                break;
            default:
                logger.warn(`未知命令: ${message.command}`, MODULE);
        }
    }

    private async selectStrategy(): Promise<void> {
        const options: vscode.OpenDialogOptions = {
            canSelectMany: false,
            filters: { 'Python Strategy': ['py'] },
            title: '选择策略文件'
        };

        const fileUri = await vscode.window.showOpenDialog(options);
        if (fileUri && fileUri[0]) {
            this._config.strategyPath = fileUri[0].fsPath;
            this.updateContent();
        }
    }

    private updateConfig(config: Partial<LiveConfig>): void {
        this._config = { ...this._config, ...config };
        this.updateContent();
    }

    private async startTrading(): Promise<void> {
        if (this._isRunning) {
            vscode.window.showWarningMessage('实盘已在运行中');
            return;
        }

        if (!this._config.strategyPath) {
            vscode.window.showErrorMessage('请先选择策略文件');
            return;
        }

        const confirm = await vscode.window.showWarningMessage(
            '⚠️ 确定要启动实盘交易吗？这将执行真实交易。',
            '确定启动',
            '取消'
        );

        if (confirm !== '确定启动') {
            return;
        }

        try {
            const response = await this._client.callBridge<{ success: boolean }>('start_bt_live_trading', {
                strategy_path: this._config.strategyPath,
                broker: this._config.broker,
                risk_control: this._config.riskControl
            });

            if (response.ok) {
                this._isRunning = true;
                vscode.window.showInformationMessage('✅ 实盘交易已启动');
                this.startDataRefresh();
            } else {
                vscode.window.showErrorMessage(`启动失败: ${response.error}`);
            }
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            vscode.window.showErrorMessage(`启动失败: ${errorMsg}`);
        }
        
        this.updateContent();
    }

    private async stopTrading(): Promise<void> {
        if (!this._isRunning) {
            return;
        }

        const confirm = await vscode.window.showWarningMessage(
            '确定要停止实盘交易吗？',
            '确定停止',
            '取消'
        );

        if (confirm !== '确定停止') {
            return;
        }

        try {
            await this._client.callBridge('stop_bt_live_trading', {});
            this._isRunning = false;
            vscode.window.showInformationMessage('实盘交易已停止');
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            vscode.window.showErrorMessage(`停止失败: ${errorMsg}`);
        }
        
        this.updateContent();
    }

    private startDataRefresh(): void {
        // 定期刷新数据（每30秒）
        const interval = setInterval(async () => {
            if (!this._isRunning) {
                clearInterval(interval);
                return;
            }
            await this.refreshData();
        }, 30000);
    }

    private async refreshData(): Promise<void> {
        try {
            const response = await this._client.callBridge<{ account: AccountInfo; positions: Position[]; trades: Trade[] }>('get_bt_live_status', {});
            
            if (response.ok && response.data) {
                this._accountInfo = response.data.account || this._accountInfo;
                this._positions = response.data.positions || [];
                this._trades = response.data.trades || [];
                this.updateContent();
            }
        } catch (error) {
            logger.error(`刷新数据失败: ${error}`, MODULE);
        }
    }

    private async generateDailyReport(): Promise<void> {
        vscode.window.showInformationMessage('📊 正在生成日报...');
        
        try {
            const response = await this._client.callBridge<{ report: string }>('generate_bt_live_daily_report', {
                account: this._accountInfo,
                positions: this._positions,
                trades: this._trades
            });

            if (response.ok && response.data) {
                const doc = await vscode.workspace.openTextDocument({
                    content: response.data.report || String(response.data),
                    language: 'markdown'
                });
                await vscode.window.showTextDocument(doc);
            }
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            vscode.window.showErrorMessage(`生成日报失败: ${errorMsg}`);
        }
    }

    private updateContent(): void {
        this._panel.webview.html = this.generateHtml();
    }

    private generateHtml(): string {
        const account = this._accountInfo;
        
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BulletTrade 实盘</title>
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
        
        .status-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .status-running {
            background: rgba(63, 185, 80, 0.2);
            color: var(--accent-green);
        }
        
        .status-stopped {
            background: rgba(139, 148, 158, 0.2);
            color: var(--text-secondary);
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
        
        .btn-start {
            background: linear-gradient(135deg, #3fb950 0%, #238636 100%);
            color: #fff;
            font-weight: 600;
        }
        
        .btn-stop {
            background: linear-gradient(135deg, #f85149 0%, #da3633 100%);
            color: #fff;
            font-weight: 600;
        }
        
        .btn-secondary {
            background: var(--bg-secondary);
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
        }
        
        .btn:hover:not(:disabled) {
            transform: translateY(-1px);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .account-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .account-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        
        .account-label {
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }
        
        .account-value {
            font-size: 24px;
            font-weight: 700;
        }
        
        .positive { color: var(--accent-green); }
        .negative { color: var(--accent-red); }
        .neutral { color: var(--accent-blue); }
        
        .main-grid {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 24px;
        }
        
        .config-panel {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
        }
        
        .panel-title {
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
        
        .form-input, .form-select {
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
        
        .content-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .section {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .data-table th,
        .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        .data-table th {
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 600;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
        }
        
        .risk-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
        }
        
        .risk-ok { background: rgba(63, 185, 80, 0.2); color: var(--accent-green); }
        .risk-warn { background: rgba(240, 180, 41, 0.2); color: var(--accent-gold); }
        .risk-danger { background: rgba(248, 81, 73, 0.2); color: var(--accent-red); }
    </style>
</head>
<body>
    <div class="header">
        <h1>
            📈 BulletTrade 实盘
            <span class="status-badge ${this._isRunning ? 'status-running' : 'status-stopped'}">
                ${this._isRunning ? '● 运行中' : '○ 已停止'}
            </span>
        </h1>
        <div class="header-actions">
            <button class="btn btn-secondary" onclick="vscode.postMessage({command: 'refreshData'})">
                🔄 刷新
            </button>
            <button class="btn btn-secondary" onclick="vscode.postMessage({command: 'generateDailyReport'})">
                📊 日报
            </button>
            ${this._isRunning ? `
                <button class="btn btn-stop" onclick="vscode.postMessage({command: 'stopTrading'})">
                    ⏹️ 停止交易
                </button>
            ` : `
                <button class="btn btn-start" onclick="vscode.postMessage({command: 'startTrading'})" ${!this._config.strategyPath ? 'disabled' : ''}>
                    ▶️ 启动交易
                </button>
            `}
        </div>
    </div>
    
    <!-- 账户概况 -->
    <div class="account-grid">
        <div class="account-card">
            <div class="account-label">账户净值</div>
            <div class="account-value neutral">¥${account.totalValue.toLocaleString()}</div>
        </div>
        <div class="account-card">
            <div class="account-label">可用资金</div>
            <div class="account-value">¥${account.cash.toLocaleString()}</div>
        </div>
        <div class="account-card">
            <div class="account-label">持仓市值</div>
            <div class="account-value">¥${account.positionsValue.toLocaleString()}</div>
        </div>
        <div class="account-card">
            <div class="account-label">今日盈亏</div>
            <div class="account-value ${account.dailyPnl >= 0 ? 'positive' : 'negative'}">
                ${account.dailyPnl >= 0 ? '+' : ''}¥${account.dailyPnl.toLocaleString()}
            </div>
        </div>
        <div class="account-card">
            <div class="account-label">今日收益率</div>
            <div class="account-value ${account.dailyReturn >= 0 ? 'positive' : 'negative'}">
                ${account.dailyReturn >= 0 ? '+' : ''}${account.dailyReturn.toFixed(2)}%
            </div>
        </div>
    </div>
    
    <div class="main-grid">
        <!-- 配置面板 -->
        <div class="config-panel">
            <div class="panel-title">⚙️ 交易配置</div>
            
            <div class="form-group">
                <label class="form-label">策略文件</label>
                <button class="btn btn-secondary" style="width: 100%;" onclick="vscode.postMessage({command: 'selectStrategy'})">
                    ${this._config.strategyPath ? '已选择' : '选择策略'}
                </button>
                ${this._config.strategyPath ? `<div style="font-size: 11px; color: var(--text-muted); margin-top: 4px; word-break: break-all;">${this._config.strategyPath}</div>` : ''}
            </div>
            
            <div class="form-group">
                <label class="form-label">券商接口</label>
                <select class="form-select" onchange="updateConfig('broker', this.value)" ${this._isRunning ? 'disabled' : ''}>
                    <option value="mock" ${this._config.broker === 'mock' ? 'selected' : ''}>模拟交易</option>
                    <option value="qmt" ${this._config.broker === 'qmt' ? 'selected' : ''}>QMT</option>
                    <option value="ptrade" ${this._config.broker === 'ptrade' ? 'selected' : ''}>恒生PTrade</option>
                </select>
            </div>
            
            <div class="panel-title" style="margin-top: 24px;">🛡️ 风控设置</div>
            
            <div class="form-group">
                <label class="form-label">最大回撤</label>
                <input type="number" class="form-input" value="${this._config.riskControl.maxDrawdown * 100}" step="1"
                    onchange="updateRiskControl('maxDrawdown', parseFloat(this.value) / 100)" ${this._isRunning ? 'disabled' : ''}>
            </div>
            
            <div class="form-group">
                <label class="form-label">单日最大亏损</label>
                <input type="number" class="form-input" value="${this._config.riskControl.maxDailyLoss * 100}" step="0.5"
                    onchange="updateRiskControl('maxDailyLoss', parseFloat(this.value) / 100)" ${this._isRunning ? 'disabled' : ''}>
            </div>
            
            <div class="form-group">
                <label class="form-label">单票止损</label>
                <input type="number" class="form-input" value="${this._config.riskControl.stopLoss * 100}" step="1"
                    onchange="updateRiskControl('stopLoss', parseFloat(this.value) / 100)" ${this._isRunning ? 'disabled' : ''}>
            </div>
            
            <div class="form-group">
                <label class="form-label">单票止盈</label>
                <input type="number" class="form-input" value="${this._config.riskControl.takeProfit * 100}" step="1"
                    onchange="updateRiskControl('takeProfit', parseFloat(this.value) / 100)" ${this._isRunning ? 'disabled' : ''}>
            </div>
        </div>
        
        <!-- 内容面板 -->
        <div class="content-panel">
            <!-- 持仓 -->
            <div class="section">
                <div class="panel-title">📦 当前持仓</div>
                ${this._positions.length > 0 ? `
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>代码</th>
                                <th>名称</th>
                                <th>数量</th>
                                <th>成本</th>
                                <th>现价</th>
                                <th>盈亏</th>
                                <th>收益率</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this._positions.map(p => `
                                <tr>
                                    <td>${p.symbol}</td>
                                    <td>${p.name}</td>
                                    <td>${p.volume}</td>
                                    <td>¥${p.cost.toFixed(2)}</td>
                                    <td>¥${p.price.toFixed(2)}</td>
                                    <td class="${p.pnl >= 0 ? 'positive' : 'negative'}">${p.pnl >= 0 ? '+' : ''}¥${p.pnl.toFixed(2)}</td>
                                    <td class="${p.pnlRatio >= 0 ? 'positive' : 'negative'}">${p.pnlRatio >= 0 ? '+' : ''}${(p.pnlRatio * 100).toFixed(2)}%</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                ` : '<div class="empty-state">当前无持仓</div>'}
            </div>
            
            <!-- 今日交易 -->
            <div class="section">
                <div class="panel-title">📝 今日交易</div>
                ${this._trades.length > 0 ? `
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>时间</th>
                                <th>代码</th>
                                <th>方向</th>
                                <th>价格</th>
                                <th>数量</th>
                                <th>金额</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this._trades.map(t => `
                                <tr>
                                    <td>${t.time}</td>
                                    <td>${t.symbol}</td>
                                    <td class="${t.direction === 'buy' ? 'negative' : 'positive'}">${t.direction === 'buy' ? '买入' : '卖出'}</td>
                                    <td>¥${t.price.toFixed(2)}</td>
                                    <td>${t.volume}</td>
                                    <td>¥${t.amount.toLocaleString()}</td>
                                    <td><span class="risk-badge ${t.status === 'filled' ? 'risk-ok' : 'risk-warn'}">${t.status === 'filled' ? '已成交' : t.status}</span></td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                ` : '<div class="empty-state">今日无交易</div>'}
            </div>
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
        
        function updateRiskControl(key, value) {
            vscode.postMessage({
                command: 'updateConfig',
                config: { 
                    riskControl: { 
                        ...${JSON.stringify(this._config.riskControl)},
                        [key]: value 
                    } 
                }
            });
        }
    </script>
</body>
</html>`;
    }

    public dispose(): void {
        BulletTradeLivePanel.currentPanel = undefined;
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) {
                d.dispose();
            }
        }
    }
}

export function registerBulletTradeLivePanel(
    context: vscode.ExtensionContext,
    client: TRQuantClient
): void {
    const disposable = vscode.commands.registerCommand('trquant.openBulletTradeLive', () => {
        BulletTradeLivePanel.createOrShow(context.extensionUri, client);
    });
    
    context.subscriptions.push(disposable);
    logger.info('BulletTrade实盘面板已注册', MODULE);
}

