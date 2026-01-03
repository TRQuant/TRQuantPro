# 📚 TRQuant 必读文档

> **重要**: 每次开始开发前，请阅读本目录下的文档！

---

## 📋 文档索引

| 优先级 | 文档 | 说明 |
|--------|------|------|
| 🔴 必读 | `01_QUICK_START.md` | 快速开始指南 |
| 🔴 必读 | `02_DEV_WORKFLOW.md` | 标准开发流程 |
| 🔴 必读 | `03_RULES.md` | 强制规则清单 |
| 🟡 推荐 | `04_TOOLS.md` | MCP工具速查 |
| 🟡 推荐 | `05_KNOWLEDGE.md` | 知识库使用 |

---

## 🚀 快速开始

```python
# 每次新对话开始，执行：
session.init()

# 开始新任务：
quick.start_task("任务名", "描述")

# 完成任务：
quick.finish_task("task_xxx", "摘要")
```

---

## ⚠️ 最重要的规则

1. **会话初始化**: 每次新对话必须执行 `session.init`
2. **绝对路径**: 文件操作必须使用 `/home/taotao/dev/QuantTest/TRQuant/...`
3. **记录日志**: 每个阶段用 `devlog.add` 或 `quick.log` 记录
4. **遇问题先搜**: 先用 `knowledge.search` 搜索已有解决方案

---

*最后更新: 2025-12-19*
