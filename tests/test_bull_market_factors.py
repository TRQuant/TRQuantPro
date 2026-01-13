# -*- coding: utf-8 -*-
"""
牛市策略因子和信号测试
=====================

测试内容：
1. 涨停因子计算正确性
2. 首板信号识别准确性
3. 综合评分逻辑验证
4. 止损止盈触发验证
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from core.research.data_provider import DataMatrices
from core.research.factors import FactorCalculator, FactorMatrices
from core.research.signals import SignalEngine, SignalParams, SignalType


class TestLimitUpFactors:
    """涨停因子测试"""
    
    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        dates = pd.date_range("2024-01-01", periods=35, freq="D")
        symbols = ["000001.XSHE", "000002.XSHE", "000003.XSHE"]
        
        # 构造收盘价：第一只股票有涨停（涨幅>9.3%）
        # 注意：第31天（index 30）相对第30天（index 29）涨停
        close_data = {
            "000001.XSHE": [10.0] * 30 + [11.0, 11.5, 12.0, 12.5, 13.0],  # index 30涨幅10%
            "000002.XSHE": [10.0] * 35,  # 无涨停
            "000003.XSHE": [10.0] * 28 + [10.0, 11.0, 12.1, 13.31, 14.64, 16.1, 17.0],  # 连续涨停
        }
        close = pd.DataFrame(close_data, index=dates)
        
        volume_data = {
            "000001.XSHE": [1000000] * 30 + [3000000, 3500000, 2000000, 1500000, 1000000],
            "000002.XSHE": [1000000] * 35,
            "000003.XSHE": [1000000] * 28 + [2000000, 3000000, 4000000, 3500000, 3000000, 2500000, 2000000],
        }
        volume = pd.DataFrame(volume_data, index=dates)
        
        return DataMatrices(
            close=close,
            open=close * 0.99,
            high=close * 1.01,
            low=close * 0.98,
            volume=volume,
            amount=volume * close,
        )
    
    def test_is_limit_up(self, sample_data):
        """测试涨停判定"""
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(
            sample_data,
            factor_list=["is_limit_up"]
        )
        
        is_limit_up = factors.is_limit_up
        assert is_limit_up is not None
        
        # 000001第31天涨停 (9.5%涨幅)
        assert is_limit_up.loc[is_limit_up.index[30], "000001.XSHE"] == True
        
        # 000002无涨停
        assert is_limit_up["000002.XSHE"].sum() == 0
        
        # 000003有多次涨停
        assert is_limit_up["000003.XSHE"].sum() >= 2
    
    def test_limit_up_count(self, sample_data):
        """测试涨停次数统计"""
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(
            sample_data,
            factor_list=["is_limit_up", "limit_up_count_5d"]
        )
        
        count = factors.limit_up_count_5d
        assert count is not None
        
        # 000002无涨停，计数应为0
        assert count["000002.XSHE"].max() == 0
    
    def test_is_first_limit_up(self, sample_data):
        """测试首板判定"""
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(
            sample_data,
            factor_list=["is_limit_up", "is_first_limit_up"]
        )
        
        is_first = factors.is_first_limit_up
        assert is_first is not None
        
        # 000001第31天是首板
        assert is_first.loc[is_first.index[30], "000001.XSHE"] == True
        
        # 000002无首板
        assert is_first["000002.XSHE"].sum() == 0


class TestBreakoutFactors:
    """突破因子测试"""
    
    @pytest.fixture
    def breakout_data(self):
        """创建突破测试数据"""
        dates = pd.date_range("2024-01-01", periods=70, freq="D")
        symbols = ["000001.XSHE", "000002.XSHE"]
        
        # 构造收盘价：第一只股票有突破
        close_data = {
            "000001.XSHE": [10.0] * 60 + [11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5],
            "000002.XSHE": [10.0] * 70,  # 无突破
        }
        close = pd.DataFrame(close_data, index=dates)
        
        high_data = {
            "000001.XSHE": [10.2] * 60 + [11.2, 11.7, 12.2, 12.7, 13.2, 13.7, 14.2, 14.7, 15.2, 15.7],
            "000002.XSHE": [10.2] * 70,
        }
        high = pd.DataFrame(high_data, index=dates)
        
        return DataMatrices(
            close=close,
            open=close * 0.99,
            high=high,
            low=close * 0.98,
            volume=pd.DataFrame(1000000, index=dates, columns=symbols),
            amount=pd.DataFrame(10000000, index=dates, columns=symbols),
        )
    
    def test_breakout_60d(self, breakout_data):
        """测试60日突破判定"""
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(
            breakout_data,
            factor_list=["breakout_60d", "breakout_ratio"]
        )
        
        breakout = factors.breakout_60d
        assert breakout is not None
        
        # 000001在第61天后有突破
        assert breakout["000001.XSHE"].iloc[60:].any()
        
        # 000002无突破
        assert breakout["000002.XSHE"].iloc[60:].sum() == 0
    
    def test_breakout_ratio(self, breakout_data):
        """测试突破幅度计算"""
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(
            breakout_data,
            factor_list=["breakout_ratio"]
        )
        
        ratio = factors.breakout_ratio
        assert ratio is not None
        
        # 000001突破幅度应该为正
        assert ratio["000001.XSHE"].iloc[65] > 0


class TestCapitalFlowFactors:
    """资金流向因子测试"""
    
    @pytest.fixture
    def flow_data(self):
        """创建资金流向测试数据"""
        dates = pd.date_range("2024-01-01", periods=20, freq="D")
        symbols = ["000001.XSHE", "000002.XSHE"]
        
        # 构造数据：第一只股票收盘价偏高位（资金流入），第二只偏低位（资金流出）
        close_data = {
            "000001.XSHE": [10.0 + i * 0.1 for i in range(20)],  # 上涨
            "000002.XSHE": [10.0 - i * 0.05 for i in range(20)],  # 下跌
        }
        close = pd.DataFrame(close_data, index=dates)
        
        high_data = {
            "000001.XSHE": [c + 0.05 for c in close_data["000001.XSHE"]],
            "000002.XSHE": [c + 0.2 for c in close_data["000002.XSHE"]],  # 高开低走
        }
        high = pd.DataFrame(high_data, index=dates)
        
        low_data = {
            "000001.XSHE": [c - 0.2 for c in close_data["000001.XSHE"]],  # 低开高走
            "000002.XSHE": [c - 0.05 for c in close_data["000002.XSHE"]],
        }
        low = pd.DataFrame(low_data, index=dates)
        
        amount = pd.DataFrame(10000000, index=dates, columns=symbols)
        
        return DataMatrices(
            close=close,
            open=close * 0.99,
            high=high,
            low=low,
            volume=pd.DataFrame(1000000, index=dates, columns=symbols),
            amount=amount,
        )
    
    def test_main_flow(self, flow_data):
        """测试主力资金流向"""
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(
            flow_data,
            factor_list=["main_flow"]
        )
        
        main_flow = factors.main_flow
        assert main_flow is not None
        
        # 000001收盘价偏高位，资金流向应为正
        assert main_flow["000001.XSHE"].iloc[-1] > 0
        
        # 000002收盘价偏低位，资金流向应为负
        assert main_flow["000002.XSHE"].iloc[-1] < 0
    
    def test_flow_strength(self, flow_data):
        """测试资金流向强度"""
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(
            flow_data,
            factor_list=["main_flow", "flow_strength"]
        )
        
        flow_strength = factors.flow_strength
        assert flow_strength is not None
        
        # 000001资金持续流入，强度应为正
        assert flow_strength["000001.XSHE"].iloc[-1] > 0


class TestSignalEngine:
    """信号引擎测试"""
    
    @pytest.fixture
    def signal_test_data(self):
        """创建信号测试数据"""
        dates = pd.date_range("2024-01-01", periods=40, freq="D")
        symbols = ["000001.XSHE", "000002.XSHE", "000003.XSHE"]
        
        close = pd.DataFrame({
            "000001.XSHE": [10.0] * 30 + [10.95, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5],
            "000002.XSHE": [10.0] * 40,
            "000003.XSHE": [10.0 + i * 0.3 for i in range(40)],
        }, index=dates)
        
        return DataMatrices(
            close=close,
            open=close * 0.99,
            high=close * 1.01,
            low=close * 0.98,
            volume=pd.DataFrame(1000000, index=dates, columns=symbols),
            amount=pd.DataFrame(10000000, index=dates, columns=symbols),
            is_tradeable=pd.DataFrame(True, index=dates, columns=symbols),
        )
    
    def test_signal_generation(self, signal_test_data):
        """测试信号生成"""
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(signal_test_data)
        
        params = SignalParams(
            max_positions=2,
            rebalance_period=5,
        )
        engine = SignalEngine(params=params)
        signals = engine.generate_signals(signal_test_data, factors, params)
        
        assert signals.entries is not None
        assert signals.scores is not None
        assert signals.target_weights is not None
        
        # 检查权重矩阵
        assert signals.target_weights.sum(axis=1).max() <= 1.0 + 1e-6
    
    def test_multi_signal_scoring(self, signal_test_data):
        """测试多信号类型评分"""
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(signal_test_data)
        
        params = SignalParams()
        engine = SignalEngine(params=params)
        signals = engine.generate_signals(signal_test_data, factors, params)
        
        scores = signals.scores
        
        # 评分应该有差异
        assert scores.std().mean() > 0
        
        # 最高分应该接近或超过60（量价齐升信号）
        assert scores.max().max() >= 50


class TestStopLossTakeProfit:
    """止损止盈测试"""
    
    def test_stop_loss_params(self):
        """测试止损参数"""
        params = SignalParams()
        
        # 验证已优化参数
        assert params.stop_loss_pct == -0.10
        assert params.take_profit_pct == 0.30
        assert params.trailing_stop_pct == -0.09
        assert params.trailing_stop_trigger == 0.15
    
    def test_optimized_params(self):
        """测试优化后的参数值"""
        params = SignalParams()
        
        # 验证来自优化的参数
        assert params.min_mom_20d == -1.25
        assert params.max_mom_20d == 25.0
        assert params.max_positions == 5
        assert params.limit_up_threshold == 0.093
        assert params.vol_ratio_threshold_first == 2.5


class TestIntegration:
    """集成测试"""
    
    def test_full_pipeline(self):
        """测试完整流水线"""
        # 创建模拟数据
        dates = pd.date_range("2024-01-01", periods=100, freq="D")
        symbols = [f"00000{i}.XSHE" for i in range(1, 6)]
        
        np.random.seed(42)
        close = pd.DataFrame(
            np.random.randn(100, 5).cumsum(axis=0) + 100,
            index=dates,
            columns=symbols
        )
        volume = pd.DataFrame(
            np.random.randint(500000, 2000000, size=(100, 5)),
            index=dates,
            columns=symbols
        )
        
        data = DataMatrices(
            close=close,
            open=close * 0.99,
            high=close * 1.02,
            low=close * 0.98,
            volume=volume,
            amount=volume * close,
            is_tradeable=pd.DataFrame(True, index=dates, columns=symbols),
        )
        
        # 计算因子
        calculator = FactorCalculator(use_gpu=False)
        factors = calculator.calculate_factors(data)
        
        # 生成信号
        params = SignalParams(
            max_positions=3,
            rebalance_period=5,
        )
        engine = SignalEngine(params=params)
        signals = engine.generate_signals(data, factors, params)
        
        # 验证输出
        assert signals.entries.shape == (100, 5)
        assert signals.scores.shape == (100, 5)
        assert signals.target_weights.shape == (100, 5)
        
        # 验证权重约束
        max_weight_sum = signals.target_weights.sum(axis=1).max()
        assert max_weight_sum <= 1.0 + 1e-6
        
        print("✅ 完整流水线测试通过")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
