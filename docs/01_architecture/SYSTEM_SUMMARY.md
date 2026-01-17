# TRQuant 十倍股早期识别系统 - 功能总结

> 版本: 1.0 | 更新日期: 2025-12-18

---

## 一、系统概述

TRQuant是一个基于A股市场的十倍股早期识别系统，通过多维度数据分析、阶段状态机、评分卡引擎等核心模块，实现对高成长潜力股票的系统化识别与跟踪。

### 核心理念

```
十倍股发展路径: S0(观察) → S1(验证) → S2(导入) → S3(放量) → S4(加速) → S5(成熟)

识别窗口: S1-S3阶段是最佳介入期
```

---

## 二、系统架构

### 2.1 模块构成

```
┌─────────────────────────────────────────────────────────────┐
│                    TRQuant 系统架构                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ 数据源层    │  │ 分析层      │  │ 展示层      │         │
│  │             │  │             │  │             │         │
│  │ - JQData    │  │ - 事件抽取  │  │ - Dashboard │         │
│  │ - AKShare   │  │ - 阶段判断  │  │ - 产业链图谱│         │
│  │ - AltData   │  │ - 评分卡    │  │ - 个股详情  │         │
│  │ - Mock      │  │ - 候选池    │  │ - 回测报告  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
│              ┌───────────▼───────────┐                     │
│              │    MCP Server层       │                     │
│              │    132个工具          │                     │
│              └───────────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 已注册模块 (16个)

| 模块ID | 名称 | 状态 | 功能 |
|--------|------|------|------|
| data_source | 数据源模块 | ✅ | 统一数据接入 |
| market | 市场分析模块 | ✅ | 市场状态分析 |
| workflow | 9步工作流 | ✅ | 投资流程管理 |
| backtest | 回测模块 | ✅ | 策略回测验证 |
| trquant_core | 核心服务器 | ✅ | MCP工具注册 |
| mongodb | MongoDB数据库 | ✅ | 持久化存储 |
| chroma | Chroma向量库 | ✅ | 向量检索 |
| cache_manager | 缓存管理器 | ✅ | L1/L2缓存 |
| redis | Redis缓存 | ✅ | 分布式缓存 |
| candidate_pool | 分层候选池 | ✅ | L0-L3四层筛选 |
| industry_chain | 产业链图谱 | ✅ | 上中下游关系 |
| strategy_pack | 策略插件层 | ✅ | 策略注册发现 |
| altdata_tier2 | 第二档数据源 | ✅ | 招投标/招聘 |
| tenbagger_eval | 十倍股评估体系 | ✅ | 7维度评估 |
| portfolio | 多策略组合 | ✅ | 组合管理执行 |
| tenbagger_gui | GUI面板 | ✅ | 可视化界面 |

---

## 三、核心功能流程

### 3.1 端到端数据流

```
数据获取 → 事件抽取 → 阶段判断 → 评分计算 → 候选筛选 → Tenbagger评估
    ↓          ↓          ↓          ↓          ↓           ↓
 财务/行情    RawDoc    S0-S5      7维度      L0-L3      S+/S/A/B/C/D
```

### 3.2 测试验证结果

| 测试项 | 状态 | 说明 |
|--------|------|------|
| 数据获取 | ✅ | 3只股票财务/行情/事件 |
| 阶段判断 | ✅ | S0-S5状态机正常 |
| 评分卡计算 | ✅ | 7维度评分正常 |
| 候选池筛选 | ✅ | L0→L1→L2→L3正常 |
| Tenbagger评估 | ✅ | 综合评估正常 |
| 产业链查询 | ✅ | 图谱查询正常 |
| 组合管理 | ✅ | 下单/持仓正常 |
| MCP工具 | ✅ | 132个工具可用 |
| GUI命令 | ✅ | 14个命令可用 |

**测试通过率: 100%**

---

## 四、MCP工具清单 (132个)

### 4.1 按类别统计

| 类别 | 工具数 | 主要功能 |
|------|--------|----------|
| strategy | 11 | 策略管理 |
| scorecard | 10 | 评分卡 |
| portfolio | 10 | 组合管理 |
| experiment | 9 | 实验跟踪 |
| chain | 9 | 产业链 |
| altdata | 9 | 另类数据 |
| stage | 8 | 阶段判断 |
| datasource | 8 | 数据源 |
| event | 7 | 事件抽取 |
| pool | 7 | 候选池 |
| tenbagger | 7 | 十倍股评估 |
| market | 5 | 市场分析 |
| 其他 | 22 | 辅助功能 |

### 4.2 核心工具

```python
# 数据获取
datasource.fetch_all         # 获取完整数据
datasource.fetch_financial   # 财务数据
datasource.fetch_price       # 行情数据

# 事件处理
event.extract                # 事件抽取
event.stage_mapping          # 阶段映射

# 阶段判断
stage.process               # 处理事件
stage.get                   # 获取阶段
stage.history               # 阶段历史

# 评分卡
scorecard.compute           # 计算评分
scorecard.explain           # 解释评分
scorecard.compare           # 对比评分

# 候选池
pool.add                    # 添加候选
pool.filter                 # 筛选
pool.stats                  # 统计

# Tenbagger评估
tenbagger.evaluate          # 综合评估
tenbagger.report            # 评估报告
tenbagger.rank              # 潜力排名

# 组合管理
portfolio.order             # 下单
portfolio.positions         # 持仓
portfolio.risk_signals      # 风险信号
```

---

## 五、GUI面板

### 5.1 已实现面板

| 面板 | 文件 | 功能 |
|------|------|------|
| 十倍股仪表盘 | tenbaggerDashboard.ts | 候选池统计、潜力排名 |
| 产业链图谱 | industryChainPanel.ts | 上中下游可视化 |
| 个股详情 | stockDetailPanel.ts | 7维评分卡、阶段时间线 |
| 回测面板 | backtestPanel.ts | 策略回测 |
| 市场面板 | marketPanel.ts | 市场状态 |

### 5.2 GUI命令 (14个)

```
candidate_pool_stats      # 候选池统计
candidate_pool_filter     # 候选池筛选
candidate_pool_add        # 添加候选
tenbagger_ranking         # 潜力排名
tenbagger_evaluate        # 股票评估
datasource_stats          # 数据源状态
industry_chain_list       # 产业链列表
industry_chain_stats      # 产业链统计
industry_chain_detail     # 产业链详情
industry_chain_stocks     # 节点股票
industry_chain_search     # 搜索产业链
stock_basic_info          # 股票基本信息
stock_events              # 股票事件
stock_stage               # 股票阶段
```

---

## 六、开发里程碑

| 里程碑 | 内容 | 状态 |
|--------|------|------|
| M1 | WorkflowContext + DataSnapshot + Experiment | ✅ |
| M3.1 | RawDoc + Event抽取 | ✅ |
| M3.2 | Stage状态机 + ScoreCard评分卡 | ✅ |
| M3.3 | 分层候选池 + 产业链图谱 | ✅ |
| M2 | Strategy Pack插件层 | ✅ |
| M3.4 | Tier2 AltData第二档数据源 | ✅ |
| M4 | Tenbagger十倍股评估体系 | ✅ |
| M5 | 多策略组合与执行 | ✅ |
| Phase2 | 数据源集成 + GUI面板 | ✅ |
| Phase3 | 产业链图谱 + 个股详情面板 | ✅ |

---

## 七、使用指南

### 7.1 快速开始

```python
# 1. 获取数据
from utils.datasource_manager import get_datasource_manager
manager = get_datasource_manager()
data = manager.fetch_for_tenbagger(["300750.XSHG"])

# 2. 阶段判断
from utils.stage_machine import StageMachine
sm = StageMachine()
stage = sm.get_or_create("300750.XSHG")

# 3. 评分计算
from utils.scorecard import get_scorecard_engine
engine = get_scorecard_engine()
card = engine.compute("300750.XSHG", data["financials"]["300750.XSHG"])

# 4. Tenbagger评估
from utils.tenbagger_evaluator import TenbaggerEvaluator
evaluator = TenbaggerEvaluator()
report = evaluator.evaluate("300750.XSHG", "宁德时代", {...})
```

### 7.2 打开GUI面板

```
命令面板 (Ctrl+Shift+P):
- TRQuant: 打开十倍股仪表盘
- TRQuant: 打开产业链图谱
- TRQuant: 查看个股详情
```

---

## 八、后续规划

- [ ] 接入真实JQData数据源
- [ ] 完善产业链初始数据
- [ ] 添加更多图表可视化
- [ ] 报告导出PDF功能
- [ ] 实盘交易对接

---

*文档版本: 1.0 | 生成时间: 2025-12-18*
