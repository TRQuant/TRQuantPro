# KB Grounding 完整方案 - 减少LLM幻觉

> **完成时间**: 2025-12-20  
> **目标**: 让 Cursor LLM 稳定使用 KB + RAG，显著降低幻觉

---

## ✅ 已创建文件

### 1. MCP 服务器
- **`mcp_servers/kb_grounding_server.py`** (19KB)
  - `kb.answer_with_evidence` - 基于知识库生成回答
  - `kb.code_with_evidence` - 基于知识库生成代码
  - `kb.verify_citations` - 验证引用覆盖率

### 2. Cursor 规则
- **`.cursorrules_grounding`** (6.8KB)
  - 强制检索流程
  - 引用格式规范
  - 验证检查清单

### 3. 文档
- **`docs/KB_GROUNDING_IMPLEMENTATION.md`** - 完整实现方案
- **`docs/KB_GROUNDING_QUICK_START.md`** - 快速开始指南
- **`docs/KB_GROUNDING_SUMMARY.md`** - 方案总结
- **`docs/KB_GROUNDING_DEPLOYMENT.md`** - 部署指南
- **`docs/KB_GROUNDING_COMPLETE.md`** - 本文档

---

## 🏗️ 核心架构

### 三层架构

```
编排层 (Cursor/Agent)
  ↓ 强制调用检索工具
检索层 (RAG)
  ↓ 多源检索 + 混合搜索
生成层 (LLM)
  ↓ 约束生成 + 引用绑定
验证层 (Verifier)
  ↓ 覆盖率检查
```

### 核心机制

1. **Tool-first 强制检索**
   - 所有生成前必须先调用 `kb.answer_with_evidence` 或 `kb.code_with_evidence`
   - 未检索到足够证据 → 拒绝生成或明确说明缺失

2. **Citation-locked 证据绑定**
   - 每个关键断言必须带引用标记 `[KB:doc_id#chunk_id]`
   - 无法给出引用 → 标记为假设或拒绝输出

3. **Post-hoc 验证**
   - 生成后自动调用 `kb.verify_citations` 验证引用覆盖率
   - coverage < 0.7 → 自动要求重写

---

## 📊 返回 JSON 规范

### `kb.answer_with_evidence` 返回

```json
{
  "context_blocks": [
    {
      "id": "kb_xxx",
      "title": "标题",
      "snippet": "相关片段",
      "source": "knowledge_base",
      "confidence": 0.95,
      "type": "knowledge|experience|practice|error_pattern"
    }
  ],
  "constraints": ["必须遵守的约束"],
  "unknowns": ["缺失的信息"],
  "recommended_actions": ["下一步建议"],
  "citation_format": "[KB:{doc_id}#{chunk_id}]",
  "evidence_sufficient": true,
  "evidence_count": 5,
  "min_required": 3
}
```

### `kb.code_with_evidence` 返回

```json
{
  "context_blocks": [...],
  "interface_contracts": [
    {
      "function": "get_fundamentals",
      "signature": "get_fundamentals(query_object, date=None)",
      "source": "kb_xxx"
    }
  ],
  "project_constraints": [
    "所有文件路径必须使用绝对路径",
    "JQData finance表必须使用正确的查询方法"
  ],
  "anti_patterns": [
    {
      "pattern": "错误模式",
      "solution": "正确做法",
      "source": "error_pattern_xxx"
    }
  ],
  "code_templates": [...],
  "evidence_sufficient": true
}
```

### `kb.verify_citations` 返回

```json
{
  "coverage": 0.85,
  "verified_citations": ["kb_xxx"],
  "unverified_sentences": [
    {
      "sentence": "关键断言",
      "reason": "包含技术术语但无引用"
    }
  ],
  "pass": true,
  "min_coverage": 0.7
}
```

---

## 🚀 快速开始

### 1. 配置 MCP 服务器

在 Cursor 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "kb-grounding": {
      "command": "python",
      "args": [
        "/home/taotao/dev/QuantTest/TRQuant/mcp_servers/kb_grounding_server.py"
      ]
    }
  }
}
```

### 2. 更新 Cursor 规则

将 `.cursorrules_grounding` 的内容合并到 `.cursorrules`

### 3. 测试

在 Cursor 中提问：
```
如何使用JQData查询财务数据？
```

应该看到：
1. 自动调用 `kb.answer_with_evidence`
2. 返回 context_blocks
3. 生成带引用的回答
4. 自动验证引用覆盖率

---

## 📈 预期效果

### 指标

- **引用覆盖率**: `coverage >= 0.7` (目标: 90%+)
- **证据充足率**: `evidence_sufficient == true` 的比例 (目标: 80%+)
- **幻觉减少率**: 无引用断言的数量减少 (目标: 70%+)

### 监控

- 记录每次生成的 `coverage`
- 记录 `evidence_sufficient == false` 的情况
- 记录 `unverified_sentences` 的数量

---

## 🔄 持续改进

### 短期（两周内）

1. ✅ 实现基础工具（已完成）
2. ⏳ 配置 MCP 服务器
3. ⏳ 更新 Cursor 规则
4. ⏳ 测试验证

### 中期（一个月内）

1. 优化检索（Hybrid Search、Query Rewriting、Reranker）
2. 扩充知识库（API文档、最佳实践、反例库）
3. 细化验证（NLP提取关键断言）

### 长期（持续）

1. 反馈循环（记录失败情况，补充知识库）
2. 自动化测试（覆盖率监控）
3. 性能优化（缓存、批量处理）

---

## 📚 相关文档

- `KB_GROUNDING_IMPLEMENTATION.md` - 完整实现方案
- `KB_GROUNDING_QUICK_START.md` - 快速开始指南
- `KB_GROUNDING_SUMMARY.md` - 方案总结
- `KB_GROUNDING_DEPLOYMENT.md` - 部署指南

---

## 🎯 关键要点

1. **强制检索**: 所有生成前必须先检索
2. **引用绑定**: 每个关键断言必须有引用
3. **自动验证**: 生成后自动检查覆盖率
4. **拒绝编造**: 证据不足时明确说明，不编造

---

*完整方案文档 | 创建时间: 2025-12-20*
