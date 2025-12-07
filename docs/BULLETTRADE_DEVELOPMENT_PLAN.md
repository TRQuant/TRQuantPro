# BulletTrade策略回测验证与实盘交易部署整合方案 - 开发计划

## 📋 项目概述

基于《BulletTrade策略回测验证与实盘交易部署整合方案.pdf》和 [BulletTrade 官方文档](https://bullettrade.cn/)，构建完整的回测验证与实盘交易模块，实现策略从开发→回测→实盘的全生命周期管理。

**重要**：本项目将采用 **AI Agent 协作框架**（参考 FoundationAgents 最佳实践），确保生成高质量、可运行的代码。详见 `docs/AGENT_INTEGRATION_PLAN.md`。

## 🚀 BulletTrade 官方四步流程

基于官方文档 https://bullettrade.cn/ ：

### 第一步：准备环境
```bash
pip install bullet-trade
# Windows QMT 支持: pip install "bullet-trade[qmt]"
```

### 第二步：启动研究
```bash
bullet-trade lab  # 启动 JupyterLab
# 配置文件: ~/.bullet-trade/setting.json
# 环境变量: ~/bullet-trade/.env
```

### 第三步：运行回测
```bash
bullet-trade backtest demo_strategy.py --start 2025-01-01 --end 2025-06-01
```

### 第四步：实盘与远程
```bash
# 本地实盘
bullet-trade live demo_strategy.py --broker qmt

# 远程实盘
bullet-trade live demo_strategy.py --broker qmt-remote

# 启动服务器（Windows端）- 支持数据和交易
bullet-trade server --listen 0.0.0.0 --port 58620 --token secret --enable-data --enable-broker
```

### 其他功能
```bash
# 参数优化
bullet-trade optimize strategies/demo_strategy.py --params params.json --start 2020-01-01 --end 2023-12-31 --output optimization.csv

# 报告生成
bullet-trade report --input backtest_results --format html

# 研究环境
bullet-trade lab  # 启动 JupyterLab
```

> **完整文档**：参见 `docs/BULLETTRADE_OFFICIAL_DOCS.md` 和 [官方文档](https://bullettrade.cn/docs/)

## 🎯 核心目标

基于 [BulletTrade 官方文档](https://bullettrade.cn/docs/)：

1. **回测验证模块**：基于 BulletTrade 实现策略回测，支持聚宽 API 兼容
2. **参数优化模块**：多进程并行参数寻优 (`bullet-trade optimize`)
3. **实盘交易模块**：支持 QMT（本地/远程）、模拟券商
4. **数据源管理**：JQData、MiniQMT、TuShare、远程 QMT server
5. **AI分析模块**：LLM 自动生成回测和实盘分析报告
6. **报告生成**：HTML/Markdown 格式报告 (`bullet-trade report`)
7. **研究环境**：JupyterLab 集成 (`bullet-trade lab`)
8. **闭环流程**：策略开发→回测验证→参数优化→实盘交易→绩效反馈

---

## 📐 架构设计

### 模块结构

```
core/
├── bullettrade/                    # BulletTrade集成模块（新增）
│   ├── __init__.py
│   ├── bt_engine.py                # BulletTrade引擎封装
│   ├── jqdata_compat.py            # 聚宽API兼容层
│   └── data_provider_adapter.py    # 数据源适配器
│
├── backtest/                       # 回测模块（增强）
│   ├── __init__.py
│   ├── bt_run.py                   # 回测执行模块（新增）
│   ├── backtest_config.py          # 回测配置
│   └── backtest_result.py          # 回测结果数据结构
│
├── trading/                        # 交易模块（增强）
│   ├── trading_engine.py           # 实盘交易引擎（新增）
│   ├── broker/                     # 券商适配器（增强）
│   │   ├── base_broker.py          # 基础Broker接口
│   │   ├── qmt_broker.py           # QMT适配器（增强）
│   │   ├── ptrade_broker.py        # 恒生PTrade适配器（增强）
│   │   └── juejin_broker.py        # 掘金适配器（新增）
│   └── risk_control.py             # 风险控制模块（新增）
│
├── reporting/                      # 报告模块（新增）
│   ├── __init__.py
│   ├── report_generator.py         # 报告生成器（增强）
│   ├── ai_analyzer.py              # AI分析器（新增）
│   └── report_formatter.py         # 报告格式化（新增）
│
└── data/                           # 数据管理模块（新增）
    ├── __init__.py
    ├── backtest_storage.py         # 回测数据存储
    ├── live_storage.py             # 实盘数据存储
    └── snapshot_manager.py        # 持仓快照管理
```

### 目录结构

```
TRQuant/
├── strategies/                     # 策略代码目录
│   ├── my_strategy_v1.py
│   └── my_strategy_v2.py
│
├── backtests/                      # 回测结果存档
│   └── {strategy_name}/
│       ├── v1/
│       │   ├── config.yaml
│       │   ├── equity_curve.csv
│       │   ├── trades.csv
│       │   ├── report_v1.html
│       │   └── report_v1.md
│       └── v2/
│
├── live_trading/                   # 实盘运行数据
│   ├── logs/
│   │   └── live_YYYY-MM-DD.log
│   ├── snapshots/
│   │   └── positions_YYYY-MM-DD.csv
│   └── reports/
│       └── YYYY-MM-DD.md
│
└── modules/                        # 系统模块（保留兼容）
    ├── bt_run.py                   # 回测执行（CLI入口）
    ├── report_generator.py         # 报告生成（CLI入口）
    └── trading_engine.py          # 交易引擎（CLI入口）
```

---

## 🔧 开发阶段规划

### 阶段一：BulletTrade集成与回测模块（优先级：高）

**Agent工作流**：每个任务都将使用多Agent协作框架（Architect → CodeGenerator → QualityChecker）

#### 1.1 BulletTrade引擎封装
- [x] **任务1.1.1**：安装和配置BulletTrade依赖（已完成 v0.5.1）
  - **Agent工作流**：
    1. Architect Agent：设计依赖管理方案和配置结构
    2. Code Generator Agent：生成requirements.txt更新和配置模块
    3. Quality Checker Agent：检查依赖冲突和配置有效性
  - 添加`bullet-trade`到`requirements.txt`
  - 创建BulletTrade配置管理（`.env`支持）
  - 实现BulletTrade环境检测和初始化

- [x] **任务1.1.2**：实现聚宽API兼容层（已完成）
  - 创建`core/bullettrade/jqdata_compat.py`
  - 实现`from jqdata import *`兼容
  - 实现核心API：`initialize`, `handle_data`, `order`, `order_value`, `get_price`, `run_daily`等
  - 实现`context`对象（包含`portfolio`, `g`等）
  - 实现证券代码格式转换（聚宽格式 ↔ 本地格式）

- [x] **任务1.1.3**：数据源适配器（已完成）
  - 创建`core/bullettrade/data_provider_adapter.py`
  - 适配JQData、MiniQMT、TuShare等数据源
  - 实现`get_price`, `history`, `attribute_history`等数据接口
  - 支持数据源切换配置

#### 1.2 回测执行模块
- [x] **任务1.2.1**：回测配置管理（已完成）
  - 创建`core/backtest/backtest_config.py`
  - 定义回测参数（起止日期、频率、基准、滑点、手续费等）
  - 支持YAML/JSON配置文件解析

- [x] **任务1.2.2**：回测执行器（已完成）
  - 创建`core/backtest/bt_run.py`
  - 封装`bullet-trade backtest`命令调用
  - 实现Python API接口（`run_backtest(strategy_path, config)`）
  - 支持进度回调和结果监听
  - 自动保存回测结果到`backtests/`目录

- [x] **任务1.2.3**：回测结果处理（已完成）
  - 创建`core/backtest/backtest_result.py`
  - 解析BulletTrade HTML报告
  - 提取关键指标（收益率、回撤、Sharpe等）
  - 提取净值曲线、交易记录数据
  - 保存为CSV格式（`equity_curve.csv`, `trades.csv`）

#### 1.3 报告生成与AI分析
- [x] **任务1.3.1**：报告生成器增强（已完成）
  - 增强`core/report_generator.py`（或创建`core/reporting/report_generator.py`）
  - 支持从HTML报告提取数据和图表
  - 支持从CSV数据重新生成图表（matplotlib）
  - 生成Markdown格式报告模板

- [x] **任务1.3.2**：AI分析器（已完成）
  - 创建`core/reporting/ai_analyzer.py`
  - 实现LLM接口调用（OpenAI/本地模型）
  - 构建回测分析Prompt模板
  - 生成结构化分析报告（收益评估、风险分析、改进建议等）
  - 保存Markdown格式AI报告

#### 1.4 数据存储管理
- [x] **任务1.4.1**：回测数据存储（已完成）
  - 创建`core/data/backtest_storage.py`
  - 实现回测结果目录结构管理
  - 支持版本化存储（按策略名/版本号组织）
  - 实现数据查询和对比接口

#### 1.5 参数优化（基于官方 `bullet-trade optimize`）
- [ ] **任务1.5.1**：参数优化模块
  - 创建`core/bullettrade/optimizer.py`
  - 封装 `bullet-trade optimize` CLI
  - 支持 JSON 格式参数配置
  - 支持多进程并行寻优
  - 输出优化结果 CSV

#### 1.6 报告生成（基于官方 `bullet-trade report`）
- [ ] **任务1.6.1**：官方报告生成
  - 封装 `bullet-trade report` CLI
  - 支持 HTML/Markdown 格式
  - 集成到 VS Code Extension

---

### 阶段二：实盘交易模块（优先级：高）

#### 2.1 实盘交易引擎
- [ ] **任务2.1.1**：交易引擎核心
  - 创建`core/trading/trading_engine.py`
  - 实现策略加载和初始化
  - 实现实时行情订阅和回调
  - 实现交易信号执行流程
  - 支持多策略实例管理

- [ ] **任务2.1.2**：Broker适配器增强
  - 创建`core/trading/broker/base_broker.py`（统一接口）
  - 增强`core/trading/broker/qmt_broker.py`（支持BulletTrade）
  - 增强`core/broker/ptrade_broker.py`（支持BulletTrade）
  - 创建`core/trading/broker/juejin_broker.py`（掘金适配器）
  - 实现统一Broker接口：`connect()`, `place_order()`, `cancel_order()`, `get_positions()`等

- [ ] **任务2.1.3**：实时行情接入
  - 实现QMT实时行情订阅（xtdata）
  - 实现恒生PTrade行情接口
  - 实现掘金行情接口
  - 支持Tick/分钟线/日线多频率

#### 2.2 风险控制模块
- [ ] **任务2.2.1**：风控引擎
  - 创建`core/trading/risk_control.py`
  - 实现净值回撤监控
  - 实现单票止损/止盈
  - 实现每日最大亏损限制
  - 实现持仓集中度控制
  - 支持紧急平仓机制

- [ ] **任务2.2.2**：日志监控
  - 增强`core/trading/trade_logger.py`
  - 实现实时日志记录（交易、成交、资金变动）
  - 实现异常告警（邮件/短信/企业微信）
  - 支持日志轮转和归档

#### 2.3 实盘数据管理
- [ ] **任务2.3.1**：持仓快照管理
  - 创建`core/data/snapshot_manager.py`
  - 实现每日收盘后持仓快照
  - 保存交易流水（`trades_YYYYMMDD.csv`）
  - 保存持仓明细（`positions_YYYYMMDD.csv`）
  - 实现历史快照查询

- [ ] **任务2.3.2**：实盘数据存储
  - 创建`core/data/live_storage.py`
  - 实现实盘日志存储（`live_trading/logs/`）
  - 实现快照存储（`live_trading/snapshots/`）
  - 实现报告存储（`live_trading/reports/`）

#### 2.4 AI实盘日报
- [ ] **任务2.4.1**：日报生成
  - 增强`core/reporting/ai_analyzer.py`
  - 实现实盘日报Prompt模板
  - 分析当日盈亏、交易统计、持仓变化
  - 对比回测预期，生成偏差分析
  - 生成改进建议
  - 支持周报/月报汇总

---

### 阶段三：系统集成与优化（优先级：中）

#### 3.1 CLI工具链
- [ ] **任务3.1.1**：命令行工具
  - 创建`modules/bt_run.py`（CLI入口）
  - 创建`modules/report_generator.py`（CLI入口）
  - 创建`modules/trading_engine.py`（CLI入口）
  - 实现参数解析和帮助信息

#### 3.2 GUI集成
- [ ] **任务3.2.1**：VS Code Extension集成
  - 在`extension/src/views/`中创建回测面板
  - 在`extension/src/views/`中创建实盘监控面板
  - 实现回测配置UI
  - 实现实盘状态监控UI
  - 实现报告查看UI

- [ ] **任务3.2.2**：PyQt6 GUI集成
  - 增强`gui/widgets/backtest_panel.py`（支持BulletTrade）
  - 创建`gui/widgets/live_trading_panel.py`（实盘监控）
  - 实现策略选择、参数配置、运行监控

#### 3.3 工作流集成
- [ ] **任务3.3.1**：8步工作流增强
  - 在`core/workflow_orchestrator.py`中集成回测步骤
  - 在`core/workflow_orchestrator.py`中集成实盘部署步骤
  - 实现自动化回测→评审→部署流程

---

### 阶段四：扩展功能（优先级：低）

#### 4.1 多市场支持
- [ ] **任务4.1.1**：期货/期权接口
  - 研究CTP接口集成
  - 研究恒生UFT接口
  - 实现多市场Broker适配

#### 4.2 可视化监控
- [ ] **任务4.2.1**：Web Dashboard
  - 实现Flask/Django Web界面
  - 实时显示策略业绩曲线
  - 持仓盈亏监控
  - 交易告警推送

#### 4.3 AI智能决策
- [ ] **任务4.3.1**：AI策略优化
  - 实现AI参数优化
  - 实现AI策略生成
  - 实现多模态策略（融合新闻、公告等）

---

## 📝 技术实现细节

### 1. BulletTrade集成

#### 1.1 依赖安装
```python
# requirements.txt
bullet-trade>=0.1.0  # 需要确认实际版本
```

#### 1.2 聚宽API兼容
```python
# core/bullettrade/jqdata_compat.py
class JQDataCompat:
    """聚宽API兼容层"""
    
    def initialize(self, context):
        """策略初始化"""
        pass
    
    def handle_data(self, context, data):
        """数据处理"""
        pass
    
    def order(self, security, amount):
        """下单"""
        pass
    
    def get_price(self, security, count, unit, fields):
        """获取价格"""
        pass
```

#### 1.3 数据源适配
```python
# core/bullettrade/data_provider_adapter.py
class DataProviderAdapter:
    """数据源适配器"""
    
    def __init__(self, provider: str):
        self.provider = provider  # 'jqdata', 'miniqmt', 'tushare'
    
    def get_price(self, security, start_date, end_date):
        """获取历史价格"""
        pass
```

### 2. 回测执行

#### 2.1 配置结构
```python
# core/backtest/backtest_config.py
@dataclass
class BulletTradeBacktestConfig:
    strategy_path: str
    start_date: str
    end_date: str
    frequency: str = 'day'  # 'day' or 'minute'
    initial_capital: float = 1000000
    benchmark: str = '000300.XSHG'  # 沪深300
    commission_rate: float = 0.0003
    slippage: float = 0.001
    data_provider: str = 'jqdata'
```

#### 2.2 执行接口
```python
# core/backtest/bt_run.py
def run_backtest(
    strategy_path: str,
    config: BulletTradeBacktestConfig,
    output_dir: Optional[str] = None
) -> BacktestResult:
    """执行BulletTrade回测"""
    pass
```

### 3. 实盘交易

#### 3.1 Broker接口
```python
# core/trading/broker/base_broker.py
class BaseBroker(ABC):
    """Broker基础接口"""
    
    @abstractmethod
    def connect(self) -> bool:
        """连接券商"""
        pass
    
    @abstractmethod
    def place_order(self, order: Order) -> str:
        """下单"""
        pass
    
    @abstractmethod
    def get_positions(self) -> List[Position]:
        """获取持仓"""
        pass
```

#### 3.2 交易引擎
```python
# core/trading/trading_engine.py
class TradingEngine:
    """实盘交易引擎"""
    
    def __init__(self, strategy_path: str, broker: BaseBroker):
        self.strategy_path = strategy_path
        self.broker = broker
    
    def start(self):
        """启动交易"""
        pass
    
    def stop(self):
        """停止交易"""
        pass
```

### 4. AI分析

#### 4.1 Prompt模板
```python
# core/reporting/ai_analyzer.py
BACKTEST_ANALYSIS_PROMPT = """
请分析以下回测结果：

策略信息：
- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: {initial_capital}

回测指标：
- 总收益率: {total_return}%
- 年化收益: {annual_return}%
- 最大回撤: {max_drawdown}%
- 夏普比率: {sharpe_ratio}
- 胜率: {win_rate}%

请从以下方面进行分析：
1. 收益风险评估
2. 交易行为分析
3. 策略优缺点
4. 改进建议
"""
```

---

## 🧪 测试计划

### 单元测试
- [ ] BulletTrade API兼容性测试
- [ ] 回测执行器测试
- [ ] Broker适配器测试
- [ ] AI分析器测试

### 集成测试
- [ ] 完整回测流程测试
- [ ] 实盘模拟测试（Mock Broker）
- [ ] 报告生成测试

### 端到端测试
- [ ] 策略开发→回测→实盘完整流程
- [ ] 多策略并行运行
- [ ] 异常处理和恢复

---

## 📊 进度跟踪

### 里程碑

- **M1**: BulletTrade集成完成（阶段一）
  - 预计时间：2周
  - 交付物：回测模块可用

- **M2**: 实盘交易模块完成（阶段二）
  - 预计时间：3周
  - 交付物：实盘交易可用

- **M3**: 系统集成完成（阶段三）
  - 预计时间：2周
  - 交付物：完整系统可用

---

## ⚠️ 风险与挑战

1. **BulletTrade依赖**：需要确认BulletTrade的稳定性和API文档完整性
2. **券商接口**：不同券商API差异较大，需要充分测试
3. **数据源**：需要确保数据源的稳定性和数据质量
4. **AI分析**：LLM调用成本和响应时间需要优化
5. **实盘风险**：需要完善的风控机制，避免实盘损失

---

## 📚 参考资料

1. BulletTrade GitHub项目
2. 聚宽API文档
3. 恒生PTrade文档
4. QMT接口文档
5. 掘金量化API文档

---

**文档版本**: v1.0  
**创建日期**: 2025-01-XX  
**最后更新**: 2025-01-XX

