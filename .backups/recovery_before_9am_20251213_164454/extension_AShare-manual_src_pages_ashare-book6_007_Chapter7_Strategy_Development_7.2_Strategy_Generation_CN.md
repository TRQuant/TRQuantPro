---
title: 7.2 策略生成
lang: zh
layout: /src/layouts/Layout.astro
---

# 7.2 策略生成

## 概述

策略生成是策略开发的核心组成部分，通过Strategy KB和Workflow Server实现从投资主线到可执行策略代码的自动化生成。

> **适用版本**: v1.0.0+  
> **优先级**: P0  
> **最后更新**: 2025-12-10

## 功能说明

策略生成功能通过`workflow.strategy.generate_candidate`工具实现，该工具：

1. **检索Strategy KB研究卡**：根据投资主线、候选池、因子候选，检索相关的研究卡和规则
2. **应用规则约束**：使用`strategy_kb.rule.validate`验证策略草案是否符合硬约束
3. **生成策略草案**：基于研究卡和规则，生成结构化的策略草案（JSON格式）
4. **生成Python代码**：将策略草案转换为可执行的Python策略代码
5. **保存策略文件**：将生成的策略代码保存为`.py`文件

## 工作流程

### 输入

- **投资主线**（Mainline）：当前市场的主要投资方向
- **候选池**（Candidate Pool）：可交易的股票池
- **因子候选**（Factor Candidates）：可用于策略的因子列表

### 处理步骤

1. **规则检索**：从Strategy KB获取相关规则（约束条件、风险模型、成本模型等）
2. **研究卡检索**：使用向量检索从Strategy KB中检索相关研究卡
3. **策略草案生成**：基于检索结果，生成结构化的策略草案
4. **规则验证**：使用`strategy_kb.rule.validate`验证策略草案
5. **Python代码生成**：将验证通过的策略草案转换为Python代码
6. **文件保存**：保存为`.py`文件到`strategies/generated/`目录

### 输出

- **策略草案**（JSON）：结构化的策略定义
- **Python策略代码**（.py）：可执行的策略文件
- **引用信息**：使用的研究卡和规则引用
- **验证结果**：规则验证状态

## 使用示例

### 基本用法

\`\`\`python
from mcp_servers.workflow_server import workflow_strategy_generate_candidate

# 生成候选策略
result = workflow_strategy_generate_candidate(
    mainline="小市值因子有效性",
    candidate_pool=["000001", "000002", ...],
    factor_candidates=["factor_market_cap", "factor_pe"],
    mode="dry_run"  # 先预览
)

# 查看生成的策略
print(result["strategy_draft"])
print(result["python_file_path"])
\`\`\`

### 完整工作流

\`\`\`python
# 1. 生成候选策略
strategy_result = workflow_strategy_generate_candidate(
    mainline="小市值因子有效性",
    candidate_pool=pool,
    factor_candidates=factors
)

# 2. 回测验证
backtest_result = workflow_run(
    strategy_id=strategy_result["strategy_id"],
    backtest_config=Ellipsis
)

# 3. 策略优化
optimized_result = optimizer_run(
    strategy_id=strategy_result["strategy_id"],
    optimization_config=Ellipsis
)

# 4. 对比报告
comparison = report_compare(
    baseline_id=current_strategy_id,
    candidate_id=optimized_result["strategy_id"]
)
\`\`\`

## 相关资源

### Strategy KB (研究卡)

1. 风格轮动策略研究 (相关性: -0.136)
2. 成长因子策略研究 (相关性: -0.182)
3. 动量因子组合策略 (相关性: -0.193)


### Manual KB / Engineering KB

基于检索到的知识，策略生成功能整合了以下能力：

- **因子库管理**：从因子库中选择和组合因子
- **策略模板**：使用标准化的策略模板结构
- **回测框架**：生成可回测的策略代码
- **优化工具**：支持后续的参数优化和因子权重优化

## 最佳实践

1. **先dry_run后execute**：始终先使用`dry_run`模式预览，确认无误后再执行
2. **规则验证**：确保生成的策略通过所有规则验证
3. **版本管理**：为每个生成的策略打上版本标签
4. **证据记录**：使用`evidence.record`记录策略生成的原因和依据
5. **回测验证**：生成后立即进行回测验证

## 注意事项

- 生成的策略代码需要符合Strategy KB的规则约束
- 策略草案必须包含所有必需字段（universe、entry、exit、position_sizing、risk、cost等）
- 生成的Python代码应该可以直接用于回测
- 建议在生成后立即进行回测验证

## 相关章节

- [7.1 策略模板](7.1_Strategy_Template_CN.md)
- [7.8 优化前的策略规范化](7.8_Strategy_Standardization_CN.md)
- [8.8 策略优化与对比](8.8_Strategy_Optimization_CN.md)
- [10.9 MCP × Cursor × 工具链联用规范](../010_Chapter10_Development_Guide/10.9_MCP_Cursor_Workflow_CN.md)

---

*最后更新: 2025-12-10*
