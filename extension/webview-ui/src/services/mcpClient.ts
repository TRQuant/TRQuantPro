/// <reference types="node" />
/**
 * TypeScript MCP 客户端
 * 
 * 在VS Code扩展侧使用，通过stdio直接与MCP服务器通信
 * 
 * 注意：此文件在扩展端运行，不在Webview中运行
 */

import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';

interface MCPMessage {
  jsonrpc: '2.0';
  id?: number | string;
  method?: string;
  params?: any;
  result?: any;
  error?: {
    code: number;
    message: string;
    data?: any;
  };
}



export class MCPClient {
  private process: ChildProcess | null = null;
  private messageId: number = 0;
  private pendingRequests: Map<number, {
    resolve: (result: any) => void;
    reject: (error: Error) => void;
  }> = new Map();
  private buffer: string = '';
  private projectRoot: string;

  constructor(projectRoot: string) {
    this.projectRoot = projectRoot;
  }

  /**
   * 启动MCP服务器
   */
  async start(): Promise<void> {
    return new Promise((resolve, reject) => {
      const serverPath = path.join(this.projectRoot, 'mcp_servers', 'unified_dev_server.py');
      
      this.process = spawn('python3', [serverPath], {
        cwd: this.projectRoot,
        env: {
          ...process.env,
          PYTHONPATH: this.projectRoot,
        },
        stdio: ['pipe', 'pipe', 'pipe'],
      });

      this.process.stdout?.on('data', (data: Buffer) => {
        this.handleData(data.toString());
      });

      this.process.stderr?.on('data', (data: Buffer) => {
        console.error('[MCP Server Error]:', data.toString());
      });

      this.process.on('error', (error: Error) => {
        console.error('[MCP Process Error]:', error);
        reject(error);
      });

      this.process.on('exit', (code: number | null) => {
        console.log(`[MCP Server] exited with code ${code}`);
        this.process = null;
      });

      // 等待服务器启动
      setTimeout(resolve, 1000);
    });
  }

  /**
   * 停止MCP服务器
   */
  stop(): void {
    if (this.process) {
      this.process.kill();
      this.process = null;
    }
  }

  /**
   * 处理接收到的数据
   */
  private handleData(data: string): void {
    this.buffer += data;
    
    // 尝试解析完整的JSON消息
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop() || '';
    
    for (const line of lines) {
      if (line.trim()) {
        try {
          const message: MCPMessage = JSON.parse(line);
          this.handleMessage(message);
        } catch (e) {
          console.error('[MCP Parse Error]:', e);
        }
      }
    }
  }

  /**
   * 处理MCP消息
   */
  private handleMessage(message: MCPMessage): void {
    if (message.id !== undefined) {
      const pending = this.pendingRequests.get(Number(message.id));
      if (pending) {
        this.pendingRequests.delete(Number(message.id));
        if (message.error) {
          pending.reject(new Error(message.error.message));
        } else {
          pending.resolve(message.result);
        }
      }
    }
  }

  /**
   * 发送请求
   */
  private async sendRequest(method: string, params: any): Promise<any> {
    if (!this.process) {
      throw new Error('MCP server not started');
    }

    const id = ++this.messageId;
    const message: MCPMessage = {
      jsonrpc: '2.0',
      id,
      method,
      params,
    };

    return new Promise((resolve, reject) => {
      this.pendingRequests.set(id, { resolve, reject });
      
      const data = JSON.stringify(message) + '\n';
      this.process?.stdin?.write(data);

      // 超时处理
      setTimeout(() => {
        if (this.pendingRequests.has(id)) {
          this.pendingRequests.delete(id);
          reject(new Error(`Request timeout: ${method}`));
        }
      }, 30000);
    });
  }

  /**
   * 调用MCP工具
   */
  async callTool<T = any>(tool: string, args: Record<string, any> = {}): Promise<T> {
    return this.sendRequest('tools/call', {
      name: tool,
      arguments: args,
    });
  }

  /**
   * 列出可用工具
   */
  async listTools(): Promise<any[]> {
    return this.sendRequest('tools/list', {});
  }

  /**
   * 检查服务器是否运行
   */
  isRunning(): boolean {
    return this.process !== null;
  }
}

// 单例模式
let mcpClientInstance: MCPClient | null = null;

export function getMCPClient(projectRoot: string): MCPClient {
  if (!mcpClientInstance) {
    mcpClientInstance = new MCPClient(projectRoot);
  }
  return mcpClientInstance;
}

export default MCPClient;
