# -*- coding: utf-8 -*-
"""
批量回测管理器
=============
支持多策略、多参数的并行回测与对比：
1. 参数网格搜索
2. 多策略对比
3. 结果排名
4. 可视化报告
"""

import logging
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
import pandas as pd
import json
import concurrent.futures
from itertools import product

logger = logging.getLogger(__name__)


@dataclass
class StrategyConfig:
    """策略配置"""
    name: str
    strategy_type: str
    params: Dict[str, Any]


@dataclass
class BatchBacktestResult:
    """批量回测结果"""
    config: StrategyConfig
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    duration_seconds: float


class BatchBacktestManager:
    """批量回测管理器"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.results: List[BatchBacktestResult] = []
        self._mongo_db = None
        self._init_mongo()
    
    def _init_mongo(self):
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
            self._mongo_db = client.get_database("trquant")
        except: pass
    
    def grid_search(self,
                   securities: List[str],
                   start_date: str,
                   end_date: str,
                   strategy_type: str,
                   param_grid: Dict[str, List],
                   callback: Callable[[int, int, BatchBacktestResult], None] = None) -> List[BatchBacktestResult]:
        """
        参数网格搜索
        
        Args:
            securities: 股票列表
            start_date: 开始日期
            end_date: 结束日期
            strategy_type: 策略类型
            param_grid: 参数网格 {"mom_short": [3,5,10], "mom_long": [15,20,30]}
            callback: 回调函数(当前索引, 总数, 结果)
        """
        # 生成参数组合
        keys = list(param_grid.keys())
        values = list(param_grid.values())
        combinations = list(product(*values))
        
        total = len(combinations)
        logger.info(f"开始网格搜索，共{total}种参数组合")
        
        self.results = []
        
        for i, combo in enumerate(combinations):
            params = dict(zip(keys, combo))
            config = StrategyConfig(
                name=f"{strategy_type}_{i}",
                strategy_type=strategy_type,
                params=params
            )
            
            # 运行回测
            result = self._run_single_backtest(securities, start_date, end_date, config)
            self.results.append(result)
            
            if callback:
                callback(i + 1, total, result)
            
            logger.info(f"[{i+1}/{total}] {params} -> 收益: {result.total_return:.2%}, 夏普: {result.sharpe_ratio:.2f}")
        
        # 保存结果
        self._save_results(f"grid_search_{strategy_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        return self.results
    
    def compare_strategies(self,
                          securities: List[str],
                          start_date: str,
                          end_date: str,
                          configs: List[StrategyConfig]) -> List[BatchBacktestResult]:
        """
        多策略对比
        """
        self.results = []
        
        for i, config in enumerate(configs):
            result = self._run_single_backtest(securities, start_date, end_date, config)
            self.results.append(result)
            logger.info(f"[{i+1}/{len(configs)}] {config.name} -> 收益: {result.total_return:.2%}")
        
        return self.results
    
    def _run_single_backtest(self, 
                            securities: List[str],
                            start_date: str,
                            end_date: str,
                            config: StrategyConfig) -> BatchBacktestResult:
        """运行单次回测"""
        try:
            from core.backtest.fast_backtest_engine import quick_backtest
            
            result = quick_backtest(
                securities=securities,
                start_date=start_date,
                end_date=end_date,
                strategy=config.strategy_type,
                **config.params
            )
            
            return BatchBacktestResult(
                config=config,
                total_return=result.total_return,
                annual_return=result.annual_return,
                sharpe_ratio=result.sharpe_ratio,
                max_drawdown=result.max_drawdown,
                win_rate=result.win_rate,
                total_trades=result.total_trades,
                duration_seconds=result.duration_seconds
            )
        except Exception as e:
            logger.error(f"回测失败 {config.name}: {e}")
            return BatchBacktestResult(
                config=config,
                total_return=0.0,
                annual_return=0.0,
                sharpe_ratio=0.0,
                max_drawdown=0.0,
                win_rate=0.0,
                total_trades=0,
                duration_seconds=0.0
            )
    
    def get_ranking(self, sort_by: str = "sharpe_ratio", ascending: bool = False) -> List[BatchBacktestResult]:
        """获取排名"""
        return sorted(self.results, key=lambda x: getattr(x, sort_by, 0), reverse=not ascending)
    
    def get_summary_df(self) -> pd.DataFrame:
        """获取汇总DataFrame"""
        data = []
        for r in self.results:
            row = {
                "name": r.config.name,
                "strategy": r.config.strategy_type,
                **r.config.params,
                "total_return": r.total_return,
                "annual_return": r.annual_return,
                "sharpe_ratio": r.sharpe_ratio,
                "max_drawdown": r.max_drawdown,
                "win_rate": r.win_rate,
                "trades": r.total_trades,
                "duration_s": r.duration_seconds
            }
            data.append(row)
        return pd.DataFrame(data)
    
    def _save_results(self, name: str):
        """保存结果"""
        if not self.results:
            return
        
        # 保存到MongoDB
        if self._mongo_db:
            try:
                data = {
                    "name": name,
                    "timestamp": datetime.now().isoformat(),
                    "results": [
                        {
                            "config": asdict(r.config),
                            "total_return": r.total_return,
                            "annual_return": r.annual_return,
                            "sharpe_ratio": r.sharpe_ratio,
                            "max_drawdown": r.max_drawdown,
                            "win_rate": r.win_rate,
                            "total_trades": r.total_trades
                        }
                        for r in self.results
                    ]
                }
                self._mongo_db.batch_backtest_results.insert_one(data)
                logger.info(f"结果已保存到MongoDB: {name}")
            except Exception as e:
                logger.warning(f"保存结果失败: {e}")
    
    def print_summary(self):
        """打印汇总"""
        if not self.results:
            print("无回测结果")
            return
        
        df = self.get_summary_df()
        print("\n" + "="*80)
        print("批量回测结果汇总")
        print("="*80)
        print(df.to_string(index=False))
        print("\n最佳策略（按夏普比率）:")
        best = self.get_ranking("sharpe_ratio")[0]
        print(f"  {best.config.name}: 收益={best.total_return:.2%}, 夏普={best.sharpe_ratio:.2f}")
