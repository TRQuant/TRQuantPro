/**
 * TRQuant 统一仪表板
 * ====================
 * 
 * 整合所有核心功能模块：
 * 1. 9步投资工作流
 * 2. 十倍股早期识别
 * 3. 趋势策略追踪
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as cp from 'child_process';
import { spawn } from 'child_process';

interface MCPResult {
    ok: boolean;
    data: any;
    error?: string;
    details?: string;
    traceback?: string;
}

export class UnifiedDashboard {
    public static currentPanel: UnifiedDashboard | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private readonly _extensionUri: vscode.Uri;
    private readonly _extensionPath: string;
    private _disposables: vscode.Disposable[] = [];
    private _currentTab: string = 'workflow';
    private _workflowId: string | null = null;  // 工作流会话ID

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri, extensionPath: string) {
        this._panel = panel;
        this._extensionUri = extensionUri;
        this._extensionPath = extensionPath;

        this._panel.webview.html = this._getHtmlContent();

        this._panel.webview.onDidReceiveMessage(
            async (message) => {
                await this._handleMessage(message);
            },
            null,
            this._disposables
        );

        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
        console.log('[UnifiedDashboard] 面板已创建');
    }

    public static createOrShow(extensionUri: vscode.Uri, extensionPath?: string) {
        try {
            console.log('[UnifiedDashboard] createOrShow 被调用', {
                extensionUri: extensionUri.toString(),
                extensionPath: extensionPath || '未提供'
            });

            const column = vscode.window.activeTextEditor?.viewColumn;

            if (UnifiedDashboard.currentPanel) {
                console.log('[UnifiedDashboard] 使用现有面板');
                UnifiedDashboard.currentPanel._panel.reveal(column);
                return UnifiedDashboard.currentPanel;
            }

            // 如果没有提供 extensionPath，尝试从 extensionUri 推断
            let extPath = extensionPath;
            if (!extPath) {
                const extension = vscode.extensions.getExtension('trquant.trquant-cursor-extension');
                extPath = extension?.extensionPath || extensionUri.fsPath;
                console.log('[UnifiedDashboard] 推断 extensionPath:', extPath);
            }

            console.log('[UnifiedDashboard] 创建新面板');
            const panel = vscode.window.createWebviewPanel(
                'trquantUnifiedDashboard',
                '🐉 韬睿量化 - 统一仪表板',
                column || vscode.ViewColumn.One,
                {
                    enableScripts: true,
                    retainContextWhenHidden: true,
                    localResourceRoots: [extensionUri]
                }
            );

            UnifiedDashboard.currentPanel = new UnifiedDashboard(panel, extensionUri, extPath);
            console.log('[UnifiedDashboard] 面板创建成功');
            return UnifiedDashboard.currentPanel;
        } catch (error) {
            console.error('[UnifiedDashboard] 创建面板失败:', error);
            vscode.window.showErrorMessage(
                `创建统一仪表板失败: ${error instanceof Error ? error.message : String(error)}`
            );
            throw error;
        }
    }

    private _getProjectRoot(): string {
        const mainPath = '/home/taotao/dev/QuantTest/TRQuant';
        if (fs.existsSync(mainPath)) {
            return mainPath;
        }
        if (process.env.TRQUANT_ROOT && fs.existsSync(process.env.TRQUANT_ROOT)) {
            return process.env.TRQUANT_ROOT;
        }
        return path.dirname(path.dirname(this._extensionPath));
    }

    private _getPythonPath(): string {
        const projectRoot = this._getProjectRoot();
        const venvPython = path.join(projectRoot, 'venv', 'bin', 'python3');
        if (fs.existsSync(venvPython)) {
            return venvPython;
        }
        return 'python3';
    }

    private async _callMCP(toolName: string, args: Record<string, any> = {}): Promise<MCPResult> {
        const pythonPath = this._getPythonPath();
        const projectRoot = this._getProjectRoot();
        const bridgePath = path.join(projectRoot, 'extension', 'python', 'bridge.py');
        
        // 构建PYTHONPATH：主文件夹 + mcp_servers + extension/python
        const pythonPaths = [
            projectRoot,
            path.join(projectRoot, 'mcp_servers'),
            path.join(projectRoot, 'extension', 'python')
        ].filter(p => fs.existsSync(p)); // 只添加存在的路径
        
        const pythonPathStr = pythonPaths.join(path.delimiter);

        return new Promise((resolve) => {
            const proc = spawn(pythonPath, [bridgePath], {
                cwd: projectRoot,
                env: {
                    ...process.env,
                    PYTHONPATH: pythonPathStr,
                    TRQUANT_ROOT: projectRoot,
                    PYTHONIOENCODING: 'utf-8'
                },
                stdio: ['pipe', 'pipe', 'pipe']
            });

            let stdout = '';
            let stderr = '';

            proc.stdout.on('data', (data) => { stdout += data.toString(); });
            proc.stderr.on('data', (data) => { stderr += data.toString(); });

            const timeout = setTimeout(() => {
                proc.kill();
                resolve({ 
                    ok: false, 
                    data: null, 
                    error: '调用超时(30秒)',
                    details: `stdout: ${stdout.substring(0, 500)}\nstderr: ${stderr.substring(0, 500)}`
                });
            }, 30000);

            proc.on('close', (code) => {
                clearTimeout(timeout);
                
                // #region agent log
                fetch('http://127.0.0.1:7242/ingest/a89fb3b8-5b13-4eda-93cb-fbdec01469c1',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'unifiedDashboard.ts:162',message:'proc close event',data:{code,stdout_length:stdout.length,stderr_length:stderr.length,stdout_preview:stdout.substring(0,200),stderr_preview:stderr.substring(0,200)},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'E'})}).catch(()=>{});
                // #endregion
                
                if (code === 0) {
                    try {
                        const lines = stdout.trim().split('\n');
                        const lastLine = lines[lines.length - 1];
                        const result = JSON.parse(lastLine);
                        
                        // #region agent log
                        fetch('http://127.0.0.1:7242/ingest/a89fb3b8-5b13-4eda-93cb-fbdec01469c1',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'unifiedDashboard.ts:169',message:'JSON parse success',data:{ok:result.ok,has_data:!!result.data,has_error:!!result.error,result_keys:Object.keys(result)},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{});
                        // #endregion
                        
                        resolve({ 
                            ok: result.ok !== false, 
                            data: result.data || result, 
                            error: result.error,
                            details: result.traceback || result.details || ''
                        });
                    } catch (e) {
                        // #region agent log
                        fetch('http://127.0.0.1:7242/ingest/a89fb3b8-5b13-4eda-93cb-fbdec01469c1',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'unifiedDashboard.ts:176',message:'JSON parse failed',data:{error:String(e),stdout_preview:stdout.substring(0,500)},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'E'})}).catch(()=>{});
                        // #endregion
                        
                        resolve({ 
                            ok: false, 
                            data: null, 
                            error: `JSON解析失败: ${e instanceof Error ? e.message : String(e)}`,
                            details: `stdout: ${stdout.substring(0, 1000)}\nstderr: ${stderr.substring(0, 1000)}`
                        });
                    }
                } else {
                    // 进程非正常退出，尝试从stdout解析错误，否则使用stderr
                    let errorMsg = `进程退出码: ${code}`;
                    let errorDetails = stderr || stdout;
                    
                    // 尝试从stdout解析JSON错误
                    try {
                        const lines = stdout.trim().split('\n');
                        const lastLine = lines[lines.length - 1];
                        const result = JSON.parse(lastLine);
                        if (result.error) {
                            errorMsg = result.error;
                            errorDetails = result.traceback || result.details || stderr;
                        }
                    } catch (e) {
                        // 解析失败，使用原始错误信息
                    }
                    
                    resolve({ 
                        ok: false, 
                        data: null, 
                        error: errorMsg,
                        details: errorDetails.substring(0, 2000)
                    });
                }
            });

            const request = {
                action: 'call_mcp_tool',
                params: { tool_name: toolName, arguments: args, trace_id: `dashboard_${Date.now()}` }
            };

            proc.stdin.write(JSON.stringify(request));
            proc.stdin.end();
        });
    }

    private async _handleMessage(message: any): Promise<void> {
        console.log(`[UnifiedDashboard] 收到消息: ${message.command}`);

        try {
            switch (message.command) {
                case 'switchTab':
                    this._currentTab = message.tab;
                    break;
                case 'workflow.runStep':
                    await this._handleWorkflowStep(message.step, message.params);
                    break;
                case 'workflow.runAll':
                    await this._handleWorkflowRunAll();
                    break;
                case 'workflow.reset':
                    await this._handleWorkflowReset();
                    break;
                case 'workflow.getResult':
                    await this._handleWorkflowGetResult(message.step);
                    break;
                case 'workflow.getStatus':
                    await this._handleWorkflowStatus();
                    break;
                case 'tenbagger.getRanking':
                    await this._handleTenbaggerRanking(message.limit, message.minScore);
                    break;
                case 'tenbagger.getStats':
                    await this._handleTenbaggerStats();
                    break;
                case 'tenbagger.filter':
                    await this._handleTenbaggerFilter(message.minLevel);
                    break;
                case 'tenbagger.getReport':
                    await this._handleTenbaggerReport(message.symbol);
                    break;
                case 'tenbagger.getStages':
                    await this._handleTenbaggerStages(message.stage);
                    break;
                case 'tenbagger.refresh':
                    await this._handleTenbaggerRefresh();
                    break;
                case 'tenbagger.getScorecards':
                    await this._handleTenbaggerScorecards(message.minGrade);
                    break;
                case 'tenbagger.jqdataScan':
                    await this._handleJQDataScan(message.filters);
                    break;
                case 'tenbagger.jqdataStock':
                    await this._handleJQDataStock(message.symbol);
                    break;
                // AKShare实时数据
                case 'akshare.realtime':
                    await this._handleAKShareRealtime(message.symbols);
                    break;
                case 'akshare.hot':
                    console.log(`[UnifiedDashboard] 处理 akshare.hot: category=${message.category}, limit=${message.limit}`);
                    await this._handleAKShareHot(message.category, message.limit);
                    break;
                case 'akshare.spot':
                    console.log(`[UnifiedDashboard] 处理 akshare.spot: sortBy=${message.sortBy}, limit=${message.limit}`);
                    await this._handleAKShareSpot(message.sortBy, message.limit);
                    break;
                case 'strategy.scan':
                    await this._handleStrategyScan(message.params);
                    break;
                case 'strategy.getList':
                    await this._handleStrategyList();
                    break;
                // MCP状态检查
                case 'mcp.checkStatus':
                    await this._handleMcpStatusCheck();
                    break;
                // 错误搜索
                case 'error.search':
                    await this._handleErrorSearch(message.query);
                    break;
            }
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            const errorStack = error instanceof Error ? error.stack : '';
            this._panel.webview.postMessage({ 
                command: 'error', 
                error: errorMessage,
                details: errorStack 
            });
        }
    }
    
    /**
     * 检查MCP服务器状态
     */
    private async _handleMcpStatusCheck() {
        const status: Record<string, { ok: boolean; message: string }> = {
            workflow: { ok: false, message: '未检查' },
            datasource: { ok: false, message: '未检查' },
            tenbagger: { ok: false, message: '未检查' }
        };
        
        try {
            // 检查工作流服务器
            const workflowResult = await this._callMCP('workflow9.get_steps', {});
            status.workflow = {
                ok: workflowResult.ok && !workflowResult.error,
                message: workflowResult.ok ? '连接正常' : (workflowResult.error || '连接失败')
            };
        } catch (e) {
            status.workflow = { ok: false, message: String(e) };
        }
        
        try {
            // 检查数据源服务器
            const datasourceResult = await this._callMCP('data_source.health_check', {});
            status.datasource = {
                ok: datasourceResult.ok && !datasourceResult.error,
                message: datasourceResult.ok ? '连接正常' : (datasourceResult.error || '连接失败')
            };
        } catch (e) {
            status.datasource = { ok: false, message: String(e) };
        }
        
        try {
            // 检查十倍股服务器
            const tenbaggerResult = await this._callMCP('tenbagger.db_stats', {});
            status.tenbagger = {
                ok: tenbaggerResult.ok && !tenbaggerResult.error,
                message: tenbaggerResult.ok ? '连接正常' : (tenbaggerResult.error || '连接失败')
            };
        } catch (e) {
            status.tenbagger = { ok: false, message: String(e) };
        }
        
        this._panel.webview.postMessage({
            command: 'mcp.statusResult',
            status
        });
    }
    
    /**
     * 搜索错误解决方案
     */
    private async _handleErrorSearch(query: string) {
        try {
            // 首先在知识库中搜索
            const kbResult = await this._callMCP('xuanyuan.knowledge_search', { query, limit: 5 });
            
            const solutions: string[] = [];
            if (kbResult.ok && kbResult.data?.results) {
                kbResult.data.results.forEach((r: any) => {
                    if (r.content) {
                        solutions.push(r.title + ': ' + r.content.substring(0, 200));
                    }
                });
            }
            
            // 如果知识库没有结果，尝试经验库
            if (solutions.length === 0) {
                const expResult = await this._callMCP('xuanyuan.experience_search', { query });
                if (expResult.ok && expResult.data?.results) {
                    expResult.data.results.forEach((r: any) => {
                        if (r.content) {
                            solutions.push(r.content.substring(0, 200));
                        }
                    });
                }
            }
            
            this._panel.webview.postMessage({
                command: 'error.searchResult',
                success: solutions.length > 0,
                solutions
            });
        } catch (e) {
            this._panel.webview.postMessage({
                command: 'error.searchResult',
                success: false,
                solutions: [],
                error: String(e)
            });
        }
    }

    private async _handleWorkflowStep(step: number, params: any = {}) {
        this._panel.webview.postMessage({ command: 'workflow.loading', loading: true });
        try {
            // 确保有工作流会话
            if (!this._workflowId) {
                const createResult = await this._callMCP('workflow9.create', { name: '统一仪表板工作流' });
                if (createResult.ok && createResult.data?.workflow_id) {
                    this._workflowId = createResult.data.workflow_id;
                } else {
                    throw new Error('创建工作流会话失败: ' + (createResult.error || '未知错误'));
                }
            }
            
            // 步骤映射：数字 -> 步骤ID
            const stepIdMap: Record<number, string> = {
                1: 'data_source',
                2: 'market_trend', 
                3: 'mainline',
                4: 'candidate_pool',
                5: 'factor',
                6: 'strategy',
                7: 'backtest',
                8: 'optimization',
                9: 'report'
            };
            
            const stepId = stepIdMap[step] || `step_${step}`;
            
            // #region agent log
            fetch('http://127.0.0.1:7242/ingest/a89fb3b8-5b13-4eda-93cb-fbdec01469c1',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'unifiedDashboard.ts:427',message:'before workflow9.run_step call',data:{step,stepId,workflow_id:this._workflowId,params},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
            // #endregion
            
            const result = await this._callMCP('workflow9.run_step', { 
                workflow_id: this._workflowId, 
                step_id: stepId,
                args: params 
            });
            
            // #region agent log
            fetch('http://127.0.0.1:7242/ingest/a89fb3b8-5b13-4eda-93cb-fbdec01469c1',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'unifiedDashboard.ts:432',message:'after workflow9.run_step call',data:{ok:result.ok,has_data:!!result.data,has_error:!!result.error,error:result.error,data_type:typeof result.data},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{});
            // #endregion
            
            // 提取详细错误信息
            let errorMsg = result.error;
            let errorDetails = result.details || result.traceback || '';
            
            // 如果 result.data 中有错误信息，也提取出来
            if (result.data) {
                const data = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
                if (data.error && !errorMsg) errorMsg = data.error;
                if (data.error_details) {
                    errorDetails = Array.isArray(data.error_details) 
                        ? data.error_details.join('\n') 
                        : String(data.error_details);
                }
                if (data.error_summary) {
                    errorDetails = (data.error_summary + '\n\n' + errorDetails).trim();
                }
                if (data.hint) {
                    errorDetails += '\n\n修复建议: ' + data.hint;
                }
                if (data.traceback) {
                    errorDetails += '\n\n堆栈跟踪:\n' + data.traceback;
                }
            }
            
            this._panel.webview.postMessage({
                command: 'workflow.stepResult', 
                step, 
                result: result.data, 
                success: result.ok,
                error: errorMsg,
                details: errorDetails
            });
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            const errorStack = error instanceof Error ? error.stack : '';
            this._panel.webview.postMessage({
                command: 'workflow.stepResult', 
                step, 
                result: null, 
                success: false, 
                error: errorMessage,
                details: errorStack
            });
        } finally {
            this._panel.webview.postMessage({ command: 'workflow.loading', loading: false });
        }
    }

    private async _handleWorkflowRunAll() {
        this._panel.webview.postMessage({ command: 'workflow.loading', loading: true });
        try {
            // 确保有工作流会话
            if (!this._workflowId) {
                const createResult = await this._callMCP('workflow9.create', { name: '统一仪表板工作流' });
                if (createResult.ok && createResult.data?.workflow_id) {
                    this._workflowId = createResult.data.workflow_id;
                } else {
                    throw new Error('创建工作流会话失败: ' + (createResult.error || '未知错误'));
                }
            }
            
            // 调用MCP工具一键执行全部
            const result = await this._callMCP('workflow9.run_all', {
                workflow_id: this._workflowId
            });
            
            if (result.ok && result.data) {
                this._panel.webview.postMessage({
                    command: 'workflow.allCompleted',
                    success: true,
                    data: result.data
                });
            } else {
                const errorMsg = result.error || '一键执行失败';
                const errorDetails = result.details || '';
                throw new Error(errorMsg + (errorDetails ? '\n' + errorDetails.substring(0, 500) : ''));
            }
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            const errorStack = error instanceof Error ? error.stack : '';
            this._panel.webview.postMessage({
                command: 'workflow.allCompleted',
                success: false,
                error: errorMessage,
                details: errorStack
            });
            
            // 显示全局错误面板（通过postMessage，因为这是后端代码）
            this._panel.webview.postMessage({
                command: 'error',
                error: errorMessage,
                details: errorStack
            });
        } finally {
            this._panel.webview.postMessage({ command: 'workflow.loading', loading: false });
        }
    }

    private async _handleWorkflowReset() {
        try {
            this._workflowId = null;
            this._panel.webview.postMessage({
                command: 'workflow.reset',
                success: true
            });
        } catch (error) {
            this._panel.webview.postMessage({
                command: 'workflow.reset',
                success: false,
                error: String(error)
            });
        }
    }

    private async _handleWorkflowGetResult(step: number) {
        try {
            if (!this._workflowId) {
                throw new Error('工作流会话不存在');
            }
            
            // 步骤映射：数字 -> 步骤ID
            const stepIdMap: Record<number, string> = {
                1: 'data_source',
                2: 'market_trend', 
                3: 'mainline',
                4: 'candidate_pool',
                5: 'factor',
                6: 'strategy',
                7: 'backtest',
                8: 'optimization',
                9: 'report'
            };
            
            const stepId = stepIdMap[step] || `step_${step}`;
            
            // 获取工作流状态，从中提取步骤结果
            const statusResult = await this._callMCP('workflow9.status', { workflow_id: this._workflowId });
            
            if (statusResult.ok && statusResult.data) {
                // 从状态中查找对应步骤的结果
                const steps = statusResult.data.steps || [];
                const stepData = steps.find((s: any) => s.id === stepId || s.step_id === stepId);
                
                this._panel.webview.postMessage({
                    command: 'workflow.result',
                    step: step,
                    result: stepData?.result || stepData?.output || null,
                    success: true
                });
            } else {
                throw new Error('获取工作流状态失败');
            }
        } catch (error) {
            this._panel.webview.postMessage({
                command: 'workflow.result',
                step: step,
                result: null,
                success: false,
                error: String(error)
            });
        }
    }

    private async _handleWorkflowStatus() {
        try {
            // 如果没有工作流会话，先获取步骤定义
            if (!this._workflowId) {
                const stepsResult = await this._callMCP('workflow9.get_steps', {});
                this._panel.webview.postMessage({ 
                    command: 'workflow.status', 
                    status: stepsResult.data || { steps: [], current_step: 0 }
                });
                return;
            }
            
            const result = await this._callMCP('workflow9.status', { workflow_id: this._workflowId });
            this._panel.webview.postMessage({ command: 'workflow.status', status: result.data });
        } catch (error) {
            this._panel.webview.postMessage({ command: 'workflow.status', status: { error: String(error) } });
        }
    }

    private async _handleTenbaggerRanking(limit: number = 50, minScore: number = 50) {
        this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: true });
        try {
            // 从数据库获取排名
            const result = await this._callMCP('tenbagger.db_rankings', { limit, min_score: minScore });
            this._panel.webview.postMessage({
                command: 'tenbagger.rankingResult', 
                rankings: result.data?.rankings || [], 
                source: result.data?.source || 'unknown',
                success: result.ok
            });
        } finally {
            this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: false });
        }
    }

    private async _handleTenbaggerStats() {
        try {
            // 从数据库获取统计
            const result = await this._callMCP('tenbagger.db_stats', {});
            this._panel.webview.postMessage({
                command: 'tenbagger.statsResult', 
                stats: result.data || {}, 
                success: result.ok
            });
        } catch (error) {
            this._panel.webview.postMessage({
                command: 'tenbagger.statsResult', stats: {}, success: false
            });
        }
    }

    private async _handleTenbaggerFilter(minLevel: string) {
        this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: true });
        try {
            const result = await this._callMCP('tenbagger.filter', { min_level: minLevel });
            this._panel.webview.postMessage({
                command: 'tenbagger.filterResult', stocks: result.data?.stocks || [], success: result.ok
            });
        } finally {
            this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: false });
        }
    }

    private async _handleTenbaggerReport(symbol: string) {
        this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: true });
        try {
            const result = await this._callMCP('tenbagger.report', { symbol });
            this._panel.webview.postMessage({
                command: 'tenbagger.reportResult', symbol, report: result.data?.report || {}, success: result.ok
            });
        } finally {
            this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: false });
        }
    }

    private async _handleTenbaggerStages(stage?: string) {
        this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: true });
        try {
            const result = await this._callMCP('tenbagger.db_stages', { stage });
            this._panel.webview.postMessage({
                command: 'tenbagger.stagesResult', 
                stages: result.data?.stages || [],
                counts: result.data?.counts || {},
                success: result.ok
            });
        } finally {
            this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: false });
        }
    }

    private async _handleTenbaggerRefresh() {
        this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: true });
        try {
            const result = await this._callMCP('tenbagger.refresh', {});
            this._panel.webview.postMessage({
                command: 'tenbagger.refreshResult', 
                result: result.data || {},
                success: result.ok
            });
            // 刷新后重新获取数据
            await this._handleTenbaggerStats();
            await this._handleTenbaggerRanking(50);
        } finally {
            this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: false });
        }
    }

    private async _handleTenbaggerScorecards(minGrade: string = 'C') {
        this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: true });
        try {
            const result = await this._callMCP('tenbagger.db_scorecards', { min_grade: minGrade });
            this._panel.webview.postMessage({
                command: 'tenbagger.scorecardsResult', 
                scorecards: result.data?.scorecards || [],
                success: result.ok
            });
        } finally {
            this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: false });
        }
    }

    private async _handleJQDataScan(filters: any = {}) {
        this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: true });
        try {
            const result = await this._callMCP('tenbagger.jqdata_scan', filters);
            this._panel.webview.postMessage({
                command: 'tenbagger.jqdataScanResult', 
                stocks: result.data?.stocks || [],
                filters: result.data?.filters || {},
                date: result.data?.date || '',
                success: result.ok,
                error: result.error
            });
        } finally {
            this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: false });
        }
    }

    private async _handleJQDataStock(symbol: string) {
        this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: true });
        try {
            const result = await this._callMCP('tenbagger.jqdata_stock', { symbol });
            this._panel.webview.postMessage({
                command: 'tenbagger.jqdataStockResult', 
                data: result.data || {},
                success: result.ok,
                error: result.error
            });
        } finally {
            this._panel.webview.postMessage({ command: 'tenbagger.loading', loading: false });
        }
    }

    private async _handleAKShareRealtime(symbols: string[]) {
        this._panel.webview.postMessage({ command: 'akshare.loading', loading: true });
        try {
            const result = await this._callBridge('akshare.realtime', { symbols });
            this._panel.webview.postMessage({
                command: 'akshare.realtimeResult', 
                stocks: result.data?.stocks || [],
                success: result.ok,
                error: result.error
            });
        } finally {
            this._panel.webview.postMessage({ command: 'akshare.loading', loading: false });
        }
    }

    private async _handleAKShareHot(category: string = 'stock', limit: number = 20) {
        console.log(`[UnifiedDashboard] _handleAKShareHot called: category=${category}, limit=${limit}`);
        this._panel.webview.postMessage({ command: 'akshare.loading', loading: true });
        try {
            console.log(`[UnifiedDashboard] Calling bridge: akshare.hot`);
            const result = await this._callBridge('akshare.hot', { category, limit });
            console.log(`[UnifiedDashboard] Bridge result: ok=${result.ok}, items=${result.data?.items?.length || 0}`);
            this._panel.webview.postMessage({
                command: 'akshare.hotResult', 
                items: result.data?.items || [],
                category: result.data?.category || category,
                success: result.ok,
                error: result.error
            });
        } catch (e) {
            console.error(`[UnifiedDashboard] Error in _handleAKShareHot:`, e);
            this._panel.webview.postMessage({
                command: 'akshare.hotResult',
                items: [],
                category: category,
                success: false,
                error: e instanceof Error ? e.message : String(e)
            });
        } finally {
            this._panel.webview.postMessage({ command: 'akshare.loading', loading: false });
        }
    }

    private async _handleAKShareSpot(sortBy: string = 'amount', limit: number = 30) {
        this._panel.webview.postMessage({ command: 'akshare.loading', loading: true });
        try {
            const result = await this._callBridge('akshare.spot', { sort_by: sortBy, limit });
            this._panel.webview.postMessage({
                command: 'akshare.spotResult', 
                stocks: result.data?.stocks || [],
                sortBy: result.data?.sort_by || sortBy,
                success: result.ok,
                error: result.error
            });
        } finally {
            this._panel.webview.postMessage({ command: 'akshare.loading', loading: false });
        }
    }
    
    private async _callBridge(action: string, params: any): Promise<any> {
        return new Promise((resolve) => {
            const pythonPath = this._getPythonPath();
            const projectRoot = this._getProjectRoot();
            const bridgePath = path.join(projectRoot, 'extension', 'python', 'bridge.py');
            
            // 构建PYTHONPATH：主文件夹 + mcp_servers + extension/python
            const pythonPaths = [
                projectRoot,
                path.join(projectRoot, 'mcp_servers'),
                path.join(projectRoot, 'extension', 'python')
            ].filter(p => fs.existsSync(p));
            
            const pythonPathStr = pythonPaths.join(path.delimiter);
            
            const proc = cp.spawn(pythonPath, [bridgePath], {
                cwd: projectRoot,
                env: { 
                    ...process.env, 
                    PYTHONPATH: pythonPathStr,
                    TRQUANT_ROOT: projectRoot,
                    PYTHONIOENCODING: 'utf-8'
                }
            });
            
            const input = JSON.stringify({ action, params });
            let output = '';
            let errorOutput = '';
            
            proc.stdout.on('data', (data: Buffer) => { output += data.toString(); });
            proc.stderr.on('data', (data: Buffer) => { errorOutput += data.toString(); });
            
            proc.on('close', () => {
                try {
                    const lines = output.trim().split('\\n');
                    const lastLine = lines[lines.length - 1];
                    resolve(JSON.parse(lastLine));
                } catch (e) {
                    resolve({ ok: false, error: 'JSON解析失败', output, errorOutput });
                }
            });
            
            proc.stdin.write(input);
            proc.stdin.end();
        });
    }

    private async _handleStrategyScan(params: any) {
        this._panel.webview.postMessage({ command: 'strategy.loading', loading: true });
        try {
            const result = await this._callMCP('market.analyze_trend', params);
            this._panel.webview.postMessage({
                command: 'strategy.scanResult', strategies: result.data?.strategies || [], success: result.ok
            });
        } finally {
            this._panel.webview.postMessage({ command: 'strategy.loading', loading: false });
        }
    }

    private async _handleStrategyList() {
        const result = await this._callMCP('strategy.list', {});
        this._panel.webview.postMessage({
            command: 'strategy.listResult', strategies: result.data?.strategies || [], success: result.ok
        });
    }

    private _getHtmlContent(): string {
        const nonce = this._getNonce();
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'nonce-${nonce}' 'unsafe-inline' 'unsafe-eval'; style-src 'unsafe-inline' 'unsafe-hashes'; img-src data: https:; font-src data:; connect-src 'none';">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TRQuant 统一仪表板</title>
    <style nonce="${nonce}">
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--vscode-editor-background); color: var(--vscode-editor-foreground); }
        .dashboard { display: flex; flex-direction: column; height: 100vh; }
        .tab-nav { display: flex; background: var(--vscode-sideBar-background); border-bottom: 1px solid var(--vscode-panel-border); padding: 0 16px; }
        .tab-item { padding: 12px 24px; cursor: pointer; border-bottom: 2px solid transparent; font-size: 14px; font-weight: 500; }
        .tab-item:hover { background: var(--vscode-list-hoverBackground); }
        .tab-item.active { border-bottom-color: var(--vscode-textLink-foreground); color: var(--vscode-textLink-foreground); }
        .tab-content { flex: 1; overflow-y: auto; padding: 20px; }
        .tab-panel { display: none; }
        .tab-panel.active { display: block; }
        .section { margin-bottom: 24px; }
        .section-title { font-size: 18px; font-weight: 600; margin-bottom: 16px; color: var(--vscode-textLink-foreground); }
        .button { padding: 8px 16px; background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; border-radius: 4px; cursor: pointer; font-size: 14px; margin-right: 8px; }
        .button:hover { background: var(--vscode-button-hoverBackground); }
        .loading { text-align: center; padding: 20px; color: var(--vscode-descriptionForeground); }
        .error { padding: 12px; background: var(--vscode-inputValidation-errorBackground); border-radius: 4px; margin: 12px 0; }
        .success { padding: 12px; background: var(--vscode-inputValidation-infoBackground); border-radius: 4px; margin: 12px 0; }
        
        /* MCP状态指示器 */
        .mcp-status { display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: var(--vscode-editor-background); border: 1px solid var(--vscode-panel-border); border-radius: 6px; font-size: 12px; margin-bottom: 16px; }
        .mcp-status-icon { width: 10px; height: 10px; border-radius: 50%; animation: pulse-status 2s infinite; }
        .mcp-status-icon.connected { background: #34c759; }
        .mcp-status-icon.disconnected { background: #ff3b30; }
        .mcp-status-icon.connecting { background: #ff9500; }
        @keyframes pulse-status { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .mcp-status-text { color: var(--vscode-descriptionForeground); }
        .mcp-status-badge { padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600; }
        .mcp-status-badge.ok { background: rgba(52, 199, 89, 0.2); color: #34c759; }
        .mcp-status-badge.error { background: rgba(255, 59, 48, 0.2); color: #ff3b30; }
        
        /* 错误面板增强 */
        .error-panel { background: var(--vscode-inputValidation-errorBackground); border: 1px solid var(--vscode-inputValidation-errorBorder); border-radius: 8px; padding: 16px; margin: 12px 0; }
        .error-panel-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
        .error-panel-icon { font-size: 24px; }
        .error-panel-title { font-weight: 600; font-size: 14px; color: var(--vscode-errorForeground); }
        .error-panel-message { font-size: 13px; line-height: 1.6; margin-bottom: 12px; }
        .error-panel-details { background: rgba(0,0,0,0.1); padding: 12px; border-radius: 4px; font-family: monospace; font-size: 11px; white-space: pre-wrap; word-break: break-all; max-height: 200px; overflow-y: auto; }
        .error-panel-actions { display: flex; gap: 8px; margin-top: 12px; }
        .error-panel-actions .button { font-size: 12px; padding: 6px 12px; }
        
        /* 工作流步骤错误状态增强 */
        .workflow-step .error-indicator { position: absolute; top: 8px; left: 8px; font-size: 16px; }
        .workflow-step .error-message { font-size: 10px; color: var(--vscode-errorForeground); margin-top: 6px; padding: 4px 6px; background: rgba(255,59,48,0.1); border-radius: 4px; word-break: break-word; max-height: 40px; overflow: hidden; text-overflow: ellipsis; }
        .workflow-step.error:hover .error-message { max-height: 100px; overflow-y: auto; }
        .workflow-steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; }
        .workflow-step { padding: 16px; background: var(--vscode-sideBar-background); border: 1px solid var(--vscode-panel-border); border-radius: 8px; cursor: pointer; transition: all 0.2s; text-align: center; position: relative; }
        .workflow-step:hover { border-color: var(--vscode-textLink-foreground); transform: translateY(-2px); }
        .workflow-step.completed { border-color: var(--vscode-testing-iconPassed); background: var(--vscode-testing-iconPassed); background: rgba(16, 185, 129, 0.1); }
        .workflow-step.running { border-color: var(--vscode-textLink-foreground); animation: pulse 1.5s infinite; }
        .workflow-step.error { border-color: var(--vscode-errorForeground); background: rgba(248, 81, 73, 0.1); }
        .workflow-step .status-badge { position: absolute; top: 8px; right: 8px; font-size: 10px; padding: 2px 6px; border-radius: 10px; }
        .workflow-step.running .status-badge { background: var(--vscode-textLink-foreground); color: white; }
        .workflow-step.completed .status-badge { background: var(--vscode-testing-iconPassed); color: white; }
        .workflow-step.error .status-badge { background: var(--vscode-errorForeground); color: white; }
        .workflow-step .result-toggle { margin-top: 8px; font-size: 11px; color: var(--vscode-textLink-foreground); cursor: pointer; }
        .workflow-result { margin-top: 16px; padding: 16px; background: var(--vscode-editor-background); border: 1px solid var(--vscode-panel-border); border-radius: 8px; display: none; }
        .workflow-result.show { display: block; }
        .workflow-result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .workflow-result-title { font-weight: 600; font-size: 14px; }
        .workflow-result-close { cursor: pointer; color: var(--vscode-descriptionForeground); font-size: 18px; }
        .workflow-result-content { max-height: 400px; overflow-y: auto; font-size: 12px; line-height: 1.6; }
        .workflow-result-content pre { background: var(--vscode-textCodeBlock-background); padding: 12px; border-radius: 4px; overflow-x: auto; }
        .workflow-result-content .metric { display: inline-block; margin: 4px 8px 4px 0; padding: 4px 8px; background: var(--vscode-badge-background); border-radius: 4px; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
        .tenbagger-list, .strategy-list { display: flex; flex-direction: column; gap: 8px; max-height: calc(100vh - 300px); overflow-y: auto; }
        .tenbagger-item, .strategy-item { padding: 12px 16px; background: var(--vscode-sideBar-background); border: 1px solid var(--vscode-panel-border); border-radius: 6px; cursor: pointer; transition: all 0.15s; }
        .tenbagger-item:hover, .strategy-item:hover { background: var(--vscode-list-hoverBackground); transform: translateX(4px); }
        .tenbagger-item.selected { background: var(--vscode-list-activeSelectionBackground); border-color: var(--vscode-textLink-foreground); }
        .tenbagger-item.level-s\\+, .tenbagger-item.level-s { border-left: 4px solid #ff6b6b; }
        .tenbagger-item.level-a { border-left: 4px solid #4ecdc4; }
        .tenbagger-item.level-b { border-left: 4px solid #ffe66d; }
        .tenbagger-item.level-c, .tenbagger-item.level-d { border-left: 4px solid #888; }
        
        /* 统计网格 - Apple风格 */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-bottom: 20px; }
        .stat-card { padding: 20px 16px; background: linear-gradient(135deg, var(--vscode-sideBar-background), var(--vscode-editor-background)); border: 1px solid var(--vscode-panel-border); border-radius: 12px; text-align: center; transition: transform 0.2s, box-shadow 0.2s; }
        .stat-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .stat-card.level-s { border-left: 4px solid #ff6b6b; }
        .stat-card.level-a { border-left: 4px solid #4ecdc4; }
        .stat-card.level-b { border-left: 4px solid #ffe66d; }
        .stat-card.highlight { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
        .stat-card.highlight .stat-value, .stat-card.highlight .stat-label { color: white; }
        .stat-value { font-size: 32px; font-weight: 700; color: var(--vscode-textLink-foreground); letter-spacing: -0.02em; }
        .stat-value.positive { color: #34c759; }
        .stat-value.negative { color: #ff3b30; }
        .stat-label { font-size: 12px; color: var(--vscode-descriptionForeground); margin-top: 6px; font-weight: 500; }
        
        /* 子标签导航 */
        .sub-tabs { display: flex; gap: 4px; background: var(--vscode-editor-background); padding: 6px; border-radius: 10px; margin-bottom: 16px; }
        .sub-tab { padding: 8px 16px; background: transparent; border: none; color: var(--vscode-descriptionForeground); border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500; transition: all 0.2s; }
        .sub-tab:hover { background: var(--vscode-list-hoverBackground); color: var(--vscode-foreground); }
        .sub-tab.active { background: var(--vscode-textLink-foreground); color: white; }
        .sub-panel { display: none; animation: fadeIn 0.3s ease; }
        .sub-panel.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
        
        /* 阶段时间线 */
        .timeline { position: relative; padding-left: 40px; margin: 20px 0; }
        .timeline::before { content: ''; position: absolute; left: 16px; top: 0; bottom: 0; width: 2px; background: var(--vscode-panel-border); }
        .timeline-item { position: relative; padding: 16px; background: var(--vscode-sideBar-background); border-radius: 10px; margin-bottom: 12px; border-left: 3px solid var(--vscode-panel-border); }
        .timeline-item::before { content: ''; position: absolute; left: -32px; top: 20px; width: 12px; height: 12px; border-radius: 50%; background: var(--vscode-panel-border); border: 3px solid var(--vscode-editor-background); }
        .timeline-item.s0::before { background: #9ca3af; }
        .timeline-item.s1::before { background: #f59e0b; }
        .timeline-item.s2::before { background: #10b981; }
        .timeline-item.s3::before { background: #ef4444; }
        .timeline-item.s1 { border-left-color: #f59e0b; }
        .timeline-item.s2 { border-left-color: #10b981; }
        .timeline-item.s3 { border-left-color: #ef4444; }
        .timeline-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
        .timeline-badge { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; }
        .timeline-badge.s0 { background: #f3f4f6; color: #6b7280; }
        .timeline-badge.s1 { background: #fef3c7; color: #92400e; }
        .timeline-badge.s2 { background: #dcfce7; color: #166534; }
        .timeline-badge.s3 { background: #fee2e2; color: #991b1b; }
        .timeline-title { font-weight: 600; font-size: 14px; }
        .timeline-desc { font-size: 12px; color: var(--vscode-descriptionForeground); line-height: 1.5; }
        
        /* 因子评分表格 */
        .factor-table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }
        .factor-table th, .factor-table td { padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--vscode-panel-border); }
        .factor-table th { background: var(--vscode-editor-background); font-weight: 600; color: var(--vscode-descriptionForeground); font-size: 12px; }
        .factor-table tr:hover { background: var(--vscode-list-hoverBackground); }
        .factor-table .positive { color: #34c759; }
        .factor-table .negative { color: #ff3b30; }
        
        /* 提示框 */
        .alert { padding: 14px 16px; border-radius: 8px; margin: 12px 0; display: flex; align-items: flex-start; gap: 10px; }
        .alert-info { background: rgba(0,113,227,0.1); border-left: 3px solid #0071e3; }
        .alert-success { background: rgba(52,199,89,0.1); border-left: 3px solid #34c759; }
        .alert-warning { background: rgba(255,149,0,0.1); border-left: 3px solid #ff9500; }
        .alert-icon { font-size: 18px; }
        .alert-content { flex: 1; }
        .alert-title { font-weight: 600; margin-bottom: 4px; font-size: 13px; }
        .alert-text { font-size: 12px; color: var(--vscode-descriptionForeground); line-height: 1.5; }
        
        /* 自定义提示和确认对话框 */
        .toast { position: fixed; top: 20px; right: 20px; background: var(--vscode-editor-background); border: 1px solid var(--vscode-panel-border); border-radius: 8px; padding: 12px 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 10000; max-width: 400px; animation: slideIn 0.3s ease; }
        .toast.success { border-left: 4px solid #34c759; }
        .toast.error { border-left: 4px solid #ff3b30; }
        .toast.info { border-left: 4px solid #0071e3; }
        @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        .confirm-dialog { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 10001; }
        .confirm-content { background: var(--vscode-editor-background); border: 1px solid var(--vscode-panel-border); border-radius: 8px; padding: 20px; max-width: 400px; }
        .confirm-title { font-weight: 600; margin-bottom: 12px; font-size: 16px; }
        .confirm-message { margin-bottom: 20px; color: var(--vscode-foreground); }
        .confirm-buttons { display: flex; gap: 8px; justify-content: flex-end; }
        .confirm-btn { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; font-size: 13px; }
        .confirm-btn.primary { background: var(--vscode-textLink-foreground); color: white; }
        .confirm-btn.secondary { background: var(--vscode-button-secondaryBackground); color: var(--vscode-button-secondaryForeground); }
        
        /* 工具栏 */
        .toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; gap: 12px; flex-wrap: wrap; }
        .toolbar-left, .toolbar-right { display: flex; gap: 8px; align-items: center; }
        .select-input, .text-input { padding: 8px 12px; background: var(--vscode-input-background); color: var(--vscode-input-foreground); border: 1px solid var(--vscode-input-border); border-radius: 4px; font-size: 13px; }
        .select-input:focus, .text-input:focus { outline: none; border-color: var(--vscode-focusBorder); }
        .text-input { min-width: 180px; }
        .button.primary { background: var(--vscode-textLink-foreground); }
        
        /* 分栏布局 */
        .content-split { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        .list-panel, .detail-panel { background: var(--vscode-sideBar-background); border: 1px solid var(--vscode-panel-border); border-radius: 8px; overflow: hidden; }
        .panel-header { padding: 12px 16px; font-weight: 600; background: var(--vscode-editor-background); border-bottom: 1px solid var(--vscode-panel-border); }
        .list-panel .tenbagger-list { padding: 12px; }
        
        /* 详情面板 */
        .detail-panel { min-height: 400px; }
        #stock-detail { padding: 16px; }
        .detail-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
        .detail-name { font-size: 20px; font-weight: 700; }
        .detail-level { padding: 4px 12px; border-radius: 4px; font-weight: 600; }
        .detail-level.level-s { background: #ff6b6b; color: white; }
        .detail-level.level-a { background: #4ecdc4; color: white; }
        .detail-level.level-b { background: #ffe66d; color: #333; }
        
        /* 评分条形图 */
        .dimension-bars { margin: 20px 0; }
        .dimension-row { display: flex; align-items: center; margin-bottom: 8px; }
        .dimension-name { width: 80px; font-size: 12px; color: var(--vscode-descriptionForeground); }
        .dimension-bar-bg { flex: 1; height: 20px; background: var(--vscode-editor-background); border-radius: 4px; overflow: hidden; margin: 0 8px; }
        .dimension-bar { height: 100%; background: linear-gradient(90deg, var(--vscode-textLink-foreground), #667eea); border-radius: 4px; transition: width 0.5s; }
        .dimension-score { width: 40px; text-align: right; font-weight: 600; font-size: 13px; }
        
        /* 优劣势 */
        .swot-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; }
        .swot-card { padding: 12px; background: var(--vscode-editor-background); border-radius: 6px; }
        .swot-title { font-weight: 600; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
        .swot-list { font-size: 12px; line-height: 1.6; color: var(--vscode-descriptionForeground); }
        .swot-list li { margin-bottom: 4px; }
        
        /* 弹窗 */
        .modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
        .modal-content { background: var(--vscode-editor-background); border: 1px solid var(--vscode-panel-border); border-radius: 8px; width: 400px; max-width: 90%; }
        .modal-header { padding: 16px; font-weight: 600; border-bottom: 1px solid var(--vscode-panel-border); }
        .modal-body { padding: 16px; }
        .modal-footer { padding: 16px; border-top: 1px solid var(--vscode-panel-border); text-align: right; }
        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; margin-bottom: 6px; font-size: 13px; color: var(--vscode-descriptionForeground); }
        .form-group .text-input { width: 100%; }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="tab-nav">
            <div class="tab-item active" data-tab="workflow">📊 9步工作流</div>
            <div class="tab-item" data-tab="tenbagger">🎯 十倍股识别</div>
            <div class="tab-item" data-tab="strategy">📈 趋势策略</div>
        </div>
        <div class="tab-content">
            <div class="tab-panel active" id="workflow-panel">
                <div class="section">
                    <!-- MCP状态指示器 -->
                    <div class="mcp-status" id="mcp-status">
                        <div class="mcp-status-icon connecting" id="mcp-status-icon"></div>
                        <span class="mcp-status-text">MCP服务器:</span>
                        <span class="mcp-status-badge" id="mcp-workflow-badge">检查中...</span>
                        <span class="mcp-status-badge" id="mcp-datasource-badge">数据源...</span>
                        <span class="mcp-status-badge" id="mcp-tenbagger-badge">十倍股...</span>
                        <button class="button" style="margin-left:auto;padding:4px 10px;font-size:11px;" data-action="checkMcpStatus">🔄 刷新状态</button>
                    </div>
                    
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                        <h2 class="section-title" style="margin:0;">9步投资工作流</h2>
                        <div style="display:flex;gap:8px;">
                            <button class="button primary" data-action="runAllWorkflowSteps">🚀 一键执行全部</button>
                            <button class="button" data-action="resetWorkflow">🔄 重置</button>
                        </div>
                    </div>
                    
                    <!-- 全局错误面板 -->
                    <div class="error-panel" id="global-error-panel" style="display:none;">
                        <div class="error-panel-header">
                            <span class="error-panel-icon">❌</span>
                            <span class="error-panel-title" id="error-panel-title">执行错误</span>
                        </div>
                        <div class="error-panel-message" id="error-panel-message">发生了一个错误</div>
                        <div class="error-panel-details" id="error-panel-details"></div>
                        <div class="error-panel-actions">
                            <button class="button" data-action="copyError">📋 复制错误</button>
                            <button class="button" data-action="searchError">🔍 搜索解决方案</button>
                            <button class="button" data-action="closeError">✕ 关闭</button>
                        </div>
                    </div>
                    
                    <div class="workflow-steps" id="workflow-steps"></div>
                    <div id="workflow-results-container" style="margin-top: 20px;"></div>
                </div>
            </div>
            <div class="tab-panel" id="tenbagger-panel">
                <!-- 子标签导航 -->
                <div class="sub-tabs">
                    <button class="sub-tab active" data-subtab="overview">📊 概览</button>
                    <button class="sub-tab" data-subtab="ranking">🏆 排名</button>
                    <button class="sub-tab" data-subtab="stages">📈 阶段分析</button>
                    <button class="sub-tab" data-subtab="factors">🔢 因子体系</button>
                    <button class="sub-tab" data-subtab="validation">✅ 验证结果</button>
                </div>
                
                <!-- 概览面板 -->
                <div class="sub-panel active" id="overview-panel">
                    <!-- AKShare 实时市场数据 -->
                    <div class="alert alert-info" style="margin-bottom:10px;">
                        <span class="alert-icon">📡</span>
                        <div class="alert-content">
                            <div class="alert-title">AKShare 实时市场数据</div>
                            <div class="alert-text">点击按钮获取A股实时行情、板块涨跌等市场数据</div>
                        </div>
                    </div>
                    <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
                        <button class="button primary" data-action="loadHotIndustries">🔥 热门行业</button>
                        <button class="button" data-action="loadHotConcepts">💡 热门概念</button>
                        <button class="button" data-action="loadTopGainers">📈 涨幅榜</button>
                        <button class="button" data-action="loadTopVolume">📊 成交榜</button>
                        <button class="button" data-action="testButtonClick" style="background:var(--vscode-button-secondaryBackground);color:var(--vscode-button-secondaryForeground);">🧪 测试按钮</button>
                    </div>
                    <div id="debug-info" style="font-size:11px;color:var(--vscode-descriptionForeground);margin-bottom:8px;padding:8px;background:var(--vscode-editor-background);border-radius:4px;display:none;">
                        <div><strong>调试信息:</strong></div>
                        <div id="debug-content"></div>
                    </div>
                    <div id="realtime-data" style="min-height:120px;background:var(--vscode-editor-background);border-radius:6px;padding:12px;margin-bottom:16px;">
                        <div style="color:var(--vscode-descriptionForeground);font-size:12px;text-align:center;padding:20px;">点击上方按钮加载实时市场数据...</div>
                    </div>
                    
                    <!-- 十倍股识别系统 -->
                    <div class="alert alert-info">
                        <span class="alert-icon">📊</span>
                        <div class="alert-content">
                            <div class="alert-title">十倍股早期识别系统 V3.0</div>
                            <div class="alert-text">基于A股100家十倍股案例研究，使用7维评分体系综合评估。连接JQData金融数据库+AKShare实时数据。</div>
                        </div>
                    </div>
                    <div class="stats-grid" id="tenbagger-stats">
                        <div class="stat-card highlight"><div class="stat-value" id="stat-total">-</div><div class="stat-label">已评估</div></div>
                        <div class="stat-card level-s"><div class="stat-value" id="stat-s">-</div><div class="stat-label">A级 (强推荐)</div></div>
                        <div class="stat-card level-a"><div class="stat-value" id="stat-a">-</div><div class="stat-label">B级 (推荐)</div></div>
                        <div class="stat-card level-b"><div class="stat-value" id="stat-b">-</div><div class="stat-label">C级 (关注)</div></div>
                        <div class="stat-card"><div class="stat-value" id="stat-avgret">-</div><div class="stat-label">平均分</div></div>
                        <div class="stat-card"><div class="stat-value" id="stat-source">-</div><div class="stat-label">数据来源</div></div>
                    </div>
                    <h3 style="font-size:15px; font-weight:600; margin:20px 0 12px;">阶段分布</h3>
                    <div class="stats-grid" style="grid-template-columns: repeat(4, 1fr);">
                        <div class="stat-card" style="border-left-color:#9ca3af;"><div class="stat-value" id="stage-s0-count" style="font-size:24px;">-</div><div class="stat-label">S0 观察期</div></div>
                        <div class="stat-card" style="border-left-color:#f59e0b;"><div class="stat-value" id="stage-s1-count" style="font-size:24px;">-</div><div class="stat-label">S1 验证期</div></div>
                        <div class="stat-card" style="border-left-color:#10b981;"><div class="stat-value" id="stage-s2-count" style="font-size:24px;">-</div><div class="stat-label">S2 导入期 ⭐</div></div>
                        <div class="stat-card" style="border-left-color:#ef4444;"><div class="stat-value" id="stage-s3-count" style="font-size:24px;">-</div><div class="stat-label">S3 放量期</div></div>
                    </div>
                    <h3 style="font-size:15px; font-weight:600; margin:20px 0 12px;">十倍股核心特征</h3>
                    <div class="stats-grid" style="grid-template-columns: repeat(4, 1fr);">
                        <div class="stat-card"><div class="stat-value" style="font-size:24px;">~17亿</div><div class="stat-label">起步市值均值</div></div>
                        <div class="stat-card"><div class="stat-value" style="font-size:24px;">78%</div><div class="stat-label">30亿以下占比</div></div>
                        <div class="stat-card"><div class="stat-value" style="font-size:24px;">~23%</div><div class="stat-label">净利润CAGR</div></div>
                        <div class="stat-card"><div class="stat-value" style="font-size:24px;">~8年</div><div class="stat-label">创十倍平均用时</div></div>
                    </div>
                    <div class="alert alert-warning" style="margin-top:16px;">
                        <span class="alert-icon">⚠️</span>
                        <div class="alert-content">
                            <div class="alert-title">风险提示</div>
                            <div class="alert-text">2019年以来100只十倍股中，61只在高点后回撤超过50%。建议严格执行止损规则（-7%~-8%）和分批止盈策略。</div>
                        </div>
                    </div>
                </div>
                
                <!-- 排名面板 -->
                <div class="sub-panel" id="ranking-panel">
                    <div class="alert alert-info" style="margin-bottom:12px;">
                        <span class="alert-icon">📊</span>
                        <div class="alert-content">
                            <div class="alert-title">JQData金融数据扫描</div>
                            <div class="alert-text">设置筛选条件，从JQData获取实时数据并评估十倍股潜力</div>
                        </div>
                    </div>
                    <div class="toolbar" style="flex-wrap:wrap;gap:8px;">
                        <div class="toolbar-left" style="flex-wrap:wrap;gap:6px;">
                            <div style="display:flex;align-items:center;gap:4px;">
                                <label style="font-size:11px;color:var(--vscode-descriptionForeground);">市值:</label>
                                <input type="number" id="min-market-cap" class="text-input" value="20" style="width:60px;" placeholder="最小"/>
                                <span style="color:var(--vscode-descriptionForeground);">-</span>
                                <input type="number" id="max-market-cap" class="text-input" value="300" style="width:60px;" placeholder="最大"/>
                                <span style="font-size:11px;color:var(--vscode-descriptionForeground);">亿</span>
                            </div>
                            <div style="display:flex;align-items:center;gap:4px;">
                                <label style="font-size:11px;color:var(--vscode-descriptionForeground);">ROE≥</label>
                                <input type="number" id="min-roe" class="text-input" value="8" style="width:50px;"/>
                                <span style="font-size:11px;color:var(--vscode-descriptionForeground);">%</span>
                            </div>
                            <div style="display:flex;align-items:center;gap:4px;">
                                <label style="font-size:11px;color:var(--vscode-descriptionForeground);">营收增≥</label>
                                <input type="number" id="min-revenue-growth" class="text-input" value="15" style="width:50px;"/>
                                <span style="font-size:11px;color:var(--vscode-descriptionForeground);">%</span>
                            </div>
                        </div>
                        <div class="toolbar-right">
                            <button class="button primary" data-action="jqdataScan">🔍 JQData扫描</button>
                            <button class="button" data-action="refreshTenbaggerData">📁 缓存数据</button>
                        </div>
                    </div>
                    <div class="content-split">
                        <div class="list-panel">
                            <div class="panel-header">潜力股排名 <span style="font-weight:normal;color:var(--vscode-descriptionForeground);font-size:12px;">(点击查看详情)</span></div>
                            <div id="tenbagger-list" class="tenbagger-list"><div class="loading">点击刷新加载数据...</div></div>
                        </div>
                        <div class="detail-panel" id="detail-panel">
                            <div class="panel-header">详情分析 <span id="close-detail" data-action="closeDetail" style="cursor:pointer;float:right;">✕</span></div>
                            <div id="stock-detail"><div class="loading" style="padding:40px;">选择左侧股票查看详情</div></div>
                        </div>
                    </div>
                </div>
                
                <!-- 阶段分析面板 -->
                <div class="sub-panel" id="stages-panel">
                    <div class="alert alert-info">
                        <span class="alert-icon">🔄</span>
                        <div class="alert-content">
                            <div class="alert-title">三轴阶段判定体系</div>
                            <div class="alert-text">基本面轴（Fundamental）+ 资金轴（Flow）+ 预期轴（Expectation）综合判定股票所处阶段</div>
                        </div>
                    </div>
                    <div class="timeline">
                        <div class="timeline-item s0">
                            <div class="timeline-header"><span class="timeline-badge s0">S0</span><span class="timeline-title">观察期 — 排除或等待</span></div>
                            <div class="timeline-desc">• 营收增速 &lt; 15%，利润增速 &lt; 20%<br>• 成交量萎缩，价格横盘/下跌<br>• 无催化剂，分析师覆盖稀少</div>
                        </div>
                        <div class="timeline-item s1">
                            <div class="timeline-header"><span class="timeline-badge s1">S1</span><span class="timeline-title">验证期 — 重点关注，小仓试探</span></div>
                            <div class="timeline-desc">• 营收增速 &gt; 15%，利润增速 &gt; 20%<br>• 成交量回升 &gt;50%，价格企稳<br>• 分析师覆盖增加，潜在催化剂酝酿中</div>
                        </div>
                        <div class="timeline-item s2">
                            <div class="timeline-header"><span class="timeline-badge s2">S2</span><span class="timeline-title">导入期 — ⭐最佳买入点</span></div>
                            <div class="timeline-desc">• 营收增速 &gt; 25%，利润增速 &gt; 30%，连续2季度改善<br>• 成交量增加 &gt;100%，突破关键位，均线多头排列<br>• 重大催化剂出现，分析师评级上调，PE重估开始</div>
                        </div>
                        <div class="timeline-item s3">
                            <div class="timeline-header"><span class="timeline-badge s3">S3</span><span class="timeline-title">放量期 — 持有/分批止盈</span></div>
                            <div class="timeline-desc">• 营收增速 &gt; 40%，利润增速 &gt; 50%<br>• 换手率极高，加速上涨，警惕巨量长上影<br>• 市场关注度极高，估值泡沫风险，需设置移动止损</div>
                        </div>
                    </div>
                </div>
                
                <!-- 因子体系面板 -->
                <div class="sub-panel" id="factors-panel">
                    <div class="stats-grid" style="grid-template-columns: repeat(4, 1fr); margin-bottom:20px;">
                        <div class="stat-card"><div class="stat-value" style="font-size:24px;color:#667eea;">40分</div><div class="stat-label">财务因子</div></div>
                        <div class="stat-card"><div class="stat-value" style="font-size:24px;color:#34c759;">25分</div><div class="stat-label">成长动量</div></div>
                        <div class="stat-card"><div class="stat-value" style="font-size:24px;color:#ff9500;">20分</div><div class="stat-label">估值因子</div></div>
                        <div class="stat-card"><div class="stat-value" style="font-size:24px;color:#af52de;">15分</div><div class="stat-label">技术因子</div></div>
                    </div>
                    <h3 style="font-size:14px; font-weight:600; margin:16px 0 10px;">财务因子评分标准（40分）</h3>
                    <table class="factor-table">
                        <thead><tr><th>因子</th><th>权重</th><th>优秀(满分)</th><th>良好(70%)</th><th>一般(30%)</th></tr></thead>
                        <tbody>
                            <tr><td>营收增速</td><td>10分</td><td class="positive">≥ 30%</td><td>≥ 15%</td><td>≥ 0%</td></tr>
                            <tr><td>利润增速</td><td>10分</td><td class="positive">≥ 50%</td><td>≥ 20%</td><td>≥ 0%</td></tr>
                            <tr><td>毛利率</td><td>8分</td><td class="positive">≥ 40%</td><td>≥ 25%</td><td>≥ 15%</td></tr>
                            <tr><td>ROE</td><td>7分</td><td class="positive">≥ 15%</td><td>≥ 10%</td><td>≥ 5%</td></tr>
                            <tr><td>净利率</td><td>5分</td><td class="positive">≥ 15%</td><td>≥ 5%</td><td>-</td></tr>
                        </tbody>
                    </table>
                    <h3 style="font-size:14px; font-weight:600; margin:16px 0 10px;">等级划分</h3>
                    <div class="stats-grid" style="grid-template-columns: repeat(6, 1fr);">
                        <div class="stat-card" style="padding:12px;"><span class="timeline-badge" style="background:#fef3c7;color:#92400e;">S+</span><div style="margin-top:8px;font-size:11px;color:var(--vscode-descriptionForeground);">≥80分</div></div>
                        <div class="stat-card" style="padding:12px;"><span class="timeline-badge" style="background:#dcfce7;color:#166534;">S</span><div style="margin-top:8px;font-size:11px;color:var(--vscode-descriptionForeground);">≥70分</div></div>
                        <div class="stat-card" style="padding:12px;"><span class="timeline-badge" style="background:#dbeafe;color:#1e40af;">A</span><div style="margin-top:8px;font-size:11px;color:var(--vscode-descriptionForeground);">≥60分</div></div>
                        <div class="stat-card" style="padding:12px;"><span class="timeline-badge" style="background:#e0e7ff;color:#3730a3;">B</span><div style="margin-top:8px;font-size:11px;color:var(--vscode-descriptionForeground);">≥50分</div></div>
                        <div class="stat-card" style="padding:12px;"><span class="timeline-badge" style="background:#f3f4f6;color:#374151;">C</span><div style="margin-top:8px;font-size:11px;color:var(--vscode-descriptionForeground);">≥40分</div></div>
                        <div class="stat-card" style="padding:12px;"><span class="timeline-badge" style="background:#fee2e2;color:#991b1b;">D</span><div style="margin-top:8px;font-size:11px;color:var(--vscode-descriptionForeground);">&lt;40分</div></div>
                    </div>
                </div>
                
                <!-- 验证结果面板 -->
                <div class="sub-panel" id="validation-panel">
                    <div class="alert alert-success">
                        <span class="alert-icon">✅</span>
                        <div class="alert-content">
                            <div class="alert-title">体系有效性验证</div>
                            <div class="alert-text">基于JQData识别 + AKShare验证，研究期后3个月数据验证</div>
                        </div>
                    </div>
                    <div class="stats-grid" style="grid-template-columns: repeat(4, 1fr);">
                        <div class="stat-card highlight"><div class="stat-value">80%</div><div class="stat-label">正收益比例</div></div>
                        <div class="stat-card"><div class="stat-value positive">+12.4%</div><div class="stat-label">平均收益</div></div>
                        <div class="stat-card"><div class="stat-value positive">+72.6%</div><div class="stat-label">最大收益</div></div>
                        <div class="stat-card"><div class="stat-value negative">-20.0%</div><div class="stat-label">最大回撤</div></div>
                    </div>
                    <h3 style="font-size:14px; font-weight:600; margin:20px 0 10px;">Top验证案例</h3>
                    <table class="factor-table">
                        <thead><tr><th>代码</th><th>名称</th><th>得分</th><th>阶段</th><th>研究期后收益</th><th>总收益</th></tr></thead>
                        <tbody>
                            <tr><td>000688</td><td>国城矿业</td><td>54.4</td><td><span class="timeline-badge s1">S1</span></td><td class="positive">+72.64%</td><td class="positive">+109.25%</td></tr>
                            <tr><td>000603</td><td>盛达资源</td><td>47.6</td><td><span class="timeline-badge s1">S1</span></td><td class="positive">+49.38%</td><td class="positive">+102.54%</td></tr>
                            <tr><td>000426</td><td>兴业银锡</td><td>53.0</td><td><span class="timeline-badge s1">S1</span></td><td class="positive">+41.60%</td><td class="positive">+135.69%</td></tr>
                            <tr><td>000833</td><td>粤桂股份</td><td>50.1</td><td><span class="timeline-badge s0">S0</span></td><td class="positive">+32.38%</td><td class="positive">+57.01%</td></tr>
                            <tr><td>000737</td><td>北方铜业</td><td>41.1</td><td><span class="timeline-badge s1">S1</span></td><td class="positive">+3.50%</td><td class="positive">+61.43%</td></tr>
                        </tbody>
                    </table>
                    <div class="alert alert-warning" style="margin-top:16px;">
                        <span class="alert-icon">💡</span>
                        <div class="alert-content">
                            <div class="alert-title">优化建议</div>
                            <div class="alert-text">优选S1/S2阶段 + 得分50+的标的 | 止损设置-8% | 分散持仓≥5只</div>
                        </div>
                    </div>
                </div>
                
            </div>
            <div class="tab-panel" id="strategy-panel">
                <div class="section">
                    <h2 class="section-title">趋势策略追踪</h2>
                    <div style="margin-bottom: 16px;">
                        <button class="button" data-action="scanStrategies">扫描策略</button>
                        <button class="button" data-action="refreshStrategyList">刷新列表</button>
                    </div>
                    <div id="strategy-content"><div class="loading">点击刷新加载数据...</div></div>
                </div>
            </div>
        </div>
    </div>
    <script nonce="${nonce}">
        const vscode = acquireVsCodeApi();
        let currentTab = 'workflow';
        let currentSubTab = 'overview';
        let tenbaggerData = []; // 缓存十倍股数据
        let selectedStock = null;
        
        // === 按钮事件绑定 (统一处理所有按钮) ===
        function bindButtonEvents() {
            // 1. 绑定data-action按钮
            const actionButtons = document.querySelectorAll('[data-action]');
            console.log('[WebView] 找到', actionButtons.length, '个data-action按钮');
            
            // 调试：列出所有按钮
            actionButtons.forEach((btn, idx) => {
                const action = btn.getAttribute('data-action');
                const step = btn.getAttribute('data-step');
                console.log('[WebView] 按钮' + (idx + 1) + ': action="' + action + '", step="' + step + '"');
            });
            
            actionButtons.forEach(function(button) {
                const action = button.getAttribute('data-action');
                const step = button.getAttribute('data-step'); // 工作流步骤ID
                
                // 移除旧的事件监听器（通过克隆节点）
                const newButton = button.cloneNode(true);
                button.parentNode.replaceChild(newButton, button);
                
                newButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    console.log('[WebView] ✅ 按钮被点击:', action, step ? '(步骤' + step + ')' : '');
                    
                    // 显示点击反馈
                    newButton.style.opacity = '0.6';
                    setTimeout(() => { newButton.style.opacity = '1'; }, 200);
                    
                    // 执行对应操作
                    try {
                        if (action === 'runWorkflowStep' && step) {
                            // 工作流步骤
                            console.log('[WebView] 调用 runWorkflowStep(' + step + ')');
                            if (typeof window.runWorkflowStep === 'function') {
                                window.runWorkflowStep(parseInt(step));
                            } else {
                                showToast('❌ 错误: runWorkflowStep 函数不存在！', 'error');
                                console.error('[WebView] runWorkflowStep 函数不存在');
                            }
                        } else {
                            // 其他按钮
                            switch(action) {
                                case 'loadHotIndustries':
                                    if (typeof window.loadHotIndustries === 'function') {
                                        window.loadHotIndustries();
                                    } else {
                                        showToast('❌ 错误: loadHotIndustries 函数不存在！', 'error');
                                        console.error('[WebView] loadHotIndustries 函数不存在');
                                    }
                                    break;
                                case 'loadHotConcepts':
                                    if (typeof window.loadHotConcepts === 'function') {
                                        window.loadHotConcepts();
                                    } else {
                                        showToast('❌ 错误: loadHotConcepts 函数不存在！', 'error');
                                        console.error('[WebView] loadHotConcepts 函数不存在');
                                    }
                                    break;
                                case 'loadTopGainers':
                                    if (typeof window.loadTopGainers === 'function') {
                                        window.loadTopGainers();
                                    } else {
                                        showToast('❌ 错误: loadTopGainers 函数不存在！', 'error');
                                        console.error('[WebView] loadTopGainers 函数不存在');
                                    }
                                    break;
                                case 'loadTopVolume':
                                    if (typeof window.loadTopVolume === 'function') {
                                        window.loadTopVolume();
                                    } else {
                                        showToast('❌ 错误: loadTopVolume 函数不存在！', 'error');
                                        console.error('[WebView] loadTopVolume 函数不存在');
                                    }
                                    break;
                                case 'testButtonClick':
                                    if (typeof window.testButtonClick === 'function') {
                                        window.testButtonClick();
                                    } else {
                                        showToast('❌ 错误: testButtonClick 函数不存在！', 'error');
                                        console.error('[WebView] testButtonClick 函数不存在');
                                    }
                                    break;
                                case 'jqdataScan':
                                    if (typeof window.jqdataScan === 'function') {
                                        window.jqdataScan();
                                    } else {
                                        showToast('❌ 错误: jqdataScan 函数不存在！', 'error');
                                        console.error('[WebView] jqdataScan 函数不存在');
                                    }
                                    break;
                                case 'refreshTenbaggerData':
                                    if (typeof window.refreshTenbaggerData === 'function') {
                                        window.refreshTenbaggerData();
                                    } else {
                                        showToast('❌ 错误: refreshTenbaggerData 函数不存在！', 'error');
                                        console.error('[WebView] refreshTenbaggerData 函数不存在');
                                    }
                                    break;
                                case 'closeDetail':
                                    if (typeof window.closeDetail === 'function') {
                                        window.closeDetail();
                                    } else {
                                        showToast('❌ 错误: closeDetail 函数不存在！', 'error');
                                        console.error('[WebView] closeDetail 函数不存在');
                                    }
                                    break;
                                case 'scanStrategies':
                                    if (typeof window.scanStrategies === 'function') {
                                        window.scanStrategies();
                                    } else {
                                        showToast('❌ 错误: scanStrategies 函数不存在！', 'error');
                                        console.error('[WebView] scanStrategies 函数不存在');
                                    }
                                    break;
                                case 'refreshStrategyList':
                                    if (typeof window.refreshStrategyList === 'function') {
                                        window.refreshStrategyList();
                                    } else {
                                        showToast('❌ 错误: refreshStrategyList 函数不存在！', 'error');
                                        console.error('[WebView] refreshStrategyList 函数不存在');
                                    }
                                    break;
                                case 'runAllWorkflowSteps':
                                    if (typeof window.runAllWorkflowSteps === 'function') {
                                        window.runAllWorkflowSteps();
                                    } else {
                                        showToast('❌ 错误: runAllWorkflowSteps 函数不存在！', 'error');
                                        console.error('[WebView] runAllWorkflowSteps 函数不存在');
                                    }
                                    break;
                                case 'resetWorkflow':
                                    if (typeof window.resetWorkflow === 'function') {
                                        window.resetWorkflow();
                                    } else {
                                        showToast('❌ 错误: resetWorkflow 函数不存在！', 'error');
                                        console.error('[WebView] resetWorkflow 函数不存在');
                                    }
                                    break;
                                case 'toggleResult':
                                    if (typeof window.toggleWorkflowResult === 'function' && step) {
                                        window.toggleWorkflowResult(parseInt(step));
                                    } else {
                                        showToast('❌ 错误: toggleWorkflowResult 函数不存在！', 'error');
                                        console.error('[WebView] toggleWorkflowResult 函数不存在');
                                    }
                                    break;
                                case 'closeResult':
                                    if (typeof window.closeWorkflowResult === 'function' && step) {
                                        window.closeWorkflowResult(parseInt(step));
                                    }
                                    break;
                                case 'checkMcpStatus':
                                    if (typeof window.checkMcpStatus === 'function') {
                                        window.checkMcpStatus();
                                    }
                                    break;
                                case 'copyError':
                                    if (typeof window.copyError === 'function') {
                                        window.copyError();
                                    }
                                    break;
                                case 'searchError':
                                    if (typeof window.searchError === 'function') {
                                        window.searchError();
                                    }
                                    break;
                                case 'closeError':
                                    if (typeof window.closeErrorPanel === 'function') {
                                        window.closeErrorPanel();
                                    }
                                    break;
                                default:
                                    console.warn('[WebView] Unknown action:', action);
                            }
                        }
                    } catch (error) {
                        console.error('[WebView] 执行操作时出错:', error);
                        showToast('执行出错: ' + (error.message || String(error)), 'error');
                    }
                }, true);
            });
            
            // 2. 绑定data-subtab子标签按钮
            const subtabButtons = document.querySelectorAll('[data-subtab]');
            console.log('[WebView] 找到', subtabButtons.length, '个子标签按钮');
            
            subtabButtons.forEach(function(button) {
                const subtab = button.getAttribute('data-subtab');
                
                // 移除旧的事件监听器
                const newButton = button.cloneNode(true);
                button.parentNode.replaceChild(newButton, button);
                
                newButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    console.log('[WebView] ✅ 子标签被点击:', subtab);
                    
                    if (typeof window.switchSubTab === 'function') {
                        window.switchSubTab(subtab);
                    } else {
                        showToast('❌ 错误: switchSubTab 函数不存在！', 'error');
                        console.error('[WebView] switchSubTab 函数不存在');
                    }
                }, true);
            });
        }
        
        // DOM加载完成后初始化
        function initializeAll() {
            console.log('[WebView] 开始初始化所有功能');
            
            // 1. 初始化工作流步骤
            initWorkflowSteps();
            
            // 2. 绑定所有按钮事件（延迟确保DOM完全渲染）
            setTimeout(() => {
                bindButtonEvents();
                console.log('[WebView] 所有按钮事件已绑定');
                
                // 验证工作流步骤按钮
                const workflowStepButtons = document.querySelectorAll('.workflow-step[data-action="runWorkflowStep"]');
                console.log('[WebView] 验证：找到', workflowStepButtons.length, '个工作流步骤按钮');
                workflowStepButtons.forEach((btn, idx) => {
                    const step = btn.getAttribute('data-step');
                    console.log('[WebView] 工作流步骤' + (idx + 1) + ': step="' + step + '"');
                });
            }, 300);
            
            // 3. 页面加载完成后的诊断
            setTimeout(() => {
                const debugDiv = document.getElementById('debug-info');
                const debugContent = document.getElementById('debug-content');
                
                if (debugDiv && debugContent) {
                    const actionButtons = document.querySelectorAll('[data-action]');
                    const subtabButtons = document.querySelectorAll('[data-subtab]');
                    const functions = {
                        'loadHotIndustries': typeof window.loadHotIndustries,
                        'loadHotConcepts': typeof window.loadHotConcepts,
                        'loadTopGainers': typeof window.loadTopGainers,
                        'loadTopVolume': typeof window.loadTopVolume,
                        'testButtonClick': typeof window.testButtonClick,
                        'runWorkflowStep': typeof window.runWorkflowStep,
                        'switchSubTab': typeof window.switchSubTab,
                        'jqdataScan': typeof window.jqdataScan,
                        'refreshTenbaggerData': typeof window.refreshTenbaggerData
                    };
                    
                    let html = '<div style="color:var(--vscode-descriptionForeground);"><strong>自动诊断:</strong><br>';
                    html += '<div style="margin-top:4px;">找到 ' + actionButtons.length + ' 个操作按钮, ' + subtabButtons.length + ' 个子标签按钮</div>';
                    html += '<div style="margin-top:4px;">函数状态: ';
                    let allOk = true;
                    for (const [name, value] of Object.entries(functions)) {
                        if (!value || value !== 'function') allOk = false;
                        const status = (value === 'function') ? '✅' : '❌';
                        html += status + ' ' + name + ' ';
                    }
                    html += '</div></div>';
                    
                    if (!allOk) {
                        debugContent.innerHTML = html + '<div style="margin-top:8px;color:var(--vscode-errorForeground);">⚠️ 发现问题！请点击"🧪 测试按钮"查看详细信息。</div>';
                        debugDiv.style.display = 'block';
                    } else {
                        debugContent.innerHTML = html + '<div style="margin-top:8px;color:var(--vscode-textBlockQuote-border);">✅ 所有检查通过！按钮应该可以正常工作。</div>';
                        debugDiv.style.display = 'block';
                    }
                }
            }, 500);
        }
        
        // DOM加载完成后初始化
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializeAll);
        } else {
            // DOM已经加载完成，立即初始化
            initializeAll();
        }
        
        // 备用：事件委托（防止直接绑定失败）
        document.addEventListener('click', function(e) {
            const actionButton = e.target.closest('[data-action]');
            const subtabButton = e.target.closest('[data-subtab]');
            
            if (actionButton) {
                console.log('[WebView] 备用事件委托捕获到点击:', actionButton.getAttribute('data-action'));
                actionButton.click(); // 触发已绑定的事件
            } else if (subtabButton) {
                console.log('[WebView] 备用事件委托捕获到子标签点击:', subtabButton.getAttribute('data-subtab'));
                subtabButton.click(); // 触发已绑定的事件
            }
        }, true);
        
        // 子标签切换 (挂载到window以便onclick调用)
        window.switchSubTab = function(tab) {
            currentSubTab = tab;
            document.querySelectorAll('.sub-tab').forEach(t => t.classList.toggle('active', t.textContent.includes(getSubTabName(tab))));
            document.querySelectorAll('.sub-panel').forEach(p => p.classList.toggle('active', p.id === tab + '-panel'));
            if (tab === 'ranking' && tenbaggerData.length === 0) {
                window.refreshTenbaggerData();
            }
        }
        function getSubTabName(tab) {
            const names = { overview: '概览', ranking: '排名', stages: '阶段', factors: '因子', validation: '验证' };
            return names[tab] || tab;
        }
        
        const workflowSteps = [
            { id: 1, name: '数据源检查', icon: '🔍' },
            { id: 2, name: '市场趋势分析', icon: '📊' },
            { id: 3, name: '投资主线识别', icon: '🎯' },
            { id: 4, name: '候选池构建', icon: '📦' },
            { id: 5, name: '因子推荐', icon: '🔢' },
            { id: 6, name: '策略生成', icon: '⚙️' },
            { id: 7, name: '回测验证', icon: '🧪' },
            { id: 8, name: '参数优化', icon: '🎛️' },
            { id: 9, name: '实盘部署', icon: '🚀' }
        ];
        
        // 十倍股评估维度配置
        const dimensions = [
            { key: 'stage', name: '阶段', weight: 0.20 },
            { key: 'scorecard', name: '评分卡', weight: 0.25 },
            { key: 'growth', name: '成长性', weight: 0.15 },
            { key: 'industry', name: '行业', weight: 0.15 },
            { key: 'altdata', name: '另类数据', weight: 0.10 },
            { key: 'momentum', name: '动量', weight: 0.10 },
            { key: 'risk', name: '风控', weight: 0.05 }
        ];
        
        // Tab 切换
        document.querySelectorAll('.tab-item').forEach(item => {
            item.addEventListener('click', () => {
                const tab = item.dataset.tab;
                currentTab = tab;
                document.querySelectorAll('.tab-item').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
                document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('active', p.id === tab + '-panel'));
                vscode.postMessage({ command: 'switchTab', tab });
                if (tab === 'tenbagger') {
                    // 获取统计数据
                    vscode.postMessage({ command: 'tenbagger.getStats' });
                }
            });
        });
        
        // === MCP状态检查 ===
        let lastError = { title: '', message: '', details: '' };
        
        window.checkMcpStatus = function() {
            console.log('[WebView] 检查MCP状态...');
            updateMcpStatusUI('connecting', 'workflow', '检查中...');
            updateMcpStatusUI('connecting', 'datasource', '检查中...');
            updateMcpStatusUI('connecting', 'tenbagger', '检查中...');
            vscode.postMessage({ command: 'mcp.checkStatus' });
        };
        
        function updateMcpStatusUI(status, server, text) {
            const iconEl = document.getElementById('mcp-status-icon');
            const badgeId = 'mcp-' + server + '-badge';
            const badgeEl = document.getElementById(badgeId);
            
            if (iconEl) {
                iconEl.className = 'mcp-status-icon ' + status;
            }
            
            if (badgeEl) {
                badgeEl.textContent = text;
                badgeEl.className = 'mcp-status-badge ' + (status === 'connected' ? 'ok' : status === 'disconnected' ? 'error' : '');
            }
        }
        
        // === 错误面板管理 ===
        window.showErrorPanel = function(title, message, details) {
            lastError = { title, message, details };
            const panel = document.getElementById('global-error-panel');
            const titleEl = document.getElementById('error-panel-title');
            const msgEl = document.getElementById('error-panel-message');
            const detailsEl = document.getElementById('error-panel-details');
            
            if (panel) {
                panel.style.display = 'block';
                if (titleEl) titleEl.textContent = title;
                if (msgEl) msgEl.textContent = message;
                if (detailsEl) detailsEl.textContent = details || '无详细信息';
            }
        };
        
        window.closeErrorPanel = function() {
            const panel = document.getElementById('global-error-panel');
            if (panel) panel.style.display = 'none';
        };
        
        window.copyError = function() {
            const text = '错误: ' + lastError.title + '\\n' + lastError.message + '\\n\\n详细信息:\\n' + lastError.details;
            navigator.clipboard.writeText(text).then(() => {
                showToast('✅ 错误信息已复制到剪贴板', 'success');
            }).catch(err => {
                console.error('复制失败:', err);
                showToast('❌ 复制失败: ' + err.message, 'error');
            });
        };
        
        window.searchError = function() {
            // 发送搜索请求到后端
            vscode.postMessage({ 
                command: 'error.search', 
                query: lastError.title + ' ' + lastError.message 
            });
        };
        
        // === 工作流功能 ===
        function initWorkflowSteps() {
            const container = document.getElementById('workflow-steps');
            if (!container) {
                console.error('[WebView] 找不到 workflow-steps 容器！');
                return;
            }
            container.innerHTML = workflowSteps.map(step => 
                '<div class="workflow-step" data-step="' + step.id + '" data-action="runWorkflowStep" style="cursor: pointer;">' +
                '<span class="error-indicator" style="display: none;">⚠️</span>' +
                '<span class="status-badge" style="display: none;"></span>' +
                '<div style="font-size: 24px; margin-bottom: 8px;">' + step.icon + '</div>' +
                '<div style="font-weight: 600; margin-bottom: 4px;">步骤 ' + step.id + '</div>' +
                '<div style="font-size: 12px; color: var(--vscode-descriptionForeground);">' + step.name + '</div>' +
                '<div class="error-message" style="display: none;"></div>' +
                '<div class="result-toggle" data-action="toggleResult" data-step="' + step.id + '" style="display: none;">查看结果</div>' +
                '</div>'
            ).join('');
            console.log('[WebView] 已生成', workflowSteps.length, '个工作流步骤');
            
            // 初始化时检查MCP状态
            setTimeout(() => {
                window.checkMcpStatus();
            }, 500);
        }
        window.runWorkflowStep = function(step) {
            const stepEl = document.querySelector('[data-step="' + step + '"]');
            if (stepEl) {
                stepEl.classList.remove('completed', 'error');
                stepEl.classList.add('running');
                const badge = stepEl.querySelector('.status-badge');
                if (badge) {
                    badge.textContent = '运行中';
                    badge.style.display = 'block';
                }
            }
            vscode.postMessage({ command: 'workflow.runStep', step, params: {} });
        }
        
        window.toggleWorkflowResult = function(step) {
            const resultId = 'workflow-result-' + step;
            let resultEl = document.getElementById(resultId);
            
            if (!resultEl) {
                // 创建结果容器
                resultEl = document.createElement('div');
                resultEl.id = resultId;
                resultEl.className = 'workflow-result';
                resultEl.innerHTML = '<div class="workflow-result-header">' +
                    '<div class="workflow-result-title">步骤 ' + step + ' 执行结果</div>' +
                    '<span class="workflow-result-close" data-action="closeResult" data-step="' + step + '">×</span>' +
                    '</div>' +
                    '<div class="workflow-result-content" id="workflow-result-content-' + step + '">加载中...</div>';
                document.getElementById('workflow-results-container').appendChild(resultEl);
            }
            
            // 切换显示
            resultEl.classList.toggle('show');
            
            // 如果显示且内容为空，请求结果
            if (resultEl.classList.contains('show') && resultEl.querySelector('.workflow-result-content').textContent === '加载中...') {
                vscode.postMessage({ command: 'workflow.getResult', step: step });
            }
        }
        
        window.closeWorkflowResult = function(step) {
            const resultEl = document.getElementById('workflow-result-' + step);
            if (resultEl) {
                resultEl.classList.remove('show');
            }
        }
        
        window.runAllWorkflowSteps = function() {
            showConfirm('确认执行', '确定要一键执行全部9个步骤吗？这可能需要几分钟时间。', () => {
                vscode.postMessage({ command: 'workflow.runAll' });
            });
        }
        
        window.resetWorkflow = function() {
            showConfirm('确认重置', '确定要重置工作流吗？所有进度将被清除。', () => {
                vscode.postMessage({ command: 'workflow.reset' });
                // 重置UI状态
                document.querySelectorAll('.workflow-step').forEach(el => {
                    el.classList.remove('running', 'completed');
                });
            });
        }
        
        // === 十倍股功能 ===
        window.refreshTenbaggerData = function() {
            document.getElementById('tenbagger-list').innerHTML = '<div class="loading">正在从缓存数据库加载...</div>';
            vscode.postMessage({ command: 'tenbagger.getRanking', limit: 50, minScore: 40 });
            vscode.postMessage({ command: 'tenbagger.getStats' });
            vscode.postMessage({ command: 'tenbagger.getStages' });
        }
        
        window.jqdataScan = function() {
            const minMarketCap = parseFloat(document.getElementById('min-market-cap')?.value) || 20;
            const maxMarketCap = parseFloat(document.getElementById('max-market-cap')?.value) || 300;
            const minRoe = parseFloat(document.getElementById('min-roe')?.value) || 8;
            const minRevenueGrowth = parseFloat(document.getElementById('min-revenue-growth')?.value) || 15;
            
            document.getElementById('tenbagger-list').innerHTML = '<div class="loading">正在从JQData获取实时数据并评估...<br><small>这可能需要30秒到1分钟</small></div>';
            vscode.postMessage({ 
                command: 'tenbagger.jqdataScan', 
                filters: {
                    min_market_cap: minMarketCap,
                    max_market_cap: maxMarketCap,
                    min_roe: minRoe,
                    min_revenue_growth: minRevenueGrowth,
                    limit: 30
                }
            });
        }
        
        function refreshPipelineData() {
            showConfirm('确认刷新', '刷新数据将重新爬取和评估，可能需要几分钟时间，是否继续？', () => {
                document.getElementById('tenbagger-list').innerHTML = '<div class="loading">正在刷新数据...</div>';
                vscode.postMessage({ command: 'tenbagger.refresh' });
            });
        }
        
        function filterByLevel() {
            const level = document.getElementById('level-filter').value;
            if (level) {
                vscode.postMessage({ command: 'tenbagger.filter', minLevel: level });
            } else {
                renderTenbaggerList(tenbaggerData);
            }
        }
        
        function searchStock() {
            const keyword = document.getElementById('stock-search').value.toLowerCase();
            if (!keyword) {
                renderTenbaggerList(tenbaggerData);
                return;
            }
            const filtered = tenbaggerData.filter(s => 
                (s.symbol && s.symbol.toLowerCase().includes(keyword)) || 
                (s.name && s.name.toLowerCase().includes(keyword))
            );
            renderTenbaggerList(filtered);
        }
        
        function renderTenbaggerList(data, source) {
            const container = document.getElementById('tenbagger-list');
            if (!data || data.length === 0) {
                container.innerHTML = '<div class="loading" style="color:var(--vscode-descriptionForeground);">暂无数据<br><small style="font-size:11px;">点击"刷新数据"从数据库加载</small></div>';
                return;
            }
            // 数据来源标识
            const sourceLabel = source === 'mongodb' ? '📊 数据库' : source === 'mock' ? '📝 模拟' : '📁 缓存';
            let html = '<div style="font-size:11px;color:var(--vscode-descriptionForeground);padding:6px 10px;background:var(--vscode-editor-background);border-radius:4px;margin-bottom:8px;display:flex;justify-content:space-between;">' +
                '<span>' + sourceLabel + '</span><span>共 ' + data.length + ' 只</span></div>';
            
            html += data.map((s, i) => {
                const code = s.symbol || s.security_id || '';
                const name = s.name || code;
                const grade = s.eval_level || s.level || s.grade || 'C';
                const score = s.total_score || s.score || 0;
                const stage = s.current_stage || s.stage || '';
                const levelClass = grade.includes('S') ? 's' : grade.toLowerCase();
                
                return '<div class="tenbagger-item level-' + levelClass + '" data-symbol="' + code + '" onclick="selectStock(\\'' + code + '\\', \\'' + name.replace(/'/g, '') + '\\')">' +
                '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                '<span style="font-weight:600;">' + (i+1) + '. ' + name + '</span>' +
                '<span class="detail-level level-' + levelClass + '" style="font-size:11px;padding:2px 8px;border-radius:4px;">' + grade + '</span>' +
                '</div>' +
                '<div style="display:flex; justify-content:space-between; font-size:11px; margin-top:6px; color:var(--vscode-descriptionForeground);">' +
                '<span>' + code + (stage ? ' <span class="timeline-badge ' + stage.toLowerCase() + '" style="font-size:10px;padding:1px 4px;">' + stage + '</span>' : '') + '</span>' +
                '<span style="font-weight:500;color:var(--vscode-textLink-foreground);">' + score.toFixed(1) + '分</span>' +
                '</div>' +
                '</div>';
            }).join('');
            container.innerHTML = html;
        }
        
        function renderStageStats(counts) {
            // 更新阶段分析面板中的统计
            const items = document.querySelectorAll('.timeline-item');
            items.forEach(item => {
                const stage = Array.from(item.classList).find(c => c.startsWith('s'))?.toUpperCase();
                if (stage && counts[stage] !== undefined) {
                    const badge = item.querySelector('.timeline-badge');
                    if (badge) badge.textContent = stage + ' (' + counts[stage] + ')';
                }
            });
        }
        
        function renderJQDataList(stocks, filters, date) {
            const container = document.getElementById('tenbagger-list');
            if (!stocks || stocks.length === 0) {
                container.innerHTML = '<div class="loading" style="color:var(--vscode-descriptionForeground);">未找到符合条件的股票</div>';
                return;
            }
            
            // 筛选条件摘要
            let filterInfo = '';
            if (filters) {
                filterInfo = '市值: ' + (filters.market_cap || '-') + ' | ROE≥' + (filters.min_roe || '-') + ' | 营收增≥' + (filters.min_revenue_growth || '-');
            }
            
            let html = '<div style="font-size:11px;color:var(--vscode-descriptionForeground);padding:8px 10px;background:var(--vscode-editor-background);border-radius:4px;margin-bottom:8px;">' +
                '<div style="display:flex;justify-content:space-between;">' +
                '<span>📊 <strong>JQData实时数据</strong> | ' + date + '</span>' +
                '<span>共 ' + stocks.length + ' 只</span>' +
                '</div>' +
                (filterInfo ? '<div style="margin-top:4px;font-size:10px;">' + filterInfo + '</div>' : '') +
                '</div>';
            
            html += stocks.map((s, i) => {
                const levelClass = (s.level || '').includes('S') ? 's' : (s.level || '').toLowerCase();
                return '<div class="tenbagger-item level-' + levelClass + '" data-symbol="' + s.symbol + '" onclick="selectStock(\\'' + s.symbol + '\\', \\'' + (s.name || '').replace(/'/g, '') + '\\')">' +
                '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                '<span style="font-weight:600;">' + (i+1) + '. ' + (s.name || s.symbol) + '</span>' +
                '<span class="detail-level level-' + levelClass + '" style="font-size:11px;padding:2px 8px;border-radius:4px;">' + (s.level || '-') + '</span>' +
                '</div>' +
                '<div style="display:flex; justify-content:space-between; font-size:11px; margin-top:4px; color:var(--vscode-descriptionForeground);">' +
                '<span>' + s.symbol + '</span>' +
                '<span style="font-weight:500;color:var(--vscode-textLink-foreground);">' + (s.score || 0).toFixed(1) + '分</span>' +
                '</div>' +
                '<div style="display:flex; gap:12px; font-size:10px; margin-top:4px; color:var(--vscode-descriptionForeground);">' +
                '<span>市值:' + (s.market_cap || 0).toFixed(0) + '亿</span>' +
                '<span>ROE:' + (s.roe || 0).toFixed(1) + '%</span>' +
                '<span class="' + ((s.revenue_growth || 0) > 0 ? 'positive' : 'negative') + '">营收:' + (s.revenue_growth > 0 ? '+' : '') + (s.revenue_growth || 0).toFixed(1) + '%</span>' +
                '<span class="' + ((s.profit_growth || 0) > 0 ? 'positive' : 'negative') + '">利润:' + (s.profit_growth > 0 ? '+' : '') + (s.profit_growth || 0).toFixed(1) + '%</span>' +
                '</div>' +
                '</div>';
            }).join('');
            container.innerHTML = html;
        }
        
        // === 提示和确认对话框工具函数 ===
        function showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = 'toast ' + type;
            toast.textContent = message;
            document.body.appendChild(toast);
            setTimeout(() => {
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }
        
        function showConfirm(title, message, onConfirm) {
            const dialog = document.createElement('div');
            dialog.className = 'confirm-dialog';
            dialog.innerHTML = '<div class="confirm-content">' +
                '<div class="confirm-title">' + title + '</div>' +
                '<div class="confirm-message">' + message + '</div>' +
                '<div class="confirm-buttons">' +
                '<button class="confirm-btn secondary" data-action="cancel">取消</button>' +
                '<button class="confirm-btn primary" data-action="confirm">确定</button>' +
                '</div></div>';
            document.body.appendChild(dialog);
            
            dialog.querySelector('[data-action="confirm"]').addEventListener('click', () => {
                dialog.remove();
                if (onConfirm) onConfirm();
            });
            dialog.querySelector('[data-action="cancel"]').addEventListener('click', () => {
                dialog.remove();
            });
            dialog.addEventListener('click', (e) => {
                if (e.target === dialog) dialog.remove();
            });
        }
        
        // === AKShare实时数据功能 (挂载到window以便onclick调用) ===
        window.loadHotIndustries = function() {
            console.log('[WebView] loadHotIndustries called');
            try {
                const container = document.getElementById('realtime-data');
                if (!container) {
                    console.error('[WebView] realtime-data element not found!');
                    showToast('❌ 错误: realtime-data元素不存在', 'error');
                    return;
                }
                container.innerHTML = '<div style="text-align:center;padding:20px;color:var(--vscode-descriptionForeground);">正在加载热门行业数据...<br><small>首次加载可能需要30-60秒</small></div>';
                console.log('[WebView] Sending message: akshare.hot');
                vscode.postMessage({ command: 'akshare.hot', category: 'industry', limit: 10 });
                console.log('[WebView] Message sent');
            } catch (e) {
                console.error('[WebView] Error in loadHotIndustries:', e);
                showToast('❌ 错误: ' + e.message, 'error');
            }
        };
        
        window.loadHotConcepts = function() {
            console.log('[WebView] loadHotConcepts called');
            try {
                const container = document.getElementById('realtime-data');
                if (!container) {
                    console.error('[WebView] realtime-data element not found!');
                    return;
                }
                container.innerHTML = '<div style="text-align:center;padding:20px;color:var(--vscode-descriptionForeground);">正在加载热门概念数据...</div>';
                vscode.postMessage({ command: 'akshare.hot', category: 'concept', limit: 10 });
            } catch (e) {
                console.error('[WebView] Error in loadHotConcepts:', e);
            }
        };
        
        window.loadTopGainers = function() {
            console.log('[WebView] loadTopGainers called');
            try {
                const container = document.getElementById('realtime-data');
                if (!container) {
                    console.error('[WebView] realtime-data element not found!');
                    return;
                }
                container.innerHTML = '<div style="text-align:center;padding:20px;color:var(--vscode-descriptionForeground);">正在加载涨幅榜...<br><small>首次加载可能需要30-60秒</small></div>';
                vscode.postMessage({ command: 'akshare.spot', sortBy: 'change', limit: 15 });
            } catch (e) {
                console.error('[WebView] Error in loadTopGainers:', e);
            }
        };
        
        window.loadTopVolume = function() {
            console.log('[WebView] loadTopVolume called');
            try {
                const container = document.getElementById('realtime-data');
                if (!container) {
                    console.error('[WebView] realtime-data element not found!');
                    return;
                }
                container.innerHTML = '<div style="text-align:center;padding:20px;color:var(--vscode-descriptionForeground);">正在加载成交榜...<br><small>首次加载可能需要30-60秒</small></div>';
                vscode.postMessage({ command: 'akshare.spot', sortBy: 'amount', limit: 15 });
            } catch (e) {
                console.error('[WebView] Error in loadTopVolume:', e);
            }
        };
        
        // 测试按钮点击功能
        window.testButtonClick = function() {
            const debugDiv = document.getElementById('debug-info');
            const debugContent = document.getElementById('debug-content');
            
            const checks = {
                '函数存在': {
                    'loadHotIndustries': typeof window.loadHotIndustries,
                    'loadHotConcepts': typeof window.loadHotConcepts,
                    'loadTopGainers': typeof window.loadTopGainers,
                    'loadTopVolume': typeof window.loadTopVolume,
                    'vscode对象': typeof vscode,
                    'vscode.postMessage': typeof vscode?.postMessage
                },
                'DOM元素': {
                    'realtime-data': !!document.getElementById('realtime-data'),
                    'debug-info': !!debugDiv
                }
            };
            
            let html = '';
            for (const [category, items] of Object.entries(checks)) {
                html += '<div style="margin-top:4px;"><strong>' + category + ':</strong><br>';
                for (const [name, value] of Object.entries(items)) {
                    const status = value ? '✅' : '❌';
                    const color = value ? 'green' : 'red';
                    html += '<span style="color:' + color + ';">' + status + ' ' + name + ': ' + String(value) + '</span><br>';
                }
                html += '</div>';
            }
            
            if (debugContent) {
                debugContent.innerHTML = html;
            }
            
            if (debugDiv) {
                debugDiv.style.display = 'block';
            }
            
            // 尝试调用一个函数
            try {
                if (typeof window.loadHotIndustries === 'function') {
                    showToast('✅ 测试成功！函数存在且可调用。现在点击"🔥 热门行业"按钮应该可以工作。', 'success');
                } else {
                    showToast('❌ 测试失败！函数不存在。请查看调试信息。', 'error');
                }
            } catch (e) {
                showToast('❌ 测试出错: ' + e.message, 'error');
            }
        };
        
        // 验证函数是否挂载成功
        console.log('[WebView] Function check:', {
            loadHotIndustries: typeof window.loadHotIndustries,
            loadHotConcepts: typeof window.loadHotConcepts,
            loadTopGainers: typeof window.loadTopGainers,
            loadTopVolume: typeof window.loadTopVolume
        });
        
        function renderHotData(items, category) {
            const container = document.getElementById('realtime-data');
            if (!items || items.length === 0) {
                container.innerHTML = '<div style="text-align:center;padding:20px;color:var(--vscode-descriptionForeground);">无数据</div>';
                return;
            }
            
            const title = category === 'industry' ? '🔥 热门行业板块' : '💡 热门概念板块';
            let html = '<div style="font-weight:600;margin-bottom:8px;font-size:13px;">' + title + '</div>';
            html += '<table class="factor-table" style="font-size:11px;"><thead><tr><th style="text-align:left;">板块</th><th>涨跌幅</th><th>领涨股</th><th>涨幅</th></tr></thead><tbody>';
            
            items.forEach((item, i) => {
                const changeClass = item.change >= 0 ? 'positive' : 'negative';
                const leaderClass = item.leader_change >= 0 ? 'positive' : 'negative';
                html += '<tr>' +
                    '<td style="text-align:left;font-weight:500;">' + (i+1) + '. ' + item.name + '</td>' +
                    '<td class="' + changeClass + '">' + (item.change >= 0 ? '+' : '') + item.change.toFixed(2) + '%</td>' +
                    '<td style="text-align:left;">' + (item.leader || '-') + '</td>' +
                    '<td class="' + leaderClass + '">' + (item.leader_change >= 0 ? '+' : '') + (item.leader_change || 0).toFixed(2) + '%</td>' +
                    '</tr>';
            });
            
            html += '</tbody></table>';
            html += '<div style="font-size:10px;color:var(--vscode-descriptionForeground);margin-top:8px;text-align:right;">数据来源: AKShare (东方财富)</div>';
            container.innerHTML = html;
        }
        
        function renderSpotData(stocks, sortBy) {
            const container = document.getElementById('realtime-data');
            if (!stocks || stocks.length === 0) {
                container.innerHTML = '<div style="text-align:center;padding:20px;color:var(--vscode-descriptionForeground);">无数据</div>';
                return;
            }
            
            const title = sortBy === 'change' ? '📈 今日涨幅榜' : '📊 今日成交榜';
            let html = '<div style="font-weight:600;margin-bottom:8px;font-size:13px;">' + title + '</div>';
            html += '<table class="factor-table" style="font-size:11px;"><thead><tr><th style="text-align:left;">股票</th><th>价格</th><th>涨跌幅</th><th>' + (sortBy === 'amount' ? '成交额' : '换手率') + '</th><th>市值</th></tr></thead><tbody>';
            
            stocks.forEach((s, i) => {
                const changeClass = s.change >= 0 ? 'positive' : 'negative';
                const extra = sortBy === 'amount' ? s.amount.toFixed(2) + '亿' : s.turnover.toFixed(2) + '%';
                html += '<tr onclick="selectStock(\\'' + s.symbol + '\\', \\'' + (s.name || '').replace(/'/g, '') + '\\')" style="cursor:pointer;">' +
                    '<td style="text-align:left;font-weight:500;">' + (i+1) + '. ' + s.name + '</td>' +
                    '<td>' + s.price.toFixed(2) + '</td>' +
                    '<td class="' + changeClass + '">' + (s.change >= 0 ? '+' : '') + s.change.toFixed(2) + '%</td>' +
                    '<td>' + extra + '</td>' +
                    '<td>' + s.market_cap.toFixed(0) + '亿</td>' +
                    '</tr>';
            });
            
            html += '</tbody></table>';
            html += '<div style="font-size:10px;color:var(--vscode-descriptionForeground);margin-top:8px;text-align:right;">数据来源: AKShare (东方财富)</div>';
            container.innerHTML = html;
        }
        
        function renderJQDataDetail(data) {
            const container = document.getElementById('stock-detail');
            if (!data || !data.symbol) {
                container.innerHTML = '<div class="loading">无数据</div>';
                return;
            }
            
            const fin = data.financials || {};
            const val = data.valuation || {};
            const tech = data.technicals || {};
            const eva = data.evaluation || {};
            
            container.innerHTML = '<div style="padding:12px;">' +
                '<h3 style="margin:0 0 12px 0;font-size:16px;">' + (data.name || data.symbol) + ' <span style="font-size:12px;color:var(--vscode-descriptionForeground);">' + data.symbol + '</span></h3>' +
                
                '<div class="stats-grid" style="grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:16px;">' +
                '<div class="stat-card" style="padding:10px;"><div class="stat-value" style="font-size:20px;">' + (eva.score || 0) + '</div><div class="stat-label">评分</div></div>' +
                '<div class="stat-card" style="padding:10px;"><div class="stat-value" style="font-size:20px;">' + (eva.level || '-') + '</div><div class="stat-label">等级</div></div>' +
                '<div class="stat-card" style="padding:10px;"><div class="stat-value" style="font-size:20px;">' + (eva.stage || 'S0') + '</div><div class="stat-label">阶段</div></div>' +
                '</div>' +
                
                '<h4 style="margin:12px 0 8px 0;font-size:13px;">财务指标</h4>' +
                '<table class="factor-table" style="font-size:12px;">' +
                '<tr><td>ROE</td><td>' + (fin.roe || 0).toFixed(2) + '%</td><td>毛利率</td><td>' + (fin.gross_margin || 0).toFixed(2) + '%</td></tr>' +
                '<tr><td>营收增长</td><td class="' + ((fin.revenue_growth || 0) > 0 ? 'positive' : 'negative') + '">' + (fin.revenue_growth || 0).toFixed(2) + '%</td>' +
                '<td>利润增长</td><td class="' + ((fin.profit_growth || 0) > 0 ? 'positive' : 'negative') + '">' + (fin.profit_growth || 0).toFixed(2) + '%</td></tr>' +
                '</table>' +
                
                '<h4 style="margin:12px 0 8px 0;font-size:13px;">估值指标</h4>' +
                '<table class="factor-table" style="font-size:12px;">' +
                '<tr><td>PE</td><td>' + (val.pe_ratio || 0).toFixed(2) + '</td><td>PB</td><td>' + (val.pb_ratio || 0).toFixed(2) + '</td></tr>' +
                '<tr><td>市值</td><td>' + (val.market_cap || 0).toFixed(2) + '亿</td><td>PS</td><td>' + (val.ps_ratio || 0).toFixed(2) + '</td></tr>' +
                '</table>' +
                
                '<h4 style="margin:12px 0 8px 0;font-size:13px;">技术指标</h4>' +
                '<table class="factor-table" style="font-size:12px;">' +
                '<tr><td>涨跌幅</td><td class="' + ((tech.price_change_pct || 0) > 0 ? 'positive' : 'negative') + '">' + (tech.price_change_pct || 0).toFixed(2) + '%</td>' +
                '<td>量比</td><td>' + (tech.volume_ratio || 1).toFixed(2) + '</td></tr>' +
                '<tr><td>均线趋势</td><td>' + (tech.ma_trend || '-') + '</td><td>相对强度</td><td>' + (tech.relative_strength || 50).toFixed(0) + '</td></tr>' +
                '</table>' +
                
                '<div style="margin-top:12px;font-size:10px;color:var(--vscode-descriptionForeground);">数据来源: JQData | 数据质量: ' + ((data.data_quality || 0) * 100).toFixed(0) + '%</div>' +
                '</div>';
        }
        
        window.selectStock = function(symbol, name) {
            selectedStock = symbol;
            document.querySelectorAll('.tenbagger-item').forEach(el => el.classList.remove('selected'));
            const el = document.querySelector('[data-symbol="' + symbol + '"]');
            if (el) el.classList.add('selected');
            // 获取详情
            vscode.postMessage({ command: 'tenbagger.getReport', symbol });
            document.getElementById('detail-panel').style.display = 'block';
            document.getElementById('stock-detail').innerHTML = '<div class="loading">加载详情...</div>';
            vscode.postMessage({ command: 'tenbagger.getReport', symbol });
        }
        
        window.closeDetail = function() {
            document.getElementById('detail-panel').style.display = 'none';
            selectedStock = null;
            document.querySelectorAll('.tenbagger-item').forEach(el => el.classList.remove('selected'));
        }
        
        function renderStockDetail(report) {
            const r = report || {};
            const dims = r.dimensions || dimensions.map(d => ({ name: d.name, score: Math.random() * 100, weight: d.weight }));
            
            let html = '<div class="detail-header">' +
                '<div class="detail-name">' + (r.name || selectedStock) + '</div>' +
                '<div class="detail-level level-' + (r.eval_level || 'b').toLowerCase() + '">' + (r.eval_level || '-') + '</div>' +
                '</div>' +
                '<div style="font-size:14px; margin-bottom:4px;">代码: ' + (r.symbol || selectedStock) + ' | 阶段: ' + (r.stage || '-') + '</div>' +
                '<div style="font-size:24px; font-weight:700; color:var(--vscode-textLink-foreground); margin:12px 0;">总分: ' + (r.total_score?.toFixed(1) || '-') + '</div>';
            
            // 维度条形图
            html += '<div class="dimension-bars">';
            dims.forEach(d => {
                const score = d.score || 0;
                html += '<div class="dimension-row">' +
                    '<div class="dimension-name">' + d.name + '</div>' +
                    '<div class="dimension-bar-bg"><div class="dimension-bar" style="width:' + score + '%;"></div></div>' +
                    '<div class="dimension-score">' + score.toFixed(0) + '</div>' +
                    '</div>';
            });
            html += '</div>';
            
            // SWOT分析
            html += '<div class="swot-grid">' +
                '<div class="swot-card"><div class="swot-title">✅ 优势</div><ul class="swot-list">' + 
                (r.strengths?.map(s => '<li>' + s + '</li>').join('') || '<li>暂无数据</li>') + '</ul></div>' +
                '<div class="swot-card"><div class="swot-title">⚠️ 劣势</div><ul class="swot-list">' + 
                (r.weaknesses?.map(s => '<li>' + s + '</li>').join('') || '<li>暂无数据</li>') + '</ul></div>' +
                '<div class="swot-card"><div class="swot-title">🚀 催化剂</div><ul class="swot-list">' + 
                (r.catalysts?.map(s => '<li>' + s + '</li>').join('') || '<li>暂无数据</li>') + '</ul></div>' +
                '<div class="swot-card"><div class="swot-title">⛔ 风险</div><ul class="swot-list">' + 
                (r.risks?.map(s => '<li>' + s + '</li>').join('') || '<li>暂无数据</li>') + '</ul></div>' +
                '</div>';
            
            // 投资建议
            if (r.recommendation) {
                html += '<div style="margin-top:16px; padding:12px; background:var(--vscode-inputValidation-infoBackground); border-radius:6px;">' +
                    '<div style="font-weight:600; margin-bottom:6px;">💡 投资建议</div>' +
                    '<div style="font-size:13px;">' + r.recommendation + '</div></div>';
            }
            
            document.getElementById('stock-detail').innerHTML = html;
        }
        
        function updateStats(stats) {
            // 更新概览面板的统计
            const totalEl = document.getElementById('stat-total');
            const sEl = document.getElementById('stat-s');
            const aEl = document.getElementById('stat-a');
            const bEl = document.getElementById('stat-b');
            const avgEl = document.getElementById('stat-avgret');
            const sourceEl = document.getElementById('stat-source');
            
            if (totalEl) totalEl.textContent = stats.total_evaluated || stats.total || 0;
            
            // 等级统计（支持by_grade和by_level两种格式）
            const grades = stats.by_grade || stats.by_level || {};
            if (sEl) sEl.textContent = (grades.A || 0);
            if (aEl) aEl.textContent = (grades.B || 0);
            if (bEl) bEl.textContent = (grades.C || 0);
            
            // 平均分
            if (avgEl) {
                const avg = stats.avg_score || 0;
                avgEl.textContent = avg > 0 ? avg.toFixed(1) : '-';
            }
            
            // 数据来源
            if (sourceEl) {
                sourceEl.textContent = stats.source === 'mongodb' ? 'MongoDB' : stats.source === 'mock' ? '模拟' : '缓存';
                sourceEl.style.fontSize = '14px';
            }
            
            // 阶段统计
            const stages = stats.by_stage || {};
            const s0El = document.getElementById('stage-s0-count');
            const s1El = document.getElementById('stage-s1-count');
            const s2El = document.getElementById('stage-s2-count');
            const s3El = document.getElementById('stage-s3-count');
            if (s0El) s0El.textContent = stages.S0 || 0;
            if (s1El) s1El.textContent = stages.S1 || 0;
            if (s2El) s2El.textContent = stages.S2 || 0;
            if (s3El) s3El.textContent = stages.S3 || 0;
        }
        
        
        // === 策略功能 ===
        window.scanStrategies = function() { vscode.postMessage({ command: 'strategy.scan', params: {} }); };
        window.refreshStrategyList = function() { vscode.postMessage({ command: 'strategy.getList' }); };
        
        // === 消息处理 ===
        window.addEventListener('message', event => {
            const msg = event.data;
            switch (msg.command) {
                case 'workflow.stepResult':
                    const stepEl = document.querySelector('[data-step="' + msg.step + '"]');
                    if (stepEl) {
                        stepEl.classList.remove('running', 'error', 'completed');
                        const badge = stepEl.querySelector('.status-badge');
                        const toggleBtn = stepEl.querySelector('.result-toggle');
                        const errorIndicator = stepEl.querySelector('.error-indicator');
                        const errorMessage = stepEl.querySelector('.error-message');
                        
                        if (msg.success) {
                            stepEl.classList.add('completed');
                            if (badge) {
                                badge.textContent = '✓ 完成';
                                badge.style.display = 'block';
                            }
                            if (errorIndicator) errorIndicator.style.display = 'none';
                            if (errorMessage) errorMessage.style.display = 'none';
                            if (toggleBtn) {
                                toggleBtn.style.display = 'block';
                                toggleBtn.textContent = '📋 查看结果';
                            }
                            // 存储结果
                            if (msg.result) {
                                stepEl.dataset.result = JSON.stringify(msg.result);
                            }
                        } else {
                            stepEl.classList.add('error');
                            if (badge) {
                                badge.textContent = '✗ 失败';
                                badge.style.display = 'block';
                            }
                            if (errorIndicator) errorIndicator.style.display = 'block';
                            
                            // 收集所有错误信息
                            let errorText = msg.error || '未知错误';
                            let errorDetails = msg.details || msg.stack || msg.traceback || '';
                            let errorSummary = '';
                            
                            // 如果 result 中有错误信息，也提取出来
                            if (msg.result) {
                                try {
                                    const result = typeof msg.result === 'string' ? JSON.parse(msg.result) : msg.result;
                                    if (result.error) errorText = result.error;
                                    if (result.error_details) {
                                        errorDetails = Array.isArray(result.error_details) 
                                            ? result.error_details.join('\n') 
                                            : String(result.error_details);
                                    }
                                    if (result.error_summary) errorSummary = result.error_summary;
                                    if (result.hint) errorDetails += '\n\n建议: ' + result.hint;
                                } catch (e) {
                                    // 解析失败，使用原始数据
                                }
                            }
                            
                            // 构建完整错误信息
                            let fullError = errorText;
                            if (errorSummary) {
                                fullError += '\n\n错误摘要:\n' + errorSummary;
                            }
                            if (errorDetails) {
                                fullError += '\n\n详细信息:\n' + errorDetails.substring(0, 2000); // 限制长度
                            }
                            
                            // 显示简短错误（UI中）
                            const shortError = errorText.length > 80 ? errorText.substring(0, 80) + '...' : errorText;
                            if (errorMessage) {
                                errorMessage.textContent = shortError;
                                errorMessage.style.display = 'block';
                                errorMessage.title = fullError; // 鼠标悬停显示完整错误
                            }
                            
                            // 存储完整错误信息
                            stepEl.dataset.error = fullError;
                            stepEl.dataset.errorShort = shortError;
                            
                            if (toggleBtn) {
                                toggleBtn.style.display = 'block';
                                toggleBtn.textContent = '🔍 查看详情';
                            }
                            
                            // 显示全局错误面板（对于数据源检查步骤，特别重要）
                            const stepName = workflowSteps.find(s => s.id === parseInt(msg.step))?.name || '步骤 ' + msg.step;
                            window.showErrorPanel(
                                '步骤 ' + msg.step + ' 执行失败: ' + stepName,
                                errorText,
                                (errorSummary ? errorSummary + '\n\n' : '') + errorDetails
                            );
                        }
                    }
                    break;
                case 'workflow.allCompleted':
                    if (msg.success) {
                        showToast('✅ 所有步骤执行完成！', 'success');
                        // 标记所有步骤为完成
                        document.querySelectorAll('.workflow-step').forEach((el, i) => {
                            el.classList.remove('running', 'error');
                            el.classList.add('completed');
                            const badge = el.querySelector('.status-badge');
                            const toggleBtn = el.querySelector('.result-toggle');
                            if (badge) {
                                badge.textContent = '完成';
                                badge.style.display = 'block';
                            }
                            if (toggleBtn) {
                                toggleBtn.style.display = 'block';
                            }
                        });
                    } else {
                        showToast('❌ 一键执行失败: ' + (msg.error || '未知错误'), 'error');
                    }
                    break;
                case 'workflow.reset':
                    // 重置所有步骤状态
                    document.querySelectorAll('.workflow-step').forEach(el => {
                        el.classList.remove('running', 'completed', 'error');
                        const badge = el.querySelector('.status-badge');
                        const toggleBtn = el.querySelector('.result-toggle');
                        if (badge) badge.style.display = 'none';
                        if (toggleBtn) toggleBtn.style.display = 'none';
                        delete el.dataset.result;
                        delete el.dataset.error;
                    });
                    // 清除所有结果
                    document.getElementById('workflow-results-container').innerHTML = '';
                    break;
                case 'workflow.result':
                    // 显示步骤结果
                    const resultContentEl = document.getElementById('workflow-result-content-' + msg.step);
                    if (resultContentEl) {
                        if (msg.success && msg.result) {
                            resultContentEl.innerHTML = formatWorkflowResult(msg.step, msg.result);
                        } else {
                            resultContentEl.innerHTML = '<div style="color: var(--vscode-errorForeground);">❌ 获取结果失败: ' + (msg.error || '未知错误') + '</div>';
                        }
                    }
                    break;
                case 'tenbagger.rankingResult':
                case 'tenbagger.filterResult':
                    const stocks = msg.rankings || msg.stocks || [];
                    if (msg.command === 'tenbagger.rankingResult') tenbaggerData = stocks;
                    renderTenbaggerList(stocks, msg.source);
                    break;
                case 'tenbagger.statsResult':
                    updateStats(msg.stats || {});
                    break;
                case 'tenbagger.stagesResult':
                    renderStageStats(msg.counts || {});
                    break;
                case 'tenbagger.refreshResult':
                    if (msg.success) {
                        const r = msg.result || {};
                        showToast('✅ 数据刷新完成！爬取: ' + (r.crawled || 0) + ', 存储: ' + (r.stored || 0) + ', 评估: ' + (r.tenbagger_evaluated || 0), 'success');
                    } else {
                        showToast('❌ 数据刷新失败: ' + (msg.error || '未知错误'), 'error');
                    }
                    break;
                case 'tenbagger.jqdataScanResult':
                    if (msg.success) {
                        tenbaggerData = msg.stocks || [];
                        renderJQDataList(msg.stocks, msg.filters, msg.date);
                    } else {
                        document.getElementById('tenbagger-list').innerHTML = '<div class="error" style="padding:20px;text-align:center;"><div style="font-size:16px;margin-bottom:8px;">❌ JQData扫描失败</div><div style="font-size:12px;color:var(--vscode-descriptionForeground);">' + (msg.error || '未知错误') + '</div></div>';
                    }
                    break;
                case 'tenbagger.jqdataStockResult':
                    if (msg.success) {
                        renderJQDataDetail(msg.data);
                    }
                    break;
                // AKShare结果
                case 'akshare.hotResult':
                    if (msg.success) {
                        renderHotData(msg.items, msg.category);
                    } else {
                        document.getElementById('realtime-data').innerHTML = '<div style="text-align:center;padding:20px;color:var(--vscode-errorForeground);">❌ 加载失败: ' + (msg.error || '未知错误') + '</div>';
                    }
                    break;
                case 'akshare.spotResult':
                    if (msg.success) {
                        renderSpotData(msg.stocks, msg.sortBy);
                    } else {
                        document.getElementById('realtime-data').innerHTML = '<div style="text-align:center;padding:20px;color:var(--vscode-errorForeground);">❌ 加载失败: ' + (msg.error || '未知错误') + '</div>';
                    }
                    break;
                case 'tenbagger.reportResult':
                    renderStockDetail(msg.report || {});
                    break;
                case 'strategy.listResult':
                case 'strategy.scanResult':
                    const strategies = msg.strategies || [];
                    const content = document.getElementById('strategy-content');
                    if (strategies.length === 0) {
                        content.innerHTML = '<div class="error">暂无策略</div>';
                    } else {
                        content.innerHTML = '<div class="strategy-list">' + strategies.map(s =>
                            '<div class="strategy-item"><div style="font-weight: 600;">' + (s.name || '未命名策略') + '</div>' +
                            '<div style="font-size: 12px; margin-top: 8px;">' + (s.description || '无描述') + '</div></div>'
                        ).join('') + '</div>';
                    }
                    break;
                    
                // MCP状态更新
                case 'mcp.statusResult':
                    const status = msg.status || {};
                    updateMcpStatusUI(
                        status.workflow?.ok ? 'connected' : 'disconnected',
                        'workflow',
                        status.workflow?.ok ? '✓ 工作流' : '✗ 工作流'
                    );
                    updateMcpStatusUI(
                        status.datasource?.ok ? 'connected' : 'disconnected',
                        'datasource',
                        status.datasource?.ok ? '✓ 数据源' : '✗ 数据源'
                    );
                    updateMcpStatusUI(
                        status.tenbagger?.ok ? 'connected' : 'disconnected',
                        'tenbagger',
                        status.tenbagger?.ok ? '✓ 十倍股' : '✗ 十倍股'
                    );
                    // 更新总图标
                    const allOk = status.workflow?.ok && status.datasource?.ok && status.tenbagger?.ok;
                    const iconEl = document.getElementById('mcp-status-icon');
                    if (iconEl) {
                        iconEl.className = 'mcp-status-icon ' + (allOk ? 'connected' : 'disconnected');
                    }
                    break;
                    
                // 全局错误显示
                case 'error':
                    window.showErrorPanel('系统错误', msg.error || '未知错误', msg.details || '');
                    break;
                    
                // 错误搜索结果
                case 'error.searchResult':
                    if (msg.success && msg.solutions && msg.solutions.length > 0) {
                        let solutionHtml = '<div style="margin-top:12px;"><strong>🔍 找到的解决方案:</strong><ul style="margin:8px 0;padding-left:20px;">';
                        msg.solutions.forEach(s => {
                            solutionHtml += '<li style="margin:4px 0;">' + s + '</li>';
                        });
                        solutionHtml += '</ul></div>';
                        const detailsEl = document.getElementById('error-panel-details');
                        if (detailsEl) {
                            detailsEl.innerHTML += solutionHtml;
                        }
                    } else {
                        showToast('未找到相关解决方案，建议在知识库中记录此问题。', 'info');
                    }
                    break;
            }
        });
        
        // initWorkflowSteps() 现在在 initializeAll() 中调用
    </script>
</body>
</html>`;
    }

    private _getNonce(): string {
        let text = '';
        const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        for (let i = 0; i < 32; i++) text += possible.charAt(Math.floor(Math.random() * possible.length));
        return text;
    }

    public dispose(): void {
        UnifiedDashboard.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }
}
