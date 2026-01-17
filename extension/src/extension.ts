/**
 * TRQuant Cursor Extension
 * ========================
 * 
 * 韬睿量化 - A股量化投资助手
 * 
 * 功能：
 * 1. 获取市场状态和投资主线
 * 2. 推荐因子和生成策略（PTrade/QMT）
 * 3. 通过MCP协议与Cursor AI集成
 * 
 * 架构：
 * - 遵循VS Code Extension最佳实践
 * - 使用依赖注入管理服务
 * - 统一的日志和错误处理
 */

import * as vscode from 'vscode';

// 核心服务
import { TRQuantClient } from './services/trquantClient';
import { MCPRegistrar } from './services/mcpRegistrar';
import { registerConfigCommands } from './services/projectConfig';
import { registerBacktestManager } from './services/backtestManager';

// 命令
import { getMarketStatus } from './commands/getMarketStatus';
import { getMainlines } from './commands/getMainlines';
import { recommendFactors } from './commands/recommendFactors';
import { generateStrategy } from './commands/generateStrategy';
import { analyzeBacktest } from './commands/analyzeBacktest';
import { createProject } from './commands/createProject';
import { runBacktest } from './commands/runBacktest';

// 视图
import { MarketPanel } from './views/marketPanel';
import { MainDashboard, registerMainDashboard } from './views/mainDashboard';
import { StrategyManagerPanel } from './views/strategyManagerPanel';
import { WorkflowPanel } from './views/workflowPanel';

// 提供者
import { registerStrategyCompletionProvider } from './providers/strategyCompletionProvider';
import { registerWorkflowProvider } from './providers/workflowProvider';
import { registerStrategyDiagnosticProvider } from './providers/strategyDiagnosticProvider';

// 工具
import { logger, LogLevel } from './utils/logger';
import { config, ConfigManager } from './utils/config';
import { ErrorHandler } from './utils/errors';

// V2 面板 (9步工作流MCP集成)
import { registerPanels, registerSidebarProviders } from './views/registerPanels';

const MODULE = 'Extension';

// 全局实例
let client: TRQuantClient;
let statusBarItem: vscode.StatusBarItem;

/**
 * 扩展激活入口
 */
export async function activate(context: vscode.ExtensionContext): Promise<void> {
    logger.info('TRQuant Extension 正在激活...', MODULE);
    
    const startTime = Date.now();

    try {
        // 初始化配置
        const configManager = ConfigManager.getInstance();
        context.subscriptions.push({ dispose: () => configManager.dispose() });

        // 初始化客户端
        client = new TRQuantClient(context);
        context.subscriptions.push({ dispose: () => client.dispose() });

        // 创建状态栏
        statusBarItem = createStatusBar();
        context.subscriptions.push(statusBarItem);

        // 注册命令
        registerCommands(context);

        // 注册V2面板 (9步工作流MCP集成)
        registerPanels(context, client);
        registerSidebarProviders(context);

        // 注册工作流视图提供者
        registerWorkflowProvider(context);
        // 注册项目资源管理器

        // 注册配置管理命令
        registerConfigCommands(context);

        // 注册回测管理器
        registerBacktestManager(context, client);

        // 注册回测报告命令

        // 注册策略代码补全提供者
        registerStrategyCompletionProvider(context);

        // 注册策略代码诊断提供者
        registerStrategyDiagnosticProvider(context);

        // 注册主控制台
        registerMainDashboard(context, client);

        // 注册MCP（如果启用）
        if (config.get('mcpEnabled')) {
            await registerMCP(context);
        }

        // 初始化完成后更新状态栏
        updateStatusBar();

        const duration = Date.now() - startTime;
        logger.info(`TRQuant Extension 激活完成 (${duration}ms)`, MODULE);

        // 自动打开主控制台 GUI（仅在存在工作区时）
        // 使用更长的延迟，确保所有资源都已准备好
        setTimeout(() => {
            try {
                const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
                if (workspaceFolder) {
                    // 检查资源是否准备好
                    const extension = vscode.extensions.getExtension('trquant.trquant-cursor-extension');
                    if (extension) {
                        MainDashboard.createOrShow(context.extensionUri, client, context.extensionPath);
                    } else {
                        logger.warn('扩展未找到，延迟打开主控制台', MODULE);
                        // 重试一次
                        setTimeout(() => {
                            try {
                                MainDashboard.createOrShow(context.extensionUri, client, context.extensionPath);
                            } catch (error) {
                                logger.warn('重试打开主控制台失败', MODULE, { error });
                            }
                        }, 1000);
                    }
                } else {
                    logger.info('未检测到工作区，跳过自动打开主控制台', MODULE);
                }
            } catch (error) {
                logger.warn('自动打开主控制台失败', MODULE, { error });
            }
        }, 1000); // 增加到1秒，给资源加载更多时间

    } catch (error) {
        ErrorHandler.handle(error, MODULE);
        throw error;
    }
}

/**
 * 创建状态栏项
 */
function createStatusBar(): vscode.StatusBarItem {
    const item = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    
    item.text = '$(graph) TRQuant';
    item.tooltip = 'TRQuant 量化助手 - 点击打开控制面板';
    item.command = 'trquant.showPanel';
    item.show();

    return item;
}

/**
 * 注册所有命令
 */
function registerCommands(context: vscode.ExtensionContext): void {
    const commands: Array<{ id: string; handler: () => Promise<void> }> = [
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
            id: 'trquant.analyzeBacktest',
            handler: () => analyzeBacktest(client, context)
        },
        {
            id: 'trquant.createProject',
            handler: () => createProject(context)
        },
        {
            id: 'trquant.runBacktest',
            handler: () => runBacktest(client, context)
        },
        {
            id: 'trquant.enableMCP',
            handler: async () => {
                await registerMCP(context);
                vscode.window.showInformationMessage('TRQuant MCP Server 已启用');
            }
        },
        {
            id: 'trquant.showPanel',
            handler: async () => {
                MarketPanel.createOrShow(context.extensionUri, client);
            }
        },
        {
            id: 'trquant.showDashboard',
            handler: async () => {
            }
        },
        // trquant.openDashboard 已在 registerMainDashboard 中注册，这里不再重复注册
        {
            id: 'trquant.showWelcome',
            handler: async () => {
            }
        },
        {
            id: 'trquant.showLogs',
            handler: async () => {
                logger.show();
            }
        },
        {
            id: 'trquant.refreshStatus',
            handler: async () => {
                await updateStatusBar();
                vscode.window.showInformationMessage('状态已刷新');
            }
        },
        {
            id: 'trquant.showStrategyManager',
            handler: async () => {
                StrategyManagerPanel.createOrShow(context.extensionUri);
            }
        },
        {
            id: 'trquant.showWorkflow',
            handler: async () => {
                WorkflowPanel.createOrShow(context.extensionUri, context.extensionPath);
            }
        }
    ];

    // 注册所有命令
    for (const { id, handler } of commands) {
        const disposable = vscode.commands.registerCommand(id, async () => {
            await ErrorHandler.wrap(handler, id);
        });
        context.subscriptions.push(disposable);
    }

    logger.info(`已注册 ${commands.length} 个命令`, MODULE);
}

/**
 * 注册MCP Server
 */
async function registerMCP(context: vscode.ExtensionContext): Promise<void> {
    try {
        await MCPRegistrar.registerServer(context);
        logger.info('MCP Server 已注册', MODULE);
    } catch (error) {
        logger.warn(`MCP注册失败: ${error instanceof Error ? error.message : String(error)}`, MODULE);
    }
}

/**
 * 更新状态栏显示
 */
async function updateStatusBar(): Promise<void> {
    try {
        const result = await client.getMarketStatus();
        
        if (result.ok && result.data) {
            const regime = result.data.regime;
            const regimeIcons: Record<string, string> = {
                'risk_on': '📈',
                'risk_off': '📉',
                'neutral': '➡️'
            };
            
            const icon = regimeIcons[regime] || '📊';
            statusBarItem.text = `$(graph) ${icon} TRQuant`;
            statusBarItem.tooltip = `TRQuant | 市场: ${regime.toUpperCase()}\n点击打开控制面板`;
        }
    } catch (error) {
        // 静默处理错误，保持默认状态
        logger.debug('更新状态栏失败', MODULE, { error });
    }
}

/**
 * 显示欢迎消息
 */
function showWelcomeMessage(context: vscode.ExtensionContext): void {
    const WELCOME_SHOWN_KEY = 'trquant.welcomeShown';
    
    if (!context.globalState.get(WELCOME_SHOWN_KEY)) {
        vscode.window.showInformationMessage(
            '欢迎使用 TRQuant 量化助手！按 Ctrl+Shift+P 输入 "TRQuant" 查看可用命令。',
            '查看命令',
            '不再显示'
        ).then(selection => {
            if (selection === '查看命令') {
                vscode.commands.executeCommand('workbench.action.quickOpen', '>TRQuant');
            } else if (selection === '不再显示') {
                context.globalState.update(WELCOME_SHOWN_KEY, true);
            }
        });
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
