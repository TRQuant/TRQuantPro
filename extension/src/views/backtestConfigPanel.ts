/**
 * 回测配置面板
 * =============
 * 
 * 提供回测配置界面，支持：
 * - 回测参数配置（日期、资金、手续费等）
 * - 策略代码选择/输入
 * - 股票池配置
 * - 执行回测并显示结果
 */

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';

const MODULE = 'BacktestConfigPanel';

export class BacktestConfigPanel {
    public static currentPanel: BacktestConfigPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];
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
    ): BacktestConfigPanel {
        const column = vscode.ViewColumn.One;

        if (BacktestConfigPanel.currentPanel) {
            BacktestConfigPanel.currentPanel._panel.reveal(column);
            return BacktestConfigPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'backtestConfig',
            '🧪 回测配置',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        BacktestConfigPanel.currentPanel = new BacktestConfigPanel(panel, extensionUri, client);
        return BacktestConfigPanel.currentPanel;
    }

    private async handleMessage(message: any): Promise<void> {
        switch (message.command) {
            case 'loadStrategyFile':
                await this.loadStrategyFile();
                break;
            case 'runBacktest':
                await this.runBacktest(message.config, message.strategyCode);
                break;
            case 'saveConfig':
                await this.saveConfig(message.config);
                break;
            case 'loadConfig':
                await this.loadConfig();
                break;
        }
    }

    /**
     * 加载策略文件
     */
    private async loadStrategyFile(): Promise<void> {
        const fileUri = await vscode.window.showOpenDialog({
            canSelectFiles: true,
            canSelectFolders: false,
            canSelectMany: false,
            filters: {
                'Python文件': ['py'],
                '所有文件': ['*']
            }
        });

        if (fileUri && fileUri[0]) {
            try {
                const code = fs.readFileSync(fileUri[0].fsPath, 'utf-8');
                this._panel.webview.postMessage({
                    command: 'strategyLoaded',
                    code: code,
                    fileName: path.basename(fileUri[0].fsPath)
                });
            } catch (error) {
                vscode.window.showErrorMessage(`读取策略文件失败: ${error}`);
            }
        }
    }

    /**
     * 运行回测
     */
    private async runBacktest(config: any, strategyCode: string): Promise<void> {
        if (this._isRunning) {
            vscode.window.showWarningMessage('回测正在运行中，请稍候...');
            return;
        }

        if (!strategyCode || strategyCode.trim().length === 0) {
            vscode.window.showErrorMessage('请先加载或输入策略代码');
            return;
        }

        this._isRunning = true;
        this._panel.webview.postMessage({ command: 'backtestRunning', running: true });

        try {
            logger.info('开始运行回测', MODULE, { config });

            // 调用 Python bridge 运行回测
            const result = await this._client.runBacktest({
                strategy_code: strategyCode,
                config: config,
                data_source: config.data_source || 'akshare'
            });

            this._isRunning = false;
            this._panel.webview.postMessage({ command: 'backtestRunning', running: false });

            if (result.ok && result.data) {
                this._panel.webview.postMessage({
                    command: 'backtestResult',
                    result: result.data
                });
                vscode.window.showInformationMessage('✅ 回测完成！');
            } else {
                const errorMsg = result.error || '回测执行失败';
                this._panel.webview.postMessage({
                    command: 'backtestError',
                    error: errorMsg
                });
                vscode.window.showErrorMessage(`回测失败: ${errorMsg}`);
            }
        } catch (error) {
            this._isRunning = false;
            this._panel.webview.postMessage({ command: 'backtestRunning', running: false });
            
            const errorMsg = error instanceof Error ? error.message : String(error);
            this._panel.webview.postMessage({
                command: 'backtestError',
                error: errorMsg
            });
            logger.error(`回测执行失败: ${errorMsg}`, MODULE);
            vscode.window.showErrorMessage(`回测失败: ${errorMsg}`);
        }
    }

    /**
     * 保存配置
     */
    private async saveConfig(config: any): Promise<void> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('请先打开一个工作区');
            return;
        }

        const configPath = path.join(workspaceFolders[0].uri.fsPath, 'backtest_config.json');
        try {
            fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');
            vscode.window.showInformationMessage(`配置已保存到: ${configPath}`);
        } catch (error) {
            vscode.window.showErrorMessage(`保存配置失败: ${error}`);
        }
    }

    /**
     * 加载配置
     */
    private async loadConfig(): Promise<void> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('请先打开一个工作区');
            return;
        }

        const configPath = path.join(workspaceFolders[0].uri.fsPath, 'backtest_config.json');
        if (!fs.existsSync(configPath)) {
            vscode.window.showWarningMessage('未找到配置文件');
            return;
        }

        try {
            const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
            this._panel.webview.postMessage({
                command: 'configLoaded',
                config: config
            });
        } catch (error) {
            vscode.window.showErrorMessage(`加载配置失败: ${error}`);
        }
    }

    private updateContent(): void {
        this._panel.webview.html = this.getHtmlContent();
    }

    private getHtmlContent(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>回测配置</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: var(--vscode-editor-background);
            color: var(--vscode-editor-foreground);
            padding: 20px;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            color: var(--vscode-textLink-foreground);
            margin-bottom: 20px;
            font-size: 24px;
        }
        
        .section {
            background: var(--vscode-editor-background);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .section-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            color: var(--vscode-textLink-foreground);
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: var(--vscode-descriptionForeground);
        }
        
        input, select, textarea {
            width: 100%;
            padding: 8px 12px;
            background: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border: 1px solid var(--vscode-input-border);
            border-radius: 4px;
            font-size: 14px;
            font-family: inherit;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: var(--vscode-focusBorder);
        }
        
        textarea {
            min-height: 200px;
            font-family: 'Consolas', 'Monaco', monospace;
            resize: vertical;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
        }
        
        .btn-primary:hover {
            background: var(--vscode-button-hoverBackground);
        }
        
        .btn-secondary {
            background: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
        }
        
        .btn-secondary:hover {
            background: var(--vscode-button-secondaryHoverBackground);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .status {
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
            display: none;
        }
        
        .status.success {
            background: var(--vscode-testing-iconPassed);
            color: white;
        }
        
        .status.error {
            background: var(--vscode-testing-iconFailed);
            color: white;
        }
        
        .status.info {
            background: var(--vscode-notificationsInfoIcon-foreground);
            color: white;
        }
        
        .result-section {
            margin-top: 20px;
        }
        
        .result-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        
        .result-table th,
        .result-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        
        .result-table th {
            background: var(--vscode-editor-lineHighlightBackground);
            font-weight: 600;
        }
        
        .loading {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid var(--vscode-progressBar-background);
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-right: 8px;
            vertical-align: middle;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 回测配置</h1>
        
        <div id="status" class="status"></div>
        
        <!-- 回测参数配置 -->
        <div class="section">
            <div class="section-title">📊 回测参数</div>
            <div class="form-row">
                <div class="form-group">
                    <label>开始日期</label>
                    <input type="date" id="startDate" value="2023-01-01">
                </div>
                <div class="form-group">
                    <label>结束日期</label>
                    <input type="date" id="endDate" value="2024-01-01">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>初始资金（元）</label>
                    <input type="number" id="initialCapital" value="1000000" min="10000" step="10000">
                </div>
                <div class="form-group">
                    <label>基准指数</label>
                    <select id="benchmark">
                        <option value="000300.XSHG">沪深300 (000300.XSHG)</option>
                        <option value="000905.XSHG">中证500 (000905.XSHG)</option>
                        <option value="000001.XSHG">上证指数 (000001.XSHG)</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>手续费率</label>
                    <input type="number" id="commission" value="0.0003" min="0" max="0.01" step="0.0001">
                </div>
                <div class="form-group">
                    <label>滑点</label>
                    <input type="number" id="slippage" value="0.002" min="0" max="0.01" step="0.0001">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>最大仓位比例</label>
                    <input type="number" id="maxPosition" value="0.8" min="0" max="1" step="0.1">
                </div>
                <div class="form-group">
                    <label>单股最大仓位</label>
                    <input type="number" id="singleStockMax" value="0.1" min="0" max="1" step="0.05">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>止损线</label>
                    <input type="number" id="stopLoss" value="0.08" min="0" max="0.5" step="0.01">
                </div>
                <div class="form-group">
                    <label>止盈线</label>
                    <input type="number" id="takeProfit" value="0.2" min="0" max="1" step="0.05">
                </div>
            </div>
            <div class="form-group">
                <label>数据源</label>
                <select id="dataSource">
                    <option value="akshare">AKShare (免费)</option>
                    <option value="jqdata">JQData (需认证)</option>
                </select>
            </div>
            <div class="form-group">
                <label>股票池（代码，用逗号分隔）</label>
                <input type="text" id="symbols" placeholder="例如: 000001.XSHE,000002.XSHE" value="000001.XSHE">
            </div>
        </div>
        
        <!-- 策略代码 -->
        <div class="section">
            <div class="section-title">📝 策略代码</div>
            <div class="button-group">
                <button class="btn btn-secondary" onclick="loadStrategyFile()">📂 加载策略文件</button>
                <button class="btn btn-secondary" onclick="loadConfig()">📥 加载配置</button>
                <button class="btn btn-secondary" onclick="saveConfig()">💾 保存配置</button>
            </div>
            <div class="form-group" style="margin-top: 15px;">
                <label>策略代码（必须定义 on_bar(engine, bars) 函数）</label>
                <textarea id="strategyCode" placeholder="def on_bar(engine, bars):
    # 策略逻辑
    for symbol, bar in bars.items():
        # 示例：简单买入持有
        if engine.portfolio.get_position(symbol) == 0:
            engine.buy(symbol, 100)"></textarea>
            </div>
        </div>
        
        <!-- 操作按钮 -->
        <div class="button-group">
            <button class="btn btn-primary" id="runBtn" onclick="runBacktest()">
                ▶️ 运行回测
            </button>
        </div>
        
        <!-- 回测结果 -->
        <div class="section result-section" id="resultSection" style="display: none;">
            <div class="section-title">📈 回测结果</div>
            <div id="resultContent"></div>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function showStatus(message, type = 'info') {
            const statusEl = document.getElementById('status');
            statusEl.textContent = message;
            statusEl.className = 'status ' + type;
            statusEl.style.display = 'block';
            if (type !== 'error') {
                setTimeout(() => {
                    statusEl.style.display = 'none';
                }, 3000);
            }
        }
        
        function getConfig() {
            return {
                start_date: document.getElementById('startDate').value,
                end_date: document.getElementById('endDate').value,
                initial_capital: parseFloat(document.getElementById('initialCapital').value),
                benchmark: document.getElementById('benchmark').value,
                commission: parseFloat(document.getElementById('commission').value),
                slippage: parseFloat(document.getElementById('slippage').value),
                max_position: parseFloat(document.getElementById('maxPosition').value),
                single_stock_max: parseFloat(document.getElementById('singleStockMax').value),
                stop_loss: parseFloat(document.getElementById('stopLoss').value),
                take_profit: parseFloat(document.getElementById('takeProfit').value),
                data_source: document.getElementById('dataSource').value,
                symbols: document.getElementById('symbols').value.split(',').map(s => s.trim()).filter(s => s)
            };
        }
        
        function getStrategyCode() {
            return document.getElementById('strategyCode').value;
        }
        
        function loadStrategyFile() {
            vscode.postMessage({ command: 'loadStrategyFile' });
        }
        
        function loadConfig() {
            vscode.postMessage({ command: 'loadConfig' });
        }
        
        function saveConfig() {
            const config = getConfig();
            vscode.postMessage({ command: 'saveConfig', config: config });
        }
        
        function runBacktest() {
            const config = getConfig();
            const strategyCode = getStrategyCode();
            
            if (!strategyCode || strategyCode.trim().length === 0) {
                showStatus('请先输入策略代码', 'error');
                return;
            }
            
            vscode.postMessage({
                command: 'runBacktest',
                config: config,
                strategyCode: strategyCode
            });
        }
        
        // 监听来自扩展的消息
        window.addEventListener('message', event => {
            const message = event.data;
            
            switch (message.command) {
                case 'strategyLoaded':
                    document.getElementById('strategyCode').value = message.code;
                    showStatus('策略文件加载成功: ' + message.fileName, 'success');
                    break;
                    
                case 'configLoaded':
                    const config = message.config;
                    if (config.start_date) document.getElementById('startDate').value = config.start_date;
                    if (config.end_date) document.getElementById('endDate').value = config.end_date;
                    if (config.initial_capital) document.getElementById('initialCapital').value = config.initial_capital;
                    if (config.benchmark) document.getElementById('benchmark').value = config.benchmark;
                    if (config.commission) document.getElementById('commission').value = config.commission;
                    if (config.slippage) document.getElementById('slippage').value = config.slippage;
                    if (config.max_position) document.getElementById('maxPosition').value = config.max_position;
                    if (config.single_stock_max) document.getElementById('singleStockMax').value = config.single_stock_max;
                    if (config.stop_loss) document.getElementById('stopLoss').value = config.stop_loss;
                    if (config.take_profit) document.getElementById('takeProfit').value = config.take_profit;
                    if (config.data_source) document.getElementById('dataSource').value = config.data_source;
                    if (config.symbols) document.getElementById('symbols').value = config.symbols.join(',');
                    showStatus('配置加载成功', 'success');
                    break;
                    
                case 'backtestRunning':
                    const runBtn = document.getElementById('runBtn');
                    if (message.running) {
                        runBtn.disabled = true;
                        runBtn.innerHTML = '<span class="loading"></span> 回测运行中...';
                    } else {
                        runBtn.disabled = false;
                        runBtn.innerHTML = '▶️ 运行回测';
                    }
                    break;
                    
                case 'backtestResult':
                    displayResult(message.result);
                    showStatus('回测完成！', 'success');
                    break;
                    
                case 'backtestError':
                    showStatus('回测失败: ' + message.error, 'error');
                    document.getElementById('resultSection').style.display = 'none';
                    break;
            }
        });
        
        function displayResult(result) {
            const resultSection = document.getElementById('resultSection');
            const resultContent = document.getElementById('resultContent');
            
            if (!result || !result.success) {
                resultContent.innerHTML = '<p style="color: var(--vscode-errorForeground);">回测执行失败</p>';
                resultSection.style.display = 'block';
                return;
            }
            
            const data = result.result || result;
            let html = '<table class="result-table">';
            
            // 基本指标
            if (data.total_return !== undefined) {
                html += '<tr><th>总收益率</th><td>' + (data.total_return * 100).toFixed(2) + '%</td></tr>';
            }
            if (data.annual_return !== undefined) {
                html += '<tr><th>年化收益率</th><td>' + (data.annual_return * 100).toFixed(2) + '%</td></tr>';
            }
            if (data.sharpe_ratio !== undefined) {
                html += '<tr><th>夏普比率</th><td>' + data.sharpe_ratio.toFixed(3) + '</td></tr>';
            }
            if (data.max_drawdown !== undefined) {
                html += '<tr><th>最大回撤</th><td>' + (data.max_drawdown * 100).toFixed(2) + '%</td></tr>';
            }
            if (data.win_rate !== undefined) {
                html += '<tr><th>胜率</th><td>' + (data.win_rate * 100).toFixed(2) + '%</td></tr>';
            }
            if (data.total_trades !== undefined) {
                html += '<tr><th>总交易次数</th><td>' + data.total_trades + '</td></tr>';
            }
            if (data.final_value !== undefined) {
                html += '<tr><th>最终资产</th><td>' + data.final_value.toFixed(2) + ' 元</td></tr>';
            }
            
            html += '</table>';
            resultContent.innerHTML = html;
            resultSection.style.display = 'block';
        }
    </script>
</body>
</html>`;
    }

    public dispose(): void {
        BacktestConfigPanel.currentPanel = undefined;
        this._disposables.forEach(d => d.dispose());
    }
}

/**
 * 导出函数：显示回测配置面板
 */
export function showBacktestConfigPanel(
    extensionUri: vscode.Uri,
    client: TRQuantClient,
    context: vscode.ExtensionContext
): void {
    BacktestConfigPanel.createOrShow(extensionUri, client);
}





