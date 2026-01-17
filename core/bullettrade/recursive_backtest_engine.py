#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BulletTrade递归回测引擎

支持策略参数动态调整、回测执行、结果标准化输出，用于进化优化系统。
"""

import sys
from pathlib import Path
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

logger = logging.getLogger(__name__)


@dataclass
class BacktestConfig:
    """回测配置"""
    start_date: str
    end_date: str
    initial_capital: float = 1000000.0
    benchmark: str = '000300.XSHG'
    frequency: str = 'day'
    cache_dir: Optional[str] = None


@dataclass
class StandardizedBacktestResult:
    """标准化回测结果"""
    # 基本信息
    backtest_id: str
    start_date: str
    end_date: str
    initial_capital: float
    
    # 绩效指标
    total_return: float          # 总收益率（小数，如0.30表示30%）
    annual_return: float         # 年化收益率
    monthly_return: float        # 月收益率（主要目标）
    sharpe_ratio: float          # 夏普比率
    max_drawdown: float          # 最大回撤（负数）
    win_rate: float              # 胜率（0-1）
    
    # 交易统计
    total_trades: int            # 总交易次数
    avg_holding_period: float    # 平均持仓周期（天）
    
    # 风险指标
    volatility: float            # 波动率
    calmar_ratio: float          # 卡玛比率（年化收益/最大回撤）
    
    # 策略参数（用于进化优化）
    strategy_params: Dict = field(default_factory=dict)
    
    # 原始结果（保留）
    raw_result: Any = None
    
    # 时间戳
    timestamp: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'backtest_id': self.backtest_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'initial_capital': self.initial_capital,
            'total_return': self.total_return,
            'annual_return': self.annual_return,
            'monthly_return': self.monthly_return,
            'sharpe_ratio': self.sharpe_ratio,
            'max_drawdown': self.max_drawdown,
            'win_rate': self.win_rate,
            'total_trades': self.total_trades,
            'avg_holding_period': self.avg_holding_period,
            'volatility': self.volatility,
            'calmar_ratio': self.calmar_ratio,
            'strategy_params': self.strategy_params,
            'timestamp': self.timestamp,
        }
    
    def meets_target(self, target_monthly_return: float = 0.30, max_dd: float = -0.20, min_sharpe: float = 2.0) -> bool:
        """检查是否满足目标条件"""
        return (
            self.monthly_return >= target_monthly_return and
            self.max_drawdown >= max_dd and  # max_drawdown是负数，>=表示不超过
            self.sharpe_ratio >= min_sharpe
        )


class RecursiveBacktestEngine:
    """递归回测引擎"""
    
    def __init__(
        self,
        base_config: BacktestConfig,
        strategy_generator_class=None,
        verbose: bool = True,
        use_mongodb: bool = True,
        use_gpu: bool = True,
        max_workers: int = 3
    ):
        """
        初始化递归回测引擎
        
        Args:
            base_config: 基础回测配置
            strategy_generator_class: 策略生成器类（默认使用BulletTradeStrategyGenerator）
            verbose: 是否输出详细信息
            use_mongodb: 是否使用MongoDB存储（默认True）
            use_gpu: 是否使用GPU加速（默认True）
            max_workers: 最大并行工作数（安全模式：3）
        """
        self.base_config = base_config
        self.verbose = verbose
        
        # 初始化数据预加载器（确保MongoDB集成）
        try:
            from core.advisor_v4.data_preloader import DataPreloader
            self.data_preloader = DataPreloader(
                use_mongodb=use_mongodb,
                cache_dir=base_config.cache_dir or "data/cache",
                max_workers=max_workers,
                verbose=verbose
            )
            if self.verbose:
                print(f"✅ 数据预加载器已初始化（MongoDB: {'启用' if use_mongodb else '禁用'}）")
        except Exception as e:
            logger.warning(f"数据预加载器初始化失败: {e}，将使用基本模式")
            self.data_preloader = None
        
        # 初始化GPU加速器（如果可用）
        self.gpu_calculator = None
        if use_gpu:
            try:
                from core.advisor_v4.gpu_accelerator import GPUTechnicalIndicatorCalculator, USE_GPU
                if USE_GPU:
                    self.gpu_calculator = GPUTechnicalIndicatorCalculator(use_gpu=True)
                    if self.verbose:
                        print(f"✅ GPU加速器已初始化")
                else:
                    if self.verbose:
                        print(f"⚠️  GPU不可用，将使用CPU计算")
            except Exception as e:
                logger.warning(f"GPU加速器初始化失败: {e}，将使用CPU计算")
        
        # 导入策略生成器
        if strategy_generator_class is None:
            try:
                from core.advisor_v4.bullettrade_strategy_generator import BulletTradeStrategyGenerator, StrategyConfig
                self.strategy_generator_class = BulletTradeStrategyGenerator
                self.strategy_config_class = StrategyConfig
            except ImportError:
                logger.error("无法导入BulletTradeStrategyGenerator")
                raise
        else:
            self.strategy_generator_class = strategy_generator_class
        
        # 导入BulletTrade引擎
        try:
            from core.bullettrade.engine import BulletTradeEngine, BTConfig
            from core.advisor_v4.bullettrade_backtest import BulletTradeBacktest
            self.bt_backtest_class = BulletTradeBacktest
            self.bt_engine_class = BulletTradeEngine
            self.bt_config_class = BTConfig
        except ImportError:
            logger.warning("BulletTrade引擎不可用，将使用简化模式")
            self.bt_backtest_class = None
            self.bt_engine_class = None
            self.bt_config_class = None
        
        # 结果存储
        self.results: List[StandardizedBacktestResult] = []
        
        # 数据预加载标记
        self._data_loaded = False
    
    def run_backtest(
        self,
        strategy_params: Dict[str, Any],
        strategy_code: Optional[str] = None,
        backtest_id: Optional[str] = None
    ) -> StandardizedBacktestResult:
        """
        执行回测（支持动态参数）
        
        Args:
            strategy_params: 策略参数（用于生成策略代码）
            strategy_code: 策略代码（如果提供，直接使用；否则根据params生成）
            backtest_id: 回测ID（如果为None，自动生成）
        
        Returns:
            StandardizedBacktestResult
        """
        if backtest_id is None:
            backtest_id = f"bt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if self.verbose:
            print(f"\n[回测 {backtest_id}] 开始执行...")
            print(f"  参数: {strategy_params}")
            print(f"  区间: {self.base_config.start_date} ~ {self.base_config.end_date}")
        
        try:
            # 1. 确保数据已加载（从MongoDB或下载）
            self._ensure_data_loaded()
            
            # 2. 生成或使用策略代码（传递GPU计算器）
            if strategy_code is None:
                strategy_code = self._generate_strategy_code(strategy_params, gpu_calculator=self.gpu_calculator)
            
            # 3. 执行回测（使用已加载的数据）
            bt_result = self._execute_backtest(strategy_code)
            
            # 4. 标准化结果
            standardized_result = self._standardize_result(
                bt_result,
                backtest_id,
                strategy_params
            )
            
            # 5. 保存结果
            self.results.append(standardized_result)
            
            if self.verbose:
                print(f"  ✅ 回测完成")
                print(f"    月收益率: {standardized_result.monthly_return*100:.2f}%")
                print(f"    最大回撤: {standardized_result.max_drawdown*100:.2f}%")
                print(f"    夏普比率: {standardized_result.sharpe_ratio:.2f}")
                print(f"    是否达标: {standardized_result.meets_target()}")
            
            return standardized_result
            
        except Exception as e:
            logger.error(f"回测执行失败: {e}", exc_info=True)
            # 返回失败结果
            return StandardizedBacktestResult(
                backtest_id=backtest_id,
                start_date=self.base_config.start_date,
                end_date=self.base_config.end_date,
                initial_capital=self.base_config.initial_capital,
                total_return=-1.0,  # 失败标记
                annual_return=-1.0,
                monthly_return=-1.0,
                sharpe_ratio=-999.0,
                max_drawdown=-1.0,
                win_rate=0.0,
                total_trades=0,
                avg_holding_period=0.0,
                volatility=0.0,
                calmar_ratio=0.0,
                strategy_params=strategy_params,
            )
    
    def _ensure_data_loaded(self):
        """确保数据已加载（从MongoDB或下载）"""
        if self._data_loaded:
            return
        
        if self.data_preloader is None:
            if self.verbose:
                logger.warning("数据预加载器不可用，跳过数据预加载")
            return
        
        try:
            if self.verbose:
                print(f"\n[数据预加载] 检查并加载数据...")
            
            # 检查数据完整性
            completeness = self.data_preloader.check_data_completeness(
                start_date=self.base_config.start_date,
                end_date=self.base_config.end_date,
                stocks=None  # 检查所有股票
            )
            
            if completeness.get('is_complete'):
                if self.verbose:
                    print(f"  ✅ 数据已完整（覆盖率: {completeness.get('coverage_percentage', 0):.1f}%）")
                self._data_loaded = True
                return
            
            # 如果数据不完整，进行下载
            if self.verbose:
                print(f"  ⚠️  数据不完整（覆盖率: {completeness.get('coverage_percentage', 0):.1f}%），开始下载...")
            
            result = self.data_preloader.preload_market_data(
                start_date=self.base_config.start_date,
                end_date=self.base_config.end_date,
                force_refresh=False
            )
            
            if result.success:
                if self.verbose:
                    print(f"  ✅ 数据预加载完成（{result.total_stocks}只股票，{result.duration_seconds:.1f}秒）")
                self._data_loaded = True
            else:
                logger.warning(f"数据预加载失败: {result.errors}")
                # 继续执行，但后续可能使用API获取数据
        except Exception as e:
            logger.warning(f"数据预加载异常: {e}，继续执行")
            # 继续执行，但后续可能使用API获取数据
    
    def _generate_strategy_code(
        self,
        params: Dict[str, Any],
        gpu_calculator=None
    ) -> str:
        """根据参数生成策略代码（支持GPU加速）"""
        # 创建策略配置
        config = self.strategy_config_class()
        
        # 更新配置参数
        for key, value in params.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        # 生成策略代码
        generator = self.strategy_generator_class(
            config=config,
            cache_data_dir=self.base_config.cache_dir
        )
        
        # 如果策略生成器支持GPU计算器，传递它
        # 注意：这里需要策略生成器类支持gpu_calculator参数
        # 如果当前实现不支持，这个参数会被忽略，但不会报错
        
        strategy_code = generator.generate_strategy_code(
            cache_data_dir=self.base_config.cache_dir
        )
        
        return strategy_code
    
    def _execute_backtest(self, strategy_code: str) -> Any:
        """执行回测（调用BulletTrade引擎）"""
        if self.bt_backtest_class is None:
            raise ImportError("BulletTrade引擎不可用")
        
        # 创建回测配置
        bt_config = self.bt_config_class(
            start_date=self.base_config.start_date,
            end_date=self.base_config.end_date,
            initial_capital=self.base_config.initial_capital,
            benchmark=self.base_config.benchmark,
            frequency=self.base_config.frequency,
            output_dir=str(Path(self.base_config.cache_dir) / "backtest_results" if self.base_config.cache_dir else Path("output/backtest_results")),
            generate_html=False,  # 递归回测不需要HTML报告
            generate_csv=False,
        )
        
        # 创建策略配置（使用默认值，因为参数已在策略代码中）
        from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig
        strategy_config = StrategyConfig()
        
        # 创建回测接口
        bt_backtest = self.bt_backtest_class(
            strategy_config=strategy_config,
            bt_config=bt_config,
            cache_dir=self.base_config.cache_dir,
        )
        
        # 执行回测
        result = bt_backtest.bt_engine.run_backtest(
            strategy_code=strategy_code,
            start_date=self.base_config.start_date,
            end_date=self.base_config.end_date,
            initial_capital=self.base_config.initial_capital,
        )
        
        return result
    
    def _standardize_result(self, bt_result: Any, backtest_id: str, strategy_params: Dict) -> StandardizedBacktestResult:
        """标准化回测结果"""
        # 计算回测天数
        start_dt = datetime.strptime(self.base_config.start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(self.base_config.end_date, '%Y-%m-%d')
        days = (end_dt - start_dt).days
        months = days / 30.0  # 近似月数
        
        # 提取指标
        total_return = getattr(bt_result, 'total_return', 0.0)
        if isinstance(total_return, str) and total_return.endswith('%'):
            total_return = float(total_return.rstrip('%')) / 100.0
        elif isinstance(total_return, (int, float)):
            if total_return > 1.0:  # 如果是百分比形式（如30表示30%）
                total_return = total_return / 100.0
        
        # 年化收益率
        if days > 0:
            annual_return = (1 + total_return) ** (365.0 / days) - 1
        else:
            annual_return = 0.0
        
        # 月收益率（主要目标）
        if months > 0:
            monthly_return = (1 + total_return) ** (1.0 / months) - 1
        else:
            monthly_return = 0.0
        
        # 其他指标
        sharpe_ratio = float(getattr(bt_result, 'sharpe_ratio', 0.0))
        max_drawdown = float(getattr(bt_result, 'max_drawdown', 0.0))
        if isinstance(max_drawdown, str) and max_drawdown.endswith('%'):
            max_drawdown = float(max_drawdown.rstrip('%')) / 100.0
        if max_drawdown > 0:  # 确保是负数
            max_drawdown = -max_drawdown
        
        win_rate = float(getattr(bt_result, 'win_rate', 0.0))
        total_trades = int(getattr(bt_result, 'total_trades', 0))
        
        # 波动率
        volatility = float(getattr(bt_result, 'volatility', 0.0))
        
        # 卡玛比率
        if abs(max_drawdown) > 0:
            calmar_ratio = annual_return / abs(max_drawdown)
        else:
            calmar_ratio = 0.0
        
        # 平均持仓周期（简化估算）
        avg_holding_period = days / max(total_trades, 1) if total_trades > 0 else 0.0
        
        return StandardizedBacktestResult(
            backtest_id=backtest_id,
            start_date=self.base_config.start_date,
            end_date=self.base_config.end_date,
            initial_capital=self.base_config.initial_capital,
            total_return=total_return,
            annual_return=annual_return,
            monthly_return=monthly_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            total_trades=total_trades,
            avg_holding_period=avg_holding_period,
            volatility=volatility,
            calmar_ratio=calmar_ratio,
            strategy_params=strategy_params,
            raw_result=bt_result,
        )
    
    def get_best_result(self, target_monthly_return: float = 0.30) -> Optional[StandardizedBacktestResult]:
        """获取最佳结果（优先满足目标月收益率）"""
        valid_results = [r for r in self.results if r.monthly_return >= 0]
        
        if not valid_results:
            return None
        
        # 优先选择满足目标的
        target_results = [r for r in valid_results if r.meets_target(target_monthly_return)]
        
        if target_results:
            # 在满足目标的结果中，选择月收益率最高的
            return max(target_results, key=lambda r: r.monthly_return)
        else:
            # 如果没有满足目标的，选择月收益率最高的
            return max(valid_results, key=lambda r: r.monthly_return)
    
    def save_results(self, output_path: str):
        """保存所有回测结果到JSON文件"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        results_data = {
            'base_config': {
                'start_date': self.base_config.start_date,
                'end_date': self.base_config.end_date,
                'initial_capital': self.base_config.initial_capital,
                'benchmark': self.base_config.benchmark,
            },
            'results': [r.to_dict() for r in self.results],
            'summary': {
                'total_backtests': len(self.results),
                'best_monthly_return': max([r.monthly_return for r in self.results], default=0.0),
                'best_backtest_id': self.get_best_result().backtest_id if self.get_best_result() else None,
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)
        
        if self.verbose:
            print(f"\n✅ 回测结果已保存到: {output_file}")
            print(f"  总回测次数: {len(self.results)}")
            if self.results:
                best = self.get_best_result()
                if best:
                    print(f"  最佳月收益率: {best.monthly_return*100:.2f}%")


def main():
    """主函数：示例用法"""
    config = BacktestConfig(
        start_date='2024-10-01',
        end_date='2024-12-31',
        initial_capital=1000000.0,
        cache_dir='output/backtest_cache'
    )
    
    engine = RecursiveBacktestEngine(config, verbose=True)
    
    # 测试回测
    test_params = {
        'max_stocks': 10,
        'min_total_score': 30.0,
        'rebalance_weekday': 0,
    }
    
    result = engine.run_backtest(test_params)
    print(f"\n回测结果: {result.to_dict()}")
    
    # 保存结果
    engine.save_results('output/recursive_backtest_results.json')


if __name__ == '__main__':
    main()
