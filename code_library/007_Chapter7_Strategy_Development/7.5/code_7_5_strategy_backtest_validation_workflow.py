"""
文件名: code_7_5_strategy_backtest_validation_workflow.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.5/code_7_5_strategy_backtest_validation_workflow.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.5_Strategy_Testing_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: strategy_backtest_validation_workflow

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def strategy_backtest_validation_workflow(
    strategy_path: str,
    start_date: str,
    end_date: str
) -> Dict[str, Any]:
        """
    strategy_backtest_validation_workflow函数
    
    **设计原理**：
    - **核心功能**：实现strategy_backtest_validation_workflow的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    from core.bullettrade import BulletTradeEngine, BTConfig
    
    # 1. 创建回测配置
    bt_config = BTConfig(
        start_date=start_date,
        end_date=end_date,
        initial_capital=1000000,
        commission_rate=0.0003,
        stamp_tax_rate=0.001,
        slippage=0.002,
        benchmark="000300.XSHG",
        data_provider="jqdata"  # 使用聚宽数据源
    )
    
    # 2. 初始化BulletTrade引擎
    engine = BulletTradeEngine(bt_config)
    
    # 3. 执行回测
    backtest_result = engine.run_backtest(
        strategy_path=strategy_path,
        start_date=start_date,
        end_date=end_date,
        frequency="day"
    )
    
    # 4. 验证回测结果
    validator = BacktestResultValidator()
    is_valid, errors = validator.validate_backtest_result(backtest_result)
    
    if not is_valid:
        raise ValueError(f"回测结果验证失败: {errors}")
    
    # 5. 验证性能阈值
    passed, threshold_errors = validator.validate_performance_thresholds(
        backtest_result,
        min_sharpe=1.0,
        max_drawdown=0.20,
        min_annual_return=0.05
    )
    
    # 6. 生成回测报告
    report_path = engine.generate_report(
        backtest_result,
        output_dir="backtest_results"
    )
    
    return {
        'backtest_result': backtest_result,
        'is_valid': is_valid,
        'passed_thresholds': passed,
        'threshold_errors': threshold_errors,
        'report_path': report_path
    }