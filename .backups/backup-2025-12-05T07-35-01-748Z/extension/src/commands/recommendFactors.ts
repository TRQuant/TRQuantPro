/**
 * 推荐因子命令
 * ==============
 * 
 * 功能：
 * - 基于市场状态推荐量化因子
 * - 展示因子分类和权重
 * - 生成因子组合建议
 * 
 * 遵循：
 * - 单一职责原则
 * - 命令模式
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';
import { ErrorHandler } from '../utils/errors';
import { Factor, MarketRegime, FactorCategory } from '../types';

const MODULE = 'RecommendFactors';

/**
 * 执行推荐因子命令
 */
export async function recommendFactors(
    client: TRQuantClient,
    context: vscode.ExtensionContext
): Promise<void> {
    logger.info('执行推荐因子命令', MODULE);

    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "TRQuant",
        cancellable: true
    }, async (progress, token) => {
        try {
            progress.report({ message: '获取市场状态...', increment: 0 });

            // 先获取市场状态
            const marketResult = await client.getMarketStatus();
            const regime = marketResult.data?.regime || 'neutral';

            if (token.isCancellationRequested) {
                return;
            }

            progress.report({ message: '推荐因子...', increment: 30 });

            // 获取因子推荐
            const result = await client.recommendFactors({
                market_regime: regime as MarketRegime,
                top_n: 15
            });

            progress.report({ increment: 40 });

            if (!result.ok || !result.data) {
                vscode.window.showErrorMessage(`获取因子推荐失败: ${result.error || '未知错误'}`);
                return;
            }

            const factors = result.data;
            logger.info(`推荐 ${factors.length} 个因子`, MODULE);

            progress.report({ message: '渲染结果...', increment: 20 });

            // 创建WebView显示结果
            createFactorsPanel(context, factors, regime);

            progress.report({ increment: 10 });

            // 提供后续操作
            showFollowUpActions(factors);

        } catch (error) {
            ErrorHandler.handle(error, MODULE);
        }
    });
}

/**
 * 创建因子推荐WebView面板
 */
function createFactorsPanel(
    context: vscode.ExtensionContext,
    factors: Factor[],
    regime: string
): vscode.WebviewPanel {
    const panel = vscode.window.createWebviewPanel(
        'trquantFactors',
        '📈 因子推荐',
        vscode.ViewColumn.Beside,
        {
            enableScripts: true,
            retainContextWhenHidden: true
        }
    );

    panel.webview.html = generateWebviewHtml(factors, regime);

    // 处理WebView消息
    panel.webview.onDidReceiveMessage(
        async (message) => {
            switch (message.command) {
                case 'generateStrategy':
                    const selectedFactors = message.factors || factors.slice(0, 5).map(f => f.name);
                    generateStrategyWithFactors(selectedFactors);
                    break;
                case 'copyPrompt':
                    const prompt = generatePrompt(factors, regime);
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
function generateWebviewHtml(factors: Factor[], regime: string): string {
    const regimeInfo = getRegimeInfo(regime);
    const groupedFactors = groupFactorsByCategory(factors);
    const categoriesHtml = Object.entries(groupedFactors)
        .map(([category, items]) => generateCategorySection(category, items))
        .join('');

    return `<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>因子推荐</title>
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

        .regime-badge {
            background: ${regimeInfo.color};
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
        }

        .info-card {
            background: linear-gradient(135deg, ${regimeInfo.color}22, ${regimeInfo.color}11);
            border-left: 4px solid ${regimeInfo.color};
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 24px;
        }

        .info-card p {
            color: var(--text-secondary);
            font-size: 14px;
        }

        .category-section {
            margin-bottom: 24px;
        }

        .category-title {
            font-size: 15px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .category-title::before {
            content: '';
            width: 4px;
            height: 16px;
            background: var(--primary);
            border-radius: 2px;
        }

        .factors-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 12px;
        }

        .factor-card {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 16px;
            border: 1px solid var(--border);
            cursor: pointer;
            transition: all 0.2s;
        }

        .factor-card:hover {
            border-color: var(--primary);
        }

        .factor-card.selected {
            border-color: var(--success);
            background: var(--success)11;
        }

        .factor-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .factor-name {
            font-weight: 600;
            font-size: 15px;
        }

        .factor-weight {
            background: var(--bg-tertiary);
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
        }

        .weight-high { background: var(--success); color: white; }
        .weight-medium { background: var(--warning); color: #1a1a2e; }
        .weight-low { background: var(--bg-tertiary); color: var(--text-secondary); }

        .factor-reason {
            color: var(--text-secondary);
            font-size: 13px;
            line-height: 1.5;
        }

        .selected-factors {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 24px;
            border: 1px solid var(--border);
        }

        .selected-title {
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 12px;
        }

        .selected-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .selected-tag {
            background: var(--primary);
            color: white;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .selected-tag .remove {
            cursor: pointer;
            opacity: 0.7;
        }

        .selected-tag .remove:hover { opacity: 1; }

        .actions {
            display: flex;
            gap: 12px;
            margin-top: 24px;
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
            <span class="header-icon">📈</span>
            <div>
                <div class="header-title">因子推荐</div>
                <div class="header-subtitle">基于当前市场状态的智能因子推荐</div>
            </div>
        </div>
        <span class="regime-badge">市场: ${regime.toUpperCase()}</span>
    </div>

    <div class="info-card">
        <p>${regimeInfo.factorAdvice}</p>
    </div>

    <div class="selected-factors" id="selectedFactors">
        <div class="selected-title">已选因子 (点击卡片添加/移除)</div>
        <div class="selected-list" id="selectedList"></div>
    </div>

    ${categoriesHtml}

    <div class="actions">
        <button class="btn btn-primary" onclick="generateStrategy()">
            🚀 使用选中因子生成策略
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
        const selectedFactors = new Set();
        
        // 默认选中前5个因子
        const defaultFactors = ${JSON.stringify(factors.slice(0, 5).map(f => f.name))};
        defaultFactors.forEach(f => selectedFactors.add(f));
        updateSelectedDisplay();
        
        function toggleFactor(name, element) {
            if (selectedFactors.has(name)) {
                selectedFactors.delete(name);
                element.classList.remove('selected');
            } else {
                selectedFactors.add(name);
                element.classList.add('selected');
            }
            updateSelectedDisplay();
        }
        
        function removeFactor(name) {
            selectedFactors.delete(name);
            const card = document.querySelector(\`[data-factor="\${name}"]\`);
            if (card) card.classList.remove('selected');
            updateSelectedDisplay();
        }
        
        function updateSelectedDisplay() {
            const list = document.getElementById('selectedList');
            list.innerHTML = Array.from(selectedFactors).map(f => 
                \`<span class="selected-tag">
                    \${f}
                    <span class="remove" onclick="removeFactor('\${f}')">×</span>
                </span>\`
            ).join('');
            
            // 更新卡片状态
            document.querySelectorAll('.factor-card').forEach(card => {
                const factorName = card.getAttribute('data-factor');
                if (selectedFactors.has(factorName)) {
                    card.classList.add('selected');
                }
            });
        }
        
        function generateStrategy() {
            vscode.postMessage({ 
                command: 'generateStrategy',
                factors: Array.from(selectedFactors)
            });
        }
        
        function copyPrompt() {
            vscode.postMessage({ command: 'copyPrompt' });
        }
    </script>
</body>
</html>`;
}

/**
 * 生成分类区块HTML
 */
function generateCategorySection(category: string, factors: Factor[]): string {
    const factorCards = factors.map(f => generateFactorCard(f)).join('');
    
    return `
        <div class="category-section">
            <div class="category-title">${getCategoryIcon(category)} ${category}</div>
            <div class="factors-grid">
                ${factorCards}
            </div>
        </div>
    `;
}

/**
 * 生成单个因子卡片HTML
 */
function generateFactorCard(factor: Factor): string {
    const weightClass = factor.weight > 0.7 ? 'weight-high' : 
                       factor.weight > 0.4 ? 'weight-medium' : 'weight-low';
    
    return `
        <div class="factor-card" data-factor="${factor.name}" onclick="toggleFactor('${factor.name}', this)">
            <div class="factor-header">
                <span class="factor-name">${factor.name}</span>
                <span class="factor-weight ${weightClass}">${(factor.weight * 100).toFixed(0)}%</span>
            </div>
            <div class="factor-reason">${factor.reason || '基于历史表现推荐'}</div>
        </div>
    `;
}

/**
 * 按类别分组因子
 */
function groupFactorsByCategory(factors: Factor[]): Record<string, Factor[]> {
    const groups: Record<string, Factor[]> = {};
    
    for (const factor of factors) {
        const category = factor.category || '其他';
        if (!groups[category]) {
            groups[category] = [];
        }
        groups[category].push(factor);
    }
    
    return groups;
}

/**
 * 获取分类图标
 */
function getCategoryIcon(category: string): string {
    const icons: Record<string, string> = {
        '盈利能力': '💰',
        '成长性': '🚀',
        '估值': '📊',
        '动量': '⚡',
        '流动性': '💧',
        '波动率': '📈',
        '质量': '✨',
        '其他': '📋'
    };
    return icons[category] || '📋';
}

/**
 * 获取市场状态信息
 */
function getRegimeInfo(regime: string): { color: string; factorAdvice: string } {
    const info: Record<string, { color: string; factorAdvice: string }> = {
        'risk_on': {
            color: '#10b981',
            factorAdvice: '当前市场风险偏好上升，建议侧重成长性和动量因子。高Beta、高成长的股票可能表现更好。'
        },
        'risk_off': {
            color: '#ef4444',
            factorAdvice: '当前市场风险偏好下降，建议侧重价值和质量因子。低波动、高分红的股票可能更稳健。'
        },
        'neutral': {
            color: '#f59e0b',
            factorAdvice: '当前市场处于震荡格局，建议均衡配置各类因子。可以考虑市场中性策略降低方向性风险。'
        }
    };
    return info[regime] || info['neutral'];
}

/**
 * 生成AI Prompt
 */
function generatePrompt(factors: Factor[], regime: string): string {
    const groupedFactors = groupFactorsByCategory(factors);
    
    return `# 量化因子推荐

## 市场状态: ${regime.toUpperCase()}

${getRegimeInfo(regime).factorAdvice}

## 推荐因子列表

${Object.entries(groupedFactors).map(([category, items]) => `
### ${category}
${items.map(f => `- **${f.name}** (权重: ${(f.weight * 100).toFixed(0)}%): ${f.reason || ''}`).join('\n')}
`).join('\n')}

---

请基于以上因子推荐，帮我：
1. 分析各因子在当前市场环境下的有效性
2. 设计因子合成方案（权重分配）
3. 生成使用这些因子的PTrade多因子策略代码

要求：
- 因子需要进行标准化处理（Z-score）
- 考虑因子间的相关性
- 包含完整的风控逻辑
`;
}

/**
 * 使用选中因子生成策略
 */
function generateStrategyWithFactors(factors: string[]): void {
    logger.info(`使用因子生成策略: ${factors.join(', ')}`, MODULE);
    vscode.commands.executeCommand('trquant.generateStrategy');
}

/**
 * 显示后续操作选项
 */
async function showFollowUpActions(factors: Factor[]): Promise<void> {
    if (factors.length === 0) {
        return;
    }

    const action = await vscode.window.showInformationMessage(
        `推荐 ${factors.length} 个因子`,
        '生成策略',
        '复制Prompt'
    );

    switch (action) {
        case '生成策略':
            vscode.commands.executeCommand('trquant.generateStrategy');
            break;
        case '复制Prompt':
            const prompt = generatePrompt(factors, 'neutral');
            await vscode.env.clipboard.writeText(prompt);
            vscode.window.showInformationMessage('Prompt已复制到剪贴板');
            break;
    }
}
