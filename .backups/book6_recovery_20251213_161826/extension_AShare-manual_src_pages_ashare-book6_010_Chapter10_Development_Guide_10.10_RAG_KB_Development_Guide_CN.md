---
title: 10.10 RAG知识库开发指南
lang: zh
layout: /src/layouts/Layout.astro
---

# 10.10 RAG知识库开发指南

## 概述

RAG知识库开发指南，包括LangChain使用、向量检索、索引构建等。

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-10

## 详细内容

> **基于LangChain生态的TRQuant知识库服务器**  
> **功能**: 将开发手册和工程代码从"静态文档"升级为"可问可追溯的工程知识库"

---

## 📋 快速开始

### 1. 确认依赖已安装

```bash
cd /home/taotao/dev/QuantTest/TRQuant
source extension/venv/bin/activate

# 检查依赖
python -c "import langchain; import chromadb; import sentence_transformers; from rank_bm25 import BM25Okapi; print('✅ 所有依赖已安装')"
```

如果缺少依赖，安装：
```bash
pip install langchain langchain-community langchain-text-splitters langchain-core langchain-huggingface chromadb rank-bm25 sentence-transformers
```

---

## 🚀 使用步骤

### Step 1: 构建索引（首次使用）

#### 1.1 预览模式（dry_run）- 查看将要索引的文件

```bash
# 在Python中执行
python << EOF
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from mcp_servers.kb_server import _handle_index_build
import json

# 预览Manual KB索引
result = _handle_index_build({
    "scope": "manual",
    "force_rebuild": False,
    "mode": "dry_run"
}, "test_trace", "inline")

response = json.loads(result[0].text)
data = response.get("data", response)
print(f"📊 预览结果:")

...

*完整内容请参考源文档*


## 相关文档

- 源文档位置：`docs/02_development_guides/` 或相关目录
- 相关代码：`extension/` 或 `mcp_servers/` 目录

## 关键要点

### 开发流程

1. **环境搭建**
   - 安装依赖
   - 配置开发环境
   - 验证环境

2. **开发实现**
   - 编写代码
   - 测试功能
   - 调试问题

3. **集成测试**
   - 单元测试
   - 集成测试
   - 端到端测试

4. **文档更新**
   - 更新文档
   - 更新示例
   - 更新指南

## 下一步

- [ ] 整理和格式化内容
- [ ] 添加代码示例
- [ ] 添加截图和图表
- [ ] 验证内容准确性

---

*最后更新: 2025-12-10*
