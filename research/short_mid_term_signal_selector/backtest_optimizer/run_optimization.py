# -*- coding: utf-8 -*-
"""
完整优化流程运行脚本

整合：
1. 市场环境识别
2. 因子权重优化
3. 回测验证
4. 最终选股
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .backtest_engine import BacktestEngine, BACKTEST_PERIODS
from .factor_optimizer import FactorOptimizer, OptimizationConfig, DEFAULT_FACTORS
from .market_regime_adapter import MarketRegimeAdapter, MarketRegime
from .final_selector import FinalSelector, generate_final_report_html


class OptimizationPipeline:
    """
    完整优化流程管道
    
    工作流程：
    1. 检测市场环境 → 确定策略基调
    2. 历史回测验证 → 验证算法有效性
    3. 因子权重优化 → 基于历史表现学习
    4. 应用优化结果 → 执行最终筛选
    5. 生成投资组合 → 浓缩到5个标的
    """
    
    def __init__(self):
        """初始化管道"""
        # 市场环境适配器
        self.regime_adapter = MarketRegimeAdapter()
        
        # 当前状态
        self.current_regime = None
        self.optimized_weights = None
        self.backtest_results = None
        
    def run_full_pipeline(self,
                         screener_func,
                         backtest_start: str = None,
                         backtest_end: str = None,
                         optimize_weights: bool = True,
                         top_n_candidates: int = 30,
                         final_count: int = 5) -> Dict:
        """
        运行完整优化流程
        
        Args:
            screener_func: 筛选函数
            backtest_start: 回测开始日期
            backtest_end: 回测结束日期
            optimize_weights: 是否优化权重
            top_n_candidates: 候选池大小
            final_count: 最终选股数量
            
        Returns:
            Dict: 包含所有结果的字典
        """
        print("\n" + "="*70)
        print("🚀 启动完整优化流程")
        print("="*70)
        
        results = {}
        
        # ============ Step 1: 市场环境检测 ============
        print("\n" + "-"*50)
        print("📊 Step 1: 市场环境检测")
        print("-"*50)
        
        regime_signal = self.regime_adapter.detect_regime()
        self.current_regime = regime_signal.regime
        results['market_regime'] = {
            'regime': regime_signal.regime.value,
            'confidence': regime_signal.confidence,
            'index_return_20d': regime_signal.index_return_20d,
            'index_return_60d': regime_signal.index_return_60d
        }
        
        # 获取策略配置
        strategy_config = self.regime_adapter.get_strategy_config()
        results['strategy_config'] = {
            'position_limit': strategy_config.position_limit,
            'stop_loss_pct': strategy_config.stop_loss_pct,
            'max_candidates': strategy_config.max_candidates
        }
        
        # ============ Step 2: 历史回测验证 ============
        if backtest_start and backtest_end:
            print("\n" + "-"*50)
            print("📈 Step 2: 历史回测验证")
            print("-"*50)
            
            engine = BacktestEngine(
                screener_func=screener_func,
                periods=['week', 'month', 'quarter']
            )
            
            self.backtest_results = engine.run_rolling_backtest(
                start_date=backtest_start,
                end_date=backtest_end,
                frequency='month',
                top_n=top_n_candidates
            )
            
            if self.backtest_results:
                # 汇总回测结果
                results['backtest_summary'] = self._summarize_backtest()
        
        # ============ Step 3: 因子权重优化 ============
        if optimize_weights and backtest_start and backtest_end and self.backtest_results:
            print("\n" + "-"*50)
            print("🔧 Step 3: 因子权重优化")
            print("-"*50)
            
            optimizer = FactorOptimizer(
                backtest_engine=engine,
                config=OptimizationConfig(
                    target_period='month',
                    target_metric='excess',
                    regularization=0.1
                )
            )
            
            optimization_result = optimizer.optimize(
                start_date=backtest_start,
                end_date=backtest_end
            )
            
            self.optimized_weights = optimization_result.optimized_weights
            
            results['factor_optimization'] = {
                'optimized_weights': self.optimized_weights,
                'improvement': optimization_result.improvement,
                'val_score': optimization_result.val_score,
                'factor_importance': optimization_result.factor_importance
            }
        else:
            # 使用默认权重并根据市场环境调整
            default_weights = {name: f.default_weight for name, f in DEFAULT_FACTORS.items()}
            self.optimized_weights = self.regime_adapter.adjust_factor_weights(
                default_weights, self.current_regime
            )
            results['factor_optimization'] = {
                'optimized_weights': self.optimized_weights,
                'note': '使用默认权重(市场环境调整)'
            }
        
        # ============ Step 4: 执行最新筛选 ============
        print("\n" + "-"*50)
        print("🔍 Step 4: 执行最新筛选")
        print("-"*50)
        
        today = datetime.now().strftime('%Y-%m-%d')
        candidates = screener_func(
            as_of_date=today,
            top_n=top_n_candidates,
            factor_weights=self.optimized_weights
        )
        
        results['candidates'] = {
            'count': len(candidates) if candidates else 0,
            'stocks': candidates[:10] if candidates else []  # 前10只作为示例
        }
        
        # ============ Step 5: 最终选股 ============
        print("\n" + "-"*50)
        print("🎯 Step 5: 最终选股 (Top 5)")
        print("-"*50)
        
        if candidates:
            from .final_selector import SelectionCriteria
            
            criteria = SelectionCriteria(
                final_count=final_count,
                max_per_sector=2 if self.current_regime != MarketRegime.STRONG_BULL else 3,
                min_sectors=3
            )
            
            selector = FinalSelector(
                criteria=criteria,
                market_regime=self.current_regime.value if self.current_regime else 'neutral'
            )
            
            selection_result = selector.select(candidates, today)
            
            results['final_selection'] = {
                'stocks': [
                    {
                        'rank': s.rank,
                        'code': s.code,
                        'name': s.name,
                        'sector': s.sector,
                        'weight': s.suggested_weight,
                        'stop_loss': s.stop_loss,
                        'target': s.target_price,
                        'reason': s.selection_reason
                    }
                    for s in selection_result.stocks
                ],
                'summary': selection_result.selection_summary
            }
            
            # 生成HTML报告
            report_path = generate_final_report_html(selection_result)
            results['report_path'] = report_path
        
        # ============ 输出最终总结 ============
        self._print_final_summary(results)
        
        return results
    
    def _summarize_backtest(self) -> Dict:
        """汇总回测结果"""
        if not self.backtest_results:
            return {}
        
        summary = {}
        for period_key in ['week', 'month', 'quarter']:
            returns = [r.avg_returns.get(period_key, 0) for r in self.backtest_results 
                      if r.avg_returns.get(period_key) is not None]
            win_rates = [r.win_rates.get(period_key, 0) for r in self.backtest_results
                        if r.win_rates.get(period_key) is not None]
            excess = [r.excess_returns.get(period_key, 0) for r in self.backtest_results
                     if r.excess_returns.get(period_key) is not None]
            
            if returns:
                summary[period_key] = {
                    'avg_return': np.mean(returns),
                    'return_std': np.std(returns),
                    'avg_win_rate': np.mean(win_rates) if win_rates else 0,
                    'avg_excess': np.mean(excess) if excess else 0,
                    'positive_periods': sum(1 for r in returns if r > 0),
                    'total_periods': len(returns)
                }
        
        return summary
    
    def _print_final_summary(self, results: Dict):
        """打印最终总结"""
        print("\n" + "="*70)
        print("📋 优化流程完成 - 最终总结")
        print("="*70)
        
        # 市场环境
        regime = results.get('market_regime', {})
        print(f"\n🌍 市场环境: {regime.get('regime', 'unknown')} "
              f"(置信度: {regime.get('confidence', 0):.0f}%)")
        
        # 策略配置
        config = results.get('strategy_config', {})
        print(f"⚙️ 策略配置: 仓位上限 {config.get('position_limit', 0)*100:.0f}%, "
              f"止损 {config.get('stop_loss_pct', 0)*100:.1f}%")
        
        # 回测表现
        backtest = results.get('backtest_summary', {})
        if backtest:
            month_data = backtest.get('month', {})
            print(f"\n📊 历史回测 (月度):")
            print(f"   平均收益: {month_data.get('avg_return', 0):.2f}%")
            print(f"   平均超额: {month_data.get('avg_excess', 0):.2f}%")
            print(f"   胜率: {month_data.get('avg_win_rate', 0):.1f}%")
        
        # 最终选股
        selection = results.get('final_selection', {})
        if selection:
            print(f"\n🏆 最终投资组合:")
            for s in selection.get('stocks', []):
                print(f"   {s['rank']}. {s['code']} {s['name']} "
                      f"({s['sector']}) - 仓位{s['weight']*100:.1f}%")
        
        # 报告路径
        if results.get('report_path'):
            print(f"\n📄 详细报告: {results['report_path']}")


def run_quick_optimization(top_n: int = 5):
    """
    快速运行优化流程（不含历史回测）
    
    适用于快速获取投资建议
    """
    print("\n🚀 快速优化模式")
    
    # 导入筛选器
    from research.short_mid_term_signal_selector.tenbagger_mainline_screener import MainlineScreener
    
    def screener_func(as_of_date=None, top_n=30, factor_weights=None):
        screener = MainlineScreener()
        return screener.screen(top_n=top_n)
    
    pipeline = OptimizationPipeline()
    
    results = pipeline.run_full_pipeline(
        screener_func=screener_func,
        backtest_start=None,  # 跳过回测
        backtest_end=None,
        optimize_weights=False,
        top_n_candidates=30,
        final_count=top_n
    )
    
    return results


def run_full_optimization(
    backtest_months: int = 12,
    top_n: int = 5
):
    """
    运行完整优化流程（含历史回测）
    
    Args:
        backtest_months: 回测月数
        top_n: 最终选股数
    """
    print("\n🚀 完整优化模式")
    
    # 计算回测区间
    end_date = datetime.now()
    start_date = end_date - timedelta(days=backtest_months * 30)
    
    # 导入筛选器（需要支持历史日期版本）
    # TODO: 实现支持历史日期的筛选函数
    
    pipeline = OptimizationPipeline()
    
    # 目前只运行快速模式，完整模式需要历史筛选支持
    print("⚠️ 完整优化模式需要历史数据筛选支持，当前运行快速模式")
    return run_quick_optimization(top_n)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='运行投资组合优化')
    parser.add_argument('--mode', choices=['quick', 'full'], default='quick',
                       help='运行模式: quick(快速) / full(完整)')
    parser.add_argument('--top-n', type=int, default=5,
                       help='最终选股数量')
    parser.add_argument('--backtest-months', type=int, default=12,
                       help='回测月数(仅full模式)')
    
    args = parser.parse_args()
    
    if args.mode == 'quick':
        results = run_quick_optimization(args.top_n)
    else:
        results = run_full_optimization(args.backtest_months, args.top_n)
