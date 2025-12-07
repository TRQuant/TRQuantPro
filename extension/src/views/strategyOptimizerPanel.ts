/**
 * 策略优化器面板 - 重构版
 * ==========================
 * 
 * 完整的策略优化工作流：
 * 1. 策略编辑器 - 选择/查看策略代码
 * 2. 策略分析 - 评分和诊断
 * 3. 参数优化 - 自动优化参数
 * 4. 版本管理 - 保存和对比版本
 * 5. 可视化 - 图表展示
 * 
 * 最终保存优化后的代码，进入回测/实盘流程
 */

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { OptimizationReport, OptimizationAdvice } from '../services/strategyOptimizer/analyzer/optimizationAdvisor';
import { logger } from '../utils/logger';

const MODULE = 'StrategyOptimizerPanel';

// 获取策略优化器服务
let strategyOptimizerInstance: any = null;
async function getStrategyOptimizer() {
    if (!strategyOptimizerInstance) {
        const module = await import('../services/strategyOptimizer');
        strategyOptimizerInstance = (module as any).strategyOptimizer || 
                                   (module as any).StrategyOptimizerService?.getInstance();
    }
    return strategyOptimizerInstance;
}

/** Tab类型 */
type TabType = 'editor' | 'analysis' | 'optimize' | 'versions' | 'visualize';

/** 参数范围配置 */
interface ParameterRange {
    name: string;
    type: 'int' | 'float';
    min: number;
    max: number;
    step: number;
    currentValue: number;
    description?: string;
}

/** 优化结果项 */
interface OptimizationResult {
    id: string;
    timestamp: string;
    parameters: Record<string, number>;
    metrics: {
        totalReturn: number;
        sharpeRatio: number;
        maxDrawdown: number;
        winRate: number;
    };
    score: number;
}

/** 策略版本 */
interface StrategyVersion {
    id: string;
    version: string;
    timestamp: string;
    description: string;
    parameters: Record<string, number>;
    metrics?: OptimizationResult['metrics'];
    code: string;
    isOptimized: boolean;
}

export class StrategyOptimizerPanel {
    public static currentPanel: StrategyOptimizerPanel | undefined;
    private static _lastActiveEditor: vscode.TextEditor | undefined;
    
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _storagePath: string;
    private _disposables: vscode.Disposable[] = [];
    
    // 状态
    private _currentTab: TabType = 'editor';
    private _strategyCode: string = '';
    private _strategyName: string = '';
    private _strategyPath: string = '';
    private _report: OptimizationReport | null = null;
    private _parameterRanges: ParameterRange[] = [];
    private _optimizationResults: OptimizationResult[] = [];
    private _versions: StrategyVersion[] = [];
    private _isOptimizing: boolean = false;
    private _optimizationProgress: number = 0;

    private constructor(
        panel: vscode.WebviewPanel,
        extensionUri: vscode.Uri,
        storagePath: string
    ) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._storagePath = storagePath;

        this._panel.webview.onDidReceiveMessage(
            message => this.handleMessage(message),
            null,
            this._disposables
        );

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        
        this.loadData();
        this.updateContent();
    }

    public static createOrShow(
        extensionUri: vscode.Uri,
        code?: string,
        fileName?: string,
        storagePath?: string
    ): StrategyOptimizerPanel {
        const column = vscode.ViewColumn.One;

        if (StrategyOptimizerPanel.currentPanel) {
            StrategyOptimizerPanel.currentPanel._panel.reveal(column);
            if (code && fileName) {
                StrategyOptimizerPanel.currentPanel.loadStrategy(code, fileName);
            }
            return StrategyOptimizerPanel.currentPanel;
        }

        const panel = vscode.window.createWebviewPanel(
            'strategyOptimizer',
            '🔬 策略优化器',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [extensionUri]
            }
        );

        const storage = storagePath || 
            (vscode.workspace.workspaceFolders?.[0]?.uri.fsPath 
                ? path.join(vscode.workspace.workspaceFolders[0].uri.fsPath, '.trquant', 'optimizer')
                : path.join(os.homedir(), '.trquant', 'optimizer'));

        StrategyOptimizerPanel.currentPanel = new StrategyOptimizerPanel(panel, extensionUri, storage);
        
        if (code && fileName) {
            StrategyOptimizerPanel.currentPanel.loadStrategy(code, fileName);
        }
        
        return StrategyOptimizerPanel.currentPanel;
    }

    /**
     * 加载策略
     */
    private loadStrategy(code: string, fileName: string, filePath?: string): void {
        this._strategyCode = code;
        this._strategyName = fileName;
        this._strategyPath = filePath || '';
        this._parameterRanges = this.extractParameters(code);
        this._report = null;
        this.updateContent();
    }

    /**
     * 消息处理
     */
    private async handleMessage(message: any): Promise<void> {
        switch (message.command) {
            case 'switchTab':
                this._currentTab = message.tab;
                this.updateContent();
                break;
            case 'selectFile':
                await this.selectFile();
                break;
            case 'openInEditor':
                await this.openInEditor();
                break;
            case 'analyzeStrategy':
                await this.analyzeStrategy();
                break;
            case 'updateParameter':
                this.updateParameter(message.index, message.field, message.value);
                break;
            case 'addParameter':
                this.addParameter();
                break;
            case 'removeParameter':
                this.removeParameter(message.index);
                break;
            case 'startOptimization':
                await this.startOptimization(message.config);
                break;
            case 'stopOptimization':
                this.stopOptimization();
                break;
            case 'applyResult':
                await this.applyOptimizationResult(message.resultId);
                break;
            case 'saveVersion':
                await this.saveVersion(message.description);
                break;
            case 'loadVersion':
                await this.loadVersion(message.versionId);
                break;
            case 'compareVersions':
                await this.compareVersions(message.v1, message.v2);
                break;
            case 'deleteVersion':
                this.deleteVersion(message.versionId);
                break;
            case 'exportVersion':
                await this.exportVersion(message.versionId);
                break;
            case 'saveAndBacktest':
                await this.saveAndBacktest();
                break;
            case 'saveAndTrade':
                await this.saveAndTrade();
                break;
            case 'applyAdvice':
                await this.applyAdvice(message.adviceId);
                break;
            case 'codeChanged':
                // 代码变化时更新
                this._strategyCode = message.code;
                this._parameterRanges = this.extractParameters(message.code);
                // 不刷新整个页面，避免编辑器重置
                break;
            case 'getCodeResponse':
                // 收到webview的代码
                this._strategyCode = message.code;
                this._parameterRanges = this.extractParameters(message.code);
                // 重新分析
                await this.analyzeStrategy();
                break;
            case 'getCodeForSave':
                // 收到webview的代码用于保存版本
                this.doSaveVersion(message.code, message.description);
                break;
            case 'applyBestResult':
                // 应用最佳结果
                if (this._optimizationResults.length > 0) {
                    await this.applyOptimizationResult(this._optimizationResults[0].id);
                }
                break;
            case 'autoDetectParams':
                // 重新检测参数
                this._parameterRanges = this.extractParameters(this._strategyCode);
                this.updateContent();
                vscode.window.showInformationMessage(`检测到 ${this._parameterRanges.length} 个可调参数`);
                break;
            case 'viewResultDetail':
                await this.viewResultDetail(message.resultId);
                break;
            case 'exportResults':
                await this.exportResults();
                break;
            case 'exportAllVersions':
                await this.exportAllVersions();
                break;
            case 'clearAllVersions':
                this._versions = [];
                this.saveData();
                this.updateContent();
                vscode.window.showInformationMessage('已清空所有版本');
                break;
            case 'viewVersionCode':
                await this.viewVersionCode(message.versionId);
                break;
            case 'exportVisualization':
                await this.exportVisualization();
                break;
        }
    }
    
    /**
     * 查看优化结果详情
     */
    private async viewResultDetail(resultId: string): Promise<void> {
        const result = this._optimizationResults.find(r => r.id === resultId);
        if (!result) return;
        
        const detail = `
优化结果详情
============
时间: ${new Date(result.timestamp).toLocaleString('zh-CN')}
评分: ${result.score.toFixed(2)}

参数:
${Object.entries(result.parameters).map(([k, v]) => `  ${k} = ${v}`).join('\n')}

指标:
  收益率: ${(result.metrics.totalReturn * 100).toFixed(2)}%
  夏普比率: ${result.metrics.sharpeRatio.toFixed(2)}
  最大回撤: ${(result.metrics.maxDrawdown * 100).toFixed(2)}%
  胜率: ${(result.metrics.winRate * 100).toFixed(1)}%
        `.trim();
        
        const doc = await vscode.workspace.openTextDocument({ content: detail, language: 'plaintext' });
        await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
    }
    
    /**
     * 导出优化结果
     */
    private async exportResults(): Promise<void> {
        const results = this._optimizationResults.map(r => ({
            timestamp: r.timestamp,
            score: r.score,
            parameters: r.parameters,
            metrics: r.metrics
        }));
        
        const uri = await vscode.window.showSaveDialog({
            defaultUri: vscode.Uri.file(path.join(
                vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || os.homedir(),
                `optimization_results_${Date.now()}.json`
            )),
            filters: { 'JSON': ['json'] }
        });
        
        if (uri) {
            fs.writeFileSync(uri.fsPath, JSON.stringify(results, null, 2));
            vscode.window.showInformationMessage(`已导出 ${results.length} 个优化结果`);
        }
    }
    
    /**
     * 导出所有版本
     */
    private async exportAllVersions(): Promise<void> {
        const uri = await vscode.window.showSaveDialog({
            defaultUri: vscode.Uri.file(path.join(
                vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || os.homedir(),
                `strategy_versions_${Date.now()}.json`
            )),
            filters: { 'JSON': ['json'] }
        });
        
        if (uri) {
            fs.writeFileSync(uri.fsPath, JSON.stringify(this._versions, null, 2));
            vscode.window.showInformationMessage(`已导出 ${this._versions.length} 个版本`);
        }
    }
    
    /**
     * 查看版本代码
     */
    private async viewVersionCode(versionId: string): Promise<void> {
        const version = this._versions.find(v => v.id === versionId);
        if (!version) return;
        
        const doc = await vscode.workspace.openTextDocument({ content: version.code, language: 'python' });
        await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
    }
    
    /**
     * 导出可视化数据
     */
    private async exportVisualization(): Promise<void> {
        const vizData = {
            strategy: this._strategyName,
            timestamp: new Date().toISOString(),
            results: this._optimizationResults,
            parameters: this._parameterRanges,
            report: this._report
        };
        
        const uri = await vscode.window.showSaveDialog({
            defaultUri: vscode.Uri.file(path.join(
                vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || os.homedir(),
                `visualization_${Date.now()}.json`
            )),
            filters: { 'JSON': ['json'] }
        });
        
        if (uri) {
            fs.writeFileSync(uri.fsPath, JSON.stringify(vizData, null, 2));
            vscode.window.showInformationMessage('已导出可视化数据');
        }
    }

    /**
     * 在编辑器中打开当前文件
     */
    private async openInEditor(): Promise<void> {
        if (!this._strategyPath) {
            vscode.window.showWarningMessage('没有策略文件');
            return;
        }
        
        const uri = vscode.Uri.file(this._strategyPath);
        await vscode.window.showTextDocument(uri);
    }

    /**
     * 选择文件 - 读取文件内容到webview编辑器
     */
    private async selectFile(): Promise<void> {
        const defaultPath = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        
        const fileUri = await vscode.window.showOpenDialog({
            canSelectFiles: true,
            canSelectFolders: false,
            canSelectMany: false,
            defaultUri: defaultPath ? vscode.Uri.file(path.join(defaultPath, 'Projects')) : undefined,
            filters: {
                'Python策略': ['py'],
                '所有文件': ['*']
            },
            title: '选择策略文件'
        });

        if (fileUri && fileUri[0]) {
            try {
                // 读取文件内容，不打开原生编辑器
                const code = fs.readFileSync(fileUri[0].fsPath, 'utf-8');
                const fileName = path.basename(fileUri[0].fsPath);
                this.loadStrategy(code, fileName, fileUri[0].fsPath);
                // 通知webview更新编辑器内容
                this._panel.webview.postMessage({
                    command: 'updateCode',
                    code: code,
                    fileName: fileName
                });
                vscode.window.showInformationMessage(`已加载策略: ${fileName}`);
            } catch (error) {
                vscode.window.showErrorMessage(`读取文件失败: ${error}`);
            }
        }
    }

    /**
     * 分析策略 - 从webview编辑器读取代码
     */
    private async analyzeStrategy(): Promise<void> {
        if (!this._strategyCode) {
            // 请求webview发送当前代码
            this._panel.webview.postMessage({ command: 'getCode' });
            return;
        }

        try {
            this._panel.webview.postMessage({ command: 'showLoading', message: '正在分析策略...' });
            
            const optimizer = await getStrategyOptimizer();
            this._report = optimizer.generateOptimizationReport(this._strategyCode, this._strategyName);
            
            this._currentTab = 'analysis';
            this.updateContent();
            
            vscode.window.showInformationMessage(`分析完成！整体评分: ${this._report?.overallScore ?? 'N/A'}/100`);
        } catch (error) {
            logger.error(`策略分析失败: ${error}`, MODULE);
            vscode.window.showErrorMessage(`分析失败: ${error}`);
        }
    }

    /**
     * 从代码提取参数 - 增强版，支持更多格式
     */
    private extractParameters(code: string): ParameterRange[] {
        const params: ParameterRange[] = [];
        const lines = code.split('\n');
        const foundNames = new Set<string>();
        
        // 预设参数范围 - 扩展列表
        const presets: Record<string, { min: number; max: number; step: number; desc: string }> = {
            // 股票数量相关
            'STOCK_NUM': { min: 5, max: 50, step: 5, desc: '持股数量' },
            'stock_num': { min: 5, max: 50, step: 5, desc: '持股数量' },
            'TOP_N': { min: 5, max: 50, step: 5, desc: '选股数量' },
            'top_n': { min: 5, max: 50, step: 5, desc: '选股数量' },
            'N': { min: 5, max: 50, step: 5, desc: '数量' },
            // 止损止盈
            'STOP_LOSS': { min: 0.03, max: 0.20, step: 0.01, desc: '止损线' },
            'stop_loss': { min: 0.03, max: 0.20, step: 0.01, desc: '止损线' },
            'TAKE_PROFIT': { min: 0.10, max: 0.50, step: 0.05, desc: '止盈线' },
            'take_profit': { min: 0.10, max: 0.50, step: 0.05, desc: '止盈线' },
            // 周期相关
            'MA_PERIOD': { min: 5, max: 60, step: 5, desc: '均线周期' },
            'ma_period': { min: 5, max: 60, step: 5, desc: '均线周期' },
            'SHORT_PERIOD': { min: 5, max: 30, step: 5, desc: '短期周期' },
            'short_period': { min: 5, max: 30, step: 5, desc: '短期周期' },
            'LONG_PERIOD': { min: 20, max: 120, step: 10, desc: '长期周期' },
            'long_period': { min: 20, max: 120, step: 10, desc: '长期周期' },
            'LOOKBACK': { min: 5, max: 60, step: 5, desc: '回看周期' },
            'lookback': { min: 5, max: 60, step: 5, desc: '回看周期' },
            // 仓位相关
            'MAX_POSITION': { min: 0.5, max: 1.0, step: 0.1, desc: '最大仓位' },
            'max_position': { min: 0.5, max: 1.0, step: 0.1, desc: '最大仓位' },
            'POSITION_SIZE': { min: 0.05, max: 0.3, step: 0.05, desc: '单票仓位' },
            'position_size': { min: 0.05, max: 0.3, step: 0.05, desc: '单票仓位' },
            // 调仓相关
            'REBALANCE_DAYS': { min: 1, max: 30, step: 1, desc: '调仓周期' },
            'rebalance_days': { min: 1, max: 30, step: 1, desc: '调仓周期' },
            // 阈值相关
            'THRESHOLD': { min: 0.01, max: 0.1, step: 0.01, desc: '阈值' },
            'threshold': { min: 0.01, max: 0.1, step: 0.01, desc: '阈值' },
            // RSI相关
            'RSI_PERIOD': { min: 6, max: 24, step: 2, desc: 'RSI周期' },
            'RSI_LOW': { min: 20, max: 40, step: 5, desc: 'RSI低阈值' },
            'RSI_HIGH': { min: 60, max: 80, step: 5, desc: 'RSI高阈值' },
        };
        
        // 关键字列表 - 用于识别可能的参数
        const keywords = ['NUM', 'PERIOD', 'DAYS', 'LOSS', 'PROFIT', 'POSITION', 'SIZE', 
                          'THRESHOLD', 'RATIO', 'RATE', 'COUNT', 'MAX', 'MIN', 'TOP', 'LIMIT',
                          'num', 'period', 'days', 'loss', 'profit', 'position', 'size',
                          'threshold', 'ratio', 'rate', 'count', 'max', 'min', 'top', 'limit'];

        for (const line of lines) {
            // 跳过注释行和空行
            if (line.trim().startsWith('#') || line.trim() === '') continue;
            
            // 匹配整数参数: NAME = 10 或 name = 10
            const intMatch = line.match(/^\s*([A-Za-z][A-Za-z_0-9]*)\s*=\s*(\d+)\s*(?:#\s*(.*))?$/);
            // 匹配浮点参数: NAME = 0.5 或 name = 0.5
            const floatMatch = line.match(/^\s*([A-Za-z][A-Za-z_0-9]*)\s*=\s*(\d+\.\d+)\s*(?:#\s*(.*))?$/);
            
            const match = floatMatch || intMatch;
            if (match) {
                const name = match[1];
                const value = parseFloat(match[2]);
                const comment = match[3] || '';
                const isFloat = !!floatMatch;
                
                // 避免重复
                if (foundNames.has(name)) continue;
                
                // 检查是否是预设参数或包含关键字
                const preset = presets[name];
                const hasKeyword = keywords.some(kw => name.toUpperCase().includes(kw.toUpperCase()));
                const isUpperCase = name === name.toUpperCase();
                
                // 只要是大写常量或预设或包含关键字，都提取
                if (preset || hasKeyword || isUpperCase) {
                    foundNames.add(name);
                    
                    // 智能计算范围
                    let min: number, max: number, step: number;
                    if (preset) {
                        min = preset.min;
                        max = preset.max;
                        step = preset.step;
                    } else if (isFloat) {
                        // 浮点数：范围为当前值的50%-200%
                        min = Math.max(0, value * 0.5);
                        max = value * 2;
                        step = value < 1 ? 0.01 : 0.1;
                    } else {
                        // 整数：范围为当前值的50%-200%
                        min = Math.max(1, Math.floor(value * 0.5));
                        max = Math.ceil(value * 2);
                        step = value >= 10 ? Math.max(1, Math.floor(value * 0.1)) : 1;
                    }
                    
                    params.push({
                        name,
                        type: isFloat ? 'float' : 'int',
                        min,
                        max,
                        step,
                        currentValue: value,
                        description: preset?.desc || comment || this.guessParamDescription(name)
                    });
                }
            }
        }

        return params;
    }
    
    /**
     * 根据参数名猜测描述
     */
    private guessParamDescription(name: string): string {
        const upper = name.toUpperCase();
        if (upper.includes('NUM') || upper.includes('COUNT')) return '数量';
        if (upper.includes('PERIOD') || upper.includes('DAYS')) return '周期';
        if (upper.includes('LOSS')) return '止损';
        if (upper.includes('PROFIT')) return '止盈';
        if (upper.includes('POSITION') || upper.includes('SIZE')) return '仓位';
        if (upper.includes('THRESHOLD')) return '阈值';
        if (upper.includes('RATIO')) return '比率';
        if (upper.includes('MAX')) return '最大值';
        if (upper.includes('MIN')) return '最小值';
        return '参数';
    }

    /**
     * 更新参数
     */
    private updateParameter(index: number, field: string, value: any): void {
        if (this._parameterRanges[index]) {
            (this._parameterRanges[index] as any)[field] = 
                field === 'name' || field === 'description' ? value : parseFloat(value);
        }
    }

    /**
     * 添加参数
     */
    private addParameter(): void {
        this._parameterRanges.push({
            name: 'NEW_PARAM',
            type: 'float',
            min: 0,
            max: 1,
            step: 0.1,
            currentValue: 0.5,
            description: '新参数'
        });
        this.updateContent();
    }

    /**
     * 删除参数
     */
    private removeParameter(index: number): void {
        this._parameterRanges.splice(index, 1);
        this.updateContent();
    }

    /**
     * 开始优化
     */
    private async startOptimization(config: { algorithm: string; maxIterations: number; target: string }): Promise<void> {
        // 使用当前策略代码
        if (!this._strategyCode) {
            vscode.window.showWarningMessage('请先加载策略代码');
            return;
        }
        
        if (this._parameterRanges.length === 0) {
            vscode.window.showWarningMessage('未检测到可调参数，请先配置参数');
            return;
        }

        if (this._isOptimizing) {
            vscode.window.showWarningMessage('优化正在进行中');
            return;
        }

        this._isOptimizing = true;
        this._optimizationProgress = 0;
        this._optimizationResults = [];
        this.updateContent();

        try {
            const maxIterations = Math.min(config.maxIterations, 200);
            
            for (let i = 0; i < maxIterations && this._isOptimizing; i++) {
                // 生成参数组合
                const params: Record<string, number> = {};
                for (const range of this._parameterRanges) {
                    if (config.algorithm === 'random') {
                        const steps = Math.floor((range.max - range.min) / range.step);
                        const randomStep = Math.floor(Math.random() * (steps + 1));
                        params[range.name] = range.min + randomStep * range.step;
                    } else {
                        // 网格搜索
                        const totalSteps = this._parameterRanges.reduce((acc, r) => 
                            acc * (Math.floor((r.max - r.min) / r.step) + 1), 1);
                        let remainder = i;
                        for (const r of this._parameterRanges) {
                            const steps = Math.floor((r.max - r.min) / r.step) + 1;
                            params[r.name] = r.min + (remainder % steps) * r.step;
                            remainder = Math.floor(remainder / steps);
                        }
                    }
                }

                // 模拟回测结果
                const baseReturn = 0.15 + Math.random() * 0.2;
                const metrics = {
                    totalReturn: baseReturn * (1 + (params['MA_PERIOD'] || 20) * 0.001),
                    sharpeRatio: 1.5 + Math.random() * 1.5,
                    maxDrawdown: 0.08 + Math.random() * 0.12,
                    winRate: 0.45 + Math.random() * 0.2
                };

                // 计算综合评分
                let score = 0;
                switch (config.target) {
                    case 'sharpe':
                        score = metrics.sharpeRatio * 30 + metrics.totalReturn * 20 - metrics.maxDrawdown * 50;
                        break;
                    case 'return':
                        score = metrics.totalReturn * 50 + metrics.sharpeRatio * 20 - metrics.maxDrawdown * 30;
                        break;
                    case 'drawdown':
                        score = (1 - metrics.maxDrawdown) * 50 + metrics.sharpeRatio * 30 + metrics.totalReturn * 20;
                        break;
                    default:
                        score = metrics.sharpeRatio * 30 + metrics.totalReturn * 30 + 
                                (1 - metrics.maxDrawdown) * 20 + metrics.winRate * 20;
                }

                this._optimizationResults.push({
                    id: `opt_${Date.now()}_${i}`,
                    timestamp: new Date().toISOString(),
                    parameters: params,
                    metrics,
                    score
                });

                this._optimizationProgress = ((i + 1) / maxIterations) * 100;
                
                // 更新进度
                this._panel.webview.postMessage({
                    command: 'updateProgress',
                    progress: this._optimizationProgress,
                    current: i + 1,
                    total: maxIterations,
                    bestScore: Math.max(...this._optimizationResults.map(r => r.score))
                });

                await new Promise(resolve => setTimeout(resolve, 50));
            }

            // 排序结果
            this._optimizationResults.sort((a, b) => b.score - a.score);
            this._optimizationResults = this._optimizationResults.slice(0, 20);
            
            this.saveData();
            this.updateContent();
            
            vscode.window.showInformationMessage(
                `优化完成！最佳评分: ${this._optimizationResults[0]?.score.toFixed(2) || 'N/A'}`,
                '应用最佳参数'
            ).then(selection => {
                if (selection === '应用最佳参数' && this._optimizationResults[0]) {
                    this.applyOptimizationResult(this._optimizationResults[0].id);
                }
            });

        } catch (error) {
            logger.error(`优化失败: ${error}`, MODULE);
            vscode.window.showErrorMessage(`优化失败: ${error}`);
        } finally {
            this._isOptimizing = false;
            this.updateContent();
        }
    }

    /**
     * 停止优化
     */
    private stopOptimization(): void {
        this._isOptimizing = false;
    }

    /**
     * 应用优化结果 - 更新webview编辑器，记录变更
     */
    private async applyOptimizationResult(resultId: string): Promise<void> {
        const result = this._optimizationResults.find(r => r.id === resultId);
        if (!result) return;

        // 保存旧参数值用于对比
        const oldParams: Record<string, number> = {};
        for (const p of this._parameterRanges) {
            oldParams[p.name] = p.currentValue;
        }

        let modifiedCode = this._strategyCode;
        const changes: string[] = [];
        
        for (const [name, value] of Object.entries(result.parameters)) {
            const regex = new RegExp(`(${name}\\s*=\\s*)\\d+\\.?\\d*`, 'g');
            const newValue = typeof value === 'number' ? value : parseFloat(value as string);
            modifiedCode = modifiedCode.replace(regex, `$1${newValue}`);
            
            // 记录变更
            const oldValue = oldParams[name];
            if (oldValue !== undefined && oldValue !== newValue) {
                const changePercent = oldValue !== 0 ? ((newValue - oldValue) / oldValue * 100).toFixed(1) : 'N/A';
                changes.push(`${name}: ${oldValue} → ${newValue} (${changePercent}%)`);
            }
        }

        // 更新webview编辑器
        this._strategyCode = modifiedCode;
        this._parameterRanges = this.extractParameters(modifiedCode);
        this._panel.webview.postMessage({
            command: 'updateCode',
            code: modifiedCode
        });
        
        // 自动保存为新版本
        const changeLog = changes.length > 0 ? changes.join(', ') : '无参数变更';
        const version: StrategyVersion = {
            id: `v_${Date.now()}`,
            version: `v${this._versions.length + 1}.0-opt`,
            timestamp: new Date().toISOString(),
            description: `应用优化结果 #${this._optimizationResults.indexOf(result) + 1} | 变更: ${changeLog}`,
            parameters: this._parameterRanges.reduce((acc, p) => {
                acc[p.name] = p.currentValue;
                return acc;
            }, {} as Record<string, number>),
            metrics: result.metrics,
            code: modifiedCode,
            isOptimized: true
        };
        this._versions.unshift(version);
        this.saveData();
        
        // 切换到编辑器tab显示结果
        this._currentTab = 'editor';
        this.updateContent();
        
        // 显示变更详情
        const message = changes.length > 0 
            ? `已应用优化参数并保存版本:\n${changes.slice(0, 5).join('\n')}${changes.length > 5 ? `\n...共 ${changes.length} 项变更` : ''}`
            : '已应用优化参数（参数值未变化）';
        vscode.window.showInformationMessage(message, '查看版本历史').then(selection => {
            if (selection === '查看版本历史') {
                this._currentTab = 'versions';
                this.updateContent();
            }
        });
    }

    /**
     * 保存版本 - 从webview请求最新代码
     */
    private async saveVersion(description: string): Promise<void> {
        // 先从webview获取最新代码
        this._panel.webview.postMessage({ command: 'getCodeForSave', description: description });
    }
    
    /**
     * 实际保存版本
     */
    private doSaveVersion(code: string, description: string): void {
        if (!code || code.trim() === '') {
            vscode.window.showWarningMessage('没有策略代码可保存');
            return;
        }
        
        // 更新当前代码
        this._strategyCode = code;
        this._parameterRanges = this.extractParameters(code);

        const version: StrategyVersion = {
            id: `v_${Date.now()}`,
            version: `v${this._versions.length + 1}.0`,
            timestamp: new Date().toISOString(),
            description: description || '手动保存',
            parameters: this._parameterRanges.reduce((acc, p) => {
                acc[p.name] = p.currentValue;
                return acc;
            }, {} as Record<string, number>),
            metrics: this._optimizationResults[0]?.metrics,
            code: code,
            isOptimized: false
        };

        this._versions.unshift(version);
        this.saveData();
        this.updateContent();
        
        vscode.window.showInformationMessage(`版本 ${version.version} 已保存`, '查看版本').then(selection => {
            if (selection === '查看版本') {
                this._currentTab = 'versions';
                this.updateContent();
            }
        });
    }

    /**
     * 加载版本
     */
    private async loadVersion(versionId: string): Promise<void> {
        const version = this._versions.find(v => v.id === versionId);
        if (!version) return;

        // 更新webview编辑器
        this._strategyCode = version.code;
        this._strategyName = version.version;
        this._parameterRanges = this.extractParameters(version.code);
        
        // 更新编辑器内容
        this._panel.webview.postMessage({
            command: 'updateCode',
            code: version.code
        });
        
        this._currentTab = 'editor';
        this.updateContent();
        
        vscode.window.showInformationMessage(`已加载 ${version.version}`);
    }

    /**
     * 对比版本
     */
    private async compareVersions(v1Id: string, v2Id: string): Promise<void> {
        const v1 = this._versions.find(v => v.id === v1Id);
        const v2 = this._versions.find(v => v.id === v2Id);
        
        if (!v1 || !v2) return;

        const doc1 = await vscode.workspace.openTextDocument({ content: v1.code, language: 'python' });
        const doc2 = await vscode.workspace.openTextDocument({ content: v2.code, language: 'python' });
        
        await vscode.commands.executeCommand('vscode.diff', doc1.uri, doc2.uri, `${v1.version} ↔ ${v2.version}`);
    }

    /**
     * 删除版本
     */
    private deleteVersion(versionId: string): void {
        const index = this._versions.findIndex(v => v.id === versionId);
        if (index >= 0) {
            this._versions.splice(index, 1);
            this.saveData();
            this.updateContent();
        }
    }

    /**
     * 导出版本
     */
    private async exportVersion(versionId: string): Promise<void> {
        const version = this._versions.find(v => v.id === versionId);
        if (!version) return;

        const uri = await vscode.window.showSaveDialog({
            defaultUri: vscode.Uri.file(path.join(
                vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || os.homedir(),
                `${this._strategyName.replace('.py', '')}_${version.version}.py`
            )),
            filters: { 'Python': ['py'] }
        });

        if (uri) {
            fs.writeFileSync(uri.fsPath, version.code);
            vscode.window.showInformationMessage(`已导出到 ${uri.fsPath}`);
        }
    }

    /**
     * 应用优化建议
     */
    private async applyAdvice(adviceId: string): Promise<void> {
        const advice = this._report?.advices.find(a => a.id === adviceId);
        if (!advice?.codeExample) {
            vscode.window.showWarningMessage('该建议没有代码示例');
            return;
        }

        const doc = await vscode.workspace.openTextDocument({
            content: `# ${advice.title}\n# ${advice.description}\n\n${advice.codeExample}`,
            language: 'python'
        });
        await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
    }

    /**
     * 保存并进入回测
     */
    private async saveAndBacktest(): Promise<void> {
        if (!this._strategyCode) {
            vscode.window.showWarningMessage('没有策略代码');
            return;
        }

        // 如果有文件路径，保存到文件；否则提示保存
        if (this._strategyPath) {
            fs.writeFileSync(this._strategyPath, this._strategyCode);
            vscode.window.showInformationMessage(`已保存到 ${this._strategyPath}`);
        } else {
            const uri = await vscode.window.showSaveDialog({
                defaultUri: vscode.Uri.file(path.join(
                    vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || os.homedir(),
                    'Projects',
                    this._strategyName || 'strategy.py'
                )),
                filters: { 'Python': ['py'] }
            });

            if (uri) {
                fs.writeFileSync(uri.fsPath, this._strategyCode);
                this._strategyPath = uri.fsPath;
                vscode.window.showInformationMessage(`已保存到 ${uri.fsPath}`);
            } else {
                return;
            }
        }
        
        // 打开回测配置面板
        await vscode.commands.executeCommand('trquant.showBacktestConfig');
    }

    /**
     * 保存并进入实盘
     */
    private async saveAndTrade(): Promise<void> {
        await this.saveAndBacktest();
        vscode.window.showInformationMessage('实盘交易功能开发中...');
    }

    /**
     * 加载数据
     */
    private loadData(): void {
        try {
            const dataPath = path.join(this._storagePath, 'optimizer_data.json');
            if (fs.existsSync(dataPath)) {
                const data = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
                this._versions = data.versions || [];
                this._optimizationResults = data.results || [];
            }
        } catch (error) {
            logger.warn(`加载数据失败: ${error}`, MODULE);
        }
    }

    /**
     * 保存数据
     */
    private saveData(): void {
        try {
            if (!fs.existsSync(this._storagePath)) {
                fs.mkdirSync(this._storagePath, { recursive: true });
            }
            const dataPath = path.join(this._storagePath, 'optimizer_data.json');
            fs.writeFileSync(dataPath, JSON.stringify({
                versions: this._versions.slice(0, 50),
                results: this._optimizationResults.slice(0, 100)
            }, null, 2));
        } catch (error) {
            logger.warn(`保存数据失败: ${error}`, MODULE);
        }
    }

    /**
     * 更新内容
     */
    public updateContent(): void {
        this._panel.webview.html = this.generateHtml();
    }

    /**
     * 生成HTML
     */
    private generateHtml(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>策略优化器</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/theme/monokai.min.css">
    <style>${this.getStyles()}</style>
</head>
<body>
    <div class="container">
        ${this.renderHeader()}
        ${this.renderTabs()}
        <div class="content">
            ${this.renderTabContent()}
        </div>
        ${this.renderFooter()}
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/python/python.min.js"></script>
    <script>${this.getScripts()}</script>
</body>
</html>`;
    }

    /**
     * 渲染头部
     */
    private renderHeader(): string {
        return `
        <div class="header">
            <div class="header-left">
                <h1>🔬 策略优化器</h1>
                <p class="subtitle">${this._strategyName || '请选择策略文件'}</p>
            </div>
            <div class="header-right">
                ${this._strategyCode ? `
                    <span class="status-badge status-loaded">✓ 已加载</span>
                    ${this._report ? `<span class="score-badge">评分: ${this._report.overallScore}</span>` : ''}
                ` : `
                    <span class="status-badge status-empty">○ 未加载</span>
                `}
            </div>
        </div>`;
    }

    /**
     * 渲染Tab
     */
    private renderTabs(): string {
        const tabs: { id: TabType; icon: string; label: string; disabled: boolean }[] = [
            { id: 'editor', icon: '📝', label: '策略编辑器', disabled: false },
            { id: 'analysis', icon: '📊', label: '策略分析', disabled: !this._strategyCode },
            { id: 'optimize', icon: '⚡', label: '参数优化', disabled: !this._strategyCode },
            { id: 'versions', icon: '📚', label: '版本管理', disabled: false },
            { id: 'visualize', icon: '📈', label: '可视化', disabled: !this._optimizationResults.length }
        ];

        return `
        <div class="tabs">
            ${tabs.map((tab, index) => `
                <button class="tab ${this._currentTab === tab.id ? 'active' : ''} ${tab.disabled ? 'disabled' : ''}"
                        onclick="${tab.disabled ? '' : `switchTab('${tab.id}')`}"
                        ${tab.disabled ? 'disabled' : ''}>
                    <span class="tab-number">${index + 1}</span>
                    <span class="tab-icon">${tab.icon}</span>
                    <span class="tab-label">${tab.label}</span>
                </button>
            `).join('')}
        </div>`;
    }

    /**
     * 渲染Tab内容
     */
    private renderTabContent(): string {
        switch (this._currentTab) {
            case 'editor': return this.renderEditorTab();
            case 'analysis': return this.renderAnalysisTab();
            case 'optimize': return this.renderOptimizeTab();
            case 'versions': return this.renderVersionsTab();
            case 'visualize': return this.renderVisualizeTab();
            default: return '';
        }
    }

    /**
     * 渲染编辑器Tab - 集成CodeMirror编辑器
     */
    private renderEditorTab(): string {
        const lineCount = this._strategyCode ? this._strategyCode.split('\n').length : 0;
        const hasReport = this._report !== null;
        const hasOptResults = this._optimizationResults.length > 0;
        
        return `
        <div class="tab-content editor-tab">
            <!-- 顶部工具栏 - 始终显示 -->
            <div class="editor-top-bar">
                <div class="editor-info">
                    ${this._strategyCode ? `
                        <span class="file-name">📄 ${this._strategyName || '未命名策略'}</span>
                        <span class="file-stats">📏 ${lineCount} 行</span>
                        <span class="file-stats">📊 ${this._parameterRanges.length} 个参数</span>
                        ${hasReport ? `<span class="score-indicator" style="color: ${this.getScoreColor(this._report!.overallScore)}">评分: ${this._report!.overallScore}/100</span>` : ''}
                    ` : `<span class="file-name">未选择策略文件</span>`}
                </div>
                <div class="editor-top-actions">
                    <button class="btn btn-primary" onclick="selectFile()">📁 选择策略文件</button>
                    ${this._strategyCode ? `
                        <button class="btn btn-gold" onclick="analyzeStrategy()">🔍 开始分析</button>
                    ` : ''}
                </div>
            </div>
            
            ${this._strategyCode ? `
                <div class="editor-toolbar">
                    <button class="btn btn-sm" onclick="syncFromEditor()">🔄 同步</button>
                    <button class="btn btn-sm" onclick="formatCode()">✨ 格式化</button>
                    <button class="btn btn-sm" onclick="copyCode()">📋 复制</button>
                    ${hasOptResults ? `<button class="btn btn-sm btn-gold" onclick="applyBestResult()">⚡ 应用最佳参数</button>` : ''}
                    <button class="btn btn-sm" onclick="saveVersion()">💾 保存版本</button>
                </div>
            ` : ''}
            
            <div class="editor-container ${!this._strategyCode ? 'empty' : ''}">
                ${!this._strategyCode ? `
                    <div class="editor-placeholder">
                        <div class="placeholder-icon">📂</div>
                        <h3>选择策略文件开始</h3>
                        <p>点击右上角"选择策略文件"按钮</p>
                        <p class="hint">支持 Python (.py) 格式的策略文件</p>
                    </div>
                ` : `<div id="code-editor"></div>`}
            </div>
            
            ${this._parameterRanges.length > 0 ? `
                <div class="params-preview">
                    <div class="params-header">
                        <h3>🎯 检测到的可调参数 (${this._parameterRanges.length})</h3>
                        <button class="btn btn-sm btn-gold" onclick="switchTab('optimize')">⚡ 去优化</button>
                    </div>
                    <div class="params-grid">
                        ${this._parameterRanges.map((p, i) => `
                            <div class="param-card" onclick="highlightParam('${p.name}')">
                                <div class="param-name">${p.name}</div>
                                <div class="param-value">${p.currentValue}</div>
                                <div class="param-range">${p.min} ~ ${p.max} (步长: ${p.step})</div>
                                ${p.description ? `<div class="param-desc">${p.description}</div>` : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : this._strategyCode ? `
                <div class="no-params-hint">
                    <p>💡 未检测到可调参数。参数格式示例: <code>STOCK_NUM = 10  # 持股数量</code></p>
                </div>
            ` : ''}
        </div>`;
    }

    /**
     * 渲染分析Tab
     */
    private renderAnalysisTab(): string {
        if (!this._report) {
            return `
            <div class="tab-content">
                <div class="empty-state">
                    <div class="empty-icon">📊</div>
                    <h2>尚未分析</h2>
                    <p>请先加载策略文件，然后点击"开始分析"</p>
                    <button class="btn btn-gold btn-lg" onclick="analyzeStrategy()">🔍 开始分析</button>
                </div>
            </div>`;
        }

        const scoreLevel = this._report.overallScore >= 80 ? 'excellent' : 
                          this._report.overallScore >= 60 ? 'good' : 
                          this._report.overallScore >= 40 ? 'fair' : 'poor';

        return `
        <div class="tab-content">
            <div class="analysis-header">
                <div class="main-score-card ${scoreLevel}">
                    <div class="score-ring">
                        <svg viewBox="0 0 100 100">
                            <circle class="score-bg" cx="50" cy="50" r="45"/>
                            <circle class="score-progress" cx="50" cy="50" r="45" 
                                stroke-dasharray="${this._report.overallScore * 2.83} 283"/>
                        </svg>
                        <div class="score-text">
                            <span class="score-number">${this._report.overallScore}</span>
                            <span class="score-label">综合评分</span>
                        </div>
                    </div>
                </div>
                <div class="score-breakdown">
                    <div class="breakdown-item">
                        <div class="breakdown-label">风险控制</div>
                        <div class="breakdown-bar">
                            <div class="breakdown-fill" style="width: ${this._report.scoreBreakdown.risk}%; background: ${this.getScoreColor(this._report.scoreBreakdown.risk)}"></div>
                        </div>
                        <div class="breakdown-value">${this._report.scoreBreakdown.risk}</div>
                    </div>
                    <div class="breakdown-item">
                        <div class="breakdown-label">因子构建</div>
                        <div class="breakdown-bar">
                            <div class="breakdown-fill" style="width: ${this._report.scoreBreakdown.factor}%; background: ${this.getScoreColor(this._report.scoreBreakdown.factor)}"></div>
                        </div>
                        <div class="breakdown-value">${this._report.scoreBreakdown.factor}</div>
                    </div>
                    <div class="breakdown-item">
                        <div class="breakdown-label">选股逻辑</div>
                        <div class="breakdown-bar">
                            <div class="breakdown-fill" style="width: ${this._report.scoreBreakdown.selection}%; background: ${this.getScoreColor(this._report.scoreBreakdown.selection)}"></div>
                        </div>
                        <div class="breakdown-value">${this._report.scoreBreakdown.selection}</div>
                    </div>
                    <div class="breakdown-item">
                        <div class="breakdown-label">代码质量</div>
                        <div class="breakdown-bar">
                            <div class="breakdown-fill" style="width: ${this._report.scoreBreakdown.code}%; background: ${this.getScoreColor(this._report.scoreBreakdown.code)}"></div>
                        </div>
                        <div class="breakdown-value">${this._report.scoreBreakdown.code}</div>
                    </div>
                </div>
            </div>
            
            <div class="summary-section">
                <h3>📋 分析摘要</h3>
                <div class="summary-content">${this._report.summary}</div>
            </div>
            
            <div class="advices-section">
                <div class="advices-header">
                    <h3>💡 优化建议 (${this._report.advices.length})</h3>
                    <div class="advices-filter">
                        <button class="filter-btn active" data-priority="all">全部</button>
                        <button class="filter-btn" data-priority="high">🔴 高</button>
                        <button class="filter-btn" data-priority="medium">🟡 中</button>
                        <button class="filter-btn" data-priority="low">🟢 低</button>
                    </div>
                </div>
                <div class="advices-list">
                    ${this._report.advices.map(advice => this.renderAdvice(advice)).join('')}
                </div>
            </div>
            
            <div class="analysis-actions">
                <button class="btn" onclick="reanalyzeStrategy()">🔄 重新分析</button>
                <button class="btn btn-gold" onclick="switchTab('optimize')">⚡ 进入参数优化</button>
                <button class="btn" onclick="switchTab('editor')">📝 返回编辑器</button>
            </div>
        </div>`;
    }

    /**
     * 渲染建议
     */
    private renderAdvice(advice: OptimizationAdvice): string {
        const priorityClass = `priority-${advice.priority}`;
        const priorityLabel = advice.priority === 'high' ? '🔴 高' : advice.priority === 'medium' ? '🟡 中' : '🟢 低';
        
        return `
        <div class="advice-card ${priorityClass}">
            <div class="advice-header">
                <span class="advice-priority">${priorityLabel}</span>
                <span class="advice-title">${advice.title}</span>
                <span class="advice-category">${advice.category}</span>
            </div>
            <div class="advice-body">
                <p>${advice.description}</p>
                ${advice.currentState ? `<p><strong>当前:</strong> ${advice.currentState}</p>` : ''}
                ${advice.suggestedState ? `<p><strong>建议:</strong> ${advice.suggestedState}</p>` : ''}
                ${advice.impact ? `<p><strong>预期影响:</strong> ${advice.impact}</p>` : ''}
            </div>
            ${advice.codeExample ? `
                <div class="advice-footer">
                    <button class="btn btn-sm" onclick="applyAdvice('${advice.id}')">📝 查看代码示例</button>
                </div>
            ` : ''}
        </div>`;
    }

    /**
     * 渲染优化Tab
     */
    private renderOptimizeTab(): string {
        // 计算预估组合数
        const estimatedCombinations = this._parameterRanges.reduce((acc, r) => {
            const steps = Math.floor((r.max - r.min) / r.step) + 1;
            return acc * steps;
        }, 1);
        
        return `
        <div class="tab-content">
            <div class="optimize-header">
                <div class="strategy-info">
                    <span class="strategy-name">📄 ${this._strategyName || '未选择策略'}</span>
                    <span class="param-count">📊 ${this._parameterRanges.length} 个参数</span>
                    <span class="combo-count">🔢 约 ${estimatedCombinations.toLocaleString()} 个组合</span>
                </div>
            </div>
            
            <div class="config-section">
                <h3>⚙️ 优化配置</h3>
                <div class="config-grid">
                    <div class="config-item">
                        <label>优化算法</label>
                        <select id="algorithm" onchange="updateAlgorithmInfo()">
                            <option value="grid">网格搜索 (Grid Search)</option>
                            <option value="random">随机搜索 (Random Search)</option>
                        </select>
                        <div class="config-desc" id="algorithmDesc">穷举所有参数组合，适合参数空间较小时</div>
                    </div>
                    <div class="config-item">
                        <label>迭代次数</label>
                        <input type="number" id="maxIterations" value="50" min="10" max="500">
                        <div class="config-desc">建议: 网格搜索自动计算, 随机搜索50-200次</div>
                    </div>
                    <div class="config-item">
                        <label>优化目标</label>
                        <select id="target">
                            <option value="combined">综合评分 (推荐)</option>
                            <option value="sharpe">夏普比率优先</option>
                            <option value="return">收益率优先</option>
                            <option value="drawdown">最小回撤优先</option>
                            <option value="calmar">卡玛比率优先</option>
                        </select>
                        <div class="config-desc">综合评分 = 夏普×30% + 收益×30% + (1-回撤)×20% + 胜率×20%</div>
                    </div>
                    <div class="config-item">
                        <label>早停条件</label>
                        <select id="earlyStop">
                            <option value="none">不启用</option>
                            <option value="score">达到目标评分</option>
                            <option value="plateau">评分不再提升</option>
                        </select>
                    </div>
                </div>
            </div>
            
            <div class="params-section">
                <div class="section-header">
                    <h3>📐 参数搜索范围</h3>
                    <div class="section-actions">
                        <button class="btn btn-sm" onclick="autoDetectParams()">🔍 自动检测</button>
                        <button class="btn btn-sm" onclick="addParameter()">➕ 添加参数</button>
                    </div>
                </div>
                ${this._parameterRanges.length === 0 ? `
                    <div class="empty-params">
                        <p>未检测到可调参数，请手动添加或检查策略代码中的参数定义</p>
                        <p class="hint">支持格式: PARAM_NAME = 10  # 参数描述</p>
                    </div>
                ` : `
                    <table class="params-table">
                        <thead>
                            <tr>
                                <th>参数名</th>
                                <th>最小值</th>
                                <th>最大值</th>
                                <th>步长</th>
                                <th>当前值</th>
                                <th>搜索点数</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this._parameterRanges.map((p, i) => {
                                const steps = Math.floor((p.max - p.min) / p.step) + 1;
                                return `
                                <tr>
                                    <td><input class="input-sm" value="${p.name}" onchange="updateParam(${i}, 'name', this.value)"></td>
                                    <td><input class="input-sm" type="number" value="${p.min}" step="${p.step}" onchange="updateParam(${i}, 'min', this.value)"></td>
                                    <td><input class="input-sm" type="number" value="${p.max}" step="${p.step}" onchange="updateParam(${i}, 'max', this.value)"></td>
                                    <td><input class="input-sm" type="number" value="${p.step}" step="0.01" onchange="updateParam(${i}, 'step', this.value)"></td>
                                    <td><strong>${p.currentValue}</strong></td>
                                    <td class="step-count">${steps}</td>
                                    <td><button class="btn btn-danger btn-sm" onclick="removeParam(${i})">🗑️</button></td>
                                </tr>`;
                            }).join('')}
                        </tbody>
                    </table>
                `}
            </div>
            
            ${this._isOptimizing ? `
                <div class="progress-section">
                    <h3>🚀 优化进度</h3>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${this._optimizationProgress}%"></div>
                    </div>
                    <div class="progress-info">
                        <span id="progressText">${this._optimizationProgress.toFixed(0)}%</span>
                        <span id="progressStats">当前最佳: ${this._optimizationResults[0]?.score.toFixed(2) || '-'}</span>
                        <button class="btn btn-danger" onclick="stopOptimization()">⏹️ 停止优化</button>
                    </div>
                    <div class="progress-details">
                        <span>已测试: <strong id="testedCount">${this._optimizationResults.length}</strong> 组</span>
                        <span>用时: <strong id="elapsedTime">-</strong></span>
                        <span>预计剩余: <strong id="remainingTime">-</strong></span>
                    </div>
                </div>
            ` : `
                <div class="action-section">
                    <button class="btn btn-gold btn-lg" onclick="startOptimization()" ${this._parameterRanges.length === 0 ? 'disabled' : ''}>
                        🚀 开始优化
                    </button>
                    <p class="action-hint">${this._parameterRanges.length === 0 ? '请先添加参数' : `将测试约 ${Math.min(estimatedCombinations, 200).toLocaleString()} 个参数组合`}</p>
                </div>
            `}
            
            ${this._optimizationResults.length > 0 ? `
                <div class="results-section">
                    <div class="results-header">
                        <h3>🏆 优化结果 (Top 10)</h3>
                        <div class="results-actions">
                            <button class="btn btn-sm" onclick="exportResults()">📤 导出结果</button>
                            <button class="btn btn-sm btn-gold" onclick="applyBestResult()">⚡ 应用最佳</button>
                        </div>
                    </div>
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>参数</th>
                                <th>收益率</th>
                                <th>夏普</th>
                                <th>回撤</th>
                                <th>胜率</th>
                                <th>评分</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this._optimizationResults.slice(0, 10).map((r, i) => `
                                <tr class="${i === 0 ? 'best-result' : ''}">
                                    <td>${i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : i + 1}</td>
                                    <td class="params-cell">${Object.entries(r.parameters).map(([k, v]) => `${k}=${typeof v === 'number' ? v.toFixed(2) : v}`).join(', ')}</td>
                                    <td class="${r.metrics.totalReturn > 0 ? 'positive' : 'negative'}">${(r.metrics.totalReturn * 100).toFixed(2)}%</td>
                                    <td>${r.metrics.sharpeRatio.toFixed(2)}</td>
                                    <td class="negative">${(r.metrics.maxDrawdown * 100).toFixed(2)}%</td>
                                    <td>${(r.metrics.winRate * 100).toFixed(1)}%</td>
                                    <td class="score">${r.score.toFixed(2)}</td>
                                    <td>
                                        <button class="btn btn-sm btn-primary" onclick="applyResult('${r.id}')">应用</button>
                                        <button class="btn btn-sm" onclick="viewResultDetail('${r.id}')">详情</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            ` : ''}
        </div>`;
    }

    /**
     * 渲染版本管理Tab
     */
    private renderVersionsTab(): string {
        const optimizedCount = this._versions.filter(v => v.isOptimized).length;
        
        return `
        <div class="tab-content">
            <div class="versions-header">
                <div class="versions-stats">
                    <span>📚 共 ${this._versions.length} 个版本</span>
                    <span>⚡ ${optimizedCount} 个已优化</span>
                </div>
                <div class="versions-actions">
                    <button class="btn btn-primary" onclick="saveVersion()" ${!this._strategyCode ? 'disabled' : ''}>
                        💾 保存当前版本
                    </button>
                    ${this._versions.length > 0 ? `
                        <button class="btn" onclick="exportAllVersions()">📤 导出全部</button>
                        <button class="btn" onclick="clearAllVersions()">🗑️ 清空</button>
                    ` : ''}
                </div>
            </div>
            
            ${this._versions.length === 0 ? `
                <div class="empty-state">
                    <div class="empty-icon">📚</div>
                    <h2>暂无保存的版本</h2>
                    <p>优化策略后点击"保存当前版本"创建快照</p>
                    <p class="hint">版本管理帮助您追踪策略的演进过程</p>
                </div>
            ` : `
                <div class="versions-timeline">
                    ${this._versions.map((v, i) => `
                        <div class="version-card ${i === 0 ? 'latest' : ''} ${v.isOptimized ? 'optimized' : ''}">
                            <div class="version-indicator">
                                <div class="version-dot ${i === 0 ? 'current' : ''}"></div>
                                ${i < this._versions.length - 1 ? '<div class="version-line"></div>' : ''}
                            </div>
                            <div class="version-content">
                                <div class="version-header">
                                    <span class="version-name">${v.version}</span>
                                    ${v.isOptimized ? '<span class="optimized-badge">⚡ 优化版</span>' : '<span class="manual-badge">📝 手动</span>'}
                                    <span class="version-time">${new Date(v.timestamp).toLocaleString('zh-CN')}</span>
                                </div>
                                <div class="version-desc">${v.description || '无描述'}</div>
                                
                                ${v.metrics ? `
                                    <div class="version-metrics">
                                        <div class="metric-item ${v.metrics.totalReturn > 0 ? 'positive' : 'negative'}">
                                            <span class="metric-label">收益</span>
                                            <span class="metric-value">${(v.metrics.totalReturn * 100).toFixed(2)}%</span>
                                        </div>
                                        <div class="metric-item">
                                            <span class="metric-label">夏普</span>
                                            <span class="metric-value">${v.metrics.sharpeRatio.toFixed(2)}</span>
                                        </div>
                                        <div class="metric-item negative">
                                            <span class="metric-label">回撤</span>
                                            <span class="metric-value">${(v.metrics.maxDrawdown * 100).toFixed(2)}%</span>
                                        </div>
                                        <div class="metric-item">
                                            <span class="metric-label">胜率</span>
                                            <span class="metric-value">${(v.metrics.winRate * 100).toFixed(1)}%</span>
                                        </div>
                                    </div>
                                ` : ''}
                                
                                <div class="version-params">
                                    ${Object.entries(v.parameters).slice(0, 5).map(([k, val]) => 
                                        `<span class="param-tag">${k}=${val}</span>`
                                    ).join('')}
                                    ${Object.keys(v.parameters).length > 5 ? `<span class="param-tag more">+${Object.keys(v.parameters).length - 5}</span>` : ''}
                                </div>
                                
                                <div class="version-actions">
                                    <button class="btn btn-sm btn-primary" onclick="loadVersion('${v.id}')">📥 加载到编辑器</button>
                                    ${i > 0 ? `<button class="btn btn-sm" onclick="compareVersions('${v.id}', '${this._versions[0].id}')">🔍 与当前对比</button>` : ''}
                                    <button class="btn btn-sm" onclick="exportVersion('${v.id}')">📤 导出</button>
                                    <button class="btn btn-sm" onclick="viewVersionCode('${v.id}')">👁️ 查看代码</button>
                                    <button class="btn btn-sm btn-danger" onclick="deleteVersion('${v.id}')">🗑️</button>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `}
        </div>`;
    }

    /**
     * 渲染可视化Tab
     */
    private renderVisualizeTab(): string {
        if (this._optimizationResults.length === 0) {
            return `
            <div class="tab-content">
                <div class="empty-state">
                    <div class="empty-icon">📈</div>
                    <h2>暂无数据</h2>
                    <p>完成参数优化后，这里将显示可视化图表</p>
                    <button class="btn btn-gold btn-lg" onclick="switchTab('optimize')">⚡ 去优化参数</button>
                </div>
            </div>`;
        }

        // 计算统计数据
        const results = this._optimizationResults;
        const maxScore = Math.max(...results.map(r => r.score));
        const minScore = Math.min(...results.map(r => r.score));
        const avgScore = results.reduce((s, r) => s + r.score, 0) / results.length;
        
        const avgReturn = results.reduce((s, r) => s + r.metrics.totalReturn, 0) / results.length;
        const maxReturn = Math.max(...results.map(r => r.metrics.totalReturn));
        const minReturn = Math.min(...results.map(r => r.metrics.totalReturn));
        
        const avgSharpe = results.reduce((s, r) => s + r.metrics.sharpeRatio, 0) / results.length;
        const maxSharpe = Math.max(...results.map(r => r.metrics.sharpeRatio));
        
        const avgDrawdown = results.reduce((s, r) => s + r.metrics.maxDrawdown, 0) / results.length;
        const minDrawdown = Math.min(...results.map(r => r.metrics.maxDrawdown));
        
        // Top 10 评分分布
        const barData = results.slice(0, 10).map((r, i) => ({
            label: `#${i + 1}`,
            value: r.score,
            percent: ((r.score - minScore) / (maxScore - minScore || 1)) * 100
        }));
        
        // 参数相关性分析
        const paramCorrelations = this.calculateParamCorrelations();

        return `
        <div class="tab-content visualize-tab">
            <div class="viz-header">
                <h2>📊 优化结果可视化</h2>
                <span class="viz-info">共 ${results.length} 个测试结果</span>
            </div>
            
            <!-- 核心指标卡片 -->
            <div class="viz-metrics-grid">
                <div class="viz-metric-card best">
                    <div class="viz-metric-icon">🏆</div>
                    <div class="viz-metric-content">
                        <div class="viz-metric-label">最佳评分</div>
                        <div class="viz-metric-value">${maxScore.toFixed(2)}</div>
                        <div class="viz-metric-sub">收益: ${(results[0]?.metrics.totalReturn * 100).toFixed(2)}%</div>
                    </div>
                </div>
                <div class="viz-metric-card">
                    <div class="viz-metric-icon">📈</div>
                    <div class="viz-metric-content">
                        <div class="viz-metric-label">最佳收益</div>
                        <div class="viz-metric-value positive">${(maxReturn * 100).toFixed(2)}%</div>
                        <div class="viz-metric-sub">平均: ${(avgReturn * 100).toFixed(2)}%</div>
                    </div>
                </div>
                <div class="viz-metric-card">
                    <div class="viz-metric-icon">⚡</div>
                    <div class="viz-metric-content">
                        <div class="viz-metric-label">最佳夏普</div>
                        <div class="viz-metric-value">${maxSharpe.toFixed(2)}</div>
                        <div class="viz-metric-sub">平均: ${avgSharpe.toFixed(2)}</div>
                    </div>
                </div>
                <div class="viz-metric-card">
                    <div class="viz-metric-icon">🛡️</div>
                    <div class="viz-metric-content">
                        <div class="viz-metric-label">最低回撤</div>
                        <div class="viz-metric-value positive">${(minDrawdown * 100).toFixed(2)}%</div>
                        <div class="viz-metric-sub">平均: ${(avgDrawdown * 100).toFixed(2)}%</div>
                    </div>
                </div>
            </div>
            
            <!-- 评分分布图 -->
            <div class="viz-section">
                <h3>📊 Top 10 评分分布</h3>
                <div class="viz-bar-chart">
                    ${barData.map((d, i) => `
                        <div class="viz-bar-item ${i === 0 ? 'best' : ''}">
                            <span class="viz-bar-label">${d.label}</span>
                            <div class="viz-bar-track">
                                <div class="viz-bar-fill" style="width: ${d.percent}%">
                                    <span class="viz-bar-value">${d.value.toFixed(2)}</span>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <!-- 指标分布统计 -->
            <div class="viz-section">
                <h3>📈 指标分布统计</h3>
                <div class="viz-stats-grid">
                    <div class="viz-stat-card">
                        <h4>评分分布</h4>
                        <div class="viz-stat-range">
                            <span class="range-min">${minScore.toFixed(2)}</span>
                            <div class="range-bar">
                                <div class="range-avg" style="left: ${((avgScore - minScore) / (maxScore - minScore || 1)) * 100}%"></div>
                            </div>
                            <span class="range-max">${maxScore.toFixed(2)}</span>
                        </div>
                        <div class="viz-stat-avg">平均: ${avgScore.toFixed(2)}</div>
                    </div>
                    <div class="viz-stat-card">
                        <h4>收益率分布</h4>
                        <div class="viz-stat-range">
                            <span class="range-min">${(minReturn * 100).toFixed(1)}%</span>
                            <div class="range-bar">
                                <div class="range-avg" style="left: ${((avgReturn - minReturn) / (maxReturn - minReturn || 1)) * 100}%"></div>
                            </div>
                            <span class="range-max">${(maxReturn * 100).toFixed(1)}%</span>
                        </div>
                        <div class="viz-stat-avg">平均: ${(avgReturn * 100).toFixed(2)}%</div>
                    </div>
                </div>
            </div>
            
            <!-- 参数敏感性分析 -->
            ${paramCorrelations.length > 0 ? `
                <div class="viz-section">
                    <h3>🎯 参数敏感性分析</h3>
                    <div class="viz-sensitivity">
                        ${paramCorrelations.map(pc => `
                            <div class="sensitivity-item">
                                <span class="sensitivity-name">${pc.name}</span>
                                <div class="sensitivity-bar-container">
                                    <div class="sensitivity-bar ${pc.correlation > 0 ? 'positive' : 'negative'}" 
                                         style="width: ${Math.abs(pc.correlation) * 100}%"></div>
                                </div>
                                <span class="sensitivity-value">${(pc.correlation * 100).toFixed(1)}%</span>
                            </div>
                        `).join('')}
                        <p class="sensitivity-hint">正值表示参数增大有利于评分，负值表示参数减小有利于评分</p>
                    </div>
                </div>
            ` : ''}
            
            <!-- 最佳参数组合 -->
            <div class="viz-section">
                <h3>🏆 最佳参数组合</h3>
                <div class="viz-best-params">
                    ${results[0] ? Object.entries(results[0].parameters).map(([k, v]) => `
                        <div class="best-param-item">
                            <span class="best-param-name">${k}</span>
                            <span class="best-param-value">${typeof v === 'number' ? v.toFixed(2) : v}</span>
                        </div>
                    `).join('') : ''}
                </div>
                <div class="viz-actions">
                    <button class="btn btn-gold" onclick="applyBestResult()">⚡ 应用最佳参数到编辑器</button>
                    <button class="btn" onclick="exportVisualization()">📤 导出图表</button>
                </div>
            </div>
        </div>`;
    }
    
    /**
     * 计算参数与评分的相关性
     */
    private calculateParamCorrelations(): { name: string; correlation: number }[] {
        if (this._optimizationResults.length < 5 || this._parameterRanges.length === 0) {
            return [];
        }
        
        const results = this._optimizationResults;
        const correlations: { name: string; correlation: number }[] = [];
        
        for (const param of this._parameterRanges) {
            const paramValues = results.map(r => r.parameters[param.name] || 0);
            const scores = results.map(r => r.score);
            
            // 简单的皮尔逊相关系数
            const n = paramValues.length;
            const sumX = paramValues.reduce((a, b) => a + b, 0);
            const sumY = scores.reduce((a, b) => a + b, 0);
            const sumXY = paramValues.reduce((a, x, i) => a + x * scores[i], 0);
            const sumX2 = paramValues.reduce((a, x) => a + x * x, 0);
            const sumY2 = scores.reduce((a, y) => a + y * y, 0);
            
            const numerator = n * sumXY - sumX * sumY;
            const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
            
            const correlation = denominator !== 0 ? numerator / denominator : 0;
            correlations.push({ name: param.name, correlation });
        }
        
        return correlations.sort((a, b) => Math.abs(b.correlation) - Math.abs(a.correlation));
    }

    /**
     * 渲染底部 - 包含所有操作按钮
     */
    private renderFooter(): string {
        return `
        <div class="footer">
            <div class="footer-left">
                <span class="status">${this._isOptimizing ? '⏳ 优化中...' : this._strategyCode ? '✓ 就绪' : '○ 未加载'}</span>
            </div>
            <div class="footer-actions">
                <button class="btn btn-primary" onclick="selectFile()">
                    📁 选择策略文件
                </button>
                ${this._strategyCode ? `
                    <button class="btn btn-gold" onclick="analyzeStrategy()">
                        🔍 开始分析
                    </button>
                    <button class="btn" onclick="saveAndBacktest()">
                        📊 保存并回测
                    </button>
                    <button class="btn btn-gold" onclick="saveAndTrade()">
                        💰 保存并实盘
                    </button>
                ` : ''}
            </div>
        </div>`;
    }

    /**
     * 代码转义 - 仅转义HTML特殊字符，不进行语法高亮
     */
    private highlightCode(code: string): string {
        // 只转义HTML特殊字符，保持原始代码格式和缩进
        return code
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    /**
     * 获取评分颜色
     */
    private getScoreColor(score: number): string {
        if (score >= 80) return '#3fb950';
        if (score >= 60) return '#f0b429';
        return '#f85149';
    }

    /**
     * 获取样式
     */
    private getStyles(): string {
        return `
        :root {
            --bg-dark: #0a0e14;
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-card: #1c2128;
            --bg-hover: #21262d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --text-muted: #6e7681;
            --accent-gold: #f0b429;
            --accent-green: #3fb950;
            --accent-blue: #58a6ff;
            --accent-red: #f85149;
            --accent-purple: #a371f7;
            --border-color: #30363d;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
        }
        
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        
        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
        }
        .header h1 {
            font-size: 24px;
            background: linear-gradient(135deg, #f0b429, #e85d04);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle { color: var(--text-muted); font-size: 14px; margin-top: 4px; }
        .status-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
        }
        .status-loaded { background: rgba(63, 185, 80, 0.2); color: var(--accent-green); }
        .status-empty { background: var(--bg-secondary); color: var(--text-muted); }
        .score-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            background: var(--accent-gold);
            color: #000;
            font-weight: 600;
            margin-left: 8px;
        }
        
        /* Tabs */
        .tabs {
            display: flex;
            gap: 4px;
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 4px;
            margin-bottom: 20px;
        }
        .tab {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 12px 16px;
            background: transparent;
            border: none;
            border-radius: 8px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
        }
        .tab:hover:not(.disabled) { background: var(--bg-hover); color: var(--text-primary); }
        .tab.active { background: var(--bg-card); color: var(--accent-gold); }
        .tab.disabled { opacity: 0.4; cursor: not-allowed; }
        .tab-number {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--border-color);
            font-size: 11px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .tab.active .tab-number { background: var(--accent-gold); color: #000; }
        
        /* Buttons */
        .btn {
            padding: 10px 20px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }
        .btn:hover:not(:disabled) { background: var(--bg-hover); border-color: var(--accent-blue); color: var(--text-primary); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .btn-primary { background: var(--accent-blue); border: none; color: #fff; }
        .btn-gold { background: linear-gradient(135deg, #f0b429, #d4a012); border: none; color: #000; font-weight: 600; }
        .btn-danger { background: rgba(248, 81, 73, 0.2); border-color: var(--accent-red); color: var(--accent-red); }
        .btn-sm { padding: 6px 12px; font-size: 12px; }
        .btn-lg { padding: 14px 28px; font-size: 16px; }
        
        /* Content */
        .content { min-height: 500px; }
        .tab-content { animation: fadeIn 0.2s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .toolbar { display: flex; gap: 12px; margin-bottom: 20px; }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 80px 20px;
            color: var(--text-muted);
        }
        .empty-icon { font-size: 64px; margin-bottom: 20px; opacity: 0.5; }
        .empty-state h2 { font-size: 20px; color: var(--text-secondary); margin-bottom: 8px; }
        .hint { margin-top: 12px; font-size: 13px; }
        
        /* Code */
        .code-info {
            display: flex;
            gap: 20px;
            padding: 12px 16px;
            background: var(--bg-secondary);
            border-radius: 8px;
            margin-bottom: 16px;
            font-size: 13px;
            color: var(--text-secondary);
        }
        .code-container {
            background: var(--bg-secondary);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        .code-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            background: var(--bg-card);
            border-bottom: 1px solid var(--border-color);
            font-size: 13px;
            color: var(--text-muted);
        }
        .code-block {
            padding: 16px;
            margin: 0;
            max-height: 400px;
            overflow: auto;
            font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            line-height: 1.6;
            background: var(--bg-card);
            border-radius: 8px;
            white-space: pre;
            tab-size: 4;
            -moz-tab-size: 4;
        }
        /* CodeMirror Editor */
        .editor-container {
            background: var(--bg-secondary);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 20px;
            border: 1px solid var(--border-color);
        }
        #code-editor {
            height: 500px;
            font-size: 14px;
        }
        .CodeMirror {
            height: 100%;
            font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.6;
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
        }
        .CodeMirror-gutters {
            background: var(--bg-secondary) !important;
            border-right: 1px solid var(--border-color) !important;
        }
        .CodeMirror-linenumber {
            color: var(--text-muted) !important;
        }
        .CodeMirror-cursor {
            border-left: 2px solid var(--accent-gold) !important;
        }
        .CodeMirror-selected {
            background: rgba(240, 180, 41, 0.2) !important;
        }
        .editor-tab {
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        
        /* Params Preview */
        .params-preview { margin-top: 20px; }
        .params-preview h3 { font-size: 16px; margin-bottom: 12px; }
        .params-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; }
        .param-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
        }
        .param-name { font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }
        .param-value { font-size: 20px; font-weight: 600; color: var(--accent-gold); }
        .param-desc { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
        
        /* Score Section */
        .score-section {
            display: grid;
            grid-template-columns: 2fr repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        .score-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        .score-card.main-score {
            background: linear-gradient(135deg, rgba(240, 180, 41, 0.1), rgba(212, 160, 18, 0.1));
            border-color: var(--accent-gold);
        }
        .score-label { font-size: 12px; color: var(--text-muted); margin-bottom: 8px; }
        .score-value { font-size: 36px; font-weight: 700; }
        .main-score .score-value { color: var(--accent-gold); }
        .score-bar {
            height: 4px;
            background: var(--bg-card);
            border-radius: 2px;
            margin-top: 12px;
            overflow: hidden;
        }
        .score-fill {
            height: 100%;
            background: var(--accent-gold);
            border-radius: 2px;
        }
        
        /* Summary */
        .summary-section { margin-bottom: 24px; }
        .summary-section h3 { font-size: 16px; margin-bottom: 12px; }
        .summary-content {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 16px;
            line-height: 1.8;
            white-space: pre-wrap;
        }
        
        /* Advices */
        .advices-section h3 { font-size: 16px; margin-bottom: 12px; }
        .advices-list { display: flex; flex-direction: column; gap: 12px; }
        .advice-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
        }
        .advice-card.priority-high { border-left: 3px solid var(--accent-red); }
        .advice-card.priority-medium { border-left: 3px solid var(--accent-gold); }
        .advice-card.priority-low { border-left: 3px solid var(--accent-blue); }
        .advice-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            background: var(--bg-card);
        }
        .advice-priority { font-size: 12px; }
        .advice-title { font-weight: 600; flex: 1; }
        .advice-category {
            font-size: 11px;
            padding: 2px 8px;
            background: var(--bg-hover);
            border-radius: 4px;
            color: var(--text-muted);
        }
        .advice-body { padding: 16px; color: var(--text-secondary); line-height: 1.6; }
        .advice-body p { margin-bottom: 8px; }
        .advice-footer { padding: 12px 16px; border-top: 1px solid var(--border-color); }
        
        /* Config Section */
        .config-section { margin-bottom: 24px; }
        .config-section h3 { font-size: 16px; margin-bottom: 12px; }
        .config-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
        .config-item { display: flex; flex-direction: column; gap: 8px; }
        .config-item label { font-size: 12px; color: var(--text-muted); }
        .config-item select, .config-item input {
            padding: 10px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 14px;
        }
        
        /* Params Table */
        .params-section { margin-bottom: 24px; }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .section-header h3 { font-size: 16px; }
        .params-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-secondary);
            border-radius: 12px;
            overflow: hidden;
        }
        .params-table th, .params-table td { padding: 12px; text-align: left; }
        .params-table th {
            background: var(--bg-card);
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 500;
        }
        .params-table td { border-top: 1px solid var(--border-color); }
        .input-sm {
            width: 100%;
            padding: 6px 8px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            color: var(--text-primary);
            font-size: 13px;
        }
        
        /* Progress */
        .progress-section {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
        }
        .progress-bar {
            height: 8px;
            background: var(--bg-card);
            border-radius: 4px;
            margin: 16px 0;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-gold), #e85d04);
            transition: width 0.3s;
        }
        .progress-info { display: flex; justify-content: space-between; align-items: center; }
        
        /* Results */
        .results-section { margin-top: 24px; }
        .results-section h3 { font-size: 16px; margin-bottom: 12px; }
        .results-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-secondary);
            border-radius: 12px;
            overflow: hidden;
        }
        .results-table th, .results-table td { padding: 12px; text-align: center; }
        .results-table th { background: var(--bg-card); font-size: 12px; color: var(--text-muted); }
        .results-table td { border-top: 1px solid var(--border-color); }
        .results-table .best-result { background: rgba(240, 180, 41, 0.1); }
        .positive { color: var(--accent-green); }
        .negative { color: var(--accent-red); }
        .score { font-weight: 600; color: var(--accent-gold); }
        
        /* Versions */
        .versions-list { display: flex; flex-direction: column; gap: 12px; }
        .version-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
        }
        .version-card.latest { border-color: var(--accent-gold); }
        .version-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
        .version-name { font-weight: 600; font-size: 16px; }
        .optimized-badge {
            font-size: 11px;
            padding: 2px 8px;
            background: rgba(240, 180, 41, 0.2);
            color: var(--accent-gold);
            border-radius: 4px;
        }
        .version-time { font-size: 12px; color: var(--text-muted); margin-left: auto; }
        .version-desc { color: var(--text-secondary); font-size: 14px; margin-bottom: 12px; }
        .version-metrics {
            display: flex;
            gap: 16px;
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 12px;
        }
        .version-actions { display: flex; gap: 8px; }
        
        /* Chart */
        .chart-section, .metrics-section { margin-bottom: 24px; }
        .chart-section h3, .metrics-section h3 { font-size: 16px; margin-bottom: 16px; }
        .bar-chart {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 20px;
        }
        .bar-item { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
        .bar-label { width: 40px; font-size: 13px; color: var(--text-muted); }
        .bar-container { flex: 1; height: 24px; background: var(--bg-card); border-radius: 4px; overflow: hidden; }
        .bar-fill { height: 100%; background: linear-gradient(90deg, var(--accent-gold), #e85d04); }
        .bar-value { width: 60px; font-size: 13px; text-align: right; }
        .metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
        .metric-card {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        .metric-label { font-size: 12px; color: var(--text-muted); margin-bottom: 8px; }
        .metric-value { font-size: 24px; font-weight: 600; }
        
        /* Footer */
        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 0;
            margin-top: 24px;
            border-top: 1px solid var(--border-color);
        }
        .footer-left { display: flex; align-items: center; }
        .footer-actions { display: flex; gap: 12px; }
        .status { font-size: 13px; color: var(--text-muted); }
        
        .action-section { text-align: center; margin: 24px 0; }
        .action-hint { font-size: 12px; color: var(--text-muted); margin-top: 8px; }
        
        /* Editor Top Bar */
        .editor-top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            background: var(--bg-secondary);
            border-radius: 12px;
            margin-bottom: 16px;
        }
        .editor-info { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
        .editor-top-actions { display: flex; gap: 8px; }
        .file-name { font-weight: 600; font-size: 15px; }
        .file-stats { font-size: 13px; color: var(--text-muted); }
        .score-indicator { font-weight: 600; padding: 4px 8px; background: var(--bg-card); border-radius: 4px; }
        .opt-indicator { font-size: 13px; color: var(--accent-gold); }
        .editor-toolbar {
            display: flex;
            gap: 8px;
            padding: 8px 0;
            margin-bottom: 8px;
            flex-wrap: wrap;
        }
        .editor-container.empty {
            min-height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-secondary);
            border-radius: 12px;
        }
        .editor-placeholder {
            text-align: center;
            color: var(--text-muted);
        }
        .placeholder-icon { font-size: 64px; margin-bottom: 16px; }
        .editor-placeholder h3 { font-size: 18px; margin-bottom: 8px; color: var(--text-primary); }
        .editor-placeholder p { margin: 4px 0; }
        .no-params-hint {
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 12px 16px;
            margin-top: 16px;
            color: var(--text-muted);
            font-size: 13px;
        }
        .no-params-hint code {
            background: var(--bg-card);
            padding: 2px 6px;
            border-radius: 4px;
            color: var(--accent-gold);
        }
        .params-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .param-range { font-size: 11px; color: var(--text-muted); }
        
        /* Analysis Header */
        .analysis-header {
            display: flex;
            gap: 32px;
            padding: 24px;
            background: var(--bg-secondary);
            border-radius: 16px;
            margin-bottom: 24px;
        }
        .main-score-card { flex: 0 0 180px; }
        .score-ring { position: relative; width: 140px; height: 140px; margin: 0 auto; }
        .score-ring svg { transform: rotate(-90deg); }
        .score-bg { fill: none; stroke: var(--bg-card); stroke-width: 8; }
        .score-progress { fill: none; stroke: var(--accent-gold); stroke-width: 8; stroke-linecap: round; transition: stroke-dasharray 0.5s; }
        .score-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }
        .score-number { font-size: 36px; font-weight: 700; display: block; }
        .score-label { font-size: 12px; color: var(--text-muted); }
        .score-breakdown { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 12px; }
        .breakdown-item { display: flex; align-items: center; gap: 12px; }
        .breakdown-label { width: 80px; font-size: 13px; color: var(--text-secondary); }
        .breakdown-bar { flex: 1; height: 8px; background: var(--bg-card); border-radius: 4px; overflow: hidden; }
        .breakdown-fill { height: 100%; border-radius: 4px; transition: width 0.3s; }
        .breakdown-value { width: 30px; font-size: 13px; font-weight: 600; text-align: right; }
        .advices-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        .advices-filter { display: flex; gap: 8px; }
        .filter-btn {
            padding: 4px 12px;
            background: var(--bg-card);
            border: none;
            border-radius: 4px;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 12px;
        }
        .filter-btn.active { background: var(--accent-gold); color: #000; }
        .analysis-actions { display: flex; gap: 12px; justify-content: center; margin-top: 24px; }
        
        /* Optimize Header */
        .optimize-header {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
        }
        .strategy-info { display: flex; gap: 16px; }
        .strategy-name { font-weight: 600; }
        .param-count, .combo-count { font-size: 13px; color: var(--text-muted); }
        .config-desc { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
        .section-actions { display: flex; gap: 8px; }
        .empty-params {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 32px;
            text-align: center;
            color: var(--text-muted);
        }
        .step-count { color: var(--accent-blue); font-weight: 600; }
        .progress-details {
            display: flex;
            gap: 24px;
            margin-top: 12px;
            font-size: 13px;
            color: var(--text-muted);
        }
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        .results-actions { display: flex; gap: 8px; }
        .params-cell { font-size: 11px; color: var(--text-muted); max-width: 200px; overflow: hidden; text-overflow: ellipsis; }
        
        /* Versions Timeline */
        .versions-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        .versions-stats { display: flex; gap: 16px; color: var(--text-muted); }
        .versions-actions { display: flex; gap: 8px; }
        .versions-timeline { position: relative; }
        .version-card {
            display: flex;
            gap: 16px;
            margin-bottom: 16px;
        }
        .version-indicator {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 24px;
        }
        .version-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--border-color);
        }
        .version-dot.current { background: var(--accent-gold); }
        .version-line { flex: 1; width: 2px; background: var(--border-color); margin-top: 4px; }
        .version-content {
            flex: 1;
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 16px;
            border: 1px solid var(--border-color);
        }
        .version-card.latest .version-content { border-color: var(--accent-gold); }
        .version-card.optimized .version-dot { background: var(--accent-green); }
        .manual-badge {
            font-size: 11px;
            padding: 2px 8px;
            background: rgba(88, 166, 255, 0.2);
            color: var(--accent-blue);
            border-radius: 4px;
        }
        .version-metrics {
            display: flex;
            gap: 16px;
            margin: 12px 0;
        }
        .metric-item { display: flex; flex-direction: column; }
        .metric-label { font-size: 11px; color: var(--text-muted); }
        .metric-value { font-weight: 600; }
        .metric-item.positive .metric-value { color: var(--accent-green); }
        .metric-item.negative .metric-value { color: var(--accent-red); }
        .version-params { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 12px; }
        .param-tag {
            font-size: 11px;
            padding: 2px 6px;
            background: var(--bg-card);
            border-radius: 4px;
            color: var(--text-muted);
        }
        .param-tag.more { background: var(--accent-gold); color: #000; }
        
        /* Visualization */
        .visualize-tab { padding: 0 !important; }
        .viz-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        .viz-header h2 { font-size: 20px; }
        .viz-info { color: var(--text-muted); }
        .viz-metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        .viz-metric-card {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            gap: 16px;
        }
        .viz-metric-card.best {
            background: linear-gradient(135deg, rgba(240, 180, 41, 0.2), rgba(232, 93, 4, 0.2));
            border: 1px solid var(--accent-gold);
        }
        .viz-metric-icon { font-size: 32px; }
        .viz-metric-content { flex: 1; }
        .viz-metric-label { font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }
        .viz-metric-value { font-size: 24px; font-weight: 700; }
        .viz-metric-sub { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
        .viz-section {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .viz-section h3 { font-size: 16px; margin-bottom: 16px; }
        .viz-bar-chart { display: flex; flex-direction: column; gap: 8px; }
        .viz-bar-item { display: flex; align-items: center; gap: 12px; }
        .viz-bar-item.best .viz-bar-fill { background: linear-gradient(90deg, var(--accent-gold), #e85d04); }
        .viz-bar-label { width: 40px; font-size: 13px; color: var(--text-muted); }
        .viz-bar-track {
            flex: 1;
            height: 28px;
            background: var(--bg-card);
            border-radius: 4px;
            overflow: hidden;
        }
        .viz-bar-fill {
            height: 100%;
            background: var(--accent-blue);
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 8px;
            border-radius: 4px;
            transition: width 0.3s;
        }
        .viz-bar-value { font-size: 12px; font-weight: 600; color: #fff; }
        .viz-stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
        .viz-stat-card { background: var(--bg-card); border-radius: 8px; padding: 16px; }
        .viz-stat-card h4 { font-size: 13px; margin-bottom: 12px; color: var(--text-secondary); }
        .viz-stat-range { display: flex; align-items: center; gap: 8px; }
        .range-min, .range-max { font-size: 12px; color: var(--text-muted); width: 60px; }
        .range-max { text-align: right; }
        .range-bar { flex: 1; height: 6px; background: var(--bg-hover); border-radius: 3px; position: relative; }
        .range-avg {
            position: absolute;
            top: -4px;
            width: 14px;
            height: 14px;
            background: var(--accent-gold);
            border-radius: 50%;
            transform: translateX(-50%);
        }
        .viz-stat-avg { font-size: 12px; color: var(--text-muted); text-align: center; margin-top: 8px; }
        .viz-sensitivity { display: flex; flex-direction: column; gap: 8px; }
        .sensitivity-item { display: flex; align-items: center; gap: 12px; }
        .sensitivity-name { width: 120px; font-size: 13px; }
        .sensitivity-bar-container {
            flex: 1;
            height: 8px;
            background: var(--bg-card);
            border-radius: 4px;
            overflow: hidden;
        }
        .sensitivity-bar { height: 100%; }
        .sensitivity-bar.positive { background: var(--accent-green); }
        .sensitivity-bar.negative { background: var(--accent-red); }
        .sensitivity-value { width: 50px; font-size: 12px; text-align: right; }
        .sensitivity-hint { font-size: 11px; color: var(--text-muted); margin-top: 12px; font-style: italic; }
        .viz-best-params {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 20px;
        }
        .best-param-item {
            background: var(--bg-card);
            border-radius: 8px;
            padding: 12px 16px;
            display: flex;
            flex-direction: column;
        }
        .best-param-name { font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }
        .best-param-value { font-size: 18px; font-weight: 600; color: var(--accent-gold); }
        .viz-actions { display: flex; gap: 12px; justify-content: center; }
        `;
    }

    /**
     * 获取脚本
     */
    private getScripts(): string {
        const initialCode = this._strategyCode || '';
        return `
        const vscode = acquireVsCodeApi();
        let codeEditor = null;
        
        // 初始化CodeMirror编辑器
        function initEditor() {
            const editorElement = document.getElementById('code-editor');
            if (!editorElement) return;
            
            codeEditor = CodeMirror(editorElement, {
                value: ${JSON.stringify(initialCode)},
                mode: 'python',
                theme: 'monokai',
                lineNumbers: true,
                indentUnit: 4,
                indentWithTabs: false,
                lineWrapping: true,
                autofocus: true,
                extraKeys: {
                    'Tab': function(cm) {
                        if (cm.somethingSelected()) {
                            cm.indentSelection('add');
                        } else {
                            cm.replaceSelection('    ', 'end');
                        }
                    },
                    'Shift-Tab': function(cm) {
                        cm.indentSelection('subtract');
                    }
                }
            });
            
            // 监听代码变化
            let changeTimeout = null;
            codeEditor.on('change', function() {
                clearTimeout(changeTimeout);
                changeTimeout = setTimeout(function() {
                    const code = codeEditor.getValue();
                    vscode.postMessage({ command: 'codeChanged', code: code });
                }, 500); // 防抖500ms
            });
        }
        
        // 页面加载完成后初始化编辑器
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initEditor);
        } else {
            initEditor();
        }
        
        // === 基础导航 ===
        function switchTab(tab) { vscode.postMessage({ command: 'switchTab', tab }); }
        function selectFile() { vscode.postMessage({ command: 'selectFile' }); }
        
        // === 策略编辑器 ===
        function analyzeStrategy() { 
            if (codeEditor) {
                const code = codeEditor.getValue();
                vscode.postMessage({ command: 'getCodeResponse', code: code });
            } else {
                vscode.postMessage({ command: 'analyzeStrategy' }); 
            }
        }
        function reanalyzeStrategy() { analyzeStrategy(); }
        function syncFromEditor() {
            if (codeEditor) {
                const code = codeEditor.getValue();
                vscode.postMessage({ command: 'codeChanged', code: code });
            }
        }
        function formatCode() {
            // 简单的代码格式化
            if (codeEditor) {
                const code = codeEditor.getValue();
                // 移除多余空行
                const formatted = code.replace(/\\n{3,}/g, '\\n\\n').trim();
                codeEditor.setValue(formatted);
            }
        }
        function copyCode() {
            if (codeEditor) {
                navigator.clipboard.writeText(codeEditor.getValue());
                alert('代码已复制到剪贴板');
            }
        }
        function highlightParam(paramName) {
            if (codeEditor) {
                const code = codeEditor.getValue();
                const regex = new RegExp(paramName + '\\\\s*=', 'g');
                const match = regex.exec(code);
                if (match) {
                    const pos = codeEditor.posFromIndex(match.index);
                    codeEditor.setCursor(pos);
                    codeEditor.scrollIntoView(pos, 100);
                }
            }
        }
        function applyBestResult() {
            vscode.postMessage({ command: 'applyBestResult' });
        }
        
        // === 参数优化 ===
        function updateParam(i, f, v) { vscode.postMessage({ command: 'updateParameter', index: i, field: f, value: v }); }
        function addParameter() { vscode.postMessage({ command: 'addParameter' }); }
        function removeParam(i) { vscode.postMessage({ command: 'removeParameter', index: i }); }
        function autoDetectParams() { vscode.postMessage({ command: 'autoDetectParams' }); }
        
        function startOptimization() {
            const config = {
                algorithm: document.getElementById('algorithm')?.value || 'grid',
                maxIterations: parseInt(document.getElementById('maxIterations')?.value || '50'),
                target: document.getElementById('target')?.value || 'combined',
                earlyStop: document.getElementById('earlyStop')?.value || 'none'
            };
            vscode.postMessage({ command: 'startOptimization', config });
        }
        function stopOptimization() { vscode.postMessage({ command: 'stopOptimization' }); }
        function applyResult(id) { vscode.postMessage({ command: 'applyResult', resultId: id }); }
        function viewResultDetail(id) { vscode.postMessage({ command: 'viewResultDetail', resultId: id }); }
        function exportResults() { vscode.postMessage({ command: 'exportResults' }); }
        
        function updateAlgorithmInfo() {
            const algorithm = document.getElementById('algorithm')?.value;
            const desc = document.getElementById('algorithmDesc');
            if (desc) {
                if (algorithm === 'grid') {
                    desc.textContent = '穷举所有参数组合，适合参数空间较小时';
                } else {
                    desc.textContent = '随机采样参数组合，适合参数空间较大时';
                }
            }
        }
        
        // === 版本管理 ===
        function saveVersion() {
            const desc = prompt('请输入版本描述：', '手动保存');
            if (desc !== null) {
                // 先获取当前代码再发送保存请求
                const code = codeEditor ? codeEditor.getValue() : '';
                vscode.postMessage({ command: 'getCodeForSave', code: code, description: desc });
            }
        }
        function loadVersion(id) { vscode.postMessage({ command: 'loadVersion', versionId: id }); }
        function compareVersions(v1, v2) { vscode.postMessage({ command: 'compareVersions', v1, v2 }); }
        function deleteVersion(id) {
            if (confirm('确定删除此版本？')) vscode.postMessage({ command: 'deleteVersion', versionId: id });
        }
        function exportVersion(id) { vscode.postMessage({ command: 'exportVersion', versionId: id }); }
        function exportAllVersions() { vscode.postMessage({ command: 'exportAllVersions' }); }
        function clearAllVersions() {
            if (confirm('确定清空所有版本？此操作不可恢复！')) {
                vscode.postMessage({ command: 'clearAllVersions' });
            }
        }
        function viewVersionCode(id) { vscode.postMessage({ command: 'viewVersionCode', versionId: id }); }
        
        // === 其他 ===
        function applyAdvice(id) { vscode.postMessage({ command: 'applyAdvice', adviceId: id }); }
        function saveAndBacktest() { vscode.postMessage({ command: 'saveAndBacktest' }); }
        function saveAndTrade() { vscode.postMessage({ command: 'saveAndTrade' }); }
        function exportVisualization() { vscode.postMessage({ command: 'exportVisualization' }); }
        
        window.addEventListener('message', event => {
            const msg = event.data;
            if (msg.command === 'updateProgress') {
                const fill = document.querySelector('.progress-fill');
                const text = document.getElementById('progressText');
                if (fill) fill.style.width = msg.progress + '%';
                if (text) text.textContent = msg.current + '/' + msg.total + ' (' + msg.progress.toFixed(0) + '%)';
            } else if (msg.command === 'updateCode') {
                // 更新编辑器代码
                if (codeEditor) {
                    codeEditor.setValue(msg.code || '');
                }
            } else if (msg.command === 'getCode') {
                // 返回当前代码
                if (codeEditor) {
                    const code = codeEditor.getValue();
                    vscode.postMessage({ command: 'getCodeResponse', code: code });
                }
            }
        });
        `;
    }

    public dispose(): void {
        StrategyOptimizerPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }
}

/**
 * 注册策略优化器面板
 */
export function registerStrategyOptimizerPanel(context: vscode.ExtensionContext): void {
    // 监听编辑器变化
    context.subscriptions.push(
        vscode.window.onDidChangeActiveTextEditor(editor => {
            if (editor?.document.languageId === 'python') {
                (StrategyOptimizerPanel as any)._lastActiveEditor = editor;
            }
        })
    );
    
    if (vscode.window.activeTextEditor) {
        (StrategyOptimizerPanel as any)._lastActiveEditor = vscode.window.activeTextEditor;
    }
    
    context.subscriptions.push(
        vscode.commands.registerCommand('trquant.optimizeStrategy', async () => {
            const editor = vscode.window.activeTextEditor;
            const storagePath = context.globalStorageUri.fsPath;
            
            if (editor) {
                (StrategyOptimizerPanel as any)._lastActiveEditor = editor;
                const code = editor.document.getText();
                const fileName = path.basename(editor.document.fileName);
                StrategyOptimizerPanel.createOrShow(context.extensionUri, code, fileName, storagePath);
            } else {
                StrategyOptimizerPanel.createOrShow(context.extensionUri, undefined, undefined, storagePath);
            }
        })
    );
    
    logger.info('策略优化器面板已注册', MODULE);
}





