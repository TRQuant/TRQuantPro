#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信号一致性测试
==============

验证向量化因子/信号计算与旧实现一致
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
import pandas as pd
import numpy as np

from core.research import (
    ResearchDataProvider,
    FactorCalculator,
    SignalEngine,
    SignalParams,
    VBTBacktest,
    BacktestResult,
)


class TestFactorParity(unittest.TestCase):
    """因子计算一致性测试"""
    
    @classmethod
    def setUpClass(cls):
        """初始化测试数据"""
        cls.provider = ResearchDataProvider(use_cache=True)
        cls.stocks = cls.provider.get_index_stocks('000300.XSHG')[:20]
        cls.data = cls.provider.get_data_matrices(
            symbols=cls.stocks,
            start_date='2024-01-01',
            end_date='2024-03-31',
        )
        cls.calculator = FactorCalculator(use_gpu=False)
    
    def test_momentum_20d_calculation(self):
        """测试20日动量计算"""
        factors = self.calculator.calculate_factors(self.data, ['mom_20d'])
        
        # 手动计算一个股票的动量
        stock = self.stocks[0]
        close = self.data.close[stock]
        expected_mom = (close / close.shift(20) - 1) * 100
        
        # 比较（忽略前20个NaN值）
        actual = factors.mom_20d[stock].iloc[20:]
        expected = expected_mom.iloc[20:]
        
        pd.testing.assert_series_equal(actual, expected, check_names=False)
        print(f"✅ 20日动量计算一致")
    
    def test_rel_position_calculation(self):
        """测试相对位置计算"""
        factors = self.calculator.calculate_factors(self.data, ['rel_position'])
        
        # 手动计算
        stock = self.stocks[0]
        close = self.data.close[stock]
        rolling_min = close.rolling(20, min_periods=1).min()
        rolling_max = close.rolling(20, min_periods=1).max()
        expected = (close - rolling_min) / (rolling_max - rolling_min + 1e-8) * 100
        
        actual = factors.rel_position[stock]
        
        # 比较
        np.testing.assert_array_almost_equal(
            actual.values, expected.values, decimal=4
        )
        print(f"✅ 相对位置计算一致")
    
    def test_vol_ratio_calculation(self):
        """测试量比计算"""
        factors = self.calculator.calculate_factors(self.data, ['vol_ratio'])
        
        # 手动计算
        stock = self.stocks[0]
        volume = self.data.volume[stock]
        vol_ma = volume.rolling(20, min_periods=1).mean()
        expected = volume / (vol_ma + 1e-8)
        
        actual = factors.vol_ratio[stock]
        
        np.testing.assert_array_almost_equal(
            actual.values, expected.values, decimal=4
        )
        print(f"✅ 量比计算一致")


class TestSignalGeneration(unittest.TestCase):
    """信号生成测试"""
    
    @classmethod
    def setUpClass(cls):
        """初始化"""
        cls.provider = ResearchDataProvider(use_cache=True)
        cls.stocks = cls.provider.get_index_stocks('000300.XSHG')[:30]
        cls.data = cls.provider.get_data_matrices(
            symbols=cls.stocks,
            start_date='2024-01-01',
            end_date='2024-06-30',
        )
        cls.calculator = FactorCalculator(use_gpu=False)
        cls.factors = cls.calculator.calculate_factors(cls.data)
    
    def test_entry_conditions(self):
        """测试买入条件"""
        params = SignalParams(
            min_mom_20d=5.0,
            max_mom_20d=50.0,
            max_rel_position=80.0,
            min_vol_ratio=1.0,
        )
        
        engine = SignalEngine(params=params)
        signals = engine.generate_signals(self.data, self.factors, params)
        
        # 验证entries是布尔矩阵
        self.assertTrue(signals.entries.dtypes.unique()[0] == bool)
        
        # 验证满足条件的信号
        mom = self.factors.mom_20d
        pos = self.factors.rel_position
        vol = self.factors.vol_ratio
        
        expected_cond = (
            (mom >= 5.0) & (mom <= 50.0) &
            (pos <= 80.0) &
            (vol >= 1.0)
        )
        
        # 检查一个样本点
        test_date = signals.entries.index[30]
        test_stock = self.stocks[0]
        
        actual = signals.entries.loc[test_date, test_stock]
        expected = expected_cond.loc[test_date, test_stock]
        
        self.assertEqual(actual, expected)
        print(f"✅ 买入条件信号一致")
    
    def test_rebalance_mask(self):
        """测试调仓日掩码"""
        params = SignalParams(rebalance_period=5)
        engine = SignalEngine(params=params)
        signals = engine.generate_signals(self.data, self.factors, params)
        
        # 验证调仓日间隔
        rebalance_indices = signals.rebalance_mask[signals.rebalance_mask].index
        if len(rebalance_indices) > 1:
            gaps = []
            for i in range(1, len(rebalance_indices)):
                gap = (rebalance_indices[i] - rebalance_indices[i-1]).days
                gaps.append(gap)
            
            # 大部分间隔应该接近5天（考虑周末）
            avg_gap = np.mean(gaps)
            self.assertGreater(avg_gap, 3)
            self.assertLess(avg_gap, 10)
        
        print(f"✅ 调仓日掩码正确")


class TestVBTBacktest(unittest.TestCase):
    """vectorbt回测测试"""
    
    @classmethod
    def setUpClass(cls):
        """初始化"""
        cls.provider = ResearchDataProvider(use_cache=True)
        cls.stocks = cls.provider.get_index_stocks('000300.XSHG')[:30]
        cls.data = cls.provider.get_data_matrices(
            symbols=cls.stocks,
            start_date='2023-01-01',
            end_date='2024-06-30',
        )
        cls.calculator = FactorCalculator(use_gpu=False)
        cls.factors = cls.calculator.calculate_factors(cls.data)
    
    def test_backtest_runs(self):
        """测试回测可以运行"""
        params = SignalParams()
        backtest = VBTBacktest(initial_capital=1000000)
        result = backtest.run(self.data, self.factors, params)
        
        self.assertIsInstance(result, BacktestResult)
        self.assertIsNotNone(result.total_return)
        self.assertIsNotNone(result.annual_return)
        self.assertIsNotNone(result.sharpe_ratio)
        print(f"✅ 回测运行成功")
    
    def test_backtest_metrics_reasonable(self):
        """测试回测指标在合理范围"""
        params = SignalParams()
        backtest = VBTBacktest(initial_capital=1000000)
        result = backtest.run(self.data, self.factors, params)
        
        # 收益率在合理范围（-100% ~ 500%）
        self.assertGreater(result.total_return, -100)
        self.assertLess(result.total_return, 500)
        
        # 夏普比率在合理范围
        self.assertGreater(result.sharpe_ratio, -5)
        self.assertLess(result.sharpe_ratio, 10)
        
        # 最大回撤在0-100%
        self.assertGreaterEqual(result.max_drawdown, 0)
        self.assertLessEqual(result.max_drawdown, 100)
        
        # 胜率在0-100%
        self.assertGreaterEqual(result.win_rate, 0)
        self.assertLessEqual(result.win_rate, 100)
        
        print(f"✅ 回测指标在合理范围")
    
    def test_backtest_speed(self):
        """测试回测速度"""
        import time
        
        params = SignalParams()
        backtest = VBTBacktest(initial_capital=1000000)
        
        start = time.time()
        result = backtest.run(self.data, self.factors, params)
        elapsed = time.time() - start
        
        # 单次回测应该在1秒内完成
        self.assertLess(elapsed, 1.0)
        print(f"✅ 回测速度正常: {elapsed:.3f}秒")


if __name__ == '__main__':
    unittest.main(verbosity=2)
