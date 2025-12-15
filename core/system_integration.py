# -*- coding: utf-8 -*-
"""
系统集成层
=========
整合所有核心模块，提供统一的系统入口：
- 数据获取
- 工作流管理
- 回测执行
- 策略进化

使用方式：
    from core.system_integration import TRQuantSystem
    
    system = TRQuantSystem()
    system.run_workflow()
"""

import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class TRQuantSystem:
    """韬睿量化系统统一入口"""
    
    def __init__(self):
        self._data_provider = None
        self._state_manager = None
        self._backtest_engine = None
        self._batch_manager = None
        self._evolver = None
        self._orchestrator = None
        
        self._init_components()
    
    def _init_components(self):
        """初始化所有组件"""
        # 数据提供者
        try:
            from core.data.unified_data_provider import get_data_provider
            self._data_provider = get_data_provider()
            logger.info("✅ 数据提供者已初始化")
        except Exception as e:
            logger.warning(f"数据提供者初始化失败: {e}")
        
        # 状态管理器
        try:
            from core.workflow.state_manager import get_state_manager
            self._state_manager = get_state_manager()
            logger.info("✅ 状态管理器已初始化")
        except Exception as e:
            logger.warning(f"状态管理器初始化失败: {e}")
        
        # 工作流编排器
        try:
            from core.workflow_orchestrator import WorkflowOrchestrator
            self._orchestrator = WorkflowOrchestrator()
            logger.info("✅ 工作流编排器已初始化")
        except Exception as e:
            logger.warning(f"工作流编排器初始化失败: {e}")
    
    def get_data(self, securities: List[str], start_date: str, end_date: str, 
                 frequency: str = "daily") -> Optional[Any]:
        """获取数据（统一接口）"""
        if not self._data_provider:
            logger.error("数据提供者未初始化")
            return None
        
        from core.data.unified_data_provider import DataRequest
        request = DataRequest(
            securities=securities,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency
        )
        response = self._data_provider.get_data(request)
        return response.data if response.success else None
    
    def run_workflow(self, name: str = "8步骤工作流") -> Dict:
        """运行完整工作流"""
        if not self._orchestrator:
            return {"success": False, "error": "工作流编排器未初始化"}
        
        # 创建工作流状态
        workflow_id = None
        if self._state_manager:
            workflow = self._state_manager.create_workflow(name)
            workflow_id = workflow.workflow_id
            logger.info(f"创建工作流: {workflow_id}")
        
        # 运行工作流
        result = self._orchestrator.run_full_workflow()
        
        return {
            "success": result.success,
            "workflow_id": workflow_id,
            "steps": [{"name": s.step_name, "success": s.success} for s in result.steps],
            "strategy_file": result.strategy_file,
            "total_time": result.total_time
        }
    
    def resume_workflow(self, workflow_id: str) -> Dict:
        """恢复工作流"""
        if not self._state_manager:
            return {"success": False, "error": "状态管理器未初始化"}
        
        step_index = self._state_manager.resume_workflow(workflow_id)
        if step_index < 0:
            return {"success": True, "message": "工作流已完成"}
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "resume_from_step": step_index
        }
    
    def quick_backtest(self, securities: List[str], start_date: str, end_date: str,
                       strategy: str = "momentum", **params) -> Dict:
        """快速回测"""
        try:
            from core.backtest.fast_backtest_engine import quick_backtest
            result = quick_backtest(securities, start_date, end_date, strategy, **params)
            return {
                "success": True,
                "total_return": result.total_return,
                "annual_return": result.annual_return,
                "sharpe_ratio": result.sharpe_ratio,
                "max_drawdown": result.max_drawdown,
                "win_rate": result.win_rate,
                "duration_seconds": result.duration_seconds
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def grid_search(self, securities: List[str], start_date: str, end_date: str,
                   strategy: str, param_grid: Dict) -> Dict:
        """参数网格搜索"""
        try:
            from core.backtest.batch_backtest_manager import BatchBacktestManager
            manager = BatchBacktestManager()
            results = manager.grid_search(securities, start_date, end_date, strategy, param_grid)
            
            best = manager.get_ranking("sharpe_ratio")[0] if results else None
            return {
                "success": True,
                "total_combinations": len(results),
                "best_params": best.config.params if best else None,
                "best_sharpe": best.sharpe_ratio if best else 0,
                "best_return": best.total_return if best else 0
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def evolve_strategy(self, securities: List[str], start_date: str, end_date: str,
                       strategy: str = "momentum", generations: int = 10) -> Dict:
        """策略进化"""
        try:
            from core.evolution.strategy_evolver import StrategyEvolver, EvolutionConfig
            
            config = EvolutionConfig(generations=generations)
            evolver = StrategyEvolver(config)
            best = evolver.evolve(securities, start_date, end_date, strategy)
            
            return {
                "success": True,
                "best_params": best.params if best else None,
                "best_fitness": best.fitness if best else 0,
                "generations": generations,
                "history": evolver.history
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        status = {
            "data_provider": "ready" if self._data_provider else "unavailable",
            "state_manager": "ready" if self._state_manager else "unavailable",
            "orchestrator": "ready" if self._orchestrator else "unavailable",
        }
        
        # 数据统计
        if self._data_provider:
            stats = self._data_provider.get_stats()
            status["data_stats"] = stats
        
        return status


# 全局单例
_system: Optional[TRQuantSystem] = None

def get_system() -> TRQuantSystem:
    """获取系统实例"""
    global _system
    if _system is None:
        _system = TRQuantSystem()
    return _system
