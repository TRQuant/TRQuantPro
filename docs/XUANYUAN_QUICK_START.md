# 轩辕剑灵快速开始指南

> **创建时间**: 2026-01-03  
> **说明**: 轩辕剑灵开发助手的快速使用指南

---

## 🚀 快速开始

### 1. 配置MCP服务器

编辑 `~/.cursor/mcp.json`，添加或更新配置：

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

### 2. 重启Cursor

完全关闭Cursor，然后重新打开。

### 3. 验证服务器

在Cursor Chat中尝试：
```
请列出所有MCP工具，特别是xuanyuan开头的工具
```

---

## 📝 使用示例

### 提示词管理

#### 列出所有模板
```
请调用 xuanyuan.prompt.templates.list
```

#### 创建新模板
```
请调用 xuanyuan.prompt.templates.create，参数：{
  "name": "代码审查模板",
  "content": "请审查以下代码，重点关注：\n1. 代码质量\n2. 性能优化\n3. 安全性",
  "category": "code_review",
  "tags": ["code", "review"]
}
```

#### 获取模板详情
```
请调用 xuanyuan.prompt.templates.get，参数：{
  "template_id": "tmpl_20260103_180230_abc123"
}
```

#### 搜索最佳实践
```
请调用 xuanyuan.prompt.best_practices.search，参数：{
  "query": "代码生成"
}
```

---

### 错误处理

#### 分析错误
```
请调用 xuanyuan.error.analyze，参数：{
  "error_message": "NameError: name 'x' is not defined",
  "code_context": "def test():\n    print(x)"
}
```

#### 获取修复建议
```
先调用 xuanyuan.error.analyze 分析错误，然后使用返回的error_id调用 xuanyuan.error.suggest_fix
```

#### 查看错误历史
```
请调用 xuanyuan.error.history，参数：{
  "limit": 10,
  "error_type": "name"
}
```

#### 生成调试步骤
```
请调用 xuanyuan.debug.steps，参数：{
  "error_message": "ImportError: No module named 'xxx'",
  "code_context": "import xxx"
}
```

---

### 命令助手

#### 获取命令建议
```
请调用 xuanyuan.command.suggest，参数：{
  "intent": "查找所有Python文件"
}
```

#### 解释命令
```
请调用 xuanyuan.command.explain，参数：{
  "command": "ls -lah | grep .py"
}
```

#### 检查命令安全性
```
请调用 xuanyuan.command.check_safety，参数：{
  "command": "rm -rf /tmp/test"
}
```

#### 查看命令历史
```
请调用 xuanyuan.command.history，参数：{
  "limit": 20
}
```

---

### 记忆功能

#### 保存上下文
```
请调用 xuanyuan.memory.save_context，参数：{
  "key": "project_config",
  "value": "使用Python 3.11，项目路径为/home/taotao/dev/QuantTest/TRQuant",
  "tags": ["config", "project"]
}
```

#### 回忆上下文
```
请调用 xuanyuan.memory.recall，参数：{
  "key": "project_config"
}
```

#### 搜索记忆
```
请调用 xuanyuan.memory.search，参数：{
  "query": "项目配置",
  "limit": 10
}
```

#### 会话摘要
```
请调用 xuanyuan.memory.summarize
```

---

## 🔧 测试服务器

运行测试脚本验证服务器功能：

```bash
cd /home/taotao/dev/QuantTest/TRQuant
python scripts/test_xuanyuan_server.py
```

---

## 📚 完整工具列表

### 提示词管理 (6个工具)
- `xuanyuan.prompt.templates.list` - 列出所有模板
- `xuanyuan.prompt.templates.get` - 获取模板详情
- `xuanyuan.prompt.templates.create` - 创建新模板
- `xuanyuan.prompt.templates.update` - 更新模板
- `xuanyuan.prompt.templates.evaluate` - 评估提示词效果
- `xuanyuan.prompt.best_practices.search` - 搜索最佳实践

### 错误处理 (4个工具)
- `xuanyuan.error.analyze` - 分析错误
- `xuanyuan.error.suggest_fix` - 建议修复方案
- `xuanyuan.error.history` - 查看错误历史
- `xuanyuan.debug.steps` - 生成调试步骤

### 命令助手 (4个工具)
- `xuanyuan.command.suggest` - 命令建议
- `xuanyuan.command.explain` - 解释命令
- `xuanyuan.command.history` - 命令历史
- `xuanyuan.command.check_safety` - 安全检查

### 记忆功能 (4个工具)
- `xuanyuan.memory.save_context` - 保存上下文
- `xuanyuan.memory.recall` - 回忆历史
- `xuanyuan.memory.search` - 搜索记忆
- `xuanyuan.memory.summarize` - 会话摘要

**总计**: 18个MCP工具

---

## 💡 使用技巧

1. **直接对话**: 在Cursor Chat中直接说"请调用 xxx"，AI会自动调用相应的工具
2. **参数传递**: 复杂参数可以使用JSON格式
3. **错误处理**: 先分析错误，再获取修复建议
4. **模板管理**: 创建常用提示词模板，提高效率
5. **上下文记忆**: 保存重要的项目配置和约定，方便后续回忆

---

## ⚠️ 常见问题

### 问题1: 工具无法调用

**解决**:
1. 检查MCP配置是否正确
2. 确认已重启Cursor
3. 查看Cursor日志确认服务器是否启动

### 问题2: 数据目录不存在

**说明**: 数据目录会在首次使用时自动创建在 `data/xuanyuan/`

### 问题3: 工具返回错误

**解决**: 查看错误信息，确认参数格式是否正确

---

## 🔗 相关文档

- 配置指南: `docs/XUANYUAN_MCP_SETUP.md`
- 服务器代码: `mcp_servers/xuanyuan_server.py`
- 测试脚本: `scripts/test_xuanyuan_server.py`

---

*创建时间: 2026-01-03*

