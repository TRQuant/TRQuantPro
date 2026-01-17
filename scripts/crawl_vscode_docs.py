#!/usr/bin/env python3
"""
VS Code Extension 和 Webview 文档爬取工具

用于爬取官方文档并整理到知识库
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse

PROJECT_ROOT = Path(__file__).parent.parent
KNOWLEDGE_DIR = PROJECT_ROOT / "docs" / "knowledge_base"


@dataclass
class DocEntry:
    """文档条目"""
    title: str
    url: str
    category: str
    content: str
    code_blocks: List[str]
    tags: List[str]


class VSCodeDocsCrawler:
    """VS Code 文档爬虫"""
    
    BASE_URLS = {
        "webview": "https://code.visualstudio.com/api/extension-guides/webview",
        "extension_api": "https://code.visualstudio.com/api/references/vscode-api",
        "extension_anatomy": "https://code.visualstudio.com/api/get-started/extension-anatomy",
        "activation_events": "https://code.visualstudio.com/api/references/activation-events",
    }
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        })
    
    def fetch_page(self, url: str) -> str:
        """获取页面内容"""
        print(f"📥 正在获取: {url}")
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ 获取失败: {e}")
            return ""
    
    def parse_docs(self, html: str, url: str, category: str) -> DocEntry:
        """解析文档"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else "Untitled"
        
        # 提取主要内容
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        
        if main_content:
            # 提取代码块
            code_blocks = []
            for code in main_content.find_all('pre'):
                code_text = code.get_text().strip()
                if code_text:
                    code_blocks.append(code_text)
            
            # 提取纯文本
            for tag in main_content.find_all(['script', 'style', 'nav', 'footer']):
                tag.decompose()
            
            content = main_content.get_text(separator='\n').strip()
            # 清理多余空行
            content = re.sub(r'\n{3,}', '\n\n', content)
        else:
            content = ""
            code_blocks = []
        
        # 生成标签
        tags = self._generate_tags(content, title)
        
        return DocEntry(
            title=title,
            url=url,
            category=category,
            content=content[:10000],  # 限制长度
            code_blocks=code_blocks[:20],  # 限制代码块数量
            tags=tags
        )
    
    def _generate_tags(self, content: str, title: str) -> List[str]:
        """生成标签"""
        tags = []
        
        keywords = {
            "webview": ["webview", "WebviewPanel", "createWebviewPanel"],
            "react": ["react", "React", "useState", "useEffect"],
            "mcp": ["mcp", "MCP", "Model Context Protocol"],
            "csp": ["Content-Security-Policy", "CSP", "nonce"],
            "message": ["postMessage", "onDidReceiveMessage"],
            "typescript": ["TypeScript", "typescript", ".ts"],
            "extension": ["extension", "Extension", "activate"],
        }
        
        text = f"{title} {content}"
        for tag, patterns in keywords.items():
            if any(p in text for p in patterns):
                tags.append(tag)
        
        return tags
    
    def crawl_all(self) -> List[DocEntry]:
        """爬取所有文档"""
        entries = []
        
        for name, url in self.BASE_URLS.items():
            html = self.fetch_page(url)
            if html:
                entry = self.parse_docs(html, url, name)
                entries.append(entry)
                time.sleep(1)  # 礼貌延迟
        
        return entries
    
    def save_entries(self, entries: List[DocEntry]) -> str:
        """保存文档条目"""
        output_file = self.output_dir / "vscode_docs.json"
        
        data = [asdict(e) for e in entries]
        output_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        return str(output_file)
    
    def generate_summary(self, entries: List[DocEntry]) -> str:
        """生成摘要文档"""
        summary_file = self.output_dir / "vscode_docs_summary.md"
        
        lines = [
            "# VS Code Extension 开发文档摘要",
            "",
            f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 文档列表",
            ""
        ]
        
        for entry in entries:
            lines.append(f"### {entry.title}")
            lines.append(f"- **URL**: {entry.url}")
            lines.append(f"- **类别**: {entry.category}")
            lines.append(f"- **标签**: {', '.join(entry.tags)}")
            lines.append(f"- **代码示例**: {len(entry.code_blocks)} 个")
            lines.append("")
            
            # 添加内容摘要
            summary = entry.content[:500] + "..." if len(entry.content) > 500 else entry.content
            lines.append("**内容摘要**:")
            lines.append(summary)
            lines.append("")
        
        summary_file.write_text('\n'.join(lines), encoding='utf-8')
        return str(summary_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="VS Code 文档爬取工具")
    parser.add_argument(
        "--output",
        type=Path,
        default=KNOWLEDGE_DIR,
        help="输出目录"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="指定要爬取的 URL"
    )
    
    args = parser.parse_args()
    
    crawler = VSCodeDocsCrawler(args.output)
    
    print("=" * 60)
    print("🔍 VS Code Extension 文档爬取工具")
    print("=" * 60)
    
    if args.url:
        html = crawler.fetch_page(args.url)
        if html:
            entry = crawler.parse_docs(html, args.url, "custom")
            entries = [entry]
        else:
            entries = []
    else:
        entries = crawler.crawl_all()
    
    if entries:
        json_file = crawler.save_entries(entries)
        summary_file = crawler.generate_summary(entries)
        
        print("\n" + "=" * 60)
        print("✅ 爬取完成!")
        print(f"📄 JSON 文件: {json_file}")
        print(f"📝 摘要文件: {summary_file}")
        print(f"📊 共爬取 {len(entries)} 个文档")
    else:
        print("\n❌ 没有爬取到任何内容")


if __name__ == "__main__":
    main()
