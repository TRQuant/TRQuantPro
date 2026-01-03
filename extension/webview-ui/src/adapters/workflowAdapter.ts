/**
 * 工作流服务适配器（TypeScript）
 * 
 * 连接GUI和MCP服务，实现版本路由和格式转换。
 * 
 * Author: TRQuant Team
 * Date: 2025-12-21
 */

import { getWebviewMCPClient } from '../services/webviewMCPClient';

// 使用ReturnType获取类型
type WebviewMCPClient = ReturnType<typeof getWebviewMCPClient>;

export interface WorkflowRequest {
    workflow_id?: string;
    step_id?: string;
    args?: Record<string, any>;
    version?: string;
}

export interface WorkflowResponse {
    success: boolean;
    workflow_id?: string;
    step_id?: string;
    result?: any;
    error?: string;
    version?: string;
}

export interface WorkflowStep {
    id: string;
    name: string;
    icon: string;
    color: string;
    description: string;
    status?: string;
}

export class WorkflowAdapter {
    private mcpClient: WebviewMCPClient;
    private defaultVersion: string = "v1";
    
    constructor(mcpClient: WebviewMCPClient) {
        this.mcpClient = mcpClient;
    }
    
    /**
     * 获取所有步骤定义
     */
    async getSteps(): Promise<WorkflowResponse> {
        const version = this.defaultVersion;
        const toolName = `workflow9.get_steps`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                version: version
            });
            
            return {
                success: result.success || false,
                result: result.steps || result.result,
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
     * 创建工作流
     */
    async createWorkflow(name?: string): Promise<WorkflowResponse> {
        const version = this.defaultVersion;
        const toolName = `workflow9.create`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                name: name,
                version: version
            }) as any;
            
            return {
                success: result.success || false,
                workflow_id: result.workflow_id,
                result: result,
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
     * 获取工作流状态
     */
    async getStatus(workflowId: string): Promise<WorkflowResponse> {
        const version = this.defaultVersion;
        const toolName = `workflow9.status`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                workflow_id: workflowId,
                version: version
            }) as any;
            
            return {
                success: result.success || false,
                workflow_id: workflowId,
                result: result,
                error: result.error,
                version: result.version || version
            };
        } catch (error: any) {
            return {
                success: false,
                workflow_id: workflowId,
                error: error.message || String(error),
                version: version
            };
        }
    }
    
    /**
     * 执行步骤
     */
    async runStep(workflowId: string, stepId: string, args?: Record<string, any>): Promise<WorkflowResponse> {
        const version = this.defaultVersion;
        const toolName = `workflow9.run_step`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                workflow_id: workflowId,
                step_id: stepId,
                args: args || {},
                version: version
            }) as any;
            
            return {
                success: result.success || false,
                workflow_id: workflowId,
                step_id: stepId,
                result: result,
                error: result.error,
                version: result.version || version
            };
        } catch (error: any) {
            return {
                success: false,
                workflow_id: workflowId,
                step_id: stepId,
                error: error.message || String(error),
                version: version
            };
        }
    }
    
    /**
     * 执行所有步骤
     */
    async runAll(workflowId: string): Promise<WorkflowResponse> {
        const version = this.defaultVersion;
        const toolName = `workflow9.run_all`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                workflow_id: workflowId,
                version: version
            }) as any;
            
            return {
                success: result.success || false,
                workflow_id: workflowId,
                result: result,
                error: result.error,
                version: result.version || version
            };
        } catch (error: any) {
            return {
                success: false,
                workflow_id: workflowId,
                error: error.message || String(error),
                version: version
            };
        }
    }
    
    /**
     * 获取工作流上下文
     */
    async getContext(workflowId: string): Promise<WorkflowResponse> {
        const version = this.defaultVersion;
        const toolName = `workflow9.get_context`;
        
        try {
            const result = await this.mcpClient.callTool(toolName, {
                workflow_id: workflowId,
                version: version
            }) as any;
            
            return {
                success: result.success || false,
                workflow_id: workflowId,
                result: result.context || result.result,
                error: result.error,
                version: result.version || version
            };
        } catch (error: any) {
            return {
                success: false,
                workflow_id: workflowId,
                error: error.message || String(error),
                version: version
            };
        }
    }
    
    /**
     * 获取可用版本列表
     */
    async getAvailableVersions(): Promise<string[]> {
        try {
            const result = await this.mcpClient.callTool('registry.list', {
                module_type: 'workflow'
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
