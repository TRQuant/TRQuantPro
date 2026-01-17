# Cursor 2.3 新功能研究与应用指南

> **研究时间**: 2026-01-06  
> **目的**: 研究Cursor 2.3的新功能，特别是Rules、Commands、Import Settings和Claude Skills，为完善市场趋势分析Notebook做准备

---

## 📋 目录

1. [Cursor 2.3 核心新功能概览](#1-cursor-23-核心新功能概览)
2. [Rules（规则）功能详解](#2-rules规则功能详解)
3. [Commands（命令）功能详解](#3-commands命令功能详解)
4. [Import Settings（导入设置）详解](#4-import-settings导入设置详解)
5. [Claude Skills 支持情况](#5-claude-skills-支持情况)
6. [TRQuant项目应用建议](#6-trquant项目应用建议)
7. [实施计划](#7-实施计划)

---

## 1. Cursor 2.3 核心新功能概览

### 1.1 主要更新

| 功能 | 说明 | 状态 |
|------|------|------|
| **Rules（规则）** | 项目级规则定义，指导AI行为 | ✅ 已支持 |
| **Commands（命令）** | 自定义命令，从对话中执行操作 | ✅ 已支持 |
| **Import Settings** | 从VS Code导入设置 | ✅ 已支持 |
| **Claude Skills** | Claude技能集成 | ⚠️ 需要Nightly版本 |
| **布局模式** | Agent/Editor/Zen/Browser四种模式 | ✅ 已支持 |
| **MCP增强** | 认证流程和连接稳定性改进 | ✅ 已支持 |

### 1.2 版本要求

- **基础功能**: Cursor 2.3+
- **Claude Skills**: 需要切换到Nightly更新渠道

---

## 2. Rules（规则）功能详解

### 2.1 什么是Rules？

Rules是项目级的规则定义系统，用于：
- ✅ 编码项目的领域知识
- ✅ 自动化项目特定的工作流程或模板
- ✅ 标准化风格或架构决策
- ✅ 为AI提供一致的指导

### 2.2 Rules的存储位置

```
项目根目录/
└── .cursor/
    └── rules/
        ├── coding-standards.md
        ├── architecture.md
        ├── workflow.md
        └── ...
```

**特点**:
- 存储在 `.cursor/rules/` 目录中
- 每个规则是一个独立的Markdown文件
- 支持版本控制（可提交到Git）
- 支持嵌套目录结构

### 2.3 Rules文件格式（MDC格式）

Rules使用 **MDC（Markdown with front matter）** 格式：

```markdown
---
name: "TRQuant编码规范"
description: "TRQuant项目的Python编码规范和最佳实践"
type: "always"  # always | auto-attached | agent-requested | manual
tags: ["coding", "python", "trquant"]
---

# TRQuant编码规范

## Python代码规范

### 命名规范
- 模块名: `snake_case`
- 类名: `PascalCase`
- 函数名: `snake_case`
- 常量: `UPPER_CASE`

### 导入规范
- 标准库导入
- 第三方库导入
- 本地模块导入
- 使用 `from core.xxx import Xxx` 格式

## 架构规范

### 三层架构
1. **Core模块** (`core/`): 核心功能实现
2. **Notebook** (`notebooks/research/`): 研究前端
3. **MCP Server** (`mcp_servers/`): LLM工具接口

### 模块导入原则
- Notebook直接导入Core模块
- MCP Server封装Core模块
- 避免Notebook通过MCP Server调用Core模块
```

### 2.4 Rules类型

| 类型 | 说明 | 使用场景 |
|------|------|---------|
| **always** | 始终应用 | 编码规范、架构决策 |
| **auto-attached** | 自动附加 | 特定文件类型、特定目录 |
| **agent-requested** | 代理请求 | 复杂任务、需要上下文 |
| **manual** | 手动调用 | 临时规则、实验性规则 |

### 2.5 创建Rules的两种方式

#### 方式1: 从对话中生成（推荐）

在Cursor Chat中：
```
"请为TRQuant项目创建一个编码规范规则，包括Python命名规范、导入规范和架构规范"
```

Cursor会自动生成规则文件并保存到 `.cursor/rules/` 目录。

#### 方式2: 手动创建

1. 创建 `.cursor/rules/` 目录
2. 创建Markdown文件
3. 添加front matter元数据
4. 编写规则内容

### 2.6 TRQuant项目建议的Rules

#### 规则1: 编码规范 (`coding-standards.md`)

```markdown
---
name: "TRQuant编码规范"
type: "always"
tags: ["coding", "python"]
---

# TRQuant编码规范

## Python代码规范
- 使用PEP 8风格
- 函数和变量使用snake_case
- 类名使用PascalCase
- 常量使用UPPER_CASE

## 导入规范
- 标准库 → 第三方库 → 本地模块
- 使用绝对导入: `from core.xxx import Xxx`
- Notebook中必须设置sys.path

## 文档规范
- 所有公共函数必须有docstring
- 使用Google风格docstring
```

#### 规则2: 架构规范 (`architecture.md`)

```markdown
---
name: "TRQuant架构规范"
type: "always"
tags: ["architecture", "design"]
---

# TRQuant三层架构规范

## 架构原则
1. Core模块是基础，所有功能在core/中实现
2. Notebook直接调用Core模块，不通过MCP Server
3. MCP Server封装Core模块，供LLM调用

## 模块组织
- `core/`: 核心功能实现
- `notebooks/research/`: 研究前端
- `mcp_servers/`: LLM工具接口

## 禁止做法
- ❌ Notebook通过MCP Server调用Core模块
- ❌ Core模块导入Notebook相关代码
- ❌ MCP Server中实现业务逻辑
```

#### 规则3: Notebook开发规范 (`notebook-development.md`)

```markdown
---
name: "Notebook开发规范"
type: "auto-attached"
autoAttach:
  - "**/*.ipynb"
tags: ["notebook", "research"]
---

# Notebook开发规范

## 初始化模式
所有Notebook的第一个cell必须包含：
```python
import sys
from pathlib import Path
# 自动检测项目根目录
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
```

## 导入规范
- 直接导入Core模块: `from core.xxx import Xxx`
- 使用统一环境初始化: `from notebooks.lib import setup_research_environment`

## 可视化规范
- 使用Plotly进行交互式可视化
- 使用ChartEngine生成专业图表
- 图表必须包含标题、轴标签、图例
```

#### 规则4: 市场趋势分析规范 (`market-trend-analysis.md`)

```markdown
---
name: "市场趋势分析规范"
type: "agent-requested"
tags: ["market", "trend", "analysis"]
---

# 市场趋势分析开发规范

## 工作流程
1. 数据源检测 (R0)
2. 市场趋势分析 (R1)
3. 主线轮动研究 (R2)
4. 因子组合开发 (R3)
5. 投资标的筛选 (R4)
6. 风控模块设计 (R5)
7. 策略开发与回测 (R6)

## 核心模块
- `MarketTrendAnalyzer`: 市场趋势分析器
- `TrendAnalyzer`: 趋势分析器（基线）
- `SimpleHMM`: HMM隐状态识别（已优化）

## 配置参数
- 周期定义: 周/月/季 = 5/21/63交易日
- 权重: Trend 0.8 + HMM 0.2
- 评分风格: `smooth_grouped`（推荐）或 `legacy`
```

---

## 3. Commands（命令）功能详解

### 3.1 什么是Commands？

Commands允许您在Cursor Chat中执行特定操作，例如：
- 创建Pull Request
- 运行测试
- 生成代码
- 执行脚本

### 3.2 Commands的使用方式

#### 在Chat中使用

```
@command create_pr
"请创建一个Pull Request，包含当前所有更改"
```

#### 自定义Commands

Commands可以存储在 `.cursor/commands/` 目录中，或通过设置导入。

### 3.3 TRQuant项目建议的Commands

#### Command 1: 运行回测

```yaml
name: "运行市场趋势回测"
description: "运行Phase 1和Phase 2回测"
command: |
  cd notebooks/research
  python -m pytest 01_市场趋势判断回测验证.ipynb
```

#### Command 2: 生成报告

```yaml
name: "生成市场趋势报告"
description: "生成市场趋势分析HTML报告"
command: |
  python scripts/generate_market_trend_report.py
```

#### Command 3: 验证代码

```yaml
name: "验证Core模块"
description: "运行Core模块的单元测试"
command: |
  pytest tests/test_core/ -v
```

---

## 4. Import Settings（导入设置）详解

### 4.1 功能说明

Import Settings允许您：
- ✅ 从VS Code导入设置
- ✅ 导入扩展、主题、配置
- ✅ 导入键绑定

### 4.2 使用步骤

1. 打开Cursor设置: `⌘/Ctrl + Shift + J`
2. 导航到: **General > Account**
3. 在"VS Code Import"下，点击"Import"按钮

### 4.3 导入内容

- ✅ 扩展（Extensions）
- ✅ 主题（Themes）
- ✅ 设置（Settings）
- ✅ 键绑定（Key Bindings）

---

## 5. Claude Skills 支持情况

### 5.1 当前状态

**Claude Skills支持**: ⚠️ **需要Nightly版本**

### 5.2 启用步骤

#### 步骤1: 切换到Nightly更新渠道

1. 打开Cursor设置: `⌘/Ctrl + Shift + J`
2. 选择 **Beta** 选项卡
3. 将更新渠道设置为 **Nightly**
4. 等待更新完成后重启Cursor

#### 步骤2: 开启Agent Skills

1. 打开Cursor设置 → **Rules**
2. 找到 **Import Settings** 部分
3. 切换 **Agent Skills** 开关将其开启

#### 步骤3: 安装Skills

启用后，可以使用 **OpenSkills** 等工具安装和管理Claude Skills。

### 5.3 替代方案（如果没有Skills）

如果Claude Skills不可用，可以使用以下替代方案：

#### 方案1: 使用Rules + Commands组合

通过Rules定义项目规范，通过Commands执行操作，实现类似Skills的功能。

**示例**:
```markdown
# .cursor/rules/market-analysis-workflow.md
---
name: "市场分析工作流"
type: "agent-requested"
---

# 市场分析工作流

## 标准流程
1. 数据源检测
2. 市场趋势分析
3. 主线轮动研究
4. 投资标的筛选
5. 生成报告

## 使用的工具
- MarketTrendAnalyzer
- TrendAnalyzer
- CandidatePoolBuilder
```

#### 方案2: 使用MCP Servers

利用现有的MCP Server架构，将功能封装成工具供AI调用。

**优势**:
- ✅ 已实现，无需额外配置
- ✅ 支持工作流集成
- ✅ 统一接口

**示例**:
```python
# 在Cursor Chat中
"请使用market.trend工具分析当前市场趋势"
```

#### 方案3: 使用Agent模式

Cursor的Agent模式允许AI代理自动执行多步骤任务，类似于Claude Skills。

**使用方式**:
1. 切换到Agent模式: `⌘/Ctrl + Alt + Tab`
2. 在Agent面板中描述任务
3. AI会自动执行多步骤操作

---

## 6. TRQuant项目应用建议

### 6.1 立即实施（高优先级）

#### 1. 创建Rules目录结构

```bash
mkdir -p .cursor/rules
```

#### 2. 创建核心Rules

- ✅ `coding-standards.md` - 编码规范
- ✅ `architecture.md` - 架构规范
- ✅ `notebook-development.md` - Notebook开发规范
- ✅ `market-trend-analysis.md` - 市场趋势分析规范

#### 3. 配置Rules类型

- **always**: 编码规范、架构规范
- **auto-attached**: Notebook开发规范（自动附加到`.ipynb`文件）
- **agent-requested**: 市场趋势分析规范（需要时请求）

### 6.2 中期实施（中优先级）

#### 1. 创建Commands

- 运行回测命令
- 生成报告命令
- 验证代码命令

#### 2. 配置Import Settings

- 从VS Code导入现有设置（如果有）
- 统一开发环境配置

### 6.3 长期实施（低优先级）

#### 1. 评估Claude Skills

- 切换到Nightly版本
- 测试Claude Skills功能
- 评估是否比现有MCP Server方案更好

#### 2. 优化Agent模式使用

- 探索Agent模式的多步骤任务能力
- 创建标准化的Agent任务模板

---

## 7. 实施计划

### 阶段1: Rules设置（1-2小时）

**目标**: 创建核心Rules，指导AI行为

**步骤**:
1. 创建 `.cursor/rules/` 目录
2. 创建4个核心规则文件
3. 配置规则类型和标签
4. 测试规则是否生效

**验证**:
- 在Cursor Chat中询问编码规范，AI应引用Rules
- 创建新文件时，AI应遵循Rules中的规范

### 阶段2: Commands设置（30分钟）

**目标**: 创建常用Commands，提高效率

**步骤**:
1. 创建 `.cursor/commands/` 目录（如果需要）
2. 定义常用命令
3. 测试命令执行

**验证**:
- 在Chat中使用 `@command` 调用命令
- 验证命令是否正确执行

### 阶段3: Import Settings（15分钟）

**目标**: 统一开发环境

**步骤**:
1. 检查是否有VS Code配置
2. 如有，执行导入
3. 验证导入结果

### 阶段4: Claude Skills评估（可选，1-2小时）

**目标**: 评估Claude Skills的可用性和价值

**步骤**:
1. 切换到Nightly版本
2. 开启Agent Skills
3. 测试OpenSkills工具
4. 与现有MCP Server方案对比
5. 决定是否采用

---

## 8. 具体实施代码

### 8.1 创建Rules目录和文件

```bash
# 创建目录
mkdir -p .cursor/rules

# 创建核心规则文件
touch .cursor/rules/coding-standards.md
touch .cursor/rules/architecture.md
touch .cursor/rules/notebook-development.md
touch .cursor/rules/market-trend-analysis.md
```

### 8.2 示例Rules文件内容

我已经在文档中提供了完整的Rules示例，可以直接使用。

### 8.3 验证Rules是否生效

在Cursor Chat中测试：
```
"请按照TRQuant编码规范创建一个新的Python模块"
```

AI应该：
- ✅ 引用Rules中的规范
- ✅ 遵循命名规范
- ✅ 遵循导入规范
- ✅ 遵循架构规范

---

## 9. 最佳实践建议

### 9.1 Rules最佳实践

1. **保持Rules简洁**: 每个Rules文件聚焦一个主题
2. **使用标签**: 方便分类和搜索
3. **定期更新**: 随着项目发展更新Rules
4. **版本控制**: 将Rules提交到Git

### 9.2 Commands最佳实践

1. **命令命名清晰**: 使用描述性名称
2. **提供文档**: 每个命令都有清晰的描述
3. **错误处理**: 命令应该处理错误情况

### 9.3 与现有架构的集成

1. **Rules补充MCP Server**: Rules提供规范，MCP Server提供功能
2. **Commands调用现有脚本**: 封装现有的Python脚本
3. **保持一致性**: Rules中的规范应该与代码库一致

---

## 10. 总结

### 10.1 核心发现

1. **Rules功能成熟**: 可以立即使用，对项目很有价值
2. **Commands功能可用**: 可以提高开发效率
3. **Claude Skills需要Nightly**: 当前稳定版不支持，需要评估
4. **MCP Server是好的替代**: 如果Skills不可用，MCP Server方案已经很好

### 10.2 推荐行动

**立即行动**:
1. ✅ 创建 `.cursor/rules/` 目录
2. ✅ 创建4个核心Rules文件
3. ✅ 测试Rules是否生效

**中期行动**:
1. 创建常用Commands
2. 配置Import Settings

**长期评估**:
1. 评估Claude Skills（如果需要）
2. 优化Agent模式使用

### 10.3 预期收益

- ✅ **提高代码一致性**: Rules确保AI遵循项目规范
- ✅ **提高开发效率**: Commands自动化常用操作
- ✅ **减少错误**: 规范化的开发流程减少错误
- ✅ **更好的AI辅助**: AI更理解项目上下文

---

**最后更新**: 2026-01-06  
**下一步**: 创建Rules文件并测试
