---
name: 纯已验证因子策略实现
overview: 重构策略系统，移除聚宽因子融合，仅使用7个已验证因子，并完善选股、仓位、风控、止损止盈等模块设计，实现BulletTrade策略代码生成和回测。
todos:
  - id: refactor_multifactor_calculator
    content: 重构MultiFactorCalculator，移除聚宽因子融合，total_score直接等于validated_score
    status: completed
  - id: design_stock_selector
    content: 设计并实现选股逻辑模块（基础过滤、流动性过滤、基本面过滤、因子筛选、综合得分排序）
    status: completed
    dependencies:
      - refactor_multifactor_calculator
  - id: design_position_manager
    content: 设计并实现仓位管理模块（目标仓位计算、仓位分配策略、调仓逻辑）
    status: completed
  - id: design_risk_manager
    content: 设计并实现风险控制模块（止损止盈规则、仓位控制、流动性保护）
    status: completed
  - id: design_stop_loss_profit
    content: 设计并实现止损止盈模块（止损逻辑、止盈逻辑、移动止损、时间止损）
    status: completed
  - id: implement_strategy_generator
    content: 实现BulletTrade策略代码生成器，内联实现7个已验证因子的计算逻辑
    status: completed
    dependencies:
      - design_stock_selector
      - design_position_manager
      - design_risk_manager
      - design_stop_loss_profit
  - id: implement_backtest_integration
    content: 实现BulletTrade回测接口封装，支持策略代码生成和回测执行
    status: completed
    dependencies:
      - implement_strategy_generator
  - id: update_documentation
    content: 更新策略设计文档和因子架构文档，移除聚宽因子相关内容
    status: completed
    dependencies:
      - refactor_multifactor_calculator
---

# 纯已验证因子策略实现计划