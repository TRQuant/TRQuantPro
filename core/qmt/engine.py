# -*- coding: utf-8 -*-
"""
QMT回测引擎
===========

封装xtquant回测功能，提供统一的API接口
"""
import logging
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from .config import QMTConfig, QMTOptimizeConfig
from .result import QMTResult, QMTOptimizeResult

logger = logging.getLogger(__name__)

# 导入现有的xtquant模块
try:
    from core.trading.xtquant_backtest import (
        XtBacktestEngine,
        XtBacktestConfig,
        XtBacktestResult,
        XTQUANT_AVAILABLE,
        check_xtquant_status,
    )
    XTQUANT_IMPORTED = True
except ImportError:
    XTQUANT_IMPORTED = False
    XTQUANT_AVAILABLE = False
    logger.warning("无法导入xtquant_backtest模块")


class QMTEngine:
    """QMT回测引擎"""
    
    def __init__(self, config: QMTConfig):
        """
        初始化QMT引擎
        
        Args:
            config: QMT配置
        """
        self.config = config
        self._xt_engine = None
        self._check_availability()
    
    def _check_availability(self):
        """检查xtquant可用性"""
        if not XTQUANT_IMPORTED:
            logger.warning("xtquant模块未导入，QMT回测可能不可用")
            return
        
        status = check_xtquant_status()
        if not status.get("can_backtest", False):
            logger.warning(f"QMT回测不可用: {status.get('message', '未知错误')}")
    
    def _convert_config(self) -> XtBacktestConfig:
        """转换配置格式"""
        return XtBacktestConfig(
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            stock_list=self.config.stock_pool,
            initial_capital=self.config.initial_capital,
            commission_rate=self.config.commission_rate,
            stamp_tax=self.config.stamp_tax_rate,
            slippage=self.config.slippage,
            benchmark=self.config.benchmark,
            data_period=self.config.data_period.value,
            qmt_path=self.config.qmt_path,
        )
    
    def _convert_result(self, xt_result: XtBacktestResult, duration: float) -> QMTResult:
        """转换结果格式"""
        return QMTResult(
            success=True,
            message="回测成功",
            total_return=xt_result.total_return,
            annual_return=xt_result.annual_return,
            sharpe_ratio=xt_result.sharpe_ratio,
            max_drawdown=xt_result.max_drawdown,
            win_rate=xt_result.win_rate,
            total_trades=xt_result.trade_count,
            trading_days=len(xt_result.daily_returns) if xt_result.daily_returns else 0,
            duration_seconds=duration,
            benchmark_return=xt_result.benchmark_return,
            equity_curve=xt_result.equity_curve,
            trades=xt_result.trades,
            daily_records=None,  # TODO: 从equity_curve构建
            metrics={
                "calmar_ratio": 0.0,  # TODO: 计算
                "sortino_ratio": 0.0,  # TODO: 计算
            },
            raw_results={
                "xt_result": {
                    "total_return": xt_result.total_return,
                    "annual_return": xt_result.annual_return,
                    "sharpe_ratio": xt_result.sharpe_ratio,
                }
            },
        )
    
    def run_backtest(
        self,
        strategy_path: Optional[str] = None,
        strategy_code: Optional[str] = None,
        strategy_func: Optional[Callable] = None,
        on_progress: Optional[Callable] = None,
    ) -> QMTResult:
        """
        执行回测
        
        Args:
            strategy_path: 策略文件路径
            strategy_code: 策略代码字符串
            strategy_func: 策略函数（接收date, data, positions, cash）
            on_progress: 进度回调函数(progress, message)
        
        Returns:
            回测结果
        """
        start_time = time.time()
        
        try:
            # 转换配置
            xt_config = self._convert_config()
            self._xt_engine = XtBacktestEngine(xt_config)
            
            # 确定策略函数
            if strategy_func:
                func = strategy_func
            elif strategy_path:
                func = self._load_strategy_from_file(strategy_path)
            elif strategy_code:
                func = self._load_strategy_from_code(strategy_code)
            else:
                return QMTResult(
                    success=False,
                    message="必须提供 strategy_path、strategy_code 或 strategy_func"
                )
            
            # 执行回测
            xt_result = self._xt_engine.run(func, on_progress)
            
            # 转换结果
            duration = time.time() - start_time
            result = self._convert_result(xt_result, duration)
            
            # 保存报告
            if self.config.output_dir:
                result.report_path = self._generate_report(result)
            
            return result
            
        except Exception as e:
            logger.error(f"QMT回测失败: {e}", exc_info=True)
            return QMTResult(
                success=False,
                message=f"回测失败: {str(e)}",
                duration_seconds=time.time() - start_time,
            )
    
    def _load_strategy_from_file(self, path: str) -> Callable:
        """从文件加载策略"""
        # TODO: 实现策略文件加载
        raise NotImplementedError("策略文件加载待实现")
    
    def _load_strategy_from_code(self, code: str) -> Callable:
        """从代码字符串加载策略"""
        # TODO: 实现策略代码加载
        raise NotImplementedError("策略代码加载待实现")
    
    def _generate_report(self, result: QMTResult) -> Optional[str]:
        """生成回测报告"""
        try:
            output_dir = Path(self.config.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            report_path = output_dir / "qmt_backtest_report.html"
            
            # 生成简单HTML报告
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>QMT回测报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .metric {{ font-size: 18px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>QMT回测报告</h1>
    <div class="metric">总收益率: {result.total_return*100:.2f}%</div>
    <div class="metric">年化收益率: {result.annual_return*100:.2f}%</div>
    <div class="metric">夏普比率: {result.sharpe_ratio:.2f}</div>
    <div class="metric">最大回撤: {result.max_drawdown*100:.2f}%</div>
    <div class="metric">胜率: {result.win_rate*100:.1f}%</div>
    <div class="metric">交易次数: {result.total_trades}</div>
    <div class="metric">回测时长: {result.duration_seconds:.2f}秒</div>
</body>
</html>
"""
            report_path.write_text(html, encoding='utf-8')
            logger.info(f"回测报告已生成: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            return None
    
    def run_batch_backtest(
        self,
        strategies: List[Dict[str, Any]],
        start_date: str,
        end_date: str,
    ) -> List[QMTResult]:
        """
        批量回测
        
        Args:
            strategies: 策略列表 [{"name": "...", "path": "...", "code": "..."}]
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            结果列表
        """
        results = []
        for i, strategy in enumerate(strategies):
            logger.info(f"回测策略 {i+1}/{len(strategies)}: {strategy.get('name', 'unknown')}")
            
            # 更新配置
            self.config.start_date = start_date
            self.config.end_date = end_date
            
            # 执行回测
            result = self.run_backtest(
                strategy_path=strategy.get("path"),
                strategy_code=strategy.get("code"),
            )
            results.append(result)
        
        return results
    
    def optimize(
        self,
        strategy_path: str,
        optimize_config: QMTOptimizeConfig,
        start_date: str,
        end_date: str,
    ) -> QMTOptimizeResult:
        """
        参数优化
        
        Args:
            strategy_path: 策略文件路径
            optimize_config: 优化配置
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            优化结果
        """
        start_time = time.time()
        
        # 获取参数组合
        param_combinations = optimize_config.get_param_combinations()
        
        best_result = None
        best_params = None
        best_score = float('-inf')
        all_results = []
        
        for i, params in enumerate(param_combinations):
            logger.info(f"优化迭代 {i+1}/{len(param_combinations)}: {params}")
            
            # TODO: 应用参数到策略
            # 这里需要根据策略代码动态修改参数
            
            # 执行回测
            self.config.start_date = start_date
            self.config.end_date = end_date
            result = self.run_backtest(strategy_path=strategy_path)
            
            # 获取目标指标
            score = getattr(result, optimize_config.target_metric, 0.0)
            
            all_results.append({
                "params": params,
                "score": score,
                "result": result,
            })
            
            # 更新最佳结果
            if score > best_score:
                best_score = score
                best_params = params
                best_result = result
        
        return QMTOptimizeResult(
            best_params=best_params or {},
            best_result=best_result,
            all_results=all_results,
            optimization_time=time.time() - start_time,
            iterations=len(param_combinations),
        )
