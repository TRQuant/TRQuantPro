/**
 * VS Code API 全局单例
 */

declare global {
  interface Window {
    acquireVsCodeApi?: () => any;
    __vscode_api__?: any;
  }
}

/**
 * 获取 VS Code API 实例
 * 采用全局挂载方式，确保 acquireVsCodeApi() 只被调用一次
 */
export function getVSCodeAPI() {
  if (typeof window === 'undefined') {
    return null;
  }

  // 如果已经初始化过，直接返回
  if (window.__vscode_api__) {
    return window.__vscode_api__;
  }

  // 尝试初始化
  if (window.acquireVsCodeApi) {
    try {
      window.__vscode_api__ = window.acquireVsCodeApi();
      console.log('[VSCodeAPI] 全局实例初始化成功');
      return window.__vscode_api__;
    } catch (error) {
      console.error('[VSCodeAPI] 调用 acquireVsCodeApi 失败:', error);
    }
  }

  // 开发环境或初始化失败，返回模拟对象
  console.warn('[VSCodeAPI] 使用模拟 API 对象');
  window.__vscode_api__ = {
    postMessage: (msg: any) => console.log('[VSCodeAPI Mock] postMessage:', msg),
    getState: () => ({}),
    setState: (state: any) => console.log('[VSCodeAPI Mock] setState:', state),
  };
  
  return window.__vscode_api__;
}

export const vscode = getVSCodeAPI();
