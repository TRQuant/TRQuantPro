#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键生成策略并回测
================
完整演示：生成策略 -> 快速回测 -> 输出报告
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
from datetime import datetime


def run_demo():
    """运行完整演示"""
    print("="*60)
    print("韬睿量化系统 - 策略生成与快速回测演示")
    print("="*60)
    
    start_time = time.time()
    
    # ==================== 步骤1：获取股票池 ====================
    print("\n📊 步骤1: 获取股票池...")
    from core.data.mock_data_generator import get_mock_generator
    mock = get_mock_generator()
    stocks = mock.generate_index_stocks("000300.XSHG", count=30)
    print(f"   股票数量: {len(stocks)}")
    print(f"   示例: {stocks[:5]}")
    
    # ==================== 步骤2：设置回测参数 ====================
    print("\n⚙️ 步骤2: 设置回测参数...")
    start_date = "2024-01-01"
    end_date = "2024-06-30"
    strategy_params = {
        "strategy_type": "momentum",
        "mom_short": 5,
        "mom_long": 20,
        "max_stocks": 10,
        "rebalance_days": 5
    }
    print(f"   回测期间: {start_date} ~ {end_date}")
    print(f"   策略类型: {strategy_params['strategy_type']}")
    print(f"   持股数量: {strategy_params['max_stocks']}")
    
    # ==================== 步骤3：运行快速回测 ====================
    print("\n🚀 步骤3: 运行快速回测...")
    backtest_start = time.time()
    
    from core.backtest.fast_backtest_engine import quick_backtest
    result = quick_backtest(
        securities=stocks,
        start_date=start_date,
        end_date=end_date,
        strategy=strategy_params["strategy_type"],
        use_mock=True,
        mom_short=strategy_params["mom_short"],
        mom_long=strategy_params["mom_long"],
        max_stocks=strategy_params["max_stocks"],
        rebalance_days=strategy_params["rebalance_days"]
    )
    
    backtest_time = time.time() - backtest_start
    print(f"   回测耗时: {backtest_time:.2f}秒")
    
    # ==================== 步骤4：展示结果 ====================
    print("\n📈 步骤4: 回测结果...")
    print(f"   总收益率: {result.total_return*100:.2f}%")
    print(f"   年化收益: {result.annual_return*100:.2f}%")
    print(f"   夏普比率: {result.sharpe_ratio:.2f}")
    print(f"   最大回撤: {result.max_drawdown*100:.2f}%")
    print(f"   胜率: {result.win_rate*100:.1f}%")
    print(f"   交易次数: {result.total_trades}")
    
    # ==================== 步骤5：生成报告 ====================
    print("\n📄 步骤5: 生成可视化报告...")
    try:
        from core.visualization.report_generator import generate_html_report
        
        metrics = {
            "total_return": result.total_return,
            "annual_return": result.annual_return,
            "sharpe_ratio": result.sharpe_ratio,
            "max_drawdown": result.max_drawdown,
            "win_rate": result.win_rate,
            "total_trades": result.total_trades
        }
        
        daily_returns = result.daily_returns.tolist() if result.daily_returns is not None else None
        report_path = generate_html_report(metrics, daily_returns, "动量策略回测报告")
        print(f"   报告路径: {report_path}")
    except Exception as e:
        print(f"   报告生成失败: {e}")
    
    # ==================== 步骤6：生成策略代码 ====================
    print("\n📝 步骤6: 生成策略代码...")
    try:
        from core.templates.strategy_templates import get_template
        template = get_template("momentum")
        code = template.generate_code({
            "short_period": strategy_params["mom_short"],
            "long_period": strategy_params["mom_long"],
            "max_stocks": strategy_params["max_stocks"],
            "rebalance_days": strategy_params["rebalance_days"]
        })
        
        # 保存策略
        strategy_dir = Path(__file__).parent.parent / "strategies" / "generated"
        strategy_dir.mkdir(parents=True, exist_ok=True)
        strategy_file = strategy_dir / f"momentum_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        strategy_file.write_text(code, encoding='utf-8')
        print(f"   策略文件: {strategy_file}")
    except Exception as e:
        print(f"   策略生成失败: {e}")
    
    # ==================== 总结 ====================
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print("✅ 演示完成!")
    print("="*60)
    print(f"总耗时: {total_time:.2f}秒")
    print(f"回测耗时: {backtest_time:.2f}秒 {'✅ <5秒' if backtest_time < 5 else '⚠️ >5秒'}")
    
    return result


def compare_strategies():
    """对比多种策略"""
    print("\n" + "="*60)
    print("策略对比测试")
    print("="*60)
    
    from core.data.mock_data_generator import get_mock_generator
    mock = get_mock_generator()
    stocks = mock.generate_index_stocks(count=30)
    
    strategies = ["momentum", "trend", "value", "multi_factor"]
    results = {}
    
    from core.backtest.fast_backtest_engine import quick_backtest
    
    for strategy in strategies:
        print(f"\n测试策略: {strategy}...")
        result = quick_backtest(
            securities=stocks,
            start_date="2024-01-01",
            end_date="2024-06-30",
            strategy=strategy,
            use_mock=True
        )
        results[strategy] = result
        print(f"  收益: {result.total_return*100:.2f}%, 夏普: {result.sharpe_ratio:.2f}")
    
    # 排名
    print("\n" + "-"*40)
    print("策略排名（按夏普比率）:")
    sorted_results = sorted(results.items(), key=lambda x: x[1].sharpe_ratio, reverse=True)
    for i, (name, r) in enumerate(sorted_results, 1):
        print(f"  {i}. {name}: 夏普={r.sharpe_ratio:.2f}, 收益={r.total_return*100:.2f}%")


if __name__ == "__main__":
    result = run_demo()
    
    # 可选：运行策略对比
    # compare_strategies()
