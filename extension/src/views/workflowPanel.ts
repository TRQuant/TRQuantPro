/**
 * 9步工作流面板 - 专业版
 * =======================
 * 
 * 设计原则：
 * 1. 简洁的CSP配置 - 移除nonce要求，允许内联样式
 * 2. 事件委托 - 统一事件处理，避免复杂的绑定
 * 3. 清晰的错误处理 - 所有错误都有详细日志
 * 4. 无alert - 使用视觉反馈代替弹窗
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn } from 'child_process';

interface MCPResult {
    ok: boolean;
    data: any;
    error?: string;
    details?: string;
}

interface WorkflowStep {
    id: number;
    name: string;
    stepId: string;
    icon: string;
    description: string;
}

const WORKFLOW_STEPS: WorkflowStep[] = [
    { id: 1, name: '数据源检查', stepId: 'data_source', icon: '🔌', description: '检查数据连接' },
    { id: 2, name: '市场趋势', stepId: 'market_trend', icon: '📈', description: '分析大盘走势' },
    { id: 3, name: '主线识别', stepId: 'mainline', icon: '🎯', description: '识别投资主线' },
    { id: 4, name: '候选池构建', stepId: 'candidate_pool', icon: '🏊', description: '筛选候选标的' },
    { id: 5, name: '因子评估', stepId: 'factor', icon: '🔢', description: '计算因子得分' },
    { id: 6, name: '策略生成', stepId: 'strategy', icon: '📋', description: '生成交易策略' },
    { id: 7, name: '回测验证', stepId: 'backtest', icon: '🔙', description: '历史回测验证' },
    { id: 8, name: '参数优化', stepId: 'optimization', icon: '⚙️', description: '优化策略参数' },
    { id: 9, name: '生成报告', stepId: 'report', icon: '📄', description: '输出分析报告' }
];

export class WorkflowPanel {
    public static currentPanel: WorkflowPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _disposables: vscode.Disposable[] = [];
    private _workflowId: string | null = null;
    private _stepResults: Map<number, any> = new Map();
    private _stepStatus: Map<number, 'pending' | 'running' | 'completed' | 'error'> = new Map();

    private constructor(panel: vscode.WebviewPanel, private readonly _projectRoot: string) {
        this._panel = panel;
        this._initializeStepStatus();
        this._panel.webview.html = this._getHtml();
        
        this._panel.webview.onDidReceiveMessage(
            async (msg) => await this._handleMessage(msg),
            null,
            this._disposables
        );
        
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        this._log('面板创建成功');
    }

    private _initializeStepStatus() {
        WORKFLOW_STEPS.forEach(step => {
            this._stepStatus.set(step.id, 'pending');
        });
    }

    public static createOrShow(extensionUri: vscode.Uri, extensionPath?: string) {
        const column = vscode.window.activeTextEditor?.viewColumn || vscode.ViewColumn.One;
        
        if (WorkflowPanel.currentPanel) {
            WorkflowPanel.currentPanel._panel.reveal(column);
            return WorkflowPanel.currentPanel;
        }

        // 确定项目根目录
        let projectRoot = '/home/taotao/dev/QuantTest/TRQuant';
        if (extensionPath) {
            // extensionPath 可能是 extension 目录或项目根目录
            if (extensionPath.endsWith('/extension')) {
                projectRoot = path.dirname(extensionPath);
            } else if (fs.existsSync(path.join(extensionPath, 'extension'))) {
                projectRoot = extensionPath;
            }
        }

        const panel = vscode.window.createWebviewPanel(
            'trquantWorkflow',
            '🐉 9步投资工作流',
            column,
            { enableScripts: true, retainContextWhenHidden: true }
        );

        WorkflowPanel.currentPanel = new WorkflowPanel(panel, projectRoot);
        return WorkflowPanel.currentPanel;
    }

    private _log(message: string, data?: any) {
        const timestamp = new Date().toISOString().substring(11, 23);
        if (data) {
            console.log(`[Workflow ${timestamp}] ${message}`, data);
        } else {
            console.log(`[Workflow ${timestamp}] ${message}`);
        }
    }

    private async _handleMessage(msg: any): Promise<void> {
        this._log(`收到消息: ${msg.command}`, msg);
        
        try {
            switch (msg.command) {
                case 'runStep':
                    await this._runStep(msg.step);
                    break;
                case 'runAll':
                    await this._runAllSteps();
                    break;
                case 'reset':
                    await this._resetWorkflow();
                    break;
                case 'getResult':
                    this._sendResult(msg.step);
                    break;
                case 'checkStatus':
                    await this._checkMcpStatus();
                    break;
            }
        } catch (error) {
            this._log('消息处理错误', error);
            this._sendError('处理消息时出错', error);
        }
    }

    private async _runStep(stepNum: number): Promise<void> {
        const step = WORKFLOW_STEPS.find(s => s.id === stepNum);
        if (!step) {
            this._sendError(`无效的步骤: ${stepNum}`);
            return;
        }

        this._log(`开始执行步骤 ${stepNum}: ${step.name}`);
        this._updateStepStatus(stepNum, 'running');

        try {
            // 确保有工作流会话
            if (!this._workflowId) {
                const createResult = await this._callMCP('workflow9.create', { name: '工作流面板' });
                if (createResult.ok && createResult.data?.workflow_id) {
                    this._workflowId = createResult.data.workflow_id;
                    this._log(`创建工作流会话: ${this._workflowId}`);
                } else {
                    throw new Error('创建工作流失败: ' + (createResult.error || '未知错误'));
                }
            }

            // 执行步骤
            const result = await this._callMCP('workflow9.run_step', {
                workflow_id: this._workflowId,
                step_id: step.stepId,
                args: {}
            });

            if (result.ok) {
                this._stepResults.set(stepNum, result.data);
                this._updateStepStatus(stepNum, 'completed');
                this._log(`步骤 ${stepNum} 完成`, result.data);
            } else {
                throw new Error(result.error || '步骤执行失败');
            }
        } catch (error) {
            this._updateStepStatus(stepNum, 'error', this._getErrorMessage(error));
            this._log(`步骤 ${stepNum} 失败`, error);
        }
    }

    private async _runAllSteps(): Promise<void> {
        this._log('开始一键执行全部步骤');
        
        for (const step of WORKFLOW_STEPS) {
            const currentStatus = this._stepStatus.get(step.id);
            if (currentStatus !== 'completed') {
                await this._runStep(step.id);
                
                // 如果步骤失败，停止执行
                if (this._stepStatus.get(step.id) === 'error') {
                    this._log(`步骤 ${step.id} 失败，停止执行后续步骤`);
                    break;
                }
            }
        }
        
        this._log('一键执行完成');
    }

    private async _resetWorkflow(): Promise<void> {
        this._log('重置工作流');
        this._workflowId = null;
        this._stepResults.clear();
        this._initializeStepStatus();
        
        // 通知前端刷新
        this._panel.webview.postMessage({ command: 'reset' });
    }

    private _sendResult(stepNum: number): void {
        const result = this._stepResults.get(stepNum);
        this._panel.webview.postMessage({
            command: 'result',
            step: stepNum,
            data: result || null
        });
    }

    private async _checkMcpStatus(): Promise<void> {
        this._log('检查MCP状态');
        
        const status: Record<string, { ok: boolean; message: string }> = {};
        
        // 测试workflow服务器
        try {
            const result = await this._callMCP('workflow9.get_steps', {});
            status.workflow = { ok: result.ok, message: result.ok ? '正常' : (result.error || '异常') };
        } catch (e) {
            status.workflow = { ok: false, message: String(e) };
        }
        
        // 测试数据源
        try {
            const result = await this._callMCP('data_source.health_check', {});
            status.datasource = { ok: result.ok, message: result.ok ? '正常' : (result.error || '异常') };
        } catch (e) {
            status.datasource = { ok: false, message: String(e) };
        }
        
        this._panel.webview.postMessage({ command: 'mcpStatus', status });
    }

    private _updateStepStatus(stepNum: number, status: 'pending' | 'running' | 'completed' | 'error', error?: string): void {
        this._stepStatus.set(stepNum, status);
        
        this._panel.webview.postMessage({
            command: 'stepUpdate',
            step: stepNum,
            status,
            error,
            result: status === 'completed' ? this._stepResults.get(stepNum) : null
        });
    }

    private _sendError(message: string, error?: any): void {
        const details = error ? this._getErrorMessage(error) : '';
        this._panel.webview.postMessage({
            command: 'error',
            message,
            details
        });
    }

    private _getErrorMessage(error: any): string {
        if (error instanceof Error) {
            return error.stack || error.message;
        }
        return String(error);
    }

    private async _callMCP(toolName: string, args: Record<string, any>): Promise<MCPResult> {
        const pythonPath = this._findPython();
        const bridgePath = path.join(this._projectRoot, 'extension', 'python', 'bridge.py');
        
        if (!fs.existsSync(bridgePath)) {
            return { ok: false, data: null, error: `Bridge文件不存在: ${bridgePath}` };
        }

        this._log(`调用MCP: ${toolName}`, { pythonPath, bridgePath, args });

        return new Promise((resolve) => {
            const pythonPaths = [
                this._projectRoot,
                path.join(this._projectRoot, 'mcp_servers'),
                path.join(this._projectRoot, 'extension', 'python')
            ].join(':');

            const proc = spawn(pythonPath, [bridgePath], {
                cwd: this._projectRoot,
                env: {
                    ...process.env,
                    PYTHONPATH: pythonPaths,
                    TRQUANT_ROOT: this._projectRoot,
                    PYTHONIOENCODING: 'utf-8'
                },
                stdio: ['pipe', 'pipe', 'pipe']
            });

            let stdout = '';
            let stderr = '';
            
            proc.stdout.on('data', (d) => { stdout += d.toString(); });
            proc.stderr.on('data', (d) => { stderr += d.toString(); });

            const timeout = setTimeout(() => {
                proc.kill();
                resolve({ ok: false, data: null, error: '调用超时(30秒)' });
            }, 30000);

            proc.on('close', (code) => {
                clearTimeout(timeout);
                this._log(`MCP返回: code=${code}, stdout长度=${stdout.length}`, { stderr: stderr.substring(0, 200) });
                
                if (code === 0 || stdout.includes('"ok"')) {
                    try {
                        const lines = stdout.trim().split('\n');
                        const lastLine = lines[lines.length - 1];
                        const result = JSON.parse(lastLine);
                        resolve({
                            ok: result.ok !== false,
                            data: result.data || result,
                            error: result.error,
                            details: result.traceback
                        });
                    } catch (e) {
                        resolve({ 
                            ok: false, 
                            data: null, 
                            error: `JSON解析失败`,
                            details: stdout.substring(0, 500) 
                        });
                    }
                } else {
                    resolve({ 
                        ok: false, 
                        data: null, 
                        error: `进程退出码: ${code}`,
                        details: stderr || stdout 
                    });
                }
            });

            const request = {
                action: 'call_mcp_tool',
                params: { tool_name: toolName, arguments: args }
            };
            
            proc.stdin.write(JSON.stringify(request));
            proc.stdin.end();
        });
    }

    private _findPython(): string {
        const candidates = [
            path.join(this._projectRoot, 'venv', 'bin', 'python3'),
            path.join(this._projectRoot, 'venv', 'bin', 'python'),
            'python3',
            'python'
        ];
        
        for (const p of candidates) {
            if (p.startsWith('/') && fs.existsSync(p)) {
                return p;
            }
        }
        return candidates[2]; // fallback to python3
    }

    private _getHtml(): string {
        const stepsHtml = WORKFLOW_STEPS.map(step => `
            <div class="step" data-step="${step.id}">
                <div class="step-header">
                    <span class="step-icon">${step.icon}</span>
                    <span class="step-num">${step.id}</span>
                    <span class="step-status"></span>
                </div>
                <div class="step-name">${step.name}</div>
                <div class="step-desc">${step.description}</div>
                <div class="step-error"></div>
                <div class="step-actions">
                    <button class="btn btn-run" data-action="run" data-step="${step.id}">▶ 执行</button>
                    <button class="btn btn-result" data-action="result" data-step="${step.id}">📋 结果</button>
                </div>
            </div>
        `).join('');

        return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
    <style>
        :root {
            --bg: #1e1e1e;
            --fg: #cccccc;
            --border: #3c3c3c;
            --accent: #0078d4;
            --success: #4caf50;
            --error: #f44336;
            --warning: #ff9800;
            --hover: #2d2d30;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
            background: var(--bg); 
            color: var(--fg); 
            padding: 20px;
            line-height: 1.5;
        }
        
        .header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }
        .title { font-size: 20px; font-weight: 600; }
        .actions { display: flex; gap: 8px; }
        
        .btn {
            padding: 8px 16px;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            transition: opacity 0.2s;
        }
        .btn:hover { opacity: 0.85; }
        .btn:active { opacity: 0.7; }
        .btn-secondary { background: #555; }
        .btn-run { background: var(--success); padding: 4px 8px; font-size: 11px; }
        .btn-result { background: #555; padding: 4px 8px; font-size: 11px; }
        
        .mcp-status {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: #252526;
            border-radius: 6px;
            margin-bottom: 16px;
            font-size: 12px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--warning);
        }
        .status-dot.ok { background: var(--success); }
        .status-dot.error { background: var(--error); }
        
        .steps {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 12px;
        }
        
        .step {
            background: #252526;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }
        .step:hover { background: var(--hover); border-color: var(--accent); }
        .step.running { border-color: var(--accent); animation: pulse 1s infinite; }
        .step.completed { border-color: var(--success); background: rgba(76, 175, 80, 0.1); }
        .step.error { border-color: var(--error); background: rgba(244, 67, 54, 0.1); }
        
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
        
        .step-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
        .step-icon { font-size: 20px; }
        .step-num { 
            background: var(--border); 
            color: #888; 
            width: 20px; 
            height: 20px; 
            border-radius: 50%; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 11px;
        }
        .step.completed .step-num { background: var(--success); color: white; }
        .step.error .step-num { background: var(--error); color: white; }
        
        .step-status {
            margin-left: auto;
            font-size: 14px;
        }
        .step.running .step-status::after { content: '⏳'; }
        .step.completed .step-status::after { content: '✅'; }
        .step.error .step-status::after { content: '❌'; }
        
        .step-name { font-weight: 600; font-size: 14px; margin-bottom: 4px; }
        .step-desc { font-size: 12px; color: #888; margin-bottom: 8px; }
        
        .step-error {
            font-size: 11px;
            color: var(--error);
            background: rgba(244, 67, 54, 0.1);
            padding: 6px 8px;
            border-radius: 4px;
            margin-bottom: 8px;
            display: none;
            max-height: 60px;
            overflow: hidden;
        }
        .step.error .step-error { display: block; }
        
        .step-actions { display: flex; gap: 6px; }
        
        .result-panel {
            margin-top: 20px;
            background: #252526;
            border: 1px solid var(--border);
            border-radius: 8px;
            display: none;
        }
        .result-panel.show { display: block; }
        .result-header {
            display: flex;
            justify-content: space-between;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
        }
        .result-title { font-weight: 600; }
        .result-close { cursor: pointer; color: #888; }
        .result-content {
            padding: 16px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Consolas', monospace;
            font-size: 12px;
            white-space: pre-wrap;
        }
        
        .error-panel {
            background: rgba(244, 67, 54, 0.1);
            border: 1px solid var(--error);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            display: none;
        }
        .error-panel.show { display: block; }
        .error-title { font-weight: 600; color: var(--error); margin-bottom: 8px; }
        .error-message { font-size: 13px; margin-bottom: 8px; }
        .error-details { 
            font-family: monospace; 
            font-size: 11px; 
            background: rgba(0,0,0,0.2); 
            padding: 8px; 
            border-radius: 4px;
            max-height: 100px;
            overflow-y: auto;
        }
        
        .log { 
            margin-top: 20px; 
            padding: 12px; 
            background: #1a1a1a; 
            border-radius: 6px;
            font-family: monospace;
            font-size: 11px;
            max-height: 150px;
            overflow-y: auto;
        }
        .log-entry { margin-bottom: 4px; }
        .log-time { color: #666; }
        .log-info { color: #4fc3f7; }
        .log-success { color: var(--success); }
        .log-error { color: var(--error); }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🐉 9步投资工作流</div>
        <div class="actions">
            <button class="btn" data-action="runAll">🚀 一键执行</button>
            <button class="btn btn-secondary" data-action="reset">🔄 重置</button>
            <button class="btn btn-secondary" data-action="checkStatus">📡 检查连接</button>
        </div>
    </div>
    
    <div class="mcp-status" id="mcpStatus">
        <span class="status-dot" id="statusDot"></span>
        <span>MCP状态:</span>
        <span id="statusText">点击"检查连接"查看</span>
    </div>
    
    <div class="error-panel" id="errorPanel">
        <div class="error-title">⚠️ 错误</div>
        <div class="error-message" id="errorMessage"></div>
        <div class="error-details" id="errorDetails"></div>
    </div>
    
    <div class="steps" id="steps">${stepsHtml}</div>
    
    <div class="result-panel" id="resultPanel">
        <div class="result-header">
            <span class="result-title" id="resultTitle">结果</span>
            <span class="result-close" data-action="closeResult">✕</span>
        </div>
        <div class="result-content" id="resultContent"></div>
    </div>
    
    <div class="log" id="log"></div>

    <script>
        const vscode = acquireVsCodeApi();
        
        // 日志函数
        function log(msg, type = 'info') {
            const logEl = document.getElementById('log');
            const time = new Date().toISOString().substring(11, 19);
            const entry = document.createElement('div');
            entry.className = 'log-entry log-' + type;
            entry.innerHTML = '<span class="log-time">[' + time + ']</span> ' + msg;
            logEl.appendChild(entry);
            logEl.scrollTop = logEl.scrollHeight;
            console.log('[Workflow]', msg);
        }
        
        // 事件委托 - 统一处理所有点击
        document.addEventListener('click', function(e) {
            const target = e.target.closest('[data-action]');
            if (!target) return;
            
            const action = target.dataset.action;
            const step = target.dataset.step ? parseInt(target.dataset.step) : null;
            
            log('点击: action=' + action + (step ? ', step=' + step : ''));
            
            switch(action) {
                case 'run':
                    if (step) {
                        log('执行步骤 ' + step);
                        vscode.postMessage({ command: 'runStep', step: step });
                    }
                    break;
                case 'runAll':
                    log('一键执行全部');
                    vscode.postMessage({ command: 'runAll' });
                    break;
                case 'reset':
                    log('重置工作流');
                    vscode.postMessage({ command: 'reset' });
                    break;
                case 'result':
                    if (step) {
                        log('查看步骤 ' + step + ' 结果');
                        vscode.postMessage({ command: 'getResult', step: step });
                    }
                    break;
                case 'closeResult':
                    document.getElementById('resultPanel').classList.remove('show');
                    break;
                case 'checkStatus':
                    log('检查MCP状态');
                    vscode.postMessage({ command: 'checkStatus' });
                    break;
            }
        });
        
        // 处理来自扩展的消息
        window.addEventListener('message', function(event) {
            const msg = event.data;
            log('收到消息: ' + msg.command, 'info');
            
            switch(msg.command) {
                case 'stepUpdate':
                    updateStep(msg.step, msg.status, msg.error);
                    break;
                case 'result':
                    showResult(msg.step, msg.data);
                    break;
                case 'reset':
                    resetUI();
                    break;
                case 'error':
                    showError(msg.message, msg.details);
                    break;
                case 'mcpStatus':
                    updateMcpStatus(msg.status);
                    break;
            }
        });
        
        function updateStep(step, status, error) {
            const el = document.querySelector('[data-step="' + step + '"]');
            if (!el) return;
            
            // 移除所有状态类
            el.classList.remove('pending', 'running', 'completed', 'error');
            el.classList.add(status);
            
            // 更新错误信息
            const errorEl = el.querySelector('.step-error');
            if (error && status === 'error') {
                errorEl.textContent = error.substring(0, 100);
                log('步骤 ' + step + ' 失败: ' + error.substring(0, 50), 'error');
            } else {
                errorEl.textContent = '';
            }
            
            if (status === 'completed') {
                log('步骤 ' + step + ' 完成 ✅', 'success');
            } else if (status === 'running') {
                log('步骤 ' + step + ' 执行中...');
            }
        }
        
        function showResult(step, data) {
            const panel = document.getElementById('resultPanel');
            const title = document.getElementById('resultTitle');
            const content = document.getElementById('resultContent');
            
            title.textContent = '步骤 ' + step + ' 结果';
            content.textContent = data ? JSON.stringify(data, null, 2) : '暂无数据';
            panel.classList.add('show');
        }
        
        function resetUI() {
            document.querySelectorAll('.step').forEach(function(el) {
                el.classList.remove('running', 'completed', 'error');
                el.querySelector('.step-error').textContent = '';
            });
            document.getElementById('resultPanel').classList.remove('show');
            document.getElementById('errorPanel').classList.remove('show');
            log('工作流已重置', 'success');
        }
        
        function showError(message, details) {
            const panel = document.getElementById('errorPanel');
            document.getElementById('errorMessage').textContent = message;
            document.getElementById('errorDetails').textContent = details || '';
            panel.classList.add('show');
            log('错误: ' + message, 'error');
        }
        
        function updateMcpStatus(status) {
            const dot = document.getElementById('statusDot');
            const text = document.getElementById('statusText');
            
            const allOk = Object.values(status).every(function(s) { return s.ok; });
            dot.classList.remove('ok', 'error');
            dot.classList.add(allOk ? 'ok' : 'error');
            
            const msgs = [];
            if (status.workflow) msgs.push('工作流: ' + (status.workflow.ok ? '✅' : '❌'));
            if (status.datasource) msgs.push('数据源: ' + (status.datasource.ok ? '✅' : '❌'));
            text.textContent = msgs.join(' | ') || '未知';
            
            log('MCP状态: ' + (allOk ? '全部正常' : '部分异常'), allOk ? 'success' : 'error');
        }
        
        // 初始化日志
        log('工作流面板已加载');
    </script>
</body>
</html>`;
    }

    public dispose() {
        WorkflowPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }
}
