/**
 * 十倍股服务适配器（TypeScript）
 * 
 * 连接GUI和MCP服务，实现版本路由和格式转换。
 * 
 * Author: TRQuant Team
 * Date: 2025-12-21
 */

import { getWebviewMCPClient } from '../services/webviewMCPClient';

// 使用ReturnType获取类型
type WebviewMCPClient = ReturnType<typeof getWebviewMCPClient>;

export interface TenbaggerRequest {
    symbol: string;
    name?: string;
    data?: Record<string, any>;
    version?: string;
}

export interface TenbaggerResponse {
    success: boolean;
    report?: any;
    error?: string;
    version?: string;
}

export interface TenbaggerRankingRequest {
    top_n?: number;
    min_level?: string;
    version?: string;
}

export class TenbaggerAdapter {
    private mcpClient: WebviewMCPClient;
    private defaultVersion: string = "v2";
    
    constructor(mcpClient: WebviewMCPClient) {
        this.mcpClient = mcpClient;
    }
    
    /**
     * 评估单个股票
     */
    async evaluate(request: TenbaggerRequest): Promise<TenbaggerResponse> {
        const version = request.version || this.defaultVersion;
        const toolName = `tenbagger_v2.evaluate`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                symbol: request.symbol,
                name: request.name,
                data: request.data || {},
                version: version
            }) as any;
            
            return {
                success: result.success || false,
                report: result.report || result.result,
                error: result.error,
                version: result.version || version
            };
        } catch (error: any) {
            return {
                success: false,
                error: error.message || String(error),
                version: version
            };
        }
    }
    
    /**
     * 批量评估股票
     */
    async batchEvaluate(request: {
        symbols: string[];
        max_count?: number;
        version?: string;
    }): Promise<TenbaggerResponse> {
        const version = request.version || this.defaultVersion;
        const toolName = `tenbagger_v2.batch`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                symbols: request.symbols,
                max_count: request.max_count,
                version: version
            }) as any;
            
            return {
                success: result.success || false,
                report: result.results || result.report,
                error: result.error,
                version: result.version || version
            };
        } catch (error: any) {
            return {
                success: false,
                error: error.message || String(error),
                version: version
            };
        }
    }
    
    /**
     * 获取股票报告
     */
    async getReport(symbol: string, version?: string): Promise<TenbaggerResponse> {
        const v = version || this.defaultVersion;
        const toolName = `tenbagger_v2.report`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                symbol: symbol,
                version: v
            }) as any;
            
            return {
                success: result.success || false,
                report: result.report || result.result,
                error: result.error,
                version: result.version || v
            };
        } catch (error: any) {
            return {
                success: false,
                error: error.message || String(error),
                version: v
            };
        }
    }
    
    /**
     * 获取排名
     */
    async getRankings(request: TenbaggerRankingRequest): Promise<TenbaggerResponse> {
        const version = request.version || this.defaultVersion;
        const toolName = `tenbagger_v2.recommendations`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                top_n: request.top_n || 20,
                min_level: request.min_level || "A",
                version: version
            }) as any;
            
            return {
                success: result.success || false,
                report: result.recommendations || result.rankings || result.result,
                error: result.error,
                version: result.version || version
            };
        } catch (error: any) {
            return {
                success: false,
                error: error.message || String(error),
                version: version
            };
        }
    }
    
    /**
     * 生成报告
     */
    async generateReport(
        format: string = "markdown",
        minLevel: string = "A",
        outputPath?: string,
        version?: string
    ): Promise<TenbaggerResponse> {
        const v = version || this.defaultVersion;
        const toolName = `tenbagger_v2.generate_report`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                format: format,
                min_level: minLevel,
                output_path: outputPath,
                version: v
            }) as any;
            
            return {
                success: result.success || false,
                report: result.content || result.report || result.result,
                error: result.error,
                version: result.version || v
            };
        } catch (error: any) {
            return {
                success: false,
                error: error.message || String(error),
                version: v
            };
        }
    }
    
    /**
     * 获取可用版本列表
     */
    async getAvailableVersions(): Promise<string[]> {
        try {
            const result = await this.mcpClient.callTool('registry.list', {
                module_type: 'tenbagger'
            }) as any;
            return result.versions || [this.defaultVersion];
        } catch (error) {
            return [this.defaultVersion];
        }
    }
    
    /**
     * 设置默认版本
     */
    setDefaultVersion(version: string): void {
        this.defaultVersion = version;
    }
    
    /**
     * 获取默认版本
     */
    getDefaultVersion(): string {
        return this.defaultVersion;
    }
}
