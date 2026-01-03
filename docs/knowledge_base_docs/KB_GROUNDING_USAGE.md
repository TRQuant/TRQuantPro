# KB Grounding Server 调用说明

> **更新时间**: 2025-12-20

---

## 📍 服务器位置

**文件位置**:
```
/home/taotao/dev/QuantTest/TRQuant/mcp_servers/kb_grounding_server.py
```

**服务器名称**: `kb-grounding-server`

---

## 🔧 调用方式

### 1. 作为独立 MCP 服务器（推荐）

kb_grounding_server 是一个**独立的 MCP 服务器**，需要在 Cursor MCP 配置中注册。

#### 配置步骤

在 `~/.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "kb-grounding": {
      "command": "/home/taotao/dev/QuantTest/TRQuant/venv/bin/python",
      "args": [
        "/home/taotao/dev/QuantTest/TRQuant/mcp_servers/kb_grounding_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/dev/QuantTest/TRQuant"
      },
      "description": "🔍 KB Grounding - 强制基于知识库的生成工具"
    }
  }
}
```

#### 提供的工具

注册后，Cursor 可以使用以下工具：

1. **`kb.answer_with_evidence`** - 基于知识库生成回答
2. **`kb.code_with_evidence`** - 基于知识库生成代码
3. **`kb.verify_citations`** - 验证引用覆盖率

---

### 2. 通过 Cursor 规则强制调用

在 `.cursorrules` 中定义了强制调用规则：

```markdown
## 🔴 强制规则：知识库优先（KB-First）

### 1. 回答生成流程（强制）

所有回答必须遵循以下流程，不得跳过：

```
用户问题
  ↓
1. 调用 kb.answer_with_evidence(question, mode)
  ↓
2. 检查 evidence_sufficient == true
  ↓
3. 基于 context_blocks 生成回答
  ↓
4. 每个关键断言必须引用 [KB:doc_id#chunk_id]
  ↓
5. 调用 kb.verify_citations(content, evidence_ids)
```

### 2. 代码生成流程（强制）

所有代码生成必须遵循以下流程：

```
代码任务
  ↓
1. 调用 kb.code_with_evidence(task, file_path, module)
  ↓
2. 检查 evidence_sufficient == true
  ↓
3. 查看 interface_contracts（接口契约）
  ↓
4. 基于 code_templates 生成代码
  ↓
5. 调用 kb.verify_citations(code, evidence_ids)
```
```

**位置**: `.cursorrules` (第 7-53 行)

---

### 3. 在测试脚本中调用

**测试脚本**: `scripts/test_kb_grounding.py`

```python
from mcp_servers.kb_grounding_server import (
    handle_answer_with_evidence,
    handle_code_with_evidence,
    handle_verify_citations
)

# 测试
result = await handle_answer_with_evidence({
    "question": "如何使用JQData查询财务数据？",
    "mode": "code"
})
```

---

## 🔗 依赖关系

### kb_grounding_server 依赖

kb_grounding_server 从 `unified_dev_server` 导入知识库工具：

```python
from mcp_servers.unified_dev_server import (
    knowledge_search,
    knowledge_get,
    experience_search,
    practice_search,
    error_pattern_search,
    evidence_search,
    research_search,
    docs_search
)
```

**说明**: 
- kb_grounding_server 本身不存储知识库
- 它调用 unified_dev_server 中的知识库工具
- unified_dev_server 必须正常运行

---

## 📊 调用流程图

```
用户问题/代码任务
    ↓
Cursor LLM (根据 .cursorrules 规则)
    ↓
自动调用 kb.answer_with_evidence 或 kb.code_with_evidence
    ↓
kb_grounding_server (MCP 服务器)
    ↓
调用 unified_dev_server 的知识库工具
    ↓
返回证据和上下文
    ↓
Cursor LLM 生成带引用的回答/代码
    ↓
自动调用 kb.verify_citations 验证
    ↓
返回最终结果
```

---

## ⚠️ 当前状态

### 已实现

- ✅ kb_grounding_server.py 文件存在
- ✅ 工具定义完整（3个工具）
- ✅ Cursor 规则已更新（强制调用规则）
- ✅ 测试脚本可用

### 待配置

- ⚠️ **kb-grounding 服务器未在 MCP 配置中**
- ⚠️ 需要添加到 `~/.cursor/mcp.json`

---

## 🚀 快速启用

### 步骤1: 添加 MCP 配置

```bash
# 编辑 MCP 配置
nano ~/.cursor/mcp.json

# 或使用 Python 脚本添加
python3 << 'EOF'
import json

config_file = "/home/taotao/.cursor/mcp.json"

with open(config_file, 'r') as f:
    config = json.load(f)

# 添加 kb-grounding
config["mcpServers"]["kb-grounding"] = {
    "command": "/home/taotao/dev/QuantTest/TRQuant/venv/bin/python",
    "args": [
        "/home/taotao/dev/QuantTest/TRQuant/mcp_servers/kb_grounding_server.py"
    ],
    "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/dev/QuantTest/TRQuant"
    },
    "description": "🔍 KB Grounding - 强制基于知识库的生成工具"
}

# 保存
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ kb-grounding 服务器已添加到配置")
EOF
```

### 步骤2: 重启 Cursor

重启 Cursor 使配置生效。

### 步骤3: 验证

在 Cursor 中提问：
```
如何使用JQData查询财务数据？
```

应该看到：
1. 自动调用 `kb.answer_with_evidence`
2. 返回 context_blocks
3. 生成带 `[KB:xxx]` 引用的回答

---

## 📚 相关文档

- `docs/KB_GROUNDING_IMPLEMENTATION.md` - 完整实现方案
- `docs/KB_GROUNDING_QUICK_START.md` - 快速开始指南
- `docs/KB_GROUNDING_DEPLOYMENT.md` - 部署指南
- `docs/KB_GROUNDING_COMPLETE.md` - 完整方案文档

---

*KB Grounding Server 调用说明 | 创建时间: 2025-12-20*

