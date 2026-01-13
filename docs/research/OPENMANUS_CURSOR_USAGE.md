# 在Cursor Chat中使用OpenManus

> **创建时间**: 2026-01-11  
> **目的**: 指导如何在Cursor Chat中使用OpenManus的browser工具

---

## ✅ 配置状态

✅ OpenManus MCP服务器已配置到 `~/.cursor/mcp.json`  
✅ 工具已注册: `browser`, `bash`, `editor`, `terminate`  
✅ JSON配置格式正确

---

## 🔧 使用方式

### 方式1: 直接在Cursor Chat中使用（推荐）

**注意**: OpenManus的MCP服务器工具名称就是 `browser`，不需要前缀 `openmanus.`

在Cursor Chat中直接说：
```
"使用browser工具访问 https://www.eastmoney.com"
```

或者：
```
"使用browser工具，action参数为go_to_url，url为https://www.eastmoney.com"
```

Cursor会自动识别并调用OpenManus的browser工具。

---

### 方式2: 指定工具名称（如果需要）

如果Cursor没有自动识别，可以明确指定：
```
"调用MCP工具browser，访问 https://www.eastmoney.com"
```

---

## 📋 Browser工具参数

### 访问网页 (go_to_url)

**在Cursor Chat中**:
```
"使用browser工具访问 https://www.eastmoney.com"
```

**参数**:
- `action`: `"go_to_url"`
- `url`: `"https://www.eastmoney.com"`

---

### 搜索股票并获取价格（多步操作）

**步骤1: 访问网站**
```
"使用browser工具，action为go_to_url，url为https://www.eastmoney.com"
```

**步骤2: 提取内容**
```
"使用browser工具，action为extract_content，goal为获取页面标题"
```

**注意**: 复杂的多步操作需要分步执行。每步调用一次browser工具，browser工具会保持会话状态。

---

### 常用操作示例

#### 1. 访问网页
```
"使用browser工具访问 https://www.eastmoney.com"
```

#### 2. 提取页面内容
```
"使用browser工具提取当前页面的标题和主要内容"
```

参数:
- `action`: `"extract_content"`
- `goal`: `"获取页面标题和主要内容"`

#### 3. 网页搜索
```
"使用browser工具搜索'000001 股票价格'"
```

参数:
- `action`: `"web_search"`
- `query`: `"000001 股票价格"`

#### 4. 点击元素
```
"使用browser工具点击页面上的搜索按钮"
```

参数:
- `action`: `"click_element"`
- `index`: `0` (元素索引)

---

## 🔍 如何查看可用工具

在Cursor Chat中：
```
"列出所有可用的MCP工具"
```

或者：
```
"显示openmanus服务器的工具列表"
```

---

## ⚠️ 注意事项

1. **工具名称**: 
   - 在Cursor中，工具名称是 `browser`（不是 `openmanus.browser`）
   - OpenManus的MCP服务器已经将工具注册为标准MCP工具

2. **多步操作**:
   - 复杂操作需要分步执行
   - browser工具会保持会话状态
   - 每步调用一次工具

3. **LLM API（可选）**:
   - 基础功能（访问URL、提取内容）不需要LLM API
   - 智能元素识别需要LLM API（可选）

4. **浏览器驱动**:
   - OpenManus使用Playwright
   - Chromium浏览器驱动已安装 ✅

---

## 🧪 测试步骤

### 1. 重启Cursor

完全关闭并重新打开Cursor，确保MCP服务器配置已加载。

### 2. 验证MCP服务器

在Cursor设置中查看MCP Servers，应该看到 `openmanus` 服务器已连接。

### 3. 测试工具调用

在Cursor Chat中：
```
"使用browser工具访问 https://www.eastmoney.com"
```

如果工具正常，Cursor会：
1. 识别需要调用browser工具
2. 通过MCP协议调用OpenManus的browser工具
3. 执行浏览器操作
4. 返回结果

---

## 📝 完整使用示例

### 示例: 访问东方财富并获取股票价格

**在Cursor Chat中**:
```
"使用browser工具完成以下任务：
1. 访问 https://www.eastmoney.com
2. 提取页面标题
3. 搜索000001
4. 获取股票当前价格"
```

Cursor会分步执行：
1. 调用browser工具，action=go_to_url, url=https://www.eastmoney.com
2. 调用browser工具，action=extract_content, goal=获取页面标题
3. 调用browser工具，action=web_search, query=000001
4. 调用browser工具，action=extract_content, goal=获取股票当前价格

---

## 🎯 如果工具没有自动识别

如果Cursor没有自动识别browser工具，可以：

1. **明确指定工具**:
   ```
   "调用MCP工具browser"
   ```

2. **检查MCP服务器状态**:
   - Cursor设置 → MCP Servers
   - 确认openmanus服务器已连接

3. **查看Cursor日志**:
   - 检查是否有错误信息
   - 验证MCP服务器是否正常启动

4. **手动测试MCP服务器**:
   ```bash
   cd /home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus
   source .venv/bin/activate
   python -m app.mcp.server
   ```
   应该看到服务器启动，等待stdio输入。

---

## 📚 相关文档

- **快速开始**: `docs/research/OPENMANUS_QUICK_START.md`
- **功能指南**: `docs/research/OPENMANUS_CAPABILITIES_GUIDE.md`
- **MCP配置**: `docs/research/OPENMANUS_MCP_SETUP.md`
- **使用示例**: `docs/research/OPENMANUS_USAGE_EXAMPLES.md`

---

**最后更新**: 2026-01-11
