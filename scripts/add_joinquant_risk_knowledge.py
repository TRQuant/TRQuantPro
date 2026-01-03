#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将聚宽风控指南存入知识库
"""

import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

import json
from pathlib import Path

# 读取文档内容
doc_path = Path('/home/taotao/dev/QuantTest/TRQuant/docs/JOINQUANT_RISK_CONTROL_GUIDE.md')
if doc_path.exists():
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"✅ 文档读取成功，长度: {len(content)} 字符")
    print(f"内容预览（前500字符）:\n{content[:500]}")
else:
    print(f"❌ 文档不存在: {doc_path}")
    
print("\n📝 请使用MCP工具将内容存入知识库:")
print("mcp_xuanyuan_knowledge_add(title='聚宽平台风控模块指南', content=content, type='guide')")
