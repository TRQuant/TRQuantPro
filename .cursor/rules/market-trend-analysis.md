---
name: "市场趋势分析开发规范"
description: "市场趋势分析模块的开发规范和最佳实践"
type: "agent-requested"
tags: ["market", "trend", "analysis", "workflow"]
---

# 市场趋势分析开发规范

## 工作流程（参考 `00_system_architecture_workflow.ipynb`）

### 研究阶段7步流程

1. **R0: 数据源检测** - 检查JQData、AKShare、MongoDB连接
2. **R1: 市场趋势分析** - 使用MarketTrendAnalyzer分析市场趋势
3. **R2: 主线轮动研究** - 识别投资主线
4. **R3: 因子组合开发** - 开发和优化因子
5. **R4: 投资标的筛选** - 筛选投资标的（不是"候选池构建"）
6. **R5: 风控模块设计** - 设计风控规则
7. **R6: 策略开发与回测** - 开发策略并回测验证

## 核心模块

### MarketTrendAnalyzer

**位置**: `core/market_trend_analyzer.py`

**功能**:
- 多周期趋势分析（周/月/季/半年/年）
- HMM隐状态识别
- 加权融合输出
- 生成workflow_params供下游使用
- 生成investment_universe_filters供标的筛选

**基线实现**: TrendAnalyzer + SimpleHMM（已回测验证）

### TrendAnalyzer

**位置**: `core/trend_analyzer.py`

**功能**: 8维技术指标打分体系

**评分风格**:
- `legacy`: 传统硬阈值方式
- `smooth_grouped`: 连续映射 + 因子分组（推荐）

### SimpleHMM

**位置**: `core/trend_ml.py`

**功能**: HMM隐状态识别（v2.0优化版本）

## 配置参数

### 周期定义
- 周: 5个交易日
- 月: 21个交易日
- 季: 63个交易日
- 可扩展: 半年、年、多年

### 权重配置
- Trend权重: 0.8（默认）
- HMM权重: 0.2（默认）
- 支持非线性参数加权模型

### 评分风格
- `smooth_grouped`: 推荐使用
  - 连续映射（避免硬阈值跳变）
  - 因子分组（趋势/震荡/波动率/量价）
  - 组间权重（0.45/0.25/0.15/0.15）
  - 得分限制在 [-100, 100]

## 开发原则

### 1. 基于已验证的基线
- 使用 `TrendAnalyzer`（v1，已回测验证）
- 使用 `SimpleHMM`（优化版本）

### 2. 持续优化
- 通过系统回测优化配置
- 根据最新市场条件调整参数
- 提高置信度预测能力

### 3. 数据源优先
- 优先使用聚宽（JQData）数据源
- 聚宽没有的，使用AKShare补充

## 输出格式

### MarketTrendSignal

```python
@dataclass
class MarketTrendSignal:
    """市场趋势信号"""
    trend_score: float  # 趋势得分 [-100, 100]
    trend_direction: TrendDirection  # 趋势方向
    market_regime: MarketRegime  # 市场状态
    confidence: float  # 置信度 [0, 1]
    workflow_params: WorkflowParams  # 下游工作流参数
    investment_universe_filters: InvestmentUniverseFilters  # 标的筛选参数
```

## 测试要求

### 回测验证
- Phase 1回测: 短周期验证
- Phase 2回测: 长周期验证
- 结果保存到MongoDB，支持版本管理

### 可视化要求
- 趋势得分时间序列图
- 多周期对比图
- 置信度分布图
