/**
 * 9步骤投资工作流面板
 * ====================
 * 
 * 完整的9步投资工作流面板
 * - 正确的Python解释器路径 (extension/venv)
 * - 统一的MCP服务器调用 (workflow9.*)
 * - 优化的结果可视化
 * 
 * 步骤：信息获取 → 市场趋势 → 投资主线 → 候选池构建 → 因子构建 → 策略生成 → 回测验证 → 策略优化 → 报告生成
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as cp from 'child_process';
import { logger } from '../utils/logger';
import { ConfigManager } from '../utils/config';

const MODULE = 'WorkflowPanel';

// ==================== 类型定义 ====================

interface WorkflowStep {
    id: string;
    name: string;
    icon: string;
    color: string;
    description: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    result?: unknown;
    duration?: number;
}

interface WorkflowState {
    workflowId: string | null;
    steps: WorkflowStep[];
    context: Record<string, unknown>;
    isRunning: boolean;
}

// 9步工作流定义
const WORKFLOW_9STEPS: Omit<WorkflowStep, 'status' | 'result'>[] = [
    { id: 'data_source', name: '信息获取', icon: '📡', color: '#58a6ff', description: '检查数据源连接状态' },
    { id: 'market_trend', name: '市场趋势', icon: '📈', color: '#667eea', description: '分析市场状态和风格轮动' },
    { id: 'mainline', name: '投资主线', icon: '🔥', color: '#F59E0B', description: '识别热点主线和板块' },
    { id: 'candidate_pool', name: '候选池构建', icon: '📦', color: '#a371f7', description: '构建候选股票池' },
    { id: 'factor', name: '因子构建', icon: '🧮', color: '#3fb950', description: '推荐量化因子组合' },
    { id: 'strategy', name: '策略生成', icon: '💻', color: '#d29922', description: '生成策略代码' },
    { id: 'backtest', name: '回测验证', icon: '🔄', color: '#1E3A5F', description: '执行策略回测' },
    { id: 'optimization', name: '策略优化', icon: '⚙️', color: '#7C3AED', description: '参数优化' },
    { id: 'report', name: '报告生成', icon: '📄', color: '#EC4899', description: '生成研究报告' }
];

// ==================== 主面板类 ====================

export class WorkflowPanel {
    public static currentPanel: WorkflowPanel | undefined;
    
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _extensionPath: string;
    private _disposables: vscode.Disposable[] = [];
    
    // 工作流状态
    private _state: WorkflowState = {
        workflowId: null,
        steps: WORKFLOW_9STEPS.map(s => ({ ...s, status: 'pending' as const })),
        context: {},
        isRunning: false
    };

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        extensionPath: string
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._extensionPath = extensionPath;

        this._panel.webview.html = this._getHtmlContent();
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        this._panel.webview.onDidReceiveMessage(
            message => this._handleMessage(message),
            null,
            this._disposables
        );
        
        logger.info('WorkflowPanel 创建完成', MODULE);
    }

    /**
     * 创建或显示面板
     */
    public static createOrShow(extensionUri: vscode.Uri, extensionPath?: string): WorkflowPanel {
        const column = vscode.ViewColumn.One;

        if (WorkflowPanel.currentPanel) {
            WorkflowPanel.currentPanel._panel.reveal(column);
            return WorkflowPanel.currentPanel;
        }

        // 确定扩展路径
        let extPath = extensionPath;
        if (!extPath) {
            // 尝试从工作区获取
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (workspaceFolders && workspaceFolders.length > 0) {
                const wsPath = workspaceFolders[0].uri.fsPath;
                const potentialExtPath = path.join(wsPath, 'extension');
                if (fs.existsSync(potentialExtPath)) {
                    extPath = potentialExtPath;
                }
            }
            
            // 回退到extensionUri
            if (!extPath) {
                extPath = extensionUri.fsPath;
            }
        }

        logger.info(`创建WorkflowPanel, extensionPath: ${extPath}`, MODULE);

        const panel = vscode.window.createWebviewPanel(
            'trquantWorkflowV3',
            '🐉 韬睿量化 - 9步投资工作流',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        WorkflowPanel.currentPanel = new WorkflowPanel(panel, extensionUri, extPath);
        return WorkflowPanel.currentPanel;
    }

    public dispose(): void {
        WorkflowPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }

    // ==================== Python路径解析 ====================

    /**
     * 获取正确的Python解释器路径
     * 使用ConfigManager统一管理，确保与整个扩展一致
     */
    private _getPythonPath(): string {
        const configManager = ConfigManager.getInstance();
        const pythonPath = configManager.getPythonPath(this._extensionPath);
        logger.debug(`获取Python路径: ${pythonPath}`, MODULE);
        return pythonPath;
    }

    /**
     * 获取项目根目录
     */
    private _getProjectRoot(): string {
        // 0. 硬编码的TRQuant项目路径（最可靠）
        const hardcodedRoot = '/home/taotao/dev/QuantTest/TRQuant';
        if (fs.existsSync(hardcodedRoot)) {
            return hardcodedRoot;
        }
        
        // 1. 工作区路径
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (workspaceFolders && workspaceFolders.length > 0) {
            return workspaceFolders[0].uri.fsPath;
        }
        
        // 2. 从extensionPath推断
        if (this._extensionPath.endsWith('extension')) {
            return path.dirname(this._extensionPath);
        }
        
        // 3. 环境变量
        return process.env.TRQUANT_ROOT || this._extensionPath;
    }

    // ==================== MCP调用 ====================

    /**
     * 调用9步工作流MCP服务器
     */
    private async _callMCP(toolName: string, args: Record<string, unknown>): Promise<unknown> {
        const pythonPath = this._getPythonPath();
        const projectRoot = this._getProjectRoot();
        const serverPath = path.join(projectRoot, 'mcp_servers', 'workflow_9steps_server.py');
        
        logger.info(`调用MCP: ${toolName}`, MODULE, { pythonPath, serverPath });
        
        // 检查服务器文件是否存在
        if (!fs.existsSync(serverPath)) {
            throw new Error(`MCP服务器文件不存在: ${serverPath}`);
        }
        
        // 通过bridge.py调用
        const bridgePath = path.join(projectRoot, 'extension', 'python', 'bridge.py');
        
        return new Promise((resolve, reject) => {
            const request = {
                action: 'call_mcp_tool',
                params: {
                    tool_name: toolName,
                    arguments: args,
                    trace_id: `wf3_${Date.now()}`
                }
            };
            
            const env = {
                ...process.env,
                PYTHONIOENCODING: 'utf-8',
                TRQUANT_ROOT: projectRoot,
                PYTHONPATH: [
                    path.join(projectRoot, 'extension', 'python'),
                    path.join(projectRoot, 'mcp_servers'),
                    projectRoot
                ].join(path.delimiter)
            };
            
            const proc = cp.spawn(pythonPath, [bridgePath], {
                cwd: projectRoot,
                env,
                stdio: ['pipe', 'pipe', 'pipe']
            });
            
            let stdout = '';
            let stderr = '';
            
            // 写入请求
            proc.stdin.write(JSON.stringify(request));
            proc.stdin.end();
            
            proc.stdout.on('data', (data) => { stdout += data.toString(); });
            proc.stderr.on('data', (data) => { stderr += data.toString(); });
            
            proc.on('close', (code) => {
                if (code !== 0) {
                    logger.error(`MCP调用失败: ${stderr}`, MODULE);
                    reject(new Error(stderr || `进程退出码: ${code}`));
                    return;
                }
                
                try {
                    const result = JSON.parse(stdout.trim());
                    if (result.ok) {
                        resolve(result.data);
                    } else {
                        reject(new Error(result.error || '调用失败'));
                    }
                } catch (e) {
                    // 尝试解析最后一行
                    const lines = stdout.trim().split('\n');
                    for (let i = lines.length - 1; i >= 0; i--) {
                        try {
                            const parsed = JSON.parse(lines[i]);
                            if (parsed.ok) {
                                resolve(parsed.data);
                                return;
                            }
                        } catch {}
                    }
                    reject(new Error(`解析响应失败: ${stdout.slice(0, 200)}`));
                }
            });
            
            // 发送请求
            proc.stdin.write(JSON.stringify(request));
            proc.stdin.end();
            
            // 超时
            setTimeout(() => {
                proc.kill();
                reject(new Error('MCP调用超时 (60s)'));
            }, 60000);
        });
    }

    /**
     * 直接执行步骤（不通过MCP服务器，直接调用Python脚本）
     */
    private async _executeStepDirect(stepId: string, args: Record<string, unknown>): Promise<unknown> {
        const pythonPath = this._getPythonPath();
        const projectRoot = this._getProjectRoot();
        const bridgePath = path.join(projectRoot, 'extension', 'python', 'bridge.py');
        
        logger.info(`直接执行步骤: ${stepId}`, MODULE, { pythonPath });
        
        return new Promise((resolve, reject) => {
            const request = {
                action: 'run_workflow_step',
                params: {
                    step_id: stepId,
                    args: args
                }
            };
            
            const env = {
                ...process.env,
                PYTHONIOENCODING: 'utf-8',
                TRQUANT_ROOT: projectRoot,
                PYTHONPATH: [
                    path.join(projectRoot, 'extension', 'python'),
                    path.join(projectRoot, 'mcp_servers'),
                    projectRoot
                ].join(path.delimiter)
            };
            
            const proc = cp.spawn(pythonPath, [bridgePath], {
                cwd: projectRoot,
                env,
                stdio: ['pipe', 'pipe', 'pipe']
            });
            
            let stdout = '';
            let stderr = '';
            
            // 写入请求
            proc.stdin.write(JSON.stringify(request));
            proc.stdin.end();
            
            proc.stdout.on('data', (data) => { stdout += data.toString(); });
            proc.stderr.on('data', (data) => { stderr += data.toString(); });
            
            proc.on('close', (code) => {
                if (code !== 0) {
                    logger.error(`步骤执行失败: ${stderr}`, MODULE);
                    reject(new Error(stderr || `进程退出码: ${code}`));
                    return;
                }
                
                try {
                    const response = JSON.parse(stdout.trim());
                    if (response.ok) {
                        resolve(response.data);
                    } else {
                        reject(new Error(response.error || '步骤执行失败'));
                    }
                } catch (e) {
                    logger.error(`解析失败: ${stdout.slice(0, 500)}`, MODULE);
                    reject(new Error(`解析失败: ${e}`));
                }
            });
            
            // 超时
            setTimeout(() => {
                proc.kill();
                reject(new Error('执行超时 (60s)'));
            }, 60000);
        });
    }

    // ==================== 消息处理 ====================

    private async _handleMessage(message: any): Promise<void> {
        logger.info(`收到消息: ${message.command}`, MODULE);

        switch (message.command) {
            case 'init':
                await this._initWorkflow();
                break;
            case 'runStep':
                await this._runStep(message.stepId, message.args);
                break;
            case 'runAll':
                await this._runAllSteps();
                break;
            case 'reset':
                this._resetWorkflow();
                break;
            case 'openReport':
                this._openReport(message.filePath);
                break;
        }
    }

    /**
     * 初始化工作流
     */
    private async _initWorkflow(): Promise<void> {
        try {
            // 通过MCP server创建工作流
            const result = await this._callMCP('workflow9.create', {
                name: '9步投资工作流'
            }) as { success: boolean; workflow_id?: string; error?: string };
            
            if (result.success && result.workflow_id) {
                this._state.workflowId = result.workflow_id;
            } else {
                // 如果MCP调用失败，使用本地生成ID
                this._state.workflowId = `wf_${Date.now().toString(36)}`;
                logger.warn(`MCP创建工作流失败，使用本地ID: ${this._state.workflowId}`, MODULE);
            }
            
            this._state.context = {};
            this._state.steps = WORKFLOW_9STEPS.map(s => ({ ...s, status: 'pending' as const }));
            
            this._postMessage({
                command: 'initialized',
                workflowId: this._state.workflowId,
                steps: this._state.steps,
                pythonPath: this._getPythonPath()
            });
            
            logger.info(`工作流初始化: ${this._state.workflowId}`, MODULE);
        } catch (error: any) {
            logger.error(`初始化失败: ${error.message}`, MODULE);
            // 即使MCP失败，也使用本地ID继续
            this._state.workflowId = `wf_${Date.now().toString(36)}`;
            this._state.steps = WORKFLOW_9STEPS.map(s => ({ ...s, status: 'pending' as const }));
            this._postMessage({
                command: 'initialized',
                workflowId: this._state.workflowId,
                steps: this._state.steps,
                pythonPath: this._getPythonPath()
            });
        }
    }

    /**
     * 执行单个步骤
     */
    private async _runStep(stepId: string, args: Record<string, unknown> = {}): Promise<void> {
        if (this._state.isRunning) {
            vscode.window.showWarningMessage('工作流正在执行中');
            return;
        }

        const stepIndex = this._state.steps.findIndex(s => s.id === stepId);
        if (stepIndex === -1) {
            vscode.window.showErrorMessage(`未知步骤: ${stepId}`);
            return;
        }

        const step = this._state.steps[stepIndex];
        this._state.isRunning = true;
        
        // 更新状态
        step.status = 'running';
        this._postMessage({ command: 'stepStarted', stepId, stepIndex });

        const startTime = Date.now();
        
        try {
            // 直接调用对应的MCP服务器执行步骤
            const result = await this._executeStepDirect(stepId, args) as { 
                success: boolean; 
                summary?: string;
                error?: string;
                [key: string]: unknown;
            };
            
            const duration = Date.now() - startTime;
            
            if (result.success) {
                step.status = 'completed';
                step.result = result;
                step.duration = duration;
                
                // 保存到上下文
                this._state.context[stepId] = result;
                
                this._postMessage({
                    command: 'stepCompleted',
                    stepId,
                    stepIndex,
                    result: result,
                    summary: result.summary || '步骤完成',
                    duration
                });
                
                logger.info(`步骤完成: ${step.name}, 耗时: ${duration}ms`, MODULE);
            } else {
                throw new Error(result.error || '步骤执行失败');
            }

        } catch (error: any) {
            step.status = 'failed';
            step.result = { error: error.message };
            step.duration = Date.now() - startTime;
            
            this._postMessage({
                command: 'stepFailed',
                stepId,
                stepIndex,
                error: error.message
            });
            
            logger.error(`步骤失败: ${step.name} - ${error.message}`, MODULE);
            vscode.window.showErrorMessage(`步骤 ${step.name} 执行失败: ${error.message}`);
        }

        this._state.isRunning = false;
    }

    /**
     * 执行所有步骤
     */
    private async _runAllSteps(): Promise<void> {
        if (this._state.isRunning) {
            vscode.window.showWarningMessage('工作流正在执行中');
            return;
        }

        if (!this._state.workflowId) {
            await this._initWorkflow();
        }

        this._postMessage({ command: 'workflowStarted', totalSteps: 9 });

        try {
            // 使用MCP server的一键执行功能
            const result = await this._callMCP('workflow9.run_all', {
                workflow_id: this._state.workflowId
            }) as { success: boolean; steps?: unknown[]; context?: Record<string, unknown>; error?: string };
            
            if (result.success) {
                // 更新所有步骤状态
                if (result.steps) {
                    this._state.steps = result.steps as WorkflowStep[];
                }
                if (result.context) {
                    this._state.context = result.context;
                }
                
                this._postMessage({ 
                    command: 'workflowCompleted', 
                    context: this._state.context,
                    steps: this._state.steps
                });
                
                logger.info('所有步骤执行完成', MODULE);
            } else {
                throw new Error(result.error || '工作流执行失败');
            }
        } catch (error: any) {
            logger.error(`一键执行失败，回退到逐步执行: ${error.message}`, MODULE);
            
            // 回退到逐步执行
            for (let i = 0; i < this._state.steps.length; i++) {
                const step = this._state.steps[i];
                await this._runStep(step.id);

                // 检查是否失败
                if (step.status === 'failed') {
                    const proceed = await vscode.window.showWarningMessage(
                        `步骤 ${step.name} 失败，是否继续？`,
                        '继续', '停止'
                    );
                    if (proceed !== '继续') {
                        break;
                    }
                }
            }

            this._postMessage({ 
                command: 'workflowCompleted', 
                context: this._state.context,
                steps: this._state.steps
            });
        }
    }

    /**
     * 重置工作流
     */
    private _resetWorkflow(): void {
        this._state.workflowId = null;
        this._state.context = {};
        this._state.steps = WORKFLOW_9STEPS.map(s => ({ ...s, status: 'pending' as const }));
        this._state.isRunning = false;
        
        this._postMessage({ command: 'reset' });
    }

    /**
     * 打开报告文件
     */
    private _openReport(filePath: string): void {
        if (filePath && fs.existsSync(filePath)) {
            vscode.env.openExternal(vscode.Uri.file(filePath));
        } else {
            vscode.window.showErrorMessage('报告文件不存在');
        }
    }

    private _postMessage(message: any): void {
        this._panel.webview.postMessage(message);
    }

    // ==================== HTML内容 ====================

    private _getHtmlContent(): string {
        const stepsHtml = WORKFLOW_9STEPS.map((step, index) => `
            <div class="step-card" id="step-${step.id}" data-step-id="${step.id}">
                <div class="step-header">
                    <div class="step-number" style="background: ${step.color};">${index + 1}</div>
                    <div class="step-icon">${step.icon}</div>
                    <div class="step-info">
                        <div class="step-name">${step.name}</div>
                        <div class="step-desc">${step.description}</div>
                    </div>
                    <div class="step-status" id="status-${step.id}">
                        <span class="status-badge pending">等待中</span>
                    </div>
                </div>
                <div class="step-actions">
                    <button class="btn btn-run" onclick="runStep('${step.id}')">
                        <span class="btn-icon">▶</span> 执行
                    </button>
                    <button class="btn btn-view" id="view-${step.id}" onclick="toggleResult('${step.id}')" disabled>
                        <span class="btn-icon">📊</span> 查看结果
                    </button>
                </div>
                <div class="step-result" id="result-${step.id}"></div>
            </div>
        `).join('');

        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <title>9步投资工作流</title>
    <style>
        :root {
            --bg-primary: #0a0e14;
            --bg-secondary: #0f141a;
            --bg-card: #151c24;
            --bg-hover: #1c2530;
            --border: #253040;
            --text: #e6edf3;
            --text-secondary: #7d8590;
            --accent: #2f81f7;
            --accent-light: #58a6ff;
            --success: #2ea043;
            --success-bg: rgba(46, 160, 67, 0.15);
            --warning: #d29922;
            --warning-bg: rgba(210, 153, 34, 0.15);
            --error: #f85149;
            --error-bg: rgba(248, 81, 73, 0.15);
            --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text);
            padding: 24px;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        /* 头部 */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding: 20px 24px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
        }
        
        .header-title {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .header-title h1 {
            font-size: 24px;
            font-weight: 600;
            background: linear-gradient(135deg, var(--accent-light), #a371f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .header-title .subtitle {
            font-size: 14px;
            color: var(--text-secondary);
        }
        
        .header-actions {
            display: flex;
            gap: 12px;
        }
        
        /* 按钮 */
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s ease;
        }
        
        .btn-icon { font-size: 12px; }
        
        .btn-primary {
            background: var(--accent);
            color: white;
        }
        
        .btn-primary:hover {
            background: var(--accent-light);
            transform: translateY(-1px);
        }
        
        .btn-secondary {
            background: var(--bg-hover);
            color: var(--text);
            border: 1px solid var(--border);
        }
        
        .btn-secondary:hover {
            background: var(--border);
        }
        
        .btn-run {
            background: var(--success);
            color: white;
            padding: 8px 16px;
            font-size: 13px;
        }
        
        .btn-run:hover {
            filter: brightness(1.1);
        }
        
        .btn-view {
            background: var(--bg-hover);
            color: var(--text-secondary);
            padding: 8px 16px;
            font-size: 13px;
            border: 1px solid var(--border);
        }
        
        .btn-view:not(:disabled):hover {
            background: var(--border);
            color: var(--text);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        /* 进度条 */
        .progress-container {
            margin-bottom: 24px;
        }
        
        .progress-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
            color: var(--text-secondary);
        }
        
        .progress-bar {
            height: 6px;
            background: var(--bg-hover);
            border-radius: 3px;
            overflow: hidden;
        }
        
        .progress-bar .progress {
            height: 100%;
            background: linear-gradient(90deg, var(--accent), var(--success));
            width: 0%;
            transition: width 0.5s ease;
            border-radius: 3px;
        }
        
        /* 步骤卡片 */
        .steps-container {
            display: grid;
            gap: 16px;
        }
        
        .step-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        
        .step-card:hover {
            border-color: var(--accent);
            box-shadow: 0 4px 20px rgba(47, 129, 247, 0.1);
        }
        
        .step-card.running {
            border-color: var(--accent);
            background: linear-gradient(135deg, rgba(47, 129, 247, 0.05) 0%, rgba(47, 129, 247, 0.02) 100%);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(47, 129, 247, 0.3); }
            50% { box-shadow: 0 0 20px 5px rgba(47, 129, 247, 0.2); }
        }
        
        .step-card.completed {
            border-color: var(--success);
            background: var(--success-bg);
        }
        
        .step-card.failed {
            border-color: var(--error);
            background: var(--error-bg);
        }
        
        .step-header {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .step-number {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 16px;
            color: white;
        }
        
        .step-icon {
            font-size: 28px;
        }
        
        .step-info {
            flex: 1;
        }
        
        .step-name {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 2px;
        }
        
        .step-desc {
            font-size: 13px;
            color: var(--text-secondary);
        }
        
        .step-status {
            min-width: 100px;
            text-align: right;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .status-badge.pending {
            background: var(--bg-hover);
            color: var(--text-secondary);
        }
        
        .status-badge.running {
            background: var(--accent);
            color: white;
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .status-badge.completed {
            background: var(--success);
            color: white;
        }
        
        .status-badge.failed {
            background: var(--error);
            color: white;
        }
        
        .step-actions {
            display: flex;
            gap: 8px;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
        }
        
        /* 结果展示 */
        .step-result {
            margin-top: 16px;
            display: none;
        }
        
        .step-result.visible {
            display: block;
        }
        
        .result-card {
            background: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
        }
        
        .result-header {
            padding: 12px 16px;
            background: var(--bg-hover);
            border-bottom: 1px solid var(--border);
            font-size: 13px;
            font-weight: 500;
            color: var(--text-secondary);
        }
        
        .result-content {
            padding: 16px;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .result-content pre {
            font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
            font-size: 12px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-break: break-all;
        }
        
        /* 指标卡片 */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .metric-item {
            background: var(--bg-hover);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 20px;
            font-weight: 700;
            color: var(--accent-light);
        }
        
        .metric-value.positive { color: var(--success); }
        .metric-value.negative { color: var(--error); }
        
        .metric-label {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 4px;
        }
        
        /* 上下文面板 */
        .context-panel {
            margin-top: 24px;
            padding: 20px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
        }
        
        .context-panel h3 {
            font-size: 16px;
            margin-bottom: 16px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .context-content {
            max-height: 300px;
            overflow-y: auto;
        }
        
        /* Python路径显示 */
        .python-info {
            margin-top: 24px;
            padding: 12px 16px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 12px;
            color: var(--text-secondary);
            font-family: monospace;
        }
        
        .python-info .label {
            color: var(--accent-light);
            margin-right: 8px;
        }
        
        /* 滚动条 */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">
            <div>
                <h1>🐉 韬睿量化 - 9步投资工作流</h1>
                <p class="subtitle">专业A股量化投资工具</p>
            </div>
        </div>
        <div class="header-actions">
            <button class="btn btn-primary" onclick="runAll()">
                <span class="btn-icon">🚀</span> 一键执行全部
            </button>
            <button class="btn btn-secondary" onclick="reset()">
                <span class="btn-icon">🔄</span> 重置
            </button>
        </div>
    </div>
    
    <div class="progress-container">
        <div class="progress-info">
            <span id="progress-text">准备就绪</span>
            <span id="progress-percent">0 / 9</span>
        </div>
        <div class="progress-bar">
            <div class="progress" id="progress"></div>
        </div>
    </div>
    
    <div class="steps-container">
        ${stepsHtml}
    </div>
    
    <div class="context-panel">
        <h3>📋 执行上下文</h3>
        <div class="context-content" id="context">
            <p style="color: var(--text-secondary);">执行步骤后，结果将显示在这里...</p>
        </div>
    </div>
    
    <div class="python-info" id="python-info">
        <span class="label">Python:</span>
        <span id="python-path">正在检测...</span>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        let completedSteps = 0;
        const totalSteps = 9;
        let workflowContext = {};
        
        // 初始化
        window.addEventListener('load', () => {
            vscode.postMessage({ command: 'init' });
        });
        
        function runStep(stepId) {
            vscode.postMessage({ command: 'runStep', stepId, args: {} });
        }
        
        function runAll() {
            vscode.postMessage({ command: 'runAll' });
        }
        
        function reset() {
            vscode.postMessage({ command: 'reset' });
            completedSteps = 0;
            workflowContext = {};
            updateProgress(0, '准备就绪');
            document.getElementById('context').innerHTML = '<p style="color: var(--text-secondary);">执行步骤后，结果将显示在这里...</p>';
            
            document.querySelectorAll('.step-card').forEach(card => {
                card.classList.remove('running', 'completed', 'failed');
            });
            document.querySelectorAll('[id^="status-"]').forEach(el => {
                el.innerHTML = '<span class="status-badge pending">等待中</span>';
            });
            document.querySelectorAll('[id^="result-"]').forEach(el => {
                el.innerHTML = '';
                el.classList.remove('visible');
            });
            document.querySelectorAll('[id^="view-"]').forEach(btn => {
                btn.disabled = true;
            });
        }
        
        function toggleResult(stepId) {
            const resultEl = document.getElementById('result-' + stepId);
            resultEl.classList.toggle('visible');
        }
        
        function updateProgress(count, text) {
            completedSteps = count;
            const percent = (count / totalSteps * 100);
            document.getElementById('progress').style.width = percent + '%';
            document.getElementById('progress-text').textContent = text;
            document.getElementById('progress-percent').textContent = count + ' / ' + totalSteps;
        }
        
        function formatValue(value) {
            if (typeof value === 'number') {
                if (Math.abs(value) < 1) {
                    return (value * 100).toFixed(2) + '%';
                }
                return value.toFixed(2);
            }
            return value;
        }
        
        function renderMetrics(result) {
            if (!result || !result.metrics) return '';
            
            const metrics = result.metrics;
            let html = '<div class="metrics-grid">';
            
            const metricDefs = [
                { key: 'total_return', label: '总收益', isPercent: true },
                { key: 'sharpe_ratio', label: '夏普比率' },
                { key: 'max_drawdown', label: '最大回撤', isPercent: true, isNegative: true },
                { key: 'win_rate', label: '胜率', isPercent: true },
                { key: 'total_trades', label: '交易次数' }
            ];
            
            metricDefs.forEach(def => {
                if (metrics[def.key] !== undefined) {
                    const value = metrics[def.key];
                    const displayValue = def.isPercent ? (value * 100).toFixed(2) + '%' : value.toFixed ? value.toFixed(2) : value;
                    const colorClass = def.isNegative ? 'negative' : (value > 0 ? 'positive' : '');
                    
                    html += '<div class="metric-item">';
                    html += '<div class="metric-value ' + colorClass + '">' + displayValue + '</div>';
                    html += '<div class="metric-label">' + def.label + '</div>';
                    html += '</div>';
                }
            });
            
            html += '</div>';
            return html;
        }
        
        function renderResultContent(stepId, result) {
            const chartId = 'chart-' + stepId + '-' + Date.now();
            let html = '<div class="result-card">';
            html += '<div class="result-header">' + (result.summary || '执行结果') + '</div>';
            html += '<div class="result-content">';
            
            // 市场趋势 - 雷达图
            if (stepId === 'market_trend') {
                html += '<div id="' + chartId + '" style="width:100%;height:300px;"></div>';
                html += '</div></div>';
                setTimeout(() => {
                    const chart = echarts.init(document.getElementById(chartId));
                    const short = result.short_term || result.indicators || {};
                    const medium = result.medium_term || {};
                    const long = result.long_term || {};
                    chart.setOption({
                        title: { text: '市场趋势分析', left: 'center', textStyle: { color: '#e6edf3' } },
                        backgroundColor: 'transparent',
                        radar: {
                            indicator: [
                                { name: '短期趋势', max: 100 },
                                { name: '中期趋势', max: 100 },
                                { name: '长期趋势', max: 100 },
                                { name: '动量', max: 100 },
                                { name: '波动率', max: 100 }
                            ],
                            axisLine: { lineStyle: { color: 'rgba(255,255,255,0.3)' } },
                            splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
                        },
                        series: [{
                            type: 'radar',
                            data: [{
                                value: [
                                    (short.score || 50) + 50,
                                    (medium.score || 50) + 50,
                                    (long.score || 50) + 50,
                                    Math.min(100, Math.abs(result.indicators?.momentum_20d || 0) * 5 + 50),
                                    100 - Math.min(100, (result.indicators?.volatility_annual || 20))
                                ],
                                name: '市场指标',
                                areaStyle: { color: 'rgba(47, 129, 247, 0.3)' },
                                lineStyle: { color: '#2f81f7' }
                            }]
                        }]
                    });
                }, 100);
                return html;
            }
            
            // 投资主线 - 柱状图
            if (stepId === 'mainline') {
                const mainlines = result.mainlines || [];
                html += '<div id="' + chartId + '" style="width:100%;height:300px;"></div>';
                html += '</div></div>';
                setTimeout(() => {
                    const chart = echarts.init(document.getElementById(chartId));
                    chart.setOption({
                        title: { text: '投资主线评分', left: 'center', textStyle: { color: '#e6edf3' } },
                        backgroundColor: 'transparent',
                        xAxis: {
                            type: 'category',
                            data: mainlines.slice(0, 8).map(m => m.name || ''),
                            axisLabel: { color: '#7d8590', rotate: 30 },
                            axisLine: { lineStyle: { color: '#253040' } }
                        },
                        yAxis: {
                            type: 'value',
                            max: 100,
                            axisLabel: { color: '#7d8590' },
                            splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
                        },
                        series: [{
                            type: 'bar',
                            data: mainlines.slice(0, 8).map((m, i) => ({
                                value: m.score || 0,
                                itemStyle: {
                                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                        { offset: 0, color: i < 3 ? '#f5576c' : '#667eea' },
                                        { offset: 1, color: i < 3 ? '#f093fb' : '#764ba2' }
                                    ])
                                }
                            })),
                            barWidth: '50%'
                        }]
                    });
                }, 100);
                return html;
            }
            
            // 回测结果 - 指标卡片 + 折线图
            if (stepId === 'backtest' || stepId === 'optimization') {
                html += renderMetrics(result);
                if (result.equity_curve || result.returns) {
                    html += '<div id="' + chartId + '" style="width:100%;height:250px;margin-top:16px;"></div>';
                    html += '</div></div>';
                    setTimeout(() => {
                        const chart = echarts.init(document.getElementById(chartId));
                        const curve = result.equity_curve || result.returns || [];
                        chart.setOption({
                            title: { text: '收益曲线', left: 'center', textStyle: { color: '#e6edf3', fontSize: 14 } },
                            backgroundColor: 'transparent',
                            xAxis: {
                                type: 'category',
                                data: curve.map((_, i) => 'D' + (i + 1)),
                                axisLabel: { color: '#7d8590' },
                                axisLine: { lineStyle: { color: '#253040' } }
                            },
                            yAxis: {
                                type: 'value',
                                axisLabel: { color: '#7d8590', formatter: '{value}%' },
                                splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
                            },
                            series: [{
                                type: 'line',
                                data: curve.map(v => (v * 100).toFixed(2)),
                                smooth: true,
                                areaStyle: { color: 'rgba(46, 160, 67, 0.2)' },
                                lineStyle: { color: '#2ea043', width: 2 }
                            }]
                        });
                    }, 100);
                    return html;
                }
            }
            
            // 五维评分 - 雷达图
            if (result.five_dimension || result.radar_data) {
                const dims = result.five_dimension || result.radar_data || {};
                html += '<div id="' + chartId + '" style="width:100%;height:280px;"></div>';
                const radarData = result.radar_data || {
                    '基本面': dims.fundamental || 0,
                    '技术面': dims.technical || 0,
                    '资金面': dims.capital || 0,
                    '消息面': dims.news || 0,
                    '行业地位': dims.position || 0
                };
                html += '</div></div>';
                setTimeout(() => {
                    const chart = echarts.init(document.getElementById(chartId));
                    const labels = Object.keys(radarData);
                    const values = Object.values(radarData);
                    chart.setOption({
                        title: { text: '五维评分', left: 'center', textStyle: { color: '#e6edf3' } },
                        backgroundColor: 'transparent',
                        radar: {
                            indicator: labels.map(l => ({ name: l, max: 20 })),
                            axisLine: { lineStyle: { color: 'rgba(255,255,255,0.3)' } },
                            splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
                        },
                        series: [{
                            type: 'radar',
                            data: [{
                                value: values,
                                name: '评分',
                                areaStyle: { color: 'rgba(245, 87, 108, 0.3)' },
                                lineStyle: { color: '#f5576c' }
                            }]
                        }]
                    });
                }, 100);
                return html;
            }
            
            // 通用JSON展示
            html += '<pre style="max-height:400px;overflow:auto;">' + JSON.stringify(result, null, 2) + '</pre>';
            
            html += '</div></div>';
            return html;
        }
        
        // 消息处理
        window.addEventListener('message', event => {
            const message = event.data;
            
            switch (message.command) {
                case 'initialized': {
                    document.getElementById('python-path').textContent = message.pythonPath;
                    break;
                }
                
                case 'stepStarted': {
                    const card = document.getElementById('step-' + message.stepId);
                    const status = document.getElementById('status-' + message.stepId);
                    
                    card.classList.remove('completed', 'failed');
                    card.classList.add('running');
                    status.innerHTML = '<span class="status-badge running">执行中...</span>';
                    updateProgress(completedSteps, '正在执行: ' + STEP_NAMES[message.stepId]);
                    break;
                }
                
                case 'stepCompleted': {
                    const card = document.getElementById('step-' + message.stepId);
                    const status = document.getElementById('status-' + message.stepId);
                    const result = document.getElementById('result-' + message.stepId);
                    const viewBtn = document.getElementById('view-' + message.stepId);
                    
                    card.classList.remove('running');
                    card.classList.add('completed');
                    
                    const duration = (message.duration / 1000).toFixed(1);
                    status.innerHTML = '<span class="status-badge completed">✅ 完成 (' + duration + 's)</span>';
                    
                    result.innerHTML = renderResultContent(message.stepId, message.result);
                    viewBtn.disabled = false;
                    
                    completedSteps++;
                    workflowContext[message.stepId] = message.result;
                    updateProgress(completedSteps, '完成: ' + STEP_NAMES[message.stepId]);
                    break;
                }
                
                case 'stepFailed': {
                    const card = document.getElementById('step-' + message.stepId);
                    const status = document.getElementById('status-' + message.stepId);
                    const result = document.getElementById('result-' + message.stepId);
                    
                    card.classList.remove('running');
                    card.classList.add('failed');
                    status.innerHTML = '<span class="status-badge failed">❌ 失败</span>';
                    
                    result.innerHTML = '<div class="result-card"><div class="result-header" style="color: var(--error);">错误</div><div class="result-content"><pre style="color: var(--error);">' + message.error + '</pre></div></div>';
                    result.classList.add('visible');
                    
                    updateProgress(completedSteps, '失败: ' + STEP_NAMES[message.stepId]);
                    break;
                }
                
                case 'workflowCompleted': {
                    document.getElementById('context').innerHTML = '<pre>' + JSON.stringify(message.context, null, 2) + '</pre>';
                    updateProgress(completedSteps, '工作流完成');
                    break;
                }
                
                case 'reset': {
                    // 已在reset函数中处理
                    break;
                }
                
                case 'error': {
                    alert('错误: ' + message.error);
                    break;
                }
            }
        });
        
        // 步骤名称映射
        const STEP_NAMES = {
            'data_source': '信息获取',
            'market_trend': '市场趋势',
            'mainline': '投资主线',
            'candidate_pool': '候选池构建',
            'factor': '因子构建',
            'strategy': '策略生成',
            'backtest': '回测验证',
            'optimization': '策略优化',
            'report': '报告生成'
        };
    </script>
</body>
</html>`;
    }
}




































