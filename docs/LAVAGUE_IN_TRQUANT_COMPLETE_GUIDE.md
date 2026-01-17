# LaVague 在 TRQuant 量化系统中的完整应用指南

> **创建时间**: 2026-01-17  
> **版本**: v1.0  
> **数据来源**: LaVague官方文档爬取 + TRQuant系统分析

---

## 📋 目录

1. [LaVague 简介](#lavague-简介)
2. [LaVague 核心功能](#lavague-核心功能)
3. [在 TRQuant 中的应用场景](#在-trquant-中的应用场景)
4. [实际应用案例](#实际应用案例)
5. [集成方案](#集成方案)
6. [使用指南](#使用指南)
7. [最佳实践](#最佳实践)

---

## 🎯 LaVague 简介

### 什么是 LaVague？

**LaVague** (Large Action Model Framework) 是一个开源框架，用于开发 **AI 驱动的 Web Agents**。

- **官网**: https://www.lavague.ai
- **文档**: https://docs.lavague.ai
- **GitHub**: https://github.com/lavague-ai/LaVague
- **许可证**: Apache-2.0
- **Python要求**: 3.10+

### 核心定位

LaVague 可以执行这样的任务：**给定一个目标（objective），自动在网页上执行一系列动作来达成该目标**。

---

## 🔧 LaVague 核心功能

### 1. 三大核心组件

#### 1.1 WorldModel（世界模型）

**功能**: 接受全局目标 + 当前页面状态 → 输出下一步动作指令

**特点**:
- 使用多模态模型理解页面内容
- 使用LLM生成动作指令
- 支持自定义模型（OpenAI、Gemini、Azure、Fireworks等）

**示例**:
```python
from lavague.core import WorldModel

world_model = WorldModel(model="gpt-4o-mini")
# 理解页面状态，生成下一步动作
```

#### 1.2 ActionEngine（动作引擎）

**功能**: 将 WorldModel 的指令编译成实际可执行代码（Selenium/Playwright），并执行

**特点**:
- 支持 Selenium 和 Playwright 驱动
- 自动生成可执行代码
- 支持自定义动作

**示例**:
```python
from lavague.core import ActionEngine
from lavague.drivers.selenium import SeleniumDriver

driver = SeleniumDriver(headless=True)
action_engine = ActionEngine(driver)
# 执行动作：点击、输入、滚动等
```

#### 1.3 WebAgent（Web代理）

**功能**: 组合 WorldModel 和 ActionEngine，从给定 URL 开始执行用户定义的目标

**特点**:
- 端到端自动化
- 支持复杂任务分解
- 支持 Gradio 交互界面
- 支持 Chrome 扩展

**示例**:
```python
from lavague.core.agents import WebAgent

agent = WebAgent(world_model, action_engine)
agent.get("https://example.com")
agent.run("登录并获取数据")
```

---

### 2. 关键特性

#### 2.1 多上下文支持（Contexts）

**内置上下文**:
- `OpenaiContext` - OpenAI模型（默认）
- `GeminiContext` - Google Gemini模型
- `AzureOpenaiContext` - Azure OpenAI模型
- `FireworksContext` - Fireworks模型

**自定义上下文**: 支持任何 LlamaIndex 兼容的模型

#### 2.2 多驱动支持（Drivers）

- **SeleniumDriver** - 基于Selenium
- **PlaywrightDriver** - 基于Playwright（未来支持）

#### 2.3 工具和接口

- **Gradio界面** - 交互式Web界面
- **Chrome扩展** - 浏览器内运行
- **TokenCounter** - 估算token使用和成本
- **测试框架** - 自动化测试和基准测试
- **调试工具** - 端到端调试

---

## 🚀 在 TRQuant 中的应用场景

### 场景1: 自动化数据收集 ⭐⭐⭐⭐⭐

#### 1.1 上市公司公告收集

**当前方式**: 使用 `CninfoCrawler` 手动爬取

**LaVague增强**:
```python
# 使用LaVague自动收集公告
instruction = """
访问巨潮资讯网，搜索股票代码000001，选择最近30天的公告，
提取所有公告的标题、日期、类型，保存为JSON格式
"""
result = lavague_crawler.execute_instruction(instruction)
```

**优势**:
- ✅ 自动处理登录、验证码、分页
- ✅ 智能识别页面变化
- ✅ 自动处理反爬虫机制

#### 1.2 研报数据收集

**当前方式**: 使用 `EastmoneyCrawler` 手动爬取

**LaVague增强**:
```python
# 自动收集研报
instruction = """
访问东方财富网，搜索股票代码600519，进入研报页面，
提取最近3个月的所有研报标题、机构、日期、评级
"""
result = lavague_crawler.execute_instruction(instruction)
```

#### 1.3 财务数据收集

**LaVague应用**:
```python
# 自动收集财务数据
instruction = """
访问同花顺网站，搜索股票代码000001，
进入财务数据页面，提取最近5年的：
- 营业收入
- 净利润
- 净资产收益率
- 资产负债率
保存为结构化数据
"""
```

---

### 场景2: 自动化表单填写和登录 ⭐⭐⭐⭐

#### 2.1 数据源网站登录

**问题**: 很多数据源需要登录才能访问

**LaVague解决方案**:
```python
# 自动登录JQData、Wind等数据源
instruction = """
访问聚宽数据网站，找到登录按钮并点击，
填写用户名和密码，完成登录验证
"""
result = lavague_crawler.execute_instruction(instruction)
```

#### 2.2 自动化查询

**应用**:
```python
# 自动查询数据
instruction = """
登录后，进入数据查询页面，
选择股票代码000001，时间范围2024-01-01至2024-12-31，
查询日线数据，下载CSV文件
"""
```

---

### 场景3: 智能数据提取 ⭐⭐⭐⭐⭐

#### 3.1 复杂页面数据提取

**问题**: 某些网站结构复杂，传统爬虫难以提取

**LaVague解决方案**:
```python
# 智能提取数据
description = """
从当前页面提取以下信息：
- 股票代码和名称
- 当前价格和涨跌幅
- 成交量
- 技术指标（MA5, MA10, MA20）
- 资金流向数据
"""
result = lavague_crawler.extract_data(description)
```

#### 3.2 动态内容提取

**应用**: 处理JavaScript渲染的动态内容
```python
# 等待动态内容加载后提取
instruction = """
等待页面完全加载，找到实时行情数据区域，
提取所有股票的实时价格和涨跌幅
"""
```

---

### 场景4: 自动化测试和验证 ⭐⭐⭐

#### 4.1 数据源可用性检测

**应用**:
```python
# 自动检测数据源是否可用
instruction = """
访问数据源网站，检查：
1. 网站是否可以正常访问
2. 登录功能是否正常
3. 数据查询功能是否可用
4. 返回检测结果
"""
```

#### 4.2 策略回测平台验证

**应用**:
```python
# 验证回测平台功能
instruction = """
访问回测平台，登录账户，
上传策略代码，运行回测，
检查回测结果是否正常生成
"""
```

---

### 场景5: 自动化工作流 ⭐⭐⭐⭐

#### 5.1 每日数据更新工作流

**应用**:
```python
# 自动化每日数据更新
workflow = [
    "登录数据源网站",
    "下载最新交易日数据",
    "验证数据完整性",
    "导入到数据库",
    "生成数据更新报告"
]

for step in workflow:
    result = lavague_crawler.execute_instruction(step)
```

#### 5.2 多数据源数据同步

**应用**:
```python
# 同步多个数据源
instruction = """
依次访问以下数据源，收集000001的数据：
1. 巨潮资讯网 - 公告数据
2. 东方财富网 - 研报数据
3. 同花顺 - 财务数据
4. 合并所有数据，保存到本地
"""
```

---

### 场景6: 智能信息检索 ⭐⭐⭐⭐

#### 6.1 投资主线信息收集

**应用**:
```python
# 自动收集投资主线相关信息
instruction = """
访问财经网站，搜索"人工智能"相关新闻和研报，
提取：
- 相关公司列表
- 行业动态
- 政策信息
- 市场观点
"""
```

#### 6.2 竞争对手分析

**应用**:
```python
# 自动分析竞争对手
instruction = """
访问行业分析网站，搜索目标公司的竞争对手，
收集：
- 竞争对手列表
- 市场份额对比
- 财务数据对比
- 业务模式分析
"""
```

---

## 📊 TRQuant 系统中的应用优先级

### 高优先级应用（立即实施）⭐⭐⭐⭐⭐

| 应用场景 | 当前状态 | LaVague价值 | 实施难度 |
|---------|---------|------------|---------|
| **公告数据收集** | 已有CninfoCrawler | 自动处理登录、验证码 | 低 |
| **研报数据收集** | 已有EastmoneyCrawler | 智能提取结构化数据 | 低 |
| **数据源登录** | 手动操作 | 完全自动化 | 中 |
| **复杂页面提取** | 困难 | 智能识别和提取 | 中 |

### 中优先级应用（短期实施）⭐⭐⭐

| 应用场景 | 当前状态 | LaVague价值 | 实施难度 |
|---------|---------|------------|---------|
| **财务数据收集** | 部分自动化 | 多数据源统一收集 | 中 |
| **投资主线信息** | 手动收集 | 自动搜索和整理 | 中 |
| **数据验证** | 手动验证 | 自动化检测 | 低 |

### 低优先级应用（长期规划）⭐⭐

| 应用场景 | 当前状态 | LaVague价值 | 实施难度 |
|---------|---------|------------|---------|
| **自动化测试** | 部分自动化 | 端到端测试 | 高 |
| **工作流自动化** | 已有WorkflowOrchestrator | 增强Web自动化能力 | 高 |

---

## 💡 实际应用案例

### 案例1: 自动化公告收集系统

**需求**: 每天自动收集指定股票的公告

**实现**:
```python
from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

def collect_announcements(stock_codes: List[str], days: int = 30):
    """自动收集公告"""
    crawler = get_lavague_crawler(headless=True)
    
    results = []
    for code in stock_codes:
        instruction = f"""
        访问巨潮资讯网，搜索股票代码{code}，
        选择最近{days}天的公告，
        提取所有公告的标题、日期、类型、链接
        """
        result = crawler.execute_instruction(instruction)
        results.append({
            "stock_code": code,
            "announcements": result.get("data", [])
        })
    
    return results
```

**优势**:
- ✅ 自动处理网站结构变化
- ✅ 自动处理分页
- ✅ 自动处理验证码（如果配置了）

---

### 案例2: 智能研报分析系统

**需求**: 自动收集和分析研报，提取关键信息

**实现**:
```python
def analyze_research_reports(stock_code: str):
    """智能分析研报"""
    crawler = get_lavague_crawler()
    
    instruction = f"""
    访问东方财富网，搜索股票代码{stock_code}的研报，
    提取每份研报的：
    - 标题和机构
    - 发布时间
    - 评级和目标价
    - 核心观点摘要
    - 投资建议
    分析所有研报，总结：
    - 平均评级
    - 平均目标价
    - 主要投资逻辑
    """
    
    result = crawler.execute_instruction(instruction)
    return result.get("data")
```

---

### 案例3: 多数据源数据同步

**需求**: 从多个数据源同步同一股票的数据

**实现**:
```python
def sync_stock_data(stock_code: str):
    """同步股票数据"""
    crawler = get_lavague_crawler()
    
    instruction = f"""
    依次访问以下数据源，收集股票{stock_code}的数据：
    
    1. 巨潮资讯网：
       - 最新公告
       - 财务报告
    
    2. 东方财富网：
       - 最新研报
       - 资金流向
    
    3. 同花顺：
       - 技术指标
       - 行业对比
    
    合并所有数据，生成统一的数据报告
    """
    
    result = crawler.execute_instruction(instruction)
    return result.get("data")
```

---

## 🔌 集成方案

### 方案1: 直接集成到现有爬虫系统

**位置**: `mcp_servers/crawlers/lavague_crawler.py`（已存在）

**集成方式**:
```python
# 在现有爬虫中添加LaVague支持
from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

class EnhancedCninfoCrawler:
    def __init__(self):
        self.lavague = get_lavague_crawler()
        self.traditional = get_cninfo_crawler()
    
    def fetch_announcements(self, stock_code: str):
        # 优先使用传统爬虫（快速）
        try:
            return self.traditional.fetch_announcements(stock_code)
        except Exception:
            # 失败时使用LaVague（智能）
            instruction = f"访问巨潮资讯网，搜索{stock_code}的公告"
            return self.lavague.execute_instruction(instruction)
```

---

### 方案2: 作为MCP工具集成

**位置**: `mcp_servers/unified_dev_server.py`（已存在）

**现有工具**:
- `crawler.lavague.execute` - 执行自然语言指令
- `crawler.lavague.extract` - 提取数据

**使用方式**:
```python
# 在Cursor Chat中使用
"使用crawler.lavague.execute工具，访问巨潮资讯网，搜索000001的公告"
```

---

### 方案3: 集成到工作流系统

**位置**: `core/workflow/workflow_orchestrator.py`

**集成方式**:
```python
# 在工作流中添加LaVague步骤
workflow_steps = [
    {"type": "lavague", "instruction": "登录数据源网站"},
    {"type": "lavague", "instruction": "下载最新数据"},
    {"type": "data_process", "action": "validate"},
    {"type": "data_store", "action": "save"}
]
```

---

## 📖 使用指南

### 基础使用

#### 1. 安装LaVague

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python -m pip install lavague
```

#### 2. 配置API密钥

```bash
export OPENAI_API_KEY="your-api-key"
# 或使用其他模型
export GEMINI_API_KEY="your-gemini-key"
```

#### 3. 基础示例

```python
from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

# 创建爬虫实例
crawler = get_lavague_crawler(headless=True)

# 导航到网页
crawler.navigate("https://www.cninfo.com.cn")

# 执行指令
result = crawler.execute_instruction(
    "搜索股票代码000001，进入公告页面，提取最近30天的公告"
)

# 提取数据
data = crawler.extract_data("提取所有公告的标题和日期")

# 关闭
crawler.close()
```

---

### 高级使用

#### 1. 自定义模型

```python
from lavague.core import WorldModel, ActionEngine
from lavague.drivers.selenium import SeleniumDriver
from lavague.contexts.gemini import GeminiContext

# 使用Gemini模型
context = GeminiContext()
driver = SeleniumDriver(headless=True)
action_engine = ActionEngine.from_context(context, driver)
world_model = WorldModel.from_context(context)
```

#### 2. 处理复杂任务

```python
# 多步骤任务
instructions = [
    "访问数据源网站",
    "登录账户",
    "导航到数据查询页面",
    "填写查询条件",
    "下载数据文件",
    "验证数据完整性"
]

for instruction in instructions:
    result = crawler.execute_instruction(instruction)
    if not result.get("success"):
        break
```

#### 3. 错误处理和重试

```python
def execute_with_retry(instruction: str, max_retries: int = 3):
    """带重试的执行"""
    for i in range(max_retries):
        try:
            result = crawler.execute_instruction(instruction)
            if result.get("success"):
                return result
        except Exception as e:
            if i == max_retries - 1:
                raise
            time.sleep(2 ** i)  # 指数退避
    return {"success": False, "error": "Max retries exceeded"}
```

---

## 🎯 最佳实践

### 1. 性能优化

**建议**:
- ✅ 优先使用传统爬虫（快速、稳定）
- ✅ LaVague作为备用方案（智能、灵活）
- ✅ 缓存常用数据，减少重复爬取
- ✅ 使用headless模式（更快）

### 2. 成本控制

**建议**:
- ✅ 使用较小的模型（gpt-4o-mini）进行简单任务
- ✅ 使用TokenCounter估算成本
- ✅ 批量处理任务，减少API调用
- ✅ 缓存结果，避免重复执行

### 3. 错误处理

**建议**:
- ✅ 设置合理的超时时间
- ✅ 实现重试机制
- ✅ 记录详细的错误日志
- ✅ 提供降级方案（传统爬虫）

### 4. 数据质量

**建议**:
- ✅ 验证提取的数据格式
- ✅ 检查数据完整性
- ✅ 对比多个数据源
- ✅ 定期更新爬取逻辑

---

## 📊 对比分析

### LaVague vs 传统爬虫

| 特性 | 传统爬虫 | LaVague |
|------|---------|---------|
| **速度** | ⚡⚡⚡ 快 | ⚡ 较慢（需要LLM调用） |
| **稳定性** | ✅ 高（固定逻辑） | ⚠️ 中等（依赖模型） |
| **灵活性** | ❌ 低（需要修改代码） | ✅ 高（自然语言指令） |
| **成本** | 💰 低 | 💰💰 高（API费用） |
| **维护** | ❌ 需要持续维护 | ✅ 自动适应变化 |
| **适用场景** | 固定结构网站 | 复杂、动态网站 |

### 推荐使用策略

**混合策略**:
1. **简单任务** → 使用传统爬虫（快速、稳定）
2. **复杂任务** → 使用LaVague（智能、灵活）
3. **失败回退** → 传统爬虫失败时，使用LaVague
4. **新网站** → 优先使用LaVague探索，然后固化到传统爬虫

---

## 🔗 相关文档

- `docs/LAVAGUE_INSTALLATION_FIX.md` - 安装问题修复指南
- `docs/CRAWLER_TOOLS_COMPLETE_GUIDE.md` - 爬虫工具完整指南
- `docs/CRAWLER_TEST_OPTIMIZATION.md` - 测试性能优化
- `mcp_servers/crawlers/lavague_crawler.py` - LaVague爬虫实现

---

## 📝 总结

### LaVague在TRQuant中的核心价值

1. **自动化数据收集** ⭐⭐⭐⭐⭐
   - 公告、研报、财务数据自动收集
   - 减少人工操作，提高效率

2. **智能数据提取** ⭐⭐⭐⭐⭐
   - 从复杂页面提取结构化数据
   - 自动适应页面变化

3. **自动化工作流** ⭐⭐⭐⭐
   - 多步骤任务自动化
   - 减少人工干预

4. **数据源管理** ⭐⭐⭐⭐
   - 自动登录和验证
   - 多数据源统一管理

### 实施建议

1. **短期**（1-2周）:
   - ✅ 修复LaVague导入问题
   - ✅ 实现基础数据收集功能
   - ✅ 测试公告和研报收集

2. **中期**（1个月）:
   - ✅ 集成到现有爬虫系统
   - ✅ 实现自动化登录功能
   - ✅ 优化性能和成本

3. **长期**（3个月）:
   - ✅ 完善工作流集成
   - ✅ 实现智能数据提取
   - ✅ 建立最佳实践文档

---

**最后更新**: 2026-01-17  
**维护者**: TRQuant Team
