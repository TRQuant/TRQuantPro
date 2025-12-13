---
title: "10.5 Cursor扩展开发"
description: "深入解析TRQuant Cursor扩展开发，包括TypeScript扩展开发、命令系统、视图系统、MCP集成、构建打包等核心技术，为VS Code/Cursor扩展开发提供完整的开发指导"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 🔌 10.5 Cursor扩展开发

> **核心摘要：**
> 
> 本节系统介绍TRQuant Cursor扩展开发，包括TypeScript扩展开发、命令系统、视图系统、MCP集成、构建打包等核心技术。通过理解Cursor扩展开发的完整方法，帮助开发者掌握VS Code/Cursor扩展的开发技巧，为构建专业级的扩展应用奠定基础。

Cursor扩展采用TypeScript开发，提供在Cursor/VS Code环境中的量化投资工作流支持，包括MCP工具集成、命令调用、视图展示等功能。

## 📋 章节概览

<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}
</script>

<div class="section-overview">
  <div class="section-item" onclick="scrollToSection('section-10-5-1')">
    <h4>🏗️ 10.5.1 扩展架构</h4>
    <p>扩展结构、激活流程、服务管理、生命周期</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-5-2')">
    <h4>⚙️ 10.5.2 命令系统</h4>
    <p>命令注册、命令处理、命令调用、命令参数</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-5-3')">
    <h4>🖥️ 10.5.3 视图系统</h4>
    <p>WebView面板、视图管理、消息通信、数据绑定</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-5-4')">
    <h4>🔗 10.5.4 MCP集成</h4>
    <p>MCP协议、MCP Server注册、MCP工具调用</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-5-5')">
    <h4>📦 10.5.5 构建打包</h4>
    <p>TypeScript编译、VSIX打包、扩展安装、调试模式</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解扩展架构**：掌握Cursor扩展的整体架构和激活流程
- **实现命令系统**：理解命令注册、处理和调用机制
- **开发视图系统**：掌握WebView面板的创建和消息通信
- **集成MCP协议**：理解MCP Server注册和工具调用
- **构建打包扩展**：掌握TypeScript编译和VSIX打包方法

## 📚 核心概念

### 技术栈

- **扩展框架**：VS Code Extension API（TypeScript）
- **通信协议**：JSON-RPC（与Python后端）、MCP（与Cursor AI）
- **视图技术**：WebView（HTML/CSS/JavaScript）
- **构建工具**：Webpack、VS Code Extension Manager (vsce)

### 扩展结构

```
extension/
├── src/
│   ├── extension.ts          # 扩展入口
│   ├── services/             # 核心服务
│   │   ├── trquantClient.ts  # Python后端客户端
│   │   └── mcpRegistrar.ts   # MCP注册器
│   ├── commands/             # 命令实现
│   ├── views/                # 视图实现
│   └── utils/                # 工具类
├── package.json              # 扩展配置
└── tsconfig.json             # TypeScript配置
```

<h2 id="section-10-5-1">🏗️ 10.5.1 扩展架构</h2>

扩展架构包括扩展结构、激活流程和服务管理。

### 扩展入口

```typescript
// extension/src/extension.ts
import * as vscode from 'vscode';
import { TRQuantClient } from './services/trquantClient';
import { MCPRegistrar } from './services/mcpRegistrar';
import { MainDashboard, registerMainDashboard } from './views/mainDashboard';
import { logger } from './utils/logger';
import { config, ConfigManager } from './utils/config';

const MODULE = 'Extension';

// 全局实例
let client: TRQuantClient;
let statusBarItem: vscode.StatusBarItem;

/**
 * 扩展激活入口
 */
export async function activate(
    context: vscode.ExtensionContext
): Promise<void> {
    logger.info('TRQuant Extension 正在激活...', MODULE);
    
    const startTime = Date.now();
    
    try {
        // 1. 初始化配置
        const configManager = ConfigManager.getInstance();
        context.subscriptions.push({
            dispose: () => configManager.dispose()
        });
        
        // 2. 初始化客户端
        client = new TRQuantClient(context);
        context.subscriptions.push({
            dispose: () => client.dispose()
        });
        
        // 3. 创建状态栏
        statusBarItem = createStatusBar();
        context.subscriptions.push(statusBarItem);
        
        // 4. 注册命令
        registerCommands(context);
        
        // 5. 注册主控制台
        registerMainDashboard(context, client);
        
        // 6. 注册MCP（如果启用）
        if (config.get('mcpEnabled')) {
            await registerMCP(context);
        }
        
        // 7. 更新状态栏
        await updateStatusBar();
        
        const duration = Date.now() - startTime;
        logger.info(`TRQuant Extension 激活完成 (${duration}ms)`, MODULE);
        
        // 8. 自动打开主控制台
        setTimeout(() => {
            MainDashboard.createOrShow(context.extensionUri, client);
        }, 500);
        
    } catch (error) {
        logger.error(`扩展激活失败: ${error}`, MODULE);
        throw error;
    }
}

/**
 * 扩展停用
 */
export function deactivate(): void {
    logger.info('TRQuant Extension 正在停用...', MODULE);
    
    if (client) {
        client.dispose();
    }
    
    logger.dispose();
}
```

### 服务管理

```typescript
// extension/src/services/trquantClient.ts
import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';
import { logger } from '../utils/logger';

export class TRQuantClient {
    private readonly MODULE = 'TRQuantClient';
    private extensionPath: string;
    
    constructor(context: vscode.ExtensionContext) {
        this.extensionPath = context.extensionPath;
        logger.info('TRQuantClient初始化完成', this.MODULE);
    }
    
    /**
     * 调用Python后端
     * 
     * **设计原理**：
     * - **进程通信**：通过spawn创建Python子进程，使用stdin/stdout通信
     * - **JSON协议**：使用JSON格式传递请求和响应，便于解析
     * - **异步处理**：使用Promise封装，支持async/await调用
     * 
     * **为什么这样设计**：
     * 1. **语言隔离**：TypeScript扩展和Python后端分离，便于独立开发和部署
     * 2. **协议简单**：JSON协议简单易用，无需复杂的序列化框架
     * 3. **异步支持**：Promise封装支持异步调用，不阻塞UI线程
     * 
     * **使用场景**：
     * - 调用Python后端的MCP工具
     * - 执行量化工作流
     * - 获取市场数据和分析结果
     * 
     * **注意事项**：
     * - 需要确保Python环境可用
     * - bridge.py脚本需要正确实现
     * - 错误处理需要完善，避免进程异常导致扩展崩溃
     */
    async callBridge<T>(
        action: string,
        params: Record<string, any>
    ): Promise<ApiResponse<T>> {
        return new Promise((resolve, reject) => {
            // 设计原理：获取Python路径和bridge脚本路径
            // 原因：需要知道Python解释器位置和bridge脚本位置
            const pythonPath = this.getPythonPath();
            const bridgePath = path.join(
                this.extensionPath,
                'python',
                'bridge.py'
            );
            
            // 设计原理：使用spawn创建子进程
            // 原因：需要与Python进程通信，spawn支持stdin/stdout
            // stdio配置：['pipe', 'pipe', 'pipe']表示stdin、stdout、stderr都使用管道
            const process = cp.spawn(pythonPath, [bridgePath], {
                stdio: ['pipe', 'pipe', 'pipe']
            });
            
            // 设计原理：构建请求对象
            // 原因：需要传递action和params给Python后端
            const request = {
                action,
                params
            };
            
            // 设计原理：通过stdin发送请求
            // 原因：子进程通过stdin接收输入
            // 注意：需要end()关闭stdin，否则Python进程会一直等待
            process.stdin.write(JSON.stringify(request));
            process.stdin.end();
            
            // 设计原理：收集stdout输出
            // 原因：Python后端的响应通过stdout返回
            let output = '';
            process.stdout.on('data', (data) => {
                output += data.toString();
            });
            
            // 设计原理：处理进程关闭事件
            // 原因：进程结束时需要解析响应或处理错误
            process.on('close', (code) => {
                if (code === 0) {
                    // 设计原理：成功时解析JSON响应
                    // 原因：Python后端返回JSON格式的响应
                    try {
                        const response = JSON.parse(output);
                        resolve(response);
                    } catch (e) {
                        reject(new Error(`解析响应失败: ${e}`));
                    }
                } else {
                    // 设计原理：失败时返回错误
                    // 原因：非零退出码表示进程异常
                    reject(new Error(`进程退出码: ${code}`));
                }
            });
        });
    }
    
    private getPythonPath(): string {
        // 获取Python路径
        return 'python3';
    }
    
    dispose(): void {
        // 清理资源
    }
}
```

<h2 id="section-10-5-2">⚙️ 10.5.2 命令系统</h2>

命令系统负责命令注册、处理和调用。

### 命令注册

```typescript
// extension/src/extension.ts
import { getMarketStatus } from './commands/getMarketStatus';
import { getMainlines } from './commands/getMainlines';
import { recommendFactors } from './commands/recommendFactors';
import { generateStrategy } from './commands/generateStrategy';

/**
 * 注册所有命令
 */
function registerCommands(context: vscode.ExtensionContext): void {
    const commands: Array<{
        id: string;
        handler: () => Promise<void>;
    }> = [
        {
            id: 'trquant.getMarketStatus',
            handler: () => getMarketStatus(client, context)
        },
        {
            id: 'trquant.getMainlines',
            handler: () => getMainlines(client, context)
        },
        {
            id: 'trquant.recommendFactors',
            handler: () => recommendFactors(client, context)
        },
        {
            id: 'trquant.generateStrategy',
            handler: () => generateStrategy(client, context)
        },
        {
            id: 'trquant.openDashboard',
            handler: async () => {
                MainDashboard.createOrShow(context.extensionUri, client);
            }
        },
        {
            id: 'trquant.launchDesktopSystem',
            handler: async () => {
                await launchDesktopSystem(context);
            }
        }
    ];
    
    for (const { id, handler } of commands) {
        const disposable = vscode.commands.registerCommand(
            id,
            async () => {
                logger.debug(`执行命令: ${id}`, MODULE);
                try {
                    await handler();
                } catch (error) {
                    logger.error(`命令执行失败: ${id}`, MODULE, { error });
                    vscode.window.showErrorMessage(
                        `命令执行失败: ${error instanceof Error ? error.message : String(error)}`
                    );
                }
            }
        );
        context.subscriptions.push(disposable);
    }
    
    logger.info(`已注册 ${commands.length} 个命令`, MODULE);
}
```

### 命令实现示例

```typescript
// extension/src/commands/getMarketStatus.ts
import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';

const MODULE = 'GetMarketStatus';

/**
 * 获取市场状态命令
 */
export async function getMarketStatus(
    client: TRQuantClient,
    context: vscode.ExtensionContext
): Promise<void> {
    try {
        logger.info('执行获取市场状态命令', MODULE);
        
        // 显示进度提示
        await vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: '获取市场状态',
                cancellable: false
            },
            async (progress) => {
                progress.report({ increment: 0, message: '正在获取市场状态...' });
                
                // 调用后端API
                const result = await client.getMarketStatus({
                    universe: 'CN_EQ',
                    lookback_days: 60
                });
                
                progress.report({ increment: 50, message: '处理结果...' });
                
                if (result.ok && result.data) {
                    const status = result.data;
                    
                    // 显示结果
                    const message = `市场状态: ${status.regime}\n` +
                        `趋势: ${status.trend}\n` +
                        `评分: ${status.score}`;
                    
                    vscode.window.showInformationMessage(message);
                    
                    // 打开市场面板
                    const MarketPanel = await import('../views/marketPanel');
                    MarketPanel.MarketPanel.createOrShow(
                        context.extensionUri,
                        client
                    );
                } else {
                    throw new Error(result.error || '获取市场状态失败');
                }
                
                progress.report({ increment: 100 });
            }
        );
        
    } catch (error) {
        logger.error('获取市场状态失败', MODULE, { error });
        vscode.window.showErrorMessage(
            `获取市场状态失败: ${error instanceof Error ? error.message : String(error)}`
        );
    }
}
```

<h2 id="section-10-5-3">🖥️ 10.5.3 视图系统</h2>

视图系统负责WebView面板的创建、消息通信和数据绑定。

### WebView面板基类

```typescript
// extension/src/views/basePanel.ts
import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';

export abstract class BasePanel {
    protected static panels: Map<string, BasePanel> = new Map();
    
    protected readonly _panel: vscode.WebviewPanel;
    protected readonly _extensionUri: vscode.Uri;
    protected readonly _client: TRQuantClient;
    protected _disposables: vscode.Disposable[] = [];
    
    protected constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._client = client;
        
        // 设置WebView选项
        this._panel.webview.options = {
            enableScripts: true,
            localResourceRoots: [
                vscode.Uri.joinPath(this._extensionUri, 'media'),
                vscode.Uri.joinPath(this._extensionUri, 'out')
            ]
        };
        
        // 监听消息
        this._panel.webview.onDidReceiveMessage(
            (message) => this.handleMessage(message),
            null,
            this._disposables
        );
        
        // 监听面板关闭
        this._panel.onDidDispose(
            () => this.dispose(),
            null,
            this._disposables
        );
        
        // 设置初始内容
        this._panel.webview.html = this.getHtml();
    }
    
    protected abstract handleMessage(message: any): Promise<void>;
    protected abstract getHtml(): string;
    
    public dispose(): void {
        BasePanel.panels.delete(this._panel.viewType);
        
        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) {
                disposable.dispose();
            }
        }
    }
    
    protected postMessage(message: any): void {
        this._panel.webview.postMessage(message);
    }
}
```

### 主控制台视图

```typescript
// extension/src/views/mainDashboard.ts
import * as vscode from 'vscode';
import { BasePanel } from './basePanel';
import { TRQuantClient } from '../services/trquantClient';

export class MainDashboard extends BasePanel {
    private static currentPanel: MainDashboard | undefined;
    
    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ) {
        super(panel, extensionUri, client);
        this.updateContent();
    }
    
    public static createOrShow(
        extensionUri: vscode.Uri,
        client: TRQuantClient
    ): MainDashboard {
        const column = vscode.ViewColumn.One;
        
        // 复用已存在的面板
        if (MainDashboard.currentPanel) {
            MainDashboard.currentPanel._panel.reveal(column);
            return MainDashboard.currentPanel;
        }
        
        // 创建新面板
        const panel = vscode.window.createWebviewPanel(
            'trquantMainDashboard',
            '📊 TRQuant 量化工作台',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );
        
        MainDashboard.currentPanel = new MainDashboard(
            panel,
            extensionUri,
            client
        );
        
        return MainDashboard.currentPanel;
    }
    
    protected async handleMessage(message: any): Promise<void> {
        const { command } = message;
        
        switch (command) {
            case 'openWorkflowStep':
                await this.openWorkflowStep(message.step);
                break;
            
            case 'getMarketStatus':
                await this.getMarketStatus();
                break;
            
            default:
                logger.warn(`未知命令: ${command}`, 'MainDashboard');
        }
    }
    
    protected getHtml(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TRQuant 量化工作台</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .workflow-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-top: 20px;
        }
        .workflow-step {
            background: white;
            border-radius: 8px;
            padding: 20px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .workflow-step:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <h1>📊 TRQuant 量化工作台</h1>
    <div class="workflow-container" id="workflowContainer">
        <!-- 工作流步骤卡片 -->
    </div>
    <script>
        const vscode = acquireVsCodeApi();
        
        // 工作流步骤数据
        const steps = [
            { step: 1, icon: '📡', name: '信息获取' },
            { step: 2, icon: '📈', name: '市场分析' },
            { step: 3, icon: '🔥', name: '投资主线' },
            { step: 4, icon: '📦', name: '候选池构建' },
            { step: 5, icon: '📊', name: '因子构建' },
            { step: 6, icon: '🛠️', name: '策略生成' },
            { step: 7, icon: '🔄', name: '回测验证' },
            { step: 8, icon: '🚀', name: '实盘交易' }
        ];
        
        // 渲染工作流步骤
        const container = document.getElementById('workflowContainer');
        steps.forEach(step => {
            const card = document.createElement('div');
            card.className = 'workflow-step';
            card.innerHTML = \`
                <div style="font-size: 32px; margin-bottom: 8px;">\${step.icon}</div>
                <div style="font-weight: 600;">\${step.name}</div>
            \`;
            card.onclick = () => {
                vscode.postMessage({
                    command: 'openWorkflowStep',
                    step: step.step
                });
            };
            container.appendChild(card);
        });
        
        // 监听消息
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'marketStatusUpdated':
                    console.log('市场状态更新:', message.data);
                    break;
            }
        });
    </script>
</body>
</html>`;
    }
}
```

<h2 id="section-10-5-4">🔗 10.5.4 MCP集成</h2>

MCP集成负责MCP Server注册和MCP工具调用。

### MCP Server注册

```typescript
// extension/src/services/mcpRegistrar.ts
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';
import { logger } from '../utils/logger';
import { config } from '../utils/config';

const MODULE = 'MCPRegistrar';

/**
 * MCP配置接口
 */
interface MCPConfig {
    mcpServers: {
        [key: string]: {
            command: string;
            args: string[];
            env?: Record<string, string>;
        };
    };
}

/**
 * MCP注册器
 */
export class MCPRegistrar {
    /**
     * 注册MCP Server到Cursor
     */
    static async registerServer(
        context: vscode.ExtensionContext
    ): Promise<void> {
        logger.info('开始注册MCP Server...', MODULE);
        
        try {
            // 获取MCP配置文件路径
            const configPath = this.getMCPConfigPath();
            logger.info(`MCP配置路径: ${configPath}`, MODULE);
            
            // 读取现有配置或创建新配置
            const mcpConfig = this.loadMCPConfig(configPath);
            
            // 添加TRQuant Server
            const pythonPath = config.getPythonPath(context.extensionPath);
            const mcpServerPath = path.join(
                context.extensionPath,
                'python',
                'mcp_server.py'
            );
            
            mcpConfig.mcpServers['trquant'] = {
                command: pythonPath,
                args: [mcpServerPath],
                env: {
                    PYTHONIOENCODING: 'utf-8',
                    TRQUANT_ROOT: path.dirname(context.extensionPath),
                },
            };
            
            // 保存配置
            this.saveMCPConfig(configPath, mcpConfig);
            
            logger.info('MCP Server 注册成功', MODULE);
            
            // 提示用户
            vscode.window
                .showInformationMessage(
                    'TRQuant MCP Server 已注册。重启Cursor后生效。',
                    '查看配置',
                    '了解更多'
                )
                .then((selection) => {
                    if (selection === '查看配置') {
                        this.openMCPConfig(configPath);
                    } else if (selection === '了解更多') {
                        vscode.env.openExternal(
                            vscode.Uri.parse('https://docs.cursor.com/context/model-context-protocol')
                        );
                    }
                });
        } catch (error) {
            logger.error(
                `MCP注册失败: ${error instanceof Error ? error.message : String(error)}`,
                MODULE
            );
            throw error;
        }
    }
    
    private static getMCPConfigPath(): string {
        const homeDir = os.homedir();
        const platform = os.platform();
        
        if (platform === 'win32') {
            return path.join(homeDir, 'AppData', 'Roaming', 'Cursor', 'User', 'globalStorage', 'mcp.json');
        } else if (platform === 'darwin') {
            return path.join(homeDir, 'Library', 'Application Support', 'Cursor', 'User', 'globalStorage', 'mcp.json');
        } else {
            return path.join(homeDir, '.config', 'Cursor', 'User', 'globalStorage', 'mcp.json');
        }
    }
    
    private static loadMCPConfig(configPath: string): MCPConfig {
        if (fs.existsSync(configPath)) {
            try {
                const content = fs.readFileSync(configPath, 'utf-8');
                return JSON.parse(content);
            } catch (error) {
                logger.warn('读取MCP配置失败，创建新配置', MODULE);
            }
        }
        
        return {
            mcpServers: {}
        };
    }
    
    private static saveMCPConfig(
        configPath: string,
        config: MCPConfig
    ): void {
        // 确保目录存在
        const configDir = path.dirname(configPath);
        if (!fs.existsSync(configDir)) {
            fs.mkdirSync(configDir, { recursive: true });
        }
        
        // 保存配置
        fs.writeFileSync(
            configPath,
            JSON.stringify(config, null, 2),
            'utf-8'
        );
    }
    
    private static openMCPConfig(configPath: string): void {
        vscode.workspace.openTextDocument(configPath).then(doc => {
            vscode.window.showTextDocument(doc);
        });
    }
}
```

<h2 id="section-10-5-5">📦 10.5.5 构建打包</h2>

构建打包包括TypeScript编译、VSIX打包和扩展安装。

### 构建配置

```json
// extension/package.json
{
  "name": "trquant-cursor-extension",
  "version": "0.1.0",
  "engines": {
    "vscode": "^1.85.0"
  },
  "scripts": {
    "compile": "webpack --mode production",
    "watch": "webpack --mode development --watch",
    "package": "vsce package --allow-missing-repository --no-dependencies"
  },
  "devDependencies": {
    "@types/vscode": "^1.85.0",
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "webpack": "^5.0.0",
    "@vscode/vsce": "^2.22.0"
  }
}
```

### 构建流程

```bash
# 1. 编译TypeScript
cd extension
npm run compile

# 2. 打包为VSIX
npx @vscode/vsce package --allow-missing-repository --no-dependencies

# 3. 安装到Cursor
cursor --install-extension trquant-cursor-extension-0.1.0.vsix --force

# 4. 重新加载窗口
# 在Cursor中按 Ctrl+Shift+P，输入 "Developer: Reload Window"
```

### 调试模式

```bash
# Watch模式（自动编译）
cd extension
npm run watch

# F5调试
# 1. 在Cursor中打开 extension/ 文件夹
# 2. 按 F5 键
# 3. 选择 "Run Extension"
# 4. 新窗口中测试（使用开发目录代码）
```

### 重要注意事项

**⚠️ 必须重新打包安装**

Cursor使用的是**已安装的扩展**（位于 `~/.cursor/extensions/`），而不是开发目录中的源代码。

**正确流程**：
1. 修改 `extension/src/` 中的代码
2. 运行 `npm run compile` 编译
3. 运行 `npx @vscode/vsce package` 打包
4. 运行 `cursor --install-extension xxx.vsix` 安装
5. 重新加载Cursor窗口

**常见错误**：
- ❌ 只编译不安装：修改代码后只运行 `npm run compile`，期望扩展自动更新
- ❌ 路径错误：使用 `path.dirname(context.extensionPath)` 获取根目录

## 🔗 相关章节

- **9.5 Cursor扩展集成**：了解Cursor扩展与系统的集成
- **10.7 MCP服务器开发指南**：了解MCP Server开发
- **第1章：系统概述**：了解系统整体设计

## 💡 关键要点

1. **扩展架构**：清晰的模块划分和服务管理
2. **命令系统**：统一的命令注册和处理机制
3. **视图系统**：灵活的WebView面板和消息通信
4. **MCP集成**：完整的MCP Server注册和工具支持
5. **构建打包**：正确的编译、打包和安装流程

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了Cursor扩展开发，包括TypeScript扩展开发、命令系统、视图系统、MCP集成、构建打包等核心技术。通过理解Cursor扩展开发的完整方法，帮助开发者掌握VS Code/Cursor扩展的开发技巧。</p>
  
  <h3>下节预告</h3>
  <p>掌握了Cursor扩展开发后，下一节将介绍前端开发指南，包括Astro文档站点开发、组件开发、页面路由、样式设计等。通过理解前端开发方法，帮助开发者掌握文档站点的开发技巧。</p>
  
  <a href="/ashare-book6/010_Chapter10_Development_Guide/10.6_Frontend_Development_Guide_CN" class="next-section">
    继续学习：10.6 前端开发指南 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12
