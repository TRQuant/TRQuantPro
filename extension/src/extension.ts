/**
 * TRQuant Cursor Extension
 * 韬睿量化 - A股量化投资助手
 * 
 * 功能：
 * 1. 获取市场状态和投资主线
 * 2. 推荐因子和生成策略
 * 3. 通过MCP协议与Cursor AI集成
 */

import * as vscode from 'vscode';
import { TRQuantClient } from './services/trquantClient';
import { MCPRegistrar } from './services/mcpRegistrar';
import { getMarketStatus } from './commands/getMarketStatus';
import { getMainlines } from './commands/getMainlines';
import { recommendFactors } from './commands/recommendFactors';
import { generateStrategy } from './commands/generateStrategy';
import { analyzeBacktest } from './commands/analyzeBacktest';
import { MarketPanel } from './views/marketPanel';

let client: TRQuantClient;
let statusBarItem: vscode.StatusBarItem;

export async function activate(context: vscode.ExtensionContext) {
    console.log('TRQuant Extension is now active!');

    // 初始化TRQuant客户端
    client = new TRQuantClient(context);
    
    // 创建状态栏项
    statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    statusBarItem.text = "$(graph) TRQuant";
    statusBarItem.tooltip = "TRQuant 量化助手";
    statusBarItem.command = 'trquant.showPanel';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // 注册命令
    const commands = [
        vscode.commands.registerCommand('trquant.getMarketStatus', () => 
            getMarketStatus(client, context)),
        
        vscode.commands.registerCommand('trquant.getMainlines', () => 
            getMainlines(client, context)),
        
        vscode.commands.registerCommand('trquant.recommendFactors', () => 
            recommendFactors(client, context)),
        
        vscode.commands.registerCommand('trquant.generateStrategy', () => 
            generateStrategy(client, context)),
        
        vscode.commands.registerCommand('trquant.analyzeBacktest', () => 
            analyzeBacktest(client, context)),
        
        vscode.commands.registerCommand('trquant.enableMCP', () => 
            enableMCP(context)),
        
        vscode.commands.registerCommand('trquant.showPanel', () => 
            MarketPanel.createOrShow(context.extensionUri, client)),
    ];

    context.subscriptions.push(...commands);

    // 自动注册MCP Server（如果配置启用）
    const config = vscode.workspace.getConfiguration('trquant');
    if (config.get('mcpEnabled')) {
        await MCPRegistrar.registerServer(context);
    }

    // 更新状态栏显示
    updateStatusBar();
}

async function enableMCP(context: vscode.ExtensionContext) {
    try {
        await MCPRegistrar.registerServer(context);
        vscode.window.showInformationMessage('TRQuant MCP Server 已启用');
    } catch (error) {
        vscode.window.showErrorMessage(`启用MCP失败: ${error}`);
    }
}

async function updateStatusBar() {
    try {
        const status = await client.getMarketStatus();
        if (status.ok && status.data) {
            const regime = status.data.regime || 'unknown';
            const regimeIcon = regime === 'risk_on' ? '📈' : 
                              regime === 'risk_off' ? '📉' : '➡️';
            statusBarItem.text = `$(graph) ${regimeIcon} TRQuant`;
            statusBarItem.tooltip = `市场状态: ${regime}`;
        }
    } catch (error) {
        // 静默处理错误，保持默认状态
    }
}

export function deactivate() {
    if (client) {
        client.dispose();
    }
}

