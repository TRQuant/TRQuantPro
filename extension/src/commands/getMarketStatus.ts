/**
 * 获取市场状态命令
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';

export async function getMarketStatus(
    client: TRQuantClient,
    context: vscode.ExtensionContext
): Promise<void> {
    // 显示进度
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "TRQuant: 获取市场状态...",
        cancellable: false
    }, async (progress) => {
        try {
            const result = await client.getMarketStatus({
                universe: 'CN_EQ',
                as_of: new Date().toISOString().split('T')[0]
            });

            if (!result.ok || !result.data) {
                vscode.window.showErrorMessage(`获取市场状态失败: ${result.error}`);
                return;
            }

            const data = result.data;

            // 构建显示内容
            const content = buildMarketStatusContent(data);

            // 创建WebView显示
            const panel = vscode.window.createWebviewPanel(
                'trquantMarketStatus',
                '📊 市场状态',
                vscode.ViewColumn.Beside,
                { enableScripts: true }
            );

            panel.webview.html = getWebviewContent(data);

            // 同时提供复制Prompt功能
            const copyPrompt = await vscode.window.showInformationMessage(
                `市场状态: ${data.regime}`,
                '复制为Prompt',
                '查看详情'
            );

            if (copyPrompt === '复制为Prompt') {
                const prompt = buildPrompt(data);
                await vscode.env.clipboard.writeText(prompt);
                vscode.window.showInformationMessage('Prompt已复制到剪贴板');
            }

        } catch (error: any) {
            vscode.window.showErrorMessage(`错误: ${error.message}`);
        }
    });
}

function buildMarketStatusContent(data: any): string {
    const lines = [
        `# 市场状态分析`,
        ``,
        `## 市场Regime: ${data.regime}`,
        ``,
        `## 指数趋势`,
    ];

    if (data.index_trend) {
        for (const [index, info] of Object.entries(data.index_trend as Record<string, any>)) {
            lines.push(`- ${index}: ${info.trend} (zscore: ${info.zscore?.toFixed(2)})`);
        }
    }

    lines.push('', '## 风格轮动');
    if (data.style_rotation) {
        for (const style of data.style_rotation) {
            lines.push(`- ${style.style}: ${style.score?.toFixed(2)}`);
        }
    }

    if (data.summary) {
        lines.push('', '## 总结', data.summary);
    }

    return lines.join('\n');
}

function buildPrompt(data: any): string {
    return `
当前A股市场状态分析：

市场Regime: ${data.regime}
${data.regime === 'risk_on' ? '风险偏好上升，适合积极配置成长股' : 
  data.regime === 'risk_off' ? '风险偏好下降，建议防御性配置' : '震荡市场，建议均衡配置'}

指数趋势：
${Object.entries(data.index_trend || {}).map(([k, v]: [string, any]) => 
    `- ${k}: ${v.trend} (动量: ${v.zscore?.toFixed(2)})`
).join('\n')}

风格轮动：
${(data.style_rotation || []).map((s: any) => 
    `- ${s.style}: ${s.score > 0 ? '占优' : '弱势'} (${s.score?.toFixed(2)})`
).join('\n')}

${data.summary || ''}

请基于以上市场状态，帮我生成适合当前市场环境的PTrade策略代码。
`.trim();
}

function getWebviewContent(data: any): string {
    const regimeColor = data.regime === 'risk_on' ? '#10b981' : 
                       data.regime === 'risk_off' ? '#ef4444' : '#f59e0b';
    const regimeIcon = data.regime === 'risk_on' ? '📈' : 
                      data.regime === 'risk_off' ? '📉' : '➡️';

    return `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #1a1a2e;
            color: #fff;
            padding: 20px;
            margin: 0;
        }
        .header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
        }
        .regime-badge {
            background: ${regimeColor};
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
        }
        .card {
            background: #252540;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
        }
        .card h3 {
            margin: 0 0 12px 0;
            color: #9ca3af;
            font-size: 14px;
        }
        .trend-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #333;
        }
        .trend-item:last-child { border: none; }
        .positive { color: #10b981; }
        .negative { color: #ef4444; }
        .summary {
            background: linear-gradient(135deg, #667eea22, #764ba222);
            border-left: 4px solid #667eea;
        }
        .copy-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 16px;
        }
        .copy-btn:hover { background: #5a6fd6; }
    </style>
</head>
<body>
    <div class="header">
        <span style="font-size: 32px;">${regimeIcon}</span>
        <h1 style="margin: 0;">市场状态</h1>
        <span class="regime-badge">${data.regime?.toUpperCase()}</span>
    </div>

    <div class="card">
        <h3>📊 指数趋势</h3>
        ${Object.entries(data.index_trend || {}).map(([k, v]: [string, any]) => `
            <div class="trend-item">
                <span>${k}</span>
                <span class="${v.zscore > 0 ? 'positive' : 'negative'}">
                    ${v.trend} (${v.zscore?.toFixed(2)})
                </span>
            </div>
        `).join('')}
    </div>

    <div class="card">
        <h3>🎯 风格轮动</h3>
        ${(data.style_rotation || []).map((s: any) => `
            <div class="trend-item">
                <span>${s.style}</span>
                <span class="${s.score > 0 ? 'positive' : 'negative'}">
                    ${s.score?.toFixed(2)}
                </span>
            </div>
        `).join('')}
    </div>

    ${data.summary ? `
    <div class="card summary">
        <h3>📝 分析总结</h3>
        <p>${data.summary}</p>
    </div>
    ` : ''}

    <button class="copy-btn" onclick="copyPrompt()">📋 复制为AI Prompt</button>

    <script>
        const vscode = acquireVsCodeApi();
        function copyPrompt() {
            vscode.postMessage({ command: 'copyPrompt' });
        }
    </script>
</body>
</html>`;
}

