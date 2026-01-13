# TRQuant 韬睿量化系统 - AI助手上下文文档

> **版本**: v1.2  
> **更新**: 2026-01-08  
> **目的**: 为Claude AI提供项目上下文，指导开发和使用

---

## 📋 项目概览

**TRQuant（韬睿量化）** 是一个专业的量化交易研究系统，采用**研究-实战双阶段分离架构**。

### 核心定位

- **研究阶段**: Jupyter Notebook（数据研究、可视化、模型验证）
- **实战阶段**: GUI面板 + API（策略执行、实盘交易）
- **数据源**: JQData（聚宽）优先，AKShare补充
- **存储**: MongoDB（信号、回测结果、版本管理）

### 系统定位（完整投资流程系统）

**TRQuant（韬睿量化）** 是一个**完整的A股量化投资系统**，区别于传统的回测平台（如QuantConnect），提供从信息获取到实盘交易的**8步骤完整工作流**。

**核心区别**：
- **QuantConnect**：回测平台，策略→回测→结果
- **TRQuant**：完整投资流程系统，8步骤完整工作流（信息获取→市场趋势→投资主线→候选池→因子构建→策略开发→回测验证→实盘交易）

**核心特点**：
- **核心定位**: 完整投资流程系统（非单纯回测平台）
- **工作流程**: 8步骤完整工作流
- **目标市场**: A股专属
- **券商对接**: PTrade/QMT
- **使用方式**: 桌面GUI系统、Cursor扩展、命令行、在线手册
- **AI集成**: MCP协议、RAG知识库、AI辅助决策
- **开发模式**: 三条铁律：信息入口先MCP、写操作走安全写入协议、大输出artifact化

---

## 🏗️ 系统架构

### 三层架构（核心原则）

```
┌─────────────────────────────────────────┐
│  研究阶段前端 (Jupyter Notebook)        │
│  notebooks/research/                    │
│  - 直接导入Core模块                      │
│  - 交互式研究和可视化                    │
└─────────────────────────────────────────┘
              ↓ 直接调用
┌─────────────────────────────────────────┐
│  功能实现层 (Core Python Modules)       │
│  core/                                   │
│  - 所有功能在这里实现                    │
│  - 可被Notebook和MCP Server调用         │
└─────────────────────────────────────────┘
              ↓ 封装调用
┌─────────────────────────────────────────┐
│  MCP Servers (LLM工具接口)              │
│  mcp_servers/                           │
│  - 封装Core模块供LLM调用                │
│  - 支持工作流自动化                      │
└─────────────────────────────────────────┘
```

### 七层架构（完整系统）

```
┌─────────────────────────────────────────────────────────────┐
│ 第1层：表现层 (Presentation Layer)                          │
│  - 桌面系统GUI (PyQt6)                                      │
│  - Cursor扩展 (TypeScript + React)                          │
│  - 命令行工具 (CLI)                                         │
│  - 在线手册 (Astro)                                         │
├─────────────────────────────────────────────────────────────┤
│ 第2层：API接口层 (API Layer)                                │
│  - TRQuantAPIBase (统一接口抽象)                            │
│  - CoreAdapter (核心模块适配器)                              │
├─────────────────────────────────────────────────────────────┤
│ 第3层：AI代理层 (AI Agent Layer)                            │
│  - AI Agent Hub (LLM服务 + 工具调度)                        │
│  - 轩辕剑灵 (AI助手，自动执行任务)                           │
├─────────────────────────────────────────────────────────────┤
│ 第4层：编排与工具链层 (Orchestration & Toolchain Layer)     │
│  - WorkflowOrchestrator (工作流编排器)                      │
│  - MCP Servers (20+个MCP服务器)                            │
│  - RAG KB (知识检索)                                        │
│  - Strategy KB (策略知识库)                                 │
│  - Evidence Server (证据记录)                                │
├─────────────────────────────────────────────────────────────┤
│ 第5层：核心业务层 (Core Business Layer)                      │
│  - DataSource (数据源管理)                                  │
│  - TrendAnalyzer (市场分析)                                 │
│  - Mainline (主线识别)                                      │
│  - CandidatePool (候选池构建)                               │
│  - FactorLib (因子库)                                       │
│  - StrategyDev (策略开发)                                   │
│  - Optimizer (策略优化)                                     │
│  - Backtest (回测验证)                                      │
├─────────────────────────────────────────────────────────────┤
│ 第6层：数据与知识平台层 (Data & Knowledge Platform Layer)   │
│  - PostgreSQL (主数据库，强事务/审计)                        │
│  - ClickHouse/TimescaleDB (时序分析库)                      │
│  - MinIO/S3 (对象存储)                                      │
│  - Redis (缓存/队列)                                        │
│  - Chroma (向量数据库)                                      │
│  - MongoDB (文档存储，研究材料)                              │
├─────────────────────────────────────────────────────────────┤
│ 第7层：执行层 (Execution Layer)                            │
│  - PTrade (交易平台)                                        │
│  - QMT (交易平台)                                           │
└─────────────────────────────────────────────────────────────┘
```

### 关键原则

1. **Core模块是基础**: 所有功能在 `core/` 中实现
2. **Notebook直接调用Core**: `from core.xxx import Xxx`
3. **MCP Server封装Core**: 供LLM和工作流调用
4. **禁止Notebook通过MCP调用Core**: 除非需要工作流集成

---

## 🔄 工作流程（统一术语）

### 8步骤完整工作流

```
步骤1: 📡 信息获取 (数据更新)
  ↓
步骤2: 📈 市场趋势 (趋势分析)
  ↓
步骤3: 🔥 投资主线 (主线识别)
  ↓
步骤4: 📦 候选池构建 (股票筛选)
  ↓
步骤5: 📊 因子构建 (因子计算)
  ↓
步骤6: 🛠️ 策略生成 (策略开发)
  ↓
步骤7: ⚡ 策略优化 (参数优化)
  ↓
步骤8: 🔄 回测验证 (回测分析)
  ↓
步骤9: 🚀 实盘交易 (交易执行)
```

### 研究阶段工作流（R0-R6）

参考 `notebooks/research/00_system_architecture_workflow.ipynb`:

- **R0**: 数据源检测
- **R1**: 市场趋势分析
- **R2**: 主线轮动研究
- **R3**: 因子组合开发
- **R4**: 投资标的筛选（不是"候选池构建"）
- **R5**: 风控模块设计
- **R6**: 策略开发与回测

**重要**: 统一使用"投资标的筛选"，不使用"候选池构建"。

---

## 📁 目录结构

### 核心目录

```
TRQuant/
├── core/                          # 核心功能实现
│   ├── market_trend_analyzer.py   # 市场趋势分析器
│   ├── trend_analyzer.py          # 趋势分析器（基线）
│   ├── candidate_pool_builder.py  # 投资标的筛选器
│   ├── signal_backtest.py         # 信号回测器
│   ├── market_regime/             # 市场环境识别
│   ├── rotation/                  # 行业轮动
│   ├── selection/                 # 标的筛选
│   ├── backtest/                  # 回测模块
│   └── ...
├── notebooks/research/             # 研究前端
│   ├── 00_system_architecture_workflow.ipynb  # 系统架构文档
│   ├── 01_Market_Trend_Analyzer.ipynb         # 市场趋势分析
│   ├── 01_market_trend_resonance_mvp.ipynb    # A股共振系统MVP
│   └── ...
├── mcp_servers/                    # MCP工具接口
│   ├── trquant_core_server.py     # 核心功能服务器
│   ├── workflow_9steps_server.py # 工作流服务器
│   ├── unified_dev_server.py      # 统一开发工具服务器
│   └── ...
├── config/                         # 配置文件
│   └── jqdata_config.json         # JQData配置
├── docs/                           # 文档
│   ├── MUST_READ/                  # 必读文档
│   ├── 02_development_guides/     # 开发指南
│   └── ...
└── .trquant/dev/knowledge/         # RAG知识库
    ├── knowledge_base.json        # 知识库JSON
    └── vector_index/              # 向量索引
```

---

## 💻 开发规范

### Python编码规范

- **命名**: `snake_case`（函数、变量）、`PascalCase`（类）、`UPPER_CASE`（常量）
- **导入**: 标准库 → 第三方库 → 本地模块
- **文档**: 所有公共函数必须有Google风格docstring
- **类型**: 所有函数参数和返回值必须有类型提示

### Notebook开发规范

**第一个Cell必须包含**:
```python
import sys
from pathlib import Path

# 自动检测项目根目录
current_dir = Path.cwd()
project_root = None
for parent in [current_dir] + list(current_dir.parents):
    if (parent / 'core').exists() and (parent / 'config').exists():
        project_root = parent
        break

if project_root is None:
    project_root = Path('/home/taotao/.cursor/worktrees/TRQuant/ope')

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 使用统一环境初始化
from notebooks.lib import setup_research_environment
env = setup_research_environment(verbose=True)
```

**导入Core模块**:
```python
# ✅ 推荐
from core.market_trend_analyzer import MarketTrendAnalyzer
from core.trend_analyzer import TrendAnalyzer

# ❌ 不推荐（除非需要工作流集成）
from core.mcp.client import MCPClient
```

**数据源检测（可选，推荐）**:
```python
from notebooks.lib import ErrorBoundary

# 检测JQData连接
jqdata_status = "❌ 未连接"
jq = None
with ErrorBoundary("检测JQData连接", suppress=True) as eb:
    jq = env.get_jqdata_client()
    if jq and hasattr(jq, 'is_authenticated') and jq.is_authenticated():
        jqdata_status = "✅ 已连接"
    elif jq:
        jqdata_status = "✅ 已连接"
```

**错误处理原则**:
- 使用 `ErrorBoundary` 包装可能失败的初始化
- 设置 `suppress=True` 使失败不影响后续代码
- 提供友好的错误提示和降级方案

### 开发流程规范

**标准开发流程**（参考 `docs/MUST_READ/02_DEV_WORKFLOW.md`）：

1. **会话初始化**: 每次新对话必须执行 `session.init`
2. **任务管理**: 使用 `quick.start_task` 和 `quick.finish_task`
3. **日志记录**: 使用 `devlog.add` 或 `quick.log` 记录进度
4. **知识检索**: 遇到问题先用 `knowledge.search` 搜索已有解决方案
5. **绝对路径**: 文件操作必须使用 `/home/taotao/dev/QuantTest/TRQuant/...`

**三条铁律**：
1. **信息入口先MCP**: 所有数据获取、信息查询优先使用MCP工具
2. **写操作走安全写入协议**: 文件写入、配置修改使用安全协议
3. **大输出artifact化**: 大文件、报告、结果使用artifact方式输出

### 增量式开发方法论（参考vibe-coding）

**核心原则**（适用于TRQuant系统开发）：

1. **增量式开发和测试**
   - 分阶段实施，每完成一步验证测试通过后再继续下一步
   - 避免一次性实现大功能，降低风险
   - 每个阶段都有明确的测试和验收标准

2. **测试驱动开发**
   - 先写测试，再写代码
   - 确保每个功能都有对应的测试用例
   - 测试通过后再提交代码

3. **文档先行**
   - 先完善文档和设计，再实施代码
   - 重要功能先写实现计划（implementation-plan.md）
   - 完成后更新进度文档（progress.md）和架构文档（architecture.md）

4. **版本控制工作流**
   - 完成第1步后：提交到Git，记录改动
   - 新建聊天（`/new` 或 `/clear`）：开始下一步
   - 继续实施：阅读memory-bank和progress.md，继续下一步
   - 验证测试：每步完成后验证，通过后再继续

5. **错误处理和回退机制**
   - 如果提示词失败或搞崩项目：使用 `/rewind` 回退（Claude Code）或 `git reset`（Git）
   - 报错处理：复制错误信息，贴给AI分析
   - 极度卡壳：回退到上一个git commit，换新提示词重试

6. **AI工具使用技巧**
   - **Claude Code / Codex CLI**: 终端版能直接看diff、喂上下文
   - **自定义命令**: 创建快捷命令如 `/explain $参数`，让模型先理解再改代码
   - **清理上下文**: 经常用 `/clear` 或 `/compact` 保持上下文清晰
   - **深度思考**: 使用 `think` < `think hard` < `think harder` < `ultrathink` 触发深度思考

---

## 🎯 核心模块说明

### MarketTrendAnalyzer

**位置**: `core/market_trend_analyzer.py`

**功能**:
- 多周期趋势分析（周/月/季 = 5/21/63交易日）
- HMM隐状态识别（SimpleHMM）
- 加权融合输出（Trend 0.8 + HMM 0.2）
- 生成workflow_params和investment_universe_filters

**基线**: TrendAnalyzer + SimpleHMM（已回测验证）

**配置**:
- `scoring_style`: `'smooth_grouped'`（推荐）或 `'legacy'`
- 周期定义: 周/月/季 = 5/21/63交易日（可扩展）

### TrendAnalyzer

**位置**: `core/trend_analyzer.py`

**功能**: 8维技术指标打分体系

**评分风格**:
- `legacy`: 传统硬阈值方式
- `smooth_grouped`: 连续映射 + 因子分组（推荐）

### CandidatePoolBuilder

**位置**: `core/candidate_pool_builder.py`

**功能**: 投资标的筛选（基于投资主线）

**注意**: 统一术语为"投资标的筛选"，不是"候选池构建"。

### A股多周期共振状态系统

**位置**: `core/resonance_state_model.py`, `core/market_trend_analyzer.py`, `core/rotation/sector_resonance.py`, `core/selection/stock_filters.py`, `core/backtest/resonance_event_study.py`

**功能**: A股本土化的多周期共振状态识别系统，作为"系统开关"用于仓位控制和风险预算

**三层结构**:
1. **Layer 1 - 市场总开关**: 沪深300 + 中证1000 多指数共振 → 仓位上限映射
2. **Layer 2 - 行业轮动**: 申万一级行业 + 主题ETF 共振TopN → 可投资池
3. **Layer 3 - 个股过滤**: RS相对强度 + 流动性 + 涨跌停/ATR异常检测 → 最终标的

**核心原则**:
- 共振不负责买点，负责"系统开关"
- 仓位控制比买卖点更重要
- 持续性确认：共振连续出现2~3次才升级仓位

**验证Notebook**: `notebooks/research/01_market_trend_resonance_mvp.ipynb`

**关键配置**:
- 短周期: 5日（情绪/短线资金）
- 中周期: 21日（主线/波段资金）
- 长周期: 63日（机构趋势）
- 确认窗口: 2次（共振持续性确认）
- 行业TopN: 5（可投资行业数量）

### 市场环境识别（Market Regime Detection）

**位置**: `core/market_regime/market_regime_detector.py`

**功能**: 识别市场环境阶段（BULL, BEAR, VOLATILE, RECOVERY, DISTRIBUTION）

**重要原则**:
- **不频繁切换**: 市场环境判断有标准、有信号，但不应该每天都计算
- **稳定性优先**: 避免隔几天就换市场环境，确保判断的持续性
- **信号确认**: 需要连续出现2~3次才确认环境切换

---

## 🔧 MCP工具使用

### 可用工具

**核心业务工具**:
- `market.trend` - 分析市场趋势
- `market.mainlines` - 识别投资主线
- `market.regime` - 识别市场环境
- `data.candidate_pool` - 筛选投资标的
- `factor.recommend` - 推荐因子
- `backtest.run` - 运行回测
- `workflow9.execute` - 执行工作流

**开发工具**（`unified_dev_server.py`）:
- `knowledge_search` - 知识库检索（RAG）
- `knowledge_add` - 添加知识到知识库
- `crawler_fetch` - 网页爬取
- `crawler_selenium_fetch` - Selenium爬取（支持JavaScript）
- `devlog_add` - 开发日志记录
- `session_init` - 会话初始化

### 使用方式

在Cursor Chat中：
```
"请使用market.trend工具分析当前市场趋势"
"请使用knowledge_search检索BulletTrade回测配置"
```

---

## 📊 数据源配置

### JQData（聚宽）

**配置文件**: `config/jqdata_config.json`

**账号信息**:
- **正式账号**: 13327806797（所有测试使用此账号）
- **数据范围**: 2022-01-01 至 2024-12-31（正式账号完整历史数据）

**使用**:
```python
from config.config_manager import get_config_manager
import jqdatasdk as jq

cm = get_config_manager()
jq_config = cm.get_config('jqdata')
jq.auth(jq_config['username'], jq_config['password'])
```

**文档**: `docs/JQDATA_CONFIGURATION_GUIDE.md`

### MongoDB

**用途**: 存储信号、回测结果、版本管理

**集合**:
- `market_trend` - 市场趋势信号
- `backtest_results` - 回测结果
- `candidate_pool` - 投资标的池

---

## 🚫 常见错误和避免

### 1. Notebook通过MCP调用Core

```python
# ❌ 错误
from core.mcp.client import MCPClient
client = MCPClient()
result = client.call_tool("market.trend", {...})

# ✅ 正确
from core.market_trend_analyzer import MarketTrendAnalyzer
analyzer = MarketTrendAnalyzer(config)
result = analyzer.analyze(...)
```

### 2. Core模块导入Notebook代码

```python
# ❌ 错误
from notebooks.lib import something

# ✅ 正确
# Core模块应该独立，不依赖Notebook
```

### 3. 术语不一致

- ❌ "候选池构建"
- ✅ "投资标的筛选"

### 4. Notebook初始化代码错误

**问题**: 初始化代码中路径错误或缺少错误处理

**正确做法**:
```python
# ✅ 正确：使用正确的项目路径和错误处理
if project_root is None:
    project_root = Path('/home/taotao/.cursor/worktrees/TRQuant/ope')

# ✅ 正确：使用ErrorBoundary和suppress参数
with ErrorBoundary("初始化评估引擎", suppress=True) as eb:
    evaluator = env.get_market_evaluator()
if eb.has_error:
    print(f"⚠️ 初始化失败: {eb.error_message} (可继续使用其他功能)")
```

### 5. 语法错误：if语句后缺少代码块

**问题**: `if` 语句后只有空行，没有实际代码块

**示例**:
```python
# ❌ 错误
def get_market_regime_detector():
    global _detector
    if _detector is None:
        # 这里缺少代码

# ✅ 正确
def get_market_regime_detector():
    global _detector
    if _detector is None:
        _detector = MarketRegimeDetector()
    return _detector
```

### 6. 市场环境频繁切换

**问题**: 市场环境判断每天计算，导致频繁切换

**正确做法**:
- 市场环境判断有标准、有信号，但不应该每天都计算
- 需要连续出现2~3次才确认环境切换
- 确保判断的稳定性和持续性

### 7. Python环境路径错误

**问题**: 脚本执行时找不到正确的Python环境

**正确做法**:
- 所有脚本必须使用完整路径: `/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python`
- 在脚本开头添加环境检查
- 使用 `source venv/bin/activate` 激活环境

### 8. 开发流程混乱

**问题**: 一次性实现大功能，导致错误难以定位和修复

**正确做法**（参考vibe-coding方法论）:
- **增量式开发**: 分步骤实施，每步验证后再继续
- **测试驱动**: 先写测试，再写代码
- **文档先行**: 重要功能先写实现计划
- **版本控制**: 每完成一步提交到Git
- **错误回退**: 使用 `/rewind` 或 `git reset` 快速回退

---

## 📚 重要文档

### 必读文档

- **快速开始**: `docs/MUST_READ/01_QUICK_START.md`
- **开发流程**: `docs/MUST_READ/02_DEV_WORKFLOW.md`
- **强制规则**: `docs/MUST_READ/03_RULES.md`
- **MCP工具**: `docs/MUST_READ/04_TOOLS.md`
- **知识库使用**: `docs/MUST_READ/05_KNOWLEDGE.md`

### 系统文档

- **系统架构**: `notebooks/research/00_system_architecture_workflow.ipynb`
- **市场趋势分析**: `notebooks/research/01_Market_Trend_Analyzer.ipynb`
- **A股共振系统MVP**: `notebooks/research/01_market_trend_resonance_mvp.ipynb`
- **开发白皮书**: `docs/02_development_guides/DEVELOPMENT_WHITEPAPER.md`
- **系统总结**: `docs/01_architecture/SYSTEM_REVIEW_AND_PLAN.md`

### 开发指南

- **开发最佳实践**: `docs/02_development_guides/BEST_PRACTICES_DEVELOPMENT_USAGE.md`
- **Cursor 2.3功能**: `docs/02_development_guides/CURSOR_2.3_FEATURES_RESEARCH.md`
- **JQData配置**: `docs/JQDATA_CONFIGURATION_GUIDE.md`
- **Rules配置**: `.cursor/rules/` 目录

---

## 🎯 开发任务指导

### 创建新功能

1. **在Core模块中实现**
   ```python
   # core/new_feature.py
   class NewFeature:
       def process(self, ...):
           # 实现逻辑
           pass
   ```

2. **在Notebook中测试**
   ```python
   # notebooks/research/test_new_feature.ipynb
   from core.new_feature import NewFeature
   feature = NewFeature()
   result = feature.process(...)
   ```

3. **（可选）封装成MCP工具**
   ```python
   # mcp_servers/xxx_server.py
   from core.new_feature import NewFeature
   # 封装成MCP工具
   ```

### 修改现有功能

1. **先查看相关文档和Rules**
2. **遵循架构规范**
3. **更新相关文档**
4. **测试验证**

### 使用RAG知识库

**知识库内容**:
- BulletTrade文档（GitHub + 网站，14个页面）
- vibe-coding-cn开发指南
- TRQuant系统开发文档（36+个相关文档）

**检索方式**:
```python
from mcp_servers.unified_dev_server import knowledge_search

# 语义搜索
result = knowledge_search("BulletTrade 回测配置", limit=10)
result = knowledge_search("市场趋势分析", limit=10)
result = knowledge_search("vibe-coding 开发流程", limit=10)
```

---

## 💡 AI助手使用建议

### 当用户请求开发任务时

1. **理解上下文**: 参考本文件和Rules
2. **遵循架构**: 三层架构原则
3. **使用正确术语**: "投资标的筛选"不是"候选池构建"
4. **直接调用Core**: Notebook中直接导入Core模块
5. **提供完整代码**: 包含路径设置、导入、使用示例
6. **使用知识库**: 遇到问题先检索RAG知识库
7. **增量式开发**: 分步骤实施，每步验证后再继续
8. **文档同步**: 完成后更新相关文档（progress.md、architecture.md）

### 增量式开发工作流（推荐）

**标准流程**：
1. **理解需求**: 阅读memory-bank所有文档，确认implementation-plan.md是否清晰
2. **提问澄清**: 提出9-10个问题，让计划100%明确
3. **执行第1步**: 使用"Ask"模式或"Plan Mode"确认后再执行
4. **验证测试**: 用户验证测试通过前，不开始第2步
5. **记录进度**: 验证通过后，更新progress.md记录做了什么
6. **更新架构**: 把新的架构洞察添加到architecture.md
7. **提交Git**: 把改动提交到Git
8. **新建聊天**: 使用 `/new` 或 `/clear` 开始下一步
9. **继续实施**: 阅读memory-bank和progress.md，继续实施计划第2步
10. **重复流程**: 直到整个implementation-plan.md全部完成

### 当用户请求分析任务时

1. **使用MCP工具**: 如 `market.trend`、`data.candidate_pool`
2. **或直接调用Core**: 在Notebook中直接使用Core模块
3. **提供可视化**: 使用Plotly生成交互式图表

### 当用户请求信息检索时

1. **优先使用RAG知识库**: `knowledge_search`
2. **支持混合检索**: 向量检索 + 关键词检索
3. **提供来源**: 返回结果包含文档来源和相关性分数

---

## 📂 工作目录规则

### ⚠️ 重要：唯一工作目录

**工作目录（唯一且固定）**: `/home/taotao/.cursor/worktrees/TRQuant/ope/`

**禁止规则**:
- ❌ **禁止使用abd目录** - abd目录已删除，不再使用，**永远不要创建或使用**
- ❌ **禁止创建新的工作目录** - 所有操作必须在ope目录下
- ✅ **所有文件操作必须使用ope目录** - 这是唯一的工作目录
- ✅ **所有文件路径必须明确包含 `/ope/`** - 确保不会误操作到其他目录
- ❌ **禁止任何工具或脚本引用abd路径** - 如果发现abd路径，立即停止并修正

**强制规则**:
1. **所有文件操作必须使用绝对路径**: `/home/taotao/.cursor/worktrees/TRQuant/ope/...`
2. **禁止使用相对路径**（除非明确知道当前目录是ope）
3. **如果系统工具尝试从abd读取文件，这是错误** - 必须使用ope路径
4. **如果发现abd目录被创建，立即删除**: `rm -rf /home/taotao/.cursor/worktrees/TRQuant/abd`

**系统工具使用规范**:
- ✅ 使用 `read_file` 时，路径必须是 `/home/taotao/.cursor/worktrees/TRQuant/ope/...`
- ✅ 使用 `write` 时，路径必须是 `/home/taotao/.cursor/worktrees/TRQuant/ope/...`
- ❌ **禁止**使用包含 `abd` 的路径
- ❌ **禁止**系统工具自动解析到abd目录

### 操作性工作统一放在 `worktrees/TRQuant/ope` 目录

所有回测验证、策略开发、数据分析等操作性工作文件统一存放：

```
工作目录: /home/taotao/.cursor/worktrees/TRQuant/ope/
Python环境: /home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python
```

**目录结构**:
```
worktrees/TRQuant/ope/
├── venv/                    # Python虚拟环境
├── scripts/                 # 脚本文件
│   └── stage_backtest/     # 回测验证脚本
├── docs/                    # 文档
├── data/                    # 数据文件（按需创建）
└── results/                 # 结果输出（按需创建）
```

**运行脚本示例**:
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./venv/bin/python scripts/stage_backtest/stage_backtest_validator.py
```

**重要**: 
- 所有操作性工作文件必须放在此目录
- Python虚拟环境也在此目录下
- 脚本中的路径引用应使用此工作目录

---

## 🔄 版本和更新

- **项目路径**: `/home/taotao/.cursor/worktrees/TRQuant/ope`
- **Python版本**: 3.11+
- **主要依赖**: pandas, numpy, jqdatasdk, pymongo, plotly

### 最新更新 (2026-01-08)

- ✅ **RAG知识库扩展**: 添加BulletTrade文档（14个页面）和vibe-coding-cn开发指南
- ✅ **市场环境识别优化**: 调整市场环境判断逻辑，避免频繁切换
- ✅ **JQData账号统一**: 所有测试使用正式账号（13327806797），数据范围2022-2024
- ✅ **开发工具完善**: 统一开发工具服务器（unified_dev_server.py）提供57个工具
- ✅ **增量式开发方法论**: 集成vibe-coding开发方法论，包括增量式开发、测试驱动、文档先行等原则

### 历史更新

- ✅ **A股多周期共振状态系统**: 完成三层架构实现（市场总开关、行业轮动、个股过滤）
- ✅ **修复语法错误**: `core/market_regime/market_regime_detector.py` 中 `get_market_regime_detector()` 函数
- ✅ **改进Notebook初始化**: 增强错误处理和数据源检测
- ✅ **新增验证Notebook**: `01_market_trend_resonance_mvp.ipynb`

---

## 📊 系统状态

### 核心模块完成度

| 模块 | 状态 | 完成度 | 说明 |
|------|------|--------|------|
| **数据源管理** | ✅ | 95% | JQData/AKShare集成完成，支持多数据源 |
| **市场分析** | ✅ | 90% | 趋势分析、宏观分析、情绪分析、风格轮动 |
| **主线识别** | ✅ | 85% | 主线扫描、映射、评分（五维评分模型） |
| **候选池** | ✅ | 90% | 多维度评分、股票筛选、权重配置 |
| **因子库** | ✅ | 95% | 60+因子，因子管理、计算、评估、优化 |
| **策略开发** | ✅ | 90% | 策略生成器、策略管理器、策略模板库 |
| **策略优化** | ✅ | 80% | 参数优化、多目标优化（待完善） |
| **回测** | ✅ | 85% | BulletTrade集成，回测引擎、分析器 |
| **执行** | ✅ | 80% | PTrade/QMT桥接，交易接口 |

### MCP服务器系统

TRQuant系统实现了**26个MCP服务器**，提供完整的工具链支持：
- **业务服务器**: TRQuant核心、数据源、回测、工作流等
- **开发工具服务器**: 统一开发工具服务器（57个工具）
- **知识库服务器**: RAG知识库、策略知识库、证据追踪
- **爬虫服务器**: 基础爬虫、Selenium爬虫、Lavague爬虫

---

**最后更新**: 2026-01-08  
**维护者**: TRQuant Team
