#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工作流直接调用模块
==================
每个步骤直接调用对应的MCP服务器，避免工作流会话问题
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, Any

# 添加路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))

# 工作流上下文（持久化）
_workflow_context: Dict[str, Any] = {}


def get_context() -> Dict[str, Any]:
    """获取工作流上下文"""
    return _workflow_context


def clear_context():
    """清除上下文"""
    global _workflow_context
    _workflow_context = {}


async def execute_step(step_id: str, args: Dict = None) -> Dict:
    """执行单个步骤，直接调用对应的MCP服务器"""
    global _workflow_context
    args = args or {}
    
    try:
        if step_id == "data_source":
            from data_source_server_v2 import _handle_health_check
            result = await _handle_health_check(args)
            result["summary"] = "数据源检查完成"
            
        elif step_id == "market_trend":
            from market_server_v2 import _handle_status
            result = await _handle_status({"index": args.get("index", "000300.XSHG")})
            result["summary"] = f"市场状态: {result.get('status', result.get('regime', 'N/A'))}"
            
        elif step_id == "mainline":
            from market_server_v2 import _handle_mainlines
            result = await _handle_mainlines({"top_n": args.get("top_n", 5)})
            mainlines = result.get("mainlines", [])
            top_name = mainlines[0].get("name", "N/A") if mainlines else "N/A"
            result["summary"] = f"识别{len(mainlines)}条主线，首选: {top_name}"
            
        elif step_id == "candidate_pool":
            from data_source_server_v2 import _handle_candidate_pool
            mainline = args.get("mainline")
            if not mainline and "mainline" in _workflow_context:
                mainlines = _workflow_context["mainline"].get("mainlines", [])
                mainline = mainlines[0].get("name", "人工智能") if mainlines else "人工智能"
            result = await _handle_candidate_pool({
                "mainline": mainline or "人工智能",
                "limit": args.get("limit", 20)
            })
            
        elif step_id == "factor":
            from factor_server import _handle_recommend
            market_state = args.get("market_state", "neutral")
            if "market_trend" in _workflow_context:
                regime = _workflow_context["market_trend"].get("status", "neutral")
                if regime == "bull":
                    market_state = "bull"
                elif regime == "bear":
                    market_state = "bear"
            result = await _handle_recommend({
                "market_state": market_state,
                "risk_preference": args.get("risk_preference", "moderate")
            })
            factors = result.get("recommendations", [])
            result["factors"] = factors
            result["summary"] = f"推荐{len(factors)}个因子"
            
        elif step_id == "strategy":
            from strategy_template_server import _handle_generate
            factors = args.get("factors", [])
            if not factors and "factor" in _workflow_context:
                factor_list = _workflow_context["factor"].get("recommendations", [])
                factors = [f.get("id", f.get("name", "momentum")) for f in factor_list[:3]]
            if not factors:
                factors = ["momentum", "value"]
            result = await _handle_generate({
                "name": args.get("template", "multi_factor"),
                "params": {"factors": factors},
                "platform": args.get("platform", "joinquant")
            })
            result["summary"] = "策略代码生成完成"
            
        elif step_id == "backtest":
            # 使用聚宽数据回测（比BulletTrade快）
            from backtest_server import _handle_jqdata_backtest
            securities = args.get("securities", [])
            if not securities and "candidate_pool" in _workflow_context:
                stocks = _workflow_context["candidate_pool"].get("stocks", [])
                securities = [s.get("code") for s in stocks[:10] if s.get("code")]
            result = await _handle_jqdata_backtest({
                "securities": securities if securities else None,
                "start_date": args.get("start_date", "2024-10-01"),
                "end_date": args.get("end_date", "2024-12-01"),
                "strategy": args.get("strategy", "momentum"),
                "max_positions": args.get("max_positions", 10)
            })
            if result.get("success"):
                metrics = result.get("formatted_metrics", result.get("metrics", {}))
                total_ret = metrics.get("total_return", "0%")
                sharpe = metrics.get("sharpe_ratio", "0")
                result["summary"] = f"聚宽回测: 收益{total_ret}, 夏普{sharpe}"
            else:
                result["summary"] = f"回测失败: {result.get('error', '未知')}"
            
        elif step_id == "optimization":
            from optimizer_server import _handle_grid_search
            result = await _handle_grid_search({
                "strategy": args.get("strategy", "momentum"),
                "start_date": args.get("start_date", "2024-10-01"),
                "end_date": args.get("end_date", "2024-12-31"),
                "param_grid": args.get("param_grid", {
                    "lookback": [10, 15, 20],
                    "top_n": [5, 10]
                })
            })
            best_params = result.get("best_params", {})
            result["summary"] = f"优化完成: 最佳参数 {best_params}"
            
        elif step_id == "report":
            # 生成简单报告
            from datetime import datetime
            report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            report_dir = PROJECT_ROOT / "reports"
            report_dir.mkdir(parents=True, exist_ok=True)
            report_file = report_dir / f"{report_id}.html"
            
            # 从上下文获取数据
            market = _workflow_context.get("market_trend", {})
            mainlines = _workflow_context.get("mainline", {}).get("mainlines", [])
            backtest = _workflow_context.get("backtest", {})
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
<p>总收益: <span class="metric">{metrics.get('total_return', 'N/A')}</span></p>
<p>夏普比率: <span class="metric">{metrics.get('sharpe_ratio', 'N/A')}</span></p>
<p>最大回撤: <span class="metric">{metrics.get('max_drawdown', 'N/A')}</span></p></div>
<p style="text-align:center;color:#8b949e;">韬睿量化 TRQuant © 2025</p></body></html>"""
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            result = {
                "success": True,
                "report_id": report_id,
                "file_path": str(report_file),
                "format": "html",
                "summary": f"报告已生成: {report_file.name}"
            }
        else:
            return {"success": False, "error": f"未知步骤: {step_id}"}
        
        # 保存到上下文
        result["success"] = True
        _workflow_context[step_id] = result
        return result
        
    except Exception as e:
        import traceback
        error_msg = f"步骤{step_id}执行失败: {str(e)}"
        print(f"ERROR: {error_msg}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return {"success": False, "error": error_msg, "traceback": traceback.format_exc()}


def execute_step_sync(step_id: str, args: Dict = None) -> Dict:
    """同步执行步骤"""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(execute_step(step_id, args))
    finally:
        loop.close()


# 供bridge.py调用
def run_workflow_step(params: dict) -> dict:
    """运行工作流步骤"""
    step_id = params.get("step_id")
    args = params.get("args", {})
    
    if not step_id:
        return {"ok": False, "error": "缺少step_id参数"}
    
    try:
        result = execute_step_sync(step_id, args)
        return {"ok": result.get("success", False), "data": result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_workflow_context(params: dict) -> dict:
    """获取工作流上下文"""
    return {"ok": True, "data": get_context()}


def clear_workflow_context(params: dict) -> dict:
    """清除工作流上下文"""
    clear_context()
    return {"ok": True, "data": {"message": "上下文已清除"}}


if __name__ == "__main__":
    # 测试
    import json
    result = execute_step_sync("data_source", {})
    print(json.dumps(result, ensure_ascii=False, indent=2))
