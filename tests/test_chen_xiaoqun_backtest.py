"""
陈小群战法回测引擎单元测试

测试内容:
1. 配置类初始化
2. 引擎初始化和重置
3. 买入/卖出执行
4. 止损止盈逻辑
5. 结果计算
6. 边界情况处理
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.strategies.chen_xiaoqun import (
    ChenXiaoqunBacktestConfig,
    ChenXiaoqunBacktestEngine,
    ChenXiaoqunBacktestResult,
    run_chen_xiaoqun_backtest
)


class TestChenXiaoqunBacktestConfig:
    """测试回测配置类"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = ChenXiaoqunBacktestConfig()
        
        assert config.initial_capital == 1000000.0
        assert config.commission == 0.0003
        assert config.stamp_tax == 0.001
        assert config.slippage == 0.001
        assert config.stop_loss_pct == -0.10
        assert config.take_profit_pct == 0.20
        assert config.max_holding_days == 5
    
    def test_custom_config(self):
        """测试自定义配置"""
        config = ChenXiaoqunBacktestConfig(
            start_date='2025-12-01',
            end_date='2026-01-14',
            initial_capital=500000.0,
            commission=0.0005,
            stop_loss_pct=-0.05
        )
        
        assert config.start_date == '2025-12-01'
        assert config.end_date == '2026-01-14'
        assert config.initial_capital == 500000.0
        assert config.commission == 0.0005
        assert config.stop_loss_pct == -0.05


class TestChenXiaoqunBacktestEngine:
    """测试回测引擎"""
    
    @pytest.fixture
    def engine(self):
        """创建测试引擎"""
        config = ChenXiaoqunBacktestConfig(
            start_date='2025-12-01',
            end_date='2025-12-31',
            initial_capital=1000000.0
        )
        return ChenXiaoqunBacktestEngine(config)
    
    @pytest.fixture
    def sample_market_data(self):
        """创建示例市场数据"""
        return {
            '2025-12-01': {
                'limit_up_count': 45,
                'zhaban_rate': 15.0,
                'max_height': 5,
                'limit_up_df': None
            },
            '2025-12-02': {
                'limit_up_count': 60,
                'zhaban_rate': 18.0,
                'max_height': 6,
                'limit_up_df': None
            },
            '2025-12-03': {
                'limit_up_count': 80,
                'zhaban_rate': 22.0,
                'max_height': 7,
                'limit_up_df': None
            }
        }
    
    def test_engine_initialization(self, engine):
        """测试引擎初始化"""
        assert engine.cash == 1000000.0
        assert engine.positions == {}
        assert engine.trades == []
        assert engine.equity_history == []
        assert engine.daily_cycles == []
    
    def test_engine_reset(self, engine):
        """测试引擎重置"""
        # 修改状态
        engine.cash = 500000.0
        engine.positions = {'000001.XSHE': {'shares': 1000, 'cost': 10.0}}
        engine.trades.append({'action': 'buy'})
        
        # 重置
        engine.reset()
        
        # 验证
        assert engine.cash == 1000000.0
        assert engine.positions == {}
        assert engine.trades == []
    
    def test_parse_position_str(self, engine):
        """测试仓位字符串解析"""
        test_cases = [
            ('10%', 0.1),
            ('50%+', 0.5),
            ('20-30%', 0.25),
            ('0%', 0.0),
            ('60%+', 0.6),
            ('10-20%', 0.15),
            (0.3, 0.3),  # 数值输入
            (None, 0.0),  # None输入
        ]
        
        for input_val, expected in test_cases:
            result = engine._parse_position_str(input_val)
            assert abs(result - expected) < 0.01, f"Failed for {input_val}: got {result}, expected {expected}"
    
    def test_get_portfolio_value(self, engine):
        """测试组合市值计算"""
        # 初始状态：只有现金
        assert engine.get_portfolio_value('2025-12-01', {}) == 1000000.0
        
        # 有持仓时
        engine.positions = {
            '000001.XSHE': {'shares': 1000, 'cost': 10.0},
            '000002.XSHE': {'shares': 500, 'cost': 20.0}
        }
        engine.cash = 970000.0
        
        # 使用当前价格
        price_data = {
            '000001.XSHE': 11.0,
            '000002.XSHE': 22.0
        }
        total = engine.get_portfolio_value('2025-12-01', price_data)
        expected = 970000.0 + 1000 * 11.0 + 500 * 22.0
        assert abs(total - expected) < 0.01
        
        # 无价格数据时使用成本价
        total_no_price = engine.get_portfolio_value('2025-12-01', {})
        expected_no_price = 970000.0 + 1000 * 10.0 + 500 * 20.0
        assert abs(total_no_price - expected_no_price) < 0.01
    
    def test_execute_buy(self, engine):
        """测试买入执行"""
        # 买入10%仓位
        success = engine.execute_buy('2025-12-01', '000001.XSHE', 10.0, 0.10)
        
        assert success == True
        assert '000001.XSHE' in engine.positions
        assert engine.positions['000001.XSHE']['shares'] > 0
        assert engine.positions['000001.XSHE']['cost'] > 0
        assert engine.cash < 1000000.0
        assert len(engine.trades) == 1
        assert engine.trades[0]['action'] == 'buy'
    
    def test_execute_buy_insufficient_funds(self, engine):
        """测试资金不足时买入"""
        engine.cash = 100.0  # 很少的现金
        
        # 尝试买入大仓位
        success = engine.execute_buy('2025-12-01', '000001.XSHE', 100.0, 0.50)
        
        assert success == False
    
    def test_execute_sell(self, engine):
        """测试卖出执行"""
        # 先建仓
        engine.positions = {
            '000001.XSHE': {'shares': 1000, 'cost': 10.0, 'buy_date': '2025-12-01'}
        }
        engine.cash = 990000.0
        
        # 卖出（假设价格上涨到11元）
        success = engine.execute_sell('2025-12-02', '000001.XSHE', 11.0, '止盈')
        
        assert success == True
        assert '000001.XSHE' not in engine.positions
        assert engine.cash > 990000.0  # 卖出后现金增加
        assert len(engine.trades) == 1
        assert engine.trades[0]['action'] == 'sell'
        assert engine.trades[0]['reason'] == '止盈'
    
    def test_execute_sell_no_position(self, engine):
        """测试无持仓时卖出"""
        success = engine.execute_sell('2025-12-01', '000001.XSHE', 10.0, '止损')
        
        assert success == False
    
    def test_run_with_empty_data(self, engine):
        """测试空数据回测"""
        result = engine.run(
            market_data_history={},
            trade_days=[],
            jq_client=None,
            verbose=False
        )
        
        assert isinstance(result, ChenXiaoqunBacktestResult)
        assert result.total_trades == 0
    
    def test_run_with_sample_data(self, engine, sample_market_data):
        """测试使用示例数据回测"""
        trade_days = list(sample_market_data.keys())
        
        result = engine.run(
            market_data_history=sample_market_data,
            trade_days=trade_days,
            jq_client=None,
            verbose=False
        )
        
        assert isinstance(result, ChenXiaoqunBacktestResult)
        assert result.start_date == '2025-12-01'
        assert result.end_date == '2025-12-03'
        assert len(result.daily_cycles) == 3  # 3天的周期记录
    
    def test_run_skips_invalid_data(self, engine):
        """测试跳过无效数据"""
        market_data = {
            '2025-12-01': None,  # 空数据
            '2025-12-02': {'invalid': 'data'},  # 缺少必需字段
            '2025-12-03': {
                'limit_up_count': 50,
                'zhaban_rate': 15.0,
                'max_height': 5,
                'limit_up_df': None
            }
        }
        trade_days = list(market_data.keys())
        
        result = engine.run(
            market_data_history=market_data,
            trade_days=trade_days,
            jq_client=None,
            verbose=False
        )
        
        # 只有12-03有有效数据
        assert len(result.daily_cycles) == 1


class TestChenXiaoqunBacktestResult:
    """测试回测结果类"""
    
    def test_default_result(self):
        """测试默认结果"""
        result = ChenXiaoqunBacktestResult()
        
        assert result.total_return == 0.0
        assert result.total_trades == 0
        assert result.win_rate == 0.0
        assert result.daily_equity == []
        assert result.trades == []
    
    def test_result_summary(self):
        """测试结果摘要"""
        result = ChenXiaoqunBacktestResult(
            start_date='2025-12-01',
            end_date='2025-12-31',
            initial_capital=1000000.0,
            final_capital=1100000.0,
            total_return=0.10,
            annualized_return=0.30,
            max_drawdown=0.05,
            sharpe_ratio=1.5,
            total_trades=20,
            win_rate=0.60
        )
        
        summary = result.summary()
        
        assert '2025-12-01' in summary
        assert '2025-12-31' in summary
        assert '10.00%' in summary  # total_return
        assert '30.00%' in summary  # annualized_return
        assert '5.00%' in summary   # max_drawdown
        assert '1.50' in summary    # sharpe_ratio
        assert '20' in summary      # total_trades
        assert '60.00%' in summary  # win_rate


class TestQuickBacktestFunction:
    """测试快捷回测函数"""
    
    def test_run_chen_xiaoqun_backtest(self):
        """测试快捷回测函数"""
        market_data = {
            '2025-12-01': {
                'limit_up_count': 45,
                'zhaban_rate': 15.0,
                'max_height': 5,
                'limit_up_df': None
            }
        }
        trade_days = ['2025-12-01']
        
        result = run_chen_xiaoqun_backtest(
            market_data_history=market_data,
            trade_days=trade_days,
            jq_client=None,
            verbose=False
        )
        
        assert isinstance(result, ChenXiaoqunBacktestResult)
    
    def test_run_chen_xiaoqun_backtest_with_config(self):
        """测试带配置的快捷回测"""
        config = ChenXiaoqunBacktestConfig(
            initial_capital=500000.0
        )
        
        result = run_chen_xiaoqun_backtest(
            market_data_history={},
            trade_days=[],
            config=config,
            verbose=False
        )
        
        assert result.initial_capital == 500000.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
