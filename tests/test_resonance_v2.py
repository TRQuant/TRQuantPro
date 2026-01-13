#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resonance V2 单元测试
====================

测试各层模块的功能正确性

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
import unittest
import warnings
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# 添加项目路径
PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

# 忽略警告
warnings.filterwarnings('ignore')


class TestConfig(unittest.TestCase):
    """测试配置模块"""
    
    def test_config_creation(self):
        """测试配置创建"""
        from core.resonance_v2.config import ResonanceV2Config, MarketState
        
        config = ResonanceV2Config()
        self.assertEqual(config.n_hmm_states, 3)
        self.assertEqual(config.slow_cycle, 60)
        self.assertEqual(config.fast_cycle, 10)
        self.assertEqual(config.train_window, 504)
        self.assertAlmostEqual(config.trend_weight, 0.4)
    
    def test_position_cap(self):
        """测试仓位上限映射"""
        from core.resonance_v2.config import ResonanceV2Config, MarketState
        
        config = ResonanceV2Config()
        
        self.assertEqual(config.get_position_cap(MarketState.RISK_ON), 1.0)
        self.assertEqual(config.get_position_cap(MarketState.RISK_OFF), 0.3)
        self.assertEqual(config.get_position_cap(MarketState.SIDEWAYS), 0.6)
    
    def test_resonance_level(self):
        """测试共振级别判定"""
        from core.resonance_v2.config import ResonanceV2Config
        
        config = ResonanceV2Config()
        
        self.assertEqual(config.get_resonance_level(85), "full")
        self.assertEqual(config.get_resonance_level(70), "add")
        self.assertEqual(config.get_resonance_level(50), "trial")
        self.assertEqual(config.get_resonance_level(20), "none")


class TestFeatureLayer(unittest.TestCase):
    """测试特征层"""
    
    def setUp(self):
        """准备测试数据"""
        # 创建模拟数据
        np.random.seed(42)
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        self.mock_df = pd.DataFrame({
            'date': dates,
            'open': 100 + np.cumsum(np.random.randn(100) * 0.5),
            'high': 100 + np.cumsum(np.random.randn(100) * 0.5) + 1,
            'low': 100 + np.cumsum(np.random.randn(100) * 0.5) - 1,
            'close': 100 + np.cumsum(np.random.randn(100) * 0.5),
            'volume': np.random.randint(1000000, 10000000, 100),
            'money': np.random.randint(100000000, 1000000000, 100),
        })
        
        from core.resonance_v2.data_layer import MarketData
        self.mock_market_data = MarketData(
            code="TEST",
            name="Test Index",
            data=self.mock_df,
            start_date="2024-01-01",
            end_date="2024-04-10"
        )
    
    def test_hmm_observations(self):
        """测试HMM观测变量提取"""
        from core.resonance_v2.feature_layer import MultiCycleFeatureExtractor
        
        extractor = MultiCycleFeatureExtractor()
        obs = extractor.extract_hmm_observations(self.mock_market_data)
        
        self.assertGreater(obs.n_samples, 0)
        self.assertEqual(obs.n_features, 4)  # log_return, volatility, trend_strength, turnover_ratio
        self.assertEqual(len(obs.feature_names), 4)
    
    def test_multi_cycle_features(self):
        """测试多周期特征提取"""
        from core.resonance_v2.feature_layer import MultiCycleFeatureExtractor
        
        extractor = MultiCycleFeatureExtractor()
        features = extractor.extract_multi_cycle_features(self.mock_market_data)
        
        self.assertEqual(len(features.slow_ma_trend), 100)
        self.assertEqual(len(features.fast_momentum), 100)
        self.assertEqual(len(features.slow_adx), 100)
    
    def test_resonance_score(self):
        """测试共振评分计算"""
        from core.resonance_v2.feature_layer import MultiCycleFeatureExtractor
        
        extractor = MultiCycleFeatureExtractor()
        features = extractor.extract_multi_cycle_features(self.mock_market_data)
        score = extractor.calculate_resonance_score(features)
        
        self.assertGreaterEqual(score.total_score, 0)
        self.assertLessEqual(score.total_score, 100)
        self.assertIn(score.level, ['full', 'add', 'trial', 'none'])


class TestHMMStateLayer(unittest.TestCase):
    """测试HMM状态层"""
    
    def setUp(self):
        """准备测试数据"""
        np.random.seed(42)
        n_samples = 300
        
        # 创建模拟观测变量
        self.mock_observations = np.column_stack([
            np.random.randn(n_samples) * 0.02,  # log_return
            np.random.rand(n_samples) * 0.3,     # volatility
            np.random.randn(n_samples) * 0.01,  # trend
            np.random.rand(n_samples) * 0.5 + 0.5,  # turnover
        ])
        
        from core.resonance_v2.feature_layer import HMMObservations
        self.hmm_obs = HMMObservations(
            data=self.mock_observations,
            feature_names=['log_return', 'volatility', 'trend_strength', 'turnover_ratio'],
            dates=[f"2024-{i//30+1:02d}-{i%30+1:02d}" for i in range(n_samples)]
        )
    
    def test_hmm_initialization(self):
        """测试HMM初始化"""
        from core.resonance_v2.hmm_state_layer import MarketStateHMM
        
        hmm = MarketStateHMM()
        self.assertEqual(hmm.n_states, 3)
        self.assertFalse(hmm.is_fitted)
    
    def test_hmm_fit(self):
        """测试HMM训练"""
        from core.resonance_v2.hmm_state_layer import MarketStateHMM
        
        hmm = MarketStateHMM()
        success = hmm.fit(self.hmm_obs)
        
        self.assertTrue(success)
        self.assertTrue(hmm.is_fitted)
        self.assertEqual(len(hmm.state_interpretations), 3)
    
    def test_hmm_predict(self):
        """测试HMM预测"""
        from core.resonance_v2.hmm_state_layer import MarketStateHMM
        
        hmm = MarketStateHMM()
        hmm.fit(self.hmm_obs)
        
        prediction = hmm.predict(self.hmm_obs)
        
        self.assertIsNotNone(prediction)
        self.assertIn(prediction.current_state, [0, 1, 2])
        self.assertEqual(len(prediction.state_probabilities), 3)
        self.assertAlmostEqual(sum(prediction.state_probabilities), 1.0, places=5)
    
    def test_hmm_state_summary(self):
        """测试状态摘要"""
        from core.resonance_v2.hmm_state_layer import MarketStateHMM
        
        hmm = MarketStateHMM()
        hmm.fit(self.hmm_obs)
        
        summary = hmm.get_state_summary()
        self.assertFalse(summary.empty)
        self.assertEqual(len(summary), 3)


class TestStrategyLayer(unittest.TestCase):
    """测试策略层"""
    
    def test_signal_generation(self):
        """测试信号生成"""
        from core.resonance_v2.strategy_layer import ResonanceStrategy, SignalType
        from core.resonance_v2.feature_layer import ResonanceScore
        from core.resonance_v2.hmm_state_layer import HMMPrediction
        from core.resonance_v2.config import MarketState
        
        strategy = ResonanceStrategy()
        
        # 创建模拟输入
        resonance = ResonanceScore(
            total_score=75.0,
            trend_score=80.0,
            vol_score=70.0,
            risk_score=75.0,
            trend_sync=True,
            vol_sync=True,
            risk_sync=True,
            level='add'
        )
        
        hmm_pred = HMMPrediction(
            current_state=0,
            state_name='risk_on',
            market_state=MarketState.RISK_ON,
            state_probabilities=np.array([0.7, 0.2, 0.1]),
            confidence=0.7,
            state_sequence=[0],
            regime_change=False,
            prev_state=None
        )
        
        signal = strategy.generate_signal(resonance, hmm_pred, 100.0, atr=2.0)
        
        self.assertIn(signal.signal_type, [SignalType.STRONG_BUY, SignalType.BUY, SignalType.HOLD])
        self.assertGreaterEqual(signal.target_position, 0)
        self.assertLessEqual(signal.target_position, 1)
        self.assertLess(signal.stop_loss, 100.0)
    
    def test_exit_conditions(self):
        """测试退出条件"""
        from core.resonance_v2.strategy_layer import ResonanceStrategy, Position, ExitReason
        from core.resonance_v2.config import MarketState
        
        strategy = ResonanceStrategy()
        
        # 创建持仓
        position = Position(
            code="TEST",
            entry_price=100.0,
            entry_date="2024-01-01",
            quantity=1000,
            current_price=90.0,
            stop_loss_price=92.0,  # 止损价
            take_profit_price=130.0,
            highest_price=100.0,
            entry_state=MarketState.RISK_ON
        )
        
        # 测试止损触发
        exit_signal, reason = strategy.check_position_exits(
            position, 91.0, MarketState.RISK_ON
        )
        
        self.assertTrue(exit_signal)
        self.assertEqual(reason, ExitReason.HARD_STOP)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_analyzer_initialization(self):
        """测试分析器初始化"""
        from core.resonance_v2 import ResonanceHMMAnalyzer
        
        analyzer = ResonanceHMMAnalyzer()
        self.assertIsNotNone(analyzer)
        self.assertEqual(analyzer.config.n_hmm_states, 3)
    
    def test_result_dataclass(self):
        """测试结果数据类"""
        from core.resonance_v2 import ResonanceResult, SignalType, MarketState
        
        result = ResonanceResult(
            index_code="000300.XSHG",
            analysis_date="2024-01-15",
            market_state=MarketState.RISK_ON,
            state_name="risk_on",
            state_confidence=0.8,
            state_probabilities={"risk_on": 0.8, "sideways": 0.15, "risk_off": 0.05},
            regime_change=False,
            resonance_score=75.0,
            resonance_level="add",
            trend_sync=True,
            vol_sync=True,
            risk_sync=True,
            signal_type=SignalType.BUY,
            target_position=0.7,
            stop_loss_price=95.0
        )
        
        # 测试to_dict
        d = result.to_dict()
        self.assertEqual(d['index_code'], "000300.XSHG")
        self.assertEqual(d['market_state'], "risk_on")
        
        # 测试summary
        summary = result.summary()
        self.assertIn("000300.XSHG", summary)
        self.assertIn("risk_on", summary)


class TestLiveData(unittest.TestCase):
    """实际数据测试（需要JQData连接）"""
    
    @unittest.skipIf(True, "Skip live data test by default")
    def test_live_analysis(self):
        """测试实际数据分析"""
        from core.resonance_v2 import ResonanceHMMAnalyzer
        
        analyzer = ResonanceHMMAnalyzer()
        result = analyzer.analyze("000300.XSHG", "2024-12-31")
        
        self.assertIsNotNone(result)
        self.assertGreater(result.state_confidence, 0)


def run_quick_test():
    """快速测试运行"""
    print("=" * 60)
    print("Resonance V2 Quick Unit Tests")
    print("=" * 60)
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestFeatureLayer))
    suite.addTests(loader.loadTestsFromTestCase(TestHMMStateLayer))
    suite.addTests(loader.loadTestsFromTestCase(TestStrategyLayer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出总结
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_quick_test()
    sys.exit(0 if success else 1)
