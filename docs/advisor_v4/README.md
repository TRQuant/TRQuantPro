# Investment Advisor V4.0 - 提前一周布局系统

> **版本**: V2.0  
> **状态**: ✅ 已完成（阶段1-8）  
> **最后更新**: 2026-01-08

---

## 📋 系统概述

Investment Advisor V4.0 是一个"提前一周布局"的量化投资系统，从"T-5预测T"（5个交易日）升级为"按周定义的提前布局系统"（统一以自然周为单位，动态适配节假日）。

### 核心特性

- ✅ **周频预测窗口**：使用`jq.get_trade_days()`动态获取周内交易日，考虑节假日
- ✅ **聚宽因子集成**：CNE5(40%) + Alpha101/191精选(35%) + 基础财务(25%)
- ✅ **规则引擎**：可解释的入场/出场/仓位规则，易于理解和调整
- ✅ **三层回测架构**：Fast(<5秒) → Standard(<30秒) → Precise(BulletTrade)
- ✅ **MongoDB缓存**：参数哈希缓存，避免重复计算
- ✅ **周度HTML报告**：多Tab格式，包含详细布局计划和交易策略

---

## 🚀 快速开始

### 1. 生成周度布局报告

```bash
# 使用命令行工具
python scripts/generate_weekly_layout_v4.py [--date YYYY-MM-DD] [--top-n 5] [--output filename.html]

# 示例
python scripts/generate_weekly_layout_v4.py --date 2025-09-13 --top-n 8
```

### 2. 程序化调用

```python
from core.advisor_v4.advisor_v4_workflow import AdvisorV4Workflow, AdvisorV4Config

# 初始化配置
config = AdvisorV4Config(
    train_start="2024-01-01",
    train_end="2024-12-31",
    val_start="2025-01-01",
    val_end="2025-08-31",
)

# 创建工作流
workflow = AdvisorV4Workflow(config=config, verbose=True)

# 生成周度布局报告
report_path = workflow.generate_weekly_layout_report(
    anchor_date="2025-09-13",
    top_n=5,
)
print(f"报告路径: {report_path}")
```

### 3. 快速验证（不依赖JQData）

```bash
# 快速验证数据结构和报告生成
python scripts/v4_weekly_layout_smoke_test.py

# 完整集成测试
python scripts/v4_full_integration_test.py
```

---

## 📁 文件结构

### 核心模块

```
core/advisor_v4/
├── advisor_v4_workflow.py      # 主工作流（周频配置、推荐方法、报告生成）
├── jqfactor_calculator.py      # 聚宽因子计算器（CNE5 + Alpha101/191 + 财务）
├── rule_based_strategy.py      # 规则引擎（入场/出场/仓位规则）
├── rule_optimizer.py            # 规则优化器（网格搜索）
├── weekly_layout_planner.py     # 周度布局计划生成器
├── weekly_report_generator.py   # 周度HTML报告生成器
├── multi_factor_calculator.py   # 多因子计算器（集成JQFactorCalculator）
├── trading_strategy.py          # 交易策略（规则引擎融合）
├── backtest_engine.py           # 回测引擎（三层架构集成）
└── data_storage.py              # 数据存储（MongoDB缓存）
```

### 数据模块

```
core/data/
└── fast_data_loader.py          # 快速数据加载器（批量获取、缓存、索引）
```

### 脚本工具

```
scripts/
├── generate_weekly_layout_v4.py      # 命令行工具（生成周度布局报告）
├── v4_weekly_layout_smoke_test.py    # 快速验证脚本
├── v4_full_integration_test.py        # 完整集成测试
├── v4_vectorized_fast_validate.py     # 快速验证层脚本
└── bullettrade_fast_validate_v4.py    # BulletTrade验证脚本
```

---

## 🎯 系统架构

### 数据流

```
JQData (聚宽数据)
    ↓
FastDataLoader (批量获取 + 缓存)
    ↓
JQFactorCalculator (CNE5 + Alpha101/191 + 财务)
    ↓
MultiFactorCalculator (因子组合加权)
    ↓
RuleBasedStrategy (规则引擎评分)
    ↓
XGBoostPredictor (可选ML预测)
    ↓
TradingStrategy (交易信号生成)
    ↓
WeeklyLayoutPlanner (周度布局计划)
    ↓
WeeklyReportGenerator (HTML报告生成)
```

### 三层回测架构

```
Fast Layer (< 5秒)
    ↓ 向量化回测，策略初筛
Standard Layer (< 30秒)
    ↓ 事件驱动，策略优化
Precise Layer (BulletTrade)
    ↓ 完整模拟，最终验证
MongoDB Cache (参数哈希)
```

---

## 📊 报告结构

生成的HTML报告包含以下Tab：

1. **首页总览**
   - 本周投资标的总览
   - 仓位建议
   - 本周布局时间表

2. **市场展望**
   - 当前市场环境
   - 仓位建议
   - 市场观察要点

3. **交易策略**
   - 每只股票的入场计划（分批建仓）
   - 每只股票的出场计划（止盈/止损/时间止损）

4. **风险提示**
   - 风险控制措施
   - 免责声明

5. **个股详情**（每只股票一个Tab）
   - 推荐理由
   - 仓位配置
   - 入场/出场计划
   - 标签

---

## 🔧 配置说明

### AdvisorV4Config

```python
config = AdvisorV4Config(
    train_start="2024-01-01",      # 训练集开始日期
    train_end="2024-12-31",        # 训练集结束日期
    val_start="2025-01-01",        # 验证集开始日期
    val_end="2025-08-31",          # 验证集结束日期
    test_start="2025-09-06",       # 测试集开始日期
    test_end="2025-09-13",         # 测试集结束日期
    lookback_weeks=1,              # 预测窗口（周数）
    # ... 其他配置
)
```

### 因子配置

- **CNE5因子**（权重40%）：size, beta, momentum, liquidity, residual_volatility
- **Alpha101/191因子**（权重35%）：alpha_001 ~ alpha_005（Top5）
- **基础财务因子**（权重25%）：ROE, PE, PB, 净利润增长率, 营收增长率

### 规则配置

- **入场规则**：CNE5 + Alpha + 财务 + 市场环境 + 流动性
- **出场规则**：止盈10% / 止损-8% / 移动止盈3% / 时间止损10天
- **仓位规则**：单票仓位12% / 最大持仓8只 / 行业分散30%

---

## 📈 性能指标

### 回测性能

- ✅ **快速验证层**: < 5秒（向量化回测）
- ✅ **标准回测层**: < 30秒（事件驱动）
- ✅ **精确回测层**: BulletTrade完整模拟
- ✅ **缓存命中率**: MongoDB参数哈希缓存

### 数据加载性能

- ✅ **批量获取**: 使用`jq.get_price()`批量获取多只股票数据
- ✅ **数据缓存**: FastDataLoader本地缓存，避免重复获取
- ✅ **增量更新**: 只获取新增数据

---

## 🧪 测试验证

### 快速验证（不依赖JQData）

```bash
python scripts/v4_weekly_layout_smoke_test.py
```

**测试内容**:
- WeeklyLayoutPlan 数据结构
- WeeklyReportGenerator 报告生成

### 完整集成测试

```bash
python scripts/v4_full_integration_test.py
```

**测试内容**:
- 模块导入测试
- 配置初始化测试
- 周度布局计划生成测试
- HTML报告生成测试
- 工作流方法测试

### 回测验证

```bash
# 快速验证层
python scripts/v4_vectorized_fast_validate.py --start 2025-09-06 --end 2025-09-13

# BulletTrade验证
python scripts/bullettrade_fast_validate_v4.py
```

---

## 📚 参考文档

1. **改进计划V2**: `docs/advisor_v4/INVESTMENT_ADVISOR_V4_PLAN_V2.md`
2. **原计划文档**: `/home/taotao/.cursor/plans/investment_advisor_v4.0_提前一周布局系统_89471cae.plan.md`
3. **RAG知识库摘要**: `docs/knowledge_base/KB_COMPREHENSIVE_SUMMARY.md`
4. **BulletTrade文档**: `docs/07_workflow/BULLETTRADE_BACKTEST_GUIDE.md`

---

## ⚠️ 注意事项

1. **JQData连接**: 生成真实报告需要JQData连接和模型文件
2. **模型训练**: 首次使用需要先运行训练模式生成模型
3. **数据范围**: 确保JQData账号有足够的数据范围
4. **缓存清理**: 如需重新计算，可清理MongoDB缓存

---

## 🐛 故障排除

### 问题1: 模块导入失败

**解决方案**:
```bash
# 确保项目根目录在sys.path中
export PYTHONPATH=/home/taotao/.cursor/worktrees/TRQuant/ope:$PYTHONPATH
```

### 问题2: JQData连接失败

**解决方案**:
```bash
# 检查配置文件
cat config/jqdata_config.json

# 测试连接
python -c "import jqdatasdk as jq; from config.config_manager import get_config_manager; cm = get_config_manager(); cfg = cm.get_config('jqdata'); jq.auth(cfg['username'], cfg['password']); print('✅ 连接成功')"
```

### 问题3: 报告生成失败

**解决方案**:
- 检查输出目录权限
- 确保WeeklyLayoutPlan数据结构完整
- 查看日志文件获取详细错误信息

---

## 📝 更新日志

### V2.0 (2026-01-08)

- ✅ 完成阶段1-8所有开发任务
- ✅ 集成BulletTrade三层回测架构
- ✅ 实现MongoDB缓存机制
- ✅ 完成周度HTML报告生成
- ✅ 通过完整集成测试

### V1.0 (原计划)

- 初始计划文档
- 阶段划分和任务定义

---

**维护者**: TRQuant Team  
**最后更新**: 2026-01-08
