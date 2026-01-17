/**
 * TRQuant 面板基类 V2
 * ====================
 * 
 * 提供统一的面板创建、消息通信、MCP调用能力
 * 
 * 特性:
 * 1. CSP安全策略
 * 2. 状态持久化
 * 3. MCP工具调用
 * 4. 主项目路径强制使用
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn } from 'child_process';

// MCP调用结果
export interface MCPResult {
    ok: boolean;
    data: any;
    error?: string;
}

// 面板配置
export interface PanelConfig {
    viewType: string;
    title: string;
    icon?: string;
}

/**
 * 面板基类
 */
export abstract class BasePanelV2 {
    protected readonly _panel: vscode.WebviewPanel;
    protected readonly _extensionPath: string;
    protected _disposables: vscode.Disposable[] = [];
    
    // 子类必须实现的属性
    abstract get config(): PanelConfig;
    
    // 子类必须实现的方法
    abstract getHtmlContent(): string;
    abstract handleMessage(message: any): Promise<void>;
    
    constructor(panel: vscode.WebviewPanel, extensionPath: string) {
        this._panel = panel;
        this._extensionPath = extensionPath;
        
        // 设置HTML内容
        this._panel.webview.html = this.getHtmlContent();
        
        // 监听Webview消息
        this._panel.webview.onDidReceiveMessage(
            async (message) => {
                console.log(`[BasePanelV2] 收到消息:`, message.command);
                try {
                    await this.handleMessage(message);
                } catch (error) {
                    console.error(`[${this.config.viewType}] 处理消息失败:`, error);
                    this.postMessage({
                        command: 'error',
                        error: String(error)
                    });
                }
            },
            null,
            this._disposables
        );
        
        // 面板关闭时清理
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        
        console.log(`[BasePanelV2] 面板已创建`);
    }
    
    /**
     * 获取项目根目录 (防止worktrees问题)
     */
    protected getProjectRoot(): string {
        // 1. 优先使用硬编码的主项目路径
        const mainPath = '/home/taotao/dev/QuantTest/TRQuant';
        if (fs.existsSync(mainPath)) {
            return mainPath;
        }
        
        // 2. 尝试环境变量
        if (process.env.TRQUANT_ROOT && fs.existsSync(process.env.TRQUANT_ROOT)) {
            return process.env.TRQUANT_ROOT;
        }
        
        // 3. 回退到扩展路径的父目录
        return path.dirname(path.dirname(this._extensionPath));
    }
    
    /**
     * 获取Python解释器路径
     */
    protected getPythonPath(): string {
        const root = this.getProjectRoot();
        const venvPython = path.join(root, 'venv', 'bin', 'python3');
        if (fs.existsSync(venvPython)) {
            return venvPython;
        }
        const venvPython2 = path.join(root, 'venv', 'bin', 'python');
        if (fs.existsSync(venvPython2)) {
            return venvPython2;
        }
        return 'python3';
    }
    
    /**
     * 调用MCP工具
     */
    protected async callMCP(toolName: string, args: Record<string, any> = {}): Promise<MCPResult> {
        const pythonPath = this.getPythonPath();
        const projectRoot = this.getProjectRoot();
        const serverPath = path.join(projectRoot, 'mcp_servers', 'unified_dev_server.py');
        
        return new Promise((resolve) => {
            const proc = spawn(pythonPath, [serverPath], {
                cwd: projectRoot,
                env: {
                    ...process.env,
                    PYTHONPATH: projectRoot,
                    TRQUANT_ROOT: projectRoot
                }
            });
            
            let stdout = '';
            let stderr = '';
            
            proc.stdout.on('data', (data) => {
                stdout += data.toString();
            });
            
            proc.stderr.on('data', (data) => {
                stderr += data.toString();
            });
            
            // 超时处理
            const timeout = setTimeout(() => {
                proc.kill();
                resolve({
                    ok: false,
                    data: null,
                    error: '调用超时 (30秒)'
                });
            }, 30000);
            
            proc.on('close', (code) => {
                clearTimeout(timeout);
                
                if (code === 0) {
                    try {
                        // 解析最后一行JSON
                        const lines = stdout.trim().split('\n');
                        const lastLine = lines[lines.length - 1];
                        const result = JSON.parse(lastLine);
                        
                        if (result.result?.content?.[0]?.text) {
                            const data = JSON.parse(result.result.content[0].text);
                            resolve({
                                ok: true,
                                data: data
                            });
                        } else {
                            resolve({
                                ok: true,
                                data: result
                            });
                        }
                    } catch (e) {
                        resolve({
                            ok: false,
                            data: null,
                            error: `JSON解析失败: ${String(e)}`
                        });
                    }
                } else {
                    resolve({
                        ok: false,
                        data: null,
                        error: `进程退出码 ${code}: ${stderr}`
                    });
                }
            });
            
            // 发送MCP请求
            const request = {
                jsonrpc: '2.0',
                id: 1,
                method: 'initialize',
                params: {
                    protocolVersion: '2024-11-05',
                    capabilities: {},
                    clientInfo: { name: 'TRQuant', version: '1.0' }
                }
            };
            proc.stdin.write(JSON.stringify(request) + '\n');
            
            // 稍等后发送工具调用
            setTimeout(() => {
                const callRequest = {
                    jsonrpc: '2.0',
                    id: 2,
                    method: 'tools/call',
                    params: {
                        name: toolName,
                        arguments: args
                    }
                };
                proc.stdin.write(JSON.stringify(callRequest) + '\n');
                proc.stdin.end();
            }, 100);
        });
    }
    
    /**
     * 调用9步工作流MCP服务器
     */
    protected async callWorkflow9(toolName: string, args: Record<string, any> = {}): Promise<MCPResult> {
        const pythonPath = this.getPythonPath();
        const projectRoot = this.getProjectRoot();
        const serverPath = path.join(projectRoot, 'mcp_servers', 'workflow_9steps_server.py');
        
        return new Promise((resolve) => {
            const proc = spawn(pythonPath, [serverPath], {
                cwd: projectRoot,
                env: {
                    ...process.env,
                    PYTHONPATH: projectRoot,
                    TRQUANT_ROOT: projectRoot
                }
            });
            
            let stdout = '';
            let stderr = '';
            
            proc.stdout.on('data', (data) => {
                stdout += data.toString();
            });
            
            proc.stderr.on('data', (data) => {
                stderr += data.toString();
            });
            
            const timeout = setTimeout(() => {
                proc.kill();
                resolve({ ok: false, data: null, error: '调用超时' });
            }, 60000);
            
            proc.on('close', (code) => {
                clearTimeout(timeout);
                
                if (code === 0) {
                    try {
                        const lines = stdout.trim().split('\n');
                        const lastLine = lines[lines.length - 1];
                        const result = JSON.parse(lastLine);
                        
                        if (result.result?.content?.[0]?.text) {
                            const data = JSON.parse(result.result.content[0].text);
                            resolve({ ok: true, data });
                        } else {
                            resolve({ ok: true, data: result });
                        }
                    } catch (e) {
                        resolve({ ok: false, data: null, error: `解析失败: ${String(e)}` });
                    }
                } else {
                    resolve({ ok: false, data: null, error: `退出码 ${code}: ${stderr}` });
                }
            });
            
            // 初始化
            const initReq = {
                jsonrpc: '2.0',
                id: 1,
                method: 'initialize',
                params: {
                    protocolVersion: '2024-11-05',
                    capabilities: {},
                    clientInfo: { name: 'TRQuant', version: '1.0' }
                }
            };
            proc.stdin.write(JSON.stringify(initReq) + '\n');
            
            setTimeout(() => {
                const callReq = {
                    jsonrpc: '2.0',
                    id: 2,
                    method: 'tools/call',
                    params: { name: toolName, arguments: args }
                };
                proc.stdin.write(JSON.stringify(callReq) + '\n');
                proc.stdin.end();
            }, 100);
        });
    }
    
    /**
     * 发送消息到Webview
     */
    protected postMessage(message: any): void {
        this._panel.webview.postMessage(message);
    }
    
    /**
     * 生成CSP安全的HTML头部
     */
    protected getHtmlHead(title: string, additionalStyles: string = ''): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: https:; connect-src https:;">
    <title>${title}</title>
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #21262d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --accent: #58a6ff;
            --success: #3fb950;
            --warning: #d29922;
            --error: #f85149;
            --border: #30363d;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 24px;
            min-height: 100vh;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1, h2, h3 {
            font-weight: 600;
            margin-bottom: 16px;
        }
        
        h1 { font-size: 28px; color: var(--accent); }
        h2 { font-size: 20px; color: var(--text-primary); }
        h3 { font-size: 16px; color: var(--text-secondary); }
        
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .btn-primary {
            background: var(--accent);
            color: #0d1117;
        }
        
        .btn-primary:hover {
            background: #79c0ff;
            transform: translateY(-1px);
        }
        
        .btn-success {
            background: var(--success);
            color: #0d1117;
        }
        
        .btn-secondary {
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .status-pending { background: var(--bg-secondary); color: var(--text-secondary); }
        .status-running { background: #1f6feb33; color: var(--accent); }
        .status-completed { background: #23863533; color: var(--success); }
        .status-failed { background: #f8514933; color: var(--error); }
        
        .log-container {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 13px;
        }
        
        .log-entry {
            padding: 4px 0;
            border-bottom: 1px solid var(--border);
        }
        
        .log-entry:last-child { border-bottom: none; }
        .log-entry.info { color: var(--text-secondary); }
        .log-entry.success { color: var(--success); }
        .log-entry.error { color: var(--error); }
        .log-entry.warning { color: var(--warning); }
        
        ${additionalStyles}
    </style>
</head>`;
    }
    
    /**
     * 生成通用的Webview脚本
     */
    protected getWebviewScript(): string {
        return `
<script>
(function() {
    const vscode = acquireVsCodeApi();
    
    // 状态管理
    let state = vscode.getState() || {};
    
    function saveState(newState) {
        state = { ...state, ...newState };
        vscode.setState(state);
    }
    
    function getState() {
        return state;
    }
    
    // 消息发送
    function send(command, data = {}) {
        console.log('[Webview] 发送:', command, data);
        vscode.postMessage({ command, ...data });
    }
    
    // 日志
    function log(msg, type = 'info') {
        const logEl = document.getElementById('log-content');
        if (logEl) {
            const entry = document.createElement('div');
            entry.className = 'log-entry ' + type;
            entry.textContent = new Date().toLocaleTimeString() + ' ' + msg;
            logEl.insertBefore(entry, logEl.firstChild);
            
            // 限制日志条数
            while (logEl.children.length > 100) {
                logEl.removeChild(logEl.lastChild);
            }
        }
        console.log('[Webview][' + type + ']', msg);
    }
    
    // 暴露给全局
    window.TRQuant = { send, log, saveState, getState, vscode };
    
    // 消息监听
    window.addEventListener('message', event => {
        const msg = event.data;
        log('收到: ' + msg.command, 'info');
        
        // 触发自定义事件
        window.dispatchEvent(new CustomEvent('trquant-message', { detail: msg }));
    });
    
    // 初始化完成
    document.addEventListener('DOMContentLoaded', () => {
        log('✅ Webview 初始化完成', 'success');
        send('webviewReady');
    });
})();
</script>`;
    }
    
    /**
     * 清理资源
     */
    public dispose(): void {
        console.log(`[BasePanelV2] 面板已关闭`);
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) {
                d.dispose();
            }
        }
    }
}
