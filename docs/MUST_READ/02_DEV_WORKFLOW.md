# 📋 TRQuant 标准开发流程

## 开发流程图

```
会话初始化 → 规划 → 开发 → 测试 → 完成
    │          │       │       │       │
session.init  task   devlog  test   task
              create  add    run   complete
```

---

## 阶段详解

### 1️⃣ 会话初始化 (必须)

```python
session.init()  # 自动检查状态
```

### 2️⃣ 规划阶段

```python
quick.start_task("任务名", "描述")
# 或分开执行:
task.create(title="任务名", status="in_progress")
devlog.add(content="【规划】...", tags=["planning"])
```

### 3️⃣ 开发阶段

```python
quick.log("dev", "完成功能X")
# 或:
devlog.add(content="【开发】...", tags=["development"])

# 遇到问题:
quick.issue("问题", "描述")
```

### 4️⃣ 测试阶段

```python
test.run(module="tests/test_xxx.py")
quick.log("test", "测试通过")
```

### 5️⃣ 完成阶段

```python
quick.finish_task("task_xxx", "完成摘要")
# 或:
task.complete(task_id)
devlog.add(content="【完成】...", tags=["completed"])
```

---

## 日志标签规范

| 标签 | 使用场景 |
|------|----------|
| 【规划】 | 任务规划 |
| 【开发】 | 开发进度 |
| 【测试】 | 测试结果 |
| 【完成】 | 任务完成 |
| 【问题】 | 遇到问题 |
| 【解决】 | 问题解决 |

---

*必读文档 2/5*
