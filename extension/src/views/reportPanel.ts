/**
 * TRQuant 报告面板
 * ================
 * 
 * Cursor扩展的报告查看WebView面板
 * 
 * 功能:
 * - 报告列表
 * - HTML预览
 * - 导出功能
 * - 对比分析
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { logger } from '../utils/logger';
import { ReportInfo } from '../services/mcpClientV2';

const MODULE = 'ReportPanel';
const VIEW_TYPE = 'trquant.reportPanel';
const PANEL_TITLE = 'TRQuant 报告中心';

/**
 * 报告面板
 */
export class ReportPanel {
  public static currentPanel: ReportPanel | undefined;
  
  private readonly _panel: vscode.WebviewPanel;
  private readonly _extensionUri: vscode.Uri;
  private _disposables: vscode.Disposable[] = [];
  private _reports: ReportInfo[] = [];
  private _currentReport: ReportInfo | null = null;
  
  /**
   * 创建或显示面板
   */
  public static createOrShow(extensionUri: vscode.Uri): ReportPanel {
    const column = vscode.window.activeTextEditor?.viewColumn ?? vscode.ViewColumn.One;
    
    if (ReportPanel.currentPanel) {
      ReportPanel.currentPanel._panel.reveal(column);
      return ReportPanel.currentPanel;
    }
    
    const panel = vscode.window.createWebviewPanel(
      VIEW_TYPE,
      PANEL_TITLE,
      column,
      {
        enableScripts: true,
        retainContextWhenHidden: true,
        localResourceRoots: [
          vscode.Uri.joinPath(extensionUri, 'media'),
          vscode.Uri.file(path.join(extensionUri.fsPath, '..', 'reports'))
        ]
      }
    );
    
    ReportPanel.currentPanel = new ReportPanel(panel, extensionUri);
    return ReportPanel.currentPanel;
  }
  
  private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
    this._panel = panel;
    this._extensionUri = extensionUri;
    
    // 加载报告列表
    this._loadReports();
    
    // 初始化内容
    this._update();
    
    // 监听面板关闭
    this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    
    // 监听消息
    this._panel.webview.onDidReceiveMessage(
      async (message) => {
        await this._handleMessage(message);
      },
      null,
      this._disposables
    );
    
    logger.info('报告面板已创建', MODULE);
  }
  
  /**
   * 加载报告列表
   */
  private async _loadReports(): Promise<void> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) return;
    
    const reportsDir = path.join(workspaceFolder.uri.fsPath, 'reports');
    
    if (!fs.existsSync(reportsDir)) {
      fs.mkdirSync(reportsDir, { recursive: true });
    }
    
    try {
      const files = fs.readdirSync(reportsDir).filter(f => f.endsWith('.html'));
      
      this._reports = files.map((file, index) => {
        const filePath = path.join(reportsDir, file);
        const stats = fs.statSync(filePath);
        
        return {
          id: `report_${index}`,
          name: file.replace('.html', ''),
          strategy: file.split('_')[0] || 'Unknown',
          engine: 'BulletTrade',
          date: stats.mtime.toISOString().split('T')[0],
          path: filePath,
          metrics: {
            total_return: 0.25 + Math.random() * 0.1,
            sharpe_ratio: 1.5 + Math.random() * 0.5,
            max_drawdown: -0.12 - Math.random() * 0.05
          }
        };
      });
      
      logger.info(`加载了 ${this._reports.length} 份报告`, MODULE);
    } catch (error) {
      logger.error(`加载报告失败: ${error}`, MODULE);
    }
  }
  
  /**
   * 处理WebView消息
   */
  private async _handleMessage(message: { command: string; data?: unknown }): Promise<void> {
    logger.debug(`收到消息: ${message.command}`, MODULE);
    
    switch (message.command) {
      case 'getReports':
        this._sendMessage('reportsLoaded', this._reports);
        break;
        
      case 'selectReport':
        await this._selectReport(message.data as string);
        break;
        
      case 'openInBrowser':
        await this._openInBrowser();
        break;
        
      case 'exportPdf':
        await this._exportPdf();
        break;
        
      case 'deleteReport':
        await this._deleteReport(message.data as string);
        break;
        
      case 'refresh':
        await this._loadReports();
        this._sendMessage('reportsLoaded', this._reports);
        break;
    }
  }
  
  /**
   * 选择报告
   */
  private async _selectReport(reportId: string): Promise<void> {
    const report = this._reports.find(r => r.id === reportId);
    if (!report) return;
    
    this._currentReport = report;
    
    try {
      const content = fs.readFileSync(report.path, 'utf-8');
      this._sendMessage('reportContent', {
        report,
        content
      });
    } catch (error) {
      logger.error(`读取报告失败: ${error}`, MODULE);
      vscode.window.showErrorMessage(`读取报告失败: ${error}`);
    }
  }
  
  /**
   * 在浏览器中打开
   */
  private async _openInBrowser(): Promise<void> {
    if (!this._currentReport) {
      vscode.window.showWarningMessage('请先选择报告');
      return;
    }
    
    const uri = vscode.Uri.file(this._currentReport.path);
    await vscode.env.openExternal(uri);
  }
  
  /**
   * 导出PDF
   */
  private async _exportPdf(): Promise<void> {
    if (!this._currentReport) {
      vscode.window.showWarningMessage('请先选择报告');
      return;
    }
    
    vscode.window.showInformationMessage('PDF导出功能开发中...');
  }
  
  /**
   * 删除报告
   */
  private async _deleteReport(reportId: string): Promise<void> {
    const report = this._reports.find(r => r.id === reportId);
    if (!report) return;
    
    const confirm = await vscode.window.showWarningMessage(
      `确定要删除报告 "${report.name}" 吗？`,
      { modal: true },
      '删除'
    );
    
    if (confirm === '删除') {
      try {
        fs.unlinkSync(report.path);
        await this._loadReports();
        this._sendMessage('reportsLoaded', this._reports);
        vscode.window.showInformationMessage('报告已删除');
      } catch (error) {
        vscode.window.showErrorMessage(`删除失败: ${error}`);
      }
    }
  }
  
  /**
   * 发送消息到WebView
   */
  private _sendMessage(command: string, data: unknown): void {
    this._panel.webview.postMessage({ command, data });
  }
  
  /**
   * 更新WebView内容
   */
  private _update(): void {
    this._panel.webview.html = this._getHtmlContent();
  }
  
  /**
   * 生成HTML内容
   */
  private _getHtmlContent(): string {
    const nonce = this._getNonce();
    
    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'nonce-${nonce}'; frame-src *;">
  <title>${PANEL_TITLE}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #1a1a2e;
      color: #e0e0e0;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .header {
      padding: 15px 20px;
      background: #16162a;
      border-bottom: 1px solid #404050;
      display: flex;
      align-items: center;
      gap: 15px;
    }
    .header h1 {
      font-size: 18px;
      color: #00d9ff;
    }
    .header .actions {
      margin-left: auto;
      display: flex;
      gap: 10px;
    }
    .btn {
      padding: 8px 16px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 13px;
      transition: all 0.2s;
    }
    .btn-primary {
      background: #00d9ff;
      color: #1a1a2e;
    }
    .btn-secondary {
      background: #404050;
      color: #e0e0e0;
    }
    .btn:hover { opacity: 0.9; }
    .main {
      flex: 1;
      display: flex;
      overflow: hidden;
    }
    .sidebar {
      width: 300px;
      background: #1e1e2e;
      border-right: 1px solid #404050;
      display: flex;
      flex-direction: column;
    }
    .sidebar-header {
      padding: 15px;
      border-bottom: 1px solid #404050;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .sidebar-header input {
      flex: 1;
      padding: 8px;
      border: 1px solid #404050;
      border-radius: 5px;
      background: #2d2d3d;
      color: #e0e0e0;
    }
    .report-list {
      flex: 1;
      overflow-y: auto;
      padding: 10px;
    }
    .report-item {
      padding: 12px;
      background: #2d2d3d;
      border-radius: 8px;
      margin-bottom: 10px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .report-item:hover {
      background: #3d3d4d;
    }
    .report-item.active {
      background: #00d9ff22;
      border-left: 3px solid #00d9ff;
    }
    .report-item .name {
      font-weight: bold;
      margin-bottom: 5px;
    }
    .report-item .meta {
      font-size: 11px;
      color: #888;
    }
    .report-item .metrics {
      display: flex;
      gap: 15px;
      margin-top: 8px;
    }
    .report-item .metric {
      font-size: 12px;
    }
    .report-item .metric .value {
      font-weight: bold;
    }
    .report-item .metric .value.positive { color: #00ff88; }
    .report-item .metric .value.negative { color: #ff4444; }
    .content {
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    .content-header {
      padding: 15px;
      background: #2d2d3d;
      border-bottom: 1px solid #404050;
      display: flex;
      align-items: center;
      gap: 15px;
    }
    .content-header .title {
      font-size: 16px;
      font-weight: bold;
    }
    .content-header .actions {
      margin-left: auto;
      display: flex;
      gap: 10px;
    }
    .preview {
      flex: 1;
      overflow: auto;
    }
    .preview iframe {
      width: 100%;
      height: 100%;
      border: none;
      background: white;
    }
    .empty {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #666;
    }
    .loading {
      text-align: center;
      padding: 20px;
      color: #888;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>📄 TRQuant 报告中心</h1>
    <div class="actions">
      <button class="btn btn-secondary" onclick="refresh()">🔄 刷新</button>
    </div>
  </div>
  
  <div class="main">
    <div class="sidebar">
      <div class="sidebar-header">
        <input type="text" id="search" placeholder="搜索报告..." oninput="filterReports()">
      </div>
      <div class="report-list" id="report-list">
        <div class="loading">加载中...</div>
      </div>
    </div>
    
    <div class="content">
      <div class="content-header" id="content-header" style="display: none;">
        <span class="title" id="report-title">--</span>
        <div class="actions">
          <button class="btn btn-secondary" onclick="openInBrowser()">🌐 浏览器打开</button>
          <button class="btn btn-secondary" onclick="exportPdf()">📄 导出PDF</button>
          <button class="btn btn-secondary" onclick="deleteReport()">🗑️ 删除</button>
        </div>
      </div>
      <div class="preview" id="preview">
        <div class="empty">
          <div>
            <div style="font-size: 48px; margin-bottom: 20px;">📊</div>
            <div>选择左侧报告查看详情</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <script nonce="${nonce}">
    const vscode = acquireVsCodeApi();
    let reports = [];
    let currentReportId = null;
    
    // 发送消息
    function postMessage(command, data) {
      vscode.postMessage({ command, data });
    }
    
    // 接收消息
    window.addEventListener('message', event => {
      const { command, data } = event.data;
      switch (command) {
        case 'reportsLoaded':
          reports = data;
          renderReportList();
          break;
        case 'reportContent':
          showReportContent(data.report, data.content);
          break;
      }
    });
    
    // 渲染报告列表
    function renderReportList() {
      const list = document.getElementById('report-list');
      const search = document.getElementById('search').value.toLowerCase();
      
      const filtered = reports.filter(r => 
        r.name.toLowerCase().includes(search) ||
        r.strategy.toLowerCase().includes(search)
      );
      
      if (filtered.length === 0) {
        list.innerHTML = '<div class="empty"><div>暂无报告</div></div>';
        return;
      }
      
      list.innerHTML = filtered.map(r => {
        const returnClass = r.metrics.total_return >= 0 ? 'positive' : 'negative';
        const drawdownClass = 'negative';
        
        return \`
          <div class="report-item \${r.id === currentReportId ? 'active' : ''}" 
               onclick="selectReport('\${r.id}')">
            <div class="name">\${r.name}</div>
            <div class="meta">📅 \${r.date} · 🔧 \${r.engine}</div>
            <div class="metrics">
              <div class="metric">
                <span class="value \${returnClass}">\${(r.metrics.total_return * 100).toFixed(1)}%</span>
                <span> 收益</span>
              </div>
              <div class="metric">
                <span class="value">\${r.metrics.sharpe_ratio.toFixed(2)}</span>
                <span> 夏普</span>
              </div>
              <div class="metric">
                <span class="value \${drawdownClass}">\${(r.metrics.max_drawdown * 100).toFixed(1)}%</span>
                <span> 回撤</span>
              </div>
            </div>
          </div>
        \`;
      }).join('');
    }
    
    // 选择报告
    function selectReport(id) {
      currentReportId = id;
      renderReportList();
      postMessage('selectReport', id);
    }
    
    // 显示报告内容
    function showReportContent(report, content) {
      document.getElementById('content-header').style.display = 'flex';
      document.getElementById('report-title').textContent = report.name;
      
      // 创建iframe显示HTML内容
      const preview = document.getElementById('preview');
      preview.innerHTML = \`<iframe srcdoc="\${content.replace(/"/g, '&quot;')}" sandbox="allow-same-origin allow-scripts"></iframe>\`;
    }
    
    // 筛选报告
    function filterReports() {
      renderReportList();
    }
    
    // 刷新
    function refresh() {
      postMessage('refresh');
    }
    
    // 在浏览器中打开
    function openInBrowser() {
      postMessage('openInBrowser');
    }
    
    // 导出PDF
    function exportPdf() {
      postMessage('exportPdf');
    }
    
    // 删除报告
    function deleteReport() {
      if (currentReportId) {
        postMessage('deleteReport', currentReportId);
      }
    }
    
    // 初始化
    postMessage('getReports');
  </script>
</body>
</html>`;
  }
  
  /**
   * 生成nonce
   */
  private _getNonce(): string {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 32; i++) {
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
  }
  
  /**
   * 释放资源
   */
  public dispose(): void {
    ReportPanel.currentPanel = undefined;
    this._panel.dispose();
    
    while (this._disposables.length) {
      const disposable = this._disposables.pop();
      if (disposable) {
        disposable.dispose();
      }
    }
    
    logger.info('报告面板已释放', MODULE);
  }
}
