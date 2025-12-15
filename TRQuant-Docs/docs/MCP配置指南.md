# MCP服务器配置指南

> 创建时间: 2025-12-09  
> 说明: 如何配置MCP服务器到Cursor

---

## 📋 配置步骤

### 方法1: 手动创建配置文件（推荐）

1. **创建配置文件**
   ```bash
   cp .cursor/mcp.json.template .cursor/mcp.json
   ```

2. **或手动创建**
   ```bash
   mkdir -p .cursor
   # 复制模板内容到 .cursor/mcp.json
   ```

3. **验证配置**
   - 检查JSON格式是否正确
   - 确认路径是否正确

### 方法2: 通过Cursor设置界面

1. 打开Cursor设置
2. 搜索 "MCP" 或 "Model Context Protocol"
3. 找到 "MCP Servers" 配置项
4. 添加服务器配置

---

## 🔧 配置内容

### Filesystem Server

```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/home/taotao/dev/QuantTest/TRQuant"
  ]
}
```

### Git Server

```json
{
  "command": "uvx",
  "args": [
    "mcp-server-git"
  ]
}
```

### TRQuant Spec Server

```json
{
  "command": "python",
  "args": [
    "mcp_servers/spec_server.py"
  ]
}
```

### TRQuant Business Server

```json
{
  "command": "python",
  "args": [
    "extension/python/mcp_server.py"
  ]
}
```

---

## ✅ 验证配置

### 1. 检查配置文件

```bash
# 检查JSON格式
cat .cursor/mcp.json | python -m json.tool
```

### 2. 重启Cursor

- 完全关闭Cursor
- 重新打开
- 检查MCP服务器状态

### 3. 测试功能

- 在Cursor中尝试使用MCP工具
- 检查是否有错误提示
- 验证功能是否正常

---

## ⚠️ 常见问题

### 问题1: 配置文件不存在

**解决**: 手动创建 `.cursor/mcp.json` 文件

### 问题2: JSON格式错误

**解决**: 使用 `python -m json.tool` 验证格式

### 问题3: 服务器无法启动

**解决**: 
- 检查命令路径是否正确
- 检查依赖是否安装
- 查看Cursor日志

---

*创建时间: 2025-12-09*
