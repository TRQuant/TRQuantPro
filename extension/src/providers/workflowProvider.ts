/**
 * TRQuant 工作流提供者
 * ====================
 *
 * 提供按8步工作流顺序排列的树视图
 */

import * as vscode from 'vscode';

export class WorkflowProvider implements vscode.TreeDataProvider<WorkflowItem> {
  private _onDidChangeTreeData: vscode.EventEmitter<WorkflowItem | undefined | null | void> =
    new vscode.EventEmitter<WorkflowItem | undefined | null | void>();
  readonly onDidChangeTreeData: vscode.Event<WorkflowItem | undefined | null | void> =
    this._onDidChangeTreeData.event;

  constructor(private context: vscode.ExtensionContext) {}

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: WorkflowItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: WorkflowItem): Thenable<WorkflowItem[]> {
    if (element) {
      // 子项
      return Promise.resolve(element.children || []);
    }

    // 根节点 - 8步工作流
    const items: WorkflowItem[] = [
      // 数据与分析阶段
      new WorkflowItem(
        '📡 1. 数据中心',
        '更新数据库和知识库',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openDataCenter',
        [
          new WorkflowItem(
            '数据源配置',
            '配置行情、财务数据源',
            vscode.TreeItemCollapsibleState.None,
            'trquant.openDataSource'
          ),
          new WorkflowItem(
            '数据更新',
            '增量更新历史数据',
            vscode.TreeItemCollapsibleState.None,
            'trquant.updateData'
          ),
          new WorkflowItem(
            '知识库',
            '管理策略知识库',
            vscode.TreeItemCollapsibleState.None,
            'trquant.openKnowledgeBase'
          ),
          new WorkflowItem(
            '质量报告',
            '查看数据完整性',
            vscode.TreeItemCollapsibleState.None,
            'trquant.dataQuality'
          ),
        ]
      ),
      new WorkflowItem(
        '📈 2. 市场分析',
        '分析市场趋势和状态',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openMarketAnalysis',
        [
          new WorkflowItem(
            '市场状态',
            '当前 Regime 判断',
            vscode.TreeItemCollapsibleState.None,
            'trquant.getMarketStatus'
          ),
          new WorkflowItem(
            '指数趋势',
            '主要指数走势分析',
            vscode.TreeItemCollapsibleState.None,
            'trquant.indexTrend'
          ),
          new WorkflowItem(
            '板块轮动',
            '行业板块强弱',
            vscode.TreeItemCollapsibleState.None,
            'trquant.sectorRotation'
          ),
          new WorkflowItem(
            '情绪指标',
            '市场情绪监控',
            vscode.TreeItemCollapsibleState.None,
            'trquant.sentiment'
          ),
        ]
      ),
      new WorkflowItem(
        '🔥 3. 投资主线',
        '识别市场热点和投资主线',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openMainlines',
        [
          new WorkflowItem(
            '热点主线',
            '当前热门投资主线',
            vscode.TreeItemCollapsibleState.None,
            'trquant.getMainlines'
          ),
          new WorkflowItem(
            '历史主线',
            '历史主线回顾',
            vscode.TreeItemCollapsibleState.None,
            'trquant.historyMainlines'
          ),
          new WorkflowItem(
            'LLM 分析',
            'AI 辅助主线解读',
            vscode.TreeItemCollapsibleState.None,
            'trquant.llmMainlines'
          ),
        ]
      ),
      new WorkflowItem(
        '📦 4. 候选池',
        '构建股票候选池',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openCandidatePool',
        [
          new WorkflowItem(
            '候选股票',
            '查看候选池股票',
            vscode.TreeItemCollapsibleState.None,
            'trquant.viewCandidates'
          ),
          new WorkflowItem(
            '筛选规则',
            '配置筛选条件',
            vscode.TreeItemCollapsibleState.None,
            'trquant.filterRules'
          ),
          new WorkflowItem(
            '关注列表',
            '个人关注股票',
            vscode.TreeItemCollapsibleState.None,
            'trquant.watchlist'
          ),
        ]
      ),

      // 策略与交易阶段
      new WorkflowItem(
        '📊 5. 因子中心',
        '构建和优化量化因子',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openFactorCenter',
        [
          new WorkflowItem(
            '因子库',
            '查看可用因子',
            vscode.TreeItemCollapsibleState.None,
            'trquant.factorLibrary'
          ),
          new WorkflowItem(
            '因子检验',
            'IC/IR 分析',
            vscode.TreeItemCollapsibleState.None,
            'trquant.factorTest'
          ),
          new WorkflowItem(
            '因子推荐',
            '基于市场状态推荐',
            vscode.TreeItemCollapsibleState.None,
            'trquant.recommendFactors'
          ),
        ]
      ),
      new WorkflowItem(
        '🛠️ 6. 策略开发',
        '开发和优化交易策略',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openStrategyDev',
        [
          new WorkflowItem(
            '创建项目',
            '新建量化策略项目',
            vscode.TreeItemCollapsibleState.None,
            'trquant.createProject'
          ),
          new WorkflowItem(
            '策略编辑器',
            '编辑策略代码',
            vscode.TreeItemCollapsibleState.None,
            'trquant.openStrategyOptimizer'
          ),
          new WorkflowItem(
            '参数优化',
            '策略参数搜索',
            vscode.TreeItemCollapsibleState.None,
            'trquant.optimizeStrategy'
          ),
          new WorkflowItem(
            'AI 生成',
            'LLM 辅助生成策略',
            vscode.TreeItemCollapsibleState.None,
            'trquant.generateStrategy'
          ),
        ]
      ),
      new WorkflowItem(
        '🔄 7. 回测中心',
        '回测验证和结果分析',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openBacktestCenter',
        [
          new WorkflowItem(
            '运行回测',
            '配置并执行回测',
            vscode.TreeItemCollapsibleState.None,
            'trquant.runBacktest'
          ),
          new WorkflowItem(
            '历史回测',
            '查看历史回测记录',
            vscode.TreeItemCollapsibleState.None,
            'trquant.backtestHistory'
          ),
          new WorkflowItem(
            '结果分析',
            '深入分析回测结果',
            vscode.TreeItemCollapsibleState.None,
            'trquant.analyzeBacktest'
          ),
          new WorkflowItem(
            '对比分析',
            '多策略对比',
            vscode.TreeItemCollapsibleState.None,
            'trquant.compareBacktests'
          ),
        ]
      ),
      new WorkflowItem(
        '🚀 8. 交易中心',
        '实盘模拟和实盘交易',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openTradingCenter',
        [
          new WorkflowItem(
            '模拟交易',
            '策略模拟验证',
            vscode.TreeItemCollapsibleState.None,
            'trquant.paperTrading'
          ),
          new WorkflowItem(
            '实盘部署',
            '部署到交易系统',
            vscode.TreeItemCollapsibleState.None,
            'trquant.deployStrategy'
          ),
          new WorkflowItem(
            '交易监控',
            '实时监控面板',
            vscode.TreeItemCollapsibleState.None,
            'trquant.tradingMonitor'
          ),
          new WorkflowItem(
            '风控管理',
            '风险控制设置',
            vscode.TreeItemCollapsibleState.None,
            'trquant.riskControl'
          ),
        ]
      ),
    ];

    return Promise.resolve(items);
  }
}

export class WorkflowItem extends vscode.TreeItem {
  children?: WorkflowItem[];

  constructor(
    public readonly label: string,
    public readonly description: string,
    public readonly collapsibleState: vscode.TreeItemCollapsibleState,
    public readonly commandId?: string,
    children?: WorkflowItem[]
  ) {
    super(label, collapsibleState);
    this.description = description;
    this.children = children;

    if (commandId) {
      this.command = {
        command: commandId,
        title: label,
        arguments: [],
      };
    }

    // 设置图标
    this.iconPath = this.getIcon();
    this.contextValue = 'workflowItem';
  }

  private getIcon(): vscode.ThemeIcon | undefined {
    const iconMap: Record<string, string> = {
      '📡 1. 数据中心': 'database',
      '📈 2. 市场分析': 'graph-line',
      '🔥 3. 投资主线': 'flame',
      '📦 4. 候选池': 'package',
      '📊 5. 因子中心': 'symbol-variable',
      '🛠️ 6. 策略开发': 'tools',
      '🔄 7. 回测中心': 'history',
      '🚀 8. 交易中心': 'rocket',
    };

    const iconName = iconMap[this.label];
    if (iconName) {
      return new vscode.ThemeIcon(iconName);
    }

    // 子项图标
    if (this.collapsibleState === vscode.TreeItemCollapsibleState.None) {
      return new vscode.ThemeIcon('circle-small');
    }

    return undefined;
  }
}

/**
 * 注册工作流提供者
 */
export function registerWorkflowProvider(context: vscode.ExtensionContext): WorkflowProvider {
  const provider = new WorkflowProvider(context);

  const treeView = vscode.window.createTreeView('trquant-workflow', {
    treeDataProvider: provider,
    showCollapseAll: true,
  });

  context.subscriptions.push(treeView);

  console.log('[TRQuant] 工作流提供者已注册');
  return provider;
}
