"""
文件名: code_7_5_test_strategy_workflow.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.5/code_7_5_test_strategy_workflow.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.5_Strategy_Testing_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: test_strategy_workflow

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd

class StrategyIntegrationTest:
    """策略集成测试"""
    
    def test_strategy_workflow(self):
        """
        测试策略完整工作流
        
        **设计原理**：
        - **端到端测试**：测试策略从初始化到执行的完整流程
        - **多交易日模拟**：模拟多个交易日，验证策略的持续运行能力
        - **状态验证**：验证每个阶段的状态，确保策略正常运行
        
        **为什么这样设计**：
        1. **完整性**：端到端测试确保策略各模块协同工作
        2. **真实性**：多交易日模拟更接近实际运行环境
        3. **可靠性**：状态验证确保策略在长期运行中保持稳定
        
        **使用场景**：
        - 策略开发完成后，验证完整工作流
        - 策略修改后，确保不影响整体流程
        - 策略部署前，进行最终验证
        """
        # 设计原理：初始化测试
        # 原因：验证策略初始化是否正确，确保基础环境就绪
        context = create_test_context()
        initialize(context)
        
        # 验证初始化结果
        assert hasattr(context, 'universe')
        assert len(context.universe) > 0
        
        # 设计原理：多交易日模拟
        # 原因：策略需要长期运行，多交易日测试验证持续运行能力
        # 实现方式：使用pd.date_range生成交易日序列，模拟实际运行
        test_dates = pd.date_range('2024-01-01', '2024-01-10', freq='B')
        
        for date in test_dates:
            context.current_dt = date
            
            # 设计原理：按时间顺序执行策略函数
            # 原因：策略函数有执行顺序（盘前→开盘→盘后），需要按顺序调用
            # 盘前处理
            before_market_open(context)
            
            # 开盘处理
            market_open(context)
            
            # 盘后处理
            after_market_close(context)
        
        # 设计原理：最终状态验证
        # 原因：验证策略运行后的最终状态，确保策略正常执行
        # 验证项：总资产>0（策略有持仓），持仓数量<=限制（风控有效）
        assert context.portfolio.total_value > 0
        assert len(context.portfolio.positions) <= context.max_stocks
    
    def test_module_integration(self):
        """测试模块集成"""
        context = create_test_context()
        
        # 测试选股模块与调仓模块的集成
        selected_stocks = select_stocks(context)
        rebalance(context, selected_stocks)
        
        # 验证集成结果
        assert all(
            stock in context.portfolio.positions 
            for stock in selected_stocks[:context.max_stocks]
        )
    
    def test_data_flow(self):
        """测试数据流"""
        context = create_test_context()
        
        # 1. 数据获取
        market_data = get_market_data(context.universe)
        assert market_data is not None
        
        # 2. 因子计算
        factor_scores = calculate_factor_scores(market_data)
        assert factor_scores is not None
        
        # 3. 选股
        selected = select_stocks_by_scores(factor_scores)
        assert len(selected) > 0
        
        # 4. 调仓
        rebalance(context, selected)
        
        # 验证数据流完整性
        assert len(context.portfolio.positions) > 0