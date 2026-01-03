# 🚀 TRQuant 快速开始指南

## 一、新对话开始

**每次新对话必须执行**:

```python
# 执行会话初始化
session.init()
```

这会自动:
- 检查工作流状态
- 显示进行中的任务
- 显示最近日志
- 给出建议操作

---

## 二、工作目录

```
主项目路径: /home/taotao/dev/QuantTest/TRQuant
```

⚠️ **所有文件操作必须使用绝对路径！**

✅ `/home/taotao/dev/QuantTest/TRQuant/docs/xxx.md`
❌ `docs/xxx.md` (禁止)

---

## 三、常用命令

### 启动任务
```python
quick.start_task("任务名", "描述")
```

### 记录进度
```python
quick.log("dev", "完成xxx功能")
# stage: plan/dev/test/done/issue
```

### 完成任务
```python
quick.finish_task("task_xxx", "完成摘要")
```

### 遇到问题
```python
# 先搜索已有解决方案
knowledge.search("问题关键词")
learn.suggest("问题描述")

# 如果没有，创建问题
quick.issue("问题标题", "描述")
```

---

## 四、检查清单

```python
session.checklist()  # 检查是否遵循流程
```

---

*必读文档 1/5*
