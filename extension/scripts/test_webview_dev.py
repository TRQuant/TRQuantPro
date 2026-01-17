#!/usr/bin/env python3
"""
Webview 开发者模式测试工具

用于测试 VS Code Extension 的 Webview 功能，包括：
- React 组件渲染
- MCP 通信
- 状态管理
- 错误处理
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List
import argparse

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
EXTENSION_DIR = PROJECT_ROOT / "extension"
WEBVIEW_DIR = EXTENSION_DIR / "webview-ui"


class WebviewTester:
    """Webview 测试器"""
    
    def __init__(self, dev_mode: bool = True):
        self.dev_mode = dev_mode
        self.test_results: List[Dict] = []
    
    def check_build(self) -> bool:
        """检查构建产物"""
        print("🔍 检查构建产物...")
        
        dist_dir = WEBVIEW_DIR / "dist"
        if not dist_dir.exists():
            print("❌ dist 目录不存在")
            return False
        
        required_files = ["index.html", "assets/index.js", "assets/index.css"]
        missing = []
        
        for file in required_files:
            filepath = dist_dir / file
            if not filepath.exists():
                missing.append(file)
        
        if missing:
            print(f"❌ 缺少文件: {', '.join(missing)}")
            return False
        
        print("✅ 构建产物完整")
        return True
    
    def check_html_content(self) -> bool:
        """检查 HTML 内容"""
        print("\n🔍 检查 HTML 内容...")
        
        html_file = WEBVIEW_DIR / "dist" / "index.html"
        if not html_file.exists():
            print("❌ index.html 不存在")
            return False
        
        content = html_file.read_text(encoding='utf-8')
        
        checks = {
            "root div": '<div id="root">' in content,
            "script tag": 'script' in content.lower(),
            "relative paths": './assets/' in content or '/assets/' in content,
        }
        
        all_pass = all(checks.values())
        
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")
        
        return all_pass
    
    def check_react_build(self) -> bool:
        """检查 React 构建配置"""
        print("\n🔍 检查 React 构建配置...")
        
        vite_config = WEBVIEW_DIR / "vite.config.ts"
        if not vite_config.exists():
            print("❌ vite.config.ts 不存在")
            return False
        
        content = vite_config.read_text(encoding='utf-8')
        
        checks = {
            "base: './'": "base: './'" in content or 'base: "./"' in content,
            "react plugin": "react" in content.lower(),
            "build config": "build:" in content,
        }
        
        all_pass = all(checks.values())
        
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")
        
        return all_pass
    
    def check_mcp_client(self) -> bool:
        """检查 MCP 客户端配置"""
        print("\n🔍 检查 MCP 客户端...")
        
        mcp_client = WEBVIEW_DIR / "src" / "services" / "webviewMCPClient.ts"
        if not mcp_client.exists():
            print("❌ webviewMCPClient.ts 不存在")
            return False
        
        content = mcp_client.read_text(encoding='utf-8')
        
        checks = {
            "acquireVsCodeApi": "acquireVsCodeApi" in content,
            "postMessage": "postMessage" in content,
            "mcpCall type": "mcpCall" in content or "mcp_call" in content,
            "mcpResult type": "mcpResult" in content,
        }
        
        all_pass = all(checks.values())
        
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")
        
        return all_pass
    
    def check_stores(self) -> bool:
        """检查状态管理 Store"""
        print("\n🔍 检查状态管理 Store...")
        
        store_dir = WEBVIEW_DIR / "src" / "store"
        if not store_dir.exists():
            print("❌ store 目录不存在")
            return False
        
        required_stores = [
            "workflowStore.ts",
            "tenbaggerStore.ts",
            "strategyStore.ts",
            "index.ts"
        ]
        
        missing = []
        for store in required_stores:
            if not (store_dir / store).exists():
                missing.append(store)
        
        if missing:
            print(f"❌ 缺少 Store: {', '.join(missing)}")
            return False
        
        print("✅ 所有 Store 文件存在")
        return True
    
    def check_react_panel(self) -> bool:
        """检查 ReactPanel 配置"""
        print("\n🔍 检查 ReactPanel 配置...")
        
        react_panel = EXTENSION_DIR / "src" / "views" / "ReactPanel.ts"
        if not react_panel.exists():
            print("❌ ReactPanel.ts 不存在")
            return False
        
        content = react_panel.read_text(encoding='utf-8')
        
        checks = {
            "asWebviewUri": "asWebviewUri" in content,
            "CSP meta": "Content-Security-Policy" in content,
            "mcpCall handler": "mcpCall" in content or "mcp_call" in content,
            "mcpResult response": "mcpResult" in content,
        }
        
        all_pass = all(checks.values())
        
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")
        
        return all_pass
    
    def run_all_checks(self) -> Dict[str, bool]:
        """运行所有检查"""
        print("=" * 60)
        print("🚀 Webview 开发者模式测试")
        print("=" * 60)
        
        checks = {
            "构建产物": self.check_build(),
            "HTML 内容": self.check_html_content(),
            "React 构建配置": self.check_react_build(),
            "MCP 客户端": self.check_mcp_client(),
            "状态管理 Store": self.check_stores(),
            "ReactPanel 配置": self.check_react_panel(),
        }
        
        print("\n" + "=" * 60)
        print("📊 测试结果汇总")
        print("=" * 60)
        
        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        
        for name, result in checks.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{status} {name}")
        
        print(f"\n总计: {passed}/{total} 通过")
        
        return checks
    
    def generate_report(self, checks: Dict[str, bool]) -> str:
        """生成测试报告"""
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "dev_mode": self.dev_mode,
            "checks": checks,
            "summary": {
                "total": len(checks),
                "passed": sum(1 for v in checks.values() if v),
                "failed": sum(1 for v in checks.values() if not v)
            }
        }
        
        report_file = EXTENSION_DIR / "test_report.json"
        report_file.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        return str(report_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Webview 开发者模式测试工具")
    parser.add_argument(
        "--dev",
        action="store_true",
        help="开发者模式（更详细的输出）"
    )
    parser.add_argument(
        "--check",
        choices=["build", "html", "react", "mcp", "stores", "panel", "all"],
        default="all",
        help="指定要运行的检查"
    )
    
    args = parser.parse_args()
    
    tester = WebviewTester(dev_mode=args.dev)
    
    if args.check == "all":
        checks = tester.run_all_checks()
        report_file = tester.generate_report(checks)
        print(f"\n📄 测试报告已保存: {report_file}")
        sys.exit(0 if all(checks.values()) else 1)
    else:
        check_methods = {
            "build": tester.check_build,
            "html": tester.check_html_content,
            "react": tester.check_react_build,
            "mcp": tester.check_mcp_client,
            "stores": tester.check_stores,
            "panel": tester.check_react_panel,
        }
        
        if args.check in check_methods:
            result = check_methods[args.check]()
            sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
