# 投资标的筛选与报告生成 MCP Server - 功能总结

> **创建时间**: 2026-01-06  
> **目的**: 总结现有功能，给出统一实现方案

---

## 📊 现有功能检查结果

### ✅ 已存在的功能

#### 1. 候选池构建
**位置**: `mcp_servers/data_source_server_v2.py`, `mcp_servers/trquant_core_server.py`

**工具**:
- `data_source.candidate_pool` - 基于投资主线构建候选股票池
- `data.candidate_pool` - 候选池构建（trquant_core_server）

**实现**:
- 使用 `CandidatePoolBuilder` 从主线构建候选池
- 支持分层候选池（L0-L3）
- ✅ **路径正确**: 使用 `Path(__file__).parent.parent` 指向ope项目

#### 2. 十倍股筛选
**位置**: `mcp_servers/utils/tenbagger_multifactor_tools.py`

**工具**:
- `tenbagger.multifactor.scan` - 扫描科技主线股票并进行多因子打分
- `tenbagger.multifactor.score` - 单股评分
- `tenbagger.multifactor.stage` - 识别成长阶段(S0-S5)
- `tenbagger.multifactor.backtest` - 回测
- `tenbagger.multifactor.report` - 生成报告

**实现**:
- 多因子评分系统
- 阶段识别（S0-S5）
- ✅ **路径正确**: 使用 `Path(__file__).parent.parent.parent` 指向ope项目

#### 3. 报告生成
**位置**: `mcp_servers/report_server.py`

**工具**:
- `report.generate` - 生成回测报告（HTML/PDF/Markdown/JSON）
- `report.compare` - 策略对比报告
- `report.diagnosis` - 策略诊断报告

**注意**: ⚠️ 主要是回测报告，不是个股分析报告

#### 4. 工作流集成
**位置**: `mcp_servers/workflow_9steps_server.py`

**功能**:
- 完整的9步工作流
- 步骤4: 候选池构建 → `data_source.candidate_pool`
- ✅ **路径正确**: 使用 `Path(__file__).parent.parent` 指向ope项目

### ❌ 缺失的功能

1. **统一的投资标的筛选接口**
   - 需要整合：十倍股、主线题材、用户指定、科技高成长
   - 现有功能分散在不同地方

2. **个股深度分析报告生成（MCP接口）**
   - 现有实现：`scripts/reports/junsheng_full_analysis_report.py`
   - 但没有MCP工具接口

3. **批量分析功能**
   - 需要支持批量分析多只股票

4. **多种筛选策略的统一封装**
   - 需要统一接口，方便调用

---

## 🎯 最佳实现方案

### 方案1: 创建新的统一MCP Server（推荐）

**优点**:
- ✅ 统一接口，降低使用复杂度
- ✅ 不影响现有功能
- ✅ 易于扩展新策略
- ✅ 统一报告格式

**实现**:
1. 创建 `mcp_servers/investment_target_server.py`
2. 创建 `core/investment_target_analyzer.py`（统一分析器）
3. 封装现有筛选逻辑
4. 统一报告生成

**工具列表**:
- `investment.screen` - 筛选投资标的
- `investment.analyze` - 深度分析单只股票
- `investment.report` - 生成分析报告
- `investment.batch_analyze` - 批量分析
- `investment.list_strategies` - 列出可用策略

### 方案2: 扩展现有MCP Server

**优点**:
- ✅ 复用现有基础设施
- ✅ 减少服务器数量

**缺点**:
- ❌ 可能影响现有功能
- ❌ 代码耦合度高

**实现**:
- 在 `trquant_core_server.py` 中添加 `investment.*` 工具
- 在 `report_server.py` 中添加个股分析报告生成

---

## 📝 实施建议

### 推荐方案：方案1（创建新的统一MCP Server）

**理由**:
1. **职责清晰**: 专门负责投资标的筛选和分析
2. **易于维护**: 独立模块，不影响现有功能
3. **易于扩展**: 方便添加新的筛选策略
4. **统一接口**: 一个Server提供所有相关功能

### 实施步骤

#### 步骤1: 创建统一分析器
```python
# core/investment_target_analyzer.py
class InvestmentTargetAnalyzer:
    def screen(self, strategy, ...):  # 统一筛选接口
    def analyze(self, stock_code, ...):  # 统一分析接口
    def generate_report(self, stock_code, ...):  # 统一报告生成
```

#### 步骤2: 创建MCP Server
```python
# mcp_servers/investment_target_server.py
TOOLS = [
    Tool(name="investment.screen", ...),
    Tool(name="investment.analyze", ...),
    Tool(name="investment.report", ...),
    Tool(name="investment.batch_analyze", ...),
    Tool(name="investment.list_strategies", ...),
]
```

#### 步骤3: 统一报告生成
- 提取公共HTML模板
- 统一数据格式
- 支持多种报告类型

#### 步骤4: 测试验证
- 单元测试
- 集成测试
- 端到端测试

---

## 🔍 现有代码复用清单

### 可直接复用

1. **数据获取**:
   - ✅ JQData认证: `config/config_manager.py`
   - ✅ CNINFO爬虫: `mcp_servers/crawlers/cninfo_crawler.py`

2. **筛选逻辑**:
   - ✅ 十倍股分析: `research/short_mid_term_signal_selector/tenbagger_deep_analysis.py`
   - ✅ 主线筛选: `research/short_mid_term_signal_selector/tenbagger_mainline_screener.py`
   - ✅ 早期识别: `research/short_mid_term_signal_selector/tenbagger_early_screener.py`
   - ✅ 科技高成长: `research/short_mid_term_signal_selector/tech_growth_screener.py`

3. **报告模板**:
   - ✅ HTML报告结构: `scripts/reports/junsheng_full_analysis_report.py`
   - ✅ 报告生成逻辑: `scripts/reports/guosheng_full_analysis_report.py`

### 需要封装

1. **统一筛选接口**: 封装各种筛选策略
2. **统一分析接口**: 封装个股分析逻辑
3. **统一报告生成**: 提取公共模板

---

## ✅ 验证检查清单

### 路径检查
- [x] `trquant_core_server.py` - ✅ 使用 `Path(__file__).parent.parent`
- [x] `data_source_server_v2.py` - ✅ 使用 `Path(__file__).parent.parent`
- [x] `workflow_9steps_server.py` - ✅ 使用 `Path(__file__).parent.parent`
- [x] `tenbagger_multifactor_tools.py` - ✅ 使用 `Path(__file__).parent.parent.parent`

### 功能检查
- [x] 候选池构建 - ✅ 已存在
- [x] 十倍股筛选 - ✅ 已存在
- [x] 报告生成 - ⚠️ 主要是回测报告
- [ ] 统一筛选接口 - ❌ 缺失
- [ ] 个股分析报告（MCP） - ❌ 缺失
- [ ] 批量分析 - ❌ 缺失

---

## 🚀 下一步行动

1. **创建统一分析器** (`core/investment_target_analyzer.py`)
2. **创建MCP Server** (`mcp_servers/investment_target_server.py`)
3. **统一报告生成** (提取公共模板)
4. **测试验证** (单元测试 + 集成测试)
5. **集成到工作流** (更新 `workflow_9steps_server.py`)

---

**最后更新**: 2026-01-06  
**状态**: 设计完成，等待实施
