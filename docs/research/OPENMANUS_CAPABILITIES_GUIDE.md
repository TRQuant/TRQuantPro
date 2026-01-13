# OpenManus 功能能力指南

> **创建时间**: 2026-01-11  
> **目的**: 详细展示OpenManus的能力和在TRQuant中的应用

---

## 📋 目录

1. [核心功能](#核心功能)
2. [在TRQuant中的应用场景](#在trquant中的应用场景)
3. [使用示例](#使用示例)
4. [集成方式](#集成方式)
5. [实际应用案例](#实际应用案例)

---

## 🎯 核心功能

### 1. 浏览器自动化 (BrowserUseTool) 🌐

**功能描述**: 基于Playwright的智能浏览器自动化工具

**核心能力**:
- ✅ **网页导航**: 访问URL、返回、刷新
- ✅ **元素交互**: 点击、输入、下拉选择、键盘操作
- ✅ **内容提取**: 根据目标提取页面内容
- ✅ **滚动操作**: 向上/向下滚动、滚动到指定文本
- ✅ **标签管理**: 打开/切换/关闭标签页
- ✅ **网页搜索**: 执行网页搜索
- ✅ **智能识别**: 使用LLM识别页面元素（需要LLM API）

**支持的操作**:
```python
actions = [
    "go_to_url",           # 访问URL
    "click_element",       # 点击元素
    "input_text",          # 输入文本
    "scroll_down",         # 向下滚动
    "scroll_up",           # 向上滚动
    "scroll_to_text",      # 滚动到文本
    "send_keys",           # 发送按键
    "get_dropdown_options", # 获取下拉选项
    "select_dropdown_option", # 选择下拉选项
    "go_back",             # 返回
    "web_search",          # 网页搜索
    "wait",                # 等待
    "extract_content",     # 提取内容
    "switch_tab",          # 切换标签
    "open_tab",            # 打开标签
    "close_tab",           # 关闭标签
]
```

**技术实现**:
- 基于 `browser-use` 库
- 使用 Playwright 作为底层引擎
- 支持智能元素识别（通过LLM）

---

### 2. 命令行工具 (Bash) 💻

**功能描述**: 执行系统Shell命令

**核心能力**:
- ✅ **命令执行**: 运行任意Shell命令
- ✅ **文件操作**: 创建、删除、移动文件
- ✅ **数据处理**: 执行数据处理脚本
- ✅ **系统调用**: 系统信息查询、进程管理

**使用场景**:
- 数据处理和转换
- 文件批量操作
- 系统维护任务
- 脚本自动化执行

---

### 3. 代码编辑器工具 (StrReplaceEditor) 📝

**功能描述**: 代码编辑和文件操作

**核心能力**:
- ✅ **文件读取**: 读取文件内容
- ✅ **代码修改**: 基于字符串替换修改代码
- ✅ **文件写入**: 保存修改后的代码
- ✅ **模板填充**: 基于模板生成代码

**使用场景**:
- 策略代码生成
- 配置文件修改
- 代码重构
- 模板填充

---

### 4. MCP服务器 (MCPServer) 🔌

**功能描述**: 提供MCP协议接口，供Cursor和其他工具调用

**核心能力**:
- ✅ **工具注册**: 注册工具到MCP服务器
- ✅ **MCP协议**: 支持标准MCP协议
- ✅ **工具调用**: 通过MCP协议调用工具
- ✅ **结果返回**: 标准化结果返回

**已注册的工具**:
- `bash`: 命令行工具
- `browser`: 浏览器自动化工具
- `editor`: 代码编辑器工具
- `terminate`: 终止工具

---

## 🎨 在TRQuant中的应用场景

### 场景1: 财经数据收集 📊

**需求**: 从财经网站获取实时行情数据和新闻信息

**使用工具**: BrowserUseTool

**工作流程**:
1. 访问东方财富网站 (`go_to_url`)
2. 搜索股票代码 (`input_text` + `click_element`)
3. 提取价格信息 (`extract_content`)
4. 保存到数据库

**示例**:
```python
# 在Cursor Chat中:
"使用openmanus的browser工具访问东方财富网站，搜索000001，获取当前价格"
```

**实际应用**:
- 实时行情数据抓取
- 新闻和公告收集
- 财务报表下载
- 宏观数据获取

---

### 场景2: 策略代码自动生成 💡

**需求**: 基于模板自动生成策略代码

**使用工具**: StrReplaceEditor

**工作流程**:
1. 读取策略模板 (`read_file`)
2. 替换策略参数 (`str_replace`)
3. 生成完整策略代码 (`write_file`)

**示例**:
```python
# 在Cursor Chat中:
"使用openmanus的editor工具，基于MA交叉策略模板，生成一个新的策略，参数为5日和20日均线"
```

**实际应用**:
- 策略参数化生成
- 批量策略创建
- 策略模板填充
- 代码重构

---

### 场景3: 数据处理自动化 🔄

**需求**: 自动化数据处理流程

**使用工具**: Bash + BrowserUseTool

**工作流程**:
1. 使用BrowserUseTool下载数据
2. 使用Bash工具执行数据处理脚本
3. 保存处理后的数据

**示例**:
```python
# 在Cursor Chat中:
"使用openmanus工具自动化执行：
1. 使用browser工具从网站下载CSV数据
2. 使用bash工具运行数据处理脚本
3. 保存处理后的数据"
```

**实际应用**:
- 数据格式转换
- 数据清洗和预处理
- 批量数据处理
- 数据导入导出

---

### 场景4: 工作流自动化 🚀

**需求**: 自动化完整的投资研究工作流

**使用工具**: 多个工具组合

**工作流程**:
1. 数据收集 (BrowserUseTool)
2. 数据处理 (Bash)
3. 策略生成 (StrReplaceEditor)
4. 结果保存

**示例**:
```python
# 在Cursor Chat中:
"使用openmanus工具自动化执行完整的策略开发流程：
1. 访问财经网站获取市场数据
2. 处理数据并计算指标
3. 生成策略代码
4. 保存到strategies目录"
```

**实际应用**:
- R0数据源检测自动化
- R1市场趋势分析数据收集
- R3因子组合开发代码生成
- R6策略开发与回测自动化

---

## 💻 使用示例

### 方式1: 在Cursor Chat中使用（推荐）✅

**前提**: 配置OpenManus MCP服务器到Cursor

**配置** (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "openmanus": {
      "command": "/home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus/.venv/bin/python",
      "args": ["-m", "app.mcp.server"],
      "env": {
        "PYTHONPATH": "/home/taotao/.cursor/worktrees/TRQuant/ope/third_party/OpenManus"
      }
    }
  }
}
```

**使用示例**:
```
用户: "使用openmanus的browser工具访问 https://www.eastmoney.com，搜索000001，获取当前价格"

Cursor: [通过MCP调用OpenManus的browser工具]
OpenManus: [执行浏览器操作]
结果: [返回股票价格信息]
```

---

### 方式2: 通过Python代码使用

**示例代码**:
```python
import sys
from pathlib import Path
import asyncio

# 添加OpenManus路径
OPENMANUS_DIR = Path(__file__).parent.parent / "third_party" / "OpenManus"
sys.path.insert(0, str(OPENMANUS_DIR))

from app.tool.browser_use_tool import BrowserUseTool

async def demo_browser():
    """演示浏览器工具使用"""
    browser = BrowserUseTool()
    
    # 访问网页
    result = await browser.execute(
        action="go_to_url",
        url="https://www.eastmoney.com"
    )
    print(f"访问结果: {result}")
    
    # 提取内容
    result = await browser.execute(
        action="extract_content",
        goal="获取页面标题"
    )
    print(f"提取结果: {result}")
    
    # 清理
    await browser.cleanup()

# 运行
asyncio.run(demo_browser())
```

---

### 方式3: 在Notebook中使用

**示例代码**:
```python
# notebooks/research/test_openmanus.ipynb
import sys
from pathlib import Path

# 添加OpenManus路径
OPENMANUS_DIR = Path.cwd().parent.parent / "third_party" / "OpenManus"
sys.path.insert(0, str(OPENMANUS_DIR))

from app.tool.browser_use_tool import BrowserUseTool
import asyncio

# 使用浏览器工具
browser = BrowserUseTool()
result = await browser.execute(
    action="go_to_url",
    url="https://www.eastmoney.com"
)
print(result)
```

---

## 🔗 集成方式

### 集成方案A: OpenManus作为MCP服务器（推荐）✅

**架构**:
```
Cursor Chat → MCP协议 → OpenManus MCP服务器 → OpenManus工具
```

**优点**:
- ✅ 已验证可以正常工作
- ✅ 可以通过Cursor Chat调用
- ✅ 工具可以直接使用（不需要LLM API）
- ✅ 无需修改OpenManus代码

**实施步骤**:
1. 配置OpenManus MCP服务器到Cursor
2. 重启Cursor
3. 在Cursor Chat中使用工具

---

### 集成方案B: 直接导入工具到TRQuant Core

**架构**:
```
TRQuant脚本 → 导入OpenManus工具 → 直接调用
```

**优点**:
- ✅ 直接使用，无需MCP协议
- ✅ 可以与TRQuant代码深度集成
- ✅ 可以在Notebook中使用

**缺点**:
- ⚠️ 需要处理依赖管理
- ⚠️ 需要确保环境兼容

**实施步骤**:
1. 在TRQuant代码中导入OpenManus工具
2. 封装成Core模块（可选）
3. 在脚本和Notebook中使用

---

## 📊 实际应用案例

### 案例1: 实时行情数据抓取

**目标**: 从东方财富网站获取实时股票价格

**步骤**:
1. 使用BrowserUseTool访问东方财富网站
2. 搜索股票代码（如000001）
3. 提取当前价格
4. 保存到数据库

**代码示例**:
```python
from app.tool.browser_use_tool import BrowserUseTool

browser = BrowserUseTool()

# 1. 访问网站
await browser.execute(action="go_to_url", url="https://www.eastmoney.com")

# 2. 搜索股票
await browser.execute(
    action="input_text",
    index=0,  # 搜索框索引
    text="000001"
)
await browser.execute(action="click_element", index=1)  # 搜索按钮

# 3. 提取价格
result = await browser.execute(
    action="extract_content",
    goal="获取股票当前价格"
)

# 4. 保存到数据库
# ... 数据库操作 ...
```

---

### 案例2: 策略代码自动生成

**目标**: 基于模板生成策略代码

**步骤**:
1. 读取策略模板
2. 替换参数（如均线周期）
3. 保存生成的策略

**代码示例**:
```python
from app.tool.str_replace_editor import StrReplaceEditor

editor = StrReplaceEditor()

# 1. 读取模板
template = editor.read_file("strategies/templates/ma_cross_template.py")

# 2. 替换参数
code = template.replace("SHORT_PERIOD = 5", "SHORT_PERIOD = 10")
code = code.replace("LONG_PERIOD = 20", "LONG_PERIOD = 30")

# 3. 保存
editor.write_file("strategies/ma_cross_custom.py", code)
```

---

### 案例3: 自动化数据更新

**目标**: 自动化执行数据更新流程

**步骤**:
1. 使用BrowserUseTool从网站下载数据
2. 使用Bash工具处理数据
3. 导入到数据库

**代码示例**:
```python
from app.tool.browser_use_tool import BrowserUseTool
from app.tool.bash import Bash

browser = BrowserUseTool()
bash = Bash()

# 1. 下载数据
await browser.execute(action="go_to_url", url="数据下载页面")
await browser.execute(action="click_element", index=0)  # 下载按钮

# 2. 处理数据
result = await bash.execute(command="python process_data.py data.csv")

# 3. 导入数据库
result = await bash.execute(command="python import_to_db.py processed_data.csv")
```

---

## 🎯 与TRQuant工作流集成

### R0: 数据源检测

**应用**: 使用BrowserUseTool检测数据源可用性

```python
# 测试数据源连接
browser = BrowserUseTool()
result = await browser.execute(
    action="go_to_url",
    url="https://www.eastmoney.com"
)
if result.success:
    print("✅ 东方财富网站可访问")
```

---

### R1: 市场趋势分析

**应用**: 使用BrowserUseTool收集市场数据和新闻

```python
# 收集市场新闻
browser = BrowserUseTool()
await browser.execute(action="go_to_url", url="新闻页面")
result = await browser.execute(
    action="extract_content",
    goal="获取最新市场新闻标题和摘要"
)
```

---

### R3: 因子组合开发

**应用**: 使用StrReplaceEditor生成因子计算代码

```python
# 生成因子计算代码
editor = StrReplaceEditor()
template = editor.read_file("factors/templates/momentum_template.py")
code = template.replace("PERIOD = 20", f"PERIOD = {factor_period}")
editor.write_file(f"factors/momentum_{factor_period}.py", code)
```

---

### R6: 策略开发与回测

**应用**: 使用StrReplaceEditor生成策略代码

```python
# 生成策略代码
editor = StrReplaceEditor()
template = editor.read_file("strategies/templates/base_strategy.py")
# ... 替换参数 ...
editor.write_file("strategies/my_strategy.py", code)
```

---

## 📝 总结

### OpenManus能做什么？

1. **浏览器自动化** ✅
   - 访问网页、点击、输入、提取内容
   - 自动化网页操作
   - 数据抓取

2. **命令行执行** ✅
   - 运行Shell命令
   - 文件操作
   - 脚本执行

3. **代码编辑** ✅
   - 代码生成
   - 文件修改
   - 模板填充

4. **MCP服务器** ✅
   - 通过Cursor Chat调用
   - 工具统一管理
   - 标准化接口

### 在TRQuant中的价值

- ✅ **增强数据收集能力**: 浏览器自动化工具可以抓取更多数据源
- ✅ **自动化工作流**: 减少手动操作，提高效率
- ✅ **代码生成**: 自动生成策略和因子代码
- ✅ **与Cursor集成**: 通过Cursor Chat使用，自然语言交互

### 下一步建议

1. **配置MCP服务器**: 将OpenManus配置到Cursor
2. **测试工具功能**: 在Cursor Chat中测试browser工具
3. **开发实际应用**: 实现财经数据抓取等实际应用
4. **集成到工作流**: 在TRQuant工作流中使用OpenManus工具

---

**最后更新**: 2026-01-11
