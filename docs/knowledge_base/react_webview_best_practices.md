# React + VS Code Webview 最佳实践

生成时间: 2025-12-21 19:47:50

---

## VS Code Webview 中使用 React 的最佳实践

**类别**: webview_react
**标签**: react, webview, vscode, vite, csp

在 VS Code Webview 中集成 React 应用的完整指南

### 关键要点

- 使用 Vite 构建 React 应用，配置 base: './' 确保相对路径
- 使用 webview.asWebviewUri() 转换所有资源路径
- 设置正确的 CSP (Content Security Policy)，包含 unsafe-inline 和 unsafe-eval
- 使用 acquireVsCodeApi() 获取 VS Code API 进行消息通信
- 使用 postMessage/onDidReceiveMessage 实现双向通信
- 使用 Zustand 进行状态管理，避免 Redux 的复杂性

### 代码示例

**示例 1**:
```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  base: './',  // 关键：确保相对路径
  build: {
    outDir: 'dist',
    rollupOptions: {
      output: {
        entryFileNames: 'assets/[name].js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: 'assets/[name].[ext]'
      }
    }
  }
});
```

**示例 2**:
```typescript
// webviewMCPClient.ts
const vscode = acquireVsCodeApi();

export function callMCP(tool: string, args: object): Promise<any> {
  return new Promise((resolve, reject) => {
    const id = generateId();
    
    const handler = (event: MessageEvent) => {
      if (event.data.type === 'mcpResult' && event.data.id === id) {
        window.removeEventListener('message', handler);
        if (event.data.error) {
          reject(new Error(event.data.error));
        } else {
          resolve(event.data.result);
        }
      }
    };
    
    window.addEventListener('message', handler);
    vscode.postMessage({ type: 'mcpCall', id, tool, args });
  });
}
```

---

## MCP 消息格式规范

**类别**: mcp_protocol
**标签**: mcp, protocol, message, webview

Webview 与 Extension Host 之间的 MCP 消息通信规范

### 关键要点

- 请求消息类型: mcpCall，包含 id, tool, args
- 响应消息类型: mcpResult，包含 id, success, result/error
- 使用唯一 id 匹配请求和响应
- 实现消息队列确保顺序处理
- 添加重试机制处理临时失败
- 设置超时避免无限等待

### 代码示例

**示例 1**:
```typescript
// 请求消息格式
{
  type: 'mcpCall',
  id: 'unique-request-id',
  tool: 'tool_name',
  args: { param1: 'value1' }
}

// 响应消息格式
{
  type: 'mcpResult',
  id: 'unique-request-id',
  success: true,
  result: { data: '...' }
}

// 错误响应格式
{
  type: 'mcpResult',
  id: 'unique-request-id',
  success: false,
  error: 'Error message'
}
```

---

## Zustand 状态管理最佳实践

**类别**: state_management
**标签**: zustand, state, react, store

在 VS Code Webview React 应用中使用 Zustand 管理状态

### 关键要点

- 每个功能模块创建独立的 Store
- 使用 immer 中间件简化不可变更新
- 在 Store 中封装 MCP 调用逻辑
- 使用 selector 优化重渲染
- 创建统一的 Store 入口文件

### 代码示例

**示例 1**:
```typescript
// store/workflowStore.ts
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

interface WorkflowState {
  steps: Step[];
  currentStep: number;
  loading: boolean;
  error: string | null;
  fetchSteps: () => Promise<void>;
  setCurrentStep: (step: number) => void;
}

export const useWorkflowStore = create<WorkflowState>()(
  immer((set, get) => ({
    steps: [],
    currentStep: 0,
    loading: false,
    error: null,
    
    fetchSteps: async () => {
      set({ loading: true, error: null });
      try {
        const result = await callMCP('workflow.get_steps', {});
        set({ steps: result.steps, loading: false });
      } catch (err) {
        set({ error: err.message, loading: false });
      }
    },
    
    setCurrentStep: (step) => set({ currentStep: step }),
  }))
);
```

---

## CSP (Content Security Policy) 配置

**类别**: security
**标签**: csp, security, webview, nonce

VS Code Webview 的安全策略配置

### 关键要点

- 必须使用 nonce 或 hash 允许内联脚本
- React 需要 unsafe-eval 才能正常运行
- Ant Design 等 UI 库需要 unsafe-inline 样式
- 限制 connect-src 到必要的来源
- 使用 webview.cspSource 作为可信来源

### 代码示例

**示例 1**:
```typescript
// ReactPanel.ts
const csp = [
  "default-src 'none'",
  \`img-src \${webview.cspSource} data: https:\`,
  \`script-src \${webview.cspSource} 'unsafe-inline' 'unsafe-eval'\`,
  \`style-src \${webview.cspSource} 'unsafe-inline'\`,
  \`font-src \${webview.cspSource}\`,
  "connect-src https://api.example.com"
].join('; ');

const html = \`
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="Content-Security-Policy" content="\${csp}">
  <link rel="stylesheet" href="\${styleUri}">
</head>
<body>
  <div id="root"></div>
  <script src="\${scriptUri}"></script>
</body>
</html>
\`;
```

---

## 资源路径处理

**类别**: resource_loading
**标签**: path, uri, webview, resource

正确处理 Webview 中的资源路径

### 关键要点

- 使用 webview.asWebviewUri() 转换本地文件路径
- 配置 localResourceRoots 限制可访问目录
- Vite 构建时使用相对路径 (base: './')
- 在 HTML 中替换 ./assets/ 为转换后的 URI
- 图片等资源也需要转换路径

### 代码示例

**示例 1**:
```typescript
// ReactPanel.ts
private _getHtmlContent(webview: vscode.Webview): string {
    const distPath = vscode.Uri.joinPath(this._extensionUri, 'webview-ui', 'dist');
    
    // 读取构建的 HTML
    const htmlPath = vscode.Uri.joinPath(distPath, 'index.html');
    let html = fs.readFileSync(htmlPath.fsPath, 'utf-8');
    
    // 转换资源路径
    const scriptUri = webview.asWebviewUri(
        vscode.Uri.joinPath(distPath, 'assets', 'index.js')
    );
    const styleUri = webview.asWebviewUri(
        vscode.Uri.joinPath(distPath, 'assets', 'index.css')
    );
    
    // 替换路径
    html = html.replace('./assets/index.js', scriptUri.toString());
    html = html.replace('./assets/index.css', styleUri.toString());
    
    return html;
}
```

---
