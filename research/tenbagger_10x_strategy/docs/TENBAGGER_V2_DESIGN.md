# 十倍股早期识别系统 V2 设计文档

> **版本**: 2.0  
> **日期**: 2025-12-19  
> **状态**: 已实现  

---

## 📋 设计目标

**核心问题**: 原系统更像在做"优质大盘股筛选"，而不是"十倍股早期识别"

**V2目标**: 
- 目标是捕捉 **S1→S2 转换点**：基本面开始可验证，但市场仍未完全定价
- 低通过率（5%-20%）才现实
- 缺失数据 = 惩罚，不是高分
- 输出可解释、可追溯

---

## 🏗️ 系统架构

### 总体架构：三层漏斗 + 双引擎 + 三轴状态机

```
                    ┌─────────────────────┐
                    │   原始候选池        │
                    │   (全市场股票)      │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │   L0 可交易宇宙     │ ← 规则引擎(一票否决)
                    │   (硬过滤)          │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │   L1 早期结构候选   │ ← 评分引擎V2
                    │   (早期信号)        │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │   L2 十倍路径精评   │ ← 三轴阶段状态机
                    │   (通过率5%-20%)    │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │   推荐列表          │ ← 通过率控制器
                    │   (口径一致性)      │
                    └─────────────────────┘
```

---

## 📁 代码结构

```
mcp_servers/utils/tenbagger_v2/
├── __init__.py              # 模块入口
├── candidate_funnel.py      # 三层漏斗候选池
├── rule_engine.py           # 规则引擎（一票否决）
├── scoring_engine_v2.py     # 评分引擎V2
├── tri_axis_stage.py        # 三轴阶段状态机
├── pass_rate_controller.py  # 通过率控制器
├── evaluator_v2.py          # 评估器V2（整合）
└── report_generator.py      # 报告生成器
```

---

## 🔧 组件详解

### 1. 三层漏斗候选池 (CandidateFunnel)

#### L0 可交易宇宙（硬过滤）

| 过滤器 | 条件 | 说明 |
|--------|------|------|
| ST/退市风险 | is_st=False, delisting_risk=False | 剔除ST和退市风险股 |
| 重大违规 | major_violation=False | 剔除违规股 |
| 长期停牌 | trading_days_ratio≥0.8 | 交易日比例≥80% |
| 财报完整性 | financial_report_count≥3 | 近4期财报≥3期 |
| 流动性下限 | avg_turnover≥0.001 | 日均换手≥0.1% |
| 数据质量 | missing_ratio≤0.5 | 缺失率≤50% |

#### L1 早期结构候选

| 信号 | 权重 | 计算方法 |
|------|------|----------|
| 收入加速 | 25% | revenue_growth_qoq_change > 0 |
| 利润拐点 | 20% | profit_growth_change > 0 |
| 毛利率改善 | 15% | gross_margin_change > 0 |
| 资本开支强度 | 15% | capex_ratio > 5% |
| 研发强度 | 15% | rd_ratio > 3% |
| 产业事件触发 | 10% | event_count ≥ 2 |

**L1通过阈值**: 50分

#### L2 早期性约束

| 约束 | 条件 | 惩罚/奖励 |
|------|------|----------|
| 市值上限 | market_cap_percentile ≤ 0.8 | 超过-30分 |
| 近期涨幅过大 | price_change_24m ≤ 2.0 | 超过-25分 |
| 机构覆盖过高 | analyst_coverage ≤ 20 | 超过-20分 |
| 低关注度 | research_report_count ≤ 10 | 满足+15分 |

**L2通过阈值**: 65分

---

### 2. 规则引擎 (RuleEngine)

**10条一票否决规则**:

| 规则ID | 名称 | 条件 | 严重级别 |
|--------|------|------|----------|
| st_delisting | ST/退市风险 | is_st OR delisting_risk | CRITICAL |
| major_violation | 重大违规 | major_violation=True | CRITICAL |
| cash_flow_negative | 经营现金流长期为负 | cash_flow_negative_years≥2 AND revenue_growth<10 | CRITICAL |
| high_leverage_short_debt | 高杠杆短债压力 | debt_ratio>70 AND short_debt_ratio>0.8 | CRITICAL |
| goodwill_dominant | 商誉/非经常损益主导 | goodwill_ratio>0.5 OR non_recurring_ratio>0.8 | HIGH |
| high_pledge | 高质押风险 | pledge_ratio>0.8 AND near_pledge_liquidation | CRITICAL |
| receivable_inventory_anomaly | 应收存货异常 | receivable_revenue_ratio>0.5 OR inventory_revenue_ratio>1.0 | HIGH |
| audit_opinion_abnormal | 审计意见异常 | audit_opinion≠"standard" | CRITICAL |
| major_lawsuit | 重大诉讼风险 | has_major_lawsuit AND lawsuit_net_asset_ratio>0.2 | HIGH |
| continuous_loss | 连续亏损 | continuous_loss_years≥3 | CRITICAL |

---

### 3. 三轴阶段状态机 (TriAxisStageMachine)

#### 三轴定义

**基本面轴 (Fundamental Momentum)**:
- 收入增速加速 (+25分)
- 利润高增长 (+25分)
- 毛利率提升 (+20分)
- 经营现金流改善 (+15分)
- 连续改善 (+15分)

**资金轴 (Flow)**:
- 均线多头排列 (+25分)
- 成交量放大 (+20分)
- 换手率从低位抬升 (+20分)
- 价格突破信号 (+20分)
- 相对强度高 (+15分)

**预期轴 (Expectation)**:
- 公告密度高 (+20分)
- 研报覆盖增加 (+20分)
- 分析师评级上调 (+15分)
- 产业事件频繁 (+20分)
- 估值锚切换 (+25分)

#### 阶段判定规则

| 阶段 | 基本面轴 | 资金轴 | 预期轴 | 说明 |
|------|----------|--------|--------|------|
| S1 验证期 | 50-70 | 0-50 | 0-40 | 真拐点+未趋势化+低关注 |
| S2 导入期 | 60-90 | 40-70 | 30-60 | **最佳介入点** |
| S3 放量期 | 70-100 | 60-100 | 50-100 | 共识形成 |
| S4 加速期 | 80-100 | 70-100 | 70-100 | 高关注度 |
| S0 观察期 | - | - | - | 不匹配任何阶段 |

---

### 4. 评分引擎V2 (ScoringEngineV2)

#### 因子定义

| 因子ID | 名称 | 权重 | 缺失惩罚 |
|--------|------|------|----------|
| revenue_growth | 营收增速 | 15% | -20分 |
| profit_growth | 利润增速 | 15% | -20分 |
| gross_margin | 毛利率 | 10% | -15分 |
| roe | ROE | 10% | -15分 |
| cash_flow_ratio | 现金流/利润 | 10% | -20分 |
| rd_ratio | 研发强度 | 10% | -10分 |
| debt_ratio | 负债率 | 8% | -15分 |
| pe_percentile | PE分位 | 7% | -10分 |
| market_cap_constraint | 市值约束 | 8% | -10分 |
| institutional_ownership | 机构持仓 | 7% | -5分 |

#### 核心改进

1. **缺失惩罚**: 缺失数据扣分（15-20分），不是默认高分
2. **分布自检**: 方差≈0自动警告并降权
3. **置信度调整**: `adjusted_score = total_score * confidence`
4. **质量标志**: good(≥0.8) / warning(0.5-0.8) / poor(<0.5)

---

### 5. 通过率控制器 (PassRateController)

**配置**:
- 目标通过率: 15%
- 最低通过率: 5%
- 最高通过率: 20%
- 自动调整: 开启
- L1阈值: 50
- L2阈值: 65

**自动调整逻辑**:
```python
if l2_pass_rate > max_pass_rate:
    l2_threshold += 5  # 收紧
elif l2_pass_rate < min_pass_rate:
    l2_threshold -= 5  # 放宽（谨慎）
```

---

### 6. 报告生成器 (ReportGenerator)

**口径一致性保证**:
1. 标题由代码自动生成，禁止手写
2. 输出前验证等级与标题声称一致
3. 检测推荐率过高自动警告
4. 配置快照可追溯

---

## 📊 等级映射

| 等级 | 分数范围 | 阶段要求 | 描述 |
|------|----------|----------|------|
| S+ | ≥85 | S1-S3 | 顶级推荐 |
| S | ≥75 | S1-S3 | 强烈推荐 |
| A | ≥65 | S1-S4 | 推荐 |
| B | ≥50 | S0-S5 | 关注 |
| C | ≥35 | S0-S5 | 观察 |
| D | <35 | - | 暂不推荐 |
| REJECTED | - | - | 已否决 |

---

## 🚀 使用示例

```python
from mcp_servers.utils.tenbagger_v2 import get_evaluator_v2, ReportGenerator

# 获取评估器
evaluator = get_evaluator_v2()

# 准备数据
stocks = [
    {
        "symbol": "300001.SZ",
        "name": "某科技股",
        "data": {
            "is_st": False,
            "revenue_growth_qoq_change": 15,
            "profit_growth": 35,
            # ... 其他数据
        }
    }
]

# 批量评估
reports = evaluator.batch_evaluate(stocks)

# 获取推荐列表
recommendations = evaluator.get_recommendations(min_level="A")

# 生成报告
generator = ReportGenerator(evaluator)
generator.save_report("output.md", format="markdown")
```

---

## 📈 测试结果

```
测试数据: 5 只股票
推荐率: 20.0%（符合目标5%-20%）
否决数: 2（ST股票、高杠杆股票）
一致性检查: ✓ 通过
```

---

## 📚 参考文档

- CANSLIM成长股筛选方法论
- Bessembinder (2018) "Do Stocks Outperform Treasury bills?"
- Investopedia Tenbagger Definition

---

*文档版本: 2.0 | 创建时间: 2025-12-19*

