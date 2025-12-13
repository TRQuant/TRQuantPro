---
title: 9.7 实盘反馈与在线再优化
lang: zh
layout: /src/layouts/Layout.astro
---

# 9.7 实盘反馈与在线再优化

## 概述

实盘反馈与在线再优化是策略从回测到实盘的关键闭环环节。

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-10

## 触发器机制

### 回测触发器

- 性能漂移（Sharpe/MaxDD/胜率/收益稳定性）低于阈值
- 触发条件：`backtest_metrics.sharpe < threshold` 或 `backtest_metrics.max_drawdown > threshold`

### 实盘触发器

- 滑点、成交率、跟踪误差、回撤、因子暴露异常、成本异常
- 触发条件：实时监控指标超过阈值

### 数据触发器

- 缺失率、延迟、异常点、数据源切换
- 触发条件：数据质量指标异常

## 响应动作

### 轻量级响应

- 参数再优化（Optimizer）→ `report.compare` → 推荐版本
- 使用场景：参数微调，不改变策略逻辑

### 中等响应

- 因子重新筛选/权重调整 → 回测 → 产出新版本
- 使用场景：因子失效，需要调整因子组合

### 严重响应

- 策略降级/停用（kill switch）→ 切换安全策略模板
- 使用场景：策略完全失效，需要紧急处理

## 上线门禁（必须强调）

### 默认模式

- 所有写操作默认使用`dry_run`模式，不会实际修改系统

### 执行模式

- 使用`execute`模式需要提供`confirm_token`
- `confirm_token`绑定：工具名 + 参数hash + trace_id + 过期时间

### 证据记录

- 所有写操作自动记录到evidence_server
- 证据包含：操作人、时间、原因、影响范围、回滚方案

### 上线流程

任何"写操作/上线/替换"必须：
1. `dry_run` 模式验证
2. `confirm_token + evidence + git tag + report compare`
3. 全量发布建议走 **job 化**（避免在线直接改）

## 在线优化安全策略

### 在线只能做

- 监控：实时监控策略表现
- 评估：评估策略性能
- 生成候选：生成优化候选策略
- 报告：生成分析报告

### 真正替换上线必须走

- 确认：`confirm_token`确认
- 证据：`evidence.record`记录
- 版本：`git tag`版本化
- 回滚：回滚方案准备

> **重要**：在线优化只能生成候选，真正替换上线必须走完整的安全流程，否则风险不可控。

## 工作流集成

标准闭环流程：

```
数据源检测 → 趋势分析 → 主线识别 → 候选池 → 因子选择 → 
策略生成 → 回测验证 → 策略优化/对比 → 输出定版策略+报告 → 
（纸上交易/模拟）→ 实盘监控 → 在线评估 → 触发再优化 → 
发布新版本策略
```

## 代码示例

\`\`\`python
# 实盘监控示例
from mcp_servers.workflow_server import workflow_run
from mcp_servers.strategy_optimizer_server import optimizer_run
from mcp_servers.report_server import report_compare

# 1. 监控实盘表现
live_metrics = monitor_live_performance(strategy_id)

# 2. 检查触发器
if live_metrics.sharpe < threshold:
    # 3. 触发再优化
    optimized_strategy = optimizer_run(
        strategy_id=strategy_id,
        mode="dry_run"  # 先dry_run
    )
    
    # 4. 对比报告
    comparison = report_compare(
        baseline_id=current_strategy_id,
        candidate_id=optimized_strategy["id"]
    )
    
    # 5. 如果通过，执行上线（需要confirm_token）
    if comparison["recommendation"] == "upgrade":
        workflow_run(
            strategy_id=optimized_strategy["id"],
            mode="execute",
            confirm_token="...",
            evidence={
                "reason": "实盘性能下降，触发再优化",
                "scope": "策略参数调整",
                "rollback": "回退到上一个版本"
            }
        )
\`\`\`

---

*最后更新: 2025-12-10*
