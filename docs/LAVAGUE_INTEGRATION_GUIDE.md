# LaVague 完整集成指南 - 基于官方源码

> **创建时间**: 2026-01-17  
> **版本**: v2.0  
> **参考**: https://github.com/lavague-ai/LaVague

---

## 📋 目录

1. [集成概述](#集成概述)
2. [架构设计](#架构设计)
3. [安装和配置](#安装和配置)
4. [使用方式](#使用方式)
5. [模型配置](#模型配置)
6. [完整示例](#完整示例)
7. [故障排除](#故障排除)

---

## 🎯 集成概述

### 为什么需要重构？

**之前的问题**:
- ❌ 导入方式错误（`get_selenium_driver`不存在）
- ❌ WorldModel初始化方式错误（不支持`model`参数）
- ❌ 未使用官方推荐的`from_context`方法
- ❌ 依赖OpenAI API，需要API密钥

**重构后的优势**:
- ✅ 完全参照官方源码实现
- ✅ 使用正确的API（`from_context`方法）
- ✅ 支持本地模型（Ollama），无需API密钥
- ✅ 支持Cursor内置模型
- ✅ 使用WebAgent（官方推荐）

---

## 🏗️ 架构设计

### 官方架构（LaVague）

```
┌─────────────────────────────────────────┐
│  WebAgent (官方推荐使用)                 │
│  - 组合WorldModel和ActionEngine         │
│  - 提供run()方法执行任务                │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  WorldModel + ActionEngine              │
│  - 通过from_context()方法创建            │
│  - 使用Context配置模型                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Context (模型配置)                      │
│  - llm: 文本生成模型                     │
│  - mm_llm: 多模态模型（视觉理解）        │
│  - embedding: 嵌入模型                  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  SeleniumDriver (浏览器驱动)             │
│  - 执行实际浏览器操作                    │
└─────────────────────────────────────────┘
```

### TRQuant集成架构

```
┌─────────────────────────────────────────┐
│  LavagueCrawler (TRQuant封装)           │
│  - 使用WebAgent                         │
│  - 支持多种模型类型                      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  CursorContext (自定义Context)          │
│  - 支持Ollama本地模型                   │
│  - 支持Cursor内置模型                   │
│  - 支持OpenAI API（备选）               │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  LaVague官方实现                        │
│  - WebAgent                             │
│  - ActionEngine.from_context()          │
│  - WorldModel.from_context()            │
└─────────────────────────────────────────┘
```

---

## 🔧 安装和配置

### 1. 安装LaVague

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python -m pip install lavague
```

### 2. 安装Ollama（推荐，本地模型）

```bash
# Ubuntu/Linux
curl -fsSL https://ollama.com/install.sh | sh

# 启动Ollama服务
ollama serve

# 下载模型（在另一个终端）
ollama pull llama3.2
ollama pull llama3.2-vision
ollama pull nomic-embed-text
```

### 3. 安装Ollama Python包

```bash
./venv/bin/python -m pip install llama-index-llms-ollama llama-index-embeddings-ollama
```

### 4. 验证安装

```bash
./venv/bin/python -c "
from lavague.core import ActionEngine, WorldModel
from lavague.drivers.selenium import SeleniumDriver
from lavague.core.agents import WebAgent
print('✅ LaVague安装成功')
"
```

---

## 💻 使用方式

### 方式1: 使用Ollama本地模型（推荐）

```python
from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

# 使用Ollama本地模型（无需API密钥）
crawler = get_lavague_crawler(headless=True, model_type="ollama")

# 导航到网页
crawler.navigate("http://www.cninfo.com.cn")

# 执行指令
result = crawler.execute_instruction(
    "访问巨潮资讯网，搜索股票代码603986，提取最近90天的所有公告",
    max_actions=20
)

# 关闭
crawler.close()
```

### 方式2: 使用Cursor内置模型

```python
# 在Cursor IDE中使用
crawler = get_lavague_crawler(headless=True, model_type="cursor")

# 执行指令（通过Cursor Chat调用）
result = crawler.execute_instruction("访问网站并提取数据")
```

### 方式3: 使用OpenAI API（备选）

```python
# 需要设置OPENAI_API_KEY
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"

crawler = get_lavague_crawler(headless=True, model_type="openai")
result = crawler.execute_instruction("执行任务")
```

---

## 🎛️ 模型配置

### CursorContext配置

**位置**: `core/crawlers/lavague_cursor_context.py`

**支持的模型类型**:

| 类型 | 说明 | 需要API密钥 | 推荐场景 |
|------|------|-----------|---------|
| **ollama** | 本地Ollama模型 | ❌ 不需要 | ✅ 推荐，完全免费 |
| **cursor** | Cursor内置模型 | ❌ 不需要 | Cursor IDE中使用 |
| **openai** | OpenAI API | ✅ 需要 | 需要高质量结果时 |

### 自定义模型

```python
from core.crawlers.lavague_cursor_context import CursorContext

# 自定义Ollama模型
context = CursorContext(
    model_type="ollama",
    llm_model="llama3.2",           # LLM模型
    mm_llm_model="llama3.2-vision", # 多模态模型
    embedding_model="nomic-embed-text"  # 嵌入模型
)
```

---

## 📝 完整示例

### 示例1: 提取股票公告（使用Ollama）

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""使用LaVague提取股票公告（Ollama本地模型）"""

from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

def extract_announcements_ollama():
    """使用Ollama本地模型提取公告"""
    
    # 创建爬虫（使用Ollama，无需API密钥）
    crawler = get_lavague_crawler(headless=True, model_type="ollama")
    
    if not crawler.agent:
        print("❌ LaVague未正确初始化")
        print("请确保：")
        print("1. 已安装LaVague: pip install lavague")
        print("2. 已安装Ollama: pip install llama-index-llms-ollama")
        print("3. Ollama服务正在运行: ollama serve")
        return
    
    # 执行指令
    instruction = """
    访问巨潮资讯网（http://www.cninfo.com.cn），
    搜索股票代码603986，
    提取最近90天的所有公告，
    包括标题、日期、类型、链接
    """
    
    print("正在执行指令（使用Ollama本地模型）...")
    result = crawler.execute_instruction(instruction, max_actions=20)
    
    if result.get("success"):
        print("✅ 执行成功")
        print(f"结果: {result.get('result', '')[:500]}...")
    else:
        print(f"❌ 执行失败: {result.get('error')}")
    
    crawler.close()

if __name__ == "__main__":
    extract_announcements_ollama()
```

### 示例2: 使用MCP工具

```python
# 在Cursor Chat中使用
"使用crawler.lavague.execute工具，执行以下指令：
访问巨潮资讯网，搜索股票代码603986，提取最近90天的所有公告"
```

---

## 🔍 故障排除

### 问题1: LaVague未初始化

**错误**: `LaVague Agent未初始化`

**解决方案**:
1. 检查LaVague是否安装: `pip show lavague`
2. 检查Ollama是否安装（如果使用ollama）: `pip show llama-index-llms-ollama`
3. 检查Ollama服务是否运行: `ollama list`

### 问题2: Ollama模型未找到

**错误**: `model not found`

**解决方案**:
```bash
# 下载所需模型
ollama pull llama3.2
ollama pull llama3.2-vision
ollama pull nomic-embed-text
```

### 问题3: 导入错误

**错误**: `cannot import name 'get_selenium_driver'`

**解决方案**:
- ✅ 已修复：使用正确的导入方式 `SeleniumDriver`
- ✅ 使用 `from_context` 方法

### 问题4: WorldModel初始化错误

**错误**: `WorldModel.__init__() got an unexpected keyword argument 'model'`

**解决方案**:
- ✅ 已修复：`WorldModel()`不需要参数，使用Context配置

---

## 📊 对比：重构前后

| 特性 | 重构前 | 重构后 |
|------|--------|--------|
| **导入方式** | ❌ 错误（`get_selenium_driver`） | ✅ 正确（`SeleniumDriver`） |
| **WorldModel** | ❌ 错误（`model`参数） | ✅ 正确（无参数，使用Context） |
| **创建方式** | ❌ 直接创建 | ✅ `from_context`方法 |
| **模型支持** | ❌ 仅OpenAI | ✅ Ollama/Cursor/OpenAI |
| **API密钥** | ❌ 必需 | ✅ 可选（Ollama不需要） |
| **官方推荐** | ❌ 未使用WebAgent | ✅ 使用WebAgent |

---

## 🔗 相关文档

- **LaVague官方文档**: https://docs.lavague.ai
- **LaVague GitHub**: https://github.com/lavague-ai/LaVague
- **Ollama文档**: https://ollama.com
- **LlamaIndex文档**: https://docs.llamaindex.ai

---

## 📝 实施步骤

### 步骤1: 安装依赖

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 安装LaVague
./venv/bin/python -m pip install lavague

# 安装Ollama支持（推荐）
./venv/bin/python -m pip install llama-index-llms-ollama llama-index-embeddings-ollama
```

### 步骤2: 安装Ollama（可选，推荐）

```bash
# 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 启动服务
ollama serve

# 下载模型
ollama pull llama3.2
ollama pull llama3.2-vision
ollama pull nomic-embed-text
```

### 步骤3: 测试

```bash
./venv/bin/python examples/lavague_cninfo_603986.py
```

---

**最后更新**: 2026-01-17  
**维护者**: TRQuant Team
