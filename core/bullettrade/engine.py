# -*- coding: utf-8 -*-
"""
BulletTrade 引擎封装

提供BulletTrade回测引擎的Python API封装
"""

import sys
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime

from .config import BTConfig, BTOptimizeConfig
from .result import BTResult, BTOptimizeResult

logger = logging.getLogger(__name__)


class BulletTradeEngine:
    """BulletTrade回测引擎封装"""
    
    def __init__(self, config: Optional[BTConfig] = None):
        """
        初始化BulletTrade引擎
        
        Args:
            config: 回测配置，可选。如果不提供，将使用默认配置
        """
        self.config = config or BTConfig()
        self._engine = None
        self._initialized = False
        
        # 添加BulletTrade包路径
        self._setup_path()
    
    def _setup_path(self):
        """设置BulletTrade包路径"""
        # 尝试多个可能的路径
        possible_paths = [
            Path(__file__).parent.parent.parent / "extension" / "venv" / "lib" / "python3.12" / "site-packages",
            Path(__file__).parent.parent.parent / "extension" / "venv" / "lib" / "python3.11" / "site-packages",
            Path.home() / ".local" / "lib" / "python3.12" / "site-packages",
        ]
        
        for path in possible_paths:
            if path.exists():
                str_path = str(path)
                if str_path not in sys.path:
                    sys.path.insert(0, str_path)
                    logger.debug(f"添加BulletTrade包路径: {str_path}")
                break
    
    def _get_bt_engine(self):
        """获取BulletTrade引擎类"""
        try:
            from bullet_trade.core.engine import BacktestEngine, create_backtest
            return BacktestEngine, create_backtest
        except ImportError as e:
            logger.error(f"导入BulletTrade失败: {e}")
            raise ImportError(
                "无法导入BulletTrade。请确保已安装: pip install bullet-trade\n"
                f"错误详情: {e}"
            )
    
    def run_backtest(
        self,
        strategy_path: Optional[str] = None,
        strategy_code: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        initial_capital: Optional[float] = None,
        **kwargs
    ) -> BTResult:
        """
        执行回测
        
        Args:
            strategy_path: 策略文件路径 (与strategy_code二选一)
            strategy_code: 策略代码字符串 (与strategy_path二选一)
            start_date: 回测开始日期，覆盖配置
            end_date: 回测结束日期，覆盖配置
            initial_capital: 初始资金，覆盖配置
            **kwargs: 其他参数
        
        Returns:
            BTResult: 回测结果
        """
        BacktestEngine, create_backtest = self._get_bt_engine()
        
        # 使用传入参数或配置参数
        _start = start_date or self.config.start_date
        _end = end_date or self.config.end_date
        _capital = initial_capital or self.config.initial_capital
        
        if not _start or not _end:
            raise ValueError("必须提供 start_date 和 end_date")
        
        # 处理策略代码
        temp_strategy_file = None
        if strategy_code and not strategy_path:
            # 创建临时策略文件
            temp_strategy_file = self._create_temp_strategy(strategy_code)
            strategy_path = temp_strategy_file
        
        if not strategy_path:
            raise ValueError("必须提供 strategy_path 或 strategy_code")
        
        # 确保输出目录存在
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置日志文件
        log_file = self.config.log_file
        if log_file is None and self.config.output_dir:
            log_file = str(output_dir / "backtest.log")
        
        try:
            logger.info(f"开始BulletTrade回测: {strategy_path}")
            logger.info(f"回测区间: {_start} ~ {_end}")
            logger.info(f"初始资金: {_capital:,.2f}")
            
            # 调用BulletTrade的create_backtest函数
            results = create_backtest(
                strategy_file=strategy_path,
                start_date=_start,
                end_date=_end,
                frequency=self.config.frequency,
                initial_cash=_capital,
                benchmark=self.config.benchmark,
                log_file=log_file,
                extras=self.config.extras,
                initial_positions=self.config.initial_positions,
                algorithm_id=self.config.algorithm_id,
            )
            
            # 生成报告
            if self.config.generate_html or self.config.generate_csv:
                self._generate_report(results, str(output_dir))
            
            # 创建结果对象
            result = BTResult.from_engine_results(results, str(output_dir))
            
            logger.info(f"回测完成: 总收益率={result.total_return:.2f}%, 夏普比率={result.sharpe_ratio:.2f}")
            
            return result
            
        finally:
            # 清理临时文件
            if temp_strategy_file and Path(temp_strategy_file).exists():
                try:
                    Path(temp_strategy_file).unlink()
                except Exception:
                    pass
    
    def _create_temp_strategy(self, code: str) -> str:
        """创建临时策略文件"""
        import tempfile
        
        # 创建临时文件
        fd, path = tempfile.mkstemp(suffix=".py", prefix="bt_strategy_")
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(code)
            return path
        except Exception:
            os.close(fd)
            raise
    
    def _generate_report(self, results: Dict[str, Any], output_dir: str):
        """生成回测报告"""
        try:
            from bullet_trade.core.analysis import generate_report
            
            generate_report(
                results,
                output_dir=output_dir,
                gen_images=self.config.generate_images,
                gen_csv=self.config.generate_csv,
                gen_html=self.config.generate_html,
            )
            logger.info(f"报告已生成: {output_dir}")
        except Exception as e:
            logger.warning(f"生成报告失败: {e}")
    
    def run_batch_backtest(
        self,
        strategies: List[Dict[str, Any]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[BTResult]:
        """
        批量回测多个策略
        
        Args:
            strategies: 策略列表，每个元素为 {"name": str, "path": str} 或 {"name": str, "code": str}
            start_date: 回测开始日期
            end_date: 回测结束日期
        
        Returns:
            List[BTResult]: 回测结果列表
        """
        results = []
        
        for i, strategy in enumerate(strategies):
            name = strategy.get("name", f"strategy_{i}")
            path = strategy.get("path")
            code = strategy.get("code")
            
            logger.info(f"回测策略 [{i+1}/{len(strategies)}]: {name}")
            
            try:
                # 设置独立的输出目录
                original_output = self.config.output_dir
                self.config.output_dir = str(Path(original_output) / name)
                
                result = self.run_backtest(
                    strategy_path=path,
                    strategy_code=code,
                    start_date=start_date,
                    end_date=end_date,
                )
                results.append(result)
                
                # 恢复原始输出目录
                self.config.output_dir = original_output
                
            except Exception as e:
                logger.error(f"策略 {name} 回测失败: {e}")
                results.append(None)
        
        return results
    
    def optimize(
        self,
        strategy_path: str,
        optimize_config: BTOptimizeConfig,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> BTOptimizeResult:
        """
        参数优化
        
        Args:
            strategy_path: 策略文件路径
            optimize_config: 优化配置
            start_date: 回测开始日期
            end_date: 回测结束日期
        
        Returns:
            BTOptimizeResult: 优化结果
        """
        import itertools
        import time
        
        t0 = time.time()
        
        _start = start_date or self.config.start_date
        _end = end_date or self.config.end_date
        
        if not optimize_config.param_grid:
            raise ValueError("param_grid 不能为空")
        
        # 生成参数组合
        param_names = list(optimize_config.param_grid.keys())
        param_values = list(optimize_config.param_grid.values())
        
        if optimize_config.method == "grid":
            param_combinations = list(itertools.product(*param_values))
        elif optimize_config.method == "random":
            import random
            all_combinations = list(itertools.product(*param_values))
            n_samples = min(optimize_config.n_trials, len(all_combinations))
            param_combinations = random.sample(all_combinations, n_samples)
        else:
            # TODO: 实现贝叶斯优化
            raise NotImplementedError(f"优化方法 {optimize_config.method} 暂未实现")
        
        logger.info(f"开始参数优化: {len(param_combinations)} 种参数组合")
        
        all_results = []
        best_result = None
        best_params = {}
        best_metric_value = float('-inf') if optimize_config.optimize_direction == "maximize" else float('inf')
        
        for i, values in enumerate(param_combinations):
            params = dict(zip(param_names, values))
            logger.info(f"优化进度 [{i+1}/{len(param_combinations)}]: {params}")
            
            try:
                # 设置extras参数
                self.config.extras = params
                self.config.output_dir = str(Path(self.config.output_dir) / f"trial_{i}")
                
                result = self.run_backtest(
                    strategy_path=strategy_path,
                    start_date=_start,
                    end_date=_end,
                )
                
                # 获取目标指标值
                metrics = result.get_metrics()
                metric_value = metrics.get(optimize_config.target_metric, 0)
                
                all_results.append({
                    "params": params,
                    "metrics": metrics,
                    "target_value": metric_value,
                })
                
                # 更新最优结果
                is_better = (
                    (optimize_config.optimize_direction == "maximize" and metric_value > best_metric_value) or
                    (optimize_config.optimize_direction == "minimize" and metric_value < best_metric_value)
                )
                
                if is_better:
                    best_metric_value = metric_value
                    best_result = result
                    best_params = params
                    logger.info(f"发现更优参数: {params}, {optimize_config.target_metric}={metric_value:.4f}")
                    
            except Exception as e:
                logger.error(f"参数组合 {params} 回测失败: {e}")
        
        runtime = time.time() - t0
        
        return BTOptimizeResult(
            best_params=best_params,
            best_result=best_result,
            all_results=all_results,
            target_metric=optimize_config.target_metric,
            n_trials=len(param_combinations),
            runtime_seconds=runtime,
        )


def run_backtest_simple(
    strategy_path: str,
    start_date: str,
    end_date: str,
    initial_capital: float = 1000000,
    benchmark: str = "000300.XSHG",
    output_dir: str = "./backtest_results",
) -> BTResult:
    """
    简化的回测接口
    
    Args:
        strategy_path: 策略文件路径
        start_date: 回测开始日期
        end_date: 回测结束日期
        initial_capital: 初始资金
        benchmark: 基准指数
        output_dir: 输出目录
    
    Returns:
        BTResult: 回测结果
    """
    config = BTConfig(
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        benchmark=benchmark,
        output_dir=output_dir,
    )
    
    engine = BulletTradeEngine(config)
    return engine.run_backtest(strategy_path=strategy_path)


__all__ = ["BulletTradeEngine", "run_backtest_simple"]

