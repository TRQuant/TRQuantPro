/**
 * TRQuant 侧栏视图提供者
 */

import * as vscode from 'vscode';

class SidebarItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly command?: vscode.Command,
        public readonly icon?: string
    ) {
        super(label, collapsibleState);
        if (icon) this.iconPath = new vscode.ThemeIcon(icon);
        if (command) this.command = command;
    }
}

export class WorkflowSidebarProvider implements vscode.TreeDataProvider<SidebarItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<SidebarItem | undefined>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    refresh(): void { this._onDidChangeTreeData.fire(undefined); }
    getTreeItem(element: SidebarItem): vscode.TreeItem { return element; }

    getChildren(): Thenable<SidebarItem[]> {
        return Promise.resolve([
            new SidebarItem('🐉 打开 React 仪表板', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openReactPanel', title: '打开 React 仪表板' }, 'browser'),
            new SidebarItem('🏠 打开统一仪表板（旧版）', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openUnifiedDashboard', title: '打开统一仪表板（旧版）' }, 'home'),
            new SidebarItem('📊 9步投资工作流', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openWorkflowPanel', title: '打开工作流面板' }, 'list-ordered'),
            new SidebarItem('⚡ 快速工作流', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openWorkflowMVP', title: '打开快速工作流' }, 'zap')
        ]);
    }
}

export class TenbaggerSidebarProvider implements vscode.TreeDataProvider<SidebarItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<SidebarItem | undefined>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    refresh(): void { this._onDidChangeTreeData.fire(undefined); }
    getTreeItem(element: SidebarItem): vscode.TreeItem { return element; }

    getChildren(): Thenable<SidebarItem[]> {
        return Promise.resolve([
            new SidebarItem('🎯 十倍股仪表盘', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openTenbaggerDashboard', title: '打开十倍股仪表盘' }, 'rocket'),
            new SidebarItem('🔗 产业链图谱', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openIndustryChain', title: '打开产业链图谱' }, 'graph'),
            new SidebarItem('📋 股票详情', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openStockDetail', title: '打开股票详情' }, 'info')
        ]);
    }
}

export class StrategySidebarProvider implements vscode.TreeDataProvider<SidebarItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<SidebarItem | undefined>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

    refresh(): void { this._onDidChangeTreeData.fire(undefined); }
    getTreeItem(element: SidebarItem): vscode.TreeItem { return element; }

    getChildren(): Thenable<SidebarItem[]> {
        return Promise.resolve([
            new SidebarItem('⚙️ 策略生成器', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openStrategyGenerator', title: '打开策略生成器' }, 'gear'),
            new SidebarItem('🧪 回测面板', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openBacktestPanel', title: '打开回测面板' }, 'beaker'),
            new SidebarItem('🎛️ 策略优化器', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openOptimizerPanel', title: '打开策略优化器' }, 'settings-gear'),
            new SidebarItem('📊 结果管理', vscode.TreeItemCollapsibleState.None,
                { command: 'trquant.openResultManager', title: '打开结果管理' }, 'list-flat')
        ]);
    }
}

export class UnifiedPanelProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'trquant-unified-panel';
    private _view?: vscode.WebviewView;

    constructor(private readonly _extensionUri: vscode.Uri) {}

    public resolveWebviewView(webviewView: vscode.WebviewView) {
        this._view = webviewView;
        webviewView.webview.options = { enableScripts: true, localResourceRoots: [this._extensionUri] };
        webviewView.webview.html = this._getHtmlContent();

        webviewView.webview.onDidReceiveMessage(data => {
            switch (data.command) {
                case 'openReactPanel': vscode.commands.executeCommand('trquant.openReactPanel'); break;
                case 'openUnifiedDashboard': vscode.commands.executeCommand('trquant.openUnifiedDashboard'); break;
                case 'openWorkflow': vscode.commands.executeCommand('trquant.openWorkflowPanel'); break;
                case 'openTenbagger': vscode.commands.executeCommand('trquant.openTenbaggerDashboard'); break;
                case 'openStrategy': vscode.commands.executeCommand('trquant.openStrategyGenerator'); break;
            }
        });
    }

    private _getHtmlContent(): string {
        return `<!DOCTYPE html>
<html><head><style>
body { padding: 8px; font-family: var(--vscode-font-family); color: var(--vscode-foreground); }
.btn { display: flex; align-items: center; gap: 8px; width: 100%; padding: 10px 12px; margin-bottom: 8px; background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; border-radius: 4px; cursor: pointer; font-size: 13px; text-align: left; }
.btn:hover { background: var(--vscode-button-hoverBackground); }
.btn.secondary { background: var(--vscode-button-secondaryBackground); color: var(--vscode-button-secondaryForeground); }
.divider { height: 1px; background: var(--vscode-panel-border); margin: 12px 0; }
.section-title { font-size: 11px; text-transform: uppercase; color: var(--vscode-descriptionForeground); margin-bottom: 8px; font-weight: 600; }
</style></head><body>
<button class="btn" onclick="send('openReactPanel')"><span>🐉</span><span>打开 React 仪表板（新版）</span></button>
<button class="btn secondary" onclick="send('openUnifiedDashboard')"><span>🏠</span><span>打开统一仪表板（旧版）</span></button>
<div class="divider"></div>
<div class="section-title">快捷入口</div>
<button class="btn secondary" onclick="send('openWorkflow')"><span>📊</span><span>9步工作流</span></button>
<button class="btn secondary" onclick="send('openTenbagger')"><span>🎯</span><span>十倍股识别</span></button>
<button class="btn secondary" onclick="send('openStrategy')"><span>📈</span><span>策略生成</span></button>
<script>const vscode = acquireVsCodeApi(); function send(cmd) { vscode.postMessage({ command: cmd }); }</script>
</body></html>`;
    }
}

export function registerSidebarProviders(context: vscode.ExtensionContext): void {
    const unifiedPanelProvider = new UnifiedPanelProvider(context.extensionUri);
    context.subscriptions.push(vscode.window.registerWebviewViewProvider(UnifiedPanelProvider.viewType, unifiedPanelProvider));
    context.subscriptions.push(vscode.window.registerTreeDataProvider('trquant-workflow', new WorkflowSidebarProvider()));
    context.subscriptions.push(vscode.window.registerTreeDataProvider('trquant-tenbagger', new TenbaggerSidebarProvider()));
    context.subscriptions.push(vscode.window.registerTreeDataProvider('trquant-strategy', new StrategySidebarProvider()));
    console.log('[TRQuant] 已注册所有侧栏视图');
}
