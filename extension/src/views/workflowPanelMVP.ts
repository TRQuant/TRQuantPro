/**
 * 9步投资工作流面板 - MVP版本
 * ===========================
 * 
 * 最小可用版本，用于验证消息通信
 * 
 * 功能:
 * 1. 基础面板显示
 * 2. 9步工作流按钮
 * 3. MCP调用
 * 4. 结果显示
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn } from 'child_process';

// 9步工作流定义
const WORKFLOW_STEPS = [
    { id: 'data_source', name: '信息获取', desc: '数据源健康检查' },
    { id: 'market_trend', name: '市场趋势', desc: '市场状态分析' },
    { id: 'mainline', name: '投资主线', desc: '主线识别' },
    { id: 'candidate_pool', name: '候选池', desc: '候选股筛选' },
    { id: 'factor', name: '因子构建', desc: '因子推荐' },
    { id: 'strategy', name: '策略生成', desc: '策略模板生成' },
    { id: 'backtest', name: '回测验证', desc: '策略回测' },
    { id: 'optimization', name: '策略优化', desc: '参数优化' },
    { id: 'report', name: '报告生成', desc: '生成报告' }
];

export class WorkflowPanelMVP {
    public static currentPanel: WorkflowPanelMVP | undefined;
    
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionPath: string;
    private _disposables: vscode.Disposable[] = [];
    private _workflowId: string | null = null;
    private _stepResults: Map<string, any> = new Map();
    
    private constructor(panel: vscode.WebviewPanel, extensionPath: string) {
        this._panel = panel;
        this._extensionPath = extensionPath;
        
        // 设置HTML内容
        this._panel.webview.html = this._getHtmlContent();
        
        // 监听消息
        this._panel.webview.onDidReceiveMessage(
            message => this._handleMessage(message),
            null,
            this._disposables
        );
        
        // 面板关闭时清理
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        
        // 输出调试信息
        console.log('[WorkflowPanelMVP] 面板已创建');
    }
    
    public static createOrShow(extensionUri: vscode.Uri, extensionPath?: string): WorkflowPanelMVP {
        const column = vscode.ViewColumn.One;
        
        // 如果已存在，显示它
        if (WorkflowPanelMVP.currentPanel) {
            WorkflowPanelMVP.currentPanel._panel.reveal(column);
            return WorkflowPanelMVP.currentPanel;
        }
        
        // 确定extensionPath
        const resolvedPath = extensionPath || extensionUri.fsPath;
        
        // 创建新面板
        const panel = vscode.window.createWebviewPanel(
            'trquantWorkflowMVP',
            'TRQuant 工作流 (MVP)',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );
        
        WorkflowPanelMVP.currentPanel = new WorkflowPanelMVP(panel, resolvedPath);
        return WorkflowPanelMVP.currentPanel;
    }
    
    public dispose(): void {
        WorkflowPanelMVP.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }
    
    // 获取Python路径
    private _getPythonPath(): string {
        const projectRoot = this._getProjectRoot();
        const venvPython = path.join(projectRoot, 'venv', 'bin', 'python3');
        if (fs.existsSync(venvPython)) {
            return venvPython;
        }
        return 'python3';
    }
    
    // 获取项目根目录 (强制使用主项目路径)
    private _getProjectRoot(): string {
        // 优先使用环境变量
        if (process.env.TRQUANT_ROOT) {
            return process.env.TRQUANT_ROOT;
        }
        // 硬编码主项目路径
        const mainPath = '/home/taotao/dev/QuantTest/TRQuant';
        if (fs.existsSync(mainPath)) {
            return mainPath;
        }
        // 回退到extension路径推断
        return path.dirname(path.dirname(this._extensionPath));
    }
    
    // 调用MCP
    private async _callMCP(toolName: string, args: Record<string, unknown>): Promise<any> {
        const pythonPath = this._getPythonPath();
        const projectRoot = this._getProjectRoot();
        const bridgePath = path.join(projectRoot, 'extension', 'python', 'bridge.py');
        
        console.log(`[WorkflowPanelMVP] 调用MCP: ${toolName}`);
        
        return new Promise((resolve, reject) => {
            const proc = spawn(pythonPath, [bridgePath], {
                cwd: projectRoot,
                env: { ...process.env, PYTHONPATH: projectRoot }
            });
            
            let stdout = '';
            let stderr = '';
            
            proc.stdout.on('data', (data) => { stdout += data.toString(); });
            proc.stderr.on('data', (data) => { stderr += data.toString(); });
            
            proc.on('close', (code) => {
                if (code === 0) {
                    try {
                        // 提取最后一行JSON
                        const lines = stdout.trim().split('\n');
                        const lastLine = lines[lines.length - 1];
                        const result = JSON.parse(lastLine);
                        resolve(result);
                    } catch (e) {
                        reject(new Error(`解析失败: ${stdout}`));
                    }
                } else {
                    reject(new Error(`进程退出: ${code}, stderr: ${stderr}`));
                }
            });
            
            const request = {
                action: 'call_mcp_tool',
                params: {
                    tool_name: toolName,
                    arguments: args,
                    trace_id: `mvp_${Date.now()}`
                }
            };
            
            proc.stdin.write(JSON.stringify(request));
            proc.stdin.end();
        });
    }
    
    // 处理Webview消息
    private async _handleMessage(message: any): Promise<void> {
        console.log(`[WorkflowPanelMVP] 收到消息: ${message.command}`);
        
        switch (message.command) {
            case 'init':
                await this._initWorkflow();
                break;
            case 'runStep':
                await this._runStep(message.stepId);
                break;
            case 'runAll':
                await this._runAllSteps();
                break;
            case 'reset':
                this._resetWorkflow();
                break;
            case 'ping':
                // 用于验证通信
                this._postMessage({ command: 'pong', timestamp: Date.now() });
                break;
        }
    }
    
    // 初始化工作流
    private async _initWorkflow(): Promise<void> {
        try {
            const result = await this._callMCP('workflow9.create', { name: 'MVP工作流' });
            if (result.ok && result.data?.workflow_id) {
                this._workflowId = result.data.workflow_id;
                this._postMessage({
                    command: 'initialized',
                    workflowId: this._workflowId,
                    steps: WORKFLOW_STEPS
                });
                vscode.window.showInformationMessage(`工作流已创建: ${this._workflowId}`);
            } else {
                throw new Error(result.data?.error || '创建失败');
            }
        } catch (e: any) {
            this._postMessage({ command: 'error', message: e.message });
            vscode.window.showErrorMessage(`初始化失败: ${e.message}`);
        }
    }
    
    // 执行单个步骤
    private async _runStep(stepId: string): Promise<void> {
        if (!this._workflowId) {
            await this._initWorkflow();
        }
        
        this._postMessage({ command: 'stepStarted', stepId });
        
        try {
            const result = await this._callMCP('workflow9.run_step', {
                workflow_id: this._workflowId,
                step_id: stepId
            });
            
            if (result.ok && result.data?.success) {
                this._stepResults.set(stepId, result.data.step_result);
                this._postMessage({
                    command: 'stepCompleted',
                    stepId,
                    result: result.data.step_result
                });
            } else {
                throw new Error(result.data?.error || '执行失败');
            }
        } catch (e: any) {
            this._postMessage({
                command: 'stepFailed',
                stepId,
                error: e.message
            });
        }
    }
    
    // 执行所有步骤
    private async _runAllSteps(): Promise<void> {
        if (!this._workflowId) {
            await this._initWorkflow();
        }
        
        this._postMessage({ command: 'allStarted' });
        
        for (const step of WORKFLOW_STEPS) {
            await this._runStep(step.id);
        }
        
        this._postMessage({ command: 'allCompleted' });
    }
    
    // 重置工作流
    private _resetWorkflow(): void {
        this._workflowId = null;
        this._stepResults.clear();
        this._postMessage({ command: 'reset' });
    }
    
    // 发送消息到Webview
    private _postMessage(message: any): void {
        this._panel.webview.postMessage(message);
    }
    
    // 生成HTML内容 - 最简化版本
    private _getHtmlContent(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TRQuant 工作流 MVP</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #1e1e2e;
            color: #cdd6f4;
            padding: 20px;
            min-height: 100vh;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #45475a;
        }
        .header h1 {
            color: #89b4fa;
            font-size: 24px;
            margin-bottom: 10px;
        }
        .header .status {
            color: #a6adc8;
            font-size: 14px;
        }
        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 30px;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
        }
        .btn-primary {
            background: #89b4fa;
            color: #1e1e2e;
        }
        .btn-primary:hover { background: #b4befe; }
        .btn-secondary {
            background: #45475a;
            color: #cdd6f4;
        }
        .btn-secondary:hover { background: #585b70; }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .steps {
            display: grid;
            gap: 15px;
            max-width: 800px;
            margin: 0 auto;
        }
        .step {
            background: #313244;
            border-radius: 12px;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.2s;
        }
        .step:hover { background: #45475a; }
        .step-num {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #45475a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #cdd6f4;
        }
        .step.completed .step-num {
            background: #a6e3a1;
            color: #1e1e2e;
        }
        .step.running .step-num {
            background: #f9e2af;
            color: #1e1e2e;
            animation: pulse 1s infinite;
        }
        .step.failed .step-num {
            background: #f38ba8;
            color: #1e1e2e;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .step-info {
            flex: 1;
        }
        .step-name {
            font-weight: 600;
            color: #cdd6f4;
            margin-bottom: 4px;
        }
        .step-desc {
            font-size: 12px;
            color: #a6adc8;
        }
        .step-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            background: #89b4fa;
            color: #1e1e2e;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
        }
        .step-btn:hover { background: #b4befe; }
        .step-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .result-box {
            margin-top: 10px;
            padding: 10px;
            background: #1e1e2e;
            border-radius: 8px;
            font-size: 12px;
            color: #a6adc8;
            max-height: 150px;
            overflow: auto;
            display: none;
        }
        .step.completed .result-box,
        .step.failed .result-box {
            display: block;
        }
        .log {
            margin-top: 30px;
            padding: 20px;
            background: #313244;
            border-radius: 12px;
            max-height: 200px;
            overflow: auto;
        }
        .log h3 {
            color: #89b4fa;
            margin-bottom: 10px;
            font-size: 14px;
        }
        .log-entry {
            font-size: 12px;
            color: #a6adc8;
            margin-bottom: 5px;
            font-family: monospace;
        }
        .log-entry.success { color: #a6e3a1; }
        .log-entry.error { color: #f38ba8; }
        .log-entry.info { color: #89b4fa; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 TRQuant 9步投资工作流</h1>
        <div class="status" id="status">点击"初始化"开始</div>
    </div>
    
    <div class="controls">
        <button class="btn btn-primary" id="btn-init" onclick="init()">🚀 初始化</button>
        <button class="btn btn-primary" id="btn-run-all" onclick="runAll()" disabled>▶️ 执行全部</button>
        <button class="btn btn-secondary" id="btn-reset" onclick="reset()">🔄 重置</button>
        <button class="btn btn-secondary" onclick="ping()">🔔 测试连接</button>
    </div>
    
    <div class="steps" id="steps">
        ${WORKFLOW_STEPS.map((step, i) => `
        <div class="step" id="step-${step.id}">
            <div class="step-num">${i + 1}</div>
            <div class="step-info">
                <div class="step-name">${step.name}</div>
                <div class="step-desc">${step.desc}</div>
            </div>
            <button class="step-btn" onclick="runStep('${step.id}')" disabled>执行</button>
            <div class="result-box" id="result-${step.id}"></div>
        </div>
        `).join('')}
    </div>
    
    <div class="log">
        <h3>📝 日志</h3>
        <div id="log-content"></div>
    </div>
    
    <script>
        // 获取VS Code API
        const vscode = acquireVsCodeApi();
        
        // 日志函数
        function log(msg, type = 'info') {
            const logDiv = document.getElementById('log-content');
            const entry = document.createElement('div');
            entry.className = 'log-entry ' + type;
            entry.textContent = new Date().toLocaleTimeString() + ' - ' + msg;
            logDiv.insertBefore(entry, logDiv.firstChild);
            console.log('[MVP]', msg);
        }
        
        // 更新状态
        function setStatus(text) {
            document.getElementById('status').textContent = text;
        }
        
        // 启用/禁用按钮
        function setButtonsEnabled(enabled) {
            document.querySelectorAll('.step-btn').forEach(btn => btn.disabled = !enabled);
            document.getElementById('btn-run-all').disabled = !enabled;
        }
        
        // 初始化
        function init() {
            log('发送初始化请求...', 'info');
            vscode.postMessage({ command: 'init' });
        }
        
        // 执行步骤
        function runStep(stepId) {
            log('执行步骤: ' + stepId, 'info');
            vscode.postMessage({ command: 'runStep', stepId: stepId });
        }
        
        // 执行全部
        function runAll() {
            log('执行全部步骤...', 'info');
            vscode.postMessage({ command: 'runAll' });
        }
        
        // 重置
        function reset() {
            log('重置工作流', 'info');
            vscode.postMessage({ command: 'reset' });
            document.querySelectorAll('.step').forEach(el => {
                el.className = 'step';
                el.querySelector('.result-box').style.display = 'none';
                el.querySelector('.result-box').textContent = '';
            });
            setStatus('已重置，点击"初始化"开始');
            setButtonsEnabled(false);
        }
        
        // 测试连接
        function ping() {
            log('发送ping...', 'info');
            vscode.postMessage({ command: 'ping' });
        }
        
        // 监听来自Extension的消息
        window.addEventListener('message', event => {
            const message = event.data;
            log('收到: ' + message.command, 'info');
            
            switch (message.command) {
                case 'initialized':
                    setStatus('工作流已初始化: ' + message.workflowId);
                    setButtonsEnabled(true);
                    log('初始化成功: ' + message.workflowId, 'success');
                    break;
                    
                case 'stepStarted':
                    const startEl = document.getElementById('step-' + message.stepId);
                    if (startEl) {
                        startEl.className = 'step running';
                    }
                    setStatus('正在执行: ' + message.stepId);
                    break;
                    
                case 'stepCompleted':
                    const completeEl = document.getElementById('step-' + message.stepId);
                    if (completeEl) {
                        completeEl.className = 'step completed';
                        const resultBox = completeEl.querySelector('.result-box');
                        resultBox.style.display = 'block';
                        resultBox.textContent = JSON.stringify(message.result, null, 2);
                    }
                    log(message.stepId + ' 完成', 'success');
                    setStatus(message.stepId + ' 已完成');
                    break;
                    
                case 'stepFailed':
                    const failEl = document.getElementById('step-' + message.stepId);
                    if (failEl) {
                        failEl.className = 'step failed';
                        const resultBox = failEl.querySelector('.result-box');
                        resultBox.style.display = 'block';
                        resultBox.textContent = '错误: ' + message.error;
                    }
                    log(message.stepId + ' 失败: ' + message.error, 'error');
                    setStatus(message.stepId + ' 执行失败');
                    break;
                    
                case 'allStarted':
                    setStatus('开始执行全部步骤...');
                    break;
                    
                case 'allCompleted':
                    setStatus('全部步骤已完成');
                    log('全部完成', 'success');
                    break;
                    
                case 'reset':
                    setStatus('已重置');
                    setButtonsEnabled(false);
                    break;
                    
                case 'pong':
                    log('连接正常! timestamp=' + message.timestamp, 'success');
                    break;
                    
                case 'error':
                    log('错误: ' + message.message, 'error');
                    setStatus('错误: ' + message.message);
                    break;
            }
        });
        
        // 页面加载完成
        log('MVP面板已加载', 'success');
    </script>
</body>
</html>`;
    }
}
