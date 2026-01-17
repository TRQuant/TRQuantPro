# -*- coding: utf-8 -*-
"""
用户使用指南面板
详细的平台使用说明和操作指南
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QTextEdit, QTabWidget, QTreeWidget,
    QTreeWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from gui.styles.theme import Colors, Typography, ButtonStyles, CardStyles


class UserGuidePanel(QWidget):
    """用户使用指南面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标题栏
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_DARK};
                border-bottom: 1px solid {Colors.BORDER_PRIMARY};
            }}
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 20)
        
        title = QLabel("📖 韬睿量化平台使用指南")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 700;
            color: {Colors.TEXT_PRIMARY};
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addWidget(header)
        
        # 内容区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {Colors.BG_SECONDARY};
            }}
        """)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 32, 40, 32)
        content_layout.setSpacing(24)
        
        # 使用标签页组织内容
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 12px;
                margin-top: -1px;
            }}
            QTabBar::tab {{
                background-color: transparent;
                color: {Colors.TEXT_MUTED};
                padding: 12px 24px;
                border: none;
                border-bottom: 2px solid transparent;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                color: {Colors.PRIMARY};
                border-bottom-color: {Colors.PRIMARY};
            }}
        """)
        
        # 平台概述
        overview_tab = self.create_overview_tab()
        tabs.addTab(overview_tab, "📋 平台概述")
        
        # 工作流程
        workflow_tab = self.create_workflow_tab()
        tabs.addTab(workflow_tab, "🔄 工作流程")
        
        # 文件管理系统
        files_tab = self.create_files_tab()
        tabs.addTab(files_tab, "📂 文件管理")
        
        # Cursor开发指南
        cursor_tab = self.create_cursor_tab()
        tabs.addTab(cursor_tab, "💻 Cursor开发")
        
        # PTrade策略开发
        ptrade_tab = self.create_ptrade_tab()
        tabs.addTab(ptrade_tab, "🚀 PTrade策略")
        
        # 行业调研资源
        research_tab = self.create_research_tab()
        tabs.addTab(research_tab, "🔬 行业调研")
        
        content_layout.addWidget(tabs)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def create_overview_tab(self) -> QWidget:
        """创建平台概述标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # 平台介绍
        intro_text = """
# 韬睿量化专业版 - 平台概述

## 🎯 平台定位

**韬睿量化专业版**是一个面向A股市场的机构级量化研究与实盘交易平台，提供从数据获取、因子分析、策略开发、回测验证到实盘交易的全流程解决方案。

## ✨ 核心优势

### 1. 本地运行与Broker直连
- **本地部署**：所有数据和处理都在本地，保护策略隐私
- **券商直连**：直接对接国金证券PTrade和QMT系统，无需第三方平台
- **实时交易**：支持模拟、纸面、实盘三种交易模式

### 2. 深耕A股市场
- **A股专用**：针对A股交易规则、市场特征深度优化
- **多数据源**：集成JQData、TuShare、Wind等主流数据源
- **本土化因子**：内置50+个A股量化因子，覆盖价值、成长、动量、质量等维度

### 3. 专业开发流程
- **AI辅助**：集成Cursor AI，智能生成策略代码
- **多平台支持**：PTrade、QMT、QuantConnect+IBKR统一管理
- **版本控制**：Git自动提交，策略版本可追溯

### 4. 开放多数据源
- **灵活接入**：支持多种数据源，可根据需求切换
- **数据缓存**：Parquet格式本地缓存，提升查询速度
- **统一接口**：DataCenter统一数据访问接口

## 🏗️ 系统架构

```
┌─────────────────────────────────────────┐
│        韬睿量化专业版平台                │
├─────────────────────────────────────────┤
│  GUI应用 (PyQt6)                         │
│  ├─ 投研分析                             │
│  ├─ AI策略助手                           │
│  ├─ 策略开发                             │
│  ├─ 回测验证                             │
│  └─ 实盘交易                             │
├─────────────────────────────────────────┤
│  Web Dashboard (Flask)                   │
│  ├─ 文件管理系统                         │
│  ├─ 策略代码管理                         │
│  └─ 回测报告查看                         │
├─────────────────────────────────────────┤
│  Bridge Services (FastAPI)               │
│  ├─ PTrade Bridge                        │
│  ├─ QMT Bridge                          │
│  └─ QuantConnect Bridge                 │
├─────────────────────────────────────────┤
│  数据层                                  │
│  ├─ JQData / TuShare / Wind              │
│  └─ 本地缓存 (Parquet)                   │
└─────────────────────────────────────────┘
```

## 📊 主要功能模块

1. **投研分析**：量化因子库、市场概览、智能推荐
2. **AI策略助手**：多因子策略生成、Cursor集成
3. **策略开发**：代码编辑、参数配置、版本管理
4. **回测验证**：本地回测、券商回测、绩效分析
5. **实盘交易**：PTrade/QMT对接、风险控制、订单管理
6. **文件管理**：策略代码、回测报告、研究文档统一管理
7. **系统设置**：数据源配置、系统状态监控
"""
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setMarkdown(intro_text)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
                line-height: 1.6;
            }}
        """)
        layout.addWidget(text_edit)
        
        return tab
    
    def create_workflow_tab(self) -> QWidget:
        """创建工作流程标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        workflow_text = """
# 🔄 完整工作流程

## 标准策略开发流程

### 第一步：数据获取与因子分析

1. **启动系统**
   - 点击"系统设置" → "启动系统"
   - 系统会自动连接JQData数据源

2. **投研分析**
   - 进入"投研分析"模块
   - 查看市场概览和量化因子库
   - 选择感兴趣的因子进行深入分析

3. **因子构建**
   - 在"投研分析"中选择因子分类
   - 查看因子计算公式和解读
   - 使用多因子选股器筛选股票池

### 第二步：策略开发（Cursor + AI）

1. **打开AI策略助手**
   - 进入"AI策略助手"模块
   - 选择目标平台（PTrade/QMT/QuantConnect）

2. **配置策略参数**
   - 选择股票池（如：沪深300、中证500、自定义）
   - 设置调仓周期（如：每20个交易日）
   - 配置因子权重（价值、成长、动量、波动）
   - 设置风险控制参数

3. **生成策略代码**
   - 点击"生成Prompt"按钮
   - 复制Prompt到Cursor
   - 在Cursor中使用AI生成策略代码
   - 将生成的代码粘贴回"策略代码"标签页
   - 点击"保存策略"自动保存到文件管理系统

### 第三步：回测验证

1. **本地回测**
   - 进入"回测验证"模块
   - 选择策略和股票池
   - 设置回测日期范围（注意账号权限限制）
   - 点击"开始回测"
   - 查看回测结果：收益曲线、交易记录、风控报告

2. **券商平台回测**
   - 在PTrade/QMT平台运行回测
   - 回测结果会自动同步到Bridge服务
   - 在Dashboard中查看回测报告

3. **结果分析**
   - 查看关键指标：年化收益、夏普比率、最大回撤、胜率
   - 分析交易记录和持仓变化
   - 识别策略优缺点

### 第四步：策略迭代

1. **分析回测结果**
   - 在Cursor中打开回测结果JSON文件
   - 使用AI分析回测报告
   - 识别需要改进的地方

2. **优化策略**
   - 调整因子权重
   - 修改调仓频率
   - 优化风险控制参数
   - 重新生成策略代码

3. **再次回测**
   - 使用优化后的策略重新回测
   - 对比前后回测结果
   - 持续迭代直到满意

### 第五步：实盘交易（可选）

1. **风险检查**
   - 确保回测结果满足风控要求
   - 检查策略稳定性

2. **部署到券商平台**
   - 通过PTrade/QMT Bridge部署策略
   - 先在模拟环境测试
   - 确认无误后切换到实盘

3. **监控与管理**
   - 在"实盘交易"模块监控持仓和订单
   - 查看交易日志和风险指标
   - 根据市场变化调整策略

## 🔁 迭代循环

```
策略开发 → 回测验证 → 结果分析 → 策略优化 → 再次回测 → ...
```

每次迭代都会：
- 保存策略代码到文件管理系统
- 保存回测结果JSON
- 生成HTML报告
- Git自动提交（如果启用）

## 📝 注意事项

1. **数据源权限**：JQData免费账号有日期范围限制，注意在允许范围内回测
2. **策略兼容性**：PTrade策略需要符合PTrade Python接口规范
3. **版本管理**：重要策略修改前建议先备份
4. **风险控制**：实盘前务必充分回测和模拟交易
"""
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setMarkdown(workflow_text)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
                line-height: 1.6;
            }}
        """)
        layout.addWidget(text_edit)
        
        return tab
    
    def create_files_tab(self) -> QWidget:
        """创建文件管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        files_text = """
# 📂 文件管理系统使用指南

## 🌐 访问方式

1. **从GUI应用访问**
   - 在首页点击"文件管理系统"按钮
   - 或点击"打开Dashboard"快捷操作

2. **直接访问**
   - 浏览器打开：`http://localhost:5000`
   - 或运行：`python start_dashboard.py`

## 📁 目录结构

### 策略代码目录

```
strategies/
├── examples/          # 本地示例策略
├── ptrade/            # PTrade策略代码
├── qmt/               # QMT策略代码
└── quantconnect/      # QuantConnect+IBKR策略
```

### 回测结果目录

```
data/
├── ptrade/
│   ├── backtest_results/    # PTrade回测结果JSON
│   └── trade_records/       # PTrade交易记录
├── qmt/
│   ├── backtest_results/    # QMT回测结果
│   └── trade_records/       # QMT交易记录
└── quantconnect/
    ├── backtest_results/    # QuantConnect回测结果
    └── trade_records/       # QuantConnect交易记录
```

### 报告目录

```
results/               # 本地回测HTML报告
```

### 研究文档目录

```
docs/                  # 研究文档、PDF、Markdown
```

## 🔍 功能说明

### 1. 策略代码管理

- **查看策略列表**：在"策略代码"页面查看所有策略
- **平台筛选**：按平台（本地/PTrade/QMT/QuantConnect）筛选
- **查看代码**：点击策略卡片查看完整代码
- **版本管理**：策略文件自动Git版本控制

### 2. 回测报告查看

- **报告列表**：在"回测报告"页面查看所有报告
- **打开报告**：点击报告卡片在浏览器中打开HTML报告
- **下载报告**：支持下载PDF格式报告

### 3. 研究文档管理

- **文档分类**：
  - 平台总览与架构
  - 策略研究与回测
  - 实盘交易与券商集成
- **在线查看**：Markdown文档自动渲染为HTML
- **下载文档**：支持下载原始文件

### 4. 文件同步

- **自动同步**：策略代码保存后自动同步到Dashboard
- **Bridge服务**：PTrade/QMT回测结果自动同步
- **Git提交**：重要文件自动Git提交（如果启用）

## 💡 使用技巧

1. **快速查找**：使用浏览器搜索功能（Ctrl+F）查找策略
2. **代码查看**：点击策略卡片查看完整代码，支持复制
3. **报告对比**：打开多个报告标签页进行对比分析
4. **文档阅读**：Markdown文档支持目录导航和搜索

## 🔗 与Cursor集成

1. **打开策略文件**
   - 在Dashboard中点击策略
   - 复制文件路径
   - 在Cursor中打开该文件

2. **查看回测结果**
   - 回测结果JSON保存在 `data/*/backtest_results/`
   - 在Cursor中打开JSON文件
   - 使用AI分析回测结果

3. **策略迭代**
   - 修改策略代码
   - 保存后自动同步到Dashboard
   - 重新回测查看效果
"""
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setMarkdown(files_text)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
                line-height: 1.6;
            }}
        """)
        layout.addWidget(text_edit)
        
        return tab
    
    def create_cursor_tab(self) -> QWidget:
        """创建Cursor开发标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        cursor_text = """
# 💻 Cursor开发工作流程

## 🎯 核心工作模式

**韬睿量化平台 + Cursor = 高效策略开发**

在Cursor中使用AI生成策略代码，然后通过平台进行回测和迭代。

## 📋 详细步骤

### 第一步：生成策略Prompt

1. **打开AI策略助手**
   - 在GUI应用中进入"AI策略助手"
   - 或直接访问：`http://localhost:5000` → "AI策略助手"

2. **配置策略参数**
   - 选择目标平台：PTrade / QMT / QuantConnect
   - 选择股票池：沪深300 / 中证500 / 自定义
   - 设置调仓周期：如每20个交易日
   - 配置因子权重：
     - 价值因子：0.25
     - 成长因子：0.25
     - 动量因子：0.30
     - 波动因子：0.20

3. **生成Prompt**
   - 点击"生成Prompt"按钮
   - 在"Prompt预览"标签页查看生成的Prompt
   - 点击"复制Prompt"按钮

### 第二步：在Cursor中生成代码

1. **打开Cursor**
   - 在Cursor中打开项目目录
   - 创建新文件或打开现有策略文件

2. **使用AI生成代码**
   - 粘贴刚才复制的Prompt
   - 使用Cursor的AI功能（Cmd/Ctrl + K）
   - 让AI根据Prompt生成完整的策略代码

3. **代码要求**
   - 必须符合PTrade Python接口规范
   - 包含必要的函数：`init()`, `before_trading()`, `handle_data()`
   - 代码要有清晰的中文注释
   - 参数要集中放在文件开头

### 第三步：保存策略代码

1. **复制生成的代码**
   - 从Cursor中复制完整代码

2. **粘贴到平台**
   - 回到"AI策略助手"
   - 切换到"策略代码"标签页
   - 粘贴代码
   - 点击"保存策略"

3. **自动保存**
   - 代码会自动保存到对应的平台目录：
     - PTrade策略 → `strategies/ptrade/`
     - QMT策略 → `strategies/qmt/`
     - QuantConnect策略 → `strategies/quantconnect/`

### 第四步：回测验证

1. **本地回测**
   - 在"回测验证"模块运行回测
   - 查看回测结果和指标

2. **券商平台回测**
   - 将策略代码复制到PTrade/QMT
   - 在券商平台运行回测
   - 回测结果会自动同步到Bridge服务

### 第五步：分析回测结果

1. **查看回测结果**
   - 回测结果JSON保存在：
     - 本地回测：`results/backtest_*.json`
     - PTrade回测：`data/ptrade/backtest_results/`
     - QMT回测：`data/qmt/backtest_results/`

2. **在Cursor中分析**
   - 打开回测结果JSON文件
   - 使用Cursor AI分析回测结果：
     ```
     请分析这个回测结果，重点关注：
     1. 年化收益和夏普比率
     2. 最大回撤和风险指标
     3. 交易频率和胜率
     4. 需要改进的地方
     ```

3. **策略优化**
   - 根据AI分析结果调整策略
   - 修改因子权重或参数
   - 重新生成代码
   - 再次回测

## 🔄 迭代循环

```
生成Prompt → Cursor生成代码 → 保存策略 → 回测验证 
    → 分析结果 → 优化策略 → 重新生成 → ...
```

## 💡 Cursor使用技巧

1. **系统Prompt**
   - 在Cursor设置中添加系统Prompt
   - 参考：`prompts/system_prompt.md`
   - 让AI理解"韬睿PTrade策略工程师"的角色

2. **代码片段**
   - 保存常用的策略代码片段
   - 在生成新策略时复用

3. **多文件编辑**
   - 同时打开策略代码和回测结果
   - 对比分析不同版本

4. **AI对话**
   - 使用Cursor Chat功能
   - 询问策略优化建议
   - 获取因子解释

## 📝 注意事项

1. **PTrade接口规范**：生成的代码必须符合PTrade Python接口
2. **代码格式**：保持代码格式统一，便于维护
3. **版本管理**：重要修改前先Git提交
4. **测试验证**：生成代码后先在本地回测验证
"""
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setMarkdown(cursor_text)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
                line-height: 1.6;
            }}
        """)
        layout.addWidget(text_edit)
        
        return tab
    
    def create_ptrade_tab(self) -> QWidget:
        """创建PTrade策略开发标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        ptrade_text = '''
# 🚀 PTrade策略开发要求

## 📌 PTrade平台简介

**PTrade（恒生PTrade）**是国金证券提供的专业量化交易平台，支持Python策略开发。

## 🔧 开发环境要求

- **Python版本**：Python 3.11
- **接口文档**：http://180.169.107.9:7766/hub/help/api?weworkcfmcode
- **策略目录**：PTrade安装目录下的策略文件夹

## 📋 策略代码规范

### 必需函数

PTrade策略必须实现以下函数：

```python
def init(context):
    """策略初始化函数，在策略启动时调用一次"""
    # 设置回测周期
    # 设置标的池
    # 初始化参数
    pass

def before_trading(context):
    """每日开盘前执行，用于检查持仓、生成当日目标持仓"""
    pass

def handle_data(context, data):
    """接收当日行情数据，在调仓日生成买卖指令"""
    pass
```

### 常用接口

```python
# 获取价格数据
get_price(security, start_date, end_date, frequency='daily', fields=['close'])

# 获取财务数据
get_fundamentals(query(...), date)

# 下单函数
order_target_percent(security, target_percent)  # 按目标比例下单
order(security, volume)  # 按数量下单
order_value(security, value)  # 按金额下单

# 获取持仓
context.portfolio.positions  # 当前持仓
context.portfolio.total_value  # 总资产
context.portfolio.available_cash  # 可用现金
```

### 参数配置区域

所有参数应集中放在文件开头：

```python
# ========== 策略参数配置 ==========
REBALANCE_FREQ = 20  # 调仓周期（交易日）
MAX_POSITIONS = 30   # 最大持仓数
POSITION_SIZE = 0.03  # 单只股票仓位（3%）
COMMISSION_RATE = 0.0003  # 手续费率（万3）

# 因子权重
FACTOR_WEIGHTS = {
    'value': 0.25,
    'growth': 0.25,
    'momentum': 0.30,
    'volatility': 0.20
}
```

## 🎯 多因子策略模板

### 标准多因子策略结构

```python
def init(context):
    # 1. 设置标的池
    context.universe = ['600519.XSHG', '000858.XSHE', ...]
    
    # 2. 设置调仓周期
    context.rebalance_freq = 20
    context.last_rebalance = None
    
    # 3. 初始化因子计算器
    context.factor_calculator = FactorCalculator()

def before_trading(context):
    # 检查是否需要调仓
    today = context.current_dt.date()
    if context.last_rebalance is None or \
       (today - context.last_rebalance).days >= context.rebalance_freq:
        context.should_rebalance = True
    else:
        context.should_rebalance = False

def handle_data(context, data):
    if not context.should_rebalance:
        return
    
    # 1. 计算因子
    factors = context.factor_calculator.calculate(context.universe)
    
    # 2. 因子合成与打分
    scores = combine_factors(factors)
    
    # 3. 选股
    selected = select_stocks(scores, MAX_POSITIONS)
    
    # 4. 调仓
    rebalance(context, selected)
    
    context.last_rebalance = context.current_dt.date()
```

## ⚠️ 注意事项

1. **接口兼容性**
   - 确保使用的接口在PTrade环境中可用
   - 如有不确定，参考PTrade接口文档

2. **数据获取**
   - 使用PTrade提供的数据接口
   - 注意数据延迟和权限限制

3. **交易规则**
   - 遵守A股交易规则（T+1、涨跌停等）
   - 注意交易时间限制

4. **错误处理**
   - 添加异常处理，避免策略崩溃
   - 记录关键日志

5. **性能优化**
   - 避免在循环中频繁调用数据接口
   - 使用缓存减少重复计算

## 🔗 与平台集成

1. **代码生成**
   - 使用"AI策略助手"生成PTrade策略代码
   - 确保生成的代码符合PTrade规范

2. **代码保存**
   - 保存到 `strategies/ptrade/` 目录
   - 文件名使用下划线命名：`mf_strategy_001.py`

3. **回测验证**
   - 先在本地回测验证逻辑
   - 再在PTrade平台回测
   - 对比结果确保一致性

4. **Bridge服务**
   - PTrade回测结果自动同步到Bridge
   - 在Dashboard中查看回测报告
'''
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setMarkdown(ptrade_text)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
                line-height: 1.6;
            }}
        """)
        layout.addWidget(text_edit)
        
        return tab
    
    def create_research_tab(self) -> QWidget:
        """创建行业调研标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        research_text = """
# 🔬 行业调研资源

## 🌟 韬睿量化核心优势

**韬睿量化拥有高端猎头资源，可以接触行业相关公司管理层，进行深度行业调研。**

## 📊 行业调研价值

### 1. 获取一手信息

- **管理层访谈**：直接与公司管理层沟通，了解公司战略和发展方向
- **行业洞察**：深入了解行业趋势、竞争格局、政策影响
- **数据验证**：验证量化模型发现的信号，提高策略可靠性

### 2. 提升策略精准度

- **因子验证**：通过调研验证量化因子的有效性
- **风险识别**：提前识别行业和公司层面的风险
- **机会发现**：发现市场尚未充分定价的投资机会

### 3. 优化投资决策

- **基本面结合**：将量化信号与基本面分析结合
- **策略调整**：根据调研结果调整策略参数和权重
- **风险控制**：基于调研信息优化风险控制规则

## 🔄 调研与策略开发的结合

### 工作流程

```
量化信号发现 → 行业调研验证 → 策略参数调整 → 回测验证 → 实盘交易
```

### 具体应用

1. **因子构建阶段**
   - 量化模型发现某个行业因子有效
   - 通过行业调研验证因子背后的逻辑
   - 确认因子可持续性后纳入策略

2. **策略优化阶段**
   - 回测发现策略在某个行业表现不佳
   - 通过调研了解行业特殊因素
   - 调整策略参数或增加行业过滤条件

3. **风险控制阶段**
   - 识别潜在风险行业或公司
   - 通过调研确认风险程度
   - 在策略中增加风险规避规则

## 💡 平台技术支持

### 提高开发效率

1. **AI辅助开发**
   - Cursor AI快速生成策略代码
   - 减少重复性编码工作
   - 专注于策略逻辑和参数优化

2. **自动化流程**
   - 策略代码自动保存和管理
   - 回测结果自动同步和分析
   - 减少人工操作，提高效率

3. **数据整合**
   - 统一数据接口，快速获取市场数据
   - 多数据源对比验证
   - 数据缓存提升查询速度

### 提高策略精准度

1. **多因子框架**
   - 50+个量化因子覆盖多个维度
   - 因子有效性验证工具
   - 因子组合优化建议

2. **回测分析**
   - 详细的回测报告和指标分析
   - 交易记录和持仓变化追踪
   - AI辅助结果解读

3. **迭代优化**
   - 快速回测验证策略改进
   - 版本对比分析
   - 持续优化机制

## 📝 使用建议

1. **定期调研**：建立定期行业调研机制
2. **记录整理**：将调研结果整理成文档，存入知识库
3. **策略更新**：根据调研结果及时更新策略
4. **效果评估**：评估调研对策略改进的实际效果

## 🔗 相关资源

- **A股实操手册**：包含行业分析框架和案例
- **研究文档**：在文件管理系统中查看历史研究文档
- **策略库**：参考其他策略的行业配置
"""
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setMarkdown(research_text)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 16px;
                font-size: 14px;
                line-height: 1.6;
            }}
        """)
        layout.addWidget(text_edit)
        
        return tab

