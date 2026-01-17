# LaVague 官方源码集成方案

> **创建时间**: 2026-01-17  
> **版本**: v2.0  
> **参考源码**: https://github.com/lavague-ai/LaVague

---

## 📋 概述

本方案完全参照LaVague官方源码实现，解决了之前频繁出现的错误，并支持使用Cursor（本地模型）而不是OpenAI API。

---

## 🔍 官方源码分析

### 核心发现

通过分析LaVague官方源码（`/tmp/lavague-source`），发现：

1. **正确的导入方式**:
   ```python
   from lavague.drivers.selenium import SeleniumDriver  # ✅ 正确
   # 不是 get_selenium_driver()  # ❌ 错误
   ```

2. **正确的初始化方式**:
   ```python
   # ✅ 官方推荐方式
   from lavague.core import ActionEngine, WorldModel
   from lavague.core.agents import WebAgent
   from lavague.drivers.selenium import SeleniumDriver
   
   driver = SeleniumDriver(headless=True)
   action_engine = ActionEngine.from_context(context, driver)
   world_model = WorldModel.from_context(context)
   agent = WebAgent(world_model, action_engine)
   ```

3. **Context机制**:
   - `Context`包含：`llm`, `mm_llm`, `embedding`
   - 可以使用任何LlamaIndex兼容的模型
   - 支持自定义Context

4. **WebAgent使用**:
   - 官方推荐使用`WebAgent`而不是直接使用`ActionEngine`
   - `agent.run(instruction)`执行任务
   - `agent.get(url)`导航到URL

---

## 🏗️ 集成架构

### 文件结构

```
TRQuant/
├── core/
│   └── crawlers/
│       └── lavague_cursor_context.py  # 自定义Context（支持Ollama/Cursor）
├── mcp_servers/
│   └── crawlers/
│       └── lavague_crawler.py          # 重构后的爬虫（参照官方实现）
└── docs/
    ├── LAVAGUE_INTEGRATION_GUIDE.md    # 集成指南
    └── LAVAGUE_OFFICIAL_INTEGRATION.md  # 本文档
```

### 核心组件

#### 1. CursorContext (`core/crawlers/lavague_cursor_context.py`)

**功能**: 自定义Context，支持多种模型类型

**支持的模型**:
- **Ollama**（推荐）: 本地模型，无需API密钥
- **Cursor**: Cursor内置模型
- **OpenAI**: OpenAI API（备选）

**实现方式**:
```python
class CursorContext(Context):
    def __init__(self, model_type="ollama", ...):
        if model_type == "ollama":
            from llama_index.llms.ollama import Ollama
            llm = Ollama(model=llm_model)
            # ...
```

#### 2. LavagueCrawler（重构版）

**改进**:
- ✅ 使用`from_context`方法（官方推荐）
- ✅ 使用`WebAgent`（官方推荐）
- ✅ 支持自定义Context
- ✅ 正确的导入方式

---

## 🚀 使用方式

### 方式1: 使用Ollama本地模型（推荐）

**优势**:
- ✅ 完全免费，无需API密钥
- ✅ 本地运行，速度快
- ✅ 数据隐私保护

**步骤**:

1. **安装Ollama**:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama serve
   ```

2. **下载模型**:
   ```bash
   ollama pull llama3.2
   ollama pull llama3.2-vision
   ollama pull nomic-embed-text
   ```

3. **安装Python包**:
   ```bash
   pip install llama-index-llms-ollama llama-index-embeddings-ollama
   ```

4. **使用**:
   ```python
   from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler
   
   crawler = get_lavague_crawler(headless=True, model_type="ollama")
   result = crawler.execute_instruction("访问网站并提取数据")
   ```

### 方式2: 在Cursor IDE中使用

**说明**: Cursor本身不是LLM API，但可以通过以下方式使用：

1. **在Cursor Chat中调用MCP工具**:
   ```
   使用crawler.lavague.execute工具，执行指令：...
   ```

2. **使用Ollama作为替代**:
   - Cursor IDE中运行代码时，使用Ollama本地模型
   - 无需API密钥，完全本地运行

---

## 📊 对比：官方实现 vs 之前实现

| 方面 | 之前实现 | 官方实现（重构后） |
|------|---------|------------------|
| **导入** | `get_selenium_driver()` ❌ | `SeleniumDriver()` ✅ |
| **WorldModel** | `WorldModel(model=...)` ❌ | `WorldModel.from_context()` ✅ |
| **ActionEngine** | `ActionEngine(wm, driver)` ⚠️ | `ActionEngine.from_context()` ✅ |
| **Agent** | 直接使用ActionEngine ⚠️ | 使用WebAgent ✅ |
| **模型配置** | 硬编码OpenAI ❌ | Context机制 ✅ |
| **本地模型** | 不支持 ❌ | 支持Ollama ✅ |

---

## 🔧 实施步骤

### 步骤1: 克隆LaVague源码（已完成）

```bash
git clone https://github.com/lavague-ai/LaVague.git /tmp/lavague-source
```

### 步骤2: 创建自定义Context

**文件**: `core/crawlers/lavague_cursor_context.py`

**功能**: 支持Ollama/Cursor/OpenAI模型

### 步骤3: 重构LavagueCrawler

**文件**: `mcp_servers/crawlers/lavague_crawler.py`

**改进**:
- 使用`from_context`方法
- 使用`WebAgent`
- 支持自定义Context

### 步骤4: 测试验证

```bash
./venv/bin/python examples/lavague_cninfo_603986.py
```

---

## 📝 代码示例

### 完整示例（参照官方实现）

```python
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent
from lavague.drivers.selenium import SeleniumDriver
from core.crawlers.lavague_cursor_context import CursorContext

# 创建Context（使用Ollama）
context = CursorContext(model_type="ollama")

# 创建Driver
driver = SeleniumDriver(headless=True)

# 使用from_context创建（官方推荐方式）
action_engine = ActionEngine.from_context(context, driver)
world_model = WorldModel.from_context(context)

# 创建WebAgent（官方推荐）
agent = WebAgent(world_model, action_engine)

# 使用Agent
agent.get("http://www.cninfo.com.cn")
agent.run("搜索股票代码603986，提取最近90天的公告")
```

---

## 🎯 关键改进

### 1. 正确的API使用

**之前**:
```python
# ❌ 错误
from lavague import get_selenium_driver
driver = get_selenium_driver()
world_model = WorldModel(model="gpt-4o-mini")
```

**现在**:
```python
# ✅ 正确（参照官方源码）
from lavague.drivers.selenium import SeleniumDriver
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent

driver = SeleniumDriver(headless=True)
action_engine = ActionEngine.from_context(context, driver)
world_model = WorldModel.from_context(context)
agent = WebAgent(world_model, action_engine)
```

### 2. Context机制

**之前**: 硬编码OpenAI API

**现在**: 使用Context，支持多种模型

### 3. 本地模型支持

**之前**: 仅支持OpenAI API

**现在**: 支持Ollama本地模型，无需API密钥

---

## 🔗 参考资源

- **LaVague官方源码**: https://github.com/lavague-ai/LaVague
- **LaVague文档**: https://docs.lavague.ai
- **Ollama**: https://ollama.com
- **LlamaIndex**: https://docs.llamaindex.ai

---

**最后更新**: 2026-01-17  
**维护者**: TRQuant Team
