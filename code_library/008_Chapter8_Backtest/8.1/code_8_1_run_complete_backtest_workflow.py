"""
文件名: code_8_1_run_complete_backtest_workflow.py
保存路径: code_library/008_Chapter8_Backtest/8.1/code_8_1_run_complete_backtest_workflow.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.1_Backtest_Framework_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: run_complete_backtest_workflow

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from core.bullettrade import BulletTradeEngine, BTConfig
from core.ptrade_integration import PTradeDeployer, PTradeConfig
from core.trading.qmt_interface import QMTTrader, QMTConfig

def run_complete_backtest_workflow(
    strategy_path: str,
    start_date: str,
    end_date: str,
    deploy_to_ptrade: bool = True,
    deploy_to_qmt: bool = False
) -> Dict:
        """
    run_complete_backtest_workflow函数
    
    **设计原理**：
    - **核心功能**：实现run_complete_backtest_workflow的核心逻辑
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
    results = {
        'internal_backtest': None,
        'ptrade_backtest': None,
        'qmt_backtest': None,
        'deployment_status': {}
    }
    
    # ========== 第一层：内部回测（BulletTrade + 聚宽数据源） ==========
    print("=" * 60)
    print("第一层：内部回测（BulletTrade + 聚宽数据源）")
    print("=" * 60)
    
    # 1. 创建BulletTrade配置
    bt_config = BTConfig(
        start_date=start_date,
        end_date=end_date,
        initial_capital=1000000,
        commission_rate=0.0003,
        stamp_tax_rate=0.001,
        slippage=0.001,
        benchmark="000300.XSHG",
        data_provider="jqdata"  # 使用聚宽数据源
    )
    
    # 2. 初始化BulletTrade引擎
    bt_engine = BulletTradeEngine(bt_config)
    
    # 3. 执行内部回测
    print(f"执行BulletTrade回测: {strategy_path}")
    internal_result = bt_engine.run_backtest(
        strategy_path=strategy_path,
        start_date=start_date,
        end_date=end_date,
        frequency="day"
    )
    
    results['internal_backtest'] = {
        'total_return': internal_result.total_return,
        'annual_return': internal_result.annual_return,
        'max_drawdown': internal_result.max_drawdown,
        'sharpe_ratio': internal_result.sharpe_ratio,
        'report_path': internal_result.report_path
    }
    
    print(f"内部回测完成:")
    print(f"  总收益率: {internal_result.total_return:.2%}")
    print(f"  年化收益率: {internal_result.annual_return:.2%}")
    print(f"  最大回撤: {internal_result.max_drawdown:.2%}")
    print(f"  夏普比率: {internal_result.sharpe_ratio:.2f}")
    
    # 4. 判断是否满足部署条件
    if internal_result.total_return < 0.10:  # 收益率低于10%
        print("警告：内部回测收益率较低，不建议部署到券商平台")
        return results
    
    # ========== 第二层：券商平台回测（PTrade/QMT） ==========
    print("\n" + "=" * 60)
    print("第二层：券商平台回测（国金证券 PTrade/QMT）")
    print("=" * 60)
    
    # 5. PTrade平台部署和回测
    if deploy_to_ptrade:
        print("\n部署到PTrade平台...")
        try:
            ptrade_config = PTradeConfig.load()
            ptrade_deployer = PTradeDeployer(ptrade_config)
            
            # 转换策略代码（聚宽风格 → PTrade格式）
            strategy_code = open(strategy_path, 'r', encoding='utf-8').read()
            ptrade_code = ptrade_deployer.convert_to_ptrade(strategy_code)
            
            # 上传策略
            strategy_name = Path(strategy_path).stem
            ptrade_deployer.upload_strategy(strategy_name, ptrade_code)
            
            # 在PTrade平台执行回测
            print("在PTrade平台执行回测...")
            ptrade_result = ptrade_deployer.run_backtest(
                strategy_name=strategy_name,
                start_date=start_date,
                end_date=end_date
            )
            
            results['ptrade_backtest'] = {
                'total_return': ptrade_result.total_return,
                'annual_return': ptrade_result.annual_return,
                'max_drawdown': ptrade_result.max_drawdown,
                'sharpe_ratio': ptrade_result.sharpe_ratio
            }
            
            print(f"PTrade回测完成:")
            print(f"  总收益率: {ptrade_result.total_return:.2%}")
            print(f"  年化收益率: {ptrade_result.annual_return:.2%}")
            print(f"  最大回撤: {ptrade_result.max_drawdown:.2%}")
            
            # 如果PTrade回测通过，启动实盘交易
            if ptrade_result.total_return > 0.15:
                print("PTrade回测通过，启动实盘交易...")
                ptrade_deployer.start_live_trading(strategy_name)
                results['deployment_status']['ptrade'] = 'live_trading'
            else:
                results['deployment_status']['ptrade'] = 'backtest_only'
                
        except Exception as e:
            print(f"PTrade部署失败: {e}")
            results['deployment_status']['ptrade'] = f'failed: {str(e)}'
    
    # 6. QMT平台部署和回测
    if deploy_to_qmt:
        print("\n部署到QMT平台...")
        try:
            qmt_config = QMTConfig(
                qmt_path="/path/to/qmt",
                account_id="8885019982",
                session_id=123456
            )
            qmt_trader = QMTTrader(qmt_config)
            
            if qmt_trader.connect():
                # 上传策略
                strategy_code = open(strategy_path, 'r', encoding='utf-8').read()
                strategy_name = Path(strategy_path).stem
                qmt_trader.upload_strategy(strategy_name, strategy_code)
                
                # 在QMT平台执行回测
                print("在QMT平台执行回测...")
                qmt_result = qmt_trader.run_backtest(
                    strategy_name=strategy_name,
                    start_date=start_date,
                    end_date=end_date
                )
                
                results['qmt_backtest'] = {
                    'total_return': qmt_result.total_return,
                    'annual_return': qmt_result.annual_return,
                    'max_drawdown': qmt_result.max_drawdown,
                    'sharpe_ratio': qmt_result.sharpe_ratio
                }
                
                print(f"QMT回测完成:")
                print(f"  总收益率: {qmt_result.total_return:.2%}")
                print(f"  年化收益率: {qmt_result.annual_return:.2%}")
                print(f"  最大回撤: {qmt_result.max_drawdown:.2%}")
                
                # 如果QMT回测通过，启动实盘交易
                if qmt_result.total_return > 0.15:
                    print("QMT回测通过，启动实盘交易...")
                    qmt_trader.start_live_trading(strategy_name)
                    results['deployment_status']['qmt'] = 'live_trading'
                else:
                    results['deployment_status']['qmt'] = 'backtest_only'
            else:
                print("QMT连接失败")
                results['deployment_status']['qmt'] = 'connection_failed'
                
        except Exception as e:
            print(f"QMT部署失败: {e}")
            results['deployment_status']['qmt'] = f'failed: {str(e)}'
    
    return results