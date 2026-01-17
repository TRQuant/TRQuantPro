"""
参数优化工具
============
集成Optuna进行策略参数优化
"""

import optuna
from typing import Dict, Callable, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


def optimize_strategy_params(
    objective_func: Callable,
    param_space: Dict[str, Any],
    n_trials: int = 100,
    direction: str = "maximize",
    study_name: Optional[str] = None,
    storage: Optional[str] = None
) -> Dict:
    """
    使用Optuna优化策略参数
    
    Args:
        objective_func: 目标函数，接受trial参数，返回要优化的值
        param_space: 参数空间定义（可选，如果objective_func内部定义则可为空）
        n_trials: 试验次数
        direction: 优化方向（"maximize" 或 "minimize"）
        study_name: 研究名称（用于持久化）
        storage: 存储路径（SQLite数据库路径）
    
    Returns:
        Dict: 优化结果，包含最佳参数、最佳值、试验历史等
    """
    try:
        # 创建或加载研究
        if storage:
            study = optuna.create_study(
                direction=direction,
                study_name=study_name,
                storage=storage,
                load_if_exists=True
            )
        else:
            study = optuna.create_study(direction=direction, study_name=study_name)
        
        # 执行优化
        study.optimize(objective_func, n_trials=n_trials, show_progress_bar=True)
        
        return {
            "success": True,
            "best_params": study.best_params,
            "best_value": study.best_value,
            "n_trials": len(study.trials),
            "study": study
        }
        
    except Exception as e:
        logger.error(f"参数优化失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def create_optuna_study(
    direction: str = "maximize",
    study_name: Optional[str] = None,
    storage: Optional[str] = None
) -> optuna.Study:
    """
    创建Optuna研究对象
    
    Args:
        direction: 优化方向
        study_name: 研究名称
        storage: 存储路径
    
    Returns:
        optuna.Study: 研究对象
    """
    if storage:
        return optuna.create_study(
            direction=direction,
            study_name=study_name,
            storage=storage,
            load_if_exists=True
        )
    else:
        return optuna.create_study(direction=direction, study_name=study_name)


def suggest_params(trial: optuna.Trial, param_space: Dict[str, Any]) -> Dict[str, Any]:
    """
    根据参数空间定义建议参数值
    
    Args:
        trial: Optuna trial对象
        param_space: 参数空间定义
            {
                "param_name": {
                    "type": "float" | "int" | "categorical",
                    "low": float,
                    "high": float,
                    "log": bool (仅float/int),
                    "choices": List (仅categorical)
                }
            }
    
    Returns:
        Dict: 参数字典
    """
    params = {}
    
    for param_name, param_def in param_space.items():
        param_type = param_def.get("type", "float")
        
        if param_type == "float":
            params[param_name] = trial.suggest_float(
                param_name,
                param_def["low"],
                param_def["high"],
                log=param_def.get("log", False)
            )
        elif param_type == "int":
            params[param_name] = trial.suggest_int(
                param_name,
                param_def["low"],
                param_def["high"],
                log=param_def.get("log", False)
            )
        elif param_type == "categorical":
            params[param_name] = trial.suggest_categorical(
                param_name,
                param_def["choices"]
            )
        else:
            raise ValueError(f"未知的参数类型: {param_type}")
    
    return params


def get_optimization_history(study: optuna.Study) -> Dict:
    """
    获取优化历史
    
    Args:
        study: Optuna研究对象
    
    Returns:
        Dict: 优化历史数据
    """
    trials = study.trials
    
    return {
        "n_trials": len(trials),
        "best_trial": {
            "number": study.best_trial.number,
            "value": study.best_trial.value,
            "params": study.best_trial.params
        },
        "trials": [
            {
                "number": t.number,
                "value": t.value,
                "params": t.params,
                "state": str(t.state)
            }
            for t in trials
        ]
    }

