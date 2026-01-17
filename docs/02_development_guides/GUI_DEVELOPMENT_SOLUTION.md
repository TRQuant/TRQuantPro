# TRQuant GUI 开发完整解决方案

> 创建日期: 2025-12-19
> 基于: VS Code Webview API 官方文档 + MCP最佳实践

---

## 🔍 网络爬取结果总结

### 1. VS Code Webview 官方最佳实践

根据 https://code.visualstudio.com/api/extension-guides/webview 的关键要点：

#### 消息传递机制
```
Extension (TypeScript)  <--->  Webview (HTML/JS)
     |                              |
     | webview.postMessage()        |
     |----------------------------->|
     |                              |
     | vscode.postMessage()         |
     |<-----------------------------|
     |                              |
     | onDidReceiveMessage()        |
     |----------------------------->|
```

#### CSP (内容安全策略) 配置
```html
<meta http-equiv="Content-Security-Policy" content="
    default-src 'none';
    script-src ${webview.cspSource} 'unsafe-inline';
    style-src ${webview.cspSource} 'unsafe-inline';
    img-src ${webview.cspSource} https: data:;
    connect-src ${webview.cspSource} https:;
">
```

#### 状态持久化
- 使用 `getState()` 和 `setState()` 保存/恢复状态
- 比 `retainContextWhenHidden` 性能更好
- 支持跨VS Code重启恢复

### 2. MCP + GUI 集成最佳实践

- **PyMCPAutoGUI**: 适用于桌面GUI自动化测试
- **MCPHub-Desktop**: MCP服务器图形管理工具
- **Docker最佳实践**: 清晰的工具命名和文档

---

## 🏗️ 完整解决方案架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Cursor IDE                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              VS Code Extension                       │   │
│  │  ┌─────────────────┐  ┌─────────────────────────┐  │   │
│  │  │  registerPanels │  │   workflowPanelV2.ts    │  │   │
│  │  │  (命令注册)      │  │   (面板管理)           │  │   │
│  │  └────────┬────────┘  └───────────┬─────────────┘  │   │
│  │           │                       │                 │   │
│  │           └───────────┬───────────┘                 │   │
│  │                       │                             │   │
│  │  ┌────────────────────▼────────────────────────┐   │   │
│  │  │           Webview (HTML/CSS/JS)              │   │   │
│  │  │  ┌────────────┐  ┌────────────────────────┐ │   │   │
│  │  │  │ 9步工作流  │  │   十倍股识别系统      │ │   │   │
│  │  │  └──────┬─────┘  └───────────┬────────────┘ │   │   │
│  │  │         │ postMessage        │              │   │   │
│  │  └─────────┼────────────────────┼──────────────┘   │   │
│  │            │                    │                   │   │
│  │  ┌─────────▼────────────────────▼──────────────┐   │   │
│  │  │              bridge.py (消息桥)              │   │   │
│  │  └─────────────────────┬───────────────────────┘   │   │
│  └────────────────────────┼───────────────────────────┘   │
│                           │                               │
│  ┌────────────────────────▼───────────────────────────┐   │
│  │              MCP Server Layer                       │   │
│  │  ┌──────────────────┐  ┌──────────────────────┐   │   │
│  │  │workflow_9steps   │  │ unified_dev_server   │   │   │
│  │  │  _server.py      │  │  (57个开发工具)      │   │   │
│  │  └──────────────────┘  └──────────────────────┘   │   │
│  │  ┌──────────────────┐  ┌──────────────────────┐   │   │
│  │  │ tenbagger_       │  │  其他MCP服务器       │   │   │
│  │  │  server.py       │  │                      │   │   │
│  │  └──────────────────┘  └──────────────────────┘   │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 文件结构

```
extension/
├── src/
│   ├── views/
│   │   ├── workflowPanelV2.ts    # 新版9步工作流面板
│   │   ├── tenbaggerPanel.ts     # 十倍股识别面板
│   │   ├── registerPanels.ts     # 面板注册
│   │   └── index.ts              # 导出
│   ├── utils/
│   │   ├── config.ts             # 配置管理
│   │   └── logger.ts             # 日志工具
│   └── extension.ts              # 入口文件
├── python/
│   └── bridge.py                 # Python消息桥
└── package.json

mcp_servers/
├── unified_dev_server.py         # 统一开发工具 (57个)
├── workflow_9steps_server.py     # 9步工作流
├── tenbagger_server.py           # 十倍股识别
└── trquant_core_server.py        # 核心数据服务
```

---

## 🔧 核心实现代码

### 1. Webview 面板基类 (TypeScript)

```typescript
// extension/src/views/basePanelV2.ts

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn, ChildProcess } from 'child_process';

export interface MCPResult {
    ok: boolean;
    data: any;
    error?: string;
}

export abstract class BasePanel {
    protected readonly _panel: vscode.WebviewPanel;
    protected readonly _extensionPath: string;
    protected _disposables: vscode.Disposable[] = [];
    
    // 子类必须实现
    abstract get viewType(): string;
    abstract get title(): string;
    abstract getHtmlContent(): string;
    abstract handleMessage(message: any): Promise<void>;
    
    constructor(panel: vscode.WebviewPanel, extensionPath: string) {
        this._panel = panel;
        this._extensionPath = extensionPath;
        
        // 设置HTML
        this._panel.webview.html = this.getHtmlContent();
        
        // 监听消息
        this._panel.webview.onDidReceiveMessage(
            msg => this.handleMessage(msg),
            null,
            this._disposables
        );
        
        // 清理
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    }
    
    // 获取项目根目录（防止worktrees问题）
    protected getProjectRoot(): string {
        const mainPath = '/home/taotao/dev/QuantTest/TRQuant';
        if (fs.existsSync(mainPath)) return mainPath;
        if (process.env.TRQUANT_ROOT) return process.env.TRQUANT_ROOT;
        return path.dirname(path.dirname(this._extensionPath));
    }
    
    // 获取Python路径
    protected getPythonPath(): string {
        const root = this.getProjectRoot();
        const venvPython = path.join(root, 'venv', 'bin', 'python3');
        return fs.existsSync(venvPython) ? venvPython : 'python3';
    }
    
    // 调用MCP工具
    protected async callMCP(toolName: string, args: Record<string, any>): Promise<MCPResult> {
        const pythonPath = this.getPythonPath();
        const projectRoot = this.getProjectRoot();
        const bridgePath = path.join(projectRoot, 'extension', 'python', 'bridge.py');
        
        return new Promise((resolve, reject) => {
            const proc = spawn(pythonPath, [bridgePath], {
                cwd: projectRoot,
                env: { ...process.env, PYTHONPATH: projectRoot }
            });
            
            let stdout = '';
            let stderr = '';
            
            proc.stdout.on('data', d => stdout += d.toString());
            proc.stderr.on('data', d => stderr += d.toString());
            
            proc.on('close', code => {
                if (code === 0) {
                    try {
                        const lines = stdout.trim().split('\n');
                        const result = JSON.parse(lines[lines.length - 1]);
                        resolve(result);
                    } catch (e) {
                        reject(new Error(`JSON解析失败: ${stdout}`));
                    }
                } else {
                    reject(new Error(`进程退出 ${code}: ${stderr}`));
                }
            });
            
            const request = {
                action: 'call_mcp_tool',
                params: { tool_name: toolName, arguments: args }
            };
            
            proc.stdin.write(JSON.stringify(request));
            proc.stdin.end();
        });
    }
    
    // 发送消息到Webview
    protected postMessage(message: any): void {
        this._panel.webview.postMessage(message);
    }
    
    // 生成CSP安全的HTML头部
    protected getHtmlHead(title: string, additionalStyles: string = ''): string {
        return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="
        default-src 'none';
        script-src 'unsafe-inline';
        style-src 'unsafe-inline';
        img-src data: https:;
        connect-src https:;
    ">
    <title>${title}</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--vscode-editor-background, #1e1e2e);
            color: var(--vscode-editor-foreground, #cdd6f4);
            padding: 20px;
            min-height: 100vh;
        }
        ${additionalStyles}
    </style>
</head>`;
    }
    
    // 生成通用的Webview脚本
    protected getWebviewScript(): string {
        return `
<script>
(function() {
    const vscode = acquireVsCodeApi();
    
    // 状态管理
    const state = vscode.getState() || {};
    
    function saveState(newState) {
        Object.assign(state, newState);
        vscode.setState(state);
    }
    
    function getState() {
        return state;
    }
    
    // 消息发送
    function send(command, data = {}) {
        vscode.postMessage({ command, ...data });
    }
    
    // 日志
    function log(msg, type = 'info') {
        const logEl = document.getElementById('log-content');
        if (logEl) {
            const entry = document.createElement('div');
            entry.className = 'log-entry ' + type;
            entry.textContent = new Date().toLocaleTimeString() + ' - ' + msg;
            logEl.insertBefore(entry, logEl.firstChild);
        }
        console.log('[Webview]', msg);
    }
    
    // 暴露给全局
    window.TRQuant = { send, log, saveState, getState, vscode };
    
    // 消息监听
    window.addEventListener('message', event => {
        const msg = event.data;
        log('收到: ' + msg.command, 'info');
        
        // 触发自定义事件，让页面处理
        window.dispatchEvent(new CustomEvent('trquant-message', { detail: msg }));
    });
    
    log('Webview已初始化', 'success');
})();
</script>`;
    }
    
    public dispose(): void {
        this._panel.dispose();
        while (this._disposables.length) {
            const d = this._disposables.pop();
            if (d) d.dispose();
        }
    }
}
```

### 2. Webview 消息处理模式

```javascript
// Webview内的JavaScript标准模式

// 1. 发送消息给Extension
window.TRQuant.send('runStep', { stepId: 'data_source' });

// 2. 监听Extension返回的消息
window.addEventListener('trquant-message', (e) => {
    const msg = e.detail;
    switch (msg.command) {
        case 'stepCompleted':
            updateStepUI(msg.stepId, 'completed', msg.result);
            break;
        case 'stepFailed':
            updateStepUI(msg.stepId, 'failed', msg.error);
            break;
    }
});

// 3. 保存/恢复状态
window.TRQuant.saveState({ currentStep: 'data_source' });
const savedStep = window.TRQuant.getState().currentStep;
```

### 3. MCP工具调用模式

```typescript
// Extension中调用MCP工具

// 9步工作流
const result = await this.callMCP('workflow9.run_step', {
    workflow_id: this.workflowId,
    step_id: 'data_source'
});

// 十倍股识别
const tenbagger = await this.callMCP('tenbagger.identify', {
    pool_size: 100,
    min_score: 70
});

// 开发工具
await this.callMCP('task.create', {
    title: '新功能开发',
    status: 'in_progress'
});
```

---

## 🚀 实施步骤

### Phase 1: 基础框架 (1天)
1. 创建 `basePanelV2.ts` 基类
2. 更新 `registerPanels.ts` 注册新命令
3. 验证消息通信正常

### Phase 2: 9步工作流 (2天)
1. 创建 `workflowPanelV2.ts`
2. 实现9步UI和交互
3. 集成 `workflow_9steps_server.py`

### Phase 3: 十倍股识别 (2天)
1. 创建 `tenbaggerPanelV2.ts`
2. 实现识别流程UI
3. 集成 `tenbagger_server.py`

### Phase 4: 数据可视化 (1天)
1. 添加ECharts图表
2. 实现实时数据更新

### Phase 5: 集成测试 (1天)
1. 完整功能测试
2. 性能优化
3. 错误处理完善

---

## ⚠️ 关键注意事项

### 1. 防止Worktrees问题
- 所有文件操作使用绝对路径
- `getProjectRoot()` 优先返回主项目路径
- 参考: `docs/ABSOLUTE_PATH_REQUIREMENT.md`

### 2. CSP安全策略
- 不使用外部CDN脚本
- 使用 `'unsafe-inline'` 允许内联脚本
- 限制 `connect-src` 只允许必要的连接

### 3. 状态持久化
- 使用 `vscode.getState()` / `vscode.setState()`
- 不依赖 `retainContextWhenHidden`
- 减少内存占用

### 4. 错误处理
- 每个MCP调用都要try-catch
- 在Webview显示友好的错误信息
- 记录详细日志便于调试

---

## 📚 参考资源

1. [VS Code Webview API](https://code.visualstudio.com/api/extension-guides/webview)
2. [VS Code Extension Samples](https://github.com/microsoft/vscode-extension-samples)
3. [MCP Protocol Specification](https://modelcontextprotocol.io/docs)
4. TRQuant内部文档:
   - `docs/UNIFIED_DEV_SERVER.md`
   - `docs/STANDARD_DEV_WORKFLOW_V2.md`
   - `docs/COMPREHENSIVE_CODE_AUDIT.md`

---

*文档版本: 1.0 | 更新时间: 2025-12-19*
