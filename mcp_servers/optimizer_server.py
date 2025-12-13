#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
策略优化 MCP Server

支持策略优化工作流，接收前序步骤信息和回测结果进行优化
"""

import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('OptimizerServer')


class OptimizerServer:
    """策略优化 MCP Server"""
    
    def __init__(self):
        logger.info("策略优化 MCP Server 初始化")
        # TODO: 初始化策略优化引擎
        # from extension.src.services.strategyOptimizer.optimizer import getOptimizationEngine
        # self.engine = getOptimizationEngine()
    
    def list_tools(self) -> List[Dict]:
        """列出所有可用工具"""
        return [
            {
                "name": "optimizer_run",
                "description": "执行策略优化，接收前序步骤信息和回测结果",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "strategy": {
                            "type": "string",
                            "description": "策略代码或策略ID"
                        },
                        "market_context": {
                            "type": "object",
                            "description": "市场上下文（来自步骤2：市场趋势）",
                            "properties": {
                                "regime": {
                                    "type": "string",
                                    "enum": ["risk_on", "risk_off", "neutral"],
                                    "description": "市场状态"
                                },
                                "trend": {
                                    "type": "string",
                                    "description": "市场趋势方向"
                                },
                                "volatility": {
                                    "type": "number",
                                    "description": "市场波动率"
                                }
                            }
                        },
                        "mainlines": {
                            "type": "array",
                            "description": "投资主线列表（来自步骤3：投资主线）",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "score": {"type": "number"},
                                    "industries": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        },
                        "candidate_pool": {
                            "type": "array",
                            "description": "候选股票池（来自步骤4：候选池构建）",
                            "items": {"type": "string"}
                        },
                        "factors": {
                            "type": "array",
                            "description": "因子推荐列表（来自步骤5：因子构建）",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "weight": {"type": "number"},
                                    "category": {"type": "string"}
                                }
                            }
                        },
                        "backtest_result": {
                            "type": "object",
                            "description": "回测结果（来自步骤7：回测验证，用于迭代优化）",
                            "properties": {
                                "total_return": {"type": "number"},
                                "annual_return": {"type": "number"},
                                "max_drawdown": {"type": "number"},
                                "sharpe_ratio": {"type": "number"},
                                "win_rate": {"type": "number"},
                                "total_trades": {"type": "number"}
                            }
                        },
                        "optimization_target": {
                            "type": "object",
                            "description": "优化目标",
                            "properties": {
                                "target_metric": {
                                    "type": "string",
                                    "enum": ["sharpe", "return", "drawdown", "win_rate"],
                                    "description": "目标指标"
                                },
                                "target_value": {"type": "number", "description": "目标值"},
                                "min_sharpe": {"type": "number", "description": "最小夏普比率"},
                                "max_drawdown_limit": {"type": "number", "description": "最大回撤限制"}
                            }
                        },
                        "optimization_algorithm": {
                            "type": "string",
                            "enum": ["grid_search", "random_search", "bayesian", "genetic"],
                            "default": "grid_search",
                            "description": "优化算法"
                        }
                    },
                    "required": ["strategy"]
                }
            },
            {
                "name": "optimizer_get_progress",
                "description": "获取优化进度",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "optimization_id": {
                            "type": "string",
                            "description": "优化任务ID"
                        }
                    },
                    "required": ["optimization_id"]
                }
            },
            {
                "name": "optimizer_get_result",
                "description": "获取优化结果",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "optimization_id": {
                            "type": "string",
                            "description": "优化任务ID"
                        }
                    },
                    "required": ["optimization_id"]
                }
            },
            {
                "name": "optimizer_compare",
                "description": "对比优化前后策略",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "original_strategy": {
                            "type": "string",
                            "description": "原始策略ID或代码"
                        },
                        "optimized_strategy": {
                            "type": "string",
                            "description": "优化后策略ID或代码"
                        }
                    },
                    "required": ["original_strategy", "optimized_strategy"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict) -> Dict:
        """调用工具"""
        logger.info(f"调用工具: {name}")
        
        try:
            if name == "optimizer_run":
                return await self._optimizer_run(arguments)
            elif name == "optimizer_get_progress":
                return await self._optimizer_get_progress(arguments)
            elif name == "optimizer_get_result":
                return await self._optimizer_get_result(arguments)
            elif name == "optimizer_compare":
                return await self._optimizer_compare(arguments)
            else:
                return {"error": f"未知工具: {name}"}
        except Exception as e:
            logger.error(f"工具执行失败: {e}", exc_info=True)
            return {"error": str(e)}
    
    async def _optimizer_run(self, args: Dict) -> Dict:
        """
        执行策略优化
        
        接收前序步骤信息：
        - market_context: 市场状态（步骤2）
        - mainlines: 投资主线（步骤3）
        - candidate_pool: 候选池（步骤4）
        - factors: 因子推荐（步骤5）
        - backtest_result: 回测结果（步骤7，用于迭代优化）
        """
        strategy = args.get("strategy")
        market_context = args.get("market_context")
        mainlines = args.get("mainlines", [])
        candidate_pool = args.get("candidate_pool", [])
        factors = args.get("factors", [])
        backtest_result = args.get("backtest_result")
        optimization_target = args.get("optimization_target", {})
        algorithm = args.get("optimization_algorithm", "grid_search")
        
        logger.info("=" * 60)
        logger.info("⚡ 开始策略优化")
        logger.info("=" * 60)
        logger.info(f"策略: {strategy[:50] if isinstance(strategy, str) and len(strategy) > 50 else strategy}")
        logger.info(f"市场状态: {market_context.get('regime') if market_context else 'N/A'}")
        logger.info(f"投资主线数: {len(mainlines)}")
        logger.info(f"候选股票数: {len(candidate_pool)}")
        logger.info(f"因子数: {len(factors)}")
        logger.info(f"回测结果: {'已提供' if backtest_result else '未提供（首次优化）'}")
        logger.info(f"优化算法: {algorithm}")
        
        # TODO: 调用实际的优化引擎
        # result = await self.engine.optimize(
        #     strategy=strategy,
        #     market_context=market_context,
        #     mainlines=mainlines,
        #     factors=factors,
        #     candidate_pool=candidate_pool,
        #     backtest_result=backtest_result,
        #     optimization_target=optimization_target,
        #     algorithm=algorithm
        # )
        
        # 模拟优化结果
        optimization_id = f"opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = {
            "optimization_id": optimization_id,
            "status": "completed",
            "optimized_strategy": {
                "id": f"strategy_{optimization_id}",
                "code": strategy,  # 实际应该是优化后的代码
                "changes": [
                    "调整因子权重",
                    "优化风控参数",
                    "改进选股逻辑"
                ]
            },
            "optimization_metrics": {
                "iterations": 10,
                "best_sharpe": 1.85,
                "best_return": 0.25,
                "best_drawdown": -0.08
            },
            "received_context": {
                "market_regime": market_context.get("regime") if market_context else None,
                "mainlines_count": len(mainlines),
                "factors_count": len(factors),
                "candidate_pool_size": len(candidate_pool),
                "has_backtest_result": backtest_result is not None
            },
            "message": "策略优化完成（模拟结果）"
        }
        
        logger.info("=" * 60)
        logger.info(f"✅ 策略优化完成: {optimization_id}")
        logger.info("=" * 60)
        
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}
    
    async def _optimizer_get_progress(self, args: Dict) -> Dict:
        """获取优化进度"""
        optimization_id = args.get("optimization_id")
        
        # TODO: 从优化引擎获取实际进度
        progress = {
            "optimization_id": optimization_id,
            "status": "running",
            "current_iteration": 5,
            "total_iterations": 10,
            "progress_percent": 50.0,
            "estimated_time_remaining": "2分钟"
        }
        
        return {"content": [{"type": "text", "text": json.dumps(progress, ensure_ascii=False, indent=2)}]}
    
    async def _optimizer_get_result(self, args: Dict) -> Dict:
        """获取优化结果"""
        optimization_id = args.get("optimization_id")
        
        # TODO: 从优化引擎获取实际结果
        result = {
            "optimization_id": optimization_id,
            "status": "completed",
            "optimized_strategy": {
                "id": f"strategy_{optimization_id}",
                "code": "# 优化后的策略代码..."
            },
            "metrics": {
                "sharpe_ratio": 1.85,
                "total_return": 0.25,
                "max_drawdown": -0.08
            }
        }
        
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]}
    
    async def _optimizer_compare(self, args: Dict) -> Dict:
        """对比优化前后策略"""
        original = args.get("original_strategy")
        optimized = args.get("optimized_strategy")
        
        # TODO: 实际对比逻辑
        comparison = {
            "original_strategy": original,
            "optimized_strategy": optimized,
            "improvements": {
                "sharpe_ratio": {"before": 1.50, "after": 1.85, "improvement": "+23.3%"},
                "total_return": {"before": 0.20, "after": 0.25, "improvement": "+25.0%"},
                "max_drawdown": {"before": -0.12, "after": -0.08, "improvement": "+33.3%"}
            },
            "changes": [
                "因子权重调整：动量因子权重从0.3提升到0.4",
                "风控参数优化：止损线从8%调整到6%",
                "选股逻辑改进：增加主线筛选条件"
            ]
        }
        
        return {"content": [{"type": "text", "text": json.dumps(comparison, ensure_ascii=False, indent=2)}]}


async def handle_request(request: Dict, server: OptimizerServer) -> Dict:
    """处理MCP请求"""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "tools/list":
        return {
            "tools": server.list_tools()
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        result = await server.call_tool(tool_name, arguments)
        return result
    else:
        return {
            "error": {
                "code": -32601,
                "message": f"未知方法: {method}"
            }
        }


async def main():
    """主函数 - 运行MCP Server"""
    logger.info("策略优化 MCP Server 启动...")
    server = OptimizerServer()
    
    # 从stdin读取请求，向stdout写入响应
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
    
    writer_transport, writer_protocol = await asyncio.get_event_loop().connect_write_pipe(
        asyncio.streams.FlowControlMixin, sys.stdout
    )
    writer = asyncio.StreamWriter(writer_transport, writer_protocol, reader, asyncio.get_event_loop())
    
    while True:
        try:
            line = await reader.readline()
            if not line:
                break
            
            request = json.loads(line.decode('utf-8'))
            response = await handle_request(request, server)
            
            if response:
                response_str = json.dumps(response, ensure_ascii=False) + '\n'
                writer.write(response_str.encode('utf-8'))
                await writer.drain()
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}")
        except Exception as e:
            logger.error(f"处理请求错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())





































