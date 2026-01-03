# 🚀 快速测试指南 - 不需要重新安装扩展

## 问题
每次修改代码都需要重新打包安装扩展，效率太低。

## ✅ 解决方案

### 方案1: F5调试模式（推荐，前端代码）

1. **在Cursor中打开扩展文件夹**
   ```bash
   cd /home/taotao/dev/QuantTest/TRQuant/extension
   ```

2. **按 `F5` 键启动调试**
   - 会自动打开新的Cursor窗口（Extension Development Host）
   - 新窗口会加载最新的代码

3. **修改代码后重新加载**
   - 在新窗口中按 `Ctrl+Shift+F5` 重新加载
   - 或关闭新窗口，在主窗口按 `F5` 重新启动

**优点**：
- ✅ 不需要重新打包安装
- ✅ 自动加载最新代码
- ✅ 可以设置断点调试
- ✅ 查看控制台输出

**缺点**：
- ⚠️ 需要两个窗口（主窗口+调试窗口）
- ⚠️ 只适用于前端TypeScript代码

---

### 方案2: 直接测试Python后端（推荐，后端代码）

创建独立测试脚本，直接测试Python功能：

```bash
# 运行快速测试脚本
cd /home/taotao/dev/QuantTest/TRQuant
venv/bin/python3 scripts/test_datasource_quick.py
```

**测试脚本位置**: `scripts/test_datasource_quick.py`

**测试内容**：
1. ✅ 直接调用数据提供者
2. ✅ 通过工作流步骤执行
3. ✅ 通过MCPClient调用
4. ✅ 通过bridge.py调用

**优点**：
- ✅ 不需要重新安装扩展
- ✅ 快速验证Python后端功能
- ✅ 可以测试所有调用路径
- ✅ 输出详细的错误信息

---

### 方案3: 使用bridge.py直接测试

```bash
# 测试数据源检查
echo '{
  "action": "call_mcp_tool",
  "params": {
    "tool_name": "workflow9.run_step",
    "arguments": {
      "workflow_id": "test-workflow",
      "step_id": "data_source",
      "args": {}
    }
  }
}' | venv/bin/python3 extension/python/bridge.py
```

**优点**：
- ✅ 模拟扩展的实际调用路径
- ✅ 可以测试完整的调用链

---

## 📋 测试清单

### 数据源检查功能测试

```bash
# 1. 直接测试Python功能
venv/bin/python3 scripts/test_datasource_quick.py

# 2. 测试bridge.py
echo '{"action": "call_mcp_tool", "params": {...}}' | venv/bin/python3 extension/python/bridge.py

# 3. 测试MCPClient
venv/bin/python3 -c "
from core.mcp.client import MCPClient
from pathlib import Path
client = MCPClient(project_root=Path.cwd())
result = client.call('workflow9.run_step', {...})
print(result)
"
```

---

## 🔍 调试技巧

### 1. 查看日志
```bash
# Python日志
tail -f logs/*.log

# 扩展日志（在Cursor中）
Ctrl+Shift+U → 选择 "TRQuant"
```

### 2. 添加调试输出
```python
# Python代码中
import logging
logger = logging.getLogger(__name__)
logger.info("调试信息")
```

### 3. 检查路径
```python
# 确认虚拟环境路径
import sys
print(sys.executable)

# 确认项目根目录
from pathlib import Path
print(Path.cwd())
```

---

## ⚠️ 常见问题

### Q1: 测试通过但扩展中不工作
**原因**: 扩展使用的是已安装的版本，不是开发目录
**解决**: 使用F5调试模式，或重新打包安装

### Q2: 模块导入错误
**原因**: Python路径不正确
**解决**: 确保使用虚拟环境中的Python，并设置正确的PYTHONPATH

### Q3: 异步事件循环冲突
**原因**: 在已有事件循环中创建新循环
**解决**: 检查是否已有循环，使用 `asyncio.get_running_loop()` 或线程池

---

## 📚 相关文档

- [扩展开发规则](../extension/development_templates_and_rules/EXTENSION_BUILD_RULES.md)
- [快速开始指南](../extension/QUICK_START.md)
- [数据源检查代码路径分析](./DATASOURCE_CHECK_ANALYSIS.md)

---

*最后更新: 2025-12-22*



























































































