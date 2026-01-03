#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将聚宽风控指南存入知识库"""
import sys
from pathlib import Path

PROJECT_ROOT = Path('/home/taotao/dev/QuantTest/TRQuant')
sys.path.insert(0, str(PJECT_ROOT))

try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError:
    print("⚠️ 知识库工具不可用，需要在MCP环境中运行")
    KB_AVAILABLE = False

def main():
    doc_path = PROJECT_ROOT / 'docs/JOINQUANT_RISK_CONTROL_GUIDE.md'
    if not doc_path.exists():
        print(f"❌ 文档不存在: {doc_path}")
        # 尝试从worktree目录读取
        doc_path = Path('/home/taotao/.cursor/worktrees/TRQuant/ope/docs/JOINQUANT_RISK_CONTROL_GUIDE.md')
        if not doc_path.exists():
            print(f"❌ worktree目录中也不存在")
            return
    
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"✅ 文档读取成功，长度: {len(content)} 字符")
    print("\n📝 请在MCP环境中运行以下命令:")
    print(f"mcp_xuanyuan_knowledge_add(")
    print(f"    title='聚宽平台风控模块指南',")
    print(f"    content='{content[:100]}...',")
    print(f"    type='guide',")
    print(f"    tags=['聚宽', 'JoinQuant', '风控', '风险管理', '最佳实践']")
    print(f")")

if __name__ == '__main__':
    main()
