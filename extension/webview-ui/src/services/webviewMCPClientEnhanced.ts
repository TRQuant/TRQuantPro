/**
 * Webview端MCP客户端（增强版）
 * 
 * 增强功能：
 * 1. 连接状态监控
 * 2. 消息队列（并发控制）
 * 3. 错误分类和处理
 * 4. 连接健康检查
 * 5. 自动重连机制
 */

import { getVSCodeAPI } from '../utils/vscodeApi';

const vscode = getVSCodeAPI();

/**
 * 连接状态
 */
export enum ConnectionStatus {
  DISCONNECTED = 'disconnected',
  CONNECTING = 'connecting',
  CONNECTED = 'connected',
  ERROR = 'error',
}

/**
 * 错误类型
 */
export enum MCPErrorType {
  TIMEOUT = 'timeout',
  NETWORK = 'network',
  SERVER = 'server',
  VALIDATION = 'validation',
  UNKNOWN = 'unknown',
}

/**
 * MCP错误
 */
export class MCPError extends Error {
  constructor(
    message: string,
    public type: MCPErrorType,
    public tool?: string,
    public retryable: boolean = false
  ) {
    super(message);
    this.name = 'MCPError';
  }
}

/**
 * 消息队列项
 */
interface QueueItem {
  id: string;
  tool: string;
  args: Record<string, any>;
  resolve: (value: any) => void;
  reject: (error: Error) => void;
  timeout: number;
  retries: number;
  timestamp: number;
}

/**
 * Webview MCP客户端（增强版）
 */
class WebviewMCPClientEnhanced {
  private messageId: number = 0;
  private pendingRequests: Map<string, QueueItem> = new Map();
  private messageQueue: QueueItem[] = [];
  private maxConcurrent: number = 5; // 最大并发数
  private currentConcurrent: number = 0;
  private maxRetries: number = 3;
  private defaultTimeout: number = 30000;
  private connectionStatus: ConnectionStatus = ConnectionStatus.DISCONNECTED;
  private healthCheckInterval: NodeJS.Timeout | null = null;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private statusListeners: Set<(status: ConnectionStatus) => void> = new Set();

  constructor() {
    this._checkConnection();
    this._startHealthCheck();
  }

  /**
   * 检查连接状态
   */
  private _checkConnection(): void {
    if (vscode) {
      this.connectionStatus = ConnectionStatus.CONNECTED;
      this.reconnectAttempts = 0;
    } else {
      this.connectionStatus = ConnectionStatus.DISCONNECTED;
    }
    this._notifyStatusChange();
  }

  /**
   * 启动健康检查
   */
  private _startHealthCheck(): void {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }

    this.healthCheckInterval = setInterval(() => {
      this._checkConnection();
      
      // 如果连接断开，尝试重连
      if (this.connectionStatus === ConnectionStatus.DISCONNECTED && 
          this.reconnectAttempts < this.maxReconnectAttempts) {
        this._attemptReconnect();
      }
    }, 5000); // 每5秒检查一次
  }

  /**
   * 尝试重连
   */
  private _attemptReconnect(): void {
    this.reconnectAttempts++;
    this.connectionStatus = ConnectionStatus.CONNECTING;
    this._notifyStatusChange();
    
    // 检查VS Code API是否可用
    const checkVSCode = getVSCodeAPI();
    if (checkVSCode) {
      this.connectionStatus = ConnectionStatus.CONNECTED;
      this.reconnectAttempts = 0;
      this._notifyStatusChange();
      this._processQueue();
    } else {
      this.connectionStatus = ConnectionStatus.DISCONNECTED;
      this._notifyStatusChange();
    }
  }

  /**
   * 通知状态变化
   */
  private _notifyStatusChange(): void {
    this.statusListeners.forEach(listener => {
      try {
        listener(this.connectionStatus);
      } catch (error) {
        console.error('[WebviewMCP] 状态监听器错误:', error);
      }
    });
  }

  /**
   * 处理消息队列
   */
  private _processQueue(): void {
    while (this.messageQueue.length > 0 && this.currentConcurrent < this.maxConcurrent) {
      const item = this.messageQueue.shift();
      if (item) {
        this.currentConcurrent++;
        this._executeRequest(item).finally(() => {
          this.currentConcurrent--;
          this._processQueue();
        });
      }
    }
  }

  /**
   * 执行请求
   */
  private async _executeRequest(item: QueueItem): Promise<void> {
    try {
      const result = await this._callTool(item.tool, item.args, item.timeout);
      item.resolve(result);
    } catch (error) {
      // 如果是可重试的错误且还有重试次数
      if (item.retries > 0 && error instanceof MCPError && error.retryable) {
        item.retries--;
        // 延迟后重新加入队列
        setTimeout(() => {
          this.messageQueue.push(item);
          this._processQueue();
        }, 1000 * (this.maxRetries - item.retries));
      } else {
        const errorObj = error instanceof Error ? error : new Error(String(error));
        item.reject(errorObj);
      }
    } finally {
      this.pendingRequests.delete(item.id);
    }
  }

  /**
   * 调用MCP工具（增强版）
   */
  async callTool<T = any>(
    tool: string,
    args: Record<string, any> = {},
    options: {
      timeout?: number;
      retries?: number;
      priority?: number; // 优先级，数字越大优先级越高
    } = {}
  ): Promise<T> {
    const { timeout = this.defaultTimeout, retries = this.maxRetries, priority = 0 } = options;

    // 检查连接状态
    if (this.connectionStatus === ConnectionStatus.DISCONNECTED) {
      throw new MCPError(
        'VS Code API不可用，请检查扩展是否已激活',
        MCPErrorType.NETWORK,
        tool,
        true
      );
    }

    const id = `mcp_${Date.now()}_${++this.messageId}`;
    
    return new Promise<T>((resolve, reject) => {
      const item: QueueItem = {
        id,
        tool,
        args,
        resolve: resolve as (value: any) => void,
        reject,
        timeout,
        retries,
        timestamp: Date.now(),
      };

      // 根据优先级插入队列
      if (priority > 0) {
        // 高优先级插入到队列前面
        this.messageQueue.unshift(item);
      } else {
        this.messageQueue.push(item);
      }

      this.pendingRequests.set(id, item);
      this._processQueue();
    });
  }

  /**
   * 执行MCP调用
   */
  private async _callTool<T>(
    tool: string,
    args: Record<string, any>,
    timeout: number
  ): Promise<T> {
    if (!vscode) {
      throw new MCPError(
        'VS Code API not available',
        MCPErrorType.NETWORK,
        tool,
        true
      );
    }

    const id = `mcp_${Date.now()}_${++this.messageId}`;

    return new Promise<T>((resolve, reject) => {
      // 设置超时
      const timeoutHandle = setTimeout(() => {
        this.pendingRequests.delete(id);
        reject(new MCPError(
          `MCP调用超时: ${tool} (${timeout}ms)`,
          MCPErrorType.TIMEOUT,
          tool,
          true
        ));
      }, timeout);

      // 注册请求
      this.pendingRequests.set(id, {
        id,
        tool,
        args,
        resolve: (value: T) => {
          clearTimeout(timeoutHandle);
          resolve(value);
        },
        reject: (error: Error) => {
          clearTimeout(timeoutHandle);
          reject(error);
        },
        timeout: timeoutHandle as unknown as number,
        retries: 0,
        timestamp: Date.now(),
      });

      // 监听响应
      const handler = (event: MessageEvent) => {
        const message = event.data;
        if (message.type === 'mcpResult' && message.id === id) {
          window.removeEventListener('message', handler);
          const pending = this.pendingRequests.get(id);
          if (pending) {
            this.pendingRequests.delete(id);
            if (message.error) {
              // 分类错误
              const errorType = this._classifyError(message.error);
              const retryable = errorType === MCPErrorType.NETWORK || 
                               errorType === MCPErrorType.TIMEOUT;
              pending.reject(new MCPError(
                message.error,
                errorType,
                tool,
                retryable
              ));
            } else {
              pending.resolve(message.result);
            }
          }
        }
      };

      window.addEventListener('message', handler);

      // 发送请求
      try {
        vscode.postMessage({
          type: 'mcpCall',
          id,
          tool,
          args,
        });

        console.log(`[WebviewMCP] 发送请求: ${tool}`, { id, args });
      } catch (error) {
        window.removeEventListener('message', handler);
        this.pendingRequests.delete(id);
        clearTimeout(timeoutHandle);
        reject(new MCPError(
          `发送请求失败: ${error instanceof Error ? error.message : String(error)}`,
          MCPErrorType.NETWORK,
          tool,
          true
        ));
      }
    });
  }

  /**
   * 分类错误
   */
  private _classifyError(errorMessage: string): MCPErrorType {
    const msg = errorMessage.toLowerCase();
    
    if (msg.includes('timeout') || msg.includes('超时')) {
      return MCPErrorType.TIMEOUT;
    }
    if (msg.includes('network') || msg.includes('连接') || msg.includes('connection')) {
      return MCPErrorType.NETWORK;
    }
    if (msg.includes('server') || msg.includes('服务器') || msg.includes('500') || msg.includes('503')) {
      return MCPErrorType.SERVER;
    }
    if (msg.includes('validation') || msg.includes('验证') || msg.includes('invalid')) {
      return MCPErrorType.VALIDATION;
    }
    
    return MCPErrorType.UNKNOWN;
  }

  /**
   * 检查是否可用
   */
  isAvailable(): boolean {
    return this.connectionStatus === ConnectionStatus.CONNECTED;
  }

  /**
   * 获取连接状态
   */
  getConnectionStatus(): ConnectionStatus {
    return this.connectionStatus;
  }

  /**
   * 监听连接状态变化
   */
  onStatusChange(listener: (status: ConnectionStatus) => void): () => void {
    this.statusListeners.add(listener);
    // 立即调用一次
    listener(this.connectionStatus);
    
    // 返回取消监听的函数
    return () => {
      this.statusListeners.delete(listener);
    };
  }

  /**
   * 获取待处理请求数量
   */
  getPendingCount(): number {
    return this.pendingRequests.size;
  }

  /**
   * 获取队列长度
   */
  getQueueLength(): number {
    return this.messageQueue.length;
  }

  /**
   * 清理所有待处理请求
   */
  clearPending(): void {
    for (const [_id, item] of Array.from(this.pendingRequests.entries())) {
      clearTimeout(item.timeout);
      item.reject(new MCPError('请求已取消', MCPErrorType.UNKNOWN, item.tool, false));
    }
    this.pendingRequests.clear();
    this.messageQueue = [];
  }

  /**
   * 销毁客户端
   */
  destroy(): void {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
      this.healthCheckInterval = null;
    }
    this.clearPending();
    this.statusListeners.clear();
  }
}

// 单例模式
let clientInstance: WebviewMCPClientEnhanced | null = null;

/**
 * 获取Webview MCP客户端实例（增强版）
 */
export function getWebviewMCPClientEnhanced(): WebviewMCPClientEnhanced {
  if (!clientInstance) {
    clientInstance = new WebviewMCPClientEnhanced();
  }
  return clientInstance;
}

/**
 * 便捷函数：调用MCP工具（增强版）
 */
export async function callMCPToolEnhanced<T = any>(
  tool: string,
  args: Record<string, any> = {},
  options?: {
    timeout?: number;
    retries?: number;
    priority?: number;
  }
): Promise<T> {
  const client = getWebviewMCPClientEnhanced();
  return client.callTool<T>(tool, args, options);
}

export default WebviewMCPClientEnhanced;

