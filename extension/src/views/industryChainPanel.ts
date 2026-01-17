/**
 * Industry Chain Panel - 产业链图谱面板
 * 
 * 展示产业链关系、上下游映射、关联股票
 * 
 * @author TRQuant Team
 * @date 2025-12-18
 */

import * as vscode from 'vscode';
import { PythonBridge } from '../pythonBridge';

export class IndustryChainPanel {
    public static currentPanel: IndustryChainPanel | undefined;
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
                        await this._loadChainData();
                        break;
                    case 'selectChain':
                        await this._selectChain(message.chainId);
                        break;
                    case 'selectNode':
                        await this._selectNode(message.nodeId);
                        break;
                    case 'search':
                        await this._searchChain(message.query);
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

        if (IndustryChainPanel.currentPanel) {
            IndustryChainPanel.currentPanel._panel.reveal(column);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'industryChainPanel',
            '🔗 产业链图谱',
            column || vscode.ViewColumn.One,
            { enableScripts: true, retainContextWhenHidden: true }
        );

        IndustryChainPanel.currentPanel = new IndustryChainPanel(panel, extensionUri);
    }

    private async _loadChainData() {
        try {
            this._panel.webview.postMessage({ command: 'loading', loading: true });
            const bridge = PythonBridge.getInstance();
            
            const chains = await bridge.executeCommand('industry_chain_list', {});
            const stats = await bridge.executeCommand('industry_chain_stats', {});
            
            this._panel.webview.postMessage({
                command: 'updateData',
                data: { chains: chains || [], stats: stats || {} }
            });
        } catch (error) {
            vscode.window.showErrorMessage(`加载产业链数据失败: ${error}`);
        } finally {
            this._panel.webview.postMessage({ command: 'loading', loading: false });
        }
    }

    private async _selectChain(chainId: string) {
        try {
            const bridge = PythonBridge.getInstance();
            const detail = await bridge.executeCommand('industry_chain_detail', { chain_id: chainId });
            
            this._panel.webview.postMessage({
                command: 'chainDetail',
                data: detail
            });
        } catch (error) {
            vscode.window.showErrorMessage(`获取产业链详情失败: ${error}`);
        }
    }

    private async _selectNode(nodeId: string) {
        try {
            const bridge = PythonBridge.getInstance();
            const stocks = await bridge.executeCommand('industry_chain_stocks', { node_id: nodeId });
            
            this._panel.webview.postMessage({
                command: 'nodeStocks',
                data: stocks
            });
        } catch (error) {
            vscode.window.showErrorMessage(`获取节点股票失败: ${error}`);
        }
    }

    private async _searchChain(query: string) {
        try {
            const bridge = PythonBridge.getInstance();
            const results = await bridge.executeCommand('industry_chain_search', { query });
            
            this._panel.webview.postMessage({
                command: 'searchResults',
                data: results
            });
        } catch (error) {
            vscode.window.showErrorMessage(`搜索失败: ${error}`);
        }
    }

    private _getWebviewContent(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>产业链图谱</title>
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --accent: #06b6d4;
            --accent-hover: #0891b2;
            --purple: #a855f7;
            --green: #22c55e;
            --orange: #f97316;
            --border: #475569;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }
        
        .container {
            display: grid;
            grid-template-columns: 280px 1fr 320px;
            height: 100vh;
        }
        
        .sidebar {
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
            padding: 20px;
            overflow-y: auto;
        }
        
        .main-view {
            padding: 20px;
            display: flex;
            flex-direction: column;
        }
        
        .detail-panel {
            background: var(--bg-secondary);
            border-left: 1px solid var(--border);
            padding: 20px;
            overflow-y: auto;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .search-box {
            display: flex;
            gap: 8px;
            margin-bottom: 20px;
        }
        
        .search-box input {
            flex: 1;
            padding: 10px 14px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 14px;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: var(--accent);
        }
        
        .btn {
            padding: 10px 16px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: var(--accent);
            color: white;
        }
        
        .btn-primary:hover {
            background: var(--accent-hover);
        }
        
        .chain-list {
            list-style: none;
        }
        
        .chain-item {
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid transparent;
        }
        
        .chain-item:hover {
            background: var(--bg-card);
        }
        
        .chain-item.active {
            background: var(--bg-card);
            border-color: var(--accent);
        }
        
        .chain-name {
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .chain-meta {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .graph-container {
            flex: 1;
            background: var(--bg-secondary);
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }
        
        .graph-placeholder {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: var(--text-secondary);
        }
        
        .graph-placeholder .icon {
            font-size: 64px;
            margin-bottom: 16px;
        }
        
        /* 产业链图可视化 */
        .chain-graph {
            width: 100%;
            height: 100%;
            padding: 20px;
        }
        
        .chain-node {
            position: absolute;
            padding: 12px 20px;
            background: var(--bg-card);
            border-radius: 10px;
            border: 2px solid var(--border);
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
            min-width: 120px;
        }
        
        .chain-node:hover {
            transform: scale(1.05);
            border-color: var(--accent);
            box-shadow: 0 4px 20px rgba(6, 182, 212, 0.3);
        }
        
        .chain-node.upstream {
            border-color: var(--purple);
        }
        
        .chain-node.midstream {
            border-color: var(--accent);
        }
        
        .chain-node.downstream {
            border-color: var(--green);
        }
        
        .node-name {
            font-weight: 600;
            font-size: 14px;
        }
        
        .node-count {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 4px;
        }
        
        .section-title {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stock-list {
            list-style: none;
        }
        
        .stock-item {
            padding: 10px 12px;
            border-radius: 6px;
            margin-bottom: 6px;
            background: var(--bg-card);
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .stock-item:hover {
            background: var(--bg-primary);
        }
        
        .stock-symbol {
            font-family: 'SF Mono', monospace;
            color: var(--accent);
            font-size: 13px;
        }
        
        .stock-name {
            font-size: 13px;
        }
        
        .stock-score {
            font-weight: 600;
            font-size: 13px;
        }
        
        .score-high { color: var(--green); }
        .score-mid { color: var(--orange); }
        .score-low { color: var(--text-secondary); }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .stat-box {
            background: var(--bg-card);
            border-radius: 8px;
            padding: 14px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: var(--accent);
        }
        
        .stat-label {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 4px;
        }
        
        .loading-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.7);
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
        
        .tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }
        
        .tag-upstream { background: rgba(168, 85, 247, 0.2); color: var(--purple); }
        .tag-midstream { background: rgba(6, 182, 212, 0.2); color: var(--accent); }
        .tag-downstream { background: rgba(34, 197, 94, 0.2); color: var(--green); }
    </style>
</head>
<body>
    <div class="loading-overlay hidden" id="loadingOverlay">
        <div class="spinner"></div>
    </div>
    
    <div class="container">
        <div class="sidebar">
            <div class="header">
                <h1>🔗 产业链</h1>
            </div>
            
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="搜索产业链..." onkeypress="if(event.key==='Enter')search()"/>
                <button class="btn btn-primary" onclick="search()">🔍</button>
            </div>
            
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-value" id="statChains">0</div>
                    <div class="stat-label">产业链</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="statNodes">0</div>
                    <div class="stat-label">节点</div>
                </div>
            </div>
            
            <div class="section-title">热门产业链</div>
            <ul class="chain-list" id="chainList">
                <li class="chain-item" onclick="selectChain('new_energy')">
                    <div class="chain-name">🔋 新能源汽车</div>
                    <div class="chain-meta">32个节点 · 156只股票</div>
                </li>
                <li class="chain-item" onclick="selectChain('semiconductor')">
                    <div class="chain-name">💎 半导体</div>
                    <div class="chain-meta">28个节点 · 124只股票</div>
                </li>
                <li class="chain-item" onclick="selectChain('ai')">
                    <div class="chain-name">🤖 人工智能</div>
                    <div class="chain-meta">24个节点 · 98只股票</div>
                </li>
                <li class="chain-item" onclick="selectChain('photovoltaic')">
                    <div class="chain-name">☀️ 光伏</div>
                    <div class="chain-meta">20个节点 · 86只股票</div>
                </li>
            </ul>
        </div>
        
        <div class="main-view">
            <div class="header">
                <h2 id="currentChainName">选择产业链查看图谱</h2>
                <button class="btn btn-primary" onclick="refresh()">🔄 刷新</button>
            </div>
            
            <div class="graph-container" id="graphContainer">
                <div class="graph-placeholder">
                    <div class="icon">🔗</div>
                    <p>点击左侧产业链查看图谱</p>
                </div>
                
                <div class="chain-graph hidden" id="chainGraph">
                    <!-- 动态渲染节点 -->
                </div>
            </div>
        </div>
        
        <div class="detail-panel">
            <div class="section-title">节点详情</div>
            <div id="nodeDetail">
                <p style="color: var(--text-secondary); text-align: center; padding: 40px 0;">
                    点击图谱中的节点查看详情
                </p>
            </div>
            
            <div class="section-title" style="margin-top: 24px;">关联股票</div>
            <ul class="stock-list" id="stockList">
                <!-- 动态渲染 -->
            </ul>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        let currentChain = null;
        
        function refresh() {
            vscode.postMessage({ command: 'refresh' });
        }
        
        function search() {
            const query = document.getElementById('searchInput').value.trim();
            if (query) {
                vscode.postMessage({ command: 'search', query });
            }
        }
        
        function selectChain(chainId) {
            currentChain = chainId;
            document.querySelectorAll('.chain-item').forEach(el => el.classList.remove('active'));
            event.currentTarget.classList.add('active');
            vscode.postMessage({ command: 'selectChain', chainId });
            
            // 显示模拟图谱
            showMockGraph(chainId);
        }
        
        function selectNode(nodeId) {
            vscode.postMessage({ command: 'selectNode', nodeId });
        }
        
        function showMockGraph(chainId) {
            const names = {
                'new_energy': '新能源汽车',
                'semiconductor': '半导体',
                'ai': '人工智能',
                'photovoltaic': '光伏'
            };
            
            document.getElementById('currentChainName').textContent = names[chainId] || chainId;
            document.querySelector('.graph-placeholder').classList.add('hidden');
            
            const graph = document.getElementById('chainGraph');
            graph.classList.remove('hidden');
            
            // 简化的产业链节点
            const nodes = {
                'new_energy': [
                    { id: 'lithium', name: '锂矿', type: 'upstream', x: 10, y: 20 },
                    { id: 'cathode', name: '正极材料', type: 'upstream', x: 10, y: 50 },
                    { id: 'battery', name: '电池制造', type: 'midstream', x: 40, y: 35 },
                    { id: 'bms', name: 'BMS系统', type: 'midstream', x: 40, y: 65 },
                    { id: 'oem', name: '整车制造', type: 'downstream', x: 70, y: 35 },
                    { id: 'charging', name: '充电桩', type: 'downstream', x: 70, y: 65 }
                ],
                'semiconductor': [
                    { id: 'equipment', name: '设备', type: 'upstream', x: 10, y: 25 },
                    { id: 'material', name: '材料', type: 'upstream', x: 10, y: 55 },
                    { id: 'fab', name: '晶圆代工', type: 'midstream', x: 40, y: 40 },
                    { id: 'design', name: '芯片设计', type: 'midstream', x: 40, y: 70 },
                    { id: 'package', name: '封测', type: 'downstream', x: 70, y: 40 }
                ],
                'ai': [
                    { id: 'gpu', name: 'GPU芯片', type: 'upstream', x: 10, y: 30 },
                    { id: 'server', name: '服务器', type: 'upstream', x: 10, y: 60 },
                    { id: 'algorithm', name: '算法', type: 'midstream', x: 40, y: 45 },
                    { id: 'app', name: '应用', type: 'downstream', x: 70, y: 30 },
                    { id: 'data', name: '数据服务', type: 'downstream', x: 70, y: 60 }
                ],
                'photovoltaic': [
                    { id: 'silicon', name: '多晶硅', type: 'upstream', x: 10, y: 40 },
                    { id: 'wafer', name: '硅片', type: 'midstream', x: 35, y: 40 },
                    { id: 'cell', name: '电池片', type: 'midstream', x: 55, y: 40 },
                    { id: 'module', name: '组件', type: 'downstream', x: 75, y: 40 }
                ]
            };
            
            const chainNodes = nodes[chainId] || [];
            graph.innerHTML = chainNodes.map(n => \`
                <div class="chain-node \${n.type}" 
                     style="left: \${n.x}%; top: \${n.y}%;"
                     onclick="selectNode('\${n.id}')">
                    <div class="node-name">\${n.name}</div>
                    <div class="node-count">\${Math.floor(Math.random() * 20 + 5)}只股票</div>
                </div>
            \`).join('');
            
            // 显示模拟股票列表
            showMockStocks();
        }
        
        function showMockStocks() {
            const stocks = [
                { symbol: '300750.SZ', name: '宁德时代', score: 85 },
                { symbol: '002594.SZ', name: '比亚迪', score: 78 },
                { symbol: '300014.SZ', name: '亿纬锂能', score: 72 },
                { symbol: '002466.SZ', name: '天齐锂业', score: 68 },
                { symbol: '300568.SZ', name: '星源材质', score: 65 }
            ];
            
            document.getElementById('stockList').innerHTML = stocks.map(s => \`
                <li class="stock-item" onclick="viewStock('\${s.symbol}')">
                    <div>
                        <div class="stock-symbol">\${s.symbol}</div>
                        <div class="stock-name">\${s.name}</div>
                    </div>
                    <div class="stock-score \${s.score >= 75 ? 'score-high' : s.score >= 60 ? 'score-mid' : 'score-low'}">
                        \${s.score}分
                    </div>
                </li>
            \`).join('');
        }
        
        function viewStock(symbol) {
            vscode.postMessage({ command: 'viewStock', symbol });
        }
        
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'loading':
                    document.getElementById('loadingOverlay').classList.toggle('hidden', !message.loading);
                    break;
                case 'updateData':
                    if (message.data.stats) {
                        document.getElementById('statChains').textContent = message.data.stats.chain_count || 0;
                        document.getElementById('statNodes').textContent = message.data.stats.node_count || 0;
                    }
                    break;
            }
        });
        
        // 初始化
        document.getElementById('statChains').textContent = '4';
        document.getElementById('statNodes').textContent = '104';
    </script>
</body>
</html>`;
    }

    public dispose() {
        IndustryChainPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }
}
