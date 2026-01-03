"""
文件名: code_7_6_deploy_strategy_workflow.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.6/code_7_6_deploy_strategy_workflow.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.6_Strategy_Deployment_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: deploy_strategy_workflow

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from core.bullettrade import BulletTradeEngine, BTConfig
from core.ptrade_integration import PTradeDeployer, PTradeConfig
from core.qmt_integration import QMTDeployer, QMTConfig

def deploy_strategy_workflow(
    strategy_path: str,
    start_date: str,
    end_date: str,
    deploy_to_ptrade: bool = False,
    deploy_to_qmt: bool = False
) -> Dict[str, Any]:
        """
    deploy_strategy_workflow函数
    
    **设计原理**：
    - **核心功能**：实现deploy_strategy_workflow的核心逻辑
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
        'backtest_result': None,
        'backtest_passed': False,
        'ptrade_deployment': None,
        'qmt_deployment': None
    }
    
    # ========== 第一步：BulletTrade回测验证 ==========
    print("=" * 60)
    print("第一步：BulletTrade回测验证")
    print("=" * 60)
    
    # 创建BulletTrade配置
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
    
    # 初始化BulletTrade引擎
    bt_engine = BulletTradeEngine(bt_config)
    
    # 执行回测
    backtest_result = bt_engine.run_backtest(
        strategy_path=strategy_path,
        start_date=start_date,
        end_date=end_date,
        frequency="day"
    )
    
    results['backtest_result'] = backtest_result
    
    # ========== 第二步：回测结果验证 ==========
    print("=" * 60)
    print("第二步：回测结果验证")
    print("=" * 60)
    
    # 验证性能指标
    if (backtest_result.sharpe_ratio > 1.0 and 
        backtest_result.max_drawdown < 0.20 and
        backtest_result.annual_return > 0.05):
        results['backtest_passed'] = True
        print("✅ 回测结果验证通过")
    else:
        print("❌ 回测结果验证失败，不满足部署条件")
        return results
    
    # ========== 第三步：策略代码转换和打包 ==========
    print("=" * 60)
    print("第三步：策略代码转换和打包")
    print("=" * 60)
    
    # 读取策略代码
    with open(strategy_path, 'r', encoding='utf-8') as f:
        jq_strategy_code = f.read()
    
    # 创建代码转换器
    converter = StrategyCodeConverter()
    
    # 创建打包器
    packager = StrategyPackager()
    
    # ========== 第四步：部署到PTrade ==========
    if deploy_to_ptrade:
        print("=" * 60)
        print("第四步：部署到PTrade平台")
        print("=" * 60)
        
        # 转换为PTrade格式
        ptrade_code = converter.convert_to_ptrade(jq_strategy_code)
        
        # 保存PTrade格式代码
        ptrade_strategy_path = strategy_path.replace('.py', '_ptrade.py')
        with open(ptrade_strategy_path, 'w', encoding='utf-8') as f:
            f.write(ptrade_code)
        
        # 打包策略
        package_result = packager.package_strategy(
            ptrade_strategy_path,
            output_dir="packages"
        )
        
        # 配置PTrade连接
        ptrade_config = PTradeConfig(
            host="ptrade.gjzq.com",
            port=7709,
            account_id="8885019982",
            strategy_path="/path/to/ptrade/strategies"
        )
        
        # 创建PTrade部署器
        ptrade_deployer = PTradeDeployer(ptrade_config)
        
        # 上传策略
        ptrade_result = ptrade_deployer.upload_strategy(
            package_path=package_result['package_path'],
            strategy_name=package_result['strategy_name']
        )
        
        results['ptrade_deployment'] = ptrade_result
    
    # ========== 第五步：部署到QMT ==========
    if deploy_to_qmt:
        print("=" * 60)
        print("第五步：部署到QMT平台")
        print("=" * 60)
        
        # 转换为QMT格式
        qmt_code = converter.convert_to_qmt(jq_strategy_code)
        
        # 保存QMT格式代码
        qmt_strategy_path = strategy_path.replace('.py', '_qmt.py')
        with open(qmt_strategy_path, 'w', encoding='utf-8') as f:
            f.write(qmt_code)
        
        # 打包策略
        package_result = packager.package_strategy(
            qmt_strategy_path,
            output_dir="packages"
        )
        
        # 配置QMT连接
        qmt_config = QMTConfig(
            qmt_path="C:/QMT",
            account_id="your_account"
        )
        
        # 创建QMT部署器
        qmt_deployer = QMTDeployer(qmt_config)
        
        # 上传策略
        qmt_result = qmt_deployer.upload_strategy(
            package_path=package_result['package_path'],
            strategy_name=package_result['strategy_name']
        )
        
        results['qmt_deployment'] = qmt_result
    
    return results