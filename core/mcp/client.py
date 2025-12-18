# -*- coding: utf-8 -*-
"""
MCP统一客户端
============

为GUI提供统一的MCP工具调用接口

功能:
- 同步/异步调用MCP工具
- 批量调用
- 进度回调
- 错误处理
- 结果缓存

使用示例:
    from core.mcp import get_mcp_client
    
    client = get_mcp_client()
    
    # 同步调用
    result = client.call("backtest.bullettrade", {
        "strategy_path": "path/to/strategy.py",
        "start_date": "2024-01-01",
        "end_date": "2024-06-30"
    })
    
    # 带进度回调
    result = client.call("backtest.bullettrade", args, 
        on_progress=lambda p, msg: print(f"{p}%: {msg}"))
"""

import logging
import json
import subprocess
import sys
import os
import asyncio
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future
import threading

logger = logging.getLogger(__name__)


@dataclass
class MCPResult:
    """MCP调用结果"""
    success: bool = False
    data: Any = None
    error: Optional[str] = None
    trace_id: str = ""
    duration: float = 0.0
    tool_name: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "trace_id": self.trace_id,
            "duration": self.duration,
            "tool_name": self.tool_name
        }


@dataclass
class BacktestProgress:
    """回测进度"""
    task_id: str
    status: str = "pending"  # pending, running, completed, failed
    progress: int = 0
    message: str = ""
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    result: Optional[MCPResult] = None


class MCPClient:
    """
    MCP统一客户端
    
    封装所有MCP服务器的调用逻辑
    """
    
    # MCP工具到服务器的映射
    TOOL_SERVER_MAP = {
        # backtest_server
        "backtest.bullettrade": "backtest-server",
        "backtest.bullettrade_batch": "backtest-server",
        "backtest.bullettrade_optimize": "backtest-server",
        "backtest.qmt": "backtest-server",
        "backtest.qmt_batch": "backtest-server",
        "backtest.qmt_optimize": "backtest-server",
        "backtest.quick": "backtest-server",
        "backtest.compare": "backtest-server",
        "backtest.status": "backtest-server",
        "backtest.logs": "backtest-server",
        
        # factor_server
        "factor.list": "factor-server",
        "factor.recommend": "factor-server",
        "factor.ic_analysis": "factor-server",
        "factor.evaluate": "factor-server",
        "factor.decay": "factor-server",
        
        # optimizer_server
        "optimizer.optuna": "optimizer-server",
        "optimizer.multi_objective": "optimizer-server",
        "optimizer.grid_search": "optimizer-server",
        "optimizer.sensitivity": "optimizer-server",
        
        # workflow_9steps_server
        "workflow9.get_steps": "workflow_9steps_server",
        "workflow9.create": "workflow_9steps_server",
        "workflow9.status": "workflow_9steps_server",
        "workflow9.run_step": "workflow_9steps_server",
        "workflow9.run_all": "workflow_9steps_server",
        "workflow9.get_context": "workflow_9steps_server",
        
        # workflow_server (legacy)
        "workflow.run_step": "workflow-server",
        "workflow.status": "workflow-server",
        "workflow.resume": "workflow-server",
        "workflow.list": "workflow-server",
        
        # market_server
        "trquant.market_status": "trquant-server",
        "trquant.mainlines": "trquant-server",
        
        # strategy_template_server
        "strategy.list": "strategy-template-server",
        "strategy.get": "strategy-template-server",
        "strategy.generate": "strategy-template-server",
        "strategy.templates": "strategy-template-server",
        
        # report_server
        "report.generate": "report-server",
        "report.visualize": "report-server",
        "report.archive": "report-server",
        "report.list": "report-server",
    }
    
    def __init__(self, project_root: Optional[Path] = None, python_path: Optional[str] = None):
        """
        初始化MCP客户端
        
        Args:
            project_root: 项目根目录
            python_path: Python解释器路径（可选，默认使用sys.executable）
        """
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        self.project_root = project_root
        self.mcp_servers_dir = project_root / "mcp_servers"
        
        # Python解释器路径
        # 优先使用传入的路径，否则尝试查找工作区venv，最后使用sys.executable
        if python_path:
            self.python_path = python_path
        else:
            self.python_path = self._find_python_path()
        
        # 线程池用于异步调用
        self._executor = ThreadPoolExecutor(max_workers=4)
        
        # 任务管理
        self._tasks: Dict[str, BacktestProgress] = {}
        self._task_lock = threading.Lock()
        
        # 结果缓存
        self._cache: Dict[str, MCPResult] = {}
        self._cache_ttl = 300  # 5分钟缓存
        
        logger.info(f"MCPClient初始化完成: {self.project_root}, Python: {self.python_path}")
    
    def _find_python_path(self) -> str:
        """查找Python解释器路径，优先使用工作区venv"""
        import platform
        
        # 1. 检查工作区路径下的 extension/venv
        venv_path = self.project_root / "extension" / "venv"
        if platform.system() == "Windows":
            python_exe = venv_path / "Scripts" / "python.exe"
        else:
            python_exe = venv_path / "bin" / "python"
        
        if python_exe.exists():
            logger.info(f"找到工作区venv: {python_exe}")
            return str(python_exe)
        
        # 2. 检查环境变量TRQUANT_ROOT下的venv
        trquant_root = os.environ.get("TRQUANT_ROOT")
        if trquant_root:
            trquant_venv = Path(trquant_root) / "extension" / "venv"
            if platform.system() == "Windows":
                python_exe = trquant_venv / "Scripts" / "python.exe"
            else:
                python_exe = trquant_venv / "bin" / "python"
            
            if python_exe.exists():
                logger.info(f"找到TRQUANT_ROOT venv: {python_exe}")
                return str(python_exe)
        
        # 3. 回退到sys.executable
        logger.info(f"使用系统Python: {sys.executable}")
        return sys.executable
    
    def call(self, 
             tool_name: str, 
             arguments: Dict[str, Any],
             on_progress: Optional[Callable[[int, str], None]] = None,
             use_cache: bool = False,
             timeout: float = 300.0) -> MCPResult:
        """
        同步调用MCP工具
        
        Args:
            tool_name: 工具名称，如 "backtest.bullettrade"
            arguments: 工具参数
            on_progress: 进度回调函数 (progress_percent, message)
            use_cache: 是否使用缓存
            timeout: 超时时间（秒）
            
        Returns:
            MCPResult
        """
        start_time = datetime.now()
        trace_id = str(uuid.uuid4())[:8]
        
        logger.info(f"[{trace_id}] 调用MCP工具: {tool_name}")
        
        # 检查缓存
        if use_cache:
            cache_key = f"{tool_name}:{json.dumps(arguments, sort_keys=True)}"
            if cache_key in self._cache:
                cached = self._cache[cache_key]
                logger.info(f"[{trace_id}] 返回缓存结果")
                return cached
        
        if on_progress:
            on_progress(0, "开始调用MCP工具...")
        
        try:
            # 根据工具名确定调用方式
            if tool_name.startswith("backtest.") or tool_name.startswith("optimizer."):
                # 回测和优化类工具，直接调用Python模块
                result = self._call_python_module(tool_name, arguments, on_progress)
            else:
                # 其他工具，通过subprocess调用MCP服务器
                result = self._call_mcp_server(tool_name, arguments, timeout)
            
            duration = (datetime.now() - start_time).total_seconds()
            
            mcp_result = MCPResult(
                success=True,
                data=result,
                trace_id=trace_id,
                duration=duration,
                tool_name=tool_name
            )
            
            if on_progress:
                on_progress(100, "调用完成")
            
            # 缓存结果
            if use_cache:
                self._cache[cache_key] = mcp_result
            
            logger.info(f"[{trace_id}] 调用成功, 耗时: {duration:.2f}秒")
            return mcp_result
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"[{trace_id}] 调用失败: {e}")
            
            return MCPResult(
                success=False,
                error=str(e),
                trace_id=trace_id,
                duration=duration,
                tool_name=tool_name
            )
    
    def call_async(self,
                   tool_name: str,
                   arguments: Dict[str, Any],
                   on_complete: Optional[Callable[[MCPResult], None]] = None,
                   on_progress: Optional[Callable[[int, str], None]] = None) -> str:
        """
        异步调用MCP工具
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            on_complete: 完成回调
            on_progress: 进度回调
            
        Returns:
            task_id
        """
        task_id = str(uuid.uuid4())[:8]
        
        with self._task_lock:
            self._tasks[task_id] = BacktestProgress(
                task_id=task_id,
                status="pending",
                started_at=datetime.now()
            )
        
        def _run():
            with self._task_lock:
                self._tasks[task_id].status = "running"
            
            result = self.call(tool_name, arguments, on_progress)
            
            with self._task_lock:
                self._tasks[task_id].status = "completed" if result.success else "failed"
                self._tasks[task_id].finished_at = datetime.now()
                self._tasks[task_id].result = result
            
            if on_complete:
                on_complete(result)
        
        self._executor.submit(_run)
        
        logger.info(f"异步任务已提交: {task_id}")
        return task_id
    
    def batch_call(self, 
                   calls: List[Tuple[str, Dict[str, Any]]],
                   parallel: bool = True) -> List[MCPResult]:
        """
        批量调用MCP工具
        
        Args:
            calls: 调用列表 [(tool_name, arguments), ...]
            parallel: 是否并行执行
            
        Returns:
            结果列表
        """
        if parallel:
            futures = []
            for tool_name, arguments in calls:
                future = self._executor.submit(self.call, tool_name, arguments)
                futures.append(future)
            
            return [f.result() for f in futures]
        else:
            return [self.call(tool_name, arguments) for tool_name, arguments in calls]
    
    def get_task_status(self, task_id: str) -> Optional[BacktestProgress]:
        """获取异步任务状态"""
        with self._task_lock:
            return self._tasks.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """取消异步任务（注意：已经运行的任务可能无法取消）"""
        with self._task_lock:
            if task_id in self._tasks:
                self._tasks[task_id].status = "cancelled"
                return True
        return False
    
    def _call_python_module(self, 
                            tool_name: str, 
                            arguments: Dict[str, Any],
                            on_progress: Optional[Callable] = None) -> Dict:
        """直接调用Python模块"""
        
        if tool_name == "backtest.bullettrade":
            return self._run_bullettrade_backtest(arguments, on_progress)
        elif tool_name == "backtest.qmt":
            return self._run_qmt_backtest(arguments, on_progress)
        elif tool_name == "optimizer.optuna":
            return self._run_optuna_optimize(arguments, on_progress)
        elif tool_name.startswith("backtest."):
            return self._run_generic_backtest(tool_name, arguments, on_progress)
        else:
            raise ValueError(f"未知的Python模块工具: {tool_name}")
    
    def _run_bullettrade_backtest(self, 
                                   arguments: Dict[str, Any],
                                   on_progress: Optional[Callable] = None) -> Dict:
        """运行BulletTrade回测"""
        try:
            from core.bullettrade import BulletTradeEngine, BTConfig
            
            if on_progress:
                on_progress(10, "初始化BulletTrade引擎...")
            
            config = BTConfig(
                start_date=arguments["start_date"],
                end_date=arguments["end_date"],
                initial_capital=arguments.get("initial_capital", 1000000),
                benchmark=arguments.get("benchmark", "000300.XSHG"),
            )
            
            if on_progress:
                on_progress(20, "配置完成，开始回测...")
            
            engine = BulletTradeEngine(config)
            result = engine.run_backtest(
                strategy_path=arguments.get("strategy_path"),
                strategy_code=arguments.get("strategy_code")
            )
            
            if on_progress:
                on_progress(90, "回测完成，处理结果...")
            
            return {
                "success": result.success,
                "message": result.message,
                "total_return": result.total_return,
                "annual_return": result.annual_return,
                "sharpe_ratio": result.sharpe_ratio,
                "max_drawdown": result.max_drawdown,
                "win_rate": result.win_rate,
                "total_trades": result.total_trades,
                "report_path": result.report_path
            }
            
        except ImportError as e:
            logger.warning(f"BulletTrade模块不可用: {e}")
            return {"success": False, "error": f"BulletTrade模块不可用: {e}"}
        except Exception as e:
            logger.error(f"BulletTrade回测失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _run_qmt_backtest(self,
                          arguments: Dict[str, Any],
                          on_progress: Optional[Callable] = None) -> Dict:
        """运行QMT回测"""
        try:
            from core.qmt import QMTEngine, QMTConfig
            
            if on_progress:
                on_progress(10, "初始化QMT引擎...")
            
            config = QMTConfig(
                start_date=arguments["start_date"],
                end_date=arguments["end_date"],
                initial_capital=arguments.get("initial_capital", 1000000),
                benchmark=arguments.get("benchmark", "000300.SH"),
            )
            
            if on_progress:
                on_progress(20, "配置完成，开始回测...")
            
            engine = QMTEngine(config)
            result = engine.run_backtest(
                strategy_path=arguments.get("strategy_path"),
                strategy_code=arguments.get("strategy_code")
            )
            
            if on_progress:
                on_progress(90, "回测完成，处理结果...")
            
            return {
                "success": result.success,
                "message": result.message,
                "total_return": result.total_return,
                "annual_return": result.annual_return,
                "sharpe_ratio": result.sharpe_ratio,
                "max_drawdown": result.max_drawdown,
                "win_rate": result.win_rate,
                "trade_count": result.trade_count,
                "report_path": result.report_path
            }
            
        except ImportError as e:
            logger.warning(f"QMT模块不可用: {e}")
            return {"success": False, "error": f"QMT模块不可用: {e}"}
        except Exception as e:
            logger.error(f"QMT回测失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _run_optuna_optimize(self,
                             arguments: Dict[str, Any],
                             on_progress: Optional[Callable] = None) -> Dict:
        """运行Optuna优化"""
        try:
            from core.optimization import OptunaOptimizer
            
            if on_progress:
                on_progress(10, "初始化Optuna优化器...")
            
            optimizer = OptunaOptimizer(
                direction=arguments.get("direction", "maximize")
            )
            
            # 构建目标函数
            strategy_path = arguments.get("strategy_path")
            start_date = arguments.get("start_date")
            end_date = arguments.get("end_date")
            
            def objective(params):
                # 修改策略参数并回测
                backtest_result = self._run_bullettrade_backtest({
                    "strategy_path": strategy_path,
                    "start_date": start_date,
                    "end_date": end_date,
                    **params
                })
                
                target_metric = arguments.get("target_metric", "sharpe_ratio")
                return backtest_result.get(target_metric, 0)
            
            if on_progress:
                on_progress(20, "开始优化...")
            
            result = optimizer.optimize(
                objective,
                arguments.get("params_to_optimize", {}),
                n_trials=arguments.get("n_trials", 50)
            )
            
            if on_progress:
                on_progress(90, "优化完成...")
            
            return {
                "success": True,
                "best_params": result.best_params,
                "best_value": result.best_value,
                "n_trials": result.n_trials,
                "optimization_time": result.optimization_time
            }
            
        except ImportError as e:
            logger.warning(f"Optuna模块不可用: {e}")
            return {"success": False, "error": f"Optuna模块不可用: {e}"}
        except Exception as e:
            logger.error(f"Optuna优化失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _run_generic_backtest(self,
                              tool_name: str,
                              arguments: Dict[str, Any],
                              on_progress: Optional[Callable] = None) -> Dict:
        """运行通用回测"""
        if "bullettrade" in tool_name:
            return self._run_bullettrade_backtest(arguments, on_progress)
        elif "qmt" in tool_name:
            return self._run_qmt_backtest(arguments, on_progress)
        else:
            return {"success": False, "error": f"未知的回测类型: {tool_name}"}
    

    def _call_workflow9_direct(self, tool_name: str, arguments: Dict[str, Any]) -> Dict:
        """直接调用workflow9服务器（避免subprocess问题）"""
        import sys
        import asyncio
        
        # 确保路径正确
        sys.path.insert(0, str(self.project_root))
        sys.path.insert(0, str(self.mcp_servers_dir))
        
        from workflow_9steps_server import _handle_tool
        
        # 运行异步函数
        loop = asyncio.new_event_loop()
        try:
            result = loop.run_until_complete(_handle_tool(tool_name, arguments))
            return result
        finally:
            loop.close()
    
    def _call_mcp_server(self,
                         tool_name: str,
                         arguments: Dict[str, Any],
                         timeout: float = 60.0) -> Dict:
        """通过subprocess调用MCP服务器"""
        
        # workflow9.* 工具使用直接调用方式
        if tool_name.startswith("workflow9."):
            return self._call_workflow9_direct(tool_name, arguments)
        
        # 确定服务器文件
        server_name = self.TOOL_SERVER_MAP.get(tool_name)
        if not server_name:
            # 尝试从工具名推断
            prefix = tool_name.split(".")[0]
            server_file = self.mcp_servers_dir / f"{prefix}_server.py"
        else:
            server_file = self.mcp_servers_dir / f"{server_name.replace('-', '_')}.py"
        
        if not server_file.exists():
            raise FileNotFoundError(f"MCP服务器文件不存在: {server_file}")
        
        # 构建调用请求
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": 1
        }
        
        # 调用服务器
        try:
            result = subprocess.run(
                [self.python_path, str(server_file)],
                input=json.dumps(request),
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.project_root)
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"MCP服务器返回错误: {result.stderr}")
            
            response = json.loads(result.stdout)
            return response.get("result", {})
            
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"MCP调用超时: {tool_name}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"MCP响应解析失败: {e}")
    
    def clear_cache(self):
        """清除缓存"""
        self._cache.clear()
        logger.info("缓存已清除")
    
    def dispose(self):
        """释放资源"""
        self._executor.shutdown(wait=False)
        logger.info("MCPClient已释放")


# 全局实例
_mcp_client: Optional[MCPClient] = None


def get_mcp_client() -> MCPClient:
    """获取全局MCP客户端实例"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client
