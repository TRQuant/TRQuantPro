#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Report Server
=====================

报告管理MCP服务器，提供回测报告、分析报告的生成和管理功能。

运行方式:
    python mcp_servers/report_server.py

工具:
    - report.list: 列出所有报告
    - report.get: 获取报告详情
    - report.generate: 生成报告（输入：backtest_id / strategy_id）
    - report.export: 导出报告（JSON/HTML，PDF后置）
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('ReportServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
except ImportError:
    MCP_SDK_AVAILABLE = False
    logger.error("官方MCP SDK不可用，请安装: pip install mcp")
    sys.exit(1)

# 导入工程化落地件
from mcp_servers.utils.envelope import wrap_success_response, wrap_error_response, extract_trace_id_from_request
from mcp_servers.utils.schema import base_args_schema, merge_schema, requires_confirm_token
from mcp_servers.utils.artifacts import create_artifact_if_needed
from mcp_servers.utils.confirm import verify_confirm_token

# 导入报告生成模块
try:
    from utils.report_generator import generate_html_report
    REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    REPORT_GENERATOR_AVAILABLE = False
    logger.warning("HTML报告生成器不可用")

try:
    from core.report_generator import ReportGenerator
    PDF_REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    PDF_REPORT_GENERATOR_AVAILABLE = False
    logger.warning("PDF报告生成器不可用")

# 报告存储目录
REPORTS_DIR = TRQUANT_ROOT / "results" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 初始化资产链接器（延迟初始化）
_asset_linker: Optional[Any] = None


def get_asset_linker():
    """获取资产链接器实例（单例）"""
    global _asset_linker
    if _asset_linker is None:
        if not ASSET_LINKER_AVAILABLE:
            raise RuntimeError("AssetLinker不可用，请检查依赖")
        if AssetLinker is None:
            raise RuntimeError("AssetLinker不可用，请检查依赖")
        _asset_linker = AssetLinker()
    return _asset_linker


def list_reports() -> List[Dict[str, Any]]:
    """列出所有报告文件"""
    reports = []
    
    # 查找JSON报告文件
    for json_file in REPORTS_DIR.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                summary = data.get("summary", {})
                
                reports.append({
                    "report_id": json_file.stem,
                    "file_path": str(json_file),
                    "strategy": summary.get("strategy", "unknown"),
                    "start_date": summary.get("start_date", ""),
                    "end_date": summary.get("end_date", ""),
                    "total_return": summary.get("total_return", 0.0),
                    "sharpe_ratio": summary.get("sharpe_ratio", 0.0),
                    "max_drawdown": summary.get("max_drawdown", 0.0),
                    "created_at": datetime.fromtimestamp(json_file.stat().st_mtime).isoformat(),
                    "size_bytes": json_file.stat().st_size
                })
        except Exception as e:
            logger.warning(f"无法读取报告文件 {json_file}: {e}")
    
    # 按创建时间排序（最新的在前）
    reports.sort(key=lambda x: x["created_at"], reverse=True)
    
    return reports


def get_report(report_id: str) -> Optional[Dict[str, Any]]:
    """获取报告详情"""
    report_file = REPORTS_DIR / f"{report_id}.json"
    
    if not report_file.exists():
        return None
    
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"读取报告失败: {e}")
        return None


# 创建MCP服务器
server = Server("trquant-report")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    base_schema = base_args_schema(mode="read")
    
    return [
        Tool(
            name="report.list",
            description="列出所有报告",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "strategy": {
                            "type": "string",
                            "description": "策略名称（可选，用于过滤）"
                        },
                        "limit": {
                            "type": "integer",
                            "default": 50,
                            "maximum": 500,
                            "description": "返回数量限制"
                        },
                        "offset": {
                            "type": "integer",
                            "default": 0,
                            "description": "偏移量（分页）"
                        }
                    }
                }
            )
        ),
        Tool(
            name="report.get",
            description="获取报告详情",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "report_id": {
                            "type": "string",
                            "description": "报告ID"
                        }
                    },
                    "required": ["report_id"]
                }
            )
        ),
        Tool(
            name="report.generate",
            description="生成报告（输入：backtest_id / strategy_id）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "backtest_id": {
                            "type": "string",
                            "description": "回测ID（可选）"
                        },
                        "strategy_id": {
                            "type": "string",
                            "description": "策略ID（可选）"
                        },
                        "report_type": {
                            "type": "string",
                            "enum": ["html", "json", "both"],
                            "default": "both",
                            "description": "报告类型"
                        }
                    }
                }
            )
        ),
        Tool(
            name="report.export",
            description="导出报告（JSON/HTML，PDF后置）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "report_id": {
                            "type": "string",
                            "description": "报告ID"
                        },
                        "format": {
                            "type": "string",
                            "enum": ["json", "html", "pdf"],
                            "default": "html",
                            "description": "导出格式"
                        }
                    },
                    "required": ["report_id"]
                }
            )
        ),
        Tool(
            name="report.compare",
            description="对比多个报告",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "report_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要对比的报告ID列表"
                        },
                        "metrics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["total_return", "sharpe_ratio", "max_drawdown", "win_rate"],
                            "description": "要对比的指标列表"
                        }
                    },
                    "required": ["report_ids"]
                }
            )
        ),
        Tool(
            name="report.archive",
            description="归档报告（需要confirm_token）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "report_id": {
                            "type": "string",
                            "description": "报告ID"
                        },
                        "archive_reason": {
                            "type": "string",
                            "description": "归档原因（可选）"
                        },
                        "confirm_token": {
                            "type": "string",
                            "description": "确认令牌（mode=execute时需要）"
                        }
                    },
                    "required": ["report_id"]
                }
            )
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（返回统一envelope格式）"""
    trace_id = arguments.get("trace_id") or extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    artifact_policy = arguments.get("artifact_policy", "pointer")  # 报告默认使用pointer
    
    try:
        if name == "report.list":
            strategy = arguments.get("strategy")
            limit = arguments.get("limit", 50)
            offset = arguments.get("offset", 0)
            
            reports = list_reports()
            
            # 按策略过滤
            if strategy:
                reports = [r for r in reports if r.get("strategy") == strategy]
            
            # 分页
            total = len(reports)
            reports = reports[offset:offset+limit]
            
            result = {
                "reports": reports,
                "total": total,
                "limit": limit,
                "offset": offset,
                "strategy": strategy
            }
            
        elif name == "report.get":
            report_id = arguments.get("report_id")
            if not report_id:
                raise ValueError("缺少必需参数: report_id")
            
            report_data = get_report(report_id)
            if not report_data:
                raise ValueError(f"报告不存在: {report_id}")
            
            # 提取摘要信息
            summary = report_data.get("summary", {})
            metrics = report_data.get("metrics", {})
            
            result = {
                "report_id": report_id,
                "summary": summary,
                "metrics": metrics,
                "strategy": summary.get("strategy", "unknown"),
                "start_date": summary.get("start_date", ""),
                "end_date": summary.get("end_date", ""),
                "total_return": summary.get("total_return", 0.0),
                "sharpe_ratio": summary.get("sharpe_ratio", 0.0),
                "max_drawdown": summary.get("max_drawdown", 0.0),
                "preview": {
                    "total_return": summary.get("total_return", 0.0),
                    "sharpe_ratio": summary.get("sharpe_ratio", 0.0),
                    "max_drawdown": summary.get("max_drawdown", 0.0)
                }
            }
            
            # 如果数据量大，使用artifact
            result = create_artifact_if_needed(report_data, "report", artifact_policy, trace_id)
            # 但保留预览信息
            if isinstance(result, dict) and "artifact_id" in result:
                result["preview"] = {
                    "total_return": summary.get("total_return", 0.0),
                    "sharpe_ratio": summary.get("sharpe_ratio", 0.0),
                    "max_drawdown": summary.get("max_drawdown", 0.0)
                }
            
        elif name == "report.generate":
            backtest_id = arguments.get("backtest_id")
            strategy_id = arguments.get("strategy_id")
            report_type = arguments.get("report_type", "both")
            
            if not backtest_id and not strategy_id:
                raise ValueError("缺少必需参数: backtest_id 或 strategy_id")
            
            # 如果是dry_run模式，只返回生成计划
            if mode == "dry_run":
                result = {
                    "mode": "dry_run",
                    "backtest_id": backtest_id,
                    "strategy_id": strategy_id,
                    "report_type": report_type,
                    "message": "这是dry_run模式，不会实际生成报告",
                    "generation_plan": {
                        "will_generate": True,
                        "formats": report_type.split(",") if isinstance(report_type, str) else [report_type]
                    }
                }
            else:
                # 实际生成报告（简化实现）
                # 这里应该调用实际的报告生成逻辑
                report_id = f"report_{backtest_id or strategy_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # 生成JSON报告（简化）
                json_report = {
                    "report_id": report_id,
                    "backtest_id": backtest_id,
                    "strategy_id": strategy_id,
                    "summary": {
                        "strategy": strategy_id or "unknown",
                        "start_date": "",
                        "end_date": "",
                        "total_return": 0.0,
                        "sharpe_ratio": 0.0,
                        "max_drawdown": 0.0
                    },
                    "generated_at": datetime.now().isoformat()
                }
                
                # 保存JSON报告
                json_file = REPORTS_DIR / f"{report_id}.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(json_report, f, ensure_ascii=False, indent=2)
                
                # 生成HTML报告（如果请求）
                html_file = None
                if report_type in ["html", "both"] and REPORT_GENERATOR_AVAILABLE:
                    try:
                        html_file = REPORTS_DIR / f"{report_id}.html"
                        # 这里应该调用实际的HTML生成逻辑
                        # generate_html_report(...)
                        html_file.write_text("<html><body>报告生成中...</body></html>", encoding='utf-8')
                    except Exception as e:
                        logger.warning(f"HTML报告生成失败: {e}")
                
                result = {
                    "report_id": report_id,
                    "json_file": str(json_file),
                    "html_file": str(html_file) if html_file else None,
                    "summary": json_report["summary"],
                    "generated_at": json_report["generated_at"]
                }
                
                # 链接策略到报告（如果提供了策略ID）
                if ASSET_LINKER_AVAILABLE:
                    try:
                        linker = get_asset_linker()
                        strategy_id = arguments.get("strategy_id")
                        backtest_id = arguments.get("backtest_id")
                        
                        if strategy_id:
                            linker.link_strategy_to_report(
                                strategy_id=strategy_id,
                                report_id=report_id,
                                backtest_id=backtest_id,
                                trace_id=trace_id,
                                metadata={
                                    "generated_at": json_report["generated_at"],
                                    "summary": json_report.get("summary", {})
                                }
                            )
                            result["strategy_id"] = strategy_id
                            result["linked"] = True
                    except Exception as e:
                        logger.warning(f"链接策略到报告失败（可选）: {e}")
                
                # 使用artifact存储完整报告
                result = create_artifact_if_needed(result, "report", artifact_policy, trace_id)
            
        elif name == "report.export":
            report_id = arguments.get("report_id")
            format_type = arguments.get("format", "html")
            
            if not report_id:
                raise ValueError("缺少必需参数: report_id")
            
            report_data = get_report(report_id)
            if not report_data:
                raise ValueError(f"报告不存在: {report_id}")
            
            # 导出逻辑
            if format_type == "json":
                # JSON导出（直接返回数据）
                result = {
                    "report_id": report_id,
                    "format": "json",
                    "data": report_data
                }
                result = create_artifact_if_needed(result, "report", artifact_policy, trace_id)
                
            elif format_type == "html":
                # HTML导出
                if REPORT_GENERATOR_AVAILABLE:
                    html_file = REPORTS_DIR / f"{report_id}_export.html"
                    try:
                        # 这里应该调用实际的HTML生成逻辑
                        # generate_html_report(report_data, ...)
                        html_file.write_text("<html><body>报告导出中...</body></html>", encoding='utf-8')
                        result = {
                            "report_id": report_id,
                            "format": "html",
                            "file_path": str(html_file),
                            "size_bytes": html_file.stat().st_size
                        }
                    except Exception as e:
                        raise RuntimeError(f"HTML导出失败: {e}")
                else:
                    raise RuntimeError("HTML报告生成器不可用")
                    
            elif format_type == "pdf":
                # PDF导出（后置功能）
                if PDF_REPORT_GENERATOR_AVAILABLE:
                    pdf_file = REPORTS_DIR / f"{report_id}_export.pdf"
                    try:
                        generator = ReportGenerator()
                        pdf_path = generator.generate_report(report_data, str(pdf_file))
                        result = {
                            "report_id": report_id,
                            "format": "pdf",
                            "file_path": pdf_path,
                            "size_bytes": Path(pdf_path).stat().st_size if Path(pdf_path).exists() else 0
                        }
                    except Exception as e:
                        raise RuntimeError(f"PDF导出失败: {e}")
                else:
                    raise RuntimeError("PDF报告生成器不可用")
            else:
                raise ValueError(f"不支持的导出格式: {format_type}")
        
        elif name == "report.compare":
            report_ids = arguments.get("report_ids", [])
            metrics = arguments.get("metrics", ["total_return", "sharpe_ratio", "max_drawdown", "win_rate"])
            
            if not report_ids:
                raise ValueError("缺少必需参数: report_ids")
            
            if len(report_ids) < 2:
                raise ValueError("至少需要2个报告ID进行对比")
            
            # 加载所有报告
            reports_data = []
            for report_id in report_ids:
                report_data = get_report(report_id)
                if not report_data:
                    logger.warning(f"报告不存在: {report_id}")
                    continue
                reports_data.append({
                    "report_id": report_id,
                    "data": report_data
                })
            
            if len(reports_data) < 2:
                raise ValueError("至少需要2个有效报告进行对比")
            
            # 对比分析
            comparison = {
                "report_ids": report_ids,
                "metrics": metrics,
                "comparison": []
            }
            
            for report_info in reports_data:
                report_id = report_info["report_id"]
                report_data = report_info["data"]
                summary = report_data.get("summary", {})
                report_metrics = report_data.get("metrics", {})
                
                comparison["comparison"].append({
                    "report_id": report_id,
                    "strategy": summary.get("strategy", "unknown"),
                    "start_date": summary.get("start_date", ""),
                    "end_date": summary.get("end_date", ""),
                    "metrics": {
                        metric: report_metrics.get(metric, summary.get(metric, 0.0))
                        for metric in metrics
                    }
                })
            
            # 使用资产链接器获取报告的血缘关系
            if ASSET_LINKER_AVAILABLE:
                try:
                    linker = get_asset_linker()
                    for comp_item in comparison["comparison"]:
                        report_id = comp_item["report_id"]
                        lineage = linker.get_asset_lineage("report", report_id)
                        comp_item["lineage"] = lineage
                except Exception as e:
                    logger.warning(f"获取报告血缘关系失败（可选）: {e}")
            
            # 找出最佳报告（按第一个指标）
            if comparison["comparison"] and metrics:
                primary_metric = metrics[0]
                best_report = max(
                    comparison["comparison"],
                    key=lambda x: x["metrics"].get(primary_metric, float("-inf"))
                )
                comparison["best"] = {
                    "report_id": best_report["report_id"],
                    "metric": primary_metric,
                    "value": best_report["metrics"].get(primary_metric, 0.0)
                }
            
            comparison = create_artifact_if_needed(comparison, "report", artifact_policy, trace_id)
            result = comparison
        
        elif name == "report.archive":
            report_id = arguments.get("report_id")
            archive_reason = arguments.get("archive_reason", "")
            
            if not report_id:
                raise ValueError("缺少必需参数: report_id")
            
            # 写操作需要confirm_token
            if requires_confirm_token(mode):
                confirm_token = arguments.get("confirm_token")
                if not confirm_token:
                    raise ValueError("mode=execute时需要confirm_token")
                
                ok, err_code = verify_confirm_token(confirm_token, name, arguments, trace_id)
                if not ok:
                    if err_code == "INVALID_TOKEN":
                        raise ValueError("确认令牌无效")
                    elif err_code == "TOKEN_EXPIRED":
                        raise ValueError("确认令牌已过期")
            
            # 检查报告是否存在
            report_data = get_report(report_id)
            if not report_data:
                raise ValueError(f"报告不存在: {report_id}")
            
            # 归档目录
            archive_dir = REPORTS_DIR / "archived"
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            if mode == "dry_run":
                # 模拟归档
                result = {
                    "mode": "dry_run",
                    "report_id": report_id,
                    "archive_reason": archive_reason,
                    "message": "这是dry_run模式，未实际归档报告",
                    "would_move_to": str(archive_dir / f"{report_id}.json")
                }
            else:
                # 实际归档
                report_file = REPORTS_DIR / f"{report_id}.json"
                archive_file = archive_dir / f"{report_id}.json"
                
                # 移动文件
                import shutil
                shutil.move(str(report_file), str(archive_file))
                
                # 更新报告数据，添加归档信息
                report_data["archived"] = True
                report_data["archived_at"] = datetime.now().isoformat()
                report_data["archive_reason"] = archive_reason
                
                # 保存归档后的报告
                archive_file.write_text(
                    json.dumps(report_data, ensure_ascii=False, indent=2),
                    encoding='utf-8'
                )
                
                # 记录证据
                try:
                    sys.path.insert(0, str(TRQUANT_ROOT / "scripts"))
                    from mcp_call import MCPClient
                    
                    client = MCPClient("trquant-evidence")
                    evidence_content = {
                        "action": "archive_report",
                        "report_id": report_id,
                        "archive_reason": archive_reason,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    client.call_tool("evidence.record", {
                        "title": f"归档报告: {report_id}",
                        "type": "report_archive",
                        "content": json.dumps(evidence_content, ensure_ascii=False, indent=2),
                        "related_change": trace_id,
                        "tags": ["report", "archive"]
                    })
                    client.close()
                except Exception as e:
                    logger.warning(f"记录证据失败（可选）: {e}")
                
                result = {
                    "mode": "execute",
                    "report_id": report_id,
                    "archived": True,
                    "archive_path": str(archive_file),
                    "message": "报告已归档"
                }
            
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-report",
            tool_name=name,
            version="1.0.0",
            trace_id=trace_id
        )
        
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
    except ValueError as e:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message=str(e),
            server_name="trquant-report",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查输入参数是否符合工具Schema要求",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except RuntimeError as e:
        envelope = wrap_error_response(
            error_code="DEPENDENCY_ERROR",
            error_message=str(e),
            server_name="trquant-report",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查报告生成器依赖是否已安装",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        logger.exception(f"工具调用失败: {name}")
        envelope = wrap_error_response(
            error_code="INTERNAL_ERROR",
            error_message=str(e),
            server_name="trquant-report",
            tool_name=name,
            version="1.0.0",
            error_hint="服务器内部错误，请查看日志",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]


async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())




