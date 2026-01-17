"""
文件名: code_7_5_test_backtest_validation.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.5/code_7_5_test_backtest_validation.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.5_Strategy_Testing_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: test_backtest_validation

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.bullettrade import BulletTradeEngine, BTConfig
from pathlib import Path

def test_backtest_validation():
    """回测验证测试（使用BulletTrade+聚宽数据源）"""
    
    # 设计原理：BulletTrade回测配置
    # 原因：使用BulletTrade进行回测验证，确保策略在历史数据上表现良好
    # 数据源：使用聚宽(JQData)数据源，与策略开发环境一致
    # 配置说明：
    # - start_date/end_date: 回测时间范围，建议至少3年，覆盖不同市场环境
    # - initial_capital: 初始资金，使用标准金额便于对比
    # - commission_rate: 手续费率，与实际交易一致
    # - slippage: 滑点，大单交易时需要考虑
    # - benchmark: 基准指数，用于计算超额收益
    bt_config = BTConfig(
        start_date="2020-01-01",
        end_date="2023-12-31",
        initial_capital=1000000,
        commission_rate=0.0003,
        stamp_tax_rate=0.001,
        slippage=0.002,
        benchmark="000300.XSHG",  # 沪深300
        data_provider="jqdata"    # 使用聚宽数据源
    )
    
    # 设计原理：创建BulletTrade引擎
    # 原因：BulletTrade兼容聚宽API，策略代码无需修改即可回测
    engine = BulletTradeEngine(bt_config)
    
    # 设计原理：检查CLI可用性
    # 原因：BulletTrade CLI是回测执行的关键，需要确保可用
    # 容错性：CLI不可用时抛出异常，避免后续执行失败
    if not engine.check_cli_available():
        raise RuntimeError("BulletTrade CLI不可用，请检查安装")
    
    # 4. 策略代码路径（聚宽风格）
    strategy_path = "strategies/test_strategy.py"
    
    # 5. 执行回测
    backtest_result = engine.run_backtest(
        strategy_path=strategy_path,
        start_date="2020-01-01",
        end_date="2023-12-31",
        frequency="day"  # 日线回测
    )
    
    # 6. 验证回测结果
    assert backtest_result.total_return > 0, "总收益率应为正"
    assert backtest_result.sharpe_ratio > 1.0, "夏普比率应大于1.0"
    assert backtest_result.max_drawdown < 0.20, "最大回撤应小于20%"
    assert backtest_result.annual_return > 0.05, "年化收益率应大于5%"
    
    # 7. 生成HTML报告（可选）
    report_path = engine.generate_report(
        backtest_result, 
        output_dir="backtest_results"
    )
    assert Path(report_path).exists(), "回测报告应已生成"
    
    return backtest_result