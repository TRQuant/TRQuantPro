# KB Grounding 快速开始

## 5分钟上手

### 1. 确保 MCP 服务器运行

```bash
# 检查 MCP 服务器
python /home/taotao/dev/QuantTest/TRQuant/mcp_servers/kb_grounding_server.py
```

### 2. 在 Cursor 中使用

**回答问题时：**
```
用户: 如何使用JQData查询财务数据？

AI: [自动调用 kb.answer_with_evidence]
    [检查证据充足性]
    [生成带引用的回答]
    [自动验证引用覆盖率]
```

**生成代码时：**
```
用户: 实现一个JQData数据获取函数

AI: [自动调用 kb.code_with_evidence]
    [获取接口契约、项目约束、反例库]
    [生成带引用的代码]
    [自动验证]
```

### 3. 引用格式

所有输出必须包含：
- `[KB:doc_id#chunk_id]` - 知识库引用
- 每个关键断言后必须有引用

### 4. 验证检查

生成后自动检查：
- 引用覆盖率 >= 0.7
- 所有技术断言都有引用
- 未通过则自动要求重写

---

## 常见问题

**Q: 证据不足怎么办？**
A: 系统会自动提示缺失信息，建议补充知识库或搜索外部文档。

**Q: 引用覆盖率不足怎么办？**
A: 系统会自动要求重写或补充引用，不能直接输出未验证内容。

**Q: 如何添加新知识？**
A: 使用 `knowledge.add` 工具添加，或使用 `crawler.search_docs` 抓取外部文档。

---

*快速开始指南 | 2025-12-20*
