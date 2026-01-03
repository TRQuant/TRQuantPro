# KB Grounding 部署指南

## 📋 部署步骤

### 1. 文件位置确认

所有文件应在主项目目录：
```
/home/taotao/dev/QuantTest/TRQuant/
├── mcp_servers/
│   └── kb_grounding_server.py          # MCP 服务器
├── .cursorrules_grounding              # Cursor 规则
└── docs/
    ├── KB_GROUNDING_IMPLEMENTATION.md  # 实现方案
    ├── KB_GROUNDING_QUICK_START.md     # 快速开始
    ├── KB_GROUNDING_SUMMARY.md         # 总结
    └── KB_GROUNDING_DEPLOYMENT.md      # 本文档
```

### 2. 配置 MCP 服务器

在 Cursor 的 MCP 配置文件中添加：

**Linux/Mac**: `~/.config/cursor/mcp.json` 或 `~/.cursor/mcp.json`
**Windows**: `%APPDATA%\Cursor\mcp.json`

```json
{
  "mcpServers": {
    "kb-grounding": {
      "command": "python",
      "args": [
        "/home/taotao/dev/QuantTest/TRQuant/mcp_servers/kb_grounding_server.py"
      ],
      "env": {
        "PYTHONPATH": "/home/taotao/dev/QuantTest/TRQuant"
      }
    }
  }
}
```

### 3. 更新 Cursor 规则

**选项A：合并规则**
将 `.cursorrules_grounding` 的内容追加到 `.cursorrules`

**选项B：替换规则**
直接使用 `.cursorrules_grounding` 替换 `.cursorrules`

**选项C：引用规则**
在 `.cursorrules` 开头添加：
```markdown
# 引入 Grounding 规则
@include .cursorrules_grounding
```

### 4. 测试验证

#### 测试 MCP 服务器

```bash
cd /home/taotao/dev/QuantTest/TRQuant
source venv/bin/activate
python mcp_servers/kb_grounding_server.py
```

#### 测试工具调用

在 Cursor 中测试：
```
测试问题: "如何使用JQData查询财务数据？"
```

应该看到：
1. 自动调用 `kb.answer_with_evidence`
2. 返回 context_blocks
3. 生成带引用的回答
4. 自动验证引用覆盖率

### 5. 监控和调试

#### 查看日志

MCP 服务器日志输出到 stderr，可在 Cursor 的 MCP 日志中查看。

#### 检查覆盖率

每次生成后检查：
- `coverage >= 0.7` ✅
- `evidence_sufficient == true` ✅
- `unverified_sentences` 为空 ✅

---

## 🔧 故障排除

### 问题1: MCP 服务器无法启动

**检查：**
- Python 路径是否正确
- 依赖是否安装（`pip install mcp`）
- 文件路径是否正确

**解决：**
```bash
which python
python -c "import mcp; print(mcp.__version__)"
ls -l /home/taotao/dev/QuantTest/TRQuant/mcp_servers/kb_grounding_server.py
```

### 问题2: 工具调用失败

**检查：**
- `unified_dev_server.py` 中的知识库工具是否可用
- 知识库是否已初始化

**解决：**
```python
from mcp_servers.unified_dev_server import knowledge_search
result = knowledge_search("test")
print(result)
```

### 问题3: 引用覆盖率始终为0

**检查：**
- 生成的内容是否包含引用标记 `[KB:xxx]`
- 验证器是否正确提取引用

**解决：**
- 确保生成时添加引用标记
- 检查 `citation_pattern` 是否正确

---

## 📊 性能优化

### 1. 检索优化

- 实现 Hybrid Search（向量+关键词）
- 添加 Query Rewriting
- 使用 Reranker 精排

### 2. 缓存机制

- 缓存常见查询结果
- 缓存接口契约
- 缓存项目约束

### 3. 批量处理

- 批量检索多个问题
- 批量验证多个内容

---

## 🔄 持续改进

1. **扩充知识库**
   - 持续添加API文档
   - 添加最佳实践
   - 添加反例库

2. **优化验证**
   - 使用NLP提取关键断言
   - 更精确的匹配算法
   - 自动补充引用

3. **反馈循环**
   - 记录验证失败的情况
   - 分析未验证的句子
   - 补充缺失的知识

---

*部署指南 | 创建时间: 2025-12-20*
