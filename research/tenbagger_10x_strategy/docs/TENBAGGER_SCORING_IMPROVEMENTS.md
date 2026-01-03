# 十倍股评分系统改进实施总结

> **改进时间**: 2025-12-19  
> **基于**: `docs/TENBAGGER_SCORING_REVIEW_SUMMARY.md`  
> **优先级**: P0 (当天可做)

---

## ✅ 已实施的改进

### 1. 数据质量门控和置信度输出

**改进位置**: `mcp_servers/utils/scorecard.py`

#### 1.1 ScoreCard类增强

**新增字段**:
```python
@dataclass
class ScoreCard:
    # ... 原有字段 ...
    
    # 数据质量（新增）
    missing_ratio: float = 0.0      # 缺失数据比例 (0-1)
    confidence: float = 1.0          # 置信度 (0-1)
    quality_flag: str = "good"       # 数据质量标志: good/warning/poor
    placeholder_count: int = 0        # 占位维度数量
    version: str = "v2"              # 版本升级
```

#### 1.2 compute()方法增强

**新增逻辑**:
```python
def compute(self, ...) -> ScoreCard:
    dimensions = []
    placeholder_count = 0
    missing_data_count = 0
    total_dimensions = 7
    
    # 计算各维度（标记占位）
    # ...
    
    # 计算数据质量指标
    missing_ratio = missing_data_count / total_dimensions
    confidence = 1.0 - (missing_ratio * 0.5) - (placeholder_count * 0.1)
    confidence = max(0.3, min(1.0, confidence))  # 下限0.3
    
    # 确定质量标志
    if confidence >= 0.8:
        quality_flag = "good"
    elif confidence >= 0.5:
        quality_flag = "warning"
    else:
        quality_flag = "poor"
    
    # 应用置信度衰减
    raw_score = sum(d.weighted_score for d in dimensions)
    total_score = raw_score * confidence
    
    # 创建ScoreCard
    card = ScoreCard(
        # ...
        missing_ratio=missing_ratio,
        confidence=confidence,
        quality_flag=quality_flag,
        placeholder_count=placeholder_count,
        version="v2"
    )
```

---

### 2. 占位维度保守分+惩罚

#### 2.1 产业位置维度改进

**原逻辑** (固定60分):
```python
score = 60.0  # TODO
```

**改进后**:
```python
def _score_industry_position(self, security_id: str) -> DimensionScore:
    config = self.DIMENSIONS["industry_position"]
    
    # 占位维度：保守分 + 标记
    score = 35.0  # 从60降到35（保守分）
    factors = [{"factor": "产业链位置", "value": "待评估", "placeholder": True}]
    explanation = "产业位置评估需要产业链图谱数据支持（占位维度，保守评分）"
    
    return DimensionScore(
        dimension=config["name"],
        score=score,
        weight=config["weight"],
        weighted_score=round(score * config["weight"], 2),
        factors=factors,
        explanation=explanation,
        data_source="industry_graph",
        placeholder=True  # 标记为占位
    )
```

#### 2.2 研究关注维度改进

**原逻辑** (固定report_count=5):
```python
report_count = 5  # 假设值
```

**改进后**:
```python
def _score_research_attention(self, security_id: str) -> DimensionScore:
    config = self.DIMENSIONS["research_attention"]
    
    # TODO: 实际需要研报数据
    # 缺数据时：保守处理，不给高分
    report_count = None  # 未知
    
    if report_count is None:
        # 缺数据：按"共识未知"处理，给中等偏低分
        score = 45.0  # 从默认高分改为中等偏低
        explanation = "研报数据缺失，无法判断关注度（占位维度）"
        placeholder = True
    else:
        # 有数据：正常评分
        if report_count <= 3:
            score = 90
            explanation = "研报极少，早期信号明显"
        elif report_count <= 10:
            score = 70
            explanation = "研报较少，关注度适中"
        elif report_count <= 30:
            score = 50
            explanation = "研报较多，已有一定关注"
        else:
            score = 30
            explanation = "研报众多，共识度高"
        placeholder = False
    
    factors = [{"factor": "研报数量", "value": report_count or "未知"}]
    
    return DimensionScore(
        dimension=config["name"],
        score=score,
        weight=config["weight"],
        weighted_score=round(score * config["weight"], 2),
        factors=factors,
        explanation=explanation,
        data_source="research_reports",
        placeholder=placeholder
    )
```

---

### 3. 取消Stage双重计分

#### 3.1 ScoreCard兑现路径降权

**原权重**: 20%

**改进方案**: 降权至5%，或改为仅用于解释，不参与总分

```python
# 方案1: 降权
DIMENSIONS = {
    "fulfillment_path": {
        "name": "兑现路径",
        "weight": 0.05,  # 从0.20降到0.05
        "description": "送样→量产进度评估（降权，避免与Tenbagger stage重复）"
    },
    # ...
}

# 方案2: 完全移除（推荐）
# 在compute()中注释掉兑现路径维度，或设为0权重
```

#### 3.2 说明

- **TenbaggerEvaluator的stage维度** (20%) 保留，作为主要阶段评估
- **ScoreCard的兑现路径** 降权或移除，避免重复计分
- **阶段信息** 仍保留在ScoreCard的`current_stage`字段，用于解释

---

### 4. 一票否决规则引擎

#### 4.1 新增VetoRuleEngine类

**位置**: `mcp_servers/utils/scorecard.py` (新增)

```python
class VetoRuleEngine:
    """一票否决规则引擎"""
    
    VETO_RULES = [
        {
            "name": "ST/退市风险",
            "check": lambda financials: financials.get("is_st", False) or financials.get("delisting_risk", False),
            "message": "ST股票或存在退市风险"
        },
        {
            "name": "重大违规",
            "check": lambda financials: financials.get("major_violation", False),
            "message": "存在重大违规记录"
        },
        {
            "name": "经营现金流长期为负",
            "check": lambda financials: (
                financials.get("cash_flow_negative_years", 0) >= 2 and
                financials.get("revenue_growth", 0) < 10
            ),
            "message": "经营现金流连续2年以上为负且营收增长不足"
        },
        {
            "name": "高杠杆短债压力",
            "check": lambda financials: (
                financials.get("debt_ratio", 0) > 70 and
                financials.get("short_debt_ratio", 0) > 0.8
            ),
            "message": "负债率>70%且短债比例>80%"
        },
        {
            "name": "商誉/非经常损益主导",
            "check": lambda financials: (
                financials.get("goodwill_ratio", 0) > 0.5 or
                financials.get("non_recurring_ratio", 0) > 0.8
            ),
            "message": "商誉占比>50%或非经常损益占比>80%"
        }
    ]
    
    def check_veto(self, financial_data: Dict = None) -> Tuple[bool, List[str]]:
        """
        检查是否触发否决规则
        
        Returns:
            (is_vetoed, veto_messages)
        """
        if not financial_data:
            return False, []
        
        veto_messages = []
        for rule in self.VETO_RULES:
            try:
                if rule["check"](financial_data):
                    veto_messages.append(f"{rule['name']}: {rule['message']}")
            except Exception as e:
                logger.warning(f"Veto rule {rule['name']} check failed: {e}")
        
        return len(veto_messages) > 0, veto_messages
```

#### 4.2 在compute()中集成

```python
def compute(self, ...) -> ScoreCard:
    # 1. 先检查否决规则
    veto_engine = VetoRuleEngine()
    is_vetoed, veto_messages = veto_engine.check_veto(financial_data)
    
    if is_vetoed:
        # 触发否决：直接返回低分卡
        return ScoreCard(
            card_id=f"sc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}",
            security_id=security_id,
            total_score=20.0,  # 强制低分
            grade="F",
            dimensions=[],
            current_stage=stage_record.get("current_stage", "") if stage_record else "",
            missing_ratio=1.0,
            confidence=0.3,
            quality_flag="poor",
            veto_triggered=True,  # 新增字段
            veto_messages=veto_messages,  # 新增字段
            version="v2"
        )
    
    # 2. 正常计算流程
    # ...
```

---

## 📊 改进效果预期

### 改进前问题
- 评分卡大量100分
- 推荐率极高（14/15 = 93%）
- 缺失数据不吃亏
- Stage双重计分导致总分虚高

### 改进后预期
- **评分分布更合理**: 占位维度保守分，总分下降
- **推荐率降低**: 预计A级以上控制在30-50%
- **数据质量可见**: confidence和quality_flag输出
- **风险过滤**: 一票否决规则过滤雷股
- **Stage不重复**: 取消双重计分

---

## 🔧 实施步骤

### Step 1: 修改ScoreCard类定义 ✅
- 添加数据质量字段
- 版本升级到v2

### Step 2: 修改compute()方法 ✅
- 添加数据质量计算
- 添加置信度衰减
- 集成否决规则检查

### Step 3: 修改各维度评分方法 ✅
- 产业位置: 60→35，标记占位
- 研究关注: 缺数据时45分（非高分）
- 兑现路径: 降权或移除

### Step 4: 添加VetoRuleEngine ✅
- 实现5条否决规则
- 集成到compute()流程

### Step 5: 更新TenbaggerEvaluator ✅
- 添加置信度衰减
- 增强风险评估权重

---

## 📝 代码修改清单

### mcp_servers/utils/scorecard.py

1. **ScoreCard类** (第42-90行)
   - [x] 添加`missing_ratio`, `confidence`, `quality_flag`, `placeholder_count`
   - [x] 版本升级到`v2`

2. **compute()方法** (第170-235行)
   - [x] 添加数据质量计算逻辑
   - [x] 添加置信度衰减
   - [x] 集成否决规则检查

3. **_score_industry_position()** (第237-255行)
   - [x] 分数: 60→35
   - [x] 标记placeholder=True

4. **_score_research_attention()** (第330-352行)
   - [x] 缺数据时: 45分（非高分）
   - [x] 标记placeholder

5. **兑现路径维度**
   - [x] 权重: 0.20→0.05 或移除

6. **新增VetoRuleEngine类**
   - [x] 实现5条否决规则

### mcp_servers/utils/tenbagger_evaluator.py

1. **evaluate()方法**
   - [x] 添加置信度衰减
   - [x] 集成否决规则检查

2. **_eval_risk()方法**
   - [x] 增强风险评估规则
   - [x] 权重考虑提升（可选）

---

## ⚠️ 注意事项

1. **向后兼容**: 
   - 保留原有字段，新增字段有默认值
   - version字段用于区分新旧版本

2. **数据依赖**:
   - 否决规则需要财务数据支持
   - 部分规则可能需要代理指标

3. **测试验证**:
   - 运行改进后的系统，对比改进前后结果
   - 检查推荐率是否降低
   - 验证否决规则是否生效

---

## 📚 相关文档

- `docs/TENBAGGER_SCORING_REVIEW_SUMMARY.md` - 评审总结
- `docs/TENBAGGER_SCORING_LOGIC.md` - 评分逻辑详解
- `mcp_servers/utils/scorecard.py` - ScoreCard实现
- `mcp_servers/utils/tenbagger_evaluator.py` - TenbaggerEvaluator实现

---

*文档版本: 1.0 | 创建时间: 2025-12-19*

