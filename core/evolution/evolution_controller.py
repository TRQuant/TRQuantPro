#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
进化控制器

控制进化轮次、精英保留、早停机制、结果持久化。
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from core.evolution.bull_market_strategy_evolver import BullMarketStrategyEvolver, Individual, EvolutionConfig
from core.evolution.evolution_feedback_analyzer import EvolutionFeedbackAnalyzer, FeedbackAnalysis
from core.bullettrade.recursive_backtest_engine import BacktestConfig

logger = logging.getLogger(__name__)


@dataclass
class EvolutionRunResult:
    """进化运行结果"""
    run_id: str
    start_time: str
    end_time: str
    total_generations: int
    best_individual: Optional[Individual]
    best_fitness: float
    reached_target: bool
    early_stopped: bool
    stop_reason: str
    
    # 每代最佳结果
    generation_best: List[Dict] = field(default_factory=list)
    
    # 反馈分析结果
    final_feedback: Optional[FeedbackAnalysis] = None


class EvolutionController:
    """进化控制器"""
    
    def __init__(
        self,
        backtest_config: BacktestConfig,
        evolution_config: Optional[EvolutionConfig] = None,
        max_generations: int = 10,
        early_stop_patience: int = 3,
        output_dir: str = 'output/evolution',
        verbose: bool = True,
        use_mongodb: Optional[bool] = None,
        use_gpu: Optional[bool] = None,
        max_workers: Optional[int] = None
    ):
        """
        初始化进化控制器
        
        Args:
            backtest_config: 回测配置
            evolution_config: 进化配置
            max_generations: 最大进化代数
            early_stop_patience: 早停耐心（连续N代无改进则停止）
            output_dir: 输出目录
            verbose: 是否输出详细信息
            use_mongodb: 是否使用MongoDB存储（默认True）
            use_gpu: 是否使用GPU加速（默认True）
            max_workers: 最大并行工作数（安全模式：3）
        """
        self.backtest_config = backtest_config
        self.evolution_config = evolution_config or EvolutionConfig()
        self.max_generations = max_generations
        self.early_stop_patience = early_stop_patience
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose
        self.use_mongodb = use_mongodb if use_mongodb is not None else True
        self.use_gpu = use_gpu if use_gpu is not None else True
        self.max_workers = max_workers if max_workers is not None else 3
        
        # 预加载数据（一次加载，多次使用）
        self._preload_all_data()
        
        # 创建进化器（传递优化参数）
        self.evolver = BullMarketStrategyEvolver(
            backtest_config=backtest_config,
            evolution_config=self.evolution_config,
            verbose=verbose,
            use_mongodb=use_mongodb,
            use_gpu=use_gpu,
            max_workers=max_workers
        )
        
        # 创建反馈分析器
        self.feedback_analyzer = EvolutionFeedbackAnalyzer(
            target_monthly_return=self.evolution_config.target_monthly_return,
            verbose=verbose
        )
        
        # 运行历史
        self.run_history: List[EvolutionRunResult] = []
    
    def _preload_all_data(self):
        """预加载所有数据（一次加载，多次使用）"""
        try:
            from core.advisor_v4.data_preloader import DataPreloader
            
            if self.backtest_config.cache_dir is None:
                cache_dir = str(self.output_dir / 'cache')
            else:
                cache_dir = self.backtest_config.cache_dir
            
            preloader = DataPreloader(
                use_mongodb=self.use_mongodb,
                cache_dir=cache_dir,
                max_workers=self.max_workers,
                verbose=self.verbose
            )
            
            if self.verbose:
                print(f"\n[数据预加载] 检查并加载回测数据...")
            
            # 检查数据完整性
            completeness = preloader.check_data_completeness(
                start_date=self.backtest_config.start_date,
                end_date=self.backtest_config.end_date,
                stocks=None
            )
            
            if not completeness.get('is_complete', False):
                if self.verbose:
                    print(f"  数据不完整，开始下载...")
                
                preloader.preload_market_data(
                    start_date=self.backtest_config.start_date,
                    end_date=self.backtest_config.end_date,
                    force_refresh=False
                )
            else:
                if self.verbose:
                    print(f"  ✅ 数据已完整（覆盖率: {completeness.get('coverage_percentage', 0):.1f}%）")
        except Exception as e:
            logger.warning(f"数据预加载失败: {e}，将继续使用API获取数据")
    
    def run_evolution(
        self,
        run_id: Optional[str] = None,
        save_intermediate: bool = True
    ) -> EvolutionRunResult:
        """
        执行进化
        
        Args:
            run_id: 运行ID（如果为None，自动生成）
            save_intermediate: 是否保存中间结果
        
        Returns:
            EvolutionRunResult
        """
        if run_id is None:
            run_id = f"evolution_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"开始进化运行: {run_id}")
            print(f"{'='*70}")
            print(f"开始时间: {start_time}")
            print(f"最大代数: {self.max_generations}")
            print(f"早停耐心: {self.early_stop_patience}")
        
        # 执行进化
        best_individual = self.evolver.evolve()
        
        # 记录每代最佳
        generation_best = []
        for gen, gen_info in enumerate(self.evolver.generation_history):
            generation_best.append({
                'generation': gen,
                'best_fitness': gen_info.get('best_fitness', 0.0),
                'best_monthly_return': gen_info.get('best_monthly_return', 0.0),
                'best_max_drawdown': gen_info.get('best_max_drawdown', 0.0),
                'best_sharpe_ratio': gen_info.get('best_sharpe_ratio', 0.0),
                'meets_target': gen_info.get('meets_target', False),
            })
        
        # 检查是否达到目标
        reached_target = False
        if best_individual and best_individual.backtest_result:
            reached_target = best_individual.backtest_result.meets_target(
                target_monthly_return=self.evolution_config.target_monthly_return,
                max_dd=self.evolution_config.max_drawdown_limit,
                min_sharpe=self.evolution_config.min_sharpe_ratio
            )
        
        # 检查早停
        early_stopped = False
        stop_reason = "completed"
        
        if len(generation_best) >= self.early_stop_patience + 1:
            # 检查最近N代是否有改进
            recent_best = [g['best_monthly_return'] for g in generation_best[-self.early_stop_patience:]]
            if len(set(recent_best)) == 1:  # 所有值相同，没有改进
                early_stopped = True
                stop_reason = f"连续{self.early_stop_patience}代无改进"
        
        # 最终反馈分析
        final_feedback = None
        if self.evolver.population:
            final_feedback = self.feedback_analyzer.analyze_population(self.evolver.population)
        
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_generations = len(generation_best)
        
        result = EvolutionRunResult(
            run_id=run_id,
            start_time=start_time,
            end_time=end_time,
            total_generations=total_generations,
            best_individual=best_individual,
            best_fitness=best_individual.fitness if best_individual else -999.0,
            reached_target=reached_target,
            early_stopped=early_stopped,
            stop_reason=stop_reason,
            generation_best=generation_best,
            final_feedback=final_feedback,
        )
        
        # 保存结果
        if save_intermediate:
            self._save_run_result(result)
        
        self.run_history.append(result)
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"进化运行完成: {run_id}")
            print(f"{'='*70}")
            print(f"总代数: {total_generations}")
            print(f"是否达到目标: {reached_target}")
            print(f"是否早停: {early_stopped} ({stop_reason})")
            if best_individual and best_individual.backtest_result:
                result_bt = best_individual.backtest_result
                print(f"最佳月收益率: {result_bt.monthly_return*100:.2f}%")
                print(f"最佳最大回撤: {result_bt.max_drawdown*100:.2f}%")
                print(f"最佳夏普比率: {result_bt.sharpe_ratio:.2f}")
        
        return result
    
    def _save_run_result(self, result: EvolutionRunResult):
        """保存运行结果"""
        output_file = self.output_dir / f"{result.run_id}_result.json"
        
        result_dict = {
            'run_id': result.run_id,
            'start_time': result.start_time,
            'end_time': result.end_time,
            'total_generations': result.total_generations,
            'best_individual': result.best_individual.to_dict() if result.best_individual else None,
            'best_fitness': result.best_fitness,
            'reached_target': result.reached_target,
            'early_stopped': result.early_stopped,
            'stop_reason': result.stop_reason,
            'generation_best': result.generation_best,
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, ensure_ascii=False, indent=2)
        
        if self.verbose:
            print(f"✅ 运行结果已保存到: {output_file}")
    
    def get_best_run(self) -> Optional[EvolutionRunResult]:
        """获取最佳运行结果"""
        if not self.run_history:
            return None
        
        return max(self.run_history, key=lambda r: r.best_fitness)
    
    def save_all_results(self, output_file: str = None):
        """保存所有运行结果"""
        if output_file is None:
            output_file = str(self.output_dir / "all_evolution_results.json")
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        all_results = {
            'summary': {
                'total_runs': len(self.run_history),
                'best_run_id': self.get_best_run().run_id if self.get_best_run() else None,
                'best_fitness': self.get_best_run().best_fitness if self.get_best_run() else -999.0,
            },
            'runs': [
                {
                    'run_id': r.run_id,
                    'best_fitness': r.best_fitness,
                    'reached_target': r.reached_target,
                    'total_generations': r.total_generations,
                }
                for r in self.run_history
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        
        if self.verbose:
            print(f"✅ 所有运行结果已保存到: {output_path}")


def main():
    """主函数：示例用法"""
    backtest_config = BacktestConfig(
        start_date='2024-10-01',
        end_date='2024-12-31',
        initial_capital=1000000.0,
        cache_dir='output/evolution_backtest_cache'
    )
    
    evolution_config = EvolutionConfig(
        population_size=20,
        generations=5,
        target_monthly_return=0.30,
    )
    
    controller = EvolutionController(
        backtest_config=backtest_config,
        evolution_config=evolution_config,
        max_generations=5,
        early_stop_patience=3,
        output_dir='output/evolution',
        verbose=True
    )
    
    # 执行进化
    result = controller.run_evolution()
    
    # 保存所有结果
    controller.save_all_results()
    
    print(f"\n最佳参数: {result.best_individual.params if result.best_individual else None}")


if __name__ == '__main__':
    main()
