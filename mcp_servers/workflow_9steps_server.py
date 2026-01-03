# -*- coding: utf-8 -*-
"""
9步投资工作流MCP服务器（真实MCP调用版）
======================================
统一的9步工作流服务，每步调用对应的底层MCP服务器

工作流步骤:
1. 信息获取 (data_source) - data_source_server_v2._handle_health_check
2. 市场趋势 (market_trend) - market_server_v2._handle_status
3. 投资主线 (mainline) - market_server_v2._handle_mainlines
4. 候选池 (candidate_pool) - data_source_server_v2._handle_candidate_pool
5. 因子构建 (factor) - factor_server._handle_recommend
6. 策略生成 (strategy) - strategy_template_server._handle_generate
7. 回测验证 (backtest) - backtest_server._handle_quick
8. 策略优化 (optimization) - optimizer_server._handle_grid_search
9. 报告生成 (report) - report_server._handle_generate

使用主项目venv: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
"""

import json
import logging
import sys
import asyncio
from pathlib import Path

# 导入工作流存储
try:
    from utils.workflow_storage import WorkflowStorage
    STORAGE_AVAILABLE = True
except ImportError:
    STORAGE_AVAILABLE = False
    WorkflowStorage = None
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 确定项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))

# 导入MCP SDK
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logger.warning("MCP SDK不可用，将使用模拟模式")

# ==================== 导入底层MCP服务器处理函数 ====================

# 数据源服务器
try:
    from data_source_server_v2 import _handle_health_check, _handle_candidate_pool
    logger.info("✅ 数据源服务器导入成功")
except ImportError as e:
    logger.warning(f"⚠️ 数据源服务器导入失败: {e}")
    _handle_health_check = None
    _handle_candidate_pool = None

# 市场分析服务器
try:
    from market_server_v2 import _handle_status as _handle_market_status
    from market_server_v2 import _handle_mainlines
    logger.info("✅ 市场服务器导入成功")
except ImportError as e:
    logger.warning(f"⚠️ 市场服务器导入失败: {e}")
    _handle_market_status = None
    _handle_mainlines = None

# 因子服务器
try:
    from factor_server import _handle_recommend
    logger.info("✅ 因子服务器导入成功")
except ImportError as e:
    logger.warning(f"⚠️ 因子服务器导入失败: {e}")
    _handle_recommend = None

# 策略模板服务器
try:
    from strategy_template_server import _handle_generate as _handle_strategy_generate
    from strategy_template_server import _handle_list as _handle_template_list
    logger.info("✅ 策略模板服务器导入成功")
except ImportError as e:
    logger.warning(f"⚠️ 策略模板服务器导入失败: {e}")
    _handle_strategy_generate = None
    _handle_template_list = None

# 回测服务器
try:
    from backtest_server import _handle_quick_backtest as _handle_backtest_quick
    logger.info("✅ 回测服务器导入成功")
except ImportError as e:
    logger.warning(f"⚠️ 回测服务器导入失败: {e}")
    _handle_backtest_quick = None

# 优化服务器
try:
    from optimizer_server import _handle_grid_search
    logger.info("✅ 优化服务器导入成功")
except ImportError as e:
    logger.warning(f"⚠️ 优化服务器导入失败: {e}")
    _handle_grid_search = None

# 报告服务器
try:
    from report_server import _handle_generate as _handle_report_generate
    logger.info("✅ 报告服务器导入成功")
except ImportError as e:
    logger.warning(f"⚠️ 报告服务器导入失败: {e}")
    _handle_report_generate = None


# ==================== 9步工作流定义 ====================

WORKFLOW_9STEPS = [
    {"id": "data_source", "name": "信息获取", "icon": "📡", "color": "#58a6ff", "mcp_tool": "data_source.health_check", "description": "检查数据源连接状态"},
    {"id": "market_trend", "name": "市场趋势", "icon": "📈", "color": "#667eea", "mcp_tool": "market.status", "description": "分析当前市场状态"},
    {"id": "mainline", "name": "投资主线", "icon": "🔥", "color": "#F59E0B", "mcp_tool": "market.mainlines", "description": "识别投资主线"},
    {"id": "candidate_pool", "name": "候选池构建", "icon": "📦", "color": "#a371f7", "mcp_tool": "data_source.candidate_pool", "description": "构建候选股票池"},
    {"id": "factor", "name": "因子构建", "icon": "🧮", "color": "#3fb950", "mcp_tool": "factor.recommend", "description": "推荐量化因子"},
    {"id": "strategy", "name": "策略生成", "icon": "💻", "color": "#d29922", "mcp_tool": "template.generate", "description": "生成策略代码"},
    {"id": "backtest", "name": "回测验证", "icon": "🔄", "color": "#1E3A5F", "mcp_tool": "backtest.quick", "description": "执行回测验证"},
    {"id": "optimization", "name": "策略优化", "icon": "⚙️", "color": "#7C3AED", "mcp_tool": "optimizer.grid_search", "description": "参数优化"},
    {"id": "report", "name": "报告生成", "icon": "📄", "color": "#EC4899", "mcp_tool": "report.generate", "description": "生成研究报告"}
]


# ==================== 工作流状态管理 ====================

class WorkflowSession:
    """工作流会话"""
    
    def __init__(self, workflow_id: str, name: str = "9步投资工作流"):
        self.workflow_id = workflow_id
        self.name = name
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.status = "created"
        self.current_step = 0
        self.context: Dict[str, Any] = {}
        self.steps = [
            {**step, "status": "pending", "result": None, "started_at": None, "completed_at": None, "error": None}
            for step in WORKFLOW_9STEPS
        ]
    
    def to_dict(self) -> Dict:
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "status": self.status,
            "current_step": self.current_step,
            "total_steps": len(self.steps),
            "context": self.context,
            "steps": self.steps,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

_workflows: Dict[str, WorkflowSession] = {}

# 初始化工作流存储
_storage_path = Path(__file__).parent.parent / "data" / "workflows"
_workflow_storage = WorkflowStorage(_storage_path) if STORAGE_AVAILABLE else None




def _save_workflow(workflow_id: str):
    """保存工作流状态到持久化存储"""
    if _workflow_storage and workflow_id in _workflows:
        try:
            _workflow_storage.save_workflow_status(workflow_id, _workflows[workflow_id].to_dict())
        except Exception as e:
            logger.warning(f"保存工作流状态失败: {workflow_id}, 错误: {e}")

def _load_workflows():
    """从持久化存储加载工作流"""
    if not _workflow_storage:
        return
    try:
        saved_workflows = _workflow_storage.list_workflows(limit=100)
        for wf_data in saved_workflows:
            wf_id = wf_data.get("workflow_id")
            if wf_id and wf_id not in _workflows:
                # 恢复工作流会话
                session = WorkflowSession(wf_id, wf_data.get("name", "恢复的工作流"))
                session.status = wf_data.get("status", "created")
                session.current_step = wf_data.get("current_step", 0)
                session.context = wf_data.get("context", {})
                session.steps = wf_data.get("steps", session.steps)
                session.created_at = wf_data.get("created_at", session.created_at)
                session.updated_at = wf_data.get("updated_at", session.updated_at)
                _workflows[wf_id] = session
        logger.info(f"从存储恢复了 {len(saved_workflows)} 个工作流")
    except Exception as e:
        logger.warning(f"加载工作流失败: {e}")

# 启动时加载已保存的工作流
_load_workflows()

# ==================== 步骤执行器（调用真实MCP服务器） ====================

async def execute_step_data_source(args: Dict, context: Dict) -> Dict:
    """步骤1: 检查数据源 - 调用 data_source_server_v2"""
    if _handle_health_check:
        result = await _handle_health_check(args)
        result["summary"] = f"数据源检查完成"
        return result
    return {"success": False, "error": "数据源服务器不可用"}


async def execute_step_market_trend(args: Dict, context: Dict) -> Dict:
    """步骤2: 市场趋势 - 调用 market_server_v2"""
    if _handle_market_status:
        result = await _handle_market_status({"index": args.get("index", "000300.XSHG")})
        result["summary"] = f"市场状态: {result.get('status', result.get('regime', 'N/A'))}"
        return result
    return {"success": False, "error": "市场服务器不可用"}


async def execute_step_mainline(args: Dict, context: Dict) -> Dict:
    """步骤3: 投资主线 - 调用 market_server_v2"""
    if _handle_mainlines:
        result = await _handle_mainlines({"top_n": args.get("top_n", 5)})
        mainlines = result.get("mainlines", [])
        top_name = mainlines[0].get("name", "N/A") if mainlines else "N/A"
        result["summary"] = f"识别{len(mainlines)}条主线，首选: {top_name}"
        return result
    return {"success": False, "error": "市场服务器不可用"}


async def execute_step_candidate_pool(args: Dict, context: Dict) -> Dict:
    """步骤4: 候选池构建 - 调用 data_source_server_v2"""
    if _handle_candidate_pool:
        # 从上下文获取主线
        mainline = args.get("mainline")
        if not mainline and "mainline" in context:
            mainlines = context["mainline"].get("mainlines", [])
            mainline = mainlines[0].get("name", "人工智能") if mainlines else "人工智能"
        
        result = await _handle_candidate_pool({
            "mainline": mainline or "人工智能",
            "limit": args.get("limit", 20)
        })
        return result
    return {"success": False, "error": "数据源服务器不可用"}


async def execute_step_factor(args: Dict, context: Dict) -> Dict:
    """步骤5: 因子推荐 - 调用 factor_server"""
    if _handle_recommend:
        # 从上下文获取市场状态
        market_state = args.get("market_state", "neutral")
        if "market_trend" in context:
            regime = context["market_trend"].get("status", context["market_trend"].get("regime", "neutral"))
            # 转换 bull/bear/neutral 到 risk_on/risk_off/neutral
            if regime == "bull":
                market_state = "bull"
            elif regime == "bear":
                market_state = "bear"
        
        result = await _handle_recommend({
            "market_state": market_state,
            "risk_preference": args.get("risk_preference", "moderate")
        })
        
        factors = result.get("recommendations", [])
        result["factors"] = factors  # 兼容字段
        result["summary"] = f"推荐{len(factors)}个因子"
        return result
    return {"success": False, "error": "因子服务器不可用"}


async def execute_step_strategy(args: Dict, context: Dict) -> Dict:
    """步骤6: 策略生成 - 调用 strategy_template_server"""
    if _handle_strategy_generate:
        # 从上下文获取因子
        factors = args.get("factors", [])
        if not factors and "factor" in context:
            factor_list = context["factor"].get("recommendations", context["factor"].get("factors", []))
            factors = [f.get("id", f.get("name", "momentum")) for f in factor_list[:3]]
        
        if not factors:
            factors = ["momentum", "value"]
        
        result = await _handle_strategy_generate({
            "name": args.get("template", "multi_factor"),
            "params": {"factors": factors, "rebalance_days": args.get("rebalance_days", 5)},
            "platform": args.get("platform", "joinquant")
        })
        
        result["summary"] = f"策略代码生成完成"
        return result
    return {"success": False, "error": "策略模板服务器不可用"}


async def execute_step_backtest(args: Dict, context: Dict) -> Dict:
    """步骤7: 回测验证 - 调用 backtest_server"""
    if _handle_backtest_quick:
        # 从上下文获取候选池股票
        securities = args.get("securities", [])
        if not securities and "candidate_pool" in context:
            stocks = context["candidate_pool"].get("stocks", [])
            securities = [s.get("code") for s in stocks[:10] if s.get("code")]
        
        if not securities:
            securities = ["000001.XSHE", "600000.XSHG"]
        
        result = await _handle_backtest_quick({
            "securities": securities,
            "start_date": args.get("start_date", "2024-01-01"),
            "end_date": args.get("end_date", "2024-06-30"),
            "strategy": args.get("strategy", "momentum")
        })
        
        metrics = result.get("metrics", {})
        total_ret = metrics.get('total_return', 0)
        sharpe = metrics.get('sharpe_ratio', 0)
        # 处理可能的字符串格式
        if isinstance(total_ret, str):
            total_ret = float(total_ret.rstrip('%')) / 100 if '%' in total_ret else float(total_ret)
        if isinstance(sharpe, str):
            sharpe = float(sharpe)
        result["summary"] = f"回测完成: 收益{total_ret:.2%}, 夏普{sharpe:.2f}"
        return result
    return {"success": False, "error": "回测服务器不可用"}


async def execute_step_optimization(args: Dict, context: Dict) -> Dict:
    """步骤8: 策略优化 - 调用 optimizer_server"""
    if _handle_grid_search:
        result = await _handle_grid_search({
            "strategy": args.get("strategy", "momentum"),
            "start_date": args.get("start_date", "2024-01-01"),
            "end_date": args.get("end_date", "2024-06-30"),
            "param_grid": args.get("param_grid", {
                "lookback": [10, 15, 20],
                "top_n": [5, 10]
            })
        })
        
        best_params = result.get("best_params", {})
        result["summary"] = f"优化完成: 最佳参数 {best_params}"
        return result
    return {"success": False, "error": "优化服务器不可用"}


async def execute_step_report(args: Dict, context: Dict) -> Dict:
    """步骤9: 报告生成 - 调用 report_server"""
    if _handle_report_generate:
        try:
            # 汇总上下文数据
            backtest_result = context.get("backtest", {})
            optimization_result = context.get("optimization", {})
            
            result = await _handle_report_generate({
                "title": args.get("title", "韬睿量化研究报告"),
                "format": args.get("format", "html"),
                "metrics": backtest_result.get("metrics", {}),
                "optimization": optimization_result,
                "context": context
            })
            
            if result.get("success"):
                result["summary"] = f"报告已生成"
                return result
        except Exception as e:
            logger.warning(f"报告服务器错误: {e}")
    
    # 使用备用报告生成器
    return _generate_fallback_report(args, context)



def _format_pct(val):
    """格式化百分比"""
    if isinstance(val, str):
        return val
    return f"{float(val):.2%}"

def _format_num(val):
    """格式化数字"""
    if isinstance(val, str):
        return val
    return f"{float(val):.2f}"

def _generate_fallback_report(args: Dict, context: Dict) -> Dict:
    """生成备用报告（当报告服务器不可用时）"""
    from datetime import datetime
    
    report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    report_dir = PROJECT_ROOT / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"{report_id}.html"
    
    # 提取上下文数据
    market = context.get("market_trend", {})
    mainlines = context.get("mainline", {}).get("mainlines", [])
    backtest = context.get("backtest", {})
    metrics = backtest.get("metrics", {})
    
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>韬睿量化研究报告</title>
<style>body{{font-family:sans-serif;background:#0d1117;color:#f0f6fc;padding:40px;}}
.card{{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:24px;margin:20px 0;}}
h1{{color:#58a6ff;}}h2{{color:#8b949e;}}.metric{{font-size:24px;font-weight:bold;color:#3fb950;}}</style></head>
<body><h1>🐉 韬睿量化研究报告</h1>
<p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<div class="card"><h2>📈 市场分析</h2><p>市场状态: {market.get('status', market.get('regime', 'N/A'))}</p></div>
<div class="card"><h2>🔥 投资主线</h2><p>{'、'.join([m.get('name','') for m in mainlines[:5]])}</p></div>
<div class="card"><h2>📊 回测结果</h2>
<p>总收益: <span class="metric">{_format_pct(metrics.get('total_return', 0))}</span></p>
<p>夏普比率: <span class="metric">{_format_num(metrics.get('sharpe_ratio', 0))}</span></p>
<p>最大回撤: <span class="metric">{_format_pct(metrics.get('max_drawdown', 0))}</span></p></div>
<p style="text-align:center;color:#8b949e;">韬睿量化 TRQuant © 2025</p></body></html>"""
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return {
        "success": True,
        "report_id": report_id,
        "file_path": str(report_file),
        "format": "html",
        "summary": f"报告已生成: {report_file.name}"
    }


# 步骤执行器映射
STEP_EXECUTORS = {
    "data_source": execute_step_data_source,
    "market_trend": execute_step_market_trend,
    "mainline": execute_step_mainline,
    "candidate_pool": execute_step_candidate_pool,
    "factor": execute_step_factor,
    "strategy": execute_step_strategy,
    "backtest": execute_step_backtest,
    "optimization": execute_step_optimization,
    "report": execute_step_report,
}


# ==================== MCP工具定义 ====================

if MCP_AVAILABLE:
    server = Server("workflow-9steps-server")
    
    TOOLS = [
        Tool(name="workflow9.get_steps", description="获取9步工作流的所有步骤定义", inputSchema={"type": "object", "properties": {}}),
        Tool(name="workflow9.create", description="创建新的9步工作流会话", inputSchema={"type": "object", "properties": {"name": {"type": "string", "default": "9步投资工作流"}}}),
        Tool(name="workflow9.status", description="获取工作流状态", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="workflow9.run_step", description="执行指定步骤", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}, "step_id": {"type": "string"}, "args": {"type": "object"}}, "required": ["workflow_id", "step_id"]}),
        Tool(name="workflow9.run_all", description="一键执行所有9个步骤", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="workflow9.get_context", description="获取工作流上下文", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="workflow9.list", description="列出所有保存的工作流", inputSchema={"type": "object", "properties": {"limit": {"type": "integer", "default": 20}, "status": {"type": "string"}}}),
        Tool(name="workflow9.restore", description="从存储恢复工作流", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]}),
        Tool(name="workflow9.delete", description="删除保存的工作流", inputSchema={"type": "object", "properties": {"workflow_id": {"type": "string"}}, "required": ["workflow_id"]})
    ]
    
    @server.list_tools()
    async def list_tools():
        return TOOLS
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            result = await _handle_tool(name, arguments)
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        except Exception as e:
            logger.error(f"工具调用失败: {name}, 错误: {e}", exc_info=True)
            return [TextContent(type="text", text=json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))]



# 使用适配器模式（解耦架构）
def _get_workflow_adapter():
    """获取工作流适配器实例（延迟加载）"""
    try:
        from mcp_servers.utils.adapters.workflow_adapter import get_workflow_adapter
        return get_workflow_adapter()
    except ImportError:
        # 如果适配器不可用，返回None，使用直接调用方式
        logger.warning("工作流适配器不可用，使用直接调用方式")
        return None

async def _handle_tool(name: str, args: Dict) -> Dict:
    """处理MCP工具调用"""
    
    """处理MCP工具调用"""
    # 优先使用适配器（解耦架构）
    adapter = _get_workflow_adapter()
    
    # 核心工具使用适配器
    if adapter and name in ["workflow9.get_steps", "workflow9.create", "workflow9.status", 
                            "workflow9.run_step", "workflow9.run_all", "workflow9.get_context"]:
        args.setdefault("version", "v1")
        
        if name == "workflow9.get_steps":
            return await adapter.handle_get_steps(args)
        elif name == "workflow9.create":
            return await adapter.handle_create(args)
        elif name == "workflow9.status":
            return await adapter.handle_status(args)
        elif name == "workflow9.run_step":
            return await adapter.handle_run_step(args)
        elif name == "workflow9.run_all":
            return await adapter.handle_run_all(args)
        elif name == "workflow9.get_context":
            return await adapter.handle_get_context(args)
    
    # 降级：直接调用（向后兼容）
    if name == "workflow9.get_steps":
        return {"success": True, "steps": WORKFLOW_9STEPS, "total": len(WORKFLOW_9STEPS)}
    
    elif name == "workflow9.create":
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
        session = WorkflowSession(workflow_id, args.get("name", "9步投资工作流"))
        _workflows[workflow_id] = session
        _save_workflow(workflow_id)  # 持久化保存
        return {"success": True, "workflow_id": workflow_id, "total_steps": len(WORKFLOW_9STEPS)}
    
    elif name == "workflow9.status":
        workflow_id = args.get("workflow_id")
        if workflow_id not in _workflows:
            return {"success": False, "error": f"工作流不存在: {workflow_id}"}
        return {"success": True, **_workflows[workflow_id].to_dict()}
    
    elif name == "workflow9.run_step":
        workflow_id = args.get("workflow_id")
        step_id = args.get("step_id")
        step_args = args.get("args", {})
        
        if workflow_id not in _workflows:
            return {"success": False, "error": f"工作流不存在: {workflow_id}"}
        if step_id not in STEP_EXECUTORS:
            return {"success": False, "error": f"未知步骤: {step_id}"}
        
        session = _workflows[workflow_id]
        step_index = next((i for i, s in enumerate(session.steps) if s["id"] == step_id), -1)
        
        session.steps[step_index]["status"] = "running"
        session.steps[step_index]["started_at"] = datetime.now().isoformat()
        
        # 执行步骤（调用真实MCP服务器）
        executor = STEP_EXECUTORS[step_id]
        result = await executor(step_args, session.context)
        
        session.steps[step_index]["completed_at"] = datetime.now().isoformat()
        
        if result.get("success", True):
            session.steps[step_index]["status"] = "completed"
            session.steps[step_index]["result"] = result
            session.context[step_id] = result
        else:
            session.steps[step_index]["status"] = "failed"
            session.steps[step_index]["error"] = result.get("error")
        
        session.updated_at = datetime.now().isoformat()
        
        return {"success": True, "step_id": step_id, "step_result": result}
    
    elif name == "workflow9.run_all":
        workflow_id = args.get("workflow_id")
        if workflow_id not in _workflows:
            return {"success": False, "error": f"工作流不存在: {workflow_id}"}
        
        session = _workflows[workflow_id]
        session.status = "running"
        
        results = []
        for step in WORKFLOW_9STEPS:
            step_result = await _handle_tool("workflow9.run_step", {"workflow_id": workflow_id, "step_id": step["id"], "args": {}})
            results.append({
                "step_id": step["id"],
                "step_name": step["name"],
                "success": step_result.get("step_result", {}).get("success", True),
                "summary": step_result.get("step_result", {}).get("summary", "")
            })
        
        session.status = "completed"
        return {"success": True, "workflow_id": workflow_id, "results": results, "completed_steps": len(results)}
    
    elif name == "workflow9.get_context":
        workflow_id = args.get("workflow_id")
        if workflow_id not in _workflows:
            return {"success": False, "error": f"工作流不存在: {workflow_id}"}
        return {"success": True, "context": _workflows[workflow_id].context}
    

    elif name == "workflow9.list":
        limit = args.get("limit", 20)
        status_filter = args.get("status")
        if _workflow_storage:
            workflows = _workflow_storage.list_workflows(limit=limit, status_filter=status_filter)
            return {"success": True, "workflows": workflows, "total": len(workflows)}
        else:
            workflows = [w.to_dict() for w in _workflows.values()]
            return {"success": True, "workflows": workflows[:limit], "total": len(workflows)}
    
    elif name == "workflow9.restore":
        workflow_id = args.get("workflow_id")
        if workflow_id in _workflows:
            return {"success": True, "workflow_id": workflow_id, "message": "工作流已在内存中"}
        if _workflow_storage:
            wf_data = _workflow_storage.load_workflow_status(workflow_id)
            if wf_data:
                session = WorkflowSession(workflow_id, wf_data.get("name", "恢复的工作流"))
                session.status = wf_data.get("status", "created")
                session.current_step = wf_data.get("current_step", 0)
                session.context = wf_data.get("context", {})
                session.steps = wf_data.get("steps", session.steps)
                _workflows[workflow_id] = session
                return {"success": True, "workflow_id": workflow_id, **session.to_dict()}
            return {"success": False, "error": f"工作流不存在: {workflow_id}"}
        return {"success": False, "error": "存储不可用"}
    
    elif name == "workflow9.delete":
        workflow_id = args.get("workflow_id")
        deleted = False
        if workflow_id in _workflows:
            del _workflows[workflow_id]
            deleted = True
        if _workflow_storage:
            _workflow_storage.delete_workflow(workflow_id)
            deleted = True
        return {"success": deleted, "workflow_id": workflow_id}
    
    return {"success": False, "error": f"未知工具: {name}"}


async def main():
    if not MCP_AVAILABLE:
        print("MCP SDK不可用", file=sys.stderr)
        sys.exit(1)
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
