import { useState, useCallback } from 'react';
import { getVSCodeAPI } from '../utils/vscodeApi';

// 使用单例 VS Code API
const vscode = getVSCodeAPI();

interface UseMCPOptions {
  immediate?: boolean;
  timeout?: number;
}

interface UseMCPResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  execute: (args?: Record<string, any>) => Promise<T>;
  reset: () => void;
}

/**
 * MCP调用Hook
 * @param tool MCP工具名称
 * @param defaultArgs 默认参数
 * @param options 选项
 */
export function useMCP<T = any>(
  tool: string,
  defaultArgs: Record<string, any> = {},
  options: UseMCPOptions = {}
): UseMCPResult<T> {
  const { timeout = 30000 } = options;
  
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const execute = useCallback(async (args: Record<string, any> = {}): Promise<T> => {
    return new Promise((resolve, reject) => {
      if (!vscode) {
        const err = new Error('VS Code API not available');
        setError(err);
        reject(err);
        return;
      }

      setLoading(true);
      setError(null);

      const messageId = `${tool}_${Date.now()}`;
      const mergedArgs = { ...defaultArgs, ...args };

      const handler = (event: MessageEvent) => {
        const message = event.data;
        if (message.type === 'mcpResult' && message.id === messageId) {
          window.removeEventListener('message', handler);
          setLoading(false);
          
          if (message.error) {
            const err = new Error(message.error);
            setError(err);
            reject(err);
          } else {
            setData(message.result);
            resolve(message.result);
          }
        }
      };

      window.addEventListener('message', handler);

      vscode.postMessage({
        type: 'mcpCall',
        id: messageId,
        tool,
        args: mergedArgs,
      });

      // 超时处理
      setTimeout(() => {
        window.removeEventListener('message', handler);
        if (loading) {
          setLoading(false);
          const err = new Error(`MCP call timeout: ${tool}`);
          setError(err);
          reject(err);
        }
      }, timeout);
    });
  }, [tool, JSON.stringify(defaultArgs), timeout]);

  const reset = useCallback(() => {
    setData(null);
    setLoading(false);
    setError(null);
  }, []);

  return { data, loading, error, execute, reset };
}

/**
 * 直接调用MCP（不使用状态管理）
 */
export async function callMCP<T = any>(
  tool: string, 
  args: Record<string, any> = {},
  timeout: number = 30000
): Promise<T> {
  return new Promise((resolve, reject) => {
    if (!vscode) {
      reject(new Error('VS Code API not available'));
      return;
    }

    const messageId = `${tool}_${Date.now()}`;

    const handler = (event: MessageEvent) => {
      const message = event.data;
      if (message.type === 'mcpResult' && message.id === messageId) {
        window.removeEventListener('message', handler);
        if (message.error) {
          reject(new Error(message.error));
        } else {
          resolve(message.result);
        }
      }
    };

    window.addEventListener('message', handler);

    vscode.postMessage({
      type: 'mcpCall',
      id: messageId,
      tool,
      args,
    });

    setTimeout(() => {
      window.removeEventListener('message', handler);
      reject(new Error(`MCP call timeout: ${tool}`));
    }, timeout);
  });
}

export default useMCP;
