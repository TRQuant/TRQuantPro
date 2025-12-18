/**
 * 策略生成面板
 * ============
 * 
 * 调用 strategy-server MCP 生成量化策略代码
 * 
 * 功能:
 * - 策略模板选择
 * - 参数配置
 * - 多平台代码生成 (JoinQuant/BulletTrade/PTrade/QMT)
 * - 代码预览和保存
 * - 平台转换
 */

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';
import { generateTraceId } from '../services/mcpClientV2';

const MODULE = 'StrategyGeneratorPanel';

// 策略模板定义
const STRATEGY_TEMPLATES = [
    {
        id: 'momentum',
        name: '动量策略',
        icon: '🚀',
        color: '#3B82F6',
        description: '追涨强势股，适合趋势市',
        params: [
            { name: 'short_period', label: '短期周期', type: 'number', default: 5, min: 1, max: 30 },
            { name: 'long_period', label: '长期周期', type: 'number', default: 20, min: 5, max: 120 },
            { name: 'max_stocks', label: '持股数量', type: 'number', default: 10, min: 1, max: 50 },
            { name: 'rebalance_days', label: '调仓周期', type: 'number', default: 5, min: 1, max: 30 },
            { name: 'stop_loss', label: '止损比例', type: 'number', default: 0.08, min: 0.01, max: 0.3, step: 0.01 },
            { name: 'take_profit', label: '止盈比例', type: 'number', default: 0.2, min: 0.05, max: 1.0, step: 0.05 }
        ]
    },
    {
        id: 'mean_reversion',
        name: '均值回归',
        icon: '🔄',
        color: '#10B981',
        description: '买入超跌股票，适合震荡市',
        params: [
            { name: 'lookback', label: '回看周期', type: 'number', default: 20, min: 5, max: 60 },
            { name: 'std_threshold', label: '标准差阈值', type: 'number', default: 2.0, min: 1.0, max: 3.0, step: 0.1 },
            { name: 'max_stocks', label: '持股数量', type: 'number', default: 10, min: 1, max: 50 },
            { name: 'holding_days', label: '持有天数', type: 'number', default: 5, min: 1, max: 20 }
        ]
    },
    {
        id: 'rotation',
        name: '轮动策略',
        icon: '🔁',
        color: '#F59E0B',
        description: '行业/风格轮动，适合结构性行情',
        params: [
            { name: 'momentum_period', label: '动量周期', type: 'number', default: 20, min: 5, max: 60 },
            { name: 'holding_period', label: '持有周期', type: 'number', default: 5, min: 1, max: 20 },
            { name: 'top_n', label: '选择数量', type: 'number', default: 3, min: 1, max: 10 }
        ]
    }
];

const PLATFORMS = [
    { id: 'joinquant', name: 'JoinQuant', icon: '📊' },
    { id: 'bullettrade', name: 'BulletTrade', icon: '🎯' },
    { id: 'ptrade', name: 'PTrade', icon: '💼' },
    { id: 'qmt', name: 'QMT', icon: '📈' }
];

export class StrategyGeneratorPanel {
    public static currentPanel: StrategyGeneratorPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private _disposables: vscode.Disposable[] = [];
    
    private _generatedCode: string = '';
    private _currentStrategy: string = 'momentum';
    private _currentPlatform: string = 'joinquant';

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._client = client;

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
        client: TRQuantClient
    ): StrategyGeneratorPanel {
        logger.info('创建策略生成面板', MODULE);
        
        const column = vscode.ViewColumn.One;

        if (StrategyGeneratorPanel.currentPanel) {
            StrategyGeneratorPanel.currentPanel._panel.reveal(column);
            return StrategyGeneratorPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'trquantStrategyGenerator',
            '🛠️ 策略生成器',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        StrategyGeneratorPanel.currentPanel = new StrategyGeneratorPanel(panel, extensionUri, client);
        return StrategyGeneratorPanel.currentPanel;
    }

    public dispose(): void {
        StrategyGeneratorPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }

    // ==================== 消息处理 ====================

    private async _handleMessage(message: any): Promise<void> {
        logger.info(`[StrategyGeneratorPanel] 收到消息: ${message.command}`, MODULE);

        switch (message.command) {
            case 'generate':
                await this._generateStrategy(message.strategyType, message.params, message.platform);
                break;
            case 'convert':
                await this._convertStrategy(message.code, message.fromPlatform, message.toPlatform);
                break;
            case 'validate':
                await this._validateStrategy(message.code, message.platform);
                break;
            case 'save':
                await this._saveStrategy(message.code, message.filename);
                break;
            case 'copyToClipboard':
                await vscode.env.clipboard.writeText(message.code);
                vscode.window.showInformationMessage('代码已复制到剪贴板');
                break;
            case 'openInEditor':
                await this._openInEditor(message.code);
                break;
            case 'runBacktest':
                await this._runBacktest(message.code);
                break;
        }
    }

    // ==================== MCP调用 ====================

    /**
     * 生成策略代码
     */
    private async _generateStrategy(
        strategyType: string,
        params: Record<string, unknown>,
        platform: string
    ): Promise<void> {
        this._postMessage({ command: 'generating' });

        try {
            const response = await this._client.callBridge('call_mcp_tool', {
                tool_name: 'strategy_template.generate',
                arguments: {
                    strategy_type: strategyType,
                    params: params,
                    platform: platform
                },
                trace_id: generateTraceId()
            });

            const resp = response as any;
            if (resp.ok && resp.data) {
                this._generatedCode = resp.data.code || resp.data;
                this._currentStrategy = strategyType;
                this._currentPlatform = platform;

                this._postMessage({
                    command: 'generated',
                    code: this._generatedCode,
                    strategyName: resp.data.strategy_name || `${strategyType}_strategy`,
                    platform: platform
                });

                logger.info(`策略生成成功: ${strategyType} -> ${platform}`, MODULE);
            } else {
                throw new Error(resp.error || '生成失败');
            }
        } catch (error: any) {
            logger.error(`策略生成失败: ${error.message}`, MODULE);
            this._postMessage({
                command: 'error',
                message: `策略生成失败: ${error.message}`
            });
            vscode.window.showErrorMessage(`策略生成失败: ${error.message}`);
        }
    }

    /**
     * 转换策略平台
     */
    private async _convertStrategy(
        code: string,
        fromPlatform: string,
        toPlatform: string
    ): Promise<void> {
        this._postMessage({ command: 'converting' });

        try {
            const response = await this._client.callBridge('call_mcp_tool', {
                tool_name: 'strategy.convert',
                arguments: {
                    code: code,
                    from_platform: fromPlatform,
                    to_platform: toPlatform
                },
                trace_id: generateTraceId()
            });

            const resp = response as any;
            if (resp.ok && resp.data) {
                this._generatedCode = resp.data.code || resp.data;
                this._currentPlatform = toPlatform;

                this._postMessage({
                    command: 'converted',
                    code: this._generatedCode,
                    fromPlatform,
                    toPlatform
                });

                vscode.window.showInformationMessage(`策略已转换: ${fromPlatform} → ${toPlatform}`);
            } else {
                throw new Error(resp.error || '转换失败');
            }
        } catch (error: any) {
            this._postMessage({
                command: 'error',
                message: `转换失败: ${error.message}`
            });
        }
    }

    /**
     * 验证策略代码
     */
    private async _validateStrategy(code: string, platform: string): Promise<void> {
        try {
            const response = await this._client.callBridge('call_mcp_tool', {
                tool_name: 'strategy.validate',
                arguments: {
                    code: code,
                    platform: platform
                },
                trace_id: generateTraceId()
            });

            const resp = response as any;
            if (resp.ok && resp.data) {
                const valid = resp.data.valid;
                const issues = resp.data.issues || [];

                this._postMessage({
                    command: 'validated',
                    valid,
                    issues
                });

                if (valid) {
                    vscode.window.showInformationMessage('策略代码验证通过 ✅');
                } else {
                    vscode.window.showWarningMessage(`策略代码有 ${issues.length} 个问题`);
                }
            }
        } catch (error: any) {
            this._postMessage({
                command: 'error',
                message: `验证失败: ${error.message}`
            });
        }
    }

    /**
     * 保存策略到文件
     */
    private async _saveStrategy(code: string, filename?: string): Promise<void> {
        const defaultName = `${this._currentStrategy}_${this._currentPlatform}_${Date.now()}.py`;
        
        const uri = await vscode.window.showSaveDialog({
            defaultUri: vscode.Uri.file(path.join(
                vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '',
                'strategies',
                filename || defaultName
            )),
            filters: {
                'Python': ['py']
            }
        });

        if (uri) {
            await vscode.workspace.fs.writeFile(uri, Buffer.from(code, 'utf-8'));
            vscode.window.showInformationMessage(`策略已保存: ${uri.fsPath}`);
            
            // 打开保存的文件
            const doc = await vscode.workspace.openTextDocument(uri);
            await vscode.window.showTextDocument(doc);
        }
    }

    /**
     * 在编辑器中打开代码
     */
    private async _openInEditor(code: string): Promise<void> {
        const doc = await vscode.workspace.openTextDocument({
            content: code,
            language: 'python'
        });
        await vscode.window.showTextDocument(doc);
    }

    /**
     * 运行回测
     */
    private async _runBacktest(code: string): Promise<void> {
        // 触发回测面板
        await vscode.commands.executeCommand('trquant.openBacktestPanel', { code });
    }

    // ==================== UI通信 ====================

    private _postMessage(message: any): void {
        this._panel.webview.postMessage(message);
    }

    // ==================== HTML内容 ====================

    private _getHtmlContent(): string {
        const templatesHtml = STRATEGY_TEMPLATES.map(t => `
            <div class="template-card" data-id="${t.id}" onclick="selectTemplate('${t.id}')">
                <div class="template-icon" style="color: ${t.color}">${t.icon}</div>
                <div class="template-info">
                    <div class="template-name">${t.name}</div>
                    <div class="template-desc">${t.description}</div>
                </div>
            </div>
        `).join('');

        const platformsHtml = PLATFORMS.map(p => `
            <label class="platform-option">
                <input type="radio" name="platform" value="${p.id}" ${p.id === 'joinquant' ? 'checked' : ''}>
                <span class="platform-label">${p.icon} ${p.name}</span>
            </label>
        `).join('');

        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>策略生成器</title>
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
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-primary);
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 8px;
        }
        
        .header p {
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 24px;
        }
        
        .config-panel {
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
        
        .template-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 24px;
        }
        
        .template-card {
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
        
        .template-card:hover {
            border-color: var(--accent);
        }
        
        .template-card.selected {
            border-color: var(--accent);
            background: rgba(88, 166, 255, 0.1);
        }
        
        .template-icon {
            font-size: 24px;
        }
        
        .template-name {
            font-weight: 600;
        }
        
        .template-desc {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .params-form {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 24px;
        }
        
        .param-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .param-label {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .param-input {
            padding: 8px 12px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 14px;
        }
        
        .platform-select {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 24px;
        }
        
        .platform-option {
            cursor: pointer;
        }
        
        .platform-option input {
            display: none;
        }
        
        .platform-label {
            display: inline-block;
            padding: 8px 16px;
            background: var(--bg-tertiary);
            border: 2px solid transparent;
            border-radius: 6px;
            font-size: 13px;
            transition: all 0.2s;
        }
        
        .platform-option input:checked + .platform-label {
            border-color: var(--accent);
            background: rgba(88, 166, 255, 0.1);
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            width: 100%;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: var(--accent);
            color: white;
        }
        
        .btn-primary:hover {
            opacity: 0.9;
        }
        
        .btn-primary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .code-panel {
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
        }
        
        .code-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-primary);
        }
        
        .code-actions {
            display: flex;
            gap: 8px;
        }
        
        .btn-small {
            padding: 6px 12px;
            font-size: 12px;
            border-radius: 4px;
        }
        
        .code-content {
            flex: 1;
            padding: 16px;
            overflow: auto;
            min-height: 400px;
        }
        
        .code-content pre {
            margin: 0;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 13px;
            line-height: 1.5;
            white-space: pre-wrap;
        }
        
        .placeholder {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: var(--text-secondary);
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: var(--accent);
        }
        
        .loading::after {
            content: '';
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid var(--accent);
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-left: 8px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛠️ 策略生成器</h1>
        <p>选择策略模板，配置参数，一键生成多平台量化策略代码</p>
    </div>
    
    <div class="main-grid">
        <div class="config-panel">
            <div class="section-title">📋 策略模板</div>
            <div class="template-list">
                ${templatesHtml}
            </div>
            
            <div class="section-title">⚙️ 参数配置</div>
            <div class="params-form" id="params-form">
                <!-- 动态填充 -->
            </div>
            
            <div class="section-title">🖥️ 目标平台</div>
            <div class="platform-select">
                ${platformsHtml}
            </div>
            
            <button class="btn btn-primary" id="generate-btn" onclick="generate()">
                🚀 生成策略代码
            </button>
        </div>
        
        <div class="code-panel">
            <div class="code-header">
                <span id="code-title">生成的代码</span>
                <div class="code-actions">
                    <button class="btn btn-small" onclick="copyCode()">📋 复制</button>
                    <button class="btn btn-small" onclick="saveCode()">💾 保存</button>
                    <button class="btn btn-small" onclick="openInEditor()">📝 编辑</button>
                    <button class="btn btn-small btn-primary" onclick="runBacktest()">▶️ 回测</button>
                </div>
            </div>
            <div class="code-content" id="code-content">
                <div class="placeholder">选择策略模板并点击"生成策略代码"</div>
            </div>
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        const templates = ${JSON.stringify(STRATEGY_TEMPLATES)};
        let currentTemplate = templates[0];
        let generatedCode = '';
        
        // 初始化
        selectTemplate('momentum');
        
        function selectTemplate(id) {
            currentTemplate = templates.find(t => t.id === id);
            
            // 更新UI
            document.querySelectorAll('.template-card').forEach(card => {
                card.classList.toggle('selected', card.dataset.id === id);
            });
            
            // 更新参数表单
            renderParams();
        }
        
        function renderParams() {
            const form = document.getElementById('params-form');
            form.innerHTML = currentTemplate.params.map(p => \`
                <div class="param-group">
                    <label class="param-label">\${p.label}</label>
                    <input type="number" 
                           class="param-input" 
                           id="param-\${p.name}" 
                           value="\${p.default}"
                           min="\${p.min || 0}"
                           max="\${p.max || 1000}"
                           step="\${p.step || 1}">
                </div>
            \`).join('');
        }
        
        function getParams() {
            const params = {};
            currentTemplate.params.forEach(p => {
                const input = document.getElementById('param-' + p.name);
                params[p.name] = parseFloat(input.value);
            });
            return params;
        }
        
        function getPlatform() {
            const selected = document.querySelector('input[name="platform"]:checked');
            return selected ? selected.value : 'joinquant';
        }
        
        function generate() {
            const btn = document.getElementById('generate-btn');
            btn.disabled = true;
            btn.textContent = '生成中...';
            
            vscode.postMessage({
                command: 'generate',
                strategyType: currentTemplate.id,
                params: getParams(),
                platform: getPlatform()
            });
        }
        
        function copyCode() {
            if (generatedCode) {
                vscode.postMessage({ command: 'copyToClipboard', code: generatedCode });
            }
        }
        
        function saveCode() {
            if (generatedCode) {
                vscode.postMessage({ command: 'save', code: generatedCode });
            }
        }
        
        function openInEditor() {
            if (generatedCode) {
                vscode.postMessage({ command: 'openInEditor', code: generatedCode });
            }
        }
        
        function runBacktest() {
            if (generatedCode) {
                vscode.postMessage({ command: 'runBacktest', code: generatedCode });
            }
        }
        
        // 消息处理
        window.addEventListener('message', event => {
            const message = event.data;
            const btn = document.getElementById('generate-btn');
            const content = document.getElementById('code-content');
            const title = document.getElementById('code-title');
            
            switch (message.command) {
                case 'generating':
                    content.innerHTML = '<div class="loading">正在生成策略代码</div>';
                    break;
                    
                case 'generated':
                    btn.disabled = false;
                    btn.textContent = '🚀 生成策略代码';
                    generatedCode = message.code;
                    content.innerHTML = '<pre>' + escapeHtml(message.code) + '</pre>';
                    title.textContent = message.strategyName + ' (' + message.platform + ')';
                    break;
                    
                case 'error':
                    btn.disabled = false;
                    btn.textContent = '🚀 生成策略代码';
                    content.innerHTML = '<div class="placeholder" style="color: var(--error);">' + message.message + '</div>';
                    break;
            }
        });
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>`;
    }
}
