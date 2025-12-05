/**
 * 获取投资主线命令
 * ==================
 * 
 * 功能：
 * - 获取A股当前TOP投资主线
 * - 展示主线相关行业和投资逻辑
 * - 支持不同时间周期筛选
 * 
 * 遵循：
 * - 单一职责原则
 * - 命令模式
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';
import { ErrorHandler } from '../utils/errors';
import { Mainline } from '../types';

const MODULE = 'GetMainlines';

/**
 * 执行获取投资主线命令
 */
export async function getMainlines(
    client: TRQuantClient,
    context: vscode.ExtensionContext
): Promise<void> {
    logger.info('执行获取投资主线命令', MODULE);

    // 让用户选择时间周期
    const timeHorizon = await vscode.window.showQuickPick([
        { label: '📅 短期 (1-5天)', value: 'short', description: '适合短线交易' },
        { label: '📆 中期 (1-4周)', value: 'medium', description: '适合波段操作' },
        { label: '📆 长期 (1月+)', value: 'long', description: '适合价值投资' },
    ], {
        placeHolder: '选择投资周期'
    });

    if (!timeHorizon) {
        return;
    }

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "TRQuant",
        cancellable: true
    }, async (progress, token) => {
        try {
            progress.report({ message: '正在获取投资主线...', increment: 0 });

            if (token.isCancellationRequested) {
                logger.info('用户取消操作', MODULE);
                return;
            }

            const result = await client.getMainlines({
                top_n: 20,
                time_horizon: timeHorizon.value as 'short' | 'medium' | 'long'
            });

            progress.report({ increment: 60 });

            if (!result.ok || !result.data) {
                vscode.window.showErrorMessage(`获取投资主线失败: ${result.error || '未知错误'}`);
                return;
            }

            const mainlines = result.data;
            logger.info(`获取到 ${mainlines.length} 条投资主线`, MODULE);

            progress.report({ message: '渲染结果...', increment: 20 });

            // 创建WebView显示结果
            createMainlinesPanel(context, mainlines, timeHorizon.value);

            progress.report({ increment: 20 });

            // 提供后续操作
            showFollowUpActions(mainlines);

        } catch (error) {
            ErrorHandler.handle(error, MODULE);
        }
    });
}

/**
 * 创建投资主线WebView面板
 */
function createMainlinesPanel(
    context: vscode.ExtensionContext,
    mainlines: Mainline[],
    timeHorizon: string
): vscode.WebviewPanel {
    const panel = vscode.window.createWebviewPanel(
        'trquantMainlines',
        '🎯 投资主线',
        vscode.ViewColumn.Beside,
        {
            enableScripts: true,
            retainContextWhenHidden: true
        }
    );

    panel.webview.html = generateWebviewHtml(mainlines, timeHorizon);

    // 处理WebView消息
    panel.webview.onDidReceiveMessage(
        async (message) => {
            switch (message.command) {
                case 'selectMainline':
                    handleMainlineSelection(message.mainline);
                    break;
                case 'generateStrategy':
                    vscode.commands.executeCommand('trquant.generateStrategy');
                    break;
                case 'copyPrompt':
                    const prompt = generatePrompt(mainlines, timeHorizon);
                    await vscode.env.clipboard.writeText(prompt);
                    vscode.window.showInformationMessage('Prompt已复制到剪贴板');
                    break;
            }
        },
        undefined,
        context.subscriptions
    );

    return panel;
}

/**
 * 生成WebView HTML
 */
function generateWebviewHtml(mainlines: Mainline[], timeHorizon: string): string {
    const timeHorizonText: Record<string, string> = {
        'short': '短期 (1-5天)',
        'medium': '中期 (1-4周)',
        'long': '长期 (1月+)'
    };

    const mainlinesHtml = mainlines.length > 0
        ? mainlines.map((m, i) => generateMainlineCard(m, i)).join('')
        : '<div class="empty-state">暂无投资主线数据</div>';

    return `<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投资主线</title>
    <style>
        :root {
            --bg-primary: #1a1a2e;
            --bg-secondary: #252540;
            --bg-tertiary: #2d2d4a;
            --text-primary: #ffffff;
            --text-secondary: #9ca3af;
            --text-muted: #6b7280;
            --primary: #667eea;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --border: #3d3d5c;
            --gold: #fbbf24;
            --silver: #94a3b8;
            --bronze: #b45309;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 24px;
            line-height: 1.6;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .header-icon { font-size: 36px; }

        .header-title {
            font-size: 24px;
            font-weight: 600;
        }

        .header-subtitle {
            color: var(--text-secondary);
            font-size: 14px;
        }

        .time-badge {
            background: var(--primary);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
        }

        .stats-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        .stat-card {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            border: 1px solid var(--border);
        }

        .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: var(--primary);
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 13px;
            margin-top: 4px;
        }

        .mainlines-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .mainline-card {
            background: var(--bg-secondary);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid var(--border);
            cursor: pointer;
            transition: all 0.2s;
        }

        .mainline-card:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
        }

        .mainline-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .mainline-rank {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .rank-badge {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
        }

        .rank-1 { background: var(--gold); color: #1a1a2e; }
        .rank-2 { background: var(--silver); color: #1a1a2e; }
        .rank-3 { background: var(--bronze); color: white; }
        .rank-default { background: var(--bg-tertiary); color: var(--text-secondary); }

        .mainline-name {
            font-size: 18px;
            font-weight: 600;
        }

        .mainline-score {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .score-bar {
            width: 100px;
            height: 8px;
            background: var(--bg-tertiary);
            border-radius: 4px;
            overflow: hidden;
        }

        .score-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--success));
            border-radius: 4px;
        }

        .score-value {
            font-weight: 600;
            color: var(--success);
            min-width: 50px;
            text-align: right;
        }

        .mainline-industries {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 12px;
        }

        .industry-tag {
            background: var(--bg-tertiary);
            color: var(--text-secondary);
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 12px;
        }

        .mainline-logic {
            color: var(--text-secondary);
            font-size: 14px;
            line-height: 1.6;
            padding-left: 16px;
            border-left: 3px solid var(--primary);
        }

        .actions {
            display: flex;
            gap: 12px;
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid var(--border);
        }

        .btn {
            padding: 12px 24px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
        }

        .btn-primary:hover { background: #5a6fd6; }

        .btn-secondary {
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }

        .btn-secondary:hover { background: #3d3d5c; }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: var(--text-muted);
        }

        .timestamp {
            text-align: center;
            color: var(--text-muted);
            font-size: 12px;
            margin-top: 24px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-left">
            <span class="header-icon">🎯</span>
            <div>
                <div class="header-title">投资主线 TOP ${mainlines.length}</div>
                <div class="header-subtitle">基于市场热度、资金流向、行业景气度综合评估</div>
            </div>
        </div>
        <span class="time-badge">${timeHorizonText[timeHorizon] || timeHorizon}</span>
    </div>

    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-value">${mainlines.length}</div>
            <div class="stat-label">主线数量</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${mainlines.length > 0 ? mainlines[0].score.toFixed(2) : '-'}</div>
            <div class="stat-label">最高评分</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${countUniqueIndustries(mainlines)}</div>
            <div class="stat-label">涉及行业</div>
        </div>
    </div>

    <div class="mainlines-list">
        ${mainlinesHtml}
    </div>

    <div class="actions">
        <button class="btn btn-primary" onclick="generateStrategy()">
            🚀 基于主线生成策略
        </button>
        <button class="btn btn-secondary" onclick="copyPrompt()">
            📋 复制为AI Prompt
        </button>
    </div>

    <div class="timestamp">
        更新时间: ${new Date().toLocaleString('zh-CN')}
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        
        function selectMainline(mainline) {
            vscode.postMessage({ command: 'selectMainline', mainline });
        }
        
        function generateStrategy() {
            vscode.postMessage({ command: 'generateStrategy' });
        }
        
        function copyPrompt() {
            vscode.postMessage({ command: 'copyPrompt' });
        }
    </script>
</body>
</html>`;
}

/**
 * 生成单个主线卡片HTML
 */
function generateMainlineCard(mainline: Mainline, index: number): string {
    const rankClass = index < 3 ? `rank-${index + 1}` : 'rank-default';
    const scoreWidth = Math.min(mainline.score * 100, 100);

    return `
        <div class="mainline-card" onclick="selectMainline('${mainline.name}')">
            <div class="mainline-header">
                <div class="mainline-rank">
                    <div class="rank-badge ${rankClass}">${index + 1}</div>
                    <span class="mainline-name">${mainline.name}</span>
                </div>
                <div class="mainline-score">
                    <div class="score-bar">
                        <div class="score-fill" style="width: ${scoreWidth}%"></div>
                    </div>
                    <span class="score-value">${mainline.score.toFixed(2)}</span>
                </div>
            </div>
            <div class="mainline-industries">
                ${mainline.industries.map(ind => `<span class="industry-tag">${ind}</span>`).join('')}
            </div>
            <div class="mainline-logic">
                💡 ${mainline.logic || '暂无详细说明'}
            </div>
        </div>
    `;
}

/**
 * 统计涉及的行业数量
 */
function countUniqueIndustries(mainlines: Mainline[]): number {
    const industries = new Set<string>();
    mainlines.forEach(m => m.industries.forEach(ind => industries.add(ind)));
    return industries.size;
}

/**
 * 生成AI Prompt
 */
function generatePrompt(mainlines: Mainline[], timeHorizon: string): string {
    const timeHorizonText: Record<string, string> = {
        'short': '短期 (1-5天)',
        'medium': '中期 (1-4周)',
        'long': '长期 (1月+)'
    };

    return `# A股投资主线分析

## 分析周期: ${timeHorizonText[timeHorizon] || timeHorizon}

## TOP ${mainlines.length} 投资主线

${mainlines.map((m, i) => `
### ${i + 1}. ${m.name} (评分: ${m.score.toFixed(2)})
- **相关行业**: ${m.industries.join(', ')}
- **投资逻辑**: ${m.logic || '暂无'}
`).join('\n')}

---

请基于以上投资主线，帮我：
1. 分析当前最值得关注的主线及其原因
2. 推荐适合这些主线的量化因子
3. 生成针对TOP3主线的PTrade量化策略代码

要求：
- 策略应该聚焦于主线相关的股票池
- 包含完整的风控逻辑
- 添加详细的中文注释
`;
}

/**
 * 处理主线选择
 */
function handleMainlineSelection(mainlineName: string): void {
    vscode.window.showInformationMessage(
        `已选择主线: ${mainlineName}`,
        '查看详情',
        '筛选股票'
    ).then(selection => {
        if (selection === '查看详情') {
            // 可以打开详细分析页面
            logger.info(`查看主线详情: ${mainlineName}`, MODULE);
        } else if (selection === '筛选股票') {
            // 可以基于主线筛选股票
            logger.info(`基于主线筛选股票: ${mainlineName}`, MODULE);
        }
    });
}

/**
 * 显示后续操作选项
 */
async function showFollowUpActions(mainlines: Mainline[]): Promise<void> {
    if (mainlines.length === 0) {
        return;
    }

    const action = await vscode.window.showInformationMessage(
        `获取到 ${mainlines.length} 条投资主线`,
        '生成策略',
        '推荐因子',
        '复制Prompt'
    );

    switch (action) {
        case '生成策略':
            vscode.commands.executeCommand('trquant.generateStrategy');
            break;
        case '推荐因子':
            vscode.commands.executeCommand('trquant.recommendFactors');
            break;
        case '复制Prompt':
            const prompt = generatePrompt(mainlines, 'short');
            await vscode.env.clipboard.writeText(prompt);
            vscode.window.showInformationMessage('Prompt已复制到剪贴板');
            break;
    }
}
