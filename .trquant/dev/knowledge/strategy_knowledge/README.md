# 陈小群策略知识库

## 📚 知识库概览

本知识库收集整理了游资大佬陈小群的投资策略、交易方法和实战案例，用于支持TRQuant量化系统的策略开发和优化。

### 知识库统计

- **总条目数**: 9条
- **知识类型分布**:
  - 策略类 (strategy): 6条
  - 案例分析 (case_study): 2条
  - 仓位管理 (position_management): 1条

### 核心标签

- `chen_xiaoqun`: 陈小群相关
- `trading_method`: 交易方法
- `strategy`: 策略
- `emotion_cycle`: 情绪周期
- `dragon_stock`: 龙头战法
- `risk_control`: 风险控制
- `discipline`: 纪律执行
- `trend_following`: 顺势而为

## 📖 知识条目列表

### 1. 策略类 (Strategy)

#### cxq_0007: 陈小群投资策略核心 - 情绪周期+龙头战法
- **标签**: emotion_cycle, dragon_stock, investment_strategy, growth_timeline
- **内容**: 陈小群从30万到10亿的成长历程和核心策略框架

#### cxq_0008: 陈小群交易逻辑详解 - 题材驱动与情绪把控
- **标签**: trading_logic, theme_driven, emotion_control, case_study
- **内容**: 题材驱动、情绪周期把控、盘口语言与资金博弈

#### cxq_0009: 陈小群策略优化建议 - 提升回报率的关键
- **标签**: strategy_optimization, return_improvement, risk_control
- **内容**: 回报率低的原因分析和改进建议

#### cxq_0006: 陈小群策略 - 30万到10亿投资智慧
- **标签**: investment_wisdom, growth_story, discipline, trend_following
- **内容**: 系统积淀、纪律为纲、顺势而为、心态为王

#### cxq_0003: 陈小群策略 - 顺势而为
- **标签**: trend_following, market_emotion, dragon_stock
- **内容**: 情绪合力与龙头战法的核心逻辑

#### cxq_0002: 陈小群策略 - 游资思维习惯
- **标签**: trading_habits, mindset, discipline, risk_control
- **内容**: 反散户思维习惯，顺势、聚焦、执行、风控、学习

### 2. 案例分析 (Case Study)

#### cxq_0005: 陈小群策略 - 华胜天成
- **标签**: case_study, ai_computing, dragon_tiger_list, 2026
- **内容**: 2026年1月14日，陈小群5.42亿买入华胜天成的龙虎榜分析

#### cxq_0001: 陈小群策略 - 龙虎榜复盘
- **标签**: dragon_tiger_list, dtl_analysis, quantitative_application
- **内容**: 龙虎榜规则、读数方法、资金属性判断、量化落地方案

### 3. 仓位管理 (Position Management)

#### cxq_0004: 陈小群策略 - 持仓
- **标签**: position_management, holding_strategy, concept_stocks
- **内容**: 陈小群帝王运概念股更新，持仓策略分析

## 🔍 如何使用知识库

### 方法1: 使用MCP工具搜索

在Cursor Chat中使用 `knowledge_search` 工具：

```
请使用knowledge_search搜索"陈小群 情绪周期"
请使用knowledge_search搜索"龙头战法 选股技巧"
```

### 方法2: 直接读取JSON文件

```python
import json
from pathlib import Path

kb_file = Path(".trquant/dev/knowledge/strategy_knowledge/chen_xiaoqun_kb.json")
with open(kb_file, 'r', encoding='utf-8') as f:
    kb = json.load(f)

# 搜索特定标签
for item in kb['items']:
    if 'emotion_cycle' in item['tags']:
        print(f"{item['title']}: {item['content'][:100]}...")
```

### 方法3: 使用Python脚本

```python
from scripts.import_chen_xiaoqun_knowledge import load_strategy_kb

kb = load_strategy_kb()

# 按类型筛选
strategy_items = [item for item in kb['items'] if item['type'] == 'strategy']

# 按标签搜索
emotion_items = [
    item for item in kb['items'] 
    if 'emotion_cycle' in item['tags']
]
```

## 📊 知识库结构

```
.trquant/dev/knowledge/strategy_knowledge/
├── chen_xiaoqun_kb.json      # 主知识库文件
├── summary.json              # 知识库摘要
└── README.md                 # 本文件
```

## 🚀 增强知识库

### 添加新知识

使用 `scripts/import_chen_xiaoqun_knowledge.py` 脚本：

```python
from scripts.import_chen_xiaoqun_knowledge import add_to_strategy_kb

add_to_strategy_kb(
    title="新知识标题",
    content="知识内容...",
    source_file="来源文件路径",
    tags=["tag1", "tag2"],
    category="strategy"  # 或 "case_study", "position_management"
)
```

### 网络爬取增强

使用MCP工具进行网络爬取：

1. **基础爬取**: `crawler_fetch(url)`
2. **Selenium爬取**: `crawler_selenium_fetch(url)` (支持JavaScript)
3. **Lavague AI爬取**: `crawler_lavague_execute(instruction, url)`

### 关键词搜索

推荐搜索的关键词：
- 陈小群 情绪周期 龙头战法
- 陈小群 首板卡位术 选股技巧
- 陈小群 仓位管理 止损止盈
- 陈小群 游资席位 大连黄河路
- 陈小群 情绪合力 市场共振
- 陈小群 打板技巧 涨停板
- 陈小群 题材轮动 主线识别
- 陈小群 风险控制 纪律执行
- 陈小群 复盘方法 交易计划
- 陈小群 浙江建投 中交地产 案例

## 📝 知识库维护

### 更新频率

- **初始构建**: 2026-01-14
- **最后更新**: 2026-01-14
- **建议更新频率**: 每月或根据新资料获取情况

### 数据来源

1. **本地文件**: `notebooks/research/chen_xiaoqun_strategy/xiaoqun_reports/`
2. **网络搜索**: 通过web_search和网络爬取获取
3. **实战案例**: 龙虎榜数据、交易记录分析

## 🎯 应用场景

### 1. 策略开发

使用知识库中的策略框架和交易逻辑，指导策略代码开发：

```python
# 示例：情绪周期判断
from core.strategies.chen_xiaoqun import judge_emotion_cycle

# 参考知识库中的情绪周期判断标准
result = judge_emotion_cycle(
    limit_up_count=45,
    max_height=5,
    zhaban_rate=20,
    avg_inflow=1000
)
```

### 2. 策略优化

根据知识库中的优化建议，改进现有策略：

- 题材选择优化
- 龙头股识别增强
- 情绪周期研判提升
- 风险控制完善

### 3. 回测分析

使用知识库中的案例和规则，分析回测结果：

- 对比实际交易案例
- 验证策略逻辑
- 识别改进点

## 📌 注意事项

1. **知识库内容仅供参考**: 实际交易需结合市场实际情况
2. **持续更新**: 市场环境变化，策略需要持续优化
3. **风险提示**: 所有投资策略都有风险，需谨慎使用
4. **合规性**: 确保策略符合相关法律法规

## 🔗 相关资源

- **策略代码**: `core/strategies/chen_xiaoqun/`
- **回测脚本**: `notebooks/research/chen_xiaoqun_strategy/04_backtest_validation.ipynb`
- **研究报告**: `notebooks/research/chen_xiaoqun_strategy/xiaoqun_reports/`

## 📧 反馈与贡献

如有新的资料或改进建议，请：
1. 添加到 `xiaoqun_reports/` 目录
2. 运行 `scripts/import_chen_xiaoqun_knowledge.py` 导入
3. 或直接使用 `add_to_strategy_kb()` 函数添加

---

**最后更新**: 2026-01-14  
**维护者**: TRQuant Team
