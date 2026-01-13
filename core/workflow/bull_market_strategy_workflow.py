#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市策略完整工作流编排器

整合所有阶段，形成端到端的自动化工作流：
1. 检测市场状态（牛市？）
2. 如果牛市 → 提取牛市高回报案例
3. 生成混合策略（7因子 + 牛市模式）
4. BulletTrade回测
5. 评估结果（月回报率是否≥30%？）
6. 如果未达标 → 递归进化优化
7. 返回最优策略
8. 存入知识库（策略+结果+经验）
"""

import sys
from pathlib import Path
from typing import Dict, Optional, Any, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

logger = logging.getLogger(__name__)


@dataclass
class WorkflowConfig:
    """工作流配置"""
    # 数据挖掘 - 历史牛市时间段（用于数据挖掘）
    historical_bull_market_periods: List[tuple] = field(default_factory=lambda: [
        # 第三次牛市（股权分置改革牛）：2005年中 - 2007年10月
        ("2005-07-01", "2007-10-31"),
        # 第四次牛市（杠杆牛）：2014年中 - 2015年6月
        ("2014-07-01", "2015-06-30"),
        # 第五次牛市（结构性牛/核心资产牛）：2019年初 - 2021年初
        ("2019-01-01", "2021-03-31"),
    ])
    
    # 数据挖掘配置
    mining_start_date: str = '2005-07-01'   # 数据挖掘开始日期（最早的历史牛市）
    mining_end_date: str = '2021-03-31'     # 数据挖掘结束日期（最新的历史牛市）
    min_return_pct: float = 10.0
    min_bull_score: float = 60.0
    
    # 回测
    backtest_start_date: str = '2024-10-01'
    backtest_end_date: str = '2024-12-31'
    initial_capital: float = 1000000.0
    
    # 进化
    evolution_population_size: int = 50
    evolution_generations: int = 10
    target_monthly_return: float = 0.30
    max_drawdown_limit: float = -0.20
    min_sharpe_ratio: float = 2.0
    
    # 数据相关
    use_mongodb: bool = True                 # 是否使用MongoDB存储
    force_refresh_data: bool = False         # 是否强制刷新数据
    
    # 并行相关
    use_parallel_backtest: bool = True       # 是否使用并行回测
    max_parallel_workers: int = 3            # 最大并行工作数（安全模式：3）
    
    # GPU相关
    use_gpu_acceleration: bool = True        # 是否使用GPU加速
    gpu_batch_size: int = 100                # GPU批处理大小
    
    # 输出
    output_dir: str = 'output/bull_market_strategy'
    cache_dir: Optional[str] = None


@dataclass
class WorkflowResult:
    """工作流执行结果"""
    workflow_id: str
    start_time: str
    end_time: str
    
    # 各阶段结果
    market_detection: Optional[Dict] = None
    data_mining: Optional[Dict] = None
    pattern_extraction: Optional[Dict] = None
    strategy_generation: Optional[Dict] = None
    backtest_results: List[Dict] = field(default_factory=list)
    evolution_results: Optional[Dict] = None
    
    # 最终结果
    best_strategy_params: Optional[Dict] = None
    best_backtest_result: Optional[Dict] = None
    reached_target: bool = False
    
    # 错误信息
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'workflow_id': self.workflow_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'market_detection': self.market_detection,
            'data_mining': self.data_mining,
            'pattern_extraction': self.pattern_extraction,
            'strategy_generation': self.strategy_generation,
            'backtest_results_count': len(self.backtest_results),
            'evolution_results': self.evolution_results,
            'best_strategy_params': self.best_strategy_params,
            'best_backtest_result': self.best_backtest_result,
            'reached_target': self.reached_target,
            'errors': self.errors,
        }


class BullMarketStrategyWorkflow:
    """牛市策略完整工作流编排器"""
    
    def __init__(self, config: Optional[WorkflowConfig] = None, verbose: bool = True):
        """
        初始化工作流
        
        Args:
            config: 工作流配置
            verbose: 是否输出详细信息
        """
        self.config = config or WorkflowConfig()
        self.verbose = verbose
        
        # 创建输出目录
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def execute(
        self,
        workflow_id: Optional[str] = None,
        skip_mining: bool = False,
        skip_evolution: bool = False
    ) -> WorkflowResult:
        """
        执行完整工作流
        
        Args:
            workflow_id: 工作流ID（如果为None，自动生成）
            skip_mining: 是否跳过数据挖掘（使用已有数据）
            skip_evolution: 是否跳过进化优化（只执行一次回测）
        
        Returns:
            WorkflowResult
        """
        if workflow_id is None:
            workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        result = WorkflowResult(
            workflow_id=workflow_id,
            start_time=start_time,
            end_time='',
        )
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"开始执行牛市策略工作流: {workflow_id}")
            print(f"{'='*70}")
        
        try:
            # ========== 阶段1: 检测市场状态 ==========
            if self.verbose:
                print(f"\n[阶段1] 检测市场状态...")
            
            market_result = self._detect_market_state()
            result.market_detection = market_result
            
            if not market_result.get('is_bull', False):
                result.errors.append("市场状态非牛市，工作流终止")
                if self.verbose:
                    print(f"  ⚠️ 市场状态: {market_result.get('strength_level', 'NON_BULL')}, 非牛市")
                    print(f"  工作流终止")
                result.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return result
            
            bull_strength = market_result.get('strength_score', 0.0)
            if self.verbose:
                print(f"  ✅ 牛市状态: {market_result.get('strength_level', 'UNKNOWN')}, 强度: {bull_strength:.1f}/100")
            
            # ========== 阶段2: 数据挖掘（可选） ==========
            if not skip_mining:
                if self.verbose:
                    print(f"\n[阶段2] 挖掘牛市高回报案例...")
                
                mining_result = self._mine_high_return_cases()
                result.data_mining = mining_result
                
                if mining_result.get('case_count', 0) > 0:
                    if self.verbose:
                        print(f"  ✅ 找到 {mining_result['case_count']} 个高回报案例")
                else:
                    result.errors.append("未找到足够的高回报案例")
                    if self.verbose:
                        print(f"  ⚠️ 未找到高回报案例，继续使用已有模式")
            else:
                if self.verbose:
                    print(f"\n[阶段2] 跳过数据挖掘（使用已有数据）")
            
            # ========== 阶段3: 模式提取（可选） ==========
            if not skip_mining:
                if self.verbose:
                    print(f"\n[阶段3] 提取牛市专属模式...")
                
                pattern_result = self._extract_patterns()
                result.pattern_extraction = pattern_result
                
                if pattern_result.get('pattern_count', 0) > 0:
                    if self.verbose:
                        print(f"  ✅ 提取 {pattern_result['pattern_count']} 个模式")
                else:
                    if self.verbose:
                        print(f"  ⚠️ 未提取到模式，使用默认模式")
            else:
                if self.verbose:
                    print(f"\n[阶段3] 跳过模式提取（使用已有模式）")
            
            # ========== 阶段4: 生成策略 ==========
            if self.verbose:
                print(f"\n[阶段4] 生成混合策略（根据牛市强度）...")
            
            strategy_result = self._generate_strategy(bull_strength)
            result.strategy_generation = strategy_result
            
            if self.verbose:
                print(f"  策略模式: {strategy_result.get('strategy_mode', 'UNKNOWN')}")
            
            # ========== 阶段5: 执行回测 ==========
            if self.verbose:
                print(f"\n[阶段5] 执行BulletTrade回测...")
            
            # 根据配置选择并行或串行回测
            if self.config.use_parallel_backtest:
                initial_backtest_result = self._run_parallel_initial_backtest(strategy_result)
            else:
                initial_backtest_result = self._run_initial_backtest(strategy_result)
            
            result.backtest_results.append(initial_backtest_result)
            
            if initial_backtest_result.get('monthly_return', 0) >= self.config.target_monthly_return:
                # 已达到目标，不需要进化
                if self.verbose:
                    print(f"  ✅ 初始回测已达到目标！月收益率: {initial_backtest_result['monthly_return']*100:.2f}%")
                result.reached_target = True
                result.best_strategy_params = strategy_result.get('params', {})
                result.best_backtest_result = initial_backtest_result
                result.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return result
            
            # ========== 阶段6: 递归进化优化（可选） ==========
            if not skip_evolution:
                if self.verbose:
                    print(f"\n[阶段6] 开始递归进化优化...")
                    print(f"  目标: 月回报率 {self.config.target_monthly_return*100:.0f}%")
                
                evolution_result = self._run_evolution()
                result.evolution_results = evolution_result
                
                if evolution_result.get('reached_target', False):
                    if self.verbose:
                        print(f"  ✅ 进化后达到目标！")
                    result.reached_target = True
                    result.best_strategy_params = evolution_result.get('best_params', {})
                    result.best_backtest_result = evolution_result.get('best_result', {})
                else:
                    if self.verbose:
                        print(f"  ⚠️ 进化后仍未达到目标")
                        best = evolution_result.get('best_result', {})
                        if best:
                            print(f"  最佳月收益率: {best.get('monthly_return', 0)*100:.2f}%")
                    result.best_strategy_params = evolution_result.get('best_params', {})
                    result.best_backtest_result = evolution_result.get('best_result', {})
            else:
                if self.verbose:
                    print(f"\n[阶段6] 跳过进化优化")
                result.best_strategy_params = strategy_result.get('params', {})
                result.best_backtest_result = initial_backtest_result
            
            # ========== 阶段7: 存入知识库 ==========
            if self.verbose:
                print(f"\n[阶段7] 存入知识库...")
            
            kb_result = self._save_to_knowledge_base(result)
            
            if self.verbose:
                print(f"  ✅ 知识库保存完成")
            
        except Exception as e:
            error_msg = f"工作流执行失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            result.errors.append(error_msg)
        
        finally:
            result.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 保存工作流结果
            self._save_workflow_result(result)
        
        return result
    
    def _detect_market_state(self) -> Dict[str, Any]:
        """阶段1: 检测市场状态"""
        try:
            from core.market_regime.bull_market_detector import BullMarketDetector
            from core.market_regime.bull_market_signal_aggregator import BullMarketSignalAggregator
            
            # 使用信号聚合器（更准确）
            aggregator = BullMarketSignalAggregator(verbose=False)
            signal = aggregator.aggregate()
            
            return {
                'is_bull': signal.bull_probability >= 30.0,
                'bull_probability': signal.bull_probability,
                'strength_level': signal.strength_level,
                'strength_score': signal.strength_score,
                'confidence': signal.confidence,
                'position_suggestion': signal.position_suggestion,
                'strategy_suggestion': signal.strategy_suggestion,
            }
        except Exception as e:
            logger.error(f"市场状态检测失败: {e}")
            return {'is_bull': False, 'error': str(e)}
    
    def _mine_high_return_cases(self) -> Dict[str, Any]:
        """阶段2: 挖掘历史牛市高回报案例（多个时间段）"""
        try:
            from core.data_mining.bull_market_high_return_miner import BullMarketHighReturnMiner
            from core.advisor_v4.data_preloader import DataPreloader
            
            miner = BullMarketHighReturnMiner(
                min_return_pct=self.config.min_return_pct,
                verbose=self.verbose
            )
            
            all_cases = []
            
            # 初始化数据预加载器
            if self.config.cache_dir is None:
                cache_dir = str(self.output_dir / 'cache')
            else:
                cache_dir = self.config.cache_dir
            
            preloader = DataPreloader(
                use_mongodb=self.config.use_mongodb,
                cache_dir=cache_dir,
                max_workers=self.config.max_parallel_workers,
                verbose=self.verbose
            )
            
            # 遍历所有历史牛市时间段
            for period_start, period_end in self.config.historical_bull_market_periods:
                if self.verbose:
                    print(f"  挖掘时间段: {period_start} ~ {period_end}")
                
                # 预加载该时间段的数据
                self._preload_data_for_period(preloader, period_start, period_end)
                
                # 挖掘该时间段的高回报案例
                try:
                    cases = miner.mine_high_return_cases(
                        start_date=period_start,
                        end_date=period_end,
                        min_bull_score=self.config.min_bull_score
                    )
                    
                    all_cases.extend(cases)
                    
                    if self.verbose:
                        print(f"    ✅ 找到 {len(cases)} 个高回报案例（累计: {len(all_cases)}）")
                except Exception as e:
                    logger.warning(f"时间段 {period_start} ~ {period_end} 挖掘失败: {e}")
                    if self.verbose:
                        print(f"    ⚠️  时间段挖掘失败: {e}")
            
            # 保存合并后的所有案例
            csv_path = str(self.output_dir / 'bull_market_high_return_cases.csv')
            if all_cases:
                miner.save_to_csv(all_cases, csv_path)
                if self.verbose:
                    print(f"  ✅ 所有案例已保存到: {csv_path}")
            
            return {
                'case_count': len(all_cases),
                'csv_path': csv_path,
                'periods_processed': len(self.config.historical_bull_market_periods),
                'avg_return': sum([c.return_pct for c in all_cases]) / len(all_cases) if all_cases else 0.0,
            }
        except Exception as e:
            logger.error(f"数据挖掘失败: {e}")
            return {'case_count': 0, 'error': str(e)}
    
    def _preload_data_for_period(self, preloader, start_date: str, end_date: str):
        """为指定时间段预加载数据"""
        try:
            # 检查数据完整性
            completeness = preloader.check_data_completeness(
                start_date=start_date,
                end_date=end_date,
                stocks=None  # 将获取所有A股
            )
            
            # 如果数据不完整，进行下载
            if not completeness.get('is_complete', False):
                if self.verbose:
                    print(f"    预加载数据: {start_date} ~ {end_date}（覆盖率: {completeness.get('coverage_percentage', 0):.1f}%）")
                
                preloader.preload_market_data(
                    start_date=start_date,
                    end_date=end_date,
                    force_refresh=self.config.force_refresh_data
                )
            else:
                if self.verbose:
                    print(f"    数据已完整，跳过下载（覆盖率: {completeness.get('coverage_percentage', 0):.1f}%）")
        except Exception as e:
            logger.warning(f"时间段 {start_date} ~ {end_date} 数据预加载失败: {e}")
            if self.verbose:
                print(f"    ⚠️  数据预加载失败: {e}")
    
    def _extract_patterns(self) -> Dict[str, Any]:
        """阶段3: 提取牛市专属模式"""
        try:
            from core.pattern_recognition.bull_market_pattern_extractor import BullMarketPatternExtractor
            
            csv_path = self.output_dir / 'bull_market_high_return_cases.csv'
            if not csv_path.exists():
                return {'pattern_count': 0, 'error': 'CSV文件不存在'}
            
            extractor = BullMarketPatternExtractor(n_clusters=4, verbose=False)
            cases_df = extractor.load_cases_from_csv(str(csv_path))
            
            patterns = extractor.extract_patterns(cases_df)
            
            # 保存模式
            json_path = str(self.output_dir / 'bull_market_patterns.json')
            if patterns:
                extractor.save_patterns(patterns, json_path)
            
            return {
                'pattern_count': len(patterns),
                'json_path': json_path,
                'patterns': [p.pattern_name for p in patterns],
            }
        except Exception as e:
            logger.error(f"模式提取失败: {e}")
            return {'pattern_count': 0, 'error': str(e)}
    
    def _generate_strategy(self, bull_strength: float) -> Dict[str, Any]:
        """阶段4: 生成混合策略"""
        try:
            from core.advisor_v4.bullettrade_strategy_generator import BulletTradeStrategyGenerator, StrategyConfig
            
            # 根据牛市强度确定策略模式
            if bull_strength > 70.0:
                strategy_mode = 'BULL_AGGRESSIVE'  # 100%牛市模式
            elif bull_strength > 30.0:
                strategy_mode = 'BULL_MIXED'  # 混合模式
            else:
                strategy_mode = 'BASE_FACTOR'  # 基础7因子模式
            
            # 创建策略配置
            config = StrategyConfig()
            
            # 根据模式调整参数
            if strategy_mode == 'BULL_AGGRESSIVE':
                # 激进模式：提高动量权重、增加持仓数量、更频繁调仓
                config.max_stocks = 15
                config.rebalance_weekday = 0  # 每周调仓
                config.min_total_score = 28.0  # 稍微降低分数要求
            elif strategy_mode == 'BULL_MIXED':
                # 混合模式：平衡参数
                config.max_stocks = 12
                config.rebalance_weekday = 0  # 每周调仓
                config.min_total_score = 30.0
            else:
                # 基础模式：保守参数
                config.max_stocks = 10
                config.rebalance_weekday = 0
                config.min_total_score = 30.0
            
            # 生成策略代码
            generator = BulletTradeStrategyGenerator(
                config=config,
                cache_data_dir=self.config.cache_dir
            )
            
            strategy_code = generator.generate_strategy_code(
                cache_data_dir=self.config.cache_dir
            )
            
            return {
                'strategy_mode': strategy_mode,
                'params': {
                    'max_stocks': config.max_stocks,
                    'min_total_score': config.min_total_score,
                    'rebalance_weekday': config.rebalance_weekday,
                },
                'strategy_code': strategy_code,
            }
        except Exception as e:
            logger.error(f"策略生成失败: {e}")
            return {'strategy_mode': 'ERROR', 'error': str(e)}
    
    def _run_initial_backtest(self, strategy_result: Dict) -> Dict[str, Any]:
        """阶段5: 执行初始回测（串行）"""
        try:
            from core.bullettrade.recursive_backtest_engine import RecursiveBacktestEngine, BacktestConfig
            
            if self.config.cache_dir is None:
                cache_dir = str(self.output_dir / 'cache')
            else:
                cache_dir = self.config.cache_dir
            
            backtest_config = BacktestConfig(
                start_date=self.config.backtest_start_date,
                end_date=self.config.backtest_end_date,
                initial_capital=self.config.initial_capital,
                cache_dir=cache_dir
            )
            
            engine = RecursiveBacktestEngine(
                base_config=backtest_config,
                verbose=self.verbose,
                use_mongodb=self.config.use_mongodb,
                use_gpu=self.config.use_gpu_acceleration,
                max_workers=self.config.max_parallel_workers
            )
            
            # 执行回测
            result = engine.run_backtest(
                strategy_params=strategy_result.get('params', {}),
                strategy_code=strategy_result.get('strategy_code'),
                backtest_id='initial_backtest'
            )
            
            return result.to_dict()
        except Exception as e:
            logger.error(f"初始回测失败: {e}", exc_info=True)
            return {'error': str(e), 'monthly_return': -1.0}
    
    def _run_parallel_initial_backtest(self, strategy_result: Dict) -> Dict[str, Any]:
        """阶段5: 并行执行初始回测（多时间段验证）"""
        try:
            from core.advisor_v4.parallel_backtest_runner import ParallelBacktestRunner
            from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig
            
            if self.config.cache_dir is None:
                cache_dir = str(self.output_dir / 'cache')
            else:
                cache_dir = self.config.cache_dir
            
            # 初始化并行回测运行器
            runner = ParallelBacktestRunner(
                cache_dir=cache_dir,
                use_gpu=self.config.use_gpu_acceleration,
                max_workers=self.config.max_parallel_workers,  # 安全模式：3个线程
                verbose=self.verbose
            )
            
            # 创建策略配置
            strategy_config = StrategyConfig()
            strategy_params = strategy_result.get('params', {})
            for key, value in strategy_params.items():
                if hasattr(strategy_config, key):
                    setattr(strategy_config, key, value)
            
            # 创建多个回测任务（可以添加更多时间段用于验证）
            periods = [
                (self.config.backtest_start_date, self.config.backtest_end_date),
                # 可以添加更多时间段用于验证（例如：不同的市场环境）
            ]
            
            if self.verbose:
                print(f"  并行回测 {len(periods)} 个时间段（使用{self.config.max_parallel_workers}个线程）")
            
            summary = runner.run_parallel_backtests(
                periods=periods,
                strategy_config=strategy_config,
                initial_capital=self.config.initial_capital
            )
            
            # 返回最佳结果
            if summary.best_result:
                return summary.best_result.to_dict()
            else:
                # 如果没有成功的结果，返回第一个结果（如果有）
                if summary.results:
                    return summary.results[0].to_dict()
                else:
                    return {'error': 'No successful backtest results', 'monthly_return': -1.0}
                    
        except Exception as e:
            logger.error(f"并行初始回测失败: {e}", exc_info=True)
            # 降级到串行回测
            if self.verbose:
                print(f"  ⚠️  并行回测失败，降级到串行回测: {e}")
            return self._run_initial_backtest(strategy_result)
    
    def _run_evolution(self) -> Dict[str, Any]:
        """阶段6: 执行递归进化优化（使用优化后的回测引擎）"""
        try:
            from core.evolution.evolution_controller import EvolutionController
            from core.evolution.bull_market_strategy_evolver import EvolutionConfig
            from core.bullettrade.recursive_backtest_engine import BacktestConfig
            
            if self.config.cache_dir is None:
                cache_dir = str(self.output_dir / 'cache')
            else:
                cache_dir = self.config.cache_dir
            
            backtest_config = BacktestConfig(
                start_date=self.config.backtest_start_date,
                end_date=self.config.backtest_end_date,
                initial_capital=self.config.initial_capital,
                cache_dir=cache_dir
            )
            
            evolution_config = EvolutionConfig(
                population_size=self.config.evolution_population_size,
                generations=self.config.evolution_generations,
                target_monthly_return=self.config.target_monthly_return,
                max_drawdown_limit=self.config.max_drawdown_limit,
                min_sharpe_ratio=self.config.min_sharpe_ratio,
            )
            
            controller = EvolutionController(
                backtest_config=backtest_config,
                evolution_config=evolution_config,
                max_generations=self.config.evolution_generations,
                output_dir=str(self.output_dir / 'evolution'),
                verbose=self.verbose,
                # 传递优化配置（如果EvolutionController支持）
                use_mongodb=self.config.use_mongodb,
                use_gpu=self.config.use_gpu_acceleration,
                max_workers=self.config.max_parallel_workers
            )
            
            # 执行进化
            evolution_result = controller.run_evolution(
                run_id=f"{self.config.backtest_start_date.replace('-', '')}_{self.config.backtest_end_date.replace('-', '')}"
            )
            
            # 提取最佳结果
            best_individual = evolution_result.best_individual
            best_result = None
            if best_individual and best_individual.backtest_result:
                best_result = best_individual.backtest_result.to_dict()
            
            return {
                'reached_target': evolution_result.reached_target,
                'best_params': best_individual.params if best_individual else {},
                'best_result': best_result,
                'total_generations': evolution_result.total_generations,
                'early_stopped': evolution_result.early_stopped,
            }
        except Exception as e:
            logger.error(f"进化优化失败: {e}", exc_info=True)
            return {'reached_target': False, 'error': str(e)}
    
    def _run_evolution_basic(self) -> Dict[str, Any]:
        """阶段6: 执行递归进化优化（基本版本，兼容旧接口）"""
        try:
            from core.evolution.evolution_controller import EvolutionController
            from core.evolution.bull_market_strategy_evolver import EvolutionConfig
            from core.bullettrade.recursive_backtest_engine import BacktestConfig
            
            if self.config.cache_dir is None:
                cache_dir = str(self.output_dir / 'cache')
            else:
                cache_dir = self.config.cache_dir
            
            backtest_config = BacktestConfig(
                start_date=self.config.backtest_start_date,
                end_date=self.config.backtest_end_date,
                initial_capital=self.config.initial_capital,
                cache_dir=cache_dir
            )
            
            evolution_config = EvolutionConfig(
                population_size=self.config.evolution_population_size,
                generations=self.config.evolution_generations,
                target_monthly_return=self.config.target_monthly_return,
                max_drawdown_limit=self.config.max_drawdown_limit,
                min_sharpe_ratio=self.config.min_sharpe_ratio,
            )
            
            controller = EvolutionController(
                backtest_config=backtest_config,
                evolution_config=evolution_config,
                max_generations=self.config.evolution_generations,
                output_dir=str(self.output_dir / 'evolution'),
                verbose=self.verbose
            )
            
            # 执行进化
            evolution_result = controller.run_evolution(
                run_id=f"{self.config.backtest_start_date.replace('-', '')}_{self.config.backtest_end_date.replace('-', '')}"
            )
            
            # 提取最佳结果
            best_individual = evolution_result.best_individual
            best_result = None
            if best_individual and best_individual.backtest_result:
                best_result = best_individual.backtest_result.to_dict()
            
            return {
                'reached_target': evolution_result.reached_target,
                'best_params': best_individual.params if best_individual else {},
                'best_result': best_result,
                'total_generations': evolution_result.total_generations,
                'early_stopped': evolution_result.early_stopped,
            }
        except Exception as e:
            logger.error(f"进化优化失败: {e}", exc_info=True)
            return {'reached_target': False, 'error': str(e)}
    
    def _save_to_knowledge_base(self, workflow_result: WorkflowResult) -> Dict[str, Any]:
        """阶段7: 存入知识库"""
        try:
            from scripts.kb.save_strategy_results_to_kb import save_workflow_result_to_kb
            
            # 使用专门的归档函数
            result = save_workflow_result_to_kb(workflow_result.to_dict())
            
            return result
        except Exception as e:
            logger.error(f"知识库保存失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def _save_workflow_result(self, result: WorkflowResult):
        """保存工作流结果到JSON文件"""
        import json
        
        output_file = self.output_dir / f"{result.workflow_id}_result.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        
        if self.verbose:
            print(f"\n✅ 工作流结果已保存到: {output_file}")


def main():
    """主函数：示例用法"""
    config = WorkflowConfig(
        backtest_start_date='2024-10-01',
        backtest_end_date='2024-12-31',
        evolution_population_size=20,  # 测试用小种群
        evolution_generations=3,       # 测试用少代数
    )
    
    workflow = BullMarketStrategyWorkflow(config=config, verbose=True)
    result = workflow.execute(skip_mining=False, skip_evolution=False)  # 执行完整工作流（包含3个历史牛市数据挖掘）
    
    print(f"\n工作流执行完成: {result.workflow_id}")
    print(f"是否达到目标: {result.reached_target}")


if __name__ == '__main__':
    main()
