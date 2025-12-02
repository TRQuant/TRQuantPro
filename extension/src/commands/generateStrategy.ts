/**
 * 生成策略代码命令
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';

export async function generateStrategy(
    client: TRQuantClient,
    context: vscode.ExtensionContext
): Promise<void> {
    // 让用户选择策略风格
    const style = await vscode.window.showQuickPick([
        { label: '📈 多因子选股', value: 'multi_factor', description: '基于因子评分选股' },
        { label: '🚀 动量成长', value: 'momentum_growth', description: '追逐强势成长股' },
        { label: '💰 价值投资', value: 'value', description: '低估值高分红' },
        { label: '⚖️ 市场中性', value: 'market_neutral', description: '多空对冲' },
    ], {
        placeHolder: '选择策略风格'
    });

    if (!style) return;

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "TRQuant: 生成策略代码...",
        cancellable: false
    }, async (progress) => {
        try {
            progress.report({ message: '获取市场状态...' });
            const marketStatus = await client.getMarketStatus();

            progress.report({ message: '获取因子推荐...' });
            const factors = await client.recommendFactors({
                market_regime: marketStatus.data?.regime
            });

            progress.report({ message: '生成策略代码...' });
            const result = await client.generateStrategy({
                factors: (factors.data || []).slice(0, 5).map((f: any) => f.name),
                style: style.value,
                risk_params: {
                    max_position: 0.1,
                    stop_loss: 0.08,
                    take_profit: 0.2
                }
            });

            if (!result.ok || !result.data) {
                vscode.window.showErrorMessage(`生成策略失败: ${result.error}`);
                return;
            }

            const strategy = result.data;

            // 创建新文件显示策略代码
            const doc = await vscode.workspace.openTextDocument({
                content: strategy.code,
                language: 'python'
            });

            await vscode.window.showTextDocument(doc, vscode.ViewColumn.One);

            // 询问是否保存
            const save = await vscode.window.showInformationMessage(
                `策略 "${strategy.name}" 已生成`,
                '保存到PTrade目录',
                '复制代码'
            );

            if (save === '保存到PTrade目录') {
                const uri = await vscode.window.showSaveDialog({
                    defaultUri: vscode.Uri.file(`${strategy.name}.py`),
                    filters: { 'Python': ['py'] }
                });
                if (uri) {
                    await vscode.workspace.fs.writeFile(uri, Buffer.from(strategy.code));
                    vscode.window.showInformationMessage(`策略已保存: ${uri.fsPath}`);
                }
            } else if (save === '复制代码') {
                await vscode.env.clipboard.writeText(strategy.code);
                vscode.window.showInformationMessage('策略代码已复制到剪贴板');
            }

        } catch (error: any) {
            vscode.window.showErrorMessage(`错误: ${error.message}`);
        }
    });
}

