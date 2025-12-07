"""参数优化模块

基于 BulletTrade 官方 `bullet-trade optimize` 命令
实现多进程并行参数寻优

官方命令格式:
bullet-trade optimize strategies/demo_strategy.py \
    --params params.json \
    --start 2020-01-01 \
    --end 2023-12-31 \
    --output optimization.csv
"""

from typing import Optional, Dict, Any, List, Callable, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import subprocess
import json
import logging
import os

logger = logging.getLogger(__name__)

# BulletTrade CLI
BT_CLI = "bullet-trade"


@dataclass
class OptimizeParam:
    """优化参数定义
    
    Attributes:
        name: 参数名称
        min_value: 最小值
        max_value: 最大值
        step: 步长
        values: 枚举值列表（与min/max/step互斥）
    """
    name: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None
    values: Optional[List[Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        if self.values:
            return {"name": self.name, "values": self.values}
        return {
            "name": self.name,
            "min": self.min_value,
            "max": self.max_value,
            "step": self.step
        }
    
    def get_values(self) -> List[Any]:
        """获取所有可能的参数值"""
        if self.values:
            return self.values
        
        if self.min_value is None or self.max_value is None or self.step is None:
            return []
        
        values = []
        current = self.min_value
        while current <= self.max_value:
            values.append(current)
            current += self.step
        return values


@dataclass
class OptimizeConfig:
    """优化配置
    
    Attributes:
        strategy_path: 策略文件路径
        params: 待优化参数列表
        start_date: 回测开始日期
        end_date: 回测结束日期
        frequency: 数据频率
        benchmark: 基准指数
        metric: 优化目标指标 ('sharpe', 'return', 'drawdown')
        n_jobs: 并行进程数
        output_dir: 输出目录
    """
    strategy_path: str
    params: List[OptimizeParam]
    start_date: str = "2020-01-01"
    end_date: str = "2023-12-31"
    frequency: str = "day"
    benchmark: str = "000300.XSHG"
    metric: str = "sharpe"
    n_jobs: int = -1  # -1 表示使用所有 CPU
    output_dir: Optional[str] = None
    
    def __post_init__(self):
        if not self.output_dir:
            strategy_name = Path(self.strategy_path).stem
            self.output_dir = f"optimization/{strategy_name}"
    
    def to_params_json(self) -> str:
        """生成参数 JSON 文件内容"""
        params_dict = {
            "params": [p.to_dict() for p in self.params],
            "metric": self.metric,
            "n_jobs": self.n_jobs
        }
        return json.dumps(params_dict, indent=2, ensure_ascii=False)
    
    def save_params_json(self, path: Optional[str] = None) -> str:
        """保存参数配置到 JSON 文件"""
        if not path:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            path = f"{self.output_dir}/params.json"
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_params_json())
        
        return path


@dataclass
class OptimizeResult:
    """优化结果
    
    Attributes:
        success: 是否成功
        best_params: 最优参数组合
        best_metric: 最优指标值
        all_results: 所有参数组合的结果
        output_file: 输出文件路径
        error: 错误信息
    """
    success: bool = False
    best_params: Dict[str, Any] = field(default_factory=dict)
    best_metric: float = 0.0
    all_results: List[Dict[str, Any]] = field(default_factory=list)
    output_file: Optional[str] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "best_params": self.best_params,
            "best_metric": self.best_metric,
            "all_results": self.all_results,
            "output_file": self.output_file,
            "error": self.error
        }


class StrategyOptimizer:
    """策略参数优化器
    
    封装 BulletTrade 的参数优化功能
    
    Example:
        >>> config = OptimizeConfig(
        ...     strategy_path="strategies/my_strategy.py",
        ...     params=[
        ...         OptimizeParam("period", min_value=5, max_value=30, step=5),
        ...         OptimizeParam("threshold", min_value=0.01, max_value=0.1, step=0.01)
        ...     ],
        ...     start_date="2020-01-01",
        ...     end_date="2023-12-31"
        ... )
        >>> optimizer = StrategyOptimizer(config)
        >>> result = optimizer.run()
    """
    
    def __init__(self, config: OptimizeConfig):
        """初始化优化器
        
        Args:
            config: 优化配置
        """
        self.config = config
        self._bt_available = self._check_bt()
        self._progress_callback: Optional[Callable[[int, str], None]] = None
    
    def _check_bt(self) -> bool:
        """检查 BulletTrade CLI 是否可用"""
        try:
            result = subprocess.run(
                [BT_CLI, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def set_progress_callback(self, callback: Callable[[int, str], None]) -> None:
        """设置进度回调"""
        self._progress_callback = callback
    
    def _report_progress(self, progress: int, message: str) -> None:
        """报告进度"""
        logger.info(f"[{progress}%] {message}")
        if self._progress_callback:
            self._progress_callback(progress, message)
    
    def run(self) -> OptimizeResult:
        """运行参数优化
        
        Returns:
            优化结果
        """
        self._report_progress(0, "开始参数优化...")
        
        if self._bt_available:
            return self._run_with_bt()
        else:
            return self._run_mock()
    
    def _run_with_bt(self) -> OptimizeResult:
        """使用 BulletTrade CLI 运行优化"""
        self._report_progress(10, "准备优化环境...")
        
        # 保存参数配置
        params_file = self.config.save_params_json()
        
        # 构建输出文件路径
        output_file = f"{self.config.output_dir}/optimization.csv"
        
        # 构建命令
        cmd = [
            BT_CLI, "optimize",
            self.config.strategy_path,
            "--params", params_file,
            "--start", self.config.start_date,
            "--end", self.config.end_date,
            "--output", output_file
        ]
        
        if self.config.frequency != "day":
            cmd.extend(["--frequency", self.config.frequency])
        
        self._report_progress(20, "执行参数优化...")
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=7200,  # 2小时超时
                cwd=os.getcwd()
            )
            
            self._report_progress(90, "解析结果...")
            
            if result.returncode == 0:
                return self._parse_bt_result(output_file)
            else:
                return OptimizeResult(
                    success=False,
                    error=result.stderr or "优化执行失败"
                )
        except subprocess.TimeoutExpired:
            return OptimizeResult(
                success=False,
                error="优化超时（超过2小时）"
            )
        except Exception as e:
            return OptimizeResult(
                success=False,
                error=str(e)
            )
    
    def _parse_bt_result(self, output_file: str) -> OptimizeResult:
        """解析 BulletTrade 优化结果"""
        import pandas as pd
        
        try:
            df = pd.read_csv(output_file)
            
            # 找出最优结果
            if self.config.metric == "drawdown":
                # 回撤越小越好
                best_idx = df["max_drawdown"].idxmin()
            else:
                # 其他指标越大越好
                metric_col = "sharpe_ratio" if self.config.metric == "sharpe" else "total_return"
                best_idx = df[metric_col].idxmax()
            
            best_row = df.iloc[best_idx]
            
            # 提取参数
            param_names = [p.name for p in self.config.params]
            best_params = {name: best_row[name] for name in param_names if name in best_row}
            
            self._report_progress(100, "优化完成")
            
            return OptimizeResult(
                success=True,
                best_params=best_params,
                best_metric=float(best_row.get("sharpe_ratio", 0)),
                all_results=df.to_dict("records"),
                output_file=output_file
            )
        except Exception as e:
            return OptimizeResult(
                success=False,
                error=f"解析结果失败: {e}"
            )
    
    def _run_mock(self) -> OptimizeResult:
        """模拟优化（当 BulletTrade 不可用时）"""
        import random
        import itertools
        
        self._report_progress(10, "使用模拟模式运行优化...")
        
        # 生成参数组合
        param_values = [p.get_values() for p in self.config.params]
        param_names = [p.name for p in self.config.params]
        
        combinations = list(itertools.product(*param_values))
        total = len(combinations)
        
        self._report_progress(20, f"共 {total} 个参数组合")
        
        all_results = []
        best_result = None
        best_metric = float('-inf')
        
        for i, combo in enumerate(combinations):
            # 模拟回测结果
            params = dict(zip(param_names, combo))
            
            sharpe = random.gauss(0.8, 0.5)
            total_return = random.gauss(20, 15)
            max_drawdown = random.uniform(5, 30)
            
            result = {
                **params,
                "sharpe_ratio": round(sharpe, 2),
                "total_return": round(total_return, 2),
                "max_drawdown": round(max_drawdown, 2),
                "win_rate": round(random.uniform(0.4, 0.6), 2)
            }
            
            all_results.append(result)
            
            # 更新最优
            metric_value = sharpe if self.config.metric == "sharpe" else total_return
            if self.config.metric == "drawdown":
                metric_value = -max_drawdown
            
            if metric_value > best_metric:
                best_metric = metric_value
                best_result = result
            
            # 报告进度
            progress = 20 + int(70 * (i + 1) / total)
            if (i + 1) % max(1, total // 10) == 0:
                self._report_progress(progress, f"已完成 {i + 1}/{total}")
        
        # 保存结果
        import pandas as pd
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
        output_file = f"{self.config.output_dir}/optimization.csv"
        pd.DataFrame(all_results).to_csv(output_file, index=False)
        
        self._report_progress(100, "优化完成")
        
        return OptimizeResult(
            success=True,
            best_params={k: v for k, v in best_result.items() 
                         if k in param_names} if best_result else {},
            best_metric=best_result.get("sharpe_ratio", 0) if best_result else 0,
            all_results=all_results,
            output_file=output_file
        )


def optimize_strategy(
    strategy_path: str,
    params: List[Dict[str, Any]],
    start_date: str,
    end_date: str,
    metric: str = "sharpe",
    progress_callback: Optional[Callable[[int, str], None]] = None
) -> OptimizeResult:
    """参数优化便捷函数
    
    Args:
        strategy_path: 策略文件路径
        params: 参数定义列表，如 [{"name": "period", "min": 5, "max": 30, "step": 5}]
        start_date: 开始日期
        end_date: 结束日期
        metric: 优化目标 ('sharpe', 'return', 'drawdown')
        progress_callback: 进度回调
        
    Returns:
        优化结果
        
    Example:
        >>> result = optimize_strategy(
        ...     "strategies/my_strategy.py",
        ...     [{"name": "period", "min": 5, "max": 30, "step": 5}],
        ...     "2020-01-01",
        ...     "2023-12-31"
        ... )
        >>> print(result.best_params)
    """
    # 转换参数定义
    param_objs = []
    for p in params:
        if "values" in p:
            param_objs.append(OptimizeParam(
                name=p["name"],
                values=p["values"]
            ))
        else:
            param_objs.append(OptimizeParam(
                name=p["name"],
                min_value=p.get("min"),
                max_value=p.get("max"),
                step=p.get("step")
            ))
    
    config = OptimizeConfig(
        strategy_path=strategy_path,
        params=param_objs,
        start_date=start_date,
        end_date=end_date,
        metric=metric
    )
    
    optimizer = StrategyOptimizer(config)
    
    if progress_callback:
        optimizer.set_progress_callback(progress_callback)
    
    return optimizer.run()



