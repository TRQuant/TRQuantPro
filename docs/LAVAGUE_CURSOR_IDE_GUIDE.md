# LaVague Cursor IDE 专用集成指南

> **创建时间**: 2026-01-17  
> **版本**: v2.0 - Cursor IDE专用版  
> **参考**: https://github.com/lavague-ai/LaVague

---

## 📋 概述

本指南专为在**Cursor IDE**中使用LaVague设计，完全参照LaVague官方源码实现，解决了之前频繁出现的错误。

### 核心特点

- ✅ **专为Cursor IDE设计** - 通过MCP工具调用，使用Cursor内置AI能力
- ✅ **完全参照官方实现** - 使用正确的API和Context机制
- ✅ **无需API密钥** - 在Cursor IDE中自动使用Cursor内置AI（除非使用OpenAI模式）
- ✅ **简化配置** - 移除Ollama等本地模型依赖

---

## 🎯 在Cursor IDE中的使用方式

### 方式1: 通过MCP工具调用（推荐）

在Cursor Chat中直接使用：

```
使用crawler.lavague.execute工具，执行以下指令：
访问巨潮资讯网，搜索股票代码603986，提取最近90天的所有公告
```

**优势**:
- ✅ 自动使用Cursor内置AI能力
- ✅ 无需配置API密钥
- ✅ 无缝集成到Cursor工作流

### 方式2: 在代码中直接调用

```python
from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

# 在Cursor IDE中使用（默认使用Cursor内置AI）
crawler = get_lavague_crawler(headless=True, use_openai=False)

# 导航到网页
crawler.navigate("http://www.cninfo.com.cn")

# 执行指令
result = crawler.execute_instruction(
    "访问巨潮资讯网，搜索股票代码603986，提取最近90天的所有公告",
    max_actions=20
)

# 关闭
crawler.close()
```

---

## 🔧 安装和配置

### 1. 安装LaVague

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python -m pip install lavague
```

### 2. 安装OpenAI Context（可选，仅当使用OpenAI模式时）

```bash
./venv/bin/python -m pip install lavague-contexts-openai
```

### 3. 验证安装

```bash
./venv/bin/python -c "
from lavague.core import ActionEngine, WorldModel
from lavague.drivers.selenium import SeleniumDriver
from lavague.core.agents import WebAgent
print('✅ LaVague安装成功')
"
```

---

## 📝 完整示例

### 示例1: 提取股票公告（Cursor IDE模式）

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""使用LaVague提取股票公告（Cursor IDE模式）"""

from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

def extract_announcements_cursor():
    """在Cursor IDE中使用LaVague提取公告"""
    
    # 创建爬虫（Cursor IDE模式，使用Cursor内置AI）
    crawler = get_lavague_crawler(headless=True, use_openai=False)
    
    if not crawler.agent:
        print("❌ LaVague未正确初始化")
        print("请确保：")
        print("1. 已安装LaVague: pip install lavague")
        print("2. 在Cursor IDE中运行此脚本")
        return
    
    # 执行指令
    instruction = """
    访问巨潮资讯网（http://www.cninfo.com.cn），
    搜索股票代码603986，
    提取最近90天的所有公告，
    包括标题、日期、类型、链接
    """
    
    print("正在执行指令（使用Cursor内置AI）...")
    result = crawler.execute_instruction(instruction, max_actions=20)
    
    if result.get("success"):
        print("✅ 执行成功")
        print(f"结果: {result.get('result', '')[:500]}...")
    else:
        print(f"❌ 执行失败: {result.get('error')}")
    
    crawler.close()

if __name__ == "__main__":
    extract_announcements_cursor()
```

### 示例2: 使用OpenAI API（备选）

```python
# 需要设置OPENAI_API_KEY
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"

# 使用OpenAI模式
crawler = get_lavague_crawler(headless=True, use_openai=True)
result = crawler.execute_instruction("执行任务")
```

---

## 🏗️ 架构说明

### Cursor IDE集成架构

```
┌─────────────────────────────────────────┐
│  Cursor IDE                              │
│  ┌───────────────────────────────────┐ │
│  │  Cursor Chat/Composer               │ │
│  │  (使用内置AI能力)                    │ │
│  └──────────────┬──────────────────────┘ │
│                 │ MCP Protocol            │
│                 ↓                          │
│  ┌───────────────────────────────────┐   │
│  │  TRQuant MCP Server                │   │
│  │  (crawler.lavague.execute)         │   │
│  └──────────────┬──────────────────────┘   │
└─────────────────┼──────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  LavagueCrawler                         │
│  - 使用WebAgent                          │
│  - 使用CursorContext                     │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  LaVague官方实现                        │
│  - ActionEngine.from_context()          │
│  - WorldModel.from_context()            │
│  - SeleniumDriver                       │
└─────────────────────────────────────────┘
```

### 关键改进

| 方面 | 之前实现 | Cursor IDE专用版 |
|------|---------|-----------------|
| **模型支持** | Ollama/OpenAI | Cursor内置AI（默认） |
| **API密钥** | 必需（Ollama除外） | 不需要（Cursor模式） |
| **配置复杂度** | 高（需要安装Ollama） | 低（仅需LaVague） |
| **集成方式** | 直接调用 | MCP工具调用 |
| **使用场景** | 通用 | Cursor IDE专用 |

---

## 🔍 故障排除

### 问题1: LaVague未初始化

**错误**: `LaVague Agent未初始化`

**解决方案**:
1. 检查LaVague是否安装: `pip show lavague`
2. 确保在Cursor IDE中运行
3. 如果使用OpenAI模式，检查OPENAI_API_KEY是否设置

### 问题2: 导入错误

**错误**: `cannot import name 'get_selenium_driver'`

**解决方案**:
- ✅ 已修复：使用正确的导入方式 `SeleniumDriver`
- ✅ 使用 `from_context` 方法

### 问题3: WorldModel初始化错误

**错误**: `WorldModel.__init__() got an unexpected keyword argument 'model'`

**解决方案**:
- ✅ 已修复：`WorldModel()`不需要参数，使用Context配置

---

## 📊 对比：重构前后

| 特性 | 重构前 | Cursor IDE专用版 |
|------|--------|-----------------|
| **导入方式** | ❌ 错误 | ✅ 正确（参照官方） |
| **WorldModel** | ❌ 错误 | ✅ 正确（from_context） |
| **模型支持** | ❌ 仅OpenAI | ✅ Cursor内置AI |
| **API密钥** | ❌ 必需 | ✅ 不需要（Cursor模式） |
| **配置复杂度** | ❌ 高（Ollama） | ✅ 低（仅LaVague） |
| **使用场景** | ⚠️ 通用 | ✅ Cursor IDE专用 |

---

## 🔗 相关文档

- **LaVague官方文档**: https://docs.lavague.ai
- **LaVague GitHub**: https://github.com/lavague-ai/LaVague
- **TRQuant MCP工具**: `docs/MCP_SERVERS_LIST.md`

---

## 📝 实施步骤

### 步骤1: 安装依赖

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 安装LaVague
./venv/bin/python -m pip install lavague
```

### 步骤2: 在Cursor IDE中测试

在Cursor Chat中：

```
使用crawler.lavague.execute工具，执行以下指令：
访问巨潮资讯网，搜索股票代码603986，提取最近90天的所有公告
```

### 步骤3: 验证

```bash
./venv/bin/python examples/lavague_cninfo_603986.py
```

---

**最后更新**: 2026-01-17  
**维护者**: TRQuant Team
