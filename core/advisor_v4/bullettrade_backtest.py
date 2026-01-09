#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BulletTrade回测接口封装 - 支持策略代码生成和回测执行

功能：
1. 策略代码生成：调用BulletTradeStrategyGenerator生成策略代码
2. 回测执行：使用BulletTradeEngine执行回测
3. 结果处理：解析回测结果，生成绩效报告，保存到MongoDB
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime

from .bullettrade_strategy_generator import BulletTradeStrategyGenerator, StrategyConfig
from core.bullettrade.engine import BulletTradeEngine, BTConfig
from core.bullettrade.result import BTResult

logger = logging.getLogger(__name__)


class BulletTradeBacktest:
    """BulletTrade回测接口封装"""
    
    def __init__(
        self,
        strategy_config: Optional[StrategyConfig] = None,
        bt_config: Optional[BTConfig] = None,
        output_dir: str = "output/advisor_v4/bullettrade",
        cache_dir: Optional[str] = None,
    ):
        """
        初始化回测接口
        
        Args:
            strategy_config: 策略配置
            bt_config: BulletTrade回测配置
            output_dir: 输出目录
            cache_dir: 数据缓存目录
        """
        self.strategy_config = strategy_config or StrategyConfig()
        self.bt_config = bt_config or BTConfig()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir = cache_dir
        
        # 策略代码生成器（传递缓存目录）
        self.strategy_generator = BulletTradeStrategyGenerator(
            self.strategy_config,
            cache_data_dir=self.cache_dir
        )
        
        # BulletTrade引擎
        self.bt_engine = BulletTradeEngine(self.bt_config)
    
    def generate_strategy_code(self, filename: Optional[str] = None) -> str:
        """
        生成策略代码并保存到文件
        
        Args:
            filename: 文件名（如果为None，自动生成）
            
        Returns:
            策略文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"advisor_v4_validated_factors_{timestamp}.py"
        
        strategy_path = self.output_dir / filename
        
        # 生成并保存策略代码（传递缓存目录）
        self.strategy_generator.save_strategy_code(
            str(strategy_path),
            cache_data_dir=self.cache_dir
        )
        
        logger.info(f"策略代码已生成: {strategy_path}")
        return str(strategy_path)
    
    def run_backtest(
        self,
        start_date: str,
        end_date: str,
        initial_capital: float = 1000000.0,
        strategy_filename: Optional[str] = None,
    ) -> BTResult:
        """
        执行回测
        
        Args:
            start_date: 回测开始日期（YYYY-MM-DD）
            end_date: 回测结束日期（YYYY-MM-DD）
            initial_capital: 初始资金
            strategy_filename: 策略文件名（如果为None，自动生成）
            
        Returns:
            BTResult: 回测结果
        """
        # 1. 生成策略代码
        strategy_path = self.generate_strategy_code(strategy_filename)
        
        # 2. 更新BulletTrade配置
        self.bt_config.start_date = start_date
        self.bt_config.end_date = end_date
        self.bt_config.initial_capital = initial_capital
        self.bt_config.output_dir = str(self.output_dir / "backtest_results")
        
        # 3. 执行回测
        logger.info(f"开始回测: {start_date} ~ {end_date}")
        logger.info(f"初始资金: {initial_capital:,.2f}")
        logger.info(f"策略文件: {strategy_path}")
        
        result = self.bt_engine.run_backtest(
            strategy_path=strategy_path,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
        )
        
        # 4. 保存回测结果摘要
        self._save_backtest_summary(result, start_date, end_date)
        
        logger.info(f"回测完成: 总收益率={result.total_return:.2%}, 夏普比率={result.sharpe_ratio:.2f}")
        
        return result
    
    def _save_backtest_summary(
        self,
        result: BTResult,
        start_date: str,
        end_date: str,
    ):
        """
        保存回测结果摘要
        
        Args:
            result: 回测结果
            start_date: 回测开始日期
            end_date: 回测结束日期
        """
        import json
        
        # 计算Calmar比率（年化收益/最大回撤）
        calmar_ratio = 0.0
        if result.max_drawdown != 0:
            calmar_ratio = result.annual_return / abs(result.max_drawdown)
        
        summary = {
            "start_date": start_date,
            "end_date": end_date,
            "total_return": result.total_return,
            "annual_return": result.annual_return,
            "sharpe_ratio": result.sharpe_ratio,
            "max_drawdown": result.max_drawdown,
            "calmar_ratio": calmar_ratio,
            "win_rate": result.win_rate,
            "total_trades": result.total_trades,
            "strategy_config": {
                "max_stocks": self.strategy_config.max_stocks,
                "single_position_max": self.strategy_config.single_position_max,
                "stop_loss": self.strategy_config.stop_loss,
                "take_profit": self.strategy_config.take_profit,
                "trailing_stop": self.strategy_config.trailing_stop,
                "time_stop_days": self.strategy_config.time_stop_days,
            },
            "timestamp": datetime.now().isoformat(),
        }
        
        summary_path = self.output_dir / "backtest_results" / f"summary_{start_date}_{end_date}.json"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"回测摘要已保存: {summary_path}")


def run_backtest_simple(
    start_date: str,
    end_date: str,
    initial_capital: float = 1000000.0,
    strategy_config: Optional[StrategyConfig] = None,
) -> BTResult:
    """
    简化的回测接口
    
    Args:
        start_date: 回测开始日期（YYYY-MM-DD）
        end_date: 回测结束日期（YYYY-MM-DD）
        initial_capital: 初始资金
        strategy_config: 策略配置（可选）
        
    Returns:
        BTResult: 回测结果
    """
    backtest = BulletTradeBacktest(strategy_config=strategy_config)
    return backtest.run_backtest(
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
    )
