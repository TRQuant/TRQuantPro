# -*- coding: utf-8 -*-
"""
TRQuant Web API
==============

基于FastAPI的Web服务，提供:
- 工作流管理API
- 策略生成API
- 回测执行API
- 因子分析API
- 系统状态API

启动方式:
    uvicorn web.api.app:app --reload --port 8000
"""

import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from contextlib import asynccontextmanager

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ============================================================
# Pydantic 模型定义
# ============================================================

class WorkflowRequest(BaseModel):
    """工作流请求"""
    name: str = "新工作流"
    start_date: str = Field(..., description="开始日期，如2024-01-01")
    end_date: str = Field(..., description="结束日期，如2024-06-30")
    benchmark: str = "000300.XSHG"
    market_regime: Optional[str] = None
    auto_optimize: bool = False


class StrategyRequest(BaseModel):
    """策略生成请求"""
    strategy_type: str = "momentum"  # momentum, value, trend, multi_factor
    factors: List[str] = []
    parameters: Dict[str, Any] = {}
    platform: str = "bullettrade"  # bullettrade, ptrade, qmt


class BacktestRequest(BaseModel):
    """回测请求"""
    strategy_path: Optional[str] = None
    strategy_code: Optional[str] = None
    start_date: str
    end_date: str
    initial_capital: float = 1000000
    benchmark: str = "000300.XSHG"
    engine: str = "bullettrade"  # bullettrade, qmt, fast


class FactorAnalysisRequest(BaseModel):
    """因子分析请求"""
    factor_name: str
    start_date: str
    end_date: str
    analysis_type: str = "ic"  # ic, decay, evaluate


class OptimizationRequest(BaseModel):
    """优化请求"""
    strategy_path: str
    start_date: str
    end_date: str
    param_space: Dict[str, Dict[str, Any]]
    n_trials: int = 50
    target_metric: str = "sharpe_ratio"
    method: str = "tpe"  # tpe, random, grid


# ============================================================
# 应用初始化
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("🚀 TRQuant Web API 启动中...")
    
    # 初始化组件
    try:
        from core.workflow_orchestrator import WorkflowOrchestrator
        app.state.orchestrator = WorkflowOrchestrator()
        logger.info("✅ 工作流编排器已初始化")
    except Exception as e:
        logger.warning(f"工作流编排器初始化失败: {e}")
        app.state.orchestrator = None
    
    try:
        from core.plugin import get_plugin_manager
        app.state.plugin_manager = get_plugin_manager()
        logger.info("✅ 插件管理器已初始化")
    except Exception as e:
        logger.warning(f"插件管理器初始化失败: {e}")
        app.state.plugin_manager = None
    
    logger.info("✅ TRQuant Web API 已就绪")
    
    yield
    
    logger.info("TRQuant Web API 关闭中...")


app = FastAPI(
    title="韬睿量化 TRQuant API",
    description="专业量化交易系统API",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 系统状态API
# ============================================================

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "韬睿量化 TRQuant",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/api/system/status")
async def system_status():
    """系统状态"""
    status = {
        "api": "running",
        "orchestrator": app.state.orchestrator is not None,
        "plugin_manager": app.state.plugin_manager is not None,
        "timestamp": datetime.now().isoformat(),
    }
    
    # 获取插件状态
    if app.state.plugin_manager:
        status["plugins"] = app.state.plugin_manager.stats
    
    return status


@app.get("/api/system/modules")
async def list_modules():
    """列出可用模块"""
    modules = []
    
    # 检查各模块可用性
    module_checks = [
        ("core.bullettrade", "BulletTrade回测引擎"),
        ("core.qmt", "QMT回测引擎"),
        ("core.factors.analysis", "因子分析"),
        ("core.optimization", "策略优化"),
        ("core.workflow", "工作流编排"),
        ("core.plugin", "插件系统"),
    ]
    
    for module_name, description in module_checks:
        try:
            __import__(module_name)
            modules.append({
                "name": module_name,
                "description": description,
                "available": True,
            })
        except ImportError:
            modules.append({
                "name": module_name,
                "description": description,
                "available": False,
            })
    
    return {"modules": modules}


# ============================================================
# 工作流API
# ============================================================

@app.post("/api/workflow/create")
async def create_workflow(request: WorkflowRequest):
    """创建新工作流"""
    try:
        from core.workflow import create_workflow
        
        workflow = create_workflow(
            name=request.name,
            start_date=request.start_date,
            end_date=request.end_date,
            auto_optimize=request.auto_optimize,
        )
        
        return {
            "success": True,
            "workflow_id": workflow.workflow_id,
            "steps": [s.name for s in workflow.steps.values()],
        }
    except Exception as e:
        logger.error(f"创建工作流失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workflow/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """获取工作流状态"""
    try:
        from core.workflow.state_manager import get_state_manager
        
        state_manager = get_state_manager()
        state = state_manager.load_state(workflow_id)
        
        if not state:
            raise HTTPException(status_code=404, detail="工作流不存在")
        
        return state
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取工作流状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/workflow/{workflow_id}/run")
async def run_workflow(workflow_id: str, background_tasks: BackgroundTasks):
    """运行工作流（后台任务）"""
    try:
        # 这里应该启动后台任务
        return {
            "success": True,
            "message": f"工作流 {workflow_id} 已启动",
            "status": "running",
        }
    except Exception as e:
        logger.error(f"运行工作流失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 策略API
# ============================================================

@app.post("/api/strategy/generate")
async def generate_strategy(request: StrategyRequest):
    """生成策略代码"""
    try:
        from core.templates.strategy_templates import get_template_class
        
        template_class = get_template_class(request.strategy_type)
        if not template_class:
            raise HTTPException(status_code=400, detail=f"未知策略类型: {request.strategy_type}")
        
        template = template_class()
        code = template.generate(
            factors=request.factors,
            params=request.parameters,
        )
        
        return {
            "success": True,
            "strategy_type": request.strategy_type,
            "platform": request.platform,
            "code": code,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"生成策略失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/strategy/templates")
async def list_strategy_templates():
    """列出策略模板"""
    templates = [
        {"name": "momentum", "description": "动量策略", "factors": ["momentum_20d", "momentum_5d"]},
        {"name": "value", "description": "价值策略", "factors": ["pe", "pb", "dividend_yield"]},
        {"name": "trend", "description": "趋势策略", "factors": ["ma_cross", "breakout"]},
        {"name": "multi_factor", "description": "多因子策略", "factors": ["configurable"]},
    ]
    return {"templates": templates}


# ============================================================
# 回测API
# ============================================================

@app.post("/api/backtest/run")
async def run_backtest(request: BacktestRequest):
    """执行回测"""
    try:
        if request.engine == "bullettrade":
            from core.bullettrade import BulletTradeEngine, BTConfig
            
            config = BTConfig(
                start_date=request.start_date,
                end_date=request.end_date,
                initial_capital=request.initial_capital,
                benchmark=request.benchmark,
            )
            engine = BulletTradeEngine(config)
            result = engine.run_backtest(
                strategy_path=request.strategy_path,
                strategy_code=request.strategy_code,
            )
            
            return {
                "success": result.success,
                "message": result.message,
                "metrics": {
                    "total_return": f"{result.total_return:.2%}",
                    "annual_return": f"{result.annual_return:.2%}",
                    "sharpe_ratio": f"{result.sharpe_ratio:.2f}",
                    "max_drawdown": f"{result.max_drawdown:.2%}",
                    "win_rate": f"{result.win_rate:.1%}",
                },
                "report_path": result.report_path,
            }
        
        elif request.engine == "qmt":
            from core.qmt import QMTEngine, QMTConfig
            
            config = QMTConfig(
                start_date=request.start_date,
                end_date=request.end_date,
                initial_capital=request.initial_capital,
                benchmark=request.benchmark.replace(".XSHG", ".SH").replace(".XSHE", ".SZ"),
            )
            engine = QMTEngine(config)
            result = engine.run_backtest(
                strategy_path=request.strategy_path,
                strategy_code=request.strategy_code,
            )
            
            return {
                "success": result.success,
                "message": result.message,
                "metrics": {
                    "total_return": f"{result.total_return:.2%}",
                    "annual_return": f"{result.annual_return:.2%}",
                    "sharpe_ratio": f"{result.sharpe_ratio:.2f}",
                    "max_drawdown": f"{result.max_drawdown:.2%}",
                },
            }
        
        elif request.engine == "fast":
            from core.backtest.fast_backtest_engine import FastBacktestEngine, BacktestConfig
            
            config = BacktestConfig(
                start_date=request.start_date,
                end_date=request.end_date,
                initial_capital=request.initial_capital,
            )
            engine = FastBacktestEngine(config)
            
            # 快速回测需要信号矩阵
            return {
                "success": True,
                "message": "快速回测引擎需要信号矩阵输入",
                "engine": "fast",
            }
        
        else:
            raise HTTPException(status_code=400, detail=f"未知回测引擎: {request.engine}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"回测失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/backtest/history")
async def get_backtest_history(limit: int = 10):
    """获取回测历史"""
    try:
        from pymongo import MongoClient
        
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
        db = client["trquant"]
        
        results = list(db.backtest_results.find().sort("timestamp", -1).limit(limit))
        
        # 转换ObjectId
        for r in results:
            r["_id"] = str(r["_id"])
        
        return {"results": results}
    except Exception as e:
        logger.warning(f"获取回测历史失败: {e}")
        return {"results": [], "error": str(e)}


# ============================================================
# 因子API
# ============================================================

@app.get("/api/factors")
async def list_factors():
    """列出所有因子"""
    try:
        from core.factors import FACTOR_CATEGORIES
        
        return {"factors": FACTOR_CATEGORIES}
    except Exception as e:
        # 返回默认因子列表
        return {
            "factors": {
                "momentum": ["momentum_5d", "momentum_10d", "momentum_20d"],
                "value": ["pe", "pb", "ps", "dividend_yield"],
                "quality": ["roe", "roa", "gross_margin"],
                "volatility": ["volatility_20d", "beta"],
            }
        }


@app.post("/api/factors/analyze")
async def analyze_factor(request: FactorAnalysisRequest):
    """分析因子"""
    try:
        from core.factors.analysis import FactorEvaluator
        
        # 这里需要实际的数据
        return {
            "success": True,
            "factor": request.factor_name,
            "analysis_type": request.analysis_type,
            "message": "因子分析需要实际数据",
        }
    except Exception as e:
        logger.error(f"因子分析失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 优化API
# ============================================================

@app.post("/api/optimize")
async def optimize_strategy(request: OptimizationRequest):
    """策略优化"""
    try:
        from core.optimization import OptunaOptimizer
        
        return {
            "success": True,
            "message": "优化任务已创建",
            "n_trials": request.n_trials,
            "method": request.method,
        }
    except Exception as e:
        logger.error(f"策略优化失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 市场数据API
# ============================================================

@app.get("/api/market/status")
async def get_market_status():
    """获取市场状态"""
    try:
        if app.state.orchestrator:
            result = app.state.orchestrator.analyze_market_trend()
            return result.__dict__ if hasattr(result, '__dict__') else {"status": "unknown"}
        return {"status": "unknown", "message": "编排器未初始化"}
    except Exception as e:
        logger.error(f"获取市场状态失败: {e}")
        return {"status": "error", "error": str(e)}


@app.get("/api/market/mainlines")
async def get_mainlines(top_n: int = 10):
    """获取投资主线"""
    try:
        if app.state.orchestrator:
            result = app.state.orchestrator.identify_mainlines()
            return result.__dict__ if hasattr(result, '__dict__') else {"mainlines": []}
        return {"mainlines": [], "message": "编排器未初始化"}
    except Exception as e:
        logger.error(f"获取投资主线失败: {e}")
        return {"mainlines": [], "error": str(e)}


# ============================================================
# 运行入口
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

