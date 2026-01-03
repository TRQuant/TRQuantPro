#!/usr/bin/env python3
"""
React + Webview 最佳实践爬取工具

爬取 React 和 VS Code Webview 相关的最佳实践文档
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict
import requests
from bs4 import BeautifulSoup
import argparse

PROJECT_ROOT = Path(__file__).parent.parent
KNOWLEDGE_DIR = PROJECT_ROOT / "docs" / "knowledge_base"


@dataclass
class PracticeEntry:
    """最佳实践条目"""
    title: str
    url: str
    category: str
    description: str
    key_points: List[str]
    code_examples: List[str]
    tags: List[str]


class ReactPracticesCrawler:
    """React 最佳实践爬虫"""
    
    RESOURCES = {
        "react_docs": {
            "url": "https://react.dev/learn",
            "category": "react_official"
        },
        "vite_docs": {
            "url": "https://vitejs.dev/guide/",
            "category": "vite"
        },
    }
    
    # 预定义的最佳实践（从经验总结）
    PREDEFINED_PRACTICES = [
        {
            "title": "VS Code Webview 中使用 React 的最佳实践",
            "category": "webview_react",
            "description": "在 VS Code Webview 中集成 React 应用的完整指南",
            "key_points": [
                "使用 Vite 构建 React 应用，配置 base: './' 确保相对路径",
                "使用 webview.asWebviewUri() 转换所有资源路径",
                "设置正确的 CSP (Content Security Policy)，包含 unsafe-inline 和 unsafe-eval",
                "使用 acquireVsCodeApi() 获取 VS Code API 进行消息通信",
                "使用 postMessage/onDidReceiveMessage 实现双向通信",
                "使用 Zustand 进行状态管理，避免 Redux 的复杂性",
            ],
            "code_examples": [
                """// vite.config.ts
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
});""",
                """// webviewMCPClient.ts
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
}""",
            ],
            "tags": ["react", "webview", "vscode", "vite", "csp"]
        },
        {
            "title": "MCP 消息格式规范",
            "category": "mcp_protocol",
            "description": "Webview 与 Extension Host 之间的 MCP 消息通信规范",
            "key_points": [
                "请求消息类型: mcpCall，包含 id, tool, args",
                "响应消息类型: mcpResult，包含 id, success, result/error",
                "使用唯一 id 匹配请求和响应",
                "实现消息队列确保顺序处理",
                "添加重试机制处理临时失败",
                "设置超时避免无限等待",
            ],
            "code_examples": [
                """// 请求消息格式
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
}""",
            ],
            "tags": ["mcp", "protocol", "message", "webview"]
        },
        {
            "title": "Zustand 状态管理最佳实践",
            "category": "state_management",
            "description": "在 VS Code Webview React 应用中使用 Zustand 管理状态",
            "key_points": [
                "每个功能模块创建独立的 Store",
                "使用 immer 中间件简化不可变更新",
                "在 Store 中封装 MCP 调用逻辑",
                "使用 selector 优化重渲染",
                "创建统一的 Store 入口文件",
            ],
            "code_examples": [
                """// store/workflowStore.ts
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
);""",
            ],
            "tags": ["zustand", "state", "react", "store"]
        },
        {
            "title": "CSP (Content Security Policy) 配置",
            "category": "security",
            "description": "VS Code Webview 的安全策略配置",
            "key_points": [
                "必须使用 nonce 或 hash 允许内联脚本",
                "React 需要 unsafe-eval 才能正常运行",
                "Ant Design 等 UI 库需要 unsafe-inline 样式",
                "限制 connect-src 到必要的来源",
                "使用 webview.cspSource 作为可信来源",
            ],
            "code_examples": [
                """// ReactPanel.ts
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
\`;""",
            ],
            "tags": ["csp", "security", "webview", "nonce"]
        },
        {
            "title": "资源路径处理",
            "category": "resource_loading",
            "description": "正确处理 Webview 中的资源路径",
            "key_points": [
                "使用 webview.asWebviewUri() 转换本地文件路径",
                "配置 localResourceRoots 限制可访问目录",
                "Vite 构建时使用相对路径 (base: './')",
                "在 HTML 中替换 ./assets/ 为转换后的 URI",
                "图片等资源也需要转换路径",
            ],
            "code_examples": [
                """// ReactPanel.ts
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
}""",
            ],
            "tags": ["path", "uri", "webview", "resource"]
        },
    ]
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_all_practices(self) -> List[PracticeEntry]:
        """获取所有最佳实践"""
        entries = []
        
        for practice in self.PREDEFINED_PRACTICES:
            entry = PracticeEntry(
                title=practice["title"],
                url="internal://knowledge-base",
                category=practice["category"],
                description=practice["description"],
                key_points=practice["key_points"],
                code_examples=practice["code_examples"],
                tags=practice["tags"]
            )
            entries.append(entry)
        
        return entries
    
    def save_entries(self, entries: List[PracticeEntry]) -> str:
        """保存最佳实践"""
        output_file = self.output_dir / "react_practices.json"
        
        data = [asdict(e) for e in entries]
        output_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        return str(output_file)
    
    def generate_markdown(self, entries: List[PracticeEntry]) -> str:
        """生成 Markdown 文档"""
        md_file = self.output_dir / "react_webview_best_practices.md"
        
        lines = [
            "# React + VS Code Webview 最佳实践",
            "",
            f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
        ]
        
        for entry in entries:
            lines.append(f"## {entry.title}")
            lines.append("")
            lines.append(f"**类别**: {entry.category}")
            lines.append(f"**标签**: {', '.join(entry.tags)}")
            lines.append("")
            lines.append(entry.description)
            lines.append("")
            lines.append("### 关键要点")
            lines.append("")
            for point in entry.key_points:
                lines.append(f"- {point}")
            lines.append("")
            
            if entry.code_examples:
                lines.append("### 代码示例")
                lines.append("")
                for i, code in enumerate(entry.code_examples, 1):
                    lines.append(f"**示例 {i}**:")
                    lines.append("```typescript")
                    lines.append(code)
                    lines.append("```")
                    lines.append("")
            
            lines.append("---")
            lines.append("")
        
        md_file.write_text('\n'.join(lines), encoding='utf-8')
        return str(md_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="React + Webview 最佳实践工具")
    parser.add_argument(
        "--output",
        type=Path,
        default=KNOWLEDGE_DIR,
        help="输出目录"
    )
    
    args = parser.parse_args()
    
    crawler = ReactPracticesCrawler(args.output)
    
    print("=" * 60)
    print("📚 React + Webview 最佳实践收集工具")
    print("=" * 60)
    
    entries = crawler.get_all_practices()
    
    json_file = crawler.save_entries(entries)
    md_file = crawler.generate_markdown(entries)
    
    print(f"\n✅ 收集完成!")
    print(f"📄 JSON 文件: {json_file}")
    print(f"📝 Markdown 文件: {md_file}")
    print(f"📊 共 {len(entries)} 条最佳实践")


if __name__ == "__main__":
    main()
