# OpenManus 整合计划（更新版）

> **创建时间**: 2026-01-11  
> **更新时间**: 2026-01-11  
> **状态**: 根据测试结果更新

---

## 📋 测试结果总结

### ✅ 已验证的功能

1. **MCP服务器功能** ✅
   - OpenManus MCP服务器可以正常工作
   - 已配置到 `~/.cursor/mcp.json`
   - 工具已注册：`browser`, `bash`, `editor`, `terminate`

2. **Browser工具** ✅
   - 可以正常访问网页（已验证访问东方财富网站成功）
   - 基础功能（go_to_url, click_element, input_text等）不需要LLM API
   - 智能提取（extract_content）需要LLM API（可选）

3. **工具注册** ✅
   - 所有工具都可以正常创建和使用
   - 可以通过MCP协议调用

### ⚠️ 关键发现

1. **LLM API是必需的** ⚠️
   - OpenManus的Agent功能需要LLM API（用于Agent推理）
   - 智能内容提取（extract_content）需要LLM API
   - 基础浏览器操作（go_to_url, click等）不需要LLM API

2. **Cursor不提供直接LLM API** ⚠️
   - Cursor的LLM能力只能通过Cursor Chat/Composer使用
   - 无法通过Python代码直接调用Cursor的LLM

---

## 🎯 整合方案（更新）

### 方案：OpenManus作为MCP服务器 + LLM API配置（推荐）✅

**架构**:
```
用户 → Cursor Chat → MCP协议 → OpenManus MCP服务器 → OpenManus工具
                                                   ↓
                                              需要LLM API
```

**优点**:
- ✅ MCP服务器已验证可以正常工作
- ✅ 工具可以直接使用（基础功能不需要LLM API）
- ✅ 可以通过Cursor Chat调用
- ✅ 无需修改OpenManus代码
- ✅ 支持智能功能（需要配置LLM API）

**缺点**:
- ⚠️ 需要配置LLM API密钥（用于智能功能）

---

## 📋 整合步骤

### 阶段1: 基础整合（已完成）✅

#### 1.1 安装OpenManus ✅

- ✅ OpenManus已安装到 `third_party/OpenManus/`
- ✅ 虚拟环境已创建（`.venv/`）
- ✅ 依赖已安装

#### 1.2 配置MCP服务器 ✅

- ✅ OpenManus MCP服务器已配置到 `~/.cursor/mcp.json`
- ✅ 工具已注册：`browser`, `bash`, `editor`, `terminate`
- ✅ 配置格式正确

#### 1.3 测试验证 ✅

- ✅ MCP服务器可以正常创建
- ✅ Browser工具可以正常访问网页
- ✅ 基础功能可用（不需要LLM API）

---

### 阶段2: LLM API配置（下一步）🔧

#### 2.1 配置LLM API密钥

**配置文件**: `third_party/OpenManus/config/config.toml`

```toml
[llm]
model = "claude-3-7-sonnet-20250219"
base_url = "https://api.anthropic.com/v1/"
api_key = "YOUR_API_KEY"  # 需要配置API密钥
max_tokens = 8192
temperature = 0.0
```

**或者使用OpenAI**:
```toml
[llm]
model = "gpt-4"
base_url = "https://api.openai.com/v1/"
api_key = "YOUR_OPENAI_API_KEY"
max_tokens = 8192
temperature = 0.0
```

#### 2.2 验证LLM配置

**测试脚本**: 创建 `scripts/test_openmanus_llm.py`

```python
import sys
from pathlib import Path

OPENMANUS_DIR = Path(__file__).parent.parent / "third_party" / "OpenManus"
sys.path.insert(0, str(OPENMANUS_DIR))

from app.config import config

print(f"LLM配置:")
print(f"  Model: {config.llm.model}")
print(f"  API Key: {'已设置' if config.llm.api_key and config.llm.api_key != 'YOUR_API_KEY' else '未设置'}")
```

#### 2.3 测试智能功能

**测试extract_content功能**:

```python
from app.tool.browser_use_tool import BrowserUseTool

browser = BrowserUseTool()

# 1. 访问网站
await browser.execute(action="go_to_url", url="https://www.eastmoney.com")

# 2. 提取内容（需要LLM API）
result = await browser.execute(
    action="extract_content",
    goal="获取页面标题和主要新闻标题"
)
```

---

### 阶段3: 功能增强（可选）🚀

#### 3.1 封装成Core模块（可选）

**目标**: 将OpenManus工具封装成TRQuant Core模块

**位置**: `core/automation/openmanus_wrapper.py`

```python
"""
OpenManus工具封装
"""
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import asyncio

OPENMANUS_DIR = Path(__file__).parent.parent.parent / "third_party" / "OpenManus"
sys.path.insert(0, str(OPENMANUS_DIR))

from app.tool.browser_use_tool import BrowserUseTool
from app.tool.bash import Bash
from app.tool.str_replace_editor import StrReplaceEditor


class OpenManusWrapper:
    """OpenManus工具封装类"""
    
    def __init__(self):
        self.browser: Optional[BrowserUseTool] = None
        self.bash: Optional[Bash] = None
        self.editor: Optional[StrReplaceEditor] = None
    
    async def get_browser(self) -> BrowserUseTool:
        """获取浏览器工具"""
        if self.browser is None:
            self.browser = BrowserUseTool()
        return self.browser
    
    async def get_bash(self) -> Bash:
        """获取Bash工具"""
        if self.bash is None:
            self.bash = Bash()
        return self.bash
    
    async def get_editor(self) -> StrReplaceEditor:
        """获取编辑器工具"""
        if self.editor is None:
            self.editor = StrReplaceEditor()
        return self.editor
    
    async def cleanup(self):
        """清理资源"""
        if self.browser:
            await self.browser.cleanup()
```

#### 3.2 集成到TRQuant工作流（可选）

**目标**: 在TRQuant工作流中使用OpenManus工具

**应用场景**:
- R0（数据源检测）: 使用BrowserUseTool检测数据源可用性
- R1（市场趋势分析）: 使用BrowserUseTool收集市场新闻
- 数据收集: 使用BrowserUseTool抓取财经网站数据

---

### 阶段4: 实际应用开发（后续）🎯

#### 4.1 财经数据抓取

**功能**: 从东方财富、同花顺等财经网站抓取实时行情数据

**使用工具**: BrowserUseTool

**实现方式**:
1. 在Cursor Chat中: `"使用browser工具访问东方财富，搜索000001，获取当前价格"`
2. 或者通过Python脚本调用OpenManus工具
3. 数据保存到TRQuant数据库

#### 4.2 策略代码自动生成

**功能**: 基于模板自动生成策略代码

**使用工具**: StrReplaceEditor

**实现方式**:
1. 读取策略模板
2. 替换参数
3. 保存生成的策略

#### 4.3 数据处理自动化

**功能**: 自动化数据处理流程

**使用工具**: Bash + BrowserUseTool

**实现方式**:
1. 使用BrowserUseTool下载数据
2. 使用Bash工具执行数据处理脚本
3. 保存处理后的数据

---

## 🔧 配置说明

### 当前配置状态

✅ **MCP服务器配置**: 已完成
- 配置文件: `~/.cursor/mcp.json`
- 服务器: `openmanus`
- 工具: `browser`, `bash`, `editor`, `terminate`

⚠️ **LLM API配置**: 待完成
- 配置文件: `third_party/OpenManus/config/config.toml`
- 需要配置API密钥

### LLM API配置步骤

1. **选择LLM提供商**:
   - Anthropic (Claude)
   - OpenAI (GPT-4)
   - 其他支持的提供商

2. **获取API密钥**:
   - 注册账号
   - 获取API密钥

3. **配置config.toml**:
   ```toml
   [llm]
   model = "claude-3-7-sonnet-20250219"
   base_url = "https://api.anthropic.com/v1/"
   api_key = "YOUR_API_KEY"
   max_tokens = 8192
   temperature = 0.0
   ```

4. **验证配置**:
   - 运行测试脚本
   - 测试extract_content功能

---

## 📊 功能对比

### 不需要LLM API的功能 ✅

| 功能 | 说明 | 状态 |
|------|------|------|
| go_to_url | 访问网页 | ✅ 可用 |
| click_element | 点击元素 | ✅ 可用 |
| input_text | 输入文本 | ✅ 可用 |
| scroll_down/scroll_up | 滚动页面 | ✅ 可用 |
| wait | 等待 | ✅ 可用 |
| go_back | 返回 | ✅ 可用 |
| refresh | 刷新页面 | ✅ 可用 |
| switch_tab | 切换标签 | ✅ 可用 |

### 需要LLM API的功能 ⚠️

| 功能 | 说明 | 状态 |
|------|------|------|
| extract_content | 智能内容提取 | ⚠️ 需要LLM API |
| 智能元素识别 | 自动识别页面元素 | ⚠️ 需要LLM API |
| Agent框架 | 智能Agent功能 | ⚠️ 需要LLM API |

---

## 🎯 下一步行动

### 立即执行（P0）

1. **配置LLM API密钥** 🔧
   - 编辑 `third_party/OpenManus/config/config.toml`
   - 添加API密钥
   - 验证配置

2. **测试智能功能** 🧪
   - 测试extract_content功能
   - 验证LLM API是否正常工作

### 后续执行（P1）

3. **封装Core模块**（可选）📦
   - 创建 `core/automation/openmanus_wrapper.py`
   - 封装OpenManus工具
   - 提供统一接口

4. **集成到工作流**（可选）🔄
   - 在R0/R1中使用BrowserUseTool
   - 开发实际应用场景

---

## ✅ 总结

### 当前状态

1. ✅ **基础整合完成**: OpenManus MCP服务器已配置
2. ✅ **工具可用**: Browser工具已验证可用
3. ⚠️ **LLM API待配置**: 需要配置API密钥才能使用智能功能

### 推荐方案

**方案: OpenManus作为MCP服务器 + LLM API配置** ✅

**理由**:
1. ✅ MCP服务器已验证可以正常工作
2. ✅ 工具可以直接使用（基础功能不需要LLM API）
3. ✅ 支持智能功能（需要配置LLM API）
4. ✅ 无需修改OpenManus代码
5. ✅ 可以通过Cursor Chat调用

### 下一步

1. **配置LLM API密钥**（必需）
2. **测试智能功能**
3. **开发实际应用**

---

**最后更新**: 2026-01-11
