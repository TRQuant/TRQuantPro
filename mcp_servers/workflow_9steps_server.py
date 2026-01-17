# -*- coding: utf-8 -*-
"""
9步投资工作流MCP服务器（独立版本）
======================================
统一的9步工作流服务

工作流步骤:
1. 信息获取 (data_source) - 获取市场数据
2. 市场趋势 (market_trend) - 分析市场趋势
3. 投资主线 (mainline) - 确定投资主线
4. 投资标的筛选 (target_selection) - 筛选投资标的
5. 因子构建 (factor) - 构建量化因子
6. 策略生成 (strategy) - 生成交易策略
7. 回测验证 (backtest) - 回测策略表现
8. 策略优化 (optimization) - 优化策略参数
9. 报告生成 (report) - 生成投资报告

跨平台兼容：Windows/Linux
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

# 配置日志
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('WorkflowServer')

# 确定项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
    logger.info("MCP SDK加载成功")
except ImportError as e:
    logger.error(f"MCP SDK不可用: {e}")
    logger.error("请确保使用venv中的Python，并安装MCP SDK:")
    logger.error("  pip install mcp")
    logger.error(f"当前Python路径: {sys.executable}")
    sys.exit(1)

# 创建服务器
server = Server("trquant-workflow")

# 工作流状态存储
WORKFLOW_SESSIONS = {}

# 9步工作流定义
WORKFLOW_STEPS = {
    1: {"name": "data_source", "title": "信息获取", "description": "获取市场数据和基础信息"},
    2: {"name": "market_trend", "title": "市场趋势", "description": "分析当前市场趋势和情绪"},
    3: {"name": "mainline", "title": "投资主线", "description": "确定投资主线和方向"},
    4: {"name": "target_selection", "title": "投资标的筛选", "description": "筛选符合条件的投资标的"},
    5: {"name": "factor", "title": "因子构建", "description": "构建量化因子"},
    6: {"name": "strategy", "title": "策略生成", "description": "生成交易策略"},
    7: {"name": "backtest", "title": "回测验证", "description": "回测策略历史表现"},
    8: {"name": "optimization", "title": "策略优化", "description": "优化策略参数"},
    9: {"name": "report", "title": "报告生成", "description": "生成投资报告"}
}

# 定义工具
TOOLS = [
    Tool(
        name="workflow.start",
        description="开始新的9步投资工作流",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "工作流名称"},
                "description": {"type": "string", "description": "工作流描述"}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="workflow.status",
        description="获取工作流当前状态",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "工作流会话ID"}
            },
            "required": ["session_id"]
        }
    ),
    Tool(
        name="workflow.step",
        description="执行工作流的下一步",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "工作流会话ID"},
                "step": {"type": "integer", "description": "步骤编号(1-9)"},
                "params": {"type": "object", "description": "步骤参数"}
            },
            "required": ["session_id", "step"]
        }
    ),
    Tool(
        name="workflow.list_steps",
        description="列出所有工作流步骤",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="workflow.complete",
        description="完成工作流并生成摘要",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "工作流会话ID"}
            },
            "required": ["session_id"]
        }
    )
]


@server.list_tools()
async def list_tools():
    """列出所有工具"""
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    try:
        if name == "workflow.start":
            result = _handle_start(arguments.get("name", ""), arguments.get("description", ""))
        elif name == "workflow.status":
            result = _handle_status(arguments.get("session_id", ""))
        elif name == "workflow.step":
            result = _handle_step(
                arguments.get("session_id", ""),
                arguments.get("step", 1),
                arguments.get("params", {})
            )
        elif name == "workflow.list_steps":
            result = _handle_list_steps()
        elif name == "workflow.complete":
            result = _handle_complete(arguments.get("session_id", ""))
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        logger.error(f"工具调用失败: {name}, 错误: {e}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


def _handle_start(name: str, description: str = "") -> Dict:
    """开始新的工作流"""
    session_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    
    session = {
        "id": session_id,
        "name": name,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "current_step": 0,
        "status": "started",
        "steps_completed": [],
        "results": {}
    }
    
    WORKFLOW_SESSIONS[session_id] = session
    logger.info(f"工作流已启动: {session_id}")
    
    return {
        "success": True,
        "session_id": session_id,
        "message": f"工作流 '{name}' 已启动",
        "next_step": {
            "step": 1,
            **WORKFLOW_STEPS[1]
        }
    }


def _handle_status(session_id: str) -> Dict:
    """获取工作流状态"""
    if session_id not in WORKFLOW_SESSIONS:
        return {"success": False, "error": f"工作流不存在: {session_id}"}
    
    session = WORKFLOW_SESSIONS[session_id]
    current_step = session["current_step"]
    
    return {
        "success": True,
        "session": session,
        "current_step": current_step,
        "next_step": WORKFLOW_STEPS.get(current_step + 1) if current_step < 9 else None,
        "progress": f"{current_step}/9",
        "progress_percent": round(current_step / 9 * 100, 1)
    }


def _handle_step(session_id: str, step: int, params: Dict = None) -> Dict:
    """执行工作流步骤"""
    if session_id not in WORKFLOW_SESSIONS:
        return {"success": False, "error": f"工作流不存在: {session_id}"}
    
    if step < 1 or step > 9:
        return {"success": False, "error": f"无效的步骤编号: {step}，有效范围: 1-9"}
    
    session = WORKFLOW_SESSIONS[session_id]
    step_info = WORKFLOW_STEPS[step]
    
    # 模拟执行步骤
    result = _execute_step(step, params or {})
    
    # 更新会话状态
    session["current_step"] = step
    session["steps_completed"].append(step)
    session["results"][step_info["name"]] = result
    
    logger.info(f"工作流 {session_id} 完成步骤 {step}: {step_info['title']}")
    
    return {
        "success": True,
        "session_id": session_id,
        "step": step,
        "step_info": step_info,
        "result": result,
        "next_step": WORKFLOW_STEPS.get(step + 1) if step < 9 else None,
        "progress": f"{step}/9",
        "progress_percent": round(step / 9 * 100, 1)
    }


def _execute_step(step: int, params: Dict) -> Dict:
    """执行具体步骤（模拟）"""
    step_info = WORKFLOW_STEPS[step]
    
    # 根据步骤返回模拟结果
    if step == 1:  # 信息获取
        return {
            "status": "completed",
            "data_sources": ["jqdata", "tushare"],
            "market_status": "open",
            "timestamp": datetime.now().isoformat()
        }
    elif step == 2:  # 市场趋势
        return {
            "status": "completed",
            "trend": "bullish",
            "sentiment": "neutral",
            "volatility": "low",
            "recommendation": "适合投资"
        }
    elif step == 3:  # 投资主线
        return {
            "status": "completed",
            "mainlines": [
                {"name": "科技创新", "weight": 0.4},
                {"name": "消费升级", "weight": 0.3},
                {"name": "绿色能源", "weight": 0.3}
            ]
        }
    elif step == 4:  # 投资标的筛选
        return {
            "status": "completed",
            "candidates": [
                {"code": "000001.XSHE", "name": "平安银行", "score": 85},
                {"code": "600519.XSHG", "name": "贵州茅台", "score": 90},
                {"code": "000858.XSHE", "name": "五粮液", "score": 82}
            ],
            "total": 3
        }
    elif step == 5:  # 因子构建
        return {
            "status": "completed",
            "factors": [
                {"name": "momentum", "weight": 0.3},
                {"name": "value", "weight": 0.25},
                {"name": "quality", "weight": 0.25},
                {"name": "size", "weight": 0.2}
            ]
        }
    elif step == 6:  # 策略生成
        return {
            "status": "completed",
            "strategy": {
                "name": "多因子策略",
                "type": "multi_factor",
                "rebalance": "monthly",
                "top_n": 10
            }
        }
    elif step == 7:  # 回测验证
        return {
            "status": "completed",
            "backtest": {
                "period": "2020-01-01 to 2024-12-31",
                "annual_return": 0.156,
                "sharpe_ratio": 1.23,
                "max_drawdown": -0.15,
                "win_rate": 0.62
            }
        }
    elif step == 8:  # 策略优化
        return {
            "status": "completed",
            "optimization": {
                "best_params": {"momentum_period": 20, "top_n": 15},
                "improved_sharpe": 1.35,
                "improved_return": 0.178
            }
        }
    elif step == 9:  # 报告生成
        return {
            "status": "completed",
            "report": {
                "title": "投资策略报告",
                "generated_at": datetime.now().isoformat(),
                "summary": "策略回测表现良好，建议实盘验证"
            }
        }
    
    return {"status": "completed", "step": step}


def _handle_list_steps() -> Dict:
    """列出所有工作流步骤"""
    return {
        "success": True,
        "total_steps": 9,
        "steps": [
            {"step": k, **v} for k, v in WORKFLOW_STEPS.items()
        ]
    }


def _handle_complete(session_id: str) -> Dict:
    """完成工作流"""
    if session_id not in WORKFLOW_SESSIONS:
        return {"success": False, "error": f"工作流不存在: {session_id}"}
    
    session = WORKFLOW_SESSIONS[session_id]
    session["status"] = "completed"
    session["completed_at"] = datetime.now().isoformat()
    
    logger.info(f"工作流已完成: {session_id}")
    
    return {
        "success": True,
        "session_id": session_id,
        "status": "completed",
        "summary": {
            "name": session["name"],
            "steps_completed": len(session["steps_completed"]),
            "created_at": session["created_at"],
            "completed_at": session["completed_at"],
            "results": session["results"]
        }
    }


async def main():
    """主入口"""
    logger.info("Workflow Server启动中...")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
