# AI模型快速参考

## 📌 默认模式

**Auto Mode (Claude Sonnet)** - 大部分任务都用这个

---

## 🚀 使用流程

```
1. 开始任务
   ↓
2. 运行评估: python scripts/task_evaluator.py
   ↓
3. 查看建议:
   ├─ 建议 Auto → ✅ 直接继续
   └─ 建议 Max  → ⚠️  切换到 Max Mode 后继续
```

---

## 🎯 快速决策

| 任务类型 | 推荐模式 | 操作 |
|---------|---------|------|
| 架构设计、算法开发 | 🔥 Max Mode | 切换到 Max Mode |
| 功能实现、文档、UI | ⚡ Auto Mode | ✅ 直接用（默认） |
| 小修改、格式化 | ⚡⚡ Fast Mode | 可用 Auto 或 Fast |

---

## 📋 模型说明

### 🔥 Max Mode (Claude Opus 4.5)
- **最强大**，用于复杂任务
- 架构设计、算法开发、疑难Bug

### ⚡ Auto Mode (Claude Sonnet) - 默认
- **平衡效率**，用于大部分任务
- 功能实现、文档、测试、UI

### ⚡⚡ Fast Mode (Claude Haiku)
- **最快最便宜**，用于简单任务
- 格式化、查询、小修改

---

## ⚠️ 重要提示

- **不支持自动切换** - 需要手动在 Cursor 中切换
- **默认 Auto Mode** - 大部分任务直接用即可
- **遇到困难时** - 从 Auto 升级到 Max Mode

---

*详细文档: `docs/AI_MODEL_STRATEGY.md`*

