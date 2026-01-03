/**
 * Webview端MCP客户端
 * 
 * 通过postMessage与Extension通信，Extension再通过stdio与Python MCP服务器通信
 * 
 * 运行在Webview环境中（React应用）
 */

// 使用单例 VS Code API
import { getVSCodeAPI } from '../utils/vscodeApi';

// 获取VS Code API（单例）
const vscode = getVSCodeAPI();

/**
 * Webview MCP客户端
 */
class WebviewMCPClient {
  private messageId: number = 0;
  private pendingRequests: Map<string, {
    resolve: (value: any) => void;
    reject: (error: Error) => void;
    timeout: number;
  }> = new Map();
  private maxRetries: number = 3;
  private defaultTimeout: number = 30000;

  /**
   * 调用MCP工具
   */
  async callTool<T = any>(
    tool: string,
    args: Record<string, any> = {},
    options: {
      timeout?: number;
      retries?: number;
    } = {}
  ): Promise<T> {
    const { timeout = this.defaultTimeout, retries = this.maxRetries } = options;

    return this._callToolWithRetry<T>(tool, args, timeout, retries);
  }

  /**
   * 带重试的MCP调用
   */
  private async _callToolWithRetry<T>(
    tool: string,
    args: Record<string, any>,
    timeout: number,
    retries: number
  ): Promise<T> {
    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        return await this._callTool<T>(tool, args, timeout);
      } catch (error) {
        lastError = error as Error;
        console.warn(`[WebviewMCP] 调用失败 (尝试 ${attempt + 1}/${retries + 1}):`, error);

        // 如果不是最后一次尝试，等待后重试
        if (attempt < retries) {
          const delay = Math.min(1000 * Math.pow(2, attempt), 10000); // 指数退避，最大10秒
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }
    }

    throw lastError || new Error(`MCP调用失败: ${tool}`);
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
      throw new Error('VS Code API not available');
    }

    const id = `mcp_${Date.now()}_${++this.messageId}`;

    return new Promise<T>((resolve, reject) => {
      // 设置超时
      const timeoutHandle: ReturnType<typeof setTimeout> = setTimeout(() => {
        this.pendingRequests.delete(id);
        reject(new Error(`MCP call timeout: ${tool} (${timeout}ms)`));
      }, timeout);

      // 注册请求
      this.pendingRequests.set(id, {
        resolve: (value: T) => {
          clearTimeout(timeoutHandle);
          resolve(value);
        },
        reject: (error: Error) => {
          clearTimeout(timeoutHandle);
          reject(error);
        },
        timeout: timeoutHandle as unknown as number,
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
              pending.reject(new Error(message.error));
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
        reject(error as Error);
      }
    });
  }

  /**
   * 检查是否可用
   */
  isAvailable(): boolean {
    return vscode !== null;
  }

  /**
   * 获取待处理请求数量
   */
  getPendingCount(): number {
    return this.pendingRequests.size;
  }

  /**
   * 清理所有待处理请求
   */
  clearPending(): void {
    for (const [_id, item] of Array.from(this.pendingRequests.entries())) {
      clearTimeout(item.timeout);
      item.reject(new Error('Request cancelled'));
    }
    this.pendingRequests.clear();
  }
}

// 单例模式
let clientInstance: WebviewMCPClient | null = null;

/**
 * 获取Webview MCP客户端实例
 */
export function getWebviewMCPClient(): WebviewMCPClient {
  if (!clientInstance) {
    clientInstance = new WebviewMCPClient();
  }
  return clientInstance;
}

/**
 * 便捷函数：调用MCP工具
 */
export async function callMCPTool<T = any>(
  tool: string,
  args: Record<string, any> = {},
  options?: {
    timeout?: number;
    retries?: number;
  }
): Promise<T> {
  const client = getWebviewMCPClient();
  return client.callTool<T>(tool, args, options);
}

export default WebviewMCPClient;
