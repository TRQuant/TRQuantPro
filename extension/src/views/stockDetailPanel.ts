/**
 * Stock Detail Panel - 个股详情面板
 * 
 * 展示股票的7维评分、阶段时间线、事件列表
 * 
 * @author TRQuant Team
 * @date 2025-12-18
 */

import * as vscode from 'vscode';
import { PythonBridge } from '../pythonBridge';

export class StockDetailPanel {
    public static currentPanel: StockDetailPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _currentSymbol: string = '';
    private _disposables: vscode.Disposable[] = [];

    private constructor(panel: vscode.WebviewPanel, symbol: string) {
        this._panel = panel;
        this._currentSymbol = symbol;
        this._panel.webview.html = this._getWebviewContent();

        this._panel.webview.onDidReceiveMessage(
            async (message) => {
                switch (message.command) {
                    case 'refresh':
                        await this._loadStockData();
                        break;
                    case 'evaluate':
                        await this._evaluateStock();
                        break;
                    case 'addToPool':
                        await this._addToPool(message.level);
                        break;
                }
            },
            null,
            this._disposables
        );

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        
        // 初始加载
        this._loadStockData();
    }

    public static createOrShow(extensionUri: vscode.Uri, symbol: string) {
        const column = vscode.ViewColumn.Two;

        if (StockDetailPanel.currentPanel) {
            StockDetailPanel.currentPanel._currentSymbol = symbol;
            StockDetailPanel.currentPanel._panel.reveal(column);
            StockDetailPanel.currentPanel._loadStockData();
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'stockDetailPanel',
            `📈 ${symbol}`,
            column,
            { enableScripts: true, retainContextWhenHidden: true }
        );

        StockDetailPanel.currentPanel = new StockDetailPanel(panel, symbol);
    }

    private async _loadStockData() {
        try {
            this._panel.webview.postMessage({ command: 'loading', loading: true });
            this._panel.title = `📈 ${this._currentSymbol}`;
            
            const bridge = PythonBridge.getInstance();
            
            const [basicInfo, evaluation, events, stage] = await Promise.all([
                bridge.executeCommand('stock_basic_info', { symbol: this._currentSymbol }),
                bridge.executeCommand('tenbagger_evaluate', { symbol: this._currentSymbol }),
                bridge.executeCommand('stock_events', { symbol: this._currentSymbol }),
                bridge.executeCommand('stock_stage', { symbol: this._currentSymbol })
            ]);
            
            this._panel.webview.postMessage({
                command: 'updateData',
                data: {
                    symbol: this._currentSymbol,
                    basicInfo: basicInfo || {},
                    evaluation: evaluation || {},
                    events: events || [],
                    stage: stage || { current: 'S0' }
                }
            });
        } catch (error) {
            vscode.window.showErrorMessage(`加载股票数据失败: ${error}`);
        } finally {
            this._panel.webview.postMessage({ command: 'loading', loading: false });
        }
    }

    private async _evaluateStock() {
        try {
            const bridge = PythonBridge.getInstance();
            const result = await bridge.executeCommand('tenbagger_evaluate', { symbol: this._currentSymbol });
            
            this._panel.webview.postMessage({
                command: 'evaluationResult',
                data: result
            });
        } catch (error) {
            vscode.window.showErrorMessage(`评估失败: ${error}`);
        }
    }

    private async _addToPool(level: string) {
        try {
            const bridge = PythonBridge.getInstance();
            await bridge.executeCommand('candidate_pool_add', { 
                symbol: this._currentSymbol, 
                level 
            });
            vscode.window.showInformationMessage(`${this._currentSymbol} 已添加到 ${level} 候选池`);
        } catch (error) {
            vscode.window.showErrorMessage(`添加失败: ${error}`);
        }
    }

    private _getWebviewContent(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>个股详情</title>
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --accent: #58a6ff;
            --green: #3fb950;
            --orange: #d29922;
            --red: #f85149;
            --purple: #a371f7;
            --border: #30363d;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 24px;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }
        
        .stock-info h1 {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        
        .stock-info .symbol {
            font-family: 'SF Mono', monospace;
            color: var(--accent);
            font-size: 16px;
        }
        
        .header-actions {
            display: flex;
            gap: 12px;
        }
        
        .btn {
            padding: 10px 18px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s;
        }
        
        .btn-primary { background: var(--accent); color: white; }
        .btn-primary:hover { filter: brightness(1.1); }
        .btn-secondary { background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border); }
        
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .card {
            background: var(--bg-secondary);
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow: hidden;
        }
        
        .card-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            font-weight: 600;
            font-size: 16px;
        }
        
        .card-body {
            padding: 20px;
        }
        
        /* 7维评分卡雷达图占位 */
        .radar-chart {
            width: 100%;
            height: 280px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }
        
        .radar-placeholder {
            width: 240px;
            height: 240px;
            border-radius: 50%;
            background: conic-gradient(
                from 0deg,
                rgba(88, 166, 255, 0.1) 0deg,
                rgba(163, 113, 247, 0.1) 51deg,
                rgba(63, 185, 80, 0.1) 102deg,
                rgba(210, 153, 34, 0.1) 153deg,
                rgba(248, 81, 73, 0.1) 204deg,
                rgba(88, 166, 255, 0.2) 255deg,
                rgba(88, 166, 255, 0.1) 306deg,
                rgba(88, 166, 255, 0.1) 360deg
            );
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .radar-center {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: var(--bg-card);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .radar-score {
            font-size: 28px;
            font-weight: 700;
            color: var(--accent);
        }
        
        .radar-grade {
            font-size: 14px;
            color: var(--text-secondary);
        }
        
        .dimension-list {
            margin-top: 16px;
        }
        
        .dimension-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid var(--border);
        }
        
        .dimension-item:last-child {
            border-bottom: none;
        }
        
        .dimension-name {
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        .dimension-score {
            font-weight: 600;
            font-size: 14px;
        }
        
        .dimension-bar {
            width: 100px;
            height: 6px;
            background: var(--bg-card);
            border-radius: 3px;
            overflow: hidden;
            margin-left: 12px;
        }
        
        .dimension-fill {
            height: 100%;
            border-radius: 3px;
            transition: width 0.3s;
        }
        
        /* 阶段时间线 */
        .stage-timeline {
            display: flex;
            justify-content: space-between;
            position: relative;
            margin: 20px 0;
        }
        
        .stage-timeline::before {
            content: '';
            position: absolute;
            top: 20px;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--border);
            border-radius: 2px;
        }
        
        .stage-node {
            position: relative;
            z-index: 1;
            text-align: center;
            width: 60px;
        }
        
        .stage-dot {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--bg-card);
            border: 3px solid var(--border);
            margin: 0 auto 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: 700;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .stage-node.active .stage-dot {
            border-color: var(--accent);
            background: var(--accent);
            color: white;
            box-shadow: 0 0 20px rgba(88, 166, 255, 0.4);
        }
        
        .stage-node.passed .stage-dot {
            border-color: var(--green);
            background: var(--green);
            color: white;
        }
        
        .stage-label {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        /* 事件列表 */
        .event-list {
            max-height: 300px;
            overflow-y: auto;
        }
        
        .event-item {
            padding: 12px 16px;
            border-radius: 8px;
            background: var(--bg-card);
            margin-bottom: 8px;
            display: flex;
            gap: 12px;
        }
        
        .event-icon {
            font-size: 20px;
        }
        
        .event-content {
            flex: 1;
        }
        
        .event-title {
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .event-date {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .event-tag {
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }
        
        .tag-positive { background: rgba(63, 185, 80, 0.2); color: var(--green); }
        .tag-neutral { background: rgba(139, 148, 158, 0.2); color: var(--text-secondary); }
        .tag-negative { background: rgba(248, 81, 73, 0.2); color: var(--red); }
        
        .loading-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .spinner {
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
        
        .full-width { grid-column: 1 / -1; }
    </style>
</head>
<body>
    <div class="loading-overlay hidden" id="loadingOverlay">
        <div class="spinner"></div>
    </div>
    
    <header class="header">
        <div class="stock-info">
            <h1 id="stockName">加载中...</h1>
            <div class="symbol" id="stockSymbol">--</div>
        </div>
        <div class="header-actions">
            <button class="btn btn-secondary" onclick="addToPool('L2')">📥 加入精选池</button>
            <button class="btn btn-primary" onclick="evaluate()">🎯 重新评估</button>
        </div>
    </header>
    
    <div class="grid">
        <div class="card">
            <div class="card-header">📊 7维评分卡</div>
            <div class="card-body">
                <div class="radar-chart">
                    <div class="radar-placeholder">
                        <div class="radar-center">
                            <div class="radar-score" id="totalScore">--</div>
                            <div class="radar-grade" id="scoreGrade">--</div>
                        </div>
                    </div>
                </div>
                <div class="dimension-list" id="dimensionList">
                    <!-- 动态渲染 -->
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">📈 阶段判断</div>
            <div class="card-body">
                <div class="stage-timeline" id="stageTimeline">
                    <div class="stage-node passed">
                        <div class="stage-dot">S0</div>
                        <div class="stage-label">观察</div>
                    </div>
                    <div class="stage-node active">
                        <div class="stage-dot">S1</div>
                        <div class="stage-label">验证</div>
                    </div>
                    <div class="stage-node">
                        <div class="stage-dot">S2</div>
                        <div class="stage-label">导入</div>
                    </div>
                    <div class="stage-node">
                        <div class="stage-dot">S3</div>
                        <div class="stage-label">放量</div>
                    </div>
                    <div class="stage-node">
                        <div class="stage-dot">S4</div>
                        <div class="stage-label">加速</div>
                    </div>
                    <div class="stage-node">
                        <div class="stage-dot">S5</div>
                        <div class="stage-label">成熟</div>
                    </div>
                </div>
                
                <div style="margin-top: 24px; padding: 16px; background: var(--bg-card); border-radius: 8px;">
                    <div style="font-weight: 600; margin-bottom: 8px;">当前阶段说明</div>
                    <div id="stageDesc" style="color: var(--text-secondary); font-size: 14px;">
                        S1 验证期 - 送样/认证中，尚未确认客户
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card full-width">
            <div class="card-header">📋 事件时间线</div>
            <div class="card-body">
                <div class="event-list" id="eventList">
                    <div class="event-item">
                        <div class="event-icon">📄</div>
                        <div class="event-content">
                            <div class="event-title">关于签订重大合同的公告</div>
                            <div class="event-date">2025-12-15</div>
                        </div>
                        <span class="event-tag tag-positive">利好</span>
                    </div>
                    <div class="event-item">
                        <div class="event-icon">🏭</div>
                        <div class="event-content">
                            <div class="event-title">产能扩张项目开工</div>
                            <div class="event-date">2025-12-10</div>
                        </div>
                        <span class="event-tag tag-positive">利好</span>
                    </div>
                    <div class="event-item">
                        <div class="event-icon">📊</div>
                        <div class="event-content">
                            <div class="event-title">三季度业绩预增公告</div>
                            <div class="event-date">2025-12-01</div>
                        </div>
                        <span class="event-tag tag-positive">利好</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        let stockData = null;
        
        function refresh() {
            vscode.postMessage({ command: 'refresh' });
        }
        
        function evaluate() {
            vscode.postMessage({ command: 'evaluate' });
        }
        
        function addToPool(level) {
            vscode.postMessage({ command: 'addToPool', level });
        }
        
        function updateUI(data) {
            stockData = data;
            
            document.getElementById('stockSymbol').textContent = data.symbol || '--';
            document.getElementById('stockName').textContent = data.basicInfo?.name || data.symbol || '加载中...';
            
            // 更新评分
            const eval_data = data.evaluation || {};
            document.getElementById('totalScore').textContent = (eval_data.total_score || 0).toFixed(0);
            document.getElementById('scoreGrade').textContent = eval_data.eval_level || '--';
            
            // 更新维度列表
            const dimensions = [
                { name: '产业位置', score: 65 },
                { name: '兑现路径', score: 72 },
                { name: '财务拐点', score: 58 },
                { name: '组织信号', score: 80 },
                { name: '估值错配', score: 55 },
                { name: '研究关注', score: 48 },
                { name: '证据密度', score: 70 }
            ];
            
            document.getElementById('dimensionList').innerHTML = dimensions.map(d => {
                const color = d.score >= 70 ? 'var(--green)' : d.score >= 50 ? 'var(--orange)' : 'var(--red)';
                return \`
                    <div class="dimension-item">
                        <span class="dimension-name">\${d.name}</span>
                        <div style="display: flex; align-items: center;">
                            <span class="dimension-score" style="color: \${color}">\${d.score}</span>
                            <div class="dimension-bar">
                                <div class="dimension-fill" style="width: \${d.score}%; background: \${color};"></div>
                            </div>
                        </div>
                    </div>
                \`;
            }).join('');
            
            // 更新阶段
            updateStageTimeline(data.stage?.current || 'S0');
        }
        
        function updateStageTimeline(currentStage) {
            const stageIndex = parseInt(currentStage.replace('S', '')) || 0;
            const nodes = document.querySelectorAll('.stage-node');
            
            nodes.forEach((node, i) => {
                node.classList.remove('active', 'passed');
                if (i < stageIndex) {
                    node.classList.add('passed');
                } else if (i === stageIndex) {
                    node.classList.add('active');
                }
            });
            
            const stageDescs = {
                'S0': 'S0 观察期 - 有产业链位置，无明显兑现信号',
                'S1': 'S1 验证期 - 送样/认证中，尚未确认客户',
                'S2': 'S2 导入期 - 已进入客户体系，小批量/验证',
                'S3': 'S3 放量期 - 批量订单，扩产明确',
                'S4': 'S4 加速期 - 业绩拐点，估值修复',
                'S5': 'S5 成熟期 - 主流共识，十倍股特征消失'
            };
            document.getElementById('stageDesc').textContent = stageDescs[currentStage] || stageDescs['S0'];
        }
        
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'loading':
                    document.getElementById('loadingOverlay').classList.toggle('hidden', !message.loading);
                    break;
                case 'updateData':
                    updateUI(message.data);
                    break;
                case 'evaluationResult':
                    if (message.data) {
                        document.getElementById('totalScore').textContent = (message.data.total_score || 0).toFixed(0);
                        document.getElementById('scoreGrade').textContent = message.data.eval_level || '--';
                    }
                    break;
            }
        });
    </script>
</body>
</html>`;
    }

    public dispose() {
        StockDetailPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }
}
