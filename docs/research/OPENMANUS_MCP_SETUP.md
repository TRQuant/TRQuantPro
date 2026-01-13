# OpenManus MCP服务器配置指南

> **创建时间**: 2026-01-11  
> **目的**: 配置OpenManus MCP服务器到Cursor，以便在Cursor Chat中使用

---

## 📋 配置步骤

### 步骤1: 检查当前MCP配置

MCP配置文件位置: `~/.cursor/mcp.json`

当前已配置的服务器：
- quantconnect
- xuanyuan
- trquant-core
- trquant-workflow
- filesystem
- git
- kb-grounding
- kb-server
- unified-dev

### 步骤2: 添加OpenManus配置

在 `~/.cursor/mcp.json` 的 `mcpServers` 对象中添加以下配置：

```json
{
  "mcpServers": {
    ...现有配置...,
    "openmanus": {
      "command": "/home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus/.venv/bin/python",
      "args": ["-m", "app.mcp.server"],
      "env": {
        "PYTHONPATH": "/home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus",
        "PYTHONIOENCODING": "utf-8"
      },
      "description": "🌐 OpenManus - 浏览器自动化工具 (browser, bash, editor, terminate)"
    }
  }
}
```

### 步骤3: 验证配置

```bash
# 检查JSON格式
cat ~/.cursor/mcp.json | python3 -m json.tool

# 测试MCP服务器启动（应该等待stdio输入，不报错）
cd /home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus
source .venv/bin/activate
python -m app.mcp.server
```

### 步骤4: 重启Cursor

1. 完全关闭Cursor
2. 重新打开Cursor
3. 检查MCP服务器状态（Cursor设置 → MCP Servers）
4. 应该看到 "openmanus" 服务器已连接

---

## 🧪 测试使用

### 测试1: 列出可用工具

在Cursor Chat中：
```
"请列出openmanus的所有工具"
```

应该看到：
- `bash`: 命令行工具
- `browser`: 浏览器自动化工具
- `editor`: 代码编辑器工具
- `terminate`: 终止工具

### 测试2: 浏览器工具 - 访问网页

在Cursor Chat中：
```
"使用openmanus的browser工具访问 https://www.eastmoney.com"
```

### 测试3: 浏览器工具 - 搜索股票

在Cursor Chat中：
```
"使用openmanus的browser工具访问东方财富网站，搜索000001，获取当前价格"
```

**注意**: 这个操作需要多步：
1. 访问东方财富网站
2. 搜索股票代码
3. 提取价格信息

可能需要多次调用browser工具，或者需要更详细的指令。

### 测试4: 浏览器工具 - 提取内容

在Cursor Chat中：
```
"使用openmanus的browser工具，先访问 https://www.eastmoney.com，然后提取页面标题"
```

---

## 📊 工具使用说明

### Browser工具参数

OpenManus的browser工具支持以下操作（action参数）：

- `go_to_url`: 访问URL
- `click_element`: 点击元素
- `input_text`: 输入文本
- `extract_content`: 提取内容
- `scroll_down`: 向下滚动
- `scroll_up`: 向上滚动
- `web_search`: 网页搜索
- ... (其他操作)

**示例调用**:
```json
{
  "action": "go_to_url",
  "url": "https://www.eastmoney.com"
}
```

```json
{
  "action": "extract_content",
  "goal": "获取页面标题"
}
```

---

## ⚠️ 注意事项

1. **LLM API配置**: 
   - Browser工具的智能元素识别需要LLM API（可选）
   - 如果只使用基础功能（访问URL、提取内容），不需要LLM API
   - 如果需要智能识别页面元素，需要配置LLM API密钥

2. **浏览器驱动**:
   - OpenManus使用Playwright
   - Chromium浏览器驱动已安装 ✅

3. **工具名称**:
   - 在Cursor Chat中，工具名称是 `browser`（不是 `browser_use`）
   - MCP服务器注册的工具名称是简化后的名称

4. **多步操作**:
   - 复杂的操作（如"搜索股票并获取价格"）可能需要多步
   - 每步调用一次browser工具
   - 或者使用OpenManus的Agent功能（需要LLM API）

---

## 🔍 故障排查

### 问题1: MCP服务器无法启动

**检查**:
1. Python路径是否正确
2. 虚拟环境是否存在
3. 依赖是否安装

**测试**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus
source .venv/bin/activate
python -m app.mcp.server
```

### 问题2: 工具未显示

**解决**:
1. 完全重启Cursor
2. 检查Cursor日志
3. 验证MCP服务器是否正常启动

### 问题3: 工具调用失败

**检查**:
1. 工具参数是否正确
2. 浏览器驱动是否安装
3. 网络连接是否正常

---

## 📝 完整配置示例

```json
{
  "mcpServers": {
    "openmanus": {
      "command": "/home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus/.venv/bin/python",
      "args": ["-m", "app.mcp.server"],
      "env": {
        "PYTHONPATH": "/home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus",
        "PYTHONIOENCODING": "utf-8"
      },
      "description": "🌐 OpenManus - 浏览器自动化工具 (browser, bash, editor, terminate)"
    }
  }
}
```

---

**最后更新**: 2026-01-11
