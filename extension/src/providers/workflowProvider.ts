/**
 * TRQuant 工作流提供者
 * ====================
 *
 * 正确的9步投资工作流（基于 INSTALL_9STEPS.md 文档）
 * 
 * 步骤：信息获取 → 市场趋势 → 投资主线 → 候选池构建 → 因子构建 → 策略生成 → 回测验证 → 策略优化 → 报告生成
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
      return Promise.resolve(element.children || []);
    }

    // 正确的9步投资工作流（基于文档定义）
    const items: WorkflowItem[] = [
      // 主工作流面板入口
      new WorkflowItem(
        '🐉 韬睿量化投资流程',
        '打开完整9步工作流面板',
        vscode.TreeItemCollapsibleState.None,
        'trquant.openWorkflowPanel'
      ),
      new WorkflowItem(
        '━━━━━━━━━━━━━━━',
        '9步投资工作流',
        vscode.TreeItemCollapsibleState.None
      ),
      
      // 步骤1：信息获取
      new WorkflowItem(
        '📡 1. 信息获取',
        '数据源检测、数据更新',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openWorkflowPanel',
        [
          new WorkflowItem('数据源配置', '配置行情、财务数据源', vscode.TreeItemCollapsibleState.None, 'trquant.openWorkflowPanel'),
          new WorkflowItem('数据更新', '增量更新历史数据', vscode.TreeItemCollapsibleState.None, 'trquant.openWorkflowPanel'),
          new WorkflowItem('知识库', '管理策略知识库', vscode.TreeItemCollapsibleState.None, 'trquant.openWorkflowPanel'),
          new WorkflowItem('质量报告', '查看数据完整性', vscode.TreeItemCollapsibleState.None, 'trquant.openWorkflowPanel'),
        ]
      ),
      
      // 步骤2：市场趋势
      new WorkflowItem(
        '📈 2. 市场趋势',
        '市场状态判断、趋势分析',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.getMarketStatus',
        [
          new WorkflowItem('市场状态', '当前 Regime 判断', vscode.TreeItemCollapsibleState.None, 'trquant.getMarketStatus'),
          new WorkflowItem('指数趋势', '主要指数走势分析', vscode.TreeItemCollapsibleState.None, 'trquant.getMarketStatus'),
          new WorkflowItem('板块轮动', '行业板块强弱', vscode.TreeItemCollapsibleState.None, 'trquant.getMarketStatus'),
          new WorkflowItem('情绪指标', '市场情绪监控', vscode.TreeItemCollapsibleState.None, 'trquant.getMarketStatus'),
        ]
      ),
      
      // 步骤3：投资主线
      new WorkflowItem(
        '🔥 3. 投资主线',
        '主线识别、主线评分',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.getMainlines',
        [
          new WorkflowItem('热点主线', '当前热门投资主线', vscode.TreeItemCollapsibleState.None, 'trquant.getMainlines'),
          new WorkflowItem('历史主线', '历史主线回顾', vscode.TreeItemCollapsibleState.None, 'trquant.getMainlines'),
          new WorkflowItem('LLM 分析', 'AI 辅助主线解读', vscode.TreeItemCollapsibleState.None, 'trquant.getMainlines'),
        ]
      ),
      
      // 步骤4：候选池构建
      new WorkflowItem(
        '📦 4. 候选池构建',
        '股票筛选、候选池管理',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openWorkflowPanel',
        [
          new WorkflowItem('候选股票', '查看候选池股票', vscode.TreeItemCollapsibleState.None, 'trquant.openWorkflowPanel'),
          new WorkflowItem('筛选规则', '配置筛选条件', vscode.TreeItemCollapsibleState.None, 'trquant.openWorkflowPanel'),
          new WorkflowItem('关注列表', '个人关注股票', vscode.TreeItemCollapsibleState.None, 'trquant.openWorkflowPanel'),
        ]
      ),

      // 步骤5：因子构建
      new WorkflowItem(
        '📊 5. 因子构建',
        '因子推荐、因子配置',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.recommendFactors',
        [
          new WorkflowItem('因子库', '查看可用因子', vscode.TreeItemCollapsibleState.None, 'trquant.recommendFactors'),
          new WorkflowItem('因子检验', 'IC/IR 分析', vscode.TreeItemCollapsibleState.None, 'trquant.recommendFactors'),
          new WorkflowItem('因子推荐', '基于市场状态推荐', vscode.TreeItemCollapsibleState.None, 'trquant.recommendFactors'),
        ]
      ),
      
      // 步骤6：策略生成
      new WorkflowItem(
        '🛠️ 6. 策略生成',
        '策略代码生成、策略优化',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openStrategyGenerator',
        [
          new WorkflowItem('创建项目', '新建量化策略项目', vscode.TreeItemCollapsibleState.None, 'trquant.createProject'),
          new WorkflowItem('策略编辑器', '编辑策略代码', vscode.TreeItemCollapsibleState.None, 'trquant.openStrategyGenerator'),
          new WorkflowItem('AI 生成', 'LLM 辅助生成策略', vscode.TreeItemCollapsibleState.None, 'trquant.generateStrategy'),
        ]
      ),
      
      // 步骤7：回测验证
      new WorkflowItem(
        '🔄 7. 回测验证',
        '回测执行、结果分析',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openBacktestPanel',
        [
          new WorkflowItem('运行回测', '配置并执行回测', vscode.TreeItemCollapsibleState.None, 'trquant.openBacktestPanel'),
          new WorkflowItem('历史回测', '查看历史回测记录', vscode.TreeItemCollapsibleState.None, 'trquant.openBacktestPanel'),
          new WorkflowItem('结果分析', '深入分析回测结果', vscode.TreeItemCollapsibleState.None, 'trquant.analyzeBacktest'),
        ]
      ),
      
      // 步骤8：策略优化
      new WorkflowItem(
        '⚡ 8. 策略优化',
        '参数优化、多目标优化',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openOptimizerPanel',
        [
          new WorkflowItem('参数搜索', '网格/贝叶斯优化', vscode.TreeItemCollapsibleState.None, 'trquant.openOptimizerPanel'),
          new WorkflowItem('多目标优化', '收益风险平衡', vscode.TreeItemCollapsibleState.None, 'trquant.openOptimizerPanel'),
          new WorkflowItem('对比分析', '多策略对比', vscode.TreeItemCollapsibleState.None, 'trquant.compareBacktests'),
        ]
      ),
      
      // 步骤9：报告生成
      new WorkflowItem(
        '📄 9. 报告生成',
        '报告生成、结果归档',
        vscode.TreeItemCollapsibleState.Collapsed,
        'trquant.openReportPanel',
        [
          new WorkflowItem('生成报告', '生成策略报告', vscode.TreeItemCollapsibleState.None, 'trquant.openReportPanel'),
          new WorkflowItem('结果归档', '保存到知识库', vscode.TreeItemCollapsibleState.None, 'trquant.openReportPanel'),
          new WorkflowItem('导出分享', '导出PDF/HTML', vscode.TreeItemCollapsibleState.None, 'trquant.openReportPanel'),
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

    this.iconPath = this.getIcon();
    this.contextValue = 'workflowItem';
  }

  private getIcon(): vscode.ThemeIcon | undefined {
    const iconMap: Record<string, string> = {
      '🐉 韬睿量化投资流程': 'symbol-event',
      '📡 1. 信息获取': 'database',
      '📈 2. 市场趋势': 'graph-line',
      '🔥 3. 投资主线': 'flame',
      '📦 4. 候选池构建': 'package',
      '📊 5. 因子构建': 'symbol-variable',
      '🛠️ 6. 策略生成': 'tools',
      '🔄 7. 回测验证': 'history',
      '⚡ 8. 策略优化': 'zap',
      '📄 9. 报告生成': 'file-text',
    };

    const iconName = iconMap[this.label];
    if (iconName) {
      return new vscode.ThemeIcon(iconName);
    }

    if (this.collapsibleState === vscode.TreeItemCollapsibleState.None && this.commandId) {
      return new vscode.ThemeIcon('circle-small-filled');
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

  console.log('[TRQuant] 9步工作流提供者已注册');
  return provider;
}
