# 📜 TRQuant 强制规则清单

## 🔴 绝对必须遵守

### 规则1: 会话初始化
```
每次新对话开始，必须执行 session.init
```

### 规则2: 绝对路径
```
所有文件操作必须使用绝对路径
路径必须以 /home/taotao/dev/QuantTest/TRQuant 开头
```

### 规则3: 记录日志
```
每个开发阶段必须记录日志
使用 devlog.add 或 quick.log
```

### 规则4: 完成任务
```
任务完成后必须调用 task.complete 或 quick.finish_task
```

---

## 🟡 强烈建议

### 规则5: 遇问题先搜索
```python
knowledge.search("问题关键词")
learn.suggest("问题描述")
```

### 规则6: 记录经验
```python
experience.add("解决方案", category="xxx")
knowledge.add(title, content, type="lesson")
```

### 规则7: 定期检查
```python
session.checklist()  # 检查是否遵循流程
```

---

## ⛔ 禁止事项

- ❌ 使用相对路径
- ❌ 在worktrees目录操作
- ❌ 不记录日志就完成任务
- ❌ 不检查状态就开始新任务

---

*必读文档 3/5*
