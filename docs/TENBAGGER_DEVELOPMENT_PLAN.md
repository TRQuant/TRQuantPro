# 十倍股早期识别体系开发计划

> 基于《十倍股早期识别体系_韬睿量化系统开发建议.pdf》
> 更新时间: 2025-12-18

---

## 一、总体目标

### 1.1 平台级目标 (TRQuant Core 2.x)

| 目标 | 说明 |
|------|------|
| 多策略容器 | 策略以 Strategy Pack 插件化装载 |
| 可复现研究 | 数据/因子/策略/回测 四位一体可追溯 |
| 端到端闭环 | 9步工作流变成可编排DAG，支持增量刷新 |
| 生产化标准 | 监控、日志、告警、权限管理 |

### 1.2 十倍股早期识别 (Tenbagger Pack)

核心证据链：**产业位置→兑现路径→财务拐点→组织信号→估值错配**

输出物：
- U1/U2/U3 分层候选池
- Stage S0-S5 状态机
- 7维评分卡
- Thesis论点对象 + Falsification证伪条件
- 专属指标：Recall@K、Time-to-detection、误杀率

---

## 二、里程碑规划

```
M1 (Jan 15) ──► M2 (Jan 31) ──► M3 (Feb 28) ──► M4 (Mar 15) ──► M5 (Mar 31)
   平台基础        策略包层       十倍股MVP       评估体系        组合执行
```

### M1: WorkflowContext + DataSnapshot + Experiment

**目标**: 平台复现与步骤互联

| 交付物 | 说明 |
|--------|------|
| WorkflowContext | 工作流上下文，步骤间数据自动传递 |
| DataSnapshot | 数据快照，确保可复现 |
| Experiment | 实验追踪，配置+数据+指标+产物 |

**新增MCP工具**:
- `snapshot.create/get/compare`
- `experiment.register/get/compare/export`

**验收标准**:
- [ ] 任意步骤输出自动流入下游步骤
- [ ] 数据快照可追溯
- [ ] 实验可对比

---

### M2: Strategy Pack 插件层

**目标**: 策略以可插拔包形式装载

| 交付物 | 说明 |
|--------|------|
| StrategyPack Manifest | 策略包注册表 |
| PackLoader | 策略包加载器 |
| pack.* 工具 | install/list/validate/run |

**验收标准**:
- [ ] 新增策略包不修改trquant-core
- [ ] 策略包输入输出与9步工作流兼容

---

### M3: Tenbagger Pack MVP

**目标**: 十倍股早期识别最小可用闭环

| 交付物 | 说明 |
|--------|------|
| IndustryGraph | 产业链图谱知识库 |
| RawDocStore | 原始文档存储 (公告/年报/互动易/新闻) |
| EventExtractor | 事件抽取 (送样/验证/量产/扩产/高管变更) |
| StageMachine | 状态机 S0-S5 + 置信度 + 证伪触发 |
| ScoreCard Engine | 7维评分卡，可解释维度贡献 |
| 分层候选池 | U1/U2/U3 输出 |

**新增MCP工具**:
- `doc.ingest/search/dedup/stats`
- `event.extract/list/validate/feedback`
- `stage.compute/get/override/history`
- `scorecard.compute/explain/versioning`
- `thesis.upsert/link_evidence/falsify/timeline`

**验收标准**:
- [ ] 每周一键刷新候选池
- [ ] 任意股票入池/出池有可追溯证据
- [ ] 事件抽取支持人工纠错回写

---

### M4: Tenbagger Pack 评估体系

**目标**: 从能用到可迭代

| 交付物 | 说明 |
|--------|------|
| TenbaggerMetricSuite | Recall@K、Time-to-detection、误杀率 |
| 时间戳一致性框架 | 避免前视偏差 |
| 评分卡版本化 | ScoreCard v1/v2 可对比 |

**验收标准**:
- [ ] 历史窗口"早识别效果评估"
- [ ] 两版本评分卡A/B对比

---

### M5: 多策略组合与执行 (可选)

**目标**: 多策略资金分配与执行端对接

| 交付物 | 说明 |
|--------|------|
| SignalSchema | 标准信号格式 |
| PortfolioAllocator | 多策略分配 + 风险预算 |
| PaperTrading | 仿真回放 |
| ExecutionAdapter | QMT/PTrade/BulletTrade对接 |

---

## 三、数据模型扩展

### MongoDB新增集合 (trquant库)

```
raw_docs          - 原始文档
events            - 结构化事件
stages            - 状态机记录
theses            - 论点对象
scorecards        - 评分卡
experiments       - 实验记录
strategy_packs    - 策略包注册
data_snapshots    - 数据快照
industry_graph    - 产业链图谱
```

### 索引设计

```javascript
// raw_docs
db.raw_docs.createIndex({security_id: 1, publish_time: -1})
db.raw_docs.createIndex({doc_type: 1, publish_time: -1})

// events
db.events.createIndex({security_id: 1, event_type: 1, event_date: -1})

// stages
db.stages.createIndex({security_id: 1, stage: 1, updated: -1})

// experiments
db.experiments.createIndex({pack_name: 1, version: 1, created: -1})
```

---

## 四、开发优先级建议

**PDF建议的两个切入点**:

1. **M1优先** (平台地基):
   - 所有策略包的基础
   - 可复现性是量化研究的生命线

2. **M3优先** (业务价值):
   - 十倍股闭环最核心路径
   - 可快速验证商业价值

**推荐顺序**: M1 → M3 → M2 → M4 → M5

理由: M1打地基，M3验证价值，M2抽象为通用能力，M4迭代优化，M5生产对接

---

## 五、风险管理

| 风险 | 对策 |
|------|------|
| 数据授权与合规 | 适配器层携带license_tag |
| 事件抽取质量 | V1规则引擎，V2模型/LLM，人工反馈机制 |
| 前视偏差 | M4前完成时间戳规则 |
| 系统复杂度膨胀 | Strategy Pack隔离复杂度 |

---

## 六、下一步行动

选择切入点：
- [ ] 先细化 M1 (WorkflowContext + DataSnapshot + Experiment)
- [ ] 先细化 M3 (Tenbagger Pack MVP)

请确认后，输出工程级细化方案：模块拆分、接口、数据表、工具清单、DoD、测试用例。

---

*文档版本: 1.0 | 基于PDF建议 2025-12-18*
