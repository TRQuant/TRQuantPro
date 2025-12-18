# 十倍股早期识别体系开发计划

> 基于《十倍股早期识别体系_韬睿量化系统开发建议.pdf》+ AltData低成本方案
> 更新时间: 2025-12-18

---

## 一、数据源策略（AltData分层）

### 核心原则

> **个人投资阶段，不要上 Wind / 巨灵 / Choice 全家桶。**
> **用「公开数据 + 少量低成本平台 + 自建抽取」即可覆盖 70–80% 的十倍股早期有效信息。**

### 数据源分层

| 档位 | 数据源 | 成本 | 优先级 |
|------|--------|------|--------|
| **Tier1** | 公告/年报(交易所/巨潮)、互动易、JQData财务 | 0~低 | 必须有 |
| **Tier2** | 招投标(官网)、招聘(趋势) | 0 | 强烈建议 |
| **Tier3** | 研报数量、舆情 | 可选 | 后期再说 |

### 落地顺序

```
Step1: 公告+互动易 → RawDoc → Event → Stage (1个行业先跑通)
Step2: JQData财务 + 7维评分卡V1
Step3: 招投标+招聘 (只做趋势，不做全量)
Step4: 考虑是否需要商业AltData
```

---

## 二、里程碑与任务

### 里程碑概览

| 里程碑 | 名称 | 状态 | 目标日期 |
|--------|------|------|----------|
| M1 | WorkflowContext + DataSnapshot + Experiment | ✅ 完成 | 2025-01-15 |
| M2 | Strategy Pack 插件层 | ⏳ | 2025-01-31 |
| M3 | Tenbagger Pack MVP | ⏳ | 2025-02-28 |
| M4 | Tenbagger 评估体系 | ⏳ | 2025-03-15 |
| M5 | 多策略组合与执行 | ⏳ | 2025-03-31 |

### M3 细化任务（整合AltData）

| 任务ID | 名称 | Tier | 预估天数 |
|--------|------|------|----------|
| M3.1 | RawDoc + Event 抽取 | Tier1 | 7天 |
| M3.2 | Stage状态机 + ScoreCard评分卡 | Tier1 | 7天 |
| M3.3 | 分层候选池 + 产业链图谱 | - | 5天 |
| M3.4 | 第二档数据源（招投标+招聘） | Tier2 | 5天 |

---

## 三、M3.1 详细设计：RawDoc + Event

### 数据表结构

```python
# MongoDB: trquant.raw_docs
RawDoc = {
    "doc_id": str,           # 文档ID
    "doc_type": str,         # announcement/annual_report/interactive_qa/news
    "source": str,           # cninfo/sse_interact/szse_interact
    "security_id": str,      # 股票代码
    "publish_time": datetime,# 发布时间
    "title": str,            # 标题
    "content": str,          # 全文
    "url": str,              # 原文链接
    "credibility": float,    # 可信度权重 (0-1)
    "processed": bool,       # 是否已抽取
    "created_at": datetime
}

# MongoDB: trquant.events
Event = {
    "event_id": str,
    "event_type": str,       # 见事件标签字典
    "security_id": str,
    "event_date": datetime,
    "source_doc_id": str,    # 关联RawDoc
    "confidence": float,     # 置信度
    "extracted_by": str,     # rule/llm/manual
    "details": dict,         # 事件详情
    "created_at": datetime
}
```

### 十倍股事件标签字典V1

| 事件类型 | 代码 | 说明 | Stage影响 |
|----------|------|------|-----------|
| 送样 | SAMPLE_DELIVERY | 送样给客户 | S1→S2 |
| 验证通过 | VALIDATION_PASS | 客户验证通过 | S2→S3 |
| 小批量订单 | SMALL_BATCH | 小批量/试产订单 | S2→S3 |
| 量产订单 | MASS_PRODUCTION | 批量订单 | S3→S4 |
| 进入供应商 | SUPPLIER_ENTRY | 进入客户供应商体系 | S2→S3 |
| 扩产公告 | EXPANSION | 扩产/新产线 | S3→S4 |
| 环评公示 | ENVIRONMENTAL | 环评/项目审批 | S2→S3 |
| 高管变更 | EXECUTIVE_CHANGE | 高管/董事变更 | - |
| 股权激励 | EQUITY_INCENTIVE | 股权激励计划 | - |
| 认证获取 | CERTIFICATION | 行业/客户认证 | S1→S2 |

---

## 四、M3.2 详细设计：Stage + ScoreCard

### Stage状态机 (S0-S5)

```
S0: 观察期（有产业链位置，但无明显兑现信号）
S1: 验证期（送样/认证中，尚未确认客户）
S2: 导入期（已进入客户体系，小批量/验证）
S3: 放量期（批量订单，扩产明确）
S4: 加速期（业绩拐点，估值修复）
S5: 成熟期（主流共识，十倍股特征消失）
```

### 7维评分卡

| 维度 | 权重 | 数据来源 | 说明 |
|------|------|----------|------|
| 产业位置 | 20% | IndustryGraph | 产业链关键节点 |
| 兑现路径 | 20% | Event/Stage | 送样→量产进度 |
| 财务拐点 | 15% | JQData | 毛利/营收/现金流 |
| 组织信号 | 10% | 招聘/高管 | 组织扩张/补强 |
| 估值错配 | 15% | JQData | PE/PB vs 增速 |
| 研究关注 | 10% | 研报数量 | 越少越好(早期) |
| 证据密度 | 10% | Event count | 多证据交叉 |

---

## 五、开发流程（遵循TRQuant标准）

### 每个任务的开发周期

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1. 规划    │ -> │  2. 开发    │ -> │  3. 测试    │ -> │  4. 记录    │
│  task.create│    │  编码实现    │    │  验证功能    │    │  devlog.add │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### MCP工具使用

```bash
# 规划
task.create(title, description, priority)
milestone.progress(milestone_id)

# 开发
task.update(task_id, status="in_progress")
module.register(name, version, status)

# 测试
pytest tests/ -v

# 记录
devlog.add(content, tags)
task.update(task_id, status="completed")
git commit && git push
```

---

## 六、下一步行动

**推荐顺序**: M3.1 → M3.2 → M3.3 → M2 → M3.4 → M4 → M5

理由：
1. M3.1 (RawDoc+Event) 是十倍股的数据地基
2. M3.2 (Stage+ScoreCard) 是核心识别逻辑
3. M3.3 完成候选池输出，形成最小闭环
4. M2 (Strategy Pack) 抽象为可复用插件
5. M3.4 补充第二档数据源
6. M4/M5 后续迭代

---

*文档版本: 2.0 | 整合AltData低成本方案 | 2025-12-18*
