/**
 * TRQuant 工作流步骤面板
 * ========================
 * 
 * 统一的工作流步骤面板，支持8个步骤的不同视图
 */

import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
import { DataUpdateService } from '../services/dataUpdateService';
import { logger } from '../utils/logger';
import { MarketStatus, Mainline, Factor } from '../types';

const MODULE = 'WorkflowStepPanel';

/**
 * Webview 消息接口
 */
interface WebviewMessage {
    command: string;
    step?: WorkflowStep;
    commandId?: string;
    dataType?: string;
    criteria?: Record<string, unknown>;
    step_id?: string;
    [key: string]: unknown;
}

export type WorkflowStep = 
    | 'data-center'      // 步骤1: 数据中心
    | 'market-analysis'  // 步骤2: 市场分析
    | 'mainlines'        // 步骤3: 投资主线
    | 'candidate-pool'   // 步骤4: 候选池
    | 'factor-center'    // 步骤5: 因子中心
    | 'strategy-dev'     // 步骤6: 策略开发
    | 'backtest-center'  // 步骤7: 回测中心
    | 'trading-center';  // 步骤8: 交易中心

interface StepConfig {
    id: WorkflowStep;
    title: string;
    icon: string;
    description: string;
    step: number;
}

const STEP_CONFIGS: Record<WorkflowStep, StepConfig> = {
    'data-center': {
        id: 'data-center',
        title: '📡 数据中心',
        icon: '📡',
        description: '更新数据库和知识库到最新状态',
        step: 1
    },
    'market-analysis': {
        id: 'market-analysis',
        title: '📈 市场分析',
        icon: '📈',
        description: '分析当前市场环境和趋势',
        step: 2
    },
    'mainlines': {
        id: 'mainlines',
        title: '🔥 投资主线',
        icon: '🔥',
        description: '识别当前市场热点和投资主线',
        step: 3
    },
    'candidate-pool': {
        id: 'candidate-pool',
        title: '📦 候选池',
        icon: '📦',
        description: '基于分析构建股票候选池',
        step: 4
    },
    'factor-center': {
        id: 'factor-center',
        title: '📊 因子中心',
        icon: '📊',
        description: '构建和优化量化因子',
        step: 5
    },
    'strategy-dev': {
        id: 'strategy-dev',
        title: '🛠️ 策略开发',
        icon: '🛠️',
        description: '开发和优化量化交易策略',
        step: 6
    },
    'backtest-center': {
        id: 'backtest-center',
        title: '🔄 回测中心',
        icon: '🔄',
        description: '验证策略在历史数据上的表现',
        step: 7
    },
    'trading-center': {
        id: 'trading-center',
        title: '🚀 交易中心',
        icon: '🚀',
        description: '实盘模拟和实盘交易',
        step: 8
    }
};

export class WorkflowStepPanel {
    private static panels: Map<WorkflowStep, WorkflowStepPanel> = new Map();
    
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _client: TRQuantClient;
    private readonly _step: WorkflowStep;
    private _disposables: vscode.Disposable[] = [];

    // 缓存数据
    private _marketStatus: MarketStatus | null = null;
    private _mainlines: Mainline[] = [];
    private _factors: Factor[] = [];
    private _candidates: unknown[] = [];

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        client: TRQuantClient,
        step: WorkflowStep
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._client = client;
        this._step = step;

        this._panel.webview.onDidReceiveMessage(
            message => this.handleMessage(message),
            null,
            this._disposables
        );

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        
        this.updateContent();
        this.loadData();
    }

    public static createOrShow(
        extensionUri: vscode.Uri,
        client: TRQuantClient,
        step: WorkflowStep
    ): WorkflowStepPanel {
        const column = vscode.ViewColumn.One;
        const config = STEP_CONFIGS[step];

        // 复用已存在的面板
        if (WorkflowStepPanel.panels.has(step)) {
            const panel = WorkflowStepPanel.panels.get(step)!;
            panel._panel.reveal(column);
            return panel;
        }

        const panel = vscode.window.createWebviewPanel(
            `trquant-${step}`,
            `${config.icon} ${config.title}`,
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        const instance = new WorkflowStepPanel(panel, extensionUri, client, step);
        WorkflowStepPanel.panels.set(step, instance);
        return instance;
    }

    private async handleMessage(message: WebviewMessage): Promise<void> {
        console.log(`[${MODULE}] 收到消息:`, message.command);
        
        switch (message.command) {
            case 'refresh':
                await this.loadData();
                break;
            case 'navigateStep': {
                const targetStep = message.step as WorkflowStep;
                WorkflowStepPanel.createOrShow(this._extensionUri, this._client, targetStep);
                break;
            }
            case 'executeCommand':
                if (message.commandId) {
                    vscode.commands.executeCommand(message.commandId);
                }
                break;
            case 'updateData':
                await this.updateData(message.dataType);
                break;
            case 'testJQAuth':
                await this.testJQAuth();
                break;
            case 'filterCandidates': {
                await this.filterCandidates(message.criteria);
                break;
            }
            case 'recommendFactors':
                await this.recommendFactors();
                break;
            case 'runBacktest':
                vscode.commands.executeCommand('trquant.runBacktest');
                break;
            case 'run_workflow_step': {
                await this.runWorkflowStep(message.step_id || '');
                break;
            }
            default:
                logger.warn(`未知命令: ${message.command}`, MODULE);
        }
    }

    private async loadData(): Promise<void> {
        try {
            switch (this._step) {
                case 'market-analysis':
                case 'data-center': {
                    const marketResult = await this._client.getMarketStatus({});
                    if (marketResult.ok && marketResult.data) {
                        this._marketStatus = marketResult.data;
                    }
                    break;
                }
                case 'mainlines': {
                    const mainlinesResult = await this._client.getMainlines({ top_n: 10 });
                    if (mainlinesResult.ok && mainlinesResult.data) {
                        this._mainlines = mainlinesResult.data;
                    }
                    break;
                }
                case 'factor-center': {
                    const regime = this._marketStatus?.regime || 'neutral';
                    const factorsResult = await this._client.recommendFactors({ market_regime: regime, top_n: 10 });
                    if (factorsResult.ok && factorsResult.data) {
                        this._factors = factorsResult.data;
                    }
                    break;
                }
            }
            this.updateContent();
        } catch (error) {
            logger.error(`加载数据失败: ${error}`, MODULE);
        }
    }

    private async updateData(dataType?: string): Promise<void> {
        const updateService = DataUpdateService.getInstance();
        
        // 显示进度
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: '🔄 数据更新',
            cancellable: false
        }, async (progress) => {
            try {
                progress.report({ increment: 0, message: '正在更新数据...' });
                
                let result;
                if (dataType === 'financial') {
                    result = await updateService.updateFinancialData();
                } else if (dataType === 'market') {
                    result = await updateService.updateMarketData();
                } else {
                    // 默认更新行情数据
                    result = await updateService.updateMarketData();
                }
                
                progress.report({ increment: 100, message: '完成' });
                
                if (result.success) {
                    vscode.window.showInformationMessage(`✅ ${result.message}`, '查看详情').then(selection => {
                        if (selection === '查看详情') {
                            const outputChannel = vscode.window.createOutputChannel('TRQuant 数据更新');
                            outputChannel.appendLine(result.message);
                            if (result.details) {
                                outputChannel.appendLine('\n详细信息:');
                                const detailsStr = typeof result.details === 'string' 
                                    ? result.details 
                                    : JSON.stringify(result.details, null, 2);
                                outputChannel.appendLine(detailsStr);
                            }
                            outputChannel.show();
                        }
                    });
                } else {
                    vscode.window.showErrorMessage(`❌ ${result.message}`, '查看详情').then(selection => {
                        if (selection === '查看详情') {
                            const outputChannel = vscode.window.createOutputChannel('TRQuant 数据更新');
                            outputChannel.appendLine(result.message);
                            if (result.details) {
                                outputChannel.appendLine('\n错误详情:');
                                const detailsStr = typeof result.details === 'string' 
                                    ? result.details 
                                    : JSON.stringify(result.details, null, 2);
                                outputChannel.appendLine(detailsStr);
                            }
                            outputChannel.show();
                        }
                    });
                }
                
                // 刷新数据
                await this.loadData();
            } catch (error) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                vscode.window.showErrorMessage(`数据更新失败: ${errorMsg}`);
            }
        });
    }

    private async testJQAuth(): Promise<void> {
        const updateService = DataUpdateService.getInstance();
        
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: '🔐 测试聚宽认证',
            cancellable: false
        }, async (progress) => {
            try {
                progress.report({ increment: 0, message: '正在测试认证...' });
                
                const result = await updateService.testJQAuth();
                
                progress.report({ increment: 100, message: '完成' });
                
                if (result.success) {
                    vscode.window.showInformationMessage(`✅ ${result.message}`, '查看详情').then(selection => {
                        if (selection === '查看详情') {
                            const outputChannel = vscode.window.createOutputChannel('TRQuant 认证测试');
                            outputChannel.appendLine(result.message);
                            if (result.details) {
                                outputChannel.appendLine('\n详细信息:');
                                const detailsStr = typeof result.details === 'string' 
                                    ? result.details 
                                    : JSON.stringify(result.details, null, 2);
                                outputChannel.appendLine(detailsStr);
                            }
                            outputChannel.show();
                        }
                    });
                } else {
                    vscode.window.showErrorMessage(`❌ ${result.message}`, '查看详情', '打开配置').then(selection => {
                        if (selection === '查看详情') {
                            const outputChannel = vscode.window.createOutputChannel('TRQuant 认证测试');
                            outputChannel.appendLine(result.message);
                            if (result.details) {
                                outputChannel.appendLine('\n错误详情:');
                                const detailsStr = typeof result.details === 'string' 
                                    ? result.details 
                                    : JSON.stringify(result.details, null, 2);
                                outputChannel.appendLine(detailsStr);
                            }
                            outputChannel.show();
                        } else if (selection === '打开配置') {
                            // 打开配置文件
                            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
                            if (workspaceFolder) {
                                const configPath = vscode.Uri.joinPath(workspaceFolder.uri, 'config', 'jqdata_config.json');
                                vscode.window.showTextDocument(configPath);
                            }
                        }
                    });
                }
            } catch (error) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                vscode.window.showErrorMessage(`认证测试失败: ${errorMsg}`);
            }
        });
    }

    private async filterCandidates(_criteria?: Record<string, unknown>): Promise<void> {
        // TODO: 实现候选池筛选逻辑
        vscode.window.showInformationMessage('🔍 正在筛选候选股票...');
    }

    private async recommendFactors(): Promise<void> {
        const regime = this._marketStatus?.regime || 'neutral';
        const result = await this._client.recommendFactors({ market_regime: regime, top_n: 10 });
        if (result.ok && result.data) {
            this._factors = result.data;
            this.updateContent();
            vscode.window.showInformationMessage('✅ 因子推荐完成');
        }
    }

    private async runWorkflowStep(stepId: string): Promise<void> {
        if (!stepId) {
            vscode.window.showErrorMessage('❌ 缺少步骤ID');
            return;
        }

        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: `🔄 执行工作流步骤: ${stepId}`,
            cancellable: false
        }, async (progress) => {
            try {
                progress.report({ increment: 0, message: '正在执行...' });
                
                // 调用Python Bridge执行工作流步骤
                const response = await this._client.callBridge('run_workflow_step', {
                    step_id: stepId
                });

                progress.report({ increment: 100, message: '完成' });

                interface WorkflowStepResponse {
                    ok: boolean;
                    summary?: string;
                    data?: unknown;
                    error?: string;
                }

                const resp = response as WorkflowStepResponse;
                if (response.ok) {
                    const summary = resp.summary || '执行成功';
                    vscode.window.showInformationMessage(`✅ ${summary}`, '查看详情').then(selection => {
                        if (selection === '查看详情') {
                            const outputChannel = vscode.window.createOutputChannel('TRQuant 工作流');
                            outputChannel.appendLine(`步骤: ${stepId}`);
                            outputChannel.appendLine(`结果: ${summary}`);
                            if (resp.data) {
                                outputChannel.appendLine('\n详细信息:');
                                outputChannel.appendLine(JSON.stringify(resp.data, null, 2));
                            }
                            outputChannel.show();
                        }
                    });
                    
                    // 刷新数据
                    await this.loadData();
                } else {
                    const errorMsg = resp.error || '执行失败';
                    vscode.window.showErrorMessage(`❌ ${errorMsg}`, '查看详情').then(selection => {
                        if (selection === '查看详情') {
                            const outputChannel = vscode.window.createOutputChannel('TRQuant 工作流');
                            outputChannel.appendLine(`步骤: ${stepId}`);
                            outputChannel.appendLine(`错误: ${errorMsg}`);
                            outputChannel.show();
                        }
                    });
                }
            } catch (error) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                vscode.window.showErrorMessage(`工作流步骤执行失败: ${errorMsg}`);
                logger.error(`工作流步骤执行失败: ${error}`, MODULE);
            }
        });
    }

    private updateContent(): void {
        this._panel.webview.html = this.generateHtml();
    }

    private generateHtml(): string {
        const config = STEP_CONFIGS[this._step];
        
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${config.title}</title>
    <style>
        ${this.getStyles()}
    </style>
</head>
<body>
    <div class="container">
        <!-- 顶部导航 -->
        <div class="workflow-nav">
            ${this.renderWorkflowNav()}
        </div>
        
        <!-- 页面头部 -->
        <div class="page-header">
            <div class="header-content">
                <div class="step-badge">步骤 ${config.step}</div>
                <h1>${config.title}</h1>
                <p class="description">${config.description}</p>
            </div>
            <div class="header-actions">
                <button class="btn btn-primary" onclick="refresh()">
                    🔄 刷新数据
                </button>
                ${config.step < 8 ? `
                <button class="btn btn-secondary" onclick="navigateStep('${this.getNextStep()}')">
                    下一步 ▶
                </button>` : ''}
            </div>
        </div>
        
        <!-- 主内容区 -->
        <div class="main-content">
            ${this.renderStepContent()}
        </div>
        
        <!-- 底部操作区 -->
        <div class="footer">
            ${this.renderFooterActions()}
        </div>
    </div>
    
    <script>
        const vscode = acquireVsCodeApi();
        
        function refresh() {
            vscode.postMessage({ command: 'refresh' });
        }
        
        function navigateStep(step) {
            vscode.postMessage({ command: 'navigateStep', step: step });
        }
        
        function executeCommand(commandId) {
            vscode.postMessage({ command: 'executeCommand', commandId: commandId });
        }
        
        function updateData(dataType) {
            vscode.postMessage({ command: 'updateData', dataType: dataType });
        }
        
        function testJQAuth() {
            vscode.postMessage({ command: 'testJQAuth' });
        }
        
        function filterCandidates(criteria) {
            vscode.postMessage({ command: 'filterCandidates', criteria: criteria });
        }
        
        function recommendFactors() {
            vscode.postMessage({ command: 'recommendFactors' });
        }
    </script>
</body>
</html>`;
    }

    private renderWorkflowNav(): string {
        const steps: WorkflowStep[] = [
            'data-center', 'market-analysis', 'mainlines', 'candidate-pool',
            'factor-center', 'strategy-dev', 'backtest-center', 'trading-center'
        ];
        
        return steps.map((step, index) => {
            const config = STEP_CONFIGS[step];
            const isActive = step === this._step;
            const isPast = index < steps.indexOf(this._step);
            
            return `
                <div class="nav-step ${isActive ? 'active' : ''} ${isPast ? 'past' : ''}" 
                     onclick="navigateStep('${step}')">
                    <span class="step-number">${index + 1}</span>
                    <span class="step-icon">${config.icon}</span>
                </div>
            `;
        }).join('<div class="nav-connector"></div>');
    }

    private renderStepContent(): string {
        switch (this._step) {
            case 'data-center':
                return this.renderDataCenterContent();
            case 'market-analysis':
                return this.renderMarketAnalysisContent();
            case 'mainlines':
                return this.renderMainlinesContent();
            case 'candidate-pool':
                return this.renderCandidatePoolContent();
            case 'factor-center':
                return this.renderFactorCenterContent();
            case 'strategy-dev':
                return this.renderStrategyDevContent();
            case 'backtest-center':
                return this.renderBacktestCenterContent();
            case 'trading-center':
                return this.renderTradingCenterContent();
            default:
                return '<div class="empty-state">功能开发中...</div>';
        }
    }

    private renderDataCenterContent(): string {
        return `
            <div class="grid-2">
                <div class="card">
                    <div class="card-header">
                        <h3>📊 数据源状态</h3>
                    </div>
                    <div class="card-body">
                        <div class="status-list">
                            <div class="status-item">
                                <span class="status-icon success">✓</span>
                                <span>日线数据</span>
                                <span class="status-time">最后更新: 今天 15:30</span>
                            </div>
                            <div class="status-item">
                                <span class="status-icon success">✓</span>
                                <span>分钟数据</span>
                                <span class="status-time">最后更新: 今天 15:30</span>
                            </div>
                            <div class="status-item">
                                <span class="status-icon warning">!</span>
                                <span>财务数据</span>
                                <span class="status-time">最后更新: 昨天</span>
                            </div>
                            <div class="status-item">
                                <span class="status-icon success">✓</span>
                                <span>基础信息</span>
                                <span class="status-time">最后更新: 今天</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h3>📚 知识库</h3>
                    </div>
                    <div class="card-body">
                        <div class="knowledge-stats">
                            <div class="stat-item">
                                <div class="stat-value">156</div>
                                <div class="stat-label">策略模式</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">89</div>
                                <div class="stat-label">因子定义</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">45</div>
                                <div class="stat-label">回测案例</div>
                            </div>
                        </div>
                        <button class="btn btn-outline" onclick="executeCommand('trquant.openKnowledgeBase')">
                            管理知识库
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h3>🔄 数据更新操作</h3>
                </div>
                <div class="card-body">
                    <div class="action-grid">
                        <button class="action-btn" onclick="updateData('market')">
                            <span class="action-icon">📈</span>
                            <span class="action-text">更新行情数据</span>
                        </button>
                        <button class="action-btn" onclick="updateData('financial')">
                            <span class="action-icon">📋</span>
                            <span class="action-text">更新财务数据</span>
                        </button>
                        <button class="action-btn" onclick="testJQAuth()">
                            <span class="action-icon">🔐</span>
                            <span class="action-text">测试聚宽认证</span>
                        </button>
                        <button class="action-btn" onclick="executeCommand('trquant.openKnowledgeBase')">
                            <span class="action-icon">📚</span>
                            <span class="action-text">管理知识库</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    private renderMarketAnalysisContent(): string {
        const regime: string = this._marketStatus?.regime || 'neutral';
        const regimeTextMap: Record<string, string> = { 'risk_on': '风险偏好', 'risk_off': '避险', 'neutral': '震荡' };
        const regimeColorMap: Record<string, string> = { 'risk_on': '#3fb950', 'risk_off': '#f85149', 'neutral': '#f0b429' };
        const regimeText = regimeTextMap[regime] || regime;
        const regimeColor = regimeColorMap[regime] || '#f0b429';
        
        return `
            <div class="market-overview">
                <div class="regime-card" style="border-color: ${regimeColor}">
                    <div class="regime-icon">${regime === 'risk_on' ? '📈' : regime === 'risk_off' ? '📉' : '➡️'}</div>
                    <div class="regime-info">
                        <div class="regime-label">当前市场状态</div>
                        <div class="regime-value" style="color: ${regimeColor}">${regimeText}</div>
                    </div>
                </div>
            </div>
            
            <div class="grid-3">
                <div class="index-card">
                    <div class="index-name">上证指数</div>
                    <div class="index-value">3,245.67</div>
                    <div class="index-change positive">+0.85%</div>
                </div>
                <div class="index-card">
                    <div class="index-name">深证成指</div>
                    <div class="index-value">10,567.89</div>
                    <div class="index-change positive">+1.23%</div>
                </div>
                <div class="index-card">
                    <div class="index-name">创业板指</div>
                    <div class="index-value">2,156.34</div>
                    <div class="index-change negative">-0.45%</div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h3>📊 板块轮动</h3>
                </div>
                <div class="card-body">
                    <div class="sector-list">
                        <div class="sector-item">
                            <span class="sector-rank">1</span>
                            <span class="sector-name">人工智能</span>
                            <span class="sector-change positive">+3.45%</span>
                        </div>
                        <div class="sector-item">
                            <span class="sector-rank">2</span>
                            <span class="sector-name">半导体</span>
                            <span class="sector-change positive">+2.89%</span>
                        </div>
                        <div class="sector-item">
                            <span class="sector-rank">3</span>
                            <span class="sector-name">新能源车</span>
                            <span class="sector-change positive">+1.67%</span>
                        </div>
                        <div class="sector-item">
                            <span class="sector-rank">4</span>
                            <span class="sector-name">医药生物</span>
                            <span class="sector-change positive">+0.89%</span>
                        </div>
                        <div class="sector-item">
                            <span class="sector-rank">5</span>
                            <span class="sector-name">银行</span>
                            <span class="sector-change negative">-0.23%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    private renderMainlinesContent(): string {
        interface MainlineDisplay {
            name: string;
            score: number;
            industries: string[];
            reasoning?: string;
            logic?: string;
        }

        const mainlines: MainlineDisplay[] = this._mainlines.length > 0 
            ? this._mainlines.map(m => ({ ...m, reasoning: m.logic }))
            : [
                { name: '人工智能', score: 92, industries: ['软件', '计算机设备'], reasoning: 'AI应用加速落地' },
                { name: '华为产业链', score: 88, industries: ['电子', '通信'], reasoning: '自主可控持续推进' },
                { name: '数据要素', score: 85, industries: ['计算机', '传媒'], reasoning: '政策支持力度大' },
            ];
        
        return `
            <div class="mainlines-grid">
                ${mainlines.map((m, i) => `
                    <div class="mainline-card ${i === 0 ? 'highlight' : ''}">
                        <div class="mainline-header">
                            <span class="mainline-rank">#${i + 1}</span>
                            <span class="mainline-score">${m.score?.toFixed(0) || 80}</span>
                        </div>
                        <div class="mainline-name">${m.name}</div>
                        <div class="mainline-industries">
                            ${(m.industries || []).map((ind: string) => `<span class="industry-tag">${ind}</span>`).join('')}
                        </div>
                        <div class="mainline-reasoning">${m.reasoning || '热点持续'}</div>
                        <button class="btn btn-sm" onclick="filterCandidates({mainline: '${m.name}'})">
                            查看相关股票
                        </button>
                    </div>
                `).join('')}
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h3>🤖 LLM 主线分析</h3>
                    <button class="btn btn-sm btn-outline" onclick="executeCommand('trquant.llmMainlines')">
                        AI 分析
                    </button>
                </div>
                <div class="card-body">
                    <div class="llm-analysis">
                        <p>根据近期市场走势和资金流向分析，当前市场主要聚焦于<strong>科技成长</strong>方向：</p>
                        <ul>
                            <li>人工智能应用端持续发酵，关注算力、应用软件</li>
                            <li>华为产业链受益于自主可控，估值有望修复</li>
                            <li>数据要素政策推进，关注数据服务商</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    private renderCandidatePoolContent(): string {
        return `
            <div class="filter-section">
                <div class="card">
                    <div class="card-header">
                        <h3>🔍 筛选条件</h3>
                    </div>
                    <div class="card-body">
                        <div class="filter-grid">
                            <div class="filter-item">
                                <label>市值范围</label>
                                <select>
                                    <option>全部</option>
                                    <option>30-100亿</option>
                                    <option>100-500亿</option>
                                    <option>500亿以上</option>
                                </select>
                            </div>
                            <div class="filter-item">
                                <label>行业</label>
                                <select>
                                    <option>全部</option>
                                    <option>计算机</option>
                                    <option>电子</option>
                                    <option>通信</option>
                                    <option>新能源</option>
                                </select>
                            </div>
                            <div class="filter-item">
                                <label>ROE</label>
                                <select>
                                    <option>全部</option>
                                    <option>>15%</option>
                                    <option>>10%</option>
                                    <option>>5%</option>
                                </select>
                            </div>
                            <div class="filter-item">
                                <label>PE</label>
                                <select>
                                    <option>全部</option>
                                    <option><30</option>
                                    <option><50</option>
                                    <option><100</option>
                                </select>
                            </div>
                        </div>
                        <div class="filter-actions">
                            <button class="btn btn-primary" onclick="filterCandidates({})">
                                应用筛选
                            </button>
                            <button class="btn btn-outline">
                                重置条件
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="candidates-section">
                <div class="card">
                    <div class="card-header">
                        <h3>📋 候选股票 (示例)</h3>
                        <span class="badge">256 只</span>
                    </div>
                    <div class="card-body">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>代码</th>
                                    <th>名称</th>
                                    <th>行业</th>
                                    <th>市值</th>
                                    <th>PE</th>
                                    <th>ROE</th>
                                    <th>入池理由</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>002415</td>
                                    <td>海康威视</td>
                                    <td>计算机</td>
                                    <td>2500亿</td>
                                    <td>18.5</td>
                                    <td>25.3%</td>
                                    <td>AI龙头</td>
                                </tr>
                                <tr>
                                    <td>300750</td>
                                    <td>宁德时代</td>
                                    <td>新能源</td>
                                    <td>8500亿</td>
                                    <td>22.3</td>
                                    <td>21.5%</td>
                                    <td>电池龙头</td>
                                </tr>
                                <tr>
                                    <td>688981</td>
                                    <td>中芯国际</td>
                                    <td>半导体</td>
                                    <td>3200亿</td>
                                    <td>45.6</td>
                                    <td>8.9%</td>
                                    <td>芯片制造</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }

    private renderFactorCenterContent(): string {
        const factors = this._factors.length > 0 ? this._factors : [
            { name: '动量因子', category: '价量', weight: 0.25, description: '20日动量' },
            { name: '价值因子', category: '估值', weight: 0.20, description: 'PE/PB综合' },
            { name: '质量因子', category: '基本面', weight: 0.30, description: 'ROE/ROIC' },
            { name: '波动率因子', category: '风险', weight: 0.15, description: '低波动溢价' },
            { name: '成长因子', category: '基本面', weight: 0.10, description: '营收增速' },
        ];
        
        return `
            <div class="grid-2">
                <div class="card">
                    <div class="card-header">
                        <h3>📊 推荐因子组合</h3>
                        <button class="btn btn-sm" onclick="recommendFactors()">
                            🔄 重新推荐
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="factor-list">
                            ${factors.map((f) => `
                                <div class="factor-item">
                                    <div class="factor-info">
                                        <span class="factor-name">${f.name}</span>
                                        <span class="factor-category">${f.category}</span>
                                    </div>
                                    <div class="factor-weight">
                                        <div class="weight-bar" style="width: ${(f.weight || 0.2) * 100}%"></div>
                                        <span>${((f.weight || 0.2) * 100).toFixed(0)}%</span>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h3>📈 因子有效性</h3>
                    </div>
                    <div class="card-body">
                        <div class="factor-metrics">
                            <div class="metric-row">
                                <span>IC 均值</span>
                                <span class="metric-value positive">0.045</span>
                            </div>
                            <div class="metric-row">
                                <span>IC IR</span>
                                <span class="metric-value positive">1.85</span>
                            </div>
                            <div class="metric-row">
                                <span>因子收益</span>
                                <span class="metric-value positive">+15.6%</span>
                            </div>
                            <div class="metric-row">
                                <span>多空收益</span>
                                <span class="metric-value positive">+22.3%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h3>📚 因子库</h3>
                </div>
                <div class="card-body">
                    <div class="factor-categories">
                        <div class="category-tag active">全部</div>
                        <div class="category-tag">价量</div>
                        <div class="category-tag">估值</div>
                        <div class="category-tag">基本面</div>
                        <div class="category-tag">技术</div>
                        <div class="category-tag">另类</div>
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>因子名称</th>
                                <th>类别</th>
                                <th>IC均值</th>
                                <th>IR</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>momentum_20d</td>
                                <td>价量</td>
                                <td>0.052</td>
                                <td>1.92</td>
                                <td><span class="status-badge success">有效</span></td>
                            </tr>
                            <tr>
                                <td>value_composite</td>
                                <td>估值</td>
                                <td>0.038</td>
                                <td>1.65</td>
                                <td><span class="status-badge success">有效</span></td>
                            </tr>
                            <tr>
                                <td>quality_roe</td>
                                <td>基本面</td>
                                <td>0.045</td>
                                <td>1.78</td>
                                <td><span class="status-badge success">有效</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    private renderStrategyDevContent(): string {
        return `
            <div class="strategy-actions">
                <div class="action-card" onclick="executeCommand('trquant.createProject')">
                    <div class="action-icon">📁</div>
                    <div class="action-title">新建项目</div>
                    <div class="action-desc">创建新的量化策略项目</div>
                </div>
                <div class="action-card" onclick="executeCommand('trquant.openStrategyOptimizer')">
                    <div class="action-icon">🛠️</div>
                    <div class="action-title">策略编辑器</div>
                    <div class="action-desc">打开策略优化器</div>
                </div>
                <div class="action-card" onclick="executeCommand('trquant.generateStrategy')">
                    <div class="action-icon">🤖</div>
                    <div class="action-title">AI 生成</div>
                    <div class="action-desc">LLM 辅助生成策略</div>
                </div>
                <div class="action-card" onclick="executeCommand('trquant.optimizeStrategy')">
                    <div class="action-icon">⚡</div>
                    <div class="action-title">参数优化</div>
                    <div class="action-desc">网格搜索/随机搜索</div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h3>📋 最近项目</h3>
                </div>
                <div class="card-body">
                    <div class="project-list">
                        <div class="project-item">
                            <div class="project-icon">📈</div>
                            <div class="project-info">
                                <div class="project-name">雍华靛兰</div>
                                <div class="project-meta">多因子策略 | 最后修改: 2小时前</div>
                            </div>
                            <button class="btn btn-sm" onclick="executeCommand('trquant.openStrategyOptimizer')">
                                打开
                            </button>
                        </div>
                        <div class="project-item">
                            <div class="project-icon">📊</div>
                            <div class="project-info">
                                <div class="project-name">睿智金龙</div>
                                <div class="project-meta">动量策略 | 最后修改: 昨天</div>
                            </div>
                            <button class="btn btn-sm">打开</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    private renderBacktestCenterContent(): string {
        return `
            <div class="backtest-actions">
                <button class="btn btn-primary btn-lg" onclick="executeCommand('trquant.runBacktest')">
                    ▶️ 运行回测
                </button>
            </div>
            
            <div class="grid-2">
                <div class="card">
                    <div class="card-header">
                        <h3>📊 回测配置</h3>
                    </div>
                    <div class="card-body">
                        <div class="config-form">
                            <div class="form-group">
                                <label>回测区间</label>
                                <div class="date-range">
                                    <input type="date" value="2023-01-01">
                                    <span>至</span>
                                    <input type="date" value="2024-12-01">
                                </div>
                            </div>
                            <div class="form-group">
                                <label>初始资金</label>
                                <input type="number" value="1000000" step="100000">
                            </div>
                            <div class="form-group">
                                <label>基准指数</label>
                                <select>
                                    <option>沪深300</option>
                                    <option>中证500</option>
                                    <option>创业板指</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h3>📈 最近回测</h3>
                    </div>
                    <div class="card-body">
                        <div class="backtest-list">
                            <div class="backtest-item">
                                <div class="backtest-info">
                                    <div class="backtest-name">雍华靛兰 v1.2</div>
                                    <div class="backtest-time">2024-12-05 14:30</div>
                                </div>
                                <div class="backtest-metrics">
                                    <span class="metric positive">+23.5%</span>
                                    <span class="metric">夏普 1.85</span>
                                </div>
                            </div>
                            <div class="backtest-item">
                                <div class="backtest-info">
                                    <div class="backtest-name">睿智金龙 v2.0</div>
                                    <div class="backtest-time">2024-12-04 16:20</div>
                                </div>
                                <div class="backtest-metrics">
                                    <span class="metric positive">+18.2%</span>
                                    <span class="metric">夏普 1.52</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h3>📊 回测结果对比</h3>
                </div>
                <div class="card-body">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>策略</th>
                                <th>年化收益</th>
                                <th>夏普比率</th>
                                <th>最大回撤</th>
                                <th>胜率</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>雍华靛兰 v1.2</td>
                                <td class="positive">+23.5%</td>
                                <td>1.85</td>
                                <td class="negative">-12.3%</td>
                                <td>58%</td>
                                <td><button class="btn btn-sm">详情</button></td>
                            </tr>
                            <tr>
                                <td>睿智金龙 v2.0</td>
                                <td class="positive">+18.2%</td>
                                <td>1.52</td>
                                <td class="negative">-15.6%</td>
                                <td>54%</td>
                                <td><button class="btn btn-sm">详情</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    private renderTradingCenterContent(): string {
        return `
            <div class="trading-overview">
                <div class="card status-card">
                    <div class="status-indicator warning"></div>
                    <div class="status-text">
                        <div class="status-title">交易状态</div>
                        <div class="status-value">模拟运行中</div>
                    </div>
                </div>
            </div>
            
            <div class="grid-2">
                <div class="card">
                    <div class="card-header">
                        <h3>🎮 模拟交易</h3>
                    </div>
                    <div class="card-body">
                        <div class="paper-trading">
                            <div class="trading-stat">
                                <div class="stat-label">模拟资金</div>
                                <div class="stat-value">¥1,000,000</div>
                            </div>
                            <div class="trading-stat">
                                <div class="stat-label">当前净值</div>
                                <div class="stat-value positive">¥1,156,890</div>
                            </div>
                            <div class="trading-stat">
                                <div class="stat-label">累计收益</div>
                                <div class="stat-value positive">+15.69%</div>
                            </div>
                            <div class="trading-stat">
                                <div class="stat-label">运行天数</div>
                                <div class="stat-value">45</div>
                            </div>
                        </div>
                        <div class="trading-actions">
                            <button class="btn btn-primary">启动模拟</button>
                            <button class="btn btn-outline">暂停</button>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h3>🚀 实盘部署</h3>
                    </div>
                    <div class="card-body">
                        <div class="deploy-section">
                            <div class="deploy-option">
                                <div class="option-icon">📊</div>
                                <div class="option-info">
                                    <div class="option-name">PTrade</div>
                                    <div class="option-desc">恒生 PTrade 接口</div>
                                </div>
                                <button class="btn btn-sm">部署</button>
                            </div>
                            <div class="deploy-option">
                                <div class="option-icon">⚡</div>
                                <div class="option-info">
                                    <div class="option-name">QMT</div>
                                    <div class="option-desc">迅投 QMT 接口</div>
                                </div>
                                <button class="btn btn-sm">部署</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h3>📋 今日交易信号</h3>
                </div>
                <div class="card-body">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>时间</th>
                                <th>代码</th>
                                <th>名称</th>
                                <th>方向</th>
                                <th>数量</th>
                                <th>价格</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>09:35:22</td>
                                <td>002415</td>
                                <td>海康威视</td>
                                <td class="buy">买入</td>
                                <td>1000</td>
                                <td>35.68</td>
                                <td><span class="status-badge success">已成交</span></td>
                            </tr>
                            <tr>
                                <td>10:15:45</td>
                                <td>300750</td>
                                <td>宁德时代</td>
                                <td class="sell">卖出</td>
                                <td>500</td>
                                <td>186.50</td>
                                <td><span class="status-badge warning">部分成交</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    private renderFooterActions(): string {
        const config = STEP_CONFIGS[this._step];
        const prevStep = this.getPrevStep();
        const nextStep = this.getNextStep();
        
        return `
            <div class="footer-nav">
                ${prevStep ? `
                    <button class="btn btn-outline" onclick="navigateStep('${prevStep}')">
                        ◀ 上一步
                    </button>
                ` : '<div></div>'}
                
                <div class="step-progress">
                    步骤 ${config.step} / 8
                </div>
                
                ${nextStep ? `
                    <button class="btn btn-primary" onclick="navigateStep('${nextStep}')">
                        下一步 ▶
                    </button>
                ` : `
                    <button class="btn btn-success">
                        ✅ 完成工作流
                    </button>
                `}
            </div>
        `;
    }

    private getNextStep(): WorkflowStep | null {
        const steps: WorkflowStep[] = [
            'data-center', 'market-analysis', 'mainlines', 'candidate-pool',
            'factor-center', 'strategy-dev', 'backtest-center', 'trading-center'
        ];
        const currentIndex = steps.indexOf(this._step);
        return currentIndex < steps.length - 1 ? steps[currentIndex + 1] : null;
    }

    private getPrevStep(): WorkflowStep | null {
        const steps: WorkflowStep[] = [
            'data-center', 'market-analysis', 'mainlines', 'candidate-pool',
            'factor-center', 'strategy-dev', 'backtest-center', 'trading-center'
        ];
        const currentIndex = steps.indexOf(this._step);
        return currentIndex > 0 ? steps[currentIndex - 1] : null;
    }

    private getStyles(): string {
        return `
            :root {
                --bg-dark: #0a0e14;
                --bg-primary: #0d1117;
                --bg-secondary: #161b22;
                --bg-card: #1c2128;
                --bg-hover: #262c36;
                --text-primary: #e6edf3;
                --text-secondary: #8b949e;
                --text-muted: #6e7681;
                --accent-gold: #f0b429;
                --accent-green: #3fb950;
                --accent-blue: #58a6ff;
                --accent-purple: #a371f7;
                --accent-red: #f85149;
                --border-color: #30363d;
            }
            
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: var(--bg-dark);
                color: var(--text-primary);
                min-height: 100vh;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }
            
            /* 工作流导航 */
            .workflow-nav {
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 16px 0;
                margin-bottom: 24px;
                background: var(--bg-secondary);
                border-radius: 12px;
                border: 1px solid var(--border-color);
            }
            
            .nav-step {
                display: flex;
                flex-direction: column;
                align-items: center;
                cursor: pointer;
                padding: 8px 16px;
                border-radius: 8px;
                transition: all 0.2s;
            }
            
            .nav-step:hover {
                background: var(--bg-hover);
            }
            
            .nav-step.active {
                background: var(--accent-gold);
            }
            
            .nav-step.active .step-number,
            .nav-step.active .step-icon {
                color: #000;
            }
            
            .nav-step.past .step-number {
                background: var(--accent-green);
            }
            
            .step-number {
                width: 24px;
                height: 24px;
                border-radius: 50%;
                background: var(--bg-card);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 4px;
            }
            
            .step-icon {
                font-size: 16px;
            }
            
            .nav-connector {
                width: 30px;
                height: 2px;
                background: var(--border-color);
            }
            
            /* 页面头部 */
            .page-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 24px;
                padding: 20px;
                background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
                border-radius: 12px;
                border: 1px solid var(--border-color);
            }
            
            .step-badge {
                display: inline-block;
                padding: 4px 12px;
                background: var(--accent-gold);
                color: #000;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 8px;
            }
            
            .page-header h1 {
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 8px;
            }
            
            .page-header .description {
                color: var(--text-secondary);
                font-size: 14px;
            }
            
            .header-actions {
                display: flex;
                gap: 12px;
            }
            
            /* 按钮 */
            .btn {
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                border: 1px solid transparent;
                transition: all 0.2s;
            }
            
            .btn-primary {
                background: var(--accent-gold);
                color: #000;
            }
            
            .btn-primary:hover {
                background: #d4a030;
            }
            
            .btn-secondary {
                background: var(--bg-card);
                color: var(--text-primary);
                border-color: var(--border-color);
            }
            
            .btn-secondary:hover {
                background: var(--bg-hover);
            }
            
            .btn-outline {
                background: transparent;
                color: var(--text-secondary);
                border-color: var(--border-color);
            }
            
            .btn-outline:hover {
                background: var(--bg-hover);
                color: var(--text-primary);
            }
            
            .btn-success {
                background: var(--accent-green);
                color: #fff;
            }
            
            .btn-sm {
                padding: 6px 12px;
                font-size: 12px;
            }
            
            .btn-lg {
                padding: 14px 28px;
                font-size: 16px;
            }
            
            /* 卡片 */
            .card {
                background: var(--bg-secondary);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                margin-bottom: 20px;
            }
            
            .card-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 16px 20px;
                border-bottom: 1px solid var(--border-color);
            }
            
            .card-header h3 {
                font-size: 16px;
                font-weight: 600;
            }
            
            .card-body {
                padding: 20px;
            }
            
            /* 网格布局 */
            .grid-2 {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }
            
            .grid-3 {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 16px;
                margin-bottom: 20px;
            }
            
            /* 状态列表 */
            .status-list {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .status-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px;
                background: var(--bg-card);
                border-radius: 8px;
            }
            
            .status-icon {
                width: 24px;
                height: 24px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
            }
            
            .status-icon.success {
                background: rgba(63, 185, 80, 0.2);
                color: var(--accent-green);
            }
            
            .status-icon.warning {
                background: rgba(240, 180, 41, 0.2);
                color: var(--accent-gold);
            }
            
            .status-time {
                margin-left: auto;
                font-size: 12px;
                color: var(--text-muted);
            }
            
            /* 知识库统计 */
            .knowledge-stats {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 16px;
                margin-bottom: 16px;
            }
            
            .stat-item {
                text-align: center;
                padding: 16px;
                background: var(--bg-card);
                border-radius: 8px;
            }
            
            .stat-value {
                font-size: 28px;
                font-weight: 700;
                color: var(--accent-gold);
            }
            
            .stat-label {
                font-size: 12px;
                color: var(--text-muted);
                margin-top: 4px;
            }
            
            /* 操作网格 */
            .action-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 16px;
            }
            
            .action-btn {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
                padding: 20px;
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.2s;
            }
            
            .action-btn:hover {
                background: var(--bg-hover);
                border-color: var(--accent-blue);
                transform: translateY(-2px);
            }
            
            .action-icon {
                font-size: 32px;
            }
            
            .action-text {
                font-size: 14px;
                color: var(--text-secondary);
            }
            
            /* 市场概览 */
            .market-overview {
                margin-bottom: 20px;
            }
            
            .regime-card {
                display: flex;
                align-items: center;
                gap: 20px;
                padding: 24px;
                background: var(--bg-secondary);
                border: 2px solid;
                border-radius: 12px;
            }
            
            .regime-icon {
                font-size: 48px;
            }
            
            .regime-label {
                font-size: 14px;
                color: var(--text-muted);
            }
            
            .regime-value {
                font-size: 32px;
                font-weight: 700;
            }
            
            /* 指数卡片 */
            .index-card {
                background: var(--bg-secondary);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            }
            
            .index-name {
                font-size: 14px;
                color: var(--text-muted);
                margin-bottom: 8px;
            }
            
            .index-value {
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 4px;
            }
            
            .index-change {
                font-size: 14px;
                font-weight: 600;
            }
            
            .index-change.positive {
                color: var(--accent-green);
            }
            
            .index-change.negative {
                color: var(--accent-red);
            }
            
            /* 板块列表 */
            .sector-list {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            
            .sector-item {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px;
                background: var(--bg-card);
                border-radius: 8px;
            }
            
            .sector-rank {
                width: 24px;
                height: 24px;
                border-radius: 50%;
                background: var(--accent-gold);
                color: #000;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: 600;
            }
            
            .sector-name {
                flex: 1;
            }
            
            .sector-change {
                font-weight: 600;
            }
            
            .sector-change.positive {
                color: var(--accent-green);
            }
            
            .sector-change.negative {
                color: var(--accent-red);
            }
            
            /* 投资主线 */
            .mainlines-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .mainline-card {
                background: var(--bg-secondary);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 20px;
            }
            
            .mainline-card.highlight {
                border-color: var(--accent-gold);
                background: linear-gradient(135deg, rgba(240, 180, 41, 0.1) 0%, var(--bg-secondary) 100%);
            }
            
            .mainline-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }
            
            .mainline-rank {
                font-size: 14px;
                font-weight: 600;
                color: var(--accent-gold);
            }
            
            .mainline-score {
                padding: 4px 12px;
                background: var(--accent-gold);
                color: #000;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 600;
            }
            
            .mainline-name {
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 12px;
            }
            
            .mainline-industries {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-bottom: 12px;
            }
            
            .industry-tag {
                padding: 4px 8px;
                background: var(--bg-card);
                border-radius: 4px;
                font-size: 12px;
                color: var(--text-secondary);
            }
            
            .mainline-reasoning {
                font-size: 14px;
                color: var(--text-muted);
                margin-bottom: 16px;
            }
            
            /* LLM 分析 */
            .llm-analysis {
                padding: 16px;
                background: var(--bg-card);
                border-radius: 8px;
                line-height: 1.8;
            }
            
            .llm-analysis strong {
                color: var(--accent-gold);
            }
            
            .llm-analysis ul {
                margin-top: 12px;
                padding-left: 20px;
            }
            
            .llm-analysis li {
                color: var(--text-secondary);
                margin-bottom: 8px;
            }
            
            /* 筛选区 */
            .filter-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 16px;
                margin-bottom: 16px;
            }
            
            .filter-item label {
                display: block;
                font-size: 12px;
                color: var(--text-muted);
                margin-bottom: 6px;
            }
            
            .filter-item select,
            .filter-item input {
                width: 100%;
                padding: 10px;
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 6px;
                color: var(--text-primary);
                font-size: 14px;
            }
            
            .filter-actions {
                display: flex;
                gap: 12px;
            }
            
            /* 数据表格 */
            .data-table {
                width: 100%;
                border-collapse: collapse;
            }
            
            .data-table th,
            .data-table td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid var(--border-color);
            }
            
            .data-table th {
                font-size: 12px;
                font-weight: 600;
                color: var(--text-muted);
                text-transform: uppercase;
            }
            
            .data-table tbody tr:hover {
                background: var(--bg-hover);
            }
            
            .positive {
                color: var(--accent-green) !important;
            }
            
            .negative {
                color: var(--accent-red) !important;
            }
            
            .buy {
                color: var(--accent-green);
            }
            
            .sell {
                color: var(--accent-red);
            }
            
            /* 状态徽章 */
            .status-badge {
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            
            .status-badge.success {
                background: rgba(63, 185, 80, 0.2);
                color: var(--accent-green);
            }
            
            .status-badge.warning {
                background: rgba(240, 180, 41, 0.2);
                color: var(--accent-gold);
            }
            
            .badge {
                padding: 4px 8px;
                background: var(--bg-card);
                border-radius: 4px;
                font-size: 12px;
                color: var(--text-muted);
            }
            
            /* 因子 */
            .factor-list {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .factor-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px;
                background: var(--bg-card);
                border-radius: 8px;
            }
            
            .factor-name {
                font-weight: 500;
            }
            
            .factor-category {
                font-size: 12px;
                color: var(--text-muted);
                margin-left: 8px;
            }
            
            .factor-weight {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .weight-bar {
                width: 80px;
                height: 8px;
                background: var(--accent-gold);
                border-radius: 4px;
            }
            
            .factor-metrics {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .metric-row {
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid var(--border-color);
            }
            
            .metric-value {
                font-weight: 600;
            }
            
            .category-tag {
                display: inline-block;
                padding: 6px 12px;
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 20px;
                font-size: 12px;
                margin-right: 8px;
                margin-bottom: 12px;
                cursor: pointer;
            }
            
            .category-tag.active {
                background: var(--accent-gold);
                color: #000;
                border-color: var(--accent-gold);
            }
            
            /* 策略操作 */
            .strategy-actions {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .action-card {
                background: var(--bg-secondary);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 24px;
                text-align: center;
                cursor: pointer;
                transition: all 0.2s;
            }
            
            .action-card:hover {
                background: var(--bg-hover);
                border-color: var(--accent-blue);
                transform: translateY(-2px);
            }
            
            .action-card .action-icon {
                font-size: 40px;
                margin-bottom: 12px;
            }
            
            .action-card .action-title {
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 8px;
            }
            
            .action-card .action-desc {
                font-size: 12px;
                color: var(--text-muted);
            }
            
            /* 项目列表 */
            .project-list {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .project-item {
                display: flex;
                align-items: center;
                gap: 16px;
                padding: 16px;
                background: var(--bg-card);
                border-radius: 8px;
            }
            
            .project-icon {
                font-size: 24px;
            }
            
            .project-info {
                flex: 1;
            }
            
            .project-name {
                font-weight: 600;
                margin-bottom: 4px;
            }
            
            .project-meta {
                font-size: 12px;
                color: var(--text-muted);
            }
            
            /* 回测 */
            .backtest-actions {
                text-align: center;
                margin-bottom: 20px;
            }
            
            .config-form {
                display: flex;
                flex-direction: column;
                gap: 16px;
            }
            
            .form-group label {
                display: block;
                font-size: 12px;
                color: var(--text-muted);
                margin-bottom: 6px;
            }
            
            .form-group input,
            .form-group select {
                width: 100%;
                padding: 10px;
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 6px;
                color: var(--text-primary);
            }
            
            .date-range {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .date-range input {
                flex: 1;
            }
            
            .backtest-list {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .backtest-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px;
                background: var(--bg-card);
                border-radius: 8px;
            }
            
            .backtest-name {
                font-weight: 500;
            }
            
            .backtest-time {
                font-size: 12px;
                color: var(--text-muted);
            }
            
            .backtest-metrics {
                display: flex;
                gap: 16px;
            }
            
            .metric {
                font-size: 14px;
            }
            
            /* 交易 */
            .trading-overview {
                margin-bottom: 20px;
            }
            
            .status-card {
                display: flex;
                align-items: center;
                gap: 16px;
                padding: 20px;
            }
            
            .status-indicator {
                width: 12px;
                height: 12px;
                border-radius: 50%;
            }
            
            .status-indicator.success {
                background: var(--accent-green);
                box-shadow: 0 0 8px var(--accent-green);
            }
            
            .status-indicator.warning {
                background: var(--accent-gold);
                box-shadow: 0 0 8px var(--accent-gold);
            }
            
            .status-title {
                font-size: 12px;
                color: var(--text-muted);
            }
            
            .status-value {
                font-size: 18px;
                font-weight: 600;
            }
            
            .paper-trading {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 16px;
                margin-bottom: 16px;
            }
            
            .trading-stat {
                padding: 12px;
                background: var(--bg-card);
                border-radius: 8px;
                text-align: center;
            }
            
            .trading-stat .stat-label {
                font-size: 12px;
                color: var(--text-muted);
            }
            
            .trading-stat .stat-value {
                font-size: 20px;
                font-weight: 700;
                margin-top: 4px;
            }
            
            .trading-actions {
                display: flex;
                gap: 12px;
            }
            
            .deploy-section {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .deploy-option {
                display: flex;
                align-items: center;
                gap: 16px;
                padding: 16px;
                background: var(--bg-card);
                border-radius: 8px;
            }
            
            .option-icon {
                font-size: 24px;
            }
            
            .option-info {
                flex: 1;
            }
            
            .option-name {
                font-weight: 600;
            }
            
            .option-desc {
                font-size: 12px;
                color: var(--text-muted);
            }
            
            /* 底部 */
            .footer {
                margin-top: 24px;
                padding: 20px;
                background: var(--bg-secondary);
                border-radius: 12px;
                border: 1px solid var(--border-color);
            }
            
            .footer-nav {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .step-progress {
                font-size: 14px;
                color: var(--text-muted);
            }
            
            /* 空状态 */
            .empty-state {
                text-align: center;
                padding: 40px;
                color: var(--text-muted);
            }
            
            @media (max-width: 1200px) {
                .grid-2, .grid-3, .strategy-actions, .action-grid, .mainlines-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }
            
            @media (max-width: 768px) {
                .grid-2, .grid-3, .strategy-actions, .action-grid, .mainlines-grid, .filter-grid {
                    grid-template-columns: 1fr;
                }
                
                .workflow-nav {
                    display: none;
                }
            }
        `;
    }

    public dispose() {
        WorkflowStepPanel.panels.delete(this._step);
        while (this._disposables.length) {
            const disposable = this._disposables.pop();
            if (disposable) {
                disposable.dispose();
            }
        }
    }
}

/**
 * 注册工作流步骤面板命令
 */
export function registerWorkflowStepPanels(
    context: vscode.ExtensionContext,
    client: TRQuantClient
): void {
    // 注册各步骤的命令
    const commands: Array<{ id: string; step: WorkflowStep }> = [
        { id: 'trquant.openDataCenter', step: 'data-center' },
        { id: 'trquant.openMarketAnalysis', step: 'market-analysis' },
        { id: 'trquant.openMainlines', step: 'mainlines' },
        { id: 'trquant.openCandidatePool', step: 'candidate-pool' },
        { id: 'trquant.openFactorCenter', step: 'factor-center' },
        { id: 'trquant.openStrategyDev', step: 'strategy-dev' },
        { id: 'trquant.openBacktestCenter', step: 'backtest-center' },
        { id: 'trquant.openTradingCenter', step: 'trading-center' },
    ];

    for (const { id, step } of commands) {
        const disposable = vscode.commands.registerCommand(id, () => {
            WorkflowStepPanel.createOrShow(context.extensionUri, client, step);
        });
        context.subscriptions.push(disposable);
    }

    console.log('[TRQuant] 工作流步骤面板命令已注册');
}

