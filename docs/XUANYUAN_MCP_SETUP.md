# 轩辕剑灵MCP服务器配置指南

> **创建时间**: 2026-01-03  
> **说明**: 如何配置轩辕剑灵MCP服务器到Cursor

---

## 📋 配置步骤

### 1. 找到MCP配置文件

MCP配置文件通常位于：
- **Linux/Mac**: `~/.config/cursor/mcp.json` 或 `~/.cursor/mcp.json`
- **Windows**: `%APPDATA%\Cursor\mcp.json`

### 2. 添加轩辕剑灵服务器配置

在MCP配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "xuanyuan": {
      "command": "/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python",
      "args": [
        "/home/taotao/.cursor/worktrees/TRQuant/ope/mcp_servers/xuanyuan_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/.cursor/worktrees/TRQuant/ope"
      },
      "description": "🐉 轩辕剑灵开发助手"
    }
  }
}
```

**注意**: 请根据实际路径修改：
- `command`: Python解释器路径（使用ope/venv中的Python）
- `args[0]`: xuanyuan_server.py的完整路径（位于ope目录下）
- `TRQUANT_ROOT`: ope目录的完整路径

### 3. 验证配置

```bash
# 检查JSON格式
cat ~/.cursor/mcp.json | python3 -m json.tool

# 测试服务器启动（应该等待stdio输入，不报错）
python3 mcp_servers/xuanyuan_server.py
```

### 4. 重启Cursor

- 完全关闭Cursor
- 重新打开
- 检查MCP服务器状态（Cursor设置 → MCP Servers）

---

## 🧪 测试工具

### 测试1: 列出提示词模板

在Cursor Chat中调用：
```
请调用 xuanyuan.prompt.templates.list
```

### 测试2: 创建提示词模板

```
请调用 xuanyuan.prompt.templates.create，参数：{
  "name": "系统提示词模板",
  "content": "你是一个专业的量化交易助手...",
  "category": "system",
  "tags": ["system", "prompt"]
}
```

### 测试3: 分析错误

```
请调用 xuanyuan.error.analyze，参数：{
  "error_message": "SyntaxError: invalid syntax",
  "code_context": "def test():\n    print('hello'"
}
```

### 测试4: 命令建议

```
请调用 xuanyuan.command.suggest，参数：{
  "intent": "查看当前目录的Python文件"
}
```

### 测试5: 保存上下文

```
请调用 xuanyuan.memory.save_context，参数：{
  "key": "project_config",
  "value": "使用Python 3.11，项目路径为/home/taotao/dev/QuantTest/TRQuant",
  "tags": ["config", "project"]
}
```

---

## 📊 可用工具列表

### 提示词管理 (xuanyuan.prompt.*)
- `xuanyuan.prompt.templates.list` - 列出所有模板
- `xuanyuan.prompt.templates.get` - 获取模板详情
- `xuanyuan.prompt.templates.create` - 创建新模板
- `xuanyuan.prompt.templates.update` - 更新模板
- `xuanyuan.prompt.templates.evaluate` - 评估提示词效果
- `xuanyuan.prompt.best_practices.search` - 搜索最佳实践

### 错误处理 (xuanyuan.error.*, xuanyuan.debug.*)
- `xuanyuan.error.analyze` - 分析错误
- `xuanyuan.error.suggest_fix` - 建议修复方案
- `xuanyuan.error.history` - 查看错误历史
- `xuanyuan.debug.steps` - 生成调试步骤

### 命令助手 (xuanyuan.command.*)
- `xuanyuan.command.suggest` - 命令建议
- `xuanyuan.command.explain` - 解释命令
- `xuanyuan.command.history` - 命令历史
- `xuanyuan.command.check_safety` - 安全检查

### 记忆功能 (xuanyuan.memory.*)
- `xuanyuan.memory.save_context` - 保存上下文
- `xuanyuan.memory.recall` - 回忆历史
- `xuanyuan.memory.search` - 搜索记忆
- `xuanyuan.memory.summarize` - 会话摘要

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

# 检查文件
ls -la mcp_servers/xuanyuan_server.py
```

### 问题2: 工具无法调用

**检查**:
- Cursor是否重启
- MCP服务器状态（Cursor设置 → MCP Servers）
- 查看Cursor日志

**解决**:
1. 完全关闭Cursor
2. 重新打开
3. 在Cursor Chat中尝试："请列出所有MCP工具"

### 问题3: 数据目录不存在

**说明**: 数据目录会在首次使用时自动创建：
- `data/xuanyuan/prompts/`
- `data/xuanyuan/errors/`
- `data/xuanyuan/commands/`
- `data/xuanyuan/memory/`

---

## 📝 使用示例

### 在Cursor Chat中使用

1. **列出所有提示词模板**:
   ```
   请调用 xuanyuan.prompt.templates.list
   ```

2. **创建新的提示词模板**:
   ```
   请调用 xuanyuan.prompt.templates.create，参数：{
     "name": "代码审查模板",
     "content": "请审查以下代码...",
     "category": "code_review"
   }
   ```

3. **分析错误并获取修复建议**:
   ```
   请先调用 xuanyuan.error.analyze 分析错误，然后调用 xuanyuan.error.suggest_fix 获取修复建议
   ```

4. **获取命令建议**:
   ```
   请调用 xuanyuan.command.suggest，我想查找所有Python文件
   ```

5. **保存和回忆上下文**:
   ```
   请调用 xuanyuan.memory.save_context 保存当前项目配置，然后可以用 xuanyuan.memory.recall 回忆
   ```

---

## 🔗 相关文档

- MCP服务器标准: `mcp_servers/utils/mcp_standard.py`
- 开发流程: `DevMustRead/MCP_STANDARD_DEV_WORKFLOW.md`

---

*创建时间: 2026-01-03*

