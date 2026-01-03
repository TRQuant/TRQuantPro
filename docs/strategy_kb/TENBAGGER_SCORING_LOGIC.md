# 十倍股评分逻辑详解

> **文档创建时间**: 2025-12-19  
> **目的**: 详细说明ScoreCard和TenbaggerEvaluator的评分逻辑

---

## 📊 一、ScoreCard (7维评分卡)

### 1.1 compute() 方法流程

**位置**: `mcp_servers/utils/scorecard.py`  
**方法**: `ScoreCardEngine.compute()`

```python
def compute(
    self,
    security_id: str,
    stage_record: Dict = None,
    events: List[Dict] = None,
    financial_data: Dict = None
) -> ScoreCard:
```

**计算流程**:
1. 计算7个维度的得分
2. 每个维度得分 × 权重 = 加权得分
3. 所有维度加权得分求和 = 总分
4. 根据总分确定等级 (A/B/C/D/F)

### 1.2 7维评分配置

| 维度 | 权重 | 说明 | 数据来源 |
|------|------|------|----------|
| 产业位置 | 20% | 产业链关键节点 | industry_graph |
| 兑现路径 | 20% | 送样→量产进度 | stage_machine |
| 财务拐点 | 15% | 毛利/营收/现金流 | jqdata |
| 组织信号 | 10% | 招聘/高管变化 | events |
| 估值错配 | 15% | PE/PB vs 增速 | jqdata |
| 研究关注 | 10% | 研报数量（越少越好） | research_reports |
| 证据密度 | 10% | 多证据交叉 | events |

**总分计算公式**:
```
total_score = Σ(dimension_score × dimension_weight)
```

### 1.3 各维度打分逻辑

#### 1.3.1 产业位置 (20%)

**方法**: `_score_industry_position()`

```python
# 当前实现：默认值
score = 60.0  # TODO: 需要产业链图谱数据
```

**归一化**: 0-100分，直接使用

---

#### 1.3.2 兑现路径 (20%)

**方法**: `_score_fulfillment_path()`

**阶段得分映射**:
```python
stage_scores = {
    "S0": 20,  # 观察期
    "S1": 40,  # 验证期
    "S2": 60,  # 导入期（最佳介入点）
    "S3": 80,  # 放量期
    "S4": 90,  # 加速期
    "S5": 50   # 成熟期（估值偏高）
}
```

**计算公式**:
```python
base_score = stage_scores.get(stage, 20)
score = base_score + (confidence * 10)  # 置信度加成
score = min(score, 100)  # 上限100
```

**归一化**: 0-100分，上限100

---

#### 1.3.3 财务拐点 (15%)

**方法**: `_score_financial_inflection()`

**评分规则**:
```python
score = 50.0  # 基础分

# 毛利率提升 > 5%: +20分
if gross_margin_change > 5:
    score += 20

# 营收增速 > 30%: +15分
if revenue_growth > 30:
    score += 15

# 经营现金流为正: +15分
if positive_cash_flow:
    score += 15

score = min(score, 100)  # 上限100
```

**归一化**: 0-100分，上限100

---

#### 1.3.4 组织信号 (10%)

**方法**: `_score_organization_signal()`

**评分规则**:
```python
score = 50.0  # 基础分

# 组织事件数 × 10分
org_events = [e for e in events if e.type in 
              ["executive_change", "equity_incentive", "hiring_surge"]]
score += len(org_events) * 10

# 股权激励: +15分
if any(e.type == "equity_incentive" for e in org_events):
    score += 15

score = min(score, 100)  # 上限100
```

**归一化**: 0-100分，上限100

---

#### 1.3.5 估值错配 (15%)

**方法**: `_score_valuation_mismatch()`

**评分规则** (基于PEG模型):
```python
score = 50.0  # 基础分

if pe > 0 and growth > 0:
    peg = pe / growth
    
    if peg < 1:
        # PEG < 1: 低估，高分
        score = 80 + (1 - peg) * 20
    elif peg < 2:
        # 1 <= PEG < 2: 合理
        score = 60
    else:
        # PEG >= 2: 偏高
        score = 40

score = min(score, 100)  # 上限100
```

**归一化**: 0-100分，上限100

---

#### 1.3.6 研究关注 (10%)

**方法**: `_score_research_attention()`

**评分规则** (研报越少越好，十倍股早期特征):
```python
report_count = 5  # 实际需要研报数据

if report_count <= 3:
    score = 90  # 研报极少，早期信号明显
elif report_count <= 10:
    score = 70  # 研报较少，关注度适中
elif report_count <= 30:
    score = 50  # 研报较多，已有一定关注
else:
    score = 30  # 研报众多，共识度高
```

**归一化**: 0-100分，直接映射

---

#### 1.3.7 证据密度 (10%)

**方法**: `_score_evidence_density()`

**评分规则**:
```python
event_count = len(events) if events else 0

if event_count >= 10:
    score = 90  # 证据充分
elif event_count >= 5:
    score = 70
elif event_count >= 2:
    score = 50
else:
    score = 30  # 证据不足
```

**归一化**: 0-100分，直接映射

---

### 1.4 等级划分

**方法**: `_compute_grade()`

```python
GRADE_THRESHOLDS = [
    (80, "A"),   # >= 80: A
    (65, "B"),   # >= 65: B
    (50, "C"),   # >= 50: C
    (35, "D"),   # >= 35: D
    (0, "F")     # < 35: F
]
```

---

## 🎯 二、TenbaggerEvaluator (综合评估)

### 2.1 evaluate() 方法流程

**位置**: `mcp_servers/utils/tenbagger_evaluator.py`  
**方法**: `TenbaggerEvaluator.evaluate()`

```python
def evaluate(self, symbol: str, name: str, data: Dict[str, Any]) -> TenbaggerReport:
```

**计算流程**:
1. 计算7个评估维度的得分
2. 每个维度得分 × 权重 = 加权得分
3. 所有维度加权得分求和 = 总分
4. 根据总分确定等级 (S+/S/A/B/C/D)

### 2.2 7维评估配置

| 维度 | 权重 | 说明 | 数据来源 |
|------|------|------|----------|
| stage | 20% | 阶段评估 | stage_machine |
| scorecard | 25% | 7维评分卡 | ScoreCardEngine |
| growth | 15% | 成长性 | financials |
| industry | 15% | 行业地位 | industry |
| altdata | 10% | 另类数据信号 | altdata |
| momentum | 10% | 市场动量 | technicals |
| risk | 5% | 风险调整 | financials |

**总分计算公式**:
```
total_score = Σ(dimension_score × dimension_weight)
```

### 2.3 各维度打分逻辑

#### 2.3.1 阶段评估 (20%)

**方法**: `_eval_stage()`

**阶段得分映射**:
```python
stage_scores = {
    "S0": 20,  # 观察期
    "S1": 40,  # 验证期
    "S2": 60,  # 导入期（最佳介入点）
    "S3": 80,  # 放量期
    "S4": 90,  # 加速期
    "S5": 50   # 成熟期
}
```

**归一化**: 0-100分，直接映射

---

#### 2.3.2 评分卡评估 (25%)

**方法**: `_eval_scorecard()`

**评分规则**:
```python
total = scorecard.get("total_score", 50)
score = min(total, 100)  # 直接使用ScoreCard的总分，上限100
```

**归一化**: 0-100分，上限100

---

#### 2.3.3 成长性评估 (15%)

**方法**: `_eval_growth()`

**评分规则**:
```python
score = 50.0  # 基础分

# 营收增速
if revenue_growth > 50:
    score += 25  # 高增长
elif revenue_growth > 20:
    score += 15  # 稳健增长

# 利润增速
if profit_growth > 50:
    score += 25  # 高增长
elif profit_growth > 20:
    score += 15  # 稳健增长

score = min(score, 100)  # 上限100
```

**归一化**: 0-100分，上限100

---

#### 2.3.4 行业地位评估 (15%)

**方法**: `_eval_industry()`

**评分规则**:
```python
score = 50.0  # 基础分

# 行业排名
if industry_rank <= 3:
    score += 30  # 行业龙头
elif industry_rank <= 5:
    score += 20  # 行业领先

# 行业增长
if industry_growth > 20:
    score += 20  # 高景气行业

score = min(score, 100)  # 上限100
```

**归一化**: 0-100分，上限100

---

#### 2.3.5 另类数据评估 (10%)

**方法**: `_eval_altdata()`

**评分规则**:
```python
score = 50.0  # 基础分

# 招投标趋势
if bid_trend == "growing":
    score += 20

# 招聘趋势
if job_trend == "expanding":
    score += 20

# 扩张信号
if expansion_signal:
    score += 10

score = min(score, 100)  # 上限100
```

**归一化**: 0-100分，上限100

---

#### 2.3.6 动量评估 (10%)

**方法**: `_eval_momentum()`

**评分规则**:
```python
score = 50.0  # 基础分

# 均线趋势
if ma_trend == "bullish":
    score += 20  # 多头排列

# 成交量趋势
if volume_trend == "increasing":
    score += 15  # 成交量放大

# 相对强度
if relative_strength > 70:
    score += 15

score = min(score, 100)  # 上限100
```

**归一化**: 0-100分，上限100

---

#### 2.3.7 风险评估 (5%)

**方法**: `_eval_risk()`

**评分规则** (风险越低得分越高):
```python
score = 70.0  # 基础分（风险较低）

# 负债率
debt_ratio = financials.get("debt_ratio", 50)
if debt_ratio > 70:
    score -= 20  # 负债率较高，扣分

# 估值
pe_ratio = financials.get("pe_ratio", 30)
if pe_ratio > 100:
    score -= 15  # 估值偏高，扣分

score = max(score, 0)  # 下限0
```

**归一化**: 0-100分，下限0

---

### 2.4 等级划分

**方法**: `_determine_level()`

```python
LEVEL_THRESHOLDS = {
    "S+": 85,  # >= 85: S+ (极高潜力)
    "S": 75,   # >= 75: S (高潜力)
    "A": 65,   # >= 65: A (较高潜力)
    "B": 50,   # >= 50: B (中等潜力)
    "C": 35,   # >= 35: C (一般)
    "D": 0     # < 35: D (较低)
}
```

---

## 📈 三、评分流程总结

### 3.1 完整评分链路

```
输入数据
  ↓
ScoreCardEngine.compute()
  ├─ 7维评分卡计算
  ├─ 各维度得分 × 权重
  └─ 总分 = Σ(加权得分)
  ↓
TenbaggerEvaluator.evaluate()
  ├─ 7维综合评估
  ├─ 各维度得分 × 权重
  └─ 总分 = Σ(加权得分)
  ↓
确定等级 (S+/S/A/B/C/D)
```

### 3.2 关键公式

**ScoreCard总分**:
```
scorecard_total = Σ(scorecard_dimension_i × weight_i)
```

**Tenbagger总分**:
```
tenbagger_total = Σ(tenbagger_dimension_i × weight_i)
```

其中:
- `scorecard_dimension_i` 包括: 产业位置、兑现路径、财务拐点、组织信号、估值错配、研究关注、证据密度
- `tenbagger_dimension_i` 包括: stage、scorecard、growth、industry、altdata、momentum、risk

### 3.3 归一化规则

所有维度得分统一归一化到 **0-100分**:
- 大部分维度: `score = min(score, 100)` (上限100)
- 风险评估: `score = max(score, 0)` (下限0)
- 阶段评估: 直接映射 (20-90分)

---

## ⚠️ 四、注意事项

1. **ScoreCard的scorecard维度** 在TenbaggerEvaluator中权重最高 (25%)，说明7维评分卡是核心评估依据

2. **阶段评估** 在两个系统中都有，但权重不同:
   - ScoreCard中: 兑现路径 20%
   - TenbaggerEvaluator中: stage 20%

3. **评分卡总分异常**: 早上运行结果显示大部分股票评分卡都是100.0分，可能原因:
   - 财务数据缺失导致默认高分
   - 评分逻辑需要检查

4. **数据依赖**: 多个维度需要实际数据支持:
   - 产业位置: 需要产业链图谱
   - 研究关注: 需要研报数据
   - 另类数据: 需要招投标、招聘数据

---

## 📚 相关文件

- `mcp_servers/utils/scorecard.py` - ScoreCard实现
- `mcp_servers/utils/tenbagger_evaluator.py` - TenbaggerEvaluator实现
- `extension/python/tenbagger_commands.py` - 调用入口

---

*文档版本: 1.0 | 创建时间: 2025-12-19*

