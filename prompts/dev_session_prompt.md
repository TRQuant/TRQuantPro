# TRQuant 开发会话 Prompt

## 使用方法

复制以下内容到新对话开始时发送给Cursor：

---

## Prompt模板

```
我要开始TRQuant项目的开发工作。请按照标准开发流程执行：

1. 首先执行会话初始化：
   - workflow.check - 检查开发流程状态
   - task.list(status="in_progress") - 查询进行中任务
   - devlog.list(limit=5) - 查询最近日志

2. 工作目录: /home/taotao/dev/QuantTest/TRQuant
   - 所有文件操作使用绝对路径

3. 可用文档:
   - docs/MCP_STANDARD_DEV_WORKFLOW.md - 完整开发流程
   - docs/UNIFIED_DEV_SERVER.md - 68个MCP工具说明

4. 我的任务: [在这里描述你的任务]
```

---

## 快速开发 Prompt

```
请在TRQuant项目中执行以下任务:

任务: [描述]

要求:
1. 先执行 workflow.check 检查状态
2. 创建任务: task.create
3. 记录日志: devlog.add
4. 完成后: task.complete

工作目录: /home/taotao/dev/QuantTest/TRQuant
```

---

## 继续开发 Prompt

```
继续TRQuant开发会话。

1. 查询当前状态:
   - task.list(status="in_progress")
   - devlog.list(limit=3)

2. 上次进度: [描述]

3. 本次目标: [描述]

工作目录: /home/taotao/dev/QuantTest/TRQuant
```

---

## GUI开发 Prompt

```
我要开发TRQuant的GUI界面。

1. 先检查面板状态: panel.list
2. 生成HTML模板: gui.generate_html
3. 验证CSP: gui.check_csp

要求:
- 参考 docs/GUI_DEVELOPMENT_SOLUTION.md
- 使用统一开发服务器的gui.*工具
- 所有文件使用绝对路径

任务: [描述GUI需求]
```

---

*最后更新: 2025-12-19*
