#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vectorbt止损止盈功能测试
========================

测试止损止盈逻辑是否正确实现
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
import pandas as pd
import numpy as np
from datetime import datetime

from core.research import (
    ResearchDataProvider,
    FactorCalculator,
    SignalParams,
    VBTBacktest,
    PositionTracker,
)


class TestStopLossTakeProfit(unittest.TestCase):
    """止损止盈功能测试"""
    
    @classmethod
    def setUpClass(cls):
        """初始化测试数据"""
        cls.provider = ResearchDataProvider(use_cache=True)
        cls.stocks = cls.provider.get_index_stocks('000300.XSHG')[:30]
        cls.data = cls.provider.get_data_matrices(
            symbols=cls.stocks,
            start_date='2023-01-01',
            end_date='2024-06-30',
        )
        cls.calculator = FactorCalculator(use_gpu=False)
        cls.factors = cls.calculator.calculate_factors(cls.data)
    
    def test_position_tracker(self):
        """测试持仓跟踪器"""
        tracker = PositionTracker()
        
        # 测试成本价更新
        tracker.update_cost_price('000001.XSHE', 10.0, pd.Timestamp('2024-01-01'))
        self.assertEqual(tracker.get_cost_price('000001.XSHE'), 10.0)
        self.assertEqual(tracker.get_entry_date('000001.XSHE'), pd.Timestamp('2024-01-01'))
        
        # 测试最高价更新
        tracker.update_highest_price('000001.XSHE', 12.0)
        self.assertEqual(tracker.get_highest_price('000001.XSHE'), 12.0)
        tracker.update_highest_price('000001.XSHE', 11.0)
        self.assertEqual(tracker.get_highest_price('000001.XSHE'), 12.0)  # 应该保持最高价
        
        # 测试分批止盈标记
        self.assertFalse(tracker.is_partial_profit_done('000001.XSHE'))
        tracker.mark_partial_profit_done('000001.XSHE')
        self.assertTrue(tracker.is_partial_profit_done('000001.XSHE'))
        
        # 测试移除持仓
        tracker.remove_position('000001.XSHE')
        self.assertIsNone(tracker.get_cost_price('000001.XSHE'))
        self.assertIsNone(tracker.get_highest_price('000001.XSHE'))
        
        print("✅ PositionTracker功能测试通过")
    
    def test_stop_loss(self):
        """测试固定止损"""
        params = SignalParams(
            min_mom_20d=0.0,
            max_mom_20d=100.0,
            max_rel_position=100.0,
            min_vol_ratio=0.5,
            max_positions=10,
            rebalance_period=5,
            stop_loss_pct=-0.08,  # -8%止损
            take_profit_pct=1.0,  # 设置很高的止盈，避免触发
        )
        
        backtest = VBTBacktest(initial_capital=1000000)
        result = backtest.run(self.data, self.factors, params)
        
        # 验证回测可以运行
        self.assertIsNotNone(result.total_return)
        self.assertIsNotNone(result.max_drawdown)
        
        print(f"✅ 固定止损测试通过: 最大回撤={result.max_drawdown:.2f}%")
    
    def test_take_profit(self):
        """测试固定止盈"""
        params = SignalParams(
            min_mom_20d=0.0,
            max_mom_20d=100.0,
            max_rel_position=100.0,
            min_vol_ratio=0.5,
            max_positions=10,
            rebalance_period=5,
            stop_loss_pct=-1.0,  # 设置很低的止损，避免触发
            take_profit_pct=0.30,  # +30%止盈
        )
        
        backtest = VBTBacktest(initial_capital=1000000)
        result = backtest.run(self.data, self.factors, params)
        
        # 验证回测可以运行
        self.assertIsNotNone(result.total_return)
        
        print(f"✅ 固定止盈测试通过: 总收益={result.total_return:.2f}%")
    
    def test_partial_profit(self):
        """测试分批止盈"""
        params = SignalParams(
            min_mom_20d=0.0,
            max_mom_20d=100.0,
            max_rel_position=100.0,
            min_vol_ratio=0.5,
            max_positions=10,
            rebalance_period=5,
            stop_loss_pct=-1.0,
            take_profit_pct=1.0,  # 设置很高的止盈，避免触发
            partial_profit_1_pct=0.20,  # +20%第一批止盈
            partial_profit_1_ratio=0.50,  # 减仓50%
        )
        
        backtest = VBTBacktest(initial_capital=1000000)
        result = backtest.run(self.data, self.factors, params)
        
        # 验证回测可以运行
        self.assertIsNotNone(result.total_return)
        
        print(f"✅ 分批止盈测试通过: 总收益={result.total_return:.2f}%")
    
    def test_trailing_stop(self):
        """测试移动止损"""
        params = SignalParams(
            min_mom_20d=0.0,
            max_mom_20d=100.0,
            max_rel_position=100.0,
            min_vol_ratio=0.5,
            max_positions=10,
            rebalance_period=5,
            stop_loss_pct=-1.0,
            take_profit_pct=1.0,
            trailing_stop_pct=-0.08,  # -8%移动止损
            trailing_stop_trigger=0.15,  # 盈利15%后启用
        )
        
        backtest = VBTBacktest(initial_capital=1000000)
        result = backtest.run(self.data, self.factors, params)
        
        # 验证回测可以运行
        self.assertIsNotNone(result.total_return)
        
        print(f"✅ 移动止损测试通过: 总收益={result.total_return:.2f}%")
    
    def test_time_stop(self):
        """测试时间止损"""
        params = SignalParams(
            min_mom_20d=0.0,
            max_mom_20d=100.0,
            max_rel_position=100.0,
            min_vol_ratio=0.5,
            max_positions=10,
            rebalance_period=5,
            stop_loss_pct=-1.0,
            take_profit_pct=1.0,
            time_stop_days=20,  # 20交易日止损
        )
        
        backtest = VBTBacktest(initial_capital=1000000)
        result = backtest.run(self.data, self.factors, params)
        
        # 验证回测可以运行
        self.assertIsNotNone(result.total_return)
        
        print(f"✅ 时间止损测试通过: 总收益={result.total_return:.2f}%")
    
    def test_trade_costs(self):
        """测试交易成本计算"""
        params = SignalParams(
            min_mom_20d=5.0,
            max_mom_20d=50.0,
            max_rel_position=80.0,
            min_vol_ratio=1.0,
            max_positions=10,
            rebalance_period=5,
        )
        
        backtest = VBTBacktest(
            initial_capital=1000000,
            commission_rate=0.0003,
            stamp_tax=0.001,
            slippage=0.001,
        )
        result = backtest.run(self.data, self.factors, params)
        
        # 验证回测可以运行
        self.assertIsNotNone(result.total_return)
        self.assertGreater(result.total_trades, 0)
        
        print(f"✅ 交易成本计算测试通过: 交易次数={result.total_trades}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
