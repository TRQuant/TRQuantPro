/**
 * 生成策略代码命令
 * ==================
 * 
 * 功能：
 * - 支持PTrade和QMT双平台
 * - 4种策略风格选择
 * - 基于市场状态和因子自动生成策略
 * - 完整风控参数配置
 * 
 * 遵循：
 * - 单一职责原则
 * - 策略模式
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { logger } from '../utils/logger';
import { ErrorHandler } from '../utils/errors';
import { config } from '../utils/config';
import { Strategy, StrategyPlatform, StrategyStyle, RiskParams } from '../types';

const MODULE = 'GenerateStrategy';

/**
 * 平台选项
 */
const PLATFORM_OPTIONS = [
    { 
        label: '📊 PTrade (恒生)', 
        value: 'ptrade' as StrategyPlatform, 
        description: '恒生PTrade平台，支持A股、ETF交易',
        detail: '函数: initialize(), handle_data()'
    },
    { 
        label: '📈 QMT (迅投)', 
        value: 'qmt' as StrategyPlatform, 
        description: '迅投QMT平台，支持股票、期货交易',
        detail: '函数: init(), handlebar()'
    }
];

/**
 * 策略风格选项
 */
const STYLE_OPTIONS = [
    { 
        label: '📈 多因子选股', 
        value: 'multi_factor' as StrategyStyle, 
        description: '综合多个因子评分选股',
        detail: '适合: 各种市场环境'
    },
    { 
        label: '🚀 动量成长', 
        value: 'momentum_growth' as StrategyStyle, 
        description: '追逐强势成长股',
        detail: '适合: 牛市、风险偏好上升'
    },
    { 
        label: '💰 价值投资', 
        value: 'value' as StrategyStyle, 
        description: '低估值高分红标的',
        detail: '适合: 熊市、风险偏好下降'
    },
    { 
        label: '⚖️ 市场中性', 
        value: 'market_neutral' as StrategyStyle, 
        description: '多空对冲策略',
        detail: '适合: 震荡市、不确定环境'
    }
];

/**
 * 执行生成策略命令
 */
export async function generateStrategy(
    client: TRQuantClient,
    context: vscode.ExtensionContext
): Promise<void> {
    logger.info('执行生成策略命令', MODULE);

    try {
        // Step 1: 选择平台
        const platform = await selectPlatform();
        if (!platform) return;

        // Step 2: 选择策略风格
        const style = await selectStyle();
        if (!style) return;

        // Step 3: 配置风控参数
        const riskParams = await configureRiskParams();
        if (!riskParams) return;

        // Step 4: 生成策略
        await generateStrategyWithProgress(client, context, platform, style, riskParams);

    } catch (error) {
        ErrorHandler.handle(error, MODULE);
    }
}

/**
 * 选择平台
 */
async function selectPlatform(): Promise<StrategyPlatform | undefined> {
    const selected = await vscode.window.showQuickPick(PLATFORM_OPTIONS, {
        placeHolder: '选择策略平台',
        title: 'Step 1/3: 选择目标平台'
    });
    return selected?.value;
}

/**
 * 选择策略风格
 */
async function selectStyle(): Promise<StrategyStyle | undefined> {
    const selected = await vscode.window.showQuickPick(STYLE_OPTIONS, {
        placeHolder: '选择策略风格',
        title: 'Step 2/3: 选择策略风格'
    });
    return selected?.value;
}

/**
 * 配置风控参数
 */
async function configureRiskParams(): Promise<RiskParams | undefined> {
    const useDefault = await vscode.window.showQuickPick([
        { label: '✅ 使用默认参数', value: 'default', description: '止损8%, 止盈20%, 单票10%' },
        { label: '⚙️ 自定义参数', value: 'custom', description: '手动配置风控参数' }
    ], {
        placeHolder: '风控参数配置',
        title: 'Step 3/3: 配置风控参数'
    });

    if (!useDefault) return undefined;

    if (useDefault.value === 'default') {
        return {
            max_position: 0.1,
            stop_loss: 0.08,
            take_profit: 0.2
        };
    }

    // 自定义参数
    const maxPosition = await vscode.window.showInputBox({
        prompt: '单票最大仓位 (%)',
        value: '10',
        validateInput: (v) => {
            const n = parseFloat(v);
            if (isNaN(n) || n <= 0 || n > 100) {
                return '请输入1-100之间的数字';
            }
            return null;
        }
    });
    if (!maxPosition) return undefined;

    const stopLoss = await vscode.window.showInputBox({
        prompt: '止损线 (%)',
        value: '8',
        validateInput: (v) => {
            const n = parseFloat(v);
            if (isNaN(n) || n <= 0 || n > 50) {
                return '请输入1-50之间的数字';
            }
            return null;
        }
    });
    if (!stopLoss) return undefined;

    const takeProfit = await vscode.window.showInputBox({
        prompt: '止盈线 (%)',
        value: '20',
        validateInput: (v) => {
            const n = parseFloat(v);
            if (isNaN(n) || n <= 0 || n > 100) {
                return '请输入1-100之间的数字';
            }
            return null;
        }
    });
    if (!takeProfit) return undefined;

    return {
        max_position: parseFloat(maxPosition) / 100,
        stop_loss: parseFloat(stopLoss) / 100,
        take_profit: parseFloat(takeProfit) / 100
    };
}

/**
 * 带进度条生成策略
 */
async function generateStrategyWithProgress(
    client: TRQuantClient,
    context: vscode.ExtensionContext,
    platform: StrategyPlatform,
    style: StrategyStyle,
    riskParams: RiskParams
): Promise<void> {
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "TRQuant",
        cancellable: true
    }, async (progress, token) => {
        try {
            // Step 1: 获取市场状态
            progress.report({ message: '获取市场状态...', increment: 0 });
            const marketResult = await client.getMarketStatus();
            
            if (token.isCancellationRequested) return;

            // Step 2: 获取推荐因子
            progress.report({ message: '获取推荐因子...', increment: 20 });
            const factorsResult = await client.recommendFactors({
                market_regime: marketResult.data?.regime
            });

            if (token.isCancellationRequested) return;

            // Step 3: 生成策略代码
            progress.report({ message: `生成${platform.toUpperCase()}策略代码...`, increment: 30 });
            
            const factors = (factorsResult.data || [])
                .slice(0, 5)
                .map(f => f.name);

            const result = await client.generateStrategy({
                factors,
                style,
                platform,
                risk_params: riskParams
            });

            progress.report({ increment: 30 });

            if (!result.ok || !result.data) {
                vscode.window.showErrorMessage(`生成策略失败: ${result.error || '未知错误'}`);
                return;
            }

            const strategy = result.data;
            logger.info(`策略生成成功: ${strategy.name}`, MODULE);

            progress.report({ message: '完成', increment: 20 });

            // 显示策略代码
            await showStrategyCode(context, strategy, platform);

        } catch (error) {
            ErrorHandler.handle(error, MODULE);
        }
    });
}

/**
 * 显示策略代码
 */
async function showStrategyCode(
    context: vscode.ExtensionContext,
    strategy: Strategy,
    platform: StrategyPlatform
): Promise<void> {
    // 创建新文档显示代码
    const doc = await vscode.workspace.openTextDocument({
        content: strategy.code,
        language: 'python'
    });

    await vscode.window.showTextDocument(doc, vscode.ViewColumn.One);

    // 提供操作选项
    const action = await vscode.window.showInformationMessage(
        `${platform.toUpperCase()} 策略 "${strategy.name}" 已生成`,
        '保存文件',
        '复制代码',
        '查看说明'
    );

    switch (action) {
        case '保存文件':
            await saveStrategy(strategy, platform);
            break;
        case '复制代码':
            await vscode.env.clipboard.writeText(strategy.code);
            vscode.window.showInformationMessage('策略代码已复制到剪贴板');
            break;
        case '查看说明':
            showStrategyInfo(strategy);
            break;
    }
}

/**
 * 保存策略文件
 */
async function saveStrategy(strategy: Strategy, platform: StrategyPlatform): Promise<void> {
    const defaultName = `${strategy.name}.py`;
    
    const uri = await vscode.window.showSaveDialog({
        defaultUri: vscode.Uri.file(defaultName),
        filters: {
            'Python文件': ['py']
        },
        title: `保存${platform.toUpperCase()}策略`
    });

    if (uri) {
        await vscode.workspace.fs.writeFile(uri, Buffer.from(strategy.code, 'utf-8'));
        
        // 同时保存元数据
        const metaUri = vscode.Uri.file(uri.fsPath.replace('.py', '_meta.json'));
        const meta = {
            name: strategy.name,
            platform: strategy.platform,
            style: strategy.style,
            factors: strategy.factors,
            risk_params: strategy.risk_params,
            created_at: new Date().toISOString()
        };
        await vscode.workspace.fs.writeFile(metaUri, Buffer.from(JSON.stringify(meta, null, 2), 'utf-8'));
        
        vscode.window.showInformationMessage(`策略已保存: ${uri.fsPath}`);
        logger.info(`策略保存到: ${uri.fsPath}`, MODULE);
    }
}

/**
 * 显示策略说明
 */
function showStrategyInfo(strategy: Strategy): void {
    const styleNames: Record<StrategyStyle, string> = {
        'multi_factor': '多因子选股',
        'momentum_growth': '动量成长',
        'value': '价值投资',
        'market_neutral': '市场中性'
    };

    const info = `
# 策略说明

## 基本信息
- **策略名称**: ${strategy.name}
- **目标平台**: ${strategy.platform.toUpperCase()}
- **策略风格**: ${styleNames[strategy.style]}

## 使用因子
${strategy.factors.map(f => `- ${f}`).join('\n')}

## 风控参数
- **单票最大仓位**: ${(strategy.risk_params.max_position * 100).toFixed(0)}%
- **止损线**: ${(strategy.risk_params.stop_loss * 100).toFixed(0)}%
- **止盈线**: ${(strategy.risk_params.take_profit * 100).toFixed(0)}%

## 策略描述
${strategy.description}

## 使用说明
1. 将代码复制到${strategy.platform.toUpperCase()}客户端
2. 根据实际情况调整股票池和参数
3. 进行回测验证后再实盘使用
4. 注意风险控制，不要超过承受能力
    `;

    // 创建Markdown文档显示
    vscode.workspace.openTextDocument({
        content: info,
        language: 'markdown'
    }).then(doc => {
        vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
    });
}
