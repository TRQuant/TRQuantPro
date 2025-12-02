/**
 * TRQuant Client
 * 与Python后端通信的客户端
 * 
 * 支持两种通信方式：
 * 1. 子进程 + JSON over stdio（本地开发）
 * 2. HTTP API（服务器部署）
 */

import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';
import axios from 'axios';

export interface TRQuantResponse<T = any> {
    ok: boolean;
    data?: T;
    error?: string;
}

export interface MarketStatus {
    regime: string;
    index_trend: Record<string, { zscore: number; trend: string }>;
    style_rotation: Array<{ style: string; score: number }>;
    summary: string;
}

export interface Mainline {
    name: string;
    score: number;
    industries: string[];
    logic: string;
}

export interface Factor {
    name: string;
    category: string;
    weight: number;
    reason: string;
}

export interface Strategy {
    code: string;
    name: string;
    description: string;
    factors: string[];
    risk_params: Record<string, any>;
}

export class TRQuantClient {
    private context: vscode.ExtensionContext;
    private bridgeProcess: cp.ChildProcess | null = null;
    private useHttp: boolean = false;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.initClient();
    }

    private initClient() {
        const config = vscode.workspace.getConfiguration('trquant');
        // 检查是否有HTTP服务可用，否则使用子进程
        this.useHttp = false; // 默认使用子进程模式
    }

    /**
     * 获取市场状态
     */
    async getMarketStatus(params?: {
        universe?: string;
        as_of?: string;
    }): Promise<TRQuantResponse<MarketStatus>> {
        return this.callBridge('get_market_status', params || {});
    }

    /**
     * 获取投资主线
     */
    async getMainlines(params?: {
        top_n?: number;
        time_horizon?: string;
    }): Promise<TRQuantResponse<Mainline[]>> {
        return this.callBridge('get_mainlines', {
            top_n: params?.top_n || 20,
            time_horizon: params?.time_horizon || 'short'
        });
    }

    /**
     * 推荐因子
     */
    async recommendFactors(params?: {
        market_regime?: string;
        mainlines?: string[];
    }): Promise<TRQuantResponse<Factor[]>> {
        return this.callBridge('recommend_factors', params || {});
    }

    /**
     * 生成策略代码
     */
    async generateStrategy(params: {
        factors: string[];
        style?: string;
        risk_params?: Record<string, any>;
    }): Promise<TRQuantResponse<Strategy>> {
        return this.callBridge('generate_strategy', params);
    }

    /**
     * 分析回测结果
     */
    async analyzeBacktest(params: {
        backtest_file?: string;
        backtest_data?: any;
    }): Promise<TRQuantResponse<any>> {
        return this.callBridge('analyze_backtest', params);
    }

    /**
     * 风险评估
     */
    async assessRisk(params: {
        portfolio: any;
    }): Promise<TRQuantResponse<any>> {
        return this.callBridge('risk_assessment', params);
    }

    /**
     * 调用Python Bridge
     */
    private async callBridge(action: string, params: any): Promise<TRQuantResponse> {
        if (this.useHttp) {
            return this.callHttp(action, params);
        } else {
            return this.callSubprocess(action, params);
        }
    }

    /**
     * 通过HTTP调用
     */
    private async callHttp(action: string, params: any): Promise<TRQuantResponse> {
        const config = vscode.workspace.getConfiguration('trquant');
        const host = config.get<string>('serverHost') || '127.0.0.1';
        const port = config.get<number>('serverPort') || 5000;

        try {
            const response = await axios.post(
                `http://${host}:${port}/api/${action}`,
                params,
                { timeout: 30000 }
            );
            return response.data;
        } catch (error: any) {
            return {
                ok: false,
                error: error.message || 'HTTP请求失败'
            };
        }
    }

    /**
     * 通过子进程调用
     */
    private async callSubprocess(action: string, params: any): Promise<TRQuantResponse> {
        return new Promise((resolve) => {
            const config = vscode.workspace.getConfiguration('trquant');
            const pythonPath = config.get<string>('pythonPath') || 'python';
            
            // 获取bridge.py路径
            const extensionPath = this.context.extensionPath;
            const bridgePath = path.join(extensionPath, 'python', 'bridge.py');

            const request = JSON.stringify({
                action,
                params
            });

            try {
                const process = cp.spawn(pythonPath, [bridgePath], {
                    cwd: path.dirname(extensionPath),
                    env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
                });

                let stdout = '';
                let stderr = '';

                process.stdout?.on('data', (data) => {
                    stdout += data.toString();
                });

                process.stderr?.on('data', (data) => {
                    stderr += data.toString();
                });

                process.on('close', (code) => {
                    if (code !== 0) {
                        resolve({
                            ok: false,
                            error: stderr || `进程退出码: ${code}`
                        });
                        return;
                    }

                    try {
                        const response = JSON.parse(stdout);
                        resolve(response);
                    } catch (e) {
                        resolve({
                            ok: false,
                            error: `解析响应失败: ${stdout}`
                        });
                    }
                });

                process.on('error', (error) => {
                    resolve({
                        ok: false,
                        error: `启动进程失败: ${error.message}`
                    });
                });

                // 发送请求
                process.stdin?.write(request);
                process.stdin?.end();

                // 超时处理
                setTimeout(() => {
                    process.kill();
                    resolve({
                        ok: false,
                        error: '请求超时'
                    });
                }, 60000);

            } catch (error: any) {
                resolve({
                    ok: false,
                    error: error.message
                });
            }
        });
    }

    dispose() {
        if (this.bridgeProcess) {
            this.bridgeProcess.kill();
        }
    }
}

