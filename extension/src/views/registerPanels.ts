/**
 * 面板注册模块
 * 统一注册所有面板命令
 */

import * as vscode from 'vscode';
import { WorkflowPanel } from './workflowPanel';
import { StrategyGeneratorPanel } from './strategyGeneratorPanel';
import { BacktestPanel } from './backtestPanel';
import { OptimizerPanel } from './optimizerPanel';
import { ReportPanel } from './reportPanel';
import { MonitoringPanel } from './monitoringPanel';
import { ResultManagerPanel } from './resultManagerPanel';
import { TRQuantClient } from '../services/trquantClient';

// 十倍股系统面板
import { TenbaggerDashboardPanel } from './tenbaggerDashboard';
import { IndustryChainPanel } from './industryChainPanel';
import { StockDetailPanel } from './stockDetailPanel';
import { WorkflowPanelMVP } from './workflowPanelMVP';

// React Webview面板
import { ReactPanel } from './ReactPanel';
// 统一仪表板
import { UnifiedDashboard } from './unifiedDashboard';

/**
 * 注册所有面板
 */
export function registerPanels(
    context: vscode.ExtensionContext,
    client: TRQuantClient
): void {
    // ========== 统一仪表板（推荐使用） ==========
    
    // React Webview面板（使用React + Ant Design）
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openReactPanel', () => {
            ReactPanel.createOrShow(context.extensionUri, context.extensionPath);
        })
    );

    // 统一仪表板（整合9步工作流、十倍股、趋势策略）
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openUnifiedDashboard', () => {
            try {
                console.log('[registerPanels] 执行 trquant.openUnifiedDashboard 命令');
                UnifiedDashboard.createOrShow(context.extensionUri, context.extensionPath);
            } catch (error) {
                console.error('[registerPanels] 打开统一仪表板失败:', error);
                vscode.window.showErrorMessage(`打开统一仪表板失败: ${error instanceof Error ? error.message : String(error)}`);
            }
        })
    );

    // ========== 量化投资工作流面板 ==========
    
    // 9步投资工作流（主命令）
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openWorkflowPanel', () => {
            WorkflowPanel.createOrShow(context.extensionUri, context.extensionPath);
        })
    );
    
    // MVP工作流面板 (简化版)
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openWorkflowMVP', () => {
            WorkflowPanelMVP.createOrShow(context.extensionUri, context.extensionPath);
        })
    );

    // 策略生成器
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openStrategyGenerator', () => {
            StrategyGeneratorPanel.createOrShow(context.extensionUri, client);
        })
    );

    // 回测面板
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openBacktestPanel', () => {
            BacktestPanel.createOrShow(context.extensionUri, client);
        })
    );

    // 策略优化器
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openOptimizerPanel', () => {
            OptimizerPanel.createOrShow(context.extensionUri, client);
        })
    );

    // 报告生成
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openReportPanel', (options?: { result?: any }) => {
            ReportPanel.createOrShow(context.extensionUri, client, options);
        })
    );

    // 监控面板
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openMonitoringPanel', () => {
            MonitoringPanel.createOrShow(context.extensionUri, client);
        })
    );

    // 结果管理面板
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openResultManager', () => {
            ResultManagerPanel.createOrShow(context.extensionUri, client);
        })
    );

    // ========== 十倍股早期识别系统面板 ==========
    
    // 十倍股仪表盘 (主面板)
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openTenbaggerDashboard', () => {
            TenbaggerDashboardPanel.createOrShow(context.extensionUri);
        })
    );

    // 产业链图谱
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openIndustryChain', () => {
            IndustryChainPanel.createOrShow(context.extensionUri);
        })
    );

    // 股票详情
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openStockDetail', (symbol?: string) => {
            StockDetailPanel.createOrShow(context.extensionUri, symbol || '300750.SZ');
        })
    );

    // 数据管道命令
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.runDataPipeline', async () => {
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "运行数据管道",
                cancellable: false
            }, async (progress) => {
                progress.report({ message: "爬取数据中..." });
                
                // 调用Python后端
                const terminal = vscode.window.createTerminal('TRQuant Pipeline');
                terminal.show();
                terminal.sendText('cd /home/taotao/dev/QuantTest/TRQuant && source venv/bin/activate');
                terminal.sendText('python3 -c "import sys; sys.path.insert(0, \'mcp_servers\'); from crawlers.pipeline import run_pipeline; print(run_pipeline())"');
                
                return new Promise<void>(resolve => setTimeout(resolve, 3000));
            });
        })
    );

    console.log('[TRQuant] 已注册所有面板命令（量化工作流 + 十倍股系统）');
}

// 兼容旧的导出
export function registerTenbaggerDashboard(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openTenbaggerDashboard', () => {
            TenbaggerDashboardPanel.createOrShow(context.extensionUri);
        })
    );
}

export function registerIndustryChainPanel(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openIndustryChain', () => {
            IndustryChainPanel.createOrShow(context.extensionUri);
        })
    );
}

export function registerStockDetailPanel(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openStockDetail', (symbol: string) => {
            StockDetailPanel.createOrShow(context.extensionUri, symbol || '300750.SZ');
        })
    );
}


// 导出侧栏注册
export { registerSidebarProviders } from './sidebarProvider';
