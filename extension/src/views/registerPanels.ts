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
import { TRQuantClient } from '../services/trquantClient';

/**
 * 注册所有面板
 */
export function registerPanels(
    context: vscode.ExtensionContext,
    client: TRQuantClient
): void {
    // 9步投资工作流（主命令）
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openWorkflowPanel', () => {
            WorkflowPanel.createOrShow(context.extensionUri, context.extensionPath);
        })
    );

    // 策略生成器 (需要 client 参数)
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openStrategyGenerator', () => {
            StrategyGeneratorPanel.createOrShow(context.extensionUri, client);
        })
    );

    // 回测面板 (需要 client 参数)
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openBacktestPanel', () => {
            BacktestPanel.createOrShow(context.extensionUri, client);
        })
    );

    // 策略优化器 (需要 client 参数)
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openOptimizerPanel', () => {
            OptimizerPanel.createOrShow(context.extensionUri, client);
        })
    );

    // 报告生成 (需要 client 参数)
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.openReportPanel', () => {
            ReportPanel.createOrShow(context.extensionUri, client);
        })
    );
}

export {
    WorkflowPanel,
    StrategyGeneratorPanel,
    BacktestPanel,
    OptimizerPanel,
    ReportPanel
};
