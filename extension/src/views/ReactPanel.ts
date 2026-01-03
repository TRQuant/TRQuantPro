import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn, ChildProcess } from 'child_process';

/**
 * React Webview 面板
 * 
 * 用于托管React应用并处理与MCP服务器的通信
 */
export class ReactPanel {
    public static currentPanel: ReactPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _extensionPath: string;
    private _disposables: vscode.Disposable[] = [];
    private _mcpProcess: ChildProcess | null = null;
    private _projectRoot: string;

    public static readonly viewType = 'trquant.reactPanel';

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        extensionPath: string
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._extensionPath = extensionPath;
        this._projectRoot = '/home/taotao/dev/QuantTest/TRQuant';

        // 设置HTML内容
        this._panel.webview.html = this._getHtmlContent();

        // 监听面板关闭
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);

        this._panel.webview.onDidReceiveMessage(
            async (message) => {
                await this._handleMessage(message);
            },
            null,
            this._disposables
        );

        console.log('[ReactPanel] 面板已创建');
    }

    public static createOrShow(extensionUri: vscode.Uri, extensionPath: string): void {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        if (ReactPanel.currentPanel) {
            ReactPanel.currentPanel._panel.reveal(column);
            return;
        }

        // 使用 webview-dist 目录（构建时从 webview-ui/dist 复制而来）
        const distPath = vscode.Uri.joinPath(extensionUri, 'webview-dist');
        const assetsPath = vscode.Uri.joinPath(extensionUri, 'webview-dist', 'assets');
        const resourcesPath = vscode.Uri.joinPath(extensionUri, 'resources');

        // 详细的调试日志
        console.log('[ReactPanel] Extension URI:', extensionUri.toString());
        console.log('[ReactPanel] Extension Path:', extensionPath);
        console.log('[ReactPanel] Dist Path:', distPath.fsPath);
        console.log('[ReactPanel] Assets Path:', assetsPath.fsPath);
        
        // 检查文件是否存在
        if (fs.existsSync(distPath.fsPath)) {
            console.log('[ReactPanel] ✓ webview-dist 目录存在');
        } else {
            console.error('[ReactPanel] ✗ webview-dist 目录不存在:', distPath.fsPath);
            console.log('[ReactPanel] 💡 提示: 请运行 npm run build:webview && npm run copy:webview');
        }

        if (fs.existsSync(assetsPath.fsPath)) {
            console.log('[ReactPanel] ✓ Assets 目录存在');
            const files = fs.readdirSync(assetsPath.fsPath);
            console.log('[ReactPanel] Assets 文件列表:', files);
        } else {
            console.error('[ReactPanel] ✗ Assets 目录不存在:', assetsPath.fsPath);
        }

        const panel = vscode.window.createWebviewPanel(
            ReactPanel.viewType,
            '🐉 TRQuant React Panel',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                // 配置 localResourceRoots 允许访问 webview-dist 资源
                localResourceRoots: [
                    distPath,           // webview-dist 目录
                    assetsPath,         // assets 子目录
                    resourcesPath,      // resources 目录
                    extensionUri        // 整个扩展目录（作为后备）
                ],
            }
        );

        ReactPanel.currentPanel = new ReactPanel(panel, extensionUri, extensionPath);
    }

    private _getHtmlContent(): string {
        const webview = this._panel.webview;
        // 使用 webview-dist 目录（构建时从 webview-ui/dist 复制而来）
        const distPath = vscode.Uri.joinPath(this._extensionUri, 'webview-dist');
        const distFsPath = distPath.fsPath;
        
        // 检查资源目录，提供更友好的错误信息
        if (!fs.existsSync(distFsPath)) {
            const errorMsg = 'React应用未构建，请先运行: npm run build:webview && npm run copy:webview';
            console.error('[ReactPanel]', errorMsg);
            console.error('[ReactPanel] 预期路径:', distFsPath);
            return this._getErrorHtml(errorMsg + `\n\n预期路径: ${distFsPath}`);
        }

        const indexPath = path.join(distFsPath, 'index.html');
        if (!fs.existsSync(indexPath)) {
            const errorMsg = `index.html不存在: ${indexPath}`;
            console.error('[ReactPanel]', errorMsg);
            // 列出目录内容以便调试
            try {
                const files = fs.readdirSync(distFsPath);
                console.error('[ReactPanel] 目录内容:', files);
            } catch (e) {
                console.error('[ReactPanel] 无法读取目录:', e);
            }
            return this._getErrorHtml(errorMsg);
        }

        let html = fs.readFileSync(indexPath, 'utf-8');

        // 生成资源URI
        const scriptPath = vscode.Uri.joinPath(distPath, 'assets', 'index.js');
        const stylePath = vscode.Uri.joinPath(distPath, 'assets', 'index.css');
        
        const scriptUri = webview.asWebviewUri(scriptPath);
        const styleUri = webview.asWebviewUri(stylePath);

        // 验证文件是否存在
        if (!fs.existsSync(scriptPath.fsPath)) {
            console.error('[ReactPanel] ✗ Script 文件不存在:', scriptPath.fsPath);
            return this._getErrorHtml('Script 文件不存在: ' + scriptPath.fsPath);
        }
        if (!fs.existsSync(stylePath.fsPath)) {
            console.warn('[ReactPanel] ⚠ Style 文件不存在:', stylePath.fsPath);
        }

        // 详细的 URI 日志
        console.log('[ReactPanel] Script Path (fs):', scriptPath.fsPath);
        console.log('[ReactPanel] Script URI (webview):', scriptUri.toString());
        console.log('[ReactPanel] Style Path (fs):', stylePath.fsPath);
        console.log('[ReactPanel] Style URI (webview):', styleUri.toString());

        // 替换相对路径为webview URI
        const scriptUriStr = scriptUri.toString();
        const styleUriStr = styleUri.toString();

        console.log('[ReactPanel] 原始 HTML 片段:', html.substring(0, 500));
        
        // 替换 script 标签中的路径（匹配 ./assets/index.js 或 assets/index.js）
        html = html.replace(
            /(<script[^>]*src=["'])(\.?\/?assets\/index\.js)(["'][^>]*>)/gi,
            `$1${scriptUriStr}$3`
        );
        
        // 替换 link 标签中的路径（匹配 ./assets/index.css 或 assets/index.css）
        html = html.replace(
            /(<link[^>]*href=["'])(\.?\/?assets\/index\.css)(["'][^>]*>)/gi,
            `$1${styleUriStr}$3`
        );
        
        console.log('[ReactPanel] 替换后 HTML 片段:', html.substring(0, 500));
        console.log('[ReactPanel] 是否包含 script URI:', html.includes(scriptUriStr));
        console.log('[ReactPanel] 是否包含 style URI:', html.includes(styleUriStr));

        // CSP 配置（进一步放宽以支持 Ant Design 和运行时脚本）
        const csp = [
            "default-src 'none'",
            "font-src " + webview.cspSource + " https: data:",
            "img-src " + webview.cspSource + " https: data: blob:",
            "script-src " + webview.cspSource + " 'unsafe-inline' 'unsafe-eval' 'wasm-unsafe-eval' https:",
            "style-src " + webview.cspSource + " 'unsafe-inline' https:",
            "connect-src " + webview.cspSource + " https: wss: http://localhost:*",
        ].join('; ');

        // 插入 CSP
        if (html.includes('<head>')) {
            html = html.replace(
                '<head>',
                '<head>\n    <meta http-equiv="Content-Security-Policy" content="' + csp + '">'
            );
        }

        // 添加调试信息和错误处理
        if (html.includes('</body>')) {
            const debugScript = `
                <script>
                    console.log("[ReactPanel Debug] Script URI:", "${scriptUriStr}");
                    console.log("[ReactPanel Debug] Style URI:", "${styleUriStr}");
                    console.log("[ReactPanel Debug] Root element exists:", !!document.getElementById('root'));
                    
                    // 检查脚本是否加载
                    window.addEventListener('error', (e) => {
                        console.error("[ReactPanel] 加载错误:", e.message, e.filename, e.lineno);
                    });
                    
                    // 检查 React 是否初始化
                    setTimeout(() => {
                        const root = document.getElementById('root');
                        if (root && root.innerHTML.trim() === '') {
                            console.warn("[ReactPanel] Root 元素为空，React 可能未初始化");
                        } else {
                            console.log("[ReactPanel] React 应用已加载");
                        }
                    }, 1000);
                </script>
            `;
            html = html.replace('</body>', debugScript + '</body>');
        }

        return html;
    }

    private _getErrorHtml(message: string): string {
        return '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Error</title><style>body{font-family:sans-serif;padding:20px;background:#1e1e1e;color:#d4d4d4}h1{color:#f48771}</style></head><body><h1>❌ React Panel 错误</h1><p>' + message + '</p></body></html>';
    }

    private async _handleMessage(message: any): Promise<void> {
        console.log('[ReactPanel] 收到消息:', message.type);

        switch (message.type) {
            case 'ready':
                console.log('[ReactPanel] Webview已就绪');
                break;

            case 'mcpCall':
            case 'mcp_call':
                await this._handleMcpCall(message);
                break;

            case 'info':
                vscode.window.showInformationMessage(message.text);
                break;

            case 'error':
                vscode.window.showErrorMessage(message.text);
                break;

            default:
                console.log('[ReactPanel] 未知消息类型:', message.type);
        }
    }

    private async _handleMcpCall(message: any): Promise<void> {
        const tool = message.tool;
        const args = message.args || {};
        const id = message.id || message.requestId;
        
        console.log('[ReactPanel] MCP调用: ' + tool, { id, args });

        try {
            const result = await this._callMcpTool(tool, args);
            
            this._panel.webview.postMessage({
                type: 'mcpResult',
                id: id,
                result: result,
                error: undefined
            });
        } catch (error) {
            console.error('[ReactPanel] MCP调用失败: ' + tool, error);
            
            this._panel.webview.postMessage({
                type: 'mcpResult',
                id: id,
                result: undefined,
                error: error instanceof Error ? error.message : '未知错误'
            });
        }
    }

    private async _callMcpTool(tool: string, args: any): Promise<any> {
        return new Promise((resolve, reject) => {
            const pythonPath = '/home/taotao/dev/QuantTest/TRQuant/venv/bin/python';
            
            const process_mcp = spawn(pythonPath, ['-c', 'import json; print(json.dumps({"ok": True, "data": {"status": "mock", "message": "Call received"}}))'], { cwd: this._projectRoot });

            let stdout = '';
            let stderr = '';
            
            process_mcp.stdout.on('data', d => stdout += d.toString());
            process_mcp.stderr.on('data', d => stderr += d.toString());
            
            process_mcp.on('close', code => {
                if (code === 0) {
                    try {
                        const res = JSON.parse(stdout.trim());
                        if (res.ok) {
                            resolve(res.data);
                        } else {
                            reject(new Error(res.error || 'Unknown error'));
                        }
                    } catch (e) {
                        reject(new Error('Invalid JSON: ' + stdout));
                    }
                } else {
                    reject(new Error('Process exited with code ' + code + '. stderr: ' + stderr));
                }
            });
        });
    }

    public dispose(): void {
        ReactPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }
}
