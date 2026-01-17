# OpenManus功能演示指南

> **创建时间**: 2026-01-11  
> **状态**: ✅ 演示脚本已创建

---

## 📋 演示脚本

### 1. OpenManus原生功能演示

**脚本位置**: `scripts/demo_openmanus_features.py`

**功能列表**:
1. BrowserUseTool - 浏览器自动化
2. Bash - Shell命令执行
3. PythonExecute - Python代码执行
4. StrReplaceEditor - 代码编辑器
5. WebSearch - 网络搜索
6. MCP Server - MCP服务器工具
7. AskHuman - 询问用户（演示模式）
8. Terminate - 终止工具（演示模式）
9. Manus Agent - 通用AI Agent（演示模式）
10. MCP Agent - MCP服务器Agent（演示模式）
11. TRQuant集成 - 在TRQuant中使用OpenManus功能

**运行方式**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/demo_openmanus_features.py
```

---

### 2. TRQuant集成功能演示

**脚本位置**: `scripts/demo_trquant_openmanus_integration.py`

**功能列表**:
1. BrowserAgent - 浏览器自动化（TRQuant封装）
2. OpenManusAgent - OpenManus Agent封装（TRQuant简化版）
3. FinancialCollector - 财经数据收集（使用BrowserAgent）
4. WorkflowEnhancer - 工作流增强（R0/R1/R2增强）
5. 实际使用演示（可选，需要网络连接）

**运行方式**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/demo_trquant_openmanus_integration.py
```

---

## 🎯 功能详细说明

### OpenManus原生功能

#### 1. BrowserUseTool（浏览器自动化）

**位置**: `third_party/OpenManus/app/tool/browser_use_tool.py`

**支持的操作**:
- `go_to_url`: 访问网页
- `click_element`: 点击元素
- `input_text`: 输入文本
- `extract_content`: 提取内容（需要LLM API）
- `screenshot`: 截图
- `scroll_down/scroll_up`: 滚动
- `wait`: 等待
- `go_back`: 返回
- `refresh`: 刷新
- `switch_tab/open_tab/close_tab`: 标签管理

**TRQuant封装**: `core.automation.BrowserAgent`

---

#### 2. Bash（Shell命令执行）

**位置**: `third_party/OpenManus/app/tool/bash.py`

**功能**:
- 执行Shell命令
- 捕获命令输出
- 错误处理

**TRQuant替代**: 直接使用Python的`subprocess`模块

---

#### 3. PythonExecute（Python代码执行）

**位置**: `third_party/OpenManus/app/tool/python_execute.py`

**功能**:
- 执行Python代码
- 支持交互式执行
- 结果捕获
- 错误处理

**TRQuant替代**: 直接使用Python解释器

---

#### 4. StrReplaceEditor（代码编辑器）

**位置**: `third_party/OpenManus/app/tool/str_replace_editor.py`

**功能**:
- 文件编辑
- 字符串替换
- 代码修改
- 多行替换

**TRQuant替代**: 直接使用文件操作

---

#### 5. WebSearch（网络搜索）

**位置**: `third_party/OpenManus/app/tool/web_search.py`

**功能**:
- Google搜索
- Bing搜索
- 百度搜索
- DuckDuckGo搜索
- 搜索结果提取

**TRQuant替代**: `core.data_collection.FinancialCollector`

---

#### 6. MCP Server（MCP服务器工具）

**位置**: `third_party/OpenManus/app/mcp/server.py`

**注册的工具**:
- `bash`: Shell命令执行
- `browser`: 浏览器自动化
- `editor`: 代码编辑器
- `terminate`: 终止工具

**配置位置**: `~/.cursor/mcp.json`

**使用方式**: 通过Cursor Chat直接调用

---

#### 7. AskHuman（询问用户）

**位置**: `third_party/OpenManus/app/tool/ask_human.py`

**功能**:
- 询问用户输入
- 获取用户反馈
- 交互式对话

**TRQuant使用**: 在自动化脚本中可以使用默认值或跳过

---

#### 8. Terminate（终止工具）

**位置**: `third_party/OpenManus/app/tool/terminate.py`

**功能**:
- 终止Agent执行
- 任务完成标记
- 清理资源

**TRQuant使用**: 在Agent循环中，调用此工具会结束执行

---

#### 9. Manus Agent（通用AI Agent）

**位置**: `third_party/OpenManus/app/agent/manus.py`

**功能**:
- 多工具支持（PythonExecute, BrowserUseTool等）
- MCP工具集成
- 浏览器上下文管理
- 任务分解和执行
- 思考循环（需要LLM API）

**TRQuant封装**: `core.automation.OpenManusAgent`（简化版，不使用LLM推理）

---

#### 10. MCP Agent（MCP服务器Agent）

**位置**: `third_party/OpenManus/app/agent/mcp.py`

**功能**:
- 连接MCP服务器
- 使用MCP工具
- stdio/SSE传输支持
- 工具自动发现

**TRQuant替代**: `core.mcp.client.MCPClient`

---

### TRQuant集成功能

#### 1. BrowserAgent（浏览器自动化封装）

**位置**: `core/automation/browser_agent.py`

**功能**:
- `navigate`: 访问网页
- `get_content`: 获取页面内容
- `get_text`: 获取元素文本
- `screenshot`: 截图
- `get_stock_price`: 获取股票价格（东方财富）

**使用示例**:
```python
from core.automation import BrowserAgent

async with BrowserAgent(headless=True) as agent:
    result = await agent.navigate("https://www.eastmoney.com")
    if result.success:
        content_result = await agent.get_content()
        print(content_result.data['content'][:100])
```

---

#### 2. OpenManusAgent（OpenManus Agent封装）

**位置**: `core/automation/openmanus_agent.py`

**功能**:
- 任务解析和执行
- 工具调用（browser, collector等）
- 简化的Agent实现（不使用LLM推理）
- 直接工具调用

**使用示例**:
```python
from core.automation import OpenManusAgent

async with OpenManusAgent(headless=True) as agent:
    result = await agent.call_tool("browser.navigate", url="https://www.eastmoney.com")
    if result.get("success"):
        print("工具调用成功")
```

---

#### 3. FinancialCollector（财经数据收集）

**位置**: `core/data_collection/financial_collector.py`

**功能**:
- `fetch_news`: 获取财经新闻（东方财富）
- `fetch_announcements`: 获取公告（东方财富）
- `fetch_market_news`: 获取市场新闻（关键词搜索）
- MongoDB存储支持

**使用示例**:
```python
from core.data_collection import FinancialCollector

async with FinancialCollector(headless=True) as collector:
    news_result = await collector.fetch_news("eastmoney", limit=10)
    if news_result.success:
        print(f"获取到 {len(news_result.data)} 条新闻")
        for news in news_result.data[:3]:
            print(f"  - {news.get('title', 'N/A')}")
```

---

#### 4. WorkflowEnhancer（工作流增强）

**位置**: `core/workflow/openmanus_integration.py`

**功能**:
- `enhance_r0_data_source`: R0数据源检测增强
- `enhance_r1_market_trend`: R1市场趋势分析增强（使用MarketTrendAnalyzer）
- `enhance_r2_mainline`: R2主线轮动研究增强
- `enhance_r4_investment_selection`: R4投资标的筛选增强（可选）

**使用示例**:
```python
from core.workflow import WorkflowEnhancer

async with WorkflowEnhancer(headless=True) as enhancer:
    # R0数据源检测
    r0 = await enhancer.enhance_r0_data_source()
    print(f"数据源可访问: {r0.data['accessible_count']}/{r0.data['total_count']}")
    
    # R1市场趋势分析（使用MarketTrendAnalyzer - 多周期共振+HMM）
    r1 = await enhancer.enhance_r1_market_trend(index_code="000300.XSHG")
    if r1.success:
        print(f"市场趋势: {r1.data.get('trend_label', 'N/A')}")
        print(f"HMM状态: {r1.data.get('hmm_state', 'N/A')}")
        print(f"共振阶段: {r1.data.get('resonance_phase', 'N/A')}")
    
    # R2主线轮动研究
    r2 = await enhancer.enhance_r2_mainline()
    if r2.success:
        hot_topics = r2.data.get('hot_topics', [])
        print(f"热点主题: {[t['keyword'] for t in hot_topics]}")
```

---

## 🚀 运行演示

### 方式1: 运行OpenManus原生功能演示

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/demo_openmanus_features.py
```

**输出**: 展示OpenManus的各个功能模块和说明

---

### 方式2: 运行TRQuant集成功能演示

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/demo_trquant_openmanus_integration.py
```

**输出**: 展示TRQuant中封装的OpenManus功能和使用示例

---

## 📚 相关文档

- **集成完成报告**: `docs/research/OPENMANUS_INTEGRATION_COMPLETE.md`
- **集成增强报告**: `docs/research/OPENMANUS_INTEGRATION_ENHANCED.md`
- **知识库总结**: `docs/research/OPENMANUS_KB_SUMMARY.md`
- **向量RAG知识库**: `docs/research/OPENMANUS_KB_COMPLETE.md`

---

## 💡 使用建议

### 开发中使用

1. **浏览器自动化**: 使用`BrowserAgent`（封装了BrowserUseTool）
2. **数据收集**: 使用`FinancialCollector`（封装了WebSearch）
3. **工作流增强**: 使用`WorkflowEnhancer`（集成到9步工作流）
4. **MCP工具**: 通过Cursor Chat直接调用（已配置到`~/.cursor/mcp.json`）

### 注意事项

1. **LLM API**: OpenManus的完整Agent功能需要LLM API，TRQuant封装版本不需要
2. **网络连接**: 浏览器自动化和数据收集需要网络连接
3. **性能优化**: TRQuant封装版本使用了缓存和连接池等性能优化

---

**演示脚本已创建**: 2026-01-11  
**维护者**: TRQuant Team
