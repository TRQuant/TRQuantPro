# Task Optimizer Server 配置指南

> **创建时间**: 2025-12-14  
> **目的**: 配置task_optimizer_server到Cursor MCP

---

## 📋 配置步骤

### 1. 找到MCP配置文件

MCP配置文件通常位于：
- **Linux/Mac**: `~/.config/cursor/mcp.json` 或 `~/.cursor/mcp.json`
- **Windows**: `%APPDATA%\Cursor\mcp.json`

### 2. 添加task_optimizer_server配置

在MCP配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "trquant-task-optimizer": {
      "command": "python3",
      "args": [
        "/home/taotao/dev/QuantTest/TRQuant/mcp_servers/task_optimizer_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/dev/QuantTest/TRQuant"
      }
    }
  }
}
```

**注意**: 请根据实际路径修改：
- `command`: Python解释器路径（可能是`python`、`python3`或完整路径）
- `args[0]`: task_optimizer_server.py的完整路径
- `TRQUANT_ROOT`: 项目根目录的完整路径

### 3. 验证配置

```bash
# 检查JSON格式
cat ~/.config/cursor/mcp.json | python3 -m json.tool

# 测试服务器启动
python3 mcp_servers/task_optimizer_server.py
```

### 4. 重启Cursor

- 完全关闭Cursor
- 重新打开
- 检查MCP服务器状态

---

## 🧪 测试工具

### 测试1: 分析任务复杂度

在Cursor中调用：
```
task.analyze_complexity({
  "task_title": "修复MCP服务器集成",
  "file_count": 6,
  "code_complexity": "medium"
})
```

### 测试2: 获取上下文缓存

```
task.get_context({
  "file_path": "docs/PROJECT_TASK_LIST.md"
})
```

### 测试3: 优化工作流

```
task.optimize_workflow({
  "task_title": "修复MCP服务器",
  "file_paths": [
    "mcp_servers/schema_server.py",
    "mcp_servers/factor_server.py"
  ]
})
```

---

## ⚠️ 常见问题

### 问题1: 服务器无法启动

**检查**:
- Python路径是否正确
- 依赖是否安装（mcp包）
- 文件路径是否正确

**解决**:
```bash
# 检查Python
which python3

# 检查依赖
pip3 list | grep mcp

# 测试直接运行
python3 mcp_servers/task_optimizer_server.py
```

### 问题2: 工具调用失败

**检查**:
- MCP服务器是否在Cursor中显示为已连接
- 查看Cursor日志中的错误信息

**解决**:
- 重启Cursor
- 检查配置文件格式
- 查看服务器日志

---

## 📝 使用示例

### 示例1: 开始新任务前

```python
# 1. 分析任务复杂度
result = task.analyze_complexity(
    task_title="修复MCP服务器集成",
    file_count=6,
    code_complexity="medium"
)

# 2. 优化工作流
workflow = task.optimize_workflow(
    task_title="修复MCP服务器集成",
    file_paths=[
        "mcp_servers/schema_server.py",
        "mcp_servers/factor_server.py",
        "docs/MCP_INTEGRATION_BEST_PRACTICES.md"
    ]
)

# 3. 根据结果决定读取策略
if workflow["file_analysis"]["cached_count"] > 0:
    # 使用缓存
    print(f"可以复用{workflow['file_analysis']['cached_count']}个文件的缓存")
else:
    # 需要读取文件
    print("需要读取所有文件")
```

### 示例2: 缓存上下文

```python
# 读取文件后，立即缓存上下文
content = read_file("docs/PROJECT_TASK_LIST.md")

# 提取关键信息
context = {
    "summary": "项目任务列表，包含15个主要阶段",
    "key_tasks": ["MCP规范标准化", "GUI前端优化", "数据库实施"],
    "last_updated": "2025-12-14",
    "total_tasks": 100
}

# 缓存
task.cache_context(
    file_path="docs/PROJECT_TASK_LIST.md",
    context=context
)
```

---

**文档维护**: 根据实际使用情况持续更新  
**最后更新**: 2025-12-14
