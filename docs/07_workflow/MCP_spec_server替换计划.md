# spec_server.py 替换计划

> 创建时间: 2025-12-09  
> 目标: 用spec_server_v2.py替换原实现

---

## 📋 替换步骤

### Step 1: 备份原文件

```bash
cp mcp_servers/spec_server.py mcp_servers/spec_server.py.backup
```

### Step 2: 测试新实现

```bash
# 使用MCP Inspector测试
npx @modelcontextprotocol/inspector python mcp_servers/spec_server_v2.py
```

### Step 3: 替换文件

```bash
mv mcp_servers/spec_server_v2.py mcp_servers/spec_server.py
```

### Step 4: 更新配置

确保配置中使用正确的路径：
```json
{
  "trquant-spec": {
    "command": "python",
    "args": ["mcp_servers/spec_server.py"]
  }
}
```

### Step 5: 验证

- 重启Cursor
- 测试所有工具功能
- 确认无错误

---

## ⚠️ 注意事项

1. **备份原文件** - 确保可以回滚
2. **测试充分** - 确保所有功能正常
3. **更新文档** - 记录变更

---

*创建时间: 2025-12-09*
